# Existing Work-Item Spec Binding

- Status: SPEC-READY — PENDING ONE INDEPENDENT EXACT-REVISION REVIEW
- Work item: `wi_e1c319cb-71b7-44f9-9f12-f5e800e9f56a`
- Spec assignment: `asg_13d9ee65-7268-448e-902b-d7b7e71a6d87`
- Inspected product revisions: 0.2.0 `origin/main` at
  `3fe0e941840ed138a6a285261c0e35687d8d27a3`; 0.1.9 `origin/0.1.9` at
  `e4c9234aa50e42bfdfa6fadd0937dff52d566c66`
- Pattern name: **current-spec binding**

## Goal

G1. An authenticated agent can bind a reviewed spec to an existing open work item and
can replace that binding after a material spec amendment.

- Acceptance: Given an owner-visible open work item with no spec binding, when an
  authorized session runs the supported bind command with a reviewed spec name, digest,
  and an unbound expectation, then `work-item-get` returns that exact name and digest.

G2. One deterministic mutation seam preserves the paired binding, rejects stale writes,
and records the principal and transition for each changed binding.

- Acceptance: Given two writers that read the same current binding, when the first writer
  changes it and the second writer submits a different replacement with the old expected
  pair, then the second call returns `stale_spec_binding` and writes no work-item field or
  history row.

G3. Shipped guidance on the 0.1.9 and 0.2.0 lines names only commands available on that
line.

- Acceptance: Given each line's built CLI command catalog and served guidance tree, when
  the release evidence compares directive-form command examples with that catalog, then
  the spec-homing directive names `work-item-bind-spec`, and no directive names the absent
  metadata form of `work-item-update`.

This feature adds a mechanism because deleting spec references loses durable governing
authority, while accepting attest-only references leaves row readers unable to determine
the current governing spec. The mechanism records a caller's decision; it does not make
that decision.

## Non-Goals

- This spec does not fetch, open, resolve, or verify spec content. The caller computes the
  digest and decides which reviewed spec governs the item.
- This spec does not bind the three blocked specimen work items, mutate another live work
  item, or backfill a binding from attests or artifacts.
- This spec does not add spec storage, artifact resolution, content custody, or a universal
  spec path.
- This spec does not add a clear-binding operation. A caller replaces a stale binding with
  a reviewed successor.
- This spec does not change title, body, `isBug`, ownership, assignment, bracket, state, or
  disposition behavior.
- This spec does not expose spec-reference flags through the body-only
  `work-item-update` CLI command defined by `specs/tightbeam/editable-work-item-body.md`.
- This spec does not grant authority from an assignment, role name, archetype, creator
  session, or repository topology.
- This spec does not add an idempotency key, edit lease, merge algorithm, or automatic
  retry.
- This spec does not add a new history read verb. `work-item-trace` carries binding history.
- This spec does not add a permanent whole-guidance regex rail. The release performs and
  records one bounded command-catalog sweep. A global parser for prose would create false
  positives and fails the red-tape test (wisdom 4).
- This spec does not implement, review, integrate, merge, release, deploy, restart, or
  mutate 0.1.8 or T1778.

Declined alternatives:

- Restoring the generic `work-item-update --spec-ref ...` CLI is declined because the
  main-era body contract reserves that command for body-only forms and rejects metadata
  flags.
- Keeping raw spec-reference writes beside a new command is declined because those writes
  bypass authorization, compare-and-swap, and correction history.
- A new work item for each spec revision is declined because it breaks one-work-item,
  many-assignments continuity.
- An admin-only database repair is declined because the required exit must be
  agent-reachable.

## Terms

- **Spec binding**: The pair `work_items.specRefName` and
  `work_items.specRefSha256`. The pair identifies the spec that currently governs one
  work item. Both values are null or both values are non-null.
- **Desired pair**: The non-null spec name and SHA-256 that the caller asks the substrate
  to store.
- **Expected pair**: The pair that the caller read before it asks for a change. It is
  either the explicit unbound pair `{null, null}` or one valid non-null name and digest.
- **Initial bind**: A changed transition from `{null, null}` to a desired pair.
- **Rebind**: A changed transition from one non-null pair to a different non-null pair.
- **Same-value replay**: A request whose desired pair equals the stored pair. It succeeds
  without a field write, history row, metadata doorbell, or state notice.
