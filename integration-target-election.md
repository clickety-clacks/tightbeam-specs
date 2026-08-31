# Integration-target election and landing refusal

## Goal

Give each participating product or repository a policy-owned destination registry. Bind each
participating work item and managed landing to exactly one registry. Give the work item a
durable, owner-authorized integration-target election that the substrate checks at the
integration outcome. The election makes one or more destinations explicit; the substrate
refuses a landing that has no matching election, registry, and destination.

Tightbeam is the first pilot. This replaces the convention-and-attest-registry practice and
also represents a separately scoped registry for the ClipMesh ruling. It realizes the
branch-authority rulings represented by
`dr_b18fef87-82ff-4893-8882-24e5d096736b`,
`dr_4ecad888-39dc-4e7c-8080-21cfb064249d`,
`dr_2e105899-339d-4ff2-a9bd-d89a1683c16d`, `att_21d12c0b`, and
`dr_70bdfcbf-76a6-42ed-aa60-28617b0e3fcd` without inferring a target from any
branch, commit, review, spec, or nearby work.

## Non-Goals

- Choose an integration target for an untargeted work item, including
  `wi_eb6f8d36-0c9e-436f-8a62-b76f1190b021`.
- Merge, push, release, deploy, or operate Git itself.
- Change the artifact identity contract of `specRefName` and `specRefSha256`.
- Make Tightbeam `0.1.8` a destination. The superseding release authority locks it.
- Infer, create, retire, or rank destination lines from repository state.
- Create a second review, approval, or decision authority in kungfu guidance.
- Backfill an election or destination selection for an existing work item.
- Make a registry display name or scope reference an integration authorization.

## Terms

- **Registry**: one stable policy row for one product or repository scope. It has an opaque
  registry ID, an explicit `product` or `repository` scope reference, one policy-owner role,
  and a pointer to one current immutable registry version. Registry equality is
  ID equality; the substrate does not derive it from a Git remote, branch, work-item title,
  assignment, or spec.
- **Registry version**: one immutable ordered version of a registry. It names the release-line
  authority reference and SHA-256 and contains the current set of live destination entries.
- **Destination entry**: one opaque destination ID plus a display name. The ID is stable while
  the destination remains in later versions of the same registry. The display name explains
  the entry to an operator; it neither identifies a registry nor authorizes a landing.
- **Election**: one immutable record that selects either `hold` or a canonical non-empty set
  of destination IDs from one frozen registry version for one work item.
- **No election**: the work item has no current election record. It is distinct from `hold`.
- **Hold**: an explicit election whose selected destination set is empty.
- **Election revision**: a positive integer assigned in order per work item. It supports
  compare-and-swap (CAS) and preserves superseded election history.
- **Election decision request (DR)**: the only DR subtype that can produce an election. It
  carries the work item, its registry ID, an expected election revision, a frozen registry
  version, and a structured selection of either hold or a subset of that version.
- **Delegation grant**: a durable, scoped authority from Mike to one principal to resolve an
  election DR. The grant identifies its grantor, grantee, work-item scope, creation time,
  revocation state, and cause.
- **Landing**: a Tightbeam-managed integration outcome. It names one work item, the same
  registry ID carried by that work item, and one destination ID. `integration-land` is its
  outcome verb.
- **specRef**: the paired `specRefName` and `specRefSha256` work-item fields. They identify
  an artifact revision; they do not authorize a registry or destination.

## Assumptions

- Mike remains the owner authorized to grant or revoke an election delegation and to create
  a registry. An existing registry's recorded policy-owner role owns its version-update and
  work-item-binding seams. The session that acts through that role remains the attributed
  principal.
- Each participating product or repository has one authoritative current registry row.
  Policy supplies its versions through the mutation seam in this spec. The substrate reads
  those rows; it does not parse release prose or inspect branches.
- The first policy setup after this capability ships creates the Tightbeam pilot registry with
  repository scope
  `github.com/clickety-clacks/tightbeam`, policy owner
  role `product-owner:tightbeam`, and initial authority `CONTRIBUTING.md` at Tightbeam commit
  `8e258b579d1170c1f3c7d71ac2c0f76f5d29431b`, SHA-256
  `8d227f279a1ef60a5dcae8c711e6a4a5cf4ed54eaae327a3768bd581730642ec`.
  Its initial live display names are `main`, `0.2.0`, and `0.1.9`; it omits locked `0.1.8`.
