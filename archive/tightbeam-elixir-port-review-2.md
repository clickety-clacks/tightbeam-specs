
1. **A committed wake or post can remain queued forever.** The transaction can commit the message, `turns` row, and fired wake, followed by a crash before the lane doorbell. On restart, the wake is no longer pending, `wakeId` correctly prevents reinsertion, and a restarted DynamicSupervisor has no remembered SessionLane child. Nothing scans committed queued turns and starts/nudges their lanes.

   Therefore `wakeId` dedupe solves uniqueness, but not liveness across the scheduler/VM crash window. A boot-time and periodic queued/running-turn reconciler must be an explicit LaneSupervisor responsibility.

2. **“Exactly-once terminal broadcast” is false.** The CAS at [lines 74–76](/Users/mike/src/shared-workspace/shared/specs/tightbeam-elixir-port.md:74) guarantees one durable terminal transition. If the process crashes after that update commits but before broadcasting, recovery sees a terminal row and emits nothing. This is at-most-once publication, possibly zero times.

   Specify either durable terminal-event delivery with client dedupe, or weaken the promise to exactly-one durable transition. Exactly-once socket receipt cannot come from `rows-affected=1`.

3. **Lane recovery can overlap prompts.** Marking an orphan `failed_unknown` and issuing asynchronous `session/cancel` does not establish that the ACP adapter has stopped the old request. Resuming queued work after adoption can start another prompt while the original still executes. Recovery must quarantine that session until the original request terminates or the adapter generation is recycled.

4. **The task topology contradicts itself.** [Lines 138–146](/Users/mike/src/shared-workspace/shared/specs/tightbeam-elixir-port.md:138) say the lane monitors the task, stays alive when it fails, yet lane death kills the task through a link. Links are bidirectional: without trapping exits, task failure kills the lane; with `async_nolink`, lane death does not kill the task. Define the precise one-way monitor/exit protocol and add the missing TaskSupervisor to the actual tree.

   The Adapter must also use asynchronous GenServer replies; a `handle_call` waiting on ACP prevents Port responses and cancellation from being processed.

5. **ConnRegistry’s replay barrier is incomplete.** A message can commit before the replay watermark but have its live publication reach ConnRegistry only after buffered draining finishes. Replay sends the row, then the delayed live push duplicates it because the stated dedupe applies only while draining. The design needs an ordered publication seam or a persistent per-connection delivered-sequence filter beyond the buffer phase.

   Takeover likewise cannot atomically “send + close + register.” Atomically swap to a generation-tagged new registration first, notify/close the old connection asynchronously, and make old unregister compare its generation so it cannot delete the replacement.

6. **The E0 oracle contradicts TypeScript.** V2 puts terminal state after typing/activity-off at [lines 187–189](/Users/mike/src/shared-workspace/shared/specs/tightbeam-elixir-port.md:187). TS broadcasts terminal first, then typing-off and activity-off in [gateway.ts](/Users/mike/src/tightbeam/src/gateway.ts:256). Production also sends the ack after dispatch returns in [server.ts](/Users/mike/src/tightbeam/src/wire/server.ts:272), but E0 omits ack entirely.

   The external CLI drivers also require both `TIGHTBEAM_URL` and `TIGHTBEAM_TOKEN`, as shown in [main.ts](/Users/mike/src/tightbeam/src/cli/main.ts:45). Golden traces need a controlled deterministic ACP adapter, not a live model instructed to reply deterministically.

7. **Commit `e446bc6` did not fully reconcile ACP guidance.** [PATTERNS.md](/Users/mike/src/tightbeam/docs/PATTERNS.md:34) still mandates `session/set_model`, then says Claude dropped it. The top of [harness.ts](/Users/mike/src/tightbeam/src/acp/harness.ts:3) repeats the obsolete rule, while the executable implementation correctly uses `session/set_config_option` at line 118.

