# Durable operational knowledge and successor inheritance

Status: FROZEN FOR INDEPENDENT EXACT-ARTIFACT REVIEW

Work item: `wi_c4f5112b-a8c4-43a2-b630-e35e933b1bf1`

Writer assignment: `asg_a9a35dc7-7d49-4c52-95a0-da9088b5ecc4`

Controlling product ruling: `art_ee8fb9f6`, SHA-256
`ecb727ef853eccb74597a11ff61eab0c6312b42936625651b33b1a4f16df7b2b`

Source baseline inspected: Tightbeam `origin/main`
`7a70a2f616363074514237b5bee48ba67c52e2ea`

## Goal

Give an agent durable, sourced operational knowledge that a successor can find,
read, and cite without turning that knowledge into substrate authority.

Add an auditable successor edge between two assignments on one work item. The
edge references the predecessor's original rows. It does not copy those rows.
It does not transfer identity, custody, credentials, roles, or policy powers.

Provide one explicit, one-use cleanup grant so a successor can revoke the named
open predecessor assignment when a principal that can already revoke both the
predecessor and successor assignments grants the action.

The load-bearing maxim is: **the substrate preserves and relates knowledge;
agents decide what the knowledge means.** This applies wisdom 6. The cleanup
grant applies wisdom 1 because its condition and action each leave typed rows.

Subtraction ruling: add the three narrow seams in this spec. Deleting durable
knowledge or successor continuity loses because the four recorded failures
block real work. Accepting the failures loses because they cause repeated
investigation and leave routine cleanup without an agent-reachable path. A
generic delegated-capability engine does not exist in this MVP.

## Non-Goals

- This spec does not add a `heuristic` attest kind. Reviewed guidance owns
  rebuttable defaults.
- This spec does not create or waive a floor, statute, rule, policy, or review
  verdict.
- This spec does not promote text into served guidance.
- This spec does not make a knowledge row satisfy a condition fact or an action
  gate.
- This spec does not inject inherited rows into a prompt, wake, or harness
  context.
- This spec does not copy predecessor rows into successor-owned rows.
- This spec does not transfer an assignment holder, assignment opener, role,
  session parent, credential, token, work-item owner, or review link.
- This spec does not add a generic delegation grammar for arbitrary verbs.
- This spec does not select a successor or infer succession from retirement,
  surrender, assignment order, shared role, shared owner, or elapsed time.
- This spec does not change the meaning of `progress`, `completion`,
  `surrender`, or `verdict` attests.
- This spec does not change the existing reviewed-guidance ceremony.
- This spec does not choose a deployment target, release line, or topology.

## Terms

- **Knowledge attest:** An `attests` row whose `kind` is `note` or `finding`.
  It belongs to one assignment and, through that assignment, one work item.
- **Note:** A sourced observation. Its text reports what the author observed.
  It carries no authority.
- **Finding:** An agent judgment tied to cited evidence and one work item. It
  carries no authority merely because Tightbeam stores it.
- **Evidence reference:** An ordered, typed reference from a knowledge attest
  to one existing `artifact` or `attest` in the same work item.
- **Currency relation:** An append-only `supersedes` or `revalidates` edge from
  a new knowledge attest to the current leaf of the same-kind knowledge chain.
- **Current leaf:** The knowledge attest in a currency chain with no incoming
  currency relation.
- **Revalidation:** A new knowledge attest that repeats the predecessor text
  byte for byte and cites fresh evidence. It records that an agent checked the
  statement again.
- **Successor inheritance:** An append-only reference edge from one predecessor
  assignment to one successor assignment on the same work item.
- **Exact-row selection:** An inheritance selection that names a non-empty set
  of original `note`, `finding`, or `verdict` attest IDs.
- **Predecessor-scope selection:** An inheritance selection that resolves the
  predecessor session's `note`, `finding`, and holder-filed `verdict` attests
  on the named work item when a reader queries the edge.
- **Successor assignment:** The explicit open obligation held by the successor
  session. It is new custody and authorization for its own stated subject. It
  is not inherited custody.
- **Cleanup grant:** An append-only authorization row for the sole action
  `revoke-predecessor-assignment`.
