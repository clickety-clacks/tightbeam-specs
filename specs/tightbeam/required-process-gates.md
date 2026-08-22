# Declarative required-process gates

Status: draft specification pending the required cold digest for
`wi_f165cdbd-72c0-4add-bb8d-2113908c3e55`. This specification authorizes no
implementation, identity publication, deployment, runtime mutation, or release
operation.

Authority and evidence:

- Mike ruled in `dr_e2a6657c-a7c8-457d-a7c9-fc88ea53a151` that this MVP uses
  organization, Topline, and work-item scopes. It does not add project or
  release entities.
- The Topline scope means the explicit V5 human-intent model from
  `wi_35abce19-8d05-4a18-90db-335cabe0893c`. It does not mean the legacy
  `toplines` telemetry, creator-turn parentage, causal trees, or an automatic
  rollup.
- The reviewed Toplines V5 specification is `art_e275210f` at SHA-256
  `d39dd61cb44f5c6ff0bbc301b28d64a893b294d1a894e148b1449b36d5585bf9`.
  Core integration is recorded against that specification. Runtime proof
  remains **NOT-PROVEN** under
  `att_a76de51c-0fb3-47a6-9ce0-8313d8be4cc6`.
- The current source census uses Tightbeam `origin/main`
  `b8e6c47e4631da8345aaf8c6ab73b0858e630bf6`. It contains `org_settings`,
  V5 Topline and explicit membership rows, work-item close, dispatch-tier
  rules and facts, remedy episodes, artifacts, attests, and supervision. It
  contains no project entity, release entity, or general work-readiness
  transition.
- `completion-rails-decisions.md` remains the authority for assignment-card
  completion rail composition. This specification does not duplicate or
  supersede it.

## Goal

Let an organization opt into named process requirements for successful
work-item and V5 Topline completion. Let a narrower scope refine inherited
requirements without embedding policy in substrate rows.

Let a work item or V5 Topline bind to one optional, neutral delivery target.
When that exact object has a target binding, require a matching durable landed
receipt before its successful completion. Keep target meaning and landing proof
inside the Kung Fu that defines the target.

Use the existing rules, facts, remedies, and prodding machinery. The substrate
must select installed law from explicit rows, verify row-visible evidence, and
record results. A user or authorized agent decides which process or target
applies.

This design adds scope bindings and landed receipts because deleting the
surface would lose the requested opt-in safety, while accepting silent missing
proof would defeat the opt-in contract.

## Non-Goals

- This specification does not add project, release, branch, tag, build, cut,
  environment, repository, or deployment entities.
- This specification does not define release management or target meaning.
- This specification does not infer a Topline from work-item ancestry, creator
  turns, prompts, titles, causal trees, or legacy Execution Map telemetry.
- This specification does not make Topline membership imply a delivery target.
- This specification does not make a Topline target apply to its member work
  items.
- This specification does not make a work-item target apply to a Topline.
- This specification does not define or replace the V5 Topline lifecycle.
- This specification does not auto-spawn, auto-assign, reassign, reopen, close,
  fail, icebox, deploy, merge, or publish.
- This specification does not run external checks during a completion
  transaction. External work must leave durable evidence first.
- This specification does not alter assignment-card completion rail
  composition from `completion-rails-decisions.md`.
- This specification does not invalidate a historical completion after its
  transaction commits.
- This specification does not ship a required process, organization default,
  delivery target, or target binding by default.

## Terms

- **V5 Topline:** A durable human intent in the V5 `toplines` table. Its work
  membership comes only from an active, attributable row in
  `topline_work_memberships`.
- **Execution Map:** The legacy read-only work telemetry. It is not a policy
  scope in this specification.
- **Completion transition:** `work-item-close` for a work item, or the V5
  `topline-close` transition for a Topline. Work-item fail and icebox are not
  completion transitions.
- **Process name:** A stable, Kung Fu-qualified name such as
  `agentic-engineering:independent-review`. A scope mutation names this stable
  name. The substrate resolves it to an installed immutable definition.
- **Process identity:** The tuple `(name, version, definitionSha256)`. A scope
  revision stores the exact tuple that it resolved.
