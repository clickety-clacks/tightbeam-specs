# O2 recovered design assessment

8 September 2026. Lead disposition after reading the complete archived predecessor design and a bounded independent review. This preserves useful prior work and identifies corrections for the existing successor designer. It is not implementation acceptance or a request to restart the design.

Later disposition on 8 September: supported recovery returned the remaining design externally. The selected replacement is [O2 current acceptance and accountable review routing](tightbeam-019-o2-acceptance-and-routing-design-2026-09-08.md). This assessment and the historical draft below remain preserved as the reasoning and superseded proposal, not the current implementation instructions.

Predecessor artifact `art_96871dce`, SHA256 `4541f6c50afc88534d6f3e7c8798f557d22088d6e8f3002af522195ad518c631`, was recovered from the retired session archive. Its unchanged text follows below. Claims about an active holder describe that historical draft, not current custody. O2 and remedy parent assignments retain their outcomes after the two old assignments were revoked for recovery.

## Required corrections

1. Absence of a linked review after `failed_unknown` does not establish absence of effects. The recipient may have begun work elsewhere. Require evidence that retry is safe or route owned reconciliation. One allowed retry is still a replay and does not by itself make it safe.
2. A linked review row does not prove current capable ownership. The proposed suppression would strand work if the reviewer is unavailable, revoked, or only covers an earlier result. Suppress duplicate commissioning while applicable review work remains owned; route an unresolved review need to its accountable owner when recovery is needed.
3. Immutable result normalization is new implementation work. The bounded b299 source check found existence validation with `git cat-file -e`, not stored resolution to a commit OID. Normalize and persist identity when evidence is filed. Do not re-resolve an old mutable ref and reinterpret historical judgment. Specify comparison across producer/reviewer clone locations and treatment of existing unnormalized evidence.
4. Changed identity requires a judgment about evidence applicability. It does not automatically require rerunning tests or repeating a complete review. Responsible agents may record justified applicability of existing evidence to the current result. Keep independent judgment and truthful current evidence; describe how later contrary verification affects acceptance. Matching refs prove identity, not verification truth.
5. Define recovery for a fired wake without a turn, pending delivery to an unavailable recipient, and repeated known failures. Give each an owned reconciliation path with restart and successor behavior. Another completion attempt must not be the only way unresolved recovery receives attention.
6. The notice mechanism covers policy, release and live effects as well as code, but the proposed key depends on a code commit digest. Define the stable supported review-need identity for non-code work without requiring invented Git evidence. Keep the code freshness change bounded and do not claim equivalent non-code freshness is already implemented.

Retain the sound parts: select the latest directly linked conclusion before checking applicability, preserve independent holder attribution, route staffing judgment to the accountable owner, and recheck terminal state transactionally. Compose with the accepted late-ruling and WakeRails predecessors. These corrections go to the existing executive/designer; they create no new producer, reviewer ceremony or current-gate bypass.

Evidence limits: lead and helper read the design; the helper made one bounded b299 validation-source check. No implementation or runtime tests were performed for this assessment. The successor must substantiate exact fields, consumers and migration behavior during engineering review.

## Preserved predecessor draft

The following is historical proposal text, not accepted final design.

# O2 acceptance and accountable review routing design

Date: 2026-09-08

Assignment: `asg_1c7f4951-aa65-41ac-ac33-61db8a4cf84d`

Holder: `agent:main:clawline:mike:main s_7e3a85f6` (`coder`, active)

Work item: `wi_fcbc79fe-8b77-42d7-a5ba-0d890359d0f9`, owned by `mike`

Authority: `tightbeam-019-work-reconciliation-2026-09-08.md` at specs commit
`62efbc3589d67bb8822fdcd6fb1d81c26262db99`, content SHA-256
`50a20b4393fe8fda32c919a590d220d7e7613f48f8e26bda6c223fc06beec2d2`, and
`tightbeam-019-agent-judgment-plan.md` revision 16 at specs commit
`33980042a8cf0aec8ad03073730944e08c1df204`, content SHA-256
`254a1612e32e115a9bf9a5c5cc74d31aa6b6811f9d08b7562b96e8a929be7466`.

