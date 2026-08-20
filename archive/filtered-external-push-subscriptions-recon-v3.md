# Focused external push subscriptions — design recon, revision 3

Date: 2026-08-10 UTC  
Assignment: `asg_623e2503-53e8-4319-aab3-efb46c70787e`  
Work item: `wi_5c34747f-b559-47f5-ae53-97d70f802676`  
Source examined: commit `8e2d632481b55ed6991604a275b641b9122ff46b`

## Decision and verdict

**Verdict: conditional, high confidence.** Tightbeam should make a gateway-native, capability-bound WebSocket subscription the primary interface. Ship `work_item_created` as the only V1 class. Write each event durably in the work-item creation transaction. Push it promptly to connected consumers. Use cursors for connection handoff, reconnect, and bootstrap recovery; do not turn the cursor into the primary polling product.

This is the smallest durable contract that meets the corrected need. It is not a generic event bus. It exposes no SQL filter, wildcard, table selector, prompt filter, arbitrary owner selector, or substrate-wide stream.

Approval conditions are:

1. The transport, capability issuer, owner binding, token rules, and revocation behavior below are part of V1.
2. Work-item creation, owner sequence allocation, and event insertion commit atomically.
3. The subscription pump defines the omitted-cursor cut and the replay-to-live handoff.
4. Delivery is owner-local, ordered, at least once, and recoverable after connection, pump, or gateway loss.
5. Slow consumers are closed independently. Replay work is bounded and fair.
6. The fixed reference load passes the fixed latency, isolation, and resource tests.
7. The product specification and rollout gates below exist before implementation is enabled.

## Facts proven from current source

- Tightbeam already has a gateway WebSocket. One process owns each socket, and `ConnRegistry` owns shared fan-out (`lib/tightbeam/wire/socket.ex:1-17`; `lib/tightbeam/conn_registry.ex:1-5`).
- The current WebSocket uses a closed subscription vocabulary. It accepts only `chat` and `work_state`; it rejects empty or unknown sets (`lib/tightbeam/wire/socket.ex:394-405`; `test/socket_test.exs:587-606`).
- Current live delivery is a hint. The store is truth. Publication can arrive out of order, and clients reconcile by sequence (`lib/tightbeam/conn_registry.ex:15-38`, `lib/tightbeam/conn_registry.ex:84-98`).
- The current chat handshake registers before replay, buffers concurrent pushes, drains literal duplicates, sends `sync_complete`, and then becomes live. This closes its replay-to-live race (`lib/tightbeam/wire/socket.ex:18-29`, `lib/tightbeam/wire/socket.ex:103-146`).
- The current socket sends ping every 30 seconds and closes after 90 seconds without pong (`lib/tightbeam/wire/socket.ex:35-39`, `lib/tightbeam/wire/socket.ex:151-160`).
- The current replay buffer is an in-memory list with no explicit byte or event bound in the socket handler (`lib/tightbeam/wire/socket.ex:64-85`, `lib/tightbeam/wire/socket.ex:103-116`).
- Current work-state fan-out filters by owner and class (`lib/tightbeam/conn_registry.ex:193-206`). The broader snapshot rule also admits a foreign-owned item through an assignment held by the user's session (`lib/tightbeam/work_state.ex:206-219`). The proposed external interface must not reuse that broader rule.
- Current work-item event kinds are only `metadata` and `composition`; they do not identify creation (`lib/tightbeam/work_state.ex:22-30`, `lib/tightbeam/work_state.ex:169-187`).
- Work-item creation commits before its current change callback. Doorbell insertion and publication then occur in a best-effort block that swallows exceptions (`lib/tightbeam/work_items.ex:86-143`, `lib/tightbeam/work_items.ex:171-180`; `lib/tightbeam/gateway.ex:5619-5659`). That path cannot be durable subscription truth.
- Existing tests prove that duplicate and reordered hints converge by refetching snapshots. They also prove that a dropped hint leaves a stale client until refetch (`test/work_state_test.exs:289-372`).
- Existing work queries are HTTP snapshot routes, not a filtered external event subscription (`lib/tightbeam/wire/router.ex:272-328`). The inspected gateway listener is HTTP; the source does not prove a native TLS listener (`lib/tightbeam/application.ex:67`; `lib/tightbeam/gateway.ex:325`; `lib/tightbeam/wire/router.ex:74-87`).
- Current device tokens are opaque `tbt_` bearers attached to one user. Only an allowlisted device resolves by token, and admin status is derived from its user (`lib/tightbeam/devices.ex:1-38`, `lib/tightbeam/devices.ex:119-137`). The existing WebSocket `pair` frame returns a token for an allowlisted device or `pair_pending` otherwise (`lib/tightbeam/wire/socket.ex:230-267`). The existing admin `approve-device` verb attaches a pending device to a user and mints its token; device revocation clears that token (`lib/tightbeam/gateway.ex:752-755`; `lib/tightbeam/devices.ex:148-170`, `lib/tightbeam/devices.ex:186-195`). Current HTTP device authentication reads the Authorization bearer and returns the resolved device (`lib/tightbeam/wire/router.ex:433-443`).
- Mike reports that a filesystem/WAL watcher is the current workaround and signals every database change (scope correction, 2026-08-10). This is user-observed context, not a source-proven claim.
- A source search on 2026-08-10 found no relevant filesystem/WAL watcher or SSE implementation under `lib/` or `test/`. SQLite uses WAL, and a plain database-file copy can omit committed data (`docs/BACKUP.md:9-25`, `docs/BACKUP.md:37-45`).

