# Surf Ace fleet-wide window-label allocator

Status: implementation-ready specification, before build. Revision r4.

Normative inputs, pinned by content:
- Requirement (settled ruling): `tightbeam-specs`
  `surf-ace-fleet-unique-window-labels.md` at commit
  `bdd9604064006929e463549438f82eb6da31de92`.
- Core invariant and existing wire protocol: Surf Ace `DESIGN.md` at commit
  `edc747dc26146c8b0ec548e9ceec20c40c449bc7`.
- Pre-build architecture and acceptance contract: design artifact
  `art_95dc7ed5`, file
  `surf-ace-fleet-window-label-allocator-design.md`, SHA-256
  `9a8dfccbdbefc14a748467c782657c13cafd6d059435812c1b96760d45eef998`.

This spec turns those three inputs into buildable requirements. Where a value
below is a design ruling from a pinned input, this spec restates it as a
requirement and does not re-decide it. Where this spec adds detail the inputs
left to the builder, it says so and keeps the detail inside the design's stated
safety property (one configured endpoint, one durable single writer, no
provisional label).

**Revision r4 closes R3-01 through R3-06 from adversarial review
`art_55b97955` (SHA-256
`f92db50971c0e15cce20f299f284a15a07ab0edd73c232e983fc4f64b2e8ae5b`). The
per-finding disposition is in "Review response (r4)" at the end. r4 supersedes
r3 (SHA-256 `d6d4b9475c62e36129946c38231dd54765600267638a87cb5057c36d50b4a496`),
r2 (SHA-256 `137e0e85a5482387a05f06f9e28df34025837484ee4e8e117131435d80584a90`),
and r1 (SHA-256
`421f7cb5b29d8c675456aa4ad9d9d922bd6e2cb26ab50e4e682d98e1c1503c7a`).
Those prior bytes remain immutable in git history and their recorded artifact
paths. This digest-specific file is the sole r4 review target.**

---

## Goal

Give the Surf Ace fleet exactly one authority that assigns window labels, so
that every live surface across every client shows a window label that no other
live surface in the fleet shows, and a user or OpenClaw can say "move content to
window b" and reach exactly one window. A client that cannot obtain an
authoritative label shows no window label and is not addressable, rather than
show a label that might be wrong.

This restores the invariant that one OpenClaw provider process held implicitly
before the CLI rewrite removed it (requirement doc, "How it was lost").

---

## Non-Goals

- G-N1. Client-led leader election. v1 uses one configured coordinator and no
  election (design artifact, "Decision" and "Non-goals").
- G-N2. A fallback or secondary allocator. v1 has one writer and no failover
  (design artifact, "Decision").
- G-N3. Multi-writer replication of allocator state.
- G-N4. Label reuse. A retired or closed surface does not free its label in v1
  (design artifact, "Persistence and recovery" and "Migration").
- G-N5. Host-qualified labels (`shrdlu b1`), random labels, provisional labels,
  or optimistic local labels. All are forbidden, not merely out of scope
  (requirement doc, "Rejected alternatives"; core invariant consequences). The
  client authority identity refined in r4 (Terms, `authorityId`) is an internal
  allocation key, never a visible label component; it does not host-qualify or
  otherwise alter the plain alphabetic user-visible label.
- G-N6. Moving pane-label allocation into this service. Pane labels stay
  client-local and lowest-free (design artifact, "Pane labels"). r4 retains
  a bounded correction to the iOS pane allocator so it is lowest-free like
  Electron (INV-11, REQ-G1); this is a defect fix against the settled ruling,
  not a move of pane allocation into the allocator.
- G-N7. Changing `surfaceId`, pane identity, content, history, topology
  revisions, or targeting rules. This work changes only how a window label is
  obtained, validated, and displayed, plus the bounded iOS pane-lowest-free
  correction named in G-N6.
- G-N8. A new transport. The allocator reuses the WebSocket/JSON envelope
  conventions already defined in `DESIGN.md` §5; it does not add REST or binary
  frames.
- G-N9. WSS/TLS for the allocator link in v1. It runs on the configured fleet
  network (the current deployment uses Tailscale), consistent with the v1 `ws`
  scheme in `DESIGN.md` §3.
- G-N10. Cryptographic authentication of claims, forgery/replay/timing
  defenses, or any hardening beyond the one-operator trusted-tailnet threat
  model. The `authorityId` is a distinguishing key, not a credential; the
  allocator does not authenticate it. Adding such hardening is a separate
  operator decision, out of v1 scope (see OQ-3).
- G-N11. Gap-free labels after a persistence failure. A reserved ordinal whose
  mapping cannot be committed is burned. Safety forbids reclaiming it; the next
  successful label may skip a letter.

---

## Terms

Each load-bearing term, what it denotes, and where it lives.

- **Fleet** — the set of Surf Ace surface clients (Electron and iOS) that a
  single user addresses as one namespace. All of them share one window-label
  space.
- **Fleet coordinator** — the one explicitly configured, always-on host that
  runs the window-label allocator process. The current deployment candidate is
  the host that runs the OpenClaw gateway (design artifact, "Decision"); OQ-5
  requires the operator to name the exact host before deployment.
- **Window-label allocator** (the **allocator**) — the single resident process
  on the fleet coordinator that owns the window-label space for the fleet. It is
  a WebSocket server. It is the only writer of window labels.
- **Fleet configuration identity** (`fleetId`) — a single value shared by the
  allocator and every client of one fleet, set by operator configuration. It
  names *which fleet* an endpoint and a client belong to. A client rejects any
  allocator whose configured `fleetId` does not match its own. Distinct from
  `allocatorId`: `fleetId` is configured up front and stable across allocator
  re-initialization; `allocatorId` is minted per initialized allocator state and
  changes when a new fleet state is initialized.
  Format: 1–128 characters from `[A-Za-z0-9._:-]`.
- **Allocator identity** (`allocatorId`) — a stable identifier minted once when a
  fleet's allocator state is first initialized, carried in every response and in
  every client provenance record. It names *which allocator state generation*
  issued a label. Format: `alloc_` followed by 3–64 characters from
  `[A-Za-z0-9._:-]`.
- **State-format version** (`stateVersion`) — the integer schema version of the
  allocator's persisted state, present in state and in responses.
- **Authority owner anchor** (`ownerAnchorId`) — the stable fingerprint of a
  per-authority, per-installation non-exportable key that the client profile,
  ordinary app-state backup, and device migration do not carry. The secure-store
  record belongs to one installation-owned authority slot; copied profile bytes
  cannot name, copy, or reproduce that slot. Two authority instances in one app
  installation use different slots and keys. Electron uses the platform secure
  store outside the copyable profile; iOS uses a non-synchronizable
  `ThisDeviceOnly` Keychain key. A client derives the fingerprint only from that
  local key; it never accepts the value from copied profile state. This is an
  ordinary clone discriminator in the trusted-client model, not a wire
  authenticator (G-N10). Format:
  `owner_` followed by 22–64 characters from `[A-Za-z0-9._:-]`.
- **Client authority identity** (`authorityId`) — a durable identifier for one
  client's surface authority (the Electron `lockless-client-authority` or the
  iOS `SurfAceLocklessAuthority` instance). Format: `auth_` followed by 22–64
  characters from `[A-Za-z0-9._:-]`. The allocator binds each `authorityId` to
  exactly one `ownerAnchorId` before accepting claims. A copied profile on a new
  installation has a different anchor and must rekey to a new `authorityId`
  before any copied label is authoritative. The identifier is an internal
  allocation key only; it is never displayed or included in a window label.
- **Fleet surface key** — the pair `(authorityId, surfaceId)` after the allocator
  has confirmed the authority-owner binding. This is the fleet-unique immutable
  key of an assignment. An unbound or ownership-conflicted pair is not a fleet
  surface key and cannot receive or display a label.
- **Label ordinal** (`ordinal`) — a non-negative integer. The allocator assigns
  ordinals in strictly increasing order and maps each to a window label:
  `0 -> a`, `1 -> b`, … `25 -> z`, `26 -> aa`, `27 -> ab`, … (bijective base-26
  over `a`–`z`, matching `DESIGN.md` §3.1.1 and §15.1).
- **Window label** (`windowLabel`) — the short alphabetic user-visible addressing
  handle for a surface window, as defined in `DESIGN.md` §2a and §15.1. Stored
  lowercase; rendered uppercase inside the identity overlay per §15.1. Distinct
  from `surfaceId` and from `authorityId`.
- **`surfaceId`** — the client-assigned surface identity, `sf_` followed by 3–64
  characters from `[A-Za-z0-9._:-]` (`DESIGN.md` §6.0 / §10 `SurfaceId`). It is
  stable within one client authority but **not** fleet-unique (A-6). It is one
  half of the fleet surface key and never changes here.
- **Assignment** — the allocator's durable, immutable mapping
  `(authorityId, surfaceId) -> { ordinal, windowLabel }` under a given
  `allocatorId`.
- **Claim** — the idempotent client-to-allocator operation that returns the
  assignment for a fleet surface key, creating it on first request.
- **Next-ordinal fence** (`nextOrdinalFence`) — the lowest ordinal that the
  custody store has never reserved. It starts at 0 and only increases. Reserving
  ordinal `n` atomically changes it from `n` to `n + 1`; the reservation is
  never rolled back, even if the later mapping commit fails. Thus every ordinal
  below it has a durable `reserved`, `committed`, or `burned` transaction and can
  never be reserved again. Recovery completes a `reserved` transaction under
  D3. This replaces r3's contradictory `highWater` name and meaning.
