# REST core detail routes v1 — canonical R4c envelopes

Status: CANDIDATE for one independent exact-revision review. Product-code work
starts only after this file receives `reviewed-clean`, the work item binds that
reviewed content hash, and the reviewed D1 implementation is present on green
product `origin/main`.

Authority: `rest-state-api-v1.md` SP2, SP4, R2, R4, R4c, R4d, R7, R8,
SR1-SR4, AU1-AU5, AU7-AU8, and A2/A35-A37; its normative wire companion;
`event-firehose-v1.md` V3-V5 and A6; the D1 transport contract in
`rest-read-plane-d1.md`; Mike ruling
`dr_2902b630-0e69-4d58-a16e-bbf3f1f0e017`; spirit verdict
`att_725b1665-6b35-419e-9f0b-d9af9c62130d`; and route authority report
`art_cc58df9e` at SHA-256
`fdd867d9d51031888eb0ca56bb184f39d1706d3e0b1fa7fada4385540b98e8f5`,
with its source-readable extract in message
`s_611313bb-ad2d-4434-b075-267b6f67f2e7` and its R7 correlation correction
in message `s_6f2e66ab-bfed-409a-92e5-a72701548c20`; message
`s_88e9615c-a45e-4726-98dc-29356d4a2ca2` fixes the shared ordered-item
encoding requirement.
This specification serves
`wi_62996c64-1871-409b-be96-ecce9555bd7e`.

## Spec homing

The canonical file is `rest-core-detail-routes-v1.md` in the
`clickety-clacks/tightbeam-specs` repository. A worktree, transcript, artifact
row, review report, or product branch is evidence, not canonical custody. The
work item binds the file path and SHA-256 only after one independent reviewer
accepts the exact bytes.

Operating pattern taught to agents: none. This file applies the existing REST
query, visibility, serializer, envelope, and review patterns. It does not amend
agent guidance.

## Goal

Deliver one canonical R4/R4c detail response for each of these nine admitted
R8 resources: work items, assignments, wakes, turns, decision requests,
sessions, devices, artifacts, and read markers. A client can fetch the exact
public item named by a notice primary key and compare that item byte-for-byte
with the notice payload after it removes only the outer envelopes.

Replace the existing legacy composite response at
`GET /api/work-items/:workItemId` with the canonical work-item detail envelope.
Add the other eight detail routes without changing their collection routes.

## Non-Goals

- This work does not add a resource, collection, filter, public field,
  projection, serializer, visibility grant, credential, cursor, compatibility
  alias, or firehose class.
- This work does not edit the firehose registry or its class, operation,
  resource, primary-reference, version, or emission mappings.
- This work does not implement or modify the six G7 detail routes for attests,
  roles, transcript messages, condition facts, critical state, and host
  environment.
- This work does not implement or modify the D1 routes for config, host
  environment collection, hosts, users, identity, or kungfu.
- This work does not change a collection response, nested route, composed
  route, legacy `/api/work` route, dispatch verb, CLI wrapper, notice envelope,
  target, deployment, or release. The exact turn and device serializer/ref
  corrections below change conformance to the existing R7 fields; they do not
  amend a projection or add a serializer.
- This work does not retain the legacy composite work-item response at
  `/api/work-items/:workItemId` under another query flag or response variant.
- This file does not authorize product edits before its exact bytes pass
  independent review and the D1 code-start dependency is satisfied.

## Terms

- **Core detail route**: one of the nine GET route templates in Table 1.
- **Canonical route key**: the exact decoded public key in Table 1. A typed
  string id must match the stored public id exactly. `turnSeq` has one valid
  path spelling: a positive base-10 integer matching `[1-9][0-9]*`.
- **Effective marker key**: `(resolved user principal id, decoded scopeKey)`.
  The user id is implicit in the resolved principal and does not become a path
  segment or query parameter. A session principal without AU2 user resolution
  has no effective marker key.