Everything below is a proposed V1 contract or a labeled assumption. It is not current behavior.

## Terms

- **Class:** one catalogued event kind. V1 has only `work_item_created`.
- **Capability:** a revocable bearer secret that fixes one owner, allowed classes, expiry, and connection limit.
- **Event row:** immutable durable subscription truth inserted with the work item.
- **Nudge:** an in-memory owner-and-sequence wake-up. It is not event truth.
- **Pump:** the serialized owner/class process that drains durable rows and feeds connections.
- **Incremental cursor:** a consumer checkpoint within one owner and feed epoch.
- **Bootstrap:** a bounded owner snapshot with a fixed barrier that ends in an incremental cursor.

## Assumptions

- The external process can protect a bearer secret, validate a TLS certificate and hostname, persist a cursor, deduplicate events, and reconnect.
- A supported TLS reverse proxy is available for remote V1 deployment.
- One gateway deployment owns one SQLite store and its subscription pumps.
- The closed `work_item_created` payload below is sufficient for the display; detail retrieval needs a separately authorized product route.

## Invariants

- Push is primary. Replay and bootstrap repair a push connection; they do not replace it.
- No response, frame, error detail, metric label, or timing branch discloses a foreign owner's event or existence.
- Work item and event commit atomically.
- One owner sees ascending `ownerSeq`; delivery is at least once and never silently dropped.
- The server accepts only catalogued filters already granted by the capability.
- Restore changes the feed epoch before any feed read or create.

## Non-goals

- A generic event bus, arbitrary predicates, exact-once delivery, webhooks, or database/WAL observation.
- Cross-owner or admin-merged feeds, prompt/title filtering, chat multiplexing, or historical synthetic creation events.
- SSE in V1, native TLS in V1, work-item deletion/tombstones, or implementation in this assignment.

## Open questions

None blocks V1. Later product decisions may add SSE as a second transport, delegated admin issuance, native TLS, or a deletion/tombstone class. Each requires a new versioned contract and threat review.

## Product specification home

Before implementation, place the approved normative contract at `docs/specs/focused-external-subscriptions-v1.md`. That document, protocol fixtures, and migration gates become product authority. This recon remains decision evidence and must not serve as a mutable runtime specification.

## Alternatives and tradeoffs

