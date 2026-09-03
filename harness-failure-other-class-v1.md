# Harness failure `other` class v1

Status: REVIEW CANDIDATE. Product work is forbidden until one different-session
reviewer accepts this file's exact SHA-256.

Authority: Mike's 2026-09-03 ruling on work item
`wi_089b8d3b-ed0f-4d09-8f6e-b238e3ed7af7`, assignment
`asg_7e6ac548-74ba-40ee-bc14-47eed7976f09`, and posture verdict
`att_959b6393-4985-44ef-8cf9-9b7f421194ac`. The earlier repair ruling is closed
work item `wi_6c74884c-3c8a-40ca-a168-d4651e876e8e`; its reviewed main landing is
`31c91a7a79bf411791d8422bb220495a72dd8d0c`.

Source baselines read for this revision:

- Tightbeam specs `main` at `c898bd4e91b7d8b6f92f2ef421d7845e6868f2be`.
- Tightbeam product `main` at `3e1dc56e1bd27854487228c05f4b2e1c9dd4fb22`.
- Tightbeam product `0.1.9` at `c3299e3a75dab21ed2839822d8ad207514f92782`.
- `production-machine-v1.md`, `stall-watchdog-kit.md`,
  `harness-kill-lifecycle.md`, and the served `product-owner.md` WORLD FACT
  guidance current on 2026-09-03.

## Goal

Add one evidence-bearing `other` harness-health class on `0.1.9` and `main`.
An authorized mind uses it only when none of the six named classes describes an
observed harness failure. Admission requires a description, the observed
state, exact probe, one exact observed error or probe-output digest, a recovery
condition, a reason that no named class applies, and a time-bounded WORLD FACT.
Incomplete input is refused before any row changes.

Each admitted `other` incident immediately pauses every prod-shaped action for
the affected `(harness, host)`. It creates a durable review obligation and
routes one evidence notice to the nearest living authority. The pause ends on
evidenced recovery or no later than the incident's bounded `expiresAt`; expiry
does not erase the incident, its evidence, its principal, or its pending review.

All prod-shaped consumers call one shared harness-availability gate. This
includes the current assignment prodder and the session garbage collector ruled
on work item `wi_86165cfa-94a6-471c-b533-0055485fbed6`. A consumer cannot carry
its own harness-health query.

Every `other` incident remains reviewable. The second incident with the same
description digest deterministically opens one promotion case. A promotion case
can close only when a reviewed canonical contract gives the recurring cause a
named class. The substrate records the recurrence and routes it; it does not
interpret the description or mint the class.

## Non-Goals

1. This spec does not change the six named classes: `auth-dead`,
   `rate-limit-dead`, `adapter_unavailable`, `model_unavailable`, `task_crash`,
   and `interrupted-outcome-unknown`.
2. This spec does not change a named class's classifier, evidence threshold,
   recovery proof, park behavior, repair action, or repair-not-revoke routing.
3. This spec does not classify an unmatched terminal failure as `other`
   automatically. The description, recovery condition, and not-known-class
   reason require judgment by an authorized mind.
4. This spec does not infer recovery by interpreting the recovery-condition
   text. An authorized principal supplies a new proof or expiry ends the pause.
5. This spec does not automatically add an enum value, edit guidance, create a
   release, or close a promotion case from a recurrence count.
6. This spec does not add a second prodder, session-garbage-collector timer,
   incident sweeper, harness liveness probe, or harness-up cache.
7. This spec does not change prompt admission, turn claiming, assignment state,
   session state, work-item state, or revocation authority.
8. This spec does not change `0.1.8`.
9. This spec does not backfill `other` incidents from old unclassified failures.
10. This spec does not expose raw error, probe, description, recovery, or
    not-known-class text in metrics, list projections, notices, or logs.

## Terms

- **Named class**: one of the six values in Non-Goal 1.
- **Other evidence**: the immutable WORLD FACT payload defined by ARC-02.
- **Source session**: the session whose `(harness, host)` the evidence concerns.
- **Description digest**: lowercase hexadecimal SHA-256 of the exact UTF-8 bytes
  of `trim(description)`. Case and internal whitespace remain significant.
- **Evidence mode**: `exact_error` or `probe_digest`.
- **Active other incident**: an incident with `failureClass='other'`,
  `state='open'`, and `now < expiresAt`.