- **Stale write**: A request whose desired pair differs from the stored pair and whose
  expected pair does not equal the stored pair.
- **Binding history**: Append-only rows that record changed transitions after this
  capability activates. It does not claim to reconstruct changes made by an older build.
- **Authorized principal**: The work item's owner user, a session owned by that user, an
  admin user, or a session owned by an admin user. The wire router supplies the resolved
  user or session principal.
- **Owner-visible not-found**: The common response for an unknown item and an item the
  principal does not own or administer. This response hides item existence.
- **Open item**: A work item whose durable `state` is exactly `open` at the binding
  transaction.
- **Directive-form command example**: A fenced, indented, or inline code fragment in served
  guidance whose first two tokens are `tightbeam <verb>`. Prose such as “tightbeam refuses”
  is not a command example.

## Assumptions

A1. At the inspected 0.1.9 and 0.2.0 revisions, the `work_items` table already enforces
the null-or-non-null pairing and validates a nonblank name plus a 64-character lowercase
hexadecimal SHA-256.

A2. At both inspected revisions, the wire router and gateway already route the raw
`work-item-update` verb, and `Tightbeam.WorkItems` accepts metadata patches that can change
the spec pair. The Rust CLI exposes no `work-item-update` command.

A3. At both inspected revisions, the served
`priv/kungfu/agentic-engineering/skills/spec-homing/SKILL.md` directs a rebind through the
absent metadata update command.

A4. At inspected 0.2.0 main, `priv/guidance/operating-manual.md` also names the absent
singular `tightbeam decision-request --request <id>` command. The CLI exposes
`decision-requests` but no singular command. The inspected 0.1.9 manual does not contain
that singular example.

A5. The main-era editable-body spec reserves the `work-item-update` CLI grammar for body
replacement and clear. It keeps raw metadata updates only as a compatibility baseline.
This spec supersedes that baseline only for `specRefName` and `specRefSha256`; title,
`isBug`, and body clauses remain in force.

A6. `work-item-brackets-v1.md` supplies the current owner and state semantics.
`work-item-v1.md` supplies the caller-computed current-governing-spec meaning where later
specs have not amended it.

A7. The wire router resolves credential identity before the work-item handler runs. A
session principal can be resolved without reading repository paths or assuming a host.

A8. Each product line has a stamped schema and an existing exact-object additive activation
pattern. An older binary refuses a database whose stamp it does not recognize.

A9. The current predecessor stamps are `coordination-fabric-v1-phase1-v5` on inspected
0.2.0 main and `operator-decision-requests-v1` on inspected 0.1.9. If either integration
base has a different stamp, the implementer stops and amends this spec before changing
schema code.

A10. `work-item-trace` already applies owner-or-admin visibility and can add a typed timeline
member without adding a read verb.

A11. The live specimens establish the product need without authorizing row mutation:

- `dr_28841f89-2c23-4a3f-9f24-2e5753f4c434` records the closed gateway-response item's
  reviewed spec and failed binding attempt.
- `wi_a1b6b53b-405a-4438-8c25-c0cd5c8f0c2d` preserves reviewed-clean
  `art_9a78ab0f`, SHA-256
  `9d1a76f1a1af9ece6fcbbb1e2ada94152a3e63c91aa6f6e2554186dcc9f7274e`, behind the
  named blocker `att_fb581ae2-e68d-40d4-946d-91096689b313` and its surrounding
  no-bypass owner ruling.
- `wi_c6589a66-33e2-43f3-ab84-1b21a5b8c6cf` preserves reviewed-clean
  `art_53d5c390`, SHA-256
  `cc856914d0c80eb4c8dc1f807692ad7b7c533f2f9ca666b9a629f76121b77bce`, behind the
  same missing capability.

A12. At inspected 0.2.0 main, accepted transactional work-item verbs publish
`verb.accepted` and a typed state notice through `Tightbeam.Firehose.Publisher`. The
inspected 0.1.9 line has the durable dispatch event log and the owner metadata doorbell,
but it has no firehose publisher or `work_item.updated` class.

## Invariants

I1. The system accepts a desired binding only as one valid name-and-digest pair.