- **Shared lookup**: the one `Tightbeam.StateResources` row lookup named in
  Table 1. Seven exist at product commit `581afe9b`. This build adds the two
  missing shared seams for turn sequence and decision-request id. A shared
  seam may delegate to the owning module or transaction query. It copies no
  SQL, visibility rule, or item map into a route.
- **Public item bytes**: the compact UTF-8 JSON bytes emitted by the resource's
  sole `Tightbeam.StateResources` serializer through the D1/M1 shared R7/R7a
  ordered-item encoder, with all top-level and nested order, conditional
  omission, and no insignificant whitespace preserved.
- **Envelope removal**: byte slicing that extracts the encoded value of REST
  `item` or notice `payload`. Decoding and re-encoding either value is not an
  A6 byte comparison.
- **Same 404**: the exact `404 not_found` status, body bytes, application-header
  bytes, visibility-filtered database statement shape, statement count, and
  AU8 timing class for an unknown or forbidden key.

## Assumptions

AS1. The reviewed D1 implementation on product `origin/main` supplies the
shared bearer/AU2 resolver, R4/R4c envelope encoder, R4d error precedence,
request decoder, and no-store response adapter. The code-start check fails
before a product edit when this assumption is false.

AS2. Product commit `581afe9b8de4b4595717a81bdd0d38402d9c747c`
contains the seven Table 1 lookups marked existing. It has no public by-sequence
turn lookup and no decision-request detail lookup in `StateResources`. It does
contain `query_turn_in_txn/2` and the Escalation-owned canonical by-id read that
the two new Table 1 seams reuse.

AS3. The R7 and wire-schema field lists remain the authority for item keys,
types, nullability, enum domains, and order. This card corrects the existing
turn and device serializers and their primary-ref extraction exactly as I4
defines. Another serializer or mutation defect remains outside this card.

AS4. The firehose registry correction lane owns `session.updated` and the
`prod.fired` observational classification. This card neither waits on that
lane to implement routes nor edits its files. Full cross-class A6 closure waits
for both reviewed lanes.

## Invariants

I1. A core detail route calls one shared lookup, one existing AU4 visibility
predicate, one public item serializer through the D1/M1 shared ordered-item
encoder, and one D1 outer-envelope encoder. The route contains no row query,
item map, JSON reshaping, field selection, item encoder, projection, or error
encoder.

I2. The service applies bearer authentication, query decoding, AU2 principal
resolution, query validation, visibility-filtered lookup, serialization, and
encoding in R4d order. The visibility check and existence selection use one
query snapshot.

I3. An unknown key, forbidden row, malformed typed string id, noncanonical
`turnSeq`, or unavailable effective marker key selects the same 404. No earlier
step exposes row existence.

I4. The detail `item` is the complete R7 item. Collection, REST detail, CLI
read, and R8 publication use the same serializer bytes. A turn item contains
the R7 integer `seq` and no `turnSeq` alias; `refs.turnSeq` derives from that
source sequence. A device item contains `deviceId` and no public storage `id`;
`refs.deviceId` derives from that public key or its source id. Field order,
JSON types, nulls, identifiers, and timestamps come only from the sole
serializer and its shared ordered-item encoder; an envelope or route does not
restate, reorder, omit, add, or transform them.

I5. Each success and application error carries
`Content-Type: application/json; charset=utf-8` and
`Cache-Control: no-store`. A core detail route emits no ETag, conditional
response, redirect, `Vary`, `Location`, `Retry-After`, `WWW-Authenticate`, or
`Set-Cookie` application header.

I6. The implementation exposes storage data only through the existing public
serializer. Serializer-owned structures contain no `cliToken`, device
`token`, `identityToken`, credential-bearing path, or storage-only field.
Opaque user-authored JSON and content strings remain governed by SR3 and do
not become field-name denylist input.

I7. The route's exact R4c `resource` literal is independent of the URL
placeholder name, query string, auth outcome, lookup outcome, and firehose
registry spelling.

I8. The work-item route has one response contract after this change. It emits
the R4/R4c detail envelope and does not emit the prior `WorkState.item_detail`
composite.

