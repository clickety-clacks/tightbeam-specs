# REST read plane D2 — remaining resource families and conformance

Status: build specification candidate for
`wi_ea98345b-51f4-4fae-b7df-3670c0d54f6b`.

Authority:

- Canonical `rest-state-api-v1.md` r3, artifact `art_971f45b5`, reviewed
  commit `8b96e512688cc3c010c33c96d1ba622e543c7206`, SHA-256
  `49b86ec874283c523001be7449b1e14aef47ca72932955445638ce6443aad754`.
- Normative companion `rest-state-api-v1-wire-schema.md` at the same canonical
  revision.
- Adopted six-resource shared-serializer contract `art_b1995a26`, SHA-256
  `72bb22676bc5cd116f696e23b21b382073efaa8dabbb2ae9d2a524641dd210f6`,
  adopted by decision fact 1093.
- D1 candidate `rest-read-plane-d1.md`, commit `5b1ffa2`, SHA-256
  `430cc2ab4768a44407e3338ea483927f2f2d0e71349deb83452815874d75f268`.
  D1's final reviewed canonical identity replaces this candidate identity at
  the code-start gate below; a seam-name difference requires a reviewed D2
  amendment before product code starts.
- Product-owner binding ruling, 2026-08-24 PT: durable human-intent Toplines
  keep `/api/toplines[/:id]`; work telemetry moves to the distinct
  `/api/execution-map` family. Contract closure is tracked by
  `wi_835a72aa-c88b-421b-a34c-41d23032c7c7` and
  `wi_3874a61f-288b-4b54-ac8a-da9234a910a2`.

## Spec home

The sole canonical repository home for this file is
`rest-read-plane-d2-v1.md` in `clickety-clacks/tightbeam-specs`. Landing and
review evidence record its containing commit and content SHA-256. A worktree,
artifact pointer, product-repository copy, or conversation is not an amendment
authority.

The D2 review set is this file plus `rest-state-api-v1.md` and
`rest-state-api-v1-wire-schema.md` at the Authority revision above, and the
adopted shared-serializer contract `art_b1995a26`. The D2 code-start set also
includes D1's final reviewed canonical spec and integration and the reviewed
canonical landings for `wi_835a72aa-c88b-421b-a34c-41d23032c7c7` and
`wi_3874a61f-288b-4b54-ac8a-da9234a910a2`. The code-start preflight records
their exact paths, commits, and SHA-256 values. This file references those
canonical landings and does not copy their draft bytes.

## Goal

Deliver the remaining canonical REST v1 collection, detail, nested, composed,
and asset-download reads after D1. A client can rebuild each admitted D2
resource from typed, authorized, deterministic responses without SQLite or a
legacy dispatch read.

## Non-Goals

- D2 does not implement the six D1 resource families: config, host
  environment, hosts, users, served identity, or kungfu.
- D2 does not add a REST-local query shape, serializer, visibility rule,
  projection field, credential, principal binding, authorization grant, or
  tailnet identity behavior.
- D2 does not change a firehose class, mapping, primary reference, version
  source, subscription filter, or payload byte.
- D2 does not migrate CLI wrappers, remove legacy dispatch reads, remove M5
  compatibility aliases, change writes, merge, deploy, or release. D3 owns CLI
  migration and removal gates.
- D2 does not add partial-name, case-folded-name, or arbitrary text search to
  `/api/sessions`. It consumes the exact `displayName` filter only after
  `wi_835a72aa-c88b-421b-a34c-41d23032c7c7` lands reviewed and canonical.
- D2 does not expose asset bytes through an artifact or work-item relation.

## Terms

- **D1 foundation**: `Tightbeam.Wire.Router.rest_read/3`,
  `Tightbeam.RestCursor.encode/4` and `decode/4`, and
  `Tightbeam.RestEnvelope.list/3` and `detail/2`, plus D1's authentication,
  status, error, and `Cache-Control: no-store` contract.
- **Query owner**: the named resource module that owns collection and detail
  selection. `Tightbeam.StateResources.list_<resource>/2` is its public REST
  collection entry point. A detail route calls the named `query_*` seam.
- **Public serializer**: the one `Tightbeam.StateResources` item function named
  in this spec. REST, a retained CLI wrapper, and an overlapping firehose state
  notice use that function.
- **Resolved principal**: the principal returned by D1's unchanged existing
  bearer and `asUser` resolver before a resource query runs.
- **Resolved user id**: the stable user id carried by a resolved user
  principal. A resolved session principal has no resolved user id; its
  `ownerUserId` metadata does not supply one.
- **Tuple cursor**: D1's opaque signed encoding of the resource name, complete
  immutable order tuple, filter fingerprint, and stable principal binding.
- **Composed resource**: a deterministic view with the closed R9 dependency
  class set and a `dependencyVersion` digest instead of its own state notice.
- **Same 404**: byte-identical status, body, headers, handler stages, database
  statement shape, and AU8 timing class for unknown and forbidden cases.

