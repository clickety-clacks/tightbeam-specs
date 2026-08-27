# Terminal operator-decision parity and integrity — v1

Status: DRAFT, TARGETLESS

Authority: work item `wi_435301fa-dead-4a1a-8e78-4a594c0f8b0d`, assignment
`asg_edf0c74c-65e3-4668-a208-002765c7304b`, diagnosed verdicts
`att_e7e215c9-a2de-461e-a593-cc96206baee2` and
`att_ef216f06-290b-4bd5-a879-c32695c4493d`, and their evidence artifacts
`art_cd0baef7`, `art_c8452adf`, and `art_c72f1895`.

Source evidence: Tightbeam `main` commit
`ffcb715b34ffd33cd5ae4e27d03a9d515a8f4fad`, the frozen 0.1.8 source commit
`2ff4ed2a93527f1a7eeb56f2b9a8c52f10368ab5`,
`escalation-substrate-v1.md`, `escalation-delivery-v1.md`,
`decision-request-client-observable-state-v1.md`,
`decision-request-expecter-preference-v1.md`, and visitor-attribution spec
`visitor-principal-v3.md` at commit
`9fed0adef203904ef44e9252cd0c5b4b8f6c6a70` and file SHA-256
`03fe3dd2d6f93537a5477d3037c1ff79b484f8810c33790391aa6c6cc76cf015`.
These source revisions are evidence pins, not implementation targets.

This contract supersedes only the owner-scoped operator-request read projection,
terminal-attribution, integrity, and raiser-delivery clauses of
`escalation-substrate-v1.md` and any candidate client projection that omits the
fields named here. It preserves that spec's decision authority, open-row
compare-and-set, transaction, visibility, authorization, privacy, and targetless
status. A selected implementation target shall amend the applicable CLI and wire
surface specs before it ships this contract. This spec does not elect that target
or bind a `specRef`.

## Goal

After a caller passes the existing visibility check for an owner-scoped operator
decision request, `decision-requests` and an exact-id `decision-request` read
shall expose the same complete terminal decision. The shared terminal projection
shall include the request identity, selected outcome, explicit rationale value,
accountable owner and on-behalf-of actor, performing principal and presenting
session, ruling time and fact, and lifecycle and consumption state. The request
kind shall not remove any terminal field.

Add the supported exact-id CLI read. A terminal row that cannot satisfy the
closed ruled shape shall produce a named integrity refusal and one durable,
privacy-safe evidence record before Tightbeam emits any part of that request or
consumes its outcome. Tightbeam shall not repair, reinterpret, or invent history.
A complete legacy ruling that lacks performer provenance shall project the
closed value `legacy-unknown`.

The winning ruling transaction shall also arm one automatic notification to the
recorded raiser through the existing wake and condition-fact path. That wake
shall observe the same `escalation-ruled` fact that closes the request. Ruling
replay and concurrent losers shall not create another notification. Manual
intermediary wakes remain an operational mitigation; they are not correctness
evidence and do not suppress the automatic notification.

Subtraction ruling: ADD wins because deleting list or exact-id reads would break
the durable owner-decision workflow, and accepting a lossy or impossible ruled
projection would discard the decision the workflow exists to preserve. The
addition reuses the existing request row, open-row compare-and-set, condition
fact, wake outbox, and lifecycle transaction. It adds one shared projection,
one integrity-evidence relation, and one CLI affordance; it adds no adjudicator,
hold state, polling loop, target selector, or second delivery channel. This is
wisdom 1, 5, 6, 8, 9, and 10: rails follow the decision rows, every marker names
cause and principal, and the substrate routes and verifies facts without
deciding the answer.

## Non-Goals

- This contract does not implement, merge, land, release, deploy, or backport
  source. It does not select a branch, release line, host, or credential.
- This contract does not act on the frozen 0.1.8 line. That revision is defect
  evidence only.
- This contract does not elect a target or attach this spec to a work item as a
  live `specRef`.
- This contract does not add an operator, intermediary, visitor, or agent as a
  decision authority. Existing owner/admin authorization remains the sole
  authority boundary.
- This contract does not give a visitor principal operator-decision authority.
  `visitor-principal-v3.md` continues to exclude that authority.
- This contract does not change which requests a caller can discover or read.
  It does not weaken hidden-row and absent-row indistinguishability.
