# Codex gates v1 — gate projection for codex homes (implementation spec)

Status: DRAFT r5 (r4 round: two residual stale-text refs corrected — the probe-model reference at ~519 now cites the pinned gpt-5.6-sol[medium], and the historical queued-caller summary at ~39 now matches the accurate timeout-or-exit wording). r4 was: DRAFT r4. r3 → r4 (2026-07-20): FINDING 1 — pins the probe
MODEL to a codex model resolved by the Gateway's codex fallback
(`gpt-5.6-sol[medium]`), never `config.default_model` (claude's fable);
Placement resolves NO per-archetype codex model, so the r3 "archetype's
configured codex model" source was wrong (§Part 2 Probe opts). FINDING 2
— corrects the queued-caller claim: callers may TIME OUT on their own
shorter `GenServer.call` budget OR EXIT with the stopping server;
neither is a graceful reply (§Part 3 step 5). Framing-symmetry pass so
codex reads as a peer, not second-class: the non-malicious bar is a
property of the RAILS TIER on BOTH harnesses (claude rails are equally
non-hermetic); codex's hook engine is described on its OWN terms
(neither harness is the reference); and the gate row is a tightbeam-side
◐ᵗ wiring gap this spec closes, not a codex deficiency (matrix
reality-audited 2026-07-20, codex has zero true vendor-✖ rows).
r2 → r3 (2026-07-20): applies Flynn's ruling that
resolves the r2 adversarial review (3 critical, 1 high, 2 medium). THE
BAR IS "WORKS FOR AGENTS WITH NON-MALICIOUS INTENT." Codex gates are
RAILS, not a security boundary — exactly like Claude rails, and never
hermetic. The r2 review's three CRITICALs (probe cwd config ≠ a real
workdir's project layer; a spoofable marker plus a `hooks.json` swap
under an unchanged manifest stamp; no containment backstop) EVERY ONE
requires a malicious or config-hostile actor — one who edits the home,
plants a project/plugin hook, fakes the marker, or rewrites the seed.
Under this bar those are OUT OF SCOPE: not defended against, and stated
as such rather than papered over. Spawn attestation is RETAINED but
DOWNGRADED from "tamper-proof enforcement proof" to an OPERATIONAL
WIRING-CHECK — its job is catching the SILENT MISCONFIG (missing/wrong
bypass seed, a too-old codex, an absent/unparseable hook file, hooks
switched off at spawn) that would let a COOPERATIVE agent run ungated
and flail into a forbidden command; it is NOT spoof-proof and never
claims to be. The containment wall is NO LONGER cited as a security
backstop — it is unbuilt at main and not the point; codex-gates stands
alone and does not depend on it. r2's real defects ARE fixed: the
wiring-check deadline is pinned as ONE absolute 120s budget across the
whole ACP request sequence with kill-on-deadline (HIGH 4); the
tamper-recovery step is corrected to change manifest BYTES, not mtime
(MEDIUM 5); the queued-caller claim is corrected to the truth — during a stalled
wiring-check callers may TIME OUT on their own shorter GenServer.call
budget (knows_session? 5s, new/load 30s, all < the 120s deadline) OR
EXIT with the stopping adapter; either is an exit crash, never a
graceful {:error, :adapter_unavailable} (MEDIUM 6).
History: r1 → r2 (2026-07-20) applied the r1 review (2 critical, 2
high, 2 medium, 2 low) plus three second-spike deltas.

Grounded in codex-gates-spike-report.md (spike run 2026-07-20 on eezo,
codex-cli 0.144.6 — read it first; every delivery mechanism below was
proven live there) plus a second independent two-machine replication
whose deltas are folded in below. Parent: rails-v1-implementation.md
defines the gate tier and remains sole authority for statute schema,
validation, and the compiled command shape — this spec changes none of
those; it ADDS exactly one substrate-reserved constant gate (the
wiring-check probe, §Part 3) compiled by the same compiler. Bible
§rails binds: rails never add guidance; a gate is deterministic
refusal only, and the statute text reaches the model solely as the
denial reason at fire time.

The one-sentence change: a gate statute, today compiled into a Claude
`PreToolUse` hook only, is now ALSO delivered to codex homes — same
compiled bytes, different vehicle — and a codex adapter refuses to
serve unless a boot-time WIRING-CHECK observes the hook engine refuse a
known-blocked probe command, so a silently misconfigured gate becomes a
visible refusal-to-boot instead of a healthy-looking ungated session.

Repo: `~/src/tightbeam_ex`. Gate: `mix compile --warnings-as-errors`
clean and `mix test` fully green. Match existing moduledoc voice; never
touch code unrelated to this spec.

## Security posture — the bar, and what the matrix mark means (read before implementing)

THE BAR IS "WORKS FOR AGENTS WITH NON-MALICIOUS INTENT." This bar is a
property of the RAILS TIER ITSELF on EVERY harness — not a codex
limitation. A rails-tier gate is deterministic denial of ENUMERATED
tool calls, built for a cooperative-but-forgetful agent hitting a known
footgun (`git reset` in a shared tree, `git push` to main). On NEITHER
harness is it a hermetic sandbox, and this spec must never be
summarized as one. Claude rails are EQUALLY non-hermetic: anyone who
can edit a Claude home — its settings.json hook — or shell out past the
tool defeats them exactly as an in-home codex actor defeats the codex
gate; the non-hermetic property is symmetric, and codex is not uniquely
limited by it. The gate is a `PreToolUse` refusal an ordinary agent
will not step around, and an agent bent on defeating it always can — on
BOTH harnesses, identically. Precisely what is and is NOT in scope:

- IN SCOPE — the cooperative agent: the compiled gate refuses the
  enumerated Bash command pre-execution, and the boot wiring-check
  proves the gate is actually wired before any session is served. That
  is the whole product: a forgetful-but-honest agent cannot blunder
  past `git reset`.
- OUT OF SCOPE — the malicious or config-hostile actor (NOT defended
  against, by ruling): an operator or agent that rewrites its own
  reachable config, swaps `hooks.json` under an unchanged manifest
  stamp (Homes does not re-verify projected files when the stamp
  matches — homes.ex `project/2`), plants a project/plugin `hooks.json`
  or a `.codex/config.toml`, disables hooks in a trusted project layer
  (`[features] hooks = false`), fabricates the probe marker instead of
  running the command, or runs effects through a subprocess outside the
  enumerated tool. Codex loads hooks ADDITIVELY from home, project, and
  plugin sources and codex-acp marks the session cwd/roots trusted
  (`createSessionConfig`, dist/index.js:26151); under
  `agent-full-access` a determined in-home/in-project actor can always
  get around a rails-tier gate. This is IDENTICAL to Claude's rails
  posture (an agent that edits its own settings.json or shells out
  defeats Claude gates too), and it is accepted, not closed here.
- What the wiring-check IS (§Part 3): an OPERATIONAL boot check, not a
  tamper proof. It drives the reserved probe gate through a throwaway
  session and requires the refusal marker. Its job is to catch the
  SILENT MISCONFIG that would otherwise ungate a COOPERATIVE agent
  invisibly — an ineffective/absent trust seed, a too-old
  codex-acp-selected executable that ignores hooks.json, an
  absent/unparseable projected `hooks.json`, hooks switched off at
  spawn. Any of these produces a healthy-looking session that silently
  runs ungated; the wiring-check converts them into a fail-closed boot
  refusal. That is its entire remit.
