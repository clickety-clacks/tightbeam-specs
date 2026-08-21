# Idle-worker parent disposition v1 — revision 2 sealed review candidate

Status: sealed immutable review candidate responding only to F1-F4 in `changes-requested` verdict `att_739eec29-bd70-4645-8ab0-3fb57abbc069`. The cold digest is complete. Implementation remains prohibited until the existing sole linked review records `reviewed-clean`. The artifact row records the content SHA-256 outside these self-referential bytes.

Canonical home: `specs/tightbeam/idle-worker-parent-disposition-v1.md` in `clickety-clacks/tightbeam-specs`

Work item: `wi_c49c1e4a-fd43-40bd-bf04-bd5150a6b5ca`

Specification assignment: `asg_9aaee147-96a9-400b-9830-949cc932350a`

Current product source provenance: `origin/0.1.8` at `4af89039dbb55291383a657ef28700b1acd8122f`

Current specification provenance: `clickety-clacks/tightbeam-specs` `origin/main` at `6b0aa95ea5b0023ee3dd12e581ab779fc1f806cf`, on dedicated branch `work/asg-9aaee147-idle-worker-respec`

Owner authority: `att_5fc0e23c-6b9c-4d3e-b47e-45ae7d296efb` and `att_29616387-319f-442e-add8-3ad737ee7fa0`

Revision 1 review evidence: predecessor `art_3609851e` at SHA-256 `8c6d3dd4beaeb4afe9335d13f1e59ff0c7c232873fe8a179b891ae30a49dac2`; sole linked verdict `att_739eec29-bd70-4645-8ab0-3fb57abbc069`; full clause report `art_88f15a24` at SHA-256 `e9f8959b5ed5799506dab4a954b38cef1215223205f3cc5c3a7d1e5c0e1d8c83`

Historical evidence only: archived recon artifact `art_9af25de4`, SHA-256 `6e383299345f37bd1737ac33c29da4e23da289f88ec371f6ebf49b22ff439f46`

Lost historical artifact: `art_d1b8493a`, expected SHA-256 `f4f085d3d9cbd5193ffb73f61011695d97157cfc0ec1cc5a3cc4dccc196e1687`. Its bytes are unavailable. This document does not recover, reproduce, supersede by byte identity, or inherit review from that artifact.

## Goal

When an active non-root child session finishes its current assigned work and enters zero open assignments through an eligible idle transition, Tightbeam must create one durable parent-disposition obligation. A responsible same-owner ancestor, or the owner's Main fallback, must explicitly retain or retire the child. Tightbeam must record the choice and enact it atomically with the corresponding lifecycle state.

Retain keeps the child active and closes the obligation. The retained child remains quiet until a later assignment opens a new work epoch. The next transition from that new work epoch to zero open assignments creates one new obligation.

Retire uses the existing terminal retirement lifecycle. It closes any pending idle-worker obligation in the retirement transaction. It rejects later assignment creation under the existing `session_retired` contract.

When a critical lease blocks a generation-bound retire choice, Tightbeam must preserve the open obligation, record an immutable proof of the exact blocking leases, and direct the responsible mind to retry no later than the bounded lease hard deadline. The substrate must not choose retain or retire.

The mechanism is substrate physics over durable rows. It observes assignment, session, lineage, decision-request, wake, lease, and retirement rows. A mind makes the disposition choice. This separation applies wisdom 1, 4, 5, 6, 8, 9, 10, 23, 24, and 26.

### Subtraction decision

ADD wins because the current maintenance line has no durable idle-worker parent obligation or retain action. DELETE loses because removing non-root worker sessions or parent accountability would remove useful work and violate the existing session model. ACCEPT loses because silent idle sessions have no named owner action or deadline. The addition reuses `decision_requests`, lineage routing, wakes, critical leases, the canonical retire transaction, and current schema activation. It adds generation state, blocker-proof state, initial-deadline evidence, and terminal lifecycle replay fields that those seams do not represent.

## Non-Goals

1. The feature does not choose retain or retire.
2. The feature does not retire a session because a deadline or lease hard deadline passes.
3. The feature does not reactivate a retired session or change retired-holder assignment refusal.
4. The feature does not create an idle obligation for the built-in Main session.
5. The feature does not create an idle obligation for an active session that has not entered a work epoch.
6. The feature does not replace assignment supervision, effort check-ins, work-item brackets, completion review gates, or their prods.
7. The feature does not implement the later data-driven prodder refactor.
8. The feature does not add park, pause, relaunch, reassignment, reparenting, automatic retirement, or session resurrection.
9. The feature does not change ordinary session-only `retire --session <key>` syntax or response fields. It adds an optional generation fence for prompts produced by this feature.
10. The feature does not change generic statute and effort request decisions, waivers, visibility, or consumption. It reserves one statute name for the lifecycle-specific actions in this spec.
11. The feature does not parse prompt prose to recover identity, generation, authority, state, or action.
12. The feature does not backfill obligations for sessions that already have zero open assignments when the schema activates.
13. The feature does not alter existing wake-cancellation rows or the accepted requester combinations for other producers.
14. The feature does not split the reviewed implementation into an eighteen-path phase. The open overlapping assignment `asg_8429e570-f9a2-4510-bc60-87b65589c46f` remains a separate custody gate for `lib/tightbeam/supervision.ex` and `test/supervision_test.exs`.
15. The feature does not merge, release, deploy, restart a live service, or probe a live work row as part of specification or implementation verification.

## Terms

