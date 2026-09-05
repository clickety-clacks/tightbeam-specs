# Prodder provenance v1

Status: bounded F1/F2 successor under `att_01f72a7e`; awaiting fresh independent exact-artifact review

Authority:

- Work item `wi_e27eb1a6-0cc3-4d3b-92e7-430f94171fcc`.
- Owner rulings `att_e5b64758` and `att_260adeca`.
- Recon evidence `att_aa4c9117` and `art_5d92d28f`.
- Changes requested in `att_032120da` and review report `art_a68bebe7`, whose reviewed bytes had SHA-256 `de0708…` as recorded by the assignment. The retired review artifact is no longer readable; this spec relies on the durable review attest and does not claim to reproduce its bytes.
- Source baseline `19a50e47aa9e7d0a8ff474321102cd890a7dd0c7`.
- Independent review verdict `att_df4ea9b8-175f-4e89-be04-59a4a63d3c3c` and exact report `art_1d204d8a`, SHA-256 `5bcac973c84942a213a7941784a8b70c389a38c241a4f290e0b6280fbb4e3b88`.
- Corrected-artifact review verdict `att_8175790d-3c5d-46f0-82d9-c26226e7496c` and exact report `art_7ebef755`, SHA-256 `7033290d27f5a53f5a252763c7344db087a93d79b0f40c2fa0806bdd867cffd7`.
- Round-four review verdict `att_2aa31efe-6e3c-4cd8-ba34-d149f23a0d65` and exact report `art_ede58e43`, SHA-256 `77f1912d1d551ae5ac888c8cc228f583357b92e010f600ede6870d3675538b5b`.
- Final exact-artifact review verdict `att_c4b4367b-c1aa-44e0-a5cf-96160052b09a` and exact report `art_52840b4c`, SHA-256 `ff64f50e08ae1914f1b2f64b6b3865ff666ca816ce6ef10e73dc904d0c57cb47`.
- Bounded successor authority `att_01f72a7e-de07-4b74-b212-e293dfdf72e2`; changes-requested verdict `att_c27b9873-6df0-4b44-9276-e7e4f7745188` and evidence report `art_f6b57667`, SHA-256 `954b914e042a6e83d6ec2e031d1ae18c536530d4fd1e81e64ac345c228c0fda2`.

This spec is a bounded amendment to `production-machine-v1.md`, `supervision-v1.md`, `supervision-impl-v1.md`, and `job-trace-observability-v1.md`. It supersedes only these conflicting clauses:

1. `supervision-impl-v1.md` permits a duplicate schedule followed by a separate clear. R11 replaces that ordering with one settlement transaction.
2. `supervision-impl-v1.md` describes `prodCount` as delivered wakes. R12 defines the counter from committed schedule settlements and committed refunds.
3. `production-machine-v1.md` suppresses a fault from the standing `user-alerted` value without retaining the matched fact. R24–R25 require an exact cause observation.
4. `supervision-impl-v1.md` says a database from before that build boots unchanged. R2 replaces that promise only for the first v1 release entry: a legacy pending branch refuses the new release before Supervision starts.
5. `supervision-impl-v1.md` requires exactly one recovery sweep on each Supervision boot or restart. R34 replaces that rule only for a release entry refused before the Supervision child starts, which runs zero Supervision sweeps. After the R1 index commits the cutover, each Supervision start retains the parent requirement to run exactly one sweep.

All other clauses in those specs remain live.

## Goal

Make each supervision prod attempt explainable from durable facts without changing the existing elevation policy.

The result shall answer five questions for one attempt:

1. Which session did supervision select?
2. Which session received the turn?
3. What terminal turn or typed no-turn outcome ended the attempt?
4. Which raw facts caused that result?
5. Did the existing fault-bubbling path admit or suppress the resulting failure?

The implementation shall preserve the parent elevation demonstrated by owner evidence `att_e5b64758`. It shall make the narrower terminal, suppression, and elevation provenance durable and legible.

Subtraction ruling: ADD wins because the owner requires the existing supervision and elevation behavior to remain while its unexplained outcomes become durable. DELETE would remove required supervision or elevation. ACCEPT would preserve the owner-ratified provenance defect.

Review-ratchet re-derivation: the principle remains one durable explanation for one new supervision attempt. The design keeps one immutable attempt carrier only because the live pending tuple is destroyed before the outcome exists. The bounded F2b successor keeps one additional schedule-basis carrier for a settled prod schedule only because the unchanged `prod_fired` row has no attempt backreference; deleting it makes the exact escalation trigger facts unjoinable without chronology. It keeps one final observation only because the owner requires that outcome. Deleting the attempt carrier loses B1 inputs. Deleting the schedule-basis carrier loses the exact raw trigger relation. Deleting the final observation loses the result. Accepting any loss preserves the defect. D1 uses a quiescent upgrade gate because a second recovery path loses. E1 makes the required R1 index the cutover-completion marker and places its exclusive creator in the non-bypass `Boot` → `Schema.ensure_all` path; another row or worker loses. D2 deletes the redundant denial-event backpointer. D3 maps each existing rules result and retains its existing action. D4 deletes the historical-absence subsystem. The design adds no carrier discriminator, absence row, worker, recovery state, or historical product.

## Non-Goals

1. This spec does not create a second escalation machine, recovery process, sweeper, queue, or retry policy.
2. This spec does not change the prod tier sequence, timing, caps, prompts, target policy, liveness policy, lineage walk, bubble recipients, terminal alert policy, or model policy.
3. This spec does not add a cause-scoped standing condition fact.
4. This spec does not infer a failure class from error text, timing, adapter name, model name, exit status, or another proxy.
5. This spec does not change the default `work-item-trace` response keys, entry keys, value types, ordering rules, or authorization behavior.
6. This spec does not migrate, classify, or report attempts claimed before the successful R2 upgrade gate. The versioned read surfaces return only v1 observations.
7. This spec does not auto-retry a terminal turn. `failed_unknown` remains terminal.
8. This spec does not change product behavior merely to make a fixture pass.
9. This spec does not implement, dispose, or mutate live work. It defines the implementation contract.
10. The one-time R2 quiescent upgrade gate runs automatically at the first v1 release entry. Its only operator action is the bounded old-binary drain in R2 after a refusal. It requires no substrate-manual amendment.

## Terms

### Prod attempt

A **prod attempt** under this v1 contract is one evaluation claimed after the R2 transaction commits the exact R1 index. It uses the persisted `pendingBranch` held in `supervision_watermarks` for one assignment, one holder terminal turn, one branch, and one tier or rung. The attempt begins when the current claim transaction persists that tuple. It ends at one terminal turn or one no-turn outcome from the closed set in this section.

### Attempt identity and deterministic wake identity

The implementation shall form these bytes:

```text
"prodder-v1" NUL assignmentId NUL decimal(holderTerminalTurnSeq)
NUL branch NUL decimal(k) NUL decimal(counterEpoch)
```

`branch` is one of `prod`, `escalation`, or `terminus`. `k` is the persisted `pendingK`. `counterEpoch` is the exact `assignment_prods.attestCount` committed by the claim transaction. No component is inferred from a timestamp.

The attempt identifier and wake identifier are the same value:

```text
w_pd_e + decimal(counterEpoch) + "_" + lowercase_hex(SHA-256(attempt identity bytes))
```

The identifier names the attempt even when no wake row is created.

### Attempt carrier

The **attempt carrier** is one immutable `lifecycle_events` row written by the claim transaction before any settlement can clear or overwrite the pending tuple. Its `kind` is `prodder_attempt_v1`. Its `subject` is the attempt identifier. Its canonical JSON `detail` is the exact R5 `attempt` object. `detail.id` and the carrier subject are the same deterministic wake identifier. `detail.workItemId` is a string or JSON `null`. The version lives in the row kind, so the carrier has no redundant `schema` key. The deterministic wake identifier lives in `detail.id`, so the attempt object has no redundant `wakeId` key.

The attempt carrier is an immutable input fact. It is not the final cause observation. The final cause observation shall copy `carrier.detail` into `observation.detail.attempt` byte-for-byte after decoding and canonical re-encoding. The implementation shall not add or remove a key. It shall not rebuild that object from a cleared watermark, current assignment row, prompt text, timestamp adjacency, or current counter.

For `branch = "escalation"`, `detail.triggerBasis` is the exact ordered raw-fact array defined by R6. For every other branch it is the empty array. The claim transaction freezes this array before it writes the carrier. A later settlement shall not recompute it.

