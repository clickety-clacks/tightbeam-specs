# Patrol failure classification and escalation v1

**Status:** Proposal for independent review
**Target:** Unset
**Work item:** `wi_6d418db1-26b4-4ad0-9886-86e757e93342`
**Scope authority:** `att_4c58ec95-6eae-4c0d-953f-8c7178bbecb9`,
`att_819bdf81-3c42-4cdd-9569-2c6ab70b1521`, and
`att_b947ee66-5703-4438-9f1c-4d5e2e1fe172`
**Product baseline:** `clickety-clacks/tightbeam` commit
`8e269e89c04b6b8569813142a12742f3325b8503`
**Specs baseline:** `clickety-clacks/tightbeam-specs` commit
`5f4b636d02aa8f1cd0670dd090d0af8c35894e88`

## Goal

Make patrol act on what happened instead of treating every failed prod turn as holder
silence.

This proposal closes two defects only:

1. A prod that the holder did not answer can advance the existing accountability
   ladder. A prod whose turn could not run cannot. Adjacent strikes use a durable,
   positive eligibility clock, and the default three-strike ladder cannot complete in
   the four-second incident window.
2. Six consecutive turns that ran and ended with a typed provider error, and are not
   already governed by a conserved wake-named Bubble cause, produce one durable patrol
   escalation through the existing Bubble lineage route. They do not end with no
   recipient. A `could_not_run` failure keeps the existing nearest-active-ancestor
   Bubble route after the existing wake retry and exhaustion contract reaches its
   routing boundary.

The substrate classifies and records. The recipient decides what to do (wisdom 6).

## Non-Goals

- Defect 1, including wake cancel/admit ordering, wake outcomes, retry, re-arm,
  exhaustion, undeliverable state, and wake-named cause conservation, remains entirely
  in `wi_113d569f-7aff-412b-aec3-0c21f2e87f40` and
  `wake-delivery-conservation.md`.
- Cancellation provenance remains in
  `wi_0abae0fd-80ec-48e2-bf61-96e611342f03` and
  `prodder-provenance-v1.md`.
- Defect 4 and supervision-dark recovery remain in
  `wi_a57dee58`.
- Transfer of unfinished work after staff loss remains in
  `wi_174a2b8b-482c-4d54-9f07-36cb55e6852b`.
- An out-of-band operator alert when the gateway cannot route or persist remains in
  `wi_f1013180-d73a-4eea-85b3-3ba4ff8c323d`.
- This proposal does not add a work-item dependency graph, recurrence-card verb,
  operator decision, new wake outcome, new retry delay, new prod-limit setting, model
  fallback, credential repair, provider repair, or provider circuit breaker.
- This proposal does not change existing successful-turn behavior, assignment
  ownership, release targeting, or delivery to a retired session.

## Terms

- **Patrol**: the existing serialized supervision production in
  `Tightbeam.Supervision`. It recognizes durable turn, wake, assignment, entitlement,
  and receipt rows and can issue prods or escalations.
- **Prod attempt**: an existing supervision wake intended for the assignment holder.
  An attempt is not an accountability strike until its terminal evidence proves the
  holder could run it and did not answer it.
- **Did not answer**: a prod attempt whose linked turn was admitted and handled, while
  the assignment acquired no qualifying liveness receipt in the attempt's frozen
  receipt epoch. A handled prompt alone is not a liveness receipt.
- **Could not run**: the closed typed `could_not_run` disposition supplied by
  `wake-delivery-conservation.md`. It proves that the inference run was not admitted.
  It is infrastructure evidence, not holder negligence.
- **Ran-and-failed provider error**: a terminal with typed run disposition
  `run_failed` and typed failure category `provider_error`. Both fields come from the
  run boundary. Error prose, marker text, numeric HTTP text, and exception inspection
  cannot establish this class.
- **D3-eligible provider error**: a ran-and-failed provider error whose terminal is not
  already represented by a wake-named Bubble cause under
  `wake-delivery-conservation.md`. A source terminal belongs to one downstream fault
  route, never both.
- **Accountability strike**: one durable `did_not_answer` classification charged to
  the current assignment receipt epoch. The configured `prod_limit` remains the number
  of strikes before the existing escalation ladder begins.
