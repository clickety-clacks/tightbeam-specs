# The corrected work-item eval

The agents completed the job from a properly populated work item. The PDO asked the PO for the staffing plan, followed it, and delegated the writing. The PO accepted the 121-word result, and all assignments and the work item closed.

Both the PO and worker read the job through the work item's linked spec. The worker confirmed it did not need another agent's conversation to understand the task. This run gives us no reason to add a separate briefing process.

## What was different

I put the complete job in the work item's specification reference before dispatch. I read the reference back and verified the file and its hash. The spec contained the facts, draft claims, word limit, deliverable and scope restrictions.

The existing `spec-dispatch-requires-spirit` rule refused the first delivery dispatch until the PO approved that spec. I obtained the PO judgment and retried the same dispatch. The PDO then sought the staffing decision before hiring the writer. No guidance was changed for these temporary agents during the run.

The run used the installed 0.1.8 build 1343 and identity revision `8a61fd3`. It is not a test of the unpublished 0.1.9 alignment changes.

## Who did the work

| Responsibility | Archetype | Model |
| --- | --- | --- |
| Delivery | PDO | Sol 6 low |
| Product judgment and staffing plan | Product owner | Opus 5.5 high |
| Writing the note | Coder | Terra 5.6 high |

The PO chose one writer and no additional orchestrators. It said the coder role fit a file produced against an accepted contract. It chose Terra from the installed model guidance because it considered Luna max excessive for the small writing task.

That choice does not demonstrate compliance with the user's newer preference for version 6 models. The served guidance still included the older fallback. The PDO used the PO's selected model and did not substitute its own choice.

## What worked

The worker received the exact spec path, its hash and the correct PDO reporting address. It sent the result to that PDO. The note corrected all three draft claims and stayed under the 180-word limit.

The note says queries do not require every satellite to copy its tape collection centrally. It avoids the earlier unsupported claim that nothing is copied. It also requires source-and-tape identification and makes an unavailable source visible as incomplete coverage.

The PDO stayed out of producing the note. When a delivery problem needed a change to the plan, it asked the PO and followed the returned revision. The PO confirmed that it found no unapproved plan changes.

## What still caused extra work

The writer's assignment defaulted to code because the PDO omitted its work type. That triggered code-test and code-review requirements for a documentation note. The PO's plan had not named a work type either.

The agents recovered without inventing tests or review evidence. The PO revised the plan, the PDO revoked the misclassified assignment and opened an evidence assignment, and the worker completed that assignment using the already accepted file. No rewrite was needed.

The PDO also opened an extra delivery assignment to record a required posture verdict after a staffing refusal. In its interview, it said it could have checked whether the existing delivery assignment could hold that verdict. It spent much of its first turn waiting and checking for the PO's decision, the note and acceptance; incoming messages queued behind that turn.

The writer initially reported the assignment complete before its completion filing succeeded. It corrected the notice after the refusal. The final records distinguish the produced document from the completed assignment.

## Result and limits

The run took 7 minutes 23 seconds from the initial PO spec-review assignment through final assignment closure, or 5 minutes 46 seconds from successful delivery dispatch. It finished September 24 at 8:05 PM PT.

I read the note and collected all three agents' explanations before retiring the temporary sessions. The note, task, interviews and work records are preserved below.

This is one successful delivery with recoverable coordination mistakes. It establishes that these agents could get the complete job through the work item and follow the PO/PDO split in this run. It does not establish that every entry point, model or larger task will behave the same way.

The newly requested invariant-preservation guidance was not active during this run. Its author has added the sentence to the shared manual candidate and matching live candidate; review and publication are separate work still in progress.

## Evidence

- [Complete task](task.md) and [delivered note](engram-correction-note.md)
- [Work item before dispatch](work-item-before-dispatch.json) and [final work item and assignments](work-item-result.json)
- [PDO interview](interviews/pdo-answer.md), [PO interview](interviews/po-answer.md), [worker interview](interviews/worker-answer.md)
- [Initial spec approval](spec-approval-attests.json) and [result acceptance and repair decision](result-review-attests.json)
- [Run configuration](run.json), [agent roster](eval-roster.json) and [turn records](turns.json)
- [Authorized invariant-guidance request](invariant-guidance-request.md)
