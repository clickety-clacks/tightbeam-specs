# 0.2 adapter-recovery resume invariant

Status: READY FOR INDEPENDENT RE-REVIEW  
Work item: `wi_cbb56e71-5c93-41c0-bfb9-e5db2dc87c91`  
Producer assignment: `asg_aaaa71d9-273e-454f-bd32-cdc77a9ab7cd`  
Supersedes artifacts: `art_1dca486c`, SHA-256
`1e5193b68b9054ae507650a60b7f056365bd5e1d40c6aed22c1da726fe8d2d2c`,
and `art_fd6e93bc`, SHA-256
`17409b8046d4e478b30370ac5ac1d29a84b98beaadd60a48e706f0bc55e250bf`
and `art_34024d2f`, SHA-256
`feea465338780b1d04fb4eba5b2c632eff58dc3345fd1ec433cbd9ab0d46f0ed`
and `art_909414fe`, SHA-256
`41553723a450ce17517fbd5c5c9bfc6f1ab5681ae8706b3254b34e2814fcf489`
Revision basis: changes-requested `att_10a6b91d` / `art_4d9afce2`,
`att_17dc4980` / `art_31e37e3c`, `att_00019ad5` / `art_84ae0369`, and
`att_51556476` / `art_5ceea0d8`

## Canonical home

This file is canonical only at
`clickety-clacks/tightbeam-specs/adapter-recovery-resume-invariant.md`.
Scratch copies and Tightbeam artifact rows are pointers, not custody. Every reviewed
revision must name the repository commit, file path, and content SHA-256.

## Spirit

An adapter outage may interrupt a turn. It must not cancel the responsibility that the
turn served.

After Tightbeam proves that the shared harness can serve work again, every still-open
assignment affected by that outage must again have a durable path to a future turn. No
assignment may become silent because a failed turn, a spent prod ladder, or an escalation
transfer removed its last restart path.

Recovery must not replay the interrupted turn. That turn is terminal, and its external
side effects are unknown. Tightbeam resumes responsibility by arming ordinary supervision.
The agent then re-reads the assignment and its facts, inspects the material world for
prior effects, and decides the next safe action.

Recovery must survive a gateway crash before or after adapter-death observation. It must
survive adapter flaps and concurrent deaths. It must remain visible in durable rows. It
must not create a turn storm across every session on a shared adapter.

## Outcome

For each recovered outage window, every affected assignment that remains open has one of
these states before recovery commits:

1. It already has a durable continuation, such as a queued or running attributed turn,
   a pending attributed wake, or an open attributed decision.
2. Tightbeam arms ordinary supervision for it now.
3. It left the affected population because it closed, its holder retired, or its holder
   moved to another adapter.

There is no fourth state.

## Assumptions and pinned dependencies

1. Adapter generations, instance readiness, planned-close intent, gateway boot epochs,
   session adapter bindings, assignment rows, and turn terminals are durable database
   facts. Recovery never infers these facts from logs or prose.
2. A ready adapter generation belongs to exactly one adapter key. The implementation
   baseline represents that key as `{harness, "shared", host}`. Harness membership comes
   from the canonical harness registry; this spec does not fix a harness count.
3. Gateway shutdown records planned adapter closes before process teardown. A prior ready
   generation with neither a planned close nor a terminal observation across an unclean
   boot boundary is an unobserved loss candidate.
4. This design depends on the supervision-population correction in
   `wi_a57dee58-7dc6-43e4-b36d-a45959e64ad6`: every open assignment held by a live session
   is watched, while a pacing row controls only when supervision acts. That work item is
   still open at this revision. Implementation and integration of this invariant must stop
   until the dependency lands in a canonical spec and commit.
5. Quota, credential, and provider-reachability classification is outside this spec.
   Another canonical mechanism may append the typed occurrence defined here, but no caller
   may open an outage window from free text, a threshold guess, or an unpinned evidence rule.

## Definitions

- **Adapter key** is the registry-derived identity for one shared adapter service on one
  host. The current storage shape is `{harness, "shared", host}`.
- **Outage window** is the single durable open harness-health incident for an adapter key.
  A unique database constraint permits at most one open window per key. Later real deaths
  join that window until service proof closes it. A later death after closure opens a new
  window.
- **Occurrence** is one typed cause row inside an outage window. It records the dead
  instance, failed generation, observation kind, cause principal, and boot epoch. An
  occurrence is evidence, not an independently recoverable incident.
- **Window revision** is a monotonic integer incremented whenever an occurrence joins the
  open window. A service proof may close only the exact revision it observed.
- **Service proof** is one successful normal harness prompt on a replacement generation.
  Its durable success commits with the outage-window recovery transition. Adapter process
  spawn and ACP initialization alone are not service proof.
