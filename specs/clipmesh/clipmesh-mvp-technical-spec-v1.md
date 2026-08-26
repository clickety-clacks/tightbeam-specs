# ClipMesh MVP technical specification v1

Status: policy amendment candidate for independent adversarial review. These
bytes authorize no implementation, product-code edit, integration, deployment,
publication, release, listener activation, enrollment, or live or
private-state mutation.

Authority and evidence:

- Canonical seed: ClipMesh `docs/initial-spirit.md` at
  `89c6579dc1ddc180ce22e954ecc39cc410eee887`, artifact
  `art_3d431942`, SHA-256
  `60e59c7b7e200a6ce70114ebad34e420cf291e4d6c4e3493f1d3b297f3e85b9a`.
- Prior canonical technical specification: tightbeam-specs commit
  `b59444fcd0d5321b73dd800146adcb67b8754177`, artifact
  `art_6b0b9064`, SHA-256
  `0f51ae73fdfa5ae479794daaddbcb59c09e20e53c59f817fe57edbf5eed31c8d`.
- Mike's authoritative MVP update:
  `att_91cda21f-c8c0-4b5a-9ef0-5ac2473e46c1`.
- Product-owner policy:
  `att_29c3a660-ee1a-4eb1-9f4c-7b5f177b6523`.
- Product-owner Spirit digest:
  `att_b4f90db5-0211-4c92-92a8-85bf14567af9`.
- Cold digest verdict:
  `att_c17096fc-7f34-4ef1-80dc-f5ceabee007a`.
- Bounded delivery plan:
  `att_4e2ae985-61ba-4539-8c7b-1115aa4526e7`.
- Mechanism verification: Tailscale's identity documentation states that a
  destination application can use LocalAPI to identify the node that made a
  request; the official `tailscale.com/client/local` package documents
  `Client.WhoIs` as a stable API. Verified 2026-08-26 against
  <https://tailscale.com/docs/concepts/tailscale-identity> and
  <https://pkg.go.dev/tailscale.com/client/local#Client.WhoIs>.
- Work item `wi_0507efeb-914b-4289-9930-30cd36eb7e88` owns the
  product thread. Assignment
  `asg_3c97d196-571f-4a54-8d41-c4b48b03a727` owns this amendment
  until one independent exact-commit review returns.

The canonical `clipmesh-spirit-v1.md` at the same candidate commit controls
product intent. This technical specification controls the build contract. A
material clarification amends both canonical files before affected work
resumes.

## Goal

Define one buildable text-only ClipMesh MVP for a small personal Tailnet. The
MVP contains a Rust hub, Rust Wayland Linux and macOS agents, a foreground
SwiftUI iOS and iPadOS client, and generic deployment assets.

The hub is trusted to read plaintext clip content. Tailscale WireGuard protects
transit. The local `tailscaled` LocalAPI authenticates each inbound peer.
ClipMesh creates no application identity, credential, device, enrollment, or
administrator system.

The specification makes the following behaviors decidable from evidence:
Tailnet-only binding, peer identity, equal-member authority, protocol
compatibility, content serialization, cursor ordering, retry and replay,
resume, live clipboard overwrite, loop suppression, persistent retention,
shared clear, platform behavior, diagnostics, migrations, and repository
neutrality.

The design adds three application mechanisms because deleting any one would
break a core outcome: one ordered SQLite state writer, one durable clear
generation, and one canonical clip-content serialization seam. Accepting
unordered state, pre-clear replay, or divergent content encodings would make
the clipboard contract false or undecidable.

## Non-Goals

- End-to-end or zero-knowledge payload encryption.
- Application accounts, pool keys, bearer credentials, device records,
  administrator endpoints, enrollment, pairing, rotation, credential expiry,
  or recurring onboarding.
- Application TLS, mutual TLS, a TLS certificate identity, or a certificate
  handoff.
- Images, files, HTML, RTF, or another clipboard MIME type.
- Public-Internet discovery or a public listener.
- Multi-tenant hosting, billing, social sharing, or application fleet
  administration.
- Passive iOS or iPadOS background clipboard monitoring.
- An iOS or iPadOS Share extension.
- Memory-only hub history.
- Hub election, failover, or direct peer-to-peer clip delivery.
- A desktop clipboard-manager interface.
- Payload heuristics for secret or sensitive-content detection.
- Erasure from an offline client, a current system clipboard, a storage
  snapshot, or storage hardware.
- A private Tailnet, host, address, username, filesystem layout, inventory
  boundary, or deployment target in public bytes.
- Implementation, target integration, deployment, publication, release,
  listener activation, or mutation of a live or private system.

## Terms

- **Tailnet:** The deployment's Tailscale network. Tailscale WireGuard
  authenticates nodes and encrypts their traffic.
- **LocalAPI:** Tailscale's local client interface to the `tailscaled`
  daemon on the same host. Version 1 relies on the specifically stable WhoIs
  operation and confines other LocalAPI compatibility inside one adapter.
- **WhoIs:** The stable LocalAPI operation documented by
  `local.Client.WhoIs(context, remoteAddr)`. The Rust
  `tailscale_identity` adapter performs that operation through the system
  local daemon connection and resolves an accepted socket's observed remote
  address to a Tailscale node.
- **Stable peer ID:** The nonempty `WhoIsResponse.Node.StableID` returned by
  LocalAPI. It is the ClipMesh session's source identity.
- **ACL-admitted member:** A Tailnet peer that can reach the configured hub
  socket under Tailnet policy and for which WhoIs returns a stable peer ID.
- **Client identity claim:** A header, query value, URL value, WebSocket
  subprotocol value, or application-message field that asks ClipMesh to treat
  the client as a named peer. Version 1 accepts no such claim.
- **Clip content:** Nonempty UTF-8 text represented in memory by
  `ClipContentV1`.
- **Canonical clip-content serialization seam:** The
  `ClipContentV1` module and type boundary. It alone validates decoded text,
  encodes or decodes wire base64url, calculates or checks content length and
  SHA-256, supplies or consumes a persistent content BLOB, compares content
  bytes, and produces a bounded UI preview.
- **Message ID:** A client-generated canonical UUIDv4 that identifies one
  publish across retries.
- **Clear request ID:** A client-generated canonical UUIDv4 that identifies
  one shared-clear request across retries. Message IDs and clear request IDs
  are global version-1 identifiers, not member-scoped identifiers.
- **Cursor:** A positive unsigned 64-bit integer allocated monotonically by
  the hub when it accepts a clip. Cursor order is history and delivery order.
- **History epoch:** A hub-generated UUIDv4 that names one supported SQLite
  continuity line. An ordinary restart preserves it.
- **Clear generation:** A positive unsigned 64-bit integer stored by the hub.
  It starts at 1 and advances by one in the same transaction as shared clear.
- **Resume boundary:** Cursor `B`, captured in the same serialized action
  that registers a resuming subscriber. Cursors at or below `B` are resume
  material. Clips accepted afterward are live material.
- **Live remote clip:** A clip accepted after the receiving session's resume
  boundary whose stable source peer ID differs from the receiving session's
  stable peer ID.
- **Exact retry:** A repeated publish whose stable source peer ID, message ID,
  clear generation, client creation timestamp, and clip content bytes equal
  one retained accepted clip.
- **Replay ledger:** Durable content-free message-ID tombstones. The ledger is
  not a member registry and grants no authority.
- **Shared clear:** An admitted member's request that atomically deletes
  retained clip rows and increments clear generation.
- **Explicit confidential or transient hint:** A real platform signal that the
  operating system or source application directly attaches to one clipboard
  entry and that a captured adapter mapping classifies as `confidential` or
  `transient`.
- **Local pause:** A desktop state that stops clipboard observation,
  publishing, remote writes, and the data session.
- **Local-only next copy:** A one-shot desktop control that suppresses the next
  eligible local observation before it creates `ClipContentV1`.
- **Content-free diagnostic:** A log, metric, health response, error, or crash
  fixture that cannot represent clip content, a preview, content length,
  content hash, raw platform metadata, stable peer ID, Tailnet user data, or a
  payload-derived string.
- **Generic fixture:** Synthetic test material made from reserved example
  values and containing no private deployment value.
- **Normal delivery conditions:** Two admitted desktop clients connected to
  one test hub; network round-trip time at most 100 ms; packet loss zero; clip
  size at most 4 KiB; no pause; both desktops unlocked; hub and clients below
  70 percent CPU utilization.

## Assumptions

1. The hub host runs a supported Tailscale client with a reachable LocalAPI.
2. LocalAPI `WhoIs` returns a nonempty node stable ID for a connection that
   Tailnet policy admits to the hub.
3. The configured hub bind address is one of the current self Tailnet
   addresses reported by the same local Tailscale client.
4. Tailnet policy owns reachability. ClipMesh does not inspect or reproduce
   Tailnet policy.
5. The deployment owner accepts a hub that reads plaintext clips.
6. Tailscale WireGuard protects traffic in transit. FileVault, LUKS, or mobile
   protected storage protects retained endpoint history at rest.
