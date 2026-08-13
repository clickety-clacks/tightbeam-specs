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

The same reviewed implementation that first ships this mechanism also teaches the
pattern in `priv/guidance/operating-manual.md`. The implementation owns that manual
edit. This spec revision does not publish the directive before the mechanism exists.

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
one readiness-qualified ordinary wake. It does not add a sweeper because the final
qualifying event is the completion transaction itself.

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
- **Forbidden repository character**: one code point in U+0000..U+001F, U+007F,
  U+0085, U+2028, or U+2029. Tightbeam checks the decoded `host` and absolute `path`
  components before it invokes Git or builds a prompt.
- **Exact commit**: the ordered pair `{repo, commit}` from one canonical commit reference.
  Equality requires byte-for-byte equality of both stored values after canonical
  validation.
- **Completion Git preflight**: the three host-Git checks for the proposed completion,
  selected test receipt, and selected clean verdict run before the mutation transaction.
  Each command has its own hard monotonic deadline of 5,000 milliseconds.
- **Filing Git check**: the host-Git check for one producer-holder
  `tests-passed` or `tests-invalidated` verdict, or one review-holder
  `reviewed-clean` verdict. It runs before the attest transaction and has its own hard
  monotonic deadline of 5,000 milliseconds.
- **Preflight evidence snapshot**: the proposed completion attest id and the exact row
  ids, repository values, and commit values for the proposed completion, selected test
  receipt, and selected clean verdict that passed the completion Git preflight.
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
- **Effective parent**: the first active session remembered on the producer holder's
  `operationalParent` chain. Resolution begins at the holder's `operationalParent`.
  The resolver skips retired targets and validates the remaining tail through exactly
  one active Main self-root before it returns the remembered session.
- **Readiness cause**: the producer's completion attest. Existing rails require the test
  and clean-review rows before completion, so completion is the final qualifying event.
- **Cause principal**: the producer holder that filed the readiness cause. The stored
  typed form is `{kind='session', id=<producer-holder-session-key>}`.
- **Readiness notice**: one `merge_readiness_notices` row and its linked prompt wake.
  The row is the structured truth. The prompt is its agent-facing projection.
- **Readiness-qualified wake**: the prompt wake whose id, origin, assignment, work item,
  and readiness identity match the completion under I7 and Architecture 6. An ordinary
  slate wake is not a readiness-qualified wake.
- **Readiness identity**: `merge-readiness:<completion-attest-id>`. This value is the
  notice dedupe key and the basis for the deterministic wake id.
- **Approval handoff**: the atomic commit of a readiness notice addressed to the
  effective parent. It is not proof that the parent ran a turn. It is not permission for
  the substrate to mutate a repository.
- **Additive activation identity**: `merge_readiness_v1`. This identity owns the exact
  schema objects and activation row in I11. It does not replace the global
  `model-identity-v1` schema stamp.
- **Activation epoch**: the one row in `merge_readiness_epoch`. Its exact values are
  `id=0`, a nonnegative integer `activatedAt`, `cause='schema_activation'`, and
  `principal='process:tightbeam'`.

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

For a typed test or clean-review verdict filing, `Assignments` first rejects a
forbidden repository character under I9. Before it opens the attest transaction, it
uses the existing host-aware repository seam to run
`git rev-parse --verify <filed-commit>^{commit}`. Canonical validation requires the
returned full lowercase object id to byte-equal the filed `commit`. Each filing Git
check has its own hard monotonic deadline of 5,000 milliseconds. At the deadline,
Tightbeam terminates the verifier and rejects a late success. The filing seam rejects a
completed semantic negative with `unverifiable_commit_ref` and inserts no attest. I9
owns its unavailable taxonomy and remedy.

Before it opens the mutation transaction, `MergeReadiness` constructs the proposed
completion evidence, selects the authoritative test receipt and final review verdict,
and validates their three references through the same host-aware seam. Each command has
its own hard monotonic deadline of 5,000 milliseconds. At a command's deadline,
Tightbeam terminates that verifier and rejects a late success.

A successful preflight returns one evidence snapshot. The completion transaction
reconstructs the proposed completion evidence and reselects the authoritative test and
review rows before its first write. It requires the same row ids, repository values,
and commit values that passed preflight. A difference returns
`stale_merge_readiness_evidence` and changes no row. The transaction invokes no external
Git command.

Completion Git preflight prevents a structured row filed before feature activation
from bypassing canonical or repository-character validation. A test row that fails
cardinality or canonical revalidation follows I3. A review row that fails either check
follows I4. I9 owns timeout, unavailable-host, and forbidden-character refusals.

After the transactional reselect, the readiness handler compares stored values byte for
byte.

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

For an open pre-feature producer whose holder filed note-only `tests-passed`, the same
`merge_readiness_tests_not_current` refusal and remedy apply. The holder files one
current typed `tests-passed` verdict for the exact completion commit. Tightbeam does
not update or replace the note-only row.

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

