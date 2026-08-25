# Completion-escalation rail v2

Status: READY FOR NEW INDEPENDENT REVIEW for
`wi_809821f8-e72b-41d8-b4b5-af28c7e670a6`.
This file revalidates reviewed artifact `art_a22ba0ec`, SHA-256
`cd1a9a99d0f041cd88077b4e55f1cd23e76b26b4804f0478ef94ed6a7a6165d6`, against
Tightbeam 0.1.7 release commit `6c13efcbe9e1ae247b8aa7e91a374015c74dc947`.
Independent verdict `att_35dc33fc-660c-4989-b78d-56eab886a1e7` requested changes to
artifact `art_46d2f24b`, SHA-256
`96bbca96ab56e5269e40b19799f9b080142e8868eb635b8d15259e7988597736`. This successor
preserves those reviewed corrections and incorporates Mike's ALWAYS-PARENT ruling
`s_0100f65a-b2b4-4278-9c5b-394987e3a839`, SQLite waiver
`s_ee88a313-e923-435f-8999-44975bafe62f`, and abstraction ruling
`s_b9c9fa65-267a-43b2-823e-d372954d1378`. It deletes lineage climbing, Main fallback,
and assignment-opener inference from completion routing. It admits one explicit
assignment-card report-to declaration and the one justified stable cancellation
classification, `completion_transition`. It supersedes the predecessor only after an
independent reviewer clears this file's new exact hash. Implementation stays
unauthorized before that verdict. The park decision remains blocked on
`wi_6937890c-6ba6-48b7-a9d2-4eb4510fe245`.

## Goal

When a child session files a completion attest, Tightbeam records the completion and
routes its action request to that child's exact `spawnedBy` parent. The completion
record and its first parent-notification wake commit in the same transaction as the
attest and assignment close. Tightbeam does not climb the lineage and does not infer a
route from the assignment opener or the create ceremony. If the exact parent is absent,
inactive, or foreign-owned, Tightbeam commits the completion with the named
`parent-unavailable` delivery failure instead of inventing a recipient. R5 defines this
only exception to the first-parent-wake guarantee.

An assignment card can explicitly declare one additional report-to session. That exact
session receives one informational copy of the completion. The declaration grants no
disposition authority and creates no fallback. Without the declaration, no commission
channel exists, including to the assignment opener.

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
  escalate through the durable parent chain and stops escalation only after a live
  authority records the required disposition or a separate terminal contract closes
  the obligation
  (`accountability-constitution-v1.md:27-31`).
- Mike ruling `s_0100f65a-b2b4-4278-9c5b-394987e3a839`, recorded in
  `att_73471946-be23-46ad-b384-de4d8a8675fe`, makes the immediate `spawnedBy` parent the
  unconditional completion route. Any other delivery, including the assignment opener,
  requires an explicit report-to declaration on the card. No route derives from the
  create verb or ceremony.
- Mike waiver `s_ee88a313-e923-435f-8999-44975bafe62f` and ruled request
  `dr_5e23055c-0d2d-4eb6-88fb-ccffb3a6a601` authorize the shape-bump/recreate boundary
  needed to widen fixed wake-cancellation vocabulary. The abstraction answer
  `s_b9c9fa65-267a-43b2-823e-d372954d1378` rejects the five proposed values as a bundle:
  only `completion_transition` is a stable new domain classification.
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
  assignments for one child session and targets only the session's exact `spawnedBy`
  parent.
- The ordinary wake store is durable and at-least-once; `turns.wakeId` provides the
  exactly-once enqueue backstop (`wakes.ex:104-200`; `ledger.ex:1-18,99-148`).
- Ordinary wake delivery can re-resolve a stale lineage target
  (`supervision.ex:735-770,2680-2695`; `gateway.ex:1313-1353`). R7 disables that behavior
  for completion-linked wakes: exact parent and report-to incarnation keys never
  retarget.
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
   ordinary same-owner sibling and an explicit report-to recipient cannot act; R11's
   exact-parent and owner-user checks remain authoritative.
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

### Amendment rulings for SQLite vocabulary and routing

1. **Use existing cancellation reasons.** Generation replacement uses `superseded`,
   terminal request disposal uses `obligation_disposed`, and an exact delivery target
   that cannot accept a completion wake uses `target_unresolvable`. The rejected
   completion-specific reason names add no domain meaning.
2. **Add only `completion_transition`.** A completion row's typed terminal state,
   decision, acting principal, and terminal timestamp remain meaningful if wake delivery
   or lifecycle-event storage changes. `completion_transition` therefore names stable
   disposition evidence in `wake_cancellations`. It points to the completion row, not to
   an opaque `lifecycle_events` id.
3. **Do not add `lifecycle_event`.** It names a storage table rather than an event in the
   product. Existing lifecycle rows remain observability mirrors; no cancellation
   authority depends on them.
4. **Bump and recreate.** Adding `assignments.completionReportToSessionKey` and widening
   the closed wake-cancellation source/disposition checks changes existing table shapes.
   The build stamps `coordination-fabric-v1-phase1-v4`. A database stamped with another
   shape is refused before DDL or feature writes and must be moved aside and recreated.
5. **Route only from durable declarations.** A non-root completion's parent channel is
   exactly the holder session's `spawnedBy`. The optional commission channel is exactly
   the card's `completionReportToSessionKey`. `openedBySession`, `openedByUser`, the
   create verb, roles, lineage ancestors, and Main provide no implicit route.
6. **Split cancellation authority by the owning action.** R7 delivery refusal is owned
   by `tightbeam:wake-scheduler`. R8 deadline reissue is owned by
   `tightbeam:completion-escalation`, including its no-replacement cancellation when the
   exact parent cannot accept the next notice. Both use existing reason
   `target_unresolvable` and name the canceled wake as the `scheduler_delivery` source.
   This preserves truthful requester identity without adding a reason. It records the
   writer's smallest-contract disposition of withdrawn request
   `dr_52983a36-5c27-425f-9383-472108c09bce` under Mike's 2026-08-25 RULE YOUR OWN
   directive.
7. **Keep one typed delivery-failure marker.** R15 already requires
   `completion_escalation_undeliverable` for each exact-target delivery refusal. Its
   detail names `channel=parent|report-to` and `resolution=target-unresolvable`, so the
   existing marker remains truthful without adding a domain event or deleting specified
   observability. This records the writer's smallest-contract disposition of withdrawn
   request `dr_2195043c-a970-422b-90c9-789e998755b3` under that directive.

## Non-Goals

- No automatic retain, park, retire, reassignment, or reparenting.
- No lineage climb, Main fallback, role fallback, assignment-opener inference, or
  create-ceremony inference for a non-root child completion.