| Design | Prompt push | Recovery | Filter and security | Ruling |
|---|---|---|---|---|
| Native focused WebSocket | Yes; commit nudges an active pump. | Cursor replay is inside connect and reconnect. | Closed classes; a capability fixes owner and classes. | **Recommended.** Reuses current gateway connection patterns but needs the separate lifecycle below. |
| Native push plus durable recovery | This is the recommended WebSocket with its required durable half. | Atomic event rows, cursors, epoch, and bootstrap close loss windows. | Same narrow capability and frame. | **Required combination, not a competing polling design.** Push without recovery loses events; recovery without push misses the product need. |
| Companion relay | Yes, after it receives the native feed. | It persists the native cursor and owns downstream retry. | Tightbeam remains narrow; the relay holds downstream secrets. | Add only for fan-out, webhooks, browser auth, or protocol conversion. It adds a service, store, backup, audit, and deletion owner. |
| Focused SSE | Yes; one-way HTTP is simple. | `Last-Event-ID` can carry the same cursor. | Same capability and class contract. | Reasonable later transport. Current source has no SSE, and browser `EventSource` cannot set an Authorization header. |
| Cursor polling only | No continuous pushed delivery. | Simple recovery. | It can be narrow. | Reject as the primary interface. Retain only as an internal replay operation or diagnostic. |
| Filesystem/WAL watcher | Wakes on storage writes, not the requested class. | Checkpoint, rotation, backup, and restore complicate position. | Observes unrelated writes before product authorization. | **Reject.** It is broad, storage-coupled, noisy, and bypasses the supported security/schema seam. |

## Closed subscription and transport

The external subscription starts as one HTTP Upgrade request. The client sends no subscription data frame:

```http
GET /api/external-subscriptions/ws HTTP/1.1
Authorization: Bearer cap_<43 base64url characters>
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Version: 13
X-Tightbeam-Subscription-Protocol-Version: 1
X-Tightbeam-Subscription-Class: work_item_created
X-Tightbeam-Subscription-Cursor: wic_v1_...
```

`X-Tightbeam-Subscription-Cursor` is the only optional header. Every other listed application header is required exactly once. V1 requires the class header to equal the single ASCII token `work_item_created`. Repeated headers, comma lists, blank values, unknown application headers, owner fields, wildcards, predicates, prompt text, table names, and chat/work-state names fail before Upgrade.

The HTTP handler performs TLS-boundary checks, capability authentication, class authorization, cursor decoding and validation, connection admission, and pending pump registration before it returns `101 Switching Protocols`. Therefore cursor errors remain HTTP errors. After `101`, the server sends replay events followed by this frame, or sends it immediately for an omitted cursor:

```json
{"type":"subscription_ready","protocolVersion":1,"class":"work_item_created","cursor":"wic_v1_..."}
```

The ready cursor is the last owner sequence emitted or the omitted-cursor cut. The client sends only WebSocket control frames after Upgrade.

Every pre-Upgrade failure has `Content-Type: application/json` and exactly this body shape:

```json
{"type":"error","protocolVersion":1,"code":"cursor_invalid","message":"cursor is invalid"}
```

The closed HTTP mapping is:

| Status | Code | Fixed message | Cause |
|---|---|---|---|
| 400 | `invalid_subscription` | `subscription request is invalid` | class/header vocabulary is invalid |
| 400 | `cursor_invalid` | `cursor is invalid` | cursor validation fails as defined below |
| 401 | `auth_failed` | `authentication failed` | capability is missing, unknown, expired, or revoked |
| 403 | `class_not_allowed` | `subscription class is not allowed` | capability does not grant `work_item_created` |
| 410 | `cursor_expired` | `cursor has expired` | epoch or retention validation fails |
| 426 | `unsupported_protocol` | `protocol version is not supported` | protocol version is not 1 |
| 429 | `connection_limit` | `connection limit reached` | capability or owner connection limit is full |
| 503 | `server_busy` | `server is busy` | replay wait capacity is full; include `Retry-After: 1` |

The status, code, and fixed public message vary only by this table. No failure returns `101`. Post-Upgrade application closes use `4003/revoked`, `4008/slow_consumer`, and `1011/stream_restart`. A normal client close uses `1000`. A post-Upgrade internal failure never invents a cursor error; the client reconnects with its last applied cursor.

The bearer appears only in the Authorization header. It never appears in the URL, subprotocol, query string, or WebSocket frame.

Remote clients must use `wss://`. The supported V1 deployment binds the Tightbeam HTTP gateway to loopback and places an approved TLS reverse proxy in front. The proxy must use TLS 1.2 or newer, present a hostname-valid certificate, forward only to loopback, preserve the Authorization and subscription headers, omit them and all frames from logs, and set its idle timeout above the 90-second pong deadline. Plain `ws://` is allowed only from the same host to a loopback address. Startup fails if this lifecycle is enabled on a non-loopback gateway bind without a configured secure termination boundary.

