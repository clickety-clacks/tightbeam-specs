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
