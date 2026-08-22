# Completion rails decisions

Status: review-ready decisions spec for
`wi_a7fd5022-1926-4e9b-ad11-14590bff7907`. This spec supersedes the design
choices in `completion-policy-named-rails.md`; that file remains evidence only.
This spec authorizes no implementation, deployment, runtime mutation, identity
change, or 0.1-line change.

Revision note: the amendment after review verdict
`att_6a11fb3a-3a89-4310-b892-e5ababb338d6` adds the frozen legacy-selector
mapping and the companion-authority contract. It does not change the attachment,
repair, subtree, vocabulary, or deletion decisions.

Authority and evidence:

- Mike opened `asg_507b144d-dc35-4f9a-b150-0e36c0027090` to produce this
  decisions spec in the canonical `tightbeam-specs` repository.
- Mike's rail direction is recorded in
  `att_1ae1a7ad-7e46-4475-90a5-c97e1a52803a`: archetypes and cards attach
  named rails; an archetype with no deliverable rail has none; the substrate
  executes the selected law and does not infer a deliverable kind.
- `att_483f9eff-ec19-4b2f-8888-0e2cf0189ed7` proves that
  `asg_29bb92dc-b7a2-4df4-9be8-3d85dbcca541` fulfilled its spawn-and-brief
  outcome. `att_a261517d-0c68-4aa1-8f0e-659741e8672b` proves completion was
  then refused only because `effectKind=code` selected a review gate for work
  with no reviewable product bytes.
- `art_4f0936f4` at SHA-256
  `6e69554ff2ebe762f4e0100e7949c2b8b837feaaf950f64b6dfdcebfa787eaa9`
  is superseded noncanonical input. Its candidate later landed at commit
  `a5c2bfd4af2fea98daa7e1038415bf1ffb1bb2a7` after its lane had been
  withdrawn. The artifact, commit, and `completion-policy-named-rails.md` do not
  carry authority and are not revised by this spec.

## Goal

Define one deterministic completion-policy model in which installed, named
completion rails compose at archetype, assignment-card, and parent-bound
`spawnedBy`-subtree scope.

The model must make these outcomes possible without substrate judgment:

1. A reviewer archetype guarantees that its linked verdict row, nonblank
   rationale, and durable delivery receipt reach its `spawnedBy` parent before
   the review card completes.
2. A parent can require installed completion rails for assignment cards held by
   sessions in that parent's `spawnedBy` subtree, and cannot affect a foreign
   subtree.
3. An authorized principal can repair the completion rails of an open card
   without rewriting its history or fabricating evidence.
4. An unsatisfied rail returns or escalates a named result. The substrate selects
   policy only from the committed rail identities.

## Non-Goals

- This spec does not add an archetype or assignment `outputKind`.
- This spec does not let a card contain a predicate, script, verdict kind, or
  executable law definition.
- This spec does not let a parent weaken archetype defaults across a subtree.
- This spec does not attach subtree policy through role bindings, work-item
  ancestry, assignment openers, current coordination parents, prompt text, or
  inferred organization topology.
- This spec does not change constitutional checks or globally selected statutes.
- This spec does not define hot reload for identity law.
- This spec does not judge the quality of a verdict rationale.
- This spec does not repair or rewrite terminal cards.
- This spec does not implement, deploy, publish identity, mutate runtime state,
  or change the 0.1 line.

## Terms

- **Completion rail:** An installed dispatch-tier rule marked as attachable to
  assignment completion. It reads declared substrate facts and produces one of
  the existing deterministic outcomes: silent pass, named denial, named remedy,
  or named escalation.
- **Rail identity:** The immutable tuple `(name, version, definitionSha256)`.
  Human and wire input uses `name@version`; the substrate resolves and snapshots
  the installed hash before accepting the attachment.
- **Rail base name:** The `name` portion of a rail identity, without its version
  or hash.
- **Archetype default:** An installed completion rail declared by the holder's
  served archetype revision. Its attachment mode is `omittable` or `required`.
  A named omission can suppress only an `omittable` default.
- **Card requirement:** A named rail that an authorized card opener adds for one
  assignment.
- **Named omission:** A card record that suppresses one exact archetype-default
  or legacy-migration rail for one assignment. It does not suppress a subtree
  binding.
