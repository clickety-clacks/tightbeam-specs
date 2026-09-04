# Owner decision request relief v1

Status: specification for build — Mike written instruction, 2026-09-04
Work item: `wi_3d328d28-4c3c-4405-a624-427426fa10d5`
Posture: HEAVY (`att_4a8e3cc4` on `asg_14e7590c`)
Evidence: `art_02574fb9`, sha256
`83782fe8522c87066d3b9eddb7207c5e8606e5a55e6346c90fdb6c7047e386b8`

Authority, verbatim (Mike, 2026-09-04):

> ROOT CAUSE, file it as a work item and staff it: the completion rail refuses
> terminal receipts on work that is landed and independently reviewed, and lanes
> respond by raising owner-facing decision requests. That rail is manufacturing
> paperwork for Mike. Fix it so a landed, reviewed card can close without an
> owner ruling.

## Goal

An owner-facing decision request that exists only because an agent could not
finish its bookkeeping is clearable by an agent, without an owner ruling, and
without giving any agent the power to decide a question that is genuinely the
owner's.

That is the whole goal. Two measured facts set its size.

**The raise rate.** Over the fourteen days to 2026-09-04 the org raised between
30 and 69 operator decision requests per day. The owner has personally ruled 494
of them.

**The clearing rate.** Zero of them were cleared by an agent, because no agent
path exists. `operator-rule` refuses any principal that is not the owner user.
`operator-withdraw` refuses anyone but the owner or the original raiser.
`attest` on the underlying card refuses anyone but that card's holder. When the
raiser retires, the last remaining path closes and the row can only be cleared
by the owner in person.

On 2026-09-04 at 19:00 UTC the owner cleared four such rows by hand
(`dr_8d3ea46f`, `dr_fa2e0f91`, `dr_0cdc5e80`, `dr_112e519e`). Their raisers had
retired days earlier; three of the four asked about work that had since
completed. That hand-clearing is the cost this specification exists to stop
recurring.

## Non-Goals

Named as deliberately as the goal, because each is a thing a reader could
mistake this document for permission to build.

1. **Not a redesign of decision requests.** The `statute`, `effort`, and
   `operator` arms keep their current shapes, kinds, and lifecycles. One
   authorization predicate changes and one query filter is deleted.
2. **No new notification surface, dashboard, digest, or queue view.** Nothing in
   this document displays decision requests to anyone.
3. **No new receipt kind, verdict kind, attest kind, or decision request kind.**
   Section "Q4" establishes that the existing rows already carry what is needed.
4. **No classifier.** Nothing here decides, by machine, whether a question is
   bookkeeping or a real owner decision. Section "Q5" explains why that is a
   refusal rather than an omission.
5. **Not a widening of who may RULE an operator request.** Ruling authority is
   unchanged and, in one respect noted in Open Questions, is to be tightened
   rather than relaxed.
6. **No change to the four named completion rails' predicates.**
   `completion-requires-review`, `completion-requires-verification`,
   `completion-requires-results-artifact`, and
   `code-review-requires-passing-tests` keep their `deny_when` clauses exactly
   as written. This document changes what an agent may do about a request
   already raised, and what the guidance tells an agent to do instead of raising
   one. It does not weaken a rail.
7. **No installation, service, schema, adapter, or host change.** Repository
   work only. The production host is locked at 0.1.8 under Mike's 2026-09-02
   change law. Nothing in this document may be applied to a running host without
   that law's separate two-step ceremony.

## Terms

**Operator decision request.** A row in `decision_requests` with
`kind = 'operator'`, addressed to the org's owner user, carrying a question and
a set of labelled options.

**Rule.** To answer an operator decision request by selecting one of its
options. Writes `status = 'ruled'` with a `decision`, a `ruledBy`, a `ruledAt`,
and a `rulingFactId`.

**Retract.** To remove an operator decision request from the open set without
answering it. Writes `status = 'withdrawn'` with a `withdrawnBy` and a
`withdrawnReason`, and writes NO decision. Retraction says the question is no
longer being asked. It never says what the answer would have been. The verb is
the existing `operator-withdraw`; this document adds no new verb.

**Raiser.** The session recorded in `decision_requests.raiserSessionKey`.

**Subject card.** The assignment named by `decision_requests.assignmentId`, when
that column is non-NULL. An operator request may have no subject card.

