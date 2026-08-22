# Declarative required-process gates

Status: changes-requested specification amended after round-2 verdict
`att_9b353a42-cd00-48c0-8b0c-f3e244315052`; the amended bytes require a cold
digest and re-review for `wi_f165cdbd-72c0-4add-bb8d-2113908c3e55`. This
specification authorizes no
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
- Independent review `att_d9aa11c7-ea16-4797-8e36-ddf05fa6706f` requested six
  changes: established rail identity reuse, a deterministic V5 capability seam,
  an exact wire contract, wrong-scope refusal, a concrete catalog-transition
  gate, and canonical hash bytes. This revision addresses only those blockers.
- Round-2 review `att_9b353a42-cd00-48c0-8b0c-f3e244315052` found that the
  catalog gate named the post-publication `identity-apply` consumer instead of
  the actual pre-publication `tightbeam/live` boundary, and that invalid scalar
  wire values lacked exact refusals and precedence. This revision removes the
  false seam and closes those scalar cases.

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
- **Active catalog identity:** The one process or delivery-target identity that
  a new mutation resolves for a stable name. Older installed identities remain
  addressable for existing rows but are not candidates for new mutations.
- **Process definition:** An installed Kung Fu declaration that maps one
  process identity to existing dispatch-tier rail identities for one or both
  completion transitions. It declares the exact fact-contract identities that
  those rules consume.
- **Required-process rail:** An installed dispatch-tier rule marked
  `attachment = "required-process"`. It stays outside global rule selection and
  participates only when an effective process definition selects it.
- **Target landing rail:** One of the two core rules
  `delivery-target-landed-work-item` and `delivery-target-landed-topline`, each
  marked `attachment = "delivery-target"` and targeted to its named completion
  verb. An active target binding selects the corresponding rule.
- **Delivery-admission rail:** An installed dispatch-tier rule marked
  `attachment = "delivery-target-admission"`. It stays outside global rule
  selection and participates only when an exact delivery-target identity
  selects it during `delivery-landed-record`.
- **Neutral landed fact:** The core boolean fact contract
  `delivery_target.landed@1`. It is true only when the object has one admitted
  receipt for its exact active target-binding revision and identity and that
  receipt carries a nonblank baseline.
- **Rail identity:** The established immutable tuple
  `(name, version, definitionSha256)` from `completion-rails-decisions.md`.
  This specification adds no second rule-identity form.
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
- **Gate-set hash:** The SHA-256 of the canonical effective process identities,
  their sources, and the active target-binding revision and identity or null.
  It changes when any completion-gating input changes.
- **Open catalog reference:** An exact process, target, selected-rail, or fact
  identity reachable from the current organization revision; from the current
  local revision of a nonterminal object; from a Topline revision inherited by
  a nonterminal member work item; or from an active target binding on a
  nonterminal object.
- **Delivery target:** An installed, versioned Kung Fu declaration. The
  substrate treats its name and evidence contract as opaque data.
- **Delivery-target identity:** The tuple
  `(name, version, definitionSha256)`. A target binding stores the exact tuple
  that it resolved.
- **Target binding:** One append-only revision that binds one work item or one
  V5 Topline to zero or one exact delivery-target identity.
- **Declared baseline:** The opaque, nonblank baseline string in a landed
  receipt. The defining Kung Fu decides whether it denotes a commit, branch,
  tag, build, design revision, domain state, or another value.
- **Landed receipt:** The one append-only row for one exact target-binding
  revision. It states that the binding landed at one declared baseline and
  names the evidence rows, admission result, cause, principal, and time. A new
  baseline requires a new binding revision.
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

A new scope mutation refuses an unknown process name before it writes. A
completion attempt refuses when the installed catalog lacks the stored process
identity, rail identity, or fact-contract identity. The response names the
missing identity and two remedies: restore that exact installed contract, or
append an authorized scope revision that resolves to an installed contract.

### I8 — Completion check and state change are one transaction

The gateway evaluates the effective process set from one database snapshot.
It evaluates selected rails and commits the successful close in the same
serialized transaction. A membership, scope, target, receipt, or object-state
change cannot occur between the check and the close.

An unmet rule commits its durable denial and remedy-episode evidence before the
gateway returns the denial. The target state does not change.

### I9 — A failure names cause, principal, and repair

A failed gate names the selected rail identity, target kind, target id,
gate-set hash, row-visible reason, and supported remedy. A process-selected
rail also names each selecting process identity in canonical order. The target
landing rail instead names its binding revision and delivery-target identity.
The durable denial records the checked principal and the command cause. A
satisfied gate is silent.

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

The substrate repeats this selection from current rows before each remedy
notice. A recurrence has no caller session and starts at step 2. An episode does
not pin a holder. Before a recurrence notice, the substrate also recomputes the
object's current gate-set hash. If the hash changed or the episode's rule is no
longer selected, supervision closes that episode as `gate_set_superseded` and
sends no notice.

### I11 — Opt-out is silent

When the object's effective process set is empty and the object has no target
binding, completion follows its existing path. Required-process code writes no
denial, remedy episode, wake, receipt, or policy event. It does not add a
latency-bearing external check. An empty local revision and clears that produce
an empty effective set stay silent under the same rule.

### I12 — Target binding has exact scope