- No disposition delegation through `report-to`. The optional declaration adds one
  informational delivery only.
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
- No in-place schema migration or downgrade preservation. The ruled boundary is named
  shape refusal followed by database recreation.
- No notice for progress, surrender, revoke, or retire interruption. The shared
  ownerless-terminal fallback work item
  `wi_3d6d13a0-c4cf-4370-88a1-b407c41ff7c1` owns expansion beyond completion.
- No user-interface design.

### Deletion assessment

ADD wins because a durable parent-facing completion and a session-slate disposition
request do not exist. DELETE loses because deleting child completion or parent
accountability would violate the work model. ACCEPT loses because an event-log-only
failure would leave no addressed request and no acknowledgment path.

The added mechanism is one completion table, one wake-membership table, one nullable
assignment-card declaration, and one producer.
The membership table makes a completion wake mechanically identifiable after the
completion row advances to a later generation or terminal state. ADD wins because the
current-only wake ids cannot identify a delayed callback for an older generation. DELETE
loses because removing the stale-delivery guard permits an obsolete request to reach a
parent. ACCEPT loses because an unclassified pending callback can create a false current
request. The table stores membership only; it does not duplicate wake state, timing,
routing, or cancellation. The mechanism reuses the wake scheduler, existing assignment
count, existing retire path, and the future park primitive.

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
- **Immediate parent**: the exact session incarnation key in `sessions.spawnedBy` on the
  child session. For a non-root child, it is the only session recipient with disposition
  authority. Tightbeam never substitutes an ancestor, Main, role holder, or assignment
  opener.
- **Explicit report-to**: the optional exact session incarnation stored as
  `assignments.completionReportToSessionKey` when the card is created through
  `assign|dispatch --report-to <session-key>`. The target must then be active and owned
  by the child's owner. The immutable declaration authorizes one informational
  completion copy. It does not authorize a disposition.
- **Parent unavailable**: the non-root child's `spawnedBy` is null, names no active
  session, or names a session with another owner. Tightbeam records the exact observed
  class and creates no parent wake. It does not climb or fall back.
- **Root Main holder**: a child session whose row has `isBuiltIn=1` and whose
  `sessionKey` equals `Org.personal_session_key(ownerUserId)`. The exact key and built-in
  marker must both match. A custom session with a Main-like name is not a root Main.
- **Owner pin**: `ownerUserId` copied from the child session by the close transaction.
  Parent and report-to admission require their exact session rows to carry this owner.
  A foreign-owned declared target is ineligible, not a cue to search elsewhere.
- **Completion record**: one `completion_escalations` row keyed by the closing attest.
  It contains the cause, the initial routing ruling, the current delivery generation,
  and the optional disposition lifecycle.
- **Completion wake membership**: one `completion_escalation_wakes` row for each notice
  or deadline wake that the completion producer arms. It maps a durable wake id to one
  completion id, generation, and literal kind. Wake state and timing remain in `wakes`.
- **Parent receipt acknowledgment**: a turn joined through `currentParentNoticeWakeId`
  reaches `status='delivered'`. It proves that the exact parent ran the notice turn. It
  does not choose a disposition.
- **Report-to receipt acknowledgment**: a turn joined through `reportToNoticeWakeId`
  reaches `status='delivered'`. It proves that the declared informational copy ran. It
  grants no disposition authority. When report-to equals the parent target, the
  report-to projection shares the parent wake instead of creating a duplicate.
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
4. Each ordinary child's `spawnedBy` parent has the same `ownerUserId`. A null, missing,
   inactive, or foreign-owned immediate parent is dirt; the producer reports it and
   creates no parent wake instead of disclosing or searching for another recipient.
5. The owner's built-in Main is permanent under the current retire rail
   (`gateway.ex:5042-5052`). Root Main has no ordinary parent; R5 preserves its explicit
   retain-only self-request without making Main a fallback for another child.
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

For each wake id stored in `currentParentNoticeWakeId`, `reportToNoticeWakeId`, or
`deadlineWakeId`, exactly one
`completion_escalation_wakes` membership row exists with the same completion id and
generation. No other completion can claim that wake id. Historical membership rows stay
after the completion advances or terminalizes.

### R2 — Atomic close, record, and first notice

When R5 admits the exact parent, the completion attest insert, guarded assignment close,
completion-record insert, first parent-notification wake insert, and parent-notice
membership insert commit in one database transaction or all roll back. When R5 admits a
distinct explicit report-to recipient, its informational wake and membership commit in
that transaction too. An open request's deadline wake and membership also commit in
that transaction. When R5 returns `parent-unavailable`, that same transaction commits
the completion record and named lifecycle failure with no parent wake. Report-to
availability never changes that result. No post-commit callback creates an initial
notice or repairs the named failure. This follows the transactional outbox pattern
already required for decision notifications
(`escalation-delivery-v1.md:33-48,93-131`).

### R3 — Cause and principal are explicit

The record stores `closingAttestId`, `assignmentId`, nullable `workItemId`,
`childSessionKey`, literal outcome `completed`, `causeBySession`, `ownerUserId`,
`rootMainHolder`, `immediateParentSessionKey`, `remainingOpenAssignments`, and the
exact parent/report-to routing fields. The notification origin is
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

### R5 — Routing is ALWAYS-PARENT plus explicit report-to

For a non-root child, the close transaction copies the exact `sessions.spawnedBy` value
to `parentSessionKey`. It creates the parent notice only when that exact row exists,
has `state='active'`, and has the stored owner pin. It records
`parentRouteStatus='scheduled'`. A null, missing, inactive, or foreign-owned exact
parent records `parentRouteStatus='unavailable'`, writes
`completion_escalation_undeliverable` with the exact reason
`parent-missing|parent-inactive|parent-owner-mismatch`, and creates no parent wake. It
does not traverse `spawnedBy`, resolve a role, select Main, or inspect assignment opener
fields. An empty-slate row remains an open action request on which the owner user can act.
A row with work remaining stays `notice-only` and queryable as a named undeliverable
completion.

Assignment creation admits optional `reportToSessionKey` only when that exact session is
active and has the holder's owner. It stores the value immutably as
`assignments.completionReportToSessionKey`; omission stores null. Completion copies the
field to `reportToSessionKey`. At close, the producer first revalidates that exact row.
An absent, inactive, or foreign-owned row records
`reportToRouteStatus='unavailable'` and creates no report-to wake. An eligible row that
equals the admitted parent or root-self target records
`reportToRouteStatus='shared-parent'` and creates no duplicate wake. Any other eligible
exact target receives one generation-0 informational notice and records
`reportToRouteStatus='scheduled'`. Null records
`reportToRouteStatus='not-declared'`. Report-to has no deadline and is never reissued.

