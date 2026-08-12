# Merge-readiness approval handoff

Status: **SPEC-READY FOR INDEPENDENT REVIEW**.

Work item: `wi_ab7d8496-a7b7-4076-ade5-1b2144a2a400`  
Authority: parent assignment `asg_bbfa003a-c1c2-4e07-8abe-11947aeb5d8e`  
Recon: artifact `art_108f9266`, inspected Tightbeam commit
`ac8651dcb104f312da1c67e0cb7b1abebc640b2b`

This spec does not authorize implementation until an independent reviewer clears its
exact content hash. The orchestrator binds the work item to the cleared hash after that
verdict.

## Goal

Tightbeam gives the effective parent one durable approval notice when one code-producing
assignment becomes ready to merge to main.

The assignment becomes ready only when these rows carry canonical commit references and
agree on one exact repository and commit:

1. The producer holder files the authoritative `tests-passed` verdict.
2. An independent linked review has a final holder-filed `reviewed-clean` verdict.
3. The producer holder files completion with the same canonical commit reference.

Tightbeam commits the completion, readiness record, and parent notice in one database
transaction. The notice tells the parent that the exact work is ready for its authorized
merge step. The notice does not perform that step.

The pattern established here is **Atomic Merge-readiness Approval Handoff**. It applies
only to assignments with `effectKind='code'`. It does not apply to policy, release,
live-mutation, review, evidence, or coordination assignments.

This rail implements substrate law over typed rows. The substrate compares identities,
records the result, and routes the notice. A parent or user decides whether and when to
merge (wisdom 1, 5, 6, 8, 9, and 26).

## Non-Goals

- No Git merge, rebase, cherry-pick, push, branch deletion, or main-branch mutation.
- No deployment, release, promotion, configuration change, or live-system mutation.
- No approval decision beyond the recorded `reviewed-clean` verdict.
- No inference about code quality, test coverage, reviewer quality, or merge strategy.
- No readiness notice for an effect other than `code`.
- No parsing of assignment subjects, attest notes, review prose, prompts, or role names.
- No replacement for the current review-completion or test-before-review rails.
- No new retry scheduler, replay sweeper, cursor, role, decision request, or standing fact.
- No retroactive notice for a completion that committed before this feature became live.
- No duplicate notice for a later review round on the same completed producer assignment.
- No user-interface design beyond the stored prompt and existing trace projection.
- No implementation of the operational-parent feature inside this work item.

**Subtraction ruling:** ADD wins because the required typed approval notice does not
exist. DELETE loses because it removes the requested handoff. ACCEPT loses because a
missing handoff leaves reviewed work undiscoverable. The design adds one focused row and
one ordinary wake. It does not add a sweeper because the final qualifying event is the
completion transaction itself.

## Terms

- **Producer assignment**: an assignment whose durable `effectKind` is exactly `code`.
  The term does not derive from the holder's archetype or the assignment subject.
- **Producer holder**: the exact session in `assignments.holderKey` for the producer
  assignment.
- **Commit reference**: one existing structured `commitRefs` entry with exact keys
  `repo` and `commit`. The existing validator proves that `repo` is
  `host:absolute-path` and that `commit` names a Git object in that repository.
- **Canonical commit reference**: a commit reference for which
  `git rev-parse --verify <filed-commit>^{commit}` returns a full lowercase object id that
  byte-equals the filed `commit`. A branch, tag, abbreviated object id, uppercase object
  id, tree, blob, or missing object is not canonical.
- **Exact commit**: the ordered pair `{repo, commit}` from one canonical commit reference.
  Equality requires byte-for-byte equality of both stored values after canonical
  validation.
- **Authoritative test outcome**: the newest producer-holder verdict on the producer
  assignment whose kind is `tests-passed` or `tests-invalidated`. Tightbeam orders these
  rows by `(ts, rowid)` descending.
- **Authoritative test receipt**: an authoritative test outcome whose kind is
  `tests-passed` and whose one canonical commit reference equals the completion commit.
- **Selected review**: the newest assignment linked to the producer through
  `reviewsAssignmentId`. Tightbeam orders review cards by `(openedAt, rowid)` descending.
- **Final review verdict**: the newest verdict on the selected review that its holder
  filed when the completion transaction reads the review. Tightbeam orders those rows by
  `(ts, rowid)` descending.
- **Independent review**: a selected review whose holder session differs from the
  producer holder session.