- **Affected assignment** is an open assignment whose active holder used the adapter key
  during the window. Incident membership records the historical set. Recovery also derives
  the current set once inside its transaction.
- **Durable continuation** is a row that the substrate will act on without another human
  or agent first remembering the work. A terminal turn, chat marker, log row, or unrelated
  activity by the same session does not qualify.
- **Arm supervision now** means the assignment is in supervision's derived population and
  its pacing row is due immediately. The periodic sweep is the liveness backstop. A nudge
  is only a latency hint.
- **Probe lease** is the persisted, adapter-key-scoped right to run one readiness prompt for
  the open outage window. At most one lease is active for the key, even when the window
  revision changes. The lease carries the revision it claimed as fenced payload, plus its
  adapter instance and generation, owner, monotonic lease epoch, attempt number, prompt
  deadline, settlement deadline, state, and next due time. A deadline never unlocks a
  successor while the prior external call may still be live.
- **Database time** is the timestamp captured by the database owner inside the transaction
  that claims, requests cancellation, settles, or completes a probe. Callers cannot supply
  it. Persisted time comparisons use this authority; host wall clocks do not decide
  eligibility.
- **Adapter-control intent** is a row in the durable adapter-control outbox. It records
  adapter key, full claim token, action (`cancel_probe` or `terminate_instance`), claimed
  instance and generation, state, cause, principal, creation time, and settlement time. A
  unique `{claimToken, action}` constraint makes delivery and restart replay idempotent. It
  never contains prompt text or provider credentials. A cancellation intent may become
  obsolete when its exact call first reaches a durable terminal. A termination intent is
  irrevocable after commit.
- **Acknowledged prompt terminal** is durable adapter evidence that the exact call no longer
  exists in its in-flight set and cannot later deliver a success. Delivery of a cancellation
  request, a local timeout, or loss of the caller alone does not qualify.

## Required design

### 0. One authoritative outage window absorbs concurrent deaths

A matching `:DOWN` for an adapter instance that reached ready state appends one occurrence
before the coordinator schedules its replacement. The transaction upserts the one open
window for the adapter key, increments its revision, records the dead instance and failed
generation, attaches the current affected assignments, and creates or refreshes the
window-scoped harness-suppression effect for every attached assignment. The commit that
first opens the window or later joins an occurrence establishes suppression before any
replacement scheduling or supervision action may proceed. A fast recovery cannot overtake
this write.

An absorbed `:DOWN` for a previously ready instance appends another occurrence to the same
open window. It does not open a second incident. A stale death for an instance that never
became ready is record-only. A planned close does not append an occurrence.

Two real ready-instance deaths that race serialize through the database owner. Both cause
rows persist exactly once. They either join the same still-open window or, if recovery
committed first, the later death opens the next window. The unique-open constraint and an
occurrence identity key make retries idempotent.

A probe or normal turn captures the window id and revision before prompting. Recovery may
commit only if that same window is still open, its revision is unchanged, and the successful
generation is newer than every failed generation in the window. A death that joins during
the prompt increments the revision and fences the stale proof. The next leased probe must
prove the newer revision.

### 1. Boot reconciliation recovers a death lost before incident creation

Before adapter replacement or recovery probing begins on gateway boot, one deterministic
reconciliation transaction examines the prior boot epoch.

For each adapter key, reconciliation appends a `boot_reconciled_loss` occurrence when all
of these durable predicates hold:

1. The prior generation reached ready state.
2. No planned-close or terminal-death row settled that generation.
3. The prior gateway boot epoch ended without a clean-shutdown row.
4. At least one durable responsibility fact points at that generation: an active session
   binding, an open assignment held by such a session, a nonterminal turn, or a failed turn
   attributed to adapter transport loss.

The reconciliation transaction uses the same open-window upsert, revision increment,
occurrence identity, and membership attachment as `:DOWN`. It also marks surviving
nonterminal turns from the lost generation failed with unknown external effects before any
new prompt can run. In that same transaction it creates or refreshes the window-scoped
harness-suppression effect for every attached assignment. Replacement scheduling and
supervision remain fenced until the transaction commits. Replaying boot reconciliation
writes nothing after the occurrence key exists.

Initial boot has no prior ready generation and opens no window. A clean gateway shutdown
has planned-close rows and opens no window. A never-ready generation opens no window. These
negative rules prevent boot from waking every assignment.

### 2. Recovery authority is a revision-bound service proof

The current adapter instance must first reach the existing instance-scoped ready state. A
stale ready signal, planned recycle, process spawn, or successful ACP `initialize` call is
not a recovery edge.

