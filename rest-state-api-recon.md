# Tightbeam REST state API recon

Status: revised recommendation, 2026-08-20. This revision adds the binding
decision rule and complete read disposition required by Mike. Recon card
`asg_9a1b4764-d714-4099-aff1-840b489e544c` on
`wi_9239a7f1-3263-403f-bb26-2ea7568fb277`.

## Verdict

**Conditional — make REST the canonical read plane. Keep the CLI as sugar over
the same typed reads. Keep all state changes in dispatch verbs.**

Confidence: **high** in the plane split and resource model. Confidence is
**medium-high** in the exact route names. The route names can change without
changing the doctrine.

The recommendation has six conditions:

1. One canonical public projection must define each resource. REST responses
   and WebSocket notice payloads must use that same projection.
2. Storage-only secrets must never enter a public projection. “Full row” must
   mean the full public resource, not every database column.
3. Every notice class must name its resource, operation, and exact primary key.
   Delete notices must carry an explicit tombstone.
4. REST and WebSocket authorization must use the same row-visibility rule.
5. Every pageable collection must use exact keyset pagination. It must not use
   offset pagination or a mutable sort field.
6. CLI reads must call the same read service as REST. They must not keep a
   second SQL implementation.

These conditions make the state model rebuildable after any missed notice.
They also keep the CLI small.

## Binding decision rule

Any read of shared Tightbeam state **MUST** have a canonical REST endpoint,
whether it returns stored resources or a canonical derived view; any CLI
command that exposes that read **MUST** call the REST endpoint and may only
select, compose, summarize, or format its response for terminal use. A read
stays CLI-only only when all its inputs are local to the caller and its output
is help or diagnostics; every state change stays a dispatch verb.

## Decision question

The decidable question was:

> Which Tightbeam reads belong in the formal client API, which deserve CLI
> convenience wrappers, and what exact contract lets a client build state and
> correlate it with the firehose?

This question matches the card. The card asks for the split, the schema-backed
resource inventory, pagination, filters, authorization, and notice
correlation. It does not ask for implementation.

## Authority and evidence baseline

The recommendation uses these snapshots:

- Event firehose r4.2 at
  `gibson:/home/mike/src/tightbeam-specs/event-firehose-v1.md`, specs commit
  `834b0154bf3a4b3eea0e4fd59fef9ecea337bcb4`. P1 makes state rows the truth.
  P2 makes the socket a change doorbell. P5 rejects direct SQL as a product
  interface and sends flexible model reads toward REST. See lines 54-82.
- The firehose requires payload IDs to match query IDs. See the same file,
  V5 at lines 181-183. Its model recipe requires subscribe first, then read a
  snapshot, then apply buffered notices idempotently. See lines 262-277.
- Observability r4 says both assignments and work items are random-access
  model entities. It leaves card grain and summarization to the view. See
  `gibson:/home/mike/src/tightbeam-specs/observability-v1.md`, specs commit
  `834b0154bf3a4b3eea0e4fd59fef9ecea337bcb4`, lines 70-103.
- Observability already defines four device-authenticated GETs for work state.
  See the same file, lines 595-725.
- The current source baseline is Tightbeam `origin/main` commit
  `644c04064594328b5ec1c1b76301a1ac893bffc2` in
  `gibson:/home/mike/src/tightbeam`.
- During this recon, the specs checkout advanced to commit
  `f25b08ea1439f461d056b66470cbaaba0d4dfe4e`. That commit added
  `rest-vs-cli-adjudication.md` draft r1. Its ruling is “REST is the read
  plane; verbs are the write plane; the CLI is sugar.” This report accepts
  that ruling and reconciles two inventory errors in the draft.

## Competing shapes and disconfirmation

### 1. Expand the CLI until every client need has a flag

Rejected.

The public CLI already has many useful read commands. Its command enum includes
`list`, `artifacts`, `decision-requests`, `work-item-get`,
`work-item-trace`, `transcript`, `toplines`, `topline`, `attests`,
`assignments`, identity and host reads, and other diagnostics. See
`cli/src/args.rs` at the source baseline, lines 67-370.

That surface is good for common agent tasks. It is a poor model API. A client
would need process spawning, JSON parsing, many round trips, and an expanding
flag language for joins and filters. This is the SQL-shaped CLI that P5 rejects.

### 2. Bless read-only access to `state.db`

Rejected.

