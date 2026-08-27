# Completion attest card-deliverable contract — v1

Status: PROPOSAL for one owner-routed independent review. No product target is
elected. This proposal derives from work item
`wi_f46d2e83-e152-429f-93c7-3c51989bd391`, spirit verdict
`att_df4251d6-87e9-4e60-8c7d-e9916a933ba9`, correction
`att_c15df88b-e936-4f03-9b46-93733767b4b8`, and split disposition
`att_b6934754-9b78-4f56-be6d-d27fbf0aeaaf`.

The proven regression is work item
`wi_113442f5-22ae-457b-a971-1b620069d490`, titled “REST read plane D3 — CLI
direct-GET migration and legacy read removal.” Its only producing assignment was
the spec assignment `asg_29aeed02-f3bc-421a-99ca-c2bce6f80ec0`. That assignment
closed with completion attest
`att_1ab4c74f-d4a3-4af2-8c61-c467062367e4`, whose note began “Completed D3 spec
authoring and push only.” No coder assignment existed. The work item later closed
as completed. The holder completed a subordinate deliverable, but the durable card
reported the larger deliverable complete.

This spec extends the current `attest`, `assign`, `dispatch`, `reopen-assignment`,
`work-item-create`, `work-item-update`, `work-item-get`, `work-item-list`,
`work-item-close`, `work-item-trace`, assignment/attest reads, and Toplines projection
contracts. It does not replace `attest-v1.md`, `work-item-v1.md`,
`completion-rails-decisions.md`, or
`completion-escalation-rail-v2.md`. When the latter completion-escalation proposal
lands, its completion record joins the claim defined here by the same closing attest
and shares the transaction boundary in I4.

## Goal

Make `kind=completion` an exact, durable assertion that the assignment's stored
deliverable is delivered. Prevent a holder from narrowing or substituting that
deliverable in the completion request or note. Let a work item close only from a
completion claim for its named card deliverable, unless the work-item owner records an
explicit narrowing ruling in the same close transaction.

For card closure, `kind=completion` asserts delivery of the card's named deliverable
only when the completed obligation was explicitly card-bound at assignment open. A
default subordinate completion terminates that obligation but is not a card-deliverable
completion. This distinction is stored before the holder acts; the completion note
cannot choose or change it.

The mechanism must prevent the `wi_113442f5` outcome: completing and reviewing only a
spec must not permit the work item for product implementation and legacy-read removal
to close without an owner narrowing ruling.

## Non-Goals

- The substrate does not decide whether bytes, artifacts, tests, or prose actually
  satisfy a named deliverable. A completion remains a holder assertion. Review and
  other installed completion rails decide whether required evidence exists.
- This spec does not parse a subject, title, note, artifact, verdict, prompt, or commit
  message for scope or quality.
- This spec does not change `kind=progress`, surrender, revocation, verdict meaning,
  completion-rail composition, completion notice routing, or session disposition.
- This spec does not add hierarchy, phases, subtasks, percentages, automatic staffing,
  automatic work-item close, or a product-specific deliverable taxonomy.
- This spec does not let an administrator, holder, reviewer, process, or substrate
  narrow a card deliverable. Only the owner principal defined in Terms can do so.
- This spec does not rewrite a pre-contract terminal work item, assignment, attest, or
  event row. It does not fabricate a completion claim for an old completion attest.
- This proposal authorizes no product code, target, merge, release, deployment, live
  mutation, identity edit, configuration change, or credential change.

## Terms

- **Card:** One `work_items` row. It is the durable identity for one user outcome across
  assignment eras and concurrent aspects.
- **Card deliverable:** The immutable text and identity created for a non-terminal card
  when this contract starts governing it. For a new card, the text is the validated
  string stored in `work_items.title` by `work-item-create`. JSON escape spelling is not
  part of the identity. A later display-title update does not change the card
  deliverable.
- **Deliverable identity:** A substrate-generated `dlv_` id plus the lowercase SHA-256
  of the UTF-8 encoding of the exact stored deliverable string. The implementation does
  not trim, case-fold, or Unicode-normalize that stored string when hashing it. The id is
  the comparison key. The text and hash make the identity readable and independently
  checkable.
- **Obligation:** One assignment row. It can deliver the whole card or a subordinate
  outcome.
- **Card-bound obligation:** An assignment whose stored deliverable identity equals its
  linked card's deliverable identity. `assign|dispatch --delivers-work-item` creates this
  binding. It requires a linked work item.
- **Subordinate obligation:** An assignment with its own deliverable identity. The exact
  assignment subject is its deliverable text. This is the default for an assignment
  created without `--delivers-work-item`, including linked assignments.