**Opener.** For an assignment, the principal in `openedBySession`, or the
owner's personal session when the card was opened by `openedByUser`. The org's
dispatch law already makes the opener the accountable party for a card it opened:
it states the expectation, it holds the card open, and it disposes of the work.

**Rail friction.** A state in which an agent's work is done and recorded, and
the substrate refuses its bookkeeping verb. The agent needs a lawful way to file
what happened. It does not need a product decision.

**Genuine owner decision.** A question whose answer changes product behaviour,
scope, priorities, release intent, user experience, commitments, or a trust
root; or which is sensitive, destructive, security-relevant, costly, hard to
reverse, or dangerous. `dr_24edf371`, "name the trust root for self-healing
satellite CLI delivery", is the worked example in the current open set, and it
is correctly the owner's.

## Assumptions

Stated separately because each is a thing believed true of the world today, not
a thing this document makes true. If one is false, the design above it moves.

**A1.** `decision_requests` carries `assignmentId`, `raiserSessionKey`,
`withdrawnBy`, and `withdrawnReason` columns, and its CHECK constraint refuses
any row with `status <> 'ruled'` that carries a non-NULL `decision`,
`rationale`, `ruledBy`, `ruledAt`, `rulingFactId`, or `ruledViaSessionKey`.
Verified against the live schema, 2026-09-04.

**A2.** `assignments` carries `openedBySession` and `openedByUser`, exactly one
of which is non-NULL. Verified in source.

**A3.** Session retirement already calls a kind-agnostic withdrawal routine on
the retiring session's open decision requests. Verified in source; its actual
filter is the defect at "Q3".

**A4.** An operator request's `assignmentId`, where present, names a card in the
same org and under the same owner as the request. No cross-owner case exists in
the live data.

**A5.** The org has exactly one owner user. Multi-owner orgs are outside this
document.

**A6.** Rail refusals are recorded in `events` with `kind = 'denied'`, which is
where this document's denial counts come from. There is no separate rail denial
table. The counts are therefore complete for the window measured and cannot be
broken down further without new recording, which is a Non-Goal.

## Invariants

**I1. Every genuine product decision and every trust-root decision stays with
the owner.** No agent may select an option on an operator decision request.
This is the invariant the whole document is built to preserve, and every
requirement below is written so that satisfying it cannot violate this.

**I2. Retraction confers no permission.** Retracting a request removes the
question and authorizes nothing. If the retracted question was genuinely the
owner's, the work it gated is still not authorized to proceed, and the agent
that retracted has gained nothing by retracting. This is what makes widening
retraction safe where widening ruling would not be. An agent that retracts a
real owner question has not stolen a decision; it has only lost its own place in
the queue, and must raise again.

**I3. An agent-authored ruling is unrepresentable, not merely forbidden.** The
storage constraint already refuses any `ruled` row whose `ruledBy` is not the
owner user, and refuses any non-`ruled` row that carries a decision at all.
There is no shape in the table for "an agent decided this". That is physics, and
this document neither relaxes it nor relies on prose to enforce it.

**I4. Every clearing act names its actor and its cause.** A retraction records
`withdrawnBy` and `withdrawnReason`. A wrong retraction is therefore
attributable to the session that made it, on the record, without a classifier
having to have been right.

**I5. Substrate-authored clearing states its own cause.** Where the substrate
itself retracts a request, the reason is a fixed sentinel naming the mechanical
cause, never an inferred judgment about the question's content.

## Architecture

The design in one sentence: **widen who may RETRACT an operator request, never
who may RULE one, and make session retirement do what its own code comment
already claims it does.**

### The seam

`decision_requests` already separates two acts that a reader might blur. Ruling
writes an answer. Retraction writes an absence. The table's constraint binds an
answer to the owner user and forbids an answer on any other status. So the
retraction path can be widened to agents without any change to the constraint,
and without any new way for an agent's judgment to enter the record as the
owner's.

That is the whole architectural idea. Everything below is its application.

### R1 — the subject card's opener may retract

`operator-withdraw` currently authorizes the owner user, or a session that is
both under the same owner AND is the request's original raiser. Add one
authorized principal: the session that opened the request's subject card.