7. Linux MVP hosts run a supported Wayland session with real clipboard and
   lock-state surfaces.
8. macOS exposes native pasteboard change counts, declared types, and a
   lock-state signal.
9. iOS and iPadOS permit foreground WebSocket use and writes to
   `UIPasteboard.general`.
10. A client clock stays within two minutes of the hub clock. The hub rejects
    a clip outside that bound.
11. The build can test Rust, Swift, SQLite, LocalAPI, socket confinement, and
    real platform adapters on their respective targets.
12. The repository root can carry the MIT license before release.

## Invariants

These clause identities replace the same-numbered clauses in the prior
technical specification. A decomposition that cites one of them must re-read
this candidate before it resumes.

### I1 — One explicit protocol version

Rust owns the canonical version-1 domain and wire schema. Swift maps that
schema without a second interpretation. Each application message carries
`protocol_version = 1`. A receiver rejects another version before
message-specific handling.

### I2 — Local Tailscale identity determines the session peer

For each accepted TCP socket, the hub calls LocalAPI WhoIs with the socket's
observed remote address before it parses an HTTP request. The hub binds the
returned stable peer ID to the connection lifetime. It closes the socket when
WhoIs fails or returns no stable ID. No client value can select or modify the
session peer.

### I3 — ACL-admitted members have equal application authority

Each established member can resume history, publish text, acknowledge
delivery, and request shared clear. The protocol has no privileged member,
administrator operation, device-control operation, or application membership
mutation.

### I4 — Tailnet-only application transport fails closed

The hub has no listener default. Before binding, it obtains the host's current
Tailnet self addresses through LocalAPI and requires each configured bind IP to
equal one of them. It rejects wildcard, loopback, LAN, public, documentation,
multicast, and link-local addresses. A LocalAPI, identity, configuration, or
bind failure starts no accept loop.

Application traffic is plaintext HTTP and WebSocket over Tailnet WireGuard.
Version 1 has no application TLS or plaintext fallback to a second interface.

### I5 — Accepted clips have one total order

The hub allocates one cursor in the same SQLite transaction that accepts a
clip. Cursor values increase without reuse. History queries, resume material,
and live delivery use ascending cursor order.

### I6 — Retry is idempotent and replay changes no state

An exact retry of a retained clip returns its original cursor with
`duplicate = true`. It creates no row and no second live delivery. A reused
message ID with changed input or a tombstoned message ID is rejected without
cursor, history, replay, or clear-generation change.

### I7 — Resume and live transition form one boundary

The hub registers the subscriber and captures resume cursor `B` in one
serialized action. It buffers clips accepted after `B` until it sends
`resume_complete(B)`. It then sends those clips in ascending cursor order as
live material. The transition is indivisible with respect to publish and
shared clear.

### I8 — Catch-up never writes a system clipboard

A desktop or mobile client processes resume material into ClipMesh history and
cursor state without a platform clipboard write. After
`resume_complete`, each new live remote clip invokes one exact platform
write when the desktop is active and unlocked or the mobile app is foreground.
Self-source, duplicate, expired, pre-clear, and already-processed clips invoke
no write.

### I9 — Clipboard loops terminate without a timer

A client suppresses its own message IDs, processed message IDs, and the first
local observation caused by its most recent remote write. It decides from
identifiers, platform revisions, and byte equality. No elapsed-time threshold
decides loop identity.

### I10 — Lock, pause, and source hints fail closed

A desktop with unknown lock state acts locked. Lock and local-pause
transitions cancel an uncommitted local observation. An explicit confidential
or transient hint prevents `ClipContentV1` creation. The client uses no
content, pattern, source-name, or timing heuristic. State check and outbox
commit or clipboard-write invocation share one serialized client boundary.

### I11 — Retention age, count, and payload limits compose

The hub accepts a clip only within the configured payload bound. It assigns
expiry from hub acceptance time. Queries omit expired rows. The serialized
writer deletes expired rows and then the lowest cursors until the configured
count holds.

Defaults are 262,144 bytes per clip, 604,800 seconds of retention, and 500
retained clips. Generic bounded configuration can change each value. No value
permits unbounded retention.

### I12 — Shared clear is an atomic generation boundary

The hub processes shared clear through the same SQLite writer as publish. One
transaction deletes retained clip rows, advances clear generation, updates the
lost-through cursor, and stores a content-free request receipt. Before the
seam releases, the hub drops queued old-generation event frames and prevents a
session writer from handing another one to WebSocket output. It preserves the
cursor high-water mark and message-ID tombstones. A publish bound to an
earlier generation is rejected. Clients delete product history and pre-clear
outbox content but do not change their system clipboard.

### I13 — SQLite is the only hub history mode

The hub persists epoch, clear generation, cursors, replay metadata, clear
receipts, and retained clips in one SQLite database. An ordinary clean or
crash restart preserves unexpired history and ordering. Version 1 exposes no
memory mode.

### I14 — Diagnostics cannot represent content or Tailnet identity

`ClipContentV1` has fixed-redaction `Debug` and `Display`.
Diagnostic types contain no clip bytes, preview, content length, content hash,
stable peer ID, Tailnet address, Tailnet user profile, raw LocalAPI response,
or payload-derived string.

### I15 — Foreground mobile combines live overwrite with explicit history

The foreground mobile client catches up into a descending history view without
a pasteboard write. After catch-up, a new live remote clip writes once to
`UIPasteboard.general`. The user can also select one retained row to write
its exact text. Background, resume, refresh, activation, clear, and epoch or
generation change write nothing.

### I16 — The public repository is topology-neutral

Source, defaults, examples, fixtures, tests, documentation, and templates
contain no value copied from a private deployment. Runtime topology enters
only through external configuration or inventory. An optional external exact
denylist stays outside the repository.

### I17 — One ordered mutation seam owns shared state

The hub SQLite writer alone mutates cursors, history, replay metadata, clear
generation, and clear receipts. Publish, resume-boundary capture, retention,
and shared clear serialize at that seam. Each client state machine alone
commits outbox, history projection, clear, and platform-write decisions.

### I18 — Each failure is explicit and content-free

Startup, LocalAPI, peer identity, admission, validation, rate, resume, clear,
storage, and platform failures produce one stable reason code. A failure
changes no state unless its response names an already committed idempotent
publish or clear.

### I19 — One seam serializes clip content across ingress, storage, and egress

Only `ClipContentV1` converts wire content to validated UTF-8 bytes, provides
the SQLite BLOB, reconstructs content from that BLOB, compares content, or
produces wire, platform, and preview output. Hub and client protocol handlers,
repositories, diagnostics, platform state machines, and UI code cannot create
or interpret a second content representation.

## Architecture

### 1. Components and ownership

| Surface | Owner | Required contents |
| --- | --- | --- |
| `clipmesh-protocol` Rust crate | Shared protocol | Closed version-1 schemas, scalar validation, `ClipContentV1`, redacted wrappers, fixtures, Rust and Swift conformance corpus |
| `clipmesh-hub` Rust binary | Hub | LocalAPI client, Tailnet-only listener, WhoIs admission, WebSocket protocol, SQLite state writer, retention, shared clear, health and readiness |
| `clipmesh-agent` Rust binary | Desktop | Session client, persistent outbox, cursor and generation state, reconnect, loop suppression, local controls, platform adapter interface |
| Wayland adapter | Desktop | Real clipboard observation and writes, platform revision, lock state, explicit confidential/transient mapping |
| macOS adapter | Desktop | Native pasteboard observation and writes, change-count loop marker, lock state, explicit confidential/transient mapping |
| `ClipMesh` SwiftUI target | Mobile | Version-1 mapping, foreground session, explicit history, live remote pasteboard write |
| Deployment assets | Packaging | Generic systemd and launchd templates, Ansible-friendly configuration variables, SQLite state setup |
| Repository checks | CI | Cross-language protocol checks, topology scan, content-canary scan, obsolete-surface scan, MIT license check |

The repository root carries the MIT license. This document establishes the
`ClipMesh protocol v1` and `ClipContentV1` patterns only for ClipMesh.

### 2. Tailnet transport and encoding

1. The hub exposes one configured TCP listener whose IP passes Architecture 8.
2. The listener accepts HTTP/1.1 and WebSocket on plaintext application bytes.
   Tailnet WireGuard owns transport authentication and encryption.
3. The data path is `GET /v1/stream` with WebSocket subprotocol
   `clipmesh.v1`.
4. The client sends no `Authorization`, identity, forwarding, proxy, or
   device header. The hub rejects `Authorization`,
   `X-Forwarded-For`, `Forwarded`, and `X-ClipMesh-*` on the stream
   request with `client_identity_claim_forbidden`.
5. The request URL contains no user information, query, or fragment.
6. Each application message is one UTF-8 JSON object in a WebSocket text
   message. Binary, invalid UTF-8, duplicate-key, unknown-field, missing-field,
   wrong-type, and unknown-message input is invalid.
7. WebSocket compression is disabled.
8. The maximum decoded WebSocket text message is
   `4 * ceil(max_payload_bytes / 3) + 4096` bytes. A receiver rejects a
   larger frame before JSON parsing.
