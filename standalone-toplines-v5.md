# Standalone Toplines MVP for 0.1.9 and 0.2.0

Canonical path: `standalone-toplines-v5.md`

Work item: `wi_875fbdd5-6756-4149-b032-f055dc4f965c`

Status: targetless specification amendment candidate. This file does not bind
the work item until an independent specification review returns reviewed-clean
for its exact SHA-256.

## Spirit

A Topline is one ask that a user wants the organization to keep in view. It is
not a second task system. Tightbeam stores the ask, records who created it, and
lets each work item point to one Topline or remain explicitly unlinked.

When a user asks, "give me toplines," Tightbeam answers with the user's intent.
It does not answer with execution telemetry, inferred themes, progress, or a
machine-generated hierarchy. Execution telemetry remains the Execution Map.

Placement happens at an observable work-item edge. Tightbeam offers the user a
choice. The user or an authorized agent links the work item to one Topline or
records `leave-unlinked`. Tightbeam does not rank, infer, or repeatedly nag.

This amendment supersedes the behavioral scope in specs commit
`3c83d382968f242ebab660f9b67593aa80a1e84e`, whose canonical file SHA-256 is
`1ffc9ee7b984df672b21d46d7a6f3cd3a40b274bd4cec8943377ca47c17881d6`.
It preserves the reviewed Lane 2 work at main
`5adc6f03e0469aa399b14a312985f92ea5036107` and `0.1.9`
`9c45e34af46aba451ac84ea5795a50a4a16fdafd`, except for bytes that implement
Concerns, multiple active Topline links, or membership episodes. Independent
Lane 2 review `att_75de3a99-6aca-4f6b-84b9-aa4d43847e62` and report
`art_32e37248` found those exact candidates reviewed-clean.

The canonical set still contains exactly two repository-root paths at one
exact specs commit:

- `standalone-toplines-v5.md` owns the Toplines product contract, delivery
  ledger, and no-release gate.
- `v0.2-program-2026-08-12.md` owns only the negative fact that Toplines is not
  a v0.2 program phase.

`standalone-toplines-concerns-and-multi-membership-follow-on.md` is a named,
targetless follow-on candidate. It is not in the canonical set. It carries no
binding, implementation, target, integration, or release authority.

## Goal

G1. Tightbeam shall store one user ask as one durable Topline owned by that
user.

G2. Tightbeam shall record the user or session that creates or changes a
Topline.

G3. Tightbeam shall let a work item have zero or one current Topline link.

G4. Tightbeam shall let an authorized user or session explicitly link or
unlink a work item.

G5. Tightbeam shall answer `toplines` and `topline` with durable intent data.

G6. Tightbeam shall keep work telemetry under `execution-map` and
`execution-map-select` with its reviewed behavior unchanged.

G7. Tightbeam shall create one placement decision at a qualifying work-item
edge and offer `leave-unlinked` as a complete decision.

G8. Tightbeam shall preserve authorization, privacy, idempotency, audit, and
pre-1.0 CLI compatibility for the retained surface.

G9. Tightbeam shall expose one typed rail fact that reports whether the call's
work item has a current Topline link.

G10. Tightbeam shall deliver the same observable contract on product lines
`0.1.9` and `0.2.0`.

G11. Tightbeam shall prove upgrade, rollback, and same-database re-upgrade with
real previous and candidate packages before final review.

G12. The delivery shall retain exactly four implementation lanes. Completed
Lane 1 and Lane 2 evidence remains provenance. Remaining work stays in Lane 3
and Lane 4.

## Non-Goals

NG1. A Topline is not a work item. It has no assignment holder, execution
state, estimate, priority, completion percentage, or causal parent.

NG2. This MVP has no Concern entity, identifier, table, index, event, response
field, route, wire verb, CLI command, lifecycle, reference, migration, repair,
or test obligation.

NG3. This MVP has no Work-membership entity or membership identifier. It does
not retain ended link episodes.

NG4. One work item cannot hold current links to two Toplines.

NG5. A link command does not replace an existing link. The actor must unlink
the work item before linking it to another Topline.

NG6. Tightbeam does not infer, rank, score, or recommend a Topline.

NG7. Tightbeam does not start an inference session for placement.

NG8. Tightbeam does not scan periodically, re-nag on a timer, or use elapsed
time to decide placement.

NG9. Tightbeam does not block work-item creation, reopening, assignment, or
completion because the work item is unlinked.

NG10. Tightbeam does not preserve the retired telemetry meanings of
`toplines` or `topline` as aliases.

NG11. This work does not change REST routes, REST cursors, pagination, or
consumer presentation policy. A separate contract cannot expand this MVP.

NG12. This work does not belong to a v0.2 program phase.

NG13. Product version `0.1.8` is not an implementation target. An exact
`0.1.8` package can serve as a previous-package fixture.

NG14. This specification and its reviews do not authorize product integration,
release, publication, deployment, service restart, or live database mutation.

NG15. This MVP does not migrate a database created by an unshipped Toplines
candidate that contains Concern or membership-episode tables. Candidate boot
shall refuse that shape without changing it.