A work item and a V5 Topline can each have zero or one active target binding.
A Topline target gates only `topline-close`. It does not gate a member work
item. A work-item target gates only `work-item-close`. It does not gate a
Topline. Organization scope does not carry a target binding in this MVP.

### I13 — Target meaning stays in Kung Fu

A target definition declares its immutable identity, its receipt-admission
rails, and its exact fact contracts. Each admission rail carries
`attachment = "delivery-target-admission"`. Tightbeam stores and compares the
identity, baseline, evidence references, and rule result. It does not parse a
repository, branch, tag, build, environment, deployment, design, or domain
value.

### I14 — A binding requires a matching landed receipt

Target-binding presence selects the neutral installed target landing rail for
that object's close. The rail passes only when an admitted landed receipt names
the active binding revision, exact target identity, and one nonblank declared
baseline. A receipt for an earlier binding, another object, or another target
identity does not satisfy the rail. The rail does not compare the opaque
baseline with an inferred or substrate-defined baseline.

Clearing a target binding removes this rail from later completion attempts. The
clear and older receipts remain visible history.

### I15 — Landing evidence is admitted before completion

`delivery-landed-record` runs the binding's exact installed target definition
and admission rails against durable evidence references. Each selected rail
must allow. The command writes the one receipt for that binding revision and
its idempotency result in one transaction only after the fold allows. A
completion transaction reads the receipt; it does not contact an external
system.

### I16 — Completion truth does not decay

A successful close records the gate-set hash, target-binding
revision if present, landed-receipt id if present, and declared baseline in its
completion event. Later branch, design, build, target, process, or fact-contract
drift does not change that historical result.

When later drift creates new work, an authorized agent uses the existing linked
reopen or follow-up work path. The substrate does not reopen an object from a
poll, target change, catalog change, or membership change.

### I17 — Honest failure remains reachable

Required processes and target landing gate successful close only. They do not
gate `work-item-fail` or `work-item-icebox`. An authorized principal can append
a reasoned process clear or target clear before a Topline close when the owner
chooses to end the intent without the selected process or target.

### I18 — Contract evolution is explicit

A rule predicate, fact type, fact meaning, target evidence contract, or process
meaning change creates a new immutable version and hash. A deployment keeps an
old open catalog reference installed, or migrates each affected current scope
or target binding through its ordinary append-only seam before removing it.
Missing compatibility evidence fails closed. The migration uses no
process-specific substrate logic.

### I19 — V5 dependency cannot fall back

Topline-scope policy, Topline target binding, Topline receipt admission, and
the added Topline projections call the V5 intent API only. If the V5 capability
is unavailable, the three mutations return `topline_v5_unavailable` and write
no policy, binding, or receipt row; this specification adds no projection to a
legacy Topline response. None consults Execution Map telemetry or legacy
`toplines` behavior.

The MVP is not runtime-proven until the V5 runtime proof resolves
`att_a76de51c`. A staged build can expose organization and work-item policy
first. It does not register or replace `topline-close`. After the V5
implementation supplies that reviewed lifecycle, the close handler activates
this specification's Topline gate only when the exact V5 capability is enabled.
An absent capability leaves that hook disabled and cannot call an Execution Map
delegate.

### I20 — Hash inputs have one byte representation

Each definition, catalog revision, gate set, and idempotency fingerprint hash
uses the canonical JSON bytes specified in Architecture. A producer cannot hash
TOML source bytes, map iteration order, presentation JSON, or an array before
its required sort.

### I21 — Process verbs and scope are compatible

Each process definition declares a nonempty subset of `work-item-close` and
`topline-close`. Completion expands only rails for the attempted verb. A
work-item scope mutation refuses a process that omits `work-item-close` with
`required_process_scope_incompatible`. An organization mutation that names a
process containing `topline-close` requires the V5 capability. A Topline scope
mutation requires the V5 capability and can select a work-item-only process for
its active member work items, a Topline-only process for the Topline close, or a
process for both verbs.

## Architecture

### Toplines V5 capability seam

Add `Tightbeam.RuntimeCapabilities` and the packaged file
`priv/runtime-capabilities.toml`. The file has no default `toplines_v5` entry.
The V5 release can add exactly this entry only after its runtime proof is
reviewed:

```toml
[toplines_v5]
contract_sha256 = "d39dd61cb44f5c6ff0bbc301b28d64a893b294d1a894e148b1449b36d5585bf9"
schema_version = 5
```

`Tightbeam.Toplines.capability/0` returns exactly
`%{contract_sha256: "d39dd61cb44f5c6ff0bbc301b28d64a893b294d1a894e148b1449b36d5585bf9",
schema_version: 5}` only when the module implements the reviewed V5 intent API,
active-membership query, and transaction-scoped close hook. At boot,
`Tightbeam.RuntimeCapabilities.load!/1`
compares the packaged entry, the module return, the installed schema version,
and the registered `topline-close` handler. If the file omits the entry, the
gateway records `toplines_v5` as disabled and continues to serve organization
and work-item functionality. If the file contains the entry and any comparison
fails, boot stops with `toplines_v5_capability_invalid` and names the mismatched
field.

The boot error is canonical JSON
`{"error":{"code":"toplines_v5_capability_invalid","field":"<field>","message":"toplines v5 capability is invalid"}}`.
`field` is one of `contractSha256`, `schemaVersion`, `intentApi`,
`activeMembershipQuery`, or `toplineCloseHandler`.

