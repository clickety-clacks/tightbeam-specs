# e2e tier map — v1

Status: DRAFT r1

Flynn's ruling (2026-07-26) that this spec implements:

1. Testing is the goal; maintaining test scripts is not. A recipe that is fiddly or
   bug-prone lives in a RUNBOOK an agent executes with judgment, not in more script
   code. Working automation (`mix test`, `feature_smoke`, `client_e2e`) stays as it is.
2. e2e proves the FUNCTIONALITY OF THE SUBSTRATE. Agent EFFECTIVENESS is evals
   (`golden-jobs-v1`), a separate process with its own corpus. A check that asserts the
   agent produced a good answer is misfiled.
3. e2e runs in ISOLATION by tier, not as one five-hour block. Full regression is an
   occasional composition of the tiers.
4. Every e2e run files a scorecard.

## Law 0 — the substrate/effectiveness line

An e2e oracle asserts something the SUBSTRATE did: a row reached a state, a frame
arrived, a file landed on the right host, a process died and healed, a refusal named its
cause. Model output may be an INSTRUMENT of that proof (the only way to see a workspace
write is to have the agent write) — it is never the SUBJECT. The test:

> If a competent agent answered differently but the substrate behaved identically, does
> the row still pass?

Yes → substrate check, keep. No → effectiveness check, move to evals.

## The pick-one table (what you changed → what you run)

An agent picking by guesswork is the failure this table exists to prevent. Match the
FIRST row that applies; run everything it names.

| You changed | Run | Why |
|---|---|---|
| anything, before commit | T1 | 130s; the floor, never skipped |
| boot, doctor, readiness, credential delivery, onboarding surfaces | T1 + T0 | first-run states are free to run and are the family's first impression |
| `lib/tightbeam/harness/**`, `lib/tightbeam/acp/**`, `credentials.ex`, `model_catalog.ex` | T1 + T2a + T2b, BOTH legs | ACP-seam changes; mocks cannot prove them (AGENTS.md §Tests — pre-merge, not after) |
| `placement.ex`, `homes.ex`, assimilate, hosts, remote credential projection | T1 + T2a + T3a (+ T3b if adapter health moved) | placement truth only exists across two real hosts |
| supervision, reconciler, adapter health/circuit, lane recovery | T1 + T2b + T4 self-check (T4 60-min before deploy) | recovery is a time-domain property |
| dispatch, wakes, escalation, work items/assignments/brackets, rails, rules, identity/config verbs | T1 + T2a | verb-level agentic surface |
| wire/router/socket, projection, session lifecycle, cancel, queueing, restart | T1 + T2b | client-journey surface |
| rails statutes or roles semantics | T1 + T2a + the MANUAL rows (SMOKE.md 17–33) | live refusal has no automation; see GAP-1 |
| specs/docs only | T1 | |
| weekly / pre-release / post-merge-storm | FULL (T0 included) | the composition, below |

Narrowing is legitimate and never a lie: a one-leg or one-journey-group run reports
`INCOMPLETE(parity)` by design (`Scorecard.run_verdict/2`, verified in
`docs/smoke-runs/2026-07-26-codex-leg-after-task20.md`). INCOMPLETE-by-scope is an
honest partial. Only a `FAIL` row is a failure.

## T0 — first-run states (Flynn ruling 2026-08-01: these belong in the runbook)

**Zero model turns, zero dollars.** Every step is a boot, a status read, or a refusal.
This tier exists because these are the states every new machine passes through and the
family's first impression of the product, and because a refusal that is technically
correct can still read as a broken product. Run it whenever the boot path, doctor,
readiness, credential delivery, or onboarding surfaces change — and before any deploy.

**Method:** a runbook an agent walks with judgment (test-agents-not-test-scripts), on a
real host, with a FRESH base dir so nothing existing is disturbed and nothing is
re-onboarded. Report per step: observed verbatim / what a first-run user would conclude /
verdict (clear, confusing, actively misleading) / evidence.

### The variations