- **Effective parent**: the first active session on the producer holder's
  `operationalParent` chain. Resolution begins at the holder's `operationalParent`.
  Resolution skips retired sessions. An active Main self-root can be the result.
- **Readiness cause**: the producer's completion attest. Existing rails require the test
  and clean-review rows before completion, so completion is the final qualifying event.
- **Cause principal**: the producer holder that filed the readiness cause. The stored
  typed form is `{kind='session', id=<producer-holder-session-key>}`.
- **Readiness notice**: one `merge_readiness_notices` row and its linked prompt wake.
  The row is the structured truth. The prompt is its agent-facing projection.
- **Readiness identity**: `merge-readiness:<completion-attest-id>`. This value is the
  notice dedupe key and the basis for the deterministic wake id.
- **Approval handoff**: the atomic commit of a readiness notice addressed to the
  effective parent. It is not proof that the parent ran a turn. It is not permission for
  the substrate to mutate a repository.

## Assumptions

1. The database owner serializes mutation transactions.
2. One completion attest closes one open assignment exactly once.
3. Existing review rails require a qualifying linked review before code completion.
4. Existing dispatch rails require the producer holder to file `tests-passed` before a
   linked review opens.
5. `commitRefs` already stores structured repository and object identities on producer
   completion and linked-review verdict rows. Its current validator proves object
   existence, not canonical commit identity.
6. Session rows persist after retirement.
7. The operational-parent dependency makes `sessions.operationalParent` total, keeps
   Main as an active self-root, rejects cycles, and keeps `spawnedBy` as provenance.
8. The ordinary wake store can insert a caller-supplied wake id inside another database
   transaction.
9. A prompt wake can name its target session, assignment, work item, origin, and prompt
   without parsing prompt text later.
10. A code-producing assignment that can qualify has one direct work item. A missing
    work item is a named completion refusal under I9.

Assumption 7 is a build dependency, not current behavior at recon commit `ac8651dc`.
Candidate commit `fa4905922119c336f6b0e4016c18a8e4a8cf2c6b` supplies the required
field, migration, setter, cycle refusal, and active-ancestor pattern. It is not authority
until it is rebased, reviewed, and merged.

## Invariants

### I1. Exact scope

`MergeReadiness` evaluates only an assignment with `effectKind='code'` during that
assignment's completion transaction. Another effect follows its existing completion
path and creates no merge-readiness row or wake.

The handler reads `effectKind`. It does not infer scope from a role, file extension,
subject, work-item title, or note.

### I2. One exact commit across three attest rows

The completion attest, authoritative test receipt, and final review verdict each carry
exactly one canonical commit reference. Their `{repo, commit}` pairs are equal.

`Assignments` applies this rule when it files a code completion, a producer-holder
`tests-passed` or `tests-invalidated` verdict for code, or a review-holder
`reviewed-clean` verdict linked to code. It refuses zero or multiple references with
`merge_readiness_exact_commit_required` and inserts no attest.

For each such filing, `Assignments` uses the existing host-aware repository seam to run
`git rev-parse --verify <filed-commit>^{commit}`. Canonical validation requires the
returned full lowercase object id to byte-equal the filed `commit`. The filing seam
rejects a noncanonical value with `unverifiable_commit_ref` and inserts no attest.

During completion, `MergeReadiness` revalidates the selected test and review references
through the same seam before its first database write. This check prevents a structured
row filed before feature activation from bypassing canonical validation. A test row that
fails cardinality or canonical revalidation follows I3. A review row that fails either
check follows I4.

After revalidation, the readiness handler compares stored values byte for byte.

### I3. Typed test receipt and invalidation

For a code producer, `Assignments` requires exactly one canonical commit reference on a
producer-holder verdict with kind `tests-passed` or `tests-invalidated`. It rejects a
missing or multiple reference. It rejects either verdict kind from another principal
when that call supplies `commitRefs`.

A `tests-invalidated` filing requires a nonblank note that names why the earlier receipt
is no longer current. The verdict row remains the typed invalidation. The note is only
its explanation.

The newest row across those two kinds is the authoritative test outcome. A newest
`tests-invalidated` row prevents readiness. A newest `tests-passed` row for another
commit also prevents readiness. The holder uses `tests-invalidated` when a later result
withdraws an earlier passing receipt for the same or a newer commit.