## Assumptions

1. Canonical green product `main` can contain the reviewed D1 implementation
   without changing the canonical R7/R7a projections, wire-schema types, AU4
   grants, R8 mappings, or R9 dependency sets.
2. The D1 reviewed specification will retain the candidate shared seam names.
   A name change falsifies this assumption and blocks D2 code until this file
   is amended and independently reviewed.
3. The product tables provide the immutable public natural keys and timestamps
   named in the cursor table below.
4. The firehose integration provides the canonical serializers, durable
   stored rows, write seams, and `rowVersion` values for its D2 overlap
   resources before D2 product code starts. This includes the read-marker row
   and set/clear seam, which do not exist on the pre-integration product base.
5. The reviewed canonical result of
   `wi_835a72aa-c88b-421b-a34c-41d23032c7c7` fixes the Toplines list and
   session `displayName` filter contract before D2 product code starts.
6. The reviewed canonical result of
   `wi_3874a61f-288b-4b54-ac8a-da9234a910a2` fixes the ExecutionMap R7 row,
   wire schema, R9 dependency set, and response-envelope shapes before D2
   product code starts.

## Invariants

1. D2 product code starts only after D1 has an independently reviewed-clean
   build spec and canonical green `main` contains D1's independently
   reviewed-clean implementation.
2. D2 product code starts only after both named REST contract-closure work
   items have independently reviewed canonical landings and every overlapping
   clause in this file conforms to their exact bytes.
3. `Router.rest_read/3` is the sole D2 GET dispatch seam. Route clauses do not
   query product tables, shape an item, encode a cursor, or build an envelope.
4. Each D2 resource has one query owner and one public item serializer. A
   collection and detail route for the same resource use the same owner and
   serializer.
5. A D2 serializer emits exactly the canonical R7/R7a field row and normative
   wire-schema types. Nullable fields remain present with JSON `null`.
6. A query evaluates its named AU4 visibility predicate before collection
   filtering, subscription filtering, serialization, pagination output, byte
   stat, byte open, or an existence-dependent response.
7. A detail, nested child, principal-mismatched cursor, and download use the
   same 404 for unknown and forbidden cases. An authorized collection omits a
   forbidden row.
8. A cursor contains the complete tuple in this spec and no offset, SQLite
   `rowid`, or live-row locator. Deleting its boundary row does not invalidate
   it.
9. A notice-backed REST item and its firehose notice payload are byte-identical
   after REST envelope removal. D2 adds no second public serializer.
10. A composed query reads only its declared R9 dependencies. Its
   `dependencyVersion` is the canonical digest of the ordered dependency
   vector.
11. Durable Toplines and mechanical ExecutionMap telemetry remain distinct
    resource families. One route, query seam, serializer, or envelope never
    carries both meanings.
12. D2 responses inherit D1's status, error envelope, authentication, and
    cache contract. `/download/:assetId` is the sole non-JSON success.
13. D2 introduces no product state and therefore introduces no mutation seam.

## Architecture

### Code-start gate

Before a product edit, the implementer records these five proofs:

1. D1's exact spec path, content SHA-256, and independently reviewed-clean
   verdict.
2. The exact D1 implementation commit and independently reviewed-clean
   verdict.
3. A green canonical `main` containing that D1 commit and the integrated
   shared firehose serializers, durable D2 rows, write seams, and version
   sources, including read markers.
4. The reviewed canonical commit, SHA-256, and verdict for
   `wi_835a72aa-c88b-421b-a34c-41d23032c7c7`.
5. The reviewed canonical commit, SHA-256, and verdict for
   `wi_3874a61f-288b-4b54-ac8a-da9234a910a2`.

A missing proof stops D2 code. A private D1, contract-amendment, or firehose
branch does not satisfy the gate. If a reviewed dependency changes a shared
name or contract listed here, amend and review this file before code starts.

### Shared dispatch and ownership

Each GET enters `Tightbeam.Wire.Router.rest_read/3`. A collection calls the
listed `Tightbeam.StateResources.list_<resource>/2` entry. A detail or composed
read calls the listed `query_*` entry. Each entry delegates storage selection
to the listed query-owner module, invokes the listed
`Tightbeam.StateVisibility` predicate, and passes rows to the listed
`Tightbeam.StateResources` serializer. The router then calls D1's cursor and
envelope seams.

The `list_<resource>/2` entries are collection adapters over the same query
owner and serializer. They are not alternate projections. For example,
`list_sessions/2` and `query_session/2` both serialize with `session/1`.
Every listed StateResources `/2` seam takes the resolved principal and one
normalized request map. That map contains route identifiers, admitted query
values, and transport parameters. It contains no raw query string.