8. **Packaging is not yet executable.** The current [package.json](/Users/mike/src/tightbeam/package.json:15) omits the ACP packages present in [package-lock.json](/Users/mike/src/tightbeam/package-lock.json:10). `npm ci` alone also does not explain how the compiled private root CLI, its wrapper, and `dist/cli/main.js` enter `<baseDir>/runtime/`. Define the shipped package manifest, compiled CLI artifact, wrapper path, adapter command paths, and an actual release command for `tightbeam-doctor`. A preboot doctor connection cannot prove future read-pool checkout PRAGMAs.

9. **Lifecycle acceptance is impossible as written.** `Tightbeam.Lifecycle` depends on DB and is itself terminated by the root `rest_for_one` recovery. It cannot reliably record the DB crash that removed its writer, and `kill -9` cannot emit an event before death. Persisted boot epochs/clean-shutdown markers and post-restart dirty-exit inference are required. Root and non-adapter restart intensities also remain unspecified.

**REJECT — v2 resolves the broad schema and SQLite strategy, but the durable-turn mechanism still violates its own conservation invariant under ordinary crash windows, and the task, replay, referee, and packaging contracts are not implementation-safe.**
tokens used
220,248
# Round 2 verdict: REJECT

Reviewed the current 262-line revision of [tightbeam-elixir-port.md](/Users/mike/src/shared-workspace/shared/specs/tightbeam-elixir-port.md) (SHA-256 `979ef8a1…b7d6d65b`). V2 is substantially better, but it still permits stranded committed turns, lost terminal broadcasts, and overlapping orphaned ACP prompts. Those directly contradict its new binding prompt-conservation law.

| # | V1 blocker | Round-2 adjudication |
|---|---|---|
| 1 | Authoritative enqueue/order | **Partially resolved.** `turns.seq` gives sound per-session execution order when lanes always query `ORDER BY seq`. Visible enqueue events and post-commit dispatch remain unsound. |
| 2 | Schema vs recovery/events | **Mostly resolved.** Additive tables are compatible with TS reopening the database. `lifecycle_events` still lacks DDL and crash-record semantics. |
| 3 | Lane/task/adapter semantics | **Not resolved.** Link/monitor topology is contradictory, orphan cancellation is not a quiescence barrier, and an Adapter GenServer may still block. |
| 4 | Supervision/restart design | **Partially resolved.** DB ordering and adapter backoff improved. The drawn tree is not a valid ownership tree, TaskSupervisor is absent, and restart intensities are unspecified. |
| 5 | ConnRegistry/replay | **Hand-waved.** Responsibilities are named, but takeover and replay algorithms remain insufficient. |
| 6 | ACP rule reconciliation | **Not resolved.** The cited “corrected” sources still contradict their executable implementation. |
| 7 | Real black-box referee | **Newly broken in detail.** E0 is the correct phase, but its prescribed frame order disagrees with TS and omits required CLI authentication. |
| 8 | SQLite transaction/adoption proof | **Resolved.** Single writer, explicit PRAGMAs, deliberate busy timeout, and bidirectional proof are adequate. |
| 9 | Packaging/doctor | **Hand-waved.** The install artifact, CLI build/wrapper, manifest, executable layout, and actual release doctor command remain unspecified. |
| 10 | Measurable reliability | **Mostly resolved.** Health and soak thresholds are concrete, but lifecycle proof for DB failure/`kill -9` is not implementable as described, and absolute loss claims have reappeared. |

## Blocking defects

1. **A committed wake or post can remain queued forever.** The transaction can commit the message, `turns` row, and fired wake, followed by a crash before the lane doorbell. On restart, the wake is no longer pending, `wakeId` correctly prevents reinsertion, and a restarted DynamicSupervisor has no remembered SessionLane child. Nothing scans committed queued turns and starts/nudges their lanes.

   Therefore `wakeId` dedupe solves uniqueness, but not liveness across the scheduler/VM crash window. A boot-time and periodic queued/running-turn reconciler must be an explicit LaneSupervisor responsibility.

2. **“Exactly-once terminal broadcast” is false.** The CAS at [lines 74–76](/Users/mike/src/shared-workspace/shared/specs/tightbeam-elixir-port.md:74) guarantees one durable terminal transition. If the process crashes after that update commits but before broadcasting, recovery sees a terminal row and emits nothing. This is at-most-once publication, possibly zero times.

   Specify either durable terminal-event delivery with client dedupe, or weaken the promise to exactly-one durable transition. Exactly-once socket receipt cannot come from `rows-affected=1`.

