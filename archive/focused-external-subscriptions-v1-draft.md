# Focused external subscriptions V1

Status: Normative product specification. Implementation awaits independent approval of this specification.

Authority:

- Work item: `wi_5c34747f-b559-47f5-ae53-97d70f802676`
- Reviewed artifact: `art_7450257b`
- Artifact SHA-256: `3e0cd6dfaafa978d2e3b5e7a8d409f56cec5b609736087e462046d3721ac0e3a`
- Artifact path: `/home/mike/.tightbeam/work/f6e67cc81f7b/filtered-external-push-subscriptions-recon-v3.md`
- Recon producer: `asg_623e2503-53e8-4319-aab3-efb46c70787e`
- Independent reviewed-clean verdict: `att_d3f75911-91d7-4199-a8ef-14fb05279dbc`
- Source base reviewed by the recon: `8e2d632481b55ed6991604a275b641b9122ff46b`
- Product source head when this specification was written: `ac8651dcb104f312da1c67e0cb7b1abebc640b2b`

`SHALL` marks a V1 requirement. The source facts and assumptions do not describe required behavior.

## Goal

G1. Tightbeam SHALL provide a gateway-native external subscription for the `work_item_created` class.

G2. The subscription SHALL push matching events to a connected consumer after the event transaction commits.

G3. Tightbeam SHALL use durable event rows and cursors for connection handoff and recovery.

G4. Tightbeam SHALL keep owner authorization and the class vocabulary closed.

G5. Tightbeam SHALL make external access broadly available only after the migration gates and Acceptance section pass.

## Non-Goals

N1. V1 does not provide a generic event bus, arbitrary predicates, exact-once delivery, webhooks, or database observation.

N2. V1 does not provide cross-owner feeds, admin-merged feeds, prompt filters, title filters, or historical synthetic creation events.

N3. V1 does not multiplex chat or work-state traffic on the external subscription.

N4. V1 does not provide SSE, native TLS termination, or work-item tombstones.

N5. V1 does not make polling the primary product interface.

N6. V1 does not make a filesystem or WAL watcher a supported product interface.

N7. V1 does not add a companion relay. A later product can add one for named fan-out or protocol-conversion needs.

N8. This specification does not authorize implementation or deployment.

## Terms

T1. **Class** means one catalogued event kind. V1 contains only `work_item_created`.

T2. **Capability** means a revocable bearer secret. It fixes one owner, a class set, an expiry, and a connection limit.

T3. **Event row** means immutable subscription truth. Tightbeam inserts it in the work-item creation transaction.

T4. **Nudge** means an in-memory owner-and-sequence wake-up. A nudge is not event truth.

T5. **Pump** means the serialized process for one active owner and class. It drains durable rows and feeds connections.

T6. **Incremental cursor** means a consumer checkpoint within one owner and feed epoch.

T7. **Bootstrap** means a bounded owner snapshot. It uses a fixed barrier and ends with an incremental cursor.

T8. **Omitted-cursor cut** means the durable owner head that the pump reads during serialized registration.

T9. **Applied cursor** means the last cursor that a client persisted after it applied the corresponding event.

T10. **Current source** means product commit `ac8651dcb104f312da1c67e0cb7b1abebc640b2b` for this specification.

## Assumptions

A1. The external process can protect a bearer secret.

A2. The external process can validate a TLS certificate and hostname.

A3. The external process can persist a cursor, deduplicate events, and reconnect.

A4. A supported TLS reverse proxy is available for a remote V1 deployment.

A5. One gateway deployment owns one SQLite store and its subscription pumps.

A6. The closed `work_item_created` payload is sufficient for the target display.

A7. Item detail retrieval uses a separate authorized product route.

### Current factual background

These facts are indicative. They do not create V1 requirements.

F1. Tightbeam has a gateway WebSocket. One process owns each socket. `ConnRegistry` owns shared fan-out.

F2. The current WebSocket uses a closed subscription vocabulary. It accepts `chat` and `work_state` only.

F3. The current store is truth for live delivery. Current clients reconcile reordered hints by sequence.

F4. The current chat handshake registers before replay. It buffers pushes and drains duplicates before live delivery.

F5. The current socket sends ping every 30 seconds. It closes after 90 seconds without pong.

F6. The current socket replay buffer has no explicit byte or event bound.

F7. Current work-state fan-out filters by owner and class. Snapshot visibility also has a broader assignment rule.

F8. Current work-item event kinds do not identify work-item creation.

F9. Current work-item creation commits before its best-effort change callback. The callback swallows publication failures.

F10. Existing HTTP work queries return snapshots. They do not provide a filtered external subscription.

F11. The gateway listener is HTTP. Current source does not prove a native TLS listener.

F12. Current device tokens are opaque `tbt_` bearers attached to one user. Only an allowlisted device resolves by token.

F13. The current pairing, approval, re-pair, and revoke paths provide the V1 control-login lifecycle.

F14. Mike reports that the current filesystem or WAL workaround signals each database change.

F15. Source search found no relevant filesystem watcher, WAL watcher, or SSE implementation.

