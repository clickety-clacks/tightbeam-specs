# Effort check-in v2 — holder-level effect measurement

Decided 2026-07-28 (Flynn). Amended 2026-08-25 for
`wi_a1b6b53b-405a-4438-8c25-c0cd5c8f0c2d`.

This file remains the canonical effort-check-in spec. The 2026-08-25 amendment
changes the measurement grain, effect channels, initial quiet window, and legacy
cutover. It preserves v2's write detection, artifact semantics, holder-first prod,
operational-parent escalation, and Main boundary.

## Goal

Detect a holder that keeps open obligations without producing an observable effect.
Emit one check-in for that holder and attribute it to the holder's open assignments.

Count coordination work as effect. Give a productive holder one 60-minute quiet
window after its latest observed effect. Keep the 15-minute response bracket after a
holder prod so a true stall still reaches the operational-parent chain.

Refuse to classify an owned workspace as zero effect when the workspace observer cannot
measure it. Record that failure as `measurement_unknown` and retry from a fresh baseline.

Delete the obsolete automated effort decision carrier through one typed, restart-safe
cutover. Preserve genuine decision requests.

This amendment adds the holder monitor because deleting effort check-in would lose the
two measured true stalls (`dr_0901f05a`, `dr_6422c904`). Accepting the current mechanism
would preserve a measured seven false check-ins out of nine. A named failure is not an
adequate replacement because the substrate can observe the relevant effects and can
route the resulting stall without asking a mind to classify it.

This spec teaches no new operating-manual pattern. It repairs one existing substrate
production.

## Non-Goals

- Content diffing or classification of the value of an effect.
- Treating turns as effect. Turns remain evidence of effort.
- Probing work outside the holder's workspace. The holder records an artifact for that
  work.
- A statistical cadence model, a learned threshold, or an inference step.
- Changes to the active operational-parent chain, its Main termination, or its existing
  post-prod backoff.
- Changes to artifact referent verification, commit-reference verification, or external
  artifact archival.
- Actor attribution for existing `work_item_events`. This amendment preserves their
  current card-scoped meaning.
- A new decision-request kind or a new operator decision path.
- Treating an unavailable owned workspace as evidence about holder effect.
- Code, release, deployment, identity, or live-org mutation under the policy assignment
  that authored this amendment.

## Terms

- **Holder** — the session named by `assignments.holderKey`.
- **Affected card** — an assignment whose `holderKey` names the holder and whose state is
  `open` in the probe transaction.
- **Holder-card membership** — the interval during which one open assignment belongs to
  one holder monitor. Its join cursor prevents card events from before that interval from
  becoming holder effect.
- **Holder effect** — one event from the closed channel set in Invariant I-04, attributable
  to the holder or to an affected card.
- **Quiet generation** — one holder monitor period that starts from fresh channel
  watermarks and ends after the holder's frozen archetype-selected quiet horizon or when
  the holder produces an effect.
- **Response generation** — the 15-minute monitor period that starts when the substrate
  sends a holder prod.
- **Holder prod** — the first wake sent to the holder after one quiet generation contains
  zero effect.
- **Parent escalation** — one wake sent to the next active operational parent after one
  response generation also contains zero effect.
- **Measurement refusal** — a persisted `measurement_unknown` outcome that states the
  workspace observer could not support an effect verdict. It is neither `effect` nor
  `zero_effect`.
- **Typed legacy effort row** — a `decision_requests` row whose `kind` is `effort`, whose
  `raiserId` is `process:tightbeam`, and whose required effort fields satisfy the current
  schema. Question text and option text do not establish this type.
- **Cutover marker** — the exact unique current-generation index created as the last write
  of the v2 holder-monitor migration transaction. Its presence proves that transaction
  committed.

## Assumptions

A-01. Current source commit `8b4a3df191ca4505bf7e65a2876da23c9e4f4a6c`
keys generations by `(assignmentId, generation)`, arms one wake per assignment, and uses
a 900,000 ms base horizon (`lib/tightbeam/effort_checkin.ex:27-52,92-114,680-731`).

