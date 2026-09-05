# ClipMesh — Product Spirit v1

Status: product-owner derived after Mike's 2026-08-25 rulings. This document
authorizes technical specification and delivery orchestration. It does not by
itself authorize implementation, deployment, enrollment, or live mutation.

## Authority and provenance

- Canonical seed: ClipMesh `docs/initial-spirit.md` at commit
  `89c6579dc1ddc180ce22e954ecc39cc410eee887`, recorded as
  `art_3d431942`, SHA-256
  `60e59c7b7e200a6ce70114ebad34e420cf291e4d6c4e3493f1d3b297f3e85b9a`.
- Mike ruling `dr_735a0a42-f318-444d-8804-96dd8ccab1f7`: the MVP uses a
  trusted, hub-readable plaintext model because ClipMesh serves a private
  tailnet, with the documented application-layer safeguards.
- Mike ruling `dr_99071b43-5acc-4f2c-8c77-0a6b355b93b6`: the repository uses
  the MIT license.
- Mike's 2026-08-25 operator boundary: ask Mike only about money or scope that
  he has not agreed. The product owner derives product and MVP design from the
  agreed Spirit instead of escalating each enduring choice.

If this document conflicts with the canonical seed, the two Mike rulings and
the operator boundary above control. All other seed outcomes and constraints
remain in force.

## Spirit

### Problem

A person with several computers needs short-lived text to move between them as
easily as one clipboard. Existing choices add a cloud account, repeated
pairwise setup, a heavy desktop application, or misleading promises about iOS
background behavior.

ClipMesh serves a small personal fleet that already communicates over a secure
private overlay such as Tailscale. It keeps enrollment automatable and gives
each device its own revocable identity.

### Outcomes

1. A managed Linux or macOS desktop joins through private deployment automation
   without asking every existing device for approval.
2. Text copied on one online, unlocked desktop reaches the other online,
   unlocked desktops within one second under normal conditions.
3. An iPhone or iPad user opens the app, sees recent entries, selects one, and
   copies it into the system pasteboard.
4. Disconnects, reconnects, and repeated delivery do not create clipboard
   loops or duplicate history.
5. An administrator revokes one device without disturbing the remaining fleet.
6. Operators can understand health, connection state, suppression, and failure
   without logs, metrics, crash reports, or errors revealing clipboard text or
   credentials.
7. The public repository remains usable by any private deployment and reveals
   nothing about Mike's topology.

### Non-goals for the first usable release

- End-to-end or zero-knowledge payload encryption.
- Images, files, HTML, RTF, or arbitrary MIME replication.
- Public-internet discovery or operation without a private network.
- Accounts, billing, social sharing, or multi-tenant hosting.
- Reliable passive background clipboard monitoring on iOS or iPadOS.
- The iOS or iPadOS Share extension.
- Mutual TLS.
- Automatic hub election, failover, or direct device-to-device delivery.
- A full desktop clipboard-manager interface.
- Pairwise GUI enrollment between every machine.
- New cryptographic primitives.
- Erasure guarantees for an offline device or text already copied into an
  operating-system pasteboard.

### Quality stance

- **Correctness matters most.** Delivery order, deduplication, replay checks,
  expiry, and loop suppression must be deterministic.
- **Security and privacy matter most.** The private overlay is one layer, not
  the authorization model. ClipMesh minimizes collection, retention, exposure,
  and logging.
- **Interaction stays honest.** Desktops synchronize automatically while
  online and unlocked. Mobile actions remain explicit. Reconnect and unlock do
  not surprise the user with stale clipboard writes.
- **Normal delivery is fast.** Online desktop-to-desktop text reaches peers in
  roughly one second. ClipMesh does not trade security checks for lower
  latency.
- **Reliability is bounded.** The MVP supports one hub and a small fleet. It
  reconnects with bounded backoff and fails visibly, but it does not promise
  high availability.
- **Compatibility is deliberate.** The first desktop surfaces are Wayland
  Linux and macOS. The mobile surface is a foreground SwiftUI app for iOS and
  iPadOS.
- **Maintainability favors small native parts.** Rust owns the hub, protocol,
  and desktop agents where practical. Narrow native bridges are acceptable
  when safer than fragile foreign-function code.
- **Deployment stays flexible.** All topology belongs to private inventory or
  runtime configuration. Public defaults remain generic and fail closed.
- **Observability is content-free.** Health and ordinary logs expose state and
  reason codes, never payloads, credential material, or payload-derived text.

## Resolved product policy

### Trust and transport

The first release trusts the self-hosted hub to read plaintext payloads. Every
connection still uses TLS over the private overlay. The hub binds only to
configured private interfaces and has no public listener by default.

Each device receives one unique, high-entropy bearer credential. The hub binds
that credential to the device identity and supports individual rotation and
revocation. Mutual TLS remains outside the MVP because certificate issuance,
renewal, storage, and mobile enrollment add work without changing the agreed
hub trust boundary.