- **Subtree binding:** An additive rail requirement rooted at one session. It
  applies to cards held by sessions whose immutable `sessions.spawnedBy` chain
  reaches that root. The root session itself is outside its subtree.
- **Binding waiver:** A one-card exception to one subtree binding, authorized by
  that binding's principal or by the owning user or administrator. A waiver is
  distinct from a named omission.
- **Parent delivery receipt:** A durable notification row addressed to the exact
  immutable `spawnedBy` parent and causally linked to one verdict. The verdict
  row and notification row commit atomically. The receipt proves durable
  delivery to the parent's inbox; it does not assert that the parent took a turn.
- **Source entry:** The durable record of why an exact rail identity participates
  in a card: archetype default, card requirement, legacy migration, subtree
  binding, named omission, or binding waiver.
- **Effective rail set:** The exact rail identities selected for one open card at
  its current rail revision.
- **Rail catalog:** The installed, validated completion-attachable rail
  definitions in one served identity revision.
- **Mint:** Add a new immutable rail name or a new version to an org-owned
  identity source.
- **Install:** Publish and load a minted rail through the existing identity
  release path so it is present in the rail catalog.
- **Repair:** Append a new rail revision to an open assignment through the one
  assignment-scoped amendment verb defined here.
- **Replay corpus:** The finite cross-product of stored legacy selectors,
  holder-archetype classes, and completion-fact presence, plus the exhaustive
  input-normalization rows defined in the `effectKind` cutover. Its ledger
  records or references the matching legacy decision, migrated decision, and
  first non-pass for every case.
- **Authority preflight:** The fail-closed check that resolves this spec through
  its work-item content pin and verifies every companion path, revision, and
  SHA-256 before implementation begins.

## Assumptions

1. The companion files pinned under `Spec homing and authority` remain the
   dispatch-tier rule engine, fact boundary, remedy/escalation mechanism, and
   identity-governance authority for this design.
2. The served identity path can publish versioned, reviewed rule definitions
   separately from a Tightbeam substrate release. The serving process may still
   require its existing restart or identity-apply procedure to load them.
3. Session rows persist after retirement, so an immutable `spawnedBy` chain can
   be resolved for a held assignment.
4. Assignment creation and append-only assignment amendment can commit their
   policy rows in the same database transaction as their idempotency result.
5. The frozen legacy selectors listed under `effectKind` cutover can be
   represented as the three named rails in that section over row-visible facts
   before `effectKind` is removed.
6. A verdict row can identify its review assignment, reviewed assignment,
   verdict kind, authoring principal, and nonblank rationale. A durable delivery
   row can identify its target session and causal verdict.

## Invariants

### I1 — One engine; no interpretation

The existing dispatch-tier rules engine is the only completion-rail executor.
The substrate selects exact installed identities from rows. It does not read a
card subject, prompt, file, artifact content, role prose, or `effectKind` to
choose a rail.

### I2 — Policy sources are durable and explicit

Each open assignment has a committed rail revision, including an explicit empty
effective set. Each revision records the source entries, exact identities,
reason, cause, principal, holder archetype revision, and binding revisions used
to compute it. Absence does not imply policy.

### I3 — Composition is additive except for authorized, source-specific relief

For a card revision, let `D` be archetype defaults, `M` be legacy-migration
rails, `C` be card requirements, `O` be named omissions, `B` be subtree
bindings, and `W` be binding waivers. The effective set is:

```text
((D union M) minus O) union C union (B minus W)
```

`O` can name only an omittable member of `D union M`. A `required` archetype
default cannot enter `O`. `W` can name only a binding ID and exact rail identity
in `B`. A card entry cannot silently cancel another source.

### I4 — Conflicts refuse; no layer guesses a winner

Two sources may name the same exact rail identity; the effective set contains it
once and preserves both sources. If two unsuppressed sources name different
versions or hashes of one rail base name, the substrate refuses the assignment
open, amendment, binding, or waiver that introduced the conflict. It names the
base name and each conflicting source. Nearest ancestor, latest timestamp, list
order, and lexical order are not precedence rules.

### I5 — Subtree bindings are floors

A parent binding can add installed rails only. A named omission cannot suppress
it. Only the binding principal, the owning user, or an administrator can append
a one-card binding waiver. An unwaived binding continues to apply after the
binding session retires because `spawnedBy` is immutable history.

### I6 — A parent cannot govern a foreign subtree