- **Fleet custody store** — the separately located, linearizable durable store
  named by `fleetId`. It owns the next-ordinal fence, authority-owner bindings,
  transaction outcomes, and the exclusive fenced writer session. It provides
  compare-and-swap transactions and rejects every mutation carrying a stale
  writer token. Local allocator files are recoverable snapshots/caches, not an
  independent authority. Copying them to another path or host cannot create a
  second writer.
- **Writer token** — an opaque monotonically fenced token returned by the
  custody store to the one exclusive writer session. Every reservation, binding,
  and mapping commit includes it. The store rejects a stale token even if its
  former process remains alive after a partition.
- **Allocator provenance** — the record a client persists per surface proving a
  window label was durably issued by the configured allocator:
  `{ fleetId, allocatorId, stateVersion, authorityId, ownerAnchorId, surfaceId, ordinal,
  windowLabel, committed: true }`. The `committed: true` field records that the
  client observed a durably committed success (REQ-C2) before persisting; a
  record without it is not proof of a durable issue. A bare `windowLabel`
  without matching provenance, provenance whose `allocatorId` does not equal the
  configured allocator identity, or provenance whose `fleetId` does not equal
  the configured fleet identity, is a **legacy label** and is never
  authoritative.
- **Configured allocator identity** — the `allocatorId` a client is configured
  or has durably learned to trust for this fleet. It is the value every
  provenance check compares against, and it must be available to the client
  offline (from configuration or persisted prior learning, not only learned at
  runtime) so that an allocator re-initialized under a new identity is detectable
  without a live round-trip. See INV-9 for how a client without a configured
  identity behaves (fail closed).
- **Legacy label** — a `windowLabel` persisted by a pre-upgrade, client-local
  allocator, carrying no allocator provenance (or provenance for another fleet
  or allocator). Not authoritative; ignored as authority (design artifact,
  "Migration").
- **Addressable / unaddressable surface** — a surface is *addressable* when it
  holds a valid allocator assignment (fresh, or persisted with provenance for
  the configured fleet and allocator identity) and is exposed in the addressable
  live projection. It is *unaddressable* otherwise: it shows no window label and
  cannot be targeted by label (see the operation matrix in D-C).
- **Pane label** (`paneLabel`) — the lowest free positive integer within one
  window, client-local (`DESIGN.md` §3.1.1 pane rules, §15.1). The user-facing
  pane token is `windowLabel + paneLabel`. r4 retains iOS pane allocation as
  lowest-free like Electron (INV-11).
- **Allocation transaction** — the two-stage custody-store transaction for one
  new assignment: reserve one ordinal under a unique `transactionId`, then
  commit the mapping under the same id. The custody store records each stage
  durably and idempotently. Its reserve and mapping operations each have one
  linearization point and return committed, clearly-not-committed, or unknown.
  Recovery queries the transaction id; it never infers an outcome from a local
  file or timeout.

---

## Assumptions

Indicative givens this spec relies on. If one is false, raise it before building.

- A-1. Exactly one always-on host can be designated the fleet coordinator, and
  it can run a resident process reachable by every client. (Design artifact
  states this as the chosen shape.)
- A-2. Every client can reach the coordinator over the configured fleet network
  at one WebSocket URL.
- A-3. The deployment can provide one fleet custody store with linearizable
  compare-and-swap, durable idempotency by transaction id, and exclusive fenced
  writer sessions, including one atomic fence-increment/journal-append mutation.
  Backend selection and its URL are deployment inputs (OQ-5);
  an implementation that cannot prove these semantics cannot serve labels.
- A-4. Clients already persist per-surface state and per-authority state across
  restarts and can extend those records with a durable `authorityId` and with
  allocator provenance without changing `surfaceId`.
- A-5. The WebSocket/JSON envelope conventions of `DESIGN.md` §5 (request /
  response / correlation `id` / `sentAt` / idempotent replay) are available to
  reuse for a new server op.
- A-6. **`surfaceId` is NOT fleet-unique.** It is stable and unique only within
  one client authority. iOS mints `surfaceId` from a client-local counter
  (`packages/ios/SurfAce/SurfAceLocklessTopologyOperations.swift` `allocateSurfaceId`
  formatting `sf_%016llx`, with `SurfAceLocklessAuthority.swift` initializing
  `nextSurfaceId` to 1), so two fresh iOS authorities both mint
  `sf_0000000000000001`; Electron mints 12 hex from a random UUID
  (`packages/electron/src/surface-core.ts`), which is only probabilistically
  unique. Therefore the fleet-unique key is the fleet surface key
  `(authorityId, surfaceId)`, not `surfaceId` alone. (This assumption replaces
  the r1/r2 assumption that `surfaceId` was globally unique, which the review
  disproved.)
- A-7. v1 fleet size and label churn are small enough that a single writer with
  a durable commit per claim is adequate; no batching is required for
  correctness. (Design artifact chose the single-writer sidecar shape.)
- A-8. Electron and iOS can persist the authority owner anchor in
  installation-local OS secure storage excluded from the copy/restore paths
  named in Terms. If either platform cannot supply that storage, its surfaces
  stay unaddressable; copied profile bytes alone never establish ownership.

---

## Invariants

Normative. Every implementation MUST satisfy every invariant. Invariants come
first because a failure of any one reintroduces the exact defect this work
exists to remove.

- INV-1. **One allocator fleet-wide, enforced structurally.** At most one
  process holds the fleet custody store's current writer token. The custody
  store, not a path-local lock, rejects every stale-token mutation. A host-local
  lock keyed only by `fleetId` also excludes a second path on the designated
  host. A process without both locks fails closed before it listens. Copied state
  bytes, a second path, or a second host cannot become a writer. Clients hold one
  fleet-wide configured endpoint, `fleetId`, and configured/learned
  `allocatorId`. There is no client election, allocator election, or fallback.
- INV-2. **Fleet-unique window labels.** No two distinct fleet surface keys
  under one `allocatorId` ever hold the same `windowLabel`, and no two live
  surfaces across the fleet ever display the same window label. (Core invariant;
  requirement "The requirement".)
- INV-3. **Monotonic, no reuse, fenced across restore.** The allocator issues
  ordinals by reserving from `nextOrdinalFence` (INV-13). An ordinal below the
  fence is reserved, committed, or burned and is never reserved again across a
  clear failure, unknown outcome, restart, corruption recovery, surface close,
  or restore. Only a committed transaction produces an assignment or success.
- INV-4. **Immutable assignment.** Once committed, an assignment
  `(authorityId, surfaceId) -> { ordinal, windowLabel }` never changes. A repeat
  claim or re-confirm for the same fleet surface key returns that assignment.
  Restoring an old snapshot may temporarily omit it from the inactive restore
  generation; journal replay reconstructs the identical proven assignment
  before that generation becomes accepted. Re-confirm returns that assignment
  or a conflict. It never imports client-supplied authority and never relabels
  that key.
- INV-5. **Durable-before-reply, with an explicit unknown outcome.** The
  allocator commits a mapping in the fleet custody store before it sends success.
  Each reserve and mapping stage has exactly three outcomes: committed,
  clearly-not-committed, or unknown. A committed reservation is not rolled back;
  a later clear mapping failure burns the ordinal. An unknown stage makes the
  allocator fail closed until it resolves that exact `transactionId`. A crash
  after mapping commit and before reply loses no assignment because a repeat
  claim returns the committed mapping.
- INV-6. **Fail closed.** An initialized allocator whose state is missing,
  unreadable, corrupt, of an unsupported `stateVersion`, internally
  inconsistent, in the unknown-persistence state, unable to reach or validate
  custody, or unable to acquire both writer locks MUST refuse claims and MUST NOT
  silently start a sequence. It requires transaction recovery, a verified
  same-identity restore, or explicit new-fleet initialization: an unknown
  transaction follows D3/D7; lost or inconsistent initialized custody follows
  I3; and only custody that has never been initialized follows I1.
- INV-7. **No label without authority.** A client displays a window label for a
  surface only when that surface holds a valid allocator assignment: a fresh
  committed claim from the configured allocator, or a persisted assignment whose
  provenance `fleetId` and `allocatorId` match the configured fleet and
  allocator. A client MUST NOT mint, retain as authoritative, or display a
  legacy, provisional, host-qualified, random, or client-local window label.
  (Requirement "What must be built" 2; core invariant consequences; design
  artifact "Client behavior".)
