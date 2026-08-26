# ClipMesh — Product Spirit v1

Status: product-policy amendment candidate for independent review. These bytes
authorize no implementation, integration, deployment, publication, release,
listener activation, enrollment, or live or private-state mutation.

Authority and provenance:

- Canonical seed: ClipMesh `docs/initial-spirit.md` at commit
  `89c6579dc1ddc180ce22e954ecc39cc410eee887`, artifact
  `art_3d431942`, SHA-256
  `60e59c7b7e200a6ce70114ebad34e420cf291e4d6c4e3493f1d3b297f3e85b9a`.
- Prior canonical Spirit: tightbeam-specs commit
  `472cfd261728bc88e9e655a9a9bf73ed94e9064e`, artifact
  `art_be61a318`.
- Mike's authoritative MVP update:
  `att_91cda21f-c8c0-4b5a-9ef0-5ac2473e46c1`.
- Product-owner policy derived from that update:
  `att_29c3a660-ee1a-4eb1-9f4c-7b5f177b6523`.
- Product-owner Spirit digest:
  `att_b4f90db5-0211-4c92-92a8-85bf14567af9`.
- Cold digest verdict:
  `att_c17096fc-7f34-4ef1-80dc-f5ceabee007a`.
- First amendment candidate `1ed56a8f699ee3332ca4e66d7ad5e97059ed2005`
  received a changes-requested verdict in
  `att_80f55013-33df-493a-a657-6259082c8961`, with report
  `art_40d4337a` at SHA-256
  `4891fe31b669ad3baa83eda895da98e4caec5b6460db4922f05c9d1fa03fb5fe`.
- Supplemental independent adjudication
  `att_abbcae70-8af7-4ea1-aa29-1e74a81674a4` added F7-F11 to the same
  open review. Replacement candidate
  `605026eaf8c1a270a340fe2b3f52a8628a42446d` then received a
  changes-requested verdict in
  `att_a532f8db-5bb9-4d77-bde3-2faf5cb13294`, with report
  `art_f813646f` at SHA-256
  `3f4eb8dfd8d245843f56cda4552ce7ef0dfe74e2478e01361da1ffeecc736c5e`.
  That verdict closed F1-F6 and retained F7-F11. This revision resolves the
  five remaining findings.
- Mike's earlier rulings remain settled: the MVP trusts a hub that can read
  plaintext, and the public repository uses the MIT license.

The Mike update and product-owner policy above supersede prior Spirit clauses
about application credentials, device administration, enrollment, separate
TLS identity, memory history, four-hour or 20-entry defaults,
administrator-only purge, and mobile live-write suppression.

## Goal

Give one person one text clipboard across devices admitted to the same
Tailnet. A copied text value moves through one trusted self-hosted hub, appears
in persistent shared history, and becomes the current clipboard on online
clients when it is a new live remote clip.

The first release contains a Rust hub, Rust Wayland Linux and macOS agents, a
foreground SwiftUI iOS and iPadOS client, and generic deployment assets. It
keeps the product small enough to inspect, test, self-host, and release under
the MIT license.

## Non-Goals

- End-to-end or zero-knowledge payload encryption.
- An application account, pool key, bearer credential, device registry,
  administrator role, enrollment flow, pairing flow, credential rotation,
  credential expiry, or recurring re-onboarding.
- A separate application TLS certificate identity, mutual TLS identity, or
  certificate handoff ceremony.
- Images, files, HTML, RTF, or another clipboard MIME type.
- Public-Internet discovery or a public listener.
- Multi-tenant hosting, billing, social sharing, or fleet administration.
- Passive background clipboard monitoring on iOS or iPadOS.
- An iOS or iPadOS Share extension.
- A memory-only hub-history mode.
- Automatic hub election, failover, or direct device-to-device delivery.
- A full desktop clipboard-manager interface.
- Content-based secret detection.
- Erasure guarantees for an offline client, a system clipboard, a storage
  snapshot, or storage hardware.
