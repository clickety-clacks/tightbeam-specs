# Topology probe — would moving process state into the DB have prevented the sample-then-act findings?

**Status:** Probe, read-only. Tree `/Users/mike/src/tightbeam_ex` @ `16b82d1c674822499b7b4119f1411ce8ea1e63a7`, 2026-07-30. **Nothing changed** — no file in `lib/`, `cli/`, `priv/` or `test/` was edited; the working tree carries only the two pre-existing `priv/kungfu/agentic-engineering/guidance/*.md` edits belonging to another lane. This document tests a hypothesis against the tree and reports a verdict with numbers; it proposes no implementation.

**Reproducing the measurements.** Every number in H3(b) was measured, not estimated. The two throwaway benchmark scripts (`db_bench.exs`, `db_bench2.exs`) are in the probe session's scratchpad and are re-runnable with the command in their headers, so a future reader can reproduce the numbers rather than trust them.

**Companion:** `sample-then-act-audit-2026-07-30.md` — the audit of 27 findings whose fact/owner inventory this probe tests.

**Provenance note, added at write time.** Every reading in this document was taken at `16b82d1`. While the report was being written, another lane fast-forwarded `fix/queued-not-running-apply` onto `main`, so main is now `ec1ab68d009016c52a1a24d01b26df3efd4a8957`. Two consequences for a later reader, neither of which changes an analysis or a number: the identity-apply fix discussed throughout H1 is now **on main**, not in flight on a branch; and line numbers in `gateway.ex`, `session_lane.ex`, `lane_manager.ex` and `ledger.ex` have shifted by that four-commit range. Every citation below resolves against `16b82d1`.

---

# VERDICT: the hypothesis is mostly WRONG. The prevention count is 9/27, and only **1** of those 9 needs the topology change.

**Tree:** `/Users/mike/src/tightbeam_ex` @ **`16b82d1c674822499b7b4119f1411ce8ea1e63a7`** (main, 2026-07-30 06:38:53 -0700). Working tree carries only the two pre-existing `priv/kungfu/.../guidance/*.md` edits from another lane. I changed nothing; the only files I wrote are two throwaway benchmarks in the scratchpad.

---

## H1 — DUPLICATED GATING FACTS: **the duplication is REAL and verified. The causal claim about the identity-apply fix is HALF TRUE, and the half that is false is the important half.**

### The specific claim, verified line by line

"A turn is running" does exist twice:

- **`SessionLane.task_ref`** — `session_lane.ex:33` (struct), set at `:182` in `claim_and_start/1`, cleared at `:135`/`:146`/`:150`.
- **`turns.status = 'running'`** — `ledger.ex:215`, written by `claim_next/3`'s guarded UPDATE; cleared at `:277` by `finish`.

They are written by the **same code path in sequence** (`claim_and_start` calls `Ledger.claim_next`, which commits `'running'`, and *then* assigns `task_ref`), which is what makes the duplication look benign and is why it survived. It is not benign. They can disagree in three verified ways:

1. `cancel_current` (`session_lane.ex:110-118`) writes the DB terminal, replies, and only *then* `Process.exit(task_pid, :kill)`. `task_ref` stays non-nil until the `:DOWN` arrives — an asynchronous window in which the DB says `canceled` and the lane says running. **F7 lives in exactly this window.**
2. `finalize/3` writes the terminal at `:219`/`:229` and the lane clears the ref at `:135`; `publish`, `terminal_publisher`, `on_terminal` and `mark_published` all run in between.
3. `Ledger.recover_running/1` (`ledger.ex:397`, called from `lane_manager.ex:53` at init) writes the `running` column with no lane in existence at all.

### Where the causal claim fails

The identity-apply fix is on `fix/queued-not-running-apply` (4 commits: `bd6fbe9`, `dfad51f`, `a1583db`, `ec1ab68`). It does end up touching both — but not because of the duplication. Sequence, from the commit messages and the diffs:

- `bd6fbe9` swapped the DB read `Ledger.pending_count` → new `Ledger.running?` (still a DB sample).
- `dfad51f` added `SessionLane.at_turn_boundary/2` — a `GenServer.call` into the lane, `:infinity`, that refuses on `task_ref` and runs the bounce closure **inside the lane's callback**. Its message states the reason explicitly: *"Checking status a second time cannot close the window: any gateway-side sample is stale the instant it is read."*
- The `Ledger.running?` call survives at branch-tip `gateway.ex:2055`. But it is **not load-bearing for correctness** — it is an org-wide early refusal that names *all* busy sessions instead of halting on the first. The lane check subsumes it.