F16. SQLite uses WAL. A plain database-file copy can omit committed data.

The recon proved F1-F16 at source base `8e2d632481b55ed6991604a275b641b9122ff46b`. The source base is an ancestor of T10 by 38 commits. The cited files are byte-identical across those commits except `application.ex` and `gateway.ex`. Their changes concern session caps and supervision checkpoints. Their HTTP listener, device control, and best-effort publication behavior remain unchanged.

| Facts | Evidence at the reviewed source base |
|---|---|
| F1 | `lib/tightbeam/wire/socket.ex:1-17`; `lib/tightbeam/conn_registry.ex:1-5` |
| F2 | `lib/tightbeam/wire/socket.ex:394-405`; `test/socket_test.exs:587-606` |
| F3 | `lib/tightbeam/conn_registry.ex:15-38`; `lib/tightbeam/conn_registry.ex:84-98` |
| F4 | `lib/tightbeam/wire/socket.ex:18-29`; `lib/tightbeam/wire/socket.ex:103-146` |
| F5 | `lib/tightbeam/wire/socket.ex:35-39`; `lib/tightbeam/wire/socket.ex:151-160` |
| F6 | `lib/tightbeam/wire/socket.ex:64-85`; `lib/tightbeam/wire/socket.ex:103-116` |
| F7 | `lib/tightbeam/conn_registry.ex:193-206`; `lib/tightbeam/work_state.ex:206-219` |
| F8 | `lib/tightbeam/work_state.ex:22-30`; `lib/tightbeam/work_state.ex:169-187` |
| F9 | `lib/tightbeam/work_items.ex:86-143`; `lib/tightbeam/work_items.ex:171-180`; `lib/tightbeam/gateway.ex:5619-5659` |
| F10 | `lib/tightbeam/wire/router.ex:272-328` |
| F11 | `lib/tightbeam/application.ex:67`; `lib/tightbeam/gateway.ex:325`; `lib/tightbeam/wire/router.ex:74-87` |
| F12-F13 | `lib/tightbeam/devices.ex:1-38`; `lib/tightbeam/devices.ex:119-195`; `lib/tightbeam/wire/socket.ex:230-267`; `lib/tightbeam/gateway.ex:752-765`; `lib/tightbeam/wire/router.ex:433-443` |
| F14 | Mike's scope correction on 2026-08-10 |
| F15 | Recon source search on 2026-08-10 |
| F16 | `docs/BACKUP.md:9-25`; `docs/BACKUP.md:37-45` |

## Invariants

I1. Push SHALL remain the primary interface. Replay and bootstrap SHALL repair a push connection.

I2. A response, frame, error, metric label, log, or timing branch SHALL NOT disclose another owner's event or existence.

I3. A work item and its event row SHALL commit in one transaction.

I4. Tightbeam SHALL deliver one owner's events in ascending `ownerSeq` order.

I5. Delivery SHALL be at least once. Tightbeam SHALL NOT silently drop a committed event.

I6. The server SHALL accept only catalogued classes that the capability grants.

I7. A supported restore SHALL change the feed epoch before a feed read or work-item creation.

I8. The event row SHALL remain delivery truth. A nudge SHALL remain a non-durable prompt.

I9. The capability owner SHALL be the only owner authority for an external feed.

I10. The system SHALL keep event truth independent from a consumer's readiness, projection, or display policy.

## Architecture

### A. Product boundary and alternatives

AR1. Tightbeam SHALL use the native focused WebSocket as the V1 transport.

AR2. Tightbeam SHALL combine WebSocket push with durable replay and bootstrap recovery.

AR3. Tightbeam SHALL keep polling as an internal replay operation or diagnostic only.

AR4. Tightbeam SHALL reject filesystem and WAL observation as a product interface.

AR5. A later companion relay SHALL consume this same narrow native feed.

AR6. A later SSE transport SHALL use a new versioned contract and threat review.

### B. WebSocket request and response

AR7. The external subscription SHALL start with this HTTP Upgrade request:

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

AR8. `X-Tightbeam-Subscription-Cursor` SHALL be the only optional application header in AR7.

AR9. The class header SHALL equal the ASCII token `work_item_created`.

AR10. The handler SHALL reject repeated headers, comma lists, blank values, and unknown application headers.

AR11. The handler SHALL reject owner fields, wildcards, predicates, prompt text, table names, chat names, and work-state names.

AR12. The client SHALL send no subscription data frame.

AR13. Before `101`, the handler SHALL complete the TLS-boundary check, capability authentication, and class authorization.

AR14. Before `101`, the handler SHALL complete cursor validation, connection admission, and pending pump registration.

AR15. After `101`, the server SHALL send replay events before `subscription_ready`.

AR16. For an omitted cursor, the server SHALL send `subscription_ready` immediately after `101`.

AR17. The server SHALL use this ready frame:

```json
{"type":"subscription_ready","protocolVersion":1,"class":"work_item_created","cursor":"wic_v1_..."}
```

