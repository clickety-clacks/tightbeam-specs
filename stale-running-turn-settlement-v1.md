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
   `requestRef` or ACP request identity. The verb SHALL return `turn_live` and
   SHALL perform no mutation. The lane SHALL report `ambiguous` when it cannot
   establish the target's live status, when the lane is unavailable, when its
   in-memory sequence disagrees with the durable running row, when the provider
   probe cannot answer, or when the serialization call is lost or re-entered.
   The verb SHALL return `turn_status_ambiguous` and SHALL perform no mutation.
   The lane SHALL report `stale` only when its task is absent and the bounded
   provider probe returns no live request for the exact target while it still
   holds the serialization call and performs the CAS.
7. The substrate SHALL not classify staleness from elapsed time, queue age,
   adapter generation, process age, or a heuristic. The operator supplies the
   settlement decision; the substrate verifies only deterministic eligibility.
8. For a `stale` result, the lane's serialized settlement call SHALL verify all
   of the following and then perform the transition before releasing its
   mailbox: the session row exists, the session state is `active`, the target
   row belongs to that session, the target status is `running`, and `endedAt`
   is NULL. A nudge or task start that arrives during this call SHALL wait
   behind it and SHALL not create a live task in the probe-to-CAS window.
9. The transition SHALL be a compare-and-set on the exact target row. Its
   predicate SHALL include `seq`, `sessionKey`, `status='running'`,
   `endedAt IS NULL`, and the active-session condition. A zero-row CAS SHALL
   leave the row unchanged. The operation SHALL re-read the exact target and
   session in the same lane call and SHALL return existing terminal truth when
   the target is terminal, `session_retired` when the active-session predicate
   lost to retirement, `turn_not_found` when the target disappeared, or
   `turn_status_ambiguous` when the row cannot be classified without guessing.
10. The winning CAS SHALL append the existing `terminal_committed` lifecycle
    event in the same transaction. The event SHALL have outcome `canceled` or
    `failed`, cause exactly `operator:stale-running-turn`, and principal
    exactly the authenticated `user:<userId>`. The event SHALL not use the
    running turn's stale owner lease as operator authority.
11. The winning CAS SHALL publish the existing `turn.ended` durable effect in
    the same transaction. It SHALL not create a `stale` state, shadow turn,
    parallel settlement table, or replacement queue.
12. After commit, the operation SHALL release the session lane through the
    existing terminal callback and drain path. The lane SHALL claim the next
    queued turn only after the target is terminal. Queued turns SHALL remain
    queued and valid.
13. If no lane is currently registered but the session is active, the
    operation SHALL obtain the normal lane seam without sending a nudge, then
    execute the settlement call before any task-start message. Failure to
    obtain that seam SHALL be `turn_status_ambiguous`, not permission to mutate
    the ledger directly.
14. A successful response SHALL identify `sessionKey`, `turnSeq`, the terminal
    status, and whether this call won the CAS or replayed existing terminal
    truth. A denial SHALL identify a stable code from the eligibility and
    authorization vocabulary in Acceptance.
15. The request's `idempotencyKey` SHALL be 1–200 characters and SHALL be
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
16. The accepted and denied dispatch observations SHALL record the verb,
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
   concrete `SessionLane.settle_stale/3` synchronous call. The lane SHALL hold
   its mailbox serialization while the CAS transaction runs. A caller SHALL
   NOT sample lane state, release the call, and later perform a database
   update.
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

## Architecture

1. Add `settle-turn` to the closed `/agent/dispatch` verb set and to the CLI
   command mapping. The wire request SHALL put all selectors in `params`:
   `sessionKey`, `turnSeq`, `outcome`, `reason`, and `idempotencyKey`. The
   server SHALL derive the principal from authenticated admin identity.
2. Add a `SessionLane.settle_stale/3` synchronous call. Its handler SHALL
   inspect the exact target and its correlated provider request, refuse on
   `live` or `ambiguous`, and retain the lane mailbox callback while it invokes
   the guarded settlement transaction. A task cannot claim or start between
   that inspection and the CAS.
3. In the stale branch, use the existing terminal transition seam with an
   operator-authorized terminal event. The transaction SHALL combine the
   guarded target update, lifecycle append, `turn.ended` publication effect,
   and the `wire_idempotency` fingerprint/response write. It SHALL return the
   row's terminal result when another writer won.
