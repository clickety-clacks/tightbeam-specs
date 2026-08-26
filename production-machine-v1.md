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

Once an assignment reaches a terminal disposition, a turn durably attributed
to that assignment can start only if its claim committed before the terminal
disposition. The ledger preserves the turn, attribution, wake, and lifecycle
evidence for either race result.

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
  response field, queue process, timer, retry, attribution backfill, or
  lifecycle backfill.
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
- **Matching queued turn:** a turn with `status = 'queued'` and
  `assignmentId` equal to the assignment-terminal transition's assignment id.
- **Legacy queued turn:** a matching queued turn found at boot whose assignment
  had already closed before this contract was active.
- **Lifecycle-covered turn:** a turn whose `seq` is greater than or equal to
  `turn_lifecycle_epoch.firstTurnSeq`. A turn below that boundary retains the
  existing legacy representation with no lifecycle-event backfill.
- **Fault-bubble notice turn:** the new ancestor notice for an existing failed
  cause, identified by `requestRef = bubble:<cause_seq>`. It carries null
  assignment attribution because it is notice work for the recipient, not
  work under the cause turn's assignment.
- **Assignment-terminal cancellation token:**
  `assignment-terminal:<outcome>:<assignmentId>`, where `<outcome>` is the
  assignment row's stored terminal outcome and `<assignmentId>` is its stored
  id.

### Assumptions

- The substrate stamps `turns.assignmentId` from an existing durable carrier;
  public prompt prose does not author it. `job-forensics-v2.md` owns that
  attribution contract.
- The database serializes assignment closure, turn claim, and boot recovery
  writes through transactions over the same ledger.
- A turn has one-way state paths:
  `queued -> running -> delivered | canceled | failed | failed_unknown`.
- `turn_lifecycle_events` permits one `terminal:committed` event and one
  `terminal:published` event per lifecycle-covered turn. Its epoch boundary
  excludes earlier turns from event backfill.
- Holder retirement closes the holder's open assignments as `revoked` before
  the existing session-retirement drain runs in the same retirement
  transaction.

### Invariants

**ATI-1 — Claim gate.** A queued turn can transition to `running` only when
its session exists and is active, and either its `assignmentId` is null or
assignment-open truth holds. The claim update evaluates these predicates and
changes the turn state in one atomic database statement.

**ATI-2 — Terminal drain.** Each assignment-terminal transition changes the
assignment state and cancels its matching queued turns in one transaction.
Each canceled row reaches `status = 'canceled'`, receives `endedAt`, retains
its existing fields and related rows, and records the assignment-terminal
cancellation token in `turns.error`.

**ATI-2E — Lifecycle evidence.** For each lifecycle-covered turn canceled by
ATI-2 or ATI-5, the same transaction appends one `terminal:committed` event
whose `outcome` is `canceled`, whose `cause` is the assignment-terminal
cancellation token, and whose `principal` is `process:tightbeam`. Existing
terminal publication appends one `terminal:published` event.

**ATI-2L — Legacy evidence boundary.** For each canceled turn below
`turn_lifecycle_epoch.firstTurnSeq`, the terminal turn row, its error token,
its `endedAt`, and its existing related rows are the historical evidence.
Cancellation appends no lifecycle event for that turn.

**ATI-2A — Lifecycle authority.** The lifecycle writer accepts an ownerless
terminal commit with an `assignment-terminal:` cause only when the outcome is
`canceled` and the principal is `process:tightbeam`. It rejects the same cause
for another outcome or principal through its existing named lifecycle-write
refusal.

**ATI-3 — Exact scope.** The terminal drain selects by the exact stored
`turns.assignmentId` and `status = 'queued'`. It leaves a turn with null
attribution, a turn attributed to another assignment, and a turn already in
`running`, `delivered`, `canceled`, `failed`, or `failed_unknown` at its
pre-transition state.

**ATI-4 — Serialized race.** The terminal drain and the claim gate form one
serialized race boundary. A committed claim wins and leaves a running turn
for its ordinary result. A committed terminal transition wins and leaves a
canceled turn that no claim can start.

**ATI-5 — Boot convergence.** Before a session lane starts, boot cancels each
legacy queued turn whose non-null `assignmentId` names a closed assignment.
Boot uses the assignment row's stored outcome to produce the same cancellation
token as ATI-2. Repeating boot, replaying terminal publication, or repeating a
terminal command appends no second terminal event and publishes no second
terminal transition for that turn.

**ATI-6 — Reopen is prospective.** Reopening an assignment authorizes future
work. It does not change a turn canceled under ATI-2 or ATI-5 and does not
enqueue a replacement turn.

**ATI-7 — Fault evidence.** An assignment-terminal canceled cause turn does
not start a fault bubble. A `failed` or `failed_unknown` cause turn that
reached terminal before assignment closure retains its existing evidence and
exactly-once bubble behavior. A canceled notice turn continues the underlying
fault's existing climb; it does not start a second bubble. The bubble
production enqueues each ancestor notice with `assignmentId = NULL`, so a
closed cause assignment does not assignment-gate the notice.

