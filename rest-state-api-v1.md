# REST state API v1 — the read plane (product spec)

Status: CANONICAL r4, 2026-08-25. r4 incorporates the landed ExecutionMap,
source-invalidation, Toplines/session lookup, and AU2 parity amendments. The
ExecutionMap amendment distinguishes durable Toplines from the mechanical
ExecutionMap and adds the REST-only ExecutionMap contract. Its firehose
companion adds source invalidation notices for existing durable Topline and
subagent-marker commits; it adds no ExecutionMap class. The Toplines/session
amendment adds the durable `/api/toplines` `(createdAt,id)` cursor and closed
`state` filter plus the exact sessions `displayName` lookup used by
`transcript --name`. It leaves the ExecutionMap/firehose companion, R7 items,
authorization, and public serializers unchanged.

G2 session-freshness landing, 2026-08-27: adds the complete session mutation
mapping shared with `event-firehose-v1.md`. It adds `session.updated` and fixes
session versioning, correlation, cold-start, reconnect, and gap recovery. It
changes no R7 session field, route, visibility grant, write surface, target, or
release authority.

G7 detail-route candidate, 2026-08-27: make each collection-only R8 resource
addressable by its canonical public key. The routes use the existing shared
query, visibility, serializer, and outer-envelope seams. This amendment adds
no R7/R7a field, R8 class, authorization grant, REST-local projection, or
second wire shape.

G4 error-contract successor, 2026-08-26: PROPOSED. This amendment applies one
closed typed error envelope to the canonical `/api` read routes in R2, R3, and
R3a. It changes no success envelope, resource label, R7/R7a item, R8/R8b
mapping, authorization grant, cursor, compatibility alias, `/version`
response, `/download/:assetId` response, firehose frame, or encoded
ExecutionMap error. The exact candidate set for G4 is this file and
`rest-state-api-v1-wire-schema.md`; it requires fresh independent review
before implementation or specRef binding.

Review history: exact review
`att_90efe520-f84c-4d3b-bd09-9c36f8a0ff08` requested changes on exact
`e4a27977477a25c3037bba164db2bc1d508bcd7a`; full report `art_bffa387b`
supplied findings F6-F7. Product-owner ruling
`att_c0fee9c0-3489-4a57-b981-080fbcca4f66` preserved the existing
message-bearing session-owner refusal and restored R6 while keeping
ExecutionMap-scoped R6a. Earlier F1-F5 and SQ6-SQ8 rulings remain
incorporated.

G1 current-main composition successor, 2026-08-27: PROPOSED. This amendment
composes the accepted `messageType` F1/F2 behavior onto canonical
`277bb5031a06270aabbc57e3c222cbd2ec89bc73`. Exact candidate `b53b1f5f` passed
the G1 behavior review but requested current-main composition in verdict
`att_adea7aeb-5448-4286-8cad-4fe250e1648c` and report `art_a3fc1d81`.
Product-owner disposition `att_e0a20ce9-3bcc-4a0c-800f-681a51cd85c4`
preserves F1/F2 and requires unique current-canonical clause identifiers. This
successor changes no G4 error or G8 authority-label behavior.

Revision history: r3 folded the REST-side adjudicated findings
F1/F8/F9/F13/F14/F16/F21/F22 from
`review-gate-observability-2026-08-21.md` and aligned with firehose r6. It
resolved changes-requested `att_71210c7b` against exact commit
`c8eb1d080890ad571c5319b2514230c71a021427`; its closure map is in the
adjudication companion. r3 also consumed Mike's ruled SQ2: the admin read plane
includes users, devices, ops metadata, and first-class archetype, kungfu, rail,
and guidance content, all admin-only with secrets structurally excluded. r2
folded the reviewed mechanical amendment
`art_8e2d8444` (reviewed-clean `att_0b648694`): adopted route/filter
inventory, interim/final CLI transport, firehose serializer scope, the
R12-to-M5 repair, and the harness-catalog compatibility ruling. Written
by tb02 and product-owner:rest-state-api. Untargeted (0.2.0 or
later); when build work starts it branches from main tip. The current contract
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
- Mike's firehose gap remediation ruling, message
  `s_fe001c27-c509-4cf6-8866-47defe5eaa21` (2026-08-27), accepts recon verdict
  `att_556f55ae-f1d2-4c83-b55d-9daf06aae929` and report `art_1d389e8e`.
  It makes G2 session freshness a read-side firehose prerequisite and leaves
  G1 and G3-G8 outside this amendment.
- Mike's rulings, 2026-08-25: remove the `asUser` GET prohibition. The
  parameter only transports the CLI's existing principal selection and adds
  no credential, binding, authorization, or tailnet-identity behavior. After
  client parity, remove legacy dispatch-read transport and compatibility
  aliases; dispatch remains the write plane. Durable authority is message
  `s_21b93fdd-5e62-4ed9-ac7e-923697463936`. This ruling supersedes only the
  contrary “no asUser query parameter” clauses in rest-vs-cli-adjudication.md
  r2 and its adopted recon baseline.
- Product-owner R3 ruling `att_2d3a8333-a1d2-478f-9b0a-f8fb75b795df`, which
  consumes D1 verdict `att_8eaa2c03` and report `art_3990b5e1`: for AU2,
  the existing dispatch resolver verifies a matching session `ownerUserId`
  and resolves `{:user, ownerUserId}`; a mismatch returns
  `403 identity_not_yours`. It rules the contrary canonical AU2
  session-principal phrase a mechanical defect.
- session-tokens-v1.md defines the Dispatch call-map principal seam for its
  stated consumers. R3 is the more-specific authority for AU2's REST
  transport parity; this spec neither changes that seam nor creates a second
  resolver.
- rest-state-api-r3-adjudication.md: durable REST finding text, source
  message identifiers, the closure map, and the SQ2 ruling pointer.
- rest-state-api-v1-wire-schema.md: normative JSON types, nested shapes,
  enum domains, nullability, and canonical ordering for R7/R7a.
- Companion mapping ruling `art_4a1cce6e`, SHA-256
  `5db8aab3496747d008fb8c024a4f1617f92695d144c89481bca3a1f20842550a`:
  condition facts and critical leases enter firehose R8 with the exact R8 rows
  below; it supersedes the fact-only `art_5d8bacb2`.
- Firehose client-buildability recon verdict
  `att_556f55ae-f1d2-4c83-b55d-9daf06aae929` and report `art_1d389e8e`
  identify G1. Mike's 2026-08-27 remediation ruling adopts one canonical
  transcript-message discriminator across fetched rows and the firehose.
  Prior product commit `505b56aa29f151faab7cd9618ca1bba922cff357`
  supplies the additive values and compatibility behavior.
- ExecutionMap authority: `topline-map-v1.md` plus product source
  `Tightbeam.ExecutionMap` at `d00e06aea578d711e608637d38a97872487df15e`.
  Durable `Tightbeam.Toplines` at that revision remains a separate source.
  D2 `wi_ea98345b-51f4-4fae-b7df-3670c0d54f6b` and D3
  `wi_113442f5-22ae-457b-a971-1b620069d490` consume this amendment; they do
  not define its contract. The adopted six-resource seam contract remains
  `art_b1995a26` / fact 1093 and is unchanged.

## Spec homing

