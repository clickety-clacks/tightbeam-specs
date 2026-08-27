# Decision-request client-observable state v1

Status: frozen candidate for independent review after the required cold digest. This
file carries no implementation, target, merge, deploy, or release authority.

## Goal

Close firehose reconstruction gap G6 for a cold client. Freeze the public
decision-request status values, the public item transitions, the firehose class for
each transition, and the identifiers that correlate each notice to one REST row.

This amendment supersedes only these existing clauses:

- the decision-request status enum in `rest-state-api-v1-wire-schema.md`;
- the decision-request row in REST R8 in `rest-state-api-v1.md`; and
- the decision-request class list in firehose R2 in `event-firehose-v1.md`.

The other clauses in those files remain in force.

## Non-Goals

- This amendment does not define the substrate's complete decision-request lifecycle
  vocabulary.
- This amendment does not define who answers, returns, rules, consumes, withdraws, or
  supersedes a request.
- This amendment does not define command inputs, authorization rules, deadlines, wake
  behavior, replacement policy, or assignment policy.
- This amendment does not add a projected actor, reason, timestamp, or successor-id
  field to the REST decision-request item.
- This amendment does not change firehose recovery, ordering, visibility, envelope,
  versioning, or shared-serializer rules.
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
- **Resource token**: the exact string `decision-requests` in the REST envelope and
  state notice.
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

DR1. The public status domain is the closed set `open`, `answered`, `returned`,
`ruled`, `consumed`, `withdrawn`, and `superseded`. The shared serializer rejects a
row with another status and emits no partial REST item or state notice. [AC1]

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
| `resource` | `decision-requests` |
| `op` | `upsert` |
| primary ref key | `decisionRequestId` |
| primary ref value | the post-transition item's `id` |
| payload | the exact post-transition R7 decision-request item |

The payload `id`, `status`, and `rowVersion` equal the values returned by an authorized
detail read for the correlation identifier after the transition. The REST list and
detail envelopes use the same `decision-requests` resource token. [AC3]

DR5. One committed DR2 transition produces one state notice for each active
subscription whose filters match and whose principal can read the post-transition
item. A retry that leaves the item unchanged produces no new state notice. [AC4, AC5]

DR6. Creation of a replacement request produces its own
`decision_request.opened` notice. Superseding the prior effort request produces a
separate `decision_request.superseded` notice whose correlation identifier names the
prior row. [AC6]

DR7. A client applies a state notice by the pair `(payload.id,payload.rowVersion)`.
After a reconnect or an unknown class/schema/version, the client discards affected
cached decision-request state and rebuilds it from REST under the existing firehose
recovery rules. [AC7]

DR8. The amendment does not require a client to infer a transition from timestamps,
actor fields, reasons, wake events, assignment events, or elapsed time. The class and
post-transition payload report the observable event directly. [AC8]

## Architecture

The decision-request public-state mapping is one closed registry seam. Each DR2 row
selects the class, fixed resource, fixed operation, primary ref key, and existing R7
serializer. REST list/detail responses and firehose payloads call that same serializer.

The public item transition is the event. The implementation compares the prior and
resulting R7 items. It selects the DR2 class from that difference, not from a timer,
wake, actor, or command name. The existing firehose path receives the committed
post-transition item after commit and keeps its current best-effort delivery contract.

The v1 client model has seven states and eight creation/transition classes. Internal
states, internal actions, and same-status changes that leave the R7 item byte-equal stay
outside this amendment. A future public status or public edge requires a reviewed
amendment to DR1 and DR2 before a producer emits it.

One mutation seam owns the public item transition: the decision-request transition
function that validates DR2, increments `rowVersion`, and hands the committed item and
selected class to the existing post-commit publisher.

## Acceptance

AC1 — Public enum closure (DR1)

- Given seven authorized detail fixtures whose statuses cover `open`, `answered`,
  `returned`, `ruled`, `consumed`, `withdrawn`, and `superseded`, when a client decodes
  each response, then each response contains one accepted public status.
- Given a stored fixture with status `paused`, when REST or the firehose serializer
  reads it, then serialization fails and no partial item or state notice is emitted.

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
  `decision_request.returned`, resource `decision-requests`, op `upsert`,
  `refs.decisionRequestId:"dr_123"`, and a payload byte-equal to the detail item with
  `id:"dr_123"`, `status:"returned"`, and `rowVersion:9`; the detail envelope also has
  resource `decision-requests`.

AC4 — Visibility (DR5)

- Given two matching subscriptions where one principal can read `dr_123` and the other
  cannot, when `dr_123` moves from `open` to `withdrawn`, then the authorized
  subscription receives one correlated notice and the other subscription receives no
  frame that identifies the row.

AC5 — Idempotent retry (DR5)

- Given `dr_123` is already `returned` with the same accepted result, when the caller
  retries that operation, then `rowVersion` stays unchanged and no second state notice
  is emitted.

AC6 — Replacement rows (DR6)

- Given open effort request `dr_old`, when creation of `dr_new` supersedes it, then the
  client receives one `decision_request.superseded` notice correlated to `dr_old` and
  one `decision_request.opened` notice correlated to `dr_new`; each payload equals its
  own REST detail item.

AC7 — Rebuild convergence (DR7)

- Given a client misses, duplicates, or reorders decision-request notices, when it
  follows the existing recovery rule and rebuilds from REST, then its map keyed by
  decision-request `id` equals a fresh REST snapshot and subsequent higher
  `rowVersion` notices converge by last-version-wins.

AC8 — Direct event detection (DR8)

- Given an `open` request whose deadline passes without a committed status change,
  when a client observes firehose traffic, then it receives no decision-request state
  notice for elapsed time alone.

Traceability is two-way: DR1 through DR8 cite their acceptance clauses, and AC1 through
AC8 cite the requirements they verify. The registry seam in Architecture traces only
to DR2 through DR5.

## Open Questions

None. This candidate has no blocking or non-blocking holes.