## Capability issuance, scope, and token rules

The sole V1 capability-control credential is Tightbeam's existing allowlisted device bearer, prefixed `tbt_`. This is the user login for these routes. The current pairing ceremony creates or finds a device, later-device approval attaches it to a user and mints the bearer, and `device_auth` resolves an allowlisted bearer to `device.user_id` and derived `device.is_admin`. Pending, denied, unknown, and revoked devices do not authenticate.

The V1 login-to-control lifecycle is exact:

1. The device sends the existing `/ws` `pair` frame with protocol version, device id, claimed name, and device information.
2. The first device receives its `tbt_` token. A later device receives `pair_pending` until an admin runs the existing `approve-device` verb with its device id and final user id.
3. The approved device sends `pair` again. The gateway rotates and returns its `tbt_` bearer, which names the attached user for the control routes below.
4. Re-pair rotates the device bearer. `revoke-device` clears it. Either action makes the previous bearer return `401 auth_failed` on the next control request.

The proposed issuer matrix is closed:

| Caller | Mint | List | Revoke | Owner selection |
|---|---|---|---|---|
| Allowlisted non-admin device bearer | Own capabilities only | Own only | Own only | Always `device.user_id`; no request field |
| Allowlisted admin device bearer | Own capabilities only | Any, for incident response | Any, for incident response | Mint still uses `device.user_id` |
| Org bearer, agent session bearer, external `cap_` bearer, pending/denied/revoked device, or inferred identity | Denied | Denied | Denied | None |

The control wire is:

```http
POST /api/external-subscription-capabilities
Authorization: Bearer tbt_...
Content-Type: application/json

{"protocolVersion":1,"classes":["work_item_created"],"expiresAt":1788985200000,"connectionLimit":5}
```

The mint body contains exactly those four fields and cannot contain `ownerUserId`. A successful mint returns `201` and exactly:

```json
{"type":"external_subscription_capability_created","protocolVersion":1,"capabilityId":"esc_...","token":"cap_...","ownerUserId":"alice","classes":["work_item_created"],"createdAt":1786393000000,"expiresAt":1788985200000,"connectionLimit":5}
```

`GET /api/external-subscription-capabilities` returns `200` with `type`, `protocolVersion`, and a `capabilities` array. Each row contains the created response fields except `token`, plus `state` and nullable revocation fields; it omits raw bearers and token digests. A non-admin sees only rows whose owner equals `device.user_id`; an admin sees all rows. `DELETE /api/external-subscription-capabilities/:capabilityId` returns `204` with no body after an authorized revoke. A non-admin foreign id returns the same `404 capability_not_found` body as an unknown id. All three routes require HTTPS at the same TLS boundary.

Device-token revocation immediately makes later control calls return `401 auth_failed`. It does not revoke already minted external capabilities. The owner must use another allowlisted device, or an admin device must use incident-response list/revoke. This behavior is explicit so device rotation does not silently break displays.

Generate each external capability from 256 CSPRNG bits and encode it as unpadded base64url after `cap_`. Show the raw bearer once. Store only its SHA-256 digest and compare digests in constant time. Never include the raw bearer in URLs, logs, audit rows, list output, traces, or error text. Default expiry is 30 days; maximum expiry is 90 days; there is no refresh. Rotation means mint a new capability and revoke the old one.

The capability row contains public capability id, token digest, owner user id, allowed class set, creating device id and user id, creation time, expiry, revocation time and actor, and connection limit. Default limits are five active connections per capability and twenty per owner.

The only V1 event visibility predicate is:

```text
event.ownerUserId = authenticatedCapability.ownerUserId
AND event.class IN authenticatedCapability.allowedClasses
```

Admin status, creator, assignment holder, org membership, prompt content, and request fields never broaden it. The `tbt_` device bearer cannot subscribe. The `cap_` bearer cannot read item detail, open chat/work-state, invoke agent verbs, or control capabilities. Capability revocation closes active sockets with `4003/revoked` and blocks reconnect.

## Durable storage, event identity, and schema

Add these logical records under one schema/feed feature version:

```text
external_feed_state(
  singleton = 1 PRIMARY KEY,
  schemaVersion = 1,
  epoch,
  startedAt
)

external_owner_head(
  ownerUserId PRIMARY KEY,
  lastSeq
)

external_work_item_created(
  ownerUserId,
  ownerSeq,
  workItemId UNIQUE REFERENCES work_items(id) ON DELETE RESTRICT,
  occurredAt,
  createdByKind,
  createdById,
  PRIMARY KEY(ownerUserId, ownerSeq)
)
```

The epoch is 128 CSPRNG bits encoded as base64url. Sequence fields are non-negative integers. Creating a work item locks/updates its owner's head and inserts the immutable creation row in the same database transaction as the item. A keyed replay finds the existing item and does not allocate another sequence or emit another event. The event dedupe identity is `(epoch, ownerSeq)`; `workItemId` is semantic identity.

The closed V1 frame is:

```json
{
  "type": "subscription_event",
  "class": "work_item_created",
  "schemaVersion": 1,
  "eventId": {"epoch": "wice_...", "seq": 7},
  "workItemId": "wi_...",
  "occurredAt": 1786385852977,
  "createdBy": {"kind": "user", "id": "mike"}
}
```

It contains no title, prompt, assignment, owner id, org id, or arbitrary row data. A schema version never changes meaning. The Upgrade header declares protocol V1; unsupported protocol or event versions fail closed before registration.

## Cursor vocabulary and errors

Cursors are base64url encodings of canonical versioned fields. They are checkpoints, not authority; the authenticated capability supplies authority.

An incremental cursor contains exactly:

```json
{"type":"incremental","version":1,"epoch":"wice_...","ownerUserId":"u_...","seq":7}
```

A bootstrap page cursor contains exactly:

```json
{
  "type":"bootstrap",
  "version":1,
  "epoch":"wice_...",
  "ownerUserId":"u_...",
  "barrier":7,
  "afterCreatedAt":1786385852977,
  "afterId":"wi_..."
}
```

The decoder rejects extra fields and non-canonical encodings. The pre-Upgrade handler and the HTTPS bootstrap endpoint return:

- `400 cursor_invalid` for malformed data, wrong type or version, wrong owner, negative sequence, a same-epoch incremental sequence above the current owner head, or a bootstrap barrier above that head.
- `410 cursor_expired` for a well-formed non-current epoch or a sequence below the published first valid sequence.

V1 retains creation rows while the work item exists, so `firstValidSeq = 0`. An owner with no event row has `head = 0`. The server gives the same public error shape and bounded timing for wrong-owner and foreign-owner probes.

## Bootstrap and zero-event handoff

Bootstrap is this exact read-only HTTPS request. It uses the external `cap_` bearer, not a `tbt_` device bearer:

```http
POST /api/external-subscriptions/work-item-created/bootstrap HTTP/1.1
Authorization: Bearer cap_...
Content-Type: application/json
X-Tightbeam-Subscription-Protocol-Version: 1

{"limit":50}
```

A continuation body is exactly `{"limit":50,"cursor":"wib_v1_..."}`. `limit` is required and must be an integer from 1 through 50. `cursor` is optional only on the first request. Extra, repeated, null, or wrong-type fields return `400 invalid_request`. The endpoint never accepts an owner or class field. The capability must grant `work_item_created`.

Every successful page returns `200` and exactly:

```json
{
  "type":"bootstrap_page",
  "protocolVersion":1,
  "class":"work_item_created",
  "items":[{"workItemId":"wi_...","createdAt":1786385852977}],
  "nextBootstrapCursor":"wib_v1_...",
  "finalIncrementalCursor":null
}
```

Both cursor fields are always present. A non-final page has a non-null `nextBootstrapCursor` and null `finalIncrementalCursor`. A final page has null `nextBootstrapCursor` and the exact incremental cursor at the barrier. `items` contains zero through `limit` entries with only `workItemId` and `createdAt`.

The endpoint uses the same fixed error envelope as the pre-Upgrade handler. Its closed mapping is:

| Status | Code | Fixed message | Cause |
|---|---|---|---|
| 400 | `invalid_request` | `request is invalid` | body or field validation fails |
| 400 | `cursor_invalid` | `cursor is invalid` | cursor validation fails |
| 401 | `auth_failed` | `authentication failed` | capability is missing, unknown, expired, or revoked |
| 403 | `class_not_allowed` | `subscription class is not allowed` | capability does not grant the endpoint class |
| 410 | `cursor_expired` | `cursor has expired` | epoch or retention validation fails |
| 426 | `unsupported_protocol` | `protocol version is not supported` | protocol version is not 1 |
| 503 | `server_busy` | `server is busy` | bootstrap capacity is full; include `Retry-After: 1` |