### Prod schedule-basis carrier

The **prod schedule-basis carrier** is one immutable `lifecycle_events` row written only for a successfully settled prod-branch schedule. Its `kind` is `prodder_schedule_basis_v1`. Its `subject` is the prod attempt identifier. Its canonical JSON detail has exact keys `attemptId` and `causalEventId`. `attemptId` equals its subject. `causalEventId` is `"ce:"` followed by the decimal `causal_events.seq` inserted by the same R11 transaction. This carrier adds no decision, counter, retry, or target state. It is the deterministic backreference from a prod attempt to the existing raw `prod_fired` row.

### Counter epoch

The **counter epoch** is the incorporated-attest count in `assignment_prods.attestCount`. The existing claim transaction advances it only when `Assignments.attest_count` exceeds the stored value. In that transaction, it appends the exact unseen `prod_answered` causal events in attest-id order, then stores the new `attestCount` and resets `prodCount` to zero. The attempt identifier freezes the stored count. A later fire can compare that frozen value with the current row without comparing timestamps or adding recovery state.

### Work-item binding

`attempt.workItemId` is the exact nullable `assignments.workItemId` value read by the claim transaction. A bound assignment stores its work-item identifier. An unbound assignment stores JSON `null`. Both cases write a carrier and a final observation. The assignment-versioned read surface in R31 makes an unbound observation retrievable. Supervision shall not refuse or skip an attempt because `workItemId` is null.

### Selected target

The **selected target** is the target result frozen when the attempt reaches R10 dispatch selection or R15 pre-schedule settlement. It is one of:

```json
{"kind":"session","sessionKey":"<exact sessions.sessionKey>"}
```

```json
{"kind":"none","reason":"<selected-none reason>"}
```

The closed `selected-none reason` set is:

- `assignment_closed_before_schedule`
- `holder_retired_before_schedule`
- `work_blocked_before_schedule`
- `lineage_exhausted_before_schedule`
- `self_terminus_before_schedule`
- `dispatch_denied_before_schedule`

For a scheduled wake, the selected session is the exact `wakes.sessionKey` written by the schedule transaction. A selected target is not evidence of delivery.

### Delivered target

The **delivered target** is the session that owns the turn created from the prod wake. It is one of:

```json
{"kind":"session","sessionKey":"<exact turns.sessionKey>"}
```

```json
{"kind":"none","reason":"<delivered-none reason>"}
```

The closed `delivered-none reason` set is:

- any selected-none reason
- `work_blocked_at_fire`
- `target_unavailable_at_fire`

For a created turn, `deliveredTarget.sessionKey` shall equal `turns.sessionKey`. It may differ from `wakes.sessionKey` because the existing delivery edge can re-resolve lineage after selection.

### Terminal turn

A **terminal turn** is the unique `turns` row joined by the deterministic wake identifier whose status is one of:

- `delivered`
- `canceled`
- `failed`
- `failed_unknown`

Its typed value is:

```json
{
  "kind":"turn",
  "seq":123,
  "status":"failed",
  "startedAt":null,
  "endedAt":1700000000000,
  "error":"exact stored error or null"
}
```

`startedAt: null` plus a raw `status: "failed"` records failed-before-start. The substrate shall not replace those fields with an inferred class.

### No-turn outcome

A **no-turn outcome** proves that the attempt ended without a joined `turns` row. Its typed value is:

```json
{"kind":"no_turn","outcome":"<no-turn outcome>"}
```

The closed and total no-turn set is:

1. `assignment_closed_before_schedule`
2. `holder_retired_before_schedule`
3. `work_blocked_before_schedule`
4. `lineage_exhausted_before_schedule`
5. `self_terminus_before_schedule`
6. `dispatch_denied_before_schedule`
7. `work_blocked_at_fire`
8. `target_unavailable_at_fire`

A transient dispatch exception, transaction rollback, or delivery exception is not terminal. It leaves the persisted pending attempt available for replay. An unrecognized state is an invariant violation, not an `other` outcome.

### Raw matched fact

A **raw matched fact** names a persisted source lookup, its stable key, and the exact columns returned to a decision. It has this returned-row shape:

```json
{
  "source":"turns",
  "key":{"seq":123},
  "fields":{"status":"failed","startedAt":null,"error":"exact stored error"}
}
```

When an exact stable-key lookup returns no row and that absence causes a typed outcome, the fact shall retain the same `source` and every equality predicate in the exact lookup `key` and shall set `fields` to JSON `null`:

```json
{"source":"sessions","key":{"sessionKey":"s_owner","state":"active"},"fields":null}
```

A no-row fact records the transaction-snapshot lookup result. It is not an inferred class.

Allowed `source` values are `lifecycle_events`, `causal_events`, `supervision_watermarks`, `assignment_prods`, `assignments`, `wakes`, `turns`, `sessions`, `condition_facts`, and `events`. The observation shall copy only fields or the no-row result read for that decision. It shall not parse, summarize, classify, or replace them.

### Cause observation

A **cause observation** is the single append-only `lifecycle_events` row for one prod attempt. Its `kind` is `prodder_outcome_v1`. Its `subject` is the attempt identifier. Its `detail` is canonical JSON in the schema defined by R5.

### Fault recognition

`faultRecognition` reports how the existing bubble production treated the terminal result. It is one of:

```json
{"kind":"not_applicable_no_turn"}
```

```json
{"kind":"not_admitted","terminalStatus":"delivered"}
```

```json
{"kind":"not_admitted","terminalStatus":"canceled"}
```

```json
{
  "kind":"suppressed_user_alerted",
  "matchedFact":{"id":203,"ts":1700000000000,"kind":"user-alerted","scope":"mike","origin":"process:tightbeam"}
}
```

```json
{
  "kind":"admitted",
  "causeTurnSeq":123,
  "action":{"kind":"notice_enqueued","recipientSessionKey":"s_parent","wakeId":"bubble:123:s_parent"}
}
```

The closed admitted `action.kind` set is:

- `notice_enqueued`
- `terminal_alert_committed`
- `none_parentless`

The value records the existing bubble result. It does not authorize a new escalation decision.

The exact admitted action schemas are:

```json
{"kind":"notice_enqueued","recipientSessionKey":"s_parent","wakeId":"bubble:123:s_parent"}
```

```json
{"kind":"terminal_alert_committed","ownerUserId":"mike","lifecycleEventId":456,"conditionFactId":203,"ownerMarkerSeq":789}
```

```json
{"kind":"none_parentless"}
```

`ownerMarkerSeq` is an integer when the owner main stream exists and JSON `null` when it does not. Each action object shall contain only the keys shown for its kind. `lifecycleEventId` names the committed `lineage_exhausted` row. `conditionFactId` names the committed `user-alerted` assertion. `wakeId` names the existing deterministic bubble wake.

An admitted `faultRecognition` object shall have exact keys `kind`, `causeTurnSeq`, and `action`. `kind` shall equal `admitted`. It shall contain no other key.

The closed `not_admitted.terminalStatus` set is `delivered` and `canceled`.

## Assumptions

1. The claim transaction can read `supervision_watermarks.pendingAssignment`, `lastEvaluatedTerminal`, `pendingBranch`, `pendingK`, and `pendingN`, `assignment_prods.attestCount`, `assignments.workItemId`, and the holder session key needed to write the attempt carrier before any settlement clears the pending tuple.
2. `wakes.wakeId` is unique. `turns.wakeId` is unique. These constraints provide the existing wake and turn idempotency seams.
3. The current delivery edge may re-resolve a lineage wake. Therefore `wakes.sessionKey` and `turns.sessionKey` can differ without corruption.
4. The current turn ledger has one terminal transition per turn. The existing terminal publication hook and `BubbleSweeper` republish committed terminal rows after a crash.
5. `condition_facts` is append-only. The current standing value derives from the latest matching assert or retract row.
6. `lifecycle_events.kind` accepts new values. Its `detail` accepts canonical JSON text. Adding indexes does not require a table or column migration.
7. The default job-trace shape is pinned by exact-key tests.
8. Source commit `19a50e47aa9e7d0a8ff474321102cd890a7dd0c7` contains the seams and real fixture paths cited in Acceptance.
9. Each packaged or direct release command that starts the application starts `Tightbeam.Boot` after `Tightbeam.DB` and before the Supervision server or wake scheduler. `Tightbeam.Boot.start_link/1` calls `Tightbeam.Schema.ensure_all/1` before it opens the boot epoch or runs recovery.

