# Owner decision request relief v1

Status: specification for build — Mike written instruction, 2026-09-04
Work item: `wi_3d328d28-4c3c-4405-a624-427426fa10d5`
Posture: HEAVY (`att_4a8e3cc4` on `asg_14e7590c`)
Evidence: `art_02574fb9`, sha256
`83782fe8522c87066d3b9eddb7207c5e8606e5a55e6346c90fdb6c7047e386b8`

Amended 2026-09-05 for review finding B-1 and post-MVP items P-1 through P-5
(`art_141180b0`). The amendment corrects one class of error throughout: the first
draft made per-ref claims against a two-branch model of a repository that has
three branches and a running release whose artifact matches no branch tip. A18 is
new and every per-ref claim below now names its ref. No requirement text changed.
The measured size of R6 changed from 17 to 8, because the 17 describes only a
frozen branch pointer that no host runs and no release ships.

Authority, verbatim (Mike, 2026-09-04):

> ROOT CAUSE, file it as a work item and staff it: the completion rail refuses
> terminal receipts on work that is landed and independently reviewed, and lanes
> respond by raising owner-facing decision requests. That rail is manufacturing
> paperwork for Mike. Fix it so a landed, reviewed card can close without an
> owner ruling.

Scope addition, verbatim (Mike, ruling `dr_778ba73b`, 2026-09-04 21:30 UTC):

> a retired raiser leaves an immortal owner-facing request that no living actor
> can clear. That is worse than the completion rail Mike named, and four of these
> were unclearable by anyone but him, forever. It is staffed as wi_3d328d28 —
> keep it, and make sure the spec covers BOTH the retired-raiser trap and the 37
> effort check-in requests that effort-rule refuses with current expecter
> required.

## Goal

Three things: the two mechanisms in the original authority, and the third named
by the scope addition.

**One.** A card that is landed and independently reviewed files its terminal
receipt, because the completion rail reads the review evidence already on the
record instead of discarding it. The rail is not exempted, weakened, or bypassed;
its predicate is corrected so that it is silent when satisfied.

**Two.** An owner-facing decision request that exists only because an agent could
not finish its bookkeeping is clearable by an agent, without an owner ruling, and
without giving any agent the power to decide a question that is genuinely the
owner's.

**Three.** An effort check-in that has a lawful agent answerer is answerable by
that agent, instead of by whichever single rung of the chain the clock has
reached. The check-in itself is untouched: same probe, same question, same
deadline, same escalation. Only the refusal of parties the substrate itself
already selected is removed, and the holder stays refused.

That is the whole goal. Above everything in it stands I1: nothing here lets an
agent rule a decision that is genuinely the owner's.

Four measured facts set its size, and the fourth corrects the scope addition's
own count.

**The false refusal rate.** Over the thirty days to 2026-09-04
`completion-requires-review` refused 821 distinct cards in 1037 denials. Of those,
**8** carried, at the moment of
refusal, a holder-filed review conclusion from a session other than the card's own
holder — a conclusion the fact discards. That 8 is the figure on `main`, on
`0.1.9`, and on the release gibson runs, which share one card-selection rule; a
larger figure of 17 belongs only to the frozen `0.1.8` pointer, which no host runs
and no release ships (A18, A6). R6 repairs exactly those and turns none
of the others from allowed to denied. The measurement, both selection rules, and
the three distinct causes are at R6.

**The raise rate.** Over the fourteen days to 2026-09-04 the org raised between 11
and 73 operator decision requests per day, 617 in total. All-time, 502 operator
requests carry a ruling, and every one of those rulings carries a `user:mike`
origin. Measured 2026-09-04 against `decision_requests` where `kind = 'operator'`,
counting raises by `createdAt` bucketed to UTC days and rulings by
`status = 'ruled'`. Read that 502 as A12 requires: `ruledBy` records attribution,
not the authorizing principal, so it counts rows the owner is recorded against,
not keystrokes proven to be his.

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

**The effort channel, measured rather than assumed.** The scope addition counts
37 effort check-in requests that `effort-rule` refuses. All 37 are open and all
37 are refused to some caller, but they are not one population and a predicate
change does not reach most of them. Of the 37: **23** carry an active session
expecter and are the rail working as designed, because the caller they refuse is
the holder, and the holder is the party the check-in is about; **3** have an
agent lineage and are the cases a predicate correction repairs; **11** reach the
owner because the card's lineage contains no agent at all, so there is no one
for any authorization change to admit. R7 fixes the 3. The 11 are OQ-5, which is
not an authorization question. The full derivation is at A10 and A11.

The scope addition's phrase "even to the card's own holder" describes the 23,
and refusing them is correct. This is recorded here rather than quietly built
around, because a builder reading the addition without this paragraph would
widen the predicate until the holder could dismiss its own check-in, which is
the current defect on BOTH `main` and `0.1.9` (R7, A9).

## Non-Goals

Named as deliberately as the goal, because each is a thing a reader could
mistake this document for permission to build.

1. **Not a redesign of decision requests.** The `statute`, `effort`, and
   `operator` arms keep their current shapes, kinds, and lifecycles. Two
   authorization predicates change, the same one-clause query filter is deleted
   in two places, one rail fact stops discarding rows, and that rail's `text`
   string is corrected to describe itself truthfully afterwards (R6). Nothing
   else. In particular no new sweep and no new trigger of any kind is built; R4
   reuses a sweep and a trigger that already exist (A13). The full fence and its
   reason live at R4 under "Build no sweep" and are not restated here, so that
   the list a builder is held to has one home.
2. **No new notification surface, dashboard, digest, or queue view.** Nothing in
   this document displays decision requests to anyone.
3. **No new receipt kind, verdict kind, attest kind, or decision request kind.**
   Section "Q4" establishes that the existing rows already carry what is needed.
4. **No classifier.** Nothing here decides, by machine, whether a question is
   bookkeeping or a real owner decision. Section "Q5" explains why that is a
   refusal rather than an omission.
5. **Not a widening of who may RULE an operator request.** Ruling authority is
   unchanged by every requirement in this document. Whether it should separately
   be TIGHTENED is an open question (OQ-1) that this document does not answer and
   does not authorize anyone to answer by building; nothing here may be read as
   an instruction to change `operator-rule`. Separately, R7 does not widen who may answer an effort
   check-in beyond the lineage the substrate itself already walks, and it admits
   no principal the substrate has not already selected as an expecter at some
   rung.
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
8. **Not a change to effort check-in escalation.** The probe, the four effect
   channels, the zero-effect verdict, the 24-hour deadline, the rung advance,
   the notification, and the ordinary-power menu are all untouched. R7 changes
   who may answer the question. It changes nothing about when the question is
   asked, of whom it is asked, what the options are, or what it costs to ignore
   it. A builder who finds itself editing `advance_expecter`, `deadline_in_txn`,
   `initial_expecter`, `menu_in_txn`, or the channel counters has left this
   document's scope. Calling those functions to enumerate the escalation lineage
   is reading, not editing, and R7 permits it explicitly; what this non-goal
   forbids is changing what any of them returns.

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
verdict vocabulary as a whole is open text; this set is closed, and it is closed
because the rail fact's definition names it, never because storage constrains it
(A7). Holder-filed
verdicts of any other kind observed on review cards in the live data —
`verified`, `merged`, `release-approved`, `tests-passed`, `spirit-approved`,
`spec-reviewed`, `spirit-reviewed`, `no-landing`, `work-blocked`, `pass` — say
something about the reviewer's own card or its own bookkeeping. They are not
conclusions about the reviewed work, and they neither grant nor retract one.

