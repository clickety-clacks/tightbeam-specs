# O2 current acceptance and accountable review routing

8 September 2026. Selected lead design for 0.1.9, returned for independent engineering acceptance and implementation through the existing O1/O2 executive. This is externally authored design, not implemented or tested behavior.

O2 permits useful independent review before verification passes. Completion still requires truthful applicable verification and independent acceptance. When review is missing, Tightbeam records and delivers the need to accountable orchestration. It does not choose or staff the reviewer.

## Basis and custody

This document completes the corrections in [the recovered design assessment](tightbeam-019-o2-recovered-design-assessment-2026-09-08.md). Preserve that file and its unchanged predecessor artifact `art_96871dce`, SHA256 `4541f6c50afc88534d6f3e7c8798f557d22088d6e8f3002af522195ad518c631`, as history. Where they differ, this document controls the selected O2 design.

The existing executive recorded external handoff in `att_2f647d4f-8e37-4dac-8016-27613dcd9769`. It reconciled the second designer's clean specs clone, revoked its assignment and retired its session, and revoked an unstarted replacement contribution. No partial source or design result was found in that bounded reconciliation. Failed-unknown history remains evidence, not proof that all possible external effects were absent. O1's active source producer remains untouched.

The delivery home remains work item `wi_fcbc79fe-8b77-42d7-a5ba-0d890359d0f9`, PO assignment `asg_915cc133-51a4-471f-94a6-be7515f4a5e7` and executive `asg_0b176aee-5650-490c-80de-2bafcbacf9b2`. The executive arranges independent engineering assessment of this result and exact source allocation. No third internal designer or parallel O1 editor is needed.

Source checks used immutable code baseline `b299457d5c95dd6e161ed9b1de70b4450b5166b7`. The final implementation must compose with reviewed late-ruling `57bc449c9478ed37170e3fe9981f6fc0fa6cc457`, accepted WakeRails and the released remedy/R1 hunks. Baseline line numbers identify inspected code; they are not final-candidate proof.

## Kungfu changes and substrate changes

Kungfu removes `code-review-requires-passing-tests`. It retains consequential-completion independent review, changes its remedy from forced `reviewer-code` assignment to accountable notification, and conforms coder, reviewer and orchestration guidance. O1 owns those shared text and TOML hunks in the final composition.

Substrate code adds applicable code-evidence selection, accountable recipient binding, durable wake outcome reconciliation and an internal reassessment consumer. One nullable versioned `noticeState` column on existing `rail_remedy_episodes` stores the notification protocol. It preserves holder attribution, open-assignment lifecycle, direct producer-review linkage, independent judgment and terminal transaction integrity. Removing the admission predicate alone does not deliver O2.

## Applicable code evidence

The code result seeking completion is the nonempty canonical set of its existing `commitRefs`. A qualifying ref names the producer-result repository locator and a full immutable commit OID. Validate that it is a commit at the declared supported repository, normalize hexadecimal case, sort the set, and reject duplicate repository/OID entries. Do not resolve a historical branch, tag or abbreviation later and reinterpret the old judgment.

The repository locator identifies the producer result. A reviewer using another clone records that inspection location in its evidence note or report and attests the same producer-result refs. Different clone paths or equal remote URLs do not silently establish identity equivalence. A changed locator can be covered by an attributed applicability judgment using the current canonical refs.

Existing producing-completion and review-verdict refs remain the transport. Permit refs on the producer holder's `verified` verdict and optional refs on its `verification-failed` verdict. Add the narrow verdict value `verification-failed` to express retraction or contrary verification through the existing `kind=verdict` path. This adds no table, receipt kind, separate phase or mandatory preliminary report. It must be documented as a local evidence convention and recognized by CLI/API validation and the completion consumer.

For code completion, the transaction must:

1. Use the prepared canonical refs that will actually be stored on completion.
2. Select the latest holder-authored `reviewed-clean` or `changes-requested` conclusion across directly linked review assignments, ordered by timestamp and rowid as today. Select before checking applicability.
3. Require that winning row to be independent, clean and applicable to those refs. A newer adverse conclusion cannot be hidden by an older matching clean row or an unrelated verdict.
4. Select the latest holder-authored `verified` or `verification-failed` conclusion on the producing assignment before comparing refs. Require the winning conclusion to be positive and applicable to the current refs. A negative may omit refs when the holder must retract verification before the result identity is known; it still defeats the earlier positive conclusion.
5. Preserve applicable existing artifact, authority and lifecycle checks.

Prepare Git validation outside the database transaction. Rule evaluation and insertion must consume the same canonical result, and the final transaction must re-read the relevant conclusions. An adverse conclusion committed before completion wins must defeat stale acceptance. If the existing dispatch seam evaluates earlier, add a transaction-level recheck rather than claiming the earlier read closes this race.

Refs establish identity, not truth. The producer and independent reviewer judge whether evidence remains applicable after a rebase, repair or changed locator. They may record a current attributed applicability conclusion citing sufficient existing evidence and its limits. This does not require rerunning unchanged checks or repeating a complete review merely because a SHA changed. An open review can record the new conclusion; a closed review uses the supported bounded successor linked to the producer. Never fabricate a test run or a predecessor's action.

Legacy attests remain unchanged. Existing full immutable refs may qualify when they match the current canonical set and satisfy attribution and conclusion rules. Mutable or incomplete historical refs remain useful evidence to agents but cannot mechanically qualify current code acceptance. A current applicability conclusion can cite that evidence without rewriting it.

Policy, release and live-mutation effects retain the existing latest independent linked-conclusion protection. O2 does not require fictitious Git refs for those effects or claim to add equivalent immutable non-code result matching. Their reviewers remain responsible for applicability to the actual result. The notification and recovery design below covers all protected producing effects.

## Accountable review need

Keep the existing remedy episode identity: statute, actual producer assignment as `subject`, and occurrence. Result refs and current review evidence are notification context, not part of this identity. A changed SHA alone does not create another notice episode. This identity works for code and non-code effects.

Resolve the recipient from attributed ownership inside the scheduling transaction. Read the assignment opener and work-item owner. Use the active opener session while it belongs to the current work owner. If ownership changed, the opener is unavailable, or the assignment was opened by a user, use that accountable user's existing Main. Validate tenancy and current routing. If no recipient exists, retain the blocked need and expose the precise missing owner; do not invent a role, identity or reviewer.

The first notification states the producer, current result/evidence context and missing independent judgment. It asks the accountable agent to choose appropriate spec or code review, reuse capable existing review, or resolve the actual restriction. Delivery is not commissioning. Commissioning is not acceptance. A historical linked review does not prove that its holder is available or that its judgment covers the current result.

Use the root notification's actual `wakeId` as this wake remedy's `producerKey`. Update wake-specific episode lookup and idempotency handling together. Other remedy action types retain their own meanings. Existing episodes whose `producerKey` contains a session or assignment must be resolved through their stored action/idempotency and actual producer records. Preserve existing review custody; do not reinterpret an assignment ID as a wake or automatically restaff after the rule changes. Unresolved legacy identity is a visible recovery case, not proof of delivery.

Add nullable versioned `noticeState` to this existing episode row. It records the current blocked-result context, review-need state, root notice, typed recovery edges containing causal parent attempt, purpose, recipient and wake ID, observed causal changes, and pending reassessment generation, wake ID and due time. Validate its version and agreement with `producerKey`. A refused completion is not a stored completion attest, so its canonical result context must be retained here for later evaluation. Update changed context in the same unresolved episode without changing its identity.

Recovery notices are new wakes, not automatic-retry or turn-repair edges. Store their explicit episode/parent/recipient linkage atomically with creation in `noticeState`; traverse those links as well as the existing retry and repair tables. Do not reconstruct this graph by parsing notification prose or scanning arbitrary idempotency-key prefixes. Limit active recovery state to the current episode and acyclic accountable owner path. Historical wakes and lifecycle records retain prior evidence. Schema upgrade leaves old rows null until their actual producers are reconciled; no separate registry is added.

