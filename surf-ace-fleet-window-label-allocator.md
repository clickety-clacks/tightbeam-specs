# Surf Ace fleet-wide window-label allocator

Status: implementation-ready specification, before build. Revision r3.

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

**Revision r3 closes the ten blocking findings of the adversarial review
`art_99b70bbc` (SHA-256
`093b63a65642935f655a7c6e7e817cc44cf9db2296ef3443f5bf0f1c1d0f036d`). The
per-finding disposition is in "Review response (r3)" at the end. r3 supersedes
r2 (SHA-256 `137e0e85a5482387a05f06f9e28df34025837484ee4e8e117131435d80584a90`)
and r1 (SHA-256
`421f7cb5b29d8c675456aa4ad9d9d922bd6e2cb26ab50e4e682d98e1c1503c7a`); those
bytes are retained in this workspace and this document is the only spec to build
from.**

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
  client authority identity added in r3 (Terms, `authorityId`) is an internal
  allocation key, never a visible label component; it does not host-qualify or
  otherwise alter the plain alphabetic user-visible label.
- G-N6. Moving pane-label allocation into this service. Pane labels stay
  client-local and lowest-free (design artifact, "Pane labels"). r3 does require
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
- G-N9. WSS/TLS for the allocator link in v1. It runs on the fleet network
  (normally Tailscale), consistent with the v1 `ws` scheme in `DESIGN.md` §3.
- G-N10. Cryptographic authentication of claims, forgery/replay/timing
  defenses, or any hardening beyond the one-operator trusted-tailnet threat
  model. The `authorityId` is a distinguishing key, not a credential; the
  allocator does not authenticate it. Adding such hardening is a separate
  operator decision, out of v1 scope (see OQ-3).

---

## Terms

Each load-bearing term, what it denotes, and where it lives.

- **Fleet** — the set of Surf Ace surface clients (Electron and iOS) that a
  single user addresses as one namespace. All of them share one window-label
  space.
- **Fleet coordinator** — the one explicitly configured, always-on host that
  runs the window-label allocator process. Normally the host that runs the
  OpenClaw gateway (design artifact, "Decision").
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
- **Allocator identity** (`allocatorId`) — a stable identifier minted once when a
  fleet's allocator state is first initialized, carried in every response and in
  every client provenance record. It names *which allocator state generation*
  issued a label. Format: `alloc_` followed by 3–64 characters from
  `[A-Za-z0-9._:-]`.
- **State-format version** (`stateVersion`) — the integer schema version of the
  allocator's persisted state, present in state and in responses.
- **Client authority identity** (`authorityId`) — a durable, fleet-unique
  identifier for one client's surface authority (the Electron
  `lockless-client-authority` or the iOS `SurfAceLocklessAuthority` instance).
  Minted once with UUID-grade entropy the first time an authority needs it,
  persisted in that authority's durable state, and never reused across distinct
  installs. Format: `auth_` followed by 22–64 characters from
  `[A-Za-z0-9._:-]`. It exists because `surfaceId` is **not** fleet-unique
  (Assumptions A-6): two independent clients can mint the same client-local
  `surfaceId`, so `surfaceId` alone cannot key a fleet-wide assignment.
  `authorityId` is an internal allocation key only; it is never displayed and is
  never part of a window label (G-N5).
- **Fleet surface key** — the pair `(authorityId, surfaceId)`. This is the
  fleet-unique immutable key of an assignment. Two physically distinct surfaces
  always have distinct fleet surface keys because distinct authorities have
  distinct `authorityId`s, even if their client-local `surfaceId`s collide.
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
- **High-water ordinal** (`highWater`) — a durable, strictly monotonic
  non-decreasing integer recording the highest ordinal the allocator has ever
  committed, stored **outside** the restorable state generation (its own
  fenced record). It is never rolled back by a state restore. It fences ordinal
  reuse across restore of an older backup (Invariants INV-3, INV-13).