The canonical spec lives only in the `tightbeam-specs` repository as
`rest-state-api-v1.md`. Canonical r4's coupled set is
`rest-state-api-v1.md`, `rest-state-api-v1-wire-schema.md`, and
`event-firehose-v1.md`; a change to an ExecutionMap envelope, dependency
entry, or R8/R8b mapping lands those coupled files in one reviewed revision.
G4 changes the shared error type without changing an encoded ExecutionMap
envelope, dependency entry, or firehose mapping. Its exact candidate set is
therefore `rest-state-api-v1.md` and `rest-state-api-v1-wire-schema.md`.
G1 changes the transcript-message projection and `message.created` mapping.
Its exact candidate set is this file, `rest-state-api-v1-wire-schema.md`, and
`event-firehose-v1.md`; all three land in one reviewed revision.
The Concern-tag semantic amendment changes no R7c wire shape, dependency entry,
R8/R8b mapping, route, or pagination rule. Its REST custody change is this file
only. `standalone-toplines-v5.md` is co-amended as a separate canonical
contract at the same targetless candidate.
`rest-state-api-r3-adjudication.md`, `rest-vs-cli-adjudication.md`, and
`topline-map-v1.md` remain authority inputs, not custody companions for this
contract. A worktree, artifact row, transcript, adjudication ledger, or review
report is evidence, not canonical custody. Canonical r3 passed joint
independent review at `att_45676d30` and landed in merge
`c84b1b8dc856861baeaa7b5ff781317ded568cb1`. The r4 ExecutionMap companion set
landed at `0139d9a71180a7175965473fade9b183d2b57601`; the Toplines/session lookup
landed at `05d08b8af74a877d4dabe3dcba8250787d5d430e`; and the AU2 parity correction
landed at `8133efdab14c5470937360a2e4be7fe595639a9d`.
G4 remains a candidate until
one exact revision of its two-file candidate set passes independent review
and lands in `tightbeam-specs`.

## Goal

Define a complete, authorized, deterministic REST read plane from which ATC,
Clawline, and future clients can rebuild every admitted shared-state model and
correlate later firehose notices without reading SQLite or replaying history.

For G4, a client can classify each application error from the HTTP status,
the closed error code, and the exact response bytes without private router or
serializer knowledge.

For G1, REST, CLI wrappers, and `message.created` expose one stored
message-kind discriminator through one shared transcript-message serializer.

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
- The G7 detail routes do not add filters, alternate identifiers, route-local
  queries, route-local serializers, or a second error envelope. They do not
  redefine firehose A6 against a collection page.
- G1 does not add a second transcript-message projection; change `role`,
  `sender`, or `content`; infer a message kind from content; or add a
  `messageType` alias.
- G4 does not define proxy, network, process-crash, undeclared-route,
  unsupported-method, compatibility-alias, `/version`, or successful binary
  download behavior. It does not prescribe a client's retry or presentation
  policy.
- G2 does not change session field meanings or add a session write
  route. It only makes changes to the existing R7 session item observable and
  recoverable.
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

AS5. The router identifies a declared R2, R3, or R3a route and its canonical
resource label before it authenticates that route's request. A route-contract
test falsifies this if one application error cannot carry the same resource
label as the route's success envelope.

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

I8. One closed error type and one encoder serve every canonical R2, R3, and
R3a read route. A route supplies only its canonical resource label, one allowed
error code, and the fields that the selected variant requires.

I9. `messageType` is the sole public message-kind discriminator on a
transcript-message item. `role` retains authorship direction and `sender`
retains provenance. No adapter emits `message_type`, `messageKind`, `kind`, or
another message-kind alias.

I10. One session projection mutation seam owns each mutable input to the R7
session item. The seam detects a change from the complete canonical item with
`rowVersion` excluded, advances its version in the same transaction, and
selects one session class. A verb declaration, elapsed time, or later read is
not the detector.

I11. `mechanicalStatus` preserves the existing
`Tightbeam.Gateway.session_status/2` `run.state` meaning. It is the string
`idle` exactly when this session has zero committed turn rows whose `status` is
`queued` or `running`; it is `running` exactly when that count is positive.
These are its only values and the qualifying-turn count is its only mutable
input. The field is not the full legacy session-status payload.

I12. Every turn transaction that can change membership in the
`queued`/`running` set invokes the session projection mutation seam before
commit. A zero-to-positive count transition stores `running`; a
positive-to-zero transition stores `idle`. A positive-to-positive transition,
including `queued` to `running`, changes no session bytes. The transaction
stores any changed `mechanicalStatus` and the next session `rowVersion`
atomically; its post-commit session notice uses that version.

## Architecture

The read plane has four seams. A principal resolver produces one authenticated
principal. A resource query applies the AU4 visibility function and fixed
filters. The R7 serializer emits the closed wire item defined by the wire
schema. An outer adapter places that item in a REST envelope, compatibility
envelope, CLI result, or firehose notice. Composed views declare their source
classes in R9 and use a dependency digest instead of a notice class.
`Tightbeam.RestEnvelope` is the sole encoder for R4c error bytes. A route
adapter selects a closed variant; it does not build an error object or add a
field or application header.

The session item is a direct R8 resource, not a composed R9 view. Its
`mechanicalStatus` value is materialized in the versioned R7 item under I11-I12.
The serializer does not count turns or derive the field at read time from
unversioned adapter memory, wakes, or another mutable source. This rule closes
freshness without adding a second session status resource or changing the
existing `idle`/`running` meaning.

Operating-guidance impact: none. Canonical r4 applies the existing REST
resource/query/serializer pattern and creates no cross-repository agent rule.

Subtraction ruling for G7: ADD wins because deleting these admitted R8
resources or classes would remove approved shared state, while accepting
collection-only access would leave A6 without an addressable comparator and
would prevent single-row recovery.

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
memberships, and Concern tags. Each Concern is a tag definition inside exactly
one Topline. Its current many-to-many associations group Work Items that have
active memberships in that Topline. ExecutionMap reports mechanical evidence the
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

T6. **Canonical read route** — one declared `/api` GET route in R2, R3, or
R3a. Compatibility aliases, `/version`, `/download/:assetId`, undeclared
paths, and unsupported methods are outside G4.

T7. **Application header** — a response header selected by the REST handler.
Protocol-managed framing and transport headers, including `Date`, `Server`,
`Connection`, `Transfer-Encoding`, and `Content-Length`, are not application
headers.

T8. **Malformed query encoding** — an incomplete or non-hexadecimal percent
escape, or percent-decoded query bytes that are not valid UTF-8. A decoded but
disallowed key, repeated key, combination, type, or value is query validation,
not malformed encoding.

T9. **Message type** — the nullable discriminator stored at the message write
seam and exposed through the optional `messageType` key on the canonical
transcript-message item. Current writers emit `assistant`, `substrate`,
`marker`, or `agent`. A null source omits the public key. A reader accepts an
unrecognized string; a missing or unrecognized value means `assistant` for
message-type presentation and does not change `role`.

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
| GET /api/sessions/:sessionKey/messages[, /:messageId] | paged transcript projection and message detail |
| GET /api/sessions/:sessionKey/coordination-share?from=&to= | pure bounded aggregate read |
| GET /api/work-items[, /:id, /:id/trace] | paged collection, detail, composed trace |
| GET /api/assignments[, /:id, /:id/attests] | paged collection (with derived status, advisory files, effect), detail, nested attests |
| GET /api/attests[, /:attestId] | bulk paged attests across authorized work and attest detail |
| GET /api/wakes[, /:wakeId, /:wakeId/digest-members] | paged wakes, detail, digest audit read |
| GET /api/turns[, /:seq] | paged turns, detail |
| GET /api/artifacts[, /:artifactId] | paged artifact metadata, detail (+ existing GET /download/:assetId for bytes) |
| GET /api/assets[, /:assetId] | paged binary-asset metadata and detail; bytes remain on existing GET /download/:assetId |
| GET /api/decision-requests[, /:id, /:id/operator-ruling-provenance] | paged collection, decision-request detail, operator-ruling-provenance detail |
| GET /api/read-markers[, /:scopeKey] | caller's markers (write stays a verb, firehose RM2) |
| GET /api/roles[, /:name] | paged role registry and role detail |

