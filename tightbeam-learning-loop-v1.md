# Learning from Tightbeam changes

Proposal, 8 September 2026. This document answers Mike's request to record what we theorize, change and observe so future agents can evaluate it and improve the system again. It proposes a working practice using existing specifications, release history and execution records. It installs no evaluator, changes no rail and creates no new worker reporting gate.

## Operating model

Ship the best-supported product design we can establish for people to use. Record why we chose it, implement it coherently, review it and verify its acceptance requirements before release. The later external forensic review tests our expectations against actual use and informs the next version. It is continuous product improvement, not permission to ship an incomplete design and wait for users to discover whether it works.

Distinguish three claims: the design is well justified; the implementation meets its release requirements; actual use supports the predicted improvement. Source analysis, domain judgment and pre-release verification support the first two. Later operational evidence informs the third. Do not demand future usage evidence before selecting a design, or use its absence to lower the release bar.

The unit is a meaningful product/design change, not every commit, agent turn or receipt. Several commits may implement one hypothesis. Several hypotheses may ship together. Preserve that grouping so future agents do not attribute a package's result to one isolated rule without evidence.

## One discoverable change record, with linked evidence

Keep a short learning ledger for each release in the canonical specs repo, linked from its release plan and the relevant governing specs. Use stable identifiers, such as H019-01, so code changes, release notes, observation reports and later decisions can refer to the same hypothesis. Ordinary workers need the ask and applicable local facts, not the ledger in every prompt.

Each entry answers six questions:

1. What failure prompted this change? Record the intended protection or benefit, concrete examples and the baseline evidence. Include Mike's corrections and earlier attempts, especially when the proposed change removes a rule with a useful original purpose.
2. What do we believe will improve, and why? State the predicted behavior, the competing risk and what would count against the hypothesis. Distinguish a demonstrated source defect from a theory about agent behavior.
3. What are we changing? Name the actual guidance, kungfu rule, substrate mechanism or combined change. Link the chosen design and implementing commits. Record deviations from the proposal, other changes shipping alongside it and its reversal path. Until chosen, label unselected changes as proposed.
4. Who actually experienced it? Record release/code version, actual loaded rule and guidance versions where observable, participating agent/model/harness versions, scope and exposure dates. A published release, an edited identity file and an agent actually running those instructions are different facts. Mark unknown or mixed exposure explicitly.
5. What happened? Link a representative set of completed, failed, abandoned and still-open cases, relevant trace/query snapshots, actual user or production outcomes, and evidence gaps. Keep evidence that contradicts the hypothesis. Do not count only successful completions or volunteers.
6. What did the external assessment find, and what did the responsible agents decide? Record a dated, scoped judgment: supported, mixed, contradicted or inconclusive. Explain the evidence, uncertainty, harms and next action. Keep, revise or reverse is an agent decision within existing authority. Link the next hypothesis/version and the next review point when a question remains.

Start with a concise hypothesis and references. Delivery and evaluation fill in the later answers when those facts exist. Do not require agents to fabricate a complete outcome report before work can begin. Revise working details normally, but preserve dated decisions, exposure records and assessments; corrections identify what they supersede. Git history supports this, while explicit links make the important lineage understandable without reconstructing every commit.

## Responsibilities and external forensics

An external forensic evaluator is the primary assessor of Tightbeam's whole-system changes. Its execution, instructions, schedule and ability to finish must not depend on the workflow or gates being evaluated. It reads authorized retained snapshots, the hypothesis ledger, actual deliverables and user/production outcomes. Independent placement does not guarantee unbiased judgment or complete evidence; the assessment still exposes contrary cases, provenance and gaps. Do not make a Tightbeam completion verdict a prerequisite for issuing the forensic report.

Tightbeam records and runs the work. Its PO owns product intent and responds to the findings with Mike where his judgment is needed. Its orchestrator delegates any internal evidence preparation and focused domain responses, synthesizes their implications for the PO, and carries authorized corrections into delivery. It does not become the investigator or test executor, or control the external evaluator's conclusion. Domain owners can challenge the report with evidence. Preserve the external findings and the subsequent product decision separately, including disagreements. Ordinary internal supervision continues to handle ongoing work.

Arrange external evaluation ownership during delivery. Mike subsequently authorized an installer follow-up seven days after verified Gibson 0.1.9 installation. That installation timestamp anchors this initial reminder, superseding the earlier proposed exposure-based reminder date. The analysis still records actual exposure separately for each change and materially different agent group; installation does not prove a week of relevant use. Reuse deployment/runtime evidence rather than introduce per-agent exposure receipts. If evidence is weak, conduct the review and record inconclusive or not-yet-exposed findings with an owned next step. Do not postpone the installation follow-up until enough successful cases accumulate. Material regressions can engage review earlier.

