# REST state API v1 — the read plane (product spec, canonical r3)

Amendment candidate, 2026-08-25: distinguish durable Toplines from the
mechanical ExecutionMap and add the REST-only ExecutionMap contract. The
amendment changes no durable Toplines field, mutation, or route. Its companion
firehose amendment adds source invalidation notices for existing durable
Topline and subagent-marker commits; it adds no ExecutionMap class.

Review status, 2026-08-25: AMENDED AFTER exact review
`att_90efe520-f84c-4d3b-bd09-9c36f8a0ff08` requested changes on exact
`e4a27977477a25c3037bba164db2bc1d508bcd7a`; full report `art_bffa387b`
supplies findings F6-F7. Product-owner ruling
`att_c0fee9c0-3489-4a57-b981-080fbcca4f66` preserves the existing
message-bearing session-owner refusal and restores canonical R6 while keeping
ExecutionMap-scoped R6a. Earlier F1-F5 and SQ6-SQ8 rulings remain incorporated.
The resulting three-file successor requires a fresh independent review before
M1, M2, specRef binding, or implementation. Separable r3 resources remain
unaffected.

Status: CANONICAL r3, 2026-08-22. r3 folds the REST-side adjudicated
findings F1/F8/F9/F13/F14/F16/F21/F22 from
`review-gate-observability-2026-08-21.md` and aligns with firehose r6.
This successor resolves changes-requested `att_71210c7b` against exact commit
`c8eb1d080890ad571c5319b2514230c71a021427`; its closure map is in the
adjudication companion.
It also consumes Mike's ruled SQ2: the admin read plane includes users,
devices, ops metadata, and first-class archetype, kungfu, rail, and guidance
content, all admin-only with secrets structurally excluded.
r2 folds the reviewed mechanical amendment
`art_8e2d8444` (reviewed-clean `att_0b648694`): adopted route/filter
inventory, interim/final CLI transport, firehose serializer scope, the
R12-to-M5 repair, and the harness-catalog compatibility ruling. Written
by tb02 and product-owner:rest-state-api. Untargeted (0.2.0 or
later); when build work starts it branches from main tip. The current amendment
is owned by successor `product-owner:rest-state-api-v2`; the legacy PO session
is revoked. Spirit questions route through the successor.

Authority and inputs:
- rest-vs-cli-adjudication.md r2 (tb02, Mike-directed): the three-plane
  ruling this spec implements. REST is the read plane, verbs are the
  write plane, the CLI is sugar.
- Recon wi_9239a7f1's report (NFS
  shared/specs/tightbeam/rest-state-api-recon.md): the inventory,
  contract baseline, and code evidence. Adopted with zero material
  rejections; its six conditions are folded in as requirements here.
- event-firehose-v1.md r6: the sibling notice socket. The two contracts
  share serializers (SR series below) — that sharing is the whole
  correlation story.
- Mike's rulings, 2026-08-20/21: clients build models from state, not
  events; SQL against state.db is not a product interface; the CLI makes
  common things easy and never re-creates SQL; auth is the existing
  gateway credential, no API keys; deployment is localhost/tailscale.
- Mike's rulings, 2026-08-25: remove the `asUser` GET prohibition. The
  parameter only transports the CLI's existing principal selection and adds
  no credential, binding, authorization, or tailnet-identity behavior. After
  client parity, remove legacy dispatch-read transport and compatibility
  aliases; dispatch remains the write plane. Durable authority is message
  `s_21b93fdd-5e62-4ed9-ac7e-923697463936`. This ruling supersedes only the
  contrary “no asUser query parameter” clauses in rest-vs-cli-adjudication.md
  r2 and its adopted recon baseline.
- session-tokens-v1.md's principal-seam table defines the existing CLI
  principal selection that AU2 transports. This spec adds no second resolver.
- rest-state-api-r3-adjudication.md: durable REST finding text, source
  message identifiers, the closure map, and the SQ2 ruling pointer.
- rest-state-api-v1-wire-schema.md: normative JSON types, nested shapes,
  enum domains, nullability, and canonical ordering for R7/R7a.
- Companion mapping ruling `art_4a1cce6e`, SHA-256
  `5db8aab3496747d008fb8c024a4f1617f92695d144c89481bca3a1f20842550a`:
  condition facts and critical leases enter firehose R8 with the exact R8 rows
  below; it supersedes the fact-only `art_5d8bacb2`.
- ExecutionMap authority: `topline-map-v1.md` plus product source
  `Tightbeam.ExecutionMap` at `d00e06aea578d711e608637d38a97872487df15e`.
  Durable `Tightbeam.Toplines` at that revision remains a separate source.
  D2 `wi_ea98345b-51f4-4fae-b7df-3670c0d54f6b` and D3
  `wi_113442f5-22ae-457b-a971-1b620069d490` consume this amendment; they do
  not define its contract. The adopted six-resource seam contract remains
  `art_b1995a26` / fact 1093 and is unchanged.

## Spec homing

The canonical spec lives only in the `tightbeam-specs` repository as
`rest-state-api-v1.md`. This amendment's exact canonical set is
`rest-state-api-v1.md`, `rest-state-api-v1-wire-schema.md`, and
`event-firehose-v1.md`; a change to an ExecutionMap envelope, dependency
entry, or R8b mapping lands those coupled files in one reviewed revision.
`rest-state-api-r3-adjudication.md`, `rest-vs-cli-adjudication.md`, and
`topline-map-v1.md` remain authority inputs, not custody companions for this
amendment. A worktree, artifact row, transcript, adjudication ledger, or review
report is evidence, not canonical custody. Canonical r3 passed joint
independent review at `att_45676d30` and landed on the canonical branch in
merge `c84b1b8dc856861baeaa7b5ff781317ded568cb1`. This amendment remains a
candidate until one exact revision of its three-file canonical set passes
independent review and lands in `tightbeam-specs`.

## Goal

Define a complete, authorized, deterministic REST read plane from which ATC,
Clawline, and future clients can rebuild every admitted shared-state model and
correlate later firehose notices without reading SQLite or replaying history.

## Non-goals

- REST v1 does not create a general mutation API.
- REST v1 does not expose SQLite rows, `rowid`, credentials,
  credential-bearing paths, or unrestricted configuration and environment
  values.
- REST v1 does not turn the firehose into an event log or make observational
  notices rebuildable state.
- REST v1 does not retire compatibility aliases before their clients migrate
  or decide future tailnet identity.
- REST v1 does not authorize implementation, deployment, or client migration.
- REST v1 does not alias ExecutionMap telemetry through `/api/toplines`, add an
  ExecutionMap firehose class, or change the six adopted shared serializer
  shapes from `art_b1995a26` / fact 1093. Exact source invalidation notices for
  existing Topline and subagent-marker commits are the ruled exception to the
  earlier no-new-class boundary.

## Assumptions

AS1. Every admitted credential resolves to exactly one user or session
principal before a read handler runs. A conformance test falsifies this if one
credential resolves ambiguously.

AS2. The write seam can allocate a durable integer version after a successful
state mutation and before commit. Crash/restart and delete/recreate tests
falsify this if a version repeats or moves backward.

AS3. The served-identity repository revision and the config,
host-environment, and credential stores are distinct inputs. A source-boundary
test falsifies this if an admin content query reads the latter stores.

AS4. Each collection has a stable public natural key. A schema test fails
before a route ships if any item lacks that key.

## Invariants

I1. Authorization precedes subscription filtering, serialization, byte open,
and existence-dependent error selection.

I2. Every projection is closed-world. This file owns field names and the
wire-schema companion owns their types and deterministic encoding.

I3. A cursor contains only an immutable ordering tuple and request binding. It
never resolves through a live row or stores `rowid`.

I4. One query and one item serializer serve REST, CLI wrappers, and every
firehose class in the A6 overlap.

I5. A stored-state mutation has one registered rebuildable-state mapping, one
registered source-invalidation mapping, or an explicit companion-spec
exclusion. Silence is never an implicit mapping.

I6. Versions increase across update, delete, and recreation of the same public
key. A process restart does not reset the version floor.

I7. Durable human intent and mechanical execution telemetry are distinct
resources. `/api/toplines[/:id]` reads durable Topline rows and memberships.
`/api/execution-map` reads a composed snapshot of execution rows. Neither name
aliases, replaces, or widens the other.

## Architecture

The read plane has four seams. A principal resolver produces one authenticated
principal. A resource query applies the AU4 visibility function and fixed
filters. The R7 serializer emits the closed wire item defined by the wire
schema. An outer adapter places that item in a REST envelope, compatibility
envelope, CLI result, or firehose notice. Composed views declare their source
classes in R9 and use a dependency digest instead of a notice class.

Operating-guidance impact: none. This amendment applies the existing REST
resource/query/serializer pattern and creates no cross-repository agent rule.

## Spirit (read this before quizzing Mike)

SP1. The state db is the truth; clients hold display models of slices of
it. This API exists so a client can build and refresh that model with
typed reads instead of SQL coupling (ATC's direct SQLite reads are the
demand evidence and the first migration target) or CLI screen-scraping.

SP2. The API is deliberately boring: resources that mirror the PRODUCT
model (not the storage layout), keyset pagination, whitelist filters. No
query language, no caller-selected joins, no fields/sort/include. When a
client needs a new shape, the answer is a new whitelisted filter or a new
composed resource — decided by this spec's PO — never a generic escape
hatch. Flexibility creep here is how SQL sneaks back in wearing a hat.