The bulk attests/wakes/turns collections are first-class on purpose:
nested-only resources force ATC-class clients into one request per parent.

During M5 migration, the two harness-catalog routes share authorization, the
canonical query, ordering and filtering, and one canonical serializer for
each harness item. Only their outer wire adapters differ. They do not promise
byte-identical complete responses. The canonical route wraps items in the v1
envelope; the compatibility alias preserves its legacy raw array until M8
removes that alias.

R3. Durable human-intent reads are GET `/api/toplines[/:id]`. Mechanical
reads are GET `/api/execution-map` and its R3a nested routes,
`/api/facts[/:factId]`, and `/api/critical-state[/:sessionKey]`. Admin reads are
GET /api/identity[, /:name],
/api/archetypes[, /:name], /api/kungfu[, /:name],
/api/guidance[, /:name], /api/rails[, /:name], /api/config[, /:key],
/api/host-env[, /:host/:harness/:name], /api/harness-processes,
/api/users[, /:userId], and
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

R3c. These are the complete G7 detail routes. Each route addresses one
existing R8 public item by the same canonical key carried in the notice and
R7/R7a projection.

| Detail route | Canonical public key | Exact success `resource` |
|---|---|---|
| `GET /api/attests/:attestId` | R7 attest `id`; equals R8 `refs.attestId` | `attests` |
| `GET /api/roles/:name` | R7 role `name`; equals R8 `refs.role` | `roles` |
| `GET /api/sessions/:sessionKey/messages/:messageId` | R7 message `(sessionKey,id)`; `id` equals R8 `refs.messageId` | `transcript messages` |
| `GET /api/facts/:factId` | canonical positive base-10 R7 fact `id`; equals R8 `refs.factId` and `rowVersion` numerically | `condition facts` |
| `GET /api/critical-state/:sessionKey` | R7 critical-state `sessionKey`; equals R8 `refs.sessionKey` | `critical state` |
| `GET /api/host-env/:host/:harness/:name` | R7a host-environment `(host,harness,name)`; equals the three R8 primary refs | `host environment` |

Each string placeholder uses the existing route identifier decoder and exact
public-key comparison. It does not trim, case-fold, alias, or normalize the
decoded value. `factId` is valid only when its path text matches
`[1-9][0-9]*` and its parsed integer equals the stored R7 `id`; a sign,
leading zero, whitespace, decimal point, exponent, or non-ASCII digit is not a
second spelling of that id. The message route returns a row only when both
path values equal that row's `sessionKey` and `id`. The host-environment route
returns a row only when all three path values equal the same row's composite
key.

Each G7 route accepts only AU2's transport-only `asUser` query parameter. The
route passes the resolved principal and canonical key to the resource's
existing shared query seam. That seam applies the existing AU4 predicate
before it exposes whether the key exists. The route then passes the returned
row to the resource's sole R7/R7a public serializer and R4 detail-envelope
adapter. Collection, detail, CLI, and firehose callers do not gain another
query, visibility predicate, field selection, projection, or serializer.

Each G7 route uses the read plane's single shared error encoder. An absent or
invalid bearer returns `401 auth_failed`. AU2 `asUser` failures retain AU2's
exact status and code. Malformed percent encoding returns
`400 malformed_query`. An unsupported query key returns
`400 invalid_filter`. An unknown key, a forbidden row, a noncanonical
identifier spelling, or a message whose `sessionKey` and `messageId` do not
name the same row returns the same `404 not_found` response under AU3/AU8.
Serializer failure returns `500 projection_invalid` without a partial item.
G7 adds no error code or body variant.

Each G7 success and error response inherits the existing shared read-plane
cache contract: it carries `Cache-Control: no-store`, carries no ETag, and
implements no conditional request behavior. The G7 route adapter adds no
cache mechanism or route-specific cache policy.

`role.removed` does not create a historical detail read. Before deletion, the
roles query and detail route expose the current item through the sole roles
serializer. The delete commit applies that same serializer to the last
pre-delete projection with the newly allocated delete `rowVersion`; the
result is the R8 tombstone payload. After commit,
`GET /api/roles/:name` returns the ordinary `404 not_found`. No route stores or
returns a tombstone as a second role shape.

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

R4c. Every canonical read-route error uses the closed `RestError` envelope in
the wire companion. The encoded outer object has exactly `schemaVersion`,
`resource`, and `error`, in that order. `schemaVersion` is `1`. `resource` is
the route's exact success-envelope resource value, including on `401`; an
error does not mint an error-only resource label.
For example, an assignment detail miss encodes exactly
`{"schemaVersion":1,"resource":"assignments","error":{"code":"not_found"}}`.

Each canonical GET route template has exactly this `resource` value in every
success and R4c error envelope. A query string does not change the value.

| Canonical GET route template | Exact `resource` value |
|---|---|
| `/api/org` | `org` |
| `/api/catalog/harnesses` | `harness catalog` |
| `/api/hosts` | `hosts` |
| `/api/hosts/:host` | `hosts` |
| `/api/sessions` | `sessions` |
| `/api/sessions/:sessionKey` | `sessions` |
| `/api/sessions/:sessionKey/messages` | `transcript messages` |
| `/api/sessions/:sessionKey/messages/:messageId` | `transcript messages` |
| `/api/sessions/:sessionKey/coordination-share` | `coordination share` |
| `/api/work-items` | `work items` |
| `/api/work-items/:id` | `work items` |
| `/api/work-items/:id/trace` | `work-item trace` |
| `/api/assignments` | `assignments` |
| `/api/assignments/:id` | `assignments` |
| `/api/assignments/:id/attests` | `attests` |
| `/api/attests` | `attests` |
| `/api/attests/:attestId` | `attests` |
| `/api/wakes` | `wakes` |
| `/api/wakes/:wakeId` | `wakes` |
| `/api/wakes/:wakeId/digest-members` | `digest members` |
| `/api/turns` | `turns` |
| `/api/turns/:seq` | `turns` |
| `/api/artifacts` | `artifacts` |
| `/api/artifacts/:artifactId` | `artifacts` |
| `/api/assets` | `assets` |
| `/api/assets/:assetId` | `assets` |
| `/api/decision-requests` | `decision requests` |
| `/api/decision-requests/:id` | `decision requests` |
| `/api/decision-requests/:id/operator-ruling-provenance` | `operator ruling provenance` |
| `/api/read-markers` | `read markers` |
| `/api/read-markers/:scopeKey` | `read markers` |
| `/api/roles` | `roles` |
| `/api/roles/:name` | `roles` |
| `/api/toplines` | `toplines` |
| `/api/toplines/:id` | `toplines` |
| `/api/execution-map` | `execution map` |
| `/api/execution-map/tree` | `execution map` |
| `/api/execution-map/subtrees/:workItemId` | `execution map` |
| `/api/execution-map/assignments` | `execution map` |
| `/api/facts` | `condition facts` |
| `/api/facts/:factId` | `condition facts` |
| `/api/critical-state` | `critical state` |
| `/api/critical-state/:sessionKey` | `critical state` |
| `/api/identity` | `identity` |
| `/api/identity/:name` | `identity` |
| `/api/archetypes` | `archetypes` |
| `/api/archetypes/:name` | `archetypes` |
| `/api/kungfu` | `kungfu` |
| `/api/kungfu/:name` | `kungfu` |
| `/api/guidance` | `guidance` |
| `/api/guidance/:name` | `guidance` |
| `/api/rails` | `rails` |
| `/api/rails/:name` | `rails` |
| `/api/config` | `config` |
| `/api/config/:key` | `config` |
| `/api/host-env` | `host environment` |
| `/api/host-env/:host/:harness/:name` | `host environment` |
| `/api/harness-processes` | `harness processes` |
| `/api/users` | `users` |
| `/api/users/:userId` | `users` |
| `/api/devices` | `devices` |
| `/api/devices/:deviceId` | `devices` |

