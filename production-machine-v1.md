# production-machine-v1 — the substrate never waits

Authority: Flynn, 2026-08-05 (the adjudication deletion rulings, recorded in
tightbeam-decisions.md). Supersedes the mechanism half of
model-ringdown-pattern.md; its principle ("model choice is judgment, done by
inference") is carried forward here, its mechanism (episodes, holds, ladder,
verb) is deleted from the tree.

## The invariant

The substrate is a Newell production machine: a recognize-act cycle over the
current durable state of the system.

- **Working memory** is the durable state: the ledger, sessions, assignments,
  attests, wakes, the condition-fact stream — and the productions' own durable
  bookkeeping (`supervision_watermarks`, `assignment_prods`), which is working
  memory like any other: written by acts, read by conditions, never private.
  Nothing else is state.
- **A production** is a rule: a declared left-hand side (a condition set over
  working memory) and a procedural right-hand side (the act). The substrate
  fires productions whose conditions match; it holds no other behavior.
- **The substrate never waits.** There is no substrate state whose exit
  condition is someone else's decision. Anything shaped like waiting is either
  a fact an agent asserted (and will retract), or it is a defect. Adjudication
  was the defect this spec exists to never rebuild: a substrate-owned hold
  whose only exit was a ruling.

Agents decide; the substrate recognizes. Parking, halting, redirecting,
choosing models — all judgment, all inference, all expressed to the substrate
as facts. On any failure the substrate's obligations TO THE FAILING TURN, IN
THAT TURN'S OWN SESSION, are exactly three: the truth (a failed turn row), the
named reason (turns.error and the chat marker), and the record (the lifecycle
event). The fault bubble and the terminal alert below are not additional
obligations of the failure — they are productions that RECOGNIZE the failed
row, fire above it, and could be deleted without touching these three. The
adjudication ruling's "exactly three" meant no hold, no episode, no ladder;
it did not mean the machine may not act on what the record now says.

## The cycle

The target semantics, stated so no mechanism drifts from them (Flynn,
2026-08-05): whenever state changes, every production whose conditions
depend on that state gets to run; their acts may change state again, which
runs THEIR dependents, and the machine iterates until nothing fires —
QUIESCENCE — where it rests until an external event (a prompt arriving, an
adapter dying, a timer) changes state again. Timers are external state
injectors, nothing more.

Where the tree stands against that, honestly:

- The fact stream already has the true shape: a filed fact is dispatched to
  every condition wake whose declared `{kind, scope}` matches — no consumer
  is hand-wired. This is the pattern the rest converges toward.
- Everywhere else, propagation edges are HAND-WIRED to the events their
  authors foresaw (a terminal commit fires the bubble and the turn-end
  shift; an attest resets the ladder). Cascades happen — a notice turn's own
  terminal re-enters recognition, which is the climb — but only along built
  edges.
- The sweep today does double duty: timer AND safety net for wiring nobody
  built. In the target it is only the timer.

Binding rule for v1: every act's state change must either fire its
dependents through a wired edge or be provably reachable by a sweep — an
unpropagated write that no sweep revisits is a defect, not a latency.
Completion path (with the statute migration): a dependency-indexed
dispatcher over all of working memory — productions declare the state their
conditions read, writes dispatch to dependents, refraction (the existing
idempotency keys and dedupe watermarks) is what makes the fixpoint
terminate.

## Legibility requirement

It must be clear from the code alone that this is a production machine.

- A production's LHS is evaluated in ONE named function per production
  (`*_production_matches?` or a module under a `productions`-named grouping),
  reading durable state only — no process state, no ambient flags.
- The RHS may remain procedural Elixir. Half a production system done honestly
  (declared recognition, procedural acts) is the standard; scattered
  conditions wearing production-system vocabulary is the anti-pattern.
- Moduledocs at each production site name the pattern and cite this spec.

Pragmatism rule: the engine is not a framework. No rule DSL, no interpreter,
no registry, until a second consumer forces one — and the completion path
(migrating a production's LHS into the statute layer that Rules.decide already
matches) is the named direction when that day comes.

## Standing facts

`condition_facts` is append-only occurrences; STANDING state is derived, never
stored: a fact stands when the latest of its assert/retract pair is the
assert. Provenance of every assertion and retraction survives by construction.