- **V0 — a fresh org knows NOTHING (neutral seed).** The first question a new install
  raises: what does this organization already believe? Per neutral-seed-v1 (Flynn's
  ruling) the answer must be "only the neutral identity" — the identity tree holds
  archetypes/default.toml and guidance/operating-model.md and nothing else, the first
  commit is `seed: neutral-identity`, the default archetype elects no skills and includes
  no guidance, rails and rules load as EMPTY sets, and the built-in fragment library
  carries only the substrate manual. Then `learn agentic-engineering` installs the bundle
  and it becomes live; `unlearn` removes exactly what learning installed. COVERED
  HERMETICALLY (identity/archetypes suites, reviewed) but NOT YET WALKED ON A REAL HOST.
  Walk it: inspect the served identity of a genuinely fresh install, confirm no
  engineering archetype/skill/rail/rule is reachable without an explicit learn, then
  learn and confirm it becomes live. Zero turns — this is all identity-tree inspection.
  NOTE for the runbook: credentials are stored once per harness per machine and injected
  at launch, and homes are per machine+harness rather than per archetype, so learning or
  unlearning NEVER requires re-onboarding. Confirm that on the real host, because "do I
  have to redo my login?" is exactly what a first-run user cannot know.
- **V1 — no harness installed at all.** No coding-agent CLI on the box. Host: eliza (no
  node toolchain by design). WALKED 2026-08-01: boot honest ("NOT READY", names it),
  spawn refuses fast. FOUND: a normal missing-prerequisite is treated as a CRASH
  (exception-driven termination + crash dump); `doctor` needs a RUNNING gateway to learn
  which harnesses to check, so the diagnostic tool cannot fully run on the broken machine
  it exists to diagnose. EXONERATED: no catalog-refresh busywork — zero retries over four
  idle minutes.
- **V2 — harness present, no credential onboarded.** Host: shrdlu, fixture harness.
  WALKED 2026-08-01: boot names the missing credential; spawn refuses in 4ms with the
  cause. FOUND: `doctor` exits 0 and says NOTHING about missing credentials; the remedy
  it prints names a provider the CLI refuses to accept, so the prescribed fix cannot be
  executed on the machine that prescribed it.
- **V3 — user already logged into the harnesses, tightbeam NOT onboarded.** THE
  REALISTIC FIRST RUN for a family member who has used Claude Code for months: ambient
  OAuth in ~/.claude and ~/.codex, tightbeam holding nothing. Tightbeam deliberately
  projects an isolated config root and will NOT borrow those credentials (verified
  2026-08-01), so the user must onboard separately. THE QUESTION THIS TIER MUST ANSWER:
  does the product SAY so, or does it report "no credential" while `claude` works fine
  two commands away — which reads as a bug, not a setup step. NOT YET WALKED (dispatched
  2026-08-01, blocked when the codex budget hit its limit). Host: eurisko, which is in
  exactly this state.
- **V4 — credential onboarded, recovery to working.** The minimum path from any of the
  above to a usable machine, as the product currently guides it. API-key leg WALKED
  2026-08-01 on eurisko ($0.13, one turn per harness, isolation proven at runtime).
  FOUND: after a successful onboard the model catalog stays stale and requires a gateway
  RESTART before models are selectable — the cause healed but recovery was not automatic.
  Subscription leg NOT WALKED — needs a human at a browser, on a test host.

### The README IS the install path under test (Flynn ruling 2026-08-01)

Every install step in this tier is executed BY FOLLOWING THE README, verbatim, as a new
user would — not by an internal recipe, a script, or an agent's memory of how it works.
That is what our users will actually use, so that is what must be proven.

Consequences, and they are the point:
- A step that fails when followed literally is a finding AGAINST THE README, not a
  hiccup for the walker to route around. Do not fix it by knowing better; record what a
  user hitting that line would experience.
- If the README omits a step the install genuinely needs, that omission is the defect —
  the most common way an install doc rots is that its author stops needing it.
- The runbook does NOT restate install instructions. It points at the README and records
  what happened when they were followed. One home for the instructions, per the
  minimize-textual-homes doctrine; two copies drift and the tested one wins by accident.
- Deviations an experienced operator would silently absorb (a missing export, an implied
  directory, a command that needs sudo) are exactly the findings a first-run user cannot
  absorb. Record them.

### Learn splits across two tiers, and the split is forced (Flynn, 2026-08-01)

A fresh org now starts neutral, so `learn` is a step EVERY new install takes. But the
interesting claim — the bundle is genuinely IN FORCE — cannot be proven without
inference: only an agent acting on the guidance, gated by a rail, denied by a rule shows
the org actually KNOWS something. That requires a credential, so it cannot live in this
zero-turn tier.

