# RETIRED 2026-08-04 by Flynn ruling: "there should be no special documentation about gibson. we install the same way as the readme in the repo, like any other user. no special tools or docs for gibson."
# Live decisions were salvaged to ROADMAP.md; everything else here is history.

# Gibson deploy checklist

**Status:** working checklist, opened 2026-08-01 on Flynn's "how close are we" — converts
the estimate into a list. Check items off here; the roadmap points at this file.

Deploy shape: a PROVISIONING RUN ON BARE GIBSON. Not an e2e from a prepared host — the
proven lesson ([[provisioning-needs-a-bare-host]], six blockers hid behind it) is that
setup is only proven by doing it from nothing. The runbook this produces becomes the
install documentation.

## Gate A — code that must be on main first

- [x] Deploy blocker: onboard-path deadlock (merged 2026-07-31)
- [x] Deploy blocker: model divergence — fence + reconciliation (merged 2026-07-31)
- [x] Neutral first boot + learn/unlearn (merged 2026-08-01; the exact fresh-install path)
- [x] Fleet updater + exact-match version handshake + admin gate (merged 2026-08-01)
- [x] Park / durable process identity (F4) — merged 028af86, 2026-08-01
- [ ] Schema collapse (F1+G1) — final CREATE TABLEs only, table-existence guards deleted
      (lane in flight; Flynn ruled dev/test DBs disposable 2026-08-01)

## Gate A — LATENT BLOCKER surfaced 2026-08-01 (fix in flight on drop-schema-shims)