Resolve the opener from `assignments.openedBySession`, or from the owner's
personal session key where the card was opened by `openedByUser`. The same-owner
check that guards the raiser path guards this one identically.

Why the opener and not someone else. The opener already carries this card's
accountability under the dispatch law: it stated the expectation, it holds the
card, it disposes of the work. A request raised against a card is a report by
the holder that it cannot finish that card's bookkeeping. The opener is the
principal who was already going to have to deal with that. Authority to retract
the question derives from authority over the work the question is about.

Rejected: any session under the same owner. Too wide by a distance. It would let
any of the org's sessions silence the trust-root question, and it derives
authority from nothing but co-ownership.

Rejected: a designated adjudicator role. It invents a principal, and per the
subtraction doctrine a mechanism named after a cognitive act is compensation for
not having a mind. The opener is a mind, and it is already there.

### R2 — a request with no subject card keeps today's authority

Where `assignmentId` is NULL, the authorized set is unchanged: the owner, or the
raiser. No card, no derived authority.

This is not an edge case tidied away. It is load-bearing for I1. `dr_24edf371`,
the trust-root question and the one genuine owner decision in the current open
set, has a NULL `assignmentId`. The shape of a request that is truly about the
product, rather than about a card's bookkeeping, is exactly the shape this
requirement leaves alone.

### R3 — retirement stops excluding the only kind the org raises

The retirement withdrawal routine's own documentation states that retirement
withdraws ALL of a retiring session's open decision request rows on that
session's behalf, withdrawal being the one lawful judgment-free exit every arm
answers to. Its query then excludes `kind = 'operator'`.

Delete that exclusion. The comment describes the intended behaviour correctly;
the filter contradicts it.

The measured consequence of the contradiction: across the entire live database,
for every kind, zero rows carry the retirement withdrawal reason. The routine
has never cleared anything in production, because the org raises operator
requests and effort requests, effort requests supersede rather than withdraw,
and operator requests were excluded. The sweep excludes precisely the one kind
that exists.

### R4 — retirement clearing keys on the raiser's state, not only the retirement event

The routine runs from the retirement event alone. A session that retired before
this change ships is never revisited, so its rows stay open forever with no
lawful actor.

Key the clearing on the raiser session's recorded state instead, so that an open
operator request whose raiser is already retired is cleared on the next pass.
The mechanism must be idempotent: a request already withdrawn, ruled, or
superseded is left untouched.

R3 and R4 together are the answer to "what happens to a request whose raiser has
retired". R3 alone fixes the future. R4 is what reaches a row that is already
stranded.

### R5 — one guidance paragraph on the raise side

At the kungfu layer, not the substrate: the agent-facing guidance for raising an
operator decision request gains one paragraph, saying that a request must not be
raised for a bookkeeping refusal that a lawful agent path can clear, and naming
the paths — retract when the question has dissolved, take the opener's
adjudication, open a fresh review round where the evidence was never filed.

This is guidance and nothing else. It is not a rail, not a check, and not a
denial. The substrate must not test whether an agent obeyed it, for the reason
given at Q5.

### What the substrate does NOT gain

No new verb. No new column. No new table. No new kind. No new rail. No
migration. R1, R3, and R4 are three edits to existing predicates and one query;
R5 is prose.

## The five questions

### Q1. Widen who may clear, or stop the raising, or both?

**Both, at two different rungs of the escalation ladder, and neither is
sufficient alone.**

Stopping the raising is guidance (R5). Widening the clearing is substrate (R1,
R3, R4).

*Why stopping the raising is insufficient alone.* It reaches no row that already
exists. It cannot be enforced without a classifier, and a classifier is refused
at Q5. And it fails exactly where the failure hurts most: the agent that raises
one of these is not being careless, it is being careful, and careful agents will
keep raising while the lawful alternative does not exist. Guidance that tells an
agent not to ask, without giving it a way to proceed, converts a decision
request into a stall.

*Why widening the clearing is insufficient alone.* It makes the rows cheap to
remove but leaves them free to create. The measured raise rate of 30 to 69 per
day is the load, and a clearing path does not reduce a raise rate. Worse, a
cheap clearing path with no guidance about when to raise actively invites more
raising, because raising becomes consequence-free.

The order matters and the guidance depends on the substrate change: R5's
paragraph is only true once R1 exists, because the path it names is the path R1
creates. Ship R1, R3, R4 first, then R5.