P5 explicitly says direct SQL is not a product interface. The code confirms why.
The schema is owned by many modules, contains internal enforcement tables, and
uses raw columns that are unsafe on a client wire. `Schema.ensure_all/1` loads
more than twenty schema owners. See `lib/tightbeam/schema.ex:7-33` at the source
baseline.

ATC currently demonstrates both the demand and the coupling problem. Its live
snapshot generator opens `state.db` with `mode=ro` and runs SQL across
`sessions`, `turns`, `assignments`, `attests`, `work_items`, `wakes`, `roles`,
and `messages`. See `gibson:/home/mike/.local/bin/tb-weather-gen:3-28`,
`:121-232`, and `:316-364`. This works today, but it binds ATC to storage DDL.
The formal API should replace that dependency.

### 3. Mirror every SQLite table as a REST resource

Rejected.

The database contains product rows, derived observability rows, audit logs,
scheduler state, idempotency rows, schema stamps, leases, liveness enforcement,
and credential-bearing rows. A table mirror would make implementation details
part of the product contract. It would also expose secrets.

For example, `sessions` stores `cliToken`; `devices` stores `token`; and
`harness_processes` stores `identityToken`. See `lib/tightbeam/org.ex:62-89`,
`lib/tightbeam/devices.ex:39-54`, and
`lib/tightbeam/harness_process.ex:18-42` at the source baseline.

The current wire already uses a safer public projection. `stream_session/1`
selects client fields and does not serialize `cliToken`. See
`lib/tightbeam/wire/payloads.ex:174-196`.

### 4. Typed public resources, with CLI wrappers over the same read service

Accepted.

This shape gives clients flexible bulk reads without exporting SQL. It preserves
common CLI workflows. It also gives the firehose one canonical row shape and
one exact ID for correlation.

## Current read surface

### Disposition labels

Every read below has exactly one disposition:

- `keep-CLI`: Keep the read only in the CLI. It reads no shared Tightbeam
  state and needs no REST route.
- `move-REST`: REST is the only final public home. Keep or rename an existing
  HTTP route, and remove any dispatch-read alias after migration.
- `exists-in-both`: A current CLI read and HTTP read already overlap. Keep the
  CLI as a wrapper over the canonical REST route.
- `new-REST`: No canonical REST route exists. Add the named route. Keep a
  current public CLI command only as a wrapper over that route.

These labels state the migration action and the final owner. They are not
degrees of preference. Retire every dispatch-only read after its canonical
REST route ships.

### Complete public CLI read disposition

This table covers all 20 public CLI commands or command forms that only read.
`attend` is not a read: it elects attention for the caller's running turn, so
it stays a dispatch write. See `cli/src/dispatch.rs:518-526` and
`lib/tightbeam/gateway.ex:5851-5871`.

| Existing CLI read | Current source | Disposition | Canonical REST target | One-clause reason |
|---|---|---|---|---|
| `help` | compiled local help | `keep-CLI` | none | It reads no shared state. |
| `<command> --help` / `help <command>` | compiled local help | `keep-CLI` | none | It reads no shared state. |
| `doctor` | local process, file, and connectivity probes | `keep-CLI` | none | Its result diagnoses the caller's machine. |
| `list` | dispatch `inspect` | `new-REST` | `GET /api/org` plus `GET /api/sessions` | Clients need the same org and session model. |
| `artifacts` | dispatch `artifacts` | `new-REST` | `GET /api/artifacts` | Artifact metadata is shared model state. |
| `decision-requests` | dispatch `decision-requests` | `new-REST` | `GET /api/decision-requests` | Decision requests are shared model state. |
| `work-item-get` | dispatch `work-item-get` | `exists-in-both` | `GET /api/work-items/:id` | The current HTTP detail route already overlaps it. |
| `work-item-trace` | dispatch `work-item-trace` | `new-REST` | `GET /api/work-items/:id/trace` | Trace order and membership are canonical semantics. |
| `transcript` | dispatch `transcript` | `new-REST` | `GET /api/sessions/:sessionKey/messages` | Clients must page conversation state. |
| `toplines` | dispatch `toplines` | `new-REST` | `GET /api/toplines` | Mechanical roster status is a shared derived view. |
| `topline` | dispatch `topline` | `new-REST` | `GET /api/toplines/:selection` | One roster subtree is a shared derived view. |
| `attests` | dispatch `attests` | `new-REST` | `GET /api/attests` and `GET /api/assignments/:id/attests` | Clients need bulk and assignment-scoped evidence. |
| `assignments` | dispatch `assignments` | `exists-in-both` | `GET /api/assignments` | Current `GET /api/work` already returns assignment state. |
| `coordination-share` | dispatch `coordination-share` | `new-REST` | `GET /api/sessions/:key/coordination-share` | The count is a shared derived read. |
| `digest-members` | dispatch `digest-members` | `new-REST` | `GET /api/wakes/:wakeId/digest-members` | Digest membership is shared audit state. |
| `identity status` | dispatch `identity-status` | `new-REST` | `GET /api/identity` | Published identity status is org state. |
| `kungfu list` | dispatch `kungfu-list` | `new-REST` | `GET /api/kungfu` | Installed bundle state is shared catalog state. |
| `config get` | dispatch `config`, action `get` | `new-REST` | `GET /api/config/:key` | Safe configuration values are shared admin state. |
| `host-env-list` | dispatch `host-env-list` | `new-REST` | `GET /api/host-env` | Host environment metadata is shared admin state. |
| `harness-process list` | dispatch `harness-processes` | `new-REST` | `GET /api/harness-processes` | Process records are shared operational state. |

