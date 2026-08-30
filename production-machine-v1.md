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
Standing facts remain outside the queue gate. Session existence and
`state = 'active'` gate each claim; the assignment-state gate below also
applies when a queued turn carries a non-null `turns.assignmentId`.

## Assignment-terminal queued-turn invalidation

Authority: `wi_154bf46b-acd6-4ff4-a2b0-732737a03d64` and its
`spirit-reviewed` verdict `att_6961f9b1-99df-47ec-82c8-f8284338b3ad`.
This amendment extends the queue contract. It does not change the production
machine's failure, retirement, or authorization policy.

### Goal

At each assignment-terminal transition, a turn already queued under that
assignment can start only if its claim committed before that transition.
A turn enqueue whose transaction sees an existing recipient session and that
assignment closed commits its input evidence but creates its turn directly as
terminal canceled; it never becomes queued. This assignment-terminal result
applies when the existing recipient session is active or retired. Reopening
makes turns whose enqueue transactions commit after reopen eligible until the
assignment's next terminal transition.
The ledger preserves the turn, attribution, wake, message, and lifecycle
evidence for each race result.

### Non-Goals

- This amendment does not cancel a running turn or rewrite a terminal turn.
- This amendment does not cancel a turn whose `assignmentId` is null or names
  another assignment.
- This amendment does not infer attribution from a prompt, origin, wake name,
  session holder, work item, or timing.
- This amendment does not change assignment close or reopen authorization,
  turn-read authorization, session-retirement authority, fault-bubble policy,
  or unknown-outcome recovery.
- This amendment does not add a schema field, public verb, request parameter,
  queue process, timer, retry, attribution backfill, or lifecycle backfill.
- This amendment does not change the public delivery result or wake eligibility
  contract.
- This amendment does not change the retired-recipient disposition for a turn
  whose `assignmentId` is null, names an open assignment, or names no
  assignment row.
- This amendment does not repair a non-null `turns.assignmentId` that names no
  assignment. The report-dirt path in ATI-10 fails that turn by a named cause
  instead of guessing an assignment or close disposition.

### Terms

- **Assignment-attributed turn:** a `turns` row whose `assignmentId` is
  non-null. The stored value is the complete assignment attribution.
- **Assignment-terminal transition:** one transaction that changes an
  assignment from `state = 'open'` to `state = 'closed'` with outcome
  `completed`, `surrendered`, or `revoked`.
- **Assignment-open truth:** in the claim transaction's current durable
  snapshot, the assignment named by `turns.assignmentId` exists with
  `state = 'open'`.
- **Head queued turn:** the queued turn with the lowest `turns.seq` for one
  session. This is the existing per-session FIFO boundary.
- **Matching queued turn:** a turn with `status = 'queued'` and
  `assignmentId` equal to the assignment-terminal transition's assignment id.
- **Closed-assignment enqueue:** an invocation of the shared turn enqueue seam
  whose recipient session row exists and whose non-null `assignmentId`
  resolves, in its transaction's durable snapshot, to an assignment with
  `state = 'closed'` and outcome `completed`, `surrendered`, or `revoked`.
- **Retired-recipient enqueue:** an invocation of the shared turn enqueue seam
  whose recipient session exists with `state = 'retired'` in that transaction's
  durable snapshot.
- **Legacy queued turn:** a matching queued turn found at boot whose assignment
  had already closed before this contract was active.
- **Lifecycle-covered turn:** a turn whose `seq` is greater than or equal to
  `turn_lifecycle_epoch.firstTurnSeq`. A turn below that boundary retains the
  existing legacy representation with no lifecycle-event backfill.
- **Fault-bubble notice turn:** the new ancestor notice for an existing failed
  cause, identified by `requestRef = bubble:<cause_seq>`. It carries null
  assignment attribution because it is notice work for the recipient, not
  work under the cause turn's assignment.