A-02. That source counts workspace writes, artifacts by holder, attests on one
assignment, and metadata updates on one work item. It does not count assignments opened,
decision requests raised or resolved, or wakes sent
(`lib/tightbeam/effort_checkin.ex:905-927,941-960`).

A-03. Existing rows already carry deterministic principals for the added channels:
`assignments.openedBySession`, `decision_requests.raiserSessionKey`, the decision terminal
principal and time fields, and `wakes.creatorSessionKey`
(`lib/tightbeam/assignments.ex:46-76`; `lib/tightbeam/escalation.ex:35-81`;
`lib/tightbeam/wakes.ex:69-92`).

A-04. `work_item_events` identifies the work item and event kind but does not stamp an
actor. The existing effort mechanism counts `metadata` events on the monitored card's work
item. This amendment applies that same rule to the work items of the affected-card set.

A-05. Filesystem observation runs before the verdict transaction. The transaction CASes
the generation and wake before it schedules an action. This amendment keeps that staging
boundary (`lib/tightbeam/effort_checkin.ex:18-20`).

A-06. The coordination fabric already sets a 60-minute seed quiet floor for open
obligations and identifies thresholds per class or archetype as the policy knob
(`coordination-fabric-v1.md:284-296`). The quiet generation adopts that existing floor.

A-07. The measured specimens are durable in the product-owner transcript:

| Source | Observation |
|---|---|
| `s_592ce865-0fa9-4d45-8634-392cd49a580c` | `dr_6dd1ec10` and `dr_d19e098f`: coordination effects occurred while the four-channel verdict reported zero effect. |
| `s_3df2a98a-097e-45fd-a449-143a087839a4` | `dr_4218ff47`: a productive coordinating holder had a 20-minute thinking gap after six attests and three assignment opens; `dr_0901f05a` and `dr_6422c904` had no effect on any named channel across one hour. |
| `s_ec085ca3-1040-43cf-a628-ae983d72a341` | `dr_bbeaa409`, `dr_fb740247`, `dr_c6eea2e7`, and `dr_e2564ae6`: two assignments on one holder emitted two check-ins for the same quiet period; the measured set was seven false and two true. |

A-08. `art_2f8cc9d0`, SHA-256
`3a84107eb1cc43aa22e88af14cdee4bd796a3dfeb661eab85a68028c4bb7ff2e`, established
the typed legacy-cleanup boundary: clean only `kind = effort` rows raised by
`process:tightbeam`; preserve operator, agent, and statute rows. Its branch commit is
`e27ceac6350ff6bcddae49bde5f3368885587dcd`.

A-09. `att_89999558-7cfc-4c89-ae85-801a0d5ffcc5` records defect D. Effort
check-in message `s_ca989727-30ca-458a-bb8a-e7d6fa22fb25` classified the owned
workspace as `unobservable` and still emitted a zero-effect prod. At 08:58:41 PT on
2026-08-25, the workspace contained modified `effort-checkin-v2.md` bytes with SHA-256
`d6e3f35bdd7d8ae6610042e541a8636fe12e83b923c2cf3e0f0fb377e99940da`.

A-10. The current effort ruling writer records `status`, `decision`, `ruledBy`, and
`ruledAt`; cancels the typed deadline wake; and inserts the successor generation in one
database transaction. It does not populate `rulingFactId`
(`lib/tightbeam/effort_checkin.ex:614-657`;
`lib/tightbeam/escalation.ex:1525-1534`).

A-11. Runtime configuration currently maps
`TIGHTBEAM_EFFORT_CHECKIN_HORIZON_MS` to `:effort_checkin_horizon_ms` and tests override
that key as the 15-minute response bracket (`lib/tightbeam/application.ex:262-263`;
`lib/tightbeam/effort_checkin.ex:1204-1205`; `test/runtime_config_test.exs:15,57`).

## Invariants

I-01. The substrate owns at most one current effort generation for one holder. The count
of affected cards does not change that cardinality.

I-02. A generation emits at most one holder prod or one parent escalation. Replay returns
the committed outcome without scheduling another wake.

I-03. The evidence for a zero-effect action records the holder key and the exact affected
card ids, sorted by `(openedAt, id)`. It records no single card as the owner of a
holder-level action.

