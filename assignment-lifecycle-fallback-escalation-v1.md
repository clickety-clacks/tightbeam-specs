# Assignment lifecycle fallback escalation v1

Status: MVP contract; implementation is forbidden until an independent reviewer files `reviewed-clean` against this exact content hash  
Work item: `wi_3d6d13a0-c4cf-4370-88a1-b407c41ff7c1`  
Authority assignment: `asg_3fce3846-487e-496a-af79-6e2114ff39ab`  
Product owner assignment: `asg_0bd4c0ab-68a0-463e-92c4-e5d11a8135c5`

## Invariants

### INV-01 — A lifecycle source reaches an agent before Main

For each eligible source, Tightbeam MUST first use any correlated existing route and the source's normal resolver result, then the recorded agent expecter and agent owner. A failed-turn source keeps Bubble's non-Main `sessions.operationalParent` climb. A completed-assignment source keeps the completion domain's explicit report-to route when declared and otherwise its `sessions.spawnedBy` parent route. Other disposition sources keep their own normal resolver. Tightbeam MAY write one report to the owning user's personal Main stream only when no such route remains pending or able to accept a turn.

Main is a report audience. Main MUST NOT be inserted into the agent-candidate list and MUST NOT receive a lifecycle model turn.

### INV-02 — Model choice remains agent judgment

The lifecycle mechanism MUST NOT read Kung Fu prose, select a model, switch a model, spawn a replacement, infer an activity, or decide that a model list is exhausted.

A supervising agent that receives a failed-turn notice applies its own currently served Kung Fu model-selection row. The agent MUST try each allowed candidate in that row once, in order. A refused candidate or a harness that is out of tokens advances to the next candidate. Nothing off-list is tried.

When the ordered row ends, the supervising agent records the attempted rungs, evidence, and consequence as a capability block on the affected assignment and schedules a re-check. Separable work continues. Model-list exhaustion creates no lifecycle report, and Main is never a model fallback.

### INV-03 — Lifecycle does not change custody

The feature MUST NOT change a work-item owner, assignment opener, assignment holder, `sessions.spawnedBy`, `sessions.operationalParent`, an explicit report-to declaration, role binding, or review relationship. It MUST NOT create a work item, assignment, session, or replacement model session.

### INV-04 — Rows, not prose, determine routing

Routing MUST use stored identifiers and typed rows. It MUST NOT parse prompts, assignment subjects, attest notes, model output, display names, error prose, or artifact contents. The only parsed strings are the closed, versioned identifiers defined in TERM-01.

### INV-05 — One source has one stable episode

Each eligible source has one derived episode id. Repeated callbacks, process crashes, restarts, and concurrent recognition MUST reuse that id. Each `(episode, recipient)` has at most one notice turn. Each episode has at most one Main report.

The typed source form selects one source-specific normal resolver. A retry MUST derive the same resolver from that stored source form and MUST NOT invoke another source's resolver, even when `spawnedBy` and `operationalParent` name different sessions.

This MVP does not coalesce several sources into a mutable per-assignment episode.

ARC-12 permits one predecessor-authored legacy marker beside the episode's one TERM-09 report during one rollback/reactivation cycle. That untyped predecessor marker is not a lifecycle report and never changes the derived episode state.

### INV-06 — A Main report is its own atomic state

The report state and the visible high-attention Main marker MUST be one `messages` row. The report's lifecycle event MUST commit in the same SQLite transaction. A crash cannot commit a reported state without its readable marker or a marker without its reported state.

### INV-07 — Existing production domains stay distinct

The change MUST preserve:

- assignment-open routing-wake cancellation;
- Bubble's existing `operationalParent` climb for failed turns;
- completion's existing explicit report-to or `spawnedBy` route;
- supervision of stalled open assignments; and
- the zero-open-assignment slate wake.

A routing-wake cancellation is never a lifecycle source. Bubble retains its current behavior byte-for-byte for unassigned turns and pre-MVP rows. For an eligible assigned turn, Bubble performs its normal non-Main lineage climb before the lifecycle mechanism tries other recorded agent edges. A correlated supervision or slate route counts as existing coverage and suppresses a duplicate lifecycle notice or report.

### INV-08 — Attribution and content are truthful

Every feature-authored event, turn, and marker uses principal, origin, or sender `process:tightbeam`. A feature-authored row MUST NOT impersonate a user or role. Each row MUST carry the identifiers applicable to its purpose; the joined source, attempt, and report rows together expose source, assignment, work-item, relation, and recipient correlation. They MUST NOT copy the original prompt, error text, model output, assignment subject, attest note, artifact content, credential, or token.

### INV-09 — Existing shape and rows remain valid

The implementation MUST add no table, column, index, trigger, or shape stamp. The database stamp remains `coordination-fabric-v1-phase1-v5`; the existing exact `coordination-fabric-v1-phase1-v4` to v5 upgrade remains owned by the baseline schema seam. Existing rows, including `assignment_reopenings`, remain readable and unchanged after that existing upgrade. Rows without an `assignment_lifecycle_source_v1` event are historical and MUST NOT be backfilled or reported.

### INV-10 — No lifecycle row is deleted

The product MUST expose no lifecycle delete or repair operation. Existing deletion and retention behavior for turns, wakes, messages, lifecycle events, assignments, assignment reopenings, sessions, and work items does not change.

## Goal

### GOAL-01

Close the proven silent-loss gap for new assigned failed turns and accepted assignment dispositions. A capable recorded agent sees the source first. If no agent route succeeds, the owning user's Main receives one durable, model-independent action-needed marker.

### GOAL-02

Preserve the current Kung Fu model-exhaustion boundary: the supervising agent records an assignment capability block and schedules a re-check. The lifecycle mechanism does not report model unavailability to Main. Ordinary Main fallback depends only on whether a recorded non-Main agent route delivered.

### GOAL-03

Prove the behavior with the three reviewed lifecycle specimens, a separate Fable routing-cancellation specimen, deterministic fault/race tests, and packaged real-harness smoke.

Subtraction decision: DELETE wins for the prior activation membership, source cursor, recovery cursor, episode table, attempt table, receipt tables, health subsystem, and migration engine. Existing atomic rows already represent the MVP. Accepting silent loss would violate GOAL-01; adding a second persistence lattice would violate the current no-shape-migration ruling and the substrate's own agent-first principle.

## Non-Goals

### NG-01

