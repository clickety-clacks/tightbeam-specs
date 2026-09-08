# Tightbeam 0.1.9 churn repair plan

Review revision 16, 8 September 2026. Gibson Codex, Subetha identity `gibson-codex-stalls-20260908a`, edits this revision under Mike's instruction to propose product refinements, accept feedback and make document changes. Kestrel edited revision 06. The canonical backing document is `tightbeam-019-agent-judgment-plan.md` in the specs repository. It records the proposed release design and selected product direction; it does not claim implementation or release readiness.

Reference target: `b299457d5c95dd6e161ed9b1de70b4450b5166b7` on `0.1.9`. Source references below name that tree, not main or the running Gibson release. Canonical remote verification established this branch tip when planning began. Later branch movement requires checking the affected conclusions, not restarting the discussion.

Status: revisions 06 through 15 and their judgments or feedback are preserved separately. They do not endorse these revised bytes. This revision incorporates Mike's product direction and participant feedback; judgments on it are recorded separately. Mike confirmed on 8 September that Wake Rails is already blessed. This document neither withdraws that approval nor asks for it again. Its pinned source comparisons describe engineering provenance, not a current product deficiency or a new approval gate. The current task authorizes document discussion and edits; it adds no implementation, staffing, release, installation or runtime authority and does not revoke authority already granted elsewhere.

## Intended result

Agents should carry an approved feature through ordinary implementation, testing, review and delivery without asking Mike to approve each internal step. They should respect actual product and operator restrictions. When execution fails, the responsible agent should see what failed and what action remains possible. A legitimate dependency wait must not provoke invented work or repeated permission requests.

The repair should guide decisions and expose useful evidence. It should not add a new authority registry, acceptance handshake, mandatory announcement row, automatic reassignment policy, or stronger enforcement merely to make agents appear active.

### Governing direction and guidance scope

The canonical operating principle is `tightbeam.md`, "Operating principle: trust, record, and agent judgment", in the shared specs repository. Agents own outcomes and supervise one another at their respective scopes. Tightbeam supplies coordination, communication, recorded accountability and responsibility, with reliability as the prodder's role. Wake Rails is already blessed.

Assume competent agents. The replacement guidance below states the ask, authority and Tightbeam-specific facts. It does not reteach professional practice. Mike's example is "Meter cyclomatic complexity", without explaining the metric. Local tools, thresholds and exceptions remain useful when relevant. The evidence and acceptance cases in this document are reference material for the repair, not additional runtime instructions.

The earlier consensus report is background, not the engineering design. Open work-item titles do not prove that their implementation is missing from this target. Code delivered to 0.1.9 is not necessarily available in the installed release, and neither fact alone settles an agreed multi-line delivery commitment.

## Release commitment and implementation scope

0.1.9 is a release for people to use. Choose the best-supported design now, implement it coherently, and establish release readiness through appropriate engineering review and verification. The later external forensic review improves future decisions; it does not substitute for pre-release acceptance or justify shipping known unresolved defects. Agent behavior remains a prediction until observed, but that uncertainty does not excuse an incomplete implementation.

This plan includes more than guidance and rails configuration:

- Guidance: authority, proportionate work, concise local instructions, PO intent opportunity and outcome ownership.
- Engineering kungfu rules and tool rails: the named admission/remedy changes, preserved completion protections and narrowed harmless Git refusal. These are policy changes executed by the substrate, not all new substrate features.
- Proposed additional substrate work: separate supervision scan cadence from the no-progress interval, and implement the reminder behavior described in section 4. The full reminder schedule and response to changed consequences still need concrete design. Missing-review routing and early-review acceptance may also require code after inspection of the supported paths; deleting a TOML predicate alone does not establish truthful current acceptance.
- Existing approved implementation: reconcile Wake Rails and retain the already-delivered failure/retry behavior. Do not count these as newly invented mechanisms or reimplement them from this document.

The source inventory is pinned to b299 and the named candidate. It is not a fresh comparison with today's 0.1.9 branch. The delivery owner must map each selected behavior to current implementing commits and remaining work before presenting an incremental code scope. No new registry, schema or timer per agent is prescribed by the learning practice.

Backing records: `tightbeam-learning-loop-v1.md` records the design rationale and later external evaluation; `tightbeam-019-install-followup-acceptance.md` specifies the existing installer follow-up item. The installer item does not own all engineering changes in this plan.

## 0. Change conflicting enforcement with the guidance

Mike identified the missing premise in the previous assessment: existing rails can still refuse the work regardless of improved guidance. This revision therefore includes the rules and hard-coded checks agents encounter. The canonical companion is `tightbeam-019-enforcement-assessment-2026-09-08.md` in the shared specs repository. It records the complete shipped engineering rule/rail inventory, configured local-file comparisons, bounded substrate checks, domain evidence and the proposed dispositions.

The lead inspected b299 source objects and the three configured identity rule/rail files read-only. The bundle declares eight active dispatch rules and five tool guards. Configured files are not proof of gateway-cached rules or generated session hook coverage. No code, identity files or runtime state changed, and no source tests ran.

### Proposed enforcement changes

- Remove `implementation-requires-posture` and `implementation-dispatch-requires-posture` as part of the selected proportionate-work design. Preserve their original purpose: an understood fix uses the existing ask, correction, focused verification and proportionate independent review. Replace heavy-by-default and blanket light-path ceremonies across the guidance homes below. Record useful grounds in the ordinary delegation brief; supervisors challenge excessive process and inadequate scrutiny. A posture token demonstrates neither. Selection is based on the existing light path, source findings and domain review; validate the composed implementation before release and evaluate actual outcomes after use.
- Replace `spec-dispatch-requires-spirit` with supported, timely PO review opportunity and supervision. The existing gate blocks any spec-backed dispatch, including preparatory work, while accepting historical verdicts without current intent qualification. Mike's purpose remains essential: the PO owns product spirit and can correct a specification itself. New or materially changed specs, and other work raising intent questions, must reach the PO in time to influence the result. The replacement needs visible delivery, accountable disposition and recovery when the PO cannot act; merely removing the gate is insufficient. Explicit governing holds remain.
- Retire count-triggered `refix-requires-diagnosis`. Its b299 fact counts all completed unlinked assignments, so completed evidence work can trigger mandatory recon before a first repair. The orchestrator judges recurrence evidence and commissions diagnosis when useful.
- Preserve applicable independent-review protection at consequential completion, but replace `completion-requires-review`'s automatic reviewer-code staffing with routing to the accountable orchestrator for suitable independent review. Exact supported routing remains an implementation-design obligation.
- Retire blanket `code-review-requires-passing-tests` admission as a policy proposal, allowing useful linked review before tests pass. Preserve producer linkage, independent judgment and truthful current evidence at clean acceptance and consequential delivery. The implementation design must inspect the acceptance consumers; moving a historical token check is insufficient. The earlier recon finding remains valid but did not settle this broader sequencing question.
- Preserve verification and durable-results protections while assessing their coarse verdict/artifact proxies for valid evidence reuse and retention. No blanket removal of these two completion rules is proposed.
- Narrow the documented `no-git-restore` harmless-unstaging overmatch while preserving protection against destructive loss of another agent's work. Verify supported syntax and harness behavior before selecting the matcher change.

These are proposed rule/mechanism changes, not instructions to evade current refusals. Do not substitute a new receipt ceremony for the removed labels. The b299 rule engine does not support a predicate `notice` effect; useful reminders must use supported communication/supervision or a specifically designed addition.

