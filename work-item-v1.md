# Work-item v1 — durable feature identity (implementation spec, r2)

Status: DRAFT r2. r1 → r2 (2026-07-20): adds work-item-update per
Flynn's orchestrator ruling (metadata mutable; state/hierarchy stay
absent), re-defines the spec-ref pin as the item's current governing
spec, and applies the r1 review findings (honest additive-change
claims, WorkItems-first bootstrap at every site, idempotent-replay
ordering). Parent ruling: decisions ledger 2026-07-20 (observability
direction — "durable work-item object: identity across re-staffing;
title + spec ref, no state") and the ROADMAP work-item-v1 entry
(SCHEDULED 2026-07-20, Flynn). This spec EXTENDS attest-v1.md r5
additively — it is the layer ABOVE assignments; attest-v1 remains
sole authority for assignment/attest behavior except where this spec
names an authorized extension. The PRINCIPAL seam is
session-tokens-v1.md r3, not restated here.

The primitive that gives a feature identity independent of who holds
it. An assignment is work in one session's hands; a WORK ITEM is the
durable thing the work is about. Assignments come and go — revoked,
surrendered, completed, re-staffed to a new session — while the work
item row persists and threads them into one history. One work item,
many assignments, covering BOTH shapes:

- SEQUENTIAL ERAS (re-staffing): revoke the old assignment, open a
  new one against the same work item; the item's assignment history
  IS the staffing history.
- CONCURRENT ASPECTS: several open assignments against one item at
  once, different holders (spec, build, review of one feature). No
  uniqueness constraint prevents this — its absence is deliberate
  and pinned (§Schema).

NO STATE COLUMN, ever, in this spec's scope. Work-item state is
DERIVED mechanically from its assignments (ledger ruling: ticket-as-
view, not ticket-as-object). The derivation function, event taxonomy,
and board/kanban consumption belong to observability-v1 — work items
are its natural card unit; this spec only lays the identity row that
derivation ranges over. When every assignment on an item closes,
NOTHING happens to the item: it persists unchanged; "done" is a view,
not a row mutation.

## Goals

1. A feature's identity survives re-staffing: `workItemId` on
   successive assignments makes "the same work, new hands" a
   queryable fact instead of prose folklore.
2. One random-access detail query returns an item and its full
   assignment history (eras and aspects), per the observability
   ruling that detail views are queries against tables, not streams.
3. A reference pin (name + content-hash) records the spec revision
   that CURRENTLY GOVERNS the item — drift becomes visible as a
   fact. The substrate never reads, fetches, or verifies the
   referenced content (T1); it records the pin the caller computed.
4. Purely additive for attest-v1 callers: the sole authorized
   observable difference is the additive nullable workItemId field
   on assignment objects; all pre-existing semantics are unchanged.
   Assignments without a workItemId remain fully legal forever
   (casual work needs no item).

## Non-goals (do not build)

NO HIERARCHY — work items do not nest; no parentId, no epics, no
sub-items. Flat. This is the anti-Jira guard: a parent ref MAY arrive
additively in a later revision if real use demands it, and is
explicitly out of scope now. NO state/status column, priorities,
sprints, orderings, board columns, descriptions-for-humans, due
dates, labels — product-layer per the boundary principle (the
substrate absorbs only facts it must witness; presentation stays
out). NO derived-status function, events, or filter contract
(observability-v1). NO delete/archive, and NO mutation beyond
work-item-update's metadata patch (§Verbs) — state and hierarchy are
not merely unpatchable, they do not exist; a mistyped title or stale
pin is corrected with work-item-update, not a new row. NO idempotency
key on work-item-create OR work-item-update (duplicate inert identity
rows are harmless; repeating an update is state-idempotent — same
values, same result; avoiding another wire_idempotency CHECK-widening
migration is worth it). NO updatedAt column and NO revision/history
table — the Dispatch audit event records THAT an update happened;
this spec provides no spec-pin history query (out of scope,
§Mutability). NO workItemId filter on the `assignments` query verb —
the detail query is work-item-get (§Verbs); a filter can arrive
additively later. NO pagination. NO visibility partitioning
(single-operator ruling, same as attest §Authorization). No UI.

## Mutability and what the pin means (r2 ruling)

Work-item metadata — title and the spec-ref pin — is MUTABLE via
work-item-update. State and hierarchy remain absent: there is
nothing of theirs to mutate, and no update can introduce them.

The spec-ref pin is the work item's CURRENT GOVERNING SPEC — "what
governs this feature now" — and is explicitly NOT per-assignment
historical provenance. Re-pinning erases nothing, because the item
pin never carried history: "what was asg_42 cut against" lives in
asg_42's own era — its subject and attest trail — not in the item's
mutable pin. Nobody may read the item pin as immutable provenance.
Ordinary verb audit records that an update happened
(accountability), but this spec provides NO spec-pin history query —
out of scope.

Cross-spec note (flagged here, not built here): metadata updates
(retitle, re-pin) do not surface through state-edge events alone;
observability-v1 must eventually invalidate/refetch its cards on
metadata update.

## Schema (follow existing migration/rebuild conventions)

DDL is camelCase per repo convention; prose may write snake_case.
Ids follow the existing convention: prefix <> Tightbeam.Id.uuid4().

work_items (new table, new module Tightbeam.WorkItems; its
ensure_schema runs BEFORE Assignments' at EVERY schema bootstrap
site — the gateway ensure_schema list AND every test setup that
ensures Assignments. The assignments FK below references work_items,
and with the pinned foreign_keys=ON SQLite rejects even a
NULL-workItemId assignment INSERT when the referenced table is
absent. The attest-era test/assignments_test.exs setup therefore
gains WorkItems.ensure_schema before Assignments — an authorized
adjustment):
- id TEXT PK — `wi_` + Tightbeam.Id.uuid4().
- title TEXT NOT NULL — free text, 1..2000 chars, non-blank after
  trim (refused "invalid_title"; same rule shape as attest's
  subject).
- specRefName TEXT NULL — caller-meaningful reference name (a spec
  path or name); 1..2000 non-blank after trim when present.
- specRefSha256 TEXT NULL — lowercase-hex sha256 of the referenced
  content, computed BY THE CALLER; must match ^[0-9a-f]{64}$ when
  present. Table CHECK: specRefName and specRefSha256 are both NULL
  or both non-null. Violations of either field or the pairing refuse
  with "invalid_spec_ref". The substrate stores the pin verbatim and
  never validates it against any file.
- createdByUser TEXT NULL, createdBySession TEXT NULL — EXACTLY ONE
  non-null (table CHECK; same typed-creator pattern as attest's
  opener columns).
- createdAt INTEGER NOT NULL (ms). No updatedAt and no revision
  rows — updates patch in place; the audit trail is Dispatch's
  (§Mutability).

assignments (attest-v1 table, EXTENDED — this is the one authorized
change to attest's schema):
- workItemId TEXT NULL REFERENCES work_items(id). Nullable forever;
  no CHECK ties it to any other column; NO uniqueness constraint on
  (workItemId, state) or any projection thereof — concurrent open
  assignments on one item are legal by design.
- Fresh DDL: the column appears in Assignments' CREATE TABLE.
- Pre-existing DBs (attest merged first): additive migration per the
  org.ex host-column precedent — `ALTER TABLE assignments ADD COLUMN
  workItemId TEXT REFERENCES work_items(id)`, duplicate-column error
  tolerated as already-migrated. Legal under foreign_keys=ON because
  the default is NULL. No rename-rebuild is needed (purely additive,
  unlike attest's idempotency CHECK widening); WorkItems'
  ensure_schema must still have run first so the referenced table
  exists.

## Authorization

Identity is the Dispatch call's PRINCIPAL (session-tokens-v1 r3).
Declared as/asUser grant nothing; roles are not consulted. The
handler check order and the router/handler precedence split are
attest-v1 §Authorization's, applied unchanged: {:process, _} →
"process_denied"; nil → "principal_required" (message teaching
session tokens); then verb authorization; then state checks.

- `work-item-create` — callers: any session or user principal (the
  attest `assign` rule; creating identity for work is as open as
  assigning work). Creator recorded in the typed columns.
- `work-item-update` — same principal model as work-item-create:
  any session or user principal. Updating is as open as creating;
  items have no owner semantics in v1.
- `work-item-get`, `work-item-list` — any non-nil session or user
  principal; read-only; no partitioning — every authorized caller
  sees all rows (single-operator ruling; revisit under multi-user as
  a statute-shaped filter, not code).
- `assign --work-item` — no NEW authorization: whoever may assign
  may link the assignment to any existing work item. Linking is not
  a privilege over the item; items have no owner semantics in v1.

## Verbs (registered exactly like existing verbs)

Four new verbs, named in the role-* family's noun-prefix style:
work-item-create, work-item-get, work-item-list, work-item-update.
All four are added to the router's @agent_verbs and to
Gateway.handlers/1, and run through Dispatch.dispatch/3. handlers/1
also supplies the valid verb set to statutes (Rules.load! takes
Map.keys of the handler table), so the new verbs — work-item-update
included — are statute-gatable with zero extra work. None takes a
typed target (sessionKey/role/userId): the router's existing generic
target handling applies unchanged and handlers ignore
call.session_key — no new target refusal is introduced for them. All
operational arguments ride under `params` (wire camelCase; the
router's atomize_params yields :title, :spec_ref_name,
:spec_ref_sha256, :work_item_id).

- `work-item-create` — params {title, specRefName?, specRefSha256?}.
  Validates title and the spec-ref pairing (§Schema), INSERTs one
  row. Returns the full work-item object (§Shapes).
- `work-item-update` — params {workItemId, title?, specRefName?,
  specRefSha256?}. A PATCH: a field ABSENT from params is
  unchanged; only provided fields change. title, when provided,
  revalidates under create's rule ("invalid_title"). The pin fields
  distinguish absent from explicit null:
  - both absent → pin unchanged.
  - explicit null (on either or both) → clears the pin; the
    both-or-neither CHECK still holds, so clearing clears BOTH
    columns. An explicit null on one pin field combined with a
    non-null value on the other refuses "invalid_spec_ref".
  - non-null value(s) → applied as a patch; after applying, the
    resulting pair must satisfy both-or-neither and the per-field
    rules (§Schema), else "invalid_spec_ref". Both fields at once
    sets/replaces the pin; one field alone is legal only against an
    already-pinned item (e.g. same specRefName, new sha256 after a
    spec revision) — one field alone against an unpinned item would
    leave the pair mixed and refuses.
  A patch providing no updatable field is a valid no-op returning
  the current row — consistent with updates being state-idempotent
  (repeating any update yields the same row). Unknown id →
  "unknown_work_item". No idempotency key (§Non-goals). Returns the
  full updated work-item object.
- `work-item-get` — params {workItemId}. Returns {workItem,
  assignments} where assignments is EVERY assignment row referencing
  the item — all states, ordered openedAt DESC, id DESC (attest's
  ordering) — the eras-and-aspects history in one random-access
  query. Unknown id → "unknown_work_item".
- `work-item-list` — no params. Returns {workItems: [...]} ordered
  createdAt DESC, id DESC (deterministic tie-break). No filters in
  v1 — there is no state to filter by; that is the point.
- `assign` (attest-v1 verb, EXTENDED — the second authorized
  change): optional params.workItemId. When present on the
  create-on-miss path, the handler verifies the work item exists
  INSIDE the same transaction as the assignment INSERT (attest
  §Atomicity pattern) — unknown → "unknown_work_item", transaction
  aborts; when valid, the INSERT carries workItemId. Absent → NULL;
  the sole observable difference from attest-v1 is the additive
  workItemId field (null) in the returned object. Idempotent
  replay: an EXISTING idempotency key SHORT-CIRCUITS before the
  newly supplied workItemId is validated — the key lookup runs
  first inside the transaction (attest's landed mechanics,
  untouched) and a hit returns the ORIGINAL assignment object with
  its ORIGINAL workItemId (null included); the work-item existence
  check runs ONLY on the create-on-miss path, so a replayed call
  carrying a different, missing, or even unknown workItemId still
  returns the original.
- `attest`, `revoke-assignment`, `assignments` — UNCHANGED in
  behavior; their returned assignment objects now carry the
  workItemId field (§Shapes). Closing, revoking, or surrendering an
  assignment never touches its work item row; after create, the
  ONLY writer of work_items is work-item-update.

## Atomicity

work-item-create is a single INSERT in one serialized DB call.
work-item-update is one serialized transaction: existence check
(unknown → "unknown_work_item"), field validation, one UPDATE of
the provided fields. The extended assign keeps attest's
one-transaction rule: idempotency lookup FIRST (a hit
short-circuits — §Verbs), then work-item existence check,
assignment INSERT, idempotency INSERT — all inside the SAME
transaction; the FK is a backstop, the in-transaction check is what
produces the typed error. No other verb in this spec mutates
anything.

## Response shapes

workItem: {id, title, specRefName, specRefSha256, createdByUser,
createdBySession, createdAt} — null for absent.
work-item-create, work-item-update: the workItem object (update
returns the post-patch row).
work-item-get: {workItem, assignments: [assignment...]}.
work-item-list: {workItems: [workItem...]}.
assignment (attest-v1 shape, EXTENDED): gains workItemId, null when
unlinked — additive field, authorized here; everything else per
attest §Response shapes.
Errors use the existing envelope. New codes, with transport status
(the router's status mapping is extended — authorized): 404-class:
unknown_work_item. 400-class: invalid_title, invalid_spec_ref.
403-class codes are attest's (process_denied, principal_required),
already mapped. Control-plane transports keep 200-with-error; the
classes bind the /agent REST statuses.

## Public API

None. No cross-lane function surface is added in v1; observability-
v1 names and owns its authorized read extensions in ITS spec (the
supervision-impl precedent), building on tables this spec lays.

## Events & audit

All four new verbs and the extended assign flow through Dispatch
with the EXISTING audit semantics exactly as stated in attest-v1
§Events & audit — accepted-call appends after commit with propagated
failure, best-effort only for statute denials. work-item-update
appears in the audit stream as an ordinary kind="verb" row — no
metadata-change event kind is added (the observability card-refresh
implication is a cross-spec note, §Mutability). No new event kinds
(derived-state events are observability-v1's, and are not built
here). No double-logging.

## Invariants (acceptance lens)

1. A work item row has no state and is never deleted; the ONLY
   mutation is work-item-update's metadata patch (title, spec-ref
   pin). No attest-v1 verb ever mutates it; all closure semantics
   live on assignments; "done" is derived elsewhere.
2. Identity across re-staffing is a join, not a copy: the item's
   history is `SELECT ... FROM assignments WHERE workItemId = ?` —
   never a second table, never denormalized.
3. Many-to-one is unconstrained: sequential eras and concurrent
   aspects are both just rows sharing a workItemId.
4. workItemId is nullable forever; the sole authorized observable
   difference to attest-v1 behavior is the additive nullable
   workItemId field on assignment objects — all pre-existing
   semantics for unlinked assignments are unchanged.
5. The spec-ref pin is caller-computed and substrate-verbatim (the
   substrate never opens, fetches, or checks the referenced
   content), and it means CURRENT GOVERNING SPEC — never
   per-assignment historical provenance (§Mutability).
6. Flat: no hierarchy column exists, none is emulated in prose,
   params, or title conventions blessed by this spec, and
   work-item-update cannot introduce one — it patches only title
   and the pin.

## CLI (Rust, cli/ — conventions from cli-rust-v1.md)

- `tightbeam work-item-create --title "..."
  [--spec-ref <name> --spec-sha256 <hex>]` — CLI enforces the
  both-or-neither pairing with a usage error; server re-validates.
- `tightbeam work-item-update <workItemId> [--title "..."]
  [--spec-ref <name>] [--spec-sha256 <hex>] [--clear-spec-ref]` —
  omitted flags leave fields unchanged (PATCH); --clear-spec-ref
  sends explicit null for both pin fields and conflicts with
  --spec-ref/--spec-sha256 (usage error); the server validates the
  resulting pair (§Verbs).
- `tightbeam work-item-get <workItemId>`
- `tightbeam work-item-list`
- `tightbeam assign ... [--work-item <workItemId>]` (existing
  subcommand, one added optional flag)
Output/exit conventions identical to existing subcommands. Extend
the existing Operations-fragment assignment bullet (added by attest)
with one clause teaching work items as the durable thread across
assignments — do not add a second bullet.

## Build ordering

attest-v1 is MERGED: main @ f739c07 carries the assignments
machinery. Cut the worktree from main at or after that SHA. If the
assignments machinery is absent from the base, STOP and report.
ROADMAP sequences the build after supervision's lane for scheduling
reasons; there is no technical dependency on supervision.

## Tests (condensed contract — cover every clause)

Schema: creator exactly-one CHECK; spec-ref both-or-neither CHECK;
title/name length-and-blank refusals; sha format refusal (uppercase,
short, non-hex each refused "invalid_spec_ref").
Bootstrap ordering: WorkItems.ensure_schema before
Assignments.ensure_schema at every site — the gateway list gains
WorkItems before Assignments, and the attest-era
assignments_test.exs setup gains WorkItems first (authorized
adjustment, §Schema).
work-item-create: by session principal and by user principal (typed
creator columns each recorded); with and without spec-ref; process
denied; nil → principal_required.
work-item-update: retitle persists; full re-pin (both fields);
one-field patch against a pinned item (same name, new sha) legal;
one-field non-null against an unpinned item refused
"invalid_spec_ref"; explicit null clears BOTH pin columns; null on
one field with a value on the other refused; absent fields
unchanged (title-only patch leaves the pin untouched); empty patch
is a no-op returning the current row; repeating an update yields
the same row (state-idempotent); unknown id → "unknown_work_item";
process denied; nil → principal_required.
work-item-get: unknown id; item with zero assignments (empty list);
item with mixed open/closed assignments — all states returned,
ordering incl. equal-timestamp tie-break.
work-item-list: ordering and tie-break; empty table.
assign: --work-item links (row carries workItemId; response shows
it); unknown work item → "unknown_work_item" and NO assignment row
survives (transaction abort proven); omitted → NULL, and the attest
suite passes with ONLY the authorized minimal adjustments —
WorkItems-first setup and the additive workItemId field on
assignment objects; no other attest behavior changes. Idempotent
replay: same key with a DIFFERENT, MISSING, or UNKNOWN work-item
argument returns the ORIGINAL assignment with its original
workItemId — proving the key lookup short-circuits before
work-item validation (§Verbs).
History shapes: re-staffing era (assign → revoke → assign same item;
get returns both, revoked one closed) and concurrent aspects (two
open assignments, different holders, same item — both legal, both
returned).
Lifecycle independence: closing every assignment on an item mutates
nothing in work_items (row byte-identical before/after);
work-item-update mutates nothing in assignments.
Migration: a pre-existing attest-era DB (no workItemId column) gains
the column via the additive ALTER; old rows read back workItemId
null; re-running ensure_schema is idempotent.
Router: four verbs reachable through /agent dispatch;
unknown_work_item maps 404; a target supplied to a work-item verb
follows existing target-less-verb router behavior (pinned by test,
not changed).
Events: each new verb (update included) appends one kind="verb"
row. Statutes: one integration test with a real [[rule]] denying
work-item-create; the verb set statutes range over comes from
Gateway.handlers/1, so work-item-update is gatable identically.
CLI: each subcommand plus the assign flag via the existing
CLI-integration harness (session-tokens-v1 r3); create pairing
usage error and update --clear-spec-ref conflict usage error
exercised.

## Handoff

Gates: mix compile --warnings-as-errors clean; full mix test green
(attest suite green with only the authorized minimal adjustments
named in §Tests); cargo test green in cli/. Commit on the branch;
do not merge. STOP and report on any conflict with existing code,
attest-v1 as merged, or this spec.
