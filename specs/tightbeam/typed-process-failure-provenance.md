# Typed process-failure provenance

Status: revision candidate after changes-requested `att_58d86e6c-026c-4c39-9812-2b6e5000b05f`; do not bind before a successor immutable artifact receives independent reviewed-clean

Work item: `wi_7efb0887-7fd4-410d-9d63-b309a962851e`

Spec assignment: recovery `asg_8bcedc04-0676-411c-beb0-574db15f69b5`; predecessor `asg_f130c566-3825-49f7-9321-1cc141297642`

Reviewed authority: `art_054cb5af`, SHA-256 `f8ec787572c32922d04a431a713f9634131eeef4e79828728c99930df5b66e88`, reviewed clean by `att_e6a2d6cb-a96a-4a54-b74b-46e07f1035f9`

Revision review: exact predecessor `art_3b042780`, SHA-256 `36abf6f049bcd2c7b2f428918375f0568d72935f4dccd7507463dd733ed9ced5`; changes requested by `att_58d86e6c-026c-4c39-9812-2b6e5000b05f`, full report `art_58551c36`

Source seam map: local `origin/main` for `/home/mike/tb-restore` at `ac8651dcb104f312da1c67e0cb7b1abebc640b2b`, observed 2026-08-12 UTC
Operating guidance change: none. This spec defines product behavior and does not teach an agent operating pattern.

## Invariants

### I-01 — One typed failure contract

Each newly admitted in-scope attempt that terminalizes as a failure has one versioned `FailureEnvelope`. The row that owns the work stores the envelope. `failure_delivery` and `failure_action` are the only bounded companion records keyed by `failureId`. The implementation does not create a generic error registry.

Acceptance: cases A01, A02, A06, A20, and A25.

### I-02 — Identity is immutable

Admission creates `attemptId` once. Failure terminalization derives `failureId` deterministically from that attempt. The system keeps `attemptId`, `failureId`, `correlationId`, origin, settlement, and `predecessorAttemptId` immutable after commit. Each marker, reader projection, parent notice, and terminal-owner alert for that failure uses the same identifiers.

Acceptance: cases A01, A06, A08, A19, and A20.

### I-03 — Replay is a read; retry is a new attempt

A same-principal, same-key, same-digest replay reads the original settlement and performs no effect. A retry creates a new `attemptId`, records the prior attempt in `predecessorAttemptId`, and leaves the prior attempt unchanged. `safe_same_attempt` is not a legal value. When a retry supersedes a pending predecessor action, a receiver that loses the action-state ordering creates no stale actionable projection. The substrate does not retry failed work automatically.

Acceptance: cases A05, A08, A15, A16, and A17.

### I-04 — Failure settlement is one database transaction

For an in-scope failure, the terminal compare-and-set, owning-row envelope, bounded legacy error text, lifecycle fact, typed local or target marker, applicable `failure_action`, parent delivery row, and terminal-owner delivery row commit together or roll back together. The terminal compare-and-set and all dependent writes are indivisible. A losing terminal compare-and-set creates no dependent fact.

Acceptance: cases A06, A08, A17, A19, and A23.

### I-05 — Outbox truth survives worker failure

Delivery intent exists only as a committed `failure_delivery` row. A worker crash before settlement commit leaves no delivery. A worker crash after commit cannot erase delivery intent. A payload-integrity conflict ends in the closed terminal delivery state `integrity_conflict`; it does not remain leased or re-enter the retry queue. A worker does not infer intent from a marker, transcript position, log, or message adjacency.

Acceptance: cases A06, A07, and A26.

### I-06 — Every delivery mutation is fenced

A claim or reclaim uses `deliveryId`, a monotonically increasing `leaseEpoch`, a fresh opaque `leaseToken`, and `leaseOwner`. A pending row is eligible only when its persisted `nextAttemptAt` is null or is at or before the claimant's one captured `claimNow`; an expired lease is independently eligible. Claim, acknowledgement, send-failure reschedule, action supersession, and integrity-conflict terminalization each compare the required current state and lease identity in one compare-and-set. A stale worker changes zero rows. Reclaim changes the epoch and token before another send.

Acceptance: cases A07, A15, and A26.

### I-07 — Receiver dedupe binds identity to bytes

The receiver transaction insert-or-reads `(deliveryId, publicPayloadHash)` before it creates a visible projection. Same-ID, same-hash replay returns the stored projection or supersession tombstone. Same-ID, different-hash replay returns `failure_delivery_integrity_conflict` and creates no second projection. A receiver or worker hash conflict causes one principal-bearing durable fact, a fenced transition to terminal `integrity_conflict`, and a bounded owner-readable status. No later claim or send is legal.

Acceptance: case A26.

### I-08 — ACP generation fencing detects the event

The connection owner settles every admitted ACP origin exactly once through the closed mutation seam: a valid response settles that origin with the owning result, while a clean generation close or first undecodable frame settles every origin still admitted. Guarded request admission, response settlement, clean close, frame write, and desynchronization are serialized by the connection owner. A generation-wide failure gives each affected failure the same deterministic `connectionFaultRef` and attributes the event to no individual request. A timeout proxy does not fence a generation.

Acceptance: cases A11, A12, A13, and A22.

### I-09 — Commit-to-send has no unfenced interval

If guarded ACP admission wins first, its durable admitted row commits and its frame is written before a generation fence can win. If a clean-close or desynchronization fence wins first, admission writes no origin row and sends no frame. If a valid response settlement wins before desynchronization, that origin is no longer in the admitted set; if desynchronization wins, the later response reads the settled origin and creates no success. A crash after admission commit and before frame write leaves an admitted row that recovery settles without resend.

Acceptance: case A22.

### I-10 — Outcome, retry, action, owner, and deadline form a closed product

The implementation accepts only the tuples in Architecture §Legal settlement matrix. It rejects every unlisted tuple before persistence. `failed_unknown` maps only to `outcome=unknown`, `retryDisposition=verify_then_new_attempt`, and `nextAction=inspect_effect`. An action other than `none` has a durable owner, a distinct valid persisted fallback owner, and one immutable server-policy deadline snapshot. `nextAction=none` has no deadline or deadline-policy fields.

Acceptance: cases A08, A16, A17, and A23.

### I-11 — No-effect retry requires evidence

`new_attempt_now` is legal only with durable, unexpired `noEffectEvidence` of kind `declared_read_only`, `pre_mutation_refusal`, or `verified_external_state`. Prose is not evidence. An expired or missing evidence row rejects the settlement tuple.

Acceptance: cases A13 and A16.

### I-12 — Owner routing and parent routing are different facts

Admission persists the primary and fallback candidates for `ownerRoute`. An actionable route without a distinct valid persisted fallback fails closed. Settlement selects the primary session only when that exact session row has `state=active`; otherwise it selects the persisted fallback and records why. An assignment fallback outranks a spawned parent. Parent routing uses `spawnedBy` independently. Parentless or unavailable parent routing produces a typed `not_applicable` delivery row and never substitutes the terminal owner.

Acceptance: cases A18 and A20.

### I-13 — The substrate routes; an accountable mind decides

The substrate classifies an observed failure, applies the closed legal matrix, routes the public projection, and verifies deadlines. It does not choose whether to repeat unknown work, resolve `user_decision`, or invent a new action. A later execution requires an explicit actor and a new attempt.

Acceptance: cases A08, A16, A17, and A23.

### I-14 — Public readers share one projection

Target chat, transcript, parent notice, terminal-owner alert, wire response, CLI response, and trace use `FailurePublicV1`. Each surface preserves the same safe fields. Raw maps and reader-specific cause reconstruction are not authority.

Acceptance: cases A01, A02, A18, A19, A21, and A25.

### I-15 — Safe mapping is closed and fail-closed

The command edge owns one versioned closed switch for observed input shapes. Unlisted or incomplete shapes map to fixed class-only or unknown causes. Arbitrary provider prose does not enter public output. `reportedAtLayer` records where Tightbeam observed a value. `upstreamClaim` records only an allowlisted assertion present in the observed payload.

Acceptance: cases A03, A10, A21, and A24.

### I-16 — Unknown stays unknown

The implementation does not convert `Internal error` into a provider cause, EOF into an outcome, `failed_unknown` into retry permission, a malformed frame into an incident-specific attribution, or source equality into selection provenance.

Acceptance: cases A03, A04, A05, A08, A10, A11, A19, and A24.

### I-17 — Model and effort provenance are independent

For each tune attempt, model selection and effort selection each preserve the submitted value or null, resolved value or null, and one closed source enum. The attempt also records the destination harness whose catalog validated the pair. The implementation captures these facts in the selection function that resolves them; it does not infer them after the result.

Acceptance: case A19.

### I-18 — Legacy history is retained without fabricated typing

Legacy idempotency successes replay forever with `digestCheck=unavailable`. Migration maps each legacy user key into the closed principal tuple `{kind=user,id=ownerUserId}` without changing its replay namespace. Historical failure rows remain `legacy_untyped` and retain their stored bounded text. Migration does not fabricate a digest, attempt, cause code, layer, outcome, retry rule, owner, or envelope for a historical row.

Acceptance: case A14.

### I-19 — Every marker names cause and principal

Each lifecycle fact, message marker, action, delivery, connection event, and integrity conflict written by this mechanism carries its `failureId` or `connectionFaultRef` and the accountable principal that wrote or asserted it. A prose-only relationship is not a link.

Acceptance: cases A01, A06, A11, A17, A19, A23, and A26.

### I-20 — New writes are structurally typed

Constructors, closed enums, database checks, unique indexes, foreign keys, and compare-and-set functions reject missing identities, invalid matrix tuples, mismatched owner-row linkage, and unsafe projection fields. New code has one mutation seam for failure state. Review guidance alone is not the enforcement rung.

Acceptance: cases A16, A20, A24, and A26.

### I-21 — Recovery is deterministic and performs no work retry

Boot captures one `bootNow`. Before traffic starts, it reconciles exact-shape migration state, closed or desynchronized connection generations, admitted origins left pending, running turns, stale v2 command attempts, expired actions, and expired delivery leases. Repeating recovery yields the same facts. A committed `failure-provenance-v1` shape is forward-only; recovery never restores a pre-migration database or starts an old-shape binary after that commit. Recovery does not resend an ACP request or repeat a user effect.

Acceptance: cases A06, A08, A12, A17, A22, and A23.

### I-22 — Compatibility retains old observable contracts

Existing clients retain the marker prefix, bounded legacy error string, unkeyed command behavior, and session-control `HTTP 200` with `ok=false` and `code`. Additive typed fields do not change the meaning of existing success responses. An old keyed client may omit `requestDigest`; the server computes the canonical digest. A new client may send it and receives a conflict if it disagrees with the server computation.

Acceptance: cases A04, A05, A14, A15, and A19.

### I-23 — Observability is derived from durable facts

Metrics compute only the enumerated safe groups, counts, and ages in Architecture §Observability from persisted typed fields. Public trace reads persisted envelope, action, delivery, connection, and migration rows only through `FailurePublicV1`. Neither surface parses public prose or exposes a diagnostic field.

Acceptance: cases A08, A12, A17, A21, A23, and A25.

### I-24 — Every incident leaves reusable evidence

The acceptance suite uses immutable fixtures captured from the reviewed incidents or recorded boundary responses. A hand-written ideal response cannot substitute for a named real fixture. A synthetic malformed frame is permitted only for the protocol parser seam because the reviewed authority marks a historical malformed-frame incident as not proven.

Acceptance: cases A01–A05, A09–A11, A14, and A19.

## Goal

Implement typed, durable, redaction-safe failure provenance for accepted turns, keyed wire/process submissions, the reviewed session-control denial path, and ACP connection-generation failures. Make the owning reader, parent route, terminal owner, and wire caller receive the same safe cause and immutable attempt identity. Preserve honest outcome uncertainty and make repetition an explicit new attempt.