- **Strike clock**: the durable tuple `lastStrikeAt`, `nextStrikeAt`, and the positive
  per-assignment `supervisionIntervalMs`. The implementation can project the first two
  from existing supervision rows when that projection is unambiguous; it shall not keep
  a second independent clock.
- **Provider-failure streak**: one current sequence of consecutive D3-eligible provider
  errors for one session. The state records one failure domain; a domain change ends
  that sequence before it starts another. The threshold is the existing owner-ratified
  value of six. This proposal does not make it configurable.
- **Failure domain**: the stable, non-secret execution identity already carried by the
  typed terminal: session, harness, provider, host, and credential-slot identifier when
  present. A change to any present component starts a new streak.
- **Bubble route**: the existing route in `Tightbeam.Productions.Bubble`: walk to the
  nearest active operational ancestor; continue upward when a notice turn cannot run;
  and, when no active ancestor remains, commit the existing owner-terminal record and
  `user-alerted` fact. The route summons a mind; it does not decide for that mind.
- **Logical escalation**: one durable patrol threshold cause. Its notice can climb more
  than one ancestor, but those notice turns remain one escalation. It is not a wake
  outcome or a replacement for a wake-named cause.

## Assumptions

1. `wake-delivery-conservation.md` will supply final, typed wake outcomes and the
   `could_not_run`, `run_failed`, `run_canceled`, and `outcome_unknown` run
   dispositions. This proposal consumes those facts and does not define their
   production.
2. The current supervision entitlement stores a positive `supervisionIntervalMs` and
   durable `dueAt`. The current mutation seam can re-arm the entitlement without a new
   wake lifecycle.
3. The current liveness-receipt ledger defines the receipt epoch and reset sources.
   Patrol does not parse attest notes, prompts, messages, or work-item titles.
4. Bubble already has nearest-active-ancestor traversal, notice-turn continuation,
   deterministic notice identity, boot sweeping, and a durable no-recipient terminal
   path. D3 reuses that route for a patrol threshold cause without changing admission,
   identity, or settlement of an existing wake-named cause.
5. Terminal rows have a monotone sequence within one database. Patrol can process
   unclassified terminals in sequence order after restart.
6. The product baseline does not yet persist `run_failed` separately from its safe
   provider category. Implementation of this proposal therefore depends on the typed
   facts from `wi_113d569f`; it must not infer them from current `failureDetail` prose.

## Invariants

1. **Typed precedence.** `could_not_run` outranks every error category. A terminal
   cannot be both an accountability strike and a provider-failure streak member.
2. **No false negligence.** A `could_not_run`, `run_failed`, `run_canceled`, or
   `outcome_unknown` prod terminal cannot increment the accountability strike count.
3. **Heard before charged.** A prod attempt increments the strike count only after its
   handled terminal and frozen receipt epoch prove `did_not_answer`.
4. **One clock.** Each assignment has one durable strike clock. A restart, duplicate
   terminal notification, delayed sweep, or concurrent recognizer cannot bypass it.
5. **Four-second regression floor.** With the default `prod_limit=3`, the persisted
   eligibility times cannot make strike 3 eligible within 4,000 milliseconds of strike
   1. Adjacent strikes always have positive spacing.
6. **One streak member per terminal.** A terminal sequence can change a
   provider-failure streak at most once.
7. **Consecutive means consecutive.** A delivered turn, a different failure domain,
   `could_not_run`, `run_canceled`, `outcome_unknown`, a non-provider `run_failed`
   terminal, or a provider failure already governed by a wake-named Bubble cause ends
   the current provider-failure streak before later provider failures count.
8. **Threshold reuse.** Exactly six consecutive qualifying terminals admit the logical
   provider-failure escalation. The seventh and later failures in the same streak do
   not admit another one.
9. **One cause, one route.** The threshold transaction commits one logical Bubble cause
   and its route disposition. Replays reuse it. Notice-turn failures can continue the
   same cause upward; they cannot create a second cause.
10. **Wake conservation stays authoritative.** Every source wake keeps the outcome,
    retry, exhaustion, wake-cause identity, and Bubble admission required by
    `wake-delivery-conservation.md`. A terminal with that conserved cause is ineligible
    for the D3 streak and patrol threshold cause. D2 only classifies it for negligence.
11. **Cause and principal.** Every classification, reset, streak increment, threshold,
    route admission, and no-recipient result names the source turn or wake, the affected
    assignment or session, a closed cause kind, and principal `process:tightbeam`
    (wisdom 5).