I-04. The closed holder-effect channel set is:

1. a workspace write detected from the holder workspace baseline;
2. an artifact row whose `createdBySession` is the holder;
3. an attest row whose `bySession` is the holder;
4. a `metadata` work-item event on the work item of an affected card;
5. an assignment row whose `openedBySession` is the holder;
6. a decision request whose `raiserSessionKey` is the holder;
7. a terminal transition on a decision request raised by the holder, or a decision
   transition whose recorded principal is the holder; and
8. a wake row whose `creatorSessionKey` is the holder.

I-05. A terminal decision transition in I-04 is one of the current typed transitions:
`ruled`, `answered`, `returned`, or `withdrawn`. The matching time and principal fields are
`ruledAt`/`ruledBy`, `answeredAt`/`answeredBy`, `returnedAt`/`returnedBy`, and
`withdrawnAt`/`withdrawnBy`. The transition counts for the raiser when its time is newer
than the decision watermark. It also counts for the recorded principal when that principal
is `session:<holderKey>` and its time is newer than the watermark.

I-06. Terminal turns are reported as effort and do not satisfy I-04.

I-07. A quiet generation waits its frozen quiet horizon from the latest observed holder
effect. A database-effect writer observes the holder workspace before it opens its
transaction. An available observation lets that transaction start a new quiet generation;
an unavailable observation follows I-10. A response generation waits its frozen response
horizon from the holder-prod transaction.

I-08. The probe reads affected cards, database channels, and the generation CAS in one
transaction after the staged workspace observation. The transaction commits the verdict,
card attributions, generation transition, and scheduled action together.

I-09. Boot verifies the tables, columns, and indexes needed by each database channel before
it starts monitor consumers. A failed verification returns
`effort_measurement_schema_invalid`. A runtime channel-read failure returns
`effort_measurement_channel_unavailable`. The consumer leaves the wake pending and the
generation armed, so the due-wake sweep can retry it. The failed attempt emits no effect
verdict, holder prod, or parent escalation.

I-10. An unavailable owned workspace produces `measurement_unknown`. The measurement
transaction emits no `effect` or `zero_effect` verdict, holder prod, or parent escalation.

I-11. A measurement refusal records the observer error, holder key, affected cards,
database-channel counts, cause, principal, resume phase, and parent-escalation cursor. It
starts one recovery generation with the quiet horizon.

I-12. An open assignment transfer updates the old holder monitor and the new holder monitor
in the same assignment-mutation transaction. A holder with no open assignments has no armed
effort generation.

I-13. The effort mechanism reports holder inactivity to agents. It creates zero decision
request rows.

I-14. The typed legacy conversion uses row type and persisted principals. It does not read
question text, option text, the request owner, or assignment subject to select a row.

I-15. The conversion changes no operator, agent, or statute decision row. It leaves already
`superseded`, `withdrawn`, and `consumed` effort rows unchanged.

I-16. The migration writes a replacement holder monitor before it terminalizes an open
legacy effort row or cancels the row's deadline wake. A rollback leaves the old row and its
wake usable.

I-17. The holder-level monitor has one mutation seam. Assignment open, transfer, terminal
close, artifact record, attest, work-item metadata event, decision raise, decision terminal
transition, wake creation, probe, holder-prod response, and boot cutover call that seam in
their existing database transactions.

I-18. `:effort_checkin_horizon_ms` and
`TIGHTBEAM_EFFORT_CHECKIN_HORIZON_MS` remain the response-horizon setting and default to
900,000 ms. `:effort_checkin_quiet_horizon_ms` and
`TIGHTBEAM_EFFORT_CHECKIN_QUIET_HORIZON_MS` set the quiet horizon and default to 3,600,000
ms. `:effort_checkin_quiet_horizons_by_archetype` is a map from served-archetype name to a
positive integer in milliseconds and defaults to an empty map. The arm transaction selects
an exact archetype-map value before the global quiet value. Each generation freezes the
selected value at arm time.

## Architecture

### Preserved v2 behavior

P-01. Git remains optional. The workspace probe compares a recorded baseline with the
current listing and mtime-derived digest. Modified, new, and deleted paths are writes.