The three Topline mutation selectors and the V5 Topline projection introduced
here call
`Tightbeam.RuntimeCapabilities.require(:toplines_v5)` before object lookup.
The V5 `topline-close` handler calls the same check before this specification's
gate hook. The staged build does not add a `topline-close` handler; the V5
implementation owns that verb and lifecycle. Neither capability branch calls
legacy telemetry code.

### Pattern: named process selection over existing rails

Kung Fu projects process declarations to `identity/processes/*.toml`. Each
declaration contains a stable qualified name, positive version, applicable
completion verbs, installed required-process rail identities, and fact-contract
identities. The loader computes the process declaration hash and consumes each
rail's established versioned identity from the served rail catalog; a process
declaration cannot assert either hash. A catalog selection index, excluded from
definition hashes, maps each selectable stable name to one exact installed
identity. An installed identity absent from the index remains available to
existing rows but cannot satisfy a new stable-name mutation. The process loader
validates the full catalog at boot. It rejects a duplicate name/version, an
index entry that names no exact installed identity, an empty or unknown
completion-verb set, an unsupported fact contract, a rail that lacks
`attachment = "required-process"`, a rail whose verb is absent from the process
completion-verb set, a declared verb with no selected rail, a rail from another
attachment class, or a dependency cycle. Globally selected statutes stay
outside this attachment class, and a scope clear cannot suppress them.

The core target module reserves and installs
`delivery-target-landed-work-item` for `work-item-close` and
`delivery-target-landed-topline` for `topline-close`. Both rules carry
`attachment = "delivery-target"`. Both deny when the core
`delivery_target.landed@1` fact is false. The fact resolver reads only the exact
active binding and its one admitted receipt. Boot refuses if the fact contract
or either reserved rule is absent, duplicated, targets another verb, or has
another attachment.

The binding layer selects process identities. The rules engine evaluates them.
The binding layer does not implement a workflow or interpret evidence.

### Canonical bytes and hashes

Canonical JSON uses UTF-8, object keys sorted by UTF-8 byte order, no
insignificant whitespace, lowercase `true`, `false`, and `null`, and base-10
integers without leading zeroes. It rejects floating-point values and invalid
Unicode. A string emits Unicode scalar values as UTF-8, escapes a quotation
mark as `\"`, escapes a reverse solidus as `\\`, never escapes `/`, and encodes
each U+0000 through U+001F control as lowercase `\u00xx`; it does not use the
short control escapes. Each SHA-256 is the lowercase hexadecimal hash of those
exact bytes. Arrays use the order below before serialization:

- rail identities sort by `name`, then numeric `version`, then
  `definitionSha256`;
- fact-contract identities sort by `factName`, then numeric `version`, then
  `type`, then `semanticsSha256`;
- process and target identities sort by `name`, then numeric `version`, then
  `definitionSha256`;
- source strings sort as `organization`, then `tl_...` by UTF-8 bytes, then
  `wi_...` by UTF-8 bytes;
- typed evidence references sort by `kind`, then `id`, both by UTF-8 bytes.
- completion verbs and stable-name lists sort by UTF-8 bytes.

The closed identity objects used below are:

```json
{"definitionSha256":"<hex>","name":"<name>","version":1}
{"factName":"<name>","semanticsSha256":"<hex>","type":"<type>","version":1}
```

The first shape is a process, target, or rail identity according to its field
context. The second shape is a fact-contract identity. An error field that can
carry more than one identity class adds a discriminator and uses exactly one of
these shapes:

```json
{"definitionSha256":"<hex>","kind":"process|deliveryTarget|rail","name":"<name>","version":1}
{"factName":"<name>","kind":"factContract","semanticsSha256":"<hex>","type":"<type>","version":1}
```

A process `definitionSha256` hashes this closed semantic object:

```json
{"completionVerbs":["topline-close","work-item-close"],"factContracts":[{"factName":"<name>","semanticsSha256":"<hex>","type":"<type>","version":1}],"name":"<qualified-name>","rails":[{"definitionSha256":"<hex>","name":"<rail-name>","version":1}],"version":1}
```

The `completionVerbs` array contains only the declared verbs and sorts by UTF-8
bytes. A delivery-target `definitionSha256` hashes this closed semantic object:

```json
{"admissionRails":[{"definitionSha256":"<hex>","name":"<rail-name>","version":1}],"factContracts":[{"factName":"<name>","semanticsSha256":"<hex>","type":"<type>","version":1}],"name":"<qualified-name>","version":1}
```

A fact contract's `semanticsSha256` hashes this closed semantic object:

```json
{"factName":"<name>","semantics":"<nonblank-contract-text>","type":"<type>","version":1}
```

The served fact catalog retains the exact semantic text and computed identity.
The canonical serializer performs no Unicode normalization or text trimming.
A semantic-text, type, or shape change creates a new version and hash.
Removing this byte binding would permit in-place semantic replacement;
accepting that failure would make catalog compatibility non-deterministic.

Rail definition hashes arrive as part of the served rail catalog's established
versioned identity. This specification treats them as opaque exact values and
does not compute or redefine them.