The binding transaction proves that the caller is the root session, the owning
user, or an administrator. A session principal can bind only at its own session
root. The substrate derives affected sessions from immutable `spawnedBy` rows.
The API accepts no arbitrary descendant list and no foreign root.

### I7 — Binding changes have no mixed window

A binding add, version replacement, or revocation appends one binding event and
new revisions for each affected open assignment in one serialized transaction.
Assignment open in the same serialization domain observes either the prior
binding revision or the new one. A crash commits neither the binding event nor
any card revision, or commits the complete set.

### I8 — Card repair is append-only and open-only

The assignment repair verb uses expected revision and idempotency. It appends
one new rail revision or writes nothing. It cannot change assignment subject,
`effectKind` history, holder, opener, work item, review link, evidence,
attestations, state, or prior rail revisions. The original card opener, the
owning user, or an administrator may repair card requirements and omittable
defaults. Binding waivers retain the narrower authorization in I5.

### I9 — Rail failures are named

A satisfied rail is silent. An unsatisfied rail returns its exact `name@version`,
outcome, row-visible reason, and remedy or escalation target. The attempt leaves
the normal durable denial or escalation evidence with cause and principal. A
child that cannot produce the required fact uses that named result in its
blocker or escalation; no path converts the failure to success or drops it.

### I10 — Judgment remains with a mind

A rail may require the existence, linkage, kind, author, nonblank rationale, and
delivery of a verdict. It cannot decide whether the rationale is correct or
good. The reviewer decides the verdict and rationale; the substrate verifies
that the declared rows exist.

### I11 — Rail law is identity data

An agent, archetype author, card opener, or parent can attach only a rail already
in the catalog. A card or subtree row cannot mint law. Any agent may propose a
rail on an identity staging branch. Under the current identity-governance rule,
only Flynn's merge to identity main mints or adopts it; changing that principal
requires an explicit identity-governance amendment. The serving process installs
only a merged identity revision. No substrate release is required when the rail
uses the existing closed fact, verb, check, outcome, and remedy vocabulary. A new
substrate fact, verb, outcome, or executor capability requires a substrate spec
and release.

### I12 — `effectKind` is deleted, not translated at runtime

`effectKind` does not survive as completion-policy sugar. The 0.2 migration uses
it once to preserve each open card's prior completion behavior as explicit
legacy-migration source entries. After cutover, assignment create, dispatch,
read, rule facts, and completion selection contain no live `effectKind` field or
branch. Historical events retain their original payloads.

### I13 — Reviewer completion reaches its parent

The reviewer archetype defaults to
`completion/verdict-delivered-to-parent@1` in `required` mode. Assignment open
refuses this rail with `completion_rail_parent_unavailable` when the holder has no
immutable `spawnedBy` parent. The rail passes only when the reviewer principal
has filed exactly one linked `reviewed-clean` or `changes-requested` verdict with
a nonblank rationale and the same transaction has committed its parent delivery
receipt. A named omission cannot suppress this rail. The rail does not require a
review of the reviewer.

### I14 — Exact versions remain executable

The substrate snapshots `name`, `version`, and `definitionSha256`. A serving
catalog that lacks an attached exact identity fails closed and names restoration
or an authorized open-card amendment as the remedy. Installation cannot replace
bytes under an existing identity.

## Architecture

### Spec homing and authority

The canonical home of this spec is
`clickety-clacks/tightbeam-specs/completion-rails-decisions.md`. Its
implementation authority is the exact byte sequence for which
`wi_a7fd5022-1926-4e9b-ad11-14590bff7907.specRefName` equals
`completion-rails-decisions.md` and whose SHA-256 equals that work item's
`specRefSha256`. A repository branch, local checkout, artifact copy, or unbound
commit is not implementation authority. The work-item pin remains empty until a
reviewed-clean revision exists. Implementation-card opening and implementation
are blocked while either pin field is absent, the name differs, or the resolved
bytes do not match the hash.

The following companions are frozen at canonical `tightbeam-specs` commit
`f27f05ae52c027a00e244aa7f5dc5a1bede9031c`:

| Canonical path | SHA-256 | Governing clauses |
|---|---|---|
| `statute-engine-v1.md` | `20bb78619f85f1e4c783b0328b8970149673140316c3e12b777672427a0469cb` | `Invariants (the acceptance lens)`, `Rule files`, `Fact vocabulary`, `Operators & typing`, `Evaluation`, and `Validation` |
| `check-tier-v1.md` | `b07d1357f00a0bbedaa34a17e310bf051c0b18d898d2e3c58b7d9ca30f53409e` | `Ruled decisions`, `Verbs`, `Statute facts`, `Response shapes`, and `Invariants (acceptance lens)` |
| `rails-mechanism-v1.md` | `434a4aaf18f3d31534f81b70eb19a009eba5159b1dbcf34b33c8f966a86b7900` | `Invariants (the acceptance lens)`, `A. Script guards`, `B. Hybrid dispatch`, `C. Remedies`, `E. Legibility`, and `F. Rail-set satisfiability` |
| `tightbeam-decisions.md` | `5f7a63b8bf726feb1817176969dd75e7a81467f99bbea25a3886dc70d629a459` | `Agency-preserving supervision`, `Org learning: codifying emergent structure`, and `Rails: hard law`, including the `propose` staging seam, Flynn merge authority, one engine, and structured-fact boundary |

An implementation preflight fetches that exact canonical commit, hashes each
companion byte-for-byte, and verifies the work-item pin for this spec. A missing
path, unavailable revision, hash mismatch, absent work-item pin, or companion
whose declared grammar cannot express a required rail returns
`completion_rails_authority_unavailable` and writes no implementation card,
migration row, rail definition, or runtime state. The remedy is a canonical spec
amendment followed by reviewed-clean review and a new work-item content pin.
There is no fallback to repository main, a local latest file, the superseded
candidate, or a compatible-looking rule.

### Pattern: completion rail composition

This pattern applies only to completion-attachable dispatch rules. Constitutional
checks and globally selected statutes remain outside the effective set and
cannot be omitted, waived, or repaired through this mechanism.

The canonical example is a review assignment held by a reviewer session. Its
archetype supplies `completion/verdict-delivered-to-parent@1`. The reviewer
files a verdict on the linked producer. The same mutation causes a durable
parent delivery. The review card can then complete. The substrate checks rows;
it does not evaluate the rationale.

### Named vocabulary

A completion rail name has this form:

```text
completion/<observable-outcome>@<positive-integer-version>
```

`<observable-outcome>` matches `^[a-z0-9][a-z0-9-]*$`. Names describe the fact
that must exist, not a cognitive operation. Version and content hash are
immutable. Any semantic change mints a new version. Aliases, unversioned names,
wildcards, version ranges, and in-place replacement are invalid.

The initial migration and reviewer scenario require these installed identities:

- `completion/independent-reviewed-clean@1`: the linked producer has an
  independent qualifying `reviewed-clean` verdict.
- `completion/verification-recorded@1`: `assignment.verdicts` contains
  `verified`.
- `completion/results-recorded@1`: `assignment.artifact_kinds` contains at
  least one of `report`, `spec`, `doc`, `data`, or `other` recorded by the holder
  on the assignment's work item.
- `completion/verdict-delivered-to-parent@1`: exactly one reviewer-authored
  linked `reviewed-clean` or `changes-requested` verdict, its nonblank rationale,
  and its atomically committed parent delivery receipt exist.

These names designate row contracts. They do not infer which card needs them.

### Minting and installation

Rail definitions live in the org-owned identity source. Any agent may propose a
definition on a staging branch. Flynn's merge to identity main is the current
mint/adoption authority. The serving process installs only that merged revision
through the normal identity publication path. The substrate validates grammar,
closed facts, exact identity, and rail-set satisfiability. It does not judge the
proposal or its review.

Installation uses the existing identity publication and serving path. It does
not require a Tightbeam binary release when the definition stays inside the
existing rule grammar. Runtime card, archetype, and binding operations can only
reference installed identities.

This spec adds no second rail registry and no live inline editor.

### Attachment records and precedence

An archetype manifest contains a unique list of entries shaped as
`{rail = "name@version", mode = "omittable|required"}`. Omission of the
manifest key means an explicit empty list for compatibility. A card open request
can add card requirements and named omissions with one nonblank reason. The
substrate rejects duplicate entries, add/omit overlap, an omission outside the
omittable default or migration basis, an omission of a `required` default, and
any unresolved identity.

A subtree binding names its root session, exact rail identities, nonblank reason,
cause, principal, identity revision, and binding revision. The substrate derives
the descendant set. Multiple ancestors compose by union. A binding waiver names
the binding ID, card, exact rail identity, reason, cause, and authorized
principal.