AR18. The ready cursor SHALL identify the last emitted owner sequence or the omitted-cursor cut.

AR19. After Upgrade, the client SHALL send WebSocket control frames only.

AR20. Each pre-Upgrade failure SHALL set `Content-Type: application/json`.

AR21. Each pre-Upgrade failure body SHALL contain only `type`, `protocolVersion`, `code`, and `message`.

AR21a. `type` SHALL equal `error`. `protocolVersion` SHALL equal `1`.

AR21b. `code` and `message` SHALL use the matching AR22 values.

This example shows the required shape:

```json
{"type":"error","protocolVersion":1,"code":"cursor_invalid","message":"cursor is invalid"}
```

AR22. The pre-Upgrade handler SHALL use this closed failure mapping:

| Status | Code | Fixed message | Cause |
|---|---|---|---|
| 400 | `invalid_subscription` | `subscription request is invalid` | class or header vocabulary is invalid |
| 400 | `cursor_invalid` | `cursor is invalid` | cursor validation fails under AR95-AR109 |
| 401 | `auth_failed` | `authentication failed` | capability is missing, unknown, expired, or revoked |
| 403 | `class_not_allowed` | `subscription class is not allowed` | capability does not grant `work_item_created` |
| 410 | `cursor_expired` | `cursor has expired` | epoch or retention validation fails |
| 426 | `unsupported_protocol` | `protocol version is not supported` | protocol version is not 1 |
| 429 | `connection_limit` | `connection limit reached` | capability or owner connection limit is full |
| 503 | `server_busy` | `server is busy` | replay wait capacity is full; include `Retry-After: 1` |

AR23. The status, code, and public message SHALL vary only by AR22.

AR24. A failed Upgrade SHALL NOT return `101`.

AR25. The server SHALL use `4003/revoked` after capability revocation.

AR26. The server SHALL use `4008/slow_consumer` after a queue overflow.

AR27. The server SHALL use `1011/stream_restart` after a pump restart.

AR28. The server SHALL use `1000` for a normal client close.

AR29. A post-Upgrade internal failure SHALL NOT create a cursor error.

AR30. After a post-Upgrade internal failure, the client SHALL reconnect with its last applied cursor.

AR31. The bearer SHALL appear only in the Authorization header.

AR32. The bearer SHALL NOT appear in a URL, subprotocol, query string, or WebSocket frame.

### C. Secure transport

AR33. A remote client SHALL use `wss://`.

AR34. A remote V1 deployment SHALL bind the Tightbeam HTTP gateway to loopback.

AR35. A remote V1 deployment SHALL place an approved TLS reverse proxy before the gateway.

AR36. The proxy SHALL use TLS 1.2 or newer.

AR37. The proxy SHALL present a certificate that is valid for the requested hostname.

AR38. The proxy SHALL forward only to loopback.

AR39. The proxy SHALL preserve the Authorization and subscription headers.

AR40. The proxy SHALL omit the Authorization header, subscription headers, and frames from its logs.

AR41. The proxy idle timeout SHALL exceed the 90-second pong deadline.

AR42. A same-host client MAY use plain `ws://` only with a loopback address.

AR43. Startup SHALL fail when the lifecycle is enabled on a non-loopback bind without a configured secure termination boundary.

### D. Control login and capability lifecycle

AR44. The sole V1 capability-control credential SHALL be an existing allowlisted `tbt_` device bearer.

AR45. A pending, denied, unknown, or revoked device SHALL NOT authenticate.

AR46. The login-to-control lifecycle SHALL use this sequence:

1. The device sends the existing `/ws` `pair` frame with protocol version, device id, claimed name, and device information.
2. The first device receives its `tbt_` token. A later device receives `pair_pending`.
3. An admin runs the existing `approve-device` verb with the later device id and final user id.
4. The approved device sends `pair` again. The gateway rotates and returns its `tbt_` bearer.
5. A re-pair rotates the device bearer. `revoke-device` clears it.
6. The previous bearer returns `401 auth_failed` on the next control request.

AR47. The control routes SHALL use this closed issuer matrix:

| Caller | Mint | List | Revoke | Owner selection |
|---|---|---|---|---|
| Allowlisted non-admin device bearer | Own capabilities only | Own only | Own only | `device.user_id`; no request field |
| Allowlisted admin device bearer | Own capabilities only | Any, for incident response | Any, for incident response | Mint uses `device.user_id` |
| Org bearer, agent session bearer, external `cap_` bearer, pending device, denied device, revoked device, or inferred identity | Denied | Denied | Denied | None |

AR48. Capability mint SHALL use this request:

```http
POST /api/external-subscription-capabilities
Authorization: Bearer tbt_...
Content-Type: application/json

{"protocolVersion":1,"classes":["work_item_created"],"expiresAt":1788985200000,"connectionLimit":5}
```

AR49. The mint body SHALL contain exactly the four fields in AR48.

AR50. The mint body SHALL NOT contain `ownerUserId`.

AR51. A successful mint SHALL return HTTP `201` and exactly this shape:

```json
{"type":"external_subscription_capability_created","protocolVersion":1,"capabilityId":"esc_...","token":"cap_...","ownerUserId":"alice","classes":["work_item_created"],"createdAt":1786393000000,"expiresAt":1788985200000,"connectionLimit":5}
```

AR52. `GET /api/external-subscription-capabilities` SHALL return HTTP `200`.

AR53. Its body SHALL contain `type`, `protocolVersion`, and a `capabilities` array.

AR54. Each array row SHALL contain the AR51 fields except `token`.

AR55. Each array row SHALL add `state` and nullable revocation fields.

AR56. Each array row SHALL omit raw bearers and token digests.

AR57. A non-admin list SHALL include only rows owned by `device.user_id`.

AR58. An admin list SHALL include every capability row.

AR59. `DELETE /api/external-subscription-capabilities/:capabilityId` SHALL return HTTP `204` with no body after an authorized revoke.

AR60. A non-admin foreign id SHALL return the same `404 capability_not_found` body as an unknown id.

AR61. The three control routes SHALL use HTTPS at the AR35 TLS boundary.

AR62. Device-token revocation SHALL make later control calls return `401 auth_failed`.

AR63. Device-token revocation SHALL NOT revoke an external capability that the device minted.

AR64. The owner SHALL use another allowlisted device to manage a surviving capability.

AR65. An admin device MAY list or revoke a surviving capability for incident response.

AR66. Tightbeam SHALL generate each external capability from 256 CSPRNG bits.

AR67. Tightbeam SHALL encode the capability as unpadded base64url after `cap_`.

AR68. Tightbeam SHALL show the raw bearer once.

AR69. Tightbeam SHALL store only the SHA-256 digest of the bearer.

AR70. Tightbeam SHALL compare bearer digests in constant time.

AR71. Tightbeam SHALL omit the raw bearer from URLs, logs, audit rows, list output, traces, and errors.

AR72. The default expiry SHALL be 30 days. The maximum expiry SHALL be 90 days.

AR73. V1 SHALL NOT refresh a capability. Rotation SHALL mint a new capability and revoke the old capability.

AR74. A capability row SHALL contain the public capability id, token digest, owner user id, and allowed class set.

AR75. A capability row SHALL contain the creating device id, creating user id, creation time, expiry, connection limit, revocation time, and revocation actor.

AR76. The default limit SHALL be five active connections per capability.

AR77. The default limit SHALL be twenty active connections per owner.

AR78. The event visibility predicate SHALL be exactly:

```text
event.ownerUserId = authenticatedCapability.ownerUserId
AND event.class IN authenticatedCapability.allowedClasses
```

AR79. Admin status, creator, assignment holder, org membership, prompt content, and request fields SHALL NOT broaden AR78.

AR80. A `tbt_` device bearer SHALL NOT subscribe.

AR81. A `cap_` bearer SHALL NOT read item detail, open chat, open work-state, invoke agent verbs, or control capabilities.

AR82. Capability revocation SHALL close active sockets with `4003/revoked` and block reconnect.

### E. Durable event storage and frame schema

AR83. V1 SHALL add these logical records under one schema and feed feature version:

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

AR84. The epoch SHALL contain 128 CSPRNG bits encoded as base64url.

AR85. Sequence fields SHALL be non-negative integers.

AR86. Work-item creation SHALL lock the owner's head in the work-item transaction.

AR86a. Work-item creation SHALL increment the owner's head by one and use the result as `ownerSeq`.

AR86b. Work-item creation SHALL insert its event row in the same transaction.

AR87. A keyed replay SHALL return the existing item without allocating a sequence or emitting an event.

AR88. The event dedupe identity SHALL be `(epoch, ownerSeq)`.

AR89. `workItemId` SHALL be the semantic identity.

AR90. The closed V1 event frame SHALL be:

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

AR91. The event frame SHALL NOT contain a title, prompt, assignment, owner id, org id, or arbitrary row data.

AR92. One schema version SHALL keep one meaning.

AR93. The Upgrade header SHALL declare protocol V1.

AR94. The server SHALL reject an unsupported protocol or event version before registration.

### F. Cursor vocabulary and validation

AR95. Cursors SHALL be base64url encodings of canonical versioned fields.

AR96. A cursor SHALL be a checkpoint. The authenticated capability SHALL remain the authority.

AR97. An incremental cursor SHALL contain exactly:

```json
{"type":"incremental","version":1,"epoch":"wice_...","ownerUserId":"u_...","seq":7}
```

AR98. A bootstrap page cursor SHALL contain exactly:

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

AR99. The decoder SHALL reject extra fields and non-canonical encodings.

AR100. The Upgrade handler and bootstrap endpoint SHALL return `400 cursor_invalid` for malformed cursor data.

AR101. They SHALL return `400 cursor_invalid` for a wrong type, wrong version, wrong owner, or negative sequence.

AR102. They SHALL return `400 cursor_invalid` for a same-epoch incremental sequence above the owner head.

AR103. They SHALL return `400 cursor_invalid` for a bootstrap barrier above the owner head.