9. The hub sends a WebSocket ping after 30 seconds without outbound traffic.
   It closes after 10 more seconds without the matching pong.
10. Version 1 has no alternate HTTP listener, redirect listener, TLS listener,
    or proxy-trusted identity-header mode.

### 2.1. Version compatibility

A version-1 client offers only `clipmesh.v1`. A version-1 hub selects that
exact subprotocol or refuses the upgrade. Neither side falls back to an
unversioned protocol.

An implementation fix can remain version 1 only when every field, scalar,
enum, validation rule, state transition, and observable response remains
unchanged. Adding, removing, renaming, or reinterpreting one wire value
requires a later reviewed protocol version.

### 3. Canonical scalar forms

| Scalar | Version-1 form | Validation |
| --- | --- | --- |
| `protocol_version` | JSON integer | Exact value `1` |
| UUID field | JSON string | Lowercase canonical UUIDv4 with hyphens |
| `cursor`, `clear_generation` | JSON string | Decimal `1` through `18446744073709551615`; no sign or leading zero |
| Timestamp | JSON integer | Signed 64-bit Unix epoch milliseconds in UTC |
| `content_type` | JSON string | Exact value `text/plain` |
| `payload_b64` | JSON string | RFC 4648 base64url without padding |
| `content_sha256` | JSON string | 64 lowercase hexadecimal characters |
| Stable peer ID | internal string | Nonempty LocalAPI `Node.StableID`; never accepted in client input |
| Reason code | JSON string | One lowercase snake-case value from Architecture 17 |

The protocol preserves UTF-8 bytes exactly. It performs no Unicode
normalization or newline conversion.

### 4. Clip content and publish schema

`ClipContentV1` is an opaque domain type. Its module exposes only these
operations:

| Operation | Input | Output and rule |
| --- | --- | --- |
| `from_wire` | `payload_b64`, `payload_bytes`, `content_sha256` | Decode base64url; require nonempty valid UTF-8; enforce size; require exact length and hash; return `ClipContentV1` |
| `from_platform` | UTF-8 bytes | Require nonempty bytes within the active size limit; return `ClipContentV1` |
| `as_storage_blob` | `ClipContentV1` | Borrow exact UTF-8 bytes for one hub or desktop SQLite content-BLOB bind |
| `from_storage_blob` | persistent BLOB | Revalidate nonempty UTF-8 and the version-1 hard maximum of 1,048,576 bytes; return `ClipContentV1` or fail storage integrity. A lower current ingress limit does not invalidate an older retained row. |
| `to_wire` | `ClipContentV1` | Produce base64url, byte count, and SHA-256 |
| `to_platform` | `ClipContentV1` | Borrow exact UTF-8 bytes for one platform write |
| `same_content` | two `ClipContentV1` values | Return exact byte equality for loop suppression |
| `to_preview` | `ClipContentV1`, scalar limit | Decode text; replace C0 controls except tab, carriage return, and line feed with U+FFFD; collapse each whitespace run to one space; return no more than the requested Unicode scalar count |

No other module can construct the type, validate or transform content, or
extract stored bytes except through these operations. Storage and wire
metadata are outputs of this seam, not parallel sources of truth.

A client-authored publish has exactly:

| Field | Type | Rule |
| --- | --- | --- |
| `message_id` | UUID string | Client-generated UUIDv4 |
| `clear_generation` | decimal string | Must equal the session generation |
| `created_at_ms` | integer | At most 120,000 ms ahead of hub time and no more than one retention window behind hub time |
| `content_type` | string | Exact `text/plain` |
| `payload_bytes` | integer | Exact decoded length in `1..max_payload_bytes` |
| `content_sha256` | string | SHA-256 of decoded bytes |
| `payload_b64` | string | Unpadded base64url of valid UTF-8 bytes |

The publish contains no source identity. The hub adds stable source peer ID,
`accepted_at_ms`, `expires_at_ms`, cursor, and history epoch as server
metadata. Expiry equals
`accepted_at_ms + retention_seconds * 1000`.

This is the canonical synthetic fixture:

```json
{
  "protocol_version": 1,
  "type": "publish",
  "event": {
    "message_id": "00000000-0000-4000-8000-000000000001",
    "clear_generation": "1",
    "created_at_ms": 1700000000000,
    "content_type": "text/plain",
    "payload_bytes": 12,
    "content_sha256": "5cb72f90e968922d30557d0af8f719d21f61792becaa87eb32477767d739dc0b",
    "payload_b64": "Zml4dHVyZSB0ZXh0"
  }
}
```

### 5. WebSocket message schemas

Each object contains exactly `protocol_version`, `type`, and the fields
listed below.

Client to hub:

| Type | Additional fields | Valid state |
| --- | --- | --- |
| `resume` | `known_history_epoch` UUID or null; `known_clear_generation` decimal or null; `after_cursor` decimal or null | `await_resume` |
| `publish` | `event` from Architecture 4 | `live` |
| `ack` | `history_epoch`, `clear_generation`, `cursor` | `replaying` or `live` |
| `clear_history` | `request_id` UUID; `expected_clear_generation` decimal | `live` |

Hub to client:

| Type | Additional fields | Meaning |
| --- | --- | --- |
| `server_hello` | `session_id`, `self_peer_id`, `history_epoch`, `clear_generation`, `newest_cursor` or null, `server_time_ms`, `limits` | WhoIs succeeded; resume is required |
| `resume_started` | `history_epoch`, `clear_generation`, `status`, `requested_after_cursor` or null, `boundary_cursor` or null, `lost_through_cursor` or null | Names catch-up snapshot |
| `event` | `history_epoch`, `clear_generation`, `cursor`, `delivery`, `accepted_at_ms`, `expires_at_ms`, `source_peer_id`, `event` | One resume or live clip |
| `resume_complete` | `history_epoch`, `clear_generation`, `boundary_cursor` or null | Ends catch-up |
| `publish_accepted` | `message_id`, `cursor`, `expires_at_ms`, `duplicate` | Publish committed or exact retry |
| `publish_rejected` | `message_id` or null, `code`, `retryable` | Publish changed no state |
| `clear_accepted` | `request_id`, `clear_generation`, `cleared_through_cursor` or null, `duplicate` | Shared clear committed or exact request retry |
| `clear_rejected` | `request_id` or null, `code`, `retryable` | Clear changed no state |
| `clear_notice` | `request_id`, `clear_generation`, `cleared_through_cursor` or null | Client clears product history and older outbox content |
| `error` | `code`, `retryable` | Session failure |

`limits` contains exactly `max_payload_bytes`, `retention_seconds`,
`history_max_entries`, `max_clock_skew_ms = 120000`, and
`max_websocket_message_bytes`.

`resume_started.status` is `fresh`, `complete`, `gap`,
`epoch_changed`, or `generation_changed`. Generation mismatch takes
precedence over epoch, fresh, gap, and complete because it requires deletion
of pre-clear client state.

`event.delivery` is `resume` at or below the captured boundary and
`live` afterward. The hub sends events to the source session so each client
maintains a contiguous cursor view. The client compares `source_peer_id`
with server-asserted `self_peer_id`; client input never supplies either
value.

Acknowledgements are nondecreasing and cannot exceed the highest cursor sent
on that session. During catch-up, a client coalesces its cursor and sends one
acknowledgement after `resume_complete`. During live delivery it sends at
most one acknowledgement per 2,000 ms.

### 6. Local Tailscale peer-identity seam

The hub uses Tailscale's stable LocalAPI client, not a shell command or HTTP
header:

1. At startup, the hub opens the operating system's standard local
   `tailscaled` connection with read permission only.
2. It reads LocalAPI status and extracts the current self Tailnet addresses.
3. It validates the configured bind IP against that exact set before it binds.
4. For each accepted socket, it captures `remoteAddr` from the socket.
5. Before HTTP parsing, it calls the `tailscale_identity` adapter's WhoIs
   operation for `remoteAddr` through the same local daemon.
6. It accepts the connection only when the call succeeds and
   `WhoIsResponse.Node.StableID` is nonempty.
7. It stores that stable peer ID only in the connection context and retained
   clip provenance required for server event metadata. It does not accept an
   identity from a request.

The hub ignores `UserProfile`, node name, Tailnet address, tags, and
capabilities for application authority. Each admitted result is an equal
member. Raw LocalAPI responses never enter logs, metrics, errors, or public
fixtures.

The adapter does not spawn `tailscale`, accept proxy headers, or use a
network-reachable identity service. The build pins its Tailscale compatibility
version. The adapter rejects an unrecognized status or WhoIs shape. Its
supported request and response shapes come from the real captures in
Architecture 19.

A LocalAPI timeout is 2,000 ms. Timeout, permission failure, daemon
unavailability, peer-not-found, malformed response, or empty stable ID closes
the socket before the hub reads an HTTP byte. The hub records only the stable
content-free code `tailnet_peer_unverified`.

### 7. Admission and validation order

The hub applies these steps:

1. configured socket acceptance;
2. LocalAPI WhoIs for the observed remote address;
3. request size, path, method, and WebSocket upgrade;
4. forbidden identity-header and URL checks;
5. exact `clipmesh.v1` subprotocol;
6. connection and message-rate admission;
7. closed message-schema validation;
8. state-machine and transaction validation.

An unknown path returns HTTP 404 `http_path_not_found`. A wrong method on a
known path returns HTTP 405 `http_method_not_allowed`. A request header
section above 16,384 bytes returns HTTP 431 `request_headers_too_large`.
These responses occur only after WhoIs succeeds.

Each HTTP error body is exactly
`{"protocol_version":1,"error":{"code":<CODE>,"retryable":<BOOLEAN>}}`.

WhoIs failure returns no application response because the hub has not admitted
the connection. Validation at a later step does not disclose the stable peer
ID or raw request value.

### 8. Configuration, binding, startup, and migrations

The hub reads one closed version-1 TOML file:

| Field | Required | Default or range |
| --- | --- | --- |
| `config_version` | yes | Exact integer `1` |
| `listen_address` | yes | One explicit IP socket address; no hostname |
| `tailscale_localapi` | no | Exact value `system` |
| `state_directory` | yes | Existing or creatable owner-only directory |
| `retention_seconds` | no | `604800`; `60..31536000` |
| `history_max_entries` | no | `500`; `1..10000` |
| `max_payload_bytes` | no | `262144`; `1..1048576` |
| `max_connections` | no | `64`; `1..1024` |
| `publish_tokens_per_minute` | no | `60`; `1..600` |
| `publish_burst` | no | `10`; `1..100` |
| `outbound_queue_messages` | no | `128`; `1..1024` |
| `outbound_queue_bytes` | no | `8388608`; computed message cap through `33554432` |

The parser rejects an unknown or duplicate field, a missing required field, a
value outside its range, trailing non-TOML bytes, a hostname bind, and a queue
byte bound below one maximum message.

The hub permits no bind before LocalAPI status succeeds. The configured IP
must exactly equal a current self Tailnet IPv4 or IPv6 address. The hub does
not accept prefix membership as proof. A port value of zero is invalid. Bind
failure, LocalAPI loss before bind, database failure, or migration failure
closes opened resources and exits before an accept loop.

The state directory is owner-only and no broader than `0700`. The database,
WAL, and shared-memory sidecar are regular non-symlink files no broader than
`0600`. The hub refuses a wrong owner, symlink, unsupported schema, failed
integrity check, or inconsistent counter.

SQLite `PRAGMA user_version` is the migration authority:

- a new empty database initializes schema version 1 in one transaction;
- a version-1 database receives no migration;
- any other nonempty or versioned schema returns
  `database_schema_unsupported` without modifying the file.

The prior quarantine schemas were never release or live-state authority. This
MVP defines no in-place migration from their application identity,
administration, enrollment, or memory-history tables. A later need for
custodial data migration requires a separate reviewed spec and explicit
private-state authority.

The desktop client requires `config_version = 1`, an explicit
`ws://` hub URL whose host is one numeric Tailscale IPv4 or IPv6 address,
with no user information, query, or fragment, plus a platform and owner-only
local-state location. The URL is runtime topology and has no public default.
The client rejects a hostname, `wss`, `http`, `https`, an address
outside Tailscale's node-address ranges. It sends no application credential
and uses no client-side LocalAPI identity assertion. An unavailable valid
endpoint follows the reconnect state machine.

The mobile build receives the same numeric Tailnet `ws://` URL through
deployment configuration and applies the same URL-shape rejection. It
persists no application identity or secret. It keeps payload history only
while the app process is active.

### 9. Hub session state machine and limits

| State | Entry | Accepted input | Exit |
| --- | --- | --- | --- |
| `tailnet_identity` | TCP accepted | No application input | WhoIs success enters `http_upgrade`; failure closes |
| `http_upgrade` | Peer context fixed | One HTTP request | Valid stream upgrade enters `await_resume`; failure responds and closes |
| `await_resume` | WebSocket accepted; `server_hello` sent | One `resume` within 5 seconds | Valid resume enters `replaying`; other input closes with `resume_required` |
| `replaying` | Boundary captured; subscriber registered | `ack`, pong | After `resume_complete`, enter `live` |
| `live` | Catch-up complete | `publish`, `ack`, `clear_history`, pong | Clear, slow consumer, heartbeat, LocalAPI loss, client close, or protocol error enters `closing` |
| `closing` | Close reason selected | No application input | Send close when possible; unregister and release limits |

The listener permits at most `max_connections` admitted WebSocket sessions.
It permits at most four sessions per stable peer ID. Reaching a bound returns
`connection_limit_reached`.

One admitted peer receives a connection-attempt bucket of 30 per minute with a
burst of 10, an application-message bucket of 120 per minute with a burst of
20, and the configured publish bucket. These counters are metadata-only.

Each session has configured outbound message and byte bounds. Crossing either
closes that session with `slow_consumer`; the hub drops no cursor silently.
The client reconnects from its last processed cursor.

Once per 60 seconds the hub probes LocalAPI status. Loss marks readiness false
and stops new accepts. Existing sessions close with
`tailscale_localapi_unavailable` at their next application-message,
heartbeat, or 60-second probe boundary. The hub does not invent a grace
period that decides peer identity.

### 10. Publish transaction and validation precedence

For one admitted `publish`, the hub performs:

1. Parse one closed JSON object. Schema failure returns
   `protocol_schema_invalid`.
2. Require integer `protocol_version = 1`; another integer returns
   `protocol_version_unsupported`.
3. Validate canonical UUID, decimal, timestamp, content-type, base64url,
   length, and hash syntax.
4. Require `created_at_ms <= hub_time + 120000`; otherwise return
   `created_at_in_future`.
5. Require
   `created_at_ms >= hub_time - retention_seconds * 1000`; otherwise
   return `event_too_old`.
6. Call `ClipContentV1::from_wire`. Its ordered failures are
   `content_type_unsupported`, `payload_encoding_invalid`,
   `payload_empty`, `payload_too_large`,
   `payload_length_mismatch`, and `payload_hash_mismatch`.
7. Enter the one SQLite writer transaction.
8. Require the event clear generation to equal current state. A lower
   generation returns `clear_generation_stale`; a higher generation returns
   `clear_generation_ahead`.
9. Recheck that the session remains live and its peer context remains valid.
10. Look up message ID in retained clips and the replay ledger.
11. Return the original cursor and `duplicate = true` for an exact retained
    retry.
12. Return `message_id_conflict` for retained changed input or
    `message_id_replay` for a tombstone.
13. Allocate the next cursor, compute accepted time and expiry, insert one clip
    using `ClipContentV1::as_storage_blob`, and insert a content-free
    tombstone.
14. Delete expired clip rows. Trim lowest cursors until the count limit holds.
    Advance `lost_through_cursor` to the greatest removed cursor.
15. Commit.
16. Before releasing the serialized hub mutation seam, enqueue
    `publish_accepted` for the source session and the accepted event in
    cursor order for each live or replay-buffering session.

Two concurrent requests with one message ID serialize at step 7. One can
commit. The other observes committed state.

Cursor exhaustion returns `hub_cursor_exhausted`, marks readiness false,
and accepts no later publish.

### 11. Resume algorithm

Before it enters the serialized hub seam, the hub validates the three client
context fields as one closed shape. A fresh client sends all three as null. A
continuing client sends nonnull history epoch and clear generation; its cursor
can be null or nonnull. A nonnull cursor without both context values returns
`resume_cursor_without_context`. Any other partial-null combination returns
`resume_context_incomplete`. Both failures register no subscriber and change
no state.

When the hub accepts a valid `resume`, the serialized hub seam:

1. compares known clear generation with the current value;
2. compares known history epoch with the current value;
3. registers the session as a buffering subscriber;
4. captures current cursor `B` or null;
5. captures `lost_through_cursor`;
6. snapshots unexpired clips after the effective cursor through `B`.

The effective cursor is null after generation or epoch mismatch. The hub then
releases the seam and sends:

1. `resume_started`;
2. snapshot clips in ascending cursor order with `delivery = resume`;
3. `resume_complete`;
4. buffered clips in ascending cursor order with `delivery = live`;
5. later accepted clips directly with `delivery = live`.

Status selection is exact. A nonnull generation that differs from current is
`generation_changed`. Otherwise, a nonnull epoch that differs from current is
`epoch_changed`. All-null context is `fresh`. Matching context with a
nonnull cursor below `lost_through_cursor` is `gap`. Every other valid shape
is `complete`. This order is the precedence order. A generation change makes
the client delete visible history, processed IDs, remote-write markers, and
outbox entries from
an older generation before it consumes resume content. It preserves its system
clipboard.

An `after_cursor` above `B` returns `cursor_ahead`. A `gap` remains visible
in product status. It does not guess missing content or write a system
clipboard.

The snapshot omits rows expired when its transaction runs. If a snapshot row
expires during transmission, the client advances its cursor but omits the row
from product history and performs no platform write.