P-02. Work outside the workspace becomes observable when the holder records an artifact.
The mechanism does not probe an undeclared remote system.

P-03. An attest uses the holder's recorded artifacts as referents. Local paths use local
stat. Remote origins use the existing remote stat path. An unavailable referent produces a
per-artifact report and does not reject the attest.

P-04. An external artifact archives as an external/released row. The archive takes no
filesystem custody of that origin.

P-05. Prod and escalation text names the observed channels. Measurement-refusal evidence
names the unavailable workspace channel. Both forms report terminal-turn count as effort
evidence.

### Holder monitor

R-01. Introduce `effort_checkin_holder_generations`. Its identity is
`(holderKey, generation)`. Its current row stores `state`, `phase`, `armedAt`,
`horizonMs`, terminal-turn watermark, the seven database-channel watermarks, host, root,
workspace baseline, wake id, evidence, parent-escalation cursor, recovery resume phase,
and recovery resume cursor.

R-02. Enforce one current row with an exact unique partial index over `holderKey` where
`state = 'armed'`. The implementation names this index
`effort_holder_one_current_v2` and verifies its SQL, columns, uniqueness, and predicate.

R-03. Introduce `effort_checkin_card_attributions`. Its primary key is
`(holderKey, generation, assignmentId)`. A zero-effect or measurement-refusal transaction
inserts one row for each affected card before it schedules the next generation or action.

R-04. Introduce `effort_checkin_holder_cards`. Its primary key is
`(holderKey, assignmentId)`. Each row stores `workItemId`, `joinedAt`, and the work-item
event cursor captured when the assignment joined that holder. Assignment open, transfer,
and terminal close update membership in the assignment transaction.

R-05. A holder-level monitor wake sets `assignmentId` and `work_item_id` to null. The
holder generation, membership, and attribution rows are the durable source of card
identity. The holder-prod and parent-escalation prompts print the exact sorted affected-card
ids. A probe or retry prompt does not copy card identity.

R-06. Opening the first assignment for an assignee holder creates one quiet generation.
Opening another assignment for that assignee holder leaves its current generation and wake
unchanged. When the opener is a session with an armed holder monitor, the assignment writer
also records one `assignmentsOpened` effect for the opener. A self-open performs both paths
in one transaction and leaves one current generation for that holder.

R-07. Closing or transferring an assignment re-evaluates membership for the old and new
holders. Removing the last affected card cancels the old holder wake with a typed
assignment-lifecycle cause and cancels its generation.

R-08. Each database-effect caller stages a workspace observation before it opens its writer
transaction. The caller passes that observation to `note_holder_effect_in_txn`. The seam
consumes the current generation with a state CAS, freezes post-write database cursors, and
schedules the next holder generation in the caller's transaction.

R-09. Given an observable staged workspace, `note_holder_effect_in_txn` records the exact
database channel as `effect` and starts a quiet generation at the effect transaction time
with the staged baseline. A work-item metadata writer calls the seam once for each distinct
current holder that has membership on that work item. The membership join cursor excludes
events committed before an assignment joined the holder.

R-10. Given an unavailable staged workspace, `note_holder_effect_in_txn` records
`measurement_unknown`, records the known database-channel counts, and starts one
measurement-retry generation. It sets the resume phase to `quiet` because the database
effect is known. It sends no holder prod or parent escalation.

R-11. A quiet probe with an observable workspace and at least one holder effect commits the
evidence and creates one quiet generation with fresh watermarks and baseline.

R-12. A quiet probe with an observable workspace and zero holder effect commits the evidence
and attributions, sends one holder prod, and creates one response generation.

R-13. A response probe with an observable workspace and at least one holder effect creates
one quiet generation. It sends no parent escalation.

R-14. A response probe with an observable workspace and zero holder effect sends one
escalation to the next active operational parent and advances the existing escalation
cursor. The existing backoff and Main termination remain in force.