12. **No silent absence.** A threshold with no runnable ancestor still commits the
    existing Bubble terminal record and standing owner fact. Failure of the gateway
    itself to persist that transaction is outside this proposal and remains
    `wi_f1013180`.
13. **Privacy.** Durable patrol state, lifecycle rows, projections, and notices contain
    only allowlisted identifiers, closed classes, counts, timestamps, and the existing
    safe public failure summary. They contain no prompt, response, raw exception,
    credential value, token, or provider response body.
14. **Targetless compatibility.** Existing rows remain readable. Missing new patrol
    state means zero strikes, no active provider streak, and no threshold escalation.
    No migration invents classifications for legacy prose-only failures.

## Architecture

### A. One patrol-classification seam

`Tightbeam.Supervision` shall own one in-transaction mutation seam for patrol
classification. Every turn-end callback and recovery sweep shall call that seam; no
other module shall write patrol strike or provider-streak state.

The seam shall read typed terminal and wake outcomes before it evaluates holder
accountability. It shall apply this precedence:

1. A retry-eligible `could_not_run` wake outcome records `could_not_run_pending`. It
   charges no strike and admits no new route. Existing retry and exhaustion continue.
2. A final `could_not_run` outcome records `could_not_run_final`, charges no strike,
   and leaves its conserved wake-named cause eligible for the existing nearest-active-
   ancestor Bubble route.
3. A terminal already represented by a wake-named Bubble cause records
   `wake_cause_conserved`, charges no strike, and makes no D3 state or route change.
4. A D3-eligible `run_failed` terminal with typed `provider_error` records one
   provider-streak observation, charges no strike, and follows section C.
5. Other `run_failed`, `run_canceled`, and `outcome_unknown` terminals charge no
   strike and end any provider streak for that failure domain. Their existing wake and
   Bubble dispositions remain unchanged.
6. A handled prod terminal with no qualifying receipt in its frozen epoch records
   `did_not_answer` and follows section B.
7. A qualifying receipt records progress and resets the current accountability epoch.

The check and its chosen state transition shall be one transaction. A lower-priority
branch cannot run after a higher-priority branch matches.

Acceptance: R-A is proven by checks 1, 2, 5, and 7 below.

### B. Accountability strikes and the durable clock

Patrol shall persist, per assignment receipt epoch, the strike count, the source wake
and turn for the last charged strike, `lastStrikeAt`, and `nextStrikeAt`. It shall use
the existing positive `supervisionIntervalMs` as the base interval and the existing
entitlement `dueAt` as the eligibility row. If existing rows can carry these values
without ambiguity, no new counter or clock table shall be added.

When `did_not_answer` wins classification, one transaction shall:

1. verify that this source attempt has not already been classified;
2. charge exactly one strike;
3. set `lastStrikeAt` to the source prod's committed admission time;
4. set `nextStrikeAt` no earlier than `lastStrikeAt + supervisionIntervalMs`;
5. for `prod_limit=3`, make strike 3 ineligible until strictly after
   `strike1At + 4_000`;
6. re-arm the existing entitlement at that `nextStrikeAt`; and
7. append one lifecycle row with the source, count, clock, cause
   `did_not_answer`, and principal.

A sweep before `nextStrikeAt` shall create no prod, escalation, counter change, or
replacement clock. A sweep at or after `nextStrikeAt` can use the existing prod-limit
ladder. A qualifying liveness receipt starts a new epoch with zero strikes and a fresh
clock through the existing receipt mutation seam.

Raw attempt counters can remain available for diagnostics, but neither ladder branch
selection nor user-facing negligence claims may use them as the strike count.

Acceptance: R-B is proven by checks 1, 2, 3, 6, and 7 below.

### C. Provider-failure streak and threshold admission

Patrol shall persist one current provider-failure streak per session. The state shall
contain at least the failure domain, streak generation, count, first and latest source
turn sequences, latest observed time, latest classified terminal sequence, threshold
state, logical escalation id, frozen owner user id, cause, and principal. This state can
share the patrol state surface from section B; it shall not create a second writer.

For each qualifying terminal in sequence order, the classification transaction shall:

- start a new generation at count 1 when no matching streak exists;
- increment an existing matching streak once;
- retain the first and latest qualifying terminal identities before count 6, without
  creating a patrol threshold cause or admitting a recipient notice;