- **Valid assignment-terminal cancellation token:** the exact string
  `assignment-terminal:<outcome>:<assignmentId>`, where `<outcome>` is the
  closed assignment row's stored terminal outcome and `<assignmentId>` equals
  both that assignment row's stored id and the canceled turn's stored
  `assignmentId`. No other outcome, id, delimiter, suffix, or shape is valid.

### Assumptions

- The substrate stamps `turns.assignmentId` from an existing durable carrier;
  public prompt prose does not author it. `job-forensics-v2.md` owns that
  attribution contract.
- The database serializes assignment closure, reopen, session retirement, turn
  enqueue, turn claim, and boot recovery writes through transactions over the
  same ledger.
- `turn_lifecycle_events` permits one `terminal:committed` event and one
  `terminal:published` event per lifecycle-covered turn. Its epoch boundary
  excludes earlier turns from event backfill.
- Holder retirement closes the holder's open assignments as `revoked` before
  the existing session-retirement drain runs in the same retirement
  transaction.

### Invariants

**ATI-1 — Claim gate.** When a session has no running turn, `claim_next`
examines its head queued turn. That turn can transition to `running` only when
its session exists and is active, and either its `assignmentId` is null or
assignment-open truth holds. One atomic database statement rechecks the head
selection, these predicates, and the transition. `claim_next` does not skip an
unclaimable head turn to claim a later row.

**ATI-2 — Terminal drain.** Each assignment-terminal transition changes the
assignment state and cancels its matching queued turns in one transaction.
Each canceled row reaches `status = 'canceled'`, receives `endedAt`, retains
its existing fields and related rows, and records the assignment-terminal
cancellation token in `turns.error`.

**ATI-2E — Lifecycle evidence.** For each lifecycle-covered turn canceled by
ATI-2, ATI-2P, or ATI-5, the same transaction appends one
`terminal:committed` event whose `outcome` is `canceled`, whose `cause` is the
assignment-terminal cancellation token, and whose `principal` is
`process:tightbeam`. Existing terminal publication appends one
`terminal:published` event.

**ATI-2L — Legacy evidence boundary.** For each canceled turn below
`turn_lifecycle_epoch.firstTurnSeq`, the terminal turn row, its error token,
its `endedAt`, and its existing related rows are the historical evidence.
Cancellation appends no lifecycle event for that turn.

**ATI-2A — Lifecycle authority.** The lifecycle writer accepts an ownerless
terminal commit with an assignment-terminal cause only when the turn row is
`canceled`, its `error` and the event `cause` equal the valid
assignment-terminal cancellation token, the event outcome is `canceled`, and
the event principal is `process:tightbeam`. In the same transaction, the
writer resolves `turns.assignmentId` to the closed assignment row and compares
the cause with that row's stored id and outcome. A malformed cause or any row,
outcome, id, error, or principal mismatch returns the existing named
lifecycle-write refusal and appends no event.

**ATI-2P — Closed-assignment enqueue.** After the existing recipient-session
existence check succeeds, the shared ledger enqueue seam resolves a non-null
`assignmentId` before it inserts the turn. For a closed-assignment enqueue, the
caller transaction inserts the attributed turn directly with
`status = 'canceled'`, `endedAt`, and the valid assignment-terminal
cancellation token in `turns.error`. The seam appends the ordinary `accepted`
lifecycle event before the ATI-2E terminal event and returns the existing
successful turn-sequence shape. It creates no queued state. When the caller is
the shared turn-bearing delivery seam, that same transaction commits the input
message and consumes a pending wake as `fired`, when present; the turn retains
its message and wake identities, and the caller returns its existing
successful delivery shape. Replay by the same wake id or client-message
identity returns the existing dedupe result and creates no second message,
turn, accepted event, terminal event, or publication.

