# Completion-escalation rail v2

Status: READY FOR SUCCESSOR INDEPENDENT REVIEW for
`wi_809821f8-e72b-41d8-b4b5-af28c7e670a6`.
This file revalidates reviewed artifact `art_a22ba0ec`, SHA-256
`cd1a9a99d0f041cd88077b4e55f1cd23e76b26b4804f0478ef94ed6a7a6165d6`, against
Tightbeam 0.1.7 release commit `6c13efcbe9e1ae247b8aa7e91a374015c74dc947`.
Independent verdict `att_35dc33fc-660c-4989-b78d-56eab886a1e7` requested changes to
artifact `art_46d2f24b`, SHA-256
`96bbca96ab56e5269e40b19799f9b080142e8868eb635b8d15259e7988597736`. This amendment
removes retired-session replay and carries the authenticated device user as a typed
principal through generic retirement. It supersedes the predecessor only after an
independent reviewer clears this file's new exact hash. Implementation stays
unauthorized before that verdict. The park decision remains blocked on
`wi_6937890c-6ba6-48b7-a9d2-4eb4510fe245`.

## Goal

When a child session files a completion attest, Tightbeam records and routes that
completion to an agent that can act on the child. The completion record and its first
notification wake commit in the same transaction as the attest and assignment close.
If corrupt state contains neither an active same-owner lineage ancestor nor the
owner's Main session, Tightbeam commits the completion with the named
`main-unavailable` delivery failure instead of inventing a recipient. R5 defines this
only exception to the first-wake guarantee.

When the completed holder is the owner's exact built-in Main, that Main is both child
and final backstop. Tightbeam creates the normal open request and addresses its notice
to that exact Main. The Main session can explicitly retain itself into the named
`retained_root` terminal state. Tightbeam does not auto-retain it. Park and retire stay
unavailable for the permanent root session.

If that close leaves a non-root child session with zero open assignments, the same
record becomes an action-needed request. A session principal authorized by R11 or the
owner user chooses exactly one disposition under R11: retain, park, or retire. Tightbeam
records and enacts that explicit choice. Tightbeam does not choose a disposition and
does not auto-retire.

This rail implements substrate law over rows. It does not teach a conversational norm.
The conditions are observable assignment, attest, session, and wake rows; the action is
deterministic routing and verification. The retain/park/retire choice stays with an
agent or user (wisdom 1, 5, 6, 8, and 9).

### Authority and current evidence

- The current accountability amendment requires unresolved operational events to
  escalate through the durable parent chain, names the owner's Main as the normal-root
  parent, and stops escalation only after a live authority records the required
  disposition or a separate terminal contract closes the obligation
  (`accountability-constitution-v1.md:27-31`).
- Direct owner assignment `asg_a12d6873-9b00-4924-b3c8-674582fd7973` and digest
  `att_55fab334-3d4b-413a-bd85-fd8e3882ba67` require a parent-facing completion notice,
  an action-needed request when the child reaches zero open assignments, an explicit
  retain/park/retire choice, and no automatic retirement.
- A completion is already a holder-filed row. The attest insert, guarded assignment
  close, work-item bracket, liveness transition, supervision transition, effort
  cancellation, and marker writes share one transaction
  (`attest-v1.md:35-42,181-196`; `assignments.ex:1124-1200`).
- Assignment creation accepts any active session and does not exclude `isBuiltIn`, while
  the retire rail makes built-in Main permanent (`assignments.ex:918-1057`;
  `gateway.ex:5042-5052`). Product ruling
  `att_e7b138b6-fb9e-4fc5-a00e-b016390a2e25` keeps Main assignable and admits only an
  explicit retain self-disposition for that exact root session.
- `Assignments.open_count/2` already defines the session-level open-assignment count
  (`assignments.ex:211-220`).
- The work-item bracket is not this rail. It counts assignments for one work item and
  targets the work-item's user owner (`work_items.ex:503-537`). This rail counts
  assignments for one child session and targets the session's living lineage parent.
- Active lineage resolution already exists as a row-only walk. It skips retired
  ancestors and distinguishes a parentless session from an exhausted lineage
  (`productions/bubble.ex:332-365`).
- The ordinary wake store is durable and at-least-once; `turns.wakeId` provides the
  exactly-once enqueue backstop (`wakes.ex:104-200`; `ledger.ex:1-18,99-148`).
- Wake delivery can re-resolve a stale lineage target at act time, but the current
  generic ladder reads no ancestor owner and can therefore return a foreign-owner rung
  (`supervision.ex:735-770,2680-2695`; `gateway.ex:1313-1353`). R5 and R7 add the owner
  pin only for completion-linked routing.
- The current assignment-change wire event is a post-commit best-effort callback and
  cannot carry this guarantee (`assignments.ex:691-709`; `gateway.ex:5631-5648`).
- The current retired-strand parent prompt is also post-commit and has no durable wake
  row (`supervision.ex:1928-1961`). It is evidence, not a reusable guarantee.
- The CLI exposes only `harness-process list`; it exposes no park/relaunch action
  (`cli/src/args.rs:513-514,1488-1501`). The existing internal harness park records do not
  authorize inventing that missing operator primitive (`harness_process.ex:202-315`).

### Revalidation rulings for the five post-review hunks

1. **Adopt with the R11 boundary.** The ordinary three-choice request applies to a
   non-root child. The exact root Main follows its separate retain-only contract. An
   ordinary same-owner sibling still cannot act; R11's typed recipient, owner-matched
   ancestor, and owner-user checks remain authoritative.
2. **Adopt.** R11's generic-retire gate applies only after a call reaches that precedence
   step. Root park and root retire refuse earlier. The handler identifies generic-retire
   intent wakes through the existing deterministic id seam; it does not rely on the word
   “canonical.”
3. **Adopt.** A14's generic-retire lease fixture uses an ordinary non-root child because
   root Main cannot enter the generic retire path.
4. **Adopt.** A24 uses one open root request with a stopped scheduler. Exact Main calls
   park and then retire against that row. This proves both refusals without pretending
   that two live empty epochs can coexist after assignment-open supersession.
5. **Replace as stale evidence.** The reviewed-clean predecessor verdict is
   `att_4f59063a-f3e5-4697-9957-1e2c0787fada` against exact `cd1a9a99…` bytes and old
   source `95aefa68476240e3364312ad8ff9a2958584ef7e`. Recon verdict
   `att_eeb27cd2-b27a-4e79-af19-435fd1f564b4` requires this successor and one new
   independent review against `6c13efc…`. Open Question 2 records the current gate.

### Amendment rulings for `att_35dc33fc-660c-4989-b78d-56eab886a1e7`

1. **F1 — delete retired-session replay.** A retired session has no CLI authentication
   seam in release `6c13efc…`. R11, R15, A13, and A16 therefore require a session caller
   to remain active for terminal read or replay. The owner user and an admin retain their
   ordinary read authority. An owner-user replay succeeds only when `actedByUser` names
   that owner. This amendment adds no retired-session credential or verb exception.
2. **F2 — carry the authenticated device user as a typed principal.** The device DELETE
   route already authenticates a device row before it constructs generic retirement
   (`wire/router.ex:235-252,433-443`). It must place
   `principal={:user, device.user_id}` on that call. Gateway retirement must derive the
   owner and the durable acting principal from the typed principal, not from `origin`.
   R3, R12, R13, A14, and A21 specify and verify this path.

## Non-Goals

- No automatic retain, park, retire, reassignment, or reparenting.
- No new park, relaunch, stop, recycle, or process-kill contract. Work item
  `wi_6937890c-6ba6-48b7-a9d2-4eb4510fe245` owns that primitive.
- No change to work-item causal parent derivation, `createdInTurnSeq`, `jobRef`, or the
  topology projection in `Toplines` (`toplines.ex:435-573,650-710`).
- No replacement for the work-item routed/slate brackets. A work item with zero open
  assignments and a session with zero open assignments are different facts.
- No replacement for fault bubbling, supervision prods, strand handling, role fallback,
  or the decision-request statute mechanism.
- No content parsing. Prompt text is presentation. Reads and actions resolve from typed
  columns and wake/turn joins.
- No new scheduler, delivery worker, retry process, standing fact, role, or socket frame.
- No retroactive completion notices for assignments already closed before this table
  exists.
- No downgrade preservation after the first completion row exists. Forward migration
  and rollback before feature use are the supported database-version boundary.
- No notice for progress, surrender, revoke, or retire interruption. The shared
  ownerless-terminal fallback work item
  `wi_3d6d13a0-c4cf-4370-88a1-b407c41ff7c1` owns expansion beyond completion.
- No user-interface design.

### Deletion assessment

ADD wins because a durable parent-facing completion and a session-slate disposition
request do not exist. DELETE loses because deleting child completion or parent
accountability would violate the work model. ACCEPT loses because an event-log-only
failure would leave no addressed request and no acknowledgment path.

The added mechanism is one completion table, one wake-membership table, and one producer.
The membership table makes a completion wake mechanically identifiable after the
completion row advances to a later generation or terminal state. ADD wins because the
current-only wake ids cannot identify a delayed callback for an older generation. DELETE
loses because removing the stale-delivery guard permits an obsolete request to reach a
parent. ACCEPT loses because an unclassified pending callback can create a false current
request. The table stores membership only; it does not duplicate wake state, timing,
routing, or cancellation. The mechanism reuses the wake scheduler, lineage resolver,
existing assignment count, existing retire path, and the future park primitive.

The deadline consumer needs one wake-owned in-transaction fired CAS. ADD wins because
the current internal-consumer callback has no such public seam. DELETE loses because a
deadline left pending repeats forever. ACCEPT loses because producer-owned wake SQL
would split mutation ownership and make the source-closure rail false.

The existing work-item slate wake remains. Deleting it would lose intent disposition
when several sessions work on one item. Folding this rail into it would lose session
lifecycle disposition when one session works across several items.

The existing generic `decision_requests` table is not reused. Its closed `statute` and
`effort` kinds, authorization, outcomes, waiver semantics, and consumption lifecycle
serve different invariants (`escalation.ex:27-94,292-321`). Extending that central
mechanism would widen more surface than the required completion lifecycle. The focused
row below carries both the notice and its optional disposition request.

The root-Main exception is one branch in the existing disposition seam. ADD wins because
the product ruling preserves Main assignability and requires explicit retain. DELETE
loses because forbidding Main assignments contradicts that ruling. ACCEPT loses because
an unactionable self-addressed request would not provide the required retain outcome.
The branch does not grant self-disposition to an ordinary child.

## Terms

- **Child session**: the assignment holder named by `assignments.holderKey` on the
  assignment closed by the completion attest. It is one session incarnation, not a role.