If an assumption is false, the implementer shall stop the affected scope and amend this spec before changing behavior.

## Invariants

### I1 — Existing policy remains authoritative

The implementation shall not create a prod tier, escalation rung, recipient rule, failure classifier, or retry rule. It shall observe the decisions made by the existing supervision and bubble productions.

### I2 — One attempt has one identity

The persisted attempt tuple shall derive one deterministic identifier and one immutable attempt carrier. A replay shall reuse both. A settled prod schedule shall also have one immutable R11 schedule-basis carrier under the same subject. The attempt-carrier detail and the final observation's attempt object shall be equal canonical bytes. A call that presents the same identifier with different attempt-carrier or schedule-basis bytes shall fail with `prodder_observation_conflict` and shall not mutate a wake, counter, pending branch, turn, or observation.

### I3 — Selection and delivery remain separate

The observation shall carry both typed target values. It shall not copy the selected target into the delivered target. A turn join is the only source for a session-valued delivered target.

### I4 — Terminal outcome is total

Each settled attempt shall carry exactly one terminal value: one joined terminal turn or one member of the closed no-turn set. A settled attempt shall not carry neither form or both forms.

### I5 — One append-only observation

One attempt shall have exactly one `prodder_attempt_v1` carrier and exactly one `prodder_outcome_v1` final observation. A prod attempt whose schedule settles shall also have exactly one `prodder_schedule_basis_v1` carrier; other attempts shall have none. The final row shall carry the cause identifier and principal. The principal is `process:tightbeam`. The actor is `Tightbeam.Supervision`.

### I6 — Raw facts remain raw

`failureBasis` shall contain the exact matched facts. It shall not contain an inferred class such as `adapter_failure`, `model_failure`, `fast_failure`, `pre_start_failure`, or `retryable`.

### I7 — Facts and actions converge after a crash

Each settlement transaction shall commit its listed durable writes as one unit. A replay after that transaction rolls back, or after process loss following its commit, shall converge to the same carrier, wake row, turn row, pending state, counter, and observation as one uninterrupted settlement. The R13 action phase shall retain the existing rule-effect transactions, CAS, dedupe, rewake, recovery, deny-first summons, and fail-soft semantics. It shall also retain the existing crash window between a deny-plus-escalation settlement and its summons. This invariant does not strengthen those existing effects into a new exactly-once action guarantee.

### I8 — The counter does not drift

For one assignment in current counter epoch E, where E is the stored `assignment_prods.attestCount`:

```text
prodCount = schedule settlements frozen to E - applied work_blocked_at_fire refunds frozen to E
```

Each schedule settlement contributes at most one. Each scheduled attempt contributes at most one same-epoch refund. The existing progress-reset transaction advances E and resets `prodCount` to zero after it appends the corresponding `prod_answered` facts. A fire from an older epoch contributes no refund to the current epoch. A pre-schedule no-turn outcome contributes zero. `target_unavailable_at_fire` consumes its committed slot and contributes no refund.

### I9 — The default trace is unchanged

The default `work-item-trace` result shall retain its exact key sets and value types. The new provenance shall appear only on the separately named versioned surfaces in R30.

### I10 — Existing recovery owns replay

After the exact R1 index records a completed cutover, each later application start shall skip the R2 pending query and start the existing Supervision recovery sweep. The existing pending-branch drain, wake scheduler, terminal publication hook, and `BubbleSweeper` shall recover v1 writes. The implementation shall not add a prodder provenance sweeper or recovery process.

### I11 — One mutation seam per state

The schedule-settlement seam shall own the pending clear and schedule counter increment. The fire-suppression seam shall own the cancel and refund. The provenance constructor shall own insertion of each closed lifecycle kind in R3. Other call sites shall invoke those seams.

## Architecture

### 1. Observation storage

R1. `Tightbeam.ProdderProvenance.ensure_cutover/1` shall be the exclusive creator and verifier of this exact index:

```sql
CREATE UNIQUE INDEX lifecycle_prodder_subject_once_v1 ON lifecycle_events(kind, subject) WHERE kind IN ('prodder_attempt_v1','prodder_schedule_basis_v1','prodder_outcome_v1')
```

The statement has no `IF NOT EXISTS` clause. `EventLog.ensure_schema/1` shall ensure the `lifecycle_events` table and its pre-v1 indexes but shall not create this index. The committed exact index is the sole durable cutover-completion marker; this contract adds no completion row. A same-name row shall have `type = 'index'`, `tbl_name = 'lifecycle_events'`, and `sql` equal to the shown statement byte-for-byte. A missing index with duplicate `(kind, subject)` pairs for any named kind, a wrong same-name row, or unequal SQL shall return `prodder_schema_conflict`. The seam shall not accept an index by name alone or choose a duplicate-row winner.

R2. `Tightbeam.Schema.ensure_all/1` shall call `Tightbeam.ProdderProvenance.ensure_cutover/1` as its final schema step on each application entry. The seam shall run one database transaction and first read `sqlite_schema` for `lifecycle_prodder_subject_once_v1`.

When the exact R1 index exists, the seam shall return `:already_complete` without executing the pending-branch query in this requirement. It shall write no row or index. This is the later-start path.

When the R1 index is absent, the seam shall reject duplicate pairs as specified by R1 and execute this exact query in the same transaction:

```sql
SELECT sessionKey, lastEvaluatedTerminal, pendingBranch, pendingAssignment, pendingK, pendingN
FROM supervision_watermarks
WHERE pendingBranch IS NOT NULL
ORDER BY sessionKey ASC
```

The first-entry gate succeeds only when that result is empty. When it is nonempty, the seam shall return this exact decoded shape, with one `pending` item per query row:

```json
{
  "code":"prodder_upgrade_not_quiescent",
  "pending":[{
    "sessionKey":"s_holder",
    "lastEvaluatedTerminal":123,
    "pendingBranch":"prod",
    "pendingAssignment":"asg_1",
    "pendingK":1,
    "pendingN":3
  }]
}
```

Each value shall equal its stored value; a nullable stored value shall appear as JSON `null`. The transaction shall roll back without creating the R1 index. `Schema.ensure_all/1` shall propagate the refusal through R34, so the v1 writer, Supervision server, and wake scheduler remain stopped.

When the first-entry query is empty, the same transaction shall execute the exact R1 statement, reread `sqlite_schema`, verify the exact definition, and commit. It shall return `:cutover_completed`. That index commit is the cutover boundary. A process loss before commit leaves the index absent and reruns the first-entry gate. A process loss after commit leaves the exact index present and uses the later-start path.

After a nonempty refusal, the operator shall restart the old binary, run its existing pending-branch drain until the query is empty, stop the old evaluator and scheduler, and start the v1 release again. The seam shall not create a carrier for a pre-v1 pending tuple or add an upgrade worker, row, discriminator, recovery state, or historical observation.

R3. `EventLog` shall expose one transaction-bound constructor for the closed kinds `prodder_attempt_v1`, `prodder_schedule_basis_v1`, and `prodder_outcome_v1`. The constructor shall receive a validated typed value. It shall encode canonical JSON and insert the requested kind and subject. The claim edge is the only caller for `prodder_attempt_v1`. The R11 prod schedule settlement is the only caller for `prodder_schedule_basis_v1`. The outcome-settlement edges are the only callers for `prodder_outcome_v1`.

R4. On a concurrent uniqueness conflict, the constructor shall read the stored JSON in the same transaction. It shall return the existing row only when the decoded stored value equals the proposed typed value. Otherwise it shall return `prodder_observation_conflict` and roll back the caller transaction. A replay that begins after settlement shall read the observation before it reads mutable decision inputs. It shall require the decoded observation `attempt` to equal the decoded immutable `prodder_attempt_v1` carrier detail. It shall require the observation `schema` to equal `prodder-provenance-v1`. For a terminal turn, it shall validate the wake and turn join. For a fire-time no-turn outcome, it shall validate the wake and absence of a joined turn. For a pre-schedule no-turn outcome, it shall validate that no wake or turn exists for the attempt identifier. It shall return the stored observation after those checks. It shall not recompute a past decision from a watermark, prompt, current standing fact, or current counter.

R5. The canonical JSON shall have this exact top-level schema:

```json
{
  "schema":"prodder-provenance-v1",
  "attempt":{
    "id":"w_pd_e0_<sha256>",
    "workItemId":"wi_…",
    "assignmentId":"asg_…",
    "holderSessionKey":"s_…",
    "holderTerminalTurnSeq":123,
    "branch":"prod",
    "counterEpoch":0,
    "tier":1,
    "rung":null,
    "prodLimit":3,
    "triggerBasis":[]
  },
  "actor":{"actorRef":"Tightbeam.Supervision","principalRef":"process:tightbeam"},
  "selectedTarget":{"kind":"session","sessionKey":"s_parent"},
  "deliveredTarget":{"kind":"session","sessionKey":"s_parent"},
  "terminal":{"kind":"turn","seq":124,"status":"delivered","startedAt":1699999999000,"endedAt":1700000000000,"error":null},
  "faultRecognition":{"kind":"not_admitted","terminalStatus":"delivered"},
  "failureBasis":[
    {"source":"lifecycle_events","key":{"kind":"prodder_attempt_v1","subject":"w_pd_e0_<sha256>"},"fields":{"detail":"exact canonical attempt carrier bytes"}},
    {"source":"wakes","key":{"wakeId":"w_pd_e0_<sha256>"},"fields":{"assignmentId":"asg_…","sessionKey":"s_parent","state":"fired"}},
    {"source":"turns","key":{"seq":124},"fields":{"wakeId":"w_pd_e0_<sha256>","sessionKey":"s_parent","status":"delivered","startedAt":1699999999000,"endedAt":1700000000000,"error":null}}
  ]
}
```

R6. `tier` shall be the persisted positive prod tier for branch `prod` and `null` otherwise. `rung` shall be the persisted positive escalation rung for branch `escalation` and `null` otherwise. `prodLimit` shall be the persisted limit used for the attempt. `counterEpoch` shall be the exact non-negative `assignment_prods.attestCount` stored by the claim transaction. `workItemId` shall be the exact assignment value: a string when bound and JSON `null` when unbound. R5 shows the bound form. The encoder shall emit the shown keys even when their values are `null`.

For `branch = "escalation"`, `triggerBasis` shall contain exactly two raw matched facts for each tier from 1 through `prodLimit`: the existing `prod_fired` `causal_events` row and the unique terminal `turns` row for that tier's deterministic prod attempt identifier. The claim transaction shall derive each prior prod attempt identifier from the current escalation attempt's exact `assignmentId`, `holderTerminalTurnSeq`, `counterEpoch`, and tier. It shall join the exact `prodder_schedule_basis_v1` row by that identifier, then join `causal_events` by its recorded `causalEventId` and `turns` by `wakeId = prior attempt identifier`. Each causal fact shall copy exact `seq`, `at`, `jobRef`, `assignmentId`, `sessionKey`, `kind`, and decoded `detail`. Each turn fact shall copy exact `seq`, `wakeId`, `sessionKey`, `status`, `startedAt`, `endedAt`, and the complete stored `error` value. The claim shall refuse with `prodder_observation_conflict` and write nothing when a required carrier, event, turn, join, or terminal status is missing or unequal. It shall not choose a fact by timestamp, array position, note text, or nearest-row inference. Every non-escalation attempt shall use `triggerBasis: []`.

R7. Canonical JSON shall use UTF-8, lexicographically sorted object keys at every depth, preserved array order, base-10 integers, JSON `null`, and no insignificant whitespace. The code blocks in this spec show decoded values for readability. The read surface shall decode the JSON before returning it.

`triggerBasis` and `failureBasis` shall each contain no duplicate `(source, key)` pair. The encoder shall sort each array by this source rank, then by the canonical JSON bytes of `key`: `lifecycle_events`, `causal_events`, `supervision_watermarks`, `assignment_prods`, `assignments`, `wakes`, `turns`, `sessions`, `condition_facts`, `events`. This is the only permitted array order.

### 2. Attempt claim and deterministic scheduling

R8. The existing claim transaction shall remain the only writer of the pending attempt tuple. When it observes new attests, it shall preserve the current order: append each unseen `prod_answered` causal event in attest-id order, then store the new `assignment_prods.attestCount` and zero `prodCount`. For a non-prod claim, the transaction shall read the exact target-walk result in its snapshot and use that result to choose the persisted `escalation` or `terminus` branch. For an escalation claim, it shall build and validate the exact R6 `triggerBasis` in that same snapshot. It shall then derive the identifier from the values in that transaction and write or verify the exact `prodder_attempt_v1` carrier before commit. The carrier shall copy the nullable `assignments.workItemId`. The stored `attestCount` is the counter epoch for the attempt.

After it writes the carrier, the claim transaction shall evaluate R15 items 1–5 in the same snapshot. When one matches, that transaction shall run the R15 settlement, including the matching raw facts, before commit. In particular, the exact target result that chooses the persisted `terminus` branch shall produce `self_terminus_before_schedule` when it names the holder and `lineage_exhausted_before_schedule` when it names no eligible target. The claim transaction shall not collapse those two results into a later evaluation of the shared `terminus` branch. When no R15 item matches, the transaction shall commit the pending tuple, counter epoch, and carrier together for the drain. A claim-time R15 settlement shall commit the counter epoch, carrier, pending clear, and final observation together. The claim transaction shall not increment `prodCount`.

R9. The drain shall read the deterministic attempt identifier and attempt object from the immutable carrier joined through the persisted pending tuple. It shall pass the identifier to the existing wake schedule edge as the wake id and idempotency key. R2 proves that a drained tuple was claimed by the v1 writer. A missing or unequal carrier after that gate is `prodder_observation_conflict`; the drain shall leave the pending tuple intact.

R10. The selected target shall come from the exact dispatch result. A scheduled attempt shall store the selected session in `wakes.sessionKey`. A pre-schedule no-turn outcome shall store a typed none value with its exact outcome reason.

R11. When rules admit the dispatch, one database transaction shall:

1. read and validate the immutable attempt carrier;
2. insert the deterministic wake row, or verify an equal existing wake row;
3. compare-and-clear the matching pending tuple;
4. increment `assignment_prods.prodCount` if this transaction inserted and settled the schedule for the first time;
5. if this transaction settled the schedule for the first time and `attempt.branch = "prod"`, append the existing `prod_fired` causal event with exact detail `{"tier":attempt.tier}`, read its inserted `seq`, and append the exact `prodder_schedule_basis_v1` carrier whose subject is `attempt.id` and whose detail is `{"attemptId":attempt.id,"causalEventId":"ce:" + decimal(seq)}`.

Step 5 shall not run for `escalation` or `terminus`. The causal event and its schedule-basis carrier shall commit together or neither shall exist. If any write fails, the transaction shall roll back. A replay that finds the equal wake and an already settled pending tuple shall require the equal schedule-basis carrier for a prod attempt and return the existing settlement without another event, carrier, or increment.

R12. `prodCount` shall implement invariant I8. The current progress reset remains its reset seam. No terminal turn status shall increment the counter.

R13. Each supervision drain invocation that finds no final observation shall call the existing `Rules.decide` once and retain its exact `{decision, to_close, to_consume}` result. It shall invoke each `to_close` entry in returned order through the existing `RailRemedy.close` or `RailEpisodes.recovered` seam before it settles the attempt. A close exception shall follow R14. For a non-allow decision, the adapter shall leave `to_consume` unused, matching the existing dispatch edge.

The adapter shall preserve this closed result and action map:

| `decision` | Existing action boundary | Adapter result | Denial settlement payload |
| --- | --- | --- | --- |
| `{:deny, error}` | none | `{:error, error}` | exact `error` |
| `{:remedy, statute, ref, error}` | call `RailRemedy.fire` once for this decision evaluation; retain its returned `producer_id` | `{:error, amended_error}` | exact `error` with `reason = "remedy_fired"` and `producer = producer_id`; this value is `amended_error` |
| `{:escalate, statute, ctx, nil}` | before settlement, call `Escalation.escalate` once for this decision evaluation; retain its newly committed `{:decision_pending, id}` | `{:decision_pending, id}` | exact `ctx.error` |
| `{:escalate, statute, ctx, dr_id}` where `dr_id` is a string | call no escalation action | `{:decision_pending, dr_id}` | exact `ctx.error` |
| `{:deny_escalate, statute, ctx}` | commit the denied settlement first; immediately after commit, call the existing fail-soft `RailEpisodes.summon` once in the original invocation | `{:error, ctx.error}` after summons returns | exact `ctx.error` |
| `:allow`, every consume wins | call existing `Escalation.consume` once for each `to_consume` ruling in returned order; each call retains its own transaction; then invoke the existing wake handler once through R11 | exact existing dispatch-handler result | none |
| `:allow`, one or more consumes lose | call existing `Escalation.consume` in returned order until every id has been attempted | `{:error, lost_error}` | exact first-losing-id error below; this value is `lost_error` |

