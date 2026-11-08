# Firehose archetype filter v1 (amendment to event-firehose-v1)

Status: PROPOSED r3, 2026-11-07. Candidate amendment to reviewed r2
(SHA-256 2dc7f2ee001a70ca03f66bf91f357cb4a7d83cf3aab1691c34892b1eff3c424f).
PO ruling att_84f10f88 / art_c8632d13 (SHA-256
42ee92e151cac9e68d1d126063b7aab3af0464d0f9fc9d4bc518b6a7d969bc93)
authorizes only target metadata, Current behavior, AF8 and AF9 corrections.
r3 awaits independent review and rebinding; r2 remains bound until then.
Amends `event-firehose-v1.md` CANONICAL r6 as
read at tightbeam-specs `origin/main` d64e38379e6ac55eece2ecf6faea3599c996c7bc
(SHA-256 e49fe7eefa3f15268383c567ed2f0946e1b32a443569e5d3afdb5e29d3feed1b).
It relies on `rest-state-api-v1.md` CANONICAL r4 at the same commit (SHA-256
a3d6a5c48e7457c97171249bf9084ff1017a95fa63f8f3b2e54b8d571b1b1d5a). Target:
private feature branch based on code `0.1.15` commit
0e6ee588db77ea8c82747116b3a3f422f2dc3805, tree
f87acffb32ffbe0bede599c7ae87c1c058bc3d82. This is the source baseline,
not an integration destination; no PR, push, merge, release or live action
is authorized. Current behavior below was read from that exact commit.

Header paragraph to add to `event-firehose-v1.md`, beside the other
successors:

> Archetype filter amendment, 2026-10-28: PROPOSED. Add the optional
> `archetype` subscription filter, which matches notices about every session
> of one archetype, including sessions spawned after the subscription began.
> The exact behavior contract is `firehose-archetype-filter-v1.md`; its AF
> labels are cited here as defined there. It adds no class, ref, envelope,
> payload field, visibility grant, or source-invalidation mapping.

The normative requirements in this document use RFC 2119 keywords as clarified
by RFC 8174, and EARS sentence forms.

## Spirit

Source: the PO outcome on the work item and its topology plan (plan artifact
SHA-256 b6779f6975e079377e860982507644f840f5a9d567d1184df4a153693e2092c6).

- Mike asked whether Firehose is one stream of every change that filters only
  narrow. His examples were "only show me tool calls from agent x" and
  "messages and tool calls from PO agents". Asked whether the Gateway should
  add a role filter, he answered "Yes".
- Outcome (Q1): "one Firehose subscription can ask for, for example, messages
  and tool calls from every product-owner session. It includes sessions
  spawned after the subscription started, without re-subscribing."
- Q2: "The filter combines with the existing class and session filters."
- Q3: "Matching REST reads take the same filter if the Firehose contract has
  them."
- Q4: "Scope is the filter only: no new security or visibility rules." Chat
  is the first consumer.
- Firehose principles this amendment keeps: G2 ("filters narrow delivery for
  one subscriber only"), P3 (missed notices are harmless; rebuild is the one
  recovery path), and the 2026-10-26 ruling that nothing refuses or fails
  unless the operator asked.

## Decision: archetype, not role binding

The filter matches by **archetype**. It does not match role names or role
bindings. Reason, checked against the source and the live org on 2026-10-28:

- A role (`roles` row: `name`, `boundSessionKey`, `ownerUserId`) names one
  bound session. "Every product-owner session" is a category, and a role is
  not one. An exact role name selects one session, which the `sessionKey`
  filter already does (Mike's "agent x" case).
- Role names have no category field. Prefixes such as `product-owner:` are a
  naming convention only (`Tightbeam.Roles` name pattern). In the live org a
  product-owner-archetype session holds no role at all, and a
  `product-owner:`-prefixed role is bound to an orchestrator-archetype session.
  A role-prefix filter would miss the first and include the second.
- Archetype (`sessions.archetype`, NOT NULL) is the session's declared kind.
  It is set at spawn, changed only by the AF5 repoint path, present on every
  session, and already a public field of the R7 session item and a
  whitelisted REST sessions filter (REST R6). It is what "PO agents" means.

Matching on both was rejected: a second mechanism with different results for
the same words would leave two live patterns for one concept.

## Terms

- **Archetype filter**: the `archetype` field of a subscribe frame's `filters`.
- **Subject session** of a notice: the session named by the notice's
  `refs.sessionKey`. A notice with no `refs.sessionKey` has no subject session.
- **Session archetype**: the `archetype` value of the subject session's
  committed session row, the same value the R7 session item serves.
- **Matching instant**: the moment the gateway decides whether one notice
  matches one subscription.

## Current behavior (from source, 0.1.15 0e6ee588)

Source: exact commit and tree above, `lib/tightbeam/firehose/hub.ex`,
`lib/tightbeam/wire/change_socket.ex`, `lib/tightbeam/firehose/rebuild.ex`,
and `lib/tightbeam/wire/router.ex`; interpretation follows PO ruling
att_84f10f88 / art_c8632d13 and Q4.

- `Tightbeam.Wire.ChangeSocket` accepts filter keys `classes`, `sessionKey`,
  `workItemId`, `origin`, `principal`. Unknown keys fail with
  `invalid_request` "invalid filters". `classes` takes a list of strings;
  each other value must be a string or null.
- `Tightbeam.Firehose.Hub.matches?/2` matches `classes` by prefix and each
  other key by literal equality with the same-named notice ref, conjunctively.
  Matching is used for normal fan-out, the session-class commit probe,
  pending subscriptions, and subscribe-time notices.
- Live Hub delivery and ChangeSocket make no per-connection notice visibility
  decision. Hub retains its existing revocation handling and secret-payload
  guard; ChangeSocket sends received live frames without a visibility
  recheck. Subscribe-time active-turn notices likewise have no visibility
  gate. The visibility-before-archetype obligation in AF8 therefore does not
  introduce a visibility decision on any of those live paths.
- Ingress overflow, `overflow_targets`, and its test are removed on this
  base. The existing per-socket outbound backlog boundary remains: overflow
  sends `:firehose_overflow` to the affected socket and ChangeSocket closes
  it with 4008. AF9 does not restore an ingress queue or overflow selector.
- An operator-selected session connection requires `filters.sessionKey` to
  equal its selected session.
- Subscribe-time active-turn notices (`turn.queued`, `turn.started`) are built
  only when `filters.sessionKey` is given, and pass through the matcher.
- `GET /api/sessions` accepts only `asUser`, `limit`, `before`, `after`, and
  `tail`; any other query key returns `400 invalid_filter`. REST R6 already
  lists `archetype` among the sessions collection's V1 whitelist filters, so
  AF10 still requires serving that matching REST filter. REST retains its
  existing visibility scope; `Firehose.Rebuild` also retains its visibility
  decision. Neither establishes visibility gating for live Hub delivery.
- The older visibility-ordering gap described in the retained non-goals is
  historical to the r2 baseline, not authority to add or reorder visibility
  on this base. The earlier archetype intent question Q-A is resolved by
  PO att_448f2e31, reaffirmed by att_84f10f88; the retained question text
  does not reopen that decision.

## Requirements

AF1. Subscribe field. (Q1, ruling "Yes")
The subscribe frame's `filters` object SHALL accept an optional `archetype`
field whose value is a string or `null`. `null` or absence imposes no
archetype constraint. A value of any other JSON type SHALL fail the subscribe
the same way any invalid filter value fails today (`invalid_request`). The S1
example and S2 field list gain `archetype`.

Acceptance: `{"classes":["message.created"],"archetype":"product-owner"}`
receives `subscription_ready`; `{"archetype":7}` receives the existing
`invalid_request` invalid-filters error; `{"archetype":null}` behaves as no
filters.

AF2. Match rule. (Q1)
When a subscription has a string archetype filter, the gateway SHALL treat a
notice as matching that field if and only if the notice has a subject session
and the session archetype equals the filter value exactly (equal code points:
no trimming, case folding, prefix, or pattern match). A notice with no subject
session SHALL NOT match. The archetype filter therefore selects exactly the
notices that a `sessionKey` filter naming some session of that archetype would
select.

Acceptance: with filter `archetype:"product-owner"`, a `message.created`
notice whose `refs.sessionKey` names a product-owner session matches; one
naming a coder session does not; a `topline.created` notice (no
`refs.sessionKey`) does not.

AF3. Sessions spawned later. (Q1: "includes sessions spawned after the
subscription started, without re-subscribing")
The gateway SHALL evaluate the session archetype at the matching instant from
committed session state, never from a set of sessions captured when the
subscription was made. When a session of the filtered archetype is spawned
after `subscription_ready`, its `session.spawned` notice and every later
notice whose subject session it is SHALL match, with no new subscribe.

Acceptance (the required end-to-end test): subscribe with
`{"classes":["message.created","tool_call."],"archetype":"product-owner"}`
and receive `subscription_ready`. Then spawn a new product-owner session and
a new coder session, and give each a turn that writes a message and a tool
call. The subscription receives the product-owner session's `message.created`
and `tool_call.*` notices and none of the coder session's, without
unsubscribing or resubscribing.

AF4. Retirement and role changes. (Q1)
Retiring a session SHALL NOT change whether its notices match; its
`session.retired` notice matches the archetype filter of its archetype.
Binding, rebinding, or releasing a role SHALL NOT change which notices an
archetype filter matches.

Acceptance: retiring a product-owner session delivers its `session.retired`
to an `archetype:"product-owner"` subscription with classes `session.`;
rebinding a role from that session to a coder session changes no delivery.

AF5. Archetype change of an existing session. (Q1)
When a session's archetype changes (the existing repoint path, permitted only
for retired sessions and for main or built-in sessions), each notice matched
after that change commits SHALL be matched against the resulting archetype.
The session's own `session.updated` notice for that change is matched against
the resulting archetype. A subscriber to the prior archetype receives no
notice that the session left; see the marked hole H1.

Acceptance: a retired session repointed from `coder` to `reviewer-code`
emits `session.updated`; an `archetype:"reviewer-code"` subscription with
classes `session.` receives it, and an `archetype:"coder"` subscription does
not.

AF6. Composition. (Q2)
The archetype filter SHALL be conjunctive with `classes`, `sessionKey`,
`workItemId`, `origin`, and `principal` under S2. Each subscription on a
connection is matched independently, as today (A3).

Acceptance: `{"classes":["tool_call."],"archetype":"product-owner",
"sessionKey":K}` delivers only K's tool-call notices when K is a
product-owner session, and nothing when K is a coder session.

AF7. No refusal for unknown names. (2026-10-26 ruling)
The gateway SHALL NOT refuse a subscribe because no session, or no archetype
definition, has the given archetype. Such a subscription matches nothing
until a session with that archetype exists, after which AF3 applies.

Acceptance: subscribing with `archetype:"no-such-archetype"` receives
`subscription_ready` and no notices.

AF8. No new visibility or authority. (Q4, G2, REST AU6;
PO ruling att_84f10f88 / art_c8632d13)
The archetype filter SHALL only narrow delivery for its own subscription,
wherever the existing filters apply: normal fan-out, the session-class
commit path, pending subscriptions, and subscribe-time notices. It SHALL NOT
add a notice that the existing filters would not deliver. It is a subscription
filter under REST AU6, which gains `archetype` in its list of filters.
The amendment SHALL NOT introduce a live visibility decision; the current
Hub and ChangeSocket have none. Existing revocation, secret-payload and
connection rules remain unchanged.

Where an existing visibility decision applies, the archetype test, including
any lookup specifically for that test, SHALL apply only to rows that decision
has already allowed. On this base that obligation and its lookup-trace
acceptance apply to the AF10 REST read, not to live Firehose paths. The choice
of how to read the archetype is left to implementation; AF3 still requires
committed session state at the matching instant, never a subscription-time
snapshot of matching sessions.

The operator-selected session rule (`sessionKey` must equal the selected
session) is unchanged, and an archetype filter neither replaces nor relaxes
it. Subscribe-time active-turn notices remain gated on `filters.sessionKey`
as today; an archetype filter alone adds none.

Acceptance: adding `archetype:"product-owner"` to an existing live
subscription retains exactly its otherwise-deliverable notices whose subject
sessions are product-owner sessions, including later-spawned and unbound
sessions, without introducing a live visibility check. For
`GET /api/sessions?archetype=product-owner`, an authenticated non-admin user
receives only product-owner sessions allowed by the existing REST AU4
visibility decision; a test double or lookup trace shows no archetype lookup
for filtering a row that decision excluded. This trace does not prohibit the
existing row read needed to decide visibility. An operator-selected connection
subscribing with only `archetype` set gets the existing
"sessionKey must match selected session" refusal; an archetype-only
subscription gains no subscribe-time active-turn notices.

AF9. Ingress-overflow targeting retired on this base. (D3, P3;
PO ruling att_84f10f88 / art_c8632d13)
The r2 ingress-overflow targeting requirement is retired for the stated
0.1.15 base: that path no longer exists and SHALL NOT be reintroduced by
this amendment. The archetype filter SHALL NOT create a new silent-drop path
for an otherwise-deliverable matching notice beyond the existing delivery
behavior. The existing per-socket backlog overflow SHALL continue to close
the affected socket with 4008, so the client reconnects, resubscribes and
rebuilds under P3. This requires no new overflow mechanism or stronger
delivery guarantee than the existing contract.

Acceptance: an `archetype:"product-owner"` subscription receives its matching
notices under normal fan-out. When matching notices overflow that socket's
existing outbound backlog boundary, the affected socket closes with 4008
and can reconnect and rebuild using AF10/AF11. Source inspection confirms
that the amendment adds no ingress-overflow queue or selector. The retired
r2 forced-ingress-overflow acceptance does not apply to this base.

AF10. Matching REST read. (Q3)
`GET /api/sessions` SHALL accept the `archetype` query filter that REST R6
already whitelists, with REST R6's general rules: exact code-point equality,
repeated values disjunctive, conjunctive with other accepted filters, AU4
visibility applied first, and an unmatched value returns an empty collection
rather than an error. Under REST R5 the page cursor SHALL bind the filter, so a
cursor reused with a different `archetype` set returns `400 invalid_cursor`.
No other R6 sessions filter is in scope.

Acceptance: `GET /api/sessions?archetype=product-owner` returns exactly the
visible sessions whose `archetype` is `product-owner`, in R5a order;
`?archetype=product-owner&archetype=coder` returns both kinds;
`?archetype=no-such` returns `200` with no items; a cursor from the first
request reused with `?archetype=coder` returns `400 invalid_cursor`.

AF11. Rebuild for an archetype subscription. (P3, M1, M2)
A client holding an archetype-filtered subscription SHALL rebuild under M1/M2
by listing the archetype's sessions through AF10 and then reading each
displayed session's existing per-session reads (messages, tool calls). This
adds no cross-session messages or tool-calls read.

Acceptance: documentation check only; the M4 recipe gains this sentence.

## Invariants

- I1. The filter adds no notice class, ref, payload field, envelope field, or
  REST item field. Notices for matching sessions are byte-identical to those
  an unfiltered subscriber receives. (Q4)
- I2. The filter is a delivery narrowing per subscription only. It never
  grants, widens, or hides visibility. (Q4, G2)
- I3. R8b's sentence "the matcher derives no ref or filter value from an
  owner, mutation actor, authenticated principal, or other row" is amended to
  except exactly one derivation: the session archetype of the subject session,
  for AF2. No other derived match is added. (AF2)

## Assumptions (falsifiable)

- A1. Every notice that concerns a session's messages, tool calls, turns,
  wakes, or session state carries that session in `refs.sessionKey`. If a
  class Mike's example needs (`message.created`, `tool_call.started`,
  `tool_call.ended`) lacks it, AF2 does not cover it.
