# Event firehose v1 — state-change notifications over ws (product spec)

Status: CANONICAL r6, 2026-08-25. r6 includes the landed source-invalidation
notices for durable Topline mutations and independently committed subagent
markers. These notices make the composed Toplines and ExecutionMap REST views
refreshable from each matching committed source change. They add no
ExecutionMap class and no rebuildable source resource. r6 also folds the
adjudicated Sol review-gate
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

G1 current-main composition successor, 2026-08-27: PROPOSED. Add the canonical
transcript `messageType` discriminator to the shared projection used by
`message.created` and matching REST rows on base
`277bb5031a06270aabbc57e3c222cbd2ec89bc73`. Exact candidate `b53b1f5f`
passed the G1 behavior review; verdict `att_adea7aeb` and report
`art_a3fc1d81` requested only current-main composition. Product-owner
disposition `att_e0a20ce9` preserves F1/F2. This successor changes no notice
envelope, source-invalidation mapping, G4 error, or G8 authority label.

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
- Mike's firehose gap remediation ruling, message
  `s_fe001c27-c509-4cf6-8866-47defe5eaa21` (2026-08-27), accepts recon verdict
  `att_556f55ae-f1d2-4c83-b55d-9daf06aae929` and report `art_1d389e8e`.
  It makes G2 session freshness a read-side firehose prerequisite and leaves
  the G3 write contract outside this amendment.
- Firehose client-buildability recon verdict
  `att_556f55ae-f1d2-4c83-b55d-9daf06aae929` and report `art_1d389e8e`
  identify G1. Mike's 2026-08-27 remediation ruling adopts it as a slice-2
  prerequisite. Prior product commit
  `505b56aa29f151faab7cd9618ca1bba922cff357` supplies the additive values
  and compatibility behavior.
- Superseded input: the archived focused design and draft (specs repo
  archive/) contributed the durable-row/cursor/pump replay machinery that
  r4 removes. observability-v1.md r4's doorbell contract ("frames are
  best-effort doorbells; reads recompute") is no longer merely
  complementary — this spec generalizes exactly that contract to the whole
  state model on a dedicated endpoint; observability-v1 remains authority
  for the existing chat wire's doorbells.
- Related card: wi_bdf9a537 (gateway behind tailscale serve) — transport
  posture this endpoint would inherit.

G2 session-freshness landing, 2026-08-27: adds sessions to the complete
rebuildable-state mapping. It adds `session.updated`, fixes the session
projection mutation seam, and makes cold start, reconnect, and gap recovery
decidable for session models. It changes no session field, visibility grant,
socket protocol, write surface, target, or release authority.

## Spec homing

The canonical firehose spec lives only in the `tightbeam-specs` repository as
`event-firehose-v1.md`. Canonical r6's coupled set is
`event-firehose-v1.md`, `rest-state-api-v1.md`, and
`rest-state-api-v1-wire-schema.md`; a change to an R8 or R8b mapping, its R9
dependency, its filter value, or its wire type lands those coupled files in
one reviewed revision. Recon documents, adjudication ledgers, artifact rows,
transcripts, worktrees, and review reports are authority evidence, not
canonical custody. The source-invalidation companion landed with REST r4 at
`0139d9a71180a7175965473fade9b183d2b57601`.

G1 uses the same exact canonical set. A change to the transcript-message
projection, `message.created` mapping, or `messageType` wire contract lands all
three files in one reviewed revision.

## Assumptions

AS1. The gateway already authenticates its existing credentials through the
chat socket's in-band exchange. C2 reuses that exchange and adds no credential
type.

AS2. The REST companion ships each R9 snapshot read before the matching
freshness class. Firehose A7 falsifies this assumption if a consumer cannot
rebuild the displayed slice after reconnect.

AS3. The REST companion ships the R7 sessions collection, detail route, and
serializer before `session.spawned`, `session.updated`, or `session.retired`.
Firehose A4 and A5 falsify this assumption if a consumer cannot rebuild its
visible sessions after cold start, reconnect, or a detected gap.

## Invariants — the state model is the entity

P1. Tightbeam's truth is the state db: durable rows, queryable. A client's
job is to hold a model of the slice it displays, built from the query
surface (CLI verbs, HTTP reads: transcript, toplines, work-item and
assignment reads).