- **Expiry instant**: the first millisecond for which `now >= expiresAt`.
- **Shared harness gate**: the one transaction-owned function that decides
  whether a prod-shaped action may target an `(harness, host)`.
- **Prod-shaped action**: any periodic or terminal-edge action that spends a
  prompt or turn to chase, inspect, or dispose of idle work. The assignment
  prodder and session garbage collector are members of this set.
- **Living authority**: the first active ancestor of the source session under
  the line's existing lineage seam; if no active ancestor exists, the source
  session owner's active Main session; if no active Main carrier exists, the
  owner user through the existing tokenless alert surface.
- **Other review**: the durable obligation for a living authority to confirm the
  incident as a one-off `other`, reclassify it to a named class, or bind it to a
  promotion case.
- **Recurrence**: a second or later admitted `other` incident, including an
  incident on a different harness or host, with the same description digest.
- **Promotion case**: one durable open record keyed by description digest that
  names the first two incident ids and requires a reviewed named-class contract.
- **Terminal incident state**: `resolved` or `expired`. Neither state deletes
  evidence or closes a pending review.

## Assumptions

1. Both lines own harness-health observations, incidents, condition facts,
   notices, and terminal turn writes in SQLite transactions.
2. `main` provides `Org.effective_parent_in_txn/2`. `0.1.9` walks the stored
   `sessions.spawnedBy` chain. Both lines cap an ancestry walk at 32 hops.
3. A stored notice turn's terminal state is the proof that a session could or
   could not receive the escalation. `delivered` proves a living authority;
   `failed`, `failed_unknown`, and `canceled` do not.
4. The four-class `0.1.9` port on assignment
   `asg_8187716c-2e0a-4b6a-be73-e68fa73c429e` precedes the `0.1.9` product
   implementation of this contract. The implementation must bind its migration
   to that port's exact reviewed and landed schema stamp. It must refuse any
   other predecessor.
5. Product `main` baseline `3e1dc56e...` contains the reviewed repair series at
   `31c91a7a...` and already recognizes the four added named classes.
6. The system clock supplies integer UTC epoch milliseconds. SQLite transaction
   serialization supplies the write order for recovery and expiry races.
7. Existing owner, admin, lineage, notice, event, and redaction rules remain
   authoritative unless this contract narrows them.

## Invariants

1. **OTH-INV-01 — Complete evidence or no effect.** The first `other` admission
   for an active incident identity commits all required evidence, one incident,
   one review, one initial escalation route, one standing harness fact, and one
   expiry identity atomically. A later admission for that active identity adds
   its immutable observation and event and reuses those rows. A refusal commits
   none of them.
2. **OTH-INV-02 — No guessed class.** Only an admitted explicit `other` mutation
   can create an `other` observation. An unmatched terminal error remains
   unclassified and does not open an incident.
3. **OTH-INV-03 — One bounded pause.** `expiresAt` is greater than acceptance
   time and no greater than `observedAt + 900000` milliseconds. The shared gate
   cannot deny because of that incident at or after `expiresAt`.
4. **OTH-INV-04 — All prod-shaped work shares one gate.** Every prod-shaped
   consumer calls the same exported transaction-owned gate immediately before
   it records or dispatches its action. No consumer reads incident rows,
   condition facts, adapter state, process state, or harness state separately.
5. **OTH-INV-05 — Healthy harnesses continue.** An active incident for one
   `(harness, host)` does not pause a different harness or host.
6. **OTH-INV-06 — Evidence and actor survive.** Admission, recovery, expiry,
   review, route, and promotion records retain their typed principal, cause,
   source row, and time. Updates and deletes cannot erase them.
7. **OTH-INV-07 — Delivery is not review.** A delivered escalation changes the
   review custodian. It does not close the review or incident.
8. **OTH-INV-08 — Expiry is not recovery.** Expiry retracts the pause and records
   `expired`. It does not claim that the harness recovered and does not close the
   review or promotion case.
9. **OTH-INV-09 — Recurrence promotes deterministically.** The second admitted
   incident with one description digest creates exactly one promotion case.
   Every later recurrence attaches to that case. No free-text similarity,
   time window, harness identity, or reviewer opinion changes this threshold.
10. **OTH-INV-10 — Judgment stays above the substrate.** The substrate validates
    fields, hashes exact bytes, counts exact digest equality, expires a deadline,
    and routes rows. It does not interpret error text, the not-known reason,
    recovery text, or promotion meaning.