## Architecture

### Code-start dependency

The builder records the exact reviewed D1 product commit and proves that the
commit is present on a freshly fetched green product `origin/main` before the
first product-source edit. The D1 commit must supply the shared transport,
auth/AU2, error-envelope, and cache seams in AS1. A private branch, preserved
worktree, unreviewed tip, or specs-only D1 revision does not satisfy this gate.

The builder branches from that exact green main tip. The builder does not
compose this card with the D1, G7, registry, CLI, firehose Card 5, deployment,
or release lane.

### Table 1 — closed route and seam map

| Route template | Canonical route key | Canonical shared lookup | AU4 row | Sole serializer | R8 primary refs | Exact R4c `resource` |
|---|---|---|---|---|---|---|
| `GET /api/work-items/:workItemId` | exact R7 `id` | `StateResources.query_work_item/3` | work items | `StateResources.work_item/1` | `workItemId` | `work items` |
| `GET /api/assignments/:assignmentId` | exact R7 `id` | `StateResources.query_assignment/3` | assignments | `StateResources.assignment/1` | `assignmentId` | `assignments` |
| `GET /api/wakes/:wakeId` | exact R7 `wakeId` | `StateResources.query_wake/2` | wakes | `StateResources.wake/1` | `wakeId` | `wakes` |
| `GET /api/turns/:turnSeq` | canonical positive base-10 R7 `seq` | new `StateResources.query_turn_by_seq/2`, reusing `query_turn_in_txn/2` | turns | `StateResources.turn/1` | `turnSeq` derived from R7 `seq` | `turns` |
| `GET /api/decision-requests/:decisionRequestId` | exact R7 `id` | new `StateResources.query_decision_request/2`, delegating to the Escalation-owned canonical by-id read | decision requests, by kind | `StateResources.decision_request/1` | `decisionRequestId` | `decision requests` |
| `GET /api/sessions/:sessionKey` | exact R7 `sessionKey` | `StateResources.query_session/2` | sessions | `StateResources.session/1` | `sessionKey` | `sessions` |
| `GET /api/devices/:deviceId` | exact R7 `deviceId` | `StateResources.query_device/2` | devices | `StateResources.device/1` | `deviceId` | `devices` |
| `GET /api/artifacts/:artifactId` | exact R7 `artifactId` | `StateResources.query_artifact/2` | artifacts | `StateResources.artifact/1` | `artifactId` | `artifacts` |
| `GET /api/read-markers/:scopeKey` | effective marker key | `StateResources.query_read_marker/3` | read markers | `StateResources.read_marker/1` | `userId`, `scopeKey` | `read markers` |

The Table 1 rows are the implementation and acceptance inventory. A missing,
extra, duplicated, or inferred row fails the build. An internal parameter name
may differ from the descriptive placeholder above; the URL template and wire
contract do not.

The two rows labeled `new` are implementation requirements. Product commit
`581afe9b` does not contain them. `query_decision_request/2` delegates to the
existing Escalation-owned read without copying `decision_requests` SQL or
bypassing Escalation's row decoding. `query_turn_by_seq/2` runs the existing
exact-sequence transaction lookup through one shared read transaction. A route
cannot substitute `query_turn/3`, whose key is `(sessionKey,messageId)`.

### Two mechanical R7 correlation corrections

`StateResources.turn/1` emits the R7 keys in their declared order. It preserves
the integer field `seq` and removes the extra public `turnSeq` alias.
Firehose primary-ref construction writes `refs.turnSeq` from the authoritative
source sequence or the serialized `payload.seq`; it does not require or add a
payload alias.

`StateResources.device/1` renames the storage field `id` to the public R7 field
`deviceId`. It emits no public `id` alias. Firehose primary-ref construction
writes `refs.deviceId` from the serialized `payload.deviceId` or the
authoritative source id; it does not retain a second public key.

These corrections change no R7 row, field order, type, nullability, registry
row, operation, class, resource, version source, or notice envelope. The
serializer remains the sole serializer for its resource.

