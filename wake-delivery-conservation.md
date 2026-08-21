# Wake delivery conservation

Status: FROZEN FOR INDEPENDENT REVIEW

Work item: `wi_113d569f-7aff-412b-aec3-0c21f2e87f40`

Source baselines:

- installed Tightbeam 0.1.7 at commit
  `6c13efcbe9e1ae247b8aa7e91a374015c74dc947`;
- `origin/main` at commit
  `ac8651dcb104f312da1c67e0cb7b1abebc640b2b`.

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

Each load-bearing clause below was re-derived from the durable rows and both source
baselines. Neither missing artifact supplies authority to a requirement.

### Baseline reconciliation

| Limb | 0.1.7 and current-main evidence | Ruling in this specification |
|---|---|---|
| A — cancel versus admission | `Wakes.cancel_in_txn/3` accepts a pending row, while the prompt scheduler reads pending wakes, invokes delivery outside that cancellation transaction, and marks the wake later. The callback-to-mark window remains (`lib/tightbeam/wakes.ex:323-380,895-960,1166-1207,1366-1386`). Process-origin wakes can mark inside the message/turn transaction, but that update does not assert one changed wake row (`lib/tightbeam/gateway.ex:978-1135`). These files are unchanged between the two baselines. | R1-R4 replace the split edge with one checked admission CAS shared by message, turn, and wake outcomes. |
| B — outcomes, retry, and bubble | Wake state remains `pending | fired | canceled`; turn state is durable and `wakeId` is unique, but the ledger explicitly performs no automatic retry (`lib/tightbeam/wakes.ex:63-97`; `lib/tightbeam/ledger.ex:1-18,39-76,363-449`). A failed scheduler callback merely leaves the wake pending, and the existing test has no bound or exhaustion (`test/wakes_test.exs:354-393,445-490`). Bubble dedupe is keyed by cause turn and recipient, and its prompt names only the turn (`lib/tightbeam/productions/bubble.ex:1-30,37-39,49-110,141-165`). These files are unchanged between the two baselines. | R5-R10 add typed wake outcomes, safe bounded retries, one logical undeliverable cause, and a wake-named bubble by extending the existing stores and Bubble production. |
| C — queued turn and model swap | The ledger reads the session's selected model and harness when it claims a queued turn, and the test queues before tuning then proves the live selection was stamped (`lib/tightbeam/ledger.ex:179-271`; `test/ledger_test.exs:104-133`). Model and harness changes use the session lane's turn boundary (`lib/tightbeam/session_lane.ex:90-111`; current-main `lib/tightbeam/gateway.ex:4229-4235,4361-4403`; `test/gateway_test.exs:3764-3883,5117-5257`). | R14 retains the fixed structure. A5 adds the missing combined wake regression. No model-switch mechanism is added. |
| D — quiescence | The incident row names later owner activity as the stale-premise event (`att_48fa113d-9907-4126-aff5-a1e0449b25e4`). Current main adds assignment liveness checkpoint binding for a self-scheduled wake, but it does not compare owner activity before delivery (`lib/tightbeam/gateway.ex:3535-3569`; `lib/tightbeam/supervision.ex:253-294`). The checkpoint binding is absent from 0.1.7. | R12-R13 add one typed owner-activity invalidation guard. Existing checkpoint semantics remain. |
| E — reliable handoff | Dispatch already commits the assignment, prompt echo, and turn in one transaction (`lib/tightbeam/assignments.ex:540-579,596-623`). An arbitrary wake remains a hint whose later carrier failure is not conserved, as recorded in `att_08870951-f045-42dc-844c-bc0addf16fba`. | Atomic dispatch remains authoritative. This specification closes only the ordinary wake carrier. |
| F — GAGGED versus negligence | The prod left-hand side checks terminal existence but does not read terminal status or failure class; a failed terminal can match the negligence ladder (`lib/tightbeam/supervision.ex:854-905,1000-1025,1114-1140`). | R11 makes the typed terminal failure a higher-priority, consumed fact. |
| G — O6 | O6 commits `078919d`, `67e1bcf`, `f64ffa7`, `81fbc2d`, and merge `ba5952b` are ancestors of both baselines. O6 regression tests remain at `test/gateway_test.exs:6452-6765`. | O6 is superseded for this work and stays closed. |

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
- **GAGGED**: the durable derived condition that the terminal under supervision is a
  mechanical `failed`, `failed_unknown`, or wake-linked `canceled` turn.
  `could_not_run`, `run_failed`, `run_canceled`, and `outcome_unknown` are runtime
  GAGGED classes; `legacy_outcome_unknown` is the migration class. GAGGED is not an
  agent-authored standing fact and does not assert `work-blocked`.
