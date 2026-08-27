# Standing accountability lifecycle

Status: canonical amended MVP spec for
`wi_0552815b-e5b5-4c56-90ed-c40825c3b9ad`; pending exact-tip re-review.

This spec is the authoritative bounded amendment for these clauses:

| Existing authority | Clause amended by this spec |
|---|---|
| `accountability-constitution-v1.md` | Section 1 guarantee 3: a standing assignment satisfies Patrol through AR3's standing-accountability production, not a completion prod. |
| `supervision-v1.md` | The invariant, stall predicate, prod lifecycle items 1-3, and the “no standing reminders” paragraph: AR3 supplies the standing lifecycle's distinct receipt, prompt, and due production. |
| `supervision-impl-v1.md` | The `:prod_ladder` turn-end slot, Goals 1-3, the periodic-sweep non-goal, Self-driving liveness, and the no-terminal due-entitlement deferral: AR3 adds no sweep and specializes the existing per-assignment entitlement by stored lifecycle kind. |
| `effort-checkin-v2.md` | Design item 1 and Acceptance items 1-3: `dispatch` arms effort check-in only for a discrete assignment. |
| `work-item-brackets-v1.md` | Bracket 1 and Bracket 2 assignment-cancellation clauses: a standing assignment is custody, and its cancellation receipt uses T4. |
| `attest-v1.md` | The closed kind vocabulary, non-terminal filing behavior, response shape, CLI usage, and tests: T6 adds holder-filed `reaffirmation`. |
| `rest-state-api-v1-wire-schema.md` and `cli-surface-v1.md` | The assignment field set and the `assign`, `dispatch`, and `attest` families gain the fields and values in AR5. |
| `event-firehose-v1.md` | V3's shared public projection and R1's assignment and attest state classes carry AR5's additive lifecycle and reaffirmation values. |

Those documents remain authoritative outside the named clauses. This table resolves a
conflict in favor of this spec; it does not authorize another behavior change.

## Goal

G1. Tightbeam represents ongoing accountable custody as a typed standing assignment
that has no completion target or deadline.

G2. Tightbeam distinguishes a standing assignment from a discrete assignment in
stored state, gateway responses, REST state, Firehose state, and CLI input and output.

G3. Tightbeam excludes a standing assignment from the two mechanisms that ask whether
an assignment produced effect or moved toward completion: the discrete supervision
prod branch and the effort-without-effect check-in.

G4. Tightbeam supervises a standing assignment through an assignment-scoped
reaffirmation receipt and a standing-accountability prod that asks no completion
question.

G5. Tightbeam keeps a standing assignment open until its holder surrenders it or an
authorized principal revokes it.

## Non-Goals

NG1. This MVP does not add a completion target, completion deadline, scheduler, or
escalation ladder. Standing accountability reuses the existing supervision entitlement
interval, wake delivery, counter, and escalation ladder.

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

1. the discrete-assignment branch of a `supervision_entitlements` generation that can
   reach a completion prod or escalation; or
2. an `effort_checkin_generations` generation that can reach an effort check-in.

A standing-accountability production uses a `supervision_entitlements` row, but it is
not completion-oriented because its prompt and receipts do not ask whether work moved
toward completion.

### T6 — Standing reaffirmation

A standing reaffirmation is an `attests` row with `kind = reaffirmation`. Only the
current holder of an open standing assignment can file it. It states that the holder
retains accountable custody; it claims no progress, effect, verdict, or completion.

The gateway wire value and CLI value are `reaffirmation`.

### T7 — Standing-accountability production

A standing-accountability production is the lifecycle-specific branch of the existing
supervision entitlement and prod ladder. Its production kind is
`standing_accountability`. Its horizon is the entitlement's stored
`supervisionIntervalMs`; that horizon is an accountability cadence, not a completion
deadline.

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

A3. Existing assignment, attest, wake-cancellation, supervision, REST, Firehose, and
CLI projections remain available to carry the lifecycle field, reaffirmation kind,
and standing-accountability production and trigger values.

A4. Holder retirement already disposes each open assignment through the recorded
revocation path. This feature relies on that existing exit.

A5. Product-owner evidence `att_6c6b3c37-56b0-40ef-be55-00abc95d27f8`
requires standing liveness to use periodic reaffirmation instead of completion.
Evidence `att_50f7e16b-dfaf-4e3a-b142-abbb8c7dc0b5` requires the primitive to be
assignment-scoped and holder-usable. This spec treats those rulings as the F1 product
decision requested by review `att_73566dd9-48e4-443e-a9c9-cc3e9094b8bd`.