- **Process definition:** An installed Kung Fu declaration that maps one
  process identity to existing dispatch-tier rule identities for one or both
  completion transitions. It declares the exact fact-contract identities that
  those rules consume.
- **Required-process rail:** An installed dispatch-tier rule marked
  `attachment = "required-process"`. It stays outside global rule selection and
  participates only when an effective process definition selects it.
- **Rule identity:** The tuple `(ruleName, definitionSha256)` computed from one
  installed rule definition.
- **Fact-contract identity:** The immutable tuple `(factName, version, type,
  semanticsSha256)`. A semantic or shape change creates a new version.
- **Local requirement:** A process that one scope explicitly requires.
- **Local clear:** A stable process name that one scope removes from its
  inherited set. A clear does not delete an earlier row or an installed process.
- **Scope revision:** An append-only snapshot of one scope's local requirements
  and clears, with exact process identities, reason, cause, principal, and
  idempotency receipt.
- **Effective process set:** The exact process identities that apply to one
  completion attempt after organization, active Topline membership, and
  work-item scope composition.
- **Delivery target:** An installed, versioned Kung Fu declaration. The
  substrate treats its name and evidence contract as opaque data.
- **Target binding:** One append-only revision that binds one work item or one
  V5 Topline to zero or one exact delivery-target identity.
- **Declared baseline:** The opaque, nonblank baseline string in a landed
  receipt. The defining Kung Fu decides whether it denotes a commit, branch,
  tag, build, design revision, domain state, or another value.
- **Landed receipt:** An append-only row that states that one exact target
  binding landed at one declared baseline. It names the evidence rows, the
  admission rule result, cause, principal, and time.
- **Responsible agent:** The deterministic existing session that receives a
  remedy notice for one failed gate, as defined in Architecture.

## Assumptions

1. The existing dispatch-tier rules engine can evaluate installed rules against
   a closed fact vocabulary and return a named denial, remedy, or escalation.
2. Existing remedy episodes can deduplicate one live remedy per rule and
   subject.
3. Existing wake and supervision paths can notify an existing session without
   creating or reassigning work.
4. Work-item close already checks owner or administrator authority and refuses
   while an assignment remains open.
5. V5 Topline rows and active membership rows preserve owner scope and actor
   attribution.
6. The V5 implementation supplies its reviewed `topline-close` lifecycle seam.
   If it does not, the Topline subset of this MVP remains blocked rather than
   adding another Topline lifecycle here.
7. Kung Fu publication can install process and target declarations beside its
   installed rule declarations.
8. A target's Kung Fu can express receipt admission with installed rules over
   durable facts. A target that needs a new fact requires a separate substrate
   specification and release.
9. The final MVP can depend on the reviewed V5 contract before V5 runtime proof
   exists. Deployment cannot claim this dependency until runtime proof resolves
   `att_a76de51c`.

## Invariants

### I1 — Scope is explicit and neutral

Only an organization scope revision, a V5 Topline scope revision, or a
work-item scope revision can select a required process. The substrate does not
derive scope from a title, prompt, creator turn, causal edge, assignment tree,
or Execution Map projection.

### I2 — V5 membership is the only Topline-to-work path

Work-item composition reads active `topline_work_memberships` rows. One work
item can inherit from several V5 Toplines. Ended memberships do not contribute.
Legacy `toplines`, `topline --under`, creator-turn parentage, and causal trees do
not contribute.

### I3 — Installed Kung Fu owns process meaning

A process definition names installed required-process rail identities and exact
fact contracts. Scope rows contain process identities, not predicates, scripts,
verdict kinds, evidence interpretations, or remedy programs. The existing rules
engine remains the only executor.

### I4 — Composition is deterministic

Let `O` be the organization requirement set. For each active Topline `T`, let
`T+` be its local requirements and `T-` its local clears:

```text
effective(T) = (O union T+) minus every identity whose stable name is in T-
```

For work item `W`, let `M(W)` be its active V5 Topline memberships. Its
inherited set is:

```text
inherited(W) = O                              when M(W) is empty
inherited(W) = union effective(T), T in M(W) otherwise
```

