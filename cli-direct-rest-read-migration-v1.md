# CLI direct-REST read migration v1 — D3 build specification

Status: DRAFT for independent review, 2026-08-25. This specification serves
work item `wi_113442f5-22ae-457b-a971-1b620069d490` and assignment
`asg_29aeed02-f3bc-421a-99ca-c2bce6f80ec0`.

Authority:

- `rest-state-api-v1.md`, canonical r3 at SHA-256
  `49b86ec874283c523001be7449b1e14aef47ca72932955445638ce6443aad754`
  (reviewed source commit `8b96e512688cc3c010c33c96d1ba622e543c7206`,
  canonical artifact `art_971f45b5`). Its C1, M4, M5, M8, AU1, AU2, A8,
  A8a, and A13a clauses control this build.
- `rest-vs-cli-adjudication.md` r2. Its three-plane ruling makes REST the
  read plane, dispatch the write plane, and the CLI terminal sugar.
- `cli-surface-v1.md`. It owns the retained public command families.
- `session-tokens-v1.md`. It owns current bearer discovery and dispatch
  principal selection. This specification changes only the transport of
  shared-state reads.
- Product-owner ruling message
  `s_f898378f-29cf-46b9-a5ad-b4e8681ef6c0`, 2026-08-25. It closes direct-read
  `--as` and `--as-process` behavior without a new REST identity parameter.
- Superseding product-owner route ruling for this assignment, 2026-08-25. The
  retained `toplines` and `topline` CLI names read current ExecutionMap
  telemetry through a separate `/api/execution-map` family. They do not read
  durable Toplines.
- Contract-closure work item
  `wi_835a72aa-c88b-421b-a34c-41d23032c7c7` owns exact session display-name
  filtering. Distinct contract-closure work item
  `wi_3874a61f-288b-4b54-ac8a-da9234a910a2`, author assignment
  `asg_2dbc772b-b800-4e47-91b7-59965560a2dd`, owns the ExecutionMap REST
  contract.

The fixed `rest-state-api-v1.md` baseline defines durable
`GET /api/toplines`, durable `GET /api/toplines/:id`, and
`GET /api/sessions/:sessionKey/messages`. It does not define an ExecutionMap
resource or a session name or `displayName` filter. Those missing clauses
remain unavailable to product code until both reviewed closure files above
amend canonical specs main. Current CLI behavior is not a contract substitute.

Source inventory baseline: Tightbeam product commit
`d00e06aea578d711e608637d38a97872487df15e`
(`d00e06a guidance: define product ownership by holder lineage`).
The implementation must repeat the inventory against the green D2 integration
tip before it edits product code. A later source change wins only when it has
live authority; source drift alone does not amend this specification.

Operating pattern taught by this specification: none. It defines product
behavior and does not amend agent guidance.

## Goal

Move each retained in-product CLI shared-state read from
`POST /agent/dispatch` to its canonical REST `GET`, while preserving the
existing bearer and the existing principal selected by `asUser`. After CLI,
Clawline, and ATC parity are accepted, remove each legacy dispatch-read path
and each M5 compatibility HTTP alias. Keep every dispatch write available.

## Non-Goals

- This build does not implement or migrate Clawline or ATC. It consumes their
  accepted M6 and M7 parity evidence only as removal gates.
- This build does not add a credential, principal binding, authorization
  grant, tailnet identity, REST mutation, query language, cache, retry policy,
  serializer, projection, or resource field.
- This build does not change a public CLI command name or remove a retained
  wrapper from `cli-surface-v1.md`.
- This build does not change D1 or D2 REST routes, filters, envelopes,
  visibility, errors, cache headers, cursor encoding, or item shapes.
- This build does not read, change, or remove durable Toplines or the
  `/api/toplines` family. The similarly named CLI commands retain their names
  and read ExecutionMap telemetry through `/api/execution-map`.
- This build does not change `doctor`, help, or another local-only read.
- This build does not remove or reroute a dispatch write.
- This build does not merge, deploy, or release product code.

## Terms

**Retained CLI read wrapper** — a public command in the first inventory table
whose result reads shared Tightbeam state. The command remains available after
its transport changes.