- This contract does not change a request question, option set, context,
  accountable owner, raiser, assignment link, deadline, or action identity.
- This contract does not change open-row compare-and-set semantics, withdrawal,
  supersession, statute ruling, effort ruling, agent answer/return, or the
  policy that consumes an applicable decision.
- This contract does not require `rationale` to be non-null. It requires the
  field to be present. Existing authority decides whether a ruling may omit
  rationale.
- This contract does not infer a legacy performer from `ownerUserId`,
  `ruledBy`, `raiserId`, lifecycle prose, a current session, a broker, an
  expecter, or an intermediary wake.
- This contract does not rewrite a historical request, condition fact,
  lifecycle event, wake, turn, or attribution field.
- This contract does not promise exactly-once socket delivery or agent
  attention. It promises at most one durable automatic prompt turn for the
  ruling wake under the existing wake delivery contract.
- This contract does not treat a fallback time as evidence that a ruling
  happened. Only the canonical condition fact represents that event.
- This contract does not add a second condition kind or accept an alias for
  `escalation-ruled`.
- This contract does not make the shared serializer an authorization source.
- This contract does not add target selection, live-state repair, historical
  mutation, self-review, or a producer review verdict.

## Terms

- **Operator decision request**: one durable, owner-scoped enumerated decision
  request created through `operator-ask` or the target-equivalent owner-decision
  create verb. Its canonical kind is `operator`. If a selected target uses a
  different stored kind, its migration shall map that one kind to `operator` at
  the read boundary without changing historical rows.
- **Request identity**: the immutable tuple `id`, `kind`, `question`, `options`,
  `raiserId`, `raiserSessionKey`, `ownerUserId`, `assignmentId`, `raisedAt`, and
  `deadlineAt`. `context` and `actionKey` remain direct-read detail and are not
  parity fields.
- **Visible request**: a request admitted by the existing list or direct-read
  visibility predicate for the authenticated caller. Authorization and privacy
  checks happen before integrity inspection or projection.
- **Exact-id read**: `decision-request` with one complete canonical `dr_...` id.
  It performs no prefix, substring, display-label, or target resolution.
- **Terminal decision projection**: the field set in Architecture §1. List and
  exact-id reads use one implementation seam to construct this set.
- **On-behalf-of actor**: the accountable user represented as
  `user:<ownerUserId>` whose existing authority permits the operator ruling.
  The compatibility field `ruledBy` retains this value.
- **Performing principal**: the canonical principal authenticated for the
  winning ruling call. It is not derived from the owner, raiser, role alias,
  origin string, broker, or session display name.
- **Presenting session**: the authenticated Tightbeam session that transported
  the winning ruling, when one existed. It is separate from the performing
  principal because a session can present a call attributed to an authorized
  user.
- **Ruling attribution**: the closed `rulingAttribution` value in Architecture
  §1. It keeps the on-behalf-of actor, performing principal, and presenting
  session distinct.
- **Legacy-complete ruling**: a pre-migration terminal operator row whose
  request identity, owner, decision, time, fact, and lifecycle shape are valid,
  but whose stored fields cannot prove the performing principal or presenting
  session.
- **Legacy unknown**: the literal state `legacy-unknown`. It records absence of
  historical proof. It is not a guess, null synonym, wildcard, repair request,
  or authorization value.
- **Impossible ruled shape**: a visible row whose status claims `ruled` or
  `consumed` but fails one or more checks in Architecture §2. A legacy-complete
  ruling is not impossible.
- **Canonical ruling fact**: one durable condition fact with kind exactly
  `escalation-ruled`, scope exactly the decision request id, and id exactly
  `rulingFactId`.
- **Raiser notification wake**: one durable prompt wake addressed to the
  request's recorded `raiserSessionKey`, armed for condition kind
  `escalation-ruled` and scope equal to the request id.
- **Durable delivery**: one committed prompt message/turn associated with the
  raiser notification wake under the existing wake outbox and wake-state
  compare-and-set. It does not mean one network publication or one inference
  response.
- **Integrity evidence**: one durable diagnostic row keyed by the request id
  and the immutable ruled-shape digest. It records that Tightbeam refused an
  admitted serialization or consumption. It is observability, not authority.
- **Manual intermediary wake**: a person- or agent-filed wake used to tell the
  raiser about a ruling while the automatic path is absent or defective. It is
  mitigation only.

## Assumptions

