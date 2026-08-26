# Stale-running-turn settlement — v1

Status: SPEC CANDIDATE — review reconciliation revision. This artifact
supersedes the incorrectly recorded SHA on `art_e081e04b`. It is bounded to
the two supplied specimens, additive to `eea3e9a`, and does not replace
automatic adapter-death recovery.

Evidence boundary: PHANTOM `att_45772d58`, confirmation `att_7ef386ea`, and the
ruled prior-specimen authority `dr_b7e2f1ff-c13f-4a36-9454-ce5f9026c71a`, which
identifies the 19-hour stuck turn and tonight's five-turn specimen in Mike
message `s_fa15c670-c408-44d7-9f28-917d6b71d2a9` at epoch `1787716372866`.
The adjacent retired-session lane `wi_154bf46b` remains excluded.

## Goal

1. Tightbeam SHALL expose one closed agent verb, `settle-turn`, for an
   authenticated operator to settle one stale or phantom `running` turn on a
   still-extant active session.
2. The request SHALL carry `sessionKey`, positive `turnSeq`, `outcome`,
   `reason`, and `idempotencyKey` as ordinary parameters. `outcome` SHALL be
   exactly `cancel` or `fail`. `reason` SHALL be non-empty and bounded to 512
   Unicode characters. The verb SHALL carry no work-item target.
3. `cancel` SHALL write the existing terminal status `canceled`. `fail` SHALL
   write the existing terminal status `failed` and the bounded reason in the
   existing turn error field. The verb SHALL never write `failed_unknown`.
4. The authenticated principal SHALL be an admin operator represented as
   `user:<userId>`. A session principal, agent principal, process principal,
   unauthenticated caller, and non-admin user SHALL be refused before any turn
   mutation.
5. The settlement decision SHALL use a synchronous lane settlement call for
   the exact `(sessionKey, turnSeq)`. The lane call SHALL retain its mailbox
   serialization across the live/stale decision and the guarded database
   transaction. The call SHALL report one of `live`, `stale`, or `ambiguous`.
6. The lane SHALL report `live` when that exact sequence is its current task or
   when the harness reports a live provider request correlated to that target's
   exact `prompt_dispatched` lifecycle event, `adapterGen`, and current
   harness-session identity. The verb SHALL return `turn_live` and SHALL
   perform no mutation. The lane SHALL report `ambiguous` when it cannot
   establish the target's live status, when the lane is unavailable, when its
   in-memory sequence disagrees with the durable running row, when the provider
   probe cannot answer, or when the serialization call is lost or re-entered.
   The verb SHALL return `turn_status_ambiguous` and SHALL perform no mutation.
   The lane SHALL report `stale` only when its task is absent and the bounded
   provider probe returns no live request for the exact target while it still
   holds the serialization call and performs the CAS.
   The provider check SHALL use the local read-only
   `Tightbeam.Acp.Conn.probe_request/5` seam defined in Architecture; it SHALL
   never issue an ACP or harness request.
7. The agent operating pattern SHALL be read-only diagnosis followed by human
   operator action. An agent MAY report the exact session, turn, observed lane
   state, and bounded evidence to an authenticated admin operator. An agent
   SHALL NOT invoke `settle-turn`, even when it holds an assignment or detects
   a phantom. The admin operator MAY then invoke the verb and the agent MAY
   read the resulting terminal truth and normal queue drain. No automatic
   component or agent self-nudge SHALL invoke this verb.
8. The substrate SHALL not classify staleness from elapsed time, queue age,
   adapter generation, process age, or a heuristic. The operator supplies the
   settlement decision; the substrate verifies only deterministic eligibility.
9. For a `stale` result, the lane's serialized settlement call SHALL verify all
   of the following and then perform the transition before releasing its
   mailbox: the session row exists, the session state is `active`, the target
   row belongs to that session, the target status is `running`, and `endedAt`
   is NULL. A nudge or task start that arrives during this call SHALL wait
   behind it and SHALL not create a live task in the probe-to-CAS window.
