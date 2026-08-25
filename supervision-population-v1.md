# Computed supervision population v1

Status: revised after independent changes-requested review; awaiting exact-revision re-review

Authority:

- Work item `wi_a57dee58-7dc6-43e4-b36d-a45959e64ad6`.
- Owner assignment `asg_3cf6e187-af6c-4f19-a550-22ae9956aced` and writer assignment `asg_a1d942e3-3882-4c2d-aa58-7f79eca383d8`.
- Owner defect evidence and rulings in the complete work-item trace, including correction `att_5ce36e8c-ce4e-4000-929a-9f54945b0f89` and resumed-design finding `att_48904071-fecc-437f-af36-ea96b66c91e7`.
- `supervision-v1.md`, `supervision-impl-v1.md`, `production-machine-v1.md`, `accountability-constitution-v1.md`, `coordination-fabric-v1.md` sections 5b and 8b, `prodder-provenance-v1.md`, the AVASARALA and MILLER seed guidance and archetypes, and the AVASARALA rename history at spec commit `3999439` and product commit `63e3400`.
- Current 0.2.0 source baseline `f24b5a17caaf738c27a69cf421e1572e3397fd36` on Tightbeam `main`.
- Current specs baseline `85ae5ecb126d54cf7759b4ce37d9459fd7bd0f0f` on `tightbeam-specs/main`.
- Independent review verdict `att_c84e1291-86ca-464a-bd46-6386ab681c2f` and clause table `art_498c59fe`, SHA-256 `83b72e92ba12f9b9d7e8a997c7066409384db43786d8c2619da9103f759a7274`.

This spec is a bounded successor amendment to the authorities above. It replaces only clauses or implementation behavior that use `supervision_entitlements`, a controller row, a watermark, or another supervision side row to decide whether an open assignment belongs to supervision. It also replaces the parent-elevation behavior that deletes an entitlement while the assignment remains open. All timing, production, escalation, provenance, judgment, and audit rules that do not conflict with this amendment remain live.

## Goal

Make the supervised population a deterministic projection of assignment truth and session life.

Every assignment whose `assignments.state` is `open` and whose holder has a matching `sessions.state` of `active` shall belong to the supervised population. The presence, absence, or state of a pacing, entitlement, controller, watermark, claim, retry, or lineage row shall not change that membership.

The implementation shall use supervision side rows only to retain timing, generation, basis, lineage, claim, and retry state. A missing `supervision_entitlements` row shall mean default pacing. A `terminus` row shall mean stopped pacing. Neither condition shall hide the assignment from supervision.

The implementation shall preserve the existing division of authority:

1. The prodder is a deterministic starvation bone. It recognizes durable facts and executes the existing fixed production ladder.
2. Staffed AVASARALA sessions make contextual supervision judgments and retain case law.
3. Staffed MILLER sessions audit conformance from durable evidence.
4. The substrate does not infer motive, quality, blame, exception merit, or promotion policy.

Subtraction ruling: ADD wins. ACCEPT preserves a constitutional patrol defect because deletion or absence of an optional pacing row can hide an open obligation. DELETE of supervision loses required patrol. DELETE of durable pacing rows loses crash-safe due times, claim identity, lineage, and retry state. Renaming or replacing `supervision_entitlements` adds migration risk without changing the governing distinction. The smallest sufficient change is one computed population seam, one default materialization seam, and removal of side-row membership tests.

Wrong-thing-unrepresentable rung: one private population query shall be the only source of watched assignments for liveness cycles, terminal evaluation, startup recovery, controller scheduling, and observability. Those call sites shall accept assignment identifiers returned by that query and shall not construct their own `INNER JOIN supervision_entitlements` population. Exact query-result and race tests shall rail the seam. A new database abstraction or topology registry would cost more than the defect warrants.

## Non-Goals

1. This spec does not change the prod tier sequence, escalation ladder, retry caps, wake prompts, model choice, lineage walk, terminal alert policy, or rules policy.
2. This spec does not define why an assignment is quiet or whether its work is good.
3. This spec does not move AVASARALA judgment or MILLER audit decisions into Elixir, SQL, prompts, timers, or routing rules.
4. This spec does not add a supervisor, sweeper, queue, worker, topology registry, session heartbeat, lease, or liveness oracle.
5. This spec does not hardcode role names, session keys, users, providers, harnesses, operational parents, main sessions, or organization shape into population membership.
6. This spec does not change assignment ownership, transfer policy, retirement policy, or the meaning of `sessions.state`.
7. This spec does not make a closed assignment watched. It does not make an assignment held by a retired or absent session watched.
8. This spec does not make an entitlement row proof that an assignment exists, remains open, or has a live holder.
9. This spec does not parse lifecycle detail text to reconstruct generation, lineage, or policy facts.
10. This spec does not change the `supervision_entitlements` table shape or its accepted value sets.
11. This spec does not change the default `prod_state/2` return keys or value types. It may add the fields specified in R21.
12. This spec does not supersede the attempt identity, settlement, refund, causal-observation, or exact-fact rules in `prodder-provenance-v1.md`. If that spec lands first, this change shall rebase on its authoritative settlement seam without weakening it.
13. This spec does not implement, merge, release, deploy, or change any 0.1.x branch. It defines the 0.2.0 implementation contract.