### Preserve proportionate work without a new ceremony

The orchestrator chooses the amount of process. `feature-cycle/SKILL.md:22-29` already gives light work a path that skips spec writing, spec review and decomposition, using the input as the specification. Preserve that useful behavior. Replace `orchestrator.md:25-42`'s default to heavy when in doubt with focused investigation and a judgment about the uncertainty and consequences. Supervisors should challenge unnecessary process as well as insufficient care, using existing delegation and results records rather than a mandatory posture worksheet.

Rowan's acceptance pair is decisive: an understood regression restoring agreed behavior is corrected with proportionate verification and independent review, without a fresh spec/discovery cycle; a similarly small patch changing a user commitment gets PO judgment. A small diff alone does not imply low risk. The PO does not select execution posture, and agents should not manufacture a specification just to obtain a spirit judgment. Every actual new spec and material intent question still reaches the PO.

Also replace feature-cycle step 0's blanket statement that every remaining step applies to light work. Select the delivery and review steps that the actual ask and protections require; do not preserve a full ceremony merely after skipping spec creation. Explain the choice when useful in the ordinary assignment brief, without a separate posture card or new required field. The current gates accept either historical light or heavy tokens equally; they cannot establish that the selected work is proportionate.

Acceptance examples: incorrect validation under an existing contract goes directly to correction, focused verification and proportionate independent code review; a one-line authorization change gets scrutiny appropriate to its consequences; novel behavior or architectural uncertainty gets the necessary investigation, specification and PO opportunity. No extra spec or spirit rerun is created solely for ceremony. These are evaluation cases, not a fixed size threshold or proof an ungated alternative works.

Conform the small-fix path across orchestrator, feature-cycle, coder and reviewer guidance. Preserve coder's use of an existing sufficient ask and routing of genuine uncertainty to its orchestrator. Replace the light-review bar of "nothing egregiously wrong" in feature-cycle and "pass unless something is egregiously wrong" in orchestrator guidance with proportionate review against the actual ask and consequences. Light work still requires intended behavior, data integrity and trust-boundary correctness; it does not permit accepting a known contract defect. Scope and depth may be smaller without treating substantive defects as acceptable.

Kestrel's Firehose pair makes that concrete: an understood checkout-depth CI correction needs no new spec cycle merely because it touches infrastructure; a startup system-actor contract question can require product/security judgment even if its final patch is one line. The lead read the cited coder, reviewer-code and feature-cycle passages; the Firehose examples remain attributed domain observations, not reproduced trials.

The selected release design removes both posture-token vetoes with these guidance and supervision changes. This supersedes the earlier unresolved disposition. Pre-release review and validation must cover both routine repairs and consequential uncertainty; future usage data is not a prerequisite for making the design choice. No new label gate, fixed line-count threshold or review quota is proposed.

### Substrate behavior is in scope

Retain attributable lifecycle actions, valid references, idempotency and truthful recovery. The hard-coded checkpoint limits, session-wide suppression and effort-checkin escalation also need to satisfy the reminder policy in section 4. A timer or absence of filings does not judge fulfillment or cancel existing authority.

Wake Rails' approved independent-verifier requirement remains explicit. It is a chosen accountability workflow, separate from tenant/creator/predicate integrity. The proposal does not remove it. Registration needs the accessible open independent-verifier assignment required by the approved contract; gentler prose cannot admit a wait without that dependency.

Acceptance must exercise guidance plus loaded rules, hard-coded checks and projected hooks. Show that authorized preparation and delivery proceed, that the PO can actually influence intent conformance, that supervisors choose appropriate recovery, and that protected actions still preserve authority and evidence. A historical approval token, queued notification or successful prompt reload alone proves none of those outcomes.

## 1. Replace conflicting authority instructions together

### Evidence and present behavior

Kestrel's Firehose notes record ordinary lifecycle notifications escalated as `dr_24c2bae1`, test-clock instrumentation stopped at `att_3e5e7674`, and an E2E helper treated as a new product requiring permission. An existing base authorization, `att_c004debf`, also had to be forwarded before work continued. These are observed permission stalls; the claim that particular wording caused them is an inference supported by the exposed guidance, not a controlled experiment.

At the target:

- `priv/kungfu/agentic-engineering/guidance/scope-and-architecture.md:3-28` defines authority by the card and requires a user HOLD for an incorrect assumed design or architectural repair.
- `priv/kungfu/agentic-engineering/guidance/product-owner.md:38-46` requires another offer and yes for every ready slice.
- The same PO file at `50-57` already requires finished-work carry and prohibits upward bookkeeping requests.
- `priv/kungfu/agentic-engineering/guidance/golden-rule.md:1` broadly says to bypass obstructing rules and apologize later. That is not a safe substitute for a precise authority boundary.
- All seven archetype TOMLs include both golden-rule and scope-and-architecture at lines 6 and 8. A PO-only correction leaves the conflicting shared instruction in every composed archetype.
- `priv/kungfu/agentic-engineering/guidance/coder.md:35-40` treats a spec-required change to existing working behavior as a conflict to report rather than an edit to make, even though an authorized feature can require exactly such a change.

Rowan independently checked the shared and PO conflict at this exact target. Kestrel checked the included fragments and coder wording.

Kestrel's later Firehose review, event `1c913a88-2e9f-4f07-bf6a-7d68704b199f`, supplied the CI reconciliation, separate test-dependency and refusal-routing cases below. Kestrel also reports a bounded search found historical defect-first escalation wording absent from b299's shipped `priv` tree. Any remaining exposure needs inspection of actual composed or local guidance; it is not evidence of another missing branch patch. These are attributed observations, not new source verification by this editor.

### Minimum proposed change

Replace the shared scope fragment with the following governing text. Keep one home for authority and reference it from callers.

> Own the approved outcome within explicit constraints. Treat assignments as divisions of responsibility within existing authority. Correct internal plans with the responsible owner. Discussion or investigation alone does not authorize implementation. Escalate changes beyond the approved outcome or authority; continue separable authorized work.

Replace the blanket golden-rule bypass with a reference to that boundary and a duty to find supported paths within it. Do not preserve "apologize later" as a competing exception.

In PO readiness, retain the four existing discovery criteria. Replace the fresh-yes clause with:

> Dispatch ready, authorized work through your orchestrator. Ask only for missing authority.

In coder's change-only section, distinguish an intentional, authorized change from a contradiction in the governing ask:

> Implement the authorized behavior change. Preserve unrelated behavior and resolve contradictions with the governing ask.

No new authority table or DR type is needed. Generic encouragement would leave the explicit HOLD and fresh-yes instructions and the section 0 gates intact, so it is insufficient. Replace the contradictory included `engineering-tenets.md:5-8` clause alongside scope and coder wording. Also remove its inference that a rejected final step necessarily proves earlier work was skipped. A refusal may instead expose an overbroad rule or malformed evidence admission. Existing mechanisms continue to govern until authorized changes are delivered.

### Acceptance cases

