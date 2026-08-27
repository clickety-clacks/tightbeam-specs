# Substrate-native exec desks — v1

Status: DRAFT FOR INDEPENDENT REVIEW. Authority: `wi_795a354d-3f97-4805-b472-b637c7542d54`, Mike's 2026-08-26 brief and revisions. This specification supersedes the earlier desk-topology recommendation only for inbound delivery mediation.

## Goal

Make mediation of each inbound worker message a delivery-physics guarantee. A caller continues to address the worker through existing `wake` and `dispatch` seams. Tightbeam accepts the send only after it durably creates an inbound mediation record for that worker's desk. The desk then acts as the worker's agent under org-authored policy: it can spend less worker attention without deleting message information or deciding the worker's work.

The first pilot is one desk for Main. It measures the attention cost and outcome distribution before an org chooses more layers.

## Non-Goals

- V1 does not mediate worker outbound traffic. Outbound mediation is a successor.
- V1 does not add a desk address, ACP session, workdir, shell, repository, filesystem, or assignment to a desk. The narrow worker-transcript read required by `OBSERVE/DIGEST` is the sole exception to the desk's row-only material boundary.
- V1 does not answer a sender from rows. Mike struck `answer-from-rows`.
- V1 does not make `verify-prods` a separate action. A desk may annotate a delivered claim with cited rows.
- V1 does not absorb `wi_1100e078`. That independent notice-layer batcher remains related prior art and must compose with desk summarization.
- V1 does not implement, deploy, release, target a line, or alter 0.1.x behavior.

## Terms

- **Worker**: an ordinary addressable Tightbeam session. Existing `wake` and `dispatch` target this identity.
- **Desk**: a lightweight Tightbeam-native agent bound to one worker's inbound path. It reads and writes only durable rows. It has no desk binding of its own.
- **Inbound envelope**: the durable record made for one accepted worker-addressed inbound send before a desk acts.
- **Mediation record**: the append-only row that links an envelope, desk, policy revision, action, outcome, source rows, cause, and acting principals.
- **Delivery policy**: a globally selected default plus an org override. It supplies desk judgment context; it does not give the substrate opinions.
- **Class hint**: the sender's `wake --class` election. It is evidence to the desk and never selects the action by itself.
- **SUMMARIZE**: desk inference that semantically collapses an already mechanically batched set into one worker delivery. It never creates, schedules, or owns the batch. Deduplication and stale-expiry are SUMMARIZE cases with an explicit record, not separate verbs.
- **ANNOTATE**: desk inference that delivers a claim to the worker and may attach durable row facts. With no attached facts it is the explicit delivered-claim path; it still is not a separate pass-through verb.
- **ESCALATE**: desk inference that forwards context to an already-addressable authority worker. That target's normal desk mediation then applies.
- **Effective parent**: the worker resolved by the shared `effective_parent` helper defined by `wi_cd2bb06d`. It returns `operationalParent` when set; otherwise it returns the owner principal's Main. Desk code does not duplicate this fallback.
- **OBSERVE/DIGEST**: the fourth v1 desk capability. It reads only its worker's transcript window and creates or supersedes a standing activity-summary `NOTE` row. It is not a mediation action and cannot answer a question, decide work, or create a worker turn.
- **Activity-summary NOTE**: a knowledge row under knowledge-row law. It reports sourced observation without authority and carries the worker identity, performing desk identity, covered transcript window, observed-at time, source reference, interval, and explicit `supersedesNoteId` when it replaces a prior summary.
- **Event shell**: the deterministic, restart-safe desk execution layer. It reacts only to durable arrival, turn-completion, check-in-arrival, and deadline-wake events. It classifies configured facts, deduplicates, appends to the independent mechanical batch, and returns stored digest or NOTE pointers without invoking a model.
- **Execution wake**: a durable self-scheduled wake for a batch or observation deadline. Its idempotency key, due time, and target desk are rows, so restart does not require polling or recreate a prior effect.
- **Desk failure**: an unavailable, unauthenticated, misbound, terminal, or deadline-expired desk execution. It is never a direct-delivery bypass.

