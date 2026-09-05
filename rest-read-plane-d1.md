# REST read plane D1 — transport foundation and six shared-seam resources

Status: build specification. Amendment status: FROZEN OWNER-DEATH SUCCESSOR
CANDIDATE FOR ONE FRESH LINKED INDEPENDENT REVIEW — cursor-signing
indeterminate-commit quarantine and recovery.
Authority: canonical REST r3 `art_971f45b5`,
reviewed SHA-256 `49b86ec874283c523001be7449b1e14aef47ca72932955445638ce6443aad754`;
the adopted six-resource contract `art_b1995a26` / fact 1093; reviewed
firehose tip `8e4a412f25950dae1e1f33af42c390a4707bcf89`; PO rulings
`att_2d3a8333` and `att_304a6d07`; and the reviewed canonical AU2 repair
required by `wi_b0a6f85f-3523-45bb-8d10-1a67a2ad02bb` /
`asg_cd74975c-70c4-479b-8e34-20f91ef44452`.

This is one bounded amendment to the cursor-authenticity seam. It serves
`wi_cb5734eb-c175-4815-8763-882d69dfa9bf` / `asg_3aa6cba1-d7cf-4859-81a7-41209df77991`.
Its authority inputs are the rejected D1 tip `af4c8b21d1173a23646434491e22700ce2b8b0e4`,
recovery review `att_1a124822-e5de-4cf2-ae20-c313e339856d` / report
`art_53518583`, missing-seam evidence `att_acef51b5-42d2-491a-8ce4-f88124374504` /
`art_c2b2ca17`, and the product-owner disposition
`att_df797c4a-083c-4a30-9e98-224a5a9900f3`. It changes design only and authorizes
no product edit, implementation, main landing, `specRef` change, D2/D3 work,
deployment, or release.

The durability amendment serves
`wi_d417a2dd-13a4-49c5-a285-917eca9fea03` /
`asg_29485a6f-b7a1-40ef-b701-b43ca6c01dfd`. Its authority inputs are the
exact-tip review `att_4cb0d3e7-33f4-46ff-8618-2f68d289ec83` / report
`art_ff237615`, the stop ruling
`att_8e52b146-5a2c-40c3-8599-ed797a41ab3a`, and the storage-contract evidence
`att_1a39c856-a23d-4ac9-a1c1-050fd32044d9` / `art_5516885a`. The first frozen
candidate review `att_1deac03d-e402-4194-93fe-10e76419fff6` / `art_8c009daf`
and disposition `att_47726348-adbf-4f5e-955c-72a6bbed036b` require only the
lifecycle and overlapping-mutation clarifications in this successor. It
changes only provisioning and rotation durability outcomes, the resulting
quarantine and recovery behavior, and their acceptance. It authorizes no
product edit, implementation, D1 route, D2/D3/CLI/firehose work, `specRef`
change, target, landing, deployment, or release.

The successor review `att_d4aba352-ce0a-41c8-bc8c-dba303fc85cd` / report
`art_ccf48b43` found one remaining case: mutation-admission owner death
after atomic publication and before a durability outcome. Product-owner
disposition `att_a4ff40b1-a065-4215-9969-269aa7d6e360` limits this revision to
that admitted-mutation failure boundary and its acceptance fixture.

## Spec homing

This file is the D1 build specification for
`wi_ed4f9020-3fb9-4ee1-9f8f-0cb2629fed96`. Its reviewed content hash, rather
than an unreviewed branch tip or a worktree copy, is the implementation
binding. A later D1 amendment replaces this file and receives a fresh exact
review before the work item binding changes.

Operating pattern taught to agents: none. This file specifies product storage
behavior; it does not amend the Tightbeam operating manual or agent guidance.

## Goal

Deliver deterministic REST collection and detail reads for config, host
environment, hosts, users, served identity, and kungfu. The REST transport
uses the one shared query, public serializer, and visibility seam assigned to
the resource. It adds no second data shape.

## Non-Goals

- D1 does not add a REST-local serializer, projection, public item field,
  credential, principal resolver, authorization grant, or tailnet identity
  behavior.
- D1 does not add a host-environment detail route, firehose class, primary
  reference, version source, firehose payload activation, CLI wire behavior,
  compatibility-alias removal, write route, deployment, or release behavior.
  M1 may migrate the existing identity CLI and firehose callers mechanically
  to the staged identity query contract below; their public bytes and behavior
  do not change.
- D1 does not start M3 through M8. M1 owns the shared seams; D1 is M2.
- This durability amendment does not add a key store, database row, authority
  pointer, journal, recovery marker, backup authority, fallback key, or old-key
  grace window. It does not weaken file or containing-directory durability.

## Terms

- **M1 seam**: the canonical `Tightbeam.StateResources` query and public
  serializer plus the canonical `Tightbeam.StateVisibility` predicate that M1
  freezes for one resource.
- **Transport adapter**: the existing `Tightbeam.Wire.Router` GET handling that
  parses a request, calls an M1 seam, and emits an R4 outer object. It owns no
  resource query, item projection, or item serializer.
- **Resolved principal**: the result from the existing gateway principal
  resolver after AU2 `asUser` transport handling.
- **Tuple cursor**: an opaque signed exclusive page boundary containing the
  resource, full immutable sort tuple, normalized filter fingerprint, and
  resolved-principal binding.
- **Identity descriptor**: a request-bound, authenticated, opaque capability
  returned by the metadata stage of `StateResources.query_identity/2`. It
  binds one identity name and exact resolved principal to one state source and
  observation version without containing, selecting, opening, or decoding the
  identity item payload.
- **Hydrated identity**: the closed internal identity row returned only by the
  authorized hydration stage of `StateResources.query_identity/2`. It is the
  only input that the pure `StateResources.identity/1` serializer accepts.
- **Request binding**: an ephemeral, unguessable operation identity minted by
  the existing REST, CLI, or firehose caller. It is not a credential,
  principal, authorization grant, durable row, or wire field. Its lifetime is
  exactly one synchronous logical read operation and ends before that caller
  returns, responds, or enqueues output.
- **Cursor-signing material**: exactly 32 cryptographically random octets held
  by the server for authenticating D1 cursors. It is not the bearer
  credential, a principal identifier, a request binding, a node cookie, or any
  value derived from a request.
- **Cursor-signing provider**: the internal capability owned by
  `Tightbeam.CursorSigning` that provisions, loads, rotates, recovers, signs,
  and verifies cursor-signing material. It is composed by
  `Tightbeam.Application`, injected by `Tightbeam.Gateway`, and consumed by
  `Tightbeam.Wire.Router`; no bearer client can supply or select it.
- **Publication boundary**: the filesystem event that makes a complete new
  canonical material record visible at `rest-cursor-signing.v1`. Provisioning
  publishes when the canonical entry becomes visible. Rotation publishes when
  the atomic rename completes.
