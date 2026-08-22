# Wake delivery conservation

Status: FROZEN FOR FRESH INDEPENDENT REVIEW

Work item: `wi_113d569f-7aff-412b-aec3-0c21f2e87f40`

Source baselines:

- installed Tightbeam 0.1.7 at commit
  `6c13efcbe9e1ae247b8aa7e91a374015c74dc947`;
- original-review `origin/main` at commit
  `ac8651dcb104f312da1c67e0cb7b1abebc640b2b`;
- revision-verification `origin/main` at commit
  `8d0baa789c4aea1513a6d77ed53a6d54d76d1fb6`.

## Spec homing

The canonical specification identity is
`tightbeam-specs/wake-delivery-conservation.md`. Work item
`wi_113d569f-7aff-412b-aec3-0c21f2e87f40` and producer assignment
`asg_3c5b8c9e-0da8-428f-9710-52582557d273` own its revision and review history.
Each review and build handoff shall bind the canonical file by a SHA-256 artifact and
the commit that contains those bytes. Editing occurs only in a writer-owned
`~/.tightbeam/work/<workspace>` clone on a non-main branch; shared checkouts are not
canonical edit surfaces.

This specification has these governing relationships:

- It amends `coordination-fabric-v1.md` for the ordinary prompt-wake act edge while
  preserving that specification's classifier, batcher, delivery-rule, and ceiling
  semantics.
- It amends the fault-bubbling and turn-end portions of `production-machine-v1.md` by
  adding wake outcomes and a separate typed Bubble-notice dedupe identity. The existing
  capable-parent climb and terminal owner alert remain controlling.
- It amends `supervision-v1.md` only with R11's typed GAGGED consumption. The existing
  entitlement and prod ladder remain controlling after that gate.
- It must be read with `escalation-delivery-v1.md`. That specification's notification
  wake producers, `targetGate`, and durable scheduling remain controlling; this
  specification replaces their split post-enqueue fired mark with R1-R4's atomic
  admission seam.
- It supersedes only the Bug A wake-outcome and sender-notice clauses in the reviewed
  S2c retirement amendment, artifact `art_aac9cafc`, while preserving its binding rule:
  queued carrier cancellation, its terminal outcome, and its sender-visible final cause
  commit in the retirement transaction, and retirement creates no automatic retry. The
  S2c managed-process clauses for `wi_a8a7cca0-9642-46e6-b9c5-0e52443d0ab9` remain
  outside this specification.
- `wake-known-unrunnable-recipient-amendment.md` is a proposed sibling amendment. It does
  not govern this specification until its own frozen hash receives the required clean
  review and handoff.

No other specification is superseded. A build that changes one of these relationships
shall amend this canonical file and publish a new content hash before implementation.

## Goal

Tightbeam conserves the intent carried by an ordinary prompt wake from scheduling to
one observable end. A caller can cancel the wake before admission. After admission,
the linked turn either reaches `handled`, enters a bounded retry sequence after a
typed retry-safe failure, or reaches `undeliverable` and starts one logical fault
bubble. The durable history names the wake, each attempt, each admitted turn, the
cause, and the principal that wrote the transition.

Tightbeam also distinguishes a failed carrier turn from agent negligence. Supervision
consumes the failed turn's typed GAGGED evidence before it can issue a negligence prod.
A delayed wake whose premise is continued owner quiescence is invalidated by a later
durable owner activity, not by elapsed-time inference.

This is substrate work. Rows record routing, admission, terminal outcomes, retry
eligibility, and observed activity. Models still decide what a prompt means and what
action to take (wisdom 5-10).

Operating pattern after release: an agent adds `--cancel-on-owner-activity` only to a
delayed self-wake whose premise is continued owner quiescence. The substrate detects the
named activity and invalidates the stale wake. Other wake purposes keep their existing
spelling. R19 binds the CLI-help and operating-manual directive to the implemented,
tested mechanism (wisdom 15-22).

### Authority and evidence custody

The direct owner assignment
`asg_70ab4afc-ac6a-4e50-a2b5-5e828d6ab372` consolidated the sibling failure family into
this work item and required durable intent through handling or explicit cancellation,
typed attempt and handling outcomes, bounded idempotent backoff, capable-parent
escalation, and duplicate prevention
(`att_59034f84-2bdb-4aa9-babc-8e0cbfaca986`). The original incident owner
recorded two canceled wakes that still fired, queued turns stranded by a planned model
swap, and a 24-hour quiescence check that fired after owner activity
(`att_941bbfdc-ccf4-4d1f-be9e-0f5eacf53cc8`,
`att_57ef3b7b-6a69-4561-8141-a9962af99ab3`,
`att_48fa113d-9907-4126-aff5-a1e0449b25e4`). The work-item trace contains four
consecutive failed wake turns, each recorded `wake_fired` before its failed terminal
(turns 10415, 10472, 10476, and 10478).

Recon assignment `asg_0164bb13-c204-4686-97d3-96b50ab0f602` and its verdict
`att_54f4736d-e56f-4528-9b00-07826c29dabe` recorded the same partial state. Its report
artifact `art_b94039d1` names path
`gibson:/home/mike/.tightbeam/work/3d714ecc0498/wake-delivery-lifecycle-recon-2026-08-12.md`
and SHA-256
`6d73e2bd4ccd3001a811428bd45fa66ca7a7a9c61a9de2383152ca88ffb27c99`, but the
exact recorded path and work directory `/home/mike/.tightbeam/work/3d714ecc0498`
returned ENOENT. The original report is unavailable. No durable artifact or archive
pointer resolves to SHA-matching bytes, so this specification treats the artifact bytes
as irrecoverable. It does not reconstruct, quote, or rely on those bytes, and it labels
no transcript-derived text as the artifact. The loss and corrected observation time are
recorded in `att_2a7d2e0a-0886-4a0f-99ea-6912748a7974` and
`att_1190bc05-4c47-46c6-b738-8121f4bc226f`. Artifact `art_c93203f0` is retained only as
integrity evidence because its caller-supplied digest did not match the file digest
(`att_1688d32e-7e18-4ae3-894b-7f7ad7abd4b6`).

Each load-bearing clause below was re-derived from the durable rows and the three source
baselines. Neither missing artifact supplies authority to a requirement.

Independent review `asg_a4e04da0-f7a6-4be4-a102-09f2098628a2` returned the
changes-requested verdict `att_62dcbc5e-8055-41d6-94dc-8a0e42d3ce19`. It found three
blocking gaps: the admission design omitted existing prompt-wake controllers; the
legacy fired-without-turn mapping assigned a failure class to a non-failed outcome; and
the null-turn Bubble design lacked routing context and a durable outcome cursor. This
revision closes those gaps in R1-R4, R5, R9, R17-R18, the Architecture, A6, A8, and A10.
It does not add a scheduler, controller, Bubble engine, or review exception.

Fresh review `asg_b556279b-f88c-4cf5-a3c9-4b5c1d9e9a3a` returned the
changes-requested verdict `att_ecafd2bd-4220-4a03-9071-863da1e2647b`. It confirmed the
legacy failure-class and null-turn Bubble repairs. It found two remaining blocking gaps:
the closed controller order omitted the live prompt batcher, and R18 did not define the
shape-stamped migration, typed `alert_user_unknown` cancellation, or dependent schema
objects. This revision closes those gaps in R1, R4, R18, the Architecture, A8, and A10.

Fresh stronger-model review `asg_f9dbe0e5-4bda-46f6-b44b-caba2ce78700` returned the
changes-requested verdict `att_9ea2ff40-df43-4b0b-b023-6f4423005b41` and report
`art_e760ebbf`. It confirmed the batcher and stamped-migration direction. It found four
remaining blocking gaps: Bubble's legacy dedupe occupied `turns.wakeId`; retirement,
unclaimable, and boot terminal writers bypassed the wake-outcome transaction; the
migration did not mechanically name the complete affected-object registry; and the
canonical spec set was not homed. It also corrected two baseline citations. This
revision closes those gaps in Spec homing, R5-R9, R15-R18, the Architecture, A2-A3, and
A6-A8.

Fresh stronger-model review `asg_4ad775e5-4317-4d2e-bf9b-e7f3ebf44be0` returned the
changes-requested verdict `att_3c6450ae-f9e4-4440-b616-db4244f7666a`. Its report row
`art_72124cd6` names SHA-256
`4a4482479020337610013a6c43337b3b958b81205db10c39424df7e3bf69a2e8`, but the
retired reviewer workspace and visible artifact row are unavailable; this revision does
not reconstruct those bytes. The verdict contains four blocking findings: A5 contradicted
the existing queued-work tune refusal; the quiescence cancellation pair was absent from
the successor shape; parent-target retirement canceled a transfer carrier outside the
terminalization bridge; and the runtime outcome principal rule conflicted with the
retirement prose. This revision closes them in R6-R9, R12-R16, R18, the Architecture,
and A4-A6.

Fresh stronger-model review `asg_0fcc18f6-35bc-4328-bde7-0e0958aa98fa` returned the
changes-requested verdict `att_8119568a-5392-4afa-8bb8-2b84c8df0cce` and report
`art_c4e21b23`, SHA-256
`ce6f82cf5c46b075b10b0b6e2059446584131e0dbbf85d125c88acb7d849fabf`. It confirmed
that the prior four findings are closed. It found one migration-scope defect: R18 and
A8 assigned prompt-delivery failure history to successful fired internal consumers.
The pinned baseline proves that `effort_deadline` can complete, mark its own wake fired,
and create no prompt turn. This revision closes that defect in Baseline reconciliation,
R18, the Architecture, and A8.

### Baseline reconciliation