The harness-health patrol may claim at most one in-flight probe lease for an adapter key
while its outage window is open. Claim is a compare-and-set on the one persisted key-scoped
lease row. The row records `claimedWindowId`, `claimedRevision`, `claimedInstanceId`,
`claimedGeneration`, `leaseOwner`, monotonic `leaseEpoch`, `attempt`, `promptDeadline`,
`settlementDeadline`, `leaseState`, and `nextProbeAt`. The claim token is the exact tuple
`{adapterKey, claimedWindowId, claimedRevision, leaseEpoch, attempt, leaseOwner}`. A later
occurrence may increment the window revision, but it does not release or supersede the
in-flight right. The old completion will be fenced by its claimed revision, and no probe
for the new revision may begin until the active lease reaches a durable terminal state. A
unique database constraint on the adapter key makes a second active lease impossible across
revisions or gateway processes.

An idle row starts with `leaseEpoch = 0` and `attempt = 0`. Each claim atomically increments
both values and stores them, so the first prompt is epoch 1, attempt 1. Attempt resets only
between outage windows; lease epoch never resets. Claim captures database time as
`claimedAt` and sets `promptDeadline = claimedAt + 115_000ms` and
`settlementDeadline = claimedAt + 120_000ms`. The adapter call receives the exact prompt
deadline. A patrol success may commit as proof only when database time is at or before that
deadline and the claim token, instance, generation, window, and revision still match.

If no terminal result has committed when database time passes `promptDeadline`, the database
owner changes `leaseState` from `running` to `cancel_requested` and emits one idempotent
cancellation intent for the exact adapter call. The typed durable intent is keyed by the
claim token, records cause and principal, commits with the state transition, and is delivered
idempotently after commit. If the call has not reached a durable terminal by
`settlementDeadline`, the database owner changes the state to `terminate_requested` and
commits one similarly keyed adapter-instance termination intent. That transaction also
marks the claimed instance `terminating` and removes it from ready routing before the intent
can be delivered. Termination is then irrevocable: a later prompt terminal records its
result but cannot settle the lease, withdraw the intent, restore ready routing, or permit a
claim. Only the durable terminal of that exact instance settles a termination-requested
lease. The adapter supervisor consumes the intent until that terminal exists.

Before a termination intent commits, an acknowledged prompt terminal may settle the lease
and atomically mark a pending cancellation intent `obsolete`. Prompt-terminal settlement,
normal-proof recovery, and termination creation all lock the adapter-key lease first and then
the claimed instance and control-intent rows in one canonical order before they recheck the
full active token. If prompt-terminal settlement won first, the termination transaction
writes no termination intent. If normal-proof recovery won first while the patrol call
remained live, the token stays cancellation-requested and termination may still commit at its
deadline. If termination won first, its routing fence makes the normal proof ineligible. A
timeout, disconnect, or other transport observation that does not prove the exact
local call terminal never settles the lease. It may only change `running` to
`cancel_requested` and commit the token-keyed cancellation intent. Time passage alone never
makes a successor claimable. A late completion with an inactive token records
`stale_probe_completion` and cannot record proof, close a window, alter pacing, or arm
supervision.

Every non-proof terminal settlement selects exactly one branch from current database state:

1. If the claimed window is still the unique current open window, retain the claimed
   attempt and write `nextProbeAt = settledAt + delay`, where
   `delay = min(60_000ms, 1_000ms * 2^(min(attempt - 1, 6)))`.
2. If the claimed window is closed and no current window exists for the key, archive the
   attempt terminal and reset the key row to idle with `attempt = 0`, no due time, and the
   monotonic lease epoch retained.
3. If a different current open window exists, archive the old attempt terminal and bind the
   key row to that window with `attempt = 0` and `nextProbeAt = settledAt`.

These branches are mutually exclusive. The generic failure backoff applies only to branch
1. No claim may succeed before its branch's due-time and terminal-settlement fences permit
it; the next successful claim increments attempt and lease epoch.

A gateway crash leaves the running, cancellation-requested, or termination-requested lease
and its intent durable. Boot reconciliation redelivers the same keyed intent or proves the
claimed instance terminal; it never clears the lease from time alone. An unknown external
prompt result is not proof. The next claimant runs a new prompt only after durable
settlement and the due-time fence. Tightbeam never replays the old prompt.

A successful normal user or agent turn can supply proof without owning the patrol lease.
It must still bind the same open window revision, satisfy the generation fence, and prove
that its adapter instance remains durably ready and routable with no committed termination
intent. If it wins recovery while a patrol probe is active, the recovery transaction changes
that lease to `cancel_requested` and emits its idempotent cancellation intent. If the exact
patrol call remains live through its settlement deadline, the lease may later advance
irrevocably to `terminate_requested`. If termination committed first, the normal proof is
fenced. A later exact-call or instance terminal settles the token through the applicable
branch above and cannot recover or fan out again.

