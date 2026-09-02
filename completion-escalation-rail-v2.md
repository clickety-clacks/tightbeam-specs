# Completion-escalation rail v2

Status: TARGETLESS G1/G2 REVISION CANDIDATE — AWAITS ONE OWNER-OPENED
INDEPENDENT EXACT-SHA REVIEW for
`wi_809821f8-e72b-41d8-b4b5-af28c7e670a6`.

Tightbeam main `6ae34287aa4864b8fe6fabfc96166d02b9827a89` contains the previously
reviewed completion-only mechanism. Mike's 2026-09-01 scope request
`s_6f2c6413-8e9a-4b7f-bfc9-3c395bcd19b0` identifies two pre-release gaps in
those landed bytes. First, the action-needed request must open for each observable
one-or-more-to-zero assignment transition, not only for a completion attest. Second,
an unanswered request must stop repeating forever to one recipient and must climb the
same-owner `spawnedBy` reporting chain after a bounded number of reissues. This revision
specifies those changes without choosing retain, park, or retire.

The prior foreign-key correction remains authoritative: diagnostic parent-copy columns
store observed keys without session foreign keys. The explicit report-to commission copy,
typed cancellation vocabulary, root-Main retain-only rule, and external park dependency
remain unchanged. This revision has no product integration target. No implementation
delta may start until one owner-opened independent reviewer accepts this file's exact
content hash.

## Goal

When a terminal assignment mutation changes a child session's open-assignment count from
one-or-more to zero, Tightbeam records one empty epoch and opens one action-needed
request in that same transaction. Completion and revocation are current 0.2 terminal
mutations and are the only trigger cases in this revision. Active surrender remains
deleted from 0.2, so this rail adds no dead branch for a transition the product cannot
emit. If surrender returns to 0.2, this trigger requires a separately reviewed third
case. A session that has never held an assignment has no observable
one-or-more-to-zero transition. Open Question 3 records that deliberate, non-blocking
exclusion.

The effective reporting parent returned by `Org.effective_parent_in_txn/2` is the
immutable initial search seed. If that exact session is eligible, it is the first action
recipient. Otherwise the initial selector skips it under R5 and R9 and chooses the
nearest active, same-owner, unvisited `spawnedBy` ancestor or the owner-user root.
Tightbeam reissues to one selected session recipient on the existing decision deadline
at most the stored per-recipient limit. If no disposition acknowledges the request, the
next deadline advances by the same rule. The walk skips retired links, terminates
cycles, and ends at the owner-user root through the existing wake-to-user seam. Each
selected session recipient or the owner user becomes the exact current disposition
authority. Tightbeam routes the unchanged request; it does not choose its outcome.

For completion, the completion record and its first notice still commit with the attest
and assignment close. A completion that leaves other assignments open remains a
`notice-only` informational record and does not start the escalation ladder. The original
effective-parent snapshot stays immutable audit truth after an action request advances
to another reporting ancestor.

An assignment card can explicitly declare one additional report-to session. That exact
session receives one informational copy of the completion. The declaration grants no
disposition authority and creates no fallback. Without the declaration, no commission
channel exists, including to the assignment opener.

When the completed holder is the owner's exact built-in Main, that Main is both child
and the initial session recipient. Tightbeam creates the normal open request and
addresses its notice to that exact Main. The Main session can explicitly retain itself into the named
`retained_root` terminal state. Tightbeam does not auto-retain it. Park and retire stay
unavailable for the permanent root session. If Main ignores its bounded notices, the
owner user becomes the terminal recipient.

If a terminal mutation leaves a non-root child session with zero open assignments, the
empty-epoch record becomes an action-needed request. A session principal authorized by
R11 or the owner user chooses exactly one disposition under R11: retain, park, or retire.
Tightbeam records and enacts that explicit choice. Tightbeam does not choose a
disposition and does not auto-retire.

This rail implements substrate law over rows. It does not teach a conversational norm.
The conditions are observable assignment, attest, session, and wake rows; the action is
deterministic routing and verification. The retain/park/retire choice stays with an
agent or user (wisdom 1, 5, 6, 8, and 9).

### Authority and current evidence

- The accountability constitution requires escalation to reach a living authority by
  climbing past dead spawner links to the owner root. It applies the same rule to empty
  or dead escalation chains (`accountability-constitution-v1.md:16-17,125-126`).
- Mike's scope request `s_6f2c6413-8e9a-4b7f-bfc9-3c395bcd19b0` supplies the observed
  trigger and silence evidence: 380 completion, 61 revocation, 53 surrender, and three
  initial-zero idle sessions; Main also ignored four consecutive daily notices on
  `wi_0bb4b7eb`.
- Ruled accept outcomes `dr_d255b817-1541-460e-8549-bc55a9e7aa1f` and
  `dr_518d5591-57b8-4a73-8aeb-6634afb334a1` were delivered as exact recorded rationale
  by the product owner in `s_904edadd-16b9-41ba-81cf-680eb8c86c3a`; the delivery is not
  represented as Mike's personal wording. The first keeps initial-zero outside this
  transition revision. The later, authoritative surrender ruling preserves the 0.2
  deletion and admits only completion and revocation here.
- Mike ruling `s_0100f65a-b2b4-4278-9c5b-394987e3a839`, recorded in
  `att_73471946-be23-46ad-b384-de4d8a8675fe`, makes the completion parent the
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
  assignments for one child session, snapshots the effective reporting parent, and
  routes an unanswered request through the same-owner spawner chain to the owner user.
- Exact main `6ae34287aa4864b8fe6fabfc96166d02b9827a89` implements the one parent-selection
  contract in `Org.effective_parent_in_txn/2`: a non-null `operationalParent` returns
  unchanged with source `explicit`; null returns the owner's canonical Main key with
  source `owner_main`; the resolver never reads `spawnedBy` and never writes. The current
  contract is the initial snapshot source for the reviewed completion-only rail. The
  current composed database stamp is `coordination-fabric-v1-phase1-v15`.
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
   current-recipient and owner-user checks remain authoritative.
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
   The revised build reserves `coordination-fabric-v1-phase1-v16` after current v15. A database stamped with another
   shape is refused before DDL or feature writes and must be moved aside and recreated.
   In-place migration remains declined because Mike's waiver selected recreation and
   current-main reconciliation changes only the allocated stamps, not that policy.
5. **Route only from durable rows.** A non-root terminal transition's immutable initial
   parent snapshot is exactly the result of `Org.effective_parent_in_txn/2` for the
   holder. An unanswered open request later walks only stored same-owner `spawnedBy`
   links under R9. The optional completion commission channel is exactly the card's
   `completionReportToSessionKey`. `openedBySession`, `openedByUser`, the create verb,
   roles, prompt text, and report-to provide no implicit action route.
6. **Split cancellation authority by the owning action.** R7 delivery refusal is owned
   by `tightbeam:wake-scheduler`. R8 deadline reissue is owned by
   `tightbeam:completion-escalation`, including its replacement cancellation when the
   current recipient cannot accept the next notice. Both use existing reason
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
8. **Delete the diagnostic parent-copy foreign keys.** A selected effective-parent key
   can name a missing row. That is required dirt, not a valid session relation. The
   completion row must preserve that dangling observed key while it records
   `parent-unavailable`. Therefore
   `immediateParentSessionKey` and `parentSessionKey` are non-null text copies without
   `REFERENCES sessions(sessionKey)`. Child, cause, and report-to fields retain their
   session foreign keys. This is the sole F1 correction from
   `att_9d9af9f6-a194-4965-a5d8-d529e6de4395` and `art_635358a2`.
9. **Preserve fired notice truth.** A delivered prompt wake is `fired`, so a later retain
   records no cancellation for that notice. Retain still cancels the pending deadline
   and any notice that has not delivered. A22 asserts `wake_fired` for the two delivered
   notices and `wake_canceled` for the pending deadline.

## Non-Goals

- No automatic retain, park, retire, reassignment, or reparenting.
- No role fallback, assignment-opener inference, or create-ceremony inference. An open
  action request climbs only the same-owner `spawnedBy` chain under R8-R9. A
  `notice-only` completion never climbs.
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
- No empty-epoch request for progress, cannot-proceed, retirement interruption, or a
  terminal mutation that leaves another assignment open.
- No active-surrender restoration or dead surrender branch. Current 0.2 cannot produce
  that transition. If surrender returns, a separate spec amendment must add and verify
  the third trigger case before release.
- No user-interface design.

### Deletion assessment

ADD wins for G1/G2 because the current durable completion row does not represent a
revocation-triggered empty epoch or a bounded recipient climb. The revision extends that
one row and producer instead of creating a second rail. DELETE loses because removing
the current completion notice/request would violate the work model. ACCEPT loses because
the observed revoked and indefinitely ignored states remain unaddressed.

The mechanism remains one completion table, one wake-membership table, one nullable
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

The completion row adds `parentResolutionSource`. ADD wins because a later reparent can
change the source session while the completion route must remain immutable audit truth.
DELETE and ACCEPT lose because recomputation cannot prove whether the close selected an
explicit stored parent or Owner Main.

## Terms

- **Child session**: the assignment holder named by `assignments.holderKey` on the
  assignment closed by the admitted terminal cause. It is one session incarnation, not
  a role.
- **Terminal cause**: the immutable row that caused the assignment close. Completion
  uses the committed `attests` row with `kind='completion'`. Revocation uses the
  committed `assignment_revocations` row for the exact assignment generation. The
  record stores `causeKind='attest'|'revocation'`, the exact `causeId`, the terminal
  outcome, and the typed cause principal. Active surrender is not a terminal cause in
  0.2 and has no branch in this revision.
- **Effective reporting parent**: the exact session incarnation key returned by
  `Org.effective_parent_in_txn/2` for the child inside the close transaction. A non-null
  `sessions.operationalParent` returns with source `explicit`; null returns the owner's
  canonical Main key with source `owner_main`. It is the immutable search seed and audit
  snapshot, not permanent disposition authority after the request advances. The resolver does
  not read `spawnedBy`, climb, judge eligibility, or write.
- **Exact parent**: shorthand in this spec for the effective reporting parent selected
  and copied into the completion row by the terminal transaction. A later reparent does
  not rewrite that snapshot. Only the separately stored current recipient carries
  session disposition authority.
- **Parent snapshot fields**: the legacy-named `immediateParentSessionKey` and
  `parentSessionKey` columns. Each stores the exact selected effective reporting parent,
  including root-self. `parentResolutionSource` stores `explicit` or `owner_main` from
  the same resolver call.
- **Explicit report-to**: the optional exact session incarnation stored as
  `assignments.completionReportToSessionKey` when the card is created through
  `assign|dispatch --report-to <session-key>`. The target must then be active and owned
  by the child's owner. The immutable declaration authorizes one informational
  completion copy. It does not authorize a disposition.