When the selected review is closed and its final holder-filed `reviewed-clean` verdict
is note-only, its row cannot accept a typed repair. After the producer holder files the
I3 typed test repair, the response tells the caller to open exactly one new independent
successor review linked to the same open producer. That successor becomes the selected
newest review. Its holder files typed `reviewed-clean` for the exact completion commit.
The older closed review and its note-only verdict remain immutable non-controlling
history.

### I5. Effective-parent resolution uses operational authority

The completion transaction starts at the producer holder's `operationalParent`. It
follows each durable `operationalParent` link through exactly one active Main self-root.
The resolver remembers the first active session as the readiness target. It keeps
validating the remaining tail after it remembers that target. A later active ancestor
does not replace the remembered target. Retired sessions do not become the target.

The resolver has no elapsed-time, row-count, or hop threshold. It does not read
`spawnedBy`, roles, session names, prompts, or work-item causal edges.

A missing row, cycle, inactive Main, or Main row whose `operationalParent` does not
self-reference is corrupt state. The handler refuses completion with
`merge_readiness_parent_unavailable`. The response names this remedy: restore or
reparent the complete operational chain, then retry.

The completion transaction stores the remembered target only after the full tail passes.
A later reparent or retirement does not rewrite the historical notice target.

### I6. Evidence pin and handoff form one transaction

The completion Git preflight runs before the mutation transaction and writes no row.
After preflight succeeds, the handler opens one database transaction. Before its first
write, the transaction checks I1-I5 against the reselected evidence and requires the
exact preflight snapshot under I2. It then performs these required steps:

1. The completion attest.
2. The guarded assignment close.
3. The readiness notice row.
4. The one readiness-qualified prompt wake for the effective parent.
5. `WorkItems.arm_slate_in_txn`, including its conditional state update and optional
   separate slate prompt wake.
6. The disposition-liveness derivation.
7. The supervision transition.
8. The effort-check cancellation or transition.

The transaction commits the required results or none. No post-commit callback creates
the readiness notice. An observer cannot read a completion without its required
readiness row and readiness-qualified wake.

After the required transitions, the handler invokes `append_attest_marker` and
`append_assignment_marker` as two distinct existing best-effort projections. A failure
in either projection remains non-fatal. The handler does not claim that projection
failure rolls back the required rows.

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
one readiness-qualified wake. A later review round cannot create another notice for the
closed producer. An ordinary slate wake can coexist without matching the readiness
identity.

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
11. The readiness-qualified prompt wake.
12. The creation time.

The wake origin and message sender are `process:tightbeam`. The cause principal remains
the holder session. The system does not derive either value from prose. The prompt emits
the repository value raw only after the filing or completion check rejects each
forbidden repository character.

### I9. Silence and named refusal

Before I1-I5 pass, Tightbeam writes no merge-readiness notice, wake, prompt, or lifecycle
event. A completion refusal returns one typed error and its remedy to the caller.

The rail refuses a code completion when the producer lacks a work item. It uses
`merge_readiness_work_item_required`. The response tells the caller to replace the card
with a work-item-linked assignment because assignment work-item identity is immutable.

A filing or completion Git preflight rejects a forbidden repository character with
`merge_readiness_repo_control_character` before it invokes Git or builds a prompt.
It accepts another valid UTF-8 repository host or path.

When one completion preflight or filing Git command reaches its
5,000-millisecond monotonic deadline, the handler terminates the verifier and returns
`merge_readiness_commit_verification_unavailable` with `reasonKind='timeout'`. It
rejects late success from that verifier.

An unregistered or unknown host returns the same refusal with
`reasonKind='unknown_host'`. A command-start failure, SSH-connect failure, or runner
infrastructure failure returns it with `reasonKind='runner_unavailable'`. A completed
reachable-host check that reports a missing repository, missing object, non-commit
object, or other semantic negative returns `unverifiable_commit_ref`.

Each completion preflight refusal names the phase as `completion`, `test`, or
`review`. Each filing refusal names `test` for `tests-passed` and
`tests-invalidated`, or `review` for `reviewed-clean`. The refusal names the host,
repository, 5,000-millisecond deadline, and phase-specific retry remedy. A completion
preflight writes no database row. A filing refusal inserts no attest.

After preflight, a row-id, repository, or commit mismatch in the transactional reselect
returns `stale_merge_readiness_evidence`. The response names each changed evidence
field and tells the holder to retry completion against the current evidence. The
transaction writes no row.

The `completion` remedy tells the holder to repair the named verification condition
and retry with one canonical completion reference. The `test` remedy tells the holder
to repair the condition, file a current holder `tests-passed` receipt for the exact
completion commit, and retry. The `review` remedy tells the holder to repair the
condition, obtain holder-filed `reviewed-clean` for the exact completion commit, and
retry.

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