It never returns WebSocket close codes.

On the first page, one read transaction captures the current epoch and `COALESCE(ownerHead, 0)` as fixed `barrier`. Every page includes:

1. owner items created before event recording existed, identified by no creation row; and
2. owner items with a creation row whose `ownerSeq <= barrier`.

Pages use immutable order `(createdAt, id)`, read `limit + 1`, return at most `limit`, and carry the same epoch, owner, and barrier in the next bootstrap cursor. Items created after the barrier are excluded from every bootstrap page. The final page returns incremental cursor `{type: incremental, version: 1, epoch, ownerUserId, seq: barrier}`.

This rule works when the event table is empty, when the owner has only pre-feature items, and when the captured barrier is zero. A new item after the barrier is delivered by replay or push from `seq > barrier`; it cannot fall between bootstrap and subscription.

A supported restore rotates the epoch before any feed read or work-item create. An old incremental or bootstrap cursor then returns HTTP `410 cursor_expired`. The client starts bootstrap in the new epoch.

## Prompt push, omitted cursor, replay, and handoff

The event row is truth. After commit, the writer performs only a nonblocking process send/cast with owner and sequence. It never performs a socket write or feed drain in the transaction. If no pump exists or the pump crashes, the row remains durable.

One serialized pump exists per active `(owner, class)`. It owns `lastDrainedSeq` and uses indexed ascending reads. Nudge order does not define event order; several nudges can collapse into one drain.

An omitted cursor means “future events after the connection's linearization cut,” not “current snapshot.” The pre-Upgrade handler asks the pump to handle omitted-cursor registration as one serialized operation:

1. authenticate and reserve admission, then read current epoch and owner head;
2. install the connection as pending at that head before the pump handles any later queued nudge; and
3. return `101`, then send `subscription_ready` with that exact incremental cursor.

The database head read is the cut. A commit at or before the cut is intentionally excluded. A commit after the cut either queues a nudge behind registration or is found by the next durable drain. If the caller needs existing state, it must bootstrap first.

For a supplied cursor, the pump installs the connection as pending before replay. Replay reads rows after the cursor in fixed pages, drains through the pump's current head, sends `subscription_ready` with the last emitted cursor, and then attaches live at that same head. If the pump advances during replay, the connection drains that exact interval before live attach.

An event created during handshake can appear in replay or the immediate live drain. It can repeat after an ambiguous network break, but it cannot disappear. The client persists a cursor only after applying the event and deduplicates by `(epoch, seq)`.

Each active owner/class pump compares its last drained sequence with the durable head once per 30-second heartbeat. A mismatch drains rows. This backstop repairs a lost nudge while push remains the prompt path.

## Crash recovery, slow consumers, fairness, and limits

The pump enqueues frames to independent per-connection queues in O(1) work and never writes synchronously to a socket. Each queue is bounded at 256 events or 1 MiB, whichever comes first. Overflow closes only that socket with `4008/slow_consumer`; no durable row is deleted or marked delivered. A healthy sibling continues without waiting.

Pump processes are supervised. A pump crash closes its associated sockets with `1011/stream_restart`; restart rebuilds state from durable head/event rows, and clients reconnect from applied cursors. A gateway crash produces EOF; atomic rows survive and reconnect replays them. A crash after commit but before nudge is repaired by reconnect replay or the heartbeat head check.

Replay uses a fixed global scheduler:

- at most four replay connections may execute; at most 100 more wait;
- excess opens fail before Upgrade with HTTP `503 server_busy` and `Retry-After: 1`; they do not advance a cursor;
- one scheduler turn reads 51 indexed rows and emits at most 50 for one connection;
- turns are round-robin across capability and owner, yield after every page, and service live drains before the next replay round.

These rules prevent one recovery or owner from monopolizing the serialized database connection. Connection admission returns `connection_limit`; it never evicts another consumer silently. Keep the current 30-second ping and 90-second pong timeout.

## Fixed reference load and release thresholds