- **Cursor-signing generation**: one complete 32-octet material value that the
  canonical file makes authoritative. The generation has no stored identifier,
  pointer, metadata record, or wire representation.
- **Cursor-signing unprovisioned state**: the provider state selected when
  startup classifies the canonical path as absent before listener admission.
  It admits only explicit local first provisioning while listener admission
  stays closed. Signing, verification, rotation, and recovery return
  `{:error, :cursor_signing_unprovisioned}`. This state covers both a fresh
  first boot and a restart on an absent canonical path; no durable history
  exists to distinguish those cases. A recovery failure never transitions a
  quarantined provider into this state.
- **Cursor-signing healthy state**: the provider state in which one validated
  canonical generation has passed containing-directory synchronization. It
  admits signing, verification, and explicit local rotation.
- **Indeterminate commit**: the single typed terminal outcome after publication
  when containing-directory synchronization fails. It states that canonical
  authority may have advanced. It is neither success nor an ordinary error.
- **Cursor-signing quarantine**: the provider state that admits only recovery.
  It refuses signing, verification, provisioning, and rotation across the
  application processes that share the canonical path.
- **Cursor-signing mutation admission**: the one ephemeral, cross-process
  admission seam shared by provision, rotate, and recovery for a canonical
  path. A provider-lifetime state observer owns this admission independently of
  the admitted mutation's per-operation owner process. It admits at most one
  mutation transition at a time and creates no durable file, marker,
  authority, or recovery input.
- **Published-but-unsynchronized phase**: the ephemeral mutation-observer state
  after successful atomic publication and before containing-directory
  synchronization establishes success or failure. The observer enters this
  phase at publication's linearization point and creates no durable phase
  marker or recovery input.
- **Canonical route key**: the fixed route-table key for the collection route
  that issued a cursor, such as `users.collection`. It is an internal signed
  binding, not a URL, query-string fragment, or response field.

## Assumptions

1. Canonical green `main` contains M1's six shared query, serializer, and
   visibility seams before a D1 product edit begins.
2. `asg_fd993fc7-43fd-401f-9433-190e07d5d7f1` is qualifying evidence for those
   M1 seams. It is not an M3 activation gate. If its landing combines M1 with
   active M3 payload wiring, the implementer waits for that landing or an
   M1-only integration split; D1 does not redefine SQ4.
3. A reviewed canonical correction for AU2 from `wi_b0a6f85f` /
   `asg_cd74975c` is a hard authority dependency. Before that correction is
   reviewed and present on canonical green `main`, D1 code does not start and
   no implementation selects session `asUser` behavior from this file.
4. The green M1 host visibility seam implements AU4: an authenticated org user
   or session can read hosts. The old admin-only implementation is not a D1
   authority source.

## Invariants

1. A D1 GET obtains resource data through the resource's single M1 query seam,
   evaluates that resource's shared visibility seam, and emits the result only
   through that resource's public serializer.
2. The router does not map a raw row, duplicate a collection query, define a
   REST-only projection, or append an item field.
3. Visibility precedes payload access, serialization, pagination, and response
   emission. The identity detail metadata stage precedes visibility but reads
   metadata only. Only a permitted caller performs the identity hydration
   stage. The public identity serializer performs no database or other I/O.
   Where one D1 detail resource mechanically has both an unknown and a
   forbidden case, those cases have the canonical identical `404 not_found`
   body, headers, statement shape, and timing class. Identity known `served`
   and unknown names both pass through the metadata stage of
   `StateResources.query_identity/2` before visibility.
4. A REST detail item has exactly its R7/R7a fields. For the six notice-backed
   resources, its serialized item bytes equal the corresponding firehose
   payload bytes after the outer object is removed.
5. Success and error responses carry `Cache-Control: no-store`. D1 emits no
   ETag and implements no conditional request behavior.
6. M1 freezes projections, R8 mappings, R9 dependencies, and AU4 visibility.
   M2 adds REST on those seams before M3 points firehose payload builders to
   the same serializers.
7. The canonical 32-octet file remains the sole cursor-signing authority.
   Quarantine and recovery create no second durable state or alternate
   authority.
8. A provisioning or rotation failure before publication returns an ordinary
   error and preserves the prior restart authority. A containing-directory
   synchronization failure after publication returns indeterminate commit and
   enters quarantine before the local owner caller receives that outcome.
9. The provider returns success only after it proves both the material-file
   flush and the containing-directory synchronization. It does not retry a
   failed post-publication directory synchronization inside the operation.
10. Recovery keeps the provider quarantined while it validates and synchronizes
    the sole canonical file. It re-enables exactly the validated generation in
    one step relative to signing, verification, provisioning, and rotation.
11. Startup classification of an absent canonical path selects the
    unprovisioned state with listener admission closed. Only explicit local
    first provisioning can leave that state; startup and recovery never
    generate material. A quarantined provider stays quarantined when recovery
    finds the canonical path absent.
12. Provision, rotate, and recovery share one indivisible cross-process
    mutation-admission decision. At most one such transition is admitted for a
    canonical path, and an overlapping mutation performs no material or
    namespace action.
13. The provider-lifetime state observer retains mutation admission
    independently of the per-operation owner process. If that owner dies in
    the published-but-unsynchronized phase, the observer establishes
    quarantine before it releases admission or exposes another lifecycle
    state.

## Architecture

### Code-start gates

The implementer proves both gates before editing product source:

1. Canonical green `main` contains the six M1 seams, with the M1 qualification
   described in Assumption 2.
2. Canonical green `main` contains the reviewed AU2 correction from
   `wi_b0a6f85f` / `asg_cd74975c`.

Failure of either gate stops D1 before a product edit. A private firehose tip,
an unreviewed AU2 repair branch, and an M3-only integration do not satisfy a
gate.

### Routes and the one resource seam

`Tightbeam.Wire.Router` owns route matching, shared request parsing, bearer
authentication reuse, cursor validation, the R4 outer envelope, canonical
errors, and cache headers. It invokes the M1 seam below. It does not introduce
`rest_read/3`, `list_<resource>/2`, a REST cursor module, a REST envelope
module, or another resource-shaped API.

M1 owns collection enumeration in the same resource query seam as detail. If
the reviewed M1 contract needs a collection-capable function clause or input,
M1 names and freezes it. D1 does not create a sibling `list_*` seam. The
following existing names are the canonical D1 resource names:

| Resource and routes | One shared query seam | Public serializer | Shared visibility | Allowed collection filters | Immutable ascending tuple |
|---|---|---|---|---|---|
| config: `/api/config`, `/api/config/:key` | `StateResources.query_config/2` | `StateResources.config/1` | `StateVisibility.config_visible?/1` | `key` exact | `(key)` |
| host environment: `/api/host-env` | `StateResources.query_host_environment/2`; `/4` remains the shared internal exact lookup, not an HTTP route | `StateResources.host_environment/1` | `StateVisibility.host_environment_visible?/1` | `host`, `harness`, `name` exact | `(host,harness,name)` |
| hosts: `/api/hosts`, `/api/hosts/:host` | `StateResources.query_host/2` | `StateResources.host/1` | `StateVisibility.host_visible?/1` | `host` exact | `(host)` |
| users: `/api/users`, `/api/users/:userId` | `StateResources.query_user/2` | `StateResources.user/1` | `StateVisibility.user_visible?/1` | `userId` exact | `(createdAt,userId)` |
| identity: `/api/identity`, `/api/identity/:name` | `StateResources.query_identity/2` | `StateResources.identity/1` | `StateVisibility.identity_visible?/1` | `name`, `state` exact | `(name)` |
| kungfu: `/api/kungfu`, `/api/kungfu/:name` | `StateResources.query_kungfu/2` | `StateResources.kungfu/1` | `StateVisibility.kungfu_visible?/1` | `status`, `rootArchetype` exact | `(name)` |

The host-environment route is one collection route. The three filters select
items from that collection; D1 exposes no `/:host/:harness/:name` detail
route. Identity detail accepts `served`; another name is absent. Both known
`served` and unknown identity names reuse the canonical
`StateResources.query_identity/2` seam before visibility. D1 adds no REST-local
or dummy identity query.

### Staged identity query contract

Identity exact-name reads use two explicit stages of the same public function.
The public surface is closed:

1. `StateResources.query_identity(source, {:metadata, name, request_binding,
   resolved_principal_binding})` returns `{:ok, identity_descriptor}` for every
   syntactically valid binary `name`, whether the name is present, absent, or
   forbidden to that resolved principal.
2. The caller evaluates `StateVisibility.identity_visible?/1` for that exact
   resolved principal. A denial ends the request with the canonical
   `404 not_found` response and does not invoke hydration.
3. Only a permitted caller invokes
   `StateResources.query_identity(source, {:hydrate, identity_descriptor,
   request_binding, resolved_principal_binding})`. It returns
   `{:ok, hydrated_identity}`, `:not_found`, `:stale`, or
   `{:error, :invalid_identity_descriptor}`.
4. Only `{:ok, hydrated_identity}` enters
   `StateResources.identity/1`. The serializer returns the existing closed R7
   identity object and performs zero I/O.

The map-filter collection clause remains part of
`StateResources.query_identity/2`; M1 adds no sibling list function. Because
identity visibility is resource-wide and admin-only, REST and CLI collection
callers evaluate `identity_visible?/1` before invoking the payload-bearing
collection clause. A denied collection therefore opens no identity payload.
An allowed collection keeps the existing filters, order, item bytes, and pure
serializer.

The binary detail form that returned a row or `nil` is not a second supported
mode after this amendment. M1 migrates exact-name callers to the tagged stages
above. It does not add `query_identity_metadata`, `hydrate_identity`, a
REST-local query, a dummy statement, a serializer query, or any other public
resource seam.

#### Metadata stage

The metadata stage performs exactly one canonical database statement for a
syntactically valid name. That statement:

- has byte-identical SQL shape and parameter count for known, unknown, and
  forbidden cases;
- returns exactly one database result row in every case;
- reads only the identity resource name, canonical primary key, publication
  row version or an inline absence sentinel, and the minimum source-generation
  metadata needed to bind the descriptor;
- does not select, return, compare, hash, open, copy, or decode the `item`
  column or any identity payload bytes; and
- does not read Git, the served-identity tree, a file, another database, or a
  process-local payload cache.

The one-row absence result is part of the real canonical metadata statement.
It is not a second or dummy query. The caller cannot distinguish a present
row from the absence sentinel because the function returns the same opaque
descriptor type and cardinality for both.

The state-source identity is the canonical identity of the database handle
used by the operation. Its source generation changes whenever that handle is
reopened, replaced, or rebound to different backing state. It is not derived
from the requested name or item payload.

The resolved-principal binding is the canonical principal kind and stable
principal identifier produced by the existing resolver, including the result
of AU2 `asUser` handling. It contains no bearer credential, session secret, or
authorization grant. The metadata stage authenticates this binding into the
descriptor without using it to vary the canonical database statement.

#### Descriptor authenticity and binding

The identity descriptor is an authenticated opaque capability. Its
representation exposes no fields through pattern matching, inspection, JSON,
logs, traces, exceptions, or firehose payloads. The authenticated content may
contain only:

- the fixed resource tag `identity`;
- the canonical requested name;
- a present-or-absent metadata tag and its observed publication row version;
- the exact state-source identity and source generation;
- the exact resolved-principal binding;
- the request binding and operation-issuance nonce; and
- the issuing process generation.

The descriptor contains no item bytes, decoded item field, item fingerprint,
file content, credential, principal grant, or reusable bearer authority. A
process-private descriptor key authenticates and conceals the content. The
key never crosses a process boundary and never enters durable state. A process
restart invalidates every outstanding descriptor.

A descriptor is valid for exactly the `identity` resource, requested name,
resolved principal, state source, source generation, request binding, and
process generation that issued it. It becomes a hydration witness only after
that same resolved principal passes `identity_visible?/1`. A descriptor cannot
hydrate kungfu, another identity name, another principal, another database, or
another request. Reuse within the same open bound operation by the same
principal is idempotent while the observed row version is unchanged. The
caller closes the operation binding before it returns, responds, or enqueues
output. Replay under a different principal or request binding, or after that
close, is an invalid descriptor, not a new lookup.

Authentication failure, malformed content, a wrong resource, a wrong source,
a wrong resolved principal, a wrong request binding, a closed operation, or
cross-process replay returns `{:error, :invalid_identity_descriptor}` before
database access. The caller records a loud internal
`identity_descriptor_invalid` fault without the raw descriptor,
name-presence tag, principal binding, or payload. A REST adapter emits the
closed `500 projection_invalid` error envelope and no partial response. Every
invalid descriptor case has that same response body and headers; descriptor
validity never becomes a name-existence answer.

#### Authorized hydration and row-version races

Hydration performs database work only after the shared visibility predicate
permits the exact resolved principal bound into the descriptor. Before any
database access, hydration compares the current resolved-principal binding to
that authenticated binding and rejects a mismatch as an invalid descriptor.
It then uses the authenticated resource, name, source, and observed version
from the descriptor. Its canonical statement returns one tagged outcome:

- `{:ok, hydrated_identity}` only when the same identity row still exists at
  the exact observed publication row version;
- `:not_found` only when an authenticated absence descriptor still observes
  absence; or
- `:stale` when a row appeared, disappeared, or changed version between the
  metadata and hydration stages.

Hydration never returns payload bytes from a row version that the metadata
stage did not observe. On `:stale`, the caller discards the descriptor and
restarts metadata, visibility, and hydration once with the same principal and
filters. A second `:stale` emits the canonical `404 not_found` response with
no partial item. A forbidden caller never reaches this race path. An unknown
authorized caller receives `:not_found`; an unknown or known forbidden caller
receives the same pre-hydration 404.