| Limb | Source evidence | Ruling in this specification |
|---|---|---|
| A — cancel versus admission | `Wakes.cancel_in_txn/3` accepts a pending row. The scheduler runs the live digest batcher before due-row selection; its group transaction creates a carrier and commits typed member replacement (`lib/tightbeam/wakes.ex:1461-1495,1701-1761,2166-2170`). Legacy timed prompt wakes still deliver and then mark fired; condition/fallback wakes instead mark and enqueue in one transaction (`lib/tightbeam/wakes.ex:1-19,2168-2209,2538-2636`). The shared gateway transaction also admits and settles supervision controllers, consumes unavailable controllers, re-arms routing brackets, and optionally marks a process wake (`lib/tightbeam/gateway.ex:1032-1229`). Work-blocked suppression cancels and refunds a supervision wake before delivery (`lib/tightbeam/wakes.ex:2213-2288`). | R1-R4 replace only the split prompt admission edge. They retain these controllers in one closed order and make their existing cancellation outcomes precede delivery outcomes. A10 proves each controller survives. |
| B — outcomes, retry, and bubble | Wake state remains `pending | fired | canceled`; turn state is durable and `wakeId` is unique, but the ledger explicitly performs no automatic retry (`lib/tightbeam/wakes.ex`; `lib/tightbeam/ledger.ex`). Bubble derives owner, lineage, cause, and its durable sweep cursor from turns only (`lib/tightbeam/productions/bubble.ex:37-328`; `lib/tightbeam/productions/bubble_sweeper.ex:27-139`). | R5-R10 add typed wake outcomes and bounded retries. Null-turn final outcomes carry a scheduling-time alert route. Bubble consumes them through a second durable cursor while retaining the existing engine and owner-alert path. |
| C — queued turn and model swap | The ledger reads the session's selected model and harness when it claims a queued turn (`lib/tightbeam/ledger.ex:179-271`; `test/ledger_test.exs:104-133`). The live tune boundary refuses while any durable turn is queued or running (`lib/tightbeam/gateway.ex:4681-4705,5131-5164`; `test/gateway_test.exs:2718,3764-3883,5117-5257`). | R14 retains the fixed structure. A5 proves that a queued wake makes tune return `turn_in_progress`, the queued carrier claims the unchanged selection, and a later tune succeeds only after the turn ends. No model-switch mechanism is added. |
| D — quiescence | The incident row names later owner activity as the stale-premise event (`att_48fa113d-9907-4126-aff5-a1e0449b25e4`). Current main adds assignment liveness checkpoint binding for a self-scheduled wake, but it does not compare owner activity before delivery (`lib/tightbeam/gateway.ex:3735-3837`; `lib/tightbeam/supervision.ex:253-294`). The checkpoint binding is absent from 0.1.7. | R12-R13 add one typed owner-activity invalidation guard. Existing checkpoint semantics remain. |
| E — reliable handoff | Dispatch already commits the assignment, prompt echo, and turn in one transaction (`lib/tightbeam/assignments.ex:540-579,596-623`). An arbitrary wake remains a hint whose later carrier failure is not conserved, as recorded in `att_08870951-f045-42dc-844c-bc0addf16fba`. | Atomic dispatch remains authoritative. This specification closes only the ordinary wake carrier. |
| F — GAGGED versus negligence | The prod left-hand side checks terminal existence but does not read terminal status or failure class; a failed terminal can match the negligence ladder (`lib/tightbeam/supervision.ex:854-905,1000-1025,1114-1140`). | R11 makes the typed terminal failure a higher-priority, consumed fact. |
| G — O6 | O6 commits `078919d`, `67e1bcf`, `f64ffa7`, `81fbc2d`, and merge `ba5952b` are ancestors of both baselines. O6 regression tests remain at `test/gateway_test.exs:6452-6765`. | O6 is superseded for this work and stays closed. |
| H — schema custody | Current main stamps the merged shape as `coordination-fabric-v1-phase1-v3` and refuses an unreadable shape before normal use (`lib/tightbeam/schema.ex:65,764-1014`). The turn table has five named indexes (`lib/tightbeam/ledger.ex:68-75`). Checkpoint bindings reference `turns(seq)`, and fired-lineage triggers forbid attribution update or deletion (`lib/tightbeam/schema.ex:471-510,704-737`). | R18 defines one exact v3-to-v4 transition, recreates the code-defined dependent objects, validates the successor, and preserves the predecessor on failure. A8 tests those rails. |
| I — internal consumers | The scheduler invokes a non-prompt consumer directly and creates no prompt carrier (`lib/tightbeam/wakes.ex:2183-2205,2342-2355`). `EffortCheckin.deadline/3` marks the consumed `effort_deadline` wake fired, and the regression fixture retains a pending replacement deadline (`lib/tightbeam/effort_checkin.ex:1400-1405`; `test/escalation_delivery_test.exs:193-208`). | R18 selects `consumer='prompt'` before any delivery-outcome backfill. It preserves each non-prompt wake and its consumer-specific history without a delivery outcome. A8 tests the fired original and pending replacement. |

## Non-Goals

- Redesign assignment dispatch, assignment custody, work-item routing, or row polling.
- Change the live model-switch or harness-switch mechanism.
- Reopen O6 credential refusal, onboarding, or first-boot sequencing.
- Add a second scheduler, fault-bubble engine, supervision ladder, activity ledger, or
  adjudication mechanism.
- Retry a carrier turn whose inference or external side effects might have started.
- Infer whether the model obeyed the wake prompt. `handled` denotes a delivered carrier
  turn only.
- Parse prompt text, error prose, chat markers, role names, or attest notes to classify
  delivery, failure, quiescence, or activity.
- Change internal non-prompt wake-consumer semantics except where the shared schema
  migration must preserve their existing rows.
- Re-execute historical failed turns during migration.
- Design a graphical interface.

### Subtraction ruling

ADD wins only for the missing cross-row lifecycle. DELETE loses because removing
scheduled prompt wakes removes the native deferred-work and agent-communication surface.
ACCEPT loses because a canceled-yet-admitted or fired-yet-unhandled wake leaves durable
intent in a false terminal state. The design reuses the wake store, turn ledger, session
lane, scheduler, terminal publisher, supervision watermark, typed cancellation seam,
and Bubble production.

The outcome table is the smallest added durable mechanism. Without it, one mutable wake
state cannot retain several attempts and their turn links. A second activity table is not
added: quiescence reads the existing turn ledger. A second failure escalator is not added:
the existing Bubble production consumes the new `undeliverable` cause.

## Terms

- **Ordinary prompt wake**: a row in `wakes` with `consumer='prompt'`. The term includes
  immediate and delayed wakes from user, agent, and process principals. It excludes an
  internal consumer wake.
- **Wake attempt**: one scheduler act for one ordinary prompt wake. Attempts are numbered
  from `0`. An attempt that reaches admission has one linked turn.
- **Admission**: one database transaction commits the prompt echo, the linked queued turn,
  the `attempt` outcome, the `admitted` outcome, and the wake's pending-to-fired CAS. An
  admitted turn has not yet run.
- **Prompt controller**: an existing typed mechanism that can consume, suppress, charge,
  settle, attribute, or re-arm a prompt wake at its act edge. The closed set in this
  specification is digest materialization and typed member replacement, work-blocked
  suppression and refund, supervision-controller admission and settlement,
  unavailable-target cancellation, routing-bracket re-arm, and condition/fallback
  `firedBy` plus lifecycle provenance.
- **Handled**: the linked turn reaches `turns.status='delivered'`, and the same terminal
  transaction commits the wake's `handled` outcome. This term says nothing about semantic
  compliance with the prompt.
- **Failed**: the linked turn reaches `failed`, `failed_unknown`, or wake-linked
  `canceled`, and the same terminal transaction commits a `failed` wake outcome with a
  closed failure class. A canceled carrier is a delivery failure even when the turn
  cancellation itself was requested.
- **Undeliverable**: a terminal wake outcome. It means no later attempt is authorized.
  Target absence, an unsafe failure, and exhaustion of the retry schedule can produce it.
- **Retry-safe failure**: a typed `could_not_run` result that proves the adapter did not
  admit the prompt to an inference run. Text matching does not supply this proof.
- **Carrier-canceled failure**: a typed `carrier_canceled` result for an admitted but
  still-queued wake turn canceled because its recipient retired. The carrier did not
  run, but retirement is an explicit final disposition and authorizes no automatic
  retry.
- **GAGGED**: the durable derived condition that the terminal under supervision is a
  mechanical `failed`, `failed_unknown`, or wake-linked `canceled` turn.
  `could_not_run`, `run_failed`, `run_canceled`, `carrier_canceled`, and
  `outcome_unknown` are runtime GAGGED classes; `legacy_outcome_unknown` is the
  migration class. GAGGED is not an agent-authored standing fact and does not assert
  `work-blocked`.
- **Negligence prod**: the existing supervision prompt that says a holder's turn ended
  without a filing or continuation (`lib/tightbeam/supervision.ex:3856-3865`).
- **Logical wake bubble**: the existing Bubble climb with one undeliverable wake as its
  cause. Failed notice turns can move that one climb to another recipient; they do not
  create another wake cause.
- **Bubble notice identity**: the typed tuple
  `{noticeKind='bubble', noticeCauseKind, noticeCauseId, recipientSessionKey}` stored on
  a Bubble notice turn. It is unique per cause and recipient. Its turn has null
  `wakeId` and `wakeAttempt`, so it is not a wake carrier and cannot create a wake
  delivery outcome.
- **Wake Bubble route**: immutable context captured when a prompt wake is scheduled. It
  names the user who receives a terminal alert and, when one exists, the resolved target
  session whose lineage starts the climb. A role name is presentation and cause context;
  it is not a lineage key.
- **Wake outcome cursor**: the `production_cursors` row named `bubble:wake-outcome`. Its
  numeric value is the greatest append-only wake-delivery outcome id that Bubble finished
  recognizing.
- **Known shape transition**: the one release-owned schema transition from stamped shape
  `coordination-fabric-v1-phase1-v3` to stamped shape
  `coordination-fabric-v1-phase1-v4`. It validates the predecessor name, applies the R18
  mapping under exclusive database custody, and stamps the successor only after its
  checks pass.
- **Terminalization bridge**: `Ledger.terminalize_in_txn/3`. It performs one guarded
  terminal update with `RETURNING`, then calls the `Wakes` terminal mutation for each
  returned wake-linked turn before the caller can commit. Session-lane completion,
  retirement drain, the unclaimable backstop, and boot recovery use this bridge.
- **Owner turn admitted**: a row in `turns` whose `origin='user:<ownerUserId>'`, whose
  target session has that `ownerUserId`, and whose `seq` is greater than a stored cursor.
  Terminal status does not change this activity fact.
- **Quiescence wake**: a delayed self-wake created with the typed
  `owner_turn_admitted` invalidation guard. Prompt prose does not make a wake a
  quiescence wake.
- **Self-wake**: an ordinary prompt wake created by a session principal whose resolved
  target session key equals that principal's session key in the scheduling transaction.
  A role target qualifies only when it resolves to that same session; the quiescence
  guard then pins that resolved session for delivery.
- **Cause**: a closed kind plus durable identifier that explains a transition. Examples
  are `turn:<seq>`, `wake:<wakeId>`, and `owner_turn:<seq>`.
- **Principal**: the typed user, session, or `process:tightbeam` identity responsible for
  a transition.

## Assumptions

1. The SQLite owner serializes mutation transactions. A transaction can use an update
   row count as the cancel-versus-admit decision.
2. The turn ledger keeps its one-way `queued -> running -> terminal` state machine and
   one running turn per session (`lib/tightbeam/ledger.ex:1-18,179-271,363-449`).
3. The session lane remains the claim and turn-boundary serialization point
   (`lib/tightbeam/session_lane.ex:90-111,249-305`).
4. A retry can reuse the first attempt's prompt echo and message id. `turns.messageId`
   does not have a uniqueness constraint.
5. The current gateway identifies checkout, session, and prompt failure stages
   (`lib/tightbeam/gateway.ex:1874-2033`). Some adapter protocols do not prove whether a
   prompt-stage inference run was admitted. R7 treats absent proof as
   `outcome_unknown`.
6. Product composition supplies the finite retry delays. This specification pins the
   shipped default to `[5000, 30000, 120000]` milliseconds. The values bound waiting;
   they do not detect an event or decide an outcome.
7. The existing Bubble production remains the single capable-parent and owner-alert
   path (`lib/tightbeam/productions/bubble.ex:1-30,112-180,332-365`).
8. User-origin turns preserve their typed `origin`, target session, and sequence in the
   turn ledger.
9. Session rows are not hard-deleted. A prompt wake can therefore retain a resolved
   session key as lineage context after that session retires. When no session resolves,
   the scheduling transaction can still derive an alert user from the typed origin,
   linked assignment or work item, or the target's durable owner row.

## Invariants

### R1 — Cancel and initial admission share one decision

`WakeScheduler` shall send each due `consumer='prompt'` row through R4's closed controller
order. The batcher can consume a digest member before admission by creating its carrier
and committing the member's existing typed replacement cancellation in one group
transaction. A row that remains after the pre-admission controllers shall enter one
controller-aware admission transaction.

`Wakes` shall admit attempt `0` only when the admission transaction changes the source
wake from `pending` to `fired` with a guarded update and verifies one changed wake row
before commit. A condition or fallback claim shall write its existing `firedBy` value in
that same guarded update.

The same transaction shall commit the echo, turn, `attempt`, and `admitted` outcomes. A
zero-row wake update shall roll back those writes and return the losing cancel-versus-
admit result.

An existing prompt controller can consume or cancel the wake before that guarded update.
That controller outcome shall commit through its existing typed seam with no prompt echo,
turn, `attempt`, or `admitted` outcome.

### R2 — Successful cancellation proves no admission

`Wakes.cancel_in_txn/3` shall return success only when its transaction commits one typed
cancellation row, changes the wake from `pending` to `canceled`, and observes no
`admitted` outcome for that wake.

After one `admitted` outcome commits, a cancellation call shall return the existing
false result and shall preserve the wake, turn, message, and outcome rows.

This rule governs runtime cancellation after migration. An R18
`wake_migration_conflict` preserves a pre-release canceled-with-admission history as
evidence; it does not make a later cancellation call succeed.

### R3 — Retry admission has one CAS identity

