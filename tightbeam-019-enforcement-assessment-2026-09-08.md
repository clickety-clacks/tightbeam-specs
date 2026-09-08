# Tightbeam 0.1.9 enforcement assessment

8 September 2026. Gibson Codex leads this assessment under Mike's instruction to conform the documents and repair plan to agent-owned judgment. Status: source-backed product and engineering proposal. No live rules, runtime configuration or code were changed. Specific mechanical dispositions below are proposals, not additional operator authorization.

## Product conclusion

Guidance and enforcement are one product behavior. Revision 10 of the local churn plan did not adequately assess existing rules that could defeat its shorter guidance. This assessment corrects that omission. Keep the Rails engine and concrete protections; retire or narrow the specific policies that make agents follow a mandatory process without establishing the protection claimed.

The proposed repair now includes rule changes. It is not guidance-only. Agents retain responsibility for proportionate engineering, product judgment and independent review. A supervisor uses the record to judge those responsibilities; a historical verdict token does not substitute for that judgment.

## What was inspected

The lead inspected immutable source objects at `b299457d5c95dd6e161ed9b1de70b4450b5166b7` using `git show` in `/home/mike/src/tb018-build`. That checkout's working tree was neither trusted as the target nor changed. The complete shipped engineering bundle contains two dispatch-rule files and one tool-rail file: `priv/kungfu/agentic-engineering/rules/engineering.toml`, `rules/verification.toml` and `rails/engineering.toml`. Together they declare eight active dispatch rules and five tool guards. The review-rounds doorbell is commented out.

The lead also read and hashed the corresponding three files under `/home/mike/.tightbeam/identity/`. These are configured local files, not proof of the gateway's in-memory rules or each session's installed hooks. `Rules.load!`, `rules.ex:162-184`, loads `identity/rules/*.toml` into persistent memory; `Rails.load!`, `rails.ex:102-136`, loads tool statutes. `gateway.ex:3413-3414` invokes both loaders. The source branch, configured identity, generated session home and running gateway are distinct evidence sources. Guidance reload alone is not proof that enforcement changed.

The local passing-test rule selects a coder holder; b299 selects a code effect. The local review refusal text also differs from b299. Kestrel reports historical Firehose session identities differing from the current local identity. Preserve these distinctions during delivery validation. The inspection did not read credentials, mutate the identity, query cached rules through a new runtime hook, run source tests or exercise live refusals.

Source/configured snapshots and hashes are in `/home/mike/.lavish/rails-assessment/`. Hard-coded paths inspected include dispatch prechecks, assignment lifecycle/attribution, fact computation, remedy routing, supervision eligibility and effort check-ins. This is a bounded enforcement assessment, not a claim to have audited every handler or every operational security boundary.

## Rule dispositions

### Assess workflow-start requirements against their purpose

- `implementation-requires-posture` and `implementation-dispatch-requires-posture`, engineering rules lines 102-124: deny coder assignment/dispatch without a work-item posture-light/heavy verdict. Revised disposition: withdraw unconditional retirement. Mike explained that these gates were introduced to stop agents sending small understood fixes through unnecessary specification and review cycles. Preserve that purpose as an explicit orchestration responsibility. The lead favors replacing the mandatory label with accountable proportionality, but the replacement must demonstrate both a usable small-fix path and adequate treatment of uncertain or consequential work. A token proves neither good judgment nor appropriate process. Merely retaining or deleting these gates is not an adequate design.
- `spec-dispatch-requires-spirit`, lines 76-86: denies any dispatch on an item with a spec reference and no historical spirit-approved token, without restricting the target role. `rules.ex:1342-1390` reads spec presence and distinct verdict kinds across all assignments, without a current-spec, PO-author or latest-verdict qualification. It can block preparatory investigation, yet an old approval can satisfy it after intent changes. Proposal: replace the blanket gate while preserving its product purpose. Mike clarified that the PO is the seat of product spirit, with responsibility to correct specifications themselves when they miss intent. Newly written or materially changed specifications, and code or other work raising an intent question, must reach the PO with enough context and time to influence the result. Record that opportunity and route any correction through accountable ownership. Retirement of the broad veto needs this supported routing and supervision in the composed design; deleting it and leaving generic prose is insufficient. Preparatory work need not stop merely because a spec reference exists. Neither the spec reference nor removal of this gate grants implementation authority. Explicit governing holds remain, and their enforcement must be assessed separately from this historical token.
- `refix-requires-diagnosis`, lines 33-51: denies dispatch and automatically assigns recon based on a prior-completion count and absent diagnosed token. `rules.ex:1421-1448` counts all completed unlinked assignments on the work item, without a code or actual-fix filter. Completed evidence mapping can therefore trigger it before the first repair. Proposal: retire this mandatory count-based routing. Expose recurrence evidence through the existing record and appropriate supervisory reminders; the orchestrator decides whether independent recon is useful. An old diagnosed token also does not prove a new cause was investigated.