The smallest corrective unit is one `FailureEnvelope`, one `failure_delivery` outbox row per asynchronous surface-and-destination tuple, and at most one `failure_action` row. ADD wins over deleting the failure surfaces because owners still need those surfaces to recover work; ACCEPT loses because the reviewed incidents prove anonymous or raw failure delivery strands owners and leaks unsafe detail.

Fixture-dependent implementation is ready for build only after this exact spec hash receives independent adversarial `reviewed-clean`, the work item binds that hash, and OQ-01 closes by binding a separately immutable fixture manifest to this work item and exact spec hash. Fixture custody does not amend or rebind this spec. A separately assigned schema/type-only scope may proceed after the spec hash is reviewed and bound only when the reviewer confirms that scope encodes no fixture-derived assumption.

## Non-Goals

1. Do not create a generic error, handler, provider, or projection registry.
2. Do not make a raw map, arbitrary exception, stack, stderr tail, prompt, credential, filesystem path, account URL, or provider prose authoritative for a public reader.
3. Do not fabricate a provider cause, request attribution, outcome, retry rule, owner, digest, selection source, or upstream claim.
4. Do not treat `Internal error`, JSON-RPC `-32603`, EOF, empty HTTP body, `:normal`, `:noproc`, timeout, or `failed_unknown` as a deeper cause than observed evidence supports.
5. Do not retry failed work, resubmit ACP requests during recovery, or turn an action deadline into execution. Delivery replay is notification recovery, not work retry.
6. Do not replace the existing turn ledger, messages projection, assignment model, user stream, harness-process ledger, or adapter coordinator.
7. Do not infer message correlation from adjacency or parse Bubble prose.
8. Do not backfill typed envelopes into historical failed rows.
9. Do not migrate a database with a missing, unknown, duplicated, or malformed shape stamp. Do not probe DDL and guess a repair.
10. Do not change model-selection policy. Record which existing source selected each value.
11. Do not claim a historical malformed ACP frame caused a timeout or turn failure.
12. Do not claim the raw Anthropic provider response matched the observed Claude ACP map.
13. Do not claim the deeper operation behind the eezo credential-process timeout.
14. Do not claim the initiating action behind observed adapter exit `:normal`.
15. Do not claim a contentless `-32603` occurred in the inspected incidents.
16. Do not claim formatter commits `81fbc2da` or `91841ad9` caused a live regression.
17. Do not decide any `failed_unknown` external-effect outcome.
18. Do not deploy, mutate a live row, or capture new production traffic under this spec-writing assignment.
19. Do not implement `wait_until`, a wait threshold, or a timer-completion condition in Failure Provenance v1. A later work item may define that behavior and its ordering contract.
20. Do not expose a privileged diagnostic reader in Failure Provenance v1. A later reviewed spec must name the reader surface, authorized principals, access-control and enforcement seam, audit evidence, and redaction contract before any internal diagnostic can leave internal storage.

## Terms

- **Attempt**: one admitted opportunity to execute one turn or command. It has immutable `attemptId` before any effect can start.
- **Replay**: a read of an existing keyed settlement. Replay performs no execution.
- **Retry**: a new admitted attempt linked through `predecessorAttemptId`.
- **Settlement**: the immutable outcome, retry disposition, owner, next action, and deadline committed for an attempt.
- **FailureEnvelope**: the versioned internal typed failure value stored on the row that owns the work.
- **FailurePublicV1**: the sole bounded, redaction-safe projection derived from `FailureEnvelope` for any public reader.
- **Owning row**: `turns` for an accepted prompt; `wire_idempotency` for a keyed wire/process command; or the existing append-only `events` denial row for the reviewed unkeyed `set_harness` path. An ACP pending-origin row names one of these original owners; it never owns an independent envelope.
- **Local/target marker**: the typed message committed in the failed attempt's target stream.
- **Parent route**: the spawned-session lineage route derived from `sessions.spawnedBy`. It is not a terminal owner.
- **Terminal owner**: the session, assignment, user, or process accountable for the settlement's next action.
- **Actionable**: `nextAction != none`.
- **Addressable session**: an exact persisted session row with `state=active`. A missing row or a row with `state=retired` is not addressable. A composed session key without that exact row is not addressable.
- **Delivery**: one durable intent to place `FailurePublicV1` on a parent or terminal-owner surface.
- **Receiver projection**: the single visible message, turn, assignment receipt, or user-owned main-stream marker created by the winning receiver transaction.
- **Receiver supersession tombstone**: the durable same-hash receipt written when an actionable terminal-owner delivery loses the atomic ordering to predecessor-action supersession. It creates no visible projection and makes replay return the same no-projection result.
- **Delivery integrity status**: the bounded owner-readable value `{failureId, deliveryId, surface, state, statusCode?, occurredAt?}` derived from the delivery row. `statusCode` is present only as fixed `failure_delivery_integrity_conflict`; it contains no payload hash or diagnostic.
- **Connection generation**: one persisted `{connectionId=launchId, adapterGeneration}` pair for an ACP process generation.
- **Connection owner send permit**: serialization provided by the exact `Tightbeam.Acp.Conn` process. Guarded admission plus frame write and generation fencing execute in mutually exclusive callbacks.
- **Canonical digest**: lowercase SHA-256 hex of RFC 8785 JSON Canonicalization Scheme bytes for the closed digest document defined below.
- **Bounded origin**: only the safe identifiers in `FailurePublicV1`; it excludes prompt and arbitrary request bodies.
- **Legacy untyped**: a historical row that retains its existing text and receives no fabricated typed envelope.
- **Principal**: the closed tuple `{kind,id}` accountable for a fact. `kind` is `user`, `session`, or `process`; a process principal uses the exact durable subsystem ID such as `process:tightbeam`.
- **Real fixture**: immutable, redacted bytes captured from a reviewed row or actual boundary response, with source identifier and SHA-256 recorded beside the fixture.
- **Fixture manifest**: a separately immutable artifact whose entries name each real fixture's canonical path, SHA-256, and reviewed source identifier. It records fixture custody only; it cannot change a requirement, expected outcome, mapping rule, or test oracle in this spec.
- **OQ-01 closure row**: one durable owner attest on this producer assignment that names the fixture manifest artifact ID, canonical path, SHA-256, and reviewed spec SHA-256. That exact tuple binds the manifest to this work item and exact reviewed spec hash. A different manifest requires a new immutable artifact and owner closure row; it does not overwrite or silently rebind the prior tuple.
- **Fault seam**: a test-only callback that aborts a transaction or crashes a worker at a named point and is unreachable in production configuration.
- **Deadline policy snapshot**: the server-resolved `failure_action_deadline_ms` value, its fixed source `process:tightbeam`, and the checked absolute deadline persisted with one actionable settlement.

## Assumptions

1. `/home/mike/tb-restore` local `origin/main` at `ac8651dcb104f312da1c67e0cb7b1abebc640b2b` is the latest locally available canonical source reference for this seam map. The checked-out `main` at inspection time was `8e2d632481b55ed6991604a275b641b9122ff46b` and 38 commits behind that ref.
2. `Tightbeam.DB` remains the single SQLite writer and `DB.transaction/2` remains the atomic multi-statement seam (`lib/tightbeam/db.ex:1-18`, `54-65`, `125-136` at the mapped ref).
3. Current databases created by the mapped source carry exactly one `schema_stamp` row with `shape=model-identity-v1`; fresh empty databases have no application tables. Migration refuses every other starting state.
4. Existing clients ignore additive JSON response fields they do not understand.
5. Assignment and user rows are durable enough to serve as owner fallbacks. A session may retire after admission.
6. `HarnessProcess.prepare_launch/3` creates `launchId` before OS process launch (`lib/tightbeam/harness_process.ex:99-175`). The adapter coordinator's generation remains monotonic per adapter key (`lib/tightbeam/adapter_coordinator.ex:13-18`, `582-601`).
7. Open Question OQ-01 will provide immutable fixture bytes and a separately immutable fixture manifest before implementation of the affected acceptance cases. Prose in the reviewed report is not a fixture, and fixture custody does not amend this spec.
8. The implementation may add one explicit migration authorized by this reviewed spec. The existing general rule still refuses unknown shapes and does not become an automatic migration framework.

## Architecture

### Authority and preserved evidence boundary

This spec turns the reviewed contract into build instructions. It does not re-adjudicate F1–F7. `art_054cb5af` at its exact SHA and `att_e6a2d6cb` are the intent authority. The current source ref is evidence for file seams, not authority to narrow behavior.

The following statements remain explicitly NOT PROVEN and therefore cannot become code truth:

1. The deeper operation that kept eezo `Credentials` busy beyond five seconds.
2. A malformed ACP frame caused any historical timeout or observed turn failure.
3. The initiating action or cause behind adapter exit `:normal`.
4. Anthropic's raw provider response exactly matched the Claude ACP error map.
5. A contentless `-32603` provider error occurred in the inspected incidents.
6. Formatter commits `81fbc2da` or `91841ad9` were live regression causes.
7. Any underlying cause or external-effect outcome for `failed_unknown`.

Required future proof, outside this implementation, remains respectively: callee/SSH operation telemetry; a captured malformed frame with connection trace; launch/action correlation; provider-side trace; a real contentless specimen; a controlled version toggle outside live work; and external-effect inspection.

The reviewed closures map into this spec without reinterpretation:

| Reviewed closure | Preserved by | Deciding acceptance |
| --- | --- | --- |
| F1 — replay is not retry | I-02, I-03, Idempotency v2 | A05, A15 |
| F2 — atomic settlement, outbox, four-part lease fencing, receiver hash dedupe | I-04–I-07, Atomic settlement, Delivery leasing | A06, A07, A26 |
| F3 — generation-fenced ACP admission, response/close settlement, desynchronization, and recovery | I-08, I-09, ACP connection-generation fencing | A11–A13, A22 |
| F4 — explicit legacy idempotency migration | I-18, Exact migration | A14, A15 |
| F5 — closed outcome/replay/retry/action/owner/deadline matrix | I-10–I-13, Legal settlement matrix | A08, A16, A17, A23 |
| F6 — model and effort selection provenance are independent | I-17, Typed readers and compatibility | A19 |
| F7 — attempt and failure identities are required | I-02, I-20, FailureEnvelope | A20, A25 |

### Resolved owner ruling R-03 — actionable fallback admission

Owner ruling `att_e4482615-3a7f-45a0-93ce-f525d65c2d11` closes former OQ-03. An assignment-primary or user-primary actionable overdue-notification route is enabled only when its admitted `ownerRoute` snapshot contains a distinct valid persisted `fallbackOwner`. The same fail-closed rule applies to a session-primary actionable route.

The route-admission validator returns stable code `missing_fallback_owner` and safe message `actionable failure route requires fallbackOwner` when a new or updated actionable route lacks that field, reuses the primary, names a missing row, or names a kind other than assignment or user. It writes no attempt and starts no effect. It does not promote a user, infer Main, reuse the primary owner, or omit notification from an otherwise enabled route.

If recovery or a deadline worker encounters a legacy persisted action without a valid fallback, it writes or reads one deduplicated lifecycle audit fact with kind `failure_route_dispatch_refused` and subject `failure:<failureId>:actionable-fallback`. `routeRef` is the deterministic string `owner-route:<owningRowKind>:<owningRowId>`. The fixed typed detail is `{routeRef, primaryOwner, missingField="fallbackOwner", safeCauseCode, refusalCode="missing_fallback_owner"}`, and its principal is `process:tightbeam`. A partial unique index on `(kind, subject)` for that kind provides dedupe. The transaction sends no notification, creates no fallback delivery, changes no owner, and leaves the legacy action in its prior state. Recovery and the deadline worker exclude a route after its audit fact exists, so they do not busy-loop.

This spec adds no mutable route registry. An authorized route update changes existing assignment/user ownership data or supplies explicit fallback input before a future admission; `admit_attempt_in_txn` snapshots the resulting route. The update affects only attempts admitted afterward. It does not amend a committed envelope, action, owner, or delivery and does not dispatch a retrospective notification.