10. The transition SHALL be a compare-and-set on the exact target row. Its
   predicate SHALL include `seq`, `sessionKey`, `status='running'`,
   `endedAt IS NULL`, and the active-session condition. A zero-row CAS SHALL
   leave the row unchanged. The operation SHALL re-read the exact target and
   session in the same lane call and SHALL return existing terminal truth when
   the target is terminal, `session_retired` when the active-session predicate
   lost to retirement, `turn_not_found` when the target disappeared, or
   `turn_status_ambiguous` when the row cannot be classified without guessing.
11. The winning CAS SHALL append the existing `terminal_committed` lifecycle
    event in the same transaction. The event SHALL have outcome `canceled` or
    `failed`, cause exactly `operator:stale-running-turn`, and principal
    exactly the authenticated `user:<userId>`. The event SHALL not use the
    running turn's stale owner lease as operator authority.
12. The winning CAS SHALL publish the existing `turn.ended` durable effect in
    the same transaction. It SHALL not create a `stale` state, shadow turn,
    parallel settlement table, or replacement queue.
13. After commit, the operation SHALL release the session lane through the
    existing terminal callback and drain path. The lane SHALL claim the next
    queued turn only after the target is terminal. Queued turns SHALL remain
    queued and valid.
14. If no lane is currently registered but the session is active, the
    operation SHALL obtain a settlement-reserved lane seam. Lane creation SHALL
    suppress the lane's initial self-nudge and reconciliation nudges until the
    settlement call returns. The operation SHALL execute the settlement call
    before any task-start message. Failure to acquire or retain that reservation
    SHALL be `turn_status_ambiguous`, not permission to mutate the ledger
    directly.
15. A successful response SHALL identify `sessionKey`, `turnSeq`, the terminal
    status, and whether this call won the CAS or replayed existing terminal
    truth. A denial SHALL identify a stable code from the eligibility and
    authorization vocabulary in Acceptance.
16. The request's `idempotencyKey` SHALL be 1–200 characters and SHALL be
    scoped by `(principal, verb, idempotencyKey)`. The request fingerprint SHALL
    be the SHA-256 digest of canonical JSON containing `verb`, `sessionKey`,
    `turnSeq`, `outcome`, and the bounded `reason`. The handler SHALL use the
    existing durable `wire_idempotency` ledger, extended with the fingerprint
    and canonical response fields, inside the same transaction as the winning
    settlement. A same-key, same-fingerprint retry SHALL return the stored
    settlement result. A same-key, different-fingerprint request SHALL return
    `idempotency_key_conflict` and SHALL perform no mutation. A different key
    against an already-terminal target SHALL return that target's existing
    terminal truth and SHALL perform no second settlement. The `turns` row and
    its lifecycle event SHALL remain the only terminal source of truth; the
    idempotency row is replay metadata, not a terminal state.
17. The accepted and denied dispatch observations SHALL record the verb,
    target identifiers, outcome, principal, idempotency-key digest, and stable
    result code. They SHALL not record the prompt body or raw credentials. The
    lifecycle row SHALL retain the cause and principal required by item 10.

## Non-Goals

- This verb does not detect stale turns automatically or add a timeout policy.
- This verb does not duplicate `eea3e9a` adapter-death recovery.
- This verb does not retire, delete, or invalidate a session or its queued
  turns. Retired/deleted-session queue invalidation remains the owner of
  `wi_154bf46b`.
- This verb does not interrupt a live task or send a harness cancel. The
  existing `cancel` verb remains the live-task cancellation path.
- This verb does not restart a gateway, adapter, session, or lane.
- This verb does not alter credentials, configuration, identity, release
  targets, deployment, or the 0.1.8 line.
- This work item remains untargeted. A session and turn are request parameters,
  not a work-item target.

## Terms

- **Target** — the exact pair `(sessionKey, turnSeq)` named by one request.
- **Still-extant session** — a session row with `state='active'`; a retired or
  absent row is not eligible.
- **Live** — the session lane owns the target sequence as its current task.
- **Stale** — the session lane owns the decision seam, has no task for the
  target, and receives a bounded provider response that no live request is
  correlated to that target while the durable row still says `running`.
- **Ambiguous** — the substrate cannot establish the live/stale distinction at
  that seam. Ambiguity is a refusal, never an authorization to settle.
- **Settlement** — one terminal CAS to `canceled` or `failed`, plus its
  same-transaction lifecycle event and terminal publication effect.