A6. The existing supervision entitlement stores a positive
`supervisionIntervalMs`, a due time, cause, and principal. The existing prod ladder
provides durable wake delivery, counters, and escalation. AR3 specializes those seams
by immutable lifecycle kind.

A7. At the A2 baseline, a due entitlement whose holder has no terminal row re-arms with
`basisKind = no_terminal` and produces no prod. AR3 retains that rule for a discrete
assignment and excludes a standing assignment from it.

## Invariants

I1. Each assignment has exactly one lifecycle kind. A new assignment stores the kind
in the same transaction that stores the assignment. A legacy assignment reads as
`discrete`.

I2. The lifecycle kind does not change after assignment creation. Reopening an
assignment preserves its original kind.

I3. A standing assignment has no completion target, completion deadline, completion
attest, or `completed` outcome.

I4. A standing assignment accepts progress, reaffirmation, and verdict attests under
AR3 and their existing authority rules. The presence or absence of those attest kinds
does not arm a completion-oriented monitor.

I5. A standing assignment can close only through the existing surrender or revocation
seam. Each close retains its existing principal, cause, and papertrail.

I6. A review assignment is discrete. The gateway refuses a request that combines
`reviewsAssignmentId` with `lifecycleKind = standing`.

I7. A standing assignment creates one lifecycle-specialized row in
`supervision_entitlements` and no row in `effort_checkin_generations`. Reopening it
re-arms the standing supervision entitlement and creates no effort generation.

I8. A holder-filed progress or reaffirmation attest against an open standing
assignment is a valid standing-accountability receipt. A holder-created pending
continuation wake accepted by the existing liveness-receipt seam is also valid. A
verdict, artifact, message, turn, or work-item update is not a standing-accountability
receipt.

I9. The completion-prod production selects the oldest eligible open discrete
assignment for the holder. An older standing assignment does not hide a newer
discrete assignment.

I10. A due standing assignment with no valid receipt, pending continuation, queued or
running turn, current blocking fact, or terminal disposition produces one
standing-accountability prod. A holder with zero terminal-turn history remains eligible.
The prod's empty answer advances the existing counter and escalation ladder. Its prompt
offers reaffirmation, continuation, or surrender and does not offer completion.

I11. A wake-cancellation receipt can use `standing_accountability` only when its id
names an open standing assignment whose holder is active and the receipt's primary
work is that assignment or its linked work item. The receipt retains the existing
cause and requester principal fields.

I12. Each canonical assignment projection exposes `lifecycleKind`. A consumer never
infers it from `effectKind`, subject text, attests, age, or monitor rows.

I13. Omission preserves existing behavior. An `assign` or `dispatch` request without
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

### AR2 — Targetless standing accountability

Assignment creation and reopening branch on the stored lifecycle kind in the same
transaction as the lifecycle action. The discrete branch keeps the existing
supervision and effort behavior. The standing branch creates or re-arms one
supervision entitlement specialized by the stored standing kind. It uses T4 as the
work-item liveness trigger and creates no effort generation.

Work-item bracket cancellation accepts `standing_accountability` as a liveness
trigger. Its validator reads the assignment type, open state, current holder state,
and work-item relation from durable rows. The validator refuses a stale or mismatched
trigger.

### AR3 — Monitor admission

The effort check-in arm, rearm, and transfer queries admit discrete assignments only.
The supervision turn-end candidate query admits discrete assignments only and orders
those candidates by `(openedAt, id)` as it does now.

The standing-accountability candidate query admits open standing assignments only. It
orders eligible candidates by `(dueAt, openedAt, id)`. A standing candidate becomes
due when its stored entitlement `dueAt` is at or before the evaluator time and the
existing pending-turn, pending-wake, blocking-fact, holder-active, and
terminal-disposition guards admit it. The standing branch does not apply the discrete
evaluator's `no_terminal` deferral. The turn-end, scheduled, and recovery entry points
run this query through the existing supervision evaluator; a new terminal is not
required. The evaluator returns `standing_not_due` without a claim when a holder has
standing custody but no due candidate.

When the holder has no terminal row, the standing evaluator claims the entitlement's
current armed generation at its stored `dueAt`. It does not increment or re-arm that
generation before the claim. The claim records `lastAttemptGeneration` as that current
generation, passes `terminalSeq = null` to the existing nullable watermark seam, writes
`cause = standing_due` and `principal = process:tightbeam`, and retains the entitlement's
existing `basisKind` and `basisId`. It writes no `no_terminal` re-arm or
`supervision_entitlement_rearmed` event.