Two authority classes, and the reserved-kinds rule runs in both directions:

- **Agent-only kinds** — the substrate is FORBIDDEN to file them.
  - `work-blocked` / `work-unblocked`, scope = a session key. Asserted and
    retracted by a session in the scope session's lineage above it, by the
    owner user, or by an admin. Meaning: an agent with authority has decided this session is
    not to be treated as stalled. The substrate never infers it, never times
    it out, never clears it.
- **Substrate-only kinds** (`process:tightbeam` origin, the existing
  reserved-kind mechanism):
  - `user-alerted` / `user-alert-cleared`, scope = the OWNER USER ID — never
    a session key, because the root main-session key is composed from the user
    id and may name no row (the ground already recorded that bug: well-formed
    addresses to nonexistent sessions, queued forever). Meaning: work owned by
    this user was shown unable to run and the user has been told; not yet
    observed healed.

Both directions of the kind rule are enforced INSIDE `ConditionFacts.file`
— not only at the verb seam, because the substrate does not file facts
through a verb: agent-only kinds are refused when origin is
`process:tightbeam`, reserved kinds are refused when it is not. The verb
seam adds the lineage-authority check for `work-blocked` on top.

A standing fact NEVER gates the turn queue. `work-blocked` changes what
productions match (prodding stops); it does not stop a turn from being
enqueued or claimed — a parent that orders a retry must be able to land one.
The queue's only gates remain session existence and `state = 'active'`.

## Assignment-terminal effort-generator retirement

Authority: `wi_a608cc9b-e34e-4f59-b330-5d83709eb62f`, supported by
`art_a4f39376`: Main recorded 201 adjudication signals, approximately all
effort check-ins; 31 fired for assignments that were already closed; none
required a true decision. This amendment extends the existing assignment-close
transaction. It does not change when effort supervision arms or what its
check-ins say. Source baselines: main
`31c91a7a79bf411791d8422bb220495a72dd8d0c`; active 0.1.9
`7090a63069ec024a918ade3f659bbd5560936285`.

### Goal

When completion, surrender, or revocation closes an assignment, that same
transaction retires the assignment's effort-check-in generator. No pending
output owned by that generator may fire after the close commits. No internal
probe, deadline, ruling, boot, or replay may re-arm or escalate that retired
generator. The ledger preserves the generator, wake, check-in, cancellation,
decision, cause, and principal evidence for every disposition.

### Non-Goals

- This amendment does not cancel a running turn or rewrite a fired wake,
  delivered check-in, ruled decision request, terminal turn, or generation
  outside the exact retirement set in EGR-2.
- This amendment does not cancel an effort generator for an open sibling
  assignment, an unrelated generator, an ordinary scheduled or condition
  wake, or a supervision-controller wake.
- This amendment does not infer ownership from prompt text, origin alone,
  recipient, assignment holder, work item, timing, or elapsed time.
- This amendment does not change effort horizons, evidence channels, prod
  wording, escalation order, effort-ruling choices, assignment-close
  authority, decision authority, wake-read authority, trace-read authority,
  or privacy.
- This amendment does not own queued-turn invalidation. The review-challenged,
  revised proposal at commit `69663367eaed3eb862e55769841e8d37b3021b5e` for
  `wi_154bf46b-acd6-4ff4-a2b0-732737a03d64` owns that sibling lane.
- This amendment adds no public verb, request parameter, timer, polling loop,
  prompt convention, decision kind, or agent instruction. It takes no action
  on 0.1.8.

### Terms

- **Assignment-terminal transition:** one transaction that changes an
  assignment from `open` to `closed` with stored outcome `completed`,
  `surrendered`, or `revoked`.
- **Effort-check-in generator:** the durable generation sequence in
  `effort_checkin_generations` for one assignment, including the wakes that
  the effort controller schedules from that sequence.
- **Effort-owned wake:** a wake whose id has a durable row in
  `effort_checkin_wake_ownership`. The row stores its exact `assignmentId`,
  `generation`, and one role: `probe`, `holder_checkin`, `parent_escalation`,
  `decision_deadline`, or `decision_notification`.
