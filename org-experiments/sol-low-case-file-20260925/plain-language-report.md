# Why the agents got tangled up

The best next test is to put the complete task in one shared document, then give each worker a link and a short instruction about its part. That is Opus's main recommendation, and I agree with it.

The PDO tried to use short instructions in this run. The problem was that the work item it pointed to did not contain the task. The other agents had to search its conversation to find out what to do. That search also exposed instructions meant for someone else.

This page retells the independent Opus 5.5 review in plain language. It includes corrections from checking the records. The original report and interviews are linked below.

## What we tested

The task was small: correct three false statements about Engram in no more than 180 words, using only the supplied facts. It required no code changes.

The September 24 run used Sol 5.6 low as PDO, Opus 5.5 high as PO, and Sonnet 5 medium as the writer. It took about four and a half minutes. This was not a test of Sol 6.

I asked all three agents about the run using copies of their saved conversations. A fresh Opus 5.5 high session then read their answers and the original records. Their recollections help explain the choices, but the recorded actions matter more when the two disagree.

## The PDO pointed to a task that was not there

The work item had a title, but no complete task or linked specification. The assignments were also too short to explain the work.

The dispatching skill told the PDO to keep its message to "AT MOST ONE SENTENCE" and point the worker to the existing records. That advice assumed those records contained the task. The PDO did not check.

The PDO said it expected the work item and originating conversation to provide the missing context. In practice, both the PO and writer had to search the PDO's conversation for the facts.

The PO had explicitly told the PDO to pass the full brief to the writer. The PDO failed to do that. The incomplete records help explain the failure; they do not excuse ignoring that instruction.

A short handoff can work, but only if its link leads to the complete task.

## The writer followed a message addressed to the PDO

While searching the PDO's conversation, the writer found a message from the PO: "Wake me with the note path and sha256 when it is ready."

The PO had sent that instruction to the PDO. The writer treated it as an instruction for itself and sent the result to the PO. It also called the product-owner role "the PDO." Its own assignment had not told it whom to report to.

The writer's explanation fits those recorded actions. My earlier description made this sound like a deliberate attempt to bypass the PDO. The evidence supports confusion about the recipient instead.

There was no demonstrated failure to reach the PDO. The writer used a wrong address for one transcript lookup, then successfully read the right conversation. It never tried sending the result to the correct PDO address.

This is why the shared task should contain the facts and requirements, while each worker gets a separate instruction naming its job and reporting destination.

## Tightbeam treated a question and a writing task as code work

The PDO left out the assignment's work type. Tightbeam defaulted to code, so completing these assignments required a code review even though no code was involved.

The guidance referred the PDO to a skill for choosing the work type. That skill did not explain it. Command help showed an optional setting without explaining its default or valid choices.

The PDO said it assumed Tightbeam would infer the right type. It did not. Repairing the assignments added two more records and extra coordination.

The immediate proposal is to explain the default and the available choices where agents already look. Opus also suggested making the choice mandatory. That is a separate product decision.

## Polling delayed messages and helped create duplicate paperwork

The PDO spent about 90 seconds sleeping and checking for progress during one long turn. Messages from the PO waited until that turn ended.

It also opened another PO judgment assignment without checking the latest result on the first one. The PO had already recorded its judgment 11 seconds earlier.

My earlier description said the PO approved the result twice. More precisely, it recorded the same judgment in two places. These were not two independent checks.

Some automatic reminders arrived only seconds after assignments opened. That deserves investigation, but this case does not establish whether the timing was a bug.

## The PO accepted a sentence that claimed too much

The supplied facts said queries did not require copying the whole tape collection to a central machine. The writer turned that into:

> Nothing is copied to a coordinator in advance.

That is a stronger claim. The facts did not say that nothing could be copied.

The PO's own checklist used similarly broad wording, and it approved the sentence. The writer had not read that checklist, so it did not get the wording from the PO. Both agents appear to have broadened the original fact separately.

The PO acknowledged the problem after an interviewer pointed it out. It did not catch it during the review. The practical lesson is to check the result against the supplied facts themselves, not just a paraphrased checklist.

## What worked

The PDO asked the PO for the staffing plan before hiring anyone. The PO chose one writer and no extra orchestrators, which suited the small task. The PDO followed that staffing choice and did not write the note itself.

The writer recovered the facts and produced a 159-word note. The PDO checked its length and file hash. When Tightbeam demanded a code review, the agents repaired the assignments instead of inventing a review.

The PO skipped a required planning skill, but its staffing choice agreed with that skill. This run shows a missed instruction; it does not show that reading the skill would have changed the outcome.

## What I would try next

Use the existing document and specification links to try one complete shared task document. It should contain the facts, constraints, expected result and acceptance criteria. Each worker should get its part, output location and reporting destination. Instructions meant only for the PDO should stay separate.

A link alone is not enough. The document must exist, identify the version to use and be readable by the worker. File access between sessions on the same machine worked here. Access between machines was not tested.

Then repeat the same task with the same models and settings. Compare a task supplied only in a message with one also stored in that shared document. Handle work types the same way in both versions, so we can tell whether the document helps. Count missing facts, searches through other agents' conversations, messages sent to the wrong agent and unsupported claims.

One run cannot tell us whether the PDO needs a smarter model. It does give us specific problems to fix or test before making that judgment.

These are recommendations. This case study has not changed guidance or software, and no new behavior test has run.

## Original interviews and records

- [The PDO's explanation](interviews/pdo-answer.md)
- [The PO's explanation](interviews/po-answer.md)
- [The writer's explanation](interviews/writer-answer.md)
- [Original task](evidence/clear-prompt.txt) and [delivered note](evidence/engram-fixture-correction-note.md)
- [Full Opus report, unchanged](opus-opinion.md)
- [Detailed case file](case-file.md) and [corrections to the report](reader-note.md)
- [Review model and tool verification](opus-review-verification.json)