NG16. A reviewed-clean final report is not release approval.

NG17. Tightbeam exposes no hard-delete command for a Topline, audit event,
idempotency record, or Placement decision.

## Terms

**Topline.** One durable user ask. Its identifier starts with `tl_`. Its owner,
title, lifecycle state, creation actor, and timestamps live in the Toplines
store.

**Topline owner.** The user whose ask the Topline records. A session acts for
the user in its durable `ownerUserId`.

**Current link.** The one present relationship between a work item and a
Topline. The relationship is keyed by `workItemId`; it has no public or stored
membership identifier. Deleting the current row unlinks the work item. Audit
events retain the transition.

**Unlinked.** A work item with no Current link. Unlinked is a valid product
state.

**Placement edge.** A committed work-item creation or `iceboxed -> open`
reopen that leaves the work item open and unlinked.

**Placement decision.** One durable pending or resolved record created for a
Placement edge. A link, `leave-unlinked`, or terminal work-item transition
resolves it.

**Execution Map.** The existing read-only work telemetry: roster, causal tree,
subtree, and assignment selection. Its concurrent-turn ancestry is evidence of
concurrency, not intent.

**Actor.** One attributable principal represented by `actorKind` and
`actorRef`. Public mutation actors use `user` or `session`. Boot reconciliation
uses `process` with reference `tightbeam`.

**Mutation key.** Caller-supplied, non-blank text of at most 200 Unicode scalar
values. It identifies one mutation for idempotent replay.

**Mutation reason.** Caller-supplied text whose trimmed length is 1 through
4,000 Unicode scalar values. Tightbeam stores the supplied text verbatim.

**Canonical title.** The supplied title after Tightbeam removes Unicode 15.1
White_Space from both ends and normalizes the result to NFC. Its length is 1
through 2,000 Unicode scalar values.

**Visible row.** A row that the caller can read under the owner-or-admin rule.

**Target line.** Product line `0.1.9` or `0.2.0`. `main` is the development
branch for the `0.2.0` line. A Target line is not a v0.2 program phase.

**Exact target revision.** The full 40-character commit selected by the
responsible product-line owner as a lane input. A branch name or local state is
not an Exact target revision.

**Exact candidate revision.** The immutable full commit produced by a lane.

**Previous-package fixture.** An owner-named immutable Gateway package and its
matching CLI. Evidence records their source revision, versions, and SHA-256
values before use.

**Candidate package.** An unshipped Gateway and matching CLI built from one
Exact candidate revision for disposable tests.

**Reviewed Lane 2 behavior.** The following behavior proven at main
`5adc6f03e0469aa399b14a312985f92ea5036107` and `0.1.9`
`9c45e34af46aba451ac84ea5795a50a4a16fdafd`: Execution Map command separation;
durable Topline list and get; Topline create, update, close, and reopen; explicit
work link and unlink; placement list and leave-unlinked; exact CLI help and
early refusal; owner visibility; mutation replay; candidate restart; immutable
previous-Gateway startup; positive legacy telemetry; same-database candidate
upgrade; populated-row preservation on main; bridge cleanup; and second-run
idempotence. Concern behavior and multi-link behavior are excluded.

## Assumptions

A1. Each work item has one durable `ownerUserId`.

A2. Each user has one addressable personal Main session.

A3. SQLite transactions serialize competing writes and commit their state and
audit rows together.

A4. The wake scheduler stores pending wakes durably and delivers one claimed
wake at a turn boundary.

A5. The Gateway checks exact CLI version compatibility before authentication
or handler dispatch because both Target lines are pre-1.0.

A6. The reviewed Execution Map fixtures define its telemetry fields, filters,
order, cursor behavior, authorization by omission, and read-only behavior.

A7. Work-item creation, reopen, and terminal disposition can call one
in-transaction Toplines seam.

A8. The database enables SQLite foreign-key enforcement before it accesses
product rows.

A9. A work item can continue through its lifecycle while unlinked.

A10. An admin can read and mutate rows for another user. An admin cannot link a
Topline and work item with different owners.

A11. The two Target lines can use different internal plumbing while returning
the same Toplines and Execution Map contract.

A12. Product-line owners will record Exact target revisions and
Previous-package fixtures before the corresponding lane starts.

A13. Lane 1 landed exact reviewed commits
`a8088e8fa540257c9f9674c4e011bf53ae909a27` on `0.1.9` and
`d0dbf34d4befbd1e46485960027363fff26b9d17` on main. These commits are
provenance, not current moving-ref authority.

A14. Lane 2 produced reviewed-clean targetless candidates at the exact commits
named under Reviewed Lane 2 behavior. They were not integrated when this
amendment was requested.

A15. Disposable local databases, synthetic principals, isolated ports, and
immutable packages can prove the contract without a live service or user
database.

## Invariants

I1. One Topline row records one user ask and one owner.

I2. One work item has zero or one row in `topline_work_links` because
`workItemId` is that table's primary key.

I3. A Current link joins a Topline and work item with the same `ownerUserId`.