**ATI-2R — Recipient-state precedence.** The existing missing-recipient rule
precedes assignment resolution: an enqueue whose session row is absent returns
`{:error, :no_session}` and creates no turn. For an existing session row, ATI-2P
precedes recipient state: a closed-assignment enqueue creates the same directly
canceled turn when the recipient is active or retired. A retired-recipient
enqueue whose `assignmentId` is null, names an open assignment, or names no
assignment row retains the existing path. It creates a queued turn with its
accepted event and existing successful enqueue result. A turn-bearing delivery
commits its message and fires its pending wake in the same transaction.
`claim_next` returns `{:unclaimable, :session_retired}`. The existing
unclaimable-turn seam changes that queued turn to `failed` with error
`unclaimable: the session retired before this turn was claimed`, lifecycle
cause `unclaimable:session_retired`, outcome `failed`, and principal
`process:tightbeam`. Existing failed-cause publication and bubbling apply.

**ATI-3 — Exact scope.** The terminal drain selects by the exact stored
`turns.assignmentId` and `status = 'queued'`. It leaves a turn with null
attribution, a turn attributed to another assignment, and a turn already in
`running`, `delivered`, `canceled`, `failed`, or `failed_unknown` at its
pre-transition state.

**ATI-4 — Serialized race.** Assignment-terminal transition, recipient-session
retirement, turn-bearing enqueue, reopen, and claim transactions form one
serialized race boundary. An enqueue that commits while the assignment is open
and the recipient is active creates a queued turn; a later terminal transaction
cancels it under ATI-2. A terminal transaction that commits before enqueue
makes that enqueue commit a canceled turn under ATI-2P, whether recipient
retirement commits before or after that terminal transaction. A claim that
commits before the terminal transaction leaves a running turn for its ordinary
result. A reopen that commits before a new enqueue makes that new turn eligible
under ATI-1 when the recipient is active. A later reopen changes none of the
canceled race results. If a retired-recipient enqueue commits while its
assignment is open, ATI-2R creates the queued turn; a later terminal transaction
cancels it under ATI-2. If that terminal transaction commits before the
unclaimable failure, ATI-2 cancellation wins. If the unclaimable failure
commits while the assignment is still open, the failed result and its existing
bubble behavior win; a later terminal transaction leaves that terminal row
unchanged under ATI-3.

**ATI-5 — Boot convergence.** Before a session lane starts, boot cancels each
legacy queued turn whose non-null `assignmentId` names a closed assignment.
Boot uses the assignment row's stored outcome to produce the same cancellation
token as ATI-2. Repeating boot, replaying terminal publication, or repeating a
terminal command appends no second terminal event and publishes no second
terminal transition for that turn. Boot leaves a turn already canceled under
ATI-2P unchanged.

**ATI-6 — Reopen is prospective.** Reopening an assignment authorizes future
work. It does not change a turn canceled under ATI-2 or ATI-5 and does not
enqueue a replacement turn. It does not change a turn canceled under ATI-2P
whose enqueue committed while the assignment was closed. A turn whose enqueue
commits with that assignment open after reopen is eligible under ATI-1 until
the assignment's next terminal transition.

**ATI-7 — Fault evidence.** An assignment-terminal canceled cause turn does
not start a fault bubble. A `failed` or `failed_unknown` cause turn that
reached terminal before assignment closure retains its existing evidence and
exactly-once bubble behavior. A closed-assignment enqueue canceled under
ATI-2P starts no bubble when its existing recipient is active or retired. An
open-assignment retired-recipient turn failed under ATI-2R retains the existing
failed-cause bubble behavior. A canceled notice turn continues the underlying
fault's existing climb; it does not start a second bubble. The bubble production
enqueues each ancestor notice with `assignmentId = NULL`, so a closed cause
assignment does not assignment-gate the notice.

**ATI-8 — Existing boundaries.** The change adds no reader or writer
authority. For an already-authorized `turn-trace` read, the `turn` object adds
`assignment_id`, equal to stored `turns.assignmentId`, and `error`, equal to
stored `turns.error`; either value is null when its stored field is null. The
change removes, renames, or changes no existing response key. The existing
event projection exposes the cancellation token as `cause`, its principal,
and event timestamps. A caller that could not read the turn before this
amendment receives the existing `not_found` shape with none of these values.