- **HERE (T0/V0, no credentials): the neutral start and the MECHANICS.** A fresh org
  knows nothing and nothing from the bundle is reachable without an explicit learn. Then
  learn: the tree gains exactly the bundle's paths and a receipt is written. Then
  unlearn: removal is exact, diffed against the pre-learn tree, no residue. All of this
  is file, ref, and refusal inspection — provable with zero turns.
- **POST-ONBOARD (T2a, with credentials): IN FORCE.** Spawn a session on a learned
  archetype and confirm the guidance actually composed into what the agent was served,
  that a rail actually gates a real turn, and that a rule actually denies one. This is
  the half that proves knowledge rather than filesystem state.

ORDERING CONSEQUENCE: onboard, THEN learn, THEN test the knowledge. A walk that learns
before a credential exists can only ever check that files landed.

### Verify the binary matches the source before you believe a walk

A V3 re-walk on eurisko (2026-08-02) ran against a tree whose SOURCE was current and whose
RELEASE CLI was five days old, because the copy carried a pre-existing binary and the host
had no cargo to rebuild. The Elixir-side observations were valid (mix compiled fresh); the
CLI-side ones were not, and the stale binary reported the very exit code the walk was
there to check. Same class as reading a build log through a pipe and getting the pipe's
exit status: an artifact was trusted without confirming it came from the code under test.

RULE: a walk that exercises the CLI must build the release binary on the target, or
confirm its timestamp against the source, and SAY which it did. A walk cannot verify a fix
that is not in the binary it ran.

Corollary found the same night: eliza had been the no-harness host "by design" and now has
both harnesses installed. Do not depend on a MACHINE staying bare — machines drift. Create
the state instead: a harness-less PATH gives the same journey on any host and cannot be
invalidated by someone provisioning the box.

### Standing rules for this tier

- Never touch ~/.claude or ~/.codex; a fresh base dir is what creates the state, never a
  reset of something real.
- Zero turns except V4's minimum recovery proof; API keys cost real money, so one small
  turn per harness is the whole budget.
- A refusal is a PRODUCT SURFACE. Judge its wording as product, not as an error string:
  can a competent non-author act on it from this exact state, without reading the source.

## T1 — local hermetic suite

- **Command**: `mix test` (repo root).
- **Proves**: everything on OUR side of the ACP seam — router/dispatch/DB/lane/rails/
  rules/work-state behavior, conformance corpus classes C1–C3 green
  (`test/conformance/manifest.toml`), the harness/provider seam guards
  (`scripts/check_harness_seam.sh`, `scripts/check_provider_literals.sh`, driven by
  `test/harness_seam_test.exs:53` and `test/provider_additivity_test.exs:7`), the CLI
  against its real release binary (`test/cli_integration_test.exs`), recorded-reality
  fixture drift against the pinned adapter versions
  (`test/subagent_markers_test.exs:74,105`), the client-e2e driver's own scorecard
  algebra and vacuous-pass guards (`test/client_e2e_test.exs:778`), and J0 (pair →
  auth → Main → sync_complete) against a real in-process gateway
  (`test/client_e2e_test.exs:906` boots Bandit + Router with no harness, no credentials).
- **Costs**: 129.6s wall, 858 tests + 6 doctests, 0 failures, 16 skipped (measured
  2026-07-26 on eezo, main @ 70aeb04, `--seed 0`, shared box). No credentials, no
  network, no tokens.
- **Requires**: `cargo build --release` in `cli/`. Absence RAISES the suite rather than
  skipping it (`test/cli_integration_test.exs:31-35`).
- **Does NOT cover**: anything across the ACP seam — no harness process, no model turn,
  no satellite, no real client app, no live rail refusal, no time-domain recovery.
  Conformance C4–Cap are `phase = "pending"` and prove nothing yet.
- **Scorecard**: none. It is a green/red command; a file per run would be noise.

Sub-second inner loop, not a tier: the two guard scripts run standalone in ~1s and are
the right reflex while editing a harness or provider seam.

## T2 — live local matrix (one host, real harnesses, real turns)

Two independent runbooks over the same provisioned org. Both run one leg per registered
harness (T-PARITY). Both burn real tokens.

### T2a — verb surface (`scripts/feature_smoke.exs`)

- **Command**: `mix run --no-start scripts/feature_smoke.exs` against an ALREADY RUNNING
  gateway; reads port+token from `<base_dir>/gateway.json`. `--no-start` is load-bearing
  — a plain `mix run` boots a second gateway that overwrites `gateway.json` and
  redirects the smoke away from the gateway under test.
