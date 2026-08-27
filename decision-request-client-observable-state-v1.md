# Decision-request client-observable state v1

Status: frozen candidate for fresh independent review after the required cold digest.
This file carries no implementation, target, merge, deploy, or release authority.

## Goal

Close firehose reconstruction gap G6 for a cold client. Freeze the public
decision-request status values, the public item transitions, the firehose class for
each transition, the wire version, and the identifiers that correlate each notice to
one REST row.

This amendment adds decision-request row/event schema revision 2 beside the existing
revision 1 enum. It supersedes only the claim that all decision-request rows use the
closed revision 1 enum, the decision-request row in REST R8 in
`rest-state-api-v1.md`, and the decision-request class list in firehose R2 in
`event-firehose-v1.md`.

REST R1 and the current `/api/decision-requests` routes remain in force. This
amendment does not add a REST namespace or change the REST envelope version.

## Non-Goals

- This amendment does not define the substrate's complete decision-request lifecycle
  vocabulary.
- This amendment does not define who answers, returns, rules, consumes, withdraws, or
  supersedes a request.
- This amendment does not define command inputs, authorization rules, deadlines, wake
  behavior, replacement policy, or assignment policy.
- This amendment does not add a projected actor, reason, timestamp, or successor-id
  field to the REST decision-request item.
- This amendment does not add `/api/v2` or change the REST envelope, route, field set,
  field types, or behavior of `/api/decision-requests` and
  `/api/decision-requests/:id`, except that it closes the existing decision-status
  domain over all client-observable values.
- This amendment does not change firehose recovery, visibility, or shared-serializer
  rules. It applies the existing widening rule to the decision-request row/event
  schema and fixes only the within-transaction handoff order in DR6.
- This amendment does not authorize product code, a product target, a merge, a deploy,
  or a release.
- Operating pattern taught to agents: none.

## Terms

- **Decision-request item**: the canonical `decision requests` R7 item returned by
  `GET /api/decision-requests` or `GET /api/decision-requests/:id`.
- **Public status**: the exact string in a decision-request item's `status` field.
- **Public transition**: a committed change that creates a visible decision-request
  item, changes its public status, or changes one or more other R7 fields while its
  status stays `open`, as listed in DR2.
- **State notice**: one firehose event frame with `op:"upsert"` and the
  post-transition decision-request item as its payload.
- **Resource token**: the exact string `decision requests` in the REST envelope and
  state notice.
- **Decision-request row/event schema**: revision 1 keeps the existing closed status
  enum `open|ruled|consumed|withdrawn|superseded|answered`. Backward-readable revision
  2 keeps every revision 1 row key and field type and adds `returned` to that finite
  enum. Each DR2 notice declares `schemaVersion:2`; its payload uses revision 2. The
  unchanged REST envelope declares `schemaVersion:1` under REST R1; that envelope
  version does not rename the row/event schema revision.
- **Spec revision**: `v1` in this filename identifies the first revision of this
  amendment. It does not identify the decision-request wire schema version.
- **Row identifier**: the decision-request item's `id`.
- **Correlation identifier**: `refs.decisionRequestId` in a state notice.
- **Replacement request**: a distinct decision-request item whose creation makes an
  open effort request become `superseded`. This amendment does not project the
  relationship between the two items.

## Assumptions

1. REST R4, R7, AU4, and SR1 already define the decision-request envelopes,
   closed-world item fields, visibility, and shared REST/firehose serializer.
2. Firehose V3 through V5 already define committed publication, `rowVersion`, and
   last-version-wins client application.
3. A successful public transition increments the item's `rowVersion` in the same
   commit as the item change.
4. The public `kind` values remain `statute`, `effort`, and `agent`.
5. The public row can expose a status without exposing the internal action that caused
   it. A client uses the status and the existing projected fields.

Closure choice: ADD wins because deleting the decision-request read resource removes
required shared state, while accepting the unmapped changes prevents live maintenance
and reconnect rebuild from agreeing.

## Invariants

DR1. Under decision-request row/event schema revision 1, the public status domain is
the closed set `open`, `answered`, `ruled`, `consumed`, `withdrawn`, and `superseded`.
Under revision 2, the public status domain is the closed set `open`, `answered`,
`returned`, `ruled`, `consumed`, `withdrawn`, and `superseded`. The shared serializer
rejects a status outside the enum for the selected revision and rejects an unknown
revision. It emits no partial REST item or state notice after either rejection. [AC1]

DR2. The public transition graph contains exactly these edges and creation:

| Prior public status | Resulting public status | Request kind | Public item change | Firehose class |
|---|---|---|---|---|
| no item | `open` | `statute`, `effort`, or `agent` | item created | `decision_request.opened` |
| `open` | `open` | `effort` | one or more non-status R7 fields change | `decision_request.updated` |
| `open` | `answered` | `agent` | status changes | `decision_request.answered` |
| `open` | `returned` | `agent` | status changes | `decision_request.returned` |
| `open` | `ruled` | `statute` or `effort` | status changes | `decision_request.ruled` |
| `ruled` | `consumed` | `statute` or `effort` | status changes | `decision_request.consumed` |
| `open` | `withdrawn` | `statute`, `effort`, or `agent` | status changes | `decision_request.withdrawn` |
| `open` | `superseded` | `effort` | status changes | `decision_request.superseded` |

The transition seam leaves the row unchanged when a requested status change is outside
this table. A same-status write that produces byte-equal R7 fields is not a public
transition. [AC2]

DR3. One transition operation derives the class from the actual prior and resulting
public items and commits the resulting row. After commit, it hands the matching state
notice to the existing best-effort firehose path. A rollback hands off no notice. [AC2]

DR4. Each DR2 class has this exact mapping:

| Property | Value |
|---|---|
| `schemaVersion` | `2` |
| `resource` | `decision requests` |
| `op` | `upsert` |
| primary ref key | `decisionRequestId` |
| primary ref value | the post-transition item's `id` |
| payload | the exact post-transition R7 decision-request item |

The payload `id`, `status`, and `rowVersion` equal the values returned by an authorized
detail read for the correlation identifier after the transition. The REST list and
detail envelopes at `/api/decision-requests` keep `schemaVersion:1` and the canonical
`decision requests` resource token. A producer emits every DR2 notice with
`schemaVersion:2`; that value identifies the backward-readable decision-request
row/event schema, not a REST API version. [AC3]

DR5. While a connection stays healthy through the existing post-commit handoff, one
committed DR2 transition produces one state notice for each active subscription whose
filters match and whose principal can read the post-transition item. A retry that
leaves the item unchanged produces no new state notice. A failed post-commit handoff
keeps the existing best-effort recovery contract. [AC4, AC5]

DR6. One state transaction creates the new open request row and changes the prior open
effort request to `superseded`. Both row effects commit or neither commits. No REST
read or notice handoff can observe a state in which only one row effect committed.
Only after commit, the existing non-durable best-effort path hands off
`decision_request.superseded` for the prior row before
`decision_request.opened` for the new row. Each notice carries its own row's
correlation identifier and post-transition payload. A crash can lose both notices;
the client rebuilds both rows from the canonical REST snapshot. [AC6]

DR7. A decision-request-row/event-schema-version-2 client applies a state notice by
the pair `(payload.id,payload.rowVersion)`. After a reconnect or an unknown
decision-request class with a supported schema version, the client discards cached
decision-request state and rebuilds it from `/api/decision-requests` under the
existing firehose recovery rules. A client that does not support the received
`schemaVersion` discards cached decision-request state, reports the unsupported
version, and waits for a compatible decoder before it applies another decision-request
snapshot or notice. [AC7]

DR8. The amendment does not require a client to infer a transition from timestamps,
actor fields, reasons, wake events, assignment events, or elapsed time. The class and
post-transition payload report the observable event directly. [AC8]

## Architecture

The decision-request public-state mapping is one closed registry seam. Each DR2 row
selects the class, fixed schema version, fixed resource, fixed operation, primary ref
key, and existing R7 serializer. REST list/detail responses and firehose payloads call
that same serializer.

The public item transition is the event. The implementation compares the prior and
resulting R7 items. It selects the DR2 class from that difference, not from a timer,
wake, actor, or command name. The existing firehose path receives the committed
post-transition item after commit and keeps its current best-effort delivery contract.

The G6 client model has seven states and eight creation/transition classes. Internal
states, internal actions, and same-status changes that leave the R7 item byte-equal stay
outside this amendment. A future public status or public edge requires a reviewed
amendment to DR1 and DR2 before a producer emits it.

Decision-request row/event schema revision 2 owns the seven-value decision-request
status domain and the eight DR2 classes. It is backward-readable: a revision 2 decoder
accepts every revision 1 row, while a revision 1 decoder rejects `returned` and an
unknown notice schema version. The firehose frame uses `schemaVersion:2` so a client
can select that event vocabulary. REST keeps its R1 `schemaVersion:1` envelope and
current unversioned route; no REST API v2 or negotiation mechanism is added.