11. **OTH-INV-11 — Authorization does not widen.** The source owner, an active
    same-owner source ancestor, or an admin may open `other`. The current review
    custodian, source owner, or admin may review or resolve it. The process
    principal may only expire, route, dedupe, and recover committed mechanics.
12. **OTH-INV-12 — Privacy follows the source owner.** Only the source owner, an
    authorized active same-owner ancestor, an admin, and the current review
    custodian may read sensitive evidence. All other surfaces return identifiers,
    class, state, times, and digests only.
13. **OTH-INV-13 — Known repairs remain repairs.** Reclassification to a named
    class invokes only that class's existing repair path. No `other` event,
    review, expiry, or promotion record authorizes revocation.
14. **OTH-INV-14 — Restart preserves the decision.** Restart reconstructs the
    pause, expiry, current route, review custody, and promotion state from rows.
    It does not create new evidence, extend `expiresAt`, or repeat a delivered
    notice.
15. **OTH-INV-15 — The quiet path is silent.** When the gate finds no active
    incident, it writes no row, sends no notice, asks no question, and returns
    `available`.

## Architecture

### ARC-01 — Explicit admission surface

Both lines expose one authenticated mutation named
`harness-health-observe-other`. Its input is:

```text
sourceSessionKey, description, evidenceMode,
observedState, exactProbe, exactObservedError?, outputDigest?,
recoveryCondition, notKnownClassReason,
observedAt, validUntil, worldStatus,
redactionConfirmed, idempotencyKey
```

`description`, `observedState`, `recoveryCondition`, and
`notKnownClassReason` are trimmed, non-empty UTF-8 strings of at most 2,000
bytes. `exactProbe` is a trimmed non-empty UTF-8 string of at most 4,000 bytes.
`worldStatus` is exactly `PROVEN` or `UNKNOWN`. `observedAt` and `validUntil`
are UTC epoch milliseconds.
`observedAt` must not be later than the transaction's acceptance time.
`validUntil` must be greater than the acceptance time and no greater than
`observedAt + 900000`.

For `exact_error`, `exactObservedError` is a trimmed non-empty UTF-8 string of
at most 8,000 bytes and `outputDigest` is null. For `probe_digest`,
`outputDigest` is exactly 64 lowercase hexadecimal SHA-256 characters and
`exactObservedError` is null. `UNKNOWN` requires `exact_error`; the exact probe
names the failed read and the error records its refusal. `redactionConfirmed`
must be true. It states that the caller used the digest mode when exact output could
contain a credential or secret, and that description, recovery, and
not-known-class text contain no secret.

The mutation refuses `missing_other_evidence`, `invalid_other_evidence`,
`stale_other_evidence`, `secret_redaction_unconfirmed`, `source_not_found`,
`source_not_active`, `not_authorized`, or `idempotency_conflict` before any
incident effect. The response names every missing or invalid field. It never
echoes sensitive field values.

An active source session may report itself. An active session may report a
source session only when it has the same owner and is an ancestor under the
line's existing lineage seam. The source owner user and an admin may report it.
`process:tightbeam` cannot supply this judgment-bearing mutation.

### ARC-02 — WORLD FACT and incident schema

Extend `harness_health_observations` with nullable columns:

```text
description, descriptionDigest, observedState, evidenceMode, exactObservedError,
exactProbe, outputDigest, recoveryCondition, notKnownClassReason,
validUntil, worldStatus, redactionConfirmed
```

Existing six-class observations require all twelve columns to be null. An
`other` opening observation requires the ARC-01 combinations. The stored
`cause` is `other:<descriptionDigest>`; the existing `principal` stores the
authenticated typed principal. The exact evidence fields, cause, principal,
and correlation identity are immutable.

Extend `harness_health_incidents.failureClass` to admit `other`. Add nullable
`descriptionDigest`, `expiresAt`, `expiredAt`, and `expiryFactId`. Six-class
incidents require these columns to be null and preserve their current
`open|resolved` transitions. An `other` incident requires
`descriptionDigest` and `expiresAt=validUntil`. It permits exactly:

- `open`: `resolvedAt`, resolution fields, `expiredAt`, and `expiryFactId` null;
- `resolved`: the existing resolution fields non-null and expiry fields null;
- `expired`: `expiredAt >= openedAt`, `expiryFactId` non-null, and resolution
  fields null.