Acceptance: an understood repair of agreed behavior proceeds without an unnecessary discovery/specification cycle; authorized investigation of a spec-backed item can proceed before a spirit verdict; a new or materially changed spec reaches its accountable PO in time to affect delivery, including when the specification itself is wrong; completed evidence work does not force another diagnosis. A queued notification alone does not prove the PO had that opportunity, and an old verdict does not dispose of a new intent question. A changed product ask still requires its governing authority. None of these changes permits impersonation, unsafe disposal of another agent's work or false completion.

### Proportionate execution is an accountable responsibility

The original light path is concrete: `feature-cycle/SKILL.md:22-29` skips specification, spec review and decomposition, treating the work-item input as the spec. `orchestrator.md:25-42` defines light/heavy selection, but says heavy is the answer when in doubt. The lead inspected both passages after Mike explained their purpose. The earlier audit read the gate predicates without adequately accounting for this intended benefit.

Preserve the small-fix path and the orchestrator's responsibility to select it when appropriate. Use the existing ask as the specification when sufficient; add process to resolve a concrete uncertainty or protect the outcome. Replace the automatic heavy default with focused investigation followed by a proportionate choice. No new fixed line-count threshold, review quota, posture worksheet or replacement label gate is proposed. The supervisor challenges unnecessary process as well as missing investigation, using the existing record and the question of what the added work resolves. This does not yet establish an automatic detector of excess process.

Rowan's `c8a01020-ff8f-45f4-b9e7-2f2e18d17d27` clarifies the role boundary. The orchestrator chooses execution posture; the PO owns product intent. A well-understood restoration of agreed behavior needs no new spec or PO acceptance ceremony merely because code behavior changes. If the specification itself misses intent or a repair changes a user commitment, route that question to the PO. Every new spec still gets presented, without manufacturing one solely to enter the process.

Acceptance pair: an understood regression is corrected with proportionate verification and independent review, without a fresh discovery/spec cycle; a similarly small patch that changes a product commitment receives PO judgment. A small but consequential implementation can warrant substantial technical scrutiny. Size decides neither case. Expanding work requires a reason in its uncertainty or consequences; existing delegation and review records should make the choice inspectable without a separate mandatory form.

Also replace feature-cycle step 0's blanket statement that every remaining step applies to light work. Select the delivery and review steps that the actual ask and protections require; do not preserve a full ceremony merely after skipping spec creation. Explain the choice when useful in the ordinary assignment brief, without a separate posture card or new required field. The current gates accept either historical light or heavy tokens equally; they cannot establish that the selected work is proportionate.

Acceptance examples: incorrect validation under an existing contract goes directly to correction, focused verification and proportionate independent code review; a one-line authorization change gets scrutiny appropriate to its consequences; novel behavior or architectural uncertainty gets the necessary investigation, specification and PO opportunity. No extra spec or spirit rerun is created solely for ceremony. These are evaluation cases, not a fixed size threshold or proof an ungated alternative works.

The two posture gates remain an unresolved replacement design, not unconditional deletions or a concluded decision to restore them unchanged. Evaluate the existing and proposed behavior against both underprocessing and overprocessing. This correction supersedes the revision 12 disposition and the earlier four-removals count.

### Preserve meaningful spirit review through supported records

