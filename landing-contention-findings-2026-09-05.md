# Landing contention: findings for the orchestration review

Status: findings, not a spec. Recorded 2026-09-05 at Mike's instruction so the
orchestration-and-rails overhaul, whenever it happens, starts from evidence
rather than from memory. Nothing here is a ruling. Measured on the live Gibson
org against branches `0.1.9` and `main` of clickety-clacks/tightbeam.

## The observation

Through early September the org's dominant cost was not building and not
reviewing new work. It was re-reviewing work it had already approved, because
the branch moved underneath it.

Measured over 4-5 September:

| Measure | Value |
| --- | --- |
| Assignments opened org-wide, 48h | 544 |
| Of those, review assignments | 467 (86%) |
| Refusals to land recorded as "LAND NEITHER" or base drift | 90 |
| Distinct sessions performing landing-related actions | 83 |
| Review assignments on one card (vocabulary purge) since 4 Sep | 19 |
| Recomposition rounds reached by several cards | 10 |
| Commits to `0.1.9` in the same 48h | 32 (about one per 90 min) |

A single small fix, the remedy-loop repair, went through ten rounds of
compose, review, lose-the-base, recompose.

## Why it costs so much

The mechanism is ordinary: someone merged, so update your branch before merging
yourself. Every active repository does this. What makes it expensive here is the
price of an update.

Verdicts in this org are bound to an exact commit. The recorded form is
"reviewed-clean for exact SHA", and the rails read it that way. Rebase onto a
new tip and the verdict no longer covers the code, so the lane must open a fresh
independent review held by a different session, and re-run the hosted gates.

In an ordinary repository a rebase costs a CI re-run. Here it costs a full
review cycle. When the branch moves faster than a review cycle completes, lanes
with any competition cannot converge: they re-review faster than they can land.

Some lanes already compute and compare patch identities across the rebase and
prove the change itself is unaltered. The verdict must still be re-filed against
the new SHA, so that proof buys nothing today.

## Why this is orchestration, not engineering

Three facts, all checkable:

1. **The substrate already has the primitive and it has never been used.** Table
   `critical_leases` carries `sessionKey`, `reason`, `startedAt`, `expiresAt`,
   `hardDeadline`. That is a landing lock. It held zero rows on 2026-09-05 and
   shows no history of use.

2. **One orchestrator independently built the right answer.** The stall-fix
   recovery owner (`s_c71f88da`) runs what its own attests call a *serializer*:
   it allocates a base commit to a producer, and when the branch moves it
   verifies the move is a true fast-forward from the allocated base and lets the
   lane continue, instead of forcing a recomposition. Roughly 42 attests
   reference the pattern. Example wording, 2026-09-05 07:48 UTC: "resume
   singular producer asg_f8b1d034 on execution-time main 439121fb. Serializer
   s_c71f88da verified this is a true fast-forward from allocated base."

3. **Nothing carries it to anyone else.** No guidance makes landing order an
   orchestrator's duty. No work item exists for landing serialization, a merge
   queue, or contention. Eighty-three sessions therefore each hold a private
   opinion about the tip, and every lane without a serializer thrashes.

The gap is not capability and not judgement. Each orchestrator is told to drive
its own lane to completion; no rail says what to do when two lanes want the same
branch. Coordinating a shared resource is nobody's stated job.

## Two candidate fixes

Recorded as options, not recommendations. Both were put to Mike on 2026-09-05.

- **Bind the verdict to the change, not the tip.** A clean rebase whose patch
  identities are unchanged carries its existing verdict forward; only the hosted
  gates re-run against the new SHA. Substrate and rails change. Removes the cost
  rather than the collision, and helps every future lane.
- **Serialize landing.** One lane at a time holds the right to land against a
  stationary base, using `critical_leases` or the serializer pattern above.
  Policy and guidance change, no substrate work required. Removes the collision
  rather than the cost.

They are complementary. The second is available immediately; the first is the
durable fix.

## Where to look when the overhaul starts

- `critical_leases` in the schema: unused mutual exclusion, ready to adopt.
- Session `s_c71f88da` attests: the working serializer prototype and its wording.
- `stall-watchdog-kit.md`: the comparable case of a duty that was written down
  once and then spread by being handed to fresh agents.
- `0.2-orchestrator-handoff.md`: current orchestrator norms, which do not
  mention shared-resource contention.