The command variants are in `cli/src/args.rs:67-370`. The command-to-verb
mapping is in `cli/src/dispatch.rs:199-210`, `:319`, `:418-423`, `:500-574`,
`:678-735`, and `:764-910` at the source baseline.

### Dispatch reads without public CLI commands

The gateway accepts seven additional read forms. This table closes the gap
between the public CLI command enum and the gateway's allowed verb set.

| Existing dispatch read | Disposition | Canonical REST target | One-clause reason |
|---|---|---|---|
| `facts-read` | `new-REST` | `GET /api/facts` | Facts are shared coordination state. |
| `artifact-get` | `new-REST` | `GET /api/artifacts/:artifactId` | Artifact detail is shared model state. |
| `assignment-get` | `move-REST` | `GET /api/assignments/:id` | The current HTTP detail route already owns the read. |
| `work-item-list` | `move-REST` | `GET /api/work-items` | The current HTTP collection already owns the read. |
| `decision-request` | `new-REST` | `GET /api/decision-requests/:id` | Decision detail is shared model state. |
| `role-list` | `new-REST` | `GET /api/roles` | The role registry is shared org state. |
| `critical`, action `inspect` | `new-REST` | `GET /api/critical-state` | Critical-state inspection is shared enforcement state. |

The allowed verb table is at `lib/tightbeam/wire/router.ex:55-58`.

Two corrections are required in `rest-vs-cli-adjudication.md` draft r1:

- `coordination-share` is a pure count over rows. Its source comment says it
  “files nothing, rules nothing.” See `lib/tightbeam/gateway.ex:5701-5729`.
- `digest-members` is a pure owner-or-admin audit read. See
  `lib/tightbeam/gateway.ex:5766-5789` and
  `lib/tightbeam/wire/router.ex:594-598`.

Both belong in REST with CLI wrappers. They do not belong in the write-plane
list.

### Existing HTTP routes

The current router has 11 HTTP reads. This table classifies each one.

| Existing HTTP read | Disposition | Canonical target | One-clause reason |
|---|---|---|---|
| `GET /version` | `move-REST` | keep `GET /version` | Build and health metadata are machine-readable and need no CLI state command. |
| `GET /harnesses` | `move-REST` | `GET /api/catalog/harnesses`; keep the old route as an alias | Harness capabilities are a REST catalog. |
| `GET /api/streams` | `exists-in-both` | `GET /api/sessions` | The CLI `list` command needs the same session collection. |
| `GET /api/org-options` | `exists-in-both` | `GET /api/org` and catalog routes | The CLI `list` command needs the same org catalogs. |
| `GET /api/trackable-sessions` | `move-REST` | retire it in favor of `GET /api/sessions` | A static empty probe is not a state contract. |
| `GET /api/session-status` | `exists-in-both` | `GET /api/sessions/:sessionKey` | The CLI and clients need the same session status. |
| `GET /api/work` | `exists-in-both` | `GET /api/assignments` | The CLI `assignments` command needs the same collection. |
| `GET /api/work/:id` | `move-REST` | `GET /api/assignments/:id` | Assignment detail has no public CLI command. |
| `GET /api/work-items` | `move-REST` | keep `GET /api/work-items` | Generic work-item collection state has no public CLI command. |
| `GET /api/work-items/:id` | `exists-in-both` | keep `GET /api/work-items/:id` | The CLI `work-item-get` command needs the same detail. |
| `GET /download/:asset_id` | `move-REST` | keep `GET /download/:asset_id` as a binary adjunct | Asset bytes are HTTP content, not terminal composition. |