- **Completion claim:** One immutable row keyed by a newly committed completion attest.
  It copies the obligation's stored deliverable identity. The holder supplies no
  deliverable field on `attest`.
- **Exact close:** A card close whose selected completion claim names the card
  deliverable identity.
- **Owner narrowing ruling:** The immutable part of a card-closure row that records the
  card deliverable, a different selected completion claim from the same card, a
  nonblank reason, and the acting owner principal.
- **Owner principal:** The user in `work_items.ownerUserId`, acting directly as that user
  or through a session owned by that user. An administrator owned by another user is not
  the owner principal for narrowing.
- **Acting principal:** The direct user id or session key that submitted a mutation. A
  closure stores exactly one of `closedByUser` and `closedBySession`. An owner narrowing
  also copies `work_items.ownerUserId` into `ownerRulingOwnerUserId`, so later audit does
  not have to infer the authorizing owner from mutable session metadata.
- **Legacy terminal row:** A card or assignment that reached a terminal state before
  this contract's activation. Its old fields remain authoritative for that historical
  transition. It has no retroactive deliverable contract.
- **Request fingerprint:** SHA-256 over the verb name and the length-prefixed exact
  values that affect the mutation. For completion it covers assignment id, kind, note,
  and commit refs. For card close it covers work-item id, selected completion-attest id,
  and nullable owner-ruling reason. Length-prefixing prevents concatenation ambiguity.

## Assumptions

1. The database owner serializes each mutation transaction.
2. `assignments.subject` and `work_items.title` are stored exactly after their existing
   validation. Neither field requires semantic normalization.
3. A work item has one owning user in `work_items.ownerUserId`.
   No supported work-item mutation changes that owner.
4. Assignment completion already inserts the attest and closes the assignment in one
   guarded transaction. Work-item close already verifies that no assignment is open.
5. Assignment reopen preserves prior attests and makes a later completion attest the
   current `closingAttestId`.
6. Installed completion rails can require evidence, but they do not change which
   deliverable a completion claims.
7. Current product evidence was reconciled against
   `clickety-clacks/tightbeam` `origin/main` commit
   `8e269e89c04b6b8569813142a12742f3325b8503`. Current spec evidence was reconciled
   against `clickety-clacks/tightbeam-specs` `origin/main` commit
   `24242a993f965953975bde0a11af2153db1f380b`.

## Invariants

### I1 — One immutable card deliverable

Each new or migrated non-terminal card has exactly one work-item deliverable link. Its
deliverable id, text, and SHA-256 do not change. `work-item-update --title` remains a
display-metadata update and does not change that link. A second link is rejected by a
primary-key constraint.

### I2 — One immutable obligation binding

Each assignment created after activation, each assignment open during activation, and
each legacy terminal assignment reopened after activation has exactly one
assignment-deliverable link before it is open. A card-bound link copies the linked
card's deliverable id. A subordinate link points to a new deliverable whose text is the
validated string stored in `assignments.subject`. A primary-key constraint makes two
links for one assignment unrepresentable.

### I3 — Completion copies; the holder does not choose

For a new `kind=completion` mutation, the server reads the obligation binding after
holder and open-state authorization. It inserts one completion claim with that exact deliverable id.
The completion request has no deliverable text, id, override, phase, or narrowing field.
The note remains audit prose and cannot change the claim.

### I4 — A completion is structurally complete or commits nothing

The completion attest, completion claim whose `claimedAt` equals the attest timestamp,
guarded assignment close, assignment marker,
work-item bracket update, supervision transition, effort cancellation, and any installed
completion-escalation record commit in one transaction. A missing or inconsistent
obligation binding aborts that transaction. No attest, claim, close, marker, wake,
transition, or cancellation from that attempt remains.

### I5 — Work-item close selects one current claim

`work-item-close` requires one `completionAttestId`. The selected row must:

1. be an attest with `kind=completion`;
2. be the current `closingAttestId` of a completed assignment;
3. belong to an assignment linked to the card being closed; and
4. have one completion claim.

The handler checks these facts and the existing zero-open-assignment condition in the
same close transaction. It does not search for a preferred completion.

### I6 — Exact close is mechanical

When the selected claim's deliverable id equals the card deliverable id, the existing
owner-or-admin close authorization can close the card. The closure row records
`basis='exact'`, both equal ids, the selected completion attest, exactly one acting
principal field, and the close time. No owner ruling reason or owner-ruling user is
accepted on an exact close.

### I7 — Only the owner can narrow at close

When the selected claim names a different deliverable from the same card, the close
commits only if the owner principal supplies `ownerRulingReason`. The reason must contain
1..2000 nonblank characters. The closure row records `basis='owner_narrowing'`, the card
deliverable id, the accepted claim's deliverable id, the completion attest, the exact
reason, the acting principal, and the close time. An administrator owned by another user
may perform an exact close but cannot create this ruling. The row also copies the
authorizing card-owner user id.