- INV-8. **Unaddressable beats wrong.** A surface with no valid assignment shows
  no window label, is excluded from the addressable live projection, and rejects
  any label-targeted or addressability-dependent operation against it with
  `window_label_unavailable` per the operation matrix in D-C. Unaddressable is
  acceptable; a possibly-wrong label is forbidden. (Requirement "What must be
  built" 2; design artifact "Client behavior".)
- INV-9. **Provenance is required to carry a label across a restart, and
  fail-closed outranks continuity.** A cached assignment is authoritative after a
  client restart only when its provenance `fleetId` equals the configured fleet
  identity, its `allocatorId` equals the configured allocator identity, AND it
  records a durable issue (`committed: true`), its `authorityId` equals the
  active authority, and its `ownerAnchorId` equals the anchor read from secure
  storage. A bare persisted `windowLabel`, copied provenance whose owner anchor
  is absent or different, or
  provenance for a different fleet or allocator identity, is a legacy label and
  its surface is unaddressable until it claims. Live re-confirmation on restart is
  governed by one rule, with the settled fail-closed rule (INV-6) as the higher
  priority when they tension:
  - if the allocator is reachable at restart, the client MUST re-confirm each
    provenanced surface with an idempotent re-confirm (REQ-C1) before admitting it as
    addressable; re-confirmation catches an allocator re-initialized under a new
    identity (identity mismatch -> unaddressable) or any divergence, and for a
    still-valid assignment returns the identical immutable mapping;
  - if the allocator is unreachable at restart, the client MAY admit a
    provenanced surface as addressable WITHOUT a live round-trip only because the
    assignment is immutable (INV-4) and never reused (INV-3), and only when its
    provenance `fleetId`, `allocatorId`, `authorityId`, and `ownerAnchorId` equal
    configured and secure-store values and it is `committed`; otherwise it stays
    unaddressable (fail closed). When reachability returns, the client
    re-confirms in the background and drops the surface to unaddressable at once
    on any identity or assignment mismatch.
  A client with no configured allocator identity for a fleet MUST claim live
  before any surface is addressable and MUST NOT trust any persisted label
  offline. Requiring a live round-trip for the reachable case, and forbidding
  offline trust without a configured identity, is the fail-closed choice: it
  never prefers a possibly-stale cached label over the live authority's word when
  that word is obtainable. Offline continuity is safe against re-initialization
  only because a new-identity re-initialization while old provenance may exist is
  forbidden as a hot recovery path (INV-15). (Design artifact "Client behavior",
  "Persistence and recovery", "Migration"; operator clarification 2026-09-03;
  review B-03.)
- INV-10. **Idempotent, serialized claims.** Repeated or concurrent claims for
  one bound fleet surface key return one stable assignment. Concurrent claims
  for different keys serialize through custody and receive different reserved
  ordinals. A copied or colliding authority with a different owner anchor fails
  ownership validation and cannot alias the bound key.
- INV-11. **Pane labels are lowest-free on every client.** Each client allocates
  the lowest free positive integer `paneLabel` within a window, client-local. On
  Electron this already holds (`lockless-client-authority.ts` lowest-free
  search). On iOS the current monotonic counter
  (`SurfAceLocklessTopologyOperations.swift` `nextPaneLabel`, initialized to 2)
  is **not** lowest-free and MUST be corrected to lowest-free within a bounded
  change that leaves pane IDs, topology revisions, split/close semantics, and
  targeting rules otherwise unchanged. Fleet uniqueness of the
  `windowLabel + paneLabel` token comes solely from the fleet-unique
  `windowLabel`. (Requirement "What must be built" 4; design artifact "Pane
  labels"; `DESIGN.md` §3.1.1 rule 4; review B-10.)
- INV-12. **Single startup validation gate.** Before serving any claim after a
  load, the allocator acquires the host lock and custody writer token, then
  validates the custody head and local projection. It either passes every §D-D
  check or fails closed. There is no partial-serve state.
- INV-13. **Next-ordinal fence never rolls back.** Custody owns
  `nextOrdinalFence`. A reservation atomically returns its old value `n` and
  persists `n + 1` before a mapping can commit. Restore never writes a smaller
  value. Recovery completes a durable `reserved` transaction under D3. An
  ordinal becomes permanently unavailable when its transaction reaches
  `burned`; a committed ordinal remains assigned. This single fence meaning
  applies to state, diagnostics, backup, restore, and acceptance.
- INV-14. **Unknown persistence fails closed until resolved.** If a commit's
  durability is unknown, the allocator sends no success or clean failure. It
  stops serving and queries custody by `transactionId`. Only custody's durable
  `absent`, `reserved`, `burned`, or `committed` answer selects a D3 transition.
  A failed query or contradictory transaction record keeps it fail closed for
  operator recovery.
- INV-15. **New-identity re-initialization is not a hot recovery.** Creating a
  new `allocatorId` (REQ-I1) invalidates all prior provenance and MUST NOT be
  used to recover a lost or corrupt allocator while any client may still hold
  prior-identity provenance, because an offline client cannot be reached to
  revoke a stale label and two fleets reusing the visible letter space would
  show two `a`s. The only recovery from a lost or corrupt allocator is restore of
  a verified backup of the **same** `allocatorId` (REQ-I3), fenced by INV-13.
  New-identity initialization is a genuine new/wiped-fleet operation whose
  runbook requires all clients drained of prior provenance first. (Review B-03,
  B-06.)

Change note against `DESIGN.md` §15.1: §15.1 says a window label "MUST be
visible at all times" and "MUST NOT be hidden based on … connection state." This
spec's live authority for a bounded exception is the core invariant in the same
`DESIGN.md` (`edc747d`) and the requirement doc: a surface with **no valid
assignment** shows no window-identity overlay (INV-7, INV-8). Once a surface
holds a valid assignment, §15.1 governs unchanged — its label is always visible
and is never hidden by pointer, hover, content type, annotation mode, or
transient connection state. The exception is keyed on *absence of authority*,
never on connection state.

---

## Architecture

### D-A. Allocator placement and configuration

- REQ-A1. The allocator is one resident process on one fleet coordinator host,
  configured explicitly. It is not started per surface and does not run on every
  client. (INV-1; design artifact "Decision".)
- REQ-A2. The coordinator host and the allocator's listen address are set by
  explicit, validated configuration. If the configuration is absent or
  malformed, the allocator refuses to start and the failure is reported; it does
  not pick a default host or port. (Consistent with `DESIGN.md` core invariant
  14, "explicit validated host configuration".)
- REQ-A3. Each surface client is configured with one allocator WebSocket URL and
  one `fleetId`, and reaches the allocator over the fleet network. A client with
  no configured allocator URL treats every surface as unaddressable (INV-8) and
  reports the missing configuration through diagnostics (§D-H); it never falls
  back to client-local allocation.
- REQ-A4. A client is configured with the expected `fleetId` and, when known,
  the expected `allocatorId` for its fleet, available offline. Every provenance
  and response check compares against these configured values; a mismatched
  `fleetId` or `allocatorId` in a response is rejected
  (`fleet_identity_mismatch` or `allocator_identity_mismatch`) and the surface
  stays unaddressable (REQ-C5). A client that has never learned an allocator
  identity for its configured fleet (fresh install, no prior claim) treats every
  persisted label as legacy and MUST claim live before any surface is
  addressable; it MUST NOT trust a persisted label offline without a configured
  identity to compare against (INV-9, fail-closed).
- REQ-A5. Each authority reads or creates its own `ownerAnchorId` in the
  installation-owned secure-store slot defined in Terms. The authority reads or
  creates an `authorityId` in its durable profile. Before a claim, the client
  binds that pair with `authority.bind` (REQ-C0). Custody accepts the first
  binding and returns it idempotently thereafter. If the `authorityId` is
  already bound to a different anchor, it returns
  `authority_ownership_conflict` and creates no assignment.
- REQ-A6. On `authority_ownership_conflict`, or when copied provenance names an
  owner anchor that does not equal secure storage, the client first makes every
  affected surface unaddressable. It mints and persists a new `authorityId`,
  binds the new pair, discards copied provenance as non-authoritative, then
  claims each surface under the new bound key. The original authority and its
  assignments do not change. If any bind or persistence step fails, the copied
  authority remains unaddressable. This is the sole rekey seam.

### D-B. Authority and allocation semantics

- REQ-B1. The fleet custody store owns one stable
  `{ fleetId, allocatorId, stateVersion }` header, `nextOrdinalFence`, the
  authority-owner binding map, the immutable fleet-surface assignment map, the
  transaction ledger, and the current writer token. The allocator's local file
  is a derived snapshot of that accepted custody state.
- REQ-B2. On a claim for a fleet surface key with no existing assignment, the
  allocator creates one `transactionId`; custody atomically reserves
  `n = nextOrdinalFence` and advances the fence to `n + 1`; the allocator then
  computes `base26(n)` and atomically commits the mapping under that transaction.
  It replies only after the mapping stage is committed. A reservation whose
  mapping stage is durably resolved as not committed transitions atomically to
  `burned` before the allocator returns a clean failure. A later claim for the
  still-unassigned key creates a new `transactionId` and reserves from the
  current fence; it never reopens the burned transaction.
- REQ-B3. On a claim for a fleet surface key that already has an assignment, the
  allocator replies with the existing assignment and commits nothing. (INV-4,
  INV-10.)
- REQ-B4. The allocator never searches for a locally unused label and never
  reuses a label. Closing a surface does not free its label in v1. (INV-3;
  design artifact "Persistence and recovery", "Migration".)
- REQ-B5. Custody serializes reservations and validates the current writer token
  inside each mutation, so different fleet surface keys cannot reserve the same
  ordinal even if an obsolete process remains alive.
- REQ-B6. `base26(n)` is the bijective base-26 encoding over the alphabet
  `a`–`z`: `0->a … 25->z, 26->aa, 27->ab …`, matching `DESIGN.md` §3.1.1 and
  §15.1. The decode inverse MUST round-trip for validation (§D-D).
- REQ-B7. **Residual collision safety net.** If, for any reason, the allocator
  would record two distinct fleet surface keys against the same `windowLabel`, or
  a claim arrives whose composed key is malformed, it MUST refuse the claim with
  `internal_error` and fail closed rather than issue a duplicate. This is a
  belt-and-suspenders check on top of the fleet-surface-key uniqueness (REQ-B1);
  the composed key is designed to make duplicates unrepresentable, and this check
  catches any implementation slip. (Review B-02.)
- REQ-B8. `label.reconfirm` supplies the client's complete cached assignment.
  The operation is read-only. If accepted custody has the same mapping from the
  activated snapshot, it returns `confirmed`. If REQ-D10 journal replay reconstructed
  that exact mapping before activating the restore generation, the accepted
  mapping carries its `recoveredAtCustodyRevision` and re-confirm returns
  `recovered`. Any repeat re-confirm of that reconstructed mapping also returns
  `recovered`. The client is comparison evidence, never authority to create,
  import, or change a mapping. Any field mismatch or absence of a matching
  accepted mapping is `assignment_conflict`; the allocator fails closed and
  serves no further claim until an operator restores consistent custody.

### D-C. WebSocket protocol

The allocator is a WebSocket server; surface clients are WebSocket clients to
it. Encoding and correlation follow `DESIGN.md` §5 exactly: UTF-8 JSON text
frames; every message carries `v`, `type`, `op`, `id`, `sentAt`; requests and
responses carry a `payload`; error responses carry `error` with `ok: false`;
per-connection unique request `id`; last-1024 idempotent replay cache.

**Complete schema delta to `DESIGN.md` §5 / §10.** Add `authority.bind`,
`label.claim`, and `label.reconfirm` to the request and response unions. Extend
the pinned `ErrorResponse.op` enum with the exact pinned-source/live operations
missing from that older enum:
`surface.window.open`, `surface.window.close`, `pane.restore`,
`surface.window.restore`, `topology.apply`, `target.apply`, `target.register`,
`consumable.ack`, `consumable.sync`, `operation.receipt.sync`,
`operation.receipt.ack`, `authority.bind`, `label.claim`, and
`label.reconfirm`. Extend the closed `ErrorBody.code` enum with exactly:
`fleet_identity_mismatch`, `allocator_identity_mismatch`, `allocator_uninitialized`,
`allocator_state_corrupt`, `allocator_state_unsupported_version`,
`authority_ownership_conflict`, `assignment_conflict`, `persistence_failed`,
`persistence_outcome_unknown`, `writer_fence_unavailable`, and
`window_label_unavailable`. The pinned `invalid_payload` code continues to cover
an invalid request envelope or payload. Except for that enumerated code
extension, `ErrorBody` retains the pinned closed property shape and constraints:
only `code`, `message`, and optional `details` are allowed. Allocator identity
belongs in `error.details.allocatorId`; no direct `error.allocatorId` property
exists.

All six new request/success payload schemas set `additionalProperties: false`.
For `authority.bind`, the request requires `protocolVersion` (constant `1`),
`fleetId`, `authorityId`, and `ownerAnchorId`; `expectedAllocatorId` is the only
optional field. Its success requires `fleetId`, `allocatorId`, `stateVersion`
(integer, minimum 1), `authorityId`, `ownerAnchorId`, and `bound` (constant
`true`). `label.claim` requires the fields in REQ-C1 except that
`expectedAllocatorId` has the stated first-contact exception. Its success
requires every field shown in REQ-C2. `label.reconfirm` requires all claim fields
and `expectedAssignment`; `expectedAllocatorId` is required because provenance
already names it. Its success requires every claim-success field plus
`confirmation`, enum `confirmed | recovered`. `ordinal` is an integer with
minimum 0; `windowLabel` matches `^[a-z]+$`; `committed` is constant `true`; and
identity strings follow Terms. The nested `expectedAssignment` object also sets
`additionalProperties: false` and requires exactly `ordinal`, `windowLabel`, and
`committed`. This paragraph and the exact op/code additions
above are the full allocator schema delta; no other envelope convention, error
property, or schema constraint changes.

- REQ-C0. **Authority bind** uses the common envelope with
  `op: "authority.bind"` and payload
  `{ protocolVersion: 1, fleetId, authorityId, ownerAnchorId,
  expectedAllocatorId? }`. Its success payload is
  `{ fleetId, allocatorId, stateVersion, authorityId, ownerAnchorId,
  bound: true }`. The allocator commits the binding before success. A repeat of
  the same pair is idempotent. A different anchor for the same `authorityId`
  returns `authority_ownership_conflict` and no success. A clear persistence
  failure returns `persistence_failed`; an unknown outcome stops service until
  custody confirms the binding pair present or absent. Present returns the bind
  success; absent returns `persistence_failed`. The client remains unaddressable
  until it receives success.
- REQ-C1. **Claim and re-confirm requests** conform to the common request
  envelope. `label.claim` is:
  ```json
  {
    "v": 1,
    "type": "request",
    "op": "label.claim",
    "id": "<RequestId, unique per connection>",
    "sentAt": 0,
    "payload": {
      "protocolVersion": 1,
      "fleetId": "<configured fleet id>",
      "authorityId": "auth_...",
      "ownerAnchorId": "owner_...",
      "surfaceId": "sf_...",
      "expectedAllocatorId": "alloc_..."
    }
  }
  ```
  `label.reconfirm` uses the same envelope and identity fields, plus
  `payload.expectedAssignment` equal to
  `{ ordinal, windowLabel, committed: true }` from persisted provenance.
  For `label.claim`, `expectedAllocatorId` is omitted only on genuine first
  contact before any identity is known. It is required for `label.reconfirm`.
  The other fields are required. The allocator accepts either operation only
  after the `(authorityId, ownerAnchorId)` binding passes.
- REQ-C2. **Claim success response** (allocator -> client), conforming to
  `DESIGN.md` §5 response envelope:
  ```json
  {
    "v": 1,
    "type": "response",
    "op": "label.claim",
    "id": "<matching request id>",
    "ok": true,
    "sentAt": 0,
    "payload": {
      "fleetId": "<fleet id>",
      "allocatorId": "alloc_...",
      "stateVersion": 1,
      "authorityId": "auth_...",
      "ownerAnchorId": "owner_...",
      "surfaceId": "sf_...",
      "ordinal": 0,
      "windowLabel": "a",
      "committed": true
    }
  }
  ```
  A `label.reconfirm` success has the same payload plus
  `"confirmation": "confirmed"` or `"recovered"`; its `op` is
  `label.reconfirm`. Both results assert the exact supplied assignment is the
  accepted custody mapping.
- REQ-C3. **Error response** (allocator -> client), conforming to `DESIGN.md` §5
  / §10 `ErrorResponse` (`ok: false`, `error` body):
  ```json
  {
    "v": 1,
    "type": "response",
    "op": "label.claim",
    "id": "<matching request id>",
    "ok": false,
    "sentAt": 0,
    "error": {
      "code": "<allocator error code>",
      "message": "<human-readable string allowed by pinned ErrorBody>",
      "details": { "allocatorId": "alloc_..." }
    }
  }
  ```
  `error.details.allocatorId` is present when identity is known. `details` is
  omitted when there is no detail. This conforms to the pinned `ErrorBody`.
- REQ-C4. `authority.bind`, `label.claim`, and `label.reconfirm` idempotency and
  request-id reuse follow `DESIGN.md` §5.3 exactly:
  - a duplicate request `id` with an identical payload returns the original
    response from the last-1024 replay cache (§5.3.2–3);
  - a duplicate request `id` with a different payload returns
    `invalid_request_id_reuse` (§5.3.4);
  - independently, the fleet-surface-key-keyed immutable assignment (REQ-B3)
    makes any claim for an already-assigned key return the same label regardless
    of connection or request `id`. This is the correctness guarantee across
    reconnects; the replay cache is the transport-level guard.
- REQ-C5. Allocator error `code` values (`[a-z_]{1,64}`) inside `error.code`:
  - `invalid_payload` — request envelope or payload shape/type invalid (the
    existing pinned code).
  - `invalid_request_id_reuse` — request `id` reused with a different payload
    (§5.3.4).
  - `unsupported_protocol_version` — `payload.protocolVersion` not supported.
  - `fleet_identity_mismatch` — `payload.fleetId` is not this allocator's fleet.
  - `allocator_identity_mismatch` — `expectedAllocatorId` present and not equal
    to this allocator's identity.
  - `authority_ownership_conflict` — the supplied `authorityId` is durably
    bound to another `ownerAnchorId`; the client follows REQ-A6.
  - `assignment_conflict` — re-confirmation contradicts accepted custody; the
    allocator enters fail-closed recovery.
  - `allocator_uninitialized` — no state exists and the allocator has not been
    explicitly initialized; fail closed (INV-6). Distinct from a served empty
    fleet, which has an initialized header with zero mappings.
  - `allocator_state_corrupt` — loaded state failed a validation check in §D-D.
  - `allocator_state_unsupported_version` — `stateVersion` not supported by this
    build.
  - `persistence_failed` — the durable commit clearly did not succeed; no
    assignment was created and no success was sent (INV-5). The client MUST
    retry.
  - `persistence_outcome_unknown` — a commit's durability is unknown/ambiguous
    (INV-14); the allocator is fail-closed pending resolution. The client MUST
    NOT treat this as not-committed; it retries the claim, which is idempotent by
    fleet surface key once the allocator resolves and serves again.
  - `writer_fence_unavailable` — the allocator lacks the current custody writer
    token or custody cannot validate it; no mutation or success occurs.
  - `rate_limited` — temporary throttle; the client retries with backoff.
  - `internal_error` — unhandled allocator error, including the residual
    collision safety net (REQ-B7).
- REQ-C6. The client MUST reject a response whose `id` does not match a request
  it sent on that connection, whose `payload.surfaceId`/`payload.authorityId` do
  not equal the pair it claimed, whose `ownerAnchorId` does not equal secure
  storage, whose `fleetId` or `allocatorId` does not match configured/expected
  values, or whose `windowLabel` does not decode to `ordinal`. A re-confirm
  response must also equal every field in `expectedAssignment`. A rejection
  leaves the surface unaddressable and is reported through diagnostics.
- REQ-C7. **Exhaustive unaddressable operation matrix.** The matrix covers the
  pinned public request set in `message-names.ts`, the larger lockless request
  union in `lockless.ts`, the three allocator recovery ops, diagnostics, and
  label resolution. No request is left to implementation judgment.

  | Operation (concrete) | On an unaddressable surface |
  |---|---|
  | Label resolution ("window b" -> surface, at controller/OpenClaw) | FAILS: the surface is absent from the addressable projection, so the label does not resolve; caller sees `window_label_unavailable`. |
  | `surfaces.list` | ALLOWED (inspection): the surface appears with `windowLabel: null`, `addressable: false` (schema delta below). |
  | `panes.list` | ALLOWED (inspection). |
  | `heartbeat.ping` | ALLOWED (liveness/inspection). |
  | `authority.bind`, `label.claim`, `label.reconfirm` | ALLOWED (ownership and label recovery). |
  | Diagnostics read (§D-H) | ALLOWED (inspection). |
  | `surface.window.open` | ALLOWED only to create a dormant unaddressable surface. It returns the pinned success response and preserves its existing `surfaceId` field semantics; no addressable projection or visible label exists until provenance is durable. |
  | `surface.window.restore` | ALLOWED only to restore a dormant unaddressable surface and its tombstone/provenance. It returns the pinned success response and completes re-confirm before any addressable projection. |
  | `surface.window.close` | ALLOWED for cleanup. It retains the immutable mapping/provenance and never frees the label. |
  | `pair.request` | REJECTED with `window_label_unavailable`. |
  | `content.set` / `content.append` / `content.patch` / `content.clear` | REJECTED with `window_label_unavailable`. |
  | `annotations.remove` | REJECTED with `window_label_unavailable`. |
  | `snapshot.get` / capture | REJECTED with `window_label_unavailable`. |
  | `pane.split`, `pane.rename`, `pane.close`, `pane.restore` | REJECTED with `window_label_unavailable`. |
  | `topology.apply` | REJECTED with generic `ErrorResponse` code `window_label_unavailable`; its `windowLabel` input is checked only after addressability and never relabels. |
  | `target.apply` | REJECTED before intent admission with generic `ErrorResponse` code `window_label_unavailable`; no intent, receipt, work item, or materialization commits. |
  | `target.register` | REJECTED before registration admission with generic `ErrorResponse` code `window_label_unavailable`; no registration commits. |
  | `consumable.ack`, `consumable.sync`, `operation.receipt.sync`, `operation.receipt.ack` | REJECTED with generic `ErrorResponse` code `window_label_unavailable` when scoped to the unaddressable surface; no delivery or receipt state mutates. |

  A bulk or sync request that names both addressable and unaddressable surface
  scopes rejects atomically; it does not apply the addressable subset. A sync
  request with no surface scope follows its existing behavior.

  A surface becomes addressable only after a committed claim and persisted
  provenance (REQ-E2); the ALLOWED inspection/recovery rows are exactly the
  positive path an operator uses to see why a surface is dark and drive it to
  addressable. (Design artifact "Client behavior" line 50; review B-08.)

  **Exhaustive label-bearing projection rule and schema delta.** At pin
  `edc747d`, the only protocol request field named `windowLabel` is
  `TopologyApplyRequest.payload.windowLabel`; it becomes a checked echo and a
  mismatch rejects the whole operation. Each element of
  `SurfacesListResponse.payload.surfaces[]` gains two required fields:
  - `windowLabel`: `string | null` — the assigned label, or `null` when the
    surface is unaddressable;
  - `addressable`: `boolean` — `true` only when the surface holds a valid
    assignment and may be resolved by label.
  These are additive; existing `surfaceId`, `name`, `viewport`, `paired` fields
  are unchanged. An unaddressable surface is always
  `{ windowLabel: null, addressable: false }`.

  The same rule covers every non-protocol projection at the pin: Electron
  surface/tombstone durable records; `surface-core` list and visible-address
  projections; renderer bootstrap/update state and identity overlay; native
  window title; `main.ts` tool, diagnostic, and log fields; iOS authority,
  runtime, model, and scene snapshots; iOS `displayId`/`visibleAddress`; and
  both platforms' topology/provider echoes. Each consumes the one validated
  assignment. When unaddressable, UI/addressing projections use no window
  label, structured inspection uses `windowLabel: null` plus
  `addressable: false`, and legacy snake-case diagnostic/log fields use
  `window_label: null`. No projection converts null, empty, legacy, provider,
  or topology input into authority. Surface/topology/pane events carry no
  independent label authority; any surface summary they reference uses this
  same nullable projection. Tombstones and backups may retain provenance for
  re-confirmation, but they do not make a surface addressable by themselves.
  `surface.window.open`, `surface.window.close`, and `surface.window.restore`
  responses and events gain no independent label authority; any embedded surface
  summary uses the same nullable projection. `target.apply`, `target.register`,
  consumable, and operation-receipt responses or echoes also gain no label
  authority. Any label token they carry is resolved against the addressable
  projection at admission and cannot populate or change an assignment.

### D-D. Persistence, atomic commit, and startup validation

- REQ-D1. The fleet custody record is the authority. Its accepted value is
  `{ fleetId, allocatorId, stateVersion, custodyRevision,
  nextOrdinalFence, authorityOwners[], mappings[], transactions[],
  currentWriterToken }`. A local allocator snapshot contains the same accepted
  projection and its `custodyRevision`; it may accelerate startup but cannot
  authorize a mutation or override custody.
- REQ-D2. Startup first takes a host-wide OS lock keyed by `fleetId` at one
  canonical location independent of the configured snapshot path. It then opens
  one exclusive fenced writer session in custody. Custody increments and returns
  the writer token atomically. Every mutation compares that token inside its
  transaction. Custody admits a replacement only after it observes the prior
  session close or an operator explicitly revokes it; elapsed time alone does
  not transfer ownership. Failure at either gate returns `writer_fence_unavailable`, opens
  no listening endpoint, and writes no state.
- REQ-D3. One new-assignment transaction has this exhaustive state machine:

  | Durable state for `transactionId` | `nextOrdinalFence` | Mapping | Required action/result |
  |---|---:|---|---|
  | absent; reserve clearly fails | unchanged | absent | Return `persistence_failed`; remain serving. |
  | reserve outcome unknown | unknown until query | absent or reserved | Stop serving; query custody by `transactionId`; follow the matching resolved row below. |
  | `reserved(n, key, ownerBinding)` after crash/recovery | `n + 1` | absent | The current writer idempotently commits that exact prepared key at `n`; a validation conflict follows the contradictory row. |
  | mapping clearly fails | `n + 1` | absent | Atomically change `reserved` to `burned`; return `persistence_failed` only after that change commits. A failed/unknown burn transition stops serving and resolves by transaction id. `burned` returns the clean failure; `reserved` follows the reserved recovery row and sends no prior failure. |
  | `burned(n, key)` | `n + 1` or greater | absent | Return/retain clean failure; no later operation may map ordinal `n`. |
  | mapping outcome unknown | `n + 1` | absent or present | Stop serving; query custody by `transactionId`. `committed` returns the exact success. `reserved` proves mapping did not commit and follows the reserved recovery row. |
  | `committed(n, key)` | `> n` | exact key -> `n` | Return success, or on recovery serve the same result to the repeat claim. |
  | contradictory transaction/mapping/binding | any | any | Return `assignment_conflict`; stop serving for operator restore. |

  Reserve linearizes when custody commits `reserved` and increments the fence.
  Assignment linearizes when custody commits the immutable mapping. The local
  snapshot is written only after custody acceptance and is never a linearization
  point.
  Failure to refresh the non-authoritative local snapshot records a diagnostic
  but does not undo a custody-committed mapping or change its success response.
- REQ-D4. Crash recovery is exhaustive by boundary: before reserve, no durable
  effect; after reserve and before mapping, commit the recorded exact prepared
  key; after a clear mapping failure and before or during the burn CAS, query the
  transaction, where `reserved` follows the reserved recovery row and `burned`
  retains the failure; after burn and before the failure reply, a later claim
  starts the new transaction required by REQ-B2; after mapping and before the
  local snapshot, rebuild the snapshot from custody; and after snapshot and
  before the success reply, a repeat claim returns the committed mapping. A
  process never guesses from a missing reply, elapsed time, or local bytes.
- REQ-D5. On startup, before serving, the allocator validates: the header and
  supported version; the configured `fleetId` and `allocatorId`; current writer
  token; increasing custody revision; one owner anchor per `authorityId`; one
  assignment per bound fleet surface key; one key per ordinal and label;
  `windowLabel = base26(ordinal)`; each mapping ordinal is below
  `nextOrdinalFence`; each transaction record is `reserved`, `burned`, or
  `committed` (`absent` means no record exists); each committed transaction has
  its exact mapping; and each reserved
  or burned ordinal is below the fence. A local snapshot ahead of custody, a
  duplicate, or a contradictory ledger entry is corrupt. A stale local snapshot
  is replaced from custody before serving.
- REQ-D6. Missing, unreadable, unsupported, or inconsistent custody fails closed
  with the applicable allocator error. Missing or corrupt local snapshot alone
  is recoverable by rebuilding it from valid custody. The allocator never creates
  a new sequence on either failure.
- REQ-D7. Unknown resolution uses only an idempotent custody query keyed by
  `transactionId`. A durable `reserved`, `burned`, or `committed` record selects
  the corresponding D3 action. An absent record proves reserve did not commit.
  A query failure or contradiction retains fail-closed
  `persistence_outcome_unknown`; no request outcome or fence value is inferred.
- REQ-D8. Custody maintains an append-only transaction journal on storage
  independent of the coordinator snapshot path. It records each transaction's
  `{ fleetId, allocatorId, transactionId, ordinal, key, ownerBinding }` and its
  durable `reserved`, `committed`, or `burned` transition. The custody backend
  makes each state transition and corresponding accepted-state mutation one
  linearizable durable operation. A stage does not return committed until its
  journal transition commits. Backup captures a mapping snapshot plus the
  journal position; restore replays through the current journal head, rebuilds
  committed mappings, retains burned ordinals, and sets `nextOrdinalFence` one
  greater than the greatest ordinal ever recorded as reserved, or 0 when the
  journal has no transaction. It never uses a snapshot's lower value. This
  journal is the recoverable non-rollback fence and mapping custody.
- REQ-D9. If both live custody and its independent transaction journal are lost,
  same-identity recovery is impossible: the allocator fails closed. The operator
  may initialize a new identity only after the INV-15 drain. The system does not
  pretend an old snapshot proves the missing fence.
- REQ-D10. Restore uses an inactive custody generation and one atomic activation
  CAS. The operator first fences and drains the allocator writer. Custody creates
  `preparing(generationId, snapshotRevision, journalPosition)` without changing
  the accepted generation. It verifies the snapshot, replays the journal through
  its captured current head, marks reconstructed mappings with
  `recoveredAtCustodyRevision`, computes the fence under D8, validates every D5
  rule, and records `ready(generationId, replayedJournalHead, computedFence)`.
  One CAS then changes the accepted generation from the prior revision to that
  exact ready generation and records `activated`. A crash or clear/unknown write
  before activation leaves the prior accepted generation authoritative; startup
  resumes or discards the inactive generation by `generationId`. An unknown
  activation is resolved by querying that id: the accepted generation is either
  the prior revision or the complete ready generation, never a partial mixture.
  When live custody has been lost, verified same-identity backup custody starts
  recovery with no accepted generation; the activation CAS expects `absent` and
  installs the complete ready generation. Before that CAS, no state can serve.
  This bootstrap is permitted only when the snapshot and journal satisfy I2 and
  carry the same `fleetId` and `allocatorId`; it never mints identity or fence
  state. A crash after activation loads the activated generation. The allocator
  obtains a new writer token and listens only after activation and D5 validation.

### D-E. Client behavior: provenance, fail-closed addressability, reconnect

- REQ-E1. Client per-surface state records allocator provenance
  `{ fleetId, allocatorId, stateVersion, authorityId, ownerAnchorId, surfaceId, ordinal,
  windowLabel, committed: true }` alongside the surface, written only after the
  client observes a durably committed success (REQ-C2). A `windowLabel` with no
  matching provenance, with provenance for another `fleetId` or a non-configured
  `allocatorId`, or with no `committed` mark is a legacy label and is not
  authoritative. Provenance whose `ownerAnchorId` does not equal the current
  secure-store anchor is copied state and follows REQ-A6.
- REQ-E2. On surface open or restore, before exposing the surface as
  addressable, the client obtains or confirms an authoritative assignment, with
  fail-closed (INV-6) as the higher priority (INV-9):
  - if it has no valid provenance (none, wrong fleet, wrong identity, wrong
    owner anchor, or uncommitted), it binds/rekeys per REQ-A5/A6, issues
    `label.claim`, and,
    on a committed success, persists provenance (REQ-E1) *before* admitting the
    surface as addressable (INV-7);
  - if it holds valid provenance AND the allocator is reachable, it sends
    `label.reconfirm` with that exact assignment before admission. `confirmed`
    or `recovered` must echo every `expectedAssignment` field byte-for-byte; the
    client persists the response, then changes the local projection atomically from
    `{windowLabel: null, addressable: false}` to
    `{windowLabel: expected.windowLabel, addressable: true}`. Any identity,
    owner, or assignment conflict keeps the null/false projection;
  - if it holds valid provenance AND the allocator is unreachable, it MAY admit
    the surface as addressable using the persisted assignment (INV-9), then
    re-confirm in the background when reachability returns and drop the surface
    to unaddressable at once on any mismatch. A background re-confirm never
    downgrades a surface whose assignment still matches.
- REQ-E2a. A clone transition is atomic at the client authority seam: anchor
  mismatch or ownership conflict changes every copied surface to null/false
  before the client persists a replacement `authorityId`. The client binds the
  replacement before it claims. It changes each surface to addressable only
  after its new provenance is durable. At no point does copied provenance appear
  under the replacement authority.
- REQ-E3. While a surface has no valid assignment and the allocator is
  unreachable or returns an error, the client:
  - keeps `windowLabel` empty and hides the window-identity overlay box (the
    pane label continues to render per `DESIGN.md` §15.1);
  - keeps the surface out of the addressable live projection, listing it with
    `windowLabel: null` and `addressable: false` (REQ-C7 schema delta) so it
    cannot be resolved by label;
  - rejects the REJECTED operations of the D-C matrix against that surface with
    `window_label_unavailable`, and permits the ALLOWED inspection/recovery
    operations;
  - retries the allocator with bounded exponential backoff and publishes
    diagnostic state (§D-H);
  - never displays a provisional, host-qualified, random, or client-local label
    (INV-7).
  (Design artifact "Client behavior".)
- REQ-E4. Readiness is per surface. A client process stays alive while one or
  more of its surfaces wait for labels; unaddressable surfaces do not block
  addressable ones. (Design artifact "Client behavior".)
- REQ-E5. Reconnect. On losing the allocator connection, the client reconnects
  with bounded backoff and re-confirms per REQ-E2; because claim and re-confirm
  operations are idempotent by fleet surface key (REQ-C4), reconnect never
  changes an assigned label. Ordinary
  controller <-> surface reconnect is unchanged by this spec, except that an
  unaddressable surface stays unaddressable until it obtains a label.

### D-F. Migration (Electron and iOS): full label-writer inventory

- REQ-F1. On the first upgraded boot, every live surface that carries only a
  legacy client-local label (no valid provenance) is unaddressable (INV-8,
  INV-9) until it claims a fleet label.
- REQ-F2. The allocator ignores the legacy letter as authority and assigns from
  its own sequence. Migration does not change `surfaceId`, pane identity, content,
  or topology (pane labels change on iOS only per INV-11). This deterministically
  repairs the live fleet's duplicate labels (requirement "Current state").
  (Design artifact "Migration".)
- REQ-F3. **Every reachable client-local window-label writer is removed or
  converted to a checked echo of the allocator assignment.** The migration is not
  complete until each of the following seams is closed; a builder MUST verify
  each by name. Any inbound `windowLabel` in a provider/topology payload becomes
  a **checked echo**: it is validated against the allocator assignment for the
  target fleet surface key and REJECTED (surface goes unaddressable, or the op
  returns `window_label_unavailable`/a mismatch error) if it disagrees — it is
  never an authority that can set or relabel a window.
  - Electron `packages/electron/src/surface-core.ts`:
    - the lowest-free window-letter computation (`usedWindowLabels` derived from
      one client's `listSurfaces()`) — deleted or made unreachable; replaced by
      the allocator claim;
    - the admission path (~`:1252-1265`) — must not assign a window label;
    - the tombstone/relabel-on-restore path (~`:1396-1419`) — must reuse the
      allocator-issued label via provenance, not recompute one;
    - the provider bootstrap / `topology.apply` path (~`:2220-2333`) — any
      `windowLabel` becomes a checked echo, never an authority.
  - Electron `packages/electron/src/ws-server.ts` provider-supplied
    `topology.apply.windowLabel` (~`:3257-3369`) — checked echo only; a
    provider cannot set or change a window label.
  - iOS `packages/ios/SurfAce/SurfAceLocklessTopologyOperations.swift`:
    - the client-local window-label allocation on open (~`:351-380`) — deleted or
      made unreachable; replaced by the allocator claim;
    - the tombstone/relabel-on-restore path (~`:423-453`) — reuse the
      allocator-issued label via provenance.
  - iOS `packages/ios/SurfAce/SurfAceRuntime.swift` restore/projection
    (~`:849-908`) — surfaces window labels from provenance/allocator only; never
    mints or recomputes a label.
  (Requirement "Current state", "How it was lost"; design artifact acceptance
  test 9; review B-09. Line numbers are at pin `edc747d`/current source and are
  guides; the builder closes the seam even if a line moved.)
- REQ-F4. Recoverable tombstones retain the allocator-issued mapping and
  provenance. Restoring the same fleet surface key re-confirms and receives the
  same label (INV-4); it claims only when no valid provenance exists. Closing a
  surface does not free its label in v1 (INV-3). (Design artifact "Migration".)

### D-G. Pane labels

- REQ-G1. Pane-label allocation stays client-local: each client allocates the
  lowest free positive integer `paneLabel` within a window. Electron already does
  this. **iOS MUST be corrected** from its monotonic `nextPaneLabel` counter
  (`SurfAceLocklessTopologyOperations.swift`, initialized to 2) to a lowest-free
  search, within a bounded change that leaves pane IDs, topology revisions,
  split/close semantics, and targeting rules otherwise unchanged (INV-11). No
  pane-label allocation moves into the allocator service. (Design artifact "Pane
  labels"; review B-10. Scope note: whether the iOS pane correction rides this
  card or a separate card is OQ-6, NON-BLOCKING for the spec — the required
  end-state is lowest-free on both clients regardless.)

### D-H. Observability

- REQ-H1. The allocator exposes diagnostic state: `fleetId`, `allocatorId`,
  `stateVersion`, `custodyRevision`, `nextOrdinalFence`, current writer-token
  generation, total assignment count, burned-ordinal count, last
  successful commit time, current serve status (`serving`, or a fail-closed
  reason from INV-6 including `unknown-persistence` and
  `writer-fence-unavailable`),
  and uptime. Read-only; carries no authority.
- REQ-H2. Each client publishes per-surface label diagnostics: whether the
  surface is addressable, its `windowLabel` (or null), the configured allocator
  URL, configured `fleetId`, expected `allocatorId`, this authority's
  `authorityId`, current `ownerAnchorId`, last claim/re-confirm attempt time,
  last error code, and current backoff.
  These surface through the existing `surf_ace_authority_diagnostics` tool path
  (`DESIGN.md` §14.3).
- REQ-H3. A client that rejects an allocator response (REQ-C6) records the
  rejection reason in diagnostics; a rejected response never silently becomes an
  addressable label.

### D-I. Operator: initialization, backup, restore

- REQ-I1. **Initialize (new fleet only).** An explicit operator action creates a
  new fleet in custody with a freshly minted `allocatorId`, configured `fleetId`,
  current `stateVersion`, `nextOrdinalFence = 0`, empty owner/mapping/transaction
  sets, and the first writer token. Initialization refuses when the custody key
  or transaction journal exists, so it cannot reset a live fleet. It is
  **not** a recovery for a lost/corrupt allocator (INV-15); its runbook requires
  every client to be drained of prior provenance first, because an offline client
  holding old provenance would otherwise display a label the new fleet reissues.
  (Design artifact "Persistence and recovery"; review B-03.)
- REQ-I2. **Backup.** A backup contains one accepted custody mapping snapshot,
  its identity and custody revision, and its transaction-journal position. The
  independently retained append-only transaction journal is part of backup
  custody, not diagnostic metadata. A successful backup proves its snapshot and
  journal position share one accepted custody revision.
- REQ-I3. **Restore (same identity, fenced).** An operator restores by placing a
  verified mapping snapshot under the same `fleetId` and `allocatorId` into the
  inactive generation of REQ-D10, then replaying the independently retained
  journal through its captured current head. Only the atomic D10 activation
  makes that generation accepted. The replay computes `nextOrdinalFence` and
  reconstructs committed mappings; the snapshot cannot lower or overwrite
  either. A post-backup surface sends
  `label.reconfirm` with its exact cached assignment before reachable admission.
  Custody returns `recovered` for the journal-reconstructed assignment under
  REQ-B8, after which the client performs
  the null/false to label/true transition in REQ-E2. The surface keeps its old
  label; restore never relabels it. A conflict fails the allocator closed.
- REQ-I4. On missing or failed state, the allocator does not self-heal by
  creating a new sequence; the only recovery is REQ-I3 (restore the same fleet,
  fenced). REQ-I1 (new fleet) is reserved for a genuinely new or fully drained
  fleet (INV-15). (INV-6.)

### Split-brain safety argument (why v1 needs no election)

By INV-1 there is one configured allocator endpoint and one custody-accepted
writer token, with no fallback. A path-local copy cannot pass the canonical host
lock; a host copy can open its own local lock but cannot acquire a second custody
writer session; and any stale process loses every mutation CAS. Two surfaces can
share a label only if (a) two reservations return one ordinal, which custody's
linearizable fence forbids; (b) an ordinal is reissued, which the append-only
transaction journal forbids; (c) a client trusts the wrong allocator, which
identity and provenance checks forbid; or (d) two physical authorities alias one
key, which owner binding and fail-closed rekey prevent. No process elects a
leader: the operator configures one endpoint and custody admits one fenced
writer. The design
deliberately trades availability (a down coordinator makes new claims
unavailable, failing closed to "unaddressable", INV-8) for the safety property,
because a split-brain here means two `a`s, the exact prohibited outcome
(requirement "What must be built" 1). Any future move to leader election is out
of scope (G-N1) and would require a proof of no split-brain before it is
permitted.

---

## Acceptance

Each check is release-blocking and maps to the design artifact's required proofs
(design artifact "Required proof" 1–10 and the fleet acceptance run) plus the
review-driven additions. A check is written so a reviewer can decide pass or fail
from observed output.

- AC-1 (proof 1 — the mandatory duplicate test). Given two independent client
  authorities with distinct owner anchors configured to one real running
  allocator, When both concurrently claim labels for many `surfaceId`s
  **including deliberately colliding client-local `surfaceId`s (for example both
  authorities' `sf_0000000000000001`)**, Then every returned `windowLabel` is
  distinct and the test FAILS if any two authorities ever receive or display the
  same window label. (INV-2, A-6; requirement "What must be built" 3; review
  B-02.)
- AC-1b (real clone ownership/rekey). Given one real client profile with a bound
  authority and assigned surface, When its profile/state bytes are copied first
  to a second authority slot on the same host and then to a second real host,
  without copying either secure-store slot, and both clients run in each case,
  Then each copy detects its local anchor mismatch, first projects null/false,
  persists a new `authorityId`, binds it, and
  receives a different label; the original retains its identity and label. The
  test fails if copied provenance is displayed, both installations use one
  assignment, or any rekey failure leaves the clone addressable. Repeat with two
  independently created authorities forced to the same `authorityId`; in that
  case the second bind must return `authority_ownership_conflict` before rekey.
- AC-2 (proof 2). Given one fleet surface key, When a client issues repeated and
  concurrent `label.claim` calls for it, Then every response carries the same
  `ordinal` and `windowLabel` and the allocator committed exactly one mapping.
  (INV-4, INV-10.)
- AC-3 (proof 3). Given an allocator with committed assignments, When the
  allocator process restarts, Then every prior mapping is preserved and the next
  new claim receives `nextOrdinalFence` as reserved at the transaction point, with
  no reuse. (INV-3, INV-5, INV-13, REQ-D4, REQ-D5.)
- AC-4 (proof 4). Given a client holding an allocator-issued label with valid
  provenance (configured fleet and identity, `committed`), When the client
  restarts with the allocator reachable, Then it live-re-confirms with an
  exact `label.reconfirm` before admitting the surface, keeps the same window label, and
  never re-mints a different label; And When the client restarts with the
  allocator unreachable, Then it admits the surface addressable from the
  persisted assignment and re-confirms in the background once reachability
  returns. (INV-9, REQ-E2.)
- AC-4b (restart fail-closed against re-initialization). Given a client holding
  provenance for allocator identity X, When the allocator has been re-initialized
  under a new identity Y (REQ-I1): if the allocator is reachable, Then the live
  re-confirm returns identity Y, the client detects the mismatch against its
  configured/held identity X, and the surface is unaddressable until it claims a
  fresh label under Y; and Given a client with no configured allocator identity
  and only a persisted bare label, When it restarts offline, Then every such
  surface is unaddressable until a live claim succeeds. (INV-6, INV-9, REQ-A4,
  REQ-E1, REQ-E2.)
- AC-4c (offline label survives no reset — the B-03 hole). Given client A
  offline holding valid provenance for identity X showing label `a`, When an
  operator attempts to recover the fleet, Then the only permitted recovery is
  restore of identity X (REQ-I3), a new-identity re-initialization is refused as
  a hot recovery (INV-15, REQ-I1 guard), and therefore no second fleet issues a
  colliding `a` while A is offline; the test FAILS if any recovery path lets a
  new identity reissue `a` while prior-identity provenance may still be
  displayed. (INV-15; review B-03.)
- AC-5 (proof 5 — unaddressable operation matrix). Given a surface with no valid
  assignment, When each exact D-C operation runs, Then inspection, allocator
  recovery, dormant `surface.window.open`/`restore`, and cleanup
  `surface.window.close` produce only their specified ALLOWED results;
  `pair.request`, content and annotation writes, snapshot, each pane mutation
  including `pane.restore`, `topology.apply`, `target.apply`, `target.register`,
  consumable/receipt ops, and label resolution produce their exact specified
  rejection envelope with no mutation. Exercise each projection inventory row
  and observe null/false or no UI label while unaddressable. Then make the
  allocator available; observe label/true only after provenance persists.
  (INV-7, INV-8, REQ-C7, REQ-E2, REQ-E3; review B-08.)
- AC-5b (closed schema conformance). Given the pinned §10 schema plus the full
  delta in D-C, When each allocator success/error and each unaddressable
  rejection is validated, Then it passes; removing an enum addition, adding
  direct `error.allocatorId`, or returning a success-shaped target response for
  an unaddressable rejection fails validation.
- AC-6 (proof 6 — legacy duplicates). Given two clients each starting with the
  same legacy `windowLabel` and no provenance, When both migrate against one
  allocator, Then each receives a different fleet label and no two live surfaces
  display the same label. (INV-2, INV-9, REQ-F1, REQ-F2.)
- AC-7 (proof 7 — fail closed on corruption). Given an initialized allocator
  whose custody record is corrupt, unsupported, or missing, When it loads, Then
  it fails closed and does not move the fence. When only the local snapshot is
  missing/corrupt, Then it rebuilds from valid custody before serving.
- AC-8 (proof 8 — exhaustive clear persistence failures). Given an initialized
  allocator, When a clear failure is injected before reservation, Then no
  transaction or mapping exists, the fence is unchanged, and the response is
  `persistence_failed`. Given a durable reservation of `n`, When a clear mapping
  failure is injected, Then custody records fence `n + 1`, transaction
  `burned(n)`, no mapping, and only then returns `persistence_failed`. When the
  claim is retried, Then its mapping uses an ordinal greater than `n`, and no
  later claim uses the burned ordinal.
- AC-8b (unknown/crash state machine). Given each reserve, mapping, and burn
  transition, When an unknown outcome is injected before and after its
  linearization point, Then the allocator exposes the exact D3 durable state,
  serves nothing while the outcome is unknown, and resolves only by
  `transactionId`. Given each D4 crash boundary, When the allocator restarts,
  Then it takes the exact D4 action and finishes with one mapping or a burned
  ordinal, never a duplicate or reused ordinal.
- AC-8c (fleet-wide single writer). Given byte-identical allocator snapshot and
  configuration bytes on two paths on one host and on two hosts, When processes
  start concurrently against the one real custody store, Then same-host path
  duplication loses the host lock and cross-host duplication loses the custody
  writer session. Exactly one endpoint listens and only its current writer token
  can reserve or commit. After forcibly fencing that writer, its next mutation is
  rejected even while its process remains alive. Also Given a client
  configured with a `fleetId`/`allocatorId` that does not match an endpoint it is
  pointed at, When it claims, Then it is rejected
  (`fleet_identity_mismatch`/`allocator_identity_mismatch`) and the surface stays
  unaddressable rather than acquiring a second label space. The test FAILS if two
  writers ever commit concurrently or a mismatched endpoint yields an addressable
  label. (INV-1, REQ-D2, REQ-A4; review B-06.)
- AC-8d (older-backup restore never reuses — the B-04 hole). Given an allocator
  that committed `a` and `b` (`nextOrdinalFence = 2`), When the operator restores
  an older mapping snapshot containing only `a` plus the current independent
  transaction journal, Then the computed fence remains 2 and the next new claim
  receives `c`. The surface holding cached `b` first projects null/false, sends
  exact `label.reconfirm`, receives `recovered` with `b`, persists it, then
  projects `b`/true. No relabel occurs. Repeat without the live custody record but
  with its independent journal backup. The test fails if `b` is reissued, the
  surface receives a new label, or restore proceeds without recoverable fence
  custody.
- AC-8e (atomic restore activation). Given an accepted generation and an older
  verified backup, When the allocator crashes or each storage outcome becomes
  unknown at every D10 boundary before activation, Then the prior accepted
  generation remains authoritative and no partial restored state can serve.
  When activation becomes unknown, Then a query by `generationId` returns either
  the complete prior generation or the complete replayed generation. Given a
  crash after activation, When the allocator restarts, Then it loads only the
  complete activated generation with the replay-computed fence and mappings.
- AC-9 (proof 9 — no client-local path, full inventory). Given the Electron and
  iOS builds, When each label-writer seam listed in REQ-F3 is inspected and
  exercised (admission, tombstone/relabel, provider bootstrap/`topology.apply`,
  ws-server provider `topology.apply.windowLabel`, iOS open, iOS tombstone, iOS
  runtime restore/projection), Then no reachable client-local window-label
  allocation path exists and every inbound provider/topology `windowLabel` is a
  checked echo that cannot set or change a label; every window label comes from an
  allocator claim. (INV-1, REQ-F3; review B-09.)
- AC-10 (proof 10 — panes lowest-free on both clients). Given a window on
  **Electron and on iOS**, When panes are created and closed such that a
  low-numbered pane is freed and a new pane is then created, Then each new pane
  receives the lowest free positive integer `paneLabel` within that window on
  both clients (the freed low number is reused before a higher one). The test
  FAILS if iOS assigns a monotonically increasing number instead of the lowest
  free. (INV-11, REQ-G1; review B-10.)
- AC-11 (fleet acceptance run). Given two real client authorities against one
  resident allocator and real custody, including colliding `surfaceId`s and one
  cloned profile, When windows are created/restored concurrently, clients and
  allocator restart, and one writer is fenced, Then rendered overlays and the
  authoritative list contain no duplicate label and no unlabeled addressable
  surface. The run is red on either condition.

Fixture honesty: AC-1, AC-1b, AC-2, AC-6, AC-8, AC-8b, AC-8c, AC-8d, AC-8e,
and AC-11 MUST run against a real allocator process and the selected real custody
adapter, with real client authorities where the check names clients. They do not
use a hand-written allocator or custody fixture. A fabricated "all-unique"
fixture would pass while shipping the exact broken behavior this work removes
(requirement "How it was lost": no test asserted the property, so every soak
passed). AC-1 is the single mandatory test called out in the requirement. r4
includes colliding client-local `surfaceId`s, real copied client state,
byte-identical two-host allocator state, and storage fault injection at every
specified transition.

Agent operating pattern: none. This specification defines product and operator
behavior; it does not teach a new agent operating pattern.

---

## Open Questions

Marked holes. Each is ruled BLOCKING (its scope waits) or NON-BLOCKING (build
around it). The settled inputs decide the load-bearing choices; the questions
below are the residue the inputs left open.

- OQ-1 (NON-BLOCKING). **Backoff bounds and rate-limit thresholds.** The client
  uses full-jitter exponential retry with base 500 ms and cap 30 s. The
  allocator default rate limit is 100 claim-family requests per connection per
  second; both values are explicit configuration. Future tuning is non-blocking
  because it changes availability, not an allocation outcome.
- OQ-2 (NON-BLOCKING). **`stateVersion` starting value and upgrade path.** v1
  starts at `stateVersion = 1`. A future schema change adds a versioned migration
  on load; v1 need only reject unsupported versions (REQ-D6). No cross-version
  migration is in v1 scope.
- OQ-3 (NON-BLOCKING). **Allocator authentication/authorization on the WS link.**
  v1 runs on the configured trusted fleet network with no WSS (G-N9)
  and no claim authentication (G-N10); the `authorityId` is a distinguishing key,
  not a credential. Whether to add a shared-secret or WSS profile is a later
  hardening decision, out of v1 scope. Do not add it without an operator ruling.
  (Watch: this is exactly the kind of unrequested hardening the org guards
  against; leaving it out is deliberate.)
- OQ-4 (NON-BLOCKING). **Label reuse / compaction policy.** v1 never reuses a
  label (INV-3, G-N4). Whether a future version reclaims labels of long-dead
  surfaces is deferred; it needs its own no-ambiguity ruling because reuse can
  reintroduce a duplicate a user still has in mind. Not in v1 scope.
- OQ-5 (BLOCKING for deployment only, not code). **Coordinator and custody
  values.** The operator must name the coordinator host, allocator URL,
  `fleetId`, custody backend/URL, and independent transaction-journal location.
  Code builds against the exact behavioral contract in A-3 and D-D with no
  default backend or endpoint. Deployment waits for these values.
- OQ-6 (NON-BLOCKING). **Does the iOS pane-lowest-free correction (INV-11,
  REQ-G1) ride this card or a separate card?** The required end-state is
  lowest-free on both clients regardless; this is a card-routing question for the
  product owner, not a spec ambiguity. The spec states the end-state; an
  orchestrator may split the iOS pane fix onto its own card without changing any
  requirement here. Raised to the operator because it is a scope-routing decision
  (the correction is a small behavior change to iOS pane numbering that the
  original "window label allocator" framing did not obviously include, though the
  settled requirement doc names lowest-free as required).

Non-goals are listed above (G-N1…G-N10); each boundary is stated so a builder
does not fill it with an assumption.

---

## Review response (r4)

r4 preserves the r3 clauses that review found closed and changes only the six
blocking areas in `art_55b97955`.

- **R3-01 (copied/colliding authority ownership).** Closed by the
  per-authority, per-installation owner anchor, allocator binding, fail-closed rekey seam,
  exact wire shapes, atomic client projection transition, and real clone plus
  forced-collision AC-1b. ADD won because an assignment still needs identity;
  DELETE would remove addressability, while ACCEPT would allow one key to denote
  two physical authorities.
- **R3-02 (two-record fence atomicity and recovery).** Closed by one explicit
  custody transaction state machine. `nextOrdinalFence` has one meaning: lowest
  never-reserved ordinal. The D3 table covers clear and unknown reserve/mapping
  outcomes; D4 covers each crash boundary; D7 resolves only by transaction id;
  D8/I2 give the fence independent recoverable custody. ADD won because DELETE
  would remove old-backup recovery and ACCEPT would permit ordinal reuse.
- **R3-03 (copied-state split brain).** Closed at the structural rung by a
  host-wide fleet lock plus a fleet-wide linearizable custody writer token that
  fences stale processes on every mutation. AC-8c starts byte-identical copies
  on two paths and two hosts, then proves only one can commit. This is not leader
  election: the endpoint is operator-configured and custody admits one writer.
  ADD won because neither deleting enforcement nor accepting two writers can
  satisfy the core invariant.
- **R3-04 (old-backup provenance and immutable assignment).** Closed by exact
  `label.reconfirm` request/response, recovery admission rules, and the
  null/false to old-label/true client transition. A missing post-backup mapping
  is reconstructed from the independent journal before atomic restore activation
  or the fleet fails closed; the client never supplies mapping authority.
  Relabeling was deleted because it contradicted immutable assignment.
- **R3-05 (closed ErrorBody).** Closed by retaining only `code`, `message`, and
  optional `details`, moving allocator identity to `details`, and enumerating
  the complete op/code delta. AC-5b validates each envelope.
- **R3-06 (operation and projection completeness).** Closed by the full public
  and lockless request matrix, including every operation named by the finding,
  plus the pinned label-bearing protocol, client, UI, tool, diagnostic, log,
  event, tombstone, and backup projections. AC-5 exercises each row. No new
  operation mechanism was added; the change classifies existing surfaces.