The wire protocol stays versioned and keeps payload representation explicit so
a later reviewed encryption design can replace plaintext. The MVP does not add
key distribution, recipient encryption, or speculative zero-knowledge
machinery.

### Device authority and enrollment

A private deployment administrator owns enrollment, revocation, rotation, and
global history purge. Ordinary device credentials carry data-plane authority
only. For the MVP, enrolled devices are equal data peers: they may read recent
history and publish plain text, but they may not enroll, revoke, rotate, or
administer another device.

Managed desktops receive credentials through Ansible or an equivalent private
secret-delivery mechanism. Mobile enrollment uses a short-lived, single-use
artifact issued by the administrator. No fleet-wide secret exists.

### History and retention

The hub uses bounded SQLite history by default because recent mobile history is
a core outcome and must survive an ordinary hub restart. A memory-only mode
remains an explicit privacy option.

The default limits are:

- four hours of retention;
- 20 history entries; and
- 256 KiB per entry.

Expiry, count, and item-size limits all apply. The first reached limit wins.
Deployments may reduce or increase the values through generic runtime
configuration, but no default permits indefinite retention.

### Sensitive content

When a platform exposes a recognized password-manager or sensitive-clipboard
hint, ClipMesh does not publish that entry. Diagnostics may record a
content-free suppression reason. ClipMesh does not claim to identify secrets
when a platform provides no reliable hint.

### Clear behavior

Every client may clear its local ClipMesh view or cache. Only administrator
authority may purge hub history and request cache clearing from online clients.
The operation does not claim to erase an offline client or text that a user
already copied into an operating-system pasteboard.

### Reconnect and unlock behavior

Reconnect and unlock never apply missed history automatically to the current
desktop clipboard. The agent uses cursors and message identifiers for resume,
deduplication, and ordering, then applies only new live events after the resume
boundary. A surface with an explicit history interface may still show retained
entries for user selection.

### Mobile scope

The MVP includes foreground history refresh, clear local history, safe preview,
and explicit pasteboard copy. The Share extension moves to the next milestone.
This is the smallest mobile surface that proves the core cross-device outcome.

### Hub placement and public topology neutrality

Private deployment inventory or runtime configuration designates one stable
hub. The public product does not elect or name it.

Source, defaults, examples, fixtures, tests, and documentation must not contain
real hostnames, usernames, tailnet names, IP addresses, filesystem layouts,
secrets, or private deployment boundaries. Generic placeholders must not
resemble actual private values. Private inventory and secret material stay
outside the public repository.

### License

The public repository uses the MIT license.

## MVP product shape

1. `clipmesh-hub`: a small Rust service with authenticated TLS connections,
   bounded SQLite or optional memory-only history, per-device revocation,
   content-free health endpoints, validation, replay rejection, and broadcast.
2. `clipmesh-agent`: a Rust Linux and macOS daemon that watches plain text,
   sends local changes, applies new live remote changes, suppresses loops,
   pauses while locked, and reconnects with bounded backoff.
3. `ClipMesh`: a foreground SwiftUI iOS and iPadOS app that displays bounded
   recent history and copies one selected entry into `UIPasteboard.general`.
4. Deployment assets: generic systemd and launchd templates plus
   Ansible-friendly variables for binaries, hub URL, device identity,
   credential material, retention, and startup behavior.

The product starts as hub-and-spoke. Direct delivery is a possible later
product, not an MVP abstraction requirement.

## Acceptance floor

The first release is acceptable only when all of these are true:

1. A newly provisioned managed desktop joins without interactive approval from
   every existing desktop.
2. Two online, unlocked desktops exchange ordinary text within one second under
   normal conditions.
3. An iPhone or iPad can fetch recent entries, copy one explicitly, and paste it
   into another app.
4. Reconnect, retry, and duplicate delivery create no echo loop or duplicate
   history.
5. Unlock or reconnect does not replace the local clipboard with a missed
   entry.
6. Revoking one device blocks its next authenticated connection and leaves
   other devices working.
7. Known sensitive-hint entries do not leave their source device.
8. Expiry, count, and item-size limits work together and remove data without
   payload disclosure in logs.
9. The hub is unreachable outside its configured private interface and exposes
   no public listener by default.
10. Repository scanning finds no private topology identifier, credential,
    payload-bearing diagnostic, or real deployment boundary in source,
    defaults, examples, fixtures, tests, or documentation.
11. The repository carries the MIT license.

## Delivery gate

This Spirit is the product authority that travels with every delivery handoff.
The technical specification must turn these outcomes and policies into exact,
testable behavior without inventing topology or expanding the MVP.

Implementation may begin only after the product owner completes the required
cold digest, confirms that this slice remains coherent, and dispatches it
through the ordinary spec-review-build-review cycle.
