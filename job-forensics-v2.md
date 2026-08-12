# Job forensics — v2 (the attribution + transition history v1 deferred)

> **AMENDED 2026-08-12:** the adjudication-episode schema this spec extends
> (`adjudication_episodes`, `episodeId`/`cause`/`healToken`, reopen/escalate
> kinds, `adjudication.ex`, and the S4 coordination below) died with
> adjudication. Adjudication was deleted 2026-08-05 ("Adjudication is DELETED. Model policy is guidance, not substrate." — `tightbeam-decisions.md`).
> Those portions are history; the non-adjudication forensics remain the
> standing record. See `adjudication-deletion-amendment.md`.

Status: READY (r2, gate NOT-READY(4) folded with the reviewer's own pins — six kinds confirmed by audit, resolvers pinned to durable carriers, prod semantics pinned, exact schema enumerated. Fold-and-go per Flynn's night order.) Flynn: "that doesn't sound hard" — it
isn't; it was deferred from job-trace-observability-v1 only because it was being
smuggled into an additive-columns lane. Prereqs on main: v1 (turns attribution + trace
verb, merged) and brackets. COORDINATE with s4-operability-v1 (READY, unimplemented):
it already adds `episodeId` + `cause` + `healToken` to adjudication episodes — this
spec ADDS to that schema, never duplicates it; if S4 implements first these columns
exist, else this lane creates them per S4's pinned definitions.

## Law 0 (binding, inherited)

Every record is a substrate side effect. No agent-authored anything.

## 1. Attribution columns — give session-keyed families their job key

Each write site already holds the assignment when it writes; it stops dropping it.
All additive, nullable (NULL = pre-v2 or genuinely jobless):

- `adjudication_episodes.assignmentId` + `.jobRef` — stamped at episode OPEN, resolved
  from the FAILING TURN's durable attribution (gate F2: the claim carries only seq —
  the resolver is `SELECT assignmentId, jobRef FROM turns WHERE seq = ?` for the turn
  whose failure opens the episode; NULL attribution stamps NULL — never inferred from
  "the session's active assignment").
- `wakes.assignmentId` — stamped at schedule time BY THE SUBSTRATE ONLY, NEVER from
  agent-supplied params (cross-review F6, Law-0 breach: the public wake handler copied
  params.assignment_id, letting an agent forge wake→turn→trace attribution). The
  assignment_id is a SUBSTRATE-INTERNAL field, stripped from any agent/dispatch param
  map before the handler and set only by trusted callers — supervision prods and
  effort check-ins pass their own local assignment; decision-DEADLINE wakes resolve it
  from the decision request's stored assignmentId (durable on the request row); bracket wakes keep their
  existing work_item_id; conversational/owner wakes NULL. THIS unlocks prod-TURN
  attribution, explicitly excluded from v1 ("no durable carrier") — the gateway's
  wake-delivery enqueue copies wake.assignmentId onto the turn like every other
  carrier.
- `wakes.canceledAt` — cancellation currently only flips state; one timestamp.
- `subagent_markers.assignmentId` — stamped at EMISSION from the parent session's
  currently RUNNING turn's `turns.assignmentId` (gate F2: a session can hold multiple
  open assignments — the running turn at emission time is the unique durable carrier;
  no running turn or NULL attribution → NULL, never guessed).

## 2. `causal_events` — append the transitions that overwrites destroy

The v1-era design, already gate-hardened (atomic in-txn append; necessity rule:
admitted ONLY if the fact is destroyed by an overwrite or has no timestamped home;
the implementation's first task is the per-kind audit, dropping any kind that proves
reconstructable):

Table: `causal_events {seq PK AUTOINCREMENT, at, jobRef, assignmentId, sessionKey,
kind, detail JSON}`, indexed `(jobRef, seq)` + `(assignmentId, seq)`. Append rides IN
the transaction of the write it records — commit together or not at all.