AR104. They SHALL return `410 cursor_expired` for a well-formed non-current epoch.

AR105. They SHALL return `410 cursor_expired` for a sequence below the published first valid sequence.

AR106. V1 SHALL retain a creation row while its work item exists.

AR107. V1 SHALL publish `firstValidSeq = 0`.

AR108. The server SHALL treat an owner with no event row as `head = 0`.

AR109. The server SHALL use the same public error and bounded timing for wrong-owner and foreign-owner probes.

### G. Bootstrap

AR110. Bootstrap SHALL use this read-only HTTPS request with the external `cap_` bearer:

```http
POST /api/external-subscriptions/work-item-created/bootstrap HTTP/1.1
Authorization: Bearer cap_...
Content-Type: application/json
X-Tightbeam-Subscription-Protocol-Version: 1

{"limit":50}
```

AR111. A continuation body SHALL be exactly `{"limit":50,"cursor":"wib_v1_..."}`.

AR112. `limit` SHALL be an integer from 1 through 50.

AR113. `cursor` SHALL be optional only on the first request.

AR114. Extra, repeated, null, or wrong-type fields SHALL return `400 invalid_request`.

AR115. The endpoint SHALL NOT accept an owner or class field.

AR116. The capability SHALL grant `work_item_created`.

AR117. A successful page SHALL return HTTP `200` and exactly this shape:

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

AR118. Both cursor fields SHALL be present.

AR119. A non-final page SHALL have a non-null `nextBootstrapCursor` and a null `finalIncrementalCursor`.

AR120. A final page SHALL have a null `nextBootstrapCursor` and the incremental cursor at the barrier.

AR121. `items` SHALL contain zero through `limit` entries.

AR122. Each item SHALL contain only `workItemId` and `createdAt`.

AR123. Bootstrap SHALL use the AR21 error envelope.

AR124. Bootstrap SHALL use this closed error mapping:

| Status | Code | Fixed message | Cause |
|---|---|---|---|
| 400 | `invalid_request` | `request is invalid` | body or field validation fails |
| 400 | `cursor_invalid` | `cursor is invalid` | cursor validation fails |
| 401 | `auth_failed` | `authentication failed` | capability is missing, unknown, expired, or revoked |
| 403 | `class_not_allowed` | `subscription class is not allowed` | capability does not grant the endpoint class |
| 410 | `cursor_expired` | `cursor has expired` | epoch or retention validation fails |
| 426 | `unsupported_protocol` | `protocol version is not supported` | protocol version is not 1 |
| 503 | `server_busy` | `server is busy` | bootstrap capacity is full; include `Retry-After: 1` |

AR125. Bootstrap SHALL NOT return WebSocket close codes.

AR126. On the first page, one read transaction SHALL capture the epoch and `COALESCE(ownerHead, 0)` as `barrier`.

AR127. The bootstrap page sequence SHALL include owner items that existed before event recording and have no creation row.

AR128. The bootstrap page sequence SHALL include owner items whose creation row has `ownerSeq <= barrier`.

AR129. Pages SHALL use immutable `(createdAt, id)` order.

AR130. A page read SHALL request `limit + 1` rows and return at most `limit` rows.

AR131. A next bootstrap cursor SHALL carry the same epoch, owner, and barrier.

AR132. Bootstrap SHALL exclude items created after the barrier.

AR133. The final page SHALL return `{type: incremental, version: 1, epoch, ownerUserId, seq: barrier}`.

AR134. AR126-AR133 SHALL work with an empty event table, only pre-feature items, or a zero barrier.

AR135. Replay or push SHALL deliver a new item after the barrier from `seq > barrier`.

AR136. A supported restore SHALL rotate the epoch before a feed read or work-item create.

AR137. After restore, an old incremental or bootstrap cursor SHALL return HTTP `410 cursor_expired`.

AR138. After restore, the client SHALL start bootstrap in the new epoch.

### H. Push, replay, and handoff

AR139. After commit, the writer SHALL send only a nonblocking process message with owner and sequence.

AR140. The writer SHALL NOT write a socket or drain a feed in the transaction.

AR141. A missing or crashed pump SHALL NOT remove or invalidate the event row.

AR142. One serialized pump SHALL exist per active `(owner, class)`.

AR143. The pump SHALL own `lastDrainedSeq` and use indexed ascending reads.

AR144. Nudge order SHALL NOT define event order.

AR145. The pump MAY collapse several nudges into one drain.

AR146. An omitted cursor SHALL mean future events after the omitted-cursor cut.

AR147. An omitted cursor SHALL NOT request the current snapshot.

AR148. The pump SHALL perform omitted-cursor registration as this one serialized operation:

1. The handler authenticates the capability and reserves admission.
2. The pump reads the current epoch and owner head.
3. The pump installs the connection as pending at that head before it handles a later queued nudge.
4. The handler returns `101`.
5. The server sends `subscription_ready` with that incremental cursor.

AR149. The database head read in AR148 SHALL be the cut.

AR150. AR148 SHALL exclude a commit at or before the cut.