SP3. Reads are safe and boring; writes are law. Nothing on this surface
mutates, ever. Anything that mutates is a dispatch verb with attribution
and rails. This asymmetry is the security model as much as the
architecture.

SP4. One canonical public projection and serializer own each resource.
When a resource has a rebuildable-state firehose class, its REST detail
item and notice payload are the same bytes from that serializer. REST-only
composed, catalog, or admin reads do not gain a notice class merely because
they have a projection. A second public serializer for one resource remains
forbidden.

SP5. The deployment is one operator's tailnet. This spec inherits the
no-API-keys ruling and does not design for adversarial third parties;
if that ever changes, scoped credentials are a later versioned addition
(same pattern as the firehose).

SP6. Moving a CLI read from dispatch to GET preserves the CLI's current
security exactly. An `asUser` GET parameter only transports the CLI's
existing principal selection. It adds no credential, principal binding,
authorization grant, or tailnet-identity behavior.

SP7. A Topline records durable human intent: its title, owner, lifecycle,
memberships, and concerns. ExecutionMap reports mechanical evidence the
substrate can derive from work, assignment, turn, attest, wake, decision,
session, user, marker, and causal-event rows. Similar historical CLI names do
not make these concepts interchangeable. A client asks Toplines what people
are carrying and ExecutionMap what the machinery records about execution.

## Terms

T1. **Resource** — one product entity or mechanical composed view with a
canonical public projection and a stable primary id.

T2. **Projection** — the explicit public field list for a resource. One
serializer owns it (SR1). Storage secrets never appear in any projection.

T3. **Keyset cursor** — an opaque, versioned encoding of the resource name
and its complete immutable ordering tuple. It is an exclusive
`before`/`after` boundary. It never contains an SQLite `rowid`, another live
storage locator, or an offset. Deleting the boundary row does not invalidate
the cursor.

T4. **Durable Topline** — a stored human-intent aggregate owned by one user,
with durable membership and concern state. Its REST home is
`/api/toplines[/:id]`.

T5. **ExecutionMap** — a read-only composed execution snapshot. It derives
work-item nodes, telemetry, and causal nesting from existing source rows. It
adds no table, mutation, or `execution_map.*` notice. Its underlying source
mutations retain their R8 mappings and the marker source has the ruled R8b
mapping. Its REST home is
`/api/execution-map` and the three nested routes in R3a.

## Requirements — surface

R1. Namespace `/api/<resource>`, JSON, every response carrying
`"schemaVersion": 1`. `/version` remains the preflight. Existing
unversioned routes become compatibility aliases (M5) until clients
migrate; an incompatible future API is a new versioned namespace.

R2. Core model resources:

| Route | Purpose |
|---|---|
| GET /api/org | small org document: archetypes, hosts, model catalog — no embedded session collection |
| GET /api/catalog/harnesses | canonical harness capability catalog using the v1 response envelope; `/harnesses` keeps its legacy raw-array envelope only during M5 migration and is removed in M8 |
| GET /api/hosts[, /:host] | paged host registry and host detail; the underlying state resource for `host.registered` |
| GET /api/sessions | paged sessions |
| GET /api/sessions/:sessionKey | session detail + mechanical status |
| GET /api/sessions/:sessionKey/messages | paged transcript projection |
| GET /api/sessions/:sessionKey/coordination-share?from=&to= | pure bounded aggregate read |
| GET /api/work-items[, /:id, /:id/trace] | paged collection, detail, composed trace |
| GET /api/assignments[, /:id, /:id/attests] | paged collection (with derived status, advisory files, effect), detail, nested attests |
| GET /api/attests | bulk paged attests across authorized work |
| GET /api/wakes[, /:wakeId, /:wakeId/digest-members] | paged wakes, detail, digest audit read |
| GET /api/turns[, /:seq] | paged turns, detail |
| GET /api/artifacts[, /:artifactId] | paged artifact metadata, detail (+ existing GET /download/:assetId for bytes) |
| GET /api/assets[, /:assetId] | paged binary-asset metadata and detail; bytes remain on existing GET /download/:assetId |
| GET /api/decision-requests[, /:id] | paged collection, detail |
| GET /api/read-markers[, /:scopeKey] | caller's markers (write stays a verb, firehose RM2) |
| GET /api/roles | paged role registry |

The bulk attests/wakes/turns collections are first-class on purpose:
nested-only resources force ATC-class clients into one request per parent.

During M5 migration, the two harness-catalog routes share authorization, the
canonical query, ordering and filtering, and one canonical serializer for
each harness item. Only their outer wire adapters differ. They do not promise
byte-identical complete responses. The canonical route wraps items in the v1
envelope; the compatibility alias preserves its legacy raw array until M8
removes that alias.

R3. Durable human-intent reads are GET `/api/toplines[/:id]`. Mechanical
reads are GET `/api/execution-map` and its R3a nested routes, `/api/facts`,
and `/api/critical-state`. Admin reads are GET /api/identity[, /:name],
/api/archetypes[, /:name], /api/kungfu[, /:name],
/api/guidance[, /:name], /api/rails[, /:name], /api/config[, /:key],
/api/host-env, /api/harness-processes, /api/users[, /:userId], and
/api/devices[, /:deviceId]. SQ2 admits these routes. Every one is admin-only;
SR2 and SR5 still exclude secrets. Mechanical and admin views are not part of
a normal display-model bootstrap.

`/api/facts` is the append-only condition-fact collection.
`/api/critical-state` returns every recorded critical-lease row, including an
expired row; it never removes a row merely because wall time passed. A client
derives current activity as `expiresAt > now`.

R3a. ExecutionMap exposes exactly these REST-only composed routes:

| Route | Result |
|---|---|
| `GET /api/execution-map` | flat roster, paged by the signed `(createdAt,id)` tuple |
| `GET /api/execution-map/tree` | complete caller-visible forest, unpaged |
| `GET /api/execution-map/subtrees/:workItemId` | caller-visible anchor plus transitive caller-visible linked descendants, unpaged |
| `GET /api/execution-map/assignments?assignmentId=<id>&assignmentId=<id>` | items selected by one or more explicit assignment ids, unpaged |

Besides AU2's transport-only `asUser`, the flat, tree, and subtree routes
accept only `origin`, `ownerUserId`, `state`, `quietOverMs`, `specRefName`,
`specRefSha256`, and `sessionKey`, plus the flat route's `before`, `after`, and
`limit`. Besides `asUser`, the assignments route accepts only repeated
`assignmentId`; it rejects each roster filter and pagination parameter. At
least one nonempty `assignmentId` is required. Duplicate exact assignment ids
collapse before selection. R6a fixes validation and filter meaning.

R3b. The shared ExecutionMap seams are exact. `Tightbeam.ExecutionMap` owns
`list_execution_map/2`, `query_execution_map_tree/2`,
`query_execution_map_subtree/2`, and `query_execution_map_assignments/2`.
`Tightbeam.ExecutionMap.execution_map_node/1` is the sole public node
serializer. `Tightbeam.StateVisibility.execution_map_node_visible?/3` composes
the existing AU4 predicates named in AU4a. Assignment selection first calls
`Tightbeam.StateVisibility.execution_map_assignment_visible?/3`, then the node
predicate. Neither predicate grants authority of its own.
`Tightbeam.Wire.Router.rest_read/3`, `Tightbeam.RestCursor`, and
`Tightbeam.RestEnvelope` remain the one route, cursor, and outer-envelope
adapters. Route code does not query rows, build a node, copy a visibility rule,
or encode an envelope.

R4. Envelopes. List:
`{"schemaVersion":1,"resource":"assignments","items":[],"page":{"oldestCursor":null,"newestCursor":null,"hasMoreBefore":false,"hasMoreAfter":false}}`.
Detail: `{"schemaVersion":1,"resource":"assignments","item":{}}`.
For every notice-backed resource, the `item` shape equals the firehose
notice `payload` shape (SR1).

R4a. ExecutionMap success envelopes are closed. Every successful route returns
`schemaVersion:1`, `resource:"execution map"`, `edgeBasis:"concurrent_turn"`,
`coverage:{attributionCutoff,basis:"conservative_shared"}`, and
`dependencyVersion`. The flat route also returns only `items` and R4 `page`.
The tree and subtree routes also return only `roots`. The assignments route
also returns only `items` and `noItem`; `noItem` sorts assignment ids ascending.
No unpaged route returns `page`. A tree node contains its R7d node keys plus
`children`; a flat or assignment-selected node has no `children` key.

Every ExecutionMap success and error response carries
`Cache-Control: no-store`. The routes define no ETag, conditional request, or
shared-cache behavior. A valid request returns 200. Invalid or absent bearer
returns `401 auth_failed`. A syntactically valid selector that is unknown or
forbidden returns the AU3 `404 not_found`. Invalid query shape or value returns
`400 invalid_filter`; malformed query encoding returns
`400 malformed_query`. A session bearer whose `asUser` mismatches its owner
returns AU2's exact `403 identity_not_yours`. Cursor errors follow AU7.
Serializer or dependency schema failure returns the read plane's closed
`500 projection_invalid` and emits no partial response.