The release test is closed, not a target-discovery exercise:

- dedicated Linux host, 4 pinned vCPU, 8 GiB RAM, local NVMe SSD, and no competing workload;
- the production BEAM release build and production SQLite settings, including WAL, foreign keys, and normal synchronous mode;
- 1,000,000 foreign-owner work items plus 100,000 retained target-owner event rows, each encoded frame below 1 KiB;
- 20 target owners, 100 caught-up live connections (five per owner), and 20 creates/second evenly distributed for 10 minutes;
- at minute two, eight recovering consumers each replay 10,000 events; four execute and four wait under the fixed scheduler;
- no injected network latency between proxy and client.

It passes only if: no missing or foreign event occurs; each owner remains ordered; caught-up consumers meet commit-to-first-socket-write p95 at or below 250 ms and p99 at or below 1 second; create-transaction p99 increases by at most 10 ms versus the same dataset/build with the external feature disabled; the sum of BEAM process memory reported for pumps, socket queues, and replay scheduling stays at or below 160 MiB; no connection exceeds 256 queued events or 1 MiB; and every recovering consumer converges. Failure blocks release and returns the design to product review. It does not revise the thresholds automatically.

## Audit, schema compatibility, operations, and deletion

Durably audit capability mint, revoke, expiry, denied authentication, and non-empty delivery batches. Operational logs record public capability id, owner, class, cursor, replay count, queue overflow, latency, close reason, and last sent cursor. Logs and metrics omit raw bearers and item content.

Expose active/waiting connections, connects, reconnects, sent/replayed events, auth and subscription failures, cursor expiry, queue depth, slow-consumer closes, replay turns, nudge-to-write latency, and heartbeat head mismatches.

V1 has no event purge or work-item deletion. The creation-row foreign key is restrictive. A future deletion design must define a separate tombstone class, cursor advancement, retention gaps, and downstream-copy duties before relaxing it. Capability deletion/revocation closes sockets but cannot erase already delivered external copies. A companion owns deletion from its own store and sinks.

## Migration and mixed-version behavior

1. Add the capability, singleton feed state, owner head, and creation tables under an additive schema migration. Keep capability mint and external endpoints disabled.
2. Initialize a fresh epoch and schema/feed feature version. Do not synthesize historical creation events; bootstrap covers existing owner state.
3. Enable and validate atomic event writes, indexes, crash recovery, and the fixed load suite while external access remains disabled.
4. Enable owner capability management, then the external WebSocket, behind one deployment feature gate.
5. Observe audit, latency, queue, replay, and isolation thresholds before broad availability.

Current chat/work-state clients and frames do not change. External protocol V1 rejects other versions. An old gateway does not understand external capabilities and must not expose the lifecycle. Once capability issuance is enabled, rollback to a writer that omits atomic event rows is prohibited by a boot/deploy schema-feature compatibility gate. Emergency rollback disables external subscription and capability mint; re-enable rotates the epoch and requires client bootstrap.

## Deterministic acceptance tests