- **Pending generator output:** an effort-owned wake whose durable wake state
  is `pending`.
- **Retirement set:** each unretired generation that owns pending generator
  output selected by the terminal transition, plus the assignment's maximum
  unretired generation when one exists. An unretired generation has null
  `retiredAt`, `retiredOutcome`, `retiredCause`, and `retiredPrincipal`.
- **Retired generation:** a generation in the exact retirement set in EGR-2,
  stamped with the assignment-terminal transition's time, stored outcome,
  cause, and principal. The transition also changes an `armed` member of that
  set to `canceled`; it retains a member already in `probed` or `canceled`.
- **Terminal cause:** the exact string
  `assignment-terminal:<outcome>:<assignmentId>`, derived from the closed
  assignment row in the terminal transaction.
- **Terminal principal:** `session:<sessionKey>` or `user:<userId>` for the
  principal authorized to make the terminal transition. Holder retirement
  uses the durable principal already required by that transition.
- **Legacy structurally-owned wake:** a pre-amendment probe referenced by
  `effort_checkin_generations.wakeId`, or a pre-amendment effort deadline
  referenced by `decision_requests.deadlineWakeId`.
- **Ambiguous legacy prompt wake:** a pre-amendment pending `prompt` wake from
  `process:tightbeam` with non-null `assignmentId` for an assignment that has
  effort-generation history, but no effort-ownership row. The term does not
  assert that the wake is an effort wake.

### Assumptions

- Assignment closure, wake scheduling, wake delivery, internal effort
  callbacks, effort rulings, and schema migration serialize through database
  transactions over one ledger.
- Wake delivery commits the prompt message, its queued turn, and the wake's
  `fired` state in one transaction.
- Existing typed wake cancellation preserves the wake row and appends
  `wake_cancellations` cause, requester, outcome, and liveness evidence in the
  cancellation transaction.
- The main line creates holder check-ins and parent escalations and retains the
  deadline and ruling path for a migrated legacy effort request. Active 0.1.9
  creates holder check-ins, effort decision notifications, and effort decision
  deadlines. This amendment covers both line-specific sets.
- The queued-turn amendment named in Non-Goals remains a separately reviewed
  contract. When both amendments land, the assignment-terminal transaction
  invokes both sibling mutations without making either mutation call the
  other.

### Invariants

**EGR-1 — Typed ownership at creation.** Every effort wake created after this
contract activates receives its wake row and one matching ownership row in the
same transaction. The ownership row's assignment and generation must equal the
durable source rows used to schedule the wake. A transaction that cannot write
that ownership row does not schedule the wake, change the generation, open or
advance an effort decision request, or emit a prompt.

**EGR-2 — Atomic retirement.** Each assignment-terminal transition performs
all of these writes in its assignment-close transaction: it changes the
assignment state; cancels every pending effort-owned wake for that assignment;
stamps the retirement set; changes each `armed` member of that set to
`canceled`; and supersedes any open effort decision request under the existing
disposition rule. A generation already in `probed` or `canceled` retains that
state while receiving the retirement stamp. A transition with an empty
retirement set closes without inventing or rewriting a generation. A failure
rolls back the assignment close and every retirement write.

**EGR-3 — Exact scope.** Retirement selects wakes only through
`effort_checkin_wake_ownership.assignmentId` and `wakes.state = 'pending'`.
It selects the retirement set only through the exact assignment id, maximum
unretired generation number, null retirement fields, and ownership rows for
the selected pending wakes. It does not select by prompt, origin, recipient,
holder, work item, or time. It changes no row owned by another assignment and
no unowned wake.

**EGR-4 — Exact evidence.** The retired generation stores `retiredAt` equal to
the assignment's `closedAt`, `retiredOutcome` equal to the stored assignment
outcome, `retiredCause` equal to the terminal cause, and `retiredPrincipal`
equal to the terminal principal. Each canceled owned wake retains its wake and
ownership rows and receives the existing typed cancellation record with
the close path's existing process requester, reason `obligation_disposed`,
causal-source kind `assignment_transition`, causal-source id equal to the
assignment id, and disposition id equal to the assignment id. The permanent
ownership relation joins that cancellation to the retired generation's exact
terminal cause and principal through the ownership row's generation. The
maximum unretired generation records the terminal retirement even when no wake
was pending. A fired or previously canceled owned wake is not rewritten; its
wake state and ownership row remain the evidence of its disposition. A later
terminal transition never overwrites non-null retirement fields.

