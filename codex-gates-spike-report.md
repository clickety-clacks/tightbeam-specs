# Codex gate projection — spike report

Status: SPIKE COMPLETE 2026-07-20, run live on eezo against codex-cli
0.144.6 (`@openai/codex` npm install; native binary
`node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin/bin/codex`).
Question under test: can tightbeam's rails gate tier (compiled
`PreToolUse` hooks, today claude-only per rails-v1-implementation.md)
be projected into codex homes with the same refusal semantics? Method:
scratch `CODEX_HOME` dirs under the session scratchpad
(`codexgates-spike/`), real `codex exec` and real `codex-acp` ACP
sessions, a real gate denying `git reset` — the mirror of the claude
gate test. `~/.codex` was only read (auth.json copied into the scratch
home; verified byte-identical to the source afterward — no credential
rotation occurred). No repo, no `~/.tightbeam*`, no launchd, nothing
outside the scratchpad was touched.

## Verdict

**WORKS — with one mandatory caveat.** Codex ≥0.144 has a
Claude-compatible `PreToolUse` hook surface that deterministically
refuses matching tool calls before execution, surfaces the statute text
to the model as the denial reason, and binds under full-access/bypass
permission modes. The hook config is byte-compatible with what
`Rails.claude_settings/0` already compiles — same `{"hooks":
{"PreToolUse": [{"matcher", "hooks": [{"type": "command", ...}]}]}}`
map, same `sh -c` payload, same exit-2-plus-stderr protocol, same
`tool_name`/`tool_input` stdin JSON including the tool name **"Bash"**
for shell. The caveat: codex gates hooks behind a per-hook-hash TRUST
review (interactive TUI ceremony); untrusted hooks are **silently
skipped** in headless runs — fail-open. The only working headless
seeding is the trust-bypass override: `--dangerously-bypass-hook-trust`
on the CLI, or (production path) the `bypass_hook_trust: true`
thread-config override delivered through codex-acp's `CODEX_CONFIG`
env var. Config-file seeding does NOT work (proven below).

Per-property verdicts:

| Property | Verdict |
|---|---|
| (a) Config file/format in a projected home | WORKS — `$CODEX_HOME/hooks.json`, claude-shape `hooks` map |
| (b) PreToolUse fires headless; exit 2 refuses; message surfaced | WORKS |
| (c) Binds under danger-full-access / agent-full-access | WORKS — stdin reports `permission_mode: "bypassPermissions"` and the block still lands |
| (d) Trust gating; exact seeding | WORKS-WITH-CAVEATS — bypass override required; silently fail-open without it |

## (a) Where hooks live and what they look like

Codex reads hooks from `$CODEX_HOME/hooks.json` (also: inline `[hooks]`
in `config.toml`, project `.codex/hooks.json` when the project layer is
trusted, and plugin-bundled `hooks/hooks.json` — all load additively;
docs: developers.openai.com/codex/config-advanced#hooks, redirecting to
learn.chatgpt.com/docs/hooks). For projection, `hooks.json` at the home
root is the fit: one whole file, owned by the substrate, delivered via
`extra_files`, never rewritten by codex (verified: after all runs codex
had written its own `config.toml`, sqlite state, and `sessions/` into
the home, but `hooks.json` was untouched).

The exact file used, verbatim — note the payload is the byte-identical
compiled command shape from `rails-v1-implementation.md` §Compilation,
wrapped in the same top-level `"hooks"` key claude's settings.json
uses:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "sh -c 'grep -qE \"git (reset|stash|rebase|checkout \\\\.|restore|clean)\" - || exit 0; echo \"[gate: no-history-rewrites] History-rewriting git commands are forbidden here: other agents may have uncommitted work in this tree.\" >&2; exit 2'"
          }
        ]
      }
    ]
  }
}
```

Schema deltas vs claude (from docs + binary-embedded JSON schema):
`timeout` is seconds (default 600); `statusMessage` (optional UI
label) and `commandWindows` exist; `type: "command"` is the only
handler type. None of these are needed for gates. Event vocabulary in
the binary: PreToolUse, PermissionRequest, PostToolUse, PreCompact,
PostCompact, SessionStart, UserPromptSubmit, SubagentStart,
SubagentStop, Stop — Stop/SubagentStop have the claude "exit 2 =
continuation prompt" semantics per binary strings, relevant to a future
block tier only.

## (b) It fires, it refuses, the model reads the law

Headless run (danger-full-access), verbatim from stderr transcript
(`run2-bypass.err` in the spike dir):

```
$ CODEX_HOME=$SPIKE/home codex exec --sandbox danger-full-access \
    --skip-git-repo-check --dangerously-bypass-hook-trust -C $SPIKE/work \
    'Run the exact command `git reset --hard HEAD` ...'