- **Operator principal** — the authenticated admin identity `user:<userId>`.
- **Existing terminal truth** — the target's terminal `turns` row and its
  `terminal_committed` lifecycle event. It outranks a caller's stale receipt.
- **Provider probe** — the local read-only lookup
  `Tightbeam.Acp.Conn.probe_request(conn, acp_request_id,
  harness_session_id, adapter_generation, timeout_ms)`. It reads the adapter
  connection's pending request entry only when that connection's generation
  equals `adapter_generation`; it does not send JSON-RPC, ACP, or harness
  traffic.
- **Correlation fence** — one coordinator-owned lease over the checked
  adapter connection generation. The lease is held from generation checkout
  through the local probe and the settlement transaction. Adapter replacement,
  close, and generation bump invalidate the lease and make the operation
  ambiguous; they cannot silently succeed while the lease is held.
- **Pointer snapshot** — the durable current `harness_pointers` row identity
  and its `harnessSessionId`, read as one pair. The row identity is the fence
  against a later pointer append.
- **Generation-fence contract** —
  `AdapterCoordinator.with_generation_fence(coordinator, adapter_key,
  expected_generation, owner_scope)`, where `owner_scope` contains the
  `lane_pid`, `gateway_pid`, and one callback. It checks out the current
  adapter at the expected generation, monitors both distinct owner pids,
  runs the callback once while replacement and generation-bump paths are
  fenced, and releases the fence in an `after` path for every callback return,
  exception, timeout, or refusal. A `DOWN` from either owner invalidates the
  fence, aborts the callback before commit, releases the fence, and returns
  `{:error, :owner_lost}`. An unavailable adapter or invalidated fence returns
  an error that the lane maps to `turn_status_ambiguous`.

## Assumptions

- `turns` already provides the terminal statuses, one-running-turn-per-session
  admission invariant, terminal CAS seam, and terminal publication sweep.
- `TurnLifecycle` already provides ordered durable events with required `cause`
  and `principal` fields. The operator cause is an additive authorized terminal
  authority; it is not a new lifecycle state.
- The lane is the process authority for whether a task is executing. A database
  read alone cannot prove that a live task is absent.
- The existing `wire_idempotency` ledger is the durable replay seam. Its
  additive fingerprint and canonical-response columns do not replace or shadow
  the `turns` terminal state.
- The target `turns` row's positive `adapterGen`, its exactly-one
  `prompt_dispatched` lifecycle event with a positive `acpRequestId`, the
  session's current `harnessSessionId`, and the current adapter connection's
  generation form the provider-probe correlation. A missing or duplicated
  prompt-dispatch event, missing generation, missing harness-session identity,
  or any mismatch is uncorrelatable and therefore ambiguous.
- The provider probe is a new local read seam because the pinned source has no
  public request-status operation. Its contract is specified here so an
  implementation cannot issue a new provider request or inspect an unbounded
  private structure.
- The settlement protocol can hold a coordinator generation fence while it
  performs the local probe and database CAS. The durable pointer chain is
  append-only, so its current row identity can participate in the CAS
  predicate. These two fences are required because `Org.append_pointer/4`
  commits independently and `AdapterCoordinator.adapter_for/2` returns a
  process-owned adapter generation.
- Boot recovery remains authoritative after process loss: every still-running
  row encountered at recovery becomes `failed_unknown` with cause
  `boot-recovery`, and is never requeued. A settlement request that loses its
  process before its CAS commits therefore makes no operator claim.
- A commit followed by process loss is recoverable from the existing terminal
  publication and pending-session reconciliation sweeps.
- The supplied evidence establishes two specimens: the earlier approximately
  19-hour stuck turn and tonight's confirmed phantom set. The evidence does not
  authorize a numeric age threshold.

## Invariants

1. Exactly one terminal status wins for a target. A live runner completion,
   operator settlement, retirement, and boot recovery race through existing
   terminal truth; none may overwrite another terminal status.
2. The live/stale/ambiguous decision and the settlement CAS execute through one
   concrete `SessionLane.settle_stale/3` synchronous call with shape
   `SessionLane.settle_stale(lane_pid, reservation_token, operator_request)`;
   `operator_request` contains the target and all verb parameters. The lane
   SHALL hold its mailbox serialization while the correlation fence, local
   probe, and CAS transaction run. A caller SHALL NOT sample lane state,
   release the call, and later perform a database update.
