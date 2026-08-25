# ClipMesh MVP technical specification v1

Status: draft for independent adversarial review. These bytes authorize no
implementation, deployment, enrollment, live service mutation, private
inventory mutation, or use of a private topology.

Authority and evidence:

- The canonical seed is ClipMesh `docs/initial-spirit.md` at commit
  `89c6579dc1ddc180ce22e954ecc39cc410eee887`, artifact `art_3d431942`,
  SHA-256
  `60e59c7b7e200a6ce70114ebad34e420cf291e4d6c4e3493f1d3b297f3e85b9a`.
- The approved product authority is `clipmesh-spirit-v1.md` at tightbeam-specs
  commit `472cfd261728bc88e9e655a9a9bf73ed94e9064e`, artifact
  `art_be61a318`, SHA-256
  `e1839054f8059bf591388123714c6801a974a3a3936ef912adcacd9832934adf`.
- Product-owner digest `att_a558caac-d662-412e-85f7-750379a3bc88` found the
  Spirit coherent and ready for the normal spec-review-build-review cycle.
- Product-owner approval `att_d7e08368-3c00-47cf-949e-0aedb40c384c`
  approved that Spirit without authorizing deployment or enrollment.
- Work item `wi_0507efeb-914b-4289-9930-30cd36eb7e88` owns this product
  thread. Assignment `asg_3dfed51c-3ba4-44ef-8772-2dbebf15af88` owns this
  specification until independent review returns `reviewed-clean`.

When this specification conflicts with the approved Spirit, the Spirit
controls. A material correction amends this file before a builder acts on it.

## Goal

Define one buildable first release of ClipMesh for a small personal fleet on a
private overlay network. The release consists of a Rust hub, Rust Wayland Linux
and macOS desktop agents, a foreground SwiftUI iOS and iPadOS client, and
generic deployment assets.

Define the shared protocol and security boundary before product code splits.
The specification makes authentication, authorization, wire compatibility,
ordering, replay handling, resume, loop suppression, retention, purge,
platform behavior, diagnostics, and repository neutrality decidable from test
evidence.

The MVP uses a trusted hub that reads plaintext. TLS, unique device
credentials, explicit administrator authority, private binding, short
retention, and content-free diagnostics bound that trust decision.

This design adds one shared protocol and authority boundary because deleting
either would delete the cross-device outcome, while accepting divergent client
behavior would make replay, purge, and credential isolation undecidable.

## Non-Goals

- The MVP does not provide end-to-end or zero-knowledge payload encryption.
- The MVP does not provide mutual TLS.
- The MVP does not copy images, files, HTML, RTF, or another MIME type.
- The MVP does not discover or operate a service on the public Internet.
- The MVP does not provide accounts, billing, social sharing, or multi-tenant
  hosting.
- The MVP does not provide an iOS or iPadOS Share extension.
- The MVP does not claim passive background clipboard monitoring on iOS or
  iPadOS.
- The MVP does not elect a hub, fail over between hubs, or deliver directly
  between devices.
- The MVP does not provide a desktop clipboard-manager interface.
- The MVP does not require pairwise approval between devices.
- The MVP does not invent cryptographic primitives.
- The MVP does not promise erasure from an offline client, an operating-system
  pasteboard, storage snapshots, or storage hardware.
- This specification does not choose a private hub, address, hostname,
  username, filesystem layout, credential, inventory, or deployment boundary.
- This specification does not implement, deploy, enroll, issue a usable
  credential, or mutate a live or private system.

## Terms

- **Administrator:** A principal authenticated with an administrator bearer
  credential. The administrator controls device creation, enrollment-artifact
  issuance, credential rotation, revocation, hub pause state, and global
  history purge. Administrator authority does not grant data-plane access.
- **Device:** One enrolled Linux, macOS, iOS, or iPadOS client identified by an
  opaque UUIDv4 `device_id` and one current device bearer credential.
- **Device credential:** A 256-bit random bearer secret bound to one device.
  It authorizes a data-plane session for that device and no administrator
  operation.
- **Administrator credential:** A 256-bit random bearer secret supplied to the
  hub through an external secret file. It authorizes administrator endpoints
  and no data-plane session.
- **Enrollment artifact:** A 256-bit random bearer secret that can activate one
  pending mobile device once before its fixed expiry.
- **Data plane:** The authenticated WebSocket session that carries resume,
  publish, delivery, acknowledgement, and control messages.
- **Control plane:** The authenticated HTTPS administrator and enrollment
  endpoints. Health and readiness endpoints form a separate unauthenticated,
  content-free surface on the same confined TLS listener.
- **Clipboard event:** The immutable client-authored metadata and UTF-8 text
  for one publish attempt. The hub binds the asserted source to the
  authenticated device.
- **Message ID:** A client-generated UUIDv4 that identifies one clipboard
  event across retries.
- **Source sequence:** A positive unsigned 64-bit integer allocated
  monotonically by one device. Gaps are valid. Reuse is invalid unless the
  request is an exact retry of an event that remains in history.
- **Cursor:** A positive unsigned 64-bit integer allocated monotonically by
  the hub when it accepts an event. Cursor order is the delivery and history
  order.
- **History epoch:** A hub-generated UUIDv4 that names one continuity interval
  of retained history. Global purge and memory-history restart replace it.
- **Resume boundary:** Cursor `B`, captured while the hub atomically registers
  a resuming session. Events at cursors less than or equal to `B` are resume
  material. Events accepted after `B` are live material.
- **Resume gap:** Evidence that at least one accepted cursor after the client's
  cursor is no longer available because of expiry or count trimming.
- **Live event:** An event accepted after a session's resume boundary. Desktop
  agents can write only live remote events to the operating-system clipboard.
- **Resume event:** A retained event at or before a session's resume boundary.
  A desktop agent records its cursor but does not write it to the
  operating-system clipboard.
- **Exact retry:** A repeated `publish` whose authenticated source,
  `message_id`, `source_seq`, timestamps, content type, payload length, content
  hash, and payload bytes equal a retained accepted event.
- **Replay ledger:** Content-free durable metadata containing each device's
  highest accepted source sequence and message-ID tombstones. Expiry and purge
  remove payload-bearing history but preserve replay resistance.
- **Local pause:** A desktop-agent state that stops clipboard observation,
  publishing, delivery application, and its data-plane connection.
- **Administrative pause:** A durable hub state for one device or the data
  plane as a whole. It refuses affected data-plane authentication and closes
  affected sessions.
- **Local-only next copy:** A one-shot desktop control that suppresses the next
  eligible local clipboard observation without sending its payload to the hub.
- **Recognized sensitive hint:** A platform clipboard signal that the platform
  adapter has mapped to the protocol-domain value `sensitive = true` from a
  captured real platform response. The adapter does not infer sensitivity from
  clipboard text.
- **Content-free diagnostic:** A log, metric, health response, error, or crash
  report that contains no payload bytes, preview, base64 payload, payload hash,
  credential, authorization header, device display name, or payload-derived
  string.
- **Generic fixture:** Test material that uses reserved example names,
  synthetic clipboard text, synthetic UUIDs, and structurally redacted
  credentials. It contains no value copied from a private deployment.
- **Normal delivery conditions:** Two authenticated desktop agents connected
  to one test hub; network round-trip time at most 100 ms; packet loss zero;
  payload at most 4 KiB; no configured pause; both desktops unlocked; hub and
  agents below 70 percent CPU utilization.

## Assumptions

1. The deployment provides a private overlay route between enrolled devices
   and one stable hub.
2. The deployment provides a valid TLS server certificate whose name matches
   the configured hub URL and whose issuer the clients trust.
3. The deployment supplies administrator and device secrets outside the public
   repository.
4. Linux MVP hosts run a Wayland session with working `wl-paste` and `wl-copy`
   commands.
5. macOS exposes pasteboard change counts, declared pasteboard types, and a
   session-lock signal through native APIs.
6. iOS and iPadOS permit foreground URLSession WebSocket use and explicit
   writes to `UIPasteboard.general`.
7. A device clock can remain within two minutes of the hub clock. A client
   outside that bound receives an explicit timestamp rejection instead of a
   weakened replay rule.
8. The deployment owner accepts hub-readable plaintext under the safeguards in
   this specification.
9. The repository can run Rust tests, Swift tests, a real SQLite process, and
   platform-specific adapter tests on their respective operating systems.
10. The MIT license text can land at the public repository root before release.

## Invariants

These invariants control the architecture and acceptance matrix. A later
implementation choice cannot weaken them without a reviewed amendment to this
file.

### I1 — One explicit protocol version

Rust owns the canonical version-1 domain and wire schemas. Swift maps those
schemas without a second interpretation. Each application message carries
`protocol_version = 1`. A receiver rejects another version before it processes
message-specific fields.

### I2 — Authentication determines device identity

The hub derives the session device from the presented credential. A published
`source_device_id` must equal that authenticated device. The hub rejects a
mismatch and writes no event, cursor, sequence, or history row.

### I3 — Device and administrator authority are disjoint

A device credential can open only the data-plane endpoint. An administrator
credential can call only administrator endpoints. An enrollment artifact can
call only the enrollment exchange endpoint. The hub returns the same
`unauthorized` shape for an invalid credential and a credential of the wrong
class.

### I4 — The transport and listener fail closed

The hub serves TLS 1.3 on explicit non-global unicast addresses. It has no
listener default. It rejects wildcard, globally routable, multicast,
link-local, and broadcast bind addresses. It starts serving only after it has
bound each configured socket and validated its complete configuration.

Each client accepts `https` and `wss` transport only. Each client verifies the
server certificate chain, validity interval, and configured DNS name. The MVP
has no certificate-verification bypass.

### I5 — Accepted events have one total order