Close each bounded evaluation with the evidence available, a dated judgment and an owned next action. An inconclusive evaluation can be complete; it does not establish that the change improved outcomes. Keep promised observation or delivery obligations owned separately. An external evaluation has its own bounded responsibility and retained report. Any supporting work inside Tightbeam uses an existing or successor bounded assignment. Do not keep fulfilled delivery open solely for a separate follow-up evaluation, or retroactively expand its contract. If evaluation was part of the original promised outcome, that requirement remains. Recover unavailable ownership through the responsible owner; the external evaluation cannot rely solely on Tightbeam waking its own evaluator.

## Engagement and the authorized installer follow-up

Mike proposed an unassigned work item as the durable future-review record. An external patrol can inspect due review obligations and take responsibility for a forensic run; the item alone does not trigger execution. Reuse that work record rather than introduce a separate scheduling registry. The external patrol/engagement path has not yet been implemented or scheduled by this proposal.

Mike then authorized the installer requirement recorded by the ClipMesh agent as `wi_0c8ebb58-ac04-4353-8ff9-d435e64c1e28`, titled "0.1.9 installer: schedule a follow-up wake seven days after verified Gibson installation". The Tightbeam PO recorded acceptance under `asg_e07250bb-b653-4310-a6cb-ffd223b22e39`. That bounded routing assignment subsequently surrendered after confirming no authorized installer had been identified. Main then closed the original item and preserved its unmet requirement in iceboxed successor `wi_cb0a4962-9f07-420e-92eb-26686454d249`, as confirmed in Main transcript turn 124270. Reuse that successor when installer custody exists. The requirement is prepared but is not bound to an installer. This corrects the earlier open-item status report. Canonical acceptance is `tightbeam-019-install-followup-acceptance.md`. This item records installer work, not evidence that a seven-day review wake exists. Its current planning scope is preserved.

The eventual authorized installer directly schedules an absolute-time wake at the verified installed-and-running timestamp plus 604800000 milliseconds. A fallback-after duration on a fact watch would start at watch creation, so it would not express this requirement. No new installation-fact convention is needed. Preserve one follow-up per verified installation, with immutable anchor, target, due time and returned wake ID; reconcile uncertain scheduling outcomes before retry. Scheduling failure remains visible and retryable without falsifying installation verification.

Recipient disposition by the external lead: address the review reminder to Mike with `--user mike`, asking to begin the external forensic review and linking the learning ledger and installation evidence. The release/install owner remains responsible for getting the reminder scheduled. ClipMesh's earlier release-owner recipient was an agent assumption, not Mike's direction. The lead sent the correction to the existing PO owner in immediate wake `w_52b48854-1590-4f1d-9124-86befae1a7ac`; this is not the future seven-day wake.

A Tightbeam wake provides a notification, not an external evaluator or gateway-down delivery guarantee. Preserve the due obligation and evidence in durable linked records readable from outside the evaluated workflow, so an external patrol can detect missed engagement. That independent trigger/recovery capability remains an implementation gap; the installer follow-up alone must not be reported as completing it. No external scheduler, installation, service-power action or future-dated wake was created by the lead's reconciliation.

## Evidence without another paperwork process

Reuse execution, assignment, artifact, review, wake, denial and deployment records. Store the relevant query or extraction version, time window and retained evidence snapshot with the assessment so later agents can reproduce the reasoning after the live state changes. Preserve report/artifact bytes as well as links. Ask agents to record judgments that cannot be inferred, such as why a broader specification was necessary, in their existing brief or decision record.

Collect product outcomes alongside process costs. For comparable kinds of asks, examine elapsed time to a usable outcome, actual rework and escaped defects, unnecessary spec/review effort, avoidable escalation, missed PO influence, and unfulfilled waits. Separate active work from provider outages or unrelated dependency delay when the data supports it. Counts of assignments or reviews are signals to inspect, not universal limits or automatic quality scores.

Classify cases by the ask, uncertainty and consequences, not by the light/heavy label the agent selected. Otherwise the system grades its own classification. Use a small independently examined sample to establish whether additional process was useful. Include both a routine repair and a small but consequential change. Known severe regressions need attention even if an average improves.