`StateResources.identity/1` accepts a hydrated identity row only. Passing an
identity descriptor, a source handle, or an unhydrated metadata row fails
closed. The serializer validates and orders the existing identity fields, but
it performs no database, transaction, process, file, Git, credential, or
network call and opens no stored JSON bytes.

#### Existing caller migration

M1 migrates callers without changing their public result:

- REST identity detail mints a request binding, binds the exact resolved
  principal into metadata, applies the shared visibility predicate to that
  same principal, hydrates through the same query function with both bindings
  when permitted, and passes only hydrated data to the pure serializer.
- REST identity collection applies the resource-wide visibility predicate
  before its existing map-filter query clause and pure serializer.
- The existing CLI identity-status read uses the same metadata, visibility,
  hydration, and serializer order. Its command, authorization, fields, and
  bytes remain unchanged.
- A firehose rebuild or ref-based identity read uses the same staged query and
  pure serializer. A committed publication path that already owns the exact
  hydrated public item may pass that item directly to the pure serializer
  after its existing committed-publication authorization; it does not create
  a descriptor or query inside the serializer. Firehose delivery still uses
  `identity_visible?/1` before emission, and notice payload bytes remain equal
  to REST item bytes.

No caller may retain a descriptor in an outbox, cursor, notice, process cache,
or durable row. No caller may expose a descriptor to an HTTP or CLI client.

### Envelopes, filters, order, and cursors

A collection response uses R4's `schemaVersion`, `resource`, `items`, and
`page` envelope. A detail response uses R4's `schemaVersion`, `resource`, and
`item` envelope. The resource strings are exactly `config`, `host environment`,
`hosts`, `users`, `identity`, and `kungfu`.

The filter table is closed. A key absent from its resource row returns
`400 invalid_filter`. A valid exact filter for a missing config, host,
host-environment, user, identity, or kungfu item returns an empty collection.
An unknown user id in `GET /api/users?userId=...` returns an empty collection,
not an existence error. Users accept no status or ownership filter. D1 has no
devices route; when that later route is added, `status` is only
`allowlisted`, `pending`, or `denied`, and `userId` is its ownership selector.
An invalid device status returns `400 invalid_filter`.

Repeated values for one allowed filter are OR. Values for distinct allowed
filters are AND. A malformed listed-filter value returns `400 invalid_filter`.

Rows sort by the full table tuple, oldest to newest. No cursor starts from the
oldest page. `before` and `after` are mutually exclusive exclusive bounds.
`limit` defaults to 50 and clamps at 500. Cursor validation checks encoding,
version, signature, resource, normalized filter fingerprint, and resolved
principal binding before a resource row lookup. The cursor carries no offset,
SQLite `rowid`, or live-row locator. A malformed, wrong-resource, or
changed-filter cursor returns `400 invalid_cursor`; a principal-binding
mismatch returns the canonical `404 not_found`.

### Canonical server-held cursor-signing seam

This amendment closes the D1 cursor-authenticity gap without changing a
resource query, item serializer, route, envelope, filter, or response field.
Every D1 cursor is authenticated by one `Tightbeam.CursorSigning` provider.
The provider uses HMAC-SHA-256 with the current server-held 32-octet material
and the fixed domain-separation prefix
`tightbeam/rest-read-plane-d1/cursor/v1\0`. The HMAC input is the existing
canonical opaque cursor body, with these bindings in its fixed D1 order: cursor
version, canonical route key, resource, exclusive page direction (`before` or
`after`), normalized filter fingerprint, complete immutable order tuple, and
exact resolved-principal kind and stable identifier. The signature is 32 octets
and remains inside the existing opaque cursor encoding. The key-generation
record is never a cursor field. Any version, route, resource, direction,
filter, tuple, or principal change therefore invalidates the signature or
produces the existing binding refusal; `limit` remains adjustable because D1
does not bind it.

#### Ownership, provisioning, and injection

`Tightbeam.CursorSigning` is the sole owner of signing material. Its canonical
durable location is `base_dir/secrets/rest-cursor-signing.v1`, a regular file
containing exactly 32 octets, with no text encoding, newline, metadata, or
second key. The containing directory is owner-only and the file mode is exactly
`0600`; the provider rejects symlinks, non-regular files, and a file not owned
by the service identity. A deployment that cannot enforce those permissions
fails closed.

Only the local gateway bootstrap, before the HTTP listener is admitted, may
invoke the provider's provisioning operation. Canonical-path absence selects
the unprovisioned state. The provider admits explicit first provisioning only
from that state and through the shared mutation-admission seam. It obtains 32
octets from the operating system CSPRNG, writes an owner-only same-directory
staging file, and durably flushes the complete record. It then publishes that
record at the canonical path with one exclusive atomic rename that refuses an
existing canonical entry. The staging file and canonical file use exact mode
`0600`. The staging file is not an authority and recovery never selects it.
The provider synchronizes the containing directory before it reports success
and atomically enters healthy state.
Provisioning never overwrites an existing file. A failure before publication
returns an ordinary error and leaves the service unprovisioned across restart.
A directory-synchronization failure after publication returns the
indeterminate-commit outcome defined below.

Normal `Tightbeam.Application` startup begins with listener admission closed and
classifies the canonical path through the shared mutation-admission seam. If
the path is absent, the provider enters unprovisioned state; explicit local
first provisioning is its sole legal transition, and recovery returns
`{:error, :cursor_signing_unprovisioned}`. If the canonical path is present,
the provider begins quarantined and performs startup recovery: it loads and
validates the file, synchronizes the containing directory, then atomically
enters healthy state and exposes that exact generation to the gateway before
it admits the listener. An unreadable, wrongly sized, otherwise malformed, or
unsynchronizable present file is a typed startup failure and leaves the
provider quarantined. Startup does not silently generate a replacement, serve
REST, or accept a cursor.

The application composition root creates the provider and passes its internal
capability through the existing gateway dependency map as `cursor_signing` to
every router instance. The router owns canonical cursor framing, binding
checks, HMAC invocation, and the existing AU7 error mapping. It owns no key
bytes, provisioning, rotation, fallback, or key store. `StateResources`, all
six query seams, all six public serializers, `StateVisibility`, and all
CLI/firehose callers are unchanged by this amendment.

#### Stability, rotation, and failure behavior

Each sign or verify operation reads one complete current material record through
the provider; it does not retain a key in a process dictionary, module
attribute, ETS table, `persistent_term`, Router state, request cache, or any
other process-local store. Atomic replacement makes every request process and
every OS process observe either the old complete record or the new complete
record. The transient bytes needed by one HMAC call are not an authority or a
cache. A missing `cursor_signing` capability or an unavailable material record
is never replaced by a dummy key, bearer-derived key, node cookie, runtime
value, or random per-request key.