Compatibility aliases, `/version`, and `/download/:assetId` do not enter this
table because R4c does not govern their response envelopes.

The closed status and code mapping is:

| HTTP status | Error code | Condition |
|---|---|---|
| 400 | `malformed_query` | T8 query decoding fails |
| 400 | `invalid_as_user` | `asUser` is repeated, or a device bearer supplies it, as AU2 defines |
| 400 | `invalid_message` | an org bearer omits `asUser` or supplies an empty value, as AU2 defines |
| 400 | `invalid_filter` | a decoded query key, multiplicity, combination, type, or value violates R5/R6 |
| 400 | `invalid_cursor` | AU7 rejects cursor encoding, signature, resource, direction, schema, tuple, or normalized filter fingerprint |
| 400 | `ambiguous_id` | an R6a typed prefix resolves to more than one visible full id |
| 401 | `auth_failed` | AU1 credential verification rejects an absent, empty, invalid, or expired bearer |
| 403 | `identity_not_yours` | a session bearer supplies a present empty or nonmatching AU2 `asUser` value |
| 404 | `not_found` | AU3, AU4, AU4a, the canonical nested-route part of AU5, or AU7 requires the same unknown-or-forbidden result |
| 500 | `projection_invalid` | after input validation, the service cannot complete the visibility-filtered query, derive one complete result, or encode it against the closed schema |

No canonical read route emits another application error status or code. A
route emits a listed code only when its named condition applies. In
particular, `ambiguous_id` remains limited to R6a typed-prefix selectors.
ExecutionMap remains the exact specialization in R4a/R4b. Its encoded error
bytes, candidate-id rule, message-bearing refusal, and A27 cases do not change.

G4 declines a second generic error family, per-route error messages or detail
objects, a transient/retryable code, and a new error-only resource label.
After input validation, an in-handler failure uses `projection_invalid`.
A failure that prevents the handler from returning an application response is
outside R4c, and client retry policy remains a non-goal.

Each R4c error sets exactly these application headers:
`Content-Type: application/json; charset=utf-8` and
`Cache-Control: no-store`. It sets no `ETag`, `Vary`, `Location`,
`Retry-After`, `WWW-Authenticate`, or `Set-Cookie` application header. The
handler returns no redirect. The encoder emits no insignificant whitespace.
For one route and principal,
unknown and forbidden selectors use the same status, exact body bytes,
application header bytes, database statement shape, and AU8 timing class.

R4d. Error selection follows this exact precedence. The handler completes one
step before it starts the next:

1. Authenticate the bearer. Failure returns `401 auth_failed` without query
   decoding or a resource query.
2. Decode the raw query. T8 failure returns `400 malformed_query` without
   principal resolution or a resource query.
3. Validate and resolve AU2 `asUser`. Return its applicable
   `invalid_as_user`, `invalid_message`, or `identity_not_yours` result before
   resource-specific query validation.
4. Validate decoded query structure and non-cursor values. This includes
   allowed keys, key multiplicity, key combinations, filters, `limit`, and the
   mutual exclusion of `before` and `after`. Failure returns
   `400 invalid_filter` without cursor-token validation or a resource query.
5. Validate each supplied cursor token against the fields named in AU7.
   Failure returns
   `400 invalid_cursor` without a resource query.
6. Apply the cursor principal binding, AU4 authorization, selector
   visibility, and existence rules. A required denial or miss returns
   `404 not_found`. An allowed R6a prefix with multiple visible matches returns
   `400 ambiguous_id`. Authorization, visibility, and existence selection use
   one visibility-filtered query snapshot. No unfiltered existence result can
   affect error selection. Failure to complete that operation returns
   `500 projection_invalid` and no partial response.
7. Produce and encode one complete canonical result. Failure returns
   `500 projection_invalid` and no partial success body.

This precedence does not change positive results already settled elsewhere.
A sessions `displayName` query with no visible exact match remains a successful
empty page. An unknown config detail key remains SR5's successful item with
`value:null`. Collection authorization still omits denied rows before a
successful response. R4a/R4b continue to govern ExecutionMap. Compatibility
aliases, `/version`, and `/download/:assetId` responses retain
their existing wire contracts.

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
| toplines | `(createdAt, id)` |

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

R5d. Conversation history has one authority: the REST transcript-messages
collection. For a target session with current history boundary
`clearedThroughSeq = F`, the visible set is the R7 transcript-message rows
whose `seq > F`, ordered by R5a `(seq,id)`. Tail, `before`, `after`,
`hasMoreBefore`, and `hasMoreAfter` operate only on that visible set. Cleared
rows do not make either page flag true. The service reads `F`, selects the
items, and computes the flags as one indivisible read; a returned page reflects
one value of `F`. For one `sessionKey`, the observable value of `F` is
non-decreasing. A production mutation cannot expose a row that an earlier
value of `F` hid.

Session creation is the sole initializer and writes
`clearedThroughSeq = 0`. After creation, the sole production write seam is the
canonical session-store operation
`advanceClearedThroughSeq(sessionKey,candidateSeq)`. It atomically writes and
returns `max(storedValue,candidateSeq)` in the session transaction. When that
maximum changes the row, the same commit publishes the resulting session
`rowVersion`; a no-change candidate returns the unchanged row and version. The
closed v1 caller inventory contains exactly two causes and source sites:

- the harness-change path submits the current maximum message `seq` at
  `gateway.ex:2700-2712`; and
- turn-failure recovery submits the old session's failed-prompt `seq` at
  `gateway.ex:3742-3758`.

Both sites must call the sole operation. No other production statement or
caller may write the column. A new cause requires an independently reviewed
amendment to this inventory before implementation and must call the same
operation.

The signed message cursor contains the immutable `(seq,id)` tuple and R5/AU7
request binding. It does not contain `clearedThroughSeq`; that value is
server-owned state, not a request filter. The service compares the decoded
tuple directly and does not resolve it through a live row. Deleting the
boundary row or advancing the history boundary therefore does not invalidate
an otherwise valid cursor.

When a valid cursor tuple is at or below the current history boundary,
`before` returns an empty page with `hasMoreBefore:false` and
`hasMoreAfter:true` exactly when the visible set is nonempty. `after` returns
the first visible page above the boundary. An empty caught-up `after` page has
`hasMoreAfter:false`; the caller retains its last non-null `newestCursor` for
healthy catch-up. Reconnect, a firehose sequence skip, or a history-boundary
change invokes a fresh displayed-slice rebuild from a cursorless tail instead
of treating `after` as gap recovery.

For a nonempty page, `hasMoreBefore` is true exactly when a visible row exists
below the page's first item, and `hasMoreAfter` is true exactly when a visible
row exists above its last item. A cursorless tail has `hasMoreAfter:false`. An
empty cursorless tail has both flags false. An empty caught-up `after` page has
`hasMoreBefore:true` exactly when the visible set is nonempty and
`hasMoreAfter:false`. The service emits `oldestCursor` bound to `before` and
`newestCursor` bound to `after`; using either cursor in the other direction
returns `400 invalid_cursor`.

