# Durable activations v1

Status: evidence-only review correction — independent re-review required  
Date: 2026-08-09 UTC  
Work item: `wi_f4b531cd-3def-4d7b-b909-5ddcb6d170bf`  
Spec assignment: `asg_f479c53e-316d-49b9-a115-74dcdb531d38`  
Source baseline: Tightbeam `origin/main` at
`769d4b44a98aa7db862fdf5619f215aded66a408`  
Prior consumer recon: `art_487c6afe`, SHA-256
`209ab2017cc23ca214e8cc1203e4af3df739fca97305964aebee3059f92e6094`, verdict
`att_93563dce-7f04-4834-81b3-df3056c3e50a`  
Acceptance authority: Mike ruling
`att_1cacf1ba-c534-4bd1-b5ff-810aa2466376`  
Independent review: `art_c68595be`, SHA-256
`7e9609dc4e527ad4ae5d2fcd1adb61e8197b5a301ad2f4903b98c5c76f8a3caf`, verdict
`att_08d7db94-6f25-4f92-9a1e-ee64edcf1c91` (`changes-requested`) on
`asg_5c19357a-ce8d-486b-ab98-2fbd9ef3f394`  
Owner adjudication: `att_7dad38f1-da37-4149-992f-02fee0ade684`, corrected by
`att_43c81355-2b77-443f-9a62-640378c7f735`, supersedes only the broader F2 read remedy
in `att_f90f0efe-ca47-4115-acd4-605f780b6ae7` and requires the terminal same-work-item
successor bridge  
Operating pattern: a domain-owned adapter decides whether an external action may run;
Tightbeam records the adapter's declared input, authority evidence, attempt, observation,
notice, and acknowledgement.

## Goal

Define one neutral, durable substrate primitive for an accountable actor's attempt to
make a prepared input take effect at an external target. The primitive must preserve
the input identity, target identity, actor, asserted authorizer and basis, external
attempt identity, observation, output references, owner notice, acknowledgement, and
causal order without deciding domain readiness, authorization, success, or recovery
policy.

The primitive must pass these three mandatory consumer examples:

1. Engineering Kung Fu activates a prepared build in production.
2. Marketing Kung Fu activates an approved campaign in the field.
3. Biosciences Kung Fu initiates an approved experiment or instrument run on real samples.

The substrate surface must express those examples without knowing the meanings of build,
production, campaign, field, experiment, instrument, or sample. Each Kung Fu owns its
semantic rules, readiness, and authorization policy. Finance transaction execution is
optional additional sanity coverage and is not a publication gate.

Formal design verdict: **one new neutral activation event stream is required**. Existing
rows preserve related evidence but cannot represent this occurrence mechanically. The
proposed `production_deploy_facts` stream and `deploy-*` verbs in `art_487c6afe` are
recast as one Engineering consumer mapping to this primitive. They do not become a
second substrate surface.

## Non-Goals

- Tightbeam does not decide whether an input is ready.
- Tightbeam does not decide whether an asserted authorizer has sufficient authority.
- Tightbeam does not interpret an authority basis, a target, or a domain result code.
- Tightbeam does not execute the external action.
- Tightbeam does not choose a rollback, retry, compensation, or reconciliation policy.
- Tightbeam does not block assignment completion as a consequence of activation state.
- This spec does not create a generic check registry, workflow engine, release planner,
  transaction processor, laboratory information system, campaign manager, or policy
  engine.
- This spec does not define regulatory, safety, financial, scientific, or marketing
  compliance.
- This spec provides no content, free-text, secret, credential, patient-data,
  audience-member-data, or transaction-instruction field. Domain owners must classify
  opaque identifiers before filing them; Tightbeam validates identifier shape and protects
  relational reads but cannot prove that a caller did not encode sensitive meaning in an
  identifier.
- This spec does not change the semantics of assignments, attests, verdicts, artifacts,
  commit references, condition facts, causal events, work items, or wakes.
- This spec does not claim that an external action is mechanically gated until its
  domain-owned mutation seam adopts the activation verbs.
- This spec does not promote Finance transaction execution from optional sanity coverage
  into a mandatory substrate acceptance example.
- No source change, deployment, external action, or live-row probe is authorized by this
  document.

## Terms

**Activation** — one declared attempt to make one prepared-input identity take effect at
one external-target identity. An activation is a durable claim about an external action,
not a Tightbeam judgment that the input became live.

**Prepared input** — a domain-owned immutable identity supplied as a `ResourceRef`. The
domain decides what preparation means. Examples are a release artifact, a campaign
bundle, an experiment run plan, and a signed transaction instruction.

**External target** — a domain-owned destination supplied as a `ResourceRef`. Examples
are a service generation, an advertising-platform campaign, an instrument/run slot, and
a payment rail instruction endpoint.

**Recording principal** — the authenticated Tightbeam user or session that appends an
activation event. Tightbeam derives this principal from the credential. A client cannot
supply it.

**Executor** — the domain identity that performs the external action. A domain adapter
asserts it as a `DomainIdentity`. Tightbeam records the assertion and does not authenticate
the external identity.

**Authorizer** — the domain identity named by an `authority-attached` event. This is an
asserted domain identity, distinct from the recording principal.

**Authority basis** — a `ResourceRef` to the immutable record on which the domain relies.
The domain decides what the reference means and whether it is current.

**Activation owner** — the existing Tightbeam user named at declaration time to receive
attempt, observation, reconciliation, and withdrawal notices. This is a notification and
read-access identity. It is not an authorization grant.

**Domain adapter** — the product-owned component that checks its domain's readiness and
authorization policy, receives Tightbeam's committed `attempted` response immediately
before the external mutation, performs the mutation, observes the target, and records that
observation.

**Attempt** — the single external action represented by one activation. A domain retry is
a new activation linked with `retry-of`; an idempotent replay of the same Tightbeam call is
the same attempt event.

**Observation** — a domain adapter's recorded claim about the external result. A
`determinate` observation carries a result the adapter considers knowable. An
`indeterminate` observation preserves uncertainty without converting absence into
failure.

**Reconciliation** — one later event that resolves an indeterminate observation to either
`determinate` or `irrecoverable`. `Irrecoverable` means the domain actor has made the
explicit decision to stop seeking stronger external truth; it is not a success or failure
classification.

**Terminal activation** — an activation with a valid `withdrawn` event before an attempt,
a `determinate` observation after an attempt, or a reconciliation after an indeterminate
observation. Acknowledgement changes notice state and does not change terminality.

**Compensating activation** — a new activation whose declaration links to a prior
activation with relation `compensates`. A rollback is one domain use of this relation.

**Successor activation** — a new activation whose declaration links to a prior activation
with relation `supersedes`. Domain ownership or authority transfer uses this relation
instead of rewriting the old activation.

**Successor bridge** — a declaration-only admission path for `supersedes`. It lets the
holder of the new root assignment name one terminal prior activation on the same work item
without reading that prior stream. The bridge discloses no prior payload, creates no prior
read relation, and supplies only the prior-link admission check. The held new root
assignment remains the declaration's write authority; the bridge grants no domain or write
authority.

**OpaqueToken** — 1–512 ASCII letters, digits, dots, underscores, colons, slashes, at
signs, plus signs, equals signs, or hyphens: `[A-Za-z0-9._:/@+=-]{1,512}`. It contains no
whitespace or control character. A field can set a smaller bound.

**ResourceRef** — exactly `{namespace, id, sha256}`. `namespace` is 1–64 lowercase
letters, digits, dots, underscores, or hyphens. `id` is an `OpaqueToken`. `sha256` is
either 64 lowercase hexadecimal characters or `null`. The object accepts no other key.
Each event shape states whether its `sha256` can be `null`.

**DomainIdentity** — exactly `{namespace, id}`. Its `namespace` and `id` follow the
corresponding `ResourceRef` rules. It contains no display name, email address, secret, or
credential.

**DomainCode** — exactly `{namespace, code}`. `namespace` follows the `ResourceRef`
namespace rule. `code` is an `OpaqueToken` bounded to 64 characters. Tightbeam compares
the bytes and does not interpret them.

**Recovery principal** — the authenticated principal that filed the `attempted` event; if
that principal is a session, its owning user or another session owned by that user; the
work-item-owner user or one of that user's sessions; or a holder session with an open
assignment on the same work item. This relation permits observation and reconciliation
after the root assignment or work item becomes terminal. It grants no domain authority.

**Notice requeue** — an append-only event that links one canceled owner-notice wake to one
new wake for the same noticed event. It changes notice delivery state only.

**Canonical semantic request** — the closed object containing the verb, caller-supplied
root assignment for `declared`, caller-supplied activation ID when applicable, predecessor
event ID when applicable, caller-supplied acting assignment when applicable, and the closed
event payload. It excludes the idempotency key, credential, and wire envelope. Tightbeam
uses the canonical camel-case wire field names, preserves explicit `null`, rejects aliases
and floating-point numbers, and encodes the object with RFC 8785 JSON Canonicalization
Scheme before computing SHA-256.