The hub allocates one cursor in the same transaction that accepts an event.
Cursor values increase without reuse. History queries, resume delivery, and
live delivery use ascending cursor order.

### I6 — Publish retry is idempotent; replay changes no state

An exact retry of a retained event that reaches replay validation returns its
original cursor with `duplicate = true`. It creates no history row and no
second live delivery. Transport, session, connection, and rate admission can
reject a publish before replay validation. A reused message ID with different
event fields, a tombstoned message ID, or a source sequence at or below the
device's accepted high-water mark is a replay rejection. A rejection advances
no cursor or source-sequence high-water mark.

### I7 — Resume and live transition form one boundary

The hub registers the subscriber and captures resume cursor `B` in one
serialized action. It buffers events accepted after `B` until it has sent
`resume_complete(B)`. It then sends buffered events in cursor order as live
events. The check and transition are indivisible with respect to publish
acceptance.

### I8 — Reconnect, unlock, and unpause do not apply backlog

A desktop writes an event to the operating-system clipboard only when the
event is tagged `live`, the event source is another device, and the desktop is
unlocked and locally active at the write boundary. Resume events update cursor
and dedupe state without changing the operating-system clipboard.

### I9 — Clipboard loops terminate without a timer

An agent suppresses its own message IDs, previously processed message IDs, and
the first local observation that matches bytes the agent just wrote remotely.
It clears the write marker on the first later clipboard observation, whether
that observation matches or differs. It also suppresses consecutive local
observations with one content hash within one agent process generation. No
elapsed-time threshold decides loop identity.

### I10 — Lock, pause, and sensitive state fail closed

A desktop whose lock state is unknown acts as locked. Lock and local-pause
transitions cancel queued, uncommitted local observations. A recognized
sensitive hint prevents outbox creation. The state check and outbox commit or
clipboard-write invocation share one serialized agent-state boundary.

### I11 — Retention limits compose

An event must satisfy the configured payload-size limit before acceptance.
After acceptance, the hub removes expired events and trims the lowest cursors
until the configured count holds. The default limits are 262,144 payload
bytes, 20 retained entries, and 14,400 seconds from client creation time. The
first reached limit removes or rejects the event.

### I12 — Purge removes payload state but not replay protection

Global purge deletes retained payloads, content hashes, source labels cached
with events, local client history, and pending desktop outbox payloads. It
replaces the history epoch. It preserves device records, credential digests,
cursor high-water state, source-sequence high-water state, and content-free
message-ID tombstones.

### I13 — History mode changes payload durability only

SQLite history mode persists accepted events across an ordinary hub restart.
Memory history mode stores payload-bearing events only in process memory. Both
modes persist device administration and content-free replay metadata. A
memory-history restart replaces the history epoch before it accepts a session.

### I14 — Diagnostics cannot represent clipboard content or secrets

Protocol types wrap payloads and credentials in types whose `Debug` and
`Display` render fixed redaction markers. Only the wire encoder and clipboard
adapter can expose payload bytes. Logging, metrics, health, errors, and panic
paths accept metadata types that contain no payload, payload hash, credential,
authorization header, or display name.

### I15 — Mobile clipboard writes require a foreground user action

The mobile client writes one selected event to `UIPasteboard.general` only
after an explicit selection action while the app is active. Resume, live
delivery, refresh, activation, and background transitions perform no pasteboard
write.

### I16 — The public repository is topology-neutral

Source, defaults, examples, fixtures, tests, documentation, and deployment
templates contain no value copied from a private deployment. Runtime topology
enters through external configuration or inventory. Repository checks combine
generic secret and topology-pattern scanning with an optional external exact
denylist whose contents remain outside the repository.

### I17 — One mutation seam owns each state

The hub event transaction alone mutates cursor, history, and replay state. The
administrator service alone mutates device, credential, pause, enrollment, and
purge state. The agent state machine alone commits outbox and clipboard-write
decisions. The mobile view model alone mutates visible history and pasteboard
requests.

Event and administrator mutations share one serialized storage writer. A
publish transaction rechecks device state, credential generation, pause state,
session epoch, and replay state before it writes. Therefore a publish orders
entirely before or entirely after a concurrent rotation, revocation, pause, or
purge.

### I18 — A failure is explicit and content-free

Startup, authentication, authorization, validation, rate, resume, storage, and
platform failures produce one stable reason code. The failure changes no state
unless its response explicitly reports a committed idempotent result or a
committed purge. No error body includes request bodies, payload metadata that
can fingerprint content, or credential material.

## Architecture

### 1. Component and repository boundary

The public product repository contains these ownership seams:

| Surface | Owner | Required contents |
| --- | --- | --- |
| `clipmesh-protocol` Rust crate | Shared protocol | Domain types, wire schemas, validation, redacted wrappers, JSON fixtures, protocol conformance tests |
| `clipmesh-hub` Rust binary | Hub | TLS listener, device data plane, administrator control plane, persistence, retention, health, limits |
| `clipmesh-agent` Rust binary | Desktop | Shared protocol client, outbox, reconnect, state machine, platform adapter interface, local control |
| Linux adapter | Desktop | Wayland `wl-paste --watch`, `wl-copy`, lock-state integration, sensitive-hint mapping |
| macOS adapter | Desktop | Native pasteboard reads and writes, change-count loop marker, lock-state integration, Keychain credential storage |
| `ClipMesh` SwiftUI target | Mobile | Version-1 Swift mapping, foreground session, history view, explicit pasteboard copy, Keychain storage |
| Deployment assets | Packaging | Generic systemd user unit, launchd agent template, Ansible role variables, configuration reference |
| Repository checks | CI | Protocol cross-language checks, secret scan, topology-neutral scan, content-canary scan, license check |

The repository root carries the MIT license. Deployment assets contain
placeholders or reserved example domains. They contain no private inventory.

This specification establishes the `ClipMesh protocol v1` pattern. It applies
only to ClipMesh hub, desktop, and mobile communication. It does not establish
a general protocol pattern for another project.

### 2. Transport and encoding

1. The hub exposes one or more configured TLS listeners.
2. The listener supports TLS 1.3 through rustls. It does not enable plaintext
   HTTP, opportunistic TLS, or a redirect from plaintext HTTP.
3. The data-plane path is `/v1/stream` and requires a WebSocket upgrade with
   subprotocol `clipmesh.v1`.
4. The client supplies `Authorization: Bearer <DEVICE_CREDENTIAL>` in the TLS
   protected upgrade request. A credential never appears in a URL, query,
   WebSocket subprotocol value, log, or error.
5. Application messages are UTF-8 JSON WebSocket text messages. Binary frames
   are invalid. A JSON document is one object with no duplicate keys and no
   byte-order mark.
6. A version-1 inbound schema is closed. An unknown field, missing field,
   duplicate key, wrong JSON type, or unknown message type produces
   `protocol_schema_invalid`. This rule makes an additive wire change a new
   reviewed protocol version.
7. The maximum decoded WebSocket text-message size is
   `4 * ceil(max_payload_bytes / 3) + 4096` bytes. The hub rejects a larger
   inbound message before JSON parsing. A client rejects a larger inbound
   message before JSON parsing. The 4,096-byte envelope allowance covers each
   version-1 metadata and JSON field at its maximum encoded size. Before it
   validates `server_hello`, a client uses the version-1 hard cap 1,402,200
   bytes. It then adopts the lower configured limit from a valid hello.
8. WebSocket compression is disabled in version 1. This removes
   secret-and-payload compression side channels and makes frame limits exact.
9. The hub sends a WebSocket ping after 30 seconds without outbound traffic.
   It closes the session with `heartbeat_timeout` when no matching pong arrives
   within 10 seconds.
10. The hub uses HTTP JSON for control-plane requests. A request and response
    carry `Content-Type: application/clipmesh+json;version=1`. The maximum
    decoded request body is 65,536 bytes.

### 2.1. Version compatibility and migration

A version-1 client offers only WebSocket subprotocol `clipmesh.v1`. A
version-1 hub selects that exact subprotocol or refuses the upgrade with
`protocol_version_unsupported`. Neither side falls back to an unversioned
protocol after a refusal.

Version 1 permits implementation fixes that leave each scalar, field, enum,
validation rule, state transition, and observable response unchanged. Adding,
removing, renaming, or reinterpreting one field or enum value creates a later
protocol version. A later hub can serve two reviewed subprotocols during a
migration window, but one session uses one version from hello through close.
The hub maps each supported wire version into one internal event model before
it writes history. A future version specification must define cross-version
history projection and downgrade behavior. Version 1 does not guess either.

### 3. Canonical scalar forms

| Scalar | Version-1 form | Validation |
| --- | --- | --- |
| `protocol_version` | JSON integer | Exact value `1` |
| UUID field | JSON string | Lowercase canonical UUIDv4 with hyphens |
| `source_seq`, `cursor` | JSON string | Decimal `1` through `18446744073709551615`, no sign, no leading zero |
| Timestamp | JSON integer | Signed 64-bit Unix epoch milliseconds in UTC |
| `content_type` | JSON string | Exact value `text/plain` |
| `payload_b64` | JSON string | RFC 4648 base64url without padding |
| `content_sha256` | JSON string | 64 lowercase hexadecimal characters over decoded payload bytes |
| Device display name | JSON string | 1 through 64 Unicode scalar values; excludes U+0000..U+001F, U+007F, U+202A..U+202E, and U+2066..U+2069 |
| Platform | JSON string | One of `linux_wayland`, `macos`, `ios`, `ipados` |
| Reason code | JSON string | One stable lowercase snake-case value from this specification |

The protocol preserves payload bytes exactly. It performs no Unicode
normalization and no newline conversion. Decoded payload bytes must form
non-empty UTF-8 text. `payload_bytes` is the decoded byte count.

