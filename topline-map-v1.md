# Topline map — the work telemetry the substrate already knows — v1

Status: DRAFT r7. This is a read-only substrate view over durable work, assignment,
turn, attest, wake, adjudication, and creation-context rows. It consumes
`core-causality-fixes-v1.md` C1 (creation context recorded) and C2 (at most one
resolved item per assignment). It adds no schema, migration, or emission.

## What v1 delivers

Flynn's ask: "render the toplines and show information like 5 agent jobs, the
number of attests, finish/start state, idle state … a map for that agent to go
figure out what's done and what isn't … should be able to query subtrees."

v1 delivers the roster, per-node telemetry, cohort selectors, explicit
assignment-set selection, and a causal forest. Parent edges are derived from the
recorded creation context, and every edge's epistemic status is stated
mechanically.

## The creation-context evidence and what it may claim

Every `work_items` row carries `createdInTurnSeq INTEGER NULL` and
`createdContextKnown INTEGER NOT NULL DEFAULT 0` (work_items.ex:25-43). Create
stamps the creating session's currently running turn (work_items.ex:80-108,
154-165); at most one turn can be running in a session lane (ledger.ex:166-175).
Pre-C1 rows carry `known = 0` through the additive migration
(work_items.ex:785-800).

**The stamp means CONCURRENCY, not proven causality** (core-causality-fixes-v1
C1, binding here): the request carries no turn identity, so the stamp says
"this create was concurrent with that running turn." Two deviations are
load-bearing for this reader:

- a separate request on the same session token while a turn runs is stamped
  with that turn — a false positive the reader cannot detect;
- cancel and boot recovery can terminalize a turn before serving stops, so an
  in-flight create can land `seq = NULL` — a false negative the reader cannot
  detect.

`createdContextKnown = 1` means the substrate looked, not that causal truth is
known. The reader never emits a confidence score, probability, or
high/medium/low grade. The response instead carries:

- a top-level constant `edge_basis: "concurrent_turn"`; and
- `parent: {status, item}` on every node, with exactly one of the four statuses
  below.

### The four parent statuses

| status | row and derivation condition | meaning |
|---|---|---|
| `linked` | `known=1`, seq set, and derivation yields a different, caller-visible item whose edge survives cycle handling | best-available parent edge, concurrency-based |
| `from_turn` | `known=1`, seq set, but no parent link may be retained | created during session work; no parent item nameable |
| `no_turn_observed` | `known=1`, `seq IS NULL` | the substrate looked and nothing was running — the root signal, subject to the false negative above |
| `unrecorded` | `known=0` | pre-C1 row; parent unknowable — not a root, not an edge |

These conditions are exhaustive and mutually exclusive. `from_turn` includes a
conversational turn, an assignment resolving to NONE, a missing turn row, an
authorization-hidden parent, and a cycle-closing edge that must be dropped.
Both `from_turn` and the two no-edge statuses carry `item: null`; the status is
the load-bearing field. A renderer labels top-level nodes with the status and
does not collapse them into a bare "root."

The row's own columns are also reported verbatim as
`creation_context: {recorded: bool, turn_seq: int|null}`. The derived `parent`
block never exposes the creating turn's `jobRef` or `assignmentId`.

### Edge derivation

For a node with `known = 1` and non-null seq, derive the candidate parent from
the recorded turn. Turns durably carry `assignmentId` and `jobRef`
(ledger.ex:37-61):

1. use the turn's `jobRef` when set; bracket nags and item-attributed turns can
   carry the work-item id without an assignment (job_trace.ex:115-139);
2. otherwise use the turn assignment's RESOLVED item, as defined in Membership;
3. otherwise retain no edge and report `from_turn, item: null`.

Derivation is total over missing, legacy, and corrupt rows. Candidate edges are
authorization-filtered before traversal. Traversal uses canonical node order
(`createdAt ASC`, then `id ASC`) and a current-ancestry visited set; an edge
whose target is already on that ancestry is the cycle-closing edge and is
dropped. The source node's `parent` block reports that same dropped result as
`{status: "from_turn", item: null}`. A corrupt self-parent therefore produces
neither a traversal edge nor a `linked`-to-self parent block.