P2. The subscription exists only to tell the client, through D1's post-commit
handoff, that an aspect of state changed, so the client updates its model
without polling.

P3. Missed notices are HARMLESS by design. A subscription feeds from the
moment of subscription; nothing earlier is available on the socket, ever.
A fresh client, a reconnecting client, and a client that suspects it
missed something all do the same thing: rebuild from the query surface,
then apply notices from a live subscription. There is exactly one recovery
path and it always works.

P4. This makes the wrong architecture unrepresentable: the stream cannot
be a client's prime model or its history source, because the socket
simply does not carry the past.

P5. The adopted `rest-state-api-v1.md` companion owns how clients read state.
Direct SQL against the db is not a product interface. The CLI makes common
agent reads concise and does not re-create SQL. Clients build bulk models from
the companion REST surface.

P6. `messageType` is the sole public message-kind discriminator for transcript
messages. `role` keeps authorship direction and `sender` keeps provenance. A
firehose adapter does not add `message_type`, `messageKind`, `kind`, or another
message-kind alias.

## Goal

G1. Tightbeam SHALL provide one WebSocket endpoint that notifies connected
consumers through D1's post-commit handoff that state changed — with enough in
the notice to update a model of that state without a follow-up query in the
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

N9. G2 does not define the G1 message discriminator, the G3 write
contract, the G4 error envelope, the G5 transcript reconciliation, the G6
decision-state subset, the G7 detail-route set, or the G8 authority labels.

Operating-guidance impact: none. Canonical r6 extends the existing
source-class registry and creates no cross-repository agent rule.

## Terms

T1. **Notice** — one frame telling a subscriber that a state change committed.
An R8 rebuildable-state notice carries its class, refs, and full canonical
public projection. An R8b source invalidation carries its class, refs, and
natural source version only.

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

T6. **Source invalidation notice** — an `op:"observe"` notice from the exact
durable commit that makes a composed REST view stale. It is a refetch trigger,
not a rebuildable resource or a direct model upsert. Its R8b mapping fixes its
class, source seam, refs, natural version, visibility, and payload.

T7. **Message type** — the nullable classification stored at the message write
seam and exposed as `messageType` in the canonical transcript-message
projection. Current writers emit `assistant`, `substrate`, `marker`, or
`agent`. The serializer omits `messageType` when the stored classification is
null. A client accepts an unrecognized string; a missing or unrecognized value
means `assistant` for message-type presentation. `role` still carries
authorship direction.

T8. **Session projection mutation** — a committed change that makes one
canonical R7 session field other than `rowVersion` differ for one
`sessionKey`. The comparison uses the complete serialized item with
`rowVersion` excluded. It does not infer change from a verb name, timer, or
declared effect list.

T9. **Session mechanical status** — the R7 `mechanicalStatus` string preserves
the existing `Tightbeam.Gateway.session_status/2` `run.state` projection. Its
closed values are `idle` and `running`. Its only mutable input is the committed
count of this session's turn rows whose `status` is `queued` or `running`:
zero maps to `idle`; a positive count maps to `running`.

## Architecture — the event vocabulary law

V1. Every state-changing commit SHALL emit its notices as part of the
commit path (post-commit, nonblocking to the transaction): a change with
no notice class is a defect the registry test catches (A1).

This amendment adds one class and one mutation seam because deleting sessions
would remove the core Clawline model, while accepting stale session bytes would
violate the ruled freshness-only architecture.

V2. Classes are namespaced `area.happening`, lowercase, dot-separated. The
registry below is part of this spec. A class name never changes meaning.

V3. **RULED (Mike), refined r5:** an R8 rebuildable-state notice payload is the
resource's CANONICAL PUBLIC PROJECTION — the full recorded product fields and
user content, unredacted after authorization, sufficient to update a displayed
model without a follow-up query. "Unredacted" never means raw rows: the
db stores credentials (session cliToken, device token, harness
identityToken) and no projection ever carries a storage secret. One
serializer per resource owns the projection; REST detail and notice
payload are byte-equivalent (A6).