The completion handler refuses an absent, non-passing, noncanonical, multiple-reference,
or non-matching authoritative outcome with `merge_readiness_tests_not_current`. The
response names this remedy: file a current holder `tests-passed` verdict with one
canonical reference for the exact completion commit, then retry completion.

Existing note-only test verdicts remain stored. They do not qualify this rail.

### I4. Latest independent review controls

The selected review follows the existing newest-card order `(openedAt, rowid)`. The
final review verdict is the newest holder verdict by `(ts, rowid)` that has been filed
when the completion transaction reads the review.

The selected review holder differs from the producer holder. When the selected review
links to a code producer, `Assignments` requires its holder to file exactly one canonical
commit reference with `reviewed-clean`. The selected final verdict is `reviewed-clean`,
and its commit reference equals the completion commit.

An older clean review cannot override a newer review card. An older clean verdict on
the selected card cannot override a newer `changes-requested` verdict. A verdict from a
user or another session cannot override the review holder's final verdict.

The existing review-completion rail runs first and keeps its current error contracts.
If that rail passes but the selected stored clean verdict does not carry exactly one
canonical commit reference equal to the completion commit, the completion handler uses
`merge_readiness_review_commit_mismatch`. The response names this remedy: obtain
holder-filed `reviewed-clean` for the exact completion commit, then retry completion.

### I5. Effective-parent resolution uses operational authority

The completion transaction starts at the producer holder's `operationalParent`. It
follows every durable `operationalParent` link until it finds the first active session.
It skips retired sessions. The walk ends at an active session or the active Main self-root.

The resolver has no elapsed-time, row-count, or hop threshold. It does not read
`spawnedBy`, roles, session names, prompts, or work-item causal edges.

A missing row, cycle, or inactive Main is corrupt state. The handler refuses completion
with `merge_readiness_parent_unavailable`. The response names this remedy: restore or
reparent the operational chain, then retry.

The completion transaction stores the resolved session. A later reparent or retirement
does not rewrite the historical notice target.

### I6. Check and handoff form one transaction

The handler checks I1-I5 and inserts the following state in one database transaction:

1. The completion attest.
2. The guarded assignment close.
3. The readiness notice row.
4. The immediate prompt wake for the effective parent.
5. Existing completion markers and transitions.

The transaction commits all five results or none. No post-commit callback creates the
initial notice. An observer cannot read a completion without its required readiness row
and wake.

This atomic boundary replaces recon gap 10's sweeper option. The design needs no cursor
because existing rails make completion the final conjunct.

### I7. Stable one-shot identity

The notice dedupe key is `merge-readiness:<completion-attest-id>`. The wake id is
`merge-readiness-notice:<completion-attest-id>`.

The notice table has unique constraints on `dedupeKey`, `completionAttestId`,
`producerAssignmentId`, and `wakeId`. The wake store keeps its existing unique wake id.
These constraints make a second notice for the same completion unrepresentable.

`MergeReadiness.open_in_txn/2` treats a repeated `completionAttestId` as an exact replay
only when these proposed values equal the existing row: readiness identity, cause,
principal kind and id, producer assignment, work item, repository, commit, test verdict,
review assignment, clean verdict, recipient, and wake id. It returns the existing row and
reuses its wake id without updating either row.

A caller-proposed notice id or creation time does not participate in replay equality.
The function ignores those proposed values on an exact replay and returns the original
notice id and `createdAt`.

If any compared field differs, the function refuses with
`merge_readiness_replay_conflict`. The response names each unequal field. The transaction
does not update the notice and does not insert, replace, or reschedule a wake.

Restart, duplicate callbacks, and concurrent completion calls create one exact notice and
one wake. A later review round cannot create another notice for the closed producer.

### I8. Cause, principal, and evidence are explicit

Each readiness row stores these values in typed columns:

1. The readiness identity.
2. The completion attest as cause.
3. The producer holder as cause principal.
4. The producer assignment.
5. The producer work item.
6. The exact repository and commit.
7. The authoritative test verdict.
8. The selected review assignment.
9. The final `reviewed-clean` verdict.
10. The effective parent.
11. The prompt wake.
12. The creation time.

The wake origin and message sender are `process:tightbeam`. The cause principal remains
the holder session. The system does not derive either value from prose.

### I9. Silence and named refusal