## Assumptions

1. The direct model-provider lane can invoke an elected desk model with a provider credential scoped to the org, not copied from the worker's harness home.
2. The existing wake/dispatch acceptance transaction can atomically persist an envelope or return a named refusal.
3. The live message database can be queried read-only for the seven-day classification analysis.
4. The reported seven-day baseline is accurate enough to seed the pilot: 27,275 inbound turns; agent-to-agent 54%, effort check-ins 19%, progress prods 11%, other process notices 8%, and user messages 4%. Data Package 2 is received on the parent assignment as `att_47a01848`.
5. `art_1e1d0b79` defines the visitor-attribution pattern required here: a desk action names both the worker it represents and the desk that performed it.
6. Mike intermediary ledger `art_a4f39376` is receiving-end evidence: of 201 Main adjudication signals, approximately all were effort check-ins; 150 were `continue`, 31 were `dismiss`, and none was a true decision. The ten highest-volume standing or coordination cards generated roughly half of the signals, and 31 signals targeted assignments already closed.

## Invariants

1. **Worker-addressed, exec-delivered.** The public send wire accepts a worker target only. No public verb, row reference, or retry accepts a desk as a recipient.
2. **Mandatory mediation.** For each accepted inbound send, the acceptance transaction creates exactly one envelope linked to the addressed worker's active desk binding. If no valid binding exists, the command refuses at send time with the named desk condition and creates no worker turn.
3. **Conservation.** Each envelope has exactly one terminal mediation outcome: `delivered`, `escalated`, or `expired_with_reason`. Each terminal outcome has a mediation record. No operation silently discards an envelope.
4. **Action floor.** A desk chooses only `SUMMARIZE`, `ANNOTATE`, or `ESCALATE`. `ANNOTATE` always results in delivery. `SUMMARIZE` either results in one delivery containing all member references or records each expired member's reason. `ESCALATE` names the authority worker and its resulting envelope.
5. **Two-name attribution.** A desk-authored row or delivery records `onBehalfOfWorker` and `performedByDesk`. It never claims the worker performed the desk's action.
6. **No desk authority over work.** A desk cannot file progress, completion, surrender, a product verdict, or an operator ruling; it cannot mutate work-item, assignment, decision-request, identity, credential, or target state.
7. **Policy belongs to the org.** The substrate routes envelopes, validates row shapes, and records outcomes. A desk model applies the elected policy. Global and org policy revisions are immutable, addressable, and included in each decision record.
8. **Bounded and recoverable.** A pending envelope has a recorded deadline. A crash, timeout, cancellation, or provider failure produces a durable named failure and a lawful retry or expiry outcome; it never produces a hidden hold.
9. **Topology is emergent.** Each worker has one inbound desk binding. An org may form further layers only by policy escalation to another worker; desks remain unaddressable and deskless, so recursion terminates.
10. **Privacy and least material.** Prompt assembly reads only the envelope, cited durable rows, current policy, and explicitly authorized worker metadata. `OBSERVE/DIGEST` may additionally read only its bound worker's transcript window to derive the activity-summary NOTE. Neither path reads a workdir, harness credential store, another worker transcript, or unrelated row content.
11. **Observation is not authority.** `OBSERVE/DIGEST` publishes a sourced NOTE, never an attest, verdict, lifecycle claim, answer, or control action. Each replacement names the prior note it supersedes. An empty observed window states `no activity since <window-start>`.
12. **Debounce is bounded observation.** A desk recomputes at most one activity-summary NOTE in each policy-configured `N`-minute interval, independent of the count of effort check-ins or other inbound traffic. A check-in receives the current NOTE id or link and no newly composed activity prose.
13. **One parent resolution.** Any desk action that needs the worker's operational parent calls the `wi_cd2bb06d` effective-parent helper. A null `operationalParent` resolves to the owner principal's Main through that helper; the desk does not store, infer, or implement another fallback.
14. **Event-driven execution.** A desk never polls. It reacts only to durable message-arrival, worker-turn-completion, check-in-arrival, and execution-wake events. With no such event, it performs no database scan, model call, or scheduled work.
15. **Two-layer execution.** The event shell performs only deterministic classification, deduplication, independent-batch append, annotation with configured row facts, and stored digest/NOTE-pointer replies. A model call may perform only semantic `SUMMARIZE` or `ESCALATE` judgment. Model cost therefore scales with semantic work, not inbound traffic volume.
16. **Receiving-end evidence.** An effort check-in aimed at a closed assignment or covered by a standing digest/NOTE is resolved in the deterministic event shell with cited row facts or a stored pointer. It cannot trigger a semantic-model call merely because it arrives. `art_a4f39376` is the initial receiving-end evidence for this floor.

