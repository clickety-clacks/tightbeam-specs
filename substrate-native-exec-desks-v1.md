# Substrate-native exec desks — v1

Status: DRAFT FOR SUCCESSOR REVIEW. Authority: `wi_795a354d-3f97-4805-b472-b637c7542d54`, Mike's rewrite order `att_7ccdd6bf-48f6-46c4-86f4-f96609594e8f`, Mike's algedonic ruling `att_6b976672-6456-486a-808e-8ecbebcadb5f`, and review verdicts `att_46758d8c-b1aa-4e14-8a96-307cd5448ef3`, `att_b51166b7-2e39-4841-aac5-0dbfc518c6bc`, `att_6f42c78a-6a5d-4750-b918-55053f209828`, and `att_438b15ed-44ff-4335-9859-653448617a00`. Canonical home: repository `clickety-clacks/tightbeam-specs`, path `substrate-native-exec-desks-v1.md`. This text supersedes the reviewed changes-requested revision at `4af894567ff070c5ffee76b635dd2990a44f355d`; revisions `561ced6d0c7df35f5a3979b3d11185f752b32409`, `7a13f97d6f418d2bf3104828619d6d6073aebf57`, `d9fd29e22b197e3eaf511e70c7a045ec64f6f178`, `0767558eccfcdee974bee9d2b426c74e6f92fcc6`, and `ac965ae33852d6890b6ae2624d9a899fed1722cb` are provenance only.

## Goal

Put one lightweight exec in each participating worker's inbound path. Callers still address the worker. Each accepted wake reaches that worker's exec, which chooses only now or the next bundle. The exec may summarize, annotate, or escalate, but it cannot decide or change the worker's work.

Pilot one exec for Main. Compare the pilot with the reproducible Main cohort that `art_a4f39376` first identified before enabling another worker or another exec layer.

## Non-Goals

- This version does not mediate outbound traffic.
- It does not expose an exec address, give an exec its own exec, or give an exec an ACP session, workdir, shell, repository, filesystem, or assignment.
- It does not let an exec complete or alter an assignment, work item, review, decision request, ruling, identity, credential, target, release, or deployment.
- It does not create observation-request or observation-cancellation records.
- It does not replace the independent notice batcher described by `coordination-fabric-v1.md`.
- It does not choose org policy, a product target, or a 0.1.x change.
- Operating guidance does not change in this draft. Callers keep using worker-addressed `wake` and `dispatch`; no guidance may advertise exec behavior before it exists.

## Terms

- **Worker:** an addressable Tightbeam session that can receive a turn.
- **Owner Main:** the canonical Main session for the user who owns the addressed worker. It is resolved from the worker's recorded owner, not from the worker hierarchy.
- **Exec:** a lightweight agent bound to one worker's inbound delivery. It acts for that worker and has no public address or inbound exec binding.
- **BUNDLE:** one durable record that groups two or more wakes the exec chose to handle together. It records the worker, exec, ordered member wake ids, policy revision, summary text when produced, citations, outcome, cause, and times.
- **SUMMARIZE:** compose the text of one BUNDLE from its member wakes. One wake is delivered from its wake row and does not create a BUNDLE.
- **ANNOTATE:** deliver a wake or BUNDLE with one or more cited durable rows. The citations support the delivery; they do not decide work.
- **ESCALATE:** send context to an addressable authority worker. The send records its source wake or BUNDLE.
- **Activity-summary NOTE:** the single durable row for one worker and debounce window. It begins `pending` as the semantic-work claim and carries a nullable semantic-start tuple: time, execution-wake cause, and `process:tightbeam` principal. It then becomes `published` with a plain observation or `failed_with_reason` with a cause. A published row records the worker, exec, covered time window, write time, transcript evidence, and prior published NOTE. An empty window says `no activity since <window-start>`.
- **Org policy:** the versioned org-authored rules that select timing, model, effort, debounce window, bundle deadline, citations, and escalation destinations. Its concrete model id and effort define the light model for this spec. Policy is input to the exec; it is not substrate truth.

## Assumptions

1. `wake` and `dispatch` already persist a worker-addressed wake before delivery.
2. The landed wake row carries the class field defined by `coordination-fabric-v1.md`.
3. `nullable-effective-parent-v1.md` supplies the shared transaction-aware effective-parent resolver before exec escalation ships.
4. `derived-model-catalog-v1.md` supplies a concrete provider model id and effort for org policy to elect.
5. `wake-delivery-conservation.md` remains the authority for wake admission, delivery outcomes, retry, and restart recovery.
6. Durable decision-request history retains `id`, `question`, `decision`, `response`, `rationale`, `ruledAt`, `ruledBy`, `assignmentId`, and `raiserId` for a cutoff-bound Main baseline query.
7. Existing NOTE read authorization can permit a principal to read a worker's NOTE without permitting that principal to read the worker transcript.
8. Existing provider telemetry can record model id, tokens, elapsed time, attempts, deadline, and terminal cause for a direct model call.