R4b. ExecutionMap error envelopes are closed. The encoded outer object has
exactly `schemaVersion`, `resource`, and `error`, in that order;
`schemaVersion` is `1` and `resource` is `"execution map"`. For
`auth_failed`, `invalid_as_user`, `invalid_message`, `not_found`,
`invalid_filter`, `malformed_query`, `invalid_cursor`, and
`projection_invalid`, `error` has exactly one key, `code`, whose value is that
literal code. For `identity_not_yours`, `error` has exactly `code` followed by
`message`; `code` is `"identity_not_yours"` and `message` is exactly
`"this session belongs to <session.owner_user_id>"`, with
`<session.owner_user_id>` replaced by the target session row's exact stored
non-null owner user id. For `ambiguous_id`, `error` has exactly `code` followed
by `candidateIds`; `code` is `"ambiguous_id"` and `candidateIds` is the
ascending array of visible full typed ids required by R6a.
`identity_not_yours` is the sole message-bearing variant. No other error object
has a `message`, details, selector, denied id, or partial success field.

The route sets exactly these application response headers for every success
and error: `Content-Type: application/json; charset=utf-8` and
`Cache-Control: no-store`. It sets no ETag, `Vary`, redirect, or
`WWW-Authenticate` header. Protocol-managed framing headers do not carry
application data. The JSON encoder emits the R4b key order with no
insignificant whitespace. Unknown and forbidden selectors therefore use the
same status, literal `not_found` body bytes, and application header bytes.

R5. Pagination: `before`/`after` are mutually exclusive, exclusive bounds.
`limit` defaults to 50 and caps at 500 by clamping. No cursor means the newest
page; page items are oldest→newest. Each cursor encodes every component of
the resource's immutable order, including the stable public key as the final
tiebreaker. The server compares the encoded tuple directly; it never resolves
a cursor through a live row. A malformed cursor, wrong-resource cursor, or
cursor whose filter fingerprint differs from the request returns typed
`400 invalid_cursor`. Filters stay fixed within one page chain. Offset
pagination is forbidden.

R5a. Stable collection orders and cursor tuples are:

| Resource | Cursor tuple |
|---|---|
| sessions | `(createdAt, sessionKey)` |
| hosts | `(host)` |
| roles | `(createdAt, name)` |
| work items | `(createdAt, id)` |
| assignments | `(openedAt, id)` |
| attests | `(ts, id)` |
| wakes | `(createdAt, wakeId)` |
| turns | `(seq)` |
| transcript messages | `(seq, id)` |
| artifacts | `(createdAt, artifactId)` |
| assets | `(createdAt, assetId)` |
| decision requests | `(raisedAt, id)` |
| identity | `(name)` |
| archetypes | `(name)` |
| kungfu | `(name)` |
| guidance | `(name)` |
| rails | `(name)` |
| config | `(key)` |
| host environment | `(host, harness, name)` |
| harness processes | `(startedAt, id)` |
| users | `(createdAt, userId)` |
| devices | `(createdAt, deviceId)` |
| read markers | `(userId, scopeKey)` |
| facts | `(id)` |
| critical state | `(sessionKey)` |
| execution map | `(createdAt, id)` |

R5b. Read-marker collection identity is the composite key
`(userId, scopeKey)`. The caller's user id remains implicit for ordinary
user reads, but it remains in the cursor tuple. Two users with the same
`scopeKey` page without loss or duplication. Updates cannot move a marker or
host-environment row because those collections order only by their immutable
natural keys.

R5c. The ExecutionMap flat route admits `limit` at most once. When present,
it matches `[1-9][0-9]*` and parses as a positive base-10 integer. The route
rejects an empty value, zero, leading zero, sign, decimal point, exponent,
whitespace, non-ASCII digit, non-integer, or repeated key as
`400 invalid_filter` before a row lookup. The R5 default remains 50, and the
route clamps a valid value above 500 to 500. This clause changes no other
resource's pagination contract.

R6. Filters are whitelisted per resource:

| Resource | V1 whitelist filters |
|---|---|
| sessions | state, ownerUserId for admin, spawnedBy, archetype, harness, provider, model, host, role |
| work items | state, ownerUserId, createdBySession, createdByUser, isBug, specRefName, holderKey |
| assignments | state, outcome, holderKey, holderRole, workItemId, reviewsAssignmentId, effectKind, derived status |
| attests | assignmentId, workItemId, kind, verdictKind, bySession, byUser |
| wakes | state, sessionKey, creatorSessionKey, workItemId, assignmentId, conditionKind, conditionScope, class, bounded due/fired time |
| turns | status, sessionKey, assignmentId, workItemId, wakeId, jobRef, bounded created/started/ended time |
| artifacts | workItemId, createdBySession, kind, state |
| assets | ownerUserId (admin only), mimeType exact |
| decision requests | status, kind, ownerUserId, assignmentId, raiserSessionKey, expecterSessionKey |
| roles | ownerUserId, boundSessionKey |
| hosts | host exact |
| identity | name exact, state |
| archetypes | skill, host, harness |
| kungfu | status, rootArchetype |
| guidance | name exact |
| rails | mode, tool |
| config | key exact |
| host environment | host, harness, name exact |
| harness processes | sessionKey, host, harness, provider, model, state |
| users and devices | status and ownership filters |
| read markers | caller user by default; scopeKey exact or prefix |
| facts | kind exact, scope exact, origin exact, tsFromInclusive, tsToExclusive |
| critical state | sessionKey exact |
| execution map flat, tree, subtree | origin, ownerUserId, state, quietOverMs, specRefName, specRefSha256, sessionKey |

Filters are conjunctive across fields and disjunctive within a repeated
field. Unknown enum = typed 400. Unknown exact-id filter = empty collection,
never an existence oracle. No `fields`, `sort`, `include`, or join parameters
exist in v1. Every bounded-time filter is an epoch-millisecond integer named
`<field>FromInclusive` or `<field>ToExclusive`. The lower comparison is `>=`;
the upper comparison is `<`. Wakes admit `dueAt` and `firedAt`; turns admit
`createdAt`, `startedAt`, and `endedAt`; facts admit `ts`. A missing bound is
open. Any other time-filter name returns `400 invalid_filter`.

R6a. ExecutionMap roster filters have these exact meanings and validation:

- `origin` is one of `user`, `session`, or `all` and compares the immutable
  creator principal kind.
- `ownerUserId`, `specRefName`, and `sessionKey` are nonempty strings and
  compare exact work-item fields. `sessionKey` compares `createdBySession`.
- `state` is one of `open`, `iceboxed`, `closed`, or `failed`.
- `quietOverMs` is a non-negative integer duration in milliseconds. A node
  matches only when `sinceProgressMs > quietOverMs`, `active.runningTurn` is false, and
  `active.pendingSessionWake` is false.
- `specRefSha256` is a 64-character lowercase hexadecimal string and is valid
  only when the same request has one nonempty `specRefName`. Both fields must
  match the current work-item pin.

Each roster filter occurs at most once. A repeated roster filter, unknown
query key, empty string where nonempty is required, invalid enum, negative or
non-integer `quietOverMs`, invalid SHA, or SHA without `specRefName`
returns `400 invalid_filter` before the query runs. Different roster filters
are conjunctive. The service first removes rows disallowed by AU4a, then
applies these filters; a filter never participates in visibility, edge
derivation, or causal reachability.

The flat cursor fingerprint is canonical JSON of these decoded fields in the
order `origin`, `ownerUserId`, `state`, `quietOverMs`, `specRefName`,
`specRefSha256`, `sessionKey`, with absent values encoded as JSON null.
Changing, adding, or removing one field returns `400 invalid_cursor` before a
row lookup. The signed cursor also binds resource, schema version, exclusive
direction, complete `(createdAt,id)` tuple, and AU7 principal identity. It
contains no selector id, offset, `rowid`, or live locator.

`workItemId` and each `assignmentId` accept a full typed id or a unique typed
prefix through the existing `Tightbeam.IdPrefix` resolver. An ambiguous
visible prefix returns `400 ambiguous_id` with its visible candidate ids in
ascending order. Unknown and invisible selectors follow AU4a's same-404 rule
and never appear in the candidate list.

R7. Projection fields are closed-world and normative. Every item contains
exactly the keys in its row below. Nullable keys remain present with `null`;
an adapter does not omit them. Every notice-backed stored-state item carries
`rowVersion`, a monotonically increasing integer derived at the write seam.
A composed item carries `dependencyVersion` as described in R9 instead. No
adapter may add a storage column or a caller-selected field.

