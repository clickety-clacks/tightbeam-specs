# Deterministic breathing query v1 — session, assignment, and work item

Status: draft spec candidate for `wi_4ef0bb82-7d16-4ddd-acff-54fbb516e80f`.
This file specifies a read-only contract on both supported product lines,
`0.1.9` and `main`/`0.2`. It does not authorize implementation.

This spec is a bounded amendment to these authorities:

| Existing authority | Clause amended by this spec |
|---|---|
| `cli-surface-v1.md` | The agent-facing surface gains one read-only `breathing` family with identical output on both supported lines. |
| `observability-v1.md` | Assignment `status` remains a separate view concern. It is not breathing, and no observability status value answers breathing by implication. |
| `standing-accountability-lifecycle.md` | Reaffirmation, progress, and continuation remain standing-accountability receipts only. They do not establish breathing. |
| `patrol-response-acknowledgment.md` | Patrol acknowledgments remain episode receipts only. They do not establish breathing. |

Background, not authority: `wi_a57dee58-7dc6-43e4-b36d-a45959e64ad6`,
`wi_0c1ad73a-e18b-4661-9cb9-a62324703c47`,
`wi_bcb85145-ca2e-49d9-b440-3acc19234709`, the superseded physical-liveness
verdict on `wi_990f7b7e-837b-4aba-8f2e-ac6617327d78`, and the 0.2 sweep
entries on supervision truth and bounded watchdog inference.

## Goal

G1. Tightbeam answers the physical question “is this target still breathing?”
for exactly three target kinds: session, assignment, and work item.

G2. The breathing answer is a deterministic query over durable product rows.
The same target and the same snapshot yield the same answer on both supported
product lines.

G3. When the target is not breathing, the same query returns one exact reason
from a closed vocabulary and the deciding evidence rows, so the caller does
not need a second forensic query.

G4. No recorded fact, attestation, work-item update, verdict, artifact,
message, condition fact, acknowledgment row, or event log line has authority
to declare breathing. Breathing is computed at query time and stored nowhere.

G5. Pacing remains row-based schedule. Pending wakes and queued or running
turns can prove a current execution path only after the target-specific
existence and state gates in AR2, AR3, or AR4 pass. They do not claim
semantic progress.

## Non-Goals

NG1. This MVP does not decide whether work is advancing, correct, useful, or
complete. Advancement remains semantic and attested.

NG2. This MVP does not change assignment status, work-item state, supervision
policy, prod limits, escalation policy, or standing-accountability policy.

NG3. This MVP does not add a breathing table, breathing event stream,
breathing condition fact, breathing watermark, or background sweeper.

NG4. This MVP does not classify intent from prose, prompt text, artifact
content, message content, or attestation text.

NG5. This MVP does not infer adapter death, harness health, or provider
policy beyond what the selected deciding rows say exactly. Raw turn error text
may appear in evidence; inferred cause labels shall not.

NG6. This MVP does not backfill historical rows or reinterpret old rows as a
stored breathing state.

NG7. This MVP specifies the CLI contract but does not implement the query or
land code on either product line.

## Terms

### T1 — Breathing

A target is **breathing** when the current durable snapshot proves at least one
current substrate path for that target to execute or be driven onward after
the target passes its target-specific existence and state gates in AR2, AR3,
or AR4. In this MVP, only these current-path rows can prove breathing after
those gates pass:

- a `turns` row with `status = 'running'`;
- a `turns` row with `status = 'queued'`; or
- a `wakes` row with `state = 'pending'`.

No other row kind proves breathing, and a row excluded by a target-specific
gate is not current-path evidence for that target.

### T2 — Physical evidence set

The **physical evidence set** for this spec is limited to these durable product
rows and fields:

- `sessions.state`;
- `assignments.id`, `assignments.openedAt`, `assignments.state`,
  `assignments.outcome`, `assignments.holderKey`, `assignments.workItemId`;
