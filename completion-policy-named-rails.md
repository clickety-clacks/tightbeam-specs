> **SUPERSEDED PRE-AUTHORITY (2026-08-22).** This draft landed from a lane that had
> already been superseded when the landing was fulfilled (race disclosed in
> att on asg_507b144d). It is EVIDENCE, not the design of record, and must not be
> adopted or revised as a second design. The authoritative completion-rails
> decisions spec is being produced under `wi_a7fd5022` by
> spec-writer:completion-rails-decisions; that document wins on every point.

# Completion policy — composable named rails

Status: proposed 0.2 design for
`wi_032f11a6-2ab2-41b6-ab04-41b06a35cf18`. This document decides the shape;
it authorizes no implementation, deployment, identity change, or 0.1 modification.

Authority and evidence:

- Mike's design input is
  `att_1ae1a7ad-7e46-4475-90a5-c97e1a52803a`.
- The concrete failure is
  `asg_29bb92dc-b7a2-4df4-9be8-3d85dbcca541`:
  `att_483f9eff-ec19-4b2f-8888-0e2cf0189ed7` proves the requested child owner
  and ownership card existed and were briefed, while
  `att_a261517d-0c68-4aa1-8f0e-659741e8672b` records that completion was refused
  only because the coordination card had defaulted to `effectKind=code`.
- Current-main evidence is Tightbeam `b8e6c47e4631da8345aaf8c6ab73b0858e630bf6`.
  `Assignments` defaults an untyped non-review assignment to `effectKind=code`,
  and `completion-requires-review` selects `code`, `policy`, `release`, and
  `live_mutation` assignments from that field.
- This design composes with `statute-engine-v1.md`, `check-tier-v1.md`, and
  `rails-mechanism-v1.md`. Those remain the one dispatch-tier rules engine.

## Decision

Completion requirements are a set of named, installed rails attached to an
assignment. An archetype supplies the default set. An assignment may add or
remove named rails with a recorded reason. The substrate snapshots the resulting
set and executes those rails. It never infers a deliverable type from the subject,
`effectKind`, files, role prose, or produced bytes.

Do not add `outputKind` to archetypes, sessions, or assignments.

Keep `effectKind` as descriptive assignment metadata for observability and rules
that genuinely concern the effect. It must not select output-specific completion
policy. This design does not change the `effectKind` vocabulary or its legacy
default.

The card-level seam attaches existing installed rails. A card never embeds a
predicate, script, verdict kind, or free-form law. New law still enters through
the reviewed identity rules tree and the existing load and satisfiability gates.

## Why this shape

`effectKind` answers a broad question about expected effect. It does not prove
that a specific assignment has a reviewable deliverable. Treating the enum as a
completion contract made a fulfilled spawn-and-brief card mechanically
unfinishable. The available workarounds were all false: fabricate an artifact,
open a synthetic review, or ask an administrator to repair metadata after work.

An `outputKind` property moves the same guess to an archetype. It still forces one
label to predict every card held by a mixed archetype, and it makes the substrate
translate that label into policy. Named rail attachment states the policy itself:
which executable checks apply to this assignment.

Archetype defaults keep the common path automatic. A coder can inherit review,
verification, and results-record rails without an opener remembering three
flags. An archetype with no common deliverable can default to an empty set. A
mixed or exceptional card carries an explicit delta and reason. Repeated deltas
are evidence that the archetype is too broad and should be split; they are not a
reason to add inference to the substrate.

The evaluated alternatives are:

| shape | decision | reason |
|---|---|---|
| `effectKind` selects completion policy | reject | It describes expected effect, not the card's evidence contract; `asg_29bb92dc` is the false-denial specimen. |
| Archetype declares one typed `outputKind` | reject | It moves the guess to a coarser level and still makes substrate code translate a type into policy. |
| Each card carries free-form predicates or scripts | reject | It bypasses reviewed law, invites opener-authored policy, and creates a second rules surface. |
| Archetype defaults plus reasoned card deltas over installed named rails | choose | The ordinary path is automatic, exceptions are explicit, and the existing rules engine remains the only executor. |

## Invariants

### C1 — One rules engine

Completion rails are ordinary installed dispatch-tier rules. The design adds an
attachment selector to the current rules engine; it does not add a second policy
interpreter, inline card scripts, or a completion framework in `Assignments`.

### C2 — Attachment is explicit row data

Every open assignment has one current completion-rail-set revision, including an
explicit empty set. The revision records the archetype default, card delta,
reason, principal, cause, time, archetype manifest identity, and exact rail
identities. Absence never means “probably no rails.”