- Before: an approved Firehose E2E run needs a helper, and the agent asks Mike to approve a new client product. After: the owner routes the helper as testing work within the existing outcome and applies proportionate review. A genuinely new shipping client remains a separate scope decision.
- Before: a wrong internal design creates an automatic operator HOLD. After: the responsible technical owner corrects the plan within the approved behavior and coordinates shared ownership. An explicit design restriction still requires its authorized owner to resolve a conflicting change.
- Before: every ready slice asks "shall I start?" again. After: an authorized ready slice starts through its orchestrator; a genuinely unapproved outcome still requires agreement.
- An explicit export refusal, production-install restriction, or proposed product behavior beyond the authorized outcome still stops the affected action. Independent authorized work continues. New behavior within the approved feature is not itself a reason to ask again.
- An authorized Firehose CI correction is reconciled onto a newer base. The owner checks that its purpose and constraints still fit the existing authority and proceeds. A changed hash alone creates no new product decision; explicitly hash-limited authority or a publication restriction still requires resolution by its governing owner. Review applicability remains a separate judgment under section 2.
- A Firehose app-consumer E2E helper runs on an already authorized runbook host while a separate provider-compatibility acceptance obligation remains open. Agent-provider login is not the consumer contract. The owner continues separable authorized implementation and testing while retaining the agreed provider acceptance requirement until fulfilled or changed by its owner.
- An automated refusal stops an action. The owner identifies the governing restriction and responsible decision-maker, resolves within existing authority or escalates the actual change required. The refusal alone does not establish a new product choice. A recovery-actor mismatch, for example, needs truthful attribution and protection against public impersonation; changing that audit contract requires its responsible owner, not a label workaround.
- This planning discussion has an obvious implementation path. The agents still make no implementation or operational changes without the corresponding authority.

## 2. Use existing review and carry mechanisms consistently

### Evidence and present behavior

Firehose ready work at `5eccf6f8` had no linked review when the executive checked; later reviewed work stopped at "owner disposition required". Separately, a reported 2,289-test pass was not admitted because the producer supplied invalid commit references. The later corrected receipt, `att_ff618865`, allowed the existing independent review to finish. Rejected evidence admission was not proof that tests had never run.

At the target:

- `coder.md:131-146` already shows a note-only `tests-passed` receipt and a ready-for-review progress report.
- `coder.md:153-158` contradicts that by saying completion requests review.
- `coder.md:160-165` correctly requires review, verification evidence and integration before completion.
- `priv/kungfu/agentic-engineering/skills/feature-cycle/SKILL.md:56-61,84-89` already uses progress for readiness and says to commission review deliberately, not trigger it by premature completion.
- `priv/guidance/operating-manual.md:79-97` already makes the opener carry finished work under standing line authority or record the precise reason and responsible principal. PO and orchestrator guidance reference this duty.
- `priv/kungfu/agentic-engineering/rules/engineering.toml:53-64` already requires the code author's admitted passing-test receipt before code review.

### Minimum proposed change

Replace coder lines 153-158 with:

> Report review readiness and changed code or interactions through a progress attest. The orchestrator commissions review and judges whether earlier evidence still applies. Complete after the required review, verification and integration.

Preserve the existing truthful tests-passed example and carry duty. Do not add another completion receipt, announcement row, or owner-acceptance handshake. On a current admission refusal, use the supported diagnostic path or correct a malformed record using original evidence. Do not invent a pass. The planned admission and review-remedy changes are specified in section 0.

Clarify the existing carry reference in PO and orchestrator guidance:

> Own the promised outcome through delivery. Use the record to identify the next responsible actor and unresolved result. Preserve completed results and report remaining commitments.

In the PO's own guidance home:

> Route goals through your orchestrator. Own product intent; review relevant specifications and results, correcting specifications themselves when needed. Complete your bounded assignment when agreed delivery and acceptance conditions are met. Report what users can use and what remains.

In the orchestrator's own guidance home:

> Use the existing ask as the spec when sufficient; choose proportionate investigation and review. Delegate investigation, specification and implementation. Give the PO current context and time to influence each new spec and results that may depart from intent; carry its disposition into the work. Commission independent spec or code review as needed. Use recon for independent failure diagnosis; its findings do not count as producer acceptance review. Complete your bounded goal assignment when its promised outcome and applicable delivery conditions are evidenced.

Spirit review uses an existing bounded PO assignment on the work item and a wake carrying the current spec/result reference, intent question and when the answer affects work. Track delivery and disposition; a queued notice is not proof of a useful opportunity. Reuse applicable judgment for unchanged slices. Present every new spec and renew context for changed intent or results. If the previous review assignment is terminal, use a bounded successor rather than inventing a reopen verb. Hold only work depending on an unresolved material intent decision; continue separable authorized preparation. Recover an unavailable PO through its responsible owner.

Conform the once-per-item and before-dispatch absolutes in `product-owner.md` and `feature-cycle/SKILL.md:98-129` with this behavior. The latter's indefinite wait and historical-token wording conflicts with timely owned review. These are named composed-guidance changes, not a new acceptance handshake.

The recovery policy preserves role ownership, previous evidence and unfinished outcomes. Silence alone does not establish that a predecessor stopped; overlapping execution or unknown external effects require reconciliation. This is an engineering acceptance condition, not a mandatory query ceremony for every follow-up.

The PO owns intent, priorities and product acceptance. It assesses the required outcomes using specialist and delivery evidence, rather than replacing specialist judgment with another technical review. It distinguishes branch delivery from installed availability and retains any unmet agreed multi-line commitment. Human acceptance is required when the governing agreement requires it, not as an invented extra gate. PO accountability must not become direct worker micromanagement.

Bounded PO completion requires evidence that its promised outcome is fulfilled. Incidental findings and child bookkeeping do not silently expand that outcome or require every child row to close first. Preserve actual delivery status and route lifecycle conflicts through supported mechanisms. Handing off unfinished required work does not fulfill the promise, and no completion rail is bypassed by this clarification.

### Diagnostic work and clean acceptance

Independent help should be available when code is failing or incomplete. A diagnostic result records findings and limits; completing that investigation does not certify the product as ready. The applicable current evidence still governs a clean acceptance verdict and consequential integration or release.

Orchestrator Editor inspected the existing path at pinned target b299457d, Subetha event `8c6ffa5b-0777-48d0-91a6-613afe9b1df4`. Recon elects bug-provenance and recon-lifecycle. A new evidence/recon assignment on the work item, with the producer revision and diagnostic question in its brief, can investigate failing tests without being the producer's linked acceptance review. The assignment receives no `reviewsAssignmentId` for that producer. Its diagnosis cannot satisfy the producer's reviewed-clean consumer, which selects qualifying verdicts on linked review cards. Recon retains its applicable results-artifact requirement. Merely changing the archetype or label of a linked review does not evade passing-test admission.

Conform `reviewer-code.md`'s "Before judging code" passing-test instruction alongside the proposed admission-rule change. It must allow honest examination of failing code while preserving current verification at clean acceptance. Changing the TOML gate alone would leave the reviewer with a contrary instruction.

This source-backed route meets the original diagnostic-help use case. It does not establish that every formal reviewer should be barred until tests pass. The expanded enforcement assessment now proposes retiring that blanket admission restriction while retaining truthful acceptance and applicable evidence, as section 0 explains. Recon remains a supported current path; no current refusal is bypassed. The prior inspection is Orchestrator Editor's attributed source/test reading, not a fresh execution or installed-behavior claim.

### Acceptance cases

