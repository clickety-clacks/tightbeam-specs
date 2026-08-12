# Patrol response acknowledgment

Status: cold-digested amended spec; artifact `art_023f8032` is historical
superseded evidence and no longer implementation authority; pending replacement
artifact, superseding spec approval, and one fresh linked independent review;
not cleared for implementation

Authority:

- Work item `wi_3e0c3cf7-96a2-4cde-9ed9-9d3ba0074d4b`.
- Owner ruling `att_985e3746-621d-40e3-85eb-aaa406fd782e`.
- Live-loop correction `att_07e7d25e-2239-4f33-9bb6-d30408f6124a`.
- Post-loop direction `att_a4b9964b-3ea3-4906-8986-56e13bce7291`.
- Owner lifecycle evidence `att_b4ec83e1-2fa1-47da-b891-244945aa3279`.
- Owner stale-escalation evidence `att_83bc1c99-6de5-469e-9d23-dbb4cc59f96d`
  and specimen `att_ed7280bb`.
- Supervisor timeline reconciliation
  `att_01b3212c-2773-4e5c-b044-c010d5efb6e6`.
- Owner work-blocked evidence `att_ddbbf084-ad7c-499e-91c6-0bc5fda4ae94`,
  `att_4346df01-2328-4d11-981c-186dd728d13f`,
  `att_111113e4-ef97-49df-93f0-db15bf6c1290`, and
  `att_ca24fb5c-cd50-425d-8ea3-db95d6b8625e`.
- Recon report `art_d0634d61`, SHA-256
  `2c49e74eb77c7706b14801f77e6a556d47d53a20ab1815922683774f3a080a29`.
- Source baseline `ac8651dcb104f312da1c67e0cb7b1abebc640b2b`.

This spec is a bounded amendment to `production-machine-v1.md`,
`supervision-v1.md`, `supervision-impl-v1.md`, and the effort-without-effect
check-in contract. Requirements R1-R24 retain the exact-answer-terminal change.
Requirements R25-R46 add act-time lifecycle admission for patrol outputs and
current `work-blocked` recognition for both supervision and effort check-ins.
Existing rail precedence, liveness receipts, prod timing, branch selection,
and escalation policy remain authoritative except at those stated boundaries.

## Goal

End the self-perpetuating supervision loop in which a process prod creates an
answer turn, that answer turn ends, and its terminal creates the next prod.

The substrate shall record one typed `patrol_response_acknowledgment` for the
exact supervision episode that the delivered answer turn closes. The record
shall bind the assignment, originating wake, recovery branch and rung, source
terminal, and answer terminal. Supervision shall consume only that answer
terminal as an acknowledgment of that episode.

Before a process-owned patrol output acts, the substrate shall revalidate its
typed causal source, source assignment, current holder, and destination session
against current durable state. The same validation shall bracket prompt
delivery and queued-turn admission. A terminal assignment transition or holder
retirement shall stop every not-yet-admitted output from that lane. The stopped
output shall not move to a successor assignment or session.

While a current `work-blocked` fact stands for an open assignment holder,
supervision and effort check-in monitoring shall produce no holder-facing prod
or stalled-work escalation. The substrate shall retain the obligation and the
blocking fact without asking the holder to complete or surrender and without
asserting another block.

Subtraction ruling: ADD wins because the owner requires patrol to remain while
one exact answer terminal closes its episode. DELETE would remove required
absence detection. ACCEPT would retain the observed infinite response loop.

Lifecycle-admission ruling: ADD one typed source seam and two act-time checks.
DELETE loses because patrol and effort observation remain required. ACCEPT
loses because a closed or blocked lane would continue to wake people. Prompt
inference loses because it cannot prove causality or successor isolation.

## Non-Goals

1. This spec does not make progress prose, an attest count, a verdict, an
   artifact, a tool call, or message content into a patrol acknowledgment.
2. This spec does not change the closed liveness-receipt source set.
3. This spec does not change prod limits, delays, prompts, counters, branch
   selection, escalation recipients, recovery lineage, or terminal policy.
4. This spec does not suppress an ordinary turn, a later terminal, a turn from
   another wake, or a turn from a user or agent message.
5. This spec does not acknowledge `canceled`, `failed`, or `failed_unknown`
   answer terminals.
6. This spec does not override completion, surrender, revoke, a rail action, a
   typed liveness receipt, or a standing blocking fact.
7. This spec does not backfill historical supervision wakes. A wake without the
   new episode row remains ineligible for acknowledgment.
8. This spec does not add a worker, sweeper, timer, queue, retry policy, public
   command, or user-visible message.
9. This spec does not reinterpret or delete an existing wake, turn, attest,
   receipt, lifecycle event, entitlement, sidecar, or watermark.
10. This spec does not implement the design, probe a live work row, or dispose
    the work item.
11. This spec teaches no new agent operating pattern. It requires no manual
    guidance amendment.
12. This spec does not reclassify, delete, or repair historical turns 19082,
    19084, or 19086. Their timestamps prove delivery before the later revoke;
    they do not by themselves prove every other admission predicate.
13. This spec does not transfer a patrol count, entitlement, generation,
    acknowledgment, wake, decision request, or observation from a predecessor
    assignment to a successor assignment.
14. This spec does not suppress user wakes, agent wakes, ordinary work turns,
    tool effects, or decision notifications unrelated to supervision or effort
    check-in monitoring.
15. This spec does not make `work-blocked` a substrate judgment. Only the
    existing authorized condition-fact seam can assert or retract that fact.
16. This spec does not add a retry worker, lifecycle sweeper, polling loop, or
    timeout that decides whether an assignment, session, or block is current.
17. This spec does not mutate the historical review assignments
    `asg_0cf8e6ec-4530-4ef9-b2aa-8579800bbe34` or
    `asg_99e999f9-847e-4d72-9f7a-1295067d7bac`.

## Terms

### Terminal identifier

A **terminal identifier** is the positive integer `turns.seq` of a turn whose
status is `delivered`, `canceled`, `failed`, or `failed_unknown`. This spec uses
`sourceTerminalId` and `answerTerminalId` for those integers. A timestamp is not
a terminal identifier.

### Recovery branch and rung

The **recovery branch** is the exact `pendingBranch` frozen by the supervision
claim that produced a wake. Its closed set for this spec is `prod` and
`escalation`. `terminus` creates no wake and cannot be acknowledged.

The **recovery rung** is the positive `pendingK` frozen by that claim. For a
`prod` branch it is the prod tier. For an `escalation` branch it is the lineage
rung and shall equal `wakes.reresolveRung`.

### Patrol response episode

A **patrol response episode** is the durable source tuple:

```text
(assignmentId, originatingWakeId, recoveryBranch, recoveryRung, sourceTerminalId)
```

The scheduling transaction freezes this tuple before the mutable pending
watermark can clear or change. The tuple is the acknowledgment key. No field is
derived from prompt text, timestamp adjacency, the current counter, or a later
watermark.

### Answer turn

The **answer turn** is the unique `turns` row created by delivery of
`originatingWakeId` or one coherent retry descendant whose patrol output source
has `rootWakeId = originatingWakeId`. It shall have the episode assignment id.
A direct prod answer runs on the assignment holder. An escalation answer can
run on the selected lineage target. Every earlier wake in the answer wake's
chain is canceled with the next wake as its exact replacement, so one chain can
create at most one answer turn.

### Patrol response acknowledgment

A **patrol response acknowledgment** is an episode row whose
`answerTerminalId` names the delivered terminal of its answer turn. Its typed
value is:

```json
{
  "schema": "patrol-response-acknowledgment-v1",
  "assignmentId": "asg_exact",
  "originatingWakeId": "w_exact",
  "recoveryBranch": "prod",
  "recoveryRung": 1,
  "sourceTerminalId": 101,
  "answerTerminalId": 102,
  "scheduledAt": 1700000000000,
  "acknowledgedAt": 1700000000100,
  "scheduledCause": "patrol_wake_scheduled",
  "scheduledPrincipal": "process:tightbeam",
  "acknowledgmentCause": "patrol_answer_terminal",
  "acknowledgmentPrincipal": "process:tightbeam"
}
```

The row retains the source tuple after acknowledgment. It never changes its
source tuple or answer terminal.

### Exact acknowledgment match

An **exact acknowledgment match** exists for evaluation terminal T only when
one acknowledged episode joins all of these durable facts:

1. `answerTerminalId = T`;
2. the answer turn joins `assignmentId` and one coherent
   `patrol_output_sources` row whose source kind is `supervision_episode`,
   source ref and root wake both equal `originatingWakeId`, and retry chain is
   unbroken;
3. the answer turn status is `delivered`;
4. the answer wake is a fired `process:tightbeam` prompt for that assignment;
5. the scheduled supervision sidecar names the same assignment and branch and
   has a settled controller;
6. the source terminal exists and belongs to the assignment holder session;
7. the source assignment is still open;
8. branch `prod` has a null lineage re-resolution tuple;
9. branch `escalation` has `reresolve = lineage`, a holder seed, and
   `reresolveRung = recoveryRung`.

Missing or unequal data is not a partial match.

### Acknowledgment fail closed

**Acknowledgment fail closed** means the candidate creates no acknowledgment
match and the terminal continues through the existing rail, receipt,
lifecycle, and prod behavior. It does not mean that the terminal, wake,
assignment, or evidence is discarded.

### Suppression target

The **suppression target** is only the prod-ladder eligibility of the exact
answer terminal. Suppression does not hide, undo, consume, or replace a message,
tool call, tool result, attest, artifact, verdict, completion, failure, or other
durable effect produced before that terminal.

### Patrol output

A **patrol output** is one process-owned action in this closed set:

1. delivery of a supervision `prod` or `escalation` prompt wake;
2. admission of the prompt turn queued by that delivery;
3. execution of an `effort_probe` or `effort_deadline` internal wake;
4. delivery of an effort check-in holder prod; or
5. delivery of an effort decision-request notification.

An ordinary process notice, user wake, agent wake, condition wake, tool effect,
or unrelated decision notification is not a patrol output.

### Patrol output source

A **patrol output source** is the immutable typed row that connects one patrol
wake to the durable state that authorized it. Its closed source kinds are:

| Source kind | Exact source |
| --- | --- |
| `supervision_episode` | one patrol response episode, identified by its originating wake id |
| `effort_generation_probe` | one `(assignmentId, generation)` whose `wakeId` is the internal probe |
| `effort_generation_prod` | one `(assignmentId, generation)` that produced one holder prod |
| `effort_decision_notification` | one `(decisionRequestId, lineageRung)` notification |
| `effort_decision_deadline` | one open decision request whose `deadlineWakeId` is the internal deadline |

Prompt text, assignment proximity, timestamps, target role, origin alone, and a
later assignment on the same work item are not causal sources.

### Patrol retry and replay

A **patrol retry** is an explicit replacement wake for the same patrol output
source after a typed delivery or destination-retirement result authorizes the
existing replacement policy. It names one root wake, one exact predecessor
wake, and a positive retry ordinal. A **patrol replay** repeats scheduling,
delivery, admission, or cancellation for an existing wake id. A replay creates
no replacement row and does not increase the retry ordinal.

An **unbroken retry chain** starts at ordinal zero. Each later source has the
same assignment, holder, source kind, source ref, source version, and root wake;
names the immediately preceding wake; increments the ordinal by one; and joins
a typed cancellation of that predecessor whose replacement is the later wake.
Only the last wake can remain pending. A missing ordinal, fork, unequal copied
field, or predecessor without that cancellation breaks the chain.

### Admission fail closed

**Admission fail closed** means a patrol output does not act when its typed
source or current-state predicate is false. Before a turn exists, the
transaction refuses or cancels the exact wake with no replacement. For a
queued turn, the transaction terminalizes that turn without harness execution.
It does not run normal prod behavior, select another assignment, or discard
the source evidence.

### Delivery admission and turn admission

**Delivery admission** is the transaction that either lets one due patrol wake
enqueue or execute its output, or cancels that wake. Source validation and the
chosen action are one indivisible step.

**Turn admission** is the transaction that either changes one queued patrol
turn to `running`, or terminalizes it without harness execution. Source and
lifecycle validation and the chosen action are one indivisible step. Delivery
admission does not authorize later turn admission.

### Current lane

The **current lane** of a patrol output is the exact source `assignmentId` and
the `holderKey` frozen in its patrol output source. It is current only while the
assignment row is `open`, its current `holderKey` equals the frozen holder, and
that holder session is `active`. A different assignment is a successor lane
even when it has the same work item, holder, subject, or owner.

### Lifecycle tombstone

A **lifecycle tombstone** is the first committed durable fact that makes a
patrol output's current lane false: assignment outcome `completed`,
`surrendered`, or `revoked`, or retirement of its frozen holder. The assignment
transition, closing attest or interruption, session transition, wake
cancellation, and queued-turn terminal remain separate truthful rows joined by
the exact assignment and wake ids. A lifecycle tombstone does not rewrite an
already admitted or terminal turn.

### Current work-blocked fact

A **current work-blocked fact** is the latest authorized `condition_facts` row
for kind `work-blocked` and the frozen holder session, when no later
`work-unblocked` row exists for that scope. Its row id is the exact recognition
source. A block on another session or a superseded block is not current.

## Assumptions

1. The source baseline writes one terminal transition through
   `Tightbeam.Ledger.finish_in_txn/4` and publishes committed terminals after
   commit.
2. Wake delivery creates at most one turn for one wake id. `wakes.wakeId` and
   the turn-to-wake join provide the durable answer identity.
3. The supervision claim freezes `pendingBranch`, `pendingAssignment`,
   `pendingK`, `pendingN`, and `lastEvaluatedTerminal` before it schedules a
   wake.
4. Each supervision wake has a `supervision_liveness_sidecar` row. Its
   `wakeKind` distinguishes `prod` from `escalation`.
5. A scheduled patrol wake has a positive source terminal id. The current
   no-terminal path does not schedule a patrol wake.
6. Completion and surrender close the assignment in their attest transaction.
   Revoke closes it in its revoke transaction. Each transition removes the
   supervision entitlement through the existing disposition seam.
7. Rail enforcement precedes the prod ladder. Typed liveness-receipt absorption
   runs before a new entitlement claim.
8. The schema owner can add and verify the additive tables in R1 and R25 before
   supervision, effort check-in, and wake scheduling start.
9. Completion, surrender, revoke, and holder retirement already have one
   transactional disposition seam for supervision and effort check-in state.
10. A queued prompt turn retains its exact `wakeId`, `assignmentId`, and
    destination `sessionKey` through turn admission.
11. An effort check-in generation and decision request already identify their
    internal probe or deadline wake. R25 supplies the missing typed carrier for
    holder prods, decision notifications, and explicit retries.
12. Condition-fact filing can invoke one in-transaction recognition seam after
    the authorized fact row exists and before that filing commits.

If an assumption is false, the implementer shall stop the affected scope and
amend this spec before changing behavior.

## Invariants

### I1 — Exact episode identity

One source tuple identifies at most one episode. One wake id identifies at most
one episode. A replay with equal bytes returns the existing episode. A replay
with unequal bytes reports `patrol_response_episode_conflict` and rolls back the
proposed schedule.

### I2 — One answer terminal

One episode records at most one answer terminal. One answer terminal belongs to
at most one episode. The transition from no answer terminal to one answer
terminal is one-way.