Each assignment rail revision stores the complete effective set and each source
entry. Reads expose both. A consumer reads the stored revision instead of
reconstructing old policy from a current archetype manifest or binding set.
An archetype default snapshots only when its card opens. A later archetype
revision does not add, remove, or replace defaults on an existing card; an
authorized amendment is required for that card.

### Mutation seams

The catalog changes only through the existing identity publication seam.

Subtree state has one command family:

```text
tightbeam completion-rails-bind --root <sessionKey>
  --require <name@version> [--require <name@version> ...]
  --reason <text> --key <idempotencyKey>

tightbeam completion-rails-bind --root <sessionKey>
  --expected-revision <n>
  [--require <name@version> ...]
  [--remove <name@version> ...]
  --reason <text> --key <idempotencyKey>
```

The first form creates the binding. The second appends a binding revision. An
empty resulting binding closes its effect for later card revisions but retains
its history. Both forms update affected open-card rail revisions atomically as
required by I7, and later assignment opens read the resulting binding revision.

An open card has one repair verb:

```text
tightbeam assignment-completion-rails-amend <assignmentId>
  --expected-revision <n>
  [--require <name@version> ...]
  [--omit <name@version> ...]
  [--restore <name@version> ...]
  [--waive-binding <bindingId>:<name@version> ...]
  [--restore-binding <bindingId>:<name@version> ...]
  --reason <text> --key <idempotencyKey>
```

`require`, `omit`, and `restore` edit the card's requirement and omission
entries. `waive-binding` and `restore-binding` edit binding-specific waivers and
apply the authorization in I5. The command rejects a no-op, an empty reason, a
stale expected revision, a terminal card, and a conflicting rail base name. A
successful command wakes the holder once with old and new exact sets, reason,
cause, and principal. The original card opener, owning user, or administrator
may use `require`, `omit`, or `restore`; the card holder alone gains no repair
authority.

This is the repair for `asg_29bb92dc-b7a2-4df4-9be8-3d85dbcca541` after
migration: omit `completion/independent-reviewed-clean@1` from its
legacy-migration basis and cite the fulfillment and refusal attests. The card's
history remains truthful. The repair creates no artifact, review card, or
synthetic verdict.

### Evaluation and escalation

On explicit completion and the turn-end completion path, the substrate resolves
the same committed assignment rail revision. It evaluates globally selected law
as before, then evaluates effective completion rails in installed deterministic
order. A missing exact definition fails closed.

Each non-pass response and row names the exact rail. A rail whose missing fact has
an installed remedy uses the existing remedy machinery. A rail whose resolution
requires a decision uses the existing escalation machinery. If a child concludes
that it cannot satisfy the named rail, it records the normal blocker against its
open assignment and escalates the exact name to the card opener or binding
principal identified by the source entry. The substrate routes that record; it
does not decide whether the child is capable.

### `effectKind` cutover

The frozen pre-cutover product authority is `clickety-clacks/tightbeam` commit
`b8e6c47e4631da8345aaf8c6ab73b0858e630bf6`. The complete legacy-selector
inventory is:

| Source at the frozen revision | SHA-256 | Legacy authority used by the migration |
|---|---|---|
| `priv/kungfu/agentic-engineering/rules/engineering.toml` | `089c32545f3d64f6399806c0d8d4f5eb4be3e0085d66c19e13b2731eae6883ce` | `completion-requires-review` and its remedy |
| `priv/kungfu/agentic-engineering/rules/verification.toml` | `835cc90cee4ad00d958b6eeb901b9f1dcbacfa2d044ec4a8ada79b74b6226f4c` | `completion-requires-verification`, `completion-requires-results-artifact`, and their remedies |
| `lib/tightbeam/rules.ex` | `5d33e8534562286926a8af3aa97517f3bed34fd0157ab87b0ae8746e7416c20c` | sorted rule-file loading, preserved in-file order, closed facts, and first non-pass evaluation |
| `lib/tightbeam/assignments.ex` | `7181469c65883a2d8b6bedc87d2e37fd3710712d55cbd983141810e3dd5c4261` | accepted values and storage defaulting: a linked review stores `review`; an omitted non-review stores `code` |
| `test/verification_papertrail_test.exs` | `607df181a9fe0c09adb0a70b497d5df229c98e45d1ae60534dcf3f380f9c9fbd` | shipped rule order and the legacy completion-gate contracts |