The router also has two WebSocket upgrade routes and seven non-read routes.
`GET /` and `GET /ws` are transports, not reads. `POST /agent/dispatch`,
`POST /agent/tool-call-observed`, `POST /api/streams`,
`PATCH /api/streams/:key`, `DELETE /api/streams/:key`,
`POST /api/session-control`, and `POST /upload` are mutations or hooks, not
reads. This accounts for all 20 route declarations in the current router.

The router states the core rule already: handlers dispatch writes, while reads
query directly. See `lib/tightbeam/wire/router.ex:9-20`. The route definitions
are at `:93-389`. Device routes use Bearer tokens at `:443-453`.

### Binding rulings for the five boundary cases

| Boundary case | Binding disposition | Exact ruling |
|---|---|---|
| `transcript` | `new-REST` | Add paged `GET /api/sessions/:sessionKey/messages`; keep `tightbeam transcript` only as a formatter over that endpoint. |
| `toplines` and `topline` | `new-REST` | Add paged `GET /api/toplines` and `GET /api/toplines/:selection`; compute canonical mechanical status on the server, while the CLI may select, render a tree, or summarize. |
| `attests` | `new-REST` | Add both bulk `GET /api/attests` and nested `GET /api/assignments/:id/attests`; one nested CLI-shaped route cannot serve model refresh. |
| `work-item-trace` | `new-REST` | Add `GET /api/work-items/:id/trace`; trace membership and order are canonical server semantics, not CLI composition. |
| `list` | `new-REST` | Split it into small `GET /api/org` and paged `GET /api/sessions`; the CLI composes those resources into its human roster. |

These rulings are final. A builder does not choose between a REST resource and
a CLI-only implementation for any of these reads.

### Current clients

Clawline currently fetches three Tightbeam read routes:

- `/api/streams`
- `/api/trackable-sessions`
- `/api/session-status?sessionKey=...`

See `/Users/mike/src/clawline/src/protocol/stream-api.ts:168-207` at Clawline
commit `d4af47ff6b2ca76f2cfaad49e0aa8ae5c327238a`.

Clawline does not currently fetch paged transcript or work state through REST.
It relies on the chat socket for conversation delivery. The formal transcript
GET is therefore new client capability, not a rename of a route Clawline
already calls.

ATC currently builds a larger model directly from SQLite. It needs sessions,
roles, work items, assignments, attests, turns, wakes, and recent messages. It
also joins these rows and filters them by state and time. The SQL references are
at `gibson:/home/mike/.local/bin/tb-weather-gen:121-232` and `:316-364`.

This is strong demand evidence for bulk typed resources. It is not authority to
copy ATC's stage or layout judgments into Tightbeam. Observability keeps card
grain and summarization in the view.

## Schema inventory and API boundary

The current schema divides into three groups.

### Core client state

- Org: `sessions`, `roles`, `users`, `devices`.
- Work: `work_items`, `assignments`, `assignment_files`,
  `assignment_effects`, `assignment_reopenings`, `attests`.
- Coordination: `wakes`, `decision_requests`, `condition_facts`.
- Conversation and execution: `messages`, `turns`, `read_states`.
- Deliberate records: `artifacts`, `assets`.

Key DDL sources are:

- `lib/tightbeam/org.ex:62-106`
- `lib/tightbeam/roles.ex:29-37`
- `lib/tightbeam/devices.ex:39-55`
- `lib/tightbeam/work_items.ex:34-55`
- `lib/tightbeam/assignments.ex:35-160`
- `lib/tightbeam/wakes.ex:68-135`
- `lib/tightbeam/escalation.ex:34-177`
- `lib/tightbeam/ledger.ex:39-76`
- `lib/tightbeam/projection.ex:54-81`
- `lib/tightbeam/artifacts.ex:31-64`

### Derived or composed reads

- `WorkState` derives assignment status from assignments, attests, and sessions.
  It does not use its doorbell log as truth. See
  `lib/tightbeam/work_state.ex:33-68`.
- Work-item detail composes work items with assignments.
- Transcript composes messages with turn and wake attribution. See
  `lib/tightbeam/transcript.ex:184-248`.