The principal already authorized to create the assignment is the only declaration
authority; `--report-to` grants no broader assignment-open authority. A missing,
inactive, or foreign-owned declared session makes `assign` or `dispatch` return
`invalid_report_to` with `reportToSessionKey=<submitted-key>` and commit no assignment,
effect, file, marker, supervision, work-item-bracket, or idempotency result. Replay of a
successful idempotent create returns the original card and cannot change the declaration.
`reopen-assignment` preserves it exactly.

For a root Main holder, the producer takes the root branch before reading `spawnedBy`.
It records `parentSessionKey=childSessionKey`, `parentRouteStatus='root-self'`, and
creates the retain-only self-addressed request. R2 and R4 create the same parent notice
and open request used for another empty child; the producer does not retain it
automatically. Root-self is an explicit root contract, not Main fallback for a child.

### R6 — Work-item parentage is immutable here

The producer reads `assignments.workItemId` for correlation. It does not write any
`work_items` field, creation-context field, assignment reference, or `Toplines` edge.
Neither exact parent delivery nor explicit report-to changes work-item parentage.

### R7 — Notice delivery uses exact durable targets

The initial parent notice has `wakeId =
completion:<closingAttestId>:parent-notice:0`. A distinct report-to notice has
`wakeId = completion:<closingAttestId>:report-to-notice`. Each uses
`consumer='prompt'`, `origin='process:tightbeam'`, `dueAt=now`, `targetGate=1`, null
`assignmentId`, and null `work_item_id`. Parent `sessionKey` is the exact admitted
`parentSessionKey`; report-to `sessionKey` is the exact admitted `reportToSessionKey`.
Each wake has null `targetRole`, null `reresolve`, null `reresolveSeed`, and null
`reresolveRung`. Generic role or lineage resolution cannot change either target.

The completion row, not `wakes.assignmentId`, carries assignment correlation. Current
code treats each process-origin prompt wake with an `assignmentId` as supervision-owned
and can suppress it when `work-blocked` stands (`wakes.ex:1210-1285`). Leaving that
carrier null prevents this completion notice from being misclassified. Leaving
`work_item_id` null prevents the generic wake-cancellation projection from treating a
session-lifecycle request as work-item liveness. The exact prompts below still carry the
assignment and work-item ids. The completion row supplies both typed joins through wake
membership.

For a notice wake joined through `completion_escalation_wakes`,
`Gateway.deliver_prompt_in_txn/5` calls the completion producer before generic target
resolution. The producer locks the decision to current rows inside that delivery
transaction. It admits a parent message and turn only when the wake remains pending,
equals `currentParentNoticeWakeId`, the completion status is `open` or `notice-only`,
and the exact parent or root-self row remains active and owner-pinned. It admits a
report-to message and turn only when the wake remains pending, equals
`reportToNoticeWakeId`, the report-to declaration still matches the copied assignment
field, the completion status is `open` or `notice-only`, and the exact report-to row
remains active and owner-pinned.

If a target predicate fails, the same transaction inserts no message or turn and
cancels the still-pending wake with existing reason `target_unresolvable`, source kind
`scheduler_delivery`, source id equal to the wake id, requester
`tightbeam:wake-scheduler`, and outcome `no_replacement`. The check and delivery or
cancellation are indivisible. The scheduler's earlier selection grants no delivery
authority. Cancellation makes the R14 receipt `canceled`, not `inconsistent`; its later
fired update cannot match (`wakes.ex:1166-1204`; `gateway.ex:978-1135`). No completion
delivery path climbs, falls back, retargets, or rewrites the card declaration.

If the exact target remains eligible but the wake is no longer current, a still-pending
historical parent wake is canceled with `superseded` and the current parent wake as its
replacement, or with `target_unresolvable` when no replacement exists. If the completion
is terminal, a still-pending parent or report-to wake is canceled with
`obligation_disposed` and the terminal `completion_transition`. These are recovery
guards for inconsistent residue; ordinary transitions already cancel the wakes in their
own transaction.

### R8 — Stable request and retry dedupe

`dedupeKey` never changes. Each routing generation uses deterministic wake ids:

```text
completion:<closingAttestId>:parent-notice:<generation>
completion:<closingAttestId>:report-to-notice
completion:<closingAttestId>:deadline:<generation>
```

The completion row stores the current generation, current deadline wake id, nullable
current parent-notice wake id, and nullable one-shot report-to wake id. Tightbeam reuses
the existing cancellation reasons and adds only the stable `completion_transition`
source/disposition classification:

- requester `{kind='process', id='tightbeam:wake-scheduler'}` can use existing reason
  `target_unresolvable` only for R7's exact delivery refusal;
- requester `{kind='process', id='tightbeam:completion-escalation'}` can use existing
  reasons `superseded`, `obligation_disposed`, and `target_unresolvable`; its
  `target_unresolvable` authority applies only when R8 cannot arm a replacement parent
  notice during deadline reissue;
- reason `superseded` uses causal source kind `wake`, names the replacement parent wake,
  and has outcome `replacement`;
- reason `target_unresolvable` uses causal source kind `scheduler_delivery`, names the
  canceled wake itself, and has outcome `no_replacement`; its requester is the wake
  scheduler for R7 delivery and the completion-escalation process for R8 reissue;
- reason `obligation_disposed` uses causal source and disposition kind
  `completion_transition`, names the same completion id in both fields, and has outcome
  `disposition`;
- a `completion_transition` source/disposition validates only when the completion row is
  terminal (`acknowledged`, `retained_root`, or `superseded`), carries the corresponding
  acting or supersession fields, and owns the canceled wake through
  `completion_escalation_wakes`.

No completion-specific reason, `lifecycle_event` source, or opaque event-log id is
admitted. `completion_transition` is justified because the typed terminal completion
row remains a domain fact if scheduler and event-log implementations change. The
proposed `completion_generation_replaced` and `completion_request_disposed` merely
renamed existing `superseded` and `obligation_disposed` facts. The proposed
`completion_delivery_ineligible` narrowed the existing `target_unresolvable` delivery
fact. The proposed `lifecycle_event` named storage rather than a domain event. No other
requester/reason compatibility pair gains authority. A raw
`UPDATE wakes SET state='canceled'` remains outside the design.

A reissue transaction CASes the current `deadlineWakeId`. It computes the next
generation and writes the `completion_escalation_reissued` observability mirror. It then
arms the replacement deadline and, when the same exact parent is still active and
owner-pinned, the replacement parent notice. While the old parent notice is still
current and pending, the transaction cancels it with `superseded` pointing to the
replacement parent wake. A `replacement` outcome is valid only when the replacement
membership names the same completion, the next generation, and kind `parent-notice`.
If no replacement parent notice can be armed, the transaction cancels a pending old
parent notice with `target_unresolvable` and `no_replacement`. It never reissues or
replaces the report-to notice. The transaction then updates the completion row to the
new generation and wake ids and marks the source deadline fired through
`Wakes.fire_internal_in_txn/4`. A refused cancellation or deadline-fire CAS rolls back
each replacement row, lifecycle row, completion-row change, and deadline consumption.