Rowan and Orchestrator Editor inspected `feature-cycle/SKILL.md:13-17,98-129` and the PO guidance; the lead also read those source passages. A bounded assignment to the accountable PO on the same work item, followed by a wake with the current spec/result reference, intent question and timing consequence, supplies an existing route. Under the current blanket gate, use the supported assign-plus-wake route rather than claiming plain dispatch already permits this case. Existing records expose assignment ownership, delivery and response; they do not by themselves guarantee that the PO received an effective opportunity.

The PO can review, request corrections or explicitly judge that an existing intent disposition still applies. The orchestrator carries that disposition into the specification and affected work. Give the opportunity before dependent choices make correction ineffective. When material intent is unresolved, retain ownership and hold the work depending on that decision while separable authorized preparation continues. Recover unavailable PO ownership through the existing hierarchy; silence does not imply approval.

Use the existing open review responsibility when appropriate. If a prior spirit assignment is terminal and a new question arises, preserve it and open a bounded successor on the same item with the prior context; no reopen command is assumed, and a review link is not a generic successor link. This is reference-level local routing, not a new mandatory receipt format or approval token for every slice.

Conform PO guidance and feature-cycle together. Remove the once-per-item absolute, the indefinite-wait framing and the assumption that a historical token settles every subsequent slice. Every new spec is presented; unchanged slices can retain a still-applicable disposition. Product spirit judgment and independent technical review answer different questions and neither substitutes for the other. Existing reminder/recovery design must make lost delivery and unavailable ownership visible. A new registry or universal notification algorithm is not established by these records.

Acceptance: a technically clean specification that misses intent reaches the PO early enough to be corrected; preparatory recon continues; a changed result reaches the PO before the affected consequential decision; a queued wake remains visibly pending; existing judgment carries across unchanged work only when its scope still applies.

### Separate review protection from enforced sequencing and staffing

- `completion-requires-review`, engineering rules lines 7-26: preserve the applicable independent-review protection for consequential output. Its current remedy always assigns reviewer-code, including for policy, release and live mutation. Proposal: replace automatic specialist selection with useful missing-review evidence routed to the accountable orchestrator, who chooses the appropriate independent reviewer and reuses valid work. The protected completion remains blocked until its applicable independent review is satisfied. This does not require a new acknowledgment or owner-acceptance record. Exact routing must reuse a supported path and be verified before implementation is considered ready.
- `code-review-requires-passing-tests`, lines 53-64: the existing unlinked recon route proves independent diagnosis is available while tests fail. It does not justify barring all linked reviewer engagement before a passing-test receipt. Proposal: retire the blanket review-assignment admission veto so the orchestrator can commission useful review when appropriate. Preserve producer linkage, reviewer independence, truthful verdicts and applicable current verification at clean acceptance and consequential delivery. A reviewer can report failures or changes requested; early review does not certify readiness. Do not move a historical tests-passed token to another gate and claim it establishes evidence applicability. The exact acceptance consumers and any needed evidence check must be specified and verified before this policy is implemented.

Acceptance: independent review can examine incomplete or failing work, and its findings remain linked and attributable. Known unmet acceptance requirements cannot be converted into a clean or ready claim. Review of policy/spec output is assigned to an appropriate specialist. Reconciliation that invalidates evidence triggers new judgment; a changed identifier alone does not automatically invalidate it.

A linked reviewer can examine failing code and file findings or changes requested without inventing a passing-test receipt. That review does not qualify the producer as clean or complete. After fixes, applicable current verification and independent review of the changed result support clean acceptance. Preserve the latest linked review-conclusion semantics: an older clean verdict cannot override newer changes requested. The b299 consumer does not itself prove revision freshness or test truth; those remain explicit acceptance-design and verification obligations. No mandatory preliminary-review phase is proposed.

This supersedes revision 09's broader conclusion to retain the admission gate unchanged. Its narrower source finding about recon remains correct. The new conclusion follows the expanded product question about agent-owned sequencing.

### Preserve evidence while assessing coarse proxies

