# Event firehose v1 — state-change notifications over ws (product spec, r4)

Status: DRAFT r4, 2026-08-21. r4 is a rescoping fold of Mike's state-model
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

T5. **Read marker** — a client-facing "the user has seen through here"
position. NOT a stream concept in r4: see MQ1.

## The event vocabulary law

V1. Every state-changing commit SHALL emit its notices as part of the
commit path (post-commit, nonblocking to the transaction): a change with
no notice class is a defect the registry test catches (A1).

V2. Classes are namespaced `area.happening`, lowercase, dot-separated. The
registry below is part of this spec. A class name never changes meaning.

V3. **RULED (Mike):** the notice payload is the changed row's full
recorded truth, unredacted — sufficient to update a displayed model
without a follow-up query in the common case. The reader is the
authenticated user on their own gateway.

V4. Notice shape:

```json
{
  "type": "change",
  "schemaVersion": 1,
  "subscriptionId": "chat-s_775f",
  "seq": 4213,
  "class": "attest.filed",
  "occurredAt": 1786900000000,
  "refs": {"sessionKey": "...", "workItemId": "wi_...",
           "assignmentId": "asg_...", "origin": "...", "principal": "..."},
  "payload": { }
}
```

`refs` carries whichever reference ids the change has; absent refs are
omitted. One schemaVersion keeps one meaning; widening bumps it.

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

R4. Records: `artifact.recorded`.

R5. Dispatch: `verb.accepted`, `verb.denied` — one per gateway verb call,
with the verb name, origin, and principal in payload/refs. The catch-all:
a change whose fact class is missing still surfaces here, which is how A1
catches registry gaps.

R6. Rails and lifecycle: `rail.denied`, `lifecycle.boot`,
`lifecycle.clean_shutdown`, `lifecycle.dirty_exit`, `lifecycle.takeover`.

R7. Derived from main tip's row vocabulary as of 2026-08-20; the build
card verifies mechanically (A1) and amends where reality disagrees.

## Connection and auth

C1. A WebSocket upgrade on the gateway's existing HTTP listener, at its
own path, separate from the chat socket.

C2. Auth is the existing gateway credential flow, authenticating the
requesting user. No new credential type.

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

S5. No admission or concurrency limit (ruled 2026-08-20).

## The model recipe (how every client uses this)

M1. Subscribe (get `subscription_ready`), THEN snapshot current state
through the query surface, then apply incoming notices to the model.
Changes that landed between subscribe and snapshot appear in both; V5's
shared ids let the client recognize and drop the duplicates.

M2. On ANY doubt — reconnect, seq skip (T4), gateway restart, or plain
suspicion — rebuild: re-snapshot the displayed slice and keep applying
notices. Rebuild is the single recovery path and is always correct.

M3. Unread marking ("has the user seen this?") is a position against
STATE rows (a row id or timestamp per view), never against the stream.
Where that position lives — client-local vs a shared substrate row — is
MQ1.

M4. A chat client: model from the transcript read (paginated,
before/after); send via wake; watch `wake.scheduled` and the turn/message
classes update the model; deep scroll-back pages the transcript read.
Whether every piece stands on today's query surface is recon wi_9fdc0c07.

## Delivery semantics

D1. While a connection is healthy, notices for a subscription arrive in
commit order, each stamped with the next seq. Delivery is best-effort:
the writer commits, then hands the notice off the transaction path; a
crashed fan-out loses notices, and that is acceptable because of P3.

D2. The writer never touches a socket in its transaction: commit, then a
nonblocking hand-off to the fan-out.

D3. Slow consumer: each connection has a bounded in-memory queue. On
overflow the server closes the connection with close code 4008. The
client reconnects, resubscribes, and rebuilds (M2).

D4. Gateway shutdown closes connections with 1012. On restart clients
resubscribe and rebuild. Decimation holds: no server-side consumer state
exists to lose.

## Errors and close codes

E1. Before the HTTP-to-WebSocket upgrade handshake completes (the
"upgrade" is the HTTP request that switches the connection into a
WebSocket): existing HTTP auth failures; `426` for an unsupported
protocolVersion.

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

A2. A subscriber receives a notice for a matching commit made after its
registration cut, and never one from before it.

A3. A filtered subscriber receives exactly the matching notices; a change
matching several of a connection's subscriptions arrives once per
matching subscription, each tagged.

A4. M1 converges: subscribe-then-snapshot-then-apply reaches a model
identical to a fresh query at any quiescent moment, duplicates dropped
via V5's shared ids.

A5. Kill the gateway mid-stream: clients detect the close, resubscribe,
rebuild, and converge again (M2). Force a slow consumer into 4008: same.

A6. The notice payload for each registry class carries the same row
content and ids the query surface returns for that row (V5), verified per
class.

A7. The feature-smoke drives one real external consumer (ATC or a script)
end to end: cold build from queries, live updates via subscription,
forced reconnect, rebuild, convergence.

## Open questions for Mike

MQ1. **Where does the read marker live?** Every client needs "the user
has seen through here" per view, and a client that runs on several
machines at once showing one picture (ATC) needs the marker SHARED across
instances. Precedents all put shared seen-ness on the server of record:
IMAP's \Seen flag, Slack's per-user per-channel last_read, Matrix read
markers, Kafka's broker-stored consumer-group offsets. Recommendation: a
tiny user-scoped substrate row — (userId, scopeKey, marker), scopeKey
chosen by the client (a session, a work item, an ATC view), marker a row
id or timestamp — set and read via normal verbs. Its changes then
broadcast as an ordinary `read_marker.updated` notice, which is exactly
how a second ATC instance repaints when the first one advances the
marker. The ws stays dumb; single-instance clients may keep markers
client-local instead. Rule: substrate rows (recommended), client-local
only, or defer to the recon's findings.

Everything else previously open is resolved or mooted by the state-model
ruling: auth (existing credential), payloads (full row), retention and
storage and cursor encoding (no event storage exists), table fold (no new
table exists). The other load-bearing unknown is no longer in this spec —
whether the query surface suffices is recon wi_9fdc0c07's question.