- A linked reviewer examines failing code and records findings or changes requested without inventing a tests-passed receipt. That investigation does not qualify the producer as reviewed-clean or complete. After fixes, applicable current verification and independent review of the changed result support clean acceptance. The latest linked review-conclusion semantics remain: an older clean verdict cannot override newer changes requested. The existing b299 consumer does not itself establish revision freshness or test truth; removing admission alone does not implement these acceptance requirements.
- A producer has real passing-test evidence and a correct readiness report. The owner commissions the required linked review without attempting early completion.
- A malformed receipt is corrected to the target's documented shape. The reviewer uses the admitted original evidence; no invented test pass and no automatic repeat of an unchanged suite.
- A clean review allows the next required authorized delivery action. A real independent publication or acceptance restriction remains visible and blocks only its protected action.
- Reconciliation changes only commit identity, or instead changes interactions that invalidate earlier evidence. The orchestrator distinguishes these cases and obtains fresh judgment where needed. Unchanged intended behavior alone does not prove review remains applicable. Explicit target constraints and agreed landing order remain binding; an operational baseline does not become a new human authorization gate.
- Work has verified 0.1.9 delivery and only a main ruling remains. The PO assesses the intended outcomes using the delivery and specialist evidence, reports actual installed availability, and retains the remaining main commitment if agreed. It seeks only a genuinely outstanding product decision. The orchestrator routes remaining technical work. Human acceptance is not added when the governing agreement does not require it.
- A review task finishes with changes-requested. Its bounded review task may be finished, but the product is not accepted on that basis. A handoff transfers responsibility; it does not fulfill an undelivered requirement.
- A PO's required outcome is evidenced, while an unrelated finding or child bookkeeping remains open. The PO can judge its bounded outcome fulfilled and route those remaining records without declaring an undelivered requirement complete or bypassing an enforced completion rule.

## 3. Declare coordination correctly; preserve producer review

### Evidence and present behavior

Patrol inspected deployed specimen `asg_028f1b7c` and found its durable `effectKind` is `policy`, although the reported remaining duty is coordination after producer completion. Patrol retracts the claim that this example proves a missing coordination exemption.

At the target:

- `engineering.toml:7-26` gates completion for code, policy, release and live_mutation. It already exempts coordination, evidence and review.
- `lib/tightbeam/assignments.ex:374-405`, `qualifying_review_verdict_kinds/3`, selects the latest holder-authored review conclusion among cards whose `reviewsAssignmentId` equals the completing assignment. It then requires a different-session review holder and reviewed-clean.
- `feature-cycle/SKILL.md:62-67` and `orchestrator.md:167-174` already classify by actual effect, not holder role.
- `orchestrator.md:215-221` nevertheless prescribes delivered-not-withdrawn progress plus opener revocation for unlinked evidence-only work. The target regression in `test/rules_test.exs:1299-1346` loads shipped engineering rules, closes an unlinked evidence assignment held by an orchestrator through ordinary dispatch, and denies code completion without review. Kestrel independently read the regression after Patrol identified it. It proves this narrow exemption, not removal of every completion requirement.
- `priv/kungfu/agentic-engineering/rules/verification.toml:2-18,49-64` retains coder verification and results-artifact checks for coder, reviewer-code, reviewer-spec, spec-writer and recon holders. Evidence classification does not waive those applicable requirements.
- `orchestrator.md:204-207` describes selection as the latest linked card's latest verdict. The implementation actually pools holder-authored review-conclusion verdicts across linked cards. Other verdict kinds are ignored. This is a prose correction, not a missing query implementation.

### Minimum proposed change

Move the existing effect-classification instruction to the assignment-creation decision, rather than leaving it only at review time. Declare genuinely coordination-only ownership as coordination. If the owner assignment itself delivers authoritative policy or code, it remains review-required. Do not reclassify a real policy deliverable merely because its only remaining action is closing the record.

No broader descendant-review inheritance is justified. A producer's review does not automatically review another assignment's different output. Do not silently rewrite existing effect rows. Any existing mislabeled assignment needs an independently verified supported disposition; no repair verb is assumed here.

Replace the blanket unlinked-work revocation instruction with:

> Classify the assignment by its actual effect. Complete fulfilled coordination or evidence work through ordinary completion, subject to applicable checks. On refusal, inspect the recorded effect and named rule; use a supported correction without losing delivery evidence.

Correct the review-selection description to match `qualifying_review_verdict_kinds/3`: choose the latest holder-authored review-conclusion verdict across all linked review cards, then require a different-session holder and reviewed-clean. Do not replace this with the newest card regardless of its verdicts or broaden it to unrelated descendant reviews.

### Acceptance cases

- A correctly declared coordination-only owner completes its actual promised coordination outcome without duplicate code review or a blanket diversion to revocation. Applicable evidence and other completion requirements still apply.
- A policy or code producer without its own qualifying linked review still cannot complete.
- Closing a linked review preserves its judgment. A later changes-requested verdict is not erased by selecting an older clean result. Unrelated later verdict kinds do not replace the latest qualifying review conclusion.
- An existing policy-labeled owner is inspected for its whole promised output, not just its final bookkeeping step. Agents preserve prior evidence and use only a supported disposition.

Patrol retains ownership of the deployed specimen. Kestrel independently read the target exemption and review query. The historical closed/superseded `wi_032f11a6` and 0.2-only completion-rails design are not authority for a new 0.1.9 subsystem.

## 4. Separate real waiting from repeated activity

Firehose recorded prods claiming missing continuation after accepted wakes `w_2c34b6db` and `w_7cdb2d92`. This demonstrates a historical mismatch, not that the same mechanism remains absent from the target.

There is a separate source-level guidance conflict at the target:

- `orchestrator.md:102-133` and `skills/unblocking/SKILL.md:8-22` reduce every sweep to advancing or ending work and treat unchanged state as a stall.
- `unblocking/SKILL.md:34-48` groups all external conditions with human decision needs, then prescribes a fresh one-hour recheck.
- `orchestrator.md:115-120` and `feature-cycle/SKILL.md:155-157` mandate rollback after two attempts without distinguishing useful experiments from repeating the same failed approach.

Proposed replacement policy. This changes the current unconditional two-attempt rollback and fresh hourly recheck policy; it is not merely a wording correction. No such policy change is applied by this draft:

> Keep each waiting obligation covered by its valid Wake Rails subscription, naming the resolver and resolving evidence. Registration needs an accessible open independent-verifier assignment. Reuse healthy coverage; route a delivery or suppression failure to its owner. Correct invalid coverage through the supported path. Recover unavailable ownership and continue independent work. An attempt count alone does not require rollback.

An accepted pending wake is not proof of delivery. Legitimate waiting and eligibility for prod suppression are different questions. The producer must create the actual resolving evidence; repeated status receipts do not resolve the dependency. The orchestrator routes production and resumes the dependent action when qualifying evidence arrives. The PO retains outcome ownership through that orchestrator and reports the product impact, without managing subscriptions itself or adding an acceptance handshake.

### Reminders support a decision

A prod should state the unmet expectation, the relevant evidence and any changed consequence. The accountable agent chooses recovery, rerouting, other authorized work or continued justified waiting. It does not owe a new activity receipt solely because a reminder arrived. Missing or invalid wait evidence receives an actionable explanation; claiming to wait does not fabricate admitted coverage or resolving evidence.

Reduce repeated reminders when both the relevant evidence and consequence are unchanged. Preserve the next bounded reassessment and renew attention when resolving evidence arrives, a commitment is threatened, the owner cannot act, or another material consequence changes. An unchanged blocker approaching an agreed delivery date has a changed consequence. Activity on another obligation does not reset attention for this one. A permanently broken notification path must not produce permanent silence.

Internal reassessment and notifying Mike are different actions. Report material product consequences and choices needing his judgment. Do not forward every internal prod or make him route routine recovery. Reuse the existing supervision and Wake Rails mechanisms; agents should not create duplicate timers to enact this policy themselves.

