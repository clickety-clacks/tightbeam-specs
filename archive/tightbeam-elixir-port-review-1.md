I’m treating this as an adversarial architecture/spec review. I’ll use the architecture-principles skill to structure the mapping critique, then verify every material claim against the port spec, parent invariants, and the current TypeScript implementation. I’ll also follow the required notification procedure when the review is ready.

I’m treating this as an adversarial architecture/spec review. I’ll use the architecture-principles skill to structure the mapping critique, then verify every material claim against the port spec, parent invariants, and the current TypeScript implementation. I’ll also follow the required notification procedure when the review is ready.

The architecture skill explicitly requires a cross-model adversarial pass for spec work. I’m loading that review procedure now; if it mandates a separate reviewer invocation, I’ll use it as a second opinion while keeping the final adjudication grounded in the repository evidence I inspect myself.

The architecture skill explicitly requires a cross-model adversarial pass for spec work. I’m loading that review procedure now; if it mandates a separate reviewer invocation, I’ll use it as a second opinion while keeping the final adjudication grounded in the repository evidence I inspect myself.

The required Fable reviewer is running as an independent second pass. Meanwhile I’m tracing the actual state transitions and persistence boundaries in the TypeScript source—especially where the prose docs simplify behavior—so the final findings won’t merely restate either specification.

The required Fable reviewer is running as an independent second pass. Meanwhile I’m tracing the actual state transitions and persistence boundaries in the TypeScript source—especially where the prose docs simplify behavior—so the final findings won’t merely restate either specification.

The first Fable invocation was rejected by the CLI because its variadic directory option consumed the prompt; no review ran. I’ve corrected the invocation and am retrying it now.

The first Fable invocation was rejected by the CLI because its variadic directory option consumed the prompt; no review ran. I’ve corrected the invocation and am retrying it now.

The core incompatibilities are now clear: “mailbox = FIFO” does not preserve the TypeScript gateway’s total ordering under multiple producers; the proposed lane restart cannot retain or even identify volatile queued/current turns; and “same schema” leaves nowhere to persist the crash/failure bookkeeping the reliability doctrine promises. I’m checking the remaining library/runtime specifics and the independent reviewer’s findings before issuing the verdict.

The core incompatibilities are now clear: “mailbox = FIFO” does not preserve the TypeScript gateway’s total ordering under multiple producers; the proposed lane restart cannot retain or even identify volatile queued/current turns; and “same schema” leaves nowhere to persist the crash/failure bookkeeping the reliability doctrine promises. I’m checking the remaining library/runtime specifics and the independent reviewer’s findings before issuing the verdict.

Fable could not connect (`ENOTFOUND`), so the mandated fallback is a fresh Codex GPT‑5.6 SOL reviewer at high reasoning. I’m launching that fallback now; if network policy blocks it too, I’ll report the failed cross-model check explicitly rather than treating it as evidence.

Fable could not connect (`ENOTFOUND`), so the mandated fallback is a fresh Codex GPT‑5.6 SOL reviewer at high reasoning. I’m launching that fallback now; if network policy blocks it too, I’ll report the failed cross-model check explicitly rather than treating it as evidence.

The independent review could not be obtained: Fable was network-blocked, and the required Codex fallback could not initialize under the read-only sandbox. I have treated both as failed checks, not as corroboration. The direct review is ready, including an additional hard blocker: the “unmodified TS E2E scripts” cannot target BEAM because each script imports and starts `src/gateway.ts` itself. I’m sending the required completion notification now.

The independent review could not be obtained: Fable was network-blocked, and the required Codex fallback could not initialize under the read-only sandbox. I have treated both as failed checks, not as corroboration. The direct review is ready, including an additional hard blocker: the “unmodified TS E2E scripts” cannot target BEAM because each script imports and starts `src/gateway.ts` itself. I’m sending the required completion notification now.

The generic notification command is deprecated on eezo and did not confirm delivery, so I’m retrying through the host-specific notifier it named.

The generic notification command is deprecated on eezo and did not confirm delivery, so I’m retrying through the host-specific notifier it named.

# Adversarial review

The port direction is sound, but the specification is not implementable as written. Its central reliability promises conflict with its “same schema” constraint, and several acceptance tests cannot actually exercise the BEAM gateway.

## 1. Mapping errors

### “Mailbox = FIFO” is insufficient

The TypeScript path performs message persistence, echo broadcast, and `fifo.enqueue()` synchronously in one event-loop turn ([gateway.ts](/Users/mike/src/tightbeam/src/gateway.ts:278)). The proposed OTP system has multiple WebSocket, HTTP, and scheduler processes sending to one lane.