| Resource | Routes | Query seam and owner | Serializer | Visibility |
|---|---|---|---|---|
| org | `GET /api/org` | `query_org/2` — `Tightbeam.Org` plus declared R9 dependencies | `org/1` | `org_visible?/1` |
| harness catalog | `GET /api/catalog/harnesses` | `list_harness_catalog/2` — `Tightbeam.ModelCatalog` | `harness_catalog/1` | `harness_catalog_visible?/1` |
| sessions | `GET /api/sessions`; `GET /api/sessions/:sessionKey` | `list_sessions/2`; `query_session/2` — `Tightbeam.Org` | `session/1` | `session_visible?/3` |
| transcript messages | `GET /api/sessions/:sessionKey/messages` | `list_messages/2` — `Tightbeam.Transcript` | `message/1` | `message_visible?/3` |
| coordination share | `GET /api/sessions/:sessionKey/coordination-share` | `query_coordination_share/2` — `Tightbeam.ExecutionMap` | `coordination_share/1` | `coordination_share_visible?/3` |
| work items | `GET /api/work-items`; `GET /api/work-items/:id` | `list_work_items/2`; `query_work_item/2` — `Tightbeam.WorkItems` | `work_item/1` | `work_item_visible?/3` |
| work-item trace | `GET /api/work-items/:id/trace` | `query_work_item_trace/2` — `Tightbeam.WorkItems` | `work_item_trace/1` | `work_item_trace_visible?/3` |
| assignments | `GET /api/assignments`; `GET /api/assignments/:id` | `list_assignments/2`; `query_assignment/2` — `Tightbeam.Assignments` | `assignment/1` | `assignment_visible?/3` |
| attests | `GET /api/attests`; `GET /api/assignments/:id/attests` | `list_attests/2` — `Tightbeam.Assignments` | `attest/1` | `attest_visible?/3` |
| wakes | `GET /api/wakes`; `GET /api/wakes/:wakeId` | `list_wakes/2`; `query_wake/2` — `Tightbeam.Wakes` | `wake/1` | `wake_visible?/3` |
| digest members | `GET /api/wakes/:wakeId/digest-members` | `list_digest_members/2` — `Tightbeam.Wakes` | `digest_member/1` | `digest_member_visible?/3` |
| turns | `GET /api/turns`; `GET /api/turns/:seq` | `list_turns/2`; `query_turn/2` — `Tightbeam.Ledger` | `turn/1` | `turn_visible?/3` |
| artifacts | `GET /api/artifacts`; `GET /api/artifacts/:artifactId` | `list_artifacts/2`; `query_artifact/2` — `Tightbeam.Artifacts` | `artifact/1` | `artifact_visible?/3` |
| assets | `GET /api/assets`; `GET /api/assets/:assetId`; `GET /download/:assetId` | `list_assets/2`; `query_asset/2` — `Tightbeam.Assets` | `asset/1` | `asset_visible?/3` |
| decision requests | `GET /api/decision-requests`; `GET /api/decision-requests/:id` | `list_decision_requests/2`; `query_decision_request/2` — `Tightbeam.Escalation` | `decision_request/1` | `decision_request_visible?/3` |
| read markers | `GET /api/read-markers`; `GET /api/read-markers/:scopeKey` | `list_read_markers/2`; `query_read_marker/2` — `Tightbeam.ReadMarkers` | `read_marker/1` | `read_marker_visible?/3` |
| roles | `GET /api/roles` | `list_roles/2` — `Tightbeam.Roles` | `role/1` | `role_visible?/3` |
| toplines | `GET /api/toplines`; `GET /api/toplines/:id` | `list_toplines/2`; `query_topline/2` — `Tightbeam.Toplines` | `topline/1` | `topline_visible?/3` |
| execution map — flat | `GET /api/execution-map` | `list_execution_map/2` — `Tightbeam.ExecutionMap` | canonical `execution_map_node/1` from `wi_3874a61f-288b-4b54-ac8a-da9234a910a2` | `execution_map_node_visible?/3` |
| execution map — tree | `GET /api/execution-map/tree` | `query_execution_map_tree/2` — `Tightbeam.ExecutionMap` | the same `execution_map_node/1` inside the canonical tree envelope from `wi_3874a61f-288b-4b54-ac8a-da9234a910a2` | `execution_map_node_visible?/3` |
| execution map — subtree | `GET /api/execution-map/subtrees/:workItemId` | `query_execution_map_subtree/2` — `Tightbeam.ExecutionMap` | the same `execution_map_node/1` inside the canonical subtree envelope from `wi_3874a61f-288b-4b54-ac8a-da9234a910a2` | `execution_map_node_visible?/3` |
| execution map — assignment selection | `GET /api/execution-map/assignments` | `query_execution_map_assignments/2` — `Tightbeam.ExecutionMap` | the same `execution_map_node/1` inside the canonical assignment-selection envelope from `wi_3874a61f-288b-4b54-ac8a-da9234a910a2` | `execution_map_assignment_visible?/3`, then `execution_map_node_visible?/3` |
| facts | `GET /api/facts` | `list_condition_facts/2` — `Tightbeam.ConditionFacts` | `condition_fact/1` | `condition_fact_visible?/3` |
| critical state | `GET /api/critical-state` | `list_critical_state/2` — `Tightbeam.CriticalLeases` | `critical_state/1` | `critical_state_visible?/1` |
| archetypes | `GET /api/archetypes`; `GET /api/archetypes/:name` | `list_archetypes/2`; `query_archetype/2` — `Tightbeam.Archetypes` | `archetype/1` | `archetype_visible?/1` |
| guidance | `GET /api/guidance`; `GET /api/guidance/:name` | `list_guidance/2`; `query_guidance/2` — `Tightbeam.Identity` | `guidance/1` | `guidance_visible?/1` |
| rails | `GET /api/rails`; `GET /api/rails/:name` | `list_rails/2`; `query_rail/2` — `Tightbeam.Rails` | `rail/1` | `rail_visible?/1` |
| harness processes | `GET /api/harness-processes` | `list_harness_processes/2` — `Tightbeam.HarnessProcess` | `harness_process/1` | `harness_process_visible?/1` |
| devices | `GET /api/devices`; `GET /api/devices/:deviceId` | `list_devices/2`; `query_device/2` — `Tightbeam.Devices` | `device/1` | `device_visible?/1` |