This adds a product policy for less repetitive notification, beyond separating scan cadence from deadlines. The one-second legacy timing fallback in section 4.2 is engineering compatibility, not the desired repeat-notification behavior. A concrete notification schedule must preserve bounded reassessment, commitment-sensitive attention and recovery from failed delivery. This revision chooses those behavioral requirements without inventing an unevidenced universal numeric interval. It makes no live configuration change.

Acceptance cases for agent discretion and reminders:

- A valid dependency remains unresolved with unchanged evidence and consequence. Repeated notifications become less frequent, the next bounded reassessment remains in force, and the agent can continue justified waiting without creating activity receipts or duplicate wakes.
- The same dependency approaches a promised delivery date, its resolver fails, or material evidence changes. Attention resumes for the affected obligation even when the blocker itself is unchanged. The owner judges the response and reports a material product consequence where needed.
- A wait record is malformed. The agent receives the exact reason and a supported correction, preserves the actual wait and continues independent work. No false coverage or fulfillment is recorded.
- Routine progress prose is absent, but the next action is authorized and its required evidence is present. The product should permit that action. Missing or stale verification evidence still prevents the particular protected action that requires it. Any existing refusal is handled through its supported correction, not bypassed.
- An apparently silent worker may still be performing an external action. The owner reconciles activity and effects before replacing or retrying, restores capable execution through the proper role and verifies continued work. Transfer does not count as delivery.
- A reminder is lost or its recipient cannot act. Bounded reassessment retains the unmet obligation and brings the failure to a capable responsible owner; neither successful notification nor silence marks it fulfilled.

### 4.1 Reuse the existing obligation-specific wait implementation

Morrow compared pinned b299 with the reviewed Wake Rails candidate `926774a30fb79df5c66015b118689b8be45aa350`. Kestrel independently read the target checkpoint and gate paths, candidate coverage and policy paths, and the cited coverage regressions. These are source and test inspections, not new test runs or proof of installation.

Already in b299:

- `lib/tightbeam/supervision.ex:673-714`, the checkpoint_scheduled transition, binds a future self-created prompt wake to the holder's running open assignment.
- `checkpoint_receipt_in_txn` at `2964-3024` admits a bounded checkpoint only when there are no other effects and the latest receipt was not itself a checkpoint. `receipt_due_at` at `3026-3031` uses that checkpoint's dueAt; ordinary receipts use the accepted/source timestamp plus the supervision interval.
- `test/supervision_test.exs:434,479,514,547` covers bounded checkpoint reuse, exclusion of unrelated or expired wakes, outstanding controllers and deadline preservation across restart.
- `gate_reason_in_txn` at `3132-3175` suppresses for harness unavailability, any queued/running holder turn, a scheduled sidecar controller, or standing work-blocked. It does not ask whether a dependency continuation covers the particular obligation.

Missing from b299 but present in the inspected candidate:

- Candidate `supervision.ex:3151-3189` replaces session-wide queued/running coverage with `Wakes.covering_continuation_in_txn?(txn, assignment_id)`.
- Candidate `wakes.ex:726-784` selects holder_continuation rows with matching assignmentId and obligationRef, then checks admission, eligibility, valid coverage and pending/queued/running state through the existing wait-prod-coverage policy evaluator.
- Candidate `continuation_facts_in_txn` at `787-853` derives the obligation and continuation state from records. For a dependency, valid coverage requires the bound verification responsibility to remain accountable. This is not credit for arbitrary notification traffic.
- Candidate `priv/kungfu/agentic-engineering/rules/verification.toml:75` onward supplies the shipped holder-continuation-coverage policy and its explicit predicates.

Wake Rails is already approved by Mike. The following is its engineering reconciliation requirement, not a new product recommendation or approval request: reconcile the existing qualified-wait implementation and its necessary admission, recognition, storage and policy dependencies. Preserve the bounded checkpoint path. Do not copy only the new supervision call into a tree lacking its required wake behavior. Do not import unrelated candidate changes solely because the branch was reviewed. The inspected dependency groups follow; they identify the existing implementation, not an audited minimum cherry-pick sequence.

The product requirement is evidence-triggered waiting and resumption for one obligation without hiding another. A b299 checkpoint is a time receipt, not a producer-evidence predicate. Lengthening it cannot establish that exact producer evidence caused resumption. Counting arbitrary pending wakes would suppress unrelated obligations. Those smaller changes cannot meet the stated acceptance cases.

Morrow's original dependency map is `/home/mike/wake-rails-notes/019-wait-dependency-map.md`. Kestrel read it in full and independently read candidate registration, policy selection and coverage functions plus the commit history. Candidate provenance starts at f303dce7 and comprises these coupled groups:

- A, `4a7eddad` through `2722f787` inclusive. Committed-fact recognition and startup ordering in `lib/tightbeam/rule_runtime.ex`, `rules.ex`, `db.ex`, `dispatch.ex`, relevant publication callers, `application.ex` and `gateway.ex`. Required behavior: recognize qualifying committed evidence without depending on another agent's status message. The existing time checkpoint has no such recognition path.
- B, `3cbaf9cc` through `40bd6fc1` inclusive. Durable registration and recognition in `wakes.ex`, `schema.ex`, `assignments.ex`, `condition_facts.ex`, `gateway.ex`, `cli/src/args.rs` and `cli/src/dispatch.rs`. Required behavior: bind the obligation, predicate, resolver and verification responsibility; recognize current matching truth and terminal dependency outcomes; preserve recognition evidence across restart. A future time alone cannot supply these identities or evidence.
- C, `66c9e21e` through `32911d0c` inclusive. Admission migration ordering and activation stamps in `schema.ex`; same-obligation coverage and watermarks in `supervision.ex`, especially `b5e48a91`; valid-wait interval relief in `effort_checkin.ex` at `3e3d2028`; shared runtime seam `32911d0c`. Required behavior: keep coverage tied to its obligation, preserve historical migrations, and prevent the existing effort supervisor from undoing a valid wait. This reuses the existing effort horizon, not a second progress system.
- D, `c75b268d` through `926774a3` inclusive. Shipped wait-verification-admission, wait-prod-coverage and wait-effort-relief policies in `priv/kungfu/agentic-engineering/rules/verification.toml`; authorized ancestor registration and creator/lineage checks at `77fc1a31`; authority inventory regression `659f2779`; operating-manual and dispatching guidance `06603540`; typed assignment identity preserved through `wire/router.ex` and CLI/router regressions at `926774a3`. Required behavior: the composed policy and actual client path must admit and use the qualified wait, rather than leaving a correct helper unreachable.

In candidate `wakes.ex:554-568`, registration validates obligation, registrant, target and admission. At `644-708`, dependency registration validates predicate contracts, resolver and verifier, selects policy, evaluates current truth, creates the durable wait, records recognition, admits its sidecar and reconciles relief atomically. Coverage at `726-784` depends on that result. Required storage includes waitMode, assignmentId/obligationRef, predicate and resolver identity, recognition provenance, verifier/policy state and admitted holder_continuation state. Reuse the existing migration implementation and historical fixtures; do not propose another schema alongside it.

For these acceptance cases, required publication behavior covers exact producer artifact/review evidence, condition facts, resolver/obligation terminal changes and turn outcomes. Other publisher coverage in those historical ranges is not independently justified by the original specimens. It is broader existing feature scope to reconcile, not mandatory new scope created by this plan. Neither Morrow nor this editor certifies that every commit or publisher edit in the ranges is indispensable. Omitting coupled runtime or relief behavior would require a separately justified alternative; no such redesign is proposed.