## Terms

### Open assignment

An **open assignment** is one `assignments` row with `state='open'`. Its exact holder is `assignments.holderKey`.

### Live session

A **live session** is one persisted `sessions` row whose `sessionKey` equals the assignment holder and whose `state='active'` in the same transaction snapshot.

`active` is the complete live-session definition for this spec. A process identifier, node, socket, harness connection, recent turn, timestamp, heartbeat, role, user, provider, operational parent, or main-session name shall not add to or replace it. A missing session row is not live. A row with `state='retired'` is not live.

### Watched population

The **watched population** is the ordered result of this logical query in one database snapshot:

```sql
SELECT a.id, a.holderKey, a.openedAt, a.workItemId
FROM assignments AS a
JOIN sessions AS s ON s.sessionKey = a.holderKey
WHERE a.state = 'open'
  AND s.state = 'active'
ORDER BY a.openedAt, a.id
```

The implementation may select additional assignment or session columns in the same query. It shall preserve the joins, predicates, and ordering above. It shall not join a supervision side table to decide membership.

### Population membership and action eligibility

**Population membership** answers only whether an assignment is watched. **Action eligibility** answers whether a production may claim, schedule, retry, escalate, stop pacing, or wait.

An assignment may be watched while action-ineligible because it has a pending turn, pending wake, work-blocked condition, valid controller, outstanding claim, future due time, or terminus pacing state. These facts constrain the existing production left-hand side. They do not remove population membership.

### Pacing row

A **pacing row** is the existing `supervision_entitlements` row for one assignment. The legacy table name remains for compatibility. The row stores only the current generation, due time, interval, state, last attempted generation, claim clock, basis, terminus time, cause, and principal.

The row is not an entitlement to be supervised. The assignment/session join grants no privilege and records no judgment. It computes the universe that the constitutional patrol must inspect.

### Default pacing

**Default pacing** is the effective pacing state for a watched assignment that has no pacing row.

Default pacing uses the running Supervision process's positive `sweep_ms` as `supervisionIntervalMs`. Its due time is `materializationClock + sweep_ms`. This rule preserves the current recovery-backfill interval and prevents a release entry from immediately prodding the complete historical missing-row population.

The ordinary default basis is `recovery_backfill:<assignmentId>`, the default cause is `recovery_backfill`, and the principal is `process:tightbeam`. A valid persisted receipt, parent-transfer, or controller fact may supply its existing generation and basis. It may constrain action eligibility. It shall not turn absence into invisibility.

### Default materialization

**Default materialization** is the single transactional operation that inserts a missing pacing row for a watched assignment. It shall use `INSERT ... ON CONFLICT DO NOTHING` or an equivalent uniqueness-preserving insert, then reread the winning row in the same transaction.

The materializer derives its generation as the maximum of 1 and the assignment's numeric `generation` or `chargedGeneration` values in `supervision_liveness_receipts`, `supervision_progress_absorptions`, and `supervision_liveness_sidecar`. An accepted retirement transfer whose own `chargedGeneration` is null uses the greatest non-null charged generation in its predecessor evidence, or 1 when none exists. The materializer shall not parse lifecycle prose.

The materializer chooses the basis in this order:

1. A valid accepted transfer at the selected generation supplies its scheduled wake kind, wake id, `parent_elevated` cause, and principal. Among equal-generation transfers, the newest valid transfer wins.
2. Otherwise, the highest `receiptId` in the selected generation supplies `basisKind='progress'`, `basisId='receipt:<receiptId>'`, `cause='progress'`, and the process principal.
3. Otherwise, the assignment supplies the recovery-backfill basis, cause, and process principal.

The materializer inserts that generation with `state='armed'`, the default due time, and the current positive interval. It first runs the existing receipt-cursor baseline seam, so historical source rows that supervision never accepted do not become new resets. Existing controller facts remain action gates.