- **Allocator provenance** — the record a client persists per surface proving a
  window label was durably issued by the configured allocator:
  `{ fleetId, allocatorId, stateVersion, authorityId, surfaceId, ordinal,
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
  pane token is `windowLabel + paneLabel`. r3 requires iOS pane allocation to be
  lowest-free like Electron (INV-11).
- **Atomic persistent-state pattern** — the repository's existing durable-write
  pattern (`packages/electron/src/persistent-state-file.ts`): write and fsync a
  complete next generation, atomically replace the accepted generation, then
  proceed, with an explicit **unknown/ambiguous** outcome
  (`PersistentStateOutcomeUnknownError`, the `ambiguous-persistence` startup
  guard) when a replace neither clearly succeeded nor clearly failed. This spec
  reuses that pattern including its unknown outcome (INV-5, INV-14) and does not
  define a new one.

---

## Assumptions

Indicative givens this spec relies on. If one is false, raise it before building.

- A-1. Exactly one always-on host can be designated the fleet coordinator, and
  it can run a resident process reachable by every client. (Design artifact
  states this as the chosen shape.)
- A-2. Every client can reach the coordinator over the fleet network (normally
  Tailscale) at a configured WebSocket URL.
- A-3. The repository already provides an atomic persistent-state pattern with
  fsync-before-replace semantics AND an explicit unknown/ambiguous outcome,
  usable by the allocator process (`packages/electron/src/persistent-state-file.ts`:
  `PersistentStateOutcomeUnknownError`, `ambiguous-persistence` guard).
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

---

## Invariants

Normative. Every implementation MUST satisfy every invariant. Invariants come
first because a failure of any one reintroduces the exact defect this work
exists to remove.

- INV-1. **One allocator fleet-wide, enforced structurally.** At most one
  process is the writer of window labels for a fleet. This is enforced not by
  convention but by an exclusive, OS-level single-writer lock on the allocator
  state (REQ-D7): a second allocator process cannot acquire the lock and fails
  closed at startup. Clients hold exactly one configured allocator endpoint, one
  configured `fleetId`, and one configured/learned `allocatorId`. There is no
  election and no fallback writer in v1. (Requirement "What must be built" 1;
  design artifact "Decision".)
- INV-2. **Fleet-unique window labels.** No two distinct fleet surface keys
  under one `allocatorId` ever hold the same `windowLabel`, and no two live
  surfaces across the fleet ever display the same window label. (Core invariant;
  requirement "The requirement".)
- INV-3. **Monotonic, no reuse, fenced across restore.** The allocator issues
  ordinals strictly increasing from the high-water ordinal (INV-13), never below
  it. A committed ordinal is never issued again — across restarts, corruption
  recovery, surface close, AND restore of any older backup. (Design artifact
  "Authority and allocation", "Persistence and recovery"; review B-04.)
- INV-4. **Immutable assignment.** Once committed, an assignment
  `(authorityId, surfaceId) -> { ordinal, windowLabel }` never changes. A repeat
  claim for the same fleet surface key returns the same assignment. (Design
  artifact "Authority and allocation".)
- INV-5. **Durable-before-reply, with an explicit unknown outcome.** The
  allocator commits the new next-ordinal, the new mapping, and the advanced
  high-water using the atomic persistent-state pattern before it sends any
  success reply. A commit has exactly three outcomes: committed (reply success),
  clearly-not-committed (reply `persistence_failed`, no state change), or
  **unknown/ambiguous** (reply nothing that implies not-committed; enter the
  fail-closed unknown state of INV-14). A crash after commit and before reply
  loses no label and creates no duplicate, because the next claim for that fleet
  surface key returns the committed mapping. (Design artifact; review B-05;
  acceptance AC-8, AC-8b.)
- INV-6. **Fail closed.** An initialized allocator whose state is missing,
  unreadable, corrupt, of an unsupported `stateVersion`, internally
  inconsistent, in the unknown-persistence state (INV-14), or unable to acquire
  its single-writer lock (INV-1) MUST refuse to serve claims and MUST NOT
  silently start a new sequence. It returns an error and requires an operator to
  restore a verified backup or explicitly initialize a new fleet. (Design
  artifact "Persistence and recovery".)
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
  records a durable issue (`committed: true`). A bare persisted `windowLabel`, or
  provenance for a different fleet or allocator identity, is a legacy label and
  its surface is unaddressable until it claims. Live re-confirmation on restart is
  governed by one rule, with the settled fail-closed rule (INV-6) as the higher
  priority when they tension:
  - if the allocator is reachable at restart, the client MUST re-confirm each
    provenanced surface with an idempotent claim (REQ-B3) before admitting it as
    addressable; re-confirmation catches an allocator re-initialized under a new
    identity (identity mismatch -> unaddressable) or any divergence, and for a
    still-valid assignment returns the identical immutable mapping;
  - if the allocator is unreachable at restart, the client MAY admit a
    provenanced surface as addressable WITHOUT a live round-trip only because the
    assignment is immutable (INV-4) and never reused (INV-3), and only when its
    provenance `fleetId` and `allocatorId` equal the configured fleet and
    allocator identity and it is `committed`; otherwise the surface stays
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
  one fleet surface key return one stable assignment. Concurrent claims for
  different fleet surface keys are serialized by the single writer and receive
  different labels. (Design artifact "Authority and allocation".)
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
  load, the allocator acquires its single-writer lock (INV-1) and validates its
  state, and either passes all checks in Architecture §D or fails closed per
  INV-6. There is no partial-serve state.
- INV-13. **High-water fence never rolls back.** The high-water ordinal is
  persisted outside the restorable state generation and only ever increases. The
  allocator issues the next ordinal as `highWater` and advances `highWater` by
  one atomically with the assignment commit. Restoring an older state generation
  restores older mappings but never lowers `highWater`, so no restore reissues an
  ordinal that was ever committed. (Review B-04.)
- INV-14. **Unknown persistence fails closed until resolved.** If a commit's
  durability is unknown/ambiguous (INV-5), the allocator MUST NOT reply success
  and MUST NOT reply a clean `persistence_failed` (which would assert
  not-committed). It enters a fail-closed unknown state, stops serving claims,
  returns `persistence_outcome_unknown`, and requires a startup re-read /
  operator resolution (the repository `ambiguous-persistence` guard) to
  determine the accepted generation before serving again. (Review B-05.)
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
- REQ-A5. Each client authority holds a durable `authorityId` (Terms). If none
  exists, the authority mints one with UUID-grade entropy and persists it before
  its first claim. The `authorityId` is stable across restarts and is sent on
  every claim (REQ-C1). Distinct installs never share an `authorityId`. (Review
  B-02.)

### D-B. Authority and allocation semantics

- REQ-B1. The allocator owns four pieces of state: one monotonically increasing
  next-ordinal counter; one immutable `(authorityId, surfaceId) ->
  { ordinal, windowLabel }` map; one stable `{ fleetId, allocatorId,
  stateVersion }` header; and one fenced `highWater` (INV-13, stored outside the
  restorable generation). (Design artifact "Authority and allocation"; review
  B-02, B-04.)
- REQ-B2. On a claim for a fleet surface key with no existing assignment, the
  allocator takes `n = highWater`, computes `windowLabel = base26(n)`, records
  the mapping under `(authorityId, surfaceId)`, sets next-ordinal to `n+1`,
  advances `highWater` to `n+1`, commits durably (INV-5, INV-13), then replies
  with `{ ordinal: n, windowLabel }`. `next-ordinal` and `highWater` are equal in
  normal operation and diverge only transiently under an older-backup restore,
  where `highWater` governs issuance (INV-13).
- REQ-B3. On a claim for a fleet surface key that already has an assignment, the
  allocator replies with the existing assignment and commits nothing. (INV-4,
  INV-10.)
- REQ-B4. The allocator never searches for a locally unused label and never
  reuses a label. Closing a surface does not free its label in v1. (INV-3;
  design artifact "Persistence and recovery", "Migration".)
- REQ-B5. A single writer serializes all mutating claims so that two different
  fleet surface keys can never be assigned the same ordinal. (INV-10.)
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

### D-C. WebSocket protocol

The allocator is a WebSocket server; surface clients are WebSocket clients to
it. Encoding and correlation follow `DESIGN.md` §5 exactly: UTF-8 JSON text
frames; every message carries `v`, `type`, `op`, `id`, `sentAt`; requests and
responses carry a `payload`; error responses carry `error` with `ok: false`;
per-connection unique request `id`; last-1024 idempotent replay cache.

**Schema delta to `DESIGN.md` §5 / §10.** This spec adds one op, `label.claim`,
to the request/response op set and to the `ErrorResponse.op` enum (`DESIGN.md`
§10 `ErrorResponse`), and adds one response-level error code,
`window_label_unavailable`, to the surface error set (§8.1). No other envelope
convention changes.

- REQ-C1. **Claim request** (client -> allocator), conforming to `DESIGN.md` §5
  request envelope:
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
      "surfaceId": "sf_...",
      "expectedAllocatorId": "alloc_..."
    }
  }
  ```
  `expectedAllocatorId` is omitted only on genuine first contact before any
  identity is known; `fleetId`, `authorityId`, and `surfaceId` are always
  present.
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
      "surfaceId": "sf_...",
      "ordinal": 0,
      "windowLabel": "a",
      "committed": true
    }
  }
  ```
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
      "message": "<bounded human string, <=512 UTF-8 bytes>",
      "allocatorId": "alloc_..."
    }
  }
  ```
  `error.allocatorId` is present when the allocator identity is known.