Before I1-I5 pass, Tightbeam writes no merge-readiness notice, wake, prompt, or lifecycle
event. A completion refusal returns one typed error and its remedy to the caller.

The rail refuses a code completion when the producer lacks a work item. It uses
`merge_readiness_work_item_required`. The response tells the caller to replace the card
with a work-item-linked assignment because assignment work-item identity is immutable.

A database write error rolls back the whole completion transaction. Tightbeam reports
the database error through the existing handler path. It does not record a partial
readiness fact.

The word “silent” in this invariant applies to readiness production. It does not hide a
completion refusal from the caller.

### I10. Corrected commits follow ordinary iteration

A `changes-requested` final review verdict leaves the producer open and creates no
readiness notice. The producer holder can create a corrected commit, file its current
test receipt, and obtain a clean verdict on the selected review.

The final completion references only the corrected commit. A test or review row for an
older commit cannot qualify the corrected completion. The successful completion creates
one notice for the corrected commit.

### I11. Migration is forward-only and non-retroactive

The schema migration creates the notice table without backfilling it. Existing closed
assignments receive no readiness notice.

Existing test and clean-review verdicts remain valid for their current consumers. A
note-only row does not qualify this feature. A pre-feature structured row qualifies an
open code completion only when completion-time revalidation proves that it satisfies
I2-I4.

The feature does not become live until the operational-parent schema and resolver are
live. Startup refuses the merge-readiness feature when that dependency is absent or has
an unknown schema stamp.

### I12. One mutation seam owns readiness state

`Tightbeam.Productions.MergeReadiness` is the only module that inserts or updates
`merge_readiness_notices`. `Assignments` calls its in-transaction function from the
code-completion path.

`Assignments` remains the only owner of attest validation and insertion. `Wakes` remains
the only owner of wake insertion and state. `MergeReadiness` calls those in-transaction
seams. It does not duplicate their SQL.

A source-closure test fails if another production path mutates the notice table.

### I13. The notice cannot mutate source

The readiness transaction writes only Tightbeam database rows and the ordinary prompt
projection. It does not invoke Git, a deployment tool, a release tool, or an external
service after commit-reference validation.

The prompt states that the parent must use the separately authorized merge workflow.
The prompt contains no command that tells the substrate to mutate a repository.

### I14. The notice is durable before model execution

The readiness row and prompt wake commit before the effective parent runs a turn. Model
failure, scheduler delay, gateway restart, or parent retirement cannot erase those rows.

Existing wake delivery rules control later wake state. This feature does not infer that
the parent merged, read, or accepted the notice from wake delivery.

### Recon-gap closure map

| Recon gap | Ruling | Home |
| --- | --- | --- |
| 1. Test receipt binding | Extend structured `commitRefs` to holder `tests-passed` and `tests-invalidated`; require one canonical ref. | I2-I3 |
| 2. Completion and clean cardinality | Require one canonical ref on completion, test receipt, and selected clean verdict; compare `{repo, commit}`. | I2, I4 |
| 3. Latest test verdict | Newest holder outcome across `tests-passed` and `tests-invalidated` controls. | I3 |
| 4. Review-card selection | Reuse newest linked review and newest holder verdict. Require independence and exact commit equality. | I4 |
| 5. Producing-card scope | Apply only to `effectKind='code'`. | I1 |
| 6. Effective parent | Use the first active `operationalParent` ancestor and skip retired rows. | I5 |
| 7. Notice carrier | Use one ordinary prompt wake backed by one structured notice row. | I6, I8, I14 |
| 8. One-shot identity | Key both notice and wake from the completion attest id. | I7 |
| 9. Payload meanings | Cause is completion; principal is its holder; origin is `process:tightbeam`. | I8 |
| 10. Atomic boundary and replay | Qualify, close, record, and arm the wake in one transaction; add no sweeper. | I6-I7 |

## Architecture

### 1. Proven source and dependencies

Recon artifact `art_108f9266` established these facts on commit `ac8651dc`:

- Producer test verdicts cannot carry structured commit references
  (`lib/tightbeam/assignments.ex:1544-1605`).
- Completion and linked-review verdicts already accept commit references whose objects
  exist (`lib/tightbeam/assignments.ex:1520-1645`).
- The newest linked review and newest holder verdict already control review qualification
  (`lib/tightbeam/assignments.ex:310-337`).
- Completion closes the assignment in the attest transaction
  (`lib/tightbeam/assignments.ex:1130-1200`).