3. A live or ambiguous target causes zero writes to `turns`, lifecycle events,
   terminal publications, queue rows, and session state.
4. A missing target, a target whose session is absent, a target on a retired
   session, and a target whose status is not `running` cause zero state
   mutation. A non-running target returns its existing terminal truth when
   available.
5. An operator settlement cannot claim or reuse the prior lane owner lease.
   Its lifecycle principal and cause identify the operator settlement directly.
6. The settlement never cancels queued work. Queue release means only that the
   already-queued next turn becomes claimable through the normal active-session
   lane drain.
7. Replaying an idempotency key or retrying after an unknown response cannot
   create a second terminal event, terminal publication, or queue release.
8. No automatic component may invoke this operator verb. Adapter readiness,
   adapter death, timers, patrol, restart, and queue scans retain their
   existing behavior.
9. A fresh-lane settlement reservation suppresses the initial self-nudge and
   every reconciliation nudge. Nudges received while reserved SHALL coalesce
   into one deferred-drain flag. Releasing the reservation SHALL clear the
   reservation and perform exactly one normal drain; it SHALL not drop queued
   work or run a task while the reservation is held.

## Architecture

1. Add `settle-turn` to the closed `/agent/dispatch` verb set and to the CLI
   command mapping. The wire request SHALL put all selectors in `params`:
   `sessionKey`, `turnSeq`, `outcome`, `reason`, and `idempotencyKey`. The
   server SHALL derive the principal from authenticated admin identity.
2. Add a settlement-reserved lane acquisition seam
   `LaneManager.ensure_settlement_lane/2`. It SHALL create a lane with a
   reservation token when none exists, prevent `SessionLane.init/1` and
   reconciliation from starting work, and return `turn_status_ambiguous` if
   another creator wins without the requested reservation. The reservation
   SHALL be released exactly once after the settlement call, with one normal
   drain.
3. Add the exact `SessionLane.settle_stale/3` synchronous call
   `SessionLane.settle_stale(lane_pid, reservation_token, operator_request)`.
   Its handler SHALL first obtain the target's adapter key and positive
   `adapterGen` as a preliminary read; missing values are ambiguous. It SHALL
   then acquire a correlation fence from
   `AdapterCoordinator.with_generation_fence/4` for the target's adapter key
   and expected `adapterGen`, with `lane_pid=self()`, the synchronous caller's
   `gateway_pid`, and one callback as its owner scope. The coordinator SHALL
   monitor both owners. Within that callback it SHALL read exactly one
   `prompt_dispatched` lifecycle event for the target, read the target's
   `adapterGen`, and read one durable current-pointer snapshot consisting of
   pointer row identity and `harnessSessionId` through
   `Org.current_pointer_snapshot/2`. It SHALL obtain
   `{:ok, adapter_pid, connection_generation}` from
   `AdapterCoordinator.adapter_for/2` under that fence, obtain the connection
   from `Acp.Adapter.conn(adapter_pid)` under the same fence, refuse before
   probing unless the generation and pointer snapshot are valid, and then call
   `Tightbeam.Acp.Conn.probe_request/5` on that fenced connection. It SHALL
   retain the lane mailbox callback and the coordinator fence while it invokes
   the guarded settlement transaction. A task cannot claim or start between
   that inspection and the CAS. If either owner receives `DOWN`, the
   coordinator SHALL invalidate the fence and the callback SHALL stop before
   commit; the lane SHALL return `turn_status_ambiguous` when it can reply.
   If the callback or transaction raises, times out, or returns live or
   ambiguous, the fence SHALL be released by the `after` path before the lane
   replies. Fence release SHALL then process queued adapter close or
   replacement messages in FIFO order through the normal coordinator teardown
   and restart path. A healthy adapter is not closed merely because a fence
   was released.
4. `probe_request/5` SHALL accept `(conn, acpRequestId, harnessSessionId,
   adapterGen, timeoutMs)` together with the coordinator-issued connection
   generation fence from item 3. It SHALL return `{:live, acpRequestId}` only
   when that checked connection is generation `adapterGen`, the pending
   entry's session id equals `harnessSessionId`, and that entry remains
   unresolved. It SHALL return `:absent` only when the checked
   current-generation connection has no entry for that exact request id. A
   missing, duplicated, or mismatched
   `prompt_dispatched` event or any generation/pointer mismatch SHALL prevent
   the call and produce `{:unknown, :uncorrelatable}`.
