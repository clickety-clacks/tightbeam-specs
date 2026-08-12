# Permission seam — spike

> RESOLVED 2026-07-23 — READ THE FINAL SECTIONS FIRST. This doc is an investigation
> LOG; its early verdicts (esp. "verdict C: seam unusable / codex hooks inert") are
> SUPERSEDED. Final conclusions, in the last three sections: (1) codex hooks WORK under
> app-server, config-only via `CODEX_CONFIG={"bypass_hook_trust":true}` — no patch, no
> fork, machine codex pinned by CODEX_PATH; PreToolUse fires + deny blocks, live-verified
> through the real adapter. (2) The PATH/ZDOTDIR shim is verified harness-independent
> defense-in-depth. (3) The claude `canUseTool` ask-mode lead is the only OPEN thread
> (feeds the future user-permission feature, nothing blocks on it). The narrative below
> is preserved for provenance — do not act on its interim verdicts.

Status: SPIKE (investigation + design, Flynn-directed 2026-07-22). Answer two questions
before any build: (1) can tightbeam enforce agent tool-use at the ACP permission seam
across all harnesses, replacing the per-harness hook layer? (2) how does tightbeam
support users who want permission prompts to BUBBLE UP to them instead of autonomous
execution? Output of the spike is a design decision + a lane plan, not code.

## Why this spike exists

The codex-gate saga established: harness hooks (claude PreToolUse, codex hooks) are
per-harness, version-fragile (codex 0.144.5→0.145.0 in two days, app-server hooks
inert), and NOT a stable enforcement surface. ACP is standardized (Zed reference impl).
`session/request_permission` flows through OUR adapter (conn.ex:180). If it carries the
tool call's command text, statute enforcement RELOCATES to one harness-independent
handler — and the same seam is exactly what a "prompt me" user wants surfaced.
Enforcement and user-consent are the SAME mechanism at different answer-sources.

## Investigation (the probe — do first, evidence to scratchpad)

Q-CAP (capability): for codex-acp 0.145 AND claude-acp, on a real adapter boot, capture
the full `session/request_permission` payload for a shell/terminal tool call. Does it
carry (a) command text, (b) tool identity, (c) a stable option set to answer with?
Cross-check the schema against Zed's reference (agent-client-protocol spec + zed source
— the reference impl for all ACP questions).

Q-BYPASS (the load-bearing unknown): our presets run bypassPermissions/yolo. Does each
harness STILL emit request_permission under bypass (so we answer it programmatically),
or does bypass SUPPRESS it? If suppressed, is there a preset short of full-bypass where
the adapter still RECEIVES every request and can auto-answer — i.e. can we get
"substrate decides every permission" WITHOUT handing the decision to a human each time?

Verdict shape: (A) both emit with command text under a usable preset → one seam gates
all harnesses; (B) split → seam for the harness that works, hooks for the other; (C)
neither → hooks-inert stands for codex.

## Findings — probe round 1 (coordinator, 2026-07-22)

Instrumented conn.ex:182 to dump session/request_permission; booted REAL codex-acp AND
claude-acp 0.145 adapters; ran a shell command in each. RESULT: under our OPERATIONAL
full-access/bypass presets, ZERO request_permission reached the adapter on EITHER
harness — the command just ran. So the seam is EMPTY for shell tools under autonomous
operation; gate-at-seam is NOT a drop-in hook replacement AS WE RUN TODAY.

INCONCLUSIVE (the load-bearing gap): the two non-bypass "ask mode" attempts are
UNVERIFIED — a set_mode override to on-request/default produced no mode-change
confirmation and the shell still ran unpermissioned. Cannot yet tell whether a
PROPERLY-APPLIED ask mode surfaces request_permission with command text. Notably: our
ACP `initialize` advertises only fs capabilities, NOT permission-handling — the bridges
may not delegate permission at all unless we advertise the capability.

RULING (Flynn 2026-07-22): DO THE DEEPER SPIKE before any codex-inertness decision.
Codex stays dark in the interim; hooks-inert is NOT ratified pending the spike.

## Deeper spike — questions to resolve (this is the real investigation)