R6. Filters are whitelisted per resource:

| Resource | V1 whitelist filters |
|---|---|
| sessions | state, ownerUserId for admin, spawnedBy, archetype, harness, provider, model, host, role, displayName exact |
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
| toplines | state exact |

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

R6b. `/api/toplines` lists the durable Topline resource in the R7 row, not
the ExecutionMap work-telemetry view. Its only caller-selected filter is
repeated `state` with the exact enum `open|closed`; omitting it selects both
states. AU4 visibility first restricts the collection to the caller's own
Toplines or to all Toplines for an admin. The filter then selects from that
visible set. The cursor binds the complete `(createdAt, id)` tuple, resource
name, canonical `state` filter fingerprint, and the AU7 principal binding. A
deleted boundary row still positions the next page from that tuple.

The cursor fingerprint is canonical JSON with the field `state`. An omitted
`state` encodes that field as JSON `null`. Present repeated `state` inputs
normalize to a deduplicated JSON array in this fixed enum order:
`["open","closed"]`. Query order and identical duplicate values therefore
produce one fingerprint. The four normalized values `null`, `["open"]`,
`["closed"]`, and `["open","closed"]` are distinct. A cursor is reusable
only when the request produces its signed `state` value; another normalized
value returns `400 invalid_cursor` before a row lookup.

`GET /api/sessions?displayName=<value>` accepts one or more nonempty
`displayName` values. A value matches a stored display name only when its
Unicode code points are equal; it does not trim, case-fold, substring-match,
or interpret SQL/LIKE metacharacters. Multiple values use the existing
same-field disjunction. AU4 visibility runs before comparison. The collection
orders R7 session items by `(createdAt, sessionKey)`. Duplicate display names
return each visible exact-match item in that order. No visible exact match
returns an empty collection. An empty value, a non-string decoded value, or an
unknown query key returns `400 invalid_filter`.

The CLI commands `toplines` and `topline` retain their existing ExecutionMap
selection, tree assembly, telemetry rendering, and response summarization.
Their distinct REST migration is governed by the canonical ExecutionMap
contract. During M4, `transcript --name` first calls the exact `displayName`
sessions collection lookup. It returns zero, one, or many visible R7 session
candidates without transcript content. The caller then chooses a `sessionKey`
and calls `GET /api/sessions/:sessionKey/messages`. The wrapper does not issue
an unfiltered session read, a substring lookup, SQL, or another session-name
endpoint. The wrapper passes REST's opaque `before` and `after` cursors through
unchanged and returns the R4 page object unchanged. It does not accept or emit
a message id as a cursor, translate the superseded transcript projection, or
fall back to a legacy dispatch read after M4 parity passes.

R6c. The shared seams for these two resources are named and exclusive:

| Resource | Visible-query seam | Public-item serializer |
|---|---|---|
| toplines | `Tightbeam.Toplines.query_public/2` | `Tightbeam.Toplines.public_item/1` |
| sessions | `Tightbeam.Org.query_public_sessions/2` | `Tightbeam.Org.public_session_item/1` |

Each query seam receives the resolved principal plus normalized, allowlisted
selection input; applies the matching AU4 function before filter comparison;
orders by R5a; and returns no serialized JSON. Each serializer emits the
existing R7 item for its resource. REST collection/detail adapters and the
migrated `transcript --name` wrapper call these seams. These callers do not
embed SQL, reimplement visibility, add a candidate-only projection, or add an
R7 field. The sessions query seam returns the complete visible ordered
displayName collision set and does not select an arbitrary match or return a
collision error.

R7. Projection fields are closed-world and normative. Every item contains
exactly the keys in its row below. Nullable keys remain present with `null`;
an adapter does not omit them. Every notice-backed stored-state item carries
`rowVersion`, a monotonically increasing integer derived at the write seam.
A composed item carries `dependencyVersion` as described in R9 instead. No
adapter may add a storage column or a caller-selected field.

For transcript messages, “exactly” applies after the conditional R7m rule.
`messageType` is optional, not a nullable public key, and is the sole R7 key
that an adapter conditionally omits.

| Resource | Canonical item fields |
|---|---|
| org | `id`, `archetypes`, `hosts`, `modelCatalog`, `dependencyVersion` |
| harness catalog | `harness`, `provider`, `models`, `capabilities`, `dependencyVersion` |
| hosts | `host`, `rowVersion` |
| sessions | `sessionKey`, `displayName`, `kind`, `orderIndex`, `isBuiltIn`, `adopted`, `ownerUserId`, `origin`, `spawnedBy`, `handle`, `archetype`, `overrides`, `identityName`, `identityRevision`, `harness`, `provider`, `model`, `thinkingLevel`, `modelContext`, `host`, `clearedThroughSeq`, `state`, `createdAt`, `updatedAt`, `mechanicalStatus`, `rowVersion` |
| transcript messages | `id`, `seq`, `sessionKey`, `role`, `messageType`, `content`, `at`, `sender`, `deviceId`, `clientMessageId`, `replyToMessageId`, `replyToClientMessageId`, `llmVisibleMessageId`, `attachments`, `attentionTier`, `turnSeq`, `assignmentId`, `jobRef`, `harness`, `provider`, `model`, `effort`, `context`, `rowVersion` |
| work items | `id`, `title`, `specRefName`, `specRefSha256`, `isBug`, `ownerUserId`, `state`, `failReason`, `routingWakeId`, `slateWakeId`, `createdByUser`, `createdBySession`, `createdInTurnSeq`, `createdContextKnown`, `createdAt`, `rowVersion` |
| assignments | `id`, `subject`, `holderKey`, `holderRole`, `holderFallback`, `openedByUser`, `openedBySession`, `openedAt`, `state`, `outcome`, `closedAt`, `closedByUser`, `closedBySession`, `closingAttestId`, `revocationReason`, `workItemId`, `reviewsAssignmentId`, `holderHarness`, `holderProvider`, `files`, `effectKind`, `derivedStatus`, `rowVersion` |
| attests | `id`, `assignmentId`, `kind`, `verdictKind`, `note`, `bySession`, `byUser`, `producer`, `producerCommand`, `byHarness`, `byProvider`, `commitRefs`, `ts`, `rowVersion` |
| wakes | `wakeId`, `sessionKey`, `targetRole`, `origin`, `prompt`, `consumer`, `dueAt`, `state`, `createdAt`, `firedAt`, `reresolve`, `reresolveSeed`, `reresolveRung`, `conditionKind`, `conditionScope`, `conditionAfterId`, `firedBy`, `creatorSessionKey`, `rumination`, `workItemId`, `assignmentId`, `canceledAt`, `targetGate`, `class`, `classElection`, `deliveryRule`, `digest`, `summon`, `rowVersion` |
| turns | `seq`, `sessionKey`, `messageId`, `wakeId`, `origin`, `prompt`, `roleRef`, `roleFallback`, `assignmentId`, `jobRef`, `model`, `thinkingLevel`, `modelContext`, `harness`, `replyAttention`, `status`, `owner`, `adapterGen`, `requestRef`, `error`, `createdAt`, `startedAt`, `endedAt`, `publishedAt`, `rowVersion` |
| artifacts | `artifactId`, `kind`, `title`, `description`, `createdBySession`, `workItemId`, `parentSession`, `originPath`, `contentSha256`, `recordedMessageId`, `recordedTurnEvidence`, `state`, `home`, `createdAt`, `updatedAt`, `rowVersion` |
| assets | `assetId`, `ownerUserId`, `mimeType`, `size`, `filename`, `createdAt`, `rowVersion` |
| decision requests | `id`, `kind`, `raiserId`, `raiserSessionKey`, `ownerUserId`, `assignmentId`, `expecterSessionKey`, `expecterUserId`, `lineageRung`, `effortGeneration`, `deadlineWakeId`, `raisedAt`, `deadlineAt`, `statuteName`, `question`, `options`, `context`, `status`, `decision`, `rationale`, `ruledBy`, `ruledAt`, `consumedAt`, `withdrawnBy`, `withdrawnReason`, `withdrawnAt`, `askedOfRole`, `answer`, `answeredBy`, `answeredAt`, `rowVersion` |
| operator ruling provenance | `requestId`, `authorityPrincipal`, `state`, `submittingSessionKey`, `ruledAt`, `rowVersion` |
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