- **Grant use:** The append-only row written in the same transaction that uses
  a cleanup grant to revoke its target assignment.
- **Readable:** An authorized caller can query the original row and its
  provenance.
- **Citable:** The original stable ID can appear in an assignment, attest,
  artifact, wake, or report as evidence.
- **Executable:** A row can alter a refusal, authorize or gate a mutation,
  satisfy a condition, choose a wake, or modify served guidance. Knowledge
  attests and inheritance edges are not executable.

## Assumptions

1. Tightbeam main at `7a70a2f616363074514237b5bee48ba67c52e2ea`
   stores assignments, work items, attests, artifacts, review links, and
   assignment reopening history as durable rows.
2. The current `attests` vocabulary is `progress`, `completion`, `surrender`,
   and `verdict`.
3. The current `revoke-assignment` authorization accepts the assignment's user
   opener, its session opener, or an administrator. It rejects another
   session.
4. The current qualifying-review resolver selects the latest holder-filed
   verdict from a linked review. It does not require the review assignment to
   remain open.
5. `work-item-trace` authorizes the work-item owner, a session owned by that
   user, or an administrator. Unknown and unauthorized work items share the
   existing `not_found` response.
6. Session and assignment origin rows remain after retirement and closure.
7. Artifact and attest IDs resolve to one durable row or to an existing
   unknown-or-ambiguous refusal.
8. The existing serialized database transaction seam can validate and commit
   the row sets named below as one unit.
9. The five `dr_*` rows in the work-item trace are ruled historical input. They
   are not open implementation gates.

## Invariants

1. A knowledge attest affects no authorization, refusal, action gate,
   condition fact, wake target, prompt, served guidance, or assignment state.
2. A successor inheritance edge affects no authorization, refusal, action
   gate, condition fact, wake target, prompt, served guidance, or assignment
   state.
3. A read returns a knowledge attest's original author, source session,
   assignment, work item, evidence references, and creation time.
4. The system changes knowledge currency only through a committed
   `supersedes` or `revalidates` relation.
5. The system derives no currency or staleness state from age, author
   retirement, assignment closure, or successor creation.
6. One knowledge chain has one current leaf. A concurrent attempt to branch a
   chain loses with `knowledge_not_current` and writes no row.
7. A knowledge attest, its evidence references, and its optional currency
   relation commit in one transaction.
8. An inheritance row refers to original attest IDs. It stores no copy of
   their text, verdict, evidence list, or currency state.
9. An inheritance read applies the named work item's authorization before it
   returns edge or row content.
10. Creating an inheritance edge leaves the two assignments, their holders,
    their lifecycle state, their openers, and their review links unchanged.
11. The successor assignment is the only custody row for successor work. A
    surrendered predecessor assignment remains surrendered.
12. A cleanup grant becomes effective only for the named successor assignment,
    named predecessor assignment, and action
    `revoke-predecessor-assignment`.
13. A principal can create a cleanup grant only when the existing
    `revoke-assignment` authorization accepts that principal for both the
    predecessor target and the successor assignment.
14. A successor uses a cleanup grant only while its successor assignment and
    the target predecessor assignment are open.
15. Grant use and predecessor revocation commit in one transaction.
16. A holder-filed `reviewed-clean` verdict remains readable and eligible for
    the existing qualifying-review resolver after its review assignment
    closes. The inheritance edge is not the eligibility source.
17. The schema stores no heuristic, confidence score, priority, truth score,
    expiry, or age threshold for knowledge.
18. Each top-level mutation row written by this spec records its cause and
    typed principal. A child reference or selection row derives both fields
    through its immutable parent foreign key.

## Architecture

### 1. Existing authority and additive scope

This spec extends `attest-v1.md` and `work-item-v1.md`. It preserves the
current review-verdict resolver and the current assignment lifecycle. It adds
one knowledge mutation seam, one inheritance mutation seam, and one cleanup
grant/use seam.

`Assignments.attest` owns a knowledge attest, its evidence references, and its
currency relation. `SuccessorInheritance.create` owns an inheritance edge and
an exact-row selection. `SuccessorInheritance.grant_cleanup` owns a cleanup
grant. `Assignments.revoke` owns the atomic grant use and target revocation.
No second mutation seam writes those rows.