5. In the stale branch, the correlation fence SHALL remain held while a
   write-locked transaction re-reads the active session, target, exactly-one
   dispatch event, target `adapterGen`, and current-pointer snapshot. The
   transaction SHALL refuse as `turn_status_ambiguous` unless every value
   equals the fenced observation, including the current pointer row identity,
   pointer `harnessSessionId`, target generation, and dispatch request id. Its
   guarded target update SHALL include the current-pointer identity and
   `harnessSessionId` as an `EXISTS` predicate, with no newer pointer row for
   the session. A pointer append that committed before the write lock makes
   the CAS ineligible; an append that follows the commit is a later
   linearized event. Adapter replacement or generation change invalidates the
   held fence and makes the result ambiguous. An owner loss observed after the
   transaction opens but before its commit SHALL roll the transaction back;
   an owner loss after commit SHALL leave the committed terminal truth to the
   existing publication and reconciliation sweeps. The transaction SHALL combine
   the guarded target update, lifecycle append, `turn.ended` publication
   effect, and the `wire_idempotency` fingerprint/response write. It SHALL
   return the row's terminal result when another writer won.
6. After a winning commit, use the existing terminal callback, publication,
   and lane drain. If the response is lost after commit, the existing
   unpublished-terminal and pending-session reconciliation paths SHALL make
   the same result observable after restart.
7. Keep the current `cancel` handler and its lane-owned kill unchanged. A
   live task must use `cancel`; `settle-turn` is only for the proven absence of
   that task in the lane seam.
8. Expose the feature through the existing capability/version mechanism before
   a client sends it. An older server SHALL reject the closed verb as
   `unknown_verb`; an older client SHALL continue using existing verbs and
   statuses without schema failure.
9. Emit one accepted or denied dispatch observation per request and one
   `terminal_committed` lifecycle event only for a winning settlement. The
   observability record SHALL use a digest for the idempotency key and reason
   where the existing privacy boundary requires redaction.
10. Rollback is additive disablement: removing the handler or capability makes
   future requests return `unknown_verb` and leaves all already-terminal rows,
   lifecycle events, and publications intact. Rollback SHALL never reverse a
   terminal status or recreate a queued turn.
11. The source-lineage evidence SHALL pin the owned product clone at
   `7a70a2f616363074514237b5bee48ba67c52e2ea`, prove that
   `eea3e9a1eb73a63ae41eafa05fb42e410f362ee7` is an ancestor, and identify the
   exact `eea3e9a` subject `Recover after proven adapter death despite cleanup
   failure`. The evidence SHALL be recorded as an immutable supporting artifact
   beside this spec.

## Acceptance

1. **Authorized cancel.** Given an active session, a durable `running` target,
   a lane result of `stale`, and an authenticated admin `user:mike`, when the
   operator sends `settle-turn` with `outcome=cancel`, then exactly one CAS
   changes the row to `canceled`, exactly one lifecycle event carries
   `cause=operator:stale-running-turn` and `principal=user:mike`, and the
   response identifies that target as the CAS winner.
2. **Authorized fail.** Given the same fixture, when `outcome=fail` and a
   bounded reason are supplied, then the row becomes `failed`, the reason is
   stored in the existing error field, and no `failed_unknown` row is created.
3. **The two supplied specimens.** Given fixtures for the earlier 19-hour
   stuck turn and the five confirmed phantom turns `69089`, `69101`, `69104`,
   `69109`, and `69110`, when an admin settles each exact stale target, then
   each target has one terminal row, one operator lifecycle event, and no
   second running row remains for its session. The proof cites
   `att_45772d58`, `att_7ef386ea`, and `dr_b7e2f1ff-c13f-4a36-9454-ce5f9026c71a`.
4. **Live refusal.** Given a target that the lane reports `live`, when the
   operator sends either outcome, then the response is `turn_live` and the
   target row, lifecycle table, queue, and publication table are byte-for-byte
   unchanged.