**Direct REST read** — an HTTP `GET` from the Rust CLI to the canonical D1 or
D2 route. It uses the endpoint and bearer returned by the existing discovery
chain. It does not send a dispatch body or call `/agent/dispatch`.

**Canonical read value** — an exact closed-world R7/R7a item or an exact
ExecutionMap view node frozen by
`wi_3874a61f-288b-4b54-ac8a-da9234a910a2`, emitted by its D1 or D2 public
serializer. A CLI formatter may place the value in a command-specific outer
object. It does not add, remove, rename, redact, or recompute a value field.

**Legacy dispatch-read path** — one read operation accepted by
`POST /agent/dispatch` at the source baseline. For mixed verbs such as
`config`, the term denotes only the read action.

**M5 compatibility alias** — one pre-v1 HTTP read route that temporarily
adapts a canonical query and serializer to its old outer response shape.

**Parity evidence** — a recorded test result that compares the old and new
transport from the same fixture state and resolved principal. Shape parity
means canonical item equality. Security parity means the same resolved
principal or refusal and the same allow, omission, deny, and same-404 result.
The product-owner `--as` and `--as-process` ruling is an intentional transport
change, so A5a replaces legacy-principal parity for those two modes.

**Removal commit** — the product commit that removes legacy dispatch-read
adapters and M5 aliases after the gates in D3-R10 pass. It is separate from
the commit that migrates CLI wrappers.

## Assumptions

AS1. The reviewed canonical closure from
`wi_835a72aa-c88b-421b-a34c-41d23032c7c7` will freeze the exact display-name
candidate filter. The reviewed canonical closure from
`wi_3874a61f-288b-4b54-ac8a-da9234a910a2` will freeze the separate
ExecutionMap route family and its selections. D2 will land each canonical GET
used in the wrapper inventory. D3 code does not start until the three
dependency gates in D3-R1 pass. A missing route, filter, or composed selection
falsifies this assumption and returns the gap to the REST product owner; D3
does not fill it locally. In particular, the fixed REST baseline's durable
Toplines clauses and sessions whitelist do not authorize an ExecutionMap
query or `displayName` query.

AS2. The existing CLI discovery chain returns one endpoint and bearer:
walk-up `.tightbeam-session`, then explicit environment, then provisioned
`gateway.json`. An integration test falsifies this if a migrated read selects
a different endpoint or token from a write in the same process context.

AS3. D1 and D2 REST envelopes expose the canonical page cursors that a CLI
caller must pass to `--before` or `--after`. A route test falsifies this if a
paginated response cannot drive the next request without the CLI minting or
decoding a cursor.

AS4. The accepted M6 and M7 lanes will record exact canonical integration
commits and parity verdicts. Legacy dispatch reads and M5 aliases remain when
either record is absent.

AS5. Product commit `d00e06a` already has no `critical` inspect read branch.
The historical inventory entry is therefore an absence assertion, not a
removal target. A source census falsifies this if D2 reintroduces that read.

## Invariants

I1. A retained shared-state CLI read performs REST I/O only. It has no runtime
fallback to dispatch, an M5 alias, SQLite, or a second local data source.

I2. The CLI uses the existing discovered bearer. When the existing command
selects a user principal through `asUser`, the CLI sends that same string once
as the GET `asUser` query value. The migration adds no identity input.

I3. The server resolves authorization before the canonical query and
serializer run. The CLI does not interpret identity, visibility, ownership,
or admin authority.

I4. A canonical REST route and its retained CLI wrapper use the same server
query and public serializer named by D1, D2, or the reviewed
`wi_3874a61f-288b-4b54-ac8a-da9234a910a2` closure. When the resource has a
firehose state class, its publisher uses that serializer too. D3 adds only HTTP
request construction and command-level outer formatting.

I5. A canonical read value reaches CLI stdout unchanged as a JSON value.
Command-level composition may select values, order already-authorized values,
join response envelopes, or render a tree. It cannot modify a canonical value.

I6. Dispatch remains the sole write plane. Removing a read arm from a mixed
verb preserves every write arm, authorization rule, event, rail, response,
and test for that verb.

I7. The CLI migration and legacy removal are separate rollback units. The
removal unit cannot land before M4, M6, and M7 parity evidence exists.

