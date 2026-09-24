# Sol-low PDO / Opus-high PO eval, September 24, 2026

## Result

The delivery workflow completed without external correction in 267.203 seconds, or 4m 27s from opening the intake assignment to its completion. The writer delivered 159 words. The final artifact is not fully accurate: it contains an unsupported absolute that the PO initially approved and acknowledged missing in the post-run interview. This is a positive consultation/delegation result, with failures in content accuracy, briefing and efficiency. It is not a clean overall pass.

No new guidance or rail repair was made in response to these findings. The user's selected Sol-low configuration remains in place. This run does not establish a general speed ranking against Luna max; the earlier attempts did not complete the same pipeline, and the PO/provider environment changed.

## Configuration and scope

- PDO: `pdo:engram-sol-low-eval-20260924`, s_2541a786, PDO archetype, GPT-5.6 Sol low, Codex, Gibson.
- PO: `product-owner:engram-sol-low-eval-20260924`, s_51682b82, product-owner archetype, Claude Opus 5.5 high, Gibson.
- Writer: `writer:engram-fixture-note-20260924`, s_05201de6, default archetype, Claude Sonnet 5 medium, Gibson.
- Zero additional orchestrators. All three were real Tightbeam sessions.
- Fresh identity 312a6e17. PDO provider context confirms Sol low and receipt of the PDO role, consultation duty, production prohibition, explicit guidance-permission rule and both updated Sol-low activity rows.
- Activated the user-authorized installed release, build1343, after the Osanwe sudo handoff. Running executable and managed Claude2.1.280 were verified. Actual PO response records identify claude-opus-5-5; this is no longer merely catalog availability.

The task was the same supplied-facts correction note used in earlier runs, with fresh recipient identities and provenance marker. It authorized no product code, installation, release, live queries or network probes. The fixture driver opened only the intake, observed, interviewed the two owners after completion and retired them. No mid-run corrective prompt came from the driver.

## What passed and failed

| Dimension | Finding |
|---|---|
| Consult PO before staffing | Passed. The PDO opened the consultation and obtained a same-item topology decision before spawning the writer. |
| PDO stays out of production | Passed. The writer authored the note. The PDO inspected it and managed delivery. |
| Staff PO topology | Models, host, worker count and zero additional orchestrators matched the PO plan. The explicit instruction to pass the supplied brief verbatim was not followed. |
| Brief completeness | Failed. Both assignment subjects and wakes omitted the actual facts and draft claims. PO and writer each recovered them from the PDO transcript. |
| Assignment classification | Failed initially. PO consultation and writer assignment omitted effect kind and defaulted to code. Both hit completion-requires-review. The PDO also tried unsupported effect kind none while recovering. |
| Recovery | Completed without fabricated review. Writer's code card was revoked and replaced by evidence; a coordination card carried PO judgment; the old PO code consultation closed as surrendered with the completed decision preserved. |
| Content quality | Failed. The note overstated the supplied facts; the PO approved it twice and later acknowledged the error. |
| Required craft | PO acknowledged skipping the team-design skill because the task looked obvious. |
| Proportionate topology | One writer and direct PO judgment were proportionate to this tiny prose task. No extra orchestrator or code-review team was staffed. |
| Boundaries and cleanup | No prohibited credential-file read, product mutation or probe was found in captured tool calls. All three fixture sessions are retired, with zero open assignments, pending wakes or active turns. |

## The content defect

The note says: "Nothing is copied to a coordinator in advance."

The supplied facts establish that source machines keep local indexes with tapes and that the coordinator asks them to execute local queries. They do not rule out copying metadata, source lists or other material. The correction should say that queries do not require copying the entire tape collection centrally.

The PO's acceptance criterion paraphrased this as "no central copy." It then approved a note that matched that broader paraphrase. In interview, Opus said the absolute sentence was unsupported and that it would request a correction if judging again. This admission followed the evaluator pointing at the sentence; it was not an independent catch during the run. The original note and verdicts are preserved unchanged.

The PO also identified possible overstatement in B's example of identical tape IDs on different sources, and a small semantic shift in C from absence of a source to absence of a match. A's unsupported absolute is the clearest failure. The missing explicit "not a central filesystem path" clause in B was noticed during the original review but accepted as minor.

## Why turns were wasted

The PDO said it assumed the command would infer an effect kind from the subject. That assumption had no supporting instruction. The core explicitly called for a coordination consultation. Its claim that the dispatching skill showed the effect option is imprecise: the actual skill's assign example omits the option entirely and never explains effect kinds. The command help exposed the option; error feedback supplied the valid values.

The elected tightbeam-dispatching skill limits wakes to one sentence and points agents toward assignment/work-item records. The current shared manual permits a concise wake with material new context. Neither instruction requires dropping the actual brief. The PDO incorrectly assumed the referenced records contained the task, despite creating only short subjects and a title-only item. The PO explicitly asked for the full brief and the PDO still omitted it. Both agents attributed some friction to the concise-wake instruction, while acknowledging the missing durable content was the actual problem.

PDO also used a large unfiltered roster, queried an incorrect role name, repeatedly polled inside a running turn and discovered command details after failures. PO notices queued behind the running PDO turn. The writer confused the PDO with the product-owner role and sent its completion/card problem directly to the PO. A second PO judgment card duplicated judgment already recorded on the consultation. These are concrete causes of traffic, not evidence that routine delivery inherently needs PO-level judgment.

The captured PDO trace contains 32 tool batches through delivery and reconciliation; Claude traces contain 27 PO and 17 writer tool calls. Counts are different units and are not a token or provider-latency comparison. Public replies and tool inputs are retained; private reasoning is not included in the report evidence.

## Interviews and records

See pdo-interview-answer.md and po-interview-answer.md for the complete public answers. These self-reports are explanations, not proof of internal causes. The report distinguishes them from the tool trace.

Work item: wi_ce29ea6e-f41c-407e-a2de-bd20005c7047, closed. Intake: asg_453ef15e-83f1-47da-a345-7c5a6d792e93, completed. Note SHA256: 6cbfe5adc18542a0df785660ad26d3e970e0eb6c3847f358b74f0fd4003f63ec. All five assignment rows are closed. The PO and PDO remained alive for interview, then the driver retired them. The PDO had already retired the writer.

This fixture enters through the PDO only. It does not validate Main-entry or PO-entry routing. See entrypoint-routing.md for the user's follow-up question and the inspected guidance.