**EGR-5 — Serialized wake race.** Wake delivery and assignment retirement
form one serialized race. If retirement commits first, a pending effort-owned
wake is canceled and cannot deliver. If delivery commits first, the wake stays
`fired`; retirement records the generator retirement and does not rewrite the
message or turn. A queued turn produced by that delivery belongs only to the
queued-turn amendment. A turn whose claim committed before closure follows
its existing running-turn contract.

**EGR-6 — Serialized controller race.** An effort probe, deadline, or ruling
transaction rechecks that the assignment is open before it changes controller
state or creates output. If retirement commits first, the callback or ruling
creates no wake, generation, deadline, escalation, or decision transition. If
the controller transaction commits first, it writes all new generations and
owned wakes before retirement selects them; retirement then cancels the
pending rows and stamps the resulting retirement set. On 0.1.9, a close-first
effort ruling returns the existing non-open decision result. A rule-first
`continue` may re-arm, but the following close retires that new generation in
the same terminal transaction.

**EGR-7 — No resurrection.** Boot, callback replay, terminal-command retry,
and terminal-publication replay do not change retired generation fields,
create an ownership row for a new wake, reopen a superseded decision request,
or schedule effort output for a closed assignment. Reopening is prospective:
it does not alter a retired generation or canceled wake, and the next lawful
arm uses a generation number greater than every stored generation for that
assignment.

**EGR-8 — History and adjudication.** Retirement never deletes or rewrites a
fired check-in wake, prompt message, turn, closed or ruled decision request,
decision ruling, generation outside the retirement set, supervision row, or
cancellation row. On either line it supersedes only an open effort decision
request and cancels only that request's pending owned deadline and notification
wakes. Active 0.1.9 may create the request; main applies the disposition only
to a migrated legacy request. Existing `continue` and `dismiss` semantics are
unchanged for a request that remains open on either line.

**EGR-9 — Compatibility boundary.** Each elected line migrates only from its
exact predecessor stamp: main from `coordination-fabric-v1-phase1-v7`, and
0.1.9 from `operator-decision-requests-v1`. The migration adds the ownership
relation and retirement fields, then backfills ownership only for legacy
structurally-owned wakes by exact foreign-key equality. Before the new stamp
commits and before any scheduler starts, it searches for ambiguous legacy
prompt wakes. If any exist, migration rolls back and returns
`incompatible_effort_wake_provenance` with their wake ids. It does not inspect
their prompts, classify them, cancel them, or advance the schema stamp. An
operator may retry only after each named wake reaches `fired` or `canceled`
through predecessor behavior. If predecessor behavior cannot lawfully settle
a named wake, upgrade remains blocked for a separately authorized data repair;
this migration does not invent that authority. An unknown predecessor stamp
receives the existing exact-shape refusal.

**EGR-10 — Authorization, privacy, and wire stability.** The terminal actor,
effort ruler, wake reader, and work-item trace reader receive exactly their
pre-amendment authorization results. Existing public requests and responses
remove or rename no field. An authorized `work-item-trace` adds
`effortRole` to an effort-owned wake entry and adds `retiredAt`,
`retiredOutcome`, `retiredCause`, and `retiredPrincipal` to an effort
generation entry; each value is null when absent. An unauthorized caller
receives the existing refusal without ownership or retirement data.

**EGR-11 — Holder-retirement order.** Holder retirement first revokes each of
the holder's open assignments and applies EGR-2. The existing session-
retirement drain then disposes the holder's remaining pending wakes. An
effort-owned wake canceled by assignment revocation records the assignment-
terminal cause and is not re-canceled as target retirement. A pending unowned
wake remains in the session-retirement lane. Both stages stay inside the
existing holder-retirement transaction.

### Architecture

Add one narrow relation, `effort_checkin_wake_ownership`, keyed and
foreign-keyed by `wakeId` to the wake, and composite-foreign-keyed by
`(assignmentId, generation)` to the generation row. Its other column is the
closed role set in Terms. Rows are permanent provenance; no close, reopen,
replay, or rollback path deletes them. Every effort wake scheduling site uses
one internal write seam that creates the wake and its ownership row together.