Integration and historical migration compatibility are real delivery risks. Preserve target-only concern tags `9e9eb50d`, nested-error handling `7311707d` and terminal-effort regression `b299457d`; do not replace target files with older candidate copies. Reconciliation must show the selected behavior and existing b299 fixes together. This is larger than guidance cleanup, and branch review is reusable evidence rather than permission for unconditional whole-branch import.

Guidance alone cannot make the existing session-wide query distinguish two obligations. Another credit schema is unnecessary because the reviewed candidate already implements that distinction.

Acceptance, reusing `test/row_driven_waits_test.exs` in the candidate:

- `911-952`: a valid admitted wait covers only its named obligation through pending, queued and running delivery. A generic prose wake naming assignments is not equivalent coverage.
- `954-988`: two assignments share a holder. A's activity or continuation cannot hide B's unmet obligation, and B's valid wait must not generate duplicate wakes or invented work.
- `990` onward: ancestor registration preserves the true creator and checks authorization lineage rather than pretending the holder registered it.
- `1361-1378`: failed or failed_unknown continuation delivery ends coverage without attesting resolution or closing the obligation. The orchestrator arranges supported recovery; the PO does not report the product requirement fulfilled. Successful notification also does not by itself fulfill the requirement.
- Morrow additionally inspected cases at `150,238,334` for resolver recognition, exact revision/producer identity and condition evidence. Preserve these with the bounded dependency path. Kestrel has not independently repeated those particular reads.

### 4.2 Separate scan frequency from the no-progress interval

Morrow identified a remaining timing coupling in both b299 and the inspected candidate. Kestrel independently checked the b299 configuration wiring, supervision state, receipt rebasing and restart regression. This is a timestamp calculation issue, not proof that every agent gets a prod once per second.

Current b299 paths:

- `lib/tightbeam/application.ex:258` defaults wake_tick_ms to 1,000.
- `lib/tightbeam/gateway.ex:158,314` sends that same value to recover_liveness! and Supervision's sweep_ms. Wakes polling uses it at `307`.
- Gateway observation inputs at `1031,1041,4254` and retirement at `6507` also use wake_tick_ms as supervision_interval_ms.
- `supervision.ex:1397,1424` stores sweep_ms and uses it for terminal evaluation; `2444,2644,3195,3317` also use it for recovery, receipt rebasing, sweep evaluation and retirement recovery. `schedule_sweep` at `3395-3398` legitimately uses it as polling cadence.
- Assignment arming at `640-650` and ordinary receipt dueAt at `3029-3031` consume an interval to establish the deadline. `test/supervision_test.exs:547` already preserves an armed deadline across restart and adopts the replacement interval only on a later receipt.

Proposed small change:

1. Add a dedicated positive supervision_interval_ms configuration value. Resolve its explicit value at configuration load; when absent, use the existing configured wake_tick_ms as a compatibility fallback. Keep wake_tick_ms for scheduling scans. Stock defaults remain 1,000 ms. This proposal does not choose a slower default or change live configuration.
2. Pass the dedicated interval through gateway startup recovery, Supervision state, terminal and verb observation contexts, new assignment arming, receipt rebasing and retirement observation/recovery. Keep sweep_ms solely as scan scheduling cadence. Update every listed interval consumer, not only the constructor.
3. Preserve already armed deadlines and their stored intervals on restart. Use the new configured interval for new arming and later eligible receipt rebases. Preserve the distinct bounded-checkpoint dueAt behavior.

The configuration field name above is proposed, not an existing supported operator command. A source change and normal validation are needed; no database redesign or per-turn timer is proposed. Any slower default is a separate policy proposal requiring a stated rationale. With the new setting omitted, changing the legacy tick still changes the fallback used for newly armed or legitimately rebased obligations after configuration reload. Independence is promised when the dedicated interval is explicit, not in legacy compatibility mode. Neither mode rewrites an already armed deadline merely because configuration changed.

Acceptance additions:

- Set scan cadence to 1 second and a different explicit interval L. New open and ordinary receipt deadlines use L, not the scan tick.
- With explicit L, vary only scan cadence. Existing deadlines and prod entitlement do not change, and newly armed/rebased deadlines still use L.
- Omit the new setting and configure a nondefault legacy tick. Preserve the previous custom interval for new/rebased work. Do not silently substitute 1,000 ms. A later change of legacy tick follows the documented fallback behavior.
- Restart with an armed deadline. Preserve it. A later eligible receipt uses configured L; a bounded checkpoint still uses its own dueAt.
- A due uncovered obligation still receives a useful prod. Qualified waits still cover only their own obligation.
- Keep the existing restart regression and add focused unequal-tick/interval and configuration-compatibility cases. No new test was run on Gibson for this plan.

## 5. Already present or not justified as another 0.1.9 patch

### Readable provider failure

Kestrel inspected `lib/tightbeam/gateway.ex:6166-6186`. `error_map_text/1` already reads both nested `data.message` and `data.details`. `test/gateway_test.exs:7652` onward contains the captured quota failure from turn 120945 and tests its chat marker and terminal state. This is stronger evidence than the open ticket title claiming the field is ignored.

Patrol reports delivery accepted at `7311707d43486c5ee580daeb640c10c8ec84e383`, review `att_593d33d4`, acceptance `att_c977a8a3`, full Racter 1,810/0 and green hosted Linux/macOS/packages run 34067732705. Those test-run records are Patrol's inspected evidence, not a new test execution by this editor. The item remains open for a main ruling, not missing 0.1.9 implementation.

Disposition: no repeat 0.1.9 implementation for this specimen. Preserve existing regression coverage and truthful deployment reporting. This does not prove that running Gibson 0.1.8 has the change installed.

### Provider failures, bounded retry and physical activity

Parallax's live 0.1.8 census documented quota, adapter, interrupted-outcome-unknown and other failed turns, often with the original wake identity preserved. That establishes the observed failure pattern, not an unimplemented b299 mechanism. His pinned source inspection found the relevant fixes `d10b51c1`, `0b52dcfb`, `708d9d18`, `8d899368` and `09ff4620` already ancestral to b299. The following findings are his contribution, with the editor's independent checks noted explicitly.

Already present at b299:

- `lib/tightbeam/harness_health.ex:20-25,229-334,565,732` defines six failure classes, opens an incident immediately for authoritative provider evidence, and requires two distinct sessions within 120 seconds for inferred shared failure. Normal delivered-turn evidence resolves incidents. Kestrel independently read the classification and incident conditions. `Supervision.prod_production_matches?/3` and `dispatch_wake/4` consult the holder's harness and host and recheck before action. Parallax inspected `test/supervision_test.exs` around `2830-2980` for scoped suppression and healthy-route continuation.
- `HarnessHealth.repair_guidance/1` at `1161-1205` names existing repairs: model selection, adapter restart, explicit resume after rate/auth recovery, and external-outcome reconciliation before rerunning interrupted work. Kestrel independently read those mappings. They are not authorization for this editor to perform a restart, credential action or replay.
- `Wakes.preserve_failed_intent_in_txn/3` at `425-565`, called from terminal classification, creates an idempotent deterministic retry successor only for the eligible rate-limit-dead prompt-wake case. Retry delay starts at 30 seconds and doubles up to 30 minutes. Prior terminal evidence remains. Kestrel independently read eligibility, deterministic identity, lineage and delay calculation. There is no automatic retry for arbitrary failed_unknown work.
- `test/failed_turn_intent_test.exs:50,102,125,205,274` contains rate-limit successor, unsafe-retry exclusion, lineage, six-failure cause routing and failed-notice exclusion cases. Parallax inspected their bodies. Ordinary repeated failures bubble the original cause through active parent lineage; failed bubble notices do not create a new recursive streak.
- `Wakes.deliver_due` around `2537-2770` uses deliver-then-mark. Parallax inspected pending prompt failure with wake-ID deduplication, unknown internal-consumer cancellation plus wake_undeliverable, and raising internal-consumer retention plus wake_delivery_failed, with tests around `test/wakes_test.exs:106-208`.
- `ExecutionMap.quiet_match?/3` and `node/2` at `279-342` expose running-turn and current-holder pending-wake activity. Quiet selection requires neither. Kestrel independently read these paths. Parallax inspected `test/execution_map_test.exs:514-576`, including stale ex-holder exclusion. The source explicitly limits historical pre-cutoff running-turn coverage; absence of old attribution is not universal proof that no work ran.

