# Escalation delivery — durable in-transaction wake — v1

Status: DRAFT r2

## Defect

Opening or retargeting a `decision_requests` row and notifying its responsible
party are one durable intent. They are currently split:

- `Tightbeam.Escalation.escalate/4` commits the request transaction, then invokes
  the optional `deliver_owner` callback (`lib/tightbeam/escalation.ex:167-217`).
  `Tightbeam.Gateway.escalation_context/3` constructs that callback and routes it
  through `notify_session/4` to `Gateway.deliver_prompt/4`
  (`lib/tightbeam/gateway.ex:760-773`).
- `Tightbeam.EffortCheckin.probe/3` and `deadline/3` commit their request
  insert/retarget transactions before calling `notify_expecter/3`
  (`lib/tightbeam/effort_checkin.ex:260-278`). `deliver_notification/2` then calls
  `Gateway.deliver_prompt/4` and converts every rescued exception and caught exit
  to `:ok` (`lib/tightbeam/effort_checkin.ex:899-929`).

A process death after either commit but before its callback leaves an open request
with no notification and no durable record that delivery is owed. The effort
rescue/catch also makes a live delivery failure indistinguishable from success.

On the statute side the callback is worse than fragile: it is dead. Nothing in
production calls `Gateway.escalation_context/3`, so no production context ever
carries `:deliver_owner` — `Dispatch` (`lib/tightbeam/dispatch.ex:112`) and
`Supervision` (`lib/tightbeam/supervision.ex:379`) both call
`Escalation.escalate/4` with a bare ctx. The owner doorbell therefore never fires
at all today; every statute escalation opens a decision request that notifies
nobody. That is task #23, and the outbox is its fix.

## Normative rule

Every notification created by opening or retargeting a decision request MUST be a
durable `wakes` row armed in the SAME database transaction as the corresponding
`decision_requests` insert or effort-expecter CAS update. This row is the
transactional outbox.

No escalation or effort-check-in path may invoke, return, carry, or schedule a
post-commit owner/expecter delivery callback. `deliver_owner`, `effort_notify`,
`notify_expecter/3`, and `deliver_notification/2` are not delivery seams.

For a newly inserted request, the winning insert arms exactly one notification
wake. An existing-request conflict or `{:decision_pending, id}` replay arms none.
For an effort deadline advance, the winning
`status='open' AND deadlineWakeId=<firing wake>` CAS arms exactly one notification
wake for the newly selected rung; a losing or replayed deadline fire arms none.

Each notification wake has:

- `consumer = 'prompt'`;
- `origin = 'process:tightbeam'`;
- `dueAt = now`;
- `targetGate = 0`;
- the same target and prompt content as the direct delivery it replaces;
- for effort notifications, the existing `assignmentId` carrier so delivery
  derives the same assignment/job attribution.

`targetGate` is an explicit wake-row delivery discriminator:

- `targetGate = 1` is the schema default and preserves the current active-session
  gate for existing nil-role prompt wakes;
- `targetGate = 0` means deliver to the recorded `sessionKey` without applying a
  target gate.

Decision notifications MUST set `targetGate = 0`. They deliver unconditionally,
including when the target session is held or retired between request commit and
wake fire. The direct deliveries being replaced omit `target_gate`
(`lib/tightbeam/effort_checkin.ex:919-924`,
`lib/tightbeam/gateway.ex:2180-2186`); adding an active-session gate would change
observable routing and is forbidden.

The prompt-wake closure in `Gateway.children_after_preflight/1` is shared by user,
role, bracket, and decision prompt wakes (`lib/tightbeam/gateway.ex:293-324`).
For its nil-role branch, it MUST pass `target_gate: nil` exactly when
`wake.target_gate == 0`, and `target_gate: wake` otherwise. Its role branch is
unchanged in target resolution. Both branches MUST pass the configured
`conn_registry` and `lane_manager`. Existing wake producers omit `targetGate`,
receive the default, and retain their current behavior.

Statute escalation targets `Org.personal_session_key(request.owner_user_id)`
(`lib/tightbeam/org.ex:606-613`). Effort notification targets
`request.expecter_session_key`, or
`Org.personal_session_key(request.expecter_user_id)` when the expecter is a user.
This is the existing wake-to-personal-session path.

The outbox row is deliverable and visible through the ordinary prompt consumer
(`lib/tightbeam/wakes.ex:320-344,501-531`). Delivery therefore moves from a
synchronous post-commit call to the next scheduler tick (at most
`config.wake_tick_ms`), which is inherent to making the intent durable.

