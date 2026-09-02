# Standalone Toplines V5 successor for 0.1.9 and 0.2.0

Canonical path: `standalone-toplines-v5.md`

**Spec homing and canonical set.** The canonical home is the
`clickety-clacks/tightbeam-specs` repository. The complete canonical set for
this successor contains exactly these repository-root paths at one exact
repository commit:

- `standalone-toplines-v5.md` is the canonical standalone product
  specification. It governs the Toplines product behavior, the two Target
  lines, the four Implementation lanes, their evidence, the Final full-scope
  review, and the No-release gate.
- `v0.2-program-2026-08-12.md` governs only the negative program-membership
  fact: the old `wi_35abce19` Toplines row is absent and no replacement
  Toplines phase or hierarchy row exists. It supplies no Toplines product
  requirement, Target-line revision, implementation custody, or release
  authority.

The deletion of the `wi_35abce19` row from
`v0.2-program-2026-08-12.md` is the paired homing change that removes Toplines
from every v0.2 program phase and hierarchy.
The two-file canonical set, not either file alone, carries this
specification-only transition.
The exact repository commit plus the SHA-256 of each file identifies this set
for specification review. After reviewed-clean, the work item's `--spec-ref`
and `--spec-sha256` values bind `standalone-toplines-v5.md`; the same reviewed
commit and the paired program-file SHA-256 preserve the negative
program-membership evidence.
A later material change amends the file that owns that authority, then presents
both canonical paths from one new exact commit for independent review.

The reviewed V5 artifact, the co-reviewed REST contract, the program-removal
artifact, prior work-item rows, messages, worktrees, and review reports are
authority or provenance inputs. They are not additional canonical custody and
cannot amend either canonical file. The REST contract remains the separate
canonical contract for REST transport. Its exact pinned commit constrains the
shared query and projection boundary without joining this custody set.

Work item: `wi_875fbdd5-6756-4149-b032-f055dc4f965c`

Prior work item: `wi_35abce19-8d05-4a18-90db-335cabe0893c` is provenance only.
It supplies reviewed design and implementation evidence. It does not place this
work in a program phase and it does not carry implementation custody.

Status: targetless spec amendment candidate. Independent specification
re-review is required before the work item can bind this file as implementation
authority.

Authority and evidence:

- Mike's ruling of 2026-09-01 on
  `wi_875fbdd5-6756-4149-b032-f055dc4f965c` preserves G3 and redefines a
  Concern as a user- or agent-applied tag inside exactly one Topline. It selects
  D1=A: unlinking a Work membership creates no Placement obligation or prompt.
  This ruling supersedes removal proposal `art_8224f898`; that artifact remains
  provenance only and supplies no current requirement.
- Prior reviewed specification commit
  `3c83d382968f242ebab660f9b67593aa80a1e84e` carried this file at SHA-256
  `1ffc9ee7b984df672b21d46d7a6f3cd3a40b274bd4cec8943377ca47c17881d6`.
  This amendment changes only `standalone-toplines-v5.md` and the separate
  canonical REST contract `rest-state-api-v1.md` in one targetless candidate.
- Lane 2 independent review found product candidates
  `5adc6f03e0469aa399b14a312985f92ea5036107` for main and
  `9c45e34af46aba451ac84ea5795a50a4a16fdafd` for 0.1.9 reviewed-clean. Those
  candidates are evidence inputs only. This assignment does not modify, land,
  or release either candidate.

- Independent exact-tip review
  `asg_afd2c88f-e685-4c64-9b5a-6b8957bf3930` verified commit
  `39a063df882fb6a8ed3a79b1e0571da3f3155e6f`, both file hashes, and the
  product contract, then returned `changes-requested` in
  `att_64ea68a8-1927-4aa1-b01e-b5ba286e319a`. Its SHA-bound report
  `art_6e1f6de9` identified one blocking finding: the candidate did not state
  its canonical set or split the authority of the paired program-row deletion.
  This amendment adds that boundary without changing a product behavior,
  Target line, lane, program byte, or release authority.
- Mike authorized one standalone Toplines deliverable for product targets
  `0.1.9` and `0.2.0` in message
  `s_17b635eb-05be-4644-bab0-aed66fc18d38`. The same ruling authorizes no
  release action and forbids inference of an unverified `0.2.0` product-line
  revision.
- Coordination with `product-owner:tightbeam-0-2-0` is limited to the explicit
  `0.2.0` target assumptions and current-line evidence in Mike's ruling. It
  carries no implementation, packaging, integration, or release custody and
  supplies no verified `0.2.0` product-line revision at specification time.
- Program-document commit
  `e7d5dd3b6a0132017ffa78b2699d0823ba4eb06e` removes the only
  `wi_35abce19` row from `v0.2-program-2026-08-12.md`. Durable artifact
  `art_83f21481`, titled `Toplines removed from v0.2 program`, records those
  bytes at SHA-256
  `987a9d7c7ecd3353d851649b6ec9c701f56106fbf12b8dd364c442d7fec5fbb4`.
  Toplines therefore belongs to no v0.2 phase or program hierarchy.
- Commit pointer `c63067846cfb4ae4ba9b6295d79370064af18090` is the recorded but
  unavailable deferral-release basis pointer. It was absent from the canonical
  repository refs after a fresh fetch and exact remote lookup. Mike's later
  direct clarification supersedes it for removal proof. This specification
  does not treat it as byte authority and does not invent or publish the missing
  object. Full commit
  `e7d5dd3b6a0132017ffa78b2699d0823ba4eb06e` and `art_83f21481` supply the
  current verified program-document bytes and removal proof.
- Reviewed V5 artifact `art_e275210f`, SHA-256
  `d39dd61cb44f5c6ff0bbc301b28d64a893b294d1a894e148b1449b36d5585bf9`,
  supplies the complete behavioral contract reproduced below. Independent
  review assignment `asg_92c0fd41-364f-4855-8146-ad2a2afbc50a` found that
  artifact reviewed-clean.
- Tightbeam specs commit
  `05d08b8af74a877d4dabe3dcba8250787d5d430e` supplies the REST Toplines
  state, cursor, projection, and shared-query contract. This specification
  narrows only its temporary CLI-name retention rule as stated in I77. It does
  not replace the REST routes or their response contract.
- Integrated core commit
  `0b52dcfb78b5ce7d9a8925fa194e44401825c30d` and prior work-item evidence
  supply implementation provenance for the Completed core defined below. They
  are not current `0.2.0` target-line authority. Each lane shall verify its
  target revision before it relies on those bytes.

## Goal

G1. Tightbeam shall store each human-level Topline as durable intent that belongs
to one user.

G2. Tightbeam shall store direct, explicit, attributable, reason-carrying
memberships between Toplines and work items.

G3. One work item shall support active membership in more than one Topline.

G4. A user or an authorized agent shall decide each membership. Tightbeam shall
record that decision. Tightbeam shall not infer or silently write a membership.

G5. Tightbeam shall prompt the responsible user's Main once when Work Item
creation, Work Item reopen, or first activation migration leaves an open work
item without a Topline decision. Membership unlink is not a placement event.

G6. Tightbeam shall keep current execution telemetry under the name Execution
Map. Existing telemetry data, filters, ordering, authorization, and read-only
behavior shall remain unchanged. Command-name text shall use the new name.

G7. Tightbeam shall expose Toplines and Execution Map through distinct CLI and
wire operations.

G8. Tightbeam shall expose one typed rail fact that reports whether the call's
work item has an active Topline membership.

G9. Tightbeam shall implement G1 through G8 with the same observable contract
on the `0.1.9` and `0.2.0` target lines.

G10. The implementation shall divide the remaining work into exactly four
implementation lanes: schema and boot; Gateway, router, and CLI; placement and
wakes; and packaging and rollback proof.

G11. The implementation shall preserve and re-prove the Completed core. It
shall add only the remaining seams required by this specification.

G12. One independent full-scope review shall evaluate both exact target-line
candidates after all four lanes pass.

## Non-Goals

NG1. A Topline is not a work item. It has no assignment holder, implementation
status, estimate, completion percentage, or execution lifecycle.

NG2. A Concern tag does not own work-item membership. Applying or removing a
Concern tag does not add, remove, or imply a Topline membership.

NG3. Tightbeam does not rank Toplines or work items. It does not calculate
importance, relevance, confidence, priority, or placement.

NG4. Tightbeam does not start a separate inference session to place work.

NG5. Tightbeam does not install a default statute for the new rail fact.

NG6. Tightbeam does not add a periodic placement scan, timer, re-nag loop, or
threshold that decides placement.

NG7. Tightbeam does not hard-delete Toplines, Concern definitions,
memberships, placement decisions, or their events. Removing a Concern tag from
a Work membership deletes the current tag-association row because that row is
not history.

NG8. Tightbeam does not change Work Item ownership or assignment resolution.

NG9. Tightbeam does not treat current concurrent-turn ancestry as intent or as
Topline membership.

NG10. Tightbeam does not preserve the old telemetry wire meanings of `toplines`
and `topline` as aliases.

NG11. Tightbeam does not add Topline presentation policy to Clawline or another
consumer in this work.

NG12. This work does not belong to a v0.2 program phase. It does not depend on
status-responder Phase 5 or another v0.2 program milestone.

NG13. This spec-authoring assignment and its independent review do not authorize
product implementation, branch integration, merge, release, deployment,
service restart, database migration, or live-state mutation. Implementation
requires a later assignment bound to the independently reviewed file hash.

NG14. This work does not re-specify or implement the REST `/api/toplines`
routes, REST cursor format, REST adapters, Firehose notices, or REST pagination.
It supplies only the shared query and projection seams that the REST contract
assigns to `Tightbeam.Toplines`.

NG15. This specification does not name or infer an exact current `0.2.0`
product revision. A product-line owner shall supply that revision at lane
start.

NG16. Product version `0.1.8` is not an implementation target. A `0.1.8`
package can serve only as an owner-approved previous-package rollback fixture
for the `0.1.9` candidate.

NG17. A reviewed-clean final report is not release approval. Release remains a
separate owner decision after this specification's scope ends.

NG18. Tightbeam does not infer or automatically migrate an unregistered partial
Toplines core database. Production boot refuses that database without changing
it. The operator can preserve it for diagnosis or replace a disposable database
under separate authority.

## Terms

**Topline.** A durable item that one user keeps at the top of mind. A Topline
groups related work through explicit membership rows. Its identifier starts
with `tl_`.

**Topline owner.** The user whose intent the Topline records. A session acts for
the user in its `ownerUserId` field.

**Work membership.** One active or ended episode that links one Topline to one
work item. Its identifier starts with `tlm_`. The episode carries the linking
reason and actor. An unlink ends that episode. A later relink creates a new
episode.

**Active membership.** A Work membership whose `unlinkedAt` field is null.

**Concern.** An optional, durable tag definition that belongs to exactly one
Topline. Its identifier starts with `tlc_`. A Concern groups active Work
memberships inside its owning Topline. It has no open/resolved lifecycle.

**Concern tag association.** The current many-to-many association between one
Concern and one active Work membership in the same Topline. The association is
current state, not an episode and not history. One Work membership can carry
many Concerns. One Concern can tag many Work memberships.

**Related agents and proofs.** Assignments, sessions, attests, and artifacts stay
attached to their Work Items. A Topline does not copy those rows. Its Work
membership IDs make them reachable through existing Work Item reads and
Execution Map.

**Placement obligation.** A durable record that an open work item has no active
Topline membership and needs an attributable decision. Its identifier starts
with `tlp_`.

**Placement episode.** The interval from one qualifying unplaced event until a
link, an explicit leave-unlinked decision, or a terminal Work Item disposition
resolves the obligation.

**Placement causal watermark.** The value stored in an obligation's
`historyCausalSeq` field. It is `COALESCE(MAX(causal_events.seq), 0)` as visible
inside the transaction at that obligation's latest state mutation: its insert
while pending or its transition from pending to a resolved state. It is an
observation boundary in the global causal-event commit order, not a Topline
event sequence and not a claim that every causal event belongs to that Work
Item.

**Qualifying rollback-era reopen.** For a Work Item with placement history, let
`H` be the greatest Placement causal watermark in that history. A candidate is
a `causal_events` row whose `seq > H`, `kind = "disposition_transition"`,
`jobRef` equals the Work Item ID, and whose JSON values at `workItemId`,
`fromState`, and `toState` equal that ID, `"iceboxed"`, and `"open"`
respectively. The qualifying event is the candidate with greatest `seq`. It
qualifies only while the current Work Item is open, has zero active memberships,
and has no pending placement obligation. Event `seq`, not event time, decides
order because millisecond times can tie.

**Qualifying rollback-era terminal disposition.** For a pending Placement
obligation with watermark `H`, this is the greatest `causal_events.seq > H`
whose row has `kind = "disposition_transition"`, `jobRef` equal to the
obligation's Work Item ID, and JSON values at `workItemId` and `toState` equal
that ID and the Work Item's current `closed`, `failed`, or `iceboxed` state. It
qualifies only while the Work Item remains in that terminal state. Event `seq`,
not event time, decides order.

**Re-upgrade terminal reconciliation.** The first reconciliation phase of every
release boot, after schema creation. It resolves a pending Placement obligation
when its Work Item has a Qualifying rollback-era terminal disposition. The
process records itself as the repair actor. It does not claim to be the actor
that made the old-gateway terminal decision.

**Execution Map.** The read-only work telemetry currently implemented by
`Tightbeam.Toplines` at the source baseline. It includes the roster, causal
forest, subtree, and assignment-selection views. Its ancestry records
concurrent-turn evidence, not intent.

**Responsible user.** The work item's durable `ownerUserId`. Placement prompts
go to that user's personal Main session.

**Actor.** The principal attributable for an action. A stored or returned actor
is one discriminated pair: `actorKind` plus `actorRef`. `actorKind` is `user`,
`session`, or, only for boot reconciliation, `process`. `actorRef` is the exact
user ID, session key, or `tightbeam`. No row stores parallel nullable user and
session actor columns.

**Mutation key.** A caller-supplied idempotency key. It is non-blank text with a
maximum length of 200 Unicode characters.

**Mutation reason.** Caller-supplied text whose trimmed length is from 1 through
4,000 Unicode characters. The substrate stores the supplied text verbatim.

**Mutation time.** One millisecond clock value sampled inside a write
transaction and reused for the current-state rows, event rows, obligation rows,
and wake rows that the mutation writes.

**Canonical title.** The result of removing the maximal leading and trailing
sequence of Unicode White_Space code points, then normalizing the remainder to
Unicode Normalization Form C (NFC), using Unicode 15.1 data. White_Space is the
closed set U+0009 through U+000D, U+0020, U+0085, U+00A0, U+1680, U+2000 through
U+200A, U+2028, U+2029, U+202F, U+205F, and U+3000. Title length counts Unicode
scalar values after this transformation; it does not count bytes, UTF-16 code
units, or grapheme clusters.

**Fingerprint JSON.** The UTF-8 bytes of one object with exactly the keys
`operation` and `parameters`. `operation` is the exact lowercase wire verb.
`parameters` is the operation-specific object in R5. The serializer sorts object
keys by UTF-8 byte order, preserves array order, emits `true`, `false`, and `null`
literally, emits integers as shortest base-10 text with zero represented as `0`,
and emits no insignificant whitespace. Before serialization, it normalizes each
string key and value to NFC with Unicode 15.1 data. A string escapes U+0022 as
`\"`, U+005C as `\\`, and U+0000 through U+001F as lowercase six-byte `\u00xx`;
it emits each other Unicode scalar value directly as UTF-8, including U+002F,
U+2028, and U+2029. The wire validator rejects invalid UTF-8, unpaired surrogate
escapes, and duplicate object keys before fingerprinting.

**Request fingerprint.** The lowercase hexadecimal SHA-256 of Fingerprint JSON.
It excludes `idempotencyKey`, credentials, CLI version, and transport metadata.

**Visible row.** A row that the caller can read under the owner-or-admin rule in
I18 through I21.

**V5 contract.** Goals G1 through G8, Non-Goals NG1 through NG11, Terms,
Assumptions A1 through A12, Invariants I1 through I66, Architecture R1 through
R14, and Acceptance AC1 through AC87 as behaviorally reproduced in this file.
The successor adds delivery rails and makes the first-production-activation
refusal explicit where the Completed core supplied no registered production
schema. Those delivery clarifications do not weaken the V5 user contract.

**Target line.** One of the two Mike-authorized product destinations:
`0.1.9` or `0.2.0`. A target line is a product maintenance line, not this
specification branch and not a v0.2 program phase.

**Exact target revision.** The full 40-character product commit selected by the
responsible product-line owner as one lane's starting revision. A branch name,
moving ref, abbreviated commit, local worktree state, or inferred commit is not
an Exact target revision.

**Exact candidate revision.** The full 40-character product commit produced by
one lane, including the final Lane 4 commit presented to full-scope review. It
is immutable evidence, not a moving branch.

**Exact lane input revision.** The immutable commit from which one lane starts.
For Lane 1 it is the Exact target revision. For Lanes 2, 3, and 4 it is the
accepted candidate commit from the immediately preceding lane on the same
Target line.

**Candidate package.** An unshipped gateway and matching CLI built from one
Exact candidate revision for deterministic tests. In the inherited V5 clauses,
`new release`, `current release`, `release`, `ship`, and `shipped` refer to this
test candidate unless a clause explicitly names a separately authorized
release. Those words do not authorize release action.

**Previous-package fixture.** One owner-named, immutable gateway package and
its exact matching CLI from the same Target line. The evidence bundle records
both package versions and SHA-256 values. A builder cannot infer this fixture
from a version number or branch name.

**Source-baseline table.** A production table that existed at the reviewed V5
source baseline before the Completed core. The partial Toplines tables created
only by the unregistered core test seam are not Source-baseline tables.