A stale or replayed deadline writes and arms zero rows. Database serialization gives a
delivery-versus-reissue race two results: delivery commits first and the old wake is no
longer pending, or reissue cancels first and R7 refuses the old callback. No two parent
notice generations for one completion remain pending after commit. Each reissued parent
notice uses R7's exact-parent wake fields. `turns.wakeId UNIQUE` prevents a duplicate
turn for one notice generation (`ledger.ex:1-18,99-148`).

### R9 — Deadline reissues; it does not judge

When the internal deadline fires, the transaction re-reads the request, the child
session, the child open-assignment count, the exact parent, and the source wake.
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
- request remains open and child remains active and empty: recheck only the exact
  parent, reissue the same request, and arm the next deadline.

Each successful branch marks the source deadline fired through
`Wakes.fire_internal_in_txn/4` in the same transaction. A branch that moves the request
to `superseded` writes its observability mirror and cancels any pending parent or
report-to notice through `obligation_disposed` with source and
disposition `completion_transition`. A refused cancellation or deadline-fire CAS
rolls back the request transition and deadline consumption.

Elapsed time never means the parent is incapable or that retire is correct. An exact
parent that remains active is re-notified. An unavailable exact parent records the
named failure and is not silently replaced because a timer elapsed.

### R10 — Assignment-open race supersedes in the opening transaction

Every successful `assign` and `dispatch` insert for a child session calls the one
`supersede_open_for_assignment_in_txn/3` seam after the assignment, effect, and file rows
exist and before the supervision transition. The seam changes an open completion request
for that child to `superseded/new-assignment`. It first writes the typed completion
transition and its lifecycle observability mirror. It then cancels the deadline and any
pending parent or report-to notice through `obligation_disposed`, with source and
disposition `completion_transition`, in that same transaction. The row stores the new
assignment id and transaction timestamp as
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
owner pin, is not the child, and its exact session key equals the copied
`parentSessionKey`. A report-to recipient, lineage ancestor, sibling, assignment opener,
role holder, or Main that is not that exact parent gains no authority. A user principal
is authorized only when it owns the child. An admin from another owner can read the
record under R15 but cannot choose a lifecycle disposition.

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
   completion row, deadline wake, parent notice wake, report-to notice wake, session row,
   and harness state unchanged. It calls neither the park dependency nor the retire preflight and writes
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
  deadline and any pending parent or report-to notice through `obligation_disposed`
  with source and disposition `completion_transition`, and
  mutate no session, harness, assignment, or work-item row. The transaction writes the
  terminal completion transition and its acknowledgment lifecycle mirror before those
  cancellations. A refused cancellation rolls back the lifecycle row and terminal
  completion state. Before the root branch
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
  acknowledgment lifecycle mirror, cancels its deadline and pending parent or report-to
  notice through `obligation_disposed` with source and disposition
  `completion_transition`, and stores `decision='retire'` before Org sees the
  remaining wakes. Request acknowledgment and session retirement therefore commit
  together. Existing post-commit broadcast, supervision notification, workspace archive,
  and adapter reap remain unchanged. If a lease is active, completion disposition leaves
  the completion request, its deadline, its parent and report-to notices, and each session row
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

No scheduler, sweep, notification terminal, unavailable-target path, or report-to path
writes a disposition.
No path writes `retained_root` except the explicit retain branch above.

### R13 — Retirement race closes the request truthfully

The existing retire transaction calls the completion seam for each retiring session.
If an open empty-slate request exists, explicit retirement acknowledges it as
`decision='retire'` with the retire call's typed principal. It writes the typed terminal
completion transition and acknowledgment lifecycle mirror, then cancels its deadline
and any pending parent or report-to notice through `obligation_disposed` with source and
disposition `completion_transition` before the session state transition. These actions share
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

The read projection derives `parentReceipt` from `currentParentNoticeWakeId` and
`reportTo.receipt` from `reportToNoticeWakeId`, or from the shared parent wake when
`reportToRouteStatus='shared-parent'`. Each wake-backed receipt maps rows without
inference:

- null wake id -> `state='not-created'`, `turnSeq=null`;
- pending wake and no turn -> `state='pending'`, `turnSeq=null`;
- canceled wake and no turn -> `state='canceled'`, `turnSeq=null`;
- existing turn -> its exact `queued|running|delivered|canceled|failed|failed_unknown`
  status and sequence;
- fired wake and no turn -> `state='inconsistent'`, `turnSeq=null`.

The fired wake row and absent joined turn are the durable evidence for `inconsistent`.
The read path writes no lifecycle event. Repeated reads return the same projection
without mutating `lifecycle_events`.

Earlier parent generations remain available through their wake/turn rows and lifecycle
trace; they do not overwrite the current parent receipt. Report-to has one generation.

Receipt does not close an action-needed request. Only R11-R13 do. Conversely, an
authorized action can acknowledge before either notice turn delivers; each pending
notice is canceled through R8's typed seam in the action transaction because its content is
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
- `completion_escalation_undeliverable` for each `parent-unavailable` generation and
  each R7 exact-target delivery refusal;
- `completion_escalation_cross_owner_lineage` when R5 observes a foreign-owned immediate
  parent; it reports dirt and never authorizes a lineage walk;
- `completion_escalation_state_inconsistent` for R11's inactive-child dirt;
- `completion_escalation_retire_deferred` when R12 observes an active critical lease;
- `completion_escalation_park_failed` when the external park operation does not commit.

For the completion ids selected into a `work-item-trace`, JobTrace joins
`completion_escalation_wakes` to `wakes`, turns, and wake cancellations. It emits those
wakes through the existing `wake_scheduled`, `wake_fired`, and `wake_canceled` entry
shapes and ranks. This explicit membership join is required because completion wakes
deliberately carry null direct work and assignment fields. A current or historical
completion cancellation names R8's existing truthful reason and the exact typed
completion, wake, or scheduler source that authorized it. The trace does not infer a
cancellation cause from the completion status.

The lifecycle `detail` is exactly:

- opened: null;
- reissued: `generation=<decimal> principal=process:tightbeam:completion-escalation`;
- superseded by assignment: `reason=new-assignment`;
- superseded by retired child:
  `reason=child-retired principal=process:tightbeam:completion-escalation`;