3. **Lane recovery can overlap prompts.** Marking an orphan `failed_unknown` and issuing asynchronous `session/cancel` does not establish that the ACP adapter has stopped the old request. Resuming queued work after adoption can start another prompt while the original still executes. Recovery must quarantine that session until the original request terminates or the adapter generation is recycled.

4. **The task topology contradicts itself.** [Lines 138–146](/Users/mike/src/shared-workspace/shared/specs/tightbeam-elixir-port.md:138) say the lane monitors the task, stays alive when it fails, yet lane death kills the task through a link. Links are bidirectional: without trapping exits, task failure kills the lane; with `async_nolink`, lane death does not kill the task. Define the precise one-way monitor/exit protocol and add the missing TaskSupervisor to the actual tree.

   The Adapter must also use asynchronous GenServer replies; a `handle_call` waiting on ACP prevents Port responses and cancellation from being processed.

5. **ConnRegistry’s replay barrier is incomplete.** A message can commit before the replay watermark but have its live publication reach ConnRegistry only after buffered draining finishes. Replay sends the row, then the delayed live push duplicates it because the stated dedupe applies only while draining. The design needs an ordered publication seam or a persistent per-connection delivered-sequence filter beyond the buffer phase.

   Takeover likewise cannot atomically “send + close + register.” Atomically swap to a generation-tagged new registration first, notify/close the old connection asynchronously, and make old unregister compare its generation so it cannot delete the replacement.

6. **The E0 oracle contradicts TypeScript.** V2 puts terminal state after typing/activity-off at [lines 187–189](/Users/mike/src/shared-workspace/shared/specs/tightbeam-elixir-port.md:187). TS broadcasts terminal first, then typing-off and activity-off in [gateway.ts](/Users/mike/src/tightbeam/src/gateway.ts:256). Production also sends the ack after dispatch returns in [server.ts](/Users/mike/src/tightbeam/src/wire/server.ts:272), but E0 omits ack entirely.

   The external CLI drivers also require both `TIGHTBEAM_URL` and `TIGHTBEAM_TOKEN`, as shown in [main.ts](/Users/mike/src/tightbeam/src/cli/main.ts:45). Golden traces need a controlled deterministic ACP adapter, not a live model instructed to reply deterministically.

7. **Commit `e446bc6` did not fully reconcile ACP guidance.** [PATTERNS.md](/Users/mike/src/tightbeam/docs/PATTERNS.md:34) still mandates `session/set_model`, then says Claude dropped it. The top of [harness.ts](/Users/mike/src/tightbeam/src/acp/harness.ts:3) repeats the obsolete rule, while the executable implementation correctly uses `session/set_config_option` at line 118.

8. **Packaging is not yet executable.** The current [package.json](/Users/mike/src/tightbeam/package.json:15) omits the ACP packages present in [package-lock.json](/Users/mike/src/tightbeam/package-lock.json:10). `npm ci` alone also does not explain how the compiled private root CLI, its wrapper, and `dist/cli/main.js` enter `<baseDir>/runtime/`. Define the shipped package manifest, compiled CLI artifact, wrapper path, adapter command paths, and an actual release command for `tightbeam-doctor`. A preboot doctor connection cannot prove future read-pool checkout PRAGMAs.

9. **Lifecycle acceptance is impossible as written.** `Tightbeam.Lifecycle` depends on DB and is itself terminated by the root `rest_for_one` recovery. It cannot reliably record the DB crash that removed its writer, and `kill -9` cannot emit an event before death. Persisted boot epochs/clean-shutdown markers and post-restart dirty-exit inference are required. Root and non-adapter restart intensities also remain unspecified.

**REJECT — v2 resolves the broad schema and SQLite strategy, but the durable-turn mechanism still violates its own conservation invariant under ordinary crash windows, and the task, replay, referee, and packaging contracts are not implementation-safe.**