**Toplines production schema stamp.** The singleton
`topline_schema_stamp` row. Its `singleton` field is integer 1, its `shape`
field is `standalone-toplines-v5`, and its `stampedAt` field is the activation
Mutation time. Lane 1 creates the row in the same transaction as the complete
R1 through R6 schema. It is separate from the product-wide `schema_stamp`.

**Toplines schema manifest.** Lane 1's committed, closed list of every table and
index that the Candidate creates under R1 through R6, plus
`topline_schema_stamp`. The manifest records each exact object name, object
type, and exact UTF-8 `sqlite_schema.sql` value. It includes `toplines`,
`topline_work_memberships`, `topline_events`, `topline_idempotency`,
`topline_concerns`, `topline_concern_tags`,
`topline_placement_obligations`, `topline_schema_stamp`, every supporting index
on those tables, `toplines_id_owner`, `work_items_id_owner`,
`topline_memberships_active_pair`, `topline_memberships_id_topline`,
`topline_memberships_work_active`, and the R6 parent index on
`causal_events`. The two Target lines use the same manifest. A prefix search or
an implementation-chosen object outside the manifest cannot decide schema
state.

**Unregistered core schema.** Any object in the closed Toplines schema object
manifest, other than the stamp table itself, that exists while the Toplines
production schema stamp row is absent. A stamp table with no singleton row is
also an Unregistered core schema. The Completed core could create the first
four tables and its supporting indexes only through its unregistered test and
integration seam. Their presence proves neither a production shape nor a safe
migration source.

**Completed core.** The accepted, self-contained Toplines implementation
proven by prior work-item evidence: Topline create, link, unlink, list, and get;
Execution Map extraction with compatibility delegates; direct-membership
truth; and the boolean `work_item.has_topline` Rules fact. The exact target
revision must contain equivalent behavior before a lane can classify it as
complete.

**Remaining scope.** Each V5 requirement not satisfied by the Completed core.
It includes the full structural schema and boot rails, Concerns, events,
idempotency, canonical titles, public projections, final Gateway/router/CLI
surface, placement and wake lifecycle, package-version binding, and real
rollback proof.

**Implementation lane.** One owned product mutation seam with a closed
acceptance map, target-line inputs, deterministic tests, and commit-bound
evidence. This specification defines exactly four Implementation lanes.

**Lane evidence bundle.** One immutable report for one lane and one Target
line. It records the root Exact target revision, the Exact lane input revision,
the exact candidate commit after work, changed paths, commands, exit status,
test counts, package hashes when applicable, fixture hashes, and each allowed
line-specific delta.

**Independent specification review.** The pre-implementation review of this
exact canonical file by a different session. It checks authority, completeness,
internal consistency, atomic requirements, acceptance traceability, and marked
holes. It reviews no product candidate and satisfies no Implementation lane or
Final full-scope review gate.

**Final full-scope review.** One independent review assignment, held by a
session that wrote none of the candidate commits, which evaluates both exact
target-line candidates and all eight Lane evidence bundles against this entire
file.

**No-release gate.** A hard boundary throughout this work and after final
review. No state in this work item, including `reviewed-clean`, authorizes
merge, release, deployment, service mutation, or live migration.

## Assumptions

A1. A Work Item belongs to one user. Current source derives a session-created
item's owner from the session owner.

A2. Each user has a personal Main session key. Current Work Item lifecycle wakes
already address that key.

A3. SQLite transactions serialize competing writes. A transaction either
commits its state and event rows together or commits none of them.

A4. Pending wakes survive gateway restart. The existing wake scheduler claims a
pending wake once.

A5. The current release is below version 1.0. The gateway therefore requires an
exact CLI version match before it authenticates or dispatches a CLI request.

A6. The source baseline's Execution Map proofs define current observable
telemetry behavior. They cover authorization by omission, deterministic order,
assignment resolution, causal cycles, coverage, filters, and read-only dispatch.

A7. The source baseline permits additive production tables and supporting
indexes without changing an existing table. It refuses unknown changes to an
existing stamped shape.

A8. `work-item-create`, `work-item-reopen`, Topline membership mutation, and Work
Item terminal disposition can call an in-transaction Topline seam.

A9. A work item remains useful when it has no Topline. Unplaced is a named state,
not a write refusal or a hold.

A10. An admin can read and mutate another user's visible rows. An admin cannot
link a Topline and a work item whose owners differ.

A11. Each source-baseline database connection enables SQLite foreign-key
enforcement before it reads or writes product rows.

A12. The source-baseline `causal_events.seq` is a durable, positive, global
commit order. Every successful Work Item close, fail, icebox, or reopen appends
one `disposition_transition` row in the same transaction as the state change.
Its detail preserves exact `workItemId`, `fromState`, and `toState` values.

A13. Mike's target ruling supplies the product versions `0.1.9` and `0.2.0`.
It supplies no Exact target revision and no Previous-package fixture.

A14. The responsible product-line owner can supply an Exact target revision
and Previous-package fixture before an implementation lane starts. Absence of
either value is a named start refusal, not an Open Question in this design.
For `0.2.0`, the lane holder coordinates with
`product-owner:tightbeam-0-2-0` only to record owner-authorized target
assumptions and current-line evidence. That coordination performs no duplicate
implementation, packaging, integration, or release action.

A15. The two Target lines can differ in internal module layout, build plumbing,
and unrelated product behavior. Their Toplines wire bytes, persistence rules,
authorization, privacy, and restart outcomes can still satisfy one V5 contract.

A16. Prior work-item evidence is sufficient to classify the Completed core as
accepted provenance. It is not sufficient to prove that an unpinned target
revision still contains that core.

A17. The `rest-state-api-v1.md` file at the exact targetless candidate that
contains this amendment remains authoritative for REST routes, REST cursors,
REST response projection, and Firehose notices. The shared
`Tightbeam.Toplines.query_public/2` and
`Tightbeam.Toplines.public_item/1` seams can serve that contract without adding
REST transport code to this work.

A18. Each lane can run its database, wake, gateway, and package proofs against
disposable local fixtures. No acceptance case needs a live user database,
deployed service, production credential, or release operation.

### Source evidence

The implementation review used commit
`0f68be08604efaa77f914f5c6f50c4df4e5c1722` and these source facts:

- `lib/tightbeam/toplines.ex:1-40` defines current Toplines as pure telemetry,
  singular assignment membership, four-valued concurrent-turn ancestry, and
  authorization by omission.
- `lib/tightbeam/toplines.ex:49-87` defines the current `toplines` and `topline`
  read modes.
- `lib/tightbeam/toplines.ex:238-342` defines the current filters and node shape.
- `lib/tightbeam/toplines.ex:595-763` defines the telemetry world, visibility,
  deterministic assignment resolution, and item membership.
- `lib/tightbeam/toplines.ex:885-910` resolves the caller through the existing
  owner-or-admin rule.
- `lib/tightbeam/work_items.ex:1-47` defines Work Item ownership, states, and
  lifecycle wake fields.
- `lib/tightbeam/work_items.ex:62-132` creates an item and its routing wake in one
  transaction.
- `lib/tightbeam/work_items.ex:280-383` applies owner-or-admin dispositions and
  records disposition events.
- `lib/tightbeam/work_items.ex:395-589` implements the existing lifecycle wake
  seams.
- `lib/tightbeam/db.ex:9-10` and `lib/tightbeam/db.ex:104` pin
  `PRAGMA foreign_keys=ON` when a database connection opens.
- `lib/tightbeam/rules.ex:1-39` defines typed request-scoped rail facts.
- `lib/tightbeam/rules.ex:104-132` declares the closed fact type map.
- `lib/tightbeam/rules.ex:930-968` gives nil facts fail-closed matching behavior.
- `lib/tightbeam/rules.ex:1156-1215` shows the existing Work Item boolean-fact
  pattern.
- `lib/tightbeam/wire/router.ex:57` and `lib/tightbeam/gateway.ex:856-880` expose
  the current wire verbs.
- `cli/src/args.rs:260-288`, `cli/src/args.rs:392-410`, and
  `cli/src/dispatch.rs:411-458` expose the current CLI meanings.
- `lib/tightbeam/cli_compatibility.ex:1-46` and
  `lib/tightbeam/wire/router.ex:392-408` enforce exact pre-1.0 CLI matching and a
  `426 incompatible_cli` refusal.
- `test/toplines_test.exs:85-847` contains the current deterministic telemetry
  proofs and router refusal proofs.
- `scripts/feature_smoke.exs:1992-2057` exercises the current released telemetry
  CLI/wire path and therefore must move to the renamed commands rather than be
  replaced by handler-only tests.
- `lib/tightbeam/causal_events.ex:38-112` defines the durable global
  `causal_events.seq`, the `disposition_transition` kind, the `(jobRef, seq)`
  index, and in-transaction append.
- `lib/tightbeam/work_items.ex:291-351` changes Work Item state and appends the
  exact disposition transition in one transaction; reopen is
  `iceboxed -> open`.
- `test/job_forensics_test.exs:123-136` proves that icebox, reopen, and close
  append ordered transitions with exact from/to states.
- `lib/tightbeam/wakes.ex:60-85` defines the durable
  `pending|fired|canceled` wake state and its `firedAt` and `canceledAt`
  history.
- `lib/tightbeam/wakes.ex:223-253` provides the in-transaction pending-only
  cancellation seam. It leaves a fired wake unchanged.

Executable source verification was unavailable in the spec-writer session. At
`2026-08-11T09:38:38Z`, command
`mix test test/toplines_test.exs test/cli_compatibility_test.exs test/rules_transport_test.exs`
in `/home/mike/.tightbeam/work/f8899f5cc784/tightbeam-product` returned
`/bin/bash: line 1: mix: command not found`. The spec-writer used no alternate
runner and made no product-source edit.

### Successor evidence and completion status

The successor-authoring session verified these durable inputs on 2026-08-29:

- `art_e275210f` has SHA-256
  `d39dd61cb44f5c6ff0bbc301b28d64a893b294d1a894e148b1449b36d5585bf9`
  and contains the complete 2,045-line V5 contract reproduced here.
- Review assignment `asg_92c0fd41-364f-4855-8146-ad2a2afbc50a` reports
  `reviewed-clean` for those exact V5 bytes.
- Prior implementation evidence binds the Completed core to integrated commit
  `0b52dcfb78b5ce7d9a8925fa194e44401825c30d`. The bounded production paths
  were `lib/tightbeam/execution_map.ex`, `lib/tightbeam/toplines.ex`,
  `lib/tightbeam/rules.ex`, and their three focused test files.
- Prior exact review records 51 focused tests with zero failures and the full
  producer gate with 1,461 tests plus 9 doctests, zero failures, and 11 skips.
  These counts are historical evidence. A lane shall not substitute them for a
  fresh target-line test.
- CLI audit artifact `art_136fdede` found that the old surface had no complete
  byte-exact Toplines command matrix. It specifically lacked full mutation-key,
  unknown-alias, retired-verb, and early-version-refusal proof. Lane 2 owns that
  remaining evidence.
- Lane 2 independent review records reviewed-clean targetless product candidates
  at main `5adc6f03e0469aa399b14a312985f92ea5036107` and 0.1.9
  `9c45e34af46aba451ac84ea5795a50a4a16fdafd`. Those exact tips prove the
  pre-amendment Lane 2 surface. They do not satisfy or implement this later
  Concern-tag amendment and this specification assignment does not mutate them.
- Commit `05d08b8af74a877d4dabe3dcba8250787d5d430e` landed the REST Toplines
  contract after V5. Its shared query and projection seams constrain Lane 1.
  Its temporary retention of the old CLI meanings is superseded only as stated
  in I77.
- Commit `e7d5dd3b6a0132017ffa78b2699d0823ba4eb06e` and
  `art_83f21481` remove Toplines from every v0.2 program phase. The targetless
  specs commit that lands this file also removes the stale row from the current
  program document.

No product-line commit observed during authoring is an Exact target revision.
Lane evidence must establish the current line state again after an owner names
that revision.

## Invariants

I1. Direct active Work membership is the sole source of Topline membership.

I2. A Topline and each active Work membership in it have the same
`ownerUserId`.

I3. One `(toplineId, workItemId)` pair has at most one active Work membership.

I4. One work item can have active memberships in multiple Toplines owned by the
same user.

I5. A Work membership carries a non-blank link reason from its actor.

I6. Ending a Work membership carries a non-blank unlink reason from its actor.

I7. A relink creates a new membership ID. An old membership ID cannot end the
new episode.

I8. The substrate creates no membership without an authenticated user or
session mutation request.

I9. A placement prompt, causal edge, assignment, shared title, matching owner,
or Concern tag does not create membership.

I10. A Concern belongs to one Topline.

I11. A Concern tag association names an active Work membership in that same
Topline.

I12. A Concern tag association does not change the result of a Topline membership
query or the `work_item.has_topline` rail fact.

I13. Ending a Work membership deletes all of its Concern tag associations in
the same transaction. The unlink creates no Placement obligation or prompt.

I14. A Topline close retains its Work memberships, Concern definitions, current
Concern tag associations, and event history.

I15. A closed Topline accepts no new Work membership, Concern definition, or
Concern tag association. Its owner or an admin can end an existing membership
or remove an existing Concern tag association.

I16. Topline state is `open` or `closed`. A Concern has no lifecycle state.

I17. The substrate records each successful Topline, Work membership, Concern
definition, or explicit Concern tag mutation and its actor in the mutated
Topline's append-only event stream. Automatic tag removal during membership
unlink is part of the `work_unlinked` mutation and creates no derived tag event.
Placement obligations preserve their actors in their own rows.

I18. A non-admin user sees only Toplines owned by that user.

I19. A non-admin session sees only Toplines owned by that session's owner.

I20. An admin sees Toplines from each owner.

I21. For a non-admin caller, an unknown identifier and an identifier owned by a
different user produce byte-identical not-found responses.

I22. A response omits invisible memberships, Work Items, Concerns, tag
associations, counts, ordering effects, and history events.

I23. A process principal cannot invoke a public Topline read or mutation. The
internal boot reconciler can write only the process-attributed Placement and
wake transitions that R6 and R12 specify.

I24. Each mutating Topline wire operation requires a mutation key.

I25. For a currently authorized caller, a replay with the same caller user,
operation, key, and request fingerprint returns the stored response and writes
no row or wake.

I26. For a currently authorized caller, reuse of the same caller user,
operation, and key with a different request fingerprint returns
`idempotency_conflict` and writes no row or wake.

I27. A successful mutation commits its current-state rows, event rows,
idempotency response, placement changes, and wake changes in one transaction.

I28. A failed mutation commits none of the rows named in I27.

I29. Execution Map returns the source baseline's telemetry bytes for the same
database, caller, parameters, and frozen evaluation time, except for error text
that names the new command.

I30. Execution Map retains `edgeBasis = "concurrent_turn"`. It does not label a
concurrent-turn edge as intent or membership.

I31. Topline responses contain no Execution Map parent block, progress clock,
mind list, turn count, or completion estimate.

I32. The `toplines` and `topline` wire verbs use the human-intent contract in
this spec. The `execution-map` and `execution-map-select` wire verbs use the
telemetry contract.

I33. A gateway rejects a mismatched pre-1.0 CLI before it resolves a Topline ID,
Work Item ID, typed target, or verb handler.

I34. No compatibility alias maps an old telemetry verb or parameter shape to a
new handler.

I35. Placement detection uses row state at a named lifecycle event. It uses no
elapsed-time threshold to decide whether work needs placement.

I36. One placement episode schedules at most one prompt wake.

I37. Firing a placement prompt does not schedule another placement prompt.

I38. A pending placement obligation remains queryable after its prompt fires.

I39. A Topline link, explicit leave-unlinked decision, or terminal Work Item
disposition resolves the current placement episode.

I40. A subsequent qualifying lifecycle event can open a new placement episode.

I41. The `work_item.has_topline` fact is boolean for a visible, known,
call-scoped Work Item. It is nil when the call has no resolvable Work Item, the
Work Item is unknown, or the Work Item is invisible to the caller.

I42. The fact is true for one or more active memberships. It is false for zero
active memberships. Ended memberships and Concern tag associations do not
count.

I43. The new release installs no statute that reads `work_item.has_topline`.

I44. The candidate adds the complete Toplines tables, indexes, and local stamp.
It does not alter a Source-baseline table or weaken the product-wide
schema-stamp refusal. It refuses an Unregistered core schema instead of
inferring or rebuilding it.

I45. Rollback preserves Topline rows because the previous release ignores the
additive Toplines tables, local stamp, and supporting indexes.

I46. Each stored actor slot uses one discriminated kind/reference pair. Both
members are present or both members are null. A required actor slot has both
members present.

I47. Database `CHECK`, partial-unique-index, and composite-foreign-key
constraints reject the actor, lifecycle, owner, same-Topline, reason, and
timestamp contradictions enumerated in R1 through R6.

I48. Each Topline read and mutation has one canonical success shape. Each
Topline refusal has one canonical error shape. An idempotency row stores the
canonical success bytes returned by the first commit.

I49. Each response array has a specified deterministic order. A response that
contains no row for an optional singleton uses JSON `null`; it does not omit the
field.

I50. A target-line candidate cannot pass Lane 4 until the real packaged CLI,
Gateway wire, boot reconciliation, wake lane, and Gateway restart smoke in AC64
passes from a fresh Gateway process. Passing does not authorize deployment.

I51. The substrate stores each Topline title and Concern title as its Canonical
title. A valid Canonical title contains from 1 through 2,000 Unicode scalar
values.

I52. A Topline title-update request whose Canonical title equals the stored title
returns `no_change` for an open or closed Topline. A closed Topline returns
`topline_closed` when the Canonical titles differ.

