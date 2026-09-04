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

Two things, matching the two mechanisms in the authority.

**One.** A card that is landed and independently reviewed files its terminal
receipt, because the completion rail reads the review evidence already on the
record instead of discarding it. The rail is not exempted, weakened, or bypassed;
its predicate is corrected so that it is silent when satisfied.

**Two.** An owner-facing decision request that exists only because an agent could
not finish its bookkeeping is clearable by an agent, without an owner ruling, and
without giving any agent the power to decide a question that is genuinely the
owner's.

That is the whole goal. Above everything in it stands I1: nothing here lets an
agent rule a decision that is genuinely the owner's.

Three measured facts set its size.

**The false refusal rate.** Over the thirty days to 2026-09-04
`completion-requires-review` refused 8 cards that carried an independent
holder-filed `reviewed-clean` on the record at the moment it refused them. The
measurement and the two distinct causes are at R6.

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
   authorization predicate changes, one query filter is deleted, one trigger key
   moves, and one rail fact stops discarding rows. Nothing else.
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
6. **No exemption, override, escape hatch, or claim on any completion rail.**
   This document corrects ONE predicate, in one named way, at R6. It creates no
   exemption flag, no override verb, no "already landed" assertion, no bypass
   principal, and no trusted claim an agent can make to skip a rail. The
   corrected predicate reads the same evidence rows the current one reads and
   admits no row that is not an independent holder-filed `reviewed-clean`.
   `completion-requires-verification`, `completion-requires-results-artifact`,
   and `code-review-requires-passing-tests` keep their `deny_when` clauses
   exactly as written: each is a set-membership test over recorded evidence
   (`SELECT DISTINCT` over the assignment's verdicts, the holder's noted
   verdicts, and the holder's recorded artifact kinds, verified in source), so
   none of them can fire on evidence that exists. Only
   `completion-requires-review` collapses history to a "latest", and that
   collapse is the defect R6 repairs.
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

**Review card.** An assignment whose `reviewsAssignmentId` names another
assignment. That other assignment is its **producing card**.

**Review-conclusion verdict.** A holder-filed verdict on a review card whose
kind is drawn from the closed set {`reviewed-clean`, `changes-requested`}: the
two kinds that state what a review round CONCLUDED about the producing card. The
verdict vocabulary as a whole is open text; this set is not. Holder-filed
verdicts of any other kind observed on review cards in the live data —
`verified`, `merged`, `release-approved`, `tests-passed`, `spirit-approved`,
`spec-reviewed`, `spirit-reviewed`, `no-landing`, `work-blocked`, `pass` — say
something about the reviewer's own card or its own bookkeeping. They are not
conclusions about the reviewed work, and they neither grant nor retract one.

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

**A7.** `attests.verdictKind` is open text. No storage constraint limits it to a
vocabulary, and the live data carries a long tail of one-off kinds. The
review-conclusion set named in Terms is therefore a property of the rail fact's
definition, chosen deliberately here, and never a property an agent sets on a
row. Verified against the live schema and against the distinct holder-filed
verdict kinds observed on review cards, 2026-09-04.

**A8.** `completion-requires-verification` denies a completion by a
coder-archetype holder until a `verified` verdict exists on that holder's own
card, and its remedy wakes the holder to file exactly that. A review card held
by a coder-archetype session must therefore carry a `verified` verdict filed
after its review work in order to close. Verified in source and in the live data;
this assumption is what makes the defect at R6 systematic rather than incidental.

## Invariants

**I1. Nothing specified here lets an agent rule a decision that is genuinely the
owner's. Product choices and trust roots stay with the owner, always.** No agent
may select an option on an operator decision request, by any route, under any
authorization this document creates. This is the invariant the whole document
exists to preserve. Every requirement below is written so that satisfying it
cannot violate this, and where a requirement could be read as bending it, the
requirement is narrowed rather than the invariant. If a future reader finds a
conflict between this invariant and any other sentence in this file, this
invariant wins and the other sentence is the defect.

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

**I6. A rail predicate reads recorded evidence and nothing an agent asserts.**
No requirement here introduces a value an agent supplies in order to satisfy a
rail. Where a predicate is corrected, it is corrected only by reading evidence
rows that already exist and that the current predicate hides from itself. A
bypass is unrepresentable because there is no field to put one in: before R6 and
after it, the only rows that can satisfy `completion-requires-review` are
holder-filed `reviewed-clean` verdicts on `--reviews`-linked cards held by a
session other than the producing card's holder. R6 does not enlarge that set of
row shapes by one. It stops unrelated rows from concealing members of it.

**I7. A correction to a rail may not reduce what the rail refuses.** Every case
`completion-requires-review` denies today, other than the cases R6 names as false
positives, it must still deny after R6. The independence guard, the effect-kind
scope, and the retraction of a clean by a later `changes-requested` are all
preserved exactly. A rail is corrected by making it silent when satisfied, never
by making it quieter when unsatisfied.

## Architecture

The design in one sentence: **correct the one completion predicate that hides
review evidence from itself, widen who may RETRACT an operator request, never
widen who may RULE one, and make session retirement do what its own code comment
already claims it does.**

### R6 — `completion-requires-review` reads the review's conclusion, not the last thing typed

This is mechanism one, and it is a defective predicate, not a rail in need of an
exemption. Wisdom rule 4: a rail is silent when satisfied, and a false positive
is a defective rail. `completion-requires-review` fires on producing cards that
carry an independent, holder-filed `reviewed-clean` on the record. The evidence
is there. The predicate cannot see it.

**The defect, exactly.** The fact `assignment.qualifying_review_verdict_kinds`
does three things, and two of them are wrong:

1. It considers only ONE of a producing card's `--reviews`-linked review cards:
   whichever carries the most recent holder-filed verdict row. **Card collapse.**
2. On that card, it reads the most recent holder-filed verdict OF ANY KIND.
   **Kind collapse.**
3. It qualifies the producing card only if that single kind is `reviewed-clean`
   and the review card's holder is not the producing card's holder. This part is
   correct and is preserved unchanged.

Each collapse hides a `reviewed-clean` that is on the record.

**The corrected predicate.** Across ALL of the producing card's
`--reviews`-linked review cards held by a session other than the producing card's
holder, consider only holder-filed REVIEW-CONCLUSION verdicts as Terms defines
them. Take the single most recent such verdict across that whole set. The
producing card qualifies if and only if that verdict's kind is `reviewed-clean`.

A holder-filed verdict whose kind is outside the review-conclusion set is
ignored by this fact: it neither qualifies a card nor retracts a qualification.
It was never a statement about the reviewed work.

**Kind collapse, measured.** Ten review cards in the live database carry the
holder-filed sequence `reviewed-clean -> verified` as their complete verdict
history: `asg_ae32658f`, `asg_e24c4273`, `asg_463f7907`, `asg_f60f061e`,
`asg_129f8993`, `asg_58bfc8f7`, `asg_9a476205`, `asg_0b1ea9e1`, `asg_187df922`,
`asg_a6f74a2b`. Each reviewed independently, each concluded clean, each is
invisible to the rail today.

The org's own paperwork causes it. Nine of those ten review cards are held by
coder-archetype sessions, and each filed exactly one completion.
`completion-requires-verification` denies a coder-archetype holder's completion
until a `verified` verdict sits on that holder's own card, and its remedy wakes
the holder to file precisely that (A8). So the reviewer files `reviewed-clean`,
is then required by a second rail to file `verified` on the same card in order to
close it, and that mandatory second verdict un-reviews the producing card. One
completion rail's remedy manufactures the state in which the other completion
rail false-positives. That is not an unlucky ordering; it is the normal path for
a coder-archetype reviewer.

**Card collapse, measured.** `asg_0bf0dc45` carries four linked review cards.
Three concluded `reviewed-clean` (`asg_2cdabccb`, `asg_3da5b789`, `asg_ec8fb3ac`).
The fourth, `asg_e526fd86`, carries a single `release-approved` and is the most
recent. The rail read the fourth card only, saw a kind that is not
`reviewed-clean`, and denied a card with three independent clean reviews and a
release approval on it.

**The size of this defect, stated honestly.** Over the thirty days to 2026-09-04
`completion-requires-review` denied 1,036 times across 820 distinct cards. Of the
denied cards that had a linked review card carrying any holder-filed verdict, the
rail saw `reviewed-clean` on 263 (the denial preceded the review; this is the
remedy loop working exactly as designed), `changes-requested` on 67 (a true
positive: the review found problems), `verified` on 7, and `release-approved` on
1. All seven of the `verified` cards had a `reviewed-clean` earlier on that same
review card. So the false positives are 8 of 338, about 2.4 percent, and this
document does not claim they explain the bulk of the denials. They do not. They
are the shape that produces the wedge the authority names: a card that IS landed
and IS independently reviewed, refused its terminal receipt.

**Why this is a predicate correction and not a bypass.** I6 and I7 are the
guarantees, and here is why they hold. R6 adds no flag, no claim, no exemption,
no principal, and no verb. The set of row shapes that can satisfy the rail is
byte-for-byte the same before and after: a holder-filed `reviewed-clean` on a
`--reviews`-linked card held by another session. Nothing an agent can file makes
the rail looser. Filing a later `changes-requested` still makes it stricter, and
still does so across cards, so a second round that finds problems still denies
the parent. The review-conclusion set is closed and lives in the fact's
definition; an agent cannot mint a kind into it, and minting a novel verdict kind
buys nothing, because only `reviewed-clean` qualifies.

**Anyone building from this must not** add an exemption path, a "landed" claim, a
skip flag, a trusted-lane carve-out, or any way for an agent to assert that
review happened. Those would be a different design and a worse one: any lane
could claim them, and the rail we need would be hollow. The whole content of R6
is that the fact stops discarding evidence it already has.

**What R6 does not fix, named so it is not assumed.** A review that happened but
was never written as a verdict row is not reached by any predicate. That case is
Q4's residual, and it is the case that actually produced `dr_8d3ea46f`. R6 does
not touch it and does not pretend to.

The subtraction test, applied to R6:

- *Delete the surface instead?* Deleting `completion-requires-review` deletes the
  org's flagship enforced review loop over code, policy, release, and
  live-mutation work. The measured 67 genuine `changes-requested` denials in
  thirty days are the rail earning its place. Deletion loses.
- *Accept the failure as a named value instead?* Accepting means the org keeps a
  rail that refuses reviewed work about eight times a month, each refusal
  landing on the owner's desk as a decision request. That is the manufactured
  paperwork the authority names. Acceptance loses.
- *Add?* Nothing is added. Two collapses are removed from a query. The rule file
  is untouched; `deny_when` keeps the same three clauses and the same fact name.

### The seam (mechanism two)

R6 above is the whole of mechanism one. R1 through R5 below are mechanism two,
and they rest on one seam.

`decision_requests` already separates two acts that a reader might blur. Ruling
writes an answer. Retraction writes an absence. The table's constraint binds an
answer to the owner user and forbids an answer on any other status. So the
retraction path can be widened to agents without any change to the constraint,
and without any new way for an agent's judgment to enter the record as the
owner's.

That is the whole architectural idea of mechanism two. R1 through R5 are its
application.

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

No new verb. No new column. No new table. No new kind. No new rail. No new rule
file entry. No exemption, override, or claim. No migration. R1, R3, R4, and R6
are edits to existing queries and authorization predicates; R5 is prose.

## The five questions

### Q1. Widen who may clear, or stop the raising, or both?

**Both, at three different rungs of the escalation ladder, and no one of them is
sufficient alone.**

Stopping the raising is two things, not one, and the more important of them is
not guidance. Removing the CAUSE of a class of raises is the predicate
correction (R6): a rail that stops false-positiving stops producing the friction
that lanes escalate. Telling lanes not to escalate the friction that remains is
guidance (R5). Widening the clearing is substrate (R1, R3, R4).

*What the clearing evidence says about which half is load-bearing.* Three
raisers, woken with the recovery owner's adjudication, withdrew their own
requests within minutes and recorded the ruling on their own cards. So a
clearing motion already exists and already works. That narrows the gap
precisely: it is not that no lawful clearing act exists, it is that the only
lawful clearing act depends on one specific session being able to run. A raiser
that is retired, out of capacity, or wedged takes the org's only exit with it.
R1 and R3 are therefore not inventing a motion; they are removing that motion's
single point of failure. This narrows what must be built and it raises the bar
on R1: since the motion works when the raiser lives, R1 must justify itself
entirely on the cases where the raiser cannot run, and it does.

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

*Why correcting the predicate is insufficient alone.* R6 removes about eight
false refusals a month. It does not reach a single request already raised, it
does nothing for the friction that comes from a rail firing correctly, and it
leaves the retired-raiser dead end exactly where it is. Fixing a cause never
clears the effects that already happened.

The order matters and the guidance depends on the substrate change: R5's
paragraph is only true once R1 exists, because the path it names is the path R1
creates. Ship R6, R1, R3, R4 first, then R5.

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

**The org already has a name for this state: wisdom rule 14, no intent in limbo
— every filed intent carries an owner and a deadline, so absence is
detectable.** An operator request whose raiser has retired is intent in limbo in
the exact sense the rule means. The intent was filed. Its owner, the raiser, no
longer exists. And the absence is UNDETECTABLE by the substrate, because the
only actor with authority to clear the row is the one actor that is gone. The
row does not expire, does not escalate, and does not surface; it simply sits
open forever until a human notices it and clears it by hand. That is the failure
rule 14 exists to make impossible, and the mechanism meant to prevent it is
already written and already broken.

**Generally: the substrate retracts it, because retirement already claims to do
exactly that and the code contradicts its own comment.** R3 deletes the
exclusion. R4 makes the clearing reachable for raisers that retired before the
fix ships. Between them the absence becomes detectable again, by the substrate,
at the moment the owner of the intent ceases to exist — which is the earliest
moment it can be known.

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

The owner clearing them by hand is not the mechanism working. It is the rule 14
failure being paid for by the one actor the rule exists to protect. Four rows
sat open for days with no lawful agent-reachable exit, and the substrate never
once said so.

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

**It closes on evidence already on the record. No new receipt kind, no new
verdict kind, no new attest kind. What is needed is that the rail READ the
evidence that is already there, which today it does not: R6.**

This question has three distinct answers because the record has three distinct
states, and conflating them is how a builder ends up building a bypass.

**One: lifecycle state is already read correctly, and needs nothing.** The
rail's fact selects review rounds by `reviewsAssignmentId` with **no filter on
the review card's state**. Its own documentation states the principle: verdict
rows beat lifecycle rows. A `reviewed-clean` verdict filed by its holder on a
review card that is now closed, or revoked, still qualifies its parent for
completion today. The independence guard is untouched by that: a self-held round
still disqualifies, so a holder cannot launder its own verdict. This was the
load-bearing thing to check before specifying anything, and checking it removed a
requirement rather than adding one. No change here.

**Two: verdict history is read wrongly, and that is a defective predicate.** The
same fact then collapses that history twice — to one review card, and to that
card's latest verdict of any kind — and each collapse can hide a `reviewed-clean`
that is sitting on the record. A card that is landed and independently reviewed
is refused its terminal receipt. Under wisdom rule 4 that is a false positive and
therefore a defective rail, and the answer is to correct the predicate, never to
grant an exemption from it. R6 states the correction, the measurements behind it,
and the reason a bypass would be the wrong build. **"Prefer what is already
there" is not a preference here. It is the whole fix: the qualifying rows exist,
and the query discards them.**

**Three: a review whose verdict was never written is reached by no predicate.**
The wedge in `dr_8d3ea46f` was neither of the above. The review had happened, but
its verdict was never written as a row, because `attest` refuses a verdict from
any principal but the card's holder and on any card that is not open, and the
review card `asg_86d4081b` was revoked before the verdict was filed. Evidence
that was never recorded is not evidence the rail is failing to read. No receipt
kind can conjure it; R6 does not reach it; this document specifies nothing for
it.

The lawful repair for that third case exists and needs no change: open a fresh
review round against the same parent, held by a living independent reviewer, and
let it file its verdict. The parent card in that very case, `asg_963d6e43`, went
on to close completed after four rounds, three revoked and one completed. The
path works.

One dead end adjacent to the third case is named in Open Questions (OQ-2) and
deliberately not specified.

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

**AC-8 (lifecycle reading, no regression).** GIVEN a producing card with exactly
one `--reviews`-linked review card held by a different session, that review card
carrying a holder-filed `reviewed-clean` verdict, and that review card being in
the closed state with outcome `revoked`, WHEN the producing card's holder attests
completion, THEN the completion is not denied by `completion-requires-review`.
This encodes today's behaviour and must stay green. It is here because a reader
might otherwise think R6 changes how lifecycle state is read. It does not.

**AC-9 (independence guard preserved).** GIVEN the same shape but where the only
`reviewed-clean` verdict on the linked review card was filed by a session equal
to the producing card's holder, WHEN that holder attests completion, THEN
`completion-requires-review` still denies it. This must stay green after R6.

**AC-10 (R6, kind collapse).** GIVEN a producing card with one
`--reviews`-linked review card held by a different session, whose holder-filed
verdict sequence is `reviewed-clean` then `verified`, WHEN the producing card's
holder attests completion, THEN the completion is not denied by
`completion-requires-review`. This check FAILS against the code as it stands on
2026-09-04; it is the defect R6 repairs, and it is drawn from ten real review
cards listed at R6.

**AC-11 (R6, card collapse).** GIVEN a producing card with four
`--reviews`-linked review cards held by sessions other than its holder, three
whose latest review-conclusion verdict is `reviewed-clean` and a fourth, most
recent, whose only holder-filed verdict is `release-approved`, WHEN the producing
card's holder attests completion, THEN the completion is not denied. This check
also FAILS today, and is drawn from `asg_0bf0dc45`.

**AC-12 (I7, retraction across cards still bites).** GIVEN a producing card with
two `--reviews`-linked review cards held by other sessions, the earlier
concluding `reviewed-clean` and the later concluding `changes-requested`, WHEN
the producing card's holder attests completion, THEN
`completion-requires-review` denies it. A later round that found problems must
still refuse the parent, across cards as well as within one.

**AC-13 (I6, no bypass exists to find).** GIVEN a producing card with NO
holder-filed `reviewed-clean` verdict on any `--reviews`-linked card held by
another session, WHEN its holder attests completion after filing verdicts of any
other kinds whatsoever on any cards it holds, including kinds not previously seen
in the vocabulary, THEN `completion-requires-review` denies it. This check must
be written so that it fails if any value an agent supplies is ever made capable
of satisfying the rail.

**AC-14 (R6, scope unchanged).** GIVEN a producing card whose effect kind is
outside `code`, `policy`, `release`, `live_mutation`, WHEN its holder attests
completion with no review at all, THEN the completion is not denied by
`completion-requires-review`, exactly as today. R6 changes one fact's query and
no clause of the rule.

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

Noted for whoever rules on it later: this is the same rule 14 shape as Q3, in a
different subsystem. A card whose holder has retired carries an intent whose
owner no longer exists, and the repair verb refuses because that owner is gone.
Q3's answer does not generalise to it, and this document does not try to
generalise it.

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

R6 is independent of the rest: it touches one fact query in the rules layer and
nothing in the decision request subsystem. It may run in parallel with the
others, and it is the one that removes a cause rather than clearing effects, so
prefer it first.

R1, R3, and R4 are independent of each other in effect but touch the same
subsystem; order them rather than running them in parallel. R5 lands after R1,
because the path its guidance names does not exist until then.

Nothing in this document is applied to a running host by the work it specifies.
The production host is locked at 0.1.8 under Mike's 2026-09-02 change law, and
any deployment of this change is a separate act requiring that law's two-step
ceremony.
