# REST read plane D1 — transport foundation and six shared-seam resources

Status: build specification. Authority: canonical REST r3 `art_971f45b5`,
reviewed SHA-256 `49b86ec874283c523001be7449b1e14aef47ca72932955445638ce6443aad754`;
the adopted six-resource contract `art_b1995a26` / fact 1093; reviewed
firehose tip `8e4a412f25950dae1e1f33af42c390a4707bcf89`; PO rulings
`att_2d3a8333` and `att_304a6d07`; and the reviewed canonical AU2 repair
required by `wi_b0a6f85f-3523-45bb-8d10-1a67a2ad02bb` /
`asg_cd74975c-70c4-479b-8e34-20f91ef44452`.

## Spec homing

This file is the D1 build specification for
`wi_ed4f9020-3fb9-4ee1-9f8f-0cb2629fed96`. Its reviewed content hash, rather
than an unreviewed branch tip or a worktree copy, is the implementation
binding. A later D1 amendment replaces this file and receives a fresh exact
review before the work item binding changes.

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
  reference, version source, firehose payload activation, CLI migration,
  compatibility-alias removal, write route, deployment, or release behavior.
- D1 does not start M3 through M8. M1 owns the shared seams; D1 is M2.

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
3. Visibility precedes serialization, pagination, and response emission.
   Where one D1 detail resource mechanically has both an unknown and a
   forbidden case, those cases have the canonical identical `404 not_found`
   body, headers, statement shape, and timing class. Identity known `served`
   and unknown names both pass through `StateResources.query_identity/2`
   before visibility.
4. A REST detail item has exactly its R7/R7a fields. For the six notice-backed
   resources, its serialized item bytes equal the corresponding firehose
   payload bytes after the outer object is removed.
5. Success and error responses carry `Cache-Control: no-store`. D1 emits no
   ETag and implements no conditional request behavior.
6. M1 freezes projections, R8 mappings, R9 dependencies, and AU4 visibility.
   M2 adds REST on those seams before M3 points firehose payload builders to
   the same serializers.

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
detail case. A denied collection omits unreadable rows. A denied detail uses
the canonical identical `404 not_found` result. The transport returns
`400 invalid_filter` and `400 invalid_cursor` before a resource-row lookup in
the cases specified above. It uses the canonical error envelope and
`Cache-Control: no-store` for these errors.

### Implementation and test touchpoints

- `lib/tightbeam/wire/router.ex`: add the listed GET matches; reuse bearer and
  AU2 dispatch-parity resolution; call M1 seams; encode R4 responses and
  canonical errors.
- `lib/tightbeam/state_resources.ex`: M1-owned collection capability within
  the six named query seams; the six named serializers remain the sole public
  item encoders.
- `lib/tightbeam/state_visibility.ex`: M1-owned AU4 predicates; the hosts
  predicate changes from the old admin-only behavior to authenticated-org
  user/session visibility before D1 consumes it.
- `lib/tightbeam/firehose/registry.ex` and
  `lib/tightbeam/admin_projection.ex`: contract tests for the shared seams;
  no REST registry, REST projection, or D1 firehose activation.
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
11. Given one unknown detail and one forbidden detail for config, users,
    identity, and kungfu, when a warmed in-process suite sends at least 10,000
    randomized real HTTP requests for each case, then both cases use the same
    handler stages, database statement shape, response encoder, and
    `Cache-Control: no-store`. The suite records equal statement counts,
    proves neither path opens bytes, and proves both p50 and p95 differ by at
    most 5%.
12. Given non-admin requests for `GET /api/identity/served` and
    `GET /api/identity/:unknown`, when the warmed suite traces the canonical
    seam, then both requests enter `StateResources.query_identity/2` before
    visibility, record the same statement shape and count, emit the same
    canonical 404 without opening payload bytes, and retain the timing bound in
    Acceptance 11.
13. Given the route table and AU4 visibility rules, when the contract test
    checks the structural exclusions, then it proves `/api/host-env` exposes
    no detail route and hosts admit every authenticated org user or session, so
    D1 has no unknown-versus-forbidden detail pair for host environment or
    authenticated host details.
14. Given the integrated registry, when the contract test reads its six rows,
    then every row names the same query, serializer, visibility, primary refs,
    and version source used by REST. The test fails if router code adds a
    REST-local serializer, projection, field, or parallel `list_*` query seam.

## Open Questions

None. A new D1 filter, host-environment detail route, public item field, or
principal rule requires a canonical REST amendment. D1 code remains blocked
until the reviewed AU2 correction described in Assumption 3 lands on canonical
green `main`.