The process catalog revision hashes
`{"active":[{"identity":<process-identity>,"name":"<name>"}],"definitions":[<process-identity>...]}`.
The target catalog uses the same object with target identities. Both arrays use
the identity ordering above; `active` sorts by `name`. Selection metadata does
not enter a definition hash.

The gate-set hash covers exactly
`{"processes":[{"identity":<process-identity>,"sources":["<source>"...]}],"targetBinding":<null-or-object>}`.
The non-null target object is
`{"definitionSha256":"<hex>","name":"<name>","revision":<integer>,"version":<integer>}`.
The idempotency fingerprint hash covers the exact operation envelope and closed
parameter shapes in Wire contract below. Stored JSON columns use these same
canonical bytes.

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
cause. The current revision is the greatest committed revision. Organization
current-state discovery uses the existing `org_settings` key
`required-process-policy-revision`, which stores the current organization
revision number. The scope revision and this setting change in one transaction.
Topline and work-item current revisions need no mutable pointer.

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
stable-name UTF-8 byte order in stored canonical JSON. The gateway rejects
duplicates and require/clear overlap.

Only an administrator can mutate organization scope. The Topline or work-item
owner, a session owned by that user, or an administrator can mutate the object
scope. Authorization and exact-id resolution occur inside the write
transaction. Unknown and invisible objects return the same bytes.

