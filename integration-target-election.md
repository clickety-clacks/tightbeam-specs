# Integration-target election and landing refusal

## Goal

Give each Tightbeam work item a durable, owner-authorized integration-target election that
the substrate checks at the integration outcome. The election makes a destination explicit;
the substrate refuses a landing that has no matching election.

This replaces the convention-and-attest-registry practice. It realizes the branch-authority
rulings represented by `dr_b18fef87-82ff-4893-8882-24e5d096736b`,
`dr_4ecad888-39dc-4e7c-8080-21cfb064249d`,
`dr_2e105899-339d-4ff2-a9bd-d89a1683c16d`, `att_21d12c0b`, and
`dr_70bdfcbf-76a6-42ed-aa60-28617b0e3fcd` without inferring a target from any
branch, commit, review, spec, or nearby work.

## Non-Goals

- Choose an integration target for an untargeted work item, including
  `wi_eb6f8d36-0c9e-436f-8a62-b76f1190b021`.
- Merge, push, release, deploy, or operate Git itself.
- Change the artifact identity contract of `specRefName` and `specRefSha256`.
- Make `0.1.8` a destination. The superseding release authority locks it.
- Infer, create, retire, or rank destination lines from repository state.
- Create a second review, approval, or decision authority in kungfu guidance.
- Backfill a target for existing work items.

## Terms

- **Destination registry**: a versioned policy record that names the current destination
  identifiers and its release-line authority reference. The substrate treats identifiers as
  opaque values; it does not compile, rank, or derive a branch topology. On 2026-08-26 the
  recorded authority is `CONTRIBUTING.md` at Tightbeam `origin/main`, whose snapshot contains
  `main`, `0.2.0`, and active maintenance `0.1.9`, and excludes locked `0.1.8`.
- **Election**: one immutable record that selects either `hold` or a canonical non-empty set
  of destination identifiers for one work item.
- **No election**: the work item has no current election record. It is distinct from `hold`.
- **Hold**: an explicit election whose selected destination set is empty.
- **Election revision**: a positive integer assigned in order per work item. It supports
  compare-and-swap (CAS) and preserves superseded election history.
- **Election decision request (DR)**: the only DR shape that can produce an election. It
  carries the work item, an expected election revision, a frozen destination-registry
  snapshot, and a structured selection of either hold or a subset of that snapshot.
- **Delegation grant**: a durable, scoped authority from Mike to one principal to resolve an
  election DR. The grant identifies its grantor, grantee, work-item scope, creation time,
  revocation state, and cause.
- **Landing**: a Tightbeam-managed integration outcome. It names one work item and one
  destination identifier. `integration-land` is its outcome verb.
- **specRef**: the paired `specRefName` and `specRefSha256` work-item fields. They identify
  an artifact revision; they do not authorize a destination.

## Assumptions

- Mike remains the owner authorized to grant or revoke an election delegation.
- The organization maintains one authoritative destination registry from the currently live
  release-line authority. A registry snapshot contains its authority reference and content
  hash. Changing the registry is policy work; it never requires a substrate topology change.
- A future integration mechanism can route every Tightbeam-managed landing through
  `integration-land`; a direct Git operation outside Tightbeam is outside this substrate
  contract.
- `operator-rule` remains the durable operator-ruling transaction. This feature extends its
  election-DR surface with typed target-selection flags; ordinary DRs retain the current
  label-or-response surface.

## Invariants

1. A work item has exactly one current state: no election, a `hold` election, or a
   `destinations` election. A `destinations` election contains one or more distinct,
   canonical destination identifiers. A `hold` election contains zero destinations.
2. Only Mike, or the grantee of an active delegation grant scoped to the work item, can rule
   an election DR. The product owner, a work-item owner, a reviewer, and a spec author do
   not gain this authority by role or assignment.
3. An election DR presents `hold` plus each entry in its frozen registry snapshot. Its
   structured selection is either `hold` or a non-empty subset of those entries. The substrate
   rejects a selection that contains any other identifier or combines `hold` with a destination.
4. The substrate commits the DR ruling, the immutable election row, the work item's current
   election pointer, and their audit events in one database transaction. A failed transaction
   changes none of them.
5. The transaction succeeds only when its expected election revision equals the work item's
   current revision. A stale request stays unresolved and returns
   `stale_integration_target_election`.
6. Repeating the same resolved DR with the same outcome idempotency key returns the recorded
   election. A competing resolution returns the existing resolution and creates no second
   election or ruling.
7. A later valid election supersedes the former current election in the same transaction.
   It retains the former record and its cause. Revoking a delegation grant prevents future
   rulings; it does not silently change an election already recorded.