### I3 — Terminal and acknowledgment commit together

For a successful answer turn, the delivered terminal transition and the
acknowledgment transition commit in one transaction. A crash exposes both or
neither. A malformed or mismatched episode does not roll back a truthful
terminal; it leaves the terminal unacknowledged and eligible for normal
behavior.

### I4 — Suppression is terminal-exact

An acknowledgment can suppress only evaluation of its
`answerTerminalId`. It cannot suppress its source terminal, an older terminal,
a newer terminal, or a terminal from another retry chain.

### I5 — Effects outrank acknowledgment

The existing rail step runs before acknowledgment handling. The existing typed
liveness-receipt absorption runs before acknowledgment handling. If either acts,
its existing result wins. The acknowledgment row remains audit evidence and
does not erase or replace the effect.

### I6 — Lifecycle remains authoritative

An episode can become acknowledged and can suppress only while its source
assignment is open. Completion, surrender, or revoke prevents a new
acknowledgment and invalidates a prior acknowledgment for later evaluation.

### I7 — Failures remain visible

A `canceled`, `failed`, or `failed_unknown` answer turn receives no
acknowledgment. Its terminal follows the existing failure and supervision
paths.

### I8 — No content inference

The substrate recognizes an answer from the wake-to-turn join and typed episode
row. It does not parse the agent reply, attest note, prompt, tool output, error
text, elapsed time, or message adjacency.

### I9 — Existing evidence remains complete

Acknowledgment handling appends no substitute for an existing fact and deletes
no fact. The episode row retains the exact source tuple, answer terminal,
timestamps, scheduled cause and principal, and acknowledgment cause and
principal. Existing trace rows remain queryable in their original order.

### I10 — No future entitlement is consumed

Acknowledgment handling advances only the session terminal watermark to the
exact answer terminal. It does not advance the entitlement generation, change a
due time, reset or increment a counter, clear a different pending branch, or
create or cancel a wake.

### I11 — One mutation seam per state

The supervision wake-scheduling transaction is the only episode creator. The
ledger terminal transaction is the only acknowledgment writer. The ordered
prod-ladder transaction is the only acknowledgment consumer.

### I12 — Act-time state wins

A schedule-time match is not authority to act later. Every patrol delivery and
queued-turn admission re-reads its destination session, exact assignment,
current holder, typed source, and applicable block from the transaction that
performs the action.

### I13 — Lifecycle is a one-way stop

After a lifecycle tombstone commits, no not-yet-admitted output from that lane
can be created, delivered, executed, rerouted, or admitted. Replays return the
same stopped outcome. A tombstone never reopens or transfers the output.

### I14 — Successor isolation

A predecessor source can read and change only rows joined to its exact
assignment and wake chain. It cannot wake a successor holder, consume or refund
a successor counter, cancel a successor wake, settle a successor request, or
create evidence attributed to a successor lane.

### I15 — Admission defines the race

Lifecycle-first cancels a pending wake or queued turn. Delivery-first preserves
the truthful enqueue but does not authorize later turn admission.
Turn-admission-first permits the running turn to finish truthfully. No timestamp
grace period decides the result, and a later lifecycle transition does not
retroactively suppress an earlier admission at the same boundary.

### I16 — Work-blocked is absence of monitor production

While a current work-blocked fact stands, supervision and effort check-in
monitoring create no holder-facing prod, no stalled-work decision request or
notification, and no request to complete or surrender. The substrate neither
asserts another block nor consumes the existing one.

### I17 — Typed causality only

A patrol output acts only through one coherent output-source row. Missing,
stale, reused, cross-assignment, cross-generation, cross-request, forked-retry,
or mismatched source data uses admission fail closed without prompt or
timestamp inference.

### I18 — Stop evidence remains auditable

Every stopped pending wake or queued turn retains its original source row when
that row exists and records the exact lifecycle transition, work-blocked fact,
or source-mismatch cause that stopped it, the process principal, and the
no-replacement outcome. Existing historical rows remain byte-equal.

## Architecture

### 1. Additive state

R1. After schema initialization installs R25, it shall install and verify this
exact table before supervision or wake delivery starts:

```sql
CREATE TABLE supervision_patrol_response_episodes (
  assignmentId TEXT NOT NULL REFERENCES assignments(id),
  originatingWakeId TEXT NOT NULL UNIQUE REFERENCES wakes(wakeId),
  recoveryBranch TEXT NOT NULL CHECK (recoveryBranch IN ('prod','escalation')),
  recoveryRung INTEGER NOT NULL CHECK (recoveryRung > 0),
  sourceTerminalId INTEGER NOT NULL REFERENCES turns(seq),
  answerTerminalId INTEGER UNIQUE REFERENCES turns(seq),
  scheduledAt INTEGER NOT NULL CHECK (scheduledAt >= 0),
  acknowledgedAt INTEGER CHECK (acknowledgedAt >= scheduledAt),
  scheduledCause TEXT NOT NULL CHECK (scheduledCause = 'patrol_wake_scheduled'),
  scheduledPrincipal TEXT NOT NULL CHECK (scheduledPrincipal = 'process:tightbeam'),
  acknowledgmentCause TEXT CHECK (acknowledgmentCause = 'patrol_answer_terminal'),
  acknowledgmentPrincipal TEXT CHECK (acknowledgmentPrincipal = 'process:tightbeam'),
  PRIMARY KEY (
    assignmentId,
    originatingWakeId,
    recoveryBranch,
    recoveryRung,
    sourceTerminalId
  ),
  CHECK (
    (answerTerminalId IS NULL AND acknowledgedAt IS NULL
      AND acknowledgmentCause IS NULL AND acknowledgmentPrincipal IS NULL)
    OR
    (answerTerminalId IS NOT NULL AND acknowledgedAt IS NOT NULL
      AND acknowledgmentCause IS NOT NULL AND acknowledgmentPrincipal IS NOT NULL)
  )
);

CREATE TRIGGER supervision_patrol_episode_insert_coherent
BEFORE INSERT ON supervision_patrol_response_episodes
WHEN NEW.answerTerminalId IS NOT NULL
  OR NEW.acknowledgedAt IS NOT NULL
  OR NEW.acknowledgmentCause IS NOT NULL
  OR NEW.acknowledgmentPrincipal IS NOT NULL
  OR NOT EXISTS (
  SELECT 1
  FROM wakes w
  JOIN supervision_liveness_sidecar s
    ON s.wakeId=w.wakeId AND s.assignmentId=w.assignmentId
  JOIN assignments a ON a.id=w.assignmentId
  JOIN turns source ON source.seq=NEW.sourceTerminalId
  WHERE w.wakeId=NEW.originatingWakeId
    AND w.assignmentId=NEW.assignmentId
    AND w.origin='process:tightbeam' AND w.consumer='prompt'
    AND w.state='pending'
    AND w.createdAt=NEW.scheduledAt
    AND a.state='open' AND source.sessionKey=a.holderKey
    AND source.status IN ('delivered','canceled','failed','failed_unknown')
    AND s.controllerOrigin='scheduled' AND s.controllerState='pending'
    AND s.wakeKind=NEW.recoveryBranch
    AND (
      (NEW.recoveryBranch='prod' AND w.reresolve IS NULL
        AND w.reresolveSeed IS NULL AND w.reresolveRung IS NULL)
      OR
      (NEW.recoveryBranch='escalation' AND w.reresolve='lineage'
        AND w.reresolveSeed=a.holderKey
        AND w.reresolveRung=NEW.recoveryRung)
    )
)
BEGIN
  SELECT RAISE(ABORT, 'patrol response episode requires a coherent scheduled wake');
END;

CREATE TRIGGER supervision_patrol_episode_source_immutable
BEFORE UPDATE OF assignmentId, originatingWakeId, recoveryBranch, recoveryRung,
  sourceTerminalId, scheduledAt, scheduledCause, scheduledPrincipal
ON supervision_patrol_response_episodes
WHEN NEW.assignmentId IS NOT OLD.assignmentId
  OR NEW.originatingWakeId IS NOT OLD.originatingWakeId
  OR NEW.recoveryBranch IS NOT OLD.recoveryBranch
  OR NEW.recoveryRung IS NOT OLD.recoveryRung
  OR NEW.sourceTerminalId IS NOT OLD.sourceTerminalId
  OR NEW.scheduledAt IS NOT OLD.scheduledAt
  OR NEW.scheduledCause IS NOT OLD.scheduledCause
  OR NEW.scheduledPrincipal IS NOT OLD.scheduledPrincipal
BEGIN
  SELECT RAISE(ABORT, 'patrol response episode source is immutable');
END;

CREATE TRIGGER supervision_patrol_acknowledgment_one_way
BEFORE UPDATE OF answerTerminalId, acknowledgedAt, acknowledgmentCause,
  acknowledgmentPrincipal
ON supervision_patrol_response_episodes
WHEN NOT (
  (NEW.answerTerminalId IS OLD.answerTerminalId
    AND NEW.acknowledgedAt IS OLD.acknowledgedAt
    AND NEW.acknowledgmentCause IS OLD.acknowledgmentCause
    AND NEW.acknowledgmentPrincipal IS OLD.acknowledgmentPrincipal)
  OR
  (OLD.answerTerminalId IS NULL AND OLD.acknowledgedAt IS NULL
    AND OLD.acknowledgmentCause IS NULL AND OLD.acknowledgmentPrincipal IS NULL
    AND NEW.answerTerminalId IS NOT NULL AND NEW.acknowledgedAt IS NOT NULL
    AND NEW.acknowledgmentCause='patrol_answer_terminal'
    AND NEW.acknowledgmentPrincipal='process:tightbeam'
    AND EXISTS (
      SELECT 1
      FROM turns answer
      JOIN wakes w ON w.wakeId=answer.wakeId
      JOIN patrol_output_sources p ON p.wakeId=answer.wakeId
      JOIN assignments a ON a.id=answer.assignmentId
      JOIN supervision_liveness_sidecar s
        ON s.wakeId=w.wakeId AND s.assignmentId=w.assignmentId
      WHERE answer.seq=NEW.answerTerminalId
        AND answer.assignmentId=OLD.assignmentId
        AND answer.status='delivered' AND answer.endedAt=NEW.acknowledgedAt
        AND w.state='fired' AND w.origin='process:tightbeam'
        AND w.consumer='prompt' AND w.assignmentId=OLD.assignmentId
        AND p.assignmentId=OLD.assignmentId AND p.holderKey=a.holderKey
        AND p.sourceKind='supervision_episode'
        AND p.sourceRef=OLD.originatingWakeId AND p.sourceVersion=0
        AND p.rootWakeId=OLD.originatingWakeId
        AND a.state='open'
        AND s.controllerOrigin='scheduled' AND s.controllerState='settled'
        AND s.wakeKind=OLD.recoveryBranch
        AND (
          (OLD.recoveryBranch='prod' AND w.reresolve IS NULL
            AND w.reresolveSeed IS NULL AND w.reresolveRung IS NULL)
          OR
          (OLD.recoveryBranch='escalation' AND w.reresolve='lineage'
            AND w.reresolveSeed=a.holderKey
            AND w.reresolveRung=OLD.recoveryRung)
        )
    ))
)
BEGIN
  SELECT RAISE(ABORT, 'patrol response acknowledgment is one-way and coherent');
END;

CREATE TRIGGER supervision_patrol_episode_immutable_delete
BEFORE DELETE ON supervision_patrol_response_episodes
BEGIN
  SELECT RAISE(ABORT, 'patrol response episode is durable');
END;
```

R2. Startup shall compare the existing table and four triggers with the exact
normalized column, constraint, foreign-key, primary-key, unique-index, and
trigger definitions in R1. A missing object shall be created only when no object
from this closed set exists. An incomplete or unequal set shall raise
`incompatible_patrol_response_acknowledgment_v1` and shall not start
supervision or the wake scheduler. Startup shall not repair, rename, rebuild, or
choose rows from an unequal table.

R3. The implementation shall not backfill the table. Historical wakes and turns
remain unchanged and ineligible.

### 2. Episode creation

R4. When supervision schedules a `prod` or `escalation` wake, it shall pass one
internal typed episode value from the claimed pending tuple to the existing wake
scheduling transaction. This value is not a public dispatch field and is not
accepted from a CLI, user, agent, prompt, or hook.

R5. The scheduling transaction shall insert or verify the wake, scheduled
supervision sidecar, episode row, and ordinal-zero `supervision_episode` output
source together. `assignmentId` shall equal `pendingAssignment`.
`recoveryBranch` shall equal `pendingBranch`.
`recoveryRung` shall equal positive `pendingK`. `sourceTerminalId` shall equal
`lastEvaluatedTerminal`. `originatingWakeId` shall equal the inserted wake id.
`scheduledAt` shall equal that wake's `createdAt`.
`scheduledCause` shall equal `patrol_wake_scheduled`.
`scheduledPrincipal` shall equal `process:tightbeam`. The four acknowledgment
columns shall be null.

R6. The episode constructor shall validate the source terminal and assignment
before insertion. The source terminal shall exist and be terminal. Its session
shall equal the assignment holder. The assignment shall be open. A `prod` wake
shall have null `reresolve`, `reresolveSeed`, and `reresolveRung`. An
`escalation` wake shall have `reresolve = lineage`, `reresolveSeed` equal to the
holder, and `reresolveRung` equal to the episode rung.

R7. A repeated equal schedule shall return the existing episode without another
row. A repeated schedule that presents the same composite key or wake id with
unequal fields shall return `patrol_response_episode_conflict` and roll back
that schedule transaction. Invalid typed input shall return
`invalid_patrol_response_episode` and roll back the wake, sidecar, episode, and
output-source writes together.

R8. A `terminus` claim, ordinary wake, user wake, agent wake, condition wake,
checkpoint wake, routing wake, and escalation-decision notice shall create no
episode row.

### 3. Acknowledgment transition

R9. After `Ledger.finish_in_txn/4` wins a transition to `delivered`, the same
transaction shall call the one acknowledgment writer with the answer terminal
id as its only input. The writer shall derive the episode key from durable
joins through the answer wake's patrol output source and root wake. No caller
shall supply an assignment, wake, root, branch, rung, or source terminal to this
seam. Other terminal statuses shall not call it.

R10. The acknowledgment writer shall read the answer turn's wake and assignment
from durable rows. It shall traverse an unbroken retry chain to exactly one
root `originatingWakeId`. It shall update one episode from null
`answerTerminalId` to the exact answer terminal only when all exact-match facts
in Terms hold and the source assignment remains open. It shall set
`acknowledgedAt` from the terminal row's exact `endedAt`,
`acknowledgmentCause` to `patrol_answer_terminal`, and
`acknowledgmentPrincipal` to `process:tightbeam`. It shall change no
source-tuple field.

R11. If the episode already names the same answer terminal, an idempotent writer
call shall return the equal acknowledgment. If it names a different answer
terminal, the writer shall report
`patrol_response_acknowledgment_conflict`, leave the episode unchanged, and
allow the truthful answer terminal to commit unacknowledged. A second terminal
finalizer that loses the ledger compare-and-set shall return the existing
`:already_terminal` result and shall not invoke the writer.

R12. For a truthful terminal, a missing episode, missing output source, broken
retry chain, non-supervision wake, non-fired wake, cross-assignment join, wrong
root, wrong branch, wrong rung, wrong source terminal, stale closed assignment,
reused wake, or reused answer terminal shall return `:not_acknowledged`. It
shall leave episode state unchanged and shall not alter the terminal. R2, R7,
and R26-R30 own malformed schema and typed source input before a terminal
exists.

