# Completion attest card-deliverable contract — v1

Status: REVISED PROPOSAL after changes-requested verdict
`att_5de64b3e-640b-4e8b-8eab-b1998c6f8969` and review report
`art_81dbecca`, for one owner-routed independent re-review. No product target is
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
completion claim for its named card deliverable, unless the exact card product-owner
session, already authorized to close, records an explicit narrowing ruling in the same
close transaction.

For card closure, `kind=completion` asserts delivery of the card's named deliverable
only when the completed obligation was explicitly card-bound at assignment open. A
default subordinate completion terminates that obligation but is not a card-deliverable
completion. This distinction is stored before the holder acts; the completion note
cannot choose or change it.

The mechanism must prevent the `wi_113442f5` outcome: completing and reviewing only a
spec must not permit the work item for product implementation and legacy-read removal
to close without a product-owner narrowing ruling.

## Non-Goals

- The substrate does not decide whether bytes, artifacts, tests, or prose actually
  satisfy a named deliverable. A completion remains a holder assertion. Review and
  other installed completion rails decide whether required evidence exists.
- This spec does not parse a subject, title, note, artifact, verdict, prompt, or commit
  message for scope or quality.
- This spec does not change `kind=progress`, surrender, revocation, verdict meaning,
  completion-rail composition, completion notice routing, or session disposition.
- This spec does not add work-item or product hierarchy, phases, subtasks, percentages,
  automatic staffing, automatic work-item close, or a product-specific deliverable
  taxonomy. It records the existing product-owner spawn-tree boundary at assignment
  open; it does not create or modify that tree.
- This spec does not let a human work-item owner, administrator, holder, reviewer,
  process, or substrate narrow a card deliverable merely because it has that status.
  Only the exact product-owner session defined in Terms can do so.
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
- **Product-owner narrowing ruling:** The immutable part of a card-closure row that
  records the card deliverable, a different selected completion claim from the same
  card, a nonblank reason, and the exact product-owner session that made the ruling.
- **Product-owner session:** A custom session observed with
  `kind='custom'` and `archetype='product-owner'` in a validated holder-to-root spawn
  chain when the assignment's immutable product-lineage capture is created. A product
  is the subtree rooted at that session, using
  `sessions.spawnedBy` ancestry. A nested product-owner session roots a sub-product. The
  capture freezes the product-owner session keys; later retirement, archetype repointing,
  role rebinding, display-name change, or `operationalParent` change does not rewrite it.
- **Card product owner:** The deepest product-owner session present in every immutable
  product-lineage capture for assignments linked to the card at the instant of close.
  “Deepest” means no other common captured product-owner session is its descendant in
  the immutable spawn tree. This is the unique nearest common product-owner ancestor.
  The card product owner is unavailable when the validated captures have no common
  product-owner session or the selected session is retired. A missing capture or session
  row, ancestry cycle, cross-human-owner edge within one chain, wrong recorded distance,
  or more than one deepest candidate is contract corruption and returns
  `deliverable_contract_inconsistent`; it is not an unavailable owner. The handler does
  not guess or fall back to Main, a human owner, an administrator, a current archetype,
  or a role.
- **Acting principal:** The direct user id or session key that submitted a mutation. A
  closure stores exactly one of `closedByUser` and `closedBySession`. A product-owner
  narrowing stores the card product owner's exact session key separately; that key must
  equal `closedBySession`. Direct-user attribution cannot create a narrowing ruling.
- **Legacy terminal row:** A card or assignment that reached a terminal state before
  this contract's activation. Its old fields remain authoritative for that historical
  transition. It has no retroactive deliverable contract.
- **Canonical tuple encoding:** The byte encoding named `TBCD1` in Architecture. It has
  explicit type tags, unsigned lengths, null representation, and ordered lists.
- **Request fingerprint:** Lowercase hexadecimal SHA-256 over one canonical `TBCD1`
  tuple. For completion it covers assignment id, kind, note, and ordered commit refs.
  For card close it covers work-item id, selected completion-attest id, and nullable
  owner-ruling reason.

## Assumptions

1. The database owner serializes each mutation transaction.
2. `assignments.subject` and `work_items.title` are stored exactly after their existing
   validation. Neither field requires semantic normalization. No supported mutation
   changes an assignment's `holderKey` or `workItemId` after open.
3. A work item has one owning user in `work_items.ownerUserId`. No supported work-item
   mutation changes that owner. Human ownership remains relevant to existing exact-close
   authorization but does not confer product-owner narrowing authority.
4. Assignment completion already inserts the attest and closes the assignment in one
   guarded transaction. Work-item close already verifies that no assignment is open.