8. `integration-land` accepts a landing only when the work item has a current
   `destinations` election that contains the supplied destination and whose registry entry is
   currently live. It refuses no-election with `integration_target_missing`, `hold` with
   `integration_target_hold`, an absent destination with `integration_target_absent`, and a
   retired registry destination with `integration_target_obsolete`.
9. A multi-destination election authorizes each listed destination independently. A landing
   at one listed destination neither consumes nor broadens authorization for another.
10. A landing guard and the landing outcome record are one transaction. The guard is not a
    preflight endpoint and cannot be separated from the outcome it permits.
11. `specRef` remains independent. An election never writes, clears, validates, or derives
    `specRef`; a specRef update never writes, clears, validates, or derives an election.
12. Each election, delegation grant, revocation, supersession, accepted landing, and refused
    landing records a principal and a cause. Election events name the DR and registry snapshot;
    refusal events name the work item, requested destination, current election revision when
    present, refusal code, and caller principal.

## Architecture

### Durable model and mutation seam

Add these additive records, with the work-item integration-target mutation owned only by the
election-resolution transaction:

- `integration_target_elections`: immutable rows with `id`, `workItemId`, `revision`,
  `mode` (`hold` or `destinations`), canonical `destinationIds`, `decisionRequestId`,
  `registrySnapshotId`, `electedByPrincipal`, `delegationGrantId`, `cause`, `createdAt`, and
  `supersededByElectionId`.
- `integration_target_registry_snapshots`: immutable rows with `id`, `authorityRef`,
  `authoritySha256`, canonical `destinationIds`, and `createdAt`.
- `integration_target_delegations`: immutable grant identity and scope plus revocation fields.
  Grant and revoke mutations are Mike-only and append attributed audit events.
- nullable `work_items.integrationTargetElectionId` and non-null
  `work_items.integrationTargetElectionRevision`, initialized to `NULL` and `0`.

The absent pointer at revision 0 represents no election. A current election row represents
either hold or destinations. Database constraints enforce the mode/set pairing, uniqueness of
`(workItemId, revision)`, uniqueness of a DR result, and one current pointer per work item.
They make unrecognized state labels and duplicate destinations unrepresentable.

The substrate accepts destination identifiers only through a registry snapshot. It contains no
compiled branch-name list, highest-version selection, or source-ref heuristic. This keeps
release topology as org policy rather than substrate physics (wisdom 10).

This adds a durable decision record because the requested landing surface must remain usable
after inference is unavailable. Deleting the landing surface would not meet the requested
integration outcome. Accepting an inferred target would retain the failure this contract
closes.

### Election and delegation flow

1. `integration-target-ask --work-item <id>` reads the live destination registry and opens
   one election DR for the current work-item revision. Its structured choices are `hold` or a
   non-empty subset of registry destination identifiers; free-text destination labels are
   invalid.
2. Mike grants a scoped delegation only with
   `integration-target-delegate --work-item <id> --principal <kind:id> --cause <text>`.
   `integration-target-revoke-delegation <grant-id> --cause <text>` records the revocation.
3. Election DR resolution uses
   `operator-rule <dr-id> (--integration-target-hold | --integration-target <id>...)`.
   `--integration-target` may repeat, and the hold flag is exclusive. Inside one transaction,
   the handler checks the caller's Mike-or-active-grantee authority, DR type, expected revision,
   registry snapshot, typed selection, and idempotency key. It then records the ruling, inserts
   the election, supersedes a former election when present, advances the pointer and revision,
   and publishes attributed audit events. The pre-existing `--decision` and `--response` forms
   reject an election DR.
4. A changed selection needs a new election DR that names the current election revision. A
   withdrawn or stale DR changes no election.

The wire representation adds `integrationTargetElection` to work-item reads and lists. It is
`null` for no election; otherwise it contains `id`, `revision`, `mode`, `destinationIds`,
`decisionRequestId`, `registrySnapshotId`, `electedByPrincipal`, and `supersededBy` when read
historically. Existing clients can ignore this additive field.

### Landing refusal

`integration-land --work-item <id> --destination <destination-id> --landing-ref <ref>` is
the sole Tightbeam outcome verb for a managed landing. It receives one destination, never a
default. Its handler performs the current-election and registry checks while inserting the
landing outcome receipt. On failure it writes the refusal event and returns the named refusal
code; it creates no acceptance receipt. A caller must use the receipt to claim a
Tightbeam-managed landing.

The implementation must route each existing or new managed integration endpoint through this
handler, rather than copy a target check into callers. The rail therefore fires where both the
condition and action leave rows (wisdom 1), is silent when satisfied (wisdom 4), and leaves a
cause and principal on both legs (wisdom 5). Selection remains an operator judgment;
verification and refusal remain deterministic substrate work (wisdom 6 through wisdom 9).

