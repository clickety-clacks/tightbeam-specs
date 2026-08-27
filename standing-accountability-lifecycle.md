# Standing accountability lifecycle

Status: canonical MVP spec for `wi_0552815b-e5b5-4c56-90ed-c40825c3b9ad`.

This spec adds one assignment lifecycle type. It amends the assignment fields in
`rest-state-api-v1-wire-schema.md` and the `assign` and `dispatch` families in
`cli-surface-v1.md`. Those documents remain authoritative outside this delta.

## Goal

G1. Tightbeam represents ongoing accountable custody as a typed standing assignment
that has no completion target or deadline.

G2. Tightbeam distinguishes a standing assignment from a discrete assignment in
stored state, gateway responses, REST state, Firehose state, and CLI input and output.

G3. Tightbeam excludes a standing assignment from the two existing mechanisms that
ask whether an assignment filed progress or completed lately: supervision's turn-end
prod ladder and the effort-without-effect check-in.

G4. Tightbeam keeps a standing assignment open until its holder surrenders it or an
authorized principal revokes it.

## Non-Goals

NG1. This MVP does not add a heartbeat, reaffirmation cadence, due date, completion
target, scheduler, reminder, or new escalation ladder for standing assignments.

NG2. This MVP does not change the thresholds, receipts, prompts, counters, or
escalation order for discrete assignments.

NG3. This MVP does not change `effectKind`. The kind of effect and the lifecycle of
the obligation remain independent facts.

NG4. This MVP does not reclassify an existing assignment. A row that predates this
feature has the discrete lifecycle.

NG5. This MVP does not change work-item state, assignment custody, holder-retirement
handling, assignment surrender, assignment revocation, or assignment reopening except
where this spec states the standing lifecycle behavior.

NG6. This MVP does not create a new work object. Assignments remain the sole custody
row for this scope.

NG7. This MVP does not set a release target or authorize implementation, deployment,
or mutation of hosted state.

## Terms

### T1 — Lifecycle kind

`lifecycleKind` is an immutable assignment field with exactly two values:

- `discrete`: custody for work that can reach the `completed` outcome;
- `standing`: custody for an ongoing responsibility that has no `completed` outcome.

The gateway wire name is `lifecycleKind`. The CLI flag is `--lifecycle-kind`.
Omission means `discrete`.

### T2 — Discrete assignment

A discrete assignment is the existing assignment lifecycle. It can close as
`completed`, `surrendered`, or `revoked`. The existing supervision and effort
check-in rules continue to apply.

### T3 — Standing assignment

A standing assignment is an open assignment whose `lifecycleKind` is `standing`.
Its open row names the current accountable holder. It can close as `surrendered` or
`revoked`. It cannot close as `completed`.

### T4 — Standing accountability trigger

A standing accountability trigger is the existing open standing assignment row with
an active holder. Its internal typed-reference form is:

```json
{"kind":"standing_accountability","id":"<assignmentId>"}
```

The trigger proves that linked work remains owned when a wake-cancellation receipt
names that assignment or its linked work item as primary work. It does not carry a
clock and does not arm a monitor.

### T5 — Completion-oriented monitor

A completion-oriented monitor is either:

1. a `supervision_entitlements` generation that can reach a prod or escalation; or
2. an `effort_checkin_generations` generation that can reach an effort check-in.

## Assumptions

A1. The reconciled disposition for this work is KEEP. Attest
`att_b0c48d26-d2b1-4497-aa3d-0b27bf233cbf` found no typed completion-free lifecycle
and no deterministic no-prod regression on canonical main. This spec preserves that
ruling and does not revive the superseded CLOSE interpretation.

A2. The inspected product baseline is Tightbeam main
`01c52e1659d52ee16d3ef90202c2df6607fcf327`. At that revision, each assignment has
an `effectKind`, each assignment open or reopen arms supervision, `dispatch` also
arms effort check-in, and the turn-end production falls back to the oldest open
assignment.

A3. Existing assignment, attest, wake-cancellation, REST, Firehose, and CLI
projections remain available to carry one new enum field and one new liveness-trigger
enum value.

A4. Holder retirement already disposes each open assignment through the recorded
revocation path. This feature relies on that existing exit.

## Invariants

I1. Each assignment has exactly one lifecycle kind. A new assignment stores the kind
in the same transaction that stores the assignment. A legacy assignment reads as
`discrete`.

I2. The lifecycle kind does not change after assignment creation. Reopening an
assignment preserves its original kind.

I3. A standing assignment has no completion target, completion deadline, completion
attest, or `completed` outcome.

I4. A standing assignment accepts progress and verdict attests under their existing
authority rules. The presence or absence of either attest kind does not arm a
completion-oriented monitor.