- REQ-C4. Idempotency and request-id reuse follow `DESIGN.md` §5.3 exactly:
  - a duplicate request `id` with an identical payload returns the original
    response from the last-1024 replay cache (§5.3.2–3);
  - a duplicate request `id` with a different payload returns
    `invalid_request_id_reuse` (§5.3.4);
  - independently, the fleet-surface-key-keyed immutable assignment (REQ-B3)
    makes any claim for an already-assigned key return the same label regardless
    of connection or request `id`. This is the correctness guarantee across
    reconnects; the replay cache is the transport-level guard.
- REQ-C5. Allocator error `code` values (`[a-z_]{1,64}`) inside `error.code`:
  - `invalid_request` — request envelope shape or type invalid (per §5 envelope
    validation).
  - `invalid_request_id_reuse` — request `id` reused with a different payload
    (§5.3.4).
  - `unsupported_protocol_version` — `payload.protocolVersion` not supported.
  - `fleet_identity_mismatch` — `payload.fleetId` is not this allocator's fleet.
  - `allocator_identity_mismatch` — `expectedAllocatorId` present and not equal
    to this allocator's identity.
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
  - `rate_limited` — temporary throttle; the client retries with backoff.
  - `internal_error` — unhandled allocator error, including the residual
    collision safety net (REQ-B7).
- REQ-C6. The client MUST reject a response whose `id` does not match a request
  it sent on that connection, whose `payload.surfaceId`/`payload.authorityId` do
  not equal the pair it claimed, whose `fleetId` or `allocatorId` does not match
  the configured/expected values (once known), or whose `windowLabel` does not
  decode to `ordinal` under REQ-B6. A rejected response leaves the surface
  unaddressable and is reported through diagnostics (REQ-H3).