**Static design fixture** — one exact JSON line embedded in section 9. Its recorded SHA-256
covers that UTF-8 line plus one trailing LF. It demonstrates that one mandatory domain can
map a complete expected stream into the closed v1 shapes. It is design evidence, not a
gateway, wake, adapter-ordering, or external-target capture.

**Runtime activation fixture** — one immutable, protected implementation artifact captured
from a real domain adapter, real Tightbeam gateway and wake pipeline, and real external
target. It contains raw response envelopes or immutable references to them, plus an ordered
adapter trace from capture instrumentation. The trace binds the committed
`attempted.eventId` response and `externalAttempt.id` to the first external-mutation spy
invocation, records zero mutation invocations before that response, and records the later
observation, notice, and acknowledgement. It also contains the mutation-before-attempt
negative mutant and crash/replay cases required by R-09c. A static design fixture or
hand-written ideal response is not a runtime fixture.

**Notice acknowledgement** — an explicit event filed by the activation owner after the
corresponding wake reaches `fired`. A fired wake proves enqueue, not human receipt.

## Assumptions

1. Each adopting domain can expose one adapter seam before its external mutation and one
   observation seam after it. A path without those seams remains outside mechanical
   activation recording.
2. Each adopting domain can provide stable input, target, executor, external-attempt,
   basis, evidence, and output references without placing sensitive content in Tightbeam.
3. The activation owner exists as a Tightbeam user with a personal session row.
4. Domain systems retain the content behind supplied references. Tightbeam preserves the
   reference and the digest where an event shape requires one, not the referenced bytes.
5. A domain adapter can decide to retry, compensate, supersede, withdraw, or reconcile a
   prior activation. Tightbeam records those decisions.
6. Current assignments carry holder, opener, work-item linkage, timestamps, terminal
   outcome, and optional review linkage, but no target, external attempt, authority basis,
   observation, or acknowledgement (`lib/tightbeam/assignments.ex:32-92` at the source
   baseline).
7. Current verdicts accept a bounded free-form `verdictKind` from a user or session and do
   not resolve domain authority (`lib/tightbeam/assignments.ex:1044-1067,1477-1491`).
8. Current commit references prove that a commit exists at a known repository, and their
   filing is limited to producing completion or review-linked verdict evidence. They do
   not identify an external activation (`lib/tightbeam/assignments.ex:1336-1424`).
9. Current artifacts preserve a pointer, optional caller-supplied digest, creator,
   work-item link, and labelled turn-observation quality. Their kind vocabulary and public
   list surface do not supply activation lifecycle or private activation reads
   (`lib/tightbeam/artifacts.ex:31-50,70-148,183-207`;
   `lib/tightbeam/gateway.ex:702-706`).
10. Current causal events accept substrate-authored kinds only. Their necessity rule
    rejects domain-authored activation facts (`lib/tightbeam/causal_events.ex:1-38,94-121`).
11. Current event rows are observability records. Core logic does not consume them as
    domain state (`lib/tightbeam/event_log.ex:1-17,64-124`).
12. Current wakes are a durable, at-least-once outbox. Wake IDs deduplicate turn enqueue,
    and `fired` records delivery into the turn pipeline rather than acknowledgement
    (`lib/tightbeam/wakes.ex:1-22,453-491,548-618`;
    `lib/tightbeam/ledger.ex:1-18,39-76`).
13. Current wire idempotency covers a closed operation set and stores the original result
    pointer. It does not store the canonical request digest required to reject a changed
    replay (`lib/tightbeam/idempotency.ex:1-29,83-107`).
14. Current boot recovery converts interrupted running turns to `failed_unknown` and does
    not retry external tools (`lib/tightbeam/ledger.ex:421-449`;
    `lib/tightbeam/boot.ex:24-38`).
15. A new table is compatible with the current additive schema bootstrap when it leaves
    old tables readable. Older binaries can ignore the table. A client that requires the
    table needs an explicit capability check (`lib/tightbeam/schema.ex:33-69`).
16. No existing spec found in the searched shared spec trees names a neutral activation
    pattern. `art_487c6afe` is evidence and a deploy-specific proposal, not live neutral
    authority.
17. The current `GET /version` response exposes `protocolVersion`, `server`, and adapter
    health but no generic feature list (`lib/tightbeam/wire/router.ex:24,101`). This
    spec therefore adds one neutral `features` list to that response instead of claiming an
    existing capability-advertisement surface.

## Invariants

**I-1 — Policy boundary.** Tightbeam's activation decision surface is limited to caller
identity, schema shape, referenced Tightbeam-row existence, causal ordering, idempotent
replay, stream uniqueness, relational read access, and durable notice delivery. Tightbeam
does not verify the existence or meaning of an external `ResourceRef`. Domain adapters
decide readiness, authorization sufficiency, result meaning, terminal business outcome,
retry, compensation, and reconciliation timing.

**I-2 — One semantic primitive.** The substrate has one `activation_events` stream and a
fixed activation verb family. Engineering uses that family. No `production_deploy_facts`
table or `deploy-*` substrate verb exists beside it.

**I-3 — Append-only truth.** An accepted event creates one row. Corrections use a named
later event or a successor activation. No verb updates or deletes an activation event.

**I-4 — Cause and principal.** Each event stores one exact authenticated recording
principal and, except `declared`, the exact prior stream head. An authority event also
stores its asserted authorizer and basis.

**I-5 — Observation is not adjudication.** A domain result remains an opaque `DomainCode`.
Tightbeam exposes it and does not map it to success, failure, readiness, settlement,
scientific validity, campaign approval, or service health.

**I-6 — One mutation seam.** Fixed activation verbs are the sole writers of activation
events. No generic fact-writer verb accepts a caller-selected kind or arbitrary payload.

**I-7 — Atomic replay or append.** Principal-scoped idempotency lookup and digest comparison
run before current access, assignment, head, or lifecycle validation. An exact hit returns
the original result. On a miss, access, stream-head and lifecycle validation, the event
insert carrying its idempotency data, and required wake scheduling occur in one database
transaction.

**I-8 — One attempt per activation.** An activation accepts at most one `attempted` event.
A domain retry declares a new activation and names the old activation with `retry-of`.

**I-9 — Uncertainty stays visible.** A missing observation leaves an unresolved attempt.
Boot, timeout, wake delivery, or process death does not synthesize an external result.

**I-10 — Compensation is an activation.** A rollback or reversal uses a new declaration
with relation `compensates`. It receives its own authority, attempt, observation, notices,
and acknowledgement.

**I-11 — Immutable owner snapshot.** The activation owner does not change within a stream.
A domain transfer uses a successor activation. Existing authority events remain bound to
the old stream and do not silently follow the successor.

**I-12 — Protected minimal payload.** Activation queries enforce relational read access.
Event-log and wake projections carry an activation ID and event kind but omit resource,
identity, result, and evidence objects.

**I-13 — Notice is evidence, not a gate.** Attempt, observation, reconciliation, and
withdrawal append a durable owner wake in the same transaction. Missing acknowledgement
stays queryable and does not block an assignment lifecycle verb.

**I-14 — Consumer enforcement is explicit.** A consumer claims a mechanical activation
gate only after its domain-owned mutation seam receives the committed `activation-attempt`
response before the external operation and records the observed response afterward.

**I-15 — Compatibility is advertised.** An adapter that depends on this contract checks
for `activation-events-v1` before external mutation. Capability absence produces a named
refusal at the adapter seam.

**I-16 — A write cannot mint its own access.** Except for declaration, a non-replay caller
must already qualify to read the activation before Tightbeam evaluates the event-specific
write relation. Filing an event never bootstraps read access for an otherwise unrelated
principal.

**I-17 — Evidence-bearing references are content-bound.** Prepared input, authority basis,
target-state snapshots, observation evidence, reconciliation evidence, and withdrawal
basis require non-null SHA-256 digests. Target and external-action identifiers can carry
`null` when no stable referenced bytes exist.

**I-18 — Successor admission does not disclose the predecessor.** The successor bridge
checks only the `supersedes` relation, prior terminality, same-work-item linkage, and the
caller's holdership of the new root assignment. Its accepted response contains the new
activation row and no prior-stream field beyond the prior activation ID supplied by the
caller. The bridge creates no read relation. The held new root assignment, not the bridge,
authorizes the declaration; the bridge grants no domain or later-write authority.

## Architecture

### 1. Existing-fact disposition

| Existing fact | Reuse | Why it is not the activation primitive |
| --- | --- | --- |
| Work item | Correlates the durable product thread and supplies a trace boundary. | It has no external input, target, authority, attempt, or observation. |
| Assignment | Supplies accountable work and a holder relation. | It describes an obligation, not an external occurrence. |
| Attest/verdict | Remains work progress, closure, or judgment evidence. | Its note and verdict vocabulary cannot carry a closed activation schema without parsing. |
| Commit reference | May be named inside a `ResourceRef` or remain completion evidence. | It proves repository object existence, not external effect. |
| Artifact | May hold detailed evidence outside the activation row. | Its digest is optional, its kinds omit activation lifecycle, and its current list is not private. |
| Causal event | Remains a substrate-only record of overwritten internal transitions. | Its admission law excludes agent-authored domain occurrences. |
| Event log | Records accepted and denied activation verbs with redacted metadata. | Core logic does not use observability rows as domain state. |
| Wake | Supplies the durable owner-notice outbox. | `fired` proves enqueue and requires a separate acknowledgement fact. |
| Condition fact | No activation use in v1. | `{kind, scope, origin, ts}` cannot carry the contract and a new generic kind would duplicate the primitive. |
| Wire idempotency | Pattern reused, table not reused. | The existing row lacks canonical request bytes and its closed operation set has no activation verb. |