### C3 — Archetype default, card delta

An archetype manifest declares `completion_rails`, an ordered list of installed
completion-attachable rail identities. Omitted means `[]` for compatibility.

An assignment normally inherits that list. The opener may provide disjoint
`add` and `remove` lists. Any nonempty delta requires one nonblank reason. The
final set is:

```text
(archetype completion_rails - remove) union add
```

Rail set membership is unordered. Installed rule order remains the deterministic
first-denial order. At open, every removal must exist in the snapshotted
archetype default and every addition must be absent from it. At amendment, every
removal must exist in the current set and every addition must be absent from it.
The substrate refuses no-op deltas instead of normalizing them away.

### C4 — The substrate does not judge the work

The substrate resolves the holder's archetype, validates rail names, computes the
set, writes it, and evaluates it. It does not read the assignment subject, inspect
an artifact, decide whether a task “really produced code,” or choose a rail from
`effectKind`.

### C5 — Only installed, attachable rails may be named

A rule is attachable at completion only when its installed declaration marks it
`attachment = "assignment-completion"`. Assignment open and amendment refuse an
unknown name, an unavailable revision, or a rule without that marker. The rule
still declares its normal verb, facts, outcome, remedy, and text under the current
rules grammar.

This marker does not make the rule global. On an `attest completion` call, an
attachable rule participates only when its exact identity is in the assignment's
current rail set. Non-attachable statutes retain their current global selection
and cannot be removed by a card.

### C6 — Exact version, no semantic drift

A completion rail identity is `(name, version, definitionSha256)`. Names and
versions are immutable. A semantic change mints a new version. The assignment
snapshot stores all three fields.

The loaded catalog must contain the exact stored identity before evaluation. A
missing or changed definition fails closed with
`completion_rail_version_unavailable` and names two remedies: restore the exact
installed rail or amend the open assignment to a current rail set with a reason.
The substrate never silently runs newer law against an older card.

### C7 — Rails remain mechanical

Every attached rail reads row-visible facts or a declared contained check. It is
silent when satisfied. A denial names the rail and the remedy. A judgment is a
verdict-producing remedy, never substrate inference. Existing cause, principal,
legibility, containment, idempotency, and satisfiability rules remain binding.

### C8 — Empty means no output-specific gate, not no law

An empty completion rail set disables only attachable output-specific rails.
Assignment existence, holder authorization, lifecycle, state, idempotency,
constitutional checks, and every non-attachable statute still apply. A card
cannot remove those protections.

### C9 — Review does not require review-of-review

The producer's independent-review rail may create a linked review assignment.
That remedy declares the review card's rail delta. The resulting review card may
require a linked verdict or results record, but its set must not contain the
producer's independent-review rail.

Rail-set satisfiability extends its existing producer-cycle check across remedy
assignment attachments. Loading refuses a completion rail whose remedy would
produce a card that reattaches the same requirement in a cycle.

### C10 — Corrections are append-only and visible

An assignment's opener or an administrator may amend the rail set while the
assignment is open. Amendment requires an expected revision, idempotency key,
nonempty reason, and explicit add/remove delta. It appends a revision; it never
rewrites or deletes the prior set.

Each amendment snapshots the unchanged open-time archetype-default basis, the
complete new member set, and the exact delta from the preceding revision. A
later archetype-manifest edit never retroactively changes that basis.

An amendment wakes the holder with the old set, new set, reason, and principal.
It does not delete verdicts, artifacts, remedy episodes, review cards, or other
work created under the earlier set. Those rows remain true and require their own
authorized disposition.

### C11 — Open is atomic

Assignment creation, rail-set resolution, the header revision, and every member
row commit in the same transaction. A crash leaves either no assignment or one
assignment with a complete set. Wire-idempotent replay returns the stored set.
The same key with a different delta or reason returns the existing idempotency
conflict and creates nothing.

### C12 — Turn-end uses the same set

The turn-end sweep's synthesized completion call resolves the exact same current
rail-set revision as a holder's explicit completion attempt. There is no second
defaulting path and no separate archetype test in supervision.

## Installed declaration shape

The current rule declaration gains two fields for attachable rules:

```toml
[[rule]]
name = "completion-requires-review"
version = 1
attachment = "assignment-completion"
verb = "attest"
edges = ["verb", "turn-end"]
text = "completion needs an independent reviewed-clean verdict"
effect = "remedy"
deny_when = [
  { fact = "attest.kind", op = "eq", value = "completion" },
  { fact = "assignment.qualifying_review_verdict_kinds", op = "not_in", value = ["reviewed-clean"] },
]

[rule.remedy]
action = "assign"
produces = "reviewed-clean"
target_role = "reviewer"
completion_rails_add = ["review-card-requires-linked-verdict@1"]
completion_rails_remove = ["completion-requires-review@1"]
completion_rails_reason = "this card reviews the producer and must not require review of itself"
```

The exact TOML nesting follows the existing `[[rule]]`, `[rule.remedy]`, and
`[rule.remedy.params]` grammar. The example shows the semantic additions; an
implementation must not create a parallel root table.

For this rule, remove the current
`assignment.effect_kind in [code, policy, release, live_mutation]` condition.
Attachment membership becomes its selector.

## Archetype declaration shape

`archetypes/<name>.toml` gains one optional top-level key:

```toml
name = "coder"
completion_rails = [
  "completion-requires-verification@1",
  "completion-requires-results-artifact@1",
  "completion-requires-review@1",
]
```

The manifest loader validates the list as unique nonblank versioned rail names.
After archetypes and rules load, one cross-catalog validation proves every
default points to an installed completion-attachable rail with the exact version.
The stored archetype projection includes the default list and manifest SHA.

The substrate contains no archetype-name switch. The shipped identity bundle,
not substrate code, decides which defaults belong to `coder`, `reviewer`,
`spec-writer`, `recon`, `product-owner`, `orchestrator`, or any future archetype.

## Durable rows

Two additive tables carry the contract.

```sql
CREATE TABLE assignment_completion_rail_revisions (
  assignmentId          TEXT NOT NULL REFERENCES assignments(id),
  revision              INTEGER NOT NULL,
  source                TEXT NOT NULL CHECK(source IN ('open','amend','migration')),
  archetype              TEXT NOT NULL,
  archetypeManifestSha   TEXT NOT NULL,
  archetypeDefaultsJson  TEXT NOT NULL,
  addedRailsJson         TEXT NOT NULL,
  removedRailsJson       TEXT NOT NULL,
  reason                 TEXT NULL,
  causedBy               TEXT NOT NULL,
  principal              TEXT NOT NULL,
  createdAt              INTEGER NOT NULL,
  PRIMARY KEY (assignmentId, revision),
  CHECK(
    (addedRailsJson = '[]' AND removedRailsJson = '[]')
    OR reason IS NOT NULL
  )
);

CREATE TABLE assignment_completion_rail_members (
  assignmentId          TEXT NOT NULL,
  revision              INTEGER NOT NULL,
  railName              TEXT NOT NULL,
  railVersion           INTEGER NOT NULL,
  definitionSha256      TEXT NOT NULL,
  attachmentSource      TEXT NOT NULL CHECK(attachmentSource IN ('archetype','card','migration')),
  PRIMARY KEY (assignmentId, revision, railName, railVersion),
  FOREIGN KEY (assignmentId, revision)
    REFERENCES assignment_completion_rail_revisions(assignmentId, revision)
);
```

`archetypeDefaultsJson`, `addedRailsJson`, and `removedRailsJson` are canonical
JSON arrays of exact `name@version` identities. The first preserves the
open-time basis. The latter two preserve the delta for this revision, so an
absent member never erases the fact that a card removed an archetype default or
that an amendment changed the preceding set. `principal` is the substrate's
serialized user, session, process, or remedy principal. `causedBy` is the
assignment-open dispatch ID for open, the amendment command ID for amend, and
the migration receipt for migration. Exact schema spelling may follow repository
conventions, but it must preserve these facts and checks.

The current revision is the maximum committed revision. No mutable current-set
column is required.

## Fact and evaluation seam

The closed fact vocabulary gains:

| fact | type | meaning |
|---|---|---|
| `assignment.completion_rails` | list(string) | Exact `name@version` members of the current revision; present `[]` for an existing assignment with an empty set; nil for unknown assignment. |
| `assignment.completion_rail_revision` | int | Current revision; nil for unknown assignment. |

The first fact exists for legibility and non-attachable policy that needs to
observe the contract. Attached-rail selection itself uses the same cached
`$assignment` dependency and stored members directly; a rule need not repeat its
own name in `deny_when`.

Evaluation order on `attest completion` is:

1. Resolve `$assignment` once.
2. Evaluate non-attachable statutes in installed order, unchanged.
3. Select installed completion-attachable rules whose exact identities are in
   the current set.