- REQ-C7. **New surface-protocol error code and the unaddressable operation
  matrix.** Add `window_label_unavailable` to the `DESIGN.md` §8.1
  response-level error set. A surface client applies the following matrix by
  concrete op when a targeted surface has no valid window-label assignment
  (unaddressable). The matrix is exhaustive over the §10 `ErrorResponse.op` set
  plus label-resolution:

  | Operation (concrete) | On an unaddressable surface |
  |---|---|
  | Label resolution ("window b" -> surface, at controller/OpenClaw) | FAILS: the surface is absent from the addressable projection, so the label does not resolve; caller sees `window_label_unavailable`. |
  | `surfaces.list` | ALLOWED (inspection): the surface appears with `windowLabel: null`, `addressable: false` (schema delta below). |
  | `panes.list` | ALLOWED (inspection). |
  | `heartbeat.ping` | ALLOWED (liveness/inspection). |
  | `label.claim` (recovery) | ALLOWED (this is the positive recovery path to become addressable). |
  | Diagnostics read (§D-H) | ALLOWED (inspection). |
  | `pair.request` | REJECTED with `window_label_unavailable`. |
  | `content.set` / `content.append` / `content.patch` / `content.clear` | REJECTED with `window_label_unavailable`. |
  | `annotations.remove` (and other annotation writes) | REJECTED with `window_label_unavailable`. |
  | `snapshot.get` / capture | REJECTED with `window_label_unavailable`. |
  | `pane.split` / `pane.rename` / `pane.close` (topology) | REJECTED with `window_label_unavailable`. |

  A surface becomes addressable only after a committed claim and persisted
  provenance (REQ-E2); the ALLOWED inspection/recovery rows are exactly the
  positive path an operator uses to see why a surface is dark and drive it to
  addressable. (Design artifact "Client behavior" line 50; review B-08.)

  **Projection schema delta (`DESIGN.md` §10 `SurfacesListResponse`).** Each
  element of `payload.surfaces[]` gains two required fields:
  - `windowLabel`: `string | null` — the assigned label, or `null` when the
    surface is unaddressable;
  - `addressable`: `boolean` — `true` only when the surface holds a valid
    assignment and may be resolved by label.
  These are additive; existing `surfaceId`, `name`, `viewport`, `paired` fields
  are unchanged. An unaddressable surface is always
  `{ windowLabel: null, addressable: false }`.

### D-D. Persistence, atomic commit, and startup validation

- REQ-D1. Allocator state lives in one dedicated state file on the coordinator,
  holding `{ fleetId, allocatorId, stateVersion, nextOrdinal, mappings[] }`
  where each mapping is `{ authorityId, surfaceId, ordinal, windowLabel }`. The
  `highWater` fence is persisted in its own durable record outside this state
  generation (INV-13). (Design artifact "Persistence and recovery"; review
  B-02, B-04.)
- REQ-D2. Every mutation uses the atomic persistent-state pattern: build and
  fsync a complete next generation, atomically replace the accepted generation,
  then reply. A partially written generation is never the accepted generation.
  The `highWater` fence is advanced durably before or atomically with the
  assignment commit so a crash cannot leave `highWater` below a committed
  ordinal.
- REQ-D3. On load, before serving any claim (INV-12), the allocator validates
  all of:
  - the header `{ fleetId, allocatorId, stateVersion }` is present and
    `stateVersion` is supported;
  - every `(authorityId, surfaceId)` maps to exactly one label;
  - every `windowLabel` belongs to exactly one fleet surface key;
  - every `windowLabel` decodes (REQ-B6) to its recorded `ordinal`, and every
    recorded `ordinal` is `< nextOrdinal`;
  - no two mappings share an `ordinal`;
  - `nextOrdinal` is strictly greater than every committed `ordinal`;
  - the `highWater` fence is present and `>= nextOrdinal - 1` and `>=` every
    committed `ordinal` (a loaded generation whose ordinals exceed `highWater`
    is corrupt).
  (Design artifact "Persistence and recovery"; review B-04.)
- REQ-D4. If any REQ-D3 check fails, or the file is missing on an allocator that
  has been initialized, or unreadable, the allocator fails closed (INV-6):
  returns `allocator_state_corrupt`, `allocator_state_unsupported_version`, or
  `allocator_uninitialized` as applicable, serves no claim, and does not create a
  new sequence.
- REQ-D5. On a claim commit, the allocator distinguishes three outcomes (INV-5):
  - **committed** — reply success (REQ-C2);
  - **clearly not committed** — send no success reply, expose no uncommitted
    mapping, leave `nextOrdinal` and `highWater` unchanged, and return
    `persistence_failed` (the client MUST retry);
  - **unknown/ambiguous** — the durable replace neither clearly succeeded nor
    clearly failed (repository `PersistentStateOutcomeUnknownError`): send no
    reply that implies not-committed, return `persistence_outcome_unknown`, and
    enter the fail-closed unknown state (INV-14, REQ-D8).
  (INV-5; review B-05; acceptance AC-8, AC-8b.)