Rotation is an explicit local operator maintenance operation owned by
`Tightbeam.CursorSigning`; it is not a REST route and cannot be requested by a
bearer client. The provider obtains fresh CSPRNG material, writes a same-
directory temporary file with exact mode `0600`, flushes it, and atomically
renames it over the active file. It then synchronizes the containing directory.
A successful return means the material-file flush and containing-directory
synchronization succeeded. It removes the old material from the verification
set at the rename boundary. A failure before that boundary returns an ordinary
error and leaves the old complete file and behavior unchanged. A
directory-synchronization failure after that boundary returns the
indeterminate-commit outcome defined below. Existing cursors issued before a
successful rotation are rejected as the existing `400 invalid_cursor`, before
a resource-row lookup. Cursors issued after a successful rotation verify with
the new material. There is no old-key grace window.

Provision, rotate, and recovery enter through the same mutation-admission seam.
The provider-lifetime state observer attempts exclusive cross-process mutation
admission before it evaluates the requested transition against the lifecycle
state or permits mutation I/O. The observer, not the admitted mutation's
per-operation owner process, owns that admission. It monitors that owner and
holds admission through establishment of the resulting lifecycle state and
return of the operation's one terminal outcome, or through establishment of
quarantine when owner death makes a return impossible. An overlapping
provision, rotate, or recovery call returns exactly
`{:error, :cursor_signing_mutation_in_progress}` to its
local owner caller before lifecycle validation, material read, CSPRNG access,
staging-file creation, or namespace mutation. It does not wait, queue, or retry
inside the provider. Thus no second mutation can publish after an earlier
mutation has returned success or entered quarantine.

Sign and verify operations linearize at their complete material read.
Concurrent operations before the rename use the old material and operations
after a successful directory synchronization use the new material; no
operation may combine bytes from two records. Before publication, the observer
closes sign and verify admission and waits for already admitted sign and verify
operations to finish their complete material read. From publication until the
directory synchronization returns, the provider admits no new sign or verify
operation across the application processes that share the canonical path.
Success releases that admission boundary onto the new generation. Failure
converts the same boundary to quarantine, so no operation can observe a healthy
provider between the failed synchronization and quarantine. The provider
releases exclusive mutation admission only after it atomically establishes
that resulting state across the application processes that share the canonical
path.

The provider-lifetime observer is the state observer for per-operation owner
death. It performs provision and rotation publication within its serialized
mutation transition. Successful atomic rename completion is the publication
linearization point. In the same serialized transition, before it permits the
directory-synchronization step, the observer enters the
published-but-unsynchronized phase. No owner-exit handling or admission release
can occur between rename completion and that phase entry. The per-operation
owner cannot release admission by exiting.

If the observer receives that owner's exit while the mutation is in the
published-but-unsynchronized phase, it linearizes owner-death handling by
transitioning directly from that phase to quarantine across the application
processes. It establishes quarantine before it releases mutation admission.
An in-flight or later directory-synchronization result from the abandoned
operation cannot establish success, ordinary error, healthy state, or another
generation. The dead owner receives no fabricated outcome. Calls made before
the quarantine transition completes remain outside mutation admission; calls
made after it completes observe the quarantine behavior below.

Owner-death quarantine uses only the canonical file for recovery. Restart or
explicit local owner recovery validates the complete record, successfully
synchronizes its containing directory, and atomically re-enables that exact
generation under the recovery contract below. This observer state creates no
durable record, authority, pointer, marker, journal, or alternate recovery
input. Owner death outside the published-but-unsynchronized phase is unchanged
by this amendment.

#### Indeterminate-commit quarantine and recovery

This named pattern applies only when provisioning or rotation publishes a
complete record and the following containing-directory synchronization fails.
It does not reclassify a pre-publication failure or a sign/verify read failure.
Canonical example: rotation rename succeeds, directory synchronization returns
an error, and the provider returns indeterminate commit from quarantine.

A post-publication containing-directory synchronization failure returns exactly
`{:indeterminate_commit, :cursor_signing_authority_may_have_advanced}` to the
local owner caller. Before it releases that outcome, the provider atomically
enters cursor-signing quarantine across the application processes that share
the canonical path. The provider does not translate this outcome to success,
an ordinary error, or an internal retry loop.

In quarantine, sign, verify, provision, and rotate calls return the typed
internal refusal `{:error, :cursor_signing_quarantined}` without reading key
bytes or performing a namespace mutation. A router that reaches this refusal
emits the existing `500 projection_invalid` envelope with
`Cache-Control: no-store` and no partial response. `Tightbeam.Gateway` checks
the provider state and admits each Router dispatch as one indivisible operation
relative to the quarantine transition. The quarantine transition does not
retroactively cancel a Router dispatch admitted before publication; a later
provider call from that dispatch still observes the current provider state. A
request not admitted before quarantine receives that closed response and
performs no resource-row lookup. The gateway does not cache a prior healthy
state or bypass the provider. No HTTP or bearer-client operation can invoke
recovery.

Recovery has two entry points: application startup on a present canonical path
before listener admission, and an explicit local owner operation on a
quarantined running provider. Both enter through the shared mutation-admission
seam and use only `base_dir/secrets/rest-cursor-signing.v1`. While the provider
stays quarantined, recovery validates one complete regular 32-octet record, its
exact `0600` mode, service ownership, and its owner-only containing directory.
Recovery then synchronizes that directory and proves that the same validated
record remains canonical. Only then does it atomically re-enable that exact
generation across the application processes that share the path.

A canonical file that disappears after present-path classification, is
malformed, is replaced during recovery, or cannot be synchronized returns
`{:error, :cursor_signing_recovery_refused}`. Startup remains refused or the
running provider remains quarantined. An absent path selected at startup is
unprovisioned instead and recovery returns
`{:error, :cursor_signing_unprovisioned}`; explicit local provisioning is its
sole legal transition. Recovery does not select a temporary file, database row,
pointer, journal, marker, backup, cached value, or newly generated value. A
later recovery attempt begins from the canonical file again; no background
retry runs.

After power loss during an indeterminate rotation, the canonical file may
contain the old or new complete generation. Recovery re-enables whichever
complete generation the canonical path contains after validation and a
successful directory synchronization. Old cursors verify only if the old
generation is recovered; new cursors verify only if the new generation is
recovered. This named failure preserves the sole-file design: deleting
rotation would violate the operator goal, while a second durable record would
violate the sole-authority invariant.

For an authentic cursor whose signature is valid but whose resolved-principal
binding differs from the request, the router preserves the canonical identical
`404 not_found` body, headers, and no-row-lookup behavior. A caller-forged body,
including one re-signed with the bearer credential or any other client-known
value, fails signature validation and returns the existing `400 invalid_cursor`
before a resource-row lookup. Malformed, wrong-version, wrong-route,
wrong-resource, wrong-direction, changed-filter, and bad-signature cases remain
the same typed invalid-cursor class.