| Resource | Canonical item fields |
|---|---|
| org | `id`, `archetypes`, `hosts`, `modelCatalog`, `dependencyVersion` |
| harness catalog | `harness`, `provider`, `models`, `capabilities`, `dependencyVersion` |
| hosts | `host`, `rowVersion` |
| sessions | `sessionKey`, `displayName`, `kind`, `orderIndex`, `isBuiltIn`, `adopted`, `ownerUserId`, `origin`, `spawnedBy`, `handle`, `archetype`, `overrides`, `identityName`, `identityRevision`, `harness`, `provider`, `model`, `thinkingLevel`, `modelContext`, `host`, `clearedThroughSeq`, `state`, `createdAt`, `updatedAt`, `mechanicalStatus`, `rowVersion` |
| transcript messages | `id`, `seq`, `sessionKey`, `role`, `content`, `at`, `sender`, `deviceId`, `clientMessageId`, `replyToMessageId`, `replyToClientMessageId`, `llmVisibleMessageId`, `attachments`, `attentionTier`, `turnSeq`, `assignmentId`, `jobRef`, `harness`, `provider`, `model`, `effort`, `context`, `rowVersion` |
| work items | `id`, `title`, `specRefName`, `specRefSha256`, `isBug`, `ownerUserId`, `state`, `failReason`, `routingWakeId`, `slateWakeId`, `createdByUser`, `createdBySession`, `createdInTurnSeq`, `createdContextKnown`, `createdAt`, `rowVersion` |
| assignments | `id`, `subject`, `holderKey`, `holderRole`, `holderFallback`, `openedByUser`, `openedBySession`, `openedAt`, `state`, `outcome`, `closedAt`, `closedByUser`, `closedBySession`, `closingAttestId`, `workItemId`, `reviewsAssignmentId`, `holderHarness`, `holderProvider`, `files`, `effectKind`, `derivedStatus`, `rowVersion` |
| attests | `id`, `assignmentId`, `kind`, `verdictKind`, `note`, `bySession`, `byUser`, `producer`, `producerCommand`, `byHarness`, `byProvider`, `commitRefs`, `ts`, `rowVersion` |
| wakes | `wakeId`, `sessionKey`, `targetRole`, `origin`, `prompt`, `consumer`, `dueAt`, `state`, `createdAt`, `firedAt`, `reresolve`, `reresolveSeed`, `reresolveRung`, `conditionKind`, `conditionScope`, `conditionAfterId`, `firedBy`, `creatorSessionKey`, `rumination`, `workItemId`, `assignmentId`, `canceledAt`, `targetGate`, `class`, `classElection`, `deliveryRule`, `digest`, `summon`, `rowVersion` |
| turns | `seq`, `sessionKey`, `messageId`, `wakeId`, `origin`, `prompt`, `roleRef`, `roleFallback`, `assignmentId`, `jobRef`, `model`, `thinkingLevel`, `modelContext`, `harness`, `replyAttention`, `status`, `owner`, `adapterGen`, `requestRef`, `error`, `createdAt`, `startedAt`, `endedAt`, `publishedAt`, `rowVersion` |
| artifacts | `artifactId`, `kind`, `title`, `description`, `createdBySession`, `workItemId`, `parentSession`, `originPath`, `contentSha256`, `recordedMessageId`, `recordedTurnEvidence`, `state`, `home`, `createdAt`, `updatedAt`, `rowVersion` |
| assets | `assetId`, `ownerUserId`, `mimeType`, `size`, `filename`, `createdAt`, `rowVersion` |
| decision requests | `id`, `kind`, `raiserId`, `raiserSessionKey`, `ownerUserId`, `assignmentId`, `expecterSessionKey`, `expecterUserId`, `lineageRung`, `effortGeneration`, `deadlineWakeId`, `raisedAt`, `deadlineAt`, `statuteName`, `question`, `options`, `context`, `status`, `decision`, `rationale`, `ruledBy`, `ruledAt`, `consumedAt`, `withdrawnBy`, `withdrawnReason`, `withdrawnAt`, `askedOfRole`, `answer`, `answeredBy`, `answeredAt`, `rowVersion` |
| read markers | `userId`, `scopeKey`, `marker`, `updatedAt`, `rowVersion` |
| roles | `name`, `boundSessionKey`, `ownerUserId`, `createdAt`, `updatedAt`, `rowVersion` |
| users | `userId`, `isAdmin`, `createdAt`, `rowVersion` |
| devices | `deviceId`, `userId`, `claimedName`, `status`, `platform`, `model`, `createdAt`, `rowVersion` |
| facts (`/api/facts`) | `id`, `ts`, `kind`, `scope`, `origin`, `rowVersion` |
| critical state (`/api/critical-state`) | `sessionKey`, `reason`, `startedAt`, `expiresAt`, `hardDeadline`, `updatedAt`, `rowVersion` |
| toplines | `id`, `ownerUserId`, `title`, `state`, `createdActor`, `createdAt`, `updatedAt`, `closedAt`, `activeWorkCount`, `openConcernCount`, `workMemberships`, `concerns`, `dependencyVersion` |
| execution map node | `id`, `title`, `specRefName`, `specRefSha256`, `state`, `failReason`, `bracket1Armed`, `origin`, `creationContext`, `parent`, `finishedAt`, `assignments`, `jobs`, `attests`, `startedAt`, `closingAttests`, `openDecisionRequests`, `turns`, `minds`, `fanOut`, `active`, `sinceProgressMs` |
| coordination share | `sessionKey`, `from`, `to`, `turns`, `wakeTurns`, `classedTurns`, `coordinationTurns`, `summons`, `algedonic`, `byClass`, `share`, `dependencyVersion` |
| digest members | `wakeId`, `prompt`, `class`, `classElection`, `createdAt`, `dependencyVersion` |
| work-item trace | `workItem`, `assignments`, `causalChildren`, `attribution`, `dependencyVersion` |

R7a. The SQ2 admin resources have these additional closed-world projections.
Nested `documents` entries contain exactly `path`, `content`, and `sha256`.
Their content is deliberate product data after admin authorization, not a
license to expose credentials, environment secrets, or host filesystem paths.
An archetype's `mcpServers` entries contain exactly `name` and `envNames`; the
environment names are sorted and their values never enter the projection.

| Resource | Canonical item fields |
|---|---|
| identity | `name`, `liveRevision`, `state`, `sessionRevisions`, `staleness`, `conflicts`, `rowVersion` |
| archetypes | `name`, `skills`, `where`, `defaults`, `references`, `modelPreferences`, `containment`, `mcpServers`, `compiledGuidance`, `sourceSha256`, `dependencyVersion` |
| kungfu | `name`, `purpose`, `phrases`, `rootArchetype`, `installedRevision`, `status`, `documents`, `rowVersion` |
| guidance | `name`, `content`, `sha256`, `dependencyVersion` |
| rails | `name`, `on`, `mode`, `tool`, `pattern`, `text`, `dependencyVersion` |
| config | `key`, `value`, `updatedAt`, `rowVersion` |
| host environment | `host`, `harness`, `name`, `value`, `valuePresent`, `updatedAt`, `rowVersion` |
| harness processes | `id`, `sessionKey`, `host`, `harness`, `provider`, `model`, `pid`, `state`, `startedAt`, `endedAt`, `rowVersion` |

R7c. `rest-state-api-v1-wire-schema.md` is normative. A route is not frozen
under M1 until its R7/R7a field row and wire-schema row both exist. The wire
schema fixes JSON types, nullability, nested object keys, enum domains, and
array order. An unknown enum value fails serialization and emits no partial
response.

R7b. `/download/:assetId` returns bytes, not a JSON projection. The asset row
is its sole authorization metadata; no inferred artifact or work-item link
grants access. SR2 and AU5 govern the binary adjunct.

R7d. The ExecutionMap node and response metadata use the exact wire shapes in
the companion schema. Their meanings are:

- `origin` reports the work item's immutable creator as
  `{principal,createdBy}`. It records `user` or `session`; it does not infer
  human or agent identity.
- `creationContext` reports `{recorded,turnSeq}` from the work-item row.
  `parent` reports exactly `{status,item}`. `status` is `linked`, `from_turn`,
  `no_turn_observed`, or `unrecorded`; only `linked` has a non-null `item`.
  The server derives a candidate from the creating turn's `jobRef`, otherwise
  its resolved assignment. It removes hidden endpoints before traversal and
  drops the deterministic cycle-closing edge. Appearance filters do not alter
  the candidate graph.
- One normative assignment resolver supplies every aggregate and edge. An
  assignment's non-null `workItemId` wins. Otherwise the resolver follows
  `reviewsAssignmentId` transitively and cycle-safely. Otherwise the result is
  NONE. A resolved assignment contributes to at most one item.
- `assignments` counts open and closed resolved assignments and closed outcomes.
  `jobs` counts distinct holders that have held a resolved assignment.
  `attests` counts allowed attests by stored kind and verdict slug.
  `startedAt` is the earliest allowed resolved assignment `openedAt`.
  `closingAttests` contains completed or surrendered closes with their closing
  attest and nullable commit refs; it excludes revoked closes.
  `openDecisionRequests` counts open statute and effort requests attributed to
  allowed resolved assignments. Agent questions do not enter that count.
- `turns` is the deduplicated union of allowed turns whose `jobRef` is the item
  or whose `assignmentId` is in the allowed resolved set. `minds` is the sorted
  distinct nonempty `(model,context,effort,harness)` stamps in that union.
  `fanOut` counts distinct subagent references carried by allowed resolved
  assignments. A turn that matches both union arms contributes once.
- `active.runningTurn` is true when the allowed turn union has a running turn.
  `active.pendingSessionWake` is true when a current open allowed holder has a
  pending prompt wake. `active.pendingWakeClasses` sums pending prompt-wake
  class counts across those current holders. A closed assignment's former
  holder does not contribute active state.
- `finishedAt` is the time of the latest allowed disposition transition whose
  destination equals the current terminal work-item state. It is null for an
  open item and for a terminal item without such evidence.
- `sinceProgressMs` is evaluation time minus the latest allowed ended turn,
  attest, matching disposition, or coverage-floor timestamp. A scheduled wake
  or fired prod does not reset it.