Source baseline: clean read-only clone at
`b299457d5c95dd6e161ed9b1de70b4450b5166b7`. The separate remedy clone remains
clean at `634cf9775398ec28ed443bd217c9a9b36b105de6`. This design makes no product,
guidance, rule, runtime, or schema edit.

## Controlling input

The full input wake is `w_d41892d3-0387-42a5-a802-55493208e6fe`. Its turn
`124377` reached `delivered`. The input identifies these gaps on `b299457d`:

1. `RailRemedy.binding_context/3` exposes the producer holder and its owner. It
   does not expose the assignment opener or the work item's accountable owner.
2. `RailRemedy.producer_live?/3` treats an active target session as a live wake
   remedy. It does not prove that the notice reached the recipient.
3. `Assignments.qualifying_review_verdict_kinds/3` selects the latest directly
   linked, holder-authored review conclusion. It does not prove that the verdict
   or verification applies to the result that now seeks completion.

The older orchestration draft is not authority. The old unmerged result-revision
and notice-effect commits are evidence of attempted designs only.

## Current behavior at b299457d

### Review admission and completion

`priv/kungfu/agentic-engineering/rules/engineering.toml` denies a linked code
review assignment while the open producer lacks a holder-noted `tests-passed`
verdict. Failing code therefore cannot enter the formal linked review path
without a claimed pass.

The `completion-requires-review` rail applies to `code`, `policy`, `release`, and
`live_mutation` effects. On a missing clean review, it blocks completion and runs
an `assign` remedy against the `reviewer-code` role. The substrate therefore
chooses and opens a reviewer assignment.

`Assignments.qualifying_review_verdict_kinds/3` examines only direct review cards
whose `reviewsAssignmentId` equals the producer assignment. It pools only
holder-authored `reviewed-clean` and `changes-requested` verdicts, orders them by
verdict `ts DESC, rowid DESC`, and tests independence on the winning row. A later
`changes-requested` already defeats an older `reviewed-clean`. Later verdicts of
other kinds do not hide a review conclusion. Descendants and unlinked verdicts
do not qualify.

The query does not read `attests.commitRefs`. A clean verdict for result A can
therefore qualify a completion that now claims result B. The verification rail
only requires that `assignment.verdicts` contains `verified`; it does not require
the producer holder as author or match the verified result to the completing
result. The results-artifact rail requires a holder artifact kind, but it does not
bind that artifact to a result revision.

### Remedy and delivery

`RailRemedy` keys an episode by `{statute, subject}` and derives the dispatch key
from `{statute, subject, occurrence}`. Its context query reads the assignment ID,
work item ID, holder key and role, holder archetype, and the holder session's
`ownerUserId`. It omits `assignments.openedBySession`, `openedByUser`, and
`work_items.ownerUserId`.

For a wake remedy, `producerKey` is the bound target session. A repeat considers
the remedy live when that session remains active. This is target availability,
not delivery evidence.

The durable wake row records `wakeId`, `sessionKey`, `targetRole`, `origin`,
`state`, `work_item_id`, and `assignmentId`. Its `state` only records scheduling:
`pending`, `fired`, or `canceled`. The turn row linked by `turns.wakeId` records
delivery: `queued`, `running`, `delivered`, `canceled`, `failed`, or
`failed_unknown`. `failed_unknown` is terminal and has no automatic retry.
`Wakes.preserve_failed_intent_in_txn/3` creates a deterministic successor only
for the proven `rate-limit-dead` failure class.

## Selected design

### 1. Permit early linked review

Remove `code-review-requires-passing-tests` and conform the reviewer guidance in
the separately owned O1/O2 guidance candidate. A reviewer can inspect a failing
result and file `changes-requested` without a fabricated pass. This removal does
not weaken completion.

### 2. Use an existing result identity

For a code completion, define the current result as the canonical, non-empty set
of existing `commitRefs` on the incoming producer completion. Resolve every ref
to its immutable commit OID with the existing host and repository validation.
Sort the normalized `{repo, commit}` set before equality or hashing. Do not add a
token, receipt kind, review phase, or descendant lookup.

The holder-authored review conclusion on a directly linked review card must carry
the same canonical `commitRefs`. Review verdicts already support these refs. The
producer holder's `verified` verdict must also carry the same refs. This requires
a narrow validation change because the current code rejects `commitRefs` on a
producer-card verdict. It reuses the existing `verified` verdict and
`attests.commitRefs` column.