The remedy episode CAS and producer dispatch, escalation one-open-request constraint and notification outbox, and malfunction-episode summon dedupe remain the action owners. The adapter shall not add another action row or worker. It shall run remedy and unattached escalation before the denial settlement. A process loss before that settlement shall leave the pending attempt available for replay through those existing seams. It shall run deny-plus-escalation summons only after its denial settlement commits, matching the existing deny-first boundary. A process loss after that commit and before summons can leave the attempt denied without a summons; replay shall return the committed observation and shall not add the omitted summons. This contract adds no recovery state for that existing crash window. A fail-soft summons result shall not change the denial payload. A pre-settlement action exception that is not fail-soft shall follow R14.

For `:allow`, the adapter shall call `Escalation.consume` in returned order. Each call shall retain its existing separate transaction. A winning consumption shall remain committed when a later consumption loses or the process exits before scheduling. When each consume wins, the adapter shall invoke the existing wake handler once. R11 replaces that handler's standalone wake-schedule transaction and the later supervision clear with the one schedule-settlement transaction; it does not invoke the handler a second time. When one or more consumes lose, the adapter shall select the first losing id in returned order and run a later denied-settlement transaction with the existing error with exact fields and values:

```json
{
  "code":"rule_denied",
  "rule":"<statuteName for the first losing decision request>",
  "edge":"verb",
  "reason":"rule_denied",
  "script_exit_class":null,
  "ref":"<exact gated assignment or work-item ref>",
  "producer":null,
  "identity_manifest_sha":"<exact active identity manifest SHA or null>",
  "message":"ruling authorization was no longer available"
}
```

`edge` shall equal `turn-end` when the call edge is `turn_end`; otherwise it shall equal `verb`. The transaction shall use that error as a denied settlement and shall create no prod wake.

A denied settlement for any table result whose denial settlement payload is not `none` shall, in one transaction:

1. insert one `events` row with existing exact columns `ts`, `kind = "denied"`, `verb`, `origin`, serialized `principal`, `sessionKey`, and the exact encoded settlement payload;
2. retain the inserted event id;
3. compare-and-clear the matching pending tuple;
4. apply the existing denial-streak behavior;
5. append the `dispatch_denied_before_schedule` observation;
6. leave `prodCount` unchanged.

The observation `failureBasis` shall name the inserted event id and copy its exact `ts`, `kind`, `verb`, `origin`, `principal`, `sessionKey`, and decoded `payload`. The event payload shall have no prodder-only field. The denied event, pending clear, denial-streak update, and final observation shall commit together or roll back together. After commit, replay shall return the final observation through R4 without reevaluating rules or initiating an action. The original deny-plus-escalation invocation shall still perform its one post-commit summons unless the process exits in that existing crash window. After rollback, the pending attempt shall remain available to the existing drain. The generic dispatch edge remains unchanged for non-supervision calls.

R14. An exception from `Rules.decide`, a non-fail-soft R13 pre-settlement action, or the dispatch handler before settlement shall leave the pending tuple intact. It shall not append a terminal observation, change `prodCount`, or create a replacement identifier.

### 3. Pre-schedule no-turn settlement

R15. The current supervision claim edge or drain edge shall evaluate items 1–5 in that edge's database transaction before it calls `Rules.decide`. It shall select the first matching outcome in this precedence order:

1. `assignment_closed_before_schedule`;
2. `holder_retired_before_schedule`;
3. `work_blocked_before_schedule`;
4. `self_terminus_before_schedule`;
5. `lineage_exhausted_before_schedule`;
6. `dispatch_denied_before_schedule`.

When none of items 1–5 matches, the adapter shall enter R13. An R13 denial shall settle item 6 in the R13 denial transaction. That transaction shall not reevaluate items 1–5. This boundary preserves the exact rule-result actions in R13 while keeping each observation settlement atomic.

For item 3, the edge shall read the latest matching `work-blocked` or `work-unblocked` row in the transaction snapshot. A latest `work-blocked` row matches item 3. No row or a latest `work-unblocked` row does not match item 3, so the edge shall continue to item 4. The edge shall not select or cite a lower-priority predicate after one matches. The settlement transaction shall compare-and-clear the matching pending tuple, leave `prodCount` unchanged, and append the cause observation. Its selected target, delivered target, and terminal values shall use the selected outcome reason.

R16. The observation basis for each pre-schedule result shall cite these raw facts:

| Outcome | Required raw fact source |
| --- | --- |
| `assignment_closed_before_schedule` | `assignments` row fields that prove the assignment no longer admits a prod |
| `holder_retired_before_schedule` | holder `sessions` row state |
| `work_blocked_before_schedule` | exact latest matching `condition_facts` `work-blocked` assertion row plus assignment identity |
| `lineage_exhausted_before_schedule` | exact `sessions` lineage rows and exact stable-key no-row lookup read by the existing target walk |
| `self_terminus_before_schedule` | pending branch fields plus holder and target session keys used by the existing terminus check |
| `dispatch_denied_before_schedule` | exact persisted denied `events` row and its rule, edge, reason, origin, and principal payload fields |

Each pre-schedule `failureBasis` shall also cite the immutable attempt carrier. The implementation shall not replace a missing required row with a fabricated unknown fact. It shall refuse the settlement and surface the dirt.

### 4. Fire, delivery, and no-turn fire outcomes

R17. A successful wake delivery shall retain the existing atomic wake delivery transaction: append the prompt, create one turn joined by `wakeId`, and mark the wake fired. The observation shall derive `deliveredTarget` from that turn row, not from the wake row.

R18. At fire time, one transaction shall:

1. read the latest `work-blocked` or `work-unblocked` `condition_facts` row for the holder in that transaction's snapshot;
2. continue normal fire with no suppression when no row exists or the latest row is `work-unblocked`;
3. when the latest row is `work-blocked`, compare-and-transition the wake from pending to canceled;
4. parse the frozen counter epoch from the validated deterministic wake identifier;
5. read the exact current `assignment_prods.attestCount` and `prodCount` row;
6. decrement `prodCount` only when the wake transition wins, the current epoch equals the frozen epoch, and `prodCount` is positive;
7. apply no decrement when the wake transition wins and the current epoch is greater than the frozen epoch, because the existing progress-reset transaction already removed that schedule contribution;
8. append the `work_blocked_at_fire` observation;
9. cite the exact deciding `work-blocked` row fields `id`, `ts`, `kind`, `scope`, and `origin`, the canceled wake row, and the pre-mutation `assignment_prods` epoch and count fields.

The deciding standing-value read, wake transition, refund, and observation shall use the same transaction and snapshot. A retraction committed before that transaction reads shall prevent suppression. A retraction committed after the transaction reads shall serialize after the completed suppression and shall not change its cited fact.

A current epoch lower than the frozen epoch, a same-epoch zero count, a missing counter row, or a malformed epoch-bearing wake identifier is dirt. The transaction shall roll back and report `prodder_refund_epoch_conflict`; it shall not clamp, decrement, or invent an epoch. A replay that sees the canceled wake and its observation shall follow R4 and shall not reread mutable refund inputs or decrement again. A canceled wake without its observation is dirt because R18 commits both in one transaction.

R19. When delivery re-resolution finds no target, one transaction shall mark the supervision wake fired and append the `target_unavailable_at_fire` observation. It shall create no turn and shall not refund `prodCount`. `failureBasis` shall cite the selected wake row, the exact session or lineage rows, and the exact stable-key no-row lookup read by re-resolution.

R20. A delivery exception before the R17 or R19 transaction commits shall leave the wake pending. It shall not append a terminal observation or change `prodCount`. The existing wake scheduler shall replay it.

### 5. Terminal-turn observation and fault recognition

R21. The existing terminal publication hook shall pass each terminal turn to the existing `Bubble.recognize_terminal` edge. That edge shall recognize a prodder-created turn from its deterministic `w_pd_` wake join and exact `prodder_attempt_v1` carrier. It shall not infer provenance from time adjacency or reconstruct cleared pending fields.

