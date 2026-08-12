# Containment v1 — Nesting Spike Report

Run: 2026-07-19 on **eezo** (real Mac, Darwin 25.5.0 / macOS 26.5.2,
Apple Silicon). Executes the spike required by
`containment-v1.md` §"The nesting spike". Time-boxed ~1h active work.

## Verdict

| Harness | Adapter (pinned) | Internal-sandbox-disable switch | Under OUTER `sandbox-exec` wall | Verdict |
|---|---|---|---|---|
| **claude** | `@agentclientprotocol/claude-agent-acp` 0.59.0 (Claude Agent SDK, in-process) | ACP session mode `bypassPermissions` | Real turn + agent shell tool-use succeeds; escape write blocked | **WORKS** |
| **codex** | `@agentclientprotocol/codex-acp` 1.1.4 | ACP session mode `agent-full-access` (→ codex `danger-full-access`) | Real turn + agent shell tool-use succeeds; escape write blocked | **WORKS** (caveat: network) |

**RECOMMENDATION: PASS → the containment build is UNBLOCKED.** Both v1
harnesses run turns, execute real tool calls (shell), and are gated by
the outer Seatbelt wall with each harness's internal sandbox disabled.
No `FAIL-UGLY` nesting EPERM was observed on either harness. The macOS
story does NOT have to stay "process-groups-only" — the Seatbelt GATING
composite from `containment-v1.md` §MACOS HOSTS is viable.

The single caveat is not a containment failure but a network-posture
fact (below): a harness that makes DIRECT provider API calls needs
egress, so the spec's "network loopback-only / gateway-only" posture
requires the gateway to proxy model calls.

## How it was driven (no gateway involved)

Adapters were driven DIRECTLY over ACP stdio (ndjson JSON-RPC 2.0) by a
small client (`scratchpad/spike/driver.mjs`): `initialize` →
`session/new` → `session/set_mode <yolo>` → `session/prompt`. The
adapter process was spawned wrapped in `/usr/bin/sandbox-exec -f
<profile> node <adapter/dist/index.js>`; the driver ran unsandboxed and
spoke JSON-RPC over the sandboxed child's stdio. The prompt forced
AGENT-SIDE shell tool use (`printf … > hello.txt ; cat hello.txt`) so
the file write happens INSIDE the sandboxed process — exercising the
wall against the harness's own tool, not a client-side `fs/*` shortcut.

Binaries used (canonical, exactly what tightbeam ships — resolved from
`tightbeam/dist/acp/presets.js`):
`/Users/mike/src/tightbeam/node_modules/@agentclientprotocol/{claude-agent-acp,codex-acp}/dist/index.js`.

Credentials: env passthrough only, no copies.
- claude: `CLAUDE_CODE_OAUTH_TOKEN` read from
  `~/.tightbeam-beam/auth/claude/oauth-token`; `CLAUDE_CONFIG_DIR` → a
  fresh scratch home.
- codex: `CODEX_HOME` → a scratch home whose `auth.json` is a **symlink**
  (pointer, not a copy) to `~/.codex/auth.json`; minimal scratch
  `config.toml` (chatgpt auth, `gpt-5.6-sol`, low effort).

## Internal-sandbox-disable switch per harness (discovered)

From `tightbeam/dist/acp/presets.js` (`yoloModeId`) and confirmed against
each adapter's advertised `session/new` modes:

- **claude** available modes: `auto, default, acceptEdits, plan, dontAsk,
  bypassPermissions`. Disable switch = **`bypassPermissions`** (set via
  `session/set_mode`). The Claude Agent SDK runs in-process and does not
  wrap tool exec in a nested `sandbox_apply`, so there is no inner
  Seatbelt to collide with the outer wall; `bypassPermissions` removes
  the per-tool permission prompts so turns run unattended.
- **codex** available modes: `read-only, agent, agent-full-access`.
  Disable switch = **`agent-full-access`**, which the adapter maps to
  codex core's `danger-full-access` (string present verbatim in
  `codex-acp/dist/index.js`). This is the mode that skips codex's own
  Seatbelt (`sandbox_apply`) — the documented nesting blocker.

## Every denial encountered and its resolution

The outer profile was built deny-default from the start with the
well-known macOS runtime baseline pre-included (`file-read*`,
`process-exec`/`fork`, `mach-lookup`, `sysctl-read`), so the only
denials seen were the load-bearing FS-write paths and the intentional
gating tests. Denials were surfaced as `EPERM`/"Operation not permitted"
in tool output and adapter stderr.

1. **codex, scratch-only writes** → WORKS. Codex needed no writes outside
   the session workdir for the task. (profile `fsgate-strict.sb`)
2. **claude, scratch-only writes** → `session/new` returns an
   undefined `sessionId` (SDK swallows the underlying write EPERM); the
   session never initializes.
   **Resolution:** allow `file-write*` to **`/dev`** — the SDK allocates
   a PTY under `/dev` during session creation.
