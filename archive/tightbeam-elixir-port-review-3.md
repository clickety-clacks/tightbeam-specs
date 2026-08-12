| 8 | Packaging/doctor | **Newly broken.** The specified package identity/path does not match the actual npm package, and `doctor` is not a standard Mix-release command. |
| 9 | Boot epochs/restart intensities | **Newly broken.** Worker-specific restart intensities cannot exist in the drawn tree, and the epoch mechanism lacks DDL, DB-restart semantics, and durable adapter-generation linkage. |

## Blocking defects

1. **Quarantine cannot establish quiescence.** V3 says the adapter monitors a TurnTask, sends `session/cancel`, and then “drops the pending entry” ([spec:171](/Users/mike/src/shared-workspace/shared/specs/tightbeam-elixir-port.md:171)). ACP cancellation is a notification; successful cancellation is confirmed by the eventual response to the original prompt ([local ACP schema](/Users/mike/src/tightbeam/node_modules/@agentclientprotocol/sdk/schema/schema.json:8361)). Dropping the pending entry discards that confirmation.

   Meanwhile, `turns` stores no adapter key, generation, ACP session/request reference, or owner token. A replacement lane cannot distinguish:

   - no request was ever sent;
   - cancellation is still in progress;
   - the old request completed after the requester died;
   - the relevant adapter generation was actually recycled.

   The result is either permanent quarantine or premature release and overlapping prompts.

2. **The monitor protocol cannot cancel a blocked TurnTask.** The precise topology uses `async_nolink` ([spec:171](/Users/mike/src/shared-workspace/shared/specs/tightbeam-elixir-port.md:171)), then later claims lane death kills the task through a link ([spec:203](/Users/mike/src/shared-workspace/shared/specs/tightbeam-elixir-port.md:203)). Both cannot be true.

   More importantly, the Adapter contract stores a `GenServer.call`’s `from` and replies later. The TurnTask remains blocked waiting for that reply; it does not execute logic for the lane’s queued `:DOWN` message. `GenServer.call` is synchronous and blocks its caller until reply or timeout ([Elixir GenServer documentation](https://hexdocs.pm/elixir/1.15.0/GenServer.html)). A custom asynchronous request/receive loop is required but not specified.

3. **The persistent sequence filter creates message loss.** Consider:

   1. Writer A commits message sequence 10 and is preempted before publication.
   2. Writer B commits sequence 11 and publishes it.
   3. The connection advances `lastDeliveredSeq` to 11.
   4. A finally publishes 10; the `seq ≤ lastDeliveredSeq` rule drops it forever.

   The single DB writer serializes commits, not the caller processes’ later publications. The filter therefore requires an ordered publication seam, reorder buffer, or store-backed gap fill. None is specified.

   The per-connection session map also grows without a retirement/pruning rule. Generation-tagged takeover only protects unregister; because old-socket closure is asynchronous, the stale handler can continue posting until it actually closes unless every inbound operation validates its registration generation.

4. **The Reconciler has no ownership protocol.** A DynamicSupervisor alone does not provide one-lane-per-session naming. V3 does not define unique registration, atomic `queued → running` ownership, or how a nudged live lane distinguishes its own running turn from an orphan. Yet recovery says any found running turn becomes `failed_unknown` ([spec:100](/Users/mike/src/shared-workspace/shared/specs/tightbeam-elixir-port.md:100)).

   Its global five-second `WHERE status IN (...)` scan also lacks a status-leading index. `turns_session(sessionKey,status,seq)` cannot efficiently serve an ever-growing ledger scanned by status alone.

5. **Terminal publication remains internally contradictory.** V3 correctly promises one durable transition plus at-least-once publication ([spec:80](/Users/mike/src/shared-workspace/shared/specs/tightbeam-elixir-port.md:80)), but immediately retains the heading and rule “Exactly-once terminal broadcast” ([spec:105](/Users/mike/src/shared-workspace/shared/specs/tightbeam-elixir-port.md:105)).

   `publishedAt` only proves whatever “broadcasting” means. If that is a cast or enqueue to connection processes, it can be stamped before any socket write. The defensible promise is at-least-once durable broadcast attempt, unless a stronger acknowledgement seam is specified. The shown terminal CAS also fails to set `endedAt`, although the unpublished index only includes rows with `endedAt IS NOT NULL`.

6. **The supervision and packaging contracts are not executable as written.**

   - Restart intensity belongs to a supervisor, not an individual worker. The root can have `3/30s`, but direct children such as DB, ConnRegistry, and LaneManager cannot each have `5/60s` without additional supervisors. A supervisor exits after exceeding its own configured intensity ([Elixir Supervisor documentation](https://elixir.hexdocs.pm/main/Supervisor.html)).
   - `boot_epochs` has no DDL and is absent from the declared additive-table list. “At boot” also does not say whether every DB-owner restart opens a new epoch; a DB worker crash does not reboot the application.
   - Adapter generations are coordinator memory. A coordinator/root restart can reset them, and no turn row records the generation that owned an orphan.
   - The repository package is named `tightbeam`, version `0.0.1` ([package.json](/Users/mike/src/tightbeam/package.json:2)); `npm pack` therefore does not naturally produce `tightbeam-cli-<ver>.tgz` or install at `node_modules/tightbeam-cli`.
   - Mix releases support commands such as `eval` and `rpc`, not an intrinsic `doctor` command ([Mix release documentation](https://hexdocs.pm/mix/Mix.Tasks.Release.html)). V3 must specify an actual overlay/wrapper or use `bin/tightbeam_gateway eval "Tightbeam.ReleaseTasks.doctor()"`.

## TypeScript verification

Commits `136519e` and `649a02e` are present on `main`.

- [PATTERNS.md](/Users/mike/src/tightbeam/docs/PATTERNS.md:34) and executable [harness.ts](/Users/mike/src/tightbeam/src/acp/harness.ts:121) now consistently require `session/set_config_option` with a bare model plus the harness-specific effort option.
- `package.json` and the root package-lock entry contain identical runtime and development dependency sets.
- The v3 success-order oracle is correct: echo precedes FIFO enqueue ([gateway.ts](/Users/mike/src/tightbeam/src/gateway.ts:278)); accepted/running and activity-on occur synchronously before dispatch returns; ack follows dispatch ([server.ts](/Users/mike/src/tightbeam/src/wire/server.ts:272)); assistant precedes terminal, then typing/activity-off ([gateway.ts](/Users/mike/src/tightbeam/src/gateway.ts:233)).
- The “fully purged” claim is not literally true: tracked root [harness.ts](/Users/mike/src/tightbeam/harness.ts:4) and a [test title](/Users/mike/src/tightbeam/src/acp/harness.test.ts:86) retain obsolete `set_model` wording. They are not the declared executable source of truth, so this is non-blocking but hazardous for pattern propagation.
- The E0 artifacts are still future work: all three current drivers still import `startGateway`, and no `test/golden/` comparator or standalone deterministic adapter exists.

The mandated independent review produced no evidence: Fable failed with `ENOTFOUND`; the GPT‑5.6 SOL fallback could not initialize under the read-only runtime. Neither failure was treated as corroboration.

**REJECT — v3 fixes the TypeScript referee and source-rule defects, but its recovery path cannot prove orphan quiescence, its live sequence filter can silently discard committed messages, and its supervision/packaging contracts remain unimplementable as specified.**
