# Cold-install e2e — shrdlu + tars (2026-08-14, in progress)

Status: RECORD (live run, Mike-directed). Both machines wiped of all prior
Tightbeam installs (pre-wipe forensics in session record; shrdlu carried
TWO installs — npm 0.1.7 + a source prodgate install with its own base;
tars carried npm 0.1.7 with a RUNNING gateway and a stale epmd from an
even older erts-16.2.1 vintage). Cold install per README from packages
built at main 63e3400 (linux on gibson; darwin on eezo). Both services
installed (systemd / LaunchDaemon per README), both providers onboarded
on both machines, agentic-engineering learned.

## Verified working end-to-end (real turns, cold org)

shrdlu claude leg: credential preflight; home projection; identity
status/edit/relearn/apply; facts-read; config; work-item/assign
round-trip; dispatch opens linked assignment (real turn); toplines board
live; **flagship reviewer-loop end-to-end** (blocked → reviewer assigned
→ verdict → completes); **owner escalation** (surrender →
decision-request → owner rules allow → proceeds). Codex credential
preflight passes after the workaround below.

## Findings bank

1. **README bootstrap defect**: the documented empty-org
   `tightbeam add-user <userId>` (flag-free) refuses with "identity
   required"; working form is self-identified `--as-user <userId>`.
   README or CLI must reconcile.
2. **PRODUCT BUG — codex catalog probe uses bare `codex`**
   (harness/codex.ex probe_script line 4 `raw=$(codex --version)`) where
   claude's probe uses absolute cli_path — dies 127 under the service's
   scrubbed shell env; CODEX_PATH is NOT consulted by the probe (only
   rails). Workaround on shrdlu: symlink into /usr/local/bin. Fix: probe
   should use the resolved cli path like claude's, honoring CODEX_PATH.
3. **First-spawn ACP adapter install exceeds the smoke's 30s curl
   deadline** on a cold base (tars observed; adapters completed after
   the check gave up). Cold-install-specific timing the smoke should
   accommodate or pre-warm.
4. **Smoke requires TIGHTBEAM_EFFORT_CHECKIN_HORIZON_MS=2500 on the
   gateway** — its own raise names it (good), README/docs don't; the
   knowledge previously lived only in a since-wiped drop-in. Documented
   drop-in/plist entries restored on both machines.
5. **Smoke is not idempotent against its own corpse**: a timed-out run
   leaves an in-flight turn that blocks identity-apply
   ("turn_in_progress") on rerun; gateway restart clears it.