1. **Child session**: one session incarnation named by `assignments.holderKey`. It is not a role and not a display name.
2. **Root Main**: the session whose row has `isBuiltIn=1` and whose `sessionKey` equals `Org.personal_session_key(ownerUserId)`. Both facts must match.
3. **Non-root child**: an active child session that is not the root Main.
4. **Open-assignment count**: `SELECT count(*) FROM assignments WHERE holderKey=?1 AND state='open'`, evaluated through the caller's `DB.Txn` when a surrounding mutation is open.
5. **Work epoch**: one numbered lifecycle interval for a child. It starts when assignment creation arms a child that has no current armed or pending generation. It ends when the generation resolves as `retain`, `retire`, or `superseded`.
6. **Generation**: the positive integer identity of a child's work epoch. The durable identity is `(childSessionKey, generation)`.
7. **Armed generation**: a generation with one or more open assignments or a generation activated from an existing non-empty assignment slate. It has no disposition request.
8. **Eligible idle transition**: one terminal assignment mutation that changes the child's in-transaction open count from one to zero while the child is active, non-root, and has an armed generation. The exact retirement interruption marker `cause='holder_retired'`, `requesterId='tightbeam:retirement'` is excluded.
9. **Pending generation**: an eligible idle transition has linked the generation to one open native decision request and its initial parent prompt and deadline reminder.
10. **Disposition request**: one row in the existing `decision_requests` table with `kind='statute'`, `raiserId='process:tightbeam'`, `statuteName='idle-worker-disposition'`, and `actionKey='session:<childSessionKey>#<generation>'`. This is the sole parent obligation. It is not a generic allow/deny statute.
11. **Immediate parent**: the `sessions.spawnedBy` value recorded on the child row.
12. **Responsible parent**: the first active same-owner session in the child's `spawnedBy` lineage. A cross-owner row ends the lineage walk.
13. **Main fallback**: the active root Main for the child's `ownerUserId`, selected when the lineage yields no responsible parent.
14. **Authorized disposition principal**: the owner's user principal, the current responsible parent session, or the current Main fallback session. A process, foreign-owner session, unrelated same-owner session, and retired session are not authorized.
15. **Initial prompt**: the immediate `process:tightbeam` prompt wake addressed to the responsible parent or Main fallback when the request opens.
16. **Current action deadline**: `decision_requests.deadlineAt`. It starts at the configured decision deadline. Each changed-blocker deferral moves it to that proof's greatest blocker hard deadline in the same transaction that replaces the reminder.
17. **Deadline reminder**: the one delayed `process:tightbeam` prompt wake linked through `decision_requests.parkWakeId`, due exactly at the current action deadline. A deferral can replace this wake only through the typed replacement seam defined below.
18. **Generation fence**: the optional positive `--generation <n>` supplied to `retire`. The gateway checks it against the target child's current pending generation before lease scheduling, wake creation, or lifecycle mutation.
19. **Manual retire**: the existing `retire --session <key>` call without `--generation`. Its authorization, legacy idempotency, subtree order, critical-lease intent wakes, response, and terminal behavior remain authoritative.
20. **Generation-bound retire**: `retire --session <childSessionKey> --generation <generation>` copied from an idle-worker prompt. It uses the same retirement lifecycle and a different critical-lease deferral projection so the pending decision request remains the only obligation.
21. **Retain action**: `retain --session <childSessionKey> --generation <generation>`. It exists only for a current pending idle-worker generation.
22. **Lifecycle input digest**: lowercase hexadecimal SHA-256 over the UTF-8 RFC 8785 canonical JSON object `{"generation":<n>,"sessionKey":"<raw child session key>"}`. The ledger key already scopes owner, operation, and idempotency key; the digest binds every remaining lifecycle input.
23. **Shell-quoted session key**: a POSIX shell word formed by surrounding the raw session key with single quotes and replacing each embedded single quote with the five-character sequence `'"'"'`. Shell parsing yields exactly one raw `--session` argument.
24. **Blocker proof**: one sealed header plus its ordered lease rows, captured in the same transaction that returns `retire_deferred` for a generation-bound retire.
25. **Direct retire resolution**: an armed generation resolves as retire inside an authorized manual retirement transaction without creating a request, initial prompt, deadline reminder, zero-basis field, parent target, or blocker proof.
26. **Request-backed retire resolution**: a pending generation and its request resolve as retire inside the retirement transaction.
27. **Canonical home**: `specs/tightbeam/idle-worker-parent-disposition-v1.md` in `clickety-clacks/tightbeam-specs`. A session-workdir copy and an artifact row are evidence pointers, not specification custody.

## Assumptions

1. `Tightbeam.DB` remains the single writer. `DB.transaction/2` uses `BEGIN IMMEDIATE`, and a `*_in_txn` helper uses only the supplied `DB.Txn`.
2. Assignment open, terminal attest close, revoke, surrender, and retirement interruption remain serialized mutations.
3. An active root Main exists for each owner. Current retirement law keeps it active.
4. Session rows and `spawnedBy` lineage remain durable after retirement.
5. Assignment creation rejects a retired target before it inserts the assignment.
6. The existing wake store provides durable scheduling and one turn admission per fired wake.
7. The existing decision-request table stores finite `deadlineAt`, current `status`, owner visibility, and one open `(raiserId, statuteName, actionKey)` tuple.
8. `CriticalLeases.active_in_txn/3` returns the current unexpired lease for one session. Each lease carries `reason`, `startedAt`, `expiresAt`, `hardDeadline`, and `updatedAt`.
9. The canonical retire transaction computes the active subtree once, rejects the entire mutation when one subtree lease is active, and retires descendants before the parent when no lease blocks it.
10. Current `wake_cancellations` has the exact eighteen-column shape and requester matrix at product `origin/0.1.8:4af89039`. Current Schema activation validates exact owned-object SQL and rolls back an interrupted additive activation.
11. Current `wire_idempotency` has the four-column legacy shape owned by `lib/tightbeam/idempotency.ex`. Its operation CHECK admits `spawn`, `retire`, `wake`, `assign`, `condition`, and `work-item-create`; its primary key is `(ownerUserId, operation, idempotencyKey)`.
12. The current repository verification authority is `.github/workflows/ci.yml` on product `origin/0.1.8:4af89039`. Its Linux and macOS jobs run the shipped-privacy and public-rule gates, build a fresh release CLI before Mix, run the same pinned toolchains and test order, and build packages only after tests pass.
13. The reviewed implementation boundary is the twenty recovered paths plus `lib/tightbeam/idempotency.ex` required by F1, as listed in Architecture AR12. Tightbeam file custody must accept that complete set before implementation edits begin.

If an assumption is false, implementation stops and reports the exact contrary row, source clause, or command result. The implementer does not infer a replacement rule.

## Invariants

### I1 — One current generation per child

For one child, the schema permits at most one `armed` or `pending` generation. Historical resolved generations remain queryable. Generation numbers increase by one and do not reuse a prior value.

### I2 — One native obligation per pending generation

A pending generation has exactly one open disposition request with the reserved statute and action key from Terms 10. The request and generation refer to each other. A unique request link and the existing one-open decision-request index make a second obligation unrepresentable.

### I3 — Atomic eligible transition

The terminal assignment change, in-transaction open-count check, generation transition to pending, request insert, initial prompt insert, deadline reminder insert, and lifecycle event commit in one database transaction or roll back together.

### I4 — Initial wake uniqueness and typed replacement

The winning pending transition creates one initial prompt and one deadline reminder. Later code creates no second immediate prompt. `defer_session_disposition_in_txn/6` is the sole path that can replace the current deadline reminder. For a changed blocker digest, it inserts a replacement wake due at the proof's greatest blocker hard deadline, cancels the old pending wake through `Wakes.cancel_in_txn/2` with typed provenance, and updates both `decision_requests.deadlineAt` and `decision_requests.parkWakeId`. These changes, the sealed proof, and the generation proof pointer commit in one transaction. The request deadline always equals the pending reminder due time.

### I5 — A marked intent has an owner and deadline

The disposition request stores the child's owner, a finite current action deadline, the question, shell-safe exact retain and retire commands, and the generation context. The generation stores the initial deadline, selected parent session, and routing kind. A pending request therefore has an accountable principal, the original deadline evidence, and one current deadline reminder.

### I6 — The substrate records; a mind chooses

No timer, delivery result, failed turn, missing response, critical-lease expiry, restart, or retry changes a generation to retain or retire. Only an authorized `retain` call or an authorized retirement transaction records the disposition.

### I7 — Retain is generation-fenced and atomic

The retain transaction verifies the child is active, the named generation is current and pending, the linked request is open, the in-transaction open count is zero, and the caller is an authorized disposition principal. It then resolves the generation as retain, consumes the request, records the acting principal, cancels each pending linked wake through the typed cancellation seam, writes the lifecycle event, and, when a key was supplied, records the terminal lifecycle idempotency result in one transaction.

### I8 — Retain-only rearm

