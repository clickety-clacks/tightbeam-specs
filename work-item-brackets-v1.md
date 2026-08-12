# Work-item lifecycle brackets — v1

Status: READY (gate-cleared 2026-07-25 by stop-rule: reviewer confirmed ZERO design/
feasibility/concurrency/architecture blockers at r5; rounds r5→r6→r7 found only
stale-sibling-clause text, closed comprehensively by the authoritative-amendment sweep
below. Trajectory 6→5→4→3→3→3-contract-text). r6 folded from r5 gate NOT-READY(3) — completed the cross-spec amendment sets: work-item-v1 owner/closure clauses + internal-writer authorization, observability-v1 exact emission-site list + metadata meaning, constitution §2 detailed bullets. Reviewer confirmed ZERO design/feasibility/concurrency blockers remain — contract-text only. r4 gate NOT-READY(3) folded — race-interlock proof, slate-rearm/owner-visibility/doorbell proofs, explicit work-item-v1 clause amendments; r3 gate NOT-READY(4) folded — in-txn terminal CAS, replay-hoist validation contract + assign-through-Dispatch proof, exact response envelope, doorbell-count proofs; r2 gate NOT-READY(5) folded — replay-vs-guard total order, icebox cancels BOTH brackets + state!=open predicate, full response-shape enumeration, create-doorbell decision, proof-plan completion; r1 gate NOT-READY(6) folded — idempotency op, dispatch rumination-vs-replay ordering, terminal disposition vs open assignments AND pre-handler statutes, fail-reason persistence, observability visibility model, orphan-owner selector). Implements accountability-constitution-v1
§2's "No intent in limbo" (UNBUILT there; that section remains the DESIGN authority —
this spec is its implementation contract, resolving the seven readiness gaps the gate
found against main `766f832`). Flynn: "spec and impl."

## Spirit (constitution §2, restated)

A work item filed and never routed must become someone's problem on a deadline; a work
item whose last assignment closed without conclusion must become someone's problem
immediately. Healthy paths are silent (red-tape test). The brackets are the effort
check-in's sibling: that machinery watches holders who have work; this watches work
that has no holder.

## Amendments to work-item-v1 (gate F7 + r5-F3 — REQUIRED, each clause named)

This lane amends FOUR live work-item-v1 clauses explicitly (naming them is the
necessity gate; the constitution §2 + Flynn's spec-and-impl directive are the
authority):
- **"no work-item states"** → the four-state `state` column (§Terminal dispositions).
- **"no create idempotency"** → the optional `idempotencyKey` + ledger op (§Bracket 1).
- **"update is the only writer besides create"** → the disposition verbs are
  additional owner/admin writers of `state`/`failReason`.
- **the pinned response shape** → the object gains ownerUserId/state/failReason
  (§Response shapes).
- **"no owner semantics"** → the `ownerUserId` column + owner-scoped visibility and
  disposition authority (§Ownership, §Terminal dispositions).
- **"assignment closure never touches the item row"** → bracket-2's last-close path
  writes `slateWakeId` on the item; disposition/assign/dispatch/fire paths write the
  wake-id columns. The writer amendment authorizes, beyond disposition writes to
  `state`/`failReason`: the create path (owner, routingWakeId), the assign/dispatch
  cancel paths (clearing routingWakeId/slateWakeId), the close path (slateWakeId),
  and the bracket-fire re-arm (routingWakeId/slateWakeId). These are INTERNAL
  substrate writers of internal columns — not new agent-facing verbs.
Plus the persistence clause below.