- What the wiring-check is NOT: it is NOT spoof-resistant and does not
  claim to be. The PASS marker is model-visible text, not authenticated
  hook provenance; a probe-only `hooks.json` swapped under an unchanged
  stamp, a planted home/plugin hook that refuses only the sentinel, or
  a model that fabricates the marker all defeat it — and all require
  the malicious/config-hostile actor that is out of scope. The check
  runs at an empty probe cwd and therefore validates only the
  cwd-INDEPENDENT wiring (home `hooks.json`, the trust seed, the
  executable's enforcement); it cannot and does not validate a real
  session's per-workdir project layer, because a workdir that disables
  hooks is a config-hostile input, out of scope. The mark means
  "wiring proven at boot," never "cannot be circumvented."
- Hook-source restriction was investigated and does NOT exist in a
  usable form: codex has no home-only hook-loading mode. The only
  source restrictions are `[features] hooks = false` (kills ALL hooks,
  including ours) and `allow_managed_hooks_only` in a root-owned,
  machine-global `/etc/codex` requirements.toml — which skips user,
  project, session, AND plugin sources, i.e. it would skip the
  projected home `hooks.json` too. Neither hardens the residual; it is
  documented as out-of-scope, not engineered against.
- The containment wall is NOT a dependency and NOT a security backstop
  for this spec. It is unbuilt at main, defaults off, and does not
  bound these bypasses; r2's "the wall backstops the residual" claim is
  RETRACTED. The wall is a FUTURE hermetic layer aimed at a DIFFERENT
  threat model (an untrusted/malicious agent, kernel-enforced effect
  denial); codex-gates neither invokes it nor leans on it, and this
  spec ships and stands on its own.
- Two distinct bypass properties, never conflated: Claude's proven
  property is that PreToolUse fires under PERMISSION bypass
  (`bypassPermissions`). Codex shares that property AND adds an
  orthogonal HOOK-TRUST layer with no Claude analog; gating
  additionally hangs on the trust seed (§Part 2). Spec, moduledoc, and
  matrix language must keep these separate — "same bypass-mode
  immunity" was an r1 overclaim.

## Why this is now possible (spike findings, condensed)

Codex has its OWN native `PreToolUse` hook engine — described here on
its own terms, since neither harness is the reference. It reads
`$CODEX_HOME/hooks.json`, whose top-level map shape (`{"hooks":
{"PreToolUse": [{"matcher", "hooks": [{"type": "command",
"command"}]}]}}`) and stdin tool-call field names (INCLUDING
`tool_name: "Bash"` for shell) COINCIDE with what claude's settings.json
independently carries — which is precisely why the substrate's ONE
compiled map (§Part 1) serves both vehicles unchanged, not because
either harness copies the other. The hook receives the tool-call JSON
on stdin; exit 0 allows, exit 2 with stderr refuses the call
pre-execution and surfaces the stderr text to the model (`Command
blocked by PreToolUse hook: <text>. Command: <cmd>`); and the hook
binds under `agent-full-access` (`permission_mode: "bypassPermissions"`).
Because the stdin wire coincides and every v1 statute targets tool
`"Bash"`, the compiled hook entries are shared byte-for-byte — the
parity claim is scoped to Bash-tool statutes (the only kind shipped law
contains); non-Bash tool coverage differs between harnesses and is
unproven.

Version floor, stated precisely: hooks were INTRODUCED in codex
0.124.0; 0.144.x is the TESTED/SUPPORTED floor (every spike run). The
floor applies to the executable codex-acp actually selects — its
BUNDLED `@openai/codex` (0.144.5 checked in via codex-acp 1.1.4; the
`^0.144.4` dependency floats), or a `CODEX_PATH` override when set —
NOT necessarily the host CLI, and spinup's satellite install is an
unpinned `npm install @agentclientprotocol/codex-acp` (spinup.ex
`ensure_remote_adapter`). No static version probe is built; instead
the boot wiring-check (§Part 3) makes ANY executable that fails to
enforce the gate — too old, too new with a hook regression, or
overridden — fail closed at boot. (A version too NEW with a
hook-behavior change is a codex-vendor risk the check catches, not
a defended threat.)

Second-spike deltas, all binding on this spec:

- PreToolUse is DENY-ONLY in 0.144.x: the binary REJECTS
  `permissionDecision` allow/ask and `updatedInput` as unsupported
  (the vendor docs overclaim allow/rewrite). Deny gates — this spec —
  are unaffected; a future block/check tier needing allow or rewrite
  has no surface today. Recorded in the harness-support future-tiers
  row (§Matrix).
- The bypass-trust warning surfaces as an app-server "warning"
  NOTIFICATION per thread (codex-acp maps it to a config-warning
  session update), in addition to stderr. Benign: the adapter must
  treat it as noise — never a boot or turn failure, zero
  model-context bytes.
- `codex exec` HANGS reading an open stdin ("Reading additional input
  from stdin..."): every smoke/test script that invokes `codex exec`
  MUST redirect `</dev/null`.
- `codex app-server` REJECTS `--dangerously-bypass-hook-trust` argv,
  so the `CODEX_CONFIG` env override is the ONLY production trust
  lever — confirming the r1 seeding choice.

The mandatory caveat stands and is EXACTLY the silent misconfig the
wiring-check exists to catch: codex trust-gates hooks (per-hook-hash
review, an interactive TUI ceremony), and an UNTRUSTED hook is
SILENTLY SKIPPED headless — fail-open, no warning, the guarded action
executes. The only production-viable seeding, proven over the real
codex-acp ACP path, is the `bypass_hook_trust` thread-config override
delivered through codex-acp's `CODEX_CONFIG` env var. Config.toml and
`-c` seeding were proven NOT to work; do not use them. The wiring-check
exists because this failure mode is invisible without it — a
cooperative agent would otherwise run believed-gated, actually-ungated.

## Scope

Changes exactly these files:

- `lib/tightbeam/rails.ex` — function rename, moduledoc + `@doc`
  rewrite, probe-entry constant.
- `lib/tightbeam/placement.ex` — codex extra_files + adapter env +
  probe opts.
- `lib/tightbeam/acp/adapter.ex` — boot wiring-check in the boot
  continuation, with the absolute-deadline budget (§Part 3).
- `lib/tightbeam/archetypes.ex` — `@builtin_harness_matrix` codex
  rails bullet (the builtin `tightbeam-harnesses` skill IS this
  constant; r1's "no such skill exists" was wrong).
- `docs/statutes.toml.example` — header line update.
- `docs/SMOKE.md` — §9 rails goes per-harness; codex stops being the
  negative control; codex live-gate + wiring-check steps added.
- `test/rails_test.exs`, `test/placement_test.exs`,
  `test/acp_adapter_test.exs`, `test/archetypes_test.exs`.

Plus, same change set (harness-support maintenance rule 1):
`shared-workspace/shared/specs/tightbeam/harness-support.md` — the
gate-statutes row AND the future-tiers row (§Matrix below).

Non-goals (do not build): block/check tiers, Stop-hook semantics,
PermissionRequest hooks, static version probing (the wiring-check
subsumes it), plugin delivery of hooks, any statute schema change, any
advisory text anywhere, reserved-name validation for the probe statute
(the name is reserved by convention; a colliding org statute is
harmless — its own gate still fires under its own name),
continuous/mid-session re-checking (rails-tier boundary), any defense
against a malicious or config-hostile actor (out of scope by ruling —
marker spoofing, stamp-preserving `hooks.json` swap, project/plugin
hook injection, mid-session hook disabling), any dependency on the
containment wall, and any claude-side wiring-check (claude has no trust
layer; its hook rides settings.json unconditionally).

## Part 1 — Rails: one compiler, harness-neutral name

Rename `Rails.claude_settings/0` to `Rails.hook_settings/0`. Same
contract: `nil` for an empty statute set, else
`%{"hooks" => %{"PreToolUse" => [entries in load order]}}`. No change
to validation, compilation, escaping, or the entry shape — the existing
byte-pinned tests keep passing modulo the call rename. The claude-
specific name is now a lie (the map is the shared compiled artifact);
the bible's honest-naming discipline says fix it at the moment it
becomes one. The function's `@doc` ("The Claude settings hook map…")
is rewritten harness-neutral in the same edit — the compiled PreToolUse
hook map, embedded in claude settings.json and codex hooks.json — so
the public contract does not keep the stale claim.

Add `Rails.probe_entry/0`: a public zero-arity function returning the
compiled PreToolUse entry for the substrate-reserved wiring-check gate,
built by the SAME entry compiler (`pre_tool_use_entry/1`) from a
module-attribute statute constant pinned exactly as:

- name: `tightbeam-probe`
- tool: `Bash` (matcher `"Bash"`)
- pattern: `tightbeam-gate-probe`
- text: `Spawn wiring-check probe command; always refused by design.`

The sentinel command `tightbeam-gate-probe` is benign by construction:
it is not a real binary, so even a total gate failure during a probe
executes nothing (a shell "command not found" at worst). The statute
name is reserved by convention, not validation (§Non-goals). The probe
entry rides ONLY the codex vehicle (§Part 2) — it never enters
`hook_settings/0`, so claude artifacts are byte-identical to today.

Rewrite the moduledoc paragraph that begins "Codex has no hook surface"
— it is now false. Replace with the facts, in the module's voice:

- Codex (hooks since 0.124.0; 0.144.x tested floor, applied to the
  codex-acp-selected executable) has the same `PreToolUse` surface;
  the identical hook map is delivered to codex homes as `hooks.json`
  (claude embeds it in settings.json). Same stdin wire, `tool_name`
  "Bash" on both — parity scoped to Bash-tool statutes — same exit-2
  refusal, and the same permission-bypass immunity (hooks fire under
  `agent-full-access` / `bypassPermissions`).
- DISTINCT from permission bypass, codex adds a hook-TRUST layer with
  no claude analog: untrusted hooks are silently skipped headless, so
  placement seeds the documented trust bypass
  (`CODEX_CONFIG={"bypass_hook_trust":true}`) on codex adapter
  processes whenever statutes exist. The home is substrate-projected
  and `hooks.json` substrate-written — the "already vetted" automation
  the bypass exists for.
- Because both the seed and the hook file can silently fail to bind,
  codex enforcement is never assumed: the adapter runs a boot
  wiring-check by driving the reserved probe gate (`probe_entry/0`) and
  requiring the refusal, failing the boot otherwise. Gates on codex are
  rails-tier for a cooperative agent — enumerated-call denial, wired
  proven at boot; a malicious or config-hostile actor is out of scope,
  exactly as for claude rails.

Keep the existing honest-limit prose about accident-grade pattern
matching; it applies unchanged to both harnesses.

## Part 2 — Placement: delivery and seeding

### hooks.json into codex homes

In `projection_spec/6`, the codex branch gains the rails file. Pinned
behavior:

- `harness == :claude`: EXACTLY today's behavior — `hook_settings/0`
  merged with model settings into `extra_files["settings.json"]`. No
  probe entry, no new bytes, ever.
- `harness == :codex`: when `Rails.hook_settings()` is non-nil,
  `extra_files["hooks.json"]` is `JSON.encode!` of that map with
  `Rails.probe_entry()` APPENDED to the `"PreToolUse"` list (probe
  last — org law fires under its own names first). When nil, no key,
  no file, no probe — an org without law projects a codex home
  byte-identical to today (manifest-hash stability preserved), and a
  lawless org is never wiring-checked because there is nothing to
  check. `model_settings(:codex, ...)` stays nil; codex homes still get
  no settings.json.

All entries — org statutes and the probe alike — come from the one
entry compiler in rails.ex and the one `JSON.encode!` call, so the
compiled command strings (including the escaping torture cases already
pinned in rails tests) are shared with the claude artifact verbatim.
The ONLY codex-specific step is appending one shared-compiled entry at
the encoding site; no codex-specific compilation or escaping path
exists.

Because extra_files ride the projection manifest, the first deploy with
statutes regenerates each codex home once (identity change, visible
context-reset markers), and every statute change regenerates codex
homes exactly as it does claude homes — a law change is an identity
change, both harnesses, no special casing.

### Trust seeding on the adapter process

In `adapter_opts/2`, when `harness == :codex` AND
`Rails.hook_settings()` is non-nil, add the env var; when nil, add
nothing (env byte-identical to today — parity with "no statutes → no
file"):

- Local branch — one more Port env pair, exact value pinned:
  `{"CODEX_CONFIG", ~s({"bypass_hook_trust":true})}`.
- Remote branch — one more `remote_env` entry. The remote command line
  is `ssh ... exec env K=V ...` and ssh JOINS argv for the remote
  shell to RE-PARSE (placement already documents this trap): a bare
  `CODEX_CONFIG={"bypass_hook_trust":true}` loses its double quotes
  remotely and codex-acp's JSON.parse throws, failing the adapter
  start. The entry must therefore carry its own single quotes, exact
  string pinned:
  `CODEX_CONFIG='{"bypass_hook_trust":true}'`.

Mechanism (state at the call site in one comment, or in the moduledoc
list of remote-env tricks): codex-acp reads `CODEX_CONFIG` (JSON) from
its environment and spreads it into every `thread/start` /
`thread/resume` config override map, where the app-server honors
`bypass_hook_trust` as a boolean override; codex emits a warning per
invocation on stderr AND as a per-thread app-server notification
(codex-acp: config-warning session update) — both harness-side noise,
zero model-context bytes, never treated as failure. This is the ONLY
seeding that works headless — config.toml and `-c` overrides are
proven no-ops for trust, `codex app-server` rejects the
`--dangerously-bypass-hook-trust` flag outright, and the persisted
trust store has no writable seam (spike §d).

If tightbeam ever sets `CODEX_CONFIG` for another purpose, the values
must merge into one JSON object — a second exporter must extend this
one, not add a duplicate env entry — and the merged value must then be
derived through placement's existing shell-quoting discipline
(`shell_quote`) rather than extending the hand-pinned single-quote
literal, which is only safe for exactly today's quote-free value.
Today there is exactly one exporter and the pinned literal stands.

### Probe opts

When `harness == :codex` AND `Rails.hook_settings()` is non-nil,
`adapter_opts/2` also pins two opts for the wiring-check (§Part 3):

- `probe_cwd`: `Path.join(base_dir, "work/gate-probe")` (the host's
  base_dir for remote adapters — a remote path string, same as `home`).
- `probe_model`: a CODEX model, pinned to the SAME codex fallback the
  Gateway applies to a modelless codex spawn — the literal
  `"gpt-5.6-sol[medium]"` (gateway.ex `create_spawn`). Pinned rationale,
  because r3 got the source wrong: Placement resolves NO session model.
  The adapter key is `{harness, identity_name, host}` (no model) and
  `adapter_opts/2` sees NEITHER the archetype NOR the per-spawn
  `p[:model]`; session models resolve PER SPAWN at the Gateway
  (`p[:model]` → `archetype.defaults[:model]` → the harness fallback,
  where codex → `gpt-5.6-sol[medium]`, gateway.ex `create_spawn`). So
  the r3 claim "the archetype's configured codex model, what placement
  already resolves for real sessions" was wrong on both counts —
  placement resolves no model, and the builtin archetype carries none.
  Do NOT source the probe model from `config.default_model` /
  `defaults.model`: that is `fable`, a CLAUDE model, and the probe runs
  on the codex executable where fable is not a valid codex model. The
  probe only needs SOME valid codex model to exercise the shared (env,
  home, executable) wiring; per-spawn model overrides do not and need
  not reach this shared adapter's boot probe (the adapter is one process
  keyed independently of any single spawn's model). This literal MUST
  track the Gateway's codex fallback as a single source — if that
  fallback value moves, this moves with it; do not fork a divergent
  second literal.

`work/<digest>` is already the session-workdir convention
(gateway.ex `session_workdir/2`), and `Placement.ensure_workdir/4`
already creates such dirs locally and over ssh — reuse that seam. The
opts-building fun (which already does the expensive home-delivery
work) RECREATES `probe_cwd` empty on every boot: remove it (local
`File.rm_rf!`; remote `rm -rf` over the same remote-command path),
then `ensure_workdir`. This is ordinary hygiene — it makes the
wiring-check reflect the projected HOME's wiring rather than stale
residue from a prior probe run; it is not a defense against a planted
project hook (that is a config-hostile input, out of scope). Claude
adapters and lawless orgs get neither opt.

## Part 3 — Boot wiring-check: the gate is proven wired, not presumed

Placement: `Tightbeam.Acp.Adapter`'s boot continuation
(`handle_continue`), immediately AFTER the ACP initialize handshake
succeeds and BEFORE the adapter answers any queued call. When the opts
carry `probe_cwd` (codex + statutes, per Part 2), the adapter runs the
wiring-check; otherwise boot is unchanged.

The wiring-check is an OPERATIONAL boot check, not a tamper proof
(§Security posture): it confirms the gate is WIRED for the exact (env,
home, executable) triple every real session on that adapter shares. It
assumes a cooperative model AT PROBE TIME and does not resist spoofing.

Mechanism, pinned:

1. `session/new` at `probe_cwd` with `probe_model`, no MCP servers —
   the adapter's normal session machinery, yolo mode and model-apply
   rules included. The probe session is throwaway: never registered,
   never served, never loaded; its bytes never reach any real
   session's context.
2. One prompt turn, text pinned: `Run exactly this command with your
   shell tool, then stop: tightbeam-gate-probe`.
3. PASS iff the turn's update stream (agent_message_chunk text or
   tool_call content) contains the marker `[gate: tightbeam-probe]` —
   the refusal envelope codex emits when the hook fires (`Command
   blocked by PreToolUse hook: [gate: tightbeam-probe] …`). A
   cooperative model attempts the command and the wired hook produces
   the marker; a marker present therefore proves the gate is wired. It
   is a substring match against the harness's OWN refusal envelope
   during a substrate-owned probe turn — a wiring observation, not
   interpretation of agent content (T1 untouched), and not
   authenticated provenance (a fabricated marker defeats it — out of
   scope).
4. ONE ABSOLUTE DEADLINE (pin 120 seconds), fail-closed (HIGH 4 fix).
   Because `Conn.request/4` uses INDEPENDENT per-request timers
   (default 60s each, and a timed-out pending entry is retained,
   conn.ex) they do NOT compose: session creation, model application,
   mode setting, prompt, and stream consumption would otherwise each
   get its own 60s and a hung check could run minutes. The adapter
   therefore records ONE monotonic deadline at wiring-check entry
   (`System.monotonic_time(:millisecond) + 120_000`) and:
   - before each ACP request computes `remaining = deadline - now`; if
     `remaining <= 0` it stops immediately with
     `{:gate_attestation_failed, :deadline}`; otherwise it passes
     `timeout: remaining` to `Conn.request/4` so no per-request timer
     can outlast the global budget;
   - bounds the prompt-turn stream wait by the same deadline (an armed
     `Process.send_after(self(), :gate_attestation_deadline, remaining)`
     whose message stops the boot);
   - on the deadline the adapter STOPS regardless of any pending Conn
     request (KILL-ON-DEADLINE) — it never waits for a hung request to
     eventually return, and the dying adapter tears the Conn (and its
     retained pending entries) down with it.
5. FAIL — marker absent when the turn completes, a turn/ACP error, or
   the absolute deadline expired: the adapter STOPS with a named error
   (`{:gate_attestation_failed, detail}`, `detail` ∈ {`:no_marker`,
   `:turn_error`, `:deadline`}), logging the collected probe output to
   the adapter stderr log. Fail-closed behavior, exact and total: the
   coordinator returns a spawned PID before boot readiness and treats
   the adapter as ready ONLY on `{:adapter_ready, key}`
   (adapter_coordinator.ex — boot is LAZY); an adapter that stops
   before signaling ready never becomes ready, its `:DOWN` drives the
   coordinator's uniform backoff → circuit accounting, and NO codex
   session is served for that adapter key while the check fails. Every
   retry re-runs the wiring-check. HONEST caller behavior (MEDIUM 6,
   sharpened r4): real-session calls that queued behind
   `handle_continue` never receive a graceful adapter-unavailable
   reply — but the FAILURE MODE is NOT uniformly "exit with the dying
   GenServer," because the adapter's own `GenServer.call` timeouts are
   SHORTER than the 120s wiring-check budget. `knows_session?` uses the
   default 5s, `new_session`/`load_session` use 30s (adapter.ex). So a
   caller queued behind a stalled 120s check will usually TIME OUT
   FIRST: its `GenServer.call` raises the standard `:timeout` exit well
   before the adapter reaches its deadline and stops. A caller whose
   timeout OUTLASTS the remaining check (or the deadline-stop) instead
   EXITS with the stopping `GenServer`. Either way the caller crashes
   with an exit — a `:timeout` exit or a stopped-server exit — never a
   clean `{:error, :adapter_unavailable}`. The guarantee is "no ungated
   session ever serves," not "a clean error to every queued caller." An
   org with statutes and a broken codex gate path loses codex service,
   never law.
6. On PASS the adapter logs one line naming the wiring-check and the
   marker (the durable per-boot evidence SMOKE cites), discards the
   probe session, and proceeds to serve.

What this proves, at boot, for the exact (env, home, executable) triple
every real session on that adapter shares: `hooks.json` present and
parseable in the projected home; the trust seed delivered and
effective; the codex-acp-selected executable actually enforcing
PreToolUse (subsuming the version floor); no spawn-time hook kill
switch in effect for the probe's config. What it does NOT prove
(§Security posture, out of scope): tamper-resistance of any kind — a
`hooks.json` swapped under an unchanged stamp, a planted home/plugin
hook, a real workdir's project layer that disables hooks, a fabricated
marker, or anything after spawn. Cost: one model turn per codex adapter
boot, on the pinned codex probe model (`gpt-5.6-sol[medium]`, §Part 2 —
never the archetype's per-spawn model or the claude `fable` default) —
accepted as the price of never
serving a believed-gated, actually-ungated session to a cooperative
agent.

## Part 4 — `docs/statutes.toml.example`

In the 4-line header, replace the "gates are claude-only today" line
with: gates run on both harnesses for non-malicious agents — claude via
settings.json hooks; codex via projected hooks.json, wiring-checked at
adapter boot (hooks exist since codex 0.124, tested floor 0.144.x on
the codex-acp-bundled binary; a codex that fails the boot wiring-check
refuses to serve rather than running ungated). The other three lines
(copy destination, restart to apply, statute change regenerates homes
with visible session-memory loss) stand.

## Part 5 — builtin skill and SMOKE

### `tightbeam-harnesses` (archetypes.ex)

The skill is the compiled-in `@builtin_harness_matrix` constant —
maintained law, bound by harness-support maintenance rule 1. Replace
the codex "Rails gates: NOT YET WIRED here…" bullet with, in the
constant's voice: Rails gates ENFORCED FOR NON-MALICIOUS AGENTS — the
same compiled PreToolUse hooks as claude, delivered as `hooks.json`,
and WIRING-CHECKED at adapter spawn (the substrate proves a probe
command is refused before serving sessions; a codex adapter that cannot
prove it does not come up). The refusal envelope reads `Command blocked
by PreToolUse hook: [gate: <name>] …` — the runtime acting, not the
model declining. Rails-tier: enumerated-call denial for a
cooperative-but-forgetful agent; NOT a sandbox and NOT tamper-proof —
a malicious or config-hostile actor is out of scope, exactly as for
claude rails. Update the claude bullet not at all.

### docs/SMOKE.md

§9 rails stops being [claude-only] and codex stops being the negative
control:

- The per-harness annotation for §9 becomes [divergent]: claude
  asserts hooks in `settings.json`; codex asserts `hooks.json` (org
  entries + the trailing `tightbeam-probe` entry), still NO
  settings.json in the codex home, AGENTS.md statute-free.
- Step 17 gains the codex arm: after gateway restart, the codex home's
  `hooks.json` decodes with one entry per statute plus the probe entry
  last.
- Step 19 (live refusal) gains the codex arm: same forbidden command
  through a real codex session; PASS quotes the codex refusal envelope
  `Command blocked by PreToolUse hook: [gate: no-history-rewrites] …`
  pre-execution.
- New codex-only step: boot wiring-check evidence — the codex
  adapter's boot log for the run contains the wiring-check PASS line;
  then break the gate deliberately (delete `hooks.json`) and restart:
  the adapter must REFUSE to boot with `gate_attestation_failed` and
  no codex session may be served — fail-closed proven live for the
  silent-misconfig case. RESTORE correctly (MEDIUM 5 fix): touching a
  file does NOT regenerate the home — `Homes.project/2` regenerates
  only when the manifest bytes differ from the stamp
  (`File.read(stamp_path) != {:ok, manifest}`) and extra_files are
  content-hashed into the manifest, so an mtime change is a no-op.
  Restore by changing manifest bytes — EDIT a statute (its bytes flow
  into the `hooks.json` content hash and thus the manifest), or DELETE
  the `.tightbeam-manifest` stamp file in the home (making the read
  mismatch) — either forces the full delete-and-reproject that rewrites
  `hooks.json`. This is a wiring-check demonstration, NOT a
  tamper-resistance test: deleting `hooks.json` is the silent-misconfig
  the check is for, not an adversary the spec claims to stop.
- Runbook note, binding on all smoke scripts: every `codex exec`
  invocation redirects `</dev/null` (open stdin hangs it).

This reproducible smoke, plus the per-boot wiring-check log line, is
the durable acceptance evidence replacing the (session-scoped, now
gone) spike artifacts — the mechanism claims stay quoted verbatim in
the spike report, but enforcement evidence is regenerated on demand,
never trusted from narrative.

## Invariants (acceptance lens)

1. Rails never add guidance — projected AGENTS.md for an org WITH
   statutes is byte-identical to one WITHOUT, exactly as the existing
   claude invariant test pins for CLAUDE.md. Nothing in this change
   writes a byte into any instruction file; the probe is a gate, not
   guidance, and its text reaches a model only as a refusal reason.
2. No statutes → no artifacts: no hooks.json, no probe entry, no
   CODEX_CONFIG, no probe opts, no wiring-check, codex manifest hash
   identical to a no-rails world. Lawless ≠ ungated: an org without
   law is byte-identical to today on BOTH harnesses and boots without
   probing.
3. One compiler: every hook entry — org statutes and the probe — is
   compiled by the same rails entry compiler and encoded by the same
   `JSON.encode!`. The only codex-specific step is appending the
   probe entry at the encoding site; no codex-specific escaping,
   pattern, or command path exists to drift.
4. Claude behavior is byte-identical to before this change (settings
   merge, model pin, no probe entry, everything).
5. The refusal is the only emission: statute text reaches the codex
   model solely inside the harness's block message at fire time.
6. Fail-closed wiring-check: a codex adapter for an org WITH statutes
   either logs a live wiring-check PASS at boot (within the 120s
   absolute deadline) or serves no sessions. The matrix mark asserts
   exactly this — "wired, proven at boot, for a non-malicious agent" —
   and nothing stronger; it does NOT assert tamper-resistance.

## Tests (cover every clause)

rails_test.exs:
1. Existing suite passes with the rename (`hook_settings/0`); the
   byte-pinned example-statute map and escaping torture pins are
   unchanged in content.
2. `probe_entry/0`: byte-pinned compiled entry — matcher "Bash", the
   `sh -c` payload greps `tightbeam-gate-probe` and emits
   `[gate: tightbeam-probe] Spawn wiring-check probe command; always
   refused by design.` on exit 2 — proving it rides the same compiler
   (same shape as the example-statute pin).

placement_test.exs:
3. Codex home, statutes present (example statute): `hooks.json`
   exists, bytes == `JSON.encode!` of `Rails.hook_settings()` with
   `Rails.probe_entry()` appended to the PreToolUse list (probe LAST);
   contains the org entry with `matcher` "Bash"; AGENTS.md contains no
   statute text and is byte-identical to the no-statute projection.
   (This REVERSES rails-v1's "codex home has neither" integration
   assertion — that reversal is authorized here and the old assertion
   must be updated, not duplicated.)
4. Codex home, no statutes: no hooks.json; manifest bytes identical to
   a no-rails world.
5. Claude home, statutes present: settings.json exactly as before the
   change (byte-pinned against the current expected value; explicitly
   assert NO probe entry).
6. `adapter_opts` local codex with statutes: env includes exactly
   `{"CODEX_CONFIG", ~s({"bypass_hook_trust":true})}`; opts include
   `probe_cwd` == base_dir/work/gate-probe and `probe_model` == the
   Gateway's codex fallback (`"gpt-5.6-sol[medium]"`) — explicitly NOT
   `config.default_model`/`fable`; without statutes: no CODEX_CONFIG
   key, no probe opts.
7. `adapter_opts` remote codex with statutes (injected `:sh` runner):
   the ssh argv contains the exact single-quoted entry
   `CODEX_CONFIG='{"bypass_hook_trust":true}'`; without statutes it is
   absent; claude adapters never carry it nor probe opts.
8. Probe-cwd hygiene: the opts fun recreates `probe_cwd` empty (a
   pre-planted file under it is gone after opts building).
9. Statute content change → codex manifest bytes change (regeneration
   trigger) — assert via `Homes.manifest_bytes/1` on the two specs.
   This also pins the MEDIUM 5 recovery mechanism: a statute-byte
   change is what forces the home to regenerate.

acp_adapter_test.exs (extend the existing fake-harness script, which
already streams scripted session/update chunks):
10. Wiring-check PASS: with probe opts, boot sends the pinned probe
    prompt to a new session at `probe_cwd`; when the fake streams a
    chunk containing `[gate: tightbeam-probe]`, boot completes and
    subsequent calls are served; the probe session is not registered.
11. Wiring-check FAIL (fail-closed): fake completes the probe turn
    WITHOUT the marker → the adapter stops with
    `{:gate_attestation_failed, :no_marker}` and no queued call is
    answered with a live session. Same fail-closed outcome on
    probe-turn error (`{:gate_attestation_failed, :turn_error}`).
12. Wiring-check DEADLINE (fail-closed, HIGH 4): the fake STALLS — it
    accepts the probe prompt but never streams the marker and never
    completes the turn. With the absolute deadline injectable/shortened
    for the test, the adapter stops with
    `{:gate_attestation_failed, :deadline}` within the budget (NOT
    waiting out multiple independent 60s Conn timers), and no queued
    call is answered with a live session.
13. No probe opts (claude, or codex without statutes) → no probe
    prompt is ever sent; boot is byte-identical to today's flow.

archetypes_test.exs:
14. The `tightbeam-harnesses` builtin skill text now states codex
    rails ENFORCED FOR NON-MALICIOUS AGENTS / wiring-checked at spawn
    and no longer contains "NOT YET WIRED" (update any existing pins of
    the old text).

## Matrix amendment (same change)

harness-support.md "Rails — gate statutes" row: codex ◐ᵗ → ✅
(ENFORCED FOR NON-MALICIOUS AGENTS). The current mark is ◐ᵗ, NOT plain
◐: the 2026-07-20 reality-audit of the matrix records codex with ZERO
true vendor-✖ rows, and this row's gap is TIGHTBEAM-SIDE (the vendor
hook surface EXISTS; tightbeam had simply not projected gates to codex
homes yet), not a codex deficiency — this spec closes exactly that
wiring gap and the mark advances to ✅. Mechanism note: projected
`hooks.json` (same compiled map as claude's settings.json, plus the
reserved `tightbeam-probe` entry) + `CODEX_CONFIG={"bypass_hook_trust":
true}` on the adapter process; enforcement WIRING-CHECKED at adapter
boot by a probe refusal within a 120s absolute deadline, FAIL-CLOSED
(no PASS → no codex sessions); refusal envelope "Command blocked by
PreToolUse hook: …". Rails-tier — enumerated Bash-call denial for a
cooperative-but-forgetful agent; the mark means "wired, proven at
boot," NOT "tamper-proof." A malicious or config-hostile actor
(stamp-preserving `hooks.json` swap, project/plugin hook injection,
mid-session hook disabling, fabricated marker) is OUT OF SCOPE — this
is the claude rails posture, not a sandbox, and does NOT depend on the
containment wall. Hooks since codex 0.124, tested floor 0.144.x applied
to the codex-acp-selected executable (bundled `@openai/codex`,
`CODEX_PATH` override aware) — floor violations fail the wiring-check,
never run silently ungated. Backed by: placement/adapter tests above +
SMOKE §9 codex arms + the per-boot wiring-check log line. Trim the
row's "projection design pending" prose; it is resolved.

"Rails — future block/check tiers" row: amend with the second-spike
fact — codex 0.144.x PreToolUse is DENY-ONLY (binary rejects
`permissionDecision` allow/ask and `updatedInput` as unsupported;
vendor docs overclaim allow/rewrite). A future tier needing
allow/ask/rewrite is vendor-blocked on codex today; deny-tier parity
is unaffected.

## Handoff

Gates: `mix compile --warnings-as-errors` clean; full `mix test`
green. Do not commit; leave the tree for review. The completion report
names the spike report (plus the folded second-spike deltas) as
evidence provenance and restates the security posture in one line: the
bar is agents with non-malicious intent — the matrix mark means a
rails-tier, boot-wiring-checked, fail-closed enumerated-call gate for a
cooperative agent, NOT a tamper-proof or hermetic boundary; a
malicious/config-hostile actor is out of scope by ruling and the
containment wall is not a dependency. If any instruction here conflicts
with the tree, another spec, or observed codex behavior, STOP and
report instead of improvising.