- `work_items.state`, `work_items.failReason`;
- `turns.seq`, `turns.sessionKey`, `turns.assignmentId`, `turns.jobRef`,
  `turns.status`, `turns.adapterGen`, `turns.error`, `turns.createdAt`,
  `turns.startedAt`, `turns.endedAt`;
- `wakes.wakeId`, `wakes.sessionKey`, `wakes.assignmentId`,
  `wakes.work_item_id`, `wakes.state`, `wakes.dueAt`, `wakes.createdAt`.

### T3 — Current path precedence

For one target snapshot, current-path evidence is selected in this exact
precedence order:

1. newest matching `running` turn by highest `turns.seq`;
2. else newest matching `queued` turn by highest `turns.seq`;
3. else earliest matching pending wake by lowest `(dueAt, wakeId)`.

This precedence is normative.

### T4 — Latest terminal turn

The **latest terminal turn** for a target is the matching `turns` row with the
highest `seq` and `status IN ('delivered','canceled','failed','failed_unknown')`.

### T5 — Breathing reason

A **breathing reason** is the exact closed string returned in the query result.
The full vocabulary for this spec is:

- `running_turn`
- `queued_turn`
- `pending_wake`
- `open_assignment_lively`
- `session_missing`
- `session_retired`
- `assignment_missing`
- `assignment_closed`
- `holder_retired`
- `work_item_missing`
- `work_item_terminal`
- `no_open_assignment`
- `latest_terminal_failed`
- `latest_terminal_canceled`
- `no_current_path`
- `all_open_assignments_not_lively`

No other reason string is valid in this MVP.

### T6 — Deciding evidence

**Deciding evidence** is the minimal public row subset that selects the answer:
the target row when present, any target-state or holder-state gate row that
decides not-breathing, the selected current-path row when breathing is true,
or the selected terminal rows when breathing is false. When ordered linked
assignment results decide a work-item answer, the deciding evidence shall
include each selected assignment entry's `id` and `openedAt`. The query may
include additional public context rows, but it shall always include the
deciding rows.

### T7 — Supported lines

The **supported lines** are Tightbeam `0.1.9` and Tightbeam `main`/`0.2`. Both
shall return the same reason vocabulary, the same top-level result fields, and
the same exit-code contract for this query family.

## Assumptions

A1. On both supported lines, the durable schemas for `sessions`, `assignments`,
`work_items`, `turns`, and `wakes` contain the physical evidence fields in T2.

A2. On both supported lines, `turns` already records `status`, timestamps,
`error`, and `adapterGen`; `wakes` already records target linkage and state;
and `sessions` already records `state`.

A3. On both supported lines, current work on a work item can be observed from
open linked assignments, direct `jobRef` turns, and work-item-targeted wakes.

A4. Main already has a canonical public-query seam in `state_resources.ex`.
`0.1.9` does not. This spec requires output parity, not one internal module
shape.

A5. The current effort-checkin implementation on both lines still counts
attests and work-item updates as effect. This spec removes their authority for
breathing only. It does not redesign effort check-in in this card.

A6. The deterministic progress-since read (`wi_0c1ad73a`) and the bounded
watchdog (`wi_bcb85145`) remain separate work. This spec defines the physical
predicate they consume or stand beside; it does not merge them.

## Invariants

I1. Breathing is never stored. No table, fact, event, or projection row records
“breathing=true” or “breathing=false” as durable truth.

I2. `attests`, work-item state transitions, work-item updates, artifacts,
verdicts, messages, condition facts, standing reaffirmations, and patrol
acknowledgment rows are never admissible evidence for breathing.

I3. A query answer is snapshot-consistent. One evaluation reads one
transactional snapshot and returns evidence only from that snapshot.

I4. The same snapshot and same target produce the same breathing answer on both
supported lines.

I5. After the target-specific existence and state gates pass, a current path
proves breathing even when it does not prove success. A pending wake, queued
turn, or running turn says “the substrate still has a path,” not “the work is
advancing.”