For a normal turn, the ledger's `delivered` terminal and recovery transition commit in one
database transaction. For a patrol probe, its success row and recovery transition commit in
one transaction. If the gateway dies after the external prompt succeeds but before commit,
no proof exists. The window stays open, and a new lease becomes claimable only after the
persisted lease boundary permits it.

### 3. Incident membership is the recovery set

When an outage window opens or gains an occurrence, it attaches every open assignment held
by an active session on the adapter key. While it remains open, the same derived query
attaches newly opened or newly assigned work on that key. Membership attachment and creation
or refresh of that window's harness-suppression effect commit together, before supervision
may act on the newly attached assignment.

Recorded membership answers only the historical question, "was this assignment on the
affected adapter during this window?" It never replaces the assignments table as the
current work population.

At recovery, Tightbeam takes the union of historical membership and one current derived
membership query inside the transaction. It then re-checks each assignment and holder:

- Closed or revoked assignments need no turn.
- Assignments whose holders retired follow the retirement contract.
- Assignments whose holders moved to another adapter leave this window's active set.
- Still-open assignments on the recovered key remain in scope.

Changing an open assignment's active holder binding from one adapter key to another is one
database-owner transaction. It locks the assignment and both adapter keys in deterministic
key order. The transaction removes only the source window's suppression from the assignment
and retains that window's historical membership with `movedAt` and destination key.

If the destination key has an open window, the same transaction attaches the assignment to
that window and creates or refreshes its suppression before the new binding becomes visible.
If the destination has a durable ready generation and no open window, the transaction leaves
no adapter suppression. It preserves any existing durable continuation; otherwise, unless
a non-adapter block applies, it arms ordinary supervision due now. If the destination is
neither durably ready nor represented by an open outage window, the move refuses with
`adapter_binding_unavailable` and changes neither binding nor suppression. A same-key rebind
is idempotent. Source recovery, destination death, close, revoke, and retirement serialize
through these locks, so no ordering leaves old suppression, misses destination membership,
or queues a turn through an open outage.

### 4. One atomic window recovery transition

The transaction that records service proof and changes the window from open to recovered
must also classify every in-scope assignment. It compares the window id, state, revision,
and proof generation in one compare-and-set.

For each still-open assignment on the recovered key, the transaction must:

1. Preserve an existing durable continuation without adding another one.
2. Otherwise upsert supervision pacing as armed and due now.
3. Clear only this window's harness-suppression effect.
4. Record the recovered generation and successful proof turn.

The transaction appends one `adapter_recovery_armed` lifecycle row. Its detail carries the
window id and revision, adapter key, occurrence count, failed-generation range, recovered
generation, proof turn id, `proofSource` (`patrol_probe` or `normal_turn`), `recoveryActor`,
and counts for armed, already-continuing, closed, retired, and moved assignments. The
authenticated database principal that commits the transition is `recoveryActor`; it is not
an outage cause principal. Each occurrence retains its own typed cause principal. Membership
rows carry the exact assignment list and the authenticated transition actor where an actor
is required. No aggregate lifecycle `cause principal` exists.

Only the compare-and-set winner arms assignments and clears suppression. A repeated handler
returns `already_recovered` and writes no recovery action. A patrol terminal may still
settle its exact outstanding lease token. All occurrences in the closed window settle
together; no occurrence owns a second close, lifecycle row, or supervision fan-out.

The same transaction reconciles the key lease. A patrol proof consumes its exact active token.
When no external patrol call is active, recovery resets `claimedWindowId`, claimed revision,
instance, generation, owner, deadlines, state, `nextProbeAt`, and `attempt` to the idle
cross-window values while retaining monotonic `leaseEpoch`. When a normal turn wins over a
live patrol call, recovery leaves that token in `cancel_requested`; a still-live call may
later advance to `terminate_requested` under the same deadlines and lock order. Its terminal
settlement must use branch 2 or 3, never the branch-1 backoff. Recovery does not wait for
cancellation or termination before it arms
assignments, but no later outage probe may claim until the old external call or terminating
instance is durably terminal.

After commit, Tightbeam nudges supervision once per affected holder. Supervision may queue
at most one recovery-driven turn per holder at a time. Other due assignments for that holder
stay due until the queued or running turn becomes terminal. If the gateway dies before a
nudge, the due pacing rows remain and the periodic sweep resumes them after boot.

### 5. Supervision resumes the assignment, not the old turn

The ordinary supervision prompt is the recovery turn. It points at the same assignment and
tells the holder to re-read the assignment, its attests, and its work item.

