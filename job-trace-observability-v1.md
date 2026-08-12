# Job trace observability — v1

Status: READY (Opus-authored 2026-07-25; confirming gate NOT-READY(4) returned only
pin-level residue — prod-turn exclusion, honest pre-boundary stamp, three encodings,
a column-count typo — all folded below; the reviewer confirmed the load-bearing joins
sound (reviewsAssignmentId reaches verdicts; matchedFactAt reconstructible). Cleared
by additive-feature stop-rule.) Trajectory as job-eval→split→descope→minimal: 8→8→9 (split) → 9→8→6
(descope) → this ruthlessly-minimal v1. The repeated finding — "family X keeps no
history / no timestamp / no attribution" — is answered structurally: v1 traces ONLY
families needing ZERO new durability infrastructure; everything that would need a new
column, timestamp, or attribution is named for `job-forensics-v2`. This is an ADDITIVE
feature (new nullable columns + one read verb; no existing behavior changes), low blast
radius; per the review-calibration doctrine it ships with the one residual (exact JSON
key strings) as an implementation-verified proof, not another gate round. Depends on
`work-item-brackets-v1` (job identity).

## Law 0 — no ceremony (binding)

Every record is a SIDE EFFECT of mediated work; no agent writes, supplies, or substitutes
for it. Attests are the one agent-authored record (prior law, untouched); this reads them.

## 1. The four additive columns (the load-bearing, unambiguous value)

`turns` gains FOUR nullable columns via additive ALTER (no rebuild):
- `assignmentId` / `jobRef` — the GATEWAY writes them at enqueue for substrate-caused
  turns WITH a durable attribution carrier at the enqueue site: the dispatch brief and
  the effort notification (both enqueue with assignment context in hand) carry both; a
  bracket-1 nag carries `jobRef` only, `assignmentId` NULL (the firing wake is joined
  to its item via the item's own routingWakeId column — durable reverse pointer, no
  new infrastructure). PROD turns are EXCLUDED in v1 (confirm-gate F1: a prod rides a
  wake that persists no assignment reference; attributing it needs a wake.assignmentId
  column — new durability → job-forensics-v2; prompt parsing is forbidden).
  Conversational turns NULL.
- `model` / `harness` — the executing mind (§2).

These columns ARE the load-bearing forensic joins (turn → assignment → job; which mind
ran which turn). They are valuable and unambiguous independent of the trace verb's shape.

## 2. Mind stamp — record the substrate's OWN decision (Flynn redesign 2026-07-26)

**Flynn ruling (supersedes the verified-boundary design and its live-field amendment):**
"an agent had to select that model to begin with — just record that." The substrate IS
the selector: spawn chose the model, tune changed it, the session row holds it. So the
stamp is a PURE OUR-SIDE WRITE — at turn CLAIM (the moment the lane takes the turn to
run), copy the session's currently-selected model/harness onto the turn row. Claim-time,
not enqueue-time (delta-review D3): a tune can land while a turn sits queued, and the
selection in effect when the turn RUNS is the answer §1's columns exist to give — same
cost, one read in the claim txn. No ACP round-trip, no per-turn read-back, no hot-path
checkpoint, no capability map, no cancel/tune serialization machinery. (The prior
design inserted a verify checkpoint into the prompt/cancel/tune intersection; its first
live smoke killed every claude turn and it was reverted — ff4b64b/e41ac63.)

The honest kernel the old design chased — "what we asked for" can diverge from "what
runs" when an APPLY fails silently (the fable trap) — is an ERROR-HANDLING concern at
the three discrete moments configuration changes (spawn/session-new, load, tune), which
are existing apply call sites. Contract: those three sites make apply failure LOUD —
the failure is recorded (the turn/session error path that already exists; the known
silent-apply gaps at load and resident-session bypass are closed as part of this lane)
— so intent≈reality is enforced where reality can change, once, instead of interrogated
every turn. The stamp's meaning: "the mind the substrate had selected when this turn ran."