I8. An HTTP, decoding, schema-version, or canonical error ends the CLI call
with exit 1. The CLI does not retry through another transport or return stale
data.

I9. The existing one-retry rule for a DNS failure that proves no request
reached the gateway remains the only automatic retry. A response status,
response body, connection failure after connect, or timeout is not replayed.

## Architecture

### D3-R1 — code-start dependency

The implementer must branch from a green canonical Tightbeam main after specs
main contains the reviewed canonical closures from
`wi_835a72aa-c88b-421b-a34c-41d23032c7c7` and
`wi_3874a61f-288b-4b54-ac8a-da9234a910a2`, and product main contains the
reviewed-clean D2 integration for
`wi_ea98345b-51f4-4fae-b7df-3670c0d54f6b`. The dependency receipt must name:

1. the reviewed display-name closure path, SHA-256, and verdict;
2. the canonical specs-main commit that contains the display-name closure;
3. the reviewed ExecutionMap closure path, SHA-256, and verdict;
4. the canonical specs-main commit that contains the ExecutionMap closure;
5. the reviewed D2 build-spec path and SHA-256;
6. the reviewed-clean D2 code commit and verdict;
7. the canonical product-main commit that contains that code; and
8. the baseline and post-integration full-gate counts from that product tip.

D1 is a transitive prerequisite of D2. If any receipt is absent, D3 product
code remains untouched.

### D3-R2 — one read transport

The Rust CLI must represent gateway I/O as a closed sum type with separate
direct-read and dispatch variants. The direct-read variant has method `GET`, a
canonical path, and encoded query pairs; it cannot carry a dispatch verb or
JSON request body. The dispatch variant keeps method `POST`, its dispatch path,
and JSON body; it cannot name a canonical read route. The compiler therefore
rejects a migrated wrapper that tries to build a dispatch read.

The direct-read seam must:

- use the existing `Endpoint.base`, `Endpoint.token`, discovery order,
  `Authorization: Bearer` header, and `x-tightbeam-cli-version` header;
- percent-encode each path segment and query key/value as UTF-8 data;
- emit at most one `asUser` query key;
- accept only a canonical JSON list, detail, or reviewed composed-view
  envelope with `schemaVersion: 1` for JSON resources;
- pass `/download/:assetId` bytes only to a command that explicitly consumes
  that binary route; no current D3 wrapper does; and
- apply I9 without adding a read-specific retry.

The existing POST seam remains the path for dispatch writes.

Adding the direct-read variant wins the subtraction test: deleting retained
CLI wrappers would break named consumers, while accepting dispatch reads would
violate the canonical three-plane ruling.

### D3-R3 — retained wrapper inventory

This table is the complete in-product shared-state CLI read migration at the
source baseline. “Canonical route/query” means the exact route and query
vocabulary frozen by the two reviewed contract closures and the D2 build spec.
The ExecutionMap and `displayName` entries state the product-owner destination;
they are not current REST authority. A wrapper must not implement them before
their reviewed closures land, infer them from CLI source, or substitute an M5
alias.