Compare with representative pre-change cases when available, and report selection differences, model changes, other released features and unequal exposure. A controlled rollout or matched replay can improve attribution when practical; it is not a mandatory new evaluation platform. With a bundled release, judge the combined behavior first, then investigate which changes explain it. Do not call a before/after association causal proof.

Missing observations remain missing. The pinned b299 dispatch code appends denial records through a best-effort path, and the recent audit did not establish live cached rule or hook versions. The implementation should name any minimal instrumentation needed to evaluate a hypothesis. No denial row is not proof no denial occurred. A missing counter is not zero. Record capture gaps and avoid comparisons whose denominators cannot be established.

## Initial 0.1.9 hypotheses to record

These release design records accompany revision 16 of `tightbeam-019-agent-judgment-plan.md`. They state the intended improvements and competing risks. They do not claim shipped implementation or observed success. The full plan distinguishes selected behavior from remaining engineering design and validation.

| ID | Design rationale and change | Evidence for success and against it |
| --- | --- | --- |
| H019-01 | Explicit proportionate orchestration, a usable small-fix path and removal of heavy-by-default wording reduce overprocessing. Selected: remove both mandatory posture-token vetoes with that guidance, ordinary recorded proportionality grounds and supervisor accountability. Preserve focused verification and independent review; underscoping consequential uncertainty is the competing risk. | Understood repairs finish without needless spec cycles; consequential small changes still receive adequate scrutiny. Compare actual quality, time and unnecessary work. A label disappearing alone is not success. |
| H019-02 | Timely, owned PO review opportunity can protect product spirit better than the blanket historical-token dispatch gate. | New specs and relevant changed results reach the PO in time to influence the affected decision, and its disposition reaches the resulting spec/work; preparation proceeds. Notification delivery alone is not success. Lost messages, stale judgments or missed intent defects count against it. |
| H019-03 | Early linked review and orchestrator-selected specialist review improve delivery without weakening acceptance. | Useful findings arrive sooner; review matches the output; known failures and stale evidence do not produce false clean acceptance. Track both review overhead and escaped defects. |
| H019-04 | Agent-chosen diagnosis from recurrence evidence avoids redundant recon while retaining adequate investigation. | Evidence-only prior completions stop forcing diagnosis; recurring bugs still get causal investigation where needed. Faster repeated guesses or unresolved recurrence count against it. |
| H019-05 | Fewer unchanged reminders with obligation-specific waiting and bounded reconsideration reduce churn without losing work. | Useful outcomes resume with fewer repetitive interruptions; threatened commitments, failed delivery and unavailable owners receive attention. Silence alone is not success. Preserve Wake Rails' approved contract. |
| H019-06 | Narrowing harmless Git-command refusals preserves custody with less obstruction. | Harmless unstaging succeeds; supported destructive forms remain protected. Test the protected and permitted actions, not just denial counts. |
| H019-07 | Concise, consistent guidance plus the corresponding enforcement changes improves ownership and delivery. | Agents carry authorized outcomes with fewer redundant permission requests and less ritual, while supervisors retain intent, evidence and quality judgment. Separate this package effect from claims about any one sentence. |

Record the implementing commits, applicable acceptance evidence and actual release exposure for each selected change. Preserve the original posture purpose alongside the decision to retire its token gates. A later finding of improvement is separate from pre-release engineering acceptance.

## Selected design and delivery links, 8 September 2026

These links extend the hypotheses above without replacing their original rationale. They identify design and evidence stages, not release exposure.

- H019-01, H019-02, H019-04 and H019-07: [complete guidance composition](tightbeam-019-guidance-composition-2026-09-08.md), selected through specs e88f8e6. This includes the role guidance, shared manual, elected procedures and conflicting automatic enforcement doctrine. The replacement source producer holds `asg_4f49f573`; implementation and composed acceptance remain pending.
- H019-03: [recovered O2 design and required corrections](tightbeam-019-o2-recovered-design-assessment-2026-09-08.md), specs 9f309e8. The archived draft offered current-code identity and accountable review routing. Review found that absence of a review row does not prove safe replay, a historical review row does not prove capable ownership, and immutable identity normalization needs actual implementation. The successor must correct those issues and preserve reuse of still-applicable verification. The recovered draft is not accepted implementation.
- H019-05: [selected reminder policy](tightbeam-019-reminder-policy-2026-09-08.md), specs 13c42ad, and [implementation design](tightbeam-019-reminder-design-2026-09-08.md), amended at specs 3da18f5. Unchanged successful-notice gaps are 5, 15, 30 and then 30 minutes. Source assessment changed the initial one-column assumption: immutable consequence data also needs a typed payload on existing condition facts. Recovery correlation must support both existing successor wakes and explicit successor turns. These changes retain the product theory while correcting unsupported implementation assumptions. No R1 implementation or usage outcome is established by these selections.
- H019-06: existing G1 work `wi_d3f86caa` receives the harmless-unstaging amendment in the [work reconciliation](tightbeam-019-work-reconciliation-2026-09-08.md). The parser/classifier owner must preserve nested-command and destructive-data protections; no separate regex implementation or accepted final hook exposure is claimed.