R7n. For `toplines`, `concerns` contains current Concern tag entries. Each entry
denotes a tag definition inside exactly one Topline and lists its currently
tagged Work Item IDs. Each listed Work Item has an active membership in that
Topline. A Concern is not an issue and has no update, open/resolved lifecycle,
or reference episodes. `openConcernCount` retains its field name and integer
type for compatibility. It equals the number of current Concern tag definitions
in the Topline. This semantic amendment changes no R7 field name and no R7c
wire type, nullability, nested key, or array-order rule.

R7m. The transcript-message write seam assigns `messageType` without parsing
message content. Current assignments are exact:

- `assistant`: the session model's own output;
- `agent`: a message delivered from an `agent:<handle>` origin;
- `substrate`: a message delivered from a `process:<name>` or
  `remedy:<statute>` origin, including ordinary Tightbeam notices;
- `marker`: a structural transcript boundary created through the marker write
  seam.

A human-authored message and a historical row without the discriminator store
null. The R7 serializer omits `messageType` for either row and never emits
`messageType:null`. Current writers emit no other string. Readers accept an
unrecognized future string. A missing or unrecognized value means `assistant`
for message-type presentation; it does not change `role`. Readers do not reject
the item or parse `content`. For a non-null source, the R7 serializer copies the
stored string. REST, CLI wrappers, and `message.created` call that one
serializer; an adapter does not construct another transcript-message map.

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

The preceding unknown-enum failure applies to closed enums. `messageType` is
the one open discriminator defined by R7m; an unrecognized string remains
valid.

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
| `operator_ruling.provenance_recorded` | operator ruling provenance | upsert | `decisionRequestId` + `sessionKey` |
| `session.spawned`, `session.updated`, `session.retired` | sessions | upsert | `sessionKey` |
| `role.created`, `role.bound` | roles | upsert | `role` |
| `role.removed` | roles | delete | `role` |
| `user.added`, `user.promoted` | users | upsert | `userId` |
| `device.approved`, `device.denied`, `device.revoked` | devices | upsert | `deviceId` |
| `artifact.recorded` | artifacts | upsert | `artifactId` |
| `read_marker.updated` after set | read markers | upsert | `userId` + `scopeKey` |
| `read_marker.updated` after clear | read markers | delete | `userId` + `scopeKey` |
| `message.created` | transcript messages | upsert | `messageId` + `sessionKey` |
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

The operator-ruling-provenance detail route and
`operator_ruling.provenance_recorded` use the one shared serializer
`Tightbeam.Escalation.public_operator_ruling_provenance_item/1`. The item uses
the terminal decision-request row's positive `rowVersion` and the exact R7
field order. The route returns the shared R4 detail envelope with resource
`operator ruling provenance`. An open request, a non-operator request, an
absent request, and a request denied by AU4 return the same R4c
`404 not_found` envelope for that resource. A successful post-epoch ruling
emits one notice after commit; a refusal, pre-epoch row, migration, or
no-change replay emits none. `refs.decisionRequestId` equals item `requestId`;
`refs.sessionKey` equals item `submittingSessionKey`. Firehose payload and
REST detail item are byte-equivalent under A6.

The session projection mutation seam uses one class per committed item change.
First materialization selects `session.spawned`. An `active` to `retired`
transition selects `session.retired`. Each other change to an R7 item field
other than `rowVersion` selects `session.updated`. The seam stores the changed
item and its next durable `rowVersion` atomically. Post-commit publication
carries that exact version.
A request whose complete serialized item, excluding `rowVersion`, is unchanged
leaves `updatedAt` and `rowVersion` unchanged and emits no session state notice.
`refs.sessionKey`, `payload.sessionKey`, and the REST item `sessionKey` are
equal. Sessions soft-retire and therefore use no delete operation.

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

SR8. The decision-request serializer emits the required `deadlineAt` key in
its R7 position. For `kind=agent`, it emits the stored null value. For
`kind=statute` and `kind=effort`, it emits the stored positive integer. An
agent row with a non-null `deadlineAt`, or a statute or effort row with a null,
non-integer, or non-positive `deadlineAt`, fails with `500 projection_invalid`
and emits no partial item. The serializer does not omit, default, derive,
backfill, or mutate `deadlineAt`.

## Requirements — auth and visibility

AU1. `Authorization: Bearer <existing gateway credential>`. A device
token resolves to its user. Without a nonempty matching `asUser`, a session
CLI token resolves to that session only. The session row's `ownerUserId` is
metadata, not an automatic authority escalation. An owner read exists only
where AU4 explicitly grants it.
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

For a session bearer, the existing resolver verifies a nonempty `asUser`
against `session.ownerUserId`. A matching value resolves the named user
principal, exactly as dispatch does. A mismatch returns
`403 identity_not_yours`. Its R4b error message is exactly
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
the authenticated user principal with `isAdmin=true`; a session principal
does not borrow that bit.

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
| operator ruling provenance | operator-request `ownerUserId` user principal; admin |
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
second query or serializer implementation. Until the `transcript` adapter is
removed, it retains the audit-elision and router non-target safeguards in
`transcript-verb-v1.md` I10 and I11.

C2. New flexible reads are designed REST-first; the CLI gains a wrapper
only when a common agent task wants one line. `doctor` stays local (it
probes the host, it is not a state resource).

C3. `transcript --name` maps to the exact-name sessions collection and returns
full R7 session items. `transcript --session` maps to the transcript-messages
collection and returns full R7 message items. Machine-readable CLI output
preserves the successful R4 envelope, R7 items, and page cursors. On refusal,
it returns the REST error code without choosing a second authorization or
cursor outcome. A human renderer may select fields, add labels, or summarize
counts without creating another data field or cursor meaning.
`transcript-verb-v1.md` owns only this wrapper and presentation mapping.

## Migration (order is normative)

M1. Freeze R7 projections, R8 mappings, R9 dependency lists, and AU4
visibility functions. M2. Add REST routes on
those seams. M3. Point the firehose payload builders at the same
serializers. M4. Point CLI read handlers at the canonical read services.
Move each wrapper from dispatch to its REST GET using the existing bearer plus
AU2's `asUser` principal selection where required. Remove its legacy dispatch
read path after parity acceptance passes. Before removal, the `transcript`
adapter retains the audit-elision and router non-target proofs in
`transcript-verb-v1.md` A9 and A10. This transport move does not change item
shapes, authorization, or the M1 query and serializer seams.
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