### Resolved owner ruling R-04 — Failure Provenance v1 has no `wait_until`

Owner ruling `att_5ef575f8-b700-4b53-a6a5-e1a79e779ca9` closes former OQ-04 by excluding `wait_until` from Failure Provenance v1. The v1 `nextAction` enum and legal settlement matrix contain no timer-only condition. The parser, constructor, and migration validator reject any v1 input that names `wait_until` before persistence with stable code `unsupported_failure_action` and safe message `wait_until is not supported by failure provenance v1`. Rejection creates no attempt, envelope, action, delivery, or effect. A later work item may add a new version with its own threshold source, ordering, and tie contract.

### Resolved owner ruling R-05 — one immutable server deadline policy

The same owner ruling closes former OQ-05. Application config `failure_action_deadline_ms` defaults to `86400000` when absent. When present, it must be an integer from `1` through `2592000000`, inclusive. The application validates the resolved value before schema mutation, runtime children, or traffic; an invalid value fails boot.

Every actionable settlement for a turn, keyed wire/process attempt, reviewed unkeyed `set_harness` denial, or ACP-inherited origin uses the same resolved server policy snapshot. The settlement constructor captures `terminalAt` once before its transaction, checked-adds the resolved duration, and persists `actionDeadline`, `deadlinePolicyMs`, and `deadlineSource=process:tightbeam` on the immutable envelope and action. An origin caller cannot supply or amend those fields. A config change affects only settlements whose `terminalAt` is captured after the change; it does not reinterpret a committed deadline.

Action completion requires both `completedAt < actionDeadline` and the completing worker's captured `now < actionDeadline`. At `completedAt == actionDeadline`, or when worker `now >= actionDeadline`, the `pending -> overdue` action compare-and-set wins instead. That transaction inserts or reuses one fallback-owner delivery and executes no work. Boot recovery compares its captured `bootNow` with each stored absolute UTC epoch-millisecond deadline; it never recalculates a committed deadline from current config.

### Current source ownership and required seams

| Owner | Current canonical evidence at `ac8651d` | Required seam |
| --- | --- | --- |
| `Tightbeam.DB` | Single writer and `BEGIN IMMEDIATE` transaction owner in `lib/tightbeam/db.ex:1-18,54-65,125-136` | Remains the only database mutation topology. Failure code uses `*_in_txn` functions and never re-enters DB from a transaction. |
| `Tightbeam.Schema` | Shape stamp and general unknown-shape refusal in `lib/tightbeam/schema.ex:35-38,711-753,893-980` | Own one exact `model-identity-v1 -> failure-provenance-v1` migration. Refuse every other stamped or malformed starting state. Register failure schema before runtime children or traffic. |
| New `Tightbeam.Failures` in `lib/tightbeam/failures.ex` | No current module | Sole failure-state mutation seam and one concept home: nested typed values, closed validators and cause mapper, owning-row failure settlement, action/delivery CAS, receiver dedupe, owner-authorized delivery-status read, migration helpers, recovery queries, and public projection. Existing owner modules may admit attempts and settle successes; they delegate every failure-field and companion-table write to this seam. |
| New `Tightbeam.FailureDeliveryWorker` | No current module | Claims committed delivery rows, invokes the destination-specific receiver, then acknowledges or fenced-reschedules through `Tightbeam.Failures`. It never executes failed work. |
| New `Tightbeam.FailureDeadlineWorker` | No current module | Applies action deadline CAS and boot reconciliation through `Tightbeam.Failures`. It alerts fallback owners and never creates a new attempt. |
| `Tightbeam.Ledger` | Turn schema and terminal CAS in `lib/tightbeam/ledger.ex:39-76,363-391`; boot recovery in `421-449` | Add typed owner columns. Delegate failed and failed-unknown terminal mutation to `Tightbeam.Failures.settle_turn_in_txn/…`. Keep successful delivery and cancellation semantics outside the failure contract. Replace running-turn recovery with typed atomic recovery. |
| `Tightbeam.SessionLane` | Task crash collapse and split finalization in `lib/tightbeam/session_lane.ex:172-194,249-305` | Carry the captured structured failure into the settlement constructor. For failure outcomes, open one transaction and call the sole failure mutation seam. Publish committed markers after commit. Do not append failure facts in a later closure. |
| `Tightbeam.CommandEdge.TerminalPublication` | Complete turn context but untyped `error` in `lib/tightbeam/command_edge.ex:96-127,343-355` | Add an optional validated `FailurePublicV1` plus committed marker identity for failed terminal publications. Construction fails for a failure missing required IDs or a public field outside the allowlist. Delivered and canceled publications retain their current success shape and `error=nil`. |
| `Tightbeam.Gateway` | Post-commit terminal publisher appends failure markers later in `lib/tightbeam/gateway.ex:2075-2103`; map flattening in `4749-4763,5502-5528`; tune resolution in `1600-1679,4001-4078` | Remove late marker creation for typed failures. Map observed failure shapes at the command edge before settlement. Publish the committed typed marker. Return typed settlement fields on wire. Refactor tune resolution to return the resolved model plus independent selection provenance in the same operation. The unkeyed `set_harness` denial transaction stores its envelope on the existing denial event. |
| `Tightbeam.EventLog` | Append-only `events` and `lifecycle_events` tables plus in-transaction append seams in `lib/tightbeam/event_log.ex:1-23,66-102,122-166` | Add nullable typed failure columns to the existing denial row and one typed denial constructor. For the reviewed unkeyed `set_harness` path, that event is the owning row; no parallel unkeyed command ledger is created. Own the deduplicated legacy missing-fallback and delivery-integrity lifecycle facts and their partial unique indexes. Other verb/denied and lifecycle events retain their current shape. |
| `Tightbeam.Projection` | Message schema and append mutation in `lib/tightbeam/projection.ex:54-81,100-164`; marker helper in `166-183` | Add typed marker columns and an explicit-ID `append_failure_marker_in_txn`. The deterministic marker ID and `messages.id` uniqueness are the local/target dedupe seam. |
| `Tightbeam.Transcript` | Reader joins assistant rows only by `replyToMessageId` and omits failure fields in `lib/tightbeam/transcript.ex:184-240` | Select and project typed failure columns. A typed marker joins by stored IDs. The reader never reparses content or legacy maps. |
| `Tightbeam.Productions.Bubble` | Reads `turns.error` and interpolates it into parent/user prose in `lib/tightbeam/productions/bubble.ex:134-155,169-223,319-329` | Typed failures bypass legacy Bubble climbing and use the delivery outbox. Legacy rows use a fixed safe `legacy_untyped` projection; raw `turns.error` no longer enters public parent or user text. Parent route remains independent from terminal ownership. |
| `Tightbeam.Idempotency` | Legacy table and read/write seam in `lib/tightbeam/idempotency.ex:21-29,34-107` | Own v2 admission, canonical digest checks, replay reads, typed conflict, success settlement, and migration. It delegates failure settlement inside its existing transaction to `Tightbeam.Failures.settle_command_in_txn`. Replace direct `wire_idempotency` SQL in `Assignments` and `WorkItems` with this module's transaction API. |
| `Tightbeam.Wire.Router` and Rust CLI | Current router accepts keys but no digest; CLI constructs JSON in `lib/tightbeam/wire/router.ex` and `cli/src/dispatch.rs` | Accept optional `requestDigest`. Compute and verify the canonical digest server-side. Add typed failure fields without changing existing status semantics. CLI prints structured non-empty JSON and never turns an empty response into outcome evidence. |
| `Tightbeam.Acp.Conn` | Request writes frame before durable admission and silently drops decode errors in `lib/tightbeam/acp/conn.ex:91-116,133-180,195-219,246-250` | Persist generation before admission. Use the Conn process as the send permit. Admit the durable origin, commit, then write the frame in one callback. Settle a response and its origin together before replying. On clean close or decode error, fence and settle the complete admitted generation set before starting a successor. |
| `Tightbeam.Acp.Adapter` | Launch identity is available during boot in `lib/tightbeam/acp/adapter.ex:326-390`; exit and bounded stderr seams in `956-975,1558-1594` | Retain `launchId` and adapter generation in state, pass both into Conn, attach `launchId` to execution provenance, and keep `:normal` or `:noproc` cause class-only. |
| `Tightbeam.AdapterCoordinator` and `Tightbeam.HarnessProcess` | Coordinator computes generation during start in `lib/tightbeam/adapter_coordinator.ex:660-729`; launch ledger owns `launchId` in `lib/tightbeam/harness_process.ex:18-43,99-175` | Compute the generation before the lazy boot closure and pass it with the prepared launch ID. A successor generation is strictly greater. Do not create a second launch registry. |
| `Tightbeam.Application` / gateway child tree | Gateway runs schema before children and traffic in `lib/tightbeam/gateway.ex:145-180,279-325` | Validate `failure_action_deadline_ms` before schema mutation. Run migration and deterministic failure recovery after schema ownership is established and before Wakes, lanes, delivery/deadline workers, adapters, or Bandit accept work. Start the two workers only after recovery. |

### FailureEnvelope

`Tightbeam.Failures.Envelope` is a closed validated value with these fields. `?` means the field may be absent only under the stated condition.

```text
schemaVersion = 1
failureId
attemptId
correlationId
predecessorAttemptId?
origin: {
  sessionKey?, messageId?, turnSeq?, assignmentId?, workItemId?,
  processOrigin, requestRef?, idempotencyScope?
}
connectionFaultRef?: {connectionId, adapterGeneration, eventId}
noEffectEvidence?: {kind, evidenceRef, assertedBy, observedAt, validUntil?}
ownerRoute: {primary, fallback?, selected, selectionReason}
reportedAtLayer
upstreamClaim?: {layer, code}
safeCause: {code, message}
protocol: {jsonRpcCode?, providerCode?, providerErrorKind?}
execution: {
  model?, harness?, adapterKey?, adapterGeneration?, launchId?, exitStatus?,
  selection?: {
    destinationHarness,
    model: {requested?, resolved?, source},
    effort: {requested?, resolved?, source}
  }
}
causeSpecificity: concrete | class_only | unknown
provenanceLinkage: linked | partial | absent
outcome: known_no_effect | known_committed | unknown
replayPolicy: return_same_settlement | no_replay_key
retryDisposition: forbidden | new_attempt_now | new_attempt_after_condition |
                  verify_then_new_attempt | user_decision
terminalOwner: {kind: session | assignment | user | process, id}
nextAction: none | submit_new_attempt | inspect_effect | reauthenticate |
            choose_model | inspect_adapter | operator_investigation
actionDeadline?
deadlinePolicyMs?
deadlineSource?: process:tightbeam
diagnostic: {class, redactedSummary?, sampleHash?, capturedBytes?}
observedAt
terminalAt
```

Field rules:

1. `attemptId` is `atm_` plus a lowercase RFC 4122 version-4 UUID generated at admission. `failureId` is the deterministic string `fail_` plus the UUID portion of `attemptId`. Unique constraints reject a collision. A successful attempt has `attemptId` and no `FailureEnvelope`.
2. `correlationId` is the admitted client message ID when it matches `^[A-Za-z0-9][A-Za-z0-9:_-]{0,255}$`, else the admitted request reference when it matches that allowlist, else `attemptId`. An unsafe internal identifier stays only in the internal origin. Settlement does not recompute correlation.
3. `predecessorAttemptId` appears only on a new attempt created as an explicit retry.
4. `processOrigin` is required and names the submitted session, user, or process identity. Optional origin fields appear only when their row exists at admission.
5. `idempotencyScope`, when present, is `{principal:{kind,id}, operation, key, digestVersion}`. The principal tuple exactly matches the owning `wire_idempotency` row. The public projection does not expose the raw key.
6. `connectionFaultRef` is required for `safeCause.code=acp_protocol_desync` and for a generation-wide clean-close settlement with `safeCause.code=adapter_unavailable`. It is absent for request-specific claims not supported by evidence.
7. `noEffectEvidence.kind` uses only `declared_read_only`, `pre_mutation_refusal`, or `verified_external_state`. `evidenceRef` names a durable row. `assertedBy` names its accountable session, user, or subsystem. `validUntil`, when present, must be at or after `terminalAt`.
8. `ownerRoute.primary`, `fallback`, and `selected` use the same `{kind,id}` owner shape as `terminalOwner`. `selectionReason` is one of `primary_available`, `primary_unavailable`, or `no_action`.
9. `reportedAtLayer` is one of `wire`, `gateway`, `ledger`, `session_lane`, `acp`, `adapter`, `harness`, `provider_adapter`, `credential_process`, or `local_task`.
10. `upstreamClaim.layer` uses the same closed enum as `reportedAtLayer`. Its `.code` is `usageLimitExceeded` or `rate_limit`, and appears only when the observed structured payload contains that exact allowlisted assertion. The other mapping rows do not create an upstream claim. Absence stays absent.
11. `protocol.jsonRpcCode` is an integer. `protocol.providerCode` is exactly `usageLimitExceeded`. `protocol.providerErrorKind` is exactly `rate_limit`. No protocol field accepts an arbitrary string. Adapter exits stay in `execution.exitStatus`; they are not provider protocol.
12. For tune attempts, `selection.model.source` and `selection.effort.source` are independently required and each is one of `explicit_request`, `session_current`, `boot_wide_default`, `destination_harness_default`, `selected_model_default`, or `catalog_fallback`. `requested` preserves the submitted value or null. `resolved` preserves the validated value or null. `destinationHarness` is required.
13. `diagnostic.redactedSummary` is UTF-8 and at most 4,096 bytes. `sampleHash` is lowercase SHA-256 hex of the complete observed boundary bytes and `capturedBytes` is their nonnegative original byte count. The complete encoded `diagnostic` is at most 8,192 bytes. The command edge derives the redacted summary and hash before discarding unbounded raw input. Unclassified boundary failures retain these bounded internal diagnostics instead of inventing a cause. The fields are structurally unavailable to `FailurePublicV1` and public trace.
14. The complete RFC 8785 encoded `FailureEnvelope` is at most 32,768 bytes. The constructor rejects a larger value before persistence; it does not truncate typed identity or settlement fields.
15. A public `origin.requestRef` is present only when it matches `^[A-Za-z0-9][A-Za-z0-9:_-]{0,255}$`; an internal request reference outside that allowlist remains internal. This check does not alter the immutable internal origin.
16. `observedAt` and `terminalAt` are persisted UTC epoch milliseconds. `terminalAt >= observedAt`.
17. An actionable envelope requires `actionDeadline`, `deadlinePolicyMs`, and `deadlineSource=process:tightbeam`. `deadlinePolicyMs` is the validated server snapshot. `actionDeadline` is the checked integer sum `terminalAt + deadlinePolicyMs`. A non-actionable envelope requires all three fields to be absent.

### FailurePublicV1

`Tightbeam.Failures.PublicV1` contains exactly:

```text
failureId
attemptId
correlationId
origin                 # bounded origin only
safeCause
causeSpecificity
provenanceLinkage
reportedAtLayer
protocol               # redaction-safe subset
upstreamClaim?         # redaction-safe and observed
connectionFaultRef?
outcome
retryDisposition
terminalOwner          # selected terminal owner
nextAction
actionDeadline?
deliveryId?            # required for asynchronous delivery
```

The bounded public origin permits `sessionKey`, `messageId`, `turnSeq`, `assignmentId`, `workItemId`, `processOrigin`, and `requestRef` only. It excludes `idempotencyScope`, prompt, request body, model selection input, diagnostic detail, and raw upstream material.

`publicPayloadHash` is the lowercase SHA-256 hex of RFC 8785 canonical bytes for `FailurePublicV1` including `deliveryId` and excluding the hash itself. `payloadVersion=1` selects the frozen `FailurePublicV1` serializer used to create that hash. A later projector change uses a new payload version; it does not reinterpret a committed v1 delivery. The worker reconstructs the versioned payload from the immutable envelope and delivery row and refuses to send if its hash differs from the committed hash.

### Legal settlement matrix

| Outcome | Replay policy | Retry disposition | Next action | Legal owner and deadline |
| --- | --- | --- | --- | --- |
| `known_no_effect` | `return_same_settlement` for v2 keyed; otherwise `no_replay_key` | `forbidden` | `none` | Session, assignment, user, or process; no deadline |
| `known_no_effect` | `return_same_settlement` for v2 keyed; otherwise `no_replay_key` | `new_attempt_now` | `submit_new_attempt` | Session, assignment, or user; deadline required; valid `noEffectEvidence` required |
| `known_no_effect` | `return_same_settlement` for v2 keyed; otherwise `no_replay_key` | `new_attempt_after_condition` | `reauthenticate`, `choose_model`, or `inspect_adapter` | Session, assignment, or user; `conditionRef` and deadline required |
| `known_no_effect` | `return_same_settlement` for v2 keyed; otherwise `no_replay_key` | `user_decision` | `operator_investigation` | Assignment or user; deadline required |
| `known_committed` | `return_same_settlement` for v2 keyed; otherwise `no_replay_key` | `forbidden` | `none` | Session, assignment, user, or process; no deadline; re-execution illegal |
| `unknown` | `return_same_settlement` for v2 keyed; otherwise `no_replay_key` | `verify_then_new_attempt` | `inspect_effect` | Session, assignment, or user; deadline required; process owner forbidden |

`nextAction` is the typed condition class for `new_attempt_after_condition`. That disposition requires `failure_action.conditionRef` to name a durable condition or verification row. Every other disposition requires `conditionRef=null`. Only a durable condition, verification, or user-authored decision result of the type required by the disposition may complete the action. Completion does not submit work. R-04 defines the fail-closed rejection for the excluded `wait_until` input.

Each actionable tuple also requires the valid persisted fallback defined by R-03. This rail does not change the six settlement families; it rejects an unrouteable tuple before admission.

### Owner routing

1. Admission persists `ownerRoute.primary` and optional `ownerRoute.fallback` before execution can begin. The envelope adds final `selected` and `selectionReason` at settlement; it does not recalculate the candidate routes.
   - An accepted turn uses its exact target session as primary. It selects its linked assignment as fallback when one exists; otherwise it selects its owning user.
   - A wire/process command that addresses an existing session uses that target session as primary and the caller's assignment or user as fallback. A command without a target session uses its accountable caller session or user as primary and requires a distinct explicit assignment or user fallback. A process caller may start an effectful in-scope attempt only when the request supplies a durable assignment or user primary plus a distinct assignment or user fallback; otherwise admission rejects before effect.
   - The reviewed unkeyed `set_harness` denial uses its target session as primary and its accountable HTTP caller user as fallback; the caller also receives the synchronous wire settlement.
   - An ACP pending origin inherits the primary and fallback stored on its original owning attempt.
2. Each actionable attempt, regardless of primary kind, requires a distinct persisted fallback of kind assignment or user whose exact row exists at admission. The validator applies R-03 and refuses before effect with `missing_fallback_owner` when the fallback is absent or invalid.
3. At settlement, an exact active primary session wins with `selectionReason=primary_available`. A missing or retired primary session selects the persisted fallback with `selectionReason=primary_unavailable`. A validated assignment or user primary selects itself with `selectionReason=primary_available`. A process primary is legal only for `nextAction=none` and selects itself with `selectionReason=no_action`.
4. If the origin has an assignment, admission selects that assignment as fallback; otherwise it selects the owning user. A spawned parent is not an owner fallback.
5. Parent routing reads `spawnedBy`. No parent or an unavailable parent commits a parent delivery with `state=not_applicable` and a closed reason. The terminal-owner delivery is still created.
6. Destination handling is closed:
   - `session`: receiver transaction writes a typed process-origin prompt/turn with `deliveryId` as its wake/client idempotency key.
   - `assignment`: receiver transaction writes an assignment-linked receipt, then wakes the current holder from the durable row. A changed holder reads the same receipt.
   - `user`: receiver transaction resolves an existing main stream owned by that exact user and writes its marker and receiver receipt together; wire push is post-commit presentation. If no owned main stream exists, it creates no receipt and returns destination unavailable so the fenced delivery remains recoverable.
   - `process`: legal only with `nextAction=none`; terminal-owner delivery is `not_applicable` with reason `no_human_action`.
7. A missing user main stream is not receipt. Send-failure reschedule retains the terminal-owner intent until an owned stream exists; a later retry then uses the same `deliveryId`. The implementation does not compose a session key or acknowledge invisible delivery.

### Durable schema and one mutation seam

The exact target stamp is `failure-provenance-v1`.

`turns` gains nullable legacy-compatible columns `attemptId`, `correlationId`, `predecessorAttemptId`, `failureId`, `failureEnvelope`, and `failureSchemaState`. New admitted turns require `attemptId` and `correlationId`. `predecessorAttemptId` is null for an original attempt. An explicit accepted retry stores the prior owning row's `attemptId`; that predecessor exists, is terminal, belongs to the same logical origin, and remains unchanged. A new `failed` or `failed_unknown` row requires `failureSchemaState=typed_v1`, non-null `failureId`, and a validated envelope whose attempt, predecessor, correlation, and owner link match the admitted `turns.seq`. Historical terminal failures use `failureSchemaState=legacy_untyped` with null typed IDs and envelope.

`messages` gains nullable `failureId`, `attemptId`, `deliveryId`, and `failureSurface`. `failureSurface` is `local_target`, `parent_notice`, or `terminal_owner_alert`. A typed failure marker requires all applicable IDs. A turn-origin marker requires `replyToMessageId=origin.messageId`. A command denial with no admitted message requires `replyToMessageId=null`; its stored `attemptId` and `failureId` join to the owning envelope and correlation. Its ID is `failure:<failureId>:<surface>` for the local/target surface. `messages.id` uniqueness remains the marker dedupe rail.

`wire_idempotency` v2 contains:

```text
principalKind: user | session | process
principalId
operation
idempotencyKey
schemaVersion
state: legacy_succeeded | in_progress | succeeded | failed
sessionKey?
target?
action?
requestDigest?
digestVersion?
attemptId?
correlationId?
predecessorAttemptId?
failureId?
failureEnvelope?
settlementJson?
createdAt
settledAt?
```

The primary key is `(principalKind, principalId, operation, idempotencyKey)`. Only `legacy_succeeded` may have null digest, attempt, and correlation. Each v2 row requires them. A user, session, and process using the same operation and key occupy different namespaces; two different IDs of the same kind also occupy different namespaces. `predecessorAttemptId` follows the same original-versus-explicit-retry rule as `turns` and is immutable for success and failure. A success has no `failureId` or envelope. A failure has both and passes the same validator.

`events` gains nullable `attemptId`, `correlationId`, `predecessorAttemptId`, `failureId`, `failureEnvelope`, and `failureSchemaState`. Each new in-scope unkeyed tune attempt writes its attempt and correlation identity on the existing event owner whether it succeeds or fails. The reviewed unkeyed `set_harness` denial uses `failureSchemaState=typed_v1`, the exact action and submitted fields in its bounded payload, and a validated envelope whose origin links the target session and event request reference. Other historical events leave these columns null. An unkeyed repeat creates a new event and new `attemptId` with `replayPolicy=no_replay_key`; an explicit linked repeat also records the terminal prior event's `attemptId` in `predecessorAttemptId`. This reuses the current event owner and creates no parallel unkeyed command ledger.

`lifecycle_events` gains nullable `principal`. Historical rows preserve null. Each lifecycle fact written by this mechanism requires a principal. The schema adds partial unique indexes on `(kind, subject)` for `failure_route_dispatch_refused` and `failure_delivery_integrity_conflict` so each refusal or conflict subject has one fact.