- at count 6, atomically mark the streak `escalated`, create or verify one deterministic
  logical escalation, and admit that cause to the Bubble route; and
- after count 6, retain the `escalated` state and create no second escalation until a
  reset boundary occurs.

The deterministic escalation id shall derive from the failure-domain identity, streak
generation, and sixth terminal sequence. The patrol threshold cause shall cite the
first through sixth terminal sequences. It shall not name itself as a wake outcome,
replace a source cause, or acquire a wake id from `wake-delivery-conservation.md`.

The following event ends the streak before it is classified for any new streak: a
delivered turn, a failure-domain change, `could_not_run`, `run_canceled`,
`outcome_unknown`, non-provider `run_failed`, or a provider failure already governed by
a wake-named Bubble cause. The reset transaction shall record the prior generation,
count, boundary turn, cause, and principal. A threshold notice turn is route machinery
and does not reset the source session's streak.

Acceptance: R-C is proven by checks 4, 5, 6, and 7 below.

### D. Patrol-threshold routing and recipient absence

This proposal shall not amend admission or settlement of any existing Bubble cause.
Final `could_not_run` keeps the admission point required by the existing wake
exhaustion contract. Every other wake and non-wake Bubble cause keeps its current
admission behavior.

When a D3 streak reaches six, patrol shall admit its deterministic threshold cause to
the existing Bubble lineage route. That cause is a new patrol fact, not a delayed,
coalesced, or renamed source-turn Bubble cause.

At the provider threshold, Bubble shall resolve the nearest active operational ancestor
from the failing session. If that recipient's notice turn fails or is canceled, the
existing climb continues with the same logical escalation. If no active ancestor
remains, the existing terminal transaction records the owner alert and standing
`user-alerted` fact. If the composed owner Main stream is absent, the record and fact
still commit and the result is `record_only`; no session is created.

The patrol threshold cause shall freeze the owner user id when T6 is classified. If the
source session row is absent before routing, the route shall use that frozen owner for
the same terminal record-and-fact result; it shall not take Bubble's silent parentless
cause branch.

The route transaction shall store the selected recipient or the closed absence result.
It shall never leave the logical escalation in a state that only a later inference
decision can release. This is a routed fact, not a hold (T-RECOGNITION).

Acceptance: R-D is proven by checks 2, 4, and 7 below.

### E. Concurrency, restart, replay, and audit

Patrol shall serialize classification by session. Its state transition shall use the
source terminal sequence and current streak generation as a compare-and-set boundary.
Two callbacks for one terminal, a callback racing the recovery sweep, or two sweeps
shall commit at most one classification.

On boot, patrol shall scan terminal sequences after its durable classification
watermark in ascending order. It shall apply the same transition seam. A crash after
classification but before notice delivery shall leave the escalation eligible for the
existing Bubble sweeper. A crash after notice admission shall replay to the same
deterministic id.

The caller-visible supervision projection and linked work-item trace shall expose the
closed classification, strike count and clock, provider streak count and generation,
threshold state, logical escalation id, selected recipient or absence result, source
turn/wake ids, cause, and principal. Projection authorization shall reuse existing
supervision and work-item trace authorization.

Unknown run dispositions, unknown provider categories, incompatible legacy state, and
invalid clock values shall return typed errors and append a safe lifecycle row. They
shall not default to `did_not_answer`, increment a streak, route a notice, or partially
mutate state. Required codes are:

- `patrol_failure_class_unknown`;
- `patrol_failure_domain_invalid`;
- `patrol_strike_clock_invalid`; and
- `patrol_state_incompatible`.

Acceptance: R-E is proven by checks 1, 4, 5, 6, and 7 below.

### F. Smallest mechanism and compatibility

ADD wins the subtraction test because patrol and provider-failed turns are existing,
required surfaces; deleting either would remove accountability or execution, and
accepting false negligence plus a silent six-failure terminal would violate the Goal.
The addition is one typed classification/state seam. No adjudicator, retry engine,
second Bubble, or parallel clock is justified.

The strongest affordable rail is a closed type plus one mutation seam, backed by unique
source identities and database checks (wisdom 3 and 26). Guidance alone is insufficient.

Migration shall be additive or exact-shape guarded. It shall not rewrite legacy turn
classification from prose, advance a legacy strike count, synthesize a provider streak,
or emit a threshold escalation during migration. Rollback shall refuse while new patrol
state cannot be represented by the predecessor; it shall never silently discard an
open streak or threshold record.