S1. Does advertising a permission-handling capability in the ACP `initialize` handshake
    make codex-acp AND claude-acp DELEGATE tool permission to the client (us)? (Read
    Zed's reference for the capability schema + the intended handshake; test with our
    initialize amended.)
S2. Does `set_mode` actually change the harness mode (confirmable), and in a non-bypass
    mode do shell/terminal calls surface request_permission WITH command text?
S3. If the seam CAN be made to fire: does it fire for EVERY tool call (unconditional,
    hook-parity) or only some (trusted-tool escape = coverage gap)?
S4. Can we run "substrate answers every permission, auto-allow-unless-denied" WITHOUT
    surrendering autonomy — i.e. is there a mode where the harness always asks and we
    instantly auto-answer, giving hook-parity enforcement AND yolo-speed?
Outcome that matters: the three-level user permission model (ask-all/ask-mutations/yolo)
Flynn designed REQUIRES this seam to work for the ask-* levels — so S1-S4 gate the
user-facing feature, not just enforcement relocation. Resolve before building either.

## Design (pending the verdict — the parts that hold regardless)

### The permission mode is a global tightbeam switch — THREE levels
- ONE org-level setting, all harnesses/models uniform (Flynn: a global switch is right),
  three rungs from most to least oversight:
  - `ask-all` — bubble BOTH reads and mutations to the user; nothing runs unseen.
  - `ask-mutations` — auto-allow reads; bubble only calls that CHANGE state (file
    writes, state-changing shell, mutating verbs). The middle ground: see the
    consequential actions, not the noise.
  - `yolo` — auto-allow everything. The dark-factory default; hands-off.
- Default `yolo`. LAW ENFORCES AT ALL THREE: statutes evaluate at the seam and DENY
  (naming the statute) before the level is even consulted — a level only governs what
  happens to a call law has NOT already forbidden. So the ladder is "how much of the
  law-permitted surface do you want to see and approve," never "which law applies."
- read/mutate classification is the same split the assignment-as-capability rail uses
  (wisdom-consistent), so `ask-mutations` and that rail share one definition of mutate.

### Onboarding must ask, clearly
- Default is `auto`, but onboarding (tightbeam-onboarding skill) asks EARLY, in plain
  words, whether to switch to `ask`. The framing, honest about the tradeoff:
  "Your agents can run tools on their own — the default (yolo), fast and hands-off.
  Or they can check with you first: on every action that CHANGES something
  (ask-mutations), or on everything including reads (ask-all). Your org's safety rules
  still block forbidden actions at every level. Which fits how you want to work?"
- Record the choice in user.md; `ask`-mode users get told where approvals surface.

### Open design questions (resolve in the spike, with Flynn where marked)
- Granularity: RESOLVED — the three-level setting (ask-all / ask-mutations / yolo) IS
  the granularity; read/mutate split shared with assignment-as-capability. (Flynn.)
- allow-always: RESOLVED — persists per (USER, tool), survives across sessions (Flynn).
- Bubble timeout: an unanswered permission ask blocks the agent's turn — what deadline,
  and does it fail-closed (deny) or park? (Fail-closed to deny is the safe default.)
- Scope: RESOLVED — PER-USER (Flynn). A user's mode governs their own agents; the org's
  autonomous workers stay yolo. So the setting lives on the user, not org-wide.

## Non-goals
- Not building the enforcement relocation here — that is the lane the verdict authorizes.
- Not changing the constitutional rail (assignment-as-capability): that gates at the
  substrate verb layer regardless; this seam gates HARNESS tool-use, a different surface.
  They compose — both must pass.

## Findings — probe round 2, deeper spike (coordinator, 2026-07-22)

Method: throwaway worktree off main@66006fa, instrumented conn.ex to dump every
session/request_permission payload AND adapter set_mode to capture the modeId sent +
the bridge's response. Booted REAL codex-acp AND claude-acp 0.145 adapters and ran shell
commands under multiple, CONFIRMED-APPLIED modes. Evidence: scratchpad/perm-*.json,
mode-*.json, perm-*-out.log.