The global schema stamp remains `model-identity-v1`. The merge-readiness feature uses
the additive activation identity `merge_readiness_v1`.

The feature owns exactly these SQLite schema objects:

1. Tables `merge_readiness_notices` and `merge_readiness_epoch`.
2. Unique indexes `merge_readiness_dedupe_key`,
   `merge_readiness_producer_assignment`, `merge_readiness_completion_attest`, and
   `merge_readiness_wake_id`.
3. No triggers.

SQLite-created autoindexes are engine-owned objects. They are not feature-owned objects.
Any table, index, or trigger whose name starts with `merge_readiness_` is feature-owned
and must appear in the preceding list.

Startup validates the operational-parent dependency before it inspects or creates a
`merge_readiness_v1` object. A missing or incompatible dependency raises its existing
shape error and changes no merge-readiness state.

When zero feature-owned objects exist, one database transaction creates and validates
the six listed objects in their Architecture 5 order. The transaction then inserts and
validates exactly one activation epoch. The feature becomes live only after this
transaction commits.

When all six objects and the one activation epoch have the exact required shape, startup
returns success without changing an object or the epoch. This state is the only
idempotent replay state.

A nonempty proper subset, malformed object, duplicate object, extra feature-owned object,
or missing, extra, or malformed activation row raises `Tightbeam.Schema.ShapeError` with
`incompatible_merge_readiness_v1`. Startup preserves the observed state byte for byte.
It does not infer, complete, replace, or repair the activation.

A failure after one listed creation statement or the activation-row insert rolls back
the transaction to zero feature-owned objects and zero activation rows.

The activation creates no readiness notice and performs no backfill. Existing closed
assignments receive no readiness notice.

Existing test and clean-review verdicts remain valid for their current consumers. A
note-only row does not qualify this feature. A pre-feature structured row qualifies an
open code completion only when the completion Git preflight and transactional evidence
reselect prove that it satisfies I2-I4.

An open pre-feature producer receives no historical backfill. Its holder can file the
typed test repair from I3. If its selected note-only clean review is closed, the caller
opens exactly one independent successor under I4. The new typed rows control future
qualification. The feature does not reopen or mutate an older attest or review.

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

The readiness row and readiness-qualified prompt wake commit before the effective parent
runs a turn. Model failure, scheduler delay, gateway restart, or parent retirement cannot
erase those rows.

Existing wake delivery rules control later wake state. This feature does not infer that
the parent merged, read, or accepted the notice from wake delivery.

### I15. The operating pattern ships with the mechanism

The same reviewed implementation that first ships the merge-readiness mechanism amends
`priv/guidance/operating-manual.md`. The directive defines the holder's typed
`tests-passed` receipt. It defines the exact independent `reviewed-clean` evidence. It
defines the readiness notice as an approval handoff rather than permission to merge.

The implementation lands the manual directive with the mechanism. It does not publish
the directive in an earlier documentation-only change. Coder and reviewer guidance keep
the role-specific commands and mechanics. The operating manual does not duplicate those
instructions.

### Recon-gap closure map

| Recon gap | Ruling | Home |
| --- | --- | --- |
| 1. Test receipt binding | Extend structured `commitRefs` to holder `tests-passed` and `tests-invalidated`; require one canonical ref. | I2-I3 |
| 2. Completion and clean cardinality | Require one canonical ref on completion, test receipt, and selected clean verdict; compare `{repo, commit}`. | I2, I4 |
| 3. Latest test verdict | Newest holder outcome across `tests-passed` and `tests-invalidated` controls. | I3 |
| 4. Review-card selection | Reuse newest linked review and newest holder verdict. Require independence and exact commit equality. | I4 |
| 5. Producing-card scope | Apply only to `effectKind='code'`. | I1 |
| 6. Effective parent | Remember the first active `operationalParent` ancestor, then validate its full tail through Main. | I5 |
| 7. Notice carrier | Use one readiness-qualified prompt wake backed by one structured notice row. | I6, I8, I14 |
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
durable chain. It returns the first active target only after it validates the tail
through one active Main self-root. It accepts no elapsed-time, row-count, or hop
threshold from its caller.

### 2. Eligibility query

Before the mutation transaction, the completion handler constructs the proposed
completion attest, including its id and timestamp. `MergeReadiness.preflight/2` receives
that evidence and performs these steps:

1. Read and authorize the open producer assignment. Require `effectKind='code'` and a
   non-null `workItemId`.
2. Reject a forbidden repository character in the proposed completion reference. Run
   its canonical host-Git check with a hard monotonic deadline of 5,000 milliseconds.
3. Select the newest holder test outcome from the two I3 kinds.
4. Require `tests-passed`; reject its forbidden repository characters; run its canonical
   host-Git check with its own 5,000-millisecond deadline; require an exact match.