The migration reads each open assignment's stored value after the legacy
defaulting above. It creates the following exact legacy-migration sources:

| Frozen legacy selector | Exact attached rail | Source mode |
|---|---|---|
| `effectKind` is `code`, `policy`, `release`, or `live_mutation` | `completion/independent-reviewed-clean@1` | `omittable` |
| `effectKind` is `evidence`, `review`, or `coordination` | no review rail | n/a |
| holder archetype is `coder` | `completion/verification-recorded@1` | `omittable` |
| holder archetype is `coder`, `reviewer`, `spec-writer`, or `recon` | `completion/results-recorded@1` | `omittable` |
| any other holder archetype | no verification or results rail | n/a |

The card's migrated set is the union of all matching rows in that table. The
`omittable` mode permits a named, authorized repair while retaining the legacy
source and omission history. The three migrated rail contracts preserve these
legacy predicates and remedies exactly:

| Legacy rule | Migrated rail pass condition | Migrated non-pass remedy |
|---|---|---|
| `completion-requires-review` | `assignment.qualifying_review_verdict_kinds` contains `reviewed-clean` | assign one linked card to role `reviewer`, producing `reviewed-clean`, and surface the denial |
| `completion-requires-verification` | `assignment.verdicts` contains `verified` | wake the exact holder session to file `verified` |
| `completion-requires-results-artifact` | `assignment.artifact_kinds` contains at least one of `report`, `spec`, `doc`, `data`, or `other` | wake the exact holder session to record an artifact on the card's work item |

All three retain the legacy `attest.kind = completion` guard. The attachment
mapping replaces only the legacy selector predicates shown in the first table.
The three migrated rails evaluate in frozen legacy first-denial order:
`completion/independent-reviewed-clean@1`, then
`completion/verification-recorded@1`, then
`completion/results-recorded@1`. Installed global law continues to run before
the attachable set as specified elsewhere; the migration does not reorder it.

Before cutover, the migrator emits a replay ledger for the complete Cartesian
product of:

- each stored `effectKind`: `code`, `policy`, `release`, `live_mutation`,
  `evidence`, `review`, and `coordination`;
- each holder-archetype class: `coder`, `reviewer`, `spec-writer`, `recon`, and
  `other`; and
- both present and absent values for `reviewed-clean`, `verified`, and a holder
  artifact whose kind is one of `report`, `spec`, `doc`, `data`, or `other` on
  the card's work item.

`other` represents every holder-archetype value outside the four named values;
the frozen predicates cannot distinguish members of that class. Each fact bit
represents absence versus a list containing the named accepted value; the frozen
membership predicates cannot distinguish other members within either class.
The cross-product therefore produces exactly `7 * 5 * 2 * 2 * 2 = 280`
exhaustive decision cases.

The ledger also contains 16 exhaustive input-normalization rows:

- eight linked-review requests, one for an omitted requested value and one for
  each of the seven accepted requested values; every row stores `review`;
- one non-review request with an omitted value; it stores `code`; and
- seven non-review requests, one for each accepted explicit value; each stores
  the requested value unchanged.

Each decision row records all inputs, the stored legacy selector, the legacy
selected rules in evaluation order, the migrated exact rail set in evaluation
order, the legacy result, the migrated result, and the first non-pass rule or
rail plus remedy. Each normalization row records its request inputs and stored
selector, then references the matching decision row by its complete key. The
cutover proceeds only when all 280 decision rows and all 16 normalization rows
match on stored selector and, where applicable, pass versus non-pass,
first-denial position, reason fact, and remedy class. A mismatch returns
`completion_rails_migration_replay_mismatch`, names the ledger row, and writes no
cutover or migrated source.

After that replay and the exact serving-catalog check pass, the migration
snapshots each open card's matching rails as exact legacy-migration source
entries. It does not retroactively attach defaults from the newly served
archetype revision to an existing card. In particular, an open legacy review
card does not acquire `completion/verdict-delivered-to-parent@1` during the
decision-equivalence migration. Cards opened after that archetype revision is
served use archetype defaults, card requirements and omissions, and subtree
bindings only.