`failure_action` contains:

```text
actionId = failure:<failureId>:action
failureId                              # primary/foreign identity
selectedOwnerKind, selectedOwnerId
fallbackOwnerKind?, fallbackOwnerId?
routeSchemaState: typed_v1 | legacy_missing_fallback
nextAction
conditionRef?
completionRef?
deadline
deadlinePolicyMs
deadlineSource = process:tightbeam
state: pending | completed | overdue | superseded
principal
completedAt?
overdueAt?
supersededAt?
supersededByAttemptId?
```

`failure_delivery` contains:

```text
deliveryId = hash(failureId, surface, destinationKind, destinationId)
failureId, attemptId
surface: parent_notice | terminal_owner_alert
destinationKind, destinationId
payloadVersion = 1
publicPayloadHash
state: pending | leased | delivered | not_applicable | overdue | superseded | integrity_conflict
leaseOwner?
leaseEpoch
leaseToken?
leaseUntil?
attemptCount
nextAttemptAt?
actionId?
deliveredAt?
notApplicableReason?
principal
supersededAt?
supersededByAttemptId?
integrityConflictAt?
integrityConflictFactId?
```

Terminal `integrity_conflict` requires both integrity fields, retains `leaseEpoch` and `attemptCount` as fence history, and requires `leaseOwner`, `leaseToken`, `leaseUntil`, and `nextAttemptAt` to be null. `actionId` is required only for an actionable `terminal_owner_alert` and references the associated `failure_action`. Every other delivery has `actionId=null`.

The unique key is `(failureId, surface, destinationKind, destinationId)`. Parentless uses destination `none:none`. `deliveryId` is `fd_` plus lowercase SHA-256 hex of RFC 8785 canonical bytes for the four-element JSON array `[failureId, surface, destinationKind, destinationId]`. `notApplicableReason`, when present, is one of `parentless`, `parent_unavailable`, `no_human_action`, `destination_retired`, or `destination_missing`.

`received_failure_deliveries` contains `deliveryId` primary key, `publicPayloadHash`, destination kind/id, `receiptKind=projected|superseded_tombstone`, nullable projection kind/id, `receivedAt`, and principal. A projected receipt requires both projection fields. A supersession tombstone requires both projection fields null. It is written in the same transaction as the visible destination-native receiver projection or the atomic no-projection decision.

`acp_connection_generations` contains `{connectionId, adapterGeneration}` unique, `adapterKey`, monotonically increasing `rowVersion`, state `open|desynced|closed`, `createdAt`, and terminal timestamps. `connectionId` equals `HarnessProcess.launchId`.

`acp_connection_events` contains deterministic `eventId`: `acp-desync:<connectionId>:<adapterGeneration>` for kind `desync` or `acp-close:<connectionId>:<adapterGeneration>` for kind `clean_close`. A desync event contains bounded byte count and optional sample hash. A clean-close event contains neither. Both contain observed time and principal. Uniqueness is `(connectionId, adapterGeneration, eventKind)`.

`acp_pending_origins` contains connection identity, `attemptId`, original owning-row kind/id, ACP method class, declared-read-only boolean, state `admitted|settled`, admitted time, nullable `settledAt`, nullable `settlementKind=response|clean_close|desync`, and settlement `failureId` when failed. An admitted row has all settlement fields null. A settled row requires `settledAt` and `settlementKind`; `failureId` is null for a successful response and required for a failed response, clean close, or desynchronization. It is a generation-membership and recovery row, not an envelope owner. Each settlement changes this row and the referenced original owning row in one transaction. A generation-wide settlement records the same `failureId` here and does not claim that an undecodable frame or clean close belonged to one request.

`Tightbeam.Failures` exposes the sole public domain-mutation API for these records:

- `admit_attempt_in_txn`
- `settle_turn_in_txn`
- `settle_command_in_txn`
- `settle_unkeyed_set_harness_denial_in_txn`
- `admit_acp_origin_in_txn`
- `settle_acp_origin_in_txn`
- `close_acp_generation_in_txn`
- `desync_generation_in_txn`
- `claim_delivery_in_txn`
- `ack_delivery_in_txn`
- `reschedule_delivery_in_txn`
- `mark_delivery_integrity_conflict_in_txn`
- `receive_delivery_in_txn`
- `complete_action_in_txn`
- `expire_action_in_txn`
- `recover_in_txn`

`read_delivery_status(deliveryId, requestingPrincipal)` is the non-mutating owner-status seam. It returns the bounded `Delivery integrity status` only when the existing owning-row authorization admits the requester or the requester exactly equals the envelope's selected terminal owner; otherwise it returns `not_found`. It never returns either hash, lease identity, or diagnostic.

Inside an existing transaction, the mutation API may call the exact owner helpers `Ledger` terminal CAS, `Projection.append_failure_marker_in_txn`, and `EventLog.append_failure_denial_in_txn`; no caller invokes those failure-specific helpers directly. Other modules may read through the typed read functions. Source-structure tests fail when another module writes companion tables or typed failure columns outside this closed call graph.

### Atomic settlement sequence

For a turn failure, `settle_turn_in_txn` executes in this order inside one `DB.transaction`:

1. validate the envelope and legal matrix;
2. compare the immutable admitted `attemptId`, `correlationId`, and `predecessorAttemptId`, then win `running -> failed|failed_unknown` for the owning `turns.seq` while writing `failureId`, envelope, schema state, end time, and bounded legacy error;
3. append the typed lifecycle fact with cause and principal;
4. insert-or-read the deterministic local/target marker with typed message columns and the origin-specific `replyToMessageId` rule above;
5. insert `failure_action` when `nextAction != none`;
6. insert-or-read the parent delivery, including typed `not_applicable`;
7. insert-or-read the terminal-owner delivery, including process-owned `not_applicable`;
8. validate that exactly one owning row and the required companion set now exist;
9. commit.

The check and action are one indivisible step. Any error raises, rolls back, and leaves the turn running for deterministic recovery. A lost terminal compare-and-set returns `already_terminal` and inserts nothing.

A keyed command denial uses the same sequence on its `wire_idempotency` owning row. The reviewed unkeyed `set_harness` denial uses the same sequence on its `events` denial row. Wire response occurs only after commit. HTTP write success is not a delivery settlement.

### Delivery leasing and receiver transaction

1. A new delivery starts with `leaseEpoch=0` and `nextAttemptAt=null`. A claimant captures one `claimNow`. Claim changes `pending` only when `nextAttemptAt IS NULL OR nextAttemptAt<=claimNow`, or changes an expired `leased` whose `leaseUntil<=claimNow`, to `leased`; increments `leaseEpoch`; writes a new 128-bit random `leaseToken` encoded as 32 lowercase hexadecimal characters, exact worker `leaseOwner`, and `leaseUntil`; and increments no send count yet. The eligibility predicate and state change are one compare-and-set. Equality is eligible.
2. The production lease duration is configuration `failure_delivery_lease_ms`, default 30,000 ms. This number bounds waiting for an unobservable crashed worker; it does not decide a delivery outcome.
3. The worker reconstructs only the committed `payloadVersion` of `FailurePublicV1` with `deliveryId`. If the reconstructed hash differs from the delivery row, the worker does not call a receiver. It runs `mark_delivery_integrity_conflict_in_txn` with its four-part lease fence. Otherwise it calls the receiver transaction with the public payload and its lease fence as internal call context; the fence is not serialized into `FailurePublicV1`. Post-commit wire publication is replayable presentation, not receipt truth.
4. Receiver first verifies the four-part fence and `state=leased`, then insert-or-reads `received_failure_deliveries` in the same transaction. For an actionable terminal-owner alert, it reads the referenced `failure_action` before projection. If the action is `superseded`, it writes or reads a same-hash `superseded_tombstone`, creates no projection, and returns the successor attempt ID. If the action is not superseded, a winning insert creates the destination-native projection in the same transaction. Same hash returns its stored projection or tombstone. Different hash returns the typed integrity failure, insert-or-reads one deterministic lifecycle fact `kind=failure_delivery_integrity_conflict, subject=<deliveryId>` with failure ID, delivery ID, observed boundary `receiver`, observed time, and accountable receiver principal, and changes the currently fenced delivery `leased -> integrity_conflict` with the integrity fields. It creates no projection. A stale fence changes no row and writes no fact.
5. Acknowledgement runs `leased -> delivered WHERE deliveryId, leaseEpoch, leaseToken, leaseOwner, state=leased`. Zero changed rows means stale.
6. A supersession-tombstone result runs `leased -> superseded` with the same four-part fence and the returned successor attempt ID. A crash before that sender transition leaves the receiver tombstone durable; a later claimant reads the same tombstone and can finish the fenced transition without a projection.
7. A worker-local mismatch uses `mark_delivery_integrity_conflict_in_txn`; a receiver mismatch performs the same state and fact writes inside `receive_delivery_in_txn`. Both change `leased -> integrity_conflict`, clear the lease fields, set `integrityConflictAt` and the deterministic fact ID, and insert-or-read the same lifecycle fact shape with boundary `worker` or `receiver`. Each mutation loses on a stale fence. `integrity_conflict` is terminal and excluded from claim, recovery, reschedule, and send queries. The owning row reader and selected terminal owner may read its bounded `Delivery integrity status`; no public reader receives either hash or diagnostics.
8. Send failure runs `leased -> pending` with the same fence. That mutation increments `attemptCount`, clears lease fields, and sets `nextAttemptAt` from a deterministic backoff of 1, 2, 4, 8, 16, 32, then 60 seconds capped. Zero changed rows means stale.
9. A delivery retry repeats notification only. It does not mutate the envelope, action, settlement, or attempt identity.
10. Terminal-owner delivery becomes `overdue` only with the associated action's won `pending -> overdue` CAS. A parent delivery to a destination that no longer exists becomes `not_applicable` with `destination_retired` or `destination_missing`; it is not rerouted to the terminal owner.
11. An expired `leased` row remains leased until a claimant wins the next claim compare-and-set. That claim increments the epoch and replaces the token. Recovery does not reset lease state in a separate write.

### Failure actions and deadlines

`failure_action` exists only for actionable settlements. Every new row has `routeSchemaState=typed_v1`, non-null R-03-valid fallback columns, and the R-05 deadline snapshot copied from its immutable envelope. The action mutation API does not accept replacement deadline fields. A database immutability trigger rejects an update that changes `deadline`, `deadlinePolicyMs`, or `deadlineSource`. A pending action has null `completionRef` and `completedAt`. A completed action has both; `completionRef` names the durable condition, verification, or user-authored decision fact that won the completion compare-and-set.

The exact `model-identity-v1` source has no `failure_action` table, so its migration creates zero `legacy_missing_fallback` rows. Production constructors cannot create that state. A23 seeds it only through the copied-database migration fixture helper, outside the domain API, to verify the defensive legacy read required by R-03. That fixture does not claim a current production row exists.

The live worker captures one `now`. `complete_action_in_txn` changes `pending -> completed` only when the durable result has `completedAt < deadline` and captured `now < deadline`. Otherwise `expire_action_in_txn` changes `pending -> overdue` and insert-or-reads the deterministic fallback-owner delivery in the same transaction. At equality, overdue wins. A lost compare-and-set means another worker or recovery pass settled the action. The worker does not edit the envelope or submit work.

Boot captures one `bootNow`. It selects typed rows with `state=pending AND deadline<=bootNow` and separately selects legacy `routeSchemaState=legacy_missing_fallback` rows whose stored deadline is at or before `bootNow` and whose deduplicated R-03 audit fact does not exist. It compares stored absolute deadlines and does not read current deadline policy for either query. A typed winner gets one overdue transition and one fallback delivery. A legacy row follows R-03 audit semantics and retains its prior state; once its audit fact exists, later boot and live-worker queries exclude it. An expired action is not reset to pending, given a new failure ID, or executed. Later execution is a separately admitted attempt.