**Effort check-in request.** A row in `decision_requests` with `kind = 'effort'`.
The substrate raises one when it armed a liveness generation on an assignment,
probed the four effect channels, and observed no effect. Its question is whether
the holder's silence should be tolerated (`continue`) or acted on (`dismiss`).
It is a supervision question about a session, never a product question.

**Expecter.** The single principal a `kind = 'effort'` row currently addresses,
held in `expecterSessionKey` or `expecterUserId`, with `lineageRung` recording
how far up the chain it has walked. Exactly one of the two columns is set.

**Escalation lineage.** The chain `route_session/5` walks for an assignment: it
starts at the card's opener session, or at the holder's parent when the opener
is the holder, and follows `spawnedBy` upward, skipping the assignment's holder
at every step and skipping sessions that are not active. It ends at the owner
user when the chain runs out. Every session in this chain is a principal the
substrate has already selected as an expecter at some rung, or would select at a
later one. The lineage is a property of the assignment, computable at any time;
the expecter is one member of it, selected by the clock.

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

**A18. The four code refs this document reads.**

| Ref | What it is | Commit, as of 2026-09-05 |
|---|---|---|
| `main` | the mainline | — |
| `0.1.9` | the active 0.1 maintenance branch; release tags are cut from here | `8bcc242b`, 2026-09-05 |
| `0.1.8` | a FROZEN branch pointer, 85 commits behind `0.1.9` | `2ff4ed2a`, 2026-08-22 |
| `v0.1.8+1337` | the release gibson runs today | `fdb3db5`, 2026-08-22 |

Ancestry, verified 2026-09-05: `0.1.8` < `v0.1.8+1337` < `7090a630` < `0.1.9`,
all one line, so the running release is a tag sitting three commits ahead of the
frozen `0.1.8` pointer and is not the tip of any branch.

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

A qualification on the denial counts at R6, now measured rather than hedged.
Reproducing what the rail SAW at each denial requires replicating the fact's
card-selection rule in SQL, and TWO such rules exist in the repository. The
VERDICT-RECENCY rule collapses to the review card carrying the most recent
holder-filed verdict, computed in one join. The `openedAt` rule collapses to the
most recently OPENED review card and reads verdicts inside it. Both were run over
the same 30-day window; the results are at R6.

Which ref carries which is the correction that matters, and an earlier draft of
this document got it wrong. `main`, `0.1.9`, AND the release gibson runs
(`v0.1.8+1337`) all carry the VERDICT-RECENCY rule; the function body is
byte-identical between `0.1.9` and the running release, verified 2026-09-05. The
`openedAt` rule survives on the frozen `0.1.8` pointer alone
(`assignments.ex:315`), which no host runs and no release ships. Commit
`8765c22e`, "Fix holder verdict selection on 0.1.8", replaced it on the 0.1.x
line before the release gibson runs was cut.

What does not move is the false refusal count this document is sized by: **8
under both rules**, because the cards it names are cards whose winning verdict is
a review conclusion the fact's kind list omits, and both rules select the same
winner on all 8. What moves is the size of the correctly-denied population around
them, and the count of cards the `openedAt` rule additionally loses. That larger
count, 17, is therefore a fact about the frozen pointer ONLY. **A builder
targeting `main`, `0.1.9`, or the running release should expect 8, not 17.**

Neither the defect nor the requirement moves. R6's requirement text holds against
both rules, because both collapse and R6 removes the collapse.

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

**A9.** `effort-rule --request <dr> --action continue|dismiss` authorizes a
session principal by one of two clauses, and WHICH ONE is a per-ref fact (A18).

The NARROW clause requires exact identity with the row's current expecter:
`authorized?({:session, key}, request), do: request.expecter_session_key == key`.
It is at `lib/tightbeam/effort_checkin.ex:1269` on the frozen `0.1.8` pointer and
at the same address in the release gibson runs, `v0.1.8+1337`; the two files are
byte-identical.

