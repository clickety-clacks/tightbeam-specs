# 0.2 adapter-recovery resume invariant

Status: READY FOR INDEPENDENT RE-REVIEW  
Work item: `wi_cbb56e71-5c93-41c0-bfb9-e5db2dc87c91`  
Producer assignment: `asg_aaaa71d9-273e-454f-bd32-cdc77a9ab7cd`  
Supersedes artifact: `art_1dca486c`, SHA-256
`1e5193b68b9054ae507650a60b7f056365bd5e1d40c6aed22c1da726fe8d2d2c`  
Revision basis: changes-requested `att_10a6b91d`, report `art_4d9afce2`

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
  one open window revision. It has an owner, attempt number, lease expiry, and next due time.

## Required design

### 0. One authoritative outage window absorbs concurrent deaths

A matching `:DOWN` for an adapter instance that reached ready state appends one occurrence
before the coordinator schedules its replacement. The transaction upserts the one open
window for the adapter key, increments its revision, records the dead instance and failed
generation, and attaches the current affected assignments. A fast recovery cannot overtake
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
new prompt can run. Replaying boot reconciliation writes nothing after the occurrence key
exists.

Initial boot has no prior ready generation and opens no window. A clean gateway shutdown
has planned-close rows and opens no window. A never-ready generation opens no window. These
negative rules prevent boot from waking every assignment.

### 2. Recovery authority is a revision-bound service proof

The current adapter instance must first reach the existing instance-scoped ready state. A
stale ready signal, planned recycle, process spawn, or successful ACP `initialize` call is
not a recovery edge.

The harness-health patrol may claim at most one in-flight probe lease for an adapter key and
window revision. Claim is a compare-and-set on the persisted lease row. The row records
`attempt`, `leaseOwner`, `leaseUntil`, and `nextProbeAt`.

A failed prompt or committed transport failure releases the lease, increments the attempt,
and computes `nextProbeAt` from the canonical bounded backoff policy. No probe may start
before that time. A gateway crash leaves the lease durable. Boot reconciliation expires a
lease only after `leaseUntil`; it never treats an unknown external prompt result as proof.
The next claimant runs a new prompt after the due time. Tightbeam never replays the old
prompt.

A successful normal user or agent turn can supply proof without owning the patrol lease.
It must still bind the same open window revision and satisfy the generation fence. If it
wins recovery, a later probe completion sees `already_recovered` and writes nothing.

For a normal turn, the ledger's `delivered` terminal and recovery transition commit in one
database transaction. For a patrol probe, its success row and recovery transition commit in
one transaction. If the gateway dies after the external prompt succeeds but before commit,
no proof exists. The window stays open, and a new lease becomes claimable only after the
persisted lease boundary permits it.

### 3. Incident membership is the recovery set

When an outage window opens or gains an occurrence, it attaches every open assignment held
by an active session on the adapter key. While it remains open, the same derived query
attaches newly opened or newly assigned work on that key.

Recorded membership answers only the historical question, "was this assignment on the
affected adapter during this window?" It never replaces the assignments table as the
current work population.

At recovery, Tightbeam takes the union of historical membership and one current derived
membership query inside the transaction. It then re-checks each assignment and holder:

- Closed or revoked assignments need no turn.
- Assignments whose holders retired follow the retirement contract.
- Assignments whose holders moved to another adapter leave this window's active set.
- Still-open assignments on the recovered key remain in scope.

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
generation, proof turn id, cause principal, and counts for armed, already-continuing,
closed, retired, and moved assignments. Membership rows carry the exact assignment list.

Only the compare-and-set winner arms assignments and clears suppression. A repeated handler
returns `already_recovered` and writes nothing. All occurrences in the closed window settle
together; no occurrence owns a second close, lifecycle row, or supervision fan-out.

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
  later transaction observes the earlier result and settles normally.
- Boot reconciliation runs before replacement scheduling and before any recovery probe.
  It is replay-safe across repeated crashes.
- A gateway restart with an open window preserves probe attempt, lease, backoff, membership,
  and suppression. It does not infer proof from logs or an external prompt response.
- A crash after recovery commit but before nudges loses only latency. Due pacing remains.
- A new assignment opened after recovery follows ordinary supervision and does not join the
  closed window.
- A death that races a successful prompt either increments the open revision first and
  fences the proof, or commits after recovery and opens the next window. No ordering loses
  the death or lets one proof close two windows.

