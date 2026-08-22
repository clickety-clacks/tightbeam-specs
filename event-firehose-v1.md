# Event firehose v1 — state-change notifications over ws (product spec, r6)

Status: DRAFT r6, 2026-08-22. r6 folds the adjudicated Sol review-gate
findings (review-gate-observability-2026-08-21.md): row versions +
always-upsert (F7), seq heartbeat (F6), revocation closes sockets (F12),
visibility-change rebuild (F11), pre-delete authorization (F18), class
mapping table (F2), mutation classes (F3), composed-view refetch rule
(F4), op:"observe" (F5), read-marker verb semantics (F10), refs id law
(F17), protocolVersion at upgrade (F19), in-band auth like the chat
socket (F20 — Mike's catch: no tickets, the existing protocol already
solves it). r5: r5 folds the tb02 adjudication of recon
wi_9239a7f1's report (rest-state-api-recon.md on the NFS; adjudication in
rest-vs-cli-adjudication.md r2): V3 now means canonical public
projections, never raw rows (the db stores credentials); notices carry
resource + op with delete tombstones; message.created joins the registry;
verb/lifecycle/rail classes are marked observational-only, outside the
rebuildable-state contract. r4.2: r4.2 (lavish review): M1 hardened —
subscribe-first is normative and the model-build algorithm SHALL be
idempotent under duplicates; REST-vs-CLI recon carded and staffed (see
P5). r4.1: read markers RULED into the spec
(§Read markers) — user-scoped substrate rows, changes broadcast as
read_marker.updated. r4 was a rescoping fold of Mike's state-model
ruling (2026-08-21): the EVENTS are not the entity — the TIGHTBEAM STATE
MODEL is. The ws exists only to tell a client that an aspect of the state
db changed. There is NO way to fetch previous events from the socket:
missing notices does not matter, because a fresh or reconnecting client
rebuilds its model from the query surface and subscribes to stay current.
This deletes replay, cursors, tail, history pages, epochs, event storage,
and retention — most of r2/r3's machinery. Untargeted (0.2.0 or later).
When build work starts it branches from main tip.

Revision history: r3.1 multiplexed subscriptions; r3 freshness-not-truth +
retention; r2.1 client workflows; r2 the nine r1 review comments; r1 the
firehose rescope of the archived focused design. Their carried-forward
content is restated here; anything absent from r4 is superseded.

Authority and inputs:
- Mike's state-model ruling (2026-08-21, ruled in review): "the events
  aren't important, the tightbeam state model is, and ws is really only
  there to tell you when an aspect of the state db has changed... a fresh
  client would rebuild up to the current point and use a sub to keep the
  model updated." A subscription starts feeding at the point of
  subscription; previous events are fetched nowhere — history is the
  query surface's job.
- Mike's earlier rulings, still in force: the stream is part of the
  observability layer alongside CLI reads and direct ro state-db queries
  (2026-08-20); auth is the requesting user's existing gateway credential,
  no capability keys, localhost/tailscale deployment (2026-08-20); notice
  payloads carry the changed row in full, unredacted (r1 comment);
  subscriptions are multiplexed on one connection, each with its own
  filters (r3.1 comment); the class vocabulary is enumerated in-doc (r1
  comment).
- Companion recon wi_9fdc0c07 (client buildability): with the socket
  carrying no history at all, the query surface is the ONLY path to the
  past. The recon proves a Clawline-class chat client stands on queries
  plus this subscription — its gaps are blocking findings against the
  query surface.
- Superseded input: the archived focused design and draft (specs repo
  archive/) contributed the durable-row/cursor/pump replay machinery that
  r4 removes. observability-v1.md r4's doorbell contract ("frames are
  best-effort doorbells; reads recompute") is no longer merely
  complementary — this spec generalizes exactly that contract to the whole
  state model on a dedicated endpoint; observability-v1 remains authority
  for the existing chat wire's doorbells.
- Related card: wi_bdf9a537 (gateway behind tailscale serve) — transport
  posture this endpoint would inherit.

## Position — the state model is the entity

P1. Tightbeam's truth is the state db: durable rows, queryable. A client's
job is to hold a model of the slice it displays, built from the query
surface (CLI verbs, HTTP reads: transcript, toplines, work-item and
assignment reads).

P2. The subscription exists only to tell the client that an aspect of that
state changed, promptly, so the client updates its model without polling.