## Architecture

### A. Binding and send transaction

`desk_bindings` records `workerSessionKey`, `deskId`, `state`, `policyRevision`, `boundAt`, `boundBy`, and a row version. The system provisions a binding for each active worker before that worker accepts inbound traffic. A desk has no `desk_bindings` row as worker.

For a worker-addressed `wake` or `dispatch`, the delivery transaction reads the active binding and, in the same transaction, either:

1. inserts an `inbound_envelope` with stable `envelopeId`, source verb/id, worker identity, sender identity, prompt reference, class hint, ordering key, deadline, and idempotency key; then returns accepted, or
2. refuses with `desk_unavailable`, `desk_misbound`, or another typed condition required by sibling `wi_c01e8f20`.

The transaction does not create a worker turn directly. An identical accepted command reuses its idempotency key and returns the original envelope; a conflicting reuse refuses. This is the selected closure because deleting mediation defeats the delivery-physics goal, and accepting an unmediated send makes loss silent.

### B. Event-driven two-layer execution and durable lifecycle

Message arrival creates the only ordinary execution event. The event shell claims its envelope by compare-and-swap and evaluates the configured structural policy without a model. It either delivers the source prompt (`ANNOTATE` with zero facts), attaches configured row facts (`ANNOTATE`), invokes the independent `wi_1100e078` mechanical-batch append, returns a stored digest/NOTE pointer, or queues a bounded semantic-model decision. `pass-through` and `batch` describe those deterministic paths; they are not additional desk inference verbs.

The desk service leases only an envelope that needs semantic-model work. Its lifecycle is `pending -> leased -> terminal`; a lease has `leaseId`, holder desk, and expiry. Only the lease winner may write a terminal record. Restart recovery expires a dead lease, records the cause, and makes the same envelope retryable without creating a second worker delivery. It never uses a periodic scan to find work.

The desk reads a fixed row API: envelope, source wake/dispatch, cited work and attests, policy revision, and prior mediation records. It writes only mediation records, desk execution records, and delivery attempts. The mediation API exposes exactly `summarize`, `annotate`, and `escalate`; no API exists for answer-from-rows or work-state mutation.

`SUMMARIZE` consumes an ordered, mechanically batched source set. It preserves each source envelope id, sender, source row, class hint, and original ordering key. It may replace repetitive content with a semantic summary, such as “three are-you-awake messages,” but the worker can query every member row. It does not select members, create a group, set a batch deadline, or schedule a delivery. The independent batcher owns the mechanical append and its deadline; it records the deadline as an execution wake, and its durable idempotency key prevents duplicate materialization after restart. `ANNOTATE` delivers the source prompt unchanged and attaches zero or more cited row facts; for example, it can put the contradicting attest beside a false no-filing prod. `ESCALATE` writes its context record and creates an ordinary worker-addressed envelope for the chosen authority worker; it never invokes a desk endpoint. When policy selects the operational-parent route, it obtains that worker only through the `wi_cd2bb06d` effective-parent helper; an explicit org policy destination remains a policy choice, not a second parent-resolution implementation.

