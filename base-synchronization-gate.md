# Base-synchronization gate for implementation passes

Status: amended after independent review
`att_230098c5-2a18-4e4c-9191-53220608b1c5`; ready for a fresh independent review  
Work item: `wi_15f960ac-3083-437a-9979-0f0313b7f474`  
Spec assignment: `asg_3e05a07b-ed03-4a90-bff3-f0c446ee31ff`  
Product authority: Mike's direct assignment
`asg_74254cdf-8629-49dc-befe-c20ad253b391`  
Source baseline: Tightbeam `main` at
`cd72fe0b06404afc6619a800c84a6a7eea595baa`  
Baseline observation: the configured SSH remote returned that commit at
`2026-08-12T14:37:25Z`  
Canonical home: `/Users/mike/shared-workspace/shared/specs/tightbeam/base-synchronization-gate.md`  
Operating pattern taught: Agentic Engineering pre-pass base synchronization; the
neutral operating-manual pointer lands in the same shipped batch

## Invariants

### I-01 — The gate precedes goal edits

Each source-changing assignment enters the base-synchronization gate before the
worker's first goal edit. Each `changes-requested` verdict enters a new gate before
the worker's first edit for that review round. Integration operations and conflict
resolution belong to the gate; implementation and review-finding edits do not.

Check: Given a new coding assignment or a new `changes-requested` attest, when the
worker prepares to edit source, then the worker completes and records the gate before
the first goal edit. Current Tightbeam facts expose the worker's release claim and later
receipts; they do not independently observe filesystem edit time.

### I-02 — A principal declares one integration base

The assignment opener or work-item owner user declares the parent or integration base
with a `base-declared` verdict on the worker assignment. The attest row identifies the
principal. Its note identifies the authority, repository, and either one moving ref or
one immutable pin. Repository
policy can supply the cited authority when it names the integration target explicitly.
The worker does not infer a base from a familiar branch name.

Check: Given a repository whose default branch is `main` but whose assignment names no
base and whose policy names no integration target, when the worker starts the gate,
then the gate enters `blocked-base-declaration`; it does not select `main`.

### I-03 — The pass binds to an immutable required commit

At the declaration-binding event in A-02, the worker binds one authorized declaration
to the attempt. The worker then resolves that base to one full immutable revision
before integration. For a moving remote ref, the fetch that observes the ref defines
the current required commit for that attempt. For a pinned base, the declared commit
is the current required commit. A later declaration, correction, or ref movement does
not rewrite the bound attempt; the next attempt or pass selects again.

Check: Given `origin/main` at commit A during the fetch and at commit B after goal
editing starts, when the worker records the gate, then that pass binds to A and the
next rework pass binds to the commit observed by its own fetch.

### I-04 — Synchronization preserves work

The worker integrates on the worker branch. The worker does not reset, restore,
clean, stash, overwrite, or rewrite work owned by another principal. A rebase is
lawful only when repository policy requires or permits it and the worker alone owns
the unpublished branch. The existing merge default remains in force when repository
policy is silent.

Check: Given a shared branch with another principal's commits and a repository that
permits rebase, when the worker enters the gate, then the worker merges or blocks; the
worker does not rewrite the shared branch.

### I-05 — The synchronized baseline is tested before goal edits

After integration and conflict resolution, the worker runs the repository's relevant
baseline test set on the synchronized worker branch. The gate releases only when the
tests pass, a lawful pass-scoped base-red exception exists, or a rework pass contains
only declared `review-target-red` failures under A-06. `review-target-red` permits the
worker to repair the finding after release; it does not excuse a new or changed
failure.

Check: Given a successful merge and no test receipt, when the worker evaluates gate
release, then the state remains `testing-synchronized-baseline` and goal editing does
not start.

### I-06 — Evidence precedes release

Every released attempt has one immutable observation-only `BASE_SYNC_V1` report, one
worker-created Tightbeam `data` artifact row whose SHA-256 matches that report, and one
fixed-shape outcome attest. Only the attest owns the attempt outcome and release
decision. A blocked or interrupted attempt preserves every report byte, artifact row,
and attest that succeeded; it does not fabricate a row that the substrate did not
confirm. An attempt with incomplete evidence cannot release. The `data` kind keeps
this gate evidence from satisfying the separate final-verification `report`
requirement.

Check: Given a green synchronized baseline and no recorded artifact, when the worker
evaluates release, then the gate remains `recording-evidence`.

### I-07 — Review rounds are fresh by event, not time

A `changes-requested` attest invalidates the prior pass's gate for rework. The new
gate identifies that exact attest as its trigger. No elapsed-time threshold decides
freshness.

Check: Given a gate released one minute before a `changes-requested` attest, when the
worker begins the requested edit, then the old gate is stale and a new gate is
required.

### I-08 — Failure is a named blocked state

An unavailable base, failed authentication, failed network operation, unavailable test
set, unresolved conflict, dirty or unproven-clean worktree, or unaccepted baseline red
leaves the gate blocked. The worker records the observed cause and principal in every
evidence seam that remains available. A refusal of the file, artifact, or attest seam
becomes `blocked-evidence`; the worker reports the exact refusal through the operating
manual and does not claim the missing row. The worker does not substitute a stale ref,
another branch, a narrower test set, or fabricated evidence.

Check: Given a failed fetch for a moving base, when a cached remote-tracking ref exists,
then the gate records `blocked-base-unavailable` and does not integrate the cached ref.

### I-09 — Review checks observable consistency and names trust boundaries

The reviewer verifies the latest released gate for the pass under review against the
facts that remain observable: trigger, declaration authority, artifact kind, artifact
creator, artifact hash, recorded commands, repository history, test results, attest
order, and base ancestry in the reviewed commit. The reviewer does not describe the holder's note as independent proof
of the first edit time or of a moving ref's historical tip. Missing or contradictory
evidence is a blocking finding.

Check: Given a rework commit whose only gate predates the triggering
`changes-requested` attest, when the reviewer evaluates the commit, then the reviewer
files `changes-requested` for stale gate evidence.

### I-10 — Detection and procedure each have one home

The new always-on Agentic Engineering guidance file `base-synchronization.md` detects
new and rework passes and directs the acting principal to the elected
`base-synchronization` skill. That skill is the sole home of gate terms, states, role
duties, exceptions, and evidence shapes. `feature-cycle` remains the sole home of
review-card commissioning and completion lifecycle. Each Agentic Engineering manifest
includes the detector and elects the skill. The neutral operating manual names the
installed pattern. `worktree-session` retains worktree custody and points across the
boundary. No rule, rail, second procedure, or organization-local guidance restates
the gate.

Check: Given the assembled Agentic Engineering Kung Fu, when a repository search groups
base-synchronization clauses by responsibility, then the always-on file contains only
event detection and the skill pointer, the skill contains the gate procedure once,
and `feature-cycle` alone contains review-card lifecycle.

## Goal

Ship one Agentic Engineering Kung Fu operating pattern that stops stale-base coding.
Before a new implementation pass or a review-rework pass, the worker must identify the
declared parent or integration base, obtain its current required commit, integrate it
without destroying work, resolve actual conflicts, test the synchronized baseline,
record deterministic evidence, and only then edit the goal.

The change must make three principals accountable:

1. The authorized declaring principal declares the base and the authority for it.
2. The worker runs and records the gate for each pass.
3. The reviewer rejects missing, stale, or false gate evidence.

Success means a stranger session can apply the pattern without inventing a branch,
freshness rule, exception, or evidence format.

## Non-Goals

- This spec does not add a Tightbeam assignment field, state table, parser, rail, rule,
  Git wrapper, hook, or automatic merge service.
- This spec does not change Git, remote hosting, repository permissions, credential
  storage, or network retry behavior.
- This spec does not persist, reconstruct, sanitize, hash, or fingerprint test stdout
  or stderr. Repository- or CI-owned logs remain governed by their existing policy.
- This spec does not persist, sanitize, encode, hash, fingerprint, or reconstruct
  worktree-status output. It retains only the bounded `clean`, `dirty`, or `error`
  preflight result defined below.
- This spec does not choose a universal default branch.
- This spec does not replace repository-owned merge, rebase, test, release, or branch
  protection policy.
- This spec does not require a worker to interrupt an active pass merely because a
  moving base advances after the gate's fetch observation.
- This spec does not replace final integration, independent review, the
  `tests-passed` receipt, the final verification report, or the `verified` verdict.
- This spec does not edit organization-local guidance or live identity state.
- This spec does not make source-less evidence, coordination, review, or runtime-only
  assignments pretend to have a source base.

## Terms

### Implementation pass

A bounded interval in which one worker edits repository source for one assignment. A
pass starts at one of two observable events:

- `new`: the worker is about to make the assignment's first goal edit;
- `rework`: a durable `changes-requested` verdict exists after the prior pass, and the
  worker is about to make the first edit that answers it.

An informational review note that has no `changes-requested` attest does not open a
rework pass. The reviewer must file the verdict before the worker treats the note as a
required edit.

### Goal edit

A source change that implements the assignment or answers a review finding. Fetching,
integrating, and resolving an integration conflict are gate operations, not goal edits.
The worker may not use that classification to add unrelated behavior during conflict
resolution.

### Source material

Repository files or an immutable non-repository source snapshot whose modification is
the assignment's implementation effect. A canonical spec, review record, evidence
report, coordination record, or runtime-only operation is not source material unless
the assignment explicitly ships that artifact as product source.

### Integration base

The line of source history that the worker's result must contain before goal editing
starts. It is one of:

- a moving branch or ref, such as `origin/main` or a stacked branch;
- a pinned immutable commit, such as a release baseline;
- an equivalent immutable revision in a non-Git source-control system.

### Base declaration

An authorized principal's `base-declared` verdict that identifies the integration
base. The assignment opener or work-item owner user is the declaring principal. The
note uses `INTEGRATION_BASE_V1` and cites its authority. An opener cites the assignment
or exact repository policy. The owner user cites
`work-item:<work-item-id>:ownerUserId`; the durable author identity is the owner ruling,
so no prior verdict is required. A live repository policy can supply the authority
when it names the target explicitly. The attest author is the base principal. The
latest valid declaration observed at A-02's declaration-binding event controls that
attempt; older and later declarations remain history for that attempt.

### Assignment opener

The user or session recorded in the worker assignment's `openedByUser` or
`openedBySession` field. A role label, work-item participant, or session that only
sends the wake is not the opener. The opener identity in the `base-declared` attest
must equal the durable assignment field.

### Work-item owner user

The human principal in the work item's durable `ownerUserId` field. This principal can
rule on a missing opener declaration, an exact pass-scoped base-red exception, or a
source snapshot exception. A session, including a product-owner session, does not gain
this authority from its archetype or assignment role.

### Base principal

The user or session that selected the base. The base declaration names this principal
through its attest author so the evidence carries both cause and accountability.

### Moving base

A declared ref whose tip can change. Its current required commit is the full commit ID
returned by the successful authoritative fetch for that gate attempt. A local cached
ref does not prove currentness after a failed fetch.

### Pinned base

A declared immutable revision. Its current required commit is the pin itself. A newer
commit on another branch does not supersede it. If the assignment says "release
branch" without a commit pin, that branch remains a moving base.

### Current required commit

The full immutable revision that the pass must contain. "Latest" in this spec means
the commit observed from the declared moving ref during the gate's successful fetch;
it does not mean the tip of a familiar default branch.

### Worker branch and worker worktree

The branch and durable worktree that the worker owns for the assignment. The worker
integrates the base there. A sibling worktree can expose a parent ref, but the worker
does not edit that sibling worktree.

### Worker session

The full `holderKey` on the worker assignment when the attempt enters `pass-entered`.
The report records that value. The attempt's evidence artifact must have
`createdBySession` equal to it. A later custody change starts a new attempt and cannot
adopt an earlier session's artifact row.

### Base-synchronization gate

The conceptual pass state derived from repository facts, gate report artifacts, and
assignment attests. It is guidance, not a new substrate state row. `released` is the
only state that permits goal edits.

### Synchronized baseline

The worker branch after it contains the current required commit, after conflict
resolution, and before goal edits for the pass. During rework, it includes the prior
reviewed implementation plus the newly integrated base.

### Relevant baseline test set

The commands that repository policy requires for the assignment's declared files and
effect, plus tests that exercise each resolved conflict path and each exact failing
command named by the triggering `changes-requested` verdict. When policy requires a
full gate, the full gate is relevant. When policy defines a docs-only gate, that gate
is relevant. When policy names no baseline command, the worker records exact existing
test commands that exercise the declared effect. If the worker cannot identify or
start such a command, the set is unavailable and the gate enters
`blocked-test-unavailable`; an empty set does not release the gate. The worker does not
narrow the set after seeing failures.