If the window interrupted a running turn, the prompt names that failed turn and states that
its external effects are unknown. It instructs the agent to inspect external state before
it repeats a push, deploy, send, migration, or other non-idempotent action.

The old turn remains terminal. Tightbeam does not change it back to queued or running.
Tightbeam does not resend its prompt. ACP `session/load` may restore model context when the
harness supports it, but it does not resume the interrupted prompt turn.

### 6. Failed recovery work remains eligible

The recovered adapter can fail again after the atomic transition and before an armed
assignment completes a turn. The new death opens the next outage window because the prior
window is closed.

The new-window transaction never inherits the closed window's attempt or backoff history.
If the key lease is idle, it binds the row to the new window with `attempt = 0`, no owner or
deadlines, and `nextProbeAt` equal to database time. If a prior-window cancellation is still
unsettled or its termination is irrevocable, the row retains its exact old token and blocks
claims. Its exact call or instance terminal then follows branch 3 and binds the row to the
unique current open window with the same fresh values. The monotonic lease epoch never
resets, so a late prior-window completion cannot match a future claim.

Such a failed turn must not consume a heard-prod rung. It must not remove the assignment
from supervision. The next revision-bound service proof performs the same transition for
the new window.

A successful recovery prompt proves only that the holder can turn again. It does not prove
that the assignment completed. Ordinary assignment facts decide completion.

### 7. Other waits keep their own exits

Recovery does not override a valid wait for an operator decision, a condition wake, a
review verdict, or another named dependency. Those rows already provide a durable
continuation, so recovery classifies the assignment as already continuing.

Recovery does not clear a non-adapter `work-blocked` fact. Such a block must carry its own
owner and exit. An open assignment with neither an exit row nor supervision remains invalid
under the global live-work invariant; adapter recovery must not hide it.

### 8. Supervision population is derived from open assignments

This design requires the canonical outcome of
`wi_a57dee58-7dc6-43e4-b36d-a45959e64ad6` before implementation.

Every open assignment held by a live session is in the watched population. A pacing row
controls when supervision acts; it never controls whether supervision can see the
assignment. Missing pacing means default pacing, not invisibility. `terminus` can stop one
escalation sequence, but it cannot remove an open assignment from the watched population.

No adapter-recovery implementation may create or retain a second watched population as a
fallback. If the dependency does not land, this design remains blocked.

## Restart, replay, and race rules

- The unique-open-window constraint is authoritative. An occurrence retry is idempotent by
  its typed occurrence identity.
- A stale `:DOWN`, stale ready signal, or proof from an older window revision cannot open or
  close the current revision.
- Recovery serializes against assignment close, revoke, holder move, and retirement. The
  move transaction clears source suppression and reconciles destination suppression or
  supervision atomically; the later transaction observes the earlier result.
- Boot reconciliation runs before replacement scheduling and before any recovery probe.
  It is replay-safe across repeated crashes.
- A gateway restart with an open window preserves probe attempt, lease, backoff, membership,
  and suppression. It does not infer proof from logs or an external prompt response.
- One adapter key has at most one active probe lease. A revision increment fences the
  claimed proof but cannot release the lease; a new-revision or new-window probe waits for
  durable terminal settlement of the old external call.
- Probe eligibility, expiry, and backoff use database time only. Restarts and host-clock
  changes cannot shorten a persisted deadline or due time. Deadline passage requests
  cancellation or instance termination; it never grants a second lease.
- Every patrol completion compares the full claim token. Expired, cancelled, settled, or
  cross-window tokens can record only a stale-completion terminal.
- Cancellation and instance-termination intents are durable, token-keyed, idempotent, and
  replayed after restart until the exact call or instance reaches a durable terminal.
- A committed termination intent is irrevocable and its instance is not routable. Prompt
  terminal settlement can prevent termination only by committing first under the same token
  lock. No successor can reuse an instance with a pending or delivered termination intent.
- An observation-only transport failure can request cancellation but cannot settle a lease.
- Non-proof settlement chooses exactly one current-window branch; only the still-open
  claimed-window branch retains attempt and applies backoff.
- A crash after recovery commit but before nudges loses only latency. Due pacing remains.
- A new assignment opened after recovery follows ordinary supervision and does not join the
  closed window.
- A death that races a successful prompt either increments the open revision first and
  fences the proof, or commits after recovery and opens the next window. No ordering loses
  the death or lets one proof close two windows.

## Operator-visible record

The incident, occurrence, proof, membership, lease-attempt terminal, adapter-control intent,
and `adapter_recovery_armed` lifecycle rows are the complete operator record. Occurrences
carry their typed cause and cause principal. Proof and lifecycle rows carry their proof
source and authenticated recovery actor instead of collapsing recovery activity into the
outage cause.