- Toplines, work-item trace, coordination share, and digest membership are
  composed reads. They remain typed resources even though no single table owns
  their complete result.

### Operational and enforcement internals

Examples include `events`, `lifecycle_events`, `boot_epochs`,
`causal_events`, `wire_idempotency`, scheduler state, supervision liveness
tables, recurrence suppression, leases, schema stamps, harness pointers, and
park fences.

These tables must not become raw core resources. An operator API can expose
selected safe projections under explicit admin routes. It must not expose
storage layout by default.

## Recommended doctrine

1. REST owns every typed read of shared Tightbeam state.
2. Dispatch verbs own every state change.
3. Every retained public CLI state read wraps REST and may add terminal-only
   selection, composition, summarization, or formatting.
4. A shared-state read can remain REST-only. It cannot remain CLI-only.
5. Local help and diagnostics can remain CLI-only because they do not read
   shared state.
6. REST offers whitelist filters. It never accepts SQL, arbitrary field names,
   caller-selected joins, or caller-selected sort expressions.
7. Derived views are valid REST resources when their derivation is mechanical
   and already owned by Tightbeam. Product judgments remain client-side.

The enforcement rung should be code structure. Each resource must have one
query function and one public serializer. The REST adapter, CLI adapter, and
notice publisher call those seams. Review prose alone is too weak.

## Formal REST contract

### Namespace and versions

Use the adjudicated `/api/<resource>` names for v1. Every JSON response carries
`"schemaVersion": 1`. The gateway's existing `/version` response remains the
protocol preflight.

Existing unversioned routes remain compatibility aliases until their clients
migrate. A future incompatible API should use a new versioned namespace. Do not
silently change a v1 field's meaning.

### Authentication and principals

Use `Authorization: Bearer <existing gateway credential>`.

- A device token resolves to its user principal.
- A session CLI token resolves to its session principal and owner.
- The org CLI token does not name a principal by itself. The current CLI read
  adapter can continue through `/agent/dispatch` until a separate, reviewed GET
  identity carrier exists.

Do not invent an unreviewed `asUser` query parameter. Query strings are poor
identity carriers and are often logged.

The canonical read service must accept a resolved principal. Device REST and
the temporary CLI dispatch adapter call it with that principal. This gives one
read implementation now without weakening auth. A later CLI-to-GET migration
can change only the transport.

### Visibility

- Collection reads omit rows the principal cannot read.
- Detail reads return the same 404 for an unknown row and a forbidden row.
- Owner-scoped rows use owner-or-admin visibility unless a live spec names a
  stricter rule.
- Admin-only resources refuse non-admin callers.
- REST and WebSocket subscription filtering use the same visibility function.

The current transcript already collapses unknown and forbidden sessions into
one `not_found` result. See `lib/tightbeam/transcript.ex:96-110`. Current work
detail routes do the same. See `lib/tightbeam/wire/router.ex:301-338`.

### Canonical list envelope

```json
{
  "schemaVersion": 1,
  "resource": "assignments",
  "items": [],
  "page": {
    "oldestId": null,
    "newestId": null,
    "hasMoreBefore": false,
    "hasMoreAfter": false
  }
}
```

The detail envelope is:

```json
{
  "schemaVersion": 1,
  "resource": "assignments",
  "item": {}
}
```

The item inside either envelope has the exact shape used in a change notice's
`payload`.

### Pagination

Every pageable collection accepts `before`, `after`, and `limit`.

1. `before` and `after` are mutually exclusive.
2. Both cursors are exclusive.
3. A request without a cursor returns the newest page.
4. Items in a page are ordered oldest to newest. A client prepends a `before`
   page and appends an `after` page.
5. The default limit is 50. The maximum is 500. A larger value is clamped.
6. The cursor is the resource's public primary ID. The server resolves that ID
   to its immutable ordering tuple.
7. An unknown or forbidden cursor returns `400 cursor_not_found`.
8. The caller must keep filters fixed while it follows one page chain.
9. Offset pagination is forbidden.

This follows the transcript precedent. Transcript uses `messages.seq` for
ordering, exposes message IDs as cursors, makes before and after exclusive, and
uses default 50 with cap 500. See `lib/tightbeam/transcript.ex:20-35`, `:73-92`,
and `:113-181`.

Each resource uses an immutable order:

| Resource | Stable order |
|---|---|
| sessions | `createdAt`, `sessionKey` |
| roles | `createdAt`, `name` |
| work items | `createdAt`, `id` |
| assignments | `openedAt`, `id` |
| attests | `ts`, `id` |
| wakes | `createdAt`, `wakeId` |
| turns | `seq` |
| transcript messages | `seq` |
| artifacts | `createdAt`, `artifactId` |
| decision requests | `raisedAt`, `id` |
| users and devices | `createdAt`, primary ID |
| read markers | `updatedAt`, `scopeKey` |

No collection sorts by current status or `updatedAt`, except read markers.
Mutable sort keys cause skipped and repeated rows during paging.

### Filters

Filters are whitelisted per resource. Multiple filters are conjunctive.
Repeated values or comma-separated enum values are disjunctive within one
field. Unknown enum values return a typed 400 error. Unknown exact IDs used as
filters return an empty collection. They do not become existence oracles.

Recommended filters:

| Resource | Filters |
|---|---|
| sessions | `state`, `ownerUserId` for admin, `spawnedBy`, `archetype`, `harness`, `provider`, `model`, `host`, `role` |
| work items | `state`, `ownerUserId`, `createdBySession`, `createdByUser`, `isBug`, `specRefName`, `holderKey` |
| assignments | `state`, `outcome`, `holderKey`, `holderRole`, `workItemId`, `reviewsAssignmentId`, `effectKind`, derived `status` |
| attests | `assignmentId`, `workItemId`, `kind`, `verdictKind`, `bySession`, `byUser` |
| wakes | `state`, `sessionKey`, `creatorSessionKey`, `workItemId`, `assignmentId`, `conditionKind`, `conditionScope`, `class`, bounded due/fired time |
| turns | `status`, `sessionKey`, `assignmentId`, `workItemId`, `wakeId`, `jobRef`, bounded created/started/ended time |
| artifacts | `workItemId`, `createdBySession`, `kind`, `state` |
| decision requests | `status`, `kind`, `ownerUserId`, `assignmentId`, `raiserSessionKey`, `expecterSessionKey` |
| roles | `ownerUserId`, `boundSessionKey` |
| users and devices | admin-only status and ownership filters |
| read markers | caller user by default; `scopeKey` exact or prefix |

Do not add `fields`, arbitrary `sort`, arbitrary `include`, or generic join
parameters in v1.

## Resource routes

### Core model resources

| Route | Purpose |
|---|---|
| `GET /api/org` | Small org metadata, archetypes, hosts, and model catalog. Do not embed an unpaged session collection. |
| `GET /api/catalog/harnesses` | Harness capability catalog; canonical replacement for `GET /harnesses` |
| `GET /api/sessions` | Paged session collection |
| `GET /api/sessions/:sessionKey` | Session public projection plus current mechanical status |
| `GET /api/sessions/:sessionKey/messages` | Paged transcript projection |
| `GET /api/sessions/:sessionKey/coordination-share?from=&to=` | Current pure coordination aggregate |
| `GET /api/work-items` | Paged work-item collection |
| `GET /api/work-items/:id` | Work-item detail |
| `GET /api/work-items/:id/trace` | Existing composed trace |
| `GET /api/assignments` | Paged assignments, including derived status and advisory files/effect |
| `GET /api/assignments/:id` | Assignment detail |
| `GET /api/assignments/:id/attests` | Paged attests for one assignment |
| `GET /api/attests` | Paged bulk attests across authorized work |
| `GET /api/wakes` | Paged wake collection |
| `GET /api/wakes/:wakeId` | Wake detail |
| `GET /api/wakes/:wakeId/digest-members` | Current pure digest audit read |
| `GET /api/turns` | Paged turn collection |
| `GET /api/turns/:seq` | Turn detail |
| `GET /api/artifacts` | Paged artifact metadata |
| `GET /api/artifacts/:artifactId` | Artifact metadata detail |
| `GET /api/decision-requests` | Paged decision request collection |
| `GET /api/decision-requests/:id` | Decision request detail |
| `GET /api/read-markers` | Caller-visible marker collection |
| `GET /api/read-markers/:scopeKey` | One marker |
| `GET /api/roles` | Paged role registry |

The bulk `/api/attests`, `/api/turns`, and `/api/wakes` collections are
important. Nested-only resources would force ATC-class clients into one request
per work item or session.

### Mechanical views and administration