1. `escalation-substrate-v1.md` remains authoritative for request creation,
   owner/admin authorization, visibility, open-row compare-and-set, the atomic
   ruling row/fact/event write, and downstream consumption except where this
   contract narrows its read and delivery clauses.
2. `escalation-delivery-v1.md` remains authoritative for transactional wake
   creation, the durable outbox, wake-state compare-and-set, and one committed
   prompt turn per wake.
3. A selected target has, or will add before this contract, the owner-scoped
   operator request kind and owner ruling verb. The target owner shall prove
   that dependency rather than infer it from this targetless spec.
4. The current wake store stamps a condition wake with the maximum existing
   condition-fact id inside the scheduling transaction. A fact inserted later
   in that transaction has a greater id and can match after commit.
5. `escalation-ruled` is the reserved condition kind for all decision-request
   rulings. No condition-name registry maps aliases to it.
6. The existing operator decision option set is a closed array of non-blank,
   distinct labels. The selected decision must equal one member byte-for-byte
   after the verb's existing input normalization.
7. A valid terminal row retains its immutable request identity. A `consumed`
   row retains the ruling fields that caused consumption.
8. A direct authenticated user call can have no presenting Tightbeam session.
   That known absence is distinct from missing legacy provenance.
9. The selected target can add one schema-version migration, additive stored
   performer fields, and one integrity-evidence relation without rewriting
   historical request rows.
10. The existing operator-decision deadline duration is available as the
    finite fallback bound for a ruling-time condition wake. The fallback only
    bounds recovery if condition evaluation stalls; it does not decide or
    classify the ruling.

## Invariants

**INV-01 — Visibility precedes integrity.** A list or exact-id read applies the
existing authentication, authorization, and visibility predicate before it
validates or projects a row. A caller who cannot see a corrupt row receives the
same result as for an absent row. The refusal and evidence paths reveal no
hidden request.

**INV-02 — One terminal projection.** List and exact-id reads call one shared
terminal projector after visibility. For one stored snapshot, every terminal
projection field is byte-equal on both surfaces. Kind-specific projectors may
add or omit non-terminal detail; they shall not add, omit, null, rename, or
reinterpret a terminal projection field.

**INV-03 — Request kind preserves the decision.** A visible `operator` row in
`ruled` or `consumed` state exposes the full terminal projection. Selecting the
operator kind cannot route through a smaller `Map.take`, field allow-list, or
equivalent serializer that strips terminal fields.

**INV-04 — Closed dual attribution.** A new winning operator ruling stores the
on-behalf-of actor, performing principal, and presenting-session state from the
authenticated call in the ruling transaction. The owner remains the authorized
on-behalf-of actor. The performing principal and session remain execution
provenance. No field substitutes for another.

**INV-05 — Legacy attribution is explicit.** A legacy-complete ruling projects
`rulingAttribution.performer.state = "legacy-unknown"`. It also projects the
literal `legacy-unknown` values required by Architecture §1. A read, migration,
replay, or consumption does not populate historical performer fields.

**INV-06 — Total ruled shape or refusal.** Tightbeam shall validate every
visible `ruled` or `consumed` operator row against Architecture §2 before it
encodes any response bytes or applies a consumption mutation. On failure it
commits integrity evidence and returns `decision_request_integrity_invalid`.
It shall not emit a partial list, a partial detail response, a best-effort
decision, or a consumption effect.

**INV-07 — Evidence does not decide.** Integrity evidence records the request
id, ruled-shape digest, cause code, sorted failing field names, attempted
surface, first-observed time, and observing principal class. It stores no
question, option, context, rationale, decision, credential, session key, or
owner id. Readers never consult it to decide visibility, validity, authority,
delivery, or consumption.

**INV-08 — One mutation seam.** The existing owner-ruling transaction remains
the sole writer of operator decision, rationale, ruling attribution, ruled
time, ruling fact id, lifecycle event, and raiser notification wake. A second
serializer, notification worker, repair job, or read path shall not write
those values.

**INV-09 — One ruling winner.** Competing rule, withdraw, supersede, and other
terminal mutations contend on the existing `kind='operator' AND status='open'`
compare-and-set. Only its winner may write the terminal tuple, canonical fact,
lifecycle event, and raiser notification wake. A loser observes the committed
row and follows the existing typed conflict or exact-replay contract.