5. Assignment reopen preserves prior attests and makes a later completion attest the
   current `closingAttestId`.
6. Installed completion rails can require evidence, but they do not change which
   deliverable a completion claims.
7. Session rows used by assignment history persist. Their `sessionKey`, `spawnedBy`,
   `ownerUserId`, and `kind` do not change after creation. Archetype, state, role
   bindings, identity, display metadata, and `operationalParent` can change. Supported
   creation produces an acyclic spawn tree; lineage capture and close still validate the
   rows and fail closed on corruption.
8. Current product evidence was reconciled against
   `clickety-clacks/tightbeam` `origin/main` commit
   `cba8d6c5e43e974e93890a901b83abd55f723500`. Current spec evidence was reconciled
   against `clickety-clacks/tightbeam-specs` `origin/main` commit
   `45a650e25f334827e8238bfff3ea58e7a32b4916`.

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

Every assignment linked to a non-terminal v1 card also has exactly one immutable
product-lineage capture. The capture records its holder session and the ordered set of
product-owner session ancestors observed while walking the immutable `spawnedBy` chain.
New assignment open records it in the assignment transaction. Activation records it for
every existing assignment linked to a card that becomes v1, including legacy terminal
assignments, without changing those assignment rows or their terminal history. A valid
chain with no product-owner ancestor records an empty capture; narrowing is then
unavailable. A missing row, cycle, cross-human-owner edge, or ambiguous depth rejects
live assignment open or the shape upgrade instead of storing a guessed lineage.

### I3 — Completion copies; the holder does not choose

For a new `kind=completion` mutation, the server reads the obligation binding after
holder and open-state authorization. It inserts one completion claim with that exact
deliverable id.
The completion request has no deliverable text, id, override, phase, or narrowing field.
The note remains audit prose and cannot change the claim.

### I4 — A completion is structurally complete or commits nothing

The completion attest, completion claim whose `claimedAt` equals the attest timestamp,
guarded assignment close, work-item bracket update, supervision transition, effort
cancellation, and any installed completion-escalation domain record and first durable
wake commit in one transaction. A missing or inconsistent obligation binding aborts that
transaction. No attest, claim, assignment close, bracket mutation, transition,
cancellation, escalation record, or durable wake from that attempt remains.

Transcript and assignment markers are best-effort projections after that authoritative
transaction. Their failure does not roll back a committed completion, and no completion,
close, retry, or read decision depends on a marker. Reads derive truth from the domain
rows named above.

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
principal field, and the close time. No owner ruling reason or product-owner session is
accepted on an exact close.

### I7 — Only the exact card product owner can narrow at close

When the selected claim names a different deliverable from the same card, the close
transaction derives the card product owner from every immutable product-lineage capture
for assignments currently linked to the card.
The close commits only when the caller also passes existing close authorization, the
acting principal is that exact session, and it supplies `ownerRulingReason`. The reason
must contain 1..2000 nonblank characters. The closure row
records `basis='owner_narrowing'`, the card deliverable id, the accepted claim's
deliverable id, the completion attest, the exact reason, the exact authorizing
product-owner session key, the identical acting session key, and the close time.

A direct human user, holder descendant, human work-item owner, administrator, reviewer,
different product owner, another session that currently holds the same role, or Main
fallback cannot create the ruling merely because of that status.
If the exact product-owner session also holds an assignment, holder status adds no
authority; only a separate close request attributed to that exact session can narrow.
The derivation and closure use the same serialized close transaction, so an assignment
insert that commits first makes close return `assignments_open`; after that assignment
completes, its captured lineage participates in the common-owner calculation. A closure
that commits first makes the later assignment insert fail under the existing closed-card
guard.

### I8 — Claim, assignment, and card boundaries do not blur

Completing a subordinate obligation can close that assignment. It cannot close the card
without I7's product-owner ruling. Completing a card-bound obligation can support an
exact card close, but it does not close the card automatically. The explicit card-close
transaction remains the sole card terminal seam.

### I9 — Failures preserve open state

A different-card completion, a subordinate completion without a product-owner ruling,
a stale completion from before assignment reopen, a missing claim, an open assignment,
or an unauthorized ruling returns a typed error and writes no card-closure or ruling
row. The card remains in its prior state.

### I10 — Retries are row-idempotent

`work-item-create`, `assign`, and `dispatch` preserve their existing idempotency key
scope and original-row replay. After the minimum authentication, owner-scope, and key-
syntax checks needed to locate that receipt, a hit wins before validation or resolution
of a newly supplied title, subject, work-item reference, holder, files, or
`deliversWorkItem` value. It returns the original row with its original deliverable
projection and creates no deliverable, link, assignment, or wake for the replay.
The new payload cannot conflict with or rebind the original identity. A miss validates
the full request and commits the existing mutation, its deliverable rows and links, and
its idempotency receipt in one transaction.