I4. The runtime exposes no membership ID, ended membership row, Concern ID, or
Concern reference.

I5. Link and unlink require an attributable `user|session` actor and a Mutation
reason.

I6. The transaction that changes a Current link appends its audit event or
commits neither change.

I7. A second link request for an already-linked work item returns
`work_already_linked`. It does not replace the row.

I8. Unlink addresses `workItemId`, deletes its Current link, and records the
former `toplineId` in the audit event.

I9. Unlink does not create a Placement decision. The unlink itself is an
attributable decision.

I10. A Topline can be `open` or `closed`. A closed Topline accepts reopen and
unlink. It rejects create-link and title-change mutations.

I11. `toplines` returns Topline summaries. `topline` returns one Topline and
its current linked work items. Neither response contains Execution Map fields.

I12. `execution-map` and `execution-map-select` preserve the reviewed telemetry
contract. They return no Topline intent projection.

I13. A non-admin user or session sees Toplines owned by its user. An admin sees
rows from each owner.

I14. An unknown identifier and a foreign identifier return the same
`not_found` response to a non-admin caller.

I15. A process principal cannot invoke a public Topline read or mutation.

I16. Each public mutation requires a Mutation key. A same-key, same-fingerprint,
currently-authorized replay returns the stored response bytes.

I17. A same-key request with a different fingerprint returns
`idempotency_conflict` without a product mutation.

I18. Tightbeam stores one immutable audit event for each successful Topline
create, update, close, reopen, link, and unlink.

I19. Event sequence starts at 1 for each Topline and increases by 1.

I20. A Placement edge creates at most one pending Placement decision and one
durable prompt wake.

I21. The Work Item transition, Placement decision, and durable wake are created
in one transaction for a current-package edge.

I22. The placement prompt offers link-to-one-Topline and leave-unlinked. It
does not choose either result.

I23. Link, leave-unlinked, or terminal work-item disposition resolves one
pending Placement decision and cancels its wake only while the wake is pending.

I24. A fired or already-canceled placement wake retains its recorded state.

I25. Firing a placement prompt does not schedule another prompt.

I26. A later `iceboxed -> open` edge can create one new Placement decision.

I27. Boot reconciliation uses durable causal events and stored watermarks. It
also queries open, unlinked work items with no Placement history. It does not
use elapsed time or inference.

I28. The `work_item.has_topline` fact is true for one Current link and false
for zero Current links. Unknown, invisible, or absent work-item context returns
the existing typed unavailable result.

I29. The product installs no default statute for `work_item.has_topline`.

I30. Candidate schema contains no table or index for Concerns, Concern
references, Work-membership episodes, or ended links.

I31. Candidate schema contains no event column or event kind that exists only
for Concerns, membership identifiers, or ended link episodes.

I32. Boot refuses an unregistered or mismatched Toplines schema before it
writes DDL or product rows.

I33. Candidate upgrade, restart, rollback, and re-upgrade preserve existing
work-item identifiers and Topline rows.

I34. `0.1.9` and `0.2.0` expose the same retained command names, parameter
shapes, success shapes, refusal slugs, authorization outcomes, and ordering.

I35. A lane starts after it records its Exact target revision, a green baseline,
its accepted predecessor evidence, and an independently reviewed specification
hash.

I36. The delivery graph contains Lane 1, Lane 2, Lane 3, Lane 4, and one Final
full-scope review. A correction review is not an implementation lane.

I37. Lane 3 is the sole reconciler for this amendment. It preserves Reviewed
Lane 2 behavior and removes only the surfaces listed in R8.

I38. Lane 4 changes package and smoke paths. A semantic defect returns to Lane
3 and regenerates downstream evidence.

I39. Lane evidence uses full commits, SHA-256 values, exact commands, exit
status, test counts, changed paths, and cross-line deltas.

I40. No lane or review authorizes integration or release.

## Architecture

### R1. Stored state

`toplines` contains these logical fields:

| Field | Contract |
| --- | --- |
| `id` | Primary key with `tl_` prefix. |
| `ownerUserId` | Immutable existing user ID. |
| `title` | Canonical title. |
| `state` | `open` or `closed`. |
| `createdActorKind`, `createdActorRef` | Complete `user|session` pair. |
| `createdAt`, `updatedAt` | Integer Mutation times. |
| `closedAt` | Null while open; integer while closed. |

`topline_work_links` contains these logical fields:

| Field | Contract |
| --- | --- |
| `workItemId` | Primary key and foreign key to one work item. |
| `toplineId` | Foreign key to one Topline. |
| `ownerUserId` | Owner shared by both parents. |
| `linkReason` | Mutation reason. |
| `linkedActorKind`, `linkedActorRef` | Complete `user|session` pair. |
| `linkedAt` | Integer Mutation time. |

Composite foreign keys through `(id, ownerUserId)` make a cross-owner link
unrepresentable. The runtime returns `owner_mismatch` before insert when both
visible parents have different owners.

This direct-link table replaces the membership mechanism. Deleting the
membership surface removes multi-link and episode behavior. Accepting no ended
link row is safe because immutable audit events retain actor, reason, time,
Topline, and work item. A second state mechanism would duplicate that record.