This spec establishes the pattern **reference inheritance** for operational
knowledge on one work item. It applies to `note`, `finding`, and citable
holder-filed `verdict` rows. It does not apply to credentials, role bindings,
assignment custody, policy, guidance, condition facts, or arbitrary artifacts.

This spec teaches no new agent guidance pattern. CLI help will describe the
mechanics. A later guidance change requires the existing reviewed guidance
path.

### 2. Knowledge attest contract

The CLI adds these fields to the existing command:

```text
tightbeam attest <asg_...> \
  --kind <note|finding> --note <text> \
  --evidence-refs '<json-array-of-{kind,id}>' \
  [--supersedes <att_...> | --revalidates <att_...>]
```

The CLI maps the three additive flags to wire fields `evidenceRefs`,
`supersedesAttestId`, and `revalidatesAttestId`.

R1. The `attest` verb accepts `kind=note` and `kind=finding` only when the
caller is the session that holds an open, work-item-linked assignment.

Check A1: Given holder `S` has open assignment `A` on work item `W`, when `S`
files a note with valid evidence, then Tightbeam returns one `att_` row whose
author, source session, assignment, and work item resolve to `S`, `A`, and `W`.

R2. A knowledge attest requires `note` text of 1 through 2,000 Unicode code
points and one through 32 typed evidence references.

Check A2: Given a request has zero evidence references, when the holder files
it, then Tightbeam returns `missing_evidence_refs` and writes no attest,
reference, or currency row.

R3. An evidence reference accepts `kind=artifact` with an `art_` ID or
`kind=attest` with an `att_` ID. The referenced row must resolve to the same
work item as the knowledge attest through the existing
`Assignments.resolved_work_item_id` seam.

Check A2: Given an evidence ID belongs to another work item, when the holder
files the knowledge attest, then Tightbeam returns `evidence_not_visible` and
writes nothing.

R4. `note` and `finding` accept neither `verdictKind` nor `commitRefs`.

Check A2: Given a finding carries either field, when the holder files it, then
Tightbeam returns `invalid_knowledge_field` and writes nothing.

R5. The response for a knowledge attest adds `workItemId`, `evidenceRefs`,
`currency`, `replacedByAttestId`, and `currentAttestId` to the existing attest
shape. Existing attest kinds retain their current response fields.

Check A1: Given a current note, when an authorized caller reads it, then
`currency=current`, `replacedByAttestId=null`, and `currentAttestId` equals the
note ID.

### 3. Evidence and currency model

The migration widens `attests.kind` to:

```text
progress | completion | surrender | verdict | note | finding
```

The `attests` table keeps the original immutable row. For `note` and
`finding`, `bySession` is required, `byUser` is null, `verdictKind` is null,
`commitRefs` is null, and `note` is required.

Add `knowledge_evidence_refs`:

```text
knowledgeAttestId  FK attests(id)
ordinal            integer >= 0
refKind            artifact | attest
refId               non-blank text
PRIMARY KEY (knowledgeAttestId, ordinal)
UNIQUE (knowledgeAttestId, refKind, refId)
```

The transaction resolves `refId` against the table selected by `refKind` and
validates the same-work-item condition before insert. The polymorphic child
row has no cross-table foreign key; transaction validation and the referenced
domain row are the existence proof. An artifact whose bytes are absent or
unverifiable remains a valid durable reference; its existing artifact state
is returned. The substrate does not convert availability into a judgment
about the knowledge text.

Add `knowledge_currency_relations`:

```text
successorAttestId    PK, FK attests(id)
predecessorAttestId  UNIQUE, FK attests(id)
relationKind         supersedes | revalidates
createdAt            epoch ms
```

R6. A currency relation connects two same-kind knowledge attests in one work
item. Its predecessor must be the current leaf when the transaction begins.

Check A3: Given two concurrent filings target one current leaf, when the
serialized transactions run, then one commits and the other returns
`knowledge_not_current` with no partial row.

R7. A `revalidates` relation requires the new attest text to equal the
predecessor text byte for byte. Its evidence set must contain at least one
typed reference absent from the predecessor's evidence set. A `supersedes`
relation permits different text.