This design adds no chat marker. The prior `[adapter recovered]` stored marker is deleted:
it duplicated authoritative evidence and could be lost after recovery commit. A future
user-notification feature needs its own durable outbox, cause/principal fields, and delivery
acceptance; it is not part of this invariant.

## Non-goals

- Do not replay, clone, or reopen a failed turn.
- Do not add a manual `resume` command.
- Do not create a second retry daemon or assignment population.
- Do not spawn replacement agents or change model, harness, effort, or host.
- Do not clear operator decisions or non-adapter blocks.
- Do not make initial adapter boot wake every open assignment.
- Do not treat message delivery, process spawn, or adapter initialization as service proof.
- Do not close assignments because the holder can turn again.
- Do not define quota, credential, or provider-failure thresholds here.
- Do not add a post-commit chat marker.

## Acceptance and proof matrix

1. **Ready death during a prompt.** Kill a ready adapter during a real prompt. The matching
   death opens one window and occurrence before replacement. The old turn becomes failed
   with unknown effects. One revision-bound successful probe recovers the window and leaves
   the assignment armed and due.
2. **No replay.** The supervision turn points at the same assignment, requires durable-fact
   and external-state inspection, and never replays the old prompt.
3. **Population isolation.** Several sessions on one adapter all retain or receive durable
   continuation. A session on another adapter receives nothing.
4. **Existing exit.** An assignment with an attributed wake or open operator decision gets
   no duplicate supervision turn.
5. **Membership growth.** An assignment opened during the window joins the recovery set.
6. **Assignment race and move.** Close, revoke, move, and retire races produce no stale
   wake. A move to a healthy key atomically clears source suppression and leaves the open
   assignment continuing or due under ordinary supervision. A move to a key with an open
   window atomically clears source suppression, joins destination membership, and installs
   destination suppression before the binding is visible. A move to an unready key without
   an outage window refuses without changing the source binding or suppression.
7. **Concurrent deaths.** Two ready deaths before proof create two occurrence rows in one
   open window. The second increments revision. A proof for the first revision is fenced.
   The revision increment does not release the first probe lease, so no second probe is in
   flight. After that lease reaches a durable terminal settlement, one proof for the final
   revision closes once and writes one lifecycle row.
8. **Death versus close.** A death committed before recovery joins and fences proof. A death
   committed after recovery opens the next window. Neither ordering loses responsibility.
9. **Replay.** Repeating an occurrence, proof, or recovery handler writes no duplicate row
   or supervision action.
10. **Negative transitions.** Stale ready, never-ready boot, planned close, clean restart,
    and initial boot produce no outage recovery.
11. **Crash before `:DOWN`.** Crash the gateway after a ready adapter disappears but before
    incident creation. Boot reconciliation opens one window from prior generation, unclean
    boot, and durable responsibility facts before replacement or probe.
12. **Reconciliation replay.** Crash again during boot reconciliation. The occurrence key,
    window upsert, failed-turn settlement, and membership remain exactly once.
13. **Failed probe.** Attempt 1 records an acknowledged prompt terminal at database time
    `T`, releases one lease, preserves
    suppression, retains `attempt = 1`, and writes `nextProbeAt = T + 1_000ms`. Later
    attempts use the exact jitter-free formula and 60-second cap above. A claim one
    database-time unit before due is refused; a claim at due may proceed and records
    `attempt = 2`. A timeout or disconnect without acknowledged call-terminal or exact
    instance-terminal evidence writes a cancellation intent but does not release the lease.
14. **Crash or live hang during prompt.** Crash after external probe success but before its
    transaction: no proof exists, boot re-establishes cancellation or instance-terminal
    evidence, and no successor starts early. Keep a gateway live while its probe call hangs:
    one durable cancellation intent commits after 115 seconds; one durable instance-
    termination intent commits after 120 seconds if needed; deadline passage alone does not
    unlock a successor. Crash and restart after either intent and prove idempotent redelivery.
    In one ordering, prompt-terminal settlement commits first under the common lock order,
    atomically obsoletes cancellation, and makes the termination transaction write nothing.
    In the other, termination commits first,
    removes the instance from routing, ignores later prompt settlement as an unlock, and
    waits for the instance terminal. Only then may one successor claim. A late completion
    fails the full-token fence and produces no proof or recovery action.
15. **External success race.** A normal successful turn and patrol probe race. One revision
    CAS wins. If the normal turn wins, it requests cancellation of the exact patrol token;
    the patrol terminal uses branch 2 when no new outage exists, resets attempt and due time,
    and writes no recovery or duplicate fan-out. If that patrol call stays live through its
    settlement deadline, termination may still commit; the instance leaves routing before
    delivery, and only its terminal settles through branch 2 or branch 3 according to the
    then-current window state. If termination committed first, the instance-ready fence
    rejects the normal proof and only the instance terminal unlocks the lease.