work-item-v1's "assign is the only verb with persistable workItemId" predates the
`dispatch` verb. AMENDED: `dispatch` persists `workItemId` exactly as `assign` does
(same in-txn existence check). **Replay ordering (gate F2):** dispatch today evaluates
rumination BEFORE the idempotency short-circuit (`dispatch_result` checks
`rumination_exists?` first). The amendment REORDERS: an idempotency-key hit
short-circuits and returns the ORIGINAL assignment BEFORE any rumination evaluation —
so a keyed replay carrying a same/different/missing/unknown workItemId yields the
original assignment and NO new rumination wake. The constitution's design requires
persistence (a dispatched assignment must cancel bracket 1 and count for bracket 2);
this clause additionally pins that replay is rumination-inert. feature_smoke's
"workItemId assign-only" assertion is updated to assert BOTH verbs persist. (Authority:
ratified constitution §2 + Flynn's spec-and-impl directive.)

## Mechanism

### Ownership and targeting (gate F1)

`work_items` gains `ownerUserId TEXT NOT NULL` — the OWNER IS ALWAYS A USER. On create:
a user creator owns directly; a SESSION creator's item is owned by that session's
`ownerUserId` (sessions are disposable projections — constitution §3 — so durable
obligations anchor to the human even when a session filed the item). Bracket wakes
target `Org.personal_session_key(ownerUserId)` — always resolvable, never retired,
no fallback chain needed. (The creator session, when there is one, stays recorded in
the existing creator columns for provenance; it carries no bracket obligation.)

### Bracket 1 — routed-or-deadline (constitution, plus gate F3/F5 fixes)

- The work-item-create TRANSACTION (which becomes a real multi-write txn) inserts the
  item, arms one `consumer='prompt'` wake to the owner's personal session
  (`dueAt = now + triage deadline`; config `:tightbeam, :work_item_triage_deadline_ms`
  / `TIGHTBEAM_WORK_ITEM_TRIAGE_DEADLINE_MS`, default 24h), and stores `routingWakeId`
  on the item. Prompt text: "route it or icebox it" + the item id/title.
- CANCELED in the same transaction by: the first `assign` OR `dispatch` referencing
  the item (F7 amendment makes both real), or the `work-item-icebox` verb (below).
- **Idempotency (gate F5, F1):** `work-item-create` gains an optional
  `idempotencyKey` (wire + CLI). The `wire_idempotency.operation` CHECK is WIDENED
  to add `'work-item-create'` (its own op string — reusing `assign` would collide
  cross-verb); key scope is `{operation, key, ownerUserId}`. A key hit returns the
  original item and arms NOTHING new; the create becomes a real multi-write txn
  (insert + ledger row + wake) so replay is atomic. Keyless creates remain legal
  (interactive use) — duplicates then arm duplicate timers, the correct nag for
  genuinely duplicate intent. Migration widens the CHECK via the table-rebuild
  pattern.
- **Nag persistence (gate F3):** supervision's prod ladder only watches sessions with
  open assignments, so an ignored bracket wake would die silently. Brackets therefore
  RE-ARM on fire instead of relying on the lattice. Mechanism (gate reviewer's
  confirmed seam): a bracket-1 wake is a process-origin prompt wake delivered through
  `Gateway.deliver_prompt_in_txn`; that transaction — for a bracket wake — CAS-checks
  the item still unrouted/un-iceboxed, appends the nag turn, arms the replacement wake,
  and updates `routingWakeId`, atomically. The ordinary deliver-then-mark scheduler
  path alone cannot re-arm; the existing Gateway transaction seam carries it. No new
  wake state or consumer. An ignored owner is re-nagged each deadline, by construction.

### Bracket 2 — concluded-or-adjudicated (gate F4 fix)

- The assignment-CLOSE transaction (all four paths — completion, surrender, revoke,
  retire-strand — the same seams effort cancel_in_txn already rides) checks, AFTER its
  own writes: does this close leave the item with zero open assignments AND the item
  is not terminal? If so it ARMS A DURABLE WAKE in that same transaction (owner's
  personal session, prompt "slate clear on <item>: close it, card more work, or rule
  it failed", `dueAt = now` — immediate), storing `slateWakeId` on the item.
  **No post-commit deliver_owner callback** (gate F4: the escalation pattern's
  commit-then-callback loses the edge on a crash; a durable wake row survives and
  redelivers through `turns.wakeId` dedupe like every other wake).
- Canceled in-txn by the next `assign`/`dispatch` referencing the item (slate no
  longer clear) or by a terminal disposition (below). Re-arms naturally on each later
  last-close.
- Like bracket 1, an ignored slate wake re-arms itself on fire (deadline = the same
  triage config) — nag by construction.

### Terminal dispositions (gate F2)

`work_items` gains `state TEXT NOT NULL DEFAULT 'open' CHECK (state IN
('open','iceboxed','closed','failed'))` (amends constitution §8's "no work-item
states" — §8 currency fix below) and `failReason TEXT NULL` (gate F4 — the
payload-free doorbell has nowhere to carry a reason; durable truth is a column, the
doorbell stays a bare metadata edge). Verbs, all owner-or-admin authority:
- `work-item-icebox <id>` — open → iceboxed. **Requires zero open assignments**;
  refused with a legible error while assignments are open. Cancels BOTH brackets
  in-txn (r3-F2: after a last-close a slate wake exists, so icebox must cancel
  bracket 2 too — every disposition cancels both, matching Proof 5).
  `work-item-reopen <id>` (iceboxed → open) re-arms bracket 1.
- `work-item-close <id>` — open|iceboxed → closed; requires zero open assignments
  (closing under live work is the bracket-2 slate-clear path's job, not a manual
  race). Cancels both brackets.
- `work-item-fail <id> [--reason]` — open|iceboxed → failed; requires zero open
  assignments; reason → `failReason` column.
- Same-state transition is a no-op success; disallowed transitions refuse.
- **Total ordering — idempotency replay, then terminal guard, then statutes
  (gate r2-F1, r3-F1):** the dispatch chokepoint runs in this exact order for an
  assign/dispatch verb carrying a workItemId:
  1. IDEMPOTENCY REPLAY LOOKUP first, for EVERY keyed assign OR dispatch (r4-F2 —
     not only workItemId-carrying calls). Validation that STILL runs before the
     lookup: authority, subject, key-format, files (assign's existing pre-lookup
     validations — preserved verbatim so assign semantics are unchanged). What the
     lookup BYPASSES on a hit: work-item existence/state validation, statute
     evaluation, terminal guard, and rumination — a key hit returns the ORIGINAL
     assignment regardless of the item's current state (matching assign-replay's
     pinned bypass-validation). A replay carrying a now-disposed/different/missing/
     unknown item still returns its original assignment; the disposition never sees
     it. The hoist applies to BOTH verbs through the Dispatch chokepoint (r4-F2: the
     existing assign-replay test calls the handler directly — this lane adds an
     assign-replay-through-Dispatch proof covering disposed items and statute
     inertness).
  2. On a MISS: the TERMINAL GUARD — refuse if `state != 'open'` (iceboxed also
     refuses new work — r3-F2), before `Rules.decide`, so no statute or remedy
     episode touches a non-open item. This is the EARLY refusal (avoids rail side
     effects); it is NOT the sole guard.
  3. On open + non-replay: `Rules.decide` and the handler proceed; the assignment
     INSERT transaction re-checks `state='open'` as an in-txn INTERLOCK and aborts if
     it changed (r4-F1: the pre-statute read and the insert are different
     transactions; a disposition committing in between must not let a terminal item
     acquire an open assignment). Both guards are required — the pre-statute one for
     rail-inertness, the in-txn one for correctness under concurrency.
  This hoists the replay lookup to the chokepoint (the one structural change; named
  because both the guard and the rail need to see the replay outcome first).
- CLI: all verbs added to cli-surface-v1's enumeration IN THIS LANE.
- Observability: state transitions emit the existing work_item_events metadata
  doorbell (bare kind edge; `failReason` is column truth, queryable, not on the
  wire) — no new frame kinds.
- **Response shapes (r3-F3 + r4-F3, exact envelopes):** the `workItem` OBJECT inside
  every response (`work-item-create/update/get/list` and device snapshot/detail)
  gains `ownerUserId`, `state`, `failReason` (additive object fields; consumers
  ignoring them unaffected). Wake IDs (`routingWakeId`/`slateWakeId`) are INTERNAL —
  never in any response object. The four disposition verbs return
  `%{ok: true, workItem: <updated object>}` (the `ok` is the ENVELOPE key beside
  `workItem`, NOT a field inside the object; the object itself is the same
  `workItem` shape work-item-get nests — note work-item-get returns
  `%{workItem, assignments}`, so a disposition returns the `workItem` half plus
  `ok`, WITHOUT the assignments list). A same-state no-op returns the same envelope
  and changes nothing.

### Create doorbell (r3-F4)

observability-v1 declared `work-item-create` SILENT because an unassigned item was not
board material. This lane makes an unassigned item OWNER-VISIBLE, so that rationale is
void: an actual create (not a keyed replay) emits ONE owner-routed metadata doorbell so
the owner's board reflects the new item; keyed replay emits nothing (it created
nothing). This re-ratifies the addendum's `work_items` row from "create-silence by
design" to "create → one owner doorbell; replay silent".