Credential wire forms are:

- device: `cm_dev_v1_` followed by the 43-character unpadded base64url encoding
  of 32 random bytes;
- administrator: `cm_admin_v1_` followed by the same encoding;
- enrollment: `cm_enroll_v1_` followed by the same encoding.

The generator reads an operating-system cryptographic random source. The hub
stores SHA-256 credential digests and credential class, not plaintext
credentials. It returns a newly issued plaintext credential in one response.
It cannot retrieve that value later.

### 4. Clipboard event schema

`ClipboardEventV1` has exactly these fields:

| Field | Type | Rule |
| --- | --- | --- |
| `message_id` | UUID string | Client-generated UUIDv4 |
| `source_device_id` | UUID string | Must equal the authenticated device |
| `source_seq` | decimal string | Must exceed the device high-water mark unless this is an exact retained retry |
| `created_at_ms` | integer | At most 120,000 ms ahead of hub time |
| `expires_at_ms` | integer | Greater than hub validation time and no later than `min(created_at_ms + retention_seconds * 1000, hub_validation_time_ms + retention_seconds * 1000)` |
| `content_type` | string | Exact value `text/plain` |
| `payload_bytes` | integer | Exact decoded length in `1..max_payload_bytes` |
| `content_sha256` | string | SHA-256 of decoded payload bytes |
| `payload_b64` | string | Unpadded base64url of valid UTF-8 payload bytes |

The hub records `accepted_at_ms` and `cursor` as server metadata. Those fields
are absent from client-authored `ClipboardEventV1`.

This is the canonical version-1 publish example. Its fixture clock is
`1700000000000` ms. The UUIDs and text are synthetic:

```json
{
  "protocol_version": 1,
  "type": "publish",
  "event": {
    "message_id": "00000000-0000-4000-8000-000000000001",
    "source_device_id": "00000000-0000-4000-8000-000000000002",
    "source_seq": "1",
    "created_at_ms": 1700000000000,
    "expires_at_ms": 1700014400000,
    "content_type": "text/plain",
    "payload_bytes": 12,
    "content_sha256": "5cb72f90e968922d30557d0af8f719d21f61792becaa87eb32477767d739dc0b",
    "payload_b64": "Zml4dHVyZSB0ZXh0"
  }
}
```

### 5. Data-plane message schemas

Each message has exact fields. The common fields `protocol_version` and `type`
appear in each object.

#### Client to hub

| Type | Additional fields | State where valid |
| --- | --- | --- |
| `resume` | `known_history_epoch` UUID or null; `after_cursor` decimal string or null | `await_resume` only |
| `publish` | `event: ClipboardEventV1` | `live` only |
| `ack` | `history_epoch` UUID; `cursor` decimal string | `replaying` or `live` |

#### Hub to client

| Type | Additional fields | Meaning |
| --- | --- | --- |
| `server_hello` | `session_id`, `device_id`, `device_display_name`, `server_time_ms`, `history_epoch`, `newest_cursor` or null, `limits` | Authentication succeeded; resume is required |
| `resume_started` | `history_epoch`, `status`, `requested_after_cursor` or null, `boundary_cursor` or null, `lost_through_cursor` or null | Names the resume snapshot and any gap |
| `event` | `history_epoch`, `cursor`, `delivery`, `accepted_at_ms`, `source_display_name`, `event` | Delivers one retained or live event |
| `resume_complete` | `history_epoch`, `boundary_cursor` or null | Ends replay; later event messages are live |
| `publish_accepted` | `message_id`, `cursor`, `expires_at_ms`, `duplicate` | The publish committed or was an exact retained retry |
| `publish_rejected` | `message_id` or null, `code`, `retryable` | The publish wrote no event state |
| `pause_notice` | `scope`, `reason_code` | Administrative pause committed; the hub closes afterward |
| `purge_notice` | `purge_id`, `history_epoch`, `purged_through_cursor` or null | Global purge committed; client clears ClipMesh history |
| `error` | `code`, `retryable` | Session-level content-free failure |

`limits` contains exactly `max_payload_bytes`, `retention_seconds`,
`history_max_entries`, `max_clock_skew_ms`, and
`max_websocket_message_bytes` as JSON integers.

`resume_started.status` is one of:

- `fresh`: the client supplied no cursor;
- `complete`: the requested cursor has no known missing successor;
- `gap`: `lost_through_cursor` exceeds the requested cursor;
- `epoch_changed`: the supplied history epoch differs from the current epoch.

`event.delivery` is `resume` for a cursor at or before the boundary and `live`
for a cursor accepted after the boundary. The hub delivers accepted events to
the source session too. The source client uses source identity to suppress a
clipboard write while preserving a contiguous cursor view.

The hub sends `publish_accepted` before it sends the matching `event` on the
publishing session. Event messages remain ordered by cursor on each session.

An `ack` states the highest cursor that the client processed for the named
epoch. Its cursor cannot exceed the highest cursor that the hub sent on that
session. Its epoch must equal the session epoch. Acknowledgements are
nondecreasing; repeating the current value is idempotent. A lower cursor,
future cursor, or wrong epoch produces `ack_invalid` and closes the session.
During replay, a client advances one pending acknowledgement cursor without
sending an acknowledgement for each event. After `resume_complete`, it sends
one acknowledgement for the highest replay cursor that it processed. During
live delivery, it replaces the pending cursor with each higher processed
cursor and sends at most one acknowledgement per 2,000 milliseconds. A client
can send the pending acknowledgement before a deliberate close when the
session message bucket has a token. This coalescing rule applies to desktop and
mobile clients.

The hub keeps valid acknowledgements in memory for health and slow-consumer
diagnosis. An acknowledgement does not delete history and does not create a
delivery guarantee.

A nonnull `after_cursor` with null `known_history_epoch` produces
`resume_cursor_without_epoch` and closes the session. When the known epoch
differs, the hub ignores `after_cursor` and returns the current retained window.

### 6. HTTP surfaces and authority

The listener exposes these paths:

| Method and path | Credential class | Effect |
| --- | --- | --- |
| `GET /healthz` | none | Process liveness only |
| `GET /readyz` | none | Content-free readiness and one reason code |
| `GET /v1/stream` upgrade | device | Open one data-plane session |
| `POST /v1/enroll` | enrollment | Consume one pending mobile artifact and return one device credential |
| `POST /v1/admin/devices` | administrator | Create one active managed device and return its first credential |
| `POST /v1/admin/enrollment-artifacts` | administrator | Create one pending mobile device and return one ten-minute artifact |
| `POST /v1/admin/devices/{device_id}/rotate` | administrator | Replace the device credential and close existing sessions |
| `POST /v1/admin/devices/{device_id}/revoke` | administrator | Mark the device revoked and close existing sessions |
| `POST /v1/admin/pause-state` | administrator | Set global or per-device administrative pause state |
| `POST /v1/admin/purge` | administrator | Purge retained hub history and notify online clients |

Each mutating HTTP request carries `protocol_version = 1`, a UUIDv4
`request_id`, and only operation fields. The hub stores a content-free receipt
by authenticated principal class and digest, method, path, request ID,
request-body SHA-256, and result code.

For a repeated request ID with the same method, path, and body:

- revoke, pause, and purge return the recorded nonsecret result;
- device creation, enrollment-artifact creation, credential rotation, and
  enrollment exchange return `secret_result_already_committed` plus the
  resource ID and no secret.

A repeated request ID with different input returns `request_id_conflict` and
writes nothing. Loss of a one-time secret response requires a new
administrator action. The hub never stores plaintext merely to make a retry
convenient.

`POST /v1/admin/devices` accepts `display_name` and platform
`linux_wayland` or `macos`. The hub generates the device ID and device
credential in one transaction. The response returns each once.

Control-plane JSON success schemas are closed and exact:

| Operation | Request fields after `protocol_version`, `request_id` | Status | Success type and fields after `protocol_version`, `request_id`, `type` |
| --- | --- | --- | --- |
| Create managed device | `display_name`, `platform` | 201 | `device_created`: `device_id`, `credential`, `credential_generation = 1`, `device_state = active`, `created_at_ms` |
| Issue mobile artifact | `display_name`, `platform` | 201 | `enrollment_artifact_created`: `device_id`, `enrollment_artifact`, `expires_at_ms`, `device_state = pending` |
| Exchange mobile artifact | none | 201 | `device_enrolled`: `device_id`, `credential`, `credential_generation = 1`, `device_state = active`, `enrolled_at_ms` |
| Rotate credential | none | 200 | `credential_rotated`: `device_id`, `credential`, `credential_generation`, `rotated_at_ms` |
| Revoke device | none | 200 | `device_revoked`: `device_id`, `device_state = revoked`, `revoked_at_ms` |
| Set pause state | `scope`, `device_id`, `paused` | 200 | `pause_state_set`: `scope`, `device_id`, `paused`, `changed_at_ms` |
| Purge history | none | 200 | `history_purged`: `purge_id`, `history_epoch`, `purged_through_cursor` or null, `purged_at_ms` |

`type` values and fixed state strings in this table are JSON strings. A
secret-returning success uses `Cache-Control: no-store` and `Pragma: no-cache`.
An error response has exactly `protocol_version` and `error`; `error` has
exactly `code` and `retryable`, plus `resource_id` only for
`secret_result_already_committed`.