5. Select the newest linked review by `(openedAt, rowid)`.
6. Require a holder different from the producer holder.
7. Select that holder's newest verdict on the review by `(ts, rowid)` descending.
8. Require `reviewed-clean`; reject its forbidden repository characters; run its
   canonical host-Git check with its own 5,000-millisecond deadline; require an exact
   match.
9. Return the proposed completion attest and one preflight evidence snapshot.

After preflight succeeds, `MergeReadiness.qualify_in_txn/3` receives the producer
assignment, proposed completion attest, and snapshot. It performs these steps before the
first write:

1. Read and authorize the open producer assignment again.
2. Reconstruct the proposed completion evidence and reselect the newest holder test,
   newest linked review, and that review holder's newest verdict.
3. Require the same completion, test, and review row ids, repository values, and commit
   values that the snapshot records.
4. Refuse a mismatch with `stale_merge_readiness_evidence`.
5. Recheck the typed I1-I4 predicates against those exact rows.
6. Remember the first active operational parent and validate the full tail through Main.
7. Return the exact rows and target to the transaction.

Only preflight uses the host-aware Git seam. Each Git command owns one hard deadline.
The mutation transaction reads typed database rows and invokes no external Git command.
Neither query reads a note or uses an event-log row as evidence.

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
repository or commit syntax. After JSON decoding, `Assignments` rejects a forbidden
repository character in the host or path before it invokes Git.

For each typed test or clean-review verdict, `Assignments` runs the filing Git check
before it opens the attest transaction. The command has one hard monotonic
5,000-millisecond deadline. It uses the I9 unavailable taxonomy and inserts no attest on
refusal. A completed semantic negative uses `unverifiable_commit_ref`.

### 4. Transaction order

The code-completion handler constructs the proposed completion attest and runs the
Architecture 2 preflight before it opens the mutation transaction. Preflight selects the
exact test and review evidence, runs the three host-Git commands with separate
5,000-millisecond deadlines, and returns the evidence snapshot. It writes no row.

After successful preflight, the handler uses this transaction order:

1. Begin the serialized transaction.
2. Read and authorize the open producer assignment.
3. Run `MergeReadiness.qualify_in_txn/3` against the proposed completion and exact
   preflight snapshot. Reselect and match the three evidence rows before any write. Run
   no external Git command.
4. Insert the completion attest.
5. Guarded-update the assignment to `closed/completed` and verify one changed row.
6. Insert the readiness notice through `MergeReadiness.open_in_txn/2`.
7. Schedule its readiness-qualified prompt wake through `Wakes.schedule_in_txn/2`.
8. Run `WorkItems.arm_slate_in_txn`; when the existing slate condition holds, it updates
   slate state and can schedule one separate ordinary slate prompt wake.
9. Derive the disposition-liveness trigger.
10. Run the terminal supervision transition.
11. Run the effort-check cancellation or transition.
12. Invoke `append_attest_marker` as an existing best-effort projection.
13. Invoke `append_assignment_marker` as an existing best-effort projection.
14. Commit.

Steps 4-11 are the required atomic tail. A refusal before step 4 changes no row. An
error in a required tail seam rolls back each required row. Steps 12 and 13 remain
distinct and non-fatal; an error in either does not roll back the required tail.

The non-code completion path keeps its existing lifecycle order. It creates no
merge-readiness row or readiness-qualified wake.

### 5. Durable record

The implementation creates this exact feature-owned shape. It cannot add, remove,
rename, or weaken a listed feature-owned object.

```sql
CREATE TABLE merge_readiness_notices (
  id                       TEXT PRIMARY KEY,
  dedupeKey                TEXT NOT NULL,
  producerAssignmentId     TEXT NOT NULL REFERENCES assignments(id),
  workItemId               TEXT NOT NULL REFERENCES work_items(id),
  completionAttestId       TEXT NOT NULL REFERENCES attests(id),
  repo                     TEXT NOT NULL,
  commitId                 TEXT NOT NULL,
  testVerdictAttestId      TEXT NOT NULL REFERENCES attests(id),
  reviewAssignmentId       TEXT NOT NULL REFERENCES assignments(id),
  reviewVerdictAttestId    TEXT NOT NULL REFERENCES attests(id),
  causeAttestId            TEXT NOT NULL REFERENCES attests(id),
  principalKind            TEXT NOT NULL CHECK (principalKind = 'session'),
  principalId              TEXT NOT NULL REFERENCES sessions(sessionKey),
  recipientSessionKey      TEXT NOT NULL REFERENCES sessions(sessionKey),
  wakeId                   TEXT NOT NULL REFERENCES wakes(wakeId)
                             DEFERRABLE INITIALLY DEFERRED,
  createdAt                INTEGER NOT NULL,
  CHECK (dedupeKey = 'merge-readiness:' || completionAttestId),
  CHECK (causeAttestId = completionAttestId),
  CHECK (wakeId = 'merge-readiness-notice:' || completionAttestId)
);

CREATE TABLE merge_readiness_epoch (
  id          INTEGER PRIMARY KEY CHECK (id = 0),
  activatedAt INTEGER NOT NULL CHECK (activatedAt >= 0),
  cause       TEXT NOT NULL CHECK (cause = 'schema_activation'),
  principal   TEXT NOT NULL CHECK (principal = 'process:tightbeam')
);

CREATE UNIQUE INDEX merge_readiness_dedupe_key
  ON merge_readiness_notices(dedupeKey);
CREATE UNIQUE INDEX merge_readiness_producer_assignment
  ON merge_readiness_notices(producerAssignmentId);
CREATE UNIQUE INDEX merge_readiness_completion_attest
  ON merge_readiness_notices(completionAttestId);
CREATE UNIQUE INDEX merge_readiness_wake_id
  ON merge_readiness_notices(wakeId);
```

