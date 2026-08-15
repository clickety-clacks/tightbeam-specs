# 0.1.8 release/test plan v2 (replacement)

Author: product-owner:tightbeam (mike's direct assignment, 2026-08-15).
Supersedes: the withdrawn tb02-executed gibson route. Nothing from that plan
is executed; its already-recorded evidence is PRESERVED and cited below.
Routed to: watchdog:release-018-completion (completion audit) and
tester:release018-gibson-e2e (gibson lane executor). Same TB02 context was
delivered to all three parties.

## What is under test

Tag v0.1.8 at becb130 (immutable; CONTRIBUTING.md freeze-by-abandonment —
test failures produce 0.1.9 fixes, never a tag change). CI proof and
boundary review already stand (run 31872013477, att_a14c0afb). This plan
verifies the FEATURES on live installs; it does not re-prove the build.

Already-standing evidence (preserved, not re-run):
- shrdlu/tars T2b client journeys on the line: claude 18/18, codex 17/18
  (finding 22 outstanding) — e2e-cold-install-2026-08-14.md.
- Gibson isolated install (port 12373): refusal battery PASSED
  (same_harness, unknown_harness, needs_onboarding); vendor-verbatim
  failure reporting observed (credential-incident fix proven in release).

## Machine choice, with reasons

| Lane | Host | Why | Executor |
|---|---|---|---|
| G | gibson, EXISTING isolated install (base ~/tb018-test/home, port 12373) | already running v0.1.8 with claude onboarded + catalog live; codex EXCLUDED here (gibson ~/.codex quota dead until Aug 20; onboarding incomplete) | tester:release018-gibson-e2e |
| S | shrdlu, NEW isolated install (operator account clu per TEST-HOSTS.md; own base dir, port 12374) | ONLY host with BOTH claude and codex credentials → the cross-harness switch battery lives here; also holds a real intact 0.1.7 state.db for the non-destructive stamp-refusal test | tester:release018-shrdlu-e2e (staffed by the product owner on plan routing) |
| T | tars, darwin tarball, isolated | darwin-aarch64 package has no live verification yet; finding 10 rules the form (tmux foreground, NEVER LaunchDaemon for claude turns) | shrdlu tester via ssh, after S goes green; light scope |

The live org install and port 11373 are untouchable everywhere. Credential
files are never read; the CLI is the only sanctioned path; secrets via
stdin only.

## Exact scope

GIBSON (G lane — claude-side, no codex until quota returns):
- G1. gh#11 operator decision requests, full lifecycle on the isolated
  install: file (--key idempotency retry), list, recommend (proxy label,
  non-resolving), rule (owner-only; non-owner refusal named), withdraw,
  supersede. Evidence: exact commands + row states per step.
- G2. Cap-removal check (efb8a653): spawn past the old ceiling on the
  isolated org; record the count reached and the absence of the old refusal.
- G3. Version identity: gateway/CLI handshake reports 0.1.8 and the
  build number per CONTRIBUTING (`<version> build N`, N = rev-list count at
  becb130). If the runtime surfaces no build number, record that as a
  FINDING (the stamp is packaging-level in 0.1.8), not a failure.

SHRDLU (S lane — the release theme lives here):
- S1. Fresh isolated 0.1.8 install from the linux tarball, account clu,
  own base dir, port 12374. Finding 14 trap: `cargo build --release` before
  any e2e driver use. Smoke drop-in EFFORT_CHECKIN_HORIZON_MS=2500 where
  the smoke requires it.
- S2. Onboard claude AND codex (credentials exist on shrdlu; stdin flows).
- S3. CROSS-HARNESS SWITCH BATTERY (the release theme): claude -> codex ->
  claude via the tune verb on a live session; the three named refusals
  re-proven here (same_harness, unknown_harness, needs_onboarding);
  continuity semantics observed and recorded: history preserved as record +
  pointer at the swap, bounded self-read available, NO auto-replay.
- S4. Finding 22 re-check on 0.1.8: the codex J5 commit-ordering journey.
  If it reproduces unchanged, record and keep OPEN (known, not a
  regression); if it worsens, surface to mike before continuing.
- S5. STAMP-REFUSAL acceptance, non-destructive: COPY shrdlu's intact
  0.1.7 state.db to a scratch path; point the isolated 0.1.8 gateway at the
  copy; expect the named refusal citing model-identity-message-envelope-v2
  and this-build operator-decision-requests-v1. The original 0.1.7 install
  is never touched. (This is the ONLY upgrade-adjacent test in scope — the
  upgrade PATH itself has no tool yet; that is Phase 0 on mike's queue and
  explicitly NOT this plan's scope.)
- S6. Credential-incident codex half where re-onboarding is possible: a
  deliberately failed onboarding must NOT restore the previous credential
  silently; the circuit must not gate credential installation. Record both.

TARS (T lane — light, after S green):
- T1. darwin-aarch64 tarball installs isolated; finding 10 form (tmux
  foreground); one real claude turn; version identity as G3.

Known flakes: O4 is documented — one retry allowed, logged as O4 when seen.

## Out of scope (named, not silent)

- Live-org deploy of v0.1.8 (mike's window; blocked on Phase 0 schema
  upgrade — fresh-install evidence does NOT cover the upgrade path).
- Overlay reconcile-survival and toolchain-PATH smokes (deploy-gated,
  they run against the LIVE org after deploy).
- Any codex activity on gibson before Aug 20 (quota).
- Building the schema upgrade tool (separate item, mike's nod pending).

## Evidence and completion

- All evidence lands in the specs repo, findings-bank style (exact
  commands, ids, timestamps), committed per batch; this file is amended
  with a scorecard per lane.
- watchdog:release-018-completion audits evidence against this scope —
  every line above either has evidence or a named skip with a reason.
- The product owner's spirit acceptance closes the plan: features verified
  against the release theme (switching proven live) and gh#11 semantics.

## User decisions required

NONE new. The two adjacent decisions already sit on mike's queue and are
not re-asked here: (1) Phase 0 schema-upgrade tool before live-org deploy;
(2) rc-machinery DELETE ruling. F22 escalates to mike only if it worsens
on 0.1.8.