| Public CLI form | Current dispatch read | Canonical direct GET composition | CLI-only composition |
|---|---|---|---|
| `list` | `inspect` | `GET /api/org`; page `GET /api/sessions` to exhaustion | Emit the exact `cli-list` object defined below. |
| `artifacts [--work-item ID] [--session KEY]` | `artifacts` | `GET /api/artifacts` with `workItemId` and `createdBySession` exact filters | None. |
| `decision-requests [--status S]` | `decision-requests` | `GET /api/decision-requests` with `status` | None. |
| `work-item-get ID` | `work-item-get` | `GET /api/work-items/:id` | None. |
| `work-item-trace ID` | `work-item-trace` | `GET /api/work-items/:id/trace` | None. |
| `transcript --session KEY [page flags]` | `transcript` retrieval | `GET /api/sessions/:sessionKey/messages` with `before`, `after`, and `limit` | None. |
| `transcript --name NAME` | `transcript` lookup | `GET /api/sessions?displayName=NAME` using the exact filter frozen by `wi_835a72aa-c88b-421b-a34c-41d23032c7c7`; call `GET /api/sessions/:sessionKey/messages` only after the caller selects a session | Return the candidate choice from canonical session items. Return no message content during lookup. |
| `toplines` | `toplines` flat roster | `GET /api/execution-map` with canonical `after` and `limit`; translate existing filters to `origin`, `ownerUserId`, `state`, `quietOverMs`, `specRefName`, dependent `specRefSha256`, and `sessionKey` | None. |
| `toplines --tree` | `toplines` tree | `GET /api/execution-map/tree` with the same roster filters and no page parameters | Render the returned forest without recomputing server telemetry. |
| `topline --under ID` | `topline` subtree | `GET /api/execution-map/subtrees/:workItemId` with the roster filters and no page parameters | Render the returned forest. |
| `topline --assignments IDS` | `topline` assignment selection | `GET /api/execution-map/assignments` with each ordered id as a repeated `assignmentId` and no roster or page parameters | Render the returned item selection and `noItem` ids. |
| `attests ASSIGNMENT [page flags]` | `attests` | `GET /api/assignments/:id/attests` with `after` and `limit` | None. |
| `assignments [--session KEY\|--role NAME] [--state S]` | `assignments` | `GET /api/assignments` with `holderKey`, `holderRole`, and `state` | None. |
| `coordination-share --session KEY --from MS --to MS` | `coordination-share` | `GET /api/sessions/:sessionKey/coordination-share?from=MS&to=MS` | None. |
| `digest-members WAKE` | `digest-members` | `GET /api/wakes/:wakeId/digest-members` | None. |
| `identity status [ARCHETYPE]` | `identity-status` | `GET /api/identity`; when an archetype is named, also `GET /api/archetypes/:name` | Join identity status with that archetype's canonical compiled guidance without changing either item. |
| `kungfu list` | `kungfu-list` | Page `GET /api/kungfu` | None. |
| `config get KEY` | `config`, action `get` | `GET /api/config/:key` | None. |
| `host-env-list [--host H] [--harness X]` | `host-env-list` | `GET /api/host-env` with `host` and `harness` | None. |
| `harness-process list` | `harness-processes` | Page `GET /api/harness-processes` | None. |

For a D3-R3 row whose CLI-only composition is `None`, stdout is the canonical
REST envelope pretty printed as JSON. The `list` wrapper emits exactly
`{"schemaVersion":1,"resource":"cli-list","org":<org item>,"sessions":[<session items>]}`
after it exhausts authorized session pages in canonical order. The
`identity status ARCHETYPE` wrapper emits exactly
`{"schemaVersion":1,"resource":"cli-identity-status","identity":<identity envelope>,"archetype":<archetype item>}`.
Their nested resource values remain JSON-value-equivalent to the decoded
canonical values. Each wrapper that accepts page flags exposes the canonical
`page` object. Its `--before` and `--after` inputs accept only the opaque cursor
returned by that object. The CLI does not decode or mint a cursor.

The two reviewed closure work items and the D2 build spec must freeze each
route and selection named in the table before D3 code starts. If their reviewed
text does not expose one, the affected wrapper is BLOCKED and the REST product
owner amends the canonical read contract first. Current CLI query names are
evidence, not authority to invent a REST parameter.

### D3-R4 — principal transport

For `Identity::User(user_id)`, the GET seam must append exactly one
`asUser=user_id` query value after standard percent encoding. For
`Identity::Session`, it must append no identity query. For
`Identity::Role(_role)`, it must append no identity query. The `--as` value is
non-transported CLI compatibility syntax on direct reads: a session bearer
remains the session principal. With an org bearer, the request carries no
`asUser`, so AU2 returns its existing identity-required `400 invalid_message`.
The CLI does not validate, resolve, or transmit the role value.

For `Identity::Process(_name)`, the CLI must refuse locally before HTTP with
`invalid_read_identity: --as-process is not supported on direct reads`. The
CLI must print that line to stderr, print no stdout, and exit 1. The caller must
use a user or session principal for a shared-state read.

The CLI must not send `as`, `asProcess`, an owner id inferred from a session
file, a role binding, a device id, or a tailnet header on a REST read. It must
not preflight whether `asUser` exists. An org bearer with known, unknown,
empty, or missing `asUser`; a session bearer with absent, matching-owner, or
mismatched-owner `asUser`; and a device bearer with `asUser` must receive the
AU2 result without client reinterpretation. These rules carry the product-owner
ruling delivered on 2026-08-25 for `asg_29aeed02`.