6. **SMOKE DRIFT vs current ruleset**: the artifact-closure group expects
   denial chain ["completion-requires-review"]; main's engineering rules
   now deny code-review-requires-passing-tests first (the passing-tests
   rail post-dates the smoke's last live run). The deferred live smoke
   rotted while deferred — the deferral's own cost, measured. Fix card
   opened (smoke files tests-passed before review handoff).
7. **Build provenance**: ad-hoc darwin package (eezo) bundles erts-16.2.1
   (older OTP 28 patch) vs the repo pin 28.5/erts-16.4 — functional, but
   real releases must come from CI's pinned toolchain.
8. **RETRACTED then corrected (Mike's challenge, rows checked): no
   clawline client ever touched the e2e org** — devices table empty, no
   external connections; the 10 agent:main:clawline sessions are the
   SMOKE'S OWN spawns (its fixture product is named clawline), 9 retired
   cleanly. The REAL tars defect: the claude dispatch turn hangs
   pre-turn-row (sessions spawn, turns table stays empty, curl starves
   at 30s) under the LaunchDaemon context — under diagnosis. The
   integrator's original inference was pattern-matching on a name;
   the rows refuted it.

## Residual state

shrdlu: service active (drop-ins: smoke horizon, CODEX_PATH pin —
e2e-vintage, removable), /usr/local/bin/codex symlink (workaround for
finding 2). tars: service active with horizon in plist; clawline
entanglement pending ruling. Source clones at ~/src/tightbeam-e2e on
both (smoke harness). Sudo passwords for both boxes passed through this
session's transcript — rotate at e2e close.

## Findings 10-12 (2026-08-14 continued session)

10. **PRODUCT/DOCS — the README-mandated macOS LaunchDaemon cannot run
    claude turns.** Proven by controlled experiment: identical box, base
    dir, and smoke — dispatch hangs indefinitely (>120s, zero bytes, no
    session row) under the system-domain daemon, passes immediately
    under a foreground user-context gateway. Consistent with the four
    daemon-spawned `claude --version` probes found hung across boots.
    The README's macOS section needs a working alternative (user-domain
    service, or a documented incompatibility + supported form).
11. **Orphan gateway processes survive service teardown** — a
    pre-bootout gateway instance survived `launchctl bootout`, held the
    Erlang node name, and silently killed the next boot with a name
    collision (third node-name ghost of this e2e; shrdlu's wipe met the
    same class). Teardown guidance should include a process/epmd check.
12. **The smoke's own drift fix proven live on shrdlu**: 25/26 with the
    doubled-denial (nested remedy dispatch artifact) asserted exactly;
    codex leg ran real turns 12/13 under quota strain; the sole
    remaining miss is real-turn artifact-record compliance by the model
    — nondeterministic turn behavior, not harness plumbing. Also: the
    gibson `codex exec` quota exhaustion did NOT stop shrdlu's
    tightbeam codex turns — the two paths meter from different buckets
    (provider-capacity world-fact, CR-003 D8's sibling, observed live).

Residual tars state: gateway FOREGROUND in tmux (tb-fg) with the smoke
horizon — deliberate, because the documented daemon form cannot run
claude turns (finding 10); the LaunchDaemon plist remains installed but
booted out. Not a finished install per the README's own standard; ruling
needed on the macOS service form before tars can be called done.

## CLOSURE (2026-08-14)

Final tallies, fixed smoke (branch fix/smoke-gate-chain):
- **shrdlu** (systemd service): claude 13/13; codex 12/13. Sole miss:
  carrier-on-real-turn — the model did not perform its in-turn
  artifact-record.
- **tars** (foreground gateway per finding 10): claude 11+ passes to the
  codex boundary; codex (gpt-5.6-sol-wm after the catalog surfaced the
  sol quota exhaustion as a named model_unavailable with alternatives —
  the three duties working) 12/13, same sole miss.
- **Finding 13:** codex in-turn artifact-record compliance 0/2 across
  boxes vs claude 2/2 where reached — a model/prompt interaction in the
  smoke's carrier check, NOT install plumbing; investigate under the
  smoke card umbrella.

VERDICT: both cold installs FUNCTIONALLY PROVEN end to end — install,
service (with the macOS exception of finding 10), onboarding, learn,
real turns on both harnesses, reviewer loops, gate chains, escalations,
toplines. The long-deferred live-smoke ruling converts to SUBSTANTIALLY
DISCHARGED WITH ONE NAMED RESIDUAL (the codex carrier check); it does
NOT fully close — Phase 3 entry re-checks with the residual resolved.

Open rulings for Mike: (1) the macOS service form (finding 10);
(2) the Sol review-lane outage (wait to Aug 20 / credits / ruled
exception); (3) the §6 exception question (Sol-via-shrdlu-gateway);
(4) whether the smoke-fix and LIVESWITCH branches may land on branch
evidence + deferred review, or hold. Rotate both box sudo passwords
at your convenience (transcript exposure noted at the time).

## T2b — client journeys, shrdlu (2026-08-14, continued session)

Tier T2b of the runbook (`client-e2e-v1.md`, driver
`scripts/client_e2e.exs`) carried forward on shrdlu at main `63e3400`,
template `~/.tightbeam`, one throwaway gateway per leg.

**claude leg: PASS — every step, twice, on two independent runs.**
Boot, pair, converse, tool use (the `uname -s` placement proof), stream
create/rename/retire, cancel, queueing, concurrency, `/new`, `/compact`,
`/model`, model change (applied `claude-opus-5`), restart resilience
(pid 4025448 → 4027909, interrupted turn delivered, harness pointer
`loaded`), restart queue survival, wakes, scheduled wakes. 13c is
MANUAL by design (app-side footer assertion).

**codex leg: FAIL — OpenAI quota exhaustion, NOT a product defect.**
The adapter's start-up gate wiring-check fails 31 times, 0 passes, every
one identical: `gate wiring-check FAIL detail=turn_error output="You've
hit your usage limit. ... try again at Aug 20th, 2026 3:35 AM."` Same
account and same date as the Sol review-lane outage (open ruling 2). The
06:20 smoke ran codex 12/13 "under quota strain"; the shrdlu bucket has
since reached zero. T2b codex is BLOCKED until credits or Aug 20 — it is
not evidence against the product.

### Findings 14-17

14. **UNDECLARED PREREQUISITE — the client-e2e driver needs the Rust CLI
    built.** shrdlu's `~/src/tightbeam-e2e` had no `cli/target`, so each
    leg's provisioned `bin/tightbeam` was the refusal shim (exit 127).
    Every harness spawn goes through `bin/tightbeam harness-exec ... --
    <adapter>`, so NO adapter could ever start: `harness-processes/`
    stayed empty, no turn row was ever written, and the client starved at
    180s per step. This produced a full-red T2b scorecard at 08:34
    (13 FAIL / 2 PASS) that read as a product regression and was not one.
    `ci.yml` names the build a "suite prerequisite"; `client-e2e-v1.md`,
    `SMOKE.md`, `TEST-HOSTS.md`, the driver script and the `ClientE2E`
    modules mention it nowhere. Cost: 44 minutes of wall clock and a
    false FAIL verdict. Fix: the driver's preflight should refuse by name
    when the resolved CLI path does not exist, and the runbook should
    list the build.
15. **PRODUCT — readiness asserts a capability it has not proved.** The
    leg gateway logged the CLI-missing warning at 08:52:57 and declared
    `READY: claude on shrdlu can run turns` at 08:52:58. Readiness proves
    the credential and the catalog; it does not prove the spawn path,
    which was structurally impossible at that moment. Per "report dirt,
    never accommodate it", a gateway that cannot spawn should refuse
    loudly rather than report ready and let every turn time out.
16. **HARNESS — the leg's evidence self-destructs.** `gateway.log` and
    `adapter-*.stderr.log` (and the adapter `.gate.log`, which carries
    the verbatim gate verdict) live INSIDE the base dir that teardown
    removes by design. The 08:34 run therefore left nothing to diagnose.
    Bit twice: the first evidence mirror written for this session globbed
    `adapter-*.stderr.log`, which does not match `*.stderr.log.gate.log`,
    and lost the decisive artifact a second time. The driver should copy
    the leg's logs to a durable path before teardown.
17. **PRODUCT — the gate buries the harness's own reason.** The operator
    and the scorecard see `{:adapter_unavailable,
    "{:gate_attestation_failed, :turn_error}"}`, a generic name, while
    the true cause ("You've hit your usage limit ... Aug 20th") sits in
    the gate log's `output=` field, already in hand. Compare the model
    catalog, which surfaces the SAME underlying quota exhaustion as a
    named `model_unavailable` with alternatives (praised in finding 12).
    Same condition, two qualities of report; the adapter gate should
    carry the harness's message out the way the catalog does.

### Findings 18-19 (codex credential recovery attempt, 2026-08-14 18:20-18:50)

18. **PRODUCT/WEDGE — an open adapter circuit has no agent-reachable
    repair verb.** After the quota outage the codex circuit latched open
    at 705 consecutive failures. `AdapterCoordinator.adapter_for/2`
    returns `{:error, :degraded}` on `entry.circuit == :open` BEFORE
    reaching `start_adapter`, and only `{:adapter_ready, key, pid}` from
    a successful start closes it — so a latched circuit can never retry
    itself. No half-open probe, no cooldown. The CLI offers no reset
    (`harness-process` has only `list`), so recovery required an
    operator running `sudo systemctl restart tightbeam`. That is
    philosophy gate 3's wedge verbatim — "if repair requires an admin at
    a database console, the design is incomplete" — the same class as
    the completion-selection wedge (wi_1b0237fe). The substrate is right
    not to judge here; it simply left the org no lawful way out.
    PROVEN both directions: a fresh credential could not be tested until
    the restart, and after the restart the adapter started immediately
    (circuit closed, generation 2).
19. **PRODUCT — re-onboarding reports success while the runtime stays
    dead.** Both `tightbeam onboard openai` runs (api_key, then
    subscription) printed "Successfully logged in" and then
    `{:provider_runtime_start_failed, %{failed: [%{reason: :degraded,
    harness: "codex"}]}}`. That names neither the latched circuit nor
    its failure count, and does not tell the operator a restart is the
    fix. Same shape as finding 17.
20. **NOT A DEFECT, recorded so it is not re-derived: an OpenAI API key
    cannot substitute for the Codex subscription.** An `sk-proj-` key
    was onboarded (banked correctly as `credentialKind: api_key`) and
    validated live against `/v1/models` (HTTP 200) — but the models it
    offers are the standard API surface (gpt-4, gpt-3.5-turbo…), NOT the
    Codex-plan models the legs run (`gpt-5.6-sol-wm` et al). Codex CLI
    also never read `OPENAI_API_KEY` from the environment (401 "Missing
    bearer or basic authentication in header"). The credential was
    restored to `subscription` by device flow. Codex-plan quota and API
    billing are different meters; only the former unblocks the legs.

## T2b codex UNBLOCKED and run (2026-08-14 evening)

Root cause of the all-day codex block was NOT the product: the credential
Tightbeam banked was for a rate-limit-exhausted OpenAI account. Proven by
A/B on one machine, one minute apart, same `codex` binary: the system home
`~/.codex` (freshly onboarded to me@mikemanzano.com) ran a real turn
(3,330 tokens); Tightbeam's projected home returned "usage limit … Aug
20th". Clearing the projected home's cache changed nothing; replacing the
banked `auth.json` with the working one made codex green immediately
(gate wiring-check PASS, circuit closed, generation 1).

**Model note:** `gpt-5.6-sol-wm` is NOT offered on the new account;
plain `gpt-5.6-sol` is. The substrate handled this WELL — named
`:model_unavailable` precisely and the catalog offered live alternatives,
which is how the right model was found. Three duties working.

### Scorecard, codex@shrdlu on gpt-5.6-sol — 17 of 18

PASS: auth preflight, boot, pair, converse, tool use, create/rename/retire
stream, cancel, queueing, /new, /compact, /model, model change (applied
gpt-5.6-terra), restart resilience (pid 360465 → 364685, interrupted turn
delivered, pointer "loaded"), restart queue survival, wakes, scheduled
wakes. 13c MANUAL by design.

### Findings 21-22

21. **PRODUCT (EVIDENCED) — `tightbeam onboard openai` reports success
    but does NOT replace the banked credential.** THE ROOT CAUSE of the
    entire day's codex block. Three onboardings ran on shrdlu (18:21
    api_key, 19:37 subscription, 19:52 subscription), each printing
    "Successfully logged in". The credential still in the store after
    all three carried `last_refresh = 2026-08-14T02:41:43Z` — the
    ORIGINAL 02:41 onboarding (cf. `/tmp/onboard-openai.log`, mtime
    02:41). None of the three re-onboardings installed anything.
    Structural comparison (key names and null/non-null only, values
    never read) of the stale store credential vs the working
    `~/.codex/auth.json`: both `auth_mode=chatgpt`, both
    `OPENAI_API_KEY: null`, identical token shape
    (id_token/access_token/refresh_token/account_id). So NOT an API-key
    override, and NOT a different account — the operator confirms the
    same account throughout, and `~/.codex` proves the field tracks
    reality (`last_refresh = 19:47:15`, exactly its login time). The
    store file's mtime DID update while its content stayed at 02:41.
    Specimen preserved: `~/.tightbeam/auth/codex/auth.json.bak.<ts>`.
    **ROOT CAUSE FOUND — a credential-recovery DEADLOCK, and it is a 0.2
    REGRESSION.** In `finish_staged_onboard/4` (main): `install_staged!`
    writes the new credential to the store, then
    `activate_staged_credential` starts the provider runtime; when that
    start returns `:degraded` — which it always does while the adapter's
    circuit is latched open — `rollback_failed_finish/5` calls
    `restore_prior_state/3` and REVERTS the just-installed credential to
    the prior one. The cycle: exhausted credential → turns fail → 5
    failures latch the circuit → operator onboards a good credential →
    activation fails BECAUSE the circuit is open → rollback discards the
    good credential → still exhausted. **A working credential cannot be
    installed while the adapter is degraded, and the adapter is degraded
    because the credential does not work.** Compounds finding 18 (the
    latched circuit has no agent-reachable reset): restarting alone does
    not help either, because by then the credential has already been
    reverted, so the fresh adapter starts on the old one.
    VERSION EVIDENCE: `v0.1.7` contains ZERO occurrences of
    `finish_staged_onboard`/`rollback_failed_finish` — its finish path is
    a plain `with` that installs the credential and returns the error if
    `state.start` fails, LEAVING THE NEW CREDENTIAL IN PLACE. The build
    shrdlu runs (`63e3400`; its version string still reads 0.1.7 because
    the 0.2 line has not bumped) contains 5. The capture side
    (`onboard_openai/1`, `onboarding_staging_path/2`) is byte-identical
    across 0.1.5 / v0.1.7 / main and is NOT at fault; the rollback that
    discards the captured credential is new in 0.2. 0.1.x is unaffected.
    Finding 19 is this bug's front end, not a separate defect.
    **SEVERITY — the failure CORRELATES WITH NEED (gate 4).** A proactive
    swap (old credential still good, adapter healthy) succeeds: activation
    starts and nothing rolls back. A REACTIVE swap — expired, revoked,
    dead account, exhausted quota — is bricked, because the adapter has
    already been failing against the bad credential and the circuit is
    latched by the time the operator onboards. Nobody swaps a working
    credential, so the recovery path is broken exactly in the case it
    exists for, and it is self-reinforcing: the longer the bad credential
    sits, the more certain the latch. Provider-agnostic — the same
    `finish_staged_onboard` path serves anthropic, whose credentials also
    expire.
    **RULING (Mike, 2026-08-14): "we have no business adding security ON
    TOP of codex or claude logins."** The substrate stores what the
    operator gave it and reports VERBATIM what the vendor said when it
    was used; it holds no opinion about whether a vendor login is valid.
    The vendor owns that judgment and the only honest test is a real
    turn. Under this ruling the fix is DELETE the rollback, not classify
    or tune it — reverting an operator's explicit credential choice is
    the substrate adjudicating someone else's auth. Same lens condemns
    the `onboarded: true/false` metadata (a second opinion about a vendor
    login) and readiness-gating on the wiring-check verdict (recording it
    is right; withholding the adapter from it is judgment). NOT
    condemned: the backoff/circuit itself, which exists to stop hammering
    a dead process and spamming lifecycle events — a legitimate duty —
    but it must never gate INSTALLING a credential and it needs an
    agent-reachable reset (finding 18). Finding 17 is the same complaint
    from the other end: the vendor's real reason sat in the gate log
    while the substrate reported its own generic verdict.
    **RULING PART 2 (Mike, 2026-08-14) — the rollback is a SILENT-SPEND
    defect, not merely a recovery wedge.** A failed login leaves the
    operator with one mental model: "it failed, the system is stopped."
    They may have CHOSEN that — "I was running out of tokens anyway, I'll
    leave it logged out." The rollback silently restores the previous
    working credential and keeps running real turns against it: real
    money, on an account the operator believes is disconnected, with no
    signal anything is live. The substrate owes truth, and a state that
    contradicts the operator's model is a lie by omission — worse than a
    state that is merely broken. This also condemns the `onboarded`
    metadata harder: after a rollback the system reports a coherent
    onboarded state describing a credential the operator thinks they
    replaced. GENERAL PRINCIPLE: **credential operations fail CLOSED and
    VISIBLE.** A failed login leaves the system failed, because that is
    what the operator will believe happened. Accepted cost, explicitly:
    a bad login can now displace a working credential — recoverable by
    signing in again, and honest, which the alternative is not.
    FIX DIRECTION: activation failure must not roll back a credential the
    operator explicitly installed — an unstartable runtime is a separate
    condition from a bad credential, and conflating them makes recovery
    impossible. NOTE: codex is green only because the working credential
    was hand-placed into the store; the DOCUMENTED onboarding path is
    BROKEN and is the thing to fix.
22. **PRODUCT — J5 concurrency violates commit ordering under codex,
    REPRODUCIBLE 2/2.** Run 1: frames whose `seq` disagrees with the
    store row they carry, so the client cannot settle them into commit
    order (`c_sim_10_10 seq=23 store=25`, `seq=24 store=25`,
    sampled_together=true, intervals_overlapped=true). Run 2 (J0,J5
    subset): `Main's turns completed out of order: [c_sim_2_2, c_sim_2_2,
    c_sim_1_1, c_sim_1_1, c_sim_1_1, c_sim_3_3]` — message 2 completing
    ahead of message 1. Two different surfaces, same step, same leg: a
    race that loses consistently, not a flake. The claude leg passes step
    10 on every run, so codex timing is what exposes it. This is the
    first genuine product defect the client-journey tier has produced and
    it deserves its own card.

Residual: T2b claude PROVEN. T2b codex 17/18 (finding 22 outstanding). The Rust CLI is
now built on shrdlu at `63e3400`. Evidence preserved outside the leg
dirs at `/tmp/t2b-*-evidence/` and `/tmp/t2b-*-scorecard.md` on shrdlu
(volatile — /tmp). Remaining runbook: T4 acceptance soak, T3 satellite
planning.
