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

## Machine choice, with reasons (AMENDED v2.1 per Mike's correction:
## shrdlu and tars are THE test machines; gibson hosts the live org and is
## NOT a test machine — its isolated install and tarball are preserved
## evidence and a reusable build artifact, not an execution venue)

| Lane | Host | Why | Executor |
|---|---|---|---|
| S | shrdlu, NEW isolated install (operator account clu per TEST-HOSTS.md; own base dir, port 12374) | ONLY host with BOTH claude and codex credentials → the cross-harness switch battery lives here; also holds a real intact 0.1.7 state.db for the non-destructive stamp-refusal test; ABSORBS the former gibson scope (now S7-S9) | tester:release018-shrdlu-e2e |
| T | tars, darwin tarball, isolated | darwin-aarch64 package has no live verification yet; finding 10 rules the form (tmux foreground, NEVER LaunchDaemon for claude turns) | shrdlu tester via ssh, after S goes green; light scope |

Gibson-recorded evidence (refusal battery, vendor-verbatim reporting) is
PRESERVED and cited; the tb018-build tarball may be REUSED as the install
artifact on shrdlu if byte-identical to the CI package (verify sha256
against the proof manifest before reuse — else install from the CI
package).

The live org install and port 11373 are untouchable everywhere. Credential
files are never read; the CLI is the only sanctioned path; secrets via
stdin only.

## Exact scope

(v2.1: former gibson G lane moved to shrdlu as S7-S9; gibson executes
nothing further.)

SHRDLU (S lane — the release theme lives here):
- S1. Fresh isolated 0.1.8 install from the linux tarball, account clu,
  own base dir, port 12374. Finding 14 trap: `cargo build --release` before
  any e2e driver use. Smoke drop-in EFFORT_CHECKIN_HORIZON_MS=2500 where
  the smoke requires it.
- S2. Onboard claude AND codex (credentials exist on shrdlu; stdin flows).
- S3. CROSS-HARNESS SWITCH BATTERY (the release theme): claude -> codex ->
  claude via the tune verb on a live session. ACCEPTANCE (v2.2, review
  finding 1 — tune-verb success alone is NOT green): (a) a real COMPLETED
  TURN on each leg — claude before any switch, codex after the first
  switch, claude after the switch back — with turn ids captured; (b)
  continuity proven by a transcript read: the pre-switch history present
  as record and the pointer visible at the swap boundary; (c) NO
  auto-replay demonstrated: the post-switch transcript contains no
  re-injected history, and self-read happens only on demand and bounded.
  The three named refusals re-proven (same_harness, unknown_harness,
  needs_onboarding), each with its exact refusal text.
- S4. Finding 22 re-check on 0.1.8: the codex J5 commit-ordering journey.
  If it reproduces unchanged, record and keep OPEN (known, not a
  regression); if it worsens, surface to mike before continuing.
- S5. STAMP-REFUSAL acceptance, non-destructive: snapshot shrdlu's intact
  0.1.7 state.db via the SQLITE ONLINE BACKUP method from a READ-ONLY
  connection (v2.2, review finding 2 — a plain file copy of a live DB is
  not a defined-consistent snapshot):
  `sqlite3 'file:<orig>?mode=ro' ".backup <scratch>/state.db"`. Point the
  isolated 0.1.8 gateway at the SNAPSHOT; expect the named refusal citing
  model-identity-message-envelope-v2 and this-build
  operator-decision-requests-v1. UNTOUCHED-ORIGINAL PROOF required:
  sha256 of the original state.db, -wal, and -shm plus an ls -la of the
  auth/ dir, captured BEFORE and AFTER the whole S5 exercise —
  byte-identical or the test is void regardless of the refusal outcome. (This is the ONLY upgrade-adjacent test in scope — the
  upgrade PATH itself has no tool yet; that is Phase 0 on mike's queue and
  explicitly NOT this plan's scope.)
- S6. Credential-incident codex half where re-onboarding is possible: a
  deliberately failed onboarding must NOT restore the previous credential
  silently; the circuit must not gate credential installation. Record both.
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
- T1. darwin-aarch64 tarball installs isolated; finding 10 form (tmux
  foreground); one real claude turn; version identity as G3.

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
- watchdog:release-018-completion audits evidence against this scope —
  every line above either has evidence or a named skip with a reason.
- The product owner's spirit acceptance closes the plan: features verified
  against the release theme (switching proven live) and gh#11 semantics.

## User decisions required

NONE new. The two adjacent decisions already sit on mike's queue and are
not re-asked here: (1) Phase 0 schema-upgrade tool before live-org deploy;
(2) rc-machinery DELETE ruling. F22 escalates to mike only if it worsens
on 0.1.8.