After this release entry, product code shall not delete a pacing row while its assignment remains open. This rule makes generation monotonic during one uninterrupted open lifecycle and makes a later missing row an explicit default case rather than a normal transfer representation. A lawful close followed by `reopen-assignment` starts the fresh lifecycle specified in R9.

### Stored pacing states

The current stored states retain their meanings:

- `armed`: the generation has a due time and can be claimed after existing gates pass.
- `claimed`: the exact generation and claim clock are held by the existing claim-and-drain flow.
- `terminus`: timer pacing has stopped for the current generation. The assignment remains watched until assignment closure or holder retirement removes it from the population query.

### Qualifying reset

A **qualifying reset** is one durably typed liveness fact accepted by current supervision law: an `artifact`, `work_item_update`, `verdict`, or `checkpoint` row recorded in `supervision_liveness_receipts`.

A progress attest whose only new evidence is prose, a later terminal, prompt text, elapsed time, a process message, a bare socket event, or an untyped lifecycle note is not a qualifying reset.

### Controller and transfer state

**Controller state** is the current durable wake, turn, and `supervision_liveness_sidecar` evidence for a prod or escalation controller. **Transfer state** is the current accepted lineage evidence derived from those rows.

Controller and transfer state may defer, settle, rebase, or stop a pacing action under existing policy. It may populate lineage and claim provenance. It shall not define population membership. Parent elevation shall retain or re-arm the pacing row instead of deleting it.

### Judgment and conformance

A **judgment** is a staffed AVASARALA conclusion that requires context beyond the deterministic facts and fixed productions. A **conformance finding** is a staffed MILLER conclusion about whether behavior and evidence obey the authoritative law.

Neither is a population-query result. The computed population gives both minds complete evidence without making their decisions.

## Assumptions

1. The current 0.2.0 schema permits exactly `active` and `retired` session states.
2. Assignment open and close operations and session retirement remain durable database transitions.
3. `assignments.id` is unique, `supervision_entitlements.assignmentId` is a primary key, and the existing transaction wrapper provides one SQLite writer order.
4. The Supervision process receives one positive `sweep_ms`. That value remains the default interval source.
5. Existing wake, turn, sidecar, receipt, absorption, watermark, and production-counter rows remain the authoritative facts for their current narrow purposes.
6. The existing assignment-open transition creates a pacing row in the assignment-open transaction. Default materialization covers migration dirt, crash-era legacy state, and any later missing-row observation.
7. Existing retirement handling closes or disposes open assignments held by retired sessions. The population query still excludes any transient or corrupt open/retired pair until that repair commits.
8. Product code is the only supported writer of supervision side state. Direct external deletion is outside the compatibility contract, but a watched missing row still receives default pacing instead of invisibility.
9. The 0.2.0 product may implement `prodder-provenance-v1.md` before, with, or after this amendment. Population recognition remains orthogonal to attempt settlement.

## Invariants

### R1 — Population source

The implementation shall compute watched population from the exact open-assignment/live-session relation in **Watched population**. No pacing, entitlement, controller, watermark, receipt, claim, retry, transfer, wake, turn, artifact, or attest row shall be required for membership.

### R2 — One population seam

`liveness_cycle/2`, `oldest_supervised_assignment/2` or its replacement, terminal sweep and evaluation, `recover_liveness/1`, controller scheduling, and supervision observability shall consume one private `watched_assignments_in_txn/1` seam or its exact single-assignment predicate. They shall not contain independent population SQL.

### R3 — Snapshot consistency

Each recognize-and-claim decision shall read assignment state, holder session state, pacing state, and action gates in one transaction snapshot. A query result read before that transaction shall be advisory only.

### R4 — Missing row

When a watched assignment has no pacing row, any path that needs pacing or controller coherence shall call default materialization in its current transaction. It shall not return `unarmed`, `idle`, `none`, or `parent_elevated` solely because the row is absent.

### R5 — Side-row non-authority

Deleting, omitting, terminating, claiming, settling, or failing to create a supervision side row shall not change the watched-population query result.

### R6 — Assignment open

The assignment-open transaction shall continue to create the assignment and its initial generation-1 armed pacing row atomically. If the insert races with default materialization, the primary-key winner shall be reread and used; the transaction shall not create a second generation or second claim.

### R7 — Assignment close

Closing an assignment shall remove it from the watched population at the assignment-state commit. Cleanup of pacing, controller, watermark, receipt-state, or retry rows may occur in the same transaction or later. Delayed cleanup shall delete or change a side row only while the same transaction still observes `assignments.state='closed'`; it shall not delete pacing that a later `reopen-assignment` created. Stale side rows shall not restore membership.