R13. A completion, surrender, or revoke that commits before the answer terminal
prevents R10 because the assignment is no longer open. A concurrent terminal
and lifecycle transition shall serialize through the database. Exactly the
transaction that first makes its complete predicate true wins; the loser
re-reads committed state and follows R12 or the existing closed-assignment path.

### 4. Ordered terminal evaluation

R14. The existing pending-branch drain shall run before evaluation of the new
terminal. It shall retain its current retry and clear behavior.

R15. For one terminal, the ordered turn-end schedule shall be:

1. evaluate and act on existing rails;
2. determine the existing prod-production candidate and terminal dedupe state;
3. absorb existing typed liveness receipts for that candidate assignment;
4. validate an exact acknowledgment match for this terminal;
5. run the existing due, gate, claim, branch, and dispatch behavior.

The checks and their actions in steps 3 and 4 shall occur in the same database
transaction that writes the terminal watermark or liveness rebase.

R16. If a rail acts, its current result halts the schedule. Acknowledgment
handling shall not run for that evaluation.

R17. If typed receipt absorption rebases the entitlement, the existing rebase
and watermark result shall win. The acknowledgment row shall remain unchanged.

R18. If no rail or typed receipt acts and an exact acknowledgment match exists,
the transaction shall advance `supervision_watermarks.lastEvaluatedTerminal` to
the answer terminal with its existing monotone compare-and-set. It shall leave
the entitlement, receipt ledger, counters, due time, pending tuple, wake rows,
and assignment unchanged. The observable evaluation result shall be
`:patrol_response_acknowledged`.

R19. If acknowledgment validation returns no exact match, the transaction shall
continue to the existing due, gate, claim, branch, and dispatch behavior. It
shall not create a partial acknowledgment or a suppression marker.

R20. A replay of the answer terminal after R18 shall return the existing
`:duplicate` result from the terminal watermark. A terminal greater than the
answer terminal shall not match the acknowledgment and shall follow R19. A
terminal lower than the watermark shall retain the existing `:coalesced`
result.

### 5. Evidence and compatibility

R21. The normal work-item trace shall retain its current keys, values, ordering,
and authorization. The new episode table is internal enforcement state.

R22. Existing causal and lifecycle rows shall remain unchanged. The episode
row, output-source chain, and their joins to the root wake, answer wake, source
terminal, answer terminal, assignment, sidecar, and typed wake cancellations
shall provide the exact audit evidence in Terms. The implementation shall not
add a public read command in this scope.

R23. The episode creator shall write the scheduled cause and principal from R5.
The acknowledgment writer shall write the acknowledgment cause and principal
from R10. Neither seam shall accept caller-supplied cause or principal values.

R24. The implementation shall use the existing boot terminal publication sweep
and supervision terminal dedupe for replay. It shall add no recovery worker.

### 6. Typed patrol output sources

R25. Before R1, schema initialization shall install and verify this exact
additive table and immutability triggers. Both tables shall exist before
supervision, effort check-in, or wake delivery starts:

```sql
CREATE TABLE patrol_output_sources (
  wakeId TEXT PRIMARY KEY REFERENCES wakes(wakeId),
  assignmentId TEXT NOT NULL REFERENCES assignments(id),
  holderKey TEXT NOT NULL REFERENCES sessions(sessionKey),
  sourceKind TEXT NOT NULL CHECK (sourceKind IN (
    'supervision_episode',
    'effort_generation_probe',
    'effort_generation_prod',
    'effort_decision_notification',
    'effort_decision_deadline'
  )),
  sourceRef TEXT NOT NULL,
  sourceVersion INTEGER NOT NULL CHECK (sourceVersion >= 0),
  rootWakeId TEXT NOT NULL REFERENCES wakes(wakeId),
  predecessorWakeId TEXT REFERENCES wakes(wakeId),
  retryOrdinal INTEGER NOT NULL CHECK (retryOrdinal >= 0),
  createdAt INTEGER NOT NULL CHECK (createdAt >= 0),
  sourceCause TEXT NOT NULL CHECK (sourceCause = 'patrol_output_scheduled'),
  sourcePrincipal TEXT NOT NULL CHECK (sourcePrincipal = 'process:tightbeam'),
  UNIQUE (rootWakeId, retryOrdinal),
  UNIQUE (sourceKind, sourceRef, sourceVersion, retryOrdinal),
  CHECK (
    (retryOrdinal = 0 AND rootWakeId = wakeId AND predecessorWakeId IS NULL)
    OR
    (retryOrdinal > 0 AND rootWakeId != wakeId AND predecessorWakeId IS NOT NULL)
  )
);

CREATE TRIGGER patrol_output_source_immutable
BEFORE UPDATE ON patrol_output_sources
BEGIN
  SELECT RAISE(ABORT, 'patrol output source is immutable');
END;

CREATE TRIGGER patrol_output_source_immutable_delete
BEFORE DELETE ON patrol_output_sources
BEGIN
  SELECT RAISE(ABORT, 'patrol output source is durable');
END;
```

R26. Startup shall compare `patrol_output_sources` and both triggers with the
exact normalized definitions in R25. A missing closed set shall be created. An
incomplete or unequal set shall raise `incompatible_patrol_output_sources_v1`
and shall not start supervision, effort check-in, or the wake scheduler.
Startup shall not repair, rename, rebuild, or choose rows from an unequal set.

R27. The internal constructor shall create the wake and its output-source row
in one transaction. It shall derive every source field from durable rows. No
CLI, hook, user, agent, prompt, or arbitrary wake caller can supply or copy an
output-source value.

R28. An ordinal-zero source shall satisfy exactly one row below.

| Source kind | Required durable join | `sourceRef` | `sourceVersion` |
| --- | --- | --- | --- |
| `supervision_episode` | the episode's originating wake, assignment, and current holder | `originatingWakeId` | `0` |
| `effort_generation_probe` | the generation's exact internal `wakeId`, assignment, generation, and frozen holder | `assignmentId` | `generation` |
| `effort_generation_prod` | the exact generation that atomically creates its sole holder prod | `assignmentId` | `generation` |
| `effort_decision_notification` | the open request, its current lineage rung, assignment, and frozen holder | `decisionRequestId` | `lineageRung` |
| `effort_decision_deadline` | the open request's exact `deadlineWakeId`, current rung, assignment, and frozen holder | `decisionRequestId` | `lineageRung` |

The constructor shall require an open assignment, equality between its current
holder and the source holder, an active holder session, an eligible source row,
and no existing ordinal-zero source for the same typed source. Failure rolls
back the wake and source together.

R29. An explicit retry transaction shall require the exact predecessor wake to
remain pending and shall require one typed delivery or destination-retirement
result that authorizes the existing replacement policy. It shall copy
`assignmentId`, `holderKey`,
`sourceKind`, `sourceRef`, `sourceVersion`, and `rootWakeId` from that
predecessor source. It shall set `predecessorWakeId` to the predecessor and
`retryOrdinal` to predecessor ordinal plus one. In one transaction it shall
revalidate R28, create the replacement wake and source, and cancel the
predecessor with a typed `replacement` outcome naming the new wake. Every
earlier predecessor shall already be canceled toward the next member of the
same chain. Two concurrent replacements for one predecessor shall race on the
root, typed source, and ordinal uniqueness constraints; one wins and the loser
returns the winning row. A fork or unequal replay shall return
`patrol_output_source_conflict` and create no wake.

R30. Replaying an equal schedule for the same wake shall return its existing
source row. It shall not create a retry or change a counter. A wake without an
output-source row is not retroactively eligible for this spec.