Check A3: Given a revalidation changes one byte of text, when the holder files
it, then Tightbeam returns `revalidation_text_changed` and writes nothing.

R8. Reads derive `currency` from the relation graph. An immediate predecessor
of `supersedes` reports `superseded`. An immediate predecessor of
`revalidates` reports `revalidated`. A leaf reports `current`. Each row also
reports the chain's `currentAttestId`.

Check A3: Given a note is revalidated and its revalidation is later
superseded, when a caller reads the three rows, then the first reports
`revalidated`, the second reports `superseded`, the third reports `current`,
and the three report the third ID as `currentAttestId`.

R9. The public `attest` request accepts at most one of `supersedesAttestId` and
`revalidatesAttestId`.

Check A2: Given a request contains both fields, when the holder files it, then
Tightbeam returns `conflicting_currency_relation` and writes nothing.

### 4. Work-item visibility and reads

R10. A knowledge read uses the existing `work-item-trace` owner/admin
authorization. An unauthorized caller receives the existing indistinguishable
`not_found` response.

Check A4: Given two users own separate work items, when one user queries the
other item's knowledge through each new read surface, then each query returns
`not_found` and exposes no row ID, text, evidence ID, author, or count.

R11. `work-item-trace` adds two deterministic arrays:
`knowledgeAttests` ordered by `ts,id`, and `successorInheritances` ordered by
`createdAt,id`. Its timeline adds creation rows for knowledge currency,
inheritance, cleanup grant, and cleanup use.

Check A4: Given one row of each new type, when the owner reads the trace, then
the arrays and timeline identify the original IDs, typed principal, cause, and
creation time. A child evidence, currency, or selection row derives principal
and cause from its immutable parent.

R12. The existing `attests <assignment>` read returns `note` and `finding`
rows only when the caller passes the linked work item's knowledge-read
authorization. It preserves existing rows and ordering for a caller that does
not pass that authorization.

Check A4: Given an unauthorized caller can still use a legacy assignment read,
when it reads that assignment's attests, then lifecycle and verdict behavior
matches the baseline and no knowledge row appears.

### 5. Successor inheritance contract

The CLI adds:

```text
tightbeam successor-inherit \
  --predecessor-assignment <asg_...> \
  --successor-assignment <asg_...> \
  (--rows '<json-array-of-attest-ids>' | --predecessor-scope) \
  --reason <text> --key <idempotencyKey>

tightbeam successor-inheritance-get <inh_...>
```

The gateway verbs are `successor-inherit` and
`successor-inheritance-get`.

R13. `successor-inherit` requires two different assignments on one open work
item. The predecessor assignment may be open or closed. The successor
assignment must be open and its holder session must be active.

Check A5: Given a surrendered predecessor and an open successor on the same
work item, when an authorized principal creates an edge, then the edge commits
without reopening the predecessor or changing either assignment.

R14. The mutation accepts a user who owns the work item, an administrator, or
a session whose owning user owns the work item or is an administrator. It
rejects process and remedy principals.

Check A5: Given a session owned by another user, when it names the two
assignments, then Tightbeam returns `not_found` and writes no inheritance row.

R15. The mutation requires exactly one selection: `exact_rows` or
`predecessor_scope`.

Check A5: Given a request names both selections or neither selection, when the
principal submits it, then Tightbeam returns `invalid_inheritance_selection`
and writes nothing.

R16. `exact_rows` accepts a JSON array containing a non-empty unique set of
attest IDs. Each ID must identify a `note`, `finding`, or
holder-filed `verdict` attest from the named predecessor session on the named
work item. Its read follows a selected knowledge row's later currency chain on
that work item.

Check A6: Given one requested row was filed by another session, when the
principal submits the exact selection, then Tightbeam returns
`invalid_inherited_row` and writes nothing.

R17. `predecessor_scope` resolves the predecessor session's `note`, `finding`,
and holder-filed `verdict` attests on the work item at read time. It follows
currency chains to expose later supersession and revalidation rows on that
work item.

Check A6: Given a finding is added after the edge and later superseded, when an
authorized caller reads the edge, then the response includes the original and
successor row and identifies the current leaf.