Add nullable `retiredAt`, `retiredOutcome`, `retiredCause`, and
`retiredPrincipal` fields to `effort_checkin_generations`. A database check
requires all four to be null or all four to be non-null; non-null values
require `state` in `probed` or `canceled`, a permitted outcome, and the exact
terminal-cause shape derived from the row's assignment id. Non-terminal
generation replacement continues to use `state = 'canceled'` with null
retirement fields.

The existing shared completion, surrender, and revocation seam supplies the
closed assignment row and authorized principal to one retirement mutation.
That mutation cancels the exact pending ownership join, stamps the retirement
set, and disposes the open effort request. It runs beside, not inside, the
queued-turn drain proposed by `wi_154bf46b`. The two mutations share only the
outer assignment-terminal transaction and terminal cause. Neither owns the
other's tables or acceptance lane.

Main advances to shape `coordination-fabric-v1-phase1-v8`. Active 0.1.9
advances to `operator-decision-requests-v2`. Each migration is additive and
transactional. A preflight provenance refusal leaves the predecessor stamp and
all rows unchanged. After activation, rollback means restoring the
pre-activation database snapshot before starting the predecessor binary; a
predecessor binary must not run against the advanced stamp because it can emit
unowned effort wakes.

Mechanism choice — ADD typed ownership at the existing close seam. Deleting
effort supervision would remove a live safety bracket. Accepting stale
post-close output would retain the measured false-prod defect and spend agent
judgment on a durable fact the substrate already knows.

Operating pattern taught to agents: none. This is ledger physics. The
substrate owns exact rows and transitions; no agent decides whether a wake
belongs to the generator.

### Acceptance

Each race check uses deterministic transaction barriers at the real close,
wake delivery, probe, deadline, ruling, boot, and claim seams. Sleeps and
elapsed-time assertions do not satisfy a race check. Each elected line runs
its applicable checks against its exact predecessor migration fixture.

1. **EGR-A1 — Three terminal outcomes.** Given three open assignments with an
   armed current generation and pending owned output, when completion closes
   the first, surrender closes the second, and an authorized principal revokes
   the third, then each close commits with its generator retired and only its
   pending owned wakes canceled. The retirement fields equal the closed row,
   terminal cause, and terminal principal on the maximum unretired generation
   and each selected wake's unretired source generation. An `armed` selected
   generation becomes canceled; a `probed` selected generation retains that
   state. Removing any retirement write from the fixture makes the close
   transaction roll back. A fourth assignment with an empty retirement set
   closes without creating or rewriting a generation or wake.
2. **EGR-A2 — Exact wake scope.** Given assignment A with pending owned probe,
   holder-checkin, parent-escalation, decision-deadline, and
   decision-notification wakes; open sibling B with the same roles; and
   pending ordinary scheduled, condition, and supervision wakes attributed to
   A, when A closes, then only A's five owned wakes change to canceled. B's
   generator and every unowned wake remain byte-for-byte unchanged. Run the
   line-applicable subset where a role does not exist.
3. **EGR-A3 — Delivery race.** Given two identical pending owned prompt wakes,
   when close commits before delivery for the first and delivery commits
   before close for the second, then the first has one typed cancellation and
   no message or turn, and its ownership row joins directly to its source
   generation's retirement cause and principal. The second remains fired with
   its message and turn, gains no cancellation record, and the maximum
   unretired generation records the retirement. With the sibling queued-turn
   amendment active, its queued turn receives that amendment's exact terminal
   disposition; a turn claimed before close remains running.
4. **EGR-A4 — Probe race and re-arm.** Given an armed probe at its callback
   boundary, when close wins, then the callback emits no output and creates no
   generation. When the probe wins and emits a prompt plus a new generation,
   then close cancels that prompt and the new probe, retires the new current
   generation, and retains the consumed generation's `probed` state while
   stamping its retirement fields. Replaying either callback creates no row.