`topline_events` contains `toplineId`, per-Topline `seq`, `kind`, optional
`workItemId`, actor pair, optional reason, Mutation time, and closed
kind-specific detail. Its kinds are `topline_created`, `topline_renamed`,
`topline_closed`, `topline_reopened`, `work_linked`, and `work_unlinked`.

`topline_idempotency` keys one stored request and response by owner, operation,
and Mutation key. The request fingerprint uses canonical UTF-8 JSON with exact
operation-specific parameters, sorted object keys, NFC strings, no
insignificant whitespace, and lowercase hexadecimal SHA-256. It excludes the
Mutation key, credentials, CLI version, and transport metadata.

The fingerprint parameter objects are closed: create uses Canonical `title`;
update uses `toplineId`, Canonical `title`, and `reason`; close and reopen use
`toplineId` and `reason`; link uses `toplineId`, `workItemId`, and `reason`;
unlink and leave-unlinked use `workItemId` and `reason`.

`topline_placement_obligations` stores the work item, owner, source edge,
causal watermark, state, prompt wake ID, opening actor and time, and resolution
actor, reason, kind, and time. State is `pending` or `resolved`. Resolution kind
is `linked`, `left_unlinked`, or `work_terminal`.

Each Placement decision has a primary key with prefix `tlp_`. Its source edge
is `created`, `reopened`, or `migration`. The database has one structural
unique index on
`(workItemId, sourceKind, COALESCE(sourceCausalSeq, 0))`. A current-package
reopen uses its positive durable causal-event sequence. Create and migration
use SQL null, with their distinct source kinds. These keys make a repeated edge
or boot unable to create a second decision.

`topline_schema_stamp` identifies the exact MVP schema. Its shape is
`standalone-toplines-mvp-v1`. The committed manifest lists each table, index,
and exact normalized `sqlite_schema.sql` value. A database that contains a
Toplines-owned object without the matching stamp receives
`unregistered_toplines_core_shape`. A different stamp or manifest receives
`unknown_toplines_schema_stamp` or `schema_shape_mismatch`. Each refusal leaves
the database unchanged.

`Tightbeam.Toplines` is the sole runtime DML seam for these tables. Work-item
transactions call its in-transaction placement functions. Rules and Execution
Map can read state but cannot mutate it.

### R2. Intent reads

`toplines [--state open|closed|all]` sends `toplines`. The default state is
`open`. It returns summaries ordered by `createdAt ASC, id ASC`:

```json
{"toplines":[{"activeWorkCount":1,"closedAt":null,"createdActor":{"kind":"session","ref":"agent:..."},"createdAt":123,"id":"tl_...","ownerUserId":"mike","state":"open","title":"Ship durable Toplines","updatedAt":456}]}
```

The summary has exactly the fields shown above. `activeWorkCount` counts Current
links. It has no Concern count, membership count, progress, assignment, or
Execution Map field.

`topline <toplineId> [--history]` sends `topline`. It returns the same summary
under `topline`, plus `workItems`. `workItems` sorts by `linkedAt ASC,
workItemId ASC` and contains Current-link objects. It contains current links
only. `--history` adds events in `seq ASC`; without that flag, the response has
no `history` field.

A Current-link object contains exactly:

```json
{"linkReason":"serves this ask","linkedActor":{"kind":"user","ref":"mike"},"linkedAt":123,"ownerUserId":"mike","toplineId":"tl_...","workItemId":"wi_...","workItemState":"open","workItemTitle":"Ship the feature"}
```

An event object contains exactly `actor`, `at`, `detail`, `kind`, `reason`,
`seq`, `toplineId`, and `workItemId`. `workItemId` and `reason` are JSON null
when the event kind does not use them. `detail` uses a closed shape for its
kind: creation has `title`; rename has `fromTitle` and `toTitle`; close and
reopen have `fromState` and `toState`; link has `linkReason`; unlink has
`unlinkReason`.

The CLI and Gateway treat a human request equivalent to "give me toplines" as
the default `toplines` read. Presentation can summarize titles, but it cannot
substitute Execution Map telemetry or infer a grouping.

### R3. Mutations and public shapes

The retained wire verbs match their CLI names:

- `topline-create --title <text> --key <key>`
- `topline-update <toplineId> --title <text> --reason <text> --key <key>`
- `topline-close <toplineId> --reason <text> --key <key>`
- `topline-reopen <toplineId> --reason <text> --key <key>`
- `topline-link-work <toplineId> <workItemId> --reason <text> --key <key>`
- `topline-unlink-work <workItemId> --reason <text> --key <key>`
- `topline-work-leave-unlinked <workItemId> --reason <text> --key <key>`
- `topline-placement-list [--state pending|resolved|all]`

Create, update, close, and reopen return `{"topline":<summary>}`. Link returns
`{"link":<current-link>,"resolvedPlacementId":<string-or-null>}`. Unlink
returns `{"toplineId":"tl_...","unlinkedWorkItemId":"wi_..."}`.
Leave-unlinked returns `{"placement":<placement>}`. The list returns
`{"placements":[...]}` in `openedAt ASC, id ASC` order.