Claim-time consequences, named (delta-review follow-up): a turn ENQUEUED but never
CLAIMED (queued at shutdown; drained by queued-retirement cancel) terminates with NULL
model/harness — legitimate, and it means exactly "no mind was ever selected for a run
of this turn"; the trace's turn entries therefore carry model|null, harness|null and a
consumer must read null as "never ran", never as a stale guess. The stamp write lives
IN the claim transaction (the status→running transition), not a follow-up write — a
running turn is never stampless. The stamp has ONE chokepoint: the claim txn (no
enqueue-time write remains).

## 3. Expose — `work-item-trace <id>` (zero-new-durability families ONLY)

Read-only; joins IMMUTABLE references (assignmentId/jobRef), never session/time proximity.
Included — each already durable and job-attributable with NO new infrastructure:
- work item CURRENT state + failReason (brackets — current, not history);
- each assignment (opener, holder, state, files, `reviewsAssignmentId`);
- each attributed turn (status, stamped mind, enqueue/end timestamps);
- attests on those assignments AND on assignments whose `reviewsAssignmentId` points
  into this job (r6-F4: review verdicts are filed on a separate review assignment;
  the trace follows `reviewsAssignmentId` INTO the job so the bad-worker verdict is
  present — the invariant is "a review assignment's attests belong to the reviewed
  assignment's job", enforced by the join, not by requiring the review assignment to
  carry the workItemId);
- decision requests for those assignments (CURRENT state, raisedAt, ruling);
- effort-checkin generations + evidence for those assignments;
- durable wake rows for those assignments: `scheduled`/`fired` with
  createdAt/dueAt/firedAt/firedBy AND the matched `condition_facts.at` for a condition
  fire (self-contained wake-latency material for the consumer).

EXCLUDED from v1 (each needs new durability → named for job-forensics-v2, NOT smuggled):
disposition HISTORY (item keeps current state only — the trace shows current disposition,
no from/to timeline); `wake_canceled` events (no `canceledAt` column exists); subagent
MARKERS (carry no assignmentId today — attribution would need a new emission column); the
overwritten-transition capture (adjudication reopens, rung climbs, prod edges — the
original causal_events, deferred at r6).