Retain does not arm another generation. A later successful assignment insert for that child creates generation `n+1` as armed. Its later eligible idle transition creates the next obligation. A retired child remains terminal and rejects the assignment before any generation mutation.

### I9 — New work supersedes pending idle state

If assignment creation wins while generation `n` is pending, the same transaction marks request `n` superseded, resolves generation `n` as superseded, cancels each pending linked wake with truthful provenance, and creates generation `n+1` as armed. A stale retain or generation-bound retire for `n` returns `stale_disposition_generation` and changes no row.

### I10 — The generation fence precedes retire effects

A generation-bound retire verifies authorization, target state, current generation, pending request, and zero open assignments inside the canonical retire transaction before it evaluates leases, schedules any wake, creates a proof, changes a request, or changes a session. A failed fence returns `stale_disposition_generation` with the requested generation and current generation or `null`.

### I11 — Retirement stays terminal and atomic

When no critical lease blocks the target subtree, request-backed acknowledgment and the existing subtree retirement commit together. For each retiring session, a pending generation resolves request-backed retire; an armed generation resolves direct retire; no generation or request stays pending for a retired session. Existing descendant-first interruption, session state, queued-turn drain, broadcast, and post-commit reap behavior remains authoritative.

### I12 — Retirement interruption creates no redundant request

The exact `holder_retired` and `tightbeam:retirement` terminal assignment cause is ineligible for request creation. If the child has an armed generation, the retirement transaction uses the direct retire shape. If a request was pending before retirement began, the retirement transaction uses the request-backed shape and cancels its pending wakes.

### I13 — Lease deferral leaves the choice open

When a generation-bound retire sees one or more active subtree leases, the transaction leaves the child, subtree sessions, generation resolution, request status, and lifecycle idempotency ledger unchanged. It captures a sealed blocker proof, points the pending generation to that proof version, sets the request's current action deadline to the greatest blocker hard deadline, replaces the deadline reminder with one reminder due exactly then, writes `idle_worker_retire_deferred`, and returns `retire_deferred`. It does not schedule a generic `w_retire_...` intent wake. Because deferral is nonterminal, the caller can retry after blockers change or end and can reuse the key when it supplied one.

### I14 — Blocker proofs are immutable and linked

Each proof header records child, generation, version, request, acting principal, capture time, retry time, blocker count, canonical blocker digest, and sealed state. Each blocker row records ordinal, leased session key, reason, started time, expiry, hard deadline, and update time. The generation-to-proof pointer uses an enforceable composite foreign key. Sealed header and blocker rows reject update and delete. A sealed header rejects a later blocker insert.

### I15 — Deferral retries are idempotent

The blocker digest is lowercase hexadecimal SHA-256 over one UTF-8 JSON value serialized by the RFC 8785 JSON Canonicalization Scheme. The value is an array sorted by leased session key; each element is the six-position array `[leasedSessionKey, reason, startedAt, expiresAt, hardDeadline, updatedAt]`. A retry that observes the same request, generation, and blocker digest reuses the existing sealed proof version, current request deadline, and current reminder. A retry with a changed blocker set creates the next proof version, moves the request deadline and reminder to the new greatest hard deadline, and preserves earlier versions.

### I16 — Parent authority derives from rows

Request creation, request visibility, wake delivery, and each disposition action resolve the current responsible parent from same-owner lineage, then Main fallback. The generation preserves the parent selected at request creation as routing evidence; it does not freeze later authority. The mechanism does not use a role, display name, prompt text, or hard-coded topology. The owner user remains authorized. A foreign ancestor is a lineage boundary and receives no row or wake.

### I17 — Cause and principal are explicit

Each generation transition, request transition, wake cancellation, blocker proof, deferral, and retirement resolution records its durable cause and typed principal. Wake cancellation uses process requester `tightbeam:idle-worker-disposition`. It accepts only these added combinations:

- `superseded` + `decision_request` + `no_replacement`;
- `superseded` + `decision_request` + `replacement`;
- `obligation_disposed` + `decision_request` + `disposition`.

Other requester combinations remain byte-for-byte equivalent in behavior and shape.

### I18 — The reserved request has one action seam

Generic `rule`, `waive`, `revoke-waiver`, and `withdraw` operations refuse a request whose statute is `idle-worker-disposition` with code `lifecycle_action_required` and the exact remedy `Use retain --session <key> --generation <n> or retire --session <key> --generation <n>.` The lifecycle actions do not call generic allow/deny ruling logic.

### I19 — Activation is exact, transactional, and epoch-last

Schema owns activation. With no feature objects present, it validates the exact product `origin/0.1.8:4af89039` source shape, transactionally evolves the `wake_cancellations` requester CHECK and `wire_idempotency` lifecycle-result shape, creates every feature table, index, trigger, and epoch table, performs the deterministic backfill, validates all objects and rows, and inserts the feature epoch last. An injected failure after each statement rolls back the complete activation. A partial, malformed, missing-epoch, extra-epoch, invalid-link, count-mismatch, digest-mismatch, result-JSON mismatch, or unsealed-active-proof shape refuses boot with prefix `incompatible_idle_worker_disposition_v1:`. Startup does not repair or infer the shape.

### I20 — Existing observable contracts remain stable

Root Main behavior, never-worked active sessions, ordinary assignment prods, work-item brackets, effort decision requests, session-only manual retire, unrelated decision requesters, unrelated wake cancellation, and existing list keys retain their current behavior. The feature adds fields and events described in Architecture without removing or renaming an existing field.

### I21 — Terminal lifecycle replay is durable and full-input bound

For `retain` and generation-bound `retire`, a non-null idempotency key names one owner, operation, lifecycle input digest, and terminal canonical result. The transaction checks the ledger before current-generation or current-session-state refusal. A row with the matching digest returns its stored result JSON exactly, even after the request resolves or the child retires. A row with a different digest, or a legacy row whose digest is null, returns the existing idempotency-conflict response and changes no domain row. A successful lifecycle choice writes its digest and result JSON in the same transaction as its domain effects. A refusal or `retire_deferred` response writes no terminal lifecycle idempotency row. Manual retire without generation preserves replay for a legacy null-digest row. A manual call that meets a digest-bearing generation-bound row returns idempotency conflict.

## Architecture

### AR1 — Canonical binding and immutable review

This file is the fresh owner-authorized specification candidate in its sole durable commons. Its review binds the canonical repository path, exact commit, and SHA-256. A material amendment changes the hash and requires a new exact-byte review before implementation resumes.

The missing `art_d1b8493a` hash and its historical reviewed-clean verdict authorize no byte in this document.

### AR2 — Generation state

Schema adds `idle_worker_generations` with this logical contract:

| Field | Contract |
| --- | --- |
| `childSessionKey` | FK to `sessions`; part of primary key |
| `generation` | positive integer; part of primary key |
| `state` | `armed`, `pending`, or `resolved` |
| `armedAt` | nonnegative integer |
| `armedBasisKind` | `assignment_open` or `schema_activation` |
| `armedBasisId` | assignment id for `assignment_open`; null for `schema_activation` |
| `zeroAt`, `zeroBasisAssignmentId` | set only for request-backed pending or resolved rows |
| `initialDeadlineAt` | immutable finite deadline copied from the request at creation; null for armed and direct retire |
| `decisionRequestId` | unique FK to `decision_requests`; null for armed and direct retire |
| `promptWakeId` | FK to `wakes`; null for armed and direct retire |
| `parentSessionKey` | FK to `sessions`; null for armed and direct retire |
| `routingKind` | `lineage` or `main_fallback`; null for armed and direct retire |
| `lineageRung` | positive for lineage; null for Main fallback, armed, and direct retire |
| `resolution` | null until resolved; then `retain`, `retire`, or `superseded` |
| `resolvedAt`, `resolvedBy` | both set exactly when resolved |
| `resolutionCauseKind`, `resolutionCauseId` | durable source of resolution |
| `retireProofVersion` | nullable composite FK to one sealed proof for this generation |

A partial unique index permits one current row per child where state is armed or pending. A unique index on `decisionRequestId` permits one generation per request. CHECKs enforce the state shapes in I1-I15. Triggers reject delete, reject mutation of a resolved row, and reject identity or armed-basis changes after insert.

### AR3 — Native decision request

The eligible transition inserts the reserved statute row directly inside the assignment transaction. It sets:

- `kind='statute'`;
- `raiserId='process:tightbeam'` and null `raiserSessionKey`;
- the child's `ownerUserId`;
- `assignmentId=zeroBasisAssignmentId`;
- finite `raisedAt` and initial `deadlineAt` using the existing decision deadline configuration;
- `statuteName='idle-worker-disposition'`;
- the action key from Terms 10;
- a question that names the child, generation, and reason for attention;
- options JSON that displays retain and retire but grants no generic allow/deny effect;
- context JSON with `childSessionKey`, `generation`, `zeroBasisAssignmentId`, and canonical shell-safe commands;
- `status='open'`; and
- `parkWakeId` equal to the deadline reminder.

The request remains visible through `decision-requests` to the owner user and the current authorized disposition sessions. Escalation visibility joins the linked generation to its child, derives the current responsible parent and Main fallback at read time, and grants no visibility to the merely historical `parentSessionKey` when that session is no longer authorized. This change does not alter unrelated request visibility.

Retain and successful retirement set the request to `consumed`, store the lifecycle decision in the generation, set `consumedAt`, and preserve the request row. New work sets it to `superseded`. Neither path invents an allow/deny ruling.

### AR4 — Parent prompt and reminder

The initial prompt and reminder use deterministic IDs derived from `(childSessionKey, generation, requestId, wakeKind)`. Each wake stores `origin='process:tightbeam'`, the zero-basis assignment id for correlation, and the child owner. Delivery resolves the current active same-owner lineage target and then Main fallback in the delivery transaction. It records the original parent and the delivered target separately.

Before prompt construction, Gateway computes the Terms 23 shell-quoted word from the raw child session key. The prompt substitutes that quoted word after each `--session`. It never inserts a raw session key into a shell command. For example, raw key `agent:main:clawline:mike:main s_deadbeef` renders as `'agent:main:clawline:mike:main s_deadbeef'`, and raw key `a'b` renders as `'a'"'"'b'`. After POSIX shell parsing, the CLI receives the original key as one argument.

The prompt text is exactly:

```text
IDLE WORKER DISPOSITION: session <childSessionKey> has zero open assignments in generation <n>. Choose one: tightbeam retain --session <shellQuotedSessionKey> --generation <n>, or tightbeam retire --session <shellQuotedSessionKey> --generation <n>. Tightbeam will not choose or auto-retire.
```

The deadline reminder adds `Decision request <requestId> reached its attention deadline; re-read current rows before acting.` It repeats the same two commands. Delivery is information, not a decision.

### AR5 — Transaction-owned assignment seams

`Assignments.open_count_in_txn/2` accepts `DB.Txn` and runs the exact query from Terms 4 through `Txn.q/3`. Existing `Assignments.open_count/2` remains the outside-transaction API.

Each successful assignment insert calls the work-epoch open seam before commit. Each terminal close, surrender, revoke, and retirement interruption calls the terminal seam after the guarded assignment update and before commit. The seam receives the typed cause and principal already carried by the assignment transition.

The open seam performs these cases:

1. no current generation: insert generation 1 armed;
2. armed generation: leave it armed;
3. pending generation: supersede it and insert `n+1` armed;
4. resolved retain or superseded generation: insert `n+1` armed;
5. resolved retire or retired child: refuse through existing session state before generation mutation.

The terminal seam performs these cases:

1. open count greater than zero: leave the armed generation unchanged;
2. open count zero plus eligible idle transition: apply AR3 and AR4 atomically;
3. retirement interruption plus armed generation: apply direct retire resolution without request or wakes;
4. retirement interruption plus pending generation: leave final resolution to the canonical retirement seam in AR7;
5. no current generation: write no idle-worker row.

### AR6 — Retain

Gateway adds verb `retain`. Router accepts an exact session target and params `generation` plus optional idempotency key. CLI exposes:

```text
tightbeam retain --session <key> --generation <n> [--key <idempotencyKey>]
```

Generation is mandatory and positive. Retain returns the child session key, generation, request id, `decision='retain'`, and `state='active'`. AR9b defines exact lifecycle replay. A non-identical replay or a stale generation returns a deterministic refusal.

Both lifecycle actions use these observable refusal classes:

| Condition | Code and effect |
| --- | --- |
| CLI omits generation from retain or supplies a nonpositive/non-integer generation | exact retain usage error; no dispatch |
| wire generation is absent where mandatory, nonpositive, or non-integer | HTTP 400 `invalid_message`; no gateway call |
| target is absent or belongs to another owner | `not_found`; no domain-row change |
| target exists for the owner, but the caller is not the owner user, current responsible parent, or current Main fallback | `forbidden`; no domain-row change |
| generation is not the target's current pending generation, including an armed, resolved, or retired target | `stale_disposition_generation`, with `requestedGeneration` and nullable `currentGeneration`; no domain-row change |
| idempotency key names a different committed operation input | existing idempotency-conflict code and response; no domain-row change |

Authorization and mutation follow I7. Retain does not touch the harness process, session state, assignment rows, or work-item rows.

### AR7 — Retire integration and generation fence

CLI extends retire to:

```text
tightbeam retire --session <key> [--generation <n>] [--key <idempotencyKey>]
```

The CLI sends `generation` only when supplied. Router admits only a positive integer. Gateway preserves the existing response for calls without generation.

For a generation-bound call, Gateway performs the AR9b idempotency lookup and then validates I10 inside the retire transaction. It computes the canonical subtree and active leases once. With no blockers, it resolves each current child generation immediately before the corresponding session state transition, retaining the canonical descendant-first order. It uses the call's typed origin as `resolvedBy` and commits the terminal result through AR9b.

Authorization is checked against the requested target generation. A descendant generation resolved by the existing mandatory cascade does not require a second disposition call; it records the authorized target retirement as its resolution cause and the original call principal as `resolvedBy`.

For manual retire without generation, Gateway keeps existing lease deferral and `w_retire_...` behavior. When the manual call later commits retirement, it resolves any current idle-worker generation in the same transaction as described by I11-I12.

### AR8 — Critical-lease proof and reminder replacement

Schema adds `idle_worker_retire_proofs` and `idle_worker_retire_blockers`.