| Route | Purpose |
|---|---|
| `GET /api/toplines` | Existing mechanical roster projection |
| `GET /api/toplines/:selection` | One composed subtree/detail selection |
| `GET /api/facts` | Existing scoped fact read |
| `GET /api/critical-state` | Current critical-state inspection projection |
| `GET /api/identity` | Admin identity publication state |
| `GET /api/kungfu` | Installed bundle catalog |
| `GET /api/config/:key` | Safe config value only; secrets excluded |
| `GET /api/host-env` | Admin projection; never expose secret values by default |
| `GET /api/harness-processes` | Admin operational projection; omit `identityToken` |
| `GET /api/users`, `GET /api/devices` | Admin-only public projections; omit device tokens |

These routes are in the read plane, but they are not all part of a normal
display-model bootstrap.

## Canonical public projections

The API must not serialize raw rows. Each resource owns an explicit field list.

At minimum:

- A session exposes identity, ownership, ancestry, archetype, host, harness,
  model fields, state, and timestamps. It omits `cliToken`.
- A device exposes identity, owner, claimed name, status, platform, model, and
  creation time. It omits `token`.
- A harness process omits `identityToken` and any credential-bearing path or
  environment value.
- A work item exposes its full product fields.
- An assignment exposes its full product fields, advisory files, effect kind,
  holder state, and mechanically derived status.
- An attest exposes its recorded fields and parsed commit references.
- A wake exposes its recorded coordination fields. Prompt content remains
  visible under the same owner rule as transcript content.
- A transcript message uses the existing transcript projection. Its `id` must
  equal the notice message ID.
- An artifact exposes deliberate metadata. `/download/:assetId` owns bytes.

“Unredacted” means that the projection does not redact user content or normal
row fields after authorization. It does not convert storage secrets into API
fields.

This distinction needs an amendment in event-firehose r4.2. V3 currently says
the changed row's full recorded truth is unredacted. The database contains
credentials, so a literal raw-row reading is unsafe. V3 and A6 should name the
canonical public projection instead.

## Read markers

The current `read_states` table is transcript-specific:
`(userId, sessionKey, lastReadMessageId)`. See
`lib/tightbeam/projection.ex:75-80`.

Firehose RM1 requires a more general row:
`(userId, scopeKey, marker)`. That row does not exist in the current schema.
The formal API should expose the new row, not pretend the old table already
satisfies RM1.

Recommended public shape:

```json
{
  "userId": "mike",
  "scopeKey": "work-item:wi_...",
  "marker": "att_...",
  "updatedAt": 1786900000000
}
```

Treat `marker` as an opaque string. The client owns its meaning. `updatedAt` is
mechanical ordering and conflict information. A marker write remains a verb,
as RM2 requires.

The notice uses refs `{userId, scopeKey}`, class `read_marker.updated`, and the
same payload shape.

## WebSocket correlation contract

Every notice must carry:

```json
{
  "type": "change",
  "schemaVersion": 1,
  "subscriptionId": "...",
  "seq": 4213,
  "class": "assignment.closed",
  "resource": "assignments",
  "op": "upsert",
  "occurredAt": 1786900000000,
  "refs": {"assignmentId": "asg_...", "workItemId": "wi_..."},
  "payload": {"id": "asg_..."}
}
```

`resource` and `op` remove class-parsing from model code. `class` remains the
human and subscription vocabulary. `refs` carries routing foreign keys.
`payload` carries the exact canonical resource.

Primary-key mapping:

| Resource | REST primary key | Notice ref |
|---|---|---|
| sessions | `sessionKey` | `sessionKey` |
| roles | `name` | `role` |
| users | `userId` | `userId` |
| devices | `deviceId` | `deviceId` |
| work items | `id` | `workItemId` |
| assignments | `id` | `assignmentId` |
| attests | `id` | `attestId` plus `assignmentId` |
| wakes | `wakeId` | `wakeId` |
| turns | `seq` | `turnSeq` plus `sessionKey` |
| messages | `id` | `messageId` plus `sessionKey` |
| artifacts | `artifactId` | `artifactId` plus `workItemId` |
| decision requests | `id` | `decisionRequestId` |
| read markers | `(userId, scopeKey)` | both fields |

For an upsert, clients replace the model entry at that key. For a delete,
`op` is `delete`, `payload` is the final public projection, and the client
removes the key. This is required for `role.removed`, because roles are hard
deleted today. See `lib/tightbeam/roles.ex:115`.

