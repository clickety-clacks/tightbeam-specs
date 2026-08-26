# Urgency-aware notice batching — v1

Status: DRAFT

Work item: `wi_1100e078-2479-4d1b-8549-d65f7a82fd3d`

Authority: the work item and its surrendered predecessor
`asg_d107120d-4e03-4159-8451-f82b0dc943e7`; Mike's later correction recorded
in `att_606787da-55b1-418c-839e-05cb25f72599`; and
`coordination-fabric-v1.md` at `09d4118dc6b651f0d1468a723a4d7a7afa8ca045`,
§§5, 7, and 13. The correction controls the ownership conflict in §13: this
work item has its own landing. Exec desks may consume a delivered batch
envelope; they do not block, own, or absorb this mechanism.

## Goal

The substrate reduces needless agent turns by delivering eligible pending
non-user notices for one recipient in one source-preserving envelope. It keeps
each source notice as a durable row, applies the current class urgency policy
before batching, and creates the envelope by the earlier of the recipient's
next turn boundary and that policy's delivery ceiling.

The mechanism is delivery physics. It does not decide notice importance,
change a notice class, infer a recipient, alter work state, or require a
decision to release a batch.

## Non-Goals

- This v1 does not batch a user-authored message.
- This v1 does not batch `algedonic` traffic. That traffic follows the immediate
  bypass defined by `coordination-fabric-v1.md` §7.
- This v1 does not change the class policy for `fyi`, `status-query`,
  `input-needed`, or `blocker`; it consumes the target and due time that the
  policy already selected.
- This v1 does not classify, summarize, annotate, answer, triage, escalate, or
  judge notice content. Exec-desk policy owns those cognitive acts.
- This v1 does not replace recurrence suppression, prod suppression, wake
  delivery, cancellation law, or the existing target-resolution path.
- This v1 introduces no human notification, user-facing control, new role,
  desk, hold, release target, or 0.1.x change.
- This v1 does not coalesce payloads into a count or a summary. A later
  coalescer may choose that behavior under separate authority.

## Terms

- **Source notice** — the durable substrate row that records one non-user
  notification before this mechanism considers delivery. Its row identifier,
  sender principal, cause, recipient address, class election, payload, and
  authorization context remain authoritative.
- **Dispatchable notice** — a source notice for which the existing class policy
  has selected a recipient delivery. A `status-query` that class policy routes
  to a rows-only answer is not dispatchable to a principal.
- **Recipient address** — the exact target form selected by existing policy:
  session, role, or user. Role addresses retain the existing send-time
  resolution rule; this mechanism does not substitute a session.
- **Visibility scope** — the recipient principal and authorization scope that
  authorize access to a source notice's payload.
- **Urgency lane** — a policy-provided delivery lane with one due time. Two
  notices share a lane only when they have the same recipient address,
  visibility scope, and due-time policy. A routine `fyi` notice therefore
  cannot delay an `input-needed` or `blocker` notice.
- **Batch** — a durable delivery envelope for one urgency lane. It contains an
  ordered, immutable list of member references after sealing. It is not a
  source notice and it does not replace any source row.
- **Member** — the durable link from one source notice to one batch. It records
  the source row id, immutable per-recipient publication sequence, policy
  revision, cause, sender principal, and inclusion state.
- **Turn boundary** — the observable transition at which the recipient has no
  running turn. This mechanism observes that transition and seals an open batch
  without guessing from elapsed time.
- **Delivery ceiling** — the latest time at which the current class policy
  requires a delivery wake to be created. The fabric currently gives `fyi` a
  four-hour ceiling and `input-needed` or `blocker` the prodder floor. This spec
  does not set those policy values.
- **Delivery token** — the deterministic token derived from a batch id. The
  wake/turn delivery path uses it as the idempotency key for that batch.

## Assumptions

1. The existing notice publisher can make a source notice durable before it
   calls the batch mutation seam.
2. The current wake pipeline accepts an idempotency key that prevents a retry
   from committing a second recipient turn for the same delivery token.
3. The current class policy can provide a dispatchable recipient address and a
   delivery ceiling without inspecting batch state.
4. A recipient turn terminal event is observable. If it is not observed, the
   ceiling timer remains the deterministic release path.
5. The deployment can store a batch with at least 50 member references and a
   rendered envelope of at least 64 KiB. A deployment that cannot meet either
   floor must leave batching disabled rather than truncate a source payload.

## Invariants

1. **Source conservation.** The mechanism creates no batch member before its
   source notice row exists. It never edits or deletes that row. Each included
   member exposes the source row id, sender principal, cause, class, and
   payload in recipient-authorized form.