Known classes retain the existing partial uniqueness on
`(harness, host, failureClass)` while open. `other` uses partial uniqueness on
`(harness, host, descriptionDigest)` while open. Different descriptions may
open concurrent `other` incidents for one shared harness. The gate remains
closed until no active incident remains.

Add durable `harness_health_other_reviews`, `harness_health_other_routes`, and
`harness_health_class_promotions`, plus append-only
`harness_health_other_review_events`. The review row is keyed by incident id and
stores `pending|closed`, current custodian, route ordinal, and nullable outcome
`confirmed_other|reclassified|promotion_required`, named class, reviewer,
cause, and closed time. Database checks require a named class only for
`reclassified`; a recurrence requires `promotion_required` and its promotion
case id. Delete and a second close are refused.

A route row stores incident id, increasing ordinal, target kind
`session|owner_user`, target reference, relation `parent|ancestor|owner_main|owner_user`,
state `skipped|pending|delivered|non_delivered|alerted`, closed reason, notice
wake id, turn seq, created time, and settled time. State/reason combinations
are closed: `skipped` requires `inactive|foreign_owner|cycle|hop_limit`;
`non_delivered` requires `failed|failed_unknown|canceled|target_retired`;
`pending|delivered` require no reason; `alerted` requires `no_active_main`.
`(incidentId, ordinal)` and each non-skipped `(incidentId, targetKind,
targetRef)` are unique. Updates permit only the named one-way transitions.

The event table appends admission, route, delivery, custody, review, recovery,
expiry, recurrence, and promotion transitions with event kind, source row,
typed principal, cause, and time. The promotion table is keyed by description
digest. It stores `open|closed`, the first and second incident ids, creation
principal `process:tightbeam`, and, when closed, named class, canonical spec
name, exact spec SHA-256, reviewed-clean attest id, closer, and close time.

### ARC-03 — Atomic opening, dedupe, and concurrency

Normalize and validate the complete input, authorize against stored session
and lineage rows, compute the description digest, expire any due matching
incident, and use the existing
transaction owner. In one transaction:

1. insert the immutable observation;
2. open or attach to the matching active other incident;
3. assert the reserved `harness-other-unavailable` standing fact when opening;
4. create the pending review and first route when opening;
5. count admitted incidents with the exact description digest;
6. on count two, insert the one promotion case; on later counts, attach the
   incident to that case; and
7. append typed events and the deterministic notice turn or owner alert.

Idempotency scope is `(principal, harness-health-observe-other,
idempotencyKey)`. An exact replay returns the original observation, incident,
review, promotion, and route ids and writes nothing. A key replay with any
different normalized field returns `idempotency_conflict`. Concurrent openings
with distinct keys for the same `(harness, host, descriptionDigest)` create one
observation per key, produce one incident, and attach both observations. The
unique indexes arbitrate; retry reads the winning rows.

### ARC-04 — Immediate upward review routing

The opening transaction selects the nearest active same-owner ancestor of the
source session. `main` walks `effective_parent`; `0.1.9` walks `spawnedBy`.
Inactive, missing, repeated, foreign-owner, and over-32-hop candidates append
skipped routes and never receive evidence. With no active ancestor, route to
the source owner's active Main. With no active Main, append an owner-user route
and use the existing tokenless alert surface.

A session route creates one notice turn with deterministic identities
`wakeId=other-review:<incidentId>:<target>` and
`requestRef=other-review:<incidentId>`. The notice contains the incident id,
harness, host, description digest, expiry time, and a restricted read pointer.
It contains no sensitive evidence text. `delivered` makes that session the
review custodian. `failed`, `failed_unknown`, `canceled`, target retirement, or
an enqueue race appends the terminal route result and selects the next rung.
Restart resumes the first pending or non-delivered route. A delivered route is
never repeated.

The owner-user alert and its event commit together before any push. Store is
truth; reconnect can replay it. Failed push does not duplicate the alert.
Review routing does not wait for or change incident expiry.

### ARC-05 — Review and promotion

An authorized reviewer closes a pending review through one idempotent mutation.
For the first incident with a digest, it selects `confirmed_other` or
`reclassified` and gives a non-empty cause. `reclassified` names one of the six
existing classes and links the existing repair guidance; it does not rewrite
the original incident or observation.