R-15. Each evidence object has exact top-level fields `holderKey`, `generation`, `phase`,
`outcome`, `affectedAssignmentIds`, `channels`, `workspace`, `turnsSinceArmed`, and
`minutesSinceArmed`. `channels` has exact keys `writes`, `artifacts`, `attests`,
`workItems`, `assignmentsOpened`, `decisionRequestsRaised`, `decisionRequestsResolved`,
and `wakesSent`.

R-16. Each count in R-15 derives from a cursor frozen in the generation row. The writer
freezes the next cursor in the same transaction that consumes the current generation.

R-17. When the staged workspace observation is unavailable, the generation CAS commits
`measurement_unknown` evidence, affected-card attributions, and one
`effort_measurement_unknown` lifecycle event. The event carries `process:tightbeam` as
principal and the observer error as cause. The transaction creates one `measurement_retry`
generation due after the quiet horizon. It stores the consumed phase and parent cursor as
its resume state unless a known database effect changes the resume phase to `quiet`. A retry
that obtains an observable workspace commits `measurement_reestablished`, freezes that
observation as the new baseline, and starts the stored phase with its phase horizon and
stored cursor. A retry that remains unavailable starts one replacement retry generation.
These outcomes send no holder prod or parent escalation.

### Typed legacy cutover

R-18. Application boot verifies the measurement schema and runs the holder cutover before
it starts effort-probe or effort-deadline consumers. The cutover observes holder workspaces,
then runs one database transaction.

R-19. When the cutover marker is absent, the transaction reads current per-assignment
generations, open assignments, and typed legacy effort rows. It creates memberships and one
holder generation for each holder with an open assignment. An observable workspace creates
a fresh `quiet` generation, or a `legacy_recheck` generation when that holder has an open
typed legacy effort row. An unavailable workspace creates a `measurement_retry` generation
whose resume phase is the phase that the observable case would have created.

R-20. A holder with an open typed legacy effort row starts in `legacy_recheck` phase with the
quiet horizon. A zero-effect legacy recheck sends one parent escalation. An effect
returns the holder to quiet phase. This re-measures the old carrier with the corrected
channels before it reports a stall.

R-21. After the replacement holder wake exists, the cutover cancels pending old probe and
deadline wakes with a typed `superseded` disposition, marks current per-assignment
generations canceled, and changes open typed legacy effort rows to `superseded` with a
status CAS.

R-22. For a ruled typed legacy effort row, the cutover changes `ruled` to `consumed` only
when `decision` is `continue` or `dismiss`, `ruledBy` and `ruledAt` are non-null, the row's
deadline wake has a typed decision-transition cancellation, and a successor
per-assignment generation exists for the row's `assignmentId` with a generation number
greater than `effortGeneration`. These fields prove the original
atomic ruling transaction committed; effort rows do not require `rulingFactId`. A failed
predicate returns `effort_legacy_ruling_incomplete`; boot stops before monitor consumers
start.

R-23. The transaction creates `effort_holder_one_current_v2` last. On later boots, the
cutover validates the exact index and checks that no open typed legacy effort row or current
per-assignment generation remains. A mismatch returns `effort_holder_cutover_conflict` and
starts no monitor consumer.

R-24. The old per-assignment generation table remains queryable as history after cutover.
The runtime writer does not insert another row into it.

R-25. Cutover replay with the marker present creates no wake, generation, attribution, or
decision transition. A stale old probe or deadline wake that fires after cutover loses its
state CAS and performs no action.

### Traceability

| Requirement | Source | Verification |
|---|---|---|
| I-01 through I-03, I-12, R-01 through R-07 | duplicate specimens `dr_bbeaa409`, `dr_fb740247`, `dr_c6eea2e7`, `dr_e2564ae6` | AC-07 through AC-10, AC-31 |
| I-04 through I-08, I-17, R-08 through R-16 | channel specimens `dr_6dd1ec10`, `dr_d19e098f`; cadence specimen `dr_4218ff47`; true stalls `dr_0901f05a`, `dr_6422c904` | AC-01 through AC-06, AC-11 through AC-13, AC-26, AC-27 |
| I-09 | current database-channel readers | AC-28 |
| I-10, I-11, R-10, R-17 | defect-D specimen `att_89999558`, SHA-256 `d6e3f35b…` | AC-14, AC-15, AC-25, AC-30 |
| I-13 through I-16, R-18 through R-25 | `art_2f8cc9d0` | AC-16 through AC-20, AC-30 |
| I-18 | current response-horizon configuration | AC-29 |
| P-01 through P-05 | original v2 provenance and acceptance | AC-21 through AC-24 |