- A future integration mechanism can route each Tightbeam-managed landing through
  `integration-land`; a direct Git operation outside Tightbeam is outside this substrate
  contract.
- `operator-rule` remains the durable operator-ruling transaction. This feature extends its
  election-DR surface with a typed election selection and idempotency key. Ordinary DRs
  retain the current label-or-response surface.

## Invariants

1. A work item has exactly one current election state: no election, a `hold` election, or a
   `destinations` election. A `destinations` election contains one or more distinct,
   canonical destination IDs. A `hold` election contains zero destination IDs.
2. Only Mike, or the grantee of an active delegation grant scoped to the work item, can rule
   an election DR. The registry policy owner, product owner, work-item owner, reviewer, and
   spec author do not gain election authority unless Mike grants it durably.
3. An election DR presents `hold` plus each destination in its frozen registry version. Its
   structured selection is either `hold` or a non-empty subset of those destination IDs. The
   substrate rejects any other ID and rejects a selection that combines `hold` with a
   destination. A multi-destination election records N destination IDs from that one registry.
4. The substrate commits the DR ruling, immutable election row, work-item current-election
   pointer, work-item election revision, and audit events in one database transaction. A
   failed transaction changes none of them.
5. The transaction succeeds only when the DR's expected election revision equals the work
   item's current revision and the DR registry ID equals the work item's registry ID. A stale
   request stays unresolved and returns `stale_integration_target_election`.
6. Repeating the same resolved DR with the same outcome idempotency key, typed selection, and
   rationale returns the recorded election. Reusing that key with a different selection or
   rationale returns `integration_target_idempotency_conflict`. A different key submitted
   after the DR resolves returns `integration_target_election_already_resolved`. No replay or
   collision creates a second election or ruling.
7. A later valid election supersedes the former current election in the same transaction.
   The successor stores the predecessor election ID. The former immutable row stays
   unchanged, and history derives its successor by the later row's predecessor link and
   revision. Revoking a delegation grant prevents future rulings; it does not silently
   change an election already recorded.
8. `integration-land` accepts a landing only when the request registry ID equals the work
   item's registry ID, the work item has a current `destinations` election containing the
   supplied destination ID, and that ID appears in the registry's current version. It refuses
   a missing work-item registry with `integration_target_registry_missing`, a registry
   mismatch with `integration_target_registry_mismatch`, no election with
   `integration_target_missing`, hold with `integration_target_hold`, an absent destination
   with `integration_target_absent`, and a retired destination with
   `integration_target_obsolete`.
9. A multi-destination election authorizes each listed destination independently. A landing
   at one listed destination neither consumes nor broadens authorization for another.
10. One transaction reads the work-item registry binding, current election pointer, and
    current registry-version pointer, applies the landing guard, and writes either the
    accepted landing receipt or the refused-landing event. The guard is not a preflight
    endpoint and cannot be separated from the outcome it permits.
11. `specRef` remains independent. A registry binding or election never writes, clears,
    validates, or derives `specRef`; a specRef update never writes, clears, validates, or
    derives a registry binding or election.
12. Each registry creation, registry version update, work-item registry binding, election,
    delegation grant, revocation, supersession, accepted landing, and refused landing records
    an actor principal and cause. Registry update and binding events also name the authorizing
    policy-owner role. Election events name the DR and frozen registry version. Landing events
    name the work item, registry, destination, current election revision when present, outcome
    or refusal code, and caller principal.

## Architecture

### Durable model and state ownership

Add these records and fields:

- `integration_target_registries`: stable rows with `id`, `scopeKind` (`product` or
  `repository`), `scopeRef`, `policyOwnerRole`, `currentVersionId`,
  `currentVersionNumber`, `createdByPrincipal`, `cause`, and `createdAt`. The pair
  `(scopeKind, scopeRef)` is unique. The registry ID has no encoded product, repository,
  branch, or version meaning.
- `integration_target_registry_versions`: immutable rows with `id`, `registryId`,
  `versionNumber`, `authorityRef`, `authoritySha256`, `predecessorVersionId`,
  `changedByPrincipal`, `authorizingPolicyOwnerRole`, `cause`, and `createdAt`.
  `(registryId, versionNumber)` is unique.