S2 — set_mode DOES apply (round-1 was invalid mode ids). Correct codex-acp mode ids are
`read-only` / `agent` / `agent-full-access` (NOT on-request/default — those are approval
POLICY values, from src/AgentMode.ts: ReadOnly & Agent → approvalPolicy "on-request",
AgentFullAccess → "never"). Correct claude-acp ids: default/acceptEdits/bypassPermissions/plan.
Every set_mode returned `{:ok, %{}}` (confirmed applied):
  - codex agent-full-access → echo ran, NO request_permission.
  - codex agent (approvalPolicy on-request) → echo ran, NO request_permission.
  - codex read-only (approval on-request, read-only sandbox) → echo ran, NO request_permission.
  - codex read-only + a WRITE (`touch`) → ran, NO request_permission.
  - claude bypassPermissions → ran, NO request_permission.
  - claude default (non-bypass, authenticated) → ran, NO request_permission.
In EVERY case the command executed and ZERO request_permission reached our adapter.

S1 — NOT capability-gated (RESOLVED, no test needed): codex-acp wires the approval handler
UNCONDITIONALLY — `new CodexApprovalHandler(connection, sessionState, signal)` (dist
index.js ~23980), with no clientCapabilities check; only the ELICITATION handler consumes
`this.clientCapabilities`. So advertising a permission capability in our ACP `initialize`
would NOT make the bridge start forwarding permission. The machinery
(CodexApprovalHandler.handleCommandExecution → session/request_permission) is always
present; it simply is not INVOKED for these commands.

S3 — WHY it doesn't fire = the trusted-command escape (the load-bearing finding):
codex only calls the approval handler when a command must ESCALATE beyond its
approval_policy/sandbox. `echo` (pure, non-mutating) and in-workspace writes do not
escalate, so codex auto-runs them in every mode. The seam therefore does NOT fire per
tool call — it is NOT hook-parity. Our rails gate specific patterns (e.g. `git stash`)
regardless of sandbox; codex will not ask for a command it deems non-escalating, so those
patterns run ungated at the seam. Claude behaves the same for ordinary Bash under default.

S4 — no "always-ask + auto-answer" mode: there is no tested mode where the harness asks
for EVERY command (which is what an auto-answer-after-statute-check enforcement or an
"ask-all" user level needs). Asking is bound to sandbox escalation, not universality.

VERDICT: **(C)** for the tested surface. The ACP permission seam is NOT a usable
hook-parity enforcement mechanism, and NOT a full "ask-all" mechanism, for either harness
as we integrate them today. Consequences:
- hooks-inert STANDS for codex (codex app-server runs no hooks AND the permission seam
  does not fire for the commands we gate).
- claude keeps its working settings.json PreToolUse hooks (those DO fire — unaffected).
- The three-level user permission model (ask-all / ask-mutations / yolo) CANNOT be
  delivered via the ACP permission seam as-integrated: the harnesses only ask on sandbox
  ESCALATION, not on every action, so "ask-all" is not reachable by mode-switching.

RESIDUAL (not blocking the verdict): I tested safe/in-workspace commands (echo, touch).
It is plausible the seam DOES fire for genuinely sandbox-escalating ops (network access,
out-of-workspace writes, destructive ops) — I did not run those (risk). If a future spike
wants "ask-mutations" specifically, the question narrows to: does read-only-sandbox mode +
an out-of-sandbox mutation reliably fire request_permission with a correlatable command,
and is that coverage enough for the product's mutation-gating intent? That is a bounded
follow-up, not a blocker for ratifying hooks-inert now.

## Reconciled verdict — two independent spikes (2026-07-22)

Coordinator (live instrumentation) + Fable's Sol (source read of both bridges) converge
on CODEX, DIVERGE on CLAUDE — and the divergence gates the user ask-mode feature.

CODEX (both agree): the approval handler is wired unconditionally, but codex only
invokes it when a command ESCALATES the sandbox; safe/in-workspace commands (incl. the
git patterns our C1 rails guard, under our full-access preset) auto-run and never reach
us. So the seam is a trusted-command escape, NOT hook-parity. + app-server runs no
hooks. => codex has NO ACP command-guard path as we run it.