4. Evaluate selected rules in installed order through the existing decision
   fold.
5. Continue to the unchanged constitutional handler only if every rule allows.

Unknown assignment remains the handler's `unknown_assignment` refusal because no
attachable rule is selected from a nil assignment. A failed rail-set read is a
rules fact failure and denies closed as `rule_error`.

## Assignment API

`assign` and `dispatch` gain optional card deltas:

```text
--completion-rails-add '["rail-a@1","rail-b@2"]'
--completion-rails-remove '["rail-c@1"]'
--completion-rails-reason "this card produces a spec rather than coordination"
```

Omitting all three means inherit. Add/remove must be unique and disjoint. A
reason without a delta is refused. A delta without a reason is refused. Removing
a rail not present in the archetype default is refused; adding a rail already in
the default is refused. This makes the stored delta honest instead of silently
normalizing opener mistakes.

A new assignment-scoped verb amends an open card:

```text
tightbeam assignment-rails-amend <assignmentId>
  --expected-revision <n>
  [--add '["rail@version"]']
  [--remove '["rail@version"]']
  --reason "..."
  --key <idempotencyKey>
```

Only the original opener or an administrator may amend. The verb changes no
`effectKind`, subject, holder, work item, review link, or assignment state.

Assignment reads and mutation responses expose:

```json
{
  "completionRailRevision": 1,
  "completionRails": [
    {"name":"completion-requires-review","version":1,"definitionSha256":"..."}
  ],
  "completionRailBasis": {
    "archetype":"coder",
    "archetypeManifestSha":"...",
    "added":[],
    "removed":[],
    "reason":null,
    "principal":"session:agent:coder:example"
  }
}
```

The wire change is additive. Older clients may omit deltas and inherit. A client
that sends the new fields to an older gateway receives the normal exact-version
refusal; it must not believe the override applied.

## Migration and initial bundle policy

Migration is additive and preserves current open-card behavior before any policy
improvement. For every existing open assignment, write revision 1 with
`source='migration'` and attach the currently applicable output-specific rails:

- attach `completion-requires-review@1` when the current rule would select the
  assignment by `effectKind`;
- attach `completion-requires-verification@1` when the current rule would select
  the holder archetype;
- attach `completion-requires-results-artifact@1` when the current rule would
  select the holder archetype.

This backfill changes no existing completion result. It only makes the current
implicit selection explicit. The migration receipt records counts by final rail
set and the identity revision that supplied each definition. A migration
revision snapshots `archetypeDefaultsJson=[]`, records the complete backfilled
set as its added delta, uses no removals, and carries the nonblank reason
`0.1 behavior-preserving backfill`. Its member rows use
`attachmentSource='migration'`. This makes replay equality and provenance as
strict as an ordinary open or amendment.

Cutover must leave no mixed-selection window. Drain assignment-open mutations,
append the final behavior-preserving revision for every open assignment, load one
identity revision containing both the attachable rules and matching archetype
defaults, verify every open assignment resolves exact definitions, and only then
resume assignment opens. If the deployment cannot provide that barrier, it must
run a bridge that dual-writes the legacy-selected set until every gateway serves
the attachment selector. It must not remove the old selector while a gateway can
still open a card under the old implicit policy.

After migration, the shipped archetype manifests provide defaults for new work.
The policy bundle should place a rail in an archetype default only when the rail
applies to that archetype's ordinary cards. Mixed archetypes use the common
denominator and explicit card deltas. The substrate does not hardcode the
initial matrix.

The `asg_29bb92dc` card is then repaired through the ordinary amendment verb:
remove `completion-requires-review@1` with a reason naming spawn coordination and
the fulfillment receipt. Its `effectKind=code` remains as historical truth. No
synthetic artifact or review is created.

Tightbeam 0.1.8 remains frozen. This design lands on current `main` only.

## Failure contracts

Every refusal is named and writes the normal denial evidence:

| code | condition | remedy |
|---|---|---|
| `unknown_completion_rail` | Add/default names no installed attachable rail. | Install the reviewed rail or choose an installed name. |
| `invalid_completion_rail_delta` | Add/remove are malformed, duplicate, overlap, or contradict the archetype default. | Correct the exact named list. |
| `completion_rail_reason_required` | A card changes its default without a reason. | State why this card differs. |
| `completion_rail_version_unavailable` | The assignment's stored definition is not loaded byte-for-byte. | Restore it or amend to a current version. |
| `completion_rail_revision_conflict` | Amendment expected revision is stale. | Read the current set and decide again. |
| `completion_rail_amend_forbidden` | Caller is neither opener nor administrator. | Ask the opener or administrator. |
| `assignment_not_open` | Amendment targets a terminal assignment. | Do not rewrite terminal history. |