I53. Each mutation operation has one closed Fingerprint JSON parameter shape.
An absent required parameter and an explicit JSON null are invalid messages; no
current mutation parameter is optional or nullable.

I54. Event `seq` is local to one Topline. Its first value is 1, and each later
committed event for that Topline increments it by exactly 1. Activity in another
Topline cannot change a returned sequence.

I55. Each event's non-null membership and Concern identifiers name parent rows
in the event's `toplineId`. A Concern tag event's membership and Concern name
parents in the same Topline.

I56. Each placement obligation stores a Placement causal watermark. Opening or
resolving that obligation and storing its new watermark are one transaction.

I57. A current-release Work Item disposition appends its
`disposition_transition` before the in-transaction placement seam observes or
resolves an obligation. A current-release reopen therefore records its exact
source causal-event sequence at episode opening and consumes that event in the
new watermark.

I58. Boot reconciliation opens one episode for the greatest Qualifying
rollback-era reopen. It opens none for an older reopen at or below the Work
Item's latest placement watermark.

I59. A boot-reconciled reopen records `process:tightbeam` as the actor that
recognized the durable event. It records the exact causal-event sequence as its
source. It does not fabricate a user or session actor that the baseline event
does not contain.

I60. One Work Item and one source causal-event sequence identify at most one
placement obligation. Gateway restart does not create another obligation or
wake for an event already bracketed by placement history.

I61. Re-upgrade terminal reconciliation resolves each pending placement
obligation whose Work Item has a Qualifying rollback-era terminal disposition.

I62. A re-upgrade terminal resolution records `process:tightbeam` and one closed
reason that names re-upgrade reconciliation plus the current terminal state. It
stores the exact terminal causal-event sequence. It does not synthesize a user
or session actor.

I63. Re-upgrade terminal reconciliation cancels a still-pending prompt wake in
the same transaction as obligation resolution. The obligation's
`promptWakeId`, process actor, resolution reason, and
`resolutionCausalEventSeq` are the linked cancellation provenance.

I64. Re-upgrade terminal reconciliation leaves a fired or already canceled wake
unchanged. A resolved terminal obligation schedules no replacement prompt.

I65. Boot runs terminal reconciliation before open-item reconciliation, wake
scheduler recovery, handler exposure, or a new placement prompt.

I66. A crash before a terminal-reconciliation commit leaves the obligation and
wake unchanged. A crash after commit is success; restart writes no second
resolution or wake mutation.

I67. The `0.1.9` and `0.2.0` candidates satisfy one semantic contract. A
Toplines or Execution Map success byte, stored-state transition, authorization
decision, privacy decision, replay result, restart result, or rollback result
cannot vary by Target line. Refusal bytes also match except that the existing
HTTP 426 `incompatible_cli` message names that Target line's required Candidate
version. Lane 4 evidence can differ only in that version literal and the
explicit source revision, digest, executable format, and line-plumbing fields
that its compatibility clause lists.

I68. Lane 1 starts only after the responsible product-line owner records the
Exact target revision, expected Candidate version, and the Previous-package
fixture. Each later lane also requires the accepted Exact candidate revision
from the immediately preceding lane. A missing or moving input blocks the lane.

I69. Each lane begins from a clean worktree at its Exact lane input revision and
a passing gate for that input. Lane 1 runs the target-line baseline gate. Each
later lane runs every committed predecessor-lane test suite in its input
ancestry before it changes a byte. A failing input is evidence of a blocked
lane. It is not permission to weaken a test or repair unrelated code.

I70. The status terms `complete` and `remaining` refer only to the status map in
this file. The Completed core is complete provenance. All four Implementation
lanes and the Final full-scope review remain incomplete until exact evidence
proves them.

I71. The delivery has exactly four Implementation lanes. A builder cannot add a
fifth catch-all lane, omit a lane, or move a requirement outside the four-lane
and final-review topology.

I72. Each product path has one owning lane during implementation. A lane can
consume another lane's public seam. It cannot mutate another lane's owned path
without a recorded owner handoff and an updated overlap ledger in both affected
Lane evidence bundles.

I73. The lane numbers define one strict completion order. Lane 1 completes
before Lane 2 starts. Lane 2 completes before Lane 3 starts. Lane 3 completes
before Lane 4 starts. Lane 4 completes before the Final full-scope review
starts.

I74. Each lane advances both Target lines from their separate Exact lane input
revisions. A clean cherry-pick is not compatibility proof. Each line runs its
own deterministic tests and produces its own Lane evidence bundle.

I75. A test named by a lane is a product deliverable. A prose claim, source
inspection, mock-only proof, historical test result, or test plan cannot replace
the committed deterministic test.

I76. The shared Toplines public-query and public-projection seams return the
canonical REST state and item projection required by `rest-state-api-v1.md`.
This work adds no REST route, REST cursor, REST pagination, or Firehose adapter.

I77. For the two Target lines, R8 and R9 supersede only the temporary sentence
in REST R6b that retained `toplines` and `topline` as Execution Map CLI names.
The final meanings are: `toplines` and `topline` expose durable intent;
`execution-map` and `execution-map-select` expose telemetry. Every other REST
requirement in the co-reviewed `rest-state-api-v1.md` remains authoritative.

I78. Each Lane evidence bundle binds all claims to full commit IDs and
SHA-256 values for external fixtures. A moving branch, uncommitted worktree,
abbreviated hash, or transcript summary cannot serve as candidate evidence.

I79. One independent session performs the Final full-scope review against both
target-line candidates. The reviewer authored none of the reviewed commits and
changes no reviewed candidate byte.

I80. The final reviewer returns either one reviewed-clean report for the full
dual-line scope or one blocking report that names every finding. A clean review
of one line, one lane, or one subset cannot complete the final gate.

I81. No lane, review, or work-item status authorizes release. Builders and the
reviewer do not merge a target branch, publish a package, deploy a service, run
a live migration, or mutate a live user database under this authority.

I82. The work-item implementation binding can name this specification only
after Independent specification review approves this exact file SHA-256. A
material spec change after binding requires amendment of the canonical file, a
new hash, and a new Independent specification review before implementation
resumes.

I83. A Lane 2, Lane 3, or Lane 4 candidate, or a Candidate package
whose gateway version, CLI version, product manifest version, or named Target
line disagree fails with the evidence classification
`target_version_mismatch`. Lane 1 does not own version declarations. No lane
adds a compatibility alias or infers which version was intended.

I84. A rollback proof uses one immutable Previous-package fixture from the same
Target line. If its gateway, CLI, version, source revision, or digest is absent
or mismatched, Lane 4 fails with `previous_fixture_unverified` before it starts
a process.

I85. The Completed core remains the sole implementation of its accepted
operations. A lane can extend or adapt its public seam. It cannot create a
second Toplines store, a second direct-membership truth, or a parallel Rules
fact.

I86. Every target-line test uses synthetic users, sessions, Work Items,
credentials, titles, reasons, and prompts. Evidence redacts bearer material and
contains no live prompt body, production database row, or unrelated user data.

I87. One exact repository commit resolves the two-file canonical set. The
standalone file is the canonical Toplines product specification. The paired
program-file deletion removes Toplines from every v0.2 program phase and
hierarchy. The two-file set, not either file alone, carries that
specification-only transition. The program file supplies no Toplines product
or release authority. The targetless commit that introduced this file also
performed that row deletion.

## Architecture

### Delivery status and scope boundary

| Surface | Status at specification handoff | Delivery owner |
| --- | --- | --- |
| V5 behavioral contract | Complete and reviewed-clean as exact artifact provenance | All lanes preserve it |
| Topline create, link, unlink, list, and get; Execution Map extraction; direct-membership fact | Completed core; each target line must re-prove presence | Lane 1 verifies and extends storage; Lane 2 verifies telemetry surface |
| Full schema, local schema stamp, structural rails, boot registration, canonical title functions, Concerns, history, idempotency, public REST seams | Remaining | Lane 1 |
| Final Gateway, router, compatibility, wire, CLI, and Execution Map command names | Remaining | Lane 2 |
| Lifecycle placement, wakes, causal watermarks, boot reconciliation, restart behavior | Remaining | Lane 3 |
| Exact target versions, candidate packages, previous-package fixtures, real-path restart and rollback smoke | Remaining | Lane 4 |
| Dual-line adversarial review | Remaining | Final full-scope reviewer |

The Completed core status does not allow a lane to skip target-line
verification. If an Exact target revision lacks an accepted core operation, the
lane records `completed_core_missing` and stops. The product-line owner must
either select a different Exact target revision or amend this specification
through review. The lane cannot silently reclassify the missing operation as
new scope.

The Completed core's `ensure_schema/1` was not registered in production boot.
Its partial tables therefore provide source-code provenance, not a production
migration stamp. Lane 1 performs the first production activation of the full
Toplines schema. It refuses any pre-existing unregistered partial table set and
preserves those bytes unchanged.

The four lanes own product mutations. The final review owns no product
mutation. The dependency order is:

```text
Lane 1 -> Lane 2 -> Lane 3 -> Lane 4 -> Final full-scope review
```

Each lane starts from the accepted commit produced by the immediately preceding
lane on that Target line. The strict chain preserves version declarations and
removes branch-composition ambiguity. A later lane cannot resolve a semantic
conflict by editing an earlier lane's owned path. The owning earlier lane
repairs that conflict and regenerates every downstream candidate and evidence
bundle.

The product owner opens an Independent specification review before any lane is
assigned or bound to this file. That review is separate from the Final
full-scope review after Lane 4.

The successor delivery gates do not form a fifth lane. Each lane performs its
own AC88 start check and produces its own AC99 evidence input. Lane 1 owns AC89
and AC90. Lane 2 owns AC91. Lane 3 owns AC92. Lane 4 owns AC93. The Final
full-scope reviewer owns the acceptance verdict for AC94 through AC100 across
the complete delivery; AC95's assignment-opening action remains with the
product owner, and AC100's targetless document change is an immutable review
input rather than a product mutation.

### Four implementation lanes

#### Lane 1 — schema and boot

**Owned seams.** Lane 1 owns the Toplines persistence module, Rules fact
extension, database schema and indexes, deterministic title scalar functions,
connection registration, the Toplines production schema stamp, the schema-first
boot entrypoint, the canonical
Toplines public query and projection functions, and focused schema, Toplines,
Rules, and boot tests. Expected product paths include
`lib/tightbeam/toplines.ex`, `lib/tightbeam/rules.ex`, the database/schema
module, the initial application boot adapter, and their focused tests. Lane 1
does not own Work Item lifecycle calls, wake scheduling, Gateway/router/CLI
dispatch, REST transport, package metadata, or the packaged smoke.

Lane 1 freezes one in-transaction placement API for Lane 3 and hands the
application boot adapter path to Lane 3 after its schema-first test passes. The
Lane 1 and Lane 3 evidence bundles record that path handoff. Lane 3 can order
reconciliation after schema creation, but it cannot change Lane 1 schema bytes,
title rules, query projection, or transaction semantics.

**Required behavior.** Lane 1 implements or verifies R1 through R7 and R11 at
the persistence seam. It preserves the Completed core. It adds the missing
Topline lifecycle, Work membership history, Concerns, Concern tag associations,
event sequence, idempotency, Placement obligation storage primitives,
Canonical title enforcement, structural database rails, deterministic reads,
the local schema activation and refusal rail, and public REST seams.
`query_public/2` and `public_item/1` return the canonical
state and projection assigned to them by `rest-state-api-v1.md`; they do not
parse a REST request or emit a Firehose notice.

Lane 1 owns V5 acceptance AC8 through AC29, AC43 through AC46, AC50 through
AC51, AC58 through AC61, AC65 through AC72, AC75, AC78 through AC83. Lane 3
later owns the lifecycle use of Placement rows. Lane 4 later proves these bytes
through real packages.

**Both-line compatibility.** The builder starts separate clean worktrees at the
owner-recorded `0.1.9` and `0.2.0` Exact target revisions. The builder records
the existing core API, product-wide schema stamp, and absence or presence of
Toplines-owned objects on each line before editing. The database constraint
outcomes, canonical JSON, query ordering, REST projection, Rules fact,
and success and refusal bytes match across lines. An internal module name or
boot hook can differ only when both Lane evidence bundles name the delta and
show the same observable result. A cherry-pick result alone does not pass.

**Deterministic tests and acceptance.** Committed tests create a fresh SQLite
database, freeze time, and cover every schema `CHECK`, partial unique index,
composite foreign key, canonical title boundary, event sequence, idempotency
fingerprint, race ordering, visibility class, empty-array order, null field,
Rules fact value, public query filter, public projection field, first schema
activation, exact stamped replay, unregistered-core refusal, unknown-stamp
refusal, each manifest object's missing or altered stamped shape, and crash on
each side of schema commit. The unregistered-core table runs once for every
manifest object that can exist without the stamp row. The tests
exercise direct SQL refusals as well as public functions. They compare exact
rows and exact JSON bytes. They run independently on both Target lines.
The test is part of the deliverable.

**Migration, replay, restart, and rollback.** Lane 1 proves additive creation
from an exact baseline database with no Toplines-owned object. The schema and
Toplines production stamp commit in one transaction. A crash before commit
leaves neither; a crash after commit leaves the complete stamped shape.
Repeated schema boot changes no row or stamp. A database with an Unregistered
core schema receives `unregistered_toplines_core_shape` before any DDL or row
write. An unknown Toplines stamp receives `unknown_toplines_schema_stamp` with
the same no-write result. Lane 1 also proves idempotent request replay before
and after a fresh process restart and preservation of stamped Topline rows when
the verified Previous-package fixture opens the database and ignores those
additive tables. Lane 1 exposes storage and transaction primitives for
reconciliation but does not implement reconciliation or schedule a wake.
Lane 3 proves lifecycle effects. Lane 4 repeats rollback with packages.

**Authorization and privacy.** Tests cover owner, same-owner session, admin,
foreign owner, unknown ID, and process principal. Foreign and unknown IDs
produce the same bytes. Public reads omit invisible rows and nested data.
Idempotency replay rechecks current authorization. Evidence uses synthetic
identities and redacts credentials.

**Refusals.** Lane 1 returns the R9 and R10 slugs at the persistence boundary
where applicable. It fails lane start with `exact_target_revision_missing`,
`baseline_not_green`, `completed_core_missing`, or
`previous_fixture_unverified` when the rollback fixture required by this lane
is absent or mismatched. It fails schema work with
`schema_shape_mismatch` if an existing stamped object differs. It does not
repair, drop, or rewrite that object automatically. It returns
`unregistered_toplines_core_shape` for any Toplines-owned object without the
local stamp and `unknown_toplines_schema_stamp` for any other local stamp.

**Evidence.** Each Target line produces a Lane 1 evidence bundle with the
baseline commit, candidate commit, full changed-path list, pre-edit schema
inventory and product-wide stamp, committed manifest, post-edit Toplines stamp
and schema dump hash, logical schema-and-row hashes for every no-write refusal
fixture, Previous-package source revision, Gateway SHA-256, and CLI SHA-256,
exact test commands, test counts,
exit status, public projection fixture hash, allowed cross-line delta ledger,
and a statement that no REST adapter, Work Item lifecycle, Gateway, CLI,
package, or live path changed.

#### Lane 2 — Gateway, router, and CLI

**Owned seams.** Lane 2 owns CLI wire dispatch in `lib/tightbeam/gateway.ex`,
verb classification in `lib/tightbeam/wire/router.ex`, pre-1.0 compatibility
ordering, `Tightbeam.ExecutionMap`, Rust CLI argument parsing and dispatch,
command help, exact CLI error rendering, the candidate version declarations in
Gateway, CLI, and product manifests, and their focused unit and integration
tests. Lane 2 does not own `Tightbeam.Toplines` persistence, Work Item
lifecycle, wakes, REST `/api/toplines` routes, Firehose notices, package
assembly, or `scripts/feature_smoke.exs`.

Lane 2 starts from the accepted Lane 1 candidate on the same Target line. It
preserves the Lane 1 commit and all Lane 1 evidence assumptions.

**Required behavior.** Lane 2 implements R8 through R10 at the public CLI wire
surface. It binds `toplines` and `topline` to human intent. It binds
`execution-map` and `execution-map-select` to unchanged telemetry. It exposes
every R9 Topline verb with its exact closed parameter shape. It rejects the
retired telemetry meanings and supplies no compatibility alias. It preserves
REST transport behavior and consumes Lane 1 public functions.

Lane 2 owns V5 acceptance AC1 through AC7, AC52 through AC53, AC73 through
AC74, and AC77. Lane 4 later executes the same command surface from packaged
artifacts.

**Both-line compatibility.** The same command names, help meanings, wire verbs,
HTTP status, canonical success JSON, refusal shape, validation order, and target
classification apply on `0.1.9` and `0.2.0`. Refusal bytes match except for the
required Candidate-version literal in the existing HTTP 426
`incompatible_cli` message. Line-specific Rust or Elixir plumbing can differ
only in the recorded delta ledger. Lane 2 sets all candidate version
declarations to the owner-recorded expected version for that Target line and
proves that Gateway, CLI, and product manifests agree. It does not publish a
package. Lane 4 verifies these frozen declarations during assembly and does not
change them.

**Deterministic tests and acceptance.** A table-driven committed suite invokes
the real CLI parser and real router for every declared read and mutation verb,
every required mutation key, every optional read flag, each mutual exclusion,
each unknown flag, each unknown alias, each retired telemetry form, each typed
target refusal, all 14 closed Topline-handler slugs, missing authentication,
process denial, foreign versus unknown IDs, and both sides of the exact
pre-1.0 version check. Success cases assert the complete request body and
response bytes. Refusal cases assert status and body bytes. The suite contains
no no-op parser case that omits dispatch assertion.
The test is part of the deliverable.