- **Completion cause**: the committed `attests` row with `kind='completion'`, joined
  through `assignments.closingAttestId`. The cause principal is
  `session:<attests.bySession>`.
- **Immediate parent**: `sessions.spawnedBy` on the child session. It can be absent or
  retired. This fact never changes when the notice routes elsewhere.
- **Capable agent parent**: the first session in the child's `spawnedBy` lineage whose
  session row has `state='active'` and the child's `ownerUserId`. A foreign-owner row is
  a boundary, not an eligible parent. “Capable” means addressable by an active session
  row; Tightbeam does not infer model quality, intent, attention, or likely compliance.
  The existing lineage resolver numbers active ancestors, so the nearest eligible active
  ancestor is active rung 1 even when one or more retired ancestors lie between it and
  the child (`supervision.ex:735-770,2680-2695`). Completion routing adds the owner check
  that the generic resolver lacks.
- **Main fallback**: the owner's built-in Main session, used as the notification
  recipient only when the lineage contains no capable agent parent. Main fallback does
  not create or change a work-item parent edge.
- **Root Main holder**: a child session whose row has `isBuiltIn=1` and whose
  `sessionKey` equals `Org.personal_session_key(ownerUserId)`. The exact key and built-in
  marker must both match. A custom session with a Main-like name is not a root Main.
- **Owner pin**: `ownerUserId` copied from the child session by the close transaction.
  Initial routing, reissue routing, and act-time routing return only a session whose
  row carries this owner. A foreign ancestor is a hard lineage boundary, not a rung to
  skip or a recipient.
- **Completion record**: one `completion_escalations` row keyed by the closing attest.
  It contains the cause, the initial routing ruling, the current delivery generation,
  and the optional disposition lifecycle.
- **Completion wake membership**: one `completion_escalation_wakes` row for each notice
  or deadline wake that the completion producer arms. It maps a durable wake id to one
  completion id, generation, and literal kind. Wake state and timing remain in `wakes`.
- **Receipt acknowledgment**: a turn with `wakeId = currentNoticeWakeId` reaches
  `status='delivered'`. It proves that the current recipient ran the notice turn. It
  does not choose a disposition.
- **Disposition acknowledgment**: an authorized `completion-disposition` call commits
  `status='acknowledged'` or the root-only `status='retained_root'`, with one decision and
  the acting typed principal.
- **Typed caller principal**: the authenticated caller identity carried separately from
  presentation origin. Its admitted retirement forms are `{:session, sessionKey}` and
  `{:user, userId}`. Storage serializes them as `session:<sessionKey>` and
  `user:<userId>`. The wire router constructs the value from the accepted credential;
  Gateway does not reconstruct it from `origin`.
- **Empty epoch**: the close transaction that changes the child's open-assignment count
  from one to zero. Its identity is the closing attest id. A later assignment supersedes
  that epoch; a later one-to-zero transition creates a different completion record.
- **Reissue deadline**: a finite retry time copied from
  `:escalation_decision_deadline_ms` (default 86,400,000 ms). It bounds when Tightbeam
  repeats an open action-needed notice. It does not decide that a recipient failed.
- **Retain**: acknowledge the request and leave the session and harness lifecycle
  unchanged.
- **Retained root**: the terminal `status='retained_root'`, `decision='retain'` outcome
  created only by an explicit authorized retain on a root Main holder. It leaves Main's
  session and harness lifecycle unchanged.
- **Park**: acknowledge only after the separately specified park primitive records its
  successful durable outcome. Park preserves the session for later relaunch.
- **Retire**: acknowledge in the same database transaction that commits the existing
  session-retire state transition. Existing cascade, interruption, wire removal, and
  post-commit reaping behavior remains authoritative
  (`gateway.ex:5022-5103,5174-5289`; `org.ex:517-625`).
- **Typed wake cancellation**: a call to `Wakes.cancel_in_txn/2` whose closed requester,
  reason, durable source, and outcome fields produce one cancellation row. This rail does
  not update a pending wake directly. Reissue, supersession, acknowledgment, retirement,
  and stale-delivery refusal each name their exact cause and process principal through
  this seam (`wakes.ex:290-352,478-516`).

## Assumptions

1. The database owner serializes each mutation transaction.
2. A completion attest can close one open assignment exactly once. Losing terminal
   races roll back the attest (`attest-v1.md:181-196,272-280`).
3. Session rows persist after retirement, and `spawnedBy` preserves incarnation
   lineage (`org.ex:65-90,505-565`).
4. Each non-Main child and each lineage ancestor has the same `ownerUserId`. A corrupt
   cross-owner lineage is dirt; the resolver reports it and falls back to the child's
   owner Main instead of disclosing across owners.
5. The owner's built-in Main is permanent under the current retire rail
   (`gateway.ex:5042-5052`). A missing Main row is nevertheless handled as an
   undeliverable fallback record, not fabricated as a session.
6. `Wakes.schedule_in_txn/2` can arm a prompt or internal deadline wake inside the
   assignment-close transaction (`wakes.ex:104-200`).
7. Prompt wake delivery uses the existing projection and turn pipeline. Aware and
   unaware clients can both read the ordinary message payload
   (`wire/payloads.ex:110-139`).
8. `wi_6937890c-6ba6-48b7-a9d2-4eb4510fe245` will define a safe, authorized park
   operation and its durable success result. This spec does not assume its function or
   wire name.
9. Successful device authentication returns a device row with a non-empty `user_id`.
   The existing stream ownership check admits only a target session owned by that user
   (`wire/router.ex:235-252,433-443`).

## Invariants

### R1 — One durable record per completion

For each assignment completion committed after `CompletionEscalation.ensure_schema/1`
has succeeded, exactly one `completion_escalations` row exists. The assignment has
`outcome='completed'` and a non-null `closingAttestId`. The completion row's
`dedupeKey` is `completion:<closingAttestId>`. A unique constraint on
`closingAttestId` and a unique constraint on `assignmentId` make a second record
unrepresentable. A partial unique index on `childSessionKey` where `status='open'`
makes two live disposition requests for one child unrepresentable. Historical
`notice-only`, `acknowledged`, `retained_root`, and `superseded` rows can coexist.

For each wake id stored in `currentNoticeWakeId` or `deadlineWakeId`, exactly one
`completion_escalation_wakes` membership row exists with the same completion id and
generation. No other completion can claim that wake id. Historical membership rows stay
after the completion advances or terminalizes.

### R2 — Atomic close, record, and first notice

When R5 resolves an existing recipient, the completion attest insert, guarded
assignment close, completion-record insert, first notification wake insert, and notice
membership insert commit in one database transaction or all roll back. An open request's
deadline wake and membership also commit in that transaction. When R5 returns
`main-unavailable`, that same transaction commits the completion record and named
lifecycle failure with no notification wake. No post-commit callback creates the
initial notice or repairs the named failure. This follows the transactional outbox
pattern already required for decision notifications
(`escalation-delivery-v1.md:33-48,93-131`).

### R3 — Cause and principal are explicit

The record stores `closingAttestId`, `assignmentId`, nullable `workItemId`,
`childSessionKey`, literal outcome `completed`, `causeBySession`, `ownerUserId`,
`rootMainHolder`, `immediateParentSessionKey`, `remainingOpenAssignments`, and the
initial routing fields. The notification origin is
`process:tightbeam`; the cause principal is `session:<causeBySession>`. No domain field
derives a principal from prose or an untyped origin string.

Each successful generic retirement carries one typed caller principal into the shared
retirement transaction. The device `DELETE /api/streams/:key` route constructs
`{:user, device.user_id}` from the authenticated device row. An agent call carries its
authenticated `{:session, sessionKey}` or explicit authenticated `{:user, userId}`.
Gateway derives the target-owner match from this typed principal and serializes it as
`session:<sessionKey>` or `user:<userId>` before it calls the completion retirement seam,
assignment interruption, or `Org.retire_in_txn/4`. It does not derive either the owner or
the acting principal from `call.origin`. A call without one admitted typed form returns
the existing generic-retire `not_found` result before idempotency or lifecycle mutation.

### R4 — Session emptiness is checked in the close transaction

After the guarded close update, the producer runs:

```sql
SELECT count(*) FROM assignments
WHERE holderKey = ?1 AND state = 'open'
```

If the result is nonzero, the row has `status='notice-only'`. If the result is zero,
the row has `status='open'`, a non-null `actionDeadlineAt`, and a non-null internal
`deadlineWakeId`. The internal deadline wake uses
`sessionKey=childSessionKey`, `consumer='completion_disposition_deadline'`,
`origin='process:tightbeam'`, `dueAt=actionDeadlineAt`, the deterministic id from R8,
null `assignmentId`, and null `work_item_id`. Its required `sessionKey` is storage
correlation; the internal consumer does not deliver a turn to the child. The count is
per child session, not per work item. The producer stores that historical result as
`remainingOpenAssignments`; later assignment changes do not rewrite it.

### R5 — Routing uses lineage facts, then Main fallback

The close transaction records the immediate parent, walks `spawnedBy`, and selects the
first active same-owner ancestor. It records `resolutionKind='lineage'` and the rung.
If none exists, it selects the existing active owner Main and records
`resolutionKind='main-fallback'` and null rung. If no active owner Main row exists,
whether the row is absent or inactive, it records `resolutionKind='main-unavailable'`
and writes a lifecycle event. An empty-slate row remains an open action request whose
deadline can retry routing. A row with work remaining stays `notice-only` and queryable
as a named undeliverable completion. The producer never inserts a wake or turn for a
fabricated or inactive session key.

The producer does not call `Roles.resolve/2`. Role fallback is office routing and would
erase the distinction between a causal parent and Main fallback
(`roles.ex:139-156`).

For a root Main holder, the producer takes the root branch before it walks `spawnedBy`.
The active owner Main selected by this rule is the child itself. The row records
`initialResolutionKind='main-fallback'`,
`currentResolutionKind='main-fallback'`, null lineage rungs, and the exact child key as
both recipient keys. R2 and R4 create the same notice and open request used for another
empty child; the producer does not retain it automatically.

### R6 — Work-item parentage is immutable here

The producer reads `assignments.workItemId` for correlation. It does not write any
`work_items` field, creation-context field, assignment reference, or `Toplines` edge.
Main is a delivery fallback only.

### R7 — Notice delivery uses the ordinary durable wake path

When R5 resolves a recipient, the initial notice wake has:

- `wakeId = completion:<closingAttestId>:notice:0`;
- `consumer='prompt'`;
- `origin='process:tightbeam'`;
- `dueAt=now`;
- `sessionKey=currentRecipientSessionKey`;
- `targetGate=1`;
- `reresolve='lineage'`, `reresolveSeed=childSessionKey`, and the recorded active rung
  when `resolutionKind='lineage'`;