## Notification outcome and recovery

Use a typed outcome lookup across the root wake, `turns.wakeId`, existing `wake_retry_attempts` and authorized `turn_repair_attempts`. The latter is essential: `Ledger.repair_terminal/5` can create a successor turn without a wake ID. Preserve the original wake and source/attempt sequence lineage. A repaired turn may supply the later delivery result; enqueue or a fired wake never does.

| Evidence | Treatment |
| --- | --- |
| Pending with routable recipient; queued or running consumer | Preserve the attempt and reassess. Do not create a competing notice. |
| Durable delivered consumer in the authorized lineage | Record notification delivery only. Keep acceptance and review ownership separate. |
| Fired wake without a consumer or supported repair lineage | Preserve a delivery inconsistency and route effects reconciliation. Do not infer success or replay the commissioning request. |
| Pending recipient no longer routable | Cancel the still-pending attempt through supported attributed cancellation, then route a recovery notice to the accountable successor. Recheck state and recipient transactionally. |
| Proven rate-limit failure | Reuse the existing bounded retry policy and lineage. Do not introduce a second retry or change its eligibility. |
| Other failed or canceled result | Preserve the actual reason and route reconciliation. Explicit cancellation is not permission to resume. |
| Failed-unknown result | Ask the responsible agent to reconcile effects. No linked review is not evidence of no effects. |
| Recovery notice fails | Route the changed failure to the next supported accountable owner, deduplicated by causal attempt and recipient. Keep the unresolved fault visible if that chain is exhausted. |

A recovery notice asks what happened and what remains authorized. It does not repeat the original commissioning instruction as though the previous attempt did nothing. Agents may use ordinary assignments, wakes and attributed dispositions to recover. The mechanism must not parse free-form prose into automatic retry authorization.

Follow only explicitly recorded repair relationships. Late callbacks and competing terminal observations must not regress an already committed delivered result or authorize another attempt. Unknown effects remain historical evidence even when an authorized successor later delivers. Correlate with R1's consumer/claim identity at the shared implementation seam; no generic wake retry is introduced by O2.

Validate each repair edge against its source, assignment and recorded principal. Return delivery evidence and outstanding attempts separately rather than choosing a single latest branch. If an authorized successor delivered while another branch is queued, running or outcome-unknown, notification delivery is proven and competing execution still needs owned reconciliation. Send no additional notification retry. Recheck the complete recorded lineage immediately before scheduling a successor; timestamp, similar prompt text and session activity cannot substitute for lineage.

Changed ownership is evaluated even if an old review exists. The responsible agent judges that review's continued capability and applicability. The mechanism reports relevant changed ownership, failure or review-lifecycle evidence, and creates no reviewer. Deterministic notification keys include episode, causal change or failed attempt, notification purpose and recipient. Repeated scans of unchanged evidence cannot generate another recovery chain or cycle back to the same failed recipient.

## Reassessment and transaction boundaries

Do not depend on another completion attempt to discover stranded delivery. Reuse the existing internal wake-consumer facility with one new `review_remedy_reconcile` consumer registered by Gateway. For the first implementation, schedule its reassessment using the effective configured supervision interval. This is internal evaluation, not a promise or requirement to notify agents at that frequency.

Use the existing internal wake prompt payload for a versioned episode reference. Initial episode creation, its notice identity and the first reassessment must be durable together. Each consumer transaction validates the episode occurrence and producer/work-item state, consumes its own wake, observes actual delivery/ownership evidence, schedules any justified recovery notice and persists the next reassessment in `noticeState`. Publication happens after commit. The consumer owns durable consumption; it must not rely on prompt-wake auto-marking.