2. **Urgency preservation.** Existing class policy decides whether a notice is
   dispatchable, its recipient address, its visibility scope, and its ceiling.
   Batching cannot make a notice less urgent, move it to another recipient, or
   create a delivery later than its lane's ceiling.
3. **One mutable seam.** `NoticeBatcher.enqueue_or_recover` is the sole mutation
   seam for batch, member, schedule, retry, cancellation, and recovery state.
   It performs each change in one database transaction.
4. **One member per source delivery.** A unique key on
   `(source_notice_id, recipient_address, visibility_scope)` permits one member
   for one source delivery. A retry returns that member and its batch; it adds
   no duplicate member.
5. **One admitted turn per batch.** A sealed batch has one delivery token. The
   scheduler may retry that token after a crash or failure, but it may commit
   only one envelope message and one recipient turn for that token.
6. **Immutable sealing.** Sealing assigns members their ascending publication
   sequence and freezes the member list and rendered member records. A source
   notice that arrives after sealing joins a later batch.
7. **No decision hold.** An open batch seals on a turn boundary or its ceiling.
   A running recipient turn may delay carrier admission under existing turn
   rules, but it cannot postpone creation of the delivery wake past the ceiling.
8. **Visibility isolation.** A batch accepts members from one recipient address
   and one visibility scope. The envelope reveals no payload or reference that
   the recipient could not read from the corresponding source row.
9. **Mechanical composition.** An exec desk receives a batch only through the
   ordinary recipient delivery path. It may read its members and apply its own
   policy after delivery. Its state, directive, availability, or judgment cannot
   prevent, merge, split, or reclassify a batch before the delivery path acts.
10. **Independent suppression.** Recurrence suppression runs before a source is
    dispatchable. This mechanism consumes a dispatchable source row only. It
    does not compute recurrence identity, rearm a recurrence, or convert a
    recurrence audit event into a member. Prod suppression remains responsible
    for duplicate triggered turns; batching never reads or writes prod counters,
    trigger state, or prod identity.
11. **Legible edges.** Each batch state transition records the cause and acting
    principal. Source, member, batch, delivery wake, turn, failure, cancellation,
    and retry references are queryable from either source or batch id.

## Architecture

### 1. Eligibility and recipient correlation

The existing publisher first authenticates the sender, writes the source notice,
and applies current class policy. It calls `NoticeBatcher.enqueue_or_recover`
only for a dispatchable non-user notice whose class is not `algedonic`.

The call receives the source row id, recipient address, visibility scope, class
policy revision, and ceiling selected by policy. It rejects a caller-supplied
recipient, ceiling, class, sender, cause, or visibility scope. The source row
remains the authority for those values.

The seam constructs an urgency-lane key from the recipient address, visibility
scope, and policy-provided due-time policy. It never mixes two address forms or
two visibility scopes. A role-addressed batch remains role-addressed through
delivery, so existing role rebinding and fallback behavior remain controlling.

### 2. Accumulation, ordering, and fairness

In one transaction, the seam assigns the next monotonically increasing
publication sequence for the urgency lane, inserts or reuses the unique member,
and attaches that member to the one open batch for the lane. When it creates the
first member, it stores both release triggers: the next observable recipient turn
boundary and the class-policy ceiling.

The scheduler seals the batch when either trigger wins. The check for a terminal
turn event and the seal transition occur in the same transaction. The scheduler
creates a due delivery wake in that transaction when the ceiling wins. It never
uses a duration as a proxy for a turn boundary.

Members appear in the envelope by publication sequence, not timestamp. This
makes ties and clock skew deterministic. A batch contains at most 50 members or
64 KiB of rendered member records. When the next member would exceed either
limit, the seam seals the current batch in the insertion transaction, starts the
next batch, and places the new member there. The sealed batch remains due under
its original triggers. This bounded-prefix rule prevents an unbounded flood from
starving later notices while preserving each lane's order.

### 3. Envelope and delivery

When a batch seals, the mechanism creates an immutable envelope with the batch
id, delivery token, recipient address, policy revision, release cause, ordered
member records, and a signed provenance record. Each member record includes the
source row id, sender principal, cause, class, publication sequence, and the
source payload as authorized for that recipient. The envelope may add a header
that names the batch size; it may not omit or rewrite a member payload.