An envelope becomes `expired_with_reason` only when its immutable deadline passes or policy identifies it as a stale duplicate. The terminal row names the policy revision, evidence rows, cause, and desk principal. Expiry preserves the source envelope and emits an observable worker-facing notice on the next eligible mediated delivery.

### C. OBSERVE/DIGEST standing summary

`OBSERVE/DIGEST` is a separately invoked desk capability, not a fourth delivery action. Worker-turn completion and check-in arrival are its only ordinary recomputation events. Each event either returns the standing NOTE pointer inside the debounce interval or schedules/uses the single durable observation execution wake at the interval boundary. It reads the bound worker's own transcript from the previous published window endpoint through the observation time, applies no interpretation beyond the configured activity-summary schema, and writes one activity-summary NOTE under knowledge-row law. The NOTE names `onBehalfOfWorker`, `performedByDesk`, transcript-window bounds, source reference, observation time, policy revision, and its superseded prior NOTE. If the configured presentation also renders a file, the NOTE stores that artifact reference; the NOTE remains the canonical query result.

The configured interval `N` is an org-policy value. The desk records the next eligible observation time and execution-wake id when it publishes a NOTE. Before that time, it returns the standing NOTE id without reading the transcript or composing new prose, regardless of check-in volume. If the transcript window has no activity, the NOTE says `no activity since <window-start>`; it cannot substitute reassuring language, infer a cause, or claim that the worker is healthy. A gateway or desk restart resumes from the durable wake and NOTE rows; it does not poll transcript state.

Effort check-ins receive only the standing NOTE pointer. The target patrol state reads that NOTE directly and sends no check-in messages. This produces zero patrol messages, zero worker turns, and a summary no older than the configured observation interval. A wedged worker is therefore observable at the first desk query: the summary must expose the lack of transcript activity for phantom-turn sequences 69089–69110 and the turn-73066 hang specimen instead of letting repeated prods consume worker attention.

### D. Policy and data loop

Policy has a global default and optional org override. A policy revision defines model/effort election, allowed source-row scopes, action prompts, deadline values, ordering rules, escalation destinations, and measurement cohort. A worker can publish standing instructions within that revision's schema; those instructions constrain its own desk, not other workers.

The initial taxonomy is data-derived. A reproducible read-only query over the real message database must record its query text/version, UTC window, classification rules, denominators, exclusions, and result rows. Mike's seven-day seed corpus is 27,275 inbound turns: agent-to-agent 54%, effort check-ins 19%, progress prods 11%, other process notices 8%, and user messages 4%. It found same-class recipient floods above ten per day in 80% of agent messages and 93% of effort check-ins: 261 agent-message and 102 check-in session-day floods, led by product owners, orchestrators, and watchdogs. The pilot targets those flood classes first.

Data Package 2 (`att_47a01848`) requires outcome-based taxonomy, not volume alone. The same analysis measures the worker's revealed material response as an attest inside the receiving turn window, then response-by-message and response-by-wake to correct the known undercount. Its initial reported outcome floors are: new assignments 74% of 283 turns, other process notices 61% of 4,588, agent messages 44% of 13,336, user messages 42% of 976, effort check-ins 28% of 4,881, and slate-clear notices 0.2% of 417. The report must state that attest-in-window omits valid later and non-attest responses; it therefore understates materiality, especially for agent messages. These figures are design evidence, not substrate thresholds.

The desk's own mediation rows feed a rerunnable read-only analysis. A policy revision may change only after an accountable org actor records the evidence and the new revision. The policy may use near-zero-material classes as candidates for semantic `SUMMARIZE` after independent mechanical batching, high-material classes for immediate `ANNOTATE` delivery with zero or more facts, and boundary classes for `ANNOTATE` after their independent batch is available. It never makes a volume threshold a substrate outcome rule or gives the desk ownership of a batch.

