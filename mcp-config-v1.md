# MCP config as identity data — implementation spec (v1)

Archetypes declare the MCP servers their sessions get; the config flows to
the harness THROUGH ACP (`session/new` / `session/load` already take an
`mcpServers` array) — no files written into homes, no harness-state
clobber risk, no per-harness config formats. Identity data in, protocol
out. Repo: worktree `~/src/tightbeam_ex-mcp` (branch `mcp-config`).
Decision-complete; implementer decides internal naming/test layout only.
Gates: `mix compile --warnings-as-errors` clean, `mix test` fully green.
Do not commit. STOP and report on any conflict.

## Invariants

1. MCP config is ARCHETYPE data — declared in the manifest, validated at
   load (bad law fails the boot), carried per-session to the harness at
   session creation AND load. The substrate never starts, monitors, or
   proxies an MCP server; it only relays the declaration (T1).
2. Zero declarations = today, byte-for-byte: sessions of archetypes with
   no MCP config send `mcpServers: []` exactly as now; no manifest hash
   changes for them (MCP config is NOT part of the home — it never enters
   the projection or its hash; changing it costs no session its memory
   and takes effect at the next adapter session create/load).
3. Fail closed at load, tolerate at runtime: a malformed declaration
   stops the boot; a harness that rejects or ignores a declared server at
   runtime is the harness's business (its error surfaces on the turn like
   any other; per-harness acceptance is a harness-support-matrix row, not
   substrate logic).

## Manifest schema (archetypes.ex)

```toml
[mcp.xcodebuild]                   # one table per server; key = server name
command = "xcodebuildmcp"          # required: executable
args = ["--daemon"]                # optional, default []
env = { XCODEBUILD_MCP_MODE = "cli" }  # optional, default {}
```

Validation (all `ArgumentError` at load!, messages containing the quoted
fragments):
- server name must match the role/skill lexicon `^[a-z0-9][a-z0-9-]*$` →
  else `invalid mcp server name`.
- `command` required non-empty string → `mcp server <name> is missing
  "command"`.
- `args` must be a list of strings → `mcp server <name>: args must be a
  list of strings`; `env` a map of string→string → `mcp server <name>:
  env must be string keys and values`.
- unknown keys inside a server table → `unknown mcp server keys` + names.

Archetype type gains `mcp: [%{name, command, args, env}]` (list, manifest
order), default `[]`. The builtin default archetype has `mcp: []`.

## Wire-through (adapter seam)

- `Tightbeam.Acp.Adapter.new_session/3` and `load_session/4` gain an
  `mcp_servers` argument (list of maps, ACP shape below); both pass it as
  the `mcpServers` param INSTEAD of the current hardcoded `[]`.
- ACP shape per server: `%{"name" => name, "command" => command,
  "args" => args, "env" => [%{"name" => k, "value" => v}, ...]}` (env as
  a LIST of name/value pairs — that is the ACP schema, not a bare map;
  sort env pairs by name for determinism).
- `Gateway.harness_session/6` builds the list once per call from the
  session's archetype (`Archetypes.get(session.archetype).mcp`) via a
  pure `Rails`-style compiler function `Archetypes.acp_mcp_servers/1`
  (archetype → ACP-shaped list) and passes it to new/load. The fallback
  (re-create) path passes it too.
- `tune set_harness`'s fresh-session path and any other new/load call
  sites pass it identically — grep for every `new_session(`/
  `load_session(` call site; NONE may keep a literal `[]` except tests
  exercising the empty case.

## Out of scope (STOP conditions)

No home/projection changes, no per-session MCP overrides, no URL/SSE
transports (command servers only in v1 — reject a `url` key with
`unknown mcp server keys` like any unknown), no health checks, no CLI
changes, no codex-specific handling (same ACP param; acceptance is the
harness's business).

## Tests (end conditions)

1. Validation matrix rows above (tmp-dir manifests, archetypes_test
   style).
2. `acp_mcp_servers/1`: byte-pinned output for the example above
   (including env-as-sorted-pairs shape); `[]` for no config.
3. Adapter: new_session and load_session pass the given list through to
   the `session/new`/`session/load` params (extend the existing adapter
   tests' fake conn to capture params; assert `mcpServers` equals the
   input; assert `[]` still sent when empty).
4. Gateway: a session whose archetype declares a server reaches the
   adapter stub with that ACP-shaped list (extend the AdapterStub to
   capture the argument in one existing golden test — smallest possible
   touch).
5. Full suite green; only these files: `lib/tightbeam/archetypes.ex`,
   `lib/tightbeam/acp/adapter.ex`, `lib/tightbeam/gateway.ex`, their
   test files.