Requirement R-01: the implementation represents the Engineering occurrence through the
same `activation_events` table and fixed activation verbs used by the other mandatory
consumers.  
Acceptance: A-01 and A-22.

### 2. Event store

Add one table named `activation_events`:

```text
seq                   INTEGER PRIMARY KEY AUTOINCREMENT
eventId               TEXT UNIQUE NOT NULL, prefix aev_
activationId          TEXT NOT NULL, prefix act_
kind                  TEXT NOT NULL, closed set below
predecessorEventId    TEXT NULL REFERENCES activation_events(eventId)
rootAssignmentId      TEXT NOT NULL REFERENCES assignments(id)
workItemId            TEXT NOT NULL REFERENCES work_items(id)
actorAssignmentId     TEXT NULL REFERENCES assignments(id)
bySession             TEXT NULL REFERENCES sessions(sessionKey)
byUser                TEXT NULL REFERENCES users(userId)
idempotencyKey        TEXT NOT NULL
requestSha256         TEXT NOT NULL, lowercase canonical-request SHA-256
payload               TEXT NOT NULL, canonical JSON with a closed per-kind schema
noticeWakeId          TEXT NULL REFERENCES wakes(wakeId)
ts                    INTEGER NOT NULL, substrate time
```

The closed `kind` set is:

```text
declared | authority-attached | attempted | observed |
reconciled | withdrawn | notice-requeued | acknowledged
```

Database constraints enforce recording-principal XOR, event-ID uniqueness, one
`declared`, one `attempted`, one `observed`, one `reconciled`, one `withdrawn`, and one
acknowledgement per noticed event. They also permit only one `notice-requeued` event for a
given canceled wake. Partial unique indexes scope idempotency separately to session and user
principals by `(principal, kind, idempotencyKey)`.

The gateway derives the authenticated principal and canonicalizes the semantic request
after stripping transport-only fields. It then evaluates the principal, kind, and
idempotency-key tuple in this exact order inside a transaction:

1. an existing tuple with the same `requestSha256` returns the original event and wake IDs
   before current access, assignment, stream-head, or lifecycle checks;
2. an existing tuple with a different digest refuses `idempotency_conflict`; and
3. a missing tuple proceeds to current access, assignment, stream-head, lifecycle, append,
   uniqueness, and wake checks.

`idempotencyKey` is an `OpaqueToken` bounded to 200 characters. It is not part of the
canonical semantic request because the database key already carries it.

For `declared`, `rootAssignmentId` is part of the canonical semantic request before
idempotency lookup. The same principal, key, and payload against a different root
assignment therefore has a different `requestSha256` and refuses `idempotency_conflict`.

Except for `declared`, a caller supplies `predecessorEventId`. In the same insert
transaction, Tightbeam verifies that it is the current stream head. A stale head refuses
`activation_head_changed` and returns the current head ID. The check and insert form one
indivisible step.

Clients supply `rootAssignmentId` only to `declared`. Tightbeam copies
`rootAssignmentId` and `workItemId` from the declaration into every later event. A client
never supplies either field on a later append.

Requirement R-02: an accepted event has one principal, one canonical request digest, one
substrate timestamp, and one immutable causal position.  
Acceptance: A-02, A-03, A-04, and A-05.

### 3. Closed event shapes

`declared` requires:

```text
ownerUserId        existing Tightbeam user
domain             namespace
correlationKey     OpaqueToken, maximum 200 characters
preparedInput      ResourceRef
target             ResourceRef
prior              null | {activationId, relation: retry-of | compensates | supersedes}
```

`correlationKey` is an `OpaqueToken` bounded to 200 characters.
`preparedInput.sha256` must be non-null; `target.sha256` can be `null`. The caller must be
a session holding `rootAssignmentId`; the assignment must be open and linked to an open
work item. Tightbeam derives `workItemId`. `ownerUserId` must name either the work-item
owner or the owning user of the root-assignment holder session; this prevents declaration
from granting visibility to an unrelated user. A `retry-of` or `compensates` prior must be
readable to the caller and belong to the same work item. A `supersedes` prior can use that
full-read path or the successor bridge. The bridge succeeds only when the caller holds the
new open root assignment and the prior activation is terminal on that assignment's work
item. An unknown prior, unreadable non-bridge prior, non-terminal bridge prior, work-item
mismatch, or holder mismatch returns `not_found` without a prior payload or count leak. The
held new root assignment authorizes the declaration; the prior relation, full-read check,
and bridge grant no domain or later-write authority.

`authority-attached` requires:

```text
authorizer         DomainIdentity
basis              ResourceRef
decision           DomainCode
```

`basis.sha256` must be non-null. A direct user filer must be the activation owner, the work
item owner, or an admin. A session filer must be owned by one of those users or supply and
hold an open `actorAssignmentId` on the same work item. The caller must already qualify for
a full stream read. The recording principal may differ from the asserted authorizer; the
response labels both. The substrate verifies shape and linkage only.

`attempted` requires:

```text
authorityEventIds  1..32 distinct authority-attached event IDs on this activation
executor           DomainIdentity
externalAttempt    ResourceRef
targetStateBefore  ResourceRef | null
```

`externalAttempt.sha256` can be `null`. When `targetStateBefore` is non-null, its `sha256`
must be non-null. The caller supplies an open `actorAssignmentId` on the same work item and
must hold it, and must already qualify for a full stream read.
The domain adapter selects the authority event set after applying domain policy.
Tightbeam verifies that each named event belongs to this activation, precedes the attempt,
and appears in ascending stream sequence. It enforces the 1–32 shape bound but does not
assess whether the bounded count is sufficient, nor does it assess quorum, decision code,
authorizer, basis, expiry, or readiness. `attempted` and its owner wake commit together
before the adapter invokes the external operation.

`observed` requires:

```text
attemptEventId       this activation's attempted event
certainty            determinate | indeterminate
result               DomainCode
targetStateAfter     ResourceRef | null
outputs              0..32 ResourceRef values
evidence             ResourceRef
externalOccurredAtMs integer | null
```

`evidence.sha256` must be non-null. When `targetStateAfter` is non-null, its `sha256` must
also be non-null; output digests can be `null`. The caller must already qualify for a full
stream read and must be a recovery principal. `externalOccurredAtMs = null` explicitly
means the external source supplied no trustworthy occurrence time. The substrate records
the domain result without interpreting it. A non-null `externalOccurredAtMs` is an integer
from 0 through 9,223,372,036,854,775,807; Tightbeam does not compare it with substrate time.

`reconciled` requires a prior `observed` event whose certainty is `indeterminate`:

```text
observedEventId       the indeterminate observation
certainty             determinate | irrecoverable
result                DomainCode
targetStateAfter      ResourceRef | null
outputs               0..32 ResourceRef values
evidence              ResourceRef
externalOccurredAtMs  integer | null
```

`evidence.sha256` must be non-null. When `targetStateAfter` is non-null, its `sha256` must
also be non-null; output digests can be `null`. The caller must already qualify for a full
stream read and must be a recovery principal. A determinate observation does not accept
reconciliation. A non-null `externalOccurredAtMs` has the same integer bound as `observed`.
The reconciliation and owner wake commit together.

`withdrawn` requires:

```text
reason             DomainCode
basis              ResourceRef
```

`basis.sha256` must be non-null. The caller must already qualify for a full stream read and
must be the work-item-owner user or one of that user's sessions, or a holder session with an
open assignment on the same work item. Withdrawal is valid only before `attempted`.
Withdrawal and its owner wake commit together.

`notice-requeued` requires:

```text
noticedEventId     attempted | observed | reconciled | withdrawn event ID
replacesWakeId     canceled wake linked to that noticed event
```

The caller must already qualify for a full stream read and must be the activation-owner
user or one of that user's sessions, the work-item-owner user or one of that user's
sessions, an admin user or one of that user's sessions, or the principal that filed the
noticed event. The wake must be `canceled`, the noticed event must remain unacknowledged,
and no prior requeue may name that wake. Tightbeam atomically appends the event, schedules a
new owner wake, and stores the new wake ID in `noticeWakeId`.

`acknowledged` requires:

```text
noticedEventId     attempted | observed | reconciled | withdrawn event ID
acknowledgedWakeId fired wake stored on that event or a linked notice-requeued event
```

The caller must be the activation-owner user or a session owned by that user. The wake
must be `fired` and must link to `noticedEventId` either directly or through a
`notice-requeued` event. One acknowledgement records one noticed event. Acknowledgement
contains no approval, outcome, or relief meaning.

