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