I6. A missing session row, `sessions.state='retired'`,
`assignments.state='closed'`, a retired assignment holder session row, or
`work_items.state!='open'` decides not-breathing before current-path selection
for that affected target in the same snapshot.

I7. A latest failed or canceled terminal turn can decide not-breathing only
when no current path exists later in the same snapshot for the same target.

I8. Assignment breathing composes from the assignment row, its holder session
row, matching turns, and matching wakes only.

I9. Work-item breathing composes from the work-item row, direct work-item turns
and wakes, and linked open-assignment breathing results. Work-item state alone
does not prove breathing.

I10. The query exposes only public row fields already allowed on that product
line. Secret material such as `cliToken` is never emitted.

I11. `wi_990f7b7e` is superseded for physical breathing. Any future rail,
watchdog, query, or product feature that needs physical liveness shall consume
this spec’s physical evidence rather than attestation inheritance or any other
recorded-fact surrogate.

## Architecture

### AR1 — Query family and result shape

The agent-facing CLI family is:

- `tightbeam breathing session <sessionKey>`
- `tightbeam breathing assignment <assignmentId>`
- `tightbeam breathing work-item <workItemId>`

Each successful invocation writes one JSON object to stdout and exits `0`,
whether the answer is breathing or not breathing. Exit `1` is reserved for
misuse, authorization refusal, or substrate failure to execute the query.

The JSON shape is:

```json
{
  "schema": "breathing-v1",
  "target": {"kind": "assignment", "id": "asg_exact"},
  "breathing": false,
  "reason": "latest_terminal_failed",
  "evidence": {}
}
```

`schema`, `target`, `breathing`, `reason`, and `evidence` are mandatory.

### AR2 — Session breathing function

For target session `S`, evaluate in this exact order:

1. if no `sessions` row exists for `S`, return
   `breathing=false, reason=session_missing`;
2. else if `sessions.state='retired'`, return
   `breathing=false, reason=session_retired`. Matching running turns, queued
   turns, or pending wakes on `sessionKey=S` do not override this step;
3. else if T3 selects a matching current-path row on `sessionKey=S`, return
   `breathing=true` with reason from that row kind;
4. else if T4 on `sessionKey=S` selects a turn with
   `status IN ('failed','failed_unknown')`, return
   `breathing=false, reason=latest_terminal_failed`;
5. else if T4 on `sessionKey=S` selects a turn with `status='canceled'`,
   return `breathing=false, reason=latest_terminal_canceled`;
6. else return `breathing=false, reason=no_current_path`.

The deciding evidence shall include the session row when present and the row
chosen by step 3, 4, or 5 when those steps match.

### AR3 — Assignment breathing function

For target assignment `A`, evaluate in this exact order:

1. if no `assignments` row exists for `A`, return
   `breathing=false, reason=assignment_missing`;
2. else if `assignments.state='closed'`, return
   `breathing=false, reason=assignment_closed`. Matching running turns, queued
   turns, or pending wakes on `assignmentId=A` do not override this step;
3. else if the holder session row exists and `sessions.state='retired'`,
   return `breathing=false, reason=holder_retired`. Matching running turns,
   queued turns, or pending wakes on `assignmentId=A` do not override this
   step;
4. else if T3 selects a matching current-path row on `assignmentId=A`, return
   `breathing=true` with reason from that row kind;
5. else if T4 on `assignmentId=A` selects a turn with
   `status IN ('failed','failed_unknown')`, return
   `breathing=false, reason=latest_terminal_failed`;
6. else if T4 on `assignmentId=A` selects a turn with `status='canceled'`,
   return `breathing=false, reason=latest_terminal_canceled`;
7. else return `breathing=false, reason=no_current_path`.

The deciding evidence shall include the assignment row, the holder session row,
and the row chosen by step 4, 5, or 6 when those steps match.

### AR4 — Work-item breathing function

For target work item `W`, evaluate in this exact order:

1. if no `work_items` row exists for `W`, return
   `breathing=false, reason=work_item_missing`;