### Repository policy

An applicable written source-control or test directive cited by the declaration or
assignment. For a checked-in directive, `worker_head_before` binds the bytes at the
cited `path:line`. For an external hosting rule, the declaration identifies its
durable source and revision. A remembered convention or uncited branch name is not
repository policy.

### Baseline red

A failure in the relevant test set on the synchronized baseline. It is one of:

- `review-target-red`: the command identity and exit status are the durable subject of
  the triggering `changes-requested` verdict and satisfy every A-06 comparison;
- `base-originated`: the same failure reproduces on a clean checkout of the current
  required commit without the worker's prior implementation;
- `worker-branch-or-integration`: every other failure.

For `review-target-red` and `base-originated`, the same failure means the same Safe
test evidence command identity and exit status. The gate does not compare process
output.

Only `review-target-red` or a lawful exception for proved `base-originated` red can
release a red gate.

### Safe test evidence

The gate records a test's command identity, revision, environment qualifier, exit
status, concise result, and classification. The command identity is the exact
repository command text before shell, environment, credential-provider, or runner
expansion, or an exact repository `path:line@revision` entrypoint plus its non-secret
arguments. It includes no literal or expanded credential value, credential-bearing
URL, unrestricted environment dump, or process argument reconstructed after secret
injection. The environment qualifier names the repository-required lane, such as a
harness name, or is `null`; it contains no environment value.

`result` is exactly `passed` when `exit=0` and `failed` when `exit` is nonzero. The gate
report does not contain, encode, sanitize, hash, or fingerprint stdout or stderr and
does not add a gate-owned output artifact. A worker can inspect transient command
output to resolve a conflict, but does not copy it into gate evidence. A citation to
an existing repository or CI run establishes only its command identity, revision, and
exit; its independently governed logs do not become gate evidence.

For `review-target-red`, the durable comparison tuple is the reviewed commit, command
identity, and exit status. This version intentionally treats two failure causes with
the same command identity and exit as the same pre-edit red observation. The later
post-edit test and independent review determine whether the requested repair worked;
the gate does not add output-capture machinery to distinguish the causes.

### Preflight cleanliness evidence

The gate records one preflight entry with exactly `command`, `exit`, and `result`. For
Git, `command` is exactly
`git status --porcelain=v1 --untracked-files=all`. The worker executes it without a
wrapper that changes its stdout. The worker maps the observation as follows:

- exit 0 and zero stdout bytes -> `result=clean`;
- exit 0 and one or more stdout bytes -> `result=dirty`;
- nonzero exit, or failure to start -> `result=error`.

`exit` is the process exit integer, or JSON `null` when the command did not start. The
worker measures only whether stdout is empty; it does not decode the stream. The
worker retains no stdout or stderr bytes, byte count, path, encoding, hash,
fingerprint, or other stream-derived value. The `clean` or `dirty` category is the
sole evidence value computed from worktree-status output. The required
`stop_observation` and outcome-attest fields consume that category through the fixed
A-07 and A-08 mapping; those mappings do not inspect a stream. A-07 separately
enumerates the other lawful source-control facts; none retain their underlying
process streams.

For non-Git source control, repository policy must name an exact status command and a
deterministic clean/dirty predicate. The worker normalizes that predicate to the same
three results and records no process output. When policy supplies no deterministic
predicate, or the command returns an unclassified observation, the worker records
`result=error` and the gate enters `blocked-worktree`; the worker does not invent a
predicate.

A `dirty` result sets `stop_observation` to
`{"event":"worktree-not-clean","reason":"preflight-dirty"}`. An `error` result
sets it to
`{"event":"worktree-not-clean","reason":"preflight-error"}`. These are the only
preflight stop reasons.

### Actual conflict

Either a textual conflict reported by source control or a semantic conflict revealed
by the synchronized-baseline tests after A-06 excludes exact `review-target-red` and
proved `base-originated` failures. Conflict resolution may combine compatible
authorities. When the base and assignment require incompatible behavior, the worker
records `blocked-conflict` and sends the decision through the assignment opener under
A-05.

### Already current

The current required commit is already an ancestor of the worker branch, or the
source-control equivalent proves inclusion. In Git, the canonical no-op proof is
`git merge-base --is-ancestor <required-commit> HEAD` with exit status 0, plus equal
pre- and post-gate worker commit IDs.

### Lawful exception

A narrow authorization that changes one gate decision without waiving the gate.
Exceptions can accept a proved base-originated red set or authorize an immutable source
snapshot when ordinary source control does not exist. They cannot waive base identity,
work preservation, conflict resolution, evidence, or review. They expire with the gate
ID they name.

### Source-less task

An assignment that changes no repository or source snapshot. Read-only recon,
coordination, review, release observation, and a runtime-only operation can be
source-less. A task is not source-less merely because its files are outside Git.

### Gate ID

The stable identity of one pass:

- `new:<assignment-id>` for the first implementation pass;
- `rework:<changes-requested-attest-id>` for a review-rework pass.

Each attempt under a gate ID receives an integer `attempt` starting at 1. A failed
attempt remains immutable when a later attempt releases the gate.

### Attest-note encoding

Every marker note in this spec is one line with no leading or trailing whitespace. It
uses the shown key order, no insignificant whitespace, raw UTF-8 for non-ASCII text,
and the shortest JSON escape required for quotation marks, reverse solidus, and control
characters. The complete marker, one ASCII space, and JSON object must be at most 2,000
UTF-8 bytes. This byte bound is at or below Tightbeam's 2,000-character rail for every
valid UTF-8 note. The writer measures the final encoded line before calling Tightbeam.
The writer never truncates, splits, or silently substitutes a pointer.

When a required note exceeds the bound, the actor does not call the oversized form.
An assignment holder files a progress attest, and any other authorized actor files a
`base-sync-note-too-long` verdict, with this bounded fallback:

```text
BASE_SYNC_NOTE_LIMIT_V1 {"shape":"INTEGRATION_BASE_V1","gate_id":"new:asg_example","attempt":null,"encoded_bytes":2001}
```

`shape` is `INTEGRATION_BASE_V1`, `BASE_RED_EXCEPTION_V1`,
`SOURCE_BASE_EXCEPTION_V1`, or `BASE_SYNC_V1`. `gate_id` and `attempt` copy the
oversized note's values or use JSON `null` when that shape has no value.
The fallback author must be the actor authorized to file the oversized note. It never
declares a base, grants an exception, records an outcome, or releases a gate. It maps
an oversized declaration to `blocked-base-declaration`, an oversized exception to the
blocked state already in force, and an oversized outcome to `blocked-evidence`.

### Next principal

The durable principal named to clear a blocked gate. It is the assignment opener for
a missing or contradictory declaration, unavailable base, network or credential
failure, unsafe integration method, incompatible source authority, unavailable test,
or evidence-recording failure. It is the owner of pre-existing work for
`blocked-worktree`, or the assignment opener when that owner cannot be identified. It
is the work-item owner user when a proved base-red or source-snapshot exception needs
authorization. The assignment opener obtains a spec-writer or product-owner ruling
when incompatible authorities need judgment; the worker does not choose that actor or
the outcome.

## Assumptions

- Tightbeam supports holder-filed `progress` attests with notes up to 2,000 characters.
  The gate's 2,000-byte emitted-note limit is a conservative, deterministic subset.
- Tightbeam supports session-recorded `data` artifacts with a path, work-item link, and
  optional caller-supplied SHA-256. `artifact-record` stores that claim without hashing
  the file; the worker computes it and the reviewer independently compares the bytes.
- Tightbeam accepts lower-case, hyphenated verdict kinds from a session or user. This
  spec uses `base-declared`, `baseline-red-accepted`, and
  `base-exception-approved`, plus the non-authorizing
  `base-sync-note-too-long` fallback.
- Tightbeam orders assignment attests by timestamp and ID, so a reviewer can compare a
  gate release claim with its triggering verdict and later test receipt. This ordering
  does not observe repository edit time.
- The current assignment record has no structured integration-base field. The first
  shipped version therefore uses an opener-filed verdict plus a holder-filed gate
  report. It does not claim that the substrate parses either note.
- Repository guidance remains authoritative for the integration method and test set.
  A repository that states neither leaves the current Kung Fu merge default in force
  and requires the opener to declare a base.
- Reviewable work is committed before a reviewer evaluates ancestry. Uncommitted review
  input is an evidence gap.
- A remote ref can move immediately after observation. The gate binds the observation
  event; it does not claim a permanent lock on the remote.
- Each shipped Agentic Engineering archetype manifest can include the shared detector
  and elect a shipped skill. The implementation does both in all six manifests.
- The spec workspace search found no current spec for this pattern.

## Architecture

### A-01 — State machine

The state machine is a normative workflow derived from evidence. Implementation does
not add a substrate status field.

| State | Entry fact | Required action | Release or next state |
| --- | --- | --- | --- |
| `pass-entered` | New assignment before its first goal edit, or a new `changes-requested` attest | Record the assignment's current full holder key as `worker_session`. Compute the gate ID and attempt number. Inspect worktree ownership and cleanliness. | `awaiting-base-declaration`; `dirty` or `error` preflight -> `blocked-worktree` |
| `awaiting-base-declaration` | No complete authorized `base-declared` verdict is bound | Read the latest authorized declaration and cited repository policy. Ask the assignment opener or work-item owner user when it is absent or contradictory. Bind the selected declaration to this attempt when leaving the state. | `resolving-base`; missing answer -> `blocked-base-declaration` |
| `resolving-base` | One declaration names repository, principal, authority, and ref or pin | Obtain the required commit by the source-specific procedure in A-03. | `integrating`; transport/auth/ref failure -> `blocked-base-unavailable` |
| `integrating` | Full current required commit exists locally | Prove already-current or apply the repository-authorized integration method on the worker branch. | `testing-synchronized-baseline`; reported conflict -> `resolving-conflicts` |
| `resolving-conflicts` | Source control or tests expose incompatible combined state | Resolve compatible textual or semantic conflicts. Record the paths and resolution commits. | `testing-synchronized-baseline`; incompatible authority -> `blocked-conflict` |
| `testing-synchronized-baseline` | Worker branch contains the required commit | Run the relevant baseline test set without goal edits. | `recording-evidence`; red -> A-06; no selectable or startable command -> `blocked-test-unavailable` |
| `recording-evidence` | Release or stop observations are known | Write and hash the immutable observation report when the session filesystem is available, attempt the artifact row, then attempt the fixed-shape outcome attest. | `released` only when a valid attest says `status=released`; any incomplete or invalid evidence -> `blocked-evidence` and A-08 recovery |
| `released` | A valid released attest exists for this gate ID and attempt | Permit goal edits for this pass. | A later `changes-requested` enters a new `pass-entered` state. |
| `not-applicable` | The assignment is source-less under A-10 | Record the classification only when the assignment otherwise presents as implementation work. | No source gate applies. A source file discovered later enters `pass-entered`. |

Blocked states retain the assignment and worktree. The worker attempts progress with
the exact observation, evidence path when one exists, and the principal who must act.
If the evidence seam refuses, I-06 and I-08 preserve the maximal successful material
without inventing a row. The worker resumes the same gate ID with the next attempt
after the cause clears.

Check: Given a credential failure on attempt 1 and a successful fetch on attempt 2,
when the worker resumes, then both attempts remain in durable evidence and only
attempt 2's outcome attest records `status=released`.

### A-02 — Base declaration and precedence

The assignment opener creates each source-changing worker assignment, ensures that the
opener or work-item owner user files a valid `base-declared` verdict, and only then
wakes the worker. Atomic `dispatch` cannot meet
that order. A-12 therefore refactors the orchestrator kernel so a source-changing card
joins file-declaring and review-linking cards on the `assign`, required-facts, `wake`
path. The work-item owner user can also file the declaration or a correction directly.
The verdict note uses one line of minified JSON
after this exact marker. The declaring principal chooses one of these five valid value
forms. Keys remain in this order:

```text
INTEGRATION_BASE_V1 {"repo":"<host:absolute-path>","kind":"moving","ref":"<remote-or-local-ref>","pin":null,"authority":"<authority>"}
INTEGRATION_BASE_V1 {"repo":"<host:absolute-path>","kind":"pinned","ref":null,"pin":"<full-commit>","authority":"<authority>"}
INTEGRATION_BASE_V1 {"repo":"<host:absolute-path>","kind":"pinned","ref":"<authorized-fetch-ref>","pin":"<full-commit>","authority":"<authority>"}
INTEGRATION_BASE_V1 {"repo":"<non-git-source-id>","kind":"non-git","ref":"<declared-line>","pin":null,"authority":"<authority>"}
INTEGRATION_BASE_V1 {"repo":"<snapshot-source-id>","kind":"non-git","ref":null,"pin":"<immutable-revision-or-snapshot-sha256>","authority":"<authority>"}
```

The JSON values for `ref` and `pin` are JSON `null`, not the string `"null"`, when
absent. `authority` is an assignment ID, an exact repository `path:line`,
`work-item:<work-item-id>:ownerUserId`, or an exception attest ID where A-10 requires
one.

The opener uses the existing command:

```text
tightbeam attest <worker-assignment> --kind verdict --verdict base-declared --note "<INTEGRATION_BASE_V1 note>"
```

The worker verifies that the attest author is the assignment opener or the work-item
owner user. An opener's `authority` cites the assignment or exact repository policy.
An owner user's `authority` is `work-item:<work-item-id>:ownerUserId`; the author's user
identity must equal that field on the durable work item. For an A-10 source-snapshot
declaration, either authorized principal instead cites the `base-exception-approved`
attest; the worker verifies that exception's author against the durable `ownerUserId`.
The worker copies the attest ID and values into the gate report and rejects a
declaration from another principal. A correction is a later authorized
`base-declared` verdict. The declaration
precedence is:

1. An authorized declaration that cites and matches an exact parent, release, or
   integration target in live repository policy.
2. An exact integration base or commit pin in a work-item owner user's declaration
   that does not contradict live repository policy.
3. An assignment opener's declaration that cites an exact base in the assignment and
   does not contradict live repository policy.
4. No base. The gate blocks and the opener must declare one.

Within one precedence level, the latest authorized declaration that the worker observes
when transitioning from `awaiting-base-declaration` to `resolving-base` controls that
attempt. This transition is the declaration-binding event. A declaration or correction
filed after that event applies to the next attempt or pass; it does not retroactively
invalidate or race the current release. Current Tightbeam has no compare-and-swap seam
between attest observation and gate release, so this version makes no stronger
in-flight guarantee.

A branch name without a repository or source ID is incomplete. A moving declaration
sets `pin=null` until resolution. A pinned declaration sets `ref=null` unless the ref
is evidence for obtaining the pin; the pin remains authoritative.

For stacked branches, the assignment opener declares the immediate parent branch or
commit, not `main`, unless repository policy says the stack flattens before each child
pass. The parent must expose a committed revision. Uncommitted parent work is not a
base.

Check: Given child branch C stacked on parent P while `main` also advances, when the
orchestrator dispatches C, then the declaration names P. The worker obtains P's current
committed tip and does not substitute `main`.

### A-03 — Establishing the current required commit

The worker follows the declared base kind:

1. For a remote-backed moving Git ref, run the repository-approved authenticated fetch
   for that exact remote and ref. Resolve the fetch result (`FETCH_HEAD` or the exact
   destination ref written by that fetch) to a full commit ID. Do not resolve an
   unchanged cached tracking ref. The successful fetch response is the observation
   event.
2. For a local stacked Git ref, resolve the declared ref once for this attempt and
   record the full committed tip as the observation event. Verify that the named ref
   resolves to that commit in the shared object database. A dirty parent worktree does
   not change the commit.
3. For a pinned Git commit, verify that the exact object exists and is a commit. Fetch
   that exact object or its authorized ref when it is absent. Do not advance to a newer
   branch tip.
4. For non-Git source control, use the repository's command that obtains the declared
   line and returns an immutable revision. Record that command and revision.

A failed network call, credential refusal, missing remote, missing ref, deleted parent,
or unavailable object enters `blocked-base-unavailable`. A cached moving ref cannot
release the gate after such a failure. Offline operation is lawful only for a pinned
commit that is already present and whose declaration does not require remote
attestation.

Check: Given an offline worker, a locally present pinned release commit R, and an
assignment that pins R, when the worker resolves the base, then R is current for the
gate without a network call. The report records `observation_kind=pinned-local`.

### A-04 — Integration method and work preservation

For Git, repository policy decides between merge and rebase. When policy is silent, the worker
merges the declared base into the worker branch, preserving the shipped Kung Fu
default. A repository-authorized rebase also requires sole worker ownership and an
unpublished branch. A policy that requires rebase on a shared or published branch is a
conflict that the opener must rule by supplying a safe branch or policy-consistent
method; the ruling cannot authorize a shared-history rewrite.

Before integration, the worker records `worker_head_before` and one Preflight
cleanliness evidence entry. Integration starts only when `result=clean`. A `dirty` or
`error` result enters `blocked-worktree`; the worker does not treat exit 0 alone as
clean. The worker can preserve its own authorized prior-pass work in reviewable
commits before retrying the gate. The worker does not commit another principal's work
and does not use a mutating stash.

For an already-current Git branch, the worker records the exit status of
`git merge-base --is-ancestor <required-commit> HEAD`. The integration result is
`already-current`, `worker_head_after` equals `worker_head_before`, and no empty merge
commit is created.

For an integration operation, the worker records the exact method, command, pre-head,
post-head, and required commit. The resulting branch must contain the required commit.
For rebase, the ancestry check applies to the rewritten post-head.

Check: Given required commit R is already an ancestor of worker head W, when the gate
runs, then the report records exit 0, `result=already-current`, and identical pre- and
post-head W.

### A-05 — Conflict handling

The worker records textual conflict paths from source control before resolving them.
The worker reads the merge base, both sides, callers, tests, and cited authorities. The
worker combines compatible behavior and records each resolution commit.

A synchronized-baseline failure that appears only on the combined branch and is not an
exact A-06 `review-target-red` failure is a semantic conflict. The worker may make only
the reconciliation edit needed to preserve compatible base and assignment behavior.
The worker records those paths as conflict paths and reruns the relevant baseline test
set. This edit remains a gate operation.

When the two authorities are incompatible, the worker does not choose a side. The gate
records `blocked-conflict` with the assignment opener as `next_principal`. The opener
obtains a durable ruling from the current spec writer when the conflict is within the
spec, or from the product owner when it changes product intent. The ruling amends its
canonical source before the worker starts the next attempt.

Check: Given a merge that reports conflicts in `lib/a.ex` and `test/a_test.exs`, when
the worker resolves them, then the attempt report lists both paths, the resolution
commit, the rerun commands, and their results.

### A-06 — Synchronized-baseline tests and red handling

The worker selects tests before running them from the assignment's declared files,
effect, repository policy, and conflict paths. The report records each safe command
identity, environment qualifier required by repository policy, revision, exit status,
`passed` or `failed` result, and classification under the Safe test evidence term. It
does not record or derive stdout or stderr.

If the worker cannot identify a command that exercises the declared effect, or a
required environment prevents the command from starting, the worker records
`blocked-test-unavailable`, a concise non-secret cause category written without
process output, and the assignment opener as the next principal. A command that starts
and exits nonzero is baseline red, not unavailable.
Provider credentials do not make a test unavailable. The worker runs a credentialed
repository-required command when the authorized credentials work, while excluding
credential values and process output from gate evidence. A credential refusal is an
unavailable required environment. The worker does not substitute a narrower command
to avoid a required credentialed lane.

When tests fail, the worker classifies the red result:

1. On a rework pass, classify a failure as `review-target-red` only when all of these
   facts match:
   - the triggering `changes-requested` verdict identifies the exact reviewed commit,
     safe command identity, and exit status as a required repair;
   - `worker_head_before` equals that reviewed commit;
   - the worker reproduces that command identity and exit status on an
     isolated checkout of `worker_head_before` and on the synchronized baseline;
   - the synchronized run contains no additional failing command identity and no
     named target whose exit status changed.
2. Release a rework gate with `test_result=review-target-red` when every red result
   satisfies step 1. The post-release goal edit repairs those declared findings. This
   classification is not a baseline-red exception and expires with the rework gate ID.
3. For every remaining failure, reproduce the same command on a clean checkout of the
   current required commit. A CI log or pointer cannot replace this gate-owned
   command/revision/exit observation.
4. If the remaining failure does not reproduce on the required commit, treat it as a
   worker-branch or integration conflict. Resolve it under A-05 or block.
5. If the remaining failure reproduces on the required commit, record it as
   `base-originated`.
6. Keep a `base-originated` gate blocked unless a live repository directive already
   names that command identity and exit status at that exact base commit, or the
   work-item owner user files `baseline-red-accepted` on the worker assignment.

A review note without every comparison fact in step 1 cannot authorize
`review-target-red`. The worker does not relabel a command identity or omit additional
failing test entries to make the comparison pass. This comparison intentionally does
not inspect or persist the command's failure output.

Before requesting an owner-user exception, the worker records the failed gate attempt
under A-07 and A-08 with `status=blocked-baseline-red`. The exception cites that
immutable artifact. A later release attempt repeats base observation and the relevant
tests. The exception applies only when the required revision and failure set still
match the cited attempt's command identities and exit statuses.

The owner-user exception note uses this marker and exact JSON key order:

```text
BASE_RED_EXCEPTION_V1 {"gate_id":"<gate-id>","required_revision":"<full-revision>","failure_artifact_id":"<blocked-attempt-artifact-id>","failure_artifact_sha256":"<hex>","reason":"<why-the-assignment-remains-valid>","principal":"user:<ownerUserId>","overrides_policy":null}
```

`overrides_policy` is a JSON string containing the exact `path:line` when the
exception overrides a green-baseline directive. It is JSON `null`, not the string
`"null"`, when no such directive exists. The override form changes only the final
value to `"<path>:<line>"`; the key order remains unchanged.

The cited blocked-attempt artifact contains the safe failing command identities,
revisions, environments, exits, and results. The gate ID is the exception's expiry. The worker,
orchestrator, reviewer, and product owner cannot authorize it by session role. Only the
work-item owner user or an already-live exact repository directive can authorize it. A
user exception must cite and override any repository directive that requires a fully
green baseline.

The exception changes the release attest's `test_result` to `accepted-base-red`; the
report keeps each failing test visible. A later rework gate must reclassify and
reauthorize the failures.

Check: Given test T fails on both the synchronized branch and required commit R, when
the work-item owner user files a pass-scoped `baseline-red-accepted` verdict for T and R,
then the gate can release with `accepted-base-red`. A later rework gate has no exception
until a new verdict names its gate ID.

### A-07 — Deterministic evidence report

Before an attempt can release, the worker writes one observation-only UTF-8 JSON object
with a final newline and the complete field set below. For a blocked attempt, the
worker writes the same report when its session filesystem is available and preserves
the file even when a later substrate step refuses. The report records inputs, commands,
and results that exist before `artifact-record`; it does not contain the attempt's
release or blocked outcome.
Object-key order, insignificant whitespace, and equivalent JSON escaping are not
normative. Arrays preserve execution or path order. Empty values use `null` or an empty
array; the worker does not omit keys. The artifact SHA-256 pins the exact bytes written
by that attempt.

```json
{
  "schema": "BASE_SYNC_V1",
  "gate_id": "new:asg_example",
  "attempt": 1,
  "assignment_id": "asg_example",
  "work_item_id": "wi_example",
  "worker_session": "agent:main:example s_example",
  "pass_kind": "new",
  "trigger_attest_id": null,
  "observed_at": "2026-08-12T07:37:55Z",
  "repo": "host:/absolute/repository",
  "worker_branch": "coder/example",
  "worker_head_before": "full-revision",
  "preflight": [
    {"command": "git status --porcelain=v1 --untracked-files=all", "exit": 0, "result": "clean"}
  ],
  "base_declaration_attest_id": "att_example",
  "base_principal": "session:agent:orchestrator:example s_example",
  "base_authority": "AGENTS.md:40",
  "base_kind": "moving",
  "base_ref": "origin/main",
  "base_pin": null,
  "observation_kind": "fetched-ref",
  "observation_commands": [
    {"command": "git fetch origin main", "exit": 0, "result": "origin/main -> full-revision"}
  ],
  "required_revision": "full-revision",
  "integration_method": "merge",
  "integration_commands": [
    {"command": "git merge-base --is-ancestor full-revision HEAD", "exit": 0, "result": "ancestor"}
  ],
  "integration_result": "already-current",
  "worker_head_after": "full-revision",
  "conflict_paths": [],
  "resolution_revisions": [],
  "tests": [
    {"command": "repository-defined command before credential expansion", "revision": "full-worker-revision", "environment": "harness-name", "exit": 0, "result": "passed", "classification": "passed"}
  ],
  "stop_observation": null,
  "exception_verdict_id": null,
  "exception_authority": null
}
```