hook: PreToolUse
ERROR codex_core::tools::router: error=Command blocked by PreToolUse hook: [gate: no-history-rewrites] History-rewriting git commands are forbidden here: other agents may have uncommitted work in this tree.. Command: git reset --hard HEAD
hook: PreToolUse Blocked
codex
Command blocked by PreToolUse hook: [gate: no-history-rewrites] History-rewriting git commands are forbidden here: other agents may have uncommitted work in this tree.. Command: git reset --hard HEAD
```

The action never executed; the model's final answer quoted the statute
text verbatim — law learned by hitting it. The refusal envelope is
`Command blocked by PreToolUse hook: <stderr>. Command: <command>`
(slightly different dressing than claude's, same one sanctioned
emission). Codex requires non-empty stderr on exit 2 ("PreToolUse hook
exited with code 2 but did not write a blocking reason to stderr" is a
hook error) — rails always emits the statute text, so this never
bites.

Allow path + matcher scoping, one turn (`run7-matcher.err`): with
`matcher: "Bash"`, `git status --short` fired the hook and passed
(`hook: PreToolUse Completed`, command executed), then
`git reset --hard HEAD` was blocked. Matcher semantics are claude's:
regex over `tool_name`, empty/omitted matches all.

The hook's stdin, captured verbatim by a tee hook — Claude-compatible
wire, including the tool name:

```json
{"session_id":"019f7ed2-...","turn_id":"019f7ed2-...","transcript_path":".../home/sessions/2026/07/20/rollout-....jsonl","cwd":".../codexgates-spike/work","hook_event_name":"PreToolUse","model":"gpt-5.6-sol","permission_mode":"bypassPermissions","tool_name":"Bash","tool_input":{"command":"git reset --hard HEAD"},"tool_use_id":"exec-..."}
```

Consequences: (1) a statute's `tool = "Bash"` matches BOTH harnesses —
no tool-name translation layer; (2) grep-over-raw-stdin-JSON works
unmodified, same caveat about JSON-escaped `"` characters; (3) the
compiled hook entry maps can be shared byte-for-byte between claude
settings.json and codex hooks.json.

## (c) Binds under bypassed permissions

Every blocking run above used `--sandbox danger-full-access`
(`approval: never`); stdin showed `permission_mode:
"bypassPermissions"`. The production path was proven separately over
ACP: a scripted driver (`acp-driver.mjs`) spoke ndjson JSON-RPC to the
same `codex-acp` binary tightbeam launches, with `CODEX_HOME` pointing
at the scratch home — initialize → session/new → `session/set_mode
{modeId: "agent-full-access"}` (exactly `Tightbeam.Acp.Adapter`'s codex
yolo mode) → session/prompt. The hook fired, the reset was refused, and
the agent_message_chunk stream carried the statute text back verbatim.
Same property we proved for claude: gates bind even when permissions
are bypassed, because PreToolUse sits in the tool router, not the
approval system.

## (d) Trust — the mandatory seeding