P3. Missed notices are HARMLESS by design. A subscription feeds from the
moment of subscription; nothing earlier is available on the socket, ever.
A fresh client, a reconnecting client, and a client that suspects it
missed something all do the same thing: rebuild from the query surface,
then apply notices from a live subscription. There is exactly one recovery
path and it always works.

P4. This makes the wrong architecture unrepresentable: the stream cannot
be a client's prime model or its history source, because the socket
simply does not carry the past.

P5. HOW clients read state is under active recon (Mike-ordered in this
review): direct SQL against the db is not a product interface; the CLI
exists to make common things easy for agents, not to re-create SQL; bulk
model-building reads likely belong on a formal REST surface exported
directly to clients. The recon recommends the CLI-vs-REST split and the
shape of that REST state API given the full internal schema; this spec
may grow a companion REST-API section (or a sibling spec) from its
findings.

## Goal

G1. Tightbeam SHALL provide one WebSocket endpoint that notifies connected
consumers, promptly after commit, that state changed — with enough in the
notice to update a model of that state without a follow-up query in the
common case.

G2. Every state-changing commit SHALL produce a notice to every connected
subscription whose filters match. Nothing is excluded from the stream
itself; filters narrow delivery for one subscriber only.

G3. The endpoint SHALL serve any consumer the gateway can authenticate as
a user: a dashboard, ATC, a script, another agent.

## Non-goals

N1. NO history on the socket: no replay, no cursors, no tail, no
scroll-back pages, no bootstrap. A subscription starts at the point of
subscription. History is the query surface.

N2. NO event storage and NO retention policy: notices are not persisted
for consumers. (The substrate's existing internal EventLog tables are out
of scope — unchanged, still write-only observability.)

N3. NO delivery guarantee across disconnects, and none needed: the
recovery path is rebuild-from-queries (P3).

N4. Nothing is sent INTO Tightbeam on this socket beyond subscribe
control messages. A chat client sends through the normal gateway verbs
(wake) and sees the effect arrive as notices.

N5. No capability or API-key system (ruled 2026-08-20). Auth is the
existing gateway credential.

N6. No delivery judgment: the substrate never decides a change is
uninteresting (philosophy gate 5).

N7. No webhooks, SSE, or polling interface in v1.

N8. This spec does not authorize implementation.

## Terms

T1. **Notice** — one frame telling a subscriber that a state change
committed: its class, its reference ids, and the changed row's recorded
content in full.

T2. **Class** — the change's namespaced kind string from §The class
registry. The set is OPEN; new mechanisms mint new classes and amend the
registry.

T3. **Subscription** — one filtered view on a connection, opened by a
subscribe message with a client-chosen `subscriptionId`; every notice for
it is tagged with that id. A connection multiplexes any number.

T4. **Seq** — a per-connection monotonically increasing counter stamped on
notices. It exists ONLY so a client can detect that delivery hiccuped
mid-connection (a skip) and trigger its one recovery path: rebuild. It is
not a resume token; nothing accepts it back.

T5. **Read marker** — a user-scoped "seen through here" position stored as
a substrate row (§Read markers). Not a stream concept; its changes merely
broadcast like any other state change.

## The event vocabulary law

V1. Every state-changing commit SHALL emit its notices as part of the
commit path (post-commit, nonblocking to the transaction): a change with
no notice class is a defect the registry test catches (A1).

V2. Classes are namespaced `area.happening`, lowercase, dot-separated. The
registry below is part of this spec. A class name never changes meaning.

V3. **RULED (Mike), refined r5:** the notice payload is the resource's
CANONICAL PUBLIC PROJECTION — the full recorded product fields and user
content, unredacted after authorization, sufficient to update a displayed
model without a follow-up query. "Unredacted" never means raw rows: the
db stores credentials (session cliToken, device token, harness
identityToken) and no projection ever carries a storage secret. One
serializer per resource owns the projection; REST detail and notice
payload are byte-equivalent (A6).

V4a. Every payload carries the row's monotonically increasing version
(`rowVersion`, or the resource's natural one: `updatedAt`, seq). Clients
apply notices and snapshot rows by LAST-VERSION-WINS upsert — "dedupe"
does not exist as a concept (M1).

V4. Notice shape:

```json
{
  "type": "change",
  "schemaVersion": 1,
  "subscriptionId": "chat-s_775f",
  "seq": 4213,
  "class": "attest.filed",
  "resource": "attests",
  "op": "upsert",
  "occurredAt": 1786900000000,
  "refs": {"sessionKey": "...", "workItemId": "wi_...",
           "assignmentId": "asg_...", "origin": "...", "principal": "..."},
  "payload": { }
}
```

`resource` and `op` (`upsert` | `delete`) spare model code from parsing
class strings. A delete carries the final public projection as its
tombstone payload and the client removes the key — required because some
rows hard-delete today (roles).

`refs` SHALL always include the resource's primary id (per the R8
mapping); other reference ids appear when the change has them. One
schemaVersion keeps one meaning; widening bumps it. Observational
classes (R5, R6) use `op: "observe"` and omit `resource`.