The material, its path, raw HMAC key, decoded cursor body, and signature-input
bytes never enter HTTP, cursor diagnostics, logs, traces, telemetry, exceptions,
crash reports, artifacts, or test output. Internal failures expose no key,
resolved request principal, route, tuple, or name-presence detail. If an
already-running provider cannot read an intact material record, the route emits
the existing `500 projection_invalid` envelope with
`Cache-Control: no-store` and no partial response; it does not downgrade to an
unauthenticated cursor mode.

The unprovisioned, mutation-in-progress, indeterminate-commit, quarantined, and
recovery-refused outcomes expose only their exact type, the operation kind, the
safe cause class, and the acting local principal: the owner for an explicit
operation or application bootstrap for startup. They expose no material, path,
generation value, temporary name, filesystem detail, cursor body, signature
input, route, tuple, or resolved principal.

### Authentication, visibility, errors, and cache

The transport uses `Authorization: Bearer <existing gateway credential>`.
Absent or invalid bearer credentials return `401 auth_failed`. An org bearer
requires one `asUser`: missing returns `400 invalid_message`, repeated returns
`400 invalid_as_user`, and malformed percent encoding returns
`400 malformed_query` before principal resolution. An org bearer passes the
decoded value to the existing resolver without normalization or existence
lookup. That resolver selects the same principal as dispatch, including an
unknown nonempty user id.

A session bearer with a matching `asUser` validates `session.ownerUserId` and
resolves the owner user principal. A mismatching session `asUser` returns
`403 identity_not_yours`. A device bearer with `asUser` returns
`400 invalid_as_user` before principal resolution. These cases require the
reviewed AU2 correction gate; D1 adds neither a resolver nor a principal
binding.

Config, host environment, users, identity, and kungfu use their M1 admin-only
visibility predicates. Hosts use their M1 AU4 predicate and admit any
authenticated org user or session, so D1 has no forbidden authenticated host
detail case. A denied collection omits unreadable rows. The identity
collection applies its resource-wide visibility predicate before its
payload-bearing collection query. A denied detail uses the canonical identical
`404 not_found` result. The transport returns
`400 invalid_filter` and `400 invalid_cursor` before a resource-row lookup in
the cases specified above. It uses the canonical error envelope and
`Cache-Control: no-store` for these errors.

### Implementation and test touchpoints

- `lib/tightbeam/cursor_signing.ex` and `lib/tightbeam/application.ex`: preserve
  the sole canonical 32-octet file; implement the three terminal durability
  outcomes, cross-process quarantine, startup and owner recovery, and their
  serialization boundaries without another durable record.
- `lib/tightbeam/gateway.ex` and `lib/tightbeam/wire/router.ex`: keep Gateway
  injection and application-boundary admission atomic with quarantine. Router
  remains a signing-provider consumer and owns no maintenance operation, key,
  state cache, or recovery path.
- Focused cursor-signing tests and the existing filesystem failure probe:
  prove persistent pre-publication and post-publication failures, restart and
  power-loss recovery, cross-process admission boundaries, exact typed
  outcomes, and redaction with captured real failure responses.
- `lib/tightbeam/wire/router.ex`: add the listed GET matches; reuse bearer and
  AU2 dispatch-parity resolution; call M1 seams; encode R4 responses and
  canonical errors.
- `lib/tightbeam/state_resources.ex`: M1-owned collection capability within
  the six named query seams; the identity seam implements the tagged metadata
  and hydration stages; the six named serializers remain the sole public item
  encoders and `identity/1` performs zero I/O.
- `lib/tightbeam/state_visibility.ex`: M1-owned AU4 predicates; the hosts
  predicate changes from the old admin-only behavior to authenticated-org
  user/session visibility before D1 consumes it.
- `lib/tightbeam/firehose/registry.ex` and
  `lib/tightbeam/admin_projection.ex`: contract tests for the shared seams;
  ref-based identity reads use the staged seam; already-hydrated committed
  identity items use the same pure serializer; no REST registry, REST
  projection, or D1 firehose activation.
- `test/router_test.exs`, `test/admin_projection_test.exs`, and focused HTTP
  route tests: routes, envelopes, auth, parity, visibility, filters, cursors,
  ordering, cache, closed fields, and firehose item-byte parity.

## Acceptance

1. Given canonical `main` lacks one M1 seam or lacks the reviewed AU2 repair,
   when the D1 code-start check runs, then it fails before a product source
   edit.
2. Given canonical green `main` satisfies both gates and an authorized
   principal, when the client sends a real HTTP GET to each route in the table,
   then the server returns 200, the stated R4 envelope, `schemaVersion: 1`,
   the resource string, an item from the listed serializer, and
   `Cache-Control: no-store`.
3. Given a raw resource row contains an extra field or lacks an R7/R7a field,
   when its listed serializer runs through a real HTTP route, then serialization
   fails and the server emits no partial item.
4. Given a D1 detail item and its matching firehose notice, when the test
   removes their outer objects, then the item JSON bytes are equal.
5. Given an authenticated non-admin user and an authenticated session, when
   either requests `/api/hosts` and a known host detail, then the shared hosts
   predicate permits the route under AU4. Given either principal requests a
   known admin-only D1 detail, then the server returns the same 404 as an
   unknown detail.
6. Given org bearer `asUser` values that are known, unknown, empty, missing,
   repeated, or malformed; session bearer values that are absent, matching, or
   mismatching; and a device bearer plus `asUser`, when direct HTTP GET and
   dispatch run with equivalent inputs after the AU2 gate passes, then they
   produce the same resolved principal or the stated 400/403 refusal. The
   test records no new credential, binding, authorization grant, or tailnet
   identity behavior.
7. Given users `userId` filters that match and do not match, when HTTP
   collection GET runs, then the named query seam restricts results and an
   unknown well-formed id yields an empty collection. Given `status` or an
   ownership key on users, then the server returns `400 invalid_filter`.
8. Given a resource's allowed filters, repeated values within one field, and
   values across two fields, when HTTP collection GET runs, then repeated
   values apply OR and distinct fields apply AND. Given an unlisted key or a
   malformed listed value, then the server returns `400 invalid_filter` before
   resource-row lookup.
9. Given tied user timestamps, deleted page-boundary rows, and more than 50
   authorized rows, when a client pages with both bounds, then it receives an
   item once in the stated tuple order. Given `limit=501`, then the page has
   500 items. The cursor inspection proves it contains no rowid, offset, or
   live-row locator.
10. Given malformed, wrong-resource, changed-filter, wrong-principal, and
    now-hidden cursors, when HTTP collection GET runs, then the server applies
    AU7 precedence: the first three return `400 invalid_cursor`, the
    wrong-principal case returns the canonical 404, and a now-hidden row is
    absent.