AR151. The next durable drain SHALL find a commit after the cut if its nudge does not run after registration.

AR152. A client that needs current state SHALL bootstrap before subscription.

AR153. With a supplied cursor, the pump SHALL install the connection as pending before replay.

AR154. Replay SHALL read rows after the cursor in fixed pages.

AR155. Replay SHALL drain through the pump's current head before `subscription_ready`.

AR156. The server SHALL send `subscription_ready` with the last emitted cursor.

AR157. The pump SHALL attach the connection to live delivery at the same head.

AR158. If the head advances during replay, the pump SHALL drain that interval before live attachment.

AR159. An event during handshake SHALL appear in replay or the immediate live drain.

AR160. An ambiguous network break MAY repeat an event. It SHALL NOT lose the event.

AR161. The client SHALL persist a cursor only after it applies the event.

AR162. The client SHALL deduplicate by `(epoch, seq)`.

AR163. Each active pump SHALL compare its last drained sequence with durable head once per 30-second heartbeat.

AR164. A mismatch SHALL drain durable rows.

### I. Crash recovery, slow consumers, fairness, and limits

AR165. The pump SHALL enqueue frames to independent per-connection queues in O(1) work.

AR166. The pump SHALL NOT write synchronously to a socket.

AR167. Each queue SHALL hold at most 256 events or 1 MiB, whichever limit arrives first.

AR168. Queue overflow SHALL close only that socket with `4008/slow_consumer`.

AR169. Queue overflow SHALL NOT delete or mark a durable row as delivered.

AR170. A healthy sibling SHALL continue without waiting for the slow socket.

AR171. A supervisor SHALL restart a crashed pump.

AR172. A pump crash SHALL close its sockets with `1011/stream_restart`.

AR173. A restarted pump SHALL rebuild its state from the durable head and event rows.

AR174. A gateway crash SHALL produce EOF for connected clients.

AR175. Atomic rows SHALL survive the gateway crash and support reconnect replay.

AR176. Reconnect replay or the heartbeat check SHALL recover a crash after commit and before nudge.

AR177. One global replay scheduler SHALL allow at most four executing replay connections.

AR178. The scheduler SHALL allow at most 100 waiting replay connections.

AR179. An excess open SHALL fail before Upgrade with HTTP `503 server_busy` and `Retry-After: 1`.

AR180. An excess open SHALL NOT advance a cursor.

AR181. One scheduler turn SHALL read 51 indexed rows and emit at most 50 rows for one connection.

AR182. Scheduler turns SHALL run round-robin across capability and owner.

AR183. A replay connection SHALL yield after each page.

AR184. The scheduler SHALL service live drains before the next replay round.

AR185. Connection admission SHALL return `connection_limit` when AR76 or AR77 is full.

AR186. Connection admission SHALL NOT evict another consumer.

AR187. The socket SHALL keep the current 30-second ping and 90-second pong timeout.

### J. Fixed release load

AR188. The release load SHALL use a dedicated Linux host with four pinned vCPUs, 8 GiB RAM, local NVMe, and no competing workload.

AR189. The load SHALL use the production BEAM release and production SQLite settings.

AR190. SQLite SHALL use WAL, foreign keys, and normal synchronous mode for this load.

AR191. The dataset SHALL contain 1,000,000 foreign-owner work items and 100,000 retained target-owner event rows.

AR192. Each encoded event frame SHALL remain below 1 KiB.

AR193. The load SHALL use 20 target owners and 100 caught-up connections, with five connections per owner.

AR194. The load SHALL create 20 items per second, evenly across the owners, for 10 minutes.

AR195. At minute two, eight consumers SHALL each replay 10,000 events.

AR196. Four replay consumers SHALL execute and four SHALL wait under the scheduler.

AR197. The proxy-to-client path SHALL add no injected network latency.

AR198. The load SHALL produce no missing event and no foreign event.

AR199. Each owner SHALL remain ordered.

AR200. Caught-up consumers SHALL meet commit-to-first-socket-write p95 at or below 250 ms.

AR201. Caught-up consumers SHALL meet commit-to-first-socket-write p99 at or below one second.

AR202. Create-transaction p99 SHALL increase by at most 10 ms against the same dataset and build with the feature disabled.

AR203. Pumps, socket queues, and replay scheduling SHALL use at most 160 MiB of BEAM process memory in total.

AR204. A connection SHALL NOT exceed 256 queued events or 1 MiB.

AR205. Each recovering consumer SHALL converge.

AR206. A failure of AR188-AR205 SHALL block release and return the design to product review.

AR207. A failed load SHALL NOT revise its own thresholds.

### K. Audit, operations, schema, and deletion

AR208. Tightbeam SHALL durably audit capability mint, revoke, expiry, and denied authentication.

AR209. Tightbeam SHALL durably audit each non-empty delivery batch.

AR210. Operational logs SHALL record public capability id, owner, class, cursor, and replay count.

AR211. Operational logs SHALL record queue overflow, latency, close reason, and last sent cursor.