- `coverage.attributionCutoff` is the causal-event epoch and
  `coverage.basis` is `conservative_shared`. For a work item older than that
  cutoff, `turns.total`, `turns.lastEndedAt`, `minds`, and `fanOut` are null;
  durable assignment and attest values remain populated. `runningTurn` stays
  boolean and `sinceProgressMs` cannot exceed evaluation time minus the cutoff.

The assignments route resolves the complete supplied id set atomically. An
allowed id that resolves to an allowed work item contributes that node once.
An allowed id that resolves to NONE contributes its canonical id to `noItem`.
One unknown or forbidden id makes the complete request the same 404. The tree
and subtree routes nest only appearing nodes. A filter-excluded but visible
parent is not emitted as a placeholder; an appearing child stays top-level and
keeps its `parent:{status:"linked",item:<id>}`.

R8. This table seeds firehose R8. Each listed state mutation has one class,
resource, operation, primary-id ref, and R7 serializer. A class can name more
than one mutation only when the operation differs, as for read-marker set and
clear. A build may expand a grouped row into individual rows, but it may not
change a mapping without a reviewed spec amendment. Observational classes
remain outside this table.

| Firehose state class | Resource | Op | Primary-id notice ref |
|---|---|---|---|
| `work_item.created`, `work_item.updated`, `work_item.iceboxed`, `work_item.reopened`, `work_item.closed`, `work_item.failed` | work items | upsert | `workItemId` |
| `assignment.opened`, `assignment.reopened`, `assignment.closed` | assignments | upsert | `assignmentId` |
| `attest.filed` | attests | upsert | `attestId` |
| `wake.scheduled`, `wake.fired`, `wake.canceled` | wakes | upsert | `wakeId` |
| `prod.fired`, `turn.started`, `turn.ended` | turns | upsert | `turnSeq` |
| `decision_request.opened`, `decision_request.ruled`, `decision_request.withdrawn` | decision requests | upsert | `decisionRequestId` |
| `session.spawned`, `session.retired` | sessions | upsert | `sessionKey` |
| `role.created`, `role.bound` | roles | upsert | `role` |
| `role.removed` | roles | delete | `role` |
| `user.added`, `user.promoted` | users | upsert | `userId` |
| `device.approved`, `device.denied`, `device.revoked` | devices | upsert | `deviceId` |
| `artifact.recorded` | artifacts | upsert | `artifactId` |
| `read_marker.updated` after set | read markers | upsert | `userId` + `scopeKey` |
| `read_marker.updated` after clear | read markers | delete | `userId` + `scopeKey` |
| `message.created` | transcript messages | upsert | `messageId` |
| `condition_fact.filed` | condition facts | upsert | `factId` |
| `critical_lease.updated` | critical state | upsert | `sessionKey` |
| `config.updated` | config | upsert | `key` |
| `host_env.updated` | host environment | upsert | `host` + `harness` + `name` |
| `identity.updated` | identity | upsert | `name` |
| `kungfu.updated` | kungfu | upsert | `name` |
| `host.registered` | hosts | upsert | `host` |

The exact firehose `resource` value for `condition_fact.filed` is
`condition facts`; `/api/facts` is the REST route for that same resource.
The fact projection `id`, notice `refs.factId`, and natural version are JSON
integers with the same positive numeric value; `rowVersion` equals `id`.
`condition_fact.filed` emits once after a successful committed insert.
`critical_lease.updated` emits
once after a committed lease change and uses the R7 version. An idempotent
no-change replay emits no state notice. Both use the same AU4 visibility and
exact R7 serializer as their REST resources, per `art_4a1cce6e`.

SQ2 admits every admin row above. They enter the REST/firehose A6 overlap and
use the same admin-only visibility function. Archetypes, guidance, and rails
are composed identity-tree resources, so R9 governs their refetch contract.

R8b. The event-firehose companion defines four source invalidation mappings
that do not represent rebuildable resources and do not enter the A6 serializer
overlap:

| Firehose source class | Exact successful mutation | Observe refs | Natural source version |
|---|---|---|---|
| `topline.created` | new `Tightbeam.Toplines.create/2` commit | `toplineId` | positive `topline_events.seq` for the appended `topline_created` event |
| `topline_work_membership.linked` | new `Tightbeam.Toplines.link_work/2` commit | `toplineId`, `membershipId`, `workItemId` | positive `topline_events.seq` for the appended `work_linked` event |
| `topline_work_membership.unlinked` | new `Tightbeam.Toplines.unlink_work/2` commit | `toplineId`, `membershipId`, `workItemId` | positive `topline_events.seq` for the appended `work_unlinked` event |
| `subagent_marker.appended` | new row from `Tightbeam.SubagentMarkers.append/3` or `append_in_txn/2` | `markerId`, `sessionKey`; `assignmentId` and `workItemId` when non-null and resolved | positive `subagent_markers.id` |

Each mapping emits exactly one `op:"observe"` notice after a new commit and
none for a refusal, Topline idempotency replay, or ignored duplicate marker.
The notice omits `resource` and carries exactly
`payload:{"sourceVersion":I}`. The companion freezes its complete wire and
emission rules. Topline notice visibility is the parent Topline's AU4
owner-or-admin predicate. Marker notice visibility is AU4a: the marker inherits
its non-null parent assignment grant and also requires its resolved work-item
grant. A null, unresolved, or denied marker assignment delivers no notice to
that principal. Visibility runs before subscription filters. These mappings add no
principal rule, public source route, ExecutionMap class, or shared serializer.

R9. A composed resource has no notice class of its own. It declares the exact
underlying class set that makes a cached instance stale. After visibility
allows a notice and the class matches one of these dependencies, the client
refetches the composed resource. Prefixes below mean every class in R8 with
that prefix.

| Composed resource | Refetch dependencies |
|---|---|
| org | `host.registered`, `config.updated`, `identity.updated`, `kungfu.updated` |
| harness catalog | `host.registered`, `host_env.updated`, `config.updated` |
| toplines | `topline.created`, `topline_work_membership.linked`, `topline_work_membership.unlinked`, `work_item.updated`, `work_item.iceboxed`, `work_item.reopened`, `work_item.closed`, `work_item.failed` |
| execution map | `work_item.*`, `assignment.*`, `attest.filed`, `wake.*`, `prod.fired`, `turn.*`, `decision_request.*`, `session.*`, `user.added`, `user.promoted`, `subagent_marker.appended` |
| coordination share | `wake.*`, `turn.*`, `prod.fired` |
| digest members | `wake.scheduled`, `wake.canceled`, `wake.fired` |
| work-item trace | `work_item.*`, `assignment.*`, `attest.filed`, `session.*`, `wake.*`, `turn.*` |
| archetypes | `identity.updated`, `kungfu.updated` |
| guidance | `identity.updated`, `kungfu.updated` |
| rails | `identity.updated`, `kungfu.updated` |

An R9 dependency list is closed-world. Adding a source table or state class to
a composed query requires the same reviewed change to this list. Each composed
response carries `dependencyVersion` equal to a stable digest of the ordered
`(source kind, stable primary key, natural version)` dependency vector. The
wire schema's `resource` position names that canonical source kind even when
the source is non-resource evidence. Equal dependencies produce equal versions
and any dependency change produces a different version.
R8b source classes participate in these refetch lists but not in direct model
upsert. The list omits `work_item.created` from Toplines because an unlinked new
work item changes no durable Topline bytes. Any new Topline or membership
mutation, or any new source read by either composition, requires one reviewed
R8b/R9 amendment before implementation.

R9b. Durable Toplines dependency extraction is closed over the visible Topline
row, its active `topline_work_memberships`, and the joined visible work-item
rows that supply `workItemTitle` and `workItemState`. The Topline row's natural
version is the greatest positive `topline_events.seq` for its id. An active
membership's natural version is the positive sequence of its `work_linked`
event. A joined work item uses its canonical R7 `rowVersion`. Link and unlink
touch the parent Topline and append the corresponding event in the same
transaction; unlink also removes the membership from the active dependency
vector. The ordered vector therefore changes for every current durable
Toplines mutation and for every work-item mutation that changes nested Topline
bytes. Extraction runs after AU4 visibility, so a hidden source row cannot
change the digest or response. The vector's canonical source-kind labels are
exactly `toplines`, `topline work memberships`, and `work items`; each stable
primary key is that source row's canonical id string.

R9a. ExecutionMap's query dependency extraction is closed over these source
rows: visible work items; assignments resolved to them; allowed attests;
allowed turns by `jobRef` or resolved assignment; allowed pending prompt
wakes for current holders; open statute and effort decision requests for
allowed resolved assignments; allowed subagent markers carried by those
assignments; allowed disposition-transition causal events; the causal-event
coverage epoch; and the session and user rows required for source visibility.
The R9 class row is the invalidation projection of that exact source set.
Disposition transitions invalidate through the corresponding existing
`work_item.*` mutation. An independent successful
`SubagentMarkers.append/3` or `append_in_txn/2` insertion invalidates through
`subagent_marker.appended`; an ignored duplicate emits none. No `turn.*`
notice is a proxy for a marker commit, and no ExecutionMap class exists.