## Invariants

1. **Atomic intent.** A new decision request and its initial notification wake
   either both commit or neither commits. An effort expecter/deadline rotation and
   its notification wake likewise either both commit or neither commits.
2. **One wake per routing event.** A request insert or effort-rung CAS winner arms
   one notification wake. Conflict, request replay, and stale deadline replay arm
   zero.
3. **Exactly-once durable prompt.** Wake execution is at-least-once. On ordinary
   decision-wake acceptance, message append, turn enqueue, and the pending-to-fired
   wake update commit in the SAME `Gateway.deliver_prompt/4` transaction because
   the shared closure passes `fire_wake_in_txn: true` for
   `origin='process:tightbeam'`
   (`lib/tightbeam/gateway.ex:316-321,833-855`). There is no production crash
   window between enqueue and fired-mark. `turns.wakeId UNIQUE`
   (`lib/tightbeam/ledger.ex:37-43`) is a backstop for synthetic inconsistent
   state or legacy residue: a pending wake whose turn already committed cannot
   commit a second turn. Exactly-once means one committed message/turn for the
   wake, not exactly-once socket publication.
4. **Committed delivery before fire.** A decision notification becomes fired only
   after its message/turn transaction has committed. Its first successful delivery
   atomically commits the message, turn, and fired-mark. A duplicate backstop path
   may mark a still-pending wake fired only after the existing committed turn is
   established by `turns.wakeId`. `:skipped` is unreachable because decision wakes
   carry `targetGate = 0` and the closure passes no target gate; the nil-gate
   resolver returns the recorded target unconditionally
   (`lib/tightbeam/gateway.ex:818-820,951-980`).
5. **Failure stays pending before durable acceptance.** Before a message/turn
   commits, a raise or exit through the scheduler delivery attempt leaves the wake
   `state='pending'` (`lib/tightbeam/wakes.ex:498-559`), visible through
   `Wakes.list_pending/1`, `Wakes.pending_count/2`, and direct inspection, and
   eligible for the next tick. The effort-specific rescue/catch-to-`:ok` is
   deleted.
6. **Dark-factory recovery.** Gateway boot includes `Tightbeam.Wakes`; scheduler
   initialization schedules its first tick, and the ordinary due-pending query
   selects every committed, due notification wake
   (`lib/tightbeam/gateway.ex:326-335`,
   `lib/tightbeam/wakes.ex:425-459,501-508`). Recovery requires no operator verb:
   restart plus the healed delivery dependency is sufficient.
7. **Configured delivery only.** The gateway prompt-wake closure passes the
   configured `conn_registry` and `lane_manager` to `Gateway.deliver_prompt/4`.
   Absent keys resolve to the same defaults already used by `notify_session/4`
   (`lib/tightbeam/gateway.ex:2180-2186`). Decision-request callers never construct
   or substitute delivery config.
8. **Delivery-only amendment.** Request identity, authorization, prompt text,
   origin, target selection, ruling behavior, evidence, and deadline timing are
   unchanged.

## Authority settlements

### Conformance ledger — “Escalation 6, 61, 105”

This specification supersedes only the entry's requirement for a post-commit
owner-user delivery callback. It obeys the entry's instruction to use the existing
wake-to-user path: the outbox row targets
`Org.personal_session_key(ownerUserId)`, and the ordinary configured prompt-wake
consumer delivers it. There is no separate post-commit callback seam. The required
end-to-end halt/open/one-owner-delivery/pending proof remains authoritative, with
delivery supplied by the outbox wake.

### `effort-without-effect-checkin-v1.md`

This specification supersedes §5's two post-commit best-effort-notify requirements
and restates its required proofs 6 and 8b:

- **Proof 6.** The request insert and its notification wake commit atomically. A
  crash after commit but before the notification is DELIVERED leaves the
  notification wake pending; ordinary wake recovery surfaces the request without
  waiting for the deadline wake.
- **Proof 8b.** A winning deadline-advance transaction commits the new rung,
  replacement deadline wake, and new-rung notification wake atomically. A crash
  after that commit but before the notification is DELIVERED leaves the
  notification wake pending; ordinary wake recovery surfaces the request. The old
  deadline wake still no-ops on `deadlineWakeId` mismatch, and authority rotates to
  the new rung.