## Operator-visible record

The incident, occurrence, proof, membership, and `adapter_recovery_armed` lifecycle rows are
the complete operator record. Each row carries its cause and principal.

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
6. **Assignment race.** Close, revoke, move, and retire races produce no stale wake.
7. **Concurrent deaths.** Two ready deaths before proof create two occurrence rows in one
   open window. The second increments revision. A proof for the first revision is fenced.
   One proof for the final revision closes once and writes one lifecycle row.
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
13. **Failed probe.** A failed probe releases one lease, increments attempt, preserves
    suppression, and sets bounded `nextProbeAt`. No second probe runs before due time.
14. **Crash during prompt.** Crash after external probe success but before its transaction.
    No proof exists. The lease prevents concurrent retry, then expires. A new prompt proves
    recovery once; the old prompt is not replayed.
15. **External success race.** A normal successful turn and patrol probe race. One revision
    CAS wins; the loser writes no recovery or duplicate fan-out.
16. **Failure after recovery.** Adapter failure before the first resumed assignment finishes
    consumes no heard-prod rung and opens the next window.
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

## Compatibility and migration

This is an internal recovery and supervision contract. It changes no public CLI or wire
request shape. Existing failed turns remain terminal and readable.

Migrate existing harness-health incidents by adding window revision, occurrence rows, and
probe-lease fields. A legacy open incident becomes revision 1 with one migration occurrence
whose cause and principal identify the migration. A legacy closed incident remains immutable
history and receives no synthetic recovery action.

Add a unique partial constraint for one open outage window per adapter key and a unique
occurrence identity constraint. Migration must refuse if existing open rows violate the
one-window invariant; an operator must reconcile those rows explicitly.

ACP provides `session/load` only to restore model context and `session/prompt` to start a
turn. It provides no assignment-resume operation. This invariant stays above that seam:
restore context when possible, then start a new supervised turn.

## Subtraction ruling

Use the existing harness-health incident, assignment membership, supervision pacing, and
ledger. Add only occurrence folding, boot reconciliation, the window revision fence, and
the persisted probe lease required to close proven races.

Do not add a resume queue, replay state, retry worker, operator command, chat marker, or
second assignment population. Deleting assignment responsibility loses because work remains
owed. Accepting a silent orphan loses because durable responsibility is the product promise.

The enforcement rung is transaction plus compare-and-set, backed by restart and real-I/O
tests. Prose alone is not the invariant.

## Open questions and stop conditions

1. Which canonical commit will satisfy
   `wi_a57dee58-7dc6-43e4-b36d-a45959e64ad6`? The implementation card must pin it. Until
   then, implementation and integration stop; there is no side-population fallback.
2. Which registered harnesses and adapter binary digests belong to a release candidate?
   The release-scope manifest answers this for each candidate. This spec intentionally does
   not hardcode the answer.
3. If a future product requires user-facing recovery notification, it needs a separate
   durable-delivery design and review. This invariant supplies operator evidence only.

## Review amendment map

- **F1:** Replaced one incident per death with one open outage window, typed occurrences,
  a monotonic revision, and a proof fence.
- **F2:** Added deterministic boot reconciliation for unobserved ready-generation loss.
- **F3:** Added assumptions, pinned dependency stop conditions, open questions, migration,
  and canonical repository custody.
- **F4:** Defined one persisted in-flight probe lease per adapter key and window revision,
  with attempt, expiry, bounded backoff, restart, and replay rules.
- **F5:** Deleted the crash-prone stored chat marker.
- **F6:** Replaced a fixed two-harness smoke with the release-scope registry manifest and
  pinned binary content digests.

## Evidence folded into this revision

- Original frozen design: `art_1dca486c`, SHA-256
  `1e5193b68b9054ae507650a60b7f056365bd5e1d40c6aed22c1da726fe8d2d2c`.
- Independent changes-requested review: `att_10a6b91d`, `art_4d9afce2`.
- Mike-confirmed harness-health distillate:
  `tightbeam-product/huddle-harness-health-patrol-DISTILLATE.md`.
- Live-work terminal-path recon `art_78b2dc50`: 263 corrected zero-path open assignments,
  primarily failed or ineffective escalation transfers.
- Adapter crash recovery canonical source commit
  `9bf91db3b9f4f7ab97c7506705890095c60ab788`.
- Original implementation baseline `origin/main` `83fb015`; this revision does not treat
  that stale commit as current source truth.