R18. The inheritance row records `id`, `workItemId`,
`predecessorAssignmentId`, `predecessorSessionKey`,
`successorAssignmentId`, `successorSessionKey`, `selectionKind`, `reason`,
typed creator, `createdAt`, idempotency key, and request fingerprint. `reason`
contains 1 through 2,000 Unicode code points. `idempotencyKey` contains 1
through 200 characters. The request fingerprint is the lowercase SHA-256 of
the canonical JSON mutation parameters after excluding `idempotencyKey` and
the identity envelope.

Check A5: Given the create succeeds, when the owner reads the edge, then each
field equals the committed source row or request and neither session row has
changed.

R19. `successor-inheritance-get` returns the edge, its exact selection when
present, and `resolvedRows` ordered by original attest `ts,id`, followed by
each selected knowledge row's currency successors in chain order. The read
deduplicates an attest ID that two selected bases resolve to and retains its
first position under that order. Each item contains the original attest ID and
current provenance fields. The verb uses the work-item knowledge-read
authorization.

Check A6: Given the predecessor session retires after edge creation, when the
successor reads the edge, then the original rows and retired source session key
remain readable.

Add `successor_inheritances` and `successor_inheritance_rows`. The edge ID uses
the `inh_` prefix. Database constraints preserve typed creator columns and the
selection-kind shape. `successor_inheritance_rows` stores only edge ID and
attest ID.

An idempotent replay with the same typed principal, operation, key, and request
fingerprint returns the canonical edge. Reuse with a different fingerprint returns
`idempotency_conflict`.

### 6. Explicit successor cleanup authorization

The CLI adds:

```text
tightbeam successor-action-grant \
  --inheritance <inh_...> \
  --action revoke-predecessor-assignment \
  --target-assignment <asg_...> \
  --reason <text> --key <idempotencyKey>

tightbeam revoke-assignment <asg_...> --successor-grant <sag_...>
```

The gateway verb is `successor-action-grant`. `revoke-assignment` gains the
optional `successorGrantId` parameter.

R20. The sole MVP action kind is `revoke-predecessor-assignment`. Its target
must equal the inheritance edge's predecessor assignment. The predecessor and
successor assignments must both be open at grant creation. Its actor must
equal the holder of the edge's successor assignment.

Check A7: Given a grant names another assignment or another session attempts
to use it, when the request runs, then Tightbeam returns `grant_scope_mismatch`
and leaves the assignments and grant-use table unchanged.

R21. Grant creation calls the existing `revoke-assignment` authorization for
the target predecessor assignment and for the successor assignment. A
principal rejected by either check cannot create the grant. This lets the
grantor invalidate an unused grant through an existing lawful revocation path.

Check A7: Given the target was opened by session `P`, when unrelated session
`Q` tries to grant cleanup, then Tightbeam returns `not_authorized` and writes
nothing. Given the grantor can revoke the predecessor but not the successor,
grant creation returns the same refusal.

R22. A valid grant is usable only while the predecessor target and successor
assignment remain open. Closing either assignment makes the grant ineffective
without deleting its row.

Check A7: Given the successor assignment surrenders before grant use, when its
former holder supplies the grant, then Tightbeam returns
`successor_assignment_closed` and leaves the predecessor open.

R23. A successful grant use inserts one `successor_action_uses` row and revokes
the predecessor assignment in one transaction. The use records the grant,
action, target, successor assignment, acting session, cause, and time.

Check A8: Given fault injection after the use insert and before predecessor
closure, when the transaction aborts, then neither the use nor revocation is
visible. Given commit succeeds, both are visible.

R24. A used grant cannot execute again. A race between ordinary authorized
revocation and grant-backed revocation produces one revoked target and at most
one grant-use row.

Check A8: Given both calls race, when the serialized transactions finish, then
one returns the revoked assignment and the other returns
`assignment_closed`; no orphan use row exists.

Add `successor_action_grants` and `successor_action_uses`. Grant IDs use the
`sag_` prefix. A grant row records the inheritance, action, target assignment,
successor assignment, typed grantor, reason, creation time, idempotency key,
and fingerprint. A use row has `grantId` as its primary key.