### Migration, compatibility, and rollback

The migration adds nullable pointers, revision 0, and new empty tables. It creates no election,
target, registry snapshot, delegation, or landing receipt for existing work. Existing work stays
untargeted until a new election DR resolves.

Readers and old clients remain compatible because work-item output only gains an optional
object. Old clients cannot invoke `integration-land`; they therefore cannot claim a managed
landing. Release the server-side outcome guard and its CLI in one compatible version before
declaring the feature available.

Rollback retains election and audit rows. Before a binary without `integration-land` can serve
managed landings, disable the managed landing entry point so it fails closed; do not delete or
rewrite elections to make an old binary appear compatible. Re-applying the migration reuses the
retained rows and revision values.

### Kungfu teaching

When the substrate capability ships, amend only
`priv/kungfu/agentic-engineering/guidance/engineering-tenets.md`. It is elected by the product
owner and each engineering archetype, so it gives the rule one guidance home. Add this
definitive teaching:

> Before a managed integration, read the work item's integration-target election. Do not infer
> a destination from a branch, a commit, a review, a spec, or nearby work. Ask Mike or a
> durably delegated principal to resolve the election DR. Treat `hold` and no election as a
> refusal to land. The substrate decides whether a named destination is elected.

This teaching does not name branches, choose targets, or authorize an outcome. It teaches the
recognition and sends the outcome to the substrate rail (wisdom 2 and wisdom 3). Do not amend
the operating manual until the capability exists, as required by the guidance documentation
spec.

## Acceptance

1. Given an existing work item with no election, when a caller invokes `integration-land` for
   `main`, then the handler returns `integration_target_missing`, writes a refusal event with
   the caller and work item, and writes no acceptance receipt.
2. Given a Mike-ruled election DR selecting `hold`, when a caller invokes `integration-land`
   for `0.1.9`, then the handler returns `integration_target_hold` and preserves the hold row.
3. Given a Mike-ruled election selecting only `main`, when a caller lands at `main`, then the
   handler writes one accepted landing receipt. When the caller lands at `0.1.9`, then the
   handler returns `integration_target_absent`.
4. Given an election selecting `main` and `0.1.9`, when separate callers land once at each
   destination, then each receives its own accepted receipt. When a caller lands at `0.2.0`,
   then the handler returns `integration_target_absent`.
5. Given the live registry contains `main`, `0.2.0`, and `0.1.9`, when
   `integration-target-ask` opens a DR, then the stored structured options contain exactly
   `hold` plus those identifiers, accept a non-empty subset of those identifiers as one typed
   selection, retain the registry authority hash, and omit `0.1.8`.
6. Given an election DR, when a principal other than Mike resolves it without an active scoped
   delegation, then the handler refuses with `integration_target_election_unauthorized` and
   leaves the DR and work-item pointer unchanged.
7. Given an active delegation scoped to the work item, when its grantee resolves the DR, then
   the election records the grant and grantee principal. Given the grant is revoked before the
   same transaction, when the grantee resolves the DR, then the handler refuses and records
   the revocation cause.
8. Given two concurrent resolutions for one election DR, when the first commits, then exactly
   one ruling, election row, pointer update, and revision increment exist. When the second
   arrives, then it returns the recorded result for the same idempotency key or a resolved-DR
   refusal for a competing key.
9. Given an election DR created at revision 2, when another election advances the work item to
   revision 3 before the DR resolves, then resolution returns
   `stale_integration_target_election`, leaves that DR unresolved, and creates no election.
10. Given a work item with `specRefName` and `specRefSha256`, when Mike resolves an election,
    then the specRef pair is byte-for-byte unchanged. Given an election, when a valid specRef
    update occurs, then the election pointer and revision are unchanged.
11. Given pre-feature work items, when the migration completes, then each has revision 0,
    a null election pointer, and no generated election, delegation, or landing rows.
12. Given a previously selected destination no longer appears in the current live registry,
    when a caller invokes `integration-land` for it, then the handler returns
    `integration_target_obsolete` and preserves the historical election.
13. Given a successful election, revocation, supersession, accepted landing, or refused
    landing, when an auditor reads the event stream and work-item history, then each record
    exposes its stated cause and principal and the election path exposes its DR and registry
    snapshot.
14. Given an installed `agentic-engineering` bundle after the feature ships, when any elected
    engineering archetype reads `engineering-tenets.md`, then it receives the exact
    integration-target teaching above and no other guidance file independently defines a
    target-selection rule.

## Open Questions

None. The implementation must derive the live registry from the release-line authority at DR
creation and landing time; changing that authority is a future owner ruling, not an
implementation choice in this contract.