Architecture 5 lists the creation order for the six feature-owned objects. The activation
transaction inserts the epoch row only after it validates the last index. The feature
owns no trigger.

The module stores the exact `tests-passed` and `reviewed-clean` attest ids. The referenced
rows carry their verdict kinds, authors, and commit references. The table does not copy
those mutable-free facts.

### 6. Wake and prompt

The transaction schedules one immediate readiness-qualified prompt wake with these
values:

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
entry exposes every I8 field and the current state of the linked readiness-qualified
wake. Authorization follows the existing work-item trace rules.

The projection does not infer a merge state. The row means only that the exact approval
handoff committed.

### 8. Migration

The release uses this order:

1. Validate the operational-parent dependency and its active-ancestor resolver.
2. Verify the global stamp is exactly `model-identity-v1`.
3. Inspect the complete `merge_readiness_v1` owned-object namespace and activation row.
4. If zero owned objects exist, create and validate the six Architecture 5 objects, then
   insert and validate the one activation epoch in the same database transaction.
5. If the exact complete activation exists, leave it unchanged.
6. Refuse any other activation state with `Tightbeam.Schema.ShapeError` and
   `incompatible_merge_readiness_v1`.
7. Enforce canonical commit references on code completion, producer-holder test outcomes,
   and review-holder clean verdicts linked to code. Apply the I9 bounded filing Git
   contract to the typed verdict filings.
8. Register the code-completion transaction hook.
9. Add the trace projection.
10. Update coder guidance with the typed `tests-passed` command.
11. Update review guidance to require one canonical commit reference on code
   `reviewed-clean`.
12. Add the I15 directive to `priv/guidance/operating-manual.md` in the same reviewed
    implementation that ships the mechanism.
13. Expose the feature only after the activation transaction commits.

The activation inserts no notice row and schedules no wake. It creates no message or turn.
A failed activation leaves the feature inactive.

### 9. Affected seams

- `lib/tightbeam/assignments.ex`: allow typed producer test outcomes, reject forbidden
  repository characters, bound typed test and review filing Git checks before their
  attest transactions, run completion Git preflight before the mutation transaction,
  pin the exact preflight evidence in that transaction, and invoke the exact readiness
  transaction tail.
- `lib/tightbeam/productions/merge_readiness.ex`: own preflight, transactional evidence
  reselect, eligibility, and notice mutation.
- `lib/tightbeam/schema.ex`: own the exact `merge_readiness_v1` additive activation after
  its operational-parent dependency.
- `lib/tightbeam/org.ex`: expose the neutral in-transaction read that remembers the
  first active operational ancestor and returns it only after full-tail validation, if
  the dependency does not already expose that read.
- `lib/tightbeam/work_items.ex`: preserve the existing `arm_slate_in_txn` state update
  and optional slate wake after the readiness-qualified wake.
- `lib/tightbeam/wakes.ex`: reuse the in-transaction wake insertion seam for the
  readiness-qualified wake and preserve the distinct slate-wake identity.
- `lib/tightbeam/job_trace.ex`: project the structured notice.
- `priv/kungfu/agentic-engineering/guidance/coder.md`: replace the note-only example
  with the typed commit-reference form and teach `tests-invalidated`.
- `priv/kungfu/agentic-engineering/guidance/reviewer.md`: require one matching canonical
  commit reference on code `reviewed-clean`.
- `priv/guidance/operating-manual.md`: implementation custody adds the concise I15
  pattern directive in the same reviewed change as the mechanism; this spec revision
  does not edit the manual.
- `test/merge_readiness_test.exs`: own the acceptance matrix and source-closure check.
- Existing assignment, rules, job-trace, CLI integration, schema-shape, and guidance
  tests: update only assertions changed by I2-I6, I9, I11, and I15.