**ATI-8 — Existing boundaries.** The change adds no reader or writer
authority. An authorized existing turn or lifecycle read exposes the canceled
status, stored `assignmentId`, assignment-terminal cancellation token, event
principal, and timestamps. A caller that could not read the turn or assignment
before this amendment gains no access through the cancellation.

**ATI-9 — Retirement composition.** During holder retirement, assignment
revocation applies ATI-2 before the existing session-retirement drain. The
assignment drain gives matching queued turns the assignment-terminal token.
The session-retirement drain then handles the holder's remaining queued turns
under its existing contract. A running turn follows ATI-4.

**ATI-10 — Missing attribution fails loudly.** If a queued turn carries a
non-null `assignmentId` that names no assignment, `claim_next` returns
`{:unclaimable, :assignment_missing}` instead of claiming it. The existing
unclaimable-turn seam then changes that queued row to `failed`, sets
`turns.error` to
`unclaimable: assignment row <assignmentId> does not exist`, and appends a
terminal lifecycle event with cause `unclaimable:assignment_missing` and
principal `process:tightbeam` when the turn is lifecycle-covered. Existing
failed-cause bubbling applies. The update rechecks that the assignment row is
still absent in the same statement that changes the turn state.

### Architecture

The assignment state row is the single decision-free source for this gate.
The shared completion, surrender, and revocation transaction invokes one
ledger mutation seam that cancels queued turns by exact `assignmentId`. The
claim update adds the assignment-open predicate beside its existing active-
session predicate. Boot invokes the same cancellation semantics for queued
rows joined to closed assignments before it starts session lanes.

The cancellation token uses fields already visible through authorized turn
and lifecycle reads. The existing unique terminal lifecycle keys make repeat
recovery and publication no-ops after the first committed cancellation. No
prompt or error prose parser, elapsed-time threshold, or inference
participates. The assignment-terminal token is a typed lifecycle-cause
convention, not prose from a caller.

The lifecycle writer's system-terminal authority list gains only the exact
ATI-2A case. The existing unclaimable-turn path gains the exact ATI-10 value
and assignment-absence predicate. The bubble producer continues to omit
assignment attribution from ancestor notices.

Mechanism choice — ADD the exact state gate: deleting assignment attribution
would destroy required causality, while accepting the failure would let work
start after its recorded authority ended.

Operating pattern taught to agents: none. This is substrate physics derived
from durable rows; it adds no agent instruction or manual step.

### Acceptance

Each check uses the real assignment-close, ledger-claim, boot, reopen,
retirement, lifecycle-publication, and fault-bubble transaction seams. A test
that edits staged state instead of exercising the named seam does not satisfy
the check.

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
   replays, both assignments reopen, and boot runs again, then the first boot
   cancels both turns. The pre-epoch turn gains no lifecycle event or lifecycle
   publication. The covered turn gains one committed event and one published
   event.
   Later actions leave both row shapes and event counts unchanged. Neither
   reopen creates a queued turn.
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
7. **ATI-A7 — Missing attribution dirt.** Given an active session with a
   lifecycle-covered queued turn whose non-null `assignmentId` names no
   assignment, when claim and the unclaimable-turn seam run, then claim returns
   `{:unclaimable, :assignment_missing}` and the seam changes that turn to
   `failed` with the ATI-10 error and lifecycle cause. A transaction that
   inserts the named assignment before the failure update makes the predicate
   false and leaves the turn queued. Neither order infers another assignment,
   cancels the turn as an assignment disposition, or grants a new principal
   access.
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
10. **ATI-A10 — Authorization and privacy.** Given a lifecycle-covered
    matching turn and principals that can and cannot close the assignment or
    read its turn, when ATI-2 cancels the turn, then close authorization results
    and read authorization results equal the pre-amendment results. The
    authorized trace contains the exact token, principal, assignment
    attribution, and timestamps; the unauthorized read returns its existing
    refusal shape without cancellation detail.
11. **ATI-A11 — Seven-row non-recurrence fixture.** Given synthetic cause turns
    69120, 69122, 69123, 69124, 69138, 69142, and 69143 that reach `failed`
    before their assignment closes, when closure, retirement, bubble
    recognition, restart, and replay run, then the seven cause rows and their
    terminal evidence remain unchanged. Each historical failure produces only
    its existing deterministic ancestor notice. No child turn is reclaimed,
    no cancellation replaces a historical failure, and no duplicate notice is
    created.
12. **ATI-A12 — Lifecycle cause authority.** Given otherwise-identical direct
    lifecycle writes that use an `assignment-terminal:` cause, when one write
    uses a non-canceled outcome and another uses a principal other than
    `process:tightbeam`, then each write returns the existing named
    lifecycle-write refusal and appends no event.

Traceability: ATI-A1 verifies ATI-2, ATI-2E, and ATI-2A; ATI-A2 and ATI-A3
verify ATI-1 and ATI-4; ATI-A4 verifies ATI-2L, ATI-5, and ATI-6; ATI-A5 and
ATI-A6 verify ATI-3; ATI-A7 verifies ATI-1 and ATI-10; ATI-A8 verifies ATI-9;
ATI-A9 and ATI-A11 verify ATI-7; ATI-A10 verifies ATI-8; ATI-A12 verifies the
rejection boundary in ATI-2A.

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