For transcript messages, the proof evaluates the R7m condition first and then
requires the resulting key set exactly. It proves `messageType` is the sole
conditional key.
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
same-404 results. The matching-owner session case proves that both transports
resolve the named user principal; the absent session case proves the existing
credential-derived principal remains unchanged. Separate GET cases prove
repeated parameters and device bearer plus `asUser` return `400
invalid_as_user`, and malformed percent encoding returns `400
malformed_query`, all before principal resolution. The test proves that the
parameter adds no credential, binding, authorization, or tailnet-identity
behavior.
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

The transcript-message cases also validate conditional `messageType`
optionality, non-null string type when present, open-reader behavior, and the
canonical key position.
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

A30. Given Toplines with a tied `createdAt` and distinct ids, when an
authorized caller pages `/api/toplines` across the tie, a deleted boundary,
and an empty final page, then the union of returned ids equals the visible
collection once in `(createdAt, id)` order. Each decoded cursor contains that
tuple, the `toplines` resource name, the canonical `state` fingerprint, and
the AU7 principal binding; it contains no `rowid`, offset, or storage locator.

A31. Given an `open` Toplines page, when its cursor is reused with
`state=closed` or a request whose normalized `state` value differs, then the
service returns `400 invalid_cursor` before a row lookup. Given
`state=open&state=closed`, the page returns the visible union once. Given an
unknown state, empty state, or unknown filter name, the service returns
`400 invalid_filter`.

Given a Toplines cursor created with `state=closed&state=open&state=open`,
when a caller reuses it with `state=open&state=closed`, then the service
accepts it because both requests normalize to `["open","closed"]`. Given a
cursor created with `state=open&state=open`, when a caller reuses it with
`state=open`, then the service accepts it because both requests normalize to
`["open"]`. Given a cursor created with absent `state`, when a caller reuses
it with `state=open&state=closed`, then the service returns
`400 invalid_cursor` before a row lookup. Given a cursor created with
`state=open`, when a caller reuses it with absent `state`, then the service
returns `400 invalid_cursor` before a row lookup.

A32. Given two readable sessions with the same display name, a readable
session whose name differs only by case, and an unreadable colliding session,
when a caller uses `GET /api/sessions?displayName=<exact>`, then the response
contains the two readable exact R7 items in R5a order and no other fixture.
Given no exact match, it returns an empty page. Given `%`, `_`, a quote, or
SQL-looking text, it makes one literal comparison and changes no query shape.
Given an empty `displayName`, a decoded non-string `displayName`, an unknown
query key, or any request that combines one of those values with a valid
`displayName`, when the sessions collection runs, then it returns
`400 invalid_filter` before any query runs. It never returns an unfiltered or
partial collection, candidate, or message content.
The transcript-name wrapper returns these candidates without message content
and retrieves content only after an explicit `sessionKey`.

A33. Given a non-owner and a colliding foreign session, when the sessions
exact-name collection runs, then its bytes equal the same collection with that
foreign session absent. Given a direct transcript GET for that foreign key,
then its bytes equal an unknown-key response. Admin, target-session, and
target-session-owner cases pass their AU4-authorized collection and detail
checks.

A34. Given the R6c resource seams, when REST collection or detail routes and
the migrated `transcript --name` wrapper run, then each invokes its named
query seam and serializer and emits the unchanged R7 object. The test rejects
inline SQL, a second visibility predicate, a second item serializer, a
caller-selected field/sort/join parameter, and a candidate-only session
projection.

A35. Given one R4c error request for every canonical GET route template in the
R4c route-to-resource table, when the client receives each error, then its
exact `resource` value equals that route's table row. The table-driven test
enumerates every row exactly once and rejects an absent, duplicate, inferred,
or query-dependent route mapping. Given canonical assignment collection and
detail routes and one fixture that triggers each R4c condition without a
second failure, when the client receives each error, then the status, exact
body bytes, application headers, and resource label equal R4c and the wire
companion. The test covers each closed code once. It uses an ExecutionMap
ambiguous-prefix request for `ambiguous_id` and a mismatched session bearer for
the sole message-bearing `identity_not_yours` variant. It rejects an extra
code, key, whitespace byte, application header, partial item, or changed key
order.

A36. Given requests that each contain two independently failing inputs, when
the handler evaluates them, then this table proves R4d precedence and proves
that no later step runs:

| Earlier failure | Later failure | Exact result |
|---|---|---|
| invalid bearer | malformed percent escape | `401 auth_failed` |
| malformed percent escape | repeated `asUser` | `400 malformed_query` |
| repeated `asUser` | unknown filter key | `400 invalid_as_user` |
| unknown filter key | invalid cursor signature | `400 invalid_filter` |
| invalid cursor signature | unknown or forbidden selector | `400 invalid_cursor` |
| valid cursor with wrong principal binding | otherwise visible selector | `404 not_found` |

A37. Given an unknown detail id and a forbidden detail id on the same route,
when the same principal requests each, then status, exact body bytes,
application header bytes, statement shape, and AU8 timing checks match. Given
an unmatched sessions `displayName`, an unknown config detail key, a
collection containing only denied rows, an ExecutionMap R4b error, a
compatibility-alias request, and an asset-download request, each retains A32,
SR5, AU3, A27, M5, and AU5 behavior respectively. The G4 error encoder is not
invoked for a compatibility alias or an asset-download response. The
ExecutionMap case reruns A27 and requires byte-identical encoded errors.

A38. Given visible messages whose stored `messageType` values are
`assistant`, `substrate`, `marker`, and `agent`, plus one human-authored
message and one historical row with no stored discriminator, when a caller
fetches `GET /api/sessions/:sessionKey/messages`, then the four classified
items expose their stored values in the R7 position. The human-authored and
historical items omit the key; no item emits `messageType:null`.

A39. Given those messages and their matching `message.created` notices, when
the contract suite removes each notice envelope, then each payload is
byte-equivalent to its fetched item. For each pair,
`refs.messageId == payload.id` and
`refs.sessionKey == payload.sessionKey`. The suite fails if REST or firehose
uses a route-local message map or a second serializer.

A40. Given two rows with identical `role`, `sender`, and `content` but distinct
stored discriminators, when the shared serializer runs, then it preserves each
stored `messageType`. Given a decoder fixture with an unrecognized nonempty
`messageType`, the client accepts the item and treats its message type as
`assistant`. Given a fixture that omits `messageType`, the client does the
same. Neither fallback changes `role`, and neither surface parses `content`.

A41. Given one visible stored row for each R3c route, when the allowed
principal fetches its collection item, its detail item, and a matching R8
upsert notice, then the detail response is `200`, its `resource` equals the
R3c table value, and its `item` bytes equal both the collection item and
notice payload.
The test constructs each path only from the R7/R7a key and matching R8 refs.
For a message, it uses both the payload `sessionKey` and `refs.messageId`. For
host environment, it uses the payload `host`, `harness`, and `name`.

Given a visible role and its next `role.removed` commit, when the test captures
the detail item before deletion and inspects the tombstone afterward, then the
tombstone contains the captured public fields from the sole roles serializer
and the newly allocated delete `rowVersion`. That version exceeds the
captured upsert version. A post-commit detail request returns the shared
`404 not_found`; no historical row, tombstone route, or second role serializer
exists.

A42. Given each R3c row, when the test repeats the detail request as each
principal that its AU4 row allows, then each case returns the same R7/R7a
bytes. For each R3c resource whose AU4 row excludes at least one authenticated
user or session principal, the test repeats the request as one such denied
principal; that response equals an unknown-key response in status, body,
application headers, statement count, and AU8 timing class. The roles resource
has no denied authenticated-principal case because AU4 grants it to each
authenticated user and session; A43 covers its absent and invalid bearer
cases. For a message, a visible session with a message id from another session
produces the same result. For an attest, the test denies the parent assignment.
For facts and critical state, the test covers their exact AU4 principal sets.