After the behavior-preserving snapshot and serving-catalog check, the 0.2
contract removes `effectKind` from current assignment storage, assignment input,
and current projections. Immutable historical event payloads retain the value
they originally recorded. An old client that sends `effectKind` receives
`unsupported_assignment_field`. The gateway does not ignore it and does not
translate it into rails. Any non-completion policy that formerly read
`effectKind` must gain an explicit row-visible selector or attachable rail before
deletion; no compatibility alias remains.

### Subtraction ruling

The design adds source rows, subtree bindings, and one repair verb because
deleting completion policy would lose required reviewer and parent guarantees,
while accepting the failure would leave fulfilled cards permanently open. It
deletes `effectKind` because preserving it as sugar would create a second policy
vocabulary whose mapping could drift from the named rails.

### Traceability

| Requirement | Design seam | Acceptance |
|---|---|---|
| Substrate executes law and does not infer | exact installed identities and one rules engine | A1, A9 |
| Archetype, card, and subtree sources compose | I3 formula and source-specific records | A2-A5 |
| Reviewer verdict reaches parent | reviewer default plus verdict/delivery rows | A6 |
| Open cards can be repaired truthfully | append-only amendment verb | A7, A8 |
| Rail law can ship without binary release | identity mint/install boundary | A10 |
| `effectKind` does not remain a second selector | frozen mapping, exhaustive replay, then deletion | A11, A12 |
| Failures are loud and actionable | named denial/remedy/escalation | A13 |
| Implementation reads only reviewed, pinned authority | spec and companion preflight | A17 |

This spec teaches no new agent operating pattern before implementation exists.
When the mechanism ships, served guidance must teach the attachment vocabulary,
the named repair verb, and the rule that an unsatisfied rail is reported or
escalated by exact name.

## Acceptance

### A1 — Empty means no attachable completion rail

Given a holder archetype has no defaults, the card has no requirements, and no
ancestor binding applies, when the opener creates the assignment, then its first
rail revision stores an empty effective set. Constitutional and globally
selected law still runs.

### A2 — A card omission beats an archetype default

Given the holder archetype defaults to
`completion/independent-reviewed-clean@1` in `omittable` mode, when the
authorized opener omits that exact rail with a nonblank reason, then the card
revision preserves the default and omission source entries and excludes the
rail from the effective set.

### A3 — A subtree binding beats an ordinary card omission

Given an ancestor binding requires
`completion/independent-reviewed-clean@1`, when a card request names an ordinary
omission of the same omittable archetype default, then the card revision stores
both sources and the rail remains in the effective set through the binding.
Given the binding principal also supplies a binding waiver, the card is created
without either contribution and preserves both the omission and waiver rows.

### A4 — Multiple ancestors compose without nearest-wins

Given two ancestors bind different exact rails, when a descendant card opens,
then both identities appear once with both binding sources. Given two ancestors
bind different versions of one base name, when the later binding is attempted,
then the gateway returns `completion_rail_identity_conflict`, names both sources,
and appends no binding or card revision.

### A5 — Foreign scope is refused

Given session `P` is not on session `C`'s immutable `spawnedBy` chain, when `P`
attempts to bind a rail by naming `C` or a foreign root, then the gateway returns
`completion_rail_binding_forbidden` and writes no binding. The bind API exposes
no descendant-list parameter. Given `P` binds a rail at its own root, a card held
by `P` does not inherit that binding, while cards held by descendants of `P` do.

### A6 — Reviewer completion delivers a reasoned verdict row

Given a review card is held by a reviewer session with `spawnedBy=P`, when the
reviewer tries to complete before filing its linked verdict, then
`completion/verdict-delivered-to-parent@1` denies by exact name. Given the
reviewer files exactly one linked `reviewed-clean` or `changes-requested` verdict
with a nonblank rationale and the same transaction commits the delivery receipt
to `P`, when the reviewer retries completion, then the rail is silent and no
review-of-review assignment exists. A card request that tries to omit this
required archetype default is refused and writes no assignment.

### A7 — The jammed coordination card is repaired without fiction

Given migration attaches `completion/independent-reviewed-clean@1` to
`asg_29bb92dc-b7a2-4df4-9be8-3d85dbcca541`, when its authorized opener runs the
repair verb with the current revision, a new key, a reason citing
`att_483f9eff-ec19-4b2f-8888-0e2cf0189ed7` and
`att_a261517d-0c68-4aa1-8f0e-659741e8672b`, and an omission of that exact rail,
then one new revision commits and the holder receives one notice. No review,
artifact, verdict, child session, or assignment is fabricated.