A grant create replay uses the same typed-principal, operation, key, and
fingerprint contract as inheritance creation. Its reason, key, and fingerprint
use R18's bounds and derivation. A different fingerprint returns
`idempotency_conflict`.

This explicit grant is the only executable row introduced by this spec. A
knowledge attest or inheritance ID cannot occupy `successorGrantId`.

### 7. Existing reviewed-clean consumption

R25. The implementation preserves `Assignments.qualifying_review_verdict_kinds`
as the source for review eligibility. The resolver selects the original linked
review verdict without testing the review assignment's lifecycle state.

Check A16: Given a linked independent review files `reviewed-clean` and then
completes, when the producer gate queries eligibility, then the existing
resolver returns `reviewed-clean` from the original verdict row.

R26. An inheritance read may expose that verdict for citation. It does not
make the verdict eligible and it does not replace the original review link.

Check A16: Given an unrelated assignment inherits an exact `reviewed-clean`
row, when a gate queries that unrelated assignment, then the inheritance edge
does not satisfy the gate.

### 8. Non-executable interaction boundary

R27. The condition-fact matcher, statute evaluator, wake scheduler, prompt
composer, served-identity renderer, assignment-state derivation, work-item
state derivation, and review-verdict resolver do not query knowledge attests or
successor inheritance tables.

Check A9: Given a note or finding contains text matching a condition kind,
rule name, wake prompt, verdict kind, or guidance directive, when each consumer
runs, then its result matches a database with that knowledge row absent.

R28. Promotion to guidance requires the existing identity or kungfu edit,
review, and publication path. The promotion may cite the knowledge attest ID.
It does not mutate or relabel the source row.

Check A10: Given a finding is later cited by a reviewed guidance change, when
the identity publishes, then the finding remains `kind=finding` and the
guidance history names its own author and revision.

### 9. Errors, audit, migration, and compatibility

New refusals use the existing error envelope:

```text
missing_evidence_refs
invalid_evidence_refs
evidence_not_visible
invalid_knowledge_field
conflicting_currency_relation
knowledge_not_current
revalidation_text_changed
invalid_inheritance_selection
invalid_inherited_row
invalid_reason
invalid_idempotency_key
grant_scope_mismatch
successor_assignment_closed
idempotency_conflict
```

Unknown or unauthorized work-item-scoped rows return the existing `not_found`
shape. Existing assignment and attest errors retain their current codes.

R29. Each accepted mutation queues its existing firehose handoff on the domain
transaction and appends the existing accepted verb event through Dispatch
after the handler returns. The domain tables remain the record of truth if the
later event-log append fails under the existing Dispatch contract.

Check A11: Given event-log append fails after a committed knowledge attest,
when the caller receives the existing propagated audit error, then the attest,
evidence refs, and currency relation remain committed as one domain unit.

R30. Fresh schema and migration schema enforce the same kind, typed-principal,
selection, relation, and grant-use constraints. Migration preserves each
existing attest byte for byte.

Check A12: Given a pre-change database contains each current attest kind and a
closed reviewed-clean review, when migration runs, then the original rows and
resolver result match the pre-migration values and the new tables are empty.

R31. CLI JSON output stays wire-faithful. Help lists the two new command
families and the additive `attest` and `revoke-assignment` flags. The CLI does
not cache inherited rows or retry a mutation.

Check A13: Given each CLI form, when the CLI integration harness captures its
dispatch body, then the verb and camelCase parameters match this contract and
stdout contains the gateway's canonical JSON response.

The implementation must amend `cli-surface-v1.md` with the named consumers:
the durable-knowledge operating-history reader and explicit successor cleanup.
It must not amend agent guidance in the implementation lane.

### 10. Traceability

| Product need | Requirements | Acceptance |
|---|---|---|
| Durable note and finding vocabulary | R1-R5 | A1-A2 |
| Explicit supersession and revalidation | R6-R9 | A3 |
| Work-item-scoped visibility | R10-R12 | A4 |
| Auditable reference inheritance | R13-R19 | A5-A6 |
| Explicit cleanup authority | R20-R24 | A7-A8 |
| Closed-review verdict remains usable | R25-R26 | A16 |
| Readable and citable, not executable | R27-R28 | A9-A10 |
| Audit, migration, and CLI compatibility | R29-R31 | A11-A13 |
| Predecessor cleanup failure | R20-R24 | A14 |
| Surrendered-card authorization continuity | R13-R19 | A15 |
| Reviewed-clean consumption after closure | R25-R26 | A16 |
| Findings prevent investigation restart | R1-R19, R27 | A17 |