### I8 — Claim, assignment, and card boundaries do not blur

Completing a subordinate obligation can close that assignment. It cannot close the card
without I7's owner ruling. Completing a card-bound obligation can support an exact card
close, but it does not close the card automatically. The explicit card-close transaction
remains the sole card terminal seam.

### I9 — Failures preserve open state

A different-card completion, a subordinate completion without an owner ruling, a stale
completion from before assignment reopen, a missing claim, an open assignment, or an
unauthorized ruling returns a typed error and writes no card-closure or ruling row. The
card remains in its prior state.

### I10 — Retries are row-idempotent

`attest kind=completion` accepts optional `--key <idempotencyKey>`. Other attest kinds
reject that parameter. The first successful keyed completion stores its fingerprint and
canonical response in the deliverable-contract idempotency table in the same transaction
as I4. The same acting
principal, operation, key, and fingerprint returns the original response, including
after restart. The same scoped key with another fingerprint returns
`idempotency_conflict`. A different key after the assignment closes returns the existing
`assignment_closed` result and creates no second attest or claim.

`work-item-close` also accepts optional `--key`. A successful keyed close stores its
fingerprint and canonical response in the same close transaction. On a closed v1 card,
an authorized request with the stored close fingerprint returns the stored closure,
even with a different key or no key. Any other authorized close request returns
`work_item_closed`. It does not add another closure or ruling. A legacy closed card
preserves the predecessor same-state no-op response in I13.

### I11 — Races serialize to one history

If completion and card close race, close succeeds only when it observes the committed
claim and zero open assignments. A close that selects the in-flight completion and
serializes first returns `completion_claim_not_found`. An owner-narrowing close that
selects an existing subordinate claim but races the last open assignment's completion
returns `assignments_open` when it serializes first. Each refusal writes nothing; the
caller can retry after completion. If two assignment terminal operations race, one wins
and the other receives `assignment_closed`. If exact and owner-narrowing closes race
after all claims commit, one closure wins and the other receives `work_item_closed`. A
same-fingerprint loser receives the stored closure.

### I12 — Reopen creates a new completion episode

Reopening a completed assignment does not change its obligation binding or old claim.
The next completion creates a new attest and claim for the same deliverable. Only the
new `closingAttestId` can support a later card close. Prior claims remain queryable.

Reopening a legacy terminal assignment that has no binding creates one subordinate
deliverable from its stored subject in the same reopen transaction. The binding exists
before the assignment becomes open. This creates no claim for the historical terminal
episode and changes no historical attest or terminal values.

Icebox and reopen preserve the card deliverable. Work-item failure writes no closure
claim. A closed card does not reopen under this spec.

### I13 — Historical rows stay historical

Activation creates no deliverable, claim, closure, or ruling row for a legacy terminal
card or assignment. It does not edit a legacy row. A later reopen may create the new
binding required by I12; that binding belongs to the new open episode, not the old
terminal transition. Reads identify untouched legacy rows with
`deliverableContract='legacy'` and nullable deliverable/closure projections. Repeating
an already-closed legacy card close preserves the existing no-op result and does not
backfill a closure.

### I14 — Visibility does not expand

Deliverable text, hashes, claims, and closure rulings appear only in a response that the
caller could already use to read the owning assignment or work item. Authorization runs
before the handler discloses whether a selected completion attest, deliverable, or ruling
exists. A selected claim outside the caller's existing read visibility returns the same
`completion_claim_not_found` envelope as an absent claim. Error responses do not reveal
a foreign card's existence, text, ids, or principal.

### I15 — The substrate compares identities, not meaning

The substrate compares exact ids and verifies relational ownership. It does not decide
whether one text is a subset, phase, artifact, or semantic equivalent of another. The
owner's explicit ruling supplies the only judgment. This follows wisdom 6 and wisdom 9.

### I16 — The contract survives restart and rejects downgrade

The elected implementation records a new schema shape. Its upgrade creates and validates
the new tables, backfills non-terminal rows, and advances the shape stamp in one database
transaction. An interruption leaves the old shape and no committed partial backfill, or
the new shape and the complete validated contract. Restart repeats the old-shape upgrade
or validates the new shape. A binary that lacks this contract refuses the new stamp
instead of accepting an unguarded close.

## Architecture

### Pattern: completion binds to the card

This pattern applies to assignment completion and work-item close. A completion claim
copies a pre-existing deliverable identity. It does not accept new scope. The pattern
does not apply to progress, surrender, revocation, verdicts, artifact classification, or
review judgment.