**INV-10 — Atomic ruling evidence.** The terminal request row, ruling
attribution, canonical condition fact, `rulingFactId` reference, ruling
lifecycle event, and raiser notification wake commit or roll back together.
No observer can see one committed component without the others.

**INV-11 — The event, not a proxy.** The raiser wake matches only the canonical
fact. Its fallback time bounds delivery recovery. It does not imply that a
ruling exists, choose an outcome, or replace the condition match.

**INV-12 — Idempotent automatic delivery.** One operator request has at most
one raiser notification wake for its ruling. An exact ruling replay returns the
stored result and creates no wake, fact, event, or turn. The existing wake-state
compare-and-set and unique wake-to-turn relation permit at most one committed
prompt turn from that wake.

**INV-13 — Canonical condition name.** Producers and consumers use the literal
`escalation-ruled`. `operator-decision-ruled`, `decision_request_ruled`, and all
other spellings are invalid as ruling condition kinds and match no raiser wake.
The lifecycle event name does not become a condition kind.

**INV-14 — Notification content is sufficient and private.** The automatic
prompt identifies the request id, says the owner ruled it, and tells the raiser
to use the exact-id read. It does not embed the question, context, rationale,
decision, owner id, or session key. The read path remains the disclosure
boundary.

**INV-15 — Manual mitigation stays separate.** A manual intermediary wake
does not share the automatic wake's idempotency key, cannot set it delivered,
and cannot satisfy an acceptance count for automatic delivery. The automatic
path remains required even if a manual wake already disclosed the result.

**INV-16 — Targetless compatibility.** This contract changes no target until
the product owner selects one through the normal work-item path. On the
selected target, additions are wire-compatible for existing list and ruling
clients except for the intentional replacement of a serialized impossible row
with a typed refusal. Existing visibility and hidden-row error envelopes remain
byte-compatible.

**INV-17 — Rollback never corrupts history.** A binary that understands the new
schema can be rolled back before any new ruling uses the new performer fields.
After such a ruling exists, an older binary that cannot preserve or project the
new attribution shall refuse startup or write access against that schema
version. Rollback never drops columns, deletes evidence, or rewrites terminal
rows.

**INV-18 — Visitor boundary.** A visitor actor remains the effective visitor
principal and carries no operator ruling authority. A broker or presenting
visitor session cannot be projected as the owner or performing operator ruler.
The operator-rule handler rejects the visitor before mutation.

## Architecture

### 1. Canonical read contract

The JSON wire result keeps the existing success envelope. `decision-requests`
returns its existing collection envelope and `decision-request` returns its
existing single-row envelope. Each visible operator row uses the target's
existing field casing and contains these parity fields:

```json
{
  "id": "dr_exact",
  "kind": "operator",
  "status": "ruled",
  "question": "Choose one",
  "options": ["alpha", "beta"],
  "raiserId": "session:raiser",
  "raiserSessionKey": "agent:raiser:session",
  "ownerUserId": "owner",
  "assignmentId": "asg_exact",
  "raisedAt": 1780000000000,
  "deadlineAt": 1780086400000,
  "decision": "alpha",
  "rationale": null,
  "ruledBy": "user:owner",
  "ruledAt": 1780000001000,
  "rulingFactId": 42,
  "consumedAt": null,
  "rulingAttribution": {
    "onBehalfOf": "user:owner",
    "performer": {
      "state": "known",
      "principal": "user:owner",
      "session": {
        "state": "known",
        "key": "agent:presenter:session"
      }
    }
  }
}
```

For a known direct call with no presenting session, `session` is exactly
`{"state":"none"}`. For a legacy-complete ruling, attribution is exactly:

```json
{
  "onBehalfOf": "user:owner",
  "performer": {
    "state": "legacy-unknown",
    "principal": "legacy-unknown",
    "session": {
      "state": "legacy-unknown"
    }
  }
}
```

The projector shall always emit every listed key for `ruled` and `consumed`
operator rows. `rationale`, `assignmentId`, `raiserSessionKey`, `deadlineAt`,
and `consumedAt` may contain JSON null when their existing domain permits it.
A consumed row keeps the same ruling values and has a non-null `consumedAt`.
An open, withdrawn, or superseded row retains the target's existing applicable
non-ruling projection; it shall not fabricate a ruling attribution.

The exact-id CLI command is:

```text
tightbeam decision-request --request <decisionRequestId>
```