`Wakes` shall identify a retry by `{wakeId, attemptNo}`. A retry transaction shall admit
attempt `n + 1` only when attempt `n` has one retry-eligible `failed` outcome, its
`retryAt` is not later than the transaction clock, and no later attempt or final wake
outcome exists.

The retry transaction shall insert one turn and one `admitted` outcome for that identity.
The database shall reject a second turn for the same identity and a second queued or
running turn for the same wake.

A retry shall reuse the source wake's settled controller, attribution, and condition or
fallback provenance. It shall retain the existing supervision charge and settlement,
routing-bracket arm, prod accounting, and single `firedBy` lifecycle event.

### R4 — Check and act are indivisible

Initial admission shall preserve this closed order:

1. `WakeScheduler` runs the existing batcher before it selects due delivery rows. For one
   eligible group, the batcher rechecks each member's boundary or ceiling, creates one
   `digest=1` carrier, cancels each carried member as `superseded` with that carrier as its
   replacement, and writes `wake_digest_materialized` in one transaction. A member
   cancellation refusal rolls back the group transaction. The existing per-group failure
   seam leaves its members pending and records `wake_digest_materialization_failed`.
2. `WakeScheduler` runs existing work-blocked suppression and prod refund for a remaining
   due row. A successful suppression commits typed cancellation and stops.
3. The admission transaction loads the wake and rechecks the variant-specific act guard:
   due ordinary wake, matching condition fact, or elapsed fallback deadline.
4. R13 quiescence invalidation runs. A successful invalidation commits typed cancellation
   and stops.
5. The transaction resolves the target and reply reference through the existing gateway
   seams.
6. The existing supervision controller admits, cancels, or records target unavailability.
   Its cancellation stops admission.
7. The transaction appends the prompt echo and enqueues the turn.
8. The existing supervision controller settles against the turn sequence.
9. `Wakes` appends `attempt` and `admitted`, applies R1's guarded wake update, and checks
   one changed row.
10. The existing routing-bracket re-arm runs once.
11. A condition or fallback wake writes its existing typed lifecycle event once.

An error at steps 3-11 shall roll back that transaction's controller, message, turn,
outcome, re-arm, lifecycle, and wake-state writes together. Initial admission, retry
admission, cancellation, quiescence invalidation, turn terminalization, retry scheduling,
and exhaustion shall evaluate their guard and commit their action in one database
transaction.

### R5 — The wake outcome history is typed and queryable

`Wakes` shall append only these wake delivery kinds: `attempt`, `admitted`, `handled`,
`failed`, and `undeliverable`.

An `admitted`, `handled`, or `failed` row shall name one `turnSeq`. An `attempt` or
`undeliverable` row shall name the turn when a turn exists. A target-resolution failure
can use a null turn link and shall name the typed target failure instead.

Each outcome shall store `wakeId`, `attemptNo`, event time, cause kind, cause id, and
principal. A failed outcome shall also store its closed failure class and optional
`retryAt`.

The scheduling transaction for a prompt wake shall store one Wake Bubble route. It shall
derive `bubbleAlertUserId` in this order: typed user origin; owner of the typed session
origin; linked work-item owner; linked assignment's work-item owner; target owner. It
shall store the target session resolved in that transaction as
`bubbleStartSessionKey`, or null when no session resolves. If this search finds no alert
user, scheduling shall return `unknown_wake_alert_user` and insert no wake.

A runtime `undeliverable` outcome with a null turn shall copy
`bubbleAlertUserId` and `bubbleStartSessionKey` from the wake. The alert user is the
sender-side or linked-work owner; it does not change when a target role or session later
loses its owner row. A runtime null-turn final outcome without `bubbleAlertUserId` shall
fail its transaction instead of fabricating a route.

The caller-visible `wake-get` projection and a linked work-item trace shall expose
`wakeId`, aggregate `state`, `latestOutcome`, `attemptCount`, latest linked `turnSeq`,
`nextRetryAt`, and the latest failed attempt's `failureClass`. `wake-get` shall also
return the ordered outcome history. A null-turn runtime `undeliverable` history row shall
include `bubbleRoute: {alertUserId, startSessionKey}`. Other outcome rows shall omit that
field.

The gateway shall authorize `wake-get` when the caller is an admin, the caller origin
equals the wake origin, or the caller owns the target session. It shall return
`unknown_wake` for an absent id and `denied` for an existing row outside that authority.

### R6 — Turn terminalization settles wake state atomically

Each runtime turn terminal writer shall call `Ledger.terminalize_in_txn/3`. The bridge
shall perform the writer's guarded terminal update with `RETURNING` and shall call
`Wakes.settle_terminal_rows_in_txn/4` for the returned rows before the transaction can
commit. A guard loser shall change no turn and append no wake outcome.

`SessionLane` shall use the bridge for a running turn's normal terminal CAS.
`Ledger.drain_queued_for_retire_in_txn` shall use it inside the session-retirement
transaction. `Ledger.fail_unclaimable` shall use it with the existing no-active-session
predicate in the guarded update. `Ledger.recover_running` shall use it for each
running-to-`failed_unknown` boot transition. A failure while settling one returned
wake-linked row shall roll back that writer's turn updates and wake outcomes together.

`Supervision.transition_in_txn` shall use the same bridge for the queued transfer carrier
that `parent_target_retired` currently invalidates before it re-arms or elevates
supervision. In the same outer retirement transaction, it shall first choose the existing
deterministic replacement kind and inputs, call the bridge, materialize exactly one
entitlement re-arm or successor wake, and then append the
`supervision_liveness_sidecar` retirement outcome that identifies that replacement. No
step becomes visible before the outer commit. The bridged turn is no longer queued when
the later generic retirement drain runs. A bridge, replacement, sidecar, or retirement
failure shall roll back the whole outer transaction.

For a returned row with null `wakeId` and `wakeAttempt`, the bridge shall commit the
turn terminal only. This includes a Bubble notice turn. For a wake-linked delivered
terminal, `Wakes` shall append one `handled` outcome. For a wake-linked `failed`,
`failed_unknown`, or `canceled` terminal, it shall append one `failed` outcome. It shall
apply R8 retry or finality from the stored class in that transaction.

### R7 — Failure classification is typed at the run boundary

The terminalization bridge shall persist one of `could_not_run`, `run_failed`,
`run_canceled`, `carrier_canceled`, or `outcome_unknown` on a runtime failed terminal
and its wake-linked failed outcome.

Checkout failure and session-establishment failure shall produce `could_not_run`.
Prompt-stage failure shall produce `could_not_run` only when the adapter returns typed
proof that the inference run was not admitted. Typed proof that the run was admitted and
failed shall produce `run_failed`. A prompt-stage failure with neither proof shall
produce `outcome_unknown`. Boot recovery and a lost runner outcome shall also produce
`outcome_unknown`.

A runtime `could_not_run` or `run_failed` terminal shall use turn status `failed`. A
runtime `outcome_unknown` terminal shall use `failed_unknown`. A canceled carrier shall
retain turn status `canceled`. A running carrier canceled through the existing
current-run seam shall use `run_canceled`. A queued carrier canceled by the retirement
drain, or by the unclaimable backstop with reason `session_retired`, shall use
`carrier_canceled`.

The unclaimable backstop reason `no_session` shall use status `failed` and class
`could_not_run` for a wake-linked row. A runtime guard prevents a new wake carrier from
entering that shape; the classification covers a row admitted before the guard existed.

The terminalization source shall supply this closed cause and principal mapping:

| Source | Expected source state | Terminal/class | Outcome cause | Principal |
|---|---|---|---|---|
| session lane delivered | `running` | `delivered` / null | `turn_terminal`, `turn:<seq>` | `process:tightbeam` |
| session lane failed | `running` | class-derived `failed` or `failed_unknown` | `turn_terminal`, `turn:<seq>` | `process:tightbeam` |
| current-run cancellation | `running` | `canceled` / `run_canceled` | `turn_terminal`, `turn:<seq>` | `process:tightbeam` |
| parent-target retirement transfer | `queued` transfer carrier | `canceled` / `carrier_canceled` | `parent_target_retired`, `transfer:<transferEvidenceId>` | `process:tightbeam` |
| retirement drain | `queued` | `canceled` / `carrier_canceled` | `recipient_retired`, `session:<sessionKey>` | `process:tightbeam` |
| unclaimable `session_retired` | `queued` plus no active session | `canceled` / `carrier_canceled` | `recipient_unclaimable`, `session:<sessionKey>:session_retired` | `process:tightbeam` |
| unclaimable `no_session` | `queued` plus no session row | `failed` / `could_not_run` | `recipient_unclaimable`, `session:<sessionKey>:no_session` | `process:tightbeam` |
| boot recovery | `running` | `failed_unknown` / `outcome_unknown` | `boot_recovery`, `turn:<seq>` | `process:tightbeam` |

The implementation shall derive an adapter failure class exclusively from the typed
stage and adapter run-admission disposition. It shall derive `run_canceled` only from
the existing current-run canceled-terminal CAS and `carrier_canceled` only from the
three closed queued-recipient paths above.

### R8 — Retry is finite, backoff-bound, and replay-safe

For the shipped retry schedule `[5000, 30000, 120000]`, a wake can have attempt numbers
`0`, `1`, `2`, and `3`. The scheduler shall make attempt `n + 1` eligible at
`failedAt + retryDelays[n]` for a `could_not_run` failure.

A `run_failed`, `run_canceled`, `carrier_canceled`, or `outcome_unknown` failure shall
transition the wake to `undeliverable` in the terminal transaction. The scheduler shall
create no retry for those classes. This preserves the reviewed retirement rule that an
agent, not automatic replay, decides whether to send new intent after recipient
retirement.

A `could_not_run` failure on attempt `3` shall append `undeliverable` in the terminal
transaction. A final wake outcome shall make later scheduler passes inert.

### R9 — Final undeliverability starts one logical Bubble cause

The Bubble production shall ignore a wake-linked failed turn while that wake has a
retry-eligible failed outcome.

Except for R6's atomically replaced `parent_target_retired` transfer, one runtime
`undeliverable` outcome shall admit one logical Bubble cause keyed by the wake id. A
notice for that cause shall store Bubble notice identity
`{'bubble','wake',<wakeId>,<recipientSessionKey>}`. A notice for an existing turn cause
shall store `{'bubble','turn',<causeTurnSeq>,<recipientSessionKey>}`. The database shall
reject a second turn for either tuple. Each notice turn shall keep null `wakeId` and
`wakeAttempt`. R5-R8 shall treat it as a non-wake turn: the bridge shall commit its turn
terminal only, and the retry and wake-cause queries shall select linked wake attempts.
Its own failed or canceled terminal shall continue the existing capable-parent climb.

A `parent_target_retired` transfer outcome is the one closed exception to Bubble
admission. Its outer retirement transaction must also commit one existing
`supervision_liveness_sidecar` retirement outcome whose kind is `child_rearm`,
`parent_elevation`, or `main_elevation` and whose outcome id identifies the replacement
entitlement or successor wake. That row proves custody continued, so Bubble shall not
start another climb for the replaced transfer wake. The transaction shall roll back if
it cannot commit the replacement; an undeliverable transfer outcome without that row is
invalid.

Bubble shall accept a committed runtime `undeliverable` outcome that lacks R6's
committed parent-retirement replacement through two inputs: a post-commit cast naming
the outcome id and a sweep of outcome ids above the Wake outcome cursor. The sweep shall
run at boot and on the existing Bubble tick. It shall advance
`production_cursors.name='bubble:wake-outcome'` to the greatest outcome id in each
ordered append-only batch only after it recognizes the batch. It shall exclude
`causeKind='legacy_import'`. A crash after the final
outcome commits and before notice admission or cursor advance shall delay that logical
cause; replay shall preserve one logical cause and one notice per recipient.

For an outcome with a linked turn, Bubble shall derive the starting session and alert
user from that turn and session rows. For a null-turn outcome, Bubble shall use the
stored Wake Bubble route. When `bubbleStartSessionKey` names a session row, Bubble shall
start with that session's existing lineage and shall skip inactive rungs through the
existing resolver. When it is null or names no session row, Bubble shall go directly to
the existing terminal-alert transaction for `bubbleAlertUserId`. An absent target owner
shall leave this stored route controlling.