Receiving-end analysis complements the inbound corpus query. It records the receiving worker, action or disposition, assignment state at arrival, source class, standing-card identity, and whether a model was called. The first evidence is `art_a4f39376`: 201 Main adjudication signals were approximately all effort check-ins; 150 resolved `continue`, 31 `dismiss`, no true decision appeared, the top ten standing or coordination cards produced about half of the volume, and 31 signals addressed closed assignments. The analysis uses these as a reproducible cohort, not a hardcoded table: the deterministic shell targets closed-assignment and standing-card traffic for cited row/pointer handling, while a model call remains justified only by unresolved semantic summary or escalation work.

### E. Direct model-provider lane

Desk inference uses a direct model-provider request, not ACP and not the worker harness. Credential references are capability handles owned by the credential subsystem; prompts and logs never contain secret values. Prompt assembly includes the fixed desk contract, current policy, envelope, permitted citations, and an output schema that can express only semantic `SUMMARIZE` or `ESCALATE`. Deterministic `ANNOTATE`, pass-through, deduplication, batch append, and pointer replies never invoke that model. Provider requests carry `deskId`, `envelopeId`, policy revision, deadline, cancellation token, and idempotency key.

Lachesis records input tokens, output tokens, provider/model, attempt id, elapsed duration, and terminal result against the desk execution. It records an unavailable quota, provider rejection, malformed response, deadline expiry, cancellation, and transport failure as distinct durable causes. The retry state machine has an absolute envelope deadline and an explicit attempt cap from policy; a retry cannot outlive either. Cancellation first records the terminal cancellation race winner, then requests provider cancellation. This closes the turn-73066 hang lesson: a stuck call is observable, bounded, and cannot leave a lease without a terminal or recoverable state.

### F. Ordering, batching, and compatibility

For one worker, a mechanically batched source set retains its smallest member ordering key. A later ready set cannot be delivered ahead of an earlier ready set. A not-ready earlier set may not block an urgent ready set past that urgent set's deadline; the policy must record the ordering exception and its cause. `wi_1100e078` is related prior art only: its independent notice-layer batcher may mechanically combine notice turns before desk ingress, and desk summarization then operates over the resulting source references. Neither system creates, schedules, alters, or owns the other's batching rows; either can ship or roll back without changing the other's acceptance contract.

Legacy inbound rows remain readable. Migration creates a desk binding before enabling mandatory mediation for a worker and backfills no historical envelope. A rollout flag selects an explicit worker cohort. Rollback stops new cohort admission only after it records each pending envelope's chosen recovery path; it never reroutes new sends directly to workers. Compatibility clients keep using worker targets and receive the same accepted/refused response shape plus optional envelope metadata.

### G. Wire, observability, and pilot

The send response adds `envelopeId` when accepted. Reads expose envelope state, mediation records, terminal cause, policy revision, two-name attribution, and linked source rows to authorized readers. The public wire rejects a `deskId` target with `desk_unaddressable`. Metrics and read-only reports expose accepted/refused sends, action/outcome counts, deadlines, retries, duplicate collapses, direct-model cost, and worker-turn savings; no metric is used to decide a message outcome.

The Main-first pilot records a before and after window. It cites the observed Main question queued behind 39 check-ins, the Shrdlu no-desks e2e result, and phantom/hang wedges as motivating specimens. Success is evidence, not an automatic topology decision: the report compares worker turns, delay, loss/refusal causes, policy drift, and Lachesis cost. An org actor decides whether to extend desks.

## Acceptance