16. **Failure after recovery.** Adapter failure before the first resumed assignment finishes
    consumes no heard-prod rung and opens the next window. The new window starts at attempt
    0 with no inherited backoff. If an old cancellation remains live, it blocks the first
    claim until settlement, then branch 3 binds the row to the new window and makes it
    immediately due. The branch-1 failure backoff never applies to this cross-window reset.
17. **Per-holder pacing.** Several recovered assignments for one holder queue one attributed
    recovery turn at a time; the rest remain due.
18. **Crash after commit.** Crash after recovery commit and before nudges. The periodic sweep
    runs every due assignment without operator action.
19. **Canonical dependency gate.** The implementation gate fails while
    `wi_a57dee58-7dc6-43e4-b36d-a45959e64ad6` lacks a landed canonical commit.
20. **Release-scoped real I/O.** For every harness named in the release candidate's canonical
    harness-scope manifest, run the real-response matrix. Evidence records harness id,
    adapter binary content digest, gateway commit, failed-turn rows, window/occurrence rows,
    proof row, recovery row, and resumed-turn rows. No fixed harness count appears here.
21. **Suppression-before-replacement.** In both `:DOWN` and boot-reconciled loss, the window,
    occurrence, membership, and suppression commit atomically. Replacement and supervision
    cannot issue a prompt between loss observation and suppression creation. A later
    occurrence refreshes the same window-scoped suppression without creating a second one.
22. **Recovery attribution.** A normal user turn and a patrol probe each record the correct
    `proofSource` and authenticated `recoveryActor`; neither overwrites any occurrence's
    cause principal.
23. **Legacy open migration.** A fully typed legacy open incident maps once to revision 1,
    one legacy-derived occurrence, immediate-due idle probe state, membership, and
    suppression. Restarting migration writes nothing further.
24. **Legacy refusal.** Missing generation, identity, principal, or boot-epoch evidence;
    duplicate open keys; and malformed adapter keys refuse the entire migration before any
    row changes. Legacy closed rows remain immutable.

## Compatibility and migration

This is an internal recovery and supervision contract. It changes no public CLI or wire
request shape. Existing failed turns remain terminal and readable.

Migration first validates the complete legacy set inside one database-owner transaction.
It may map a legacy open incident only when durable typed columns provide its adapter key,
incident id, dead instance, failed generation, observation kind, original cause principal,
and boot epoch. It must not recover missing values from logs, prose, timestamps, or sentinel
defaults. Duplicate open adapter keys, malformed keys, duplicate incident ids, or any
missing fence field refuse the whole migration before a schema or data write commits.

For each valid legacy open incident, migration creates the outage window at revision 1 and
one occurrence whose stable identity is `legacy:<legacyIncidentId>`. The occurrence retains
the legacy observation kind and cause principal; migration does not become the outage cause.
It derives and attaches current affected membership, creates the window-scoped suppression,
and initializes one key-scoped probe row with `leaseEpoch = 0`, `attempt = 0`,
`leaseState = idle`, no claimed window, revision, instance, generation, owner, prompt
deadline, or settlement deadline, and `nextProbeAt` equal to the transaction's database
time so the first post-migration claim is immediately due. A replay sees the stable legacy
identity and writes nothing.

A legacy closed incident remains immutable history and receives no window, occurrence,
lease, suppression, proof, or recovery action. Add the unique partial constraint for one
open outage window per adapter key, the unique occurrence identity constraint, and the
unique adapter-key probe-lease constraint in the same all-or-nothing migration. A restart
before commit repeats validation; a restart after commit observes the constraints and
stable identities and is a no-op.

Create the empty durable adapter-control outbox and its unique `{claimToken, action}`
constraint in that migration. No legacy incident synthesizes cancellation or termination
intent. The first post-migration claim is the only source of such an intent.

ACP provides `session/load` only to restore model context and `session/prompt` to start a
turn. It provides no assignment-resume operation. This invariant stays above that seam:
restore context when possible, then start a new supervised turn.

## Subtraction ruling

Use the existing harness-health incident, assignment membership, supervision pacing, and
ledger. Add only occurrence folding, boot reconciliation, the window revision fence, the
persisted probe lease, and the two token-keyed adapter-control intent actions required to
close proven races.

Do not add a resume queue, replay state, retry worker, operator command, chat marker, or
second assignment population. Deleting assignment responsibility loses because work remains
owed. Accepting a silent orphan loses because durable responsibility is the product promise.