Notice turns for a wake cause shall carry `requestRef='bubble:wake:<wakeId>'`. Bubble
shall re-derive their prompt and terminal alert from the final outcome, its linked turn
when present, and its stored route. Those structured rows shall be the sole prompt and
lineage inputs.

The first sentence of a wake Bubble notice shall name the wake id and the final linked
turn sequence, when one exists. Existing non-wake Bubble causes shall keep their current
turn-sequence identity and routing behavior, but shall store that identity in the typed
notice columns instead of `turns.wakeId`.

### R10 — Handled and undeliverable are mutually final

The database shall permit one `handled` or one `undeliverable` outcome for one wake. It
shall reject a history containing both final kinds. A final outcome shall have no
`retryAt`.

### R11 — Supervision consumes GAGGED before negligence

The supervision production shall read the terminal row's typed failure class before the
prod ladder acts. A terminal in `failed`, `failed_unknown`, or wake-linked `canceled`
shall yield the named `holder_gagged` no-match result.

In one transaction, supervision shall advance its terminal watermark and append one
`supervision_gagged_terminal` lifecycle row naming the terminal, failure class, cause,
and `process:tightbeam` principal. It shall preserve the assignment's prod count,
attempt count, entitlement generation, and due time.

A later delivered terminal remains eligible for the existing liveness-receipt and prod
logic. GAGGED consumption shall leave the `work-blocked` fact set unchanged.

### R12 — Quiescence uses one named durable activity

The wake command shall accept the typed `owner_turn_admitted` invalidation guard only
for a prompt self-wake whose `dueAt` is later than the scheduling transaction clock. It
shall reject the guard before row insertion for an immediate wake, a non-session caller,
or a target that resolves to another session. The scheduling transaction shall store the
resolved owner user id and the greatest admitted owner-turn sequence visible in that
transaction.

For an accepted role target, the guard shall pin the wake's stored session key as its
delivery target. A guarded wake shall keep that target after a later role rebind.
Unguarded role wakes retain their existing delivery-time re-resolution.

The wire field shall be `invalidationKind='ownerTurnAdmitted'`. The CLI spelling shall be
`--cancel-on-owner-activity`. Missing this flag shall preserve ordinary wake behavior.

### R13 — Owner activity invalidates at the wake act edge

Before a guarded quiescence wake admits a turn, the admission transaction shall query for
an owner-origin turn with a sequence greater than the stored cursor and a target session
owned by the stored owner. It shall resolve delivery against the pinned session from R12,
not the current role binding.

When such a turn exists, the transaction shall cancel the quiescence wake through the
typed cancellation seam with reason `quiescence_invalidated`, cause
`owner_turn_admitted:<turnSeq>`, and principal `process:tightbeam`. It shall commit no
prompt echo, carrier turn, `attempt`, or `admitted` outcome.

The cancellation command shall use this closed provenance:

- `requesterKind='process'` and `requesterId='tightbeam:quiescence-guard'`;
- `reasonKind='quiescence_invalidated'`;
- `causalSourceKind='owner_turn_admitted'` and the decimal owner turn sequence as
  `causalSourceId`;
- `outcomeKind='no_replacement'`, a null replacement, and the transaction clock as
  `canceledAt`.

Only the Wakes act-edge guard may use that requester and pair. Source validation shall
require the named turn to exist, exceed `invalidationAfterTurnSeq`, have
`origin='user:<invalidationOwnerUserId>'`, and target a session owned by that user. A
caller-supplied cancellation command, stale turn, other owner, or other target shall
fail validation and change no row.

When no such turn exists, the same transaction shall continue through R1 admission.

### R14 — Wake delivery preserves the fixed model-switch boundary

A wake turn shall read the target session's live model, effort, context, and harness when
the ledger claims it. Admission and retry shall leave the turn's adapter generation and
model fields unset until claim.

A model or harness change shall continue to act through the session lane turn boundary.
The existing session lane shall remain the sole model-migration path.

### R15 — One wake mutation seam owns the new rows

`Tightbeam.Wakes` shall be the only module that inserts wake delivery outcomes or changes
the wake row for admission, cancellation, invalidation, retry eligibility, handling, or
undeliverability. `Ledger.terminalize_in_txn/3` shall be the only runtime turn-terminal
update bridge. It shall call a `Wakes` function inside the same transaction for each
returned wake-linked row. Gateway, SessionLane, retirement, the unclaimable backstop,
parent-target retirement in Supervision, and boot recovery shall use these seams.

The R18 transition may materialize its closed successor rows through `Schema` and the
named `Wakes` migration helpers. That pre-boot copy is not a runtime terminal event. The
v3-to-v4 transition is the sole migration path authorized to insert a wake outcome or
normalize a wake-linked terminal row.

### R16 — Cause and principal survive each transition

The outcome writer shall reject an empty cause kind, empty cause id, or any outcome
principal other than `process:tightbeam`. Scheduler admission, retry, terminal
settlement, GAGGED consumption, invalidation, Bubble, and migration transitions shall
use that principal. The source wake and typed cancellation rows retain their creator,
origin, and requester principals.

Every runtime wake-delivery outcome shall use `process:tightbeam`. The authenticated
retirement principal shall remain on each existing typed cancellation, retirement
sidecar, and retirement lifecycle row emitted by either retirement path. It shall not be
copied into a wake-delivery outcome. A terminalization caller shall supply its closed
source tag; neither `Ledger` nor `Wakes` shall infer a cause or principal from the error
string.

### R17 — Restart recovery preserves eligibility

Gateway restart shall reconstruct due retry work from wake outcomes and clocks while
preserving attempt numbers, `retryAt`, and the unique final outcome.

A running wake turn recovered as `failed_unknown` shall use R6's terminalization bridge,
store `outcome_unknown`, enter R8's immediate `undeliverable` path, and produce zero
replacement turns. A boot-recovery transaction failure while writing one linked outcome
shall roll back the selected running-turn transitions and leave them eligible for the
next exact recovery pass.

Boot recovery shall start the existing Bubble sweeper with both cursor feeds. The
`bubble:wake-outcome` feed shall resume after its committed outcome id and shall
re-recognize an earlier final outcome when a crash prevented cursor advance. The
deterministic wake-cause and notice identities shall make that replay inert after prior
notice admission.

### R18 — Legacy rows remain truthful without replay

`Schema` shall expose one known shape transition from
`coordination-fabric-v1-phase1-v3` to `coordination-fabric-v1-phase1-v4`. The application
shall run it under exclusive database custody before `Schema.ensure_all/1`, `Wakes`,
`LaneManager`, `Supervision`, or Bubble starts. The transition shall refuse an absent,
multiple, or different predecessor stamp. A database already stamped with the successor
shall pass validation without a second migration.

The shape transition shall preserve existing wake, cancellation, turn, message,
lifecycle, and Bubble rows except for the closed conflict normalizations below. It shall
select the wake consumer before it applies this closed mapping. Only a wake with
`consumer='prompt'` can enter a delivery-outcome backfill or Wake Bubble route mapping.

| Legacy shape | Migration result |
|---|---|
| non-prompt wake without a turn, in any state | Preserve its wake, cancellation, message, and consumer-specific lifecycle values. Create no wake delivery outcome, conflict normalization, or Wake Bubble route. Do not apply a prompt mapping below. |
| `pending` prompt wake without a turn | Preserve it without an outcome. Derive and store the R5 Wake Bubble route. Its first later act uses attempt `0`. |
| `pending` prompt wake without a turn whose alert user cannot be derived | Insert the typed `alert_user_unknown` cancellation below; change the wake to `canceled` at the same migration timestamp; backfill null-turn `attempt` plus `undeliverable` with `causeKind='legacy_import'`; record `wake_migration_conflict` with the prior row and reason `alert_user_unknown`. |
| `canceled` prompt wake without a turn | Preserve it without a delivery outcome. Its typed cancellation remains final. |
| `fired` prompt wake without a turn | Backfill null-turn `attempt` plus `undeliverable` with `causeKind='legacy_import'`, a null failure class, and no Bubble route. |
| exact legacy Bubble notice turn | When `origin='process:tightbeam'`, `requestRef='bubble:<decimalTurnSeq>'`, `wakeId=requestRef || ':' || sessionKey`, and no wake row has that id, store `noticeKind='bubble'`, `noticeCauseKind='turn'`, the decimal turn sequence as `noticeCauseId`, and the target as `noticeRecipientSessionKey`; set `wakeId` and `wakeAttempt` null; create no wake outcome. |
| unlinked turn in `failed` or `failed_unknown` | Preserve its status, set `failureClass=legacy_outcome_unknown`, and create no wake outcome. |
| unlinked turn in `queued`, `running`, `delivered`, or `canceled` | Preserve it with a null failure class and create no wake outcome. |
| linked turn, prompt wake state `fired` | Set `wakeAttempt=0`; backfill `attempt` and `admitted`; then apply the terminal mapping below. |
| linked turn, prompt wake state `pending` | Normalize the wake to `fired`, record its prior state in `wake_migration_conflict`, and apply the linked-turn mapping. The turn is durable admission evidence. |
| linked turn, prompt wake state `canceled` | Preserve the wake and cancellation rows, record both prior states in `wake_migration_conflict`, and apply the linked-turn mapping. |

The transition shall treat a non-null legacy `turns.wakeId` as a wake link only when a
`wakes` row has that exact id. It shall treat it as a Bubble notice only when the complete
typed relation above holds. Another non-null legacy value has no lawful interpretation;
the transition shall return `ShapeError`, roll back, and preserve v3 rather than infer a
cause from the string.

A turn linked to a non-prompt wake also has no lawful prompt-attempt interpretation.
The transition shall return `ShapeError`, roll back, and preserve v3 instead of assigning
that turn an attempt number or delivery outcome.

The terminal mapping is also closed. `delivered` gains `handled`. `failed` and
`failed_unknown` retain their status, gain failure class `legacy_outcome_unknown`, and
gain `failed` plus `undeliverable`. `canceled` retains its status, gains failure class
`legacy_outcome_unknown`, and gains `failed` plus `undeliverable`. A queued or running
turn under a `fired` wake retains its status and continues through normal claim or boot
recovery. A queued or running turn under a `canceled` wake is normalized to
`failed_unknown` with failure class `legacy_outcome_unknown` and an ended-at migration
time; it gains `failed` plus `undeliverable`, and the claim query excludes it.

The `alert_user_unknown` cancellation shall use this closed provenance:

- `requesterKind='process'` and `requesterId='tightbeam:schema-migration'`;
- `reasonKind='alert_user_unknown'`;
- `causalSourceKind='schema_transition'` and
  `causalSourceId='coordination-fabric-v1-phase1-v3->coordination-fabric-v1-phase1-v4'`;
- `outcomeKind='no_replacement'`, a null replacement, and the migration timestamp as
  `canceledAt` on both rows.

The transition shall insert that cancellation while the wake is pending. It shall then
update the wake to the cancellation row's `wakeState` and `canceledAt`. For an open linked
work item, the cancellation shall use `workImpactKind='linked_work_open'`, that work item
as the primary work, `livenessTriggerKind='pending_wake'`, the wake id as
`livenessTriggerId`, and `actionNeeded=1`. For a wake without open linked work, it shall
use the existing non-open work-impact shape, null liveness fields, and `actionNeeded=0`.
The successor cancellation allowlists and compatibility check shall admit only this
schema-migration pair in addition to the existing pairs.

The successor cancellation shape shall also admit the one runtime quiescence pair from
R13: requester `tightbeam:quiescence-guard`, reason
`quiescence_invalidated`, source kind `owner_turn_admitted`, and outcome
`no_replacement`. The runtime validator shall require R13's source-row proof. The v3
copy has no such rows to backfill; the transition changes only the successor DDL and
allowlists for this pair.