### Route processing

Each route accepts only AU2's transport-only `asUser` query key. The D1 adapter
performs these steps in one fixed order:

1. Authenticate the bearer. A refusal returns `401 auth_failed` before query
   decoding or lookup.
2. Decode the raw query. Invalid percent encoding or decoded non-UTF-8 bytes
   return `400 malformed_query` before principal resolution or lookup.
3. Apply AU2 to the sole optional `asUser` value. The adapter preserves AU2's
   `invalid_as_user`, `invalid_message`, and `identity_not_yours` status and
   exact bytes.
4. Reject another decoded query key or invalid multiplicity as
   `400 invalid_filter` before lookup.
5. Decode the path key without trimming, case-folding, aliasing, Unicode
   normalization, typed-prefix expansion, or alternate numeric spelling.
6. Pass the resolved principal and Table 1 key to the shared lookup and AU4
   predicate in one visibility-filtered snapshot. A miss or denial returns the
   same 404.
7. Pass the allowed row to the Table 1 serializer. A lookup, schema,
   serialization, or encoding failure returns `500 projection_invalid` with
   no partial item.
8. Insert the shared ordered-item bytes into the detail envelope without
   decoding, map reshaping, reordering, or re-encoding, and return 200.

When an existing CLI-oriented lookup accepts a unique typed prefix, the REST
adapter requires the returned R7 primary key to equal the complete decoded path
key before it exposes the row. A prefix-resolved mismatch returns the same 404
without a second lookup.

The effective marker key step requires a resolved user principal. It uses that
user id even when the user is an admin. Thus two users can hold the same
`scopeKey` without ambiguity or cross-user selection. An org or matching
session bearer can use AU2 to resolve the marker's user. A session principal
that remains session-scoped gets the ordinary same 404. The route adds no
`userId` selector.

### Success and error bytes

A success body has exactly these outer keys in order and no insignificant
whitespace:

`{"schemaVersion":1,"resource":"<Table 1 literal>","item":<public item bytes>}`

An application error uses the shared R4c `RestError` encoder. For example, an
assignment miss is exactly:

`{"schemaVersion":1,"resource":"assignments","error":{"code":"not_found"}}`

The closed cases exercised by this card are:

| Status | Code | Core-detail condition |
|---|---|---|
| 400 | `malformed_query` | raw query decoding fails |
| 400 | `invalid_as_user` | AU2 repeated `asUser` or device-bearer case |
| 400 | `invalid_message` | AU2 requires a user selection or receives its empty org-bearer value |
| 400 | `invalid_filter` | decoded query structure contains anything except one optional `asUser` |
| 401 | `auth_failed` | bearer verification fails |
| 403 | `identity_not_yours` | session bearer supplies a nonmatching AU2 user |
| 404 | `not_found` | I3 miss or denial |
| 500 | `projection_invalid` | shared query, projection, schema, or encoding cannot complete one item |

`identity_not_yours` retains R4c's sole message-bearing error shape. Another
case adds no message, details, selector, denied id, or partial item.

### A6 byte comparison

The route suite derives one nine-row comparator table from Table 1 and the
reviewed R8 registry. For an upsert class, the fixture commits a real row,
captures the raw change frame, performs the authorized HTTP detail GET, slices
the raw `payload` and `item` value bytes, and requires exact equality. The test
also requires equality between each Table 1 R7 key and its R8 primary refs,
including integer equality between payload `seq` and `refs.turnSeq`, string
equality between payload `deviceId` and `refs.deviceId`, and both string
components for a read marker. Firehose Card 5 consumes the reviewed landed
behavior through its own acceptance harness; this card does not edit that
harness.

The comparison does not decode and re-encode either value. It does not remove,
sort, normalize, omit, or coerce an item field. The REST detail envelope is the
sole routine byte difference.

This card adds no delete behavior. If the reviewed registry maps a mutation as
delete, the comparator uses the registry-owned final public projection and
version contract, then requires the post-commit detail GET to return the
ordinary same 404. A route implementation does not mint history or a second
tombstone serializer.