3. **claude, scratch + `/dev`** → `session/new` OK, but the Terminal tool
   fails: `EPERM: operation not permitted, mkdir '…'`. The tool creates a
   per-command working directory under the system temp.
   **Resolution:** allow `file-write*` to **`/private/tmp`**. (TMPDIR
   `/private/var/folders` alone did NOT satisfy it; `/private/tmp` did.)
4. **claude, scratch + `/dev` + `/private/tmp`** → WORKS end to end
   (`hello.txt` = `contained`).

Both harnesses then pass under one **unified** profile
(`fsgate-unified.sb`): codex tolerates the claude superset trivially.

## Gating proof (the payoff — wall vs. the agent's own tool)

With internal sandboxing DISABLED (so the OUTER wall is the sole layer),
each harness was told to write OUTSIDE the workdir (`printf pwned >
$HOME/…`):

- **codex** (`agent-full-access`): tool failed —
  `/bin/bash: /Users/mike/…: Operation not permitted`; file absent.
- **claude** (`bypassPermissions`): Terminal tool failed; agent reported
  "sandboxed to the current working directory … blocked from writing to
  `/Users/mike/`"; file absent.

The outer Seatbelt wall contains the harness's own tool execution even
with the harness's internal sandbox off. This is the exact property
`containment-v1.md` requires ("even a custody-escapee stays gated").

## Nesting nuance (recorded)

The spec's premise is that an outer profile makes an inner
`sandbox_apply` fail with `EPERM`. On this build that hard failure was
**not** reproduced: codex run in `agent` mode (workspace-write, internal
sandbox nominally ON) under the outer wall still completed the turn — it
gated via ACP permission prompts, not via a nested Seatbelt that blew
up. This does not change the recommendation: `agent-full-access` is the
correct, spec-aligned config and works cleanly. If a future codex build
reintroduces a hard nested `sandbox_apply`, `agent-full-access` already
avoids it. Do not rely on workspace-write nesting "happening to work."

## Network posture

- **Outbound-open + FS-gated** (`fsgate-*` functional variant): both
  harnesses run real turns. This is what the spike validated.
- **Loopback-only** (`fsgate-loopback.sb`): FS gating identical; codex's
  turn fails at the provider request —
  `stream disconnected … failed to lookup address information` /
  `error sending request for url (https://chatgpt.com/backend-api/codex/responses)`.
  The wall demonstrably restricts network, but a harness making DIRECT
  provider calls cannot reach the model under loopback-only. Consequence
  for the build: the production "gateway-only" posture means model API
  calls must be **proxied through the gateway on loopback** (or the
  provider host explicitly allowed). This is a design choice for the
  implementation spec, not a containment blocker.

## Minimum working profile (verbatim)

Unified, harness-agnostic, **functional (network-open)** variant. Replace
the first `subpath` with the per-session workdir at placement time;
switch the network stanza per the posture chosen (see below).

```scheme
(version 1)
(deny default)

;; read anywhere: materials, dyld, adapter code, caches, creds-via-symlink
(allow file-read*)

;; writes: deny-by-default; only the session scratch tree + PTY + temp
(allow file-write*
  (subpath "<SESSION_WORKDIR>")   ;; e.g. the placement scratch/workdir
  (subpath "/private/tmp")        ;; claude Terminal per-command workdir
  (subpath "/dev"))               ;; claude session-new PTY allocation

;; process lifecycle: exec node + shell/codex child, fork
(allow process-fork)
(allow process-exec)
(allow signal (target self))

;; macOS runtime baseline (dyld/malloc/etc — not the research question)
(allow mach-lookup)
(allow sysctl-read)

;; network — pick ONE posture:
(allow network-outbound)                          ;; open egress (works)
;; (allow network-outbound (remote ip "localhost:*"))  ;; loopback-only:
;;   gateway must proxy model calls, else the turn cannot reach the provider
```

Per-harness true minimums (subset of the above):
- **codex**: scratch-only writes are sufficient (`/dev` + `/private/tmp`
  not required for its shell path).
- **claude**: requires scratch + `/dev` + `/private/tmp`.

## Artifacts (all under the session scratchpad)

`…/scratchpad/spike/`
- `driver.mjs` — the ACP stdio client / sandbox wrapper.
- `profiles/` — `fsgate-v1.sb` (baseline), `fsgate-strict.sb`
  (codex min), `fsgate-claude-tmp.sb` == `fsgate-unified.sb`
  (both-harness min), `fsgate-loopback.sb` (network-gated).
- `logs/` — control, sandboxed, escape, loopback, and per-profile runs
  for both harnesses (18 logs).

Nothing was written outside the scratchpad except this report. The
running gateway (:11373), `~/.tightbeam*`, repo checkouts, and launchd
were not touched. No credential files were copied.