CLAUDE (divergence): source read found `canUseTool` in claude-agent-acp — a permission
callback carrying `toolName` + `toolInput` (COMMAND TEXT) and returning
allow/deny/allow_always (which maps EXACTLY onto Flynn's ask-all/ask-mutations 3-level
model). BUT the coordinator's live test in `default` mode saw it NOT fire for a shell
command. Unresolved: does canUseTool forward to the ACP client (us) in a specific
non-bypass permissionMode, or does the bridge self-answer? This is ONE bounded test
(try acceptEdits / advertise permission handling; watch whether request_permission with
toolInput reaches conn.ex).

DECISIONS, separated:
1. CODEX ENFORCEMENT NOW: verdict C confirmed — hooks-inert is the honest interim
   (seam doesn't fire for our patterns; hooks don't run). Independent of #2.
2. ASK-MODE / uniform enforcement FUTURE: NOT closed. claude's canUseTool looks like
   the real seam for the 3-level model (command text + allow/deny/allow_always). Resolve
   the one canUseTool-forwarding test before building the permission feature; codex
   ask-mode would be limited to sandbox-escalating ops until OpenAI widens it.


## PATH-facade spike — codex CAN be wrapped (2026-07-22, live-verified)

Flynn's question: can we monkeypatch CLI calls so codex's shell commands hit OUR shim?
Answer: YES — verified end-to-end on codex 0.145.0.

Findings (three live probes, scratchpad/pathshim):
1. NAIVE PATH PREPEND FAILS where it matters. Codex's internal git spawns (rev-parse,
   status --porcelain) inherit our env and hit the shim, but AGENT commands run via
   **`/bin/zsh -lc`** (hardcoded login zsh) — the login profile chain (/etc/zprofile
   path_helper + user dotfiles) rebuilds PATH and the shim drops out.
2. THE COUNTER IS **ZDOTDIR**: point the spawned codex's ZDOTDIR at a tightbeam-owned
   dotdir whose .zshenv/.zprofile/.zlogin chain-source the user's real dotfiles and
   then PREPEND the shim dir — our prepend runs AFTER path_helper and user files, so
   it gets the last word.
3. VERIFIED: with the ZDOTDIR facade, `git stash` from the codex agent resolved to the
   shim, was DENIED with the statute message, exit 77 — and codex relayed the denial
   text to the model verbatim (teachable, hook-parity UX). `which git` reports the
   shim path.

Properties: no codex internals touched (robust to auto-updates of codex ITSELF, though
the `/bin/zsh -lc` invocation is codex behavior — re-probe per version like everything
else); env-injection only, per-session, nothing machine-global; harness-independent in
principle (any harness spawning login zsh gets the same treatment; claude keeps its
working hooks). LIMIT: absolute-path invocations (/usr/bin/git) bypass — this is
honest-agent rails, same trust tier hooks occupied; the sandbox remains containment.