**ATI-9 — Retirement composition.** During holder retirement, assignment
revocation applies ATI-2 before the existing session-retirement drain. The
assignment drain gives matching queued turns the assignment-terminal token.
The session-retirement drain then handles the holder's remaining queued turns
under its existing contract. A running turn follows ATI-4.

**ATI-10 — Missing attribution fails loudly.** If an active session's head
queued turn carries a non-null `assignmentId` that names no assignment,
`claim_next` returns
`{:unclaimable, {:assignment_missing, <turnSeq>, <assignmentId>}}` instead of
claiming that turn or a later row. The existing unclaimable-turn seam then
changes exactly that `turnSeq` to `failed` only if it remains queued, retains
the same `assignmentId`, and the assignment row remains absent. It changes no
other turn. A winning update sets `turns.error` to
`unclaimable: assignment row <assignmentId> does not exist` and appends a
terminal lifecycle event with cause `unclaimable:assignment_missing` and
principal `process:tightbeam` when the turn is lifecycle-covered. Existing
failed-cause bubbling applies. Whether the failure update wins or its
predicates have become false, the session lane immediately evaluates its next
claim without an external wake, timer, or enqueue. Existing `no_session` and
`session_retired` unclaimable behavior is unchanged for a turn whose
`assignmentId` is null, names an open assignment, or names no assignment row.
ATI-2P governs a turn whose existing assignment is closed.

### Architecture

The assignment state row is the single decision-free source for the assignment
gate. The session row remains the existing source for recipient existence and
claimability.

The shared completion, surrender, and revocation transaction invokes one
ledger mutation seam that cancels queued turns by exact `assignmentId`. The
shared ledger enqueue seam first applies its existing recipient-session
existence rule. For an existing recipient, it resolves non-null assignment
attribution in the caller transaction. A closed assignment makes the seam
create the turn as canceled with the stored assignment's terminal token,
regardless of whether the existing recipient is active or retired. A null or
open assignment, or a missing assignment row, leaves retired-recipient
admission and unclaimable handling on its existing path. A turn-bearing
delivery caller commits its ordinary wake and message evidence in the same
transaction. The claim update evaluates session state before reporting an
assignment-state mismatch and adds the
assignment-open predicate beside its existing active-session predicate. Boot
invokes the same cancellation semantics for queued rows joined to closed
assignments before it starts session lanes.

The cancellation token uses stored turn and assignment fields. The lifecycle
writer validates its exact shape and cross-row equality; it does not authorize
by prefix. The existing unique terminal lifecycle keys make repeat recovery
and publication no-ops after the first committed cancellation. No prompt or
error prose parser, elapsed-time threshold, or inference participates. The
assignment-terminal token is a typed lifecycle-cause convention, not prose
from a caller.

The lifecycle writer's system-terminal authority list gains only the exact
ATI-2A case, which serves transition-time, post-close-enqueue, and boot
cancellation. The existing unclaimable-turn path gains the exact ATI-10 tuple,
single-row compare-and-set, and immediate next-claim evaluation. The
authorized `turn-trace` projection adds the two ATI-8 fields. The bubble
producer continues to omit assignment attribution from ancestor notices.

Mechanism choice — ADD the exact assignment-state gate at enqueue and claim,
and reuse the terminal cancellation token. For an existing recipient, closed
assignment state takes precedence because it is the durable decision that this
attributed work ended; recipient retirement remains the cause only while the
assignment is open, attribution is null, or the assignment row is missing.
Refusing the whole delivery would discard required message or wake evidence.
Retaining a closed-assignment queued row would let reopen resurrect it.
Deleting assignment attribution would destroy required causality.

Operating pattern taught to agents: none. This is substrate physics derived
from durable rows; it adds no agent instruction or manual step.