- **Proves**, in order (`scripts/feature_smoke.exs:36-47`): local deployment (live home +
  cwd projection + durable redelivery), served-identity public seams, onboard surface,
  facts read, default-archetype config, work-item + assignment get, dispatch opens an
  assignment, effort-without-effect check-in and reassignment, the flagship enforced
  review loop, escalation to owner. Credential preflight per leg first
  (`scripts/feature_smoke.exs:52-63`) — FAIL or INCOMPLETE raises before any leg runs.
- **Costs**: ESTIMATE 20–40 min for both legs (multi-turn review loop and check-in
  horizon dominate; no run has recorded wall clock — the first run under this map
  records it). Exits non-zero on the FIRST failed assertion, so a late failure costs the
  whole run.
- **Requires**: a provisioned template org with BOTH harness credentials live, a running
  gateway on it, `TIGHTBEAM_SMOKE_MODEL_<HARNESS>` per registered harness,
  `TIGHTBEAM_EFFORT_CHECKIN_HORIZON_MS=2500`.
- **Isolation**: NONE at leg granularity. `FeatureSmokePlan.legs/2`
  (`lib/tightbeam/feature_smoke_plan.ex:5-17`) maps over every `Harness.all/0` entry and
  RAISES when any leg's model env is missing, and `@registry`
  (`lib/tightbeam/harness.ex:72`) is compile-time. Running one leg is impossible without
  a code change. See GAP-3.
- **GAP (found 2026-08-01): learn/unlearn are not exercised here.** T2a covers
  `identity-relearn` and `apply` but never `learn` or `unlearn` — the verbs landed with
  neutral-seed the same day and the tier predates them. Post-learn correctness is proven
  hermetically (identity suite: bundle imports archetypes/guidance/skills/rails/rules,
  writes a receipt, reloads all law) and once on a real host by T0/V0, but nothing
  REPEATABLE exercises the verb surface. Since a fresh org now starts neutral, learn is
  on the critical path for every new install and belongs in this tier: learn, confirm the
  bundle is live and an agent can actually use it, unlearn, confirm removal is exact.
- **Does NOT cover**: client-visible wire behavior, restart, satellites, sustained load,
  and (see GAP above) learn/unlearn.

### T2b — client journeys (`scripts/client_e2e.exs`)

- **Command**: `mix run --no-start scripts/client_e2e.exs` with
  `TIGHTBEAM_CLIENT_E2E_TEMPLATE`, `TIGHTBEAM_CLIENT_E2E_PORT` (≥12000, refused below),
  `TIGHTBEAM_CLIENT_E2E_HARNESSES`, `TIGHTBEAM_SMOKE_MODEL_<HARNESS>`,
  `TIGHTBEAM_CLIENT_E2E_OUT=<scorecard path>`.
- **Proves**: SMOKE.md steps 1–16b as J0–J8 — pair, converse, tool use, stream
  lifecycle, cancel, queue order, cross-lane concurrency, slash commands, model change,
  restart resilience (real SIGTERM of the captured pid, exit + port-unreachable + NEW
  pid confirmed: `lib/tightbeam/client_e2e/leg_gateway.ex:169-188`), queued-turn
  survival, wakes, scheduled wakes. Every step carries a two-column oracle — client
  assertion AND substrate assertion (`lib/tightbeam/client_e2e/journeys.ex` `@oracles`).
  It provisions and tears down a FRESH org per leg and refuses to run on a dirty
  worktree (`scripts/client_e2e.exs:189-209`).
- **Costs**: ESTIMATE 15–25 min per leg (~20 real model turns, two gateway restarts,
  180s per-turn timeout ceiling, `client_e2e.ex:22`). Measured numbers go in the
  scorecard header from now on.
- **Requires**: the same template org and live credentials; one throwaway port per leg.
- **Isolation**: per leg via `TIGHTBEAM_CLIENT_E2E_HARNESSES=codex` (proven — the
  committed codex-only scorecard). Per JOURNEY isolation exists in the library
  (`run_leg(journeys: [...])`, `lib/tightbeam/client_e2e.ex:60`) but is unreachable from
  the script. See GAP-4.
- **Does NOT cover**: the real iOS app's RENDERING (row 13c is permanently `MANUAL` —
  the app-side assertion lives in clawline's own tests), rails/roles, satellites, soak.

## T3 — real-host satellite runbook (agent-executed)