### 7. Lifecycle admission and tombstones

R31. Delivery admission shall re-read, in this order, the exact output-source
row, current wake state, unbroken retry chain, source row from R28, source
assignment, current holder, holder session, and destination session. It shall
act only when the current wake is the pending last member of its chain, the
assignment is open, the source holder is still the assignment's holder, the
holder is active, the destination is active, and every source join is exact.
The reads and enqueue, internal execution, or cancellation shall occur in one
database transaction.

R32. A direct supervision prod, effort generation prod, and effort generation
probe shall target the frozen holder. A supervision escalation shall retain its
existing same-assignment lineage rule and shall resolve only to an active
destination at R31. An effort decision notification or deadline shall target
the request's exact current expecter. No output may resolve through, or derive
authority from, another assignment. The active-destination check in R31 applies
to effort decision notifications even when their existing generic wake gate is
zero.

R33. Turn admission shall re-read R31's source, chain, assignment, holder,
holder-session, destination-session, and applicable block predicates for the
queued turn's exact `wakeId`, `assignmentId`, and destination. The prompt wake
shall be `fired`, shall be the last member of its chain, and shall join exactly
one queued turn. If all facts match, the transaction may claim that turn.
Otherwise it shall compare-and-set `queued` to `canceled`, set the terminal
time to the exact lifecycle or condition-fact timestamp that caused the stop,
and record the exact stop evidence under R44. When no durable stop fact exists
because the source itself is malformed, it shall use the admission transaction
clock and name `patrol_output_source_mismatch` as cause. It shall not start the
harness, retarget the turn, or enqueue a replacement.

R34. Completion, surrender, revoke, and holder retirement shall, in their
existing lifecycle transaction, tombstone every not-yet-admitted patrol output
for the exact assignment. The transaction shall dispose supervision and effort
state through their existing seams, cancel every pending source wake with no
replacement, supersede any open effort decision request, cancel its pending
deadline and notification wakes, and cancel every queued turn joined through
`patrol_output_sources`. A replay shall return the already-tombstoned state.

R35. A turn that reached `running` through R33 before the lifecycle transaction
committed is already admitted. It may finish through the normal ledger seam.
The later lifecycle tombstone shall not rewrite it. R10 and R13 still prevent a
new acknowledgment or prod from the now-closed assignment.

R36. A missing source, broken predecessor chain, inactive or missing session,
closed or mismatched assignment, changed holder, stale generation, closed or
advanced decision request, reused source, or cross-assignment wake shall use
admission fail closed. It never means acknowledgment fail closed, normal prod
behavior, or successor-lane selection. A pending-wake source mismatch shall use
the typed cancellation reason `patrol_source_mismatch`, requester
`tightbeam:wake-scheduler`, causal source kind `scheduler_delivery`, causal
source ref equal to the exact wake id, and a no-replacement outcome.

R37. Historical turns 19082, 19084, and 19086 occurred at
1786525417781, 1786525418890, and 1786525419917. The later revoke committed at
1786525633131. The implementation shall leave those rows byte-equal. F10 shall
assert only that each recorded delivery precedes the recorded revoke. Neither
the implementation nor the fixture shall add a classification, relabel a turn
as post-revoke, or infer an unrecorded active-session predicate from that
order.

### 8. Current work-blocked recognition

R38. The monitor-production checks for supervision and effort check-in shall
read the exact current work-blocked fact for the frozen holder. They shall
check at initial match, pending-branch dispatch, wake creation, delivery
admission, effort probe execution, effort request creation, effort decision
notification or deadline execution, and queued-turn admission. At every act
boundary, recognition and its action shall be one transaction. R40's silent
internal recheck is the only wake creation permitted by a positive block match.

R39. When a current work-blocked fact stands, supervision shall retain its
existing `:work_blocked` no-match result. A branch claimed before the fact shall
clear without dispatch. A wake created before the fact shall be canceled with
reason `production_unmatched`, causal source `condition_fact` and the exact
fact id, and no replacement. A queued patrol turn shall follow R33. Any charged
prod rung shall be refunded exactly once; no entitlement generation or future
terminal shall be consumed.

R40. When an armed effort probe sees a current work-blocked fact, its
transaction shall mark that generation `probed` and record evidence outcome
`work_blocked` with the exact fact id. In the same transaction it shall create
one next generation and its typed `effort_generation_probe` internal wake at
the existing horizon with the same multiplier and `agentProdded` value. It
shall not observe zero effect, create a holder prod, open or advance a decision
request, or create a prompt notification.

R41. Filing `work-blocked` shall use one in-transaction recognition seam to
cancel already pending effort holder prods and supersede open effort decision
requests for the blocked holder. It shall cancel their pending notification and
deadline wakes with the fact id and no replacement. It shall not file another
condition fact, retire or replace the holder, close the assignment, or decide
the request.

R42. A patrol output queued before `work-blocked` and delivered or admitted
after it shall stop under R38-R41. Replaying its probe, wake, notification,
deadline, cancellation, or queued-turn admission shall create no additional
output, request, fact, refund, or cancellation effect.

R43. A later authorized `work-unblocked` fact makes the next internal effort
probe and the next supervision evaluation use ordinary open-lane behavior.
No suppressed prod, escalation, request, or retry is replayed. A block on a
different holder changes nothing in this lane.

### 9. Evidence, ordering, and compatibility

R44. Lifecycle and block stops shall preserve any immutable output-source row
that exists and use the existing typed wake-cancellation and terminal evidence
seams. The wake-cancellation vocabulary shall add only the R36
`patrol_source_mismatch` reason under the stated requester, source, and
no-replacement tuple.
Each stop shall name the exact wake, assignment, causal source kind and ref,
source version when present, process principal, no-replacement outcome, and
committed time. A source-mismatch stop shall name the absent or unequal field.
A queued-turn stop shall append one lifecycle event that names its terminal id
and wake id. Replays shall return the existing rows without appending
duplicates.

R45. The implementation shall not parse prompt or reply text, infer causality
from timestamps, select a successor by work item or role, or change generic
`targetGate = 0` behavior for outputs outside the closed patrol set. It shall
not alter ordinary work, user or agent wakes, tool effects, unrelated decision
notifications, or the acknowledgment ordering in R14-R20.

R46. The implementation shall not backfill `patrol_output_sources`. Historical
wakes and turns retain their existing evidence and are ineligible for the new
admission mechanism. The implementation shall add no worker or sweeper; the
existing schedule, delivery, lifecycle, condition-fact, and ledger seams own
all actions.

## Acceptance

Each fixture shall use a real database and the real assignment, wake schedule,
wake delivery, ledger terminal, supervision evaluation, receipt, and lifecycle
seams at source baseline `ac8651dcb104f312da1c67e0cb7b1abebc640b2b` plus
the implementation. A fixture may insert givens before the exercised seam. It
shall not directly insert an acknowledgment or substitute a source insert for
the constructor under test. To exercise downstream mismatch handling, F18 may
seed one schema-valid but semantically mismatched output-source given before
delivery or turn admission; that fixture shall identify the bypassed
constructor and shall still use the real admission seam. No fixture shall
replace an exercised mutation with a stub.

### F1 — The observed loop terminates

Given open assignment A held by active session H, delivered source terminal T0,
and a due tier-1 prod claim,

When the real schedule creates wake W and episode
`(A, W, prod, 1, T0)`, the real wake delivery creates answer turn T1, and T1
finishes `delivered` without a rail action or typed liveness receipt,

Then the terminal transaction records exactly one acknowledgment with
`answerTerminalId = T1`, evaluation returns
`:patrol_response_acknowledged`, the watermark advances to T1, and no second
prod wake, pending branch, counter change, entitlement generation, or answer
turn is created. Exactly one ordinal-zero `supervision_episode` output source
binds W to A, H, and root W.

