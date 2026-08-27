# Terminal operator-decision parity and integrity — v1

Status: SPEC-READY, TARGETLESS — exact-revision review findings F1-F3 applied;
awaiting parent-opened independent re-review

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
`03fe3dd000a920be82c17e1a4246ef9e0482edfd7b8cffda125a94ab4ec1c32c`.
These source revisions are evidence pins, not implementation targets.

Revision evidence: independent exact-revision review verdict
`att_8a08d480-8aae-46b9-93c8-191a18dcd749` and report artifact
`art_1dfda29c` against commit
`a98b3cac7a0734c5ddf2c53201f7b8829815eeee`.

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
closed ruled shape shall produce a named integrity refusal and durable,
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
one immutable epoch row, one integrity-evidence relation, and one CLI
affordance; it adds no adjudicator, hold state, polling loop, target selector,
or second delivery channel. The epoch wins over rewriting historical rows or
accepting a nullable ambiguity because it deterministically brackets legacy
facts from future writes. This is
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
  decision authority. Existing operator-owner authorization remains the sole
  ruling boundary.
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
  mutation, a producer-opened independent review, or a producer review verdict.

## Terms

- **Operator decision request**: one durable, owner-scoped enumerated decision
  request created through `operator-ask` or the target-equivalent owner-decision
  create verb. Its canonical kind is `operator`.
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
  request identity, owner, non-blank outcome, time, fact, and lifecycle shape
  are valid, but whose stored fields cannot prove one or both of performing
  principal and presenting session.
- **Legacy unknown**: the literal state `legacy-unknown`. It records absence of
  historical proof. It is not a guess, null synonym, wildcard, repair request,
  or authorization value.
- **Legacy ruling epoch**: the immutable activation row whose
  `legacyRulingFactMaxId` is the greatest condition-fact id visible in the
  exclusive activation transaction. A ruling whose canonical fact id is at or
  below that cutoff can use legacy-unknown fields. A later ruling cannot.
- **Impossible ruled shape**: a visible row whose status claims `ruled` or
  `consumed` but fails one or more checks in Architecture §2. A legacy-complete
  ruling is not impossible.
- **Canonical ruling fact**: one durable condition fact with kind exactly
  `escalation-ruled`, scope exactly the decision request id, and id exactly
  `rulingFactId`.
- **Canonical ruling lifecycle event**: exactly one lifecycle row whose kind
  is `decision_request_ruled` and whose subject is the request id. Integrity
  checks use those relational fields and do not parse lifecycle prose.
- **Raiser notification wake**: for a post-activation ruling, exactly one
  durable prompt wake with the complete relational shape in Architecture §2.
  It is addressed to the request's recorded `raiserSessionKey` and armed for
  condition kind `escalation-ruled` and scope equal to the request id.
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
   operator-owner and other existing authorization, visibility, open-row
   compare-and-set, the atomic ruling row/fact/event write, and downstream
   consumption except where this contract narrows its read and delivery clauses.
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
6. The existing operator option set is a non-empty array of objects whose sole
   key is `label`; normalized labels are non-blank and distinct. The existing
   ruling verb accepts exactly one listed-label input or one non-blank free-text
   response.
7. A valid terminal row retains its immutable request identity. Under the
   existing operator contract, an operator row never enters `consumed` and its
   `consumedAt` value remains null. The consumption field is still part of the
   parity projection so both readers expose that lifecycle fact.
8. The authenticated ruling call exposes its canonical effective principal and
   whether a Tightbeam transport session presented it. A post-migration call
   with no presenting session records known absence; it does not use legacy
   unknown.
9. The selected target can add one schema-version migration, additive stored
   performer fields, one singleton legacy-epoch relation, and one
   integrity-evidence relation without rewriting historical request rows.
10. The existing operator-decision deadline duration is available as the
    finite fallback bound for a ruling-time condition wake. The fallback only
    bounds recovery if condition evaluation stalls; it does not decide or
    classify the ruling.
11. An operator request is filed by an authenticated session and stores a
    non-null `raiserSessionKey`. The automatic ruling notice targets that exact
    recorded session; it does not re-resolve a role or owner at delivery time.