AR212. Logs and metrics SHALL omit raw bearers and item content.

AR213. Operations SHALL expose active connections, waiting connections, connects, reconnects, sent events, and replayed events.

AR214. Operations SHALL expose authentication failures, subscription failures, cursor expiry, queue depth, and slow-consumer closes.

AR215. Operations SHALL expose replay turns, nudge-to-write latency, and heartbeat head mismatches.

AR216. V1 SHALL NOT purge event rows or delete work items.

AR217. The creation-row foreign key SHALL use restrictive deletion.

AR218. A future deletion design SHALL define a tombstone class, cursor advancement, retention gaps, and downstream-copy duties before it relaxes AR217.

AR219. Capability deletion or revocation SHALL close sockets.

AR220. Capability deletion or revocation SHALL NOT erase an external copy that the consumer already received.

AR221. A future companion SHALL own deletion from its store and sinks.

### L. Migration and mixed-version behavior

AR222. The rollout SHALL use this sequence:

1. Add the capability, feed state, owner head, and creation tables with an additive schema migration.
2. Keep capability mint and external endpoints disabled.
3. Initialize a fresh epoch and one schema and feed feature version.
4. Do not synthesize historical creation events. Use bootstrap for existing owner state.
5. Enable and validate atomic writes, indexes, crash recovery, and the fixed load while external access remains disabled.
6. Enable owner capability management.
7. Enable the external WebSocket behind the same deployment feature gate.
8. Observe audit, latency, queue, replay, and isolation thresholds before broad availability.

AR223. Current chat and work-state clients and frames SHALL remain unchanged.

AR224. External protocol V1 SHALL reject another protocol version.

AR225. An old gateway SHALL NOT expose the external lifecycle.

AR226. After capability issuance, a boot and deployment gate SHALL reject a writer that omits atomic event rows.

AR227. Emergency rollback SHALL disable the external subscription and capability mint.

AR228. Re-enable after emergency rollback SHALL rotate the epoch and require client bootstrap.

AR229. Protocol fixtures SHALL encode the exact V1 wire shapes before external access is enabled.

### M. Clause-preservation map

This map binds each reviewed authority section to this specification.

| Reviewed authority section | Preserved clauses |
|---|---|
| Decision and approval conditions | G1-G5, I1-I10, AR1-AR6, AR206 |
| Facts proven from current source | F1-F16, T10 |
| Terms | T1-T9 |
| Assumptions | A1-A7 |
| Invariants | I1-I10 |
| Non-goals | N1-N8 |
| Open questions | Open Questions |
| Product specification home | This canonical file and Authority block |
| Alternatives and tradeoffs | AR1-AR6, N5-N7 |
| Closed subscription and transport | AR7-AR32 |
| Secure transport boundary | AR33-AR43 |
| Capability issuance, scope, and tokens | AR44-AR82 |
| Durable storage, identity, and schema | AR83-AR94 |
| Cursor vocabulary and errors | AR95-AR109 |
| Bootstrap and zero-event handoff | AR110-AR138 |
| Prompt push, omitted cursor, replay, and handoff | AR139-AR164 |
| Crash recovery, slow consumers, fairness, and limits | AR165-AR187 |
| Fixed reference load and release thresholds | AR188-AR207 |
| Audit, compatibility, operations, and deletion | AR208-AR221 |
| Migration and mixed-version behavior | AR222-AR229 |
| Deterministic acceptance tests | AC1-AC20 |
| Review finding B1 | AR33-AR82; AC4-AC6 |
| Review finding B2 | AR7-AR32, AR95-AR164; AC3, AC7-AC13, AC17 |
| Review finding I3 | AR165-AR207; AC12-AC15, AC19 |
| Review finding I4 | All eight canonical sections; AR222-AR229; AC20 |
| Review finding N5 | F2 and immutable source provenance in Authority |
| Formal recommendation | G1-G5, AR1-AR6 |

## Acceptance

AC1. Given a create that fails before commit, when the transaction ends, then no item, event, or push exists. Given one committed create, then one item, one atomic event row, and one prompt push exist. Given a keyed replay, then no new sequence or push exists.

AC2. Given creates for Alice, Bob, and Alice, when Alice consumes her feed, then she receives owner sequences 1 and 2 only. Frames, errors, timing buckets, logs, and metrics reveal no evidence of Bob.

AC3. Given each invalid Upgrade header case, when the client connects, then the server returns the AR22 status and envelope. The cases include an unknown class, wildcard, repeated header, empty header, chat class, owner header, predicate header, extra application header, and bad protocol. The server does not return `101` or register a pump.

AC4. Given a later device, when it sends `pair`, then `pair_pending` cannot control capabilities. When an admin approves it for Alice and it pairs again, then the returned `tbt_` bearer can mint for Alice. Re-pair makes the previous bearer fail. An owner field fails. Org, session, `cap_`, and revoked device bearers fail. An admin device can list or revoke a foreign capability, but it cannot mint for another owner.