1. Given an active worker binding, when `wake --role worker` is accepted, then one envelope exists with that worker target, its source wake id, and an active desk id; no direct worker turn exists before desk delivery.
2. Given no active binding, when a caller sends to that worker, then the command returns `desk_unavailable`, names the worker and cause, and writes no worker turn.
3. Given a caller supplies a desk id to `wake` or `dispatch`, when validation runs, then it refuses `desk_unaddressable` before any envelope or turn is written.
4. Given the same accepted command is retried with its idempotency key, when the second request arrives, then it returns the original envelope id and creates no second envelope or delivery.
5. Given an idempotency key is reused with different target or prompt bytes, when validation runs, then it refuses with a typed conflict and preserves the original envelope unchanged.
6. Given `wi_1100e078` has mechanically batched three source envelopes, when a desk emits `SUMMARIZE`, then the worker receives one semantic delivery with all three envelope ids and source rows, and the mediation record names `SUMMARIZE` without creating or scheduling a batch.
7. Given an `ANNOTATE` action has a contradicting attest, when delivery occurs, then the worker receives the original prompt plus the cited attest reference and the row records both principals.
8. Given an `ESCALATE` action names an authority worker, when the desk commits it, then a new envelope targets that worker and its own desk, with no desk target on the wire.
9. Given a desk attempts to answer a sender from rows, when the desk API validates output, then it refuses the unsupported action and records the schema violation without suppressing the envelope.
10. Given a desk attempts a work lifecycle or decision mutation, when authorization runs, then it refuses before mutation and names the desk capability rule.
11. Given a provider returns malformed action JSON, when the attempt ends, then one durable failure records the raw response reference, cause `model_response_invalid`, and the envelope remains recoverable until its deadline.
12. Given a provider request exceeds the envelope deadline, when the deadline wins the race, then its execution records `deadline_expired`, later provider completion writes no delivery, and the envelope has one terminal outcome.
13. Given cancellation races provider success, when both execute, then exactly one terminal execution row wins and no second worker delivery appears.
14. Given a desk process dies with a lease, when lease recovery runs, then it records the lost lease cause and reoffers the same envelope once without changing its idempotency identity.
15. Given a repeated stale envelope is expired through `SUMMARIZE`, when expiry is recorded, then the reason, policy revision, and source envelope are queryable and the next mediated worker delivery includes the notice.
16. Given a sender sets `wake --class blocker`, when the desk selects an action, then the record preserves `blocker` as a hint and identifies the policy evidence for its independently selected action.
17. Given two policy revisions, when a desk action occurs, then its mediation record references exactly the revision read for that action; later policy changes do not rewrite it.
18. Given a desk prompt is assembled, when its inputs are inspected, then they contain only authorized rows and no worker transcript path, workdir path, harness credential material, or unrelated message body.
19. Given a provider call finishes, when Lachesis reads the execution, then it reports the model, attempt, input/output token counts, duration, and terminal cause.
20. Given an earlier ready group and a later ready group for one worker, when delivery runs, then the earlier group's smallest ordering key is delivered first unless a recorded deadline exception applies.
21. Given a migration cohort is enabled, when its first worker begins receiving traffic, then the active binding predates the first accepted envelope; historical messages have not been backfilled as envelopes.
22. Given a rollback begins with pending envelopes, when new sends arrive, then each is still mediated or visibly refused; no new direct-to-worker path appears.
23. Given the Main-first pilot closes, when the report is generated, then it contains reproducible before/after query identifiers, query text/version, UTC window, classification rules, denominators, exclusions, response channels, desk action/outcome counts, latency, named failures, Lachesis cost, and the attest-in-window limitation.
24. Given `wi_1100e078` independently emits one notice-layer batch with its member references, when it reaches a worker desk, then the desk records it as one mechanically batched source set while preserving every member reference; disabling either feature leaves the other feature's send, ordering, and terminal-outcome contract unchanged.
25. Given the seven-day classification query runs against the live message database, when it reports the target cohort, then its output separately names the agent-message and effort-check-in flood denominators, 261 and 102 session-day floods, the greater-than-ten-per-day rule, and its top sender roles.
26. Given the outcome analysis runs for a policy revision, when it classifies a traffic class, then it includes attest, message, and wake response channels; it labels the attest-in-window rate as a floor; and it records `att_47a01848` as the seed-evidence source for the initial rate table.
27. Given a desk has no activity-summary NOTE for its worker or its configured `N`-minute interval has elapsed, when `OBSERVE/DIGEST` runs, then it reads only that worker's transcript window and creates one dual-attributed knowledge-row NOTE with source, window, observation time, and policy revision.
28. Given a standing activity-summary NOTE is less than `N` minutes old, when one or more effort check-ins arrive, then the desk reads no transcript, emits no new summary prose, and supplies only the existing NOTE id or link.
29. Given an activity-summary NOTE supersedes a prior NOTE, when the new NOTE is written, then it names the prior NOTE id; authorized patrol reads the new NOTE directly and sends no message or worker turn.
30. Given a worker transcript window contains no activity since `T`, when `OBSERVE/DIGEST` publishes its NOTE, then the NOTE says `no activity since T` and does not infer health, progress, or a cause.
31. Given phantom-turn sequences 69089–69110 or the turn-73066 hang leave no new worker transcript activity, when the first desk observation is requested after the eligible interval, then the standing NOTE exposes that inactivity and the worker receives no patrol prod.
32. Given a worker has a non-null `operationalParent`, when an `ESCALATE` action uses the operational-parent route, then it calls the shared effective-parent helper and addresses that returned worker.
33. Given a worker has a null `operationalParent`, when an `ESCALATE` action uses the operational-parent route, then the shared effective-parent helper returns the owner principal's Main, and the desk records that returned worker without storing or deriving a local fallback.
34. Given no message-arrival, worker-turn-completion, check-in-arrival, or due execution-wake event, when the desk is idle, then it performs zero polling queries, zero model calls, and zero scheduled executions.
35. Given a message-arrival event matches a deterministic configured path, when the event shell handles it, then it performs classification, deduplication, independent-batch append, configured annotation, or stored-pointer reply without a model call.
36. Given a mechanically batched set needs semantic collapse or escalation judgment, when the event shell reaches that boundary, then it creates one bounded model execution; no other inbound traffic creates a model call solely because it arrived.
37. Given a batch or debounce deadline is created, when the gateway or desk restarts before it fires, then the durable execution wake fires at most once by its idempotency key and does not require a polling scan.
38. Given a check-in arrives inside the `N`-minute observation interval, when the event shell handles it, then it returns the standing NOTE pointer and performs no transcript read or model call.
39. Given an effort check-in targets an assignment already closed at arrival, when the event shell handles it, then it returns cited assignment-state facts or a stored pointer, records `art_a4f39376`-compatible receiving evidence, and creates no semantic-model call or worker turn.
40. Given a receiving-end evidence query runs, when it reports the cohort, then it includes source class, worker, action/disposition, assignment state at arrival, standing-card identity, model-call count, and the `art_a4f39376` baseline figures of 201 signals, 150 continue, 31 dismiss, zero true decisions, top-ten half-volume, and 31 closed-assignment targets.