- `integration_target_registry_destinations`: immutable identity rows with `id`, `registryId`,
  `displayName`, `createdByPrincipal`, `cause`, and `createdAt`. `(registryId, id)` is unique.
  A retired ID remains in this table and cannot become live again.
- `integration_target_registry_version_destinations`: immutable membership rows with
  `registryId`, `registryVersionId`, and `destinationId`. The composite foreign keys require
  the version and destination to belong to that registry. The three fields form the primary
  key, so one version cannot contain a destination twice.
- `integration_target_election_requests`: one immutable extension row per election DR with
  `decisionRequestId`, `workItemId`, `registryId`, `expectedElectionRevision`,
  and `registryVersionId`. The standard DR options are a deterministic projection of that
  immutable version: one `{kind:"hold"}` entry plus one
  `{kind:"destination", destinationId, displayName}` entry for each member ordered by
  destination ID.
- `integration_target_elections`: immutable rows with `id`, `workItemId`, `revision`,
  `mode` (`hold` or `destinations`), canonical `destinationIds`, `decisionRequestId`,
  `registryId`, `registryVersionId`, `predecessorElectionId`, `idempotencyKey`,
  `electedByPrincipal`, `delegationGrantId`, `cause`, and `createdAt`.
- `integration_target_delegations`: immutable grant identity and scope plus revocation fields.
  Grant and revoke mutations are Mike-only and append attributed audit events.
- `integration_target_landing_receipts`: immutable accepted-outcome rows with `id`,
  `workItemId`, `registryId`, `destinationId`, `landingRef`, `electionId`,
  `electionRevision`, `currentRegistryVersionId`, `idempotencyKey`, `principal`, `cause`, and
  `createdAt`. `(workItemId, idempotencyKey)` and
  `(registryId, destinationId, landingRef)` are unique.
- nullable `work_items.integrationTargetRegistryId`, nullable
  `work_items.integrationTargetElectionId`, and non-null
  `work_items.integrationTargetElectionRevision`, initialized to `NULL`, `NULL`, and `0`.

The absent election pointer at revision 0 represents no election. A current election row
represents either hold or destinations. Database constraints enforce the mode/set pairing,
uniqueness of `(workItemId, revision)`, one result per DR, one current pointer per work item,
registry consistency across each DR and election, and canonical unique destination IDs. The
registry-version membership foreign keys make cross-registry and duplicate version entries
unrepresentable.

The substrate accepts destination IDs only through a stored registry version. It contains no
compiled branch-name list, highest-version selection, source-ref heuristic, or parser for
release policy. Registry scope and destination display names remain policy material rather
than substrate topology (wisdom 10).

This adds durable decision and landing records because the requested landing surface must
remain usable when inference is unavailable. Deleting the landing surface would not meet the
requested integration outcome. Accepting an inferred target would retain the failure this
contract closes.

### Registry and work-item scope mutation seams

`integration-target-registry-create --scope-kind <product|repository> --scope-ref <ref>
--policy-owner-role <role> --authority-ref <ref> --authority-sha256 <hex>
--destination <display-name>... --cause <text>` is Mike-only. It generates one opaque
registry ID and one opaque destination ID per supplied display name, inserts registry version
1, advances the current-version pointer, and writes one attributed audit event in a single
transaction. A scope collision returns `integration_target_registry_scope_exists` and the
existing registry ID; it changes no row.

`integration-target-registry-update <registry-id> --expected-version <n>
--authority-ref <ref> --authority-sha256 <hex> --retain <destination-id>...
--add <display-name>... --cause <text>` is the only registry-version mutation seam. Only the
holder of the registry's exact `policyOwnerRole` may call it through that role. The audit
records both the authorizing role and the acting session principal. The requested live set is
the retained current IDs plus newly generated IDs. The command rejects an ID outside the
current version with `integration_target_destination_not_current`, rejects a duplicate ID or
empty authority, and returns `stale_integration_target_registry` on CAS mismatch. It inserts
new destination identities and one immutable version, advances the registry's pointer and
number with CAS, and writes its audit event in one transaction. Failure changes none of those
rows. Removing an ID from the new version retires it without deleting history. A later entry
with the same display name receives a new opaque ID and does not reactivate the retired ID.

