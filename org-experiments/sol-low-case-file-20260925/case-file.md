# Case file: the last completed PDO/PO behavioral evaluation

Prepared September 25, 2026. This is a retrospective evidence file for one run, not standing guidance, a new evaluation, or a finding that a particular model is incapable. The user asked for participant accounts first, followed by an independent Opus 5.5 opinion.

## Questions from the user

Should a PDO rewrite the brief for each child, or should each child receive an authoritative shared work item with a scoped instruction such as "work on part 6"? Why did the agents act as they did in this run? Were they confused by guidance, records, role addresses or something else? The user doubts that broad claims of incompetence explain the behavior. The independent analyst should assess these possibilities and alternatives from the evidence, without taking that doubt or the previous evaluator's grades as the answer.

## Scope and identities

This is the September 24 correction-note fixture, work item `wi_ce29ea6e-f41c-407e-a2de-bd20005c7047`. It completed in 267.203 seconds from intake opening to completion. It is the last completed agent-behavior run identified in the retained experiment record. Later 0.1.9 code tests and guidance reviews are different evidence and are outside this case.

| Participant | Actual original configuration | Original Tightbeam session |
|---|---|---|
| PDO | GPT-5.6 Sol, low, Codex | s_2541a786 |
| PO | Claude Opus 5.5, high | s_51682b82 |
| Writer | Claude Sonnet 5, medium; default archetype | s_05201de6 |

The identity revision was `312a6e17edaf74545bebd8758cb09fd0d1f2d47d`. This did not test Sol 6. Original seats remain retired. Follow-up interviews resumed copies of saved conversations through their native clients with tools disabled; no org seats, records, staffing or original verdicts were changed. Original work directories had been removed at retirement; saved provider conversations remained. Full interview prompts and invocation receipts are retained so their influence is visible. Interviews are post-hoc explanations, not access to hidden causal reasoning.

## Evidence order

Read primary task, delivered text and visible actions before adopting the evaluator's summary. Exact files and hashes are listed in `evidence-manifest.json`.

1. **E1: original task**: `evidence/clear-prompt.txt`. It contains all three facts, claims A-C, the 180-word limit, no-probe/no-code bounds, credential restriction, intent and role-addressed opening.
2. **E2: actual output**: `evidence/engram-fixture-correction-note.md`. Preserve its wording; do not silently correct it.
3. **E3: durable records**: `evidence/work-item-result.json`, `work-item-trace.json`, `consultation-attests.json`, `po-result-attests.json`, `intake-attests.json`, `writer-attests.json`. The work item had a title and no spec reference carrying the facts. Assignment subjects named obligations. Inspect rather than assume what those references made retrievable.
4. **E4: original public provider traces**: `evidence/pdo-public-trace.jsonl`, `po-public-trace.jsonl`, `writer-public-trace.jsonl`. These retain original source line numbers, timestamps, public prompts, replies, tool calls and tool results. Private reasoning blocks are excluded. Compact call/reply indexes are `s_2541a786-audit.json`, `s_51682b82-claude-audit.json`, `s_05201de6-claude-audit.json`.
5. **E5: instructions at the time**: `evidence/s_2541a786-developer.txt` is the retained PDO received context. `evidence/identity-312a6e17/` contains historical role, shared, model and team-design source. Source bytes alone do not prove every participant attended to them. `installed-tightbeam-dispatching-SKILL.md` is accompanied by `dispatch-skill-match.json`, checking its full text against the PDO's original tool result. Use that receipt before attributing a current installed copy to the run.
6. **E6: original interviews**: `evidence/pdo-interview-prompt.txt`, `pdo-interview-answer.md`, `po-interview-prompt.txt`, `po-interview-answer.md`. The original PO interview explicitly points out the absolute wording. Its acknowledgment is therefore prompted, not an independent catch. No original writer interview existed.
7. **E7: new follow-up interviews**: `interviews/{pdo,po,writer}-prompt.txt` and `*-answer.md`, plus `verification.json` and invocation receipts. All three completed before commissioning the independent analyst. They used their original model families/settings. The new PO and PDO qualify some of their earlier causal claims; do not flatten those qualifications.
8. **E8: prior evaluator assessment**: `evidence/eval-report.md`. This is an assessment to audit, not primary evidence of intent, causation or model ability. `delivery-metrics.json` and `turns-timeline.json` support timing. The original report's tool batch counts use different units across clients and are not directly comparable token or latency measurements.