`POST /v1/admin/enrollment-artifacts` accepts `display_name` and platform
`ios` or `ipados`. The hub creates a pending device and an enrollment artifact
whose expiry is `issued_at_ms + 600000`. One successful `/v1/enroll`
transaction consumes the artifact, activates the device, and returns its first
device credential. Concurrent exchanges have one winner. An expired artifact
returns `enrollment_artifact_invalid`. A consumed artifact returns
`secret_result_already_committed` only for the exact request that consumed it;
another request returns `enrollment_artifact_invalid`. Before an exchange,
before new artifact issuance, and once per 60 seconds, the hub marks expired
artifacts and deletes their still-pending device rows. It retains a
content-free consumed or expired artifact-digest tombstone for 86,400 seconds
after consumption or expiry, then deletes that tombstone. It preserves the
content-free request receipt. A credential absent from both the active-artifact
set and tombstones receives the ordinary `unauthorized` response.

Credential rotation generates a new credential digest, increments the device
credential generation, invalidates the prior digest, and commits those changes
in one transaction. The hub then closes sessions authenticated under the prior
generation with `credential_rotated`.

Revocation sets device state to `revoked` and invalidates its credential in one
transaction. The hub then closes that device's sessions with `device_revoked`.
No other device row or session changes.

Administrative pause accepts exactly one scope:

- `{"scope":"global","device_id":null,"paused":<boolean>}`;
- `{"scope":"device","device_id":<UUID>,"paused":<boolean>}`.

Setting pause is idempotent. When pause becomes true, the hub sends
`pause_notice` and closes affected data-plane sessions. Affected upgrade
requests receive `administratively_paused`. The administrator control plane
remains reachable. Removing pause permits a fresh data-plane session; resume
semantics prevent backlog clipboard writes.

### 7. Authentication and authorization failure order

The hub applies checks in this order:

1. TLS handshake and certificate selection;
2. method, path, content type, and request-size limit;
3. credential syntax and credential digest lookup;
4. credential class and principal state;
5. endpoint-specific authorization;
6. administrative pause and connection limits;
7. schema and operation validation;
8. transaction conflict and storage result.

Steps 3 through 5 return the same HTTP 401 body:

`{"protocol_version":1,"error":{"code":"unauthorized","retryable":false}}`

The response does not reveal whether a credential, device, or administrator
exists. Authenticated requests can receive a more specific content-free code.

At step 4, a consumed enrollment artifact has no enrollment authority. The hub
can continue only through closed request-envelope validation and an exact
receipt lookup under that artifact digest. The same request ID, method, path,
and body hash returns `secret_result_already_committed` with the committed
device ID and no credential. Another request returns
`enrollment_artifact_invalid` and writes nothing. This exception grants no
mutation and expires when the artifact-digest tombstone expires.

### 8. Configuration and startup

The hub reads one versioned TOML configuration and separate secret files. The
configuration has these fields:

| Field | Required | Default or valid range |
| --- | --- | --- |
| `config_version` | yes | Exact integer `1` |
| `listen_addresses` | yes | Non-empty array of explicit socket addresses |
| `tls_certificate_file` | yes | Existing regular file |
| `tls_private_key_file` | yes | Existing regular file owned by the service user; mode no broader than `0600` |
| `administrator_credential_file` | yes | Existing regular file owned by the service user; mode no broader than `0600` |
| `state_directory` | yes | Existing or creatable directory owned by the service user; mode no broader than `0700` |
| `history_mode` | no | `sqlite`; alternate `memory` |
| `retention_seconds` | no | `14400`; valid `60..604800` |
| `history_max_entries` | no | `20`; valid `1..1000` |
| `max_payload_bytes` | no | `262144`; valid `1..1048576` |
| `max_connections` | no | `64`; valid `1..1024` |
| `max_connections_per_device` | no | `2`; valid `1..8` and no greater than `max_connections` |
| `publish_tokens_per_minute` | no | `60`; valid `1..600` |
| `publish_burst` | no | `10`; valid `1..100` |
| `outbound_queue_messages` | no | `64`; valid `1..256` |
| `outbound_queue_bytes` | no | `2097152`; valid from computed `max_websocket_message_bytes` through `16777216` |

The parser rejects unknown fields, duplicate TOML keys, missing required
fields, values outside these ranges, a queue-byte limit below the computed
message limit, and trailing non-TOML bytes.

The administrator credential file contains one credential followed by zero or
one LF byte. The Linux device credential file uses the same rule for a device
credential. Leading whitespace, trailing whitespace other than that LF,
multiple lines, and a second token are invalid.

An allowed bind IP is one of:

- IPv4 loopback `127.0.0.0/8`;
- IPv4 private-use `10.0.0.0/8`, `172.16.0.0/12`, or `192.168.0.0/16`;
- IPv4 shared-address space `100.64.0.0/10`;
- IPv6 loopback `::1`;
- IPv6 unique-local `fc00::/7`.

The hub rejects an unspecified, global, multicast, broadcast, documentation,
or link-local address. It does not resolve a bind hostname. It binds each
configured socket before it starts an accept loop. Failure to validate or bind
one address closes sockets already opened and exits nonzero.

At startup the hub validates that:

- the TLS certificate parses and is valid at the current time;
- the private key parses and matches the certificate;
- the administrator credential has exact administrator syntax;
- secret and key files are regular, non-symlink files with restrictive
  ownership and mode;
- the state directory and existing database satisfy ownership and mode rules;
- the database schema is supported and migrations can commit;
- history and replay metadata are internally consistent;
- memory history mode rotates the history epoch after a prior process instance.

The hub begins serving only after these checks succeed. A failure emits one
content-free startup code and exits nonzero.

While running, the hub rechecks certificate validity once per 60 seconds. At
the first check at or after certificate expiry, it marks readiness false and
completes no new TLS handshake. A readiness request on a TLS connection
established before expiry returns `tls_certificate_not_current`. Existing TLS
sessions continue until their ordinary close boundary. Replacing the
configured certificate requires a process restart in version 1.

The desktop agent requires a versioned configuration with an `https` hub base
URL, opaque device ID, platform, credential storage reference, TLS trust
configuration, and local-state location. It rejects URL user information,
query parameters, fragments, `http`, `ws`, and an insecure credential file.
The agent remains inactive when it cannot prove the lock state or initialize
the clipboard adapter.

An enrolled desktop that cannot open, validate, and atomically update its
local state returns `local_state_unavailable` and remains inactive. It does not
reset its source-sequence allocator. Recovery restores the same local state or
enrolls a new device identity.

The mobile client stores the device credential in Keychain with
`kSecAttrAccessibleWhenUnlockedThisDeviceOnly`. It stores no credential in
preferences, logs, a URL, a pasteboard, app state restoration, or a crash
report. Enrollment succeeds in the UI only after Keychain storage succeeds.
If the one-time exchange succeeded but Keychain storage failed, the UI reports
`credential_storage_failed` and instructs the administrator to rotate or
re-enroll; it does not display the credential again.

### 9. Hub session state machine

| State | Entry | Accepted input | Exit |
| --- | --- | --- | --- |
| `tls_handshake` | TCP accepted | TLS records | Failure closes; success enters `authenticate` |
| `authenticate` | TLS complete | HTTP upgrade | Valid active device enters `await_resume`; failure returns HTTP and closes |
| `await_resume` | WebSocket accepted; `server_hello` sent | One `resume` within 5 seconds | Valid input enters `replaying`; other app input closes with `resume_required` |
| `replaying` | Boundary captured; subscriber registered | `ack`, pong | After resume messages and `resume_complete`, enter `live` |
| `live` | Resume complete | `publish`, `ack`, pong | Pause, revocation, rotation, slow consumer, heartbeat failure, client close, or protocol error enters `closing` |
| `closing` | Close reason selected | No application input | Send close frame when possible, unregister subscriber, release limits |

A client can send `resume` once per session. A client publishes only in
`live`. The client queues a local outbox item until `live` instead of sending
it during replay.

The hub enforces both an outbound message count and byte count per session.
Reaching either limit closes that session with `slow_consumer`. The hub does
not drop an event silently. The client reconnects and resumes from its last
processed cursor.

The listener permits at most 64 active non-WebSocket HTTP requests. Before
authentication, one source address receives a token bucket of 30 requests per
minute with a burst of 10. One authenticated administrator receives 60 control
requests per minute with a burst of 20. Health and readiness share a bucket of
120 requests per minute with a burst of 20 per source address. Exceeding a
bucket returns HTTP 429 with `request_rate_limited` and no state change.

One WebSocket session receives an application-message token bucket of 120
messages per minute with a burst of 20. `resume`, `ack`, and `publish` each
consume one token. WebSocket pong frames do not. An empty bucket sends
`message_rate_limited` and closes the session.

The default per-device publish token bucket adds 60 tokens per minute up to a
10-token burst. One publish attempt consumes one token before payload
validation. An empty bucket returns `publish_rate_limited` and writes no event
state. Connection and control-message limits use fixed metadata counters, not
payload inspection.

### 10. Publish transaction and validation precedence

For one authenticated `publish`, the hub performs these steps:

1. Validate the closed message schema and scalar forms.
2. Compare `source_device_id` with the authenticated device.
3. Validate created time, expiry, content type, decoded length, UTF-8, and
   content hash in that order.
4. Start the serialized storage transaction. Recheck active device state,
   session credential generation, administrative pause, and session history
   epoch.
5. Look up `message_id` in retained history and the replay ledger.
6. When retained history contains an exact retry, return its original cursor
   and expiry with `duplicate = true`; do not continue.
7. When the message ID exists with different fields, return
   `message_id_conflict`.
8. When only a message-ID tombstone exists, return `message_id_replay`.
9. Compare `source_seq` with the device high-water mark. Return
   `source_sequence_replay` when it is not greater.
10. In the same SQLite transaction or memory-state write lock, allocate the next
   cursor, insert the event, advance the source-sequence high-water mark, and
   insert the message-ID tombstone.
11. Remove expired events. Trim lowest cursors until the count limit holds.
    Update `lost_through_cursor` to the greatest removed cursor.
