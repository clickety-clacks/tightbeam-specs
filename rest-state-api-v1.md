# REST state API v1 — the read plane (product spec, r2)

Status: DRAFT r2, 2026-08-22. r2 folds the reviewed mechanical amendment
`art_8e2d8444` (reviewed-clean `att_0b648694`): adopted route/filter
inventory, interim/final CLI transport, firehose serializer scope, the
R12-to-M5 repair, and the harness-catalog compatibility ruling. Written
by tb02 and product-owner:rest-state-api. Untargeted (0.2.0 or
later); when build work starts it branches from main tip. OWNED by
product-owner:rest-state-api (staffed under
product-owner:tightbeam-codex-sol-relief) — spirit questions route to
Mike through that PO.

Authority and inputs:
- rest-vs-cli-adjudication.md r2 (tb02, Mike-directed): the three-plane
  ruling this spec implements. REST is the read plane, verbs are the
  write plane, the CLI is sugar.
- Recon wi_9239a7f1's report (NFS
  shared/specs/tightbeam/rest-state-api-recon.md): the inventory,
  contract baseline, and code evidence. Adopted with zero material
  rejections; its six conditions are folded in as requirements here.
- event-firehose-v1.md r5: the sibling notice socket. The two contracts
  share serializers (SR series below) — that sharing is the whole
  correlation story.
- Mike's rulings, 2026-08-20/21: clients build models from state, not
  events; SQL against state.db is not a product interface; the CLI makes
  common things easy and never re-creates SQL; auth is the existing
  gateway credential, no API keys; deployment is localhost/tailscale.

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

## Terms

T1. **Resource** — one product entity or mechanical composed view with a
canonical public projection and a stable primary id.

T2. **Projection** — the explicit public field list for a resource. One
serializer owns it (SR1). Storage secrets never appear in any projection.

T3. **Keyset cursor** — the resource's public primary id used as an
exclusive `before`/`after` boundary, resolved server-side to an immutable
ordering tuple. Never an offset.

## Requirements — surface

R1. Namespace `/api/<resource>`, JSON, every response carrying
`"schemaVersion": 1`. `/version` remains the preflight. Existing
unversioned routes become compatibility aliases (M5) until clients
migrate; an incompatible future API is a new versioned namespace.

R2. Core model resources:

| Route | Purpose |
|---|---|
| GET /api/org | small org document: archetypes, hosts, model catalog — no embedded session collection |
| GET /api/catalog/harnesses | canonical harness capability catalog using the v1 response envelope; `/harnesses` remains an undeprecated compatibility alias using its legacy raw-array outer envelope |
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
| GET /api/decision-requests[, /:id] | paged collection, detail |
| GET /api/read-markers[, /:scopeKey] | caller's markers (write stays a verb, firehose RM2) |
| GET /api/roles | paged role registry |

The bulk attests/wakes/turns collections are first-class on purpose:
nested-only resources force ATC-class clients into one request per parent.

The two harness-catalog routes share authorization, the canonical query,
ordering and filtering, and one canonical serializer for each harness item.
Only their outer wire adapters differ. They do not promise byte-identical
complete responses. The canonical route wraps items in the v1 envelope;
the compatibility alias preserves its legacy raw array.

R3. Mechanical views: GET /api/toplines[/:id], /api/facts, and
/api/critical-state. The remaining candidate admin reads — /api/identity,
/api/kungfu, /api/config/:key, /api/host-env, /api/harness-processes,
/api/users, and /api/devices — remain conditional on SQ2. If adopted,
their safe projections and admin-only visibility must be frozen before
routes ship. Mechanical and admin views are not part of a normal
display-model bootstrap.

R4. Envelopes. List:
`{"schemaVersion":1,"resource":"assignments","items":[],"page":{"oldestId":null,"newestId":null,"hasMoreBefore":false,"hasMoreAfter":false}}`.
Detail: `{"schemaVersion":1,"resource":"assignments","item":{}}`.
For every notice-backed resource, the `item` shape equals the firehose
notice `payload` shape (SR1).

R5. Pagination: `before`/`after` (mutually exclusive, exclusive bounds),
`limit` default 50 cap 500 (clamped), no cursor = newest page, page items
oldest→newest, keyset only on immutable orders (createdAt/openedAt/ts/seq
+ id tiebreak; the transcript precedent), unknown or forbidden cursor =
`400 cursor_not_found`, filters fixed within one page chain, offset
pagination forbidden.

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
| decision requests | status, kind, ownerUserId, assignmentId, raiserSessionKey, expecterSessionKey |
| roles | ownerUserId, boundSessionKey |
| users and devices | admin-only status and ownership filters, only if SQ2 exposes these resources |
| read markers | caller user by default; scopeKey exact or prefix |