Each test entry records the exact revision on which the command ran. A base-red
classification contains separate synchronized-worker and required-base entries, even
when their command strings match. A `review-target-red` classification contains the
isolated `worker_head_before` and synchronized-worker entries. `environment` is the
repository-required non-secret qualifier or `null`; it never contains an environment
value or credential. `command` satisfies the Safe test evidence term even when the
repository runner obtains credentials at runtime.
`classification`
is `passed`, `review-target-red`, `base-originated`, or
`worker-branch-or-integration`. A report's `pass_kind` is `new` or `rework`.
The source-less A-08 attest uses `source-less` and creates no report. `base_kind` is
`moving`, `pinned`, or `non-git`. Allowed non-null `observation_kind` values are
`fetched-ref`, `stacked-local`, `pinned-local`, and `non-git-current`. Allowed non-null
`integration_method` values are `merge`, `rebase`, `repository-update`,
`snapshot-apply`, and `none`. A field is `null` when its step was not reached. Allowed
`integration_result` values are `already-current`, `integrated`,
`conflicts-resolved`, `conflicted`, and `not-run`.

A test entry has exactly `command`, `revision`, `environment`, `exit`, `result`, and
`classification`. A zero exit has `result=passed`; a nonzero exit has
`result=failed`. The entry contains no process output or value derived from process
output.

`stop_observation` is `null` when the observations meet a release condition. Otherwise
it is an object with exactly `event` and `reason`. `reason` is a concise non-secret
category written without copying process output; it is not an outcome or release
decision. Allowed `event` values and their A-08
outcome mappings are:

| Observed event | Outcome status |
| --- | --- |
| `base-declaration-invalid` | `blocked-base-declaration` |
| `base-unavailable` | `blocked-base-unavailable` |
| `worktree-not-clean` | `blocked-worktree` |
| `conflict-unresolved` | `blocked-conflict` |
| `test-unavailable` | `blocked-test-unavailable` |
| `baseline-red-unaccepted` | `blocked-baseline-red` |

An artifact-recording or attest failure happens after the report is written and cannot
appear in `stop_observation`; A-08 maps that later fact to `blocked-evidence`.

`observed_at` is the UTC RFC 3339 time immediately after the base observation. It is
`null` when the attempt stops before a base observation.
`base_pin` copies the declaration's full Git commit, immutable non-Git revision, or
snapshot SHA-256; it is null when the declaration uses a moving ref. A principal value
is `user:<id>` or `session:<full-session-key>`. `conflicted` records an unresolved
attempt; `conflicts-resolved` records a successful reconciliation.

`preflight` contains exactly one Preflight cleanliness evidence entry recorded before
integration. It retains the categorical result and no command output. Only
`result=clean` permits integration. `integration_commands` records each exact
ancestry, merge, rebase, or non-Git update command in execution order. An
already-current attempt records its ancestry command. An integrated attempt records
its merge, rebase, or repository-update command and the post-operation inclusion
check. An integration command entry has exactly `command`, `exit`, and `result`.

Without an exception, both exception fields are `null`. A repository-authored
base-red allowance sets `exception_authority` to its exact `path:line` and leaves
`exception_verdict_id` null. An owner-user exception sets the verdict ID and uses
`attest:<same-id>` as its authority.

The file path is:

```text
<session-workdir>/evidence/base-sync/<assignment-id>/<new--assignment-id|rework--attest-id>--attempt-<n>.json
```

The worker never overwrites an attempt file. The worker hashes the bytes with SHA-256,
then records it:

```text
tightbeam artifact-record --kind data --title "base sync <gate-id> attempt <n>" --path "<absolute-report-path>" --description "BASE_SYNC_V1 evidence" --work-item <work-item-id> --sha256 <hex>
```

The returned artifact row must have `kind=data`, `createdBySession` equal to the
report's `worker_session`, the same work item and path, and `contentSha256` equal to the
computed hash. A different kind or creator is invalid evidence even when every other
field and byte matches.

The report records no raw stdout or stderr. Test entries and classifications contain
no value derived from test-process output; they retain only the six fields that this
schema enumerates. Non-test source-control evidence is limited to the non-test fields
explicitly listed in the complete A-07 schema, and each value satisfies that field's
definition. The report does not retain the underlying process streams or add a
non-schema source-control value. The report also
excludes credentials, tokens, credential-bearing remote URLs, expanded credential
arguments, and unrestricted environment dumps. Runtime credential injection does not
make the repository-required command unavailable or prevent its safe pre-expansion
identity from entering the report. The deterministic stop and outcome fields consume
the preflight category; they do not inspect output and are not new stream
observations.

Check: Given one attempt report, when a reviewer parses it, then every listed field is
present with the specified type, each command and path array preserves observed order,
the file is UTF-8 with a final newline, and its exact bytes match the artifact SHA-256.

### A-08 — Deterministic assignment attest

After artifact recording, the worker files a holder progress attest. The note is one
line of minified JSON after the marker. Keys remain in this order:

```text
BASE_SYNC_V1 {"gate_id":"new:asg_example","attempt":1,"pass_kind":"new","trigger_attest_id":null,"base_declaration_attest_id":"att_example","base_ref":"origin/main","required_revision":"full-revision","integration_result":"already-current","worker_head_after":"full-revision","test_result":"passed","exception_verdict_id":null,"exception_authority":null,"artifact_id":"art_example","artifact_sha256":"hex","status":"released","blocked_reason":null,"next_principal":null}
```

The worker applies the attest-note encoding term before the call. When this exact form
would exceed 2,000 UTF-8 bytes, the worker files the bounded
`BASE_SYNC_NOTE_LIMIT_V1` progress attest instead and the attempt becomes
`blocked-evidence`; the oversized outcome never takes effect.

The release attests use `pass_kind=new` or `pass_kind=rework`. The source-less
classification uses `pass_kind=source-less`. `test_result` is `passed`,
`review-target-red`, `accepted-base-red`, `failed`, or `not-run`. The worker uses the
same shape for blocked attempts and changes `status`, `test_result`, and available
fields without omitting keys. Allowed `status` values are `released`,
`blocked-base-declaration`, `blocked-base-unavailable`, `blocked-worktree`,
`blocked-conflict`, `blocked-test-unavailable`, `blocked-baseline-red`, and
`blocked-evidence`; `not-applicable` exists only in the source-less attest. The worker
files a released attest only after `artifact-record` returns its artifact ID.

For blocked attempts, `blocked_reason` is the exact non-null A-07
`stop_observation.event`, or one of `artifact-record-failed`,
`artifact-row-invalid`, `artifact-row-ambiguous`, `artifact-row-missing`,
`artifact-bytes-mismatch`, `outcome-note-too-long`, and `outcome-attest-refused`.
It is not free-form text. `next_principal` carries the exact principal from the term
above. The gate report retains no stdout, stderr, fingerprint, or reconstructed
failure detail.

When artifact recording fails, the worker files `status=blocked-evidence`, sets the
artifact fields to `null`, and names the failure and responsible principal in
`blocked_reason` and `next_principal`. That attest does not release the gate. If
Tightbeam also refuses the attest, the worker reports the exact substrate refusal to
its supervisor under the operating manual; the local attempt file remains evidence.

An interruption does not imply an outcome. The outcome attest is derived without
judgment from the validated report and the artifact-record result. A non-null
`stop_observation.event` maps to the blocked status in A-07's table. With
`stop_observation=null`, the only valid release mappings are:

- every test passes -> `test_result=passed`;
- at least one test is `review-target-red`, every other test passes, and A-06's exact
  comparisons hold -> `test_result=review-target-red`;
- at least one test is `base-originated`, one valid exception covers every such
  failure, and every other test passes or is `review-target-red` ->
  `test_result=accepted-base-red`.

Any other field combination is invalid evidence and maps to `blocked-evidence`; it
cannot release. On restart, the worker reads artifacts and attests for the exact gate
ID and attempt before any mutation:

1. When an outcome attest already exists, it is authoritative for the recorded
   outcome and the worker files no duplicate. Before honoring a released outcome, the
   worker locates the cited artifact and repeats the row, report, and SHA-256 checks in
   step 2 except for the current-holder comparison. For this completed attempt,
   artifact `createdBySession`, report `worker_session`, and outcome-attest `bySession`
   must equal each other. A later assignment holder does not invalidate valid completed
   evidence. A mismatch or unavailable cited artifact prevents goal edits, is reported
   as an evidence integrity failure, and starts a fresh numbered attempt. A blocked
   outcome resumes through a fresh numbered attempt after its cause clears.
2. When one matching artifact row exists and no outcome attest exists, the worker
   rehashes the file and compares its kind, creator, path, SHA-256, work item, schema,
   gate ID, attempt, and worker session with the row. `kind` must be `data`;
   `createdBySession` and report `worker_session` must equal the assignment's current
   holder. If all values match and no later attempt exists, the worker
   applies the mapping above and files the derived outcome attest for that same
   attempt. A mismatch produces `blocked-evidence`; the worker does not amend the
   artifact row.
3. When no matching artifact row exists, the worker does not replay
   `artifact-record`, because a lost response can hide a committed row. The worker
   files `blocked-evidence` with null artifact fields when Tightbeam accepts the
   attest, preserves the local file, and starts a fresh numbered attempt.
4. When multiple rows match the same path, gate ID, attempt, or SHA-256, the worker
   records `blocked-evidence`, reports the evidence-integrity incident to the
   assignment opener, and starts a fresh numbered attempt. No ruling can make an
   ambiguous attempt release.

These rules make a report-to-artifact or artifact-to-attest interruption recoverable
without overwriting files, fabricating success, or creating a duplicate artifact on
purpose.

The report is the detailed evidence. The attest is the ordered release marker that a
reviewer can find without interpreting prose. Tightbeam does not parse either shape in
this version. The base gate does not file `tests-passed`, `verified`, or a `report`
artifact. Those existing receipts remain reserved for the later implementation and
final-verification gates.

A source-less classification uses the same attest keys, creates no gate artifact, and
uses one of these exact `blocked_reason` values: `read-only-recon`, `coordination`,
`review`, `release-observation`, `runtime-only`, or `evidence-or-spec-only`. It uses
this exact value shape:

```text
BASE_SYNC_V1 {"gate_id":null,"attempt":0,"pass_kind":"source-less","trigger_attest_id":null,"base_declaration_attest_id":null,"base_ref":null,"required_revision":null,"integration_result":"not-run","worker_head_after":null,"test_result":"not-run","exception_verdict_id":null,"exception_authority":null,"artifact_id":null,"artifact_sha256":null,"status":"not-applicable","blocked_reason":"read-only-recon","next_principal":null}
```

Check: Given an evidence artifact ID and hash, when the worker files the release attest,
then `tightbeam attests <assignment>` shows the marker after the trigger verdict and
before the pass's later `tests-passed` or ready-for-review progress attest.

### A-09 — Review-round freshness and reviewer obligations

`feature-cycle` alone owns how each review round is commissioned, completed, and
followed by a fresh linked card. The base-synchronization skill neither restates nor
branches that lifecycle. It consumes the current round's linked review and verdict.
After `changes-requested`, the producer runs a gate with
`gate_id=rework:<that-attest-id>` before editing. The current-round reviewer checks:

1. The latest pass has one released gate whose trigger is the latest applicable
   `changes-requested` attest.
2. The evidence row has `kind=data`; its `createdBySession` equals the report's
   `worker_session` and the outcome attest's author; its bytes match the recorded
   SHA-256; the report satisfies the complete A-07 schema; and the attest outcome
   equals A-08's deterministic mapping.
3. The base-declaration attest exists, its author is an authorized declaring
   principal under A-02, and its note names the authority.
4. The report contains the A-03 observation command, full required revision, and
   successful result. For a moving ref, this is holder-recorded historical evidence,
   not an independently queryable historical-remote fact.
5. The reviewed commit contains the required revision.
6. The integration result and conflict evidence agree with repository history.
7. The selected tests follow repository policy and cover conflict paths.
8. An exception verdict, when present, has the authorized principal, exact scope, and
   current gate ID.
9. The released gate attest precedes the pass's later `tests-passed` and
   ready-for-review receipts. This ordering checks the durable claim sequence; it does
   not establish the first filesystem edit time.
10. A `review-target-red` outcome matches the triggering verdict's reviewed commit,
    safe command identity, and exit status in both the isolated `worker_head_before`
    and synchronized reproductions, with no additional failing command identity or
    changed target exit.