### Observability amendment (gate F5 — REQUIRED, beyond the addendum row)

observability-v1 pins work items as state-free with assignment-holder-derived
visibility, which breaks THREE ways for brackets: an UNASSIGNED item's owner can't
see it (visibility needs a visible assignment), a transition doorbell has no
recipients (fan-out derives owners from assignment holders), and the pinned
snapshot/detail shapes can't carry `state`. Amendment, in this lane, to
observability-v1: (1) work-item visibility gains an OWNER path — an item is visible
to its `ownerUserId` regardless of assignments (the owner column this lane adds is
the authority); (2) work-item snapshot/detail AND `/agent` shapes gain `ownerUserId`, `state`, and
`failReason` (additive — §Terminal dispositions enumerates them; an admin listing all
items needs `ownerUserId` to see ownership); (2b, r5-F2) the EXACT emission-site list
is extended: observability-v1 today pins sites at update and assign only — this lane
ADDS the create site (one owner doorbell) and the four disposition sites
(icebox/close/fail/reopen), and BROADENS the normative `metadata` kind meaning from
"title/spec-pin change" to "any owner-visible work-item metadata change incl. state
transitions"; (3) the
work-item doorbell fan-out includes the item's owner, not only assignment holders,
so a transition on an unassigned item reaches someone. This is a named amendment to
a live spec (the necessity gate: authority is constitution §2, which requires the
owner to be nagged about unassigned items).