### Q2. Who may clear one, and what structurally prevents that principal from ruling a decision that is genuinely the owner's?

**Who: the subject card's opener (R1), plus the raiser as today, plus the
substrate on raiser retirement (R3, R4). A request with no subject card keeps
raiser-and-owner authority only (R2).**

**What prevents it from becoming a ruling, structurally, in three layers:**

*First, a different act.* The widened verb is retraction, not ruling. It writes
`status = 'withdrawn'` and no decision. There is no option selection anywhere in
its path.

*Second, unrepresentable rather than forbidden.* The storage constraint refuses
any `ruled` row whose `ruledBy` is not the owner user, and refuses a decision on
any row that is not `ruled`. An opener that retracts cannot produce a row shaped
like an answer, whatever it intends. This is I3, and it exists today; this
document does not create it and does not touch it.

*Third, and most important: retraction is not a route to the outcome.* This is
I2. An agent that wanted a genuine owner decision to go its way gains nothing by
retracting the question, because retraction authorizes nothing. The work stays
ungated-by-nothing and unauthorized-by-anything; the agent has removed its own
request and must raise again to get an answer. The dangerous half of this
question is dangerous only if the widened path can be used to GET a decision.
It cannot. It can only be used to STOP ASKING for one.

The residual risk is honest and bounded: an opener may retract a question that
was genuinely the owner's, and the owner then never sees it. The row survives as
`withdrawn`, naming the retracting session and its stated reason (I4), the
underlying work still cannot lawfully proceed, and whoever picks the work up
must raise again with a living raiser. The cost of that mistake is a delay and
an attributable record. The cost of the current design is measured above: 494
rulings and a hand-clearing session.

There is one open question attached to this answer, and it is BLOCKING for one
requirement that this document deliberately does not yet state. See OQ-1.

### Q3. What happens to a request whose raiser has retired?

**Generally: the substrate retracts it, because retirement already claims to do
exactly that and the code contradicts its own comment.** R3 deletes the
exclusion. R4 makes the clearing reachable for raisers that retired before the
fix ships.

**For the four that already existed:** they are gone, and the way they went is
the evidence for this document rather than a problem it must solve. On
2026-09-04 at 19:00 UTC the owner ruled all four in person: `dr_8d3ea46f`
`authorize-successor`, `dr_fa2e0f91` `main-only`, `dr_0cdc5e80`
`keep-open-with-liveness-exemption`, `dr_112e519e` `accept-explicit-synthetic`.
Their raisers `s_38b44b0b`, `s_72fd7b84`, and `s_ffeef545` had retired days
earlier, and three of the four asked about work that had already completed by the
time they were answered.

So the honest answer to "answer it for the four that already exist, not only for
future ones" is: **the four cost the owner a hand-clearing session that R3 and R4
would have prevented, and as of this writing no stranded row remains.** The open
operator set is three, all with living raisers. R4 is therefore prophylactic
today rather than remedial, and the specification says so plainly instead of
claiming a cleanup it will not perform.

The subtraction test, applied to R3 and R4:

- *Delete the surface instead?* Deleting the operator request arm would take
  `dr_24edf371` with it. The owner must keep every genuine product decision;
  that is I1. Deletion loses.
- *Accept the failure as a named value instead?* Accepting means the org keeps a
  class of row that only a human can clear, which is the manufactured paperwork
  named in the authority. Accepting the defect the card exists to remove is not
  a design. Acceptance loses.
- *Add?* R3 is a deletion of a filter clause and R4 is a change of trigger key.
  What is added is nothing; what is removed is an exclusion that contradicted
  its own documentation.

### Q4. Does a landed and independently reviewed card close on evidence already on the record, or does it need a new receipt kind?

**It closes on evidence already on the record. No new receipt kind. No change to
`completion-requires-review`.**

The rail's fact already reads evidence rather than liveness. It selects review
rounds by `reviewsAssignmentId` with **no filter on the review card's state**,
picks the round carrying the most recent holder-filed verdict row, and reads the
kind off that same row. Its own documentation states the principle: verdict rows
beat lifecycle rows. A `reviewed-clean` verdict filed by its holder on a review
card that is now closed, or revoked, still qualifies its parent for completion
today. The independence guard is untouched by that: a self-held round still
disqualifies, so a holder cannot launder its own verdict.