### Subtraction and touch boundary

ADD wins for the eight absent routes because deleting the admitted R8
resources would remove approved product state, while accepting their absence
would leave A6 and single-row recovery unbuildable. For work items, replacement
wins: the implementation deletes the legacy composite behavior at the existing
canonical path instead of adding a compatibility mode.

ADD wins for the two shared query seams because each absent detail route needs
one non-route-local row lookup; deleting either route loses the approved
resource, and accepting route-local SQL violates the one-query invariant.

The intended product touch set is the router, the two new shared query seams,
the exact turn/device serializer and primary-ref corrections, and focused
core-detail tests. A source diff that changes another serializer, a projection
contract, collection, registry row, visibility grant, mutation, CLI, notice
envelope, or Card 5 comparator file is outside this spec.

## Acceptance

The builder implements one table-driven test inventory with one row per Table
1 route. Each acceptance check below identifies the required row set.

AC1 — **D1 gate.** Given a freshly fetched product main that lacks the exact
reviewed D1 product commit or has a red repository gate, when the code-start
check runs, then it stops before a product-source edit. Given green main with
that commit, the check records the base SHA and permits the route branch.

AC2 — **Route inventory and work-item replacement.** Given the router's
compiled route table, when the inventory test compares it with Table 1, then
each template appears once with its exact resource literal and no tenth route
appears under this feature. Given a visible work item with assignments and
trace data, when the client GETs its detail path, then the body contains only
`schemaVersion`, `resource`, and the R7 work-item `item`; it contains no legacy
composite `assignments`, trace, holder, or cursor field.

AC3 — **Success envelope and shared seams.** Given one visible valid R7 row per
Table 1 route, when each allowed principal performs the real HTTP GET, then the
response is 200 with the exact success key order, exact Table 1 resource
literal, exact public item bytes, and exact application headers. A seam spy
records one Table 1 lookup, the resource's existing AU4 predicate, one Table 1
serializer, one D1/M1 shared ordered-item encoder, and one shared envelope
encoder. It records no route-local SQL, item map, JSON reshaping, visibility
predicate, projection, item encoder, serializer, or error encoder.

Given the two new query seams, when the spy calls `query_turn_by_seq/2` and
`query_decision_request/2`, then the first uses the existing exact-sequence
transaction lookup and the second uses the Escalation-owned canonical by-id
read. The source scan finds no duplicated turn or decision-request SQL in the
router or another `StateResources` function.

AC4 — **Canonical keys and types.** Given each row and its matching R8 notice,
when the table constructs the path only from the primary refs, then the detail
item's public key equals those refs with the exact JSON type. For turns,
`payload.seq` is an integer equal to `refs.turnSeq` and the payload contains no
`turnSeq`. For devices, `payload.deviceId` equals `refs.deviceId` and the
payload contains no public `id`. Given a truncated
typed id, changed case, leading or trailing whitespace, alternate Unicode
normalization, or mismatched key, the applicable string-key route returns the
same 404. Given `turnSeq` spellings `0`, `01`, `+1`, `-1`, `1.0`, `1e0`, a
space-bearing value, a non-ASCII digit, an overflow value, or non-digits, the
turn route returns the same 404 without a second numeric interpretation.

AC5 — **Read-marker composite identity.** Given two users with the same
`scopeKey` and distinct marker bytes, when each resolved user fetches that
path, then each receives only the item whose `(userId,scopeKey)` equals its
effective marker key. Given a session principal without AU2 user resolution,
then it receives the same 404 as an unknown key. No test request supplies a
`userId` path or query selector.

AC6 — **AU2 and error precedence.** Given each Table 1 route, when the test
sends an absent bearer, invalid bearer, missing org-bearer `asUser`, empty
org-bearer `asUser`, repeated `asUser`, mismatched session-bearer `asUser`,
device bearer plus `asUser`, malformed percent escape, and one unsupported
decoded query key, then the route returns the exact R4c status, body bytes, and
application headers in the route-processing order. A spy proves no later
principal or row operation runs after the selected failure.