- `reresolve='lineage'`, `reresolveSeed=childSessionKey`, and `reresolveRung=1` when
  `resolutionKind='main-fallback'`; this gate is used only if the planned Main becomes
  ineligible before delivery;
- null `assignmentId` deliberately;
- null `work_item_id` deliberately.

The completion row, not `wakes.assignmentId`, carries assignment correlation. Current
code treats each process-origin prompt wake with an `assignmentId` as supervision-owned
and can suppress it when `work-blocked` stands (`wakes.ex:1210-1285`). Leaving that
carrier null prevents this completion notice from being misclassified. Leaving
`work_item_id` null prevents the generic wake-cancellation projection from treating a
session-lifecycle request as work-item liveness. The exact prompt below still carries
the assignment and work-item ids. The completion row supplies both typed joins through
`currentNoticeWakeId`.

For a notice wake joined through `completion_escalation_wakes`,
`Gateway.deliver_prompt_in_txn/5` calls the completion producer before generic target
resolution. The producer locks the decision to current rows inside that delivery
transaction. It admits a message and turn only when the wake row still has
`state='pending'`, the completion row still has
`currentNoticeWakeId=<delivering-wake-id>`, and the completion status is `open` or
`notice-only`. If one predicate fails, the transaction inserts no message or turn. If
the wake is still pending, the producer cancels it through R8's typed
`completion_delivery_ineligible` command before returning. The check and the delivery or
cancellation action are one database transaction. The ordinary scheduler can select a
pending row earlier; that snapshot grants no delivery authority
(`wakes.ex:1166-1204`; `gateway.ex:978-1135`).

The stored `ownerUserId` is the owner pin. If the recorded recipient is active and has
the pinned owner, the transaction uses it without another fallback lifecycle event. If
that recipient is absent, inactive, or foreign-owned, the transaction applies the wake's
lineage gate. The lineage walk stops at the first foreign-owner ancestor; it does not
return that ancestor or traverse through it. When the same-owner lineage is exhausted,
the transaction selects the existing active pinned-owner Main and records
`completion_escalation_fallback`. A foreign boundary also records
`completion_escalation_cross_owner_lineage`. If no active pinned-owner Main exists, the
transaction records `completion_escalation_undeliverable`, cancels the still-pending
current notice through the same typed `completion_delivery_ineligible` command, and
delivers no message or turn. That cancellation makes the R14 receipt `canceled`, not
`inconsistent`;
the scheduler's later fired update cannot match the canceled wake. The owner check,
fallback selection, and message/turn insert or typed wake cancellation are one database
transaction, so the checked target cannot change between selection and use
(`gateway.ex:1013-1057,1313-1353`; `wakes.ex:333-352`).

This completion-aware check handles a recipient that retires after close and before
delivery; it does not change the policy for non-completion wakes. The delivered turn's
`sessionKey` is the actual recipient. The completion record preserves its planned
resolution; act-time rerouting does not overwrite the initial or current routing facts.

### R8 — Stable request and retry dedupe

`dedupeKey` never changes. Each routing generation uses deterministic wake ids:

```text
completion:<closingAttestId>:notice:<generation>
completion:<closingAttestId>:deadline:<generation>
```

The completion row stores the current generation, current deadline wake id, and the
nullable current notice wake id from R5. Tightbeam extends the closed typed-cancellation
vocabulary only for this rail:

- requester `{kind='process', id='tightbeam:completion-escalation'}` can use reasons
  `completion_generation_replaced` and `completion_request_disposed`;
- requester `{kind='process', id='tightbeam:wake-scheduler'}` can use reason
  `completion_delivery_ineligible`;
- durable source kind `lifecycle_event` accepts only a lifecycle row whose subject
  joins the canceled wake through `completion_escalation_wakes`;
- for reason `completion_generation_replaced`, that lifecycle row has kind
  `completion_escalation_reissued`; for reason `completion_request_disposed`, it has
  kind `completion_escalation_superseded` or `completion_escalation_acknowledged`;
- source kind `scheduler_delivery` accepts only the canceled wake id itself for reason
  `completion_delivery_ineligible`;
- disposition kind `completion_transition` accepts only the same joined lifecycle row
  used as the command's durable source;
- `completion_generation_replaced` accepts `replacement` or `no_replacement`;
  `completion_request_disposed` accepts `disposition`; and
  `completion_delivery_ineligible` accepts `no_replacement` from source kind
  `scheduler_delivery`.

No other requester gains those reasons. This is the cause/principal rail for each wake
that this mechanism withdraws; a raw `UPDATE wakes SET state='canceled'` is outside the
design.

A reissue transaction CASes the current `deadlineWakeId`. It computes the next routing
generation and writes the `completion_escalation_reissued` lifecycle source. It then
arms the replacement deadline and, when routing resolves a recipient, the replacement
notice. While the old notice is still the row's current notice, the transaction cancels
that notice through `completion_generation_replaced`, pointing to the new notice or to
`no_replacement` for `main-unavailable`. It does not try to cancel an old notice that is
already fired or canceled. A `replacement` outcome is valid only when the replacement
wake membership names the same completion, the next generation, and kind `notice`.
The transaction then updates the completion row to the new generation and wake ids and
marks the source deadline fired through `Wakes.fire_internal_in_txn/4`. A refused
cancellation of a pending old notice or a refused deadline-fire CAS raises and rolls
back each replacement row, lifecycle row, completion-row change, and deadline
consumption.

A stale or replayed deadline writes and arms zero rows. Database serialization gives a
delivery-versus-reissue race two results: delivery commits first and the old wake is no
longer pending, or reissue cancels first and R7 refuses the old callback. No two notice
generations for one completion remain pending after commit. Each reissued notice uses the
R7 wake fields with its current generation and current resolution. `turns.wakeId UNIQUE`
prevents a duplicate turn for one notice generation (`ledger.ex:1-18,99-148`).

### R9 — Deadline reissues; it does not judge

When the internal deadline fires, the transaction re-reads the request, the child
session, the child open-assignment count, the recorded recipient, and the source wake.
The handler acts only when the source wake is still pending, still equals the row's
`deadlineWakeId`, and the row remains `status='open'`. A scheduler snapshot does not
bypass that check. A callback that fails one predicate writes and arms zero rows.

- child has one or more open assignments: set `status='superseded'`,
  `supersededReason='new-assignment'`, store the earliest open assignment ordered by
  `openedAt,id` as `supersededByAssignmentId`, store `supersededAt=now`, consume the
  deadline, and arm nothing;
- child is retired: set `status='superseded'`,
  `supersededReason='child-retired'`, store `supersededAt=now`, consume the deadline,
  and arm nothing;
- request remains open and child remains active and empty: re-resolve from current
  rows, reissue the same request, and arm the next deadline.

Each successful branch marks the source deadline fired through
`Wakes.fire_internal_in_txn/4` in the same transaction. A branch that moves the request
to `superseded` writes its typed lifecycle source and cancels any pending current notice
through `completion_request_disposed`. A refused cancellation or deadline-fire CAS
rolls back the request transition and deadline consumption.

Elapsed time never means the parent is incapable or that retire is correct. A retired
recipient is an observable event and re-resolution skips it. An active recipient is
re-notified, not silently climbed past because a timer elapsed.

### R10 — Assignment-open race supersedes in the opening transaction

Every successful `assign` and `dispatch` insert for a child session calls the one
`supersede_open_for_assignment_in_txn/3` seam after the assignment, effect, and file rows
exist and before the supervision transition. The seam changes an open completion request
for that child to `superseded/new-assignment`. It first writes the supersede lifecycle
source. It then cancels the deadline and any pending current notice through
`completion_request_disposed`, with disposition `completion_transition`, in that same
transaction. The row stores the new assignment id and transaction timestamp as
`supersededAt`. The lifecycle row records that id and its typed opener principal. A
refused cancellation raises and rolls back the assignment insert and the request
transition (`assignments.ex:918-1057`).

If a new assignment and a disposition race, database serialization permits one result:

- assignment wins: disposition returns `request_superseded` and enacts no disposition;
- retain wins: the later assignment commits through the existing open path;
- retire wins: the later assignment fails the existing active-holder interlock;
- park wins: the future park contract defines and enforces the assignment interlock.

### R11 — Explicit acknowledgment and authorization

`completion-disposition <completion-id> --decision retain|park|retire` accepts only a
session or user principal. Process and remedy principals are refused.

A session principal is authorized when it is active at action time, has the stored
owner pin, is not the child, and is the recorded current recipient, the actual
current-generation notice recipient joined through `currentNoticeWakeId`, or an active
ancestor above the child.
The actual-recipient clause lets an owner Main selected by R7 act without rewriting the
planned routing facts. A user principal is authorized only when it owns the child. An
admin from another owner can read the record under R15 but cannot choose a lifecycle
disposition.

One self-disposition exception exists. The exact active root Main holder passes the
session-principal check for its own completion row. Its explicit `retain` reaches R12.
Its `park` and `retire` calls reach the root refusal below. No other child session passes
authorization for its own request.

Before a call can commit acknowledgment, the handler performs authorization,
`status='open'`, child-active, and zero-open-count checks in that same transaction. It
stores exactly one of
`actedBySession` or `actedByUser`, plus `actedAt` and `decision`. A repeated identical
decision by the same principal returns the original terminal record. A session principal
must still be active and owner-pinned for this replay. A user principal must still own
the child. The replay does not enact the lifecycle action again. A retired session has no
read or replay exception.

The owner user and an admin can read a terminal row under R15. An owner-user replay
returns the original record only when `actedByUser` names that owner. If
`actedBySession=P`, an identical owner-user decision reaches step 5 and returns
`request_not_open` without changing the completion row, lifecycle rows, wakes, session,
harness, assignment, or work item.

The action handler uses this refusal precedence:

1. A decision outside `retain|park|retire` returns `invalid_decision`.
2. A missing completion id returns `unknown_completion`.
3. A process or remedy principal returns `principal_not_allowed`.
4. A principal outside the authorization rule above returns `not_authorized`; this
   check precedes request-state disclosure. An active, owner-pinned exact
   `actedBySession`, or the owner `actedByUser`, is authorized on an `acknowledged` or
   `retained_root` row only for the identical replay in step 5.
5. An identical terminal replay returns the original record. Another call on an
   `acknowledged` or `retained_root` row returns `request_not_open`; `notice-only`
   returns `action_not_required`; `superseded` returns `request_superseded`.
6. An open request whose child is not active returns `child_not_active` and records
   dirt, because R13 requires acknowledgment in the retire transaction.
7. An open request whose child has gained an assignment is atomically superseded with
   the earliest open assignment ordered by `openedAt,id` and its opener principal,
   stores `supersededAt=now`, then returns `request_superseded`.
