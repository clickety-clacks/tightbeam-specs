# REST read plane D1 — transport foundation and six shared-seam resources

Status: build specification. Authority: canonical REST r3 `art_971f45b5`,
reviewed SHA-256 `49b86ec874283c523001be7449b1e14aef47ca72932955445638ce6443aad754`;
the adopted six-resource contract `art_b1995a26` / fact 1093; and reviewed
firehose tip `8e4a412f25950dae1e1f33af42c390a4707bcf89`.

## Goal

Deliver deterministic REST list and detail reads for config, host environment,
hosts, users, served identity, and kungfu. REST calls the existing shared query,
public serializer, and visibility seam for each resource.

## Non-Goals

- D1 adds no REST-local serializer, projection, field, credential, principal
  binding, authorization grant, or tailnet identity behavior.
- D1 does not change firehose classes, primary references, version sources, or
  payload bytes.
- D1 does not implement remaining resources, nested/download reads, composed
  views, CLI migration, alias removal, or writes.
- D1 is M2 only. It does not start M3–M8 work and preserves canonical M1–M8.

## Terms

- **Shared seam**: the named `StateResources` query and serializer plus the
  named `StateVisibility` predicate, called by REST and firehose.
- **Resolved principal**: the existing bearer-authenticated principal after
  existing CLI `asUser` handling. `asUser` does not authenticate a request.
- **Tuple cursor**: opaque signed exclusive page boundary with resource,
  complete immutable sort tuple, filter fingerprint, and principal binding.

## Assumptions

1. Before D1 code starts, canonical green `main` contains the integrated result
   for `asg_fd993fc7-43fd-401f-9433-190e07d5d7f1`.
2. That integration preserves the six seams at reviewed tip `8e4a412f`, or a
   reviewed equivalent. A contract test proves the current registry names them.
3. Existing router authentication distinguishes organization CLI, session CLI,
   and device bearer credentials before the resource read runs.

## Invariants

1. A handler gets raw data through its table query seam, serializes through its
   table serializer, and checks its table visibility predicate. It never maps
   raw rows itself.
2. Visibility runs before serialization, pagination, or output. Unknown and
   forbidden details return identical `404 not_found` responses.
3. Each item has exactly its canonical R7a fields. REST detail item bytes equal
   the corresponding firehose payload bytes after outer-envelope removal.
4. Each success and error response includes `Cache-Control: no-store`.
5. M1 owns projections, R8 mappings, and visibility. D1 consumes those seams;
   M3 through M8 remain independently gated.

## Architecture

### Code-start gate

The implementer proves canonical green `main` contains the integration result
for `asg_fd993fc7-43fd-401f-9433-190e07d5d7f1` before any product edit. A base
lacking it, including a private firehose branch, fails this gate. This avoids a
second serializer; accepting a duplicate would violate the shared contract.

### Routes, seams, filters, and order

Collection enumeration belongs in `Tightbeam.StateResources`, beside the named
detail query. It normalizes rows for that same serializer; router code owns
neither a query nor an item shape.

| Resource and routes | Query seam | Serializer / visibility | Filters | Tuple |
|---|---|---|---|---|
| config: `/api/config`, `/api/config/:key` | `query_config/2` | `config/1`; `config_visible?/1` | `key` exact | `(key)` |
| host environment: `/api/host-env` | `query_host_environment/2`, `/4` detail | `host_environment/1`; `host_environment_visible?/1` | `host`, `harness`, `name` exact | `(host,harness,name)` |
| hosts: `/api/hosts`, `/api/hosts/:host` | `query_host/2` | `host/1`; `host_visible?/1` | `host` exact | `(host)` |
| users: `/api/users`, `/api/users/:userId` | `query_user/2` | `user/1`; `user_visible?/1` | none | `(createdAt,userId)` |
| identity: `/api/identity`, `/api/identity/:name` | `query_identity/2`; only `served` resolves | `identity/1`; `identity_visible?/1` | `name`, `state` exact | `(name)` |
| kungfu: `/api/kungfu`, `/api/kungfu/:name` | `kungfu_names/1`, then `query_kungfu/2` | `kungfu/1`; `kungfu_visible?/1` | `status`, `rootArchetype` exact | `(name)` |