Proof identity is `(childSessionKey, generation, proofVersion)`. The header has a unique `(childSessionKey, generation, blockerDigest)` key. Blocker identity adds `ordinal`; a unique key also prevents the same `leasedSessionKey` twice in one proof.

The deferral transaction sorts active subtree leases by `sessionKey`, inserts an unsealed header, inserts the ordered blockers, computes and verifies count and digest from stored rows, seals the header, points the generation at the version, and replaces the reminder. Deferred composite foreign keys check at commit. Trigger errors use these exact messages:

- `idle-worker blocker proof is sealed`;
- `idle-worker blocker proof header is immutable`;
- `idle-worker blocker proof row is immutable`;
- `idle-worker generation requires a sealed blocker proof`.

The `retire_deferred` response adds `decisionRequestId`, `generation`, `proofVersion`, `proofDigest`, and `retryAt` to the existing ordered `deferred` list. `retryAt`, the proof header retry time, the updated request `deadlineAt`, and the replacement reminder due time are the same greatest blocker hard deadline. It leaves existing manual-retire responses unchanged.

### AR9 — Wake cancellation evolution

Schema treats the product `origin/0.1.8:4af89039` `wake_cancellations` table as source v1. If feature epoch is absent, it requires that exact table and trigger shape, builds the target table with the same eighteen columns plus only the I17 requester CHECK arm, copies each column without transformation, and proves:

1. source count equals target count;
2. `source EXCEPT target` over all eighteen columns is empty; and
3. `target EXCEPT source` over all eighteen columns is empty.

It then replaces the source table and recreates each current index and trigger in the feature activation transaction. Runtime `Wakes` adds the same requester and reason combinations to its closed maps. The transaction rolls back on any copy, proof, trigger, or shape failure.

### AR9b — Lifecycle idempotency ledger

The feature evolves `wire_idempotency` in the same Schema-owned activation. The target preserves the four legacy columns and primary key. It adds operation `retain` to the operation CHECK. It adds nullable `inputDigest`, `resultJson`, and `completedAt` columns. Existing rows copy without transformation and keep all three added columns null. Bidirectional `EXCEPT` over the four legacy columns and exact row counts prove preservation before the source table is replaced.

The target CHECKs admit these row shapes only:

1. `operation='retain'`: `inputDigest`, `resultJson`, and `completedAt` are non-null;
2. `operation='retire'`: the three added columns are either all null for a legacy manual result or all non-null for a generation-bound result;
3. another admitted operation: the three added columns are all null.

A non-null digest contains exactly 64 lowercase hexadecimal characters. A non-null completion time is a nonnegative integer. A non-null result is valid JSON. Lifecycle result JSON admits null, booleans, integers, UTF-8 strings, arrays, and string-keyed objects; it rejects floating-point numbers. Schema restart validation canonicalizes each non-null result with the same encoder and requires byte equality.

`lib/tightbeam/idempotency.ex` adds transaction-scoped lifecycle lookup and terminal put functions. For `retain`, the operation is `retain`; for both manual and generation-bound retirement, it is `retire`. A generation-bound call computes the Terms 22 digest before lookup. Lookup occurs inside the lifecycle transaction after caller-owner resolution but before target state, generation, request, or lease checks.

The lookup has exactly three outcomes:

1. no row: continue with authorization and lifecycle checks;
2. row with equal non-null `inputDigest`: decode `resultJson`, require its RFC 8785 canonical re-encoding to equal the stored bytes, and return that exact result without domain mutation;
3. row with a different digest or null digest: return the existing idempotency-conflict response without domain mutation.

On successful retain or successful generation-bound retirement with a key, Gateway RFC 8785-canonicalizes the exact public success response and inserts `sessionKey`, digest, canonical result JSON, and completion time in the domain transaction. A uniqueness race rereads the winning row and applies the same three outcomes. Refusals and lease deferrals insert no row. Manual retirement without generation continues to write the legacy `sessionKey`-only shape. A manual replay of a legacy row keeps its current response; a manual call that meets a digest-bearing generation-bound row returns idempotency conflict because the input modes differ. Other operations ignore the added columns and remain unchanged.

### AR10 — Activation, backfill, restart, and refusal

Feature-owned objects include the three idle-worker tables above, their indexes and triggers, the evolved wake-cancellation object, the evolved wire-idempotency object, and `idle_worker_disposition_epoch`.

On first activation, after object creation and before epoch insert, Schema selects active non-root sessions with at least one open assignment, ordered by `sessions.createdAt, sessions.sessionKey`. It inserts generation 1 armed with `armedBasisKind='schema_activation'`, null basis id, and `armedAt=activatedAt`. It inserts no row for a zero-open session, retired session, or root Main. It does not select a historical assignment as activation basis.

On restart with the epoch present, Schema validates exact object SQL and:

- one current generation per child;
- monotonic generations;
- request/action-key/generation reciprocal links;
- pending prompt and reminder links;
- request owner and child owner equality;
- current parent owner equality;
- proof composite links, sealed state, blocker count, order, and digest;
- lifecycle idempotency operation/digest/result shapes and canonical result JSON;
- no pending generation for a retired child;
- one exact epoch row with `cause='schema_activation'` and `principal='process:tightbeam'`.

Any violation refuses startup through the I19 prefix. Startup writes no repair row.

### AR11 — Observability and public guidance

`list` adds nullable `idleWorkerDisposition` to each session projection. When present it contains `generation`, `state`, `decisionRequestId`, `initialDeadlineAt`, `deadlineAt`, `resolution`, `resolvedAt`, `resolvedBy`, `retireProofVersion`, and `retryAt`. `deadlineAt` is the request's current action deadline. `retryAt` is null until a proof exists and otherwise equals the latest sealed proof's retry time. Existing keys and ordering remain unchanged. `decision-requests` exposes the same current `deadlineAt` from its authoritative row.

Lifecycle events use these names:

- `idle_worker_generation_armed`;
- `idle_worker_disposition_requested`;
- `idle_worker_disposition_retained`;
- `idle_worker_disposition_superseded`;
- `idle_worker_retire_deferred`;
- `idle_worker_disposition_retired`;
- `idle_worker_disposition_activation_refused`.

Each event detail carries child, generation, cause, and principal. Deferral adds proof version, digest, prior request deadline, and new `retryAt`/request deadline. Prompt, reminder, and cancellation rows remain the authoritative delivery evidence.

When the capability ships, `priv/guidance/operating-manual.md` adds this directive under `Hire help: spawn and retire`:

```text
When a worker reaches zero open assignments, Tightbeam opens one idle-worker decision request for its responsible parent. Read the current request before you act. Copy one command from the prompt; its session key is already quoted as one shell argument. Run `tightbeam retain --session '<key>' --generation <n>` to keep the worker, or `tightbeam retire --session '<key>' --generation <n>` to end it. Use the generation printed in the prompt; a stale generation refuses without effect. A critical lease can defer retirement until its hard deadline. Re-read the request and retry the same generation after the blocker ends. Tightbeam records the choice and does not choose for you.
```

The manual text lands in the same implementation commit as both verbs. A source guard asserts the exact heading, commands, generation refusal, lease retry, and no-auto-choice sentence. Before the verbs ship, guidance remains unchanged, satisfying wisdom 20.

### AR12 — Complete implementation boundary and custody