An attached rail's own denial keeps its installed rule name and text. This table
does not replace rail-specific remedies.

## Acceptance

### Shape and validation

1. Archetype manifest omission produces an explicit empty default.
2. Unknown, duplicate, unversioned, or non-attachable rail defaults fail load by
   file and archetype name.
3. A valid card delta snapshots exact names, versions, hashes, source, reason,
   cause, principal, and open-time archetype default in the assignment-open
   transaction.
4. Empty inherited and empty overridden sets remain distinguishable by their
   revision basis.
5. A card cannot define a predicate, script, verdict kind, or inline rail.

### Policy behavior

6. A product-owner spawn-coordination assignment with `effectKind=code` and an
   empty rail set completes after its universal checks. It creates no review or
   artifact requirement. This fixture cites `asg_29bb92dc`, `att_483f9eff`, and
   `att_a261517d`.
7. An assignment with `effectKind=evidence` and an attached independent-review
   rail is denied until its qualifying reviewed-clean fact exists. This proves
   `effectKind` is not the selector in either direction.
8. A coder inheriting review, verification, and results-artifact rails remains
   denied until each row-visible requirement is satisfied.
9. A linked review card produced by the review remedy can file its verdict and
   complete without review-of-review. Its own declared rails still run.
10. An empty output-specific set cannot bypass holder, lifecycle, state,
    authorization, idempotency, or non-attachable statutes.
11. The explicit completion verb and turn-end sweep select the same set and
    return the same first denial.

### Amendment and recovery

12. Authorized amendment appends one revision, wakes the holder once, and leaves
    all prior evidence and remedy children intact.
13. Lost-response replay with the same key returns the same revision. A different
    payload with that key, including a different reason, conflicts and appends
    nothing.
14. Concurrent amendments from one expected revision produce exactly one new
    revision and one named revision conflict.
15. Crash before commit leaves no partial revision or member rows. Crash after
    commit is recovered by idempotent replay.
16. Definition removal or in-place drift fails closed by exact rail identity.

### Compatibility and migration

17. Backfill reproduces the pre-migration decision for every open assignment
    under the three current output-specific completion rails.
18. `effectKind`, existing assignment projections, review links, verdicts,
    artifacts, and terminal history remain byte-for-byte unchanged except for
    additive completion-rail fields.
19. Old clients inherit archetype defaults. New-client deltas cannot be silently
    ignored by an old gateway.
20. Removing the old `effectKind` selector from
    `completion-requires-review` occurs only after every open assignment has an
    explicit migrated set and the new selection path is live.

## Implementation sequence

This sequence is descriptive, not implementation authority:

1. Extend installed rule and archetype validation; add cross-catalog checks.
2. Add durable revision/member tables and transactional assignment-open snapshot.
3. Add the cached facts and attachable-rule selection to the existing rules fold.
4. Add wire/CLI projection and card delta input.
5. Add authorized append-only amendment and holder notice.
6. Backfill open assignments and prove outcome equivalence.
7. At one drained or dual-write cutover, convert the three current
   output-specific rules and ship matching archetype defaults.
8. Remove the `effectKind` selector only after the migration and exact-definition
   gates pass on every open assignment and every serving gateway.
9. Prove the `asg_29bb92dc` repair and the review-without-review-of-review fixture.

## Non-goals

- No archetype `outputKind` field.
- No inference from assignment prose, file lists, artifacts, or effect labels.
- No inline or user-authored executable law on a card.
- No change to `effectKind` vocabulary, default, or unrelated consumers.
- No generic workflow engine or hardcoded archetype policy in substrate code.
- No weakening of constitutional checks or non-attachable statutes.
- No automatic deletion or closure of review, remedy, or evidence rows after a
  rail amendment.
- No implementation, deployment, identity apply/relearn, or 0.1 change under
  this design assignment.

## Guidance impact

Do not change served guidance for this design alone. Guidance must teach only the
mechanism that current main actually serves. When implementation ships, its CLI
help and operating-manual change must say: inherit the archetype completion
rails by default; when a card differs, add or remove installed named rails and
record one reason. The implementation must not teach `outputKind` or ask agents
to infer policy from `effectKind`.