- A2. A session's row is committed before any notice whose subject session it
  is reaches the matcher (D2: commit, then hand-off). If not, a
  just-spawned session's first notice could miss under AF3.
- A3. Archetype changes only through the existing repoint path, and only for
  retired, main, or built-in sessions (`Tightbeam.Org.repoint_archetype_in_txn`).

## Non-goals

- Filtering by role name, role binding, or role-name prefix.
- Lists of archetypes in one subscription filter. A client wanting two
  archetypes opens two subscriptions (S5 allows 100).
- Filtering by message author within a session. The filter selects by session,
  as `sessionKey` does; a message's `role` field already tells who wrote it.
- Any new visibility, security, authorization, or refusal rule.
- Any other REST R6 sessions filter (`state`, `role`, `harness`, and so on), and
  any cross-session messages or tool-calls collection.
- Subscribe-time active-turn notices for archetype-only subscriptions.
- History, replay, or notification to a prior-archetype subscriber.
- Reordering the existing filters (`classes`, `sessionKey`, `workItemId`,
  `origin`, `principal`) to run after visibility. That pre-existing AU6
  conformance gap belongs to the Firehose owner, not to this amendment.

## Coupled set

Spec homing couples `event-firehose-v1.md`, `rest-state-api-v1.md`, and
`rest-state-api-v1-wire-schema.md` for filter-value changes. This amendment
changes the Firehose S1/S2 filter set. In `rest-state-api-v1.md`, the AU6
list of subscription filters gains `archetype` (AF8); R6 already lists
`archetype` for sessions, so AF10 needs no REST text. The wire schema defines
no subscribe filter or sessions query parameter and needs no change.

## Marked holes

- H1 (NON-BLOCKING). A subscriber to a session's prior archetype is not told
  when that session's archetype changes. This affects only retired, main, and
  built-in sessions. Such a client recovers by an M2 rebuild. Not specified
  further.

## Open questions

- Q-A (NON-BLOCKING, PO intent confirmation). Mike's wording was "role
  filter" and "PO agents". This contract reads that as the session's
  archetype, for the reasons in "Decision". Matching role names would select
  single bound sessions, not categories, and in the live org would miss a
  product-owner session that holds no role. The PO is asked to confirm that
  archetype is what Mike meant. If the PO instead wants role-name matching,
  this contract is replaced, not amended.
