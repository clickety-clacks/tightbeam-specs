# Effort pseudo-decision cleanup

## Decision

Do not add a second stalled-work analyzer. Current `main` already has the
required prodder behavior. The smallest remaining change is a one-time,
idempotent conversion of any *proven legacy effort row* during an upgrade.
It must never select a row by its question text, its owner, or a generic
`operator` kind.

The conversion does not make a decision for an operator. It ends the obsolete
automated decision carrier and hands its still-open assignment back to the
current prodder path.

## Verified behavior

Commit `7f0e2e0` on the current-main ancestry removed
`EffortCheckin.open_request_in_txn/4`. After a zero-effect probe, the code now
does the following:

1. sends one holder prod;
2. on continued silence, sends an `[effort escalation]` wake to the next active
   operational parent;
3. re-arms the monitor until Main is reached; and
4. stops at Main without creating a decision row.

`test/effort_checkin_test.exs` proves the parent wake and asserts zero
`decision_requests` rows for that stalled assignment. The production module
states the same boundary: it reports inactivity to agents and never
manufactures an operator decision.

The live read on 2026-08-24 also found no current automated candidate: exact
matching of the historic `["continue", "dismiss"]` menu returned an empty
set. The 25 open live rows are legacy `operator` requests with real questions;
this design deliberately leaves them untouched.

## Exact conversion boundary

A row is eligible only when all of the following are true:

- `kind = 'effort'`;
- `raiserId = 'process:tightbeam'`;
- it has a valid `assignmentId`, `effortGeneration`, and `deadlineWakeId`; and
- it satisfies the existing effort-arm schema constraints.

This is a typed historical shape, not a content classifier. `operator`,
`agent`, and `statute` rows are never candidates. In particular, an operator
request remains open until its operator rules or withdraws it.

## Smallest implementation slice

Add one boot/upgrade transaction owned by `Escalation`, where the
`decision_requests` table already has its single writer boundary. Its input is
the typed set above.

For every eligible **open** row, atomically:

1. re-enter the current effort-checkin parent-escalation path for its still-open
   assignment, using the durable generation and current operational-parent
   chain;
2. create the resulting parent wake and replacement monitor before any old
   carrier is terminalized;
3. cancel the legacy `deadlineWakeId` with a typed `superseded` disposition;
   and
4. set the old row to `superseded`.

The order prevents the cleanup from silently losing the stalled assignment.
If the assignment is already terminal, no replacement is needed: cancel the
pending deadline and supersede the effort row in the same transaction.

For an eligible **ruled** row, set `status = 'consumed'` only after confirming
the original ruling transaction completed its existing generation effect. The
old `continue` and `dismiss` paths already make that effect in the ruling
transaction, so this is a historical terminalization, not a new judgment.

Leave already `superseded`, `withdrawn`, and `consumed` effort rows unchanged.
The conversion must be restart-safe: every update is status-CAS guarded and
every replacement is keyed to the old request id, so a retry neither emits a
second parent wake nor changes a genuine request.

No query filter is required for current behavior. Once open effort rows are
terminalized, the ordinary open owner queue contains only real decision
requests; `--status all` continues to show legacy rows as history.

## Acceptance evidence

- A new zero-effect stall produces holder and parent/Main wakes and zero effort
  decision rows.
- Seeded open legacy effort row: one parent handoff and one typed cancellation;
  its row becomes `superseded`; a restart is a no-op.
- Seeded ruled legacy effort row whose ruling effect exists: it becomes
  `consumed`; a restart is a no-op.
- Seeded open legacy `operator`, current `agent`, and `statute` rows survive
  byte-for-byte and remain visible to their proper readers.
- A legacy effort row whose assignment is terminal produces no replacement
  monitor and has a typed terminal cancellation.

## Non-goals

- Do not classify questions by wording or options.
- Do not close, consume, or hide genuine operator requests.
- Do not change the prodder's observation channels, thresholds, parent chain,
  or Main boundary.
- Do not deploy this design until an implementation card and review establish
  the exact legacy-schema upgrade route.