1. Fail creation before commit; prove no item, event, or push. Commit once; prove one item, one atomic event row, and one prompt push. Replay a keyed create; prove no new sequence or push.
2. Create Alice, Bob, Alice; prove Alice receives only owner sequences 1 and 2 and no observable evidence of Bob in frames, errors, timing buckets, logs, or metrics.
3. Send each invalid Upgrade header case: unknown class, wildcard, repeated or empty header, chat class, owner/predicate header, extra application header, or bad protocol. Prove the exact HTTP status/error envelope, no `101`, and no pump registration.
4. Send the existing pair frame for a later device and prove `pair_pending` cannot control capabilities. Run `approve-device` for Alice, pair again, mint with the returned `tbt_` bearer, and prove owner derives as Alice. Re-pair and prove the previous bearer fails. Prove an owner field is rejected; org/session/`cap_`/revoked device bearers fail; an admin device can list/revoke foreign capabilities but cannot mint for another owner.
5. Revoke the minting device; prove control calls return `401` while its existing `cap_` remains usable until separately revoked. Prove the capability has 256 CSPRNG bits, only its digest is stored, comparisons are constant time, list/audit/proxy/app logs omit it, and capability revoke closes with `4003`.
6. Prove remote plain `ws://` and external non-loopback bind without secure termination fail. Prove valid `wss://` through the configured proxy works with certificate and hostname validation.
7. Exercise the exact bootstrap POST with initial and continuation bodies. Prove response field closure, mutually exclusive cursors, limit bounds, stable `(createdAt,id)` order, no foreign fields/items, and a final sequence-zero incremental cursor when no event rows exist.
8. Pause bootstrap after its barrier, create an item, finish bootstrap, and subscribe with its final cursor; prove the new item arrives exactly by replay/push and is not skipped.
9. Supply malformed, extra-field, wrong-version, wrong-owner, negative, above-head, expired-epoch, and below-retention cursors to both bootstrap and Upgrade. Prove exact HTTP `400 cursor_invalid` or `410 cursor_expired`, fixed JSON envelopes, no `101` on Upgrade, and no foreign disclosure.
10. Omit the Upgrade cursor and pause the pump on both sides of its pre-`101` head-read cut. Prove a pre-cut event is excluded and a post-cut event is pushed. Bootstrap-first proves both current state and later event.
11. Register pending, pause replay, create an event, and resume. Prove it appears before `subscription_ready` or in the immediate live drain, never zero times. Reverse and collapse nudges; prove ascending durable order.
12. Drop a nudge; advance one heartbeat; prove head mismatch drains the row. Crash after commit before nudge; prove reconnect replay recovers it.
13. Crash the owner pump during replay; prove affected sockets close with `1011/stream_restart`, healthy owners continue, and reconnect converges. Crash the gateway before and after socket write; prove EOF, at-least-once replay, and stable dedupe identity.
14. Block one socket and fill its exact queue bound; prove only it closes with `4008/slow_consumer`, a healthy sibling continues within latency thresholds, and reconnect converges.
15. Start five replay consumers plus live traffic; prove only four execute, page turns are round-robin, live drains run before the next round, and the fifth waits. Fill 100 wait slots; prove the next Upgrade gets HTTP `503 server_busy`, `Retry-After: 1`, and no cursor advance.
16. Exceed per-capability and per-owner limits; prove pre-Upgrade HTTP `429 connection_limit` and no unrelated eviction. Revoke with active sockets; prove `4003/revoked` and denied reconnect.
17. Restore a stale backup through the supported ceremony; prove epoch rotates before access, old incremental/bootstrap cursors expire, zero-event bootstrap succeeds, and new-epoch reconnect resumes.
18. Prove every frame matches the closed V1 schema and contains no title, prompt, owner id, assignment, or arbitrary substrate row.
19. Run the exact reference load; prove every fixed correctness, latency, writer-overhead, fairness, convergence, and memory threshold. Any failure blocks release.
20. Exercise mixed deployment: old clients remain unaffected; unsupported external version fails closed; rollback gate rejects an old writer after issuance; emergency disable/re-enable rotates epoch and forces bootstrap.

## Review finding reconciliation

- **B1 owner credential:** closed by the existing allowlisted `tbt_` device bearer, its pairing/approval/revocation lifecycle, exact owner derivation, closed issuer matrix and control wire, and tests 4–6. The separate TLS, token, and revocation rules remain unchanged.
- **B2 wire and recovery:** closed by pre-Upgrade cursor validation with exact HTTP errors, the exact HTTPS bootstrap request/response/error wire, and tests 3 and 7–13. The reviewed storage, cursor fields, barrier, zero-event, restore, and cut rules remain unchanged.
- **I3 queue/crash/load determinism:** closed by nonblocking enqueue, independent queues, supervised pump/gateway recovery, fixed replay scheduler, fixed reference load, and tests 12–15 and 19.
- **I4 specification/migration:** closed by Terms, Assumptions, Invariants, Non-goals, Open Questions, spec home, staged migration, version negotiation, and rollback gate.
- **N5 citation:** the closed-vocabulary claim now cites `lib/tightbeam/wire/socket.ex:394-405`.

## Formal recommendation

Approve implementation planning only for the V1 contract above: a focused, capability-bound WebSocket push subscription with durable owner-local event rows and cursor-based recovery. Reject polling-only and filesystem/WAL watching as the product interface. Treat replay as a required repair mechanism behind push. Add a companion only when a named integration needs fan-out or protocol conversion, and keep it downstream of this same narrow native contract.