## Observed sequence to check against primary evidence

The PDO read its transcript and the dispatching skill, consulted the addressed PO, received a topology decision, and then spawned one temporary writer. The PDO did not author the note. No additional orchestrator was created for this small prose task. Those are positive results of the role split.

The PO's first reads found an assignment subject and a work item title without the supplied facts. It retrieved the PDO transcript. The PO then specified one writer, required the supplied brief and restrictions to be transferred verbatim, and said it would judge the result. Its message to the PDO included: "Wake me with the note path and sha256 when it is ready."

The PDO's writer handoff included references, the word bound and restrictions but omitted the source facts and claims. The writer queried its assignment, work item and own transcript, tried a constructed PDO session address that did not resolve, then read the actual PDO transcript. It found the facts there. This observed retrieval resolves the PDO's retrospective uncertainty about possible implicit context inheritance for this particular run: the trace shows explicit recovery. It does not establish that all child sessions lack inheritance in every situation.

The writer produced 159 words. Claim A's correction includes "Nothing is copied to a coordinator in advance." The supplied facts say local indexes and tapes remain on each machine, SSH queries run locally, and whole-tape centralization is not required by the stated intent. Whether the output improperly broadens that statement, and how the surrounding claim affects its reading, should be judged independently.

The PO's criteria included "no central copy". Its later approval checked for invented security, protocol or performance details and approved the note. The PO acknowledged the unsupported absolute when the original interviewer pointed to it. The chronology establishes these statements, not which one psychologically caused another.

Both the initial PO consultation and writer assignment omitted effect classification and became code work. Completion required a review. The agents did not invent review evidence. They used progress records and replacement coordination/evidence assignments; the original PO consultation ended surrendered with its delivered decision recorded. A second PO judgment assignment duplicated judgment already present on the first. The PDO polled during its running turn while messages queued.

The writer sent completion and the card issue directly to the PO. Its own later scheduled wake explicitly labeled `product-owner:engram-sol-low-eval-20260924` as the PDO. The follow-up writer interview says it acted on the PO's "Wake me" instruction found in the PDO transcript and encountered a failed PDO address lookup. The actual failed call was a transcript lookup using a constructed session key, not a failed wake to the proper PDO role. Preserve that distinction when judging whether the office was unreachable or misunderstood.

The PO did not invoke the team-design skill in its recorded calls. It initially said the case looked obvious. In the follow-up it correctly distinguishes that retrospective explanation from the absence of a recorded contemporaneous reason. Its later suggestion to compare two conditions changes several variables at once; the analyst should assess the usefulness and confounds rather than adopt it automatically.

## Current tool and record boundaries relevant to the question

The original installed CLI exposed a work-item title and optional spec reference plus hash, not a general work-item body field. Assignments had subjects and advisory file lists. An artifact or specification can carry complete content and be referenced; this case did not establish such a brief before delegation. Do not assume a desired richer work item already existed, or assume a new database feature is necessary when an existing readable artifact may suffice. The actual distinction to examine is task content availability and stable authority versus repeated paraphrasing, not simply long versus short messages.

A role-addressed intake message also contains instructions that are not task facts for every child. Assess the benefit and risks of verbatim transfer, paraphrase, scoped pointers and transcript retrieval without treating any representation as automatically correct. The user has not authorized new permanent guidance or product changes in this diagnostic request.

## Limits

This is one short fixture with mixed models, one task and an evaluator-designed intake. It cannot establish a general model capability ranking or a causal attribution to effort level. Participant recollection can rationalize. The two original interviews were directed by known observed errors. The new interviews mention the user's shared-record hypothesis, so they are not blind. The independent analyst is a fresh Opus 5.5 session, not the original PO, and receives all three accounts only after those accounts are complete. Recommendations remain proposals; do not describe an unrun comparison as validation.