Canonical example: a card named “Implement CLI direct GET and remove legacy reads” has
deliverable `dlv_full`. A spec-writing assignment defaults to subordinate deliverable
`dlv_spec`. Its completion closes the spec assignment and claims `dlv_spec`; exact card
close refuses. A coder assignment opened with `--delivers-work-item` claims `dlv_full`
on completion and can support exact card close. The owner can instead close from
`dlv_spec` only by recording an owner narrowing ruling.

### Durable rows

Use companion tables so old domain rows remain byte-for-byte unchanged:

```sql
CREATE TABLE deliverables (
  id        TEXT PRIMARY KEY,
  name      TEXT NOT NULL CHECK(length(name) BETWEEN 1 AND 2000 AND length(trim(name)) >= 1),
  sha256    TEXT NOT NULL CHECK(length(sha256)=64 AND sha256 NOT GLOB '*[^0-9a-f]*'),
  createdAt INTEGER NOT NULL
);

CREATE TABLE work_item_deliverables (
  workItemId   TEXT PRIMARY KEY REFERENCES work_items(id),
  deliverableId TEXT NOT NULL UNIQUE REFERENCES deliverables(id),
  UNIQUE(workItemId, deliverableId)
);

CREATE TABLE assignment_deliverables (
  assignmentId TEXT PRIMARY KEY REFERENCES assignments(id),
  deliverableId TEXT NOT NULL REFERENCES deliverables(id),
  sourceKind TEXT NOT NULL CHECK(sourceKind IN ('assignment','work_item')),
  sourceWorkItemId TEXT NULL REFERENCES work_items(id),
  CHECK(
    (sourceKind='assignment' AND sourceWorkItemId IS NULL) OR
    (sourceKind='work_item' AND sourceWorkItemId IS NOT NULL)
  ),
  UNIQUE(assignmentId, deliverableId),
  FOREIGN KEY(sourceWorkItemId, deliverableId)
    REFERENCES work_item_deliverables(workItemId, deliverableId)
);
CREATE UNIQUE INDEX assignment_own_deliverable
  ON assignment_deliverables(deliverableId)
  WHERE sourceKind='assignment';

CREATE TABLE completion_claims (
  attestId TEXT PRIMARY KEY REFERENCES attests(id),
  assignmentId TEXT NOT NULL REFERENCES assignments(id),
  deliverableId TEXT NOT NULL REFERENCES deliverables(id),
  claimedAt INTEGER NOT NULL,
  UNIQUE(attestId, deliverableId),
  FOREIGN KEY(assignmentId, deliverableId)
    REFERENCES assignment_deliverables(assignmentId, deliverableId)
);

CREATE TABLE work_item_closures (
  workItemId TEXT PRIMARY KEY REFERENCES work_items(id),
  completionAttestId TEXT NOT NULL UNIQUE REFERENCES attests(id),
  cardDeliverableId TEXT NOT NULL REFERENCES deliverables(id),
  acceptedDeliverableId TEXT NOT NULL REFERENCES deliverables(id),
  basis TEXT NOT NULL CHECK(basis IN ('exact','owner_narrowing')),
  ownerRulingReason TEXT NULL
    CHECK(ownerRulingReason IS NULL OR length(trim(ownerRulingReason)) BETWEEN 1 AND 2000),
  ownerRulingOwnerUserId TEXT NULL REFERENCES users(userId),
  closedByUser TEXT NULL,
  closedBySession TEXT NULL,
  requestFingerprint TEXT NOT NULL
    CHECK(length(requestFingerprint)=64 AND requestFingerprint NOT GLOB '*[^0-9a-f]*'),
  closedAt INTEGER NOT NULL,
  CHECK((closedByUser IS NOT NULL) != (closedBySession IS NOT NULL)),
  CHECK(
    (basis='exact' AND cardDeliverableId=acceptedDeliverableId AND
      ownerRulingReason IS NULL AND ownerRulingOwnerUserId IS NULL) OR
    (basis='owner_narrowing' AND cardDeliverableId<>acceptedDeliverableId AND
      ownerRulingReason IS NOT NULL AND ownerRulingOwnerUserId IS NOT NULL)
  ),
  FOREIGN KEY(workItemId, cardDeliverableId)
    REFERENCES work_item_deliverables(workItemId, deliverableId),
  FOREIGN KEY(completionAttestId, acceptedDeliverableId)
    REFERENCES completion_claims(attestId, deliverableId)
);

CREATE TABLE deliverable_contract_idempotency (
  actorKind TEXT NOT NULL CHECK(actorKind IN ('user','session')),
  actorRef TEXT NOT NULL CHECK(length(trim(actorRef)) >= 1),
  operation TEXT NOT NULL CHECK(operation IN ('attest-completion','work-item-close')),
  idempotencyKey TEXT NOT NULL CHECK(length(trim(idempotencyKey)) BETWEEN 1 AND 200),
  requestFingerprint TEXT NOT NULL
    CHECK(length(requestFingerprint)=64 AND requestFingerprint NOT GLOB '*[^0-9a-f]*'),
  canonicalResponse TEXT NOT NULL CHECK(json_valid(canonicalResponse)),
  completionAttestId TEXT NULL REFERENCES completion_claims(attestId),
  workItemId TEXT NULL REFERENCES work_item_closures(workItemId),
  PRIMARY KEY(actorKind, actorRef, operation, idempotencyKey),
  CHECK(
    (operation='attest-completion' AND completionAttestId IS NOT NULL AND workItemId IS NULL) OR
    (operation='work-item-close' AND completionAttestId IS NULL AND workItemId IS NOT NULL)
  )
);
```