### Acceptance

Each check uses the real assignment-close, ledger-enqueue, ledger-claim,
turn-bearing-delivery, boot, reopen, retirement, lifecycle-publication, and
fault-bubble transaction seams. A test that edits staged state instead of
exercising the named seam does not satisfy the check.

1. **ATI-A1 — Each disposition.** Given three open assignments with one
   already-fired lifecycle-covered queued turn attributed to each, when the
   holder completes the first, surrenders the second, and an authorized
   principal revokes the third, then each close and its matching cancellation
   commit together. Each turn is `canceled`, and its error equals
   `assignment-terminal:<outcome>:<assignmentId>`. Each terminal-event cause
   equals the same token, and each event principal is `process:tightbeam`.
   Each turn, wake, attribution, and existing lifecycle row remains readable.
2. **ATI-A2 — Terminal wins.** Given an open assignment with a
   lifecycle-covered attributed queued turn, when its terminal transaction
   commits before a concurrent claim, then the claim returns no turn and the
   row remains canceled with one committed terminal event and one terminal
   publication.
3. **ATI-A3 — Claim wins.** Given the same initial state, when claim commits
   before the terminal transaction, then the turn remains running through the
   close and reaches its ordinary delivered, failed, canceled, or
   failed-unknown result. The assignment drain adds no assignment-terminal
   event to that turn.
4. **ATI-A4 — Boot, replay, and reopen.** Given two synthetic legacy queued
   rows attributed to closed assignments, with one turn below the lifecycle
   epoch and one turn inside it, when boot runs twice, terminal publication
   replays, both assignments reopen, boot runs again, and one new attributed
   turn is enqueued for each reopened assignment, then the first boot cancels
   both legacy turns. The pre-epoch turn gains no lifecycle event or lifecycle
   publication. The covered turn gains one committed event and one published
   event. Later actions leave both legacy row shapes and event counts
   unchanged. Neither reopen creates a turn, but each new post-reopen turn is
   claimable and follows its ordinary running and terminal path.
5. **ATI-A5 — Attribution boundary.** Given one queued turn attributed to
   assignment A, one attributed to open sibling assignment B, one with null
   attribution, and one ordinary user turn with null attribution, when A
   closes, then only A's queued turn changes. The other three remain
   claimable under their pre-amendment session gates.
6. **ATI-A6 — Turn-state boundary.** Given queued, running, delivered,
   canceled, failed, and failed-unknown turns attributed to one open
   assignment, when it closes, then only the queued rows gain the
   assignment-terminal cancellation. Each other row and lifecycle history is
   byte-for-byte unchanged.
7. **ATI-A7 — Missing attribution dirt.** Given an active session with no
   running turn and three lifecycle-covered queued turns in sequence order —
   head turn M whose non-null `assignmentId` names no assignment, turn B
   attributed to an open sibling assignment, and turn N with null attribution
   — when claim and the unclaimable-turn seam run, then claim returns
   `{:unclaimable, {:assignment_missing, M.seq, M.assignmentId}}`. The seam
   changes only M to `failed` with the ATI-10 error and lifecycle cause, then
   the immediate next claim starts B. After B reaches terminal, the next claim
   starts N. In a second fixture where B precedes M, claim starts B before it
   diagnoses M. In a third fixture, inserting M's assignment as open before
   the failure update makes the compare-and-set change no row; the immediate
   next claim starts M. No case infers another assignment, fails a batch,
   cancels M as an assignment disposition, or changes another turn.
8. **ATI-A8 — Retirement order.** Given a retiring holder with one attributed
   turn whose claim committed before retirement, one attributed queued turn
   whose claim did not commit before retirement, and one queued
   null-attributed turn, when retirement commits before the second attributed
   turn's claim, then assignment revocation cancels that queued attributed turn
   with the revoked assignment token. The existing session drain cancels the
   null-attributed turn with its session-retirement reason. The retirement
   transaction leaves the already-running attributed turn and its lifecycle
   rows unchanged; its later ordinary terminal or boot recovery follows the
   existing running-turn contract.
