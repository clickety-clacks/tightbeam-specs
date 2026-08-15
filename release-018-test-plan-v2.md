# 0.1.8 release/test plan v2 (replacement)

Author: product-owner:tightbeam (mike's direct assignment, 2026-08-15).
Supersedes: the withdrawn tb02-executed gibson route. Nothing from that plan
is executed; its already-recorded evidence is PRESERVED and cited below.
Routed to: watchdog:release-018-completion (completion audit) and
tester:release018-shrdlu-e2e (S lane; T lane after S green). The former
gibson tester is stood down (lane withdrawn, card surrendered); v2.1
removed gibson as an execution venue.

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
  failure reporting observed. PROVENANCE: VERSION-UNVERIFIED per watchdog
  attestation (asg_2aa46337 — a baseline specimen showed CLI 0.1.8 vs a
  gateway requiring 0.1.7 on that install); cite only as mixed-version
  evidence, nonblocking; shrdlu S3 CONTROLS the refusal surface.

## Machine choice, with reasons (AMENDED v2.1 per Mike's correction:
## shrdlu and tars are THE test machines; gibson hosts the live org and is
## NOT a test machine — its isolated install and tarball are preserved
## evidence and a reusable build artifact, not an execution venue)

| Lane | Host | Why | Executor |
|---|---|---|---|
| S | shrdlu, IN-PLACE REPLACEMENT of the standard install on port 11373, account clu (v2.8/B1 — the earlier isolated-venue clause was stale text from the withdrawn form) | ONLY host with BOTH claude and codex credentials → the cross-harness switch battery lives here; its real 0.1.7 state.db supplies the first-boot stamp-refusal capture; ABSORBS the former gibson scope (S7-S9) | tester:release018-shrdlu-e2e |
| T | tars, darwin tarball, isolated | darwin-aarch64 package has no live verification yet; finding 10 rules the form (tmux foreground, NEVER LaunchDaemon for claude turns) | shrdlu tester via ssh, after S goes green; light scope |

Gibson-recorded evidence (refusal battery, vendor-verbatim reporting) is
PRESERVED and cited; the tb018-build tarball may be REUSED as the install
artifact on shrdlu if byte-identical to the CI package (verify sha256
against the proof manifest before reuse — else install from the CI
package).

GIBSON's live org install and its port 11373 are untouchable. On SHRDLU,
mike's v2.7 correction makes the standard-port install the REPLACEMENT
TARGET — that supersedes the earlier 0.1.7-untouched constraint for
shrdlu only. Credential
files are never read; the CLI is the only sanctioned path; secrets via
stdin only.

## Exact scope

(v2.1: former gibson G lane moved to shrdlu as S7-S9; gibson executes
nothing further.)

SHRDLU (S lane — the release theme lives here):
- S1 (v2.7, MIKE'S CORRECTION — the isolated/parallel form is WITHDRAWN
  and must not be credited): IN-PLACE REPLACEMENT on the STANDARD port
  11373, account clu, with any prior TEST installation removed first (the
  12374 isolated base from the withdrawn form is torn down). The prior
  standard 0.1.7 install is the replacement target. BEFORE first boot (v2.8/B3+I2, MANDATORY): read the real DB's actual
  stamp via a read-only connection (`sqlite3 'file:...?mode=ro' "SELECT
  shape FROM schema_stamp"`) — v0.1.7 stamps model-identity-v1, NOT the
  later message-envelope string, and an unstamped DB yields a ONE-string
  refusal — and take a read-only `.backup` pre-boot copy (the only
  pristine pre-exposure artifact while refuse-before-write is itself
  under test). At first boot the schema stamp refusal fires — capture its
  exact text and expect it to cite THE STRING THE READBACK RETURNED plus
  this build's operator-decision-requests-v1 (not a hardcoded pair), then
  proceed by the sanctioned move-aside path, PRESERVING the moved-aside
  DB as evidence. REPLACEMENT MECHANICS (v2.8/I1, stated not implied):
  stop/remove the 0.1.7 service on 11373 first; state.db and the auth dir
  move aside WHOLE to preserved paths (auth per the v2.7b move-only
  rule); identity/ and homes/ are substrate-owned projections the fresh
  install regenerates — record their fate in evidence either way.
  TEST-HOSTS section-1 clean-start is explicitly SUPERSEDED here by
  mike's in-place ruling: the DB is retained precisely to capture the
  refusal, then moved aside. Finding 14
  trap: `cargo build --release` before any e2e driver use;
  EFFORT_CHECKIN_HORIZON_MS=2500 drop-in where the smoke requires it.
  WHOLE-BASE RESET (v2.9/R2 ruling, superseding the v2.7b auth-only
  scope, which the supplement proved insufficient): the in-place install
  ADOPTS retained state without ceremony (release finding — credential
  continuity while org rows refuse), and the fresh org BOOTED with
  retained auth/identity/homes present, so its own state.db may embed
  the adoption. Therefore: (a0) STOP THE RUNNING 0.1.8 GATEWAY/SERVICE on 11373 FIRST
  (v2.11/I5 — the whole-base move must never run under a serving
  gateway; record the stop in evidence), THEN (a) move aside the ENTIRE
  retained base
  contents — auth/, identity/, homes/, and any residue — preserved
  UNREAD beside the moved-aside DB (move only; names+mtimes trail);
  homes/ retention is NOT an option (v2.10/B5): sweep_auth
  (becb130 homes.ex:316, boot path) harvests homes/*/<harness> into the
  auth store at EVERY boot, so retained homes re-adopt old credentials
  after any auth-only move — whole-base is the only closing form; (b)
  the current fresh state.db is DISCARDED-BY-MOVE-ASIDE too, labeled
  contaminated-fresh; (c) fresh first boot on the clean base (no refusal
  expected — the old DB is gone; S1's refusal capture predates this and
  is UNAFFECTED), then S1b RE-RUNS — this ONE repeat is RULED
  deliberately, not implied; (d) ALL credited credentials originate from
  S2 ceremonies — nothing adopted counts; (e) the armed OAuth ceremony
  targets the pre-reset base: LET IT EXPIRE per the standing protocol
  and re-arm only after the reset, on mike's real-time go.
  STATUS, single-crediting (v2.11 refresh): S1 = CREDITED-WITH-NAMED-LIMIT
  via the transition clause below; S1b = PASSED on the pre-reset base and
  RE-RUNS after the whole-base reset (the re-run is the crediting run);
  isolated-form evidence (7281952/6247d1a) = recorded, not credited.
  TRANSITION CLAUSE (v2.10/B4 — the executed run predates v2.8's
  mandatory pre-boot backup and must not fail audit-at-HEAD forever):
  the already-executed run is CREDITED via compensating proof — pre-boot
  SOURCE_STAMP readback banked; refusal text = readback + build strings
  (vindicated); moved-aside DB inode/mtime/size recorded stable across
  the refusal boot with ACTIVE_DB_PATHS_ABSENT evidence; a POST-exposure
  read-only .backup of the moved-aside DB taken NOW; the pre-exposure
  gap stays a NAMED LIMIT per the owner's acceptance ruling. The
  mandatory pre-boot readback+backup pair binds every FUTURE staging.
  STATUS: S1 evidence from the isolated form (specs 7281952) is MARKED
  UNPROVEN for this acceptance — recorded, not credited; S1b's ceremony
  evidence (6247d1a) is tied to the withdrawn base and must be RE-RUN on
  the replaced install.
- S1b (v2.3, review finding 3): the MANDATORY pair-then-connect ceremony
  per docs/TEST-HOSTS.md section 3a, BEFORE any onboarding or e2e
  evidence. DRIVER FORM PINNED (v2.9/I3): against a service-held standard
  port the driver runs `mix run --no-start` ONLY — dependency apps via
  ensure_all_started on named client deps, never :tightbeam — and the
  exact command goes into evidence (the ceremony is a wire-client act by
  contract; auto-start boots a second app into the held port) — it establishes the admin user and the Main stream; without it
  S2 has no admin to onboard under and the install has no Main. Evidence:
  the ceremony's own output + the resulting admin/Main rows.
- S2 (v2.4, finding 3 — ORDER MATTERS: needs_onboarding has no safe
  fixture once both providers are onboarded): S2a onboard CLAUDE only.
  S2b with codex NOT yet onboarded, drive the needs_onboarding refusal
  naturally (attempt a switch/spawn to codex) and capture its exact text —
  no credential is damaged because none exists yet. S2c onboard codex.
  All after S1b, stdin flows.
- S3. CROSS-HARNESS SWITCH BATTERY (the release theme): claude -> codex ->
  claude via the tune verb on a live session. ACCEPTANCE (v2.2, review
  finding 1 — tune-verb success alone is NOT green): (a) a real COMPLETED
  TURN on each leg — claude before any switch, codex after the first
  switch, claude after the switch back — with turn ids captured; (b)
  continuity proven by a transcript read: the pre-switch history present
  as record and the pointer visible at the swap boundary; (c) NO
  auto-replay proven AT THE ADAPTER BOUNDARY (v2.4, finding 2 —
  transcript rows prove storage, not what reached the destination
  harness): becb130 creates a fresh session/new at switch
  (adapter.ex:691-723) and appends self-read guidance separately
  (gateway.ex:2526-2535); evidence must show the session/new FIRST
  PROMPT carried no prior messages (adapter stderr/debug capture or an
  equivalent boundary artifact), plus the bounded tool-read happening
  only on demand. Refusals re-proven with exact text: same_harness and
  unknown_harness here; needs_onboarding lives in S2b.
- S4. Finding 22 re-check on 0.1.8: the codex J5 commit-ordering journey.
  If it reproduces unchanged, record and keep OPEN (known, not a
  regression); if it worsens, surface to mike before continuing.
- S5: DELETED (v2.8/B2, deletion preferred by the delta review): the
  refusal capture folded into S1's real first-boot flow; the snapshot
  variant needed the withdrawn isolated gateway and is gone with it.
  S5's serving-version pinning exception re-homes to S1 (see pinning).
- S6. Credential-incident codex half where re-onboarding is possible: a
  deliberately failed onboarding must NOT restore the previous credential
  silently; the circuit must not gate credential installation. ACCEPTANCE
  (v2.6 — the circuit half is VACUOUS while the circuit is closed): the
  circuit-does-not-gate proof requires the PRESERVED INCIDENT
  PRECONDITION — codex adapter circuit demonstrably OPEN first
  (e.g. consecutiveFailures at threshold, captured), THEN credential
  install succeeds WITHOUT a gateway restart, the credential fingerprint
  changes with NO prior-credential restore, and durable status/health is
  recorded after. 0.2-build-ledger.md incident-part-2 records this exact
  valid proof shape and the discarded fake passes — match it.
- S7 (was G1). gh#11 operator decision requests, full lifecycle: file
  (--key idempotency retry), list, recommend (proxy label, non-resolving),
  rule (owner-only; non-owner refusal named), withdraw, supersede.
  Evidence: exact commands + row states per step.
- S8 (was G2). Cap-removal check (efb8a653): spawn past the old ceiling on
  the isolated org; record the count reached and the absence of the old
  refusal.
- S9 (was G3). Version identity: gateway/CLI handshake reports 0.1.8 and
  the build number per CONTRIBUTING. If the runtime surfaces no build
  number, record it as a FINDING (packaging-level stamp in 0.1.8), not a
  failure.

TARS (T lane — light, after S green):
- T1. darwin-aarch64 tarball installs isolated UNDER OPERATOR ACCOUNT
  `mike` (explicit per TEST-HOSTS.md — the account rule is part of the
  artifact under test); finding 10 form (tmux foreground, never
  LaunchDaemon); pair-then-connect per section 3a likewise precedes
  evidence; FRESH CLAUDE ONBOARDING on the isolated base per TEST-HOSTS
  section 3b (v2.5 — the existing tars credential belongs to the intact
  0.1.7 install, not this base; without 3b the real turn cannot execute);
  one real claude turn; version identity as S9. NAMED LIMIT
  (v2.4): the foreground form proves the Darwin BINARY journey only — it
  deliberately does NOT prove the LaunchDaemon service mode F10 rules out
  for claude turns; the evidence must state this limit.

Known flakes: O4 is documented — one retry allowed, logged as O4 when seen.

## Out of scope (named, not silent)

- Live-org deploy of v0.1.8 (mike's window; blocked on Phase 0 schema
  upgrade — fresh-install evidence does NOT cover the upgrade path).
- Overlay reconcile-survival and toolchain-PATH smokes (deploy-gated,
  they run against the LIVE org after deploy).
- ANY test execution on gibson (Mike's correction: gibson hosts the live
  org and is not a test machine; its isolated install is preserved
  evidence only).
- Building the schema upgrade tool (separate item, mike's nod pending).

## Evidence and completion

- All evidence lands in the specs repo, findings-bank style (exact
  commands, ids, timestamps), committed per batch; this file is amended
  with a scorecard per lane.
- Every evidence batch is PINNED (v2.4, finding 7): package sha256, plan
  revision commit, host, account, base dir, port, and the serving
  gateway's reported version — unpinned evidence does not count.
  S1 FIRST-BOOT EXCEPTION (v2.8, re-homed from deleted S5): the
  first-boot gateway correctly refuses BEFORE serving, so no serving
  version exists by design for that batch; it pins instead the refusing
  binary's package sha256 and the version/build the refusal output or
  boot log reports — the refusal artifact IS the version evidence.
- MUST-PASS set (v2.4, finding 7 — named skips cannot green the plan):
  S1 (incl. its refusal capture), S1b, S2a-c, S3, S6, S7, S8, S9, T1
  each PASS or the plan is
  BLOCKED/INCOMPLETE, stated as such. S4 alone may close as
  reproduces-unchanged (known finding 22). The watchdog audits against
  plan HEAD at audit time.
- ACCEPTANCE SCOPE (v2.4, finding 6): all evidence here is
  FRESH-INSTALL-ONLY; it does not establish upgrade viability, and the
  LIVE-ORG DEPLOY of v0.1.8 stays BLOCKED on Phase 0 (schema upgrade)
  regardless of how green this plan ends.
- The product owner's spirit acceptance closes the plan: features verified
  against the release theme (switching proven live) and gh#11 semantics.

## User decisions required

NONE new. The two adjacent decisions already sit on mike's queue and are
not re-asked here: (1) Phase 0 schema-upgrade tool before live-org deploy;
(2) rc-machinery DELETE ruling. F22 escalates to mike only if it worsens
on 0.1.8.