V5. Payload rows SHALL carry the same primary ids the query surface
returns for the same rows, so a client can match a notice against fetched
state (the correlation seam; recon wi_9fdc0c07 verifies it).

## The class registry (initial enumeration, derived from main tip)

R1. Work:
`work_item.created`, `work_item.updated`, `work_item.iceboxed`,
`work_item.reopened`, `work_item.closed`, `work_item.failed`,
`assignment.opened`, `assignment.reopened`, `assignment.closed` (outcome
in payload), `attest.filed` (kind and verdictKind in payload).

R2. Attention and escalation:
`wake.scheduled`, `wake.fired`, `wake.canceled`, `prod.fired`,
`turn.started`, `turn.ended`, `decision_request.opened`,
`decision_request.ruled`, `decision_request.withdrawn`.

R3. Org shape:
`session.spawned`, `session.retired`, `role.created`, `role.bound`,
`role.removed`, `user.added`, `device.approved`, `device.denied`,
`device.revoked`.

R4. Records: `artifact.recorded`, `read_marker.updated` (RM3).

R4b. Conversation: `message.created` — without it a chat client cannot be
lively (M4 promised message classes; recon wi_9239a7f1 caught the
registry gap).

R5. Dispatch (OBSERVATIONAL-ONLY): `verb.accepted`, `verb.denied` — one
per gateway verb call, with the verb name, origin, and principal in
payload/refs. The catch-all: a change whose fact class is missing still
surfaces here, which is how A1 catches registry gaps. Observational-only
means: these stream (every event streams), but they are OUTSIDE the
rebuildable-state contract — no REST resource replays them, and a model
must never depend on having seen one (they are audit, not state).

R6. Rails and lifecycle (OBSERVATIONAL-ONLY, same contract): `rail.denied`,
`lifecycle.boot`, `lifecycle.clean_shutdown`, `lifecycle.dirty_exit`,
`lifecycle.takeover`.

R6b. Admin-state mutations (F3): `config.updated`, `host_env.updated`,
`identity.updated`, `host.registered`, `kungfu.updated`,
`user.promoted` — state classes, so their REST models cannot rot behind
observational verb notices.

R7. Derived from main tip's row vocabulary as of 2026-08-20; the build
card verifies mechanically (A1) and amends where reality disagrees.

R8. The build card materializes the class mapping TABLE the acceptance
tests presuppose: every state class row names its resource, op
(upsert|delete), primary-id ref key, and serializer — seeded from the
adopted recon's primary-key table (rest-state-api-recon.md §WebSocket
correlation contract). A class without a row is a red build.

| Class | Resource | Op | Primary notice ref | Serializer | Version and emission | Visibility and convergence | A1/A6 coverage |
|---|---|---|---|---|---|---|---|
| `condition_fact.filed` | `condition facts` | `upsert` | `factId` | exact shared R7 condition-fact serializer | The condition fact `id` is its append-only natural version; its `rowVersion` equals `id`. Each successful insertion into `condition_facts` emits one notice after commit. An idempotent filing that returns the existing fact emits none. | `GET /api/facts` visibility. Consumers apply last-version-wins by `factId`. | A1 covers the class and primary-ref mapping. A6 verifies this serializer is byte-equivalent to the REST detail item. |
| `critical_lease.updated` | `critical state` | `upsert` | `sessionKey` | exact shared R7 critical-state serializer | The item uses R7 critical-state `rowVersion`. Each committed change to the R7 item for one `sessionKey` emits one notice after commit. A replay or idempotent request that leaves the item and `rowVersion` unchanged emits none. | `GET /api/critical-state` admin-only visibility. Consumers apply last-version-wins by `sessionKey`. | A1 covers the class and primary-ref mapping. A6 verifies this serializer is byte-equivalent to the REST detail item. |

R9. Composed views (toplines, coordination-share, digest-members, org)
have no notices of their own. Each composed REST resource DECLARES its
underlying state classes; a client refreshes the view when a matching
notice arrives. The REST spec carries the per-view dependency lists.