A43. Given each R3c route, when the test sends no bearer, each AU2 `asUser`
failure, malformed percent encoding, an unsupported query key, a
noncanonical fact id, an unknown key, and a forced serializer failure, then
the route returns respectively `401 auth_failed`, AU2's exact result,
`400 malformed_query`, `400 invalid_filter`, `404 not_found`,
`404 not_found`, and `500 projection_invalid`. Each response uses the shared
general error encoder and contains no partial item. A seam-identity test fails
if route code adds SQL, a visibility predicate, an item map, a serializer, or
an error encoder instead of calling the existing shared seams.

Given each A41 success and each A43 error, when the shared response adapter
encodes it, then the response carries `Cache-Control: no-store` and no ETag.
Given the same visible-detail request with `If-None-Match` and
`If-Modified-Since`, when the route runs, then it ignores those conditional
headers and returns the same `200` item instead of `304`.

A44. Given first materialization, a non-retirement item change, and an
`active` to `retired` transition for one session, when each transaction
commits, then the mapping selects exactly `session.spawned`, `session.updated`,
and `session.retired`, respectively. Each notice uses resource `sessions`, op
`upsert`, primary ref `sessionKey`, and the R7 session serializer.

A45. Given a change to a session item field other than `rowVersion`, when REST
detail and its notice payload are encoded, then their item bytes are equal and
their `sessionKey` values equal `refs.sessionKey`. The transaction stores a
greater `rowVersion` before the post-commit notice becomes eligible for
publication.

A45a. Given a request whose session item fields other than `rowVersion` do not
change, then `updatedAt` and `rowVersion` remain unchanged and no session state
notice exists.

A46. Given a client that receives `subscription_ready` for `session.`, when it
pages `GET /api/sessions` while the target session changes, then applying the
buffered notice and snapshot items by `(sessionKey,rowVersion)` yields the same
collection as a fresh quiescent read. Reversing the arrival order yields the
same bytes.

A47. Given a session change during a disconnected interval, when the client
reconnects, then it resubscribes before paging the visible sessions collection
and converges from that snapshot plus live notices.

A48. Given one suppressed session notice, when the next sequence or heartbeat
exposes the gap, then the client runs the same resubscribe-and-snapshot path and
converges to a fresh quiescent sessions read.

A49. A table drives every mutable input to the R7 session item through the
session projection mutation seam and verifies A44-A45. For I11, it begins with
zero qualifying turns and `mechanicalStatus:"idle"`, then tests these committed
qualifying-count transitions: zero to one, one to zero, one to two, and two to
one. The first two cases produce `running` and `idle`, respectively, advance
the session `rowVersion`, and emit one `session.updated`; the latter two leave
the session item and its version unchanged and emit no session state notice.

A49a. Given one qualifying turn, changing its status from `queued` to `running`
leaves `mechanicalStatus:"running"` unchanged. Given a turn whose old and new
statuses are both outside `queued` and `running`, changing that status leaves
`mechanicalStatus` unchanged. Each case emits no session state notice from this
input. The table fails on a direct session writer, a turn writer that bypasses
I12, another input to `mechanicalStatus`, a value outside `idle` and `running`,
or any read-time derivation of the field.

A50. Given 1,205 visible transcript messages with tied and regressed
timestamps, when a caller reads the cursorless tail and repeatedly passes each
`oldestCursor` as `before`, then each visible `(seq,id)` appears once, each page
is oldest-to-newest, and the chain stops with `hasMoreBefore:false`. Decoding
each cursor yields the complete `(seq,id)` tuple and no message-id alias or live
row locator.

A51. Given a cursor returned before its boundary row is deleted, when the next
page runs, then its items and page object equal the result produced while that
row existed while the other rows remain unchanged.

A51a. Given a cursor whose tuple is at or below a newly advanced
`clearedThroughSeq`, when `before` runs, then it returns an empty item list,
`hasMoreBefore:false`, and `hasMoreAfter:true` exactly when visible rows exist.
When `after` runs with that cursor, it returns only visible rows above the new
boundary.

A51b. Given nonempty visible history and a caught-up `after` cursor, when the
caller requests the next page, then the page is empty and sets
`hasMoreBefore:true` and `hasMoreAfter:false`. Given an `oldestCursor` used as
`after` or a `newestCursor` used as `before`, the service returns
`400 invalid_cursor`.

A51c. A source-structure test finds one session-creation seam that initializes
`clearedThroughSeq` at zero, exactly one post-creation production write
statement owned by `advanceClearedThroughSeq`, and exactly the two inventoried
caller sites: the harness-change maximum-message-seq path at
`gateway.ex:2700-2712` and the turn-failure old-session failed-prompt-seq path at
`gateway.ex:3742-3758`. Given concurrent candidates above, equal to, and below
the stored value through both callers, then every committed and subsequently
read value equals the maximum value seen for that session. A changed value and
its new session `rowVersion` become visible in the same commit; an unchanged
value retains its row version. The transcript route exposes no previously
cleared row. The test fails for a direct write, a second writer, an unlisted
caller, a decreasing result, or separate boundary and row-version publication.

A52. Given concurrent message inserts and a boundary advance, when the REST
tail and backward pages run, then each returned page corresponds wholly to the
boundary before or after the commit and never mixes both. The versioned
snapshot-to-buffer handoff and reconnect proof are
`transcript-verb-v1.md` A5 and A6; this REST test does not define a second
client recovery algorithm.

A53. Given the same principal and selection, when direct REST and the M4
`transcript` wrapper run successfully, then their R4 envelopes, R7 items, and
page cursors are equal. Given a REST refusal, the wrapper returns the same
error code without choosing a second authorization or cursor outcome. Passing
a prior message id as `before` returns `400 invalid_cursor`; the wrapper does
not decode, translate, retry, or invoke the legacy dispatch read.

A54. Given stored decision-request rows with `(kind,deadlineAt)` equal to
`(agent,null)`, `(statute,1)`, and `(effort,2)`, when the shared serializer
encodes each row, then each item contains `deadlineAt` in the R7 position; the
agent item contains null, and the statute and effort items contain their exact
stored positive integers. Given `(agent,1)`, `(statute,null)`, `(effort,null)`,
or a statute or effort value that is non-integer or less than one, when the
shared serializer encodes the row, then it returns `500 projection_invalid`
and emits no partial item.

## Open questions — Spirit questions for Mike

G4 has no open questions. R4c closes its error variants, status map, headers,
precedence, and preserved special cases. The broader ruled and non-blocking
questions below are unchanged.

G1 has no open questions. T9, R7m, A38, A39, and A40 close its discriminator,
compatibility, correlation, and shared-serializer behavior.

G7 has no open question. The G4 general error envelope is a delivery
dependency, not an unruled behavior; no G7 route ships before that envelope is
canonical.

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
lint and fresh independent exact-byte review are canonical r4's pre-build
gate. Acceptance clauses remain executable and decidable. Product tests and a
`tests-passed` receipt belong to the later implementation card; this spec-only
assignment does not implement or claim them. Authority:
`att_d5b0a440-bd51-498f-8b96-e6512fedf68f`.

Deleting `fanOut` or Toplines would remove current product meaning. Accepting
snapshot-only or no-notice freshness would break I5 and the live display-model
outcome. Those subtraction alternatives therefore lose to the four bounded
source invalidation mappings above.