11. Given an authorized known identity name, the same known name under a
    forbidden principal, and an unknown name, when a database spy traces the
    metadata stage, then every call executes exactly one byte-identical SQL
    statement with the same parameter count and returns exactly one database
    row and one opaque descriptor. The spy records zero `item` column access,
    payload-byte opens, JSON decodes, Git reads, file reads, and secondary
    queries.
12. Given an authentic descriptor and descriptors with a changed byte, wrong
    resource, wrong name, wrong source, wrong source generation, wrong resolved
    principal, wrong request binding, closed operation, prior process
    generation, and cross-request replay, when hydration runs, then only the
    authentic descriptor used by the exact principal that cleared visibility
    may reach the database. Every invalid case returns
    `invalid_identity_descriptor` before database access, records the safe
    loud fault, emits no descriptor or principal-binding content, and opens no
    payload. Repeating the authentic descriptor inside its bound operation by
    the same principal returns the same result while the observed version
    remains unchanged.
13. Given a descriptor for a present row, an absent row, and each row changing,
    appearing, or disappearing before hydration, when an authorized caller
    hydrates, then an unchanged present row returns a hydrated item only from
    its observed version, unchanged absence returns `:not_found`, and every
    race returns `:stale` without payload. The caller retries the full
    metadata-visible-hydration sequence once. A second race emits the
    canonical 404 and no partial item.
14. The identity timing proof uses one warmed in-process server, one database,
    one connection configuration, and one valid closed identity item whose
    stored encoded payload is at least 116,000 bytes. The suite records the
    machine, runtime, database version, fixture byte count, and random seeds.
    It performs exactly 2,000 unrecorded warm-up calls per cohort, then five
    recorded runs. Each metadata run contains exactly 10,000 known-authorized,
    10,000 known-forbidden, and 10,000 unknown calls in one balanced random
    order produced from that run's recorded seed. Each real-HTTP run contains
    exactly 10,000 forbidden-known and 10,000 unknown calls in one balanced
    random order. Statement spies run separately from latency measurement.
    The timer uses monotonic nanoseconds from entry into the measured stage, or
    HTTP dispatch, through the complete returned value, or response bytes.
    The suite uses nearest-rank p50 and p95, removes no sample or outlier, and
    reports every run rather than an average. For each cohort pair and
    percentile, `delta = abs(a - b) / min(a, b) * 100`; every recorded run must
    have `delta <= 5%` at both p50 and p95.
15. Given non-admin requests for `GET /api/identity/served` and
    `GET /api/identity/:unknown`, when the deterministic spy proof and the
    randomized real-HTTP proof run, then both requests enter the metadata stage
    of `StateResources.query_identity/2` before visibility, use the exact
    statement shape, count, and one-row cardinality from Acceptance 11, emit
    the same canonical 404 and `Cache-Control: no-store`, never invoke
    hydration or the serializer, open no payload bytes, and meet Acceptance
    14's timing bound in every run.
16. Given REST detail, REST collection, CLI identity status, firehose rebuild,
    firehose ref-based reads, and an already-hydrated committed firehose item,
    when caller-contract spies execute each path, then every name-based path
    uses the tagged stages of the one public `query_identity/2` function,
    every denied path stops before payload access, and every serialized path
    passes hydrated data to the one public `identity/1` serializer. A serializer
    spy records zero database, process, file, Git, credential, and network I/O.
    Public CLI, REST item, and firehose payload bytes remain unchanged.
17. Given the route table and AU4 visibility rules, when the contract test
    checks the structural exclusions, then it proves `/api/host-env` exposes
    no detail route and hosts admit every authenticated org user or session, so
    D1 has no unknown-versus-forbidden detail pair for host environment or
    authenticated host details.
18. Given the integrated registry, when the contract test reads its six rows,
    then every row names the same query, serializer, visibility, primary refs,
    and version source used by REST. The test fails if router code adds a
    REST-local serializer, projection, field, parallel `list_*` query seam,
    second identity query function, or serializer database access.
19. Given a cursor issued for each collection route, `before` and `after`, every
    allowed filter combination, tied order tuples, and each resolved-principal
    kind, when the test inspects only the server-side decoded body, then the
    signed body contains exactly the D1 cursor version, canonical route key,
    resource, exclusive direction, normalized filter fingerprint, complete
    immutable tuple, and exact principal binding. It contains no bearer,
    offset, `rowid`, live locator, payload, or key bytes. Changing any listed
    binding returns `400 invalid_cursor` before a row lookup; changing only
    `limit` retains the existing D1 behavior.
20. Given a valid cursor whose principal binding is changed, when a test caller
    recomputes its signature with the bearer credential, a hash of that
    credential, a node cookie, or any other client-known value, then the server
    returns `400 invalid_cursor`, performs no resource-row lookup, and emits no
    cursor detail. Given an unmodified authentic cursor used by another
    principal, then the server returns the canonical identical `404 not_found`
    result from Acceptance 10.
21. Given a provisioned material file and a cursor issued before a clean
    application restart, when startup validates that file and synchronizes its
    containing directory, then the provider re-enables that exact generation
    before listener admission. The same route and principal can reuse the
    cursor with unchanged D1 item bytes. The test proves that startup neither
    regenerated material nor used material retained by the prior process.
22. Given a valid pre-rotation cursor, when the local operator invokes the
    provider's rotation operation and the file flush, atomic rename, and
    containing-directory synchronization succeed, then the operation returns
    success. The old cursor returns `400 invalid_cursor` before a row lookup,
    and a cursor issued after success verifies with the fresh 32-octet
    generation. No REST or bearer-client operation can invoke rotation.
23. Given at least 64 concurrent request processes and at least two application
    processes, when they issue and verify cursors before, during, and after one
    successful rotation, then each admitted operation observes one complete
    generation. Operations that finish their material read before publication
    use the old generation. The provider admits no operation from publication
    through directory synchronization. Operations admitted after success use
    the new generation. The test records the read, publication, synchronization,
    and admission boundaries. No torn, mixed, process-local, dummy, or
    bearer-derived key succeeds, and a rejected cursor causes no row lookup.
24. Given an empty first-boot secrets directory, when the application starts,
    then it selects unprovisioned state and keeps listener admission closed.
    Signing, verification, rotation, and recovery return
    `{:error, :cursor_signing_unprovisioned}`. When the local owner explicitly
    invokes bootstrap provisioning, then it creates exactly one canonical
    32-octet file with exact mode `0600` and enters healthy state only after the
    material-file flush and containing-directory synchronization succeed.
    `Tightbeam.Application` then admits the listener. Given a present file that
    is unreadable, not exact mode `0600`, not exactly 32 octets, or whose
    directory cannot be synchronized during normal startup, then startup
    remains quarantined and fails before listener admission. It emits no
    secret-bearing diagnostic, silently generates no replacement, and serves
    no REST request. Given a missing or malformed injected provider, Router
    startup also fails closed with no fallback.
