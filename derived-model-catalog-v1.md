# Derived model catalog v1 — full model inventory derived from each harness

Status: DRAFT r2 (Flynn-converged design; supersedes r1). r1's build exists (uncommitted in
tightbeam_ex-modelcat) and is REVISED to this, not restarted from scratch.

## Goal

Replace the hardcoded `@model_catalog` constant (gateway.ex ~87) and the `model_pins` map with a
**full model INVENTORY derived from each harness**. The substrate publishes the complete, neutral
truth (every model the harness reports, with its metadata); it does NOT curate, alias, or pin.

## Substrate / product boundary (governing principle)

The SUBSTRATE exposes the full derived inventory. The CLIENT is responsible for offering the models
in an organized fashion (grouping by family, hiding old versions, choosing which efforts to show,
etc.). So: NO allowlist, NO "sensible subset", NO friendly-alias namespace, NO `model_pins` in the
substrate. The substrate hands over everything; the client projects it.

## Canonical ref = the provider identifier (opaque)

There is ONE model namespace: the provider's real id, treated as an OPAQUE string.
- Claude ref = the API `id` (`claude-opus-5`).
- Codex ref = the cache `slug` (`gpt-5.6-sol`).
- Effort rides as the existing `id[effort]` bracket syntax (tightbeam's ONLY contribution — the
  string packing; the effort concept + levels are the harness's). `parse_model_ref` and the effort
  config-option path are UNCHANGED (claude applies it via config `effort`, codex via
  `reasoning_effort`).
- No aliases (`opus`), no pins, no `[1m]` (1M is intrinsic `max_input_tokens`, not a ref). Because
  ids are opaque and never parsed into family/version, an Anthropic naming change cannot break a
  parser — an id is just a string that is or isn't in the live inventory.

Model is ALWAYS specified (an explicit ref or the config default) — there is no "floating": the
stored `session.model` is a concrete provider ref, locked to exactly what was chosen. To get a newer
model, pick a newer one.

## Derivation (all metadata from the same fetch as the models)

Per harness, derive the inventory: for each model, one catalog entry carrying `ref`, `display_name`,
`efforts` (the provider-reported supported levels), `max_input_tokens`/context, and the raw
capability info the client may want to organize on. Emit `ref` where there are no efforts, and one
`ref[effort]` per reported effort.

- CLAUDE (live API): `GET https://api.anthropic.com/v1/models?limit=100` with `Authorization:
  Bearer <token>` (token at `<base_dir>/auth/claude/oauth-token` — VERIFIED it authorizes the
  endpoint) + `anthropic-version: 2023-06-01`. Each model: `id`, `display_name`, `max_input_tokens`,
  `capabilities.effort` = `{low,medium,high,xhigh,max: {supported}}` (per-model supported effort
  levels — VERIFIED on claude-opus-5). DETERMINE whether the list endpoint already includes
  `capabilities.effort`; if not, fetch per-model `GET /v1/models/<id>` (≤~10 models, cache them).
  Derive `id[effort]` for each supported effort; bare `id` if none.
- CODEX (its maintained cache): `<CODEX_HOME>/models_cache.json` →
  `{models:[{slug, display_name, supported_reasoning_levels:[{effort}]}]}` (VERIFIED sol supports
  low/medium/high/xhigh/max/ultra). Derive `slug[effort]` per supported level; bare slug if none.

## Config default = a provider id (settable)

`TIGHTBEAM_DEFAULT_MODEL` / archetype `defaults[:model]` must be a real provider ref
(`claude-opus-5`, `gpt-5.6-sol[medium]`), validated against the derived inventory at use — warn
loudly if the configured default is not currently offered (do not silently ship a dead default).
No pin/alias resolution step exists anymore.

## Invariants

- I1 — Every derived ref is a real (model[,effort]) the harness supports; spawn/tune validate against
  the derived inventory (so a dead ref can't be offered or accepted). `opus[1m]` can't be derived.
- I2 — `parse_model_ref` and the effort mechanism UNCHANGED; only the catalog source + the removal of
  aliases/pins change.
- I3 — Graceful degrade, NEVER crash: missing/expired token, 401, network error/timeout, malformed or
  unexpectedly-shaped JSON, missing codex cache — each yields empty-or-last-known for that harness +
  a logged warning. Never raise into gateway boot, `/list`, or `/api/org-options`.
- I4 — ASYNC + cached: derive into an in-memory cache (TTL ~15 min). The network/file fetch runs in a
  spawned Task that messages the result back — it must NEVER run inside a GenServer call that a reader
  awaits, and must NEVER block gateway boot. Readers get the cached value (or empty/last-known)
  immediately; a slow/hung API call cannot time out `/list`. (This is the r1 review's MAJOR + boot
  findings — the blocking in-callback fetch is the specific defect to fix.)

## All readers + validation

Every `@model_catalog` reader (gateway.ex org-options, session_status, inspect/list, spawn, tune
set-model, tune harness-swap) reads the derived inventory; spawn + tune validate the ref against it.
No hardcoded catalog and no `model_pins` remain as a source of truth.

## Freshness contract (adjudication requirement)

Added for `model-adjudication` (`model-ringdown-pattern.md`), which must distinguish a
model that is *genuinely, currently* absent from one that only *looks* absent because a
refresh failed — otherwise a Claude-catalog 401 reads as "model missing" and an adjudicator
wrongly rings to Codex, masking an auth fault. Membership answers therefore carry a **health
state**, not just data:

The three states partition on **the data's age, not the refresh's fate**, so coverage is
total — every membership answer lands in exactly one:

- `fresh` — data derived for that harness **within the TTL**.
- `stale` — **data exists but is not `fresh`** — its age is past the TTL, for ANY reason. This
  single state covers both a *failed* refresh still serving last-known data AND an
  *in-flight* refresh while the cached data has already expired (the case a fate-based split
  missed): if there is data and it is not fresh, it is stale. Ruling: any present-but-not-fresh
  data ⇒ `stale`, never `unavailable`.
- `unavailable(reason)` — **no data at all** for that harness (never derived, or empty cache)
  plus the failure reason.

Requirements on the reader:

- Every membership query returns `{present?: bool, health: fresh | stale | unavailable(reason)}`
  for the harness the ref belongs to — the state travels with the answer.
- Absence is trustworthy **only** when `health = fresh`. A caller MUST NOT treat absence under
  `stale`/`unavailable` as "model missing."
- This refines I3: the graceful-degrade path additionally records which of `stale` /
  `unavailable(reason)` it entered, so readers can tell them apart.

## Hardening (from r1 review)

- Declare `:ssl` (and `:inets` for `:httpc`) explicitly in `extra_applications` — do not rely on
  bandit transitively starting `:ssl`.
- The HTTPS call MUST verify the server certificate (peer verification / CA store) — the r1 build used
  `verify_none`, exposing the bearer token to MITM. Verify the cert.
- No admin/refresh verb (r1 added an unspecced `refresh/1`; drop it — TTL is enough for v1).

## Migration

Pre-users, so cheap: existing sessions store alias models (`opus`, `fable`) that are not valid
provider ids. Normalize them to the resolved id or reset the playground org — do not leave sessions
with refs that fail validation. (Note this; the reset itself is an ops step, not code.)

## Non-goals

- No client-side presentation logic in the substrate (grouping/curation is the client's job).
- No alias namespace, no `model_pins`, no float/lock modes, no per-request network/file I/O.
- No change to `parse_model_ref` or how effort is applied to a harness.

## Tests

- Claude inventory derived from a fixture API JSON (INJECT the fetch — no test hits the network):
  correct `id[effort]` set from `capabilities.effort`, display names, max_input_tokens; bare id when
  no efforts.
- Codex inventory from a fixture models_cache.json: `slug[effort]` per supported level incl. the ones
  the old catalog missed (`max`, `ultra`); bare slug when none.
- Degrade: missing token / failed fetch / malformed JSON / missing cache → empty-or-last-known, NO
  crash of a reader, boot, or `/list`.
- ASYNC: a slow/hung fetch does NOT block `ModelCatalog.get` or a concurrent `/list` (the r1 MAJOR) —
  assert a reader returns promptly (cached/empty) while a refresh is in flight.
- `opus[1m]` (and any `[1m]`) never appears. Validation accepts every derived ref, rejects an absent
  one, and — with a provider-id default — the default claude spawn path validates (the r1 CRITICAL).
- No `@model_catalog`/`model_pins` remains as source of truth.

## Handoff

Revise the r1 build in tightbeam_ex-modelcat to this. Both sources + effort derivation are fully
resolved above (no investigation needed). Build gate: `mix compile --warnings-as-errors` + `mix test`
(+ seeds) green. Then Opus code-review before merge.