The discrete production has priority when a turn-end evaluation finds both a discrete
candidate and a due standing candidate. Otherwise, the evaluator claims one due
standing candidate with production kind `standing_accountability` and sends this
prompt through the existing supervision wake seam:

```text
Standing assignment <assignmentId> needs accountability reaffirmation. File reaffirmation, schedule a continuation, or file surrender. This is accountability prod <k> of <N>; a reply without a row escalates to your spawner.
```

The `attest` transaction accepts `kind = reaffirmation` only when the caller is the
current holder and the assignment is open and standing. It stores the non-terminal
attest, resets the standing assignment's existing prod counter, and re-arms its
entitlement at `attest.ts + supervisionIntervalMs` in one transaction. A holder-filed
progress attest performs the same standing-accountability reset after it stores the
progress row. An accepted holder-created continuation uses the existing pending-wake
gate. Empty prod answers advance the existing counter and escalation ladder.

The reaffirmation re-arm records `basisKind = standing_reaffirmation`,
`basisId = <attestId>`, `cause = standing_reaffirmation`, and
`principal = session:<holderKey>` on the entitlement transition and its lifecycle
event. The standing-progress re-arm records `basisKind = progress`, the progress attest
id, `cause = progress`, and the same holder principal. The schema widens the closed
entitlement basis vocabulary by `standing_reaffirmation` and the closed cause vocabulary
by `standing_reaffirmation` and `standing_due`.

The gateway returns `reaffirmation_requires_standing` when the holder files
reaffirmation against a discrete assignment with this message:

```text
assignment <assignmentId> is discrete; reaffirmation is only valid for standing assignments; file progress, completion, or surrender
```

The refusal writes no attest, assignment transition, entitlement transition, wake,
counter, or Firehose state event.

This design adds no periodic sweep. It reuses the existing per-assignment entitlement
due time, evaluator, wake delivery, counter, and escalation machinery. Each standing
claim, receipt absorption, re-arm, prod, and escalation retains its existing cause and
principal fields.

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
camel-case `lifecycleKind` gateway parameter and performs no local inference. The
`attest` CLI and gateway accept `reaffirmation` as an additional non-terminal,
non-verdict kind and expose that exact value in the returned attest object.

The gateway's `assign`, `dispatch`, `assignment-get`, `assignments`,
`work-item-get`, and `work-item-trace` assignment objects include non-null
`lifecycleKind`. The CLI exposes the applicable results from `assign`, `dispatch`,
`assignments`, `work-item-get`, and `work-item-trace` without removing that field.
REST assignment resources and Firehose assignment state resources include the same
field and enum. In the canonical REST assignment field order, `lifecycleKind`
follows `effectKind` and precedes `derivedStatus`. Wake-cancellation trace objects may
expose `livenessTriggerKind = standing_accountability` and
`livenessTriggerId = <assignmentId>`.

Gateway, CLI, REST, and Firehose attest projections expose `kind = reaffirmation` as
they expose another non-terminal attest kind. No projection labels reaffirmation as
progress, completion, or verdict.

Existing creation callers remain input-compatible because omitted input defaults to
`discrete`. The new output member is additive.

### AR6 — Subtraction ruling and operating pattern

ADD wins because deleting assignment custody would leave standing intent unowned,
while accepting completion prods would make supervision report a known falsehood.
The standing-accountability branch preserves constitutional patrol without a
completion claim. The design adds no scheduler or parallel work object.

T4 uses the open assignment row as the work-item liveness trigger. The standing
supervision entitlement remains a patrol controller, not the proof that linked work is
owned.

Operating pattern: the CLI help is the instruction surface for selecting this type.
This MVP requires no operating-manual or Kung Fu amendment.

## Acceptance

### AC1 — Explicit standing creation and projection (G1, G2; I1, I12; AR1, AR5)

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

### AC2 — Compatible default and input refusal (G2; I6, I13; AR1, AR5)

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

### AC3 — Deterministic monitor separation and standing patrol (G3, G4; I7-I10; AR2, AR3)

**Given** one standing assignment created by `dispatch`, **when** the creation
transaction commits, **then** the assignment has one armed supervision entitlement,
zero effort generations, and zero effort decision requests. Its entitlement stores
the assignment's positive `supervisionIntervalMs` and a due time equal to
`openedAt + supervisionIntervalMs`.