Runbook: `satellite-e2e-v1.md`. Executor is an agent on eezo with SSH per
`environments.md`; the safety rails there are absolute and apply to every group below.
Host matrix, credential requirements (satellite store projection AND gateway-side
onboarding), fixture bare-metal policy and teardown discipline are unchanged — this map
only groups the journeys so a targeted run is affordable.

| Group | Journeys | Proves | ESTIMATE per pairing |
|---|---|---|---|
| T3a placement | S1 assimilate cold, S2 session on satellite, S3 workspace motion | a satellite can be brought up from nothing and hold a session whose workspace and home live THERE, not on the gateway | 60–90 min |
| T3b fault + reinstall | S4 adapter death and heal, S5 re-assimilate (linux only) | an adapter fault opens its circuit, terminalizes with a named cause, and heals; re-assimilate replaces in place and credentials survive outside deletion scope | 45–75 min |
| T3c negatives | N1 no node, N2 no credential at the projection seam, N3 no harness CLI on gateway | missing dependencies REFUSE CLEANLY with a named, actionable error — never a hang, crash, or half-configured state | 30–45 min |
| S6 teardown | ALWAYS | no residue, protected surfaces unchanged, lock released | 10 min |

- **S6 runs in every T3 run without exception**, including after failures and including
  after a group you chose not to run. A T3 run that skips teardown is a FAIL.
- **T3a is a precondition for T3b**: S4 needs the resident session S2 created. T3c is
  independent and can run alone.
- **Costs**: two real hosts + SSH + credentials on both + the lock. Full both-pairing
  pass is Flynn's observed ~5 hours; no run has recorded wall clock.
- **Order**: linux pairing FIRST; macOS/tars only after a clean linux run
  (`satellite-e2e-v1.md` §Host matrix).
- **Does NOT cover**: client journeys (T2b), verb surface (T2a), sustained load (T4).
- **Known-FAIL rows are product defects, not oracle problems** — keep reporting them:
  S4's reason clause and resident-session recovery, and N2's catalog masquerade on a
  post-boot-assimilated host.

## T4 — soak (`scripts/soak.exs`)

- **Command**: `mix run scripts/soak.exs -- --minutes 2 --self-check` (acceptance),
  `--minutes 60` (pre-deploy), `--minutes 1440` (release).
- **Proves** A1–A5 (`docs/SOAK.md`): no stalled turn past 180s, message integrity and
  wake non-duplication, failures visible with reasons and lifecycle rows, wake
  conservation, and gateway recovery within 60s of every kill in the matrix
  (adapter SIGKILL, gateway SIGTERM/SIGKILL, cancel).
- **Costs**: 2 min / 60 min / 24 h. Claude credentials only — it symlinks
  `~/.tightbeam-beam/auth/claude` into its arena and never copies the token. Dedicated
  arena `~/.tightbeam-soak`, marker-guarded (`.soak-arena`).
- **Does NOT cover**: codex leg, client wire, satellites, any verb outside the load loop.
- Any A1–A5 FAIL blocks deploy of whatever the soak was proving.

## FULL regression

`T1` → `T2a + T2b` (both legs) → `T3a + T3b + T3c` (both pairings, S6 each) →
`T4 --minutes 60` → the SMOKE.md MANUAL rows (17–33) run by hand. Verdict is the worst
constituent verdict; a missing tier makes the regression INCOMPLETE, never a pass.

Out of scope, deliberately: EVALS. `golden-jobs-v1` scores agent effectiveness from
`work-item-trace` artifacts against a fixture corpus. It is not a tier here and its
results never gate an e2e verdict.

## Scorecards

Format is `docs/smoke-runs/TEMPLATE.md` (v1 row schema, algebra implemented in
`Tightbeam.ClientE2E.Scorecard`). Cell values `PASS`, `PASS (divergence <matrix row>)`,
`FAIL(note)`, `INCOMPLETE(blocker)`, `MANUAL(reason)`, `N/A[harness-only]` are unchanged.
Three minimal extensions, so agent-executed and narrowed runs file the same way:

1. **`PASS (workaround: <what you did>)`** — a new cell value. The satellite runbook
   already mandates reporting pass-with-workaround and the v1 schema had no cell for it.
   It counts as PASS for the verdict; an unnamed workaround is a FAIL.