Unknown, missing, extra, wrong-type, over-bound, or non-canonical keys refuse before an
event or wake row is inserted.

Requirement R-03: each event kind accepts only its named payload and lifecycle position.  
Acceptance: A-06, A-07, A-08, A-09, A-10, A-11, and A-12.

### 4. Lifecycle and terminality

```text
declared
  ├─ authority-attached (one or more, domain-selected)
  │    └─ attempted
  │         └─ observed(determinate) ── terminal
  │         └─ observed(indeterminate)
  │                └─ reconciled(determinate|irrecoverable) ── terminal
  └─ withdrawn ── terminal

attempted | observed | reconciled | withdrawn
  ├─ notice-requeued (only after a linked wake is canceled)
  └─ acknowledged (notice state only)
```

Authority events may be appended before `attempted`. The stream admits no later authority
event after an attempt. A terminal stream admits `notice-requeued` and `acknowledged`
events for its noticed events and no other kind. Neither notice event changes the derived
activation state or terminality.

A retry, compensation, or authority/owner transfer creates a new activation. The new
declaration names the prior activation and relation. For an authority or owner transfer,
the domain adapter first terminalizes the old stream: it withdraws an unattempted stream,
or records the required observation or reconciliation for an attempted stream. Only then
does the new holder declare the `supersedes` activation through a full predecessor read or
the successor bridge. This ordering makes an old unattempted activation mechanically unable
to run after transfer. The bridge does not disclose the old stream or grant read, domain, or
later-write authority; the held new root assignment remains the declaration's authority.

Requirement R-04: the derived lifecycle follows the diagram and preserves unresolved
attempts as unresolved.  
Acceptance: A-13, A-14, A-15, and A-16.

### 5. Notice outbox and acknowledgement

For `attempted`, `observed`, `reconciled`, and `withdrawn`, Tightbeam schedules one existing
prompt wake to the declared owner's personal session in the event transaction. The wake
uses the work-item link and the acting-assignment link when `actorAssignmentId` is non-null.
Its prompt contains only the activation ID, event kind, and the command for the protected
status read. The event stores the wake ID. A replacement wake uses the same redacted prompt
and names the original noticed event kind.

Existing wake delivery remains at-least-once. A crash between delivery and `fired` may
redeliver; the turn ledger's unique wake ID deduplicates enqueue. A delivery exception
leaves the wake pending. A canceled or undeliverable wake remains visible and cannot be
acknowledged as fired. Once an operator cancels an undeliverable wake, an authorized caller
can use `activation-renotify` to append `notice-requeued` and schedule one replacement
wake. A second replacement is possible only if the immediately named replacement is later
canceled. No canceled wake can be requeued twice.

No activation fact is rolled back because live prompt delivery failed after commit. The
event and pending wake are the durable outbox state. No acknowledgement is inferred from a
turn result, transcript read, socket publication, or elapsed time.

Requirement R-05a: Tightbeam commits each noticed event and its pending wake atomically.  
Acceptance: A-17.

Requirement R-05b: Tightbeam replaces a canceled delivery only through a causally linked
`notice-requeued` append.  
Acceptance: A-18.

Requirement R-05c: Tightbeam records receipt only from an explicit owner acknowledgement
of a fired wake.  
Acceptance: A-12 and A-18.

### 6. Crash recovery, correlation, and dedupe

The adapter follows this order:

1. read `activation-status` and the external target;
2. apply domain readiness and authorization policy;
3. append or replay `attempted` while holding the domain mutation lock and receive its
   committed response;
4. invoke the external operation with `externalAttempt.id` as its domain idempotency or
   correlation reference;
5. observe the external target;
6. append `observed`; and
7. append `reconciled` later only when the first observation was indeterminate.

A crash before the `attempted` transaction leaves no attempted event. A lost response to a
committed attempt is recovered by replaying the same key and request bytes. When the crash
case's ordered adapter trace proves that no mutation began, the adapter receives the
replayed committed response before invoking the first mutation. Once a mutation may have
begun, recovery reads the external target and records an observation; it invokes no
additional mutation.

A crash after the external action and before `observed` follows the same recovery path. If
the external source cannot supply a determinate answer, recovery records an indeterminate
observation. A recovery principal may append the observation or reconciliation even after
the root assignment or work item becomes terminal; no work-item reopening or completion
gate is required. The correlation key groups related activations; it does not deduplicate
them. `externalAttempt` is the domain's action identity; Tightbeam's idempotency key
deduplicates only the Tightbeam append.

Requirement R-06: recovery reuses the committed attempt and appends observation or
reconciliation evidence. In a crash-before-mutation case, the ordered adapter trace proves
that no mutation began, and the adapter invokes the first mutation only after receiving the
replayed committed response. After a mutation may have begun, recovery invokes zero
additional mutations.  
Acceptance: A-19, A-20, and A-21.

### 7. Readers and data minimization

A full activation stream is readable by:

- the activation-owner user and sessions owned by that user;
- the work-item-owner user and sessions owned by that user;
- a holder session named by `rootAssignmentId` or `actorAssignmentId`, plus that session's
  owning user;
- a user or session that filed an event in the stream; and
- a Tightbeam admin user or a session owned by that admin.

An unreadable activation returns the same `not_found` response as an unknown activation.
List verbs omit unreadable rows before pagination and counts. A caller does not gain read
access by knowing an activation, work-item, assignment, wake, artifact, or external
reference ID alone. For a non-declaration append that is not an exact replay, Tightbeam
checks this read relation before event-specific write authority. The prospective filer
relation is not included in that check, so a write cannot mint its own read access. A
successful successor-bridge declaration grants read access to the new activation only;
status and list continue to return `not_found` or omit the prior activation unless another
listed read relation applies.

Event-log rows record verb, principal, activation ID, event kind, and accepted or denied
status. They omit canonical payload bytes. Work-item trace includes event ID, kind,
principal, acting assignment, substrate timestamp, and notice state for authorized trace
readers; it omits resource and domain-identity objects. Wakes omit those objects too.

The wire rejects free text and unknown payload keys. A domain that needs detailed or
sensitive evidence stores it in its own system and supplies a protected opaque reference
with the required or permitted digest stated in section 3.

Requirement R-07a: Tightbeam returns full activation payloads only to principals with a
named read relation.  
Acceptance: A-23.

Requirement R-07b: Tightbeam omits protected payload bytes from list, event,
trace-summary, and wake projections.  
Acceptance: A-24.

### 8. CLI and wire

Expose fixed CLI verbs:

```text
tightbeam activation-declare --assignment A --owner U --domain N
  --correlation C --input RESOURCE_JSON --target RESOURCE_JSON
  [--prior ACT --relation retry-of|compensates|supersedes] --key K

tightbeam activation-authority --activation ACT --after EVENT
  [--assignment A] --authorizer IDENTITY_JSON --basis RESOURCE_JSON
  --decision CODE_JSON --key K

tightbeam activation-attempt --activation ACT --after EVENT --assignment A
  --authority-events ID[,ID...] --executor IDENTITY_JSON
  --external-attempt RESOURCE_JSON --target-state-before RESOURCE_JSON|null --key K

tightbeam activation-observe --activation ACT --after EVENT [--assignment A]
  --attempt EVENT --certainty determinate|indeterminate --result CODE_JSON
  --target-state-after RESOURCE_JSON|null --outputs RESOURCE_JSON_ARRAY
  --evidence RESOURCE_JSON --external-occurred-at MS|null --key K

tightbeam activation-reconcile --activation ACT --after EVENT [--assignment A]
  --observation EVENT --certainty determinate|irrecoverable --result CODE_JSON
  --target-state-after RESOURCE_JSON|null --outputs RESOURCE_JSON_ARRAY
  --evidence RESOURCE_JSON --external-occurred-at MS|null --key K

tightbeam activation-withdraw --activation ACT --after EVENT [--assignment A]
  --reason CODE_JSON --basis RESOURCE_JSON --key K

tightbeam activation-renotify --activation ACT --after EVENT
  --noticed-event EVENT --replaces-wake W --key K

tightbeam activation-ack --activation ACT --after EVENT
  --noticed-event EVENT --wake W --key K

tightbeam activation-status --activation ACT
tightbeam activations [--assignment A | --work-item WI | --correlation C]
```

The wire uses the same verb names and camel-case field names. The router rejects caller
fields for top-level `eventId`, top-level `activationId` on declaration, `workItemId`,
`bySession`, `byUser`, `requestSha256`, top-level `noticeWakeId`, `seq`, and `ts`.
Named payload references such as `prior.activationId`, `noticedEventId`,
`replacesWakeId`, and `acknowledgedWakeId` remain caller inputs. Responses return exact
stored rows plus a derived state labelled `declared`, `attempted`,
`needs-reconciliation`, `withdrawn`, or `observed`. The derived state does not include
`authorized`, `ready`, `successful`, `settled`, `valid`, or `healthy`.