- **Negligence prod**: the existing supervision prompt that says a holder's turn ended
  without a filing or continuation (`lib/tightbeam/supervision.ex:3856-3865`).
- **Logical wake bubble**: the existing Bubble climb with one undeliverable wake as its
  cause. Failed notice turns can move that one climb to another recipient; they do not
  create another wake cause.
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
   (`lib/tightbeam/gateway.ex:1874-2033`). Adapter protocols do not all prove whether a
   prompt-stage inference run was admitted. R7 treats absent proof as
   `outcome_unknown`.
6. Product composition supplies the finite retry delays. This specification pins the
   shipped default to `[5000, 30000, 120000]` milliseconds. The values bound waiting;
   they do not detect an event or decide an outcome.
7. The existing Bubble production remains the single capable-parent and owner-alert
   path (`lib/tightbeam/productions/bubble.ex:1-30,112-180,332-365`).
8. User-origin turns preserve their typed `origin`, target session, and sequence in the
   turn ledger.

## Invariants

### R1 — Cancel and initial admission share one decision

`Wakes` shall admit attempt `0` only through a transaction that changes the source wake
from `pending` to `fired` with a guarded update. The transaction shall verify one changed
wake row before commit.

The same transaction shall commit the echo, turn, `attempt`, and `admitted` outcomes. A
zero-row wake update shall roll back those writes and return the losing cancel-versus-
admit result.

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

### R4 — Check and act are indivisible

Initial admission, retry admission, cancellation, quiescence invalidation, turn
terminalization, retry scheduling, and exhaustion shall evaluate their guard and commit
their action in one database transaction.

### R5 — The wake outcome history is typed and queryable

`Wakes` shall append only these wake delivery kinds: `attempt`, `admitted`, `handled`,
`failed`, and `undeliverable`.

An `admitted`, `handled`, or `failed` row shall name one `turnSeq`. An `attempt` or
`undeliverable` row shall name the turn when a turn exists. A target-resolution failure
can use a null turn link and shall name the typed target failure instead.

Each outcome shall store `wakeId`, `attemptNo`, event time, cause kind, cause id, and
principal. A failed outcome shall also store its closed failure class and optional
`retryAt`.

The caller-visible `wake-get` projection and a linked work-item trace shall expose
`wakeId`, aggregate `state`, `latestOutcome`, `attemptCount`, latest linked `turnSeq`,
`nextRetryAt`, and the latest failed attempt's `failureClass`. `wake-get` shall also
return the ordered outcome history.

The gateway shall authorize `wake-get` when the caller is an admin, the caller origin
equals the wake origin, or the caller owns the target session. It shall return
`unknown_wake` for an absent id and `denied` for an existing row outside that authority.

### R6 — Turn terminalization settles wake state atomically

When a wake-linked turn wins its terminal CAS, `SessionLane` shall call the `Wakes`
terminal mutation seam inside the same transaction.

A delivered terminal shall append one `handled` outcome. A `failed`, `failed_unknown`,
or wake-linked `canceled` terminal shall append one `failed` outcome. The canceled case
shall append `undeliverable` in that transaction. A terminal CAS loser shall append no
wake outcome.