Keep at most one pending reassessment for an episode. Its persisted identity and due time must survive restart. Duplicate delivery or an old occurrence callback loses the conditional update. No separate timer service or review registry is needed. On upgrade, perform a bounded idempotent reconciliation of existing open episodes and their exact idempotency producers, creating a missing reassessment without inventing successful notification or repeating a historical assignment remedy. Ambiguous historical dispatch gets one deduplicated reconciliation request. A consumed generation cannot be rearmed by repeated bootstrap.

Evaluate the recorded missing-review context using the same latest-conclusion and applicable code-ref rules as completion. When qualifying review resolves that recorded need, record it satisfied with the closing evidence and stop ordinary review-request notices and checks. This does not certify verification, completion, or an unrecorded later result. Close the episode once any separate recovery-notice tracking is also discharged. A later actual refusal reopens a closed episode through the existing occurrence CAS; while recovery still holds the episode open, update the review-need context in that same occurrence. Keep results-artifact and verification failures distinct from missing independent review; they do not automatically create another reviewer request.

Re-read assignment/work-item lifecycle before every notice bind, cancellation, reassessment or successor action. If terminal transition wins, create no new review-request notice and dispose of its pending internal work through the supported transaction path. If scheduling wins first, terminal disposal must still remove its pending review-request work. Closing this notification episode never completes an assignment or erases unresolved unknown-effect evidence.

Terminal or satisfied review need stops stale review-request prompts, but it does not erase already-started unknown or competing effects. Preserve those attempts and route their reconciliation to the accountable owner through an explicitly linked recovery notice. Track that recovery notice's delivery independently until delivered, governed cancellation, or visible owner-chain exhaustion. In `noticeState`, terminal review need cannot return to requested; the episode may remain live solely to track its existing effects-recovery handoff. The recovery message names the terminal producer as historical causal context and uses the accountable owner's supported delivery scope; it cannot reopen or act as the closed producer. Once delivered, further effects reconciliation is the agent's recorded responsibility; its delivery is not a mechanical claim that those effects were resolved. Do not keep a fulfilled product assignment open solely to host this separate recovery obligation.

An explicitly withdrawn notification puts automatic notification into a stopped state. Bootstrap, repeated refusals and occurrence reopening must preserve that stop; they cannot recreate the canceled request under a different transport or recipient as a bypass. The independent-review requirement remains. The accountable agent may commission review or communicate through ordinary supported operations without a new resume ceremony. Record the restriction for the responsible agent. Similarly, an explicit hold on the affected operation remains in force while separable authorized work proceeds.

Inspect the typed cancellation record. Follow an explicit replacement and stop on fulfilled/disposed obligations, `requester_withdrew`, or an applicable governing suppression such as `production_unmatched`. Bootstrap must preserve these stops. Retirement or unresolvable routing can justify owned recovery only after checking the cause and current owner. The b299 cancellation allowlist does not yet authorize the new consumer. Add a narrowly scoped `tightbeam:rail-remedy` requester entry for its own episode-linked wakes and genuine superseded, obligation-disposed or target-unresolvable cases, retaining causal-reference and outcome validation. Never impersonate another allowed process.

The chosen internal reassessment needs focused queue-growth verification. Ordinary review-request checking stops on terminality. Any remaining check tracks only the separate effects-recovery handoff and ends at delivery, governed cancellation or recorded exhaustion. That recovery check, like its notice, uses the accountable owner's delivery scope; terminal producer/work-item IDs remain historical causal payload rather than active wake bindings that terminal-disposal selectors would delete. Unchanged review work must not generate repeated agent prompts. Ordinary effort and R1 reminder policy remain separate; this consumer cannot suppress required effort decisions or reset R1 success clocks on evaluation.

## Implementation and acceptance