This was the load-bearing thing to check before specifying anything here, and
checking it removed a requirement rather than adding one.

**The residual case, named precisely so it is not mistaken for the above.** The
wedge in `dr_8d3ea46f` was not the rail. The review had happened, but its verdict
was never written as a row, because `attest` refuses a verdict from any principal
but the card's holder and on any card that is not open, and the review card
`asg_86d4081b` was revoked before the verdict was filed. Evidence that was never
recorded is not evidence that the rail is failing to read. No receipt kind can
conjure it, and this document specifies none.

The lawful repair for that case exists and needs no change: open a fresh review
round against the same parent, held by a living independent reviewer, and let it
file its verdict. The parent card in that very case, `asg_963d6e43`, went on to
close completed after four rounds, three revoked and one completed. The path
works.

One dead end adjacent to this is named in Open Questions (OQ-2) and deliberately
not specified.

### Q5. How does a lane distinguish rail friction from a real owner decision at the moment it is about to raise one?

**It cannot be made mechanically, the substrate must not attempt it, and this
document designs for the honest case instead.**

The distinguishing property is the SUBJECT MATTER of the question: whether the
answer changes the product. That is a judgment about meaning. The substrate
records truth, routes, and executes named law; it never judges. A classifier
here would be a deterministic rule standing in for a mind, and a wrong
deterministic rule is wrong identically and silently in every case it touches,
which is what brittleness is. A misclassifier's failure mode is the one thing I1
forbids: a genuine product question mechanically labelled bookkeeping and cleared
without the owner ever seeing it.

So the design does three things instead of classifying, and no fourth thing.

*It puts the judgment where a mind already is.* The lane classifies, because the
lane is a mind and it is the mind holding the facts. R5's guidance tells it what
the classes mean and what the lawful alternatives are.

*It makes the cheap path cheap.* The measured evidence says most of these are not
classification failures at all. Of the eight requests open when this was drafted,
three were rail friction and four were agents asking permission for bounded,
in-scope engineering acts that the owner's own standing law already answered. A
lane that asks permission it already has has not misclassified its question; it
has doubted its authority. R1 gives it a real alternative — take the opener's
adjudication and retract — which is precisely what nine living raisers did on
2026-09-04, citing the recovery owner's adjudication artifact in their withdrawal
reasons. That pattern is already the org's practice. Today it stops working the
moment the raiser retires. R1 and R3 make it survive that.

*It makes every classification attributable.* I4: the retraction row names the
session and its stated reason. A lane that clears something it should not have
cleared is identifiable from the record, without any machine having been right
first.

## Acceptance

Each check is decidable from the record by a reviewer who was not present.

**AC-1 (R1, positive).** GIVEN an open operator decision request whose
`assignmentId` names a card opened by session S, and whose raiser is a different
session, WHEN S calls `operator-withdraw` on it with a reason, THEN the call
succeeds, the row reads `status = 'withdrawn'` with `withdrawnBy` naming S and
the given `withdrawnReason`, and `decision`, `ruledBy`, `ruledAt`, and
`rulingFactId` are all NULL.

**AC-2 (R1, negative).** GIVEN the same request, WHEN a session that is neither
the raiser, nor the subject card's opener, nor the owner user calls
`operator-withdraw`, THEN the call is refused and the row is unchanged.

**AC-3 (R2).** GIVEN an open operator decision request with a NULL
`assignmentId`, WHEN any session other than its raiser calls
`operator-withdraw`, THEN the call is refused and the row is unchanged.

**AC-4 (I1, I3).** GIVEN an open operator decision request, WHEN any principal
other than the owner user attempts to rule it by any route, THEN no row exists
afterwards with `status = 'ruled'` attributable to that principal. This check
must be written so that it fails if the ruling authorization is ever widened.

**AC-5 (R3).** GIVEN a session holding one open `operator` request and one open
request of another kind, WHEN that session retires, THEN both rows read
`status = 'withdrawn'` with the retirement sentinel as `withdrawnReason` and no
decision on either.

**AC-6 (R4).** GIVEN an open `operator` request whose raiser session is ALREADY
in the retired state before the mechanism runs, WHEN the mechanism runs, THEN
that row reads `status = 'withdrawn'` with the retirement sentinel.