### R7 — Failure classification is typed at the run boundary

The gateway shall persist one of `could_not_run`, `run_failed`, or `outcome_unknown` on a
failed turn and its wake-linked failed outcome. The session lane shall persist
`run_canceled` when a wake-linked admitted turn wins the existing canceled-terminal CAS.

Checkout failure and session-establishment failure shall produce `could_not_run`.
Prompt-stage failure shall produce `could_not_run` only when the adapter returns typed
proof that the inference run was not admitted. Typed proof that the run was admitted and
failed shall produce `run_failed`. A prompt-stage failure with neither proof shall
produce `outcome_unknown`. Boot recovery and a lost runner outcome shall also produce
`outcome_unknown`.

A runtime `could_not_run` or `run_failed` terminal shall use turn status `failed`. A
runtime `outcome_unknown` terminal shall use `failed_unknown`. A canceled carrier shall
retain turn status `canceled` and use failure class `run_canceled`.

The implementation shall derive an adapter failure class exclusively from the typed
stage and adapter run-admission disposition. It shall derive `run_canceled` exclusively
from the existing canceled-terminal CAS.

### R8 — Retry is finite, backoff-bound, and replay-safe

For the shipped retry schedule `[5000, 30000, 120000]`, a wake can have attempt numbers
`0`, `1`, `2`, and `3`. The scheduler shall make attempt `n + 1` eligible at
`failedAt + retryDelays[n]` for a `could_not_run` failure.

A `run_failed`, `run_canceled`, or `outcome_unknown` failure shall transition the wake to
`undeliverable` in the terminal transaction. The scheduler shall create no retry for
those classes.

A `could_not_run` failure on attempt `3` shall append `undeliverable` in the terminal
transaction. A final wake outcome shall make later scheduler passes inert.

### R9 — Exhaustion starts one logical Bubble cause

The Bubble production shall ignore a wake-linked failed turn while that wake has a
retry-eligible failed outcome.

One runtime `undeliverable` outcome shall admit one logical Bubble cause keyed by the
wake id. Bubble notice turns shall use deterministic identity
`bubble:wake:<wakeId>:<recipientSessionKey>`. Re-recognition of the outcome shall reuse
that identity.

Bubble shall scan unmatched runtime `undeliverable` outcomes during normal recognition
and boot recovery. A crash after the final outcome commits and before notice admission
shall delay that logical cause; it shall not lose or duplicate it.

The first sentence of a wake Bubble notice shall name the wake id and the final linked
turn sequence, when one exists. Existing non-wake Bubble causes shall keep their current
turn-sequence identity and routing behavior.

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
delivery target. A later role rebind shall not retarget that guarded wake. Unguarded role
wakes retain their existing delivery-time re-resolution.

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
undeliverability. Gateway, SessionLane, recovery, and migration code shall call a `Wakes`
function inside their existing transaction.

### R16 — Cause and principal survive each transition

The outcome writer shall reject an empty cause kind, empty cause id, or empty principal.
The closed principal set shall remain the existing typed user, session, and process
forms. Scheduler admission, retry, terminal settlement, GAGGED consumption, invalidation,
and Bubble transitions shall use `process:tightbeam`; the source wake retains its creator
and origin principal.

### R17 — Restart recovery preserves eligibility

Gateway restart shall reconstruct due retry work from wake outcomes and clocks while
preserving attempt numbers, `retryAt`, and the unique final outcome.

A running wake turn recovered as `failed_unknown` shall enter R8's immediate
`undeliverable` path and shall produce zero replacement turns.

Boot recovery shall also submit each runtime `undeliverable` outcome without matching
Bubble evidence to R9 recognition.

### R18 — Legacy rows remain truthful without replay

The schema migration shall preserve existing wake, cancellation, turn, message,
lifecycle, and Bubble rows except for the two conflict normalizations below. It shall
apply this closed mapping:

| Legacy shape | Migration result |
|---|---|
| `pending` wake without a turn | Preserve it without an outcome. Its first later act uses attempt `0`. |
| `canceled` wake without a turn | Preserve it without a delivery outcome. Its typed cancellation remains final. |
| `fired` wake without a turn | Backfill null-turn `attempt` plus `undeliverable` with `legacy_outcome_unknown`. |
| unlinked turn in `failed` or `failed_unknown` | Preserve its status, set `failureClass=legacy_outcome_unknown`, and create no wake outcome. |
| unlinked turn in `queued`, `running`, `delivered`, or `canceled` | Preserve it with a null failure class and create no wake outcome. |
| linked turn, wake state `fired` | Set `wakeAttempt=0`; backfill `attempt` and `admitted`; then apply the terminal mapping below. |
| linked turn, wake state `pending` | Normalize the wake to `fired`, record its prior state in `wake_migration_conflict`, and apply the linked-turn mapping. The turn is durable admission evidence. |
| linked turn, wake state `canceled` | Preserve the wake and cancellation rows, record both prior states in `wake_migration_conflict`, and apply the linked-turn mapping. |

The terminal mapping is also closed. `delivered` gains `handled`. `failed` and
`failed_unknown` retain their status, gain failure class `legacy_outcome_unknown`, and
gain `failed` plus `undeliverable`. `canceled` retains its status, gains failure class
`legacy_outcome_unknown`, and gains `failed` plus `undeliverable`. A queued or running
turn under a `fired` wake retains its status and continues through normal claim or boot
recovery. A queued or running turn under a `canceled` wake is normalized to
`failed_unknown` with failure class `legacy_outcome_unknown` and an ended-at migration
time; it gains `failed` plus `undeliverable` and never runs.

Every backfilled outcome uses `legacy_import`. Bubble shall send no new notice for it;
existing Bubble and cancellation rows remain escalation and disposition evidence. A
second migration pass shall insert no second outcome or conflict row.

### R19 — Guidance follows the implemented mechanism

The release change shall update the wake CLI help and the operating manual in one batch
after R12-R13 and A4 pass. The directive shall state that
`--cancel-on-owner-activity` applies to a delayed self-wake whose premise is continued
owner quiescence. The directive shall leave other wake purposes unchanged.

## Architecture

### Durable shape

Rebuild `turns` in the existing pre-boot schema migration to replace table-level
`wakeId UNIQUE` with an attempt identity. Preserve existing columns and add:

```sql
wakeAttempt INTEGER NULL CHECK (wakeAttempt >= 0),
failureClass TEXT NULL
  CHECK (failureClass IN
    ('could_not_run','run_failed','run_canceled','outcome_unknown',
     'legacy_outcome_unknown'))
```

The rebuilt table adds a check that `failed` and `failed_unknown` rows carry a non-null
failure class; a wake-linked `canceled` row carries `run_canceled` or
`legacy_outcome_unknown`; and every other turn row carries a null failure class.
Another table check requires `wakeId` and `wakeAttempt` to be null together or populated
together. This prevents the nullable-column behavior of a unique index from admitting
an unnumbered wake turn. The rebuilt table also declares
`UNIQUE(seq, wakeId, wakeAttempt)` for the outcome link below.

Create these indexes after the rebuild:

```sql
CREATE UNIQUE INDEX turns_wake_attempt
  ON turns(wakeId, wakeAttempt)
  WHERE wakeId IS NOT NULL;

CREATE UNIQUE INDEX turns_one_active_per_wake
  ON turns(wakeId)
  WHERE wakeId IS NOT NULL AND status IN ('queued','running');
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
                   ('could_not_run','run_failed','run_canceled','outcome_unknown',
                    'legacy_outcome_unknown')),
  causeKind    TEXT NOT NULL CHECK
                 (causeKind IN
                   ('scheduler_due','retry_due','turn_terminal','target_unresolvable',
                    'retry_exhausted','unsafe_failure','legacy_import')),
  causeId      TEXT NOT NULL CHECK (length(causeId) > 0),
  principal    TEXT NOT NULL CHECK
                 (principal = 'process:tightbeam'
                  OR principal GLOB 'user:?*'
                  OR principal GLOB 'session:?*'),
  UNIQUE (wakeId, attemptNo, kind),
  FOREIGN KEY (turnSeq, wakeId, attemptNo)
    REFERENCES turns(seq, wakeId, wakeAttempt) DEFERRABLE INITIALLY DEFERRED,
  CHECK (kind NOT IN ('admitted','handled','failed') OR turnSeq IS NOT NULL),
  CHECK ((kind = 'failed' AND failureClass IS NOT NULL)
         OR (kind != 'failed' AND failureClass IS NULL AND retryAt IS NULL)),
  CHECK (retryAt IS NULL OR (kind = 'failed' AND failureClass = 'could_not_run'))
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

The mutation seam uses these cause pairs:

| Transition | `causeKind` | `causeId` |
|---|---|---|
| initial `attempt` and `admitted` | `scheduler_due` | `wake:<wakeId>` |
| retry `attempt` and `admitted` | `retry_due` | `outcome:<priorFailedOutcomeId>` |
| `handled` and `failed` | `turn_terminal` | `turn:<turnSeq>` |
| target-resolution `undeliverable` | `target_unresolvable` | `role:<targetRole>` when a role was requested; otherwise `session:<sessionKey>` |
| exhausted `undeliverable` | `retry_exhausted` | `outcome:<finalFailedOutcomeId>` |
| unsafe `undeliverable` | `unsafe_failure` | `outcome:<failedOutcomeId>` |
| migrated outcome | `legacy_import` | `wake:<wakeId>` |

Every runtime row in this table uses principal `process:tightbeam`. The wake and typed
cancellation rows retain their existing creator and requester principals.

Add nullable quiescence guard columns to `wakes`:

```sql
invalidationKind TEXT NULL
  CHECK (invalidationKind IN ('owner_turn_admitted')),