The enforcement rung is transaction plus compare-and-set, backed by restart and real-I/O
tests. Prose alone is not the invariant.

## Open questions and stop conditions

1. **Blocking — implementation and integration.** Which canonical commit will satisfy
   `wi_a57dee58-7dc6-43e4-b36d-a45959e64ad6`? The implementation card must pin it. Until
   then, implementation and integration stop; there is no side-population fallback.
2. **Blocking — release evidence only; non-blocking for implementation and integration.**
   Which registered harnesses and adapter binary digests belong to a release candidate?
   The release-scope manifest must answer this before the release evidence gate runs. This
   spec intentionally does not hardcode the answer.

## Review amendment map

- **F1:** Replaced one incident per death with one open outage window, typed occurrences,
  a monotonic revision, and a proof fence.
- **F2:** Added deterministic boot reconciliation for unobserved ready-generation loss.
- **F3:** Added assumptions, pinned dependency stop conditions, open questions, migration,
  and canonical repository custody.
- **F4:** Defined one persisted in-flight probe lease per adapter key and open window, with
  a claimed-revision fence, exact database-time deadlines, deterministic backoff, restart,
  and replay rules.
- **F5:** Deleted the crash-prone stored chat marker.
- **F6:** Replaced a fixed two-harness smoke with the release-scope registry manifest and
  pinned binary content digests.
- **R1:** Made suppression creation or refresh part of the same window-open or occurrence-
  join transaction, before replacement or supervision can act.
- **R2:** Made the active probe right adapter-key scoped across revision changes.
- **R3:** Defined the database time authority, lease duration, attempt numbering, and exact
  jitter-free retry formula.
- **R4:** Classified each open question by its blocking gate and removed the duplicate
  notification non-goal.
- **R5:** Defined all-or-nothing typed legacy migration, deterministic field mapping,
  replay-safe identities, and restart behavior.
- **R6:** Separated per-occurrence cause principals from lifecycle proof source and
  authenticated recovery actor.
- **S1:** Made holder moves atomically clear source suppression and either install
  destination suppression or restore ordinary supervision.
- **S2:** Added prompt and settlement deadlines, idempotent cancellation, instance-terminal
  fencing, full claim tokens, and stale-completion handling; time alone never unlocks a
  successor probe.
- **S3:** Defined lease settlement for patrol and normal-turn recovery, fresh attempt state
  for the next window, and monotonic epochs that fence cross-window late completions.
- **T1:** Made committed instance termination irrevocable, removed the instance from routing,
  and serialized prompt-terminal settlement against termination creation.
- **T2:** Removed observation-only transport failure as a settlement path; it can request
  cancellation but cannot unlock a successor.
- **T3:** Replaced conflicting reset/backoff prose with three mutually exclusive settlement
  branches selected from the current outage-window state.

## Evidence folded into this revision

- Original frozen design: `art_1dca486c`, SHA-256
  `1e5193b68b9054ae507650a60b7f056365bd5e1d40c6aed22c1da726fe8d2d2c`.
- Independent changes-requested review: `att_10a6b91d`, `art_4d9afce2`.
- First canonical revision: `art_fd6e93bc`, SHA-256
  `17409b8046d4e478b30370ac5ac1d29a84b98beaadd60a48e706f0bc55e250bf`,
  commit `f26ca0df4cf77165b8a01b24212a85f363b30f13`.
- Independent re-review changes requested: `att_17dc4980`, `art_31e37e3c`.
- Second canonical revision: `art_34024d2f`, SHA-256
  `feea465338780b1d04fb4eba5b2c632eff58dc3345fd1ec433cbd9ab0d46f0ed`,
  commit `53dc6d90a1622bbe5d576f3291a8984a1641e8de`.
- Independent second re-review changes requested: `att_00019ad5`, `art_84ae0369`.
- Third canonical revision: `art_909414fe`, SHA-256
  `41553723a450ce17517fbd5c5c9bfc6f1ab5681ae8706b3254b34e2814fcf489`,
  commit `7bf4a422cbd8522975b1430039a8f8b1e0d174ac`.
- Independent third re-review changes requested: `att_51556476`, `art_5ceea0d8`.
- Mike-confirmed harness-health distillate:
  `tightbeam-product/huddle-harness-health-patrol-DISTILLATE.md`.
- Live-work terminal-path recon `art_78b2dc50`: 263 corrected zero-path open assignments,
  primarily failed or ineffective escalation transfers.
- Adapter crash recovery canonical source commit
  `9bf91db3b9f4f7ab97c7506705890095c60ab788`.
- Original implementation baseline `origin/main` `83fb015`; this revision does not treat
  that stale commit as current source truth.