Repeated values for one listed filter are disjunctive. Different filters are
conjunctive. Each unlisted query key returns `400 invalid_filter`. Users accept
no collection filter because its canonical projection has neither status nor
ownership. An identity detail name other than `served` is unknown.

Each list returns R4's `schemaVersion`, `resource`, `items`, and `page`
envelope. Each detail returns R4's `schemaVersion`, `resource`, and `item`
envelope. Resource strings exactly match the registry: `config`, `host
environment`, `hosts`, `users`, `identity`, and `kungfu`.

`before` and `after` are mutually exclusive exclusive bounds. No cursor gives
the newest page; items are oldest to newest. `limit` defaults to 50 and clamps
at 500. Cursor validation checks encoding, version, resource, filter fingerprint,
and principal binding before any row lookup. Cursors contain no offset, SQLite
`rowid`, or live-row locator.

### Authentication, visibility, status, and cache

Use `Authorization: Bearer <existing gateway credential>` and AU1/AU2 unchanged.
Invalid or absent bearer returns `401 auth_failed`. An organization CLI bearer
needs exactly one `asUser`: missing returns `400 invalid_message`, repeated
returns `400 invalid_as_user`, and malformed percent encoding returns `400
malformed_query` before resolution. A device bearer plus `asUser` returns `400
invalid_as_user` before resolution. A session bearer remains a session; owner
mismatch returns existing `403 identity_not_yours`.

Each D1 resource is admin-only. The named predicate evaluates the resolved
principal. A non-admin list or detail returns `404 not_found`. Invalid listed
filter values return `400 invalid_filter`. A malformed, wrong-resource, or
changed-filter cursor returns `400 invalid_cursor`; a cursor bound to another
principal returns `404 not_found`. Successful and error JSON responses include
`Cache-Control: no-store`; D1 adds no ETag or conditional-request behavior.

### Touchpoints

- `lib/tightbeam/wire/router.ex`: routes, existing bearer/`asUser` reuse,
  envelopes, validation, and error encoding.
- `lib/tightbeam/state_resources.ex`: shared collection enumeration only;
  existing serializers remain the only public item encoders.
- `lib/tightbeam/state_visibility.ex`: invoke listed predicates; no router copy.
- `lib/tightbeam/firehose/registry.ex` and `admin_projection.ex`: contract
  checks only; no REST registry or REST projection.
- `test/router_test.exs`, `test/admin_projection_test.exs`, and a focused REST
  route suite: routes, auth, visibility, filters, cursors, cache, closed-world
  shapes, and firehose-byte parity.

## Acceptance

1. Given a canonical main without the named firehose integration, when D1's
   code-start check runs, then it fails before a product source edit.
2. Given integrated green main and an admin bearer, when each list and detail
   route runs, then it returns HTTP 200, its R4 envelope, `schemaVersion:1`,
   `Cache-Control:no-store`, and an item from the listed serializer.
3. Given a raw row with an extra or missing canonical field, when the route
   serializes it, then the serializer refuses and no partial item is emitted.
4. Given each matching firehose notice and REST detail, when outer envelopes are
   removed, then their item JSON bytes are equal.
5. Given a non-admin organization, device, or session principal, when it calls
   every D1 route, then it receives the same 404 as an unknown detail and no
   item serialization occurs.
6. Given known, unknown, empty, missing, repeated, device, and session-mismatch
   `asUser` cases, when the GET runs, then it has the stated AU2 result and
   exactly the existing dispatch principal semantics.
7. Given tied timestamps, deleted cursor boundaries, and pages larger than 50,
   when each collection pages in both directions, then every authorized item
   appears once in table order; `limit=501` yields 500; no cursor has a rowid,
   offset, or live lookup locator.
8. Given allowed and unlisted filters plus malformed, wrong-resource, and
   changed-filter cursors, when requests run, then listed filters restrict
   output, unlisted filters return 400, and each invalid cursor returns 400
   before row lookup.
9. Given invalid bearer, unknown detail, forbidden detail, and valid detail,
   when responses are compared, then they are respectively 401, identical 404,
   identical 404, and 200, and each includes the cache header.
10. Given the integrated registry, when the contract test reads its six rows,
    then each names this table's query, serializer, visibility, primary refs,
    and version source; a REST-local serializer or projection fails the test.

## Open Questions

None. Adding a users status or ownership filter requires a canonical REST
specification amendment, because the present public projection has no such field.