8. An open root Main request with decision `park` or `retire` returns exactly:

   ```json
   {
     "code": "root_lifecycle_unsupported",
     "completionId": "cn_...",
     "requestStatus": "open",
     "decision": "park"
   }
   ```

   The `decision` value is the submitted `park` or `retire`. The handler leaves the
   completion row, deadline wake, current notice wake, session row, and harness state
   unchanged. It calls neither the park dependency nor the retire preflight and writes
   no completion lifecycle event.
9. If a pending generic-retire intent wake exists for the child or its active subtree,
   a disposition that reaches this step returns `retire_deferred` with the R12 response
   shape and enacts nothing. The handler identifies those wakes through the existing
   deterministic retire-intent id function. For each active owner-matched member of the
   child's target subtree, it enumerates that member and its owner-matched lineage
   ancestors as possible generic-retire roots, computes each `(root, member)` id, and
   checks those ids for a pending wake. It stops each lineage at a foreign-owner row. It
   does not parse prompt text or match an id prefix. The response stores no requested
   disposition and schedules no retry. If the intent wake terminalizes while the child
   stays active, the caller must issue a new `completion-disposition` call; that call
   re-evaluates current rows. If the intent retires the child, R13 closes the request in
   the retirement transaction.
10. An authorized park request reaches the dependency check in R12. Retain reaches its
   R12 action directly. Retire reaches the critical-lease preflight in R12.

### R12 — Decisions are actions, not substrate choices

- `retain`: for an ordinary child, commit `status='acknowledged'` and
  `decision='retain'`. For a root Main holder, commit `status='retained_root'` and
  `decision='retain'`. Both branches store the acting principal and `actedAt`, cancel the
  deadline and any pending current notice through `completion_request_disposed`, and
  mutate no session, harness, assignment, or work-item row. The transaction writes the
  acknowledgment lifecycle source before those cancellations. A refused cancellation
  rolls back the lifecycle row and terminal completion state. Before the root branch
  writes `retained_root`, it verifies `isBuiltIn=1` and the exact owner personal-session
  key in the same transaction. Only an explicit authorized call reaches either branch.
- `retire`: use the existing retire mutation seam. In the action transaction, the
  completion path first applies the current `isBuiltIn` permanence denial. R11 already
  gives the exact root Main its specific response; a non-root built-in dirt row receives
  the existing generic `denied` result and no lifecycle mutation. The current gateway
  then extracts one DB-only subtree/critical-lease preflight from
  `retire_cascade_in_txn/6`; the generic retire verb and completion disposition both call
  it (`gateway.ex:5042-5052,5174-5233`). If no target-subtree lease is active, the current
  parent-last cascade calls the same `retire_session_in_txn/6` path. Both entry points
  supply the typed caller principal required by R3. The shared retirement handler derives
  the owner and serialized acting principal from that value once, before the transaction,
  and passes the serialized principal through the cascade. That path calls the
  completion retirement seam before `Org.retire_in_txn/4`, because Org's current
  retirement transition cancels target-gated wakes after the session state update
  (`gateway.ex:5259-5270`; `org.ex:540-625`). The completion seam writes its
  acknowledgment lifecycle source, cancels its deadline and pending notice through
  `completion_request_disposed`, and stores `decision='retire'` before Org sees the
  remaining wakes. Request acknowledgment and session retirement therefore commit
  together. Existing post-commit broadcast, supervision notification, workspace archive,
  and adapter reap remain unchanged. If a lease is active, completion disposition leaves
  the completion request, its deadline, its current notice, and each session row
  unchanged; schedules no `w_retire_...` intent wake; writes
  `completion_escalation_retire_deferred`; and returns:

  ```json
  {
    "code": "retire_deferred",
    "completionId": "cn_...",
    "requestStatus": "open",
    "deferred": [{"sessionKey": "agent:... s_...", "until": 1786330000000, "reason": "..."}]
  }
  ```

  The `deferred` list uses the existing retire response order and fields. A later retry
  after the leases end can commit retirement and acknowledgment. The generic `retire`
  verb keeps its existing intent-wake behavior; this no-side-effect deferred response
  applies to `completion-disposition --decision retire` because that verb cannot
  acknowledge an action that did not happen.
- `park`: call only the interface ratified by
  `wi_6937890c-6ba6-48b7-a9d2-4eb4510fe245`. Acknowledgment commits only after that
  primitive's durable success condition. A park-operation failure leaves the request open
  and records the failure. No placeholder park implementation is permitted.

No scheduler, sweep, notification terminal, or fallback path writes a disposition.
No path writes `retained_root` except the explicit retain branch above.

### R13 — Retirement race closes the request truthfully

The existing retire transaction calls the completion seam for each retiring session.
If an open empty-slate request exists, explicit retirement acknowledges it as
`decision='retire'` with the retire call's typed principal. It writes the acknowledgment
lifecycle source and cancels its deadline and any pending current notice through
`completion_request_disposed` before the session state transition. These actions share
the retirement transaction. A refused typed cancellation rolls back retirement.
The device generic-retire path records `actedByUser=device.user_id`; an agent
generic-retire path records `actedBySession=sessionKey`. The transaction passes the same
serialized principal to assignment interruption, the completion seam, and Org retirement.
It never parses the presentation origin to recover that principal.
If the generic retire verb defers on a critical lease, no session retirement occurred,
so the request remains open and its existing deadline continues. The generic retire
response and intent wake remain governed by the existing retire contract. R11 prevents
a conflicting completion disposition while that intent wake remains pending.
If retirement wins before completion, the assignment becomes revoked and the later
completion loses with `assignment_closed`; no completion record appears. If completion
wins first, the same retire transaction acknowledges the record. No request remains
open for a retired child.

### R14 — Receipt and action acknowledgment remain distinct

The read projection derives `receipt` from the wake and optional turn whose wake id is
the record's `currentNoticeWakeId`. It maps rows without inference:

- null `currentNoticeWakeId` -> `state='not-created'`, `turnSeq=null`;
- pending wake and no turn -> `state='pending'`, `turnSeq=null`;
- canceled wake and no turn -> `state='canceled'`, `turnSeq=null`;
- existing turn -> its exact `queued|running|delivered|canceled|failed|failed_unknown`
  status and sequence;
- fired wake and no turn -> `state='inconsistent'`, `turnSeq=null`.

The fired wake row and absent joined turn are the durable evidence for `inconsistent`.
The read path writes no lifecycle event. Repeated reads return the same projection
without mutating `lifecycle_events`.

Earlier generations remain available through their wake/turn rows and lifecycle trace;
they do not overwrite current-generation receipt.

Receipt does not close an action-needed request. Only R11-R13 do. Conversely, an
authorized action can acknowledge before its notice turn delivers; the pending notice
is canceled through R8's typed seam in the action transaction because its content is
then stale. The joined wake-cancellation row exposes the exact requester, reason, source,
outcome, cause principal, and cancellation time; the receipt state stays a mechanical
projection of wake and turn rows.

### R15 — Observability is durable and replayable

The completion row and joined assignment, attest, session, wake, and turn rows are the
source of truth. The producer writes these exact lifecycle kinds with
`subject=<completion-id>`:

- `completion_escalation_opened` in the close transaction;
- `completion_escalation_reissued` for each successful generation CAS;
- `completion_escalation_superseded` for each transition to `superseded`;
- `completion_escalation_acknowledged` for each first transition to `acknowledged` or
  `retained_root`;
- `completion_escalation_fallback` when routing selects Main;
- `completion_escalation_undeliverable` for each `main-unavailable` generation and each
  R7 act-time route with no pinned-owner Main;
- `completion_escalation_cross_owner_lineage` when R5 or R7 rejects a foreign ancestor;
- `completion_escalation_state_inconsistent` for R11's inactive-child dirt;
- `completion_escalation_retire_deferred` when R12 observes an active critical lease;
- `completion_escalation_park_failed` when the external park operation does not commit.

For the completion ids selected into a `work-item-trace`, JobTrace joins
`completion_escalation_wakes` to `wakes`, turns, and wake cancellations. It emits those
wakes through the existing `wake_scheduled`, `wake_fired`, and `wake_canceled` entry
shapes and ranks. This explicit membership join is required because completion wakes
deliberately carry null direct work and assignment fields. A current or historical
completion cancellation names one of R8's three completion reasons and the exact
lifecycle or scheduler source that authorized it. The trace does not infer a
cancellation cause from the completion status.

The lifecycle `detail` is exactly:

- opened: null;
- reissued: `generation=<decimal> principal=process:tightbeam:completion-escalation`;
- superseded by assignment: `reason=new-assignment`;
- superseded by retired child:
  `reason=child-retired principal=process:tightbeam:completion-escalation`;
- ordinary acknowledged: `decision=<retain|park|retire>`;
- retained root: `decision=retain outcome=retained_root`;
- fallback:
  `resolution=main-fallback generation=<decimal> principal=process:tightbeam:completion-escalation`;
- undeliverable:
  `resolution=main-unavailable generation=<decimal> principal=process:tightbeam:completion-escalation`;
- cross-owner lineage:
  `foreignSessionKey=<session-key> principal=process:tightbeam:completion-escalation`;
- state inconsistent:
  `reason=child-not-active principal=<session:session-key|user:user-id>`;
- retire deferred:
  `reason=critical-lease principal=<session:session-key|user:user-id>`;
- park failed:
  `reason=<park_dependency_unavailable|park_operation_failed> principal=<session:session-key|user:user-id>`.

Observability joins the event subject back to typed rows to project closing attest,
child session, cause principal, acting principal, decision, and reason. No decision path
parses prompt or event prose. A `new-assignment` supersede joins
`supersededByAssignmentId` to its typed opener principal.

Every lifecycle marker therefore carries cause and principal without guessing. Opened
joins the closing attest and its holder principal. Reissued joins the prior deadline
wake and names the completion process. Assignment supersession joins the new assignment
and its typed opener. Acknowledgment joins the terminal completion row and its exactly
one acting principal. The remaining process markers name the completion process in
their exact detail. The three refused-action markers copy the already-authorized typed
caller into their exact detail at write time. Detail remains observability only; no
authorization, routing, transition, or read-visibility decision parses it.

`completion-notices --status open|all [--session <child>]` returns records visible to
the owner user, an admin, the child, the active owner-pinned recorded recipient, the
active owner-pinned actual current-generation notice recipient, and active sessions in
its owner-matched lineage.
An `acknowledged` or `retained_root` row remains visible to an exact `actedBySession` only
while that same session incarnation is active and owner-pinned. Retirement removes that
session's read and replay authority. The owner user and an admin retain their ordinary
read authority. A role, a replacement incarnation, or a sibling gains no visibility from
`actedBySession`. `--status open` selects only `status='open'`; `all` selects each status.
Except for the explicit admin rule, the query exposes no row whose `ownerUserId` differs
from the caller's owner.