BEAM only guarantees send order from the same sender; it does not establish an application-level order among different senders ([Erlang signal ordering](https://www.erlang.org/doc/system/ref_man_processes.html)). This permits:

1. Connection A inserts message sequence 10.
2. Connection B inserts sequence 11.
3. B’s lane message arrives first.
4. The harness executes 11 before 10.

The lane must own the authoritative enqueue sequence—or consume a durable sequence assigned transactionally by the store. Merely saying “mailbox = FIFO” in [Architecture mapping](/Users/mike/src/shared-workspace/shared/specs/tightbeam-elixir-port.md:54) does not preserve the current ordering.

The acceptance criteria also need concurrent producers, not the current single-caller FIFO test ([fifo.test.ts](/Users/mike/src/tightbeam/src/core/fifo.test.ts:9)).

### A restarted lane cannot recover its state

The proposed lane keeps its queue and current turn in GenServer memory, then says “crash → restart clean + turn marked failed” ([port spec](/Users/mike/src/shared-workspace/shared/specs/tightbeam-elixir-port.md:54)). The existing queue is explicitly volatile ([fifo.ts](/Users/mike/src/tightbeam/src/core/fifo.ts:43)), and the required identical SQLite schema has no turn/queue table.

After a lane crash, the replacement process cannot know:

- Which turn was current.
- Which turns were queued.
- Which terminal state has already been broadcast.
- Whether the adapter accepted or even completed the prompt.

`terminate/2` is not a solution: it is not guaranteed for `:kill`, VM death, or all supervisor shutdown paths. A separate durable turn record or surviving coordinator is required. That conflicts with “same schema, no migration” ([port spec](/Users/mike/src/shared-workspace/shared/specs/tightbeam-elixir-port.md:36)).

### Lane death can leave an ACP turn running

If the lane dies after issuing `session/prompt`, the adapter may continue executing tools and modifying the world. Restarting the lane “clean” and running the next prompt can violate the one-turn-per-session invariant.

The spec must define:

- A supervised per-turn task monitored by the lane.
- What kills/cancels that task when its lane dies.
- How the ACP connection sends `session/cancel` when the original requester disappears.
- Whether an unknown-outcome turn is failed without retry. It must not be automatically retried after potentially executing tools.
- How queued turns resume only after adapter re-adoption completes.

Long-running work must not be awaited inside the lane’s GenServer callback, or cancel/status messages cannot be handled; Elixir explicitly recommends handling task completion asynchronously rather than awaiting long work inside an OTP behaviour ([Task documentation](https://hexdocs.pm/elixir/Task.html)).

### Adapter restart semantics are underspecified

The current gateway caches both adapters and live harness-session objects ([gateway.ts](/Users/mike/src/tightbeam/src/gateway.ts:194)), but never observes `adapter.exited`; today they become stale after a child exit. The port is right to improve this, but “restart + session/load re-adoption” is not a design.

It must specify:

- Who owns the adapter generation and invalidates all stale session handles.
- Whether re-adoption is lazy, as the parent design requires ([tightbeam.md](/Users/mike/src/shared-workspace/shared/specs/tightbeam.md:149)), or eagerly loads every active lane.
- What happens when `session/load` fails or the transcript is missing.
- How simultaneous lane loads are bounded after an adapter restart.
- Whether a normal-but-unexpected Port exit restarts. A `:transient` child does not restart after `normal` or `shutdown` ([OTP child restart semantics](https://www.erlang.org/doc/system/sup_princ.html)).
- How planned idle reaping is distinguished from an unexpected exit.
- How an in-flight turn gets exactly one failed terminal state while pending turns remain ordered.

Eagerly reloading all “live lanes” risks a thundering herd; the parent spec explicitly says load on demand.

### Adapter death can create a lane restart storm

If lanes use synchronous `GenServer.call` against the adapter/connection, one adapter death can make every calling lane exit. Enough simultaneous lane failures can exceed `LaneSupervisor` restart intensity, kill the supervisor, and discard every dynamic child.

OTP supervisors deliberately terminate themselves after exceeding restart intensity; supervision does not imply the application “as a whole does not go down” ([OTP restart intensity](https://www.erlang.org/doc/system/sup_princ.html)). The spec names no restart intensities, backoff, circuit breaker, degraded state, or escalation policy.

### ACP Port framing is not fully mapped

The spec says NDJSON framing is handled with `{:line, ...}` ([port spec](/Users/mike/src/shared-workspace/shared/specs/tightbeam-elixir-port.md:63)). Erlang’s line mode splits lines longer than the configured maximum into one or more `:noeol` fragments, which must be reassembled before JSON decoding ([`open_port` line framing](https://www.erlang.org/doc/apps/erts/erlang.html#open_port/2)).

Acceptance must cover:

- A JSON-RPC line larger than the Port line limit.
- Multiple lines in one OS read.
- Split UTF-8 sequences.
- EOF with an unterminated line.
- Malformed JSON.
- Stderr capture without merging it into NDJSON stdout.
- Port exit before or after `exit_status`.
- Adapter processes surviving an abrupt BEAM VM death; closing a Port does not universally guarantee the OS process exits.

### Adapter rules are contradictory

The port says to carry `PATTERNS.md` rules unchanged ([port spec](/Users/mike/src/shared-workspace/shared/specs/tightbeam-elixir-port.md:39)), but that document still says Claude uses `session/set_model` ([PATTERNS.md](/Users/mike/src/tightbeam/docs/PATTERNS.md:34)). The actual current implementation uses `session/set_config_option` for both adapters because Claude ACP 0.59 dropped `set_model` ([harness.ts](/Users/mike/src/tightbeam/src/acp/harness.ts:118)); the parent spec records the same update ([tightbeam.md](/Users/mike/src/shared-workspace/shared/specs/tightbeam.md:788)).

Following the binding port text would reproduce a known failure. The source-of-truth adapter rules must be reconciled before implementation.

### Per-connection rate limits change behavior

The port claims keepalives and rate limits become per-connection state ([port spec](/Users/mike/src/shared-workspace/shared/specs/tightbeam-elixir-port.md:73)). Current pairing and typing limits are global maps keyed by device ID ([server.ts](/Users/mike/src/tightbeam/src/wire/server.ts:82)); the pairing test deliberately reconnects repeatedly with the same device ID ([server.test.ts](/Users/mike/src/tightbeam/src/wire/server.test.ts:286)).

Moving pairing limits into a connection process resets the limit on every reconnect and breaks existing behavior. A shared device-keyed rate-limit owner is required.

### WebSocket fan-out and takeover ownership are missing

“One process per connection” is accurate for Bandit ([Bandit process model](https://bandit.hexdocs.pm/WebSocket_README.md.html)), but it does not replace the current centralized connection set used for:

- Owner-scoped broadcast.
- Device takeover and `session_replaced`.
- Closing the previous socket atomically.
- Global device rate limits.

Those behaviors currently live in the shared server state ([server.ts](/Users/mike/src/tightbeam/src/wire/server.ts:182), [broadcast path](/Users/mike/src/tightbeam/src/wire/server.ts:333)). The supervision tree needs an explicit connection registry/broadcast owner.

### Replay can race live delivery

The TypeScript auth path synchronously builds the snapshot, sends `auth_result`, stream snapshot, replay messages, and finally `sync_complete` ([server.ts](/Users/mike/src/tightbeam/src/wire/server.ts:205)). In BEAM, concurrent connection and broadcaster processes can send a live message in the middle of replay.

The spec needs a replay watermark and per-connection live-event buffer so that reconnects see neither gaps nor duplicates. This is absent from both mapping and acceptance criteria.

### Wake “at least once” currently ends at volatile enqueue

The current scheduler marks a wake fired after `deliver()` returns ([wakes.ts](/Users/mike/src/tightbeam/src/core/wakes.ts:114)). In production, `deliver()` means “persist an echo and enqueue in memory,” not “the harness accepted or completed the turn” ([gateway.ts](/Users/mike/src/tightbeam/src/gateway.ts:311)).

Therefore:

- Crash after enqueue and mark-fired can lose the queued turn permanently.
- Crash after delivery but before mark-fired can enqueue a duplicate.
- There is no dedupe key linking a wake to its generated message.
- A target retired after scheduling is silently dropped but still marked fired.

The parent spec also says `1:1 wake→turn` ([tightbeam.md](/Users/mike/src/shared-workspace/shared/specs/tightbeam.md:855)), which conflicts with accepting duplicate delivery. The delivery commit point and dedupe mechanism must be specified.

## 2. Missing or invalid acceptance criteria

The largest acceptance-wall problem is literal: the “existing TS scripts, unmodified” cannot run against BEAM. Each imports and starts the TypeScript gateway itself:

- [wire-first-light.ts](/Users/mike/src/tightbeam/scripts/wire-first-light.ts:11)
- [dm-first-light.ts](/Users/mike/src/tightbeam/scripts/dm-first-light.ts:14)
- [agent-uses-cli.ts](/Users/mike/src/tightbeam/scripts/agent-uses-cli.ts:11)

`wire-first-light` also exits zero even when its final `pass` expression is false ([wire-first-light.ts](/Users/mike/src/tightbeam/scripts/wire-first-light.ts:111)). Acceptance wall item 2 is therefore impossible and, in one path, not a trustworthy gate.

Required acceptance additions:

- Refactor or add black-box scripts that accept an external URL/baseDir and never import `startGateway`.
- Differential wire traces: run the same deterministic request trace against TS and BEAM, normalize UUID/timestamps, compare frame shapes and ordering.
- Concurrent posts from multiple sockets plus a wake to one session; assert store sequence equals execution order and no overlap occurs.
- Concurrent same-`c_id` retries: one echo/turn, repeated ack for identical content, conflict without ack for different content. The dedupe scope must remain `(sessionKey, deviceId, clientMessageId)` ([store.ts](/Users/mike/src/tightbeam/src/core/store.ts:85)).
- Reconnect while writes occur; prove replay/live handoff has no gaps or duplicates and `sync_complete` terminates replay.
- Kill lane during current turn and with queued turns.
- Kill adapter during initialize, load, prompt, cancel, after tool effects, and after final chunks but before the JSON-RPC result.
- Kill WakeScheduler before delivery, after enqueue, and before `mark fired`.
- Kill/restart the DB owner while HTTP, replay, and wakes are active.
- Multi-session adapter traffic with interleaved ACP notifications; prove chunks route by `sessionId`.
- Large NDJSON-line and partial-framing tests.
- Normal versus abnormal adapter exit and repeated auth/startup failure, proving no restart storm.
- Exact frame-order assertions for echo, accepted/running, ack, assistant reply, activity-off, and terminal state.
- Soak thresholds: memory growth, mailbox sizes, DB busy errors, scheduler delay, missed/duplicate wakes, restart counts, and response latency. “Zero unexplained restarts” is subjective and does not test recovery.

The spec also claims fixtures are copied verbatim, but the repository has no `test/fixtures/` tree; most tests construct data and fake adapters inline. Porting 76 test names is useful, but not an independent behavioral oracle.

## 3. SQLite adopt-in-place risks

Raw Exqlite is the safer choice, but the current database contract needs to be written down first.

Specific problems:

- TypeScript sets `WAL`, `foreign_keys=ON`, and `synchronous=NORMAL` ([db.ts](/Users/mike/src/tightbeam/src/core/db.ts:7)); it does not set `busy_timeout`. The port silently adds one ([port spec](/Users/mike/src/shared-workspace/shared/specs/tightbeam-elixir-port.md:107)), changing lock-contention timing and error behavior.
- Exqlite currently defaults `busy_timeout` to 2000 ms and defaults journal mode to `DELETE` unless configured. WAL enables concurrent reads, not concurrent writes ([Exqlite connection options](https://exqlite.hexdocs.pm/Exqlite.Connection.html)).
- Foreign-key enforcement and busy handling are connection-specific. Every pooled connection must receive the intended settings; SQLite requires foreign keys to be enabled separately per connection ([SQLite foreign keys](https://www.sqlite.org/foreignkeys.html)).
- “Route writes through contexts” does not enforce single-writer behavior. Context modules callable from many Plug/GenServer processes are still multiple concurrent writers.
- The current check-then-insert operations for message dedupe, spawn idempotency, first-user bootstrap, and handle uniqueness rely partly on the single Node execution context. In BEAM they need transactions plus constraint-error adjudication.
- Ecto migrations would normally introduce migration metadata and encourage schema conventions that do not match camelCase columns and epoch-millisecond integers.
- JSON text produced by Jason may differ from `JSON.stringify` in key ordering or escaping. That matters if “byte-identical” includes stored event payload text or serialized wire bytes.
- A `.schema` textual diff is insufficient. It does not prove row encoding, PRAGMAs, library compile options, transaction behavior, or that TS can reopen data written by BEAM.
- WAL cutover must consider `state.db-wal` and `state.db-shm`. Clean last-close normally checkpoints and removes them, while crash recovery may leave them present ([SQLite WAL lifecycle](https://www.sqlite.org/walformat.html)).

Adoption acceptance should include:

1. TS creates and populates every table, including pending wakes and high AUTOINCREMENT values.
2. BEAM opens the exact directory, runs `integrity_check`/`foreign_key_check`, and changes no schema object.
3. BEAM reads and mutates all row types.
4. BEAM stops; TS reopens the same DB and reads those mutations.
5. Repeat after an intentionally unclean TS termination with WAL sidecars present.
6. Compare `table_xinfo`, `index_xinfo`, foreign keys, triggers, `user_version`, `application_id`, and compile/runtime SQLite versions.
7. Assert no Ecto migration table or other framework metadata appears.
8. Pin and verify every connection’s `journal_mode`, `foreign_keys`, `synchronous`, and explicit busy timeout.

## 4. Supervision-tree flaws

The flat `one_for_one` tree does not encode actual dependencies:

- EventLog, WakeScheduler, Bandit handlers, lanes, and adapters all depend on the database.
- Lanes depend on adapter availability but must not die merely because an adapter dies.
- An adapter owns a Port/connection and per-session ACP routing state, but the proposed relation between `Acp.Adapter` and `Acp.Conn` is not shown.
- A separate EventLog GenServer appears to exist only for code organization; the current event log is a direct database context. If it is a process, its serialization purpose and failure semantics must be stated.
- If a mutation succeeds and EventLog dies before the append, the caller may see failure after the side effect already occurred. Retrying can duplicate non-idempotent work.

The tree needs at least explicit subtrees and ownership:

- Core DB ownership and readiness.
- Connection registry/broadcaster.
- Adapter subtree in which adapter lifecycle and Port lifecycle are one coherent work unit.
- Lane supervisor plus turn-task supervisor.
- An adapter directory/coordinator publishing adapter generations and degraded state.
- Restart intensities, backoff, and failure escalation for each subtree.
- Readiness behavior while DB recovery or scheduler catch-up is occurring.

The assertion that every crash creates an event-log row is also impossible for a crash caused by database failure, and the existing `events.kind` constraint only allows `verb|denied` ([events.ts](/Users/mike/src/tightbeam/src/core/events.ts:34)). Adding lifecycle events changes the supposedly identical schema/contract.

## 5. Positions on the four open questions

1. **Bandit vs Cowboy: Bandit.** Bandit already provides the desired one-process-per-WebSocket model and Plug/WebSock integration. The choice does not solve connection registration, takeover, replay barriers, or slow-client mailbox growth; those remain application responsibilities.

2. **Ecto vs raw Exqlite: raw Exqlite.** Adopt-in-place, exact camelCase schema, explicit SQL, and no migrations favor raw SQL. Put writes behind an actual serialized ownership/transaction seam; use separately configured read connections only if needed. Rename `Tightbeam.Repo` to something such as `Tightbeam.DB`, because “Repo” falsely implies Ecto.

3. **Mix release vs Burrito: Mix release.** TARS is a controlled target, and this product still requires Node for the retained CLI and ACP adapter packages. Burrito does not make the overall artifact self-contained and adds packaging/cross-build risk without solving those Node assets. Include ERTS in the release and pin OTP/Elixir/SQLite/adapter versions.

4. **Telemetry surface:** `/version` should preserve compatibility fields and expose static release/build identity. Do not rename scheduler/run-queue data to the existing Node `loopLagP99Ms`; either retain a real timer-jitter equivalent or version the field. `/health` should contain dynamic core readiness: DB read/write probe, wake scan age, supervisor/restart counters, scheduler/run-queue summaries, and degraded adapter counts. Lazy adapter failure should degrade the affected sessions, not make the whole gateway globally unready.

## 6. Wishful versus verifiable

Wishful claims include:

- “The app as a whole does not go down.”
- “No process can wedge the system.”
- “Nothing dies silently.”
- “A slow client can only hurt itself.”
- “Every crash produces an event-log row.”
- “Unmodified TS E2E scripts are the referee.”
- “Schema diff + fixture tests” proves database adoption.

BEAM reduces shared-state failure coupling, but GenServers can block, mailboxes can grow without bound, native code and SQLite can stall, external adapter processes can hang, and supervisors intentionally give up after restart limits. These properties become credible only through bounded calls, monitors, watchdogs, mailbox policies, restart configuration, fault injection, and explicit degraded states.

The AutoCodeBench and Bun-port anecdotes may support the staffing decision, but they provide no evidence for Tightbeam’s ordering, durability, or wire compatibility. Likewise, “first light,” a vertical slice, and a 24-hour happy-path soak cannot serve as production proof. The skeleton must be production architecture, not a disposable prototype hidden behind phase language.

The spec also adds new behavior—telemetry spans, busy timeout, Watchdog fields, and durable crash events—while calling the port behavior unchanged. Those additions may be desirable, but their exact contracts and schema implications must be approved explicitly.

The required independent cross-model review could not be completed: Fable was network-blocked, and the Codex fallback could not initialize in the read-only sandbox. No external review output was used.

## Blocking revisions

Before implementation:

1. Define a durable/authoritative enqueue sequence and multi-producer ordering.
2. Reconcile “same schema” with lane/wake recovery and crash-event persistence.
3. Specify lane, turn-task, adapter-generation, cancel, and unknown-outcome semantics.
4. Redesign the supervision tree around real dependencies, restart intensity, and backoff.
5. Add connection registry, takeover, shared rate-limit, broadcast, and replay-barrier ownership.
6. Reconcile the binding ACP rules with the current 0.59 adapter behavior.
7. Replace the impossible “unmodified scripts” gate with real external black-box/differential tests.
8. Specify exact SQLite connection settings, transaction seams, and bidirectional adopt-in-place proof.
9. Specify Node CLI/ACP-package packaging and executable discovery inside the Mix release deployment.
10. Replace absolute uptime claims with measurable health and fault-injection criteria.

**Verdict: REJECT — the current spec would allow an implementation that loses or reorders turns, duplicates or drops wakes, restart-storms on adapter failure, and passes an acceptance wall that never exercised the BEAM gateway.**

# Adversarial review

The port direction is sound, but the specification is not implementable as written. Its central reliability promises conflict with its “same schema” constraint, and several acceptance tests cannot actually exercise the BEAM gateway.

## 1. Mapping errors

### “Mailbox = FIFO” is insufficient

The TypeScript path performs message persistence, echo broadcast, and `fifo.enqueue()` synchronously in one event-loop turn ([gateway.ts](/Users/mike/src/tightbeam/src/gateway.ts:278)). The proposed OTP system has multiple WebSocket, HTTP, and scheduler processes sending to one lane.

BEAM only guarantees send order from the same sender; it does not establish an application-level order among different senders ([Erlang signal ordering](https://www.erlang.org/doc/system/ref_man_processes.html)). This permits:

1. Connection A inserts message sequence 10.
2. Connection B inserts sequence 11.
3. B’s lane message arrives first.
4. The harness executes 11 before 10.

The lane must own the authoritative enqueue sequence—or consume a durable sequence assigned transactionally by the store. Merely saying “mailbox = FIFO” in [Architecture mapping](/Users/mike/src/shared-workspace/shared/specs/tightbeam-elixir-port.md:54) does not preserve the current ordering.

The acceptance criteria also need concurrent producers, not the current single-caller FIFO test ([fifo.test.ts](/Users/mike/src/tightbeam/src/core/fifo.test.ts:9)).

### A restarted lane cannot recover its state

The proposed lane keeps its queue and current turn in GenServer memory, then says “crash → restart clean + turn marked failed” ([port spec](/Users/mike/src/shared-workspace/shared/specs/tightbeam-elixir-port.md:54)). The existing queue is explicitly volatile ([fifo.ts](/Users/mike/src/tightbeam/src/core/fifo.ts:43)), and the required identical SQLite schema has no turn/queue table.

After a lane crash, the replacement process cannot know:

- Which turn was current.
- Which turns were queued.
- Which terminal state has already been broadcast.
- Whether the adapter accepted or even completed the prompt.

`terminate/2` is not a solution: it is not guaranteed for `:kill`, VM death, or all supervisor shutdown paths. A separate durable turn record or surviving coordinator is required. That conflicts with “same schema, no migration” ([port spec](/Users/mike/src/shared-workspace/shared/specs/tightbeam-elixir-port.md:36)).

### Lane death can leave an ACP turn running

If the lane dies after issuing `session/prompt`, the adapter may continue executing tools and modifying the world. Restarting the lane “clean” and running the next prompt can violate the one-turn-per-session invariant.

The spec must define:

- A supervised per-turn task monitored by the lane.
- What kills/cancels that task when its lane dies.
- How the ACP connection sends `session/cancel` when the original requester disappears.
- Whether an unknown-outcome turn is failed without retry. It must not be automatically retried after potentially executing tools.
- How queued turns resume only after adapter re-adoption completes.

Long-running work must not be awaited inside the lane’s GenServer callback, or cancel/status messages cannot be handled; Elixir explicitly recommends handling task completion asynchronously rather than awaiting long work inside an OTP behaviour ([Task documentation](https://hexdocs.pm/elixir/Task.html)).

### Adapter restart semantics are underspecified

The current gateway caches both adapters and live harness-session objects ([gateway.ts](/Users/mike/src/tightbeam/src/gateway.ts:194)), but never observes `adapter.exited`; today they become stale after a child exit. The port is right to improve this, but “restart + session/load re-adoption” is not a design.

It must specify:

- Who owns the adapter generation and invalidates all stale session handles.
- Whether re-adoption is lazy, as the parent design requires ([tightbeam.md](/Users/mike/src/shared-workspace/shared/specs/tightbeam.md:149)), or eagerly loads every active lane.
- What happens when `session/load` fails or the transcript is missing.
- How simultaneous lane loads are bounded after an adapter restart.
- Whether a normal-but-unexpected Port exit restarts. A `:transient` child does not restart after `normal` or `shutdown` ([OTP child restart semantics](https://www.erlang.org/doc/system/sup_princ.html)).
- How planned idle reaping is distinguished from an unexpected exit.
- How an in-flight turn gets exactly one failed terminal state while pending turns remain ordered.

Eagerly reloading all “live lanes” risks a thundering herd; the parent spec explicitly says load on demand.

### Adapter death can create a lane restart storm

If lanes use synchronous `GenServer.call` against the adapter/connection, one adapter death can make every calling lane exit. Enough simultaneous lane failures can exceed `LaneSupervisor` restart intensity, kill the supervisor, and discard every dynamic child.

OTP supervisors deliberately terminate themselves after exceeding restart intensity; supervision does not imply the application “as a whole does not go down” ([OTP restart intensity](https://www.erlang.org/doc/system/sup_princ.html)). The spec names no restart intensities, backoff, circuit breaker, degraded state, or escalation policy.

### ACP Port framing is not fully mapped

The spec says NDJSON framing is handled with `{:line, ...}` ([port spec](/Users/mike/src/shared-workspace/shared/specs/tightbeam-elixir-port.md:63)). Erlang’s line mode splits lines longer than the configured maximum into one or more `:noeol` fragments, which must be reassembled before JSON decoding ([`open_port` line framing](https://www.erlang.org/doc/apps/erts/erlang.html#open_port/2)).

Acceptance must cover:

- A JSON-RPC line larger than the Port line limit.
- Multiple lines in one OS read.
- Split UTF-8 sequences.
- EOF with an unterminated line.
- Malformed JSON.
- Stderr capture without merging it into NDJSON stdout.
- Port exit before or after `exit_status`.
- Adapter processes surviving an abrupt BEAM VM death; closing a Port does not universally guarantee the OS process exits.

### Adapter rules are contradictory

The port says to carry `PATTERNS.md` rules unchanged ([port spec](/Users/mike/src/shared-workspace/shared/specs/tightbeam-elixir-port.md:39)), but that document still says Claude uses `session/set_model` ([PATTERNS.md](/Users/mike/src/tightbeam/docs/PATTERNS.md:34)). The actual current implementation uses `session/set_config_option` for both adapters because Claude ACP 0.59 dropped `set_model` ([harness.ts](/Users/mike/src/tightbeam/src/acp/harness.ts:118)); the parent spec records the same update ([tightbeam.md](/Users/mike/src/shared-workspace/shared/specs/tightbeam.md:788)).

Following the binding port text would reproduce a known failure. The source-of-truth adapter rules must be reconciled before implementation.

### Per-connection rate limits change behavior

The port claims keepalives and rate limits become per-connection state ([port spec](/Users/mike/src/shared-workspace/shared/specs/tightbeam-elixir-port.md:73)). Current pairing and typing limits are global maps keyed by device ID ([server.ts](/Users/mike/src/tightbeam/src/wire/server.ts:82)); the pairing test deliberately reconnects repeatedly with the same device ID ([server.test.ts](/Users/mike/src/tightbeam/src/wire/server.test.ts:286)).

Moving pairing limits into a connection process resets the limit on every reconnect and breaks existing behavior. A shared device-keyed rate-limit owner is required.

### WebSocket fan-out and takeover ownership are missing

“One process per connection” is accurate for Bandit ([Bandit process model](https://bandit.hexdocs.pm/WebSocket_README.md.html)), but it does not replace the current centralized connection set used for:

- Owner-scoped broadcast.
- Device takeover and `session_replaced`.
- Closing the previous socket atomically.
- Global device rate limits.

Those behaviors currently live in the shared server state ([server.ts](/Users/mike/src/tightbeam/src/wire/server.ts:182), [broadcast path](/Users/mike/src/tightbeam/src/wire/server.ts:333)). The supervision tree needs an explicit connection registry/broadcast owner.

### Replay can race live delivery

The TypeScript auth path synchronously builds the snapshot, sends `auth_result`, stream snapshot, replay messages, and finally `sync_complete` ([server.ts](/Users/mike/src/tightbeam/src/wire/server.ts:205)). In BEAM, concurrent connection and broadcaster processes can send a live message in the middle of replay.

The spec needs a replay watermark and per-connection live-event buffer so that reconnects see neither gaps nor duplicates. This is absent from both mapping and acceptance criteria.

### Wake “at least once” currently ends at volatile enqueue

The current scheduler marks a wake fired after `deliver()` returns ([wakes.ts](/Users/mike/src/tightbeam/src/core/wakes.ts:114)). In production, `deliver()` means “persist an echo and enqueue in memory,” not “the harness accepted or completed the turn” ([gateway.ts](/Users/mike/src/tightbeam/src/gateway.ts:311)).

Therefore:

- Crash after enqueue and mark-fired can lose the queued turn permanently.
- Crash after delivery but before mark-fired can enqueue a duplicate.
- There is no dedupe key linking a wake to its generated message.
- A target retired after scheduling is silently dropped but still marked fired.

The parent spec also says `1:1 wake→turn` ([tightbeam.md](/Users/mike/src/shared-workspace/shared/specs/tightbeam.md:855)), which conflicts with accepting duplicate delivery. The delivery commit point and dedupe mechanism must be specified.

## 2. Missing or invalid acceptance criteria

The largest acceptance-wall problem is literal: the “existing TS scripts, unmodified” cannot run against BEAM. Each imports and starts the TypeScript gateway itself:

- [wire-first-light.ts](/Users/mike/src/tightbeam/scripts/wire-first-light.ts:11)
- [dm-first-light.ts](/Users/mike/src/tightbeam/scripts/dm-first-light.ts:14)
- [agent-uses-cli.ts](/Users/mike/src/tightbeam/scripts/agent-uses-cli.ts:11)

`wire-first-light` also exits zero even when its final `pass` expression is false ([wire-first-light.ts](/Users/mike/src/tightbeam/scripts/wire-first-light.ts:111)). Acceptance wall item 2 is therefore impossible and, in one path, not a trustworthy gate.

Required acceptance additions:

- Refactor or add black-box scripts that accept an external URL/baseDir and never import `startGateway`.
- Differential wire traces: run the same deterministic request trace against TS and BEAM, normalize UUID/timestamps, compare frame shapes and ordering.
- Concurrent posts from multiple sockets plus a wake to one session; assert store sequence equals execution order and no overlap occurs.
- Concurrent same-`c_id` retries: one echo/turn, repeated ack for identical content, conflict without ack for different content. The dedupe scope must remain `(sessionKey, deviceId, clientMessageId)` ([store.ts](/Users/mike/src/tightbeam/src/core/store.ts:85)).
- Reconnect while writes occur; prove replay/live handoff has no gaps or duplicates and `sync_complete` terminates replay.
- Kill lane during current turn and with queued turns.
- Kill adapter during initialize, load, prompt, cancel, after tool effects, and after final chunks but before the JSON-RPC result.
- Kill WakeScheduler before delivery, after enqueue, and before `mark fired`.
- Kill/restart the DB owner while HTTP, replay, and wakes are active.
- Multi-session adapter traffic with interleaved ACP notifications; prove chunks route by `sessionId`.
- Large NDJSON-line and partial-framing tests.
- Normal versus abnormal adapter exit and repeated auth/startup failure, proving no restart storm.
- Exact frame-order assertions for echo, accepted/running, ack, assistant reply, activity-off, and terminal state.
- Soak thresholds: memory growth, mailbox sizes, DB busy errors, scheduler delay, missed/duplicate wakes, restart counts, and response latency. “Zero unexplained restarts” is subjective and does not test recovery.

The spec also claims fixtures are copied verbatim, but the repository has no `test/fixtures/` tree; most tests construct data and fake adapters inline. Porting 76 test names is useful, but not an independent behavioral oracle.

## 3. SQLite adopt-in-place risks

Raw Exqlite is the safer choice, but the current database contract needs to be written down first.

Specific problems:

- TypeScript sets `WAL`, `foreign_keys=ON`, and `synchronous=NORMAL` ([db.ts](/Users/mike/src/tightbeam/src/core/db.ts:7)); it does not set `busy_timeout`. The port silently adds one ([port spec](/Users/mike/src/shared-workspace/shared/specs/tightbeam-elixir-port.md:107)), changing lock-contention timing and error behavior.
- Exqlite currently defaults `busy_timeout` to 2000 ms and defaults journal mode to `DELETE` unless configured. WAL enables concurrent reads, not concurrent writes ([Exqlite connection options](https://exqlite.hexdocs.pm/Exqlite.Connection.html)).
- Foreign-key enforcement and busy handling are connection-specific. Every pooled connection must receive the intended settings; SQLite requires foreign keys to be enabled separately per connection ([SQLite foreign keys](https://www.sqlite.org/foreignkeys.html)).
- “Route writes through contexts” does not enforce single-writer behavior. Context modules callable from many Plug/GenServer processes are still multiple concurrent writers.
- The current check-then-insert operations for message dedupe, spawn idempotency, first-user bootstrap, and handle uniqueness rely partly on the single Node execution context. In BEAM they need transactions plus constraint-error adjudication.
- Ecto migrations would normally introduce migration metadata and encourage schema conventions that do not match camelCase columns and epoch-millisecond integers.
- JSON text produced by Jason may differ from `JSON.stringify` in key ordering or escaping. That matters if “byte-identical” includes stored event payload text or serialized wire bytes.
- A `.schema` textual diff is insufficient. It does not prove row encoding, PRAGMAs, library compile options, transaction behavior, or that TS can reopen data written by BEAM.
- WAL cutover must consider `state.db-wal` and `state.db-shm`. Clean last-close normally checkpoints and removes them, while crash recovery may leave them present ([SQLite WAL lifecycle](https://www.sqlite.org/walformat.html)).

Adoption acceptance should include:

1. TS creates and populates every table, including pending wakes and high AUTOINCREMENT values.
2. BEAM opens the exact directory, runs `integrity_check`/`foreign_key_check`, and changes no schema object.
3. BEAM reads and mutates all row types.
4. BEAM stops; TS reopens the same DB and reads those mutations.
5. Repeat after an intentionally unclean TS termination with WAL sidecars present.
6. Compare `table_xinfo`, `index_xinfo`, foreign keys, triggers, `user_version`, `application_id`, and compile/runtime SQLite versions.
7. Assert no Ecto migration table or other framework metadata appears.
8. Pin and verify every connection’s `journal_mode`, `foreign_keys`, `synchronous`, and explicit busy timeout.

## 4. Supervision-tree flaws

The flat `one_for_one` tree does not encode actual dependencies:

- EventLog, WakeScheduler, Bandit handlers, lanes, and adapters all depend on the database.
- Lanes depend on adapter availability but must not die merely because an adapter dies.
- An adapter owns a Port/connection and per-session ACP routing state, but the proposed relation between `Acp.Adapter` and `Acp.Conn` is not shown.
- A separate EventLog GenServer appears to exist only for code organization; the current event log is a direct database context. If it is a process, its serialization purpose and failure semantics must be stated.
- If a mutation succeeds and EventLog dies before the append, the caller may see failure after the side effect already occurred. Retrying can duplicate non-idempotent work.

The tree needs at least explicit subtrees and ownership:

- Core DB ownership and readiness.
- Connection registry/broadcaster.
- Adapter subtree in which adapter lifecycle and Port lifecycle are one coherent work unit.
- Lane supervisor plus turn-task supervisor.
- An adapter directory/coordinator publishing adapter generations and degraded state.
- Restart intensities, backoff, and failure escalation for each subtree.
- Readiness behavior while DB recovery or scheduler catch-up is occurring.

The assertion that every crash creates an event-log row is also impossible for a crash caused by database failure, and the existing `events.kind` constraint only allows `verb|denied` ([events.ts](/Users/mike/src/tightbeam/src/core/events.ts:34)). Adding lifecycle events changes the supposedly identical schema/contract.

## 5. Positions on the four open questions

1. **Bandit vs Cowboy: Bandit.** Bandit already provides the desired one-process-per-WebSocket model and Plug/WebSock integration. The choice does not solve connection registration, takeover, replay barriers, or slow-client mailbox growth; those remain application responsibilities.

2. **Ecto vs raw Exqlite: raw Exqlite.** Adopt-in-place, exact camelCase schema, explicit SQL, and no migrations favor raw SQL. Put writes behind an actual serialized ownership/transaction seam; use separately configured read connections only if needed. Rename `Tightbeam.Repo` to something such as `Tightbeam.DB`, because “Repo” falsely implies Ecto.

3. **Mix release vs Burrito: Mix release.** TARS is a controlled target, and this product still requires Node for the retained CLI and ACP adapter packages. Burrito does not make the overall artifact self-contained and adds packaging/cross-build risk without solving those Node assets. Include ERTS in the release and pin OTP/Elixir/SQLite/adapter versions.

4. **Telemetry surface:** `/version` should preserve compatibility fields and expose static release/build identity. Do not rename scheduler/run-queue data to the existing Node `loopLagP99Ms`; either retain a real timer-jitter equivalent or version the field. `/health` should contain dynamic core readiness: DB read/write probe, wake scan age, supervisor/restart counters, scheduler/run-queue summaries, and degraded adapter counts. Lazy adapter failure should degrade the affected sessions, not make the whole gateway globally unready.

## 6. Wishful versus verifiable

Wishful claims include:

- “The app as a whole does not go down.”
- “No process can wedge the system.”
- “Nothing dies silently.”
- “A slow client can only hurt itself.”
- “Every crash produces an event-log row.”
- “Unmodified TS E2E scripts are the referee.”
- “Schema diff + fixture tests” proves database adoption.

BEAM reduces shared-state failure coupling, but GenServers can block, mailboxes can grow without bound, native code and SQLite can stall, external adapter processes can hang, and supervisors intentionally give up after restart limits. These properties become credible only through bounded calls, monitors, watchdogs, mailbox policies, restart configuration, fault injection, and explicit degraded states.

The AutoCodeBench and Bun-port anecdotes may support the staffing decision, but they provide no evidence for Tightbeam’s ordering, durability, or wire compatibility. Likewise, “first light,” a vertical slice, and a 24-hour happy-path soak cannot serve as production proof. The skeleton must be production architecture, not a disposable prototype hidden behind phase language.

The spec also adds new behavior—telemetry spans, busy timeout, Watchdog fields, and durable crash events—while calling the port behavior unchanged. Those additions may be desirable, but their exact contracts and schema implications must be approved explicitly.

The required independent cross-model review could not be completed: Fable was network-blocked, and the Codex fallback could not initialize in the read-only sandbox. No external review output was used.

## Blocking revisions

Before implementation:

1. Define a durable/authoritative enqueue sequence and multi-producer ordering.
2. Reconcile “same schema” with lane/wake recovery and crash-event persistence.
3. Specify lane, turn-task, adapter-generation, cancel, and unknown-outcome semantics.
4. Redesign the supervision tree around real dependencies, restart intensity, and backoff.
5. Add connection registry, takeover, shared rate-limit, broadcast, and replay-barrier ownership.
6. Reconcile the binding ACP rules with the current 0.59 adapter behavior.
7. Replace the impossible “unmodified scripts” gate with real external black-box/differential tests.
8. Specify exact SQLite connection settings, transaction seams, and bidirectional adopt-in-place proof.
9. Specify Node CLI/ACP-package packaging and executable discovery inside the Mix release deployment.
10. Replace absolute uptime claims with measurable health and fault-injection criteria.

**Verdict: REJECT — the current spec would allow an implementation that loses or reorders turns, duplicates or drops wakes, restart-storms on adapter failure, and passes an acceptance wall that never exercised the BEAM gateway.**