`integration-target-bind-registry --work-item <id> --registry <registry-id> --cause <text>`
is the only work-item registry-binding mutation seam. Only the holder of that registry's
`policyOwnerRole` may bind it through that role. It succeeds only when the work-item field is
null, its election revision is 0, and it has no election or landing row. The binding is then
immutable. It records the authorizing role, acting session principal, and cause. New and
existing work items remain unusable for managed landing until this explicit binding occurs;
the substrate never derives one.

`integration-target-registry-get <registry-id>`,
`integration-target-registry-version-get <registry-version-id>`, and
`integration-target-registry-list` return registry material in these shapes:

```json
{
  "id": "<registry-id>",
  "scopeKind": "product|repository",
  "scopeRef": "<policy reference>",
  "policyOwnerRole": "<role>",
  "currentVersionNumber": 1,
  "createdByPrincipal": "user:<id>|session:<key>",
  "cause": "<text>",
  "createdAt": 0,
  "currentVersion": {
    "id": "<registry-version-id>",
    "registryId": "<registry-id>",
    "versionNumber": 1,
    "authorityRef": "<authority reference>",
    "authoritySha256": "<64 lowercase hex>",
    "predecessorVersionId": null,
    "changedByPrincipal": "user:<id>|session:<key>",
    "authorizingPolicyOwnerRole": null,
    "cause": "<text>",
    "createdAt": 0,
    "destinations": [{"id": "<destination-id>", "displayName": "<name>"}]
  }
}
```

Registry get returns the object above. Registry-version get returns the exact
`currentVersion` object shape for the requested historical or current version. Registry list
returns `{"registries":[<registry object>...]}` ordered by registry ID. Destinations are
ordered by destination ID. Registry get and list each run in one read transaction. Registry
get, registry list, DR creation, and landing each read every registry row and its pointed-to
immutable version in one database snapshot; no result can pair a new pointer with an old
version body. `authorizingPolicyOwnerRole` is null for the Mike-created first version and is
the authorizing role string for a policy-owner update. Each `createdAt` value is an integer
Unix epoch in milliseconds.

After the empty schema migration, Mike creates the Tightbeam pilot registry through
`integration-target-registry-create` with the exact scope, policy-owner role, authority, hash,
and display names in Assumptions. This is policy data, not compiled topology. Creating a
ClipMesh registry is a separate Mike-authorized policy action; a ClipMesh display name such as
`0.1.0` cannot collide with a Tightbeam display name because elections and landings carry the
registry ID and opaque destination ID.

### Election and delegation flow

1. `integration-target-ask --work-item <id>` reads the work item's explicit registry binding
   and atomically reads that registry's current version. A missing binding returns
   `integration_target_registry_missing`. The command opens one operator DR with subtype
   `integration_target_election`, the current work-item revision, and the frozen registry
   options. Its standard projection enumerates `hold` plus each registry destination; free
   text and cross-registry IDs are invalid.
2. Mike grants a scoped delegation only with
   `integration-target-delegate --work-item <id> --principal <kind:id> --cause <text>`.
   `integration-target-revoke-delegation <grant-id> --cause <text>` records the revocation.
3. Election DR resolution uses
   `operator-rule <dr-id> (--integration-target-hold | --integration-target <destination-id>...)
   --idempotency-key <opaque-key> --rationale <text>`. The election subtype requires a
   non-empty rationale and stores it as the election cause. `--integration-target` may repeat,
   and the hold flag is exclusive. Inside one transaction, the handler checks the caller's
   Mike-or-active-grantee authority, DR subtype, expected revision, work-item registry binding,
   frozen registry version, typed selection, and idempotency outcome. It records base DR ruling
   `integration_target_election`, stores the typed resolution in the election row, supersedes
   a former current election when present, advances the pointer and revision, and publishes
   attributed audit events. The pre-existing `--decision` and `--response` forms reject an
   election DR.
4. A changed selection needs a new election DR that names the current election revision. A
   withdrawn or stale DR changes no election.

Decision-request reads and lists add these fields for the election subtype:

```json
{
  "subtype": "integration_target_election",
  "integrationTargetElection": {
    "workItemId": "<work-item-id>",
    "registryId": "<registry-id>",
    "expectedElectionRevision": 0,
    "registryVersionId": "<registry-version-id>",
    "options": [{"kind": "hold"}, {"kind": "destination", "destinationId": "<id>", "displayName": "<name>"}],
    "resolution": null
  }
}
```

After resolution, `resolution` is
`{"mode":"hold|destinations","destinationIds":["<id>"],"electionId":"<id>"}`;
hold has an empty `destinationIds` array. The exact election object is:

```json
{
  "id": "<election-id>",
  "workItemId": "<work-item-id>",
  "revision": 1,
  "mode": "hold|destinations",
  "destinationIds": ["<destination-id>"],
  "decisionRequestId": "<decision-request-id>",
  "registryId": "<registry-id>",
  "registryVersionId": "<registry-version-id>",
  "predecessorElectionId": null,
  "idempotencyKey": "<opaque-key>",
  "electedByPrincipal": "user:<id>|session:<key>",
  "delegationGrantId": null,
  "cause": "<rationale>",
  "createdAt": 0
}
```

Hold uses an empty `destinationIds` array. `operator-rule` returns
`{"decisionRequestId":"<id>","election":<exact election object>,"replayed":<boolean>}`.
Existing DR fields remain present; `ruling` is the constant
`integration_target_election` after resolution.

Work-item reads and lists add `integrationTargetRegistryId` and
`integrationTargetElection`. The election field is `null` for no election; otherwise it is
the exact election object above. Existing clients can ignore these additive fields.

### Landing refusal

`integration-land --work-item <id> --registry <registry-id>
--destination <destination-id> --landing-ref <ref> --idempotency-key <opaque-key>
--cause <text>` is the sole Tightbeam outcome verb for a managed landing. It receives one
registry and one destination, never a default. Its handler performs the registry-binding,
current-election, and current-registry checks while inserting the landing outcome receipt.
On refusal it writes the refused-landing event and returns the named refusal code; it creates
no acceptance receipt. A caller must use the receipt to claim a Tightbeam-managed landing.

The handler first looks up `(workItemId, idempotencyKey)`. An exact receipt match returns that
receipt. A receipt whose request fields differ returns
`integration_landing_idempotency_conflict`. With no receipt, the handler applies guard checks
in this order: missing work-item registry, request-registry mismatch, no current election,
hold, destination absent from the elected set, then elected destination absent from the
current registry version. The first failing check determines the single refusal code. The
handler accepts only after each check passes.

A retry with the same `(workItemId, idempotencyKey)` and identical registry, destination,
landing ref, principal, and cause returns the recorded receipt with `replayed:true`. Reusing
that key with different request fields returns `integration_landing_idempotency_conflict`.
An accepted response is:

```json
{
  "receipt": {
    "id": "<receipt-id>",
    "workItemId": "<work-item-id>",
    "registryId": "<registry-id>",
    "destinationId": "<destination-id>",
    "landingRef": "<ref>",
    "electionId": "<election-id>",
    "electionRevision": 1,
    "currentRegistryVersionId": "<registry-version-id>",
    "idempotencyKey": "<opaque-key>",
    "principal": "user:<id>|session:<key>",
    "cause": "<text>",
    "createdAt": 0
  },
  "replayed": false
}
```

A refused response is
`{"code":"<refusal-code>","refusalEventId":"<event-id>","receipt":null}`.

The implementation must route each existing or new managed integration endpoint through this
handler, rather than copy a target check into callers. The rail therefore fires where both the
condition and action leave rows (wisdom 1), is silent when satisfied (wisdom 4), and leaves a
cause and principal on both legs (wisdom 5). Selection remains an operator judgment;
verification and refusal remain deterministic substrate work (wisdom 6 through wisdom 9).

### Migration, compatibility, and rollback

The migration adds nullable work-item fields, revision 0, and the new empty tables. It creates
no registry, registry version, destination, work-item registry binding, election, target
selection, delegation, or landing receipt. Existing work stays untargeted until Mike creates
its registry, the registry policy owner binds the work item, and a new election DR resolves.

Readers and old clients remain compatible because work-item and decision-request output only
gain optional fields. Old clients cannot resolve the new DR subtype because label-or-response
resolution rejects it. Old clients cannot invoke `integration-land`; they therefore cannot
claim a managed landing. Release the server-side outcome guard and its CLI in one compatible
version before declaring the feature available.