5. **EGR-A5 — Decision races on both lines.** Given separate open effort
   requests at notification, deadline, and `continue` ruling boundaries, when
   close wins each race, then the request is superseded, its pending owned
   wakes are canceled, and the losing action creates no replacement. When
   each action wins first, close cancels every pending replacement and retires
   any new current generation. A ruled request and its ruling remain byte-for-
   byte unchanged. The main fixture starts from a migrated legacy open effort
   request; the 0.1.9 fixture also exercises new request creation.
6. **EGR-A6 — Restart, replay, and reopen.** Given a retired generator with
   canceled, fired, and ruled history, when boot runs twice, the terminal
   command and publication replay, the assignment reopens and closes once
   without a new arm, reopens again, boot runs, and one new arm commits, then
   all prior rows and retirement fields remain unchanged. The intervening
   close creates no generation and overwrites no retirement field. No pre-
   reopen output fires. Exactly one new generation with a greater number and
   one owned probe exist after the arm.
7. **EGR-A7 — Migration and refusal.** Given each exact predecessor fixture
   with generation probes and 0.1.9 decision deadlines, when migration runs,
   then ownership backfill matches only the exact referenced wake ids and the
   successor stamp commits. Given a second fixture with one ambiguous legacy
   prompt wake, migration returns `incompatible_effort_wake_provenance` with
   that id, writes no ownership row, cancels no wake, changes no business row,
   and retains the predecessor stamp. A prompt with effort-looking text but no
   structural ownership is never backfilled. After predecessor behavior
   settles the named wake, the same fixture migrates; if the wake remains
   pending, every retry returns the same refusal without changing data.
8. **EGR-A8 — Evidence, authorization, and privacy.** Given canceled, fired,
   and unaffected owned wakes plus authorized and unauthorized trace readers,
   when the authorized reader requests the work-item trace, then wake entries
   expose their stored roles, cancellation entries expose their existing typed
   disposition, and each retired generation exposes its terminal cause and
   principal in the four retirement fields. Historical prompt and decision
   content is unchanged. The unauthorized reader receives the existing refusal
   and no new data. Terminal and ruling authorization matrices equal the
   predecessor fixtures.
9. **EGR-A9 — Idempotency and rollback.** Given one successful retirement,
   when the close command retries and boot replays, then row counts, wake
   states, retirement fields, cancellations, requests, and trace entries do
   not change. Given a migration fault before stamp commit, the transaction
   restores the predecessor bytes. Given an activated successor snapshot,
   restoring its paired pre-activation snapshot allows the predecessor binary
   to start with its predecessor stamp; starting that binary on the successor
   stamp receives the exact-shape refusal.
10. **EGR-A10 — Shared transaction composition.** Given a pending owned prompt
    wake, a fired owned prompt whose turn is queued, a fired owned prompt whose
    turn is running, and a queued unrelated turn, when the assignment-terminal
    transaction runs with both amendments active, then this amendment cancels
    only the pending wake and retires the generator. The sibling amendment
    alone disposes the matching queued turn. Neither amendment changes the
    running or unrelated turn, and a forced failure in either mutation rolls
    back the assignment close and both mutations.
11. **EGR-A11 — Holder-retirement order.** Given a retiring holder with two
    open assignments, one pending effort-owned wake for each assignment, one
    pending unowned wake, and one already-running turn, when holder retirement
    commits, then each assignment revocation retires its generator and cancels
    its owned wake with the revoked terminal cause before the session drain.
    The session drain cancels only the unowned pending wake with its existing
    target-retirement cause. It does not add a second cancellation for either
    owned wake, and it does not change the running turn. A forced failure in
    either stage rolls back the holder retirement, assignment revocations,
    generator retirements, and wake dispositions.

Traceability: EGR-A1 verifies EGR-2 and EGR-4; EGR-A2 verifies EGR-1 and EGR-3;
EGR-A3 verifies EGR-5; EGR-A4 and EGR-A5 verify EGR-6 and EGR-8; EGR-A6
verifies EGR-7; EGR-A7 verifies EGR-9; EGR-A8 verifies EGR-10; EGR-A9 verifies
EGR-2, EGR-7, and EGR-9; EGR-A10 verifies the composition assumption and
EGR-3; EGR-A11 verifies EGR-11.

### Open Questions

None. Implementation is gated on independent acceptance of this exact revision.

## The prod production