`/api/toplines[/:id]` serializes only durable human-intent Toplines. The four
ExecutionMap routes serialize only mechanical work telemetry. The exact
ExecutionMap R7 and envelope shapes live in the reviewed canonical result of
`wi_3874a61f-288b-4b54-ac8a-da9234a910a2`; D2 references that one home and
does not restate or fork the projection.

### Filter allowlists

`before`, `after`, `limit`, and `asUser` are D1 transport parameters, not
resource filters. Different listed resource filters are conjunctive. Repeated
values for one listed filter are disjunctive. A repeated singleton transport
parameter is invalid. An unlisted query key returns `400 invalid_filter`.

| Resource | Allowed collection filters |
|---|---|
| org | none |
| harness catalog | none |
| sessions | `state`, `ownerUserId` (admin only), `spawnedBy`, `archetype`, `harness`, `provider`, `model`, `host`, `role`, `displayName` exact after `wi_835a72aa-c88b-421b-a34c-41d23032c7c7` lands canonical |
| transcript messages | none |
| coordination share | required singleton `from`, `to` epoch-millisecond bounds; `from < to` |
| work items | `state`, `ownerUserId`, `createdBySession`, `createdByUser`, `isBug`, `specRefName`, `holderKey` |
| work-item trace | none |
| assignments | `state`, `outcome`, `holderKey`, `holderRole`, `workItemId`, `reviewsAssignmentId`, `effectKind`, `derivedStatus` |
| attests | `assignmentId`, `workItemId`, `kind`, `verdictKind`, `bySession`, `byUser` |
| wakes | `state`, `sessionKey`, `creatorSessionKey`, `workItemId`, `assignmentId`, `conditionKind`, `conditionScope`, `class`, `dueAtFromInclusive`, `dueAtToExclusive`, `firedAtFromInclusive`, `firedAtToExclusive` |
| digest members | none |
| turns | `status`, `sessionKey`, `assignmentId`, `workItemId`, `wakeId`, `jobRef`, `createdAtFromInclusive`, `createdAtToExclusive`, `startedAtFromInclusive`, `startedAtToExclusive`, `endedAtFromInclusive`, `endedAtToExclusive` |
| artifacts | `workItemId`, `createdBySession`, `kind`, `state` |
| assets | `ownerUserId` (admin only), `mimeType` exact |
| decision requests | `status`, `kind`, `ownerUserId`, `assignmentId`, `raiserSessionKey`, `expecterSessionKey` |
| read markers | `scopeKey` exact or `scopeKeyPrefix`; the two are mutually exclusive; a non-admin collection binds `userId` to the resolved user; no collection exposes a `userId` filter |
| roles | `ownerUserId`, `boundSessionKey` |
| toplines | `state` only |
| execution map — flat, tree, subtree | `origin`, `ownerUserId`, `state`, `quietOverMs`, `specRefName`, dependent optional `specRefSha256`, `sessionKey` |
| execution map — assignment selection | repeated `assignmentId` only; no roster filter |
| facts | `kind`, `scope`, `origin`, `tsFromInclusive`, `tsToExclusive` |
| critical state | `sessionKey` exact |
| archetypes | `skill`, `host`, `harness` |
| guidance | `name` exact |
| rails | `mode`, `tool` |
| harness processes | `sessionKey`, `host`, `harness`, `provider`, `model`, `state` |
| devices | `status`, `userId` |