Rollback retains registry, binding, election, receipt, and audit rows. Before a binary without
`integration-land` can serve managed landings, disable the managed landing entry point so it
fails closed; do not delete or rewrite rows to make an old binary appear compatible.
Re-applying the migration leaves retained registry IDs, current version pointers, work-item
bindings, election pointers, and revision values unchanged.

### Kungfu teaching

When the substrate capability ships, amend only
`priv/kungfu/agentic-engineering/guidance/engineering-tenets.md`. It is elected by the product
owner and each engineering archetype, so it gives the rule one guidance home. Add this
definitive teaching:

> Before a managed integration, read the work item's integration-target election. Do not infer
> a destination from a branch, a commit, a review, a spec, or nearby work. Ask Mike or a
> durably delegated principal to resolve the election DR. Treat `hold` and no election as a
> refusal to land. The substrate decides whether the named registry and destination are
> elected.

This teaching does not name branches, choose targets, or authorize an outcome. It teaches the
recognition and sends the outcome to the substrate rail (wisdom 2 and wisdom 3). Do not amend
the operating manual until the capability exists, as required by the guidance documentation
spec.

## Acceptance

1. Given an existing work item with a Tightbeam registry binding and no election, when a caller
   invokes `integration-land` for that registry and its `main` destination ID, then the handler
   returns `integration_target_missing`, writes a refusal event with the caller, work item, and
   registry, and writes no acceptance receipt.
2. Given a Mike-ruled election DR selecting `hold`, when a caller invokes `integration-land`
   for the bound registry and its `0.1.9` destination ID, then the handler returns
   `integration_target_hold` and preserves the hold row.
3. Given a Mike-ruled election selecting only the Tightbeam `main` destination ID, when a
   caller lands at that ID, then the handler writes one accepted landing receipt. When the
   caller lands at the Tightbeam `0.1.9` destination ID, then the handler returns
   `integration_target_absent`.
4. Given an election selecting the Tightbeam `main` and `0.1.9` destination IDs, when separate
   callers land once at each ID, then each receives its own accepted receipt. When a caller
   lands at the Tightbeam `0.2.0` destination ID, then the handler returns
   `integration_target_absent`.
5. Given the Tightbeam policy-owner role bound a work item to a current registry version whose
   display names are `main`, `0.2.0`, and `0.1.9`, when `integration-target-ask` opens a DR,
   then its typed projection contains exactly `hold` plus those three opaque destination IDs
   and display names. The DR accepts a non-empty subset of those IDs as one selection, retains
   the registry ID and authority hash, and omits `0.1.8`.
6. Given an election DR, when a principal other than Mike resolves it without an active scoped
   delegation, then the handler refuses with `integration_target_election_unauthorized` and
   leaves the DR and work-item pointer unchanged.
7. Given an active delegation scoped to the work item, when its grantee resolves the DR, then
   the election records the grant and grantee principal. Given the grant is revoked before the
   resolution transaction begins, when the grantee resolves the DR, then the handler refuses
   and records the revocation cause.
8. Given one resolved election DR, when the same typed selection, rationale, and idempotency key
   are sent serially, then the second response returns the same election ID with
   `replayed:true` and no new row or event. When the same key carries a different selection or
   rationale, then the handler returns `integration_target_idempotency_conflict`. When a
   different key follows the committed resolution, then it returns
   `integration_target_election_already_resolved`.
9. Given an election DR created at revision 2, when another election advances the work item to
   revision 3 before the DR resolves, then resolution returns
   `stale_integration_target_election`, leaves that DR unresolved, and creates no election.
10. Given a work item with `specRefName` and `specRefSha256`, when the registry policy-owner
    role binds a registry or Mike resolves an election, then the specRef pair is byte-for-byte
    unchanged. Given a registry binding and election, when a valid specRef update occurs, then
    both pointers and the election revision are unchanged.
11. Given pre-feature work items, when the migration completes, then each has a null registry
    ID, revision 0, a null election pointer, and no generated registry, registry version,
    destination, binding, election, delegation, or landing row.