No new public CLI verb is required. The existing `attest`, `attests`, and
`work-item-trace` verbs provide the write and read surfaces.

### 10. Requirement traceability

| Requirement | Acceptance | Implementation surface |
| --- | --- | --- |
| I1 | A2 | assignment effect query |
| I2 | A1, A3, A5, A7 | commit validation and qualification |
| I3 | A4-A5, A16 | attest validation and test selection |
| I4 | A6-A8, A16 | linked-review selection |
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
| I15 | A21 | operating-manual directive |

## Acceptance

Each case uses the real SQLite database and the real assignment and wake handlers. Tests
must create Git commits through a real repository fixture. A hand-written commit response
does not satisfy commit verification.

### A1. Exact happy path

Given code producer `P` links to work item `W`, holder `H` files `tests-passed` with one
canonical reference `{R,C}`, independent review `V` has final holder `reviewed-clean`
with the same reference, and `H` files completion with the same reference, when the
transaction commits, then exactly one completion, one readiness row, and one
readiness-qualified prompt wake exist. The readiness row and readiness-qualified wake
contain the exact I8 and Architecture 6 values. An ordinary slate wake can also exist
under the existing work-item rule.

### A2. Non-code completion stays unchanged

Given an assignment has `effectKind='policy'` and satisfies its existing completion
rules, when its holder completes it, then the existing close commits. No merge-readiness
row or readiness-qualified wake exists.

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

Given each of NUL, tab, CR, LF, DEL, NEL, line separator, and paragraph separator appears
in a separate run in the decoded repository host or path on a code completion, holder
test outcome, or code-review clean verdict, when the holder files it, then the handler
returns `merge_readiness_repo_control_character`. It invokes no Git command. It inserts
no attest, readiness row, or wake.

Given a filing Git check for `tests-passed`, `tests-invalidated`, or
`reviewed-clean` has not returned at its own 5,000-millisecond monotonic deadline in
separate runs, when the deadline expires, then Tightbeam terminates the verifier and
rejects a later success. The handler returns
`merge_readiness_commit_verification_unavailable` with `reasonKind='timeout'`, phase
`test` or `review`, host, repository, deadline, and phase-specific remedy. It inserts
no attest.

Given an unknown host occurs in each filing kind in separate runs, when the filing Git
check runs, then the same refusal has `reasonKind='unknown_host'` and the same required
fields. Given a command-start, SSH-connect, or runner infrastructure failure occurs in
each filing kind in separate runs, then the refusal has
`reasonKind='runner_unavailable'`. Each run inserts no attest.

Given the filing host is reachable but Git reports a missing repository, missing object,
non-commit object, or another semantic negative, when each filing kind runs in separate
runs, then the handler returns `unverifiable_commit_ref`. It inserts no attest.

Given a fault fixture places one of those eight characters in the proposed completion,
selected pre-feature test, or selected pre-feature review repository in separate runs,
when `H` files completion, then completion Git preflight returns
`merge_readiness_repo_control_character` before Git or prompt generation. The assignment
stays open. No completion attest, readiness row, or wake exists.

Given the completion, test, or review verifier has not returned at its own
5,000-millisecond monotonic deadline in separate runs, when that deadline expires, then
Tightbeam terminates that verifier. A later success does not qualify. The handler returns
`merge_readiness_commit_verification_unavailable` with `reasonKind='timeout'`, the exact
phase, host, repository, deadline, and phase-specific retry remedy. The assignment stays
open. No completion or readiness row exists.

Given an unregistered or unknown host occurs in the completion, test, or review phase in
separate runs, when completion preflight runs, then the same refusal has
`reasonKind='unknown_host'`. It carries the exact phase, host, repository, deadline, and
remedy. Preflight writes no row.

Given a command-start failure, SSH-connect failure, or runner infrastructure failure
occurs in each phase in separate runs, when completion preflight runs, then the same
refusal has `reasonKind='runner_unavailable'` and the same required fields. Preflight
writes no row.

Given the host is reachable but Git reports a missing repository, missing object,
non-commit object, or another negative verification result, when preflight runs, then
the handler returns `unverifiable_commit_ref`. It names the phase, host, repository,
deadline, and phase-specific remedy. Preflight writes no row.

Given all three Git checks succeed and a fault fixture pauses before the mutation
transaction, when the fixture changes the proposed completion, authoritative test, or
final clean-review evidence in separate runs, then the transaction reselects the
evidence before its first write. The matrix changes each evidence row id, repository,
and commit in separate runs. Each run returns `stale_merge_readiness_evidence`, names
the changed field, keeps the assignment open, and writes no completion or readiness row.

Given an instrumented verifier records whether the mutation transaction is open, when A1
runs, then it records three calls before transaction entry and zero calls during the
transaction.