The implementation can add derived indexes required by the specified reads. It must not
add a second mutable deliverable representation. Table names and fields above are the
normative storage vocabulary.

### Creation and activation

`work-item-create` inserts the card row, deliverable row, and work-item link in one
transaction. `assign` and `dispatch` insert the assignment, its deliverable row when
subordinate, and its link in their existing atomic open transaction.

The shape upgrade backfills:

1. one card deliverable from the current title of each `open` or `iceboxed` work item;
2. one subordinate deliverable from the subject of each open assignment; and
3. no claim, closure, or ruling for a pre-activation attest or terminal row.

For backfill only, a deliverable id is `dlv_` plus the lowercase SHA-256 of the
length-prefixed tuple `(completion-attest-card-deliverable-v1, sourceKind, fullSourceId)`.
Live creation continues to use the product's ordinary random id generator. The upgrade
orders rows by full source id and verifies that every generated id is unique, so the same
captured predecessor fixture produces byte-identical backfill rows. It validates exact
cardinality, name hashes, foreign keys, and source-kind checks before it advances the
stamp. A database containing a partial or ambiguous prior deliverable table returns
`deliverable_contract_inconsistent`, names the table and source row id, and leaves the
predecessor stamp unchanged.

### Mutation seams

After activation, four domain mutation seams can create rows defined by this contract.
The one-time shape upgrade in I16 is separate:

1. `work-item-create` establishes the immutable card deliverable.
2. The assignment-open seam establishes the immutable obligation binding. `assign` and
   `dispatch` call it for new assignments. `reopen-assignment` calls it only when a
   legacy terminal assignment lacks a binding, before that assignment becomes open.
3. `attest kind=completion` copies that binding into an immutable completion claim.
4. `work-item-close` records either an exact closure or the owner's one-time narrowing
   ruling and closure.

No amend, delete, repair, or free-standing narrowing verb exists. A wrongly named new
card is failed or iceboxed and replaced. An open obligation with the wrong binding is
revoked and replaced. These existing exits avoid a mutable scope history.

### Wire and CLI

- `assign` and `dispatch` add optional boolean `params.deliversWorkItem`, exposed as
  `--delivers-work-item`. It defaults to `false`. `true` without `workItemId` returns
  `deliverable_work_item_required` and creates nothing.
- `attest` adds optional `params.idempotencyKey`, exposed as `--key` only when
  `kind=completion`. No deliverable parameter exists. Other kinds supplied with a key
  return `idempotency_key_not_applicable` and write nothing.
- `reopen-assignment` adds no flag. It establishes the I12 subordinate binding when the
  selected legacy terminal assignment has none.
- `work-item-close` requires `params.completionAttestId`, exposed as
  `--completion-attest <attestId>`. It accepts optional `params.ownerRulingReason`,
  exposed as `--owner-ruling-reason <text>`, and optional `params.idempotencyKey`,
  exposed as `--key`.
- The CLI refuses `--owner-ruling-reason` without `--completion-attest`. The server
  repeats each validation.
- Short-id resolution uses the existing typed prefix resolver. Ambiguous prefixes return
  its existing ambiguity envelope and write nothing.

### Authorization and precedence

Completion resolves the assignment and verifies the holder before it reads a keyed retry
receipt. A same-key, same-fingerprint hit returns its stored response before open-state
or completion-rail evaluation; a same-key, different-fingerprint hit returns
`idempotency_conflict`. A miss preserves existing open-state authorization, then checks
the constitutional deliverable binding before it evaluates completion rails. A user,
process, non-holder session, or retired holder cannot file a new claim. A missing
binding cannot arm a remedy for a completion attempt that has no defined claim.