Appearance filters do not participate in edge derivation. A visible parent
excluded only by a roster filter remains nameable in the child's `parent`
block; Surface defines how the filtered forest is rendered.

## Membership — RESOLVED for the story, DIRECT untouched

The one normative definition of an item's resolved assignment set is:

```
resolved_assignments(item) =
  {a : Assignments.resolved_work_item_id(db, a.id) = item}
```

`resolved_work_item_id/2` is total and cycle-safe. An assignment's own
non-null `workItemId` wins; otherwise resolution follows `reviewsAssignmentId`;
otherwise it returns NONE (assignments.ex:381-390,838-864). Every field labeled
RESOLVED below uses exactly this set. Edge derivation and the turn union call
the same resolution rule; neither may carry a second membership definition.

The recursive `work-item-trace` relation seeds on `workItemId` and follows
review links (job_trace.ex:68-87). It is equivalent to the normative set only
when no legacy review/item conflict exists. An implementation reusing that CTE
must keep a conflicted row under its own pin and exclude it from membership
reached through a reviewed chain when its own non-null pin differs from the
resolution of its `reviewsAssignmentId`. In other words, the direct seed honors
own-pin-wins and the recursive term cannot also attribute that row to the
reviewed item's chain.

New conflicts are refused before insert (assignments.ex:743-749), with the
`:review_item_conflict` response at assignments.ex:831-835. Legacy conflicts
are logged without mutation by the boot audit (assignments.ex:392-427,
gateway.ex:175-186). This response carries no conflict field: the resolution is
singular, while the logged conflict remains an operator concern.

An assignment resolving to NONE belongs to no item's ordinary telemetry. It is
not an item orphan and does not create a synthetic item. The explicit
`--assignments` surface reports a visible NONE assignment in `no_item`, as
defined below.

DIRECT consumers are not widened. `feature_smoke` cleanup revokes exactly the
direct assignments returned by `work-item-get`
(scripts/feature_smoke.exs:787-800), and client work-item snapshots remain
direct (`work_state.ex:97-128,217-220`).

## Origin: reported and annotated, never classified

Every node carries `origin: {principal: "user"|"session", created_by}` from the
immutable creator columns; the schema requires exactly one creator
(work_items.ex:37-43), and create maps user and session principals directly to
those columns (work_items.ex:80-108,699-709). These columns record the
authenticated principal class, not human-versus-agent identity. A human using
a session token, including `--as-user`, writes `createdBySession`.

The substrate does not decide which items are "toplines."
`--origin user|session|all` selects; the annotation is present regardless of
filter so a caller can re-slice one response.

## Per-node telemetry — only what the rows support

Field-group labels are normative:

### DIRECT — the item's own row or item-keyed event

- **title** and **specRefName** / **specRefSha256** — the item's own row,
  reported verbatim: no derivation, no truncation, no formatting. The roster's
  purpose is a map an agent can read, and a node identified only by id does not
  serve it. The pin is a cohort selector below, so a node that can be selected
  by `--spec` names the spec it carries; it is mutable, and this reports its
  current value like any other column.
- **state** / **failReason** — the item's own row.
- **bracket1_armed** — `routingWakeId IS NOT NULL` (work_items.ex:25-43).
- **origin** and **creation_context** — the item's own immutable creator and
  C1 context columns.
- **parent** — derived from the item's own C1 context as specified above.
- **finished_at** — the timestamp of the latest `disposition_transition`
  causal event whose `toState` equals the item's current terminal state
  (`closed`, `failed`, or `iceboxed`). Dispositions append that event with
  `jobRef = item` and exact from/to state (work_items.ex:325-345).
  `finished_at` is null for an open item even with prior transitions and for a
  terminal item with no matching event.

### RESOLVED — `resolved_assignments(item)`

- **assignments** — `{open, closed, by_outcome: {completed, surrendered,
  revoked}}`.
- **jobs** — distinct `holderKey` sessions that ever held a resolved
  assignment, including closed assignments. This is a history count, not a
  current-holder count; `holderKey`, state, outcome, and timestamps are durable
  assignment columns (assignments.ex:32-49).