So the fix needed the lane call because **the act is an external harness effect** (`Adapter.close_session` + `Adapter.load_session`, 65 s and 30 s+ budgets) that no transaction can contain — not because the fact had two homes. And note the direction of travel: `dfad51f`'s message rules that **`task_ref`, the process fact, is the T-SOURCE owner** — *"the lane is also where the fact physically lives (T-SOURCE) — task_ref is the lane's own record of a turn in flight, not a projection of it."* The repo's own most recent fix in this exact family moved the decision **out of the DB and into the process**. That is the opposite of the hypothesis.

### Inventory of every fact with more than one representation

| Fact | Copies | Authoritative | Writers | Can disagree? | Split-read decision? |
|---|---|---|---|---|---|
| **a turn is running** | `SessionLane.task_ref`; `turns.status='running'` | **Disputed in-tree.** SQL is authoritative for *admission* (`ledger.ex:171` returns `:busy`); `dfad51f` rules the lane authoritative for the *boundary* | lane (both, in sequence); `recover_running` (DB only, at boot) | **YES**, 3 verified windows above | **YES.** DB copy read by `identity apply`, `supervision.ex:209`, `application.ex:163` drain, `TurnObservations:137`. Process copy read by `cancel_current`, `at_turn_boundary`, `maybe_start`. F7, F9, F20 |
| **adapter generation** | coordinator `state.adapters[key].generation`; `turns.adapterGen` (`ledger.ex:523`); `adjudication_episodes.healToken` | coordinator | coordinator (live); lane (stamps) | yes, by design | **No** — declared one-way stamps, used correctly as *comparison inputs* (`adjudication.ex:541`). T-SOURCE-compliant |
| **harness session residency** | `Acp.Adapter.known`; `harness_pointers` chain | the **harness**; the adapter is its proxy | adapter (`:337,:356,:360,:377`); gateway (pointer rows) | yes, expected | Declared correctly in-code (`gateway.ex:2124-2127`). F11 is that only the `false` branch handles it |
| **session model / harness** | `sessions.model`/`harness`; what the harness actually loaded | T-SOURCE says the harness | gateway (DB); `apply_model_strict` (harness) | **YES, no tiebreak** | **YES — this is F3.** The DB copy is *not* declared a cache; `claim_next` stamps it onto every turn (`ledger.ex:215`) |
| **draining** | `:persistent_term` (`application.ex:137`) | the flag | `prep_stop` | single copy, but split reads | **YES.** Lane reads the flag (`:161`), drain loop counts `turns.status='running'` (`:163`). **F20** |
| **credential status / kind** | `.tightbeam/credential.json` on the machine (possibly over ssh); `Credentials.pending`; `ModelCatalog.entries` | the **machine's file** | `write_metadata!`; the operator's `tightbeam onboard` | **YES** — F22 is a lost update on the owner; F23 a torn read pair | yes |
| **archetypes** | identity git tree; `:persistent_term` (`archetypes.ex:107`) | the git tree | `Archetypes.load!` | yes | F19 — three sites don't guard nil |
| `turns.owner` | `"lane:#{inspect(pid)}"` | — | `claim_next` | — | **Read nowhere.** A write-only pid projection = a correct cache |
| `SessionLane.current_seq` / `current_message_id` | ↔ turns row | turns row | lane | only within its own callback | no |
| `SessionLane.quarantined` | ↔ nothing | — | **none** | — | **Confirmed: no writer anywhere in `lib/`.** The moduledoc contract at `:15-19` does not exist in code |

---

## H2 — THE PREVENTION COUNT

**Method note.** `DB.transaction/2` runs `fun` **inside the DB owner process** (`db.ex:129-141`), on the single connection. So "make the decision inside a single DB transaction" is available **only when the act is pure SQL**. I verified this convention holds tree-wide: I scanned every `DB.transaction`/`transaction!` body in `lib/` for calls into another GenServer and found **zero true positives** (the 8 hits were all post-commit or `*_in_txn(txn, …)` pure helpers). The codebase states the rule and its reason at `gateway.ex:1493-1495`: *"It runs post-commit rather than in the transaction because the coordinator writes to the DB, and the txn body executes inside the DB owner."*

### Counts (F1–F27)

| Class | Count | Findings |
|---|---:|---|
| **PREVENTED** — read could join the transaction the act already opens | **9** | F1, F5, F10, F12, F13, F15, F16, F17, F20 |
| **NOT PREVENTED — external effect** (harness JSON-RPC, ssh, subprocess, OS signal, filesystem, CLI) | **15** | F2, F3, F4, F7, F8*, F9, F11, F14, F18, F22, F23, F24, F25, F26, F27 |
| **NOT PREVENTED — the act is ALREADY atomic and it does not help** | **3** | F6, F19, F21 |
| UNCLEAR | **0** | — |