### Migration (gate F6)

Table rebuild per the established pattern: `ownerUserId` backfilled from the creator
columns (session creators → their session's ownerUserId at migration time). **Orphan
selector (gate F6):** a row whose creator session no longer resolves backfills to the
DETERMINISTIC org owner = the `users` row with `isAdmin=1` and the lowest `userId`
(stable ordering; "org owner" is not otherwise a singleton). If ZERO admin users
exist, the migration REFUSES with a legible error rather than guessing (greenfield
makes this reachable only in a corrupt DB). `state='open'`;
`failReason`/`routingWakeId`/`slateWakeId` NULL. EXISTING items get NO retroactive
brackets — brackets arm on post-migration events only. The migration release note
instructs one manual `work-item-list` review; retroactive nagging of old intent is
operator judgment, not substrate law. Upgrade proof from a pre-change schema fixture
(the 8d pattern) that POPULATES child references (`assignments`, `artifacts`,
`work_item_events`) and asserts `PRAGMA foreign_key_check` clean after the
parent-table rebuild.

## Constitution currency fixes (gate C9 + r5-F3, folded here)

§2's `dispatch` marker UNBUILT → SHIPPED; §2's brackets marker UNBUILT → points at
this spec; §8's "no work-item states" line amended to name the four disposition
states. AND §2's DETAILED bracket bullets are updated to the shipped mechanics
(r5-F3 — they still describe the pre-implementation design): "first assign cancels"
→ "first assign OR dispatch cancels"; "post-commit owner wake" (bracket 2) → "durable
in-transaction wake, no post-commit callback"; "both wakes ride the ordinary lattice /
an ignored owner is prodded" → "brackets RE-ARM on fire (the lattice does not watch
holderless work); an ignored owner is re-nagged each horizon by the re-arm, not by the
prod ladder". The constitution's §2 becomes a faithful description of what shipped. Named r7
additions: §2's "No state" clause → the four disposition states; §2's "owner defaults
to the creator" → owner is the creating user, or a session-creator's owning user (never
the creator session); the observability exact-site list also adds the `dispatch`
composition doorbell (dispatch now persists workItemId like assign).

**Authoritative-amendment sweep (r7, deterministic close):** this spec is AUTHORITATIVE
wherever it conflicts with prior text describing PRE-BRACKETS work-item behavior. Every
clause in accountability-constitution-v1 §2/§8, work-item-v1, and observability-v1 that
asserts any of {no work-item state, no owner semantics, owner-defaults-to-creator,
create has no idempotency, update is the only writer, the old response shape, the old
emission-site list, first-assign-only cancellation, post-commit bracket delivery,
lattice-nagging} is amended to this spec's shipped mechanics. An un-enumerated stale
clause is covered by this sweep, not a defect — the implementer treats this spec as the
current belief and updates any sibling text it contradicts in the same change (specs
state current belief; git carries history).

## Non-goals