### D3-R5 — response and error behavior

The CLI must parse the canonical REST error envelope with the existing
terminal rule: print `code: message` when a nonempty message exists, otherwise
print `code`, to stderr and exit 1. It must print a successful JSON result to
stdout and exit 0.

The CLI must return `invalid_response` and exit 1 when a successful JSON route
returns malformed JSON, a missing or non-integer `schemaVersion`, a
`schemaVersion` other than 1, a list envelope without `items` and `page`, or a
detail envelope without `item`. A composed-view envelope must contain each
closed key frozen by its reviewed source specification. The CLI must not print
a partial result.

The command parser keeps its current mutual-exclusion, required-value, numeric,
and positive-limit checks. Server-owned invalid filter, invalid cursor,
authorization, same-404, and AU2 errors pass through unchanged.

### D3-R6 — formatter boundary

One formatter registry must contain exactly the D3-R3 rows whose CLI-only
composition column is not `None`: `list`, transcript name lookup, the three
ExecutionMap command forms, and `identity status ARCHETYPE`. A formatter
receives authorized canonical values. It cannot call the database, query
another source, infer authorization, or serialize a resource value from a
storage row.

The `list` formatter must not restore the current dispatch `inspect` query or
add wakes, digest carriers, roles, or pending devices to the canonical
org-plus-sessions composition.
The `transcript --name` formatter may perform only the candidate selection
frozen by `wi_835a72aa-c88b-421b-a34c-41d23032c7c7`; it does not scan sessions
or transcripts to recreate a missing server filter. The `toplines` and
`topline` formatters may arrange a canonical ExecutionMap view but must not
reproduce the server's telemetry computation or read the durable
`/api/toplines` resource.

### D3-R7 — compatibility during M4

The CLI migration commit changes the retained wrappers to direct GETs and
keeps the legacy dispatch reads and M5 aliases present. Tests may invoke the
legacy reads only through an explicit parity harness. Production CLI code has
no dispatch-read branch after this commit.

The build must not add a feature flag, environment switch, automatic fallback,
or transport negotiation. An older CLI can continue to use dispatch during
the migration window. A migrated CLI uses REST and fails loudly when the REST
contract is unavailable.

### D3-R8 — legacy dispatch-read inventory

The source census must classify each operation before the removal commit.
These 23 read operations are present at baseline:

| Class | Legacy dispatch-read operations |
|---|---|
| Retained-wrapper adapters | `inspect`; `artifacts`; `decision-requests`; `work-item-get`; `work-item-trace`; `transcript`; `toplines`; `topline`; `attests`; `assignments`; `coordination-share`; `digest-members`; `identity-status`; `kungfu-list`; `config` action `get`; `host-env-list`; `harness-processes` |
| No public CLI wrapper | `facts-read`; `artifact-get`; `assignment-get`; `work-item-list`; `decision-request`; `role-list` |

The canonical recon also names historical `critical` action `inspect`. Product
commit `d00e06a` has only the state-changing critical declaration path. The
removal suite must assert that an inspect action is absent while preserving
the declaration write.

For a read-only verb, removal deletes its router allowlist entry and dispatch
adapter. For `config`, removal deletes only action `get`; action `set` and its
authorization remain. Removal must not delete a canonical query or serializer
that D1, D2, or firehose uses.

### D3-R9 — M5 compatibility alias inventory

The removal commit must remove these seven route declarations and their outer
compatibility adapters:

- `GET /api/streams`
- `GET /api/org-options`
- `GET /api/trackable-sessions`
- `GET /api/session-status`
- `GET /api/work`
- `GET /api/work/:id`
- `GET /harnesses`

It must preserve `GET /version`, canonical `/api/...` reads,
`GET /download/:assetId`, WebSocket upgrades, upload, session-control writes,
stream writes, and `/agent/dispatch` writes.

### D3-R10 — M8 removal gates

M8 is the removal commit. It may start only after one durable gate receipt
names all of:

1. M4: the reviewed-clean CLI migration commit, its canonical integration
   commit, and passing D3-R11 parity evidence for every D3-R3 row;