- Current Main has no operational-parent field or resolver
  (`lib/tightbeam/org.ex:13-90`; `lib/tightbeam/recurrence_suppression.ex:474`).
- `EventLog.notice/5` is durable but lacks caller-controlled dedupe
  (`lib/tightbeam/event_log.ex:282-423`; `lib/tightbeam/projection.ex:166-180`).
- The ordinary wake and turn path has a unique caller-controlled `wakeId`
  (`lib/tightbeam/ledger.ex:1-76`; `lib/tightbeam/gateway.ex:978-1040`).

Implementation depends on the operational-parent work represented by commit
`fa490592`. The dependency must land as separate reviewed work. This feature consumes
its field, root invariant, and cycle refusal. It calls one neutral active-ancestor read
seam in `Org`. If the dependency does not expose that read seam, this feature adds the
read-only seam without adding parent state or parent mutation. The seam walks the full
durable, cycle-free chain. It accepts no elapsed-time, row-count, or hop threshold from
its caller.

### 2. Eligibility query

`MergeReadiness.qualify_in_txn/3` receives the producer assignment, the proposed
completion attest, and its one canonical commit reference. It returns either a complete
qualification value or one I2-I5 and I9 refusal.

The query performs these steps:

1. Require `effectKind='code'` and a non-null `workItemId`.
2. Select the newest holder test outcome from the two I3 kinds.
3. Require `tests-passed`; canonical-revalidate its one reference; require an exact match.
4. Select the newest linked review by `(openedAt, rowid)`.
5. Require a holder different from the producer holder.
6. Select that holder's newest verdict on the review by `(ts, rowid)`.
7. Require `reviewed-clean`; canonical-revalidate its one reference; require an exact match.
8. Resolve the first active operational parent.
9. Return the exact rows and target to the transaction.

Steps 3 and 7 use the host-aware Git seam. Every other step reads typed database rows.
The query does not read a note or use an event-log row as evidence.

### 3. Canonical attest filings

The producer holder uses these forms. Each command substitutes one real repository and
the full lowercase object id of one commit. The review holder, not the producer holder,
files the `reviewed-clean` form.

```text
tightbeam attest <producer> --kind verdict --verdict tests-passed \
  --commit-refs '[{"repo":"<host>:<absolute-path>","commit":"<commit>"}]' \
  --note "<test command or suite>; passed: <result>"

tightbeam attest <producer> --kind verdict --verdict tests-invalidated \
  --commit-refs '[{"repo":"<host>:<absolute-path>","commit":"<commit>"}]' \
  --note "<reason the earlier receipt is no longer current>"

tightbeam attest <review> --kind verdict --verdict reviewed-clean \
  --commit-refs '[{"repo":"<host>:<absolute-path>","commit":"<commit>"}]' \
  --note "<review evidence>"

tightbeam attest <producer> --kind completion \
  --commit-refs '[{"repo":"<host>:<absolute-path>","commit":"<commit>"}]' \
  --note "<completion evidence>"
```

The feature uses the existing `--commit-refs` JSON contract. It adds no alternate
repository or commit syntax.

### 4. Transaction order

The existing code-completion transaction uses this order:

1. Read and authorize the open producer assignment.
2. Validate the one completion reference as a canonical commit through the host-aware seam.
3. Build the proposed completion attest id and timestamp.
4. Run `MergeReadiness.qualify_in_txn/3` against that exact commit.
5. Insert the completion attest.
6. Guarded-update the assignment to `closed/completed` and verify one changed row.
7. Insert the readiness notice through `MergeReadiness.open_in_txn/2`.
8. Schedule its immediate prompt wake through `Wakes.schedule_in_txn/2`.
9. Run the existing work-item, supervision, effort, and marker transitions.
10. Commit.

Steps 4-9 share the existing transaction. A refusal before step 5 changes no row. A
failure after step 5 rolls back all steps.

The non-code completion path skips steps 4, 7, and 8.

### 5. Durable record

The implementation creates this logical shape. It can add equivalent database checks.
It cannot weaken a listed relation.