The gateway adds a `features` array to the existing `GET /version` response. The array is
sorted, contains unique closed strings, and includes `activation-events-v1` exactly when
the gateway serves this contract. The additive response field does not change
`protocolVersion: 1`. A current CLI treats a missing `features` field as an empty list. A
current CLI against a gateway without that feature reports
`capability_missing: activation-events-v1` before a domain adapter invokes an external
operation.

Requirement R-08a: the transport exposes the fixed verbs and rejects substrate-owned input
fields.  
Acceptance: A-25.

Requirement R-08b: the gateway advertises `activation-events-v1` exactly when it serves
this contract.  
Acceptance: A-26.

Requirement R-08c: an adapter invokes zero external actions when
`activation-events-v1` is absent.  
Acceptance: A-26.

### 9. Mandatory consumer mapping and optional sanity coverage

The mandatory table maps each Kung Fu's material to the same substrate fields. It does
not define domain policy.

| Field | Engineering Kung Fu: prepared build in production | Marketing Kung Fu: approved campaign in the field | Biosciences Kung Fu: approved experiment or instrument run on real samples |
| --- | --- | --- | --- |
| `preparedInput` | prepared build manifest or artifact digest | approved creative, audience-definition, and schedule bundle digest | approved protocol revision, real-sample-set reference, and reagent-lot plan digest |
| `target` | production service, cluster, and environment identity | field platform account and campaign identity | real-sample instrument and run-slot identity |
| `authority-attached` | Engineering-owned activation approval or change record | Marketing-owned brand, budget, and field approval record | Biosciences-owned PI, safety, facility, and real-sample approval records |
| `executor` | Engineering deploy manager or service identity | Marketing campaign publisher identity | Biosciences instrument controller or operator identity |
| `externalAttempt` | production activation generation or request ID | field publish request ID | real-sample instrument run request ID |
| `result` | Engineering-owned activation result code | Marketing/platform-owned field result code | Biosciences/instrument-owned run result code |
| `outputs` | active-generation and receipt references | campaign ID and field-platform receipt references | run ID and instrument-log references |
| Compensation | new activation linked with `compensates` | pause or withdrawal as a new activation when externally effectful | abort or cleanup as a new activation when externally effectful |

The example domain identities and codes remain owned by the respective Kung Fu. They do
not enter Tightbeam's table, column, event-kind, verb, state, capability, or error-code
vocabulary.

The three mandatory static design fixtures below are part of this spec artifact. Each code
block contains exactly one JSON line. Its pin hashes the UTF-8 bytes of that line followed
by one LF; the Markdown fence and marker comments are outside the hash. Each fixture carries
domain vocabulary only in fixture metadata and domain-owned payload values. Each expected
stream uses the same emitted substrate names.

Engineering static design fixture:

<!-- static-fixture:engineering:start -->
```json
{"consumer":"engineering-kung-fu","events":[{"eventId":"aev_fixture_eng_declared","kind":"declared","payload":{"correlationKey":"build-42-production","domain":"engineering","ownerUserId":"usr_engineering_owner","preparedInput":{"id":"build-42","namespace":"engineering.build","sha256":"1111111111111111111111111111111111111111111111111111111111111111"},"prior":null,"target":{"id":"service-a","namespace":"engineering.production","sha256":null}},"rootAssignmentId":"asg_fixture_eng"},{"actorAssignmentId":"asg_fixture_eng","eventId":"aev_fixture_eng_authority","kind":"authority-attached","payload":{"authorizer":{"id":"change-board","namespace":"engineering"},"basis":{"id":"change-42","namespace":"engineering.approval","sha256":"2222222222222222222222222222222222222222222222222222222222222222"},"decision":{"code":"approved","namespace":"engineering"}}},{"actorAssignmentId":"asg_fixture_eng","eventId":"aev_fixture_eng_attempted","kind":"attempted","noticeWakeId":"w_fixture_eng_attempted","payload":{"authorityEventIds":["aev_fixture_eng_authority"],"executor":{"id":"deploy-manager","namespace":"engineering"},"externalAttempt":{"id":"generation-42","namespace":"engineering.activation","sha256":null},"targetStateBefore":{"id":"generation-41","namespace":"engineering.production","sha256":"3333333333333333333333333333333333333333333333333333333333333333"}}},{"actorAssignmentId":"asg_fixture_eng","eventId":"aev_fixture_eng_observed","kind":"observed","noticeWakeId":"w_fixture_eng_observed","payload":{"attemptEventId":"aev_fixture_eng_attempted","certainty":"determinate","evidence":{"id":"receipt-42","namespace":"engineering.activation","sha256":"5555555555555555555555555555555555555555555555555555555555555555"},"externalOccurredAtMs":1786233600000,"outputs":[{"id":"generation-42","namespace":"engineering.production","sha256":null}],"result":{"code":"target-observed","namespace":"engineering"},"targetStateAfter":{"id":"generation-42","namespace":"engineering.production","sha256":"4444444444444444444444444444444444444444444444444444444444444444"}}},{"eventId":"aev_fixture_eng_ack_attempted","kind":"acknowledged","payload":{"acknowledgedWakeId":"w_fixture_eng_attempted","noticedEventId":"aev_fixture_eng_attempted"}},{"eventId":"aev_fixture_eng_ack_observed","kind":"acknowledged","payload":{"acknowledgedWakeId":"w_fixture_eng_observed","noticedEventId":"aev_fixture_eng_observed"}}],"fixtureKind":"static-design","policyOwner":"engineering-kung-fu","runtimeCapture":"pending-implementation","scenario":"prepared-build-production-activation"}
```
<!-- static-fixture:engineering:end -->

SHA-256: `5ade2056315401d6c0e3a1988969d0d842c348be8f50b4616dab7602e6c6a4f6`

Marketing static design fixture:

<!-- static-fixture:marketing:start -->
```json
{"consumer":"marketing-kung-fu","events":[{"eventId":"aev_fixture_mkt_declared","kind":"declared","payload":{"correlationKey":"campaign-73-field","domain":"marketing","ownerUserId":"usr_marketing_owner","preparedInput":{"id":"campaign-bundle-73","namespace":"marketing.campaign","sha256":"6666666666666666666666666666666666666666666666666666666666666666"},"prior":null,"target":{"id":"platform-account-9","namespace":"marketing.field","sha256":null}},"rootAssignmentId":"asg_fixture_mkt"},{"actorAssignmentId":"asg_fixture_mkt","eventId":"aev_fixture_mkt_authority","kind":"authority-attached","payload":{"authorizer":{"id":"brand-budget-owner","namespace":"marketing"},"basis":{"id":"campaign-approval-73","namespace":"marketing.approval","sha256":"7777777777777777777777777777777777777777777777777777777777777777"},"decision":{"code":"approved","namespace":"marketing"}}},{"actorAssignmentId":"asg_fixture_mkt","eventId":"aev_fixture_mkt_attempted","kind":"attempted","noticeWakeId":"w_fixture_mkt_attempted","payload":{"authorityEventIds":["aev_fixture_mkt_authority"],"executor":{"id":"campaign-publisher","namespace":"marketing"},"externalAttempt":{"id":"publish-73","namespace":"marketing.platform","sha256":null},"targetStateBefore":{"id":"campaign-73-draft","namespace":"marketing.field","sha256":"8888888888888888888888888888888888888888888888888888888888888888"}}},{"actorAssignmentId":"asg_fixture_mkt","eventId":"aev_fixture_mkt_observed","kind":"observed","noticeWakeId":"w_fixture_mkt_observed","payload":{"attemptEventId":"aev_fixture_mkt_attempted","certainty":"determinate","evidence":{"id":"platform-receipt-73","namespace":"marketing.platform","sha256":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"},"externalOccurredAtMs":1786233600000,"outputs":[{"id":"campaign-73-live","namespace":"marketing.field","sha256":null}],"result":{"code":"field-observed","namespace":"marketing"},"targetStateAfter":{"id":"campaign-73-live","namespace":"marketing.field","sha256":"9999999999999999999999999999999999999999999999999999999999999999"}}},{"eventId":"aev_fixture_mkt_ack_attempted","kind":"acknowledged","payload":{"acknowledgedWakeId":"w_fixture_mkt_attempted","noticedEventId":"aev_fixture_mkt_attempted"}},{"eventId":"aev_fixture_mkt_ack_observed","kind":"acknowledged","payload":{"acknowledgedWakeId":"w_fixture_mkt_observed","noticedEventId":"aev_fixture_mkt_observed"}}],"fixtureKind":"static-design","policyOwner":"marketing-kung-fu","runtimeCapture":"pending-implementation","scenario":"approved-campaign-field-launch"}
```
<!-- static-fixture:marketing:end -->

SHA-256: `6408cd99b703cd4048697b9a9568e92aefe2657fe0dcdda5b9efe7927f2a6dc5`

Biosciences static design fixture:

<!-- static-fixture:biosciences:start -->
```json
{"consumer":"biosciences-kung-fu","events":[{"eventId":"aev_fixture_bio_declared","kind":"declared","payload":{"correlationKey":"experiment-run-18","domain":"biosciences","ownerUserId":"usr_biosciences_owner","preparedInput":{"id":"protocol-sample-set-18","namespace":"biosciences.protocol","sha256":"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},"prior":null,"target":{"id":"instrument-4-slot-18","namespace":"biosciences.instrument","sha256":null}},"rootAssignmentId":"asg_fixture_bio"},{"actorAssignmentId":"asg_fixture_bio","eventId":"aev_fixture_bio_authority","kind":"authority-attached","payload":{"authorizer":{"id":"pi-safety-facility","namespace":"biosciences"},"basis":{"id":"run-approval-18","namespace":"biosciences.approval","sha256":"cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"},"decision":{"code":"approved","namespace":"biosciences"}}},{"actorAssignmentId":"asg_fixture_bio","eventId":"aev_fixture_bio_attempted","kind":"attempted","noticeWakeId":"w_fixture_bio_attempted","payload":{"authorityEventIds":["aev_fixture_bio_authority"],"executor":{"id":"instrument-controller-4","namespace":"biosciences"},"externalAttempt":{"id":"run-request-18","namespace":"biosciences.instrument","sha256":null},"targetStateBefore":{"id":"instrument-4-ready","namespace":"biosciences.instrument","sha256":"dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd"}}},{"actorAssignmentId":"asg_fixture_bio","eventId":"aev_fixture_bio_observed","kind":"observed","noticeWakeId":"w_fixture_bio_observed","payload":{"attemptEventId":"aev_fixture_bio_attempted","certainty":"determinate","evidence":{"id":"instrument-log-18","namespace":"biosciences.instrument","sha256":"ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"},"externalOccurredAtMs":1786233600000,"outputs":[{"id":"run-18","namespace":"biosciences.instrument","sha256":null}],"result":{"code":"run-observed","namespace":"biosciences"},"targetStateAfter":{"id":"instrument-4-run-18","namespace":"biosciences.instrument","sha256":"eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"}}},{"eventId":"aev_fixture_bio_ack_attempted","kind":"acknowledged","payload":{"acknowledgedWakeId":"w_fixture_bio_attempted","noticedEventId":"aev_fixture_bio_attempted"}},{"eventId":"aev_fixture_bio_ack_observed","kind":"acknowledged","payload":{"acknowledgedWakeId":"w_fixture_bio_observed","noticedEventId":"aev_fixture_bio_observed"}}],"fixtureKind":"static-design","policyOwner":"biosciences-kung-fu","runtimeCapture":"pending-implementation","scenario":"approved-experiment-instrument-run-real-samples"}
```
<!-- static-fixture:biosciences:end -->

SHA-256: `8def2b1ac502bfde66c69b70e05f2284e24e14dddbecb3ee832f46b6e03e9053`

Finance transaction execution is an optional fourth mapping:

| Field | Optional Finance sanity mapping |
| --- | --- |
| `preparedInput` | signed instruction or transaction-batch digest |
| `target` | rail, account, and instruction endpoint identity |
| `authority-attached` | Finance-owned approval or control records |
| `executor` | payment or ledger execution service identity |
| `externalAttempt` | transaction idempotency or instruction ID |
| `result` | Finance/rail-owned result code |
| `outputs` | acceptance, settlement, or rejection receipt references |
| Compensation | reversal or cancel instruction as a new activation when externally effectful |

Requirement R-09a: the design self-gate recomputes each mandatory static fixture SHA-256,
parses its JSON, validates each expected event payload against the closed section 3 shape,
validates the expected row-owned identifiers against their named section 2 fields, and
confirms that its emitted substrate names belong to the section 12 manifest. Domain
vocabulary appears only in consumer documentation, fixture metadata, and domain-owned
payload values.  
Acceptance: A-27, A-28, A-29, and A-34.

Requirement R-09b: the publication gate labels Finance as optional and does not use its
result to replace a mandatory fixture result.  
Acceptance: A-30 and A-34.

Requirement R-09c: before an implementation can pass a mandatory consumer runtime gate,
that consumer's immutable runtime activation fixture proves this strict order: the
`attempted` row and notice wake commit; the adapter receives that committed event response;
then the adapter invokes the first external mutation with the same `externalAttempt.id`.
The capture records zero mutation invocations before the response and one first invocation
after it. The gate rejects a mutation-before-attempt mutant. The same fixture suite proves
that a lost committed response replays to the original event before any mutation, and that
recovery after a mutation but before observation invokes zero additional mutations and
observes the original attempt.  
Acceptance: A-19, A-20, A-27, A-28, A-29, and A-34.

### 10. Compatibility and migration

`activation_events` is a new additive table with new indexes and foreign keys. The change
does not alter an existing table or reinterpret an existing row. The schema bootstrap
creates the table on a compatible stamped database. An older gateway ignores the table.
An adopting domain adapter refuses before external mutation when the gateway lacks
`activation-events-v1` in `GET /version.features`.

Existing deploy attests, artifacts, wakes, and report `art_487c6afe` remain historical
evidence. No migration translates them into activation events because translation would
invent input, target, authority, attempt ordering, observation, and acknowledgement facts
that were not mechanically present.

The Engineering consumer replaces the proposed names as follows:

```text
production_deploy_facts          -> activation_events
deploy-intent                    -> activation-declare
deploy-authorize                 -> activation-authority
deploy-begin                     -> activation-attempt
deploy-finish                    -> activation-observe or activation-reconcile
deploy-ack                       -> activation-ack
rollback mode                    -> new activation with relation compensates
environment=production           -> Engineering-owned target identity and policy
work-item-owner/admin authority  -> Engineering-owned authorizer/basis evaluation
deploy completion gate           -> optional Engineering rule over activation queries
```

Requirement R-10a: upgrade creates the additive activation table while keeping prior rows
byte-stable.  
Acceptance: A-31.

Requirement R-10b: upgrade creates zero activation events from historical rows.  
Acceptance: A-31.

Requirement R-10c: an older otherwise-compatible binary retains its existing behavior in
the presence of the additive table.  
Acceptance: A-32.

### 11. Observability

Accepted and denied activation verbs use the existing event log with redacted metadata.
Wake delivery failures use existing lifecycle-event recording keyed by wake ID. Protected
status reads return stream rows ordered by `(seq, eventId)` and include pending/fired/
canceled notice state and acknowledgement linkage.

`work-item-trace` adds redacted activation summaries for authorized trace readers. It does
not merge activation state into assignment outcome or work-item state. Operational queries
can count unresolved attempts, indeterminate observations, irrecoverable reconciliations,
pending notices, canceled notices, and unacknowledged fired notices without reading domain
payloads.

Requirement R-11: operators can locate unresolved and undelivered activation records from
durable rows without parsing prose or domain payloads.  
Acceptance: A-33.

### 12. Publication self-gate

This block is the canonical emitted machine-vocabulary manifest for v1. A spec amendment is
required before an implementation adds another externally emitted name in one of the gated
categories.

<!-- machine-vocabulary:start -->
```text
table:
activation_events

columns:
seq eventId activationId kind predecessorEventId rootAssignmentId workItemId
actorAssignmentId bySession byUser idempotencyKey requestSha256 payload noticeWakeId ts

event-kinds:
declared authority-attached attempted observed reconciled withdrawn notice-requeued acknowledged

payload-keys-and-values:
ownerUserId domain correlationKey preparedInput target prior relation retry-of compensates
supersedes authorizer basis decision authorityEventIds executor externalAttempt
targetStateBefore attemptEventId certainty determinate indeterminate result targetStateAfter
outputs evidence externalOccurredAtMs observedEventId irrecoverable reason noticedEventId
acknowledgedWakeId replacesWakeId namespace id sha256 code

new-wire-fields:
features

derived-states:
declared attempted needs-reconciliation withdrawn observed

capability:
activation-events-v1

verbs:
activation-declare activation-authority activation-attempt activation-observe
activation-reconcile activation-withdraw activation-renotify activation-ack activation-status
activations

error-codes:
invalid_activation_payload not_found activation_head_changed activation_transition_refused
activation_assignment_refused activation_owner_refused activation_relation_refused
activation_authority_refused activation_notice_refused invalid_idempotency_key
idempotency_conflict capability_missing
```
<!-- machine-vocabulary:end -->

The design artifact fails publication when one of the static gates below fails. An
implementation fails release when a static gate fails or any mandatory runtime gate is not
`PASS`.

1. **Mandatory static-fixture gate.** Recompute the three exact section 9 fixture hashes and
   require the recorded SHA-256 values. Parse each JSON line. Engineering, Marketing, and
   Biosciences must each carry declaration, authority, attempt, determinate observation,
   attempt and observation notice IDs, and two acknowledgements through the section 3
   shapes. A fixture fails if its hash differs, JSON is invalid, a required shape is absent,
   or it needs a new column, event kind, derived state, capability, error code, or verb.
2. **Machine-vocabulary gate.** For each table name, column name, payload key and closed
   payload value, event kind, derived state, capability name, new wire field, wire/CLI verb,
   and error code, insert a token boundary before an ASCII uppercase letter that follows a
   lowercase letter or digit, lowercase the result, and split on each non-letter. None of
   the resulting tokens equals:
   `engineering`, `build`, `production`, `deploy`, `release`, `rollback`, `marketing`,
   `campaign`, `field`, `bioscience`, `biosciences`, `experiment`, `instrument`, `sample`,
   `finance`, `financial`, `transaction`, `payment`, or `settlement`. Consumer docs,
   mappings, fixtures, and domain-owned payload values are outside this lexical check.