## Invariants

1. **Worker address, exec delivery.** A public send accepts a worker target. An accepted wake reaches that worker's active exec before it can create a worker turn. A send to an exec is unrepresentable. (A1, A2)
2. **One timing choice.** The exec chooses only `now` or `next bundle`. It cannot withhold a wake past the next bundle boundary or reorder wakes by a private priority. (A3, A4)
3. **Visible outcome.** Each accepted wake has a delivery outcome on its wake state or belongs to one BUNDLE whose outcome is delivered, escalated, or expired with a reason. No accepted wake disappears. (A5, A6)
4. **Three verbs.** The exec exposes only `SUMMARIZE`, `ANNOTATE`, and `ESCALATE`. `SUMMARIZE` creates one BUNDLE only when the member count is greater than one. `ANNOTATE` names its cited rows. `ESCALATE` calls the shared effective-parent resolver when policy selects the parent route. (A7–A9)
5. **Two names.** An exec-authored BUNDLE, NOTE, annotation, escalation, or algedonic carrier turn records the worker it represents and the exec that performed the action. (A10)
6. **No work authority.** The exec can write wake outcomes, BUNDLEs, activity-summary NOTEs, citations, and worker-addressed escalation sends. No exec capability can write work or decision state. (A11)
7. **Event-driven split.** Durable arrival, turn-boundary, deadline, worker-turn-completion, and check-in events are the only exec triggers. Deterministic code handles routing, class use, grouping, citations, idempotency, deadlines, and outcome commits. A model handles semantic summary, annotation judgment, escalation judgment, or NOTE prose. Idle time causes no query, model call, or new wake. (A12, A13)
8. **Observation without authority.** A unique worker-window key permits one activity-summary NOTE row in a debounce window. One checked change from a null semantic-start tuple authorizes one semantic execution. Each check-in wake links to the NOTE row. Publication returns the same NOTE pointer to each waiting check-in; failure records one cause on the NOTE row and settles each waiting check-in with that cause. No check-in creates a worker turn. A published NOTE reports inactivity literally and does not infer health, progress, or cause. (A14–A19)
9. **Policy stays policy.** Tightbeam validates the elected policy revision and records it with each exec result. The substrate does not infer timing, escalation, or model policy. (A21)

## Architecture

### Inbound path

The existing worker session row names one active exec id and policy revision. An exec has no session row. `wake` and `dispatch` continue to accept only worker targets. In one acceptance transaction, Tightbeam reads those two worker fields and either persists the wake for exec handling or returns a typed refusal before writing a wake, dispatch assignment, or worker turn. The wake row is the durable record for direct delivery; there is no inbound-envelope record or separate binding record.

The shell chooses timing from durable message kind and the existing class field: following `coordination-fabric-v1.md`, a present `fyi` or `status-query` permits the next bundle, a present `input-needed` or `blocker` requires now, and no class sends agent or user messages now while substrate notices and effort check-ins may join the next bundle. Under `att_6b976672-6456-486a-808e-8ecbebcadb5f`, `algedonic` is a deterministic exception. For a worker other than Owner Main, the routing transaction admits the source wake itself to Owner Main. Its carrier turn uses that source wake id and records the represented worker and performing exec. The exec preserves the content and class without answering, absorbing, triaging, or reclassifying it. `wake-delivery-conservation.md` then records `handled`, retry, or `undeliverable` for that same wake and its own carrier turn. Restart resumes that wake's existing attempt state and cannot create a second carrier wake. If the addressed worker is Owner Main, its exec admits the same source wake to that Main worker. Main is the user boundary, and the fabric creates no second human carrier. This rule replaces the conflicting algedonic carrier text in `coordination-fabric-v1.md`.

The next bundle closes at the earlier of the worker's next turn boundary and the org-policy deadline, as required by `coordination-fabric-v1.md`. The shell creates or reuses one durable wake for that deadline; it does not poll. At close, one member is delivered from its wake row. Two or more members permit `SUMMARIZE`, which creates one BUNDLE with ordered member references. Direct delivery and BUNDLE delivery use the ordering and terminal outcome rules in `wake-delivery-conservation.md`.

`ANNOTATE` attaches cited rows to the delivery outcome of a wake or BUNDLE. `ESCALATE` creates an ordinary send to an authority worker and links that send to its source wake or BUNDLE. A parent-route escalation calls the resolver in `nullable-effective-parent-v1.md` inside the transaction that needs the resolved destination. The resolver grants no authority; the caller still applies existing send authorization.