**Migration, replay, restart, and rollback.** Lane 2 proves matching-version
dispatch before and after a fresh Gateway restart, mutation replay through the
real router with the same key, `idempotency_conflict` for changed parameters,
and HTTP 426 before authentication or ID lookup for an old or future CLI.
Using the Previous-package fixture must expose the old telemetry names only
during the rollback fixture. Re-upgrade restores the new names without an alias
or data conversion. Lane 4 repeats this path with packaged binaries.

**Authorization and privacy.** Compatibility runs before authentication.
Authentication and principal-kind checks run before wire-shape record lookup.
Owner filtering makes foreign and unknown IDs byte-identical. Help, error text,
and logs expose no credential, hidden ID, idempotency fingerprint input, or
foreign title.

**Refusals.** Lane 2 preserves HTTP 426 `incompatible_cli` bytes. It uses the
closed R9 refusal mapping after compatibility and authentication. Unknown
aliases and legacy parameter shapes return `invalid_message`; they never fall
through to Execution Map. It fails lane start with
`exact_target_revision_missing`, `baseline_not_green`,
`lane_1_contract_missing`, or `previous_fixture_unverified`. A completed Lane 2
candidate whose declarations disagree fails with `target_version_mismatch`.

**Evidence.** Each Target line produces a Lane 2 evidence bundle with exact
commits, changed paths, generated CLI help, a closed verb/parameter/status/body
matrix, exact Rust and Elixir commands and counts, router coverage, baseline
Execution Map parity results, compatibility ordering proof, cross-line delta
ledger, Previous-package source revision, Gateway SHA-256, and CLI SHA-256, and
a statement that no Toplines schema, lifecycle, REST route, Firehose, package,
or live path changed.

#### Lane 3 — placement and wakes

**Owned seams.** Lane 3 owns the Work Item lifecycle calls into the frozen
Lane 1 transaction API, Placement episode transitions, causal watermark
capture, wake creation and pending-only cancellation, responsible-Main
addressing, terminal-first boot-reconciliation orchestration, open-item
reconciliation orchestration, and their deterministic lifecycle, wake, crash,
and restart tests. Expected paths include `lib/tightbeam/work_items.ex`,
`lib/tightbeam/wakes.ex`, `lib/tightbeam/causal_events.ex`, a reconciliation
orchestrator, the session wake lane, and the boot adapter handed off by Lane 1.
Lane 3 issues no direct DML against a Toplines-owned table; it calls Lane 1's
frozen `*_in_txn` API. It does not change schema definitions, CLI verbs, REST
transport, package metadata, or the packaged smoke.

Lane 3 starts from the accepted Lane 2 candidate on the same Target line. It
therefore carries the accepted Lane 1 persistence contract and the frozen Lane
2 version and command declarations without changing either owned seam.

**Required behavior.** Lane 3 implements R6 and R12 lifecycle integration. A
qualifying create or reopen opens at most one Placement episode and schedules
one prompt to the responsible user's Main. Link, explicit leave-unlinked, and a
terminal disposition resolve it. Boot orders schema creation, terminal
reconciliation, open-item reconciliation, wake recovery, then handler
exposure. It records process attribution only for boot reconciliation. It uses
causal sequence, not wall time, to order rollback-era events.

Lane 3 owns V5 acceptance AC30 through AC42, AC54 through AC57, AC62 through
AC63, AC76, and AC84 through AC87. Lane 4 later exercises these outcomes through
real packages and a real wake lane.

**Both-line compatibility.** Both Target lines call the same frozen Lane 1
transaction contract and produce the same Placement rows, wake rows, prompt
bytes, causal watermarks, actor pairs, resolution reasons, cancellation
outcomes, and boot order. A line-specific Work Item or session-lane hook can
differ only when the delta ledger identifies it and deterministic tests prove
the same committed transaction boundary.

**Deterministic tests and acceptance.** Committed tests freeze time and causal
sequence, use a disposable Main, and cover create, reopen, multiple membership,
final unlink with no prompt, link, explicit leave-unlinked, close, fail, icebox, prompt fire,
pending cancel, fired preservation, already-canceled preservation, rollback-era
reopen, rollback-era terminal disposition, transaction race order, crash before
commit, crash after commit, repeated restart, and turn-boundary delivery. Each
case asserts exact row counts, actors, reasons, wake state, prompt body, and the
absence of a duplicate prompt.
The test is part of the deliverable.

**Migration, replay, restart, and rollback.** Lane 3 proves schema-first boot,
terminal reconciliation before open-item reconciliation, replay by causal
watermark, restart idempotency, a rollback-era open item with no history, a
rollback-era reopen after history, and a rollback-era terminal disposition for
pending, fired, and canceled wakes. A crash before commit leaves all rows
unchanged. A crash after commit writes no duplicate on restart. Lane 4 repeats
the combined path with packaged processes.

**Authorization and privacy.** The lifecycle seam accepts only the actor already
authorized by the Work Item transaction. It cannot accept a caller-supplied
owner override. A prompt names only its synthetic Work Item, obligation,
reason, and three decisions. It includes no foreign Topline, hidden membership,
credential, unrelated assignment, or Execution Map ancestry. Admin mutation
preserves the Work Item owner's responsible Main.

**Refusals.** A non-qualifying event writes no Placement or wake row. Duplicate
source events no-op by the structural uniqueness rail. A stale decision returns
`placement_not_pending`. A cross-owner link returns `owner_mismatch`. A boot
candidate with missing or contradictory causal evidence commits no product row,
blocks handler exposure, and makes the Lane evidence bundle record
`reconciliation_evidence_invalid`; it does not guess an actor, event, or state.
Lane start also refuses
`exact_target_revision_missing`, `baseline_not_green`,
`lane_1_contract_missing`, `lane_2_contract_missing`, or
`target_version_mismatch`.

**Evidence.** Each Target line produces a Lane 3 evidence bundle with exact
commits, changed paths, the Lane 1 API hash, transaction diagrams derived from
tests, exact commands and counts, frozen-clock and causal-sequence fixtures,
prompt fixture hash, crash-point results, restart row-count snapshots, rollback
reconciliation snapshots, cross-line delta ledger, and a statement that no
schema, CLI, REST, package, or live path changed outside the recorded boot-path
handoff.

#### Lane 4 — packaging and rollback proof

**Owned seams.** Lane 4 owns package assembly inputs, package-only support
files, `scripts/feature_smoke.exs`, and immutable evidence for the real packaged
path. It starts from the accepted Lane 3 candidate, whose ancestry contains the
accepted Lane 1 and Lane 2 commits. It changes no Toplines state machine,
schema, Gateway handler semantics, router semantics, CLI command semantics,
Work Item lifecycle, wake semantics, REST route, or Firehose code. If a package
test exposes a product defect, the owning earlier lane repairs that defect and
regenerates every affected downstream candidate and evidence bundle before
Lane 4 restarts.

**Required behavior.** Lane 4 verifies that each Exact lane input revision has
the accepted Lane 1, Lane 2, and Lane 3 commits in order and that Lane 2 bound
the respective candidate to version `0.1.9` or `0.2.0`. It changes no version
declaration or earlier-lane semantic byte. For each line, it commits only its
owned package or smoke paths, then builds a fresh Gateway and exact matching CLI,
verifies their embedded version and source revision,
executes AC64 through the real HTTP/wire router and normal boot and wake paths,
restarts on the same database, rolls back to the owner-named
Previous-package fixture, mutates through that fixture's real public path, and
re-upgrades the same database. It performs no publish, install into a live
prefix, deployment, or live migration.

Lane 4 owns V5 acceptance AC47 through AC49 and AC64. Its packaged smoke also
samples the Lane 1, Lane 2, and Lane 3 public path named by AC64. Focused lane
tests remain authoritative for cases that AC64 does not sample.

**Both-line compatibility.** The `0.1.9` smoke uses only a `0.1.9` candidate and
its owner-verified previous fixture. The `0.2.0` smoke uses only a `0.2.0`
candidate and its separately owner-verified previous fixture. The two smokes
run the same scenario and compare the same canonical outputs. Allowed
differences are candidate version, source revision, package digest, executable
format, and explicitly recorded line plumbing. Toplines state and public bytes
cannot differ except for the required Candidate-version literal in the
existing HTTP 426 `incompatible_cli` message.

**Deterministic tests and acceptance.** The committed smoke assembles the real
packages in a disposable directory, chooses isolated ports, freezes supported
test clocks, starts a fresh Gateway process, waits at most 10 seconds at each
named delivery observation, uses the exact packaged CLI for all public calls,
captures process exit and logs, and always checks that processes and ports are
gone. It rejects a direct handler, handwritten response fixture, alternate
runner, unbuilt CLI, reused Gateway process, or pre-populated success response.
It also proves Previous-package telemetry access, retained Topline rows, one
rollback-created Work Item's re-upgrade placement, and a source guard with no
hard-delete surface. It runs independently for both Target lines.
The test is part of the deliverable.

**Migration, replay, restart, and rollback.** The packaged scenario starts from
the exact baseline schema, creates and mutates Toplines, replays a committed
key, restarts the candidate on the same database, proves no duplicate
obligation or prompt, boots the Previous-package fixture, records a rollback
interval Work Item creation and terminal disposition through real public verbs,
then re-upgrades. It proves retained rows, process-attributed reconciliation,
pending-only wake cancellation, fired wake and delivered-turn preservation,
causal watermark advancement, no duplicate prompt, and byte-identical reads.

**Authorization and privacy.** The smoke creates only synthetic users and one
disposable personal Main inside its isolated database. It uses ephemeral test
credentials, redacts tokens from logs, verifies owner, admin, foreign, unknown,
and process cases through packaged calls, and destroys no user-owned path. It
does not read a configured live database or contact a deployed Gateway.

**Refusals.** Lane 4 fails before process start with
`exact_target_revision_missing`, `target_version_mismatch`,
`lane_3_contract_missing`, `candidate_package_unverified`, or
`previous_fixture_unverified`. During the smoke it asserts HTTP 426 for a
mismatched CLI, `invalid_message` for retired or unknown aliases, the R9
canonical refusal bytes for denied mutations, and a non-zero test result for
any timeout, leaked process, leaked port, digest change, row loss, duplicate
row, changed prompt, or unrecorded cross-line delta.

**Evidence.** Each Target line produces a Lane 4 evidence bundle with the exact
Lane 1, Lane 2, and Lane 3 ancestor commits, Lane 4 input and candidate commits,
parentage and Lane 4-owned diff, package version output, Gateway and CLI
SHA-256 values, Previous-package source revision and SHA-256 values, assembly
commands, smoke command and exit status, ordered process log, redacted request
and response transcript, before/after database snapshot hashes, causal-event
sequence, wake and delivered-turn hashes, cleanup proof, changed-path list, and
cross-line delta ledger. The bundle states that no package was published and no
live service or database was touched.

### Final full-scope review

The product owner opens one review assignment only after Lane 4 has recorded
both exact Lane 4 candidate commits and all eight Lane evidence bundles.
The assignment names this specification's reviewed SHA-256, both candidate
commits, both candidate package hashes, all four lane commits per line, and all
evidence artifact IDs.

The reviewer first derives an independent model from Goal, Non-Goals, Terms,
Assumptions, and Invariants. The reviewer then reads the complete Architecture,
all AC1 through AC100, both target-line diffs, every Lane evidence bundle, and
the current program document. The reviewer re-runs every committed lane test
suite and both packaged smokes from clean worktrees. The reviewer verifies that
the Toplines and Execution Map public semantic diff between the lines is empty
after excluding only the explicit package-version and source-revision evidence
surfaces and the required Candidate-version literal in the existing HTTP 426
`incompatible_cli` message.

The report maps every acceptance case to exact source and committed test
evidence. It verifies four-lane ownership, handoffs, changed-path completeness,
REST boundary preservation, removal from the v0.2 program, privacy, exact
refusals, restart and rollback behavior, package cleanup, and the No-release
gate. A finding blocks the whole dual-line review until the owning lane repairs
it and all downstream evidence is regenerated.

The reviewer writes no candidate byte and performs no merge, release,
deployment, deployed-service restart, or live mutation. The local disposable
process starts and restarts required by the committed tests are test execution,
not service mutation. `reviewed-clean` marks the dual-line candidates
full-scope-reviewed for a separate owner decision. It does not authorize
product integration or release.

### Pattern names

**Direct Intent Membership** applies to Topline-to-Work membership. It does not
apply to Execution Map ancestry, assignment resolution, or Concern tags.
Canonical example: Work Item `wi_a` has active memberships `tlm_1` in `tl_alpha`
and `tlm_2` in `tl_beta`.

**Placement Episode** applies when a named lifecycle event leaves an open Work
Item with no active membership and no unresolved placement obligation. It does
not apply on a timer. Canonical example: creating `wi_a` opens `tlp_1` and arms
one wake to its owner's Main.

**Rollback Reopen Reconciliation** applies only during release boot to a Work
Item with prior placement history and a later durable reopen that the previous
gateway could not send through the Topline seam. It does not infer membership,
replay an older reopen, or scan periodically. Canonical example: `wi_a` has a
resolved `left_unlinked` episode at watermark 40, the previous gateway records
its `iceboxed -> open` transition at causal sequence 43, and re-upgrade opens
one `reopened` episode sourced by sequence 43.

**Rollback Terminal Reconciliation** applies only during release boot to a
pending Placement episode whose Work Item became terminal through the previous
gateway. It resolves the existing episode; it does not delete the episode,
reopen the Work Item, or create a replacement prompt. Canonical example:
`tlp_a` is pending at watermark 40, the previous gateway closes `wi_a` at causal
sequence 43, and re-upgrade resolves `tlp_a` as `work_terminal` under
`process:tightbeam` before wake recovery.

**Execution Map Compatibility Rename** applies to the existing four telemetry
views. It does not permit a change to their data, filters, ordering,
authorization, or read-only behavior.

### Mutation seam

`Tightbeam.Toplines` is the sole runtime DML seam for Topline,
membership, Concern, Concern-tag, Topline-event, Topline-idempotency, and
placement-obligation rows. Work Item transactions call its public
`*_in_txn` placement functions. The Lane 3 boot reconciler orchestrates those
same public transaction functions and does not write a Toplines-owned table
directly. Rules and Execution Map read these rows but do not mutate them.

Each actor slot in these tables uses two columns named `<stem>ActorKind` and
`<stem>ActorRef`. A present pair serializes as
`{"kind":"<kind>","ref":"<ref>"}`. A nullable pair serializes as JSON `null`
when both columns are null. DDL `CHECK` constraints enforce pair completeness,
the closed kind set for that slot, and a non-blank reference. Topline mutation
actors accept `user|session`. Placement opening accepts `user|session`, plus
`process` with reference `tightbeam` only for a `migration` cause or a
boot-reconciled `reopened` cause. No table adds `...ByUser` and `...BySession`
alternatives. Placement resolution accepts `user|session`, plus
`process:tightbeam` only for Re-upgrade terminal reconciliation.

Wire responses use canonical JSON: object keys sort by UTF-8 byte order, arrays
use the order specified below, integers use base 10, and serialization contains
no insignificant whitespace. Expanded examples in this document show the same
objects with whitespace only for readability.

### R1. Topline state

The implementation shall add a `toplines` table with these logical fields:

| Field | Contract |
| --- | --- |
| `id` | Primary key with `tl_` prefix. |
| `ownerUserId` | Existing user ID. Immutable. |
| `title` | Canonical title containing 1 through 2,000 Unicode scalar values. |
| `state` | `open` or `closed`. |
| `createdActorKind`, `createdActorRef` | Required `user|session` actor pair. |
| `createdAt` | Mutation time. |
| `updatedAt` | Mutation time of the last successful mutation. |
| `closedAt` | Null while open. Set by close. Cleared by reopen. |

`topline-create` creates an open Topline for the caller's user. It accepts no
owner target. `topline-update` changes the title and requires a reason.
`topline-close` and `topline-reopen` require a reason. Closing a Topline does not
inspect Work Item states. Repeating the same state transition with a new key
returns `invalid_transition`.

Each reason in R1 is a Mutation reason. Create and update transform the supplied
title to its Canonical title before storage or comparison. `topline-update`
returns `no_change` when that Canonical title equals the stored title. This
equality check runs after authorization and idempotency handling but before the
closed-state check. It therefore returns `no_change` for an equal title on an
open or closed Topline. It writes no event, idempotency row, or `updatedAt`
change.

`updatedAt` changes on a committed title, state, Work membership, Concern
definition, or explicit Concern tag mutation for that Topline. A closed Topline
accepts `topline-reopen`, `topline-unlink-work`, and
`topline-concern-unlink-work`. It rejects a different Canonical title, new
Concerns, new Work memberships, and new Concern tag associations with
`topline_closed`.

Each SQLite connection that can read or write these tables shall register
deterministic scalar functions `tightbeam_canonical_title(text)` and
`tightbeam_unicode_scalar_length(text)`. The first returns the Canonical title or
SQL null for a non-text value or invalid UTF-8. The second returns the Unicode
scalar-value count or SQL null for a non-text value or invalid UTF-8. Schema
creation shall fail before exposing the mutation seam when either function is
absent.

The `toplines` table DDL shall enforce: `state IN ('open','closed')`;
`typeof(title) = 'text'`; `tightbeam_canonical_title(title) IS NOT NULL`;
`title = tightbeam_canonical_title(title)`;
`tightbeam_unicode_scalar_length(title) BETWEEN 1 AND 2000`; a complete
`user|session` creation actor; integer `createdAt` and `updatedAt` with
`updatedAt >= createdAt`; and exactly one lifecycle tuple, either
`state = 'open' AND closedAt IS NULL` or `state = 'closed' AND closedAt IS an
integer AND closedAt >= createdAt`.

### R2. Work membership state

The implementation shall add a `topline_work_memberships` table with these
logical fields:

| Field | Contract |
| --- | --- |
| `id` | Primary key with `tlm_` prefix. |
| `toplineId` | Existing Topline ID. |
| `workItemId` | Existing Work Item ID. |
| `ownerUserId` | Owner shared by the Topline and Work Item. |
| `linkReason` | Trimmed length from 1 through 4,000 Unicode characters. |
| `linkedActorKind`, `linkedActorRef` | Required `user|session` actor pair. |
| `linkedAt` | Mutation time. |
| `unlinkReason` | Null while active; otherwise 1 through 4,000 characters. |
| `unlinkedActorKind`, `unlinkedActorRef` | Both null while active; required `user|session` pair after unlink. |
| `unlinkedAt` | Null while active; mutation time after unlink. |

A partial unique index shall cover `(toplineId, workItemId)` where
`unlinkedAt IS NULL`.

The membership DDL shall enforce a complete `user|session` link actor, trimmed
link-reason length from 1 through 4,000, integer `linkedAt`, and exactly one
unlink tuple: either `unlinkedAt`, `unlinkReason`, `unlinkedActorKind`, and
`unlinkedActorRef` are all null; or the time and reason are non-null, the reason
has trimmed length from 1 through 4,000, the actor is a complete
`user|session` pair, and `unlinkedAt` is an integer not less than `linkedAt`.
The release shall add unique
indexes on `(id, ownerUserId)` for `toplines` and `work_items`. Composite
foreign keys from `(toplineId, ownerUserId)` and `(workItemId, ownerUserId)`
make a cross-owner membership unrepresentable. The write seam still returns
`owner_mismatch` before an insert reaches that rail.

`topline-link-work` accepts `toplineId`, `workItemId`, `reason`, and
`idempotencyKey`. The handler shall resolve authorization and owner equality,
re-read the Topline and Work Item inside the write transaction, require an open
Topline, and insert one membership episode.

The Work Item state does not restrict an explicit link. An authorized actor can
group open, iceboxed, closed, or failed Work Items.

`topline-unlink-work` accepts `membershipId`, `reason`, and `idempotencyKey`.
The membership ID, rather than a `(toplineId, workItemId)` pair, makes a stale
unlink unable to end a later relink.

Each reason in R2 is a Mutation reason.

If a concurrent transaction already created an active pair under a different
key, the losing link returns `membership_exists` with no mutation. If a
concurrent transaction already ended the named membership, the losing unlink
returns `membership_ended` with no mutation.

### R3. Concern tags

The implementation shall add a `topline_concerns` table with these logical
fields:

| Field | Contract |
| --- | --- |
| `id` | Primary key with `tlc_` prefix. |
| `toplineId` | Existing Topline ID. |
| `title` | Canonical title containing 1 through 2,000 Unicode scalar values. |
| `createdActorKind`, `createdActorRef` | Required `user|session` actor pair. |
| `createdAt`, `updatedAt` | Integer Mutation times. |

Concern create and update transform the supplied title to its Canonical title
before storage or comparison. Concern create sets creation and update time to
one Mutation time. A Concern has no state, resolution fields, resolve verb,
reopen verb, or resolution history. The Concern DDL shall enforce
`typeof(title) = 'text'`, `tightbeam_canonical_title(title) IS NOT NULL`,
`title = tightbeam_canonical_title(title)`, `tightbeam_unicode_scalar_length(title)
BETWEEN 1 AND 2000`, a complete creation actor, integer `createdAt` and
`updatedAt`, and `updatedAt >= createdAt`.

The implementation shall add a `topline_concern_tags` table with `toplineId`,
`concernId`, `membershipId`, `tagReason`, `taggedActorKind`, `taggedActorRef`,
and `taggedAt`. Its primary key is `(concernId, membershipId)`. It stores only
current tag associations. It has no association ID, untag fields, lifecycle
state, or ended episode history. The DDL shall enforce a complete
`user|session` tag actor, tag-reason bounds, and integer `taggedAt`. Unique
indexes on
`(id, toplineId)` for Concerns and memberships support composite foreign keys
from `(concernId, toplineId)` and `(membershipId, toplineId)`. The association
therefore cannot name parents from different Toplines. The mutation seam also
requires the membership to be active.

The wire and CLI verbs are:

- `topline-concern-create <toplineId> --title <text> --key <key>`
- `topline-concern-update <concernId> --title <text> --reason <text> --key <key>`
- `topline-concern-link-work <concernId> <membershipId> --reason <text> --key <key>`
- `topline-concern-unlink-work <concernId> <membershipId> --reason <text> --key <key>`

The link-work verb applies the Concern as a tag. The unlink-work verb removes
that tag. They are the tag and untag operations; their `link-work` and
`unlink-work` spellings are retained only for wire and CLI compatibility. The
link handler shall require the Concern and active Work membership
to name the same Topline. Ending a Work membership shall delete all of its
Concern tag associations in the same transaction. That automatic cleanup
appends no derived Concern event and creates no Placement obligation or prompt.

Concern create, update, and link-work require an open Topline. Concern
unlink-work can run while its Topline is open or closed.

Each reason in R3 is a Mutation reason. A Concern update whose Canonical title
equals its stored title returns `no_change`. The Topline must be open before
this equality check runs. A second tag association for the same Concern and
membership returns `concern_tag_exists`. Removing an absent association returns
`concern_tag_absent`. These refusals write no row.

### R4. Event history

The implementation shall add an append-only `topline_events` table with an
integer `seq` local to `toplineId`, event kind, optional membership ID,
optional Concern ID, `actorKind`, `actorRef`, reason, integer `eventAt` equal to
Mutation time, and canonical JSON detail.

The event DDL shall enforce the closed event-kind set below, a complete
`user|session` actor pair, `typeof(seq) = 'integer' AND seq >= 1`, an integer
event time, and the required identifier combination for its kind. Its primary
key is `(toplineId, seq)`, and `toplineId` references `toplines(id)`. It shall
reject an event that supplies a membership or Concern ID for a kind whose
identifier tuple does not permit that ID. `detail` shall parse as a
JSON object with exactly the keys and value types listed below. The mutation
seam supplies its canonical bytes.

The membership table shall have a unique index on `(id, toplineId)`. The Concern
table shall have a unique index on `(id, toplineId)`. Each non-null event parent
is guarded by these composite foreign keys:

- `(membershipId, toplineId)` references the membership index;
- `(concernId, toplineId)` references the Concern index.

SQLite foreign-key enforcement remains enabled on each connection before
schema or mutation work.

`topline_created`, `topline_renamed`, `topline_closed`, and `topline_reopened`
require both optional IDs to be null. A `work_*` kind requires only
`membershipId`. A non-tag `concern_*` kind requires only `concernId`. A
`concern_work_*` kind requires `membershipId` and `concernId`. The two
`*_created` kinds require a null reason; each
other kind requires a Mutation reason.

The closed event-kind set is:

`topline_created`, `topline_renamed`, `topline_closed`, `topline_reopened`,
`work_linked`, `work_unlinked`, `concern_created`, `concern_renamed`,
`concern_work_tagged`, and `concern_work_untagged`.

Each event detail has this closed shape:

| Event | Required detail |
| --- | --- |
| `topline_created` | string `title` |
| `topline_renamed` | string `fromTitle`, string `toTitle` |
| `topline_closed`, `topline_reopened` | string `fromState`, string `toState` |
| `work_linked` | string `workItemId`, string `linkReason` |
| `work_unlinked` | string `workItemId`, string `unlinkReason` |
| `concern_created` | string `title` |
| `concern_renamed` | string `fromTitle`, string `toTitle` |
| `concern_work_tagged` | string `membershipId`, string `tagReason` |
| `concern_work_untagged` | string `membershipId`, string `untagReason` |

The event rows and current-state rows shall commit in the same transaction. For
the first event in one mutation, the mutation seam computes
`COALESCE(MAX(seq), 0) + 1` over that Topline inside the write transaction. Each
additional event in that transaction uses the preceding assigned value plus 1.
Competing writes serialize. An aborted transaction consumes no sequence value.
A transaction that writes multiple events assigns consecutive values in the
semantic order specified here. No global event sequence is stored or returned.
`topline <toplineId> --history` returns authorized events in `seq ASC` order. A
normal `topline <toplineId>` omits history. No additional singular-read spelling
ships.

When one Work unlink deletes multiple Concern tag associations, the transaction
appends only its `work_unlinked` event. The committed state contains no tag
association for the ended membership.

### R5. Idempotency

The implementation shall add a `topline_idempotency` table keyed by
`(callerUserId, operation, idempotencyKey)`. The row stores the request
fingerprint in `requestFingerprint` and the exact canonical JSON
success-response bytes from R9 in `canonicalResponse`. Error responses are not
stored.

Each fingerprint input has exactly this envelope before serialization:

```json
{"operation":"<wire-verb>","parameters":{<closed-parameter-shape>}}
```

The closed parameter shapes are:

| Operation | `parameters` keys |
| --- | --- |
| `topline-create` | `title` |
| `topline-update` | `reason`, `title`, `toplineId` |
| `topline-close`, `topline-reopen` | `reason`, `toplineId` |
| `topline-link-work` | `reason`, `toplineId`, `workItemId` |
| `topline-unlink-work` | `membershipId`, `reason` |
| `topline-concern-create` | `title`, `toplineId` |
| `topline-concern-update` | `concernId`, `reason`, `title` |
| `topline-concern-link-work` | `concernId`, `membershipId`, `reason` |
| `topline-concern-unlink-work` | `concernId`, `membershipId`, `reason` |
| `topline-work-leave-unlinked` | `reason`, `workItemId` |

Each listed value is a JSON string. A title value is its Canonical title. Each
other value is the validated wire value. Fingerprint JSON then NFC-normalizes
each string as its term specifies. Thus NFC-equivalent reason or identifier
spellings have the same fingerprint even though the first successful request
stores a Mutation reason verbatim. Every listed key is required. An omitted key,
an extra key, or explicit JSON null returns `invalid_message` before the
fingerprint exists. No mutation in this specification has an absent/null
equivalence rule because none has an optional or nullable semantic parameter.
The idempotency key is required by the wire but is not a member of `parameters`.

Each mutation shall compute the Fingerprint JSON and its hash after wire
validation and before the write. It shall check the idempotency row inside the
same transaction as
the mutation. A matching replay returns the stored response. A key collision
with a different fingerprint returns `idempotency_conflict`.

The handler shall authenticate the current principal and authorize each named
record before it reads an idempotency response. A caller who lost authorization
receives the current authorization refusal instead of a stored response.

After authorization, the handler checks idempotency before it validates mutable
state. A matching replay therefore returns its stored response after a later
close, unlink, rename, or tag removal. A request under a different key validates
the current state.

The CLI requires `--key` on each Topline mutation. The wire requires
`idempotencyKey`. Read operations accept no idempotency key.

### R6. Placement obligations

The implementation shall add a `topline_placement_obligations` table with these
logical fields:

| Field | Contract |
| --- | --- |
| `id` | Primary key with `tlp_` prefix. |
| `workItemId` | Existing Work Item ID. |
| `ownerUserId` | Work Item owner and responsible user. |
| `cause` | `created`, `reopened`, or `migration`. |
| `causeRef` | Work Item ID or migration release ID. |
| `sourceCausalEventSeq` | Exact positive `causal_events.seq` for `reopened`; null for every other cause. |
| `resolutionCausalEventSeq` | Exact positive terminal `causal_events.seq` for a process-attributed re-upgrade terminal resolution; null for every `user|session` resolution. |
| `historyCausalSeq` | Required non-negative Placement causal watermark. |
| `openedActorKind`, `openedActorRef` | Required opening actor; `user|session` for create or current-release reopen; `process` and `tightbeam` for migration or a boot-reconciled reopen. |
| `state` | `pending`, `linked`, `left_unlinked`, or `work_terminal`. |
| `openedAt` | Mutation time. |
| `dueAt` | Equal to `openedAt`. |
| `promptWakeId` | The one wake for this episode. |
| `resolutionActorKind`, `resolutionActorRef` | Null while pending; required `user|session` pair after caller or current-release disposition resolution, or `process:tightbeam` for re-upgrade terminal reconciliation. |
| `resolutionReason` | Null while pending; Mutation reason or one closed terminal-resolution cause after resolution. |
| `resolvedAt` | Null while pending; Mutation time after resolution. |

A partial unique index shall permit at most one pending placement obligation per
Work Item. A second partial unique index on
`(workItemId, sourceCausalEventSeq)` where `sourceCausalEventSeq IS NOT NULL`
shall permit at most one placement obligation for one Work Item reopen event.
Another partial unique index on `(workItemId, resolutionCausalEventSeq)` where
`resolutionCausalEventSeq IS NOT NULL` shall permit at most one placement
resolution for one Work Item terminal event.
The release shall add a unique `(seq, jobRef)` index to `causal_events`; the
placement table shall use it as the parent key for composite foreign keys from
`(sourceCausalEventSeq, workItemId)` and
`(resolutionCausalEventSeq, workItemId)`.

The placement DDL shall enforce the closed `cause` and `state` sets, a non-blank
`causeRef`, integer `historyCausalSeq >= 0`, integer `openedAt` and `dueAt` with
`dueAt = openedAt`, and a non-blank `promptWakeId`. `sourceCausalEventSeq` is a
positive integer exactly when `cause = 'reopened'`; every other cause requires
it to be null. `resolutionCausalEventSeq` is a positive integer exactly for the
`process:tightbeam` re-upgrade terminal-reconciliation tuple; each
`user|session` resolution requires it to be null. A composite foreign key from
`(workItemId, ownerUserId)` to `work_items` preserves the responsible owner, and
`promptWakeId` references the existing wake row. A `migration` row requires
`openedActorKind = 'process'` and `openedActorRef = 'tightbeam'`. A `reopened`
row accepts either a complete `user|session` opening actor or exactly
`process:tightbeam`. A `created` row requires a complete `user|session` opening
actor. A pending row requires
`resolutionActorKind`, `resolutionActorRef`, `resolutionReason`, `resolvedAt`,
and `resolutionCausalEventSeq` to be null. A non-pending row requires a complete
resolution actor, a non-blank resolution reason, and integer
`resolvedAt >= openedAt`; its `resolutionCausalEventSeq` follows the
user/session-versus-process rule above.
State `linked` stores the link reason under its `user|session` actor. State
`left_unlinked` stores the submitted reason under its `user|session` actor.
State `work_terminal` accepts exactly one of these tuples:

- a `user|session` actor plus `work_item_closed`, `work_item_failed`, or
  `work_item_iceboxed`; or
- `process:tightbeam` plus `reupgrade_terminal_reconciliation_closed`,
  `reupgrade_terminal_reconciliation_failed`, or
  `reupgrade_terminal_reconciliation_iceboxed`.

The DDL rejects a process resolution actor or re-upgrade reconciliation reason
in another state or combination.
For cause `created|reopened`, `causeRef` equals `workItemId`. For cause
`migration`, `causeRef` is the
non-blank release identifier supplied by the boot reconciler. The DDL enforces
the equality check.

The source composite causal-event foreign key proves that a reopened
obligation's source sequence belongs to the same Work Item. Before insert, the
mutation seam shall also prove that the source row has kind
`disposition_transition` and the exact `workItemId`,
`fromState = "iceboxed"`, and `toState = "open"` JSON field values. Before a
process-attributed re-upgrade terminal resolution, the mutation seam shall
prove that the resolution event belongs to the same Work Item, has kind
`disposition_transition`, and has exact `workItemId` and `toState` JSON values
that match the stored terminal resolution reason. `historyCausalSeq` is a
high-water observation and therefore has no foreign key: zero is valid when the
causal-event table is empty.

The Work Item mutation and placement recognition shall be one transaction at
these edges:

1. `work-item-create` opens an episode after it inserts an open unlinked Work
   Item.
2. `work-item-reopen` changes the state, appends and obtains the exact
   `disposition_transition` sequence, then opens an episode when the reopened
   Work Item has no active membership. The episode stores that sequence in
   `sourceCausalEventSeq`.

`topline-unlink-work` never opens a Placement episode. It creates no Placement
prompt or wake, even when it ends the Work Item's final active membership.

A Work Item close, fail, or icebox shall append its disposition event before it
resolves a pending placement obligation in the same transaction. At every
placement-obligation insert or resolution, the placement seam sets
`historyCausalSeq` to `COALESCE(MAX(causal_events.seq), 0)` after any causal
event from that transaction has been appended.

Opening an episode shall schedule one immediate prompt wake to
`Org.personal_session_key(ownerUserId)` in that same transaction. The prompt
origin is `process:tightbeam`. The prompt shall name the obligation ID, the Work
Item, and these three choices: link it to an existing Topline, create and link a
Topline, or record that it remains unlinked. The prompt shall not suggest a
placement.

The wake uses the existing session lane. If the target Main has a running turn,
the lane starts the placement turn only after the running turn reaches its
observable end. No time threshold substitutes for that turn boundary.

`topline-work-leave-unlinked <workItemId> --reason <text> --key <key>` resolves
the pending episode as `left_unlinked` and cancels its pending wake. A successful
`topline-link-work` resolves the pending episode as `linked` and cancels its
pending wake. A Work Item close, fail, or icebox resolves the pending episode as
`work_terminal` and cancels its pending wake. If the wake already fired, each
resolution updates the obligation without trying to retract the delivered turn.
Calling leave-unlinked without a pending obligation returns
`placement_not_pending` and writes nothing.

The leave-unlinked reason is a Mutation reason. A link resolution copies the
link actor and link reason. A terminal resolution copies the disposition actor
and stores `work_item_closed`, `work_item_failed`, or `work_item_iceboxed` as
its resolution reason when the current-release disposition seam performs the
resolution. The Work Item row retains any separate failure reason.