Each backfilled outcome uses `legacy_import`. Bubble shall send no new notice for it;
existing Bubble and cancellation rows remain escalation and disposition evidence. A
second migration pass shall insert no second outcome or conflict row.

`legacy_outcome_unknown` remains a turn failure class. The migration shall assign it only
to a `failed`, `failed_unknown`, or wake-linked `canceled` turn and its linked `failed`
outcome. A null-turn legacy `undeliverable` has no `failed` row, so its `failureClass`
and `wake-get.failureClass` shall be null. Its `legacy_import` cause records why the
outcome exists.

`Schema.successor_registry/0` shall be the complete, ordered transition input and the
complete clean-v4 bootstrap input. It shall concatenate the same exported object records
used by `Wakes.ensure_schema/1`, `Ledger.ensure_schema/1`,
`Schema.ensure_supervision_liveness_v1_in_txn/2`, and the supervision enforcement pass.
Each record shall contain `{owner, type, name, sql, dependsOn}`. A table-level foreign
key shall appear in its table's record; an index or trigger shall have its own record.
The product shall contain no second DDL string for an owned v4 object.

The transition shall compute the dependency closure whose `dependsOn` contains
`wakes`, `wake_cancellations`, or `turns`. That closure necessarily contains the five
existing turn indexes; the wake due, delivery, condition, and cancellation-state
indexes; the pending-insert and typed-cancellation triggers; the supervision sidecar,
pending-controller, fired-lineage sidecar, fired-lineage turn, and checkpoint-binding
triggers; the checkpoint binding's `sourceTurnSeq` foreign key; and each new notice,
outcome, conflict, and append-only object. The registry, not this explanatory list, is
the complete authority.

For each table record in that closure, the transition shall create a temporary
successor and copy its rows before it drops the predecessor. R18's closed mapping shall
change only copied `wakes`, `wake_cancellations`, and `turns` rows, and it shall populate
the new outcome and conflict tables. The transition shall copy another affected child
table value-for-value. It shall drop predecessor indexes and triggers before tables,
drop child tables before parent
tables, rename parent successors before child successors, and then create indexes and
triggers in registry dependency order.

Before it changes the stamp, the transition shall require one normalized
`sqlite_master` row matching each registry record, no duplicate owned name, an empty
`PRAGMA foreign_key_check` result, and an `ok` `PRAGMA integrity_check` result. A
missing, extra duplicate, or mismatched owned object shall roll back the transaction and
preserve the predecessor stamp. Post-commit `Schema.ensure_all/1` and a clean v4 restart
shall validate that same registry without adding an object.

### R19 — Guidance follows the implemented mechanism

The release change shall update the wake CLI help and the operating manual in one batch
after R12-R13 and A4 pass. The directive shall state that
`--cancel-on-owner-activity` applies to a delayed self-wake whose premise is continued
owner quiescence. The directive shall leave other wake purposes unchanged.

## Architecture

### Shape transition gate

`Schema.migrate_known_shape/1` runs on the database owner's connection before the
application starts another database consumer. It classifies the database by the exact
`schema_stamp` row:

- an empty new database continues to normal successor-shape creation;
- `coordination-fabric-v1-phase1-v4` continues to `Schema.ensure_all/1` without mutation;
- `coordination-fabric-v1-phase1-v3` enters the one R18 transition;
- an absent stamp on a non-empty database, multiple stamps, or another stamp returns
  `ShapeError` without DDL.

For the known predecessor, the migration connection sets `PRAGMA foreign_keys=OFF`
before `BEGIN IMMEDIATE`, acquires the write lock, and rechecks the predecessor stamp.
It creates the successor tables under temporary names, copies and normalizes rows through
the R18 mapping, replaces the rebuilt tables, and recreates the code-defined successor
object registry. It runs `PRAGMA foreign_key_check` and `PRAGMA integrity_check` before
the commit. It changes the single stamp from v3 to v4 as the transaction's final
mutation. A failed DDL, copy, normalization, object check, or stamp update rolls back the
transaction. After commit, the connection restores `PRAGMA foreign_keys=ON`, re-reads the
v4 stamp, and runs `Schema.ensure_all/1` as validation rather than migration.

The transition does not infer a shape from table contents or stored DDL. The exact
predecessor stamp selects one code-defined plan. A later run against v4 validates the
successor and performs no row backfill.

### Durable shape

Rebuild `turns` in the existing pre-boot schema migration to replace table-level
`wakeId UNIQUE` with an attempt identity. Preserve existing columns and add:

```sql
wakeAttempt INTEGER NULL CHECK (wakeAttempt >= 0),
failureClass TEXT NULL
  CHECK (failureClass IN
    ('could_not_run','run_failed','run_canceled','carrier_canceled','outcome_unknown',
     'legacy_outcome_unknown')),

noticeKind TEXT NULL CHECK (noticeKind = 'bubble'),
noticeCauseKind TEXT NULL CHECK (noticeCauseKind IN ('turn','wake')),
noticeCauseId TEXT NULL CHECK (length(noticeCauseId) > 0),
noticeRecipientSessionKey TEXT NULL REFERENCES sessions(sessionKey)
```

The rebuilt table adds a check that `failed` and `failed_unknown` rows carry a non-null
failure class; a wake-linked `canceled` row carries `run_canceled`,
`carrier_canceled`, or `legacy_outcome_unknown`; and another terminal row carries a null
class unless R7 assigns one.
Another table check requires `wakeId` and `wakeAttempt` to be null together or populated
together. This prevents the nullable-column behavior of a unique index from admitting
an unnumbered wake turn. The rebuilt table also declares
`UNIQUE(seq, wakeId, wakeAttempt)` for the outcome link below.

A second check requires the four notice columns to be null together or populated
together. A third check forbids a row from carrying both a wake-attempt identity and a
notice identity. An ordinary non-wake, non-notice turn can leave both identities null.

Create these indexes after the rebuild:

```sql
CREATE UNIQUE INDEX turns_wake_attempt
  ON turns(wakeId, wakeAttempt)
  WHERE wakeId IS NOT NULL;

CREATE UNIQUE INDEX turns_one_active_per_wake
  ON turns(wakeId)
  WHERE wakeId IS NOT NULL AND status IN ('queued','running');

CREATE UNIQUE INDEX turns_notice_dedupe
  ON turns(noticeKind, noticeCauseKind, noticeCauseId, noticeRecipientSessionKey)
  WHERE noticeKind IS NOT NULL;
```

Add the append-only outcome table:

```sql
CREATE TABLE wake_delivery_outcomes (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  wakeId       TEXT NOT NULL REFERENCES wakes(wakeId),
  attemptNo    INTEGER NOT NULL CHECK (attemptNo >= 0),
  kind         TEXT NOT NULL CHECK
                 (kind IN ('attempt','admitted','handled','failed','undeliverable')),
  turnSeq      INTEGER NULL REFERENCES turns(seq),
  at           INTEGER NOT NULL,
  retryAt      INTEGER NULL,
  failureClass TEXT NULL CHECK
                 (failureClass IN
                   ('could_not_run','run_failed','run_canceled','carrier_canceled',
                    'outcome_unknown','legacy_outcome_unknown')),
  bubbleAlertUserId TEXT NULL,
  bubbleStartSessionKey TEXT NULL,
  causeKind    TEXT NOT NULL CHECK
                 (causeKind IN
                   ('scheduler_due','retry_due','turn_terminal','target_unresolvable',
                    'parent_target_retired','recipient_retired',
                    'recipient_unclaimable','boot_recovery',
                    'retry_exhausted','unsafe_failure','legacy_import')),
  causeId      TEXT NOT NULL CHECK (length(causeId) > 0),
  principal    TEXT NOT NULL CHECK (principal = 'process:tightbeam'),
  UNIQUE (wakeId, attemptNo, kind),
  FOREIGN KEY (turnSeq, wakeId, attemptNo)
    REFERENCES turns(seq, wakeId, wakeAttempt) DEFERRABLE INITIALLY DEFERRED,
  CHECK (kind NOT IN ('admitted','handled','failed') OR turnSeq IS NOT NULL),
  CHECK ((kind = 'failed' AND failureClass IS NOT NULL)
         OR (kind != 'failed' AND failureClass IS NULL AND retryAt IS NULL)),
  CHECK (retryAt IS NULL OR (kind = 'failed' AND failureClass = 'could_not_run')),
  CHECK (kind = 'undeliverable'
         OR (bubbleAlertUserId IS NULL AND bubbleStartSessionKey IS NULL)),
  CHECK (bubbleStartSessionKey IS NULL OR bubbleAlertUserId IS NOT NULL),
  CHECK (turnSeq IS NOT NULL OR kind != 'undeliverable'
         OR causeKind = 'legacy_import' OR bubbleAlertUserId IS NOT NULL)
);

CREATE UNIQUE INDEX wake_delivery_one_final
  ON wake_delivery_outcomes(wakeId)
  WHERE kind IN ('handled','undeliverable');

CREATE INDEX wake_delivery_retry_due
  ON wake_delivery_outcomes(kind, retryAt, wakeId, attemptNo)
  WHERE kind='failed' AND retryAt IS NOT NULL;

CREATE TRIGGER wake_delivery_no_update
BEFORE UPDATE ON wake_delivery_outcomes
BEGIN
  SELECT RAISE(ABORT, 'wake_delivery_outcomes is append-only');
END;

CREATE TRIGGER wake_delivery_no_delete
BEFORE DELETE ON wake_delivery_outcomes
BEGIN
  SELECT RAISE(ABORT, 'wake_delivery_outcomes is append-only');
END;

CREATE TRIGGER wake_delivery_no_after_final
BEFORE INSERT ON wake_delivery_outcomes
WHEN EXISTS (
  SELECT 1 FROM wake_delivery_outcomes
  WHERE wakeId=NEW.wakeId AND kind IN ('handled','undeliverable')
)
BEGIN
  SELECT RAISE(ABORT, 'wake delivery already final');
END;
```

Create the deterministic migration-conflict table in the successor shape:

```sql
CREATE TABLE wake_migration_conflicts (
  wakeId           TEXT PRIMARY KEY REFERENCES wakes(wakeId),
  predecessorShape TEXT NOT NULL
    CHECK (predecessorShape = 'coordination-fabric-v1-phase1-v3'),
  reason           TEXT NOT NULL CHECK
    (reason IN ('alert_user_unknown','pending_with_linked_turn',
                'canceled_with_linked_turn')),
  priorWakeState   TEXT NOT NULL CHECK
    (priorWakeState IN ('pending','fired','canceled')),
  priorTurnStatus  TEXT NULL CHECK
    (priorTurnStatus IN ('queued','running','delivered','canceled',
                         'failed','failed_unknown')),
  recordedAt       INTEGER NOT NULL CHECK (recordedAt >= 0),
  principal        TEXT NOT NULL CHECK (principal = 'process:tightbeam')
);
```

The v4 `wake_cancellations` shape extends `reasonKind` with
`alert_user_unknown | quiescence_invalidated` and `causalSourceKind` with
`schema_transition | owner_turn_admitted`. Its compatibility check admits exactly two
new pairs:

| Requester | Reason | Source kind | Outcome | Authority |
|---|---|---|---|---|
| `tightbeam:schema-migration` | `alert_user_unknown` | `schema_transition` | `no_replacement` | v3-to-v4 transition only |
| `tightbeam:quiescence-guard` | `quiescence_invalidated` | `owner_turn_admitted` | `no_replacement` | R13 act-edge guard only |

The `Wakes` validation allowlists and successor-registry DDL shall carry those exact
pairs. A public cancellation caller receives neither requester authority.

The mutation seam uses these cause pairs:

| Transition | `causeKind` | `causeId` |
|---|---|---|
| initial `attempt` and `admitted` | `scheduler_due` | `wake:<wakeId>` |
| retry `attempt` and `admitted` | `retry_due` | `outcome:<priorFailedOutcomeId>` |
| session-lane `handled` and `failed` | `turn_terminal` | `turn:<turnSeq>` |
| parent-target transfer `failed` and `undeliverable` | `parent_target_retired` | `transfer:<transferEvidenceId>` |
| retirement `failed` and `undeliverable` | `recipient_retired` | `session:<sessionKey>` |
| unclaimable `failed` and any immediate `undeliverable` | `recipient_unclaimable` | `session:<sessionKey>:<closedReason>` |
| boot-recovery `failed` and `undeliverable` | `boot_recovery` | `turn:<turnSeq>` |
| target-resolution `undeliverable` | `target_unresolvable` | `role:<targetRole>` when a role was requested; otherwise `session:<sessionKey>` |
| exhausted `undeliverable` | `retry_exhausted` | `outcome:<finalFailedOutcomeId>` |
| unsafe `undeliverable` | `unsafe_failure` | `outcome:<failedOutcomeId>` |
| migrated outcome | `legacy_import` | `wake:<wakeId>` |

Each runtime row in this table uses principal `process:tightbeam`. The wake and typed
cancellation rows retain their existing creator and requester principals.

Add nullable quiescence guard columns to `wakes`:

```sql
invalidationKind TEXT NULL
  CHECK (invalidationKind IN ('owner_turn_admitted')),
invalidationOwnerUserId TEXT NULL,
invalidationAfterTurnSeq INTEGER NULL
```

A table check requires the three invalidation columns to be null together or populated
together.

Add these immutable Wake Bubble route columns to `wakes`:

```sql
bubbleAlertUserId TEXT NULL,
bubbleStartSessionKey TEXT NULL,
CHECK (bubbleStartSessionKey IS NULL OR bubbleAlertUserId IS NOT NULL)
```

`schedule_in_txn` writes them once for a prompt wake under R5. Migration writes them
only for a preserved pending prompt wake. No later target re-resolution mutates them.

Existing `wakes.state` remains the compatibility aggregate:

- initial admission changes `pending` to `fired`;
- pre-admission cancellation and quiescence invalidation change `pending` to `canceled`
  through typed cancellation;
- an ordinary target absence changes `pending` to `canceled`; a condition or fallback
  target absence preserves its already-claimed `fired` state and `firedBy` value;
- retry, handled, failed, and post-admission undeliverable outcomes leave the aggregate
  state `fired` and use `wake_delivery_outcomes` as their detailed truth.

The existing `wake_fired` lifecycle marker and `wakes.state='fired'` mean that the prompt
act edge was claimed. A condition or fallback target failure can be fired without a
turn. Only an `admitted` outcome proves admission, and only a typed final outcome proves
handling or undeliverability.

### Read projection

Add wire verb and CLI command `wake-get <wakeId>`. Its result has this fixed shape:

```text
{
  wakeId, state, latestOutcome, attemptCount, turnSeq, nextRetryAt, failureClass,
  outcomes: [
    {attemptNo, kind, turnSeq, at, retryAt, failureClass,
     cause: {kind, id}, principal, bubbleRoute?}
  ]
}
```

`latestOutcome` is the newest outcome by outcome id. `attemptCount` is the number of
distinct `attempt` outcomes. `turnSeq` is the newest non-null linked turn. `nextRetryAt`
is non-null only while a retry-eligible failed outcome has no later attempt or final
outcome. `failureClass` is the newest failed outcome's class, including after final
undeliverable. `outcomes` is ordered by outcome id. The linked work-item trace embeds the
seven scalar summary fields but does not duplicate the history array.

A pending wake and an R18 canceled-without-turn wake have `latestOutcome=null`,
`attemptCount=0`, null turn, retry, and failure fields, and an empty history. Aggregate
`state`, not a fabricated delivery outcome, reports their pending or canceled condition.
An R18-preserved non-prompt wake has the same empty delivery projection while its
aggregate state continues to report its consumer-specific state.

The read handler applies R5 authorization before it queries the history. The new exact-id
read leaves the existing pending-wake list unchanged.

### Transaction order

`WakeScheduler` keeps the existing digest batcher as the first prompt controller. Before
it selects due delivery rows, it groups the eligible `digest=0` prompt members by the
existing `deliveryRule`. One group transaction rechecks the boundary or ceiling, creates
one `digest=1` carrier, commits each member's typed `superseded` cancellation with that
carrier as its replacement, and writes `wake_digest_materialized`. The carried members
do not enter admission, create delivery outcomes, or create turns. The carrier can enter
the remaining due-row pass once, and its `digest=1` value excludes it from batching.

A refused member cancellation or another group error rolls back the carrier, member
cancellations, and materialization lifecycle together. The existing failure seam records
`wake_digest_materialization_failed` after that rollback and leaves the members pending.
The batcher does not change the existing schedule for a group that has not reached its
boundary or ceiling.

For a remaining supervision-owned prompt wake, `WakeScheduler` next runs the existing
work-blocked recognition. Its successful typed cancellation and prod refund stop the
act. Internal consumers retain their existing consumer-specific delivery path and do
not enter the delivery-outcome mechanism.

During the R18 v3-to-v4 transition, `Schema` applies the same boundary before it maps a
legacy wake. It preserves a non-prompt wake and its consumer-specific history without a
delivery outcome or Wake Bubble route. It applies attempt, admission, and final-outcome
backfills only to `consumer='prompt'` rows.

Each remaining prompt wake enters one transaction. `Wakes.claim_prompt_in_txn` loads
the row, rechecks its ordinary-due, condition-fact, or fallback-deadline guard, and runs
R13. The gateway then runs the existing target, reply, enqueueability, and supervision
controller seams. A controller cancellation commits its current cancellation,
entitlement, refund, and lifecycle effects with no delivery outcome.

After those gates admit, the transaction appends one prompt echo, enqueues
`{wakeId, wakeAttempt=0}`, settles the supervision controller, appends `attempt` and
`admitted`, changes the wake through R1's checked CAS, runs routing-bracket re-arm, and
writes condition/fallback lifecycle provenance. Commit is followed by the existing echo
publication and lane nudge. Any error rolls back that closed set.

An ordinary target-resolution failure appends a null-turn `attempt` and
`undeliverable`, copies the Wake Bubble route, and consumes the pending wake as
`canceled` through typed target-unresolvable cancellation. A condition or fallback
target-resolution failure performs the same outcome writes after its variant claim, so
it retains `state='fired'`, `firedBy`, and its existing lifecycle event. Neither path
commits a message or turn. An unavailable supervision controller keeps its existing
typed cancellation instead and creates no delivery outcome.

If a retry transaction finds no target, it appends the null-turn `attempt`, copies the
Wake Bubble route into `undeliverable`, and leaves the compatibility wake state `fired`.

Retry admission uses the first echo's message id and prompt. It inserts no second echo.
It enqueues `{wakeId, wakeAttempt=n+1}`, appends `attempt` and `admitted`, and consumes
the exact failed row's retry eligibility in one transaction. It does not rerun initial
prompt controllers. The uniqueness constraints make replay return the existing
admission.

Turn finalization changes from separate terminal writers to this composition:

1. The source writer calls `Ledger.terminalize_in_txn/3` with a closed source tag,
   terminal values, and its source-specific guard.
2. The bridge applies the guarded update with `RETURNING`. The SessionLane guard is the
   running-to-terminal CAS. The retirement guard selects queued turns for the retiring
   session. The parent-target retirement guard selects the one queued transfer carrier
   named by its transfer evidence. The unclaimable guard selects queued turns with the
   closed no-active-session predicate. The boot guard selects running turns for recovery.
3. For each returned wake-linked row, the bridge calls
   `Wakes.settle_terminal_rows_in_txn/4`. A delivered row appends `handled`. A failed,
   failed-unknown, or canceled row appends `failed` and either stores the exact retry or
   appends `undeliverable` under R8.
4. A returned non-wake row commits only its turn terminal state. A Bubble notice is a
   non-wake row because its wake identity is null.
5. The source writer adds its existing typed lifecycle effects in the same transaction.
6. The transaction commits, then terminal publication, supervision recognition, and
   Bubble recognition run from the committed rows.

A failure in steps 2-5 rolls back the source writer's returned turn rows, wake outcomes,
and lifecycle effects together. A guard loser returns no row and creates no outcome.

### Wake Bubble route capture

`Wakes.schedule_in_txn` derives the alert user from typed rows in R5's fixed order. A
role target contributes its role row only when the earlier origin and linked-work rows do
not identify the alert user. The transaction records the resolved target session as the
lineage start when resolution succeeds. A later role rebind, owner-row change, target
retirement, or resolution failure does not rewrite that snapshot.

The route is sender-visible fault custody, not delivery authority. Delivery still uses
the existing target resolution and role-fallback rules. A null-turn final outcome copies
the route only so Bubble can tell the stored user and, when available, climb from the
stored session. An outcome with a linked turn continues to use that turn's actual target
and owner.

### Failure and Bubble integration

The adapter boundary returns a typed run-admission disposition beside its error. The
gateway maps checkout and session-stage failures directly to `could_not_run`. Adapter
implementations map protocol evidence to `could_not_run`, `run_failed`, or
`outcome_unknown`. The default for absent protocol evidence is `outcome_unknown`.

Bubble extends its cause model with a typed wake cause. The display request reference is
`bubble:wake:<wakeId>`, but the durable dedupe identity is the R9 notice tuple. For a
wake-linked failed turn, its left-hand side reads the wake's final outcome. A
retry-pending failure does not match. An undeliverable runtime outcome matches once.

Gateway notice admission accepts `notice_dedupe={kind, causeKind, causeId,
recipientSessionKey}` separately from `wake_id` and `wake_attempt`. Bubble supplies the
notice tuple and omits both wake fields. Ledger maps the unique notice-index conflict to
the existing already-admitted result. Existing non-wake Bubble causes retain their
request references and prompts while moving their dedupe identity out of `turns.wakeId`.
This prevents a notice terminal from creating a wake outcome, retry, or recursive wake
cause.

`BubbleSweeper` retains its turn cursor and adds the `bubble:wake-outcome` cursor over
append-only outcome ids. Both the terminal cast and the outcome-id cast are hints; both
cursors are the boot-recovery authority. Wake recognition loads the final outcome. It
derives context from the linked turn or reads the stored null-turn route. The existing
lineage resolver, notice-turn evidence, owner terminal-alert transaction, and
`user-alerted` fact remain authoritative. A null start session invokes the same terminal
alert directly; it does not create a synthetic session or parse a role.

### Supervision integration

Add the terminal failure-class read to the declared prod left-hand side before the
production returns `{:match, assignment}`. Add `holder_gagged` to the closed no-match
vocabulary. `evaluate_terminal` handles that result before it passes a verdict into the
turn-end prod schedule. The handler writes the existing terminal watermark plus the
named lifecycle row in one transaction and returns `:gagged`.

This is a gate on observable terminal truth, not an inferred holder state. It adds no
standing-fact authority and no threshold.

### Quiescence integration

The scheduling handler resolves the self session and owner from rows. It captures:

```sql
SELECT COALESCE(MAX(t.seq), 0)
FROM turns t
JOIN sessions s ON s.sessionKey=t.sessionKey
WHERE t.origin='user:' || ?1 AND s.ownerUserId=?1
```

At admission, R13 checks for a row above that cursor in the same transaction that would
admit the wake. The activity row is the event; due time is only the wake's existing wait
bound.

### Migration order

The application shall call `Schema.migrate_known_shape/1` before `Schema.ensure_all/1`
and before `Wakes`, `LaneManager`, `Supervision`, or Bubble starts. The migration shall
select its plan only from the exact stamp. For the v3 plan, the database-owner connection
shall disable foreign-key enforcement before it begins the exclusive transaction. The
transition and clean-v4 bootstrap shall both consume `Schema.successor_registry/0`.
The transaction shall:

1. acquire the write lock and recheck that exactly one v3 stamp remains;
2. load the registry, reject a duplicate owned name or missing dependency, and compute
   the complete dependency closure for each rebuilt predecessor table;
3. create code-defined temporary v4 successors for each table in the affected closure,
   including `wakes`, `wake_cancellations`, and `turns`, then create the new outcome and
   migration-conflict successor tables;