- `completion-requires-verification`, verification rules lines 2-18: a coder completion requires a verified verdict and the remedy wakes its holder. Keep the requirement to establish applicable verification at completion. Assess whether existing recorded evidence already establishes it before requiring another special receipt. A verdict kind is not proof of current tested revision, sufficient coverage or actual fulfillment. Do not remove evidence protection as routine paperwork.
- `completion-requires-results-artifact`, lines 49-64: selected deliverer/reviewer roles need a holder-recorded artifact. Its documented purpose includes preventing loss of deliverables when workspaces are removed. Preserve durable results and reasoning. Assess assignment/work-item scope, retention and reuse of already sufficient artifacts; do not require a redundant document merely because an investigation is small. No blanket removal is proposed. A retention-safe alternative needs a concrete design before narrowing this gate.

Acceptance: required output remains retrievable after workspace cleanup; existing sufficient evidence can be used when applicable; a token or unrelated work-item artifact does not certify a different promised outcome. The holder and supervisor remain accountable for the result.

### Narrow tool guards to their protection

The five `rails/engineering.toml` guards cover mutating stash, reset-hard, clean-force, checkout-discard and all restore commands. Their stated protection is custody of other agents' work. Keep that protection. These command patterns do not establish actual ownership, and `no-git-restore` explicitly acknowledges blocking harmless `git restore --staged`.

Proposal: narrow the documented harmless-unstaging overmatch and assess the other matchers against their actual destructive effect. A safe matcher change must preserve the protected destructive forms across supported command syntax and harness adapters. Do not turn textual evasions into the agent's workaround or claim a regex is a complete security boundary. No unverified replacement pattern is prescribed here.

### Distinguish approved wait accountability from record integrity

Wake Rails remains product-approved. Morrow's candidate inspection at `926774a30fb79df5c66015b118689b8be45aa350` identifies an independent-verifier contract: registration requires an accessible open verifier assignment and matching admission policy; coverage requires accountable verification. This is a chosen workflow policy, not merely tenant or predicate integrity. A real producer dependency without the required verifier can be refused.

Keep the existing approved contract visible in the plan. No removal is proposed by this assessment. The concise guidance must name the open independent-verifier requirement because it is a local fact agents cannot infer. Any future choice to accept a self-explained wait would be an explicit policy/mechanism delta across admission, coverage and effort relief. Gentler wording cannot supply it.

Retain ownership, creator, tenant and predicate-evidence integrity. Keep registration, valid coverage, delivered notification and fulfilled dependency distinct.

## Hard-coded checks and the reliability path

`dispatch.ex:74-166` evaluates statutes before the ordinary handler and can deny, invoke a remedy or escalate. Assignment idempotency and terminal-item checks occur before that. Statutes therefore do constrain the calls agents make, regardless of contrary guidance.

`assignments.ex:1191-1240` requires lifecycle attestations from the actual holder on an open assignment; `1300-1313` restricts revocation to opener/admin. Keep these attribution and lifecycle protections. Recovery must preserve what the predecessor did, using supported succession/disposition. It must not fabricate a predecessor's completion. `1631-1673` constrains evidence references; correct malformed admission using real evidence rather than pretending the work never happened.

`supervision.ex:2964-3024` hard-codes a bounded checkpoint and disallows a consecutive checkpoint without another effect. `3132-3175` includes session-wide running/queued suppression and scheduled-wake, work-blocked and outage conditions. These determine attention eligibility, not authorization of a protected product action. The existing qualified-wait integration and proposed less-repetitive reminder policy must address these mechanics explicitly. Unrelated activity must not hide an obligation that needs attention.

`effort_checkin.ex:1-18,475-558` treats artifacts, attests and work-item updates as effects, prods after one silent bracket and opens a routed decision request after continued silence. This is not itself proof that work is blocked, nor that no product progress occurred. Its signals and automatic escalation need to participate in the same reminder policy. No-filing alone should produce a question for the responsible agent, not a conclusion that its authority vanished or a demand for meaningless progress prose.