Trace: R4–R10, R14–R18, R25, R27–R28, R31, R33, I1–I5, I10–I12, I17.

### F2 — Ordinary work remains eligible

Given the completed F1 episode and a later ordinary turn T2 for H created by a
user message, agent wake, or ordinary work continuation,

When T2 finishes and the existing prod-production conditions match,

Then no episode has `answerTerminalId = T2`, the F1 acknowledgment is not
reused, and T2 follows the existing receipt, due, claim, counter, branch, and
dispatch behavior.

Trace: R8, R19–R20, I4, I8, I10.

### F3 — Effects are preserved

Given three otherwise equal F1 episodes,

When the first answer turn creates a real typed artifact receipt, the second
creates a real verdict receipt, and the third files a real progress attest
before each turn finishes,

Then artifact and verdict receipt absorption each win before acknowledgment
suppression and retain their existing rebase behavior. The progress attest
remains durable and is not converted into a receipt or acknowledgment. The
third terminal alone follows the exact F1 acknowledgment result. A later
terminal after that progress remains eligible under F2.

Given a fourth F1 answer turn that commits a real tool call, tool result, and
their durable message rows before it finishes,

When its answer terminal is acknowledged,

Then the acknowledgment changes only that terminal's prod-ladder eligibility.
The tool call, result, message rows, and any tool-owned durable effect remain
byte-equal and visible through their existing read surfaces.

Trace: R15–R19, R21–R23, I5, I8–I10.

### F4 — Failure and lifecycle are not suppressed

For each row below, Given an exact scheduled episode, When the real named seam
runs before terminal evaluation, Then the expected result holds:

| Real seam | Expected result |
| --- | --- |
| answer turn ends `canceled` | no acknowledgment; existing canceled-terminal behavior |
| answer turn ends `failed` | no acknowledgment; existing failure and bubble behavior |
| boot recovery ends the answer `failed_unknown` | no acknowledgment; existing unknown-outcome behavior |
| completion attest commits before answer finish | assignment closes; no acknowledgment; entitlement remains disposed |
| surrender commits before answer finish | assignment closes; no acknowledgment; entitlement remains disposed |
| opener revoke commits before answer finish | assignment closes; no acknowledgment; entitlement remains disposed |
| exact rail action wins on delivered answer evaluation | rail result wins; acknowledgment does not suppress the rail |

No row may create a replacement episode, reopen an assignment, or create a
patrol suppression for a future terminal.

Trace: R9–R13, R16, I3, I5–I7.

### F5 — Invalid episode creation and acknowledgment mismatch fail closed

Given schedule inputs that differ from one valid episode in exactly one
dimension,

When the real episode constructor runs, Then each row below refuses the schedule
transaction and creates no wake, sidecar, episode, or output source:

| Invalid schedule input | Required evidence |
| --- | --- |
| null, zero, negative, or unknown source terminal | `invalid_patrol_response_episode` |
| branch outside `prod` or `escalation` | `invalid_patrol_response_episode` |
| rung zero, negative, or unequal to the claimed pending value | `invalid_patrol_response_episode` |
| wake id belongs to another assignment | `invalid_patrol_response_episode` |
| source terminal belongs to another holder | constructor refusal; no episode |
| escalation wake has another lineage rung | constructor refusal; no episode |
| prod wake carries lineage fields | constructor refusal |

Given a real answer terminal and a stored episode candidate that differs from
the truthful wake-to-turn join in one dimension,

When the real acknowledgment writer and terminal evaluation run, Then each row
below leaves the terminal truthful and unacknowledged and follows normal
behavior:

| Acknowledgment mismatch | Required evidence |
| --- | --- |
| missing episode row | zero acknowledged episodes for the wake |
| answer turn joins a wake outside the episode's coherent retry chain | `:not_acknowledged` |
| wake or turn names another assignment | `:not_acknowledged` |
| sidecar branch differs from the episode | `:not_acknowledged` |
| escalation wake lineage rung differs from the episode | `:not_acknowledged` |
| source assignment closes before finish or evaluation | no acknowledgment or no suppression |
| an acknowledged wake is presented by a second answer terminal | conflict is reported; second terminal remains normal |
| an answer terminal already belongs to another episode | uniqueness or exact-join refusal; terminal remains normal |

The fixture shall assert that no acknowledgment mismatch changes a counter,
entitlement, receipt, pending branch, wake, source terminal, or existing
acknowledgment.

Trace: R2, R6–R7, R10–R13, R19, I1–I4, I6.

### F6 — Branch and rung isolation

Given four independent real assignments whose episodes cover `(prod,1)`,
`(prod,2)`, `(escalation,1)`, and `(escalation,2)`, each with a distinct wake,
source terminal, holder, and answer turn,

When each answer terminal finishes in an interleaved order,

Then each terminal acknowledges only its own composite key. Replacing any wake,
branch, rung, or source terminal with a value from another row produces F5
normal behavior. No acknowledgment suppresses another episode's answer.

Trace: R5–R12, R18–R20, I1–I4.

### F7 — Concurrency

Given one valid delivered answer turn and one unrelated terminal for another
session and assignment,

When two terminal finalizers race for the answer turn, two supervision
notifications race for its terminal, and the unrelated terminal evaluates
concurrently,

Then one terminal finalizer wins, one acknowledgment row names the answer, one
watermark transition consumes the answer terminal, and zero duplicate prod
wakes arise from it. The unrelated terminal is not acknowledged and follows
normal behavior. The database contains no partial or conflicting episode or
output source.

Trace: R9–R13, R15–R20, R25, R27–R31, R33, I1–I4, I11–I12, I17.

### F8 — Crash boundaries

For each boundary below, Given one F1 episode, When the process stops at the
named boundary and the existing recovery path restarts, Then the recovered
state equals one uninterrupted run:

1. before the wake, sidecar, episode, and output-source schedule transaction
   commits;
2. after that transaction commits and before wake delivery;
3. after wake delivery commits and before answer turn terminalization;
4. inside the terminal-plus-acknowledgment transaction before commit;
5. after terminal-plus-acknowledgment commit and before terminal publication;
6. after R18 commits and before its caller receives the result.

Rollback exposes none of that transaction's writes. A crash before boundary 1
commits leaves no wake or key; recovery may schedule one new episode through the
normal seam. After boundary 1 commits, recovery reuses that exact episode, wake,
and output source. In either case, recovery exposes at most one acknowledged
episode, one output source at ordinal zero, one answer terminal for its chain,
and one watermark transition. It does not suppress a future terminal.

Trace: R5, R7, R9–R11, R18, R20, R24–R31, R33, I1–I4, I12, I17.

### F9 — Replay

Given the final F1 state,

When the scheduler replays the exact episode bytes, terminal publication
replays the answer terminal, supervision re-evaluates the same terminal, and a
later terminal T2 then finishes,

Then the schedule returns the equal episode, a direct idempotent writer call
returns the equal acknowledgment, a second terminal finalizer returns
`:already_terminal`, same-terminal evaluation returns `:duplicate`, and T2
follows normal behavior. The equal output source is reused at ordinal zero. Row
counts, counters, entitlement generation, wake counts, and source facts remain
equal to the uninterrupted F1 result before T2.

Trace: R7, R11, R20, R24–R30, I1–I4, I10, I17.

### F10 — Recorded delivery-before-revoke is not rewritten

Given an immutable evidence fixture containing terminal turns 19082, 19084, and
19086 at 1786525417781, 1786525418890, and 1786525419917, followed by revoke of
their source assignment at 1786525633131,

When the fixture reads those durable rows and runs the paired lifecycle
admission controls,