| kind | detail | lost today because |
|---|---|---|
| `adjudication_reopen` / `adjudication_escalate` | {episodeId, fromState, toState, toRung?, toTarget?} | episode row overwritten in place |
| `effort_rung_advance` | {requestId, fromRung, toRung, fromExpecter, toExpecter} | request row overwritten |
| `prod_fired` | {tier: INTEGER (the supervision ladder tier that fired)} | counter is a mutable aggregate, resets after attest |
| `prod_answered` | {byAttestId} — ONE event per previously-unseen attest id observed at the answer evaluation (multiple attests between evaluations each get one, ordered by id). NO BACKFILL (cross-review F5): the unseen-attest resolver must be BOUNDED to attests filed at/after the causal_events table's creation (a v2-epoch cutoff timestamp), NOT the assignment's entire pre-v2 history — the first post-migration attest must not retroactively emit events for historical ones. | same — the edge is lost |
| `disposition_transition` | {workItemId, fromState, toState, failReason?} | item keeps current state only |

(Wake fire/schedule stay excluded — durable on the wake row; bracket nags stay
excluded — durable as wake-backed turns. The audited exclusion list from v1's gates
stands.)

## 3. Trace verb extension

`work-item-trace`'s timeline gains entry types with EXACT key sets (every key always
present, nullable where marked — never absent-vs-null ambiguity):
- `causal_event` {at, seqTiebreak, type: "causal_event", id: "ce:"<seq>, kind,
  assignmentId|null, jobRef|null, sessionKey|null, detail} — detail is the kind's
  pinned map verbatim; per-kind column sources: adjudication kinds carry the episode's
  stamped assignmentId/jobRef (nullable); effort_rung_advance carries the request's;
  prod kinds carry the prod's assignment; disposition_transition carries jobRef =
  workItemId with assignmentId null.
- `wake_canceled` {at: canceledAt, seqTiebreak, type: "wake_canceled", id: wakeId,
  assignmentId|null, reason|null}.
Type rank (extending v1's pinned order): wake_canceled = 2.5 slot → full rank list
becomes [turn_start=0, wake_scheduled=1, wake_fired=2, wake_canceled=3,
decision_request=4, causal_event=5, effort_generation=6, attest=7, turn_end=8] —
job_trace's sorter requires an explicit rank per type and gets one. Schema test
extended — missing/extra key fails, as shipped in v1.

## Non-goals

No new verbs. No agent visibility. No backfill of pre-v2 history (NULL is honest).
No cost/token capture (still no carrier). Golden-jobs consumes; nothing else changes.

## Required proofs

1. Atomicity: append + domain write commit/rollback together (simulated failure).
2. Each kind emits at its transition with exact detail; per-kind audit documented —
   any dropped kind named in the impl report.
3. Prod-turn attribution end to end: prod wake carries assignmentId → delivered turn
   stamped assignmentId+jobRef → appears in the trace (the v1 exclusion, closed).
4. Episode attribution: an adapter-fault episode carries assignmentId/jobRef from the
   open seam; reopen/escalate append events; the CURRENT row still matches v1 reads.
5. Marker attribution: emission-stamped; unresolvable = NULL, never guessed.
6. wake.canceledAt written on every cancel path; trace carries the entry.
7. Disposition history: icebox→reopen→close yields three transition events with
   correct from/to; work-item row unchanged in shape.
8. Trace schema: extended timeline validates; v1 consumers (golden-jobs contract)
   unaffected by the additive types.
9. Migration: all columns additive ALTERs, causal_events fresh table, existing rows
   preserved, indexes proven.

## Component touches

adjudication.ex (open-seam stamping + reopen/escalate appends — coordinate with S4's
columns), supervision.ex (prod wake assignmentId + fired/answered appends),
effort_checkin.ex + escalation.ex (rung appends), wakes.ex (assignmentId, canceledAt),
subagent_markers.ex (emission stamp), work_items.ex (disposition appends), gateway
wake-delivery enqueue (prod-turn attribution), job_trace.ex + appendix schema + tests,
migrations. All within existing write transactions — no new processes, no hot-path
changes.