- REQ-D6. A restart resumes issuing ordinals strictly above the high-water fence
  (INV-3, INV-13), so no restart, and no restore of an older backup, reuses or
  skips-into a committed label.
- REQ-D7. **Single-writer lock.** At startup, before serving, the allocator
  acquires an exclusive OS-level lock on its state (for example an advisory file
  lock or equivalent single-holder lease). If the lock cannot be acquired, a
  writer is already running: the second process fails closed (INV-1, INV-6) and
  does not serve. The lock is held for the process lifetime and released on exit.
  This makes two concurrent writers structurally unrepresentable rather than
  merely discouraged. (Review B-06.)
- REQ-D8. **Unknown-persistence resolution.** While in the unknown state
  (INV-14) the allocator serves no claim and returns
  `persistence_outcome_unknown`. Resolution is the repository
  `ambiguous-persistence` startup path: re-read durable state, determine which
  generation is the accepted one, advance or confirm `highWater`, and either
  resume serving (if a consistent accepted generation is found and passes REQ-D3)
  or remain fail-closed for operator restore (INV-6). Resolution never issues a
  label below `highWater`. (Review B-05.)

### D-E. Client behavior: provenance, fail-closed addressability, reconnect

- REQ-E1. Client per-surface state records allocator provenance
  `{ fleetId, allocatorId, stateVersion, authorityId, surfaceId, ordinal,
  windowLabel, committed: true }` alongside the surface, written only after the
  client observes a durably committed success (REQ-C2). A `windowLabel` with no
  matching provenance, with provenance for another `fleetId` or a non-configured
  `allocatorId`, or with no `committed` mark is a legacy label and is not
  authoritative (INV-9).
- REQ-E2. On surface open or restore, before exposing the surface as
  addressable, the client obtains or confirms an authoritative assignment, with
  fail-closed (INV-6) as the higher priority (INV-9):
  - if it has no valid provenance (none, wrong fleet, wrong identity, or
    uncommitted), it issues `label.claim(fleetId, authorityId, surfaceId)` and,
    on a committed success, persists provenance (REQ-E1) *before* admitting the
    surface as addressable (INV-7);
  - if it holds valid provenance AND the allocator is reachable, it MUST
    re-confirm with an idempotent claim before admitting the surface; the
    re-confirm returns the identical assignment (INV-4) for a valid surface, or a
    fleet/identity/assignment mismatch, which keeps the surface unaddressable;
  - if it holds valid provenance AND the allocator is unreachable, it MAY admit
    the surface as addressable using the persisted assignment (INV-9), then
    re-confirm in the background when reachability returns and drop the surface
    to unaddressable at once on any mismatch. A background re-confirm never
    downgrades a surface whose assignment still matches.
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
  with bounded backoff and re-claims per REQ-E2; because claims are idempotent by
  fleet surface key (REQ-C4), reconnect never changes an assigned label. Ordinary
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
  provenance. Restoring the same fleet surface key claims (and therefore
  receives) the same label (INV-4). Closing a surface does not free its label in
  v1 (INV-3). (Design artifact "Migration".)

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
  `stateVersion`, `nextOrdinal`, `highWater`, total assignment count, last
  successful commit time, current serve status (`serving`, or a fail-closed
  reason from INV-6 including `unknown-persistence` and `lock-held-elsewhere`),
  and uptime. Read-only; carries no authority.
- REQ-H2. Each client publishes per-surface label diagnostics: whether the
  surface is addressable, its `windowLabel` (or null), the configured allocator
  URL, configured `fleetId`, expected `allocatorId`, this authority's
  `authorityId`, last claim attempt time, last error code, and current backoff.
  These surface through the existing `surf_ace_authority_diagnostics` tool path
  (`DESIGN.md` §14.3).
- REQ-H3. A client that rejects an allocator response (REQ-C6) records the
  rejection reason in diagnostics; a rejected response never silently becomes an
  addressable label.

### D-I. Operator: initialization, backup, restore

- REQ-I1. **Initialize (new fleet only).** An explicit operator action creates a
  new fleet: it writes an initial state with a freshly minted `allocatorId`, the
  configured `fleetId`, the current `stateVersion`, `nextOrdinal = 0`, no
  mappings, and `highWater = 0`. Initialization refuses to run if committed
  allocator state already exists, so it cannot silently reset a live fleet. It is
  **not** a recovery for a lost/corrupt allocator (INV-15); its runbook requires
  every client to be drained of prior provenance first, because an offline client
  holding old provenance would otherwise display a label the new fleet reissues.
  (Design artifact "Persistence and recovery"; review B-03.)
- REQ-I2. **Backup.** Because every mutation atomically replaces a complete
  accepted generation (REQ-D2), the accepted state file is always internally
  consistent; a backup is a copy of that accepted generation. The `highWater`
  fence is captured with each backup for diagnostics, but on restore the **live**
  fence governs and is never lowered by a restored value (INV-13).