## Acceptance

### A1 — A sourced note and finding persist

Given active session `S` holds open assignment `A` on work item `W`, artifact
`art_E` belongs to `W`, and attest `att_E` belongs to `W`, when `S` files one
note citing `art_E` and one finding citing `att_E`, then Tightbeam stores two
attests and two ordered evidence rows. Each response names `S`, `A`, `W`, its
evidence, `currency=current`, and its own `currentAttestId`. `A` remains open.

### A2 — Invalid knowledge writes are atomic refusals

Given separate requests have no evidence, foreign-work-item evidence, both
currency fields, a verdict field, a commit reference, a closed assignment, or
a non-holder caller, when Tightbeam processes each request, then it returns the
specified refusal. Counts in `attests`, `knowledge_evidence_refs`, and
`knowledge_currency_relations` remain unchanged for each request.

### A3 — Currency is explicit and linear

Given note `N1` is current, when the holder revalidates it as `N2` with
byte-identical text and at least one evidence reference absent from `N1`, and
later supersedes `N2` as `N3`, then
the read reports `N1=revalidated`, `N2=superseded`, and `N3=current`. Each row
reports `N3` as `currentAttestId`. Advancing the clock changes no field. Two
concurrent attempts to replace `N3` produce one successor row and one
`knowledge_not_current` refusal.

### A4 — Work-item visibility contains knowledge

Given user `U1` owns `W1`, user `U2` owns `W2`, and each item has one finding,
when `U1` or a session owned by `U1` reads `W1`, then the finding and evidence
are visible. When that principal reads `W2` through work-item trace,
inheritance get, or assignment attests, then no `W2` knowledge ID, text,
evidence ID, author, or count is returned. An administrator can read both.

### A5 — Exact successor inheritance creates references, not copies

Given predecessor assignment `P` and open successor assignment `S` belong to
work item `W`, `P` is held by session `SP`, `S` is held by session `SS`, and
`P` contains note `N` and finding `F`, when an authorized principal creates an
exact-row inheritance for `[N,F]`, then one `inh_` row and two selection rows
commit. The response derives `SP` and `SS` from the assignments. Counts and
bytes in `attests`, `assignments`, `sessions`, roles, review links, and
credentials remain unchanged.
Replaying the exact request with the same typed principal and key returns the
same edge. Changing `reason` while reusing that tuple returns
`idempotency_conflict` and writes no row.

### A6 — Scoped inheritance follows original history

Given an edge selects `predecessor_scope`, when `SP` later files finding `F1`
on another `SP` assignment on `W` and a holder later supersedes `F1` with
`F2`, then an authorized inheritance read returns `F1`, `F2`, their authors,
evidence, currency relation, and `F2` as current. Retiring `SP` and closing `P`
does not remove those rows. The read stores no successor-owned copy.

### A7 — A cleanup grant has exact authority

Given opener session `O` can revoke open predecessor assignment `P`, successor
assignment `S` is open, `O` can also revoke `S`, and inheritance `I` connects `P` to `S`, when `O`
creates grant `G` for `revoke-predecessor-assignment`, then `G` names `I`,
`P`, `S`, `S`'s holder, `O`, cause, and creation time. Another target, another
actor, a closed `S`, and a principal that cannot revoke either `P` or `S` each
produce the specified refusal and no grant row. Replaying the exact request
with the same typed principal and key returns `G`. Changing `reason` while
reusing that tuple returns `idempotency_conflict` and writes no row.

### A8 — Cleanup use is one atomic action

Given A7 and the holder of `S` calls `revoke-assignment P --successor-grant G`,
when the transaction commits, then `P` is closed with outcome `revoked` and one
use row names `G`, `P`, `S`, and the acting session. Replaying `G` returns
`assignment_closed`. Fault injection and a race with ordinary revocation leave
no orphan use row and no double close.

