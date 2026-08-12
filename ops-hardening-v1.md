# Ops hardening v1 — implementation spec

Six independent, focused tasks finishing core ops (spawning, management,
comms). Each section stands alone; implement ALL, in order. Repo:
`~/src/tightbeam_ex`. Gate: `mix compile --warnings-as-errors` clean and
`mix test` fully green after EVERY section (do not batch-break the suite).
Follow the existing comment discipline (moduledocs carry invariants and
WHY; match `lib/tightbeam/archetypes.ex`'s voice). Touch nothing outside
the files each section names. Do not commit; leave the tree for review.
If a section conflicts with the tree, STOP and report.

## 1. cliToken persists across boots

Today `Gateway.children/1` mints a fresh `cliToken` every boot and
rewrites `gateway.json` — anything holding the old token dies on restart.
Change: if `gateway.json` exists and decodes with a non-empty `"cliToken"`
string, KEEP that token (still rewrite the file to refresh `port`); mint
only when absent/invalid. File mode stays 0600.
Files: `lib/tightbeam/gateway.ex`, `test/gateway_test.exs`.
Tests: children/1 twice against the same base_dir → same token, updated
port; corrupt/missing gateway.json → fresh token minted.

## 2. Wake targets accept a user id (reach the operator's Main)

Wake resolution today: a target is a sessionKey or an agent handle. Add:
a bare user id (`mike`) or `user:<id>` resolves to that user's Main
session via `Org.personal_session_key/1` — but ONLY when that user exists
(users table) AND no session handle shadows the bare id (handle lookup
wins; document that precedence in one comment). Unknown stays the
existing not-found error. This applies wherever wake/cancel-wake targets
resolve (the shared target_session/resolve path in gateway or router —
find the single chokepoint; do NOT duplicate logic per verb).
Files: the one resolver site (+ its module), `test/gateway_test.exs` or
`test/router_test.exs` (wherever target resolution is already tested).
Tests: wake target "mike" → enqueued for the Main key; "user:mike" same;
handle shadowing (a session with handle "mike" wins); unknown id → error.

## 3. Model pin in projected claude homes (the fable fix)

Claude's offered-model list is environment-dependent (see
harness-support.md, Model row): fresh workdirs don't offer fable at all.
Fix: every projected CLAUDE home's `settings.json` pins a model, so the
pin puts it on the offered list deterministically.
- New config: `Application.get_env(:tightbeam, :model_pins)` defaulting to
  `%{"fable" => "claude-fable-5[1m]"}` (runtime.exs override via
  `TIGHTBEAM_MODEL_PINS` JSON, same pattern as TIGHTBEAM_HOSTS).
- In `Placement.deliver_home`, for `:claude` only: pick the session-facing
  default ref = `archetype.defaults[:model] || config default model ref`
  (the config map already carries the org default); map it through
  :model_pins — a hit yields the pin VALUE, a miss uses the ref verbatim.
  Merge `%{"model" => value}` into the settings map that rails may already
  contribute (`Rails.claude_settings/0` may be nil — merging must handle
  nil on either side; the settings.json extra_file now exists whenever
  EITHER source contributes). Codex homes unchanged, byte-identical.
- Hash consequence: claude homes regenerate ONCE on deploy (identity
  change; the context-reset markers will show — expected, note it in the
  moduledoc where the pin is built, not as a code comment).
Files: `lib/tightbeam/placement.ex`, `config/runtime.exs`,
`test/placement_test.exs`.
Tests: claude home settings.json contains {"model": "claude-fable-5[1m]"}
under default org config; archetype default model overrides; merge with a
rails statute present yields BOTH "model" and "hooks" keys; codex home
has no settings.json when no statutes exist.

## 4. Host-keyed adapter stderr logs

`adapter-<harness>:<archetype>.stderr.log` collides across hosts. Rename
to `adapter-<harness>:<archetype>@<host>.stderr.log` in
`Placement.adapter_opts/2`.
Files: `lib/tightbeam/placement.ex`, `test/placement_test.exs` (update the
pinned opts assertions).

## 5. External wake seam — formal contract for an external wake engine

The operator will run wake scheduling in an EXTERNAL engine; the substrate
must expose a stable seam. Most of it exists; formalize and finish:
- `wake` verb gains optional `idempotency_key`: dedupe per (origin,
  idempotency_key) exactly like spawn's (reuse the Idempotency store; the
  stored result replays). An external engine retrying a schedule call must
  not double-schedule.
- `inspect` for a `process:` origin currently resolves to no owner and
  shows nothing useful. Change: for process callers, `inspect` returns
  `%{wakes: [...]}` — the pending wakes whose origin equals the caller's
  origin, each with wakeId, sessionKey, dueAt, prompt. (No sessions, no
  devices — a process has no ownership.)
- `cancel-wake` already works for the scheduling origin; add a test
  proving a process origin can cancel ONLY its own wakes (another
  origin's wakeId → the existing not-found/denied error).
Files: `lib/tightbeam/gateway.ex`, `test/gateway_test.exs`.
Tests: wake with idempotency_key twice → one row, same wakeId replayed;
process-origin inspect lists exactly its own pending wakes; process
cancels own wake ok, other origin's wake denied/not-found.

## 6. Workdir follows the session on `tune set_host`

Per-session workdirs are host-local; `set_host` currently strands the
session's durable scratch (and any self-written memory) on the old host.
In the `set_host` tune handler, AFTER placement resolve succeeds and
BEFORE `Org.set_host` commits: sync `<old base>/work/<digest>` →
`<new base>/work/<digest>` (digest is derivable — same session_key hash
used by `Gateway.session_workdir/2`). Four topologies via the existing
host_config ssh fields (nil = local path):
  local→local: `File.cp_r!`; local→remote: rsync to `dest:<path>`;
  remote→local: rsync from `dest:<path>`; remote→remote: rsync with the
  source host as the ssh -e hop is NOT supported — do old→gateway staging
  tmp → new (two rsyncs through `<base_dir>/staging/workdir-moves/<digest>`,
  cleaned after).
Missing source dir = nothing to move (fresh sessions), proceed. Any sync
FAILURE denies the tune with `%{code: "workdir_move_failed", message: ...}`
— fail closed; silent memory loss is never acceptable. Use the injectable
`:sh` runner pattern from `Placement.deliver_home` so tests capture
command lines. Put the sync in Placement (`move_workdir/4` or similar),
not inline in the gateway handler.
Files: `lib/tightbeam/placement.ex`, `lib/tightbeam/gateway.ex`,
`test/placement_test.exs`, `test/gateway_test.exs`.
Tests: command-capture for all four topologies (local→local may use a real
tmp dir copy); failure → tune denied and Org.host unchanged; missing
source → tune proceeds.

## Acceptance
Warnings-clean compile; full suite green; only the files named above
changed (+ this is six sections — a section's tests land with its code).
Do not commit.