The WIDE clause admits every session unconditionally:
`authorized?({:session, _key}, _request), do: true`. It is on **both** `main`
(`lib/tightbeam/effort_checkin.ex:1390`, introduced by commit `e02cab00`, "Add
targetless decision request responders", 2026-08-27 00:00 UTC) and **`0.1.9`**
(`lib/tightbeam/effort_checkin.ex:1425`, introduced by commit `7090a630`, "Adapt
decision expecter preference to 0.1.9", 2026-08-27 07:29 UTC).

`7090a630` is contained in no release tag. That is why the release gibson runs
still carries the NARROW clause while the branch that ships next carries the
WIDE one. A reader who checks only the running host will not see the defect R7's
"must not become any session" paragraph guards against.

The user clause is identical on all four refs. Nothing else in any ref's `rule/3`
guards the caller. Verified in source on all four refs, 2026-09-05.

**A10.** On 2026-09-04 the org held 37 open `kind = 'effort'` requests. 23 carry
a session expecter, and every one of those expecter sessions is in the active
state. 14 carry a user expecter with a NULL session expecter. Verified against
the live database, read only.

**A11.** Of the 14 at a user expecter: 11 are on cards the owner opened himself
(`openedByUser` non-NULL), and every one of those cards is held by a session
with no active ancestor by `spawnedBy`, so the card's lineage contains no agent
at any rung; 2 are on cards whose opener session is retired and has no parent;
1 is on a card whose opener session is active and is not the current expecter.
Their ages run from 0.1 to 7.8 days and every one carries a deadline on
2026-09-05, which is the 24-hour re-arm described at OQ-5. Verified against the
live database, read only.

**A12.** `decision_requests.ruledBy` records the call's attributed origin, not
its authorizing principal. A session call carrying `--as-user <id>` records
`user:<id>` while being authorized as the session. Of the 918 effort rulings
attributed to `user:mike` in the 14 days to 2026-09-04, 540 are on requests whose
expecter was a session, which the user clause of `authorized?` cannot authorize;
those calls were therefore authorized as the expecter session and merely
attributed to the owner. No count in this document claims to measure the owner's
own keystrokes in this channel. The upper bound on rulings that required a user
principal is the 378 whose expecter was a user, and even that is an upper bound
rather than a count, because the identity flag is available to an agent.

**A13.** The state-keyed retired-raiser sweep that R4 requires ALREADY EXISTS.
`Escalation.recover_retired/1` selects sessions in the retired state that still
have open decision requests, and calls `withdraw_for_retired/2` on each. It is
documented as the boot backstop for retirement casts lost across a crash, and
`boot.ex` calls it on every gateway boot. Its candidate query carries the SAME
`kind != 'operator'` exclusion as `withdraw_for_retired/2` itself. So the sweep,
its state key, and its trigger are all built; only the exclusion stops it
working. Verified in source on all four refs, 2026-09-05: the routine is at
`escalation.ex:1625` on `main`, `:819` on `0.1.9`, and `:654` on both the `0.1.8`
pointer and the running release; the boot call is at `boot.ex:53` on `main` and
`boot.ex:32` on the other three. This
assumption is what collapses R4 from a mechanism to a deletion.

**A14. `main` only.** On `main` `withdraw_for_retired/2` carries a SECOND
filter beside the kind exclusion: it rejects any request whose `context.verb` is
`cannot-proceed` (`escalation.ex:1476`, applied at `:1509`), with the stated
reason that retirement is neither an exact assignment disposition nor an exact
release fact. That carve-out is deliberate and is not a defect. No row in the live
database sets `context.verb` at all — all 6,563 rows across both live kinds read
NULL — so it fires on nothing today, and deleting the kind exclusion does reach
operator rows.

**Neither `0.1.9` nor `0.1.8` has such a filter.** On both, and therefore in the
running release too, `withdraw_for_retired/2` selects `id` alone and decodes no
context (the row query is at `escalation.ex:704` on `0.1.9` and `:539` on the
`0.1.8` pointer and the running release, against `SELECT id,context` at `:1505`
on `main`). The typed cannot-proceed request does not exist on either ref at all:
the strings `cannot-proceed` and `cannot_proceed` appear nowhere in
`escalation.ex` on `0.1.9` or `0.1.8`, verified 2026-09-05. R3's instruction to
preserve the carve-out is therefore a no-op on those refs, and it is NOT
an instruction to port the carve-out there. Verified in source on all four refs
and against the live database, read only. A14's split is why R3 and R4 appear in
OQ-6's ref election.

**A15.** Nothing outside the decision request subsystem gates on a request being
open. No rail fact reads `decision_requests`: the fact list in
`lib/tightbeam/rules.ex` contains no decision-request fact. The only consumer of
the open set elsewhere in the tree is a count summed into the execution map
projection, which displays and authorizes nothing:
`open_decision_requests/2` at `lib/tightbeam/execution_map.ex:518` on `main` and
`:429` on `0.1.9`, on the `0.1.8` pointer, and in the running release, fed by one
`SELECT ... GROUP BY assignmentId` over open rows. The function body is
character-identical on all four refs; only the address differs, and
`execution_map.ex` is byte-identical across the three non-`main` refs. Verified in
source on all four refs, 2026-09-05.
This assumption is what makes I2 a checked claim rather than an assertion.

**A16.** Operator request populations by the opener of their subject card, over
all 630 rows in the live database: 349 have an opener session in the active
state, 127 have an opener session that is now retired, 106 are on cards the owner
opened himself, and 48 have no subject card. Opener state is measured now, not as
of the moment each request was open, so the 127 measures how often an opener has
since retired rather than a count of retractions that would have failed.
Verified against the live database, read only.

**A17.** The `sessions` table carries exactly two states in the live database:
`active` (407 rows) and `retired` (2,712 rows). Measured 2026-09-04, read only.
R7's active-session condition is therefore inert against today's data — every
lineage member that can make a call is already `active` — and a build that omits
the condition passes every test the live corpus can produce. This assumption is
why AC-23 is written against the predicate rather than against the corpus. If a
third state is ever added, the condition stops being inert and R7's requirement
sentence is already correct for it; nothing in this document needs amending.

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

**I2. Retraction removes a question, never a gate.** Retracting a request
authorizes nothing. If the retracted question was genuinely the owner's, the work
it gated is still not authorized to proceed, and the agent that retracted has
gained nothing by retracting. This is what makes widening retraction safe where
widening ruling would not be. An agent that retracts a real owner question has
not stolen a decision; it has only lost its own place in the queue, and must
raise again.

This is a checked claim, not a hopeful one, and it is checked in the only way
that would falsify it: by asking what else in the substrate reads the open set.
If the EXISTENCE of an open operator request gated anything, then retracting one
would remove that gate, and every widening below would be a bypass wearing a
different verb. It gates nothing. No rail fact reads `decision_requests` at all,
and the single consumer of the open set outside the request subsystem is a count
in a projection that displays and authorizes nothing (A15). Retraction therefore
changes what a viewer sees and what nobody may do. A future change that makes an
open request gate anything breaks this invariant and must revisit R1 through R4
before it lands.

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

**I7. A correction to a rail may not reduce what the rail refuses.** A rail is
corrected by making it silent when satisfied, never by making it quieter when
unsatisfied.

Stated so that it can be decided rather than argued: exactly one class of case
may change from denied to allowed, and it is defined by the corrected predicate
itself, not by the two causes R6 narrates. A case may change if and only if the
most recent holder-filed review-conclusion verdict across all of the producing
card's linked review cards is `reviewed-clean` and sits on a card held by another
session. Every other case the rail denies today it must still deny. "R6 names it
as a false positive" is not a licence a builder may extend; the sentence above is
the whole of the exception, and anything else that stops denying is a regression
however well it is argued.

Three consequences are worth naming because each is a place a plausible
implementation would drift: the effect-kind scope is untouched (AC-14); a later
`changes-requested` still retracts an earlier clean, across cards as well as
within one (AC-12); and a self-held latest round still disqualifies past an
earlier independent clean (AC-20), which is the third collapse R6 deliberately
keeps.

**I8. A holder never answers its own effort check-in.** The check-in asks
whether the holder produced effect. Admitting the holder as an answerer destroys
the only property the mechanism has, and it is the one widening that would turn
a liveness prod into a formality. No requirement here admits the holder by any
route. The lineage walk already excludes it, and AC-16 is written to fail if any
change ever admits it.

The reason widening who may answer an effort check-in does not touch I1 is worth
stating rather than assuming: an effort check-in is a supervision act about
whether a session is working, not a product choice, a scope call, a release
intent, or a trust root. It is `kind = 'effort'`, not `kind = 'operator'`, and
the two arms are separate rows with separate verbs and separate authorization.
I1 governs `operator` requests, and nothing in R7 reaches them. If a future
reader finds an effort check-in whose real content is a product decision, the
defect is that it was raised as an effort row, and the repair is upstream of
this document.

That separation is mechanical, not conventional, and a builder should verify it
before trusting this paragraph. The `effort-rule` entry point refuses any request
whose `kind` is not `effort` before it consults `authorized?/2` at all, so the
predicate R7 changes is unreachable from an `operator` row. Verified on all four
refs in A18 (2026-09-05): the refusal and the `authorized?/2` call are clauses of
one `cond` in `rule/3`, in that order, at `effort_checkin.ex:409`/`:406` on
`main`, `:375`/`:372` on `0.1.9`, and `:336` on the `0.1.8` pointer and the
running release. `main` and `0.1.9` place an additional visibility clause AHEAD
of the kind refusal, which masks a non-effort request as not-found; that makes
the gate stricter, not weaker, and does not change this conclusion. R7
widens a clause of a function that operator requests never call. A build that
moves the kind check, or that reuses the widened predicate on the operator path,
breaks I1 — which is the one invariant this document forbids trading against
anything.

## Architecture

The design in one sentence: **correct the one completion predicate that hides
review evidence from itself, widen who may RETRACT an operator request, never
widen who may RULE one, admit the whole escalation lineage the substrate already
walks to answer an effort check-in while still refusing the holder, and make
session retirement do what its own code comment already claims it does.**

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

**The corrected predicate.** Consider every holder-filed REVIEW-CONCLUSION
verdict, as Terms defines that set (A7), on every one of the producing card's
`--reviews`-linked review cards. Order that pool by the verdict row's own recency
— `ts` descending then `rowid` descending, so that two verdicts filed in the same
millisecond still have exactly one winner. Every ref already orders VERDICTS this
way inside the fact; what R6 changes is that this ordering now decides the winner
outright, rather than being applied inside a review card that a separate rule
picked first. On the frozen `0.1.8` pointer that separate rule is `openedAt`
descending, and a builder targeting that ref must not read "the order the fact
already uses" as licence to keep `openedAt` anywhere in the corrected predicate.
On `main`, on `0.1.9`, and in the running release the separate rule is verdict
recency instead (A6), and `openedAt` does not appear in the fact at all.
Take the single most recent verdict in the pool. The producing card qualifies if
and only if that verdict's kind is `reviewed-clean` AND the card it sits on is
held by a session other than the producing card's holder.

Read in that order, and only in that order. The independence test applies to the
winning verdict, exactly where it applies today; it is NOT a filter that removes
self-held cards from the pool before the winner is chosen. The difference is not
cosmetic and it is the subject of the preserved behaviour named below.

A holder-filed verdict whose kind is outside the review-conclusion set is
ignored by this fact: it neither qualifies a card nor retracts a qualification.
It was never a statement about the reviewed work. If the pool is empty — no
linked review card carries any holder-filed review-conclusion verdict at all, as
when every one of them carries only `verified` — then there is no winner, the
fact yields nothing, and the rail denies exactly as it does today.

**The fact's return contract does not change.** Today
`assignment.qualifying_review_verdict_kinds` returns either the single-element
list `["reviewed-clean"]` or the empty list, and the rule tests it with
`not_in ["reviewed-clean"]`. After R6 it returns the same two values, under the
corrected reading. A builder who changes the fact to return the winning kind
whatever it is, or a boolean, has changed the rule's contract and will find
itself editing `deny_when`, which Non-Goal 6 forbids.

**One computation, not two.** The winning verdict and the holder it is tested
against must be read from the same row. The fact already works this way
deliberately, because reopening lets one review card carry several verdicts over
its life, so "which verdict wins" and "whose card is it on" cannot be two
separately-derived answers that have to agree by luck. Pooling across cards makes
that temptation stronger, not weaker: a builder who computes the winning verdict
in one query and the qualifying cards in another has reintroduced the defect a
previous review of this fact already removed.

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
release approval on it. This example was replayed under both card-selection rules
and selects `asg_e526fd86` under each, so it demonstrates the card collapse
identically on every ref in A18.

**A third collapse exists and R6 deliberately does NOT remove it.** The fact's
card selection today ignores who holds the card, and applies the independence
test only to whichever card won. So a review card held by the producing card's
own holder, carrying the most recent verdict, wins the selection and then fails
independence, and the producing card is denied even though an earlier
independent round concluded `reviewed-clean`. That behaviour is deliberate: the
fact's own documentation states it as a rule, that a self-held latest round
still disqualifies so a holder cannot launder its own verdict past an earlier
independent one, and it was written that way in response to a previous review of
this fact.

It looks like a third false positive and it is not one. Removing it would let a
producing card's holder resurrect a stale independent clean by filing a verdict
on a card it holds itself, which is the laundering the guard exists to stop. It
is also a change to observable behaviour that nothing in this document's
authority asks for, and I7 forbids it. R6 removes the card collapse and the kind
collapse. It leaves this one exactly as it is, and the ordering stated in the
corrected predicate is what preserves it. AC-20 pins it.

**The size of this defect, stated honestly, under both selection rules.** Over the
thirty days
to 2026-09-04 `completion-requires-review` denied 1,037 times across 821 distinct
cards. 360 of those cards had a linked review card; 339 had one carrying any
holder-filed verdict. What the rail SAW on those depends on which card-selection
rule is replayed, so both were replayed over the same window. Read the columns by
A6: the first is what `main`, `0.1.9`, and the running release actually do; the
second describes the frozen `0.1.8` pointer alone.

| what the rail saw | verdict-recency selection (`main`, `0.1.9`, running release) | `openedAt` selection (frozen `0.1.8` pointer only) |
|---|---|---|
| `reviewed-clean` | 264 | 255 |
| `changes-requested` | 67 | 63 |
| `verified` | 7 | 7 |
| `release-approved` | 1 | 1 |
| winning card carries no holder verdict | 0 | 34 |

The `reviewed-clean` rows are the denial preceding the review — the remedy loop
working exactly as designed. The `changes-requested` rows are true positives: the
review found problems. The `verified` and `release-approved` rows are the false
positives, 8 under both rules, and all seven `verified` cards carry a
`reviewed-clean` earlier on that same review card. That is about 2.4 percent of
the 339, and this document does not claim they explain the bulk of the denials.
They do not. They are the shape that produces the wedge the authority names: a
card that IS landed and IS independently reviewed, refused its terminal receipt.

**What R6 changes, measured under both rules.** Applying the corrected predicate
to the same 821 cards: **272 qualify, against 264 under verdict recency and 255
under `openedAt`. R6 flips 8 cards from denied to allowed on `main`, on `0.1.9`,
and in the running release, and 17 on the frozen `0.1.8` pointer. It flips 0 cards
from allowed to denied under either rule.** The `openedAt` figure is larger only
because that rule additionally loses cards whose most recently OPENED review card
carries
no verdict while an earlier one concluded clean; the corrected predicate reaches
those too, as a consequence of removing the card collapse and not as a separate
requirement.

**8 is the live number.** No host runs the `openedAt` rule and no release ships
it, so a builder targeting any ref this work item can plausibly land on should
expect 8. The 17 is retained here only so the frozen pointer's behaviour is on
the record, and it must not be quoted as the size of this defect.

That zero is I7's test made empirical, not argued. It is the check a builder
should re-run before and after, and AC-22 pins it as an acceptance obligation
rather than a claim to trust.

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
  rail that refuses reviewed work about eight times a month on every ref that runs
  or ships, each refusal landing on the owner's desk as a
  decision request. That is the manufactured paperwork the authority names.
  Acceptance loses.
- *Add?* Nothing is added. Two collapses are removed from a query. `deny_when`
  keeps the same three clauses, the same fact name, and the same values, and the
  fact keeps its return contract, so no rule logic is edited.

One string in the rule file does have to change, and it is not logic. The rule's
`text` — the sentence a denied agent reads — currently says completion "needs
exactly one `--reviews`-linked card held by a different session whose latest
holder-filed verdict is reviewed-clean". That sentence describes both collapses
verbatim, and after R6 it would describe the rail wrongly to the one reader who
most needs it right: the agent that was just refused. Correct it to state the
corrected predicate. A rail that misdescribes itself is what sends a lane looking
for someone to ask, which is the paperwork this document exists to stop.

### R7 — `effort-rule` admits the escalation lineage, not only the rung the clock has reached

**The defect.** The frozen `0.1.8` pointer and the release gibson runs authorize a
session principal by exact identity with the row's current expecter (A9). `main`
and `0.1.9` carry the opposite defect and are treated separately below. But the
expecter is not a party
the request was addressed to once and for all. It is one member, selected by the
clock, of a chain the substrate itself computes: `initial_expecter/2` picks the
first entry, and `advance_expecter/2` walks `spawnedBy` upward on each 24-hour
deadline, `route_session/5` skipping the holder and any inactive session at every
step. Every session in that chain is a principal the substrate has already
decided is entitled to answer. The predicate admits exactly one of them at a
time, and which one is a function of how many deadlines have passed.

That is the same defect shape as R6 and R1: a predicate collapses a set the
substrate already computes down to a single current member, and refuses the rest.
Two consequences, both present in the live data (A11):

- **The passed rung.** An active session at a lower rung, entitled to answer and
  in fact the expecter until the last deadline fired, is refused now. One open
  request is in this state.
- **The retired rung.** When the current expecter retires, no living member of
  the chain may act, and the request is stranded exactly as a retired raiser
  strands an operator request at R1. Two open requests are in this state. This is
  the retired-raiser trap in a second subsystem, and it is why R7 belongs on this
  work item rather than its own.

**The requirement.** Change the session clause of `authorized?/2` so that a
session principal is authorized when it is a member of the request's escalation
lineage, as Terms defines that set: computed from the assignment by the same walk
`route_session/5` performs, excluding the assignment's holder at every step,
**admitting only sessions in state `active` and stepping past any session that is
not**, and never read from the row's current expecter columns. The user clause is
unchanged. The authorized actions remain exactly `continue` and `dismiss`.

Both halves of that sentence are load-bearing and a builder must implement both.
Dropping the active-session condition builds a WIDER set than Terms defines and a
wider one than `route_session/5` selects from, which contradicts R7's own
rationale: the members admitted are exactly the principals the substrate has
already decided are entitled to answer, and a session the selector steps past was
never one of them. The condition is currently inert in the live data — the
`sessions` table holds only `active` and `retired` (A17), and a retired session
cannot make a call — so a build that omits it passes every test the live corpus
can produce and is still wrong. AC-23 pins it.

`authorized?/2` is one private function consulted at TWO points on the rule path:
once in `effort-rule`'s pre-transaction check and again inside the ruling
transaction, so the check survives a concurrent expecter advance. R7 changes that
one function, and both call sites therefore change together. A builder who inlines
a lineage test at one site and leaves the other on identity has built the race the
second check exists to close. AC-24 pins it.

R7 may read, call, or extract the walk `route_session/5` already performs in
order to enumerate that set, including lifting it into a shared function that
both the selector and the membership test call. It may likewise CALL
`initial_expecter/2` and `advance_expecter/2` if enumeration needs them: Non-Goal 8
forbids changing what those functions return, not reading them. What R7 must not
do is change the principal `route_session/5` selects for `advance_expecter/2`,
which is the behaviour Non-Goal 8 protects. Enumerating a chain and picking one
member of it are the same walk read two ways; R7 adds the first reading and leaves
the second identical.

Everything else stays where it is. `advance_expecter/2` still walks on deadline.
The deadline is still 24 hours. The notification still goes to the current
expecter. `menu_in_txn/3` still computes the ordinary-power menu for the current
expecter's rung, and every ordinary power keeps its own handler's authorization,
so admitting a lineage member to `effort-rule` grants it nothing anywhere else.

**Two things R7 must not become.**

*It must not admit the holder.* The holder is the party under supervision. A
check-in a stalled holder may dismiss is not a check-in. `route_session/5`
already excludes the holder from the chain, and R7's membership test excludes it
for the same reason. I8 states this and AC-16 fails if it is ever violated.

*It must not become "any session".* **BOTH `main` and `0.1.9` already carry that
change** (A9) — `main` at `effort_checkin.ex:1390` from `e02cab00`, `0.1.9` at
`:1425` from `7090a630`. Read against the rule path around it, no other clause
excludes the holder, so on `main` and on `0.1.9` as they stand a stalled holder
may dismiss its own
liveness check-in. R7 REPLACES that clause; it does not build on it and it is not
a formalisation of it. This is recorded here because a builder working on
EITHER of those refs would otherwise read the existing widening as the fix
already landed and
close the requirement without changing anything.

This warning applies to `0.1.9` as much as to `main`, and an earlier draft of this
document said `main` only. `0.1.9` is the branch release tags are cut from, so the
ref most likely to be built on is one the earlier draft did not warn about. The
running release is not affected: `7090a630` is in no tag, so the shipped artifact
still carries the narrow clause (A9, A18).

**Size, stated rather than implied.** R7 reaches 3 of the 37 open effort
requests. It leaves the 23 correctly refused, and it does not reach the 11 that
have no agent in the lineage at all, because there is no principal for it to
admit. What happens to those 11 is OQ-5, and this document does not decide it.
A builder must not close OQ-5 by widening R7; AC-18 is written to make that
attempt fail.

### The seam (mechanism two)

R6 and R7 above are mechanisms one and three. R1 through R5 below are mechanism
two, and they rest on one seam.

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

**The opener can be dead too, and this is the limit of R1.** The authority R1
derives is perishable in exactly the way the raiser's is: an opener session
retires like any other. Across the 630 operator requests in the live database,
349 have an active opener, 127 have an opener that has since retired, 106 are on
cards the owner opened himself, and 48 have no subject card (A16). Three
consequences follow, and none of them is worked around:

- On the 106 owner-opened cards R1 adds nothing. Terms resolves the opener of
  such a card to the owner's own session, and the owner could already retract.
  R1 is a no-op there by construction, not by oversight.
- Where the raiser has retired, a dead opener costs nothing, because R3 and R4
  clear the row on the raiser's retirement without needing any live principal at
  all. That is the case the authority names, and it is closed.
- One residual case is left open and is named here rather than hidden: the raiser
  is alive but cannot run — out of capacity, wedged, or unresponsive — AND the
  subject card's opener has retired. R3 and R4 do not fire, because the raiser
  never retired, and R1 admits a principal that cannot act. That row is stranded
  until the raiser recovers or retires.

R1 removes the single point of failure in the common case; it does not make the
clearing path immortal, and this document does not claim it does. Closing the
residual would mean deriving authority from something further up than the opener,
which is a wider design than the authority permits and is not specified here. It
is recorded as OQ-7.

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

Delete that one clause, `AND kind != 'operator'`, from that routine's row query:
`lib/tightbeam/escalation.ex:1505` on `main`, `:704` on `0.1.9`, and `:539` on
both the `0.1.8` pointer and the running release.
The clause is character-identical in all four places; only its address differs. The
comment describes the intended behaviour correctly; the filter contradicts it.
Nothing else in the routine changes.

**On `main`, one thing in that routine must NOT be deleted.** There the
same query is followed by a second filter that rejects any request whose
`context.verb` is `cannot-proceed`, on the stated ground that retirement is
neither an exact assignment disposition nor an exact release fact (A14). That
carve-out is deliberate and correct, and R3 leaves it exactly as it is. R3
deletes the KIND exclusion and only the kind exclusion. A builder that reads
"delete that exclusion" as licence to strip both filters has changed a behaviour
this document did not authorize changing.

**On `0.1.9` and on `0.1.8` that filter does not exist**, and this paragraph is
therefore a no-op on both, and in the running release. A builder on either of
those refs must not add it. Porting
the carve-out backwards would be a behaviour change on a shipping line, with no
authority in this document and none in the work item: the rows it would guard do
not exist there either (A14). R3 on `0.1.9` or `0.1.8` is one deletion and nothing
else.

The measured consequence of the contradiction: across the entire live database,
for every kind, zero rows carry the withdrawal reason `raiser-retired` that the
routine writes. The routine has never cleared anything in production, because the
org raises exactly two kinds — 5,933 effort rows and 630 operator rows, and no
others — effort requests supersede rather than withdraw, and operator requests
were excluded. The sweep excludes precisely the one kind it could have helped.

### R4 — the sweep that already exists stops excluding the same kind

R3 alone fixes the future: it fires on the retirement event, so a session that
retired before it ships is never revisited and its rows stay open forever with no
lawful actor. Reaching those rows needs a pass keyed on the raiser's recorded
state rather than on the retirement event.

**That pass is already built.** `Escalation.recover_retired/1` selects every
session in the retired state that still has open decision requests and calls the
withdrawal routine on each; `boot.ex` calls it on every gateway boot (A13). It is
the exact mechanism, with the exact state key and a working trigger. Its
candidate query carries the same `kind != 'operator'` exclusion.

So R4 is one deletion, not a mechanism: **delete `AND dr.kind != 'operator'` from
`recover_retired/1`'s candidate query** — `lib/tightbeam/escalation.ex:1629` on
`main`, `:823` on `0.1.9`, and `:658` on both the `0.1.8` pointer and the running
release, character-identical in all four. With R3
that makes both halves of the pair the same one-clause subtraction in two places.

**Build no sweep.** No scheduler, no timer, no daemon, no periodic pass, no
migration-time backfill, and no second reconciliation beside the one that exists.
The trigger is the existing boot call and this document adds none. A builder that
finds itself writing a new sweep has misread R4 and should re-read A13. The
idempotence R4 needs is already a property of the routine it reuses: the update
is guarded on `status = 'open'`, so a request already withdrawn, ruled, or
superseded is left untouched and no second lifecycle row is written.

R3 and R4 together are the answer to "what happens to a request whose raiser has
retired". R3 fixes the future at the retirement event. R4 reaches a row that is
already stranded, at the next boot. Neither one adds anything to the substrate.

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
file entry. No exemption, override, or claim. No migration. R1, R3, R4, R6, and
R7 are edits to existing queries and authorization predicates; R5 is prose. R3
and R4 are deletions of one clause each, and R4 reuses a sweep and a trigger the
substrate already has (A13); the sweep fence a builder is held to is stated once,
at R4 under "Build no sweep", and is not repeated here.

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
does nothing for a rail that refuses correctly — which is not rail friction as
Terms defines it, since the work is not done and recorded — and it leaves the
retired-raiser dead end exactly where it is. Fixing a cause never clears the
effects that already happened.

*What the ordering claim is, exactly.* R5's paragraph is not FALSE before R1
ships. Every path it names works today for a raiser that can run: raisers
retracted their own requests on 2026-09-04, openers adjudicated, and the fresh
review round is the repair Q4 records as already working. R5 is incomplete before
R1, not untrue: without R1 its advice has nothing to offer the case where the
raiser cannot run, which is the case that produced this document. Ship R6, R1,
R3, R4 first, then R5, so the paragraph can name the opener path as well. That is
a preference about completeness, not a dependency, and R5 shipping early would
make no sentence in it wrong.

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

One question was attached to this answer and has since been ruled out of this
document's scope, for the reason stated here: a retraction removes the question
and authorizes nothing, so nothing specified here rests on the ruling path. See
OQ-1.

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
would have prevented, and as of this writing no stranded row remains.** At
2026-09-04 22:50 UTC the open operator set is a single row, `dr_24edf371`, whose
raiser is active and which is the genuine owner decision named in Terms. R4 is
therefore prophylactic today rather than remedial, and the specification says so
plainly instead of claiming a cleanup it will not perform. It will not stay
prophylactic: 127 of the 630 operator requests raised to date sit on cards whose
opener has since retired (A16), and raisers retire at the same rate.

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
- *Add?* Nothing is added. R3 and R4 are the same one-clause deletion in two
  places, and the sweep and trigger R4 needs already exist (A13). What is removed
  is an exclusion that contradicted its own documentation, twice.

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
document designs for the honest case instead.** The question's "real owner
decision" is the term Terms defines as **genuine owner decision**; the two names
are one concept and the defined one governs.

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

**AC-4 (I1, I3, what this build must hold).** GIVEN an open operator decision
request, WHEN a session principal calls `operator-withdraw` under any of the
widenings R1 through R4 grant, THEN the row reads `status = 'withdrawn'` and its
`decision`, `ruledBy`, `ruledAt`, and `rulingFactId` are all NULL; AND GIVEN the
same request, WHEN a session principal calls `operator-rule` without an identity
flag, THEN the call is refused and the row is unchanged. This check is green
today and must stay green after every requirement here lands. It is the whole of
what this document changes and the whole of what it can promise.

**AC-4b (I1, the hole OQ-1 names).** GIVEN an open operator decision request,
WHEN an agent session calls `operator-rule` with the owner's identity flag, THEN
the row is unchanged. This check FAILS today and this document does not repair
it. It is written here so that the gap is a named red check rather than an
absence, and it belongs to the requirement OQ-1 asks whether to state; a builder
working from this document must not attempt to make it pass. It cannot be
decided from the `decision_requests` row, whose `ruledBy` records attribution
and not the authorizing principal (A12); it is decidable only from the `events`
row's calling session key. AC-4 does not subsume it, and a reader who reads AC-4
as covering the identity-flag route has read it wrong.

**AC-5 (R3).** GIVEN a session holding one open `operator` request and one open
request of another kind, WHEN that session retires, THEN both rows read
`status = 'withdrawn'` with the retirement sentinel as `withdrawnReason` and no
decision on either.

**AC-6 (R4).** GIVEN an open `operator` request whose raiser session is ALREADY
in the retired state, and whose retirement therefore left it open, WHEN
`Escalation.recover_retired/1` runs — the routine `boot.ex` already calls on
every gateway boot (A13), and no other trigger — THEN that row reads
`status = 'withdrawn'` with the retirement sentinel. The check names that
routine by name; a builder who has to introduce a new trigger to make it pass
has built something R4 forbids.

**AC-7 (R4, idempotence).** GIVEN a request already `ruled`, `withdrawn`, or
`superseded` whose raiser is retired, WHEN `recover_retired/1` runs, THEN the
row is byte-identical to before and no second lifecycle record is written.

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

**AC-15 (R7, the passed rung).** GIVEN an open `effort` request whose current
expecter is the session at rung 1 of its assignment's escalation lineage, and an
active session at rung 0 of that same lineage which is not the assignment's
holder, WHEN the rung-0 session calls `effort-rule --action continue`, THEN the
request reads `status = 'ruled'` with `decision = 'continue'`, and the deadline
wake and generation are disposed of exactly as they are when the current expecter
rules. This check FAILS against the `0.1.8` pointer and against the running
release as they stand on 2026-09-05, which is the defect R7 repairs. On `main` and
`0.1.9` it passes for the wrong reason — the wide clause admits every session
(A9) — so on those refs AC-15 alone does not demonstrate R7, and AC-16 is the
check that does.

**AC-16 (I8, the holder stays refused).** GIVEN an open `effort` request on an
assignment, WHEN the assignment's holder session calls `effort-rule` with either
`continue` or `dismiss`, THEN the call is refused and the row is byte-identical
to before. This check must be green on whichever ref R7 lands on, and it must be
written so that it fails for any change that admits the holder by any route.

**Where it starts red.** AC-16 passes today on the frozen `0.1.8` pointer and in
the release gibson runs, which carry the narrow clause. **It starts RED on BOTH
`main` and `0.1.9`**, which carry the wide clause that admits every session (A9).
An earlier draft of this document said `main` only; that was wrong, and `0.1.9`
is the ref release tags are cut from. A builder on either of those two refs must
expect this check to fail before the work begins and must not read its failure as
a defect in the check. It is the check that makes the difference between R7 and
the existing widening observable.

**AC-17 (R7, the retired rung).** GIVEN an open `effort` request whose current
expecter session is in the retired state, and an active session above it in the
same escalation lineage which is not the assignment's holder, WHEN that session
calls `effort-rule --action dismiss`, THEN the request is ruled and the holder
re-arm proceeds exactly as it does for a dismissal by the current expecter. This
check also FAILS today.

**AC-18 (R7, no lineage means no path).** GIVEN an open `effort` request whose
assignment's escalation lineage contains no active session other than the holder,
WHEN any session calls `effort-rule` with either action, THEN the call is refused
and the request keeps its user expecter. R7 creates no answerer where the
substrate itself computes none. This check exists so that a builder cannot close
OQ-5 by widening R7, and it must be written so that it fails if any principal
outside the computed lineage is ever admitted.

**AC-19 (R7, scope unchanged).** GIVEN an open `effort` request and a lineage
member that R7 newly admits, WHEN that member calls `effort-rule` with an action
other than `continue` or `dismiss`, THEN the call is refused with the existing
invalid-action error; and WHEN that member invokes any ordinary power from the
request's menu, THEN that power's own handler authorizes it independently and R7
grants it nothing. R7 changes one clause of one authorization predicate.

**AC-20 (I7, the third collapse stays).** GIVEN a producing card with two
`--reviews`-linked review cards, an earlier one held by another session whose
holder filed `reviewed-clean`, and a later one held by the producing card's own
holder whose holder filed `reviewed-clean` after it, WHEN the producing card's
holder attests completion, THEN `completion-requires-review` denies it. This
check is green today and must stay green after R6. It is the anti-laundering
behaviour R6 deliberately preserves, and it is the check that fails if a builder
filters self-held cards out of the pool before choosing the winning verdict
instead of testing independence on the winner.

**AC-21 (R6, the empty pool).** GIVEN a producing card with one
`--reviews`-linked review card held by another session, whose holder's only
verdict is `verified` and which carries no review-conclusion verdict at all,
WHEN the producing card's holder attests completion, THEN
`completion-requires-review` denies it. This check is green today and must stay
green after R6. R6 makes the rail read conclusions it already has; it invents
none where there are none.

**AC-22 (R6, no card flips from allowed to denied).** GIVEN the set of producing
cards that `completion-requires-review` denied over a stated window, WHEN the
fact is evaluated over that same set before and after R6 on the line being
built, THEN every card the current predicate qualifies is still qualified by the
corrected one, and the count of cards that move from qualified to unqualified is
zero. This document measured that count as 0 under both selection rules over the
thirty days
to 2026-09-04, with 8 cards moving from denied to allowed under verdict recency
(`main`, `0.1.9`, the running release) and 17 under `openedAt` (the frozen `0.1.8`
pointer only, A6). A builder re-runs the comparison on the ref being built
and records both numbers on the card; on any ref this work item can plausibly land
on, the expected move-to-allowed figure is 8. The comparison is a read-only query
run by
hand; nothing here authorizes a report, a view, or a check that ships
(Non-Goal 2). A nonzero denied count is a defect in the
implementation, not a revision of this requirement: R6 removes a collapse, and
removing a collapse cannot subtract a member from the pool.

**AC-23 (R7, only active sessions are admitted).** GIVEN an open `effort`
request whose escalation lineage contains a session in a state other than
`active`, WHEN that session's principal calls `effort-rule` on the request,
THEN the call is refused as unauthorized, and WHEN the next `active` session
along the same walk calls it, THEN the call is authorized. This check cannot be
produced from the live corpus today, because `sessions` holds only `active` and
`retired` and a retired session makes no calls (A17). It is written against the
predicate, not against the corpus, and it fails a build that computes lineage
membership without the state condition.

**AC-24 (R7, both call sites move together).** GIVEN an open `effort` request
and a lineage member that R7 newly admits, WHEN that member rules the request,
THEN the ruling is authorized both by the pre-transaction check and by the
in-transaction re-check, and the request reaches `ruled`. A build that changes
one call site and not the other fails this check by refusing inside the
transaction after admitting outside it. The two checks exist so authorization
survives a concurrent expecter advance; R7 changes the one predicate they share
and leaves both call sites in place.

**AC-25 (I4, a retraction is a marker carrying its cause and its principal).**
GIVEN an open operator decision request and a principal R1 through R4 newly
admits, WHEN that principal calls `operator-withdraw` WITHOUT a reason, THEN the
call is refused and the row is unchanged; and WHEN it calls with a reason, THEN
the row records `withdrawnBy` naming that principal and `withdrawnReason`
carrying the given cause, and a `decision_request_withdrawn` lifecycle row is
written carrying both. This check is green today — the withdrawal reason is
required at the entry point on all four refs in A18, verified 2026-09-05 at
`escalation.ex:659` on `main`, `:477` on `0.1.9`, and `:314` on the `0.1.8`
pointer and the running release, and the row update and the lifecycle
write happen inside one transaction — and it must stay green after every
widening here lands. AC-1 does not test it: AC-1 supplies a reason in its GIVEN,
so a build that accepted a reasonless retraction would pass AC-1 and still
destroy I4. Widening WHO may retract is lawful only while every retraction stays
attributable to a principal and a stated cause. That is the property which makes
a wrong retraction findable in the record afterwards rather than a silent loss,
and it is the whole of what this document offers against a retraction that
should not have happened.

## Open Questions

**OQ-1. RULED on 2026-09-04: out of scope for this document, and it stays out.**
Whether hardening the operator RULING path belongs to this work item.

While verifying I1 against the source, a gap was found between what I1 promises
and what the ruling path enforces. Its shape is not the same on both code lines,
and its detail is deliberately not written here: the spec commons is a public
repository, and a precise account of a gap in an authorization guard does not
belong in one. The finding is recorded on `asg_d893bbf9` and carried to the
card's owner, who has it. What can be said safely is the part that matters to a
reader of this document: a `decision_requests` row alone would not distinguish
the case, while the `events` row would, because it records the calling session
key.

Measured state as of 2026-09-04: unexercised. All 493 successful operator
rulings in the preceding 30 days carry the owner principal with a NULL session
key, that is, the owner's own CLI. All 140 refusals in the preceding 14 days are
likewise from the owner's CLI. No agent session has attempted it. It was not
executed against the live org during this specification's verification and must
not be.

**The ruling, and the reason it is the right one.** Nothing specified here
depends on the ruling path. The retraction widening in R1 through R4 records no
decision — a retraction removes the QUESTION and authorizes nothing — so widening
it neither uses nor worsens that path; R5 is prose; R6 is a completion rail and
touches the decision request subsystem nowhere; and R7 is the `effort` arm, which
I1 does not govern and which reaches no `operator` row. A hole this document does
not stand on is not a hole this document must fill. **Every requirement here —
R1 through R7 — may be built now**, and no card may be widened on account of this
question.

The finding travels as a security fact to the owner by a different instrument
than a decision request, on the card owner's ruling of 2026-09-04. It does not
gate this build, it is not reopened by a later reader of this file, and the
requirement that would state the ruling guard precisely is not written here. If
it is ever wanted, it belongs to its own work item with its own authority.

**It must not be tested.** Exercising the gap to confirm it IS the forgery. It
was not executed against the live org during this specification's verification,
it was found by reading source on a read-only checkout, and no builder working
from this document may execute it either. The measured state recorded above —
unexercised, by any session, ever — is the last word this file has on it.

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
If the owner later wants standing measurement of rail denials — the whole
denial population, wider than rail friction as Terms defines it — it is its own
work item.

**OQ-4. NON-BLOCKING.** Whether R5's guidance paragraph should later be promoted
up the escalation ladder is not decided here, and this document's position is
that it should not be promoted on the evidence available. A rail on the raise
side would require the classifier that Q5 refuses. Revisit only if measurement
shows the guidance failing, which requires OQ-3 first.

**OQ-5. BLOCKING, for the claim that the effort channel is fixed. Blocks
nothing this document specifies.** What becomes of an effort check-in that
reaches the owner user and has no agent above the holder.

`advance_expecter/2`, given a request whose expecter is already a user, returns
the same user at the same rung (`lib/tightbeam/effort_checkin.ex:989`, released
line). `deadline_in_txn/3` then writes that same expecter back to the row,
schedules a fresh deadline wake into the owner's personal session, and re-arms
the notification. The default deadline is 24 hours. So a check-in that tops out
at the owner re-asks the owner every day and never resolves. Eleven of the
fourteen requests currently at a user expecter are in this state, and the oldest
has been in it for 7.8 days (A11).

This is rule 14 in its exact form. The intent has an owner, and its deadline is
rewritten before it can ever expire, so its absence is not detectable. It is not
an authorization defect: for those eleven, the card was opened by the owner and
the holder has no ancestor, so there is genuinely no agent to admit, and R7
changes nothing about them.

Three answers exist and this document deliberately picks none. ADD: resolve the
request after a bounded number of terminal re-arms, recording the mechanical
cause. DELETE: stop escalating a liveness prod past the last agent, on the ground
that a check-in with no supervisor above the holder has no addressee and the
substrate is asking a question it has nobody to ask. ACCEPT: let it stand and
re-ask, and record that as the org's chosen answer rather than an accident.
Choosing among them is a judgment about what the org wants when nobody answers a
supervision question for a week. That is the owner's to make, and a specification
that assumed one would be deciding its own scope.

What is blocked is only the claim that the effort channel is fixed. **R7 may be
built now**, and it closes every case in that channel where a lawful agent
answerer exists.

**OQ-6. NON-BLOCKING, but the card must answer it before a builder starts.**
Which REF R7 and R6 target. TWO requirements raise this, not one. Read this
section against A18: there are three branches and a running release, not two
lines, and an earlier draft of this section reasoned about two.

R7's targets differ in text. The `0.1.8` pointer and the running release carry
the narrow session clause; **both `main` and `0.1.9` carry the wide one** (A9),
which is the opposite defect: too wide rather than too narrow. R7's requirement
sentence is the same against any of them, and only the clause the builder
replaces differs. The consequence a card must carry: on `main` and on `0.1.9`,
AC-16 starts RED.

R6's targets differ in behaviour, which is the sharper case. The fact's card
selection is NOT byte-identical across refs, but the split does not fall where an
earlier draft placed it. `main`, `0.1.9`, AND the running release all collapse to
the review card carrying the most recent holder-filed verdict, computed in one
join; the function body is byte-identical between `0.1.9` and the running
release. Only the frozen `0.1.8` pointer collapses to the most recently OPENED
review card and reads verdicts inside it. R6's requirement text holds against
both rules, because both collapse and R6 removes the collapse. What differs is
what a builder deletes, and what the change is worth: **8 cards on any ref this
work item can plausibly land on, and 17 only on the frozen pointer**, measured in
R6 and pinned by AC-22. A builder targeting the frozen pointer must not carry
`openedAt` into the corrected predicate; on the other three refs `openedAt` is
not in the fact to carry. A6 records the same split from the measurement side.

R3 and R4 raise a weaker form of it. The clause each deletes is
character-identical on all four refs, so the requirement and the edit are the
same; what differs is the address (R3 at `:1505` on `main`, `:704` on `0.1.9`,
`:539` on the `0.1.8` pointer and the running release; R4 at `:1629`, `:823`, and
`:658` respectively) and the surrounding routine. Only `main`'s
`withdraw_for_retired/2` carries a cannot-proceed carve-out; neither `0.1.9` nor
`0.1.8` has it, or the typed request it guards, at all (A14). So R3's "must not
delete" paragraph guards something that exists on ONE ref. A builder must not read
it as an instruction to port that carve-out backwards.

R1, R2, and R5 do not raise this question: R1 and R2 change one authorization
predicate, `operator_withdrawer_in_txn/3`, which is byte-identical across `0.1.8`
and `0.1.9` (verified 2026-09-05) and on `main`, and R5 is
kungfu guidance with no code target at all.

Whether this work item lands on `0.1.9`, on `main`, or on both by cherry-pick is
an election under the repository's cross-ref rule, and it belongs on the
assignment cards that dispatch R3, R4, R6, and R7. Each card states its ref by the
names in A18; a card that does not state it, or that says `0.1.x`, is not ready to
dispatch. **`0.1.x` is not a branch and is not an answer to this question.**

**OQ-7. NON-BLOCKING, and deliberately not specified.** The residual case R1
leaves open: a request whose raiser is ALIVE but cannot run — out of capacity,
wedged, or unresponsive — AND whose subject card's opener has itself retired.
R1 admits the opener, R3 and R4 clear the row when the raiser retires, and
neither reaches this shape. It is a real hole and it is left open on purpose.

Closing it means deriving withdrawal authority from something further up than
the subject card's opener: an ancestor walk, a lineage rule, or an owner-agent
role. Every one of those is a general permissions design, which is wider than
this work item's authority and is exactly the accretion its fences forbid. The
honest MVP position is that the row stays open, visible, and answerable by the
owner user, who retains the authority every requirement here already grants.

A builder must not close OQ-7. If it turns out to bite in practice — a row
stranded in this shape and noticed — the evidence goes back to the owner as its
own work item, with the stranded row named. It is not a defect in R1 to be
repaired inside this build.

## Sequencing note

R6 is independent of the rest: it touches one fact query in the rules layer and
nothing in the decision request subsystem. It may run in parallel with the
others, and it is the one that removes a cause rather than clearing effects, so
prefer it first.

Four requirements target code that differs across the refs in A18, and each of
their cards must name the ref it targets before dispatch, by the names in A18:
R3, R4, R6, and R7, per OQ-6. R6's difference is the sharpest, because there the
refs differ in BEHAVIOUR and not only in address, and the behavioural split
isolates the frozen `0.1.8` pointer alone. R1, R2, and R5 need no such election.

R1, R3, and R4 are independent of each other in effect but touch the same
subsystem; order them rather than running them in parallel. R3 and R4 delete the
same clause in two functions and should land together. R5 lands after R1 so its
guidance can name the opener path, which is a preference about completeness and
not a dependency: R5 is true and buildable before R1, merely incomplete (Q1).

R7 touches `effort_checkin.ex` and nothing R1 through R6 touch, so it may run in
parallel with all of them. Its card must carry AC-16 as a check that has to be
green on whichever ref it lands, because on BOTH `main` and `0.1.9` that check
starts red (A9, AC-16). `0.1.9` is the ref release tags are cut from, so the ref
most likely to carry this work is one that starts red.

Nothing in this document is applied to a running host by the work it specifies.
The production host runs `v0.1.8+1337` and is locked at 0.1.8 under Mike's
2026-09-02 change law, and any deployment of this change is a separate act
requiring that law's two-step ceremony.
