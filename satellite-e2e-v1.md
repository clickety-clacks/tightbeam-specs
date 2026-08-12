# Satellite e2e runbook — v1

Status: ACTIVE RUNBOOK (Flynn ruling 2026-07-25: this is a runbook a TEST AGENT gets
through, NOT a script we maintain — "we want our test agents to be flexible and I don't
want to get into the business of maintaining broken testing scripts"). The journeys,
oracles, and safety rails below were adversarially gate-cleared against main 58f7fe0
(trajectory 8→7→1→READY); the executor is an agent that follows this runbook, adapts
around incidental failures, and reports an honest scorecard. No satellite_e2e script
exists or should be written.

## Executor contract (the flexibility rule)

- You are an agent on the ORCHESTRATION host (eezo) with SSH access per
  environments.md. Read environments.md before starting; it is the access truth.
- GET THROUGH THE RUNBOOK: an incidental failure (SSH hiccup, slow boot, flaky model
  turn) is yours to diagnose and work around — retry, respawn, take another path — and
  every workaround goes in the scorecard. A journey is only FAILED when its oracle
  genuinely does not hold after honest effort; it is SKIPPED (named reason) only when
  its preconditions cannot be established at all. Either way, CONTINUE to every later
  journey you still can run, and ALWAYS run teardown.
- Report per journey: pass / pass-with-workaround (named) / fail (evidence) /
  skip (reason). Never launder a workaround into a clean pass.
- The safety rails are NOT adaptive surface — they are absolute. When a rail blocks
  your workaround, the workaround dies, not the rail.

## Preconditions on the GATEWAY host (check these first — each one blocked a run)

The runbook long assumed these because the orchestration host happened to satisfy them.
None held on shrdlu the first time a run started there, and each failed with a message
about something else:

- **The gateway needs the leg's harness CLI installed.** shrdlu had no `codex` at all, so
  onboarding could not run — `tightbeam onboard openai` shells out to
  `codex login --device-auth`. npm's prefix there is `/usr`, so install user-local
  (`npm install -g --prefix ~/.local <pkg>@<pinned>`); the rails forbid sudo. Pin the
  version: harness CLIs auto-update under us.
- **The gateway needs its OWN onboarding for that harness** (already stated below) — and
  that onboarding is INTERACTIVE device auth, so a human must be reachable when the run
  starts. Budget for it or do it in advance.
- **The gateway must reach the satellite NON-INTERACTIVELY, with no `-i` flag.** Assimilate
  runs a bare `ssh <dest>`; an identity that only works when named on the command line is
  not enough. Give the gateway host an `~/.ssh/config` entry (`Host`, `User`,
  `IdentityFile`, `IdentitiesOnly yes`) and confirm `ssh -o BatchMode=yes <dest> hostname`
  answers before starting.
- **A pre-existing base dir may hold a database older than the current build**, which
  refuses to boot by design (`Schema.ShapeError`). Move it aside as the message says;
  credentials live in `auth/` and are unaffected.

## Host matrix (Flynn-assigned roles)

| pairing | gateway | satellite | harness leg |
|---|---|---|---|
| linux/linux | shrdlu (`clu@shrdlu`) | eurisko (`clu@eurisko`; eliza rejected — no node at all) | codex |
| macOS/macOS | tars (`mike@tars`) | eezo | claude |

(Legs swapped 2026-07-25 after run lnx-0725a: eurisko already holds a codex credential
store but no claude one — claude onboarding needs an interactive login, codex runs now;
eezo holds claude credentials, so the claude leg rides the macOS pairing. Complementary
coverage across the matrix is preserved. eurisko's non-interactive PATH now exposes
asdf node — operator fix, ~/.bashrc prepend, backup at ~/.bashrc.bak-tightbeam.)

Legs are complementary across pairings (claude and codex have materially different
remote launch recipes — both get covered across the matrix). Record exact harness+model.
Run linux FIRST; macOS/tars only after a clean linux run.

**Credentials — TWO requirements (mac-0726a):** the SATELLITE needs the harness
credential store (projected, below) AND the GATEWAY needs its OWN onboarding for that
harness — model validation is a gateway-side authenticated catalog fetch (task #22; on
linux shrdlu satisfied this by accident). A gateway with no harness credential cannot
place sessions ANYWHERE for that harness. Assimilate does not transport credentials
(SATELLITE.md). Harness
credentials live on each satellite OUTSIDE your deletion scope (standard harness auth
dirs). Tightbeam reads them from the registered satellite `base_dir/auth/{claude,codex}`
— PROJECT them: COPY the persistent store to `<run base_dir>/auth/<harness>` before S2, and
recopy after S5's reinstall. **Copy, not symlink.** A symlinked auth directory is silently
ignored by the current build — no catalog derives and no log line is emitted at all, so it
presents downstream as `catalog_unavailable {:unavailable, :not_derived}` and reads as a
broken catalog rather than an unreadable store (measured 2026-08-03: same org, same boot,
symlink vs copy the only difference). Revert to symlinks only once that is fixed and the
fix is verified here. The S2 preflight is the registry
harness's `credential_live?/3` callback, not symlink/store presence: construct the
satellite-shaped target from the registered host (`host_name`, remote `base_dir`, SSH
destination, and the normal command runner), pass the projected `auth/<harness>`
directory as `home_path`, and inject
`Tightbeam.Harness.Support.credential_transport/2` plus the manifest-default bounded
timeout. Grade the exact result algebra: `:live` → PASS; `{:dead, reason}` → FAIL;
`{:unknown, reason}` → INCOMPLETE/blocker, never PASS. A non-PASS result blocks S2's
spawn until repaired or explicitly waived by name.

## Safety rails (ABSOLUTE — checked before every kill/rm/install)

**Including setup.** These govern every kill, rm and install you perform for this run, not
only the ones inside a journey — the preconditions above are where you are improvising on a
shared host, which is exactly when they matter most. A run on 2026-08-03 signalled a
stranger's process during setup, matching on a loose pattern; it survived only because the
process belonged to another user and the kernel refused. The rails were correct and were
simply not applied yet.

**A pidfile is not identity on its own.** `mix run` execs `beam.smp`, whose argv contains
neither the project path nor the run root, so a pidfile check that greps argv will report
"stale" for a live process you own. That is the KERNEL-IDENTITY case below: owner, plus
`/proc/<pid>/cwd` under your tree, plus owning your test port — all three, re-verified
immediately before the signal.

- Verify remote identity first: SSH `hostname` must match the intended role host;
  gateway host ≠ satellite host; abort the operation otherwise.
- Everything you create on a remote host lives under `~/.tightbeam-e2e-<runid>/`
  (base) or `~/.tightbeam-e2e-install-<runid>/` (install), each with a `RUN_MARKER`
  file naming your runid. Every `rm` target must be one of those two roots and contain
  your marker — never anything else, never `~`, never broad globs.
- Kills: exact PID with POSITIVE IDENTITY. Primary predicate: command line contains
  your run's base_dir or install dir (use `ps -ww` — macOS truncates argv without it).
  KERNEL-IDENTITY equivalent (mac-0726a: a system-toolchain gateway's argv contains NO
  run root): cwd under a run root (lsof) AND open files under a run root AND owning
  your test port's listener — re-verified immediately before the kill. Either
  predicate suffices; NO match = do not signal. Never `pkill`/pattern kills. No
  `sudo`. No systemctl/launchd/unit operations on any host, ever. Teardown scripts
  must not let an identity-check abort skip the REMAINING teardown steps (mac-0726a:
  a fail-fast script left the gateway running on the production host for minutes —
  each teardown step independent, failures reported not cascaded).
- Lock: create `~/.tightbeam-e2e-<pairing>.lock` (runid+pid) on the gateway host at
  start; refuse to run if it exists with a live pid; remove it (that exact path only)
  at the end.
- npm confinement: run assimilate's remote npm with `NPM_CONFIG_CACHE` and `TMPDIR`
  inside your install root.
- Protected surfaces, pre/post (record before, assert identical after):
  - shrdlu AND tars: OpenClaw ports **18789, 18792, 18800** listener PIDs. Your test
    gateway port comes from **12000-12999**, not protected, not already listening.
  - eliza (if used): Subetha three-way — service PID (exact match, read-only), `:4000`
    listen state, HTTP answers — unchanged after the run.
  - tars additionally: artifacts confined to your two run roots, both removed at end
    (standing TARS rule: no dev artifacts, ever).
  - gibson: not in this matrix (prod lane).

## Run-gateway fixture notes (lnx-0725d)

- Device pairing auto-creates a Main session ON THE GATEWAY HOST whose turns fail
  forever (a run-owned gateway installs a harness CLI but no local ACP adapter). This
  is fixture noise, not a product bug: expect a `<harness>:shared@<gateway>` adapter
  key in /version with a climbing failure count and adjudication chatter. Match
  circuit polls on the EXACT satellite adapter key (`codex:shared@sat-e2e-<host>`) —
  a loose grep will read the gateway key's circuit mid-S4.
- S4 status (until tasks #16/#19 land): the reason clause FAILS today by design of the
  defect (bare :task_crash instead of adapter_unavailable) and the resident-session
  recovery clause FAILS (adjudication hold with no visible decision surface). Keep
  reporting them as FAIL — they are product defects under repair, not oracle problems.

> **AMENDED 2026-08-12:** adjudication holds were deleted 2026-08-05; judge
> the resident-session recovery clause against the ruled contract — the turn
> fails by name, publishes the reason, records it — not against a hold
> surface. See `adjudication-deletion-amendment.md`.

## The journeys (oracles gate-cleared against real surfaces)

Runnable in three isolated groups (`e2e-tier-map-v1` T3), so a targeted run costs
minutes rather than the full pass: **T3a placement** = S1–S3; **T3b fault + reinstall** =
S4–S5 (needs T3a's resident session in the same run); **T3c negatives** = N1–N3
(independent). S6 teardown runs in EVERY run, including one where you ran a single group
and including one that failed. The safety rails and credential requirements above apply
to every group.

S1 **Assimilate cold** — NOTE: assimilate creates the satellite base_dir WITHOUT your
   RUN_MARKER — write the marker into it immediately after every assimilate/
   re-assimilate, or teardown will rightly refuse the removal (hit in lnx-0725c/d and
   mac-0726a). FIRST bootstrap an admin on the fresh org (run lnx-0725b:
   REGISTER refuses "admin required" on a fresh base_dir — pair a device over the run
   gateway's ws (cold-start rule: first paired user is admin); this is part of S1, not
   a workaround). Then `assimilate <ssh-dest>` with your run-owned `--base-dir` →
   hosts.json on the gateway gains the satellite entry (config entry — hosts are never
   DB rows); shipped CLI + adapter executables exist and are executable at your install
   path on the satellite. (No homes/doctor assertions — those don't exist at
   assimilate time.)
S2 **Session on satellite** — credential projection + the authenticated registry
   preflight above (presence alone is not a pass); install a run-owned
   archetype `sat-e2e-<runid>` whose `where` admits the satellite (the shipped default
   admits eezo/tars/racter only); `spawn --host <satellite>` with it; drive one turn →
   turn completes; `inspect.sessions[].host` names the satellite; the session's
   workspace and delivered home exist on the satellite — DERIVE the paths via the
   `Placement.workdir_path/2` and `Homes.home_path/3` conventions from session key +
   registered base_dir (spawn/inspect return no paths); the session workspace path
   does NOT exist on the gateway (the gateway's staged baseline home DOES exist by
   design — don't flag it).
S3 **Workspace motion** — the session's turn writes a nonce file in its workspace →
   SSH content check on the satellite matches; no copy at that path on the gateway.
S4 **Adapter death** — chmod -x your run-owned adapter executable on the satellite;
   kill its exact PID (lineage-matched); wait for that adapter key's circuit to OPEN
   in `/version` adapter health (`generation`, `circuit`, `consecutive_failures`);
   another turn on the resident session terminalizes `failed` with the degraded-adapter
   reason (NOT failed_unknown; no synchronous dispatch refusal exists — don't assert
   one). Restore the executable; circuit closes; a subsequent turn completes.
S5 **Reinstall (linux only)** — remove ONLY your two run roots on the satellite (no
   unit ops, no uninstall verb — neither exists); re-assimilate → same hosts.json key
   re-registered (replace-in-place; no supersession semantics); S1's oracle passes
   again; authenticated credential preflight returns `:live` (store was outside
   deletion scope).
S6 **Teardown (ALWAYS, even after failures)** — reachable satellite: your test gateway
   process gone (exact PID), its SSH adapter children gone, port free; remote session
   workspaces deleted VIA SSH (retire does not remove them); both run roots removed on
   both hosts (marker-checked); protected-surface post-checks pass; lock released.
   Unreachable satellite: report exactly what you created there (your creation notes)
   as named residue and FAIL the run naming it — never silent.

## Fixture bare-metal policy (Flynn-directed 2026-07-25)

The DELETABLE satellites (eurisko, eliza) start every e2e run BARE. The fixture reset
is a SANCTIONED RAIL CATEGORY with an exact pinned path list (like the lockfile
exception — rails are precision, not blanket prohibition; an agent may rm ONLY these
exact paths, on deletable satellites only, and only when NO onboarding tmux session
(claude-onboard/codex-onboard) is live — if one is, SKIP the reset, record the live
inventory instead):
  ~/.local/bin/claude   ~/.local/lib/node_modules/@anthropic-ai/claude-code/
  ~/.local/bin/codex    ~/.local/lib/node_modules/@openai/codex/
Record what was removed (or the skip + inventory) in the scorecard so nothing silently leans on
pre-installed tooling and the positive journeys prove tightbeam's OWN bring-up
(assimilate-shipped adapters + projected credentials) end to end. CREDENTIAL STORES
(~/.claude, ~/.codex) PERSIST — they are the onboarding product, deliberately outside
fixture scope; credential ABSENCE is tested at the projection seam (below), not by
deleting stores. Exemptions: shrdlu and racter (Flynn: needed for other things), tars
(OpenClaw production provider host) and eezo (dev/orchestration host, live sessions) —
on those, absence is created per-run via PATH-scoped environments, never global
removal; the run-owned gateway still installs its own confined harness CLI in its
install root (the lnx-0725a pattern). Model catalog: the gateway reads
homes/<HOSTNAME>/<harness>/models_cache.json — keyed by the gateway's hostname, NOT the
literal "local"; a wrong key degrades silently at boot (:missing_cache) and bites at
spawn (lnx-0725b workaround 4).

## Negative journeys (Flynn-directed 2026-07-25: missing dependencies are test
material, not just blockers — "a good opportunity to test what happens if dependencies
like harnesses and oauths aren't available")

Each asserts the product REFUSES CLEANLY with a named, actionable error — never a hang,
crash, or half-configured state. Run 1 (lnx-0725a) proved N1/N3 accidentally; they are
now first-class. All rails apply (incl. eliza's Subetha three-way when touching eliza).

N1 **No node on satellite** — assimilate against eliza (the permanent negative fixture:
   no node anywhere) → PROBE fails first, exit nonzero, message names node and the
   remedy ("install node and retry"); NOTHING is created on the satellite (verified —
   run 1 evidence: PROBE precedes any satellite write); hosts.json unchanged.
N2 **No harness credential at the projection seam** — the substrate reads credentials
   from the registered base_dir's auth/<harness>, so N2 is host-state independent:
   simply DO NOT project claude into the run base_dir (no symlink), attempt a claude
   spawn → refused with the pinned onboarding error naming the harness, host, and
   remedy; no session row leaks into active state; no remote workspace created. (This
   stays valid even after the host gains a ~/.claude store — the seam under test is
   tightbeam's, not the host's.) KNOWN DEFECT until task #17 lands: on a host
   assimilated after gateway boot the refusal comes out as the catalog masquerade
   ("cannot validate model...") because credential validation fails open with no
   Credentials server — a gateway restart produces the true pinned refusal (run
   lnx-0725c evidence). Post-#17, no restart may be needed and the masquerade form is
   itself a FAIL.
N3 **No harness CLI on gateway** — boot a run-owned gateway from an env whose PATH has
   no harness CLI → boot refuses with the named error (gateway.ex:387 family) listing
   what it looked for; no port bound, no partial base_dir daemon left running.

## macOS environment (mac-0726a)

No `setsid` — detach with `( nohup … & )`. TARS has system Elixir 1.20.2/OTP29 and
cargo 1.94 — no install-root toolchain dance; only the confined harness-CLI install
applies. PATH-scoped absence recipe: shim dir of symlinks (elixir/erl/mix + node/npm),
PATH=$shim:/usr/bin:/bin — homebrew bin must be OFF PATH for N3.

## Scorecard (report format)

Pairing, hosts, harness+model, runid; per journey: verdict + evidence (command outputs,
paths, timestamps) + workarounds; protected-surface pre/post results; residue: NONE or
named. The run is clean only if every journey in scope passed and residue is NONE.

COMMIT the scorecard to `tightbeam_ex/docs/smoke-runs/<date>-<gateway-sha>-satellite-<pairing>-<runid>.md`
in the `TEMPLATE.md` v1 schema, with the header carrying `Tier`, `Scope` (which groups
ran), `Wall clock`, and `Runid`. Verdict cells: `PASS`, `PASS (workaround: …)`,
`FAIL(note)`, `INCOMPLETE(blocker)`, `SKIP(reason)`. A run report alone is not filing —
`e2e-tier-map-v1` §Scorecards is the rule.

## History

r1-r3 were spec rounds for a scripted driver; Flynn redirected to agent-executed
runbook (scripts rot; agents adapt). The oracle/rail content survived unchanged — the
gate work was about WHAT to verify and what's safe, which is executor-independent.