R22. For a prodder turn with `status = delivered`, the recognition transaction shall append the observation with `faultRecognition = {"kind":"not_admitted","terminalStatus":"delivered"}`.

R23. For a prodder cause turn with `status = canceled`, the recognition transaction shall append the observation with `faultRecognition = {"kind":"not_admitted","terminalStatus":"canceled"}`. This preserves the current rule that a canceled cause turn does not start a bubble.

R24. For a prodder terminal admitted by the current bubble production, recognition shall read the terminal turn, wake, immutable attempt carrier, lineage rows, and exact latest matching `user-alerted` condition fact in one database snapshot. It shall use those rows for both the existing bubble decision and the observation.

R25. A standing `user-alerted` assertion shall produce `faultRecognition.kind = suppressed_user_alerted`. `matchedFact` shall name the exact condition fact row that won the standing-value evaluation. The implementation shall not reconstruct that fact from a timestamp or store a cause-scoped standing value.

R26. An admitted, unsuppressed terminal shall retain the current bubble action. Its observation shall name the original cause turn and one exact existing action from the closed set in Terms.

R27. The durable bubble action and the cause observation shall converge as one idempotent settlement:

- A notice enqueue shall use the existing deterministic `bubble:<causeTurnSeq>:<recipientSessionKey>` wake identity. The enqueue and observation shall commit in one transaction. A replay shall verify the same wake and observation.
- A terminal alert shall append the existing lifecycle marker, owner-stream marker when the stream exists, standing `user-alerted` fact, and cause observation in the current terminal-alert transaction. Wire publication remains post-commit.
- A parentless cause with no action shall append the cause observation in one transaction.

R28. If the process crashes after terminal turn commit but before R22–R27 commit, the current terminal publication sweep and `BubbleSweeper` shall retry recognition. The unique observation index and existing deterministic bubble wake shall make the retry idempotent. If the observation already exists, recognition shall follow R4 instead of reevaluating current `user-alerted` or lineage facts.

R29. `failureBasis` for a terminal turn shall include the immutable `prodder_attempt_v1` carrier row, exact `turns` terminal fields, joined `wakes` fields, and each raw condition or lineage fact that the existing recognition read. It shall follow the R7 total order. The implementation shall not add a `failureClass` field.

### 6. Versioned read surface and compatibility

R30. Add two separately named versioned read commands:

```text
tightbeam work-item-trace-prodder-v1 <work-item-id>
tightbeam assignment-trace-prodder-v1 <assignment-id>
```

R31. `work-item-trace-prodder-v1` shall apply the same owner or admin authorization and `not_found` behavior as the default work-item trace. Its result shall have exact top-level keys `schema`, `workItemId`, and `observations`. `schema` shall equal `prodder-provenance-v1`. `workItemId` shall equal the requested identifier. `observations` shall be an array. Each item shall have exact keys `id`, `ts`, and `detail`. `id` and `ts` shall be integers from the final `lifecycle_events` row. `detail` shall be the full decoded R5 object. The query shall include only observations whose carrier has that work-item id. Items shall sort by `id` ascending.

`assignment-trace-prodder-v1` shall authorize an admin or the `sessions.ownerUserId` reached by joining the requested assignment's `holderKey`. It shall return `not_found` before authorization detail leaks for an unknown or unauthorized assignment. Its result shall have exact top-level keys `schema`, `assignmentId`, `workItemId`, and `observations`. `assignmentId` shall equal the requested id. `workItemId` shall equal the assignment's string id or JSON `null`. `observations` and its item shape shall follow this section. The observation query shall include only the requested assignment. This surface retrieves both bound and unbound assignments without a write.

R32. The default `work-item-trace` command shall not call the new read path. Its output shall retain the exact top-level keys, entry keys, causal-event keys, and types pinned at the source baseline.

### 7. Migration and recovery

R33. `Schema.ensure_all/1` shall ensure the existing tables and pre-v1 indexes before it invokes the R2 seam as its final schema step. The migration shall add only the exact R1 index and code that reads or writes the existing tables. It shall not rebuild `lifecycle_events`, change the closed `causal_events.kind` set, or backfill a carrier or cause observation.

R34. `Tightbeam.Boot.start_link/1` shall remain the second root child after `Tightbeam.DB`. It shall call `Schema.ensure_all/1` before `EventLog.boot/0`, turn recovery, the Supervision server, or the wake scheduler can start. Each packaged `tightbeam-gateway` start and each direct release command that starts the application shall enter this child sequence; neither entry path shall expose a flag or command that skips `ensure_cutover/1`.

When R2 returns `{:error, error}` for a nonempty first-entry query, `Schema.ensure_all/1` shall return that value and `Boot.start_link/1` shall return `{:error, {:prodder_cutover_refused, error}}`. The root application start shall fail before Supervision starts. That refused release entry shall run zero Supervision recovery sweeps. When `ProdderProvenance.ensure_cutover/1` returns `prodder_schema_conflict` while it validates R1, Boot shall fail the same startup before it executes the R2 pending-branch query or starts Supervision.

When R2 returns `:cutover_completed` or `:already_complete`, `Schema.ensure_all/1` shall return `:ok` and Boot shall continue. Each admitted Supervision start shall run exactly one existing recovery sweep, preserving the parent boot/restart contract after cutover.

R35. On a later start with the exact R1 index present, recovery shall skip the R2 pending query and use the existing Supervision sweep to drain an unsettled v1 pending branch. It shall use the existing wake scheduler for a pending v1 wake and the terminal publication sweep plus `BubbleSweeper` for an unobserved v1 terminal turn. No new periodic worker is permitted.

R36. Operators shall be able to replay those existing recovery edges without changing the deterministic identifier. A later replay shall not delete the R1 index or reenter the first-entry R2 query. Replay shall satisfy F6.

## Acceptance

The implementation shall run these fixtures against a real database and the real dispatch, wake, ledger, supervision, bubble, and trace seams at source baseline `19a50e47aa9e7d0a8ff474321102cd890a7dd0c7` plus the implementation. Handwritten direct inserts may establish givens. They shall not replace the exercised mutation seam.

### F1 — Success

Real fixture basis: `test/supervision_test.exs:754-790`, which exercises an atomic supervision fire.

Given an open assignment held by active session H, holder terminal turn T0, a persisted prod branch at tier 1, and no `work-blocked` fact,

When the real supervision drain schedules and the real wake scheduler delivers the attempt, and turn T1 finishes `delivered`,

Then one deterministic `w_pd_…` wake exists, its immutable attempt carrier retains the full tuple after the pending tuple clears, T1 joins that wake, selected and delivered targets both name H, one cause observation joins T1, `prodCount` is 1, and default trace exact-key assertions still pass.

Trace: R3–R12, R17, R21–R22, R28–R32.

### F2 — Every no-turn outcome

Real fixture basis: `test/supervision_test.exs:709-736`, `1006-1064`, `1338-1414`, plus the real target walk and dispatch denial edge.

For this table, `none(X)` means `{"kind":"none","reason":"X"}`. `session(S)` means `{"kind":"session","sessionKey":"S"}`. S is the exact scheduled `wakes.sessionKey`.

For each row below, Given the stated raw fact, When the real settlement edge runs, Then no joined turn exists and the exact typed outcome and targets are observed:

| Raw given | Expected outcome X | Selected target | Delivered target | Counter result |
| --- | --- | --- | --- | --- |
| assignment no longer admits prod before schedule | `assignment_closed_before_schedule` | `none(X)` | `none(X)` | unchanged |
| holder session is retired before schedule | `holder_retired_before_schedule` | `none(X)` | `none(X)` | unchanged |
| exact standing `work-blocked` fact matches before schedule | `work_blocked_before_schedule` | `none(X)` | `none(X)` | unchanged |
| existing lineage walk has no eligible target before schedule | `lineage_exhausted_before_schedule` | `none(X)` | `none(X)` | unchanged |
| existing terminus check selects the holder itself | `self_terminus_before_schedule` | `none(X)` | `none(X)` | unchanged |
| real rule edge persists a dispatch denial | `dispatch_denied_before_schedule` | `none(X)` | `none(X)` | unchanged |
| scheduled wake changes pending to canceled on an exact fire-time `work-blocked` match | `work_blocked_at_fire` | `session(S)` | `none(X)` | same epoch: decremented once; later epoch: unchanged |
| real delivery re-resolution returns no target | `target_unavailable_at_fire` | `session(S)` | `none(X)` | scheduled count retained |