AC7 — **AU4 and same 404.** Given each Table 1 AU4 row, when the test uses each
allowed principal class, then the route returns the same R7 bytes. Given one
authenticated principal excluded by that AU4 row, when it requests a known
key and then an unknown key, then status, body bytes, application headers,
statement shape, and statement count match. The existing AU8 harness runs at
least 10,000 randomized requests per case and requires the canonical p50 and
p95 bound. The decision-request cases cover statute, effort, and agent kinds.

AC8 — **Closed error and projection failure.** Given each Table 1 route and a
forced shared-lookup, schema, serializer, or encoding failure after input
validation, when the request runs, then it returns exact
`500 projection_invalid` bytes for that route's resource and no partial item.
Given an unknown, forbidden, malformed-key, or noncanonical-key request, then
it returns exact `404 not_found` bytes and does not return a resource-specific
legacy error code.

AC9 — **Cache and conditional requests.** Given each AC3 success and each AC6
through AC8 error, when the response is inspected, then it carries the two I5
application headers and no prohibited application header. Given the same
visible request with `If-None-Match` and `If-Modified-Since`, then the route
returns the same 200 item bytes and does not return 304.

AC10 — **Closed fields, types, and secret structure.** Given one fixture per
Table 1 resource that populates each nullable field, enum, array, nested
object, and opaque content slot, when the shared serializer runs through HTTP,
then the item has exactly its R7 keys in R7 order and the wire-schema types,
nullability, identifier spellings, timestamp forms, enum domains, nested keys,
array order, nested order, and conditional omissions. Randomizing source map
and set order 1,000 times produces identical item bytes. A structural scan of
serializer-owned fields finds none of I6's prohibited storage keys. Opaque
user content remains byte-preserved. A route-local decode, map reshape, or
re-encode fails the test even when semantic JSON equality holds. The turn
fixture fails on a `turnSeq` item key, and the device fixture fails on an `id`
item key.

AC11 — **Raw A6 parity.** Given one committed upsert fixture for each reviewed
R8 class whose resource is in Table 1, when the comparator captures the real
notice and authorized real HTTP detail response, then raw `payload` bytes
equal raw `item` bytes. The table also asserts exact class, operation,
serializer identity, resource mapping, primary-ref names, key equality, and
version type. An independent source-key assertion derives turn and device refs
from committed storage or mutation output before serialization, so matching
REST and notice aliases cannot create a tautological pass. The test fails if it
performs JSON re-encoding, uses a hand-made notice, accepts a route-local
projection, emits `payload.turnSeq`, emits `payload.id` for a device, or treats
an envelope resource label as item bytes.

AC12 — **Focused and full evidence.** Given the completed targetless product
branch, when verification runs, then focused route, auth, precedence, error,
cache, secret, key, type, seam-identity, and raw-parity tests pass. The builder
also records baseline and after counts from the repository's full green gate
on Gibson. The evidence names the product base SHA, candidate SHA, D1 landing
SHA, exact commands, pass/failure/skip counts, and the shared Table 1 test
source. A source-diff assertion rejects changes outside the touch boundary.

AC13 — **Scope separation.** Given the candidate diff, when a reviewer checks
it against the D1, G7, registry, Card 5, CLI, deployment, and release lanes,
then it contains only this card's routes, two query seams, two R7 conformance
corrections, focused tests, and required ref extraction. It does not contain
the G7 role/name or condition-fact id corrections. The candidate has no
integration target and performs no canonical landing, deployment, or release.

## Open Questions

None. D1's reviewed product landing is a blocking code-start dependency, not
an unresolved product choice. The two absent Table 1 query seams and two
mechanical R7 corrections are closed implementation requirements. Another
missing shared lookup, serializer, AU4 seam, or D1 adapter is an upstream
conformance defect and returns to the responsible owner; the core-detail
builder does not fill it with route-local behavior.