Let `W+` be the work item's local requirements and `W-` its local clears:

```text
effective(W) = (inherited(W) union W+)
               minus every identity whose stable name is in W-
```

A Topline clear suppresses an organization requirement on that Topline path.
It does not suppress another Topline's explicit requirement. A work-item clear
suppresses that stable name from the merged work-item set. The organization
scope has no clear list because it inherits from no policy scope.

### I5 — Conflicting identities fail closed

Two sources can contribute the same process identity; the effective set stores
it once and preserves both sources. If unsuppressed sources contribute different
versions or hashes for one stable name, the completion attempt returns
`required_process_identity_conflict`. The substrate does not choose by scope,
time, list order, or lexical order. An authorized work-item clear or scope
migration is the remedy.

### I6 — Policy history is append-only

One mutation seam replaces one scope's complete local requirement and clear
snapshot. It requires the expected revision, a nonblank reason, and an
idempotency key. It appends a revision or writes nothing. It cannot change a
Topline membership, object state, assignment, attest, artifact, target binding,
receipt, or prior revision.

Each scope revision records its exact process identities, stable clears,
reason, cause, checked principal, owner scope, and creation time. A later Kung
Fu edit does not rewrite that evidence.

### I7 — Unknown or unavailable law refuses

A scope mutation refuses an unknown process name before it writes. A completion
attempt refuses when the installed catalog lacks the stored process identity,
rule identity, or fact-contract identity. The response names the missing
identity and two remedies: restore that exact installed contract, or append an
authorized scope revision that resolves to an installed contract.

### I8 — Completion check and state change are one transaction

The gateway evaluates the effective process set from one database snapshot.
It evaluates selected rules and commits the successful close in the same
serialized transaction. A membership, scope, target, receipt, or object-state
change cannot occur between the check and the close.

An unmet rule commits its durable denial and remedy-episode evidence before the
gateway returns the denial. The target state does not change.

### I9 — A failure names cause, principal, and repair

A failed gate names the process identity, selected rule identity, target kind,
target id, effective-set revision hash, row-visible reason, and supported
remedy. The durable denial records the checked principal and the command cause.
A satisfied gate is silent.

### I10 — Existing custody receives the remedy

The substrate selects one responsible agent without interpreting work content:

1. If the caller session holds an open assignment on the work item, or on an
   active member work item of the Topline, select that session.
2. Otherwise, if the target scope has exactly one distinct open assignment
   holder, select that holder.
3. Otherwise, select the target owner's personal Main session.

For a Topline, the target scope contains assignments on its active member work
items. For a work item, it contains assignments on that item. The remedy uses
the existing wake, supervision, and recurrence mechanisms. It does not spawn,
assign, reassign, or change object state.

### I11 — Opt-out is silent

When the organization has no requirements, the object has no local scope
revision, and the object has no target binding, a completion follows its
existing path. Required-process code writes no denial, remedy episode, wake,
receipt, or policy event. It does not add a latency-bearing external check.

### I12 — Target binding has exact scope

A work item and a V5 Topline can each have zero or one active target binding.
A Topline target gates only `topline-close`. It does not gate a member work
item. A work-item target gates only `work-item-close`. It does not gate a
Topline. Organization scope does not carry a target binding in this MVP.

### I13 — Target meaning stays in Kung Fu

A target definition declares its immutable identity, its receipt-admission
rules, and its exact fact contracts. Tightbeam stores and compares the identity,
baseline, evidence references, and rule result. It does not parse a repository,
branch, tag, build, environment, deployment, design, or domain value.

### I14 — A binding requires a matching landed receipt

Target-binding presence selects the neutral installed required-process rail
`delivery-target-landed` for that object's close. The rail passes only when
an admitted landed receipt names the active binding revision, exact target
identity, and one nonblank declared baseline. A receipt for an earlier binding,
another object, another target version, or another baseline does not satisfy
the rail.

Clearing a target binding removes this rail from later completion attempts. The
clear and older receipts remain visible history.

### I15 — Landing evidence is admitted before completion