4. copy another affected child table value-for-value; add route and quiescence columns;
   set each lawful linked-turn attempt identity; migrate each exact legacy Bubble
   identity into the typed notice columns; and reject another non-null legacy turn wake
   id with `ShapeError`;
5. derive the Wake Bubble route for each preserved pending prompt wake;
6. for each R18 `alert_user_unknown` case, insert its typed cancellation while the wake
   is pending and then change that wake to the cancellation's state and timestamp;
7. backfill R18 outcomes and conflict rows from structured pre-normalization values;
8. drop the affected predecessor triggers and indexes in reverse dependency order,
   then drop affected child tables before their rebuilt parents;
9. rename successor parents before successor children, then create the registry's
   remaining tables, indexes, and triggers in dependency order;
10. compare normalized `sqlite_master` SQL with each registry record, reject a missing,
    mismatched, extra duplicate, or unreachable owned object, and require an empty
    `PRAGMA foreign_key_check` plus an `ok` `PRAGMA integrity_check`;
11. change the single shape stamp from v3 to v4 as the final mutation and commit.

After commit, the owner connection shall restore foreign-key enforcement, re-read the
single v4 stamp, and run `Schema.ensure_all/1`. The application shall repeat that
validation on a clean restart. Neither validation may add or replace an object. A
failure before commit shall roll back the successor tables, copied rows, normalizations,
cancellation rows, outcome rows, conflict rows, dependent objects, and stamp change. No
database-consuming component shall start after that failure. A later v4 startup shall
validate without running the transition again.

The migration reads structured row columns. It does not parse chat or error prose.

### Exact implementation surfaces

- Extend `lib/tightbeam/schema.ex` with the exact v3-to-v4 shape gate,
  `successor_registry/0`, successor tables, complete dependency closure, normalized
  object checks, rollback, and final stamp change. Use the same registry for clean-v4
  bootstrap and validation.
- Amend `lib/tightbeam/application.ex` so the known-shape gate and successor validation
  finish before another database consumer starts.
- Extend `lib/tightbeam/wakes.ex` with the outcome schema, controller-aware admission
  CAS, retry query, terminal seam, quiescence guard, Wake Bubble route, projections, and
  migration helpers. Preserve the batcher's group membership, `digest=1` carrier,
  typed member replacement, lifecycle, rollback, and before-due-selection position.
- Extend `lib/tightbeam/ledger.ex` with `wakeAttempt`, `failureClass`, the typed notice
  columns and unique notice dedupe, plus `terminalize_in_txn/3`. Replace each direct
  bulk terminal writer with that bridge.
- Amend prompt delivery and notice admission in `lib/tightbeam/gateway.ex`; remove the
  prompt path's split `mark_fired` edge, accept `notice_dedupe` separately from wake
  identity, pass `process:tightbeam` as the wake-outcome principal, and retain the
  authenticated retirement principal on existing retirement lifecycle, cancellation,
  and sidecar evidence.
- Amend `lib/tightbeam/session_lane.ex` so the lane terminal CAS uses the bridge. Amend
  `Ledger.drain_queued_for_retire_in_txn`, `Ledger.fail_unclaimable`, and
  `Ledger.recover_running` so their current transactions use the same bridge.
- Amend `lib/tightbeam/supervision.ex` so `parent_target_retired` replaces its direct
  queued-turn cancellation with the bridge, chooses the existing deterministic
  retirement replacement kind and inputs before terminalization, and then materializes
  one replacement entitlement or wake and its linked sidecar outcome. Commit the bridged
  terminal, replacement, sidecar, and existing lifecycle together.
  Preserve `Org.retire_in_txn` ordering so this transition finishes before the session
  state change and before the generic retirement drain.
- Amend `lib/tightbeam/productions/bubble.ex` to recognize a runtime undeliverable wake
  as one typed cause from linked-turn or stored null-turn context and to admit each
  notice with null wake identity plus the typed notice tuple.
- Amend `lib/tightbeam/productions/bubble_sweeper.ex` with the append-only outcome-id
  feed and `bubble:wake-outcome` cursor while retaining its turn feed.
- Amend `lib/tightbeam/supervision.ex` with the typed GAGGED no-match and atomic
  consumption.
- Add the `wake-get` wire verb and Rust CLI command. Add the invalidation wire field and
  Rust CLI flag without changing the unguarded wake request.
- After the mechanism passes its acceptance tests, update the wake paragraph in
  `priv/guidance/operating-manual.md` and the CLI help in one guidance batch. Publish no
  pre-mechanism directive.
- Update wake, batcher, ledger, gateway, Bubble, supervision, controller-preservation,
  schema-shape, dependency-trigger, soak, and trace tests.

No source edit is authorized by this specification. These paths name the later build
surface.

### Traceability

| Requirement | Implementation seam | Acceptance |
|---|---|---|
| R1-R4 | Batcher group transaction, Wakes admission/cancel CAS, Gateway transaction, existing prompt controllers, turn indexes | A1, A10 |
| R5-R7 | outcome table, Wake Bubble route, Ledger terminalization bridge, lane, parent-target retirement, generic retirement, unclaimable, and boot writers | A2, A3, A6, A10 |
| R8-R10 | retry query, scheduler, typed Bubble cause and notice dedupe | A2, A3, A6, A7 |
| R11 | Supervision terminal LHS, watermark, lifecycle | A3 |
| R12-R13 | wake guard columns, scheduling handler, admission transaction | A4 |
| R14 | existing claim and turn-boundary seams | A5 |
| R15-R16 | Wakes mutation API, Ledger terminalization bridge, closed source tags, process outcome principal, and authenticated cancellation/sidecar retirement principal | A1-A4, A6 |
| R17 | bridged boot recovery, retry query, and both Bubble cursors | A2, A6, A7 |
| R18 | Schema exact-shape gate, successor registry, notice migration, Wakes migration seam, and Ledger successor table | A8 |
| R19 | CLI help and operating-manual wake paragraph | A9 |

## Acceptance

Tests use the real SQLite owner, wake store, turn ledger, gateway delivery transaction,
session lane, scheduler, terminal publisher, Supervision, and Bubble production. Adapter
failure fixtures come from captured typed adapter responses. Hand-written ideal response
maps do not satisfy the adapter-boundary cases.

### A1 — Deterministic cancel-versus-admit race

Given one pending prompt wake and barriers that force cancellation to commit before the
admission CAS, when admission resumes, then cancellation returns success, the wake is
`canceled`, one typed cancellation exists, and no message, turn, `attempt`, or `admitted`
outcome exists.

Given the same fixture with barriers that force admission to commit first, when
cancellation resumes, then admission returns appended, cancellation returns false, the
wake is `fired`, one message exists, one attempt-0 turn exists, and exactly one `attempt`
plus one `admitted` outcome links that turn. Proves R1-R4, R15-R16.

### A2 — Failed retry, recovery, and exhaustion

Given retry delays `[10, 20]`, a fake clock, and a captured adapter response classified
`could_not_run`, when attempt 0 fails at time 100, then one failed outcome links attempt
0, `retryAt=110`, no final outcome exists, and Bubble has no wake cause. A scheduler pass
at 109 admits no turn. A pass at 110 admits attempt 1 once.

Given attempt 1 then reaches delivered, when the terminal transaction commits, then one
handled outcome links attempt 1, later scheduler passes admit no turn, and no
undeliverable or wake Bubble exists.

Given a fresh copy where attempts 0, 1, and 2 each fail `could_not_run`, when the clock
reaches each retry time, then three attempt identities and three turns exist. Attempt 2
commits one undeliverable outcome. Repeating the scheduler and Bubble recognizer creates
no fourth attempt and no second logical wake cause. Proves R3-R10, R15-R17.

Given that exhausted wake cause and one existing turn-sequence Bubble cause both target
the same recipient, when Bubble admits their notices, then the rows carry distinct typed
identities `{'bubble','wake',wakeId,recipient}` and
`{'bubble','turn',turnSeq,recipient}`. Each notice has null `wakeId` and `wakeAttempt`.
Terminalizing either notice creates no wake outcome, retry, or recursive wake cause.

When `wake-get` and the linked work-item trace read that exhausted fixture, then they
expose `undeliverable`, attempt count 3, the final turn sequence, a null next retry, and
`could_not_run`. `wake-get` returns the outcomes in id order; each row carries its
specified cause and `process:tightbeam` principal. A caller with no R5 authority receives
`denied`; an authorized query for an absent id receives `unknown_wake`.

### A3 — Repeated carrier failure precedes negligence prod

Given a holder with an open assignment and the exhausting fixture from A2, when
Supervision inspects each failed terminal, then `prod_production_matches?` returns the
`holder_gagged` no-match and `evaluate` returns `:gagged`. Each evaluation advances the
terminal watermark once, writes one typed GAGGED lifecycle row, preserves the prod
counters and entitlement, and creates no prod wake.

When the final failure also commits undeliverable, then the existing Bubble path creates
one logical escalation whose first notice says the exact wake id and final turn sequence.
Repeated supervision sweeps and Bubble recognition create no negligence prod and no
second logical cause. Proves R7-R11, R16.

Given the retirement and boot-recovery fixtures from A6, when Supervision observes their
`carrier_canceled` and `outcome_unknown` terminals before another prod cycle, then it
consumes each as GAGGED with the stored class and creates no negligence prod.

### A4 — Stale-quiescence invalidation

Given session `S1` is running an owner-origin turn for user `mike`, when `S1` schedules a
delayed self-wake with `--cancel-on-owner-activity`, then the wake stores owner `mike` and
the current owner-turn cursor.

Given a later `user:mike` turn is admitted to another mike-owned session `S2`, when the
quiescence wake reaches its act edge, then one typed cancellation names
`owner_turn_admitted:<S2 turn seq>`, the wake becomes canceled, and no prompt echo, turn,
attempt, or admitted outcome is created for it.

The cancellation row shall contain requester `tightbeam:quiescence-guard`, reason
`quiescence_invalidated`, source kind `owner_turn_admitted`, source id equal to `S2`'s
decimal turn sequence, and outcome `no_replacement`. The source validator shall prove
the stored owner, cursor, origin, and target-owner predicates. The lifecycle row shall
use principal `process:tightbeam`.

Given the same command is supplied through the public cancellation surface, or names a
missing, stale, other-owner, or other-target turn, when validation runs, then it returns
the existing cancellation refusal and changes no wake, cancellation, outcome, or turn.

Given a clean v4 bootstrap and a v3-to-v4 migration, when the successor registry is
validated, then both contain the exact R13 reason/source/requester pair. The migrated
v3 fixture creates no quiescence cancellation because no predecessor row can carry the
new guard.

Given the same scheduled fixture with no owner turn above its cursor, when the wake acts,
then it follows A1's admission path. Proves R4, R12-R13, R15-R16.

Given the invalidation flag on an immediate wake, a non-session caller, or a wake whose
target resolves to another session, when scheduling validates the request, then it
returns `invalid_invalidation_guard` and inserts no wake row.

Given a guarded self-wake was scheduled through a role that then binds to another
session, when the wake reaches its act edge without later owner activity, then it admits
to the stored self session. The new role holder receives no carrier turn.

Given transaction barriers force the owner turn to commit first, the wake invalidates as
above. Given barriers force wake admission to commit first, the wake has one admitted
turn and the later owner turn does not rewrite that outcome.

### A5 — Queued wake preserves the tune boundary

Given session `S` selects model A and its live lane is idle, when a prompt wake admits
attempt 0 while a barrier holds the post-commit lane nudge, then its queued turn has no
claimed model or adapter generation. When an authorized caller attempts to tune `S` to
model B while that row is queued, then the tune returns `turn_in_progress`; the session
selection and engine remain model A and the queued row remains unchanged.

When the barrier releases the nudge, the lane claims the queued wake turn, stamps model
A and its current harness, runs through model A's adapter, and reaches handled. Only
after the terminal commits may the same authorized tune change `S` to model B.

The fixture shall contain one wake turn, one attempt, one admission, one handled outcome,
no failed outcome, no retry, and no Bubble cause. It shall also prove that the refused
tune changed no model, harness, adapter generation, or engine process. Proves R14 and
retains the fixed C limb.