The supervision prodder is the first production formalized under this spec.

The turn-end schedule (`rail_enforcement, pending_wake_gate, prod_ladder`) is
this machine's CONFLICT-RESOLUTION STRATEGY — the standard production-system
answer to "several rules could fire": a fixed priority order, first act wins
the cycle. Name it exactly that, in the code. Within it, each step's LHS must
be COMPLETE FOR THAT STEP — a declared LHS that omits gates the code applies
elsewhere is the scattered-conditions anti-pattern with better marketing.

- **LHS, declared in one site, complete:** holder session active ∧ no running
  or queued turn for the holder (a pending turn means the strand is moving) ∧
  this terminal seq not already evaluated (the watermark) ∧ an open assignment
  obligation exists ∧ no pending wake for the holder — ANY origin, matching
  the ground: a scheduled wake means the strand is not stalled regardless of
  who scheduled it ∧ **no standing `work-blocked` fact for the holder
  session**. A fresh attest is NOT a match gate — implementation surfaced
  the ground truth: an attest RESETS the ladder inside the act (prod count
  back to zero) and the production still fires, deliberately and
  test-pinned ("progress resets"); an attest answers the previous prods, it
  does not discharge the standing obligation.
- **RHS, procedural, unchanged:** prod the holder up to n times, then escalate
  rung by rung up the lineage, then terminus with the loss named.
- **Act-time recognition:** the prodder is two-phase on the ground — match
  records a durable pending branch, a later drain dispatches it, possibly
  across a restart. The drain RE-READS the standing `work-blocked` fact
  immediately before dispatch and DISCARDS a pending branch whose holder is
  now blocked. Nothing is lost: the obligation still stands in working
  memory, and the production re-matches from current state after retraction.
  Recognition happens at act time or it is not recognition.

This is not suppression bolted onto the prodder. The prodder does not check a
flag; the production does not match. The same absence-of-match that applies to
a session with no open assignment applies to a blocked one.

## Fault bubbling: delivery is the proof

When a turn fails, the substrate tells someone who can act. Who can act is
never guessed — it is demonstrated.