12. Commit. Enqueue `publish_accepted` to the source session. Enqueue the
    accepted event to each live or replay-buffering session in cursor order.

Hub cursor exhaustion returns `hub_cursor_exhausted`, marks hub readiness
false, and accepts no later publish. A desktop that has allocated source
sequence `18446744073709551615` enters `device_sequence_exhausted` and sends no
later publish under that device identity. Other devices remain active. A
counter never wraps.

Two concurrent requests with one message ID or one source sequence serialize
at step 4. One can commit. The other observes committed state and follows the
retry or replay rules.

### 11. Resume algorithm

When the hub accepts `resume`, it holds the event-state serialization seam long
enough to:

1. register the session as a buffering subscriber;
2. capture current cursor `B` or null when no event has been accepted;
3. capture the current history epoch and `lost_through_cursor`;
4. create a retained-event snapshot with cursors greater than the effective
   requested cursor and less than or equal to `B`. The effective cursor is null
   when the known epoch differs.

The hub then releases event-state serialization and sends:

1. `resume_started` with `fresh`, `complete`, `gap`, or `epoch_changed`;
2. each unexpired snapshot event in ascending cursor order with
   `delivery = resume`;
3. `resume_complete` with boundary `B`;
4. each event buffered after `B` in ascending cursor order with
   `delivery = live`;
5. later accepted events directly with `delivery = live`.

If `after_cursor` exceeds `B`, the hub sends `cursor_ahead` and closes. For this
comparison, null `B` is below each positive cursor, so any nonnull
`after_cursor` is ahead when `B` is null. If the known epoch differs, the
client clears its ClipMesh cache before it processes resume events. A `gap`
remains visible in client status. It does not cause a desktop clipboard write
or a guessed repair.

Resume status precedence is `epoch_changed`, then `fresh`, then `gap`, then
`complete`. The hub tests epoch mismatch first. With a matching epoch it tests
for null `after_cursor`, then a cursor ahead of `B`, then a cursor behind
`lost_through_cursor`.

The snapshot excludes events expired when the snapshot transaction runs. It
still sends a snapshot event that expires while replay is in progress. A client
discards an event whose expiry is at or before its current UTC time and
advances the pending acknowledgement cursor without applying or displaying the
payload. This keeps the cursor sequence and the earlier gap status truthful.

### 12. Persistence, expiry, restart, and purge

SQLite history mode uses one database under the configured state directory
with file mode `0600`, parent mode no broader than `0700`,
`PRAGMA secure_delete = ON`, `journal_mode = DELETE`, and
`synchronous = FULL`.

The durable model separates:

- device and credential records;
- mutating HTTP request receipts;
- administrative pause state;
- current history epoch, cursor high-water mark, and lost-through cursor;
- per-device source-sequence high-water marks;
- content-free message-ID tombstones;
- payload-bearing retained events.

Mutating HTTP request receipts persist for the lifetime of hub state. Device
and credential records persist through revocation. Expired pending-enrollment
cleanup is the only version-1 device-row deletion. Version 1 has no deletion
operation for an active or revoked device.

A retained event stores its source ID, source display-name snapshot, source
sequence, timestamps, content type, payload length, content hash, and payload.
Expiry deletes the complete retained event row. A tombstone stores only message
ID, source device ID, source sequence, and accepted cursor. It stores no payload
length, hash, preview, or label. A tombstone persists for the lifetime of its
device row. Version 1 has no device-delete operation, so revocation and purge
do not delete tombstones.

The hub runs expiry and count trimming:

- inside each accepted-publish transaction;
- before it creates a resume snapshot;
- once per 60 seconds while ready.

An event is expired when hub time is greater than or equal to
`expires_at_ms`. Queries filter expired rows even before the periodic delete
commits.

SQLite history survives an ordinary clean or crash restart. Before readiness,
the hub deletes expired rows and verifies count bounds. It preserves the epoch
when retained history continuity remains available.

Memory history mode keeps the payload-bearing event map in memory. It writes
the cursor, replay metadata, and device administration to SQLite without
payload fields. Startup after a prior process instance clears the in-memory
map, replaces the epoch, and sets `lost_through_cursor` to the prior cursor
high-water mark.

Global purge runs through one administrator mutation seam:

1. start one storage transaction;
2. capture the greatest retained cursor;
3. delete each retained event row;
4. replace the history epoch with a new UUIDv4;
5. set `lost_through_cursor` to the cursor high-water mark;
6. insert the nonsecret purge receipt;
7. commit the transaction;
8. send `purge_notice` to online sessions;
9. close each data-plane session with `history_purged`;
10. return the committed purge response.

Purge uses the same serialized writer as publish. A publish ordered before
purge is deleted by that purge. A publish attempt from an old-epoch session
ordered after purge returns `session_epoch_stale` and closes. A new-epoch
session can publish after it completes resume. Per-session output ordering
sends `purge_notice` before the close and prevents an old-epoch event after the
notice.

With SQLite `secure_delete`, the delete overwrites freed database content. The
specification makes no claim about copies outside the database file, storage
snapshots, controller remapping, or hardware recovery.

An online client clears its ClipMesh history on `purge_notice`. An offline
client detects the new epoch at its next session and clears before it sends
`resume`. A desktop clear deletes pending outbox payloads, its last processed
cursor, processed message IDs, the pending remote-write marker, and the prior
local-observation hash. It installs the new epoch and a null processed cursor
before it can open the new-epoch session. A mobile clear deletes visible
history and its current-session cursor before it processes new-epoch resume
events. A client does not clear its operating-system pasteboard, device
credential, or source-sequence allocator.

### 13. Desktop outbox and state machine

The desktop agent persists these local values in an owner-only state store
with secure-delete behavior:

- unaccepted outbox events;
- the highest allocated source sequence;
- the last processed hub cursor and history epoch;
- the 1,024 most recent processed message IDs ordered by hub cursor;
- one pending remote-write suppression marker.

It persists credentials separately through Keychain on macOS or an owner-only,
non-symlink secret file on Linux. It never accepts a credential on a command
line.

For one eligible local clipboard observation, the agent:

1. obtains clipboard bytes and platform metadata from the adapter;
2. holds the agent-state serialization seam;
3. confirms state `active_unlocked` and confirms the observation is current;
4. stops when the adapter supplied `sensitive = true`;
5. consumes `local_only_next` and stops when that flag is armed;
6. computes the local content hash; stops when it equals the immediately prior
   observed local content hash in this process generation; otherwise stores it
   as the in-memory prior hash;
7. applies the one-shot remote-write loop marker;
8. validates non-empty UTF-8 and the current server payload limit;
9. deletes expired outbox items, then checks whether this event would cross an
   outbox bound; on overflow it enters `outbox_full` without allocating a
   sequence or retaining the new payload;
10. allocates the next local source sequence without reuse;
11. creates one UUIDv4 message ID, sets `created_at_ms` from UTC corrected by
   the offset observed in `server_hello`, sets `expires_at_ms` to creation plus
   the hello retention limit, computes the hash, and creates the outbox event;
12. commits the sequence and outbox event before releasing the state seam;
13. sends or retries that exact event after the session reaches `live`.

An accepted response removes the outbox item. A retryable rejection retains
it. A permanent validation, replay, or expiry rejection quarantines it as
content-free failure metadata and deletes the payload. Source-sequence gaps
remain valid.

The outbox holds at most 20 events and 1,048,576 decoded payload bytes. Reaching
either bound enters `outbox_full`, stops new clipboard observation, and keeps
existing outbox events for retry. The local clipboard value that would cross
the bound remains local and is not queued later. The agent deletes an expired outbox payload,
records a content-free `event_expired` result, and leaves its allocated source
sequence unused. When accepted or expired items bring both bounds below their
limits, the agent returns to its prior active network state.

For one received `event`, the desktop agent:

1. verifies protocol fields, hash, payload length, UTF-8, epoch, and expiry;
2. records cursor and message ID;
3. ignores the payload when `delivery = resume`;
4. ignores the payload when source device equals the local device;
5. ignores a duplicate processed message ID;
6. holds the agent-state serialization seam;
7. confirms state `active_unlocked` and `delivery = live`;
8. reads the current clipboard hash;
9. skips the write when current bytes already equal the event bytes;
10. writes exact text through the platform adapter;
11. stores one loop marker containing message ID and content hash;
12. releases the state seam and advances the pending acknowledgement cursor.

The loop marker is consumed by the first subsequent local clipboard
observation. A matching content hash suppresses publish. A differing hash
clears the marker and proceeds as a new local observation. This rule contains
no time window. The consecutive-content rule suppresses an additional watcher
notification for the same bytes after marker consumption.

Desktop agent states are:

| State | Clipboard watch | Publish | Remote write | Network |
| --- | --- | --- | --- | --- |
| `starting_unknown_lock` | off | off | off | off |
| `active_unlocked` | on | on | live only | connected or reconnecting |
| `locked` | off | off | off | disconnected |
| `locally_paused` | off | off | off | disconnected |
| `administratively_paused` | off | off | off | authentication refused until unpaused |
| `outbox_full` | off | retry existing | off | connected or reconnecting |
| `adapter_failed` | off | off | off | disconnected; readiness false |
| `stopping` | off | off | off | closing |

A lock, pause, or adapter-failure transition increments a state generation and
cancels an observation that has not committed its outbox event. An unlock or
local resume starts a new WebSocket session. Resume material cannot change the
clipboard. The first event accepted after the new resume boundary can.

The agent exposes an owner-only local control interface for:

- `status`;
- `pause`;
- `resume`;
- `local-only-next`.

The interface uses local IPC, not a TCP listener. Its peer credentials must
match the desktop user. `local-only-next` arms one in-memory flag and reveals
no clipboard content. A service restart clears that flag.