This feature does not judge correctness, urgency, importance, staffing, or the next action.

### NG-02

This feature does not implement model ring-down. Agents apply the Kung Fu policy through existing spawn, assignment, wake, and credential flows.

### NG-03

This feature does not add HarnessHealth, provider suppression, model availability state, a model retry counter, or a model-selection API.

### NG-04

This MVP does not backfill historical terminals, cover terminal sources committed while the rollback predecessor runs, or coalesce multiple source episodes. It does not deduplicate an untyped legacy Main marker written by the rollback predecessor against the current version's typed TERM-09 report. ARC-12 bounds that accepted degradation to one duplicate during one rollback/reactivation cycle. These cases can be extended later without changing this MVP's identifiers.

### NG-05

This MVP does not add a continuously running source sweeper, fairness cursor, permanent-failure ledger, transition ledger, or lifecycle mutation command. Recognition uses existing transaction hooks, terminal replay, and ARC-12's one finite activation reconciliation.

### NG-06

This MVP does not add structured marker columns or require client-specific rendering. Unaware clients display readable marker text.

### NG-07

This feature does not alter assignment-open routing cancellation, wake-cancellation attribution, Bubble for unassigned turns, supervision thresholds, slate timing, work-item disposition, or a source domain's normal resolver. Lifecycle consumes that resolver's typed recipient result.

## Terms

### TERM-01 — Source and episode

The eligible source forms and stable identifiers are:

| Source | Source id | Eligibility |
|---|---|---|
| assigned terminal turn | `turn:<seq>` | `turns.assignmentId` is non-null; status is `failed` or `failed_unknown`; `requestRef` does not begin `assignment-lifecycle:`; the terminal transaction wrote the ARC-01 source event |
| assignment disposition | `assignment:<assignmentId>:<outcome>:<generation>` | outcome is `completed`, `surrendered`, or `revoked`; `generation` is the positive base-10 integer defined below; the closing transaction wrote the ARC-01 source event |
`episodeId` is `ale:<sourceId>` for a turn or assignment source.

For an assignment close, `generation = 1 + COUNT(assignment_reopenings.id WHERE assignmentId = <assignmentId>)`, evaluated in the closing transaction after all earlier reopenings and before the source event is inserted. The first close is generation `1`. Reopening records that close in `assignment_reopenings`; the next close is therefore the next generation even when its outcome repeats. The identifier uses canonical decimal digits with no sign and no leading zero.

The assignment source id contains the assignment id, outcome, and close generation once as canonical correlation and idempotency identity. Those components are not copied into another feature-owned persistence field.

After commit, the stored source-event subject is authoritative. A projection MUST NOT recompute an older generation from the assignment's later reopenings.

A turn whose `requestRef` begins `assignment-lifecycle:` is an attempt, not a new source. A `canceled` turn and a routing-wake cancellation are not sources.

### TERM-02 — Audience

The audience is `work_items.ownerUserId` when the assignment has a work item. Otherwise it is the immutable `sessions.ownerUserId` of the assignment holder. Its report stream is `Tightbeam.Org.personal_session_key(audienceUserId)`.

Agent routing does not depend on resolving the audience. If neither row yields one user after all non-Main routes terminate non-delivered, recognition returns the named error `lifecycle_audience_missing`; it does not invent an owner or suppress an available agent route.

### TERM-03 — Expecter edge

The agent expecter is `assignments.openedBySession`. `openedByUser` is recorded source context but is never a model-turn recipient.

### TERM-04 — Agent-owner edge

The agent-owner assignment is the one assignment attributed to the expecter's turn at `assignments.openedAt`:

- the turn belongs to the expecter session;
- `startedAt <= openedAt`;
- `endedAt` is null or `endedAt >= openedAt`;
- the turn has a non-null `assignmentId`; and
- that assignment has the same non-null `workItemId` as the subject assignment.

The edge recipient is that assignment's `holderKey`. More than one matching turn is an invariant error; no match produces a null edge. The immutable turn and assignment rows are the edge record. No feature table copies them.

### TERM-05 — Source-specific normal route

A source-specific normal route is the ordered recipient result of that source domain's typed resolver. Lifecycle consumes the result; it does not reinterpret one parent field as another.

- For an assigned failed-turn source, Bubble walks active `sessions.operationalParent` ancestors nearest-first, bounded at 32 hops. Bubble owns that walk, and lifecycle creates no second climb. Its visited set is derived from exact `bubble:<rootTurnSeq>` attempt rows; a repeated recipient or the end of the bound is exhaustion, not a duplicate enqueue.
- For a completed-assignment source, the completion resolver uses its typed explicit report-to declaration when one exists. Otherwise it seeds its existing active, same-owner parent route from the holder's immutable `sessions.spawnedBy`. Lifecycle consumes those ordered recipients as `source_route` candidates.
- For surrendered or revoked assignment sources, lifecycle consumes the existing outcome-specific resolver result. It does not start a `spawnedBy` or `operationalParent` walk.

The typed source form selects the resolver kind. The resolver's ordered recipients are deduplicated with every existing-route, expecter, and agent-owner recipient for that episode. No resolver kind, recipient list, mutable lineage state, or universal parent edge is persisted by lifecycle.

### TERM-06 — Existing route

Existing coverage is one of:

- a Bubble notice whose cause is the root failed turn;
- an exact supervision controller wake or turn correlated by the existing sidecar to that root turn and assignment; or
- the work item's `slateWakeId` created in the same assignment-close transaction.

Queued or running coverage keeps the episode `resolving`. Delivered coverage resolves it. A terminal non-delivered route permits the next candidate. A pending slate wake is coverage because its existing domain intentionally routes the zero-assignment decision to Main.

An exact correlated non-delivered route also counts as a prior attempt by its recipient. Lifecycle MUST NOT send that recipient a second notice for the same episode.

### TERM-07 — Lifecycle notice

A lifecycle notice is a model turn to a non-Main source-route, agent-expecter, or agent-owner recipient. Its identifiers are:

- `wakeId = assignment-lifecycle:<sourceId>:<relation>:<sessionKey>`;
- `clientMessageId` equal to `wakeId` and `deviceId = process:tightbeam`;
- `requestRef = assignment-lifecycle:<sourceId>`;
- the source assignment id in `turns.assignmentId`; and
- the source work-item id in `turns.jobRef` when present.

For a failed-turn source, the prompt is exactly:

```text
Assignment lifecycle source <sourceId> on assignment <assignmentId> needs supervision. You are its recorded <expecter|agent owner>. Inspect the durable rows and decide the next action. If the failure is model availability, use your currently served Kung Fu activity row: try each allowed candidate once in order; use nothing off-list; if the row ends, record the attempted rungs, evidence, and consequence as a capability block on the affected assignment and schedule a re-check. Do not report to Main merely because the row ended. Tightbeam did not change ownership.
```

The prompt contains no source error or assignment subject.

For an assignment disposition, the prompt is exactly:

```text
Assignment lifecycle source <sourceId> on assignment <assignmentId> needs supervision. You are its recorded <source route|expecter|agent owner>. Inspect the durable rows and decide the next action. Tightbeam did not change ownership or parent routing.
```

### TERM-08 — Derived episode state

The read projection derives one state; no mutable lifecycle state row exists:

| State | Row predicate |
|---|---|
| `resolving` | source event exists and none of the four terminal predicates below matches; this includes a queued/running route, an untried eligible agent edge, or a terminal non-delivered attempt awaiting callback or activation reconciliation |
| `resolved_existing` | a correlated existing route delivered or a same-transaction slate wake covers an assignment close |
| `resolved_agent` | a source-route, expecter, or agent-owner lifecycle notice delivered |
| `reported_main` | the deterministic ARC-07 Main marker exists |
| `refused` | ARC-10's deterministic refusal event exists |

The projection applies the predicates in this first-match order: `refused`, `reported_main`, `resolved_existing`, `resolved_agent`, `resolving`. Refusal wins over a route that appears later. Lifecycle writes forbid terminal-state overlap; another domain may add a route after refusal, but it cannot change the episode state.

`resolving -> resolved_existing | resolved_agent | reported_main | refused` is allowed. No transition leaves a terminal state.

### TERM-09 — Main report marker

The Main report is one `messages` row with role `assistant`, sender `process:tightbeam`, attention tier `high`, device id `process:tightbeam`, and client message id `assignment-lifecycle:main:<sourceId>`. Its first line is `[assignment lifecycle]`.

The ordinary exhausted-routing body is exactly:

```text
[assignment lifecycle]

Assignment lifecycle source <sourceId> on assignment <assignmentId> needs your action. No recorded non-Main agent route delivered. Tightbeam did not change ownership.
```

### TERM-10 — Capable agent

An agent is capable only when its correlated existing-route or lifecycle-notice turn reaches `delivered`. An active session row permits an attempt; it does not prove capability.

## Assumptions

### ASM-01

`turns`, `assignments`, `assignment_reopenings`, `sessions`, `work_items`, `wakes`, `messages`, and `lifecycle_events` retain committed rows needed by the derived projection.

### ASM-02

SQLite transactions and the existing unique indexes on `turns.wakeId` and `(messages.sessionKey, messages.deviceId, messages.clientMessageId)` provide atomicity and idempotency.

### ASM-03

The existing terminal publication reconciler enumerates a terminal turn whose `publishedAt` remains null after a crash and invokes the configured terminal hooks. At the implementation baseline, the live lane acknowledges publication before its asynchronous recognition hook; ARC-11 changes that ordering for eligible lifecycle terminals.

### ASM-04

The current Bubble root correlation is `requestRef = bubble:<rootTurnSeq>`. Supervision sidecars and slate wake ids retain their current exact correlation fields.

### ASM-05

The controlling implementation baseline is `main@8eeccbd6dfd221fe9d105783459637fb7a17ea83`, database shape `coordination-fabric-v1-phase1-v5`, CI file SHA-256 `1ccc8176ca9a8b9c2a677eaf31723e3c9602f6790ed8baccb945a5bc2d000e57`, and supported application rollback baseline `8eeccbd6dfd221fe9d105783459637fb7a17ea83` on the same v5 store. Historical commit `b8e6c47e4631da8345aaf8c6ab73b0858e630bf6` is a v3 binary and MUST refuse a v5 store; it is not a runnable rollback predecessor.

### ASM-06

At the ASM-05 baseline, `agentic-engineering` Kung Fu's `preferred-models.md` and `orchestrator.md` define the ordered candidates, assignment capability block, and re-check policy. The live catalog decides whether each named candidate is selectable. That guidance may change without a product database migration.

## Architecture

### ARC-01 — Source admission and persistence

Add lifecycle event kind `assignment_lifecycle_source_v1`. It is written only inside the transaction that wins the terminal source transition. The turn path excludes `requestRef` values beginning `assignment-lifecycle:` so a failed notice remains an attempt in its original episode.

The event has this exact existing-table shape:

| `lifecycle_events` field | Value |
|---|---|
| `ts` | the terminal transaction clock |
| `kind` | `assignment_lifecycle_source_v1` |
| `subject` | TERM-01 source id |
| `detail` | JSON object below |

```json
{
  "schemaVersion": "assignment-lifecycle-source-v1",
  "workItemId": null,
  "principal": "process:tightbeam"
}
```

`workItemId` is the exact work-item id string when the assignment has one; otherwise it is JSON null.

The event stores no prompt, error, assignment-subject text, note, outcome copy, model response, or credential. Its presence is the post-activation eligibility boundary. An existing terminal row without this event is historical.

Before inserting, the terminal transaction checks for the exact event kind and subject. If it already exists, the source retains its original episode and the transaction writes no second source event. Every such check runs inside the existing single-owner `BEGIN IMMEDIATE` transaction, so the second writer observes the first commit and cannot insert concurrently. For an assignment disposition, the same transaction derives TERM-01's generation from existing `assignment_reopenings` rows. A retry of one close reuses its source; a close after a reopen has the next generation and therefore creates a distinct source even when the outcome repeats. Deleting the existing reopen surface is outside scope, and accepting same-outcome collapse violates GOAL-01; deriving the generation from its existing papertrail adds no persistence surface.

Live lane failure, task-crash failure, unclaimable-turn failure, and boot recovery to `failed_unknown` all invoke the same source-admission helper inside the transaction that wins their guarded terminal update. Assignment completion, surrender, and revocation invoke the assignment form inside their existing close transaction.

The source event's typed `subject` stores the source form that selects the TERM-05 resolver. Re-entry decodes the same stored form and therefore reuses that resolver; it never runs both completion-parent and failed-turn-parent routing for one source.

### ARC-02 — Candidate order and exclusion

After correlated existing routes are settled, derive candidates in this order:

1. each TERM-05 source-specific normal-route recipient, in the source resolver's order;
2. the expecter edge; and
3. the agent-owner edge.

For a failed-turn source, Bubble already owns the `operationalParent` lineage, so step 1 adds no second candidate. For a completed-assignment source, step 1 consumes the completion resolver's explicit report-to result or its `spawnedBy` result without translating either to `operationalParent`. For surrendered and revoked sources, step 1 consumes only their existing outcome-specific resolver result and starts no parent walk.

Deduplicate equal session keys while preserving the first relation. Exclude the assignment holder, the audience's composed Main key, a `sessions.kind = main` row, a missing session, a non-active session, and any recipient already used by an exact correlated existing route or lifecycle notice for the episode, regardless of that prior turn's terminal outcome.

If a candidate disappears between selection and enqueue, the transaction returns `skipped`; recognition continues to the next candidate. A role lookup and role rebind are outside this MVP because routing uses immutable session keys.

### ARC-03 — Failed-turn integration

The lane or recovery seam writes ARC-01's source event in the same transaction as an eligible failed turn. Bubble then keeps its existing non-Main `operationalParent` climb. Lifecycle never reads `spawnedBy` for that source.

For an eligible assigned root, Bubble evaluates its non-Main lineage before the legacy owner-wide `user-alerted` suppression. Both `parentless` and exhausted terminal rungs call the lifecycle evaluator instead of writing Bubble's owner-wide marker or `user-alerted` fact. Unassigned roots and roots without ARC-01's source event use the existing Bubble path unchanged.

A terminal lifecycle-notice turn is intercepted before Bubble can treat it as a new cause. It calls the evaluator for its `requestRef` source: `delivered` yields `resolved_agent`; `failed`, `failed_unknown`, or `canceled` permits the next untried candidate. A queued or running notice prevents another action. The active version never starts a second Bubble climb from a lifecycle notice; ARC-12 covers the predecessor doing so after rollback.

A terminal Bubble notice whose cause is an eligible root also re-evaluates that root. Delivered resolves the existing route. Non-delivered continues Bubble or, at its terminal rung, permits the first untried lifecycle edge.

An exact correlated supervision route is considered before a lifecycle candidate. If that route is pending, recognition returns without writing. Its terminal callback re-evaluates the root. If delivered, it yields `resolved_existing`; otherwise evaluation continues.

### ARC-04 — Assignment-disposition integration

Every completion, surrender, and revocation seam calls one transaction-local lifecycle function after the assignment row, source-specific normal resolver, supervision terminus, and slate result are final but before commit. Completion passes its explicit report-to or `spawnedBy` resolver result. Surrender and revocation pass only their existing outcome-specific resolver result. The lifecycle function does not read either parent column to replace the result.

The function writes ARC-01's source event. If the close transaction created a `slateWakeId`, it records `resolved_existing` and writes no notice or report. Otherwise it attempts ARC-02's candidates transaction-locally. If no candidate can be enqueued, it writes ARC-07's Main report in the same transaction.

The close handler carries any newly appended notice or marker as a post-commit delivery result. Only after the outer transaction commits may it publish the message and nudge the target lane through the existing Gateway completion seam. A crash before that step loses no work: message replay exposes a marker, and the existing pending-turn reconciler starts a queued notice.

### ARC-05 — Deterministic notice insertion

Notice message and turn insertion use the existing Gateway/Ledger transaction seam and TERM-07 identifiers. A new turn and its projection message commit together. An existing identical `wakeId` or `clientMessageId` is success by duplication and creates no second row. Reuse with different content or correlation stops that insertion; the same outer transaction preserves the existing row, writes ARC-10's refusal event, and commits the source transition. It does not raise a database error or roll the source back.

### ARC-06 — Existing-route resolution

The evaluator reads only the exact correlations in TERM-06. It does not treat an uncorrelated wake, turn, delivered message, progress attest, matching prose, same-session activity, or predecessor `lineage_exhausted` event as resolution.

Bubble and supervision keep their own state and mutation seams. Lifecycle adds no receipt table. Their existing durable turn, wake, and sidecar rows are the receipts for this MVP.

### ARC-07 — Atomic Main report

When agent routing is exhausted, one transaction MUST:

1. insert or read the deterministic TERM-09 message;
2. append lifecycle event `assignment_lifecycle_reported_v1` only when the message was newly inserted; and
3. commit both or neither.

The report event subject is the TERM-01 source id. Its detail is:

```json
{
  "schemaVersion": "assignment-lifecycle-report-v1",
  "episodeId": "ale:...",
  "messageId": "s_...",
  "reason": "agent_supervision_unavailable",
  "principal": "process:tightbeam"
}
```

`reason` is exactly `agent_supervision_unavailable`. No other key or reason value is permitted.

Wire publication occurs after commit. Replay from `messages` is recovery when no client was connected or publication failed.

### ARC-08 — Model-exhaustion boundary

Lifecycle adds no model-exhaustion condition kind, event, report reason, API, or state transition. A supervising agent applies its currently served Kung Fu row. When the ordered row ends, that agent records the attempted rungs, evidence, and consequence as a capability block on the affected assignment and schedules a re-check through the existing assignment and wake seams.

The capability block and re-check are agent-policy records. They are not lifecycle sources, routes, delivery receipts, or Main-report triggers. The lifecycle evaluator neither reads nor writes them. Removing this typed-report path is smaller than retaining a second escalation mechanism, and accepting a model-driven Main report would violate INV-01 and INV-02.

### ARC-09 — API and trace

No new public mutation verb is added.

`assignment-get` adds `lifecycleEpisodes`, ordered by source event `(ts, id)`. Each entry has exactly:

```json
{
  "episodeId": "ale:...",
  "sourceId": "turn:<seq>",
  "sourceAt": 0,
  "state": "resolving",
  "attempts": [
    {"relation": "expecter", "sessionKey": "...", "turnSeq": 0, "status": "queued"}
  ],
  "reportMessageId": null
}
```

`sourceId` uses either TERM-01 form. `state` is exactly one TERM-08 value. `relation` is exactly one of `bubble`, `supervision`, `source_route`, `expecter`, or `agent_owner`; `status` is the joined row's exact existing status. `reportMessageId` is the exact message id string only in `reported_main`; otherwise it is JSON null.

`job-trace` includes the three lifecycle event kinds and the correlated attempt turns. Neither API returns source error text or report body.