invalidationOwnerUserId TEXT NULL,
invalidationAfterTurnSeq INTEGER NULL
```

A table check requires the three invalidation columns to be null together or populated
together. Existing `wakes.state` remains the compatibility aggregate:

- initial admission changes `pending` to `fired`;
- pre-admission cancellation, quiescence invalidation, and target absence change
  `pending` to `canceled` through typed cancellation;
- retry, handled, failed, and post-admission undeliverable outcomes leave the aggregate
  state `fired` and use `wake_delivery_outcomes` as their detailed truth.

The existing `wake_fired` lifecycle marker and `wakes.state='fired'` mean admission after
this migration. Neither is evidence of `handled`; only the typed final outcome supplies
that fact.

### Read projection

Add wire verb and CLI command `wake-get <wakeId>`. Its result has this fixed shape:

```text
{
  wakeId, state, latestOutcome, attemptCount, turnSeq, nextRetryAt, failureClass,
  outcomes: [
    {attemptNo, kind, turnSeq, at, retryAt, failureClass,
     cause: {kind, id}, principal}
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

The read handler applies R5 authorization before it queries the history. The new exact-id
read leaves the existing pending-wake list unchanged.

### Transaction order

Initial admission uses this order inside `Gateway.deliver_prompt_in_txn/5`:

1. Load the wake and its quiescence guard through `Wakes`.
2. Run R13 activity invalidation.
3. Resolve the current target.
4. Append one prompt echo.
5. Enqueue turn `{wakeId, wakeAttempt=0}`.
6. Call `Wakes.admit_prompt_in_txn/4` with the turn sequence.
7. Insert `attempt` and `admitted` outcomes.
8. Change `wakes.state` from `pending` to `fired` and verify one changed row.
9. Commit, then publish and nudge through the existing post-commit path.

Any error or lost CAS rolls back steps 4-8. The scheduler removes the prompt path's
current callback-then-`mark_fired` sequence. Internal consumer delivery keeps its
existing consumer-specific act edge.

If step 3 finds no target, `Wakes` appends an `attempt` with a null turn, appends
`undeliverable`, and consumes the pending wake as `canceled` through the typed
target-unresolvable cancellation in that transaction. It commits no message or turn. If
a retry transaction finds no target, it appends the null-turn `attempt` and
`undeliverable` while the compatibility wake state remains `fired`.

Retry admission uses the first echo's message id and prompt. It inserts no second echo.
It enqueues `{wakeId, wakeAttempt=n+1}`, appends `attempt` and `admitted`, and consumes
the exact failed row's retry eligibility in one transaction. The uniqueness constraints
make replay return the existing admission.

Turn finalization changes from a ledger-only terminal transaction to this composition:

1. `Ledger.finish_in_txn` wins the running-to-terminal CAS.
2. `Wakes.finish_prompt_attempt_in_txn` appends `handled` or `failed`.
3. A retry-safe failure stores the exact next `retryAt`, or appends `undeliverable` at
   exhaustion.
4. An unsafe failure appends `undeliverable` immediately.
5. The existing typed harness lifecycle writer runs.
6. The transaction commits, then terminal publication, supervision recognition, and
   Bubble recognition run from the committed rows.

### Failure and Bubble integration

The adapter boundary returns a typed run-admission disposition beside its error. The
gateway maps checkout and session-stage failures directly to `could_not_run`. Adapter
implementations map protocol evidence to `could_not_run`, `run_failed`, or
`outcome_unknown`. The default for absent protocol evidence is `outcome_unknown`.

Bubble extends its cause parser with `bubble:wake:<wakeId>`. For a wake-linked failed
turn, its left-hand side reads the wake's final outcome. A retry-pending failure does not
match. An undeliverable runtime outcome matches once. The existing lineage resolver,
notice-turn evidence, owner terminal alert, and `user-alerted` fact remain authoritative.

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

Before `Wakes`, `LaneManager`, `Supervision`, or Bubble starts, one exclusive migration
transaction shall:

1. rebuild `turns` with the two new columns and indexes;
2. copy existing turn values and apply only the canceled-wake/nonterminal-turn
   normalization from R18;
3. set `wakeAttempt=0` for a non-null `wakeId` and normalize a pending wake with a linked
   turn to `fired`;
4. create `wake_delivery_outcomes` and quiescence columns;
5. backfill R18 outcomes from typed wake and turn columns;
6. append R18's deterministic conflict lifecycle rows with the pre-normalization values;
7. commit before recovery reads retry eligibility.

The migration reads structured row columns. It does not parse chat or error prose.

### Exact implementation surfaces

- Extend `lib/tightbeam/wakes.ex` with the outcome schema, admission CAS, retry query,
  terminal seam, quiescence guard, projections, and migration helpers.
- Extend `lib/tightbeam/ledger.ex` with `wakeAttempt`, `failureClass`, composite dedupe,
  and finalization parameters.
- Amend prompt delivery composition in `lib/tightbeam/gateway.ex`; remove the prompt
  path's split `mark_fired` edge.
- Amend `lib/tightbeam/session_lane.ex` so terminal CAS and wake settlement share one
  transaction.
- Amend `lib/tightbeam/productions/bubble.ex` to recognize a runtime undeliverable wake
  as one named cause.
- Amend `lib/tightbeam/supervision.ex` with the typed GAGGED no-match and atomic
  consumption.
- Add the `wake-get` wire verb and Rust CLI command. Add the invalidation wire field and
  Rust CLI flag without changing the unguarded wake request.
- After the mechanism passes its acceptance tests, update the wake paragraph in
  `priv/guidance/operating-manual.md` and the CLI help in one guidance batch. Publish no
  pre-mechanism directive.
- Update wake, ledger, gateway, Bubble, supervision, schema-shape, soak, and trace tests.

No source edit is authorized by this specification. These paths name the later build
surface.

### Traceability

| Requirement | Implementation seam | Acceptance |
|---|---|---|
| R1-R4 | Wakes admission/cancel CAS, Gateway transaction, turn indexes | A1 |
| R5-R7 | outcome table, Ledger failure class, SessionLane terminal transaction | A2, A3, A6 |
| R8-R10 | retry query, scheduler, Bubble wake cause | A2, A3, A6, A7 |
| R11 | Supervision terminal LHS, watermark, lifecycle | A3 |
| R12-R13 | wake guard columns, scheduling handler, admission transaction | A4 |
| R14 | existing claim and turn-boundary seams | A5 |
| R15-R16 | Wakes mutation API and schema checks | A1-A4, A6 |
| R17 | boot recovery and retry query | A2, A6, A7 |
| R18 | pre-boot schema migration | A8 |
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

### A4 — Stale-quiescence invalidation

Given session `S1` is running an owner-origin turn for user `mike`, when `S1` schedules a
delayed self-wake with `--cancel-on-owner-activity`, then the wake stores owner `mike` and
the current owner-turn cursor.

Given a later `user:mike` turn is admitted to another mike-owned session `S2`, when the
quiescence wake reaches its act edge, then one typed cancellation names
`owner_turn_admitted:<S2 turn seq>`, the wake becomes canceled, and no prompt echo, turn,
attempt, or admitted outcome is created for it.

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

### A5 — Queued wake survives a model swap

Given session `S` selects model A and its live lane is idle, when a prompt wake admits
attempt 0 while a barrier holds the post-commit lane nudge, then its queued turn has no
claimed model or adapter generation. When the existing turn-boundary tune changes `S` to
model B, the barrier releases the nudge, and the lane claims the queued wake turn, then
the turn stamps model B and its current harness, runs through model B's adapter, and
reaches handled.

The fixture shall contain one wake turn, one attempt, one admission, one handled outcome,
no failed outcome, no retry, and no Bubble cause. Proves R14 and retains the fixed C limb.

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

Given an initial wake's target becomes unresolvable before admission, when the wake acts,
then one null-turn attempt and one target-unresolvable undeliverable outcome commit, the
compatibility wake state becomes canceled through typed provenance, one wake-named
Bubble cause starts, and no prompt echo or turn exists.

### A7 — Restart preserves a due retry

Given attempt 0 commits `could_not_run` with `retryAt=110` and the gateway stops at 105,
when it restarts at 110, then the boot scheduler admits attempt 1 once. A second restart
preserves both attempt identities and does not move `retryAt`. Proves R3, R8, R17.

Given an undeliverable outcome commits and the gateway stops before Bubble admits its
first notice, when it restarts, then Bubble admits one wake-named logical cause. A second
restart creates no second notice for the same recipient and no second logical cause.
Proves R9 and R17.

### A8 — Legacy migration preserves evidence

Given fixtures for each row in R18's wake-shape and terminal mappings, when the migration
runs, then unchanged columns compare equal, each linked turn has `wakeAttempt=0`, each
shape has exactly the specified outcomes, and each normalization has one conflict row
that preserves its prior state. A canceled wake's queued or running carrier is
`failed_unknown` and never runs. Restarting after migration produces no second backfill
row, conflict row, retry, or retroactive Bubble notice. Proves R18.

### A9 — Guidance source closure

Given a built release in which A4 passes, when the assembled identity and CLI help are
inspected, then each contains the exact `--cancel-on-owner-activity` spelling and the
delayed-self-wake scope from R19. Given a source tree in which the guard mechanism or A4
is absent, then the source-closure check rejects that directive. Proves R19.

## Open Questions

None. The specification has no blocking or non-blocking hole. A change to the retry
schedule, safe-failure vocabulary, named owner activity, final-outcome vocabulary, or
legacy migration ruling requires an amendment and a new content hash before build
handoff.