R10. Visibility-affecting classes (`role.bound`, `role.removed`,
`user.promoted`, `device.revoked`, `session.retired`, `user.added`) are
rebuild triggers: a client receiving one that touches its own principal
re-snapshots (M2); the server MAY instead close the affected
subscriptions to force it.

## Connection and auth

C1. A WebSocket upgrade on the gateway's existing HTTP listener, at its
own path, separate from the chat socket.

C2. Auth is IN-BAND, exactly like the existing chat socket: connect
plain, send an `auth` frame carrying the existing gateway credential as
the first message, receive `auth_result` (same failure vocabulary).
Browser-compatible by construction — no Authorization header on the
upgrade, no tickets, no credential in the URL. No new credential type.

C4. Revocation closes sockets: a `device.revoked` or `session.retired`
affecting a connection's principal closes that connection (1008); the
client's reconnect re-auths and rebuilds (M2).

C3. Transport posture: localhost or tailscale; TLS termination is the
operator's proxy (see wi_bdf9a537 for the tailscale-serve posture).

## Subscribing

S1. After auth, the client opens subscriptions — any number, all on this
one connection:

```json
{
  "type": "subscribe",
  "protocolVersion": 1,
  "subscriptionId": "chat-s_775f",
  "filters": {
    "classes": ["attest.", "work_item."],
    "sessionKey": null,
    "workItemId": null,
    "origin": null,
    "principal": null
  }
}
```

S2. `filters` and every field in it are optional; `classes` match by
prefix; multiple given fields are conjunctive; no filters means
everything.

S3. The server answers `subscription_ready` (tagged with the
subscriptionId). Delivery for that subscription begins at the server's
processing of the subscribe — the registration cut. A change committed
after the cut is delivered; nothing before it ever is.

S4. Changing filters is `{"type": "unsubscribe", "subscriptionId": ...}`
then a fresh subscribe on the same connection. Duplicate subscriptionId or
unknown unsubscribe is `invalid_request`.

S5. No admission or concurrency limit (ruled 2026-08-20) — with one
sanity cap (Mike, 2026-08-22, resolving review finding F23): at most 100
subscriptions per connection; the 101st subscribe is refused with a typed
invalid_request naming the cap. Not an admission limit — a runaway-client
backstop no real client hits.

## The model recipe (how every client uses this)

M1. Subscribe (get `subscription_ready`) FIRST, then snapshot current
state through the query surface, then apply incoming notices to the
model. Mike's review note is normative: the danger zone is the gap
between building the model and receiving the first notice — subscribing
first closes it, and the worst case becomes duplicate records, never
missed ones. Therefore the client's model-build algorithm SHALL be
IDEMPOTENT under duplicate records — implemented as last-version-wins
upsert on (id, rowVersion) (V4a): an older version over a newer one is a
no-op, anything applied twice converges. Plain drop-by-id is FORBIDDEN
(it silently keeps stale rows).

M2. On ANY doubt — reconnect, seq skip (T4), gateway restart, or plain
suspicion — rebuild: re-snapshot the displayed slice and keep applying
notices. Rebuild is the single recovery path and is always correct.

M3. Unread marking ("has the user seen this?") is a position against
STATE rows (a row id or timestamp per view), never against the stream.
Shared markers live in substrate rows (RM1); a strictly single-instance
client MAY keep its marker client-local instead.

## Read markers (RULED, Mike 2026-08-21)

RM1. The substrate SHALL provide user-scoped read-marker rows:
`(userId, scopeKey, marker)`. `scopeKey` is a client-chosen string naming
the view (a session, a work item, an ATC view name); `marker` is a row id
or timestamp meaning "seen through here". The substrate stores and
broadcasts; it never interprets either field (physics, not judgment).

RM2. Markers are set through a named verb (`read-marker-set`: scopeKey +
marker + optional expected-current for conditional write, refusing on
mismatch) and cleared through `read-marker-clear` — the lawful repair
path for a wrong marker. Reads via REST. No ws involvement in writing.

RM3. A marker change broadcasts as an ordinary `read_marker.updated`
notice. That is the whole multi-instance sync mechanism: one ATC instance
advances the marker, every other instance holding a matching subscription
repaints. Precedents for server-side seen-state: IMAP `\Seen`, Slack
per-user per-channel `last_read`, Matrix read markers, Kafka
broker-stored consumer-group offsets.