- Acceptance: Given a missing field, blank name, name longer than 2,000 characters,
  uppercase digest, short digest, or nonhex digest, when the handler validates the call,
  then it returns `invalid_spec_ref` and changes no row.

I2. The system accepts an expected binding only as `{null, null}` or one valid non-null
name-and-digest pair, with both expected keys present on the wire.

- Acceptance: Given one missing expected key, a mixed null/non-null pair, or a malformed
  expected value, when a raw caller submits the request, then it returns
  `invalid_expected_spec_ref` and changes no row.

I3. The binding command applies only to an open item.

- Acceptance: Given an authorized item in `iceboxed`, `closed`, or `failed`, when a caller
  submits a valid bind or same-value replay, then it returns `work_item_not_open` and
  preserves the current pair and history count.

I4. The work-item owner or an admin authorizes the binding command.

- Acceptance: Given an owner user, an owner session, an admin user, an admin session, an
  unrelated user, and an unrelated session, when each submits the same valid request, then
  the first four reach state validation and the latter two receive the owner-visible
  `not_found` response.

I5. Roles, assignment membership, creator identity, and archetype names grant no additional
binding authority.

- Acceptance: Given a non-owner session that holds an assignment on the item, when it binds
  through its held role, then it receives `not_found` and writes no history row.

I6. An unknown item and an unauthorized known item have the same response status, code, and
message.

- Acceptance: Given one unknown id and one known id owned by another user, when the same
  principal calls the command, then both responses equal HTTP 404 with
  `{"error":{"code":"not_found","message":"work item not found"}}`.

I7. A changed binding compares the expected pair and writes the desired pair in one
transaction.

- Acceptance: Given current pair P, expected pair P, and desired pair Q, when the command
  succeeds, then one transaction changes both work-item columns to Q and appends one history
  row from P to Q.

I8. A stale writer changes no substrate state.

- Acceptance: Given current pair Q, expected pair P, and desired pair R where P, Q, and R
  differ, when the command runs, then it returns HTTP 409 `stale_spec_binding`; pair Q,
  history, doorbells, and state notices remain unchanged.

I9. A same-value replay succeeds before the expected-pair comparison, provided the item is
still open.

- Acceptance: Given a first call that changes P to Q and a repeated call that still expects
  P and desires Q, when the repeated call runs on the open item, then it returns success with
  `changed: false`, `cause: "same_value"`, and `historySeq: null`; it writes no row and emits
  no metadata doorbell or state notice.

I10. The update statement reasserts the open state and prior pair as compare-and-swap
predicates.

- Acceptance: Given an injected interleaving that changes the state or pair after the
  handler's first read but before its update, when the update statement runs, then it
  changes zero rows, the handler re-reads in the transaction, and it returns
  `work_item_not_open` or `stale_spec_binding` from the re-read truth.

I11. Each changed binding appends one history row with the prior pair, next pair, derived
cause, resolved principal, and commit time.

- Acceptance: Given an initial bind by session S followed by a rebind by user U, when the
  owner reads `work-item-trace`, then it contains two ordered `spec_binding` members. The
  first carries `initial_bind`, S, and a null prior pair. The second carries `rebind`, U,
  and the first binding as its prior pair.

I12. The history table records only post-activation changed bindings and does not invent
legacy provenance.

- Acceptance: Given an upgraded item that already carries pair P and has no history row,
  when the owner reads its trace, then the history list is empty. When the owner changes P
  to Q, one `rebind` row records P and Q.

I13. The dedicated command is the one mutation seam for spec bindings after activation.

- Acceptance: Given a raw `work-item-update` request containing `specRefName`,
  `specRefSha256`, or either field beside a title, `isBug`, or body field, when the handler
  receives it, then it returns `spec_binding_command_required` before any metadata or body
  write.

I14. Metadata updates that omit both spec-reference fields keep their prior behavior.

- Acceptance: Given title-only, `isBug`-only, body-only, and body-clear requests, when each
  runs after activation, then each follows its governing contract and preserves the spec
  pair and binding history.

I15. The substrate records the authenticated principal, not a caller-authored origin string,
for a changed binding.