ExecutionMap builds its dependency vector only after AU4a source visibility.
A hidden source row cannot change `dependencyVersion`, an aggregate, order,
nesting, filter outcome, or response bytes. For an underlying R7 resource, the
vector uses its canonical primary key and `rowVersion`. For non-resource
append-only evidence, a disposition-transition causal event uses the exact
triple `("causal events", seq, seq)`, where both `seq` values are the same
positive `causal_events.seq` JSON integer. A subagent marker uses the exact
triple `("subagent markers", id, id)`, where both `id` values are the same
positive `subagent_markers.id` JSON integer. The fixed coverage epoch uses the
exact triple `("causal events epoch", "causal_events_epoch", epoch)`, where
`epoch` is the stored positive epoch-millisecond JSON integer. These literal
source-kind labels, key types, and version types are part of the dependency
digest input. Query dependency
extraction and this R9a source list must match exactly.

Evaluation time is not a dependency row. `sinceProgressMs` and a
`quietOverMs` result can therefore change while `dependencyVersion` stays
equal. The digest is an invalidation aid, not an entity tag or response hash;
R4a's `no-store` rule prevents time-derived output from becoming a cache
promise.

R10. `rowVersion` has resource-key lifetime. The write seam allocates it from
a durable monotonic sequence and stores a version floor keyed by
`(resource, primary key)`. An upsert version exceeds the prior upsert or delete
version for that key. A delete notice carries a version greater than the row's
last upsert. Recreating a hard-deleted key carries a version greater than that
tombstone. Version floors survive process restart and are never collected
while a v1 client can present buffered notices.

## Requirements — projections and serializers

SR1. Code structure enforces one query function and one public serializer
per resource. The REST adapter, CLI read wrappers, and firehose publisher
call those seams. For every rebuildable-state class in firehose A6, the
REST detail item and notice payload are byte-equivalent after envelope
removal.

SR2. Secrets are structurally excluded: sessions omit `cliToken`, devices
omit `token`, harness processes omit `identityToken` and any
credential-bearing path or env value; host-env and config expose safe
values only. A test greps every projection (firehose A6).

SR3. Projections carry the resource's full product fields and user
content, unredacted after authorization (Mike's payload ruling as refined
in firehose V3): "unredacted" governs content, never storage secrets.

SR4. Ids are the correlation contract: each projection's primary id equals the
id the firehose notice `refs` carry (firehose V5 and its primary-key table).
Public projection fields literally named `id` are strings except
`facts.id`; `facts.id` and `refs.factId` are JSON integers, and their numeric
values must equal each other and `facts.rowVersion`. A decimal string is not
an equivalent fact id. Other primary-key and ref fields use their exact wire
types. A client applies last-version-wins upsert by `(primary id,
rowVersion)`.

SR5. Safe-value exposure is explicit and default-deny. In v1 the complete
config value allowlist is `default-archetype`. No other config key returns a
value: every live key remains visible to an admin as metadata, but its `value`
is `null`. Unknown detail means the key does not exist, not that its value is
hidden. The host-environment value allowlist is empty: its route
may return `host`, `harness`, `name`, `valuePresent`, and timestamps, but its
`value` is always `null`. Identity, kungfu, and harness-process projections
return only the R7a fields. Archetype, kungfu, rail, and guidance content is
admitted only through its named R7a projection after admin authorization; it
does not widen the config or environment allowlists. Any unlisted projection
field remains absent. An existing config key outside the value allowlist keeps
its metadata row with `value:null`; other unknown detail keys return 404. A new
safe value or projection field requires a reviewed amendment; a name-pattern,
denylist, or “not known secret” test cannot admit it.

SR6. Admin content is source-bound and sanitized. Archetypes and compiled
guidance read only the committed served-identity tree at its live revision.
Guidance reads only built-in served guidance and `identity/guidance/*.md`.
Rails read only parsed `identity/rails/*.toml` statutes. Kungfu `documents`
read only `README.md`, `capabilities.md`, and `preferred-models.md` beneath
`identity/kungfu/<name>/`; symlinks, `..`, dotfiles, receipts, manifests, and
all other paths are excluded. `documents.path` is relative and matches
`^[A-Za-z0-9][A-Za-z0-9._/-]*$`.

Before serialization, one content sanitizer replaces a full secret-bank
value, a PEM private-key block, a bearer/API-token assignment, or an absolute
path rooted in the Tightbeam base directory or an operating-system home
directory with `[redacted-secret]` or `[redacted-host-path]`. It runs on
`compiledGuidance`, guidance `content`, kungfu document `content`, and rail
`pattern` and `text`. It never reads environment values to enrich output. The
same sanitized item bytes serve REST and firehose.

SR7. ExecutionMap has one composed query family and one public node serializer:
the exact seams in R3b. Flat, tree, subtree, and assignment selection call the
same membership resolver, source loader, telemetry builder, edge builder, and
`execution_map_node/1`. Tree assembly adds only the schema-declared `children`
key. The assignments adapter adds only `noItem`. A route-local node map or a
second membership, edge, visibility, or serializer implementation is a
contract failure. These seams are separate from durable Toplines and do not
change the six shared serializer shapes adopted by `art_b1995a26` / fact 1093.

## Requirements — auth and visibility

AU1. `Authorization: Bearer <existing gateway credential>`. A device
token resolves to its user. A session CLI token resolves to that session
only. The session row's `ownerUserId` is metadata, not an automatic authority
escalation. An owner read exists only where AU4 explicitly grants it.
No new credential type exists. The optional `asUser` GET parameter is not a
credential and never authenticates a request.

AU2. The org CLI token names no principal by itself. For a CLI GET,
`asUser=<userId>` transports the same principal selection as the existing
dispatch `asUser` field. The GET adapter passes the decoded value through the
existing CLI principal resolver without normalization or an existence lookup.
An org bearer plus one `asUser` value therefore resolves to the same
self-declared, unverified user principal that dispatch resolves today. An
unknown nonempty user id is not rejected or bound; AU4 simply evaluates that
resolved principal. An org bearer without `asUser` returns the existing
dispatch `400 invalid_message` identity-required error. An empty value returns
the same result as an empty dispatch `asUser` value. Repeated `asUser` query
keys return `400 invalid_as_user` before principal resolution because dispatch
has only one `asUser` field. Malformed percent encoding returns
`400 malformed_query` before principal resolution.

For a session bearer, the existing resolver still verifies `asUser` against
the session owner and the resolved principal remains that session; a mismatch
returns `403 identity_not_yours`. Its R4b error message is exactly
`"this session belongs to <session.owner_user_id>"`, with
`<session.owner_user_id>` replaced by the target session row's exact stored
non-null owner user id. For a device bearer, `asUser` cannot replace or elevate
the credential-resolved user principal; its presence returns
`400 invalid_as_user` before principal resolution. No case creates a
credential, a new binding, an authorization grant, or tailnet-identity
behavior. The canonical read service takes the resulting RESOLVED principal,
so this migration changes only transport, never authorization.

AU3. Visibility: collections omit rows the principal cannot read; detail
returns the same 404 for unknown and forbidden (transcript precedent);
admin resources refuse non-admins. AU4 is the complete per-resource allow
matrix. REST and firehose use the same named visibility function for each
row. Anything the matrix does not grant is denied.

AU4. Per-resource allow matrix. “Owner” means the named user principal, not
any session that happens to carry that user's id. “Session owner” is an
explicit grant to the user principal that owns the target session. Admin is
the authenticated user principal with `isAdmin=true`; a session token does
not borrow that bit.

| Resource | Allowed principals |
|---|---|
| org, harness catalog, hosts, roles | any authenticated user or session in the org |
| sessions | target session; target session owner; admin |
| transcript messages, coordination share | target session; target session owner; admin |
| work items, work-item trace | work-item owner; creating session; a session that holds an assignment on the item; admin |
| assignments | holder session; work-item owner; opener when the opener is a user or session principal; admin |
| attests | any principal allowed to read the parent assignment |
| wakes | target session; creator session; target session owner; creator session owner; admin |
| digest members | any principal allowed to read the digest-carrier wake |
| turns | target session; target session owner; admin |
| artifacts | creating session; work-item owner; any principal allowed to read the linked work item; admin |
| assets | asset's `ownerUserId` user principal; admin |
| decision requests — statute | raiser; `ownerUserId` user principal; admin |
| decision requests — effort | named expecter session or user; holder of the linked assignment; admin |
| decision requests — agent question | asker session; asked session; stamped accountable owner user; admin |
| read markers | marker's `userId` user principal; admin |
| facts | filing session; filing session owner; admin; process-origin facts are admin-only |
| toplines | topline owner; admin |
| execution map | derived source-by-source under AU4a; no independent grant |
| critical state | admin only |
| identity, archetypes, kungfu, guidance, rails, config, host environment, harness processes, users, devices | admin only |

AU4a. ExecutionMap authorization composes existing AU4 grants and introduces
none. A node requires the work-items grant for that principal and item. An
assignment contributes only when the principal also has the assignments grant.
An attest requires its parent assignment grant. A wake or turn requires its
own AU4 grant and the relevant resolved assignment or work-item grant before it
can affect telemetry. A decision request requires its kind-specific AU4 grant
and its resolved assignment grant. A subagent marker requires its parent
assignment's grant and the resolved work item's grant before it contributes to
a node. A disposition event inherits its parent work item's grant.
Session and user rows are consulted only by the existing principal resolver and
the named underlying predicates; they create no ExecutionMap-only owner or
admin borrowing.