4. After a winning commit, use the existing terminal callback, publication,
   and lane drain. If the response is lost after commit, the existing
   unpublished-terminal and pending-session reconciliation paths SHALL make
   the same result observable after restart.
5. Keep the current `cancel` handler and its lane-owned kill unchanged. A
   live task must use `cancel`; `settle-turn` is only for the proven absence of
   that task in the lane seam.
6. Expose the feature through the existing capability/version mechanism before
   a client sends it. An older server SHALL reject the closed verb as
   `unknown_verb`; an older client SHALL continue using existing verbs and
   statuses without schema failure.
7. Emit one accepted or denied dispatch observation per request and one
   `terminal_committed` lifecycle event only for a winning settlement. The
   observability record SHALL use a digest for the idempotency key and reason
   where the existing privacy boundary requires redaction.
8. Rollback is additive disablement: removing the handler or capability makes
   future requests return `unknown_verb` and leaves all already-terminal rows,
   lifecycle events, and publications intact. Rollback SHALL never reverse a
   terminal status or recreate a queued turn.
9. The source-lineage evidence SHALL pin the owned product clone at
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
6. **Eligibility refusal.** Given each of: absent session, retired session,
   absent turn, queued turn, delivered turn, canceled turn, failed turn, and
   failed-unknown turn, when the operator sends `settle-turn`, then the
   response is respectively `session_not_found`, `session_retired`,
   `turn_not_found`, or `turn_not_running` as applicable, and no new terminal
   event or queue change occurs.
7. **Authorization refusal.** Given a session principal, agent principal,
   process principal, non-admin user, or missing authentication, when the
   caller sends `settle-turn`, then the response is `not_authorized` and the
   target remains unchanged.
8. **CAS race.** Given one stale target and two concurrent settlement requests,
   when both reach the CAS, then exactly one changes the row and appends the
   lifecycle event; the loser returns the existing terminal truth and creates
   no event or publication. Given a runner completion races the operator, the
   same one-terminal rule decides the result. Given a queued successor sends a
   nudge while the lane settlement call holds its serialization, then the
   successor cannot claim before the target CAS commits; if a task is already
   current at the call boundary, the operator receives `turn_live` and the CAS
   does not run.
9. **Idempotent retry.** Given a committed settlement and a lost first
   response, when the same request is retried with the same idempotency key,
   then the response identifies the existing terminal truth and counts one
   lifecycle event, one terminal publication, and one queue release.
10. **Idempotency collision.** Given a principal and key already recorded for
    one target/outcome/reason fingerprint, when the same principal reuses that
    key with a different target, outcome, or reason, then the response is
    `idempotency_key_conflict` and the second target, lifecycle table, queue,
    and publication table remain unchanged. Given a different principal uses
    the same key, then the request has a separate scope and is evaluated only
    against its own target.
11. **Queue release.** Given one stale running target and one queued successor,
    when settlement commits, then the successor remains queued until the
    existing terminal callback/drain, then claims as the next turn. The
    settlement never deletes, cancels, or rewrites that successor.
12. **Restart before commit.** Given a process loss before the settlement CAS
    commits, when the gateway restarts, then existing boot recovery handles the
    still-running row as `failed_unknown` and the lost operator request does
    not reappear as a `canceled` or `failed` settlement.
13. **Restart after commit.** Given process loss after the settlement CAS but
    before the response or queue nudge, when the gateway restarts, then the
    existing unpublished-terminal and pending-session sweeps publish the
    committed terminal truth and drain the active session exactly once.
14. **Compatibility and rollback.** Given an older client or server, then the
    unsupported verb is rejected as `unknown_verb` and existing `cancel`,
    automatic adapter recovery, retired-session handling, and terminal statuses
    retain their current behavior. Given the new handler is disabled after a
    successful settlement, existing terminal rows remain terminal and no queue
    row is recreated.
15. **Observability.** Given one accepted request, one live refusal, one
    ambiguous refusal, and one authorization refusal, then each produces one
    stable dispatch observation with the target and principal, and only the
    accepted CAS produces the operator lifecycle event. No observation contains
    prompt text, credentials, or an unbounded reason.
16. **Source lineage and deterministic replay matrix.** Given the immutable
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