The delivery-destination transaction named in Open Questions must commit the worker delivery and the wake or BUNDLE outcome as one indivisible change. Failure before that commit leaves the input eligible for idempotent replay. Expiry records its reason on the affected wake or BUNDLE. Model failure records its cause and raw-response reference when present; it cannot silently settle the input. The exec delivery service is the sole writer of BUNDLE and exec activity-summary NOTE rows.

### Activity summary

Worker-turn completion and check-in arrival are durable triggers. The trigger transaction reads the NOTE row keyed by worker and current debounce window. When no row exists, it inserts one `pending` NOTE; the insert winner also creates one immediately due execution wake keyed by that NOTE. When a pending row exists, each arriving check-in wake links to it and the trigger creates no execution wake. When a published row exists, the transaction settles an arriving check-in with its pointer. When a failed row exists, the transaction settles an arriving check-in as `expired_with_reason` with its stored cause. A worker-turn completion creates no work for a terminal row. The exec may read only its worker's bounded transcript window when the execution wake fires. Existing NOTE read authorization decides who may receive a published NOTE pointer; that permission never exposes the transcript.

Before a provider call, the execution-wake handler uses one transaction to set the pending NOTE's semantic-start time, cause `wake:<execution-wake-id>`, and principal `process:tightbeam` only when that tuple is null. Only the winner starts one bounded model call. In one terminal transaction, success publishes that NOTE, cites its source rows, points to the prior published NOTE, settles the execution wake, and settles each linked check-in wake with the same pointer. Failure changes the row to `failed_with_reason`, settles the execution wake, and settles each linked check-in wake as `expired_with_reason` with the same cause. After restart, a pending NOTE with a null semantic-start tuple replays its unsettled execution wake. A pending NOTE with a semantic-start tuple and no terminal result becomes `failed_with_reason` with cause `outcome_unknown`; restart starts no second model call and settles the linked wakes through the same failure transaction. The path has no observation-request row, cancellation event, polling loop, second model call in the same window, or NOTE-created successor wake.

### Runtime, policy, and pilot

Tightbeam runs semantic exec work as a bounded direct provider call on the concrete model id and effort elected by org policy from `derived-model-catalog-v1.md`. The call is not an ACP session and receives no workdir. Existing provider telemetry records model, tokens, elapsed time, attempts, deadline, and terminal cause. The credential source remains blocked by the credential question below.

Before Main pilot activation, the operator records `tightbeam version` and runs this exact baseline pipeline: `tightbeam --as-user mike decision-requests --status all | jq -c '[.decisionRequests[] | select(.ruledBy == "user:mike" and .ruledAt <= 1787842277183) | {id, question, decision, response, rationale, ruledAt, assignmentId, raiserId}] | sort_by(.ruledAt, .id)'`. The operator artifact-records the pipeline, cutoff, version, JSON output, and output SHA-256. `art_a4f39376` is seed provenance for this cohort, not custody of the baseline bytes.

The Main pilot report compares that frozen query artifact with the exec cohort. It records immediate worker turns, wakes deferred, BUNDLEs, annotations, escalations, expired inputs, NOTE-pointer check-in answers, model calls, tokens, latency, and named failures. Tightbeam enables no second worker or exec layer until both artifacts exist and the product owner records whether to continue.

This design adds only BUNDLE because direct sends already have durable wake rows and observations already have NOTE rows. Deleting mediation would preserve the measured interruption load, while accepting silent loss would violate wake delivery conservation.

## Acceptance