The ordinary wake pipeline delivers the envelope using the batch delivery token.
It resolves the stored recipient address through its existing rules. A delivered
envelope therefore becomes one agent turn containing the complete ordered member
set. If the address cannot resolve, ordinary wake delivery records its existing
terminal result; the batcher does not pick a substitute recipient.

The batcher does not inspect whether the recipient is an exec desk. A desk sees
the envelope as ordinary inbound material. It may then exercise only the
authority of its own delegation card and policy. This feature's scope ends at
committing the ordinary delivery carrier.

### 4. Failures, retries, and crash recovery

The batch states are `open`, `sealed`, `delivery_pending`, `delivered`,
`delivery_failed`, and `canceled`. `enqueue_or_recover` owns each transition.
`delivered`, `delivery_failed`, and `canceled` are terminal. The terminal row
names its cause and principal.

After sealing, the seam writes the delivery wake and token before it marks the
batch `delivery_pending`. A transaction failure rolls back both changes. A
delivery attempt that fails before the wake/turn path commits leaves the batch
`delivery_pending`, leaves the wake pending under ordinary wake law, and records
the typed attempt failure. Recovery retries the same token; it does not rebuild
or duplicate the envelope.

On boot, recovery scans `open` batches for expired ceilings, `sealed` batches
without a wake, and `delivery_pending` batches without a terminal delivery. It
runs the same mutation seam. For each row it either completes the missing durable
edge or reads its existing idempotent edge. It never reconstructs a batch from
payload text, changes member order, or creates a second member.

### 5. Late arrival and cancellation

A source notice that reaches the seam after its lane's batch has sealed receives
the next publication sequence and joins a new open batch. It cannot mutate the
sealed envelope.

An authorized source-cancellation transition races the member-seal transition
through the same mutation seam. If cancellation wins before sealing, the seam
marks the member `canceled`, records the source cancellation reference, and
excludes it from the envelope. If sealing wins, the source cancellation remains
recorded on the source row and does not rewrite the immutable envelope. A source
notice with no active members leaves no empty batch wake; an open empty batch is
marked `canceled` with its cause and principal.

Only the authenticated source cancellation authority may request this path. The
batcher applies the existing authorization result; it does not add a new
cancellation authority.

### 6. Interfaces, authorization, and observability

The internal write interface is:

```text
enqueue_or_recover(source_notice_id, policy_delivery_ref) ->
  {member_id, batch_id, state}
```

`policy_delivery_ref` is an opaque reference to the existing policy decision.
The seam resolves authoritative recipient, class, ceiling, sender, cause, and
visibility data from durable rows. A stale, unauthorized, missing, non-user, or
`algedonic` source returns a typed refusal and creates no batch state.

The internal delivery interface is:

```text
deliver_batch(batch_id, delivery_token) -> existing_wake_or_terminal_result
```

It accepts only the stored token. A repeated call returns the same durable wake
or terminal result. No new public CLI verb or wire message is part of v1. Existing
authorized source and wake reads gain batch references. A batch read applies the
same recipient and source-row visibility checks to every member; a caller who
lacks access to any member receives no batch payload.

The system records `batch_opened`, `member_added`, `batch_sealed`,
`delivery_armed`, `delivery_attempted`, `delivery_delivered`,
`delivery_failed`, `member_canceled`, and `batch_canceled` lifecycle events.
Each event records batch id, member id when applicable, source row id, cause,
principal, and related wake or turn id. Derived queries report member count,
age to seal, age to carrier admission, release cause, retry count, overflow
count, terminal result, and source-to-batch-to-turn lineage. Payload text is not
included in aggregate metrics or logs.

### 7. Compatibility, migration, and rollback

Batching is disabled by default until an org policy selects it for a recipient
lane. While disabled, the publisher uses the existing one-notice delivery path
unchanged. Existing notices receive no retrospective member or batch row.

Migration adds batch and member tables, unique keys, lifecycle event kinds, and
read projections. It preserves every existing source notice, wake, message, turn,
authorization record, and terminal result without reinterpretation.

Rollback first disables admission of new members. It leaves sealed and
`delivery_pending` batches on the versioned ordinary wake path until a durable
terminal result exists. An operator may then remove the feature only after the
batch queries show zero open, sealed, and delivery-pending batches. This avoids
turn loss and avoids replaying a source through the legacy path.

## Acceptance

Each acceptance check is a deterministic automated fixture against a file-backed
database and the ordinary wake/turn delivery test seam.

1. **Routine envelope.** Given two dispatchable non-user `fyi` source rows with
   the same recipient address and visibility scope, when both enter an open lane,
   then the turn-boundary seal creates one envelope with two ordered member records
   and commits one recipient turn with both original payloads and source ids.