An unknown enum returns `400 invalid_filter`. An unknown exact-id filter returns
an empty authorized collection. A lower time bound compares `>=`; an upper
time bound compares `<`. A missing bound is open. For ExecutionMap,
`specRefSha256` is allowed only when `specRefName` is present, and
`quietOverMs` is a non-negative integer number of milliseconds. The reviewed
canonical closures own every enum domain, default, duplicate-value behavior,
empty-selection behavior, and validation error beyond the binding allowlists
stated here. D2 does not copy those closure contracts. D2 adds no `fields`,
`sort`, `include`, offset, generic join, roster, partial-name, or name-pattern
filter.

`GET /api/read-markers/:scopeKey` always resolves the singular composite key
`(resolvedUserId,scopeKey)`. This binding applies to every resolved user
principal, including an admin. An admin operator that needs another user's
marker uses the existing D1 org-bearer `asUser=<targetUserId>` transport
parameter so the principal resolver supplies that target user id before the
query. A session principal has no `resolvedUserId` for this route. It receives
the same 404 after `query_read_marker/2` executes the same parameterized
composite-key statement with a SQL `NULL` user-id parameter; the statement
cannot match a non-null marker key and performs no target-key lookup. A
`userId` query key remains `400 invalid_filter`. Thus two allowed rows with one
`scopeKey` never compete for one detail envelope.

### Deterministic order and tuple cursors

Each pageable route returns the newest page when no cursor is present. Items
inside a page are oldest to newest. `before` and `after` are mutually exclusive
bounds. `limit` defaults to 50 and clamps at 500.

| Pageable resource | Immutable cursor tuple |
|---|---|
| sessions | `(createdAt,sessionKey)` |
| transcript messages | `(seq,id)` |
| work items | `(createdAt,id)` |
| assignments | `(openedAt,id)` |
| attests | `(ts,id)` |
| wakes | `(createdAt,wakeId)` |
| turns | `(seq)` |
| artifacts | `(createdAt,artifactId)` |
| assets | `(createdAt,assetId)` |
| decision requests | `(raisedAt,id)` |
| read markers | `(userId,scopeKey)` |
| roles | `(createdAt,name)` |
| toplines | `(createdAt,id)` |
| execution map — flat | `(createdAt,id)` |
| facts | `(id)` |
| critical state | `(sessionKey)` |
| archetypes | `(name)` |
| guidance | `(name)` |
| rails | `(name)` |
| harness processes | `(startedAt,id)` |
| devices | `(createdAt,deviceId)` |

`/api/org`, harness catalog, coordination share, work-item trace, digest
members, execution-map tree, execution-map subtree, and execution-map
assignment selection are unpaged and do not accept page parameters. A detail
route does not accept page parameters. Updating each visited read marker
cannot move it because its tuple contains only immutable key parts. Two users
with one `scopeKey` retain distinct cursor identities.

### Authorization and same-404 matrix

The visibility function applies this canonical AU4 matrix. “Owner” means the
user principal. A session does not borrow its owner's grants or admin bit.

| Resource | Allowed resolved principals |
|---|---|
| org, harness catalog, roles | authenticated org user or session |
| sessions, transcript messages, coordination share | target session; target session owner; admin |
| work items, work-item trace | work-item owner; creating session; session holding an assignment on the item; admin |
| assignments | holder session; work-item owner; user or session opener; admin |
| attests | a principal allowed to read the parent assignment |
| wakes | target session; creator session; target-session owner; creator-session owner; admin |
| digest members | a principal allowed to read the parent digest-carrier wake |
| turns | target session; target-session owner; admin |
| artifacts | creating session; work-item owner; principal allowed to read linked work item; admin |
| assets | asset `ownerUserId` user; admin |
| statute decision requests | raiser; `ownerUserId` user; admin |
| effort decision requests | named expecter session or user; linked-assignment holder; admin |
| agent decision requests | asker session; asked session; accountable owner user; admin |
| read markers | marker `userId` user; admin |
| toplines | topline owner; admin |
| execution map — flat, tree, subtree | principals admitted by the underlying work-item AU4 grants in the reviewed `wi_3874a61f-288b-4b54-ac8a-da9234a910a2` canonical closure |
| execution map — assignment selection | principals admitted by the assignment AU4 grants before selection and the underlying work-item AU4 grants before node emission, as fixed by the reviewed `wi_3874a61f-288b-4b54-ac8a-da9234a910a2` canonical closure |
| facts | filing session; filing-session owner; admin; a process-origin fact is admin only |
| critical state, archetypes, guidance, rails, harness processes, devices | admin only |

A nested handler checks the parent and child through their named predicates.
It performs no child serialization until both checks allow the read. A
forbidden parent, forbidden child, unknown parent, and unknown child return the
same 404. A cursor principal-binding mismatch returns that same 404.

For `/download/:assetId`, `query_asset/2` reads the exact metadata row and
`asset_visible?/3` runs before `File.stat`, path construction that touches the
filesystem, or byte open. An artifact relation, work-item relation, matching
filename, or guessed path grants nothing.

### Visibility before firehose subscription filters