Codex reviews non-managed hooks per hook hash in an interactive TUI
ceremony ("Hooks need review" / "Trust all and continue" / "Continue
without trusting (hooks won't run)"). Headless, an untrusted hook is
**silently skipped — no warning, no refusal, the guarded action simply
executes** (proven: run1 and run3 ran `git reset --hard` with the gate
configured but untrusted). This is the failure mode to engineer
against: a projection bug here is INVISIBLE ungating.

What was tested for seeding:

| Mechanism | Result |
|---|---|
| `--dangerously-bypass-hook-trust` CLI flag on `codex exec` | WORKS (run2; run4 proves no `[features]` toggle needed — hooks are on by default in 0.144.6) |
| `bypass_hook_trust = true` in home `config.toml` | DOES NOT WORK — silently skipped (run5) |
| `codex exec -c bypass_hook_trust=true` | DOES NOT WORK — silently skipped (run6) |
| `CODEX_CONFIG='{"bypass_hook_trust":true}'` env on codex-acp | WORKS (ACP run — the production path) |
| Seeding the persisted trust store directly | NOT VIABLE — store location never surfaced in home files across all runs; no CLI writer found; only the TUI ceremony writes it |

Why the env path works: `codex-acp` spawns `codex app-server` with
fixed argv but reads `CODEX_CONFIG` (JSON) from its environment and
spreads it into every `thread/start`/`thread/resume` `config` override
map (verified in the bundled codex-acp source: `createSessionConfig`
merges `this.config` from `CODEX_CONFIG`); the app-server accepts
`bypass_hook_trust` as a boolean thread-config override (binary string:
"`bypass_hook_trust` override must be a boolean"). Codex prints a
stderr warning per invocation ("Enabled hooks may run without review
for this invocation") — harness stderr only, zero bytes of model
context.

**The exact seeding for a projected codex home** is therefore not in
the home at all — it is one adapter-process env var:

```
CODEX_CONFIG={"bypass_hook_trust":true}
```

set where placement already assembles adapter env. Security posture:
the bypass makes codex run ANY hooks.json in that home without review.
Acceptable here by construction — the home is substrate-projected,
`hooks.json` is written only by tightbeam from operator-authored
statutes, and the flag's own warning ("intended only for automation
that already vets hook sources") describes tightbeam exactly. It is
scoped per adapter process, never global, and touches no operator
`~/.codex`.

## Additional facts for the projection spec

- Escaping: the settings.json compiled command string from rails.ex was
  embedded in hooks.json UNCHANGED (JSON encoding supplies the same
  layer claude's settings.json does) and the torture-adjacent pattern
  (`checkout \\.` — double-escaped backslash) survived to grep intact.
  One compiler, two delivery vehicles.
- Remote quoting hazard (satellites): the remote adapter command line
  is `ssh ... exec env K=V ...` and ssh re-parses argv remotely; a bare
  `CODEX_CONFIG={"bypass_hook_trust":true}` loses its double quotes to
  the remote shell and codex-acp's `JSON.parse` then throws. The value
  must ride single-quoted on the remote command line (placement's
  existing `shell_quote` discipline).
- Version floor: all of this requires codex ≥0.144 on the EXECUTING
  host. An older codex ignores hooks.json entirely — silently ungated,
  fail-open. There is no in-band refusal to detect this; the honest
  posture is a harness-support-matrix note plus whatever version
  attestation spinup grows later.
- Codex mutates its home (`config.toml` with personality and per-cwd
  `projects` trust, sqlite state, `sessions/`) but never `hooks.json`;
  the manifest hash gate is undisturbed.
- `codex exec` inherits stdin and blocks reading it when the parent
  leaves it open ("Reading additional input from stdin...") —
  spike-harness note only; codex-acp is unaffected.
- Auth: the scratch home used a COPY of `~/.codex/auth.json`; after all
  runs it remained byte-identical to the source (no rotation
  occurred, nothing written back).

## Artifacts

All runs, configs, wire logs, and captures are preserved in the session
scratchpad `codexgates-spike/` dir: `home/` (the scratch CODEX_HOME
with hooks.json), `run1-no-bypass.*` through `run7-matcher.*`,
`acp-driver.mjs`, `acp-wire.log`, `pretooluse-capture.jsonl`. The
scratchpad is session-scoped and disposable; everything needed to
re-run is quoted verbatim above.