A Placement object contains exactly `id`, `openedActor`, `openedAt`,
`ownerUserId`, `promptWakeId`, `resolutionActor`, `resolutionKind`,
`resolutionReason`, `resolvedAt`, `sourceCausalSeq`, `sourceKind`, `state`, and
`workItemId`. The four resolution fields are JSON null while pending.
`sourceCausalSeq` is JSON null for `created` and `migration`; it contains the
durable reopen sequence for `reopened`. The default placement-list state is
`pending`.

`topline-create` creates an open Topline for the caller's user. Update changes
the Canonical title. Close and reopen change state. A Canonical title equal to
the stored title returns `no_change` without an event or idempotency row.
Close retains Current links. Those links continue to satisfy
`work_item.has_topline`. An authorized caller can unlink from a closed Topline.
The public surface has no hard-delete verb.

Link re-reads the visible Topline and work item in one write transaction. It
requires an open Topline and equal owners. It can link a work item in any work
state. If `workItemId` already exists in `topline_work_links`, the handler
returns `work_already_linked` without changing it.

Unlink re-reads the Current link and both visible parents in one transaction.
It deletes the link, appends `work_unlinked` to the former Topline, and leaves
placement unchanged. A missing Current link returns `not_found`.

A committed update, close, reopen, link, or unlink sets the Topline's
`updatedAt` to that mutation's time. Create sets `createdAt` and `updatedAt` to
one sampled time.

The retained handler refusal map is:

| Slug | Message |
| --- | --- |
| `idempotency_conflict` | `idempotency key conflicts with a prior request` |
| `invalid_message` | `invalid message` |
| `invalid_transition` | `invalid state transition` |
| `no_change` | `no change` |
| `not_found` | `record not found` |
| `owner_mismatch` | `topline and work item owners differ` |
| `placement_not_pending` | `placement is not pending` |
| `process_denied` | `process principals cannot access Toplines` |
| `topline_closed` | `topline is closed` |
| `work_already_linked` | `work item already has a topline` |

Validation order is CLI compatibility; authentication and principal kind;
closed wire shape; owner-filtered visibility; owner equality; idempotency;
lifecycle state; structural uniqueness. The existing 426
`incompatible_cli` response runs before authentication or record lookup.

### R4. Execution Map separation

`execution-map` accepts the reviewed roster filters and tree option.
`execution-map-select` accepts exactly one reviewed selection by subtree or
assignment set. Both verbs stay read-only and non-targeted.

The implementation preserves each reviewed telemetry fixture and assertion
except command-name text. `toplines` and `topline` reject telemetry parameters.
Execution Map rejects Topline mutation or intent parameters. No alias maps a
retired shape to either surface.

### R5. Placement and wakes

The work-item create and reopen mutations evaluate the Placement edge inside
their write transaction. When the committed result is open and unlinked, the
transaction creates one pending Placement decision and one durable wake for
the owner's Main. The wake names the work item and provides the exact link and
leave-unlinked commands. It does not enumerate a foreign owner's Toplines.

If a link commits while a decision is pending, the same transaction resolves
the decision as `linked` and cancels a still-pending wake. If
leave-unlinked commits, the same transaction resolves it as `left_unlinked`.
If close, fail, or icebox commits, the same transaction resolves it as
`work_terminal`. A stale decision returns `placement_not_pending`.

The wake scheduler delivers at the observable turn boundary. It uses no delay
as a proxy for turn state. Delivery creates no new Placement decision or wake.

Candidate boot runs schema verification, rollback terminal reconciliation,
rollback reopen reconciliation, open-item reconciliation, then
wake recovery. Reopen and terminal reconciliation consume the greatest
qualifying durable causal event after the stored watermark. Open-item
reconciliation creates one `migration` decision for an open, unlinked work item
that has no Placement history. It runs after schema verification on each boot;
the structural source key makes later runs no-op for the same work item.
Reconciliation records `process:tightbeam` as the opening or resolution actor.
A repeated boot observes the stored edge key or advanced watermark and writes
no duplicate.

### R6. Authorization, privacy, and audit

The Gateway derives the acting user from the authenticated principal. A
mutation accepts no owner override. A session can act for its owner. An admin
can act on a visible foreign owner's rows, but a link still requires equal
Topline and work-item owners. A process principal receives `process_denied`.

Reads omit foreign rows and nested work data. Non-admin foreign and unknown IDs
return the same bytes. Evidence uses synthetic identities and redacts tokens.

Mutation response bytes, state rows, audit events, idempotency rows, placement
rows, and wake transitions commit in the transaction that owns the action.
Crash-before-commit leaves none of them. Crash-after-commit plus replay returns
the stored result without a second state change or event.

### R7. Schema, compatibility, and install law

The two Target lines use one logical Toplines manifest and one public contract.
Line-specific module layout can differ only when both evidence bundles name the
delta and prove the same observable result.