### A9 — Knowledge and inheritance cannot execute

Given a note and finding contain exact text equal to a condition kind, rule
name, wake prompt, verdict kind, and guidance directive, when the condition
matcher, statute engine, wake scheduler, prompt composer, review resolver, and
identity renderer run, then their outputs equal the outputs from a database
without those two rows. Creating and reading an inheritance edge produces no
wake, prompt, condition, denial, assignment transition, or guidance revision.

### A10 — Guidance promotion keeps separate authority

Given finding `F` is current, when a separately authorized and reviewed
identity change cites `F`, then the identity revision carries its own author,
review, content hash, and publication event. `F` remains a finding with its
original author, evidence, work item, and creation time.

### A11 — Audit failure does not split a domain transaction

Given the event sink fails after the knowledge domain transaction commits,
when `attest` returns the existing audit failure, then the knowledge attest,
its evidence rows, and its optional currency relation are present together.
Given failure occurs before domain commit, none is present. The same pair of
checks applies to inheritance creation, grant creation, and grant use.

### A12 — Existing data migrates without reinterpretation

Given a database contains progress, completion, surrender, verdict, reopening,
review-link, and work-item rows, when migration completes, then each old row is
byte-equivalent through its public read. A closed linked `reviewed-clean`
verdict still qualifies. The migration creates no knowledge, inheritance,
grant, or use row.

### A13 — CLI and wire forms are exact

Given valid and invalid invocations of the new CLI forms, when the CLI harness
captures requests, then valid calls use the exact verbs and camelCase fields in
this spec. Invalid local syntax sends no request. Gateway refusals use stderr,
exit 1, and canonical JSON error details under the existing CLI convention.

### A14 — Observed failure 1: predecessor cleanup revocation authority

Given predecessor assignment `P` is open, its holder is unavailable, successor
assignment `S` is open, and the holder of `S` is neither an opener authorized
to revoke both assignments nor an administrator, when that holder calls
ordinary `revoke-assignment P`, then the existing `not_authorized` refusal
remains. When a shared authorized opener or an administrator creates exact
grant `G` after passing the existing revocation check for both `P` and `S`, and
the holder retries with `G`, then A8 closes `P` and records the grant use. No
principal authorized for both assignments and no explicit grant means no
revocation.

### A15 — Observed failure 2: authorization across a surrendered card

Given predecessor assignment `P` carried the prior work authorization and
settled evidence, `P` closes as `surrendered`, and an authorized expecter opens
successor assignment `S` on the same work item with its own subject and effect
kind, when the expecter creates an inheritance edge from `P` to `S`, then `P`
remains surrendered and `S` is the sole open custody row. The edge exposes the
original evidence and provenance so the successor can cite settled ground.
`S`'s assignment row is the explicit authorization for its stated successor
work; the edge transfers none of `P`'s verb rights. A privileged cleanup action
still requires A7.

### A16 — Observed failure 3: reviewed-clean after review closure

Given review assignment `R` links to producer assignment `P`, `R`'s holder
files verdict `V=reviewed-clean`, and `R` later completes, when the successor
inherits exact row `V`, then an authorized read returns `V` from `R` with its
author and review link. When `P`'s existing gate calls
`qualifying_review_verdict_kinds`, it returns `reviewed-clean` from `V` without
checking `R.state`. When an unrelated assignment inherits `V`, that edge does
not make `V` qualify for the unrelated assignment.

### A17 — Observed failure 4: findings prevent investigation restart

Given predecessor `SP` filed finding `F1` with evidence, revalidated it as
`F2`, and a successor edge selects predecessor scope, when successor `SS`
reads the edge before starting work, then it receives `F1`, `F2`, their
evidence, `F1=revalidated`, and `F2=current`. Tightbeam records the read only
through existing query audit behavior. It neither tells `SS` to accept the
finding nor starts an investigation. `SS` can cite `F2` in its own assignment
or filing and decide whether new evidence warrants more investigation.

## Open Questions

None. The five historical decision requests are ruled input. Independent
review of this exact artifact is the blocking next gate. Implementation,
targeting, binding, merging, release, deployment, and live-state mutation stay
out of scope until that review clears.