D2 does not change firehose delivery. Its conformance suite calls the existing
publisher with a hidden row that matches `classes`, `sessionKey`, `workItemId`,
`origin`, and `principal`. The publisher must call the resource's named
visibility function first and must not call the subscription matcher after a
denial. A delete uses the last pre-delete projection for this check. The suite
requires no frame and no distinguishable error.

### Safe-value and content allowlists

D2 adds no safe config or host-environment value. Those allowlists remain D1's
`default-archetype` and empty list respectively.

| Resource | Exact D2 exposure boundary |
|---|---|
| sessions | R7 fields only; omit `cliToken` |
| devices | R7 fields only; omit `token` |
| harness processes | R7a fields only; omit `identityToken`, credential-bearing paths, command environment, and environment values |
| toplines | canonical R7 fields only; no ExecutionMap node or envelope field |
| execution map | exact R7 fields from the reviewed `wi_3874a61f-288b-4b54-ac8a-da9234a910a2` canonical closure; no Topline field or serializer |
| archetypes | committed live served-identity bytes only; MCP entries contain only `name` and sorted `envNames`; omit commands, arguments, values, and host paths |
| guidance | built-in served guidance and committed `identity/guidance/*.md` only; one shared sanitizer owns `content` |
| rails | parsed committed `identity/rails/*.toml` only; one shared sanitizer owns `pattern` and `text` |
| assets | R7 metadata only in JSON; bytes only through authorized `/download/:assetId` |

The shared content sanitizer replaces a full secret-bank value, PEM private-key
block, bearer or API-token assignment, Tightbeam-base absolute path, and
operating-system-home absolute path with the canonical redaction marker. It
does not read environment values to enrich output. A symlink, traversal,
dotfile, receipt, manifest, or non-allowlisted identity source does not enter a
D2 item.

### Composed-view dependencies

The query owner extracts exactly the listed R9 classes. `dependencyVersion`
is the lowercase SHA-256 digest of canonical JSON
`[resource,primaryKey,rowVersion]` entries sorted by resource and canonical
primary-key bytes.

| Composed resource | Closed refetch dependency set |
|---|---|
| org | `host.registered`, `config.updated`, `identity.updated`, `kungfu.updated` |
| harness catalog | `host.registered`, `host_env.updated`, `config.updated` |
| coordination share | `wake.*`, `turn.*`, `prod.fired` |
| digest members | `wake.scheduled`, `wake.canceled`, `wake.fired` |
| work-item trace | `work_item.*`, `assignment.*`, `attest.filed`, `session.*`, `wake.*`, `turn.*` |
| toplines | `work_item.*`, `assignment.*`, `attest.filed`, `session.*`, `role.*`, `wake.*`, `turn.*`, `decision_request.*` |
| archetypes | `identity.updated`, `kungfu.updated` |
| guidance | `identity.updated`, `kungfu.updated` |
| rails | `identity.updated`, `kungfu.updated` |

The reviewed canonical result of `wi_3874a61f-288b-4b54-ac8a-da9234a910a2`
owns the exact ExecutionMap dependency set. D2 consumes that closed set after
reviewed canonical landing and does not duplicate it here.

### Envelopes, status, cache, and download

A JSON collection returns HTTP 200 through `RestEnvelope.list/3`:

`{"schemaVersion":1,"resource":"assignments","items":[],"page":{"oldestCursor":null,"newestCursor":null,"hasMoreBefore":false,"hasMoreAfter":false}}`

A JSON detail or singleton composed read returns HTTP 200 through
`RestEnvelope.detail/2`:

`{"schemaVersion":1,"resource":"assignments","item":{}}`

The three unpaged ExecutionMap response shapes are the exact reviewed
canonical envelopes from `wi_3874a61f-288b-4b54-ac8a-da9234a910a2`. They
reuse D1 envelope utilities. D2 does not define or duplicate those shapes.

The resource string is the canonical R7/R8 resource name. JSON uses UTF-8,
compact encoding, and `application/json`. Success and error responses include
`Cache-Control: no-store`. D2 adds no ETag, conditional GET, or public cache
behavior.

D2 inherits these D1 outcomes: absent or invalid bearer is `401 auth_failed`;
invalid filter or bounded-time value is `400 invalid_filter`; invalid cursor
structure, resource, or filter fingerprint is `400 invalid_cursor`; malformed
query encoding is `400 malformed_query`; a principal-bound cursor mismatch and
unknown or forbidden detail are `404 not_found`. The D1 error encoder owns the
exact JSON error body.

An authorized `/download/:assetId` returns HTTP 200 bytes with the metadata
row's `Content-Type`, exact stored size, and `Cache-Control: no-store`. It has
no JSON envelope. Its error paths use the D1 JSON error encoder and cache
header. D2 adds no `Content-Disposition` contract.

### Touchpoints

- `lib/tightbeam/wire/router.ex`: D2 GET clauses and reuse of
  `rest_read/3`; download authorization before byte open.