2. M6: the reviewed-clean Clawline migration commit, its canonical integration
   commit, and accepted proof that Clawline uses no M5 alias;
3. M7: the reviewed-clean ATC migration commit, its canonical integration
   commit, and accepted proof that ATC reads no Tightbeam SQLite state; and
4. a source census at the removal base that finds no in-product caller of a
   legacy dispatch read or M5 alias outside the explicit parity tests being
   deleted with the removal.

The product owner for `rest-state-api-v1.md` accepts the receipt. The check and
removal are one integration step: the removal branch is cut from the exact
green main named by the receipt, and main cannot advance before that branch is
integrated or the receipt is repeated against the new tip.

### D3-R11 — parity matrix

The parity harness must seed one real database fixture through product write
seams, start the real HTTP router, and run the built Rust CLI. It must capture
the legacy dispatch response before removal and the canonical REST response
from the same state. Handwritten ideal responses do not satisfy parity.

For each D3-R3 row, the harness must cover:

- a successful nonempty result;
- an empty authorized result where the route admits one;
- each CLI filter or selection;
- a forbidden or invisible row;
- an unknown detail id where the route admits one;
- pagination with a cursor returned by the preceding page; and
- exact canonical item equality between the CLI result and REST after removing
  only their documented outer envelopes.

The AU2 security table must cover the cases in canonical A8a. It must assert
the same resolved principal or refusal and the same allow, omission, deny, and
same-404 result between dispatch and GET. Separate raw GET cases must prove
that repeated `asUser` returns `400 invalid_as_user`, malformed percent
encoding returns `400 malformed_query`, and a device bearer plus `asUser`
returns `400 invalid_as_user`, each before principal resolution.

The parity harness must not apply legacy role-principal expectations to
`--as` or `--as-process`. A5a is the complete acceptance for those modes.

### D3-R12 — rollback boundaries

The CLI migration commit is reversible while the legacy dispatch reads and M5
aliases remain. Its rollback reverts the migrated wrappers as one unit and
does not revert D1 or D2.

After the removal commit lands, rollback runs in reverse dependency order:
first restore the exact removal commit, then roll back a client migration only
if the restored transport has passed its parity smoke. Production code never
falls back per request. A partial restoration that reopens an alias without
its authorization, query, serializer, and parity tests is forbidden.

### D3-R13 — implementation touchpoints and traceability

Likely product touchpoints, verified at baseline:

- `cli/src/dispatch.rs`: request type, GET construction, send/parse seam,
  command routing, and unit tests;
- `cli/src/args.rs`: cursor/help wording only when canonical cursors change the
  accepted input description;
- `test/cli_integration_test.exs`: real built-CLI plus router parity;
- `lib/tightbeam/wire/router.ex`: M5 routes, dispatch allowlist, bearer/AU2
  adapter, and routing tests;
- `lib/tightbeam/gateway.ex`: legacy handler registration and mixed `config`
  read/write split;
- the ExecutionMap query and serializer modules frozen by
  `wi_3874a61f-288b-4b54-ac8a-da9234a910a2`: D3 reuses them and does not add a
  second telemetry projection;
- `test/router_test.exs`, `test/gateway_test.exs`, and resource-focused tests:
  removal absence and write-preservation proofs.

The implementer must recensus touchpoints at the D2 integration tip. A changed
filename does not authorize a second seam.

| Requirement | Acceptance | Primary touchpoint |
|---|---|---|
| D3-R1 | A1 | build evidence only |
| D3-R2, D3-R5 | A2, A6 | `cli/src/dispatch.rs` |
| D3-R3, D3-R6 | A3, A4 | CLI routing and integration tests |
| D3-R4 | A5 | CLI GET builder and router AU2 tests |
| D3-R7 | A7 | CLI integration tests |
| D3-R8, D3-R9 | A8, A9 | router and gateway registrations |
| D3-R10 | A10 | gate receipt and source census |
| D3-R11 | A3-A6 | captured parity fixtures |
| D3-R12 | A11 | ordered revert smoke |

## Acceptance

A1. **Given** the two contract-closure work items, the D2 work item, specs main,
and canonical Tightbeam main, **when** a coder attempts to start D3, **then**
the eight D3-R1 receipts name exact amendment, spec, review, integration, and
gate evidence; deleting one receipt keeps product bytes unchanged.

