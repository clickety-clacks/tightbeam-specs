# Learning from Tightbeam changes

Proposal, 8 September 2026. This document answers Mike's request to record what we theorize, change and observe so future agents can evaluate it and improve the system again. It proposes a working practice using existing specifications, release history and execution records. It installs no evaluator, changes no rail and creates no new worker reporting gate.

## Operating model

Choose a testable version using the best available judgment. Record its hypothesis before deployment. Establish what was actually used, inspect the resulting work, and record whether to keep, revise or reverse the change. Link the next attempt to the previous one. Lack of post-change evidence is expected before a first trial; it is not a reason to defer choosing the trial. Mechanical correctness and a concrete implementation still need verification.

The unit is a meaningful product/design change, not every commit, agent turn or receipt. Several commits may implement one hypothesis. Several hypotheses may ship together. Preserve that grouping so future agents do not attribute a package's result to one isolated rule without evidence.

## One discoverable change record, with linked evidence

Keep a short learning ledger for each release experiment in the canonical specs repo, linked from its release plan and the relevant governing specs. Use stable identifiers, such as H019-01, so code changes, release notes, observation reports and later decisions can refer to the same hypothesis. Ordinary workers need the ask and applicable local facts, not the ledger in every prompt.

Each entry answers six questions:

1. What failure prompted this change? Record the intended protection or benefit, concrete examples and the baseline evidence. Include Mike's corrections and earlier attempts, especially when the proposed change removes a rule with a useful original purpose.
2. What do we believe will improve, and why? State the predicted behavior, the competing risk and what would count against the hypothesis. Distinguish a demonstrated source defect from a theory about agent behavior.
3. What are we trying? Name the actual guidance, kungfu rule, substrate mechanism or combined change. Link the chosen design and implementing commits. Record deviations from the proposal, other changes shipping alongside it and its reversal path. Until chosen, label candidate treatments as proposed.
4. Who actually experienced it? Record release/code version, actual loaded rule and guidance versions where observable, participating agent/model/harness versions, scope and exposure dates. A published release, an edited identity file and an agent actually running those instructions are different facts. Mark unknown or mixed exposure explicitly.
5. What happened? Link a representative set of completed, failed, abandoned and still-open cases, relevant trace/query snapshots, actual user or production outcomes, and evidence gaps. Keep evidence that contradicts the hypothesis. Do not count only successful completions or volunteers.
6. What did the responsible agents conclude? Record a dated, scoped judgment: supported, mixed, contradicted or inconclusive. Explain the evidence, uncertainty, harms and next action. Keep, revise or reverse is an agent decision within existing authority. Link the next hypothesis/version and the next review point when a question remains.

Start with a concise hypothesis and references. Delivery and evaluation fill in the later answers when those facts exist. Do not require agents to fabricate a complete experiment report before work can begin. Revise working details normally, but preserve dated decisions, exposure records and assessments; corrections identify what they supersede. Git history supports this, while explicit links make the important lineage understandable without reconstructing every commit.

## Responsibilities

The Tightbeam PO owns whether the changes deliver the product properties Mike intends and sets the review priority. Its orchestrator commissions implementation, observation and focused domain analysis, using existing assignments, messages and wakes. Domain owners interpret findings within their responsibilities and challenge the composition. The author of a change should not be the sole judge of its success; the supervising agent uses independent evidence and actual outcomes.

The orchestrator arranges a review at deployment. For this initial 0.1.9 trial, propose a first review one week after the first confirmed exposure, with earlier attention to a material regression. This is a scheduling choice for this trial, not a new systemwide gate or fixed quota. Review whatever evidence exists then; if the sample is weak, record inconclusive and choose a useful next review. Do not wait indefinitely for enough successful cases. An unavailable owner triggers ordinary ownership recovery.

## Evidence without another paperwork process

Reuse execution, assignment, artifact, review, wake, denial and deployment records. Store the relevant query or extraction version, time window and retained evidence snapshot with the assessment so later agents can reproduce the reasoning after the live state changes. Preserve report/artifact bytes as well as links. Ask agents to record judgments that cannot be inferred, such as why a broader specification was necessary, in their existing brief or decision record.

Collect product outcomes alongside process costs. For comparable kinds of asks, examine elapsed time to a usable outcome, actual rework and escaped defects, unnecessary spec/review effort, avoidable escalation, missed PO influence, and unfulfilled waits. Separate active work from provider outages or unrelated dependency delay when the data supports it. Counts of assignments or reviews are signals to inspect, not universal limits or automatic quality scores.

Classify cases by the ask, uncertainty and consequences, not by the light/heavy label the agent selected. Otherwise the system grades its own classification. Use a small independently examined sample to establish whether additional process was useful. Include both a routine repair and a small but consequential change. Known severe regressions need attention even if an average improves.

Compare with representative pre-change cases when available, and report selection differences, model changes, other released features and unequal exposure. A controlled rollout or matched replay can improve attribution when practical; it is not a mandatory new experiment platform. With a bundled release, judge the combined behavior first, then investigate which changes explain it. Do not call a before/after association causal proof.