5. **Live and ambiguous runtime refusal.** Given a missing lane, an unavailable
   runtime probe, a provider probe that reports a live request for the target,
   or a lane/durable sequence disagreement, when the operator sends either
   outcome, then the response is respectively `turn_status_ambiguous`,
   `turn_status_ambiguous`, `turn_live`, or `turn_status_ambiguous`, and no
   settlement mutation occurs. A provider probe that returns no request is the
   only provider result that can support `stale`.
6. **Provider probe contract.** Given a target row with `adapterGen=7`, exactly
   one `prompt_dispatched` lifecycle event for that target with
   `acpRequestId=42`, the current pointer `harnessSessionId=hs-1`, and
   `AdapterCoordinator.adapter_for/2` returns the current adapter connection
   at generation 7, when
   `probe_request(conn, 42, "hs-1", 7, 1000)` reads a pending entry with that
   id before the 1,000 ms deadline, then it returns `{:live, 42}` whether or
   not the original ACP caller has received its own request timeout, because
   the adapter has not resolved the pending entry. Given the same correlation
   and no pending entry on generation 7 while the coordinator fence remains
   valid, it returns `:absent`. Given a missing
   or duplicate dispatch event, a missing or malformed event request id, a
   missing or zero target generation, a pointer mismatch, or a target stamped
   generation 6 while the only available connection is generation 7, it
   returns `{:unknown, :uncorrelatable}` before probing. A target stamped
   generation 7 with request id 42 present only on an old generation-6
   connection has no entry on the checked generation-7 connection and therefore
   returns `:absent`; the old entry is not evidence for this target. Given a
   closed
   connection, provider error, probe timeout, or late reply after the probe
   deadline, it returns `{:unknown, reason}`; the lane releases its reservation
   and returns `turn_status_ambiguous`. The probe sends no provider request,
   cancels no provider request, and ignores a late local reply.
7. **Eligibility refusal.** Given each of: absent session, retired session,
   absent turn, queued turn, delivered turn, canceled turn, failed turn, and
   failed-unknown turn, when the operator sends `settle-turn`, then the
   response is respectively `session_not_found`, `session_retired`,
   `turn_not_found`, or `turn_not_running` as applicable, and no new terminal
   event or queue change occurs.
8. **Authorization refusal.** Given a session principal, agent principal,
   process principal, non-admin user, or missing authentication, when the
   caller sends `settle-turn`, then the response is `not_authorized` and the
   target remains unchanged.
9. **Correlation replacement race.** Given a stale sample with pointer row P,
   harness session `hs-1`, target `adapterGen=7`, and a generation-7 checked
   connection, when a pointer append commits or the coordinator replaces that
   connection before the write-locked correlation re-read, then the result is
   `turn_status_ambiguous`, the target and all terminal/publication/queue
   tables are unchanged, and no provider request or cancellation is sent.
   Given the pointer append or generation replacement occurs only after the
   settlement CAS commits, then the settlement remains the single earlier
   linearization point and the later pointer/generation event does not create a
   second terminal event.
10. **CAS race.** Given one stale target and two concurrent settlement requests,
   when both reach the exact `SessionLane.settle_stale/3` CAS, then exactly one changes the row and appends the
   lifecycle event; the loser returns the existing terminal truth and creates
   no event or publication. Given a runner completion races the operator, the
   same one-terminal rule decides the result. Given a queued successor sends a
   nudge while the lane settlement call holds its serialization, then the
   successor cannot claim before the target CAS commits; if a task is already
   current at the call boundary, the operator receives `turn_live` and the CAS
   does not run.
11. **Idempotent retry.** Given a committed settlement and a lost first
   response, when the same request is retried with the same idempotency key,
   then the response identifies the existing terminal truth and counts one
   lifecycle event, one terminal publication, and one queue release.
12. **Idempotency collision.** Given a principal and key already recorded for
    one target/outcome/reason fingerprint, when the same principal reuses that
    key with a different target, outcome, or reason, then the response is
    `idempotency_key_conflict` and the second target, lifecycle table, queue,
    and publication table remain unchanged. Given a different principal uses
    the same key, then the request has a separate scope and is evaluated only
    against its own target.
13. **Queue release.** Given one stale running target and one queued successor,
    when settlement commits, then the successor remains queued until the
    existing terminal callback/drain, then claims as the next turn. The
    settlement never deletes, cancels, or rewrites that successor.