12. Condition facts are append-only and use an `AUTOINCREMENT` integer id. A
    fact committed after the exclusive activation cutoff has an id greater than
    `legacyRulingFactMaxId`; deletion or reuse cannot move it behind the epoch.

## Invariants

**INV-01 — Visibility precedes integrity.** A list or exact-id read applies the
existing authentication, authorization, and visibility predicate before it
validates or projects a row. A caller who cannot see a corrupt row receives the
same result as for an absent row. The refusal and evidence paths reveal no
hidden request.

**INV-02 — One terminal projection.** List and exact-id reads call one shared
terminal projector after visibility. When no mutation occurs between the two
reads, every terminal projection field is byte-equal on both surfaces.
Kind-specific projectors may add or omit non-terminal detail; they shall not
add, omit, null, rename, or reinterpret a terminal projection field.

**INV-03 — Request kind preserves the decision.** A visible `operator` row in
`ruled` state exposes the full terminal projection. Selecting the operator kind
cannot route through a smaller `Map.take`, field allow-list, or equivalent
serializer that strips terminal fields. A stored `consumed` operator row
refuses as impossible; it is not a smaller projection.

**INV-04 — Closed dual attribution.** A new winning operator ruling stores the
on-behalf-of actor, performing principal, and presenting-session state from the
authenticated call in the ruling transaction. The owner remains the authorized
on-behalf-of actor. The performing principal and session remain execution
provenance. No field substitutes for another.

**INV-05 — Legacy unknowns are explicit and lossless.** Each unproved performer
component of a legacy-complete ruling projects its own `legacy-unknown` state.
A stored legacy session key remains a known session even when the performing
principal is unknown. Only a ruling whose canonical fact id is at or below the
immutable legacy ruling epoch can use those unknown states. A read, migration,
replay, or consumption does not populate historical fields or discard stored
provenance.

**INV-06 — Total ruled shape or refusal.** Tightbeam shall validate every
visible `ruled` operator row against Architecture §2 before it encodes any
response bytes or applies a consumption mutation. An operator row that claims
`consumed` is itself an impossible ruled shape. On failure Tightbeam commits
integrity evidence and returns `decision_request_integrity_invalid`. It shall
not emit a partial list, a partial detail response, a best-effort decision, or
a consumption effect.

**INV-07 — Evidence does not decide.** Integrity evidence records the request
id, ruled-shape digest, cause code, sorted failing field names, attempted
surface, first-observed time, and canonical observing principal. It stores no
question, option, context, rationale, decision, credential, or separate owner
field. Readers never consult it to decide visibility, validity, authority,
delivery, or consumption.

**INV-08 — One mutation seam.** The existing owner-ruling transaction remains
the sole writer of operator decision, rationale, ruling attribution, ruled
time, ruling fact id, lifecycle event, and raiser notification wake. A second
serializer, notification worker, repair job, or read path shall not write those
values.

**INV-09 — One ruling winner.** Competing rule, withdraw, supersede, and other
terminal mutations contend on the existing `kind='operator' AND status='open'`
compare-and-set. Only its winner may write the terminal tuple, canonical fact,
lifecycle event, and raiser notification wake. A loser observes the committed
row and follows the existing typed conflict or exact-replay contract.

**INV-10 — Atomic ruling evidence.** For a post-activation ruling, the terminal
request row, ruling attribution, canonical condition fact, `rulingFactId`
reference, ruling lifecycle event, and raiser notification wake commit or roll
back together. No observer can see one committed component without the others.
Pre-activation rows remain governed by the legacy boundary in INV-05 and do not
gain a historical wake.

**INV-11 — The event, not a proxy.** The raiser wake matches only the canonical
fact. Its fallback time bounds delivery recovery. It does not imply that a
ruling exists, choose an outcome, or replace the condition match. Because the
wake and fact commit together and the fire seam rechecks for a matching fact
before it classifies a due wake, a valid automatic notification records
`firedBy="condition"`, never `fallback`.

**INV-12 — Idempotent automatic delivery.** One post-activation operator
ruling has exactly one canonical raiser notification wake. An exact ruling
replay returns the stored result and creates no wake, fact, event, or turn. The
existing wake-state compare-and-set and unique wake-to-turn relation permit at
most one committed prompt turn from that wake. Pre-activation rulings do not
acquire a wake by migration, projection, replay, or consumption.

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
has a distinct non-process origin and wake row, cannot set the automatic wake
delivered, and cannot satisfy an acceptance count for automatic delivery. The
automatic path remains required even if a manual wake already disclosed the
result.