Card close preserves existing owner-or-admin authorization for exact close. It checks
that authorization before resolving the completion-attest reference. For a mismatch,
the handler then checks exact owner-principal authority before it accepts a ruling
reason. A foreign principal receives the existing non-disclosing authorization error.

### Typed errors

| Code | Condition | Remedy |
|---|---|---|
| `deliverable_work_item_required` | `--delivers-work-item` names no linked card. | Link the assignment to a work item or omit the flag. |
| `assignment_deliverable_missing` | An open assignment has no binding after activation. | Stop and repair the incompatible database through the supported shape path. |
| `completion_attest_required` | A non-terminal card close omits the completion attest. | Name the exact current completion attest. |
| `completion_claim_not_found` | The selected attest or its claim is absent after authorization. | Complete the obligation, then retry with its exact attest. |
| `completion_claim_stale` | The selected attest is not the assignment's current closing attest. | Read the assignment and use the current completion. |
| `completion_claim_wrong_card` | The readable selected assignment is linked to another card or no card. | Select a completion from this card. |
| `completion_deliverable_mismatch` | The claim differs and `ownerRulingReason` is omitted. | Complete a card-bound obligation, or ask the owner to rule explicitly. |
| `owner_ruling_required` | A mismatch includes `ownerRulingReason`, but its value is blank. | Supply the owner's explicit reason. |
| `owner_ruling_forbidden` | The caller can administer an exact close but does not own this card. | Ask the card owner to rule. |
| `owner_ruling_not_applicable` | An exact close supplies a narrowing reason. | Remove the reason and close exactly. |
| `idempotency_key_not_applicable` | A non-completion attest supplies `idempotencyKey`. | Remove the key. |
| `idempotency_conflict` | A scoped key was reused with another fingerprint. | Read the stored result or use a new key for a new request. |
| `work_item_closed` | A later close conflicts with the stored closure. | Read the immutable closure. |
| `deliverable_contract_inconsistent` | Upgrade or boot validation finds missing, duplicate, or mismatched contract rows. | Preserve the database and use the supported recovery path. |

Existing typed errors remain authoritative for earlier precedence steps, including
`not_holder`, `assignment_closed`, `not_authorized`, `assignments_open`,
`invalid_transition`, and ambiguous or unknown id errors.

### Read projections and audit

Every non-legacy work-item projection adds:

```json
{
  "deliverableContract": "v1",
  "deliverable": {"id":"dlv_...","name":"...","sha256":"..."},
  "closure": null
}
```

A closed v1 card replaces that null with:

```json
{
  "completionAttestId":"att_...",
  "cardDeliverable":{"id":"dlv_...","name":"...","sha256":"..."},
  "acceptedDeliverable":{"id":"dlv_...","name":"...","sha256":"..."},
  "basis":"exact|owner_narrowing",
  "ownerRulingReason":null,
  "ownerRulingOwnerUserId":null,
  "closedByUser":null,
  "closedBySession":"agent:...",
  "closedAt":123
}
```

Exactly one of `closedByUser` and `closedBySession` is nonnull. The two owner-ruling
fields are nonnull only for `basis='owner_narrowing'`.

Every non-legacy assignment projection adds:

```json
{
  "deliverableContract": "v1",
  "deliverable": {
    "id":"dlv_...", "name":"...", "sha256":"...",
    "sourceKind":"assignment|work_item", "sourceWorkItemId":null
  }
}
```

For `sourceKind='work_item'`, `sourceWorkItemId` is the linked work-item id. Each
completion attest adds:

```json
{
  "deliverableClaim": {
    "id":"dlv_...", "name":"...", "sha256":"...", "claimedAt":123
  }
}
```

Other attest kinds project `deliverableClaim:null`. Legacy terminal objects project
`deliverableContract:'legacy'`, `deliverable:null`, and `closure:null` where applicable.

`work-item-get`, `work-item-list`, `assignments`, `attests`, `work-item-trace`, Toplines
list and detail, and every accepted verb response use the same stored projection. No
projection reconstructs an old claim from a note. The ordinary verb event remains an
audit mirror. Domain rows are the source of truth.

### Compatibility and guidance

An old `assign` or `dispatch` client creates a subordinate obligation. An old `attest`
client can complete it because the server copies the binding and the new key is optional.
An old `reopen-assignment` client can reopen a legacy terminal assignment because the
server establishes its subordinate binding without a new parameter. An old close client
cannot close a non-terminal v1 card because it cannot name the required completion
attest; the server returns `completion_attest_required` without
mutation. On a v1 card already closed under this contract, that old close request
returns `work_item_closed`; legacy closed cards keep the predecessor same-state no-op.
Read additions are additive.