`delivery-landed-record` runs the active target definition's installed
admission rules against durable evidence references. The command writes the
receipt and its idempotency result in one transaction only after those rules
pass. A completion transaction reads the receipt; it does not contact an
external system.

### I16 — Completion truth does not decay

A successful close records the effective process-set hash, target-binding
revision if present, landed-receipt id if present, and declared baseline in its
completion event. Later branch, design, build, target, process, or fact-contract
drift does not change that historical result.

When later drift creates new work, an authorized agent uses the existing linked
reopen or follow-up work path. The substrate does not reopen an object from a
poll, target change, catalog change, or membership change.

### I17 — Honest failure remains reachable

Required processes and target landing gate successful close only. They do not
gate `work-item-fail` or `work-item-icebox`. An authorized principal can append
a reasoned process clear or target clear before a Topline close when the intent
should end without the selected process or target.

### I18 — Contract evolution is explicit

A rule predicate, fact type, fact meaning, target evidence contract, or process
meaning change creates a new immutable version and hash. A deployment keeps an
old referenced contract installed, or migrates each affected open scope through
the ordinary append-only policy seam before removing it. Missing compatibility
evidence fails closed. The migration uses no special process-specific substrate
logic.

### I19 — V5 dependency cannot fall back

Topline-scope policy, Topline target binding, and Topline close gating call the
V5 intent API only. If the V5 capability is unavailable, these operations return
`topline_v5_unavailable` and write no policy or target row. They do not consult
Execution Map telemetry or legacy `toplines` behavior.

The MVP is not runtime-proven until the V5 runtime proof resolves
`att_a76de51c`. A staged build can expose organization and work-item policy
first, but it must keep each Topline-specific verb fail-closed until V5 is
proven and enabled.

## Architecture

### Pattern: named process selection over existing rails

Kung Fu projects process declarations to `identity/processes/*.toml`. Each
declaration contains a stable qualified name, positive version, applicable
completion verbs, installed required-process rail identities, and fact-contract
identities. The loader computes the declaration and rule hashes; a declaration
cannot assert its own hash. The process loader validates the full catalog at
boot. It rejects a duplicate name/version, an unsupported fact contract, a rule
that lacks `attachment = "required-process"`, a rule that targets another verb,
or a dependency cycle. Globally selected statutes stay outside this attachment
class, and a scope clear cannot suppress them.

The binding layer selects process identities. The rules engine evaluates them.
The binding layer does not implement a workflow or interpret evidence.

### Scope rows and mutation seam

Add one append-only revision family:

```text
required_process_scope_revisions
  scopeKind              organization | topline | work_item
  scopeRef               organization | tl_... | wi_...
  revision               positive integer
  requiredJson           canonical array of exact process identities
  clearedNamesJson       canonical array of stable process names
  catalogRevisionSha256  exact served process-catalog revision
  reason                 nonblank text
  cause                  durable mutation receipt id
  principalKind          user | session
  principalRef           checked user or session id
  ownerUserId            checked owner scope
  createdAt              epoch milliseconds
```

The primary key is `(scopeKind, scopeRef, revision)`. The mutation creates its
durable receipt in the same transaction; that receipt id is the revision's
cause. The current revision is the greatest committed revision. Organization current-state discovery uses the
existing `org_settings` key `required-process-policy-revision`, which stores the
current organization revision number. The scope revision and this setting
change in one transaction. Topline and work-item current revisions need no
mutable pointer.

The one mutation verb is:

```text
tightbeam required-processes-set
  (--organization | --topline <tl_id> | --work-item <wi_id>)
  --expected-revision <n>
  --require '["qualified:name", ...]'
  --clear '["qualified:name", ...]'
  --reason <text>
  --key <idempotencyKey>
```

Revision `0` means that no prior scope revision exists. `--require` and
`--clear` are complete local snapshots, not incremental patches. Empty arrays
restore inheritance. Organization calls require an empty clear array. Lists use
stable-name lexical order in stored canonical JSON. The gateway rejects
duplicates and require/clear overlap.