Reconnect delay uses full jitter. Attempt `n`, starting at zero, selects a
random delay in `0..min(30000, 500 * 2^n)` milliseconds. A successful live
session lasting 30 seconds resets `n` to zero. Authentication, revocation,
administrative pause, invalid TLS, invalid configuration, credential-storage,
and adapter failures do not retry automatically; they remain visible until
their external cause changes or the user requests retry.

### 14. Platform desktop behavior

The Wayland adapter uses `wl-paste --watch` to observe clipboard changes and
`wl-copy` to write exact UTF-8 text. It captures the real advertised MIME list
before it maps a recognized sensitive hint. It ignores a clipboard that does
not offer plain UTF-8 text. Command stderr is converted to a reason code and is
not copied verbatim into ordinary diagnostics.

The macOS adapter uses native pasteboard APIs. It records the change count
created by its own write and uses that observed count as the primary loop
marker. It maps recognized sensitive pasteboard types from captured real API
responses. It stores the bearer credential in Keychain.

Each adapter emits one domain observation containing bytes, observed platform
revision, and `sensitive` boolean. Shared agent code never receives the raw
platform type list. This seam prevents diagnostics and protocol code from
serializing platform metadata that can reveal content origin.

### 15. Mobile state machine and presentation

The mobile client keeps fetched payload history and its current-session cursor
in memory only. It persists the device credential in Keychain. It persists the
history epoch and content-free connection status in protected app preferences.
It does not persist payloads, previews, content hashes, or device display
names.

Mobile states are:

| State | Network | Visible history | Pasteboard write |
| --- | --- | --- | --- |
| `unenrolled` | enrollment only | empty | none |
| `inactive` | closed | obscured; in-memory history retained | none |
| `foreground_connecting` | TLS and resume | prior in-memory entries marked stale | explicit selection only |
| `foreground_live` | connected | resume and live entries | explicit selection only |
| `foreground_error` | closed or retryable | current unexpired in-memory entries | explicit selection only |

On foreground activation, the client opens a session with its known history
epoch and `after_cursor = null`. The hub therefore returns the complete current
retained window instead of only successors to the prior foreground session.
The client replaces the visible list with that returned history and tracks a
cursor in memory until it leaves foreground. Manual refresh closes the current
session and performs the same flow. Background transition closes the WebSocket
and covers payload UI before the operating system captures an app-switcher
snapshot.

The history view orders entries by descending hub cursor. Each row shows the
source display name, age `max(0, current_utc_ms - created_at_ms)`, and at most
160 Unicode scalar values of text. It replaces C0 controls other than tab,
carriage return, and line feed with U+FFFD for display. It collapses each
whitespace run in the preview to one space. These transformations affect
preview only. The view removes an entry at its expiry before the next render or
selection action.

Selecting one unexpired row while active writes the exact decoded event text
to `UIPasteboard.general`. The client performs no pasteboard read. It shows a
content-free success state. A local-clear action empties visible history
without changing the current session cursor, calling administrator purge, or
changing the system pasteboard.

`purge_notice` or an epoch change clears visible history before the client
renders new resume events. A live event updates the foreground list but does
not write to the pasteboard.

### 16. Observability

The Rust protocol crate provides `ClipboardPayload`, `ContentHash`,
`DeviceCredential`, `AdministratorCredential`, and `EnrollmentArtifact`
wrappers with fixed redacted `Debug` and `Display` implementations. Only
explicit wire and adapter methods can access their inner bytes.

Ordinary structured logs can contain:

- UTC timestamp;
- component and stable event code;
- severity;
- request ID, session ID, device ID, message ID, cursor, or purge ID;
- protocol version;
- state transition names;
- bounded counts and durations;
- a reason code.

They cannot contain payload bytes, payload base64, previews, content hashes,
exact payload lengths, credentials, authorization headers, request bodies,
response bodies that contain a secret, raw platform clipboard types, or device
display names.

Metrics use fixed names and labels from protocol version, component, state,
and reason code. They do not use device, session, message, source label,
payload, hash, or credential values as labels.

`GET /healthz` returns HTTP 200 and exactly
`{"status":"ok"}` after the process starts its health surface.

`GET /readyz` returns HTTP 200 and
`{"status":"ready","protocol_version":1}` only when configuration, TLS,
storage, counters, and administrator state permit data-plane service. It
returns HTTP 503 and
`{"status":"not_ready","reason_code":<CODE>}` otherwise. It contains no
fleet counts or identifiers.

Crash reporting is disabled by default. If a deployment enables it, the crash
path uses the same metadata-only event type and excludes process memory,
request bodies, environment values, command lines, and local state files.

### 17. Stable failure codes

| Code | Surface | Retryable | State effect |
| --- | --- | --- | --- |
| `config_parse_failed` | startup | no | process exits before serving |
| `config_unknown_field` | startup | no | process exits before serving |
| `config_missing_required` | startup | no | process exits before serving |
| `config_value_invalid` | startup | no | process exits before serving |
| `bind_address_disallowed` | startup | no | process exits before serving |
| `bind_failed` | startup | yes after external repair | opened sockets close; process exits |
| `tls_material_invalid` | startup | no | process exits before serving |
| `tls_certificate_not_current` | startup or readiness | yes after certificate replacement and restart | process exits or readiness becomes false |
| `secret_file_insecure` | startup or desktop | no | component remains inactive |
| `state_path_insecure` | startup or desktop | no | component remains inactive |
| `local_state_unavailable` | desktop | no automatic retry | agent remains inactive; source sequence does not reset |
| `database_schema_unsupported` | startup | no | process exits without migration |
| `database_integrity_failed` | startup | no | process exits without serving |
| `unauthorized` | HTTP | no | none |
| `administratively_paused` | upgrade or publish | no | none |
| `connection_limit_reached` | upgrade | yes | none |
| `request_rate_limited` | HTTP | yes | none |
| `request_too_large` | HTTP | no | none |
| `message_rate_limited` | WebSocket | yes after reconnect | none; close session |
| `protocol_version_unsupported` | HTTP or WebSocket | no | none |
| `protocol_schema_invalid` | HTTP or WebSocket | no | none; close WebSocket |
| `resume_required` | WebSocket | no | none; close |
| `resume_deadline_exceeded` | WebSocket | yes | none; close |
| `cursor_ahead` | WebSocket | no | none; close |
| `resume_cursor_without_epoch` | WebSocket | no | none; close |
| `session_epoch_stale` | publish | yes after reconnect | none; close |
| `source_device_mismatch` | publish | no | none |
| `message_id_conflict` | publish | no | none |
| `message_id_replay` | publish | no | none |
| `source_sequence_replay` | publish | no | none |
| `created_at_in_future` | publish | yes after clock repair | none |
| `event_expired` | publish | no | none |
| `expiry_exceeds_retention` | publish | no | none |
| `content_type_unsupported` | publish | no | none |
| `payload_empty` | publish | no | none |
| `payload_too_large` | publish | no | none |
| `payload_encoding_invalid` | publish | no | none |
| `payload_length_mismatch` | publish | no | none |
| `payload_hash_mismatch` | publish | no | none |
| `publish_rate_limited` | publish | yes | none |
| `hub_cursor_exhausted` | publish or readiness | no | hub readiness false |
| `device_sequence_exhausted` | desktop | no | affected device publishing stops |
| `ack_invalid` | WebSocket | no | none; close session |
| `slow_consumer` | WebSocket | yes | close session |
| `heartbeat_timeout` | WebSocket | yes | close session |
| `credential_rotated` | WebSocket | no | close affected sessions after committed rotation |
| `device_revoked` | WebSocket | no | close affected sessions after committed revocation |
| `history_purged` | WebSocket | yes after reconnect | close affected sessions after committed purge |
| `enrollment_artifact_invalid` | enrollment | no | none |
| `secret_result_already_committed` | control plane | no | returns committed resource ID only |
| `request_id_conflict` | control plane | no | none |
| `credential_storage_failed` | client | no automatic retry | server operation can already be committed |
| `storage_unavailable` | hub | yes after repair | readiness false; no partial event commit |
| `adapter_unavailable` | desktop | no automatic retry | agent inactive |
| `lock_state_unknown` | desktop | no automatic retry | agent acts locked |
| `outbox_full` | desktop | yes after drain or expiry | observation stops; existing retry continues |
| `tls_validation_failed` | client | no automatic retry | no WebSocket or clipboard action |

The wire and readiness code set is closed for protocol v1. An implementation
can add a private internal log code only when it cannot cross a wire or health
surface and a test proves it content-free.

HTTP status mapping is exact:

| Status | Codes |
| --- | --- |
| 200 or 201 | Named success response |
| 400 | `protocol_version_unsupported`, `protocol_schema_invalid` |
| 401 | `unauthorized` |
| 409 | `request_id_conflict`, `secret_result_already_committed` |
| 410 | `enrollment_artifact_invalid` |
| 413 | `request_too_large` |
| 423 | `administratively_paused` on a data-plane upgrade |
| 429 | `connection_limit_reached`, `request_rate_limited` |
| 503 | `storage_unavailable`, `hub_cursor_exhausted`, `tls_certificate_not_current`, or global `administratively_paused` on readiness |

A WebSocket close frame uses the stable code as its UTF-8 reason and one of
these private close numbers:

| Close number | Reasons |
| --- | --- |
| 4400 | `protocol_version_unsupported`, `protocol_schema_invalid`, `resume_required`, `cursor_ahead`, `resume_cursor_without_epoch`, `ack_invalid` |
| 4403 | `administratively_paused`, `credential_rotated`, `device_revoked` |
| 4408 | `resume_deadline_exceeded`, `heartbeat_timeout` |
| 4409 | `session_epoch_stale`, `history_purged` |
| 4429 | `slow_consumer`, `message_rate_limited` |
| 4500 | `storage_unavailable`, `hub_cursor_exhausted` |

