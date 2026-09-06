# Tightbeam: verified dependency waits — discussion notes

Conversation notes, commissioned by Mike on September 6 as the spirit for a dedicated Tightbeam sub-PO's refactor targeting 0.1.9. Not yet a canonical spec. No production changes authorized or made. Captured September 5–6, 2026. Earlier sections retain the chronology; later clarifications supersede earlier proposals.

## Commission and controlling interpretation — September 6

Mike: "i'd like a new sub-po for this refactor. have tightbeam po create it, and use this document as spirit. we target 0.1.9. let's get this going."

Product outcome: reduce unnecessary paid turns by replacing repeated unchanged-dependency checks and invalid prodding with actual row-driven wakes in the common production/rail engine. This is an architectural correction of the separate conditional-wake matcher, not another alternate rule system or a catalog of special blocker types. The engine executes policy; self-block admission and verification policy belong in rails.

Important correction to the early diagnostic framing: the sampled churn predominantly supports legitimate dependencies not recognized as valid waiting, NOT dishonest agents manufacturing accepted progress. The recovery owner did have a few ready-now tasks (scope comparison and routing investigation); these need explicitly scheduled continuations, not fake dependencies. The refusal-loop agent did not show evidence that merely giving it another turn would help. Independent assessment is inference, not guaranteed proof; do not turn the earlier brainstorming about assessor budgets into a mandated large new subsystem.

Use the existing Tightbeam PO to create and staff a dedicated child PO with real parentage and durable work. The child should canonicalize this spirit in the specs repo, inspect/reuse existing rule and wake machinery, reconcile related cards, and own a bounded plan, implementation, tests, independent review, and integration for 0.1.9 under repository rules. Preserve historical delivery records. No new 0.2 target is implied. No release, installation, production restart, direct production-data repair, or deployment is authorized by this commission.

## Mike's stated direction

- Policies expressible as rails (including who may self-block) should be rails; the substrate should be agnostic to those policies.
- Trust agents to report inability to proceed, but always verify the claim. Older agents gave up prematurely; do not make distrust a permanent substrate assumption.
- A wait must name what the agent is waiting ON. No unactioned blocks.
- Verification must challenge an unjustified claim. A justified claim must put an unblocking action in motion.
- Merely notifying a parent is insufficient: the parent can also fail to act.
- Waiting for work-item completion should create a completion-conditioned wake. Waiting for a user decision should create/link a decision request and its resolution-conditioned wake.
- A valid dependency wait should suppress prodding for the waiting work, then wake the agent when its condition changes.
- Conceptually a conditional wake is a production rule over durable system state. Explore predicates parameterized by rows, not only literal kind/scope fact events.

## Grounded context

- Running 0.1.8 hard-codes the self-block prohibition in gateway.ex's work_block_authority?: caller must differ from target and be above it in spawnedBy lineage (owner/admin alternatives).
- production-machine-v1.md Standing facts assigns work-blocked authority to ancestors/owner/admin; facts suppress prodding, not all turn delivery.
- tightbeam-decisions.md August 19 ruling for 0.2 removes surrender, permits typed cannot-proceed, retains the obligation, pauses card supervision, and routes parent disposition. This is a design ruling, not proof it is installed.
- wake-on-fact-v1.md contains historical supervision/parking language amended August 12; do not treat its old pending-wake suppression description as running behavior.
- The two previously sampled churn sessions had no work-blocked/unblocked facts. Recent substrate-recovery transcript repeats unchanged tooling/approval blockers and references existing follow-up wakes without new evidence.

## Observed candidate dependency categories

Sampled live decision-request records and prior recovery-owner response; these are reported blockers, not independently validated necessities:

- Work/review/integration result or disposition of a predecessor assignment.
- Owner decision: verification route, product scope, provisioning contract, architecture ambiguity.
- Conflicting authority: permitted build host versus platform required; approved run location versus host restriction.
- Resource/capability recovery: quota, credentials, sanctioned tooling, disposable verification environment.
- Human action: browser acceptance, keychain/signing interaction.
- Version-specific artifact availability: compatible macOS executable, exact reviewed revision.

## Proposals/questions for discussion, not yet Mike's decisions