- `lib/tightbeam/state_resources.ex`: D2 `list_*`, `query_*`, and public
  serializers; existing serializers remain unchanged unless the canonical
  R7/wire schema requires the missing named function.
- `lib/tightbeam/state_visibility.ex`: the named AU4 predicates and
  visibility-before-filter call order.
- `lib/tightbeam/rest_cursor.ex` and `lib/tightbeam/rest_envelope.ex`: reuse
  only; D2 adds no second cursor or envelope implementation.
- `lib/tightbeam/org.ex`, `transcript.ex`, `work_items.ex`, `assignments.ex`,
  `wakes.ex`, `ledger.ex`, `artifacts.ex`, `assets.ex`, `escalation.ex`,
  `read_markers.ex`, `roles.ex`, `toplines.ex`, `execution_map.ex`,
  `condition_facts.ex`, `critical_leases.ex`, `archetypes.ex`, `identity.ex`,
  `rails.ex`, `harness_process.ex`, and `devices.ex`: query ownership listed
  above.
- `lib/tightbeam/firehose/registry.ex` and publisher modules: contract and
  visibility-order tests only; D2 changes no class or payload.
- `test/router_test.exs`, resource-module tests,
  `test/firehose_publisher_test.exs`, and
  `test/rest_read_plane_d2_conformance_test.exs`: routes, filters, tuples,
  shapes, authorization, same-404, cache, download, dependency digests, and
  parity.

Subtraction decision: add these GET adapters because the canonical product
spec requires typed rebuildable state. Deleting the resources would remove the
read-plane goal; accepting dispatch or SQLite access would preserve the
forbidden coupling.

## Acceptance

Implement the numbered cases as ExUnit tests in
`test/rest_read_plane_d2_conformance_test.exs`, with route-dispatch cases in
`test/router_test.exs` and publisher-order cases in
`test/firehose_publisher_test.exs`. Run:

```sh
mix test test/rest_read_plane_d2_conformance_test.exs test/router_test.exs test/firehose_publisher_test.exs
```

A missing numbered case fails conformance.

1. **Code-start gate.** Given D1 lacks one required reviewed-clean or
   canonical-green proof, when the D2 implementer runs preflight, then
   preflight fails before a product source edit.
2. **Route inventory.** Given the D2 route table, when a table-driven router
   test issues each collection, detail, nested, composed, metadata, and
   download GET, then each route reaches its listed query seam and no listed
   route is absent.
3. **Shared ownership.** Given instrumentation on the router and resource
   seams, when a collection and detail for one resource run, then both invoke
   the listed query owner, visibility predicate, and one public serializer;
   the router emits no item field itself.
4. **Closed wire shape.** Given each R7/R7a D2 item with randomized input map
   and set order over 1,000 runs, when its serializer runs, then the JSON bytes
   match the normative field order, types, nullability, nested keys, enum
   domains, and canonical array order on each run.
5. **List envelopes.** Given an authorized empty collection and a nonempty
   collection, when each GET runs, then it returns HTTP 200, the exact D1 list
   envelope, `schemaVersion:1`, the canonical resource string, page metadata,
   and `Cache-Control:no-store`.
6. **Detail envelopes.** Given an authorized known row, when its detail GET
   runs, then it returns HTTP 200, the exact D1 detail envelope, the listed
   serializer's item, and `Cache-Control:no-store`.
7. **Filters.** Given each listed filter, one unlisted key, one unknown enum,
   and one unknown exact identifier, when the collection runs, then listed
   filters restrict the authorized set, the unlisted key and unknown enum
   return `400 invalid_filter`, and the unknown exact identifier returns an
   empty list.
8. **Time bounds.** Given a row at each lower and upper wake, turn, and fact
   boundary, when the paired inclusive/exclusive filters run, then the lower
   row appears and the upper row does not; an invalid integer returns `400
   invalid_filter`.
9. **Tuple pagination.** Given tied leading tuple components, a deleted
   boundary row, deleted neighbors, and more than 500 rows, when each pageable
   resource pages before and after, then each authorized key appears once in
   tuple order, default limit is 50, `limit=501` returns 500, and the cursor
   decodes to the complete listed tuple without rowid, offset, or locator.
10. **Read-marker composite key.** Given two users with the same `scopeKey`,
    an admin, and an admin-owned marker with that scope, when each authorized
    collection pages while each visited marker updates, then each
    `(userId,scopeKey)` appears once, the admin collection includes all three
    rows, and no marker crosses principals.
11. **Cursor precedence.** Given malformed, wrong-resource,
    changed-filter, wrong-principal, and now-hidden cursor cases, when each
    request runs, then the first three return `400 invalid_cursor` before row
    lookup, wrong-principal returns the same 404, and a now-hidden row is
    omitted from the authorized page.
12. **AU4 matrix.** Given each D2 resource, each principal granted in its AU4
    row, and a session owned by an otherwise granted user, when reads run,
    then only the explicit principals receive items; the session receives no
    borrowed owner or admin grant.