An explicit linked-attempt admission validates the predecessor disposition in the same transaction. `forbidden` rejects the link. `new_attempt_now` requires the selected owner and no-effect evidence that remains unexpired at new admission; its pending action then becomes `superseded`. `new_attempt_after_condition` requires a completed action whose `completionRef` names the required satisfied condition. `verify_then_new_attempt` requires a completed action whose verification result says `known_no_effect`; `known_committed` or `unknown` rejects admission. `user_decision` requires a completed action whose durable assignment- or user-authored decision says `submit_new_attempt`. These checks admit a new `attemptId`; none executes the predecessor attempt.

When a valid linked admission supersedes a pending predecessor action, that transaction records `supersededByAttemptId`. It also changes an unclaimed `pending` terminal-owner delivery for that predecessor to `superseded`. A leased delivery remains leased because another worker owns its four-part fence, but its receiver transaction must test the referenced action state before projection. SQLite writer ordering decides the race: a receiver transaction that commits its visible projection first may be followed by supersession; a successor transaction that commits first forces the later receiver to write or read the no-projection tombstone and causes the lease owner to finish `leased -> superseded`. The transaction does not supersede a delivered receipt, a parent notice, or the predecessor envelope. A condition-, verification-, or decision-completed predecessor action remains `completed`. No background worker creates action transitions.

### ACP connection-generation fencing

1. `AdapterCoordinator` computes the positive generation before it creates the lazy boot closure and passes it to `Acp.Adapter`.
2. `HarnessProcess.prepare_launch` supplies `launchId`. `Acp.Adapter` persists both in its state and passes them, the adapter key, and DB handle to `Acp.Conn`.
3. Conn inserts the generation row before it admits an origin. Existing exact same `{connectionId,generation}` is a read; any disagreement is dirt and closes the port.
4. Conn's GenServer callback is the send permit. For an origin-bearing request, it validates the generation's `open` state and row version, inserts the durable pending origin, commits, writes the frame, then updates in-memory pending state before returning from the callback.
5. On a valid response, Conn remains the serialization owner while the response edge settles the original owning row. In that same transaction `settle_acp_origin_in_txn` changes the exact origin `admitted -> settled`, records `settlementKind=response`, and records the owning failure ID only when the response settles as failure. The response is delivered to its caller only after commit. A duplicate response reads the settled origin and returns the stored owning result; it writes no row and creates no second caller result.
6. On a clean port close, Conn fences in memory immediately and calls `close_acp_generation_in_txn`. In one transaction that function compare-and-sets `open -> closed`, increments row version, insert-or-reads the deterministic `clean_close` event, selects the complete durable `admitted` origin set, settles each still-running original owner with `safeCause.code=adapter_unavailable`, and changes each origin to `settled` with `settlementKind=clean_close` and its failure ID. A clean close with no admitted origins writes only the generation event. Duplicate close reads the existing event and changes nothing.
7. On the first decode failure, Conn fences in memory immediately, computes only byte count and SHA-256 sample hash, and acquires the same callback serialization by already owning its mailbox turn.
8. In one transaction `desync_generation_in_txn` compare-and-sets `open -> desynced`, increments row version, insert-or-reads the deterministic event, selects the complete durable `admitted` origin set under that same transaction, settles each still-running original owning row, and changes each origin to `settled` with `settlementKind=desync` and its failure ID. It stores no independent envelope on `acp_pending_origins`.
9. For either generation-wide failure, a declared and proven read-only method uses `known_no_effect` only with `noEffectEvidence.kind=declared_read_only`. Prompt and unclassified methods use `unknown`, `verify_then_new_attempt`, and `inspect_effect`.
10. Each affected envelope contains the same `connectionFaultRef` for that event. None contains a request-specific upstream claim.
11. The single SQLite writer and Conn callback serialization decide response versus generation-fence ordering. A committed response removes its origin from the later fence's admitted set. A committed clean-close or desync fence settles the origin first, so a later response reads that settlement and creates no success projection.
12. After a generation-wide failure commits, Conn replies to remaining callers, closes the port when needed, and tells the coordinator to start a strictly newer generation.
13. If a generation-fence transaction fails, Conn closes the port. Recovery reads the persisted row and event. It may omit an unavailable desync sample hash, but it cannot settle a connection-caused origin without `connectionFaultRef`.
14. Duplicate malformed frames lose the generation CAS and read the existing event. Restart never reopens or admits work to a `desynced` or `closed` generation. Recovery reruns the corresponding event settlement for any origin still `admitted`; it does not resend.

### Idempotency v2 and canonical digest

The digest document is:

```json
{
  "digestVersion": 1,
  "principal": {"kind": "user|session|process", "id": "..."},
  "operation": "spawn|retire|wake|assign|condition|work-item-create",
  "target": null,
  "params": {}
}
```

`target` is the submitted target kind and identifier, or null. `params` contains the router's validated submitted fields after field-name normalization and before default resolution. It excludes `idempotencyKey` and `requestDigest`. Null and absent remain distinct. Array order is preserved. Object order is normalized by RFC 8785. The server computes the digest. If a client sends `requestDigest`, it must be lowercase 64-character SHA-256 hex and equal the server result before admission.

The v2 transaction behavior is:

1. Lookup and uniqueness use the exact canonical principal tuple plus operation and key; digest principal and row principal must match.
2. No row: insert `in_progress` with canonical digest, attempt, correlation, target, action, and timestamps before the effect.
3. Same principal tuple, operation, key, and digest: return the stored settlement. If still `in_progress`, reconcile from operation-specific durable evidence; do not execute again.
4. Same principal tuple, operation, and key with a different digest: return `idempotency_digest_conflict`, create no attempt, and execute nothing.
5. A different principal kind or ID with the same operation and key is a distinct namespace and follows the no-row rule.
6. Legacy row: return its historical session success with `digestCheck=unavailable`; do not compare or fill a digest.
7. Unkeyed client: set `replayPolicy=no_replay_key`; repeating creates a new attempt.
8. A stale v2 `in_progress` row settles `known_committed` only from a durable operation result, `known_no_effect` only from pre-mutation refusal or verified no-effect evidence, and otherwise `unknown`. It never restarts automatically.

### Exact migration

The only permitted in-place migration starts from exactly one `schema_stamp` row equal to `model-identity-v1`. It runs before runtime children start. Inside the migration transaction, it first verifies that no pre-v2 turn has `status IN ('queued','running')`. If one exists, it raises `Tightbeam.Schema.MigrationBusyError`, changes no row, and lets the old binary resume so that pending work can settle. The migration does not fabricate attempt identity for work admitted by the old shape.

In one `BEGIN IMMEDIATE` transaction, the migration:

1. creates the target v2 tables and typed companion tables with final checks and indexes;
2. copies each `wire_idempotency` row as `schemaVersion=1`, `state=legacy_succeeded`, mapping its old `ownerUserId` to `principalKind=user` and `principalId=<exact old ownerUserId>`, preserving `operation`, `idempotencyKey`, and `sessionKey`, and leaving digest, attempt, envelope, and settlement null;
3. copies `turns`, preserving each field; labels existing `failed` and `failed_unknown` rows `legacy_untyped`; leaves their typed IDs and envelope null;
4. copies `messages`, preserving each field and leaving typed failure columns null;
5. copies `events`, preserving each field and leaving typed failure columns null;
6. copies `lifecycle_events`, preserving each field and leaving historical principal null;
7. verifies source and target row counts for each rebuilt table and validates all target checks;
8. atomically swaps table names, recreates the exact operation and query indexes, and removes transaction-local legacy tables;
9. replaces the one shape stamp with `failure-provenance-v1` as the final statement;
10. commits.

Any failure before commit rolls back the complete migration and leaves `model-identity-v1`. Once the final shape-stamp transaction commits, the database is forward-only: no recovery path restores old-shape bytes or starts an old binary against that database, even if the process stops before listener activation or before the first typed admission. A pre-v2 queued or running row raises the named busy error with its count, but not request content. A missing, duplicate, unknown, or malformed stamp raises `Tightbeam.Schema.ShapeError` with the observed stamp and the only accepted source/target pair. The code does not inspect DDL to choose a path, issue try-and-catch `ALTER` statements, or repair by inference.

Fresh databases stamp `failure-provenance-v1` before creating application tables and create only the target shape.

### Closed safe-cause mapping and redaction

The mapper version is `failure-safe-cause-v1`. It matches only these shapes. `{}` means no public protocol fields; `—` means no upstream claim.

| Observed safe shape | Code and fixed public message | Specificity | Reported layer | Public protocol | Upstream claim |
| --- | --- | --- | --- | --- | --- |
| Codex `data.codexErrorInfo=usageLimitExceeded`; include a retry time only when the structured-time rule below proves a UTC instant | `codex_usage_limit`; `Codex usage limit reached` plus optional bounded UTC retry time | `concrete` | `provider_adapter` | observed integer `jsonRpcCode`; `providerCode=usageLimitExceeded` | `{layer=provider_adapter, code=usageLimitExceeded}` |
| Claude `data.errorKind=rate_limit`; include a reset time only when the structured-time rule below proves a UTC instant | `claude_rate_limit`; `Claude rate limit reached` plus optional bounded UTC reset time | `concrete` | `provider_adapter` | observed integer `jsonRpcCode`; `providerErrorKind=rate_limit` | `{layer=provider_adapter, code=rate_limit}` |
| `data.details` begins with exact class `Invalid value for config option model` | `invalid_model_config`; `Configured model is unavailable` | `concrete` | `acp` | observed integer `jsonRpcCode` only | — |
| `data.details == Session not found` | `session_not_found`; `Session was not found` | `concrete` | `acp` | observed integer `jsonRpcCode` only | — |
| `data.details == auth expired` | `authentication_expired`; `Authentication expired` | `concrete` | `acp` | observed integer `jsonRpcCode` only | — |
| typed tune denial `code=model_unavailable` | `model_unavailable`; `Requested model or effort is unavailable for the destination harness` | `concrete` | `gateway` | `{}` | — |
| first undecodable frame on a fenced generation | `acp_protocol_desync`; `Adapter protocol stream became unreadable` | `class_only` | `acp` | `{}` | — |
| boot recovery or interruption with unverified effect | `outcome_unknown`; `Execution was interrupted; effect is unknown` | `unknown` | `ledger` | `{}` | — |
| task crash with observed `File.Error :enoent` | `required_file_missing`; `A required local file is unavailable` | `concrete` | `session_lane` | `{}` | — |
| other task crash | `task_crash`; `Local task crashed` | `class_only` | `session_lane` | `{}` | — |
| `acp_exit` plus bounded integer status | `adapter_exit`; `Adapter exited` | `class_only` | `adapter` | `{}`; status stays in `execution.exitStatus` | — |
| `:noproc` or `:normal` adapter loss | `adapter_unavailable`; `Adapter became unavailable` | `class_only` | `adapter` | `{}` | — |
| captured credential-status timeout | `credential_status_timeout`; `Credential status check timed out` | `concrete` | `credential_process` | `{}` | — |
| empty body or EOF with no deeper evidence | `response_missing`; `Command produced no parseable response` | `unknown` | `wire` | `{}` | — |
| outer `message=Internal error` with no allowlisted concrete field | `acp_internal_error`; `ACP returned an internal error` | `class_only` | `acp` | observed integer `jsonRpcCode` only | — |
| every unlisted shape | `unclassified_failure`; `Failure cause is unavailable` | `unknown` | the boundary layer that supplied the input | `{}` | — |

Message constructors interpolate only a parsed UTC instant, a bounded integer exit status, or a closed enum. A time parser accepts only an allowlisted structured field containing either RFC 3339 with the `Z` UTC designator or a nonnegative integer UTC epoch millisecond value. It does not parse prose or infer a year or timezone from `observedAt`. The reviewed Codex prose without a timezone and Claude prose without a year therefore produce no public retry/reset time. Accepted instants render as RFC 3339 UTC; every other value is omitted. Public output never contains raw account state, path, URL, prompt, map, stderr, stack, or credentials.