For a recurrence, the only admitted outcome is `promotion_required`, bound to
the digest's open promotion case. The second incident creates that case even if
its first incident's review is still pending. Later incidents share it. The
promotion case closes only with a new named class, canonical spec name, exact
SHA-256, and one different-session `reviewed-clean` attest bound to those bytes.
Closing a promotion case does not migrate historical `other` rows. A later
classifier release may recognize the new class prospectively.

Expiry never closes a review. Every list and trace read exposes pending reviews
and open promotions until an authorized reviewer closes them. The substrate
does not decide whether two different digests mean the same cause.

### ARC-06 — Shared gate, recovery, and expiry

Expose one transaction-owned `HarnessHealth.prod_shape_gate_in_txn/4` taking
`txn`, `harness`, `host`, and `now`. Every prod-shaped consumer calls it after
selecting a candidate and immediately before writing or dispatching an action.
It first expires due `other` incidents, then returns:

```text
available
unavailable {incidentIds, failureClasses, earliestExpiryAt?}
```

The known-class decision remains the existing standing-fact decision. An
`other` decision requires `state='open' AND now < expiresAt`. At the expiry
instant, the function atomically changes the due incident to `expired`, files
`harness-other-restored`, records `expiredAt` and `expiryFactId`, and appends an
event before it decides availability. A separate consumer cannot skip this
step or copy its predicate. The transaction rechecks the selected prod-shaped
candidate after an `available` result before it writes the action.

An authorized `harness-health-resolve-other` mutation requires the incident id,
an exact probe and output digest, `observedAt`, `worldStatus=PROVEN`, cause,
`redactionConfirmed=true`, and idempotency key. It must prove the caller's
recorded recovery condition; the substrate records the caller's assertion and
does not parse the condition. Before `expiresAt`, it writes a normal-success
observation, changes the incident to `resolved`, and retracts the standing
fact atomically. At or after `expiresAt`, expiry wins and resolution returns
`incident_expired` without claiming recovery.

If another active incident remains for the same harness, the gate remains
unavailable. A normal delivered turn continues to resolve the six known
classes as today; it does not resolve `other` without the explicit proof.

### ARC-07 — Authorization and privacy

Mutation authorization uses stored typed principals. Presentation origin,
prompt text, role label, model output, and a caller-supplied owner never confer
authority. A review custodian can read and review only its routed incident. An
owner and admin can read every incident for that owner. An active same-owner
ancestor can read an incident only while it is a route target or custodian.

Detail reads return exact evidence only to those principals. Ordinary incident
lists, prodder output, garbage-collector output, notices, lifecycle summaries,
logs, firehose rows, and metrics expose only ids, class, harness, host, state,
times, status, and review/promotion state. They never expose description,
description digest, error, probe, output digest, recovery, not-known reason,
idempotency key, or free-text cause. The routed same-owner review notice may
carry the description digest because its recipient already has detail-read
authority.

Only an admin can read a promotion case's cross-owner incident membership. A
source owner or review custodian sees its own incident and the fact that a
promotion is required, never another owner's incident id or equality evidence.

Metrics are aggregate counts keyed only by line, class, state, evidence mode,
world status, route result, review outcome, and promotion state. They exclude
user, session, assignment, work item, host, harness, principal, cause, exact
time, text, and digest.

### ARC-08 — Migration, rollback, and compatibility

Each line performs one transactional, stamped copy migration. It validates its
one exact predecessor stamp before creating complete replacement tables,
copying rows with new columns null, rebuilding indexes and triggers, validating
counts and foreign keys, swapping tables, creating the four new tables, and
advancing the stamp. It never sniffs DDL to guess a predecessor.

The target stamps are `harness-health-other-v1-main` and
`harness-health-other-v1-019`. Main accepts only
`coordination-fabric-v1-phase1-v15`. The 0.1.9 implementation records in its
candidate report the exact reviewed four-class predecessor commit and stamp;
this contract admits only that stamp. Missing, unknown, partially migrated, or
already conflicting objects cause `harness_health_other_schema_conflict` and
abort startup before Supervision, the prodder, or the session garbage collector
starts.

A crash before commit leaves the predecessor stamp and tables. A restart runs
the same migration. A crash after commit reads the target stamp and starts
without copying again. Target stamp plus a missing or mismatched object is a
refusal, not a repair loop.