These are strictly stronger than a best-effort notification backed only by a later
deadline: the notification intent itself is durable and remains pending until
delivered. The durable `effort_deadline` mechanism, expecter ladder, and the
remaining proofs stay authoritative.

Follow-up authority edits, outside this rewrite, MUST update:

- `conformance-handoff-ledger.md` to replace only the post-commit callback
  requirement with the transactional outbox while retaining its wake-to-user
  requirement;
- `effort-without-effect-checkin-v1.md` §5 and required proofs 6 and 8b with the
  outbox terms above.

Implementation plus the proofs below satisfies `gateway-split-v1.md` prerequisite
P0. The split may not preserve `Gateway.escalation_context/3` as a compatibility
surface.

### Task #23 configuration bypass

A hardcoded `%{}` or omitted configured delivery option at either request caller is
non-conforming. `Supervision.init/1` demonstrates the required propagation shape
by retaining `Keyword.take(opts, [:conn_registry, :lane_manager])` and using those
options at delivery (`lib/tightbeam/supervision.ex:159-168,820-830`).

Escalation and effort request callers perform no delivery. The shared prompt-wake
closure is constructed inside `Gateway.children_after_preflight/1`, where gateway
config is already in scope. Forwarding the two options affects user, role, bracket,
and decision prompt wakes alike, but absent keys resolve to the existing defaults;
there is no production behavior delta.

## Explicitly out of scope

- Routing and expecter selection are unchanged:
  `EffortCheckin.initial_expecter/2`, `advance_expecter/2`, and
  `route_session/5` keep their current lineage semantics; statute escalation keeps
  `ownerUserId` routing.
- The `consumer='effort_deadline'` wake, 24-hour deadline interval, rung advance,
  terminal-user re-arm, ruling cancellation, and deadline CAS are unchanged except
  that the winning request retarget transaction also arms its prompt notification
  wake.
- The check-in evidence payload and probe observation are unchanged. No
  direction/diff review is added.

## Required proofs

All proofs are automated and runnable with:

```sh
mix test test/escalation_delivery_test.exs
```

1. **Statute atomicity — fail-before/pass-after.** Install a temporary SQLite
   trigger that aborts only `INSERT INTO wakes` where `NEW.consumer='prompt'`;
   call `Escalation.escalate/4`; assert the call fails and neither the new
   `decision_requests` row nor a notification wake commits. Remove the trigger,
   retry, and assert one open request and one due pending prompt wake to
   `Org.personal_session_key(ownerUserId)`.
2. **Effort-open atomicity — fail-before/pass-after.** With the same prompt-only
   abort trigger, fire a zero-effect probe. Assert the request insert, generation
   transition, source-wake fire, deadline wake, and notification wake all roll
   back. Remove the trigger and assert one open effort request, its unchanged
   `effort_deadline` wake, and one due pending prompt wake to the initial expecter.
   Assert that wake carries the request's `assignmentId`, and that draining it
   produces a turn whose `assignmentId` and `jobRef` equal what the deleted explicit
   delivery opts carried — the `wake_attribution` seam
   (`lib/tightbeam/gateway.ex:893-916`) is the carrier that replaces them.
3. **Effort-retarget atomicity — fail-before/pass-after.** Abort prompt-wake insert
   while firing the current `effort_deadline`; assert the old expecter,
   `lineageRung`, `deadlineWakeId`, and pending deadline wake remain unchanged.
   Retry without the trigger and assert one CAS advance, one replacement deadline
   wake, and one prompt wake to the advanced expecter.
4. **Crash-before-delivery boot recovery — fail-before/pass-after.** Use a
   file-backed DB. Commit a request and due notification wake with the scheduler
   stopped, close the DB process, then restart the gateway DB and the exact
   `Tightbeam.Wakes` child options returned by
   `Gateway.children_after_preflight/1`. Without calling `Wakes.fire_due/1` or any
   operator verb, assert the boot tick creates the turn carrying that wake's
   `wakeId` and the wake becomes fired.
5. **Failure remains observable — fail-before/pass-after.** Run a due notification
   through a prompt-delivery function that raises and one that exits before durable
   acceptance. After each attempt assert no fired transition, the wake remains in
   `Wakes.list_pending/1`, and `Wakes.pending_count/2` includes it. Restart with a
   healthy delivery function and assert the ordinary tick delivers it.