Historical `legacy_untyped` rows use their stored bounded string only on the local legacy surface. Parent and owner projections use fixed `Failure cause is unavailable` and retain safe turn/session identifiers. They receive no fabricated code, layer, outcome, retry, or owner.

### Typed readers and compatibility

| Surface | Durable source | Required projection |
| --- | --- | --- |
| Local or target transcript | Typed `messages` marker committed with owner settlement | `FailurePublicV1`; exact IDs; legacy marker prefix retained |
| Parent notice | `failure_delivery` plus receiver receipt | Same public payload plus bounded origin; delivered or typed `not_applicable` |
| Terminal-owner alert | `failure_delivery` plus `failure_action` when actionable | Same public payload and selected route; delivery recovery ends at receipt, action supersession/overdue, or a terminal integrity status |
| Owning-row and selected-owner delivery status | `failure_delivery` | Bounded `Delivery integrity status`; no payload hash, diagnostic, or arbitrary text |
| Wire and CLI | Keyed or unkeyed attempt settlement | Same safe IDs and settlement; response loss replays settlement, never execution |
| Public trace | Owning envelope plus lifecycle/action/delivery/connection rows | `FailurePublicV1` only; diagnostic fields are structurally unavailable; no prose parsing |

Existing `data.details` mappings remain. New mappings add the reviewed Codex nested fields, Claude kind, adapter exits, task crash, credential timeout, response missing, protocol desync, and unknown outcome. Existing session-control denial remains `HTTP 200` with `ok=false` and `code`; additive typed fields include `attemptId`, `failureId`, `correlationId`, `requestDigest`, `replayPolicy`, and `FailurePublicV1` where a failure exists.

For exact reviewed event `30942`, model and effort request values are null, destination harness is `codex`, resolved values are the observed Claude model and medium effort, and both sources are `boot_wide_default`. The implementation records this observed resolution. It does not call it source-session copying. A later destination-harness default records `destination_harness_default` and does not rewrite history.

### Observability

Expose durable counts grouped by safe cause code, reported layer, harness, model, cause specificity, provenance linkage, outcome, retry disposition, and terminal-owner kind. Metric labels use only those closed typed fields and exclude diagnostic objects and arbitrary strings. Expose counts of:

- new terminal failure rows missing typed envelopes;
- legacy-untyped terminal rows;
- typed markers missing `failureId` or `attemptId`;
- unsettled parent notices and terminal-owner alerts by delivery state;
- delivery lease reclaims, stale acknowledgements, stale reschedules, and integrity conflicts;
- ACP desynchronization and clean-close events, and terminal generations with admitted origins;
- pending origins per connection generation;
- pending and overdue actions by owner kind;
- legacy missing-fallback route refusals by primary owner kind and safe cause code;
- v2 idempotency reconciliation results and digest conflicts.

Expose age measurements from persisted timestamps for attempt admission to settlement, failure commit to reader receipt, unknown outcome, pending delivery, and pending/overdue action. Public trace serializes only `FailurePublicV1`; it emits no internal envelope, action, delivery, connection, migration, or diagnostic field that is absent from that projection.

### Staged rollout and recovery

#### Stage 0 — fixture and baseline gate

Close OQ-01 through its separately immutable fixture manifest and durable owner closure row. Verify each fixture's canonical path and SHA-256 against the manifest before a test reads that fixture. Record no fixture custody data by amending this spec. Run the unmodified canonical CI gates and record counts. Run actual harness boundary smoke for adapter-dependent assumptions using the recorded versions required by product guidance. No feature code proceeds for a case whose real fixture path or SHA-256 is missing or mismatched.

#### Stage 1 — exact schema and dormant readers in copied databases

Build the exact migration, target schema, validators, public projector, trace readers, and metrics. Run migration on a copied real database and a fresh database with no production traffic. Prove transaction rollback on every pre-commit migration fault seam and forward recovery after a committed target stamp. Gate on zero change to existing wire and transcript bytes in the unmodified baseline. This stage is not a separately deployable production mode.

#### Stage 2 — complete command-denial settlements

Enable full atomic typed settlement for the reviewed `set_harness` denial and keyed wire/process denials. Enable receiver dedupe and delivery/deadline workers. A typed origin enables the entire envelope/marker/action/delivery set; partial typed writes are not a stage. Keep existing response keys and status.

#### Stage 3 — complete turn settlements and readers

Enable typed admission for accepted turns, task crashes, adapter failures, and boot `failed_unknown`. Switch typed failures from legacy Bubble to delivery outbox. Keep legacy Bubble recognition only for legacy-untyped rows and use its fixed safe renderer. Enable transcript and parent/owner public projections.

#### Stage 4 — ACP generation fencing

Enable persisted connection generations, origin admission, serialized commit-plus-send, decode-event fencing, and restart recovery. Run live harness feature smoke for both harnesses with pinned binaries after deterministic seam tests pass.

#### Stage 5 — client digest emission

Release Rust CLI support for `requestDigest` and typed output. The server remains compatible with old keyed clients that omit the digest and unkeyed clients. Compare server- and client-computed fixture digests before making the client field default.

Stages 1–4 are implementation and verification gates. The first production server release contains their complete behavior and does not pause in a mode that writes new legacy-untyped in-scope failures. Roll forward only after each stage's acceptance subset and observability checks pass. Stage 5 may release later because server-computed digests preserve old-client behavior.

#### Boot recovery order

Before Bandit, Wakes, lanes, adapters, delivery workers, or deadline workers accept work:

1. resolve and validate `failure_action_deadline_ms`; fail boot before any schema mutation when invalid;
2. validate or execute the exact schema transition;
3. capture one `bootNow`;
4. reconcile `desynced` or `closed` connection rows and admitted origins without resend;
5. atomically settle running turns as unknown using the validated policy snapshot;
6. reconcile v2 `in_progress` commands from operation-specific durable evidence using that snapshot for a newly created actionable settlement;
7. expire pending actions by their stored deadline with one CAS and fallback delivery;
8. make expired delivery leases claimable without changing their settlement;
9. start readers and workers;
10. accept traffic.

Repeating steps 4–8 produces no duplicate envelope, marker, action, event, receipt, or delivery.

#### Production recovery and rollback

Before a production migration, the release operator drains new work and runs the exact copied-database and integrity gates named by OQ-02. These are rollout prerequisites, not actions authorized by this writing assignment.

If migration fails before commit, the transaction rollback leaves `model-identity-v1`; the old binary may resume. The committed shape stamp is the complete rollback boundary. After `failure-provenance-v1` commits, recovery is forward-only from owning rows and outbox, including a stop before listener activation or before any typed attempt is admitted. The release does not restore a pre-migration backup, start the old binary, or discard target-shape rows after that commit. This deletion avoids a separate traffic-acceptance event whose ordering could disagree with actual listener availability.

### Test-only fault seam

`FailureSettlementFault` is injected only in tests and has no production configuration key or default callback. It supports these exact points:

- before terminal compare-and-set;
- after each settlement transaction statement;
- after commit and before delivery claim;
- after send and before delivery acknowledgement;
- before action deadline compare-and-set;
- after ACP origin admission commit and before frame write;
- after each migration copy/swap statement.

A transaction point raises and rolls back. A worker point exits the test worker. Tests use an injected clock and never wait on wall time.

### Requirements-to-seam trace

| Invariants | Implementation seam | Acceptance |
| --- | --- | --- |
| I-01–I-04, I-10–I-11, I-19–I-20 | `Tightbeam.Failures`, Ledger, SessionLane, CommandEdge | A06, A08, A16, A20 |
| I-05–I-07 | delivery worker, delivery/action tables, receiver transaction | A06, A07, A17, A23, A26 |
| I-08–I-09, I-21 | Acp.Conn, Acp.Adapter, AdapterCoordinator, connection tables | A11–A13, A22 |
| I-12–I-14 | Projection, Transcript, Bubble, destination receivers | A18, A19, A21, A25 |
| I-15–I-16, I-24 | closed mapper and immutable fixture bundle | A01–A05, A09–A11, A21, A24 |
| I-17 | Gateway tune selection result | A19 |
| I-18, I-22 | Schema, Idempotency, Router, CLI | A05, A14, A15, A19 |
| I-23 | typed trace and metrics readers | A08, A12, A17, A21, A23, A25 |

## Acceptance

The implementation must pass these 26 deterministic cases. Each fixture-dependent test resolves its real fixture only through the work-item-bound fixture manifest and verifies the fixture SHA-256 before parsing it. Each test name or fixture metadata records the reviewed evidence source from the manifest. `FailureSettlementFault` and an injected clock replace sleeps.

### A01 — Surf Codex cause and one identity

Given the immutable real fixture derived from lifecycle row `221422`, when the command edge settles the attempt, then it writes `safeCause.code=codex_usage_limit`, a bounded fixed message, typed local marker, parent delivery, owner delivery, and one identical `failureId` on each surface; and no account URL or raw map crosses `FailurePublicV1`.

### A02 — Claude weekly limit

Given the immutable real fixture derived from lifecycle row `219529`, when the command edge settles the attempt, then it writes `safeCause.code=claude_rate_limit`, preserves the numeric protocol code separately, writes the typed marker and bounded parent/owner projection, and publishes no arbitrary provider prose.

### A03 — Existing `data.details` classes and no invented specimen

Given real fixtures from historical turns `729` and `4183`, when the mapper processes them, then it returns `invalid_model_config` and `session_not_found` respectively. The test suite contains no hand-written contentless `-32603` incident fixture while that specimen remains NOT PROVEN.

### A04 — Eezo credential timeout produces typed non-empty response

Given the captured eezo credential-timeout result, a valid distinct persisted fallback, and a controllable credential-boundary seam, when spawn fails before mutation, then the wire returns deterministic non-empty JSON with attempt and correlation IDs, `credential_status_timeout`, `outcome=known_no_effect`, and zero spawn artifacts without a real sleep.

### A05 — Post-effect response loss replays settlement

Given the captured real CLI regression in which the effect committed before an empty response, when the caller repeats the same v2 key and digest, then it receives the original `known_committed` settlement, the effect count remains one, and the CLI does not emit parser EOF.

### A06 — Settlement crash matrix

Given one legal actionable failure attempt, one legal `nextAction=none` failure attempt, and each `FailureSettlementFault` point before commit, after each statement, and after commit before delivery claim, when the process crashes and recovery runs twice, then the database contains either zero dependent facts after rollback or exactly one owning envelope, lifecycle fact, marker, parent delivery, and owner delivery after commit. The actionable fixture also contains exactly one legal action; the `nextAction=none` fixture contains no action.

### A07 — Lease reclaim fences stale ack and reschedule

Given a pending delivery with `nextAttemptAt=t`, when claimants using one injected clock run at `t-1`, `t`, and `t+1` on fresh copies, then the first changes zero rows and equality and after are eligible. Given a worker that sent and crashed before acknowledgement, when a second worker reclaims the delivery at `leaseUntil` and the stale worker tries acknowledgement, send-failure reschedule, and integrity terminalization with its old epoch, token, and owner, then all stale compare-and-sets affect zero rows and only the current lease can settle delivery.

### A08 — Running-turn recovery is verify-first

Given one running turn, absent deadline config, and captured `terminalAt=t`, when boot recovery runs twice, then one unknown envelope, marker, action, parent delivery, and owner delivery exist; the owner is not `process`; retry is `verify_then_new_attempt`; next action is `inspect_effect`; `deadlinePolicyMs=86400000`; `deadlineSource=process:tightbeam`; `actionDeadline=t+86400000`; and no execution occurs.

### A09 — Task crash retains safe concrete provenance

Given the immutable real fixture derived from lifecycle row `541`, when the session lane settles it, then the owning turn and parent projection show `required_file_missing`, the path is absent publicly, and the bounded internal diagnostic retains the redacted local stack class and linkage.