- **attests** — `{total, by_kind}` plus `by_verdict_kind` over raw stored
  caller-supplied slugs. Verdict slugs are shape-validated only
  (assignments.ex:1346-1357); no durable approved/rejected taxonomy exists.
  Collapsing them would invent classification.
- **started_at** — `MIN(openedAt)` over the resolved set; null if the set is
  empty.
- **closing_attests** — plural
  `[{assignmentId, attestId, commitRefs|null}]`, restricted to
  completed/surrendered closes. Those outcomes require a non-null
  `closingAttestId`; revoked requires it to be null
  (assignments.ex:41-62). Revoked closes appear only in
  `assignments.by_outcome.revoked`.
- **open_decision_requests** — count of open decision requests attributed to
  the resolved set.

### RESOLVED turn union and current-holder state

- **turns** — `{total, last_ended_at}` over the union of turns with
  `jobRef = item` or `assignmentId` in the resolved set, deduped by `seq`.
  Turns durably carry both keys (ledger.ex:37-61). A bracket nag may have only
  `jobRef`; a review turn may have only `assignmentId`; either arm alone
  undercounts.
- **minds** — distinct `{model, harness}` over the same turn union. The mind is
  stamped when a queued turn is claimed (ledger.ex:178-221).
- **fan_out** — assignment-attributed subagent markers. `assignmentId` is the
  durable marker carrier (subagent_markers.ex:20-45), stamped from the running
  parent turn at emission (subagent_markers.ex:303-312).
- **active.running_turn** — true when the turn union contains a currently
  running turn.
- **active.pending_session_wake** — true when any **current open-assignment
  holder** in the resolved set has a pending `consumer='prompt'` wake. It does
  not inspect only item-attributed wakes: supervision gates the current open
  holder at turn end (supervision.ex:201-220,316-320), and wake suppression is
  session-keyed across all pending prompt wakes (wakes.ex:333-344).
> **AMENDED 2026-08-12:** the `holds` field below died with adjudication —
> `adjudication_episodes` is gone. Adjudication was deleted 2026-08-05 ("Adjudication is DELETED. Model policy is guidance, not substrate." — `tightbeam-decisions.md`). Retained as history. See `adjudication-deletion-amendment.md`.

- **holds** — plural `[{episodeId, cause|null, sessionKey}]`, restricted to open
  adjudication holds whose `sessionKey` is one of those same current
  open-assignment holders. The hold carrier is durable on
  `adjudication_episodes` (adjudication.ex:20-36).

A holder is current for the last two fields only while it owns an open resolved
assignment. A stale ex-holder with only closed assignments contributes to the
historical `jobs` count, but none of its pending conversational wakes or holds
marks the item active.

### Progress clock and coverage

**since_progress_ms** is time since the latest known progress event:

- an ended turn in the turn union;
- any attest in the resolved set, including durable attests from before the
  attribution epoch; or
- an item disposition transition.

A scheduled wake or fired prod is not progress. The public clock anchor is the
maximum of all known progress timestamps and the coverage baseline. The
baseline is `createdAt` for an item created at or after
`attribution_cutoff`; for an older item it is
`max(createdAt, attribution_cutoff)`. Thus an older item's clock can never
claim quiet time before attribution was knowable:
`since_progress_ms <= now - attribution_cutoff`. Pre-epoch attests are not
discarded; filing an attest resets the progress clock, subject to the same
cutoff floor.

Turn attribution, mind stamps, and marker attribution shipped as nullable
ALTERs with no per-row stamp (ledger.ex:75-87; subagent_markers.ex:42-45).
The one conservative shared epoch is `causal_events_epoch`, written once at
table creation (causal_events.ex:51-59,79-99). The response reports
`coverage: {attribution_cutoff: <epoch>, basis:
"conservative_shared"}`. For an item older than the cutoff, every count whose
zero depends on those nullable attribution carriers is `null`, never `0`;
absence is unknown. Durable assignment and attest facts remain reportable.
The progress clock uses the cutoff floor above. Parent derivation does not use
the shared cutoff: C1 has its own per-row knowledge bit, and `unrecorded` is
that edge's coverage statement.