- A private hostname, Tailnet name, address, username, filesystem layout,
  inventory boundary, or deployment target in the public repository.

## Terms

- **Tailnet:** The deployment's Tailscale network. WireGuard within Tailscale
  encrypts traffic between Tailnet peers.
- **ACL-admitted member:** A Tailnet peer whose connection the deployment's
  Tailnet policy admits to the ClipMesh hub service.
- **Local Tailscale boundary:** The trusted Tailscale component on the hub host
  that accepts a Tailnet connection and asserts the authenticated peer
  identity to the hub through a local, non-network handoff.
- **Tailnet peer identity:** The immutable identity asserted by the local
  Tailscale boundary for one accepted connection. It is not a field supplied
  by a ClipMesh client.
- **Trusted plaintext hub:** The self-hosted ClipMesh service that can read
  clipboard text while it validates, orders, stores, and distributes it.
- **ClipMesh history:** The hub's retained SQLite clip rows and the product
  history projected from those rows. A system clipboard is not history.
- **Resume material:** Retained clips sent during catch-up through the
  session's captured resume boundary.
- **Live remote clip:** A clip from another Tailnet peer that the hub accepts
  after the receiving session's resume boundary.
- **Clear generation:** The durable, increasing hub value that distinguishes
  clips and queued publishes created before and after a shared clear.
- **Shared clear:** An equal-member request that atomically removes retained
  clips and advances the clear generation.
- **Explicit confidential or transient hint:** A signal supplied by the
  operating system or source application that directly marks one clipboard
  entry confidential or transient.
- **Canonical clip-content serialization seam:** The single implementation
  boundary that turns text into the stored and transmitted representation and
  turns that representation back into text.

## Assumptions

1. The deployment provides one stable hub reachable only through its Tailnet.
2. The local Tailscale boundary can assert authenticated peer identity for
   each connection it hands to the hub.
3. Tailnet policy controls which peers can reach the hub. ClipMesh does not
   create a second membership system.
4. The deployment owner accepts a trusted hub that can read clipboard text.
5. Tailnet WireGuard protects network transit. FileVault, LUKS, or the mobile
   platform's protected storage protects endpoint history at rest.
6. Linux MVP hosts provide a supported Wayland clipboard and lock-state
   surface. macOS provides native pasteboard and lock-state surfaces.
7. iOS and iPadOS permit a foreground network session and pasteboard writes.
8. The release process can run Rust, Swift, SQLite, platform-adapter, network
   confinement, and repository-boundary checks on their real targets.

## Invariants

### S1 — The hub trust decision is explicit

The hub reads plaintext clip content. ClipMesh makes no end-to-end encryption
claim. Tailnet WireGuard protects transit between Tailnet peers.

### S2 — Tailnet admission is the membership boundary

The hub accepts a session only when the trusted local Tailscale boundary
asserts its peer identity. The hub ignores and rejects client-supplied identity
claims. Each ACL-admitted member has the same publish, history, and shared-clear
authority.

### S3 — The service fails closed to Tailnet-only reachability

The hub has no listener default. It binds only through an explicit generic
Tailnet-only configuration whose validation fails before service when the
local Tailscale boundary or confinement cannot be proved. The public product
contains no public listener or private topology value.

### S4 — History is persistent and bounded

The hub uses SQLite. The default retained window is seven days or 500 clips,
with oldest clips removed first when either limit applies. Deployments can
configure both limits through generic bounded settings.

### S5 — Shared clear is one generation change

An ACL-admitted member can request shared clear. The hub deletes retained
clips and advances the clear generation in one transaction. A client or hub
rejects queued or replayed content from an earlier generation. Shared clear
does not change a system clipboard.

### S6 — Resume and live behavior are distinct

Resume material updates ClipMesh history and cursor state. It does not write a
desktop or mobile system clipboard. After catch-up completes, each new live
remote clip directly overwrites the current system clipboard on an eligible
desktop and on a foreground mobile client.