It sends wire verb `decision-request` with `params.request`. It accepts one
non-blank complete id and no target flag or positional id. An absent, shortened,
or non-visible id follows the existing hidden-id `not_found` contract. The
command prints the existing result envelope and exits 0 on success.

### 2. Integrity contract

A `ruled` operator row is valid only when all of these checks pass in one
database snapshot:

1. Every request-identity field required by the stored schema is present and
   the id and kind are canonical.
2. `ownerUserId` is non-blank and `ruledBy` equals
   `user:<ownerUserId>`.
3. `decision` is non-blank and equals one member of the immutable stored option
   array under the ruling verb's existing normalization.
4. The rationale key is present in the projection. Its stored value is either
   null or a string accepted by the existing ruling contract.
5. `ruledAt` is an integer timestamp and `rulingFactId` is an integer id.
6. `rulingFactId` resolves to one condition fact whose kind is exactly
   `escalation-ruled` and whose scope is exactly the request id.
7. A post-migration ruling has a canonical performing principal and one closed
   session state: `known` with a canonical session key, or `none`.
8. A legacy-complete ruling uses the exact `legacy-unknown` performer value. It
   does not mix known and unknown performer members.
9. `status='ruled'` has `consumedAt=null`. `status='consumed'` has an integer
   `consumedAt` that is not earlier than `ruledAt`.

The same rules apply to a `consumed` row. A row that fails a check is an
impossible ruled shape. The list projector validates all admitted rows before
it encodes the collection. One impossible row refuses the whole collection;
it never removes that row and returns the rest. The detail projector validates
before it encodes the row. The consumer validates inside its transaction before
its consumption compare-and-set or external effect.

The typed wire refusal is HTTP 500 with the existing error envelope:

```json
{
  "error": {
    "code": "decision_request_integrity_invalid",
    "message": "decision request integrity check failed",
    "requestId": "dr_exact"
  }
}
```

The CLI prints the typed code and request id to stderr and exits nonzero. It
prints no terminal fields. Because visibility precedes validation, returning the
id does not disclose a hidden request.

The additive relation `decision_request_integrity_evidence` has one row per
`(requestId, shapeDigest)`. `shapeDigest` is SHA-256 over a versioned canonical
encoding of the fields inspected by checks 1-9, including explicit nulls but no
secret or free-text values in the evidence row. The row stores:

```text
requestId, shapeDigest, schemaVersion, causeCode, failingFields,
firstSurface, firstObservedAt, observerPrincipalClass
```

`causeCode` is `ruled-shape-incomplete`. `failingFields` is a sorted JSON array
of closed field names. `firstSurface` is one of `list`, `detail`, `consume`, or
`migration-preflight`. `observerPrincipalClass` is one of `session`, `user`,
`process`, `org`, or `migration`; it contains no principal id. A uniqueness
conflict reads and returns the existing identical evidence row. A conflict with
different canonical evidence for the same key returns
`decision_request_integrity_evidence_conflict`. If evidence cannot commit, the
operation returns `decision_request_integrity_evidence_unavailable`. Both
errors still prohibit serialization and consumption.

### 3. Ruling and automatic raiser delivery

The owner-ruling transaction performs these ordered steps:

1. Authenticate the call, apply existing owner/admin authorization, load the
   operator request, validate the selected label, and derive the canonical
   on-behalf-of actor, performing principal, and presenting-session state.
2. Win the existing open-row compare-and-set. A loser creates no side effect.
3. Write the decision, explicit rationale value, attribution, and `ruledAt` to
   the request inside the transaction.
4. Schedule one pending prompt wake to the recorded `raiserSessionKey`. Set
   `conditionKind="escalation-ruled"`, `conditionScope=<requestId>`,
   `targetGate=0`, and the existing operator-decision duration as the finite
   fallback after `ruledAt`. The wake cursor is therefore the greatest
   condition-fact id before the new ruling fact.
5. File the canonical condition fact, store its id in `rulingFactId`, and write
   the existing ruling lifecycle event.
6. Validate the resulting ruled shape and commit the row, wake, fact, reference,
   and event together. After commit, nudge the existing condition evaluator.

The automatic prompt text is exactly:

```text
Decision request <requestId> was ruled. Read it with tightbeam decision-request --request <requestId>.
```