3. **Sibling-fact gate.** The activation semantic store contains exactly one table,
   `activation_events`. A proposal for a deploy, campaign, experiment, instrument-run,
   sample-run, finance, or transaction sibling fact fails even when it claims to reuse the
   generic stream elsewhere.
4. **Policy-boundary gate.** Substrate handlers limit their decisions to I-1. A handler,
   rule, constraint, or derived state that interprets a domain code, selects a sufficient
   authorizer, evaluates readiness, or decides business success fails.

Each mandatory consumer also has one **implementation runtime gate**. It is `PASS` only
when an immutable `Runtime activation fixture` with an artifact ID and recorded SHA-256
satisfies R-09c and the matching A-27, A-28, or A-29. A static design fixture, hand-written
response, mock-only transcript, or stated intention cannot make this gate pass. Until an
implementation supplies that artifact, the runtime result is `PENDING IMPLEMENTATION`.
This evidence-only design can publish its static fixture results but cannot claim a real
gateway, wake, adapter-ordering, or external-target capture pass.

Finance may exercise the same gates as optional additional evidence. A Finance pass does
not replace an Engineering, Marketing, or Biosciences pass.

#### Publication gate record — 2026-08-09 UTC

- Engineering static fixture: **PASS** — exact SHA-256
  `5ade2056315401d6c0e3a1988969d0d842c348be8f50b4616dab7602e6c6a4f6`; the expected
  stream completes the closed lifecycle without a new substrate name. Real capture proof:
  **PENDING IMPLEMENTATION**.
- Marketing static fixture: **PASS** — exact SHA-256
  `6408cd99b703cd4048697b9a9568e92aefe2657fe0dcdda5b9efe7927f2a6dc5`; the expected
  stream completes the same lifecycle without a new substrate name. Real capture proof:
  **PENDING IMPLEMENTATION**.
- Biosciences static fixture: **PASS** — exact SHA-256
  `8def2b1ac502bfde66c69b70e05f2284e24e14dddbecb3ee832f46b6e03e9053`; the expected
  stream completes the same lifecycle without a new substrate name or sample content.
  Real capture proof: **PENDING IMPLEMENTATION**.
- Machine vocabulary: **PASS** — the canonical manifest contains no forbidden domain token;
  the `productionTarget`, `campaign-launched`, `bioscience-experiment`, and
  `production_deploy_facts` negative fixtures each fail the token gate.
- Sibling fact: **PASS** — the manifest contains exactly one semantic table,
  `activation_events`; a second-table mutant fails the count gate.
- Policy boundary: **PASS** — the canonical derived states contain no authorization,
  readiness, or business-outcome state; an added `authorized` state fails the closed-state
  check. Event shapes preserve domain codes without interpreting sufficiency or meaning.
- Finance sanity coverage: **OPTIONAL** — A-30 remains outside the mandatory result set and
  cannot replace a mandatory pass.
- Structural supplement: **PASS** — the spec contains eight canonical sections; A-01
  through A-34 each trace from Architecture; declaration idempotency includes the root
  assignment; successor admission discloses no prior payload and grants no read, domain, or
  write authority; owner relation, transfer terminalization, and acknowledgement-field
  separation checks pass.

Requirement R-12a: design publication runs the four static gates and records a pass/fail
result with fixture SHA-256 for each mandatory static fixture, plus machine vocabulary,
sibling-fact count, and policy boundary.  
Acceptance: A-34.

Requirement R-12b: implementation release records a separate runtime result for each
mandatory consumer and refuses a release pass until all three results cite immutable
runtime activation fixtures that satisfy R-09c. Before implementation, each result is
`PENDING IMPLEMENTATION`, not `PASS` or `FAIL`.  
Acceptance: A-27, A-28, A-29, and A-34.

### 13. Subtraction and enforcement rung

**ADD chosen:** one neutral append-only stream closes a shared, mechanically observable
gap across the three mandatory consumers; deleting the activation surface leaves external
actions without typed durable provenance, while accepting the failure contradicts the work
item's explicit papertrail goal and forces each consumer to duplicate it.

**ADD chosen for notice requeue:** a linked replacement is required only after an operator
cancels a wake; deleting it makes a canceled notice permanently unacknowledgeable, while
accepting that permanent failure breaks the goal's durable owner-notice and acknowledgement
chain.

**DELETE chosen for the prior proposal:** delete the proposed deploy-specific table, verbs,
production enum, owner/admin deploy authority, rollback mode, and substrate completion gate
from the implementation plan; `art_487c6afe` remains evidence for the Engineering mapping.

**ACCEPT chosen for universal enforcement:** a domain path without an adopted mutation seam
is recorded as not mechanically gated. Tightbeam does not infer or claim coverage from shell
commands, time thresholds, repository topology, or prose.

**DELETE chosen for unsupported real-capture passes:** the evidence-only design publishes
SHA-pinned static design fixtures and labels each real capture `PENDING IMPLEMENTATION`.
Accepting a real-capture pass without an immutable runtime artifact would make the evidence
claim false; deleting static fixtures would remove the design's reproducible cross-domain
self-gate.

**ADD chosen for the successor bridge:** one declaration admission check uses the existing
new-root assignment and work-item relations without adding an event, verb, or read role.
Deleting transfer support makes the required successor inexpressible; a broader prior-stream
read loses because transfer admission needs no predecessor disclosure.

The affordable rung is a typed table plus closed wire verbs, relational constraints,
idempotent CAS appends, protected reads, and consumer-owned source guards at each adopted
mutation seam. Guidance alone is insufficient because the event, caller, and action leave
machine-readable rows. A global shell rail is defective because it cannot identify the
domain event without false positives.

## Acceptance

**A-01 — one primitive.** Given a fresh schema, when the table and wire vocabularies are
listed, then one `activation_events` table and one activation verb family exist, and no
`production_deploy_facts` table or `deploy-*` verb exists.

**A-02 — principal and cause.** Given a declaration by holder session S with root assignment
R and a later event after head E, when each call succeeds, then the declaration's canonical
request digest includes R, the rows store S as the derived principal, the later row stores E
as predecessor, and caller-supplied principal or timestamp fields refuse.

**A-03 — head CAS.** Given concurrent appends after the same head, when both transactions
run, then one wins and the other returns `activation_head_changed` with the winning head;
the stream contains one successor.

**A-04 — byte-identical replay.** Given one accepted event, when the same principal reuses
its key with the same canonical semantic request, including the same `rootAssignmentId` for
a declaration, after later stream events and after the acting assignment or work item
becomes terminal, then the original event and wake IDs return before current head,
lifecycle, or assignment checks and row counts stay unchanged.

**A-05 — changed replay.** Given one accepted declaration, when the same principal and key
carry the same payload but a different `rootAssignmentId`, then the call refuses
`idempotency_conflict` and row counts stay unchanged. The same refusal applies when any
other canonical semantic request byte changes.

**A-06 — closed schemas.** Given each event verb, when one required key is missing, one
unknown key is present, one field has the wrong type, an opaque token contains whitespace
or a control character, one bound is exceeded, or a required evidence digest is null, then
the call refuses before an event or wake row exists.

**A-07 — declaration accountability.** Given an open assignment on an open work item, when
its holder declares an activation, then work-item identity is derived and stored. Given a
non-holder, closed assignment, unlinked assignment, or terminal work item, the declaration
refuses without rows. Given an otherwise valid declaration whose `ownerUserId` is neither
the work-item owner nor the holder session's owning user, the declaration refuses
`activation_owner_refused` without rows or newly granted read access.

**A-08 — neutral authority.** Given two authority events with different domain identities,
bases, and decision codes, when a domain adapter selects both for an attempt, then Tightbeam
verifies their membership and records the set without deciding quorum or meaning. Given an
unrelated user who knows the activation ID but has no read relation, an authority append
returns `not_found`, creates no row, and does not grant that user later read access.

**A-09 — authority membership.** Given an authority event from another activation, an
unknown event, a duplicate ID, or an event list outside ascending stream sequence, when the
list is supplied to an attempt, then the call refuses with no partial write. Given an
attempted activation, when a caller attaches another authority event, then that append also
refuses with no partial write.

**A-10 — one attempt.** Given one attempted event, when another non-replay attempt is filed
for that activation, then it refuses and the caller must declare a `retry-of` activation.

**A-11 — observation shapes.** Given an attempted activation, when a recovery principal
records each certainty with a bounded domain code, content-bound evidence and target-state
references, outputs, and occurrence time, then the stored bytes round-trip exactly and
derived state follows the lifecycle without interpreting the result code.

**A-12 — explicit acknowledgement.** Given a noticed event, when a non-owner, unrelated
wake, pending wake, canceled wake, or duplicate acknowledgement is supplied, then
acknowledgement refuses. When the owner acknowledges the fired original wake or a fired
replacement linked through `notice-requeued`, one acknowledgement row exists for the
noticed event.