### A6 — Unsafe and recovered failures do not replay

Given one wake turn fails after prompt admission with class `run_failed`, when its
terminal transaction commits, then it records failed plus undeliverable, schedules no
retry, and starts one wake Bubble cause.

Given an admitted wake turn is canceled through the existing current-run cancellation
seam, when the canceled-terminal CAS commits, then the turn retains status `canceled`,
stores `run_canceled`, records failed plus undeliverable, schedules no retry, and remains
GAGGED to Supervision.

Given a running wake turn exists when the gateway stops, when boot recovery changes the
turn to `failed_unknown` with class `outcome_unknown`, then it records failed plus
undeliverable and admits no replacement turn. Proves R6-R10 and R17.

Given a queued supervision transfer carrier targets parent session `P`, when an
authenticated principal retires `P`, then the parent-target transition first chooses one
existing deterministic `child_rearm`, `parent_elevation`, or `main_elevation`
replacement kind and its inputs. The shared bridge then changes the transfer turn to
`canceled` with `carrier_canceled` and appends failed plus undeliverable with cause
`parent_target_retired`, source id `transfer:<transferEvidenceId>`, and outcome principal
`process:tightbeam`. The transition next materializes exactly one replacement entitlement
or wake and a sidecar outcome that identifies it. The same outer transaction commits the
bridged terminal and outcome, replacement, sidecar with the authenticated retirement
principal, existing retirement lifecycle, and session retirement. The generic
retirement drain does not return that turn; the
replacement suppresses a second Bubble climb; no retry is scheduled.

Given an injected bridge, replacement, sidecar, or outcome failure, when that transaction
rolls back, then `P` remains active, the original transfer carrier remains queued, and no
wake outcome, replacement, or retirement sidecar row is created. A repeated successful
retirement creates no second replacement or outcome.

Given a queued wake carrier belongs to a session that an authenticated principal retires,
when the retirement transaction drains that queue, then the shared terminalization
bridge changes the turn to `canceled` with `carrier_canceled`, appends failed plus
undeliverable with cause `recipient_retired` and outcome principal
`process:tightbeam`, schedules no retry, and leaves the original wake final. The typed
retirement lifecycle and any typed cancellation retain the authenticated retirement
principal. Bubble admits one sender-visible cause. An injected outcome-write failure
rolls back the turn, outcomes, retirement lifecycle effects, and session retirement
together.

Given a queued wake carrier becomes unclaimable because its session is retired, when the
backstop transaction runs, then the same bridge changes the turn to `canceled` with
`carrier_canceled`, appends failed plus undeliverable with cause
`recipient_unclaimable`, uses `process:tightbeam`, and schedules no retry. Given the
closed legacy `no_session` fixture instead, the bridge stores `failed` with
`could_not_run` and applies the normal retry rule. A repeated backstop pass changes no
row and appends no duplicate outcome.

Given an initial wake's target becomes unresolvable before admission, when the wake acts,
then one null-turn attempt and one target-unresolvable undeliverable outcome commit, the
compatibility wake state becomes canceled through typed provenance, one wake-named
Bubble cause starts, and no prompt echo or turn exists. The outcome copies the scheduling
transaction's `bubbleAlertUserId` and `bubbleStartSessionKey`.

Given that target's role and owner row are absent at act time, when Bubble recognizes the
outcome, then it uses the stored alert user. When the stored start session exists, Bubble
starts with that session's lineage. When the stored start session is null or absent,
Bubble commits the existing terminal alert directly for the stored user. It does not
create a synthetic session or use the role name as lineage.

Given the gateway stops after the null-turn undeliverable commits but before its outcome
cast runs, when Bubble boots, then the `bubble:wake-outcome` cursor recognizes that
outcome. Repeating the cast and sweep admits no second notice for one recipient and no
second logical wake cause.

### A7 — Restart preserves a due retry

Given attempt 0 commits `could_not_run` with `retryAt=110` and the gateway stops at 105,
when it restarts at 110, then the boot scheduler admits attempt 1 once. A second restart
preserves both attempt identities and does not move `retryAt`. Proves R3, R8, R17.

Given an undeliverable outcome commits and the gateway stops before Bubble admits its
first notice, when it restarts, then Bubble admits one wake-named logical cause. A second
restart creates no second notice for the same recipient and no second logical cause.
Proves R9 and R17.

Given one wake cause and one existing turn cause each crash after their first notice
commits but before their cursors advance, when Bubble restarts and recognizes both causes
again, then the typed wake and turn notice tuples return the existing rows. The restart
adds no notice, wake outcome, retry, or recursive cause.

### A8 — Legacy migration preserves evidence

Given an exact v3-stamped fixture with one row for each R18 wake-shape and terminal
mapping, when the application starts, then the shape gate selects the v3-to-v4 plan,
unchanged columns compare equal, each linked prompt turn has `wakeAttempt=0`, each shape
has the specified outcomes, and each normalization has one conflict row that preserves
its prior state. A canceled prompt wake's queued or running carrier is `failed_unknown`
and does not run. Restarting the v4 database produces no second backfill row, conflict
row, retry, or retroactive Bubble notice. Proves R18.

The fired prompt-without-turn fixture shall have `attempt` plus `undeliverable`,
`causeKind='legacy_import'`, a null `failureClass`, and no Bubble route. `wake-get` shall
return a null failure class for it.

Given a successful fired `consumer='effort_deadline'` wake with no prompt turn and its
pending replacement deadline, when migration commits, then the original retains its
exact consumer, state, fired time, payload, and consumer-specific lifecycle rows. The
replacement retains its exact pending state and schedule. Both rows have a null Wake
Bubble route and zero delivery outcomes. Their exact-id reads return
`latestOutcome=null`, `attemptCount=0`, a null linked turn, and an empty outcome history.
Restarting v4 changes no row and creates no outcome, conflict, retry, or Bubble notice.

The pending prompt fixture whose alert user cannot be derived shall first gain one
cancellation with the exact requester, reason, causal source, outcome, work-impact,
liveness, action-needed, replacement, and timestamp fields from R18. It shall then
become canceled at that same timestamp, gain the specified `alert_user_unknown`
conflict and legacy outcomes, and cease to be eligible for runtime admission. The typed
pending-insert and wake-update cancellation triggers shall accept that migration pair
and shall continue to reject an unproved cancellation or another requester using the
new reason or causal-source value.

The clean-v4 and migrated-v4 cancellation DDL and validator shall also accept only R13's
`tightbeam:quiescence-guard | quiescence_invalidated | owner_turn_admitted |
no_replacement` runtime pair after its source-row proof. The v3 copy shall create no
such cancellation. A public caller or another process requester using any member of
that pair shall be rejected.

Given the v3 fixture contains a fired-lineage row and a liveness checkpoint binding,
when migration commits, then each named predecessor turn index exists, the binding still
references its source turn, and both fired-lineage immutability triggers still reject an
update or delete. The checkpoint-binding coherence trigger shall still reject an
incoherent insert. The successor outcome append-only and final-outcome triggers shall
reject their prohibited mutations.

Given the fixture contains an exact legacy Bubble notice identity, when migration
commits, then its request reference, prompt, origin, target, status, and timestamps stay
equal; its typed notice tuple names the turn cause and recipient; its wake fields are
null; and it creates no wake outcome. Given a non-null legacy `turns.wakeId` that matches
neither a wake row nor the exact Bubble relation, when migration runs, then it returns
`ShapeError`, preserves v3, and changes no row or object.

Given a legacy turn links to a non-prompt wake, when migration runs, then it returns
`ShapeError`, preserves v3, and creates no attempt number, delivery outcome, or Bubble
route.

The migration test shall enumerate `Schema.successor_registry/0` and assert that its
normalized records equal the complete owned-object set produced by clean-v4 bootstrap.
It shall reject a missing, duplicate, mismatched, or dependency-unreachable record. The
transition shall rebuild each affected table, index, and trigger in registry dependency
order. Immediate `Schema.ensure_all/1` and a clean restart shall execute no DDL and shall
leave each normalized object definition equal.

A source census shall reject a schema-owner `CREATE TABLE`, `CREATE INDEX`, or
`CREATE TRIGGER` statement that does not originate from one exported registry record.
This check covers `Wakes`, `Ledger`, supervision liveness, and supervision enforcement,
so a clean bootstrap cannot make an unregistered owned object invisible to the registry
comparison.

Given a non-empty database with no stamp, multiple stamps, or a stamp other than v3 or
v4, when the shape gate runs, then startup returns `ShapeError`, runs no successor DDL,
and starts no database consumer. Given an injected failure during copy, normalization,
dependent-object creation, either integrity check, or the stamp change, when the
transaction rolls back, then the database retains the v3 stamp and its predecessor
tables and rows. Given that restored fixture starts again without the injection, then
one v4 migration commits. Given that v4 database starts once more, then validation is
read-only and its rows and object definitions compare equal. Proves R18.

### A9 — Guidance source closure

Given a built release in which A4 passes, when the assembled identity and CLI help are
inspected, then each contains the exact `--cancel-on-owner-activity` spelling and the
delayed-self-wake scope from R19. Given a source tree in which the guard mechanism or A4
is absent, then the source-closure check rejects that directive. Proves R19.

### A10 — Existing prompt controllers survive admission replacement

Given one eligible batch group with two `digest=0` prompt members, when the scheduler
runs the first controller, then one `digest=1` carrier, two typed `superseded`
cancellations that name the carrier as replacement, and one
`wake_digest_materialized` lifecycle commit in the group transaction. The two members
create no delivery outcomes, echoes, or turns. The carrier enters the remaining due-row
pass once, can admit as attempt 0 in that pass, and is not selected as a batch member.

Given the typed cancellation refuses one eligible member, when batch materialization
runs, then the group transaction creates no carrier, cancellation, or materialization
lifecycle and leaves both members pending. The failure seam records one
`wake_digest_materialization_failed` lifecycle. Given a group that has not reached its
existing boundary or ceiling, when the scheduler runs, then its members, fallback, and
sender schedule remain unchanged.

Given a due supervision wake with a pending liveness sidecar and an enqueueable target,
when attempt 0 admits, then the sidecar admits and settles once against the carrier turn,
the existing entitlement charge stays single, and the same transaction commits one
attempt plus one admission.

Given the same sidecar returns its existing controller cancellation, when the wake acts,
then the typed cancellation and controller state commit, and no echo, turn, delivery
outcome, bracket re-arm, or condition/fallback lifecycle exists.

Given a due supervision wake whose target is unavailable, when the existing unavailable
controller seam acts, then its cancellation, liveness trigger, and lifecycle event commit
without a delivery outcome. Given a standing work-blocked fact appears before act, when
the scheduler recognizes it, then the supervision wake cancels, the charged prod rung is
refunded once, and admission does not open.

Given a routing-bracket wake whose work item remains holderless and non-terminal, when
attempt 0 admits, then `rearm_on_fire_in_txn` records one replacement in the admission
transaction. A replay of the same attempt records no second replacement.

Given one matching condition wake and one elapsed fallback wake, when they admit, then
their rows retain `firedBy='condition'` and `firedBy='fallback'` respectively. Each row
has its existing lifecycle event, one attempt, one admission, and one carrier turn.

Given the condition target becomes unresolvable, when its act transaction commits, then
`firedBy='condition'`, the matched-fact lifecycle provenance, one null-turn attempt, and
one undeliverable outcome commit together. No echo or turn exists.

Given an injected transaction error after supervision settlement or routing re-arm but
before commit, when the transaction rolls back, then the wake remains pending and the
controller, entitlement, message, turn, outcome, re-arm, and lifecycle rows equal their
pre-act fixture. Proves R1-R5 and R15-R16.

## Open Questions

No open question remains. The specification has no blocking or non-blocking hole. A
change to the retry schedule, safe-failure vocabulary, named owner activity,
final-outcome vocabulary, or
legacy migration ruling requires an amendment and a new content hash before build
handoff.