- **Parent unavailable**: the non-root child's selected effective reporting parent names
  no active session, names a session with another owner, or cycles to the child. Tightbeam records the exact
  observed class. For an action-needed request, R9 walks from that snapshot toward a
  living same-owner ancestor or the owner-user root. For `notice-only`, no fallback
  notice exists.
- **Root Main holder**: a child session whose row has `isBuiltIn=1` and whose
  `sessionKey` equals `Org.personal_session_key(ownerUserId)`. The exact key and built-in
  marker must both match. A custom session with a Main-like name is not a root Main.
- **Owner pin**: `ownerUserId` copied from the child session by the close transaction.
  Parent and report-to admission require their exact session rows to carry this owner.
  A foreign-owned declared target is ineligible, not a cue to search elsewhere.
- **Completion/empty-epoch record**: one `completion_escalations` row keyed by the
  terminal cause. A completion can be `notice-only` or can open an empty epoch.
  Revocation creates a row only when it opens an empty epoch. The row contains the cause,
  immutable initial routing snapshot, current escalation recipient, action generation,
  and disposition lifecycle.
- **Completion wake membership**: one `completion_escalation_wakes` row for each notice
  or deadline wake that the completion producer arms. It maps a durable wake id to one
  completion id, generation, and literal kind. Wake state and timing remain in `wakes`.
- **Current action-notice wake**: the wake named by the legacy column
  `currentParentNoticeWakeId`. After G2 advances the request, this wake targets the
  current recipient and need not target the immutable parent snapshot. The column name
  does not grant parent authority.
- **Current-recipient receipt acknowledgment**: a turn joined through
  `currentParentNoticeWakeId` reaches `status='delivered'`. It proves that the current
  session recipient ran the notice turn. At the owner-user root, delivery through the
  user's Main stream provides the existing user-delivery receipt. Neither receipt chooses
  a disposition.
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
- **Empty epoch**: one terminal transaction that changes the child's open-assignment
  count from one-or-more to zero. Its identity is the terminal cause kind plus cause id.
  A later assignment supersedes that epoch. A later one-or-more-to-zero transition creates
  another row even when it closes the same reopened assignment.
- **Current escalation recipient**: exactly one typed principal stored on an open request:
  either an active, owner-matched session selected for the current rung, or the owner user
  at the terminal root rung. This principal is the only session recipient authorized to
  disposition the row; the owner user retains owner authority at every rung.
- **Owner-user root carrier**: `Org.personal_session_key(ownerUserId)`, used only to
  carry the ordinary prompt wake to the owner user's stream. The stored recipient and
  disposition authority are the owner user, not that Main session. A missing or inactive
  carrier is named delivery dirt; it does not transfer authority or close the request.
- **Living capable authority**: for deterministic routing, either the owner user or an
  active, owner-matched session that is not the child, has not already received this
  request, and can therefore pass R11 authorization. R5's root-self Main is the sole
  session exception before it advances. This term describes stored
  eligibility; the substrate does not infer attention, skill, or the correct disposition.
- **Action generation**: the zero-based count stored in legacy field `generation` for
  action-notice scheduling attempts. Generation zero is the initial attempt. Each
  successful deadline transaction that reissues to the same recipient or advances to a
  new recipient increments it once before it tries to arm the replacement. The value
  still advances when the selected owner-user root has no eligible carrier, but no wake
  or `completion_escalation_reissued` marker falsely claims delivery in that case.
  `notice-only` and report-to wakes use generation zero and never advance.
- **Recipient generation**: the zero-based count of recipient changes for one request.
  Generation zero is the first eligible recipient selected from the effective-parent
  search seed, which can already be an ancestor or the owner user. Each later change to
  another session or the owner-user root increments it once. Same-recipient reissues do
  not increment it.
- **Recipient reissue count**: the number of notices issued after the first notice to the
  current recipient. It starts at zero and increments only for a same-recipient reissue.
  A recipient change resets it to zero.
- **Recipient reissue limit**: the non-negative `prod_limit` value copied into the request
  when an empty epoch opens. The default is 3. It bounds waiting; it does not classify a
  recipient or select a disposition. With the default, one initial notice plus three
  reissues gives one recipient four notices before the next deadline climbs.
- **Reissue deadline**: a finite retry time copied from
  `:escalation_decision_deadline_ms` (default 86,400,000 ms). It bounds when Tightbeam
  repeats or advances an open action-needed notice. It does not decide that a recipient
  failed.
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
3. Session rows persist after retirement. `spawnedBy` preserves the durable creation
   provenance that R9 alone can walk for an unanswered action request
   (`org.ex:65-90,505-565`).
4. Initial parent-notice admission requires the selected effective parent to carry the
   child's `ownerUserId` and not equal the non-root child. A missing, inactive,
   foreign-owned, or self-cycling snapshot is dirt; the
   producer reports it, creates no wake for that target, and applies R9's typed
   same-owner search for an action request. A `notice-only` completion does not search.
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

### R1 — One durable record per admitted terminal cause

For each assignment completion committed after `CompletionEscalation.ensure_schema/1`
has succeeded, exactly one `completion_escalations` row exists. For each revocation that
changes the holder's open-assignment count from one-or-more to zero, exactly one row
exists. A revocation that leaves another assignment open creates no row. Active
surrender is absent from the 0.2 producer and creates no branch here.

The row's `dedupeKey` is `terminal:<causeKind>:<causeId>`. Completion stores
`causeKind='attest'`, `causeId=closingAttestId`, and `outcome='completed'`. Revocation
stores `causeKind='revocation'`, `causeId=revocationId`, null `closingAttestId`, and
`outcome='revoked'`. A unique constraint on `(causeKind,causeId)` makes replay of one
terminal cause unrepresentable. `assignmentId` is intentionally non-unique. If a closed
assignment reopens and later closes again, the later terminal cause creates a distinct
row when R1 admits that outcome; each earlier row remains immutable durable history.
A partial unique index on `childSessionKey` where `status='open'` makes two live
disposition requests for one child unrepresentable. Historical `notice-only`,
`acknowledged`, `retained_root`, and `superseded` rows can coexist.

For each wake id stored in `currentParentNoticeWakeId`, `reportToNoticeWakeId`, or
`deadlineWakeId`, exactly one `completion_escalation_wakes` membership row exists with
the same completion id and the action generation recorded when that wake was inserted.
Every parent-notice membership carries its
typed delivery recipient. An action-notice or deadline membership also carries the
recipient generation and reissue count that the request stored when it inserted that
membership; later request advances do not rewrite history. A `notice-only` parent membership
carries null recipient counters. A report-to membership carries no action recipient. No other completion can claim that
wake id. Historical membership rows stay after the request advances or terminalizes.

### R2 — Atomic terminal transition, record, and first notice

For completion, the attest insert, guarded assignment close, completion-record insert,
each admitted first notice wake, and membership insert commit in one database transaction or
all roll back. When R5 admits a distinct explicit report-to recipient, its informational
wake and membership commit in that transaction too. For a zero-producing revocation,
the revocation row, revocation-generation row, guarded assignment close, empty-epoch
record, first admitted action notice, and membership commit in the revocation transaction
or all roll back. Each open session-recipient request's deadline wake and membership
commit with it. An owner-user-root request has no deadline under R4.

If initial selection or R9 reaches the owner-user root, the same transaction attempts to
arm the request through the existing wake-to-user outbox target. If that carrier is
missing or inactive, the request commits with the owner user as current recipient, null
current notice and deadline, and the named `owner-carrier-unavailable` failure marker.
The owner can still act through the read/command path. Report-to availability never changes the
action-request result. No post-commit callback creates or repairs an initial request.
This follows the transactional outbox pattern already required for decision notifications
(`escalation-delivery-v1.md:33-48,93-151`).

### R3 — Cause and principal are explicit

The record stores `causeKind`, `causeId`, nullable `closingAttestId`, nullable
`revocationId`, `assignmentId`, nullable `workItemId`, `childSessionKey`, the exact
terminal `outcome`, exactly one typed cause principal, `ownerUserId`,
`rootMainHolder`, `immediateParentSessionKey`, `parentResolutionSource`,
`remainingOpenAssignments`, the exact parent/report-to routing fields, and the current
recipient fields. The notification origin is `process:tightbeam`. Completion's cause
principal is `session:<attests.bySession>`. Revocation's cause principal is exactly
`user:<revokedByUser>` or `session:<revokedBySession>`. No domain field derives a
principal from prose or an untyped origin string.

Each successful generic retirement carries one typed caller principal into the shared
retirement transaction. The device `DELETE /api/streams/:key` route constructs
`{:user, device.user_id}` from the authenticated device row. An agent call carries its
authenticated `{:session, sessionKey}` or explicit authenticated `{:user, userId}`.
Gateway derives the target-owner match from this typed principal and serializes it as
`session:<sessionKey>` or `user:<userId>` before it calls the completion retirement seam,
assignment interruption, or `Org.retire_in_txn/4`. It does not derive either the owner or
the acting principal from `call.origin`. A call without one admitted typed form returns
the existing generic-retire `not_found` result before idempotency or lifecycle mutation.

### R4 — Each terminal mutation detects its own empty epoch

After a guarded terminal update changes one assignment from open to closed, the shared
producer runs in that same transaction:

```sql
SELECT count(*) FROM assignments
WHERE holderKey = ?1 AND state = 'open'
```

The guarded update proves that the count before the update was one-or-more. A zero result
therefore proves the event itself without a time threshold or a second snapshot. If a
completion returns nonzero, its row has `status='notice-only'`. If completion or
revocation returns zero, the row has `status='open'`. A selected session recipient has a
non-null `actionDeadlineAt` and internal `deadlineWakeId`; the owner-user root has
neither. A nonzero revocation returns without creating a
completion-escalation row or wake. The internal deadline wake uses
`sessionKey=childSessionKey`, `consumer='completion_disposition_deadline'`,
`origin='process:tightbeam'`, `dueAt=actionDeadlineAt`, the deterministic id from R8,
null `assignmentId`, and null `work_item_id`. Its required `sessionKey` is storage
correlation; the internal consumer does not deliver a turn to the child. The count is
per child session, not per work item. The producer stores that historical result as
`remainingOpenAssignments`; later assignment changes do not rewrite it. A session that
starts and remains at zero never enters this seam.

### R5 — Initial routing preserves parent truth and commission separation

For a non-root child, the close transaction calls `Org.effective_parent_in_txn/2` and
copies its exact `session_key` result to `immediateParentSessionKey` and
`parentSessionKey`. It copies the returned source to `parentResolutionSource`. It creates
the parent notice only when that exact row exists,
has `state='active'`, has the stored owner pin, and does not equal the non-root child. It records
`parentRouteStatus='scheduled'`. A missing, inactive, or foreign-owned exact
parent records `parentRouteStatus='unavailable'`, writes
`completion_escalation_undeliverable` with the exact reason
`parent-missing|parent-inactive|parent-owner-mismatch|parent-cycle`. It does not resolve a role or
inspect assignment-opener fields. A null `operationalParent` selects Owner Main inside
the shared resolver; no consumer-local Main fallback exists. A `notice-only` row creates
no replacement notice and remains queryable as a named undeliverable completion.