A2. **Given** the same session workdir and explicit environment/provisioned
fallback fixtures, **when** one migrated read and one dispatch write discover
their endpoint, **then** both select the same base URL and bearer, both send
the CLI version header, the read uses GET, and the write uses
`POST /agent/dispatch`.

A3. **Given** a real seeded router fixture, **when** the built CLI runs each
D3-R3 form, **then** the capture shows only its canonical GET composition,
zero dispatch-read requests, zero M5 alias requests, and the documented
command-level JSON.

A4. **Given** a canonical R7/R7a item or ExecutionMap node containing each
closed key and realistic nested content, **when** a simple or composed wrapper
prints it, **then** parsing CLI stdout yields a value equal to the route value.
Removing, renaming, adding, or redacting one closed key fails the test.

A5. **Given** the full canonical A8a credential and `asUser` matrix, **when**
the harness compares legacy dispatch with direct GET, **then** each case has
the same resolved principal or refusal and the same authorized result. A raw
request with repeated `asUser`, malformed encoding, or device bearer plus
`asUser` returns the exact AU2 error before a query runs.

A5a. **Given** a session bearer, an org bearer, and a read invoked with
`--as held-role`, `--as unknown-role`, or `--as-process cron`, **when** the
built CLI runs, **then** both `--as` values send no identity query and use the
session principal with the session bearer, either `--as` value receives AU2's
identity-required refusal with the org bearer, and `--as-process` sends no HTTP
request and returns the exact local `invalid_read_identity` error.

A6. **Given** malformed JSON, wrong schema versions, incomplete envelopes,
400, 401, 403, 404, 426, timeout, DNS failure, and post-connect failure
responses, **when** a migrated wrapper runs, **then** only the first DNS
failure retries once; each other case exits 1, prints the canonical terminal
error, prints no partial stdout, and sends no dispatch or alias request.

A7. **Given** the CLI migration commit before removal, **when** source and
traffic are inspected, **then** production wrappers contain no dispatch-read
branch while every D3-R8 adapter and D3-R9 alias remains available to older
clients and parity tests.

A8. **Given** the accepted D3-R10 receipt, **when** the removal commit runs the
dispatch census, **then** each of the 23 baseline read operations is refused at
the router or mixed-verb read selector, `critical inspect` remains absent, and
the corresponding canonical GET returns its contract response.

A9. **Given** the removal commit, **when** each D3-R9 route is requested with a
valid bearer, **then** it returns canonical `404 not_found`; `GET /version`,
canonical reads, download, WebSocket, upload, session-control writes, stream
writes, and a representative request from each dispatch write family still
passes its existing contract test.

A10. **Given** one missing, stale, or non-reviewed M4, M6, or M7 receipt,
**when** removal is proposed, **then** the removal test refuses before editing
a route registration. **Given** all receipts against the exact green base,
**when** main advances first, **then** the receipt is stale and must be repeated.

A11. **Given** the two commits from D3-R12, **when** a release fixture first
reverts the removal commit and then reverts the CLI migration commit, **then**
the legacy parity smoke passes between the reverts. Reverting in the opposite
order fails the rollback-order test before a product release step.

A12. **Given** the CLI-migration branch or the later removal branch, **when**
the documented product gates run from a green baseline and again after that
branch's change, **then**
`mix format --check-formatted`, `scripts/verify_mix.sh`, `cargo fmt --check`,
and `cargo test` pass with recorded baseline and after counts. The implementer
also runs the built CLI against the real in-process router fixture; compile and
unit-test success alone do not satisfy this acceptance.

## Open Questions

Open Questions: none. The REST product owner ruled the direct-read `--as` and
`--as-process` behavior on 2026-08-25. The display-name query vocabulary is
owned by `wi_835a72aa-c88b-421b-a34c-41d23032c7c7`; the separate ExecutionMap
family is owned by `wi_3874a61f-288b-4b54-ac8a-da9234a910a2` under
`asg_2dbc772b-b800-4e47-91b7-59965560a2dd`. Both are D3-R1 code-start
dependencies rather than inventions in this specification. Durable
`/api/toplines` semantics remain outside D3.