2. else if `work_items.state!='open'`, return
   `breathing=false, reason=work_item_terminal`. Matching direct running turns,
   queued turns, pending wakes, or linked-assignment breathing results do not
   override this step;
3. else if T3 selects a direct current-path row on `jobRef=W` or
   `work_item_id=W`, return `breathing=true` with reason from that row kind;
4. else compute assignment breathing for every open linked assignment with
   `assignments.workItemId=W`, ordered by these exact keys:
   a. breathing assignments sort before non-breathing assignments;
   b. among breathing assignments, `running_turn` sorts before
      `queued_turn`, and `queued_turn` sorts before `pending_wake`;
   c. any remaining tie sorts by `(openedAt, id)`;
5. if any ordered assignment result is breathing, return
   `breathing=true, reason=open_assignment_lively`, with the first breathing
   assignment result in evidence;
6. else if there are zero open linked assignments, return
   `breathing=false, reason=no_open_assignment`;
7. else return
   `breathing=false, reason=all_open_assignments_not_lively`.

For step 7, `evidence.openAssignments` shall contain one ordered entry per open
linked assignment with that assignment’s `id`, `openedAt`, `breathing`,
`reason`, and deciding evidence subset. This is the only array-form reason in
this MVP.

### AR5 — Recorded-fact removal

Every consumer that needs physical liveness after this spec lands shall use
AR2, AR3, or AR4, or the shared internal query helper that implements them.
No consumer may treat any of these as breathing authority:

- attestation presence or absence;
- work-item update presence or absence;
- artifact presence or absence;
- verdict presence or absence;
- condition-fact presence or absence;
- patrol-response acknowledgment presence or absence;
- standing reaffirmation presence or absence.

This amendment does not delete those rows or their existing meanings. It
deletes only their authority to answer breathing.

### AR6 — Cross-line implementation seam

Both supported lines shall expose one identical public contract.

On `main`/`0.2`, the implementation shall reuse the canonical public query seam
that already serves public rows, so the evidence payload uses the same public
serializers as other state reads.

On `0.1.9`, the implementation may read the same underlying tables through the
line’s existing getters and direct row queries. It shall not backport the whole
`state_resources` subsystem merely to satisfy this contract.

Internal seam choice is line-local. Output parity is mandatory.

### AR7 — Relationship to adjacent work

The deterministic progress-since read remains a separate factual history query.
It may help a human or higher layer judge advancement after a breathing answer.
It is not part of the breathing predicate.

The bounded watchdog remains separate. It may consume the breathing predicate as
one mechanical input before any labeled inference. It may not widen breathing
with inference or replace the exact reasons in this spec.

## Acceptance

A1. Given no session row for `session_missing`, when the caller runs
`tightbeam breathing session session_missing`, then stdout is one
`schema=breathing-v1` JSON object with `breathing=false`,
`reason=session_missing`, and exit `0`.

A2. Given an active session with at least one matching running turn and no
newer matching running turn, when the caller queries that session, then the
result is `breathing=true`, `reason=running_turn`, and `evidence.turn.seq`
equals the highest matching running `turns.seq`.

A3. Given an active session with no matching running turn and at least one
matching queued turn, when the caller queries that session, then the result is
`breathing=true`, `reason=queued_turn`, and `evidence.turn.seq` equals the
highest matching queued `turns.seq`.

A4. Given an active session with no matching running or queued turn and at
least one matching pending wake, when the caller queries that session, then the
result is `breathing=true`, `reason=pending_wake`, and
`evidence.wake.(dueAt,wakeId)` equals the lowest matching `(dueAt,wakeId)`.

A5. Given a session row with `state='retired'` and at least one matching
running turn, queued turn, or pending wake in the same snapshot, when the
caller queries that session, then the result is `breathing=false`,
`reason=session_retired`, and the evidence includes that session row and no
inferred adapter or provider label.