The condition evaluator selects the new fact because its id is greater than the
wake cursor and its kind and scope are exact. Its existing pending-to-fired
compare-and-set and wake-to-turn uniqueness produce at most one durable prompt
turn. A fallback fire uses the same wake and does not create a second channel.

An exact ruling replay is successful only under the selected target's existing
idempotency contract. It returns the stored request after integrity validation
and does not repeat steps 2-6. A different option, rationale, principal, or
terminal verb follows the existing terminal-conflict contract.

### 4. Migration, compatibility, and rollback

The selected target shall use one additive schema migration:

1. Add stored performing-principal and presenting-session-state fields if that
   target does not have them. Existing `ruledBy` remains the on-behalf-of owner
   compatibility field. An existing `ruledViaSessionKey` can satisfy only the
   known-session member; null alone cannot distinguish `none` from
   `legacy-unknown`.
2. Add `decision_request_integrity_evidence` and its uniqueness constraint.
3. Preflight every terminal operator row in one read snapshot. Classify a row
   as post-migration valid, legacy-complete, or impossible. The migration writes
   no request row.
4. Refuse activation with `decision_request_integrity_invalid` if any row is
   impossible. Commit the privacy-safe evidence row for each impossible shape
   before refusing activation.
5. Record the new schema version only after the preflight passes. Legacy-complete
   rows retain null storage and project `legacy-unknown` at read time.

Wire compatibility is additive: the exact-id verb and `rulingAttribution` are
new, while existing list envelopes and flat fields retain their names and
meaning. The intentional behavior change is that a visible impossible terminal
row now returns a typed failure instead of lossy JSON or consumption. A selected
target that already exposes `decision-request` keeps its syntax and exact-id
semantics; another target adds the syntax before advertising it.

The implementation shall update the applicable canonical CLI and REST/wire
specs in the same source change. If
`decision-request-client-observable-state-v1.md` becomes live first, this
contract supersedes its operator terminal field set only; its shared-serializer
rule remains compatible and shall call this projector.

Rollback to an older binary is allowed only while no post-migration ruling or
integrity evidence exists. Otherwise the deployment preflight refuses the old
binary before it serves reads or writes. Forward recovery redeploys the aware
binary. Rollback does not reverse the migration or mutate history.

### 5. Observability

The existing request row, canonical condition fact, lifecycle event, wake row,
and prompt turn remain the primary trace. The integrity relation adds refusal
evidence without duplicating private payloads. The trace for one successful
ruling shall join:

```text
decision request id
  -> rulingFactId / escalation-ruled fact
  -> one raiser notification wake
  -> zero or one prompt turn while pending, exactly one after durable delivery
```

The wake lifecycle shall name whether `condition` or `fallback` fired it. The
request trace shall show the on-behalf-of actor, performing principal, and
presenting-session state as separate fields. An operator-facing inspect command
may expose integrity evidence only under existing admin visibility. Ordinary
decision-request reads do not expose integrity evidence rows.

## Acceptance

Each case uses a fresh database, fixed timestamps, deterministic transaction
barriers, and the selected target's real gateway and built CLI where named.

**A-01 — Open projection.** Given one visible open operator request, when its
owner and raiser list it and fetch its exact id, then existing open fields match
their current contract, no ruling attribution is fabricated, and neither read
writes integrity evidence.

**A-02 — Ruled list/detail parity.** Given one valid ruled operator request with
known performer and session provenance, when the same authorized caller lists
all requests and fetches the exact id in one database snapshot, then every field
from Architecture §1 is present and byte-equal. The detail response may add
`context` and `actionKey`; it does not change a parity field.

**A-03 — Request kind cannot strip fields.** Given a valid ruled operator row
and a valid ruled non-operator row, when each passes its existing visibility
predicate, then selecting `kind='operator'` does not remove `decision`,
`rationale`, `ownerUserId`, `ruledBy`, `ruledAt`, `rulingFactId`, `consumedAt`,
or `rulingAttribution`. A projection-level test fails if a kind-specific
allow-list omits one of them.

**A-04 — Exact-id CLI and wire.** Given the real gateway and built Rust CLI,
when an authorized caller runs `tightbeam decision-request --request <fullId>`,
then the wire request is verb `decision-request` with `params.request`, the CLI
prints the single result envelope, and exits 0. Blank ids, prefixes, positional
ids, duplicate request flags, and target flags fail. An absent or non-visible id
returns the existing `not_found` status, envelope, stderr, and nonzero exit.