AC5. Given a device that minted a capability, when an admin revokes the device, then its control calls return `401`. Its `cap_` remains usable until separate revocation. The capability contains 256 CSPRNG bits. Storage contains only its digest. Digest comparison is constant time. Lists, audits, proxy logs, and application logs omit the bearer. Capability revocation closes the socket with `4003`.

AC6. Given a remote plain `ws://` client or an external non-loopback bind without secure termination, when the lifecycle starts, then it fails. Given valid `wss://` through the configured proxy, when certificate and hostname validation pass, then the connection works.

AC7. Given initial and continuation bootstrap requests, when the client pages, then each body and response matches AR110-AR124. Limits, field closure, cursor exclusivity, `(createdAt, id)` order, owner isolation, and a sequence-zero final cursor pass.

AC8. Given a paused bootstrap after barrier capture, when a new item commits and bootstrap finishes, then replay or push delivers the new item. The handoff does not skip the item.

AC9. Given malformed, extra-field, wrong-version, wrong-owner, negative, above-head, expired-epoch, and below-retention cursors, when bootstrap or Upgrade validates them, then it returns exact HTTP `400 cursor_invalid` or `410 cursor_expired`. Upgrade does not return `101`. The result does not disclose a foreign owner.

AC10. Given an omitted cursor and a pump paused on each side of the head-read cut, when the connection completes, then a pre-cut event is excluded and a post-cut event is pushed. A bootstrap-first flow returns current state and the later event.

AC11. Given a pending registration and paused replay, when an event commits and replay resumes, then the event appears before `subscription_ready` or in the immediate live drain. It does not appear zero times. Reversed and collapsed nudges still produce ascending durable order.

AC12. Given a dropped nudge, when one heartbeat passes, then the head mismatch drains the row. Given a crash after commit and before nudge, when the client reconnects, then replay recovers the row.

AC13. Given a pump crash during replay, when supervision restarts it, then affected sockets close with `1011/stream_restart`, healthy owners continue, and reconnect converges. Given a gateway crash before or after socket write, then clients receive EOF and recover at least once with the same dedupe identity.

AC14. Given one blocked socket, when its queue reaches 256 events or 1 MiB, then only that socket closes with `4008/slow_consumer`. A healthy sibling stays within the latency thresholds. The closed consumer converges after reconnect.

AC15. Given five replay consumers and live traffic, when scheduling begins, then four replay and one waits. Page turns are round-robin. Live drains run before the next replay round. Given 100 full wait slots, the next Upgrade returns `503 server_busy`, `Retry-After: 1`, and no cursor advance.

AC16. Given full per-capability or per-owner connection limits, when another client connects, then it receives pre-Upgrade HTTP `429 connection_limit`. No unrelated connection closes. Given capability revocation, active sockets close with `4003/revoked` and reconnect fails.

AC17. Given a stale backup, when the supported restore runs, then it rotates the epoch before feed access. Old incremental and bootstrap cursors expire. Zero-event bootstrap succeeds. A new-epoch reconnect resumes.

AC18. Given each emitted event, when its frame is validated, then it matches AR90 exactly. It contains no title, prompt, owner id, assignment, or arbitrary substrate row.

AC19. Given the exact AR188-AR197 load, when the 10-minute run completes, then AR198-AR205 pass. A failure blocks release.

AC20. Given a mixed deployment, when old clients connect, then their behavior stays unchanged. An unsupported external version fails closed. After issuance, rollback to an old writer fails at the compatibility gate. Emergency disable and re-enable rotates the epoch and requires bootstrap.

## Open Questions

OQ1-OQ4 do not block V1. OQ5-OQ10 block independent approval and implementation.

OQ1. **NON-BLOCKING.** A later product decision can add SSE as a second transport.

OQ2. **NON-BLOCKING.** A later product decision can add delegated admin issuance.

OQ3. **NON-BLOCKING.** A later product decision can add native TLS.

OQ4. **NON-BLOCKING.** A later product decision can add a deletion or tombstone class.

Each non-blocking later decision requires a new versioned contract and threat review.

OQ5. **BLOCKING.** AR49 requires `expiresAt`, but AR72 defines a default expiry. Product must either make `expiresAt` optional or remove the default.

OQ6. **BLOCKING.** The reviewed authority does not define what happens when a capability expires during an active connection. Product must define whether the server closes that connection, including the trigger and close code.

OQ7. **BLOCKING.** The reviewed control wire does not define the list `type` value, the `state` vocabulary, revocation field names, or closed control-route error envelopes. Product must define those values or remove them from the external contract.

OQ8. **BLOCKING.** AR109 and AC2 require bounded, non-disclosing timing without a measurable bound. Product must define a repeatable timing test or remove timing from the security contract.

OQ9. **BLOCKING.** AR124 defines `503 server_busy` for full bootstrap capacity without defining that capacity. Product must define the concurrency and wait limits or remove this error case.

OQ10. **BLOCKING.** AR95-AR99 require canonical cursor encoding without defining the byte encoding, prefixes, or compatibility rule. Product must define that format or declare server-generated cursors opaque and require backward-compatible decoding.