### 12. SQLite state, retention, shared clear, and restart

The hub uses one database with file mode `0600`, parent mode no broader than
`0700`, `PRAGMA foreign_keys = ON`, `secure_delete = ON`,
`journal_mode = WAL`, and `synchronous = FULL`.

Schema version 1 owns these tables:

| Table | Required state |
| --- | --- |
| `hub_meta` | one row: history epoch, clear generation, cursor high-water, lost-through cursor |
| `message_tombstones` | message ID primary key; accepted cursor, clear generation |
| `clips` | cursor primary key; message ID unique; source peer ID; clear generation; created, accepted, expiry timestamps; exact content BLOB |
| `clear_receipts` | request ID primary key; expected generation, committed generation, cleared-through cursor |

`clips.content` is the only payload-bearing hub column. It receives and
returns bytes only through `ClipContentV1`. A tombstone and clear receipt
store no content length, hash, preview, or source label.

The retained clip source peer ID is event provenance, not a member record. It
leaves SQLite on retention or shared clear. The durable tombstone and clear
receipt tables contain no peer identity. WhoIs admission never requires a
preexisting row. Version 1 exposes no peer-list, peer-create, peer-update,
peer-delete, or membership query. Message-ID tombstones persist for the
lifetime of hub state so an expired payload cannot become an accepted replay.

The hub runs expiry and oldest-first count trimming:

- inside each accepted publish transaction;
- before each resume snapshot;
- once per 60 seconds while ready.

A row expires when hub time is at or after its `expires_at_ms`. Queries omit
it even before periodic deletion.

For `clear_history`, the hub:

1. validates request ID and expected generation;
2. enters the common SQLite writer;
3. looks up the receipt by global request ID;
4. returns its result with `duplicate = true` when method input is exact;
5. returns `request_id_conflict` when that ID names different input;
6. requires expected generation to equal current generation;
7. fails with `clear_generation_exhausted` when current generation is the
   unsigned-64 maximum;
8. captures the greatest retained cursor;
9. deletes each retained clip;
10. increments clear generation;
11. sets lost-through cursor to cursor high-water;
12. inserts the content-free receipt;
13. commits;
14. removes queued resume and live event frames whose generation is older;
15. requires each session writer to recheck generation while holding the seam
    immediately before it hands a complete event frame to WebSocket output;
16. enqueues `clear_accepted` for the requester and `clear_notice` for
    each admitted session, marks those sessions closing with
    `history_cleared`, and releases the seam.

A publish ordered before clear commits and is then deleted. A publish ordered
after clear must carry the new generation. A pre-clear publish already decoded
but waiting for the writer fails generation recheck and writes nothing.
A complete old-generation frame handed to WebSocket output before clear commit
is pre-clear delivery and precedes `clear_notice` on that ordered stream. No
old-generation frame is handed to WebSocket output after clear commits.

On `clear_notice`, a client atomically deletes its ClipMesh history,
processed IDs, remote-write marker, and outbox content whose generation is
lower. It installs the new generation. It preserves the current system
clipboard, local pause, configuration, and newer outbox content.

An ordinary restart preserves each table. Before readiness the hub runs
`quick_check`, validates foreign keys and high-water relationships, deletes
expired rows, applies count trimming, and reconstructs no content outside
`ClipContentV1::from_storage_blob`.

### 13. Desktop outbox, state machine, and local controls

The desktop persists in one owner-only SQLite state store:

- unaccepted outbox events with their clear generation;
- last processed hub cursor, history epoch, and clear generation;
- the 1,024 most recent processed message IDs in cursor order;
- one pending remote-write suppression marker with exact content.

Each outbox and remote-write-marker content column is a BLOB written by
`ClipContentV1::as_storage_blob` and read by
`ClipContentV1::from_storage_blob`. The local store exposes no alternate
content column or serializer.

The desktop store uses SQLite `user_version = 1`, WAL mode, and atomic
transactions. Its parent directory is owner-only and no broader than `0700`.
Its database, WAL, and shared-memory files are regular non-symlink files no
broader than `0600`. An absent database initializes version 1 with null
resume context and an empty outbox; it creates no identity or onboarding
state. An unsupported, corrupt, insecure, read-only, or non-atomic store
returns `local_state_unavailable`, opens no session, and remains byte-identical
until external repair.

For one local observation the client:

1. obtains bytes, platform revision, and explicit hint classification;
2. enters the client state seam;
3. requires `active_unlocked_live` and the observation still current;
4. stops for `confidential` or `transient`;
5. stops when it consumes `local_only_next`;
6. calls `ClipContentV1::from_platform`;
7. applies the remote-write loop marker by platform revision or
   `ClipContentV1::same_content` and stops on a match;
8. deletes expired or stale-generation outbox rows;
9. enforces 128-event and 8,388,608-byte outbox bounds;
10. creates one message ID and publish bound to the current clear generation;
11. commits the exact outbox event before releasing the seam;
12. sends or retries that exact event only while the session is live.

The client observes no new clipboard value while connecting, replaying,
disconnected, locked, paused, or outbox-full. A value seen in those states is
not queued merely because state later becomes live.

A `publish_accepted` response deletes the matching outbox BLOB. A retryable
rejection retains the exact row. A permanent validation, replay, or stale
generation rejection records content-free failure metadata and deletes the
outbox BLOB. Message-ID reuse is not attempted.

For one received event the desktop:

1. validates schema, cursor, epoch, generation, expiry, and content through
   `ClipContentV1::from_wire`;
2. enters the client state seam;
3. rechecks cursor order, generation, and processed message ID;
4. records a previously unseen event in product history;
5. sets `apply = true` only for a new live remote clip in
   `active_unlocked_live`;
6. calls the platform write exactly once when `apply = true`, even when the
   current clipboard bytes are equal;
7. stores the message ID, exact content BLOB, and resulting platform revision
   as the remote-write loop marker;
8. advances the acknowledgement cursor.

The first later local observation consumes the loop marker. A matching
platform revision or matching bytes suppresses publish. A different
observation clears the marker and proceeds. No timer participates.

Desktop states:

| State | Observe | Publish | Remote write | Network |
| --- | --- | --- | --- | --- |
| `starting_unknown_lock` | off | off | off | off |
| `active_unlocked_connecting` | off | retry after live | off | connecting or replaying |
| `active_unlocked_live` | on | on | live remote only | connected |
| `locked` | off | off | off | disconnected |
| `locally_paused` | off | off | off | disconnected |
| `outbox_full` | off | retry existing | off | connected or reconnecting |
| `adapter_failed` | off | off | off | disconnected |
| `stopping` | off | off | off | closing |

Unlock, local resume, and reconnect enter
`active_unlocked_connecting`. Successful catch-up enters
`active_unlocked_live`. Resume material never changes the clipboard. The
first later live remote clip does.

The owner-only local non-TCP control interface exposes `status`, `pause`,
`resume`, `clear-local-history`, and `local-only-next`.
`clear-local-history` deletes local ClipMesh history and processed-ID cache
but preserves outbox, cursor, epoch, generation, hub history, and system
clipboard. Only shared clear deletes pre-clear outbox content.

Reconnect uses full jitter:
`0..min(30000, 500 * 2^n)` ms for attempt `n`. A live session lasting 30
seconds resets `n`. Invalid configuration, local-state failure, unknown lock
state, and adapter failure require an external repair before retry.

### 14. Platform hint and desktop adapter behavior

The Wayland adapter uses a captured real watch interface to observe clipboard
changes and a captured real write interface to write exact UTF-8 text. The
macOS adapter uses native pasteboard APIs and records the change count from its
own write.

Each adapter emits exactly:

- text bytes;
- one observed platform revision;
- `hint = ordinary | confidential | transient`.

The adapter can emit `confidential` or `transient` only for a signal
listed in a checked-in registry entry whose evidence names a real platform
capture. Unknown, absent, ambiguous, source-name-only, and content-derived
signals map to `ordinary`.

Shared code never receives a raw MIME list, pasteboard type list, source
application identity, or platform error text. Command or API failures become
stable reason codes.

### 15. Mobile state machine and explicit history

The mobile client keeps clip history, processed IDs, cursor, epoch, and clear
generation in memory while the app process is active. It stores only generic
hub configuration and content-free connection state in protected
preferences. It stores no application identity, credential, payload, preview,
content hash, or stable peer ID after process exit.

| State | Network | Visible history | Automatic pasteboard write |
| --- | --- | --- | --- |
| `inactive` | closed | obscured; in-memory rows can remain | none |
| `foreground_connecting` | connecting or replaying | prior rows marked stale | none |
| `foreground_live` | connected | resume and live rows | each new live remote clip once |
| `foreground_error` | closed or retryable | unexpired in-memory rows | none |

Foreground activation opens a session and resumes. Manual refresh repeats the
same catch-up. Background closes the WebSocket and covers clip UI before an
app-switcher snapshot.

The history view orders rows by descending cursor. Each row shows age and the
result of `ClipContentV1::to_preview(content, 160)`. UI code receives only
that bounded preview. Preview production never changes `ClipContentV1`.