Missing observations remain missing. The pinned b299 dispatch code appends denial records through a best-effort path, and the recent audit did not establish live cached rule or hook versions. The implementation should name any minimal instrumentation needed to evaluate a hypothesis. No denial row is not proof no denial occurred. A missing counter is not zero. Record capture gaps and avoid comparisons whose denominators cannot be established.

## Initial 0.1.9 hypotheses to record

These are starter entries derived from revision 15 of the churn plan. They are proposed treatments, not claims that anything has shipped or that every replacement design has been selected.

| ID | Theory and candidate treatment | Evidence for success and against it |
| --- | --- | --- |
| H019-01 | Explicit proportionate orchestration, a usable small-fix path and removal of heavy-by-default wording reduce overprocessing. Replacing the two mandatory posture-token gates is a candidate whose exact design still needs selection. | Understood repairs finish without needless spec cycles; consequential small changes still receive adequate scrutiny. Compare actual quality, time and unnecessary work. A label disappearing alone is not success. |
| H019-02 | Timely, owned PO review opportunity can protect product spirit better than the blanket historical-token dispatch gate. | New specs and relevant changed results reach the PO before affected commitments; corrections influence delivery; preparation proceeds. Lost messages, stale judgments or missed intent defects count against it. |
| H019-03 | Early linked review and orchestrator-selected specialist review improve delivery without weakening acceptance. | Useful findings arrive sooner; review matches the output; known failures and stale evidence do not produce false clean acceptance. Track both review overhead and escaped defects. |
| H019-04 | Agent-chosen diagnosis from recurrence evidence avoids redundant recon while retaining adequate investigation. | Evidence-only prior completions stop forcing diagnosis; recurring bugs still get causal investigation where needed. Faster repeated guesses or unresolved recurrence count against it. |
| H019-05 | Fewer unchanged reminders with obligation-specific waiting and bounded reconsideration reduce churn without losing work. | Useful outcomes resume with fewer repetitive interruptions; threatened commitments, failed delivery and unavailable owners receive attention. Silence alone is not success. Preserve Wake Rails' approved contract. |
| H019-06 | Narrowing harmless Git-command refusals preserves custody with less obstruction. | Harmless unstaging succeeds; supported destructive forms remain protected. Test the protected and permitted actions, not just denial counts. |
| H019-07 | Concise, consistent guidance plus the corresponding enforcement changes improves ownership and delivery. | Agents carry authorized outcomes with fewer redundant permission requests and less ritual, while supervisors retain intent, evidence and quality judgment. Separate this package effect from claims about any one sentence. |

The selected treatment for each entry must be stated before its actual exposure. An unselected posture mechanism is a design choice to make, not a requirement to produce future trial data before trying it. Record the original posture purpose even if the selected treatment retires the token gate.

## Example: the posture experiment

Problem: agents have put small understood bugs through full specification/review cycles. Light/heavy posture was introduced to prevent this. The current predicates accept either token, while guidance defaults uncertainty to heavy.

Hypothesis: making proportionate execution an explicit orchestrator responsibility, removing that default and preserving the direct small-fix path can reduce unnecessary process without increasing substantive defects. Candidate gate changes remain part of the treatment to select and record.

Compare an understood checkout-depth CI correction, a one-line authorization change and work with actual architectural uncertainty. Record the chosen work, why extra process was useful where invoked, time to usable outcome, failures/rework and the independent assessment of adequacy. Do not classify the authorization change as light merely because its diff is small, or the CI correction as heavy merely because it touches infrastructure.

A first assessment might be mixed: routine repairs became simpler, but uncertain tasks were expanded too slowly. That would justify refining escalation of consequential uncertainty, not declaring the entire philosophy false or reinstating every old gate. This is an illustrative possible finding, not observed data. The actual assessment must cite real cases and preserve contrary findings.

## Relationship to existing self-tuning work

`self-tuning-rails-core-FUTURE.md` sections 6e-6g already discuss versioned guidance, production/user evidence and remedy rates. Retain the link between changes and outcomes, and the requirement for evidence beyond agents agreeing with one another. A first implementation of this learning practice does not require that future autonomous tuning system.

Do not use falling remedy rate as the definition of success. Removing a rail mechanically removes its remedies; agents can also avoid a troublesome action altogether. Less enforcement activity may mean improvement, missing protection or stalled work. Read it alongside comparable outcomes, process cost, lost attention and real defects. No metric automatically rewrites policy or grants implementation authority.

## Next concrete step

Create the 0.1.9 learning ledger from these entries when selecting the candidate design. Attach the implementation and exposure records as delivery happens, appoint the PO/orchestrator review responsibility, and schedule the first review through existing mechanisms. Capture a representative baseline before exposure where possible. If a baseline cannot be reconstructed, record that limitation and still evaluate the trial honestly. The next review produces a small set of justified changes and links them back to the prior evidence, repeating this same process.