\* F8 is genuinely **split**: of its four gates, `:318` (wake gate → prod) and `:342` (adjudication hold) are adjacent to pure-SQL acts and would be **PREVENTED**; `:209` and `:353` are separated from their acts by `Rules.decide`, which spawns `RailScript.run` subprocesses, and `:353` gates `RailRemedy.fire`, which staffs work. Counted by its worst gate.

Suspicions (7): S1 (`gateway:1396` elected_attention) **PREVENTED**; S2, S3 (`artifacts.ex:254` → `File.rename`), S6 (blocking ssh in the Wakes loop) **NOT PREVENTED — external**; S5 (`mark_published` drops the predicate) is **already covered by idempotence** and is not a defect; S4 and S7 are not races at all. Totals with suspicions: **10 / 34 PREVENTED**.

### The number that actually decides it

Of the **9 PREVENTED**, **8 already have their fact in the DB.** Only **F20** (the `draining` flag in `:persistent_term`) requires *moving* a process-held fact.

> **The topology change — relocating process state into the DB — prevents exactly 1 of 27 findings.**
> The other 8 are prevented by putting the read inside a transaction the code **already opens**, with no state moving anywhere.

Broken out by where the gating fact lives today:

- Findings gating on a fact **already in the DB**: 15. Prevented: **8** (53%).
- Findings gating on a fact **not in the DB** (process state, OS pid, remote file, CLI clock): 12. Prevented: **1** (8%).

The lever with all the leverage is discipline — "re-assert in the transaction you already have" — which is precisely the audit's **Guard A**, already measured at one true positive and zero false positives.

### Second axis: WOULD IDEMPOTENCE HAVE MADE IT HARMLESS?

| | Count | Findings |
|---|---:|---|
| **YES** | **2** | F16 (upsert kills it outright), S5 (already relied on) |
| **PARTIAL** (act tolerates the race via a recovery/compensation path) | **3** | F10 (the `order_index` half — derive it), F11 (the `false` branch already has recovery; the `true` branch has none), F14 (the heal machinery compensates, badly, via `:degraded` + hold) |
| **NO** | **22** | everything else |

**On F5 specifically — the "idempotence would have covered it" guess is wrong, and the repo proves it.** F5 is not duplicate delivery; it is delivery of a **cancelled** intent. Duplicates are already handled: `turns.wakeId` is `UNIQUE` (`ledger.ex:41`) and `Wakes`' moduledoc says so verbatim — *"crash between deliver and mark → redelivered after restart, deduped by the turns table's `wakeId` UNIQUE (enqueue is exactly-once)."* Idempotence buys nothing here. F5's answer is **(a)**, and the repo already contains the proof it works: the **condition**-wake path `fire_candidate/fire_in_txn` (`wakes.ex:754-805`) re-reads the row and enqueues **inside one transaction**, and is correct. Only the legacy timed path (`deliver_due`, `:511-546`) has the hole.

### **NEITHER (a) nor (b): 16 of 27.** This is the expensive set.

F2, F3, F4, F6, F7, F8, F9, F18, F19, F21, F22, F23, F24, F25, F26, F27. What they actually need:

- **Fencing tokens** — 8: F3 (already has one! `apply_model_strict(adapter, sid, model, prior_model)` is a harness-side CAS — the defect is *ordering*, not the absence of a fence), F4, F6, F18, F22, F24, F26, and F7 (**blocked at the protocol**: ACP `session/cancel` carries only `sessionId`).
- **Decide inside the process that owns the fact** — 5: F7, F9, F11, F14, F23. This is the remedy the repo keeps re-deriving (`at_turn_boundary`, `TurnObservations`).
- **Plain discipline** (null guard, check the return value, catch the exit, one clock) — 5: F18, F19, F21, F25, F27.
- **Call-graph layering** — 1: F2.

**F6 is the cleanest single disproof in the set.** Its act `RailRemedy.close/3` (`rail_remedy.ex:64-74`) is *already* one atomic guarded UPDATE. Full atomicity, and it is still wrong, because it closes the wrong `occurrence`. Perfect transactions buy nothing; a fencing predicate buys everything.

### THE OUTBOX — the reading HOLDS, verbatim, and it was never named

`Wakes` is a textbook transactional outbox and the moduledoc says every part of it without using the word:

- Intent committed atomically with the state change: `Wakes.schedule_in_txn/2` (`wakes.ex:178`) writes the durable row **inside the caller's transaction** — **17 call sites** across escalation, gateway, work_items, effort_checkin, assignments, adjudication, supervision.
- Separate dispatcher: one `WakeScheduler` GenServer with a tick.
- At-least-once with an idempotent consumer: *"delivery goes through the SAME turn pipeline as a user post"*, *"at-least-once"*, *"deduped by the turns table's `wakeId` UNIQUE (enqueue is exactly-once)"*. `Adjudication.deterministic_wake_in_txn` adds a second idempotency key: *"so an at-least-once sweep enqueues EXACTLY ONE probe turn per token even if it runs twice."*

**Why the external effects bypass it, and whether they could route through it.** The outbox today carries exactly **one** effect type: *prompt this session*. F3/F7/F9/F11/F14 want an *adapter* effect. But the generalisation seam **already exists and is already used for an adapter-touching effect**: `Wakes` takes `internal_consumers` (`wakes.ex:442`), and `gateway.ex:366-370` registers three — `effort_probe`, `effort_deadline`, and `Adjudication.probe_retry_consumer() => adapter_heal_retry`. An "adapter effect" consumer is **additive to a live mechanism**, not an invention. Caveats, both real:

- Anything routed through it becomes at-least-once, so it must be idempotent or fenced. `close_session`/`load_session` plausibly are; `apply_model_strict` already carries its fence. **`session/cancel` cannot be** — no turn identity on the wire. F7 cannot use the outbox.
- `deliver_due` currently runs `attempt_internal_delivery` **inline in the scheduler loop**, where an `effort_probe` costs up to 8 s of ssh. Adding effect consumers there makes suspicion S6 worse unless they are dispatched off-process.

---

## H3(a) — WHICH PROCESS-HELD FACTS COULD MOVE

Only facts that **gate a decision** are listed.

**CAN move (and F20 is the one that should):**