```sql
CREATE TABLE merge_readiness_notices (
  id                       TEXT PRIMARY KEY,
  dedupeKey                TEXT NOT NULL UNIQUE,
  producerAssignmentId     TEXT NOT NULL UNIQUE REFERENCES assignments(id),
  workItemId               TEXT NOT NULL REFERENCES work_items(id),
  completionAttestId       TEXT NOT NULL UNIQUE REFERENCES attests(id),
  repo                     TEXT NOT NULL,
  commitId                 TEXT NOT NULL,
  testVerdictAttestId      TEXT NOT NULL REFERENCES attests(id),
  reviewAssignmentId       TEXT NOT NULL REFERENCES assignments(id),
  reviewVerdictAttestId    TEXT NOT NULL REFERENCES attests(id),
  causeAttestId            TEXT NOT NULL REFERENCES attests(id),
  principalKind            TEXT NOT NULL CHECK (principalKind = 'session'),
  principalId              TEXT NOT NULL REFERENCES sessions(sessionKey),
  recipientSessionKey      TEXT NOT NULL REFERENCES sessions(sessionKey),
  wakeId                   TEXT NOT NULL UNIQUE REFERENCES wakes(wakeId)
                             DEFERRABLE INITIALLY DEFERRED,
  createdAt                INTEGER NOT NULL,
  CHECK (dedupeKey = 'merge-readiness:' || completionAttestId),
  CHECK (causeAttestId = completionAttestId),
  CHECK (wakeId = 'merge-readiness-notice:' || completionAttestId)
);
```

The module stores the exact `tests-passed` and `reviewed-clean` attest ids. The referenced
rows carry their verdict kinds, authors, and commit references. The table does not copy
those mutable-free facts.

### 6. Wake and prompt

The transaction schedules one immediate prompt wake with these values:

- `wakeId = 'merge-readiness-notice:' || completionAttestId`
- `sessionKey = recipientSessionKey`
- `origin = 'process:tightbeam'`
- `consumer = 'prompt'`
- `assignmentId = producerAssignmentId`
- `work_item_id = workItemId`
- `dueAt = createdAt`

The stored prompt uses this exact field order:

```text
[merge ready]
producer=<producerAssignmentId> work-item=<workItemId>
repo=<repo> commit=<commitId>
cause=<completionAttestId> principal=session:<principalId>
tests-passed=<testVerdictAttestId>
review=<reviewAssignmentId> reviewed-clean=<reviewVerdictAttestId>
This exact work is ready for its authorized merge-to-main step. This notice did not merge, push, deploy, or release it.
```

Generated values replace only the angle-bracket fields. Prompt prose is presentation.
No consumer parses it.

### 7. Read projection

`work-item-trace` adds one `merge_readiness_notice` entry from the structured row. The
entry exposes every I8 field and the current ordinary wake state. Authorization follows
the existing work-item trace rules.

The projection does not infer a merge state. The row means only that the exact approval
handoff committed.

### 8. Migration

The release uses this order:

1. Merge and verify the operational-parent dependency.
2. Create `merge_readiness_notices` through the canonical schema registry.
3. Enforce canonical commit references on code completion, producer-holder test outcomes,
   and review-holder clean verdicts linked to code.
4. Register the code-completion transaction hook.
5. Add the trace projection.
6. Update coder guidance with the typed `tests-passed` command.
7. Update review guidance to require one canonical commit reference on code
   `reviewed-clean`.
8. Activate the feature after the schema stamp succeeds.

The migration inserts no notice rows and schedules no wakes. A failed schema step leaves
the old version active.

### 9. Affected seams

- `lib/tightbeam/assignments.ex`: allow typed producer test outcomes and invoke the
  readiness transaction for code completion.
- `lib/tightbeam/productions/merge_readiness.ex`: own eligibility and notice mutation.
- `lib/tightbeam/schema.ex`: register the notice table after its dependencies.
- `lib/tightbeam/org.ex`: expose the neutral in-transaction read that returns the first
  active operational ancestor, if the dependency does not already expose it.
- `lib/tightbeam/wakes.ex`: reuse the in-transaction wake insertion seam.
- `lib/tightbeam/job_trace.ex`: project the structured notice.
- `priv/kungfu/agentic-engineering/guidance/coder.md`: replace the note-only example
  with the typed commit-reference form and teach `tests-invalidated`.
- `priv/kungfu/agentic-engineering/guidance/reviewer.md`: require one matching canonical
  commit reference on code `reviewed-clean`.
- `test/merge_readiness_test.exs`: own the acceptance matrix and source-closure check.
- Existing assignment, rules, job-trace, CLI integration, schema-shape, and guidance
  tests: update only assertions changed by I2-I4 and I11.