## Acceptance

AC-01. Given a holder opens an assignment during a quiet generation and produces no
effect on the original four channels, when the assignment transaction commits, then the
consumed generation records `assignmentsOpened` as one and `effect` as its outcome. A new
quiet generation exists and no prod or parent escalation exists. This reproduces the
omitted coordination channel in `dr_d19e098f`.

AC-02. Given a holder raises a decision request during a quiet generation, when the holder
workspace observation is staged and the decision transaction commits, then the consumed
generation records
`decisionRequestsRaised` as one and starts a new quiet generation. The transaction emits no
zero-effect action. This reproduces `dr_6dd1ec10`, `dr_d19e098f`, and the `dr_6089ef63`
timeline cited with them.

AC-03. Given a decision request raised by the holder is ruled during a quiet generation,
when the ruling transaction commits, then `decisionRequestsResolved` is one and the
transaction emits no zero-effect action.

AC-04. Given a holder rules a request raised by another session during a quiet generation,
when the ruling transaction commits with `ruledBy = session:<holderKey>`, then
`decisionRequestsResolved` is one and the transaction emits no zero-effect action.

AC-05. Given a holder sends one immediate wake, one timed wake, or one condition wake in
three separate fixtures, when each wake transaction commits, then its consumed generation
records `wakesSent` as one and starts one new quiet generation. The transaction emits no
zero-effect action.

AC-06. Given the `dr_4218ff47` fixture has six attests and three assignment opens in the
hour before a 20-minute thinking interval, when 15 and 20 minutes have passed since the
latest effect, then no effort wake exists. When 60 minutes pass with no later effect, then
one holder prod exists.

AC-07. Given one holder has two open assignments from the `dr_bbeaa409` and
`dr_fb740247` fixture, when one quiet generation contains zero effect, then one holder prod,
one response generation, and two attribution rows exist. Two prods do not exist.

AC-08. Given one holder has the two open assignments from `dr_c6eea2e7` and
`dr_e2564ae6`, when one quiet generation contains zero effect, then the evidence contains
both ids in `(openedAt, id)` order and names no primary assignment.

AC-09. Given a holder has 70 open assignments, when one quiet generation contains zero
effect, then the database contains one holder generation, one holder prod, and 70
attribution rows. It contains zero effort decision requests.

AC-10. Given another session opens a second assignment for a holder 30 minutes into the
holder's quiet generation, when the assignment transaction commits, then the existing wake
id and generation remain unchanged. At probe time the new assignment appears in the
affected-card set.

AC-11. Given the `dr_0901f05a` fixture has zero writes, artifacts, attests, work-item
metadata, assignment opens, decision-request activity, and wake sends for 60 minutes, when
the quiet probe commits, then one holder prod exists with eight zero channel values.

AC-12. Given the `dr_6422c904` fixture has the same full-channel silence, when the holder
prod receives no effect for the 15-minute response generation, then one parent escalation
exists and no decision request exists.

AC-13. Given a holder writes one workspace path after a holder prod, when the response
probe commits, then a new quiet generation exists and no parent escalation exists.

AC-14. Given the exact `att_89999558` fixture has modified owned-workspace bytes at SHA-256
`d6e3f35bdd7d8ae6610042e541a8636fe12e83b923c2cf3e0f0fb377e99940da` and the
workspace observer returns unavailable, when the probe consumes its generation, then the
evidence outcome is `measurement_unknown`. One `effort_measurement_unknown` lifecycle
event and one recovery generation exist. A `zero_effect` outcome, holder prod, parent
escalation, and effort decision request do not exist.

AC-15. Given the AC-14 recovery generation and an observable workspace on its next probe,
when the probe commits, then the evidence outcome is `measurement_reestablished`, that
observation becomes the workspace baseline, and the stored `quiet` phase resumes. The probe
sends no holder prod or parent escalation.