The completion consumer must use this order:

1. Normalize the incoming code completion's `commitRefs`. Refuse a missing,
   empty, duplicate, or unverifiable identity.
2. Select the newest holder-authored `reviewed-clean` or `changes-requested`
   verdict across every directly linked review card by `ts DESC, rowid DESC`.
3. Require that exact winning row to come from a different session, say
   `reviewed-clean`, and carry refs equal to the incoming result.
4. Require the newest holder-authored `verified` verdict on the producer to carry
   the same refs. Keep the existing results-artifact requirement.

The selector chooses the newest conclusion before it compares revisions. Thus a
newer `changes-requested` always defeats an older clean verdict. A new result
revision invalidates both prior clean and prior verification. Completion remains
blocked until the latest conclusion is an independent clean judgment for the new
revision and the producer records verification for that same revision.

This design does not use `tests-passed` as a freshness token. Repository-defined
verification may include tests, builds, or other checks. The `verified` note and
its existing report artifact retain what ran and what happened; `commitRefs`
identify the result to which that evidence applies.

### 3. Route missing review to accountable orchestration

Keep `completion-requires-review` as a blocking remedy. Replace its automatic
`assign reviewer-code` action with a wake to the accountable opener or owner.
The wake tells that actor which producer, work item, result refs, and missing
judgment blocked completion. That actor chooses spec review, code review, or a
supported correction and opens any review assignment through the ordinary
assignment path.

Resolve the accountable recipient inside the remedy transaction:

1. Read the assignment's `openedBySession` or `openedByUser` and derive the
   opener's user from `sessions.ownerUserId` when needed.
2. If the current `work_items.ownerUserId` differs from the opener's user, route
   to that current owner's Main. This is the changed-owner recovery.
3. Otherwise, route to the active `openedBySession`. If that session is retired
   or unavailable, route to its owner's Main. For a user opener, route to that
   user's Main.
4. If neither an opener nor an existing owner Main is routable, keep completion
   blocked and return the exact unbound recipient. Do not guess a role or create
   a reviewer.

Bind the selected endpoint into the wake row's `sessionKey`. Store the producer
in `assignmentId`, the item in `work_item_id`, and keep the remedy origin. A
historical role binding is not available on the assignment, so a role target
cannot prove opener accountability.

### 4. Dedupe one review need and reconcile delivery

Define a private review-need identity from the rule name, producer assignment,
canonical result-ref digest, and selected accountable principal. Use it for both
the remedy episode and the existing wake idempotency key. This is an internal
key over existing facts, not a receipt or product token.

Store the resulting `wakeId`, rather than the target session, as the wake
episode's `producerKey`. Repeated completion attempts then reconcile the same
wake and its linked turn:

- `pending`, `queued`, or `running`: the notice remains in flight. Do not send
  another notice.
- `delivered`: the notice reached its target. Keep completion blocked until a
  qualifying verdict exists. Delivery does not commission or approve review.
- `canceled` or a known failed delivery without an existing retry: permit one
  deterministic successor for the same need and recipient.
- `failed_unknown`: first query direct review assignments and their opener and
  time rows. If a linked review appeared after the notice started, preserve it
  as observed commissioning and do not retry. If no linked review exists and
  the recipient is unchanged, permit one deterministic notice successor. A
  replay returns that same successor. If that successor also ends unknown,
  surface the wake and turn IDs for owner reconciliation instead of looping.
- changed recipient: preserve the old wake and allow exactly one notice for the
  new accountable principal. If a linked review already exists, do not send it.

Before every bind, schedule, retry, or changed-owner recovery, re-read the
producer assignment and work item in the same transaction. A closed producer or
terminal work item cancels the need and creates no wake. This must compose after
the accepted closed-assignment remedy suppression and WakeRails transaction
predecessor.

Review commissioning is a separate fact: a new assignment row directly linked by
`reviewsAssignmentId` to the producer. The row's `openedBySession` or
`openedByUser` records who commissioned it. Review judgment is another separate
fact: the linked card holder's conclusive verdict. Only the applicable verdict
and current verification can admit completion.

## Deterministic acceptance cases

1. Failing result A has no `tests-passed`. A directly linked reviewer can file
   `changes-requested` with refs A. The producer cannot complete.