The service applies those predicates before membership, aggregation, edge
derivation, filtering, pagination, dependency-vector construction, and
serialization. A parent link requires both endpoint work items to be visible.
Collections omit denied nodes and denied contributors. A subtree anchor
requires the work-item grant. Each assignments selector first requires the
assignment grant; an assignment resolved to an item also requires the
work-item grant. A visible assignment resolving to NONE appears in `noItem`.
One unknown or denied selector makes the complete selector request the same
`404 not_found` body, headers, statement shape, and AU8 timing class.

Twin-world byte identity is normative: for the same principal, request,
evaluation time, and allowed rows, a database containing denied source rows
produces byte-identical ExecutionMap output to a database where those rows are
absent. This applies to flat, tree, subtree, and assignment-selection routes.

AU5. Nested routes and binary downloads authorize each hop. A nested child
is returned only when the caller may read both the parent and the child.
`/api/assignments/:id/attests`, `/api/wakes/:wakeId/digest-members`, and every
nested item apply that intersection before lookup results leave the service.
`/download/:assetId` resolves the exact asset metadata row, applies the asset
visibility function, and only then opens bytes. Unknown
parent, unknown child, forbidden parent, forbidden child, and forbidden
download all return the identical 404 body, status, headers, and timing class.

AU6. Visibility filtering always runs before subscription filtering. The
server first evaluates the R8 row or R8b source through its named AU4
visibility function for the authenticated principal. Only an allowed row may then be tested against
`classes`, `sessionKey`, `workItemId`, `origin`, or `principal` subscription
filters. A subscription filter never broadens visibility and never becomes an
existence oracle. Delete uses the last pre-delete projection for this first
step, as firehose A2b requires.

AU7. Cursor error precedence is deterministic. Base64/version/signature,
resource, and filter-fingerprint failures return `400 invalid_cursor` without
a row lookup. A valid cursor also binds the authenticated principal kind and
stable principal id. A binding mismatch returns the same 404 as unknown. For
the correct binding, rows hidden now or hidden since cursor creation are
simply absent from the authorized page; the server never reports that they
exist. “Unauthorized cursor use” means a binding mismatch or a request whose
resource itself is forbidden.

AU8. “Same timing class” means unknown and forbidden paths use the same
handler stages, database statement shape, response encoder, and optional
minimum-duration pad. In a warmed in-process test of at least 10,000 randomized
requests per case, forbidden and unknown p50 and p95 latency must each differ
by no more than 5%, and neither case may perform a byte open. The test records
the statement count and requires exact equality. Production network latency is
not part of this conformance measure.

## Requirements — relationship to the CLI

C1. In the final v1 shape, every retained CLI shared-state read calls the
corresponding REST GET and may only select, compose, summarize, or format
that response. A wrapper that currently sends dispatch `asUser` sends the
same value as the GET `asUser` parameter. During M4 migration, the existing
dispatch adapter may remain; both transports resolve the same principal and
call the same canonical query function and serializer. No CLI read keeps a
second query or serializer implementation.

C2. New flexible reads are designed REST-first; the CLI gains a wrapper
only when a common agent task wants one line. `doctor` stays local (it
probes the host, it is not a state resource).

## Migration (order is normative)

M1. Freeze R7 projections, R8 mappings, R9 dependency lists, and AU4
visibility functions. M2. Add REST routes on
those seams. M3. Point the firehose payload builders at the same
serializers. M4. Point CLI read handlers at the canonical read services.
Move each wrapper from dispatch to its REST GET using the existing bearer plus
AU2's `asUser` principal selection where required. Remove its legacy dispatch
read path after parity acceptance passes. This transport move does not change
item shapes, authorization, or the M1 query and serializer seams.
M5. Keep current routes only as migration aliases (/api/streams,
/api/org-options, /api/session-status, /api/work[/:id],
/api/trackable-sessions, /harnesses); no new client may adopt them. M6. Migrate
Clawline (streams/status aliases → sessions + transcript GETs). M7. Migrate
ATC off direct SQLite. M8. After M4, M6, and M7 parity acceptance passes,
remove the listed aliases and every legacy dispatch read path. Dispatch write
verbs remain. No breaking removal lands before its client moves.

SQ4 is ruled REST-first: M2 ships before M3. The firehose is the freshness
plane, while REST is the rebuildable state source. A client must be able to
snapshot supported state before it relies on live notices. This sequencing
ruling does not change projections, authorization, or serializer identity.

## Acceptance

A1. Table-driven per-mutation test: every rebuildable-state firehose class has
exactly one R8 row naming resource, op, primary-key refs, R7 serializer, AU4
visibility function, and `rowVersion` source. Every R8b source invalidation has
exactly one mapping naming its successful commit, observe refs, natural source
version, and AU4 visibility predicate. The test fails on a missing or extra
state mutation or source mapping.
A2. For every non-observational rebuildable-state class governed by
firehose A6, the REST detail item equals the notice payload after envelope
removal.
A3. Closed-world projection proof: every collection and detail item has
exactly its R7 keys and no others. The secret-exclusion sweep rejects
`cliToken`, device `token`, `identityToken`, credential paths, environment
secrets including MCP environment values, and every value outside SR5's
explicit allowlist.
A4. Subscribe-first multi-resource snapshot plus buffered notices converges
under concurrent creates/updates/deletes by last-version-wins upsert on
`(primary key, rowVersion)`; reconnect + fresh rebuild converges with no event
history. An older snapshot row applied after a newer notice is a no-op. Delete
and recreate the same role name across a process restart; the recreate version
exceeds the tombstone and stale pre-delete notices cannot remove it.
A5. Pagination proofs: tied timestamps, a deleted boundary row, deleted
neighbors, empty pages, before/after, default 50, cap 500, wrong-resource
cursor, and changed-filter cursor. Tests decode each cursor and prove it holds
the complete R5a tuple and no SQLite `rowid` or live storage locator. While
paging host environment and read markers, update every visited row; their
immutable natural-key order produces no skip or duplicate.
A6. Unauthorized detail, nested child, cursor use, and download are
indistinguishable from unknown in body, status, headers, and the AU8 measured
timing class. Malformed, wrong-resource, changed-filter, wrong-principal, and
now-hidden-row cursor cases each assert AU7 precedence.
A7. ATC builds its current model with zero SQLite access; Clawline lists
sessions, pages transcript, fetches work state, and correlates notices
by exact ids.
A8. CLI wrappers return the same item shapes as REST for equivalent
reads.
A8a. A table compares direct GET with dispatch for an org bearer plus known,
unknown, empty, and missing `asUser`, and for a session bearer plus absent,
matching-owner, and mismatched-owner `asUser`. Both transports produce the
same resolved principal or refusal and the same allow, deny, omission, and
same-404 results. Separate GET cases prove repeated parameters and device
bearer plus `asUser` return `400 invalid_as_user`, and malformed percent
encoding returns `400 malformed_query`, all before principal resolution. The
test proves that the parameter adds no credential, binding, authorization, or
tailnet-identity behavior.
A9. Read-marker pagination creates two users with the same `scopeKey`;
paging each authorized view visits
every `(userId, scopeKey)` exactly once.
A10. For every AU4 row, a table tests each allowed principal and one denied
session owned by an otherwise allowed user. The denied session remains denied
unless the row explicitly grants that session itself.
A11. Subscription-order proof: create a row hidden from the subscriber that
matches every supplied subscription filter. The visibility function runs,
returns false, and the filter matcher is not invoked. Repeat for a delete
using the last pre-delete projection. No frame or distinguishable error leaks.
A12. Nested and download proof: authorize the parent but deny the child, then
deny the parent while authorizing the child. Both cases equal the unknown 404.
An asset denied by its metadata visibility function never opens or stats its
bytes, including for a session owned by the asset's `ownerUserId`.
A13. Safe-value proof enumerates all live config keys and host environment
names. Only `default-archetype` returns a config value; no host environment
value returns. An unlisted live config key appears with `value:null`, and its
`config.updated` notice carries the identical redacted item.
A13a. After M4, M6, and M7 parity passes, every M5 alias and legacy dispatch
read path is absent. The corresponding canonical REST GET still passes its
contract tests, and every dispatch write verb remains available.
A14. Every unblocked R9 composed view has a test that mutates one row for each
declared dependency and observes a changed dependency digest. A state class
not in the declared list leaves the digest unchanged. Query dependency
extraction and the R9 list must match exactly.
A15. A session token reads its own session-scoped rows. It cannot read another
session, an owner-only read, an owner read marker, or an admin resource merely
because both sessions share `ownerUserId` or that owner is admin.
A16. An admin can list and fetch each SQ2 resource, including archetype,
kungfu, rail, and guidance content. A user or session principal receives the
unknown 404 for every one. Archetype MCP entries expose sorted environment
names but never commands, arguments, values, or host paths. Fixtures place a
secret-bank value, PEM block, token assignment, Tightbeam base path, home path,
symlink, `..`, receipt, and non-allowlisted kungfu document in every admitted
content source; SR6 redacts or excludes each and preserves ordinary prose.
A17. The wire-schema suite validates every R7/R7a item against its exact JSON
types, nullability, nested keys, and enum domain. It randomizes input map and
set order 1,000 times and requires byte-identical item serialization and
dependency digests. The ExecutionMap cases include the literal causal-event,
subagent-marker, and coverage-epoch triples from R9a and reject a changed
source-kind label, key type, or version type. Semantic sequences retain their
declared order.
A18. Facts and critical-state rows have immutable cursors, complete R7 wire
schemas, AU4 visibility tests, and exactly one R8 state mapping. The suite
fails if either companion firehose class is absent from the adopted registry.
For `condition_fact.filed`, it also requires the exact `condition facts`
resource value and integer equality across item `id`, `refs.factId`, and
`rowVersion`. For both companion classes, it tests an allowed and denied
principal through the shared AU4 function, then applies older, duplicate, and
newer snapshots and notices in both orders to prove per-primary-key
last-version-wins convergence.