| Fact | Gates | Verdict |
|---|---|---|
| `Application` `draining` (`:persistent_term`) | `session_lane.ex:161` → `claim_next` | **CAN, and it is the single genuine win.** Fold the predicate into `claim_next`'s existing transaction; the drain's count and the lane's claim then serialize at one owner. This is F20 and it is the whole payload of the topology change |
| coordinator `circuit` / `failures` / `last_failure` | `adapter_for` → `{:error, :degraded}` | CAN. But nothing in the audit is caused by their being in-process |
| `Credentials.pending` (onboarding leases) | lease expiry | CAN — a lease row with a TTL is a standard shape |
| `SessionLane.current_seq` / `current_message_id` | cancel reply payload | CAN (they're already in the turns row); pure duplication, harmless |
| `ModelCatalog.entries` | `validate_catalog_model` | CAN, but it is a declared TTL cache either way — no change in kind |
| `Archetypes` `:persistent_term` | F19 | CAN, and it **would not fix F19** — a DB read returns nil just as readily; the bug is the missing `\|\| builtin_default()` |

**STRUCTURALLY CANNOT move:**

| Fact | Gates | What blocks it |
|---|---|---|
| `SessionLane.task_ref` | `cancel_current`, `at_turn_boundary`, `maybe_start` | It is a **monitor reference** — meaningless outside the process. The *fact* it stands for already lives in the DB; what cannot move is the **lane's atomicity**. `at_turn_boundary` needs "no turn is running" and "do the adapter bounce" to be indivisible for 30–65 s. The only way to do that in the DB is to hold `BEGIN IMMEDIATE` for 65 s, which stalls every session (measured below) |
| `SessionLane.task_pid` | the kill | pid |
| `Acp.Adapter.known` | F11 | **T-SOURCE forbids it.** The *harness* owns residency; `known` is the adapter's record of what it asked. A DB row would be a third-order cache — strictly worse, and the code already says so at `gateway.ex:2124-2127` |
| `Acp.Conn.pending` | quiescence probe | JSON-RPC id ↔ live port correlation table |
| coordinator `pid` / `monitor` | `adapter_for` liveness | pid, monitor ref |
| coordinator load semaphore (`load_active`, `load_queue`) | `with_load_slot` | Crash-release is `Process.monitor` (`:504-520`). A DB lease needs TTL + reaping to get back what the monitor gives free |
| `Credentials` status / kind | F22, F23, `validate_credential` | **T-SOURCE forbids it.** Owner is `.tightbeam/credential.json` on the machine, often over ssh. The available fix is *one* call to the owner instead of two |
| `TurnObservations.windows` | evidence class | Explicitly ruled non-durable in the moduledoc: *"A window that outlives the turn that opened it has no value, so `turns.requestRef` … stays unused"* |
| `RailEpisodes.incarnation` (`make_ref()`) | foreign-incarnation refusal | a ref, and refusing foreign incarnations is the point |

Coordinator `epoch` is **already in the DB** (`coordinator_epochs`, `adapter_coordinator.ex:158-167`).

## H3(b) — MEASURED COST

**Method.** Two throwaway scripts under the scratchpad, run against this tree via `MIX_ENV=test mix run --no-start`, using the **real `Tightbeam.DB`** (one GenServer, one connection, production PRAGMAs: WAL / foreign_keys=ON / synchronous=NORMAL / busy_timeout=5000) on an **on-disk** file, seeded with the real `Ledger.ensure_schema` DDL and indices: 60 sessions × 300 turns = **18 000 rows, ~2.1 MB, 30 running**. 20 000 iterations per cell after a 200-iteration warm-up; latency at the caller in nanoseconds. Host: **eezo, Apple M4 Max, 16 cores, macOS 25.5.0, load average 19.4→20.7 during the run** (other lanes active — the contended tails are pessimistic).

**A. Uncontended (one caller, idle DB owner)**

| Operation | mean | p50 | p95 | p99 | max |
|---|---:|---:|---:|---:|---:|
| `GenServer.call` floor (no-op server) | 0.8 µs | 0.8 | 0.9 | 1.0 | 32 µs |
| `SELECT 1` (round trip + `prepare`) | 8.0 µs | 5.5 | 16.2 | 28.7 | 159 µs |
| **the `running?` gate read** | **29.4 µs** | **22.4** | 46.6 | 119.9 | 2.3 ms |
| `Ledger.pending_count/2` | 14.2 µs | 10.2 | 24.8 | 56.8 | 666 µs |
| `Ledger.running_turn_message_id/2` | 45.2 µs | 22.2 | 44.5 | 190.6 | 30.1 ms |
| **`DB.transaction` (BEGIN IMMEDIATE + 1 read + COMMIT)** | **31.0 µs** | **24.8** | 49.2 | 99.6 | 813 µs |
| `DB.transaction` (2 reads + 1 guarded UPDATE) | 90.7 µs | 37.7 | 91.5 | 487.0 | 65.9 ms |

Note: **wrapping the read in a transaction costs ~2 µs at p50.** Under WAL + `synchronous=NORMAL` a read-only `BEGIN IMMEDIATE`/`COMMIT` is nearly free. Atomicity is not the expensive thing.

**B. Contended — N concurrent callers on the single DB owner** (2 000 ops each)

| Config | READ mean | READ p50 | READ p95 | READ p99 |
|---|---:|---:|---:|---:|
| 4 readers | 235 µs | 142 | 206 | 571 |
| 16 readers | 770 µs | 507 | 627 | 2 265 |
| 16 readers + 2 writers | 641 µs | 494 | 604 | 705 |
| 16 readers + 8 writers | 823 µs | 626 | 879 | 4 649 |
| 16 readers + 16 writers | 1 070 µs | 774 | 978 | 3 155 |

Clean queueing law: **p50 ≈ N_concurrent × ~32 µs** (16 × 32 = 512 µs vs measured 507 µs). The DB owner is a hard FIFO; latency is linear in concurrency, exactly as the single-writer topology promises.

**C. Round trips per turn (measured by tracing the DB owner's mailbox)**

The lane's claim/deliver loop is **5 calls to the DB owner per turn**: `enqueue` 1, `claim_next` 1, `stamp_adapter` 1, `finish` 1, `mark_published` 1 (each transaction is one call carrying several statements).

**Extra reads the change implies:** on the hot per-turn path the process facts that gate decisions are `draining?` (`session_lane.ex:161`), `adapter_for` (`gateway.ex:1365`), `knows_session?` (`gateway.ex:1790`), `Archetypes.get` (`gateway.ex:1765`) — **+4 per turn, 5 → 9, +80% of the lane's DB-owner traffic.**

**What that totals:**

- Uncontended: 4 × 29 µs = **0.12 ms/turn**.
- At 16-way contention: 4 × 770 µs = **3.1 ms/turn**.
- Against a turn whose `Adapter.prompt` budget is **600 000 ms** and whose realistic duration is seconds: **0.05% of a 6-second turn.**
- Serializer duty cycle: one session at 5 calls per ~6 s turn ≈ 0.002% of the DB owner. Even 1 000 concurrent sessions at 9 calls/turn ≈ 3% duty. **The owner is nowhere near saturation.**

> **The read cost is not the objection. The reads are free.** Anyone rejecting this on latency is rejecting it for the wrong reason.

**D. The cost that IS fatal — holding one transaction open** (measured, `db_bench2.exs`)

| Transaction held for | An unrelated session's read waited |
|---:|---:|
| 1 ms | 100 µs |
| 10 ms | 5.7 ms |
| 100 ms | **95.2 ms** |

**1:1.** The transaction body runs inside the DB owner, so holding it blocks every other session for its full duration. The in-tree budgets of the acts in the NOT-PREVENTED set: `Adapter.prompt` 600 000 ms; adapter boot `handle_continue` 185 000 ms; `close_session` 65 000 ms; `apply_model_strict` 30 000 ms; `effort_probe` ssh 8 000 ms; `RailScript.run` seconds. Any of those inside a transaction is a **T-CONCURRENCY violation of the first order** — it makes every session wait on one session's harness call, which is the exact thing the product exists to escape.

**Second-order cost, unquantified but structural:** moving facts into the DB puts `DB.query` calls *inside more server callbacks*. There are 13 stateful processes; the F2 deadlock exists because a serializer makes a synchronous call from inside its own callback. This change adds such calls. **It enlarges the F2 surface rather than shrinking it.**

## H3(c) — THE CYCLE, THE GRAPH, THE LAYERING RULE

**Method.** I extracted the graph mechanically with a ~60-line static pass (transitive closure through each module's private functions from every `handle_*`/`init` entry point, plus state-held closure invocations), then hand-verified every edge in the cycle. Grep alone finds nothing useful: **the only syntactic `GenServer.call` inside a callback body in the whole tree is `adapter_coordinator.ex:312-313`** (`GenServer.stop`). Every real edge is indirect — through a plain function or a closure held in state.

**Processes (13 stateful + 1 leaf registry).** From `application.ex:73-91` and `gateway.ex:children_after_preflight`: `DB`, `LaneRegistry` (a `Registry`), `LaneManager`, `SessionLane` (per session), `WakeScheduler`, `Supervision`, `AdapterCoordinator`, `Acp.Adapter` (per key), `Acp.Conn` (per adapter), `Credentials` (per machine), `ModelCatalog`, `RailEpisodes`, `TurnObservations`, `ConnRegistry`. **`Tightbeam.Gateway` is NOT a GenServer** — confirmed, it is a call-through module; its code executes in whichever process invoked it, which is what makes the cycle hard to see.

**Synchronous edge list** (caller callback → callee process):

```
SessionLane        -> DB                    [Ledger.claim_next :172 / finish :111 / DB.transaction :218]
LaneManager        -> DB                    [Ledger.recover_running :53, unpublished_terminals :77]
LaneManager        -> SessionLane           [CAST only, :63/:85 — not a blocking edge]
WakeScheduler      -> DB                    [deliver_due :513, fire_candidate :751]
WakeScheduler      -> LaneManager           [Gateway.complete_delivery :759 -> ensure_lane, gateway.ex:1001]
WakeScheduler      -> ConnRegistry          [publish_message / publish_turn_state]
Supervision        -> DB                    [many]
Supervision        -> WakeScheduler         [Wakes.pending_count :318, self_pending_count :353]
Supervision        -> RailEpisodes          [summon :399, recovered :415]
Supervision        -> Credentials           [Dispatch.dispatch :687 -> spawn -> validate_credential]
Supervision        -> LaneManager/ConnRegistry [Gateway.deliver_prompt :836]
RailEpisodes       -> DB
TurnObservations   -> DB                    [Ledger.running_turn_message_id :137, inside handle_call]
ModelCatalog       -> DB                    [Placement.hosts :177]  (Credentials calls are in a detached Task.start :190 — NOT an edge)
AdapterCoordinator -> DB                    [EventLog.lifecycle :356; mint_epoch at init]
AdapterCoordinator -> Acp.Adapter           [:310  Adapter.conn — 5 s DEFAULT, no timeout arg]
AdapterCoordinator -> Acp.Conn              [:311  Conn.close, :312-313 GenServer.stop]
Acp.Adapter        -> Acp.Conn              [Conn.request, :infinity — :329,:347,:373,:425,:558,:611,:637,:662,:700]
Acp.Adapter        -> Credentials           [handle_info :461 -> :523 -> :530 state.on_auth_event]
Credentials        -> AdapterCoordinator    [handle_call :198 state.park -> gateway.ex:418 -> :3358 close_adapter]
Credentials        -> ConnRegistry, DB      [publish_sessions :349, capture_sessions :339]
DB                 -> (leaf; calls nobody)
Acp.Conn           -> (leaf; send/2 to the Adapter, never call)
ConnRegistry       -> (leaf)
```

**F2 cycle — verified hop by hop at this SHA:**

| # | Hop | Evidence |
|---|---|---|
| 1 | `Acp.Adapter.handle_info({:acp_notification,"session/update",…})` → `maybe_emit_account_update` | `acp/adapter.ex:461` |
| 2 | → `emit_auth_classification` → `state.on_auth_event.(classification, event)` | `:523`, `:530` |
| 3 | handler is `Placement.auth_event_handler/2`, wired at `placement.ex:988` | `placement.ex:1078-1086` |
| 4 | → `Credentials.mark_terminal/3` = `GenServer.call`, **5 s default** | `credentials.ex:128` |
| 5 | inside `handle_call({:mark_terminal,…})` → `state.park.(provider)` | `credentials.ex:191`, `:198` |
| 6 | `park` = `stop_provider_runtime(provider, machine)` | `gateway.ex:418` |
| 7 | → `AdapterCoordinator.close_adapter` = `GenServer.call` | `gateway.ex:3358-3367` |
| 8 | inside `handle_call({:close_adapter,…})` → `Tightbeam.Acp.Adapter.conn(pid)` = `GenServer.call(A, :conn)` **with no timeout argument** | `adapter_coordinator.ex:310`; `acp/adapter.ex:211` |
| 9 | **A is blocked in its own `handle_info` at step 1. Deadlock, 5 s.** | — |

Secondary confirmed: the `catch :exit` at `:314-316` aborts the whole `try`, so `Conn.close`, and both `GenServer.stop` at `:311-313` never run — and the monitor was already `demonitor(…, [:flush])`'d at `:307`, so when A dies of its own timeout there is **no `adapter_down` row and no failure count**.

**Any other cycle: NO.** The only other candidates dissolve on inspection, all three by design and all three commented as such:

- `LaneManager → SessionLane` is a **cast** (`session_lane.ex:63`).
- `SessionLane → Supervision` is a **cast** (`Supervision.notify_terminal`, `supervision.ex:56`; wired `gateway.ex:240`).
- `AdapterCoordinator → Gateway` heal sweep is a **`Task.Supervisor.start_child`** (`gateway.ex:285-294`), with the comment *"the coordinator must never block on either (adapter checkouts queue behind it)."*

`Supervision → Credentials → AdapterCoordinator → Acp.Adapter → Credentials` re-enters the same cycle from a second door; Supervision is not itself in it.

**THE LAYERING RULE THAT FORBIDS IT.** Tier the graph by what a process may block on:

```
T0  DB                                     (leaf)
T1  Acp.Conn, ConnRegistry                 (leaf)
T2  Acp.Adapter, Credentials, ModelCatalog, RailEpisodes, TurnObservations
T3  AdapterCoordinator
T4  SessionLane, LaneManager, WakeScheduler, Supervision
```

> **A process may make a synchronous call only to a strictly lower tier. Every upward notification is a `cast` or a `Task`.**

The cycle is exactly one upward call: `Acp.Adapter` (T2) synchronously calls `Credentials` (T2, peer) which calls `AdapterCoordinator` (T3, **above**). **The rule already exists in this codebase and is already applied twice out of three.** There are exactly three upward hooks, all state-held closures: `on_adapter_ready` (a `Task`), `on_terminal` (a `cast`), and **`on_auth_event` (a `call`)**. F2 is the only one of the three that is synchronous.

**Could a mechanical check enforce it, in the idiom of the two shell guards?**

- **In the existing grep idiom — yes, for the thing that matters.** The upward hooks are all state-held closures invoked inside callbacks. A **frozen inventory** guard in the exact form of `check_provider_literals.sh` (grep → sort → `cmp` against `priv/…`, with `--print` to regenerate) can enumerate every `state.<field>.(` invocation reachable from a `handle_*` body and freeze the list with its required shape (`cast` / `Task` / `call`) next to it. Today that inventory is small and real: 17 in `credentials.ex`, plus `adapter_coordinator.ex:400`, `session_lane.ex:113/239/248`, `lane_manager.ex:78/80`. Adding a fourth upward hook, or converting an existing one to a `call`, fails the build until someone bumps the file — **which forces the layering question into review at the one moment it is decidable.** That alone would have caught F2.
- **For true acyclicity — feasible, but not in shell.** Grep cannot do it: the only syntactic `GenServer.call` in a callback in the tree is the `GenServer.stop` pair, so a text guard sees nothing. It needs a transitive static pass over each module's callback closure. I wrote one in ~60 lines of Python during this probe and it found **exactly one cycle, the known one, and no others.** That is more machinery than the two existing scripts, but it is demonstrably within reach and it produces a **verdict**, not just countability — which is more than the audit concluded was possible for the general sample-then-act class.

## H3(d) — SHARDING: **AdapterCoordinator's globality is INCIDENTAL, with exactly one exception, and that exception is a live T-CONCURRENCY violation.**

Everything in `state.adapters[key]` — `pid`, `monitor`, `generation`, `ready`, `circuit`, `failures`, `timer`, `last_failure`, backoff — is **per key** and shares nothing across keys. `adapter_sup`, `adapter_opts`, `db`, `backoff_base_ms`, `failure_circuit`, `on_adapter_ready` are immutable config, trivially replicable.

**What is actually shared across all keys:**

1. **The re-adoption load semaphore** — `load_active`, `load_queue`, `load_soft_cap` (default **3**, `adapter_coordinator.ex:225`, `:281-288`, `:504-536`). **This is the only true global, and it is load-bearing in the wrong direction.** Its stated purpose is *"no thundering herd after an adapter bounce"* — and **a bounce is per key**: one adapter dies, *its* sessions re-`session/load`. A global cap of 3 means **claude's bounce and codex's bounce share a budget of three slots**, so one harness's re-adoption waits on another harness's. That is T-CONCURRENCY's second clause, verbatim: *"no harness's work ever waits on another harness's."* Per-key or per-machine preserves the anti-herd purpose exactly and removes the coupling. Its only real callers are `gateway.ex:1799` and `:3219`, both per-session `load_session` paths.
2. **The circuit is NOT shared** — `entry.circuit`, per key. A degraded claude does not degrade codex.
3. **The epoch IS shared** (`state.epoch`, one per coordinator init) but **is not a barrier to sharding.** It is minted from the DB's `coordinator_epochs` AUTOINCREMENT (`:158-167`), so N shards each mint a globally-ordered epoch from the same table for free. And tokens are only ever compared **within a key**: `Adjudication.heal_candidates` (`adjudication.ex:513-537`) filters `WHERE e.cause = ?1` — the adapter key name — before calling `newer_token?`. **Sharding preserves the ordering invariant the epoch exists for.**
4. **Nothing else.** Health (`:290-302`) is a projection, trivially merged across shards.

**Verdict:** per-machine or per-harness sharding is available and would break nothing the coordinator exists to do. What globality currently buys is **one global serializer that every lane calls on every turn** (`adapter_for`, `gateway.ex:1365`) — which is precisely the wedge surface F2 exploits: a 5 s credential-event deadlock in one harness stalls every session on every harness. Sharding does not fix F2 (the cycle is still a cycle), but it bounds its blast radius to one machine.

---

## What I verified line by line vs. inferred

**Verified line by line at this SHA:** all of H1 (both copies, all three divergence windows, the no-writer `quarantined`, the write-only `turns.owner`); the full F2 cycle, all 9 hops; F1, F3, F5, F6, F7, F8, F10, F11, F12, F13, F14, F15, F16, F17, F18, F19, F20, F21, F23; the identity-apply fix across all four branch commits including the retained `Ledger.running?`; the outbox reading (`schedule_in_txn` call sites, the `wakeId UNIQUE` dedupe, the three `internal_consumers`); AdapterCoordinator in full; the whole call graph (extracted mechanically, then hand-checked for every edge in the cycle and every hook shape); the "no process call inside any transaction body" convention (scanned tree-wide, zero true positives).

**Not re-opened, taken from the audit:** F4, F22, F24–F27 (Rust CLI — I classified these from the audit's quoted evidence without re-reading `cli/src`), and the seven suspicions' line citations.

**Measured, not inferred:** every number in H3(b). Both benchmark scripts are in the scratchpad (`db_bench.exs`, `db_bench2.exs`) and are re-runnable with the command in their headers.

**Inferred, flagged as such:** that the topology change enlarges the F2 deadlock surface (structural argument from the graph, not measured); the per-turn extra-read count of 4 (static, from the hot-path call sites, not traced through a live turn).

---

## The one-paragraph answer

The duplication is real and I found nine more instances of it, but it is not what causes these defects. **Twenty-two of twenty-seven findings already gate on a fact that lives in the DB.** Putting the read inside a transaction the code already opens would prevent nine of them; *moving* a process-held fact into the DB prevents **one** (F20, the drain flag). Meanwhile the counterfactual is unavailable where it is most needed: `DB.transaction` runs its body inside the single DB owner, so a decision whose act is a harness call, an ssh round trip or a subprocess cannot be made inside one — and holding a transaction for T ms delays every other session by T ms, measured 1:1, against acts budgeted at 8 s to 600 s. Reads themselves are free (22 µs p50, 0.05% of a turn), so cost is not the argument; **T-CONCURRENCY is**. The repo's own most recent fix in this exact family, on `fix/queued-not-running-apply`, moved a decision **out of the DB and into the lane**, citing T-SOURCE — the opposite of the change under test. **Discipline is the answer for the nine; fencing tokens are the answer for eight more; deciding inside the owning serializer is the answer for five; and one call-graph layering rule — already applied two times out of three in this codebase — is the answer for F2.**