### A4. Only the holder's typed test outcome controls

Given another session and a user have note-only `tests-passed` rows on producer `P`, when
`P`'s holder tries to complete, then those rows do not qualify. The handler returns
`merge_readiness_tests_not_current`, keeps `P` open, and creates no readiness state.

### A5. Latest test outcome controls

Given `H` files `tests-passed` for commit `C1` and later files `tests-invalidated` for
`C1`, when `H` tries to complete `C1`, then the handler refuses with
`merge_readiness_tests_not_current`.

Given canonical commits `C1` and `C2` exist in repository `R`, the current holder
`tests-passed` receipt names `{R,C1}`, and completion and the selected clean verdict name
`{R,C2}`, when `H` files completion, then the handler returns
`merge_readiness_tests_not_current`. The assignment stays open. No completion attest,
readiness row, or wake exists.

Given canonical commit `C` exists in repositories `R1` and `R2`, the current holder
`tests-passed` receipt names `{R1,C}`, and completion and the selected clean verdict name
`{R2,C}`, when `H` files completion, then the same refusal and silence apply.

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

Given `H.operationalParent=P1`, `P1` is retired, `P1.operationalParent=P2`, `P2` is
active, and `P2` reaches an active Main self-root through valid parent rows, when `H`
completes qualifying work, then the readiness row and readiness-qualified wake target
`P2`. They do not target `P1` or read `spawnedBy`.

### A10. Long and corrupt parent chains are deterministic

Given a fault-injected database has a missing parent row, a cycle, or an inactive Main,
when `H` files qualifying completion, then the handler returns
`merge_readiness_parent_unavailable`. The completion and readiness transaction rolls back.

Given the operational-parent chain contains 33 consecutive retired sessions followed by
active session `P` and then a valid tail to the active Main self-root, when `H` files
qualifying completion, then completion succeeds. The readiness row and
readiness-qualified wake target `P`.

Given the resolver first reaches active `P1`, later reaches active `P2`, and then
reaches the active Main self-root, when `H` completes qualifying work, then the
readiness target is `P1`. `P2` does not replace it.

Given the resolver first reaches active `P1` and its remaining tail contains a missing
row or a cycle in separate runs, when `H` files completion, then the handler returns
`merge_readiness_parent_unavailable`. It creates no completion or readiness state.

Given the tail reaches an inactive Main or a Main whose `operationalParent` names another
row in separate runs, when `H` files completion, then the same refusal and silence
apply.

### A11. Each readiness and tail failure rolls back completion

Given a temporary database trigger aborts the readiness-row insert, when `H` files a
qualifying completion, then the completion attest, assignment close, notice row,
readiness-qualified wake, optional slate wake, slate-state update, supervision state,
and effort state are absent. After the trigger is removed, one retry commits one
complete required set.

Given a fault fixture raises immediately after one required tail seam succeeds in a
separate run, the matrix covers completion-attest insertion, guarded assignment close,
readiness-row insertion, readiness-qualified wake insertion, optional slate-wake
insertion, slate-state update, disposition-liveness derivation, supervision transition,
and effort-check cancellation or transition. When `H` files a qualifying completion in
each run, then the completion attest, assignment close, readiness row,
readiness-qualified wake, optional slate wake, slate-state update, supervision state,
and effort state are absent. After the fixture is removed, one retry commits one
complete required set.

The slate-wake and slate-state runs make the existing slate condition true before
completion.

Given the required tail succeeds and `append_attest_marker` fails, when the transaction
continues, then the required set and the assignment-close marker commit. The
completion-attest marker is absent.

Given the required tail succeeds and `append_assignment_marker` fails, when the
transaction continues, then the required set and the completion-attest marker commit.
The assignment-close marker is absent.

### A12. Concurrent completion dedupes

Given two concurrent qualifying completion calls for one open producer, when both run,
then one succeeds and one returns the existing terminal-race response. One completion
attest, one readiness row, and one readiness-qualified wake exist.

### A13. Restart preserves one handoff

Given a qualifying completion commits while the prompt scheduler is stopped, when the
gateway restarts, then the same pending readiness-qualified wake remains linked to the
same readiness row. Delivery creates at most one readiness turn because the readiness
wake id is stable. Restart creates no second readiness row or readiness-qualified wake.
An ordinary slate wake keeps its separate identity and lifecycle.

### A14. Payload carries exact evidence

Given A1 commits, when the parent reads the stored prompt and `work-item-trace`, then both
name the producer, work item, repository, commit, cause, cause principal, test verdict,
review, clean verdict, recipient, and readiness-qualified wake from the same readiness
row. The prompt sender and readiness wake origin are `process:tightbeam`.

Given a real repository path contains printable valid UTF-8 such as `répo-雪`, when A1
commits, then the stored row, prompt, and trace retain that exact repository value. The
prompt emits one physical `repo=` line and no generated field creates another prompt
line.