**INV-16 — Targetless compatibility.** This contract changes no target until
the product owner selects one through the normal work-item path. On the
selected target, additions are wire-compatible for existing list and ruling
clients except for the intentional replacement of a serialized impossible row
with a typed refusal. Existing visibility and hidden-row error envelopes remain
byte-compatible.

**INV-17 — Rollback never restores the defect.** Before schema activation, the
deployment can roll back to the prior binary. After activation, a binary that
cannot preserve and project this contract shall refuse gateway startup against
the new schema version, even when no new ruling exists. Recovery rolls forward
to an aware binary. Rollback never drops columns, deletes evidence, rewrites
terminal rows, or serves the lossy projection again.

**INV-18 — Visitor boundary.** A visitor actor remains the effective visitor
principal and carries no operator ruling authority. A broker or presenting
visitor session cannot be projected as the owner or performing operator ruler.
The operator-rule handler rejects the visitor before mutation.

**INV-19 — Future attribution defects are rejected at write time.** After
activation, a database trigger rejects an `open` to `ruled` operator transition
unless performing principal and presenting-session state form the closed
post-migration attribution shape in Architecture §2. The ruling transaction's
single commit supplies the event and wake. The read-time relational checks
cover missing, wrong, or duplicate event and wake rows, plus legacy data,
manual corruption, restore defects, and disabled or unaware writers. The
trigger takes the database-refusal rung for attribution; the visibility-first
read and consume refusal is the deterministic rail for cross-relation
integrity.

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
  "options": [{"label": "alpha"}, {"label": "beta"}],
  "raiserId": "session:raiser",
  "raiserSessionKey": "agent:raiser:session",
  "ownerUserId": "owner",
  "assignmentId": "asg_exact",
  "raisedAt": 1780000000000,
  "deadlineAt": 1780086400000,
  "decision": "alpha",
  "rationale": null,
  "ruledBy": "user:owner",
  "ruledViaSessionKey": "agent:presenter:session",
  "ruledAt": 1780000001000,
  "rulingFactId": 42,
  "consumedAt": null,
  "rulingAttribution": {
    "onBehalfOf": "user:owner",
    "performer": {
      "principal": {
        "state": "known",
        "value": "user:owner"
      },
      "session": {
        "state": "known",
        "key": "agent:presenter:session"
      }
    }
  }
}
```

For a known direct call with no presenting session, `ruledViaSessionKey` is
null and `session` is exactly `{"state":"none"}`. For a legacy-complete
ruling with neither performer component stored, `ruledViaSessionKey` is null
and attribution is exactly:

```json
{
  "onBehalfOf": "user:owner",
  "performer": {
    "principal": {
      "state": "legacy-unknown"
    },
    "session": {
      "state": "legacy-unknown"
    }
  }
}
```

When a legacy row stores `ruledViaSessionKey` but no performing principal, the
projector preserves that key and emits a known session member beside a
`legacy-unknown` principal member. It does not collapse both members to unknown.

The request row stores new rulings in the additive columns
`ruledViaPrincipal` and `ruledViaSessionState`. `ruledViaPrincipal` is the
canonical performing principal. `ruledViaSessionState` is `known` or `none`;
`known` requires a non-null `ruledViaSessionKey`, and `none` requires null. The
nested wire attribution is a projection of those stored fields plus `ruledBy`.
Pre-migration rows retain null in the new columns.

The projector shall always emit every listed key for a `ruled` operator row.
`rationale`, `assignmentId`, `deadlineAt`, and `ruledViaSessionKey` may contain
JSON null when their existing domain permits it. `raiserSessionKey` is non-null
for an operator request. `consumedAt` is present and null. An open, withdrawn,
or superseded row retains the target's existing applicable non-ruling
projection; it shall not fabricate ruling attribution. A stored operator row
with `status="consumed"` is impossible and follows §2.

The exact-id CLI command is:

```text
tightbeam decision-request --request <decisionRequestId>
```

This syntax supersedes the positional `decision-request <id>` notation in
`escalation-substrate-v1.md` for any target that implements this contract.
It sends wire verb `decision-request` with `params.request`. It accepts one
non-blank complete id and no target flag or positional id. An absent, shortened,
or non-visible id follows the existing hidden-id `not_found` contract. The
command prints the existing result envelope and exits 0 on success.

### 2. Integrity contract

A `ruled` operator row is valid only when all of these checks pass in one
database snapshot:

1. Every request-identity field required by the stored schema is present and
   the id and kind are canonical.
2. `ownerUserId` and `raiserSessionKey` are non-blank and `ruledBy` equals
   `user:<ownerUserId>`.
3. The stored option value decodes as a non-empty array of objects whose sole
   key is `label`; normalized labels are non-blank and distinct.
4. `decision` is a non-blank normalized string. It can be a stored option label
   accepted through the label input or a free-text response. The row does not
   encode which input form produced it, and integrity validation does not infer
   that form from the string.
5. The stored rationale is null or a string accepted by the existing ruling
   contract. The shared projector always emits its key and exact value.
6. `ruledAt` is an integer timestamp and `rulingFactId` is an integer id.
7. `rulingFactId` resolves to one condition fact whose kind is exactly
   `escalation-ruled` and whose scope is exactly the request id.
8. A ruling whose fact id is greater than `legacyRulingFactMaxId` has a known
   canonical `ruledViaPrincipal` and one closed session state: `known` with the
   same canonical key as `ruledViaSessionKey`, or `none` with
   `ruledViaSessionKey=null`.
9. A legacy-complete ruling has a fact id at or below
   `legacyRulingFactMaxId` and uses `legacy-unknown` for each unproved performer
   component. A stored non-null `ruledViaSessionKey` produces a known session
   component even when the principal component is unknown. A null legacy
   session value produces `legacy-unknown`, never `none`.
10. `status` is exactly `ruled` and `consumedAt` is null. `consumed` is not a
    valid operator lifecycle state.
11. Exactly one lifecycle event has kind `decision_request_ruled` and subject
    equal to the request id. Zero or more than one matching row is invalid.
    Validation does not inspect `detail` prose.
12. If `rulingFactId` is greater than `legacyRulingFactMaxId`, exactly one wake
    has all of this canonical shape: `sessionKey` equals the stored
    `raiserSessionKey`; `targetRole` is null; `origin` is
    `process:tightbeam`; `prompt` equals the literal in §3 after substituting
    the request id; `consumer` is `prompt`; `conditionKind` is
    `escalation-ruled`; `conditionScope` equals the request id;
    `conditionAfterId` is less than `rulingFactId`; `creatorSessionKey` equals
    the known presenting session or is null for a `none` session;
    `dueAt` equals `ruledAt` plus the existing operator-decision duration;
    `targetGate` is `0`; and role re-resolution is absent. Its state is either
    pending with null `firedAt` and `firedBy`, or fired with an integer
    `firedAt` and `firedBy="condition"`. Zero or more than one matching wake is
    invalid. A pre-activation ruling has no automatic-wake integrity
    requirement because this contract never invents or backfills historical
    delivery.

A row that fails a check is an impossible ruled shape. The list projector
validates all admitted rows before it encodes the collection. It commits one
atomic evidence batch for every invalid admitted row and returns the
lexicographically smallest invalid request id in the refusal. It never removes
an invalid row and returns the rest. The detail projector validates before it
encodes the row. A consumer validates inside its transaction before its
consumption compare-and-set or external effect.

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
structural descriptor for checks 1-12: each inspected member's presence and
type class, each closed-vocabulary state, each cross-field equality result,
each fact, event, and wake cardinality or relational-match result, and the
sorted failing-field names. The closed failure vocabulary includes
`rulingLifecycleEvent` and `raiserNotificationWake`. The
descriptor contains no field value, free text, credential, principal id, user
id, session key, option label, decision, or timestamp. The row stores:

```text
requestId, shapeDigest, schemaVersion, causeCode, failingFields,
firstSurface, firstObservedAt, observerPrincipal
```

`causeCode` is `terminal-shape-invalid`. `failingFields` is a sorted JSON array
of closed field names. `firstSurface` is one of `list`, `detail`, `consume`, or
`migration-preflight`. `observerPrincipal` is the canonical authenticated
principal or `process:tightbeam` for migration. Evidence is visible only under
the existing admin audit boundary. A uniqueness conflict reads and returns the
existing identical evidence row. A conflict with different canonical evidence
for the same key returns
`decision_request_integrity_evidence_conflict`. If evidence cannot commit, the
operation returns `decision_request_integrity_evidence_unavailable`. Both
errors still prohibit serialization and consumption.

### 3. Ruling and automatic raiser delivery

The owner-ruling transaction performs these ordered steps:

1. Authenticate the call, apply existing operator-owner authorization, load the
   operator request, validate exactly one listed-label input or non-blank text
   response, and derive the canonical on-behalf-of actor, performing principal,
   and presenting-session state. If the stored row is already terminal,
   classify replay or conflict before scheduling anything.
2. Fix `ruledAt` for this attempt and schedule one pending prompt wake to the
   recorded `raiserSessionKey`. Set
   `conditionKind="escalation-ruled"`, `conditionScope=<requestId>`,
   `origin="process:tightbeam"`, `creatorSessionKey` to the presenting session
   or null, `targetGate=0`, and the existing operator-decision duration as the
   finite fallback after `ruledAt`. The wake cursor is therefore the greatest
   condition-fact id before the new ruling fact.
3. File the canonical condition fact with `origin="process:tightbeam"`.
4. Execute one complete `kind='operator' AND status='open'` compare-and-set that
   writes status, decision, explicit rationale value, attribution, `ruledAt`,
   and the new fact id as `rulingFactId`. If the compare-and-set loses, roll
   back the wake and fact before classifying the committed winner under the
   existing replay/conflict contract.
5. Write the existing ruling lifecycle event only after the compare-and-set
   wins.
6. Validate the resulting ruled shape and commit the row, wake, fact,
   reference, and event together. After commit, nudge the existing condition
   evaluator.

The automatic prompt text is exactly:

```text
Decision request <requestId> was ruled. Read it with tightbeam decision-request --request <requestId>.
```

The condition evaluator selects the new fact because its id is greater than the
wake cursor and its kind and scope are exact. Its existing pending-to-fired
compare-and-set and wake-to-turn uniqueness produce at most one durable prompt
turn. If the due-time branch selects the wake after downtime, the fire seam
finds the already-committed matching fact first and records `condition` as the
cause. It uses the same wake and does not create a second channel.

An exact ruling replay by the authorized owner returns the stored request after
integrity validation and does not repeat steps 2-6. Normalized outcome and
rationale must match. The row does not infer whether an equal outcome arrived
through label or text input. A different presenting session can deliver an
otherwise exact owner replay, but it does not replace the winning ruling's
stored principal or session. A different outcome, rationale, owner principal,
or terminal verb follows the existing terminal-conflict contract.

### 4. Migration, compatibility, and rollback

The selected target shall use one additive schema migration:

1. Add nullable `ruledViaPrincipal` and `ruledViaSessionState` request columns.
   Existing `ruledBy` remains the on-behalf-of owner compatibility field.
   Existing `ruledViaSessionKey` remains the presenting-session compatibility
   field.
2. Add `decision_request_integrity_evidence` and its uniqueness constraint. Add
   singleton relation `decision_request_terminal_epoch` with columns `id=0`,
   `schemaVersion`, `legacyRulingFactMaxId`, `activatedAt`, `cause`, and
   `principal`.
3. Under the target's exclusive schema-activation transaction, read the maximum
   condition-fact id once. Preflight every operator row against that proposed
   legacy cutoff in the same snapshot. Classify non-ruling rows as applicable,
   ruled rows as legacy-complete or impossible, and any consumed row as
   impossible. The migration writes no request row.
4. In that transaction, record or reuse privacy-safe evidence for every
   impossible pre-existing shape, then insert the immutable epoch row with the
   proposed fact cutoff, `cause="terminal-operator-decision-parity-v1"`, and
   `principal="process:tightbeam"`; install the future-write trigger; and move
   the existing schema stamp to the new version. The presence of an impossible
   row does not withhold activation. After activation, an admitted read or
   consumer refuses that row through §2 while other gateway behavior remains
   available. The migration adds no repair, disposition, hold, or request-row
   write. Legacy-complete request rows retain null storage and project
   `legacy-unknown` at read time.
5. The trigger covers both a new terminal insert and an `open` to `ruled`
   update. It requires non-null `ruledViaPrincipal`,
   `ruledViaSessionState` in `known|none`, and the exact session-state/key
   relation from §2. It aborts the entire caller transaction with
   `decision_request_integrity_invalid` before an incomplete new ruling can
   commit.

An evidence or schema write failure aborts the activation transaction and can
be retried against unchanged request history. An impossible request shape is a
named accepted failure value, not an activation dependency: only its admitted
serialization or consumption is refused. This deletion wins over a repair
workflow because the visibility-first per-row rail already prevents the lossy
behavior, and a repair would violate the no-history-rewrite boundary.

Wire compatibility is additive: the exact-id verb and `rulingAttribution` are
new, while existing list envelopes and flat fields retain their names and
meaning. The intentional behavior change is that a visible impossible terminal
row now returns a typed failure instead of lossy JSON or consumption. A
selected target that already exposes `decision-request` keeps its syntax and
exact-id semantics; another target adds the syntax before advertising it.

The implementation shall update the applicable canonical CLI and REST/wire
specs in the same source change. If
`decision-request-client-observable-state-v1.md` becomes live first, this
contract supersedes its operator terminal field set only; its shared-serializer
rule remains compatible and shall call this projector.

Rollback to the prior binary is allowed only before schema activation. After
activation, deployment preflight refuses any binary that does not declare the
new schema version and complete projector before it serves reads or writes.
This fence applies even when no post-migration ruling or integrity evidence
exists because the prior projection is itself the diagnosed defect. Forward
recovery redeploys an aware binary. Rollback does not reverse the migration or
mutate history.

### 5. Observability

The existing request row, canonical condition fact, lifecycle event, wake row,
and prompt turn remain the primary trace. The immutable epoch row brackets
legacy facts. The integrity relation adds refusal evidence without duplicating
private payloads. The trace for one successful post-activation ruling shall
join:

```text
decision request id
  -> rulingFactId / escalation-ruled fact
  -> one raiser notification wake
  -> zero or one prompt turn while pending, exactly one after durable delivery