`JobTrace` adds `type='completion_escalation'` at rank 8 and
`type='completion_escalation_event'` at rank 9, then moves `turn_end` from rank 8 to rank
10. Every other rank stays unchanged.
It queries `completion_escalations` directly by `workItemId` or by the trace's assignment
ids; it does not add a `CausalEvents` kind. One completion row projects its opened entry
and at most one terminal entry:

- opened: `id=<completion-id>:opened`, `at=createdAt`, `phase='opened'`;
- superseded: `id=<completion-id>:superseded`, `at=supersededAt`,
  `phase='superseded'`, when status is `superseded`;
- acknowledged: `id=<completion-id>:acknowledged`, `at=actedAt`,
  `phase='acknowledged'`, when status is `acknowledged`.
- retained root: `id=<completion-id>:retained_root`, `at=actedAt`,
  `phase='retained_root'`, when status is `retained_root`.

Each entry contains `completionId`, `assignmentId`, nullable `workItemId`,
`closingAttestId`, `childSessionKey`, `causePrincipal`, `currentStatus`, nullable
`decision`, nullable `actingPrincipal`, nullable `supersededReason`, and nullable
`supersededByAssignmentId`. `actingPrincipal` is exactly
`session:<actedBySession>`, `user:<actedByUser>`, or null. Existing JobTrace type order
remains unchanged relative to every existing type.

For the completion ids in that typed result, JobTrace also selects lifecycle rows whose
kind is one of the exact kinds above. It emits
`id=le:<lifecycle-events.id>`, `at=<lifecycle-events.ts>`,
`type='completion_escalation_event'`, `completionId=<subject>`, `kind`, and the exact
opaque `detail`. JobTrace exposes `detail`; it does not parse it.

The rank map remains closed. `Map.fetch!/2` continues to raise for an unranked type. The
two new ranks preserve the relative order of each existing type
(`job_trace.ex:15-53`).

### R16 — Wire compatibility and exact payload

No socket frame type changes. The notification is an ordinary stored `message` with
`role='user'`, `sender='process:tightbeam'`, and the existing
`[from process:tightbeam]` provenance stamp. Existing clients render readable text and
aware clients retain the same sender anti-forgery rule (`wire/payloads.ex:10-31,110-139`).

The unstamped prompt body is exactly:

```text
Child completion recorded.
completionId=<completion-id>
assignmentId=<assignment-id>
workItemId=<work-item-id-or-none>
childSessionKey=<session-incarnation-key>
closingAttestId=<attest-id>
outcome=completed
causePrincipal=session:<child-session-key>
immediateParentSessionKey=<session-key-or-none>
recipientResolution=<lineage:rung-N|main-fallback>
remainingOpenAssignments=<decimal-count>
actionNeeded=<true|false>
```

When `actionNeeded=false`, the prompt ends after that line. For an ordinary non-root
child with `actionNeeded=true`, it appends exactly this final line:

```text
Choose retain, park, or retire with `tightbeam completion-disposition <completion-id> --decision <retain|park|retire>`. Tightbeam will not choose or auto-retire.
```

For a root Main holder with `actionNeeded=true`, it appends this retain-only final line
instead:

```text
Choose retain with `tightbeam completion-disposition <completion-id> --decision retain`. Tightbeam will not choose or auto-retain.
```

An explicit root `park` or `retire` call still returns R11's
`root_lifecycle_unsupported` response without invoking a lifecycle primitive.

The read/command JSON object uses camelCase:

```json
{
  "id": "cn_...",
  "dedupeKey": "completion:att_...",
  "assignmentId": "asg_...",
  "workItemId": "wi_...",
  "childSessionKey": "agent:... s_...",
  "rootMainHolder": false,
  "closingAttestId": "att_...",
  "outcome": "completed",
  "remainingOpenAssignments": 0,
  "cause": {"bySession": "agent:... s_...", "principal": "session:agent:... s_..."},
  "parent": {
    "immediateSessionKey": "agent:... s_...",
    "initialRecipientSessionKey": "agent:... s_...",
    "initialResolution": "lineage",
    "initialLineageRung": 1,
    "currentRecipientSessionKey": "agent:... s_...",
    "currentResolution": "lineage",
    "currentLineageRung": 1,
    "actualNoticeSessionKey": null
  },
  "receipt": {"state": "pending", "turnSeq": null},
  "request": {
    "status": "open",
    "decision": null,
    "deadlineAt": 1786330000000,
    "generation": 0,
    "actedBySession": null,
    "actedByUser": null,
    "actedAt": null,
    "supersededReason": null,
    "supersededByAssignmentId": null,
    "supersededAt": null
  },
  "createdAt": 1786240000000
}
```

`actualNoticeSessionKey` is the `sessionKey` of the turn joined through
`currentNoticeWakeId`; it is null until that turn exists. This keeps the stored planned
recipient distinct from the act-time recipient after gateway re-resolution. For
the prompt, `recipientResolution` is the schedule-time planned resolution for that wake
generation; only `actualNoticeSessionKey` reports an act-time reroute. For
`notice-only`, `request.status` is `notice-only` and its deadline/action fields are
null. For a retained root, `request.status` is `retained_root`, `decision` is `retain`,
`rootMainHolder` is true, and the acting fields name the explicit caller. For an
ordinary child, `rootMainHolder` is false. For missing `workItemId` or parent fields,
JSON uses null; prompt text uses `none`. No key is conditionally omitted.

### R17 — Compatibility and migration

`completion_escalations` is a new table created by its own `ensure_schema/1`; the schema
composition registers it after `Assignments`. Existing stamped databases create the
table additively. No existing table is altered, rebuilt, sniffed, or repaired. No schema
shape bump is required because the new build creates the table without reinterpreting
an existing column (`schema.ex:7-37,622-646`).

The release backfills no rows and arms no notices for historical completions. The first
post-release completion is the first eligible cause. Before that first row, rollback
leaves an empty unused table and no new-consumer wake. After the first row exists,
downgrade to a build that does not register `completion_disposition_deadline` is
unsupported: current `Wakes` cancels an unknown internal consumer as
`consumer_unavailable` (`wakes.ex:1181-1198,1306-1332`). Register the new internal
consumer beside `effort_probe` and `effort_deadline` in the gateway child specification,
not in `Wakes` (`gateway.ex:292-300`). This spec makes no post-use downgrade preservation
claim.

The gateway and Rust CLI add `completion-notices` and `completion-disposition`. Because
the package is pre-1.0 and currently requires exact CLI/gateway versions, the release
bumps both together (`cli_compatibility.ex:1-38`). Old Clawline clients remain compatible
because the wire frame is unchanged.

### R18 — One mutation seam

`Tightbeam.Productions.CompletionEscalation` is the only module that inserts or updates
`completion_escalations` or inserts `completion_escalation_wakes`. Assignment close/open
and retirement call its in-transaction functions. The deadline consumer and public verbs
delegate to it. A source-closure test fails if production SQL mutates either table
anywhere else.

`Wakes` remains the only owner of typed cancellation validation and cancellation rows.
`EventLog` remains the only owner of lifecycle insertion. The completion producer calls
their in-transaction seams; it does not duplicate their SQL. `Gateway` remains the owner
of message/turn delivery and session-retire orchestration. These boundaries let the
completion producer choose no disposition while keeping its tables behind one mutation
seam.

The close path runs the producer inside the same transaction, so no committed completion
can lack its dependent record. When routing resolves, it also cannot lack its first
notice or notice membership. An open request cannot lack its deadline or deadline
membership. `main-unavailable` is the only no-notice result and carries its named
lifecycle marker. No recovery sweep is required for this edge. The ordinary wake
scheduler supplies crash recovery after commit.

## Architecture

### Record shape

`completion_escalations` contains:

```sql
CREATE TABLE completion_escalations (
  id                        TEXT PRIMARY KEY,
  dedupeKey                 TEXT NOT NULL UNIQUE,
  assignmentId              TEXT NOT NULL UNIQUE REFERENCES assignments(id),
  workItemId                TEXT NULL REFERENCES work_items(id),
  childSessionKey           TEXT NOT NULL REFERENCES sessions(sessionKey),
  remainingOpenAssignments INTEGER NOT NULL CHECK (remainingOpenAssignments >= 0),
  closingAttestId           TEXT NOT NULL UNIQUE REFERENCES attests(id),
  outcome                   TEXT NOT NULL CHECK (outcome = 'completed'),
  causeBySession            TEXT NOT NULL REFERENCES sessions(sessionKey),
  ownerUserId               TEXT NOT NULL REFERENCES users(userId),
  rootMainHolder            INTEGER NOT NULL CHECK (rootMainHolder IN (0,1)),
  immediateParentSessionKey TEXT NULL REFERENCES sessions(sessionKey),
  initialRecipientSessionKey TEXT NULL REFERENCES sessions(sessionKey),
  initialResolutionKind     TEXT NOT NULL CHECK (
    initialResolutionKind IN ('lineage','main-fallback','main-unavailable')
  ),
  initialLineageRung        INTEGER NULL CHECK (initialLineageRung IS NULL OR initialLineageRung >= 1),
  currentRecipientSessionKey TEXT NULL REFERENCES sessions(sessionKey),
  currentResolutionKind     TEXT NOT NULL CHECK (
    currentResolutionKind IN ('lineage','main-fallback','main-unavailable')
  ),
  currentLineageRung        INTEGER NULL CHECK (currentLineageRung IS NULL OR currentLineageRung >= 1),
  generation                INTEGER NOT NULL DEFAULT 0 CHECK (generation >= 0),
  currentNoticeWakeId       TEXT NULL UNIQUE REFERENCES wakes(wakeId),
  deadlineWakeId            TEXT NULL UNIQUE REFERENCES wakes(wakeId),
  actionDeadlineAt          INTEGER NULL,
  status                    TEXT NOT NULL CHECK (
    status IN ('notice-only','open','acknowledged','retained_root','superseded')
  ),
  decision                  TEXT NULL CHECK (decision IN ('retain','park','retire')),
  actedBySession            TEXT NULL REFERENCES sessions(sessionKey),
  actedByUser               TEXT NULL REFERENCES users(userId),
  actedAt                   INTEGER NULL,
  supersededReason          TEXT NULL CHECK (
    supersededReason IN ('new-assignment','child-retired')
  ),
  supersededByAssignmentId  TEXT NULL REFERENCES assignments(id),
  supersededAt              INTEGER NULL,
  createdAt                 INTEGER NOT NULL,
  CHECK (causeBySession = childSessionKey),
  CHECK (dedupeKey = 'completion:' || closingAttestId),
  CHECK (
    (initialResolutionKind = 'lineage' AND initialRecipientSessionKey IS NOT NULL AND initialLineageRung IS NOT NULL)
    OR
    (initialResolutionKind = 'main-fallback' AND initialRecipientSessionKey IS NOT NULL AND initialLineageRung IS NULL)
    OR
    (initialResolutionKind = 'main-unavailable' AND initialRecipientSessionKey IS NULL AND initialLineageRung IS NULL)
  ),
  CHECK (
    (currentResolutionKind = 'lineage' AND currentRecipientSessionKey IS NOT NULL AND currentLineageRung IS NOT NULL)
    OR
    (currentResolutionKind = 'main-fallback' AND currentRecipientSessionKey IS NOT NULL AND currentLineageRung IS NULL)
    OR
    (currentResolutionKind = 'main-unavailable' AND currentRecipientSessionKey IS NULL AND currentLineageRung IS NULL)
  ),
  CHECK (
    (currentResolutionKind = 'main-unavailable' AND currentNoticeWakeId IS NULL)
    OR
    (currentResolutionKind != 'main-unavailable' AND currentNoticeWakeId IS NOT NULL)
  ),
  CHECK (
    rootMainHolder = 0
    OR (
      initialResolutionKind = 'main-fallback'
      AND initialRecipientSessionKey = childSessionKey
      AND currentResolutionKind = 'main-fallback'
      AND currentRecipientSessionKey = childSessionKey
    )
  ),
  CHECK (
    status = 'notice-only'
      AND remainingOpenAssignments >= 1
      AND decision IS NULL AND actionDeadlineAt IS NULL AND deadlineWakeId IS NULL
      AND actedBySession IS NULL AND actedByUser IS NULL AND actedAt IS NULL
      AND supersededReason IS NULL AND supersededByAssignmentId IS NULL AND supersededAt IS NULL
    OR status = 'open'
      AND remainingOpenAssignments = 0
      AND decision IS NULL AND actionDeadlineAt IS NOT NULL AND deadlineWakeId IS NOT NULL
      AND actedBySession IS NULL AND actedByUser IS NULL AND actedAt IS NULL
      AND supersededReason IS NULL AND supersededByAssignmentId IS NULL AND supersededAt IS NULL
    OR status = 'acknowledged'
      AND rootMainHolder = 0
      AND remainingOpenAssignments = 0
      AND decision IS NOT NULL AND actionDeadlineAt IS NOT NULL AND deadlineWakeId IS NULL
      AND ((actedBySession IS NOT NULL) != (actedByUser IS NOT NULL)) AND actedAt IS NOT NULL
      AND supersededReason IS NULL AND supersededByAssignmentId IS NULL AND supersededAt IS NULL
    OR status = 'retained_root'
      AND rootMainHolder = 1
      AND remainingOpenAssignments = 0
      AND decision = 'retain' AND actionDeadlineAt IS NOT NULL AND deadlineWakeId IS NULL
      AND ((actedBySession IS NOT NULL) != (actedByUser IS NOT NULL)) AND actedAt IS NOT NULL
      AND supersededReason IS NULL AND supersededByAssignmentId IS NULL AND supersededAt IS NULL
    OR status = 'superseded'
      AND remainingOpenAssignments = 0
      AND decision IS NULL AND actionDeadlineAt IS NOT NULL AND deadlineWakeId IS NULL
      AND actedBySession IS NULL AND actedByUser IS NULL AND actedAt IS NULL AND supersededAt IS NOT NULL
      AND (
        (supersededReason = 'new-assignment' AND supersededByAssignmentId IS NOT NULL)
        OR
        (supersededReason = 'child-retired' AND supersededByAssignmentId IS NULL)
      )
  )
);
CREATE INDEX completion_escalations_child_status
  ON completion_escalations(childSessionKey, status);
CREATE UNIQUE INDEX completion_escalations_one_open_child
  ON completion_escalations(childSessionKey) WHERE status = 'open';

CREATE TABLE completion_escalation_wakes (
  wakeId       TEXT PRIMARY KEY REFERENCES wakes(wakeId),
  completionId TEXT NOT NULL REFERENCES completion_escalations(id),
  generation   INTEGER NOT NULL CHECK (generation >= 0),
  kind         TEXT NOT NULL CHECK (kind IN ('notice','deadline')),
  UNIQUE (completionId, generation, kind)
);
CREATE INDEX completion_escalation_wakes_completion
  ON completion_escalation_wakes(completionId, generation, kind);
```

`rootMainHolder` is captured from the session row and
`Org.personal_session_key(ownerUserId)` in the close transaction. The DDL does not embed
the Main key format. The action seam rechecks both inputs before it writes
`retained_root`. This keeps topology in `Org.personal_session_key/1`, its existing single
home (`org.ex:1035-1042`). The DDL makes a root holder's initial and current recipient
the child itself through `main-fallback`; a root row cannot be represented as a lineage
request.

Each schedule operation inserts its wake row before its membership row in the same
transaction. A notice or deadline without membership rolls back the producer call. The
source-closure test treats both tables as one producer-owned state seam.

The implementation can strengthen the DDL with equivalent checks. It cannot weaken a
listed relation or add a state value without a spec amendment.

### Transaction order

Completion uses this total order in the existing assignment transaction:

1. Read and authorize the open assignment.
2. Insert the completion attest.
3. Guarded-update the assignment to `closed/completed` and verify one changed row.
4. Fetch the closed assignment.
5. Call `CompletionEscalation.open_in_txn/3` only for `kind='completion'`.
6. Arm the existing work-item slate bracket.
7. Derive the current disposition liveness trigger.
8. Commit the existing supervision terminal-disposition transition.
9. Cancel the effort check-in through its existing typed seam.
10. Append the existing completion and assignment markers.
11. Commit.

Steps 5-10 preserve the current 0.1.7 relative order of steps 6-10. The new producer
enters immediately after the guarded close so each later failure rolls back the
completion row and, when routing resolves, the first notice with the attest and
assignment close
(`assignments.ex:1130-1200`). A surrender follows the existing path without step 5.

The new producer cannot reject a truthful completion because delivery is unavailable.
If Main is absent, it commits `main-unavailable` and the lifecycle record. A database
write failure rolls back the entire terminal transition, as any failure inside the
existing atomic close does.

Assignment-open calls the supersede seam after it inserts assignment, effect, and file
rows and before it commits the supervision transition. Retirement calls the
acknowledgment seam before `Org.retire_in_txn/4` changes the session state and performs
typed target-wake cancellation. Before that transaction, Gateway resolves the owner and
serialized acting principal from `call.principal` under R3. These calls share the caller's
transaction.

### Deadline consumer

Register one internal wake consumer, `completion_disposition_deadline`, in the Gateway
child specification. Its handler calls `CompletionEscalation.reissue_in_txn/2`. The
current wake id is the CAS token. The handler marks the source deadline fired, updates or
closes the request, and arms replacement wakes in one transaction. It runs no model and
invokes no session lifecycle action.

### Typed cancellation integration

Add `EventLog.lifecycle_with_id_in_txn/4` as the lifecycle insert that returns its row
id; keep the existing `lifecycle_in_txn/4` return contract unchanged. The completion
producer serializes the positive integer id as base-10 text and uses it as the
`lifecycle_event` cause and `completion_transition` disposition id in R8 cancellation
commands. The validators match it with `CAST(lifecycle_events.id AS TEXT)`; they do not
parse lifecycle detail.

Extend `Wakes` with R8's three reason values, the two named process requesters, the
`lifecycle_event` source, and the `completion_transition` disposition. For
`completion_generation_replaced` and `completion_request_disposed`, the validator joins
the lifecycle subject to `completion_escalations`, proves that the canceled wake is that
row's current notice or deadline, and applies R8's reason-specific lifecycle kind. For a
`replacement` outcome, it also proves the replacement membership names the same
completion, the next generation, and kind `notice`. For
`completion_delivery_ineligible`, the validator requires a notice membership but does
not require the wake to remain current; this admits a delayed callback from a historical
generation. The existing `scheduler_delivery` source validator continues to require its
source id to equal the canceled wake id. A completion cancellation command that fails
one check returns `false`; each completion caller converts `false` to a transaction
failure. Existing cancellation reasons, requesters, and compatibility pairs stay
unchanged (`wakes.ex:290-352,478-516,599-606,651-789`).

Add `Wakes.fire_internal_in_txn/4` as the wake-owned CAS that changes one pending wake
with the expected internal consumer to `fired` and sets `firedAt`. It returns `true` only
when one row changes. The completion producer uses this seam for deadline consumption;
it never updates `wakes.state` directly.

### Exact implementation surfaces

- New: `lib/tightbeam/productions/completion_escalation.ex`.
- Register schema after `Assignments` in `lib/tightbeam/schema.ex`.
- Call close/open seams from `lib/tightbeam/assignments.ex`.
- Call retire acknowledgment from the canonical transaction in
  `lib/tightbeam/gateway.ex` before `Org.retire_in_txn/4`; preserve the existing
  post-commit retire completion path.
- Enforce R7 in gateway delivery for notice wakes joined through
  `completion_escalation_wakes`; leave non-completion wake rerouting outside this change.
- Register the internal deadline consumer in `lib/tightbeam/gateway.ex` composition.
- Extend typed cancellation in `lib/tightbeam/wakes.ex` and add the id-returning lifecycle
  insert in `lib/tightbeam/event_log.ex`.
- Add read/action handlers in `lib/tightbeam/gateway.ex` and typed routing in the router.
- Add `principal: {:user, device.user_id}` to the authenticated device DELETE call in
  `lib/tightbeam/wire/router.ex`. Make generic retirement in
  `lib/tightbeam/gateway.ex` require and consume R3's typed caller principal. Preserve
  `origin` only as presentation and existing event context.
- Add Rust CLI args/dispatch/help for the two commands.
- Add R15's completion, lifecycle, and membership-linked wake/cancellation projections
  to `JobTrace`; expose lifecycle detail as opaque text. Do not parse that detail, add a
  `CausalEvents` kind, or change work-item parent derivation.
- Add `test/completion_escalation_test.exs` and the source-closure assertion.

No source edit is authorized by this artifact. These are handoff surfaces for a later,
independently reviewed implementation assignment.

## Acceptance

Each acceptance case uses the real SQLite DB, real assignment handler, real wake store,
real gateway delivery transaction, and real turn ledger. A hand-written notification
object is not a fixture.

Traceability is two-way: R1→A1,A2,A4; R2→A2,A3; R3→A5,A14,A21; R4→A1,A2; R5→A5-A8,A23,A24;
R6→A7,A19; R7→A6,A8-A10,A17,A23; R8→A4,A10-A14,A17; R9→A8,A11; R10→A12;
R11→A14,A16,A24; R12→A13-A15,A24; R13→A14; R14→A10,A17,A18;
R15→A5,A12-A14,A18,A22-A24; R16→A2,A24; R17→A20; and R18→A21. Each acceptance
case points back to the named requirement or exact contract it verifies.