V4a. Every R8 payload carries the row's monotonically increasing version
(`rowVersion`, or the resource's natural one: `updatedAt`, seq). Clients apply
R8 notices and snapshot rows by LAST-VERSION-WINS upsert — "dedupe" does not
exist as a concept (M1). An R8b payload carries only its positive
`sourceVersion`; T6 forbids applying it as a row upsert.

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

`resource` and `op` (`upsert` | `delete` | `observe`) spare model code from
parsing class strings. A delete carries the final public projection as its
tombstone payload and the client removes the key — required because some
rows hard-delete today (roles).

`refs` SHALL always include the resource's primary id (per the R8
mapping); other reference ids appear when the change has them. One
schemaVersion keeps one meaning; widening bumps it. Observational classes
(R5, R6) and source invalidation classes (R8b) use `op: "observe"` and omit
`resource`. An observational notice is audit. A source invalidation notice is
a closed-world composed-view refetch trigger; it never masquerades as a row
the query surface can rebuild.

V5. Payload rows SHALL carry the same primary ids the query surface
returns for the same rows, so a client can match a notice against fetched
state (the correlation seam; recon wi_9fdc0c07 verifies it).

V5a. The `message.created` payload is the exact shared R7 transcript-message
item. Its `messageType` value comes from the stored discriminator; neither the
firehose adapter nor the serializer derives it from `content`, `sender`, or a
first-line convention. A null stored discriminator omits the key from both
surfaces. The notice carries `refs.messageId` equal to payload `id` and
`refs.sessionKey` equal to payload `sessionKey`. The matching REST row and
notice payload expose the same present or omitted `messageType` bytes.

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
`session.spawned`, `session.updated`, `session.retired`, `role.created`, `role.bound`,
`role.removed`, `user.added`, `device.approved`, `device.denied`,
`device.revoked`.

R4. Records: `artifact.recorded`, `read_marker.updated` (RM3).

R4b. Conversation: `message.created` — without it a chat client cannot be
lively (M4 promised message classes; recon wi_9239a7f1 caught the
registry gap).

R4c. Composed-view invalidation sources: `topline.created`,
`topline_work_membership.linked`, `topline_work_membership.unlinked`, and
`subagent_marker.appended`. R8b is their complete mapping. There is no
`execution_map.*` class.

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
| `session.spawned`, `session.updated`, `session.retired` | `sessions` | `upsert` | `sessionKey` | exact shared R7 session serializer | The session projection mutation seam allocates the next durable session `rowVersion` in the same transaction as the changed projection. First materialization selects `session.spawned`; an `active` to `retired` state transition selects `session.retired`; each other changed item selects `session.updated`. One commit selects one class. A no-change request emits none. | REST AU4 session visibility. Consumers apply last-version-wins by `sessionKey`. The payload `sessionKey` equals `refs.sessionKey`. | A1 covers the mutation seam and class selection. A6 verifies byte equivalence with `GET /api/sessions/:sessionKey`. |
| `condition_fact.filed` | `condition facts` | `upsert` | `factId` | exact shared R7 condition-fact serializer | The condition fact `id` is its append-only natural version; its `rowVersion` equals `id`. Each successful insertion into `condition_facts` emits one notice after commit. An idempotent filing that returns the existing fact emits none. | `GET /api/facts` visibility. Consumers apply last-version-wins by `factId`. | A1 covers the class and primary-ref mapping. A6 verifies this serializer is byte-equivalent to the REST detail item. |
| `critical_lease.updated` | `critical state` | `upsert` | `sessionKey` | exact shared R7 critical-state serializer | The item uses R7 critical-state `rowVersion`. Each committed change to the R7 item for one `sessionKey` emits one notice after commit. A replay or idempotent request that leaves the item and `rowVersion` unchanged emits none. | `GET /api/critical-state` admin-only visibility. Consumers apply last-version-wins by `sessionKey`. | A1 covers the class and primary-ref mapping. A6 verifies this serializer is byte-equivalent to the REST detail item. |
| `message.created` | `transcript messages` | `upsert` | `messageId`, `sessionKey` | exact shared R7 transcript-message serializer | The item uses its R7 `rowVersion`. Each newly committed transcript message emits one notice after commit; an idempotency replay that returns the existing row emits none. | `GET /api/sessions/:sessionKey/messages` visibility. Consumers correlate by `messageId` and apply last-version-wins by `(payload.id, payload.rowVersion)`. | A1 covers the class and both refs. A6 verifies the complete item, including conditional `messageType` omission, is byte-equivalent to the matching REST row. |

