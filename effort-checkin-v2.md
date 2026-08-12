# Effort check-in v2 — attestation-anchored, write-detection, no git requirement

Decided 2026-07-28 (Flynn). Supersedes the v1 implementation's semantics
(dispatch-anchored git-motion brackets). Read §Provenance before touching any
of this — it records the design intent whose loss produced v1's misses.

## Provenance — why v1 missed, so no future agent repeats it

The ORIGINAL intent, in order:

1. **Attestations are the claims.** The mechanism exists to check that
   attestations actually did the work they attest to.
2. **Artifacts are the referents.** After a claim, check whether the thing
   pointed at was actually written.
3. **Git entered for exactly one reason**: "we don't know when a change
   happened to an existing doc" seemed unanswerable. It is answerable:
   record mtimes before work starts and compare. The question is "did it
   WRITE to the file, not what" (Flynn, verbatim). Content-addressing,
   attribution, and diffs were never required.

What v1 built instead: ambient git-motion detection over the workdir,
armed on dispatch. Three unrequested constraints crept in, none ruled:

- "effect" narrowed to *git tree motion* (git became a REQUIREMENT, not
  the optional artifact-control Flynn blessed);
- observation narrowed to *inside the workdir* (Flynn: "I never asked for
  that constraint" — work legitimately happens elsewhere, including over
  ssh on other machines, e.g. standing up a web server);
- substrate-side activity (artifacts, attests, work-item updates) was
  computed as alarm METADATA (`turnsSinceArmed`) but ignored by the
  verdict — an alarm carrying its own refutation.

The standing lesson (recorded in orchestrator memory as
attribute-failures-to-authority-first): when a mechanism misfires, first ask
whether the failing constraint was ever requested. Unrequested constraints
are deleted, not accommodated with more mechanism. The audit that reviewed
v1 misattributed these constraints as "bad design" and proposed pluggable
probes — more machinery to compensate for machinery nobody ordered.

## Clarifications ruled 2026-07-28 (binding on this design)

- Git is a GENERAL change-management system, substrate-blessed for artifact
  control where an org uses it (identity repo, commit-refs evidence). It is
  never a requirement for observation.
- Worktrees are subfolders inside the workdir (the comingling-era sibling
  naming survives by inertia only).
- Work outside the workdir — including on other machines — is legitimate.
  The agent surfaces it by RECORDING ARTIFACTS; explicit declaration beats
  probing.
- mtime with a recorded baseline is sufficient write-detection. Its two
  miss-cases (mtime-preserving ops like cp -p/rsync -a/mv-in-place; clock
  jumps) fail SAFE — a missed write costs one prod, answered by an attest.
- Turns are effort, never effect. A spinning session has turns.

## Design

1. **Arm (on dispatch, as today):** write a stamp file and record a file
   listing of the workdir root. No git anywhere in this path.
2. **Probe (on the horizon wake, as today):** writes-since-stamp =
   `find "$root" -newer <stamp>` plus a listing diff (new paths, deleted
   paths). Portable shell; works on any workspace in any domain.
3. **Verdict:** EFFECT = any of, since armed:
   - writes in the workdir (probe above),
   - an artifact recorded by the holder,
   - an attest on the assignment,
   - a work-item update by the holder.
   The substrate signals use the same watermark query shape the turns count
   already uses. Turns alone are NOT effect.
4. **Prod the AGENT first.** Zero effect on all channels → a wake to the
   HOLDER naming the four channels ("no writes, artifacts, attests, or
   work-item updates observed since <t> — record your work or say what's
   happening"). Only continued silence at the next bracket escalates to the
   owner decision request (existing rungs/backoff unchanged). Owners get
   decisions, not status.
5. **Verification of attested referents — the referents ARE the recorded
   artifacts.** Per Provenance §2 verbatim ("Artifacts are the referents"):
   there is no new naming surface. When an attest lands on an assignment,
   the holder's recorded artifacts are the referents, verified by
   write-detection of each artifact's `originPath` — local stat, or
   `ssh <host> stat` where the origin names a remote host. commit-refs
   verification stays as-is for orgs using git evidence. A referent that
   cannot be checked reports that legibly, per-artifact; it never rejects
   the attest and never blames the credential or the claim.
   (An earlier draft of this clause implied a new `--referents` attest
   input. That was drift past the ruled design — an invented input surface
   on a delete-mechanism change — caught by the implementing lane before it
   was built. Recorded here so it is not reinvented.)
6. **External artifacts survive archival.** `artifact-record` accepts any
   origin (verified: origin_path is opaque at record time). Archival
   currently RAISES on origins outside the session workspace
   (artifacts.ex archived_relative_path!) — fix: such origins are EXTERNAL
   artifacts, marked external/released at archive time; the row is the
   record, there is nothing to take into custody.
7. **Legibility texts:** every prod and alarm names the channels it
   checked. An untracked or absent workspace is stated once as a fact, not
   nagged.
8. **Guidance:** the operating guidance/kungfu instructs agents that remote
   or non-filesystem work becomes observable by recording artifacts.

## Non-goals

- No content diffing, no "what changed" — write-detection only.
- No pluggable probe framework. One mechanism.
- No observation outside the workdir; remote work is declared, not probed.
- No change to bracket arming, rungs, backoff, CAS discipline, or the
  decision-request machinery beyond inserting the agent-prod rung.

## Acceptance

1. **The prod happens when agents neither write, attest, nor record**
   (Flynn's direct question — this test is mandatory): an armed assignment
   whose holder has turns but no writes/artifacts/attests/updates receives
   the agent prod at the horizon; the same setup WITH an artifact recorded
   receives silence. Fail-before demonstrable against v1 (which knows
   nothing of artifacts).
2. An agent doing exclusively remote work that records one artifact is
   never prodded.
3. Continued silence after the agent prod escalates to the owner request
   with evidence naming all four channels.
4. A workspace with NO git repo anywhere: probe works, no `unobservable`,
   no nag.
5. mtime probe: modified file caught; new file caught; deleted file
   caught; the cp -p miss-case documented in the test as accepted-safe.
6. An attest on an assignment whose holder recorded a remote-origin
   artifact verifies that artifact over ssh stat; an unreachable origin
   reports legibly, per-artifact, without rejecting the attest or
   implicating claim or credential.
7. A session with an external artifact archives cleanly; the artifact row
   is marked external, nothing raises.