For an open request, the producer passes that immutable parent snapshot to R9's initial
selector. If the
exact parent is active and owner-matched, recipient rung zero is that session. If it is
retired, R9 walks its stored `spawnedBy` links nearest-first. If it is missing,
foreign-owned, cyclic, or has no eligible same-owner ancestor, R9 selects the owner-user
root. The action notice targets the selected current recipient, while the original
parent fields and `parentRouteStatus` remain unchanged. At the owner-user root, the
producer requires an active, owner-matched personal-Main carrier before it arms the wake.
If that carrier is unavailable, it applies R2's named no-delivery result.

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
`reportToRouteStatus='not-declared'`. Report-to applies only to a completion row. A
revocation empty epoch uses that same closed `not-declared` value, copies no report-to
target, and creates no commission wake. Report-to has no deadline and is never reissued.

The principal already authorized to create the assignment is the only declaration
authority; `--report-to` grants no broader assignment-open authority. A missing,
inactive, or foreign-owned declared session makes `assign` or `dispatch` return
`invalid_report_to` with `reportToSessionKey=<submitted-key>` and commit no assignment,
effect, file, marker, supervision, work-item-bracket, or idempotency result. Replay of a
successful idempotent create returns the original card and cannot change the declaration.
`reopen-assignment` preserves it exactly.

For a root Main holder, the producer takes the root branch before ordinary target
eligibility. It requires the shared resolver's fixed-point result to equal the child key,
records `parentResolutionSource='owner_main'`,
`immediateParentSessionKey=childSessionKey`, `parentSessionKey=childSessionKey`,
`parentRouteStatus='root-self'`, and
creates the self-addressed completion notice. When the close empties Main's slate, R2
and R4 create the retain-only open request; a nonempty result remains `notice-only`. The
producer does not retain Main automatically. Root-self is an explicit root contract, not Main fallback for a child.
After the stored reissue limit, R9 advances the request to the owner-user root through
that same Main stream and changes the current authorized principal from the Main session
to the owner user.

### R6 — Work-item parentage is immutable here

The producer reads `assignments.workItemId` for correlation. It does not write any
`work_items` field, creation-context field, assignment reference, or `Toplines` edge.
Neither exact parent delivery nor explicit report-to changes work-item parentage.

### R7 — Notice delivery uses exact durable targets

The first completion notice or empty-epoch action notice has `wakeId =
completion:<cause-token>:parent-notice:<generation>`, where `cause-token` is
`attest:<attest-id>` or `revocation:<revocation-id>`. A distinct completion report-to
notice has `wakeId = completion:attest:<attest-id>:report-to-notice`. Each uses
`consumer='prompt'`, `origin='process:tightbeam'`, `dueAt=now`, `targetGate=1`, null
`assignmentId`, and null `work_item_id`. A `notice-only` parent wake targets the exact
admitted `parentSessionKey`. An action notice targets the current session recipient, or
targets `Org.personal_session_key(ownerUserId)` as the existing carrier for the
owner-user root. Report-to `sessionKey` is the exact admitted `reportToSessionKey`.
Each wake has null `targetRole`, null `reresolve`, null `reresolveSeed`, and null
`reresolveRung`. Generic role or lineage resolution cannot change that wake's target. A
later deadline can create a new generation with another target only through R8-R9.

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
transaction. It admits a `notice-only` parent message and turn only when the wake remains
pending, equals `currentParentNoticeWakeId`, and the exact parent or root-self row remains
active and owner-pinned. It admits an open action message and turn only when the wake is
current and its membership's typed recipient, recipient generation, and reissue count
equal the request row. A session recipient must remain active and owner-pinned. An
owner-user recipient must equal `ownerUserId`; its carrier must equal the owner's
personal Main key and remain active and owner-matched. It admits a
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
An owner-user carrier failure writes R15's `owner-root`/`owner-carrier-unavailable`
detail. A generation-0 notice whose typed recipient equals the immutable parent snapshot
writes the `parent` delivery-refusal detail. Any other session action notice writes the
`recipient` detail, and the informational copy writes `report-to`. The request remains
open at the owner-user root if its carrier fails; the owner retains read and disposition
authority, and no higher principal exists.

If the exact target remains eligible but the wake is no longer current, a still-pending
historical action wake is canceled with `superseded` and the current action wake as its
replacement, or with `target_unresolvable` when no replacement exists. If the request is
terminal, a still-pending action or report-to wake is canceled with
`obligation_disposed` and the terminal `completion_transition`. These are recovery
guards for inconsistent residue; ordinary transitions already cancel the wakes in their
own transaction.

### R8 — Stable request and retry dedupe

`dedupeKey` never changes. Each action generation uses deterministic wake ids:

```text
completion:<cause-token>:parent-notice:<generation>
completion:attest:<attest-id>:report-to-notice
completion:<cause-token>:deadline:<generation>
```

The row stores the current action generation, current typed recipient, recipient
generation, recipient reissue count, frozen recipient reissue limit, current deadline
wake id, nullable current action-notice wake id, and nullable one-shot report-to wake id.
Each transition to `acknowledged`, `retained_root`, or `superseded` cancels or consumes
the pending deadline and clears both `deadlineWakeId` and `actionDeadlineAt`. It
preserves the last typed recipient, recipient counters, notice ids, and wake membership
as terminal audit truth.
It copies `Application.get_env(:tightbeam, :prod_limit, 3)` when the empty epoch opens and
refuses a non-integer or negative value before mutation. The copied value does not change
after restart or a later config edit. Tightbeam reuses the existing cancellation reasons
and the stable `completion_transition` source/disposition classification:

- requester `{kind='process', id='tightbeam:wake-scheduler'}` can use existing reason
  `target_unresolvable` only for R7's exact delivery refusal;
- requester `{kind='process', id='tightbeam:completion-escalation'}` can use existing
  reasons `superseded`, `obligation_disposed`, and `target_unresolvable`; its
  `target_unresolvable` authority applies only when R8 cannot arm a replacement action
  notice during deadline reissue;
- reason `superseded` uses causal source kind `wake`, names the replacement action wake,
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

A deadline transaction CASes the current `deadlineWakeId`. It computes the next action
generation. When it arms a replacement notice, it writes the existing
`completion_escalation_reissued` observability mirror with the resulting recipient
generation, reissue count, and typed recipient. If it reaches the owner-user root but
cannot arm the carrier, it writes only R15's typed owner-carrier-undeliverable marker;
it does not claim that a notice was reissued. It never reissues or replaces the
report-to notice.

For one recipient, the first notice has `recipientReissueCount=0`. While the count is
less than `recipientReissueLimit` and the same session remains active and owner-matched,
the deadline transaction increments the count and arms one replacement notice plus one
replacement deadline for that same recipient. When the count equals the limit, or when
the session is no longer eligible, the transaction advances under R9 instead of
reissuing. A recipient change increments `recipientGeneration`, resets
`recipientReissueCount=0`, and arms one first notice for the new recipient. Reaching the
owner-user root arms one first owner notice and no replacement deadline.
Notice delivery does not reset either counter and does not acknowledge the request.
Only R11-R13 terminalize it; a later empty epoch starts a new row with fresh counters.

While the old action notice remains current and pending, the transaction cancels it with
`superseded` pointing to the replacement action wake. A `replacement` outcome is valid
only when the replacement membership names the same completion and the next action
generation. If no replacement notice can be armed, the transaction cancels a pending old
notice with `target_unresolvable` and `no_replacement`. The transaction updates the row
to the new generation and recipient fields, sets the current action-notice and deadline
fields to null, and marks the source deadline fired through
`Wakes.fire_internal_in_txn/4`. A refused cancellation or deadline-fire CAS rolls back
each replacement row, lifecycle row, completion-row change, and deadline consumption.

A stale or replayed deadline writes and arms zero rows. Database serialization gives a
delivery-versus-reissue race two results: delivery commits first and the old wake is no
longer pending, or reissue cancels first and R7 refuses the old callback. No two
action-notice generations for one request remain pending after commit. Each reissued action
notice uses R7's exact-target wake fields. `turns.wakeId UNIQUE` prevents a duplicate
turn for one action-notice generation (`ledger.ex:1-18,99-148`). Membership history makes the
visited recipient set and each count reset replayable without mutable hidden state.

### R9 — Deadline reissues; it does not judge

When the internal deadline fires, the transaction re-reads the request, child session,
child open-assignment count, current typed recipient, immutable parent snapshot,
historical recipient memberships, and source wake.
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
- request remains open, child remains active and empty, current recipient is an eligible
  session, and its reissue count is below the stored limit: reissue the same request to
  that session and arm the next deadline;
- request remains open, child remains active and empty, and the current session is
  ineligible or has exhausted its reissue limit: walk `spawnedBy` nearest-first from that
  session. An ineligible current session writes R15's exact recipient-undeliverable
  marker; limit exhaustion does not. Skip retired same-owner rows. Select the first active same-owner session not
  present in historical recipient membership and not equal to the child. A missing link,
  foreign-owner link, nil link, child link, repeated key, or exhausted finite row set ends the session walk and selects the
  owner user. Do not inspect roles, assignment openers, report-to, or prompt text;
- current recipient is the owner user: no deadline exists, so this callback state is
  inconsistent residue and writes or arms zero rows.

Each successful branch marks the source deadline fired through
`Wakes.fire_internal_in_txn/4` in the same transaction. A branch that moves the request
to `superseded` writes its observability mirror and cancels any pending parent or
report-to notice through `obligation_disposed` with source and
disposition `completion_transition`. A refused cancellation or deadline-fire CAS
rolls back the request transition and deadline consumption.

Elapsed time never means a recipient is incapable or that retire is correct. The stored
count only bounds how long one session remains the current recipient. Advancing changes
the authorized mind, not the requested decision. At the owner-user root, the request
remains open until an authorized disposition, a new assignment, or retirement settles
it. Ordinary at-least-once wake delivery keeps the root notice pending until durable
acceptance while its permanent carrier remains eligible. R7 records and cancels a root
notice if corrupt state later makes that carrier ineligible. The completion producer
schedules no infinite root reminders.

### R10 — Assignment open or reopen supersedes in its transaction