**A-05 — Lifecycle states.** Given open, ruled, consumed, withdrawn, and
superseded operator fixtures, when visible list and exact-id reads run, then
open, withdrawn, and superseded preserve their existing applicable fields;
ruled has null `consumedAt`; consumed has `consumedAt >= ruledAt`; and both
terminal decision states retain the identical ruling tuple. No state fabricates
fields from another state.

**A-06 — Optional rationale is explicit.** Given two valid rulings, one with a
string rationale and one with stored null, when list and detail reads run, then
both contain the `rationale` key with the exact stored value. Neither serializer
omits the key or replaces null with an empty string.

**A-07 — Known dual attribution.** Given an authorized owner rule presented by
a Tightbeam session, when the ruling wins, then `ruledBy` and
`rulingAttribution.onBehalfOf` equal `user:<ownerUserId>`, the performer
principal equals the authenticated effective principal, and the known session
key equals the authenticated transport session. A role alias, raiser, current
owner session, broker, origin text, and process name cannot replace those
values.

**A-08 — Known no-session attribution.** Given an authorized direct user call
with no presenting Tightbeam session, when the ruling wins, then performer
state is `known`, its principal is the authenticated user, and session is
exactly `{"state":"none"}`. It is not `legacy-unknown`.

**A-09 — Legacy attribution.** Given a pre-migration row with a valid owner,
decision, ruling time, canonical fact, and lifecycle shape but no provable
performer fields, when migration, list, exact read, replay, and consumption
inspect it, then the stored row remains byte-identical and both reads emit the
exact legacy attribution from Architecture §1. No operation copies the owner,
raiser, current caller, lifecycle prose, or wake origin into performer fields.

**A-10 — Visitor and intermediary separation.** Given a visitor credential, a
broker user, and an intermediary session, when each attempts operator-rule
without existing owner authority, then each call retains its canonical
principal, receives the existing authorization refusal, and writes no request,
fact, event, wake, evidence, or attribution. A manual intermediary wake does
not appear as ruling performance or automatic delivery.

**A-11 — Valid-label ruling.** Given an open request whose options are
`["alpha","beta"]`, when the authorized owner selects `alpha`, then one
transaction writes the complete ruled shape, one canonical fact, one lifecycle
event, and one raiser notification wake. The fact id stored on the row resolves
to kind `escalation-ruled` and scope equal to the request id.

**A-12 — Invalid labels.** Given the same open request, when the owner submits
`gamma`, a blank label, a case-changed label, or a non-string value, then the
existing typed invalid-decision refusal occurs before the open-row mutation.
Request, fact, event, wake, evidence, and turn counts do not change.

**A-13 — Terminal mutation race.** Given one open request, when valid rule,
withdraw, and supersede transactions wait at deterministic barriers and then
resume in every order, exactly one open-row compare-and-set wins. Only a ruling
winner creates the ruling tuple, fact, ruling event, and raiser wake. Every
loser follows the existing conflict contract and creates none of those effects.

**A-14 — Ruling replay.** Given one committed ruling, when the same authorized
principal repeats the exact accepted option and rationale under the target's
existing replay contract, then it returns the stored valid row. Counts for
request mutation, condition fact, lifecycle event, wake, and prompt turn do not
increase. A changed option, rationale, principal, or terminal verb does not
qualify as that replay.

**A-15 — At-most-once automatic raiser delivery.** Given one ruling winner and
concurrent condition evaluators, fallback evaluation, scheduler restart, and
delivery replay, when all paths settle, then the database contains one raiser
notification wake and at most one prompt turn for its wake id. After delivery,
it contains exactly one committed prompt turn. The prompt matches Architecture
§3 and the request remains unchanged.

**A-16 — Correct condition kind.** Given pending wakes scoped to the same
request under `escalation-ruled`, `operator-decision-ruled`, and
`decision_request_ruled`, when the canonical ruling fact commits, then only the
`escalation-ruled` wake matches it. The two wrong names remain pending until
their finite fallback or explicit cancellation and are never treated as
aliases. Production code creates none of the wrong-name wakes.

**A-17 — Schedule-before-fact race closure.** Given unrelated condition facts
already exist and the ruling transaction pauses after scheduling the raiser
wake but before filing its fact, when an evaluator runs before commit, it sees
neither row. After commit, the new fact id is greater than the wake cursor and
the exact kind/scope match fires it. A rollback exposes neither wake nor fact.