After the capability ships, CLI help and the operating manual must teach one
pattern: completion claims the stored assignment deliverable; use
`--delivers-work-item` only when that obligation delivers the whole card; card close
names the completion attest; only the owner can record a narrower close. Guidance must
land with the implemented commands, not with this proposal (wisdom 20 and wisdom 21).

### Subtraction ruling

ADD wins because the rows currently cannot distinguish a whole-card completion from a
subordinate completion. DELETE loses because removing work-item close would remove the
owner's terminal lifecycle seam. ACCEPT loses because the demonstrated regression makes
“completed” materially false without a named refusal or ruling. The design adds only
immutable identities, claims, one closure row, and keyed retry receipts; it adds no
adjudicator or mutable scope engine.

### Traceability

| Requirement | Mechanism | Acceptance |
|---|---|---|
| Completion binds to stored scope | I2-I4; completion claim | A1-A5 |
| Partial or different work cannot close a card silently | I5-I9 | A2, A3, A6, A7 |
| Only owner can narrow | I7; owner-principal check | A7, A8 |
| Races and replay keep one history | I10-I12 | A9-A12 |
| Reopen, restart, and history remain truthful | I12, I13, I16; reopen and shape upgrade | A13, A14 |
| Reads are exact and private | I14; stored projections | A15 |
| `wi_113442f5` cannot recur | card/subordinate binding split | A16 |

## Acceptance

### A1 — Whole-card completion and exact close

Given a new card has deliverable `D`, and its only assignment was created with
`--delivers-work-item`, when the holder files completion, then the assignment and attest
commit with one claim for `D`. When an authorized caller closes the card with that
attest, then one exact closure commits and the card becomes closed.

### A2 — Subordinate completion closes only its obligation

Given card deliverable `D` and a default linked assignment whose subject creates
subordinate deliverable `S`, when the holder files completion, then the assignment
closes with a claim for `S`. When an authorized caller attempts card close with that
attest and no owner ruling, then the server returns
`completion_deliverable_mismatch`, writes no closure, and leaves the card open.

### A3 — A partial artifact is not a whole-card identity

Given the holder records a real `spec` artifact and completes a spec-writing assignment
bound to `S`, when card close selects that completion for card deliverable `D`, then the
artifact does not alter identity comparison. The close follows A2. The test fixture uses
the real artifact-record response shape, not a hand-written ideal response.

### A4 — The note cannot narrow or substitute

Given a card-bound assignment for `D`, when its holder files completion with note
“completed the spec only,” then the stored claim still names `D`, and the note remains
unchanged in audit readback. Given a subordinate assignment for `S` files note
“delivered D,” then its claim still names `S`. No note creates or changes a deliverable.

### A5 — Wrong holder and missing binding commit nothing

Given session B does not hold assignment A, when B files completion, then the existing
`not_holder` error wins and no attest or claim appears. Given a fault-injected runtime
fixture removes A's binding after boot, when the holder attempts completion, then the
server returns `assignment_deliverable_missing` and the entire I4 transaction rolls
back. Given an upgrade fixture contains zero or two candidate bindings for A, startup
returns `deliverable_contract_inconsistent` with detail
`assignment_deliverable_missing` or `assignment_deliverable_ambiguous`; it does not
choose one or serve commands.

### A6 — Different-card completion is refused

Given one principal can read cards C1 and C2 and each has a completed assignment, when
that authorized C1 closer selects C2's completion attest, then the server returns
`completion_claim_wrong_card`, reveals no C2 deliverable text, writes no C1 closure,
and leaves C1 open. Given the C1 closer cannot read C2, the same request returns
`completion_claim_not_found`, indistinguishable from an unknown attest id.

### A7 — Owner narrowing is explicit and atomic

Given a subordinate claim `S` belongs to card deliverable `D`, when the owner principal
closes with that attest and a nonblank owner ruling reason, then the card state and one
`basis='owner_narrowing'` closure commit in the same transaction. Readback shows D, S,
the exact reason, cause attest, acting principal, authorizing owner user, and time. Fault
injection at each write leaves both the card and closure absent or both committed.

### A8 — A wrong owner cannot narrow

Given an administrator owned by another user can perform an exact close, when that
administrator tries A7, then the server returns `owner_ruling_forbidden`, writes no
ruling or closure, and leaves the card open. Given the card owner supplies a blank
reason, the server returns `owner_ruling_required`. Given an exact claim supplies a
reason, the server returns `owner_ruling_not_applicable`.

### A9 — Completion retry is deterministic

Given completion succeeds with key K, when the same principal repeats K and the same
fingerprint, then it receives the original attest, claim, and assignment response and
attest, claim, and retry-receipt row counts stay one. The same assertion holds after a
process restart. When it repeats K with another note or commit refs, then it receives
`idempotency_conflict`. When it uses a different key after close, then it receives
`assignment_closed` and no second claim or retry receipt appears.