The implementation owns exactly these twenty-one paths as one reviewed unit. Entries 1-4 and 6-21 preserve every recovered path; entry 5 is the F1-required idempotency owner:

1. `specs/tightbeam/idle-worker-parent-disposition-v1.md` in `clickety-clacks/tightbeam-specs` (the canonical mapping of the recovered `shared/specs/tightbeam/idle-worker-parent-disposition-v1.md` path)
2. `lib/tightbeam/assignments.ex`
3. `lib/tightbeam/escalation.ex`
4. `lib/tightbeam/gateway.ex`
5. `lib/tightbeam/idempotency.ex`
6. `lib/tightbeam/schema.ex`
7. `lib/tightbeam/supervision.ex`
8. `lib/tightbeam/wakes.ex`
9. `lib/tightbeam/wire/router.ex`
10. `cli/src/args.rs`
11. `cli/src/dispatch.rs`
12. `priv/guidance/operating-manual.md`
13. `test/assignments_test.exs`
14. `test/escalation_test.exs`
15. `test/gateway_test.exs`
16. `test/router_test.exs`
17. `test/schema_shape_test.exs`
18. `test/supervision_test.exs`
19. `test/wakes_test.exs`
20. `test/cli_integration_test.exs`
21. `test/archetypes_test.exs`

The canonical spec path lives in the separate spec commons and is represented as path 1 for cross-repository assignment custody. Before product editing, the owner must open one code assignment containing this exact set and Tightbeam must accept it without `files_overlap`. The present overlap on `lib/tightbeam/supervision.ex` and `test/supervision_test.exs` under `asg_8429e570-f9a2-4510-bc60-87b65589c46f` blocks implementation but does not alter this spec.

### AR13 — Recoverable-authority delta

| Subject | Recoverable prior authority | Fresh spec ruling |
| --- | --- | --- |
| Artifact identity | `art_d1b8493a` was expected at SHA `f4f085d3...`, but its row has no content hash or archive home and its bytes are absent. | A new artifact identity and SHA bind this text. No old review transfers. |
| Revision 1 review | `art_3609851e` SHA `8c6d3dd4...` received changes-requested in `att_739eec29`; `art_88f15a24` SHA `e9f8959b...` records F1-F4. | Revision 1 remains immutable history. This revision changes only F1-F4 plus superseding homing and provenance rulings, and requires the existing sole linked review to assess its new exact bytes. |
| Product basis | Lost artifact used `6c13efcbe9e1ae247b8aa7e91a374015c74dc947`; revision 1 used historical `origin/0.1.x:ce686fa`. | Re-census source provenance only at product `origin/0.1.8:4af89039dbb55291383a657ef28700b1acd8122f`. No product bytes change in this assignment. |
| Branch | Historical cards named `main`; a later stale correction named nonexistent `0.1.9`. | The later owner no-`0.1.9` triage supersedes that correction. This spec lands from specs `origin/main:6b0aa95e` on `work/asg-9aaee147-idle-worker-respec`; product `origin/0.1.8` is provenance only. |
| Canonical home | Prior owner ruling named `shared/specs/tightbeam/idle-worker-parent-disposition-v1.md`; revision 1 remained in session scratch. | Org-local homing law maps the canonical authority to `clickety-clacks/tightbeam-specs:specs/tightbeam/idle-worker-parent-disposition-v1.md`. Scratch and artifact rows remain evidence pointers. |
| Parent decision surface | Prior changes-requested F1 required reuse of native `decision_requests` with deadline, prompt, reminder, and lifecycle resolution. | Preserved through reserved statute rows and lifecycle-specific retain/retire actions. |
| Retain-only rearm | `att_3150aa1e` ruled that only retain can later rearm through new work. | Preserved in I8-I9. |
| Terminal retirement | Prior goal and reviews rejected resurrection and automatic retirement. | Preserved in I6, I8, and I11. |
| Retirement interruption | Final reviewed F1 excluded `holder_retired/tightbeam:retirement` from request creation and allowed direct armed-to-retired resolution. | Preserved in I12 and AR5. |
| In-transaction count | Final reviewed F2 required `Assignments.open_count_in_txn/2` over `Txn.q/3`. | Preserved in AR5 against current DB non-reentry law. |
| Initial wakes | Final reviewed F3 limited initial prompt/reminder creation and made typed deferral the sole replacement. | Preserved in I4 and AR4/AR8. |
| Stale prompt race | Accepted B1 required optional retire generation fencing before lease or mutation. | Preserved in I10 and AR7; retain also requires the fence. |
| Lease deferral | Accepted I1 required bounded deferral, exact blocker snapshots, history, idempotency, and retry. | Preserved and made SQL-enforceable in I13-I15 and AR8; the request deadline now moves atomically with the reminder. |
| Wake provenance | Accepted cancellation F1 required truthful `tightbeam:idle-worker-disposition` requester and exact table evolution. | Preserved in I17 and rebased to the current product `origin/0.1.8:4af89039` eighteen-column source shape in AR9. |
| Proof integrity | Accepted proof F2 required sealed history and enforceable generation linkage. | Preserved in I14-I15 and AR8/AR10. |
| Schema activation | Prior F3/F5 required canonical Schema ownership, deterministic epoch basis, rollback, and malformed-shape refusal. | Preserved in I19 and AR10; source shape and branch basis are current. |
| Generic compatibility | Prior reviews required unchanged unrelated requesters, manual retire, root, and never-worked behavior. | Preserved in I20 and Acceptance A4/A8/A16. |
| Guidance | Accepted I2 required exact commands, authority, refusal, deferred retry, and source guard. | Preserved in AR11 with the current command forms. |
| Implementation paths | Recon `art_9af25de4` recovered the exact twenty-path boundary and two-path overlap. | All twenty recovered paths remain in AR12; F1 adds only `lib/tightbeam/idempotency.ex`, for a twenty-one-path boundary. The two named overlap paths remain a separate custody gate. |
| Verification | Prior artifact named Mix, Rust, packaging, real smoke, and exact-commit review gates. | Preserved and updated to the exact product `origin/0.1.8:4af89039` CI order, clean baseline/after counts, packaged-binary smoke, and frozen-tip Linux+macOS review in A18-A20. |

### AR14 — Changes-requested closure ledger

| Finding | Revision 2 closure |
| --- | --- |
| F1 — terminal full-input idempotency was unspecified and `lib/tightbeam/idempotency.ex` was outside custody | Terms 22, I7, I13, I21, AR6-AR7, AR9b, AR10, AR12, A5, A10, A12, and A15 define digest-bound stored-result replay, defer-without-record behavior, legacy manual compatibility, schema evolution, tests, and the added owner path. |
| F2 — lease deferral did not rule whether `decision_requests.deadlineAt` changes | Terms 16-17, I4-I5, I13-I15, AR2-AR3, AR8, AR11, A7, A10, and A11 make the request deadline, reminder due time, and latest proof retry time equal in one transaction while retaining `initialDeadlineAt`. |
| F3 — repository gates omitted public-rule, fresh release CLI, and frozen-tip two-platform CI | Assumption 12 and A18-A20 bind the exact current CI order, both local baseline/after runs, and successful Linux+macOS checks for the frozen commit. |
| F4 — generated prompt commands did not shell-quote session keys | Terms 23, AR3-AR4, AR11, and A17 define one POSIX quoting transform, use it in both generated commands, and test the real custom-key grammar through a shell. |