M4. A chat client: model from the transcript read (paginated,
before/after); send via wake; watch `wake.scheduled` and the turn/message
classes update the model; deep scroll-back pages the transcript read.
Whether every piece stands on today's query surface is recon wi_9fdc0c07.

## Delivery semantics

D1. While a connection is healthy, notices for a subscription arrive in
commit order, each stamped with the next seq. Delivery is best-effort:
the writer commits, then hands the notice off the transaction path; a
crashed fan-out loses notices, and that is acceptable because of P3.

D1b. Heartbeat: the server sends each connection a periodic frame
(`{"type":"heartbeat","seq":N}`, ~15s) with the connection's latest seq.
A missed heartbeat window or a seq mismatch is a rebuild trigger (M2) —
this is what makes a lost TRAILING notice detectable; a bare gap check
cannot see it.

D2. The writer never touches a socket in its transaction: commit, then a
nonblocking hand-off to the fan-out.

D3. Slow consumer: each connection has a bounded in-memory queue. On
overflow the server closes the connection with close code 4008. The
client reconnects, resubscribes, and rebuilds (M2).

D4. Gateway shutdown closes connections with 1012. On restart clients
resubscribe and rebuild. Decimation holds: no server-side consumer state
exists to lose.

## Errors and close codes

E1. The client states `protocolVersion` in the upgrade request itself
(query parameter on the ws path); an unsupported version is refused `426`
before the upgrade completes. Auth failures happen in-band after upgrade
(C2), not at the HTTP layer.

E2. After upgrade, one error frame shape
`{"type":"error","code":"...","message":"..."}` with the single code
`invalid_request` (malformed subscribe/unsubscribe, duplicate or unknown
subscriptionId).

E3. Close codes: `4008` slow-consumer (D3), `1012` restarting (D4), plus
the standard codes.

## Acceptance

A1. Every state-changing verb on main tip emits notices whose classes
match §The class registry, both directions — a test diffs the verb table
and emitted classes against the registry.

For `condition_fact.filed` and `critical_lease.updated`, the A1 table names
the shared AU4 visibility function for the R8 resource and tests one allowed
and one denied principal. The REST detail and firehose fan-out invoke that
same function; the allowed principal receives the committed notice and the
denied principal receives neither detail nor notice.

A2. A subscriber receives a notice for a matching commit made after its
registration cut, and never one from before it.

A2b. Delete notices are authorized against the row's LAST pre-delete
state (F18): whoever could see the row learns it is gone; nobody else
learns it existed. Kill a subscriber's credential: the socket closes
within one notice/heartbeat (C4). Suppress the fan-out for one commit:
the next heartbeat exposes the gap and the client rebuilds (D1b).

A3. A filtered subscriber receives exactly the matching notices; a change
matching several of a connection's subscriptions arrives once per
matching subscription, each tagged.

A4. M1 converges: subscribe-then-snapshot-then-apply reaches a model
identical to a fresh query at any quiescent moment, duplicates dropped
via V5's shared ids.

A5. Kill the gateway mid-stream: clients detect the close, resubscribe,
rebuild, and converge again (M2). Force a slow consumer into 4008: same.

A6. For every state (non-observational) class, the notice payload and the
REST detail item are BYTE-EQUIVALENT after removing envelope fields — one
serializer owns both (V3). Verified per class by a table-driven test that
also names each class's resource, op, and primary-key mapping. And no
public projection anywhere contains cliToken, a device token, an
identityToken, or a secret host-env value.

For `condition_fact.filed` and `critical_lease.updated`, the A6 test uses
the R8 shared serializer, primary ref, and version fields to apply older,
duplicate, and newer detail items and notices in both orders for one `factId`
and one `sessionKey`. It proves per-resource last-version-wins convergence to
the R7 item: condition facts use equal integer `id`, `refs.factId`, and
`rowVersion`; critical state uses its R7 `rowVersion`.

A7. The feature-smoke drives one real external consumer (ATC or a script)
end to end: cold build from queries, live updates via subscription,
forced reconnect, rebuild, convergence.

## Open questions for Mike

None. The read-marker question (r4's MQ1) is RULED 2026-08-21: substrate
rows, per §Read markers. Everything earlier is resolved or mooted by the
state-model ruling: auth (existing credential), payloads (full row),
retention and storage and cursor encoding (no event storage exists),
table fold (no new table exists). The load-bearing unknown is no longer
in this spec — whether the query surface suffices is recon wi_9fdc0c07's
question.