12. Given a previously selected destination ID is absent from the registry's current version,
    when a caller invokes `integration-land` for it, then the handler returns
    `integration_target_obsolete` and preserves the historical election. When the policy owner
    later adds the same display name, then the registry assigns a new opaque destination ID;
    the historical election remains obsolete.
13. Given a registry creation or update, binding, successful election, revocation,
    supersession, accepted landing, or refused landing, when an auditor reads the event stream
    and work-item history, then each record exposes its stated cause and actor principal. A
    registry update or binding also exposes its authorizing policy-owner role. The election
    path exposes its DR and frozen registry version. The landing path exposes its registry,
    destination, election, and current registry version.
14. Given an installed `agentic-engineering` bundle after the feature ships, when an elected
    engineering archetype reads `engineering-tenets.md`, then it receives the exact
    integration-target teaching above and no other guidance file independently defines a
    target-selection rule.
15. Given no Tightbeam registry exists, when Mike invokes `integration-target-registry-create`
    with the exact Tightbeam scope, policy-owner role, authority, hash, and display names in
    Assumptions, then it returns one opaque registry ID and three opaque destination IDs, and
    registry get returns version 1 with those values. When the same scope is created again,
    then the handler returns `integration_target_registry_scope_exists` with the existing
    registry ID and changes no row.
16. Given a Tightbeam registry and a ClipMesh registry each display a destination named
    `0.1.0`, when a ClipMesh work item opens an election, then its DR enumerates only the
    ClipMesh destination ID. When a landing supplies the Tightbeam registry ID for that
    ClipMesh work item, then the handler returns `integration_target_registry_mismatch`. When
    it supplies the ClipMesh registry ID plus the Tightbeam destination ID, then the handler
    returns `integration_target_absent`. Neither call writes a receipt.
17. Given a registry update from version 3 to 4, when deterministic fault injection fails after
    a new destination identity, version row, or membership row is inserted but before pointer,
    audit, or commit completion, then version 3 stays current and no new destination, version-4,
    membership, or audit row remains. Given a stale expected version, then the handler returns
    `stale_integration_target_registry` and changes no row. Given the update succeeds, when
    registry get, registry-version get, and registry list run, then each returns the same
    atomic version-4 body and pointer relation.
18. Given an election resolution, when deterministic fault injection fails after each of the
    DR ruling, election insertion, predecessor link, work-item pointer, revision, or audit
    writes, then the transaction leaves the DR, election rows, pointer, revision, and audits
    byte-for-byte at their pre-call values.
19. Given a current election at revision 1, when a new DR at revision 1 resolves, then its
    election row has revision 2 and `predecessorElectionId` equal to the revision-1 election.
    The work-item pointer moves to revision 2, the revision-1 row stays byte-for-byte
    unchanged, and history derives revision 1's successor from the revision-2 row.
20. Given one open and one resolved election DR, when new and old clients read or list decision
    requests, then new clients receive the exact typed DR shape and resolution defined above;
    old clients retain their existing fields and see the resolved base ruling
    `integration_target_election`. Given a bound work item, when work-item get and list run,
    then both return the same registry ID and exact current-election object. Given current and
    historical registry versions, when registry get, registry-version get, and registry list
    run, then each response matches its exact wire shape and registry list orders rows by
    registry ID and destinations by destination ID.
21. Given one accepted landing, when the exact request and landing idempotency key are replayed,
    then the handler returns the same receipt with `replayed:true`. When the key carries a
    different registry, destination, landing ref, principal, or cause, then the handler returns
    `integration_landing_idempotency_conflict` and writes no second receipt.
22. Given an old client that ignores additive registry, election, and DR fields, when it reads
    pre-feature and post-feature rows, then its prior fields retain their prior values and
    shapes. When it tries label-or-response resolution on an election DR, then the server
    returns the typed-DR refusal and changes no election state.
23. Given the managed landing entry point is disabled before rollback, when a binary without
    `integration-land` serves ordinary pre-feature operations, then those operations continue
    and managed landing fails closed. When the new binary and migration are re-applied, then
    the Tightbeam registry IDs, current version pointer, work-item bindings, election pointers,
    revisions, receipts, and audits equal their pre-rollback values.

## Open Questions

None. Registry policy reaches the substrate only through the explicit scoped-registry
mutation seams above; implementation must not derive it from release prose or repository
topology.