### S7 — Sensitive-content suppression requires an explicit source hint

ClipMesh classifies and suppresses an entry as sensitive only when the
operating system or source application explicitly marks it confidential or
transient. ClipMesh uses no payload, pattern, source-name, or timing heuristic
to classify content. Lock, local pause, local-only control, validation, and
loop suppression remain separate observable state rules.

### S8 — One serialization seam owns clip content

Ingress, SQLite storage, and egress use the canonical clip-content
serialization seam. Protocol, storage, logging, and platform code do not create
another content encoding path.

### S9 — Ordering, replay resistance, and loop suppression are deterministic

The hub assigns one total cursor order. Exact retry is idempotent. Conflicting
or tombstoned message-ID reuse changes no state. Clients suppress self-delivery
and remote-write echoes from observable identifiers and state, not
elapsed-time guesses.

### S10 — Diagnostics are content-free

Logs, metrics, health, errors, and crash fixtures cannot represent clip bytes,
previews, content hashes, client-supplied identity claims, Tailnet identity
material, or payload-derived strings.

### S11 — Mobile history remains explicit

The foreground mobile client shows retained history and lets the user select
an older row to copy. That explicit history action coexists with S6's direct
write for a new live remote clip.

### S12 — Public bytes stay topology-neutral

Source, defaults, examples, fixtures, tests, documentation, and deployment
templates contain only reserved examples or placeholders. Private inventory
and Tailnet policy remain outside the public repository.

### S13 — The MVP remains text-only and MIT licensed

Version 1 carries nonempty UTF-8 `text/plain` only. The repository root
carries the MIT license.

### S14 — Held actions remain held

This Spirit does not elect an integration or release target. It does not
authorize implementation, product-code edits, deployment, publication,
listener activation, enrollment, or live or private-state mutation.

## Architecture

### Product shape

1. `clipmesh-hub` is a Rust service behind a trusted local Tailscale
   connection boundary. It validates asserted Tailnet peer identity, stores
   bounded SQLite history, orders clips, rejects replay, performs shared clear,
   and broadcasts clips.
2. `clipmesh-agent` is a Rust Wayland Linux and macOS daemon. It observes
   eligible local text, publishes while live, applies live remote text,
   suppresses loops, pauses while locked, and resumes without a clipboard
   write.
3. `ClipMesh` is a foreground SwiftUI iOS and iPadOS client. It catches up
   history without a pasteboard write, applies a new live remote clip while
   foreground, and lets the user select a retained row explicitly.
4. Deployment assets expose generic variables for the hub endpoint,
   Tailnet-only confinement, state storage, retention, limits, and startup
   behavior. They contain no application credential or device-enrollment
   surface.

### Trust and authority

The trusted hub and local `tailscaled` daemon are separate components. For
each accepted socket, the hub performs the stable LocalAPI WhoIs operation
documented by `local.Client.WhoIs` with the socket's observed remote
address and uses only the returned node stable ID. A ClipMesh request cannot
choose, override, or supplement its peer identity.

Tailnet policy owns reachability. ClipMesh has no application administrator or
device-control plane. Operational control of the hub process, host, Tailnet
policy, configuration, and backups remains local deployment administration,
outside the ClipMesh wire protocol.

### History, clear, and live delivery

SQLite is the only hub history mode. The hub keeps the newest clips within
both configured retention age and count. A shared clear creates one durable
generation boundary. Each publish binds to the generation observed by its
session, so content queued before clear cannot reappear after clear.

Catch-up fills product history only. The hub marks the boundary before it sends
resume material, then marks later clips live. An eligible client writes only a
new live remote clip after catch-up. Desktop eligibility requires an unlocked,
active agent. Mobile eligibility requires the app to be foreground.

### Content boundary and privacy

One canonical seam encodes and decodes clip content for network ingress,
SQLite storage, network egress, and platform delivery. This seam exists
because deleting it would leave multiple encodings that a later reviewed
content-protection change could not replace locally. Accepting multiple
encodings would make byte fidelity and canary coverage undecidable.