I5. A standing assignment can close only through the existing surrender or revocation
seam. Each close retains its existing principal, cause, and papertrail.

I6. A review assignment is discrete. The gateway refuses a request that combines
`reviewsAssignmentId` with `lifecycleKind = standing`.

I7. A standing assignment creates no row in `supervision_entitlements` and no row in
`effort_checkin_generations`. Reopening it creates neither row.

I8. The turn-end supervision production selects the oldest open discrete assignment
for the holder. An older standing assignment does not hide a newer discrete
assignment. If the holder has only standing assignments, the production records no
claim, prod, escalation, completion rail action, or decision request.

I9. A wake-cancellation receipt can use `standing_accountability` only when its id
names an open standing assignment whose holder is active and the receipt's primary
work is that assignment or its linked work item. The receipt retains the existing
cause and requester principal fields.

I10. Each canonical assignment projection exposes `lifecycleKind`. A consumer never
infers it from `effectKind`, subject text, attests, age, or monitor rows.

I11. Omission preserves existing behavior. An `assign` or `dispatch` request without
`lifecycleKind` creates a discrete assignment and produces the monitor rows that its
verb produces at the A2 baseline.

## Architecture

### AR1 — One immutable type seam

The `assign` and `dispatch` creation transaction accepts `lifecycleKind`, validates
the two-value enum, stores it with the assignment, and returns it. No later mutation
verb changes the value.

The gateway returns `invalid_lifecycle_kind` for another value. It returns
`standing_review_conflict` when a review request asks for the standing lifecycle.
Both refusals create no assignment, monitor, wake, message, or Firehose state event.

### AR2 — Standing accountability without a clock

Assignment creation and reopening branch on the stored lifecycle kind in the same
transaction as the lifecycle action. The discrete branch keeps the existing
supervision entitlement. The standing branch uses T4 as the liveness trigger and
does not create a supervision entitlement.

Work-item bracket cancellation accepts `standing_accountability` as a liveness
trigger. Its validator reads the assignment type, open state, current holder state,
and work-item relation from durable rows. The validator refuses a stale or mismatched
trigger.

### AR3 — Monitor admission

The effort check-in arm, rearm, and transfer queries admit discrete assignments only.
The supervision turn-end candidate query admits discrete assignments only and orders
those candidates by `(openedAt, id)` as it does now.

When a holder has no open discrete assignment, supervision returns the deterministic
no-match reason `standing_only` if that holder has an open standing
assignment. The no-match path writes no watermark or completion-oriented lifecycle
row.

The lifecycle read and the decision to arm a monitor occur in the same transaction as
assignment creation or reopening. The immutable lifecycle kind governs later monitor
claims without a second classification decision.

### AR4 — Completion refusal and lawful exits

The assignment transition seam refuses a completion attest against a standing
assignment with code `standing_has_no_completion` and this message:

```text
standing assignment <assignmentId> has no completion outcome; file surrender or ask an authorized principal to revoke it
```

The persistence constraint also refuses a committed assignment shape that combines
`lifecycleKind = standing` with `outcome = completed`.

The refusal leaves the assignment open and writes no attest, close, wake, cancellation,
or state event. Existing surrender and revocation authority applies unchanged.

### AR5 — Wire and CLI visibility

The CLI accepts `--lifecycle-kind discrete|standing` on `assign` and `dispatch`. Its
help names both values and states that omission selects `discrete`. The CLI sends the
camel-case `lifecycleKind` gateway parameter and performs no local inference.

The gateway's `assign`, `dispatch`, `assignment-get`, `assignments`,
`work-item-get`, and `work-item-trace` assignment objects include non-null
`lifecycleKind`. The CLI exposes the applicable results from `assign`, `dispatch`,
`assignments`, `work-item-get`, and `work-item-trace` without removing that field.
REST assignment resources and Firehose assignment state resources include the same
field and enum. In the canonical REST assignment field order, `lifecycleKind`
follows `effectKind` and precedes `derivedStatus`. Wake-cancellation trace objects may
expose `livenessTriggerKind = standing_accountability` and
`livenessTriggerId = <assignmentId>`.

Existing creation callers remain input-compatible because omitted input defaults to
`discrete`. The new output member is additive.

### AR6 — Subtraction ruling and operating pattern

ADD wins because deleting assignment custody would leave standing intent unowned,
while accepting completion prods would make supervision report a known falsehood.
The design adds no scheduler or parallel work object.

Reusing `supervision_entitlement` as the standing trigger would falsely represent an
armed completion monitor, so T4 uses the open assignment row itself.

Operating pattern: the CLI help is the instruction surface for selecting this type.
This MVP requires no operating-manual or Kung Fu amendment.

## Acceptance

### AC1 — Explicit standing creation and projection (G1, G2; I1, I10; AR1, AR5)