Resume rows update visible history without a pasteboard write. In
`foreground_live`, each new live remote event calls
`UIPasteboard.general` once with exact `ClipContentV1::to_platform`
bytes. Selecting one unexpired history row also writes its exact bytes once.
The client performs no pasteboard read.

Local clear empties only visible local history. Shared `clear_notice`
empties history, processed IDs, and stale-generation state. Neither operation
changes the system pasteboard.

### 16. Observability and health

The shared Rust crate provides fixed-redaction `Debug` and `Display` for
`ClipContentV1`, `ContentHash`, and LocalAPI response wrappers.
Application errors accept metadata-only types.

Ordinary logs can contain:

- UTC timestamp;
- component and stable event code;
- severity;
- request ID, session ID, message ID, cursor, or clear generation;
- protocol version;
- state transition;
- bounded count or duration;
- stable reason code.

They cannot contain clip bytes, base64, preview, exact content length, content
hash, stable peer ID, Tailnet address, Tailnet node or user name, raw LocalAPI
response, request body, platform clipboard metadata, or payload-derived text.

Metrics use fixed labels from component, protocol version, state, and reason
code. They do not label by peer, session, message, cursor, Tailnet value, clip
metadata, or platform source.

After WhoIs admission, `GET /healthz` returns HTTP 200 and exactly
`{"status":"ok"}`. `GET /readyz` returns HTTP 200 and exactly
`{"status":"ready","protocol_version":1}` only when LocalAPI, binding,
SQLite, counters, and migrations permit service. Otherwise it returns HTTP
503 and exactly
`{"status":"not_ready","reason_code":<CODE>}`. Neither endpoint exposes a
public listener or accepts an unverified peer.

Crash reporting is off by default. If a deployment enables it, the crash path
excludes process memory, request bodies, environment values, command lines,
LocalAPI responses, and local state files.

### 17. Stable failure codes

| Code | Surface | Retryable | State effect |
| --- | --- | --- | --- |
| `config_parse_failed` | startup | no | exit before bind |
| `config_unknown_field` | startup | no | exit before bind |
| `config_missing_required` | startup | no | exit before bind |
| `config_value_invalid` | startup | no | exit before bind |
| `tailscale_localapi_unavailable` | startup, readiness, session | after daemon repair | no new accepts; existing session closes at defined boundary |
| `tailnet_bind_unverified` | startup | no | exit before bind |
| `tailnet_peer_unverified` | admission | yes on a new connection | close before HTTP parsing |
| `bind_failed` | startup | after external repair | close resources and exit |
| `state_path_insecure` | startup or desktop | no | component inactive |
| `local_state_unavailable` | desktop | after repair | no session or outbox mutation |
| `database_schema_unsupported` | startup | no | no file mutation; exit |
| `database_integrity_failed` | startup or runtime | after custodial repair | readiness false; no partial commit |
| `storage_unavailable` | hub | after repair | readiness false; transaction rolls back |
| `http_path_not_found` | HTTP | no | none |
| `http_method_not_allowed` | HTTP | no | none |
| `request_headers_too_large` | HTTP | no | none |
| `client_identity_claim_forbidden` | HTTP | no | none |
| `connection_limit_reached` | upgrade | yes | none |
| `request_rate_limited` | HTTP | yes | none |
| `message_too_large` | WebSocket | no | close; no parse or durable change |
| `message_rate_limited` | WebSocket | after reconnect | close; no durable change |
| `protocol_version_unsupported` | HTTP or WebSocket | no | none |
| `protocol_schema_invalid` | WebSocket | no | close; no durable change |
| `resume_required` | WebSocket | no | close |
| `resume_deadline_exceeded` | WebSocket | yes | close |
| `resume_context_incomplete` | resume | no | close |
| `resume_cursor_without_context` | resume | no | close |
| `cursor_ahead` | resume | no | close |
| `session_context_stale` | publish or clear | after reconnect | close; no durable change |
| `clear_generation_stale` | publish or clear | no for old content | none; client deletes old content |
| `clear_generation_ahead` | publish or clear | after reconnect | none |
| `clear_generation_exhausted` | clear or readiness | no | readiness false; no clear |
| `request_id_conflict` | clear | no | none |
| `message_id_conflict` | publish | no | none |
| `message_id_replay` | publish | no | none |
| `created_at_in_future` | publish | after clock repair | none |
| `event_too_old` | publish | no | none |
| `content_type_unsupported` | publish | no | none |
| `payload_empty` | publish | no | none |
| `payload_too_large` | publish | no | none |
| `payload_encoding_invalid` | publish | no | none |
| `payload_length_mismatch` | publish | no | none |
| `payload_hash_mismatch` | publish | no | none |
| `publish_rate_limited` | publish | yes | none |
| `hub_cursor_exhausted` | publish or readiness | no | readiness false |
| `history_cleared` | WebSocket | after reconnect | old-generation queue removed; close after notice |
| `ack_invalid` | WebSocket | no | close |
| `slow_consumer` | WebSocket | after reconnect | close |
| `heartbeat_timeout` | WebSocket | after reconnect | close |
| `adapter_unavailable` | desktop | after repair | agent inactive |
| `lock_state_unknown` | desktop | after repair | agent acts locked |
| `outbox_full` | desktop | after drain or clear | observation off; existing retry continues |

The version-1 wire and readiness code set is closed. An internal code can be
added only when a test proves it cannot cross a wire or health surface and
contains no forbidden diagnostic value.

HTTP status mapping is exact:

| Status | Code |
| --- | --- |
| 400 | `protocol_version_unsupported` |
| 403 | `client_identity_claim_forbidden` |
| 404 | `http_path_not_found` |
| 405 | `http_method_not_allowed` |
| 429 | `connection_limit_reached`, `request_rate_limited` |
| 431 | `request_headers_too_large` |
| 503 | `tailscale_localapi_unavailable`, `storage_unavailable`, `hub_cursor_exhausted`, `clear_generation_exhausted` |

WebSocket close mapping:

| Close | Reasons |
| --- | --- |
| 4400 | schema, version, message-size, resume-context, cursor, or ack failure |
| 4403 | `client_identity_claim_forbidden` |
| 4408 | resume deadline or heartbeat |
| 4409 | stale session, clear generation, or `history_cleared` |
| 4429 | slow consumer or message rate |
| 4500 | LocalAPI, storage, cursor, or clear-generation terminal failure |

### 18. Topology-neutral repository checks

CI scans the tracked tree, staged diff, and reachable Git history:

1. generic secret scanning rejects private keys, authorization headers, and
   credential-shaped assignments;
2. a source census rejects application-authentication middleware, application
   credential types, device-registry persistence, administrator routes,
   enrollment routes, pairing, credential lifecycle jobs, app TLS listeners,
   and a selectable memory-history mode;
3. examples contain no active listener, hub URL, Tailnet value, user home,
   inventory, or service-specific address;
4. network examples use only reserved documentation values or explicit
   placeholders;
5. fixtures use a documented synthetic UUID and stable-peer namespace;
6. deployment templates reference generic variables;
7. logs, snapshots, and error fixtures contain none of the content, identity,
   or topology canaries;
8. the root contains the MIT license and no contradictory project license;
9. when `CLIPMESH_PRIVATE_DENYLIST_FILE` names an external owner-only file,
   each nonblank literal is checked against tracked bytes, staged diff, and
   history. Failure prints the denylist line number and public path or commit,
   not the literal.

The check permits this specification to name removed concepts in authority and
non-goal prose. It rejects executable, schema, configuration, route, and
deployment surfaces that implement them.

### 19. Real-response fixture capture plan

Handwritten ideal responses do not prove an external seam.

Capture rules:

1. Use an isolated synthetic Tailnet test environment, synthetic clip text,
   reserved names, and synthetic IDs.
2. Keep raw captures outside the public repository in an owner-only path.
3. Record command, tool and OS version, scenario, PT time, exit status, and raw
   SHA-256 in an owner-only manifest.
4. Parse and structurally sanitize the response. Replace stable peer IDs,
   Tailnet addresses, node names, and user data with typed markers. Fail on an
   unknown identity-shaped or content-bearing field.
5. Commit the sanitized fixture, its SHA-256, and generic provenance with no
   private path, host, user, address, or raw identity-bearing hash.
6. Replay the fixture through the production parser. Also run the same
   assertion against a fresh unsanitized response in isolation.

Required captures:

| Seam | Real capture |
| --- | --- |
| Tailscale LocalAPI | status with self addresses; WhoIs success; peer not found; daemon unavailable; permission refusal; malformed response |
| Tailnet socket | allowed exact self bind; wildcard, loopback, LAN, public, and stale self-address refusal; non-Tailnet probe |
| WebSocket | upgrade, hello, resume, live publish, exact retry, replay rejection, clear, generation rejection, slow consumer |
| SQLite | initialize, publish, restart, expiry, count trim, shared clear, crash rollback, integrity refusal, unsupported-schema refusal |
| Wayland | real observation, explicit hint, remote write echo, lock transition, adapter failure |
| macOS | real bytes, declared types, change counts for local and remote writes, lock transition |
| iOS/iPadOS | foreground resume, live pasteboard overwrite, explicit row selection, background transition, shared clear |