Rollback uses the old binary only against a preserved pre-migration database
copy. The old binary must refuse a target-stamped database. No down-migration
drops evidence or rewrites `other` as a named class. New clients accept all
seven class strings. Old clients that do not recognize `other` display it as an
opaque class with its state and incident id; they cannot mutate it. Existing six-class
request and response bytes remain unchanged.

### ARC-09 — Observability and red-tape silence

Owner/admin trace joins the incident, immutable observations, standing fact,
expiry, routes and notice terminals, current custodian, review, recurrence,
promotion case, and recovery or expiry event. Every row includes its causal id,
typed principal, and timestamp. A restart read produces the same trace.

The shared gate emits one typed suppression event only when a prod-shaped
candidate is actually denied. The event names consumer kind, candidate id,
harness, host, blocking incident ids and classes, and earliest expiry. It
contains no evidence text. Repeated evaluation of the same consumer candidate
and unchanged blocking incident set dedupes to one event.

No incident means no gate event. A known-class incident produces no new
question, review, promotion, expiry, or evidence requirement. Opening `other`
produces one consolidated review notice, not one notice per affected session or
assignment. Expiry produces one transition and no prompt. Promotion produces
one notice when its case first opens and no repeated notice for later attached
incidents.

## Acceptance

1. **OTH-AC-01 — Required fields.** Given an authorized caller and one table row
   for each required ARC-01 field omitted, empty after trim, malformed, stale,
   or mutually inconsistent, when it calls `harness-health-observe-other`, then
   the typed refusal names the invalid fields and zero observation, incident,
   fact, review, route, event, turn, wake, or promotion rows change.
2. **OTH-AC-02 — Exact error entry.** Given a fresh `PROVEN` exact-error WORLD
   FACT with redaction confirmed, when an authorized source owner admits it,
   then one transaction writes the exact error, description digest, recovery
   condition, not-known reason, cause, principal, open incident, 15-minute-or-
   shorter expiry, standing fact, pending review, first route, and notice.
3. **OTH-AC-03 — Probe digest and unreachable probe.** Given `probe_digest`,
   when the probe or 64-character digest is missing, then admission refuses.
   Given `UNKNOWN`, when the failed exact probe and exact refusal are present,
   then admission records UNKNOWN without treating the subject as absent.
4. **OTH-AC-04 — Authorization and privacy.** Given a foreign-owner session,
   inactive session, unrelated same-owner session, or unauthenticated caller,
   when it opens, reads, reviews, or resolves `other`, then the operation refuses
   with no side effect. Given an ordinary list, notice, event, log, firehose, or
   metrics read, then none of the sensitive fields in ARC-07 appears.
5. **OTH-AC-05 — No automatic fallback.** Given a terminal error that matches
   none of the six classifiers, when the turn closes, then it creates no
   `other` row. The terminal truth remains visible. Given each six-class
   specimen, its class, threshold, repair action, and no-revocation behavior
   match the pre-change line.
6. **OTH-AC-06 — Whole-harness shared gate.** Given an active `other` incident
   for `(codex,gibson)`, when the assignment prodder, session garbage collector,
   and every registered prod-shaped test consumer reach their act boundary,
   then all call `prod_shape_gate_in_txn/4`, record no prompt or turn, and return
   the same incident id. A consumer for `(claude,gibson)` proceeds.
7. **OTH-AC-07 — Act-time race.** Given a consumer selected work before an
   incident opened, when the incident commits before the consumer's act
   transaction, then the consumer re-reads the shared gate and writes no action.
   Given the consumer commits first, then its one action may exist and the later
   incident pauses subsequent actions.
8. **OTH-AC-08 — Immediate living-authority route.** Given active, inactive,
   foreign-owner, and cyclic ancestor fixtures on both lines, when `other`
   opens, then the exact line adapter selects the nearest active same-owner
   ancestor, appends skipped evidence for rejected rungs, and sends one redacted
   notice. A delivered turn makes that target custodian but leaves review open.
9. **OTH-AC-09 — Escalation failure and owner terminus.** Given the first notice
   ends `failed`, `failed_unknown`, `canceled`, or loses to target retirement,
   when routing resumes, then it records that result and selects the next rung
   once. With no active ancestor it uses active Main; with no active Main it
   commits one tokenless owner alert and no model turn.