- REQ-I3. **Restore (same identity, fenced).** An operator restores by placing a
  verified backup as the allocator state and starting the allocator, which
  validates it on load (REQ-D3) and fails closed if it does not pass (INV-6).
  Restoring does not reset `allocatorId`; the same fleet identity and label
  assignments return, so clients with matching provenance stay addressable.
  Restoring an **older** backup (fewer mappings) never lowers `highWater`, so no
  ordinal that was ever committed is reissued; a surface created after the backup
  and missing from it is treated as new on its next claim and receives an ordinal
  above `highWater` — it may be **relabeled** (a named, accepted consequence of
  data loss) but is never **duplicated**. (INV-3, INV-13; review B-04.)
- REQ-I4. On missing or failed state, the allocator does not self-heal by
  creating a new sequence; the only recovery is REQ-I3 (restore the same fleet,
  fenced). REQ-I1 (new fleet) is reserved for a genuinely new or fully drained
  fleet (INV-15). (INV-6.)

### Split-brain safety argument (why v1 needs no election)

By INV-1 there is exactly one configured allocator endpoint and — enforced by the
single-writer lock (REQ-D7) — exactly one durable writer, with no fallback
(G-N2). Two surfaces can be assigned the same label only if (a) two writers each
advance a counter over the same symbol set, which the exclusive lock makes
structurally impossible; or (b) one writer reissues an ordinal, which the
high-water fence (INV-13) makes impossible across restart and restore; or (c) a
client trusts a label from the wrong authority, which the fleet/allocator
identity checks (INV-9, REQ-A4, REQ-C6) and the ban on new-identity hot
re-initialization (INV-15) prevent; or (d) two physical surfaces share an
assignment key, which the fleet surface key (Terms, A-6) prevents. The design
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
  authorities **with distinct `authorityId`s** configured to one real running
  allocator, When both concurrently claim labels for many `surfaceId`s
  **including deliberately colliding client-local `surfaceId`s (for example both
  authorities' `sf_0000000000000001`)**, Then every returned `windowLabel` is
  distinct and the test FAILS if any two authorities ever receive or display the
  same window label. (INV-2, A-6; requirement "What must be built" 3; review
  B-02.)
- AC-2 (proof 2). Given one fleet surface key, When a client issues repeated and
  concurrent `label.claim` calls for it, Then every response carries the same
  `ordinal` and `windowLabel` and the allocator committed exactly one mapping.
  (INV-4, INV-10.)
- AC-3 (proof 3). Given an allocator with committed assignments, When the
  allocator process restarts, Then every prior mapping is preserved and the next
  new claim receives an ordinal strictly greater than the high-water fence, with
  no reuse. (INV-3, INV-5, INV-13, REQ-D6.)
- AC-4 (proof 4). Given a client holding an allocator-issued label with valid
  provenance (configured fleet and identity, `committed`), When the client
  restarts with the allocator reachable, Then it live-re-confirms with an
  idempotent claim before admitting the surface, keeps the same window label, and
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
  assignment and an unavailable allocator, When a controller exercises each op in
  the D-C matrix, Then `surfaces.list`/`panes.list`/`heartbeat.ping`/`label.claim`/
  diagnostics are ALLOWED and the surface appears with `windowLabel: null,
  addressable: false`, while `pair.request`/content.*/annotations.*/`snapshot.get`/
  pane.* and label resolution are REJECTED with `window_label_unavailable`; and
  When the allocator becomes available and returns a committed assignment, Then
  the surface becomes addressable only after the client persists provenance.
  (INV-7, INV-8, REQ-C7, REQ-E2, REQ-E3; review B-08.)
- AC-6 (proof 6 — legacy duplicates). Given two clients each starting with the
  same legacy `windowLabel` and no provenance, When both migrate against one
  allocator, Then each receives a different fleet label and no two live surfaces
  display the same label. (INV-2, INV-9, REQ-F1, REQ-F2.)
- AC-7 (proof 7 — fail closed on corruption). Given an initialized allocator
  whose state file is corrupted, of an unsupported version, or missing, When it
  loads, Then it fails closed, serves no claim, returns the applicable
  `allocator_state_*` / `allocator_uninitialized` code, and never resets or
  advances the sequence. (INV-6, INV-12, REQ-D3, REQ-D4.)
- AC-8 (proof 8 — persistence failure). Given a claim whose durable commit is
  forced to **clearly fail**, When the client claims, Then no success reply is
  sent, no uncommitted mapping is exposed, `nextOrdinal` and `highWater` are
  unchanged, and the client receives `persistence_failed`; a subsequent
  successful claim for that fleet surface key then commits exactly one mapping.
  (INV-5, REQ-D5.)
- AC-8b (persistence unknown/ambiguous — the B-05 hole). Given a claim whose
  durable commit is forced into the **unknown/ambiguous** outcome (repository
  `PersistentStateOutcomeUnknownError`), When the client claims, Then the
  allocator sends no reply implying not-committed, returns
  `persistence_outcome_unknown`, and serves no further claim until the
  `ambiguous-persistence` resolution (REQ-D8) determines the accepted generation;
  And after resolution, the fleet surface key resolves to exactly one committed
  mapping with no duplicate and no reused ordinal. (INV-5, INV-14, REQ-D5, REQ-D8;
  review B-05.)
- AC-8c (single-writer lock — the B-06 hole). Given one allocator running and
  holding its state lock, When a second allocator process is started against the
  same state, Then the second fails closed at startup (cannot acquire the lock,
  status `lock-held-elsewhere`) and serves no claim; And Given a client
  configured with a `fleetId`/`allocatorId` that does not match an endpoint it is
  pointed at, When it claims, Then it is rejected
  (`fleet_identity_mismatch`/`allocator_identity_mismatch`) and the surface stays
  unaddressable rather than acquiring a second label space. The test FAILS if two
  writers ever serve concurrently or a mismatched endpoint yields an addressable
  label. (INV-1, REQ-D7, REQ-A4; review B-06.)
- AC-8d (older-backup restore never reuses — the B-04 hole). Given an allocator
  that has committed ordinals up to `b` (highWater 2), When an operator restores
  an older backup whose latest committed ordinal is `a` (nextOrdinal 1) and
  starts the allocator, Then the live `highWater` is not lowered, the next new
  claim receives `c` (never `b`), and a surface that had `b` and is missing from
  the backup is relabeled above `highWater` on reconnect but no two live surfaces
  ever share a label. The test FAILS on any reissue of `b`. (INV-3, INV-13,
  REQ-I3; review B-04.)
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
- AC-11 (fleet acceptance run). Given at least two clients with distinct
  `authorityId`s against one allocator, When windows are created and restored
  concurrently and the allocator and both clients are restarted, Then inspecting
  the rendered overlays and the authoritative list output shows no two live
  surfaces with the same window label and no unlabeled surface that is
  addressable. The run is red if either condition is violated. (INV-2, INV-8;
  design artifact "Required proof" final paragraph.)

Fixture honesty: AC-1, AC-2, AC-6, AC-8c, AC-8d, and AC-11 MUST run against a
real allocator process and real client authorities, not a hand-written fixture,
because a fabricated "all-unique" fixture would pass while shipping the exact
broken behavior this work removes (requirement "How it was lost": no test
asserted the property, so every soak passed). AC-1 is the single mandatory test
called out in the requirement, and r3 strengthens it to include colliding
client-local `surfaceId`s (A-6).

---

## Open Questions

Marked holes. Each is ruled BLOCKING (its scope waits) or NON-BLOCKING (build
around it). The settled inputs decide the load-bearing choices; the questions
below are the residue the inputs left open.

- OQ-1 (NON-BLOCKING). **Backoff bounds and rate-limit thresholds.** The client
  retry backoff bounds (initial, max, jitter) and the allocator `rate_limited`
  threshold are not fixed by the inputs. Build with sensible bounded values
  (for example initial 0.5 s, cap 30 s, full jitter) and expose them as
  configuration. These bound waiting, not an outcome, so they do not gate
  correctness.
- OQ-2 (NON-BLOCKING). **`stateVersion` starting value and upgrade path.** v1
  starts at `stateVersion = 1`. A future schema change adds a versioned migration
  on load; v1 need only reject unsupported versions (REQ-D4). No cross-version
  migration is in v1 scope.
- OQ-3 (NON-BLOCKING). **Allocator authentication/authorization on the WS link.**
  v1 runs on the trusted fleet network (normally Tailscale) with no WSS (G-N9)
  and no claim authentication (G-N10); the `authorityId` is a distinguishing key,
  not a credential. Whether to add a shared-secret or WSS profile is a later
  hardening decision, out of v1 scope. Do not add it without an operator ruling.
  (Watch: this is exactly the kind of unrequested hardening the org guards
  against; leaving it out is deliberate.)
- OQ-4 (NON-BLOCKING). **Label reuse / compaction policy.** v1 never reuses a
  label (INV-3, G-N4). Whether a future version reclaims labels of long-dead
  surfaces is deferred; it needs its own no-ambiguity ruling because reuse can
  reintroduce a duplicate a user still has in mind. Not in v1 scope.
- OQ-5 (BLOCKING for the coordinator-selection step only, not for allocator or
  client code). **Which host is the fleet coordinator, its allocator URL, and the
  `fleetId` value.** The design fixes the *shape* (one configured always-on
  coordinator, normally the OpenClaw gateway host) but the concrete host, URL,
  and `fleetId` are operator configuration values. Allocator and client code
  build against configuration (REQ-A2, REQ-A3, REQ-A4) with no default; only the
  deployment/config step waits on the operator naming them. This does not block
  writing or reviewing the code.
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

## Review response (r3)

How each blocking finding of `art_99b70bbc` is closed. Per the subtraction
ratchet, each closure names why DELETE and ACCEPT lost when it chose ADD.

- **B-01 (custody / overwritten bytes).** Closed by process: r2's exact bytes are
  preserved in this workspace at `surf-ace-fleet-window-label-allocator.r2.md`
  (SHA-256 `137e0e8…`), r1 at `421f7cb…` is recorded in the artifact history, and
  r3 is authored as a **distinct** file, never overwriting a prior revision's
  path. Durable custody is a landing in the `tightbeam-specs` git repo (immutable
  via commit history) — requested below in the handoff; this seat cannot push.
  (DELETE/ACCEPT n/a: this is a custody-hygiene fix, not a mechanism.)
- **B-02 (`surfaceId` not fleet-unique).** Closed by ADD: the fleet surface key
  `(authorityId, surfaceId)` (Terms, A-6, REQ-A5, REQ-B1) plus a residual
  collision safety net (REQ-B7) and a collision-inclusive AC-1. ADD chosen
  because DELETE (drop the need for a key) is impossible — an assignment needs a
  key — and pure ACCEPT (detect collision and darken both surfaces) needlessly
  makes two legitimately-distinct surfaces unaddressable; the composed key keeps
  both addressable and distinct. The visible label stays a plain letter (G-N5).
  The deeper root fix (make `surfaceId` itself globally unique) is left to the
  owner as it touches identity/migration; noted, not taken, because the composed
  key closes the safety hole without changing `surfaceId`.
- **B-03 (cached provenance survives reinit).** Closed by DELETE: new-identity
  re-initialization is forbidden as a hot recovery path (INV-15, REQ-I1 guard,
  REQ-I4); the only recovery is same-identity restore. AC-4c proves no new
  identity can reissue a label while prior provenance may be displayed. DELETE
  chosen over ADD (an epoch/revocation channel to reach offline clients) because
  an offline client is by definition unreachable, so no revocation channel can be
  relied on; removing the dangerous path is both simpler and actually safe.
- **B-04 (older-backup restore reuses an ordinal).** Closed by ADD: the
  non-rollback high-water fence (INV-3, INV-13, REQ-B1/B2/D1/D2/D3/D6, REQ-I2/I3,
  AC-8d), stored outside the restorable generation. ADD chosen because DELETE
  (forbid restore of older backups) removes the only data-loss recovery, and
  ACCEPT (allow reuse) reintroduces the prohibited duplicate. The fence makes
  reuse unrepresentable while permitting restore; a post-backup surface may be
  relabeled (named, accepted) but never duplicated.
- **B-05 (persistence unknown outcome erased).** Closed by ADD, reusing an
  existing repository primitive: the explicit unknown/ambiguous outcome and
  fail-closed unknown state (INV-5, INV-14, REQ-D5, REQ-D8, error
  `persistence_outcome_unknown`, AC-8b). ADD chosen because ACCEPT (treat unknown
  as not-committed) can drop a committed label and, on retry against a
  half-committed state, risk a second mapping; DELETE (ignore the case) is the
  bug. This is reuse of `PersistentStateOutcomeUnknownError`/`ambiguous-persistence`,
  not new machinery.
- **B-06 (one endpoint ≠ one writer).** Closed by ADD at the make-unrepresentable
  rung: an exclusive OS single-writer lock (INV-1, REQ-D7) plus a fleet
  configuration identity (`fleetId`, Terms, REQ-A3/A4) and negative AC-8c. ADD
  chosen because the property (one writer) cannot be delivered by DELETE or
  ACCEPT — it needs an enforcement seam; the lock is the highest affordable rung
  (structural exclusion) over mere convention.
- **B-07 (envelopes contradict DESIGN §5).** Closed by rewrite to the pinned
  envelope: REQ-C1/C2/C3 now carry `v`, `type`, `op`, `id`, `sentAt`, and
  `payload`/`error` with `ok`; REQ-C4/C5 add `invalid_request_id_reuse` (§5.3.4);
  a schema delta adds `label.claim` to the op enums. (Conformance fix, no
  mechanism choice.)
- **B-08 (unaddressable boundary not decidable).** Closed by the concrete
  operation matrix and the projection schema delta in REQ-C7 (exact ALLOWED vs
  REJECTED ops, `windowLabel`/`addressable` fields on `SurfacesListResponse`) and
  the positive inspection/recovery path; AC-5 exercises the matrix. The deletion
  test now answers YES per op.
- **B-09 (migration misses writers).** Closed by the full seam inventory in
  REQ-F3 (Electron admission, tombstone, provider bootstrap/`topology.apply`,
  ws-server provider `topology.apply.windowLabel`; iOS open, tombstone, runtime
  restore) with provider/topology `windowLabel` demoted to a checked echo; AC-9
  verifies each seam. (Completeness fix.)
- **B-10 (pane labels not lowest-free on iOS).** Closed by scoping the bounded
  iOS correction to lowest-free (INV-11, REQ-G1, AC-10) and removing the false
  "unchanged on both" claim; the card-routing question is OQ-6. Authorized by the
  settled requirement doc, which names lowest-free as required — the iOS monotonic
  counter is a demonstrated bug against it, so the correction cites live
  authority, not tidiness.