Allocate one composed implementation against the released shared predecessor. Principal seams are `Assignments` evidence validation/selection and final completion transaction; `Dispatch`/Gateway preparation; `Rules` applicable facts; `RailRemedy` ownership, episode and wake-ID handling; `Wakes` and Ledger repair-lineage outcome lookup; Gateway internal-consumer registration; and supported upgrade initialization. Preserve late-ruling/WakeRails atomic publication and terminal disposal. The O1 owner supplies the TOML and guidance hunks; no second editor changes them independently.

Independent engineering acceptance must verify these behaviors on the actual composed candidate:

1. Linked review of failing code records honest findings without tests-passed fiction. It cannot supply clean completion until applicable verification and independent acceptance exist.
2. Latest adverse review or verification defeats older positive evidence, including concurrent completion, mismatched revisions and unrelated later notes. Self-held, unlinked and descendant evidence cannot qualify.
3. Full immutable refs work across reviewer inspection clones using declared producer identity. Mutable old refs are never reinterpreted. Justified current applicability can reuse real prior evidence without a fake rerun. Duplicate or invalid refs fail with an actionable error.
4. Code, policy, release and live-effect missing-review needs notify the accountable owner and create no automatic reviewer. A historical, revoked, unavailable or stale review does not suppress owned recovery.
5. Duplicate completion attempts and reassessments retain one episode and notice lineage. Cover all outcome rows above, authorized wake and turn repair, mixed successor branches and delivered-plus-running siblings, unavailable/changed recipient, owner-chain exhaustion and explicit cancellation.
6. Crash/restart before and after notice creation, terminal consumer commit, repair binding, reassessment scheduling and publication preserves truthful pending/delivered state. Unknown effects are not replayed from absence of a review card.
7. Upgrade handles actual legacy episode producer types and ambiguous bindings, and preserves existing review assignments, waits and queued work. Repeated bootstrap and restart after explicit withdrawal do not rearm a canceled notice. Terminal assignment/work-item races leave no surviving stale prompt or internal reassessment.
8. The final O1/O2 combination permits the understood small-fix path, timely PO influence and useful early review while preserving independent acceptance. It adds no preliminary review phase, posture token or notification receipt ceremony.

The lead selected this as the best current design, not a demonstrated cure. Record implementation, exact-candidate evidence and actual exposure against the existing learning-loop hypotheses. Independent assessment may identify a concrete defect to correct before implementation; it need not reopen the settled operating principle or numeric reminder policy.


## Exact cancellation-contract precedence for 0.1.9

This section reconciles the selected O2 notification behavior with archived cancellation spec `art_b21e079d`, SHA256 `62255b57b1dc4e11a8a545f7abf0ccb3565c1334510263c8c7efb2b7d1f88780`. It consumes coordinator `att_74eb044a` and cancellation-owner `att_2e776195`, plus the exact schema reservation SHA256 `32c8b62367dd91ec99f5911b6a5a944ac95244df6e7e481c824d0536f3ecc580`. The lead read and hash-verified both documents; independent bounded review agreed with these restrictions. The archive remains unchanged historical evidence.

Only the following two internal `tightbeam:rail-remedy` tuples take precedence over the older closed matrix and requester admission. This is not a general process-cancellation exemption.

1. `target_unresolvable / scheduler_delivery / replacement` supersedes the old R14 no-replacement-only restriction and A5/A8 exclusion for this requester. The old wake must still be pending, its recipient currently unresolvable, and either the current episode review need requested or the narrowly defined existing effects-recovery handoff below still required. Validate the exact versioned episode/current occurrence, old wake or validated retry ancestry, current accountable recipient and tenant scope. The different replacement must be pending and linked to that same episode and primary obligation under R8. Its causal edge, cancellation and notice-state compare-and-set commit together. Recheck all predicates in that transaction; a losing attempt rolls back newly created rows or reuses only the verified winner. The replacement remains the R11 surviving trigger.
2. `superseded / wake / no_replacement` supersedes the old R14 replacement-only restriction, A5/A8 exclusion, and R11/R12 plus their dependent T4 surviving-trigger/action-needed requirement only for this requester and a proven satisfied, terminal or withdrawn review-notice need. Re-read the exact episode/current occurrence, wake linkage or validated retry ancestry, current need and its governing evidence transactionally. A requested need refuses this branch. Linked underlying work may remain open while this stale notice has null liveness-trigger fields and `actionNeeded = 0`. These fields describe cancellation of the notice only; they neither complete the underlying assignment/work nor prove effects reconciliation.