1. **A1 — Worker target.** Given worker W's session row names a valid exec and policy revision, when Tightbeam accepts a wake for W, then that exec receives the wake before any worker turn exists.
2. **A2 — Invalid target or configuration.** Given a caller targets an exec id or a worker row lacks a valid exec id, when acceptance runs, then Tightbeam returns the matching typed refusal and writes no wake, dispatch assignment, or worker turn.
3. **A3 — Timing inputs.** Given an unclassed agent message and an `fyi`-class user message reach an exec, when the shell chooses timing, then the agent message goes now and the `fyi` message goes now or in the next bundle. Given an `algedonic` wake reaches an exec whose represented worker is not Owner Main, when routing commits, then one turn admits to Owner Main with that source wake id, represented worker, performing exec, unchanged content, and unchanged class. Given that carrier turn reaches delivered, when its terminal transaction commits, then the same source wake records `handled` with that turn. Given delivery exhausts its lawful attempts or has an unsafe failure, when `wake-delivery-conservation.md` terminalizes the source wake, then that wake records `undeliverable`. Given the represented worker is Owner Main, its exec admits that source wake to the Main worker without creating a carrier wake.
4. **A4 — Bundle bound.** Given a substrate notice waits for the next bundle, when the worker turn boundary or policy deadline occurs first, then that event delivers the input and no private priority delays it.
5. **A5 — Direct conservation.** Given a direct delivery commits, when its rows are read after restart, then the wake names one terminal delivery outcome and no BUNDLE exists for it.
6. **A6 — Failure conservation.** Given delivery cannot finish before its deadline, when the deadline wins, then the wake or BUNDLE records `expired_with_reason` and the source remains queryable.
7. **A7 — Summary cardinality.** Given one queued wake, when the bundle closes, then the original wake delivers without a BUNDLE; given three queued wakes, then one BUNDLE lists those three wake ids in order.
8. **A8 — Cited annotation.** Given the shell attaches a closed-assignment fact to an effort check-in, when delivery commits, then the outcome cites that assignment row and contains both worker and exec names.
9. **A9 — Parent escalation.** Given policy selects the parent route, when the exec escalates, then the transaction calls the shared effective-parent resolver and the resulting ordinary send links to its source wake or BUNDLE.
10. **A10 — Attribution.** Given the exec writes a BUNDLE, NOTE, annotation, escalation, or algedonic carrier turn, when the row is read, then it identifies the represented worker and performing exec as separate fields.
11. **A11 — Capability floor.** Given an exec attempts an attest, assignment transition, decision ruling, or other work mutation, when authorization runs, then the operation refuses before mutation.
12. **A12 — Idle cost.** Given no durable exec trigger occurs during an hour, when execution evidence is queried, then it shows zero exec queries, model calls, and newly created wakes for that hour.
13. **A13 — Semantic boundary.** Given a deterministic pass-through or stored NOTE-pointer reply, when the shell handles it, then no model execution exists; given org policy requires semantic summary, then one bounded model execution cites its input and policy revision.
14. **A14 — Debounce.** Given a published NOTE and five check-ins inside its debounce window, when the exec handles them, then each receives the same NOTE pointer and no pending NOTE, execution wake, or model call exists for those arrivals.
15. **A15 — Initial single-flight.** Given no NOTE covers window W, when five check-ins and one worker-turn completion arrive concurrently, then one pending NOTE and one execution wake exist for W, each check-in wake links to that NOTE, one handler changes its null semantic-start tuple to the time, execution-wake cause, and `process:tightbeam` principal, and no second model call starts.
16. **A16 — Success fan-out.** Given six check-in wakes link to one pending NOTE, when its model result succeeds, then one transaction publishes the NOTE, settles its execution wake, and settles each check-in wake with the same NOTE pointer.
17. **A17 — Failure fan-out and restart.** Given six check-in wakes link to one pending NOTE, when its deadline or terminal model failure wins, then one transaction records `failed_with_reason`, settles its execution wake, and settles each check-in wake as `expired_with_reason` with the same cause. Given restart finds a pending NOTE with a semantic-start tuple and no terminal result, then it records cause `outcome_unknown`, settles each linked wake, and starts no second model call. A later check-in in that window receives the stored cause and starts no model call.
18. **A18 — Minimal summary records.** Given the exec creates, publishes, or fails an activity-summary NOTE, when its durable rows are inspected, then no observation-request or observation-cancellation record exists.
19. **A19 — Honest idle note.** Given the covered transcript has no activity since T, when the exec publishes the NOTE, then it says `no activity since T` and states no health, progress, or cause conclusion.
20. **A20 — Summary privacy.** Given a principal may read worker notes but not the worker transcript, when it receives an activity-summary pointer, then it can read the NOTE and cannot read the transcript evidence body.
21. **A21 — Policy record.** Given an exec result commits under policy revision P, when policy later changes to Q, then the result still names P and no substrate row derives a replacement timing, escalation, model id, or effort.
22. **A22 — Baseline custody.** Given the Main pilot has not started, when the operator runs the specified cutoff-bound pipeline, then one artifact contains the exact pipeline, cutoff `1787842277183`, Tightbeam version, compact sorted JSON output, and output SHA-256; rerunning with the same durable rows produces the same bytes.
23. **A23 — Pilot gate.** Given Main pilot evidence is complete, when another worker or exec layer is proposed, then the proposal cites the frozen baseline artifact, before/after report, and product owner's recorded continue decision.

## Open Questions

**BLOCKING — delivery-destination transaction.** Which existing durable turn or queue row receives an exec-produced worker delivery, and which transaction commits that destination with the terminal wake or BUNDLE outcome? Implementation cannot start until one answer makes delivery and outcome indivisible; a split commit can lose a delivery or create a duplicate after restart.

**BLOCKING — exec-model credential lane.** Which existing credential kind and operator-owned configuration path may issue the direct provider handle for semantic exec calls? Implementation cannot start until one answer supplies a revocable handle without reading, copying, or reusing the worker harness credential.