AC-16. Given one holder has three current per-assignment generations and two open typed
legacy effort rows, when cutover commits, then one `legacy_recheck` holder generation and
one wake exist. The three old generations are canceled. The two effort rows are
`superseded`. Their old pending wakes carry typed superseded dispositions.

AC-17. Given the AC-16 database after commit, when application boot runs cutover again,
then row counts and wake ids are byte-for-byte unchanged.

AC-18. Given one open operator row, one open agent row, one open statute row, and one open
typed effort row, when cutover commits, then the first three rows are byte-for-byte
unchanged and the effort row follows R-21.

AC-19. Given a ruled typed effort row has `decision`, `ruledBy`, `ruledAt`, and a typed
deadline cancellation but lacks a successor generation for its referenced assignment,
when cutover runs, then boot returns `effort_legacy_ruling_incomplete`. It creates no marker
and starts no monitor consumer.

AC-20. Given process loss before the cutover transaction commits, when boot retries, then
the old generations, decision rows, and wakes remain usable until one complete transaction
creates the replacement monitor and marker.

AC-21. Given a workspace without a Git repository, when a file is modified, created, or
deleted after arm, then the workspace channel reports a write. The probe does not invoke
Git.

AC-22. Given a holder performs remote work and records one remote artifact, when the quiet
artifact transaction commits, then the artifact channel reports one effect, a new quiet
generation exists, and no prod exists.

AC-23. Given an attest refers to a recorded remote artifact whose origin is unreachable,
when referent verification runs, then it records the per-artifact failure and preserves the
attest.

AC-24. Given a session owns an external artifact, when session archival runs, then the
artifact row becomes external/released and archival completes without taking filesystem
custody.

AC-25. Given a response generation has parent cursor `p3` and its workspace observation is
unavailable, when the measurement retry later obtains an observable workspace, then the
new generation has phase `response`, parent cursor `p3`, and the frozen response horizon.
No quiet generation, prod, or parent escalation is created by recovery.

AC-26. Given a quiet generation is due at minute 60 and the holder records an artifact at
minute 59, when the artifact transaction commits with an observable staged workspace, then
the old generation records `effect` and the replacement quiet generation is due 60 minutes
after the artifact transaction. No wake remains due at the original minute 60.

AC-27. Given assignment B joins a holder on work item W after W already has one metadata
event, when W receives no later metadata event, then B's membership cursor excludes the old
event. Given W receives one metadata event after B joins, when that writer commits, then the
holder records one `workItems` effect rather than one effect per assignment on W.

AC-28. Given the artifact channel table is missing at boot, when schema verification runs,
then boot returns `effort_measurement_schema_invalid` and starts no monitor consumer. Given
the table becomes unreadable after boot, when a due probe reads it, then the probe returns
`effort_measurement_channel_unavailable`, leaves its wake pending and generation armed, and
emits no verdict or action.

AC-29. Given no effort horizon environment values, when runtime configuration loads, then
the response horizon is 900,000 ms and the quiet horizon is 3,600,000 ms. Given the existing
`TIGHTBEAM_EFFORT_CHECKIN_HORIZON_MS=303` fixture, when runtime configuration loads, then
the response horizon is 303 ms and the quiet horizon remains 3,600,000 ms. Given a holder's
served archetype is `product-owner` and the archetype map contains
`product-owner: 5,400,000`, when the holder generation arms, then its frozen quiet horizon
is 5,400,000 ms while an unmapped archetype freezes 3,600,000 ms.

AC-30. Given cutover finds an open typed legacy effort row and the holder workspace is
unavailable, when the cutover transaction commits, then one `measurement_retry` generation
exists with `legacy_recheck` as its resume phase. A legacy zero-effect verdict and parent
escalation do not exist.

AC-31. Given one holder has assignments A and B and a quiet probe returns zero effect, when
the probe transaction commits, then its internal probe wake has null assignment and work
item ids, while the holder-prod prompt lists A and B in `(openedAt, id)` order.

## Open Questions

None. This amendment rules the measurement grain, effect set, quiet and response windows,
affected-card attribution, and legacy cutover required for implementation and review.
