# Observability v1 — grain-agnostic work model, thin change doorbells, query surface (implementation spec, r4)

Status: DRAFT r4 (revised per Flynn's grain-agnostic OBSERVABILITY
GRAIN ruling resolving the r3 review's one BLOCKER: the substrate
does NOT decide what a "card" is — card grain is VIEW-SIDE and
tightbeam has no business modeling it. r3 made the bare assignment
THE card and pinned `ref = assignmentId`; work-items now EXIST on
main. r4 drops that: the substrate exposes BOTH model entities —
ASSIGNMENTS and WORK-ITEMS — random-accessibly via queries, plus
thin change-doorbells on BOTH grains; the VIEW picks its grain and
queries. Also: `verdictKind` merged (check-tier), so the `verified`
predicate flips from constant-false to LIVE; supervision repinned
r13 → r17 (consumed seams survive); baseline repinned f739c07 →
ac60d09.) History: r3 per the r2 confirmation round (supervision
r12 → r13, re-auth preserves subscription class, `verified` pinned
constant-false while `verdictKind` absent); r2 per the r1 adversarial
round (verified predicate pinned, honest dropped-event convergence +
registration-before-snapshot ordering, delete-all test on non-cursor
fields, `emit/3` return contract, four emission-site mechanics,
detail-cursor semantics, work-state-only inbound gating); r1 initial.
Parent design: the decisions-ledger entries of 2026-07-20
(OBSERVABILITY DIRECTION RULED + refinements + boundary principle +
the CODEX-GATES POSTURE + OBSERVABILITY GRAIN ruling that r4 applies).
This spec is sole authority for its scope; the ledger entries are
background. It consumes attest-v1.md r5 (assignments/attests rows,
the `assignments` query verb), work-item-v1.md r2 (`work_items`
rows, the nullable `workItemId` on assignments, work-item verbs
including work-item-update and the assign `--work-item` link),
check-tier-v1.md r4 (the `verdict` attest kind and the `verdictKind`
column, merged — the `verified` derivation is now live), and
supervision-impl-v1.md r17 (derived-stranded ruling, `assignment_prods`
rows, the retire-site `:on_retired` seam — the consumed fields and
seam survive r17 unchanged; r17's `reresolveSeed`/`reresolveRung`
land on the `wakes` row, not on `assignment_prods`, and its
cascade-boundedness rewrite leaves the mechanism untouched).
attest, work-item, and check-tier are MERGED at main ac60d09;
supervision-impl is NOT yet merged and must be before this builds
(§Build ordering). Code claims verified against main ac60d09.

Model-as-view, not object: there is NO ticket table, NO state
machine, NO transition rows, and NO substrate-chosen "card." Both
model entities the substrate already owns — the ASSIGNMENT (work in
one session's hands) and the WORK-ITEM (the durable feature the work
is about, work-item-v1) — are exposed RANDOM-ACCESSIBLY. Work state
is a MECHANICAL, judgment-free status FUNCTION over an assignment's
existing facts, computed at query time; a work-item has NO substrate
status at all (work-item-v1: no state column, ever) — a view that
wants an item-level roll-up computes it from the item's assignments,
which the substrate serves with their derived per-assignment status
attached. Agents produce facts; humans and dashboards consume views;
nothing writes state as an act separate from doing the work. What
this spec adds is (1) the per-assignment status function and its
random-access query surface over BOTH grains, (2) THIN change-event
classes on the existing wire — UI doorbells, not truth, one per
grain — and (3) the monotone cursors that join them. The existing
marker messages (context-reset/turn-failed, gateway.ex `append_marker`)
are the proto-precedent: substrate facts a chat reader must see,
riding the same wire. This spec generalizes that into first-class
TYPED event classes with a per-connection filter; the markers
themselves are unchanged (they remain ordinary chat messages).