Acceptance: R-F is proven by checks 6 and 7 below.

## Acceptance

### 1. Class distinction and precedence

Given one supervised assignment at strike count 0, one prod attempt ending with final
typed `could_not_run`, and one otherwise identical prod attempt ending handled with no
receipt, when patrol classifies each in separate fixtures, then the first records
`could_not_run_final`, keeps strike count 0, and cannot select negligence; the second
records `did_not_answer`, sets strike count 1, and persists its clock. If the first also
carries a safe provider category, `could_not_run` still wins.

### 2. Could-not-run keeps its existing route

Given a `could_not_run` wake with a retry still eligible, when patrol classifies it,
then no strike or Bubble notice is added. Given the same wake after the existing retry
contract commits final `undeliverable`, when Bubble recognizes it, then exactly one
wake-named logical cause routes to the nearest active ancestor. No patrol retry,
wake re-arm, cancellation, wake outcome, or replacement cause is created. The existing
supervision entitlement clock remains governed by section B.

### 3. The four-second ladder does not recur

Given `prod_limit=3`, a positive stored `supervisionIntervalMs`, and the incident replay
clock starting strike 1 at time 1,000, when handled no-receipt prod terminals and sweeps
are replayed through time 5,000 inclusive, then strike 3 is not eligible at or before
time 5,000. Every committed strike has `nextStrikeAt > lastStrikeAt`, and every sweep
before the stored `nextStrikeAt` creates no strike or escalation. Advancing to the exact
later eligibility times admits each remaining strike once.

### 4. Six provider failures produce one escalation

Given child session C, nearest active ancestor P, one failure domain D, and six
consecutive typed `run_failed` plus `provider_error` terminals T1 through T6, when
patrol classifies them in order, then counts 1 through 5 persist source-terminal bounds
with no patrol threshold cause or recipient notice. Classification of T6 atomically
records count 6, one deterministic logical escalation, cause/principal, and route
admission to P. Replaying T1 through T6 and adding T7 creates no second logical
escalation or first-recipient notice. None of T1 through T7 has a wake-named Bubble
cause.

### 5. Reset boundaries do not blend incidents

For each reset boundary—delivered turn, failure-domain change, `could_not_run`,
`run_canceled`, `outcome_unknown`, non-provider `run_failed`, and a provider failure
with a conserved wake-named Bubble cause—given five qualifying provider failures, the
boundary, and five more qualifying provider failures, when patrol classifies the
sequence, then two streak generations each end at count 5 and no threshold escalation
exists. The conserved wake cause keeps its own route unchanged. Given a qualifying
receipt after two accountability strikes, the next handled no-receipt prod is strike 1
of a new receipt epoch.

### 6. Concurrency, restart, and typed refusal

Given a database snapshot at provider count 5, when two recognizers classify T6
concurrently, then one count-6 transition and one logical escalation commit. Kill the
gateway after that commit and before notice delivery; after restart and two sweeps, the
same escalation id has one first-recipient notice. Repeating the test with an unknown
run disposition, invalid failure domain, nonpositive clock, and incompatible patrol
state returns the matching typed code, writes one safe lifecycle row, and changes no
strike, streak, route, or wake row.

### 7. Privacy, audit, compatibility, and boundary census

Given fixtures containing secret-looking prompt text, provider response bodies, raw
exceptions, credential values, and tokens, when D2 and D3 paths run and their lifecycle,
supervision, work-item trace, notice, and log surfaces are exported, then none of those
secret values appears. Each state change instead exposes its closed class, allowlisted
failure-domain ids, counts, clocks, source ids, cause, and principal.

Start from a predecessor database containing turns, wakes, prod counters, and no patrol
classification state. After migration and two boot sweeps, legacy rows are unchanged,
new state is empty, and no escalation exists. The implementation diff and source census
show no changes to wake cancel/admit ordering, wake outcome enums, retry delays,
undeliverable settlement, re-arm policy, assignment staff transfer, substrate-down
alerts, identity, credentials, or release targeting.

## Open Questions

None. The owner fixed the scope, the three-strike incident bound, the six-failure
threshold, the Bubble route, and all adjacent ownership boundaries. Implementation
details that preserve this contract remain with the builder.