### R8 — Session retirement

Retiring a session shall remove its held assignments from the watched population at the session-state commit. Existing retirement disposition rules remain authoritative. Any obligation that those rules leave open under an active holder shall enter the population only through its assignment/session relation, not through a pacing-row write.

### R9 — Assignment reopen

The existing authorized `reopen-assignment` transition shall restore watched membership and fresh pacing in the same transaction that records `assignment_reopenings` and changes the assignment from closed to open. It shall retain the current holder and current authorization, reason, work-item, and active-holder checks.

Reopen shall complete the existing terminal-disposition cancellation of stale controllers and clearing of the pending watermark before it writes fresh pacing. It shall preserve the receipt cursor and durable receipt, attempt, lifecycle, counter, and reopening history. It shall use one `INSERT ... ON CONFLICT(assignmentId) DO UPDATE` or equivalent single-row upsert to replace any stale pacing row from the closed lifecycle. The stored result shall be exactly one generation-1 `armed` row with `dueAt=reopenClock+sweep_ms`, the positive current interval, `basisKind='assignment_open'`, the assignment id as basis id, `cause='assignment_open'`, and the reopening principal. It shall clear `lastAttemptGeneration`, `claimClock`, and `terminusAt`. An absent row and a stale `armed`, `claimed`, or `terminus` row shall produce the same fresh row. Reopen shall neither retain nor advance the closed lifecycle's generation.

The assignment-state update, reopening history, pacing replacement, existing assignment-open liveness trigger, and existing work-item bracket cancellation shall commit or roll back together. Concurrent delayed close cleanup shall serialize through the R7 closed-state predicate. A losing reopen shall return the existing named transition error and leave both assignment and pacing state unchanged.

### R10 — Parent elevation

Admitting a valid parent elevation shall retain the armed generation that `controller_scheduled` already created. It shall settle the sidecar without advancing that generation or deleting the pacing row. A missing row at this edge shall use default materialization from the controller evidence before settlement. A pending or running parent controller may make the assignment action-ineligible, but the assignment remains watched.

Accepted-transfer lookup and parent-target-retirement recovery shall select from wake, turn, and sidecar evidence. They shall not require the pacing row to be absent.

### R11 — Terminus

Terminus shall update the pacing row to `state='terminus'` with no due time or interval, as the current schema requires. It shall leave the assignment open, leave population membership unchanged, clear the current claim and pending watermark under existing rules, and emit the existing terminus evidence. Action-candidate selection shall skip terminus while continuing to inspect later watched assignments.

### R12 — Terminus reset

The first qualifying reset accepted after terminus shall atomically advance the generation, restore `state='armed'`, store the new durable basis, set the positive current interval and due time under the existing reset rule, clear ladder counters under the existing repair seam, and leave one reset receipt. Concurrent duplicate observations shall advance the generation once.

### R13 — No implicit terminus reset

A sweep, process restart, row read, AVASARALA case comment, MILLER finding, or mere continued assignment openness shall not reset terminus. These facts preserve membership only.

### R14 — Ladder semantics

Default materialization shall not increment `attemptCount`, `prodCount`, `deniedStreak`, `attestCount`, or a prodder-provenance counter. A claim and delivered outcome shall continue to affect the ladder exactly once under existing law. A qualifying reset shall reset the current ladder epoch exactly as the current typed liveness-receipt seam requires.

### R15 — Claim race

Only one transaction may change one armed generation to claimed. It shall compare assignment id, generation, due time, state, and evaluation clock as the current claim CAS requires. A losing cycle shall reread or return duplicate; it shall not schedule a second wake.

### R16 — Close and retirement races

Before an action commits, the act transaction shall reread that the assignment is open and that its current holder session is active. It shall also apply the existing pending-turn, pending-wake, work-blocked, controller, and lineage gates. Closure or holder retirement that wins the writer order shall make the act stale.

### R17 — Crash recovery

Every Supervision start shall run the existing recovery transaction. Recovery shall run the existing lineage normalization and legacy parent-retirement migration before it materializes missing pacing. It shall then enumerate the watched population, materialize each missing pacing row, and apply existing claimed-generation, controller, transfer, receipt, and retirement repair. Runtime cycles shall use the same default materialization, so recovery is not the only path that prevents invisibility.

### R18 — Idempotent recovery

Repeating recovery without an intervening durable fact shall preserve the same population, generation, due time, claim, controller, and retry state. It shall not emit a second materialization or reset event.

### R19 — Current schema compatibility