- ordinary acknowledged: `decision=<retain|park|retire>`;
- retained root: `decision=retain outcome=retained_root`;
- parent unavailable at close or reissue:
  `channel=parent resolution=parent-unavailable reason=<parent-missing|parent-inactive|parent-owner-mismatch> generation=<decimal> principal=process:tightbeam:completion-escalation`;
- parent or report-to target refused at R7 delivery:
  `channel=<parent|report-to> resolution=target-unresolvable reason=target-unresolvable generation=<decimal> principal=process:tightbeam:completion-escalation`;
- cross-owner lineage:
  `parentSessionKey=<session-key> principal=process:tightbeam:completion-escalation`;
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
one acting principal. `opened`, `reissued`, `superseded`, and `acknowledged` are stable
domain transitions because each remains meaningful if wake scheduling and event-log
storage change. Undeliverable, cross-owner, inconsistent, deferred, and park-failed are
operational observations, not cancellation-authority types. The remaining process markers name the completion process in
their exact detail. The three refused-action markers copy the already-authorized typed
caller into their exact detail at write time. Detail remains observability only; no
authorization, routing, transition, or read-visibility decision parses it.

`completion-notices --status open|all [--session <child>]` returns records visible to
the owner user, an admin, the child, the active owner-pinned exact parent, and the active
owner-pinned explicit report-to recipient. Report-to visibility grants no disposition
authority.
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

The unstamped parent prompt body is exactly:

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
parentRoute=<spawnedBy|root-self>
reportToSessionKey=<session-key-or-none>
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

The unstamped body of a distinct explicit report-to notice is exactly:

```text
Child completion copied by explicit report-to.
completionId=<completion-id>
assignmentId=<assignment-id>
workItemId=<work-item-id-or-none>
childSessionKey=<session-incarnation-key>
closingAttestId=<attest-id>
outcome=completed
causePrincipal=session:<child-session-key>
immediateParentSessionKey=<session-key-or-none>
parentRoute=<spawnedBy|parent-unavailable|root-self>
reportToSessionKey=<report-to-session-key>
remainingOpenAssignments=<decimal-count>
actionNeeded=<true|false>
This report is informational. Only the exact completion parent target or owner user can choose a disposition.
```

Assignment `assign`, `dispatch`, and `assignments` JSON adds the camelCase key
`reportToSessionKey`, always present with a string or null. The CLI accepts exactly
`--report-to <session-key>` on `assign` and `dispatch`. Omission stores null. No reopen,
attest, or disposition command accepts this flag.

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
  "routing": {
    "parent": {
      "sessionKey": "agent:... s_...",
      "routeStatus": "scheduled",
      "receipt": {"state": "pending", "turnSeq": null}
    },
    "reportTo": {
      "sessionKey": "agent:... s_...",
      "routeStatus": "scheduled",
      "sharesParentNotice": false,
      "receipt": {"state": "pending", "turnSeq": null}
    }
  },
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

`routing.parent.routeStatus` is `scheduled`, `unavailable`, or `root-self`.
`routing.reportTo` is null when no declaration exists. Otherwise its `routeStatus` is
`scheduled`, `shared-parent`, or `unavailable`. `sharesParentNotice` is true only for
`shared-parent`, and that object's receipt equals the parent receipt. A scheduled
report-to has its own receipt. An unavailable parent or report-to has
`receipt.state='not-created'`. No actual-recipient field exists because R7 forbids
retargeting. For `notice-only`, `request.status` is `notice-only` and its deadline/action fields are
null. For a retained root, `request.status` is `retained_root`, `decision` is `retain`,
`rootMainHolder` is true, and the acting fields name the explicit caller. For an
ordinary child, `rootMainHolder` is false. For missing `workItemId` or parent fields,
JSON uses null; prompt text uses `none`. No key is conditionally omitted.

### R17 — Compatibility and migration

`completion_escalations` is a new table created by its own `ensure_schema/1`; the schema
composition registers it after `Assignments`. The build also adds nullable
`assignments.completionReportToSessionKey` and admits `completion_transition` in the
closed `wake_cancellations` source/disposition checks. SQLite cannot widen those
existing shapes through `CREATE TABLE IF NOT EXISTS`. Under Mike's waiver, Schema bumps
the exact stamp from `coordination-fabric-v1-phase1-v3` to
`coordination-fabric-v1-phase1-v4`. A database carrying the prior or any other stamp is
refused by name before schema-module DDL or feature queries run. Tightbeam does not
alter, rebuild, sniff, copy, or repair it. The operator moves it aside and lets this
build create a fresh database, as the existing shape refusal instructs
(`schema.ex:35-65,938-1005`).

The release migrates and backfills no rows. Recreation starts with no assignments,
completion rows, or historical notices. The first completion recorded in the recreated
database is the first eligible cause. Downgrade means restoring a database created by
the downgraded build; a build that does not carry the exact stamp refuses this database.
Register the new internal consumer beside `effort_probe` and `effort_deadline` in the
gateway child specification, not in `Wakes` (`gateway.ex:292-300`).

The gateway and Rust CLI add `completion-notices`, `completion-disposition`, and optional
`reportToSessionKey`/`--report-to` on assignment creation. Because
the package is pre-1.0 and currently requires exact CLI/gateway versions, the release
bumps both together (`cli_compatibility.ex:1-38`). Old Clawline clients remain compatible
because the wire frame is unchanged.

### R18 — One mutation seam

`Tightbeam.Productions.CompletionEscalation` is the only module that inserts or updates
`completion_escalations` or inserts `completion_escalation_wakes`. Assignment close/open
and retirement call its in-transaction functions. The deadline consumer and public verbs
delegate to it. A source-closure test fails if production SQL mutates either table
anywhere else.

`Assignments` is the only owner of
`assignments.completionReportToSessionKey`. It writes that field only in the card-create
transaction and never updates it. `CompletionEscalation` copies the declaration into its
own record at close; it never mutates the assignment card.

`Wakes` remains the only owner of typed cancellation validation and cancellation rows.
`EventLog` remains the only owner of lifecycle insertion. The completion producer calls
their in-transaction seams; it does not duplicate their SQL. `Gateway` remains the owner
of message/turn delivery and session-retire orchestration. These boundaries let the
completion producer choose no disposition while keeping its tables behind one mutation
seam.

The close path runs the producer inside the same transaction, so no committed completion
can lack its dependent record. When a target is admitted, the row also cannot lack its first
admitted notice or notice membership. An open request cannot lack its deadline or
deadline membership. `parent-unavailable` is the only no-parent-notice result and
carries its named lifecycle marker. Report-to omission or unavailability never removes
the parent result. No recovery sweep is required for this edge. The ordinary wake
scheduler supplies crash recovery after commit.

## Architecture

### Record shape

The recreated `assignments` table adds exactly:

```sql
completionReportToSessionKey TEXT NULL REFERENCES sessions(sessionKey)
```