13. **Nested same-404.** Given an allowed parent with denied child, a denied
    parent with allowed child, an unknown parent, and an unknown child, when
    the nested routes run, then the four responses have identical 404 body,
    status, headers, statement shape, and AU8 timing class.
14. **Download same-404.** Given known-allowed, known-denied, and unknown asset
    ids, when `/download/:assetId` runs, then the allowed case returns exact
    bytes and metadata content type while the denied and unknown cases are the
    same 404 and perform no file stat or byte open.
15. **Visibility before subscription filters.** Given a hidden upsert and
    delete whose last projection matches each subscription filter, when the
    publisher evaluates delivery, then visibility returns false, the matcher
    is not invoked, and no frame or distinguishable error appears.
16. **Safe-value boundary.** Given fixtures containing session and device
    tokens, a harness identity token, credentials, MCP commands and values,
    PEM material, banked secrets, home paths, Tightbeam paths, symlinks,
    traversal, receipts, manifests, and unlisted identity content, when D2
    routes serialize them, then only the exact allowlisted fields and redaction
    markers appear.
17. **Firehose byte parity.** Given each notice-backed D2 resource and its
    matching REST detail, when the REST envelope is removed, then item JSON
    bytes equal notice payload bytes and primary ids equal notice refs.
18. **Composed dependencies.** Given one mutation for each listed dependency
    and one unlisted state class, when each composed view refetches, then each
    listed mutation changes `dependencyVersion`, the unlisted class leaves it
    unchanged, and dependency extraction equals this spec's closed set or the
    reviewed canonical ExecutionMap closure's closed set, as applicable.
19. **Facts and critical state.** Given allowed and denied principals plus
    older, duplicate, and newer snapshots and notices, when facts and critical
    state rebuild, then the fact id, notice ref, and row version are equal JSON
    integers and both resources converge by last-version-wins per primary key.
20. **D1 reuse.** Given a structural scan of the D2 change, when it finds a
    REST-local serializer, projection, cursor codec, envelope encoder, or
    duplicate visibility rule, then the conformance gate fails.
21. **Canonical closure gate.** Given either
    `wi_835a72aa-c88b-421b-a34c-41d23032c7c7` or
    `wi_3874a61f-288b-4b54-ac8a-da9234a910a2` lacks a reviewed canonical
    commit and SHA-256, when D2 preflight runs, then preflight fails before a
    product source edit.
22. **Toplines semantic boundary.** Given durable human-intent Toplines and
    mechanical work telemetry, when `/api/toplines` and
    `/api/toplines/:id` run, then they invoke `Tightbeam.Toplines`, accept no
    list filter except `state`, page by `(createdAt,id)`, and emit only
    `topline/1` items; no ExecutionMap node or envelope appears.
23. **ExecutionMap route modes.** Given authorized telemetry, when the four
    ExecutionMap routes run, then `/api/execution-map` is a flat collection
    paged by `(createdAt,id)` and the tree, subtree, and repeated-assignment-id
    selection routes are unpaged; no route invokes `topline/1`.
24. **ExecutionMap filter and visibility order.** Given one visible and one
    hidden node that both match each allowed flat, tree, or subtree filter,
    and an assignment selection with a hidden assignment or hidden node, when
    the routes run, then visibility executes before every allowed filter and
    before assignment or node serialization; an unlisted or roster filter
    returns `400 invalid_filter`.
25. **Exact session-name lookup.** Given sessions with equal and near-match
    display names, when `/api/sessions?displayName=<exact>` runs after the
    reviewed `wi_835a72aa-c88b-421b-a34c-41d23032c7c7` canonical closure
    lands, then only exact matches within the visible set appear and partial
    or case-folded lookup is not introduced.
26. **Unpaged routes.** Given each route declared unpaged and each of
    `before`, `after`, and `limit`, when the test sends one page parameter at
    a time, then the route returns `400 invalid_filter` and performs no
    resource query.
27. **Read-marker storage gate.** Given canonical `main` lacks the durable
    `(userId,scopeKey)` row, set/clear write seam, or monotonic version source,
    when D2 preflight runs, then it fails before `Tightbeam.ReadMarkers` query
    code is added.
28. **Read-marker detail identity.** Given two owners and an admin each have a
    marker with the same `scopeKey`, when the admin user credential calls the
    detail route directly and the org bearer then calls it once through
    existing D1 `asUser` for each owner, then the direct call returns only
    `(adminUserId,scopeKey)` and the two resolved-user calls return only their
    respective composite rows. A `userId` query key returns D1's invalid-filter
    error with HTTP 400. A session principal receives the same 404 after one
    equal-shape, equal-count statement with a SQL `NULL` user-id parameter and
    without a target-key lookup or row serialization.

## Open Questions

None. The product-owner binding ruling closed the route-identity question.
The two reviewed canonical closures remain code-start dependencies, not open
design questions.