The implementation shall retain the current `supervision_entitlements`, `supervision_liveness_sidecar`, `supervision_liveness_receipt_state`, `supervision_liveness_receipts`, `supervision_liveness_checkpoint_bindings`, `supervision_progress_absorptions`, `assignment_prods`, and `supervision_watermarks` shapes. It shall satisfy the current checkpoint-binding trigger by materializing default pacing before the binding insert. It shall not weaken that trigger to accept a closed assignment or retired holder.

### R20 — Migration and rollback

The first new-binary recovery shall backfill all watched missing rows in its normal transaction and record their existing lifecycle basis. Correctness shall not depend on completing a separate bulk migration. No table rewrite, schema-shape stamp change, or offline data conversion is required.

An old 0.2.0 binary may reopen the database because the schema remains byte-compatible. Rollback restores the old population defect for any row later missing. The implementation shall expose the read-only internal function `Tightbeam.Supervision.rollback_precheck/1` with return type `:ok | {:error, [map()]}`. In one read transaction, the function shall consume `watched_assignments_in_txn/1` and left-read `supervision_entitlements` for those exact results; it shall not restate the population join. It shall return `:ok` when no watched pacing row is absent. Otherwise, it shall return `{:error, rows}`, where each row contains `assignmentId`, `holderKey`, and `openedAt`, ordered by `openedAt, assignmentId`.

Before an operator replaces the running new binary with an old 0.2.0 binary, the operator shall invoke `Tightbeam.Supervision.rollback_precheck(Tightbeam.DB)` through the installed release wrapper's existing `rpc` command, with the same base-directory, port, and node environment used to start that gateway. The operator shall admit rollback only after that invocation returns `:ok`; a connection failure or `{:error, rows}` shall refuse rollback. This seam adds no Tightbeam CLI verb, gateway wire verb, remote endpoint, or database write. Rows created by this release require no reverse conversion.

### R21 — Observability

`prod_state/2` shall continue to return its current fields. For an existing assignment it shall add:

```text
supervisionWatched        boolean
supervisionPacingSource   "stored" | "default"
```

It shall set `supervisionWatched=true` exactly for the R1 relation. Before materialization, a missing row shall report `supervisionState="default"`, the read-only derived generation and basis, null due time and interval, and `supervisionPacingSource="default"`. This read shall not start or move a clock. After materialization it shall report `"stored"`. A terminus row shall report `supervisionWatched=true`, `supervisionState="terminus"`, and `supervisionPacingSource="stored"`. A closed assignment or an assignment without a live holder shall report `supervisionWatched=false` if existing counter or side state causes `prod_state/2` to return a map.

The implementation shall emit one `supervision_entitlement_materialized` lifecycle event for a successful missing-row insert. Its subject shall be the assignment id. Its detail shall name generation, basis, due time, interval, cause, and principal using the existing lifecycle detail convention. It shall not emit an event when another transaction already inserted the row.

### R22 — Security and authorization

This amendment shall add no Tightbeam CLI verb, gateway wire verb, remote endpoint, write permission, or caller-controlled population predicate. The read-only internal rollback function in R20 is callable only through the release wrapper's existing local `rpc` seam and grants no new mutation authority. Only existing authorized assignment/session transitions can change membership. The process principal may materialize pacing only after the R1 query proves the assignment is watched. Caller-supplied role names, lineage, session liveness, due times, or topology shall not be trusted as membership evidence.

### R23 — Deterministic bone boundary

The prodder shall restrict itself to R1 membership, stored durable gates, the transaction clock, the configured interval, and the existing fixed production policy. It shall not classify work quality, intent, fault, blame, exception merit, or whether a human deserves escalation.

### R24 — Staffed-mind boundary

AVASARALA may inspect the complete watched population and durable action evidence and may issue judgments through existing staffed-role mechanisms. MILLER may audit the same evidence and implementation conformance. Neither role's presence, staffing topology, current session key, or conclusion shall be embedded in the population query or required for deterministic pacing.

### R25 — Failure behavior

An impossible duplicate pacing row, malformed stored pacing row, malformed accepted transfer, or stale claimed generation shall retain the current named incompatibility or invariant-failure behavior. The implementation shall not reinterpret malformed state as “not watched.” A transient database failure shall roll back the materialization, claim, counter, watermark, wake, and event writes together.

## Architecture

### 1. Population projection

Add one private `watched_assignments_in_txn/1` query with the exact R1 relation and ordering. Add one exact single-assignment form for `prod_state/2` and act-time rechecks. Both forms shall share the same predicates.