**Given** a fresh database and an active holder, **when** a caller runs
`tightbeam assign --subject "own release health" --session <holder> --lifecycle-kind standing`,
**then** the gateway receives `lifecycleKind = standing`, the stored assignment has
that type, and the command result includes `"lifecycleKind":"standing"`.

**When** the caller reads the assignment through each JSON surface named in AR5,
**then** each assignment object reports `"lifecycleKind":"standing"`. A Firehose
`assignment.opened` state event hydrates the same value.

**When** the REST schema conformance fixture serializes that assignment, **then** its
declared field order places `lifecycleKind` after `effectKind` and before
`derivedStatus`.

### AC2 — Compatible default and input refusal (G2; I6, I11; AR1, AR5)

**Given** the same holder, **when** a caller runs `assign` without
`--lifecycle-kind`, **then** the stored and projected lifecycle kind is `discrete`
and the creation transaction writes one supervision entitlement.

**When** the caller runs `dispatch` without `--lifecycle-kind`, **then** the stored
and projected lifecycle kind is `discrete` and the creation transaction writes one
supervision entitlement and one effort generation.

**Given** a legacy assignment without a stored lifecycle value, **when** a caller
reads it through a surface named in AR5, **then** the projection reports
`lifecycleKind = discrete`.

**When** a caller runs `tightbeam help`, **then** the `assign` and `dispatch` usage
lines name `--lifecycle-kind discrete|standing` and the help states that omission
selects `discrete`.

**When** a caller supplies `--lifecycle-kind perpetual`, **then** the command returns
`invalid_lifecycle_kind` and creates no assignment, monitor, wake, message, or
Firehose state event.

**When** a caller combines `--reviews <assignmentId>` with
`--lifecycle-kind standing`, **then** the command returns
`standing_review_conflict` and creates no assignment, monitor, wake, message, or
Firehose state event.

### AC3 — Deterministic no-prod regression (G3; I7, I8; AR2, AR3)

**Given** one standing assignment created by `dispatch` and one committed terminal
turn for its holder, **when** the test invokes the turn-end supervision evaluator
directly, **then** the evaluator returns `standing_only` and the assignment has zero
effort generations, zero supervision entitlements, zero supervision controller
wakes, zero `prod_fired` events, zero effort decision requests, and zero
completion-rail actions. The evaluator writes no supervision watermark.

The test uses direct evaluator calls and committed fixture rows. It does not sleep or
wait for a scheduler.

**Given** an older standing assignment and a newer discrete assignment for one
holder, **when** the same turn-end evaluator runs, **then** it selects the discrete
assignment, produces one tier-1 prod for that discrete assignment, and creates no
monitor row for the standing assignment.

### AC4 — Completion is impossible; custody has exits (G4; I2-I5; AR4)

**Given** an open standing assignment, **when** its holder files a completion attest,
**then** the gateway returns `standing_has_no_completion`, the assignment remains
open, and no completion attest or secondary state row exists.

**When** the schema test attempts to commit that standing assignment with
`outcome = completed`, **then** the database constraint refuses the transaction.

**When** its holder files a progress attest, **then** the gateway stores that attest
and creates no supervision entitlement or effort generation.

**When** an authorized caller files a verdict attest, **then** the gateway stores that
attest and creates no supervision entitlement or effort generation.

**When** its holder files surrender instead, **then** the assignment closes with
`outcome = surrendered` through the existing papertrail.

**Given** another open standing assignment, **when** an authorized principal revokes
it, **then** it closes with `outcome = revoked` through the existing papertrail.

**When** an authorized principal reopens either assignment, **then** its
`lifecycleKind` remains `standing` and no completion-oriented monitor row exists.
The corresponding Firehose `assignment.closed` and `assignment.reopened` state
events hydrate `lifecycleKind = standing`.

### AC5 — Typed work-item liveness (G1, G2; I9; AR2, AR5)

**Given** one open work item with a pending routing wake and a second open work item
with a pending slate wake, **when** a standing assignment takes custody of each item,
**then** the assignment transition cancels each bracket wake. **When** a caller reads
each cancellation receipt through `work-item-trace`, **then** it reports
`standing_accountability`, the exact assignment id,
`workImpactKind = linked_work_open`, `actionNeeded = true`,
`causalSourceKind = assignment_transition`, `causalSourceId = <assignmentId>`,
`requesterKind = process`, and `requesterId = tightbeam:work-items`.

**Given** a closed, discrete, foreign-work-item, or retired-holder assignment,
**when** a cancellation attempts to cite it as `standing_accountability`, **then** the
transaction refuses the trigger and writes no cancellation receipt.

## Open Questions

None. This MVP has no blocking or non-blocking holes.