The hub sends the corresponding `error`, `pause_notice`, or `purge_notice`
application message before the close when the WebSocket can still accept an
outbound message. A client treats a close without that message by its close
number and reason. It does not display raw transport text to the user.

### 18. Topology-neutral repository checks

CI runs one repository-boundary command over the tracked tree, staged diff,
and reachable Git history. The command performs these checks:

1. a secret scanner finds no known token, private key, authorization header,
   high-entropy assignment, or credential-shaped value;
2. a ClipMesh token regex rejects
   `cm_(dev|admin|enroll)_v1_[A-Za-z0-9_-]{43}` in tracked bytes;
3. configuration examples contain no active listener, hub URL, credential,
   user home, private inventory, or service-specific address;
4. example network names use only the reserved domain `example.invalid` or an
   explicit angle-bracket placeholder;
5. fixture UUIDs come from a documented synthetic fixture namespace;
6. deployment templates reference variables instead of private inventory;
7. logs, snapshots, and error fixtures contain none of the content and secret
   canaries used by the observability tests;
8. the repository root carries the exact MIT license text;
9. when `CLIPMESH_PRIVATE_DENYLIST_FILE` names an external owner-only file, the
   scanner matches each nonblank literal against tracked bytes, staged diff,
   and reachable Git history and fails on one match. The command prints only
   the denylist line number and repository path or commit, not the private
   literal.

CI fixtures use loopback, reserved example domains, synthetic device names,
and synthetic UUIDs. Bind-classification unit tests construct address classes
from numeric octets and prefixes; an address in such a test is evidence of an
RFC class, not a deployment default.

The external denylist remains optional for public CI because the public
repository does not own private topology. A deployment release gate supplies
it. Passing generic CI alone is not evidence about values CI was never given.

### 19. Real-response fixture capture plan

Handwritten ideal responses cannot establish an external seam. Before a
platform or transport adapter merges, its builder captures responses from the
real library, process, database, simulator, or operating system named below.

Capture rules:

1. Run an isolated test hub and clients with synthetic clipboard text, reserved
   example names, synthetic UUIDs, and credentials created only for that run.
2. Keep raw captures outside the public repository in an owner-only directory.
3. Record the command, tool version, operating-system version, test scenario,
   UTC time, and exit status in the build assignment log. Record the raw-capture
   SHA-256 only in an owner-only manifest beside the raw capture.
4. Run a structural sanitizer that parses the response and replaces credential
   values with typed markers. The sanitizer fails on an unknown credential-like
   string. It does not invent or reorder fields.
5. Commit the sanitized response plus its SHA-256 and capture metadata that
   contains no private path, hostname, username, address, credential, or raw
   hash of a secret-bearing response. The build assignment log names the
   sanitized fixture SHA-256 and states whether the owner-only raw manifest was
   recorded.
6. Replay the sanitized fixture through the production parser. Separately run
   the same conformance assertion against a fresh unsanitized response in an
   isolated test.

Required real captures are:

| Seam | Capture |
| --- | --- |
| rustls hub | Successful TLS 1.3 handshake; invalid chain; wrong name; expired certificate; non-TLS request |
| WebSocket | Upgrade, hello, resume with history, live publish, exact retry, replay rejection, gap, slow consumer, rotation close, purge notice |
| Administrator HTTPS | Device creation, artifact issuance, artifact exchange, rotation, revocation, pause, purge, repeated request ID |
| SQLite | Accept and restart; expiry delete; count trim; global purge; secure-delete database inspection |
| Wayland | Real `wl-paste --watch` observation, MIME discovery, `wl-copy` echo, lock transition, command failure |
| macOS | Real pasteboard bytes, type list, change count after local and remote writes, lock transition, Keychain success and refusal |
| iOS/iPadOS | URLSession WebSocket frames, foreground/background transitions, Keychain storage, explicit `UIPasteboard.general` write, app-switcher privacy cover |

The sensitive-hint registry can add one platform signal only after a capture
shows that signal on a real platform response and a test proves that the
adapter emits `sensitive = true` without passing payload bytes to the outbox.

## Acceptance

The evidence column names the minimum proof. A reviewer can request more
evidence when a named test did not exercise the claimed boundary.