2. **Header gains `Tier:`, `Scope:`, `Wall clock:`, `Runid:`.** `Scope` has precedent —
   the hand-driven `docs/smoke-runs/2026-07-18-1b9a60b.md` already carries one. Scope names the legs and
   journey groups that were IN scope, so `INCOMPLETE(parity)` on a deliberate narrow run
   reads as scope and not as breakage. Wall clock is what keeps this map's cost column
   honest — tiers are defined by cost, so every run records it. Runid is required for T3
   (it is the rail that names deletable roots).
3. **`SKIP(reason)`** for a T3 journey whose preconditions could not be established at
   all. Verdict-neutral like MANUAL; the reason is required.

**Where they are filed**: `~/shared-workspace/tightbeam_ex/smoke-runs/` (run records are operational instance reports, not product documentation — moved out of the repo by 8451bd1, 2026-07-28; TEMPLATE.md moved with them), named
`<date>-<gateway-sha>-<lane>[-<runid>].md` where lane ∈ `feature-smoke`, `client-e2e`,
`satellite-<pairing>`, `soak`. T2b writes its own file via
`TIGHTBEAM_CLIENT_E2E_OUT`; T2a, T3 and T4 scorecards are written by the executing
agent into the same directory in the same schema. T1 files nothing. Zero satellite
scorecards exist today — every T3 run from now on commits one.

## Provisioning — the ONE recipe

This recipe was hand-typed roughly eight times for satellite runs and got it wrong
twice. It lives here now; the code paths cited are the authority.

### A template org (the thing T2 copies from)

A template org is a full, working org whose credential material is valid on THIS host.
`~/.tightbeam-beam` is the dev org and is NOT a valid template today: its home
projection is keyed `homes/default/`, while every reader resolves
`homes/<Placement.local_host_name/0>/<harness>` (`lib/tightbeam/homes.ex:245`,
`lib/tightbeam/placement.ex:108`). Measured 2026-07-26 on eezo:
`Tightbeam.ClientE2E.preflight/3` against it returns INCOMPLETE for both harnesses,
ENOENT on `homes/eezo/claude/oauth-token`. Use an org built as below (the
`~/.tightbeam-smoke-*` orgs on eezo are of this shape).

Required contents, all four or the org is not ready:

1. **Credential store rows — three parts per harness, all three.**
   - backing file: `auth/claude/oauth-token` (a full 108-char `sk-ant-oat…` setup
     token) or `auth/codex/auth.json` (`lib/tightbeam/credentials.ex:91-92`);
   - home symlink: `homes/<host>/<harness>/{oauth-token,auth.json}` → that backing file;
   - metadata row: `auth/<harness>/.tightbeam/credential.json` with `"onboarded": true`.
     This one is load-bearing: status is `:onboarded` only when
     `metadata["onboarded"] == true` AND the credential is present
     (`lib/tightbeam/credentials.ex:299-303`); absence yields
     `{:needs_onboarding, :missing}`.
   The sanctioned way to produce all three is `tightbeam onboard <provider>` ON the host.
   Never harvest or copy a rotating Claude login.
2. **Codex model catalog**: `homes/<host>/codex/models_cache.json`, copied from a live
   `~/.codex/models_cache.json` (`lib/tightbeam/harness/codex.ex:331`). Wrong host key
   degrades silently at boot (`:missing_cache`) and bites at spawn
   (`catalog_unavailable`).
3. **Identity repo, committed and clean**: `identity/` with its `.git`; anything
   hand-placed under it must be committed or every identity verb wedges on
   "identity working tree is dirty".
4. **Default model matches default harness**: `TIGHTBEAM_DEFAULT_HARNESS` /
   `TIGHTBEAM_DEFAULT_MODEL` or the archetype `[defaults]`. A claude default against a
   codex org fails `model_unavailable` at spawn.

**Verify before booting anything** — this is the gate, one command per harness:

```sh
mix run --no-start -e 'IO.inspect(Tightbeam.ClientE2E.preflight("claude", "<org>"))'
```

`:pass` → go. `fail` → repair. `incomplete` → BLOCKER, never permission to boot
(SMOKE P3). It probes through the harness registry callbacks and needs no running
gateway (`lib/tightbeam/client_e2e.ex:154-207`).

`mix tightbeam.doctor --base-dir <org>` is useful for the harness BINARY, identity,
and hosts rows only. Its `harness_auth` rows are unreliable standalone: measured
2026-07-26 against a working org it reported
`dead_sign_in … {:needs_onboarding, :credential_server_unavailable}` for both harnesses,
because the Credentials server does not run inside a bare mix task. Do not use it as the
credential gate. Its `ready` flag also passes on ONE ready harness, so it never proves
T-PARITY (`lib/mix/tasks/tightbeam.doctor.ex:99`).