### ARC-10 — Error behavior

The implementation uses these named failures:

| Code | Result |
|---|---|
| `lifecycle_audience_missing` | source and refusal event commit; no audience is invented |
| `lifecycle_source_invalid` | refusal event commits; malformed source is not routed |
| `lifecycle_edge_ambiguous` | refusal event commits; no candidate is guessed |
| `lifecycle_idempotency_conflict` | existing row is preserved and refusal event commits |

The first four failures write one lifecycle event with kind `assignment_lifecycle_refused_v1`, subject equal to the source id, and exact detail:

```json
{
  "schemaVersion": "assignment-lifecycle-refusal-v1",
  "episodeId": null,
  "code": "lifecycle_source_invalid",
  "principal": "process:tightbeam"
}
```

`episodeId` is the exact TERM-01 episode string when derivable; otherwise it is JSON null. `code` is exactly one of the first four ARC-10 codes and no other value.

The source mutation is not rolled back merely because lifecycle routing cannot proceed. Before insertion, the transaction checks exact kind and subject; a repeated callback writes no second refusal. The callback then completes, so malformed durable state becomes one named terminal value rather than a retry loop or hold.

Each refusal logs the code, source id, episode id when derivable, and principal. It logs no protected content.

### ARC-11 — Crash, restart, and race behavior

Assignment disposition, slate coverage, source event, notice insertion, and immediate Main fallback share the assignment transition transaction. A crash leaves all or none.

For failed turns, the source event shares the guarded terminal transaction. The live lane and terminal reconciler MUST run lifecycle/Bubble recognition to a durable result before setting `publishedAt`. A durable result is one queued/running exact existing route, one deterministic lifecycle notice, one Main marker, one refusal, or a delivered resolution. The reconciler uses a no-lane-nudge delivery mode during its own pass, then its existing pending-session scan starts any queued notice; this avoids a synchronous call back into itself.

A crash before that durable result leaves `publishedAt` null, so terminal replay re-enters the evaluator. A crash after the result but before acknowledgement replays idempotently. Deterministic turn and message keys make both cases converge. A committed ARC-10 refusal is a durable result and is not retried after publication acknowledgement. The evaluator checks refusal before any route predicate; once refused, it performs no further lifecycle write even if another domain later inserts or delivers a correlated route.

SQLite serialization decides candidate-retirement, supervision-route, and report races. Each transaction re-reads eligibility immediately before its write. The committed pre-change or post-change state wins; no check-then-act gap is permitted.

### ARC-12 — Migration, rollback, and compatibility

There is no lifecycle DDL migration. The shape stamp remains `coordination-fabric-v1-phase1-v5`. The baseline's existing exact v4-to-v5 `operationalParent` upgrade remains unchanged and is not owned by this feature. Lifecycle MUST NOT down-migrate any store.

The supported application rollback baseline `8eeccbd6dfd221fe9d105783459637fb7a17ea83` accepts the same v5 store, ignores the new lifecycle event kinds, and can read all new rows. It may execute already queued lifecycle notice turns as ordinary turns and may write its legacy `lineage_exhausted` event and marker. Rollback MUST NOT delete or rewrite any event, turn, wake, message, assignment, assignment-reopening, or work-item row.

Historical v3 binary `b8e6c47e4631da8345aaf8c6ab73b0858e630bf6` is not a supported rollback target. When pointed at a v5 store, it MUST refuse at the existing shape gate before any lifecycle or application write. Neither this feature nor an operator downgrades the stamp or data to make that binary run.

At each activation of this version, before it accepts new work, Boot reads the maximum existing `lifecycle_events.id`. It enumerates each `assignment_lifecycle_source_v1` event at or below that fixed boundary in `(ts, id)` order and invokes the evaluator. A source that is resolved, refused, or waiting on a pending route is an idempotent no-op. A source after the boundary uses its normal terminal hook. A crash restarts the finite pass from the same rows; deterministic identifiers make repetition safe. The pass stores no cursor or receipt.

During this activation pass, the evaluator commits an inserted lifecycle notice as queued and returns without synchronous publication or a lane nudge. Boot does not invoke `Gateway.complete_delivery/2` or `LaneManager.ensure_lane/2` for that notice. After lane infrastructure starts, the existing pending-session scan publishes the queued notice and starts its lane.

This activation pass is required because the predecessor can acknowledge a lifecycle-notice terminal after writing only its own untyped rows; ordinary `publishedAt` replay then has no terminal left to revisit. Deleting the pass would restore silent loss. Treating the predecessor event as delivery violates INV-01, and adding a receipt or cursor loses to the finite idempotent scan.

On reactivation, exact source events written by this version remain eligible and idempotent. The evaluator uses the exact source and attempt rows, ignores the predecessor's unversioned `lineage_exhausted` detail, and never parses its prose. When no refusal, typed current-version report, delivered or pending route, or untried agent candidate exists, it writes TERM-09's one deterministic marker. During one supported rollback/reactivation cycle, this can leave one predecessor legacy marker and one current TERM-09 marker for the same underlying failure. Current-version replays add no second TERM-09 marker. This named duplicate is safer than treating an event written with no Main stream as delivery, and avoiding it would require forbidden prose parsing or a new receipt surface.

Terminal sources committed only before first activation or while the predecessor runs have no source event and remain outside this MVP by NG-04. Repeated rollback/reactivation cycles and cross-version legacy-marker deduplication are deferred; they do not change current source identifiers or rows.

### ARC-13 — Observability, security, and deletion

Metrics expose counts for source admitted, existing-route resolved, agent resolved, Main reported by reason, duplicate callback, and named error code. Labels MUST NOT contain a prompt, error, note, subject, model output, credential, arbitrary session key, assignment id, or work-item id.

Structured logs may carry source id, episode id, relation, recipient session key, and named code. Report bodies and notice prompts use only TERM-07 and TERM-09 content.

No new delete API, cascade, retention timer, or secret-bearing column exists.

### ARC-14 — Captured real fixtures

Implementation commits these immutable, real-row fixtures and a provenance file:

1. `test/fixtures/assignment_lifecycle/routing-owner-present.json` — work item `wi_8cd66374-6a48-446e-88e1-502652ff24c0`, routing wake `w_9a13250f-2e93-4819-a464-b02bd10356c7`, assignment `asg_64cdf952-5d10-4c58-b74f-224fa5c1f278`.
2. `test/fixtures/assignment_lifecycle/live-switch-failed-worker.json` — work item `wi_507991c2-af57-440f-92a3-da199d9b00e1`, owner assignment `asg_9f5977dd-1d6e-49a5-a48a-c3d68b387f7f`, worker assignment `asg_15c877a9-6015-4f93-939a-e94d75de240e`, failed turns `3523` and `3601`.
3. `test/fixtures/assignment_lifecycle/overlay-user-rooted.json` — work item `wi_4274ccf5-62b6-45e2-9753-74bae345c2f4`, assignment `asg_7b5f3876-2b6f-4d3b-b92c-f3b2dd8f64c6`, failed supervision turn `5352`, surrender attest `att_2a04e02a-e461-4343-b77d-d0e69df686c0`, delivered slate turn `5727`.
4. `test/fixtures/assignment_lifecycle/fable-routing-cancellation.json` — separate negative fixture for work item `wi_9086ebd5-bd62-4c04-9b97-ac83ce34f53e`, routing wake `w_90267efc-5c07-4153-802f-14c9b1e819f1`, assignment `asg_8e48d3cb-60f6-4a66-be36-345f5b86f841`.
5. `test/fixtures/assignment_lifecycle/provenance.json` — source artifact `art_9d7e1cd9`, source SHA-256 `009d3659f5c16729dccdd3d5e5c177c6db4e6160ebab37be96f364874cffe574`, producer `att_f9faaead-4952-48dc-b2e8-a6b9c1389dc0`, reviewed-clean `att_fbdc63ab-0758-4801-8ab8-080c81b5004a`, completion `att_6a156a8a-9e77-478e-a513-cec717f8ab66`, capture commit `f5e4b25971c0037a2a17a8df4edf5f4e6e7e45cc`, and exact capture argv.

Fixtures preserve identifiers, principals, correlations, timestamps, state, and terminal columns. They redact prompts, errors, subjects, notes, model context, message content, and credentials with byte length and SHA-256 evidence. Hand-written ideal fixtures do not pass.

ARC-14 fixture validation and AC-15 packaged smoke are release-blocking for this MVP because a hand-written, mock-only, or source-tree-only pass can conceal silent loss, duplicate terminal escalation, false attribution, or human-principal impersonation. Each is an incredibly detrimental failure under owner ruling `att_a8418685-4f10-4a91-90b0-9ac9b6bceb48`. This rationale adds no fixture or smoke scope.

### ARC-15 — Exact implementation decomposition

Production files:

```text
lib/tightbeam/assignment_lifecycle.ex          # new; source decoder, edge/query projection, evaluator, report
lib/tightbeam/assignments.ex                   # transaction-local assignment source hook
lib/tightbeam/boot.ex                          # failed_unknown recovery admission hook
lib/tightbeam/event_log.ex                     # typed lifecycle source/report readers and documentation
lib/tightbeam/gateway.ex                       # failed-turn source hook and transaction-local notice seam
lib/tightbeam/job_trace.ex                     # derived lifecycle projection
lib/tightbeam/lane_manager.ex                  # replay recognition before publication acknowledgement
lib/tightbeam/ledger.ex                        # terminal/recovery callback inside guarded updates
lib/tightbeam/productions/bubble.ex            # assigned root terminal handoff; notice re-entry
lib/tightbeam/session_lane.ex                  # live terminal admission and recognition ordering
lib/tightbeam/wire/payloads.ex                 # document `[assignment lifecycle]` marker
```

Tests and evidence files:

```text
test/tightbeam/assignment_lifecycle_test.exs
test/tightbeam/assignments_test.exs
test/tightbeam/job_trace_test.exs
test/tightbeam/productions/bubble_test.exs
test/fixtures/assignment_lifecycle/routing-owner-present.json
test/fixtures/assignment_lifecycle/live-switch-failed-worker.json
test/fixtures/assignment_lifecycle/overlay-user-rooted.json
test/fixtures/assignment_lifecycle/fable-routing-cancellation.json
test/fixtures/assignment_lifecycle/provenance.json
scripts/capture_assignment_lifecycle_fixtures.exs
scripts/assignment_lifecycle_smoke.exs
```

`lib/tightbeam/schema.ex`, Rust CLI files, identity/Kung Fu content, client code, release code, and deployment files are outside the implementation set.

### ARC-16 — Source and review provenance

Normative intent originates in `art_9d7e1cd9` at SHA-256 `009d3659f5c16729dccdd3d5e5c177c6db4e6160ebab37be96f364874cffe574`, independently reviewed-clean in `att_fbdc63ab-0758-4801-8ab8-080c81b5004a`.

This MVP consumes ninth-review report `art_52f72ba6` at SHA-256 `93c916f24657d40c66d96e7d4cc0e02df4bffbe954ce25ddd2eb2b62a43f6fde`, owner source ruling `att_dc857f39-585b-4d12-985f-d4a40e60a89d`, custody ruling `att_57bb03f4-81d9-4511-9434-d6ff0e81b8fe`, and Mike's focused-correction/MVP ruling delivered on 2026-08-21.

The first MVP review covered `art_c0dd2b7e` at SHA-256 `34f38864174b6b95525f0fb1a6497b1df6087cee6bd096aadec5792b375a393e` and filed changes-requested verdict `att_08478431-132c-41d6-a9ca-902f3fedb4a4` with report `art_ac28c6c8` at SHA-256 `d11a405ca630ce829ffbb3141209e7a6d9ccdf6573627271dcb6b79f357f74c7`. Operator decision `dr_cfe612db-7289-4a1f-acd5-5bb26701fbfc` authorized the minimal F1/F2 closure: close-generation assignment identity, deletion of untyped predecessor events as coverage, and the bounded rollback duplicate in ARC-12. Owner re-pin `att_7d588233-c56b-4641-a90e-1c8af14f1cf0` adopts `main@b8e6c47e4631da8345aaf8c6ab73b0858e630bf6` and deletes typed model-exhaustion-to-Main behavior from this MVP. Owner ruling `att_a8418685-4f10-4a91-90b0-9ac9b6bceb48` advances the baseline to `main@2d0bbf056996ca573379bc022f7620b55f309120` with rollback predecessor `b8e6c47e4631da8345aaf8c6ab73b0858e630bf6` and supplies the exact blocking-fixture rationale in ARC-14, AC-14, and AC-15.