9. **ATI-A9 — Bubble boundary.** Given one assignment-attributed queued cause
   turn and one attributed cause turn that failed before closure, when the
   assignment closes and the recognizer replays across restart, then the
   canceled cause produces no bubble and the failed cause retains one bubble
   per existing recipient key. Each new ancestor notice has
   `assignmentId = NULL`, remains claimable after the cause assignment closes,
   and dedupes by its existing recipient key. Given a notice turn canceled by
   session retirement or explicit cancellation, its underlying cause advances
   under the existing canceled-notice rule without creating a
   bubble-about-a-bubble.
10. **ATI-A10 — Authorization, observability, and compatibility.** Given a
    lifecycle-covered matching turn and principals that can and cannot close
    the assignment or read its turn, when ATI-2 cancels the turn, then close
    authorization and trace-read authorization equal the pre-amendment
    results. The authorized trace's `turn.assignment_id` equals the stored
    assignment id, `turn.error` equals the cancellation token, and the event
    exposes that token as its cause with principal and timestamps. Every
    pre-amendment trace key and value remains unchanged. The unauthorized read
    returns the existing `not_found` shape without cancellation detail.
11. **ATI-A11 — Seven-row non-recurrence fixture.** Given synthetic cause turns
    69120, 69122, 69123, 69124, 69138, 69142, and 69143 that reach `failed`
    before their assignment closes, when closure, retirement, bubble
    recognition, restart, and replay run, then the seven cause rows and their
    terminal evidence remain unchanged. Each historical failure produces only
    its existing deterministic ancestor notice. No child turn is reclaimed,
    no cancellation replaces a historical failure, and no duplicate notice is
    created.
12. **ATI-A12 — Lifecycle cause authority.** Given canceled,
    lifecycle-covered turns, two valid closed assignments, and
    otherwise-identical direct lifecycle writes, when the writes respectively
    use `assignment-terminal:revoked:<assignmentId>:extra`, a permitted
    disposition different from the attributed closed assignment's stored
    outcome, the other valid closed assignment's id instead of stored
    `turns.assignmentId`, a turn `error` different from the event cause, a
    non-canceled event outcome, and a principal other than
    `process:tightbeam`, then each write returns
    `{:error, {:turn_lifecycle_write_rejected,
    :invalid_terminal_authority}}` and appends no event.
13. **ATI-A13 — Post-close delivery for each disposition.** Given three
    assignments already closed as `completed`, `surrendered`, and `revoked`,
    three active recipient sessions, and pending attributed wakes Wc, Ws, and
    Wr respectively, when the three wakes run through the shared turn-bearing
    delivery transaction and terminal publication runs, then the three input
    messages commit with three new turns created directly as `canceled`. Each
    turn retains its assignment id, has `endedAt`, and has the exact token for
    its stored assignment outcome. Each turn has one accepted lifecycle event,
    one committed canceled event, and one published canceled event. Wc, Ws,
    and Wr become `fired` and retain their respective turn identities. Each
    caller receives its existing successful delivery shape, and no row enters
    `queued` or starts a fault bubble.
14. **ATI-A14 — Post-close replay, reopen, and mixed-queue progress.** Given a
    closed assignment A, an open sibling assignment B in the same active
    session, and a pending wake attributed to A, when the wake delivers, the
    process restarts, the same wake delivery replays, A reopens, and turns
    attributed to B, with null attribution, and attributed to reopened A are
    enqueued in that order, then the original A delivery remains one canceled
    turn with one message, accepted event, committed event, and publication.
    Replay creates no second row or event. Without boot cleanup, a repair
    timer, or another enqueue, successive claim evaluations start the B turn,
    the null-attributed turn, and the new post-reopen A turn in FIFO order. The
    canceled A turn never becomes claimable and does not block those turns.