The client algorithm is:

1. Establish the subscription and receive `subscription_ready`.
2. Buffer notices.
3. Read every required REST collection, following pages.
4. Build the model from the REST items.
5. Apply buffered notices in arrival order as ID-keyed upserts or deletes.
6. Continue with live notices.
7. On reconnect or doubt, repeat the same rebuild.

Independent collection GETs do not need one cross-resource database
transaction. Subscribe-first buffering closes the gap. The client must apply
buffered notices only after all initial collections are loaded.

## Firehose issues that the REST spec must resolve

### Message creation has no class in the current registry

M4 says a chat client watches turn and message classes. The class registry in
r4.2 lists work, wakes, turns, decisions, org rows, artifacts, and read
markers, but it does not list a message-created class. See
`event-firehose-v1.md:185-214` and `:302-305`.

The REST transcript can build history, but it cannot make a live chat client
lively without a message notice. Add a message class, or explicitly keep the
existing chat socket as the live message carrier. Do not claim the dedicated
state firehose alone closes this need until one of those contracts is stated.

### Delete semantics are missing

The current notice shape has no operation field. A full-row payload does not
tell a generic client whether to upsert or remove. Add `resource` and `op`, or
define an equally typed per-class operation registry.

### Audit notices are not state-model notices

R5 includes `verb.accepted` and `verb.denied` for every gateway call. A denial
does not change domain state. N2 also says the internal `events` tables remain
write-only and out of scope. See `event-firehose-v1.md:104-106` and `:205-208`.

Do not add raw audit tables to the core REST model to hide this mismatch.
Either:

- classify these as observational notice-only classes outside the rebuildable
  state contract; or
- expose a separate admin operations resource and state its retention.

The same review applies to lifecycle and rail classes.

## Migration and compatibility

1. Freeze canonical public projections and visibility functions first.
2. Add REST collection and detail routes that call those seams.
3. Make notice payload builders call the same serializers.
4. Make CLI read handlers call the same query services.
5. Keep current HTTP routes as compatibility adapters.
6. Migrate Clawline from stream/status aliases to sessions and transcript GETs.
7. Migrate ATC from direct SQL to paged core resources.
8. Remove compatibility routes only under a separate versioned decision.

No current CLI read needs removal. No current client route needs an immediate
breaking rename.

## Acceptance proofs for the future spec

1. For every notice class, a table-driven test names its resource, operation,
   primary-key mapping, public serializer, and visibility function.
2. For every resource, REST detail and notice payload are byte-equivalent after
   removing envelope fields.
3. No public projection contains `cliToken`, device `token`,
   `identityToken`, or a secret host environment value.
4. A subscribe-first, multi-resource snapshot plus buffered notices converges
   under concurrent creates, updates, and deletes.
5. A forced disconnect followed by a fresh REST rebuild converges without
   event history.
6. Pagination covers tied timestamps, deleted cursor-neighbor rows, empty
   pages, before, after, the 50 default, and the 500 cap.
7. Unauthorized detail and cursor reads are indistinguishable from unknown
   rows.
8. ATC can build its current agent/work/turn model without SQLite access.
9. Clawline can list sessions, page older transcript, fetch current work state,
   and correlate live notices by exact IDs.
10. Existing CLI wrappers return the same item shapes as REST for equivalent
    reads.

## Final recommendation

Adopt this binding rule: every read of shared Tightbeam state has a canonical
REST endpoint, and every retained CLI form calls that endpoint and only
selects, composes, summarizes, or formats for terminal use. Only local help and
diagnostics stay CLI-only; all state changes stay dispatch verbs.

The complete disposition is fixed above: 20 public CLI read forms, seven
additional dispatch reads, and 11 current HTTP reads each have one label, one
canonical target, and one reason. The five named boundary cases each have a
binding route and ruling.

This implements the three-plane ruling from `rest-vs-cli-adjudication.md`:

- REST is the canonical read plane.
- Dispatch verbs are the write plane.
- The CLI is convenience sugar.

Amend the draft inventory in four places:

1. Split the paged session collection from the small `/api/org` document.
2. Add first-class bulk resources for wakes, turns, and attests.
3. Put `coordination-share` and `digest-members` in the read plane.
4. Define safe canonical projections, delete operations, and exact notice IDs.

Do not expose SQLite tables. Do not grow a generic query language. Do not make
the firehose a second source of truth.