### AR15 — Prior clause preservation ledger

| Historical reviewed clause group | Preservation in this spec |
| --- | --- |
| Goal: one obligation, parent choice, retain rearm, terminal retire | Goal; I1-I12; A1-A9 |
| Initial F1-F5: liveness, deferred retire, Schema ownership, canonical form/home, deterministic activation basis | I2-I6, I13, I19; AR1, AR3-AR4, AR8-AR10; A2-A4, A10, A14-A15 |
| B1: generation-fenced retire | I10; AR7; A8, A12 |
| I1: durable lease blocker proof | I13-I15; AR8; A10-A11 |
| I2: exact manual contract | AR11; A16-A18 |
| Cancellation F1: truthful requester and exact evolution | I17; AR9; A6-A7, A16 |
| Proof F2: immutable history and composite linkage | I14-I15; AR8-AR10; A10-A11, A15 |
| Final F1: direct retire, no redundant request | I11-I12; AR5/AR7; A2, A9 |
| Final F2: transaction-handle open count | Terms 4; I3; AR5; A13 |
| Final F3: initial-only wakes and sole typed replacement | I4; AR4/AR8; A2, A7, A10 |
| Reviewed invariants I1-I19 | I1-I21. I20 holds the compatibility set that prior I19 carried; I21 closes revision-1 F1 without weakening an accepted invariant. |
| Reviewed acceptance A1-A20 | Acceptance A1-A20 below preserves the same behavioral sequence and updates source/toolchain evidence only. |

## Acceptance

Each acceptance case runs on a fresh disposable database unless it explicitly tests restart or activation of a captured fixture. Tests use injected time, direct due-row control, or synchronous fire/drain seams. They do not use sleep, widened timeout, or a production work row.

### A1 — Arm and deduplicate

Given active non-root child `C` has no generation, when assignment `A1` opens, then generation 1 is armed with basis `A1`. Given `A2` opens while `A1` remains open, then no second generation appears. Given concurrent assignment opens, then one transaction creates generation 1 and both assignments commit against that generation.

### A2 — Eligible last close and retirement exclusion

Given `C` has armed generation 1 and one open assignment, when completion, surrender, or revoke closes that assignment, then the same transaction commits zero open assignments, one reserved request, one prompt, one reminder, and one pending generation. Run each terminal kind as a separate fixture. Given retirement interruption closes the last assignment with `holder_retired/tightbeam:retirement`, then no request or wake appears and generation 1 resolves direct retire in the retirement transaction.

### A3 — Restart and duplicate delivery

Given the request transaction commits and the gateway stops before wake delivery, when the same database restarts, then exact-shape validation passes and the two pending wakes remain deliverable. Given the initial prompt or reminder is delivered at least once, when scheduler reconciliation runs again, then no second turn is admitted for the same wake id and no second request appears.

### A4 — Root and never-worked behavior

Given built-in Main closes its last assignment, then no idle-worker generation, request, or wake appears. Given an ordinary child has zero open assignments but no assignment has opened since activation, when sweeps and restarts run, then no idle-worker row appears. Given an active child has open work at activation, then one schema-activation armed generation appears and its later last close opens one request.

### A5 — Retain authority, idempotency, and refusal

Given pending generation 1 addressed to parent `P`, when `P` runs retain with key `K` and generation 1, then generation, request, wakes, event, and the AR9b terminal row commit atomically and `C` remains active. After any later state change, replay the same owner, operation, key, child, and generation; it returns byte-identical stored result JSON. Reuse `K` with another child or generation; it returns the existing idempotency-conflict response with zero effects. Inject failure before each transaction statement and prove neither domain effects nor the terminal row commits alone. Run owner user and Main fallback success fixtures. Run foreign target, unrelated same-owner session, process principal, retired parent, wrong child, nonpositive generation, stale generation, legacy-null-digest, and conflicting idempotency fixtures; each returns the exact AR6 or AR9b refusal and changes no domain row.

### A6 — New work supersedes pending

Given generation 1 is pending, when assignment `A2` opens first, then generation 1 and its request become superseded, each pending linked wake has one truthful cancellation row, and generation 2 becomes armed in the assignment transaction. A later retain or generation-bound retire for generation 1 returns `stale_disposition_generation` with zero effects.

### A7 — Replacement reminder provenance

Given a pending reminder exists and a generation-bound retire observes a changed blocker set, when deferral commits, then the replacement reminder is inserted before the old reminder cancels, `wake_cancellations` records requester `tightbeam:idle-worker-disposition`, reason `superseded`, source `decision_request`, outcome `replacement`, and the request points only to the replacement. The updated request `deadlineAt`, replacement due time, proof `retryAt`, and greatest blocker hard deadline are equal. The generation's `initialDeadlineAt` remains byte-identical. Inject failure between each write and prove all deadline, reminder, cancellation, proof, and pointer rows roll back. Given no replacement is needed during retain, supersede, successful retirement, or same-digest deferral, then any pending wake cancellation records the matching `no_replacement` or `disposition` combination from I17 and the current request/reminder pair remains unchanged where applicable.

### A8 — Stale retire fence and manual compatibility

Given a prompt for generation 1 and current generation 2, when an authorized parent runs retire with generation 1, then the response is `stale_disposition_generation`; active leases, generic retire-intent wakes, proof rows, requests, sessions, assignments, lifecycle events, and idempotency rows remain unchanged. Given the same caller omits generation, then the current manual-retire contract executes unchanged, including its existing critical-lease response, generic intent wake, and replay of legacy null-digest rows. Reuse a key first committed by one retire input mode from the other mode; the call returns idempotency conflict and changes no domain row.

### A9 — Successful retirement and race

Given pending generation 1, no active subtree lease, and authorized parent `P`, when `P` runs generation-bound retire with key `K`, then request consumption, generation resolution, descendant-before-ancestor cascade, assignment interruption, session retirement, queue drain, events, and terminal result row commit once. Replaying `K` returns the stored success after retirement. Given manual retire races the eligible last close of an armed generation, serialization yields one of two outcomes: the eligible close wins and retire consumes its request, or retire wins and the interruption creates no request. No committed outcome leaves a pending request for a retired child, a pending initial prompt after the choice, or a terminal idempotency row without its matching lifecycle outcome.

### A10 — Deferred retirement

Given pending generation 1 and active leases on child `C` and descendant `D`, when `P` runs generation-bound retire with key `K`, then the response is `retire_deferred`, sessions and request remain open, no generic retire-intent wake or terminal idempotency row appears, proof version 1 contains the sorted exact leases, and request deadline plus sole reminder due time equal the greatest hard deadline. Replay `K` while the blocker digest is unchanged; no proof, reminder, deadline, or terminal ledger row changes. Change the blockers and retry `K`; version 2 and its new atomic deadline/reminder replace version 1 as current evidence while version 1 stays immutable. Given the blockers end and `P` retries `K` for generation 1, then successful retirement consumes the same request, retains prior proofs as history, and records the terminal result. A later identical replay returns that exact result.

### A11 — Proof history and mutation rails