11. Every test entry has the six A-07 fields, `result` agrees with `exit`, and no test
    evidence contains stdout, stderr, a fingerprint, or a value derived from process
    output. The preflight entry has exactly its three fields, follows the bounded
    cleanliness predicate, and retains no status bytes or derived value beyond
    `clean` or `dirty`. Every other non-test source-control fact is one of the fields
    that A-07 explicitly enumerates, and no raw process stream is retained. A
    repository-required credentialed command is not omitted merely because it uses
    credentials.

The reviewer records missing, contradictory, or stale gate evidence as a blocking
finding. The reviewer does not repair the branch or evidence. A `reviewed-clean`
verdict cites the gate ID, artifact ID, artifact SHA-256, `worker_session`, required
revision, and reviewed commit.
When a `changes-requested` verdict makes a failing test the rework target, its note
identifies the reviewed commit, safe command identity, and exit status or cites one
immutable artifact that contains those three facts. Without that shape, a later gate
cannot classify the failure as `review-target-red`.

Check: Given feature-cycle supplies current review card Q2 after prior card Q1 closed,
when Q2 checks the reworked commit, then the gate evidence uses Q1's
`changes-requested` attest as its trigger. Given current required revision R and
reviewed commit C, when R is not an ancestor of C, then the reviewer files
`changes-requested` even when tests on C pass.

### A-10 — Stacks, release lines, worktrees, non-Git, and source-less tasks

- Stacked branch: use the immediate declared parent. Refresh that parent on each pass.
- Pinned release: use the exact pinned commit. Do not chase `main` or a newer release
  tip. A release branch without a pin remains moving.
- Multiple worktrees: resolve refs from the repository, integrate only in the worker's
  worktree, and treat uncommitted parent state as unavailable.
- Non-Git source control: apply the same state machine with the repository's immutable
  revision, update, ancestry or inclusion proof, deterministic worktree-status
  predicate, conflict detection, and test policy. The report retains only the fields
  in A-07's complete schema, not the underlying process streams.
- Source files without source control: the gate blocks by default. The work-item owner
  user can file `base-exception-approved` that identifies an immutable
  source snapshot artifact, its SHA-256, the integration procedure, and the gate ID.
  The note uses this exact shape:

  ```text
  SOURCE_BASE_EXCEPTION_V1 {"gate_id":"<gate-id>","snapshot_artifact_id":"<artifact-id>","snapshot_sha256":"<hex>","integration_procedure":"<exact-procedure>","principal":"user:<ownerUserId>"}
  ```

  The authorized declaring principal then files `base-declared` with `kind=non-git`,
  the snapshot source ID in `repo`, the SHA-256 in `pin`, and the exception attest
  ID in `authority`. The worker obtains the snapshot bytes, verifies the recorded
  SHA-256, and records `observation_kind=pinned-local`. The snapshot becomes the pinned
  base for this pass. The report uses `integration_method=snapshot-apply` when the exact
  authorized procedure changes the working source, or `none` when an inclusion proof
  establishes `already-current`.
- Source-less assignment: no base exists and the gate is not applicable. If the card's
  wording could be read as implementation, the holder files one progress attest with
  `BASE_SYNC_V1`, `status=not-applicable`, and the applicable A-08 source-less reason
  enum before the effect. Discovering source later starts a new gate.

A generic emergency, deadline, network outage, or credential outage does not authorize
an exception. The work-item owner user can change the product requirement, choose a
pinned source, or accept a proved base red; no principal can label unknown current
source as current.

Check: Given a directory of source files with no source control, when the work-item owner user
provides only "proceed anyway," then the gate stays blocked. When the owner instead
records an immutable snapshot artifact and `base-exception-approved` for the gate ID,
then the worker uses that snapshot as the pinned base.

### A-11 — Current source and provenance

The source baseline was verified against remote `main` at
`cd72fe0b06404afc6619a800c84a6a7eea595baa` on `2026-08-12T14:37:25Z`. The original
guidance read used `f5e4b25971c0037a2a17a8df4edf5f4e6e7e45cc`. The eight paths that
changed between those commits are `cli/src/args.rs`, `lib/tightbeam/assignments.ex`,
and six assignment/review tests or conformance fixtures. No Agentic Engineering
guidance, manifest, skill, neutral manual, artifact implementation, work-item
implementation, archetype composer, or packaging script changed. The current source
lines below therefore use `cd72fe0`.

| Current source | Lines | Existing authority or mechanism |
| --- | ---: | --- |
| `priv/kungfu/agentic-engineering/skills/worktree-session/SKILL.md` | 3, 11-40 | Triggers for repository work; owns worktree isolation, destructive-Git protection, current main reconciliation, tests, and cleanup. |
| `priv/kungfu/agentic-engineering/guidance/coder.md` | 13-17, 100-105, 107-149 | Reads authority first, pauses on conflicts, records tests and final verification, and triggers worktree reconciliation before build. |
| `priv/kungfu/agentic-engineering/guidance/orchestrator.md` | 28-54, 94-126 | Owns dispatch context, file declarations, review commissioning, and verification from rows. |
| `priv/kungfu/agentic-engineering/guidance/reviewer.md` | 12-19, 43-70, 78-88 | Reads source authority, reviews the integrated result, cites evidence gaps, and files the verdict. |
| `priv/kungfu/agentic-engineering/guidance/product-owner.md` | 3-5, 11-12, 35-64 | Owns product intent but not worker orchestration; quality floors are not theirs to waive. |
| `priv/kungfu/agentic-engineering/skills/feature-cycle/SKILL.md` | 40-52, 60-74, 101-113 | Defines implement, repeated review, final integration, and verification stages. |
| `priv/kungfu/agentic-engineering/skills/committing-and-pushing/SKILL.md` | 25-49 | Owns final branch-to-main semantic integration, tests after reconciliation, review freshness, and re-sync when main moves. |
| `priv/kungfu/agentic-engineering/skills/reviewing-code/SKILL.md` | 14-25, 34-60 | Owns detailed review evidence and verdict ceremony. |
| `priv/kungfu/agentic-engineering/archetypes/coder.toml` | 1-2 | Elects `worktree-session` and `committing-and-pushing` for coder sessions. |
| `priv/kungfu/agentic-engineering/archetypes/orchestrator.toml` | 1-16 | Projects the orchestrator kernel and elects `feature-cycle`. |
| `priv/kungfu/agentic-engineering/archetypes/reviewer.toml` | 1-18 | Projects the reviewer kernel and elects `reviewing-code`. |
| `priv/kungfu/agentic-engineering/archetypes/product-owner.toml`, `recon.toml`, `spec-writer.toml` | 1-19 | Complete the six-manifest projection set; each manifest supports shared guidance includes. |
| `priv/kungfu/agentic-engineering/guidance/engineering-tenets.md` | 17-24 | Requires stepwise evidence, failure reporting, ordered overlapping changes, and explicit handoffs. |
| `priv/kungfu/agentic-engineering/capabilities.md` | 15-17 | Already names Engineering law and worktree discipline as one adoption capability. |
| `priv/guidance/operating-manual.md` | 162-173 | Supplies neutral dirty-worktree custody and worker-owned worktree rules to each session. It does not declare an engineering integration base. |
| `priv/skills/tightbeam-guidance-authoring/SKILL.md` | 9-35 | Wisdom 15-22: directives, frequency-based homes, always-on detection, one concept per home, grounded terms, real mechanisms, verified sources, and batched edits. |
| `AGENTS.md` | 38-55, 77-86 | Repository test policy, baseline-before-change evidence, and the docs-only assembly gate. The TOML manifest edits make this batch non-docs-only. Adapter-seam changes additionally require live `feature_smoke` against both real harnesses, so gate evidence must support credentialed required tests. |
| `lib/tightbeam/assignments.ex` | 35-95, 371-376, 1207-1237, 1684-1703 | Assignment schema has no base field; attests carry ordered notes; producer-card arbitrary valid verdict kinds exist, while linked-review verdicts require their holder. |
| `lib/tightbeam/work_items.ex` | 35-52, 812 | Work items carry the durable `ownerUserId` used for owner-only rulings. |
| `lib/tightbeam/artifacts.ex` | 31-51, 70-125 | `data` artifacts record path, work item, creator, caller-supplied SHA-256, and observation-quality provenance without validating file bytes or satisfying the final `report`-artifact gate. |
| `lib/tightbeam/archetypes.ex` | 122-130, 168-174, 248-313 | `fragments/0`, `guidance/2`, and include resolution are the concrete pure composition seam for cold projection evidence. |
| `lib/tightbeam/identity.ex` | 372-401, 1053-1081 | `learn!/3` imports a shipped bundle; validation discovers `skills/*/SKILL.md` and rejects a manifest that elects a missing skill. |
| `lib/tightbeam/containment.ex` | 7-16, 24-29, 85-107 | Containment is not a security boundary, does not contain adapters, permits filesystem reads, and opens network egress. No existing launcher can prove a secret-free capture boundary; this spec therefore adds none. |
| `packaging/assemble.sh` | 34-45 | Builds and packages the runtime and CLI; it does not compose or verify archetype guidance. |
| `priv/kungfu/agentic-engineering/rules/verification.toml` | 20-35 | Final coder completion requires a `report` artifact. Base-gate evidence must use `data` so it does not satisfy this distinct requirement. |
| `cli/src/args.rs` | 386-390, 482-488 | The shipped CLI exposes artifact recording and progress/verdict attests. |

Provenance: commit `7608dd16c616f7ae189111024f4953250db03730`
(`2026-07-23T10:47:36-07:00`) first packaged the current three-line
`worktree-session` main-reconciliation rule. Commit
`c16e10483fbe8e83b4393a8b4126f7a27d14a12c`
(`2026-07-24T21:50:25-07:00`) restructured and renumbered the skill while retaining
that rule. Commit
`f425fcfdfa8e8ed7fcd8b01f3a181a0b61cdee4c`
(`2026-08-06T03:35:13Z`) refracted the worktree rule into the coder kernel. This spec
extends that live pattern; it does not mint a parallel name.

The cold digest also found an existing lifecycle contradiction: `feature-cycle` lines
72-74 requires one review card to receive verdicts until clean, while `reviewing-code`
lines 54-59 requires that card to complete after each verdict. The first review of this
spec produced the concrete case: `asg_0996df7b-f8ae-452a-a44a-8a56c1f1ab96` closed
after `changes-requested`. The A-12 `feature-cycle` refactor replaces impossible card
reuse with one fresh linked card per review round and retains reviewer completion;
A-09 only consumes that lifecycle for base-evidence freshness.

The amendment closes every blocking finding in
`att_c19d96cf-80db-4cb1-b340-f3387c961a9e`:

| Finding | Closure in this spec |
| --- | --- |
| B1 — canonical home | Metadata, A-13, and A-15 bind the artifact to the shared `specs/tightbeam` path; the superseded session-workdir file is not canonical. |
| B2 — taught-pattern discovery | I-10 and A-12 require one neutral operating-manual pointer in the same shipped batch. |
| B3 — impossible proof | I-01 and I-09 state that ordered attests are worker claims and observable consistency, not independent observation of edit time or a moving ref's historical remote tip. |
| B4 — inaccessible home | I-10 and A-13 place the short detector in shared guidance and the sole procedure in one shipped skill elected by all six Agentic Engineering manifests. |
| B5 — evidence/schema determinism | A-07 records preflight and integration commands, makes array order normative, makes object-key order and whitespace non-normative, and binds each artifact's own bytes by SHA-256. |
| B6 — source-less pass kind | A-07 restricts reports to `new` or `rework`; A-08 gives source-less classification an attest-only `source-less` value and no report. |
| B7 — declaration authority | Terms and A-02 derive opener identity from the assignment row and owner-user authority from durable `ownerUserId`; neither depends on an unavailable-opener ceremony or a prior owner ruling. |

The next amendment closes every finding in
`att_d2022b2b-369a-43d7-abe0-5f0cf7012ac6`:

| Finding | Closure in this spec |
| --- | --- |
| B1 — rework red deadlock | I-05, Terms, A-06, A-07, and A-09 keep `review-target-red` releasable when the triggering reviewed commit, safe command identity, and exit status reproduce on the pre-integration commit and synchronized baseline with no additional failing command. Later reviews deleted the stream and fingerprint comparison rather than reopening the deadlock. |
| B2 — evidence lifecycle | I-06 and A-07 delete outcome fields from the immutable pre-record report and add observation-only stop facts. A-08 makes the attest the sole outcome, defines a total report-to-outcome mapping, validates a cited artifact before honoring release, and defines append-only recovery for interruptions or ambiguous rows. |
| B3 — correction race | I-03 and A-02 bind the declaration at the observable attempt transition. Later corrections apply to the next attempt or pass; the spec deletes the unenforceable in-flight invalidation guarantee. |
| B4 — exception null type | A-06 types `overrides_policy` as a JSON string or JSON `null` and rejects the string `"null"`. |
| I5 — false provenance | A-11 replaces the unrelated `8a26bd3` attribution with full-history evidence from `7608dd16`, `c16e1048`, and `f425fcf`. |
| I6 — false projection check | A-11 and A-15 state that `packaging/assemble.sh` only packages. Direct `Archetypes.guidance/2` composition proves the detector projection; identity learning, skill-byte comparison, and manifest validation prove the elected skill projection. |

Check: Given the implementation starts from another source commit, when the implementer
opens the edit, then the implementer re-runs the source map. If a load-bearing clause
or mechanism changed, the implementer stops before editing and reports the exact
changed commit, paths, and lines to the orchestrator and canonical spec writer. The
implementer does not amend spec authority.

The next amendment closes every finding in
`att_118187c0-8c80-4839-a597-45008853d0e9`:

| Finding | Closure in this spec |
| --- | --- |
| F1 — dispatch contradiction | A-02, A-12, A-13, and A-15 add `orchestrator.md` to the batch and narrow atomic dispatch so source-changing cards can receive a declaration between assignment creation and wake. |
| F2 — artifact trust | I-06, the worker-session term, and A-07 through A-09 require `kind=data` and bind `createdBySession` to the attempt's worker, report, and outcome-attest author. Negative acceptance rejects a wrong-kind or foreign row. |
| F3 — every-attempt contradiction | I-06 now requires complete rows only for release. A-07 and A-08 require blocked or interrupted attempts to preserve the maximal bytes and rows that actually succeeded without fabricating absent evidence. |
| F4 — duplicated review lifecycle | I-10, A-09, and A-12 leave commissioning and completion only in `feature-cycle`; the base skill consumes the current round and owns only base-specific evidence. |
| F5 — note rail | The attest-note encoding term caps the canonical emitted line at 2,000 UTF-8 bytes, forbids truncation and implicit pointers, and defines one bounded non-authorizing fallback for every oversized required shape. A-08 replaces free-form outcome reasons with enums. |
| F6 — always-on depth | I-10 and A-12 through A-15 split a short detector from one elected on-demand skill across all six manifests. State, schema, exception, and recovery depth occur only in the skill. |

The next amendment closed every finding then known in
`att_4b47aa7a-e6a2-49d3-af74-6b36d05458f0`:

| Finding | Closure in this spec |
| --- | --- |
| F1 — nondeterministic sanitization | The then-current candidate used a deterministic literal sanitizer. The following review proved that mechanism unsafe for transformed secrets, so the next amendment deletes it. This row is provenance, not a live requirement. |
| F2 — unauthorized implementer amendment | A-11 and A-15 delete implementer amendment authority. A stale source map stops implementation and returns the evidence to the orchestrator and canonical spec writer. Only a spec-writer assignment may amend the canonical file; a new artifact/hash, fresh linked independent review, reviewed-clean verdict, and orchestrator re-pin are required before the implementer is woken to restart. |

The next amendment closed the sole finding then known in
`att_2bae131e-81de-4fe1-873c-ee4600c508d2`:

| Finding | Closure in this spec |
| --- | --- |
| F1 — transformed-secret leakage | The then-current candidate replaced literal redaction with a secret-free launcher precondition. The following review proved that precondition unbuilt and incompatible with credentialed required tests, so the next amendment deletes the entire stream/fingerprint surface. This row is provenance, not a live requirement. |

The next amendment closes the sole finding in
`att_3e912e95-825c-450f-8ce0-2d75e140165e`:

| Finding | Closure in this spec |
| --- | --- |
| F1 — credentialed-test deadlock | The Safe test evidence term, A-06 through A-09, and AC-42, AC-43, AC-47, and AC-56 delete persisted stdout/stderr, output encodings, fingerprints, reconstruction, capture authorities, and the secret-free-launch precondition. Repository-required credentialed commands run under A-06 without gate-owned stream capture. The gate retains only safe pre-expansion command identity, revision, non-secret environment qualifier, exit, `passed` or `failed` result, and classification. A-11 records the live credentialed-smoke rule and the absence of a security launcher. |

The next amendment closes the sole finding in
`att_230098c5-2a18-4e4c-9191-53220608b1c5`:

| Finding | Closure in this spec |
| --- | --- |
| F1 — contradictory preflight output contract | The Preflight cleanliness evidence term, A-04, A-07, A-09, AC-01, and AC-19 delete undefined “sanitized output.” Git uses one exact status command and maps exit plus stdout emptiness to the bounded `clean`, `dirty`, or `error` enum without retaining stream bytes. Worktree-status output yields only the `clean` or `dirty` evidence category; A-07 separately enumerates lawful non-test source-control facts without retaining their underlying streams. Non-Git policy must provide its deterministic predicate or the gate blocks. |

### A-12 — One-home and clause-preservation map

| Existing clause | Disposition | Required treatment |
| --- | --- | --- |
| New `guidance/base-synchronization.md` | Add | Begin with the unique top-level heading `# Base synchronization trigger`. Detect new implementation and review-rework passes, prohibit goal edits before release, identify opener/worker/reviewer trigger duties, and direct each actor to the elected `base-synchronization` skill. Include no state table, marker schema, exception, recovery, or review-card lifecycle. |
| New `skills/base-synchronization/SKILL.md` | Add | Own the gate vocabulary, A-01 through A-08 and A-10 procedure, base-specific A-09 evidence checks, exceptions, note-size behavior, and evidence shapes once. It does not own review-card commissioning or completion. |
| Each of six archetype TOML manifests | Refactor | Include `base-synchronization.md` after `engineering-tenets.md` and elect `base-synchronization` once. The skill remains on-demand depth rather than always-on prompt text. |
| `worktree-session` frontmatter line 3 | Retain | Keep the repository-work and worktree-isolation trigger. The always-on detector identifies new and rework passes and invokes the skill. |
| `worktree-session` lines 11-17 | Retain | Keep worker-owned durable worktree and repository-guidance reading. |
| `worktree-session` lines 18-23 | Retain | Keep declared files and overlap blocking. |
| `worktree-session` lines 24-34 | Retain | Keep destructive-Git refusal and dirty-tree ownership handling. |
| `worktree-session` lines 35-37 | Refactor | Remove the main-only procedure. Point pre-pass base synchronization to the always-on detector, which invokes the procedural skill. Keep worktree-specific integration boundaries here. |
| `worktree-session` lines 38-40 | Retain | Keep cleanup and completion evidence. |
| `coder.md` lines 13-17 | Retain | The detector supplies the event; the skill supplies the declaration requirement. Keep coder source-of-truth reading without a duplicate procedure. |
| `coder.md` lines 100-105 | Retain | Base/spec conflicts still pause instead of inviting a guess. |
| `coder.md` lines 107-130 | Retain | Final relevant tests, `tests-passed`, `report` artifact, and `verified` remain separate from the gate's `data` artifact. |
| `coder.md` lines 139-149 | Refactor | Keep completion order, worktree ownership, and cleanup. Replace the duplicate main-specific phrase with a pointer to the always-on gate. |
| `orchestrator.md` lines 28-39 | Refactor | Retain atomic `dispatch` for cards that need no fact between assignment creation and wake. Replace “exactly those cards” with the three two-step cases: file declarations, review links, and source-changing cards that require a pre-wake base declaration. Do not duplicate the declaration schema. |
| `orchestrator.md` lines 48-54 | Retain | Keep seam decomposition and file collision prevention. Base declaration does not replace files. |
| `orchestrator.md` lines 94-126 | Retain | The skill supplies gate verification. Preserve effect classification, review linkage, and final verification. |
| `reviewer.md` lines 12-19 | Retain | Keep independent reading of the source of truth. |
| `reviewer.md` lines 43-48 | Retain | The detector invokes the skill for A-09. Keep whole-result review without duplicating gate checks. |
| `reviewer.md` lines 58-70 | Retain | Missing gate evidence is an evidence-gap finding under the existing rule. |
| `reviewer.md` lines 78-88 | Retain | Keep verdict and wake lifecycle. |
| `product-owner.md` lines 3-5, 11-12, 35-64 | Retain unchanged | Keep product-intent rulings, the no-worker-orchestration boundary, and the rule that product owners do not waive quality floors. A product owner can resolve an incompatible product-intent conflict under A-05, but role ownership alone cannot declare a worker base or authorize A-06/A-10 exceptions. |
| `feature-cycle` lines 40-52 | Retain | The detector supplies the base-gate trigger. Keep coding lifecycle without a second gate statement. |
| `feature-cycle` lines 60-74 | Refactor | Solely own review-card lifecycle. Keep independence and replace same-card re-filing with one fresh linked card after each completed `changes-requested` round. The base skill consumes the resulting current round but does not repeat this rule. |
| `feature-cycle` lines 101-104 | Retain unchanged | Existing text owns final integration and post-integration review freshness. A-15 verifies that readers distinguish this event from the always-on pre-pass gate. |
| `feature-cycle` lines 105-113 | Retain | Final verification papertrail remains distinct. |
| `committing-and-pushing` lines 25-49 | Retain with boundary | Keep final main integration, semantic resolution, post-integration tests, and stale-review rule. State only that final integration is a different event from the always-on pre-pass gate. |
| `reviewing-code` lines 14-25 | Retain | The detector invokes the skill's A-09 checks. Keep whole-result review without a duplicate checklist. |
| `reviewing-code` lines 34-60 | Retain | Keep reproduction, citations, one verdict, wake, and completion. Fresh-round assignment custody resolves the former same-card contradiction. |
| `engineering-tenets` lines 17-24 | Retain unchanged | The gate instantiates these principles; it does not restate them. |
| Neutral `priv/guidance/operating-manual.md` lines 162-173 | Refactor | Retain universal worktree custody. Add one neutral pointer: an installed engineering bundle can require a pre-edit base gate, and its bundle guidance owns the procedure. |
| `AGENTS.md` lines 38-55, 77-86 | Retain unchanged | Repository policy supplies the Tightbeam test commands, docs-only gate, and credentialed live adapter smoke. The base gate records safe evidence for that smoke without capturing process output. |
| Agentic Engineering rules and rails | Retain unchanged | No current structured fact carries the declared ref, observed remote revision, integration result, pass trigger, and baseline-test outcome together. A rail would parse prose or infer judgment and create false positives. |
| `rules/verification.toml` lines 20-35 | Retain unchanged | Keep the final `report`-artifact requirement. The base gate records `data` and cannot satisfy it. |
| `capabilities.md` lines 15-17 | Retain unchanged | "Engineering law (worktree discipline...)" already names the adoption capability. A second capability name would drift. |
| Organization-local guidance | Excluded | Do not edit or mirror the shipped directive there. Learned identities receive the batch through the existing relearn/apply lifecycle. |

No existing shipped guidance requirement is deleted without replacement. The two
main-specific duplicate phrases move into the generalized canonical procedure. Final
integration clauses remain because they govern a different event. The prior unshipped
stream/fingerprint proposal is deleted rather than replaced.

Check: Given the proposed edit, when repository search finds `BASE_SYNC_V1`, then the
schema occurs only in `skills/base-synchronization/SKILL.md`. The always-on fragment
contains only detection and a skill pointer. `feature-cycle` alone defines fresh-card
lifecycle; the manual and worktree skill contain only boundary pointers.

### A-13 — Exact proposed edit files

The implementation edits this exact set in one batch:

1. Add `priv/kungfu/agentic-engineering/guidance/base-synchronization.md`.
2. Add `priv/kungfu/agentic-engineering/skills/base-synchronization/SKILL.md`.
3. Edit `priv/kungfu/agentic-engineering/archetypes/coder.toml`.
4. Edit `priv/kungfu/agentic-engineering/archetypes/orchestrator.toml`.
5. Edit `priv/kungfu/agentic-engineering/archetypes/product-owner.toml`.
6. Edit `priv/kungfu/agentic-engineering/archetypes/recon.toml`.
7. Edit `priv/kungfu/agentic-engineering/archetypes/reviewer.toml`.
8. Edit `priv/kungfu/agentic-engineering/archetypes/spec-writer.toml`.
9. Edit `priv/kungfu/agentic-engineering/skills/worktree-session/SKILL.md`.
10. Edit `priv/kungfu/agentic-engineering/guidance/coder.md`.
11. Edit `priv/kungfu/agentic-engineering/guidance/orchestrator.md`.
12. Edit `priv/kungfu/agentic-engineering/skills/committing-and-pushing/SKILL.md`.
13. Edit `priv/kungfu/agentic-engineering/skills/feature-cycle/SKILL.md`.
14. Edit `priv/guidance/operating-manual.md`.