### A per-leg org (what T2b does automatically, and what T3 does by hand)

Copy `auth/`, `homes/`, `identity/` from the template into a fresh base_dir; copy
`state.db`, `gateway.json`, logs and `work/` NEVER — that is the history a fresh leg
must not have (`lib/tightbeam/client_e2e/leg_gateway.ex:45,55-71` and its moduledoc).
Boot with `TIGHTBEAM_BASE_DIR`, `TIGHTBEAM_PORT` (12000–12999),
`TIGHTBEAM_EFFORT_CHECKIN_HORIZON_MS=2500`. Note home symlinks are absolute: a copied
home still points at the TEMPLATE's `auth/` file, so the template must outlive its legs.

### On a satellite (T3)

Additionally, in this order: bootstrap an admin by PAIRING A DEVICE over the run
gateway's ws before `register` (a fresh base_dir refuses `register` with "admin
required"); write the `RUN_MARKER` into the satellite base_dir immediately after every
assimilate (assimilate does not create it, and teardown will rightly refuse an unmarked
removal); symlink `<run base_dir>/auth/<harness>` → the satellite's persistent store
BEFORE S2 and again after S5's reinstall; install a run-owned archetype whose `where`
admits the satellite (the shipped default admits eezo/tars/racter only); onboard the
GATEWAY for that harness too — model validation is a gateway-side authenticated catalog
fetch, and a gateway with no credential for a harness cannot place its sessions
anywhere.

## Audit — every e2e-ish entry point (2026-07-26, main @ 70aeb04)

| Entry point | Covers | Invocation | Cost | Requires | Executor | Era / status |
|---|---|---|---|---|---|---|
| `mix test` | T1, above | `mix test` | 129.6s measured | `cli/` release binary | automated | current |
| `scripts/feature_smoke.exs` | T2a verb surface | `mix run --no-start` | 20–40 min EST | running gateway, both credentials, models | automated | current |
| `scripts/client_e2e.exs` + `lib/tightbeam/client_e2e/**` | T2b journeys J0–J8 | `mix run --no-start` | 15–25 min/leg EST | template org, both credentials, ports ≥12000 | automated | current (2026-07-25/26) |
| `satellite-e2e-v1.md` | T3 S1–S6, N1–N3 | agent follows runbook | ~5 h both pairings | two real hosts, SSH, credentials both sides | AGENT | current, ACTIVE RUNBOOK |
| `scripts/soak.exs` + `docs/SOAK.md` | T4 A1–A5 kill matrix | `mix run scripts/soak.exs -- --minutes N` | 2 min / 60 min / 24 h | claude credential, dedicated arena | automated | current |
| `docs/SMOKE.md` | the normative journey list; steps 17–33 (rails, roles) are `[manual]` | human/agent, by hand | hours | live org, scratch git repo | MANUAL | current, never automated |
| `test/conformance/**` + `test/conformance_test.exs` | C1–C3 green; C4–C7, Cap `phase = pending` | inside `mix test` | included in 130s | none | automated | current |
| `test/cli_integration_test.exs` | Rust CLI against the real router | inside `mix test` | included | `cargo build --release` | automated | current |
| `scripts/check_harness_seam.sh`, `check_provider_literals.sh` | harness/provider literal containment | standalone (~1s) or inside `mix test` | ~1s | none | automated | current |
| `scripts/l0_smoke_catalog.exs` | live derived-catalog fetch, freshness, no boot hang | `mix run` | seconds | real `~/.tightbeam-beam` claude token + codex cache | automated | L0 era, superseded by the T2 preflight; still runs |
| `scripts/l0_smoke_spawn.exs` | dead model ref denies at `validate_catalog_model` before spinup | `mix run` | seconds | copies real auth+identity to scratch | automated | L0 era, superseded; still runs |
| `scripts/e1_first_light.exs` | supervised prompt round-trip to a real claude adapter | `mix run` | ~1 min | the TS repo's `node_modules` adapter + `~/.claude` creds directly | automated | E1 era, superseded by T2b; paths still resolve |
| `mix tightbeam.doctor`, `mix tightbeam.catalog_diff` | org readiness / catalog drift probes | mix task | seconds | live catalog fetch | automated | current; NOT credential gates (above) |