A6. Given an open assignment whose holder session is active and whose newest
matching terminal turn has `status='failed'` and `error='usageLimitExceeded'`,
and given no later matching running turn, queued turn, or pending wake, when
the caller queries that assignment, then the result is
`breathing=false`, `reason=latest_terminal_failed`, and the evidence includes
that exact terminal turn row with its raw `error`.

A7. Given an open assignment whose holder session is active and whose newest
matching terminal turn has `status='delivered'`, and given no later matching
running turn, queued turn, or pending wake, when the caller queries that
assignment, then the result is `breathing=false`, `reason=no_current_path`.

A8. Given a closed assignment and at least one matching running turn, queued
turn, or pending wake in the same snapshot, when the caller queries that
assignment, then the result is `breathing=false`, `reason=assignment_closed`,
and the evidence includes the assignment row with `state='closed'`.

A9. Given an open assignment whose holder session is retired and at least one
matching running turn, queued turn, or pending wake in the same snapshot, when
the caller queries that assignment, then the result is
`breathing=false`, `reason=holder_retired`, even if older delivered turns also
exist.

A10. Given an open work item with one open linked assignment that returns
`breathing=true`, when the caller queries that work item, then the work-item
result is `breathing=true`, `reason=open_assignment_lively`, and the evidence
includes that assignment result.

A11. Given an open work item with zero open linked assignments and one pending
work-item-targeted wake, when the caller queries that work item, then the
result is `breathing=true`, `reason=pending_wake`.

A12. Given an open work item with multiple open linked assignments and every
linked assignment returns `breathing=false`, and given no direct work-item
running turn, queued turn, or pending wake, when the caller queries that work
item, then the result is
`breathing=false`, `reason=all_open_assignments_not_lively`, and
`evidence.openAssignments` contains one ordered result per open linked
assignment ordered by `(openedAt, id)`, where each entry carries `id`,
`openedAt`, `breathing`, `reason`, and the deciding evidence subset.

A13. Given a target whose rows change during query execution, when the query
commits, then every returned evidence row and the selected reason come from one
transactional snapshot. The result never mixes a pre-close assignment row with
a post-close wake or turn row.

A14. Given the same persisted rows before and after a process restart, when the
caller repeats the same breathing query, then the returned JSON is identical
except for row-order-preserving serialization details already fixed by the line.
No recovery job or backfill row is required.

A15. Given a caller that is authorized to run the command, when the query
returns either `breathing=true` or `breathing=false`, then the CLI exits `0`.
Given misuse, authorization refusal, or substrate execution failure, the CLI
exits `1` and does not emit a fake breathing answer.

A16. Given both supported lines loaded with the same fixture rows, when the
same query runs on both lines, then both lines return the same top-level keys,
the same reason string, the same `breathing` boolean, and the same deciding
evidence values.

A17. Given a target whose session, assignment, or work item public row carries
secret sibling fields in storage, when the query returns evidence, then the
evidence omits every field already treated as secret by the line’s public query
surface, including tokens.

A18. Given a standing assignment with only a `reaffirmation` attest or only a
patrol-response acknowledgment since its last prompt, and given no current
running turn, queued turn, or pending wake, when the caller queries that
assignment, then the result is still `breathing=false`. Those recorded facts do
not establish breathing.

A19. Given a work item row with `state!='open'` and at least one matching
direct running turn, queued turn, pending wake, or lively linked assignment in
the same snapshot, when the caller queries that work item, then the result is
`breathing=false`, `reason=work_item_terminal`, and the evidence includes the
work-item row that closed eligibility for that target.

A20. Given an open work item with multiple open linked assignments whose
results are respectively `running_turn`, `queued_turn`, `pending_wake`, and
`no_current_path`, and given no direct work-item running turn, queued turn, or
pending wake, when the caller queries that work item, then the result is
`breathing=true`, `reason=open_assignment_lively`, and the evidence includes
the linked assignment result with `reason=running_turn` as the first ordered
breathing assignment winner.

## Open Questions

None for this MVP.