Minimum recommendation: retain those mechanisms and their regressions. Replace misleading intervention guidance in `orchestrator.md` and `unblocking/SKILL.md` alongside section 4 with:

> Diagnose apparent stalls from relevant execution, dependency and failure evidence. Reuse healthy recovery. Reconcile possible external effects before retrying an unknown outcome.

This is not a mandatory multi-query ceremony before every ordinary follow-up. The evidence needed depends on the suspected failure. No missing b299 code mechanism was established by Parallax's specimens. No new classifier, stored liveness bit, semantic-progress detector, incident schema, general replay loop or automatic reassignment is justified here.

Acceptance preserves the existing cases: corroborated shared failure suppresses the affected harness/host while healthy routes proceed; an eligible rate-limit wake has one idempotent backed-off successor; unsafe outcomes retain evidence and require reconciliation; a healthy pending recovery is not duplicated; current running or pending work prevents quiet selection while a stale former holder does not. Physical activity is not proof of meaningful product progress, and a sent or delivered notification is not fulfillment.

Parallax observed that raising internal consumers retry per scheduler tick without dedicated backoff. This is an incidental finding outside the original provider/physical-liveness specimen. It does not silently expand this plan. Preserve it as a separate finding if later prioritized; do not add a general retry framework here.

### Standing carry and local integration-target wording

The shipped operating manual already defines standing carry and the default active lines, with explicit exceptions. The separately inspected `/home/mike/.tightbeam/identity/skills/integration-targets/SKILL.md` is org-local and absent from the entire pinned Git tree. Its fresh target-election requirement conflicts with that manual.

Disposition: retain the shipped manual; propose a separate owner-controlled correction to local composed guidance if later approved. Use latest applicable explicit rulings over standing defaults. Do not invent a nonexistent product source path or claim a branch commit changes every active session's effective instructions. Diagnose exposure by reading actual composed text through the existing update/reread process, not a new identity-generation gate.

### Existing bookkeeping routing and stale opener

Patrol reports the stale-opener case resolved using existing openedBySession routing. The earlier consensus records bookkeeping-routing and landing-serializer predecessors as closed. They are baselines, not proof of more unimplemented machinery. Preserve shared landing agreements; do not turn an operational base checkpoint into a new product permission request.

### Outside this minimum plan unless a specimen establishes necessity

No revival of typed progress, a broad authority engine, identity-generation equality, automatic reassignment, a general completion redesign, or a 0.2-only lifecycle command. Wider PO editorial changes and optional reflection policy remain separate from this minimum remedy unless the final reviewers establish a direct original-specimen need.

## 6. Delivery boundaries and validation

The original observers' source contributions are now collected. The remaining plan review is judgment of this whole composition, not a request to investigate every open work item. Existing work is evidence and implementation provenance, not an automatic instruction to implement every open title.

If later authorized, the guidance changes need one composed review covering the seven included archetypes, PO and orchestrator fragments, feature-cycle, unblocking, human communication and the operating manual. Inspect the separately owned local integration-target skill for actual exposure. Replace the named contradictory clauses rather than append a second policy with opposite wording. Preserve the named authority, independent-review, evidence and release protections while delivering section 0's explicit changes to workflow admission and remedy routing. Confirm the loaded rule version and projected hook behavior, not merely the edited guidance. The approved-helper, explicit-hold, discussion-only, review-order, bounded-completion and legitimate-wait cases in this document are acceptance scenarios for that review, not a new evaluation platform or mandatory ceremony.

The wait candidate needs a reconciled target result with the cited row-driven wait, schema-shape, policy-selection and CLI/router regressions. Retain the existing checkpoint, failure/retry and review-exemption regressions. The cadence change needs unequal-tick/interval and compatibility coverage. The reminder policy also needs the product acceptance cases above: fewer unchanged notifications with bounded reassessment, renewed attention to material consequences, and recovery from lost delivery. Do not claim the cadence split alone implements that policy. Tests must run on an authorized test host under the repository's existing verification contract; none were executed on Gibson for this planning exercise.

The plan deliberately does not certify a minimal cherry-pick set, choose a slower prod default, authorize production installation, or repair historical misclassified rows. Its wait recommendation names necessary behavior and existing coupled implementation, with integration cost and broader publisher scope visible. If an implementation proposal adds unrelated behavior or changes explicit constraints to reconcile that candidate, that is a separate scope judgment. Routine conflict resolution that preserves the agreed behavior belongs to the existing technical owner.

Patrol and Orchestrator Editor independently support replacing blanket evidence-only revocation with ordinary completion subject to applicable checks. The target regression supports that change. No general repair verb for a historically mislabeled assignment has been established; this does not prevent the creation-time guidance fix or justify weakening producer review. Any actual historical-row repair remains a separately diagnosed supported disposition, not a proposed subsystem.

## 7. Domain review and plan ownership

Gibson Codex leads this document and the Subetha discussion under Mike's instruction. Domain owners assess the implications for their own responsibilities and raise concrete conflicts. The lead resolves the composition and records substantive feedback. Historical judgments retain their revision and scope; they do not automatically approve new text. Routine acknowledgment rounds are unnecessary.

Editorial work changes the proposal. It does not itself install guidance, implement mechanisms or change live operation.

## Revision record

Draft 02 incorporates Rowan's full Draft 01 review, event `179f61d1-106e-45c1-86e2-4dd0e04d2edc`. It narrows the product-behavior hold to unauthorized changes, separates PO goal routing from orchestrator worker routing, makes review commissioning explicit, and clarifies outcome-based PO acceptance and bounded completion. Rowan found the direction sound but did not give final approval while section 6 remained open. No other participant's final approval is implied.

Draft 03 incorporates Patrol's target regression and applicable-check qualification, events `b7548505-5947-4067-888f-fb686fe71bca` and `4bb220cf-5c5d-4394-a49d-0fdda4569845`, and Orchestrator Editor's source check and full Draft 01 critique, events `bf2905fc-c306-41f6-9910-033c6341d978` and `af26447e-ff23-4ddb-a44c-10b248291f78`. It replaces blanket revocation, corrects review-selection prose, preserves role boundaries, assesses review reuse against changed code and interactions, and labels waiting/rollback changes as policy proposals. These contributions are not whole-final-draft approval.

Patrol's scoped Draft 03 review, event `221707cf-6638-4fe1-bd8a-fb2bd99c48ee`, found no remaining objection within his sections 3 and 5 contributions and relevant revised text. He withheld whole-plan agreement pending completion.