```

A legacy-complete trace joins the request to its canonical fact and exactly one
canonical ruling lifecycle event. Absence of a historical automatic wake is not
repaired or presented as proof of delivery.

The successful automatic wake lifecycle shall name `condition` as its firing
cause. Test-only wrong-name wakes can name `fallback`. The request trace shall
show the on-behalf-of actor, performing principal, and presenting-session state
as separate fields. An operator-facing inspect command may expose integrity
evidence only under existing admin visibility. Ordinary decision-request reads
do not expose integrity evidence rows.

## Acceptance

Each case uses a fresh database, fixed timestamps, deterministic transaction
barriers, and the selected target's real gateway and built CLI where named.
Impossible-shape cases use an explicit fixture-only corruption seam after clean
activation; they never falsify a live work, ruling, assignment, or completion
row.

**A-01 — Open projection.** Given one visible open operator request, when its
owner and raiser list it and fetch its exact id, then existing open fields match
their current contract, no ruling attribution is fabricated, and neither read
writes integrity evidence.

**A-02 — Ruled list/detail parity.** Given one valid ruled operator request with
known performer and session provenance, when the same authorized caller lists
all requests and fetches the exact id with no intervening mutation, then every
field from Architecture §1 is present and byte-equal. The detail response may
add `context` and `actionKey`; it does not change a parity field.

**A-03 — Request kind cannot strip fields.** Given a valid ruled operator row
and a valid ruled non-operator row, when each passes its existing visibility
predicate, then selecting `kind='operator'` does not remove `decision`,
`rationale`, `ownerUserId`, `ruledBy`, `ruledViaSessionKey`, `ruledAt`,
`rulingFactId`, `consumedAt`, or
`rulingAttribution`. A projection-level test fails if a kind-specific allow-list
omits one of them.

**A-04 — Exact-id CLI and wire.** Given the real gateway and built Rust CLI,
when an authorized caller runs `tightbeam decision-request --request <fullId>`,
then the wire request is verb `decision-request` with `params.request`, the CLI
prints the single result envelope, and exits 0. Blank ids, prefixes, positional
ids, duplicate request flags, and target flags fail. An absent or non-visible id
returns the existing `not_found` status, envelope, stderr, and nonzero exit.

**A-05 — Lifecycle and consumption state.** Given valid open, ruled, withdrawn,
and superseded operator fixtures plus a deliberately impossible stored
`consumed` operator fixture, when visible list and exact-id reads run, then open,
withdrawn, and superseded preserve their existing applicable fields; ruled
exposes null `consumedAt`; and the impossible consumed row produces the §2
integrity refusal. No valid state fabricates fields from another state.

**A-06 — Optional rationale is explicit.** Given two valid rulings, one with a
string rationale and one with stored null, when list and detail reads run, then
both contain the `rationale` key with the exact stored value. Neither serializer
omits the key or replaces null with an empty string.

**A-07 — Known dual attribution.** Given an authorized owner rule presented by
a Tightbeam session, when the ruling wins, then `ruledBy` and
`rulingAttribution.onBehalfOf` equal `user:<ownerUserId>`, the performer
principal member has state `known` and value equal to the authenticated
effective principal, and the known session key equals both
`ruledViaSessionKey` and the authenticated transport session. A role alias,
raiser, current owner session, broker, origin text, and process name cannot
replace those values.

**A-08 — Known no-session attribution.** Given an authorized direct user call
with no presenting Tightbeam session, when the ruling wins, then performer
principal is exactly `{"state":"known","value":"user:<ownerUserId>"}`
and session is exactly `{"state":"none"}` while
`ruledViaSessionKey` is null. Neither component is `legacy-unknown`.

**A-09 — Legacy attribution.** Given a pre-migration row with a valid owner,
decision, ruling time, canonical fact, and lifecycle shape but no provable
performer principal, when migration, list, exact read, replay, and consumption
inspect it, then the stored row remains byte-identical, the principal member is
`legacy-unknown`, and both reads preserve any stored `ruledViaSessionKey` as a
known session member. A second fixture with no stored session projects a
`legacy-unknown` session member. No operation copies the owner, raiser, current
caller, lifecycle prose, or wake origin into an unknown field. Each legacy
fixture's ruling fact id is at or below the immutable epoch cutoff.

**A-10 — Visitor and intermediary separation.** Given a visitor credential, a
broker user, and an intermediary session, when each attempts operator-rule
without existing owner authority, then each call retains its canonical
principal, receives the existing authorization refusal, and writes no request,
fact, event, wake, evidence, or attribution. A manual intermediary wake does
not appear as ruling performance or automatic delivery.

**A-11 — Valid label and text rulings.** Given two open requests whose options
are `[{"label":"alpha"},{"label":"beta"}]`, when the authorized owner
selects label `alpha` for one and submits non-blank text for the other, then each
transaction writes the exact normalized outcome, complete ruled shape, one
canonical fact, one lifecycle event, and one raiser notification wake. Each
fact id stored on its row resolves to kind `escalation-ruled` and scope equal to
that request id.

**A-12 — Invalid labels.** Given the same open request, when the owner submits
`gamma`, a blank label, a case-changed label, a non-string label value, blank
text, or both label and text inputs, then the existing typed input refusal
occurs before the open-row mutation. Request, fact, event, wake, evidence, and
turn counts do not change.

**A-13 — Terminal mutation race.** Given one open request, when valid rule,
withdraw, and supersede transactions wait at deterministic barriers and then
resume in every order, exactly one open-row compare-and-set wins. Only a ruling
winner creates the ruling tuple, fact, ruling event, and raiser wake. Every
loser follows the existing conflict contract and creates none of those effects.

**A-14 — Ruling replay.** Given one committed post-migration ruling, when the
authorized owner repeats the exact normalized outcome and rationale through the
same or a different presenting session, then it returns the stored valid row and
preserves the winner's attribution. The same contract applies to a
legacy-complete ruling. Counts for request mutation, condition fact, lifecycle
event, wake, and prompt turn do not increase. A changed outcome, rationale,
owner principal, or terminal verb does not qualify as that replay.

**A-15 — At-most-once automatic raiser delivery.** Given one ruling winner and
concurrent condition evaluators, fallback evaluation, scheduler restart, and
delivery replay, when all paths settle, then the database contains one raiser
notification wake and at most one prompt turn for its wake id. After delivery,
it contains exactly one committed prompt turn. The prompt matches Architecture
§3, the automatic wake records `firedBy="condition"`, and the request remains
unchanged.

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
row and separate post-activation ruled rows with a missing `rulingFactId`, no
canonical ruling lifecycle event, no canonical raiser wake, two canonical
ruling lifecycle events, and two canonical raiser wakes, when the caller lists
them, then the response is HTTP 500
`decision_request_integrity_invalid`, contains the lexicographically smallest
bad request id and no decision fields, emits no partial collection bytes, and
commits one evidence row for each bad shape. The evidence names
`rulingFactId`, `rulingLifecycleEvent`, or `raiserNotificationWake` as
applicable.

**A-19 — Detail integrity refusal.** Given separate visible post-activation
ruled rows whose fact has a wrong kind or scope, whose only ruling lifecycle
event has a wrong kind or subject, or whose only intended automatic wake has a
wrong target session, origin, prompt, consumer, condition kind, condition
scope, fact cursor, creator session, fallback deadline, target gate,
role-resolution state, or wake/firing state, when the caller fetches each exact
id, then it receives the
same named refusal and no row bytes. Evidence names `rulingFactId`,
`rulingLifecycleEvent`, or `raiserNotificationWake` under the closed failure
vocabulary and stores no fact, event, wake, or private request payload.

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

**A-23 — Migration preflight.** Given legacy-complete rows with and without a
stored session, a row missing decision, a row missing owner, a consumed operator
row, a row with a missing fact, and a row with a wrong-name fact, when migration
runs, then it classifies the legacy-complete rows without request writes,
records one evidence row per impossible shape, atomically records one epoch
whose fact cutoff equals the snapshot maximum, installs the future-write
trigger, advances the schema stamp, and activates without repairing or
disposing of a request. Authorized reads and consumers refuse only the admitted
impossible rows through §2; other gateway behavior remains available. When the
migration is invoked again, the epoch and schema stamp remain unchanged and the
evidence count does not increase. A later null-principal ruling cannot qualify
as legacy because its fact id exceeds the cutoff.

**A-24 — Rollback fence.** Given schema activation has not occurred, when the
deployment rolls back, then the prior binary resumes under the predecessor
schema stamp and request history remains unchanged; no reverse migration runs.
A failed activation transaction leaves no epoch, evidence batch, trigger, or
new schema stamp. Given the new schema is active, when an unaware old binary
attempts gateway start with zero or more new rulings and evidence rows, then
preflight refuses it and leaves all rows intact. Redeploying an aware binary
restores service.

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
Given a post-activation writer attempts a ruled insert or open-to-ruled update
with a missing or inconsistent principal, session state, or session key, then
the database trigger returns `decision_request_integrity_invalid` and the whole
writer transaction rolls back.

**A-27 — Real-response fixture and compatibility gate.** Given an unmodified
selected source revision and the candidate implementation in fresh owned
worktrees, when the implementation lane builds the release CLI, captures real
gateway responses for valid open, ruled, withdrawn, superseded, and legacy
fixtures plus hidden and impossible-consumed fixtures, and runs the target's
baseline and candidate gates, then the baseline is recorded, the candidate gate
is green, and checked-in fixtures are captured from those real responses rather
than hand-written. Existing non-operator decision-request tests remain green.

**A-28 — Trace completeness.** Given one known-attribution ruling, one legacy
ruling, one delivered raiser wake, and one integrity refusal, when an authorized
operator inspects their traces, then it can join each request to its canonical
fact and exactly one canonical ruling lifecycle event, join each
post-activation ruling to exactly one canonical wake and its prompt turn when
present, and distinguish
on-behalf-of actor, performer principal, and presenting-session state; confirm
that the automatic wake fired by condition while a test-only wrong-name wake
fell back; and find the privacy-safe evidence row. No join depends on lifecycle
prose parsing.

## Open Questions

None. Target selection, `specRef` binding, implementation, and the independent
exact-revision re-review are intentionally outside this assignment. The parent
shall open that re-review against the successor commit and file SHA after this
spec's required cold digest and spec-ready receipt.