Filters are conjunctive across fields and disjunctive within a repeated
field. Unknown enum = typed 400. Unknown exact-id filter = empty collection,
never an existence oracle. No `fields`, `sort`, `include`, or join parameters
exist in v1. The technical specification must pin wire names and inclusivity
for every bounded-time pair; this product spec does not invent them.

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

SR4. Ids are the correlation contract: each projection's primary id
equals the id the firehose notice `refs` carry (firehose V5 and its
primary-key table). A client dedupes snapshot-vs-notice by these ids.

## Requirements — auth and visibility

AU1. `Authorization: Bearer <existing gateway credential>`. A device
token resolves to its user; a session CLI token to its session and owner.
No new credential type; no `asUser` query parameter ever (query strings
are logged and are poor identity carriers).

AU2. The org CLI token names no principal by itself; CLI reads continue
through /agent/dispatch until a reviewed GET identity carrier exists
(SPIRIT QUESTION SQ1). The canonical read service takes a RESOLVED
principal, so this migration changes only transport, never authorization.

AU3. Visibility: collections omit rows the principal cannot read; detail
returns the same 404 for unknown and forbidden (transcript precedent);
owner-or-admin scoping unless a live spec names stricter; admin resources
refuse non-admins. REST and firehose subscription filtering use the SAME
visibility function.

## Requirements — relationship to the CLI

C1. In the final v1 shape, every retained CLI shared-state read calls the
corresponding REST GET and may only select, compose, summarize, or format
that response. Until SQ1 supplies a reviewed GET identity carrier, the CLI
may continue through `/agent/dispatch`; that adapter calls the same canonical
query function and serializer with a resolved principal. No CLI read keeps a
second query or serializer implementation.

C2. New flexible reads are designed REST-first; the CLI gains a wrapper
only when a common agent task wants one line. `doctor` stays local (it
probes the host, it is not a state resource).

## Migration (order is normative)

M1. Freeze projections and visibility functions. M2. Add REST routes on
those seams. M3. Point the firehose payload builders at the same
serializers. M4. Point CLI read handlers at the canonical read services.
Move each wrapper from dispatch to its REST GET only when AU2 has a reviewed
identity carrier; this transport move does not change item shapes,
authorization, or the M1 query and serializer seams.
M5. Keep current routes as compatibility aliases (/api/streams,
/api/org-options, /api/session-status, /api/work[/:id],
/api/trackable-sessions, /harnesses). M6. Migrate Clawline (streams/status aliases →
sessions + transcript GETs). M7. Migrate ATC off direct SQLite. M8.
Retire aliases only under a separate versioned decision (SQ3). No
breaking rename lands before its client moves.

## Acceptance

A1. Table-driven per-class test: resource, op, primary-key mapping,
serializer, visibility function (shared with firehose A6).
A2. For every non-observational rebuildable-state class governed by
firehose A6, the REST detail item equals the notice payload after envelope
removal.
A3. Secret-exclusion sweep over every projection.
A4. Subscribe-first multi-resource snapshot plus buffered notices
converges under concurrent creates/updates/deletes; reconnect + fresh
rebuild converges with no event history.
A5. Pagination proofs: tied timestamps, deleted cursor neighbors, empty
pages, before/after, default 50, cap 500.
A6. Unauthorized detail/cursor indistinguishable from unknown.
A7. ATC builds its current model with zero SQLite access; Clawline lists
sessions, pages transcript, fetches work state, and correlates notices
by exact ids.
A8. CLI wrappers return the same item shapes as REST for equivalent
reads.

## Spirit questions for Mike (the PO's quiz list)

SQ1. The org-token GET identity carrier (AU2): design a reviewed header
scheme so the CLI can hit GETs directly, or keep CLI reads on dispatch
indefinitely? (Interim posture is safe; this is about ergonomics.)

SQ2. Admin reads exposure (R3): comfortable with users/devices/host-env
projections existing at all on the read plane, or should admin reads stay
CLI/dispatch-only on this deployment?

SQ3. Compatibility alias retirement: aggressive (retire when Clawline+ATC
migrate) or indefinite tolerance?

SQ4. Sequencing: does the REST plane ship before, with, or after the
firehose socket? They share serializers, so building REST first makes the
firehose payloads nearly free; confirm that ordering instinct.

SQ5. Tailnet identity: wi_bdf9a537 (gateway behind tailscale serve) would
add tailscale identity headers — should AU1 anticipate accepting tailnet
identity as a principal source once that lands, or stay
bearer-credential-only in v1?