The wake delivery path shall not re-arm a placement wake. An ignored placement
obligation remains pending and overdue. `topline-placement-list` returns the
caller's visible obligations in `openedAt ASC, id ASC` order. Its `--state`
filter accepts `pending|resolved|all`; `resolved` includes the three terminal
obligation states. An omitted `--state` or wire `state` field means `pending`.

The exact placement-list success shape is
`{"placements":[<placement>...]}`. A placement object has exactly these fields:

```json
{
  "cause": "migration",
  "causeRef": "release_0.1.x",
  "dueAt": 123,
  "id": "tlp_...",
  "openedActor": {"kind": "process", "ref": "tightbeam"},
  "openedAt": 123,
  "ownerUserId": "mike",
  "promptWake": {"id": "w_...", "state": "pending"},
  "resolutionActor": null,
  "resolutionReason": null,
  "resolvedAt": null,
  "state": "pending",
  "workItemId": "wi_...",
  "workItemTitle": "Ship durable Toplines"
}
```

`promptWake.state` is the current wake-row value `pending|fired|canceled`.
`resolutionActor`, `resolutionReason`, and `resolvedAt` are JSON null while the
obligation is pending and are non-null after resolution. The placements array
uses `openedAt ASC, id ASC`. `sourceCausalEventSeq` and `historyCausalSeq` are
internal reconciliation rails and do not add fields to this canonical response.
`resolutionCausalEventSeq` is also internal and does not add a response field.

Boot reconciliation shall run after additive schema creation on each boot of
this release, including a re-upgrade after rollback. Its terminal phase runs
first. It considers pending Placement obligations in `openedAt ASC, id ASC`
order. For each candidate it uses one transaction to re-read the obligation,
its Work Item, the prompt wake, and matching causal events before it writes.

When the Work Item has a Qualifying rollback-era terminal disposition, the
terminal phase resolves the existing obligation as `work_terminal`. It records
`resolutionActorKind = 'process'` and `resolutionActorRef = 'tightbeam'`. It
stores that qualifying event's sequence in `resolutionCausalEventSeq`. It maps
current Work Item state to the exact resolution cause as follows:

| Work Item state | `resolutionReason` |
| --- | --- |
| `closed` | `reupgrade_terminal_reconciliation_closed` |
| `failed` | `reupgrade_terminal_reconciliation_failed` |
| `iceboxed` | `reupgrade_terminal_reconciliation_iceboxed` |

The transaction sets `resolvedAt` to its Mutation time and updates
`historyCausalSeq` to `COALESCE(MAX(causal_events.seq), 0)`. It does not change
the Work Item state or failure reason. The process actor identifies the repair;
the matching causal-event row remains the durable evidence of the old-gateway
terminal transition.

If the referenced wake is pending, the same transaction changes it to
`canceled` and sets `canceledAt = resolvedAt`. The obligation's immutable
`promptWakeId` links that wake mutation to the process actor and explicit
resolution cause. If the wake is fired or already canceled, reconciliation
leaves every wake field unchanged. In each wake state, it creates no placement
obligation, wake, or prompt. The resolved `work_terminal` row is the durable
record that no new prompt is due for that episode.

After terminal reconciliation finishes, ordinary open-item reconciliation
considers Work Items in UTF-8 byte order by Work Item ID. For each candidate it
uses one transaction to re-read the current Work Item, active memberships,
pending obligation, placement history, and matching causal events before it
writes.

For an open Work Item with zero active memberships, no placement-obligation
history, and `createdAt` earlier than the Toplines production schema stamp's
`stampedAt`, reconciliation shall create one `migration` episode and one prompt
as before. A Work Item created at or after activation does not use this path.
Therefore, unlinking a current Work membership cannot become a delayed
migration prompt after restart. A Work Item with placement history does not use
this migration path.

For an open Work Item with zero active memberships, placement history, and no
pending obligation, reconciliation shall compute `H` and the Qualifying
rollback-era reopen from the rows defined in Terms. If no qualifying event
exists, it writes nothing. If one exists, it creates exactly one `reopened`
episode with `causeRef` equal to the Work Item ID,
`sourceCausalEventSeq` equal to that event's sequence,
`openedActorKind = 'process'`, and `openedActorRef = 'tightbeam'`. It sets the
new row's `historyCausalSeq` to the current causal high-water value and creates
one immediate prompt in the same transaction. The high-water value is at least
the source event sequence. If several post-watermark reopen events exist, only
the greatest sequence opens the current episode.

The transaction, pending-obligation uniqueness, source-event uniqueness, and
stored high-water value make crash and restart safe. A later boot cannot reopen
an episode from the same or an older event, including after the prior episode is
resolved. Reconciliation never orders by millisecond time, assigns a Topline,
or runs outside release boot. Schema creation, terminal reconciliation, and
ordinary open-item reconciliation all finish before the gateway recovers the
wake scheduler or exposes handlers.

### R7. Topline reads

`toplines [--state open|closed|all]` sends wire verb `toplines`. The default
state is `open`. It returns:

```json
{
  "toplines": [
    {
      "id": "tl_...",
      "ownerUserId": "mike",
      "title": "Ship durable Toplines",
      "state": "open",
      "createdActor": {"kind": "session", "ref": "agent:..."},
      "createdAt": 123,
      "updatedAt": 456,
      "closedAt": null,
      "activeWorkCount": 2,
      "openConcernCount": 1
    }
  ]
}
```

Rows sort by `createdAt ASC, id ASC`. `activeWorkCount` counts active Work
memberships. `openConcernCount` is retained for compatibility and counts
current Concern tag definitions in the Topline; `open` does not name a Concern
lifecycle state. The object shown above is the **Topline summary** and has
exactly those fields.

`topline <toplineId> [--history]` sends wire verb `topline`. It returns the same
Topline summary inside `{"topline":<object>}`, augmented with these exact
arrays:

- `workMemberships`, sorted by `linkedAt ASC, id ASC`, with the membership ID,
  Work Item ID, Work Item title and state, link reason, actor, and link time;
- `concerns`, sorted by `createdAt ASC, id ASC`, with the active Work membership
  IDs tagged by each Concern;
- `history` only when requested.

The read returns active Work memberships, each current Concern, and current
Concern tag associations. History contains no ended tag-association episodes.
The augmented Topline object has no other fields.

A Work-membership object has exactly these fields:

```json
{
  "id": "tlm_...",
  "linkReason": "Groups the release work",
  "linkedActor": {"kind": "session", "ref": "agent:..."},
  "linkedAt": 123,
  "ownerUserId": "mike",
  "toplineId": "tl_...",
  "unlinkReason": null,
  "unlinkedActor": null,
  "unlinkedAt": null,
  "workItemId": "wi_...",
  "workItemState": "open",
  "workItemTitle": "Ship durable Toplines"
}
```

An active membership uses null for each unlink field. An ended membership uses
a non-null reason, actor, and time. `workMemberships` includes active rows only
and sorts them by `linkedAt ASC, id ASC`. Mutation responses use this same
object shape and capture Work Item title and state at the mutation time.

A Concern object has exactly these fields:

```json
{
  "createdActor": {"kind": "user", "ref": "mike"},
  "createdAt": 123,
  "id": "tlc_...",
  "membershipIds": ["tlm_a", "tlm_b"],
  "title": "Migration risk",
  "toplineId": "tl_...",
  "updatedAt": 123
}
```

`membershipIds` lists active Work memberships tagged with this Concern and
sorts by membership ID ascending using UTF-8 bytes.
The `concerns` array sorts by `createdAt ASC, id ASC`.

A Concern-tag object used by mutation responses has exactly these fields:

```json
{
  "concernId": "tlc_...",
  "membershipId": "tlm_...",
  "tagReason": "This work addresses the risk",
  "taggedActor": {"kind": "user", "ref": "mike"},
  "taggedAt": 123,
  "toplineId": "tl_..."
}
```

When requested, `history` contains event objects in `seq ASC`. Each event object
has exactly `actor`, `at`, `concernId`, `detail`, `kind`, `membershipId`,
`reason`, `seq`, and `toplineId`. The two optional identifier
fields and `reason` use JSON null when the event kind has no value for them.
`actor` is a non-null actor object. `detail` has exactly the keys in R4.

The `toplines` handler refuses legacy telemetry parameters with
`invalid_message`. The `topline` handler refuses `under` and `assignments` with
`invalid_message`.

### R8. Execution Map rename

`execution-map` replaces the old telemetry CLI command `toplines` and sends wire
verb `execution-map`. It accepts the source baseline's `origin`, `owner`,
`state`, `quiet-over`, `spec`, `spec-sha`, `session`, and `tree` options.

`execution-map-select` replaces the old telemetry CLI command `topline` and
sends wire verb `execution-map-select`. It accepts exactly one source baseline
selection:

- `--under <workItemId>` with the roster filters; or
- `--assignments <id,...>` without roster filters.

The implementation shall rename the telemetry module to
`Tightbeam.ExecutionMap`. It shall move the source baseline's reader and proof
suite. The final proof suite shall retain each source-baseline fixture and each
non-command-name assertion. Only module names, wire verbs, CLI names, and error
text that contains the retired command names can change.

The router shall classify both Execution Map verbs as non-target verbs. A
volunteered typed target shall receive the same early refusal as the current
telemetry verbs.

**Candidate-completion acceptance gate: mandatory real-path smoke.** Lane 4
shall update `scripts/feature_smoke.exs` and run it with a fresh packaged
Gateway process and the exact matching packaged CLI. The smoke shall
use the real HTTP/wire router, the normal boot sequence, the normal wake
scheduler, and a disposable personal Main session. Direct handler calls, a
handwritten response fixture, or an alternate runner cannot satisfy this gate.

The smoke database shall begin from a source-baseline schema containing one
open unlinked Work Item with no placement history. The first Candidate boot
shall reconcile that item, deliver its one placement prompt through the normal
session lane, and expose the obligation through the packaged CLI. The same run
shall call `execution-map`, create a Topline, link the Work Item, and read it
with `topline`. A gateway restart on the same database shall create no second
migration obligation or prompt.

The smoke shall then create a second open unlinked Work Item with the real
Candidate `work-item-create` CLI and observe its one fired placement prompt.
It shall stop that Gateway, boot the Previous-package fixture with its exact
matching packaged CLI, successfully read telemetry through the fixture's old
`toplines` command, close the second Work Item with the real
`work-item-close` wire path, capture that close event's causal sequence, and
create a third open unlinked Work Item through the fixture's real
`work-item-create` wire path. It shall then stop the Previous-package fixture
and re-upgrade the same database. The fresh Candidate Gateway shall resolve the
second Work Item's still-pending episode under `process:tightbeam`, store the
captured sequence and `reupgrade_terminal_reconciliation_closed`, preserve the
fired wake and delivered turn byte-for-byte, and create no replacement prompt.
Its later open-item phase shall create one migration episode and one prompt for
the third Work Item. After handler exposure, the packaged Candidate `topline`
read shall equal its pre-rollback canonical bytes. The run shall create no other
episode or prompt.

The smoke may bound each delivery observation to 10 seconds; expiration fails
the test and does not decide placement state. AC64 is the exact pass/fail
contract. This gate must pass before Lane 4 can complete. It does not authorize
deployment.

### R9. Wire and CLI mutation verbs

The remaining Topline wire verbs match their CLI names:

- `topline-create --title <text> --key <key>`
- `topline-update <toplineId> --title <text> --reason <text> --key <key>`
- `topline-close <toplineId> --reason <text> --key <key>`
- `topline-reopen <toplineId> --reason <text> --key <key>`
- `topline-link-work <toplineId> <workItemId> --reason <text> --key <key>`
- `topline-unlink-work <membershipId> --reason <text> --key <key>`
- the Concern verbs in R3;
- `topline-work-leave-unlinked <workItemId> --reason <text> --key <key>`; and
- `topline-placement-list [--state pending|resolved|all]`.

Mutation verbs carry each record ID named by their CLI form as an ordinary body
parameter. `topline-placement-list` carries only its optional `state` filter.
These verbs accept no top-level typed target. The router authenticates the
principal before a handler resolves a record ID.

Each successful mutation returns exactly one of these canonical shapes:

| Mutation | Success result |
| --- | --- |
| `topline-create`, `topline-update`, `topline-close`, `topline-reopen` | `{"topline":<Topline summary>}` |
| `topline-link-work` | `{"membership":<Work-membership object>,"resolvedPlacementId":<string-or-null>}` |
| `topline-unlink-work` | `{"membership":<Work-membership object>,"openedPlacement":null,"untaggedConcernIds":[<id>...]}` |
| `topline-concern-create`, `topline-concern-update` | `{"concern":<Concern object>}` |
| `topline-concern-link-work` | `{"concernTag":<Concern-tag object>}` |
| `topline-concern-unlink-work` | `{"concernId":<id>,"membershipId":<id>}` |
| `topline-work-leave-unlinked` | `{"placement":<placement>}` |

`untaggedConcernIds` sorts by ID ascending using UTF-8 bytes. A link that
resolves no pending placement uses null for `resolvedPlacementId`. An unlink
always uses null for `openedPlacement`; that field remains only for response
compatibility. The response object
for a committed mutation is rendered once, stored in the idempotency row, and
returned byte-for-byte on an authorized matching replay.

Each Topline-handler refusal returns exactly
`{"code":"<slug>","message":"<message>"}` with this closed mapping:

| Slug | Message |
| --- | --- |
| `concern_tag_absent` | `concern tag is not applied to membership` |
| `concern_tag_exists` | `concern tag is already applied to membership` |
| `idempotency_conflict` | `idempotency key conflicts with a prior request` |
| `invalid_message` | `invalid message` |
| `invalid_transition` | `invalid state transition` |
| `membership_ended` | `membership is already ended` |
| `membership_exists` | `active membership already exists` |
| `no_change` | `no change` |
| `not_found` | `record not found` |
| `owner_mismatch` | `topline and work item owners differ` |
| `placement_not_pending` | `placement is not pending` |
| `process_denied` | `process principals cannot access Toplines` |
| `topline_closed` | `topline is closed` |
| `topline_mismatch` | `concern and membership toplines differ` |

Validation chooses the first refusal in this order: CLI compatibility;
authentication and principal kind; wire shape; owner-filtered record visibility;
owner equality and same-Topline references; idempotency replay or conflict;
mutable lifecycle state; uniqueness. The existing compatibility layer retains
its source-baseline HTTP 426 `incompatible_cli` bytes and runs before this
mapping. Transport-level missing or invalid authentication retains its existing
gateway bytes and does not enter a Topline handler.

Within the mutable-lifecycle phase, a Topline update compares Canonical titles
before it tests whether the Topline is closed. A Concern update first requires an
open parent Topline, then compares Canonical titles.

### R10. Authorization and validation

User and session principals can read and mutate rows that their user owns.
Admins can read and mutate rows from any owner. Process principals receive
`process_denied`.

A non-admin mutation that names an unknown or invisible Topline, membership,
Concern, Concern tag association, placement obligation, or Work Item returns:

```json
{"code":"not_found","message":"record not found"}
```

The handler shall filter by owner before it distinguishes record type or state.
An authorized cross-owner link attempt returns `owner_mismatch`. Missing,
blank, overlength, malformed, and mutually exclusive inputs return
`invalid_message` before a transaction writes state.

Authorization runs before idempotency replay. The same request key does not
restore access that the caller no longer has.

Read authorization uses omission. A Topline response in a database that also
contains another user's rows shall be byte-identical to a response from a twin
database without those rows.

### R11. Rail fact

The implementation shall add exactly one new Rules fact:

```text
work_item.has_topline => :bool
```

The fact resolves the Work Item through the existing `$work_item_id` dependency.
It returns:

- `nil` when `$work_item_id` is nil, names no Work Item, or names a Work Item
  that the current caller cannot see under I18 through I21;
- `false` when the Work Item exists and has zero active memberships; and
- `true` when the Work Item exists and has one or more active memberships.

The fact query counts no ended membership and no Concern tag. It returns
one boolean, not Topline IDs, reasons, titles, or placement suggestions. Rules
retain the existing behavior in which nil satisfies no operator.

### R12. Race and crash behavior

Each Topline mutation shall re-read authorization and affected current state in
its write transaction. The check and action are indivisible.

A link racing a Topline close has one of two outcomes based on transaction
order:

- link commits first, then close commits and retains that membership; or
- close commits first, then link returns `topline_closed`.

A final unlink racing a Work Item terminal disposition has the same outcome in
either transaction order: the membership ends, all of its Concern tag
associations disappear, and unlink creates no Placement obligation or prompt.

A process crash before commit leaves no current-state row, event, idempotency
row, obligation, or wake from that mutation. A process crash after commit is a
success. Retrying with the same key returns the committed response.

On gateway restart, additive schema creation runs first. Re-upgrade terminal
reconciliation runs second. Ordinary open-item reconciliation runs third. The
gateway then recovers the wake scheduler and exposes handlers. A pending prompt
for a terminal Work Item therefore cannot fire between candidate selection and
its cancellation.

For each terminal candidate, the state and causal-event checks, obligation
resolution, watermark update, and pending-wake cancellation are indivisible. A
crash before commit leaves the obligation and wake unchanged. A crash after
commit is a success; restart sees a non-pending obligation and writes nothing.
A fired or already canceled wake remains unchanged across either path.

Ordinary open-item reconciliation then fills pre-activation Work Items with no
placement history and Work Items with a Qualifying rollback-era reopen. It
excludes a post-activation Work Item that became unplaced through membership
unlink. For each open
candidate, its state check, causal watermark comparison, obligation insert, and
wake insert are indivisible. A crash before commit leaves no new obligation or
wake. A crash after commit is a success, and restart recognizes the source
event as already bracketed.

### R13. Compatibility, migration, and rollback