15. **ATI-A15 — Open assignment with retired recipient.** Given an open
    assignment A held by an active session, a different retired recipient R
    with active lineage parent P, no queued or running turn for R, and a pending
    `targetGate = 0` decision-notice wake Wo that targets R and carries A's
    attribution, when Wo fires, `claim_next` and the unclaimable-turn seam run,
    terminal publication runs, the bubble recognizer runs, the process
    restarts, and the same wake delivery replays, then Wo's message commits,
    Wo becomes `fired`, and its turn first exists as `queued` with one accepted
    event. `claim_next` returns `{:unclaimable, :session_retired}`. The
    unclaimable-turn seam changes that turn to `failed` with the ATI-2R error,
    cause, outcome, and principal. Terminal publication occurs once. The failed
    cause creates one existing-shape notice for P with `assignmentId = NULL`.
    Replay returns the existing dedupe result and creates no second message,
    turn, event, publication, or notice. Assignment A remains open.
16. **ATI-A16 — Closed assignment with retired recipient.** Given a closed
    assignment A, a retired recipient R with active lineage parent P, no queued
    or running turn for R, and a pending `targetGate = 0` decision-notice wake
    Wc that targets R and carries A's attribution, when Wc fires, terminal
    publication runs, `claim_next` runs, the bubble recognizer runs, the process
    restarts, and the same wake delivery replays, then Wc's message commits, Wc
    becomes `fired`, and its turn is created directly as `canceled` with A's
    assignment-terminal token. The turn has one accepted event, one committed
    canceled event, and one published canceled event. `claim_next` returns
    `:none` for R's empty queued set. The turn gains no
    `unclaimable:session_retired` error or event and creates no bubble. Replay
    returns the existing dedupe result and creates no second message, turn,
    event, publication, or notice.
17. **ATI-A17 — Retired-recipient failure versus assignment close.** Given two
    equivalent fixtures with an open assignment A and one ATI-2R queued turn
    for a retired recipient, when A's terminal transaction commits before the
    unclaimable-turn seam in the first fixture, then ATI-2 cancels the turn with
    A's assignment-terminal token, the unclaimable-turn seam changes no row,
    and no bubble starts. When the unclaimable-turn seam commits while A
    remains open in the second fixture, then the turn becomes `failed` with
    the ATI-2R error and event and produces
    its one existing bubble. Closing A afterward leaves that failed row and its
    lifecycle evidence unchanged. Restart, terminal publication replay, and
    bubble recognition replay create no second event, publication, or notice in
    either fixture.

Traceability: ATI-A1 verifies ATI-2, ATI-2E, and ATI-2A; ATI-A2 and ATI-A3
verify ATI-1 and ATI-4; ATI-A4 verifies ATI-2L, ATI-5, and ATI-6; ATI-A5 and
ATI-A6 verify ATI-3; ATI-A7 verifies ATI-1 and ATI-10; ATI-A8 verifies ATI-9;
ATI-A9 and ATI-A11 verify ATI-7; ATI-A10 verifies ATI-8; ATI-A12 verifies the
rejection boundary in ATI-2A; ATI-A13 verifies ATI-2P, ATI-2E, ATI-2A, and the
three post-close disposition tokens; ATI-A14 verifies ATI-1, ATI-4, ATI-5,
ATI-6, ATI-2P replay, and mixed-queue progress; ATI-A15 verifies ATI-2R's
open-assignment retired-recipient path and ATI-7 failed-cause bubbling; ATI-A16
verifies ATI-2P's precedence over recipient retirement, ATI-2R's boundary, and
ATI-7 canceled-cause suppression; ATI-A17 verifies both ATI-4 race orders,
ATI-2R failure, ATI-3 terminal preservation, and ATI-7 bubble disposition.

### Open Questions

None. The amendment has no blocking or non-blocking product decision left for
implementation.

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