Only an administrator can mutate organization scope. The Topline or work-item
owner, a session owned by that user, or an administrator can mutate the object
scope. Authorization and exact-id resolution occur inside the write
transaction. Unknown and invisible objects return the same bytes.

### Effective-set projection

Work-item and V5 Topline reads add a `requiredProcesses` object:

```json
{
  "effective": [
    {"name":"agentic-engineering:independent-review","version":1,
     "definitionSha256":"...","sources":["organization","tl_...","wi_..."]}
  ],
  "localRevision": 2,
  "localRequired": [],
  "localCleared": [],
  "effectiveSha256": "..."
}
```

The projection sorts by stable name, version, and hash. It derives sources from
the current rows and active V5 memberships. It does not persist a copied
effective set on the work item.

### Delivery-target rows and mutation seams

Kung Fu projects target declarations to `identity/delivery-targets/*.toml`.
Each target declaration contains a stable qualified name, positive version,
content hash, receipt-admission rule identities, and fact-contract identities.

Add append-only `delivery_target_binding_revisions` and
`delivery_landed_receipts` tables. A binding revision stores target kind, target
id, revision, nullable exact target identity, reason, cause, principal, owner,
and time. A null identity is an explicit clear. A receipt stores its own id,
binding revision, exact target identity, declared baseline, canonical typed
evidence-row references, admission decision id, cause, principal, owner, and
time.

The binding mutation is:

```text
tightbeam delivery-target-set
  (--topline <tl_id> | --work-item <wi_id>)
  --expected-revision <n>
  (--target <qualified-name> | --clear)
  --reason <text>
  --key <idempotencyKey>
```

The receipt mutation is:

```text
tightbeam delivery-landed-record
  (--topline <tl_id> | --work-item <wi_id>)
  --binding-revision <n>
  --baseline <opaque-nonblank-text>
  --evidence '<canonical-array-of-typed-row-references>'
  --key <idempotencyKey>
```

The receipt command accepts only typed references supported by the existing
row-reference resolver. The target's admission rules decide which references
and facts are required. The substrate validates existence, visibility, exact
binding identity, and the installed rule result.

Reads expose `deliveryTarget: null` when unbound. A bound projection exposes
the exact identity, binding revision, binding principal and reason, latest
matching receipt id, and declared baseline. It does not expose domain-specific
interpretation.

### Completion and remedy seam

`work-item-close` and V5 `topline-close` call one transaction-scoped selector
before the state mutation. The selector returns the effective process
identities plus `delivery-target-landed` when that exact object has an
active target binding. It then calls the existing rules decision fold in
installed deterministic order.

On allow, the handler commits the close and its completion evidence. On denial,
the handler commits the denial and uses `RailRemedy` with subject
`<target-kind>:<target-id>:<effective-sha256>:<rule-identity>`. Repeated denials
can leave separate attempt events, but one live remedy subject produces one
notice. When the required fact appears, the next evaluation closes the remedy
episode through the existing close path.

### Idempotency, crash, and replay

Policy, target, and receipt mutations use the existing wire-idempotency
fingerprint pattern. The fingerprint covers the operation, scope, expected
revision, complete request body, checked owner, and resolved exact catalog
identities.

- The same key and fingerprint returns the stored response and writes nothing.
- The same key with another fingerprint returns `idempotency_conflict`.
- A stale expected revision returns `revision_conflict` and writes nothing.
- A crash before commit leaves no revision, receipt, event, or idempotency row.
- A crash after commit returns the committed result on replay.
- A completion retry re-reads current rows. It cannot reuse an in-memory pass.

### Compatibility and rollout

The new mutation verbs and response members are additive to the current wire
surface. Existing work-item verbs keep their spelling and existing fields.
Current clients can ignore the added projections. A client that sends a new
verb to an older gateway receives its ordinary unknown-verb or exact-version
refusal; it cannot believe a binding applied.

Execution Map responses remain unchanged. They do not expose, inherit, or
evaluate required-process or delivery-target state.

Schema migration adds tables and registers the V5 Topline module before the new
Topline policy modules. It creates no policy revision, target binding, receipt,
denial, remedy, or wake. The organization setting remains absent until an
administrator opts in.