25. Given a material file, a cursor, and each D1 route, when the test captures
    logs, traces, telemetry, exceptions, crash output, HTTP bytes, and artifact
    output for provisioning, restart, signing, verification, rotation,
    unprovisioned refusal, mutation-overlap refusal, mutation-owner death,
    indeterminate commit, quarantine, and recovery refusal, then none contains
    the material, path, generation value, temporary name, HMAC input, raw
    cursor body, signature detail, route, tuple, or resolved principal. A safe
    internal fault may contain only the exact outcome type, operation kind,
    safe cause class, and acting local principal: the owner for an explicit
    operation or application bootstrap for startup. HTTP error bodies remain
    the existing closed envelopes and `Cache-Control: no-store`.
26. Given all Acceptance 1–18 fixtures and gates, when they rerun with the
    provider injected, then routes, envelopes, status codes, cache headers,
    authentication, visibility, filters, order, pagination, six shared query
    seams, identity staging, CLI behavior, firehose behavior, and serialized
    item bytes are unchanged. The provider adds no serializer, query, route,
    public field, credential, principal rule, D2/D3 behavior, deployment, or
    release behavior.
27. Given deterministic failure injection before the publication boundary of
    first provisioning, when the local owner invokes provisioning, then the
    operation returns an ordinary error and restart observes the unprovisioned
    state. Given the same injection before rotation publication, then rotation
    returns an ordinary error and restart loads the byte-identical prior
    generation. Neither case enters quarantine or leaves a temporary authority.
28. Given a persistent containing-directory synchronization failure immediately
    after first-provision publication and after rotation rename, when the local
    owner invokes each operation, then each invocation returns exactly
    `{:indeterminate_commit, :cursor_signing_authority_may_have_advanced}` after
    one failed synchronization and performs no internal retry. It never returns
    success or an ordinary error. The provision case leaves a complete canonical
    record visible. The rotation case leaves either old or new restart authority
    possible and removes the old generation from the running verification set
    at rename.
29. Given the failure in Acceptance 28 and concurrent sign, verify, provision,
    and rotate calls from at least two application processes, when the failed
    directory synchronization is pending, then each overlapping mutation call
    returns `{:error, :cursor_signing_mutation_in_progress}` and performs no
    material or namespace action. When the synchronization returns, the
    provider converts the held publication boundary to quarantine before it
    releases the indeterminate outcome. Each call admitted after that release
    returns `{:error, :cursor_signing_quarantined}`, reads no key bytes, and
    performs no namespace mutation. A real HTTP request that reaches that
    provider returns `500 projection_invalid`, `Cache-Control: no-store`, and
    no partial response or row lookup.
30. Given a quarantined provider and one complete canonical record, when an
    explicit local owner recovery validates that record, successfully
    synchronizes its containing directory, and proves that the record stayed
    canonical, then recovery atomically re-enables exactly that generation
    across both application processes. Given a missing, malformed, concurrently
    replaced, or persistently unsynchronizable canonical record, then recovery
    returns `{:error, :cursor_signing_recovery_refused}` and both processes
    remain quarantined. The test observes no alternate store, generated
    replacement, background retry, HTTP recovery path, or bearer-client
    recovery path.
31. Given power loss after an indeterminate rotation and fixtures that restore
    the canonical path once with the old complete generation and once with the
    new complete generation, when the application restarts, then startup first
    remains quarantined, validates the restored record, and synchronizes the
    containing directory. It then admits the listener with exactly the restored
    generation. The old fixture accepts only old-generation cursors; the new
    fixture accepts only new-generation cursors. A validation or synchronization
    failure refuses startup and admits no listener.
32. Given power loss after indeterminate first provisioning and fixtures that
    restore the canonical path once absent and once with the complete published
    generation, when the application restarts, then the absent fixture selects
    unprovisioned state and admits no listener. Recovery returns
    `{:error, :cursor_signing_unprovisioned}`; explicit local first provisioning
    is the sole legal transition and follows Acceptance 24. The complete-record
    fixture begins quarantined, validates and synchronizes that exact record,
    then atomically enables it before listener admission. Neither fixture
    silently generates material or selects a staging file.
33. Given at least two application processes sharing one canonical path and a
    fixture that holds one lifecycle-valid mutation immediately after
    exclusive admission—provision in unprovisioned state, rotate in healthy
    state, or recovery in quarantine—when the test starts one overlapping
    provision, one overlapping rotate, and one overlapping recovery in
    separate runs for each held mutation, then the held mutation is the sole
    admitted mutation in each of the nine request-pair shapes. The overlapping
    request returns exactly
    `{:error, :cursor_signing_mutation_in_progress}` before lifecycle
    validation, material read, CSPRNG access, staging-file creation, or
    namespace mutation; it does not wait, queue, or retry. The test repeats
    each provision-winner and rotate-winner shape with success, ordinary
    pre-publication error, and post-publication indeterminate commit. It repeats
    each recovery-winner shape with success and recovery refusal. In each
    fixture, only the admitted operation can publish or change lifecycle state.
    Its terminal outcome agrees with the canonical generation and provider
    state established before mutation admission is released. A request started
    after release is evaluated against that resulting state. No losing overlap
    publishes later, changes the admitted operation's outcome, or creates a
    durable lock, marker, journal, authority, or recovery input.
34. Given at least two application processes sharing one canonical path and a
    provision or rotation whose observer has completed atomic publication,
    entered the published-but-unsynchronized phase, and blocked the containing-
    directory synchronization from returning, when the test kills the admitted
    mutation's per-operation owner process, then the observer records the owner
    exit and transitions directly to quarantine before it releases mutation
    admission. While admission remains held, concurrent provision, rotate, and
    recovery calls return `{:error, :cursor_signing_mutation_in_progress}`;
    sign and verify are not admitted. After quarantine and admission release,
    sign, verify, provision, and rotate return
    `{:error, :cursor_signing_quarantined}` without a material read or namespace
    mutation; recovery alone may enter Acceptance 30. The dead owner receives
    no success, ordinary error, or fabricated indeterminate return. The test
    trace orders atomic rename, published-but-unsynchronized phase entry, owner
    exit, quarantine, and admission release. An in-flight or later
    synchronization result cannot establish success or healthy state. Explicit
    owner recovery and restart each use only the canonical file and follow
    Acceptance 30–32 before that exact generation is re-enabled. The provision
    and rotation fixtures each prove that no later generation publishes before
    recovery and that no second durable record, pointer, marker, journal, retry,
    or secret-bearing diagnostic appears.

## Open Questions

None for this cursor-signing amendment. A new D1 filter, host-environment detail
route, public item field, or principal rule requires another canonical REST
amendment. D1 code remains blocked until this amendment is independently
reviewed and the reviewed AU2 correction described in Assumption 3 lands on
canonical green `main`.