Independent review assignment `asg_5df4205e-ca2f-4e97-a53f-ddb289fe895b` covered `art_71a67610` at SHA-256 `bf27ef2b7a1b190cc8175ce070c2a0c9d8ece363636b16851cbae66b7d80c8e1` and filed changes-requested verdict `att_1bcebc61` with report `art_b5a5f51e` at SHA-256 `3f8b1d9803278865b0c61aefa54e2dda769d6ce573b663812a9daf2d3b5f26dd`. Mike's direct ruling in transcript message `s_10c2b127-a7d6-42bc-b189-8453879e3d33` authorizes one current-main re-pin, that report's F1-only activation correction, and its matching AC-12 case. The re-pin adopts `main@8eeccbd6dfd221fe9d105783459637fb7a17ea83`.

Fresh independent review assignment `asg_06569baa-8488-4632-8830-50477b31718c` covered frozen `art_9b4a467d` at SHA-256 `dbed7b4b138cd9cfc931a4854918ad435f22693e7b3e3f65e2eacde42fb56964` and filed changes-requested verdict `att_5cec5137-d582-44b8-a24d-b945a4141d46`. Full report `art_df1fb359` at SHA-256 `0acb50729960ab412bd679818b9b5bf389de6b31fad356ecee578b7a47a1e5c5` found the v3/v5 compatibility contradiction and the universal `spawnedBy` parent contradiction; it independently found the activation correction closed. Owner ruling `att_b96ca649-8620-4b24-a31f-519d42cae4fb` makes v5 canonical, retains the existing v4-to-v5 upgrade, sets `8eeccbd6...` as the same-shape rollback baseline, makes historical `b8e6c47e...` a refusing non-target, and requires source-specific normal resolvers without translating `spawnedBy` and `operationalParent`. No other product requirement changes.

The prior frozen candidate `art_1fbd7a55` at SHA-256 `5caf7d2dba7f90532c339d11b230bf4ba86d6e29ac1cf0ff8002403140272ca6` remains historical review evidence. It is not implementation authority.

The builder MUST recheck remote `refs/heads/main`. If it differs from `8eeccbd6dfd221fe9d105783459637fb7a17ea83`, implementation stops for an owner re-pin.

## Acceptance

### AC-01 — Existing route wins

Given the routing-owner specimen and an eligible failed assigned turn, when Bubble or exact supervision coverage is queued, running, or delivered, then lifecycle writes no duplicate notice or report. When that coverage terminates non-delivered, lifecycle considers the next distinct agent edge once.

### AC-02 — Source route and agent edges precede Main

Given distinct active source-route, expecter, and agent-owner recipients not already attempted by an exact existing route, when an eligible source is recognized, then the source-route recipient receives one deterministic notice first. If it fails, the expecter receives one; if that fails, the agent owner receives one. If the source resolver returns no recipient, the expecter is first. Main receives no model turn. If any candidate delivers, state is `resolved_agent` and no ordinary Main report exists. A recipient already attempted by Bubble, supervision, or an earlier candidate receives no second notice.

### AC-03 — Source-specific parent routes and ownership stay unchanged

Given child `C` has `spawnedBy=P1` and `operationalParent=P2`, when an assigned turn in `C` fails, then Bubble follows `P2` and lifecycle never substitutes `P1`. Given an assignment held by `C` completes without an explicit report-to declaration, then the completion resolver starts from `P1` and lifecycle never substitutes `P2`. Given completion has an explicit report-to declaration `R`, then its resolver uses `R` and does not start from either parent column. Given surrender or revocation, then lifecycle consumes only that outcome's existing resolver result and starts no parent walk.

Repeated terminal callbacks create one source event and at most one notice for each `(episode, recipient)`, even when `P1` and `P2` differ. One source never invokes both the failed-turn and completion resolver or treats both `P1` and `P2` as source-route candidates. A failed lifecycle notice does not start another Bubble climb. No write changes `spawnedBy`, `operationalParent`, report-to, holder, opener, owner, role, or review columns. No user-rooted reparenting or replacement session occurs.

### AC-04 — Assignment terminal and slate behavior

Given completion, surrender, and revocation in separate cases, when each commits without a slate wake, then its exact source event and one agent notice or Main report commit atomically with the assignment transition. Given the close creates a slate wake, then state is `resolved_existing` and lifecycle creates no notice or report.

Given an assignment closes `completed`, reopens, and closes `completed` again, then the first source ends in `:completed:1`, the second ends in `:completed:2`, and both have distinct episodes and routing outcomes. Replaying either close callback ten times does not create another source for that generation.

### AC-05 — Atomic report and idempotency

Given no eligible agent route, when recognition reports Main, then one high-attention marker and one report event commit in one transaction with `process:tightbeam` attribution. Replaying the callback ten times leaves one marker and one report event. Injected failure at either write commits neither.

### AC-06 — Crash and restart

Given a failed-turn source commits and the process crashes before routing, when terminal publication recovery runs, then it recognizes the same episode before acknowledging publication. Crashes before and after notice or report commit yield one deterministic turn or marker, never zero after recovery and never two. Boot-recovered `failed_unknown` and unclaimable assigned turns write their source event in the guarded terminal transaction and pass the same test.

### AC-07 — Race closure

Given candidate retirement or supervision route insertion races evaluation, when both transactions finish, then SQLite order produces exactly the pre-change or post-change valid result. No report commits while a route visible to its transaction remains pending or delivered.

Given ARC-10 refusal commits and an independently owned route is inserted or delivered later, when the episode is read and recognition is retried, then its state remains `refused` and lifecycle writes no notice or report.

### AC-08 — Kung Fu ring-down

Given an agent receives a lifecycle notice and its applicable test Kung Fu row is `[candidate-A, candidate-B, candidate-C]`, when A is refused and B is out of tokens, then the agent tries C once. It does not retry A or B, use an off-list model, or report model unavailability to Main.

Given C also fails, when the row ends, then the agent records A, B, C, their evidence, and the consequence as a capability block on the affected assignment and schedules one re-check. Separable work continues. No lifecycle Main marker or report event is created.

This is an agent-policy acceptance fixture. The lifecycle substrate proves only its no-report boundary; it does not parse the policy, perform the attempts, create the capability block, or schedule the re-check.

### AC-09 — Model exhaustion never reports Main

Given a delivered supervisor notice and an exhausted ordered model row, when the agent records its assignment capability block and schedules a re-check, then the lifecycle episode remains `resolved_agent`. No lifecycle Main marker, report event, or additional lifecycle state transition appears.