1. A turn reaches a non-delivered terminal: row, reason, marker in the
   failing session's own stream. Which terminals START a bubble, decided per
   state: `failed` and `failed_unknown` bubble — both are the work not
   happening with nobody having decided that (`failed_unknown` doubly so: the
   outcome is unknown, which is more worth a parent's attention, not less).
   `canceled` never bubbles: cancellation IS a decision, made by an authority
   (a retire drain, an explicit cancel), and bubbling it would report a
   decision as a fault.
2. Bubbles climb from sessions with a lineage parent (`spawnedBy` set). A
   session with no parent — a user's main session OR any session the user
   created directly — is its own terminal rung: the marker in its stream IS
   the user notice, and spending a model turn to restate it elsewhere is
   noise. For a spawned session, the substrate enqueues a NOTICE TURN to the
   lineage parent: origin `process:tightbeam`, a fact-shaped sentence — which
   child, what reason (the stage is durably recorded in the lifecycle event's
   detail; the sentence carries what the parent acts on). No menu, no verb to run, no
   substrate-suggested remedy. What to do about it is the parent's judgment.
3. **The durable carrier — no prose is ever parsed.** A notice turn is marked
   in `turns.requestRef` (the ledger's declared-unused slot, claimed by this
   spec) as `bubble:<cause_seq>` — the seq of the ORIGINAL failed turn. Cause
   context is re-derived from that turn's row (session, error, timestamps) at
   every rung; the notice prose is presentation, composed fresh per rung and
   never read back. Exactly-once per rung rides the existing mechanism:
   `turns.wakeId` UNIQUE, with the deterministic key
   `bubble:<cause_seq>:<recipient>` — a crash between recognition and enqueue
   re-attempts into a conflict, not a duplicate.
4. The notice turn's terminal state is the evidence, decided for ALL FOUR
   terminals:
   - **delivered** — the parent demonstrably ran a turn; it knows; the
     substrate is done. Retry, halt, redirect, `work-blocked`, report up:
     all inference from here.
   - **failed** — the parent is shown unable to run (same quota wall, or any
     other reason; the substrate does not care which). The climb continues:
     the same `bubble:<cause_seq>` moves one rung up as a new notice turn.
   - **canceled** — the recipient retired or the notice was canceled; either
     way this recipient will never act. The climb continues, exactly as for
     failed. (A canceled CAUSE turn never bubbles — rule 1; a canceled NOTICE
     still climbs, because the underlying fault remains untold.)
   - **failed_unknown** — the recipient was not SHOWN able. The climb
     continues. Worst case a recipient that did see it is climbed past and an
     ancestor hears the same fact — a spurious sentence, not a lost fault.
   A failed notice turn is a rung of the climb, never the start of a new
   bubble — notices about notices do not exist.
5. **Terminal rung — the alert to the user is not a turn.** When the climb
   exhausts the lineage (no rung above; a retired rung counts as exhausted —
   it can never run a turn), the substrate posts a substrate-authored message
   into the owner's main stream over the clawline wire: store-and-push, no
   model, no tokens, structurally incapable of sharing the failure mode that
   caused the climb. Store is truth; replay serves a disconnected user. In
   the same transaction it files `user-alerted` scope = the owner user id.
   When the owner has no main session row to carry the stream, the fact and
   the lifecycle event still file — log it and be done; the alert replays as
   product surface when one exists. Never enqueue to a composed key.
6. **Suppression while the alert stands:** the bubbling production's LHS
   includes "no standing `user-alerted` for the failing session's owner".
   Subsequent failures under an alerted owner fail with their own row and
   marker but do not re-climb and do not re-alert. The user has been told;
   the state machine knows.
7. **Retraction is observed, not declared:** the first turn that reaches
   `delivered` for ANY session owned by an alerted user is proof capacity
   exists. The substrate files `user-alert-cleared` for that owner in the
   delivery transaction. If work fails again, the climb re-runs and re-alerts
   from current state. Recovery is automatic when the cause heals; no
   operator verb exists for this.

Deliberate v1 naiveties, named: one notice per failed turn (no dedup across a
parent's many children — collapsing notices is a judgment about what the
parent wants to hear, which makes it inference's problem); `user-alerted`
scope is the root alone, not (root, cause) — a second distinct cause under an
already-alerted root rides the standing alert until it clears.

## Model policy is guidance

A markdown document, read by agents, never by the substrate: which models for
which task classes (with efforts), and what an agent may do when its model is
unavailable — switch per the table, assert `work-blocked` and report up, or
surface to the user for re-onboarding. This is where park/swap/respawn live
now: as prose judgment, exercised by inference. The substrate's entire
contribution to model unavailability is the failed turn and the bubble above.

## Explicitly deferred

- Statute-layer migration of production LHSs (completion path, needs a second
  consumer).
- Notice dedup / alert scoping by cause (inference's problem until shown
  otherwise).
- Any substrate awareness of WHY a session is blocked. The reason lives in
  the failed turns and the notice prose; the fact carries only that an
  authority said so.

## Pre-deletion leftovers

A database from before the adjudication deletion may carry
`adjudication_episodes`, `sessions.adjudicationHold`, and old-regime facts.
They are dead: no query names them, the new kinds share nothing with them,
and no boot reconciler exists or may be added to clean them. Fresh installs
never create them. Report dirt, never accommodate it — and never sweep it.

## Proofs owed by the implementation

1. A standing `work-blocked` fact stops prodding for exactly that holder —
   including a pending branch recorded before the assertion and drained after
   it; retraction resumes prodding; the turn queue accepts and claims turns
   throughout.
2. A spawned session's failed (and failed_unknown) turn produces a notice
   turn to its parent, deduped by deterministic wakeId; a canceled cause turn
   produces none; a failed, canceled, or failed_unknown notice climbs; a
   delivered notice ends the climb; a parentless session's failure marks its
   own stream and climbs nowhere.
3. With every lineage rung failing, the user's stream receives the wire alert
   and `user-alerted` stands; further failures under that root neither climb
   nor re-alert.
4. A delivered turn under an alerted root clears the alert; the next
   exhausted climb alerts again.
5. The substrate never files `work-blocked`; agents never file `user-alerted`
   (both refused at the verb seam).
6. The prod production's LHS is one function reading durable state only —
   asserted by test against its module surface.