Before rollout removes an old rule or fact contract, a compatibility gate must
prove that no open scope or target binding references it. Otherwise the release
fails closed and names the referencing rows. The V5 runtime smoke is a release
prerequisite for enabling Topline-specific verbs.

### Proposed implementation paths

This path census is a build boundary, not implementation authority:

- Add `lib/tightbeam/required_processes.ex` for catalog validation, scope
  revisions, composition, projections, and transaction-scoped selection.
- Add `lib/tightbeam/delivery_targets.ex` for target catalog validation,
  binding revisions, receipt admission, and the neutral landed fact.
- Register both schemas after V5 Toplines in `lib/tightbeam/schema.ex`.
- Add transaction-scoped selected-rule evaluation and fact-contract identities
  in `lib/tightbeam/rules.ex`. Reuse `lib/tightbeam/rail_remedy.ex`,
  `lib/tightbeam/supervision.ex`, and existing wake delivery.
- Add the work-item close interlock and completion evidence to
  `lib/tightbeam/work_items.ex`.
- Add the V5 Topline close interlock and projections to
  `lib/tightbeam/toplines.ex` only after the reviewed V5 close seam exists. Do
  not define a replacement lifecycle and do not call its Execution Map
  compatibility delegates.
- Add handlers in `lib/tightbeam/gateway.ex`, wire declarations in
  `lib/tightbeam/wire/router.ex` and `lib/tightbeam/wire/payloads.ex`, and CLI
  parsing plus request encoding in `cli/src/args.rs` and
  `cli/src/dispatch.rs`.
- Add focused proofs in `test/required_processes_test.exs`,
  `test/delivery_targets_test.exs`, `test/work_items_test.exs`,
  `test/toplines_test.exs`, `test/rules_test.exs`, `test/gateway_test.exs`,
  `test/router_test.exs`, `test/payloads_test.exs`, and the CLI suites.
- Add Kung Fu declarations under `priv/kungfu/<bundle>/processes/*.toml` and
  `priv/kungfu/<bundle>/delivery-targets/*.toml` only when a reviewed product
  lane defines actual process or target meaning.

This specification teaches no agent operating pattern before the mechanism
exists. Guidance lands with the implementation only after the named verbs and
failure contracts pass their acceptance cases.

## Acceptance

### A1 — No opt-in preserves existing completion

Given no organization revision, no local revision, and no target binding, when
an authorized principal closes an otherwise closable work item, then the
existing close response and state transition succeed. The feature writes no
policy, denial, remedy, wake, target, or receipt row.

### A2 — Organization requirements reach ungrouped work

Given the organization requires installed process `P` and work item `W` has no
active V5 membership or local override, when `W` closes without `P`'s required
evidence, then the gateway denies by exact process and rule identity. Given the
evidence exists, the same close succeeds and records the effective-set hash.

### A3 — Topline inheritance uses explicit membership

Given Topline `T` requires `P` and `W` has one active membership in `T`, when
`W` closes, then `P` participates. Given the membership ends before the close,
then `P` does not participate unless another source requires it. A causal-tree
edge with the same identifiers changes neither result.

### A4 — Many-to-many merge and work-item clear are deterministic

Given `W` belongs to `T1` and `T2`, `T1` requires `P`, and `T2` requires `Q`,
when `W` reads its policy, then its effective set contains `P` and `Q` with
their source ids. Given `W` stores a local clear for `P`, then only `Q` remains.
Neither Topline policy row changes.

### A5 — A Topline clear affects one inheritance path

Given organization scope requires `P`, `T1` clears `P`, `T2` inherits `P`, and
`W` belongs to both Toplines, when `W` resolves policy, then `P` remains through
`T2`. Given `W` belongs only to `T1`, then `P` is absent.

### A6 — Conflicting versions refuse without guessing

Given two active sources contribute different identities for stable process
name `P`, when the object attempts completion, then the gateway returns
`required_process_identity_conflict`, names both sources, writes the denial,
and keeps the object open. It does not select a winner.

### A7 — Scope mutation is authorized, atomic, and replay-safe