6. **Exactly one initial delivery and dedupe backstop —
   fail-before/pass-after.** Open one request and assert one notification wake and
   an ordinary drain atomically commits its message, turn, and fired-mark.
   Separately construct the otherwise-unreachable legacy/synthetic state by
   committing `Gateway.deliver_prompt(..., wake_id: wake.wake_id)` while leaving
   the wake pending; restart/drain the scheduler. Assert exactly one projection
   message and one `turns` row for that `wakeId`, then assert the wake is fired.
7. **Decision replay is silent — fail-before/pass-after.** After one request has
   returned `{:decision_pending, id}`, replay the same decision-pending path with
   that id. Assert notification-wake, message, and turn counts are unchanged.
   Repeat through the open-request conflict path; it is silent too.
8. **Effort ladder conservation — fail-before/pass-after.** Expire successive
   `effort_deadline` wakes across a live ancestor, a skipped held/retired ancestor,
   and the terminal owner-user rung. At every expiry assert the same
   `initial_expecter`/`advance_expecter`/`route_session` result, a fresh full
   deadline interval, exactly one replacement internal deadline wake, and exactly
   one prompt wake to that rung. At the terminal user rung, assert expiry re-arms
   against the same user as before.
9. **Injected delivery dependencies — fail-before/pass-after.** Start non-default,
   uniquely named `ConnRegistry` and lane-manager processes; place both names in
   gateway config; obtain and start the real gateway `Tightbeam.Wakes` child; open
   and deliver one statute request and one effort request. Assert publication
   reaches only the injected registry and lane nudges reach only the injected lane
   manager. The test MUST fail if either option is replaced by `%{}`, omitted, or
   defaulted.
10. **Closure law — fail-before/pass-after.** A source-closure test maintains an
    explicit allowlist of every production `decision_requests` insert/retarget
    site: `Escalation.escalate/4`
    (`lib/tightbeam/escalation.ex:167-215`),
    `EffortCheckin.open_request_in_txn/4`
    (`lib/tightbeam/effort_checkin.ex:564-628`), and
    `EffortCheckin.deadline_in_txn/3`
    (`lib/tightbeam/effort_checkin.ex:425-492`). It fails if a new site appears
    without an in-transaction `consumer='prompt'` arm.

    Repo-wide production AST allowlists cover every turn-bearing delivery sink:

    - `Gateway.deliver_prompt/4`: the prompt-wake role and nil-role branches
      (`lib/tightbeam/gateway.ex:298,316`), the `post` handler
      (`lib/tightbeam/gateway.ex:502`), `notify_session/4`
      (`lib/tightbeam/gateway.ex:2181`), and supervision recovery
      (`lib/tightbeam/supervision.ex:820`);
    - `notify_session/4`: the override-removal notification
      (`lib/tightbeam/gateway.ex:3082`);
    - `Gateway.deliver_prompt_in_txn/5`: assignment dispatch
      (`lib/tightbeam/assignments.ex:548`), condition/fallback wake fire
      (`lib/tightbeam/wakes.ex:750`), the `deliver_prompt/4` wrapper
      (`lib/tightbeam/gateway.ex:788`), and adjudication delivery
      (`lib/tightbeam/gateway.ex:3554,3620,3798,3925`);
    - `Ledger.enqueue_in_txn/2`: the delivery core
      (`lib/tightbeam/gateway.ex:837`) and the `Ledger.enqueue/2` wrapper
      (`lib/tightbeam/ledger.ex:139`);
    - `Ledger.enqueue/2`: zero production call sites.

    This set is complete because every committed turn reaches
    `Ledger.enqueue_in_txn/2`; the only production caller outside its own wrapper is
    `Gateway.deliver_prompt_in_txn/5`, whose wrapper and direct callers are all
    enumerated. A path that drops below delivery to
    `Projection.append_in_txn/2` plus `Ledger.enqueue_in_txn/2` therefore still
    creates a new closed-sink call site. The AST allowlists are also backed by a
    raw-SQL assertion: `insert into turns` — matched case-, whitespace- and
    identifier-quoting-insensitively, so `"turns"`, `[turns]` and a backticked
    name are all caught — appears in production code only in
    `lib/tightbeam/ledger.ex`, so a hand-written turn insert cannot step around
    the enumerated sinks. Any new call site fails.

    The closure law states its own boundary, and the two SQL scans do not read the
    same thing. The turn-insert scan greps each production file's ENTIRE SOURCE
    TEXT, so it sees the phrase wherever written — including in a comment, a false
    positive it accepts rather than parsing to exclude. The decision-request scan
    walks the AST and inspects individual string LITERALS.

    Neither catches SQL whose table name is assembled at runtime: a concatenated
    or interpolated name leaves the phrase nowhere adjacent to be found. Folding
    arbitrary concatenation is not attempted — it is unbounded, and a writer
    concatenating SQL to slip past a named guard is evading review, which no test
    prevents. The law is a floor against drift, not a sandbox against intent, and
    its completeness is not iterated further: a further hole is documented here
    rather than chased.

    The test also asserts `Escalation` and `EffortCheckin` contain no indirect
    function invocation and production contains no `deliver_owner`,
    `effort_notify`, `notify_expecter`, `deliver_notification`, or
    `Gateway.escalation_context/3`.