The liveness timer shall start from this projection. Terminal processing shall start from the holder's rows in this projection. Startup recovery shall start from this projection. No path shall first select armed or claimed entitlements and then treat that subset as the universe.

After default materialization, action selection may filter the computed population by pacing state and existing action gates. It shall select one due armed assignment by `dueAt, openedAt, id`. A terminus or future-due assignment remains watched but does not block a later due assignment. A side-table join used only after population enumeration is an action query, not a population query.

### 2. Effective pacing

For each watched assignment, supervision shall left-read its pacing row:

1. An armed or claimed row supplies stored pacing and claim state.
2. A terminus row supplies stopped pacing.
3. No row supplies the default projection.

A read-only projection may report default pacing without writing. Any recognize, controller, checkpoint, or recovery path that requires a row shall call `materialize_default_pacing_in_txn/3` before continuing.

The materializer shall validate the assignment/session relation again. It shall derive accepted transfer lineage through the existing accepted-transfer query. It shall insert once, reread once, and return the stored winner. The implementation shall not add a second recovery worker or a second materialization implementation.

### 3. Recognition and action

Recognition proceeds in this order inside the transaction that claims work:

1. Prove the assignment is in R1.
2. Read or materialize effective pacing.
3. Stop if pacing is terminus.
4. Stop if due time is in the future.
5. Apply the existing production left-hand-side gates.
6. CAS the exact armed generation to claimed.
7. Persist the existing pending watermark and attempt state atomically.

Drain, scheduling, settlement, refund, and causal observation remain governed by the current production and provenance specs. They reread assignment/session truth before the act commits.

### 4. Controllers and lineage

Controller scheduling materializes pacing before the current coherence writes. A scheduled controller retains its sidecar and charged generation. Parent elevation settles the controller and retains the already-rearmed pacing generation instead of clearing it. A parent turn, pending wake, or accepted transfer can defer an action through current gates. It cannot cause the population query to omit the child assignment.

`transferred_assignments_in_txn/2` or its replacement shall enumerate valid accepted transfers from transfer evidence. It shall not use `supervision_entitlements.assignmentId IS NULL` as the transfer discriminator.

`prod_state/2` shall project pacing and transfer facts together. It shall not use the current mutually exclusive rule “pacing row, otherwise transfer projection.” Existing transfer fields remain available when a pacing row exists.

### 5. Reset and terminus lifecycle

Assignment open creates generation 1. Each accepted typed liveness receipt, controller settlement, parent-retirement rearm, policy denial rearm, no-terminal rearm, or terminal rebase keeps its current generation and due-time rule.

Terminus stops timer pacing but preserves the row and population membership. A qualifying reset after terminus uses the same receipt transaction that accepts the durable source. It advances once, clears the current ladder epoch under the existing receipt rule, and re-arms. A later terminal does not reset terminus. Closing the assignment ends that open lifecycle. A lawful reopen starts a fresh lifecycle by replacing any stale pacing state under R9. Retiring its holder removes it from the live-holder population while existing disposition runs.

### 6. Upgrade, recovery, and rollback

The release uses the current schema. On first and later starts, recovery runs current legacy normalization before it enumerates R1 and repairs missing pacing. A missing row with accepted receipt or transfer evidence uses that exact numeric generation and basis. Another missing row receives recovery-backfill defaults.

Runtime recognition uses the same repair, so a row that becomes absent after startup cannot wait for another boot. Because the release does not alter table SQL, rollback needs no schema action. `Tightbeam.Supervision.rollback_precheck/1`, called through the installed release wrapper's existing local `rpc` command while the new gateway runs, provides the exact admission seam in R20.

### 7. Evidence and minds

The deterministic substrate exposes membership, pacing source, stored state, lineage, gates, attempts, outcomes, and lifecycle events. AVASARALA consumes those facts when a case needs contextual judgment. MILLER consumes them when auditing conformance. The substrate neither issues their conclusions nor selects their staffed sessions.

## Acceptance

Each test shall use a fixed database clock and a fixed positive `sweep_ms`. Each test shall assert durable rows and observable return values, not log text timing or process sleeps.

### A1 — Complete population

Given two active sessions, one retired session, three open assignments held by those sessions, and one closed assignment, when the population seam runs, then it returns exactly the two open assignments held by active sessions in `openedAt, id` order.

Falsifies: an open/live assignment is absent; an open/retired, open/missing-holder, or closed assignment is present; ordering differs.

Traces: R1, R2, R7, R8.

### A2 — Entitlement state cannot filter membership

Given four open assignments held by active sessions whose pacing states are armed, claimed, terminus, and missing, when the population seam runs, then it returns all four exactly once.