No new public CLI verb is required. The existing `attest`, `attests`, and
`work-item-trace` verbs provide the write and read surfaces.

### 10. Requirement traceability

| Requirement | Acceptance | Implementation surface |
| --- | --- | --- |
| I1 | A2 | assignment effect query |
| I2 | A1, A3, A7 | commit validation and qualification |
| I3 | A4-A5 | attest validation and test selection |
| I4 | A6-A8 | linked-review selection |
| I5 | A9-A10 | operational-parent resolver |
| I6 | A1, A11 | completion transaction |
| I7 | A12-A13, A15 | notice constraints, replay equality, and wake id |
| I8 | A14 | notice row, prompt, trace |
| I9 | A3-A10, A17 | typed refusals |
| I10 | A8, A15 | ordinary review iteration |
| I11 | A16 | schema migration |
| I12 | A18 | source-closure test |
| I13 | A19 | side-effect boundary |
| I14 | A13, A20 | durable wake and real smoke |

## Acceptance

Each case uses the real SQLite database and the real assignment and wake handlers. Tests
must create Git commits through a real repository fixture. A hand-written commit response
does not satisfy commit verification.

### A1. Exact happy path

Given code producer `P` links to work item `W`, holder `H` files `tests-passed` with one
canonical reference `{R,C}`, independent review `V` has final holder `reviewed-clean`
with the same reference, and `H` files completion with the same reference, when the
transaction commits, then exactly one completion, one readiness row, and one prompt wake
exist. The readiness row and wake contain the exact I8 and Architecture 6 values.

### A2. Non-code completion stays unchanged

Given an assignment has `effectKind='policy'` and satisfies its existing completion
rules, when its holder completes it, then the existing close commits. No merge-readiness
row or wake exists.

### A3. Canonical filing refusal

Given a code completion, holder test outcome, or code-review clean verdict has zero commit
references or two commit references, when its holder files it, then the handler returns
`merge_readiness_exact_commit_required`. It inserts no attest, readiness row, or wake.

Given a branch, tag, abbreviated object id, uppercase object id, tree, blob, or missing
object is the filed `commit` on a holder test outcome, code-review clean verdict, or code
completion, then filing returns `unverifiable_commit_ref`. It inserts no attest,
readiness row, or wake.

Given a pre-feature structured test or review row has invalid cardinality or a
noncanonical commit, when the producer holder files completion, then the handler returns
I3's or I4's completion-time error. The assignment stays open. No completion attest,
readiness row, or wake exists.

### A4. Only the holder's typed test outcome controls

Given another session and a user have note-only `tests-passed` rows on producer `P`, when
`P`'s holder tries to complete, then those rows do not qualify. The handler returns
`merge_readiness_tests_not_current`, keeps `P` open, and creates no readiness state.

### A5. Latest test outcome controls

Given `H` files `tests-passed` for commit `C1` and later files `tests-invalidated` for
`C1`, when `H` tries to complete `C1`, then the handler refuses with
`merge_readiness_tests_not_current`.

Given `H` then files `tests-passed` for corrected commit `C2`, when the matching review
is clean and `H` completes `C2`, then one notice names `C2`. No notice names `C1`.

### A6. Newest review card controls

Given an older linked review has holder-filed `reviewed-clean` for `C` and a newer linked
review has no verdict, when `H` tries to complete `C`, then the existing review gate
refuses completion. No readiness row or wake exists.

Given the newer review holder files matching `reviewed-clean`, when `H` retries, then the
notice names the newer review and its clean verdict.

### A7. Review commit mismatch refuses

Given the completion and test receipt name `{R,C2}` while the selected clean verdict
names `{R,C1}`, when `H` files completion, then the handler returns
`merge_readiness_review_commit_mismatch`. The assignment stays open. No readiness state
exists.

The same result occurs when repository strings differ while commit strings match.

### A8. Changes requested stays silent

Given the selected review holder files `reviewed-clean` for `C1` and later files
`changes-requested`, when `H` tries to complete `C1`, then the existing review gate
refuses completion. No readiness row or wake exists.

Given the holder produces `C2`, files current tests, and receives final matching
`reviewed-clean`, when the holder completes `C2`, then one notice names `C2`.

### A9. Retired parent is skipped