11. **Retired target is still delivered — fail-before/pass-after.** Open a statute
    request and an effort request, retire or otherwise make each recorded target
    non-active before its notification wake fires, then drain the real scheduler.
    Assert each message and turn commits to the recorded target, each wake becomes
    fired only with that committed turn, and no `:skipped` or
    fired-with-nothing-committed outcome exists. A control prompt wake with the
    default `targetGate = 1` MUST retain the existing active-session gate.

## Component touches

- `lib/tightbeam/escalation.ex`
  - `Escalation.escalate/4`: arm the owner prompt wake inside the winning request
    transaction.
  - `Escalation.deliver_owner/2`: delete. It is private at
    `lib/tightbeam/escalation.ex:1033`; its only production invocation is the
    post-commit path at line 217.
- `lib/tightbeam/effort_checkin.ex`
  - `probe/3` and `deadline/3`: remove post-commit notification steps.
  - `open_request_in_txn/4`: arm the initial-expecter prompt wake after the winning
    insert, inside the existing transaction.
  - `deadline_in_txn/3`: arm the new-rung prompt wake inside the winning retarget
    transaction.
  - `notify_expecter/3` and `deliver_notification/2`: delete. They are private at
    lines 899 and 909; their only production invocations are the post-commit path
    being replaced. Delete the rescue/catch swallow and `effort_notify` config
    seam.
- `lib/tightbeam/wakes.ex`
  - Add the `targetGate` wake column/map field with schema default `1`; preserve it
    through schema ensure/rebuild and row decoding.
  - `schedule_in_txn/2` writes the column: its INSERT column list and value tuple
    (`lib/tightbeam/wakes.ex:212-217`) MUST gain `targetGate`, taking `0` from the
    caller's option and the schema default `1` otherwise. Without this encoding
    step every wake silently defaults to gated and the retired-target proof cannot
    pass.
- `lib/tightbeam/gateway.ex`
  - Delete public `Gateway.escalation_context/3` at line 762. It has zero callers
    in production or tests.
  - In the shared prompt-wake closure, use `targetGate` to omit `target_gate` only
    for decision wakes, retain the gate for every existing nil-role wake, retain
    role behavior, and forward configured `conn_registry` and `lane_manager` in
    both branches.
  - `notify_session/4` remains for its unrelated caller.
- `test/effort_checkin_test.exs`
  - RECONCILE the proof-6/8b test at line 734: replace `effort_notify` crash/callback
    assertions at lines 738 and 752 with assertions that the request and its
    notification wake commit together, the wake stays pending until delivery, boot
    recovery surfaces it, and stale deadline replay remains silent. Do not delete
    the test.
- `test/gateway_test.exs`
  - RECONCILE the gateway effort-consumer test at line 1267: remove its
    `effort_notify` seam at line 1273 and assert the real durable prompt wake and
    configured delivery path. Do not delete the test.
- `test/escalation_test.exs`
  - RECONCILE the owner-delivery test at line 137: replace the `deliver_owner`
    callback assertions at lines 150 and 160 with one durable wake on the winning
    insert, delivery only after commit, and no wake on replay. Do not delete the
    test.
- `test/escalation_delivery_test.exs`
  - Own the eleven runnable proofs above.

## Implementation handoff

Change only the delivery mechanism, the `targetGate` discriminator, and the named
configuration propagation. Reuse `Wakes.schedule_in_txn/2`, the existing prompt
consumer, `Gateway.deliver_prompt/4`, and `turns.wakeId` dedupe. Do not add a second
scheduler, delivery worker, retry state, operator recovery verb, routing fallback,
or callback compatibility layer.