Preserve all already-started unknown or competing attempts and their owned recovery handoff. A terminal review need cannot return to requested, and an explicit withdrawn stop survives bootstrap, repeated refusal and occurrence reopening. The terminal/satisfied effects-recovery clarification below supersedes the earlier blanket exclusion of terminal-scope replacement. R8's same-primary restriction remains. Recovery retains its own valid owner delivery scope and evidence.

No `obligation_disposed` tuple or other requester/reason/source/outcome combination is added by this two-case reconciliation. All unrelated R8-R14/A1-A8 rules, primary-work derivation, typed causal references, pending-state first-winner behavior, row/foreign-key/trigger checks and rollback guarantees remain. SQL shape permission does not substitute for same-transaction episode authorization.

The sole combined schema writer must update actual existing constraints through the guarded ordered upgrade, preserve old cancellation rows and trigger/foreign-key behavior, and prove fresh/upgraded parity and unknown-predecessor refusal. O2 owns focused positive and negative tests for the two tuples, wrong process, cross-episode or stale occurrence, invalid retry ancestry, requested-need disposal, recipient/tenant mismatch, fire/cancel races and rollback. Preserve reported failures until tested against the actual allocated schema predecessor. This precedence resolves the specification conflict; it does not grant shared edits, new schema numbers, source transfer, landing, public export, installation or release acceptance.


### Existing effects-recovery notice after terminal or satisfied review need

This clarification reconciles the already-selected effects-recovery delivery obligation with the requested-review predicate above. The concrete unsupported transition was preserved in owner handoff `w_b7f4da1d-5322-424d-90ab-c98fb3030432`. Independent bounded review confirms that the same cancellation tuple can express the required transition without broader process authority.

For `tightbeam:rail-remedy / target_unresolvable / scheduler_delivery / replacement`, the need predicate may alternatively be an already-recorded, pending effects-reconciliation notice in the same version-1 episode and occurrence, with terminal or satisfied review need and a still-required, undelivered recovery handoff. The old recipient must actually be unresolvable. Validate exact notice purpose, causal attempt, retry/repair lineage and current accountable tenant-valid successor in the cancellation transaction. Retarget only that existing effects handoff within its valid owner delivery scope, preserving R8 primary-obligation checks, causal references, pending-state first winner, paired replacement/cancellation/notice-state update and rollback.

Re-read the complete authorized attempt lineage before replacing anything. A delivered result forbids another delivery attempt. Healthy pending notices, queued/running consumers and eligible bounded rate-limit retries remain in place across ordinary reassessment. Unknown or competing effects are not proof of safe replay. Explicitly withdrawn or suppressed recovery remains stopped. Deduplicate by causal attempt and recipient, preserve visited/exhausted owner-chain evidence, and never cycle back merely because another scheduler check occurred.

This exception does not create a new review request, change terminal review need back to requested, imply that unknown effects were reconciled, or move a closed producer/work item into active wake scope. Historical producer IDs remain causal context. The notice's delivery still transfers reconciliation responsibility rather than proving fulfillment.

Required focused regressions cover genuinely unroutable existing effects notices after both terminal and satisfied review need, exactly one replacement and stable subsequent checks, and preservation of the stopped ordinary review request. Negative cases cover delivered or healthy pending/running/retrying attempts, withdrawn/suppressed recovery, wrong purpose/episode/occurrence/ancestry/recipient/primary obligation, exhausted chains, competing execution and a losing transaction. Existing positive and negative requested-review cancellation tests remain. No additional tuple, schema-shape exception, source owner, public authority or release acceptance is granted by this clarification.