Given `H.operationalParent=P1`, `P1` is retired, and `P1.operationalParent=P2` where `P2`
is active, when `H` completes qualifying work, then the readiness row and wake target
`P2`. They do not target `P1` or read `spawnedBy`.

### A10. Long and corrupt parent chains are deterministic

Given a fault-injected database has a missing parent row, a cycle, or an inactive Main,
when `H` files qualifying completion, then the handler returns
`merge_readiness_parent_unavailable`. The completion and readiness transaction rolls back.

Given the operational-parent chain contains 33 consecutive retired sessions followed by
active session `P`, when `H` files qualifying completion, then completion succeeds. The
readiness row and wake target `P`.

### A11. Notice write failure rolls back completion

Given a temporary database trigger aborts the readiness-row insert, when `H` files a
qualifying completion, then the completion attest, assignment close, notice row, wake,
and existing close transitions are absent. After the trigger is removed, one retry
commits one complete set.

### A12. Concurrent completion dedupes

Given two concurrent qualifying completion calls for one open producer, when both run,
then one succeeds and one returns the existing terminal-race response. One completion
attest, one readiness row, and one wake exist.

### A13. Restart preserves one handoff

Given a qualifying completion commits while the prompt scheduler is stopped, when the
gateway restarts, then the same pending wake remains linked to the same readiness row.
Delivery creates at most one turn because the wake id is stable. Restart creates no
second readiness row or wake.

### A14. Payload carries exact evidence

Given A1 commits, when the parent reads the stored prompt and `work-item-trace`, then both
name the producer, work item, repository, commit, cause, cause principal, test verdict,
review, clean verdict, recipient, and wake from the same readiness row. The prompt sender
and wake origin are `process:tightbeam`.

### A15. Replay is exact or refused

Given A1 committed, when `MergeReadiness.open_in_txn/2` receives the same completion id
and the same identity, cause, principal, producer, work item, commit, evidence, recipient,
and wake id again, then it returns the original readiness row. A different proposed notice
id or creation time does not change this result. The original id, `createdAt`, row, and
wake remain unchanged.

Given the same completion id is replayed with a different `reviewVerdictAttestId` or any
other compared field from I7, when the readiness seam runs, then it returns
`merge_readiness_replay_conflict` and names each unequal field. The existing row remains
unchanged. No second readiness row, wake, message, or turn exists. A later linked review
introduced through a fault fixture produces this same refusal.

### A16. Migration is silent

Given the pre-feature database contains closed code assignments with note-only test
receipts and clean reviews, when the schema migration runs, then it creates the empty
notice table. It creates no wake, message, turn, or trace entry for those assignments.

### A17. Missing work item refuses with a repair path

Given a code producer has no work item, when its holder files otherwise qualifying
completion, then the handler returns `merge_readiness_work_item_required`. The response
tells the caller to replace the card with a work-item-linked assignment. No completion
or readiness state commits.

### A18. One mutation seam

Given the source-closure test scans production SQL, when the implementation gate runs,
then only `Tightbeam.Productions.MergeReadiness` mutates
`merge_readiness_notices`. The same test proves that the module calls `Wakes` instead of
mutating wake state directly.

### A19. Approval-only boundary

Given A1 commits in a repository whose main branch does not point at `C`, when the
readiness transaction and wake delivery finish, then each preexisting Git ref, remote
configuration value, and worktree file remains unchanged. Deployment and release state
also remain unchanged. Only Tightbeam database and prompt projection rows change.

### A20. Real gateway smoke

Given one real gateway has a producer session, an independent reviewer session, an
active operational parent, and one real commit in a temporary repository, when the
sessions file the typed test receipt, matching clean review, and completion through the
real CLI, then capture these real outputs as the implementation fixture:

1. The three attests and their canonical commit references.
2. The readiness row.
3. The pending or delivered wake.
4. The parent prompt or delivered turn.
5. The `work-item-trace` entry.
6. The unchanged Git refs and deployment state.

Given that captured state, when the test invokes the readiness seam again and restarts
the gateway, then the captured row ids and wake id remain unchanged. No duplicate prompt
or turn appears.

Passing unit tests without this smoke does not satisfy the feature.

## Open Questions

None. I1-I14 close the ten load-bearing recon gaps.

An independent reviewer can reject a ruling or expose a new hole. A material ruling
change must amend this canonical file before the orchestrator binds or implements it.