- Acceptance: Given a session credential that the router lawfully resolves to user U through
  `--as-user U`, when the command changes a binding, then the history row stores
  `changedByUser=U` and `changedBySession=null`; the accepted verb audit stores principal
  `user:U`.

I16. Binding history follows work-item-trace owner-or-admin visibility. The 0.2.0 binding
state notice follows the same owner-or-admin visibility.

- Acceptance: Given a changed binding containing a unique spec-name sentinel, when the
  owner, an admin, and an unrelated user read binding history, then only the owner and admin
  can observe the history. When the same principals subscribe to the 0.2.0 firehose, only
  the owner and admin receive the binding state notice. Existing current-work-item read
  visibility does not change.

I17. The audit payload records bounded binding descriptors and does not copy spec content.

- Acceptance: Given a successful change and each refusal class, when event rows are read in
  a test, then each row carries verb, result code, work-item id, resolved principal, and
  cause when known. A successful row carries prior and next SHA-256 plus `changed`; no row
  contains bytes read from a referenced file.

I18. On both lines, a changed binding emits one existing `metadata` doorbell after commit.
On 0.2.0, it also emits one owner-visible `work_item.updated` state notice after commit.
The 0.1.9 implementation does not add a firehose subsystem. A same-value replay emits no
doorbell or state notice.

- Acceptance: Given one changed call followed by one same-value replay, when event and
  notice fixtures are counted, then each line contains one new metadata doorbell and two
  verb-attempt audit rows. The 0.2.0 fixture also contains one new state notice. The 0.1.9
  fixture contains no binding state-notice class.

I19. Spec-reference creation behavior stays compatible.

- Acceptance: Given `work-item-create --spec-ref N --spec-sha256 H`, when the command runs on
  either line, then it stores N and H under the existing pairing rule and creates no binding
  history row. A later rebind records the creation pair as its prior pair.

I20. Guidance ships with the capability it teaches.

- Acceptance: Given a build before the new command lands, when guidance is assembled, then
  it retains no premature new command directive. Given the implementation commit for a
  target line, the same commit changes that line's spec-homing directive to the exact new
  syntax.

I21. The release sweep corrects each confirmed absent directive in scope.

- Acceptance: Given the inspected 0.1.9 tree, when the bounded sweep runs, then it reports
  only the spec-homing metadata-update directive as confirmed absent and replaces it. Given
  the inspected 0.2.0 tree, it also reports the singular `decision-request` example and
  replaces that example with the existing plural read command.

I22. The implementation uses no host, Main-session key, repository checkout path, or role
name as a binding authority or destination.

- Acceptance: Given two org fixtures with different users, session keys, roles, and hosts,
  when the same owner/admin cases run, then their outcomes depend only on authenticated
  principal, work-item owner, item state, and binding values.

## Architecture

### 1. Authority and supersession

This spec adds `work-item-bind-spec` and makes it the exclusive post-create mutation seam
for `specRefName` and `specRefSha256`.

It supersedes these older clauses only where they conflict:

- `work-item-v1.md`: the `work-item-update` spec-patch grammar, partial-pair patch rules,
  clear operation, any-principal authorization for spec changes, no-CAS rule, and no-history
  rule.
- `observability-v1.md`: the spec-pin metadata emission site moves from
  `work-item-update` to `work-item-bind-spec`.
- `specs/tightbeam/editable-work-item-body.md`: Assumption A3 and the raw-metadata
  compatibility clauses remain true for title and `isBug`, but raw spec-reference fields
  now return `spec_binding_command_required`. Its body-only CLI grammar and body behavior
  remain unchanged.

The current-governing-spec meaning, caller-computed digest, create-time binding, body/spec
separation, owner/state semantics, and existing work-item projections remain in force.

### 2. Durable representation

Each line adds this exact table:

```sql
CREATE TABLE work_item_spec_binding_history (
  seq                   INTEGER PRIMARY KEY AUTOINCREMENT,
  workItemId            TEXT NOT NULL REFERENCES work_items(id),
  priorSpecRefName      TEXT,
  priorSpecRefSha256    TEXT,
  nextSpecRefName       TEXT NOT NULL
                        CHECK(length(trim(nextSpecRefName)) BETWEEN 1 AND 2000),
  nextSpecRefSha256     TEXT NOT NULL
                        CHECK(length(nextSpecRefSha256) = 64 AND
                              nextSpecRefSha256 NOT GLOB '*[^0-9a-f]*'),
  changedByUser         TEXT REFERENCES users(userId),
  changedBySession      TEXT REFERENCES sessions(sessionKey),
  changedAt             INTEGER NOT NULL CHECK(changedAt >= 0),
  cause                 TEXT NOT NULL CHECK(cause IN ('initial_bind','rebind')),
  CHECK((priorSpecRefName IS NULL) = (priorSpecRefSha256 IS NULL)),
  CHECK(priorSpecRefName IS NULL OR
        length(trim(priorSpecRefName)) BETWEEN 1 AND 2000),
  CHECK(priorSpecRefSha256 IS NULL OR
        (length(priorSpecRefSha256) = 64 AND
         priorSpecRefSha256 NOT GLOB '*[^0-9a-f]*')),
  CHECK((changedByUser IS NOT NULL) != (changedBySession IS NOT NULL)),
  CHECK((cause = 'initial_bind' AND priorSpecRefName IS NULL) OR
        (cause = 'rebind' AND priorSpecRefName IS NOT NULL)),
  CHECK(priorSpecRefName IS NULL OR
        priorSpecRefName != nextSpecRefName OR
        priorSpecRefSha256 != nextSpecRefSha256)
);
CREATE INDEX work_item_spec_binding_history_item
  ON work_item_spec_binding_history(workItemId, seq);
```

Each line also adds this activation marker:

```sql
CREATE TABLE work_item_spec_binding_activation (
  id          INTEGER PRIMARY KEY CHECK(id = 0),
  activatedAt INTEGER NOT NULL CHECK(activatedAt >= 0),
  cause       TEXT NOT NULL CHECK(cause = 'schema_activation'),
  principal   TEXT NOT NULL CHECK(principal = 'process:tightbeam')
);
```

The activation transaction creates the history table, index, activation table, and row
`(0, now, 'schema_activation', 'process:tightbeam')`. It updates the line-specific schema
stamp in that transaction. It validates the exact object set on later boots. A partial,
duplicate, malformed, or wrongly stamped set raises
`incompatible_work_item_spec_binding_v1` before a gateway accepts requests.

Both `activatedAt` and `changedAt` store nonnegative Unix epoch milliseconds.

The activation performs no work-item update and no history backfill. The 0.2.0 successor
stamp is `coordination-fabric-v1-phase1-v6`. The 0.1.9 successor stamp is
`operator-decision-requests-v1-spec-binding-v1`. A changed predecessor requires a spec
amendment, not an inferred migration.

### 3. Mutation transaction

`Tightbeam.WorkItems` remains the work-item mutation owner. Its dedicated handler performs
this order:

1. Require a user or session principal. Preserve transport-first credential refusals.
2. Resolve the id through an owner-or-admin visibility predicate. Return the common
   `not_found` response when resolution fails.
3. Require `state='open'`.
4. Validate the desired pair and the present expected pair.
5. If the stored pair equals the desired pair, return the same-value response. On 0.2.0,
   queue the accepted firehose observation without a state notice.
6. Compare the stored pair with the expected pair. Return `stale_spec_binding` on mismatch.
7. Run one `UPDATE work_items SET specRefName=?, specRefSha256=? WHERE id=? AND state='open'
   AND specRefName IS ? AND specRefSha256 IS ?` statement.
8. Require exactly one changed row. On zero rows, re-read and classify the result as
   `work_item_not_open` or `stale_spec_binding`.
9. Append one history row in the same transaction. Derive `initial_bind` from a null prior
   pair and `rebind` from a non-null prior pair. Stamp the resolved user or session
   principal and the transaction time.
10. On 0.2.0, queue the accepted firehose observation and owner-visible state notice through
    the existing transaction-aware publisher seam. On both lines, commit before the
    metadata callback runs. Preserve each line's existing dispatch event-audit semantics.

Raw `work-item-update` rejects a request containing either spec-reference field before it
applies title, `isBug`, or body changes. No private helper, router alias, admin command, or
legacy CLI path writes the pair after activation.

### 4. Wire and CLI

The CLI grammar is:

```text
tightbeam work-item-bind-spec <workItemId> \
  --spec-ref <name> --spec-sha256 <64-lowercase-hex> \
  (--expect-unbound | \
   --expect-spec-ref <current-name> --expect-spec-sha256 <current-64-lowercase-hex>)
```

The command accepts at most one existing identity selector. It accepts no target, key,
clear, title, `isBug`, or body flag. The exact usage text is the one-line form:

```text
usage: tightbeam work-item-bind-spec <workItemId> --spec-ref <name> --spec-sha256 <hex> (--expect-unbound | --expect-spec-ref <name> --expect-spec-sha256 <hex>)
```

An unbound request sends:

```json
{"verb":"work-item-bind-spec","params":{"workItemId":"wi_1","specRefName":"spec.md","specRefSha256":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","expectedSpecRefName":null,"expectedSpecRefSha256":null}}
```

A rebind request sends the same object with non-null expected fields. The existing identity
field precedes `verb` when one is present. The router atomizes the five parameters and strips
none of them.

A changed result is:

```json
{
  "workItem": {"id":"wi_1","specRefName":"spec.md","specRefSha256":"<hex>"},
  "specBinding": {
    "changed": true,
    "cause": "initial_bind",
    "historySeq": 1,
    "previous": {"specRefName":null,"specRefSha256":null},
    "current": {"specRefName":"spec.md","specRefSha256":"<hex>"}
  }
}
```

The `workItem` member uses the existing complete public work-item shape. A same-value result
uses that shape and returns `changed:false`, `cause:"same_value"`,
`historySeq:null`, and identical `previous` and `current` pairs.

On both lines, register the verb in the wire agent-verb set, gateway handler table, CLI
command enum, parser, request builder, help, unknown-command roster, and statute verb
inventory. On 0.2.0, also register it in the transaction-aware publisher set and map it to
the existing `work_item.updated` class. Do not add an alias or a new 0.1.9 state-notice
class.

### 5. Trace, audit, and visibility

`work-item-trace` adds one timeline member for each history row, ordered by `changedAt` and
then `seq`:

```json
{
  "type":"spec_binding",
  "id":1,
  "at":1780000000000,
  "cause":"rebind",
  "principal":{"kind":"session","id":"agent:spec-writer:x s_1"},
  "previous":{"specRefName":"spec.md","specRefSha256":"<old>"},
  "current":{"specRefName":"spec.md","specRefSha256":"<new>"}
}
```

The trace's existing owner-or-admin authorization applies. On 0.2.0, the state notice uses
existing work-item visibility. This spec does not narrow the existing visibility of the
current pair in `work-item-get`, `work-item-list`, or their state projections.

The changed-binding history row is the atomic principal audit. Each line's durable dispatch
event remains the attempt audit and stores its existing resolved-principal columns. Add a
verb-specific event projection so a successful attempt stores only work-item id, result
code `ok`, changed flag, cause, prior SHA-256, and next SHA-256. A refused attempt stores
only requested work-item id and result code. The projection does not change the response
envelope. It does not store spec names, the complete work-item result, or referenced
content. An unauthorized refusal stores no current or prior pair.

The metadata doorbell remains a bare change edge. The history row carries cause and
principal (wisdom 5); the substrate does not infer why a spec was chosen (wisdom 6).

### 6. Failure contract

| Condition | Result | HTTP |
| --- | --- | --- |
| CLI shape, flag, or desired/expected pairing error | exact usage; no request | — |
| Unknown or unauthorized item | `not_found`: `work item not found` | 404 |
| Item state is not `open` | `work_item_not_open`: `spec binding requires an open work item` | 409 |
| Desired pair missing, null, mixed, nontext, blank, overlong, uppercase, short, or nonhex | `invalid_spec_ref`: `spec ref must be a non-blank name and lowercase sha256` | 400 |
| Expected keys missing, mixed, or malformed | `invalid_expected_spec_ref`: `expected spec ref must be an explicit unbound pair or a valid name and lowercase sha256` | 400 |
| Desired differs and expected pair is stale | `stale_spec_binding`: `work item spec binding changed; read the item and retry with its current pair` | 409 |
| Raw metadata update contains a spec field | `spec_binding_command_required`: `use work-item-bind-spec to change a spec binding` | 400 |
| Process principal reaches handler | `process_denied`: `process principals cannot use work-item verbs` | 403 |
| Missing handler principal | `principal_required`: `work-item verbs require a user credential or a session token` | 403 |
| Session credential asserts another identity | existing router refusal | existing status |
| Malformed or partial activation objects | boot raises `incompatible_work_item_spec_binding_v1` | — |
| Unexpected handler failure | existing `server_error` envelope | 500 |