2. **User exclusion.** Given a user-authored message with the same recipient as
   an open batch, when it reaches publication, then no member references that
   message and the existing user-message delivery path receives it.
3. **Algedonic bypass.** Given an `algedonic` source row and an open routine
   batch, when the source reaches publication, then the source follows the
   immediate bypass path and the routine batch has no new member.
4. **Urgency separation.** Given an open `fyi` batch and a dispatchable blocker
   for the same recipient, when the blocker enters the seam, then it receives a
   separate urgency lane whose delivery wake is armed no later than the blocker
   ceiling; the `fyi` batch remains unchanged.
5. **Policy no-delivery.** Given a `status-query` that current policy resolves
   without a principal delivery, when its source row is published, then the
   batch tables contain no member or batch row for that source.
6. **Ceiling release.** Given an open routine batch whose recipient has no turn
   boundary before the stored ceiling, when the ceiling becomes due, then one
   transaction seals the batch and arms its delivery wake. The fixture asserts
   that no decision row or desk state participates in that transition.
7. **Boundary release.** Given an open batch and a recipient terminal-turn
   event before its ceiling, when the scheduler processes that event, then it
   seals the batch once and creates the ordinary delivery carrier before the
   ceiling.
8. **Atomic boundary race.** Given one terminal-turn event and one concurrent
   member insertion, when their transactions race, then the fixture finds the
   member in exactly one immutable batch and finds no delivery wake whose member
   set depends on an out-of-transaction observation.
9. **Stable order.** Given three source rows inserted with equal timestamps in
   publication-sequence order, when their batch seals, then the envelope lists
   their source ids in that sequence.
10. **Bounded prefix.** Given 51 equal-scope eligible notices, when they enter
    an empty lane, then the first sealed batch has 50 members, the remaining
    source is the first member of a later batch, and both batches retain order.
11. **Payload limit.** Given a candidate member that would make rendered member
    records exceed 64 KiB, when it enters a nonempty batch, then the prior batch
    seals without truncation and the candidate appears intact in the next batch.
12. **Publish replay.** Given the same source delivery is submitted twice, when
    the seam processes both requests, then both responses identify one member and
    one batch and the envelope contains that source once.
13. **Crash recovery before arm.** Given a process stop after a batch seals but
    before its wake persists, when the database restarts, then recovery arms one
    wake with the stored token and retains the sealed member set.
14. **Delivery retry.** Given a delivery attempt that fails before a wake/turn
    commit, when the scheduler retries after restart, then the same token creates
    one turn and the batch records the failed attempt and the later delivery.
15. **Post-commit replay.** Given a committed wake and turn for a batch whose
    batch state remains `delivery_pending` in a synthetic crash fixture, when
    recovery runs, then it marks the existing delivery terminal and commits no
    second wake, message, or turn.
16. **Late arrival.** Given a sealed batch, when another eligible source reaches
    the same lane, then the sealed envelope stays byte-identical and the source
    appears once in a new batch.
17. **Cancellation race.** Given a member and concurrent source cancellation and
    seal actions, when cancellation wins, then the member is excluded with its
    cancellation reference; when sealing wins, then the envelope stays immutable
    and the source cancellation remains separately recorded.
18. **Authorization and privacy.** Given two source rows with different
    visibility scopes for the same role address, when they enter the seam, then
    they produce separate batches; a caller authorized for only one source cannot
    read the other source or a combined envelope.
19. **Exec-desk composition.** Given a recipient address that resolves to an
    exec desk and a ready batch, when the carrier delivers, then the batcher
    commits its ordinary delivery without reading the desk card, directives, or
    availability. The desk receives the envelope as inbound material.
20. **Suppression separation.** Given a recurrence audit row that has no
    dispatchable source notice and a prod state with a triggered turn in flight,
    when the batcher runs, then it creates no member from the audit row and makes
    no write to recurrence identity, rearm fields, prod counters, trigger state,
    or turn-accounting rows.
21. **Migration and rollback.** Given pre-migration notices and one
    post-migration sealed batch, when migration completes and rollback disables
    new admission, then pre-migration notices gain no batch rows, the sealed
    batch reaches one terminal outcome through its stored wake, and no source
    replays through legacy delivery.

## Open Questions

None. V1 fixes the bounded member and rendered-payload floors in Assumption 5 to
make overflow behavior testable. A later policy extraction may replace those
constants after evidence from this feature's observability queries; it must
preserve the no-truncation and bounded-prefix invariants.