The `0.1.9` candidate declares Gateway, CLI, and package version `0.1.9`. The
main candidate declares version `0.2.0`. Each matching CLI uses the exact
version of its Gateway. Cross-version requests retain the existing 426 refusal.

The immutable previous-package fixture remains the real contract probe. The
test verifies the fixture digest before extraction or process start. It clears
inherited node identity, uses isolated ports and a disposable file database,
and records process logs and exit status.

For each Target line, the committed package smoke performs this sequence:

1. Boot the Previous-package Gateway and matching CLI on a new database.
2. Create a legacy work item through the real previous CLI/router and prove
   positive previous telemetry.
3. Stop the previous Gateway.
4. Boot the Candidate package on the same database and prove lossless upgrade,
   retained legacy identifiers, Execution Map, Topline intent, and restart
   idempotence.
5. Create a Topline, link one work item, create open work item `wi_terminal`,
   and deliver `wi_terminal`'s pending placement prompt through real Candidate
   paths.
6. Stop the Candidate and boot the Previous-package fixture on that database.
7. Prove previous telemetry still works, close `wi_terminal`, and create open
   work item `wi_migration` through previous public paths.
8. Stop the previous Gateway and re-upgrade the same database with the Candidate.
9. Prove the Topline and link bytes match their pre-rollback values, resolve
   `wi_terminal` as `work_terminal`, open one `migration` decision for
   `wi_migration`, preserve the fired wake history, and pass a second restart
   without duplicate rows.

The smoke uses packaged executables and real HTTP/wire routes. Direct handler
calls and handwritten success fixtures do not satisfy it. The smoke publishes
nothing and touches no live service or database.

### R8. Four-lane ledger and narrowing reconciliation

| Lane | State under this amendment | Exact evidence | Remaining duty |
| --- | --- | --- | --- |
| Lane 1 — schema and boot | Completed and landed as provenance | `0.1.9` `a8088e8fa540257c9f9674c4e011bf53ae909a27`; main `d0dbf34d4befbd1e46485960027363fff26b9d17`; landing `art_092ca5f9` | Lane 3 removes unshipped over-scope schema and installs the direct-link shape. |
| Lane 2 — Gateway, router, and CLI | Completed and reviewed-clean as targetless provenance | `0.1.9` `9c45e34af46aba451ac84ea5795a50a4a16fdafd`; main `5adc6f03e0469aa399b14a312985f92ea5036107`; `att_75de3a99`; `art_32e37248` | Lane 3 reconciles retained behavior to owner-recorded targets and strips removed commands and fields. |
| Lane 3 — MVP reconciliation, placement, and wakes | Closed until this exact spec amendment is independently reviewed | No candidate yet | Perform the sole target-correct reconciliation, narrowing, placement, wake, focused tests, dual-line review, and guarded integration candidate. |
| Lane 4 — package and rollback proof | Closed until Lane 3 returns one reviewed-clean dual-line result | No candidate yet | Build real packages and commit the install-law smoke on both lines. |

Lane 3 starts from owner-recorded Exact target revisions. It treats the two
Reviewed Lane 2 commits as semantic patch provenance, not moving targets. It
preserves target changes and the Reviewed Lane 2 behavior. It removes these
feature-only surfaces and no unrelated byte:

| Product path or symbol | Required reconciliation |
| --- | --- |
| `lib/tightbeam/toplines/schema.ex` and schema manifest tests | Remove `topline_work_memberships`, `topline_concerns`, `topline_concern_refs`, their indexes, membership/Concern event columns, and Concern event kinds. Add `topline_work_links` keyed by `workItemId`. Keep Topline, event, idempotency, placement, and stamp rails. |
| `lib/tightbeam/toplines.ex` | Remove the six Concern handlers and helpers, Concern projections, `openConcernCount`, `concerns`, `membershipId`, `endedConcernReferenceIds`, ended-link queries, and episode/relink code. Adapt retained link, unlink, read, placement, fact, event, and idempotency paths to Current links. |
| `lib/tightbeam/gateway.ex` | Remove registrations for `topline-concern-create`, `topline-concern-update`, `topline-concern-resolve`, `topline-concern-reopen`, `topline-concern-link-work`, and `topline-concern-unlink-work`. Preserve the eight retained Topline verbs and two Execution Map verbs. |
| `cli/src/args.rs` | Remove the six Concern commands, flags, help, allow-list entries, and parser fixtures. Change `topline-unlink-work` from `membershipId` to `workItemId`. Preserve closed-shape and before-I/O refusal tests. |
| `cli/src/dispatch.rs` | Remove six Concern request bodies and tests. Change retained unlink JSON from `membershipId` to `workItemId`. |
| `lib/tightbeam/rules.ex` | Read `work_item.has_topline` from `topline_work_links`. Preserve its typed unavailable behavior and no-default-statute rule. |
| `lib/tightbeam/firehose/registry.ex` and proof tests, where present | Remove Concern notice kinds and membership identifiers. Preserve retained Topline and work-link audit notices with `toplineId` and `workItemId`. |
| `test/toplines_test.exs`, `test/toplines_rails_test.exs`, `test/toplines_schema_test.exs`, `test/cli_integration_test.exs`, CLI unit tests, and corresponding line-specific tests | Delete Concern, multi-link, membership-episode, stale-membership-ID, Concern corruption, and Concern lifecycle cases. Adapt retained cases to direct links. Preserve Execution Map, authorization, early refusal, idempotency, restart, previous-package, and same-database upgrade proofs. |

