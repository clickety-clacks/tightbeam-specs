# Full-client e2e — simulator client → real gateway — v1

ARCHITECTURE AMENDMENT (Flynn-authority 2026-07-25, implemented): the driver is a
TIGHTBEAM-SIDE SIM CLIENT on the real HTTP/WS surface ("sim client → gateway journeys"
— Flynn's framing; the sim client IS the driver). It proves the gateway emits everything
a client needs. Proving the APP RENDERS it (real-app driver via XcodeBuildMCP+AXe over
the accessibility identifiers, incl. the footer 13c which renders the catalog DISPLAY
NAME, not the posted ref) is a NAMED FOLLOW-UP lane, not part of this deliverable.

Status: READY (gate-cleared 2026-07-25, Sol-high round 4: zero blocking; 5→3→1→0). Flynn mandate: "previous agents were
stopping short of actually testing the client. BOTH of these must happen" — the CLI e2e
(cli_integration, its own lane) AND this: the REAL Clawline client, in a simulator,
driving the operator journeys against a REAL tightbeam gateway. Governing directive
(clawline/CLAUDE.md, Flynn 2026-07-24): NEVER mock tightbeam in integration/e2e — a
green test on a mocked backend is forbidden; the existing model is the web client's
`playwright/tests/shrdlu-tightbeam-pairing.spec.ts`.

## Spirit

SMOKE.md's client journeys are today a MANUAL runbook: a human with the iOS simulator
walks pair → converse → lifecycle → cancel → queueing → concurrency → restart → wakes.
This spec automates that runbook. The deliverable is a DRIVER that boots a fresh
gateway org, boots the real iOS client in a simulator, and walks the journeys
asserting BOTH sides: what the client shows (screens, bubbles, indicators) and what
the substrate recorded (rows, frames). When it exists, "did we break the client?" is
a command, not an afternoon.

## Scope — the journeys (SMOKE.md is NORMATIVE; this list is an index)

Each J-spec implements its SMOKE.md steps BY NUMBER and inherits the runbook's PASS
conditions VERBATIM — the summaries below are an index for reading, never a
restatement of acceptance (r1 F1: summarizing dropped conditions, e.g. J4's
three-post ordering; where this file and SMOKE.md disagree, SMOKE.md wins — but the
precedence is scoped to numbered journey steps and their PASS conditions ONLY
(r2 F2): SMOKE's generic waive-a-leg-by-name allowance is NOT sufficient for this
spec's proofs — here a missing codex leg is INCOMPLETE unless the divergence is a
live negative-proved `harness-support.md` row).

J0 pair: fresh org, first device pairs, becomes admin; catalog shows Main;
   sync_complete leaves the connecting state.
J1 converse: post → echo bubble, typing indicator with live progress, assistant
   reply, indicator clears; turn row delivered. Tool-use variant shows a tool title.
J2 lifecycle: create stream (appears live, no reconnect), rename (live), retire
   (gone live; rows soft-retained).
J3 cancel: long task, cancel mid-turn; turn row canceled; client shows the stop.
J4 queueing: two posts one lane — strict order, no interleave.
J5 concurrency: two streams in parallel — both progress independently.
J7 restart resilience (executable proof, r1 F4): capture the gateway PID at boot;
   SIGTERM that exact pid; await process exit AND the health endpoint going
   unreachable; restart on the SAME port and base_dir; confirm a NEW pid; the app
   stays running throughout — then assert reconnect, snapshot heal, no loss of
   delivered rows. Killing a wrapper or dropping a socket cannot satisfy this.
J8 wakes: a scheduled wake fires and its prompt lands in the stream as a turn.
J6 slash commands (SMOKE §6, steps 11-13 — IN v1, corrected 2026-07-25): the
   substrate interprets no message content, so `/new`, `/compact`, and `/model` are
   ordinary text to the model and their PASS condition is J1's oracle verbatim — the
   turn COMPLETES (bubble, indicator clears, `delivered` row). This journey exists to
   catch the shipped regression class of a slash command dying pre-model and hanging
   the indicator forever. Step 13's second half (change the model for real through the
   client picker; assert `session-status` shows the new ref AND the client's model
   FOOTER populates — the Swift decode contract raw JSON checks miss) adds exactly two
   identifiers (picker entry, footer label) to the testability deliverable.
(§9-10 rails/roles journeys remain v2 — those DO need client UI maps that don't exist
yet; named here so their absence is a decision.)

## Architecture

- **Driver**: a script/runner in the clawline repo (owner: client repo, where the
  playwright model lives) named `e2e/sim/` — per journey one spec file. Tooling:
  XcodeBuildMCP to build/install/launch the iOS app in a named simulator; AXe
  (accessibility automation) to tap/type/read the UI; assertions on the
  accessibility tree, not screenshots (screenshots are failure artifacts only).