Then the terminal uses the same no-turn outcome, `faultRecognition` is `{"kind":"not_applicable_no_turn"}`, `failureBasis` cites the exact returned rows or no-row lookup read, and a second call returns the equal observation without another counter change.

Given the real retire transaction closes assignment A and retires holder H while `work-blocked` also stands for H, When the real pre-schedule settlement runs, Then it records only `assignment_closed_before_schedule`. Given A remains open while H is retired and `work-blocked` stands, Then it records only `holder_retired_before_schedule`. Given A is open, H is active, `work-blocked` stands, and the target walk would otherwise reach self-terminus or lineage exhaustion, Then it records only `work_blocked_before_schedule`. Given no higher predicate matches and the real claim-time terminus check selects holder H, When the claim transaction runs, Then it commits only `self_terminus_before_schedule` with its carrier and does not invoke rules. Given no higher predicate matches and the real claim-time target walk returns no eligible target, When the claim transaction runs, Then it commits only `lineage_exhausted_before_schedule` with its carrier and does not invoke rules. Given a persisted `escalation` branch had an eligible target at claim time but its real drain-time target walk returns no eligible target, When the real pre-schedule settlement runs, Then it records only `lineage_exhausted_before_schedule` and does not invoke rules. Given no higher predicate matches, the real target walk returns an eligible target, and the real rules edge denies dispatch, When the real denial settlement runs, Then it records `dispatch_denied_before_schedule`. Each overlap fixture shall prove that the first matching predicate is the sole outcome and that its `failureBasis` does not cite a lower predicate.

When a lineage-exhausted or target-unavailable outcome depends on no active row for computed session key M, Then `failureBasis` shall contain `{"source":"sessions","key":{"sessionKey":"M","state":"active"},"fields":null}` from that settlement snapshot.

Trace: R13–R20, R29, I3–I8.

### F3 — All terminal-turn statuses, including failed before start

Real fixture basis: `lib/tightbeam/ledger.ex` queued-to-failed unclaimable path and terminal publication path; the fixture shall retire or invalidate the delivered session after queue creation and before claim.

For each row below, Given the real wake delivery transaction created queued turn T1, When the stated real ledger seam terminalizes T1 and the existing terminal recognition edge runs, Then the exact result is observed:

| Real terminal seam | Stored status | Required recognition and action |
| --- | --- | --- |
| normal delivery completion | `delivered` | `not_admitted` with terminalStatus `delivered`; zero bubble actions |
| real retire drain cancels the created prodder turn | `canceled` | `not_admitted` with terminalStatus `canceled`; zero bubble actions |
| session becomes unclaimable before claim while exact `user-alerted` assertion F stands | `failed` with `startedAt: null` | `suppressed_user_alerted` naming F; zero bubble actions; exact stored error; no inferred class |
| boot recovery terminalizes a running turn whose outcome is unknown, no `user-alerted` assertion stands, and active parent P is the nearest ancestor | `failed_unknown` | `admitted` with one exact `notice_enqueued` action naming P and `bubble:<T1.seq>:<P>` |

The `failed_unknown` fixture shall create the turn through the real wake edge, claim it through the real ledger edge, simulate process loss, and run the real boot-recovery and terminal-publication seams. The canceled fixture shall create the turn through the real wake edge and cancel it through the real retire drain. The failed fixture's `matchedFact` shall be the exact F row used in that recognition snapshot.

Trace: R21, R24–R29, I6.

### F4 — Selected target differs from delivered target

Real fixture basis: `test/supervision_test.exs:1269-1305`, which retires a target during delivery re-resolution.

Given selection writes session S into the wake,

When S retires before delivery and the real delivery edge re-resolves to active ancestor P,

Then `selectedTarget.sessionKey` is S, `deliveredTarget.sessionKey` is P, the joined turn belongs to P, and no field says the wake delivered to S.

Trace: R10, R17, I3.

### F5 — Crash windows

Real fixture basis: transaction boundaries in `lib/tightbeam/supervision.ex:641-945`, `lib/tightbeam/wakes.ex:453-546`, `lib/tightbeam/gateway.ex:972-1079`, and `lib/tightbeam/productions/bubble.ex:121-244`.

For each settlement transaction boundary below, Given a fault injection forces rollback immediately before commit and process loss immediately after commit, When the existing recovery edge replays, Then the settlement-owned database state equals one uninterrupted settlement. The R13 rule-action windows use their separate outcome-specific assertions below:

1. pending claim, including a claim-time self-terminus or lineage-exhausted settlement;
2. prod-branch schedule, pending clear, counter increment, exact `prod_fired {tier}` settlement, and its deterministic schedule-basis carrier;
3. each R13 denied or scheduled settlement;
4. fire-time cancel, refund, and no-turn observation;
5. target-unavailable fire and observation;
6. prompt append, turn creation, and wake-fired transition;
7. terminal turn recognition, cause observation, and the outcome-appropriate existing bubble settlement.

The schedule fixture shall also settle an escalation branch and prove it increments the existing counter but appends no `prod_fired` causal event.

The crash set shall also run both serial orders between a progress reset and fire-time suppression. If suppression commits first, it shall decrement the old epoch once before the reset zeroes that epoch. If reset commits first, it shall append its exact `prod_answered` causal events, advance `assignment_prods.attestCount`, and zero `prodCount`; suppression shall then cancel and observe the older wake without decrementing the new epoch. Both orders shall end with the same current counter value. Each observation shall preserve the exact order that occurred through its frozen and current epoch facts.

The crash set shall prove carrier preservation by crashing after the R8 claim commit and after the R11 pending clear. Replay shall recover the same attempt object from `prodder_attempt_v1` and the same prod event reference from `prodder_schedule_basis_v1`. It shall not read a cleared or overwritten watermark.

The R13 set shall exercise these real result and action boundaries:

| Real `Rules.decide` result | Given / When | Required observable result |
| --- | --- | --- |
| bare deny | Given `{:deny, error}`, When the adapter settles it | it returns `{:error, error}`; no remedy or request action occurs; one denied event has exact `error`; one no-turn observation cites that event |
| remedy | Given `{:remedy, statute, ref, error}`, When the real `RailRemedy.fire` returns outcome O | the existing remedy episode and producer behavior occurs; the adapter returns `{:error, amended_error}`; the denied payload and `amended_error` have `reason = remedy_fired` and `producer = O.producer_id`; one no-turn observation cites that event |
| escalation | Given `{:escalate, statute, ctx, nil}`, When the real `Escalation.escalate` runs before denial settlement and returns `{:decision_pending, DR}` | one open request and its existing notification outbox exist; the adapter returns `{:decision_pending, DR}`; the denied payload equals `ctx.error`; one no-turn observation cites that event |
| attached escalation | Given `{:escalate, statute, ctx, DR}`, When the adapter settles denial | it returns `{:decision_pending, DR}` without calling `Escalation.escalate`, and creates no second request or notification; the denied payload equals `ctx.error` |
| deny plus escalation | Given `{:deny_escalate, statute, ctx}`, When denial commits before the real fail-soft summon | the no-turn observation and exact denied payload commit first; the original invocation then produces the existing episode/request action or its existing failure record and returns `{:error, ctx.error}` |
| allow, consumes win | Given `:allow` and each ruling CAS wins, When each existing separate consume transaction and the one R11-backed wake-handler invocation run | each ruling is consumed; the handler runs once; R11 schedules exactly one prod wake; the adapter returns the exact handler result; no denied event or no-turn observation exists |
| allow, one or more consumes lose | Given `:allow` and ruling L is the first losing id in returned order, When all existing separate consume transactions run | each winning CAS remains consumed; no prod wake exists; one later denied-settlement transaction writes the exact R13 `lost_error` for L and one no-turn observation citing that event; the adapter returns `{:error, lost_error}` |

For remedy and unattached escalation, the test shall inject process loss before the existing pre-settlement action, after that action returns but before settlement, before denial-settlement commit, and after commit. Before settlement, the pending tuple shall remain. Replay shall re-enter the applicable existing action seam and retain its documented CAS, dedupe, rewake, or recovery result. For bare deny and attached escalation, which have no result-specific action, the test shall inject before denial commit and after commit. Rollback before denial commit shall leave no denied event, pending clear, denial-streak update, or final observation. Process loss after denial commit shall replay through the final observation without another rules decision or action.