`attest kind=completion` accepts optional `--key <idempotencyKey>`. Other attest kinds
reject that parameter. The first successful keyed completion stores its fingerprint and
canonical response in the deliverable-contract idempotency table in the same transaction
as I4. The same acting principal, operation, key, and fingerprint returns the original
response, including
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
a foreign card's existence, text, ids, product lineage, or principal.

### I15 — The substrate compares identities, not meaning

The substrate compares exact ids and verifies relational ownership. It does not decide
whether one text is a subset, phase, artifact, or semantic equivalent of another. The
card product owner's explicit ruling supplies the only judgment. This follows wisdom 6
and wisdom 9.

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
on completion and can support exact card close. The exact card product-owner session,
when already authorized to close, can instead close from `dlv_spec` only by recording a
product-owner narrowing ruling.

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

CREATE TABLE assignment_product_lineage_captures (
  assignmentId TEXT PRIMARY KEY REFERENCES assignments(id),
  workItemId TEXT NOT NULL REFERENCES work_items(id),
  holderSessionKey TEXT NOT NULL REFERENCES sessions(sessionKey),
  captureKind TEXT NOT NULL CHECK(captureKind IN ('assignment_open','activation')),
  UNIQUE(assignmentId, workItemId)
);

CREATE TABLE assignment_product_owner_ancestry (
  assignmentId TEXT NOT NULL
    REFERENCES assignment_product_lineage_captures(assignmentId),
  productOwnerSessionKey TEXT NOT NULL REFERENCES sessions(sessionKey),
  distance INTEGER NOT NULL CHECK(distance >= 0),
  PRIMARY KEY(assignmentId, productOwnerSessionKey),
  UNIQUE(assignmentId, distance)
);

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
  ownerRulingProductOwnerSessionKey TEXT NULL REFERENCES sessions(sessionKey),
  closedByUser TEXT NULL,
  closedBySession TEXT NULL,
  requestFingerprint TEXT NOT NULL
    CHECK(length(requestFingerprint)=64 AND requestFingerprint NOT GLOB '*[^0-9a-f]*'),
  closedAt INTEGER NOT NULL,
  CHECK((closedByUser IS NOT NULL) != (closedBySession IS NOT NULL)),
  CHECK(
    (basis='exact' AND cardDeliverableId=acceptedDeliverableId AND
      ownerRulingReason IS NULL AND ownerRulingProductOwnerSessionKey IS NULL) OR
    (basis='owner_narrowing' AND cardDeliverableId<>acceptedDeliverableId AND
      ownerRulingReason IS NOT NULL AND
      ownerRulingProductOwnerSessionKey IS NOT NULL AND
      closedByUser IS NULL AND
      closedBySession=ownerRulingProductOwnerSessionKey)
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

### Canonical tuple bytes and hashes

`TBCD1` encodes one value as the five ASCII bytes `TBCD1`, followed by that value. It
admits only these recursively encoded value types:

| Value | Bytes |
|---|---|
| null | tag `00` |
| UTF-8 string | tag `01`, unsigned 64-bit big-endian byte length, then the exact UTF-8 bytes |
| ordered list | tag `02`, unsigned 64-bit big-endian element count, then each encoded value in order |

Lengths count bytes, not Unicode scalar values. Empty string and empty list have zero
length or count. Numbers, booleans, maps, invalid UTF-8, negative lengths, truncated
values, trailing bytes, and values whose length cannot fit in unsigned 64 bits are
invalid. Encoders do not normalize, sort, trim, case-fold, or coerce a value.

The completion request tuple is exactly
`["attest-completion", assignmentId, "completion", note-or-null, commitRefs-or-null]`.
When commit refs are present, the last value is an ordered list in request and stored
order; each ref is the ordered list `[repo, commit]`. JSON map-key order therefore has
no effect, but changing ref-list order changes the fingerprint. Omitted `commitRefs`
encodes as null; an explicitly supplied empty list encodes as an empty list and is a
different request. The close tuple is exactly
`["work-item-close", workItemId, completionAttestId, ownerRulingReason-or-null]`.

Backfill hashes exactly
`["completion-attest-card-deliverable-v1", sourceKind, fullSourceId]`. For source kind
`work_item` and id `wi_example`, the complete encoded bytes are:

```text
5442434431020000000000000003010000000000000025636f6d706c6574696f6e2d6174746573742d636172642d64656c6976657261626c652d7631010000000000000009776f726b5f6974656d01000000000000000a77695f6578616d706c65
```

Their SHA-256 is
`e913ecd5b5031094cd75c65f30690aa321c539fd2651ba9b8f0f0b054d204295`, so the
backfill id is `dlv_e913ecd5b5031094cd75c65f30690aa321c539fd2651ba9b8f0f0b054d204295`.
The completion tuple with assignment `asg_example`, null note, and empty commit-ref list
hashes to `46cfdeffcfbd58706efd31e8c18c7e30e397b6a462009d17ece7c9a175bff524`.
The close tuple for `wi_example`, `att_example`, and reason `because` hashes to
`1286084e2da28c5728aee9e31687131b32fba61b2a54101eb0f3556e72865e7a`.

### Creation and activation

`work-item-create` inserts the card row, deliverable row, and work-item link in one
transaction. `assign` and `dispatch` insert the assignment, its deliverable row when
subordinate, its link, and—when linked to a card—its product-lineage capture and
zero-or-more ordered product-owner ancestry rows in their existing atomic open
transaction. `distance=0` denotes that the holder session itself is a product owner;
each `spawnedBy` edge adds one. Only ancestors whose captured session row has both
`kind='custom'` and `archetype='product-owner'` enter the ancestry table; Main is never
made a product owner by fallback or by archetype text alone.

All three seams apply I10's inherited replay ordering. A keyed `work-item-create` replay
returns the originally created card and immutable deliverable even if the retry supplies
a different or now-invalid title. A keyed `assign` or `dispatch` replay returns the
original assignment and binding even if the retry changes the subject, linked card,
holder, files, or `deliversWorkItem`. A replay never checks the new card state, opens a
second obligation, creates a second deliverable, changes subordinate to card-bound (or
the reverse), schedules a second delivery, or evaluates a rail for the new payload.

The shape upgrade backfills:

1. one card deliverable from the current title of each `open` or `iceboxed` work item;
2. one subordinate deliverable from the subject of each open assignment; and
3. one `captureKind='activation'` product-lineage capture for every assignment linked to
   an `open` or `iceboxed` card, including a legacy terminal assignment, using the
   session tree observed in the upgrade transaction; and
4. no deliverable for a legacy terminal assignment and no claim, closure, or ruling for
   a pre-activation attest or terminal row.

For backfill only, a deliverable id is `dlv_` plus the lowercase SHA-256 of the exact
`TBCD1` tuple defined above.
Live creation continues to use the product's ordinary random id generator. The upgrade
orders rows by full source id and verifies that every generated id is unique, so the same
captured predecessor fixture produces byte-identical backfill rows. It validates exact
cardinality, name hashes, foreign keys, and source-kind checks before it advances the
stamp. It also validates that each captured holder and work-item id equals the immutable
assignment row, each recorded distance matches the holder's `spawnedBy` chain, every
product-owner ancestor had both `kind='custom'` and `archetype='product-owner'` in the
captured transaction, and all required captures exist. A database containing a partial
or ambiguous prior deliverable or product-lineage table returns
`deliverable_contract_inconsistent`, names the table and source row id, and leaves the
predecessor stamp unchanged.

Backfilled card deliverables copy `work_items.createdAt` into `deliverables.createdAt`.
Backfilled assignment deliverables copy `assignments.openedAt`. Live rows use the
existing mutation timestamp. Product-lineage capture rows contain no wall-clock value;
`captureKind` says whether the observed tree came from assignment open or activation.
Thus retrying an interrupted upgrade cannot change bytes merely because time advanced.

### Mutation seams

After activation, four domain mutation seams can create rows defined by this contract.
The one-time shape upgrade in I16 is separate:

1. `work-item-create` establishes the immutable card deliverable.
2. The assignment-open seam establishes the immutable obligation binding. `assign` and
   `dispatch` call it for new assignments and record the linked assignment's immutable
   product-lineage capture. `reopen-assignment` calls it only when a legacy terminal
   assignment lacks a binding, before that assignment becomes open. If the assignment
   is linked to a v1 card and activation did not already record its required capture,
   reopen records that capture in the same transaction. An unlinked assignment has no
   product-lineage capture.
3. `attest kind=completion` copies that binding into an immutable completion claim.
4. `work-item-close` records either an exact closure or the exact card product owner's
   one-time narrowing ruling and closure.

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
or completion-rail evaluation and before note validation, commit-ref repository
verification, or producer-evidence checks. A same-key, different-fingerprint hit returns
`idempotency_conflict` before validating the changed payload. Only authentication, holder
authorization, key syntax, and canonical fingerprint encoding precede receipt lookup. A
miss preserves existing open-state authorization, validates the payload, then checks the
constitutional deliverable binding before it evaluates completion rails. A user,
process, non-holder session, or retired holder cannot file a new claim. A missing binding
cannot arm a remedy for a completion attempt that has no defined claim.

Card close preserves existing owner-or-admin admission. It checks that authorization
before selected-claim or product-lineage resolution. Product-owner status grants no new
read or close authority. A foreign principal receives the existing non-disclosing
authorization error.

After admission, the close transaction applies one total order: resolve the selected
claim under I14 visibility; verify current closing-attest and same-card relations; check
the zero-open-assignment guard; compare deliverable identities; then authorize and
validate any product-owner ruling. This order makes an absent or foreign claim win before
`assignments_open`, while an existing same-card claim with any open assignment returns
`assignments_open` before identity or ruling errors.

After those shared checks, exact identity requires existing owner-or-admin authorization
and rejects any reason as `owner_ruling_not_applicable`. A mismatch without a reason returns
`completion_deliverable_mismatch`. A mismatch with a reason requires the exact card
product-owner session; an admitted human owner, administrator, holder descendant, or
different product owner receives `owner_ruling_forbidden`. Valid captures with no common
owner or a retired common owner return `product_owner_unavailable`. Corrupt captures or
spawn relations return `deliverable_contract_inconsistent`; they never degrade to
unavailable. A foreign caller still receives the existing authorization error. Only
after exact product-owner authority succeeds does the handler validate the reason as
nonblank. Thus an authorized product owner with a blank reason receives
`owner_ruling_required`, while an unauthorized principal cannot use reason validation
as a product-membership oracle.

### Typed errors

| Code | Condition | Remedy |
|---|---|---|
| `deliverable_work_item_required` | `--delivers-work-item` names no linked card. | Link the assignment to a work item or omit the flag. |
| `product_owner_lineage_invalid` | Live linked-assignment open finds a missing session row, spawn cycle, cross-human-owner edge, or ambiguous distance while capturing lineage. | Preserve the card and repair the session registry through its supported path before assigning. |
| `assignment_deliverable_missing` | An open assignment has no binding after activation. | Stop and repair the incompatible database through the supported shape path. |
| `completion_attest_required` | A non-terminal card close omits the completion attest. | Name the exact current completion attest. |
| `completion_claim_not_found` | The selected attest or its claim is absent after authorization. | Complete the obligation, then retry with its exact attest. |
| `completion_claim_stale` | The selected attest is not the assignment's current closing attest. | Read the assignment and use the current completion. |
| `completion_claim_wrong_card` | The readable selected assignment is linked to another card or no card. | Select a completion from this card. |
| `completion_deliverable_mismatch` | The claim differs and `ownerRulingReason` is omitted. | Complete a card-bound obligation, or ask the card product owner to rule explicitly. |
| `owner_ruling_required` | The exact card product owner supplies a blank reason for a mismatch. | Supply the product owner's explicit reason. |
| `owner_ruling_forbidden` | An admitted caller is not the exact card product-owner session. | Route the close to that exact session if it also has existing close authority; otherwise complete the card deliverable exactly. |
| `product_owner_unavailable` | An admitted caller requests narrowing but valid captures have no common product owner or the one captured owner is retired. | Complete the card deliverable exactly; owner absence does not transfer narrowing authority. |
| `owner_ruling_not_applicable` | An exact close supplies a narrowing reason. | Remove the reason and close exactly. |
| `idempotency_key_not_applicable` | A non-completion attest supplies `idempotencyKey`. | Remove the key. |
| `idempotency_conflict` | A scoped key was reused with another fingerprint. | Read the stored result or use a new key for a new request. |
| `work_item_closed` | A later close conflicts with the stored closure. | Read the immutable closure. |
| `deliverable_contract_inconsistent` | Upgrade, boot, or an admitted mutation finds missing, duplicate, or mismatched contract rows. | Preserve the database and use the supported recovery path. |

Existing typed errors remain authoritative for earlier precedence steps, including
`not_holder`, `assignment_closed`, `not_authorized`, `assignments_open`,
`invalid_transition`, and ambiguous or unknown id errors.

### Read projections and audit

Every non-legacy work-item projection adds:

```json
{
  "deliverableContract": "v1",
  "deliverable": {"id":"dlv_...","name":"...","sha256":"..."},
  "cardProductOwner":{"sessionKey":"agent:...","status":"active"},
  "closure": null
}
```

`cardProductOwner` is derived only from immutable capture rows plus the selected session
row. Its exact status is `active`, `retired`, or `unavailable`. `active` and `retired`
include the one derived session key. `unavailable` uses `sessionKey:null` and means the
valid captures have no common product-owner session. Missing, cyclic, cross-owner,
wrong-distance, or ambiguous stored lineage is not projected: boot or the mutation
returns `deliverable_contract_inconsistent` and serves no partial read. Exact close
remains available when status is `retired` or `unavailable`. Narrowing requires `active`.

A closed v1 card replaces that null with:

```json
{
  "completionAttestId":"att_...",
  "cardDeliverable":{"id":"dlv_...","name":"...","sha256":"..."},
  "acceptedDeliverable":{"id":"dlv_...","name":"...","sha256":"..."},
  "basis":"exact",
  "ownerRulingReason":null,
  "ownerRulingProductOwnerSessionKey":null,
  "closedByUser":"owner",
  "closedBySession":null,
  "closedAt":123
}
```

Exactly one of `closedByUser` and `closedBySession` is nonnull. The two owner-ruling
fields are nonnull only for `basis='owner_narrowing'`. For that basis,
`basis` is `owner_narrowing`, `closedByUser` is null, and `closedBySession` and
`ownerRulingProductOwnerSessionKey` are byte-identical. The
persisted session and assignment ancestry rows let audit recompute the common
product-owner lineage without current archetypes, role bindings, display names, or
`operationalParent`.

Every non-legacy assignment projection adds:

```json
{
  "deliverableContract": "v1",
  "deliverable": {
    "id":"dlv_...", "name":"...", "sha256":"...",
    "sourceKind":"assignment|work_item", "sourceWorkItemId":null
  },
  "productLineage": {
    "holderSessionKey":"agent:...",
    "captureKind":"assignment_open|activation",
    "productOwnerAncestors":[
      {"sessionKey":"agent:...","distance":1}
    ]
  }
}
```

For `sourceKind='work_item'`, `sourceWorkItemId` is the linked work-item id. Each
ancestor list is in ascending numeric distance and can be empty. An unlinked assignment
projects `productLineage:null`. A legacy terminal assignment linked to a v1 card keeps
`deliverableContract:'legacy'` and `deliverable:null`, but projects the activation
lineage capture used for product-owner authority. Each
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

Existing keyed creation replay remains compatible: a replay returns the original card
or assignment and its original deliverable binding even when a newer client sends a
different `deliversWorkItem` value or other creation payload. The server does not apply
new binding validation to that replay.

After the capability ships, CLI help and the operating manual must teach one
pattern: completion claims the stored assignment deliverable; use
`--delivers-work-item` only when that obligation delivers the whole card; card close
names the completion attest; only the exact card product-owner session can record a
narrower close. The same guidance must warn that `work-item-update --title` changes only
the display title: the original deliverable id, name, and hash remain authoritative. It
must direct an opener who named the wrong deliverable to fail or icebox that card and
create a correctly named replacement; retitle is not a repair. Guidance must land with
the implemented commands, not with this proposal (wisdom 20 and wisdom 21).

### Subtraction ruling

ADD wins because the rows currently cannot distinguish a whole-card completion from a
subordinate completion. DELETE loses because removing work-item close would remove the
explicit card terminal lifecycle seam. ACCEPT loses because the demonstrated regression
makes “completed” materially false without a named refusal or ruling. The design adds only
immutable identities, captured existing product lineage, claims, one closure row, and
keyed retry receipts; it adds no adjudicator or mutable scope engine. Deriving lineage
only at close loses durable proof when session metadata changes, and accepting mutable
inference would let authority drift, so the immutable assignment-time capture is the
smallest row that preserves the existing product boundary.

Within that addition, DELETE wins for marker atomicity: markers are removed from the
authoritative transaction set because domain rows already decide every state and read.
Making best-effort markers strict would add failure coupling without truth; deleting
markers entirely would lose useful operator projection. Marker absence is therefore an
accepted, visible projection failure, never an ambiguous domain outcome.

### Traceability

| Requirement | Mechanism | Acceptance |
|---|---|---|
| Completion binds to stored scope atomically | I2-I4; completion claim | A1-A5 |
| Partial or different work cannot close a card silently | I5-I9 | A2, A3, A6, A7 |
| Only the durable card product owner can narrow | I7; immutable session ancestry | A7, A8, A11 |
| Tuple identity and request replay are byte-deterministic | `TBCD1`; I10, I16 | A9, A13 |
| Creation retries preserve original scope | I10; creation replay precedence | A17 |
| Races and replay keep one history | I10-I12 | A9-A12 |
| Reopen, restart, and history remain truthful | I12, I13, I16; reopen and shape upgrade | A13, A14 |
| Reads are exact and private | I14; stored projections | A15 |
| Retitle cannot mutate or repair the card deliverable | I1; replacement repair | A15 |
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
attest and no product-owner ruling, then the server returns
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

For a keyed completion with all optional installed completion rails active, inject one
deterministic database failure immediately before each applicable authoritative write:
completion attest, completion claim, guarded assignment-state update, work-item bracket
mutation, supervision transition, effort cancellation, completion-escalation record,
first durable escalation wake, and keyed idempotency receipt. At every probe, the call
fails and the before/after database snapshots for all these rows and states are
byte-identical; the assignment remains open. Then inject failure only in each
post-commit transcript or assignment-marker callback. Completion still commits exactly
once, the failed marker may be absent, and every read derives the same completed state,
claim, and retry response from authoritative rows.

### A6 — Different-card completion is refused

Given one principal can read cards C1 and C2 and each has a completed assignment, when
that authorized C1 closer selects C2's completion attest, then the server returns
`completion_claim_wrong_card`, reveals no C2 deliverable text, writes no C1 closure,
and leaves C1 open. Given the C1 closer cannot read C2, the same request returns
`completion_claim_not_found`, indistinguishable from an unknown attest id.

### A7 — Product-owner narrowing is explicit and atomic

Given a subordinate claim `S` belongs to card deliverable `D`, and all linked assignment
captures have exact nearest common product-owner ancestor P, and P passes existing close
authorization, when session P closes with that attest and a nonblank owner ruling reason,
then the card state and one `basis='owner_narrowing'` closure commit in the same
transaction. Readback shows D, S, the exact reason, cause
attest, `closedBySession=P`, `ownerRulingProductOwnerSessionKey=P`, and time. Fault
injection before the card state write, closure write, or keyed receipt leaves the card,
closure, and receipt all absent or all committed.

### A8 — Wrong, changed, absent, and cross-product authority fail closed

Given P is the card product owner, independently try A7 as the direct human work-item
owner, an administrator, a non-P assignment holder, another descendant session, a
reviewer, a sibling product-owner session, Main, and another session currently bound to
P's role. Configure each wrong actor to pass existing close admission; every attempt
returns `owner_ruling_forbidden`, writes no ruling or closure, and leaves the card open.
A foreign actor that fails existing admission receives the existing non-disclosing
authorization error instead. Rebinding the role or changing `operationalParent` changes
none of those results. Changing P's current archetype metadata does not rewrite the
capture or confer authority on another session. Retiring P makes product-owner narrowing
unavailable because P can no longer act; it does not transfer authority, and an admitted
human owner receives `product_owner_unavailable`. P with a blank reason
receives `owner_ruling_required`. An exact claim with a reason receives
`owner_ruling_not_applicable` under existing exact-close authorization.

Place one assignment holder in each of two sibling sub-product trees under parent
product owner P. P is the nearest common product owner and either child product owner is
forbidden. Place all holders inside one child tree; that child product owner is required
instead of P. Add and complete a new linked assignment under the sibling tree before
close; authority changes from the child to P in that close transaction, the child is
forbidden, and P can rule. Place holders in valid captures under product-owner roots with
no common product-owner ancestor, including roots owned by different humans; an admitted
human owner or administrator receives `product_owner_unavailable`, no ruling commits,
and exact close from an exact claim remains available. A foreign caller receives the
existing non-disclosing authorization error. Separately inject a missing capture or
session row, ancestry cycle, cross-human-owner edge inside one chain, wrong distance, or
ambiguous deepest candidate. Boot or close returns
`deliverable_contract_inconsistent`, writes nothing, and does not project partial
lineage or owner status.

### A9 — Completion retry is deterministic

Given completion succeeds with key K, when the same principal repeats K and the same
fingerprint, then it receives the original attest, claim, and assignment response and
attest, claim, and retry-receipt row counts stay one. The same assertion holds after a
process restart. When it repeats K with another note or commit refs, then it receives
`idempotency_conflict`. When it uses a different key after close, then it receives
`assignment_closed` and no second claim or retry receipt appears.

After the original commit-ref repository or commit becomes unavailable, repeat K with
the original payload. The stored response still wins and no repository probe runs.
Repeat K with a different invalid note or unverifiable commit ref; fingerprint conflict
wins before payload validation or repository I/O.

An independent test encoder must reproduce all three golden hashes in Canonical tuple
bytes and hashes. It must also distinguish null from empty string, null from empty list,
the UTF-8 byte lengths of `e` and `é`, reordered commit refs, and a changed `repo` or
`commit`. The service must store exactly those independently computed fingerprints.

### A10 — Card-close retry is deterministic

Given a card close succeeds, when a currently authorized caller repeats the exact
fingerprint, then it receives the stored closure, and closure and keyed-receipt row
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

Race a child product owner's narrowing against creation of a new linked assignment in a
sibling sub-product; make the child session also pass the existing human-owner admission
check. If narrowing serializes first, the card closes and the assignment
creation receives the existing closed-card refusal. If assignment creation serializes
first, the child narrowing receives `assignments_open`. After the new holder completes
that assignment, a child retry receives `owner_ruling_forbidden`, and the now-common
parent product owner can retry. No order records the child as authorizer after the
sibling assignment exists.

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
backfill, after product-lineage capture, after validation, and before stamp update—restart
yields the complete old shape or complete new shape. Running the upgrade twice produces
identical domain rows and one stamp. Boot against a new stamp with a missing, duplicate,
wrong-hash, wrong-source, wrong-holder, wrong-card, wrong-distance, or missing lineage-
capture row returns `deliverable_contract_inconsistent` before serving commands.

The backfill fixture containing `work_item` source `wi_example` must produce the exact
encoded bytes, hash, and `dlv_` id in Canonical tuple bytes and hashes. A second upgrade
implementation that independently encodes the same tuple must produce byte-identical
rows.

### A14 — Historical rows are not rewritten

Given a captured predecessor database contains closed and failed cards; terminal
completed, surrendered, and revoked assignments; and an assignment that completed and
then reopened before activation, when the upgrade runs, then the byte values of those
domain rows and their attests match before and after. No claim or closure row appears for
their historical terminal transitions. The still-terminal objects use the legacy read
form in I13. The currently open reopened assignment receives the v1 subordinate binding,
while its old completion attest keeps `deliverableClaim:null`. An older binary refuses
the new shape stamp. A legacy terminal assignment linked to a card that becomes v1 may
receive only the `captureKind='activation'` product-lineage companion row required to
identify the card's current product; its assignment, attests, deliverable contract, and
terminal projections remain legacy and byte-unchanged.

### A15 — Projections and privacy are exact

For create, update, assign, dispatch, completion, close, reopen-assignment,
work-item-get, work-item-list, assignments, attests, work-item-trace, and Toplines list
and detail, assert the exact additive projection in Architecture. Hash each projected
name independently and match the stored hash. A principal that cannot read the owning
card or assignment receives the existing non-disclosing error and no deliverable,
claim, reason, or product-owner field.

Given a new card is created with title A, capture the exact deliverable id, name, hash,
and projection bytes. When `work-item-update --title B` succeeds, then the display title
reads B, while every deliverable field and its projection bytes remain identical to the
captured A values. A later `assign|dispatch --delivers-work-item` binds A's unchanged
deliverable, and close compares against A. The supported repair for a wrong original
deliverable is to fail or icebox that card and create a replacement; retitle never
repairs or changes the obligation.

Build nested, sibling, empty, retired, and valid cross-root lineage fixtures. Assert the
exact `cardProductOwner` status and session key, each assignment's ascending-distance
capture, and the same values across get, list, trace, Toplines, restart, and keyed replay.
Later archetype, role, display, or `operationalParent` changes leave the capture bytes
unchanged. For missing-row, cyclic, cross-owner-edge, wrong-distance, and ambiguous
fixtures, assert `deliverable_contract_inconsistent` before reads are served.

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
can close only after either a card-bound implementation assignment completes or the card
product owner records A7's explicit narrowing ruling.

### A17 — Creation replay preserves the original binding

Create card A with key K, then repeat K with a different and independently invalid title.
The replay returns card A and its original deliverable projection; row counts for cards,
deliverables, links, and routing wakes remain one. Restart and repeat to obtain the same
result.

For both `assign` and `dispatch`, first create a keyed subordinate assignment. Repeat its
key while changing the subject, linked card, holder, files, and
`deliversWorkItem=true`. The replay returns the original assignment with its original
subordinate deliverable and original card link; no card-bound link, second deliverable,
assignment, product-lineage capture, ancestry set, delivery, or wake appears. The
original capture and ancestry bytes remain unchanged. Repeat the inverse fixture: first
create a keyed card-bound assignment, then retry as subordinate and against a different
card. The
original card deliverable remains bound. Run both directions after restart and after
the newly supplied card becomes terminal. The existing receipt wins in every case. A
different key follows normal validation and open-card guards and cannot mutate the first
binding.

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
