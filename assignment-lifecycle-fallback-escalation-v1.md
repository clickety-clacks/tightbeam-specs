# Assignment lifecycle fallback escalation v1

Status: MVP contract; implementation is forbidden until an independent reviewer files `reviewed-clean` against this exact content hash  
Work item: `wi_3d6d13a0-c4cf-4370-88a1-b407c41ff7c1`  
Authority assignment: `asg_3fce3846-487e-496a-af79-6e2114ff39ab`  
Product owner assignment: `asg_0bd4c0ab-68a0-463e-92c4-e5d11a8135c5`

## Invariants

### INV-01 — A lifecycle source reaches an agent before Main

For each eligible source, Tightbeam MUST first use any correlated existing route, including Bubble's non-Main holder-parent climb, then the recorded agent expecter and agent owner. It MAY write one report to the owning user's personal Main stream only when no such route remains pending or able to accept a turn.

Main is a report audience. Main MUST NOT be inserted into the agent-candidate list and MUST NOT receive a lifecycle model turn.

### INV-02 — Model choice remains agent judgment

The lifecycle mechanism MUST NOT read Kung Fu prose, select a model, switch a model, spawn a replacement, infer an activity, or decide that a model list is exhausted.

A supervising agent that receives a failed-turn notice applies its own currently served Kung Fu model-selection row. The agent MUST try each allowed candidate in that row once, in order. A refused candidate or a harness that is out of tokens advances to the next candidate. Nothing off-list is tried.

Main MUST NOT receive a `model candidates exhausted` report from a failed turn, a provider name, an error string, or an unavailable first candidate. That report is permitted only after an authorized supervising agent files the typed fact defined in ARC-08.

### INV-03 — Lifecycle does not change custody

The feature MUST NOT change a work-item owner, assignment opener, assignment holder, session parent, role binding, or review relationship. It MUST NOT create a work item, assignment, session, or replacement model session.

### INV-04 — Rows, not prose, determine routing

Routing MUST use stored identifiers and typed rows. It MUST NOT parse prompts, assignment subjects, attest notes, model output, display names, error prose, or artifact contents. The only parsed strings are the closed, versioned identifiers defined in TERM-01.

### INV-05 — One source has one stable episode

Each eligible source has one derived episode id. Repeated callbacks, process crashes, restarts, and concurrent recognition MUST reuse that id. Each `(episode, recipient)` has at most one notice turn. Each episode has at most one Main report.

This MVP does not coalesce several sources into a mutable per-assignment episode.

### INV-06 — A Main report is its own atomic state

The report state and the visible high-attention Main marker MUST be one `messages` row. The report's lifecycle event MUST commit in the same SQLite transaction. A crash cannot commit a reported state without its readable marker or a marker without its reported state.

### INV-07 — Existing production domains stay distinct

The change MUST preserve:

- assignment-open routing-wake cancellation;
- Bubble's existing climb for failed turns;
- supervision of stalled open assignments; and
- the zero-open-assignment slate wake.

A routing-wake cancellation is never a lifecycle source. Bubble retains its current behavior byte-for-byte for unassigned turns and pre-MVP rows. For an eligible assigned turn, Bubble performs its normal non-Main lineage climb before the lifecycle mechanism tries other recorded agent edges. A correlated supervision or slate route counts as existing coverage and suppresses a duplicate lifecycle notice or report.

### INV-08 — Attribution and content are truthful

Every feature-authored event, turn, and marker uses principal, origin, or sender `process:tightbeam`. A feature-authored row MUST NOT impersonate a user or role. Each row MUST carry the identifiers applicable to its purpose; the joined source, attempt, and report rows together expose source, assignment, work-item, relation, and recipient correlation. They MUST NOT copy the original prompt, error text, model output, assignment subject, attest note, artifact content, credential, or token.

### INV-09 — Existing shape and rows remain valid

The implementation MUST add no table, column, index, trigger, or shape stamp. The database stamp remains `coordination-fabric-v1-phase1-v3`. Existing rows remain readable and unchanged. Rows without an `assignment_lifecycle_source_v1` event are historical and MUST NOT be backfilled or reported.

### INV-10 — No lifecycle row is deleted