**Pinned schema (r6-F5 + confirm-gate F3, REALLY pinned):** the artifact is
`{workItem: {id, ownerUserId, state, failReason, title}, assignments: [{id, holderKey,
openerRef, state, files, reviewsAssignmentId}], timeline: [entry]}`. Encodings pinned:
`openerRef` is the string `"user:"<userId>` or `"session:"<sessionKey>` (from the
mutually-exclusive openedByUser/openedBySession columns); the `assignments` array
INCLUDES review assignments reached via reviewsAssignmentId (they are members, not just
attest sources), sorted by `id` ASC with `files` sorted ASC; `wake_fired.firedBy` is
NULLABLE (timed/internal fires persist NULL — the schema says so rather than promising
a value the substrate doesn't keep). Each `entry` is
`{at: int_ms, type, id, ...typed}` sorted by `(at ASC, then the fixed type rank
[turn_start=0, wake_scheduled=1, wake_fired=2, decision_request=3, effort_generation=4,
attest=5, turn_end=6], then `id` ASC)`. Typed fields, EXACT:
- `turn_start`/`turn_end` {id: turnSeq, assignmentId, jobRef, status, model|null,
  harness|null, at} (null = never claimed, no mind ever ran it) — model/harness are the BARE session-selected strings stamped at claim (no
  confirmation markers; the verified-encoding appendix language is retired with the
  boundary design)
- `attest` {id: attestId, assignmentId, kind, verdict|null, commitRefs|null}
- `wake_scheduled` {id: wakeId, assignmentId|null, dueAt}; `wake_fired` {id: wakeId,
  assignmentId|null, firedBy, matchedFactAt|null}
- `decision_request` {id: requestId, assignmentId, state, ruling|null}
- `effort_generation` {id: "gen:"<assignmentId>":"<generation>, assignmentId, state,
  evidence|null}
The impl checks the artifact against this exact key set as a schema test; a missing or
extra key fails. (This is the one residual carried as a verified proof, not a gate.)

**Authorization:** ADMIN-or-OWNER only (item ownerUserId or admin); every other principal
AND an absent id return `not_found` (no existence leak). Tighter than work-item-get;
named. CLI row in cli-surface.

## 4. `commitRefs` (Flynn-approved rider)

Completion attests gain OPTIONAL `commitRefs` `[{repo: "host:abs-path", commit}]`. When
present, the substrate validates at filing that each commit exists in the named repo
(`git cat-file`), refusing on an unverifiable ref. bisect→commit→commitRefs→attest→trace
is then a checked chain. Structures an existing coder duty; Law-0-clean; carried in the
trace's attest entries.

## job-forensics-v2 (DEFERRED, named)

Adds: disposition transition history (immutable event or an events table); wake
`canceledAt` AND wake `assignmentId` (unlocking prod-turn attribution, excluded from
v1); subagent-marker `assignmentId` attribution at emission; and the
overwritten-transition capture for supervision-internal families (adjudication
reopen/escalate, effort/decision rung climbs, prod fired/answered edges) — each of which
requires FIRST adding job attribution to families keyed on session, not job. v1 gives
the conversation flow, minds, stalls, escalations-as-decision-requests, verdicts, and
current dispositions; v2 gives the fine-grained supervision transition history.

## Non-goals

- No derived metrics/scoring (the trace is a QUERY; golden-jobs computes FROM it).
- No new tables, timestamps, or attribution columns beyond the four on `turns`
  (everything that would need them is job-forensics-v2).
- No agent-visible observability (Law 0). No measured cost (no carrier). No wire frames.

## Required proofs

1. Attribution: dispatch and effort turns carry assignmentId+jobRef; a PROD turn
   carries neither (excluded in v1 — no durable carrier); bracket-1 nag carries
   jobRef (via the item's routingWakeId reverse pointer) with assignmentId NULL;
   conversational turns NULL.
2. Mind stamp: every CLAIMED turn carries the session's selected model/harness as of
   claim time (pure DB write in the claim txn); a tune landing while a turn is queued
   is reflected in that turn's stamp when it runs; a never-claimed turn keeps NULL; a
   failed model-apply at spawn/load/tune is LOUD (recorded, never silent) and does NOT
   persist the unapplied selection — the silent-apply gaps at load and resident-tune
   closed with fail-before/pass-after tests.
3. Trace: the artifact matches the EXACT pinned schema (schema test: missing/extra key
   fails); includes review verdicts via reviewsAssignmentId; wake entries carry
   matchedFactAt so wake latency is computable from the self-contained artifact;
   excluded families (disposition history, wake_canceled, markers) are absent by design.
4. Authorization: owner and admin get the artifact; every other principal and an absent
   id get `not_found`.
5. commitRefs: valid commit passes filing and appears in the trace; nonexistent commit
   refused at filing.
6. Migration: turns gains the FOUR columns via additive ALTER (nullable, no rebuild);
   existing rows preserved; index proof on (jobRef), (assignmentId).

## Component touches

`turns` four-column attribution (enqueue touchpoints) + model/harness stamp in the
ledger's CLAIM txn from the session row (no adapter interaction); loud apply-failure
closures at session-new/load/tune; `work-item-trace` verb
(gateway + router + CLI + cli-surface row) + the exact-schema test; `commitRefs` on the
attest schema + filing-time git validation; observability addendum row for the new turns
columns (substrate-stamped, silent); additive turns migration. PREREQUISITE:
work-item-brackets-v1 merged first.

## Appendix — mind-stamp encoding

`turns.harness` keeps the harness wire name; `turns.model` carries the BARE
session-selected model reference (e.g. `gpt-5.6-sol[medium]`) copied at claim time. No
confirmation markers — the verified/capability encoding was retired with the boundary
design (Flynn redesign: the stamp records the substrate's own selection; apply-failure
loudness at the three config-change sites is what keeps selection≈reality).