Then the three turns remain byte-equal. The assertion records only that each
delivery timestamp precedes the revoke timestamp; it does not label a new
product state, classify them as post-revoke, or infer whether the destination
was active from timestamps. A paired synthetic control in which all R33
predicates are true and the turn reaches `running` permits that turn to finish;
a later revoke leaves the admitted turn unchanged.

Trace: R35, R37, R44, I9, I15, I18.

### F11 — Terminal state precedes observation

Given assignment A with `state = closed`, `outcome = revoked`, and
`closedAt = 1786525633131`, its frozen holder H retired with zero open
assignments, and a stale supervision escalation, effort probe, holder prod,
decision notification, and deadline candidate for A,

When each real creation, delivery, internal-consumer, and turn-admission seam
runs in both original and replay order,

Then no new wake or turn is created, delivered, executed, rerouted, or admitted.
Existing pending candidates are canceled once with A's terminal lifecycle as
cause, existing queued turns become `canceled` without harness execution, and
replays return the same stopped rows. No candidate reaches any session or
assignment that succeeded A.

This fixture carries owner evidence
`att_83bc1c99-6de5-469e-9d23-dbb4cc59f96d` and specimen `att_ed7280bb` without
mutating either historical review assignment.

Trace: R31-R36, R44-R46, I12-I15, I18.

### F12 — Queue-before, lifecycle-before-admission

For each lifecycle transition `completed`, `surrendered`, explicit `revoked`,
and holder retirement, Given one pending source wake and one separately queued
patrol turn created while assignment A and holder H are current,

When the real lifecycle transaction commits before wake delivery or turn
admission,

Then that transaction cancels the pending wake and queued turn, disposes only
A's supervision and effort state, supersedes only A's open effort request, and
records the exact lifecycle cause. Later delivery, claim, terminal publication,
and boot replay are idempotent and start no harness.

Trace: R33-R36, R44, I12-I15, I18.

### F13 — Predecessor and successor isolation

Given predecessor assignment A with a root wake and two retry-source rows,
closed A, and open successor assignment B on the same work item with its own
holder, entitlement, effort generation, request, wake, and counters,

When A's root, first retry, second retry, cancellation, delivery, and queued
turn are replayed concurrently with a valid B prod,

Then every A action returns its stopped predecessor result. It creates no turn
for B, changes no B counter or generation, settles no B request, cancels no B
wake, and writes no B-attributed evidence. B's prod follows ordinary behavior
exactly once.

Repeat with A and B sharing a holder and with distinct holders. The outcome is
the same because assignment id, not placement or work item, defines the lane.

Trace: R27-R36, R44-R46, I13-I14, I17-I18.

### F14 — Lifecycle races have only admission-before or lifecycle-before

Given one valid source wake for open assignment A, run each pair below behind a
database barrier:

1. delivery admission races completion, surrender, revoke, and holder
   retirement in four independent runs;
2. queued-turn admission races the same four transitions;
3. retry creation races each transition; and
4. two retry creations race each other while A remains current.

Then each race exposes only its ordered result. Delivery-first records the
fired wake and queued turn; the later lifecycle transaction cancels that queued
turn. Lifecycle-first cancels the pending wake and creates no turn.
Turn-admission-first records a running turn that R35 permits to finish;
lifecycle-first cancels the queued turn without starting the harness.
Retry-first records one replacement that the later lifecycle transaction
cancels; lifecycle-first creates no replacement. In the two-retry race, one
ordinal wins and the loser returns it. No run creates a forked chain, partial
source, replacement after tombstone, or successor effect.

Trace: R29, R31-R36, I12-I15, I17-I18.

### F15 — Lifecycle crash and replay

For a pending wake and a separately queued turn, stop and restart at each
boundary below:

1. before an initial output source and wake commit;
2. after source and wake commit but before delivery admission;
3. inside delivery admission before commit;
4. after turn enqueue but before turn admission;
5. inside lifecycle tombstoning before commit;
6. after lifecycle commit but before the caller receives its result;
7. inside queued-turn cancellation before commit; and
8. after cancellation commit but before terminal publication.

Then rollback exposes none of the interrupted transaction. Recovery reuses the
same source or stopped rows, produces at most one wake per root and ordinal, one
wake-cancellation row per stopped wake, one terminal and one lifecycle event
per stopped queued turn, and never admits a future or successor turn because
of the replay.

Trace: R27-R36, R44, R46, I12-I15, I17-I18.

### F16 — Current work-blocked stops every holder-facing monitor output

Given open assignment A held by active H, file current authorized
`work-blocked` fact F through the real condition-fact seam before item 1. For
items 2-8, prepare the named state without F, file F through that seam, and then
exercise the named later edge. Run item 9 after each stopped edge:

1. supervision initial match;
2. a prod or escalation branch claimed before F;
3. a supervision wake created before F;
4. a supervision answer turn queued before F;
5. an armed effort probe with `agentProdded = 0`;
6. an armed effort probe with `agentProdded = 1`;
7. a holder prod queued before F;
8. an open effort decision request with pending notification and deadline; and
9. five replays of every stopped edge.

Then supervision returns or preserves `:work_blocked`, clears the claimed
branch, cancels the pending wake or queued turn, and refunds a charged rung once.
Each effort probe records only outcome `work_blocked` with F and arms one later
internal probe. The holder receives no prod and no request to complete or
surrender. No stalled-work request or notification is created or advanced; an
existing one is superseded and its pending outputs are canceled. Exactly one
authorized block fact remains, and the substrate asserts no second block.

No output may say that A or H stalled. The cancellation and probe evidence may
truthfully identify F, and it is not holder-facing.

Trace: R38-R44, I12, I16-I18.

### F17 — Blocked-versus-open controls

Given the F16 database, When an authorized `work-unblocked` fact U later
supersedes F and the next internal effort probe and next supervision terminal
run,

Then both use ordinary open-lane behavior from new current state. They do not
replay a suppressed wake, retry, request, notification, or counter charge.

Given instead a current block on another holder, Then A behaves exactly like an
unblocked open assignment. Given a stale block followed by U, Then the stale
fact has no effect. Given F while an ordinary user wake, agent wake, tool call,
or unrelated decision notification targets H, Then that ordinary action retains
its existing behavior.

Trace: R38, R43, R45, I16.

### F18 — Output-source mismatches fail closed

Starting from one valid source of each R28 kind, change exactly one dimension:
assignment, frozen holder, destination, source kind, source ref, source version,
root wake, predecessor wake, retry ordinal, generation, decision request,
lineage rung, wake id, session state, assignment state, or current-holder
relation.

When the real constructor, delivery admission, internal consumer, and queued
turn admission run,

Then creation mismatch rolls back source and wake together. Later mismatch
cancels only the exact candidate with reason `patrol_source_mismatch` and no
replacement. It does not parse a prompt, select another assignment, run the
harness, change an acknowledgment, or touch a successor. Replaying the
mismatch changes no row count or counter.

Trace: R25-R36, R44-R46, I12-I14, I17-I18.

### Requirement-to-fixture map

| Requirement | Fixtures |
| --- | --- |
| R1–R3 | F5, F8 |
| R4–R8 | F1, F2, F5, F6, F8, F9 |
| R9–R13 | F1, F4–F9 |
| R14–R20 | F1–F9 |
| R21–R24 | F2–F4, F8–F9 |
| R25–R30 | F1, F5, F7–F9, F11–F15, F18 |
| R31–R37 | F1, F7–F8, F10–F15, F18 |
| R38–R43 | F16–F17 |
| R44–R46 | F10–F18 |

## Open Questions

None. Artifact `art_023f8032` and its spec-approved verdict remain immutable
historical evidence for the superseded hash; they are not implementation
authority. The implementation scope remains blocked until this amended file is
cold-digested, recorded as one replacement artifact, receives one superseding
`spec-approved` verdict for its exact hash, and one fresh linked independent
review returns `reviewed-clean` for that hash.