### A10 — Card-close retry is deterministic

Given a card close succeeds, when a currently authorized caller repeats the exact
fingerprint, then it receives the stored closure and closure and keyed-receipt row
counts stay one, including after restart. Owner-ruling data remains part of that one
closure row. When an authorized later request selects a different completion or reason,
then it receives `work_item_closed` and the stored closure remains unchanged.

### A11 — Completion and close race has one legal order

Run the close at the transaction probe before completion commits. Close returns
`completion_claim_not_found` and writes nothing; completion then commits; a close retry
succeeds. Reverse the probe order. Completion commits first and close succeeds. No run
produces an orphan claim, a closure without a claim, or two closures.

Given a subordinate claim already exists and the card's last open assignment is
card-bound, race that assignment's completion against an owner-narrowing close selecting
the subordinate claim. If narrowing serializes first, it returns `assignments_open` and
writes nothing; completion commits and a narrowing retry can close. If completion
serializes first, narrowing observes zero open assignments and can close. Then race that
narrowing request against an exact close selecting the new whole-card claim. Exactly one
closure commits; the other request returns `work_item_closed`.

### A12 — Competing terminal operations preserve one history

Race completion against surrender and revocation on one assignment. Exactly one terminal
operation wins. A winning completion has exactly one claim. A losing completion has zero
claims.
Race two different authorized card-close requests. Exactly one closure wins; the loser
receives `work_item_closed`. Race two identical closes; the loser receives the stored
closure.

### A13 — Reopen, restart, and replay

Given a completed assignment reopens, its old claim stays readable and no longer equals
the current closing attest. A close using it returns `completion_claim_stale`. A later
completion creates a new claim that can support close.

Given a legacy completed or surrendered assignment has no binding, when it reopens after
activation, then one subordinate binding from its stored subject commits in the reopen
transaction before the assignment becomes open. Its old attests and terminal values are
unchanged, no historical claim appears, and a later completion copies the new binding.

At each upgrade fault point—after table creation, after card backfill, after assignment
backfill, after validation, and before stamp update—restart yields the complete old shape
or complete new shape. Running the upgrade twice produces identical domain rows and one
stamp. Boot against a new stamp with a missing, duplicate, wrong-hash, or wrong-source
row returns `deliverable_contract_inconsistent` before serving commands.

### A14 — Historical rows are not rewritten

Given a captured predecessor database contains closed and failed cards; terminal
completed, surrendered, and revoked assignments; and an assignment that completed and
then reopened before activation, when the upgrade runs, then the byte values of those
domain rows and their attests match before and after. No claim or closure row appears for
their historical terminal transitions. The still-terminal objects use the legacy read
form in I13. The currently open reopened assignment receives the v1 subordinate binding,
while its old completion attest keeps `deliverableClaim:null`. An older binary refuses
the new shape stamp.

### A15 — Projections and privacy are exact

For create, update, assign, dispatch, completion, close, reopen-assignment,
work-item-get, work-item-list, assignments, attests, work-item-trace, and Toplines list
and detail, assert the exact additive projection in Architecture. Hash each projected
name independently and match the stored hash. A principal that cannot read the owning
card or assignment receives the existing non-disclosing error and no deliverable,
claim, reason, or owner field.

### A16 — Exact `wi_113442f5` non-recurrence

Capture the real work-item, assignment, attest, and trace response rows for
`wi_113442f5-22ae-457b-a971-1b620069d490` into a deterministic fixture. Preserve at
least the work-item title; the spec assignment id, subject, and work-item link; completion
attest id, kind, note, and commit ref; and the absence of any coder assignment.

Replay that shape under v1 by creating the card, opening the spec assignment without
`--delivers-work-item`, filing the spec artifact, closing each review obligation required
by installed completion rails, and then filing completion. The spec assignment closes
with its subordinate claim. Card close with that completion returns
`completion_deliverable_mismatch`; the card stays open and has no closure. The same replay
can close only after either a card-bound implementation assignment completes or the owner
records A7's explicit narrowing ruling.

## Open Questions

1. **BLOCKING FOR IMPLEMENTATION, NON-BLOCKING FOR THIS PROPOSAL — schema predecessor
   and target:** no product integration target is elected. Before any code assignment,
   the owner must select the exact Tightbeam base, allocate the successor shape stamp
   without colliding with another reviewed schema lane, and amend this canonical file
   with that base commit and stamp. The behavioral contract and independent spec review
   do not depend on that target choice.

No other questions are open. The proposal decides the MVP behavior, identity model,
authorization, transaction boundaries, replay, compatibility, projections, errors, and
regression contract.