Given scope revision `3`, when an authorized caller submits a complete local
snapshot with expected revision `3`, then revision `4`, its cause/principal
event, and its idempotency result commit together. A same-key replay returns
revision `4`. A changed fingerprint, stale revision, invisible id, or injected
fault writes no partial revision.

### A8 — Unknown and removed definitions fail closed

Given a caller names an uninstalled process, when it sets policy, then the
gateway returns `unknown_required_process` and writes nothing. Given an open
scope references an exact identity that the served catalog lacks, when the
object closes, then `required_process_version_unavailable` names restoration
and scope-migration remedies.

### A9 — Completion and policy changes serialize

Given one transaction changes an active membership or scope revision while
another closes the object, when both complete, then the close observes the
complete state before or after that change. It cannot commit from a mixed
effective set. Fault injection cannot leave a closed object without its
completion evidence.

### A10 — Remedy targets existing custody once

Given a session caller holds an open assignment in the target scope, when a
process gate denies, then one live remedy episode targets that session. Given no
caller-held assignment and exactly one distinct holder, the episode targets
that holder. Given ambiguous or empty holder custody, it targets the owner's
personal Main. Repeated denial for the same subject produces no spawn,
assignment, reassignment, or duplicate live notice.

### A11 — Work-item target does not roll up

Given work item `W` has a target binding and its Topline `T` has none, when `W`
closes without a matching receipt, then `delivery-target-landed` denies.
When `T` closes, `W`'s binding does not participate.

### A12 — Topline target does not roll down

Given Topline `T` has a target binding and member work item `W` has none, when
`T` closes without a matching receipt, then `delivery-target-landed`
denies. When `W` closes, `T`'s binding does not participate.

### A13 — Receipt admission stays domain-owned

Given a target definition requires evidence facts `E`, when an authorized
caller records a receipt without `E`, then the target's installed admission
rule denies and no receipt commits. Given `E` exists and the active binding,
target identity, baseline, and references match, then one receipt and its
admission decision commit.

### A14 — Stale receipt cannot satisfy a new binding

Given binding revision `1` has a landed receipt and revision `2` changes or
clears the target, when the object closes, then the revision `1` receipt does
not satisfy revision `2`. Rebinding the prior target creates a later revision
and requires a receipt for that revision.

### A15 — Historical completion remains true

Given an object closes against target binding `4`, baseline `B`, and receipt
`R`, when its branch, design, build, target catalog, or process catalog changes,
then the close event still reports binding `4`, `B`, and `R`. No automatic
reopen occurs. A later need uses a linked reopen or follow-up work item.

### A16 — Failure and icebox remain reachable

Given a target-bound work item lacks a landed receipt, when its owner fails or
iceboxes it through an otherwise valid transition, then that transition does
not evaluate the landing rail. Its normal failure or icebox history remains
truthful.

### A17 — Contract evolution requires compatibility evidence

Given a process uses fact contract `F@1`, when a release removes or changes
`F@1` without migrating each open reference or retaining exact compatibility,
then the catalog or release gate refuses and names the referencing scope rows.
Given migration appends current scope revisions to `F@2`, then later completion
uses only `F@2` and preserves the `F@1` history.

### A18 — V5 absence never becomes legacy inference

Given the runtime lacks the enabled V5 intent capability, when a caller sets a
Topline process, binds a Topline target, records a Topline receipt, or closes a
Topline through this feature, then the gateway returns
`topline_v5_unavailable` and writes nothing. An Execution Map row with matching
creator-turn ancestry does not change the result.

### A19 — CLI, wire, and projections agree

Given each new CLI mutation, when the CLI encodes it, then the byte-exact wire
request contains the selected scope, expected revision, complete snapshot or
binding data, reason where required, and idempotency key. Gateway and direct
wire tests return the same named errors. Work-item and V5 Topline reads expose
the same effective identities, source ids, target revision, receipt id, and
baseline in stable order.

## Open Questions

None. Mike's ruling fixes the MVP scopes and the target boundary. The reviewed
V5 dependency remains a rollout prerequisite with NOT-PROVEN runtime evidence;
it is not an unmarked design choice in this specification.