### AC-10 — No capable supervisor

Given all recorded non-Main agent routes terminate non-delivered, when recognition reaches fallback, then Main receives one `agent_supervision_unavailable` marker. The marker states only that no recorded non-Main route delivered. It makes no model-availability or capability-block claim.

### AC-11 — Capability-block isolation

Given an assignment capability block and its scheduled re-check exist before or after lifecycle recognition, when the evaluator reads the episode, then it ignores both records as lifecycle routing evidence. They create no lifecycle source, route, resolution, refusal, or Main report.

### AC-12 — Historical compatibility and rollback

Given a fresh database or an existing v5 database, when the feature binary starts, then the shape remains `coordination-fabric-v1-phase1-v5` and lifecycle adds no schema object. Given an exact v4 database, when the baseline's existing upgrade runs, then it produces v5 with `operationalParent` through the existing schema seam before lifecycle evaluation; lifecycle does not alter that upgrade.

Given new lifecycle rows on v5, when supported rollback baseline `8eeccbd6dfd221fe9d105783459637fb7a17ea83` starts against the same store, then the shape check passes and it preserves them. Given historical v3 binary `b8e6c47e4631da8345aaf8c6ab73b0858e630bf6` starts against that v5 store, then it deterministically refuses at the shape gate, performs no write, and does not downgrade the stamp or data.

Given existing terminal rows without ARC-01 events, when the feature binary starts, then it reports none and changes no existing row.

Given the last queued lifecycle notice enters the predecessor during one rollback/reactivation cycle and the predecessor acknowledges that terminal, then the restored rows project `resolving`, not an absent state. When the current version activates, its fixed-boundary pass visits the typed source. If the predecessor wrote `lineage_exhausted` with no active Main stream, the evaluator ignores that event and writes exactly one current TERM-09 marker. If an active Main stream instead received one predecessor legacy marker, the evaluator writes exactly one current TERM-09 marker, yielding the one named duplicate. Ten pass or evaluator replays add no additional marker. No test parses predecessor event detail or marker text.

Given a fixed-boundary source has one untried eligible agent candidate and lane infrastructure has not started, when Boot invokes the evaluator, then Boot completes and one deterministic lifecycle notice remains queued without publication or a lane nudge. The activation path makes zero calls to `Gateway.complete_delivery/2` and `LaneManager.ensure_lane/2` for that notice. When lane infrastructure and the existing pending-session scan start, the scan publishes that queued notice and starts exactly one lane for it.

### AC-13 — Trace, security, and deletion

Given one episode in each derived state, including `refused`, when `assignment-get` and `job-trace` run, then they return ARC-09's exact identifiers, states, attempts, and report id. They return no source error or report body. No lifecycle delete command exists, and retirement or disposition deletes no lifecycle evidence.

### AC-14 — Fixture fidelity

Given the reviewed capture source, when the five ARC-14 files are validated, then every named id, timestamp, principal, correlation, state, terminal field, redaction length, and redaction SHA matches the real source. Changing one preserved value or using a hand-written row causes failure. The Fable cancellation fixture creates no lifecycle source.

This validation is release-blocking for the exact ARC-14 rationale. It adds no fixture.

### AC-15 — Deterministic and packaged gates

The exact implementation commit MUST pass on Linux and macOS under the CI definition whose SHA-256 is `1ccc8176ca9a8b9c2a677eaf31723e3c9602f6790ed8baccb945a5bc2d000e57`. Commands use these exact working directories:

| Working directory | Command |
|---|---|
| repository root | `mix format --check-formatted` |
| repository root | `scripts/verify_mix.sh` |
| repository root | `mix test` |
| `cli/` | `cargo fmt --check` |
| `cli/` | `cargo test` |
| repository root | `sh packaging/assemble.sh` |

The packaged smoke installs the assembled artifact into a fresh prefix and uses a fresh database. It runs one real available Claude or Codex agent route selected through the live permitted catalog, proves a delivered agent notice suppresses Main, and proves an `agent_supervision_unavailable` Main marker without invoking a model. A separate throwaway agent-policy case exhausts an ordered candidate row, records the attempted candidates and evidence as the affected assignment's capability block, schedules a re-check, and proves no lifecycle Main marker appears. A mock harness, source-tree-only run, unavailable candidate retry, or unrecorded credential block does not pass. If no candidate in the smoke activity's allowed row is available, the gate records the attempted ordered candidates and evidence as the affected assignment's capability block and schedules a re-check; it does not silently pass, substitute, or report Main.

This packaged smoke is release-blocking for the exact ARC-14 rationale. It adds no smoke case.

### AC-16 — Clause map

| Requirement | Acceptance | Proposed files |
|---|---|---|
| INV-01, INV-03, INV-04 | AC-01 through AC-04, AC-10, AC-12 | `assignment_lifecycle.ex`, `bubble.ex`, `assignments.ex` |
| INV-02 | AC-08 through AC-11 | `assignment_lifecycle.ex`; existing Kung Fu, assignment, and wake seams unchanged |
| INV-05, INV-06 | AC-04 through AC-07, AC-12 | `assignment_lifecycle.ex`, `gateway.ex`, `session_lane.ex`, `lane_manager.ex`, `ledger.ex`, existing unique indexes |
| INV-07 | AC-01, AC-03, AC-04, AC-14 | `bubble.ex`, existing supervision/slate seams |
| INV-08, INV-10 | AC-05, AC-13 | `event_log.ex`, `projection.ex` unchanged, `job_trace.ex` |
| INV-09 | AC-04, AC-12 | `assignments.ex`; no schema file change |
| GOAL-01 | AC-01 through AC-07, AC-12 | source hooks and evaluator |
| GOAL-02 | AC-08 through AC-11 | lifecycle no-report boundary; existing agent-policy records unchanged |
| GOAL-03 | AC-14, AC-15 | fixtures, deterministic tests, packaged smoke |
| ARC-01 through ARC-08 | AC-01 through AC-12 | production file set in ARC-15 |
| ARC-09 through ARC-13 | AC-05 through AC-13 | trace, errors, compatibility, observability |
| ARC-14 through ARC-16 | AC-14, AC-15, independent hash-bound review | fixtures, gates, provenance |

## Open Questions

Blocking: none.

Non-blocking: none. NG-04 through NG-06 are explicit follow-on deferrals, not hidden decisions required to build this MVP.
