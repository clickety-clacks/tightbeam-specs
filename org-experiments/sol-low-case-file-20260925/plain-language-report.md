# I set up the handoff test incorrectly

In Tightbeam, the job belongs in the work item. I created this work item with only a title and sent the full instructions to the PDO in a separate message. There was no task description or linked specification for the other agents to read.

That was my setup error. I then judged the agents as though I had supplied a complete work item. The run does not tell us whether they handle a properly created work item correctly.

I withdraw the recommendation to add a separate shared brief or more handoff process based on this run. The next valid test should encode the job in the work item using Tightbeam's existing mechanism, then exercise that normal flow.

The original records and Opus report remain linked below. This correction replaces the earlier recommendation and my attribution of the missing instructions mainly to the PDO.

## What we tested

The task was small: correct three false statements about Engram in no more than 180 words, using only the supplied facts. It required no code changes.

The September 24 run used Sol 5.6 low as PDO, Opus 5.5 high as PO, and Sonnet 5 medium as the writer. It took about four and a half minutes. This was not a test of Sol 6.

I asked all three agents about the run using copies of their saved conversations. A fresh Opus 5.5 high session then read their answers and the original records. Their recollections help explain the choices, but the recorded actions matter more when the two disagree.

## What my setup made the agents do

The work item I created had a title, but no complete task or linked specification. I sent the facts, correction requirements and restrictions separately to the PDO through the eval runner.

The dispatching skill told the PDO to keep its message to "AT MOST ONE SENTENCE" and point the worker to the existing records. I had failed to put the job in those records.

The PDO said it expected the work item and originating conversation to provide the missing context. Both the PO and writer searched the PDO's conversation for the facts. That search describes their recovery from my incomplete input. It does not demonstrate a failure of the intended work-item handoff.

## The writer followed a message addressed to the PDO

While searching the PDO's conversation, the writer found a message from the PO: "Wake me with the note path and sha256 when it is ready."

The PO had sent that instruction to the PDO. The writer treated it as an instruction for itself and sent the result to the PO. It also called the product-owner role "the PDO." Its own assignment had not told it whom to report to.

The writer's explanation fits those recorded actions. My earlier description made this sound like a deliberate attempt to bypass the PDO. The evidence supports confusion about the recipient instead.

There was no demonstrated failure to reach the PDO. The writer used a wrong address for one transcript lookup, then successfully read the right conversation. It never tried sending the result to the correct PDO address.

This happened while the writer was recovering instructions that I had left out of the work item. We cannot use it to conclude that a worker given a complete work item would make the same mistake.

## Tightbeam treated a question and a writing task as code work

The PDO left out the assignment's work type. Tightbeam defaulted to code, so completing these assignments required a code review even though no code was involved.

The guidance referred the PDO to a skill for choosing the work type. That skill did not explain it. Command help showed an optional setting without explaining its default or valid choices.

The PDO said it assumed Tightbeam would infer the right type. It did not. Repairing the assignments added two more records and extra coordination.

Those tool and guidance observations remain in the record. They are separate from the missing task, and do not establish a need for another task document or briefing stage.

## Polling delayed messages and helped create duplicate paperwork

The PDO spent about 90 seconds sleeping and checking for progress during one long turn. Messages from the PO waited until that turn ended.

It also opened another PO judgment assignment without checking the latest result on the first one. The PO had already recorded its judgment 11 seconds earlier.

My earlier description said the PO approved the result twice. More precisely, it recorded the same judgment in two places. These were not two independent checks.

Some automatic reminders arrived only seconds after assignments opened. This case does not establish whether the timing was a bug.

## The PO accepted a sentence that claimed too much

The supplied facts said queries did not require copying the whole tape collection to a central machine. The writer turned that into:

> Nothing is copied to a coordinator in advance.

That is a stronger claim. The facts did not say that nothing could be copied.

The PO's own checklist used similarly broad wording, and it approved the sentence. The writer had not read that checklist, so it did not get the wording from the PO. Both agents appear to have broadened the original fact separately.

The PO acknowledged the problem after an interviewer pointed it out. It did not catch it during the review. That wording error is visible in the delivered note, but it does not validate my test of the handoff process.

## What worked

The PDO asked the PO for the staffing plan before hiring anyone. The PO chose one writer and no extra orchestrators, which suited the small task. The PDO followed that staffing choice and did not write the note itself.

The writer recovered the facts and produced a 159-word note. The PDO checked its length and file hash. When Tightbeam demanded a code review, the agents repaired the assignments instead of inventing a review.

The PO skipped a required planning skill, but its staffing choice agreed with that skill. This run shows a missed instruction; it does not show that reading the skill would have changed the outcome.

## What the next test needs to establish

First, create a complete work item through Tightbeam's existing process. Confirm that reading it gives the agents the job, including its facts and constraints. Then give the PDO that work item and evaluate whether it consults the PO, follows the staffing plan and delegates the assigned parts correctly.

That is the normal flow we meant to test. My incomplete setup prevented this run from answering that question. It provides no basis for requiring another document, adding briefing steps or deciding that the PDO needs a smarter model.

This correction changes the report. No new behavior test has run, and it adds no guidance or software changes.

## Original interviews and records

- [The PDO's explanation](interviews/pdo-answer.md)
- [The PO's explanation](interviews/po-answer.md)
- [The writer's explanation](interviews/writer-answer.md)
- [Original task](evidence/clear-prompt.txt) and [delivered note](evidence/engram-fixture-correction-note.md)
- [Original Opus report, preserved with the correction above](opus-opinion.md)
- [Detailed case file](case-file.md) and [corrections to the report](reader-note.md)
- [Review model and tool verification](opus-review-verification.json)