The router adds HTTP 409 mappings only for `work_item_not_open` and
`stale_spec_binding`. Error responses keep the existing
`{"error":{"code":...,"message":...}}` shape.

### 7. Compatibility, migration, and rollback

Upgrade from each exact predecessor stamp is additive to work-item data. The migration
creates the sidecar objects and changes the stamp in one transaction. A failure rolls back
the objects, activation row, and stamp. Existing `work_items` bytes remain unchanged.

Fresh databases create the sidecars with the target stamp. Upgraded databases start with an
empty history. Existing non-null pairs remain readable and become the prior pair of their
first changed rebind.

An older binary refuses the successor stamp. This refusal prevents an older raw metadata
handler from bypassing the exclusive binding seam.

Rollback has two states:

1. Before the first history row, the release rollback is permitted to drop the empty sidecar objects and
   restore the exact predecessor stamp in one reviewed transaction.
2. After one history row exists, destructive rollback is prohibited. Keep the successor
   binary or ship a forward fix. Retaining the tables while restoring the old stamp would
   permit unaudited writes and is not a rollback.

The 0.1.9 and 0.2.0 migrations, binaries, guidance, and release evidence remain line-local.
No command assumes which host runs either line.

### 8. Guidance correction and bounded sweep

On both lines, replace the spec-homing rebind sentence with this directive after the command
exists:

> After independent review clears the spec, bind an unbound open item with
> `tightbeam work-item-bind-spec <workItemId> --spec-ref <name> --spec-sha256 <hex> --expect-unbound`.
> Rebind a changed spec with the same command plus
> `--expect-spec-ref <currentName> --expect-spec-sha256 <currentHex>`. If the command reports
> a stale binding, read the item and decide whether the new current pair already governs it.

On 0.2.0 main, replace the operating-manual sentence
`Read the answer with tightbeam decision-requests or tightbeam decision-request ...` with
`Read answers with tightbeam decision-requests.` No 0.1.9 edit is needed for that sentence.

The release evidence enumerates directive-form command examples under `priv/guidance`,
`priv/seed`, and `priv/kungfu`, then compares each verb with the exact built CLI catalog for
that line. It records file, line, verb, and result. Prose matches are excluded by the term's
syntax rule. The sweep is evidence for this incident closure, not a new runtime subsystem.

### 9. Traceability and verification

| Requirements | Implementation seams | Verification |
| --- | --- | --- |
| I1-I10, I13-I15 | `lib/tightbeam/work_items.ex` | `test/work_items_test.exs` |
| I11-I12, I16 | history activation plus `lib/tightbeam/job_trace.ex` | schema-shape and job-trace tests |
| I15, I17-I18 | history, dispatch audit, work-item callback; 0.2.0 publisher | dispatch and visibility tests on both lines; 0.2.0 firehose tests |
| I3-I6 | router identity plus work-item authorization | router and CLI-integration tests |
| I19 | existing create seam | create regression tests |
| I20-I21 | two spec-homing copies; 0.2.0 operating manual | packaging assembly plus SHA-bound sweep report |
| I22 | no topology input | two-org fixtures |
| Wire and CLI | router, gateway, `cli/src/args.rs`, `cli/src/dispatch.rs` | Rust byte fixtures and real CLI integration |
| Migration and rollback | line-specific `Tightbeam.Schema` | exact predecessor, fresh, interrupted, malformed, old-binary, and rollback fixtures |

Each implementation line must run its repository-defined clean baseline and exact-candidate
gates. Build the release CLI before the reality smoke. The smoke uses a fresh file-backed
org and the built binary; it creates an unbound item, binds it, repeats the same call,
rebinds it, drives a stale writer, restarts the gateway, reads the item and trace, and proves
teardown. Capture the real JSON responses as fixtures. Do not use a hand-written ideal
fixture for CLI or wire acceptance (wisdom 24).