### A8 — Repair is atomic and idempotent

Given a successful repair, when the caller repeats the same key and fingerprint,
then the gateway returns the stored response and keeps one new revision. Given
the same key with a different reason or delta, the gateway returns
`idempotency_conflict`. Given a stale expected revision, a terminal card, or a
fault before commit, no rail revision or member row commits.

### A9 — `effectKind` cannot select a rail

Given two migrated assignments have identical committed rail sources and
different retained `effectKind` values in their historical event payloads, when
completion is evaluated after cutover, then both select the same exact rail set
and receive the same rail decision. No runtime path reads the historical label.

### A10 — An org installs law without a substrate release

Given a staging proposal adds a new versioned completion rail that
uses only installed facts, verbs, checks, outcomes, and remedies, when the org
receives Flynn's identity-main merge and the serving process loads that revision,
then the rail appears in the catalog without a Tightbeam binary change. Given a
parent or card attempts to name an uninstalled rail or embeds a predicate, then
the gateway refuses it by exact name and writes no policy row.

### A11 — Migration preserves current open-card decisions

Given the frozen legacy sources and the 296-row corpus, when the migration
generates its replay ledger, then all 280 decision rows contain the required
inputs, ordered legacy rules, ordered migrated rails, both results, and both
first non-pass records. All decision rows match on pass versus non-pass,
first-denial position, reason fact, and remedy class. All 16 normalization rows
match their required stored selector and reference the matching decision row.
Given any mismatch, missing case, duplicate case, or changed source hash, the
migration returns the named failure and writes no cutover or migrated source.
Given the ledger matches, each real open card receives only the union specified
by the frozen mapping, not a later archetype default, before the old selector is
removed.

### A12 — `effectKind` is gone after cutover

Given migration and exact-catalog verification succeed, when a new client reads
or creates an assignment, then the current wire projection and accepted input
contain no `effectKind`. When an old client sends the field, the gateway returns
`unsupported_assignment_field` and creates no assignment. A repository check
finds no live completion selector, rule fact, or compatibility mapping from
`effectKind` to rails.

### A13 — A child cannot fail silently

Given an effective rail is unsatisfied, when the child attempts completion, then
the response and durable event name its exact identity, outcome, reason, and
remedy or escalation target. Given the child records that it cannot produce the
fact, when it escalates through the existing work path, then the durable blocker
and routed notice carry the same exact identity and source principal.

### A14 — Binding updates are atomic across open cards

Given a parent has two descendant sessions holding open cards, when the parent
adds a binding, then the binding event and one new revision for each affected
card commit in one transaction. A concurrent assignment open observes the old
complete binding revision or the new complete binding revision. Fault injection
leaves no binding-only or partial-card state.

### A15 — Exact definition drift fails closed

Given an open card stores an attached rail hash that the served catalog no
longer contains, when completion is attempted, then the gateway returns
`completion_rail_version_unavailable`, names the exact identity, and names two
remedies: restore that installed definition or amend the open card to an
installed identity. It does not run newer bytes under the old identity.

### A16 — A parent-delivery rail requires a parent

Given a root session has `spawnedBy=NULL`, when an opener attempts to create a
card whose archetype or card sources include
`completion/verdict-delivered-to-parent@1`, then the gateway returns
`completion_rail_parent_unavailable` and writes no assignment or rail revision.
Given the immutable parent row exists but is inactive, the durable notification
can still be addressed to that exact inbox; this rail does not infer parent
capability or wait for the parent to take a turn.

### A17 — Implementation authority fails closed

Given the work item lacks either spec pin, the pinned spec name or bytes differ,
a companion or frozen product-source path or revision is unavailable, any
declared SHA-256 differs, or the pinned grammar cannot express a required rail,
when implementation preflight runs, then it returns
`completion_rails_authority_unavailable` and writes no implementation card,
migration row, rail definition, or runtime state. Given all pins and hashes
match, the preflight records the resolved spec hash, companion commit and
hashes, and frozen product-source commit and hashes in the implementation
handoff ledger before any build work starts.

## Open Questions

None. This document decides the completion-rail attachment model, precedence,
vocabulary, installation authority, open-card repair seam, subtree scope,
reviewer guarantee, and deletion of `effectKind` for the 0.2 implementation.