NAMING (deviation from the tasking sketch, deliberate): the
open-with-retired-holder state is called **stranded**, following
supervision-impl's ruled vocabulary — supervision already uses
"stalled"/`stalledAt` for a DIFFERENT mechanical condition (the
escalation epoch). One word per condition; this spec defines the
stranded QUERY that supervision promised ("computed at query time by
any observer"). Upheld by the r1 adversarial review.

## Design position — grain-agnostic (Flynn's ruling, 2026-07-20)

Recorded verbatim (decisions-ledger 2026-07-20 "OBSERVABILITY /
KANBAN", under the CODEX-GATES POSTURE + OBSERVABILITY GRAIN entry):

> tightbeam does NOT decide what a "card" is — that is VIEW-SIDE
> semantics and the substrate has no business modeling it. Neither
> "assignment is the card" nor "work-item is the card." The substrate
> exposes BOTH model entities (assignments AND work-items)
> RANDOM-ACCESSIBLY (queries), plus thin change-doorbells; the VIEW
> (kanban / stream-widget / an unsolved 20k' view) picks its grain and
> queries. Flynn's load-bearing point: a board is FUNDAMENTALLY RANDOM
> ACCESS — it needs "all current work + state, now," which comes from a
> QUERY, never from reconstructing a stream; events only say "re-query
> this." Product context (why the substrate must stay grain-agnostic —
> the right view is not yet known): kanban is "too mechanical — like
> looking under the hood to check if the steering wheel works when
> turning the wheel would tell you"; Flynn's stream-widget (newest
> ticket-change inserted left in a horizontally-scrolling list, deltas
> summarized on top) shows live action well but still lacks the 20k'
> overview; the 20k' work view is an OPEN product problem. A substrate
> that committed to a card grain would bet on a view not yet designed.

The design position this fixes, stated for implementation: observability
exposes the MODEL — assignments and work-items — RANDOM-ACCESSIBLY,
plus thin change doorbells on each grain, and NOTHING ELSE. The card
grain, columns, swimlanes, priorities, orderings, item-level status
AGGREGATION/roll-up policy, and the 20k' overview are VIEW concerns
this substrate does not model, name, branch on, or decide. This is the
substrate/product boundary applied to observability: the substrate
serves neutral, queryable material at both grains; the product picks a
grain, queries it, and owns its own summarization. A board is random
access by nature — it reads "all current work + state, now" from a
QUERY; the events only ever say "re-query this."

## Goals

1. `status(assignment)` is a total, deterministic derivation over
   existing rows — any observer computes the same answer from the same
   facts, with zero stored state.
2. BOTH grains are random-access: assignments query to a filterable
   snapshot of per-assignment derived status; work-items query to a
   snapshot of item metadata plus each item's assignments carrying
   their derived status, so a view can present items and drill into
   assignments — or present assignments directly. A board renders from
   ONE snapshot query per grain + a filtered thin-change stream, joined
   by a monotone cursor; detail views are random-access queries at
   click time, never event payloads.
3. Thin events are self-healing in the precise sense that the NEXT
   READ RECOMPUTES: a duplicated or reordered doorbell is neutralized
   by the client contract, and a LOST doorbell leaves the consumer
   stale — with no automatic signal — until its next refetch or
   reconnect snapshot, which heals it unconditionally. The stream can
   never become a second drift-prone copy of state; it also never
   promises prompt convergence, only convergence at the next read.
   This holds for BOTH grains.
4. One wire: chat clients and boards are per-connection FILTERS over
   the same socket, not separate systems; both grains' doorbells ride
   the one work-state subscription class.

## Non-goals (do not build)

The board UI itself and every board concept — columns, priorities,
sprints, swimlanes, orderings, descriptions-for-humans, the card
grain itself, and any item-level status AGGREGATION policy
(product/view layer; the substrate serves neutral queryable material
at both grains, per the bible's boundary and the ledger's grain
ruling). The substrate does NOT choose a card unit and does NOT define
`ref` as one entity: assignment-grain events ref an assignment,
work-item-grain events ref a work item, and a view decides which grain
is its card. Judgment-based status of any kind ("blocked", "at risk",
"almost done" — T1 violations). A work-item STATE/status column or a
substrate-computed item-level aggregate status — work-item-v1 pins "no
state, ever"; any worst-status-wins / roll-up summarization is
VIEW-SIDE policy and is NOT built here (an OPTIONAL mechanical
convenience the substrate MAY expose is bounded in §Query surface and
a view may ignore it). Mutation of work-items or assignments (this
spec is read + doorbell only; work-item-v1 owns work-item writes,
attest owns assignment writes). Turn-level liveness states
(running-right-now stays on the existing turn-state frames, which
remain chat-class; see §Open ruling). New agent verbs or CLI
subcommands (agents already have the `assignments`, `work-item-get`,
and `work-item-list` verbs; the query surface here is the device-authed
product side). Pagination, event retention/pruning, role filter params,
multi-user visibility partitioning (single-operator v1, matching attest
r5's ruling). Backfill or replay of state events — a reconnecting
consumer re-snapshots; that IS the recovery protocol. No changes under
cli/.

## The status function (normative derivation — assignment grain)

Vocabulary — CLOSED at six states; adding one is a spec revision:
`open | active | stranded | claims-done | verified | abandoned`.
This is a PER-ASSIGNMENT function only. Work-items have no substrate
status (§Design position, §Query surface).

For one assignment row `a` (attest r5 schema), with `holder` =
sessions row for `a.holderKey` (always exists — attest FK) and
`filings(a)` = COUNT of attests rows for `a.id`, evaluated in THIS
precedence order (first match wins; the order is normative — a closed
assignment is never stranded, whatever its holder's state):

1. `a.state='closed' ∧ a.outcome IN ('surrendered','revoked')` →
   **abandoned**.
2. `a.state='closed' ∧ a.outcome='completed' ∧ ∃ attests row for
   a.id with kind='verdict' AND verdictKind='verified'` →
   **verified**. That string-exact predicate is the ONE reserved
   convention this spec and check-tier share for human verification:
   `verdictKind='verified'` and nothing else. Check-tier's verdictKind
   lexicon is otherwise free (`^[a-z0-9][a-z0-9-]*$`, 1..64) — NO other
   verdict row ("tests-passed", "reviewed", any future kind) makes this
   state; "any verdict = verification" is explicitly wrong. LIVE IN V1
   (flipped from r3's dormant form): at main ac60d09 check-tier is
   merged — attests carries the `verdictKind TEXT NULL` column and the
   `kind` CHECK admits `'verdict'` (assignments.ex:55-56). The
   derivation therefore evaluates this branch with REAL SQL against
   `verdictKind` (an EXISTS over attests where `kind='verdict' AND
   verdictKind='verified'`); the r3 constant-false / no-SQL /
   no-schema-probe pin is RETIRED because its precondition (the column
   absent) no longer holds. REACHABILITY: check-tier files verdicts
   only while the assignment is OPEN and never lets a verdict row land
   after closure (check-tier §race invariant); a `verdictKind='verified'`
   verdict filed while open, then a completion that closes the
   assignment, makes this branch true at the completion write — so
   `verified` is reached open/active → verified at the completion site
   (§Emission), never as a post-closure verdict (which check-tier
   refuses). Its positive test is now ACTIVE, not pending (§Tests).
3. `a.state='closed' ∧ a.outcome='completed'` → **claims-done** — the
   holder CLAIMS completion; the substrate records the claim and
   never adjudicates it (a completion with no `verified` verdict).
4. `a.state='open' ∧ holder.state='retired'` → **stranded** — this is
   exactly supervision's derived view-state (open ∧ holder
   retired), now a named query any consumer gets for free.
5. `a.state='open' ∧ filings(a) = 0` → **open** — obligation exists,
   nothing filed yet.
6. else (`a.state='open' ∧ filings(a) ≥ 1`) → **active** — the holder
   has filed at least one attest of any kind.

Every input is an existing substrate row; no clocks, no content reads,
no new stored state. Edges are NOT enumerated: any (from,to) pair the
function can produce across one substrate write is legal (e.g. a
completion attest as the first-ever filing yields open→claims-done,
never passing through active; a completion closing an assignment that
already carries a `verified` verdict yields open/active→verified,
never passing through claims-done). Consumers MUST NOT assume a
transition graph — there is no state machine, only a function sampled
before and after facts change.

## Schema (two additive tables — one per grain; repo migration conventions)

Assignment-grain doorbell log (UNCHANGED from r3):

    CREATE TABLE IF NOT EXISTS work_state_events (
      id           INTEGER PRIMARY KEY AUTOINCREMENT,  -- THE assignment cursor
      ts           INTEGER NOT NULL,
      assignmentId TEXT    NOT NULL REFERENCES assignments(id),
      fromState    TEXT,                               -- NULL = creation
      toState      TEXT    NOT NULL,
      CHECK (fromState IS NULL OR fromState IN
        ('open','active','stranded','claims-done','verified','abandoned')),
      CHECK (toState IN
        ('open','active','stranded','claims-done','verified','abandoned'))
    );
    CREATE INDEX IF NOT EXISTS work_state_events_assignment
      ON work_state_events (assignmentId, id);

Work-item-grain doorbell log (NEW, additive):

    CREATE TABLE IF NOT EXISTS work_item_events (
      id           INTEGER PRIMARY KEY AUTOINCREMENT,  -- THE work-item cursor
      ts           INTEGER NOT NULL,
      workItemId   TEXT    NOT NULL REFERENCES work_items(id),
      kind         TEXT    NOT NULL,
      CHECK (kind IN ('metadata','composition'))
    );
    CREATE INDEX IF NOT EXISTS work_item_events_item
      ON work_item_events (workItemId, id);

Each table's AUTOINCREMENT integer id is that grain's cursor — the
same seq discipline as `messages.seq`, `turns.seq`, and `events.id`
(monotone across deletes and restarts by AUTOINCREMENT semantics;
verified pattern at projection.ex:34, ledger.ex:39, event_log.ex:40).
Two grains, two independent monotone cursors: a consumer that spans
both grains tracks both high-waters (§Query surface, §client contract);
an assignment-only view tracks only the assignment cursor. The
work-item-grain event carries NO from/to and NO state — a work-item
has no substrate status; the row records only THAT the item changed
and how (metadata vs composition), a pure "re-query this item"
doorbell.

LOAD-BEARING INVARIANT — NEITHER table is ever state: no code path
reads either to answer a status or composition question. The substrate
reads them for exactly two purposes: minting/reporting each grain's
high-water cursor (`MAX(id)`) and forensics. The status function
consults only assignments/attests/sessions rows; work-item queries
consult only work_items/assignments/attests/sessions rows. Emitters
compute an assignment's fromState from TRUTH (the status function,
pre-write), never from the last row here; work-item emitters record a
change the domain write already made, never derive it back from the
log. This is what makes a lost or wrong event row harmless by
construction on BOTH grains — the pathology the ticket-as-object
design died of (a second copy of reality) is structurally impossible.

## The thin events (wire schemas — one frame type per grain)

Two new frame types, both pushed on the existing socket, both in the
`work_state` subscription class (§Per-connection filter). Both are
DOORBELLS — "re-query this ref" — never a second copy of state.

Assignment-grain (UNCHANGED from r3):

    {"type": "work_state_event", "ref": "<assignmentId>",
     "sessionKey": "<holderKey>", "from": <state|null>,
     "to": <state>, "cursor": <id>, "ts": <ms>}

NO payload. `ref` names the assignment; `sessionKey` names the holder
so a chat client can interlace the event between that stream's bubbles
and a board can group by holder; `cursor` is the `work_state_events.id`
minted by the emission insert. A work-item-grain view routes this
doorbell by the assignment→item mapping it already holds from its last
query (each assignment row carries `workItemId`, §Query surface) — the
frame is not widened to carry `workItemId` (it is a doorbell; the view
re-queries).

Work-item-grain (NEW):

    {"type": "work_item_event", "ref": "<workItemId>",
     "kind": "metadata"|"composition", "cursor": <id>, "ts": <ms>}

NO payload, NO from/to. `ref` names the changed work item; `kind`
says what changed — `metadata` (title or spec-ref pin patched via
work-item-update) or `composition` (an assignment was linked to this
item, i.e. its `workItemId` was set). `cursor` is the
`work_item_events.id` minted by the emission insert. Detail is a query
at click time (§Query surface), never in the frame. Add
`Payloads.work_state_event/1` and `Payloads.work_item_event/1` beside
the existing payload builders (payloads.ex; camelCase keys, same
conventions).

Delivery contract (BOTH grains): frames are best-effort doorbells.
They may be lost (crash/disconnect), duplicated, or — rarely, across
two concurrent emitters — pushed out of cursor order. Each grain's
cursor governs the snapshot join and dedupe for its own grain, NOT
total ordering across grains. The CLIENT CONTRACT (normative for any
consumer): (1) subscribe first — meaning the socket subscription is
SUCCESSFULLY ESTABLISHED (the `auth_result` success frame received,
i.e. the connection is registered) BEFORE beginning the HTTP snapshot
request(s); auth sent but unacknowledged does not count, because frames
emitted in that window are not guaranteed delivered — then buffer; (2)
snapshot each grain the view uses; (3) for each grain, discard
buffered/arriving events of THAT grain with `cursor <=
snapshot.cursor[grain]`; (4) for a live event, either refetch the ref
(always correct) or, on the assignment grain only, apply `to` directly
IFF `from` matches the consumer's current view of that ref — on any
mismatch, refetch the ref or re-snapshot; a work_item_event carries no
state to apply, so it is always a refetch of its ref. Convergence
claim, stated honestly and identically per grain: duplication and
reordering are fully neutralized by steps 3–4; LOSS is not signaled —
a dropped post-snapshot event (in particular a dropped FINAL
assignment edge, or a dropped composition doorbell) leaves the
consumer stale, with no automatic prompt to refetch, until its NEXT
read (any refetch of that ref, or the reconnect/refresh snapshot), at
which point it converges unconditionally because reads compute from
table truth. The self-heal is "the next read recomputes", never
"always converges promptly"; the loss test includes that later read
explicitly, on both grains (§Tests).

## Emission (sites, mechanics — all best-effort, all cold-path)

Assignment-grain emission = compute `from := status(ref)` BEFORE the
domain write, `to := status(ref)` AFTER it commits; if `from ≠ to` (or
creation), INSERT the work_state_events row, then push the
work_state_event frame. Work-item-grain emission = after a work-item
metadata write or an assignment→item link commits, INSERT a
work_item_events row and push the work_item_event frame; there is no
from/to to compute — the caller emits only when the write actually
changed something (below). Both run as the LAST statement of the
success branch of each site's handler, AFTER the domain transaction
commits, NEVER inside it, wrapped in a total catch (statute-engine
style: rescue + catch exit/throw) — an emission failure never fails the
verb, and no verb result depends on it. The pinned mechanics:

- SUCCESS BRANCH, exactly: the attest-module and work-item-module
  handlers signal denial by returning an error map `%{code: ...,
  message: ...}` (assignments.ex denial pattern) from inside the same
  `transaction/2` wrapper as success. The emission branch must EXCLUDE
  every such denial return — emit only when the handler's result is the
  success shape (the assignment/attest/work-item response map), never
  when it carries a `code` key. A denied verb changed nothing; it emits
  nothing.
- TRANSACTION SEAM, unchanged: attest r5's and work-item-v1's
  one-transaction-per-verb mutation seam (`transaction(db, fn txn ->
  ... end)`) is preserved verbatim — no emission code moves inside a
  txn closure. The insert+push happens after `DB.transaction/2` returns
  success, in the handler, best-effort.

A crash between commit and emission loses a doorbell on either grain;
harmless — truth is in the tables and the next snapshot shows it (at
the cost stated in §client contract: staleness until the consumer's
next read).

Assignment-grain sites — exactly the verbs that move the status
function's inputs, all existing handlers, no hot-path hooks (no
Ledger/SessionLane/Wake seams; see §Open ruling for the deliberate
consequence):

- `assign` (attest's handler, work-item-extended): emit `{from: null,
  to: 'open'}` — a fresh assignment is always open (zero filings; the
  handler already refuses retired holders). PINNED: an idempotent
  replay (idempotency-key hit) returns the EXISTING assignment
  (attest's `idempotency_assignment` → `fetch_assignment!`, short-
  circuiting before work-item validation per work-item-v1) — it creates
  nothing and must emit NO false null→open creation event. Thread a
  created-vs-replayed distinction out of the assign transaction
  (internal only — the wire response is unchanged) and emit only on
  created. Tested (§Tests).
- `attest` (attest's handler, check-tier-extended): first filing of
  kind progress flips open→active; a completion → claims-done, OR →
  verified when a `verdictKind='verified'` verdict already exists on
  the assignment (branch 2); surrender → abandoned. A `verdict` filing
  (check-tier) leaves the assignment OPEN and, being one more filing,
  never changes the status of an already-active assignment (from = to =
  active → NO row, NO frame) and flips open→active as a first filing;
  it is a completion, not a verdict, that later realizes `verified`. A
  progress or verdict attest when already active computes from = to →
  NO row, NO frame (counter resets and repeat filings are not state
  edges).
- `revoke-assignment` (attest's handler): → abandoned (from may be
  open, active, or stranded — compute, don't assume).
- `retire` (gateway's `retire_result`, active branch — at ac60d09 the
  branch that calls `Org.retire`; after supervision merges it is the
  same site that invokes supervision's `:on_retired` closure, and
  emission goes immediately after that closure invocation): for EACH of
  the retiring session's open assignments (attest's `Assignments.list`,
  open filter, holder = key), emit `{from: open|active, to:
  'stranded'}`. PINNED ORDERING — capture BEFORE retire: each
  assignment's pre-state (`status/2`: open|active) MUST be captured
  BEFORE `Org.retire` runs; querying status after retirement returns
  stranded for every open assignment, making `from == to` and emitting
  nothing. The handler collects `[{assignment_id, pre_state}]` first,
  retires, then emits per pair. This deliberately does NOT touch
  `Tightbeam.Supervision` or its doorbell — supervision's
  `supervision_stranded` lifecycle row keeps its own (optional,
  strandedAt-deduped) life; this event class is the UI wire's, and the
  two enumerate independently. Scope discipline: supervision's module
  is not modified.

Work-item-grain sites — exactly the verbs that change work-item
metadata or item↔assignment composition, all existing handlers:

- `work-item-update` (work-item-v1's handler): emit `{kind:
  'metadata'}` for the item — ONLY when the patch actually changed a
  column. work-item-v1 makes an empty or same-values patch a state-
  idempotent no-op returning the current row; capture the row's
  metadata (title, specRefName, specRefSha256) BEFORE the update and
  compare AFTER — emit iff any of the three changed. A no-op patch
  emits nothing (filter unchanged, mirroring the assignment grain's
  from == to rule).
- `assign` with a `workItemId` (attest's work-item-extended handler,
  create path only): emit `{kind: 'composition'}` for that work item —
  the item gained an assignment. Emit ONLY when the assignment was
  CREATED (not on idempotent replay, whose original workItemId is
  returned unchanged — work-item-v1 §Verbs) AND `workItemId` is
  non-null. A created assignment WITH a work item therefore emits TWO
  doorbells at this site: the assignment-grain `{from: null, to:
  'open'}` AND the work-item-grain `{kind: 'composition'}` — both
  post-commit, both best-effort, independent. v1 sets `workItemId` only
  at assign time (work-item-v1 has no relink verb); should a future
  verb change an existing assignment's `workItemId`, that site emits
  `composition` the same way — the trigger is "an assignment's
  `workItemId` is set or changes." Closing, revoking, surrendering, or
  progressing an assignment does NOT change its `workItemId` and emits
  NO composition event; a work-item view learns those via the
  assignment-grain status edge for the assignment it is tracking.

No sweep, no backfill, no startup reconciliation on either grain:
events missed while the gateway (or a consumer) was down are healed by
the consumer's reconnect snapshot — that is the whole recovery story,
by design.

New module `Tightbeam.WorkState` (lib/tightbeam/work_state.ex) owns
`ensure_schema/1` (registered in `Gateway.children/1`'s ensure_schema
list AFTER work_items' and assignments' — both referenced tables must
exist first, foreign_keys=ON), the status derivation, the queries for
both grains, and the emit halves. The frame push composes in the
gateway like `publish_message` does (gateway.ex `publish_message`
site): small private helpers that build `Payloads.work_state_event/1`
/ `Payloads.work_item_event/1` and call the new registry publishers
(below), fanned out per §Per-connection filter.

Public API (no other surface):
- `WorkState.status(db, assignment_id) :: state | nil` — nil for
  unknown id; the assignment emitters' pre/post read.
- `WorkState.list(db, filters) :: %{work: [...], cursor: int}` — the
  assignment-grain snapshot (§Query surface); rows and cursor read
  atomically in ONE `DB.transaction/2`, so they are mutually
  consistent. `cursor` = `MAX(work_state_events.id)`.
- `WorkState.detail(db, assignment_id) :: map | nil` — the
  assignment-grain detail, assembled atomically in ONE `DB.transaction/2`
  (§Query surface pins its cursor semantics).
- `WorkState.list_items(db, filters) :: %{items: [...], cursor:
  %{assignment: int, work_item: int}} ` — the work-item-grain snapshot:
  item metadata plus each item's assignments with derived status, and
  BOTH grains' high-water cursors, all read atomically in ONE
  `DB.transaction/2`.
- `WorkState.item_detail(db, work_item_id) :: map | nil` — the
  work-item-grain detail, assembled atomically in ONE `DB.transaction/2`.
- `WorkState.emit(db, assignment_id, from) :: event_map | nil` —
  computes `to`, inserts iff edge; returns the inserted event map (the
  push helper's input) when a row was written, `nil` when there is no
  edge (`from == to`, non-creation). NOT `:ok` — the caller branches on
  the return to decide whether to push a frame; total catch at the call
  sites.
- `WorkState.emit_item(db, work_item_id, kind) :: event_map` — inserts
  one work_item_events row of `kind` and returns the event map (the
  push helper's input). The caller has already decided a change
  occurred (§Emission: work-item-update compares pre/post; assign emits
  only on created + non-null workItemId), so this always inserts;
  total catch at the call sites.

## Per-connection filter (the wire contract)

The auth frame gains ONE additive optional field, `subscriptions`: an
array from the CLOSED two-class vocabulary — extension is a spec
revision:

- `"chat"` — everything the wire pushes today: messages, turn state,
  typing, activity, stream_* frames, markers included. Both existing
  registry fan-out entry points (`publish_message`, `broadcast`) are
  hereby classed "chat".
- `"work_state"` — the derived-observability doorbells: BOTH
  `work_state_event` (assignment grain) AND `work_item_event`
  (work-item grain) frames. One class carries both grains; a view
  subscribes once and filters by frame `type` for the grain(s) it
  renders. (Two grains, one subscription class — the class is
  "observability doorbells," not "one grain.")

Absent → `["chat"]`: an existing client's connection is
BYTE-IDENTICAL to today (frames, order, replay — the E0 discipline);
protocolVersion stays 1. Empty array or any unknown class →
`wire_error "invalid_message"` + close. PINNED ORDERING — fail
closed FIRST: subscription parsing/validation is the first act of
the auth success path, BEFORE `seed_main_stream` AND BEFORE
`ConnRegistry.register` (at ac60d09 those run back-to-back,
socket.ex:263-266; validation goes in front of both). An invalid
subscriptions field must cause zero side effects: no org material
seeded, no registration, no replay. Kanban-of-assignments sends
`["work_state"]` and renders `work_state_event`; a work-item board
sends `["work_state"]` and renders `work_item_event` (and re-queries
assignments on the assignment edges it cares about); a state-aware
clawline sends `["chat","work_state"]` and interlaces the frames
between bubbles by `sessionKey` — all client concerns; the substrate
only delivers.

Socket flow for a connection WITHOUT "chat": auth → auth_result
(replay_count 0, replay_truncated false, session_keys [], empty
read/tail states — same shape, empty collections) → NO
stream_snapshot, NO message replay → sync_complete → live. It skips
`seed_main_stream` (a state-only consumer must not mutate org
material) and never receives chat-class frames. INBOUND GATING
(pinned — without it the "never mutates" claim is false): at
ac60d09 the post-auth inbound routes accept `message`, `stream_read`,
and `typing` unconditionally (socket.ex:179-198) — `message` mutates
org/projection material and `stream_read` writes read state and
echoes a chat-class `stream_read_state` frame. On a connection
WITHOUT "chat", every chat-class inbound frame (`message`,
`stream_read`, `typing`) is REFUSED with `wire_error
"invalid_message"` (the existing unsupported-type response,
socket.ex:201-206; connection stays open, nothing written).
RE-AUTH AND PAIRING (pinned — without this the gating is
bypassable): at ac60d09 `route/2` matches `auth` and `pair_request`
in EVERY phase, before any gate (socket.ex:172-173), so a re-auth
with `subscriptions` absent would default to `["chat"]` and run
`seed_main_stream` — silently converting a state-only connection.
Therefore the subscription class is a CONNECTION-LIFETIME property,
fixed by the FIRST successful auth: a subsequent `auth` frame on an
already-authed connection re-validates credentials but PRESERVES
the established subscription set, and performs NO re-registration
(the existing conn entry and its subscriptions stand — re-registering
would drive `ConnRegistry.register`'s same-device takeover against the
connection itself and self-close it; the preserving re-auth must not
re-register). The absent → `["chat"]` default applies ONLY to the
initial auth; on re-auth, an absent `subscriptions` field keeps the
current set, a present field equal to the current set is a no-op, and
a present field that DIFFERS → `wire_error "invalid_message"` + close
(changing class requires a new connection). A re-auth on a connection
WITHOUT "chat" runs NO `seed_main_stream`, NO stream_snapshot, NO
replay — a work-state-only connection stays work-state-only for its
lifetime and never silently becomes chat. `pair_request` keeps today's
behavior on every connection class (device pairing is its own
pre-existing surface, unchanged by this spec; its device-row write
is pairing material, not chat/org material). The never-mutates
claim, stated precisely: a state-only connection never mutates ORG,
PROJECTION, or READ-STATE material and never receives chat-class
frames — both directions gated, re-auth included, all tested.
Connections WITH "chat" keep today's flow exactly, plus (if also
subscribed) work_state frames — including today's re-auth behavior,
which for a default connection is unchanged (its preserved set IS
the default `["chat"]`). State frames ride the socket's untagged `{:push,
payload}` path (buffered during replay, drained unfiltered —
socket.ex:101-136): the socket-side seq watermark is for message
replay dedupe; state-event dedupe belongs to the CLIENT's per-grain
cursor rule, not the socket.

ConnRegistry changes (conn_registry.ex): the register conn map gains
`:subscriptions` (a set; the socket passes it from auth).
`publish_message` and `broadcast` deliver only to "chat" subscribers
(today's callers are unaffected — every default connection is
"chat"). New `publish_work_state(server, owner_user_id, payload,
deliver)` — same shape as `broadcast`, delivering to connections
where `user_id == owner` AND "work_state" ∈ subscriptions — used for
`work_state_event` frames, scoped to the assignment holder's
ownerUserId. New `publish_work_item(server, owner_user_ids, payload,
deliver)` — same shape, delivering to connections where `user_id ∈
owner_user_ids` AND "work_state" ∈ subscriptions — used for
`work_item_event` frames; the owner-id SET is the distinct ownerUserId
over the item's current assignment holders, computed by the gateway
push helper at emit time (for `composition`, that set necessarily
includes the just-linked holder's owner; for `metadata` on an item
with zero assignments the set is empty and nothing is delivered —
harmless, the next HTTP re-query heals). Fan-out scoping deliberately
mirrors `broadcast` (owner-only, no admin widening —
conn_registry.ex:154-157); admins read everything via the HTTP query
surface instead. Revisit under multi-user as policy, not now.

## Query surface (random access; reads query directly, per the router convention)

Four GET routes on the existing router (router.ex — "Reads query
directly"; device Bearer auth; errors in the existing
`{"error":{code,message?}}` envelope). Two serve the ASSIGNMENT grain
(unchanged from r3) and two serve the WORK-ITEM grain (new). A view
uses whichever grain(s) it renders.

ASSIGNMENT GRAIN:

- `GET /api/work?status=S1,S2&state=open|closed|all&sessionKey=K`
  → `{"work": [...], "cursor": <int>}`.
  Each element: the assignment response shape (verbatim, camelCase —
  attest r5 fields PLUS work-item-v1's additive `workItemId`, null when
  unlinked) PLUS `"status": <state>` and `"holderState":
  "active"|"retired"`. The `workItemId` on each row is what lets a
  work-item view map an assignment-grain doorbell to its item without
  widening the frame. Filters are DUMB filter inputs over
  substrate-owned material (the boundary rule): `status` — optional
  comma-separated list from the six-state vocabulary, unknown value →
  400 `invalid_status`; `state` — the raw assignment column filter,
  default `all` (a board needs closed rows for its claims-done /
  verified / abandoned lanes), invalid → 400 `invalid_state_filter`
  (attest's code); `sessionKey` — optional holder filter, matched as a
  dumb string against holderKey: an unknown key yields an empty list,
  not 404 (it is a filter, not a target resolution; no role param — see
  §Non-goals). Ordering: openedAt DESC, id DESC (attest's tie-break
  discipline). No pagination in v1.
  `cursor` = `MAX(work_state_events.id)` (0 when none), read in the
  SAME `DB.transaction/2` as the rows (`WorkState.list`), pinning the
  join invariant: every assignment event with `id <= cursor` is already
  reflected in the returned rows. (The converse race — a domain write
  committed, its event not yet inserted at snapshot time — yields a
  snapshot that already shows the new truth and a later event with
  `id > cursor`; the client's apply-or-refetch is idempotent.
  Harmless, stated.)
  Visibility: non-admin devices see assignments whose holder session's
  ownerUserId is the device user; admins see all — mirroring `GET
  /api/session-status` (owner or admin), the existing device-route
  convention.

- `GET /api/work/:id` — the assignment detail view, the click-time
  query ("the assignment" is this response, assembled fresh from
  tables):
  `{"assignment": <assignment shape + "status" + "holderState">,
    "attests": [<attest r5/check-tier shape (incl. verdictKind)... ts
      ASC, id ASC>],
    "supervision": <the assignment_prods row — attemptCount, prodCount,
      deniedStreak, attestCount, lastProdAt, stalledAt, strandedAt — or
      null when no row>,
    "holder": {"sessionKey", "state", "displayName"},
    "cursor": <int>}`.
  Unknown id, or non-admin caller not owning the holder session →
  404 `unknown_assignment` (attest's code). The supervision block is
  a raw row projection — counters as facts, no interpretation.
  DETAIL CURSOR SEMANTICS (pinned): `cursor` is the GLOBAL assignment
  high-water `MAX(work_state_events.id)` (0 when none), and the whole
  detail response is assembled atomically in ONE `DB.transaction/2`
  (`WorkState.detail`), exactly the list-snapshot discipline. Its join
  guarantee is REF-SCOPED: every assignment event with `ref == :id ∧ id
  <= cursor` is reflected in this response. A client may therefore
  discard buffered/arriving ASSIGNMENT events FOR THIS REF with `cursor
  <= detail.cursor`; it MUST NOT discard events for OTHER refs against
  a detail cursor. Only the full assignment-list snapshot licenses
  global assignment-grain discard.

WORK-ITEM GRAIN (new — item metadata + its assignments-with-status,
NO substrate item-status):

- `GET /api/work-items?sessionKey=K`
  → `{"items": [...], "cursor": {"assignment": <int>, "workItem":
  <int>}}`.
  Each element: `{"workItem": <work-item-v1 shape: id, title,
  specRefName, specRefSha256, createdByUser, createdBySession,
  createdAt>, "assignments": [<assignment shape + "status" +
  "holderState">... openedAt DESC, id DESC]}` — the item's metadata
  plus EVERY assignment referencing it, each carrying its derived
  per-assignment status. The substrate computes NO item-level aggregate
  status: worst-status-wins / "done when all closed" / any roll-up is
  VIEW-SIDE policy (§Design position); the view aggregates the
  per-assignment statuses it is handed however it chooses. `sessionKey`
  is a dumb optional filter restricting to items that HAVE an
  assignment held by K (unknown key → empty list). Ordering: items by
  createdAt DESC, id DESC (work-item-v1's tie-break); assignments
  within an item by openedAt DESC, id DESC. No pagination in v1.
  BOTH cursors are returned and read in the SAME `DB.transaction/2` as
  the rows (`WorkState.list_items`): `assignment` =
  `MAX(work_state_events.id)`, `workItem` = `MAX(work_item_events.id)`
  (each 0 when none). Join invariant, per grain: every work_item event
  with `id <= cursor.workItem` and every assignment event with `id <=
  cursor.assignment` is reflected in the returned rows. A work-item
  view tracks BOTH high-waters and dedupes each grain's frames against
  the matching cursor.
  Visibility: non-admin devices see items that have at least one
  assignment whose holder ownerUserId is the device user; admins see
  all (mirroring the assignment-grain owner-or-admin rule). An item
  with zero visible assignments is not shown to a non-admin (there is
  nothing it owns on that item); admins see all items including
  assignment-less ones.

- `GET /api/work-items/:id` — the work-item detail view, the
  click-time query ("the work item" is this response, assembled fresh
  from tables):
  `{"workItem": <work-item-v1 shape>,
    "assignments": [<assignment shape + "status" + "holderState">...
      openedAt DESC, id DESC],
    "cursor": {"assignment": <int>, "workItem": <int>}}`.
  Every assignment referencing the item, each with derived status; NO
  aggregate item status (§Design position). To drill from here into one
  assignment's attests and supervision counters, the view calls `GET
  /api/work/:id` — the two detail routes compose, each grain owning its
  own depth. Unknown id, or non-admin caller owning none of the item's
  assignment holders → 404 `unknown_work_item` (work-item-v1's code).
  DETAIL CURSOR SEMANTICS (pinned): both cursors are GLOBAL
  high-waters (`MAX` over each events table, 0 when none), and the
  whole response is assembled atomically in ONE `DB.transaction/2`
  (`WorkState.item_detail`). Ref-scoped join, per grain: every
  work_item event with `ref == :id ∧ id <= cursor.workItem`, and every
  assignment event whose assignment is one of THIS item's assignments
  with `id <= cursor.assignment`, is reflected. A client may discard
  buffered/arriving work_item events FOR THIS ITEM with `cursor <=
  cursor.workItem`, and assignment events for THIS ITEM's assignments
  with `cursor <= cursor.assignment`; it MUST NOT discard events for
  other items/assignments against a detail cursor. Only a full
  grain-list snapshot licenses global discard of that grain.

The `/agent`-side `assignments`, `work-item-get`, and `work-item-list`
verbs keep their own attest/work-item all-rows rulings; the device
routes here follow the device-route owner-or-admin convention — two
surfaces, each following its own established convention (stated, not
changed).

## Invariants (acceptance lens)

1. Status is a per-assignment VIEW: total, deterministic, judgment-
   free, computed from assignments/attests/sessions rows only.
   `work_state_events` is never read to answer status — delete every
   row in it and every status answer, and every NON-CURSOR field of
   every list/detail response, is unchanged (tested exactly so). A
   work-item has NO substrate status: the work-item queries derive only
   the per-assignment statuses they attach; no item-level aggregate is
   computed or stored. The `cursor` fields necessarily change when an
   events table is emptied (N → 0 — `MAX` over an emptied table); that
   is the cursor doing its job, not events feeding a view.
2. Thin events are doorbells with no correctness job on BOTH grains:
   duplication and reordering are neutralized outright by the client
   contract; loss leaves a contract-following consumer stale only until
   its next read, which reconverges it with table truth via idempotent
   refetch. Nothing in the substrate branches on an event row existing,
   in either table — delete every row in BOTH `work_state_events` and
   `work_item_events` and every non-cursor field of every response is
   unchanged.
3. One wire, typed classes, per-connection filter: a default
   (subscriptions-absent) connection is byte-identical to main ac60d09
   behavior; protocolVersion unchanged. Both grains' doorbells ride the
   single `work_state` subscription class.
4. Each grain's cursor joins query and stream: subscribe-first
   (registration ACKed) → snapshot → discard ≤ that grain's high-water
   is race-free by the one-transaction snapshot invariant (§Query
   surface). A cross-grain view tracks both high-waters.
5. The grain boundary holds: the substrate chooses NO card unit,
   defines NO board concept (columns, priorities, readiness,
   orderings), and computes NO item-level status aggregate; it exposes
   both model entities random-accessibly with mechanical per-assignment
   status and pure change doorbells, and filters are dumb inputs. Any
   summarization is view-side.
6. Closed vocabularies: six assignment states, two work_item_event
   kinds (metadata, composition), two subscription classes, edges
   unenumerated. `verified` is now LIVE — check-tier is merged at
   ac60d09, so the branch evaluates real `verdictKind` SQL; the r3
   constant-false form is retired.
7. Zero behavior change to every existing verb, frame, and client; a
   pre-existing DB boots unchanged (two additive tables). Emission is
   cold-path only (four assignment-grain verb handlers + two
   work-item-grain sites); no hot-path (turn/wake) hooks exist in this
   build.

## Tests (condensed contract — cover every clause)

Status function: one fixture matrix covering ALL SIX branches and the
precedence order — notably closed-completed and closed-revoked with a
RETIRED holder → claims-done / abandoned, never stranded; the
derived-stranded query test mirrors supervision's (open + retire
holder, no events emitted, no sweep → status = stranded; close it →
not). `verified` is now REACHABLE and its positive test is ACTIVE (no
longer pending-check-tier): file a `kind='verdict', verdictKind='verified'`
attest while the assignment is OPEN, then a completion closing it →
status `verified`; a completion with NO verdict, or with only a
DIFFERENT verdictKind (e.g. `tests-passed`) → `claims-done` (branch 2's
string-exact predicate: only `verified` counts). Assert the derivation
executes real `verdictKind` SQL against the ac60d09 schema and the full
matrix runs green (the r3 no-such-column guard is moot — the column
exists). Unknown id → nil.
Never-read invariant (BOTH tables): perform a full lifecycle across
both grains, snapshot every list/detail response, DELETE all
`work_state_events` AND all `work_item_events` rows, then assert every
status answer AND every NON-CURSOR field of every list/detail response
(assignment and work-item grains) is unchanged, and the `cursor`
fields read 0 (they necessarily drop from N — asserting them unchanged
is impossible and wrong).
Assignment emission: one event per edge at each site — assign
(null→open); assign REPLAY with the same idempotency key (existing
assignment returned, NO row, NO frame); first progress (open→active);
second progress (NO row, NO frame); a `verdict` filing on an active
assignment (from == to = active → NO row, NO frame) and as a first
filing (open→active); completion after progress with no verdict
(active→claims-done); completion after a `verified` verdict
(active→verified, or open→verified as first filing — edges
unenumerated); completion as first filing with no verdict
(open→claims-done); surrender; revoke from open, from active, and from
stranded; a DENIED verb (e.g. attest on a closed assignment →
`%{code: ...}`) emits NO row, NO frame; retire with two open
assignments — one zero-filing, one with a progress attest — → exactly
two assignment events with `from` = open and active respectively
(proving pre-states are captured BEFORE `Org.retire`), closed
assignments untouched. `emit/3` returns the event map on an edge and
nil on no-edge.
Work-item emission: work-item-update that changes the title, and one
that changes the spec-ref pin → exactly one `{kind:'metadata'}` event
each; a no-op / empty patch (work-item-v1's state-idempotent no-op) →
NO row, NO frame (filter-unchanged, pre/post compared); assign WITH a
`workItemId` on the create path → exactly one `{kind:'composition'}`
event AND (same site) one assignment `{null→open}` event — two
independent doorbells; assign WITHOUT a workItemId → NO composition
event; assign REPLAY carrying a workItemId (idempotency hit returns the
original) → NO composition event, NO assignment event; closing /
revoking / progressing a linked assignment → NO composition event
(workItemId unchanged). `emit_item/3` returns the event map.
Both grains post-commit and total-caught: an injected emission failure
(e.g. registry down) leaves the verb result and domain rows correct on
both grains.
Cursors: within each table ids strictly increase across emissions;
each frame `cursor` equals its inserted row id; the two tables' cursors
are independent sequences.
Assignment snapshot: rows+cursor from one `DB.transaction/2`; after N
emissions, `cursor` ≥ every assignment event reflected in rows (the
join invariant, under a concurrent-write interleave); filters — each
status value, comma list, invalid → 400 invalid_status; state
open/closed/all + default all; sessionKey filter and unknown key →
empty list; ordering with equal openedAt; each row carries workItemId
(null and non-null).
Work-item snapshot: items + assignments-with-status + BOTH cursors from
one `DB.transaction/2`; an item with two open assignments held by
different sessions (concurrent aspects) → both returned with their
statuses, NO aggregate status field present; a re-staffing item (assign
→ revoke → assign same item) → all three assignment rows with statuses
abandoned/…/open; item ordering createdAt DESC id DESC, assignment
ordering openedAt DESC id DESC; sessionKey filter restricts to items
with an assignment held by K, unknown key → empty; the assignment
high-water and work-item high-water each ≥ their reflected events under
a concurrent interleave.
Detail (assignment): full shape with and without an assignment_prods
row; attest ordering incl. a verdict row's verdictKind projected;
unknown id and non-owner non-admin → 404; admin sees all; owner-scoping
on the list route likewise; assembled in one `DB.transaction/2` with
`cursor` = global assignment MAX and the ref-scoped join.
Detail (work-item): full shape — item + assignments-with-status + both
cursors — assembled in one `DB.transaction/2`; unknown id and a
non-admin owning none of the item's assignment holders → 404
unknown_work_item; admin sees all; the ref-scoped joins hold per grain
(every work_item event for `:id` and every assignment event for THIS
item's assignments, each ≤ its cursor, reflected; a concurrent emission
on ANOTHER item/assignment may land ≤ a cursor without appearing —
asserting ref-scoped, not global). NO aggregate item status field.
Wire: default-auth regression — a subscriptions-less connection
produces today's exact frame sequence (auth_result, stream_snapshot,
replay, sync_complete; no work_state or work_item frames ever);
work_state-only connection — auth_result with empty collections, no
stream_snapshot, no replay, no seed_main_stream call, sync_complete,
then receives BOTH work_state_event and work_item_event frames and
NEVER receives message / typing / turn-state / stream_* / marker
frames; inbound gating — a work_state-only connection sending
`message`, `stream_read`, or `typing` gets `wire_error invalid_message`
per frame, the connection stays open, and NO row is written; re-auth
class preservation — a work-state-only connection sending a second
`auth` with `subscriptions` absent, and again with `["work_state"]`,
keeps its class with NO re-registration/self-close: NO seed_main_stream,
NO stream_snapshot, NO replay, both grains' state frames still
delivered; a second `auth` with a DIFFERING set (e.g. `["chat"]`) →
invalid_message + close; a default (subscriptions-absent) connection's
re-auth behaves exactly as at ac60d09 (regression); chat+work_state
receives chat frames plus both grains' state frames interlaced; empty
subscriptions array and unknown class → invalid_message + close,
unregistered, AND no seed_main_stream side effects (validation precedes
seeding and registration); fan-out scoping — an other-owner subscribed
connection receives neither grain's frames; an admin non-owner
connection receives no frames (broadcast-mirror) but reads the rows over
HTTP; a work_item_event for an item whose assignments span two owners
reaches each owning subscriber; a metadata change on an
assignment-less item delivers to nobody (empty owner set) and heals on
next HTTP read.
Self-healing (the contract test, client simulated, BOTH grains): under
duplicated and cursor-reordered frame deliveries per grain, a consumer
implementing §client contract (assignment: apply-iff-from-matches else
refetch; work-item: always refetch) ends every schedule equal to table
truth; under DROPPED deliveries — including a dropped FINAL assignment
edge and a dropped composition doorbell — assert the honest shape: the
consumer is STALE after the drop (no signal arrives), and a subsequent
explicit read (ref refetch or re-snapshot, part of the test schedule)
reconverges it with table truth.
Registry: publish_message/broadcast deliver to chat subscribers only;
publish_work_state to work_state subscribers of the holder's owner
only; publish_work_item to work_state subscribers whose user is in the
item's owner set only.

## Build ordering & handoff

Cut the worktree from main AFTER supervision-impl-v1 (r17) merges
(transitively: attest, work-item, check-tier, session-tokens,
statute-engine, cli-rust). Baseline as verified at ac60d09: attest's
schema and atomic handlers, work-item-v1's `work_items` table +
nullable `workItemId` on assignments + work-item verbs, and
check-tier's `verdict` kind + `verdictKind` column are ALL PRESENT;
`assignment_prods`, `Tightbeam.Supervision`, and the `:on_retired`
seam are ABSENT (supervision not yet merged) — so the STOP gate below
correctly fires today and clears only after the supervision merge. If
`assignments`/`attests`, `work_items`/`workItemId`, `verdictKind`,
`assignment_prods`, or the gateway retire-site `:on_retired` seam are
absent from main at build time, STOP and report — do not vendor around
them. Supervision's stamps (`assignment_prods`) feed the assignment
detail view; its retire seam locates one assignment-grain emission
site. Supervision r17's cascade-boundedness rewrite and its
`reresolveSeed`/`reresolveRung` wake columns do not touch the consumed
`assignment_prods` columns or the `:on_retired` closure — both survive
r17.

Gates: `mix compile --warnings-as-errors` clean; full `mix test`
green (cli/ untouched — no cargo gate). Commit on the branch; do not
merge. STOP and report on any conflict with existing code, with
attest / work-item / check-tier as merged or supervision as merged, or
with this spec.

## Open ruling (Flynn-level, ruled r1, upheld by the r1 review)

`active` is derived from FILINGS (≥1 attest row), not from a running
turn. Chosen because every input stays assignment-scoped and every
edge lands in a cold-path verb handler — the alternative ("holder has
a running/queued turn or pending wake", supervision's idle conjuncts
negated) is equally mechanical but needs hooks at turn-enqueue (hot
path, several gateway sites) and makes all of one holder's cards
flip together on every turn. Consequence: the board shows
open/active by work-record, and "working right now" remains the chat
wire's turn-state frames. If Flynn wants turn-liveness ON the board,
that is a revision adding states + hot-path emission sites — flag,
don't improvise.

## Addendum phase — row-family emission audit (Flynn-directed; READY, gate-cleared 2026-07-25 after 5 Sol-high rounds)

Flynn's question: have we been consistent about emitting row writes to the clawline
stream? Answer: mostly by design, twice by omission. This addendum is the disposition
table — every persisted row family, its carriers AT ROW-WRITE GRANULARITY (r1 review:
family-level "covered" hid silent mutations), and whether each silence is a decision or
a hole — plus the two closures. Emission mechanics for anything added here follow
§Emission verbatim: cold-path, best-effort, success-branch only, after the domain
transaction commits, total catch.

Carrier vocabulary: DIRECT = a wire frame pushed at the write; CHAT = the write
materializes a chat message/turn that reaches the stream as `server_message` (a
legitimate carrier under the grain-agnostic ruling — this is the same carrier decision
requests and supervision prods use, and it applies equally where wakes fire into
turns); QUERY = no push, truth reachable through a verb; SILENT = none of these.

### Disposition table (row families; silent mutations named, not averaged away)

| Row family | Carriers by mutation | Disposition |
|---|---|---|
| messages | live chat writes: DIRECT (`server_message`). Silent: assignment/attest MARKER rows inserted via `Projection.append_marker_in_txn/3` (surface on replay, no live push) | mixed — marker-row silence BY DESIGN (markers are transcript furniture; the same verb's work_state edge is the live signal) |
| turns | lifecycle: DIRECT (`assistant_typing`, `activity_event`, `prompt_turn_state_event`). Silent: `publishedAt`, `adapterGen` bookkeeping writes and substrate-stamped `assignmentId`/`jobRef`/`model`/`harness` | mixed — bookkeeping and substrate-stamp silence BY DESIGN (substrate internals; attribution/mind stamps are QUERY material through `work-item-trace`) |
| assignment_files | SILENT (rows written inside assignment creation; overlap refusal surfaces as the verb's error) | by design — file claims are INTERNAL collision machinery (no query verb exposes them; `declared_files/2` is internal API); observables are the files_overlap refusal and the boolean `assign.declared_files_overlap_open` producer fact (P3, advisory) — no row content ever surfaces |
| sessions (streams) | create/rename/retire/history-barrier: DIRECT (`stream_*`). Silent mutations: `set_host`, model/harness/provider changes, identity revision stamps, `adjudicationHold`, boot-maintenance fields | mixed — silent set is BY DESIGN (admin/substrate mutations; snapshot heals on reconnect) EXCEPT identity stamps (HOLE 1 below). The stream projection deliberately omits these fields; `stream_updated` is an OPAQUE DOORBELL (re-query), not a diff carrier |
| read_states | DIRECT (`stream_read_state`) | covered |
| assignments | status edges: DIRECT (`work_state_event`). Silent: holder rebinding during adjudication respawn | mixed — rebinding silence BY DESIGN (supervision machinery; board heals on snapshot); revisit only if a client renders live holder identity |
| work_state_events | DIRECT (they ARE the assignment-grain carrier rows) | covered |
| work_items, work_item_events | update/link: DIRECT doorbells. Silent: `work-item-create` itself | mixed — create-silence BY DESIGN (a bare item with no assignment is not yet board material; first link emits composition) |
| attests | edge-only via the status function; non-edge filings silent | silent BY DESIGN (thin-doorbell doctrine; truth queryable) |
| decision_requests | open: CHAT to the owner's Main. Ruling: CHAT via `escalation-ruled` wake for supervision-origin only. Silent: generic-origin ruling, consume, withdraw | mixed — silent transitions BY DESIGN (raiser is parked ON the request; ruling resumes it — the resumption IS the signal). Consistent with wakes: chat-on-fire is the carrier |
| wakes | schedule/cancel rows: SILENT. Fire: CHAT (materializes a turn) | mixed BY DESIGN (§Open ruling hot-path exclusion for scheduling; the fire is chat-carried) |
| condition_facts | SILENT | by design (hot-path exclusion) |
| subagent_markers (markers merge, 2026-07-25) | rows SILENT; a STOP's condition-fact may fire a parent wake, whose delivery is CHAT | by design — parent-attributed observability; the parent's wake turn IS the signal, and see-never-expect forbids making children board material |
| events (dispatch audit) | SILENT (query/feed only) | by design — audit trail, not board material |
| producer_jobs | SILENT (success may indirectly emit an attest/status edge; failure writes a lifecycle row) | by design pending a Flynn promotion — producer health is operator material, not stream material |
| assignment_prods, assignment_interruptions, adjudication_episodes, rail_remedy_episodes, escalation_waivers | prods/adjudication reach the affected session as CHAT; rows themselves SILENT | by design (supervision enumerates independently) |
| lifecycle_events | SILENT — a SHARED operational family (adapters, wakes, escalation, producers, placement, rails), not merely supervision's | by design — operational forensics, query-only |
| artifacts, assets | SILENT | by design (artifacts-and-reconciliation owns any future surfacing) |
| critical_leases, boot_epochs, harness_pointers, wire_idempotency, org_settings, scheduler_state, supervision_watermarks | SILENT | by design (substrate internals; queryable where a verb exists) |
| users, devices | pairing attempts: DIRECT (auth flow frames). Silent: promotion, approval/denial/revocation | mixed — silent set BY DESIGN in v1; revisit if a client renders admin rosters |
| roles | SILENT (create/bind/rm) | by design in v1 — revisit only if a client renders live rosters |
| **identity revisions (r5: live publication + per-session stamps)** | SILENT | **HOLE — closure 1** |
| **credential terminal parking (r5 §10)** | SILENT | **HOLE — closure 2** |

> **AMENDED 2026-08-12:** rows above naming `adjudicationHold`,
> `adjudication_episodes`, or adjudication respawn/chat describe machinery
> deleted 2026-08-05; the `producer_jobs` row describes machinery deleted
> 2026-07-29 (`verification-papertrail-v1.md`). Retained as history. See `adjudication-deletion-amendment.md`.

### The two closures (this phase's entire implementation surface)

Both reuse EXISTING frame kinds — no new wire schema, no new tables. `stream_updated`
is used as an opaque doorbell (stated intent, per the table): it tells a client to
re-query the stream; the accompanying process message carries the human explanation
where one is needed.

1. **Identity apply visibility.** In `identity_apply_session`, thread an internal
   `:applied | :noop` distinction out of the per-session branch (never-started sessions
   are `:noop` and emit NOTHING); after `Org.set_identity_revision/3` on the `:applied`
   branch, best-effort push `stream_updated` for that session. No wire response change.
   `identity edit`/`relearn` publication stays silent — nothing live changed until
   apply.
2. **Credential-parking visibility.** The park CLOSURE (runtime stop) is NOT the
   emission point — it is per-provider-runtime and knows nothing of sessions (r1 review
   F4). The interface is TWO-STAGE, both closures gateway-supplied, because
   `credentials.ex` owns the sequencing but has no DB/session access and a callback
   first invoked after park cannot recover the pre-park set (r2 review C):
   (a) `mark_terminal` acts only on a nonterminal→terminal TRANSITION (already-terminal
   re-entry emits nothing and re-parks nothing); (b) **stage 1 — pre-park capture**:
   before invoking the park closure, `mark_terminal` calls a gateway-supplied capture
   closure returning an IMMUTABLE payload of the affected sessions (active sessions
   whose harness maps to the terminal provider on the affected machine — the
   retire-capture pattern from §Emission); (c) **stage 2 — post-park publication**:
   after the terminal metadata write and successful park, `mark_terminal` hands that
   same payload to a gateway-supplied publish closure, which emits per captured session
   one process-origin `server_message` (credential terminal; parked pending re-onboard)
   plus one `stream_updated`. `credentials.ex` stays wire-free — it threads two opaque
   closures exactly as it threads the park closure today, and the payload passes from
   stage 1 to stage 2 untouched. (d) Successful re-onboard runs the SAME two-stage
   shape (capture before the resume takes effect: still-active sessions of that
   provider on that machine; publish the counterpart message after); failed or
   cancelled onboarding emits nothing.

### Tests (extend §Tests)

- identity-apply on a started session yields exactly one `stream_updated`; `:noop`
  (never-started) yields none. Apply has no turn-boundary refusal to test
  (`dr_07bdef13`); a session with a running turn is applied like any other.
- mark_terminal with N running provider-sessions yields N park messages + N
  `stream_updated`; a second mark_terminal for the same provider (already terminal)
  emits nothing and re-parks nothing.
- successful re-onboard yields exactly one counterpart message per still-active
  provider-session; failed/cancelled onboarding yields none.
- the captured payload is immutable across the park: a test mutates session membership
  INSIDE the injected park closure and asserts the publication still targets exactly
  the pre-park set (r2 review C).
- Emission failure proven with an injected publisher that raises/exits (a closed
  socket is NOT a failure — broadcasting to zero connections succeeds); the verb
  result is unchanged — total-catch parity with §Emission.

Everything else in the table is a recorded decision: a future "why doesn't X show up
live?" gets answered by this table, and promoting a BY-DESIGN silence into an emitter
is a revision to THIS section, not an ad-hoc broadcast added at a write site.