The explicit-hint registry can add a signal only after its real capture proves
the operating system or source application marked that entry confidential or
transient. A source name, MIME name without documented semantics, payload
pattern, or timing observation cannot qualify.

### 20. Clause continuity for existing decomposition

The amendment preserves invariant and acceptance identifiers so prior work can
be reconciled without an unmarked renumbering. The meaning at this candidate
commit controls.

| Prior area | Current authority |
| --- | --- |
| I1, I5-I10, I14, I16-I18 | Identifier retained and tightened |
| I2 | LocalAPI WhoIs identity; no client source claim |
| I3 | Equal ACL-admitted member authority; no application authority classes |
| I4 | Tailnet-only plaintext application transport; no application TLS |
| I11 | Seven days or 500 clips by default |
| I12 | Equal-member shared clear with clear generation |
| I13 | SQLite only |
| I15 | Foreground live overwrite plus explicit mobile history |
| I19 | New canonical clip-content serialization seam |
| Architecture 2-8 | Replaced TLS, credential, control-plane, enrollment, and certificate surfaces with Tailnet transport and WhoIs |
| Architecture 12 | Replaced memory mode and administrator purge with persistent SQLite and shared clear |
| Architecture 15 | Removed contrary mobile live-write suppression |
| A01-A62 | Identifiers retained below; each Given/When/Then at this commit supersedes its prior text |

No decomposition can rely on a removed application identity, credential,
device, administration, enrollment, pairing, rotation, certificate,
memory-history, old retention, or administrator-only purge clause.

## Acceptance

The evidence column names the minimum proof. Each fixture that represents an
external response follows Architecture 19.