One mutation seam owns the public item transition: the decision-request transition
function that validates DR2, increments `rowVersion`, and hands the committed item and
selected class to the existing post-commit publisher.

## Acceptance

AC1 — Public enum closure (DR1)

- Given seven authorized detail fixtures whose statuses cover `open`, `answered`,
  `returned`, `ruled`, `consumed`, `withdrawn`, and `superseded`, when a client decodes
  each response under row schema revision 2 from
  `GET /api/decision-requests/:id`, then each envelope has
  `schemaVersion:1`, resource `decision requests`, the unchanged R7 key and type set,
  and one accepted public status.
- Given a revision 1 fixture with status `returned`, a revision 2 fixture with status
  `paused`, or a fixture that selects unknown revision 3, when REST or the firehose
  serializer reads it, then serialization fails and no partial item or state notice
  is emitted.

AC2 — Transition and atomicity matrix (DR2, DR3)

- Given a fixture for each DR2 row, when the named item change commits, then the row has
  the resulting public item and the post-commit handoff names the matching class and
  committed `rowVersion`.
- Given a transaction failure before commit, when the client reads REST and the
  firehose, then it observes neither the resulting row version nor its state notice.
- Given an open effort request whose public `lineageRung`, expecter, deadline, options,
  or context changes, when the resulting R7 item commits, then the handoff names
  `decision_request.updated` and carries the higher `rowVersion`.
- Given an `answered` agent request, when a caller attempts to change it to `ruled`,
  then the mutation is rejected and its public item is unchanged.

AC3 — Event-to-row correlation (DR4)

- Given a committed `open` to `returned` transition for `dr_123` at row version 9,
  when an authorized client receives the notice and fetches
  `GET /api/decision-requests/dr_123`, then the notice has class
  `decision_request.returned`, `schemaVersion:2`, resource `decision requests`, op
  `upsert`, `refs.decisionRequestId:"dr_123"`, and a payload byte-equal to the detail
  item with `id:"dr_123"`, `status:"returned"`, and `rowVersion:9`; the detail envelope
  has `schemaVersion:1` and resource `decision requests`.

AC4 — Visibility (DR5)

- Given a connection that stays healthy through post-commit handoff and two matching
  subscriptions where one principal can read `dr_123` and the other cannot, when
  `dr_123` moves from `open` to `withdrawn`, then the authorized subscription receives
  one correlated notice and the other subscription receives no frame that identifies
  the row.

AC5 — Idempotent retry (DR5)

- Given `dr_123` is already `returned` with the same accepted result, when the caller
  retries that operation, then `rowVersion` stays unchanged and no second state notice
  is emitted.

AC6 — Replacement rows (DR6)

- Given open effort request `dr_old`, when replacement creation fails before its
  transaction commits, then `dr_old` remains `open`, `dr_new` is absent, and no
  replacement notice is handed off.
- Given the replacement process crashes before commit, when recovery and REST reads
  run, then `dr_old` remains `open`, `dr_new` is absent, and neither replacement
  notice is handed off.
- Given the replacement process crashes after commit but before fan-out, when the
  service restarts, then REST exposes both committed row effects and no notice recovery
  occurs; a fresh REST snapshot reconstructs both rows.
- Given open effort request `dr_old` and a matching subscription whose connection stays
  healthy through both post-commit handoffs, when creation of `dr_new` commits, then
  one REST snapshot can observe only the pair `dr_old.status:"superseded"` and
  `dr_new.status:"open"`; the client receives `decision_request.superseded` correlated
  to `dr_old` before `decision_request.opened` correlated to `dr_new`, and each payload
  equals its own REST detail item.

AC7 — Rebuild convergence (DR7)

- Given a schema-version-2 client misses, duplicates, or reorders decision-request
  notices, when it follows the existing recovery rule and rebuilds from REST, then its
  map keyed by decision-request `id` equals a fresh REST snapshot and subsequent higher
  `rowVersion` notices converge by last-version-wins.
- Given a schema-version-1 client receives a decision-request frame with
  `schemaVersion:2`, when it cannot decode version 2, then it discards its cached
  decision-request map, reports schema version 2 as unsupported, and applies no
  decision-request snapshot or notice until it has a version-2 decoder.

AC8 — Direct event detection (DR8)

- Given an `open` request whose deadline passes without a committed status change,
  when a client observes firehose traffic, then it receives no decision-request state
  notice for elapsed time alone.

Traceability is two-way: DR1 through DR8 cite their acceptance clauses, and AC1 through
AC8 cite the requirements they verify. The registry seam in Architecture traces only
to DR2 through DR5.

## Open Questions

None. This candidate has no blocking or non-blocking holes.