The product MUST expose no lifecycle delete or repair operation. Existing deletion and retention behavior for turns, wakes, messages, lifecycle events, condition facts, assignments, sessions, and work items does not change.

## Goal

### GOAL-01

Close the proven silent-loss gap for new assigned failed turns and accepted assignment dispositions. A capable recorded agent sees the source first. If no agent route succeeds, the owning user's Main receives one durable, model-independent action-needed marker.

### GOAL-02

When an agent determines that a failed turn cannot continue because the applicable Kung Fu model list is exhausted, Main receives one capability-block marker only after that agent-owned fact commits.

### GOAL-03

Prove the behavior with the three reviewed lifecycle specimens, a separate Fable routing-cancellation specimen, deterministic fault/race tests, and packaged real-harness smoke.

Subtraction decision: DELETE wins for the prior activation membership, source cursor, recovery cursor, episode table, attempt table, receipt tables, health subsystem, and migration engine. Existing atomic rows already represent the MVP. Accepting silent loss would violate GOAL-01; adding a second persistence lattice would violate the current no-shape-migration ruling and the substrate's own agent-first principle.

## Non-Goals

### NG-01

This feature does not judge correctness, urgency, importance, staffing, or the next action.

### NG-02

This feature does not implement model ring-down. Agents apply the Kung Fu policy through existing spawn, assignment, wake, condition, and credential flows.

### NG-03

This feature does not add HarnessHealth, provider suppression, model availability state, a model retry counter, or a model-selection API.

### NG-04

This MVP does not backfill historical terminals, cover terminal sources committed while the rollback predecessor runs, or coalesce multiple source episodes. Those cases are visible in existing rows and can be added later without changing this MVP's identifiers.

### NG-05

This MVP does not add a general source sweeper, fairness cursor, permanent-failure ledger, transition ledger, or lifecycle mutation command. Recognition uses existing transaction hooks and terminal replay.

### NG-06

This MVP does not add structured marker columns or require client-specific rendering. Unaware clients display readable marker text.

### NG-07

This feature does not alter assignment-open routing cancellation, wake-cancellation attribution, Bubble for unassigned turns, supervision thresholds, slate timing, or work-item disposition.

## Terms

### TERM-01 — Source and episode

The eligible source forms and stable identifiers are:

| Source | Source id | Eligibility |
|---|---|---|
| assigned terminal turn | `turn:<seq>` | `turns.assignmentId` is non-null; status is `failed` or `failed_unknown`; the terminal transaction wrote the ARC-01 source event |
| assignment disposition | `assignment:<assignmentId>:<outcome>` | outcome is `completed`, `surrendered`, or `revoked`; the closing transaction wrote the ARC-01 source event |
`episodeId` is `ale:<sourceId>` for a turn or assignment source. A model-list exhaustion fact continues the named turn episode; it does not create a second episode.

ARC-08's model-list exhaustion input has evidence id `model-exhausted:<conditionFactId>:<turnSeq>`. It continues the named turn episode and is not a second lifecycle source.

The assignment source id contains the assignment id and outcome once as canonical correlation and idempotency identity. Those components are not copied into another feature-owned persistence field.

A turn whose `requestRef` begins `assignment-lifecycle:` is an attempt, not a new source. A `canceled` turn and a routing-wake cancellation are not sources.

### TERM-02 — Audience

The audience is `work_items.ownerUserId` when the assignment has a work item. Otherwise it is the immutable `sessions.ownerUserId` of the assignment holder. Its report stream is `Tightbeam.Org.personal_session_key(audienceUserId)`.

If neither row yields one user, recognition returns the named error `lifecycle_audience_missing`; it does not invent an owner.

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

### TERM-05 — Holder-parent edge

The holder-parent edge starts at `sessions.spawnedBy` for the assignment holder. For a failed-turn source, Bubble walks active ancestors nearest-first with its existing 32-hop and cycle behavior, and lifecycle does not create a second climb. For an assignment-disposition source, lifecycle applies the same active, nearest-first, 32-hop, visited-set rules because no Bubble root exists.

### TERM-06 — Existing route

Existing coverage is one of:

- a Bubble notice for the root failed turn;
- an exact supervision controller wake or turn correlated by the existing sidecar to that root turn and assignment; or
- the work item's `slateWakeId` created in the same assignment-close transaction; or
- an existing Bubble `lineage_exhausted` event whose exact root is the source turn or a lifecycle-notice turn for the source.

Queued or running coverage keeps the episode `resolving`. Delivered coverage resolves it. A terminal non-delivered route permits the next candidate. A pending slate wake is coverage because its existing domain intentionally routes the zero-assignment decision to Main.

### TERM-07 — Lifecycle notice

A lifecycle notice is a model turn to a non-Main agent expecter, agent-owner, or assignment-disposition holder-parent recipient. Its identifiers are:

- `wakeId = assignment-lifecycle:<sourceId>:<relation>:<sessionKey>`;
- `clientMessageId` equal to `wakeId` and `deviceId = process:tightbeam`;
- `requestRef = assignment-lifecycle:<sourceId>`;
- the source assignment id in `turns.assignmentId`; and
- the source work-item id in `turns.jobRef` when present.

For a failed-turn source, the prompt is exactly:

```text
Assignment lifecycle source <sourceId> on assignment <assignmentId> needs supervision. You are its recorded <expecter|agent owner>. Inspect the durable rows and decide the next action. If the failure is model availability, use your currently served Kung Fu activity row: try each allowed candidate once in order; use nothing off-list; file model-candidates-exhausted for episode <episodeId> only after the list ends. Tightbeam did not change ownership.
```

The prompt contains no source error or assignment subject.

For an assignment disposition, the prompt is exactly:

```text
Assignment lifecycle source <sourceId> on assignment <assignmentId> needs supervision. You are its recorded <expecter|agent owner|holder parent>. Inspect the durable rows and decide the next action. Tightbeam did not change ownership.
```

### TERM-08 — Derived episode state

The read projection derives one state; no mutable lifecycle state row exists:

| State | Row predicate |
|---|---|
| `resolving` | source event exists; an existing route or lifecycle notice is queued/running, or an untried eligible agent edge remains |
| `resolved_existing` | a correlated existing route delivered, or a same-transaction slate wake covers an assignment close |
| `resolved_agent` | an expecter or agent-owner lifecycle notice delivered |
| `reported_main` | the deterministic ARC-07 Main marker exists |
| `refused` | ARC-10's deterministic refusal event exists |

`resolving -> resolved_existing | resolved_agent | reported_main | refused` is allowed. `resolved_agent -> reported_main` is allowed only after ARC-08's typed exhaustion fact. No transition leaves `refused`, and no other transition exists.

### TERM-09 — Main report marker

The Main report is one `messages` row with role `assistant`, sender `process:tightbeam`, attention tier `high`, device id `process:tightbeam`, and client message id `assignment-lifecycle:main:<sourceId>`. Its first line is `[assignment lifecycle]`.

An ordinary exhausted-routing body states that no recorded agent route accepted the notice and that model-candidate exhaustion was not established. A typed exhaustion body names the exhaustion fact id and states that an agent reported the applicable candidate list exhausted.

### TERM-10 — Capable agent

An agent is capable only when its correlated existing-route or lifecycle-notice turn reaches `delivered`. An active session row permits an attempt; it does not prove capability.

## Assumptions

### ASM-01

`turns`, `assignments`, `sessions`, `work_items`, `wakes`, `messages`, `condition_facts`, and `lifecycle_events` retain committed rows needed by the derived projection.

### ASM-02

SQLite transactions and the existing unique indexes on `turns.wakeId` and `(messages.sessionKey, messages.deviceId, messages.clientMessageId)` provide atomicity and idempotency.

### ASM-03

The existing terminal publication reconciler retries a terminal turn whose `publishedAt` remains null after a crash. Its `on_terminal` hook runs again before publication is acknowledged.

### ASM-04

The current Bubble root correlation is `requestRef = bubble:<rootTurnSeq>`. Supervision sidecars and slate wake ids retain their current exact correlation fields.

### ASM-05

The controlling implementation baseline is `main@a1cea925563adbb7cca62b463a705658bd07d025`, database shape `coordination-fabric-v1-phase1-v3`, CI file SHA-256 `1ccc8176ca9a8b9c2a677eaf31723e3c9602f6790ed8baccb945a5bc2d000e57`, and rollback predecessor `ef1ef51b8e1b0293d69b1208655a735e42bbf99d`.