R8b. Source invalidation classes are deliberately not R8 rebuildable-state
rows. Each emits `op:"observe"`, omits `resource`, and carries exactly
`payload:{"sourceVersion":I}`, where `I` is a positive JSON integer. A client
never applies this payload as state; after visibility and subscription filters
allow it, the client refetches each composed REST view that lists the class in
its closed R9 dependencies.

| Class | Exact successful source commit | Required refs | Source version and `occurredAt` | Visibility before filters | Emission |
|---|---|---|---|---|---|
| `topline.created` | `Tightbeam.Toplines.create/2` inserts the `toplines` row and its `topline_events(kind='topline_created')` row in one transaction | `toplineId` | `sourceVersion` is that Topline's positive `topline_events.seq`; `occurredAt` is its `eventAt` | the REST AU4 Toplines owner-or-admin predicate on the committed Topline | exactly once after a new commit; an idempotency replay emits none |
| `topline_work_membership.linked` | `Tightbeam.Toplines.link_work/2` inserts `topline_work_memberships`, touches the parent Topline, and inserts `topline_events(kind='work_linked')` in one transaction | `toplineId`, `membershipId`, `workItemId` | `sourceVersion` is the positive sequence of that `topline_events` row; `occurredAt` is its `eventAt` | the REST AU4 Toplines owner-or-admin predicate on the parent Topline | exactly once after a new commit; a refusal or idempotency replay emits none |
| `topline_work_membership.unlinked` | `Tightbeam.Toplines.unlink_work/2` ends `topline_work_memberships`, touches the parent Topline, and inserts `topline_events(kind='work_unlinked')` in one transaction | `toplineId`, `membershipId`, `workItemId` | `sourceVersion` is the positive sequence of that `topline_events` row; `occurredAt` is its `eventAt` | the REST AU4 Toplines owner-or-admin predicate on the parent Topline after commit | exactly once after a new commit; a refusal or idempotency replay emits none |
| `subagent_marker.appended` | `Tightbeam.SubagentMarkers.append/3` or `append_in_txn/2` inserts one `subagent_markers` row | `markerId`, `sessionKey`; `assignmentId` and `workItemId` when the marker has a non-null assignment that resolves to a work item | `markerId` is the inserted positive row id encoded as a canonical base-10 string without leading zeros; `sourceVersion` is the same id as a positive JSON integer; `occurredAt` is marker `at` | the marker inherits its non-null parent assignment's AU4 grant and requires the resolved work item's AU4 grant; a null, unresolved, or denied assignment yields no delivery to that principal | exactly once after `Txn.changes(txn) == 1`; `INSERT OR IGNORE` returning the existing marker emits none |

The marker mapping derives authorization only from existing assignment and
work-item grants. It creates no principal behavior. The Topline mappings expose
no new Topline field or serializer. These four notices carry only the refs and
source version needed to invalidate a composed view; the authorized REST
composition remains the only rebuild path.

R8b filter values are closed. `classes` matches the notice's literal class by
S2 prefix. `sessionKey` and `workItemId` match only the equal literal ref when
that ref is present in the mapping row; an absent ref is no match. Thus
`sessionKey` has a value only for `subagent_marker.appended`, and `workItemId`
has a value only for the two membership classes and for a marker whose
non-null assignment resolves to a work item. The R8b refs object contains
exactly the refs named by its mapping row and omits every absent optional ref.
Each mapping omits `origin` and `principal`; a subscription that supplies
either filter does not match an R8b notice. Visibility still runs first, so a
hidden source never reaches this matcher. A composed-view client subscribes
to the R9 class prefixes and adds only ref filters for which these rules define
a value; the matcher derives no ref or filter value from an owner, mutation
actor, authenticated principal, or other row.

R9. Composed views (toplines, execution map, coordination-share,
digest-members, org) have no notices of their own. Each composed REST resource
DECLARES its underlying state and source-invalidation classes; a client
refreshes the view when a matching notice arrives. The REST spec carries the
per-view dependency lists.

R10. Visibility-affecting classes (`role.bound`, `role.removed`,
`user.promoted`, `device.revoked`, `session.retired`, `user.added`) are
rebuild triggers: a client receiving one that touches its own principal
re-snapshots (M2); the server MAY instead close the affected
subscriptions to force it.