### A15. Replay is exact or refused

Given A1 committed, when `MergeReadiness.open_in_txn/2` receives the same completion id
and the same identity, cause, principal, producer, work item, commit, evidence, recipient,
and wake id again, then it returns the original readiness row. A different proposed notice
id or creation time does not change this result. The original id, `createdAt`, row, and
readiness-qualified wake remain unchanged.

Given the same completion id is replayed with a different `reviewVerdictAttestId` or any
other compared field from I7, when the readiness seam runs, then it returns
`merge_readiness_replay_conflict` and names each unequal field. The existing row remains
unchanged. No second readiness row, readiness-qualified wake, readiness message, or
readiness turn exists. A later linked review introduced through a fault fixture produces
this same refusal.

### A16. Additive activation is exact, atomic, and silent

Given the pre-feature database contains closed code assignments with note-only test
receipts and clean reviews, the global stamp is `model-identity-v1`, the operational-parent
dependency is valid, and zero `merge_readiness_v1` objects exist, when activation runs,
then one transaction creates the two tables and four indexes from I11. It inserts one
valid epoch row. It creates no readiness row, wake, message, turn, or trace entry for the
closed assignments. The feature is unavailable before commit and available after commit.

Given the exact six owned objects and exact activation row exist, when startup runs twice,
then both runs succeed. The object DDL and activation row remain byte-identical.

Given an empty activation, a fault matrix aborts separately after creation of each I11
table and index and after the epoch-row insert. When activation runs for each fault, then
it returns an error. Zero feature-owned objects and zero activation rows remain.

Given a fault fixture presents, in separate runs, one nonempty proper subset, one
malformed object, one duplicate object, or one extra object whose name starts with
`merge_readiness_`, when startup runs, then it raises `Tightbeam.Schema.ShapeError` containing
`incompatible_merge_readiness_v1`. A before-and-after snapshot proves that startup changed
no schema object or row.

Given the exact six objects exist with, in separate runs, a missing, extra, or malformed
activation row, when startup runs, then it raises the same error. A before-and-after
snapshot proves that startup changed no schema object or row.

Given the operational-parent dependency is absent or incompatible, when startup runs,
then its existing shape error occurs before inspection or creation of a
`merge_readiness_v1` object.

Given activation succeeds while code producer `P` remains open, `P`'s holder has a
note-only `tests-passed` verdict, and selected independent review `R1` is closed with
a holder-filed note-only `reviewed-clean` verdict, when the holder first tries to
complete canonical commit `C`, then the handler returns
`merge_readiness_tests_not_current`. It tells the holder to file typed
`tests-passed` for `C`. It creates no completion or readiness state.

Given the holder files that typed test repair and retries completion while `R1` remains
selected, then the handler returns `merge_readiness_review_commit_mismatch`. It names
`R1` as closed and tells the caller to open exactly one new independent successor
review `R2` linked to `P`. It creates no completion or readiness state.

Given `R2` becomes the newest linked review and its holder files typed
`reviewed-clean` for `C`, when the producer holder completes `C`, then one readiness
notice names the typed test receipt and `R2` clean verdict. The note-only test row,
`R1`, and `R1`'s note-only verdict remain byte-identical non-controlling history.

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
3. The pending or delivered readiness-qualified wake and any distinct slate wake.
4. The parent readiness prompt or delivered turn.
5. The `work-item-trace` entry.
6. The unchanged Git refs and deployment state.

Given that captured state, when the test invokes the readiness seam again and restarts
the gateway, then the captured row ids and readiness wake id remain unchanged. No
duplicate readiness prompt or readiness turn appears.

Passing unit tests without this smoke does not satisfy the feature.

### A21. The operating pattern lands with the mechanism

Given the implementation candidate introduces the merge-readiness mechanism, when its
source change is reviewed, then the same change amends
`priv/guidance/operating-manual.md`. The concise directive defines typed
`tests-passed`, exact independent `reviewed-clean`, and the readiness notice as an
approval handoff rather than merge permission.

Given the coder and reviewer guidance changes from Architecture 9, when the guidance
source is inspected, then role-specific commands remain in those role files. The
operating manual does not duplicate the commands. No earlier documentation-only change
publishes the pattern before the mechanism exists.

## Open Questions

None. I1-I15 close the ten load-bearing recon gaps and the seven replacement-review
findings. The controlling owner rulings fix full-tail parent validation, bounded filing
and completion Git checks with typed unavailable reasons, transactional stale-evidence
refusal, no-backfill recovery for open preactivation producers, the required transaction
tail, repository prompt safety, and implementation custody for the operating-manual
directive.

An independent reviewer can reject a ruling or expose a new hole. A material ruling
change must amend this canonical file before the orchestrator binds or implements it.