For deny plus escalation, the test shall inject process loss before denial commit, after denial commit but before `RailEpisodes.summon`, and after the fail-soft summons returns. Loss before commit shall leave the pending tuple and no final observation. Loss after commit but before summons shall leave the exact denied event and observation, no summons from that invocation, and no replayed summons. Loss after summons shall retain its existing episode/request action or failure record. Each committed denied event in this set shall retain the baseline payload with no prodder-only field.

For `:allow`, the test shall inject process loss after each separate `Escalation.consume` transaction and before the later schedule or denial settlement. Each winning consumption shall remain committed. The pending tuple shall remain until one later settlement commits. Replay shall reenter `Rules.decide` against those existing committed ruling states; this contract shall not roll them back as a batch or add a recovery row.

For both `to_close` entry kinds, the fixture shall return one real entry from `Rules.decide`, invoke the matching `RailRemedy.close` or `RailEpisodes.recovered` seam before result-specific action, and prove that a later exception leaves the pending attempt replayable. For a non-allow result, the fixture shall prove that `to_consume` remains unused.

The fire-time set shall serialize `work-unblocked` immediately before and immediately after the R18 snapshot read. A retraction committed before the read shall prevent cancellation, refund, and no-turn observation; the existing normal fire shall proceed. A retraction serialized after the read shall leave one canceled wake, one refund when same-epoch, and one observation citing the exact preceding `work-blocked` assertion rather than the later retraction.

The equality check shall compare the exact wake rows, turn rows, pending tuple, `prodCount`, cause observation, bubble wake or terminal alert facts, and lifecycle rows that the contract names.

Trace: R8–R29, I7–I8.

### F6 — Replay

Real fixture basis: `test/gateway_test.exs:1415-1431`, `test/gateway_test.exs:4909-4922`, and existing wake-id and turn-wake-id unique constraints.

Given one attempt has settled for each of the four terminal statuses and each of the eight no-turn outcomes,

When the test replays the real drain, wake fire, terminal publication, and bubble recognition edges in that order twice,

Then each attempt has one cause observation. A scheduled attempt has one prod wake and at most one joined turn. Its schedule contributes once in its counter epoch. A same-epoch `work_blocked_at_fire` outcome refunds once. A later-epoch `work_blocked_at_fire` outcome refunds zero times. Every other outcome refunds zero times.

Bubble action cardinality shall match the observed outcome. This table counts only R27 bubble actions. It does not count an R13 rule effect:

| Observed outcome | Required bubble-action cardinality |
| --- | --- |
| admitted failure with `notice_enqueued` | one deterministic bubble wake |
| admitted failure with `terminal_alert_committed` | one terminal-alert settlement |
| admitted failure with `none_parentless` | zero durable action rows and one typed `none_parentless` result |
| `suppressed_user_alerted` | zero actions for this attempt |
| `not_admitted` delivered or canceled | zero actions for this attempt |
| any no-turn outcome | zero actions for this attempt |

A mismatched attempt carrier, schedule-basis carrier, or outcome payload under the same attempt identifier returns `prodder_observation_conflict` and changes none of those rows. For each attempt, the fixture shall prove carrier `detail` and final `detail.attempt` have the same exact key set and canonical bytes. The fixture shall prove the attempt carrier has no `schema` or `wakeId` key. For a settled prod schedule, it shall prove one schedule-basis carrier points to the exact committed `prod_fired` row. For an escalation after three prod tiers, it shall prove `triggerBasis` contains the exact three causal rows and exact three terminal turns, including each complete stored error envelope. The fixture shall present the same facts in different input enumeration orders and prove that the R7 ordered `triggerBasis` and `failureBasis` bytes and replay equality are identical. Rollback before the prod schedule commit shall leave neither causal event nor schedule-basis carrier. Process loss after commit shall replay to the equal rows without a duplicate. Concurrent equal claims shall return equal carrier bytes; one unequal causal-event or turn reference shall fail without mutation.

Trace: R3–R4, R9–R11, R18–R20, R27–R28, I2, I5, I7–I8.

### F7 — Compatibility

Real fixture basis: exact key assertions in `test/job_trace_test.exs:307-339` and the existing prompt text assertions in supervision tests.

Given the source-baseline compatibility suite and a work item with new cause observations,

When the test calls the default `work-item-trace` and compares existing supervision prompts and wake delivery payloads,

Then each existing exact-key and exact-value assertion passes unchanged. When the test separately calls `work-item-trace-prodder-v1`, it receives only the R31 shape, sorted by observation id.

Given one work-item-bound assignment and one unbound assignment each has a v1 attempt, When the test calls the work-item surface and each assignment surface, Then the bound observation appears on both relevant surfaces, the unbound observation appears only on its assignment surface with `workItemId: null`, each response has only the exact R31 top-level keys, and neither read causes a write.

For each application-start entry in this closed set—packaged `tightbeam-gateway start` and direct `release/bin/tightbeam_gateway start`—Given a database copy with no R1 index and one non-null legacy pending branch, and the old evaluator and scheduler are stopped, When the entry starts v1, Then `Boot.start_link/1` calls `Schema.ensure_all/1`, which calls `ProdderProvenance.ensure_cutover/1` and executes the exact R2 query once. The seam returns `prodder_upgrade_not_quiescent` with the row's six exact ordered values. It creates no R1 index, carrier, or outcome. The application starts no Supervision server or wake scheduler and runs zero recovery sweeps.

Given that refusal, When the operator restarts the old binary, runs its existing pending drain until the exact R2 query is empty, stops the old evaluator and scheduler, and retries either application-start entry, Then the same cutover transaction creates and verifies the exact R1 index and returns `:cutover_completed`. Boot continues, the admitted Supervision start runs exactly one existing recovery sweep, and the cutover creates no carrier or outcome for the pre-v1 attempt.

Given the R1 index is absent and the exact R2 query is empty, When the fixture injects process loss immediately before or immediately after the index transaction commits, Then loss before commit leaves no index and the next application start executes the exact R2 query once. Loss after commit leaves the exact index and the next application start executes that query zero times and runs exactly one existing Supervision recovery sweep. Neither path creates a cutover-completion row.

Given a pre-v1 supervision wake or turn and a v1 observation coexist after the gate, When either versioned surface reads, Then it returns only the v1 observation. The response contains no historical-absence key or synthetic absence item.

Given `sqlite_schema` contains the exact R1 index and a valid v1 carrier retains its pending tuple after a process loss before settlement, When either application-start entry restarts v1, Then `ProdderProvenance.ensure_cutover/1` returns `:already_complete`, the query spy records zero executions of the R2 pending-branch query, Boot continues, and Supervision runs exactly one existing recovery sweep. The existing drain settles or replays the same deterministic attempt identifier without a schema conflict, a second counter effect, or a second observation.

Given `sqlite_schema` contains the exact R1 index, When startup verifies schema, Then startup skips the R2 pending-branch query and admits the writer regardless of a valid v1 pending tuple. Given the index is absent and the exact R2 query is empty, When startup runs the cutover seam, Then the seam creates and verifies the exact index before it admits the writer. Given instead a same-name non-unique index, an index over different columns, a different predicate, or duplicate named rows before index creation, When startup verifies schema, Then it reports `prodder_schema_conflict` with the exact mismatch, executes no R2 pending-branch query, starts no Supervision server, and runs zero recovery sweeps.

Trace: R1–R3, R30–R36, I1, I9–I10.

### Requirement-to-fixture map

| Requirement | Fixtures |
| --- | --- |
| R1–R7 | F1, F2, F3, F6, F7 |
| R8–R14 | F1, F2, F5, F6 |
| R15–R20 | F2, F4, F5, F6 |
| R21–R29 | F1, F3, F5, F6 |
| R30–R32 | F1, F7 |
| R33–R36 | F5, F6, F7 |

## Open Questions

None.

Owner rulings `att_260adeca` and bounded successor ruling `att_01f72a7e` close B1–B5 and the F2b carrier/source seam. A proposed change beyond the exact schedule-basis carrier, escalation `triggerBasis`, admitted `causal_events` source, or to another typed set, transaction boundary, counter equation, observation schema, versioned surface, or existing policy requires a new spec amendment before implementation.