Implementation notes for the lane:
- The shim must parse git argv properly (skip `-c k=v` global flags to find the
  subcommand) — codex's internal calls carry `-c core.hooksPath=... -c core.fsmonitor=
  false` prefixes and must pass through untouched unless the SUBCOMMAND is gated.
- Shim consults the same statute source the hooks did (fast, deterministic; no gateway
  round-trip needed for pattern statutes).
- Env (e.g. TIGHTBEAM_SHIM_LOG) propagates through fine — the shim can emit toward the
  substrate for total-emission legibility.

CONSEQUENCE FOR THE PARKED DECISION: hooks-inert ratification is now the WRONG framing.
The real choice is: build the shim lane (small: shim script + zdotdir template + adapter
env injection) and bring codex back GUARDED, vs. bring it back stamped-unguarded in the
interim. The enforcement gap that motivated hooks-inert is closable substrate-side.

CLAUDE TOO (2026-07-22, live-verified): the identical facade (PATH prepend + ZDOTDIR)
intercepts claude's agent shell commands as well — `git stash` denied with statute
message, exit 77, relayed to the model. Claude's INTERNAL git ops (status polling,
diffs) also traverse the shim, reconfirming the shim must gate on the parsed
SUBCOMMAND and pass everything else through. Net: ONE harness-independent enforcement
layer verified on both harnesses — claude gets defense-in-depth (hooks + shim), codex
gets its only command guard. (Probe set both PATH and ZDOTDIR; which one claude
strictly needs was not isolated — the lane ships both, so it doesn't matter.)


## FINAL REVERSAL — codex hooks WORK under app-server (2026-07-23, build+test verified)

The hooks-inert conclusion is REFUTED at rust-v0.145.0. A source spike + upstream's own
integration tests + a purpose-built PreToolUse test (real `codex app-server` child, mock
model, marker-file proof) established:
- Hooks execute under app-server via the SAME core engine as exec. The 0.144.x "zero
  hooks fire" live result was a version+trust artifact: codex-acp's BUNDLED binary
  (pre-CODEX_PATH pinning) + untrusted hook state + no bypass — discovery
  (hooks/src/engine/discovery.rs:566) filters untrusted handlers, so nothing fired.
- The ONLY gate is trust: `bypass_hook_trust` — NOT a config.toml key, NOT a CLI flag
  on the app-server subcommand — must arrive as a `thread/start` request `config`
  override (app-server/src/config_manager.rs:225).
- PreToolUse FIRES for shell commands (tool_name "Bash", full command text in
  tool_input.command); the deny protocol (stdout JSON permissionDecision:"deny")
  ACTUALLY BLOCKS execution, model receives the reason via
  FunctionCallError::RespondToModel (core/src/tools/registry.rs:490-533). Both shell
  and unified_exec emit PreToolUse (shell_command.rs:249, exec_command.rs:408);
  write_stdin correctly does not re-fire. SessionStart fires too. 11 events total;
  PreToolUse/PermissionRequest/PostToolUse/Stop/UserPromptSubmit can block or alter.
- Upstream main (44d76c6) is byte-identical on this mechanism — stable surface, no
  patch, no pinned fork, zero maintenance burden.

DELIVERY THROUGH OUR STACK (verified in codex-acp dist source): the bridge's
`CODEX_CONFIG` env var (JSON) is parsed at startup and SPREAD AS THE BASE of the
`config` map codex-acp sends on every thread/start & thread/resume
(createSessionConfig). So tightbeam's fix is ONE ENV VAR on the codex adapter spawn:
`CODEX_CONFIG={"bypass_hook_trust":true}` — the 0.144.x seed that was removed as
"dead" was the RIGHT mechanism pointed at the wrong binary. (The bin/codex shim's
`--dangerously-bypass-hook-trust` flag remains exec-only — harmless, insufficient.)

VERDICT REWRITE: codex enforcement = hooks (config-only revival) as the rails tier,
the PATH/ZDOTDIR shim as harness-independent defense-in-depth, the Seatbelt wall as
containment. hooks-inert ratification: DEAD — nothing to ratify. The claude canUseTool
ask-mode thread is unchanged (still the open lead for the user permission feature).


## Live adapter A/B + gate-detection fix (2026-07-23, real codex-acp boot)

Verified end-to-end through the REAL tightbeam adapter (not a bespoke driver), codex
0.145.0 pinned via CODEX_PATH, fixture home with the rails hooks.json:
- C (CODEX_PATH pin + CODEX_CONFIG={"bypass_hook_trust":true}): gate wiring-check PASS
  — the PreToolUse hook fired, BLOCKED `tightbeam-gate-probe`, marker surfaced.
- D (pin only, NO seed): gate FAIL — the probe command actually executed
  (`zsh: command not found: tightbeam-gate-probe`), hook filtered as untrusted, adapter
  fails closed and stops. The seed is precisely the arming switch; fail-closed intact.

GATE-DETECTION subtlety (load-bearing for future re-probes): the boot wiring-check
detects the block by finding the marker in the probe session's OUTPUT. A blocked
PreToolUse returns the reason to the model as a tool-call result; codex does NOT surface
the hook's stderr as agent text on its own. So the gate PROMPT must instruct the probe
model to report the refusal VERBATIM — otherwise the model just narrates and the marker
never appears, giving a false-negative (gate fails though hooks work). @gate_prompt was
updated to demand verbatim echo (matching the driver prompt that first proved the block).
This is fail-closed-safe either way: no firing hook => no refusal to echo => gate fails.
If a future codex version stops surfacing the block to the model at all, re-probe and
consider a model-independent signal (probe hook writes a marker file the adapter checks).