- No supervision/lattice changes (nag-by-re-arm makes them unnecessary — F3).
- No new frame kinds, facts, or statutes; org law MAY later predicate on the doorbell
  events (constitution's "further conditions are ORG LAW" line stands).
- No auto-icebox, auto-close, or any substrate-decided disposition.

## Required proofs (fail-on-revert)

1. Create (keyed and keyless) arms bracket 1 in the create txn; keyed replay returns
   the original and arms nothing; `routingWakeId` stored.
2. First `assign` AND first `dispatch` referencing the item each cancel bracket 1
   in their own txn — and BOTH persist `workItemId` on the assignment (the F7
   amendment, asserted both directions; the updated smoke assertion ships in this
   lane).
3. Bracket-1 fire with the item still unrouted re-arms itself (new wakeId, one nag
   turn delivered); icebox cancels and stops the nag.
4. Last-close of a non-terminal item arms the slate wake IN the close transaction
   (all four close paths); a crash between commit and any delivery loses nothing
   (the wake row is durable; redelivery dedupes via turns.wakeId). Next assign
   cancels it; re-arms on the next last-close cycle.
5. Terminal dispositions: each verb transitions correctly, cancels both brackets,
   refuses assign/dispatch afterward, repeats as no-op success; reopen re-arms
   bracket 1.
6. Owner resolution: session-created items anchor to the session's owning user;
   bracket wakes reach the personal session; no bracket ever targets a retired
   session.
7. Effort-checkin coexistence: an item whose dispatched assignment carries an armed
   effort bracket closes cleanly through both machineries in one transaction
   (ordering asserted).
8. Migration: pre-change DB rebuilds, backfills owners, arms nothing retroactively.
9. feature_smoke: create → idle past a short triage horizon → owner receives the
   route-or-icebox nag → dispatch cancels it → revoke (last close) → slate wake
   arrives → `work-item-fail` disposes; per-leg per T-PARITY.
10. Replay ordering: dispatch replay across same/different/missing/unknown workItemId
    returns the original assignment with ZERO rumination wake AND no terminal-guard
    evaluation (a replay of a since-disposed item still succeeds).
11. Disposition-while-open: each of icebox/close/fail is REFUSED while any assignment
    on the item is open; legible error.
12. Terminal-beats-rail: dispatching the shipped refix-bug flow against a
    closed|failed|iceboxed item creates NO statute/remedy episode and NO diagnosis
    assignment (the pre-statute guard fires first).
13. failReason: `work-item-fail --reason` persists to the column and the reason
    appears in get/list/detail; icebox/close leave it NULL.
14. Response shapes: create/get/list/UPDATE/detail AND device snapshot expose
    ownerUserId/state/failReason on the workItem object; wake IDs never appear in any
    response; each disposition returns %{ok:true, workItem}; same-state is an ok
    no-op.
15. Create doorbell: an actual create emits EXACTLY ONE owner-routed metadata
    doorbell (assert count AND recipient = ownerUserId); a keyed replay emits ZERO.
16. RACE interlock (r4-F1 proof): a disposition committed AFTER the pre-statute guard
    read but BEFORE the assignment-insert txn causes the insert to abort on the
    in-txn state='open' check — the terminal item does NOT acquire an open
    assignment (drive the two checks around an injected concurrent disposition).
17. Bracket-2 slate re-arm ON FIRE: an ignored slate wake re-arms itself at the next
    horizon (distinct from Proof 4's assign/last-close re-arm cycle).
18. Owner visibility: a NON-ADMIN owner lists AND details its own UNASSIGNED item
    through the owner path (the test uses owner, not admin, access — proving the
    visibility amendment, not admin bypass).
19. Disposition doorbells: each real disposition (icebox/close/fail/reopen) emits its
    metadata doorbell; a same-state no-op emits NONE.

## Component touches

work_items.ex (schema rebuild, owner/state/wake columns, verbs); assignments.ex
(dispatch workItemId persistence — the amendment; bracket cancels + slate arming in
the close paths); wakes (nothing new — prompt wakes + the cancel-and-replace pattern
as used by effort_deadline); router/gateway verb registration; cli args/dispatch +
cli-surface-v1 enumeration; work-item-v1 amendment paragraph; constitution currency
fixes; observability addendum row update; config + env for the triage deadline;
feature_smoke journey; migration + upgrade fixture.