Explicitly not reported: any percentage, completion estimate, confidence
score, or confidence grade.

## Surface

`tightbeam toplines [--origin user|session|all] [--owner <u>] [--state <s>]
[--quiet-over <duration>] [--spec <name> [--spec-sha <sha>]]
[--session <key>] [--tree]`

Without `--tree`, this is the roster with full telemetry. With `--tree`, it is
the caller-visible causal forest. `--quiet-over` requires
`since_progress_ms` over the bound, `active.running_turn = false`, and
`active.pending_session_wake = false`.

Cohort selectors are exact, with no inference:

- `--spec <name> [--spec-sha <sha>]` selects items whose current pin matches.
  The pin is mutable, so repinning moves an item between cohorts.
- `--session <key>` selects items created by that session. Creator identity is
  immutable.

`tightbeam topline --under <id> [the same roster filters]` defines its causal
candidate set as the authorized-visible anchor plus its transitive
authorized-visible descendants through `linked` edges. Roster filters then
select the appearing nodes, each with full telemetry.

Roster filters select which authorized nodes **appear**; they do not change
authorization, edge derivation, or causal reachability. Tree nesting exists
only among appearing nodes. If a child's linked parent is authorized-visible
but filter-excluded, the child appears top-level and retains
`parent: {status: "linked", item: <parent-id>}`. No placeholder node is
emitted, and an excluded parent is not pulled into the result. The same rule
applies to `--tree` and `--under`, including when an excluded anchor or
intermediate ancestor has selected descendants.

`tightbeam topline --assignments <id,...>` is explicit assignment-set
selection. Empty input is a usage error and duplicate ids collapse. Each
visible id is resolved by the normative membership function:

- a visible id resolving to an item contributes that visible item once;
- a visible id resolving to NONE contributes no item and is returned in
  `no_item: [assignmentId, ...]`;
- any unknown or invisible id makes the whole request `not_found`.