### A10 — Adapter exits preserve only proven cause

Given immutable real fixtures for a numeric adapter exit with bounded stderr, `:noproc`, and `:normal`, when each settles, then the envelope records launch correlation and safe exit fields; public output excludes stderr; and `:normal` and `:noproc` remain class-only with unknown initiating cause.

### A11 — ACP origins settle on response, clean close, and desync

Given one durable admitted origin and a valid response, when Conn handles the response, then the owning result and `admitted -> settled` origin transition with `settlementKind=response` commit together before the caller receives the result; a duplicate response reads that result and writes nothing. Given a fresh generation with multiple admitted origins, when the port closes cleanly, then one `clean_close` event changes the generation to `closed`, each original owner settles once as `adapter_unavailable`, each origin records `settlementKind=clean_close` and the same connection event reference, and no request attribution is invented. Given another fresh generation with multiple admitted origins and one captured protocol fixture or synthetic parser-seam undecodable frame with no request ID, when Conn receives it, then it writes one deterministic desync event, fences the generation, gives each admitted origin the same connection reference, makes no request attribution, replies without a hang, closes the port, and permits only a newer generation.

### A12 — Duplicate generation termination and restart are idempotent

Given each clean-close and desynced generation from A11, when the same termination is processed again and boot recovery runs twice, then the generation compare-and-set, event uniqueness, and origin settlement CAS produce no duplicate event or settlement; no origin remains admitted; and neither terminal generation admits work.

### A13 — Read-only and prompt malformed settlements differ

Given one declared and proven read-only method and one prompt on the same fenced generation, valid inherited owner routes for both origins, and one validated server deadline-policy snapshot, when both settle, then only the read-only method has `known_no_effect` with durable `declared_read_only` evidence; the prompt has `unknown`, `verify_then_new_attempt`, `inspect_effect`, its inherited distinct persisted fallback, and the immutable deadline snapshot.

### A14 — Legacy idempotency migration preserves uncertainty

Given a quiescent copied database containing real legacy idempotency rows, when the exact migration commits, then each old key maps to `principalKind=user` and its exact old `ownerUserId` as `principalId`; original keyed replay still returns the stored session result; digest and attempt remain null; digest conflict is unavailable; and no envelope or cause field is fabricated. Given a stop immediately after the target shape commits and before listener activation or typed admission, when recovery starts, then it retains `failure-provenance-v1`, starts no old binary, restores no old-shape bytes, and completes forward recovery. Given a second copy with a queued or running pre-v2 turn, when migration runs, then it raises `MigrationBusyError`, changes no row, and retains `model-identity-v1`.

### A15 — V2 principal replay, conflict, and retry supersession

Given settled v2 command rows for user, session, and process principals, when the exact same principal tuple, operation, key, and digest repeat, then each stored settlement is read with no effect. When the same tuple and key carry a different digest, then a typed conflict returns with no effect. When the same operation and key are used by a different principal kind or ID, then the request occupies a distinct row and cannot replay or conflict with the first principal. Given each retry disposition and its required evidence/result state, when an accountable actor requests an explicit linked attempt, then admission applies the five disposition rules in Architecture §Failure actions and deadlines, creates a new attempt only for an accepted rule, leaves the predecessor envelope and owning settlement unchanged, and applies the specified completed-or-superseded action state. A rejected rule writes nothing. Given a leased actionable predecessor delivery racing that accepted successor, when the receiver transaction commits first, then it may create exactly one current-action projection before supersession; when successor admission commits first, then the receiver creates one same-hash supersession tombstone, creates no projection, and the lease owner or a later claimant changes the delivery to `superseded` with the successor attempt ID.

### A16 — Legal matrix is exhaustive

Given the Cartesian product of each v1 outcome, replay policy, retry disposition, v1 next action, owner kind, fallback presence, condition reference, and no-effect evidence state plus validated server deadline-policy snapshots and terminal times at both ordinary and checked-add overflow boundaries, when the validator processes each tuple, then it accepts exactly the tuples generated by the six matrix rule families after expanding each enumerated alternative and whose absolute deadline is representable. It rejects every absent tuple, expired evidence, missing durable evidence reference, missing or extra `conditionRef`, process-owned unknown, an actionable route without the required fallback, caller-supplied deadline fields, deadline-policy fields on `nextAction=none`, and an overflowing deadline sum before persistence.

### A17 — Deadline cutoff is exact and does not execute work

Given three pending actions with `deadline=d`, valid persisted fallbacks, and durable completion results at `d-1`, `d`, and `d-1`, when workers run respectively at `d-1`, `d-1`, and `d`, then only the first action completes. The equality case and the worker-at-deadline case each produce exactly one `pending -> overdue` transition and one fallback-owner delivery. No case creates an attempt, executes work, changes the envelope, or changes the persisted deadline policy.

### A18 — Parentless and unavailable owner routes stay distinct

Given parentless Surf, a separate attempt whose primary owner is unavailable, and a user destination with no owned main stream, when they settle and delivery runs, then Surf gets parent `not_applicable`; the unavailable primary selects its deterministic assignment or user fallback; each still gets its terminal-owner row; the missing-stream send creates no receiver receipt and fenced-reschedules the same delivery; and no raw Bubble interpolation occurs.

### A19 — Exact model-free Codex restore denial

Given the immutable real fixture for event `30942`, its model-free request, a valid distinct persisted fallback and durable selection-condition reference, configured `failure_action_deadline_ms=3600000`, and captured `terminalAt=t`, when the gateway denies restoration, then model and effort `requested` are null, `resolved` values match the observed selection, both sources are `boot_wide_default`, destination harness is `codex`, outcome is known no effect, retry disposition is `new_attempt_after_condition`, next action is `choose_model`, action and delivery rows are typed, the action stores the supplied durable condition reference, deadline `t+3600000`, policy `3600000`, and source `process:tightbeam`, existing HTTP status/code remain, and every surface carries one failure ID.

### A20 — Required identity, fallback, and closed action enforcement

Given attempts with missing `failureId`, missing `attemptId`, a `failureId` not derived from its `attemptId`, mismatched owning attempt, any actionable primary with a missing, same-as-primary, missing-row, session-kind, or process-kind fallback, a caller-supplied deadline field, or v1 `nextAction=wait_until`, when admission or settlement validates them, then it rejects before persistence, writes no dependent facts, and starts no effect. Route failures use `missing_fallback_owner`; the excluded action uses `unsupported_failure_action` and safe message `wait_until is not supported by failure provenance v1`.

### A21 — Public redaction boundary

Given secret-like tokens, stacks, prompts, stderr, filesystem paths, arbitrary provider prose, account URLs, an unsafe request reference, a populated internal `diagnostic`, and an envelope above 32,768 canonical bytes, when constructors and public readers process them, then the oversize envelope is rejected; the unsafe request reference stays internal; none of the secret-like values appears in chat, parent prompt, owner alert, wire, CLI, transcript, or public trace; `diagnostic`, `redactedSummary`, `sampleHash`, and `capturedBytes` are absent from each public surface; and the fixed safe code and message remain.

### A22 — ACP admission/response/fence races and commit-before-send crash

Given the two permit orders between guarded admission and each generation fence plus a crash after admission commit and before frame write, when each schedule runs deterministically, then an admission that wins sends only after its admitted row commits and is included in settlement; a fence that wins causes no row and no send; and the crash case is recovered conservatively without resend. Given both SQLite commit orders between a valid response transaction and desynchronization, when the response wins, then its origin settles once with the owning result and desynchronization excludes it; when desynchronization wins, then the later response reads the failure settlement and creates no success or second caller result.

### A23 — Boot validates policy and uses stored absolute deadlines

In the policy-validation subcase, given absent config, boundary values `1` and `2592000000`, and invalid values `0`, `2592000001`, and a non-integer, when separate boots start, then absent config resolves to `86400000`, both boundary values pass, and each invalid boot stops before schema mutation, workers, or traffic. In the recovery subcase, given a typed pending action with a valid persisted fallback and a legacy-missing-fallback action whose stored deadlines precede captured `bootNow`, when config has since changed and recovery runs twice while racing the live deadline worker, then recovery uses each stored absolute deadline; the typed action has one overdue transition and one fallback delivery; the legacy query writes or reads one deduplicated `failure_route_dispatch_refused` audit, creates no fallback delivery, leaves owner and action state unchanged, and excludes the audited row from later boot and worker queries; and neither path executes work, resets an action, or creates a new failure ID.

### A24 — Closed mapping is exhaustive and fail-closed

Given one immutable fixture for each mapping row plus unlisted provider prose, when the mapper runs, then each listed shape yields its exact code, fixed message, specificity, layer, and safe protocol; the unlisted shape yields `unclassified_failure` with bounded internal diagnostic hash/count; and no raw detail appears in `FailurePublicV1`.

### A25 — Every reader preserves safe provenance

Given concrete, class-only, unknown, linked, partial, absent, upstream-claimed, and connection-fault envelopes, when target chat, transcript, parent, owner, wire, CLI, and trace project them, then each surface serializes the same `FailurePublicV1` fields, only asynchronous surfaces add `deliveryId`, and no surface serializes an internal diagnostic field.

### A26 — Receiver hash conflict is atomic

Given one leased `deliveryId`, `payloadVersion=1`, and public payload hash, when the receiver processes it, replays the same pair, and receives the same ID with a different hash on fresh copies, then the first call creates one projection, the second returns that projection, and the conflict call returns `failure_delivery_integrity_conflict`, creates no second projection, writes or reads one principal-bearing deterministic integrity fact, and changes the currently fenced delivery to terminal `integrity_conflict` in the same transaction. Given another leased row whose worker reconstructs different bytes under v1, when it checks before send, then it sends nothing and makes the same fenced terminal transition with boundary `worker`. In both conflict paths a stale fence changes no row or fact; the selected terminal owner and owning-row reader can read only the bounded integrity status; and later claim, recovery, reschedule, and send queries exclude the delivery.

## Open Questions

### OQ-01 — BLOCKING for implementation: immutable fixture custody

The reviewed authority names the real rows and incidents but this spec workdir does not contain the complete redacted bytes and SHA records needed for A01–A05, A09–A10, A14, A19, and the listed mapping rows in A24. Before affected implementation begins, the work-item owner must assign read-only fixture extraction from the already reviewed evidence. The extractor must record each fixture as an immutable artifact and record one separately immutable fixture manifest whose entries name the exact fixture canonical paths, SHA-256 values, and reviewed source identifiers. A builder must not reconstruct fixture bytes from this prose.

OQ-01 remains open until those exact fixture paths and SHA-256 values exist and the work-item owner files the `OQ-01 closure row`. The owner does not amend this spec to close OQ-01. If a fixture reference becomes a normative spec requirement or changes a requirement, expected outcome, mapping rule, or test oracle, the owner must keep OQ-01 open, create a successor immutable spec, obtain fresh independent `reviewed-clean`, and replace the spec binding before affected implementation begins.

Given an owner closure row whose manifest artifact ID, canonical path, SHA-256, and reviewed spec SHA-256 match the work-item-bound tuple, when a fixture-dependent builder starts, then the builder uses only that exact spec and manifest tuple and verifies each fixture SHA-256 before parsing. Given a missing or mismatched tuple field, fixture path, or fixture SHA-256, when the builder starts, then the affected scope remains blocked and no fixture-dependent feature code runs. Pure schema/type code may proceed only after independent review confirms it does not encode fixture-derived assumptions.

### OQ-02 — BLOCKING for production rollout only: maintenance and forward-recovery authority

The deployment owner has not named the production database, maintenance window, migration principal, or forward-recovery incident owner. Implementation and copied-database migration tests may proceed. A production migration waits until those four values are recorded on the rollout assignment and the copied-database gates pass. No named principal may restore an old shape after the target stamp commits. This spec does not authorize a deploy or live-state mutation.