### A1 — Completion with work remaining

Given child `C` has two open assignments and active parent `P`, when `C` completes the
first assignment, then the handler commits the attest, closed assignment, one completion
row, one generation-0 prompt wake, and its notice membership in one transaction. The row
is `notice-only`, stores `remainingOpenAssignments=1`, repeats that value in the exact
prompt, and has no deadline wake or deadline membership.

### A2 — Empty epoch opens one action request

Given `C` has one open assignment and active same-owner parent `P`, when `C` completes
it, then the same transaction commits one `status='open'` completion row, one due prompt
wake, and one internal deadline wake whose `sessionKey`, consumer, origin, due time,
deterministic id, null `assignmentId`, and null `work_item_id` match R4. It commits one
notice and one deadline membership row for generation 0. The completion row stores
`remainingOpenAssignments=0`. The JSON projection matches R16, and the prompt matches
R16 byte-for-byte after substituting ids/timestamps.

### A3 — Rollback proves the outbox boundary

Given `C` has an active parent, run two fixtures in which a temporary SQLite trigger
aborts either the generation-0 completion notice insert or its membership insert. When
`C` files completion in either fixture, then the attest, assignment close, completion
row, notice wake, deadline wake, work-item slate wake, and both completion wake
memberships all roll back. The markers, current liveness trigger, supervision
transition, and effort cancellation also leave no committed row or state change. After
removing the trigger, one retry commits exactly one of each applicable row in the R2
transaction order.

### A4 — Replay and terminal race dedupe

Given two concurrent completion calls for one open assignment whose child has an active
same-owner parent, when both run, then one returns success and one returns
`assignment_closed`; one attest, one completion row, one generation-0 notice wake and
membership, and one generation-0 deadline wake and membership exist. No orphan attest,
completion row, wake, or membership row exists. A corruption fixture that tries to
insert a second `status='open'` row for the same child fails the partial unique index.

### A5 — Parent routing and recorded cause

Given `C.spawnedBy=P` and `P` is active, when `C` completes, then the record names `P` as
immediate parent and initial recipient, `resolutionKind='lineage'`, rung 1, the exact
closing attest, assignment, work item, outcome, child incarnation, cause session, and
owner. The stored message sender is `process:tightbeam`. The opened lifecycle event and
typed `work-item-trace` entry carry the same completion id, closing attest, child, cause
principal, and work item. The trace entry has `type='completion_escalation'`,
`phase='opened'`, `at=createdAt`, and the R15 id. The lifecycle row has
`kind='completion_escalation_opened'`, `subject=<completion-id>`, null detail, and a
paired `completion_escalation_event` trace entry.

### A6 — Dead parent is skipped from rows, not time

Given immediate parent `P1` is retired and same-owner ancestor `P2` is active, when `C`
completes, then initial routing selects `P2` at active rung 1. Given an initially active
immediate parent `P1` retires after the close but before wake delivery while same-owner
`P2` remains active, when the wake fires, then act-time re-resolution delivers to `P2`
at active rung 1; the record preserves `P1` as its initial and current planned recipient,
the turn names `P2` as actual recipient, and the R16 projection exposes both values
without overwriting one.

### A7 — Main fallback preserves work-item parentage

Given no active lineage ancestor and active owner Main `M`, when `C` completes, then one
notice targets `M`, the record says `main-fallback`, and the before/after values of
`work_items.createdInTurnSeq`, the creation turn's `jobRef`, the completing assignment's
`workItemId` and `reviewsAssignmentId`, and the `Toplines` parent projection are
identical. No assignment row is created or reparented; only the completing assignment's
specified terminal fields change under R1-R2. This fixture cross-links
`wi_3d6d13a0-c4cf-4370-88a1-b407c41ff7c1` and asserts that fallback is delivery only.

### A8 — Missing Main fails loudly without fabricating

Given corrupt fixture state has no active lineage ancestor and the owner Main row is
absent or inactive, when completion commits, then it records `main-unavailable`, writes
one `completion_escalation_undeliverable` event, inserts no prompt wake to an absent or
inactive Main key, and leaves an empty-slate request open and queryable with its internal
deadline armed and `receipt.state='not-created'`. Given
the child instead has another open assignment, the same fixture commits `notice-only`,
inserts no prompt or deadline wake, and remains queryable as the named undeliverable
completion. Each failure writes `completion_escalation_undeliverable`. Given owner Main
becomes
active before the open request's deadline, the deadline transaction routes generation 1
to Main and arms its replacement deadline. Given Main remains absent, the deadline
records another named failure, arms only the replacement deadline, and inserts no turn.
Given active Main `M` is the planned `main-fallback` recipient and becomes inactive
before delivery, when a same-owner ancestor is then active, the owner-pinned act-time
gate delivers to that ancestor and records it as actual recipient. Given no same-owner
ancestor is active, the same gate writes one undeliverable event, cancels the notice
wake, inserts no message or turn, and projects `receipt.state='canceled'`.

### A9 — Crash recovery

Given a file-backed DB commits completion plus due wakes while the scheduler is stopped,
when the DB and ordinary wake child restart, then the boot tick delivers the pending
notice without an operator command. The completion row remains one, the notice turn count
for its wake id becomes one, and the wake becomes fired only with the committed message
and turn.

### A10 — Delivery retry and exactly-once backstop

Given notice delivery raises before durable acceptance, when the scheduler ticks, then
the wake stays pending and no turn exists. After the dependency heals, a later tick
commits one message and turn. Given synthetic legacy residue leaves that wake pending
after the turn committed, when the scheduler retries, then `turns.wakeId` prevents a
second turn and the wake settles without duplicate parent content. Given the scheduler
selects a pending notice and another transaction makes that generation ineligible before
the delivery transaction starts, when the delayed callback runs, then R7 inserts no
message or turn. If the wake is still pending, the same transaction cancels it with
reason `completion_delivery_ineligible`, source kind `scheduler_delivery`, requester
`tightbeam:wake-scheduler`, and outcome `no_replacement`.

### A11 — Deadline is a reminder, not a verdict

Given an open empty-slate request whose active parent has not acted, when its deadline
fires, then generation increments once, the same active parent receives one reissued
notice, one replacement deadline is armed, and no decision or session lifecycle changes.
Given generation 0 remains pending without a turn because delivery failed, when its
deadline fires, then the same transaction arms generation 1 and its membership, records
them as the replacement outcome while it cancels generation 0, and commits with exactly
one pending notice generation. A replay of the old deadline id cancels nothing and arms
nothing. Given the scheduler selected generation 0 before that transaction, when its
delayed delivery callback starts afterward, the delivery transaction observes that
generation 0 is canceled and no longer current, and inserts no generation-0 message or
turn. If delivery commits first, generation 0 has one turn before generation 1 is armed.

### A12 — New assignment supersedes atomically

Given an open empty-slate request, when a new assignment to `C` commits, then that same
transaction marks the request `superseded/new-assignment`, cancels the deadline and any
pending current notice through typed `completion_request_disposed` cancellations, and
records the new assignment id, `supersededAt`, and typed opener principal. Each
cancellation points to the supersede lifecycle row through source kind `lifecycle_event`
and disposition kind `completion_transition`. If any attempted pending-wake cancellation
is refused, then the assignment insert, effect/files, supersede lifecycle row, request
transition, and all cancellation rows roll back.
A concurrent disposition loses with `request_superseded` if assignment-open commits
first. Given the scheduler selected the pending notice before assignment-open commits,
when its delayed delivery callback starts afterward, the delivery transaction observes
the superseded status and inserts no message or turn. If delivery commits first, its
turn precedes the supersede transaction. No pending notice or later deadline presents
the stale request.

### A13 — Retain

Given an open request and authorized parent `P`, when `P` chooses retain, then the request
becomes `acknowledged/retain`, records `actedBySession=P`, cancels pending notice/deadline
wakes through typed `completion_request_disposed` cancellations sourced from the
acknowledgment lifecycle row, and changes no session, harness, assignment, or work-item
row. Identical replay by `P` while `P` remains active and owner-pinned returns the same
record. A different choice is refused. If `P` retires first, the same session key cannot
read the terminal row or replay the decision.
Given any attempted pending-wake cancellation is refused, then no acknowledgment or
lifecycle row commits.

### A14 — Retire and race

Given an open request and authorized parent `P`, when `P` chooses retire, then request
acknowledgment and the existing retire database transition commit together. Existing
cascade/interruption, typed target-wake cancellation, wire removal, and post-commit reap
run once. The completion deadline and pending notice cancellations point to the
acknowledgment lifecycle source. Given any attempted completion-wake cancellation is
refused, the request, session, assignment, ordinary retirement wakes, and lifecycle rows
remain unchanged. Given retire and
completion race before the assignment closes, either completion wins and retire
acknowledges its request, or retire wins and completion returns `assignment_closed` with
no completion row. Given the target subtree has an active critical lease, when `P`
chooses retire through `completion-disposition`, then the response exactly matches R12,
the request remains `open`, no session or request field changes, no `w_retire_...` wake
is scheduled, and one `completion_escalation_retire_deferred` event exists. After the
lease ends, one retry commits the acknowledgment and retirement. Given an ordinary
non-root child's open request and the same active lease, when the generic `retire` verb
runs first, then its existing deferred response and intent wake remain while the
completion request stays open and unacknowledged. While that intent wake is pending,
retain, park, and retire disposition calls each return
`retire_deferred` and enact nothing. After the intent wake terminalizes with the child
still active, when the caller retries, the handler re-evaluates the requested
disposition from current rows. The deferred event has the exact R15 detail and appears as a
`completion_escalation_event` in `work-item-trace`.

Given an owner-matched ancestor `A` is the root of a deferred generic-retire cascade and
the open completion request belongs to descendant `C`, when the pending intent wake is
addressed to `C` or an active member of `C`'s subtree, then R11's deterministic
`(root, member)` enumeration finds it and refuses each completion disposition. The test
uses no prompt or wake-id-prefix match.

Given an authenticated device for owner `U` calls `DELETE /api/streams/:key` for ordinary
non-root child `C` owned by `U`, and `C` has an open completion request with no critical
lease, when generic retirement commits, then the router call contains
`principal={:user, U}`. The request becomes `acknowledged/retire` with `actedByUser=U` and
null `actedBySession`. Assignment interruption, the completion lifecycle row, wake
cancellations, and the Org retirement marker each name `user:U`. The fixture asserts that
changing only `origin` cannot change the owner match or any stored principal. Given the
same call lacks an admitted typed principal, it returns `not_found` and changes no
idempotency, completion, wake, assignment, session, or lifecycle row.