**AC-7 (R4, idempotence).** GIVEN a request already `ruled`, `withdrawn`, or
`superseded` whose raiser is retired, WHEN the mechanism runs, THEN the row is
byte-identical to before and no second lifecycle record is written.

**AC-8 (Q4, no regression).** GIVEN a producing card with exactly one
`--reviews`-linked review card held by a different session, that review card
carrying a holder-filed `reviewed-clean` verdict, and that review card being in
the closed state with outcome `revoked`, WHEN the producing card's holder
attests completion, THEN the completion is not denied by
`completion-requires-review`. This encodes today's behaviour; it must stay
green, and it is here because a reader of this document might otherwise think
Q4 asked for a change.

**AC-9 (Q4, boundary preserved).** GIVEN the same shape but where the only
`reviewed-clean` verdict on the linked review card was filed by a session equal
to the producing card's holder, WHEN that holder attests completion, THEN
`completion-requires-review` still denies it.

## Open Questions

**OQ-1. BLOCKING, for one requirement this document does not state.**
Whether hardening the operator RULING path is in scope for this work item.

While verifying I1 against the source, the ruling authorization was found not to
hold as written on either the mainline or the released line: the owner-user
principal that `operator-rule` requires is obtainable through the ordinary
identity flag, and the proxy carve-out beside that check reads a field nothing in
the shipped code ever sets. The `decision_requests` row would be indistinguishable
from an owner ruling; the `events` row would not, because it records the calling
session key.

Measured state as of 2026-09-04: unexercised. All 493 successful operator
rulings in the preceding 30 days carry the owner principal with a NULL session
key, that is, the owner's own CLI. All 140 refusals in the preceding 14 days are
likewise from the owner's CLI. No agent session has attempted it. It was not
executed against the live org during this specification's verification and must
not be.

Why it is BLOCKING and why it blocks nothing else: I1 is the invariant this
document promises, and a promise resting on an unenforced guard is a promise
this document cannot make honestly. But the retraction widening in R1 through R4
does not depend on it. Retraction records no decision, so widening it neither
uses nor worsens the ruling path. **R1 through R5 may be built now.** What is
blocked is only the additional requirement that would state the ruling guard
precisely, which is not written here because writing it without a ruling would
be this document deciding its own scope. The owner, or the recovery owner under
the owner's standing laws, rules whether that requirement belongs on this work
item or its own.

Detail beyond what is written here is deliberately withheld from this file. The
spec commons is a public repository. The full finding is recorded on
`asg_d893bbf9` as `att_63956e2b` and in the wake to the recovery owner.

**OQ-2. NON-BLOCKING. Deliberately not specified; do not build it.**
`reopen-assignment` requires the card's holder session to be active. When a card
must be reopened to receive a record of work that genuinely happened, and its
holder has since retired, there is no lawful agent-reachable repair. That is a
gap against the project's own philosophy gate, which requires every state to have
a lawful agent-reachable repair verb.

It is out of scope here. This document's authority names two mechanisms, and this
is a third. The repair for the case that surfaced it — open a fresh review round —
works today, as Q4 records. Anyone building from this document must not read this
paragraph as permission to change reopening. It is written down so it is not
rediscovered as new.

**OQ-3. NON-BLOCKING.** Rail refusals are recorded only in the general event
log, with no per-rule denial record. The counts in this document were extracted
by matching rule names in event payload text, which is sufficient for the window
measured and is not a durable measurement surface. Building one is a Non-Goal.
If the owner later wants standing measurement of rail friction, it is its own
work item.

**OQ-4. NON-BLOCKING.** Whether R5's guidance paragraph should later be promoted
up the escalation ladder is not decided here, and this document's position is
that it should not be promoted on the evidence available. A rail on the raise
side would require the classifier that Q5 refuses. Revisit only if measurement
shows the guidance failing, which requires OQ-3 first.

## Sequencing note

R1, R3, and R4 are independent of each other in effect but touch the same
subsystem; order them rather than running them in parallel. R5 lands after R1,
because the path its guidance names does not exist until then.

Nothing in this document is applied to a running host by the work it specifies.
The production host is locked at 0.1.8 under Mike's 2026-09-02 change law, and
any deployment of this change is a separate act requiring that law's two-step
ceremony.