## Connection and auth

C1. A WebSocket upgrade on the gateway's existing HTTP listener, at its
own path, separate from the chat socket. RULED (Mike, 2026-08-22): this
socket ADDS to the product, it does not replace Clawline's chat ws —
the two coexist indefinitely: GET /ws stays the chat wire exactly as
today; the firehose mounts at its own path (working name /ws/changes)
on the SAME port. No new port: WebSockets are distinguished by path,
and one listener means one auth surface, one tailscale-serve config,
one firewall story.

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
upsert on (primary id, rowVersion) (V4a), where a session's primary id is
`sessionKey`: an older version over a newer one is a
no-op, anything applied twice converges. Plain drop-by-id is FORBIDDEN
(it silently keeps stale rows).

M1b. Apply only R8 `upsert` and `delete` payloads directly to the model under
M1. For each allowed R8b `observe` notice, refetch every currently held R9 view
that declares the class and replace that composed snapshot. The client does
not compare `sourceVersion` with `dependencyVersion` and does not apply the
R8b payload as an entity. Repeating one R8b notice may repeat the refetch and
cannot change the resulting snapshot bytes at a quiescent source state.

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
classes update the model; watch `session.*` for picker, engine, identity,
history-barrier, retirement, and mechanical-status freshness; deep scroll-back
pages the transcript read.
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

The same table covers every R8b source commit. It fails if a successful new
Topline or marker commit emits no mapped class, emits more than the one mapped
class, or if a refusal, idempotency replay, or ignored duplicate emits one.

For `condition_fact.filed` and `critical_lease.updated`, the A1 table names
the shared AU4 visibility function for the R8 resource and tests one allowed
and one denied principal. The REST detail and firehose fan-out invoke that
same function; the allowed principal receives the committed notice and the
denied principal receives neither detail nor notice.

For sessions, the A1 table drives first materialization, display-name change,
adoption change, archetype, identity or override change, engine or host change,
history-barrier change, mechanical-status change, and retirement through the
single projection mutation seam. Given a successful commit, when any R7 item
field other than `rowVersion` changes, then the same transaction advances
`rowVersion` and selects
exactly one of `session.spawned`, `session.updated`, or `session.retired` by
the R8 rule. Given unchanged serialized bytes, then it advances no version and
emits no session state notice. The test fails if any writer can change a
mutable input to the R7 session item outside this seam.

For the T9 input, the table commits these cases: zero qualifying turns to one,
one to zero, one to two, two to one, `queued` to `running`, and a change wholly
outside the `queued`/`running` set. Only zero to positive and positive to zero
change `mechanicalStatus`, advance the session `rowVersion`, and select
`session.updated`. The other cases emit their mapped turn notices and no
session notice from the T9 input.

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

For each session class, a table tests the closed filter rules: its literal
class matches the `session.` prefix; `refs.sessionKey` matches only the equal
`sessionKey` filter; and `origin` and `principal` never match. The visibility
predicate runs before the matcher, and a denied session invokes no matcher and
emits no frame.

For each R8b class, a table tests the closed filter rules: its literal class
matches the correct prefix; each present `sessionKey` or `workItemId` ref
matches only the equal filter; each absent ref does not match; and `origin`
and `principal` never match. The visibility predicate runs before the matcher,
and a denied source invokes no matcher and emits no frame.

A4. M1 converges: subscribe-then-snapshot-then-apply reaches a model identical
to a fresh query at a quiescent moment. Reapplying the same R8 notice converges
through V4a last-version-wins. Receiving the same R8b source version twice may
cause two refetches and cannot mutate the model directly.

Given a client that receives `subscription_ready` for `session.`, when it pages
`GET /api/sessions` while one session changes concurrently, then applying the
buffered session notice and snapshot items by `(sessionKey,rowVersion)` yields
the same session collection as a fresh quiescent read. The outcome is the same
whether the snapshot item or notice arrives first.

A5. Kill the gateway mid-stream: clients detect the close, resubscribe,
rebuild, and converge again (M2). Force a slow consumer into 4008: same.

Given a client that misses `session.updated`, when a later sequence or
heartbeat exposes the gap, then the client resubscribes, pages the visible
sessions collection, and converges from that snapshot plus live notices.