`assign` and `dispatch` validate the declared target as active and owner-matched in the
same transaction that inserts the card. No update or reopen seam changes this immutable
field.

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
  parentSessionKey          TEXT NULL REFERENCES sessions(sessionKey),
  parentRouteStatus         TEXT NOT NULL CHECK (
    parentRouteStatus IN ('scheduled','unavailable','root-self')
  ),
  reportToSessionKey        TEXT NULL REFERENCES sessions(sessionKey),
  reportToRouteStatus       TEXT NOT NULL CHECK (
    reportToRouteStatus IN ('not-declared','scheduled','shared-parent','unavailable')
  ),
  generation                INTEGER NOT NULL DEFAULT 0 CHECK (generation >= 0),
  currentParentNoticeWakeId TEXT NULL UNIQUE REFERENCES wakes(wakeId),
  reportToNoticeWakeId      TEXT NULL UNIQUE REFERENCES wakes(wakeId),
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
    (parentRouteStatus = 'scheduled' AND rootMainHolder = 0
      AND parentSessionKey IS NOT NULL
      AND parentSessionKey IS immediateParentSessionKey
      AND currentParentNoticeWakeId IS NOT NULL)
    OR
    (parentRouteStatus = 'unavailable' AND rootMainHolder = 0
      AND parentSessionKey IS immediateParentSessionKey
      AND currentParentNoticeWakeId IS NULL)
    OR
    (parentRouteStatus = 'root-self' AND rootMainHolder = 1
      AND parentSessionKey = childSessionKey
      AND currentParentNoticeWakeId IS NOT NULL)
  ),
  CHECK (
    (reportToRouteStatus = 'not-declared'
      AND reportToSessionKey IS NULL AND reportToNoticeWakeId IS NULL)
    OR
    (reportToRouteStatus = 'scheduled'
      AND reportToSessionKey IS NOT NULL AND reportToNoticeWakeId IS NOT NULL
      AND reportToSessionKey IS NOT parentSessionKey)
    OR
    (reportToRouteStatus = 'shared-parent'
      AND reportToSessionKey IS NOT NULL AND reportToNoticeWakeId IS NULL
      AND parentRouteStatus IN ('scheduled','root-self')
      AND reportToSessionKey IS parentSessionKey)
    OR
    (reportToRouteStatus = 'unavailable'
      AND reportToSessionKey IS NOT NULL AND reportToNoticeWakeId IS NULL)
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
  kind         TEXT NOT NULL CHECK (kind IN ('parent-notice','report-to-notice','deadline')),
  UNIQUE (completionId, generation, kind)
);
CREATE INDEX completion_escalation_wakes_completion
  ON completion_escalation_wakes(completionId, generation, kind);