Each Target line produces one Candidate package that binds a matching Gateway
and CLI version: `0.1.9` on the `0.1.9` line and `0.2.0` on the `0.2.0` line.
The Gateway retains the source baseline's pre-1.0 exact version check. An old or
future CLI receives HTTP 426 `incompatible_cli` before the changed `toplines` or
`topline` semantics can run.

Each candidate registers the two deterministic title scalar functions in R1 on
each product database connection before Toplines schema activation. On first
production boot, Lane 1 queries the exact Toplines schema manifest. If the stamp
table and every other manifest object are absent, one transaction creates the
complete R1 through R6 tables and indexes, creates the local stamp table, and
inserts shape `standalone-toplines-v5`. It changes no Source-baseline table and
does not change the product-wide `schema_stamp`.

The local stamp table has exactly `singleton`, `shape`, and `stampedAt`.
`singleton` is the primary key and must equal integer 1. `shape` is non-blank
text. `stampedAt` is a non-negative integer. Exactly one row exists after
activation.

Boot classifies every other state in this order. A present stamp table whose
manifest SQL differs returns `schema_shape_mismatch`. An absent stamp table
with any other manifest object, or an exact stamp table with no row, returns
`unregistered_toplines_core_shape`. An exact stamp table with a row count,
singleton, field type, or `stampedAt` value outside its contract returns
`schema_shape_mismatch`. One structurally valid stamp row with a shape other
than `standalone-toplines-v5` returns `unknown_toplines_schema_stamp`. With the
exact row, boot requires every other manifest object to exist with its exact
manifest SQL; a missing or altered object returns `schema_shape_mismatch`, and
an exact set is a no-op. Each refusal occurs before DDL, reconciliation, wake
recovery, or handler exposure and preserves every schema entry and row. Boot
reads `sqlite_schema` only to compare it with the committed manifest. It does
not infer a migration shape, migrate a partial core row, drop a table, or widen
a CHECK in place.

Rollback proof uses the owner-verified Previous-package fixture and its exact
matching CLI for that Target line. The previous Gateway ignores the additive
Toplines tables, supporting indexes, and local stamp. It presents the old
telemetry command names during the fixture interval. It cannot mutate
Toplines. Candidate re-upgrade preserves the rows and first resolves pending
placement episodes for Qualifying rollback-era terminal dispositions. It then
runs ordinary reconciliation for open Work Items created during the fixture
interval and for Qualifying rollback-era reopens after prior placement history.

Mixed old and new binaries are unsupported. The exact CLI check turns the mix
into a refusal instead of a semantic fallback.

### R14. Deletion and subtraction assessment

No hard-delete verb ships. Closing and membership unlinking preserve causal
history. Deleting this surface would fail G1 through G5 because the user asked
for durable intent grouping. Accepting silent unplaced work would fail G5.

The design adds Direct Intent Membership because Execution Map ancestry cannot
represent user judgment. A current many-to-many Concern tag table is the
smallest mechanism that preserves optional grouping inside one Topline without
inventing issue lifecycle or reference-episode history. Accepting implied
Concern membership would violate invariant I1.

The design adds one-shot Placement Episodes because manual-only placement was
rejected by the user decision. A periodic organizer was deleted from the design
because the lifecycle events are observable and an overdue obligation is a
named value.

The design adds one Rules boolean because rails need neutral membership truth.
It does not add a statute because product policy must decide what to do with the
truth.

V2 deletes the paired nullable user/session actor columns. It adds `CHECK`,
partial unique, and composite foreign-key constraints because deleting the
durable intent and placement rows would fail G1 through G5, while accepting
contradictory stored states would make I1 through I17 undecidable at review.
These database constraints are the highest affordable rail at the persistence
seam.

V3 retains event history because G2, I5 through I7, and I17 require attributable
causal evidence. Deleting exposed history would remove that evidence, and
accepting owner-dependent sequence gaps or cross-Topline parents would violate
the visibility rule in I22. Topline-local sequence and composite parent keys are
the smallest database rails that preserve the required history without exposing
another Topline's activity.

V4 retains rollback and re-upgrade support under owner ruling
`att_152df3a9-287c-4b0e-a945-6d00568c449a`. Deleting reopen prompting would
violate G5 and AC38. Accepting a missed rollback-era reopen would silently lose
an observable lifecycle event. The Placement causal watermark and exact source
event are the smallest deterministic bracket: millisecond time can tie, while
the existing causal sequence already orders the event. The reconciler records
the process that observed an unattributed baseline event instead of inventing a
human actor.

V5 retains pending placement history through rollback under owner ruling
`att_748b827c-9fee-4e87-9e52-3b9076ca57bb`. Deleting rollback support remains
rejected. Deleting a stranded obligation would erase its prompt and decision
history. Accepting it as pending would contradict I39. Process-attributed
resolution of the existing row is the smallest repair: `promptWakeId` already
links the wake, and the existing wake state already distinguishes pending,
fired, and canceled history. No new table, wake state, prompt, or user action is
added.

Operating pattern taught to agents: none outside the product's placement prompt
and CLI help. This implementation does not amend the operating manual or an
archetype identity.

## Acceptance

Each case uses a fresh database unless the case states a restart or rollback.
Each test freezes the evaluation clock when it compares bytes.

### Execution Map separation and parity

AC1. Given each fixture and non-command-name assertion in the source baseline
`ToplinesTest`, when the moved `ExecutionMap` proof suite runs, then each
assertion passes without weakening or deletion.

AC2. Given the source baseline roster filters, when the new CLI parses
`execution-map`, then the wire request uses verb `execution-map` and preserves
each parameter value.

AC3. Given `--under` and `--assignments` cases, when the new CLI parses
`execution-map-select`, then it preserves the source baseline's mutual exclusion
and filter refusal behavior.

AC4. Given a typed target field on either Execution Map wire verb, when the
router validates the request, then it returns the same early
`invalid_message` bytes for unknown, visible, and invisible target values.

AC5. Given a new CLI call to `toplines`, when the gateway handles it, then the
response has a `toplines` array and has no Execution Map `edgeBasis`, `coverage`,
`items`, or `roots` field.

AC6. Given legacy telemetry fields on `toplines`, or `under|assignments` on
`topline`, when a matching-version client sends them, then the gateway returns
`invalid_message` and writes no Topline, membership, Concern, placement, or wake
row.

AC7. Given an old pre-1.0 CLI version, when it sends the former `toplines`
request to the new gateway, then the gateway returns 426 `incompatible_cli`
before any handler lookup or record-ID lookup.

### Direct membership

AC8. Given an open Topline and an open same-owner Work Item, when the owner links
them with a reason and key, then one active `tlm_` episode and one `work_linked`
event commit.

AC9. Given one Work Item and two open same-owner Toplines, when the owner links
the Work Item to each Topline, then both active memberships exist and both
Toplines list the Work Item.

AC10. Given an active pair, when another link with a different key races it,
then one transaction commits and the other returns `membership_exists` without
an extra event.

AC11. Given an active membership, when the owner unlinks its membership ID with
a reason, then that episode ends and one `work_unlinked` event commits.

AC12. Given an ended episode and a new relink episode for the same pair, when a
caller retries the old membership ID, then it returns `membership_ended` and the
new episode remains active.

AC13. Given blank or overlength link or unlink reason, when the caller submits
the mutation, then it returns `invalid_message` and writes no state, event,
obligation, or wake.

AC14. Given a closed Topline, when a caller links new work, then the handler
returns `topline_closed` and writes nothing.

AC15. Given a Topline with open Work Items, when its owner closes it, then the
Topline becomes closed and its memberships remain active.

AC16. Given a closed Topline, when its owner reopens it with a new key and
reason, then it accepts a later membership.

AC17. Given a stored title `Café` and an update title consisting of U+0020,
`Cafe`, U+0301, and U+00A0, when the owner submits the update, then Canonical
title comparison returns `no_change`. Given a different Canonical title, when
the owner updates the Topline, then list and get return the new Canonical title
and history retains both prior and new Canonical titles in the rename event.

### Concerns

AC18. Given an open Topline, when its owner creates a Concern, then the Concern
is an active tag definition that belongs to that Topline and no Work Item gains
membership.

AC19. Given a Concern and an active Work membership in the same Topline, when
the owner applies the Concern, then one Concern tag association exists and
`work_item.has_topline` has the same value as before the tag.

AC20. Given a Concern in Topline A and a Work membership in Topline B, when a
caller tries to apply the Concern, then the handler returns `topline_mismatch` and writes
nothing.

AC21. Given one membership with two Concern tags, when the owner unlinks the
membership, then both tag associations disappear in the same transaction, the
response lists both Concern IDs in UTF-8 order, only `work_unlinked` is added to
history, and no Placement obligation or prompt exists.

AC22. Given one Concern applied to two Work memberships and one membership
carrying two Concerns, when the owner reads the Topline, then each Concern lists
its tagged membership IDs in UTF-8 order and both many-to-many associations are
visible.

### Authorization and visibility

AC23. Given two users with Toplines, Work Items, memberships, Concerns, and
history, when one non-admin lists or gets rows, then response bytes match a twin
database where the other user's rows do not exist.

AC24. Given an unknown ID and a foreign-owner ID, when a non-admin performs each
read or mutation, then both responses equal
`{"code":"not_found","message":"record not found"}`.

AC25. Given an admin, when the admin lists Toplines, then rows from both owners
appear in canonical order.

AC26. Given an admin, a Topline owned by user A, and a Work Item owned by user B,
when the admin attempts a link, then the handler returns `owner_mismatch`.

AC27. Given a process principal, when it invokes a Topline read or mutation,
then the handler returns `process_denied`.

### Idempotency, races, and recovery

AC28. Given one mutation request that emits a Topline event, when the caller
sends it twice with the same key and the same R5 Fingerprint JSON, then both
responses match and the database contains one mutation event.

AC29. Given a committed key, when the caller reuses it with a different title,
reason, or target ID whose NFC-normalized R5 parameter value differs, then the
handler returns `idempotency_conflict` and the first state remains.

AC30. Given a forced crash before transaction commit, when the gateway restarts,
then no partial Topline state, event, idempotency row, obligation, or wake exists.

AC31. Given a forced crash after commit but before response delivery, when the
caller retries the same key, then it receives the stored response and no second
event appears.

AC32. Given a link racing a Topline close, when both finish, then the database
matches one of the two R12 serial outcomes and no active membership belongs to a
Topline that was already closed when its link checked state.

AC33. Given a final unlink racing a Work Item close, when both finish, then the
membership and its Concern tags are absent and unlink created no Placement
obligation, prompt, or wake.

### Placement

AC34. Given a session-created open Work Item with no membership, when create
commits, then one pending `created` obligation and one prompt wake to the
owner's Main commit in the same transaction.

AC35. Given the obligation from AC34, when the Work Item gains membership before
wake delivery, then the obligation becomes `linked` and the pending wake is
canceled.

AC36. Given the obligation from AC34, when the owner records leave-unlinked with
a reason, then the obligation becomes `left_unlinked` and no membership appears.

AC37. Given a placement wake that fires, when the scheduler runs later without a
new lifecycle event, then no replacement placement wake exists and the
obligation remains pending.

AC38. Given an unlinked iceboxed Work Item, when its owner reopens it, then one
new `reopened` episode and one prompt commit.

AC39. Given a Work Item with two active memberships, when either or both end,
then no unlink creates a Placement obligation, prompt, or wake.

AC40. Given a pending obligation, when the Work Item closes, fails, or iceboxes,
then the obligation becomes `work_terminal` and its pending wake is canceled.

AC41. Given source-baseline Work Items plus new empty Topline tables containing
one open unlinked Work Item with no placement history, one closed unlinked Work
Item, one open linked Work Item, and one open unlinked Work Item with a prior
`left_unlinked` obligation and no later Qualifying rollback-era reopen, when boot
reconciliation runs twice, then it creates one migration episode only for the
first Work Item.

AC42. Given a pending obligation whose prompt fired, when the owner lists pending
placement obligations, then the row remains visible with its past `dueAt` and
fired wake ID.

### Rail fact

AC43. Given a call with no Work Item reference, an unknown Work Item, a foreign
Work Item, a visible unlinked Work Item, a visible Work Item with only ended
memberships, and a visible Work Item with two active memberships, when Rules
computes `work_item.has_topline`, then the results are respectively nil, nil,
nil, false, false, and true.

AC44. Given a directly inserted corrupt Concern tag association that names an
ended Work membership, when Rules computes the fact for that visible Work Item,
then it returns false.

AC45. Given the shipped identity tree after implementation, when Rules loads,
then no statute condition names `work_item.has_topline`.

### Migration, rollback, and deletion

AC46. Given a source-baseline database with no Toplines-owned object, when a
Candidate first boots, then one transaction preserves every Source-baseline
table, creates the complete R1 through R6 objects, and records Toplines shape
`standalone-toplines-v5` in singleton row 1 with one non-negative `stampedAt`.
A repeated boot changes no schema or row. A crash
before the activation commit leaves no Toplines object or stamp; a restart then
performs the one activation. A crash after commit leaves the complete stamped
shape and restart writes nothing. Given an Unregistered core schema, boot
returns `unregistered_toplines_core_shape` before changing any schema or row.
Given a local stamp other than the exact V5 shape, boot returns
`unknown_toplines_schema_stamp` with the same no-write result. Given the exact
stamp and one missing or altered manifest object, boot returns
`schema_shape_mismatch` and preserves every schema entry and row. Given an
altered stamp table, including one that permits invalid row cardinality, or a
present stamp row with an invalid singleton, field type, or `stampedAt`, boot
returns `schema_shape_mismatch` with the same no-write result.

AC47. Given Topline mutations under the new release, when the previous release
and its matching CLI boot against the same database, then boot succeeds, old
telemetry reads succeed, and Topline rows remain byte-for-byte unchanged.

AC48. Given an open Work Item created during rollback, when the new release
boots again, then boot reconciliation creates one placement episode for
it and preserves prior Topline rows.

AC49. Given CLI help, the wire verb allow-list, and Gateway handlers, when a test
searches the released surfaces, then no Topline, Concern definition, membership,
placement, or event hard-delete verb exists.

AC50. Given a closed Topline with an applied Concern, when the owner removes the
tag, then removal succeeds. When the owner tries to create, rename, or apply a
Concern, then each operation returns `topline_closed` and writes nothing.

AC51. Given a closed or failed same-owner Work Item and an open Topline, when the
owner links them with a reason and key, then the membership commits.

AC52. Given a Topline read request that contains `idempotencyKey`, when the
router validates it, then it returns `invalid_message` and writes no Topline
state.

AC53. Given an admin mutation that committed under a key, when that user loses
admin authorization and retries the key, then the gateway returns the current
not-found authorization response instead of the stored success response.

AC54. Given one Topline, when a membership, Concern, or explicit Concern tag
mutation commits, then that Topline's `updatedAt`, each affected current-state
timestamp, and each event timestamp equal the transaction's one Mutation time.

AC55. Given a session-created Work Item, a user-reopened Work Item, and boot
reconciliation, when each opens a placement episode, then the opening actors are
respectively the creator session, the user, and `process:tightbeam`. Given a
final unlink by a session, then no placement episode opens.

AC56. Given an open Work Item created while the previous release runs during a
rollback interval, when the new release boots twice, then the first boot creates
one migration episode and the second boot creates none.

AC57. Given the owner's Main has a running turn when a placement wake becomes
due, when the scheduler delivers the wake, then no second turn runs for that
session. When the running turn ends, then the lane can start the placement turn.

AC58. Given an open or closed Topline whose stored title equals the requested
Canonical title, when an authorized caller submits update with a new key, then
the handler returns `no_change` and writes no event, idempotency row, or
`updatedAt` change. Given a closed Topline and a different Canonical title, when
the caller submits update, then the handler returns `topline_closed`. Given an
Concern under an open Topline and an equal Canonical title, when the caller
submits update, then the handler returns `no_change` with the same no-write
result.

AC59. Given an applied Concern tag, when another key tries to apply the same
pair, then it returns `concern_tag_exists`. Given an absent pair, when a caller
tries to remove it, then it returns `concern_tag_absent`. Neither refusal writes
a row.

AC60. Given one Work membership tagged with Concerns `tlc_b` and `tlc_a`, when
the owner unlinks the Work membership, then the response lists `tlc_a` before
`tlc_b`, both tag rows are absent at commit, and history contains no derived
Concern untag event.

AC61. Given the released product source, when a source guard searches writes to
the seven state families named by the Mutation seam, then runtime writes exist
only in `Tightbeam.Toplines`; schema DDL is the sole exception.

AC62. Given a pending placement obligation, when the owner submits
leave-unlinked with a blank reason, then the handler returns `invalid_message`.
Given no pending obligation, when the owner submits a valid reason, then the
handler returns `placement_not_pending`. Neither refusal writes a row.

AC63. Given a successful membership link or Concern tag application and its
key, when later state changes and the authorized caller retries the original
request with the same key, then the handler returns the stored original
response. A new key receives the current-state result.

### Canonical contracts, structural rails, and real-path gate