No migration from the unshipped superseded candidate schema is required. Lane
3 proves that a fresh baseline creates only the MVP manifest and that a
database carrying an unregistered superseded shape refuses without mutation.

Lane 3 produces two exact targetless candidates and two evidence bundles. One
independent dual-line review must return reviewed-clean before the product
owner can authorize guarded target integration or open Lane 4. The review maps
each removed symbol and each retained behavior to exact diff and test evidence.

Lane 4 starts only from owner-accepted Lane 3 commits. It owns package assembly,
`scripts/feature_smoke.exs`, package-only support files, and the R7 proof. It
changes no Toplines schema, state machine, Gateway handler, router, CLI
semantics, work-item lifecycle, wake semantics, REST route, or identity state.

### R9. Final full-scope review and no-release gate

After Lane 4 produces both exact candidates, package hashes, and evidence
bundles, the product owner opens one independent Final full-scope review. The
reviewer reads this exact reviewed spec, the complete dual-line diffs, the Lane
1 and Lane 2 provenance, both Lane 3 bundles, and both Lane 4 bundles. The
reviewer reruns committed focused suites and both package smokes in clean
worktrees.

The reviewer verifies identical retained semantics across lines, the complete
absence of removed surfaces, exactly four implementation lanes, privacy,
refusals, upgrade, rollback, re-upgrade, process cleanup, and the no-release
gate. The reviewer writes no candidate byte. A reviewed-clean result makes the
candidates eligible for a separate owner decision. It does not integrate or
release them.

## Acceptance

AC1. Given user `mike` and title `Ship durable Toplines`, when Mike runs
`topline-create --title "Ship durable Toplines" --key k1`, then Tightbeam
stores one open `tl_` row owned by Mike, records Mike's principal, appends event
sequence 1, and returns the exact Topline summary shape from R2.

AC2. Given Mike owns two Toplines, another user owns one, and each row has a
distinct title, when Mike runs `toplines`, then the response contains Mike's
two open titles in `createdAt ASC, id ASC` order and contains no foreign title,
work progress, assignment, Concern, membership, or Execution Map field.

AC3. Given one Topline linked to two work items, when its owner runs
`topline <id>`, then `workItems` contains two current-link objects in
`linkedAt ASC, workItemId ASC` order and exposes no membership identifier.

AC4. Given the reviewed telemetry fixtures, when both Target-line candidates
run `execution-map` and `execution-map-select`, then each non-command-name
field, filter, order, cursor, tree edge, authorization omission, and refusal
matches its reviewed fixture.

AC5. Given telemetry parameters on `toplines` or `topline`, when the matching
CLI sends the request, then the parser returns `invalid_message` before handler
I/O. Given Topline parameters on an Execution Map verb, the same boundary
returns `invalid_message`.

AC6. Given a matching CLI and an open same-owner Topline and work item, when the
owner runs `topline-link-work <tl> <wi> --reason "serves this ask" --key k2`,
then one `topline_work_links` row exists for the work item, one `work_linked`
event exists, and the response names the Current link and any resolved
Placement decision.

AC7. Given a work item linked to `tl_a`, when an authorized caller tries to
link it to `tl_b` with a new key, then the handler returns
`work_already_linked`, retains `tl_a`, and appends no event.

AC8. Given a Current link from work item `wi_a` to `tl_a`, when the owner runs
`topline-unlink-work wi_a --reason "no longer serves the ask" --key k3`, then
the link row is absent, `tl_a` contains one `work_unlinked` event naming
`wi_a`, and no Placement decision or wake is created.

AC9. Given direct SQL attempts to insert two `topline_work_links` rows for one
`workItemId`, when SQLite enforces the manifest, then the second insert fails at
the primary-key rail and the database contains one link.

AC10. Given a Topline owned by user A and a work item owned by user B, when an
admin attempts to link them, then the handler returns `owner_mismatch`, and the
composite foreign-key fixture also rejects a direct SQL cross-owner row.

AC11. Given a committed mutation under key `k4`, when the currently authorized
caller repeats the same operation and parameters after Gateway restart, then
the response bytes match and row and event counts do not change.

AC12. Given key `k4` committed for one fingerprint, when the caller changes one
parameter, then the handler returns `idempotency_conflict` and changes no row.

AC13. Given a foreign Topline ID and an unknown Topline ID, when a non-admin
caller performs the same read or mutation, then both responses are byte-equal
`not_found` results.

AC14. Given a process principal, when it sends a public Topline read or
mutation, then the handler returns `process_denied` and reads no hidden row into
the response.

AC15. Given a mismatched pre-1.0 CLI, when it sends a request with valid,
invalid, foreign, or unknown identifiers, then the Gateway returns its existing
HTTP 426 `incompatible_cli` bytes before authentication or lookup.