Given a disconnect after a session change, reconnect uses the same
resubscribe-and-snapshot sequence and reaches the same result.

A6. For every R8 rebuildable-state class, the notice payload and the REST
detail item are BYTE-EQUIVALENT after removing envelope fields — one
serializer owns both (V3). Verified per class by a table-driven test that
also names each class's resource, op, and primary-key mapping. And no
public projection anywhere contains cliToken, a device token, an
identityToken, or a secret host-env value.

The G7 comparators for resources that previously had collection-only reads are
exactly these addressable detail routes:

| R8 resource | Detail comparator |
|---|---|
| attests | `GET /api/attests/{payload.id}` |
| roles | `GET /api/roles/{payload.name}` |
| transcript messages | `GET /api/sessions/{payload.sessionKey}/messages/{payload.id}` |
| condition facts | `GET /api/facts/{payload.id}` |
| critical state | `GET /api/critical-state/{payload.sessionKey}` |
| host environment | `GET /api/host-env/{payload.host}/{payload.harness}/{payload.name}` |

Each comparator invokes the same resource query, AU4 visibility predicate,
and public serializer as its collection and R8 publisher. The REST adapter
adds only the shared detail envelope. A REST-local projection or a second item
shape fails A6.

For an upsert class, A6 compares the live detail `item` with the notice
payload. For `role.removed`, the delete commit invokes the same roles
serializer on the last pre-delete projection with the new delete
`rowVersion`; A6 compares that serializer output with the tombstone payload.
After commit, `GET /api/roles/:name` returns the ordinary unknown
`404 not_found`. The firehose does not create REST history or a second role
shape.

Given one newly committed message for each current `messageType` value and one
historical message whose stored discriminator is null, when an authorized
client fetches the rows and receives their `message.created` notices, then
each notice payload is byte-equivalent to its matching fetched item. Each
notice also has `refs.messageId == payload.id` and
`refs.sessionKey == payload.sessionKey`. The historical item and payload omit
`messageType`; neither emits `messageType:null`.

Given equal message content across those fixtures, when REST and firehose
serialize them, then each surface preserves the stored discriminator. The test
fails if either surface parses content or calls a route-local serializer.

Given a matching fetched item and notice payload with an unrecognized nonempty
`messageType`, when a conforming client reads either item, then it accepts the
item and treats its message type as `assistant`. Given a matching pair that
omits `messageType`, the client does the same. Neither fallback changes `role`.

R8b source invalidations are outside A6 because they expose no rebuildable
resource. A table-driven test instead requires their exact `op`, absent
`resource`, refs, one-key payload, source version, commit cut, and visibility
predicate. It then proves the matching R9 composed view changes after refetch.

For `condition_fact.filed` and `critical_lease.updated`, the A6 test uses
the R8 shared serializer, primary ref, and version fields to apply older,
duplicate, and newer detail items and notices in both orders for one `factId`
and one `sessionKey`. It proves per-resource last-version-wins convergence to
the R7 item: condition facts use equal integer `id`, `refs.factId`, and
`rowVersion`; critical state uses its R7 `rowVersion`.

For each session class, the A6 test requires `resource:"sessions"`,
`op:"upsert"`, equal payload and ref `sessionKey`, and the exact R7 session
bytes returned by `GET /api/sessions/:sessionKey`. Older, duplicate, and newer
snapshot items and notices applied in both orders converge by the session
`rowVersion`.

A7. The feature-smoke drives one real external consumer (ATC or a script)
end to end: cold build from queries, live updates via subscription,
forced reconnect, rebuild, convergence.

## Open questions for Mike

None. The read-marker question (r4's MQ1) is RULED 2026-08-21: substrate rows,
per §Read markers. Everything earlier is resolved or mooted by the state-model
ruling: auth uses the existing credential; R8 rebuildable payloads carry the
full canonical row; R8b carries only its exact invalidation version; no event
storage, retention, or cursor exists. The adopted REST companion owns the
query surface.

The source-invalidation amendment is ruled by
`att_d5b0a440-bd51-498f-8b96-e6512fedf68f`: preserve marker-backed `fanOut`
and durable Toplines, map their exact source commits, and add no
ExecutionMap notice class.