```

`rootMainHolder` is captured from the session row and
`Org.personal_session_key(ownerUserId)` in the close transaction. The DDL does not embed
the Main key format. The action seam rechecks both inputs before it writes
`retained_root`. This keeps topology in `Org.personal_session_key/1`, its existing single
home (`org.ex:1035-1042`). The DDL makes a root holder's parent target the child itself
through `root-self`; it does not make Main a fallback for another child.

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
completion row and each admitted initial notice with the attest and
assignment close
(`assignments.ex:1130-1200`). A surrender follows the existing path without step 5.

The new producer cannot reject a truthful completion because delivery is unavailable.
If the exact parent is unavailable, it commits `parent-unavailable` and the lifecycle
record. A database
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

Keep `EventLog.lifecycle_in_txn/4` unchanged. Lifecycle rows mirror completion events for
observability; cancellation validation does not use their ids or parse their detail.

Extend `Wakes` only as follows: admit source and disposition kind
`completion_transition`; let process requester `tightbeam:wake-scheduler` use existing
reason `target_unresolvable` for R7 completion delivery; let process requester
`tightbeam:completion-escalation` use existing reasons `superseded`,
`obligation_disposed`, and `target_unresolvable` for R8 production; and add only the
exact compatibility pairs in R8. For `obligation_disposed`, the validator joins the
source/disposition completion id to `completion_escalations`, proves a typed terminal
state and its required terminal fields, and proves that the canceled wake belongs to
that completion. For a `superseded` replacement, it proves that the replacement
membership names the same completion, the next generation, and kind `parent-notice`.
For `target_unresolvable`, the existing `scheduler_delivery` source validator requires
its source id to equal the canceled wake id and a completion membership. The
`tightbeam:wake-scheduler` pair admits a delayed R7 callback from either exact completion
channel. The `tightbeam:completion-escalation` pair admits only R8's pending historical
parent notice when reissue cannot arm its replacement. A completion cancellation
command that fails one check returns `false`; each completion caller converts `false`
to a transaction failure. Existing reason meanings and every unrelated requester and
compatibility pair remain unchanged (`wakes.ex:290-352,478-516,599-606,651-789`).

Add `Wakes.fire_internal_in_txn/4` as the wake-owned CAS that changes one pending wake
with the expected internal consumer to `fired` and sets `firedAt`. It returns `true` only
when one row changes. The completion producer uses this seam for deadline consumption;
it never updates `wakes.state` directly.

### Exact implementation surfaces

- New: `lib/tightbeam/productions/completion_escalation.ex`.
- Register schema after `Assignments` in `lib/tightbeam/schema.ex`.
- Add immutable assignment `reportToSessionKey` create validation/projection and call
  close/open seams from `lib/tightbeam/assignments.ex`.
- Call retire acknowledgment from the canonical transaction in
  `lib/tightbeam/gateway.ex` before `Org.retire_in_txn/4`; preserve the existing
  post-commit retire completion path.
- Enforce R7's exact non-reresolving targets in gateway delivery for notice wakes joined
  through `completion_escalation_wakes`; leave non-completion wake rerouting outside this
  change.
- Register the internal deadline consumer in `lib/tightbeam/gateway.ex` composition.
- Extend typed cancellation in `lib/tightbeam/wakes.ex`; keep EventLog's insertion
  contract unchanged.
- Add read/action handlers in `lib/tightbeam/gateway.ex` and typed routing in the router.
- Add `principal: {:user, device.user_id}` to the authenticated device DELETE call in
  `lib/tightbeam/wire/router.ex`. Make generic retirement in
  `lib/tightbeam/gateway.ex` require and consume R3's typed caller principal. Preserve
  `origin` only as presentation and existing event context.
- Add Rust CLI args/dispatch/help for the two completion commands and assignment-create
  `--report-to`.
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

Given child `C` has two open assignments, active exact parent `P`, and no report-to
declaration, when `C` completes the first assignment, then the handler commits the
attest, closed assignment, one completion row, one generation-0 parent prompt wake, and
its `parent-notice` membership in one transaction. The row
is `notice-only`, stores `remainingOpenAssignments=1`, repeats that value in the exact
prompt, and has no deadline wake or deadline membership.

### A2 — Empty epoch opens one action request

Given `C` has one open assignment, active exact same-owner parent `P`, and no report-to
declaration, when `C` completes it, then the same transaction commits one
`status='open'` completion row, one due parent prompt
wake, and one internal deadline wake whose `sessionKey`, consumer, origin, due time,
deterministic id, null `assignmentId`, and null `work_item_id` match R4. It commits one
`parent-notice` and one deadline membership row for generation 0. The completion row stores
`remainingOpenAssignments=0`. The JSON projection matches R16, and the prompt matches
R16 byte-for-byte after substituting ids/timestamps.

### A3 — Rollback proves the outbox boundary

Given `C` has an active exact parent and a distinct explicit report-to, run four
fixtures in which a temporary SQLite trigger aborts the generation-0 parent notice, the
report-to notice, or either membership insert. When
`C` files completion in either fixture, then the attest, assignment close, completion
row, both notice wakes, deadline wake, work-item slate wake, and each completion wake
membership all roll back. The markers, current liveness trigger, supervision
transition, and effort cancellation also leave no committed row or state change. After
removing the trigger, one retry commits exactly one of each applicable row in the R2
transaction order.

### A4 — Replay and terminal race dedupe

Given two concurrent completion calls for one open assignment whose child has an active
same-owner exact parent and distinct explicit report-to, when both run, then one returns
success and one returns `assignment_closed`; one attest, one completion row, one
generation-0 parent notice and membership, one report-to notice and membership, and one
generation-0 deadline wake and membership exist. No orphan attest,
completion row, wake, or membership row exists. A corruption fixture that tries to
insert a second `status='open'` row for the same child fails the partial unique index.

### A5 — Parent routing and recorded cause

Given `C.spawnedBy=P`, `P` is active and owner-matched, and the assignment omits
`--report-to`, when `C` completes, then the record names `P` as immediate parent and
`parentSessionKey`, records `parentRouteStatus='scheduled'` and
`reportToRouteStatus='not-declared'`, and stores the exact closing attest, assignment,
work item, outcome, child incarnation, cause session, and owner. Exactly one parent
notice targets `P`; neither `openedBySession` nor `openedByUser` creates another notice.
The opened lifecycle event and typed `work-item-trace` entry carry the same completion
id, closing attest, child, cause principal, and work item. The trace entry has
`type='completion_escalation'`, `phase='opened'`, `at=createdAt`, and the R15 id. The
lifecycle row has `kind='completion_escalation_opened'`,
`subject=<completion-id>`, null detail, and a paired
`completion_escalation_event` trace entry.

### A6 — Dead parent fails loudly and never climbs

Given exact immediate parent `P1` is retired and same-owner ancestor `P2` and owner Main
`M` are active, when `C` completes, then the row preserves `P1`, records
`parentRouteStatus='unavailable'`, creates no parent notice for `P1`, `P2`, or `M`, and
writes the exact parent-inactive undeliverable marker with R15's parent channel detail.
Given `P1` is initially active
but retires after close and before delivery while `P2` and `M` remain active, when the
wake fires, then the delivery transaction cancels that exact wake with
`target_unresolvable`, inserts no message or turn, does not retarget, and writes R15's
exact parent delivery-refusal detail. The owner user can still read and disposition the
open request.

### A7 — Explicit report-to is the only commission channel

Given assignment opener `O`, active exact parent `P`, and a distinct active same-owner
session `R`, when `O` creates the card with `--report-to R` and `C` completes, then the
close transaction creates one parent notice for `P` and one informational report-to
notice for `R`. `R` can read the row but receives `not_authorized` from each disposition.
Given the otherwise identical card omits `--report-to`, completion creates no notice for
`O` or `R`, even when `O` is an active same-owner session. Given the declaration names
`P`, completion creates one parent notice, records `shared-parent`, and creates no
duplicate report-to wake. In each fixture, work-item parentage and `Toplines` are
byte-identical before and after except for the completing assignment's specified
terminal fields.

Given `--report-to` names a missing, inactive, or foreign-owned session, when `assign`
and `dispatch` each run, then each returns `invalid_report_to`, names the submitted key,
and commits none of the rows listed in R5. Given a successful idempotent dispatch is
replayed with another `--report-to`, then the idempotency conflict behavior is unchanged
and the original card declaration remains immutable. Assignment JSON always projects
the original string or null.

### A8 — Parent and report-to absence are explicit

Given a non-root child has null, missing, inactive, or foreign-owned exact parent, when
completion commits, then each fixture records `parentRouteStatus='unavailable'`, writes
the exact R5 reason, creates no parent wake, and leaves an empty-slate request open and
queryable with its internal deadline armed and `routing.parent.receipt.state='not-created'`.
An active ancestor and owner Main receive no inferred notice. Given the child instead
has another open assignment, the row is `notice-only`, has no deadline, and remains
queryable. Given a distinct report-to declaration becomes inactive before close, then
the row records `reportToRouteStatus='unavailable'`, creates no report-to wake, and does
not change the parent result. Given report-to instead names the exact parent and that
row becomes inactive before close, then both routes record `unavailable`; the report-to
route does not record `shared-parent`. Given an admitted parent or report-to retires after close
but before delivery, R7 cancels only that channel's wake with `target_unresolvable`,
writes the exact R15 delivery-refusal detail with the corresponding channel, and does
not redirect it.

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
selects a pending parent or report-to notice and the exact target retires before the
delivery transaction starts, when the delayed callback runs, then R7 inserts no message
or turn. If the wake is still pending, the same transaction cancels it with existing
reason `target_unresolvable`, source kind `scheduler_delivery`, requester
`tightbeam:wake-scheduler`, and outcome `no_replacement`, and writes R15's exact
delivery-refusal detail for that channel.

### A11 — Deadline is a reminder, not a verdict

Given an open empty-slate request whose exact active parent has not acted, when its deadline
fires, then generation increments once, that same exact parent receives one reissued
notice, one replacement deadline is armed, and no decision or session lifecycle changes.
Given generation 0 remains pending without a turn because delivery failed, when its
deadline fires, then the same transaction arms generation 1 and its membership, records
them as the replacement outcome while it cancels generation 0, and commits with exactly
one pending notice generation. A replay of the old deadline id cancels nothing and arms
nothing. Given the scheduler selected generation 0 before that transaction, when its
delayed delivery callback starts afterward, the delivery transaction observes that
generation 0 is canceled and no longer current, and inserts no generation-0 message or
turn. If delivery commits first, generation 0 has one turn before generation 1 is armed.

Given the exact parent is unavailable when the deadline fires, then generation advances,
the row records `parentRouteStatus='unavailable'`, no replacement parent notice is
created, one replacement deadline is armed, and a pending old parent notice is canceled
with `target_unresolvable`, source kind `scheduler_delivery`, requester
`tightbeam:completion-escalation`, and outcome `no_replacement`. The report-to notice
count remains one or zero exactly as generation 0 established; no report-to notice is
reissued.

### A12 — New assignment supersedes atomically

Given an open empty-slate request, when a new assignment to `C` commits, then that same
transaction marks the request `superseded/new-assignment`, cancels the deadline and any
pending parent or report-to notice through typed `obligation_disposed` cancellations, and
records the new assignment id, `supersededAt`, and typed opener principal. Each
cancellation points to the terminal completion row through source and disposition kind
`completion_transition`. If any attempted pending-wake cancellation
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
wakes through typed `obligation_disposed` cancellations sourced from the terminal
`completion_transition`, and changes no session, harness, assignment, or work-item
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
typed terminal `completion_transition`. Given any attempted completion-wake cancellation
is refused, the request, session, assignment, ordinary retirement wakes, and lifecycle
rows remain unchanged. Given retire and
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
`completion-disposition`, then the exact active owner-pinned `spawnedBy` parent and the
owner user can act. The explicit report-to recipient, another active same-owner ancestor,
assignment opener, owner Main when it is not the exact parent, ordinary child acting on
its own row, a sibling, an admin user from another owner, a
different-owner session/user, a process principal, a remedy principal, and each retired
session principal are refused without
changing the request. Each refusal code and the R11 precedence is asserted. The read
matrix separately calls `completion-notices` and proves that the owner user, an admin,
the child, exact parent, and explicit report-to can read the row while an undeclared
opener, sibling, other ancestor, and every non-admin
different-owner principal receive no row. Given `P` acknowledges retain and later
retires, the exact retired session key `P` cannot read that acknowledged row or replay
the identical retain decision. The owner user and an admin can still read it. The owner
user's identical retain returns `request_not_open` because `actedBySession=P`; it
changes no completion row, lifecycle row, wake, session, harness, assignment, or work
item. A separate terminal fixture with `actedByUser=ownerUserId` proves that the same
owner-user principal can replay its identical decision. A replacement incarnation with
the same role and each sibling cannot read or replay either row.

### A17 — Receipt differs from action

Given a parent or report-to notice turn delivers, then that channel's read projection
says `receipt.state='delivered'` while the request remains open. Given an authorized
action commits before either notice delivery, then the action transaction cancels each
stale pending notice and the request is acknowledged. Given the scheduler selected one
notice before acknowledgment commits, when its delayed
delivery callback starts afterward, the delivery transaction observes the acknowledged
status and inserts no message or turn. If delivery commits first, its turn precedes the
acknowledgment transaction. No test treats a delivered turn as a retain decision.

### A18 — Notice-only completion remains visible

Given A1 and a parent notice terminal of delivered, failed, canceled, or
`failed_unknown`, when `completion-notices --status all` runs, then it returns the
completion with that exact parent receipt state.
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

### A20 — Compatibility and shape refusal

Given a database stamped `coordination-fabric-v1-phase1-v3`, including one whose
`wake_cancellations` table carries the old closed checks, when the new build boots, then
Schema refuses it before any DDL, assignment query, cancellation insert, or completion
producer call. The error names both stamps and says to move the database aside and let it
be recreated. Given an empty database, when the new build boots, then it stamps
`coordination-fabric-v1-phase1-v4` before table creation and creates the new assignment,
cancellation, and completion shapes. A fixture inserts and validates each R8
compatibility pair against the real recreated SQLite schema. The build performs no
ALTER, table copy, data migration, or historical completion backfill. Current ordinary
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

The closure test also proves that only `Assignments` writes
`completionReportToSessionKey`, only card creation accepts `reportToSessionKey`, and no
path derives it from `openedBySession`, `openedByUser`, a role, or create-verb identity.
It proves that every completion parent target equals the holder row's exact `spawnedBy`,
that parent/report-to wakes carry no reresolution fields, that report-to never reaches
the disposition authorization branch, and that the completion producer adds no new
cancellation reason or `lifecycle_event` source.

### A22 — Real smoke

Given one real gateway with exact parent `P`, child `C`, distinct explicit report-to `R`,
and same-owner opener `O`, when a real assignment is dispatched with `--report-to R`,
`C` files completion, and `P` retains, then the smoke captures both actual stored
messages, turns, wakes, the completion row, assignment projection, CLI read
response, visibility results for the R15 matrix, typed opened and acknowledged
`work-item-trace` entries, and retain acknowledgment response. It also captures the
opened and acknowledged lifecycle rows, their
`completion_escalation_event` trace entries, and the membership-linked
`wake_canceled` entries for the retained request's parent notice, report-to notice, and
deadline. It proves `R` can read but cannot act and that `O` receives no inferred
delivery. Compare those
outputs to R15-R16 after replacing only generated ids/timestamps. Passing unit tests
without this smoke does not satisfy the rail.

### A23 — Cross-owner lineage fails closed

Given corrupt fixture state points `C.spawnedBy` at an active session owned by another
user while the child's owner Main `M` is active, when `C` completes, then the resolver
writes one `completion_escalation_cross_owner_lineage` event, sends no wake or readable
row to the foreign
session or user, records `parentRouteStatus='unavailable'`, and preserves the foreign
`spawnedBy` fact for diagnosis. It sends no notice to `M`; Main state is irrelevant.

Given same-owner `P1` is the exact parent, foreign-owner `P2` is its ancestor, and
`P1` retires before delivery, when the notice wake fires, then the delivery transaction
does not deliver to or inspect `P2`. It cancels the exact `P1` wake with
`target_unresolvable`, inserts no message or turn for `P2`, `M`, or a fabricated key,
and preserves `P1` as the parent target. The parent receipt becomes `canceled`, and
repeated reads add no lifecycle event.

### A24 — Root Main retains explicitly

Given exact built-in Main `M` holds one open assignment and the scheduler is stopped,
when `M` completes that assignment, then the close transaction creates the normal
`status='open'` row with `remainingOpenAssignments=0`, addresses the generation-0 notice
to `M` as `root-self`, and arms the deadline. Before delivery,
`completion-notices --status open` called as `M` returns that row with
`routing.parent.receipt.state='pending'`, null acting fields, and null decision. The session and harness
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
   exact artifact `art_46d2f24b`, SHA-256 `96bbca96…`. This canonical amendment preserves
   those resolutions and incorporates ruled request `dr_5e23055c…` plus Mike's
   ALWAYS-PARENT ruling. No implementation scope can start until a linked independent reviewer
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