- **Client testability deliverable (r1 F2)**: the journeys' asserted surfaces gain
  ACCESSIBILITY IDENTIFIERS in the app — pairing already has them
  (PairingView); the typing indicator and its live progress text, stream catalog
  rows, message bubbles, tool-title label, and cancel affordance do not. The
  driver spec enumerates the required identifier per assertion, and adding them is
  part of THIS spec's implementation (client repo), not an assumed precondition.
- **Deterministic reset (r1 F3)**: the client persists device identity and auth in
  the Keychain, so install-over-prior-run boots past pairing into a stale
  provider. Each leg starts from `simctl` app uninstall (or simulator erase for
  the first leg of a run) so J0 always begins at the server-URL form; per-leg
  isolation is part of the matrix contract.
- **Gateway**: the driver boots a FRESH org PER HARNESS LEG (r2 F1 — the client's
  Keychain device-ID persists across reinstall, so a reused org takes the
  known-device path instead of J0's first-user bootstrap, and prior-leg rows
  linger; leg isolation therefore requires a fresh base_dir provisioned AND torn
  down per leg), each exactly as feature_smoke's provisioning doctrine prescribes
  (docs/SMOKE.md §Fresh-org provisioning: credential store rows, catalog
  readiness, matched default model, short effort horizon), on a run-local port,
  AFTER running SMOKE.md's credential PREFLIGHT (P1/P2) for that leg's harness
  (r1 F7). Teardown is defined as existing
  operations only (r1 F8): SIGTERM the gateway's captured pid, await exit, then
  remove the run-local base directory. The driver emits a V1 SCORECARD (r2 F3, algebra pinned r3): one row per SMOKE
  step. Row statuses: `pass | fail | manual | incomplete(blocker)`; PREFLIGHT rows
  (P1/P2 per leg) are AUTOMATED rows and take pass/fail like any other — `manual`
  is reserved for journey steps outside v1 automation scope and is VERDICT-NEUTRAL.
  Per-leg verdict algebra: `PASS` iff every applicable preflight row and every
  automated row is `pass` (negative-proved divergences count as pass for their row,
  citing the harness-support.md row id); any `fail` → `FAIL`; else any
  `incomplete` → `INCOMPLETE(blockers listed)`. The run verdict is the worst leg
  verdict. The template correction (docs/smoke-runs/TEMPLATE.md gains this schema)
  is a named component touch. No shared/live gateways in CI runs (shrdlu stays the
  manual/web target).
- **Substrate oracles (normative duality, r1 F5)**: for EVERY client action the
  J-spec carries a two-column oracle row — the client assertion (accessibility
  tree) AND the substrate assertion (the `sqlite3 <base_dir>/state.db` row or
  CLI-read frame SMOKE.md names for that step). BOTH columns MUST pass; "may" is
  not part of this contract. A step where one side has no observable counterpart
  says so explicitly in the J-spec (silence illegal).
- **Harness parity (T-PARITY)**: the run is a MATRIX — one full pass per registered
  harness, same as SMOKE.md mandates; a single-harness run reports INCOMPLETE.

## Non-goals

- No mocked gateway, ever (standing directive).
- No pixel/screenshot assertions (accessibility tree is the oracle; screenshots are
  captured on failure for humans).
- No Android/web drivers in v1 (web has its playwright model; Android is its own
  lane when mandated).
- No CI-infrastructure design in v1 (the driver must be runnable-by-command on a dev
  Mac; scheduling it is an ops decision recorded separately).

## Required proofs

1. J0-J8 (J6 included per the 2026-07-25 correction) each pass against a fresh org on
   the claude leg, asserting both client and substrate oracles.
2. The codex leg passes the same journeys, or the divergence is a LIVE row in
   `harness-support.md` with its required negative proof (r1 F9 — never a
   runner-local waiver minted when a leg fails).
3. A deliberately broken gateway (wrong port) yields a FAILING run with a legible
   client-side error assertion — the driver cannot pass vacuously.
4. J7 proves reconnect against a real gateway restart (not a socket drop
   simulation).
5. SMOKE.md gains per-step annotations naming which J-spec automates it; steps
   without one remain explicitly manual (silence illegal, same rule as the
   capability matrix).

## Component touches

clawline repo: `e2e/sim/` driver + specs, accessibility identifiers for the
asserted surfaces, simulator provisioning docs; tightbeam_ex: `docs/SMOKE.md`
per-step automation annotations (r1 F6 — SMOKE.md lives in the gateway repo; proof
5 edits it there) and `docs/smoke-runs/TEMPLATE.md` v1-scorecard schema (r2 F3); gateway + CLI otherwise consumed as black boxes; shared specs:
this spec.