Shared clear needs a durable generation because deleting that mechanism would
allow an offline or queued pre-clear clip to restore cleared history.
Accepting that failure would contradict the user-visible meaning of clear.

### Topology and delivery hold

The public product names no Tailnet, host, address, user, path, or deployment
boundary. Private deployment configuration selects the hub and Tailnet
confinement. The hub-and-spoke shape does not assume where the hub runs.

Implementation can start only after an independent reviewer clears the exact
Spirit and technical-spec commit and the product owner accepts that reviewed
candidate. Integration, deployment, publication, listener activation, and
release require their own later authority.

## Acceptance

| ID | Given / When / Then |
| --- | --- |
| S-A01 | Given a connection admitted by Tailnet policy and handed over by the local Tailscale boundary, when the hub opens a ClipMesh session, then it uses only the boundary-asserted peer identity. |
| S-A02 | Given a request that asserts a different peer identity in application data, when the hub validates it, then the hub rejects the request and changes no state. |
| S-A03 | Given default configuration or a configuration that cannot prove Tailnet-only confinement, when the hub starts, then it accepts no connection and exits with a content-free failure. |
| S-A04 | Given two ACL-admitted members, when either publishes, reads history, or requests shared clear, then the hub applies the same authority rules to both. |
| S-A05 | Given default retention and 501 unexpired clips, when clip 501 commits, then SQLite retains the newest 500 clips. |
| S-A06 | Given default retention and a clip that reaches seven days of age, when history is queried, then the query omits that clip and oldest-first cleanup removes its row. |
| S-A07 | Given retained clips and a current clear generation, when one admitted member requests shared clear, then one transaction deletes retained clips and advances the generation. |
| S-A08 | Given an offline or queued publish from before shared clear, when it reaches the hub after clear, then the hub rejects it and it does not enter history or a system clipboard. |
| S-A09 | Given a nonempty desktop or mobile clipboard and retained resume material, when catch-up runs, then product history fills and the system clipboard remains unchanged. |
| S-A10 | Given catch-up is complete, when another member publishes a new live remote clip, then an unlocked active desktop and a foreground mobile client each write the exact text once. |
| S-A11 | Given a clipboard entry with no explicit confidential or transient hint, when the client observes supported text, then it does not suppress the entry because of its bytes, pattern, source name, or timing. |
| S-A12 | Given an explicit confidential or transient hint, when the client observes the entry, then no clip content enters its outbox, the wire, history, or diagnostics. |
| S-A13 | Given one clip crossing ingress, SQLite, and egress, when seam instrumentation runs, then each content transformation uses the canonical serialization seam and the delivered UTF-8 bytes equal the source bytes. |
| S-A14 | Given overlapping remote writes, duplicate watcher notifications, duplicate delivery, exact retry, replay attempt, or concurrent publish, when the state machines process them, then cursor order stays total, each remote-write echo stays suppressed, a later eligible local write of the same bytes publishes, exact retry creates no duplicate, replay changes no state, and no clipboard loop forms. |
| S-A15 | Given repository and diagnostic canaries, when boundary scans run, then they find no clip content, content hash, private topology value, application credential surface, or non-MIT project license. |

## Open Questions

No blocking product question remains for this MVP.

The following questions are **NON-BLOCKING**:

1. Which captured Wayland and macOS signals qualify as explicit confidential
   or transient hints? Until a signal has a real capture and test, the adapter
   treats it as an ordinary supported text entry.
2. Which supported Linux lock-state API supplies the real lock event? Unknown
   or unavailable lock state remains locked.
3. Future E2EE, a Share extension, new clipboard types, direct delivery, or
   another protocol version each requires a new reviewed product decision.

Operating pattern taught to agents: none. This Spirit defines ClipMesh product
behavior and does not amend Tightbeam operating guidance.