## Acceptance

AC1 — Initial bind:

- Given an open unbound item owned by U,
- When U's session submits a valid desired pair and explicit unbound expectation,
- Then both columns change together, one `initial_bind` history row names that session, and
  get plus trace return the committed values.

AC2 — Reviewed-spec rebind:

- Given an open item bound to P,
- When U submits desired Q with expected P,
- Then the item changes to Q, one `rebind` row records P and Q, and P remains in history.

AC3 — Lost-response replay:

- Given AC2 committed but its response was lost,
- When U repeats desired Q with expected P while the item remains open,
- Then the call succeeds as `same_value` and adds no history, doorbell, or state notice.

AC4 — Stale writer:

- Given writers A and B read P,
- When A commits Q and B submits R with expected P,
- Then B receives HTTP 409 `stale_spec_binding`, Q remains current, and no B mutation row
  exists.

AC5 — State race:

- Given the item is open at the first read,
- When a disposition changes it before the binding CAS,
- Then the CAS changes zero rows and the command returns HTTP 409
  `work_item_not_open` without history.

AC6 — Authorization and privacy:

- Given owner, admin, unrelated, assignment-holder-only, and unknown-item cases,
- When each calls the command and reads trace,
- Then only owner and admin cases observe or change binding truth; unauthorized and unknown
  command responses are byte-equal not-found envelopes.

AC7 — Pair validation:

- Given the complete desired and expected validation matrix,
- When CLI and raw-wire tests run,
- Then valid pairs reach the transaction; missing, mixed, blank, uppercase, short, long, and
  nonhex cases return their exact usage or typed error without writes.

AC8 — Exclusive seam:

- Given a request through raw `work-item-update` with one or two spec fields, alone or mixed
  with title, `isBug`, or body,
- When the request runs,
- Then it returns `spec_binding_command_required` before any work-item or body write. Metadata
  calls without spec fields retain their prior results.

AC9 — Upgrade and old-binary refusal:

- Given one database at each exact predecessor stamp with unbound and bound items,
- When the successor migrates it,
- Then item bytes remain fixed, the validated sidecars and target stamp appear atomically,
  and history starts empty. When the predecessor binary opens the successor database, it
  refuses the unknown stamp before serving a mutation.

AC10 — Rollback boundary:

- Given a migrated database with zero history rows,
- When the reviewed rollback transaction runs,
- Then it removes only the empty sidecars and restores the predecessor stamp. Given one
  history row, the same rollback refuses and preserves the successor state.

AC11 — Wire, CLI, audit, and restart reality:

- Given a fresh file-backed org and the exact built CLI,
- When the smoke performs initial bind, same-value replay, rebind, stale write, gateway
  restart, get, and trace,
- Then captured real responses match the exact grammar and envelopes, history survives the
  restart, principal audit is correct, line-specific counts match I18, and teardown succeeds.

AC12 — Guidance on both product lines:

- Given the exact candidate for 0.1.9 and the exact candidate for 0.2.0,
- When packaging assembles served identity and the bounded command-catalog sweep runs,
- Then both spec-homing copies teach `work-item-bind-spec`; neither teaches metadata
  `work-item-update`; the 0.2.0 manual no longer teaches singular `decision-request`; and
  each recorded directive verb exists in that candidate's CLI catalog.

AC13 — Specimen reconciliation without live mutation:

- Given the reviewed artifact tuples on closed `wi_f2281739` and open
  `wi_a1b6b53b` plus `wi_c6589a66`,
- When an independent reviewer evaluates this contract,
- Then the closed item remains immutable and its attest chain remains the historical evidence
  of the missing capability. After the applicable line ships, each open item can use the
  same command with an explicit current expectation. The spec production and review stages
  perform no bind.

AC14 — Scope and substrate boundary:

- Given a desired spec pair that names a missing file, an unreviewed file, or a file on a
  different host,
- When an authorized owner submits it with a matching expected pair,
- Then the substrate records the pair without fetching or judging the file. Agent guidance
  remains responsible for review and selection.

## Open Questions

None. The independent reviewer can return findings against this exact revision. A finding
amends this canonical file before implementation authority can be issued.