### ASM-06

The shipped `agentic-engineering` Kung Fu defines ordered model candidates by activity and the live catalog decides whether each named candidate is selectable. That content may change without a product database migration.

## Architecture

### ARC-01 — Source admission and persistence

Add lifecycle event kind `assignment_lifecycle_source_v1`. It is written only inside the transaction that wins the terminal source transition.

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
  "workItemId": "wi_... or null",
  "principal": "process:tightbeam"
}
```

The event stores no prompt, error, assignment-subject text, note, outcome copy, model response, or credential. Its presence is the post-activation eligibility boundary. An existing terminal row without this event is historical.

Before inserting, the terminal transaction checks for the exact event kind and subject. If it already exists, the source retains its original episode and the transaction writes no second source event. SQLite's write serialization makes the check and insert one atomic mutation seam. This also means a reopened assignment that later closes with the same outcome rejoins its original canonical `assignment:<assignmentId>:<outcome>` episode.

### ARC-02 — Candidate order and exclusion

After correlated existing routes are settled, derive candidates in this order:

1. the expecter edge;
2. the agent-owner edge; and
3. for an assignment-disposition source only, each holder-parent edge nearest-first.

For a failed-turn source, Bubble already owns the holder-parent lineage, so step 3 adds no candidate.

Deduplicate equal session keys while preserving the first relation. Exclude the assignment holder, the audience's composed Main key, a `sessions.kind = main` row, a missing session, a non-active session, and any `(episode, recipient)` whose deterministic attempt turn already exists.

If a candidate disappears between selection and enqueue, the transaction returns `skipped`; recognition continues to the next candidate. A role lookup and role rebind are outside this MVP because routing uses immutable session keys.

### ARC-03 — Failed-turn integration

The Gateway writes ARC-01's source event in the same transaction as an eligible failed turn. Bubble then keeps its existing holder-parent climb.

At Bubble's terminal rung, an eligible assigned root calls the lifecycle evaluator instead of Bubble's owner-wide `user-alerted` terminal alert. Unassigned roots and roots without ARC-01's source event use the existing Bubble path unchanged.

A terminal lifecycle-notice turn calls the evaluator for its `requestRef` source. `delivered` yields `resolved_agent`. `failed`, `failed_unknown`, or `canceled` permits the next candidate. A queued or running notice prevents another action.

An exact correlated supervision route is considered before a lifecycle candidate. If that route is pending, recognition returns without writing. Its terminal callback re-evaluates the root. If delivered, it yields `resolved_existing`; otherwise evaluation continues.

### ARC-04 — Assignment-disposition integration

Every completion, surrender, and revocation seam calls one transaction-local lifecycle function after the assignment row, supervision terminus, and slate result are final but before commit.

The function writes ARC-01's source event. If the close transaction created a `slateWakeId`, it records `resolved_existing` and writes no notice or report. Otherwise it attempts ARC-02's candidates transaction-locally. If no candidate can be enqueued, it writes ARC-07's Main report in the same transaction.

### ARC-05 — Deterministic notice insertion

Notice message and turn insertion use the existing Gateway/Ledger transaction seam and TERM-07 identifiers. A new turn and its projection message commit together. An existing identical `wakeId` or `clientMessageId` is success by duplication and creates no second row. Reuse with different content or correlation is `lifecycle_idempotency_conflict` and the transaction aborts.

### ARC-06 — Existing-route resolution

The evaluator reads only the exact correlations in TERM-06. It does not treat an uncorrelated wake, turn, delivered message, progress attest, matching prose, or same-session activity as resolution.

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
  "reason": "agent_supervision_unavailable | model_candidates_exhausted",
  "principal": "process:tightbeam"
}
```

Wire publication occurs after commit. Replay from `messages` is recovery when no client was connected or publication failed.

### ARC-08 — Model-list exhaustion fact

Add agent-only condition kind `model-candidates-exhausted`. Its scope is an exact `ale:turn:<seq>` episode id.

The condition verb accepts it only when:

- the episode decodes to an eligible ARC-01 assigned failed turn;
- the caller is above the failed turn's session in `spawnedBy` lineage or is that session's owning user/admin, using the existing `work-blocked` authority rule; and
- a correlated expecter, agent-owner, Bubble, or supervision agent turn delivered for the episode.

The substrate does not inspect or count model attempts. The fact is the supervising agent's judgment that it applied the applicable Kung Fu row and exhausted its allowed candidates once each. The agent also uses existing `work-blocked` when current model policy requires the affected session to stop receiving ordinary work.

The condition fact and ARC-07 report commit in one transaction. The report reason is `model_candidates_exhausted`. Duplicate facts cannot duplicate the deterministic report. The substrate MUST refuse this condition kind from `process:tightbeam` and from the affected session itself.

### ARC-09 — API and trace

No new public mutation verb is added. The existing `condition` verb accepts ARC-08's new kind.

`assignment-get` adds `lifecycleEpisodes`, ordered by source event `(ts, id)`. Each entry has exactly:

```json
{
  "episodeId": "ale:...",
  "sourceId": "turn:... or assignment:...",
  "sourceAt": 0,
  "state": "resolving | resolved_existing | resolved_agent | reported_main | refused",
  "attempts": [
    {"relation": "bubble | supervision | expecter | agent_owner | holder_parent", "sessionKey": "...", "turnSeq": 0, "status": "..."}
  ],
  "reportMessageId": "s_... or null"
}
```

`job-trace` includes the three lifecycle event kinds and the correlated attempt turns. Neither API returns source error text or report body.

### ARC-10 — Error behavior

The implementation uses these named failures:

| Code | Result |
|---|---|
| `lifecycle_audience_missing` | source and refusal event commit; no audience is invented |
| `lifecycle_source_invalid` | refusal event commits; malformed source is not routed |
| `lifecycle_edge_ambiguous` | refusal event commits; no candidate is guessed |
| `lifecycle_idempotency_conflict` | existing row is preserved and refusal event commits |
| `model_exhaustion_not_authorized` | condition command returns a value error and writes no fact/report |
| `model_exhaustion_unproven_route` | no delivered agent route exists; condition command writes nothing |

The first four failures write one lifecycle event with kind `assignment_lifecycle_refused_v1`, subject equal to the source id, and exact detail:

```json
{
  "schemaVersion": "assignment-lifecycle-refusal-v1",
  "episodeId": "ale:... or null",
  "code": "one ARC-10 code",
  "principal": "process:tightbeam"
}
```

The source mutation is not rolled back merely because lifecycle routing cannot proceed. Before insertion, the transaction checks exact kind and subject; a repeated callback writes no second refusal. The callback then completes, so malformed durable state becomes one named terminal value rather than a retry loop or hold.

Each refusal logs the code, source id, episode id when derivable, and principal. It logs no protected content.

### ARC-11 — Crash, restart, and race behavior

Assignment disposition, slate coverage, source event, notice insertion, and immediate Main fallback share the assignment transition transaction. A crash leaves all or none.

For failed turns, the source event shares the terminal transaction. A crash before routing leaves `publishedAt` null; existing terminal replay re-enters the evaluator. Deterministic turn and message keys make re-entry idempotent. A committed ARC-10 refusal lets publication complete and is not retried.

SQLite serialization decides candidate-retirement, supervision-route, condition-fact, and report races. Each transaction re-reads eligibility immediately before its write. The committed pre-change or post-change state wins; no check-then-act gap is permitted.

### ARC-12 — Migration, rollback, and compatibility

There is no DDL migration. The shape stamp remains `coordination-fabric-v1-phase1-v3`.

The immediate predecessor `ef1ef51b8e1b0293d69b1208655a735e42bbf99d` ignores the new lifecycle event kinds and can read all new rows. It may execute already queued lifecycle notice turns as ordinary turns. Rollback MUST NOT delete or rewrite any event, turn, wake, message, condition fact, assignment, or work-item row.

On reactivation, exact source events written by this version remain eligible and idempotent. Terminal sources committed only before first activation or while the predecessor runs have no source event and remain outside this MVP by NG-04.

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

### ARC-15 — Exact implementation decomposition

Production files:

```text
lib/tightbeam/assignment_lifecycle.ex          # new; source decoder, edge/query projection, evaluator, report
lib/tightbeam/assignments.ex                   # transaction-local assignment source hook
lib/tightbeam/condition_facts.ex               # agent-only exhaustion kind and atomic report hook
lib/tightbeam/event_log.ex                     # typed lifecycle source/report readers and documentation
lib/tightbeam/gateway.ex                       # failed-turn source hook and transaction-local notice seam
lib/tightbeam/job_trace.ex                     # derived lifecycle projection
lib/tightbeam/productions/bubble.ex            # assigned root terminal handoff; notice re-entry
lib/tightbeam/wire/payloads.ex                 # document `[assignment lifecycle]` marker
```

Tests and evidence files:

```text
test/tightbeam/assignment_lifecycle_test.exs
test/tightbeam/assignment_lifecycle_model_exhaustion_test.exs
test/tightbeam/assignments_test.exs
test/tightbeam/condition_facts_test.exs
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

The prior frozen candidate `art_1fbd7a55` at SHA-256 `5caf7d2dba7f90532c339d11b230bf4ba86d6e29ac1cf0ff8002403140272ca6` remains historical review evidence. It is not implementation authority.

The builder MUST recheck remote `refs/heads/main`. If it differs from `a1cea925563adbb7cca62b463a705658bd07d025`, implementation stops for an owner re-pin.

## Acceptance

### AC-01 — Existing route wins

Given the routing-owner specimen and an eligible failed assigned turn, when Bubble or exact supervision coverage is queued, running, or delivered, then lifecycle writes no duplicate notice or report. When that coverage terminates non-delivered, lifecycle considers the next distinct agent edge once.

### AC-02 — Agent edges precede Main

Given distinct active expecter and agent-owner recipients, when an eligible source is recognized, then the expecter receives one deterministic notice first. If it fails, the agent owner receives one. Main receives no model turn. If either delivers, state is `resolved_agent` and no ordinary Main report exists.

### AC-03 — Parent lineage and ownership stay unchanged

Given `holder -> parent -> Main`, when a failed assigned turn bubbles, then the existing Bubble turn reaches `parent` before lifecycle tries other edges. No write changes `spawnedBy`, holder, opener, owner, role, or review columns. No user-rooted reparenting or replacement session occurs.

### AC-04 — Assignment terminal and slate behavior

Given completion, surrender, and revocation in separate cases, when each commits without a slate wake, then its exact source event and one agent notice or Main report commit atomically with the assignment transition. Given the close creates a slate wake, then state is `resolved_existing` and lifecycle creates no notice or report.

### AC-05 — Atomic report and idempotency

Given no eligible agent route, when recognition reports Main, then one high-attention marker and one report event commit in one transaction with `process:tightbeam` attribution. Replaying the callback ten times leaves one marker and one report event. Injected failure at either write commits neither.

### AC-06 — Crash and restart

Given a failed-turn source commits and the process crashes before routing, when terminal publication recovery runs, then the same episode resumes. Crashes before and after notice or report commit yield one deterministic turn or marker, never zero after recovery and never two.

### AC-07 — Race closure

Given candidate retirement, supervision route insertion, or model-exhaustion filing races evaluation, when both transactions finish, then SQLite order produces exactly the pre-change or post-change valid result. No report commits while a route visible to its transaction remains pending or delivered.

### AC-08 — Kung Fu ring-down

Given an agent receives a lifecycle notice and its applicable test Kung Fu row is `[candidate-A, candidate-B, candidate-C]`, when A is refused and B is out of tokens, then the agent tries C once. It does not retry A or B, use an off-list model, or report exhaustion to Main before C also fails.

This is an agent-policy acceptance fixture. The lifecycle substrate proves only the ordered attempts' durable session/assignment/turn rows and the later agent-authored fact; it does not parse the policy or perform the attempts.

### AC-09 — Main only after typed exhaustion

Given the same episode and a delivered supervisor notice, when the authorized supervisor files `model-candidates-exhausted`, then the fact, one Main marker, and one report event commit atomically. The body cites the fact and says the applicable list was exhausted. A raw failed turn, first unavailable candidate, generic `work-blocked`, error text, provider, or `process:tightbeam` filing produces no such marker.

### AC-10 — No capable supervisor

Given all recorded non-Main agent routes terminate non-delivered and no exhaustion fact exists, when recognition reaches fallback, then Main receives one `agent_supervision_unavailable` marker. It states that model-candidate exhaustion was not established. It does not claim a capability block.

### AC-11 — Authority refusals

Given the affected session itself, an unrelated agent, `process:tightbeam`, an assignment outcome episode, or a turn episode with no delivered agent route, when each files `model-candidates-exhausted`, then the command returns ARC-10's named refusal and writes no fact or report.

### AC-12 — Historical compatibility and rollback

Given existing terminal rows without ARC-01 events, when the new binary starts, then it reports none and changes no existing row. Given new rows, when the predecessor binary starts against the same store, then the shape check passes and it preserves them. Reinstalling the new binary does not duplicate prior notices or reports.

### AC-13 — Trace, security, and deletion

Given one episode in each derived state, including `refused`, when `assignment-get` and `job-trace` run, then they return ARC-09's exact identifiers, states, attempts, and report id. They return no source error or report body. No lifecycle delete command exists, and retirement or disposition deletes no lifecycle evidence.

### AC-14 — Fixture fidelity

Given the reviewed capture source, when the five ARC-14 files are validated, then every named id, timestamp, principal, correlation, state, terminal field, redaction length, and redaction SHA matches the real source. Changing one preserved value or using a hand-written row causes failure. The Fable cancellation fixture creates no lifecycle source.

### AC-15 — Deterministic and packaged gates

The exact implementation commit MUST pass on Linux and macOS under the CI definition whose SHA-256 is `1ccc8176ca9a8b9c2a677eaf31723e3c9602f6790ed8baccb945a5bc2d000e57`:

```text
mix format --check-formatted
scripts/verify_mix.sh
mix test
cargo fmt --check --manifest-path native/tightbeam_cli/Cargo.toml
cargo test --manifest-path native/tightbeam_cli/Cargo.toml
sh packaging/assemble.sh
```

The packaged smoke installs the assembled artifact into a fresh prefix and uses a fresh database. It runs one real available Claude or Codex agent route selected through the live permitted catalog, proves a delivered agent notice suppresses Main, proves an agent-supervision-unavailable Main marker without invoking a model, and proves a typed exhaustion marker after captured real unavailable-candidate evidence on throwaway sessions. A mock harness, source-tree-only run, unavailable candidate retry, or unrecorded credential block does not pass. If no candidate in the smoke activity's allowed row is available, the gate reports `capability_blocked` with the attempted ordered candidates; it does not silently pass or substitute.

### AC-16 — Clause map

| Requirement | Acceptance | Proposed files |
|---|---|---|
| INV-01, INV-03, INV-04 | AC-01 through AC-04, AC-10 | `assignment_lifecycle.ex`, `bubble.ex`, `assignments.ex` |
| INV-02 | AC-08 through AC-11 | `condition_facts.ex`, `assignment_lifecycle.ex` |
| INV-05, INV-06 | AC-05 through AC-07 | `assignment_lifecycle.ex`, `gateway.ex`, existing unique indexes |
| INV-07 | AC-01, AC-03, AC-04, AC-14 | `bubble.ex`, existing supervision/slate seams |
| INV-08, INV-10 | AC-05, AC-09, AC-13 | `event_log.ex`, `projection.ex` unchanged, `job_trace.ex` |
| INV-09 | AC-12 | no schema file change |
| GOAL-01 | AC-01 through AC-07 | source hooks and evaluator |
| GOAL-02 | AC-08 through AC-11 | typed agent fact and atomic report |
| GOAL-03 | AC-14, AC-15 | fixtures, deterministic tests, packaged smoke |
| ARC-01 through ARC-08 | AC-01 through AC-12 | production file set in ARC-15 |
| ARC-09 through ARC-13 | AC-05 through AC-13 | trace, errors, compatibility, observability |
| ARC-14 through ARC-16 | AC-14, AC-15, independent hash-bound review | fixtures, gates, provenance |

## Open Questions

Blocking: none.

Non-blocking: none. NG-04 through NG-06 are explicit follow-on deferrals, not hidden decisions required to build this MVP.