- Scope waits to an assignment/obligation; one waiting card must not silence supervision of unrelated actionable cards in the same session.
- Record predicate, exact row identities/version expectations, why necessary, resume action, resolver owner, and verification evidence/status.
- Check existence/truth/authority mechanically; separately verify semantic necessity (is the dependency real, or is there an authorized next step?).
- Registration should atomically link the dependency, necessary request/work, and wake; test predicate immediately to avoid waiting for an event that already occurred.
- Prefer durable, pure, bounded, authorized predicates over supported rows to arbitrary agent SQL/code. Support useful AND/OR predicates with causal evidence.
- Handle resolution alternatives: failure, cancellation, withdrawal, supersession, missing resolver, and dependency cycles; wake to reconsider rather than wait forever for success.
- Resolver/verification obligations need their own oversight. Escalate failed resolution or verification, not repeatedly wake the waiting worker to say nothing changed.
- Timers detect missing resolution and trigger reassessment; they are not evidence that the dependency cleared. Avoid automatic recurring worker checks as the default.
- Decide who verifies, when provisional suppression starts, and how a stalled verifier is handled without creating another expensive polling loop.

## Potential work-item framing

Replace opaque blocked state with verified, actionable dependency waits, separating rail-level admission policy from durable predicate-wake mechanics. Define interactions with prodder AND effort check-ins. Preserve open obligations and guarantee an accountable resolution path.

## Discussion refinement: row predicates, not dependency categories

Mike rejects introducing an enumeration of blocker types. The domain is already expressed by the kinds of durable records the system can write. Quota, credentials, etc. should be observations recorded in the database; waiting is a predicate over those records.

Illustrative logical records/predicates, NOT assertions about existing table/column names:

- Work item: referenced row reaches a terminal disposition; continuation inspects whether it succeeded, failed, or was canceled.
- Decision request: referenced row gains a ruling or another terminal disposition; continuation reads the result rather than equating any resolution with approval.
- Quota observation: latest observation for exact provider/account/scope reports usable capacity; passage of an estimated reset time triggers a probe, not a fabricated recovery fact.
- Credential observation: latest exact host/provider/principal observation reports validated usable authentication. Store metadata, never credential secrets, in these observable rows.
- Capability/environment observation: latest observation for exact target reports required capability healthy/ready.
- Artifact plus review records: an artifact for the required revision exists AND an applicable accepted review references that exact artifact/revision.
- Human action: referenced action/request record reaches a completed or otherwise terminal disposition, with recorded evidence.
- Authority: applicable ruling/authorization record exists for the exact operation/scope, or the pending clarification request reaches a terminal disposition.

Same wake mechanism in every case: bind row identities/parameters, evaluate a predicate over current durable state, reevaluate on relevant writes, and deliver once when satisfied. Domain-specific producers remain responsible for truthful observations and changes; predicates do not themselves restore resources or obtain decisions. Semantic verification still asks whether the chosen predicate is a necessary dependency.

## September 6: prods, continuation grace, and pretend progress

Mike's concern: a prod cannot merely say "wake up"; it must require an explicit production/wake. But a turn can legitimately end before its requested work is complete, so continuation must be possible without letting agents indefinitely claim to be working.

Discussion proposal, not yet decided:

- With an open obligation, turn-end oversight asks for an explicit next transition: completion evidence, an actionable continuation, or a dependency-conditioned continuation.
- A continuation for work ready now can itself be a one-shot production over current state; no fake external dependency or arbitrary delay is necessary.
- The continuation identifies a concrete next action and the evidence expected from it. Its existence proves a plan, NOT progress, and must not itself reset an effort/progress budget.
- Bounded continuation grace permits legitimate multi-turn work. Meaningful task-specific evidence or an independent assessment can justify renewal; writing more plans, wakes, or cosmetic records cannot automatically renew it.
- On exhausted grace, create an accountable independent assessment/disposition obligation, not another identical worker prod. The assessor checks actual outputs, failed attempts, and constraints, then directs a concrete next step, validates a dependency wait, adjusts the plan, or recommends reassignment.
- Avoid equating no code diff with no work: investigation and reasoning may produce useful evidence, but semantic adequacy needs judgment, not merely a row count.
- Anti-evasion policy belongs in rails; substrate supplies durable turns, evidence references, one-shot production firing, and accounting. Exact budgets, verifier selection, and assessment rules remain open design questions.

## Existing work and assessor limitation

Mike points out that an adversarial assessor is still inference and can rubber-stamp the worker. Another agent is not a proof of actual advancement.