The b299 predicate-rule engine admits deny, remedy and escalate effects, `rules.ex:433-440`. The staged review-doorbell comment explicitly says a nonblocking notice is not supported there. Consequently, retiring a gate does not mean changing its effect to an invented notice value. Use existing communication/supervision for relevant attention, or identify the smallest additional mechanism needed. Do not create duplicate timers or a second obligation registry.

## Guidance conflicts found alongside enforcement

Kestrel identified another included contradiction at `guidance/engineering-tenets.md:5-8`: it cites a live spec as authority, then directs adjudication when a clause requires behavior change. Replace that clause with the shared authority boundary alongside scope and coder wording. Also remove the inference that a rejected final step necessarily proves earlier work was skipped. A rejection can reveal an overbroad rule or malformed evidence admission.

Kestrel reports defect-first escalation prose in local coder guidance while it is absent from shipped b299. Read actual composed guidance during delivery validation. A branch-only text fix does not establish that active agents receive it.

## Delivery and observation

The plan must name the rule changes, relevant guidance changes and hard-coded policy changes together. Preserve current enforced refusals until an authorized change is delivered. Runtime validation should identify the loaded rule version and projected hook coverage, then exercise the product acceptance cases through the actual enforcement path on an authorized test host. Merely reading a shorter prompt or checking a TOML file is insufficient.

Observe whether authorized work proceeds without redundant receipts, supervisors choose appropriate recovery, real evidence remains available, and genuinely protected actions still refuse correctly. Measure unwanted blocking and lost attention alongside successful refusals. An enforcement system is not successful merely because it never permits an action.

This assessment supports targeted policy/mechanism changes within the existing architecture. It withdraws the earlier confidence that the repair was adequately assessed without these changes. Exact spirit-review opportunity and recovery routing, review-acceptance design, retention-safe artifact narrowing, safe tool matching, reminder delivery design and loaded-runtime verification remain explicit engineering work, not reasons to reopen the already approved Wake Rails product behavior.

## Domain evidence

- Orchestrator Editor: `b780ecf3-6110-4a67-bf36-2add8d4a754d`, workflow gates and configured/source distinction; `6318e1be-50ba-4b15-b85f-ac7bbf0e6850`, attribution, evidence and tool boundaries; `9c542857-de6b-4d5f-b01f-258c722ffe5c`, gate retirement and limits of the prior recon conclusion.
- Rowan: `e555321c-e80b-4072-b7bb-f5b71ffa6c39`, spirit gate scope/staleness, PO responsibilities and lifecycle protection.
- Kestrel: `96999535-2498-4189-af2d-95532fcd5e2b`, Firehose exposure, automatic reviewer choice, shared tenets conflict and configured/source differences.
- Morrow: `d00ead00-3d69-4979-8121-ceb01d6e0184`, hard-coded prod eligibility and candidate independent-verifier requirement. Candidate details are attributed source inspection; the lead did not run it.

Domain contributions inform the lead's proposed composition. They are not approval of unseen later text. No unanimity or acknowledgment round is required.

Mike's subsequent clarification in this conversation is authoritative for the spirit requirement above. It was relayed to domain owners in `fc3dfe14-8728-4fd1-99cb-8cea088ef865`; it corrects any interpretation that retiring the blanket dispatch veto may remove meaningful PO review of product intent.

Spirit routing contributions: Rowan `4fdf4e60-7f93-4ec1-8ab8-b6bd1b608d2b` and `87859dd5-19c6-40b4-afc9-d0dbfef5fba4`; Orchestrator Editor `22faa583-8ebb-4de3-b3b3-c26fdba4b375`. They establish a supported record route, not a completed automatic delivery guarantee.

Orchestrator Editor's focused revision 11 follow-up `f055b9a8-c995-4cf1-9163-da28e2f1de6f` informs the linked failing-code acceptance case and explicit spec/code reviewer routing. It reports no further role-boundary objection, without claiming the remaining mechanisms are designed or installed.

Orchestrator Editor's `21996d7e-992f-499c-979c-455888fd1cbb` identifies the blanket remaining-steps clause in feature-cycle and supplies the contrasting proportionality cases above. The contributor favors removing the veto with a positive small-fix duty and composed guidance changes; no observed trial of that alternative is claimed.
