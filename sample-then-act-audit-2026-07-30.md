# Sample-then-act audit — Tightbeam Elixir substrate

**Status:** Audit, read-only. Tree `/Users/mike/src/tightbeam_ex` @ `16b82d1c674822499b7b4119f1411ce8ea1e63a7`, 2026-07-30. No code changed; nothing in this audit edited `lib/`, `cli/`, or any file in the repo.

**READING NOTE — confidence gradations.** Tier 1 items **F1, F2, F3, F4, F6** plus **F7, F10, F13, F16, F19, F20** and the quarantine finding were re-read and confirmed personally, line by line, against the tree at the SHA above. **F8, F11, F12, F14, F15, F17, F18, F21–F27** are agent-reported with quoted evidence that was *not* independently re-opened — high-confidence leads, but not verified to the same standard. The Suspicions section names mechanisms for which no interleaving was established; it is retained deliberately, because a named mechanism without an established interleaving is exactly the thing that gets rediscovered later. The quarantine finding in §1 is a *documented contract that does not exist in code* — a different and arguably worse class than the races around it.

---

**Tree:** `/Users/mike/src/tightbeam_ex`, branch `main`, **SHA `16b82d1c674822499b7b4119f1411ce8ea1e63a7`** (2026-07-30 06:38:53 -0700). Working tree carries two uncommitted edits, both under `priv/kungfu/agentic-engineering/guidance/` (another lane's work) — nothing in `lib/` or `cli/`. Read-only throughout; nothing was edited.

---

## 1. Fact / owner inventory

Thirteen processes hold mutable state. Only **four** own facts that anyone else reads.

| Owner | Facts it owns | Serialization boundary |
|---|---|---|
| `Tightbeam.SessionLane` (per session, `LaneRegistry`) | `task_ref` (= "a turn is running"), `current_seq`, `current_message_id`, `quarantined` | its own callback only |
| `Tightbeam.AdapterCoordinator` | per-key `generation`, `ready`, `circuit`, `failures`, `pid`, `last_failure`, `epoch`, load semaphore | its own callback only |
| `Tightbeam.Acp.Adapter` | `known` (which harness sids exist), `chunks`, `progress`, `conn` pid | its own callback only |
| `Tightbeam.Acp.Conn` | `pending` (in-flight ACP requests), `port`, `closed` | its own callback only |
| `Tightbeam.RailEpisodes` | `incarnation`, `seq`, `last_summon` | its own callback; **positions minted before the check** |
| `Tightbeam.TurnObservations` | `windows` | its own callback; **deadline re-checked adjacent to mutation** |
| `Tightbeam.Credentials` | `pending` (onboarding leases). *Status/kind are NOT owned* — they live in `credential.json`, possibly over ssh | its own callback |
| `Tightbeam.ModelCatalog` | `entries` (a declared TTL cache of a remote fact) | its own callback |
| SQLite via `Tightbeam.DB` | `turns.status`, `sessions.state`/`adjudicationHold`/`model`/`harness`, `wakes.state`, `decision_requests.status`, `rail_remedy_episodes.status`+`occurrence`, `adjudication_episodes.status`+`correlationKey`, `assignments.state`, `artifacts.state` | **only inside `DB.transaction`/`Txn.q`**; every read via `DB.query` is a sample |
| `Supervision`, `Wakes`, `LaneManager`, `DB` | own only immutable config + timers | — |

Two of these are stated but not real:

- **`SessionLane.quarantined` is never set to `true`.** It is initialised `false` at `session_lane.ex:37`, read at `:158`, and written nowhere in `lib/`. `Conn.pending_count/1` (`acp/conn.ex:66`) has **zero production callers**; `{:acp_orphan_resolved, sid}` and `{:acp_late_reply, method}` (`acp/conn.ex:207-208`) are emitted to the Adapter, whose catch-all `handle_info(_msg, state)` (`acp/adapter.ex:514`) drops them. The moduledoc contract at `session_lane.ex:15-19` — "the lane will not start the next queued turn until the orphaned ACP request is observed resolved" — **does not exist in code.** After a `failed_unknown`, the next turn prompts an adapter that may still hold an unresolved request for that session. This is the degenerate case of the defect: nobody asks the owner at all.
- **`ConnRegistry.register/2`'s moduledoc** (`conn_registry.ex:45-50`) says the caller sends `session_replaced`+close to `replaced`; `wire/socket.ex:283` discards it. Doc drift, no race.

---

## 2. Samplers (public reads of a fact the caller does not own)

`SessionLane.cancel_current/1` :78, `nudge/1` :61 · `Registry.lookup(LaneRegistry,…)` :62/:79, `lane_manager.ex:92` · `AdapterCoordinator.adapter_for/2` :75, `generation/2` :81, `ready_token/2` :115, `last_failure/3` :128, `health/1` :102 · `Acp.Adapter.knows_session?/2` :198, `conn/1` :211 · `Acp.Conn.pending_count/1` :66 · `TurnObservations.evidence/3` :110 · `Credentials.status/2` :58, `kind/2` :69 · `ModelCatalog.get/1` :47, `get/3` :56, `member?/4` :79, `entry/4` :86 · `Application.draining?/0` :101 · `Archetypes.get/1` :135 · `Ledger.pending_count/2` :448, `running_turn_message_id/2` :484, `pending_sessions/1` :439, `last_terminal_seq/2` :461, `prior_adapter_generation/3` :533, `unpublished_terminals/1` :500 · `RailRemedy.live?/3` :51 · `Escalation.open_episodes/2`, `resolve/3` · `Adjudication.get_by_correlation/2`, `open_for_session?/2` · `Org.get/2`, `current_pointer/2`, `list_for_user/3` · `Assignments.oldest_open/2`, `open_count/2` · `Wakes.pending_count/2`, `self_pending_count/2` · `DB.changes/1` :69 (a public sampler of the connection's last-statement count, no production caller — a trap for the next one; `Txn.changes/1` is the correct read).

---

## 3. RACY findings, ranked by consequence

### Tier 1 — silent, high-consequence

**F1 · `park_escalation` mints a fact cursor after the fact it waits for was already filed → a 24-hour park.** *(verified personally)*
- READ: `rules.ex:841` `Escalation.resolve(db, call, rule)` → `escalation.ex:144` returns `{:needs_request, id}` for a request read as `status='open'`.
- ACT: `supervision.ex:419-451` opens its **own** transaction, reads only `deadlineAt, parkWakeId` (`:421-426`) — **never re-asserts `status='open'`** — and schedules the park wake, which stamps `conditionAfterId = MAX(condition_facts.id)` (`wakes.ex:184`).
- Interleaving: between `Rules.decide` returning and that transaction (a lifecycle write plus a txn open), the owner rules the request. `escalation.ex:752-770` CASes `status='ruled'` and files the one-and-only `escalation-ruled` fact at id *N*. `park_escalation` then sets `conditionAfterId ≥ N`. The matcher requires `f.id > w.conditionAfterId` (`wakes.ex:670`, `:703`). There is exactly one such fact per request (`rulingFactId` is written once), so **the condition can never match**.
- Consequence: **availability.** The park wake fires only on its fallback `due_at = deadlineAt` = `@default_decision_deadline_ms` = **86 400 000 ms / 24 h** (`escalation.ex:13`). The session sits parked for a day after an escalation answered in seconds, invisibly — request reads `ruled`, wake reads `pending`, nothing logs the mismatch. `Escalation.nudge` fires the fact *before* the park wake exists, so the eager path cannot rescue it. Window is only a few DB round trips, but the failure is total and undetectable.

**F2 · Adapter → Credentials → AdapterCoordinator → same Adapter is a closed call cycle that wedges the shared serializer.** *(verified personally, full path)*
- `acp/adapter.ex:527-533` invokes `on_auth_event` **inside the adapter's own `handle_info`**, untrapped → `placement.ex:1078-1086` → `Credentials.mark_terminal/3` = `GenServer.call`, 5 s default (`credentials.ex:128`) → `credentials.ex:210` `state.park.(provider)` → `gateway.ex:418` → `gateway.ex:3358-3367` `stop_provider_runtime` → `AdapterCoordinator.close_adapter` (`GenServer.call`) → `adapter_coordinator.ex:310` `Tightbeam.Acp.Adapter.conn(pid)` = `GenServer.call(A, :conn)` with **no timeout argument** (`acp/adapter.ex:211`). A is blocked in its own `handle_info`. Deadlock.
- `stop_provider_runtime` targets `{module.id(), "shared", machine}` — by construction the key of the adapter that raised the event. Not an exotic interleaving.
- Consequence: **T-CONCURRENCY violation, direct.** The AdapterCoordinator is the serializer every lane calls for `adapter_for/2` — one harness's credential event stalls every session on every harness for the full 5 s. Also violates `docs/PATTERNS.md` §"Shared serializers never touch the slow world". Secondary: the `catch :exit` at `adapter_coordinator.ex:313-315` aborts the whole `try`, so `Conn.close`, `GenServer.stop(conn)` and `GenServer.stop(pid)` at `:311-313` never run; the monitor was already `demonitor(…, [:flush])`'d at `:308`, so when A dies of its own timeout there is **no `adapter_down` lifecycle row and no failure count** — a credential revocation is recorded as a clean planned teardown.

**F3 · `adjudicate_swap` mutates the live harness before the ruling CAS; the rollback cannot undo it.** *(verified personally; independently found by the gateway sweep)*
- READ: `gateway.ex:3828` `episode.status != "notified"`, outside any transaction.
- ACT: `gateway.ex:4046` `strict_apply_current_model(db, session, call.params.model)` → `gateway.ex:4806-4818` issues a live JSON-RPC `Adapter.apply_model_strict` **before** `ruling_transaction` opens at `:4049`, whose `Adjudication.resolve_in_txn` at `:4075` raises `superseded_or_stale` if a heal won.
- Interleaving: `on_adapter_ready` (`gateway.ex:285`) fires a Task → `adapter_healed` → `release_hold` commits `heal_resolve_in_txn`, landing after `:3828` read `notified` and after `:4814` already switched the harness.
- Consequence: **correctness + T-SOURCE.** `sessions.model` says the old ref, the adapter runs the new one, no tiebreak; the operator is told `"stale or unknown adjudication episode"` (`:3871`). The comment at `gateway.ex:3861-3865` explicitly claims "the transaction already rolled back, so nothing partial survives" — **that claim is false for the pre-transaction adapter mutation.** Every sibling ruling path (`stop`, `park`, `respawn`) does all mutation inside `ruling_transaction`; this is the one that does not.

**F4 · `contain.rs:254` SIGKILLs a process group whose pid it already released.** *(verified personally)*
```rust
228:  match child.try_wait() {
229:      Ok(Some(child_status)) => status = Some(child_status),   // waitpid(WNOHANG) REAPS — pid P freed here
...
253:  if started.elapsed() >= args.timeout {
254:      let pgid = child.id() as libc::pid_t;                    // stale integer
257:      libc::killpg(pgid, libc::SIGKILL);
```
The loop deliberately stays armed after the leader exits — that is what `cli/src/contain.rs:1446 timeout_stays_armed_when_the_leader_exits_before_a_descendant` tests. So the reaped-pid path is the *intended* one. Interleaving: the check script forks a daemon holding stdout and `exit 0`; `try_wait` reaps at t≈5 ms; readers never see EOF; the wrapper spins in 2 ms sleeps until `--timeout-ms`; on a busy host (Linux default `pid_max` 32768; eezo runs at load ≈44 under parallel lanes) P is handed to a new group leader; `killpg(P, SIGKILL)` kills an unrelated group. Consequence: **correctness and availability off the containment seam**, unhandleable signal, and the report says only `SCRIPT_TIMEOUT`. Sibling at `:231-238` is safe (nothing reaped); `ceremonies.rs:308-314` is safe (returns on `Ok(Some(_))`). This is the sole pid→signal path in `cli/src`.

**F5 · The timed wake path delivers a wake that has been canceled.** *(mechanism verified personally; cancel writers per the sweeps sampling)*
- READ: `wakes.ex:512-518` selects `state = 'pending' AND dueAt <= ?1`.
- ACT: `wakes.ex:526` `attempt_delivery(fn -> deliver.(wake) end)` → `gateway.ex:899` `Ledger.enqueue_in_txn` **unconditionally**; `mark_fired`'s `AND state='pending'` guard runs at `:540`, after the turn already exists. Even the "atomic" variant (`gateway.ex:911-917`) puts its guarded UPDATE *after* the enqueue and discards the result.
- Interleaving: the loop is still working through earlier rows (each a full delivery transaction; an `effort_probe` consumer costs up to 8 s of ssh, `effort_checkin.ex:283` → `placement.ex:286`). Meanwhile a gateway transaction cancels W — `effort_checkin.ex:197`/`:549`/`:574`, `adjudication.ex:613-618` (which cancels the superseded heal-retry precisely to enforce "at most one pending retry").
- Consequence: **correctness.** The durable row says `canceled`; the agent got the prompt and burned a turn. Note the asymmetry: the *condition*-wake path (`wakes.ex:749-763`) re-reads and CASes inside one transaction and is correct. Only the legacy timed path has the hole.

**F6 · `RailRemedy.close/3` is the one transition in its module without occurrence scoping.** *(verified personally)*
- READ: `rules.ex:912-918` `maybe_close/4` calls `RailRemedy.live?(db, rule.name, subject)` during `Rules.decide`.
- ACT: `dispatch.ex:96` (and `supervision.ex:417`) `RailRemedy.close(db, statute, subject)` — `rail_remedy.ex:64-74`, `UPDATE … WHERE statute=?1 AND subject=?2 AND status='live'`. **No `occurrence`, no `claimToken`** — while `rail_remedy.ex:107`, `:126`, `:154`, `:181`, `:213`, `:231`, `:336` all carry one. The lifecycle *cycles* (`closed → claimed → dispatched → live → closed`), which is exactly why `occurrence` exists.
- Interleaving: `maybe_close` for rule 1 sees occurrence *N* live. `decide_rules(rest, …)` continues folding; each later rule with a check spawns a `RailScript.run` subprocess (seconds). In that window another passing dispatch on the same subject closes *N*; a third dispatch's deny fires the remedy → `claim(closed)` → occurrence *N+1*, dispatched, live. Our stale close then wins the CAS against *N+1*.
- Consequence: **correctness + legibility.** A remedy episode for a real, unrepaired violation is stamped `closed`/`closedAt`; the producer stays outstanding; the next violation opens *N+2* and dispatches a **second** producer instead of rewaking. The comment at `rules.ex:773` claims this is "the same shape `maybe_close/4` uses for remedy episodes" — but the malfunction path mints a `RailEpisodes.evaluating` position before the check and this one does not. The fix is one predicate, not a redesign.

### Tier 2 — correctness, bounded or noisy

**F7 · `cancel` interrupts the *next* turn at the harness.** `gateway.ex:1631` consumes the lane's "a turn is running" fact outside the callback that produced it; `gateway.ex:1665` then sends ACP `session/cancel`, which carries only `sessionId` — no turn identity. Between them: `Projection.get`, `publish_turn_state`, `Org.get`, two broadcasts, `Org.current_pointer`, `AdapterCoordinator.adapter_for` (a `GenServer.call`), `Adapter.conn` (another). Meanwhile the lane has already killed the task, processed its own `:DOWN`, and `maybe_start` claimed queued turn *N+1* onto the same sid. Consequence: turn *N+1* is interrupted; it records `failed`. The comment at `:1628-1629` ("the substrate's truth is the ledger row either way") defends the ledger, not the harness side effect on a different turn. Also: `adapter_for` is not a read — it **lazily boots** an adapter (`adapter_coordinator.ex:247`), so cancelling after an adapter death spawns a fresh harness process as a side effect and then times out in `Adapter.conn` (5 s default, adapter inside a 185 s `handle_continue`), swallowed by the `rescue`/`catch` at `:1669-1673`.

**F8 · Every gate in the supervision prod ladder is stale across a `RailScript.run`.** *(agent-reported, quoted evidence)* `supervision.ex:209` (`Ledger.pending_count == 0`), `:318` (`Wakes.pending_count == 0`), `:342` (`Adjudication.open_for_session?`), `:353` (`Wakes.self_pending_count`) are all read before `Rules.decide` at `:365`, which spawns the statute check subprocess, and acted on at `:687`/`:370`/`:380`. Consequences: a prod delivered to a session that is mid-turn or has already scheduled its continuation; `prodCount` advanced (`:725`) and the ladder walked toward the spawner on a strand that never stalled; in the `:342` case the prod turn is admitted by `claim_next`'s hold filter only if `wakeId = adjudicationHold`, so it sits **queued indefinitely** — a non-terminal row `Ledger.non_terminal_older_than/2` is documented to require be empty. `supervision.ex:591` (the drain path) never samples busy at all. `supervision.ex:353` is the worst of the four: it gates `RailRemedy.fire`, which **staffs work** (assign/spawn/wake).

**F9 · `identity apply` — KNOWN, in flight.** `gateway.ex:2051` `Ledger.pending_count`, acted on at `:2122-2124` `close_session`/`load_session`, across `Identity.live_revision!`, `Placement.holder_workdir` (may rsync), `served_snapshot`, `adapter_for`, `knows_session?` — per session, for `--all`. Listed only as the pattern exemplar; do not re-litigate.

**F10 · Session-cap and `order_index` read outside the transaction that creates.** `gateway.ex:2749` reads `length(Org.list_for_user(...)) >= max_live_sessions_per_user`; `:2808` reads `sessions` again for `order_index: length(sessions)` (`:2828`); the transaction at `:2839` re-checks **only idempotency**. Between: `validate_credential` (may be an ssh round trip), `validate_catalog_model`, and `Spinup.ensure_ready` (process spawn / ssh, seconds). Two concurrent spawns with different idempotency keys both pass and both commit → cap breached by the concurrency, and both rows get the same `order_index`, making stream order nondeterministic.

**F11 · `Adapter.knows_session?` → act, on all three residency paths.** `gateway.ex:1790→1801`, `:2121→2122`, `:3210→3212/3219`. `known` is mutated from other processes (`acp/adapter.ex:337`, `:356`, `:360`, `:377`). The `true` branch has **no fallback** — the "harness lost the session" recovery (`gateway.ex:1817-1834`) exists only on the `load_session` error path — so a concurrent `reap_adapter_sessions` (`gateway.ex:4655`) or identity-apply close leaves the lane prompting a closed sid.

**F12 · `adapter_key` sampled at turn start, used to build the hold cause minutes later.** `gateway.ex:1329`/`:1363`, consumed at `:1406` and `:1493`, across an `Adapter.prompt` with a 600 000 ms timeout. A mid-turn `tune set_harness` makes the hold's cause name an adapter the session no longer uses; the real adapter's ready edge never matches it in `heal_candidates` (`:4353`) and the session wedges on `adjudicationHold` until a human rules.

### Tier 3 — legibility / narrow availability

| # | Site | Shape | Consequence |
|---|---|---|---|
| F13 | `gateway.ex:3673` `%{state: "active"} <- Org.get` → `:3677` `CriticalLeases.declare` (`critical_leases.ex:23-63` never re-checks session state in its own txn) | lease written for a session retired in the window | orphan lease defers an ancestor's retire up to `critical_lease_hard_cap_ms` = 4 h (`gateway.ex:3765`) |
| F14 | `gateway.ex:4657` session count → `:4667` `close_adapter` | adapter torn down under a session created in the window | brand-new session's first turn gets `{:error, :degraded}` and an `adjudicationHold` |
| F15 | `gateway.ex:2332` `state: "active"` → `:2284` `Roles.bind` | role bound to a retired session | every wake through that role silently `:skipped` (`gateway.ex:882`) |
| F16 | `wire/socket.ex:456` `unless Org.get(db, key) do Org.create(...)` | check-then-create outside a txn; `sessionKey` is PRIMARY KEY and `Org.create` uses `transaction!` (raises) | two devices connecting simultaneously for a fresh user → one socket handler crashes. Same family as the roadmap's `spawn --name` UNIQUE leak (ERROR-BOUNDARY SEAM) |
| F17 | `work_state.ex:134` `status/2` (own round trip) gates `:145` INSERT in a *different* transaction | two emitters interleave | doorbell cursor *N+1* asserts a `fromState` that cursor *N* already passed; clients regress |
| F18 | `rail_remedy.ex:213` claim CAS → `:228` `Dispatch.dispatch` → `:231` live CAS | dispatch exceeding `@ttl_ms` (60 s) loses the live CAS silently; return value discarded | `producerKey` never set, `live?` stays false so `maybe_close` never closes it, row stuck `dispatched`; each 60 s cycle writes a lifecycle row claiming a fresh dispatch |
| F19 | `gateway.ex:1765`, `:2112`, `:3225` `Archetypes.get()` **unguarded**, vs `:1132`, `:1534`, `:3073`, `:3459` which use `|| Archetypes.builtin_default()` | `Archetypes.load!/1` (`gateway.ex:1951/:1968/:1975`, identity-edit/relearn) replaces the persistent_term; `acp_mcp_servers(nil)` raises on `archetype.mcp` (`archetypes.ex:143`) | TurnTask crash → `{:error, :task_crash}`, opaque, no adjudication closure |
| F20 | `session_lane.ex:161` `draining?` → `:172` `claim_next` | `application.ex:137` flips the flag, `:163` counts `status='running'`; the lane's claim queues behind that count at the DB owner | a turn started after the flag is eaten under a **clean_shutdown** stamp (`application.ex:150`) |
| F21 | `gateway.ex:1252-1257`, `:3350-3355`, `placement.ex:1173-1184` `GenServer.whereis` then call **by name** | death in the window is an uncaught `:noproc` exit, not the documented `:subscription` fallback | in `adapter_opts` this exit runs inside the adapter's boot fun → adapter dies, failure charged to the circuit |
| F22 | `credentials.ex:191-215` `read_metadata` (ssh `cat`) → `write_metadata!` (second ssh), with `gate`/`capture`/`park` between | an operator finishing `tightbeam onboard` on the satellite in the window | a freshly-banked credential is overwritten with the stale map + `"terminal" => true` — working credential marked revoked, all sessions on that host parked |
| F23 | `model_catalog.ex:230-232` two separate `Credentials` calls for status then kind | re-onboard between them | old status paired with new kind, contradicting the moduledoc's own claim that the pairing is load-bearing |
| F24 | **CLI** `dispatch.rs:833-835` re-`discover()`s per call; `dispatch.rs:931-933` resolves and validates an endpoint then **throws it away** | gateway restart rewrites `gateway.json` mid-ceremony (`dispatch.rs:786-789` documents this) | `finish` hits a gateway with no matching lease → `ceremonies.rs:104-118` `remove_dir_all`s the staging dir and cancels — destroys a captured, validated credential and burns a single-use auth code. (I checked the cross-org worst case: `onboarding_staging_path` carries `System.unique_integer` (`credentials.ex:686-700`), so a wrong gateway fails loud with `onboarding_not_started` rather than banking silently) |
| F25 | **CLI** `ceremonies.rs:67` reads `leaseTtlMs`, `:295` starts the clock after `harness_cli` (HTTP `GET /harnesses` + `uname` spawn) | two budgets the comment at `:174-176` says must be one | ceremony completes, `finish` posts after the server lease expired |
| F26 | **CLI** `probe.rs:660 → 684/706/738` stitches four snapshots by pid with **no identity re-check**; Linux does re-stat (`probe.rs:427-434`) with a dedicated test | pid reuse between passes | a stranger's exe/cwd/uptime attributed to a tightbeam lineage in `doctor` output. macOS `platform_limits` (`probe.rs:849-853`) does not name it |
| F27 | **CLI** `contain.rs:194-197` reads a failed spawn as `CONTAINED_REFUSED` on the strength of "`rules.ex` … so it cannot" (`:180-184`) | script rewritten/swept between validation and exec | operator debugs SBPL/landlock instead of the script's lifetime |

### Known / already tracked (not re-litigated)

`Dispatch.dispatch/3`'s third return unhandled at `wire/router.ex:823` (`control_response`), `wire/socket.ex:433` (crashes a **live WebSocket handler**), `supervision.ex:687`, and mislabelled at `rail_remedy.ex:228`. One new sibling: **`dispatch.rs:890`** — `parse_response` handles non-2xx, `error`, and `decisionPending`, then falls to `Ok(json.get("result"))`, so a 2xx body with none of those keys is **exit 0, no output**; there is no `_ =>` arm saying "the gateway sent something this CLI does not understand". Also `decisionPending` is only checked inside the 2xx branch, and `harnesses.rs:114-124` bypasses `parse_response` entirely and fails open into a guessed binary name.

### Suspicions (mechanism named, no interleaving established)

`gateway.ex:1396` `elected_attention` read outside the txn that writes `replyAttention` (missed election only) · `gateway.ex:4654-4655` one adapter pid used for N `close_session` round trips · `artifacts.ex:254` fixes the artifact set before `File.rename`s the workspace at `:492` — each UPDATE *is* CAS-guarded but the *set* is not, and `Txn.changes` is never consulted there (unique among the repo's CAS sites) · `subagent_markers.ex:102` assumes `ConditionFacts.file_in_txn/2`'s success shape when its `@spec` declares `map() | {:error, map()}` — currently unreachable because origin is `"process:tightbeam"` · `Ledger.mark_published` drops the `publishedAt IS NULL` predicate, but the feed is documented at-least-once · blocking ssh consumers inside the `Wakes` scheduler loop · `Archetypes.load!` doing a `:persistent_term.put` (global literal-area scan) as an admin-verb side effect.

---

## 4. The correct idiom already exists in-repo

Cite these when fixing, rather than inventing anything: `TurnObservations.handle_call({:observe,…})` (deadline compared **adjacent** to the mutation, with read and prune already behind it) · `RailEpisodes.evaluating/recovered` (position minted before the check; foreign incarnation refused) · `gateway.ex:4753-4759` `commit_host_rearm` (in-txn re-read + CAS + retry) · `gateway.ex:4144-4169` `adjudicate_respawn` (prepared set re-verified in-txn, `raise EffortRearmRace`, bounded retry) · `Org.swap_model_in_txn` (stale read passed as the CAS *expected value*, `:stale` handled) · `Escalation.consume` in `dispatch.ex:132-153` (CAS, loser path explicit) · `contain.rs:1022-1024` (fd pinned so there is no reopen window).

---

## 5. Guard assessment

The repo's idiom is two shell scripts run as ExUnit tests (`test/harness_seam_test.exs:72`, `test/provider_additivity_test.exs:7`), in two forms: **(a) ban a literal** with directory/file carve-outs plus one `perl -0777` character-proximity check, and **(b) freeze an inventory** — `check_provider_literals.sh` greps `-Rl`, sorts, and `cmp`s against `priv/provider_literal_sites.txt`, with `--print` to regenerate.

**A pure ban cannot work for this class.** The defect needs three things — a read of a fact owned elsewhere, an act conditioned on it, and a yield between them. Grep can see the first *only if it is named*, can see the second/third only by character proximity, and Elixir has no effect types to tell a yielding call from a pure one. Worse, the read and the act routinely live in different modules: `rules.ex:916` reads and `dispatch.ex:96` acts; `gateway.ex:3828` reads and `gateway.ex:4814` acts. No text-proximity heuristic crosses a module boundary. **No grep can decide SAFE vs RACY**, because there is no syntax for "this read is advisory". Say that plainly and stop there for the general form.

**Three narrower guards are feasible, and two need no naming convention at all.**

**Guard A — CAS scoping on re-enterable lifecycles.** *No convention needed; would have caught F6 today.* I extracted all 87 `UPDATE` statements in `lib/` and classified them. Every table whose status is **one-way** (`turns`, `wakes`, `sessions.state`, `artifacts`, `assignments`) is correctly guarded by `identity + state`. Every table whose status can be **re-entered** (`rail_remedy_episodes`, `adjudication_episodes`) carries an identity token (`occurrence`, `correlationKey`, `claimToken`) in the WHERE of every transition — **except exactly one**: `rail_remedy.ex:68`. So the rule "for a table listed as cycling, every mutating statement must name its occurrence token" has, measured today, **one true positive and zero false positives**. The guard is a `perl -0777` extraction of `UPDATE <table> SET … WHERE …` blocks plus a small table→required-predicate map — squarely inside the existing scripts' complexity. Add `park_escalation`'s missing `status='open'` (F1) by extending it to "a transaction that acts on a row read in an *earlier* transaction must re-assert the predicate it read".

**Guard B — frozen sampler-call-site counts.** *Convention needed; the only form that scales.* Rename every public reader of process-owned or CAS-owned state with a marker prefix — `Ledger.sampled_pending_count/2`, `AdapterCoordinator.sampled_generation/2`, `Adapter.sampled_knows_session?/2`, `Credentials.sampled_status/2`. The surface is small enough to be real: ~50 GenServer entry points across 13 processes, of which perhaps 25 are reads, plus ~20 DB-level samplers. Then grep `\bsampled_\w+\(` across `lib/` and `cli/src` and freeze **per-file counts** in `priv/sampler_sites.txt` (`lib/tightbeam/gateway.ex 14`). Counts, not file lists: the provider inventory is only 6 file paths at file granularity, which would put `gateway.ex` in permanently and make every new sampler call there invisible; counts are sensitive to additions and immune to line shifts. Adding a call anywhere fails the build until someone bumps the number — which forces the SAFE/RACY question into review at the one moment it is decidable, by the person who knows the answer. That is exactly what the provider guard buys and all it buys.

**Guard C — stale-handle proximity ban.** *Reuses the existing `perl -0777` idiom verbatim* (the `Homes.home_path(...).{0,240}File\.write!` check in `check_harness_seam.sh`). Within one function body, flag a `Process.whereis|GenServer.whereis|Registry.lookup|adapter_for|current_pointer` result followed within N characters by a second `GenServer.call` or an `Adapter.`/`Conn.` call. Today that fires on `harness_cancel`, `strict_apply_current_model`, `apply_model_change`, and the three `whereis`-then-call-by-name sites — four to six hits, small enough to allowlist, and each one is a real finding above.

**What none of them catch:** F1's cursor-vs-fact ordering, F2's call cycle (that wants a `:erlang.process_info(:current_stacktrace)` assertion or a static call-graph pass, not grep), F5's deliver-before-mark ordering, F8's "the gate is stale by the time the ladder fires", and the whole `cli/src` set — the Rust side would need its own inventory and shares no idiom with the shell scripts. A guard here buys **countability and forced review**, never a verdict.

---

## 6. Coverage

**Read exhaustively, by me:** `session_lane.ex`, `lane_manager.ex`, `adapter_coordinator.ex`, `ledger.ex`, `turn_observations.ex`, `rail_episodes.ex`, `dispatch.ex`, both guard scripts, `rules.ex:740-919`, `rail_remedy.ex:30-360`, plus every line I cite in Tier 1 and F6–F7, F10, F13, F16, F19–F20, and the quarantine/orphan wiring. I ran a full extraction of all 87 `UPDATE` statements in `lib/` and classified their WHERE clauses myself — that is the basis for Guard A.

**Read exhaustively by delegated sweeps, spot-verified by me at the load-bearing lines:** `gateway.ex` (4996 lines), `supervision.ex`, `wakes.ex`, `escalation.ex`, `effort_checkin.ex`, `adjudication.ex`, `acp/adapter.ex`, `acp/conn.ex`, `conn_registry.ex`, `credentials.ex`, `model_catalog.ex`, `db.ex`, `placement.ex`, `identity.ex`, `archetypes.ex`, `application.ex`, `cli/src/*`. I personally re-read and confirmed F1, F2, F3, F4, F6, F7, F10, F13, F16, F19, F20 and the quarantine finding. **F8, F11, F12, F14, F15, F17, F18, F21–F27 are agent-reported with quoted evidence that I did not independently re-open.** Treat those as high-confidence leads, not as verified as Tier 1.

**Sampled, not exhaustive:** the business-fact modules (`assignments.ex`, `work_items.ex`, `org.ex`, `projection.ex`, `event_log.ex`, `devices.ex`, `roles.ex`) were swept for the mutation/CAS signature at every write site and at their gating reads, but not read end to end — the sweep found them uniformly CAS-disciplined, which is why Guard A measures clean. `cli/src/args.rs` and `screen.rs` were grep-driven only (`screen.rs` is a pure `vte` replay over an in-memory buffer and touches no external fact).

**Could not reach:** anything requiring runtime observation — whether `classify_auth_event` actually returns `:terminal` on a live harness (F2's trigger), and the real frequency of the Tier-1 windows under load. F1, F3 and F6 have windows measured in DB round trips; F4, F5, F8 and F9 have windows measured in subprocess/ssh time. Test files were out of scope except where they document a contract — `cli/src/contain.rs:1446` and `probe.rs:1588` are cited for exactly that reason.