**A-18 — List integrity refusal.** Given an authorized list contains one valid
row and one ruled row missing `rulingFactId`, when the caller lists them, then
the response is HTTP 500 `decision_request_integrity_invalid`, contains the bad
request id and no decision fields, emits no partial collection bytes, and
commits one evidence row whose failing fields are `["rulingFactId"]`.

**A-19 — Detail integrity refusal.** Given a visible ruled row whose fact has a
wrong kind or scope, when the caller fetches its exact id, then it receives the
same named refusal and no row bytes. Evidence names `rulingFactId` under the
closed failure vocabulary and stores no fact payload or private request field.

**A-20 — Consumption integrity refusal.** Given an impossible ruled row is the
candidate for policy consumption, when the consumer transaction runs, then it
commits no consumption timestamp, authorization, handler effect, event, or
notification. It commits or reuses the evidence row and returns
`decision_request_integrity_invalid`.

**A-21 — Integrity evidence idempotency.** Given one impossible immutable shape,
when list, detail, consume, restart, and replay observe it repeatedly, then the
unique `(requestId, shapeDigest)` relation contains one row. A forced
non-identical uniqueness conflict returns
`decision_request_integrity_evidence_conflict`. A forced evidence-write failure
returns `decision_request_integrity_evidence_unavailable`. Neither case emits or
consumes the request.

**A-22 — Visibility and privacy.** Given an impossible ruled row, when an
unauthorized session, unrelated user, process principal, org principal without
visibility, and anonymous caller use list and exact-id reads, then each receives
its existing absent-row result and no integrity evidence is written on that
call. An authorized owner and raiser receive A-18 or A-19. No external response
contains the question, context, rationale, option, owner id, or session key.

**A-23 — Migration preflight.** Given fixtures for a post-migration valid row,
a legacy-complete row, a row missing decision, a row with a non-option decision,
a row missing owner, a row with a missing fact, and a row with a wrong-name
fact, when migration preflight runs twice, then it classifies the first two
without request writes, records one evidence row per impossible shape, and
refuses schema activation. After only valid and legacy-complete fixtures remain
in a fresh database, activation succeeds without rewriting either row.

**A-24 — Rollback fence.** Given the new schema with no post-migration ruling or
evidence, when the documented old-binary preflight runs, then rollback is
allowed without reverse migration. Given either one new attributed ruling or
one integrity evidence row, the same preflight refuses the old binary before
gateway start and leaves all rows intact.

**A-25 — Manual mitigation does not mask automatic delivery.** Given a manual
intermediary wake reaches the raiser before the owner rules, when the owner
later rules, then the ruling transaction still creates its one automatic wake.
The manual wake cannot fire, cancel, acknowledge, or deduplicate the automatic
wake, and only the automatic wake counts toward A-15.

**A-26 — Atomic failure matrix.** Given injected failures after each ordered
step in Architecture §3, when the transaction aborts, then request, attribution,
fact, event, and automatic wake counts return to their pre-call values. Given a
successful commit followed by a failed scheduler nudge, the durable wake and
fact remain joinable and a restarted evaluator delivers through the same wake.

**A-27 — Real-response fixture and compatibility gate.** Given an unmodified
selected source revision and the candidate implementation in fresh owned
worktrees, when the implementation lane builds the release CLI, captures real
gateway responses for open, ruled, consumed, legacy, hidden, and impossible
fixtures, and runs the target's baseline and candidate gates, then the baseline
is recorded, the candidate gate is green, and checked-in fixtures are captured
from those real responses rather than hand-written. Existing non-operator
decision-request tests remain green.

**A-28 — Trace completeness.** Given one known-attribution ruling, one legacy
ruling, one delivered raiser wake, and one integrity refusal, when an authorized
operator inspects their traces, then it can join each request to its canonical
fact, lifecycle event, wake, and prompt turn when present; distinguish
on-behalf-of actor, performer principal, and presenting-session state; identify
condition versus fallback delivery; and find the privacy-safe evidence row.
No join depends on lifecycle prose parsing.

## Open Questions

None. Target selection, `specRef` binding, implementation, and the independent
exact-revision review are intentionally outside this assignment. The parent
shall open one independent review against the published commit and file SHA
after this spec's required cold digest and spec-ready receipt.