**A-13 — withdrawal.** Given a declared activation with no attempt, when its work-item owner
or a holder of an open related assignment withdraws it, then the stream becomes terminal and
one owner wake exists. Given an attempted activation, withdrawal refuses.

**A-14 — indeterminate recovery.** Given an attempted activation and an indeterminate
observation, when status is read, then it reports `needs-reconciliation`. A determinate or
irrecoverable reconciliation makes it terminal while retaining the indeterminate row.

**A-15 — invalid reconciliation.** Given a determinate observation, no observation, another
activation's observation, or a prior reconciliation, when reconciliation is requested, then
it refuses with no row.

**A-16 — transfer and stale authority.** Given an unattempted activation under owner/basis
snapshot O1, when the domain transfers responsibility to O2, then the adapter first
withdraws O1; afterward an O2-owned session holds the new root assignment and declares a
`supersedes` activation naming O2 with new authority events. When O2 has no read relation to
O1, the successor bridge admits the declaration only because O1 is terminal and both roots
belong to the same work item. The response exposes no O1 payload; status and list still hide
O1; no O1 read, domain authority, or later-write authority is created. O2's held new root
assignment remains the declaration authority. A non-terminal O1, different work item, or
root not held by O2 returns `not_found` without a row. An O1 attempt after withdrawal
refuses, and O1 authority IDs cannot be used by the successor.

**A-17 — atomic notice outbox.** Given injected failure before event insert, between event
and wake insert, and at transaction commit, when a noticed event is appended, then event and
wake counts show both rows or neither. A successful row stores the exact wake ID.

**A-18 — delivery semantics and requeue.** Given a delivery exception, crash after delivery,
normal delivery, and operator cancellation, when the wake scheduler recovers, then pending
wakes retry, turn enqueue deduplicates by wake ID, and only explicit owner action creates
acknowledgement. An authorized requeue of the canceled wake atomically appends one
`notice-requeued` event and one replacement wake; a second requeue of the same canceled wake
refuses without rows. An unrelated caller, a pending or fired wake, an unrelated canceled
wake, and an already acknowledged noticed event each refuse requeue without rows.

**A-19 — crash before attempt response.** Given an `attempted` row and notice wake that
commit but whose response is lost before the adapter receives it, when recovery replays the
same key and canonical request, then Tightbeam returns the original event and wake IDs. The
mutation spy records zero calls before that replay response. The adapter then invokes the
external mutation once with the original `externalAttempt.id`; another exact replay appends
no row and invokes no additional mutation.

**A-20 — crash around external mutation.** Given kills after the committed attempt response
but before mutation, immediately after the external mutation, and immediately before the
observed append, when recovery runs, then the first case reuses the committed attempt and
invokes one first mutation; the latter two cases read external truth, invoke zero additional
mutations, and record one observation against the original attempt. Recovery appends no
automatic attempt and does not reopen a terminal assignment or work item.

**A-21 — unresolved external truth.** Given a source that cannot determine whether an
effect occurred, when recovery records `indeterminate`, then no timeout rewrites it. A later
recovery principal records one reconciliation or leaves the state unresolved; the
external-operation spy records zero mutation calls in either case.

**A-22 — deploy recast.** Given the exact Engineering facts proposed in `art_487c6afe`, when
mapped to v1, then declaration, authority, attempt, observation, compensation, notice, and
acknowledgement use activation verbs only; production scope and authority sufficiency stay
in the Engineering adapter/rule.

**A-23 — protected reads.** Given an activation visible to its owner, work-item owner,
named assignment holder, filer, and admin, plus an unrelated user, when each calls status and
list, then related principals receive the permitted stream and the unrelated user receives
`not_found` or an omitted list row with no count leak. A non-replay append by the unrelated
user also returns `not_found`; the rejected filer does not become a reader. Given a
successful successor-bridge declaration by a new holder without a prior-stream read
relation, that holder can read the new activation while status and list still hide the prior
activation. The bridge alone does not make any principal a prior-stream reader or writer.

**A-24 — payload leak check.** Given distinctive resource IDs, domain identities, result
codes, and evidence refs, when event logs, trace summaries, wake prompts, and denial rows are
read, then none contains those distinctive bytes; protected activation status does.

**A-25 — wire ownership.** Given wire requests that supply `eventId`, derived principal,
work item, digest, top-level `noticeWakeId`, sequence, or timestamp, when each reaches the
router, then the router rejects the substrate-owned field and the handler receives none of
it. The named `replacesWakeId` and `acknowledgedWakeId` payload references remain accepted
inputs to their fixed verbs.

**A-26 — capability refusal.** Given a current adapter against (a) a current gateway whose
`GET /version.features` omits `activation-events-v1` and (b) an older gateway whose version
response has no `features` field, when the adapter reaches its pre-mutation boundary, then
both cases refuse with the named missing capability and the external-operation spy records
zero calls. A gateway that serves v1 advertises the feature exactly once in its sorted list.

**A-27 — mandatory Engineering Kung Fu example.** Given the exact Engineering static design
fixture in section 9, when the self-gate hashes and parses it, then its SHA-256 equals
`5ade2056315401d6c0e3a1988969d0d842c348be8f50b4616dab7602e6c6a4f6`, its expected
stream contains declaration, authority, attempt, determinate observation, two notices, and
two acknowledgements, and it needs no Engineering substrate name or policy decision. Its
real gateway, wake, adapter-ordering, and production-target capture remains `PENDING
IMPLEMENTATION` until one SHA-recorded runtime artifact proves R-09c.

**A-28 — mandatory Marketing Kung Fu example.** Given the exact Marketing static design
fixture in section 9, when the self-gate hashes and parses it, then its SHA-256 equals
`6408cd99b703cd4048697b9a9568e92aefe2657fe0dcdda5b9efe7927f2a6dc5`, its expected
stream contains declaration, authority, attempt, determinate observation, two notices, and
two acknowledgements, and it needs no Marketing substrate name or policy decision. Its real
gateway, wake, adapter-ordering, and field-platform capture remains `PENDING IMPLEMENTATION`
until one SHA-recorded runtime artifact proves R-09c.

**A-29 — mandatory Biosciences Kung Fu example.** Given the exact Biosciences static design
fixture in section 9, when the self-gate hashes and parses it, then its SHA-256 equals
`8def2b1ac502bfde66c69b70e05f2284e24e14dddbecb3ee832f46b6e03e9053`, its expected
stream contains declaration, authority, attempt, determinate observation, two notices, and
two acknowledgements, and it needs no Biosciences substrate name or policy decision. The
fixture contains opaque sample references and no sample content. Its real gateway, wake,
adapter-ordering, and instrument-target capture remains `PENDING IMPLEMENTATION` until one
SHA-recorded protected runtime artifact proves R-09c.

**A-30 — optional Finance sanity example.** Given a provider sandbox and a non-value-moving
test instruction, when the Finance adapter uses its real authority references, idempotency
ID, provider response, and receipt, then captured responses replay through the same schema
and Tightbeam does not map the domain result to settled or successful. A failure here is a
sanity finding; it does not replace or relax A-27, A-28, or A-29.

**A-31 — additive upgrade.** Given a compatible stamped database from the prior build,
when the new gateway boots, then it creates the activation table and indexes without
altering old table bytes or synthesizing activation events. Existing non-activation client
journeys still pass when `GET /version` contains the additive `features` field.

**A-32 — downgrade boundary.** Given activation rows written by a current gateway, when an
older binary opens the same otherwise-compatible database, then existing behavior remains
readable and the adopting adapter still refuses because the older gateway does not advertise
the capability.

**A-33 — operator query.** Given one unresolved attempt, one indeterminate observation, one
pending notice, one canceled notice, and one fired-unacknowledged notice, when protected
status and redacted work-item trace are queried, then each condition is mechanically
distinguishable without parsing notes, prompts, or domain result codes.

**A-34 — publication self-gate.** Given (a) the generic v1 design, (b) a candidate with a
`productionTarget` payload key or column, (c) a candidate with a `campaign-launched` event
kind, (d) a candidate with a `bioscience-experiment` verb, (e) a candidate with a sibling
`production_deploy_facts` table, and (f) a candidate that treats one domain decision code as
authorized, when the section 12 static gates run, then only (a) passes. Changing one byte in
any mandatory fixture also fails its recorded SHA. The report records separate static
fixture passes for Engineering, Marketing, and Biosciences and labels Finance optional.
Given an implementation candidate whose trace mutates before the committed attempt response,
when the runtime gate runs the ordered proof and mutation-before-attempt mutant, then the
candidate fails. A candidate without the required real artifact remains `PENDING
IMPLEMENTATION`; the crash-before-response replay and crash-after-mutation recovery cases
must also satisfy A-19 and A-20 before a runtime pass.

## Open Questions

None. This spec has no blocking or non-blocking open question. Domain-specific readiness,
authorization, result, retry, compensation, transfer, and compliance decisions are inputs
to consumer adapters rather than holes in the substrate contract.