14. **Restart before commit.** Given a process loss before the settlement CAS
    commits, when the gateway restarts, then existing boot recovery handles the
    still-running row as `failed_unknown` and the lost operator request does
    not reappear as a `canceled` or `failed` settlement.
15. **Restart after commit.** Given process loss after the settlement CAS but
    before the response or queue nudge, when the gateway restarts, then the
    existing unpublished-terminal and pending-session sweeps publish the
    committed terminal truth and drain the active session exactly once.
16. **Compatibility and rollback.** Given an older client or server, then the
    unsupported verb is rejected as `unknown_verb` and existing `cancel`,
    automatic adapter recovery, retired-session handling, and terminal statuses
    retain their current behavior. Given the new handler is disabled after a
    successful settlement, existing terminal rows remain terminal and no queue
    row is recreated.
17. **Observability.** Given one accepted request, one live refusal, one
    ambiguous refusal, and one authorization refusal, then each produces one
    stable dispatch observation with the target and principal, and only the
    accepted CAS produces the operator lifecycle event. No observation contains
    prompt text, credentials, or an unbounded reason.
18. **Fresh-lane ordering.** Given no registered lane, one active session, and
    one queued successor, when settlement-reserved acquisition starts, then
    the fresh lane emits no initial or reconciliation nudge before the
    settlement call returns. A queued successor cannot claim during the held
    reservation. After release, exactly one normal drain may claim it. If the
    reservation cannot be acquired or retained, the result is
    `turn_status_ambiguous` and the target remains unchanged.
19. **Agent operating pattern.** Given an agent observes a candidate phantom,
    when it needs operator action, then it emits a read-only escalation with
    the exact `sessionKey`, `turnSeq`, lane result, correlation evidence, and a
    bounded reason; it does not invoke `settle-turn`. Given an authenticated
    admin operator then invokes the verb, the agent may consume the result and
    observe the normal terminal callback and queue drain. An agent principal's
    direct invocation remains `not_authorized` with zero mutation.
20. **Fence owner loss and teardown.** Given a stale sample with a monitored
    `lane_pid` and `gateway_pid`, a pending adapter close or replacement, and a
    valid generation fence, when the lane or gateway owner dies during the
    provider probe, then the coordinator observes `DOWN`, invalidates and
    releases the fence automatically, the callback performs no settlement CAS,
    and the surviving request path returns `turn_status_ambiguous` or no
    response if its gateway died. When the gateway restarts before any CAS,
    boot recovery applies the existing `failed_unknown` rule to the still
    running row. When owner loss occurs after the CAS commits, the committed
    terminal truth remains authoritative and existing reconciliation publishes
    it exactly once. When the callback raises, the probe times out, or the
    probe returns live or ambiguous, the `after` release occurs before the
    response and no settlement CAS occurs for the non-winning result.
21. **Fence release and adapter replacement.** Given a close or replacement
    message arrives while the fence is held, when the callback returns,
    refuses, times out, or loses an owner, then the fence is released before
    the queued message is handled; the normal close/restart path then closes
    the old adapter and permits the next adapter generation to be checked out
    in FIFO order. A queued replacement cannot remain blocked on the released
    fence. Given no queued teardown and a healthy adapter, release performs no
    forced close or generation bump.
22. **Source lineage and deterministic replay matrix.** Given the immutable
    source-evidence artifact, then its recorded commands prove the exact
    `eea3e9a1eb73a63ae41eafa05fb42e410f362ee7` object and its ancestry to the
    owned product clone, and its cited lane, ledger, lifecycle, publication,
    recovery, capability, and idempotency seams resolve in that checkout. The
    acceptance suite SHALL then run the above
    cases against fresh throwaway databases, fixed session/turn identifiers,
    fixed principals, and fixed idempotency keys. It SHALL assert exact status,
    code, cause, principal, event count, publication count, and queue state;
    wall-clock age SHALL not appear in any expected result.

## Open Questions

None. The operator-only authorization, `settle-turn` name, parameter shape,
three-valued runtime refusal, terminal statuses, cause/principal values, and
CAS/restart behavior are ruled by this candidate. Implementation may choose
internal function names and storage indexes only if it preserves these clauses.