- wi_26471b0d-a597-4d33-8ad0-7adb68a222e0, closed: Enforce valid liveness receipts as the only way to clear prodder liveness. Source commits f8472edb and c57f4482 are ancestors of v0.1.8 (checked). Supervision consumes typed durable sources, not progress prose. This is structural evidence enforcement, not semantic proof of progress.
- wi_990f7b7e-837b-4aba-8f2e-ac6617327d78, closed: Typed progress attests inherit assignment effectKind; acknowledgments do not count as effect. Producer completion records reviewed implementation edb7788968aa74512cf309c2e5f354a91e9bc575 as targetless, with no merge or deployment. Later landing has NOT been established by this inspection; do not infer it from closed status.
- wi_04b132eb-5af6-48d4-b7b9-463eb80e7da7, closed: activity-theater guidance explicitly includes rubber-stamp supervision and asks what changed on the deliverable, not how much activity occurred. Work scope included truthful rows with no deliverable movement.

Any proposed new work must reconcile these existing mechanisms rather than treating progress accountability as a new idea.

## Mike's correction: all sampled unchanged-status loops should be wakes

The recovery-owner examples are not reasons for recurring checks or progress filings; express their next actionable transitions as predicate wakes:

- "Re-read the decision; ruled but selected answer absent": wait for a readable resolution record, including its actual disposition (not merely status=ruled). The missing readback is itself a repair obligation; register/link that repair rather than passively wait for an unowned data defect to fix itself.
- "Candidate frozen; no merge/deploy authorized": wait for the applicable disposition/authorization or cancellation/supersession. A wake to reconsider is not permission to merge or deploy.
- "Tooling blocker unchanged; retain holder": wait for verified required capability restoration or an authorized alternative disposition.
- "Receipt of continue instruction; custody verified": acknowledgment is not advancement. If an actionable next step exists, arm its immediate continuation; otherwise arm the actual dependency predicate. Do not schedule another custody-confirmation turn.

General rule from this discussion: persist what change would make the next action possible, then run on that change. Do not repeatedly spend agent turns confirming the absence of change. Monitor resolver obligations separately so the wait is never unactioned.

## Existing smarter-wake work: reconciliation candidates

- wi_2ef3d514-eb1b-4521-81ad-696a0b00d865, currently iceboxed: "Condition wakes: wake fires on a recorded event (artifact recorded, assignment closed, turn terminal) with a timeout fallback — replace polling check-back clocks." Closely aligned motivation, but framed as event matching, not ad hoc rails over arbitrary supported durable-state predicates.
- wi_fca19e0c-6d7b-4946-98b8-41cf1856bafd, closed: "Add agency-preserving condition prompts for dependency changes." Bounded implementation exposes existing kind/scope condition wakes through CLI. Its contract says the wake delivers a new notification turn; the agent rereads state and decides, rather than automatically replaying a workflow. This principle should survive any rail unification.
- wi_c60c0189-375a-4bce-bced-e80862d2a454, open: advertised self-scheduled continuation cannot suppress supervision. Current scope explicitly separates the wording fix from designing a new continuation-credit mechanism.

Mike's clarified framing: a conditional wake IS an ad hoc rail/production, with a predicate over durable rows and a side effect of waking the accountable agent. This is more than adding event names or extending a separate wake subsystem. Searching the above item scopes and relevant wake/rail specs did not establish that this unification is already an explicit delivery requirement. Reconcile/amend existing work if Mike commissions it; no org records changed during this discussion.

## Explicit refactor direction and current adoption barrier

Mike explicitly requires refactoring wakes into true rails in the production system, dependent on actual business rows rather than separately manufactured evidence of those rows. This records the requirement; no implementation or org work-item mutation has been undertaken here.

Current adoption explanation: conditional wakes are useful notifications, but an agent-scheduled condition wake does not satisfy the running prodder's pending-wake suppression guard. That guard requires a supervision-owned scheduled controller linked to the assignment; ordinary agent wakes cannot create that controller. Replacing timed rechecks with condition wakes alone therefore does not establish valid sleeping or stop prods. A separate ancestor-approved session block can suppress prodding, but was absent for the sampled agents. Generic advice to schedule a continuation is consequently misleading as a suppression remedy. Existing condition wakes also require a matching fact producer; they do not directly observe arbitrary business-row changes. We have not proven lack of guidance as the reason these particular agents chose timed rather than condition wakes.

## Agreed turn-end rule

Mike confirmed: there is no spontaneous or separate "immediate continuation" mechanism. Before ending its turn, an agent with unfinished actionable work explicitly schedules a wake eligible after that turn finishes. If progress depends on another state change, it schedules a predicate wake instead.

If the agent neither finishes the obligation nor schedules its next wake, the prodder supplies the missing turn and requires the agent to account for its next transition. A covering wake already delivered into a queued/running continuation must also prevent a duplicate prod. Coverage is obligation-specific, not an exemption conferred by any unrelated session wake. Wake justification/progress verification remains separate rail policy; scheduling alone is not proof of advancement.