**Given** that entitlement is not due, **when** the test invokes the supervision
evaluator directly, **then** the evaluator returns `standing_not_due` and writes no
claim, prod, escalation, completion-rail action, decision request, or watermark.

**Given** committed fixture rows make that entitlement due and leave its active holder
without a pending wake, queued or running turn, current blocking fact, or receipt,
**when** the test invokes the evaluator directly, **then** it returns
`standing_accountability`, writes one tier-1 prod whose production kind is
`standing_accountability`, and uses the exact AR3 prompt. The transaction writes no
effort generation, effort decision request, or completion-rail action.

**Given** equivalent due fixture rows whose active holder has zero rows in `turns`,
**when** the test invokes the scheduled and recovery entry points separately at the same
fixture clock, **then** each path claims the current armed entitlement generation and
produces the same tier-1 standing-accountability result on its isolated database. Each
claim leaves `supervision_watermarks.lastEvaluatedTerminal = null` and stores
`cause = standing_due`, the exact generation, and the principal from AR3. It leaves no
`no_terminal` re-arm or re-arm event. The test invokes the entry points directly and
does not sleep.

**When** the holder files `tightbeam attest <assignmentId> --kind reaffirmation`,
**then** the gateway stores one non-terminal reaffirmation attest, leaves the assignment
open, resets its standing prod counter, and re-arms its entitlement at
`attest.ts + supervisionIntervalMs`. The matching gateway, CLI, REST, and Firehose
attest projections report `kind = reaffirmation`. The entitlement and lifecycle event
report the exact reaffirmation basis, cause, id, and principal from AR3.

**When** the same holder instead files progress, **then** the gateway stores progress
and performs the same counter reset and entitlement re-arm. **When** a non-holder
tries reaffirmation, **then** the gateway returns `not_holder`. **When** the holder of
a discrete assignment tries it, **then** the gateway returns
`reaffirmation_requires_standing`. **When** the holder tries after close, **then** the
gateway returns `assignment_closed`. Each refusal writes no attest, assignment
transition, entitlement transition, wake, counter, or Firehose state event.

**Given** a due standing assignment with prod limit 2, **when** two delivered
standing-accountability prod turns end without a progress attest, reaffirmation attest,
pending continuation, blocking fact, or terminal disposition, **then** direct evaluator
calls produce tier 1, tier 2, and one escalation to the existing spawner rung. Each
claim uses committed fixture rows; the test does not sleep or wait for a scheduler.

**Given** an older due standing assignment and a newer eligible discrete assignment
for one holder, **when** the turn-end evaluator runs, **then** it selects the discrete
assignment and produces one tier-1 discrete prod. It writes no standing claim in that
evaluation and creates no effort generation for the standing assignment.

### AC4 — Completion is impossible; custody has exits (G5; I2-I5; AR4)

**Given** an open standing assignment, **when** its holder files a completion attest,
**then** the gateway returns `standing_has_no_completion` with the exact AR4 message,
the assignment remains open, and no completion attest or secondary state row exists.

**When** the schema test attempts to commit that standing assignment with
`outcome = completed`, **then** the database constraint refuses the transaction.

**When** its holder files a progress attest, **then** the gateway stores that attest
and re-arms the existing standing supervision entitlement under AC3. It creates no
second supervision entitlement or effort generation.

**When** an authorized caller files a verdict attest, **then** the gateway stores that
attest and leaves the standing supervision entitlement unchanged. It creates no second
supervision entitlement or effort generation.

**When** its holder files surrender instead, **then** the assignment closes with
`outcome = surrendered` through the existing papertrail.

**Given** another open standing assignment, **when** an authorized principal revokes
it, **then** it closes with `outcome = revoked` through the existing papertrail.

**When** an authorized principal reopens either assignment, **then** its
`lifecycleKind` remains `standing` and no completion-oriented monitor row exists.
The corresponding Firehose `assignment.closed` and `assignment.reopened` state
events hydrate `lifecycleKind = standing`.

### AC5 — Typed work-item liveness (G1, G2; I11; AR2, AR5)

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

### AC6 — Canonical authority closure (G3, G4; AR2, AR3, AR5)

**Given** the canonical spec set named in the opening authority table, **when** the
implementation change updates its touched authority text, **then** each named clause
points to this spec for the standing lifecycle and retains its prior rule for the
discrete lifecycle. A repository search reports no live clause that requires a standing
assignment to arm effort check-in, receive a completion prod, or remain without
standing-accountability patrol.

## Open Questions

None. This MVP has no blocking or non-blocking holes.