Given proof version 1 is sealed, execute direct SQL attempts to add a blocker, update and delete each blocker, update and delete the header, point the generation to a missing or unsealed header, commit a wrong count, commit a wrong digest, and reuse an ordinal or leased session key. Each operation aborts with the specified constraint or trigger message. Given a changed blocker set on retry, then version 2 seals, the generation points to version 2, request deadline and reminder move to version 2 `retryAt`, and version 1 remains byte-identical and queryable. Given the same blocker set, then no version 2 appears; the request deadline, reminder due time, proof `retryAt`, and list `retryAt` remain unchanged.

### A12 — Concurrent lifecycle choices

Given one pending generation, run retain versus retain with the same and different keys, retain versus generation-bound retire, two generation-bound retires with the same key and with different keys, new assignment versus retain, and new assignment versus retire behind deterministic barriers. In each pair one serialized current-state result wins. A matching committed key returns its byte-identical stored result before stale-state checks; a different input under the same key returns idempotency conflict; an uncommitted key can return `stale_disposition_generation`. Request, generation, wakes, proofs, terminal ledger, assignment count, and session state match one complete legal outcome. A deferred retire never becomes the terminal winner and remains retryable under its key.

### A13 — Transaction-scoped open count

Instrument `Assignments.open_count/2` to fail if called from the DB owner. Given an eligible close, assignment open, revoke, surrender, and retirement interruption, then each transaction completes through `open_count_in_txn/2` and the exact `Txn.q/3` query. A source guard rejects a terminal seam that calls the outside-transaction function.

### A14 — Parent chain and cascade

Given immediate parent `P1` is inactive, same-owner ancestor `P2` is active, and Main `M` is active, then request creation records `P2` and lineage rung 2. Given no active same-owner ancestor, then it records `M` and Main fallback. Given a foreign-owner ancestor appears, then no foreign wake or visibility row appears and routing falls back to `M`. Given the recorded parent becomes inactive while the request remains pending, then the newly current responsible parent can list and act on the request, while the historical parent cannot. Given a parent retirement cascades through children, then each current child generation resolves retire descendant-first and no idle request is created by retirement interruptions.

### A15 — Activation, interruption, and restart refusal

From the exact product `origin/0.1.8:4af89039` source database shape, inject failure after each activation statement and after backfill but before epoch insert. Each run rolls back to the exact source shape and rows. A full run preserves all eighteen wake-cancellation columns and every four-column legacy idempotency row by count and bidirectional `EXCEPT`, preserves other requester and idempotency behavior, creates exact feature objects, backfills only active non-root sessions with open assignments, and inserts the epoch last. Restart then succeeds. Partial object sets, altered SQL, missing or duplicate epoch, invalid request link, pending retired child, unsealed active proof, count mismatch, digest mismatch, noncanonical result JSON, floating-point lifecycle result, partial lifecycle-result columns, lowercase-digest violation, malformed lifecycle ledger row, and broken composite link each refuse with `incompatible_idle_worker_disposition_v1:` and perform no repair.

### A16 — Compatibility and source guards

Run the existing focused tests for assignments, escalation, gateway retirement, schema shape, supervision, wakes, router, CLI integration, and archetype/manual projection. Their existing assertions pass unchanged except assertions that add the new documented fields or commands. A source guard proves unrelated requester maps and CHECK arms remain present; generic statute/effort request behavior remains unchanged; only the reserved idle statute returns `lifecycle_action_required`; root, never-worked, ordinary prods, work-item brackets, and manual retire preserve their observable behavior.

### A17 — CLI and operating manual

CLI parser and dispatch tests prove exact retain syntax, optional retire generation, positive integer checks, session-only target, identity fields, idempotency key, generated JSON, help text, and error text. Router tests prove the same wire contract. Prompt tests use real `Org.custom_session_key/2` values containing spaces and a fixture containing an embedded single quote; each generated command uses the Terms 23 transform. Execute each command through a POSIX shell into an argument-capturing CLI fixture and prove `--session` receives exactly one value byte-equal to the raw key. Prove no prompt command contains the unquoted raw key. `test/archetypes_test.exs` proves the exact AR11 manual directive appears once under `Hire help: spawn and retire`, after both commands exist, and that no earlier or alternate guidance text teaches an unbuilt command.

### A18 — Repository and toolchain gates

On an unmodified clean product `origin/0.1.8` worktree at exact implementation-base commit selected by the owner, record the commit and run these commands in this order:

```text
python3 scripts/verify_shipped_privacy.py
python3 scripts/verify_public_rule_facts.py
elixir --version
rustc --version
(cd cli && cargo build --release)
mix deps.get
mix compile
mix format --check-formatted
scripts/verify_mix.sh
(cd cli && cargo fmt --check)
(cd cli && cargo test)
sh packaging/assemble.sh
```

Run each parenthesized CLI command from the repository root. The release CLI build must start without a restored `cli/target` tree and must complete before any Mix command, matching current CI's fresh-binary prerequisite. Remove inherited `TIGHTBEAM_*` and `RELEASE_*` variables for Mix commands as current repository guidance requires. Record baseline Mix and Rust counts. After implementation, run the same ordered gates on the frozen implementation tip and record after counts. A missing tool, dependency, release CLI, supported platform, or credential is a named blocker; no substitute command counts.

### A19 — Real disposable package smoke

Build the package from the frozen implementation tip with `sh packaging/assemble.sh`. Install that exact tarball into a new disposable prefix. Start the packaged gateway against a new disposable base directory with the packaged gateway binary, and drive the packaged CLI over its real HTTP dispatch seam. Create an owner Main, parent, child, and descendant; open and close real assignment rows; capture the real request, generation, wake, turn, proof, cancellation, session, and lifecycle rows for these journeys:

1. eligible idle, retain, new work, second eligible idle, successful generation-bound retire;
2. eligible idle, real critical lease, deferred retire, deadline reminder, lease end, retry, successful retire;
3. stale generation refusal after new work;
4. manual retire without generation;
5. root and never-worked exclusions.

The smoke records package path and SHA, source commit, CLI and gateway paths, toolchain versions, commands, row captures, and teardown. It targets no production database, work item, assignment, session, or credential. Passing unit tests without this package smoke does not satisfy A19.

### A20 — Frozen-tip review and handoff

After A1-A19 pass, freeze and push one bounded product implementation commit based on the owner-selected `origin/0.1.8` source tip. Record the canonical spec repository/path/commit/SHA, exact twenty-one-path custody and diff, baseline and after gates, package artifact SHA, smoke evidence, and current overlap resolution. Open or update one pull request for that exact frozen commit. The required GitHub `ci` checks for both `linux` and `macos` must succeed on that same commit; a later push invalidates the evidence. One independent exact-commit review must compare that frozen tip with this reviewed spec and the real smoke. Implementation completion requires its `reviewed-clean` verdict. Merge, release, deployment, service restart, and cross-port remain separately owner-authorized actions.

## Open Questions

None.

The owner settled fresh-respec authority, canonical home, source provenance, retain-only rearm, terminal retirement, complete path boundary, custody separation, review count, and missing-artifact treatment. Implementation remains blocked until this exact canonical revision receives the sole linked fresh `reviewed-clean` verdict and the complete twenty-one-path assignment clears the separate overlap gate.