The implementation does not add a rail or rule, edit source code or tests,
or edit `AGENTS.md`, `CLAUDE.md`, `capabilities.md`, `engineering-tenets.md`, identity
source, organization-local guidance, or a role kernel other than the listed `coder.md`
and `orchestrator.md` files.

Check: Given the implementation diff, when the reviewer lists changed paths, then the
set equals these fourteen paths.

### A-14 — Enforcement rung and deletion analysis

This change takes the guidance, on-demand skill, and independent-review rung. The short
always-on fragment detects the event for each projected archetype. The elected skill
owns procedural depth once. The manual supplies only pattern discovery,
`worktree-session` supplies only Git-worktree custody, and `feature-cycle` supplies
only review-card lifecycle.

A substrate rail loses for this release because the assignment row has no declared
base, the substrate does not observe authoritative remote state, and relevant-test
selection needs repository and human judgment. A rail would have to read prose or infer
currentness. That violates wisdom 1, 4, 6, 9, 20, and 21. A future rail requires
structured base-declaration, observation, integration, pass-trigger, and test-result
rows; this spec does not create them.

The evidence artifact uses `kind=data`. Using `kind=report` would make the existing
completion rule treat pre-edit gate evidence as the final verification report. That
false release would weaken an existing rail, so this spec keeps the two artifact
purposes distinct.

The subtraction choices are:

- Delete the branch/worktree surface: rejected because repository implementation and
  review-rework still require isolated source changes.
- Accept stale-base failure: rejected because existing source-control, artifact, attest,
  and review mechanisms can prevent it without new substrate state.
- Add one shared detector and one shared on-demand skill: selected because every
  archetype can act as opener, source worker, or reviewer, while rare exception and
  interruption ceremony must not inflate every always-on prompt. The six manifests
  already support both guidance includes and skill elections. This adds no product
  command.

The third changes-requested round re-derived each closure before adding surface:

| Finding | Smallest closure | Why delete or accept lost |
| --- | --- | --- |
| F1 | Delete `orchestrator.md`'s word `exactly` and name the existing two-step case. | Deleting pre-wake declaration defeats I-02; accepting contradiction makes dispatch nondeterministic. |
| F2 | Compare two artifact-row fields that already exist. | Deleting recovery reopens prior B2; accepting a foreign or `report` row creates false release. |
| F3 | Delete I-06's universal every-attempt claim. | No added recovery mechanism is needed; absent rows remain named failure. |
| F4 | Delete review-card lifecycle from the base skill. | `feature-cycle` already owns it; accepting duplication violates wisdom 18. |
| F5 | Delete free-form outcome reasons and add one bounded non-authorizing overflow marker. | Deleting declaration and exception detail destroys accountability; accepting truncation makes evidence false. The marker creates no release or new substrate state. |
| F6 | Relocate depth into one elected skill and keep only the detector always-on. | Deleting depth makes the gate unbuildable; accepting it always-on violates wisdom 16-17. |

The fourth changes-requested round re-derived the headline invariant before closing
the two findings:

| Finding | Smallest closure | Why delete or accept lost |
| --- | --- | --- |
| F1 | The then-current candidate added one byte-level literal sanitizer; the fifth round below supersedes and deletes it after transformed-secret leakage was demonstrated. | This historical choice retained exact fingerprints, but it failed the transformed-secret case and is not a live requirement. |
| F2 | Delete the implementer's authority to amend the spec and use the existing spec-writer plus linked-review handoff. | Adding an implementation-owned amendment lane duplicates `feature-cycle`. Accepting stale or unreviewed authority breaks the content-hash gate. |

The fifth changes-requested round deleted the defective sanitizer but selected a
secret-free precondition that the sixth round below supersedes:

| Finding | Smallest closure | Why delete or accept lost |
| --- | --- | --- |
| F1 | The then-current candidate deleted literal redaction, refused secret-bearing or unknown capture before process start, and retained byte framing for cited secret-free invocations. | That historical choice prevented transformed-secret persistence but required an unbuilt launcher and deadlocked credentialed required tests; it is not a live requirement. |

The sixth changes-requested round deletes the self-created capture surface:

| Finding | Smallest closure | Why add or accept lost |
| --- | --- | --- |
| F1 | Delete stdout/stderr persistence, encodings, fingerprints, reconstruction, capture authorities, and the secret-free-launch precondition; retain the safe command identity, revision, environment qualifier, exit, concise result, and classification. | Adding a credential-aware sandbox loses because current containment is not a security boundary and the fourteen-file guidance batch must not invent one. Accepting a permanently blocked credentialed smoke loses because repository policy requires that smoke. Accepting command-and-exit comparison without output identity is the smaller named limitation. |

The seventh changes-requested round deletes the residual undefined preflight surface:

| Finding | Smallest closure | Why add or accept lost |
| --- | --- | --- |
| F1 | Delete “sanitized output” and the blanket gate-wide output-derived-value ban. Retain one exact Git status command whose clean/dirty branch depends on stdout emptiness, the strict raw-stream and test-output-derived bans, and only the source-control facts that A-07 enumerates. | Adding a sanitizer or wrapper loses because neither exists and status paths need not persist. Deleting cleanliness proof loses I-04 and I-06. Accepting an undefined result makes release undecidable. |

Check: Given a proposal to add `base-synchronized` as an enforced rail fact during this
implementation, when the reviewer compares it with current source, then the reviewer
rejects it as unbuilt scope.

### A-15 — Rollout and implementation decomposition

The orchestrator orders the work because the fourteen files share one concept:

1. A guidance implementer rechecks remote `main`, repository guidance, the fourteen source
   files, and this spec hash. If current source invalidates a load-bearing A-11 or A-12
   claim, the implementer stops before editing, files the exact changed commit, paths,
   lines, and impact on its implementation assignment, and wakes the orchestrator.
   The orchestrator returns the evidence to the holder of this canonical spec-writer
   assignment, or opens one spec-writer amendment assignment if that custody is no
   longer live. Only that spec writer may amend the canonical file. The spec writer
   cold-digests and records a new spec artifact and SHA-256. The orchestrator opens one
   fresh linked independent spec review bound to that artifact/hash. Implementation
   remains blocked until `reviewed-clean`; then the orchestrator records the replacement
   artifact ID, SHA-256, and verdict on the implementation assignment and wakes the
   implementer to restart its pre-pass gate. The implementer never edits the spec or
   continues under the invalidated hash.
2. The implementer adds the short `base-synchronization.md` detector and the
   `base-synchronization` skill. The skill establishes the single procedural home for
   exact states, principal duties, exceptions, and evidence shapes.
3. The implementer includes the detector and elects the skill in each of the six
   archetype manifests. Cold projections must show the detector once and manifest
   inspection must show the skill elected once.
4. The implementer replaces the duplicate main-specific clauses in
   `worktree-session` and `coder.md` with boundary pointers, extends orchestrator's
   two-step dispatch cases to pre-wake base declaration, adds the distinct final-
   integration boundary to `committing-and-pushing`, replaces impossible same-card
   review reuse in `feature-cycle`, and adds the neutral manual pattern pointer.
5. Before editing, the implementer records the clean-tree baseline required by
   `AGENTS.md:50-53`. After editing, the implementer runs
   `mix format --check-formatted && scripts/verify_mix.sh` because the batch changes
   TOML manifests. The implementer runs `sh packaging/assemble.sh` as the repository's
   package-build smoke; that script does not validate guidance composition.
6. The implementer creates an isolated Tightbeam base directory inside the assignment
   workdir, runs `Tightbeam.Identity.init!/1` and
   `Tightbeam.Identity.learn!/3` for `agentic-engineering`, loads the learned manifests
   with `Tightbeam.Archetypes.load!/1`, and calls
   `Tightbeam.Archetypes.guidance/2` with
   `Tightbeam.Archetypes.fragments/0` for `coder`,
   `orchestrator`, `product-owner`, `recon`, `reviewer`, and `spec-writer`. The
   implementer writes each complete result and its SHA-256 under the assignment's
   evidence directory. Each result must contain the detector's unique top-level heading
   exactly once. The evidence records the six names, output paths, hashes, heading
   counts, elected skill list, and composer function. The implementer also reads the
   learned identity's `skills/base-synchronization/SKILL.md`, verifies byte equality
   with the shipped skill, records both SHA-256 values, and proves each loaded manifest
   elects that installed skill. Repository search separately proves one detailed
   procedure in the skill, one neutral manual pointer, review-card lifecycle only in
   `feature-cycle`, and no organization-local edit.
7. One independent policy reviewer checks this spec, the exact diff, the six direct
   composition outputs, the package-build result, the source-line preservation map,
   and the acceptance matrix. The producer
   resolves a `changes-requested` round, runs its fresh rework gate, and returns through
   the fresh linked review assignment that `feature-cycle` requires; the closed prior-
   round card remains immutable history. A-09 supplies only the base-evidence checks.
8. After `reviewed-clean`, the integration owner merges the shipped Kung Fu change by
   repository policy. Release and deployment remain separate authorized work.
9. After a build containing the merged Kung Fu is installed, the organization owner
   batches `tightbeam identity relearn` and `tightbeam identity apply` for selected
   sessions. The rollout records the identity revision before and after. No
   implementation assignment runs those live mutations implicitly.

The spec artifact remains at
`/Users/mike/shared-workspace/shared/specs/tightbeam/base-synchronization-gate.md`. The work item and review bind its exact
SHA-256. A material review amendment creates a new hash and invalidates the prior
handoff hash. Only a spec-writer assignment may make that amendment; implementation
cannot resume until the replacement hash has a linked `reviewed-clean` verdict and the
orchestrator records the replacement pin on the implementation assignment.

Check: Given the guidance and manifest edits are complete, when the applicable Elixir
gate, package-build smoke, any of the six direct composition checks, or the learned-
skill byte/election check fails, then the implementation is not ready for review and
no live identity mutation starts.

## Acceptance

The implementation and independent review execute this matrix. Each row names the
invariants and architecture clauses it verifies.