10. **OTH-AC-10 — Idempotency and concurrent opens.** Given exact replay of one
    key before or after restart, then all returned ids match and counts do not
    change. A changed payload with that key conflicts. Two concurrent distinct
    keys for the same harness and description create one open incident, two
    observations, one review, one active fact, and one initial route.
11. **OTH-AC-11 — Multiple other causes.** Given two descriptions with different
    digests on one harness, when both are admitted, then two incidents open.
    Resolving or expiring one leaves the gate unavailable until the other is no
    longer active.
12. **OTH-AC-12 — Evidenced recovery.** Given an active `other` incident and an
    authorized fresh `PROVEN` recovery probe, when resolve commits before
    expiry, then one transaction appends proof, marks `resolved`, retracts its
    fact, preserves opening evidence, and never invokes revocation. The same key
    replays without a second transition.
13. **OTH-AC-13 — Deterministic expiry race.** Given `now < expiresAt`, recovery
    may resolve. Given `now >= expiresAt`, when recovery and a prod-shaped gate
    contend in either start order, SQLite serialization yields one `expired`
    transition, one retract fact, no resolved claim, no denied prod because of
    that incident, and the recovery call returns `incident_expired`.
14. **OTH-AC-14 — Crash and restart.** At barriers after observation insert,
    incident insert, fact assertion, review insert, route insert, notice enqueue,
    expiry state write, and recovery proof insert, force rollback or process
    loss. After restart, either the whole owning transaction is absent or its
    complete state is readable; replay writes no duplicate and does not extend
    expiry or resend a delivered notice.
15. **OTH-AC-15 — Review is durable.** Given delivery, resolution, or expiry,
    when no authorized review outcome exists, then the review stays pending and
    owner/admin trace lists it. Given an authorized first-occurrence review,
    then `confirmed_other` or a named-class `reclassified` closes it once with
    reviewer, cause, and time.
16. **OTH-AC-16 — Recurrence promotion.** Given two admitted incidents with byte-
    identical trimmed descriptions and any harness or host, when the second
    commits, then exactly one promotion case opens and its review permits only
    `promotion_required`. A third attaches without a second case or notice.
    Case close refuses without a canonical spec name, exact SHA-256, distinct-
    session reviewed-clean attest, and new named class.
17. **OTH-AC-17 — Digest exactness.** Given descriptions that differ only by
    case or internal whitespace, when admitted, then their digests differ and
    they do not recur. Given descriptions that differ only in leading or
    trailing whitespace, their trimmed bytes and digests match.
18. **OTH-AC-18 — Migration and rollback.** On each line, given its exact
    predecessor fixture with open and resolved six-class incidents, when the
    migration runs, then counts, ids, foreign keys, facts, and old response
    bytes remain exact; new columns are null; the target stamp is exact. Each
    forced migration barrier rolls back to the predecessor. Unknown, partial,
    or target-stamp-with-bad-object fixtures refuse before supervision starts.
19. **OTH-AC-19 — Shared-gate registration.** Given the prodder and session
    garbage collector plus every module registered as prod-shaped, when a
    static call-site test scans their act boundaries, then each calls only the
    shared gate and no module contains a direct harness-health, condition-fact,
    adapter, process, or harness-up predicate. Adding a prod-shaped consumer
    without registration makes the test fail.
20. **OTH-AC-20 — Quiet-path silence and observability.** Given no active
    incident, repeated gate calls write nothing. Given one denied candidate,
    repeated identical calls produce one redacted suppression event. Given an
    open, resolved, expired, reviewed, recurrent, and promoted fixture, the
    authorized trace reconstructs cause, principal, evidence, route, custody,
    review, expiry/recovery, and promotion from typed rows without parsing a
    notice.
21. **OTH-AC-21 — Cross-line parity.** Run OTH-AC-01 through OTH-AC-20 against
    targetless candidates based on the exact admitted `0.1.9` four-class port
    and current `main`. The observable outcomes, refusal codes, privacy,
    idempotency, expiry, and review/promotion semantics match. Only the declared
    parent adapter and schema stamps differ.

## Open Questions

None. Any implementation discovery that changes a field, deadline, authority,
state, refusal, migration predecessor, privacy boundary, route, gate, review, or
promotion rule must amend this canonical file and receive a new exact-revision
review before product work continues.