Falsifies: any state or missing row changes the result.

Traces: R1, R4, R5, R11.

### A3 — Runtime missing-row default

Given an open assignment held by an active session, no pacing row, transaction clock `70_000`, and `sweep_ms=60_000`, when a runtime liveness cycle recognizes it, then one armed generation-1 row exists with `dueAt=130_000`, recovery-backfill basis and cause, and process principal. No claim or counter change occurs before that due time.

Falsifies: no row, invisibility until restart, a due time other than `130_000`, or a counter change.

Traces: R4, R14, R17, R18.

### A4 — Concurrent materialization

Given A3 state and two serialized cycle requests at the same fixed clock, when both execute, then one pacing row and one materialization lifecycle event exist; at most one generation claim and one pending attempt exist.

Falsifies: duplicate events, generation 2 caused only by the race, or two claims.

Traces: R6, R15, R21, R25.

### A5 — Restart recovery

Given one ordinary missing row, one missing row with valid accepted parent-transfer evidence, and one stored claimed row, all for watched assignments, when recovery runs twice, then legacy normalization runs first, the ordinary row uses recovery-backfill defaults, the transfer row uses the maximum exact numeric generation and accepted lineage basis, the claimed row follows current claim recovery, and the second run changes none of those results.

Falsifies: omission, lifecycle-text parsing, duplicate generation advance, due-time drift, or a second event.

Traces: R17, R18, R25.

### A6 — Terminus remains watched

Given one holder has an older watched terminus assignment and a younger watched armed assignment that is due, when timer and terminal processing run, then both assignments are present, elapsed time does not re-arm the terminus row, the due assignment can claim, and `prod_state/2` reports watched terminus stored pacing for the older assignment.

Falsifies: omission, timer rearm of terminus, starvation of the younger due assignment, or `supervisionWatched=false`.

Traces: R11, R13, R21.

### A7 — Terminus reset once

Given A6 and one qualifying liveness receipt, when two cycles observe that receipt, then one next generation is armed, the receipt is stored once, the current ladder epoch resets once, and the second cycle is a duplicate.

Falsifies: terminus persists after accepted repair, two generations, two receipts, or unchanged ladder counters.

Traces: R12, R14, R15.

### A8 — Non-reset evidence

Given A6, when a sweep, restart, later holder terminal, untyped lifecycle note, AVASARALA comment, or MILLER finding occurs without a qualifying reset, then terminus and counters remain unchanged while membership remains true.

Falsifies: any listed observation re-arms or removes the assignment.

Traces: R13, R23, R24.

### A9 — Close race

Given a due watched assignment, when closure commits before the claim transaction's act-time reread, then no claim, watermark, wake, materialization event, or prod counter commits and the assignment is absent from the next population read.

Falsifies: any action survives the winning close.

Traces: R3, R7, R16, R25.

### A10 — Retirement race

Given a due watched assignment, when holder retirement commits before the act-time reread, then no old-holder action commits, the assignment is absent from the population relation, and existing retirement disposition runs without using a pacing row as membership proof.

Falsifies: an old-holder prod or population inclusion after retirement.

Traces: R8, R16.

### A11 — Reopen replaces stale pacing

Given an authorized closed assignment held by an active session, a stale pending controller and watermark, and, in separate cases, an absent, armed, claimed, or terminus pacing row left from its closed lifecycle, when `reopen-assignment` commits at clock `80_000` with `sweep_ms=60_000`, then the assignment is open and watched, one reopening history row exists, the stale controller is canceled, the pending watermark is clear, the receipt cursor and historical evidence are unchanged, and exactly one pacing row is armed at generation 1 with `dueAt=140_000`, assignment-open basis and cause, the reopening principal, and null attempt, claim, and terminus fields. When delayed close cleanup serializes after this commit, its closed-state predicate changes nothing.

Falsifies: reopen refusal caused only by the stale row, retained or advanced old generation, retained claim or terminus state, missing history, pacing deletion after reopen, duplicate pacing, or a partial commit.

Traces: R7, R9, R15, R25.

### A12 — Parent elevation retains pacing

Given `controller_scheduled` already re-armed generation G and an escalation controller is admitted to a parent turn, when parent-elevation settlement commits, then the assignment remains watched, pacing generation G remains armed with its stored due time, the sidecar settles with exact lineage, and no second controller is scheduled while current gates report the parent turn pending or running. When that parent target later retires, transfer recovery finds the assignment from transfer evidence even though its pacing row exists.

Falsifies: pacing-row deletion, generation G+1 from settlement alone, disappearance, lost lineage, missing retirement recovery, or duplicate controller.