AC64. Given a Target line's exact baseline database with one open unlinked Work
Item and no placement history, a disposable personal Main, a fresh packaged
Candidate gateway, and the exact matching packaged CLI, when the updated
`scripts/feature_smoke.exs` boots the Gateway through the normal boot path, then
within 10 seconds the
normal wake lane fires one `process:tightbeam` migration prompt naming its
obligation and three choices. When the smoke calls `execution-map`,
`topline-placement-list`, `topline-create`, `topline-link-work`, and `topline`
through the real CLI and wire router, then each canonical response succeeds.
When it restarts the gateway on the same database, then no second migration
obligation or prompt exists. Given the smoke then creates a second open unlinked
Work Item with the real Candidate `work-item-create` CLI and observes its fired
placement prompt, when it boots the verified Previous-package fixture and its
matching CLI, successfully reads telemetry through the fixture's old
`toplines` command, closes that Work Item through the real `work-item-close`
wire path, captures that close event's causal sequence, creates a third open
unlinked Work Item through the fixture's real `work-item-create` wire path, and
re-upgrades the same database through a fresh Candidate Gateway, then boot
resolves the second Work Item's pending episode as `work_terminal` under
`process:tightbeam` before handler exposure, stores the captured sequence in
`resolutionCausalEventSeq`, stores
`reupgrade_terminal_reconciliation_closed`, preserves the fired wake and
delivered turn byte-for-byte, and creates no replacement prompt. Its later
open-item phase creates one migration episode and one prompt for the third Work
Item and no other episode or prompt, and its packaged `topline` read equals the
pre-rollback canonical bytes. Lane 4 fails if any step uses a direct handler,
handwritten response fixture,
alternate runner, retired telemetry verb, inferred previous package, or
unverified package digest. The case runs independently for `0.1.9` and `0.2.0`.

AC65. Given direct SQL inserts with an invalid Topline state, a partial creation
actor, an open row with `closedAt`, a closed row without `closedAt`, a closed row
with non-integer `closedAt`, `updatedAt < createdAt`, a non-text title, a title
with a leading U+00A0, a decomposed non-NFC title, an empty Canonical title, or a
title with 2,001 Unicode scalar values, when SQLite evaluates each insert, then
the applicable `toplines` `CHECK` rejects it.

AC66. Given direct SQL inserts with a partial link actor, blank link reason,
partial unlink tuple, non-`user|session` unlink actor, non-integer `unlinkedAt`, or
`unlinkedAt < linkedAt`, when SQLite evaluates each insert, then the applicable
membership `CHECK` rejects it.

AC67. Given direct SQL inserts with a partial Concern creation actor,
non-integer creation or update time, `updatedAt < createdAt`, a non-canonical
title, or a title outside the 1-through-2,000 scalar-value bound, when SQLite
evaluates each insert, then the applicable Concern `CHECK` rejects it.

AC68. Given direct SQL inserts into `topline_concern_tags` with a partial tag
actor, blank tag reason, or non-integer `taggedAt`, when SQLite evaluates each
insert, then the applicable Concern-tag `CHECK` rejects it. Given a duplicate
`(concernId,membershipId)` pair, then the primary key rejects it.

AC69. Given direct SQL inserts with an invalid placement cause or state, a
partial opening actor, a process actor on `created`, a migration or
process-reopened actor other than
`process:tightbeam`, `dueAt != openedAt`, a blank wake ID, a pending row with a
resolution value, a resolved row with one resolution value missing, a process
resolution on `linked` or `left_unlinked`, a process terminal resolution with
an ordinary terminal reason, a `user|session` resolution with a re-upgrade
terminal-reconciliation reason, a process resolution reference other than
`tightbeam`, a non-integer placement time, a non-integer or negative
`historyCausalSeq`, a reopened row without a positive
`sourceCausalEventSeq`, a non-reopened row with a source sequence, a
process-attributed re-upgrade terminal row without a positive
`resolutionCausalEventSeq`, a `user|session` resolution with a resolution
sequence, or a create/reopen cause reference unequal to the Work Item ID, when
SQLite evaluates each insert, then the applicable placement
`CHECK` rejects it. Given a reopened row whose source causal event belongs to a
different Work Item, or a terminal row whose resolution causal event belongs to
a different Work Item, when SQLite evaluates it, then the applicable composite
foreign key rejects it. Given a second placement row for the same Work Item and
source sequence or resolution sequence, when SQLite evaluates it, then the
applicable partial unique index rejects it.

AC70. Given direct SQL event inserts with an unknown kind, a partial actor, an
actor kind outside `user|session`, a non-integer or non-positive `seq`,
non-integer `eventAt`, malformed JSON detail, the wrong detail key set or value
type, or an identifier supplied for an event kind that does not accept it, when
SQLite evaluates each insert, then the applicable event `CHECK` rejects it.

AC71. Given a Topline owned by user A and a Work Item owned by user B, when a
direct SQL insert attempts a membership carrying either owner, then a composite
foreign key rejects it.

AC72. Given a Concern in Topline A and a membership in Topline B, when a direct
SQL insert attempts a Concern tag association, then a composite foreign key
rejects it.

AC73. Given one successful fixture for each mutation row in the R9 table, when
the matching-version CLI invokes each mutation through the gateway, then the
response bytes equal the canonical JSON rendering of that row's exact success
shape, including each required JSON null.

AC74. Given any successful fixture from AC73, when the client repeats the same
authorized request after related current state changes, then the replay bytes
equal the first response bytes and the stored `canonicalResponse` bytes.

AC75. Given a Topline with memberships, Concerns, current tag associations
inserted out of ID order, and events, when its owner calls
`topline <id> --history`, then the envelope and nested objects have exactly the
R7 fields, membership and Concern arrays use their specified orders,
`membershipIds` uses UTF-8 ID order, history uses `seq ASC`, and
each absent optional singleton is JSON null.

AC76. Given one pending migration placement and one resolved placement, when
the owner calls `topline-placement-list` without `--state`, then only the
pending row appears. When the owner calls it with `--state all`, then both rows
appear in `openedAt ASC, id ASC`; each row has the exact R6 actor and wake
objects, and the pending row has three null resolution fields.

AC77. Given one fixture for each refusal slug in R9, when the matching-version
CLI invokes its Topline operation, then response bytes equal that slug's exact
canonical error object. Given a mismatched CLI, when it sends the request, then
the source-baseline HTTP 426 bytes appear instead.

AC78. Given an active Concern tag association, when its owner invokes
`topline-concern-unlink-work`, then the association disappears and one
`concern_work_untagged` event records the explicit actor, reason, Concern, and
membership without a cause field. Given membership unlink removes tags, when
history is read, then no derived untag event exists.

AC79. Given `topline-update` with `toplineId = "tl_a"`, a title supplied as
`Cafe` plus U+0301, and a reason whose scalar sequence is `line`, U+000A,
U+0022, `quoted`, U+0022, when the handler builds Fingerprint JSON, then it
produces exactly these 112 UTF-8 bytes with no trailing newline:

```json
{"operation":"topline-update","parameters":{"reason":"line\u000a\"quoted\"","title":"Café","toplineId":"tl_a"}}
```

Then the request fingerprint is exactly
`a7731986a4a7032356c78c89b387006891b07da3055ed05f442030addb0902e1`.

AC80. Given any R5 mutation envelope, when a required parameter is absent, is
explicit JSON null, or an undeclared parameter is present, then wire validation
returns `invalid_message` before computing a fingerprint or reading an
idempotency row. Given two otherwise equal requests whose string parameters are
NFC-equivalent, when each fingerprint is computed, then the fingerprint bytes
are equal.

AC81. Given empty event streams for Toplines A and B, when A creation, B
creation, and A rename commit in that order, then A history has sequence 1 and
2 while B history has sequence 1. Given another owner's events inserted between
those commits in a twin database, when A or B history is read, then its sequence
values and response bytes remain unchanged.

AC82. Given existing parents in Topline B, when direct SQL attempts an event in
Topline A that names B's membership or Concern, then a composite foreign key
rejects it. Given the same positive `seq` in
different Toplines, when both rows use valid parents, then both inserts succeed;
given a duplicate `seq` in one Topline, then its composite primary key rejects
the second insert.

AC83. Given a product database connection on which either R1 title function is
absent, when the release initializes Topline schema, then initialization fails
before a Topline handler or boot reconciliation can run. Given an otherwise
valid row and both functions registered, when direct SQL inserts the Canonical
title `Café`, then the title checks pass; when it inserts the decomposed
equivalent, then the canonical-title equality check rejects it.

AC84. Given the new release created an open, unlinked Work Item `wi_reopen`, its
owner resolved its pending placement as `left_unlinked`, and that resolved row
stores `historyCausalSeq = 40`; and given the new release then iceboxed the Work
Item in causal event 41, rollback started the previous gateway, and that gateway
reopened the Work Item in causal event 42 with
`kind = "disposition_transition"`, `jobRef = "wi_reopen"`, and detail values
`workItemId = "wi_reopen"`, `fromState = "iceboxed"`, and
`toState = "open"`; and given every event and placement mutation in this setup
uses the same millisecond clock value, when the new release boots again, then it
uses sequence rather than time and commits exactly one pending `reopened`
obligation for `wi_reopen`, exactly one prompt wake, `causeRef = "wi_reopen"`,
`sourceCausalEventSeq = 42`, opening actor `process:tightbeam`, and
`historyCausalSeq >= 42`. It creates no migration obligation and no membership.
When the gateway restarts on that committed database, then it creates no second
obligation or prompt for causal event 42.

AC85. Given the new release opened pending obligations `tlp_closed`,
`tlp_failed`, and `tlp_iceboxed` with pending prompt wakes and Placement causal
watermark 40; and given rollback started the previous gateway, which recorded
matching `disposition_transition` events 41, 42, and 43 with the respective
Work Item IDs in `jobRef` and `detail.workItemId`, `fromState = "open"`, and
`toState` values `"closed"`, `"failed"`, and `"iceboxed"`; when the new release
boots again, then its terminal phase runs before wake recovery and resolves
each existing obligation as `work_terminal` under `process:tightbeam`. Their
respective `resolutionCausalEventSeq` values are 41, 42, and 43. Their
respective resolution reasons are `reupgrade_terminal_reconciliation_closed`,
`reupgrade_terminal_reconciliation_failed`, and
`reupgrade_terminal_reconciliation_iceboxed`. Each obligation stores
`historyCausalSeq = 43`. For each obligation, its resolution and the original
wake's pending-to-canceled transition commit in one transaction,
`canceledAt = resolvedAt`, and `promptWakeId` retains that wake's ID. No new
obligation, wake, prompt, membership, or Work Item state change occurs. The
failed Work Item retains its old-gateway failure reason.

AC86. Given a pending Placement obligation whose prompt wake already fired at
time 50, and given the previous gateway later closed its Work Item in matching
causal event 51 during rollback, when the new release performs terminal
reconciliation, then the obligation resolves as `work_terminal` under
`process:tightbeam` with `resolutionCausalEventSeq = 51` and reason
`reupgrade_terminal_reconciliation_closed`. The wake row retains its exact
`fired` state, `firedAt`, prompt, and identifiers, the delivered turn remains,
and no replacement prompt exists. Given the same terminal candidate with an
already canceled wake, when reconciliation runs, then every wake field remains
unchanged and no replacement prompt exists.

AC87. Given a Qualifying rollback-era terminal disposition and a pending wake,
when a forced crash occurs before the terminal-reconciliation transaction
commits, then the obligation and wake retain their prior values. When restart
retries, then it commits one process-attributed `work_terminal` resolution and
one pending-to-canceled wake transition. Given a forced crash after that commit
but before scheduler recovery or handler exposure, when restart runs, then the
committed resolution and cancellation remain byte-identical and no second row,
wake mutation, or prompt occurs.

### Dual-line delivery and review gates

AC88. Given Mike's authorized Target lines and no owner-recorded Exact target
revision, when an implementation lane evaluates its start gate, then it records
`exact_target_revision_missing`, changes no product byte, and does not infer a
revision from `main`, `0.1.9`, a local worktree, or prior implementation
evidence. Given an Exact target revision but no accepted immediately preceding
lane candidate for Lane 2, Lane 3, or Lane 4, when that lane evaluates its start
gate, then it records `lane_1_contract_missing`, `lane_2_contract_missing`, or
`lane_3_contract_missing` respectively and changes no product byte.

AC89. Given an owner-recorded Exact target revision for each line, when Lane 1
compares the revision with the Completed core definition, then it records each
operation and focused test as present or records `completed_core_missing` and
stops. It does not implement a missing core operation under this authority.

AC90. Given clean `0.1.9` and `0.2.0` worktrees at their separate Exact target
revisions and green baseline gates, when Lane 1 completes, then both lines pass
the full Lane 1 acceptance map with identical database-constraint outcomes,
JSON, authorization, privacy, replay, restart, and rollback-fixture results.
Each line has a separate
commit-bound Lane 1 evidence bundle and every line-specific delta appears in
both bundles.

AC91. Given the two accepted Lane 1 contracts, when Lane 2 completes, then the
real CLI parser and router on both lines pass the closed command and refusal
matrix. `toplines` and `topline` expose intent, `execution-map` and
`execution-map-select` preserve telemetry, an incompatible CLI receives the
source-baseline HTTP 426 bytes before authentication or lookup, and no retired
verb or unknown alias dispatches. Each line has a separate commit-bound Lane 2
evidence bundle.

AC92. Given the two accepted Lane 1 transaction APIs, when Lane 3 completes,
then each qualifying lifecycle edge, wake transition, crash point, restart,
rollback-era reopen, and rollback-era terminal disposition passes the Lane 3
map on both lines with identical Placement, causal, wake, prompt, privacy, and
refusal results. Each line has a separate commit-bound Lane 3 evidence bundle.

AC93. Given an accepted Lane 3 candidate whose first-parent history contains the
accepted Lane 1 and Lane 2 commits, plus one verified Previous-package fixture
for each Target line, when Lane 4 commits only its owned package or smoke paths
and runs the packaged smoke, then the `0.1.9` and `0.2.0` scenarios each pass
AC64 from real matching packages, produce no leaked process or port, preserve
the same canonical Toplines state and prompt evidence, and create separate
commit-bound Lane 4 evidence bundles. No command publishes, installs into a
live prefix, deploys, or contacts a live Gateway.

AC94. Given the work-item evidence graph, when a verifier orders completion
facts, then it finds exactly four Implementation lanes. Lane 1 precedes Lane 2,
Lane 2 precedes Lane 3, Lane 3 precedes Lane 4, and Lane 4 precedes the Final
full-scope review. It finds no fifth implementation lane and no acceptance case
parked outside a lane or the final review.

AC95. Given both Lane 4 completions and all eight Lane evidence bundles, when
the product owner opens the Final full-scope review, then the assignment names
this file's exact reviewed SHA-256, both exact Lane 4 candidate commits,
both package hashes, and every evidence artifact. The reviewer belongs to a
different session and authored no candidate commit.

AC96. Given the final review assignment, when the reviewer evaluates the work,
then the reviewer reads and maps all G1 through G12, NG1 through NG18, A1
through A18, I1 through I87, R1 through R14, and AC1 through AC100 against both
exact candidates. The reviewer re-runs every committed lane test suite and both
packaged smokes.
The reviewer returns one reviewed-clean dual-line report or one blocking report
that names all observed findings; a one-line or one-lane verdict cannot pass.

AC97. Given a reviewed-clean Final full-scope review, when any actor checks this
work item's authority, then no merge, release, package publication, deployment,
deployed-service restart, live migration, or live database mutation is
authorized. Such an action requires a separate owner instruction outside this
specification.

AC98. Given the exact co-reviewed specs candidate containing
`rest-state-api-v1.md`, when the final reviewer inspects both product candidate
diffs, then `Tightbeam.Toplines.query_public/2` and
`Tightbeam.Toplines.public_item/1` satisfy the canonical REST projection while
no `/api/toplines` route, REST cursor, pagination, or Firehose adapter changed
under these lanes. The only superseded REST text is the temporary CLI-name
retention rule named in I77.

AC99. Given any Lane evidence bundle, when an independent reader resolves its
claims without the producer's worktree, then every target input, candidate,
changed path, command, result, fixture, and allowed delta resolves from a full
commit, artifact ID, or SHA-256. A version mismatch yields
`target_version_mismatch`; an absent or mismatched rollback fixture yields
`previous_fixture_unverified`; neither case starts a product process.

AC100. Given an exact specification-review candidate commit, when a reviewer
resolves its canonical set, then the set contains exactly
`standalone-toplines-v5.md` and `v0.2-program-2026-08-12.md`. The standalone
file is the canonical Toplines product specification. The program-file row
deletion is the paired homing change that removes Toplines from every v0.2
program phase and hierarchy. The two-file set, not either file alone, carries
the specification-only transition. The program file supplies no Toplines
product requirement, Target-line revision, implementation custody, or release
authority. The separate canonical REST contract `rest-state-api-v1.md` is
co-amended at that same exact candidate without joining the Toplines canonical
set. The review evidence records the exact commit and SHA-256 values for both
amended canonical contracts, plus the unchanged paired program-file SHA-256.
A path resolved at another commit or an authority claim outside these scopes
fails this case.

### Traceability

| Requirement group | Acceptance cases |
| --- | --- |
| G1-G4, I1-I17, I51-I52, I54-I55, R1-R4 | AC8-AC22, AC50-AC51, AC54, AC58-AC61, AC65, AC67, AC70, AC81-AC83 |
| G5, I35-I40, I56-I66, R6 | AC34-AC42, AC55-AC57, AC62, AC84-AC87 |
| G6-G7, I29-I34, R7-R9 | AC1-AC7 |
| G8, I41-I43, R11 | AC43-AC45 |
| I18-I23, R10 | AC23-AC27 |
| I24-I28, I53, R5, R12 | AC28-AC33, AC52-AC53, AC63, AC79-AC80, AC87 |
| I44-I45, R13-R14 | AC46-AC49, AC56, AC84-AC87 |
| I46-I47, R1-R4, R6 | AC65-AC72 |
| I48-I49, R4, R6-R7, R9 | AC73-AC78 |
| I50, R8 | AC64 |
| G9, I67-I70, I74, I83-I86 | AC88-AC93, AC99 |
| G10, I71-I75 | AC90-AC94 |
| G11, I70, I85 | AC89-AC90 |
| G12, I78-I82 | AC95-AC97, AC99 |
| NG12-NG18, I76-I77, I81, I87 | AC46, AC97-AC100 |

## Open Questions

None. This specification marks no blocking or non-blocking hole.