Given a corrupt non-root child row has `isBuiltIn=1`, when an authorized principal
chooses retire, then the shared current permanence preflight returns the existing
generic `denied` result before the critical-lease or retire mutation. The completion
request, session, wakes, assignments, and lifecycle rows remain unchanged.

### A15 — Park dependency gate

Given the park primitive from `wi_6937890c-6ba6-48b7-a9d2-4eb4510fe245` is absent or has
not received its required reviewed-clean contract, when a caller chooses park, then the
gateway returns `park_dependency_unavailable`, leaves the request open, and records the
attempt as `completion_escalation_park_failed`. The feature release gate remains red.
Given that primitive later lands with a reviewed contract, when the real park
success/failure fixture runs, then success acknowledges only after its durable success
row and park-operation failure leaves the request open.

### A16 — Authorization matrix

Given one completion request, when each listed principal separately calls
`completion-disposition`, then the recorded current recipient, the actual
current-generation recipient, another active same-owner ancestor, and the owner user can
act while each session principal is active and owner-pinned. The initial Main-fallback
fixture and the R7 act-time Main-fallback fixture prove that Main can read and act without
rewriting the planned recipient. An ordinary child acting on its own row, a sibling, an
admin user from another owner, a
different-owner session/user, a process principal, a remedy principal, and each retired
session principal are refused without
changing the request. Each refusal code and the R11 precedence is asserted. The read
matrix separately calls `completion-notices` and proves that the owner user, an admin,
the child, both typed recipient forms, and owner-matched lineage can read the row while a sibling and every non-admin
different-owner principal receive no row. Given `P` acknowledges retain and later
retires, the exact retired session key `P` cannot read that acknowledged row or replay
the identical retain decision. The owner user and an admin can still read it. The owner
user's identical retain returns `request_not_open` because `actedBySession=P`; it
changes no completion row, lifecycle row, wake, session, harness, assignment, or work
item. A separate terminal fixture with `actedByUser=ownerUserId` proves that the same
owner-user principal can replay its identical decision. A replacement incarnation with
the same role and each sibling cannot read or replay either row.

### A17 — Receipt differs from action

Given a notice turn delivers, then the read projection says `receipt=delivered` while the
request remains open. Given an authorized action commits before notice delivery, then the
action transaction cancels the stale pending notice and the request is acknowledged.
Given the scheduler selected that notice before acknowledgment commits, when its delayed
delivery callback starts afterward, the delivery transaction observes the acknowledged
status and inserts no message or turn. If delivery commits first, its turn precedes the
acknowledgment transaction. No test treats a delivered turn as a retain decision.

### A18 — Notice-only completion remains visible

Given A1 and a notice terminal of delivered, failed, canceled, or `failed_unknown`, when
`completion-notices --status all` runs, then it returns the completion with that exact receipt state.
Queued, running, pending-without-turn, and canceled-without-turn fixtures map exactly as
R14 requires. A fired-without-turn dirt fixture returns `inconsistent`; two consecutive
reads leave the lifecycle row count unchanged. No deadline or action request is created.
Existing fault bubbling can independently recognize a failed notice turn; this rail does
not duplicate it.

### A19 — Existing bracket coexistence

Given one completion empties both child `C` and work item `W`, when the close commits,
then the completion notice/request and the work-item slate wake both exist. The first is
session lifecycle addressed to a parent; the second is intent disposition addressed to
the user owner. Each completion wake carries null `work_item_id` and null
`assignmentId`; the completion row holds its correlations. A later assignment supersedes
the completion request through R10 and cancels the work-item slate wake through its
existing bracket seam. Neither cancellation is authorized by the other mechanism's row.

### A20 — Compatibility and additive schema

Given a current stamped database with no `completion_escalations` table, when the new
build boots, then it creates the table without altering existing tables or arming
historical notices. Given no completion row has been recorded, then rollback leaves no
pending new-consumer wake. Given a completion row exists, then the compatibility matrix
marks downgrade to a gateway without `completion_disposition_deadline` unsupported; no
test claims that old gateway preserves or ignores the pending deadline. Current ordinary
message/prompt-turn payload goldens remain byte-identical.

### A21 — Closure law

Given the release-candidate source tree, when the AST/source closure test runs, then it
proves that only
`Tightbeam.Productions.CompletionEscalation` mutates `completion_escalations` and
`completion_escalation_wakes`; every assignment completion path calls its in-transaction
open seam; every assignment-open path calls its supersede seam; retirement calls its
retire acknowledgment seam; and no completion-table mutation occurs in a post-commit
callback. The same test proves that only the explicit authorized retain
branch writes `status='retained_root'`; that branch tests both `isBuiltIn=1` and the
exact owner personal-session key; and a root `park` or `retire` refusal calls neither
the park nor the retire lifecycle primitive. It also proves that each completion wake
cancellation calls `Wakes.cancel_in_txn/2` with one R8 reason; no completion producer
code updates `wakes.state` directly; each deadline consumption calls
`Wakes.fire_internal_in_txn/4`; the internal consumer is registered in Gateway; and each
completion lifecycle insert uses `EventLog`. The test also proves that authenticated
device DELETE constructs `principal={:user, device.user_id}`; generic retirement derives
its owner and serialized principal from `call.principal`; each successful retirement
passes that serialized principal through assignment interruption, completion
acknowledgment, and Org retirement; and none of those paths derives a principal from
`call.origin`.

### A22 — Real smoke

Given one real gateway with two real agent sessions in a parent/child lineage, when a
real assignment is dispatched, the child files completion, and the parent retains, then
the smoke captures the actual stored message, turn, wake, completion row, CLI read
response, visibility results for the R15 matrix, typed opened and acknowledged
`work-item-trace` entries, and retain acknowledgment response. It also captures the
opened and acknowledged lifecycle rows, their
`completion_escalation_event` trace entries, and the membership-linked
`wake_canceled` entries for the retained request's notice and deadline. Compare those
outputs to R15-R16 after replacing only generated ids/timestamps. Passing unit tests
without this smoke does not satisfy the rail.

### A23 — Cross-owner lineage fails closed

Given corrupt fixture state points `C.spawnedBy` at an active session owned by another
user while the child's owner Main `M` is active, when `C` completes, then the resolver
writes one `completion_escalation_cross_owner_lineage` event, sends no wake or readable
row to the foreign
session or user, routes the completion to `M` as `main-fallback`, and preserves the
foreign `spawnedBy` fact for diagnosis. Given `M` is also absent or inactive, the result
is the R5 `main-unavailable` named failure rather than cross-owner disclosure.

Given same-owner `P1` is the planned recipient, foreign-owner `P2` is its ancestor, and
`P1` retires before delivery, when the notice wake fires, then the delivery transaction
does not deliver to or traverse through `P2`. It writes the exact R15 cross-owner event
and fallback event, and delivers to active pinned-owner Main `M`; the turn names `M` as
actual recipient and the completion row preserves `P1` as planned recipient. If `M` is
absent, it writes the exact R15 undeliverable event and inserts no message or turn for
`P2` or a fabricated Main key. The current notice wake becomes `canceled`, the R14
receipt is `canceled`, and repeated reads add no lifecycle event.

### A24 — Root Main retains explicitly

Given exact built-in Main `M` holds one open assignment and the scheduler is stopped,
when `M` completes that assignment, then the close transaction creates the normal
`status='open'` row with `remainingOpenAssignments=0`, addresses the generation-0 notice
to `M` as `main-fallback`, and arms the deadline. Before delivery,
`completion-notices --status open` called as `M` returns that row with
`receipt.state='pending'`, null acting fields, and null decision. The session and harness
remain active; no automatic retain occurs. The stored notice uses R16's exact root
retain-only action line and does not advertise park or retire.

Given that open root request, when exact `M` calls
`completion-disposition --decision retain`, then the transaction commits
`status='retained_root'`, `decision='retain'`,
`actedBySession=M`, and `actedAt`; cancels the pending notice and deadline; and changes no
session, harness, assignment, or work-item row. It writes one
`completion_escalation_acknowledged` event with
`detail='decision=retain outcome=retained_root'`. When exact `M` repeats the same retain,
the command returns the original record and the completion row, wakes, session, harness,
and completion lifecycle-event count remain unchanged.

Given one fresh open root request and a stopped scheduler, when exact `M` submits park
and then retire, then each response matches R11 with
`code='root_lifecycle_unsupported'` and the submitted decision. The request remains
`open` after each call; its pending notice and deadline, acting fields, session, harness,
and completion lifecycle-event count remain unchanged. Neither the park nor the retire
seam is called.

Given an ordinary non-built-in child `C` has an open completion request, when exact `C`
submits retain, park, and retire in sequence, then each call returns `not_authorized` and
the request, wakes, session, harness, and completion lifecycle-event count remain
unchanged.

## Open Questions

1. **BLOCKING — park action contract.** The safe park/relaunch/stop-recycle primitive is
   unbuilt and is owned by `wi_6937890c-6ba6-48b7-a9d2-4eb4510fe245`. The completion
   record, notice, read path, retain path, and retire path are separable. The full
   retain/park/retire feature must not release until A15 uses the ratified real park
   interface. This spec does not name that interface.
2. **BLOCKING IMPLEMENTATION GATE — independent successor review.** The predecessor
   `art_a22ba0ec`, SHA-256 `cd1a9a99…`, received reviewed-clean verdict
   `att_4f59063a-f3e5-4697-9957-1e2c0787fada` against old source `95aefa…`.
   Recon verdict `att_eeb27cd2-b27a-4e79-af19-435fd1f564b4` found current-source drift
   and required this successor against release `6c13efc…`. Verdict
   `att_35dc33fc-660c-4989-b78d-56eab886a1e7` then requested F1 and F2 changes against
   exact artifact `art_46d2f24b`, SHA-256 `96bbca96…`. This canonical amendment resolves
   both findings. No implementation scope can start until a linked independent reviewer
   files `reviewed-clean` against the new exact artifact hash and release commit. On
   `changes-requested`, amend this canonical file before responding and publish another
   hash. The reviewed artifact retains this gate text; the linked verdict row resolves it
   without changing reviewed bytes.
3. **NON-BLOCKING — wider terminal coverage.** Completion is the only terminal admitted
   by this rail. Surrender, revoke, canceled, and failed assignment outcomes remain with
   `wi_3d6d13a0-c4cf-4370-88a1-b407c41ff7c1`. That owner can later supersede this scope
   with one shared terminal-notice design; this spec does not pre-approve that expansion.

Operating pattern taught by this spec: none. The new commands and production do not
exist in release 0.1.7. Guidance must not teach them before implementation and release
(wisdom 20 and 21).