After active-identity resolution, the same transaction applies I21. A work-item
scope request containing a process without `work-item-close` returns
`required_process_scope_incompatible`. A Topline scope request requires the V5
capability; it accepts a process for either completion verb because the Topline
is both a close target and an explicit inheritance source for active member
work items. An organization request containing a `topline-close` process also
requires the V5 capability. Each refusal writes no scope revision or
idempotency row.

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
  "localCleared": []
}
```

The projection sorts by stable name, version, and hash. It derives sources from
the current rows and active V5 memberships. It does not persist a copied
effective set on the work item.

### Delivery-target rows and mutation seams

Kung Fu projects target declarations to `identity/delivery-targets/*.toml`.
Each target declaration contains a stable qualified name, positive version,
computed definition hash, receipt-admission rail identities, and fact-contract
identities. A catalog selection index, excluded from definition hashes, maps
each selectable stable name to one exact installed identity. An installed
identity absent from the index remains available to existing bindings but
cannot satisfy a new stable-name mutation. The target loader rejects a
duplicate name/version, an index entry that names no exact installed identity,
an unsupported fact contract, an admission rule that lacks
`attachment = "delivery-target-admission"`, or an admission rule that targets a
verb other than `delivery-landed-record`.

Add append-only `delivery_target_binding_revisions` and
`delivery_landed_receipts` tables. A binding revision stores target kind, target
id, revision, nullable exact target identity, reason, cause, principal, owner,
and time. A null identity is an explicit clear. A receipt stores its own id,
binding revision, exact target identity, declared baseline, canonical typed
evidence-row references, admission decision id, cause, principal, owner, and
time. A unique constraint on `(targetKind, targetId, bindingRevision)` permits
one receipt for one binding revision.

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
row-reference resolver. The target's admission rails decide which references
and facts are required. The substrate validates existence, visibility, exact
binding identity, and the installed rule result.

The target object's owner, a session owned by that user, or an administrator
can set or clear its binding and record its landed receipt. Authorization and
object lookup occur inside each write transaction. A binding mutation resolves
the named active target identity inside that transaction. A receipt mutation
reads the binding's exact stored target identity and evaluates that identity's
installed admission contract inside the transaction. Unknown and invisible
objects return the same bytes. A new binding mutation with an unknown target
name returns `unknown_delivery_target`. An unavailable stored target identity
or admission contract returns `delivery_target_version_unavailable`. A second
receipt request for the binding under another idempotency key returns
`landed_receipt_exists`. Each refusal writes no
binding revision or landed receipt.

Reads expose `deliveryTarget: null` when unbound. A bound projection exposes
the exact identity, binding revision, binding principal and reason, the
matching receipt id, and declared baseline. It does not expose domain-specific
interpretation.

### Completion and remedy seam

`work-item-close` and V5 `topline-close` call one transaction-scoped selector
before the state mutation. The selector returns the effective process
identities plus the object's corresponding target landing rail when that exact
object has an active target binding. It computes the gate-set hash and then
calls the existing rules decision fold in installed deterministic order. It
evaluates one copy of each selected rail identity and preserves the canonically
ordered process identities that selected that rail.

On allow, the handler commits the close and its completion evidence. On denial,
the handler commits the denial and uses `RailRemedy` with subject
`<target-kind>:<target-id>:<gate-set-sha256>:<rail-identity>`. Repeated denials
can leave separate attempt events, but one live remedy subject produces one
initial notice. When the required fact appears, the next evaluation closes the
remedy episode through the existing close path. Before recurrence sends a later
notice, supervision recomputes the current gate-set hash and current
responsible agent, then evaluates the episode's exact selected rail against
current durable facts. It closes a superseded episode without a notice. If the
rail now allows, it closes the episode as `gate_now_satisfied` without a notice.
Otherwise, it routes the live episode to the newly selected responsible agent.
Deleting recurrence would discard existing prodding; accepting a notice after
the rail allows would violate I9's satisfied-gate silence.

### Idempotency, crash, and replay

Policy, target, and receipt mutations use the existing wire-idempotency
pattern. The idempotency row key is
`(callerUserId, operation, idempotencyKey)`. Its fingerprint is SHA-256 over
`{"operation":"<verb>","parameters":{<closed-shape>}}` using the canonical
bytes below. `parameters` contains each validated request value except
`idempotencyKey`; it contains no authenticated principal, catalog-derived
identity, or other value that can change after the first commit.

- The gateway authenticates the current principal and authorizes the named
  object before it reads an idempotency row. A direct Topline selector first
  performs I19's capability check, as fixed in the refusal precedence below.
- After authorization, the gateway checks a matching committed idempotency row
  before it resolves the current catalog, mutable revision, binding, evidence,
  or admission rails.
- The same key and fingerprint returns the stored response and writes nothing,
  even when the live catalog or binding changed after the first commit.
- The same key with another fingerprint returns `idempotency_conflict`.
- A stale expected revision returns `revision_conflict` and writes nothing.
- A crash before commit leaves no revision, receipt, event, or idempotency row.
- A crash after commit returns the committed result on replay.
- A completion retry re-reads current rows. It cannot reuse an in-memory pass.

### Wire contract

The CLI sends the existing `/agent/dispatch` envelope and no typed target. For
a session credential with no identity override, the three mutation bodies have
exactly these keys; expanded whitespace below is not sent:

```json
{"params":{"cleared":["<process-name>"],"expectedRevision":3,"idempotencyKey":"<key>","reason":"<reason>","required":["<process-name>"],"scopeKind":"organization|topline|workItem","scopeRef":"organization|tl_...|wi_..."},"verb":"required-processes-set"}
{"params":{"expectedRevision":3,"idempotencyKey":"<key>","reason":"<reason>","targetId":"tl_...|wi_...","targetKind":"topline|workItem","targetName":"<target-name>"},"verb":"delivery-target-set"}
{"params":{"baseline":"<opaque-nonblank-text>","bindingRevision":3,"evidence":[{"id":"<row-id>","kind":"<supported-row-kind>"}],"idempotencyKey":"<key>","targetId":"tl_...|wi_...","targetKind":"topline|workItem"},"verb":"delivery-landed-record"}
```

`targetName: null` is the one target-clear representation. Each other listed
member is required and non-null. The router returns `invalid_message` for an
omitted member, an extra member, a wrong JSON type, a scope-kind/id-prefix
mismatch, duplicate list entries, require/clear overlap, or a list outside its
required canonical order. It also returns `invalid_message` when
`expectedRevision` is not an integer greater than or equal to zero,
`bindingRevision` is not a positive integer, or a required string fails the
closed scalar constraints below. `organization` requires
`scopeRef: "organization"` and an empty `cleared` array.

All strings are valid UTF-8 and are stored without trimming. `reason` and
`baseline` contain 1 through 2,000 Unicode code points and remain nonempty after
`String.trim/1`. `idempotencyKey`, each process or target name, and each
evidence `kind` and `id` contain 1 through 200 Unicode code points and remain
nonempty after `String.trim/1`. A null `targetName` bypasses the target-name
constraint. A nonblank evidence kind that the existing typed row-reference
resolver does not support passes wire-shape validation and later returns
`unsupported_evidence_kind`; a blank kind returns `invalid_message`.

The idempotency fingerprint removes only
`idempotencyKey` and wraps the remaining `params` as the operation envelope in
Idempotency, crash, and replay.

The gateway wraps successful handler values in `{"result":...}`. The exact
handler values are:

```json
{"requiredProcesses":<required-processes-object>,"scopeKind":"organization|topline|workItem","scopeRef":"organization|tl_...|wi_..."}
{"bindingRevision":4,"deliveryTarget":<delivery-target-object-or-null>,"targetId":"tl_...|wi_...","targetKind":"topline|workItem"}
{"landedReceipt":<landed-receipt-object>,"targetId":"tl_...|wi_...","targetKind":"topline|workItem"}
```

A required-processes object contains exactly `effective`, `localCleared`,
`localRequired`, and `localRevision`. Each identity in
`effective` or `localRequired` contains exactly `definitionSha256`, `name`, and
`version`; an effective entry also contains `sources`. The arrays and object
keys use Canonical bytes and hashes ordering. `localRevision` is `0` when the
scope has no revision.

A non-null delivery-target object contains exactly `baseline`,
`bindingPrincipal`, `bindingReason`, `bindingRevision`, `definitionSha256`,
`landedReceiptId`, `name`, and `version`. `baseline` and `landedReceiptId` are
both null before landing. `bindingPrincipal` is exactly
`{"kind":"user|session","ref":"<id>"}`. A landed-receipt object contains
exactly `admissionDecisionId`, `baseline`, `bindingRevision`, `cause`,
`createdAt`, `evidence`, `id`, `principal`, and `targetIdentity`.
`targetIdentity` contains exactly `definitionSha256`, `name`, and `version`;
`principal` has the same actor shape as `bindingPrincipal`.

New handler refusals use exactly
`{"error":{"code":"<slug>","message":"<message>"}}` unless one of the
structured exceptions below applies. The closed slug/message mapping is:

| Slug | Message |
| --- | --- |
| `binding_revision_conflict` | `binding revision does not match` |
| `delivery_target_version_unavailable` | `delivery target version is unavailable` |
| `idempotency_conflict` | `idempotency key conflicts with a prior request` |
| `invalid_message` | `invalid message` |
| `landed_receipt_exists` | `landed receipt already exists` |
| `not_found` | `record not found` |
| `process_denied` | `process principals cannot mutate required process state` |
| `required_process_catalog_in_use` | `candidate catalog removes an open required-process reference` |
| `required_process_identity_conflict` | `required process identities conflict` |
| `required_process_scope_incompatible` | `required process does not apply to this scope` |
| `required_process_version_unavailable` | `required process version is unavailable` |
| `revision_conflict` | `expected revision does not match` |
| `topline_v5_unavailable` | `toplines v5 capability is unavailable` |
| `unknown_delivery_target` | `delivery target is not installed` |
| `unknown_required_process` | `required process is not installed` |
| `unsupported_evidence_kind` | `evidence kind is not supported` |

`required_process_catalog_in_use` instead returns exactly:

```json
{"error":{"code":"required_process_catalog_in_use","message":"candidate catalog removes an open required-process reference","missingIdentity":<discriminated-identity>,"referencingRowIds":["<row-id>"...]}}
```

`referencingRowIds` sorts by UTF-8 bytes. The boot-only
`required_process_catalog_incompatible` uses the same inner object and message
`installed catalog omits an open required-process reference`; boot writes that
object to its structured startup error rather than an HTTP response.

The unavailable-identity and identity-conflict exceptions return exactly:

```json
{"error":{"code":"required_process_version_unavailable","message":"required process version is unavailable","missingIdentity":<discriminated-identity>,"remedies":["restore_exact_contract","migrate_scope_revision"]}}
{"error":{"code":"delivery_target_version_unavailable","message":"delivery target version is unavailable","missingIdentity":<discriminated-identity>,"remedies":["restore_exact_contract","append_target_binding_revision"]}}
{"error":{"code":"required_process_identity_conflict","conflicts":[{"identity":<process-identity>,"sources":["<source>"...]}...],"message":"required process identities conflict"}}
```

`conflicts` uses process-identity order. Each `sources` array uses source order.
These remedies name existing append-only mutation paths; they do not execute a
repair.

A selected completion rail denial instead returns exactly:

```json
{"error":{"code":"required_process_denied","gateSetSha256":"<hex>","message":"required process gate denied","processes":[<process-identity>...],"rail":<rail-identity>,"reason":"<installed-reason-code>","remedy":"<installed-remedy-code-or-null>","targetId":"tl_...|wi_...","targetKind":"topline|workItem"}}
```

For a target landing denial, `processes` is empty and the error also contains
`"binding":{"definitionSha256":"<hex>","name":"<name>","revision":3,"version":1}`.
A delivery-admission rail denial is exactly:

```json
{"error":{"code":"delivery_evidence_denied","message":"delivery evidence denied","rail":<rail-identity>,"reason":"<installed-reason-code>","remedy":"<installed-remedy-code-or-null>","targetId":"tl_...|wi_...","targetIdentity":<target-identity>,"targetKind":"topline|workItem"}}
```

The installed immutable rail supplies `reason` and `remedy`; tests load a real
rail fixture rather than inventing response text.

Validation chooses the first applicable refusal in this order: existing exact
CLI compatibility; transport authentication and principal kind; closed wire
shape; `toplines_v5` capability for a direct Topline selector; owner-filtered
object visibility and authorization; idempotency replay or conflict; expected
scope or binding revision; active catalog resolution; I21 scope compatibility;
effective-set identity conflict; binding and receipt state; typed evidence
kind support; typed evidence existence and visibility; selected-rail decision.
An organization request discovers that a resolved process contains
`topline-close` during I21 and then applies the capability check. Each refusal
writes no domain or idempotency row unless I8 explicitly requires a durable
completion denial.

### Compatibility and rollout

The new mutation verbs and response members are additive to the current wire
surface. Existing work-item verbs keep their spelling and existing fields.
Current clients can ignore the added projections. A client that sends a new
verb to an older gateway receives its ordinary unknown-verb or exact-version
refusal; it cannot believe a binding applied.

Execution Map responses remain unchanged. They do not expose, inherit, or
evaluate required-process or delivery-target state.

Schema migration adds the new tables. When the V5 Topline module is present,
boot registers it before the Topline extensions in this specification. A staged
build without V5 does not register those extensions. Migration creates no
policy revision, target binding, receipt, denial, remedy, or wake. The
organization setting remains absent until an administrator opts in.

Add `Tightbeam.RequiredProcesses.validate_catalog_transition/3`, with arguments
`(databaseSnapshot, currentCatalogSet, candidateCatalogSet)`. Each catalog set
contains its process, target, rail, and fact catalogs.

The actual pre-publication seam is `Tightbeam.Identity.publish_live!/1`, which
fast-forwards `refs/heads/tightbeam/live` from the current live object id to the
candidate `identity/main` object id. Evolve it to `publish_live!/2` with a
required publication guard. Every existing caller supplies that guard;
catalog-neutral identity edits validate as a no-op. `identity-apply` only
materializes a revision that is already live, so it does not participate in
this transition gate.

The gateway supplies
`Tightbeam.RequiredProcesses.guard_live_publication/5` with
`(database, runtimeConfig, currentLiveOid, candidateMainOid, advanceRef)`. The
guard loads and validates both catalog sets by exact Git object id, then enters
the same serialized database-owner critical section used by scope, binding,
receipt, and completion selectors. Inside that section it calls
`validate_catalog_transition/3` against one database snapshot. If the candidate
omits one reachable identity, the guard does not call `advanceRef`; the
publication command returns `required_process_catalog_in_use`, names the
missing identity and referencing row ids, and leaves `tightbeam/live`, the
served law registry, and the database unchanged. The candidate commit can
remain unserved on `identity/main` for an ordinary corrective identity edit.

On allow, the guard preloads the candidate law, invokes `advanceRef` as a
compare-and-swap from `currentLiveOid` to `candidateMainOid`, swaps the served
law registry to those already validated bytes, and only then releases the
critical section. Requests cannot observe a new ref with old served law or old
ref with new served law. A crash before the compare-and-swap leaves the old ref
live. A crash or reload failure after it terminates the serving process before
traffic resumes; boot then validates and loads the exact live object id. This
reuses the existing publication boundary and adds no release entity or verb.

Binary boot calls the same function after schema migration and before the
gateway accepts traffic, using the installed catalogs as the candidate. A
missing referenced identity stops boot with
`required_process_catalog_incompatible` and the same identity and row ids.
Core target rails and `delivery_target.landed@1` participate in this boot check.
A rollout first retains the exact identity or migrates each named current scope
or binding through its ordinary append-only mutation, then retries the existing
identity publication or boot seam. The V5 runtime smoke is a prerequisite for
adding the `toplines_v5` capability entry.

### Proposed implementation paths

This path census is a build boundary, not implementation authority:

- Add `lib/tightbeam/required_processes.ex` for catalog validation, scope
  revisions, composition, projections, and transaction-scoped selection.
- Add `lib/tightbeam/runtime_capabilities.ex` and packaged
  `priv/runtime-capabilities.toml` for the fail-closed V5 seam. The staged file
  omits `toplines_v5`.
- Add `lib/tightbeam/delivery_targets.ex` for target catalog validation,
  binding revisions, receipt admission, and the neutral landed fact.
- Register both schemas in `lib/tightbeam/schema.ex`. When V5 is present, its
  Topline and membership schemas precede these extensions; staged work-item and
  organization support does not require a V5 registration.
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
- Call `guard_live_publication/5` from the existing `publish_live!/2`
  pre-publication boundary. Call `validate_catalog_transition/3` from that
  guard and from boot after migration and before gateway traffic.
- Add focused proofs in `test/required_processes_test.exs`,
  `test/delivery_targets_test.exs`, `test/work_items_test.exs`,
  `test/toplines_test.exs`, `test/rules_test.exs`, `test/gateway_test.exs`,
  `test/router_test.exs`, `test/payloads_test.exs`, capability and
  identity-publication suites, and the CLI suites.
- Add Kung Fu declarations under `priv/kungfu/<bundle>/processes/*.toml` and
  `priv/kungfu/<bundle>/delivery-targets/*.toml` only when a reviewed product
  lane defines actual process or target meaning.

This specification teaches no agent operating pattern before the mechanism
exists. Guidance lands with the implementation only after the named verbs and
failure contracts pass their acceptance cases.

## Acceptance

### A1 — No opt-in preserves existing completion

Given an object's effective process set is empty and it has no target binding,
when an authorized principal closes the otherwise closable object, then the
existing close response and state transition succeed. This remains true when
empty local revisions or clears produce that empty set. The feature writes no
policy, denial, remedy, wake, target, or receipt row.

### A2 — Organization requirements reach ungrouped work

Given the organization requires installed process `P` and work item `W` has no
active V5 membership or local override, when `W` closes without `P`'s required
evidence, then the gateway denies by exact process and rail identity. Given the
evidence exists, the same close succeeds and records the gate-set hash.

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
and keeps the object open. Each selected rail is named by exact
`(name, version, definitionSha256)`. The gateway does not select a winner or
construct a versionless rail identity.

### A7 — Scope mutation is authorized, atomic, and replay-safe

Given scope revision `3`, when an authorized caller submits a complete local
snapshot with expected revision `3`, then revision `4`, its cause/principal
event, and its idempotency result commit together. A same-key replay returns
revision `4` even after the active catalog identity changes. A changed
fingerprint, stale revision, invisible id, or injected fault writes no partial
revision.

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

Given a session caller holds an open assignment on an active member work item
of Topline `T`, when `T`'s process gate denies, then one live remedy episode
targets that session. Given no caller-held assignment and exactly one distinct
holder in `T`'s active members, the episode targets that holder. Given ambiguous
or empty holder custody, including a closable work item with no open
assignment, it targets the owner's personal Main. Repeated denial for the same
subject produces no spawn, assignment, reassignment, or duplicate live notice.
Given custody changes before recurrence, when the episode remains current, then
the next notice targets the newly selected responsible agent. Given the
gate-set hash changes before recurrence, then supervision closes the old
episode as `gate_set_superseded` and sends no notice.
Given the hash is unchanged but the missing durable fact now exists, then
recurrence closes the episode as `gate_now_satisfied` and sends no notice.

### A11 — Work-item target does not roll up

Given work item `W` has a target binding and its Topline `T` has none, when `W`
closes without a matching receipt, then `delivery-target-landed-work-item`
denies.
When `T` closes, `W`'s binding does not participate.

### A12 — Topline target does not roll down

Given Topline `T` has a target binding and member work item `W` has none, when
`T` closes without a matching receipt, then `delivery-target-landed-topline`
denies. When `W` closes, `T`'s binding does not participate.

### A13 — Receipt admission stays domain-owned

Given a target definition requires evidence facts `E`, when an authorized
caller records a receipt without `E`, then the target's installed admission
rule denies and no receipt commits. Given `E` exists and the active binding,
target identity, and references match, and the caller supplies a nonblank
baseline, then one receipt and its admission decision commit. A same-key replay
returns that receipt after a later binding or catalog change. A different-key
request for the same binding returns `landed_receipt_exists` and writes no
second receipt.

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

Given a candidate `identity/main` revision removes fact contract `F@1` while an
open catalog reference reaches it, when identity publication attempts the
compare-and-swap advance of `tightbeam/live`, then it returns
`required_process_catalog_in_use`, names `F@1` and the sorted referencing row
ids, and changes neither `tightbeam/live`, the served law registry, nor the
database. Given an installed binary catalog omits that reference, when the
gateway boots, then boot stops with `required_process_catalog_incompatible` and
the same evidence. Given migration appends current scope revisions to `F@2`,
then a later publication succeeds and preserves `F@1` history. The same cases
apply to a target definition, selected rail, or target fact contract reached by
an active binding on a nonterminal object.

### A18 — V5 absence never becomes legacy inference

Given `priv/runtime-capabilities.toml` omits `toplines_v5`, when a caller sets a
Topline process, binds a Topline target, or records a Topline receipt, then the
gateway returns `topline_v5_unavailable` and writes nothing. Given the V5 module
and `topline-close` handler exist while that entry is absent, when the caller
closes a Topline, then the V5 handler returns `topline_v5_unavailable` before
this gate hook. Given the staged build has no V5 close handler, then this
specification does not register one. Given the packaged entry disagrees with
the V5 module, schema version, or registered handler, then boot stops with
`toplines_v5_capability_invalid`. An Execution Map row with matching
creator-turn ancestry changes none of these results.

### A19 — CLI, wire, and projections agree

Given each new CLI mutation and a session credential without an identity
override, when the CLI encodes it, then its bytes equal the corresponding
closed request in Wire contract. Given one fixture for each fixed refusal and
each selected-rail denial shape, when the CLI and direct wire invoke it, then
both return the exact canonical error bytes. Given two simultaneously true
refusals, then the response follows the stated precedence. Work-item and V5
Topline reads expose the exact required-processes and delivery-target objects in
canonical order.

Given a blank `reason` and an unknown process name, or a negative
`expectedRevision` and an unknown process name, then wire-shape validation
returns exact `invalid_message` bytes before catalog resolution. Given valid
scalars, a current binding, and a nonblank unsupported evidence kind, then
receipt admission returns exact `unsupported_evidence_kind` bytes. Given that
unsupported kind with a stale binding revision, then
`binding_revision_conflict` wins by the stated precedence.

### A20 — Target mutations are authorized and exact

Given object owner `U`, when another non-administrator user sets its target or
records its receipt, then the gateway returns the same response bytes as for an
unknown object and writes nothing. Given `U`, a session owned by `U`, or an
administrator names an unknown target in a new binding request, then the
gateway returns `unknown_delivery_target` and writes nothing. Given an
authorized caller binds an active target identity and that exact installed
identity later disappears, then receipt admission returns
`delivery_target_version_unavailable` and writes nothing.

### A21 — Catalog selection is deterministic

Given two installed versions for stable process name `P`, when the process
selection index names `P@2`, then a new scope mutation stores the exact `P@2`
identity while a scope that already stores `P@1` continues to resolve `P@1`.
Given a process or target selection index names an identity that is not
installed, when the gateway boots, then catalog validation refuses startup and
names the invalid index entry.

### A22 — Wrong-scope process selection refuses

Given process `P` declares only `topline-close`, when an authorized caller sets
`P` on a work-item scope, then the gateway returns
`required_process_scope_incompatible` and writes nothing. Given process `Q`
declares only `work-item-close` and V5 is enabled, when an authorized caller
sets `Q` on a Topline scope, then the revision commits and `Q` applies only to
active member work items. Given an organization request names a process that
contains `topline-close` while V5 is disabled, then it returns
`topline_v5_unavailable` and writes nothing.

### A23 — Canonical hashes are byte-stable

Given equivalent process, target, or fact-contract declarations whose TOML key
order and formatting whitespace differ while their string values are equal,
when the loader canonicalizes their closed semantic object, then both produce
the same definition or semantics hash. Given equivalent catalogs whose
map or declaration enumeration differs, then both produce the same catalog
revision hash. Given one gate set whose input map or source enumeration order
differs, when both instances sort and serialize under Canonical bytes and
hashes, then both produce the same gate-set hash. Given one request whose
validated closed values are equal, when both handlers build the fingerprint
envelope, then both produce the same fingerprint; changing one semantic value
changes it.

## Open Questions

None. Mike's ruling fixes the MVP scopes and the target boundary. The reviewed
V5 dependency remains a rollout prerequisite with NOT-PROVEN runtime evidence;
it is not an unmarked design choice in this specification.