A19. Given one durable Topline linked to a work item and one ExecutionMap node
for that item, when a client calls `/api/toplines/:id` and
`/api/execution-map`, then the first response has the unchanged durable
Toplines R7 shape and the second has the R7d execution shape. Neither response
contains a field from the other shape, and no `/api/toplines` route invokes an
ExecutionMap seam.

A20. Given two visible work items with the same `createdAt`, when the client
pages `/api/execution-map` forward and backward with `limit=1`, then both items
appear once in `(createdAt,id)` order. Decoding each signed cursor yields the
complete tuple, resource, direction, schema version, filter fingerprint, and
principal binding, with no offset, `rowid`, selector id, or live locator.
Deleting the boundary item before the next request does not change the page.
Given absent `limit`, valid `500`, and valid `501`, the route uses 50, 500, and
clamped 500 respectively. Given empty, zero, leading-zero, negative, signed,
decimal, exponent, whitespace, non-ASCII-digit, non-integer, or repeated
`limit`, it returns `400 invalid_filter` before a row lookup.

A21. Given a flat request with each valid R6a filter, when the request runs,
then visibility removes denied rows before the conjunctive filters run and the
result matches the stated field or quiet predicate. Given a changed filter,
dependent SHA without name, repeated roster filter, unknown key, malformed
SHA, negative `quietOverMs`, or a cursor from another filter set, when the
request runs, then it returns the specified 400 before a row lookup or node
serialization.

A22. Given visible linked descendants, a filter-excluded visible parent, an
invisible parent, a multi-node cycle, and a self-cycle, when `/tree` and
`/subtrees/:workItemId` run, then each route is unpaged, uses deterministic
root and sibling order, preserves the filtered visible parent id without a
placeholder, conflates the invisible parent with `from_turn`, and drops the
deterministic cycle-closing edge. Unknown and forbidden subtree anchors return
byte-identical 404 responses.

A23. Given repeated `assignmentId` values containing one allowed assignment
resolved to a visible item and one allowed assignment resolved to NONE, when
`/api/execution-map/assignments` runs, then it returns the item once and the
NONE id once in sorted `noItem`. Given an empty set, roster filter, or paging
parameter, it returns `400 invalid_filter`. Given one unknown or denied id
beside allowed ids, it returns the all-or-nothing same 404 and exposes no
partial item or `noItem` value.

A24. Given a visible item with resolved assignments, attests, turns, wakes,
decision requests, markers, dispositions, and a candidate parent, when one
source row is denied under its existing AU4 predicate, then that row affects
no count, clock, active flag, mind, fan-out, parent, order, filter result, or
dependency version. A twin database without the denied row produces
byte-identical output on all four routes, equal statement counts, and AU8
latency within the existing bound.

A25. Given an own-pinned review assignment, a null-pin transitive review, a
cycle, a turn with both `jobRef` and `assignmentId`, a closed former holder,
and a current holder with a pending classed wake, when the node is serialized,
then membership attributes each assignment to at most one item, the turn
counts once, the former holder contributes only historical `jobs`, and only
the current holder contributes pending wake state. Given a pre-cutoff item,
the four coverage-dependent fields are null and `sinceProgressMs` respects the
coverage floor.

A26. Given one new allowed marker insertion and one ignored duplicate, when
contract tests inspect the R8b registry, R9a extractor, and flat, tree,
subtree, and assignment routes, then the insertion emits exactly one
`subagent_marker.appended` notice after commit and the duplicate emits none.
Each route calls the named query family, source-derived visibility composition,
and sole node serializer; the extractor names exactly the R9a source set and
the refetch changes marker-backed `fanOut`. The registry has no ExecutionMap
class, durable Toplines bytes are unchanged, and the six `art_b1995a26`
serializer bytes remain unchanged.

A27. Given each ExecutionMap success, auth failure, invalid `asUser`,
mismatched session-bearer `asUser`, missing org-principal selection, malformed
query encoding, invalid filter, invalid cursor, ambiguous visible prefix,
unknown selector, forbidden selector, and projection failure, when the response
is encoded, then each success has status 200 and the exact R4a and wire-schema
body, each error has its specified status and exact R4b body, and every response
has the exact application headers. The mismatched session-bearer case has
status 403 and exact error bytes with `code` followed by `message`; the message
uses the target session row's exact stored non-null owner user id. The test
compares exact encoded bytes for every success envelope and closed error
variant and rejects an unauthorized message, extra key, wrong key order, or
extra application header. `identity_not_yours` is the sole message-bearing
variant. Unknown and forbidden selectors have identical body and application
headers. An unpaged response has no `page`; a projection failure emits no
partial JSON.

A28. Given one new Topline create, link, and unlink commit plus an idempotent
replay of each, when the firehose and Toplines composition are exercised, then
the new commits emit exactly `topline.created`,
`topline_work_membership.linked`, and
`topline_work_membership.unlinked`, respectively, and the replays emit none.
Every notice has the exact R8b observe wire, passes owner-or-admin visibility
before filters, and triggers a refetch whose `dependencyVersion` changes. A
work-item title update or disposition change for an active membership also
changes the refetched Topline digest and nested bytes; `work_item.created`
alone does neither. Older, duplicate, and newer source notices cannot be applied as a
Topline upsert.

A29. Given each R8b class and subscriptions that independently set `classes`,
`sessionKey`, `workItemId`, `origin`, and `principal`, when the source commits,
then the firehose applies the exact R8b filter-value rules after visibility.
An exact present ref matches, a different or absent ref does not match, and
the four mappings never match `origin` or `principal`. A hidden source does
not invoke the subscription matcher. A client holding an R9 view subscribes
to its dependency classes plus any ref filters whose R8b rows define values.

## Open questions — Spirit questions for Mike

SQ1. **RULED 2026-08-25 — transport existing `asUser`.** Remove the
prohibition on an `asUser` GET parameter. It only transports the CLI's
existing principal selection and adds no credential, binding, authorization,
or tailnet-identity behavior. Message
`s_21b93fdd-5e62-4ed9-ac7e-923697463936` supersedes only the contrary
parameter prohibition in the adjudication and recon baseline. M4 direct REST
CLI reads may proceed under AU2.

SQ2. **RULED 2026-08-22 — expose.** REST v1 includes admin-only users,
devices, host-environment metadata, harness processes, identity publication,
installed kungfu, safe config values, and first-class archetype, kungfu, rail,
and guidance content. The R7/R7a closed field lists, SR2/SR5 exclusions, and
AU4 admin-only row are the ruling's security boundary.

SQ3. **RULED 2026-08-25 — remove after migration.** Remove every M5
compatibility alias and legacy dispatch read path after M4, M6, and M7 parity
acceptance passes. Do not remove an alias before its client moves. Dispatch
write verbs remain. Authority is message
`s_21b93fdd-5e62-4ed9-ac7e-923697463936`.

SQ4. **RULED 2026-08-23 — REST-first.** Build the shared M1 seams, ship M2
REST as the rebuildable state source, then ship the M3 firehose freshness
plane. Mike's direct auto-adjudication message
`s_75aeaab2-94e1-4a80-ab87-004570ec75a9` is the ruling authority. The ruling
does not change projections, authorization, or serializer identity.

SQ5. **Open; non-blocking because v1 remains bearer-only.** Tailnet identity:
wi_bdf9a537 (gateway behind tailscale serve) would
add tailscale identity headers — should AU1 anticipate accepting tailnet
identity as a principal source once that lands, or stay
bearer-credential-only in v1?

SQ6. **RULED 2026-08-25 — preserve marker-backed `fanOut`.** Add exact
`subagent_marker.appended` source invalidation through the event-firehose
companion. Do not use `turn.*` as a proxy and do not add an ExecutionMap class.
Authority: `att_d5b0a440-bd51-498f-8b96-e6512fedf68f`.

SQ7. **RULED 2026-08-25 — preserve durable Toplines with notices.** Add exact
source invalidation mappings and durable versions for Topline and
topline-work-membership mutations. No snapshot-only or no-notice exclusion
exists. Authority: `att_d5b0a440-bd51-498f-8b96-e6512fedf68f`.

SQ8. **RULED 2026-08-25 — pre-build evidence boundary.** Deterministic spec
lint and fresh independent exact-byte review are this amendment's pre-build
gate. Acceptance clauses remain executable and decidable. Product tests and a
`tests-passed` receipt belong to the later implementation card; this spec-only
assignment does not implement or claim them. Authority:
`att_d5b0a440-bd51-498f-8b96-e6512fedf68f`.

Deleting `fanOut` or Toplines would remove current product meaning. Accepting
snapshot-only or no-notice freshness would break I5 and the live display-model
outcome. Those subtraction alternatives therefore lose to the four bounded
source invalidation mappings above.