`not_found` is reserved for the unknown/invisible conflation. Returning it for
a visible NONE assignment would conflate substrate truth ("this assignment has
no item") with authorization. Silently dropping the id would make the tool lie
by omission about an assignment the caller explicitly selected.

All node sequences are deterministic: roster rows, forest roots, and siblings
use `createdAt ASC`, then `id ASC`. `no_item` uses assignment id ascending.

## Authorization — omission, no existence leak

An item node is visible under the existing `work-item-trace` owner-or-admin
rule (work_items.ex:577-619). Invisible nodes are omitted entirely; no response
value, total, count, order, marker, id, filtered flag, or nesting choice may
depend on their existence.

For `--assignments`, an id that resolves to an item is usable only when that
item is visible under the node rule. An id resolving to NONE is visible under
the assignment-detail rule: admin, or a caller who owns the assignment's
holder session (wire/router.ex:629-633). All other assignment ids are
invisible.

Consequences:

- an edge is reported only when both endpoints are visible. A visible child of
  an invisible parent reports `parent: {status: "from_turn", item: null}`,
  indistinguishable from the conversational-turn case;
- the parent block and creation context never carry the creating turn's
  `jobRef` or `assignmentId`;
- unknown and invisible `--under` selectors return identical `not_found`;
- unknown or invisible `--assignments` ids return identical, all-or-nothing
  `not_found`; visible NONE ids use `no_item` instead.

The normative leak bar is **twin-world byte identity**. For the same caller,
request, fixed evaluation time, and visible rows, the caller's complete
response in a database containing invisible rows must be byte-identical to the
response in a database where those invisible rows and their assignments and
turn attributions are physically absent. This applies independently to roster,
`--tree`, `--under`, and `--assignments`. Parent-block identity is a focused
sub-proof of this whole-response requirement, not a substitute for it.

## Required proofs

All are automated. Every proof must fail when the behavior it names is broken.

1. Origin annotation and `--origin` selection; the same item is annotated
   identically under every filter that includes it.
2. Parent-status quadrichotomy in one response: `linked` from an
   item-attributed running turn, `no_turn_observed` from a recorded null seq,
   `unrecorded` from `known = 0`, and `from_turn` from a turn with neither
   `jobRef` nor a resolving assignment. Assert all four are distinct and
   exhaustive, especially `no_turn_observed != unrecorded`.
3. Edge derivation succeeds through both carriers: a `jobRef` with no
   assignment and a turn assignment resolving transitively through a
   NULL-`workItemId` review assignment.
4. Twin-world authorization: with invisible items, assignments, attests,
   wakes, holds, markers, and turn attributions present in one database and
   physically absent in its twin, freeze evaluation time and assert complete
   response byte identity for roster, `--tree`, `--under`, and
   `--assignments`. Also assert the focused invisible-parent block is
   byte-identical to the conversational-turn block.
5. `--under` returns the anchor plus transitive visible linked descendants.
   Unknown and invisible anchors return identical `not_found`. A directly
   inserted multi-node cycle terminates and drops the deterministic
   cycle-closing edge in both traversal and the source node's parent block. A
   directly inserted self-parent likewise yields no traversal edge and
   `parent: {status: "from_turn", item: null}`, never linked-to-self.
6. Singular resolved membership under legacy conflict: directly insert a
   review assignment R whose own pin is B while it reviews A's chain, bypassing
   the C2 guard as the boot audit contemplates. R contributes to exactly one
   item's telemetry — B — with its turns, attests, historical job holder, and
   mind each singly attributed. A receives none of them. Parent-edge
   derivation from an assignment-only turn attributed to R resolves B, and the
   turn union places that same turn under B only. Also assert an ordinary
   NULL-pin review follows its chain, a NONE assignment belongs to no item, and
   DIRECT client snapshots retain byte parity.
7. Turn union: a bracket nag (`jobRef`, no assignment) and a review turn
   (assignment, no `jobRef`) each count exactly once; a turn carrying both keys
   is not double-counted.
8. Terminal fields: `finished_at` is null for open after icebox→open, set from
   the transition matching a current terminal state, and null for terminal
   pre-event history. `closing_attests` includes completed and surrendered
   closes with non-null attest ids, excludes revoked closes, and
   `by_outcome.revoked` still counts them.
9. Progress and quietness: a pre-cutoff item's `since_progress_ms` never exceeds
   `now - attribution_cutoff`; a durable pre-epoch attest participates as a
   progress event and resets the clock subject to that floor; scheduling or
   firing a wake does not reset it. `--quiet-over` excludes a current holder
   with a running turn or pending prompt wake. A stale ex-holder with a pending
   conversational wake does not set `active.pending_session_wake`, does not
   appear in `holds`, and does not defeat `--quiet-over`; it remains represented
   only in the ever-held `jobs` history.
10. Coverage: an item older than `attribution_cutoff` reports every
    attribution-dependent count as null, never zero; durable assignment and
    attest facts remain populated; its parent block is still derived from its
    own per-row C1 coverage bit.
11. Filtered forests: in both `--tree` and `--under`, filter out a
    caller-visible parent while retaining its child. Assert the child appears
    top-level with `parent: {status: "linked", item: <parent-id>}`, the parent
    node and all placeholders are absent, and root/sibling order is
    `createdAt ASC`, then `id ASC`.
12. `--assignments` exercises all three classes in one proof: a visible
    with-item id contributes its item, a visible NONE id appears in `no_item`
    and contributes no item, and unknown versus invisible ids produce
    byte-identical all-or-nothing `not_found`. Duplicate input collapses and
    empty input remains a usage error.
13. The roster's deterministic order is `createdAt ASC`, then `id ASC`, under
    every combination of roster filters.
14. Every surface is read-only in its own effects. The ordinary audit row is
    expected and allowed.

## Component touches

A telemetry read module, `toplines` and `topline` verbs in gateway/router, CLI
and surface rows, and tests. No schema, migration, emission, or changes to
work-item, assignment, ledger, wake, adjudication, or marker writers.
`work-item-families-v1` is superseded because its cohort selectors are absorbed
here.