Draft 04 incorporates Morrow's exact-target wait and cadence findings, events `ab8fff6a-a8bf-4171-b132-4c8570aa0b1d` and `0bd16088-06ab-48db-bc1b-ae0e521d10c1`, Rowan's failed-notification acceptance distinction, event `1c3430a0-40e6-45a3-a453-35bb9b3b56e2`, and Orchestrator Editor's per-obligation acceptance and candidate-scope critique, event `528e47fb-dd5e-476e-8b73-4e7ba6aecbef`. The editor identified the custom-configuration compatibility question while specifying the cadence change. No final approval is implied.

Review revision 05 incorporates Parallax's consolidated target findings, event `ace27b0a-ea59-40cc-908e-9a544705d6f3`, and Orchestrator Editor's no-mandatory-query-ceremony qualification, event `53a8470b-d2a6-4485-ac32-d9e65b56c8d1`. It resolves cadence compatibility with the editor's config-load proposal and Morrow/Orchestrator Editor qualifications, events `0380c6bb-360f-46b7-a6a5-cfb763b94311` and `a3056538-582b-4e81-8f23-e83dccecb072`. It includes Morrow's original local dependency map, his explicit scope limitation `4bcfa66e-610d-4e6b-81f3-111d7eb22cd6`, and Rowan/Orchestrator Editor's minimality and delivery-risk critiques `dd80b5d4-6a19-40e6-8980-2fe26100ced6` and `4eb9061a-1503-4b2f-b526-8ebdaf94f615`. The complete source collection is ready for review; contributor approval is still a separate recorded fact.

Review revision 06 changes only the revision label, this record and section 2's coder replacement paragraph. Orchestrator Editor identified that its imperative accidentally assigned review commissioning to the coder, event `b407f763-a0c7-4834-b74a-b61bd87dbb1e`; Parallax raised the same objection in `0378ecf0-87de-4036-b1bf-c74f058fdd3b`. The corrected paragraph has the coder report changed code and interactions while the orchestrator assesses review applicability and commissions review. Morrow and Rowan agreed to revision 05 within its stated limits; those agreements do not automatically endorse these new bytes. No other technical or policy proposal changed.


Review revision 07 follows Mike's 8 September instruction to propose agent-directed supervision in Subetha, accept feedback and edit the document. Mike explicitly distinguished product behavior from merge workflow and confirmed Wake Rails is already blessed. Proposal event `3092ff6e-d5df-454a-83ff-95b278de76e1` introduced explanatory waits, useful and less repetitive prods, narrow hard gates and owner-directed recovery. Rowan's critique `e4477af4-ef2b-4202-bce1-9e836a2bd68d` and Orchestrator Editor's critique `ea9864d3-4db5-47d7-902f-b0d4afb52edf` added expected resolving evidence, bounded reassessment, changed consequences, evidence-versus-paperwork distinctions, role-preserving recovery and reconciliation of possible external effects. Those edits are incorporated. Prior target source findings retain their original authors' attribution and were not reverified as current state. No new source tests were run for this document revision. Revision 06 and its review record remain historical artifacts.


Review revision 08 applies Mike's concise-guidance direction and the canonical operating principle established on 8 September. Replacement guidance assumes professional competence and retains intent, authority and local Tightbeam facts; technical evidence and acceptance cases remain reference material. It adds the gate-placement question from the lead's product assessment for domain discussion and replaces the all-participant approval ceremony with lead-owned, focused domain review. The archived revision 07 and its judgments remain unchanged.


Review revision 09 incorporates focused domain feedback on revision 08. Morrow's event `a1dfe7ef-f466-481c-8cce-d9ec26a010ca` restores obligation-specific coverage and reuse of a healthy subscription. Rowan's event `78a7ab00-a439-4f31-a50e-411bace2f18e` restores concise PO acceptance and user-availability responsibilities. Orchestrator Editor's events `e7e053e4-a899-429c-a59c-e614cccb90db` and `0980c600-fa14-4b23-acb3-d4e40b88229b` clarify delegated authority, specialist roles, applicable completion checks and bounded goal completion. Patrol's event `5af24203-7913-4b04-b0f0-303f7dd11893` informs the concise carry instruction and the distinction between diagnosis and acceptance. The lead accepts those local facts while declining to recreate long professional tutorials or a new review ceremony. Orchestrator Editor then supplied the bounded diagnostic-path inspection in event `8c6ffa5b-0777-48d0-91a6-613afe9b1df4`. The lead resolved the question by retaining the existing acceptance-review gate and teaching the existing recon route. No gate change is selected.


Review revision 10 incorporates Kestrel's revision 09 Firehose-domain feedback, event `1c913a88-2e9f-4f07-bf6a-7d68704b199f`. It adds reference acceptance cases for authority across CI reconciliation, independent testing dependencies and refusal routing, plus the attributed source-exposure clarification. Runtime replacement guidance is unchanged. Revision 09 and its records are preserved. Kestrel supports the direction with no blocking Firehose-domain objection; that judgment concerns revision 09, not these later bytes.


Review revision 11 follows Mike's correction that existing enforcement is part of the product. It incorporates the canonical enforcement assessment and source/configured-rule findings from Orchestrator Editor, Rowan, Kestrel and Morrow. It proposes retiring unnecessary workflow gates, separates review protection from forced sequencing/staffing, and names remaining mechanical design obligations. Mike's spirit clarification preserves a meaningful PO opportunity to review and correct specifications or other work against intent; blanket-gate retirement without that opportunity is insufficient. Earlier revision judgments and the narrower recon-path finding remain historical. The lead's previous confidence in the guidance-focused scope is superseded.


Review revision 12 incorporates Orchestrator Editor's focused follow-up `f055b9a8-c995-4cf1-9163-da28e2f1de6f`. It restores explicit independent spec-or-code review in the orchestrator home and adds the failing-code linked-review acceptance sequence. Latest qualifying linked verdicts, current evidence and the remaining acceptance-consumer design obligations stay distinct. No mandatory preliminary review phase or live mechanism change is introduced.


Review revision 13 records Mike's explanation of the posture gates' anti-overprocessing purpose and his challenge to unconditional removal. That recommendation is withdrawn pending a concrete proportionality design. Rowan's `c8a01020-ff8f-45f4-b9e7-2f2e18d17d27` supplies the distinction between restoring agreed behavior and changing product commitments. The small-fix path, orchestrator ownership, PO intent boundary and balanced acceptance cases are explicit. The proposal does not simply restore the old gates or claim their replacement has been validated.


Review revision 14 incorporates Orchestrator Editor's `21996d7e-992f-499c-979c-455888fd1cbb`: name feature-cycle's blanket remaining-steps clause for correction, use ordinary delegation context for proportionality, and include contrasting validation, authorization and novel-behavior acceptance cases. The contributor favors replacing posture vetoes with the positive small-fix duty; the lead retains the unresolved replacement disposition and the absence of an observed trial.


Review revision 15 incorporates Kestrel's `d57c0977-30b4-40b1-ae42-3a8ac1839176`. It preserves substantive correctness under light review, names the coder/reviewer/feature-cycle composition, and adds the two Firehose proportionality cases. Lead source reading also identified reviewer-code's passing-test-before-judging clause as a required companion change for early review. No current rule changes or observed post-change outcomes are claimed.

Revision 16 selects the coherent posture replacement, distinguishes guidance/kungfu/substrate implementation scope, publishes this plan canonically and corrects the learning language to production release improvement. The later forensic review does not replace release readiness. Earlier revision judgments remain historical.