## Open Questions

- **BLOCKING — delivery destination seam.** Which existing durable turn/queue row receives a desk-produced worker delivery, and which transaction owns its atomic commit with a mediation terminal record? The spec requires one answer before implementation because a split commit could violate conservation.
- **BLOCKING — credential authority.** Which existing credential kind and operator-owned configuration path may issue direct model-provider handles for desks? The spec prohibits worker-harness credential reuse, but the concrete capability seam must be selected before implementation.
- **NON-BLOCKING — pilot policy.** The first Main policy's exact deadlines, model election, and allowed summarization prompt are org choices. The global-policy mechanism is buildable before this policy is finalized.
- **NON-BLOCKING — escalation topology.** The first authority workers for `ESCALATE` are org choices. Escalation's worker-addressed mechanics are buildable independently.
- **NON-BLOCKING — parent-helper delivery.** `wi_cd2bb06d` owns the `operationalParent` nullability and effective-parent helper. This spec consumes that helper for parent-route escalation and does not duplicate its schema, migration, or implementation.

## Rationale for adding the mechanism

Deleting mediation loses the required delivery guarantee; accepting queue floods as a named failure preserves the present 39-check-in harm. The added mechanism wins because only a durable, worker-addressed mediation seam can reduce interruption while preserving rows and loud failure.