| ID | Given | When | Then | Trace |
| --- | --- | --- | --- | --- |
| AC-01 | New source-changing assignment; moving `origin/main`; Git preflight exits 0 with zero stdout bytes | Worker starts the first pass | Preflight records the exact command, exit 0, and `result=clean` without status output; opener declaration is bound; recorded fetch resolves a full commit; branch integrates; relevant tests pass; artifact and released attest claim release before later implementation receipts | I-01-I-06, A-01-A-08 |
| AC-02 | Latest review verdict is `changes-requested`; base advanced | Worker starts rework | New gate ID uses that verdict's attest ID; recorded fetch resolves the new commit; it is integrated and tested before later rework receipts | I-01, I-03, I-07, A-09 |
| AC-03 | Latest review verdict is `changes-requested`; base did not advance | Worker starts rework | A fresh gate still runs; ancestry proves already-current; pre/post head is equal; tests and evidence are new for this trigger | I-07, A-04, A-09 |
| AC-04 | Child branch is stacked on committed parent branch P | Child pass starts | Declaration names immediate parent P; worker obtains P's current committed tip; `main` is not substituted | I-02, A-02, A-10 |
| AC-05 | Assignment pins release commit R; `main` and release branch advance | Pass starts | Required revision remains R; report records pinned observation; no newer tip supersedes it | I-03, A-03, A-10 |
| AC-06 | Repository requires rebase; branch is worker-owned and unpublished | Worker integrates | Rebase is used; post-head contains required revision; tests and evidence use rewritten post-head | I-04, A-04 |
| AC-07 | Repository is silent on method | Worker integrates | Merge is used; no rebase occurs | I-04, A-04 |
| AC-08 | Repository permits rebase; branch is shared or published | Worker enters integration | Worker merges when policy permits merge; otherwise gate blocks for a ruling; worker does not rewrite shared history | I-04, A-04 |
| AC-09 | No assignment or repository base declaration exists | Worker enters gate | State is `blocked-base-declaration`; worker asks opener; no familiar default is inferred | I-02, A-02 |
| AC-10 | Moving remote base; network call fails; cached ref exists | Worker resolves base | State is `blocked-base-unavailable`; cached ref does not release gate | I-08, A-03 |
| AC-11 | Moving remote base; credential is rejected | Worker fetches | Failure category and next principal are recorded; goal edits do not start; no alternate remote is tried | I-08, A-03 |
| AC-12 | Declared ref is missing or deleted | Worker resolves base | Gate blocks and asks opener; `main` or another branch is not substituted | I-02, I-08, A-03 |
| AC-13 | Git reports textual conflicts | Worker resolves them | Report lists original conflict paths, resolution revisions, post-head, and rerun tests without retaining a raw source-control stream | I-04-I-06, A-05, A-07 |
| AC-14 | Base and assignment require incompatible behavior | Worker evaluates conflict | Gate records `blocked-conflict` with the assignment opener as next principal; opener obtains a canonical spec-writer or product-owner ruling; worker chooses neither side | I-08, A-05 |
| AC-15 | Baseline test fails only on synchronized worker branch and is not an exact declared review target | Worker classifies red | Failure is integration or worker-branch conflict; no baseline-red exception applies; gate stays blocked until resolved | I-05, A-05-A-06 |
| AC-16 | Baseline test fails on required commit and worker branch; no exception exists | Worker classifies red | Gate records `blocked-baseline-red`; goal edits do not start | I-05, I-08, A-06 |
| AC-17 | Work-item owner user accepts exact base-originated failures for current gate | Worker records exception | Release attest says `accepted-base-red`; report cites the verdict ID, keeps failing results visible, and releases only this gate | I-05-I-06, A-06-A-08 |
| AC-18 | Required Git commit is already an ancestor | Worker integrates | Canonical ancestry command exits 0; result is `already-current`; no empty commit exists; pre/post head matches | I-03-I-04, A-04 |
| AC-19 | Worker Git worktree contains another principal's uncommitted or untracked path; exact preflight exits 0 with one or more stdout bytes | Gate starts | Preflight records exit 0 and `result=dirty`, retains no status byte, path, count, encoding, or fingerprint, and maps the attempt to `blocked-worktree`; worker preserves files and asks the owner or opener | I-04, I-08, A-01, A-04, A-07 |
| AC-20 | Non-Git repository exposes immutable revisions and update policy | Pass starts | Report records the exact current revision and the update, inclusion-proof, conflict, and test command facts that A-07 and policy require; it retains no raw process stream; artifact and attest release the gate | I-01-I-09, A-03, A-07, A-10 |
| AC-21 | Source exists without source control; owner records immutable snapshot and exception; opener declares it | Pass starts | Declaration uses `kind=non-git`; snapshot SHA becomes the immutable base for the named gate; integration and tests still run | I-02-I-06, A-10 |
| AC-22 | Source exists without source control; no immutable snapshot exists | Pass starts | Gate blocks; a generic "proceed" instruction does not release it | I-02, I-08, A-10 |
| AC-23 | Assignment changes no source | Holder classifies task | Gate is not applicable; ambiguous implementation wording gets one N/A marker; discovering source enters a real gate | A-10 |
| AC-24 | Reviewer sees released gate before an older `changes-requested`, but none after it | Reviewer checks rework | Reviewer files blocking stale-evidence finding | I-07, I-09, A-09 |
| AC-25 | Reviewed commit does not contain recorded required revision | Reviewer checks ancestry | Reviewer files `changes-requested` even when current tests pass | I-09, A-09 |
| AC-26 | Moving base advances after gate release during active pass | Worker continues same pass | Released observation remains valid; next rework pass fetches again; no time threshold interrupts work | I-03, I-07, A-03, A-09 |
| AC-27 | Two attempts exist for one gate | Reviewer reads evidence | Each recorded artifact and outcome attest remains immutable; attempt numbers are sequential; only the latest valid released attest authorizes edits | I-06, A-01, A-07-A-08 |
| AC-28 | Artifact bytes change after recording | Reviewer hashes file | Hash mismatch is a blocking evidence finding | I-06, I-09, A-07, A-09 |
| AC-29 | Review card Q1 closes after `changes-requested`; producer completes a fresh rework gate | `feature-cycle` commissions the next review round | Its sole lifecycle rule creates fresh card Q2; the base skill only requires Q2 to check gate evidence triggered by Q1's verdict | I-07, I-10, A-09, A-12 |
| AC-30 | Final integration occurs after implementation review | Main or declared final target moves | Existing committing procedure re-integrates and re-proves; pre-pass gate is not treated as final-integration proof | I-10, A-12 |
| AC-31 | Proposed implementation adds a rail or structured base field | Reviewer checks scope | Reviewer rejects it as unrequested and unbuilt; fourteen-file detector, skill, guidance, and manifest set remains exact | I-10, A-13-A-14 |
| AC-32 | Exact fourteen-file set is edited | Implementer runs repository gates and direct composition | Clean-tree baseline and post-change `mix format --check-formatted && scripts/verify_mix.sh` are green; package smoke exits 0; `Archetypes.guidance/2` produces six named files and hashes with the detector heading once; all six manifests elect the skill once; `BASE_SYNC_V1` occurs only in that skill; feature-cycle alone owns review-card lifecycle; the manual has one pointer | I-10, A-11-A-15 |
| AC-33 | Existing clauses in A-12 are compared with the diff | Reviewer builds preservation table | Retained clauses remain; refactored clauses keep their original intent; no listed clause silently disappears | A-11-A-13 |
| AC-34 | Live identity has not been reprojection-batched | Shipped files merge | No live session is mutated implicitly; an authorized later rollout records relearn/apply revisions | I-10, A-15 |
| AC-35 | Orchestrator opens a source-changing assignment | Orchestrator hands off the work | The orchestrator uses the kernel's two-step case; row order is assignment, authorized `base-declared` verdict, then wake; the worker reads the declaration before entering `resolving-base` | I-02, A-01-A-02, A-12 |
| AC-36 | Work item records owner user U | U declares or corrects a base that does not contradict live repository policy | `base-declared` authority is `work-item:<id>:ownerUserId`; attest author equals U; worker and reviewer accept it without a prior ruling; a session that is neither the assignment opener nor U is rejected regardless of archetype | I-02, A-02, A-09 |
| AC-37 | Worker session W records a valid `data` artifact and released progress attest | Final verification rule evaluates the assignment | Artifact `createdBySession` is W; base evidence does not satisfy the required final `report` artifact, `tests-passed` receipt, or `verified` verdict | I-06, I-10, A-07-A-09, A-12-A-14 |
| AC-38 | Authorized base correction arrives after the current attempt's declaration-binding event | Current attempt has not released | Bound declaration continues to control the current attempt; correction controls the next attempt or pass; no claim of atomic in-flight invalidation is made | I-02-I-03, A-01-A-03 |
| AC-39 | Two writers serialize one valid report with different object-key order or whitespace | Reviewer parses and hashes each artifact | Both satisfy the field contract; each artifact is judged only against its own SHA-256; the spec does not require byte equality across writers | I-06, A-07 |
| AC-40 | Source-less implementation-looking assignment | Holder classifies it | Holder files the exact `pass_kind=source-less` N/A attest and no report artifact; report validation still accepts only `new` or `rework` | A-07-A-08, A-10 |
| AC-41 | Repository policy names no baseline command and no existing command that exercises the declared effect can be selected or started | Worker reaches synchronized-baseline testing | Gate records `blocked-test-unavailable`, names a concise non-secret cause category and the assignment opener, and does not release with an empty test set | I-05, I-08, A-01, A-06-A-08 |
| AC-42 | Triggering `changes-requested` identifies reviewed commit C, safe command identity T, and exit E; worker head is C; isolated C and synchronized baseline reproduce only T/E | Worker classifies rework red | Gate releases with `test_result=review-target-red`; report contains both command/revision/exit reproductions and no process output; only the post-release goal edit may repair the finding | I-01, I-05-I-07, A-05-A-09 |
| AC-43 | A rework synchronized run adds another failing command identity or changes the triggering T/E exit | Worker classifies rework red | `review-target-red` is refused; the gate classifies the remaining red under A-06 and blocks unless another lawful release condition applies; output comparison is not required or recorded | I-05, I-08, A-05-A-06 |
| AC-44 | One `kind=data` evidence row created by the current worker exists for an attempt but the process stopped before the outcome attest | Worker restarts | Worker rehashes and validates creator, kind, row, and report, then files exactly one derived outcome attest for the same attempt; it does not create another artifact | I-06, I-08, A-07-A-08 |
| AC-45 | Process stopped during artifact recording and restart finds no matching row | Worker recovers | Worker does not replay the call; it records `blocked-evidence` with null artifact fields when possible, preserves the local report, and starts a fresh numbered attempt | I-06, I-08, A-07-A-08 |
| AC-46 | Base-red exception overrides no repository policy | Owner user files the exception | `overrides_policy` is JSON `null`; the string `"null"` is invalid | I-05-I-06, A-06 |
| AC-47 | A credentialed test's safe command identity is T; it exits 1 after emitting arbitrary bytes, including transformed credential text and invalid UTF-8 | Worker records the failing test | The entry contains exactly command T, revision, non-secret environment qualifier, exit 1, `result=failed`, and classification; no stdout, stderr, encoding, fingerprint, capture authority, credential, or output-derived value enters gate evidence | I-05-I-06, A-06-A-09 |
| AC-48 | A released outcome cites a missing, mismatched, ambiguous, non-`data`, or foreign-session artifact row | Worker restarts or reviewer checks evidence | No cited attempt authorizes goal edits; the integrity failure is reported; a fresh numbered attempt must produce one unique worker-created `data` row | I-06, I-08-I-09, A-07-A-09 |
| AC-49 | A required marker's canonical encoded line is 2,000 UTF-8 bytes | Authorized actor files it | Tightbeam accepts the unsplit exact note; reviewer recomputes the same length and values | I-02, I-05-I-06, A-02, A-06-A-10 |
| AC-50 | A required marker's canonical encoded line is 2,001 UTF-8 bytes | Authorized actor prepares to file it | Actor does not call or truncate the oversized form; actor files the bounded `BASE_SYNC_NOTE_LIMIT_V1` form using verdict or progress authority; the original declaration, exception, or outcome does not take effect | I-02, I-05-I-06, I-08, A-02, A-06-A-10 |
| AC-51 | Artifact recording refuses after a blocked attempt's local report is written | Worker records maximal evidence | Local immutable report remains; null artifact fields or a refused attest are reported exactly; I-06 does not claim an absent row; the attempt cannot release | I-06, I-08, A-07-A-08 |
| AC-52 | Six assembled archetypes include the detector and elect the skill | Reviewer searches projected, learned, and source material | Each projection contains only one detector heading; learned and shipped skill bytes have the same SHA-256; all six loaded manifests elect it; all deep state/schema/exception/recovery clauses occur only in the skill; fresh-card lifecycle occurs only in `feature-cycle` | I-10, A-12-A-15 |
| AC-53 | Artifact row has correct path, SHA, work item, schema, gate, and attempt but `kind=report` or `createdBySession` differs from worker W | Recovery or review evaluates it | Evidence is `blocked-evidence`; it cannot release the gate or satisfy base evidence through another principal | I-06, I-09, A-07-A-09 |
| AC-54 | Worker W completed a valid released attempt; assignment custody later moves to X | X or a reviewer validates the old release | Artifact creator, report `worker_session`, and outcome-attest author all remain W, so the completed release remains valid; X does not adopt or rewrite it and uses a new attempt for later work | I-06, I-09, A-07-A-09 |
| AC-55 | Implementer rechecks current source and finds a load-bearing A-11 or A-12 claim stale | Implementer reports the difference | Implementer stops without editing the spec or product; a spec-writer assignment owns any amendment; a new artifact/hash receives one fresh linked independent review; only a reviewed-clean replacement pin recorded by the orchestrator permits a restarted implementation pass | I-06, I-09-I-10, A-11, A-15 |
| AC-56 | Repository policy requires live `feature_smoke` against two real harnesses and the authorized provider credentials work | Worker runs the synchronized baseline | Both credentialed commands start; each entry records its safe pre-expansion command identity, revision, harness qualifier, exit, concise result, and classification; no credential value or process output enters gate evidence; A-06 maps the exits to the release decision | I-05-I-06, A-01, A-06-A-09, A-11 |

Acceptance is `reviewed-clean` only when AC-01 through AC-56 are satisfied or marked
not applicable by their own Given condition with evidence. A reviewer cannot replace a
missing Given condition with an assumed scenario.

## Open Questions

None. The spec has no blocking or non-blocking holes. Future structured substrate
enforcement is a separate product decision, not an open question in this guidance
release.