AC16. Given an open unlinked work item created by the current Candidate, when
the create transaction commits, then it also commits one pending Placement
decision and one durable wake addressed to the owner's Main.

AC17. Given the pending decision from AC16, when its wake is delivered, then
the prompt names the work item, offers one explicit link command and one
leave-unlinked command, and schedules no second wake.

AC18. Given the pending decision from AC16, when the owner runs
`topline-work-leave-unlinked <wi> --reason "standalone work" --key k5`, then
the decision becomes `resolved/left_unlinked`, a still-pending wake becomes
canceled, and the work item remains unlinked and usable.

AC19. Given a resolved placement decision and an iceboxed work item, when the
owner reopens it, then the reopen transaction creates one new pending decision
and one wake. A second Gateway boot creates neither duplicate.

AC20. Given a pending decision whose wake already fired, when the work item
closes, then the decision resolves as `work_terminal` and the fired wake row
and delivered turn remain byte-identical.

AC21. Given a previous package created an open, unlinked work item with no
Placement history, when the Candidate boots, then open-item reconciliation
creates one `migration` decision and one prompt. A second boot leaves their row
counts unchanged.

AC22. Given an absent work-item context, an unknown work item, a foreign work
item, an unlinked visible work item, and a linked visible work item, when Rules
loads `work_item.has_topline`, then it returns the existing typed unavailable
result for the first three, `false` for the fourth, and `true` for the fifth.

AC23. Given a fresh baseline database, when Candidate boot activates Toplines,
then the schema matches the committed MVP manifest and contains no object or
column named for Concern, Concern reference, Work membership, membership ID,
or ended link.

AC24. Given one object from the superseded unshipped schema without the MVP
stamp, when Candidate boot runs, then it returns
`unregistered_toplines_core_shape`, preserves the database hash, and exposes no
Topline handler.

AC25. Given the exact Reviewed Lane 2 candidates, when Lane 3 reconciles them
to owner-recorded targets, then its changed-path ledger accounts for each R8
removal, retains each Reviewed Lane 2 behavior, and contains no unrelated
product change.

AC26. Given the candidate source and CLI help, when a source guard searches the
closed removed set, then it finds none of the six Concern command names,
`membershipId`, `openConcernCount`, `endedConcernReferenceIds`,
`topline_concerns`, `topline_concern_refs`, or
`topline_work_memberships` in runtime, schema, help, migration, or public test
fixtures.

AC27. Given exact package digests and a disposable database, when each Target
line runs the nine-step R7 smoke, then the previous Gateway proves positive
legacy telemetry, Candidate upgrade and restart preserve identifiers, rollback
preserves Candidate-created Topline bytes, and re-upgrade reconciles one
rollback-era edge without duplicate state.

AC28. Given the R7 smoke ends, when the harness checks processes, ports,
temporary credentials, and logs, then no process or port remains, no token
appears in evidence, and no live path was accessed.

AC29. Given this exact amendment lacks a reviewed-clean specification verdict,
when Lane 3 evaluates its start gate, then it records
`specification_review_missing` and changes no product byte.

AC30. Given reviewed-clean Lane 3 candidates are absent, when Lane 4 evaluates
its start gate, then it records `lane_3_contract_missing` and starts no package
process.

AC31. Given both Lane 4 candidates and their evidence bundles, when the product
owner opens Final full-scope review, then the assignment names this file's
reviewed SHA-256, both exact commits, both package hashes, the Previous-package
digests, and all Lane 3 and Lane 4 artifacts.

AC32. Given Final full-scope review, when the reviewer maps the contract, then
the report maps G1 through G12, NG1 through NG17, I1 through I40, R1 through R9,
and AC1 through AC34 to exact source, tests, and evidence on both lines.

AC33. Given a reviewed-clean Final full-scope report, when an actor checks its
authority, then it authorizes no target push, merge, release, publication,
deployment, service restart, live migration, or live database mutation.

AC34. Given a closed Topline with one Current link, when the owner reads the
Topline and the rail fact, then the read contains that work item and the fact is
`true`. When the owner unlinks it, the link disappears and the closed Topline
retains its audit history.

### Traceability

| Requirement group | Architecture | Acceptance |
| --- | --- | --- |
| G1-G5, I1-I19 | R1-R3, R6 | AC1-AC15 |
| G6, I11-I12 | R2, R4 | AC2-AC5 |
| G7, I20-I27 | R5 | AC16-AC21 |
| G8-G9, I13-I19, I28-I29 | R3, R6 | AC10-AC15, AC22 |
| G10-G12, I30-I40 | R7-R9 | AC23-AC34 |
| NG2-NG5, NG15 | R1, R3, R8 | AC7-AC9, AC23-AC26 |
| NG6-NG10 | R2, R4-R5 | AC2-AC5, AC16-AC21 |
| NG11-NG14, NG16-NG17 | R7-R9 | AC27-AC34 |

## Open Questions

None. This amendment has no blocking or non-blocking product hole. The named
follow-on candidate carries the deferred Concern and multi-membership questions
without expanding this MVP.