Deleting the table-existence guards exposed that production boot.ex ensures only 4 of
~24 schemas, then runs recovery (recover_retired) that reads `sessions` — a table boot
never creates. It worked until now only because lazy ensure_schema calls elsewhere and
the guards masked it. On a FRESH Gibson database this boot fails ("no such table:
sessions"). Root cause: the complete schema list lived ONLY in test support, so prod
boot and the suite ensured different sets. Fix: one canonical ensure-all in production
that boot AND tests share; boot ensures the full set before any recover_*. This is the
find that justifies doing the deletion before deploy rather than after.

## Gate B## Gate B — the "must become loud" trio (production-gate ruling, item 00)

- [x] Wake self-call failure is durable: wake_delivery_failed EventLog row, not only a
      log line (wakes.ex internal_delivery_failed — verified 2026-08-01)
- [x] Credential revocation records the truth: last_health "revoked" +
      {:needs_onboarding, :revoked} classification (credentials.ex:207/:381 — verified
      2026-08-01; provisional — confirm the teardown path writes it, not only refresh)
- [ ] F1's 24h invisible park: the escalation cursor code is GONE from escalation.ex,
      meaning the mechanism was restructured, not patched — VERIFY the answered-in-
      seconds-parked-24h window is actually closed, and that a parked-past-answer
      session is loud. Needs code reading, not grep.

## Gate C — the artifact-carrier activation gate (0a, ruled by Flynn, R7)

Status three days stale as of opening this checklist; verify current state before
scheduling anything:

- [ ] group-12 denial assertion redesign (was "P2, in review" 2026-07-30)
- [ ] one full-parity journey rerun on linux
- [ ] a macOS T2a run (both-platform scorecards require the carrier era on both)
- [ ] scorecards, with no waiver hiding a failed load-bearing leg

## THE DEPLOY GATE (Flynn ruling 2026-08-01)

The deploy artifact is main's HEAD. THE gate is main's HEAD full-smoked on the SMOKE
machines (shrdlu gating, eurisko for real-harness turns) AFTER each merge lands — not a
branch gate, and not a post-merge mix on eezo. Branch gates (reconciled with main) only
catch regressions before merge; they do not prove what ships. eezo is advisory under lane
load; do not let it stand in for the smoke machines on anything deploy-bound. A branch is
not "done" until main-with-it-merged is green on shrdlu.

## Gate T0 — first-run states (free, and the family's first impression)

Ruled into the e2e runbook 2026-08-01 (e2e-tier-map-v1.md, tier T0). Zero turns.

- [ ] V0 fresh org knows nothing (neutral seed) — covered hermetically and reviewed,
      NOT yet walked on a real host; includes confirming learn/unlearn never forces
      re-onboarding
- [x] V1 no harness installed (eliza) — walked; found crash-dump-on-normal-state and
      doctor's circular dependency on a running gateway
- [x] V2 harness present, no credential (shrdlu) — walked; found doctor exits 0 silent
      on missing credentials and prescribes a provider the CLI refuses
- [x] V3 user already logged in, tightbeam not onboarded (eurisko) — WALKED 2026-08-01,
      verdict CONFUSING. The fact that Tightbeam keeps its own credential and does not
      use ~/.claude or ~/.codex is stated only in buried README service material, never
      at the point of refusal. A first-run user sees "no credential" while `claude` works
      two commands away and concludes the product is broken, not unconfigured. Plus
      doctor exits 0 on a machine where every turn will fail. FIX IN FLIGHT.
- [x] V4a recovery via API key — walked, $0.13; found the catalog needs a restart
- [ ] V4b recovery via subscription — needs a human at a browser, on a test host

- [ ] T2a must gain LEARN-IN-FORCE coverage (post-onboard, needs inference): guidance
      composed into what the agent is served, a rail gating a real turn, a rule denying
      one. T0/V0 covers only the mechanics — files, receipt, exact removal — because
      proving knowledge requires an agent to act. Ordering: onboard, then learn, then
      test the knowledge
- [ ] (superseded framing) T2a must gain learn/unlearn coverage — the verbs landed 2026-08-01 with neutral
      seed and no e2e tier exercises them, yet learn is now on the critical path for
      every new install (proven hermetically + once by T0/V0, nothing repeatable)

## Gate S — smoke proof on the TEST hosts (Gibson does not smoke)

Ruled 2026-08-01: Gibson runs no smoke. There is no special "Gibson build" — the
deploy is just `main` at the chosen commit. The test hosts smoke THAT commit; Gibson
runs the identical commit, trusted because it passed there. Real harnesses live on eurisko (claude +
codex under asdf, plus node); shrdlu has neither installed.

- [x] API-token completes ONE small turn in BOTH harnesses with NO OAuth — PROVEN
      2026-08-01 on eurisko, $0.13: claude authMethod api_key, codex auth_mode apikey,
      isolation via projected config roots verified in code and at runtime; exactly two
      turns in the DB. FINDING filed: model catalog needed a gateway RESTART after
      onboarding to flip live (boot-time missing-credential cache not refreshed by the
      credential heal — dark-factory violation, roadmap).
      (original item:) API-token completes ONE small turn in BOTH harnesses with NO OAuth — the boundary
      the fixture cannot prove. On eurisko, isolated base dir, api-keys banked, one
      minimal turn per harness (claude, codex), proven to route through the delivered key
      and not ambient ~/.claude/~/.codex oauth. Minimal spend: cheapest model, a
      one-token prompt; keys ephemeral; never touch ~/.claude or ~/.codex.
- [ ] Subscription/OAuth completes a turn in both harnesses — the prime path; browser
      ceremony needs a human; run on a test host, not Gibson.
- [ ] Full smoke green on the deploy commit (plain `main`) on the test hosts —
      the same commit that will be copied to Gibson, no Gibson-specific artifact.

## Gate D — the provisioning run itself

- [ ] Add gibson to the host registry (it is not in hosts.json)
- [ ] Adopt the versioned-migration discipline (PRAGMA user_version) — ruled to arrive
      WITH this deploy, when a durable DB first exists; small, deliberate, its own commit
- [ ] Write the bare-host runbook AS the install happens (test-agents-not-test-scripts:
      runbook + flexible agent, not a script)
- [ ] Onboard credentials on gibson through the real ceremony so the machine is usable
      (the subscription/api-token PROOF happens on the test hosts, Gate S, not here).
- [ ] Post-install: full smoke on gibson; satellite assimilation of at least one
      machine; one update-clients sweep to prove day-2 operations from the prod gateway

## After the install — adoption sequence (Flynn ruling 2026-08-01)

First real use of the live Gibson tightbeam is TIGHTBEAM'S OWN DEVELOPMENT running on
tightbeam — dogfood narrow and deep. Operate that way and watch how it behaves before
migrating anything else (the ROADMAP backburner, OpenClaw/Tracker work, other streams)
onto it. Do NOT plan those migrations now; the in-situ evaluation of tightbeam-on-
tightbeam is the gate that decides whether and when they happen. If developing tightbeam
on tightbeam is awkward, that is the finding, discovered on our own work rather than a
family member's.

## Explicitly NOT gating (recorded so nobody re-adds them)

Conformance gaps under ruling (dispatch fiction, model-catalog projection, assignment
capability, artifact release verb, custody guidance); F3 heal re-ruling; end-to-end
deadline propagation; CLI surface ratification; the F3 adapter_heal intermittent
(recorded, cross-branch, needs its own investigation). Flynn's ruling stands: usable
core loop over solving every edge before install.