Every successful `assign` and `dispatch` insert and every successful
`reopen-assignment` transition for a child session calls the one
`supersede_open_for_assignment_in_txn/3` seam. An insert calls it after the assignment,
effect, and file rows exist and before the supervision transition
(`assignments.ex:918-1057`). A reopen calls it after the guarded assignment update
changes the outcome to `open` and before the
supervision transition. The seam changes an open completion request for that child to
`superseded/new-assignment`. It first writes the typed completion transition and its
lifecycle observability mirror. It then cancels the deadline and any pending parent or
report-to notice through `obligation_disposed`, with source and disposition
`completion_transition`, in that same transaction. The row stores the opened or
reopened assignment id and transaction timestamp as `supersededAt`. The lifecycle row
records that id and the typed principal that opened or reopened the assignment. A
refused cancellation raises and rolls back the assignment insert or guarded reopen
update and the request transition.

If assignment opening or reopening and a disposition race, database serialization
permits one result:

- opening or reopening wins: disposition returns `request_superseded` and enacts no
  disposition;
- retain wins: the later assignment commits through the existing open path;
- retire wins: the later assignment fails the existing active-holder interlock;
- park wins: the future park contract defines and enforces the assignment interlock.

### R11 — Explicit acknowledgment and authorization

`completion-disposition <completion-id> --decision retain|park|retire` accepts only a
session or user principal. Process and remedy principals are refused.

A session principal is authorized when it is active at action time, has the stored
owner pin, is not the child, and its exact session key equals
`currentRecipientSessionKey`. A report-to recipient, sibling, assignment opener, role
holder, unvisited ancestor, or previous recipient gains no authority. Advancing the
recipient atomically removes the prior session's authority and grants it to the new
session. A user principal is authorized only when it owns the child; the owner can act
at every rung. An admin from another owner can read the record under R15 but cannot
choose a lifecycle disposition.

One self-disposition exception exists. Before a root Main request advances, the exact
active root Main holder is its current session recipient and can retain its own row. Its
`park` and `retire` calls reach the root refusal below. After the request advances to the
owner-user root, Main loses session authority and the owner user remains authorized. No
other child session passes authorization for its own request.

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
   check precedes request-state disclosure. An active, owner-pinned current
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
Retirement interruption calls the shared terminal seam after each guarded revocation in
its deterministic assignment order. Earlier revocations with work remaining create no
row. The revocation that changes the count to zero creates one open row, and the later
retirement acknowledgment seam terminalizes that same row as `acknowledged/retire` in
the transaction before session retirement. Its initially armed notice and deadline are
canceled in that transaction; no request becomes externally visible as open.

If retirement wins before a concurrent completion, the assignment becomes revoked, the
later completion loses with `assignment_closed`, and the zero-producing revocation row
records the retirement cause and acknowledgment. If completion wins first, the same
retire transaction acknowledges that completion row. No request remains open for a
retired child.

### R14 — Receipt and action acknowledgment remain distinct

The read projection derives `request.receipt` from `currentParentNoticeWakeId`.
`routing.parent.receipt` derives from the generation-0 parent-notice membership only
when its recipient is the immutable parent snapshot; otherwise it is `not-created`.
`reportTo.receipt` derives from `reportToNoticeWakeId`, or from that immutable parent
receipt when `reportToRouteStatus='shared-parent'`. Each wake-backed receipt maps rows
without inference:

- null wake id -> `state='not-created'`, `turnSeq=null`;
- pending wake and no turn -> `state='pending'`, `turnSeq=null`;
- canceled wake and no turn -> `state='canceled'`, `turnSeq=null`;
- existing turn -> its exact `queued|running|delivered|canceled|failed|failed_unknown`
  status and sequence;
- fired wake and no turn -> `state='inconsistent'`, `turnSeq=null`.

The fired wake row and absent joined turn are the durable evidence for `inconsistent`.
The read path writes no lifecycle event. Repeated reads return the same projection
without mutating `lifecycle_events`.

Earlier action-recipient generations remain available through membership, wake, turn,
and lifecycle rows. They do not overwrite `request.receipt` or the immutable initial
parent receipt. Report-to has one generation.

Receipt does not close an action-needed request. Only R11-R13 do. Conversely, an
authorized action can acknowledge before either notice turn delivers; each pending
notice is canceled through R8's typed seam in the action transaction because its content is
then stale. The joined wake-cancellation row exposes the exact requester, reason, source,
outcome, cause principal, and cancellation time; the receipt state stays a mechanical
projection of wake and turn rows.

### R15 — Observability is durable and replayable

The completion row and joined assignment, attest or revocation, session, wake, and turn
rows are the source of truth. The producer writes these exact lifecycle kinds with
`subject=<completion-id>`:

- `completion_escalation_opened` in the close transaction;
- `completion_escalation_reissued` for each successful generation CAS that arms a
  replacement action notice;
- `completion_escalation_superseded` for each transition to `superseded`;
- `completion_escalation_acknowledged` for each first transition to `acknowledged` or
  `retained_root`;
- `completion_escalation_undeliverable` for an unavailable initial parent, an ineligible
  current recipient, an unavailable owner-user carrier, and each R7 exact-target delivery
  refusal;
- `completion_escalation_cross_owner_lineage` when R5 or R9 observes a foreign-owned
  link; it reports dirt, excludes that link, and routes the open request to the owner-user
  root without granting the foreign owner visibility through that lineage. R15's
  independent admin audit rule remains unchanged;
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
- reissued:
  `generation=<decimal> recipientGeneration=<decimal> recipientReissueCount=<decimal> recipient=<session:session-key|user:user-id> principal=process:tightbeam:completion-escalation`;
- superseded by assignment: `reason=new-assignment`;
- superseded by retired child:
  `reason=child-retired principal=process:tightbeam:completion-escalation`;
- ordinary acknowledged: `decision=<retain|park|retire>`;
- retained root: `decision=retain outcome=retained_root`;
- initial parent unavailable at close:
  `channel=parent resolution=parent-unavailable reason=<parent-missing|parent-inactive|parent-owner-mismatch|parent-cycle> generation=<decimal> principal=process:tightbeam:completion-escalation`;
- current session recipient ineligible at deadline:
  `channel=recipient resolution=recipient-ineligible reason=<recipient-missing|recipient-inactive|recipient-owner-mismatch> generation=<decimal> principal=process:tightbeam:completion-escalation`;
- owner-user carrier unavailable at scheduling or R7 delivery:
  `channel=owner-root resolution=target-unresolvable reason=owner-carrier-unavailable generation=<decimal> principal=process:tightbeam:completion-escalation`;
- parent, session current-recipient, or report-to target refused at R7 delivery:
  `channel=<parent|recipient|report-to> resolution=target-unresolvable reason=target-unresolvable generation=<decimal> principal=process:tightbeam:completion-escalation`;
- cross-owner initial parent:
  `parentSessionKey=<session-key> principal=process:tightbeam:completion-escalation`;
- cross-owner R9 link:
  `recipientPathSessionKey=<session-key> principal=process:tightbeam:completion-escalation`;
- state inconsistent:
  `reason=child-not-active principal=<session:session-key|user:user-id>`;
- retire deferred:
  `reason=critical-lease principal=<session:session-key|user:user-id>`;
- park failed:
  `reason=<park_dependency_unavailable|park_operation_failed> principal=<session:session-key|user:user-id>`.

Observability joins the event subject back to typed rows to project the terminal cause,
child session, cause principal, acting principal, decision, and reason. No decision path
parses prompt or event prose. A `new-assignment` supersede joins
`supersededByAssignmentId` to its typed opener principal.

Every lifecycle marker therefore carries cause and principal without guessing. Opened
joins the attest or revocation cause and its typed principal. Reissued joins the prior
deadline wake and names the completion process. Assignment supersession joins the new assignment
and its typed opener. Acknowledgment joins the terminal completion row and its exactly
one acting principal. `opened`, `reissued`, `superseded`, and `acknowledged` are stable
domain transitions because each remains meaningful if wake scheduling and event-log
storage change. Undeliverable, cross-owner, inconsistent, deferred, and park-failed are
operational observations, not cancellation-authority types. The remaining process markers name the completion process in
their exact detail. The three refused-action markers copy the already-authorized typed
caller into their exact detail at write time. Detail remains observability only; no
authorization, routing, transition, or read-visibility decision parses it.

`completion-notices --status open|all [--session <child>]` returns an owner-matched row
to the owner user, an admin, and the active owner-pinned child. The active owner-pinned explicit
report-to recipient can read its completion copy in every status. For `notice-only`, the
active owner-pinned initial parent can read. For `open`, the active owner-pinned current
session recipient can read. A prior escalation recipient loses read access when the
request advances unless another listed rule grants access. Report-to visibility grants
no disposition authority.

An `acknowledged` or `retained_root` row is also visible to its exact
`actedBySession` only while that same session incarnation remains active and
owner-pinned. Retirement removes that session's read and replay authority. A session
that was current when the owner user acted gains no terminal-read exception. A role, a
replacement incarnation, or a sibling gains no visibility from `actedBySession`.
`--status open` selects only `status='open'`; `all` selects each status.
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

Each entry contains `completionId`, `assignmentId`, nullable `workItemId`, `causeKind`,
`causeId`, nullable `closingAttestId`, nullable `revocationId`, `outcome`,
`childSessionKey`, `causePrincipal`, `currentStatus`, nullable `currentRecipient`,
`recipientGeneration`, `recipientReissueCount`, `recipientReissueLimit`, nullable
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

For an open request, the unstamped current-recipient prompt body is exactly:

```text
Child assignment slate became empty.
completionId=<completion-id>
assignmentId=<assignment-id>
workItemId=<work-item-id-or-none>
childSessionKey=<session-incarnation-key>
causeKind=<attest|revocation>
causeId=<cause-id>
closingAttestId=<attest-id-or-none>
revocationId=<revocation-id-or-none>
outcome=<completed|revoked>
causePrincipal=<session:session-key|user:user-id>
immediateParentSessionKey=<session-key>
parentResolutionSource=<explicit|owner_main>
parentRoute=<effective-parent|parent-unavailable|root-self>
reportToSessionKey=<session-key-or-none>
remainingOpenAssignments=<decimal-count>
actionNeeded=true
recipientPrincipal=<session:session-key|user:user-id>
recipientGeneration=<decimal>
recipientReissueCount=<decimal>
recipientReissueLimit=<decimal>
```

A `notice-only` completion preserves this predecessor prompt byte-for-byte and contains
no recipient fields:

```text
Child completion recorded.
completionId=<completion-id>
assignmentId=<assignment-id>
workItemId=<work-item-id-or-none>
childSessionKey=<session-incarnation-key>
closingAttestId=<attest-id>
outcome=completed
causePrincipal=session:<child-session-key>
immediateParentSessionKey=<session-key>
parentResolutionSource=<explicit|owner_main>
parentRoute=<effective-parent|parent-unavailable|root-self>
reportToSessionKey=<session-key-or-none>
remainingOpenAssignments=<positive-decimal-count>
actionNeeded=false
```