| ID | Traces to | Given / When / Then | Required evidence |
| --- | --- | --- | --- |
| A01 | I1, Architecture 2-5 | Given Rust and Swift version-1 implementations, when each decodes and re-encodes the canonical publish and sanitized capture corpus, then each field and exact UTF-8 content byte is preserved. | Cross-language conformance logs and fixtures |
| A02 | I1, I18 | Given one valid message, when one unknown field, duplicate key, wrong type, unsupported version, binary frame, invalid UTF-8 frame, or oversized frame is introduced separately, then the exact code and close apply and no durable state changes. | Table-driven negative matrix |
| A03 | I2, Architecture 6 | Given an admitted socket, when WhoIs returns stable peer ID P, then the session and accepted clip source use P without reading an application identity field. | LocalAPI capture, connection context assertion, database row |
| A04 | I3 | Given two distinct admitted stable peer IDs, when each resumes, publishes, acknowledges, and requests clear, then the same validation and mutation rules apply. | Complete equal-member operation matrix |
| A05 | I4, Architecture 2 | Given two Tailnet peers and the plaintext ClipMesh protocol, when one clip crosses the connection, then a hub application capture can recover the test text while a capture outside the WireGuard endpoints cannot. | Isolated Tailnet packet and application captures |
| A06 | I4, Architecture 8 | Given no bind value, a wildcard, loopback, LAN, public, documentation, link-local, multicast, hostname, or stale self address, when the hub starts, then it exits before an accept loop with the exact content-free code. | Startup matrix and socket probes |
| A07 | I4, Architecture 8 | Given one validated Tailnet self address whose port cannot bind, when startup runs, then it closes LocalAPI and SQLite resources and accepts no connection. | Real occupied-socket process test |
| A08 | I13, Architecture 8 and 12 | Given a symlink, wrong owner, or mode broader than the state-directory or database bound, when the hub starts, then it leaves the file unchanged and exits before bind. | Unix permission and before/after hash tests |
| A09 | I5 | Given 25 concurrent publishes from admitted peers, when clients read history and live delivery, then each observes one identical ascending cursor order with no reused cursor. | Concurrency log and SQLite query |
| A10 | Goal, normal delivery | Given normal delivery conditions, when one desktop observes 100 synthetic texts at 1,100 ms intervals, then each target write completes within 1,000 ms of source observation and no publish is rate-limited. | Timestamped real-adapter run |
| A11 | I6 | Given one retained accepted clip and rate buckets that admit ten retries, when its source retries exact input ten times, then each returns the original cursor with `duplicate = true`, history remains one row, and peers receive no second live event. | Hub, peer, and SQLite counters |
| A12 | I6, I12 | Given one accepted clip, when its source reuses the message ID with changed input, retries its tombstoned ID after expiry, or retries after clear, then the specified conflict, replay, or generation code returns and no hub state changes. | Replay matrix with database snapshots |
| A13 | I6, I17 | Given two concurrent publishes with one message ID, when the writer serializes them, then one commits and the other returns exact retry only when the full retry tuple matches or conflict otherwise. | Barrier test repeated 100 times |
| A14 | I7 | Given publishes accepted while resume output is blocked, when catch-up completes, then cursors through boundary B arrive as resume before `resume_complete`, and later cursors arrive live in order. | Deterministic subscriber barrier test |
| A15 | I7, I11 | Given a cursor behind `lost_through_cursor`, when the client resumes, then status is `gap`, retained successors arrive in order, and no guessed clip appears. | Age- and count-gap tests |
| A16 | I8 | Given a nonempty desktop clipboard and retained resume rows, when reconnect, unlock, or local resume catches up, then history and cursor change while the clipboard-write spy records zero calls. | Linux and macOS real-adapter tests |
| A17 | I8 | Given completed catch-up and an unlocked active desktop, when another peer publishes one live clip, then the platform write receives exact text once even if current clipboard bytes match. | Linux and macOS write-spy captures |
| A18 | I9 | Given a remote live write that produces duplicate watcher notifications, when the matching observation arrives, then no publish occurs; a later distinct observation publishes once without a timer. | Adapter event-sequence tests |
| A19 | I10, I17 | Given a local observation stopped at the state barrier, when lock or pause wins, then no content or outbox row exists; when outbox commit wins, the exact row follows normal retry and the transition adds no later write. | Deterministic client race test |
| A20 | I10, Architecture 14 | Given each captured registered confidential or transient signal and each unregistered, absent, ambiguous, source-name-only, or content-derived signal, when the adapter observes them separately, then only the registered signals suppress `ClipContentV1`; every other supported text entry maps to ordinary and follows normal state rules. | Real captures, ordinary-path assertions, and canary scan |
| A21 | I10, Architecture 13 | Given `local-only-next`, when two eligible local observations occur, then the first creates no content or outbox row and the second publishes once. | Local-control integration test |
| A22 | I11, I19 | Given default config and 262,144 UTF-8 bytes, when published, then the hub accepts them; 262,145 bytes returns `payload_too_large` without state change. | Boundary tests through the canonical seam |
| A23 | I11 | Given default config and 501 unexpired clips, when clip 501 commits, then SQLite contains cursors 2 through 501 and `lost_through_cursor` reaches at least cursor 1. | SQLite and resume test |
| A24 | I11 | Given a clip accepted at T, when hub time reaches T plus 604,800 seconds, then history omits it and oldest-first cleanup deletes its row within 60 seconds. | Controlled-clock SQLite test |
| A25 | I13 | Given retained SQLite clips, when the hub stops cleanly or crashes and restarts, then epoch, generation, cursor order, replay state, and unexpired content remain. | Real process restart and crash tests |
| A26 | I13, Architecture 8 | Given a new database, version 1 database, unsupported version, and nonempty zero-version database, when startup runs, then only the new database initializes, version 1 opens unchanged, and unsupported inputs remain byte-identical with `database_schema_unsupported`. | Migration matrix with file hashes |
| A27 | I12 | Given retained clips, queued old-generation frames, and generation G, when one admitted member clears, then one transaction deletes clips, commits G+1, updates lost-through, stores one receipt, drops queued old-generation event frames before release, and leaves each system clipboard unchanged. | SQLite, queue-writer, desktop, and mobile assertions |
| A28 | I2, Architecture 6 | Given WhoIs success, peer-not-found, timeout, permission refusal, malformed response, and empty stable ID, when sockets arrive, then only success reaches HTTP parsing and each failure closes with no application response. | Real LocalAPI admission matrix |
| A29 | I2, Architecture 2 and 7 | Given an admitted peer, when it supplies Authorization, forwarding, ClipMesh identity headers, URL user info, query, or fragment, then the hub returns `client_identity_claim_forbidden` and changes no state. | HTTP request matrix |
| A30 | I12, I17 | Given two distinct clear requests expecting generation G, when they race, then one commits G+1 and the other returns `clear_generation_stale`; no clip survives from G. | SQLite barrier test |
| A31 | I15 | Given 500 retained clips, when the mobile app enters foreground, then it catches up a descending age-and-preview history and performs no pasteboard write before `resume_complete`. | Swift state and pasteboard-spy test |
| A32 | I15 | Given a foreground mobile session after catch-up, when a new live remote clip arrives, then the app writes exact text once even when current pasteboard bytes match; resume, refresh, activation, background, and generation change each produce zero writes. | Swift transition matrix with real pasteboard |
| A33 | I14, Architecture 16 | Given unique clip, base64, hash, stable-peer, Tailnet-address, node-name, user-name, and platform-metadata canaries, when success and each failure class run, then logs, metrics, health, errors, and crash fixtures contain none. | Byte-for-byte output scan |
| A34 | I14, Architecture 16 | Given ready and not-ready admitted sessions, when health and readiness are queried, then status, body, and reason shape are exact and expose no count or identity. | Real HTTP captures |
| A35 | Architecture 8 and 9 | Given each configured connection, per-peer, rate, and outbound-queue boundary, when exceeded separately, then the named refusal or close occurs and admitted peers preserve cursor order. | Limit matrix |
| A36 | I16, Architecture 18 | Given clean tracked bytes and synthetic external denylist, when repository checks run, then clean bytes pass; one seeded secret, topology value, active listener, obsolete app-authority surface, or content canary fails without echoing the sensitive literal. | CI log and seeded-failure matrix |
| A37 | Goal, Architecture 1 and 8 | Given generic systemd, launchd, and Ansible assets, when rendered with reserved values, then native syntax checks pass and variables cover hub URL, Tailnet-only bind, state, retention, limits, and startup without an application identity secret. | Native syntax and rendered-fixture checks |
| A38 | Non-Goals, Architecture 1 | Given the repository root, when license checks run, then the canonical MIT license exists and no contradictory project license exists. | License scan |
| A39 | Architecture 19 | Given each external seam, when its tests merge, then evidence names a real capture, owner-only manifest, sanitizer, sanitized fixture, fresh-response run, and boundary scan. | Capture ledger and test logs |
| A40 | Goal, Non-Goals | Given the built dependency graph, routes, schemas, and config, when censused, then it contains no E2EE, app identity, credential, device registry, control plane, enrollment, pairing, rotation, application TLS, memory history, Share extension, direct delivery, non-text content, or public listener. | Dependency, route, schema, and config census |
| A41 | I2-I4 | Given a desktop already admitted by Tailnet policy, when generic deployment starts its agent with hub URL and a new local-state path only, then the hub's WhoIs result admits it and the client reaches live without an application account, credential, or onboarding state. | Isolated deployment-to-live run |
| A42 | I4, Architecture 8 | Given a hub bound to one validated Tailnet self address in an isolated network, when Tailnet, second-interface, loopback, and public-side probes run, then only the admitted Tailnet probe reaches HTTP. | Network-namespace and Tailnet probe log |
| A43 | Architecture 13 and 15 | Given nonempty product history and system clipboard, when desktop or mobile local clear runs, then only that client's visible history and processed cache clear; hub rows, generation, outbox, and system clipboard remain unchanged. | Client, hub, and platform before/after state |
| A44 | I3, I12 | Given two admitted peers, when either requests shared clear, then each can commit the same operation and neither can invoke an app-admin, device, or membership operation. | Operation and route matrix |
| A45 | I4, Architecture 8 | Given one valid hub or desktop config, when each required field is removed, unknown field added, URL scheme changed, and bound crossed separately, then startup fails before network activity with the exact code. | Generated config mutation matrix |
| A46 | I12, I17 | Given a publish and clear stopped at the common writer, when each ordering is released, then publish-before-clear is committed then deleted, and clear-before-publish causes the old-generation publish to write nothing. | Deterministic transaction test |
| A47 | I18, Architecture 17 | Given one trigger per stable code, when it fires, then surface, retryability, state diff, and emitted bytes match the table and contain no diagnostic canary. | Failure-code matrix |
| A48 | Architecture 13 | Given an active desktop with held outbound sends, when a new observation would exceed 128 events or 8,388,608 bytes, then it allocates no message ID, stores no new content, enters `outbox_full`, and preserves existing rows. | Persistent outbox boundary test |
| A49 | Architecture 10 and 12 | Given cursor or clear generation at unsigned-64 maximum, when the next corresponding mutation is attempted, then the counter does not wrap and the exact terminal code and readiness effect occur. | Injected counter-boundary tests |
| A50 | I2, I4, Architecture 9 | Given a ready hub and established sessions, when LocalAPI becomes unavailable, then readiness becomes false, no new socket reaches HTTP, and existing sessions close at the specified observable boundary without accepting a later mutation. | Real daemon-loss process test |
| A51 | I6, Architecture 13 | Given one unaccepted outbox row, when the desktop restarts with intact state, then it retries the exact message ID, generation, timestamp, and content; the next eligible observation receives a different message ID. | Restart and local-state inspection |
| A52 | I18, Architecture 8 and 13 | Given an absent desktop database, when the agent starts, then it initializes version 1 and can resume with null context; given an unsupported, corrupt, insecure, read-only, or non-atomic store, it emits `local_state_unavailable`, changes no store bytes, opens no session, and remains inactive until repaired. | Local-state initialization and failure matrix |
| A53 | I7, Architecture 5 and 9 | Given a 500-row resume followed by live clips, when a client processes the stream, then it sends one highest-cursor ack after `resume_complete`, later acks occur at most once per 2,000 ms, and the message bucket is not exhausted. | Controlled-clock trace |
| A54 | I12, Architecture 12 | Given one committed clear whose response was lost, when an admitted peer retries the same global request ID and generation, then it receives the committed generation with `duplicate = true`; changed input returns `request_id_conflict`. | Clear-receipt restart test |
| A55 | I12, I17 | Given a client with history, processed IDs, remote marker, pre-clear outbox rows, and nonempty clipboard, when it consumes `clear_notice`, then it deletes the named old-generation state and leaves its clipboard unchanged. | Desktop and mobile state snapshots |
| A56 | Architecture 13 | Given an unlocked desktop that is connecting, replaying, or disconnected, when its clipboard changes, then it allocates no message ID and creates no outbox row; reaching live does not queue that value without a later observation. | Deterministic connection-state test |
| A57 | I11, Architecture 10 | Given hub time T and retention R, when `created_at_ms` equals T+120000 or T-R, then the hub admits timestamp validation; T+120001 returns `created_at_in_future` and T-R-1 returns `event_too_old`. | Controlled-clock boundary table |
| A58 | I18, Architecture 7 and 17 | Given an admitted connection, when path, method, header size, identity header, and rate defects occur separately, then the exact HTTP status and code return in precedence order and no state changes. | Real HTTP precedence matrix |
| A59 | I18, Architecture 2 and 17 | Given a WebSocket session, when binary, invalid UTF-8, unknown schema, or oversize input arrives, then the exact error and close occur before durable mutation. | Real frame-boundary captures |
| A60 | I18, Architecture 3, 4, and 10 | Given one valid publish, when each version, UUID, decimal, timestamp, generation, content type, base64, UTF-8, size, length, and hash defect is introduced separately, then the exact precedence code returns and state remains byte-identical. | Ordered validation matrix |
| A61 | I19, Architecture 4 and 12 | Given one instrumented clip moving through platform ingress, wire ingress, SQLite, wire egress, preview egress, and platform output, when the run completes, then each content access crosses `ClipContentV1` and the final platform bytes equal the initial bytes. | Compile-time visibility test, seam trace, SQLite and platform captures |
| A62 | I8, I12, I15 | Given a foreground mobile client offline during clear with a nonempty pasteboard, when it reconnects, then generation catch-up clears product history without a pasteboard write; the first later live remote clip overwrites the pasteboard once. | Controlled-clock Swift and real pasteboard test |

### Acceptance execution order

1. Run schema, scalar, LocalAPI identity, and configuration tests.
2. Capture real external responses before accepting fixtures.
3. Run SQLite, publish, clear, resume, and concurrency tests against a real
   process and database.
4. Run Wayland, macOS, and mobile adapter tests on their named platforms.
5. Run content, identity, obsolete-surface, and topology scans over test output
   and tracked bytes.
6. Run the cross-platform normal-delivery test last.

A release claim records command, platform, tool versions, exact commit,
fixture provenance, pass and failure counts, and elapsed time. Compile-only or
mock-only evidence does not satisfy a real-response row.

## Open Questions

No blocking product question remains for the MVP.

The following questions are **NON-BLOCKING**:

1. **Explicit-hint registry entries.** Which Wayland and macOS signals have
   real evidence that the operating system or source application marks the
   entry confidential or transient? Architecture 14 defaults each
   unverified signal to ordinary.
2. **Linux lock-state provider.** Which supported session-lock API supplies
   the real event on the target Wayland test distribution? Unknown state acts
   locked.
3. **Local IPC implementation.** Should desktop control use an owner-only Unix
   socket or native per-user service IPC? Architecture 13 fixes commands,
   caller ownership, and effects. The choice cannot add a TCP listener.
4. **Future protocol work.** E2EE, a Share extension, additional clipboard
   types, direct delivery, another Tailnet authority policy, or another wire
   version requires a new reviewed specification.

Operating pattern taught to agents: none. This specification defines ClipMesh
behavior and does not amend Tightbeam operating guidance.