2. The producer fixes A into B. A's verdict and verification do not qualify B.
3. An older clean A followed by a newer adverse B cannot qualify A or B. The
   newest conclusive row wins before revision comparison.
4. The producer fixes B into C. A later independent clean C with refs C, plus
   holder-authored verified C and a results artifact, admits completion C.
5. A later `verified` or other non-conclusion verdict on a review card does not
   hide the standing clean or adverse review conclusion.
6. An unlinked, descendant, self-held, user-authored, or wrong-revision verdict
   does not qualify completion.
7. A missing code or spec review creates no reviewer assignment. It creates one
   notice to the accountable opener or current work owner.
8. A fired wake without a turn, or a queued/running turn, is not delivered. A
   `turns.status='delivered'` row proves delivery only.
9. A delivered notice with no linked review remains only notice delivery. A
   directly linked assignment proves commissioning. Its holder verdict proves
   judgment.
10. Ten repeated completion attempts for the same result and recipient return
    one notice need and one wake or deterministic retry successor. They create
    zero automatic reviewer assignments.
11. A `failed_unknown` notice plus an already opened direct review creates no
    retry. A `failed_unknown` notice with no linked review permits one successor;
    repeated reconciliation returns that successor.
12. When the accountable owner changes, the former notice remains historical.
    One notice reaches the new principal unless a linked review already exists.
13. Completion, revocation, retirement transfer, or work-item termination that
    wins before scheduling creates no stale review notice. A terminal transition
    that races scheduling leaves no surviving pending wake.
14. Restart preserves the episode, idempotency row, wake, turn outcome, and any
    retry lineage. Reconciliation after restart creates no duplicate notice or
    review assignment.

## Rejected and unresolved alternatives

The selected 0.1.9 design rejects an automatic reviewer role remedy, a generic
product-owner role target, historical `tests-passed` as freshness, selection by
review-card open time, descendant review inheritance, and a new preliminary
review or acceptance receipt.

An older unmerged candidate added `assignment_review_revisions` and a
`bind-review-revision` verb. The selected design does not carry that schema or
ceremony. Existing verdict and completion `commitRefs` are sufficient for code
acceptance when `verified` can carry the same refs.

One boundary remains explicit: this revision rule is selected for code, the
domain affected by the passing-test admission change. Policy, release, and live
mutation effects keep the existing latest-conclusion rule until their supported
result identity is specified. Do not force a Git commit onto a non-Git live
effect inside this O2 change.

## Future hunk allocation and order

No implementation allocation exists on this design card. The required owner
order remains:

1. Finish and review the late-ruling predecessor.
2. Compose the accepted WakeRails transaction and publication changes.
3. Release one immutable composed predecessor.
4. Allocate exact shared hunks to the remedy/O2 implementation owner.

The future allocation must name these baseline hunks:

- `lib/tightbeam/assignments.ex`: review winner query at lines 321-405; attest
  `commitRefs` validation at lines 1609-1678; new holder-authored applicable
  verification read.
- `lib/tightbeam/dispatch.ex` or the corresponding Gateway normalization seam:
  normalize code completion refs before `Rules.decide/2` at lines 107-149.
- `lib/tightbeam/rules.ex`: expose current result identity to the two applicable
  review and verification facts without changing descendant scope.
- `priv/kungfu/agentic-engineering/rules/engineering.toml`: the separately owned
  guidance producer removes admission and changes the completion remedy from
  automatic assignment to accountable wake. Compose its final reviewed bytes;
  do not edit this hunk from the remedy lane.
- `lib/tightbeam/rail_remedy.ex`: episode claim/re-entry at lines 92-320; wake
  producer identity and liveness at lines 399-439 and 542-584; accountable
  binding context at lines 597-670.
- `lib/tightbeam/gateway.ex`: wake idempotency and response at lines 4307-4354,
  if the composed predecessor does not already provide the required wake ID and
  outcome seam.
- `lib/tightbeam/wakes.ex`: wake/turn outcome lookup and the bounded typed
  failed-notice successor near lines 425-618. Preserve existing rate-limit retry
  behavior and WakeRails custody.

The acceptance query should land before the new rule can remove admission. The
accountable wake path should land only on the immutable WakeRails/remedy
predecessor. The final composed candidate then needs one independent challenge
against all fourteen cases.