| ID | Traces to | Given / When / Then | Required evidence |
| --- | --- | --- | --- |
| A01 | I1, Architecture 2-5 | Given Rust and Swift version-1 implementations, when each decodes and re-encodes the canonical publish fixture and sanitized real-capture corpus, then the publish fixture preserves its exact field values and payload bytes, each captured message preserves its canonical field semantics, and each unsupported version is rejected before message handling. | Rust and Swift conformance logs plus captured fixtures |
| A02 | I1, Architecture 2 and 5 | Given a valid message, when one unknown field, duplicate key, wrong type, binary frame, oversized frame, decreasing ack, future ack, or wrong-epoch ack is introduced separately, then the receiver returns the specified protocol code and writes no durable state. | Table-driven negative tests |
| A03 | I2 | Given device A's credential and an event asserting device B, when A publishes, then the hub returns `source_device_mismatch`; history, cursor, and A's sequence high-water mark remain unchanged. | Hub integration test with database before/after snapshot |
| A04 | I3, Architecture 6 | Given one credential of each class, when each calls each protected path, then only the exact class-path pair succeeds; invalid and wrong-class credentials return the same `unauthorized` body. | Complete credential-path matrix |
| A05 | I4 | Given a valid client configuration, when the server chain is invalid, the name is wrong, the certificate is expired, or the endpoint is plaintext, then the client opens no WebSocket and performs no clipboard action. | Real rustls and platform client captures |
| A06 | I4, Architecture 8 | Given hub configurations with an empty listener list, wildcard, global, multicast, link-local, documentation, or unresolvable bind value, when the hub starts, then it exits nonzero before any accept loop. | Startup tests and socket probe |
| A07 | I4, Architecture 8 | Given two configured allowed sockets and the second cannot bind, when the hub starts, then it closes the first socket and exits nonzero. | Real socket test |
| A08 | I4, Architecture 8 | Given a symlink, wrong owner, or mode broader than the specified secret, key, database, or state-directory mode, when the component starts, then it remains inactive with one content-free code. | Unix permission tests |
| A09 | I5 | Given 25 accepted events from concurrent devices, when clients read history and live delivery, then each observes one identical ascending cursor order with no reused cursor. | Concurrency integration log and database query |
| A10 | Goal, normal delivery | Given normal delivery conditions, when one desktop copies 100 synthetic texts sequentially, then each target clipboard write completes within 1,000 ms of source observation. | Timestamped end-to-end test log |
| A11 | I6 | Given one accepted retained event and rate buckets configured to admit ten retries, when its source retries the exact event ten times, then each retry returns the original cursor with `duplicate = true`; history count and peer live-delivery count remain at their post-acceptance values of one. | Hub, peer, and database counters |
| A12 | I6 | Given one accepted event, when a client reuses its message ID with a changed field, reuses its source sequence with a new ID, or reuses its tombstoned ID after purge, then the exact replay code returns and no cursor or history state changes. | Replay matrix with before/after state |
| A13 | I6, Architecture 10 | Given two concurrent publishes with one message ID, when the hub serializes them, then one commits and the other returns exact retry or conflict according to its bytes. | Concurrency test repeated 100 times |
| A14 | I7 | Given events accepted during a deliberately blocked resume send, when the resume completes, then events at or below boundary B arrive as `resume` before `resume_complete`; later cursors arrive as `live` in order with no gap. | Deterministic barrier integration test |
| A15 | I7 | Given a client cursor behind `lost_through_cursor`, when it resumes, then `resume_started.status = gap`, retained successors arrive in order, and no guessed event appears. | Expiry and count-gap tests |
| A16 | I8 | Given a desktop clipboard value and missed retained events, when the agent reconnects, unlocks, or leaves local pause, then it processes resume cursors without changing that clipboard value. | Linux and macOS real adapter tests |
| A17 | I8 | Given a completed resume and an unlocked active target, when another device publishes a new live event, then the target writes exact UTF-8 bytes once. | Linux and macOS real adapter tests |
| A18 | I9 | Given a remote live write that triggers duplicate local watcher notifications, when those observations match, then the agent sends no publish; when a later different observation occurs, then it publishes once without waiting for a timer. | Adapter event-sequence tests |
| A19 | I10 | Given a local observation paused at the agent state barrier, when lock or pause wins the barrier, then no outbox row or publish exists; when outbox commit wins first, then the event follows normal retry rules and the transition performs no later clipboard action. | Deterministic state-race tests |
| A20 | I10, Architecture 14 | Given each recognized sensitive hint captured from a real platform, when the clipboard changes, then no payload enters outbox, wire, log, metric, or error; one content-free suppression counter increases. | Real platform capture and canary scan |
| A21 | I10, Architecture 13 | Given `local-only-next`, when two eligible local changes occur, then the first remains local and the second publishes; no payload crosses the local control interface. | Local-control integration test |
| A22 | I11 | Given default config and one 262,144-byte UTF-8 payload, when it publishes, then it is accepted; a 262,145-byte payload returns `payload_too_large` without state change. | Boundary tests |
| A23 | I11 | Given default config and 21 unexpired accepted events, when event 21 commits, then history contains cursors 2 through 21 and `lost_through_cursor` is at least cursor 1. | Database and resume test |
| A24 | I11 | Given one event whose expiry is reached, when history is queried before and after the periodic delete, then neither query delivers it and the row is deleted within 60 seconds. | Controlled-clock storage test |
| A25 | I13 | Given SQLite history with retained events, when the hub restarts ordinarily, then epoch, cursor order, replay high-water state, and unexpired history remain. | Real process restart test |
| A26 | I13 | Given memory history with retained events, when the hub restarts, then payload history is empty, the epoch changes, replay of an old source sequence is rejected, and no payload bytes exist in SQLite. | Real process restart and database scan |
| A27 | I12 | Given retained history and pending online plus offline desktop outbox events, when an administrator purges, then the hub response reports a committed new epoch, online clients clear on notice, the offline client clears on next hello, no purged outbox payload republishes, and no client changes its system pasteboard. | Hub, mobile, desktop, and database test |
| A28 | I3, Architecture 6 | Given two active devices, when an administrator revokes one, then its current session closes and its next upgrade returns `unauthorized`; the other device remains live and can publish. | Multi-device integration test |
| A29 | I3, Architecture 6 | Given one active device, when an administrator rotates it, then the old credential and session stop working, the new credential opens one session, and the plaintext new credential appears only in the first response. | Rotation and secret-canary test |
| A30 | I3, Architecture 6 | Given one mobile enrollment artifact, when two exchanges with distinct request IDs race before ten minutes, then one returns a credential and one returns `enrollment_artifact_invalid`; when an unconsumed artifact reaches ten minutes, then no exchange succeeds, its pending device row is deleted within 60 seconds, and its digest tombstone disappears 86,400 seconds after expiry. | Controlled-clock concurrency and storage test |
| A31 | I15, Architecture 15 | Given 20 retained events, when the app enters foreground, then it displays descending history with source, age, and bounded preview; selecting one unexpired row writes exact text once to `UIPasteboard.general`. | Swift UI and real pasteboard test |
| A32 | I15 | Given resume, live delivery, refresh, activation, background, and epoch-change transitions, when each occurs without row selection, then a pasteboard write spy records zero calls. | Swift state-machine test |
| A33 | I14, Architecture 16 | Given unique payload, base64, payload hash, device label, device credential, admin credential, and enrollment canaries, when success and each failure class run, then logs, metrics, health, errors, and crash fixtures contain none of those canaries. | Byte-for-byte canary scan |
| A34 | I14, Architecture 16 | Given ready and not-ready hub states, when health and readiness are requested, then their status, body, and reason-code shapes match this specification and contain no identifiers or counts. | Real HTTP captures |
| A35 | Architecture 9 | Given configured connection, per-device, publish, and outbound queue limits, when each boundary is exceeded separately, then the named refusal or close occurs; accepted peer sessions preserve cursor order. | Limit matrix |
| A36 | I16, Architecture 18 | Given the tracked repository, when generic boundary checks and a synthetic external denylist run, then clean bytes pass; one seeded token, hostname, private literal, active listener default, or content canary fails with path and no secret echo. | CI log and seeded-failure tests |
| A37 | Goal, Architecture 1 | Given generic systemd, launchd, and Ansible assets, when rendered with reserved synthetic values, then each passes its native syntax check and exposes variables for binary, hub URL, device ID, credential reference, retention, and startup behavior. | Native syntax checks and rendered fixture |
| A38 | Non-Goals, Architecture 1 | Given the repository root, when the license check runs, then it finds the canonical MIT license and no contradictory project license. | License scan |
| A39 | Architecture 19 | Given each external seam in the capture table, when its tests merge, then the assignment evidence names a real capture, sanitizer, sanitized fixture, fresh-response conformance run, and topology/secret scan. | Capture log, fixture provenance, and test log |
| A40 | Goal, Non-Goals | Given the built MVP dependency graph and wire schema, when reviewed, then it contains no Share extension, E2EE key distribution, mTLS, hub election, direct-delivery, image/file MIME path, public listener, private inventory, or deployment mutation. | Dependency and repository census |
| A41 | Goal, Architecture 6 | Given an administrator credential held by synthetic deployment automation, when it creates a managed desktop, stores the returned device credential through the declared secret reference, and starts the agent, then the device opens a live session without an action on an existing device. | Isolated Ansible-to-agent acceptance run |
| A42 | I4, Architecture 8 | Given a hub bound to one allowed address in an isolated network namespace, when probes target that address and a second unbound interface, then only the configured address completes TLS. | Network-namespace socket and TLS probe log |
| A43 | Architecture 15 | Given foreground mobile history and a nonempty system pasteboard, when the user invokes local clear, then visible history empties while the session cursor, hub history, and system pasteboard remain unchanged. | Swift state, hub query, and pasteboard assertions |
| A44 | I10, Architecture 6 | Given two active devices, when an administrator pauses one device, then that session closes and the peer remains live; when the administrator pauses globally, then both data sessions close while an authenticated administrator can remove the pause. | Administrative pause matrix |
| A45 | I4, Architecture 8 | Given one valid configuration, when each required field is removed, each unknown field is added, and each bounded value crosses its lower or upper bound separately, then startup exits with the exact configuration code before any listener accepts. | Generated configuration mutation matrix |
| A46 | I17, Architecture 6 and 10 | Given a publish stopped at the storage barrier and a concurrent rotation, revocation, pause, or purge, when each ordering is released separately, then the publish commits entirely before the administrator mutation or writes nothing after it; no stale credential or epoch commits later. | Deterministic transaction-race tests |
| A47 | I18, Architecture 17 | Given one trigger for each stable failure code, when the component fails, then it emits that code and retryability, its state diff matches the table, and its response contains none of the content or secret canaries. | Failure-code matrix with state snapshots and canary scan |
| A48 | Architecture 13 | Given a disconnected active agent, when another observation would take its outbox above 20 events or 1,048,576 bytes, then the new payload remains local without sequence allocation, observation stops with `outbox_full`, existing items remain exact, and accepting or expiring enough items resumes observation. | Persistent outbox boundary and restart test |
| A49 | Architecture 10 | Given a synthetic hub cursor at unsigned-64 maximum, when a device publishes, then the hub returns `hub_cursor_exhausted` and becomes not ready; given one device source sequence at maximum, when that agent observes a new copy, then only that agent stops publishing with `device_sequence_exhausted` while another device remains live. | Injected counter-boundary tests |
| A50 | I4, Architecture 8 | Given a running hub certificate, an established readiness connection, and an established data session, when the certificate crosses expiry and the 60-second validity check runs, then readiness on the established connection returns `tls_certificate_not_current`, a new handshake cannot complete, and the existing data session closes only at its ordinary boundary. | Controlled-clock real TLS process test |
| A51 | I6, I17, Architecture 13 | Given an enrolled desktop that has committed source sequence 41 and one unaccepted outbox event, when the process restarts with intact local state, then it retries the exact event with its original sequence and allocates 42 for the next eligible observation. | Real process restart and local-state inspection |
| A52 | I6, I18, Architecture 8 and 13 | Given an enrolled desktop credential with missing, corrupt, read-only, or non-atomic local state, when the agent starts, then it emits `local_state_unavailable`, allocates no source sequence, opens no data-plane session, and remains inactive until the state is restored or a new device identity is enrolled. | Local-state failure matrix with network and outbox probes |
| A53 | I7, Architecture 5 and 9 | Given a default 20-event resume followed by live events, when a client processes the replay and live stream, then it sends one highest-cursor acknowledgement after `resume_complete`, coalesces later acknowledgements to at most one per 2,000 milliseconds, and does not exhaust the application-message bucket. | Controlled-clock client and hub message trace |
| A54 | I3, Architecture 6 and 7 | Given a consumed enrollment artifact whose exact exchange response was lost, when the client repeats the same request ID and body before tombstone expiry, then the hub returns `secret_result_already_committed` with the committed device ID and no credential; a different request ID returns `enrollment_artifact_invalid` and writes nothing. | Request-receipt and controlled-clock storage test |

### Acceptance execution order

1. Run schema, scalar, and authority tests before platform tests.
2. Capture real external responses before accepting their fixtures.
3. Run hub persistence and state-machine tests against a real hub process and
   real SQLite file.
4. Run Linux, macOS, and mobile adapter tests on their named platforms.
5. Run the content-canary and repository-boundary scans over test output and
   tracked bytes.
6. Run the cross-platform normal-delivery test last because it depends on each
   earlier seam.

A release claim records test command, platform, tool versions, commit, fixture
provenance, pass count, failure count, and elapsed time. Passing compile-only or
mock-only tests does not satisfy a real-response row.

## Open Questions

No blocking product question remains for this MVP. The following questions are
explicitly **NON-BLOCKING**:

1. **NON-BLOCKING — initial sensitive-hint registry entries.** Which exact
   Wayland MIME identifiers and macOS pasteboard types do the first real
   captures support? Architecture 14 and acceptance A20 let protocol, hub,
   desktop state, and fixture work proceed. A capture can support zero or more
   registry entries. The adapter suppresses each captured recognized entry and
   makes no claim about an unrecognized signal.
2. **NON-BLOCKING — Linux lock-state provider selection.** Which available
   session-lock API supplies the real lock event on the supported Wayland test
   distribution? The agent domain seam treats unavailable or unknown state as
   locked, so the choice does not alter protocol or security semantics.
3. **NON-BLOCKING — local IPC implementation.** Should the platform adapter use
   an owner-only Unix-domain socket or a native per-user service IPC for agent
   control? Architecture 13 fixes commands, peer authorization, and effects.
   The transport choice cannot introduce a TCP listener or payload transfer.
4. **NON-BLOCKING — future protocol work.** A later product decision can study
   a Share extension, end-to-end encryption, additional clipboard types,
   direct delivery, or native Wayland capture. None is a version-1 extension;
   each requires a new reviewed specification and, when the wire changes, a
   new protocol version.

Operating pattern taught to agents: none. This specification defines ClipMesh
product behavior and does not amend Tightbeam operating guidance.