The separate cadence wiring correction supports H019-05 but does not implement its reminder backoff. Independent local review `att_6bf3d547` accepted base `926774a3` plus patch `58617021b3715b2e35e851e0a2a84580f05c97ba9752809d43977f1c8d483728`. The added retirement regression passed six focused tests. The earlier full 1855 Mix and 296 Rust results belong to patch `885c5c70`, whose product bytes were unchanged by that test addition. These are local patch-level results, not final release integration or evidence that agents churn less. Preserve the report and hashes through the existing cadence item `wi_c737aee7`.

The [release inventory](tightbeam-019-release-inventory-2026-09-08.md) records included work, other-line exclusions, reusable consumer evidence and the final candidate acceptance requirements. The [work record](tightbeam-019-work-records-2026-09-08.md) retains recovery and handoff history. Failed or unknown turns and superseded source custody remain evidence of the old system's behavior; they must not be counted as exposure to the proposed replacement guidance. Fill in actual implementing commits and installed/loaded exposure only when verified.

## Example: the posture design decision

Problem: agents have put small understood bugs through full specification/review cycles. Light/heavy posture was introduced to prevent this. The current predicates accept either token, while guidance defaults uncertainty to heavy.

Hypothesis: making proportionate execution an explicit orchestrator responsibility, removing that default and preserving the direct small-fix path can reduce unnecessary process without increasing substantive defects. The selected design removes both token gates with the composed guidance changes. Exercise the contrasting acceptance cases before release; retain actual outcomes for later external assessment.

Compare an understood checkout-depth CI correction, a one-line authorization change and work with actual architectural uncertainty. Record the chosen work, why extra process was useful where invoked, time to usable outcome, failures/rework and the independent assessment of adequacy. Do not classify the authorization change as light merely because its diff is small, or the CI correction as heavy merely because it touches infrastructure.

A first assessment might be mixed: routine repairs became simpler, but uncertain tasks were expanded too slowly. That would justify refining escalation of consequential uncertainty, not declaring the entire philosophy false or reinstating every old gate. This is an illustrative possible finding, not observed data. The actual assessment must cite real cases and preserve contrary findings.

## Relationship to existing self-tuning work

`self-tuning-rails-core-FUTURE.md` sections 6e-6g already discuss versioned guidance, production/user evidence and remedy rates. Retain the link between changes and outcomes, and the requirement for evidence beyond agents agreeing with one another. A first implementation of this learning practice does not require that future autonomous tuning system.

Do not use falling remedy rate as the definition of success. Removing a rail mechanically removes its remedies; agents can also avoid a troublesome action altogether. Less enforcement activity may mean improvement, missing protection or stalled work. Read it alongside comparable outcomes, process cost, lost attention and real defects. No metric automatically rewrites policy or grants implementation authority.

## Next concrete step

Use these entries as the initial 0.1.9 change ledger. Link implementing commits and pre-release acceptance evidence as delivery proceeds, then record actual exposure. Arrange an external evaluation owner and an internal owner for responding to findings. Capture a representative baseline where possible. Missing baseline evidence limits later attribution; it does not excuse missing release verification. The next review recommends a small set of justified changes and links them to the prior rationale and evidence.


## Review lineage

Rowan's `d2c8b26f-8778-4a55-ad68-fd9fbed6b656` clarified bounded evaluation completion, treatment-specific exposure and actual PO influence. Orchestrator Editor's `005d6086-3103-4b62-8b40-31f139ce3f5a` clarified delegation, exposure groups and separation of fulfilled delivery from later evaluation. Mike then challenged the internal-evaluation premise; the lead revised the proposal to external primary forensics, retaining useful internal support and product accountability. The earlier internal-owner model is superseded.

The orchestration contribution recommends selecting removal of the two posture-token vetoes together with the positive small-fix path, with underscoping consequential uncertainty as the counter-risk. The lead selected that composed approach after Mike challenged the earlier loss of purpose. This records the release design choice and its rationale, not empirical proof or implementation authority.