For an ordinary non-root child with an open request, the action prompt appends exactly
this final line:

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
immediateParentSessionKey=<session-key>
parentResolutionSource=<explicit|owner_main>
parentRoute=<effective-parent|parent-unavailable|root-self>
reportToSessionKey=<report-to-session-key>
remainingOpenAssignments=<decimal-count>
actionNeeded=<true|false>
This report is informational. It grants no disposition authority.
```

Assignment `assign`, `dispatch`, and `assignments` JSON adds the camelCase key
`reportToSessionKey`, always present with a string or null. The CLI accepts exactly
`--report-to <session-key>` on `assign` and `dispatch`. Omission stores null. No reopen,
attest, or disposition command accepts this flag.

The read/command JSON object uses camelCase:

```json
{
  "id": "cn_...",
  "dedupeKey": "terminal:attest:att_...",
  "assignmentId": "asg_...",
  "workItemId": "wi_...",
  "childSessionKey": "agent:... s_...",
  "rootMainHolder": false,
  "causeKind": "attest",
  "causeId": "att_...",
  "closingAttestId": "att_...",
  "revocationId": null,
  "outcome": "completed",
  "remainingOpenAssignments": 0,
  "cause": {"bySession": "agent:... s_...", "byUser": null, "principal": "session:agent:... s_..."},
  "routing": {
    "parent": {
      "sessionKey": "agent:... s_...",
      "resolutionSource": "explicit",
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
    "currentRecipient": "session:agent:... s_...",
    "recipientGeneration": 0,
    "recipientReissueCount": 0,
    "recipientReissueLimit": 3,
    "receipt": {"state": "pending", "turnSeq": null},
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

`routing.parent.routeStatus` is `scheduled`, `unavailable`, or `root-self` and describes
only the immutable initial parent snapshot. Prompt `parentRoute` maps those values to
`effective-parent`, `parent-unavailable`, and `root-self`, respectively.
`request.currentRecipient` is the typed
principal that can act at the current rung.
`routing.reportTo` is null when no declaration exists. Otherwise its `routeStatus` is
`scheduled`, `shared-parent`, or `unavailable`. `sharesParentNotice` is true only for
`shared-parent`, and that object's receipt equals the parent receipt. A scheduled
report-to has its own receipt. An unavailable parent or report-to has
`receipt.state='not-created'`. For `notice-only`, `request.status` is `notice-only` and
its deadline, recipient, and action fields are null. For a retained root,
`request.status` is `retained_root`, `decision` is `retain`,
`rootMainHolder` is true, and the acting fields name the explicit caller. For an
ordinary child, `rootMainHolder` is false. The parent object always carries a non-null
`sessionKey` and `resolutionSource='explicit'|'owner_main'`. For missing `workItemId`,
JSON uses null and prompt text uses `none`. An `acknowledged`, `retained_root`, or
`superseded` request has `deadlineAt=null`; it preserves the last typed recipient and
recipient counters as terminal audit fields. No key is conditionally omitted.

### R17 — Compatibility and migration

Current v15 already creates `completion_escalations` and
`completion_escalation_wakes`, registers their schema after `Assignments`, stores
`assignments.completionReportToSessionKey`, and admits `completion_transition` in the
closed `wake_cancellations` source/disposition checks. G1/G2 widens the two completion
tables with typed terminal-cause and recipient-routing fields; it does not add a second
rail or cancellation value. SQLite cannot widen those existing shapes through
`CREATE TABLE IF NOT EXISTS`. Under Mike's waiver, Schema
reserves successor stamp `coordination-fabric-v1-phase1-v16` after exact current-main
stamp `coordination-fabric-v1-phase1-v15`. A database carrying v15 or any other stamp is
refused by name before schema-module DDL or feature queries run. Tightbeam does not
alter, rebuild, sniff, copy, or repair it. The operator moves it aside and lets this
build create a fresh database, as the existing shape refusal instructs
(`schema.ex:88-98,1817-1914`).

The release migrates and backfills no rows. Recreation starts with no assignments,
completion rows, or historical notices. The first admitted terminal transition in the
recreated database is the first eligible cause. Historical zero-session reconciliation
is outside this runtime producer. Downgrade means restoring a database created by
the downgraded build; a build that does not carry the exact stamp refuses this database.
Preserve the registered internal consumer beside `effort_probe` and `effort_deadline` in
the gateway child specification, not in `Wakes` (`gateway.ex:292-300`).

The gateway and Rust CLI retain `completion-notices`, `completion-disposition`, and
optional `reportToSessionKey`/`--report-to` on assignment creation. This revision extends
their existing prompt and JSON projections without adding a command. Because
the package is pre-1.0 and currently requires exact CLI/gateway versions, the release
bumps both together (`cli_compatibility.ex:1-38`). Old Clawline clients remain compatible
because the wire frame is unchanged.

### R18 — One mutation seam

`Tightbeam.Productions.CompletionEscalation` is the only module that inserts or updates
`completion_escalations` or inserts `completion_escalation_wakes`. Assignment completion
and revocation call its one `open_terminal_in_txn` function immediately after their
guarded close. Assignment open/reopen and retirement call its other in-transaction
functions. The deadline consumer and public verbs delegate to it. A source-closure test
fails if production SQL mutates either table anywhere else or if an admitted terminal
path bypasses the shared function.

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

Each admitted terminal path runs the producer inside the same transaction. A completion
cannot lack its dependent record. A zero-producing revocation cannot lack its request
and either its first admitted notice/membership or R2's named root-carrier failure. A nonzero revocation creates none of those
rows. Every open session-recipient request has a deadline and deadline membership; an
owner-user-root request deliberately has no deadline. `parent-unavailable` preserves
the initial routing failure while R9 finds the current action recipient. Report-to
omission or unavailability never changes the action route. No recovery sweep is required
for this edge. The ordinary wake scheduler supplies crash recovery after commit.

## Architecture

### Record shape

The recreated `assignments` table retains exactly:

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
  causeKind                 TEXT NOT NULL CHECK (causeKind IN ('attest','revocation')),
  causeId                   TEXT NOT NULL,
  assignmentId              TEXT NOT NULL REFERENCES assignments(id),
  workItemId                TEXT NULL REFERENCES work_items(id),
  childSessionKey           TEXT NOT NULL REFERENCES sessions(sessionKey),
  remainingOpenAssignments INTEGER NOT NULL CHECK (remainingOpenAssignments >= 0),
  closingAttestId           TEXT NULL UNIQUE REFERENCES attests(id),
  revocationId              TEXT NULL UNIQUE REFERENCES assignment_revocations(id),
  outcome                   TEXT NOT NULL CHECK (outcome IN ('completed','revoked')),
  causeBySession            TEXT NULL REFERENCES sessions(sessionKey),
  causeByUser               TEXT NULL REFERENCES users(userId),
  ownerUserId               TEXT NOT NULL REFERENCES users(userId),
  rootMainHolder            INTEGER NOT NULL CHECK (rootMainHolder IN (0,1)),
  immediateParentSessionKey TEXT NOT NULL,
  parentSessionKey          TEXT NOT NULL,
  parentResolutionSource    TEXT NOT NULL CHECK (
    parentResolutionSource IN ('explicit','owner_main')
  ),
  parentRouteStatus         TEXT NOT NULL CHECK (
    parentRouteStatus IN ('scheduled','unavailable','root-self')
  ),
  reportToSessionKey        TEXT NULL REFERENCES sessions(sessionKey),
  reportToRouteStatus       TEXT NOT NULL CHECK (
    reportToRouteStatus IN ('not-declared','scheduled','shared-parent','unavailable')
  ),
  generation                INTEGER NOT NULL DEFAULT 0 CHECK (generation >= 0),
  currentRecipientSessionKey TEXT NULL REFERENCES sessions(sessionKey),
  currentRecipientUserId    TEXT NULL REFERENCES users(userId),
  recipientGeneration       INTEGER NULL CHECK (recipientGeneration >= 0),
  recipientReissueCount     INTEGER NULL CHECK (recipientReissueCount >= 0),
  recipientReissueLimit     INTEGER NULL CHECK (recipientReissueLimit >= 0),
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
  CHECK ((causeBySession IS NOT NULL) != (causeByUser IS NOT NULL)),
  UNIQUE (causeKind, causeId),
  CHECK (dedupeKey = 'terminal:' || causeKind || ':' || causeId),
  CHECK (
    (causeKind = 'attest' AND causeId = closingAttestId
      AND closingAttestId IS NOT NULL AND revocationId IS NULL
      AND outcome = 'completed' AND causeBySession = childSessionKey)
    OR
    (causeKind = 'revocation' AND causeId = revocationId
      AND revocationId IS NOT NULL AND closingAttestId IS NULL
      AND outcome = 'revoked' AND remainingOpenAssignments = 0
      AND reportToSessionKey IS NULL AND reportToRouteStatus = 'not-declared'
      AND reportToNoticeWakeId IS NULL)
  ),
  CHECK (
    (parentRouteStatus = 'scheduled' AND rootMainHolder = 0
      AND parentSessionKey IS NOT NULL
      AND parentSessionKey IS immediateParentSessionKey
      AND (
        remainingOpenAssignments = 0
        OR currentParentNoticeWakeId IS NOT NULL
      ))
    OR
    (parentRouteStatus = 'unavailable' AND rootMainHolder = 0
      AND parentSessionKey IS immediateParentSessionKey
      AND (
        (remainingOpenAssignments >= 1 AND currentParentNoticeWakeId IS NULL)
        OR remainingOpenAssignments = 0
      ))
    OR
    (parentRouteStatus = 'root-self' AND rootMainHolder = 1
      AND parentResolutionSource = 'owner_main'
      AND immediateParentSessionKey = childSessionKey
      AND parentSessionKey = childSessionKey
      AND (
        remainingOpenAssignments = 0
        OR currentParentNoticeWakeId IS NOT NULL
      ))
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
      AND currentRecipientSessionKey IS NULL AND currentRecipientUserId IS NULL
      AND recipientGeneration IS NULL AND recipientReissueCount IS NULL
      AND recipientReissueLimit IS NULL
      AND decision IS NULL AND actionDeadlineAt IS NULL AND deadlineWakeId IS NULL
      AND actedBySession IS NULL AND actedByUser IS NULL AND actedAt IS NULL
      AND supersededReason IS NULL AND supersededByAssignmentId IS NULL AND supersededAt IS NULL
    OR status = 'open'
      AND remainingOpenAssignments = 0
      AND ((currentRecipientSessionKey IS NOT NULL) != (currentRecipientUserId IS NOT NULL))
      AND recipientGeneration IS NOT NULL AND recipientReissueCount IS NOT NULL
      AND recipientReissueLimit IS NOT NULL
      AND (
        (currentRecipientSessionKey IS NOT NULL
          AND currentParentNoticeWakeId IS NOT NULL
          AND actionDeadlineAt IS NOT NULL AND deadlineWakeId IS NOT NULL)
        OR
        (currentRecipientUserId = ownerUserId
          AND actionDeadlineAt IS NULL AND deadlineWakeId IS NULL)
      )
      AND decision IS NULL
      AND actedBySession IS NULL AND actedByUser IS NULL AND actedAt IS NULL
      AND supersededReason IS NULL AND supersededByAssignmentId IS NULL AND supersededAt IS NULL
    OR status = 'acknowledged'
      AND rootMainHolder = 0
      AND remainingOpenAssignments = 0
      AND decision IS NOT NULL AND actionDeadlineAt IS NULL AND deadlineWakeId IS NULL
      AND ((actedBySession IS NOT NULL) != (actedByUser IS NOT NULL)) AND actedAt IS NOT NULL
      AND supersededReason IS NULL AND supersededByAssignmentId IS NULL AND supersededAt IS NULL
    OR status = 'retained_root'
      AND rootMainHolder = 1
      AND remainingOpenAssignments = 0
      AND decision = 'retain' AND actionDeadlineAt IS NULL AND deadlineWakeId IS NULL
      AND ((actedBySession IS NOT NULL) != (actedByUser IS NOT NULL)) AND actedAt IS NOT NULL
      AND supersededReason IS NULL AND supersededByAssignmentId IS NULL AND supersededAt IS NULL
    OR status = 'superseded'
      AND remainingOpenAssignments = 0
      AND decision IS NULL AND actionDeadlineAt IS NULL AND deadlineWakeId IS NULL
      AND actedBySession IS NULL AND actedByUser IS NULL AND actedAt IS NULL AND supersededAt IS NOT NULL
      AND (
        (supersededReason = 'new-assignment' AND supersededByAssignmentId IS NOT NULL)
        OR
        (supersededReason = 'child-retired' AND supersededByAssignmentId IS NULL)
      )
  ),
  CHECK (
    status = 'notice-only'
    OR (
      ((currentRecipientSessionKey IS NOT NULL) != (currentRecipientUserId IS NOT NULL))
      AND recipientGeneration IS NOT NULL
      AND recipientReissueCount IS NOT NULL
      AND recipientReissueLimit IS NOT NULL
      AND (currentRecipientUserId IS NULL OR currentRecipientUserId = ownerUserId)
      AND (
        currentRecipientSessionKey IS NULL
        OR (rootMainHolder = 1 AND currentRecipientSessionKey = childSessionKey)
        OR (rootMainHolder = 0 AND currentRecipientSessionKey != childSessionKey)
      )
    )
  )
);
CREATE INDEX completion_escalations_child_status
  ON completion_escalations(childSessionKey, status);
CREATE INDEX completion_escalations_assignment
  ON completion_escalations(assignmentId);
CREATE UNIQUE INDEX completion_escalations_one_open_child
  ON completion_escalations(childSessionKey) WHERE status = 'open';

CREATE TABLE completion_escalation_wakes (
  wakeId                 TEXT PRIMARY KEY REFERENCES wakes(wakeId),
  completionId           TEXT NOT NULL REFERENCES completion_escalations(id),
  generation             INTEGER NOT NULL CHECK (generation >= 0),
  kind                   TEXT NOT NULL CHECK (kind IN ('parent-notice','report-to-notice','deadline')),
  recipientGeneration    INTEGER NULL CHECK (recipientGeneration >= 0),
  recipientReissueCount  INTEGER NULL CHECK (recipientReissueCount >= 0),
  recipientSessionKey    TEXT NULL REFERENCES sessions(sessionKey),
  recipientUserId        TEXT NULL REFERENCES users(userId),
  CHECK (
    kind = 'report-to-notice'
      AND generation = 0
      AND recipientGeneration IS NULL AND recipientReissueCount IS NULL
      AND recipientSessionKey IS NULL AND recipientUserId IS NULL
    OR
    kind = 'parent-notice'
      AND (
        (generation = 0
          AND recipientGeneration IS NULL AND recipientReissueCount IS NULL
          AND recipientSessionKey IS NOT NULL AND recipientUserId IS NULL)
        OR
        (recipientGeneration IS NOT NULL AND recipientReissueCount IS NOT NULL
          AND ((recipientSessionKey IS NOT NULL) != (recipientUserId IS NOT NULL)))
      )
    OR
    kind = 'deadline'
      AND recipientGeneration IS NOT NULL AND recipientReissueCount IS NOT NULL
      AND recipientSessionKey IS NOT NULL AND recipientUserId IS NULL
  ),
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

`immediateParentSessionKey` and `parentSessionKey` deliberately have no session foreign
key. They are immutable diagnostic copies of the shared resolver's selected effective
parent key, which can name a missing row under R5. `parentResolutionSource` preserves
whether selection used the explicit stored parent or Owner Main. Their checks still require the two copies to match for
an ordinary child. `childSessionKey`, `causeBySession`, and `reportToSessionKey` retain
their session foreign keys because each must name an existing row when stored.

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
5. Call `CompletionEscalation.open_terminal_in_txn/4` with the attest cause.
6. Arm the existing work-item slate bracket.
7. Derive the current disposition liveness trigger.
8. Commit the existing supervision terminal-disposition transition.
9. Cancel the effort check-in through its existing typed seam.
10. Append the existing completion and assignment markers.
11. Commit.

Steps 5-10 preserve the current relative order of steps 6-10. The shared producer
enters immediately after the guarded close so each later failure rolls back the
completion row and each admitted initial notice with the attest and
assignment close
(`assignments.ex:1130-1200`).

Revocation uses this total order in the existing revocation transaction:

1. Read and authorize the open assignment generation.
2. Insert the revocation and revocation-generation rows.
3. Guarded-update the assignment to `closed/revoked` and verify one changed row.
4. Fetch the closed assignment.
5. Call the same `open_terminal_in_txn/4` with the revocation cause.
6. Run the existing work-item slate, supervision, interruption, and lifecycle effects in
   their current relative order.
7. Commit.

The shared function performs R4's count before deciding whether to insert. A nonzero
revocation returns without a completion row or wake. A zero-producing revocation commits
its request with the revocation and close. A later failure in either branch rolls the
entire revocation transaction back.
The 0.2 line has no active-surrender transaction to join. If that mutation returns, its
separately reviewed implementation must call the same terminal seam and add the third
cause shape and fixtures before release.

The shared producer cannot reject a truthful terminal mutation because delivery is unavailable.
If the exact parent is unavailable, it commits `parent-unavailable` and the lifecycle
record. A database
write failure rolls back the entire terminal transition, as any failure inside the
existing atomic close does.

Assignment opening by `assign` or `dispatch` calls the supersede seam after it inserts
the assignment, effect, and file rows and before it commits the supervision transition.
`reopen-assignment` calls the same seam after its guarded update changes the assignment
to `open` and before it commits the supervision transition. Retirement calls the
acknowledgment seam before `Org.retire_in_txn/4` changes the session state and performs
typed target-wake cancellation. Before that transaction, Gateway resolves the owner and
serialized acting principal from `call.principal` under R3. These calls share the caller's
transaction.

### Deadline consumer

Preserve the internal wake consumer, `completion_disposition_deadline`, in the Gateway
child specification. Its handler calls `CompletionEscalation.reissue_in_txn/2`. The
current wake id is the CAS token. The handler marks the source deadline fired, updates or
closes the request, and arms replacement wakes in one transaction. It runs no model and
invokes no session lifecycle action.

### Typed cancellation integration

Keep `EventLog.lifecycle_in_txn/4` unchanged. Lifecycle rows mirror completion events for
observability; cancellation validation does not use their ids or parse their detail.

Preserve the existing `Wakes` integration: source and disposition kind
`completion_transition`; process requester `tightbeam:wake-scheduler` can use existing
reason `target_unresolvable` for R7 completion delivery; let process requester
`tightbeam:completion-escalation` use existing reasons `superseded`,
`obligation_disposed`, and `target_unresolvable` for R8 production; retain only the
exact compatibility pairs in R8. For `obligation_disposed`, the validator joins the
source/disposition completion id to `completion_escalations`, proves a typed terminal
state and its required terminal fields, and proves that the canceled wake belongs to
that completion. For a `superseded` replacement, it proves that the replacement
membership names the same completion, the next generation, and kind `parent-notice`.
For `target_unresolvable`, the existing `scheduler_delivery` source validator requires
its source id to equal the canceled wake id and a completion membership. The
`tightbeam:wake-scheduler` pair admits a delayed R7 callback from either exact completion
channel. The `tightbeam:completion-escalation` pair admits only R8's pending historical
action notice when reissue cannot arm its replacement. A completion cancellation
command that fails one check returns `false`; each completion caller converts `false`
to a transaction failure. Existing reason meanings and every unrelated requester and
compatibility pair remain unchanged (`wakes.ex:290-352,478-516,599-606,651-789`).

Preserve `Wakes.fire_internal_in_txn/4` as the wake-owned CAS that changes one pending wake
with the expected internal consumer to `fired` and sets `firedAt`. It returns `true` only
when one row changes. The completion producer uses this seam for deadline consumption;
it never updates `wakes.state` directly.

### Exact implementation surfaces

- Extend `lib/tightbeam/productions/completion_escalation.ex` with the shared terminal
  seam, typed current-recipient state, bounded reissue, and R9 walk.
- Call that terminal seam from completion and revocation transactions in
  `lib/tightbeam/assignments.ex`; preserve existing report-to, open/reopen, and
  retirement seams.
- Recreate the v16 completion tables through `lib/tightbeam/schema.ex`; preserve the
  existing registration point and shape-refusal policy.
- Extend existing completion-linked delivery in `lib/tightbeam/gateway.ex` for typed
  session and owner-user recipients; preserve exact non-reresolving wake targets and the
  existing deadline consumer.
- Preserve existing cancellation pairs in `lib/tightbeam/wakes.ex` and EventLog's
  insertion contract; add no reason, source, disposition, or lifecycle kind.
- Extend the existing read/action projections and prompt payloads in Gateway and the Rust
  CLI. Preserve command names, report-to flags, typed retirement principal, and wire
  frame.
- Extend existing `JobTrace` completion entries with R15's cause and recipient fields;
  keep lifecycle detail opaque and preserve its ranks.
- Extend `test/completion_escalation_test.exs` and the source-closure assertion with
  A25-A28 and the amended G2 cases.

No source edit is authorized by this artifact. These are handoff surfaces for a later,
independently reviewed implementation assignment.

## Acceptance

Each acceptance case uses the real SQLite DB, real assignment handler, real wake store,
real gateway delivery transaction, and real turn ledger. A hand-written notification
object is not a fixture.

Traceability is two-way: R1→A1,A2,A4,A12,A25; R2→A2,A3,A8,A25; R3→A5,A14,A21,A25; R4→A1,A2,A4,A25,A28; R5→A5-A8,A23,A24;
R6→A7,A19; R7→A6,A8-A10,A17,A23; R8→A4,A10-A14,A17,A26; R9→A6,A8,A11,A23,A24,A27; R10→A12;
R11→A11,A13,A14,A16,A24,A26; R12→A13-A15,A24; R13→A14; R14→A10,A17,A18;
R15→A5,A6,A8,A11-A14,A18,A22-A27; R16→A2,A8,A24,A25; R17→A20,A25; and R18→A21,A25. Each acceptance
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

Given `C` has an active exact parent and a distinct explicit report-to, run six
fixtures in which a temporary SQLite trigger aborts the generation-0 action notice, the
generation-0 deadline, the report-to notice, or each corresponding membership insert.
Run one fixture for each of those six inserts. When
`C` files completion in any fixture, then the attest, assignment close, completion
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

Given completion and revocation race for the same open assignment generation, exactly
one guarded close wins. If completion wins, its attest-cause row commits and revocation
returns `assignment_closed` without a revocation row. If revocation wins, its
revocation-cause row commits and completion returns `assignment_closed` without an
attest row. The winner's post-close count alone determines `notice-only`, `open`, or no
revocation escalation row. No race produces two terminal causes or two open requests.

Given `C` has two open assignments and concurrent terminal calls close different
assignments, serialize one completion and one revocation in both commit orders. The
first committed close observes one remaining assignment. If it is the completion, it
creates one `notice-only` row; if it is the revocation, it creates no escalation row.
The second committed close alone observes zero and creates the one open empty-epoch
request for its terminal cause. Exactly one request is open, and no lost update,
duplicate empty epoch, or partial-index conflict occurs.

### A5 — Parent routing and recorded cause

Given `C.operationalParent=P`, `P` is active and owner-matched, and the assignment omits
`--report-to`, when `C` completes, then the record stores `P` in both parent snapshot
fields and records `parentResolutionSource='explicit'`,
`parentRouteStatus='scheduled'` and
`reportToRouteStatus='not-declared'`, and stores the exact closing attest, assignment,
work item, outcome, child incarnation, cause session, and owner. Exactly one parent
notice targets `P`; neither `openedBySession` nor `openedByUser` creates another notice.
The opened lifecycle event and typed `work-item-trace` entry carry the same completion
id, closing attest, child, cause principal, and work item. The trace entry has
`type='completion_escalation'`, `phase='opened'`, `at=createdAt`, and the R15 id. The
lifecycle row has `kind='completion_escalation_opened'`,
`subject=<completion-id>`, null detail, and a paired
`completion_escalation_event` trace entry.

### A6 — Dead initial parent preserves truth and the request climbs

Given selected explicit parent `P1` is retired and same-owner ancestor `P2` and owner Main
`M` are active, when `C` completes, then the row preserves `P1`, records
`parentRouteStatus='unavailable'`, creates no notice for `P1`, selects `P2` as current
recipient generation 0, and writes the exact parent-inactive undeliverable marker with
R15's parent channel detail. It does not select `M` while `P2` remains eligible.
Given `P1` is initially active
but retires after close and before delivery while `P2` and `M` remain active, when the
wake fires, then the delivery transaction cancels that exact wake with
`target_unresolvable`, inserts no message or turn, and writes R15's exact parent
delivery-refusal detail. When the current deadline fires, one transaction selects `P2`,
increments recipient generation, resets its reissue count, and arms the replacement
notice and deadline. The owner user can read and disposition the open request throughout.

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

Given a non-root child has a null stored parent and an eligible Owner Main, when
completion commits, then the record targets that Main, stores
`parentResolutionSource='owner_main'`, and does not take the unavailable path. Given the
selected explicit parent is missing, inactive, or foreign-owned, then completion records
`parentRouteStatus='unavailable'`, writes
the exact R5 reason, creates no notice for that target, and leaves an empty-slate request
open and queryable. R9 selects the nearest eligible same-owner ancestor or the owner-user
root as its current recipient; a session recipient has a deadline and an owner-user-root
recipient does not. `routing.parent.receipt.state='not-created'` continues to describe
the immutable initial route.
The missing-parent fixture runs with `PRAGMA foreign_keys=ON`, copies the dangling
effective-parent key into both diagnostic parent fields, and commits successfully.
Given a non-root child resolves to itself, then the row records
`parentRouteStatus='unavailable'` with `parent-cycle`, sends no notice to the child, and
selects the owner-user root.

Given the selected Owner Main and therefore the owner-user wake carrier is missing or
inactive in corrupt fixture state, then completion stores the owner user as current
recipient generation 0, leaves current notice and deadline null, and writes the exact
`owner-carrier-unavailable` marker. The owner user can read and disposition the request;
no session principal gains authority and no scheduler invents another carrier.
Given the owner-root notice instead commits while the carrier is active and corrupt
fixture state makes that carrier inactive before delivery, then R7 cancels that notice
with `target_unresolvable`, inserts no message or turn, and writes the same exact
owner-root marker. The request stays open with the owner user as its terminal recipient,
no deadline or higher fallback appears, and the owner retains read and disposition
authority.

No role, opener, or report-to target receives an inferred action notice. Given the child instead
has another open assignment, the row is `notice-only`, has no deadline, and remains
queryable. Given a distinct report-to declaration becomes inactive before close, then
the row records `reportToRouteStatus='unavailable'`, creates no report-to wake, and does
not change the parent result. Given report-to instead names the exact parent and that
row becomes inactive before close, then both routes record `unavailable`; the report-to
route does not record `shared-parent`. Given an admitted parent or report-to retires
after close but before delivery, R7 cancels only that channel's wake with
`target_unresolvable` and writes the exact R15 delivery-refusal detail with the
corresponding channel. A report-to notice never redirects. An open action request can
advance only when its deadline transaction applies R9.

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
selects a pending action-recipient or report-to notice and the exact target retires before the
delivery transaction starts, when the delayed callback runs, then R7 inserts no message
or turn. If the wake is still pending, the same transaction cancels it with existing
reason `target_unresolvable`, source kind `scheduler_delivery`, requester
`tightbeam:wake-scheduler`, and outcome `no_replacement`, and writes R15's exact
delivery-refusal detail for that channel.

### A11 — Four ignored notices advance without deciding

Given an open empty-slate request whose exact active parent `P1` has not acted and whose
stored reissue limit is the default 3, the initial notice records recipient generation 0
and reissue count 0. Deliver that notice without a disposition. When three consecutive
deadlines each fire and each replacement notice delivers without a disposition, then
`P1` has four delivered receipts: the initial notice plus reissues with counts 1, 2, and
3. One next deadline remains armed, and no decision or session lifecycle changes. When that deadline
fires and eligible same-owner ancestor `P2` exists, one transaction selects `P2`, records
recipient generation 1 and reissue count 0, arms `P2`'s first notice and deadline, removes
`P1`'s disposition and read authority, and grants disposition authority to `P2`. The
unchanged request remains open.

Given generation 0 remains pending without a turn because delivery failed, when its
deadline fires, then the same transaction arms generation 1 and its membership, records
them as the replacement outcome while it cancels generation 0, and commits with exactly
one pending notice generation. A replay of the old deadline id cancels nothing and arms
nothing. Given the scheduler selected generation 0 before that transaction, when its
delayed delivery callback starts afterward, the delivery transaction observes that
generation 0 is canceled and no longer current, and inserts no generation-0 message or
turn. If delivery commits first, generation 0 has one turn before generation 1 is armed.

Given the current session recipient is unavailable when the deadline fires, then the
transaction does not spend another reissue on it. It records the delivery failure,
selects the next eligible same-owner unvisited ancestor, or selects the owner-user root
when no such session exists. A pending old notice is canceled through R8. The report-to
notice count remains one or zero exactly as generation 0 established; no report-to
notice is reissued. At the owner-user root, one ordinary at-least-once user notice stays
pending until durable delivery while its permanent carrier remains eligible. No deadline
exists, and the substrate records no
retain, park, or retire decision.

### A12 — Assignment open or reopen supersedes atomically

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

Given completed assignment `A` left completion row `H0` open and `C` has no other open
assignments, when
`reopen-assignment A` commits, then that same transaction changes `A` to `open`, marks
the request `superseded/new-assignment`, stores `A` as `supersededByAssignmentId`,
records the typed reopen principal in the lifecycle row, and performs the same deadline
and notice cancellations. The assignment's immutable report-to declaration does not
change. If any attempted pending-wake cancellation is refused, then the guarded reopen
update, supersede lifecycle row, request transition, and all cancellation rows roll
back, so `A` remains completed and `H0` remains open. When `A` later completes again,
the handler creates row `H1` with the same `assignmentId`, a distinct
`closingAttestId` and `dedupeKey`, and `status='open'`. Row `H0` remains immutable
`superseded/new-assignment` history. Exactly two completion rows exist for `A`, and only
`H1` is open.

### A13 — Retain

Given an open request and authorized current recipient `P`, when `P` chooses retain, then the request
becomes `acknowledged/retain`, records `actedBySession=P`, cancels pending notice/deadline
wakes through typed `obligation_disposed` cancellations sourced from the terminal
`completion_transition`, and changes no session, harness, assignment, or work-item
row. Identical replay by `P` while `P` remains active and owner-pinned returns the same
record. A different choice is refused. If `P` retires first, the same session key cannot
read the terminal row or replay the decision.
Given any attempted pending-wake cancellation is refused, then no acknowledgment or
lifecycle row commits.

### A14 — Retire and race

Given an open request and authorized current recipient `P`, when `P` chooses retire, then request
acknowledgment and the existing retire database transition commit together. Existing
cascade/interruption, typed target-wake cancellation, wire removal, and post-commit reap
run once. The completion deadline and pending notice cancellations point to the
typed terminal `completion_transition`. Given any attempted completion-wake cancellation
is refused, the request, session, assignment, ordinary retirement wakes, and lifecycle
rows remain unchanged. Given retire and completion race before the assignment closes,
either completion wins and retire acknowledges its completion row, or retire wins and
completion returns `assignment_closed` while the zero-producing retirement revocation
row commits directly as `acknowledged/retire`. Exactly one terminal-cause row exists and
no request remains open. Given the target subtree has an active critical lease, when `P`
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
`completion-disposition`, then the exact active owner-pinned current session recipient
and the owner user can act. The explicit report-to recipient, a previous recipient, an
unvisited active same-owner ancestor, assignment opener, owner Main when it is not the
current recipient, ordinary child acting on
its own row, a sibling, an admin user from another owner, a
different-owner session/user, a process principal, a remedy principal, and each retired
session principal are refused without
changing the request. Each refusal code and the R11 precedence is asserted. The read
matrix separately calls `completion-notices` and proves that the owner user, an admin,
the active child, current session recipient, and explicit report-to can read the row while a
previous recipient, undeclared opener, sibling, other ancestor, and every non-admin
different-owner principal receive no row. Given `P` acknowledges retain and later
retires, the exact retired session key `P` cannot read that acknowledged row or replay
the identical retain decision. The owner user and an admin can still read it. The owner
user's identical retain returns `request_not_open` because `actedBySession=P`; it
changes no completion row, lifecycle row, wake, session, harness, assignment, or work
item. A separate terminal fixture with `actedByUser=ownerUserId` proves that the same
owner-user principal can replay its identical decision. A replacement incarnation with
the same role and each sibling cannot read or replay either row.

### A17 — Receipt differs from action

Given an action-recipient or report-to notice turn delivers, then `request.receipt` or
that report-to channel says `state='delivered'` while the request remains open. Given an authorized
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
session lifecycle addressed to the current recipient; the second is intent disposition addressed to
the user owner. Each completion wake carries null `work_item_id` and null
`assignmentId`; the completion row holds its correlations. A later assignment supersedes
the completion request through R10 and cancels the work-item slate wake through its
existing bracket seam. Neither cancellation is authorized by the other mechanism's row.

### A20 — Compatibility and shape refusal

Given a database stamped `coordination-fabric-v1-phase1-v15`, including one whose
`wake_cancellations` table carries the old closed checks, when the new build boots, then
Schema refuses it before any DDL, assignment query, cancellation insert, or completion
producer call. The error names both stamps and says to move the database aside and let it
be recreated. Given an empty database, when the new build boots, then it stamps
`coordination-fabric-v1-phase1-v16` before table creation and creates the new assignment,
cancellation, and completion shapes. A fixture inserts and validates each R8
compatibility pair against the real recreated SQLite schema. The build performs no
ALTER, table copy, data migration, or historical completion backfill. Current ordinary
message/prompt-turn payload goldens remain byte-identical.

### A21 — Closure law

Given the release-candidate source tree, when the AST/source closure test runs, then it
proves that only
`Tightbeam.Productions.CompletionEscalation` mutates `completion_escalations` and
`completion_escalation_wakes`; every assignment completion path and every assignment
revocation path calls its shared in-transaction terminal seam; every assignment-open
path calls its supersede seam; retirement calls its
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
`call.origin`. It also proves that a nonzero revocation leaves no
completion-escalation row, a zero-producing revocation cannot commit without one, and no
initial-zero sweep or activation hook opens a request. It also proves that this revision
adds no active-surrender write, terminal producer branch, cause value, or fixture and
does not weaken the existing surrender-refusal tests.

The closure test also proves that only `Assignments` writes
`completionReportToSessionKey`, only card creation accepts `reportToSessionKey`, and no
path derives it from `openedBySession`, `openedByUser`, a role, or create-verb identity.
It proves that every immutable initial parent target and resolution source equal the
result of `Org.effective_parent_in_txn/2` for the holder in that transaction; only R9's
request-routing walk reads `spawnedBy`, and no path implements a second Main fallback,
that parent/report-to wakes carry no reresolution fields, that report-to never reaches
the disposition authorization branch, and that the completion producer adds no new
cancellation reason or `lifecycle_event` source.

### A22 — Real smoke

Given one real gateway with exact parent `P`, child `C`, distinct explicit report-to `R`,
and same-owner opener `O`, when a real assignment is dispatched with `--report-to R`,
`C` files completion, both notice turns deliver, and `P` retains, then the smoke captures
both actual stored
messages, turns, wakes, the completion row, assignment projection, CLI read
response, visibility results for the R15 matrix, typed opened and acknowledged
`work-item-trace` entries, and retain acknowledgment response. It also captures the
opened and acknowledged lifecycle rows, their
`completion_escalation_event` trace entries, the membership-linked `wake_fired` entries
for the delivered parent and report-to notices, and the membership-linked
`wake_canceled` entry for the still-pending deadline. It proves retain creates no
cancellation row for either fired notice. It proves `R` can read but cannot act and that `O` receives no inferred
delivery. Compare those
outputs to R15-R16 after replacing only generated ids/timestamps. Passing unit tests
without this smoke does not satisfy the rail.

### A23 — Cross-owner lineage fails closed

Given corrupt fixture state points `C.operationalParent` at an active session owned by another
user while the child's owner Main `M` is active, when `C` completes, then the completion
producer writes one `completion_escalation_cross_owner_lineage` event, sends no wake or readable
row to the foreign session or non-admin user through that lineage, records
`parentRouteStatus='unavailable'`, and preserves the foreign
selected effective-parent fact for diagnosis. It selects the owner-user root through
the existing user-wake carrier without granting the foreign session or `M` session
disposition authority.

Given same-owner `P1` is the exact parent, foreign-owner `P2` is its ancestor, and
`P1` retires before delivery, when the notice wake fires, then the delivery transaction
does not deliver to or inspect `P2`. It cancels the exact `P1` wake with
`target_unresolvable` and preserves `P1` as the initial parent target. When the deadline
advances, the walk stops at the foreign link and selects the owner-user root. It inserts
no message or turn for `P2` or a fabricated key. Repeated reads add no lifecycle event
and grant no non-admin cross-owner visibility through that lineage.

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

Given `M` ignores its initial notice plus the stored maximum reissues, when the next
deadline fires, then the request advances once to the owner-user root, stores that typed
recipient and the incremented recipient generation, arms one user notice through the
personal Main carrier, removes the deadline, and removes `M`'s session disposition
authority. The owner user can still choose retain; the substrate chooses nothing.

Given an ordinary non-built-in child `C` has an open completion request, when exact `C`
submits retain, park, and retire in sequence, then each call returns `not_authorized` and
the request, wakes, session, harness, and completion lifecycle-event count remain
unchanged.

### A25 — Revocation detects the same empty epoch

Given child `C` has two open assignments, when an authorized user revokes the first,
then the revocation and close commit without a completion-escalation row or wake because
one assignment remains open. Given `C` has one open assignment, when an authorized user
revokes it, then the revocation row, revocation-generation row, closed assignment, one
open completion-escalation row, its current-recipient notice, and its deadline commit in
one transaction. The row stores `causeKind='revocation'`, the exact revocation id,
`outcome='revoked'`, and `causePrincipal=user:<id>`. A session-principal revocation stores
the exact session principal instead. A forced failure at the first action-notice wake,
the deadline wake, or either corresponding membership insert rolls back the revocation
and close. Replaying the revoked generation creates
nothing. Reopening and revoking again creates one different empty epoch keyed by the new
revocation-generation cause.

### A26 — Retry state survives restart and config change

Given a request copied reissue limit 3 and reached recipient generation 1, reissue count
2, when the gateway restarts and `prod_limit` changes to 1, then the read projection and
next deadline still use stored limit 3. Replaying any consumed deadline creates no row.
One live deadline advances the count once. A concurrent disposition either commits first
and the deadline writes nothing, or the deadline commits first and the disposition
rechecks the new current recipient before authorization. No restart, replay, or race
creates two current recipients or more than one pending current notice.

### A27 — Chain termination and privacy

Given a chain contains retired rows, then R9 skips them nearest-first. Given the next
link is missing, foreign-owned, nil, the child, already visited, or cyclic, then the same deadline
transaction terminates the session walk and selects the owner-user root. It never reads
a foreign row's `spawnedBy` beyond the boundary and never grants a foreign session or
non-admin user delivery, read, or action authority through that lineage. R15's explicit
admin audit read remains available. Membership history records every armed action notice
and deadline with its typed recipient, action generation, recipient generation, and
reissue count. Each selected session rung therefore has both memberships. An owner-root
rung has one notice membership and no deadline; if its carrier is unavailable, the
current completion row and exact undeliverable marker record that selected rung without
inventing either membership. Owner/admin trace can reconstruct the walk after restart
without prompt parsing; no previous recipient can read or act solely because it appears
in that history.

### A28 — Initial-zero is not a proxy transition

Given an active session starts with zero assignments and no terminal mutation runs,
when startup, activation, scheduler, and read paths execute, then none creates an empty
epoch, request, wake, or lifecycle marker. Initial-zero is a different condition that
requires its own evidence, detector, activation boundary, and separately authorized
proposal.

## Open Questions

1. **BLOCKING — park action contract.** The safe park/relaunch/stop-recycle primitive is
   unbuilt and is owned by `wi_6937890c-6ba6-48b7-a9d2-4eb4510fe245`. The completion
   record, notice, read path, retain path, and retire path are separable. The full
   retain/park/retire feature must not release until A15 uses the ratified real park
   interface. This spec does not name that interface.
2. **BLOCKING IMPLEMENTATION GATE — independent successor review.** The predecessor
   remains reviewed history. Current implementation evidence is exact main
   `6ae34287aa4864b8fe6fabfc96166d02b9827a89`. Mike's G1/G2 request changes this spec
   before any implementation reconciliation. No implementation scope can start until
   the product owner opens one different-session review and that reviewer files
   `reviewed-clean` against this candidate's exact artifact hash. On
   `changes-requested`, amend this canonical file first and publish another hash. The
   reviewed artifact retains this gate text; the linked verdict resolves it without
   changing reviewed bytes.
3. **NON-BLOCKING DECIDED EXCLUSION — initial zero.** Accepted decision request
   `dr_d255b817-1541-460e-8549-bc55a9e7aa1f`, with exact recorded rationale delivered
   in `s_904edadd-16b9-41ba-81cf-680eb8c86c3a`, keeps a session that never held an
   assignment outside this revision. It made no one-or-more-to-zero transition. Adding
   it here would widen the scoped request and require a different detector and activation
   boundary. A28 makes the exclusion executable rather than implicit. A future need for
   never-staffed-session escalation requires a separate evidence-backed proposal.
4. **NON-BLOCKING DECIDED EXCLUSION — active surrender.** Later accepted decision
   request `dr_518d5591-57b8-4a73-8aeb-6634afb334a1`, with exact recorded rationale
   delivered in `s_904edadd-16b9-41ba-81cf-680eb8c86c3a`, is authoritative for this
   conflict. Tightbeam 0.2 deliberately deleted active surrender; current Assignments
   closes lifecycle attests as completed, and tests refuse new surrender writes. This
   revision therefore implements completion and revocation only. It neither restores a
   product behavior nor adds dead code for a transition 0.2 cannot emit. Historical
   surrendered rows receive no runtime backfill here. If surrender returns to 0.2, a
   separately authorized amendment must add the third cause, seam call, and fixtures.

Operating pattern taught by this spec: none. The G1/G2 revision does not exist in exact
current implementation source `6ae34287aa4864b8fe6fabfc96166d02b9827a89`. Guidance must not teach it before implementation and release
(wisdom 20 and 21).