Traces: R10, R15, R19.

### A13 — Checkpoint with initially missing pacing

Given a valid running held assignment and checkpoint wake but no pacing row, when the checkpoint transaction runs, then it materializes pacing first, the unchanged coherence trigger accepts exactly one binding, and a later receipt absorption advances one generation.

Falsifies: transaction rollback solely for missing pacing, trigger weakening, or two bindings.

Traces: R4, R12, R19.

### A14 — Controller with initially missing pacing

Given a watched assignment and no pacing row, when the full recognition path reaches valid controller scheduling after the default due time, then pacing materialization, claim, wake, sidecar, and watermark commit through their existing transaction boundaries. Forced failure in each transaction leaves that transaction's writes rolled back and preserves the existing replay contract. A direct `controller_scheduled` transition with no claimed generation remains invalid and rolls back its wake row.

Falsifies: invisibility, a controller without a claim, a partial transaction, or a duplicate wake.

Traces: R4, R15, R19, R25.

### A15 — Stale side rows cannot create population

Given a closed assignment and a retired-holder assignment with armed pacing, pending-controller, receipt, and retry rows, when all population consumers run, then neither assignment is selected and no action commits.

Falsifies: any side row restores membership.

Traces: R5, R7, R8.

### A16 — Observability matrix

Given watched assignments with stored armed, stored claimed, stored terminus, and missing pacing, plus a closed assignment with counters, when `prod_state/2` runs, then the four watched rows report `supervisionWatched=true`; the missing row reports state `default`, source `default`, derived generation and basis, null due time and interval, and no write; the stored rows report source `stored`; and the closed row reports watched false.

Falsifies: a missing map, a write from the read-only projection, a false watched value, or a changed existing field type.

Traces: R21.

### A17 — Query-shape rail

Given the implementation source, when the supervision query-shape test inspects the named population seam and its consumers, then the seam contains the assignment/session join and exact state predicates, and no consumer selects its population through an inner join to `supervision_entitlements` or a sidecar.

Falsifies: `liveness_cycle/2`, terminal selection, recovery, controller scheduling, or observability contains an independent side-row membership predicate.

Traces: R1, R2.

### A18 — Topology and mind independence

Given the same assignment and session rows but changed role names, providers, harnesses, operational parents, staffed AVASARALA sessions, or staffed MILLER sessions, when the population seam runs, then its result is unchanged. Given a session-state or assignment-state change, the result changes according to R1.

Falsifies: topology or staffed-mind presence affects membership; assignment/session truth does not.

Traces: R22, R23, R24.

### A19 — Existing ladder and provenance conformance

Given identical durable action facts and a present pacing row, when the pre-change and post-change production paths run, then they select the same branch, rung, target, counter transition, attempt identity, settlement, refund, and cause observation. The only allowed difference is additive population/pacing-source observability.

Falsifies: this amendment changes prodder policy or provenance semantics.

Traces: R14, R23 and `prodder-provenance-v1.md`.

### A20 — Upgrade and rollback fixture

Given a current 0.2.0 database fixture containing stored, missing, accepted parent-transfer, terminus, closed, reopened, and retired-holder cases, when the new binary boots, then it passes current schema-shape validation and A1–A16 without a table rewrite. While that new gateway runs, when the test invokes `Tightbeam.Supervision.rollback_precheck(Tightbeam.DB)` through the installed release wrapper's existing `rpc` command, then it returns `{:error, rows}` with exact ordered assignment, holder, and open-clock fields while any watched pacing row is missing. After new-binary recovery materializes all watched missing rows, the same invocation returns `:ok`; the old binary then opens the same database without reverse conversion. A release-wrapper connection failure refuses rollback.

Falsifies: a shape change, required offline migration, unsafe rollback signal, or unreadable new rows.

Traces: R19, R20.

### A21 — Full regression boundary

The implementation change shall pass the full current 0.2.0 test suite, including supervision, schema-shape, assignment reopen, session retirement, wake delivery, work-item trace, and provenance tests. The implementation shall add the deterministic cases above to the existing supervision and schema-query test modules rather than creating a second behavioral harness.

Falsifies: any existing authoritative behavior changes outside the bounded amendment.

Traces: R1–R25.

## Open Questions

None. The owner rows and independent review resolve the population source, default, terminus, reopen lifecycle, rollback invocation, removal of the unsupported active-holder transfer case, role boundary, target release, and review lane. Implementation questions shall amend this canonical spec before code changes. A materially new scope or monetary decision returns to the owner; answerable mechanics remain in the assigned lane.
