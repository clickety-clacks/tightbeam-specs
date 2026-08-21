# REST state API v1 — the read plane (product spec, r1)

Status: DRAFT r1, 2026-08-21, written by tb02. Untargeted (0.2.0 or
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

SP4. One projection per resource, shared with the firehose. The REST
detail item and the ws notice payload are the same bytes from the same
serializer. Two serializers would drift, and drift between two public
shapes of one row is a standing bug factory.

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
unversioned routes become compatibility aliases (R12) until clients
migrate; an incompatible future API is a new versioned namespace.

R2. Core model resources:

| Route | Purpose |
|---|---|
| GET /api/org | small org document: archetypes, hosts, model catalog — no embedded session collection |
| GET /api/sessions | paged sessions |
| GET /api/sessions/:sessionKey | session detail + mechanical status |
| GET /api/sessions/:sessionKey/messages | paged transcript projection |
| GET /api/sessions/:sessionKey/coordination-share | pure aggregate read |
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

R3. Mechanical views and admin reads: GET /api/toplines[/:id],
/api/facts, /api/identity, /api/kungfu, /api/config/:key (safe values
only), /api/host-env (no secret values), /api/harness-processes (no
identityToken), /api/users and /api/devices (admin-only, no tokens).
Part of the read plane; not part of a normal display-model bootstrap.

R4. Envelopes. List:
`{"schemaVersion":1,"resource":"assignments","items":[],"page":{"oldestId":null,"newestId":null,"hasMoreBefore":false,"hasMoreAfter":false}}`.
Detail: `{"schemaVersion":1,"resource":"assignments","item":{}}`. The
`item` shape equals the firehose notice `payload` shape (SR1).

R5. Pagination: `before`/`after` (mutually exclusive, exclusive bounds),
`limit` default 50 cap 500 (clamped), no cursor = newest page, page items
oldest→newest, keyset only on immutable orders (createdAt/openedAt/ts/seq
+ id tiebreak; the transcript precedent), unknown or forbidden cursor =
`400 cursor_not_found`, filters fixed within one page chain, offset
pagination forbidden.

R6. Filters: whitelisted per resource (the adopted tables in the recon
report are the v1 baseline), conjunctive across fields, disjunctive
within a repeated field, unknown enum = typed 400, unknown exact-id
filter = empty collection (never an existence oracle). No `fields`,
`sort`, `include`, or join parameters in v1.

## Requirements — projections and serializers

SR1. One query function and one public serializer per resource; the REST
adapter, the CLI read wrappers, and the firehose notice publisher all
call those seams. This is enforced by code structure, not review prose:
REST detail and notice payload are byte-equivalent after envelope
removal (firehose A6).

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

C1. Every CLI read verb becomes a wrapper over the corresponding read
service (same query function, same serializer). No CLI read keeps a
second implementation.

C2. New flexible reads are designed REST-first; the CLI gains a wrapper
only when a common agent task wants one line. `doctor` stays local (it
probes the host, it is not a state resource).

## Migration (order is normative)

M1. Freeze projections and visibility functions. M2. Add REST routes on
those seams. M3. Point the firehose payload builders at the same
serializers. M4. Point CLI read handlers at the same query services.
M5. Keep current routes as compatibility aliases (/api/streams,
/api/org-options, /api/session-status, /api/work[/:id],
/api/trackable-sessions). M6. Migrate Clawline (streams/status aliases →
sessions + transcript GETs). M7. Migrate ATC off direct SQLite. M8.
Retire aliases only under a separate versioned decision (SQ3). No
breaking rename lands before its client moves.

## Acceptance

A1. Table-driven per-class test: resource, op, primary-key mapping,
serializer, visibility function (shared with firehose A6).
A2. Byte-equivalence: REST detail item == notice payload per class.
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