## Findings — misfiled effectiveness checks

- **MIS-1 (fix): J8 wakes, SMOKE step 16.** `journeys.ex:1256` fails the row when the
  assistant's reply does not contain `WAKE OK`. That asserts instruction compliance. The
  substrate's claims are already asserted beside it — the wake's prompt arrived as a
  sender-tagged message, the turn row carries the `wakeId`, the turn reached
  `delivered`. Drop the content match; keep the rest. Evidence this misfires:
  `docs/smoke-runs/2026-07-26-a888f9b-client-e2e.md` row 16 FAILs the claude leg for a
  reply that was not the literal string while every substrate oracle held.
- **MIS-2 (keep, narrowed): J1 tool use, SMOKE step 4.** `journeys.ex:347` requires the
  reply to contain the local `uname -s`. The progress-label assertion is the substrate
  proof that a tool call happened; the content match additionally proves the command ran
  in the right PLACE, which is why the same shape is load-bearing on a satellite (T3's
  S3 nonce file). Keep it, and state in the oracle that it is a PLACEMENT proof, not an
  answer-quality proof — so nobody generalizes it into asserting good answers.
- Nothing in T1, T2a, T4 or T3's oracles asserts answer quality. Reviewed the T3
  workspace-motion nonce (S3) explicitly: agent action is the instrument, the SSH content
  check on the satellite is the assertion. Correctly filed.

## Findings — coverage gaps the audit exposed

- **GAP-1 (largest): 17 of SMOKE.md's 33 steps have never appeared in any committed
  scorecard.** Steps 17–24 (rails: live tool refusal, boot wiring-check, bad-law boot
  refusal, law removal, satellite propagation) and 25–33 (roles: typed targets,
  unstaffed/staffed office, late binding, deleted office, Main permanence, spawn
  atomicity, acting-as) are `[manual]`, and the client-e2e driver emits rows 1–16b only —
  the committed scorecards stop at 16b while `TEMPLATE.md` still carries 17–33 rows. The
  mechanisms have unit coverage (`test/rails_test.exs`, `test/roles_test.exs`), so what
  is unproven is the LIVE half: a real harness's tool call actually being refused by a
  gate, and role delivery through the real dispatch path. Until someone runs them, the
  honest posture is MANUAL rows carried in every T2 scorecard.
- **GAP-2: zero satellite scorecards are committed** (`docs/smoke-runs/` holds eight
  client-e2e runs plus one 2026-07-18 hand-driven smoke), so five satellite runs'
  evidence lives only in run reports. Fixed by the filing rule above.
- **GAP-3: T2a cannot run one leg.** `feature_smoke` always runs every registered
  harness and refuses without a model for each. A targeted adapter-seam fix therefore
  costs both legs. Smallest fix: an env leg filter in `FeatureSmokePlan.legs/2`, ~5 lines,
  not attempted here.
- **GAP-4: T2b's journey-group isolation is unreachable from the script.**
  `run_leg(journeys: [...])` exists; `scripts/client_e2e.exs` never passes it. A
  `TIGHTBEAM_CLIENT_E2E_JOURNEYS` passthrough (~3 lines) would turn "did I break
  restart?" from a 20-minute leg into a 3-minute one. Until it exists, T2b's isolation
  granularity is per leg.
- **GAP-5: no tier proves the real client APP renders anything.** Row 13c is permanently
  MANUAL and the sim client is the driver by design (`client-e2e-v1.md` architecture
  amendment). The real-app driver (XcodeBuildMCP + AXe over accessibility identifiers) is
  a named follow-up lane that does not exist.
- **GAP-6: recorded-reality drift is gated for two fixtures, not all.**
  `test/fixtures/subagent_markers/*` are cross-checked against the pinned
  `@adapter_version` (`subagent_markers_test.exs:74,105`); `test/fixtures/credentials/
  *-0.145.0.json` are named for a codex CLI version nothing asserts. Harness CLIs
  auto-update under us, so that stamp should be checked the same way.
- **Residue, operational**: eight `~/.tightbeam-smoke-*` template orgs and one
  `~/.tightbeam-client-e2e-*` leg directory are still in `$HOME` on eezo, the latter with
  a codex home written to minutes ago — a teardown that reported `:not_removed` and left a
  harness process holding the tree, exactly the case `leg_gateway.ex:273-288` documents.
  Not a spec matter; naming it so somebody sweeps.
