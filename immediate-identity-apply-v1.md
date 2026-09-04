# Immediate identity apply — v1

**Status:** Candidate for independent whole-contract exact-revision review.

**Work item:** `wi_ff222e95-ecd4-4ba0-83cc-ddd9e2301e07`

**Controlling correction:** Mike ruling
`att_9cbe6cbd-4ef1-42a8-81e1-deb8a8ac0379`, spirit verdict
`att_26f60256-752b-44fb-8c64-6ce60d86811a`, posture verdict
`att_38b6c8a4-c5c6-4eee-bd85-161e1e9a08d0`, product verdict
`att_350ad471-3e6a-459e-9149-40f85c61c913`, and ruled architecture
decision `dr_2932fbe0-cf86-46c9-8ae4-86aeea289119`.

**Amendment trace:** This candidate descends from reviewed commit
`8ed70006d913d60646eb6508a0d51ec58b342bc4`, whose canonical file SHA-256 is
`bf6f10d31b219353b6567dfe0405aed34a8e1d4525b4dde8296c2de9e7d37113`.
Coder evidence `att_6419ea77-c2ed-47c1-825b-990ac1990f5b` disproved that
candidate's `ContextProjectionV1` premise. Amendment surrender
`att_944e72db` exposed the rotating-credential conflict in generation-specific
harness homes. The ruled decision reopens that architecture and requires the
single-writer design below.

**Observed source bases:** Preserved Tightbeam `0.1.9` at
`91da03046eb8c48888ec486b2264f1618303298e` and preserved Tightbeam `main` at
`910cbde089762623b88d6c83d0445e333750a880` on 2026-09-04. Installed adapter
evidence is Codex ACP `1.1.4`, Claude Agent ACP `0.66.0`, and ACP TypeScript SDK
`1.4.0` on the same date.

**Authority and scope:** This specification replaces only the identity-apply
behavior in `served-identity-home-projection-v1.md` section 9 and
`relearn-and-identity-apply-workflow.md`. The identity Git publication model,
single-revision rendering, explicit administrator election, per-session
workdir, durable history, shared-runtime boundary, and relearn conflict behavior
remain authoritative. This specification supersedes revoked lazy-boundary
assignment `asg_63666748-d0cd-48f9-8142-9bc135d78698` and its commit
`975e66a616fb2af0c48209b9a419a9952c6ac7a8` in full. Apply does not wait for a
turn boundary and does not cancel a running turn.

## Goal

Make an explicit identity apply change every selected session's active identity
revision even when that session has a running turn. Preserve the running turn
on the immutable identity generation that it captured at admission. Make every
operation and turn admitted after the activation point observe the target
generation.

Make single-session and all-session apply converge without
`turn_in_progress`, without organization-wide quiescence, and without lazy
next-boundary application. Order concurrent applies, recover after crashes,
roll back only when rollback preserves later-operation truth, isolate partial
failure, and leave durable, redacted evidence on `0.1.9` and `main`.

## Non-Goals

- Relearn and identity edit do not apply a revision automatically.
- Apply does not cancel, replay, resume, or manufacture a model turn.
- Apply does not change the identity generation already captured by an admitted
  turn or another admitted operation.
- Apply does not restart a shared Codex runtime or another session.
- Apply does not change user, device, role, or administrator authority.
- Apply does not make an ancestor revision current. An intentional content
  rollback is a new descendant identity commit that reverts content, followed
  by a new apply operation.
- This specification does not change identity composition, credentials, host
  placement, or product-owned workdir files.
- This specification defines a product capability seam. It does not authorize
  an adapter workaround, live adapter replacement, install, or host change.

## Terms

- **Live revision:** The immutable Git object ID at `tightbeam/live`.
- **Active identity generation:** The one durable, monotonically ordered
  generation that a session advertises to operations admitted now. It names one
  revision, render contract, guidance digest, and immutable Tightbeam-owned
  generation payload. It does not require a second harness process or context.
- **Generation ordinal:** A session-local unsigned integer. Activation changes
  it only from N to N+1 in the same transaction that changes the active revision
  and stamps.
- **Identity binding:** The generation ID, ordinal, revision, render contract,
  guidance digest, projection root, native skill root, and history cursor
  captured by one operation or turn at admission. After realization, the turn
  row separately records the adapter session ID that serves that binding.
- **Projection root:** The immutable directory
  `<generation-store>/sha256/<first-two-generation-ID-characters>/<generation-ID>`.
  It contains `generation.json`, `guidance.utf8`, and one harness-native skills
  tree. It is generation material, not a session cwd or harness home.
- **Shared harness home:** The existing one home for one harness and machine:
  `CODEX_HOME` for Codex or `CLAUDE_CONFIG_DIR` for Claude. It contains the
  canonical rotating credential state. Apply never copies, versions, swaps, or
  links that state into another home.
- **Resident generation:** The generation realized by the logical session's
  current adapter session. It equals the active generation except while a
  prior-bound turn is running, while target realization is recovering, or while
  no adapter session is resident.
- **Target realization:** Starting or resuming one adapter session with the
  unchanged product cwd, an admitted work row's captured native skill root, and
  that binding's guidance after the prior adapter session is closed. It occurs before
  the first adapter request for that work and before the first prompt for a turn.
  It does not activate the generation; R-10 has already done that.
- **Prior-bound operation:** A turn or operation whose admission transaction
  captured the generation that was active before apply activation.
- **Later operation:** An operation whose admission transaction locks the
  session row after activation commits. Wall-clock invocation time is not the
  ordering fact; the session-row transaction is.
- **Adapter-dependent operation:** A later operation that must send an ACP
  request to the logical session's resident adapter session. Its binding is
  visible at admission, but its effect cannot run through a differently bound
  resident session.
- **Prepared generation:** A target generation whose complete identity
  snapshot, immutable payload, and recovery receipt exist, but which is not yet
  the session's active generation. Preparation creates no adapter session.
- **Activation point:** The one database transaction that compare-and-sets the
  expected active generation to the prepared target generation, updates all
  identity stamps, and records that the target is active. The resident adapter
  session remains separately identified.
- **Draining generation:** A former active generation retained only while a
  prior-bound operation can still read it or return a result from it.
- **Apply operation:** One durable administrator request with one frozen target
  revision and one frozen set of active session keys.
- **Apply target:** The durable per-session member of an apply operation.
- **Generation preparation effect:** A same-ID, status-readable operation that
  renders, validates, and publishes one immutable target payload without
  starting, changing, or stopping an adapter session.
- **Executor lease:** The durable per-target tuple of acting principal,
  executor owner ID, owner epoch, acquisition time, expiry time, and recovery
  ordinal that fences one preparation or recovery attempt. The effect-creation
  epoch is the owner epoch captured once when the effect ID is created; later
  lease adoption does not change it or the effect ID.
- **Request principal:** The authenticated administrator user or
  administrator-owned agent that accepted apply.
- **Acting principal:** The authenticated principal or `process:tightbeam`
  actor that performed a recorded transition.
- **Cause:** A closed machine-readable value that explains a transition or
  marker. Free text is not a cause.
- **Rollout alarm episode:** The durable interval during which at least one
  active session is stale against one live revision.

## Assumptions

1. Turn and operation admission can lock the session row and capture its active
   identity binding in the same transaction that admits work.
2. A TurnTask and each adapter call can carry the captured identity binding
   instead of rereading mutable session identity fields.
3. The turn ledger gives each accepted turn exactly one terminal state and at
   most one turn runs per session.
4. Durable build evidence can state whether the pinned Codex and Claude adapter
   versions implement the exact new/resume, guidance, additional-directory,
   close, and history behavior in R-03 and R-04. R-03 refuses the command before
   it creates an operation when the matching evidence is absent for any selected
   target.
5. One logical session runs at most one model turn. A target-bound turn cannot
   claim until a prior-bound turn has reached its one durable terminal state.
6. The existing adapter coordinator limits session load work to three
   concurrent load slots per host.
7. Both release lines can add logically equivalent additive SQLite storage
   without rewriting existing session, turn, transcript, assignment, or
   work-item rows.
8. The gateway resolves the authenticated caller to an administrator user or
   administrator-owned session before it invokes an identity effect.
9. The exact-version CLI and gateway ship together on both pre-1.0 lines.

## Invariants

**I-01 — Immediate active revision.** A running turn is not a precondition,
wait condition, or refusal. Once a target is prepared, activation can commit
while any prior-bound turn continues to run.

**I-02 — Prior work is immutable.** A prior-bound turn retains its captured
guidance, native skill root, revision, render stamps, adapter session ID,
workdir, and history cursor until its one terminal result. Apply does not
signal, cancel, rebind, close, or route that turn through the target generation.

**I-03 — Later work sees target.** After activation commits, every later
operation and turn captures the target binding. No later admission can capture
the draining generation.

**I-04 — One linearization point.** Preparation has no visible identity effect.
The activation transaction changes the generation ordinal, active revision,
render stamps, target result, and activation audit event together or changes
none of them. It does not change the resident adapter session of a running turn.

**I-05 — One revision per generation.** Guidance, skills, render contract,
digest, context configuration, and stamps for a generation come from one
immutable revision. A running turn cannot observe mixed generation bytes.

**I-06 — No privilege by identity swap.** Served identity content does not
grant user, device, role, or administrator authority. The gateway evaluates
those durable authorities independently. An apply cannot elevate its caller or
a prior-bound turn.

**I-07 — No downgrade.** Activation does not replace an active revision with
its Git ancestor or an unrelated revision. A stale executor cannot overwrite a
generation activated by a later operation.

**I-08 — Per-session isolation.** Apply changes only the selected session's
active identity generation and Tightbeam-owned generation material. It
preserves the session key, logical workdir, transcript, durable history,
assignments, work items, credentials, product-owned files, other sessions, and
the shared runtime process.

**I-09 — Bounded execution.** Preparation, catch-up, cleanup, and recovery use
the existing per-host load semaphore. At most three such effects run per host.
No database lock is held during adapter or filesystem I/O.

**I-10 — Crash truth.** Each preparation effect has one deterministic ID and
authoritative status. Lost responses cause status and payload reconciliation,
not a second payload or adapter session. Activation, realization ownership, and
rollback are database compare-and-set transactions with observable committed
truth.

**I-11 — Rollback preserves readers.** Automatic rollback to a prior generation
is allowed only when no operation or turn captured the target generation. If a
target-bound reader exists, recovery repairs the target generation and never
lies by repointing the session behind that reader.

**I-12 — Partial progress.** A failed or recovering target does not prevent
another selected target from preparing or activating.

**I-13 — Explicit human choice.** The substrate computes revision relations,
bindings, effect status, reader counts, results, and stale sets. Only an
administrator elects publish, apply, a new apply after terminal failure, or a
content rollback.

**I-14 — Accountable evidence.** Every operation, target transition, refusal,
recovery observation, generation activation, rollback, cleanup, and alarm
marker records a cause, request principal, and acting principal. Evidence
contains no identity content, transcript content, raw adapter envelope, stack
trace, credential, token, or secret-bearing environment value.

**I-15 — One rotating-credential authority.** The existing shared harness
runtime and shared harness home remain the sole rotation authority for Codex or
Claude subscription credentials on a machine. Apply workers and generation
storage never write a credential. Apply does not create a generation home,
credential copy, credential symlink, credential broker, or second shared
adapter runtime. Generation selection uses only ordinary per-session inputs and
ordinary vendor-child lifecycle inside that existing runtime.

## Architecture

### Source defect and elected mechanism

The durable incident is work item
`wi_ff222e95-ecd4-4ba0-83cc-ddd9e2301e07`: 258 of 327 active sessions were
stale, including 250 on revision `3a8f3bc9a4dea76d1e7d0ea73df42af0dbdd95f3`
and eight with no revision, while live was
`2e12888fecaf6e34b2a1fbdb259bb8afa60c08f8`. Attest
`att_864fed42-a14e-43b0-94f4-5df4f0038ecf` records all-session and
single-session `turn_in_progress` refusals. Attest
`att_c65de4bc-1925-4804-a657-da41c3c64726` records the stale holder's
zero-effect effort request refusing both actions for lack of a liveness trigger.

On both observed source bases, `identity_apply_sessions` performs a
whole-selection running check, then `identity_apply_at_lane` synchronously asks
`SessionLane.at_turn_boundary/2`. The relevant observed locations are
`lib/tightbeam/gateway.ex:4198-4306` on main and
`lib/tightbeam/gateway.ex:3094-3202` on `0.1.9`.

The elected mechanism is multi-version identity data inside the existing
single-writer runtime topology. A running turn owns a prior binding. Apply
prepares an immutable target payload beside it and atomically makes that payload
active for later admissions. It does not prepare a second adapter context. The
old adapter session stays resident until its one turn terminals. The shared
adapter then closes that session and realizes the durable active binding before
the next prompt. Apply never edits identity bytes in place beneath a running
turn and never waits for that turn to activate.

### Requirements

**R-01 — Command forms and immediate execution.** Both lines shall accept:

```text
tightbeam identity apply (<session> | --all) [--key <idempotency-key>]
tightbeam identity apply --operation <operation-id>
```

The effect form shall commit R-03 before execution. A supervised executor that
is independent of the request shall begin each target without waiting for a
turn boundary. The command may return a completed result if all targets
terminalize while connected. If the connection ends first, the operation
continues and the command shall return or recover this durable shape:

```json
{
  "state": "running",
  "outcome": null,
  "operationId": "iap_<id>",
  "identityRevision": "<target-oid>",
  "selector": {"kind": "all", "sessionKey": null},
  "requestedBy": "session:agent:product-owner:example",
  "applied": [],
  "pending": ["agent:coder:one"],
  "failed": []
}
```

`applied` and `identityRevision` retain their existing names and types.
`--operation` is read-only and mutually exclusive with a selector and `--key`.
The CLI help states that apply preserves a running turn on its captured
generation and makes the target generation active for later operations.

**R-02 — Idempotency.** `--key` shall bind request principal, verb, key, and
canonical selector in one unique transaction. The canonical selector is exactly
`{"kind":"all","sessionKey":null}` or
`{"kind":"session","sessionKey":"<exact-key>"}`. The winning transaction
captures the target revision. Repeating the same binding returns the same
operation. Another selector returns `idempotency_conflict` and the remedy `Use
a new --key for the different selector.` An unkeyed request receives a generated
key and durable operation ID.

**R-03 — Atomic acceptance.** One transaction shall authenticate R-16, capture
the live revision, freeze active selected sessions, lock their rows in ascending
session-key order, and read each selected session's durable adapter capability
metadata. That metadata shall be derived from the running build manifest and
the adapter package identity verified when the shared adapter process starts;
session or identity content cannot supply it. Every selected adapter shall
declare all of these exact values:

```json
{
  "generationInput": "native-additional-directory-v1",
  "historyCatchUp": "durable-before-first-prompt-v1",
  "sessionClose": "acp-session-close-v1",
  "sharedCredentialHome": "single-writer-v1"
}
```

Codex shall additionally declare
`"guidanceInput":"acp-meta-developer-instructions-v1"`; Claude shall declare
`"guidanceInput":"acp-meta-system-prompt-append-v1"`. A declaration is valid
only for the package version and package-content digest recorded by the
release-blocking A-21 adapter capture. If any declaration or matching capture is
absent, the transaction returns `generation_isolation_unsupported`, names the
first session in sorted order, and creates no operation, target, generation,
payload, adapter session, or idempotency binding. Otherwise it creates the
operation and targets, recording each target's expected active generation and
prior revision. A missing or different value is an absent capability. The
transaction commits before any preparation I/O.

A one-session selector that is absent or retired returns `not_found` with the
remedy `Run tightbeam identity status and select an active session.` For
`--all`, a session retired before its row lock is excluded. A session created
after acceptance is not selected. No running-turn query occurs in acceptance.

**R-04 — Immutable generation store and native realization.** A generation
shall live at its projection root in a content-addressed Tightbeam-owned store
outside the product-owned workdir. `generation.json` shall be exactly one RFC
8785 JSON object with these members and JSON types:

```json
{
  "archetype": "string",
  "guidanceSha256": "64 lowercase hexadecimal characters",
  "harness": "codex or claude",
  "renderContract": "string",
  "revision": "40 lowercase hexadecimal characters",
  "schema": "tightbeam.identity-generation.v1",
  "sessionKey": "string",
  "skills": [{"path": "string", "sha256": "64 lowercase hexadecimal characters"}]
}
```

`archetype`, `renderContract`, and `sessionKey` shall be nonempty valid Unicode
scalar sequences in NFC; the renderer shall reject rather than normalize any
non-NFC value. `harness` shall be exactly `codex` or `claude`; `schema` shall be
exactly `tightbeam.identity-generation.v1`. A skill `path` shall be the NFC
POSIX relative path from the harness's native skills directory to one regular
Tightbeam-owned file. It shall
start with `tightbeam__`, use `/`, contain no empty, `.` or `..` segment, contain
no NUL, and be unique. `skills` shall contain every regular file in the elected
Tightbeam-owned skill trees and shall be sorted by ascending unsigned UTF-8
bytes of `path`. Each skill digest covers its exact stored bytes. The guidance
digest covers the exact bytes stored in `guidance.utf8`. No layer normalizes
line endings for this metadata operation: a CRLF/LF or terminal-newline change
changes the covered byte digest.

RFC 8785 determines object-member order, escaping, and scalar encoding. The
hash input is exactly the UTF-8 RFC 8785 serialization of this object: no BOM,
prefix, length field, delimiter, or trailing newline. The lowercase SHA-256 of
those bytes is the generation ID. The identical bytes shall be stored as
`generation.json`. `guidance.utf8` shall be valid UTF-8 and shall store the
complete rendered guidance bytes. A Codex generation shall store each listed
skill at `P/.codex/skills/<path>`. A Claude generation shall store each listed
skill at `P/.claude/skills/<path>`. A generation shall contain neither the
other harness's native directory nor `.agents/skills`. It shall contain no
credential, token, auth configuration, vendor settings, transcript, or product
file. Publication shall write and fsync a temporary sibling tree, set
directories to mode `0555` and regular files to `0444`, fsync the parent, and
use an atomic no-replace rename. A published generation object and every file
below it are immutable. Tightbeam shall validate file type, mode, size, path,
and digest before each realization and shall fail closed on a mismatch.
Every walk shall use `lstat`. It shall reject a symlink, a non-directory parent,
a non-regular leaf, a regular file whose link count is not one, an unlisted
leaf, a missing listed leaf, and a resolved store or temporary path that escapes
the configured generation store. The only allowed entries are
`generation.json`, `guidance.utf8`, the selected harness's native parent
directories, and the listed skill files.

For a logical session with product workdir `C` and captured projection root
`P`, target realization shall use the existing shared adapter process and
shared harness home. The bridge shall send these exact inputs:

| Input | Codex ACP 1.1.4 behavior required by this contract | Claude Agent ACP 0.66.0 behavior required by this contract |
| --- | --- | --- |
| cwd | `session/resume.cwd = C`, or `session/new.cwd = C` when no vendor session exists | `session/resume.cwd = C`, or `session/new.cwd = C` when no vendor session exists |
| generation root | Replace the prior generation root with `P` in `additionalDirectories`; retain every pre-existing non-generation product root in its prior order | Replace the prior generation root with `P` in `additionalDirectories`; retain every pre-existing non-generation product root in its prior order |
| guidance | Decode `P/guidance.utf8` without normalization and send it as `_meta.developerInstructions` on `session/resume` or `session/new` | Decode `P/guidance.utf8` without normalization and send it as `_meta.systemPrompt.append` on the locked `claude_code` preset for `session/resume` or `session/new` |
| native skills | Adapter discovery from `P/.codex/skills/tightbeam__*` | SDK discovery from `P/.claude/skills/tightbeam__*` |
| close | ACP `session/close` after the resident turn terminals and before target realization | ACP `session/close` after the resident turn terminals and before target realization |
| harness home | The one unchanged machine `CODEX_HOME` | The one unchanged machine `CLAUDE_CONFIG_DIR` |

`session/load` is not target realization. Codex ACP `1.1.4` does not forward
`developerInstructions` on that path. The bridge shall use `session/resume` or
`session/new` as specified above. Claude shall retain `settingSources` containing
`project`. The adapter shall receive `C`, byte-for-byte, as cwd; it shall never
receive `P` as cwd. Identity apply shall not create a harness process, change a
harness-home environment value, or touch a credential path.

Before a generation-ready session opens, R-21 shall prove that `C` and every
non-generation additional directory contain no Tightbeam-owned reserved child
under `.codex/skills/tightbeam__*` or `.claude/skills/tightbeam__*`. Target
preparation repeats that collision check. A collision fails with
`generation_prepare_failed`; the adapter does not select one copy by search
order. Product-owned non-prefixed skills, product guidance, vendor-native
skills, and every product path remain at their existing backing paths. Identity
apply creates, renames, writes, and deletes no byte below `C`.

Activation does not send `P` to an adapter and does not start, resume, close, or
reload a session. While an A turn runs, the adapter session retains C, P-A, and
A guidance even after B activates. After that turn terminals, R-11 closes A.
Only a later target-bound turn sends C, P-B, and B guidance to a new or resumed
adapter session. Another Tightbeam logical session may concurrently realize its
own root through the same adapter process; the release-blocking adapter capture
shall prove that native discovery and prompt-time skill resolution do not bleed
between those sessions. This isolation is the served-identity correctness
boundary. It does not grant a new filesystem authorization against an already
authorized process that deliberately opens an absolute store path.

**R-05 — Admission binding and visibility.** Turn claim and every session-scoped
operation admission shall lock the session row and copy the complete active
identity binding into its durable work row or request context before releasing
the lock. Adapter calls shall use that captured binding. They shall not reread
the session's active identity fields.

Activation and admission therefore have two legal orders. Admission-first is
prior-bound and remains so through completion. Activation-first is
target-bound. A queued turn has no binding until claim and is target-bound when
claimed after activation. A tool operation issued after activation from a
prior-bound model turn is a later operation: it observes the target session
binding and resolves Tightbeam-owned identity reads from that immutable payload,
but it retains its authenticated session principal. R-16 governs its authority.

A later operation that needs no adapter request executes from its captured
binding immediately. An adapter-dependent later operation records that binding
and enters `realization_pending` when the resident generation differs. It shall
not route through the prior resident session. The session realization lane runs
it after the prior turn terminals and its captured generation is realized under
R-11. Its admission and B visibility are immediate even when its adapter effect
must remain pending behind A. Apply activation never waits for that effect.

**R-06 — Per-target state machine.** Each target shall have exactly these
states:

```text
pending -> preparing -> prepared -> activating -> active_verifying -> succeeded
              |            |            |              |
              +-> failed    +-> failed  +-> failed      +-> rollback_pending -> failed
                                                       +-> recovery_required
pending | preparing | prepared | activating -> superseded
recovery_required -> activating | active_verifying | rollback_pending | succeeded | failed
```

`succeeded`, `failed`, and `superseded` are terminal. A transition uses a
compare-and-set on the target owner epoch. The operation has `state: "running"`
and `outcome: null` while any target is nonterminal. It has
`state: "completed"` and outcome `succeeded`, `partial`, or `failed` from its
terminal targets. An empty `--all` selection succeeds.

**R-07 — Preparation effect.** Under one host load slot, the executor shall
render and validate the target generation and publish its immutable object
without calling the adapter or changing the resident adapter session or current
session row. The seam is:

```text
prepare_identity_generation(effectId, ownerEpoch, priorBinding, targetGeneration)
prepare_identity_generation_status(effectId, ownerEpoch)
```

The effect ID is lowercase SHA-256 of UTF-8 operation ID, one NUL byte, UTF-8
session key, one NUL byte, ASCII effect-creation epoch, one NUL byte, and ASCII
`prepare-identity-generation`. The effect-creation epoch is stored before the
first call and never changes. Lease adoption changes `ownerEpoch` but not the
effect ID. Operation ID and session key shall contain no NUL. The epoch shall
be unsigned base-10 ASCII with no leading zero except the value `0`. Calls with
one ID coalesce to one logical preparation.

Status returns only `not_started`, `in_progress`,
`prepared(targetGenerationId,projectionRootHash,validated=true)`, or
`failed(safeCode)`. `prepared` proves that the complete immutable payload exists,
its canonical metadata recomputes the target generation ID, every listed file
recomputes its stored digest, the native root has no reserved-name collision,
and the R-03 build evidence matches the running adapter package. It also proves
that preparation made no adapter request and left the prior adapter session
unchanged. Preparation performs no session-row or resident-generation update.

**R-08 — Preparation recovery.** Each target shall durably store
`leaseOwnerPrincipal`, `leaseOwnerId`, `ownerEpoch`, `leaseAcquiredAtMs`,
`leaseExpiresAtMs`, `effectCreatedEpoch`, `recoveryOrdinal`, `nextAttemptAtMs`,
`callDeadlineAtMs`, and `lastObservationCode`. `ownerEpoch` and
`recoveryOrdinal` begin at zero; the other fields begin `NULL`. Every time this
requirement says database time, the write transaction shall obtain one integer
millisecond value from its SQLite connection with:

```sql
SELECT CAST(strftime('%s','now') AS INTEGER) * 1000
       + CAST(substr(strftime('%f','now'), 4, 3) AS INTEGER)
```

Tests shall replace that database clock, not the process clock.

An executor may acquire an unowned target, or adopt one whose
`leaseExpiresAtMs <= databaseNowMs`, only when `nextAttemptAtMs` is `NULL` or
`nextAttemptAtMs <= databaseNowMs`. One transaction shall lock the target,
increment `ownerEpoch`, set the authenticated acting principal as lease owner,
and compare-and-set the prior owner epoch. An executor owner ID shall be 32
lowercase hexadecimal characters made from 16 operating-system CSPRNG bytes
once at supervisor process start. The transaction shall set `leaseOwnerId` to
that ID, set `leaseAcquiredAtMs` to database now, and set `leaseExpiresAtMs` to
database now plus 45,000 ms. Tests inject the executor owner ID. The first such
transaction shall also set immutable `effectCreatedEpoch = ownerEpoch` and
persist the R-07 effect ID.
Later adoption preserves both fields. An unexpired lease cannot be transferred.

Only an executor holding the exact stored principal, executor owner ID, and
owner epoch may start an R-07 call or consume its return. Immediately before a
call, one transaction shall recheck that ownership. It shall require database
now before lease expiry and at or after `nextAttemptAtMs` when present, set
`callDeadlineAtMs` to database now
plus 30,000 ms, and extend `leaseExpiresAtMs` to at least database now plus
45,000 ms. It then releases the database lock before I/O. Return consumption
shall lock the target and require the same principal and epoch, database now no
later than `callDeadlineAtMs`, and database now before `leaseExpiresAtMs`.
Failure of any check discards that return without a target transition. A call
already in flight when its lease expires may finish, but its same-ID effect and
content-addressed publication coalesce and its stale owner cannot consume the
return, activate, roll back, or clean up.

During `preparing`, return consumption and timeout observation shall each
compare-and-set target state `preparing`, the complete owner tuple, and the
stored call deadline. The first transaction to commit at the deadline controls;
the loser rereads durable state and performs no write.

The first owner invokes R-07. An adopter or a recovering owner queries status
before any invoke. `not_started` authorizes the same owner, under the same
lease checks, to invoke the same effect ID. `in_progress`, timeout,
unavailability, or an invalid receipt authorizes another status call only. For
each such retryable observation, the consumption transaction captures
`observedAtMs = databaseNowMs`, reads recovery ordinal `n`, sets:

```text
delayMs(0..3) = [5000, 10000, 20000, 40000][n]
delayMs(n >= 4) = 60000
nextAttemptAtMs = observedAtMs + delayMs(n)
recoveryOrdinal = n + 1
leaseOwnerPrincipal = NULL
leaseOwnerId = NULL
leaseExpiresAtMs = observedAtMs
```

The current owner may record a timeout observation only when database now is
at or after the stored `callDeadlineAtMs` and before lease expiry. That
transaction uses the same principal, executor owner ID, and epoch checks as
return consumption.

The scheduler shall not acquire or call before the stored
`nextAttemptAtMs`; a later scheduler wake uses the stored time and does not
re-anchor it. If an owner dies without recording an observation, the first
executor that adopts at lease expiry queries status immediately. Recovery never
creates a new effect ID. A late or stale return changes no durable state.

The executor shall not fall back to in-place cwd mutation, adapter invocation,
turn cancellation, or a boundary wait. A build-evidence mismatch, reserved-name
collision, payload-integrity failure, or runtime contradiction of the
capability declaration is `generation_prepare_failed`; it changes no active
binding and alarms the false capability declaration for operator repair.

**R-09 — Pre-activation validation.** After preparation, a short transaction
shall lock the session row and revalidate target ancestry, expected generation,
session incarnation, adapter generation, generation ID, projection-root hash,
and R-03 build evidence. A first incarnation or adapter-generation mismatch
discards the preparation receipt and returns the target to `pending` with cause
`session_generation_changed`. A second consecutive mismatch terminates as
`session_unstable` without activation.

If the session already has the same generation ID and revision, the target
records `succeeded` with cause `already_active` and no new ordinal. If a newer
descendant generation is active, the target becomes `superseded`. An ancestor
or unrelated target never activates.

**R-10 — Atomic activation.** The activation transaction is the only live
identity replacement. It shall compare-and-set the exact expected generation
and ordinal. It shall create ordinal N+1; make the prepared generation and
payload active; update revision, render contract, and guidance digest; preserve
the separate resident generation and adapter session ID; mark the former
generation draining when it has a reader or resident adapter session; record
target state `active_verifying`; persist the preparation receipt; and append
`identity_generation_activated` with the prior and target bindings. It commits
all fields together.

The transaction does not inspect or mutate the running turn. A running turn's
durable binding keeps the prior generation reachable. The command does not wait
for its terminal state. The new active generation is visible immediately after
commit. After commit, the executor shall read back the active binding and call
the status seam with the same effect ID. That call and receipt consumption use
the R-08 lease, owner tuple, database clock, and deadline. Exact matching active
fields plus a matching `prepared(...,validated=true)` receipt change
`active_verifying` to `succeeded` without another ordinal. A mismatch follows
R-12. Receipt consumption and timeout observation compare-and-set
`active_verifying`, the complete owner tuple, and the stored call deadline. A
retryable observation applies the R-08 next-attempt formula without changing
the active binding or `active_verifying` state.

If another apply activates descendant C after B's activation commit but before
B consumes its readback, the durable B activation event and exact prior/target
tuple prove that B did activate. B becomes `succeeded` with cause
`activated_then_superseded`; it does not restore B, advance another ordinal, or
change C. A readback mismatch without that exact committed lineage follows
R-12. Every rollback compare-and-sets B as the still-active generation.

**R-11 — Resident realization and history catch-up.** A prior-bound turn
shall keep its prior adapter session ID and immutable generation through
terminal publication. Its terminal callback shall record the result against
that binding and shall not overwrite the session's active generation or
resident generation. Only after that terminal transaction commits may the
coordinator send ACP `session/close` for that adapter session.

A turn claim or adapter-dependent operation shall capture the active binding and
enter `realization_pending` when the resident generation differs. It is an
admitted reader of that captured generation, but it is not runnable and sends
no adapter request. The session realization lane processes admitted work in
admission order. Under one host load slot, the coordinator shall validate that
work row's captured payload, wait only for an already admitted prior-bound turn
to terminal, close a different resident adapter session, and use R-04
`session/resume` or `session/new` inputs for the captured generation.

Before a turn prompt, realization shall advance `historyThroughSeq` through
every terminal transcript row that precedes the prompt, including a prior-bound
turn that ended after target preparation. One transaction then
compare-and-sets the same work binding, session incarnation, adapter generation,
and realization owner; records the returned adapter session ID and resident
generation; and makes that work runnable. A concurrent apply cannot retarget
admitted work. Adapter-independent work never enters this lane.

Before each close or realize call, a transaction shall persist
`realizationOwnerId`, `realizationOwnerEpoch`, `realizationState`, and the exact
resident and desired generation IDs. A stale owner cannot send a prompt or
consume a return. Realization uses the R-08 database clock, executor owner ID
format, 45,000 ms lease, 30,000 ms call deadline, owner-epoch adoption rule, and
retry schedule. Each call and return consumption compare-and-set the work ID,
captured generation ID, adapter-process incarnation, complete owner tuple,
state, and deadline. `closing`, `resuming`, and `catching_up` are recoverable.
An adapter-process incarnation change proves every prior in-memory adapter
session absent. With the same incarnation, a repeated close after a persisted
`closing` intent treats an adapter `session not found` result as already closed.
An uncertain resume return authorizes close of that same session ID and another
resume with the same captured inputs before any prompt. A no-vendor-session case
uses the existing crash-safe initial `session/new` path and the captured target
binding. These rules never start a second shared adapter process.

Identity activation itself has already completed and does not wait for
realization or catch-up. A close, resume, initial-start, or catch-up failure
leaves the target generation active and the work row `realization_pending`;
recovery retries the same captured generation. It records
`target_generation_recovery_required` on the work row and session without
changing a terminal apply target. No adapter-dependent effect or prompt can run
with a resident generation different from its work binding.

**R-12 — Rollback.** A failure before activation leaves the prior generation
active and may delete an unreferenced prepared generation. There is no visible
state to roll back.

If activation verification detects an invalid target payload or inconsistent
active fields after commit, one transaction may compare-and-set the active
binding back to the exact prior
binding only when the target generation has zero durable admitted readers and
the prior payload is proven valid. It records `rollback_pending`, then the
rollback transaction restores the prior stamps, advances the
generation ordinal again, records terminal `failed`, and emits
`identity_generation_rolled_back` with code
`activation_verification_failed`. The ordinal never moves backward.

If any operation or turn captured the target binding, automatic rollback is
forbidden. The target remains active and `recovery_required`; recovery repairs
the target payload by quarantining an invalid object and publishing only a
byte-equal object that recomputes the same generation ID. It never edits a
published file in place. It admits no new turn while the active payload is
invalid, but session-scoped status continues to report the target revision. A
realization failure occurs after work admission and therefore cannot trigger
rollback; R-11 recovery keeps the admitted work on its captured target. This
rule prevents a later operation from holding a generation that the session
falsely claims never became active.

**R-13 — Draining and cleanup.** Each admitted work row is a durable reference
to its generation. After the last prior-bound reader terminals, cleanup may
close only that resident adapter session by ACP `session/close`. It shall
remove the projection-root payload only after no resident adapter session,
nonterminal operation, turn, prepared generation, draining generation, active
generation, or rollback obligation references that generation ID. It shall
never remove or alter the logical workdir, shared harness home, credential,
non-prefixed skill, or another generation payload. Cleanup retains the
generation ID, canonical metadata
bytes and hash, revision, and audit fields; an audit reference does not require
guidance or skill payload bytes. Cleanup failure records a retryable event and
does not change the target revision, target result, transcript, product files,
or shared runtime. A generation referenced by a nonterminal operation, turn,
resident adapter session, draining generation, active generation, or rollback
obligation keeps its payload.

**R-14 — Concurrent apply ordering.** Apply operations do not use a fleet lock.
Preparation may run concurrently. Activation serializes on each session row and
expected generation compare-and-set.

If two operations target the same revision, the first activation wins and the
second records `already_active`. If target B and descendant C race from A, C may
activate first; B then records `target_superseded` and cannot downgrade C. If B
activates first, C may compare against B and activate C. An unrelated or
unreadable target records `identity_revision_unavailable`. A stale owner epoch
cannot prepare a new effect, activate, roll back, or clean up.

**R-15 — Result and partial failure.** The operation query shall return every
frozen target in ascending session-key order with state, prior and target
revision, prior and target generation ID, ordinals, effect ID, attempt count,
history cursor, safe error, timestamps, and whether a prior-bound turn is still
draining. It also reports the nullable resident generation ID and any current
realization state without changing the target's terminal result. `applied`
lists succeeded keys; `pending` lists nonterminal keys; `failed` lists failed
and superseded keys.

One target failure does not stop another. The same idempotency key never retries
a terminal target. After repair, a human starts a new apply with a new key.
Nonterminal recovery is automatic.

**R-16 — Authorization and causal visibility.** Effect and query forms require
the existing identity-administrator boundary. The gateway shall check authority
before reading an operation or writing an idempotency binding. Denial returns
`forbidden`, exposes no target existence, and writes only the ordinary denied
verb event.

User, device, administrator, assignment, role, and dispatch-rule authority do
not come from served guidance or skill bytes. Apply changes none of those rows.
A later operation from a prior-bound turn authenticates as the same durable
session principal and observes the target active identity in session status.
Its authorization is evaluated from current durable authority and compiled law,
never from either generation's prose. Its audit context records both
`causalTurnGenerationId` and `activeGenerationId`. Therefore identity apply
cannot grant an old turn a new administrator or role capability.

**R-17 — Revision races and intentional content rollback.** Acceptance freezes
one target revision. A later `tightbeam/live` publication does not retarget it.
Git ancestry is checked before preparation and again before activation. `NULL`,
equal, or ancestor recorded revisions may proceed. Target ancestors and
unrelated or unreadable revisions do not activate.

A success at B may remain stale against later live C. The alarm reports it and
an administrator may apply C. To undo content, an administrator publishes a
descendant commit that reverts the content and applies that new revision. Apply
does not point a session directly to an ancestor.

**R-18 — Audit and redaction.** Additive events shall record operation
acceptance, every target transition, preparation recovery, activation,
rollback, draining cleanup, operation completion, and the R-20 alarm lifecycle.
Each event stores operation ID when applicable, session key when applicable,
prior and target generation IDs and revisions, cause, request principal, acting
principal, executor owner ID, owner epoch, effect-creation epoch, lease
acquisition and expiry times, recovery ordinal, next-attempt time, and database
timestamp. Admission events additionally store the captured generation ID.
Generation events store only the generation ID, projection-root hash, harness,
native-root kind, adapter package identity, and adapter session ID when one is
realized; they do not store cwd contents, guidance, skill bytes, additional
directory values, harness-home paths, or environment values. Realization events
also record resident generation, desired generation, adapter-process
incarnation, realization owner ID and epoch, state, and safe result.

Only fixed R-19 codes, safe messages, and remedies persist. Unknown errors map
to `internal_apply_failure`. Raw thrown values, adapter messages, response
bodies, stdout, stderr, stack traces, identity bytes, transcript bytes,
credentials, tokens, cookies, authorization headers, and environment values are
neither interpolated nor persisted.

**R-19 — Named failures and remedies.** The first matching row controls a
command, target, or session-recovery result. Safe placeholders receive only
recorded identifiers.

| Code | Deterministic condition | Exact remedy |
| --- | --- | --- |
| `forbidden` | R-16 denies the caller. | `Ask an identity administrator to run this command.` |
| `not_found` | An authorized one-session target or operation query finds no visible active object. | `Run tightbeam identity status and select an active session or operation.` |
| `idempotency_conflict` | A principal reuses one key with another canonical selector. | `Use a new --key for the different selector.` |
| `target_superseded` | The target is an ancestor of the active revision. | `Run tightbeam identity status and start a new operation against the current live revision.` |
| `identity_revision_unavailable` | A required object is unreadable or revisions are unrelated. | `Repair the identity repository, run tightbeam identity status, then start a new operation.` |
| `session_retired` | Retirement commits before target activation. | `Run tightbeam identity status; no apply is required for the retired session.` |
| `session_unstable` | Incarnation or adapter generation changes twice during preparation. | `Stabilize the session adapter, then start a new operation with a new --key.` |
| `generation_isolation_unsupported` | Before operation acceptance, a selected harness lacks an exact R-03 declaration or matching real-adapter capture for native additional directories, generation guidance, session close, single-writer credential home, immutable generation preparation, or history catch-up. | `Install the reviewed matching Tightbeam release and adapter capability before retrying apply.` |
| `generation_prepare_failed` | Target generation rendering, validation, storage, build-evidence validation, or reserved-name collision check fails. | `Repair the named identity revision, matching build, or reserved Tightbeam skill path, then start a new operation.` |
| `activation_conflict` | Expected generation compare-and-set loses to a non-ancestry session mutation. | `Inspect the session and operation, then start a new apply against the current live revision.` |
| `activation_verification_failed` | Activation readback fails before any target-bound reader exists, and automatic rollback restores the prior generation. | `Repair the matching Tightbeam build or adapter, then start a new apply operation.` |
| `target_generation_recovery_required` | An activated target payload is invalid with target-bound readers, or a claimed target-bound turn cannot realize its captured generation. | `Restore the matching Tightbeam build or adapter and inspect this session; automatic target recovery will continue.` |
| `internal_apply_failure` | No earlier safe condition matches. | `Inspect this operation, repair the substrate fault, then start a new operation.` |

Preparation timeout, `in_progress`, cleanup retry, and database commit retry are
nonterminal apply observations. Their exact remedy is
`Inspect tightbeam identity apply --operation <operationId>; automatic recovery
continues. Restore the matching build or adapter if the state remains
unchanged.` Adapter unavailability during realization is nonterminal. Its exact
remedy is `Inspect tightbeam identity status for <sessionKey>; automatic
realization recovery continues. Restore the matching build or adapter if the
state remains unchanged.` Every refusal and terminal failure includes its
remedy.

**R-20 — Stale-version alarm and status.** At boot, after live publication,
after every activation, and every 60,000 ms, the substrate shall compute the
active stale-session set from durable active bindings and one live snapshot. It
shall not call a harness or mutate identity.

A nonempty set opens one alarm episode for that live revision and records one
normal-attention `identity_rollout_stale` notice to each distinct administrator
Main session. It includes live revision, stale count, missing-revision count,
active operation count, and these remedies: `Run tightbeam identity status.
Elect rollout with tightbeam identity apply --all.`

If the set remains nonempty 30 minutes after `firstObservedAt`, one transaction
records exactly one high-attention `identity_rollout_overdue` notice. It adds
pending, recovery-required, and terminal-failure counts plus affected operation
IDs. Its remedy is `Inspect tightbeam identity status and each reported
tightbeam identity apply --operation <operationId>; repair named failures or
elect a new rollout.`

When the set becomes empty, one transaction closes the episode and records
`identity_rollout_current`. Repeated scans and restarts do not duplicate these
markers. If no administrator session is addressable, the durable event still
commits.

`identity status` shall retain per-session stale reasons and add live revision,
stale count, missing-revision count, active operation IDs, target-state counts,
alarm episode ID, first-observed time, `generationReady`, active generation ID
and ordinal, nullable resident generation ID and adapter session ID, claimed
turn generation ID, realization state, and its safe recovery code. Doctor shall add
`identity-session-rollout`: `PASS` when current, `WARN` for an open episode, and
`INFO` when the non-mutating check cannot read the identity or session store.
This composes with the shipped-Kung-Fu staleness check from
`wi_61c28d6e-9a2b-4743-916b-a31fd47748e2`; neither check applies or relearns.

**R-21 — Migration, release parity, and package rollback.** Each line shall add
logically equivalent operation, target, identity-generation, durable binding,
resident-generation, realization-recovery, and alarm storage. The additive
schema migration rewrites no existing row and creates no apply operation,
notification, generation, adapter session, or identity mutation.

A separate reviewed readiness bridge shall mark one session
`generationReady=true` only while holding that idle session's admission lock.
It shall render the session's recorded active revision into an immutable
ordinal-zero payload, validate the exact R-03 adapter capture, close its idle
legacy adapter session, and remove only byte-verified Tightbeam-owned reserved
`tightbeam__*` children from the native skills directory below `C`. It shall
not change the cwd pathname `C`, the active revision, any product-owned or
non-prefixed byte, credential state, transcript, or durable history. It then
records no resident
adapter session and the ordinal-zero payload as active. A running turn remains
on the legacy path until its existing terminal callback; the bridge neither
waits inside an apply nor changes that turn. An existing running row without an
exact recorded legacy revision and render stamps uses the existing
failed-unknown recovery path before its session can become generation-ready.
Existing queued turns capture a binding only when claimed after readiness.

R-03 shall treat a selected session without `generationReady=true` as lacking
the R-03 capability and create no apply operation. This one-time readiness
bridge is package migration, not lazy apply: after the marker is set, every
apply activation follows R-10 immediately and no turn boundary gates it.

`0.1.9` and main shall implement the same state machine, wire fields, codes,
timers, load bound, audit fields, and fixture corpus. Line-specific module names
and migration numbers are not behavioral differences.

Disabling new apply admission shall not disable recovery, history catch-up, or
generation cleanup. Package rollback to code that does not understand durable
identity bindings shall be refused while a nonterminal apply, prepared payload,
active or draining generation, generation-bound turn, resident generation, or
realization obligation exists. The code is
`identity_generation_downgrade_blocked`; its remedy is `Restore the matching
Tightbeam build and resolve every active or draining identity generation before
retrying package rollback.`

After those conditions are absent, the reviewed downgrade bridge may collapse
each session's one active generation into the legacy direct projection while
holding that idle session's admission lock. It verifies byte-equal revision,
render contract, guidance digest, and Tightbeam-owned skills before it marks the
session legacy-compatible. The bridge does not change the active revision,
history, logical workdir, credentials, or product-owned files. It may write only
the verified Tightbeam-owned reserved skill children required by the legacy
projection. Old code may start only after every active session is
legacy-compatible. A schema rollback never drops operation, generation,
binding, alarm, realization, or audit evidence.

### Deterministic substrate and human-choice boundary

The substrate may authenticate, capture a revision, freeze keys, render and
hash a generation, prepare a payload, order activation, capture an admission
binding, reconcile an elected effect, count readers, close one resident adapter
session, realize one captured generation, clean a drained payload, compute
staleness, and emit evidence. These are facts and actions.

Only an administrator may publish identity, elect apply, select one or all
sessions, choose a new apply after terminal failure, publish a content-revert
commit, or repair a host. The substrate exposes facts and exact remedies. It
does not make these choices.

## Acceptance

**A-01 — Running self-apply (R-01, R-05, R-10, I-01 through I-03).** Given an
administrator-owned agent invokes `identity apply --all` inside its own held
turn on generation A, target B prepares and activates before the held turn is
released. The command does not return `turn_in_progress`, cancel, or wait for
the boundary. Status reports B active while the running turn row and adapter
call remain bound to A. A later admitted operation and the next turn bind B.

**A-02 — Running bystander and fleet progress (R-06 through R-10, R-15, I-09,
I-12).** Given
`--all` selects running, idle resident, queued-only, never-started, and
nonresident sessions, each target prepares and activates independently. A held
turn delays neither its own activation nor another target. One failed target
does not stop later targets. No target uses a global running-turn query.

**A-03 — Admission/activation race (R-05, R-10).** A deterministic barrier
releases one turn claim and activation in both session-row lock orders.
Claim-first binds prior A and finishes on A after B activates. Activation-first
binds B. No row contains a binding assembled from both generations.

**A-04 — Immutable skill and guidance isolation (R-04, R-07, R-13, I-02, I-05,
I-08).** Run
the deterministic bridge fixture once for Codex and once for Claude with one
logical workdir `C`, roots P-A and P-B, and another logical session with P-X in
the same shared adapter process. Hold an A turn and activate B. The apply path
makes no adapter call, creates no adapter session, and sends no P-B path. The A
turn reports cwd exactly `C`, receives exact A guidance, and invokes an A-only
native skill sentinel after activation. It observes A and not B. A later
Tightbeam operation captures B and reads B identity bytes directly from P-B.

Release A. Its terminal result commits before ACP `session/close`. Claim the
next turn, close A, and realize B with cwd C, P-B as the sole generation
additional directory, and exact B guidance. That turn observes the B-only
native skill and not A. During both phases, a prompt in the other logical
session observes X and neither A nor B. A and B each see the same product
sentinel and non-prefixed product skill at their unchanged backing paths. An
ordinary write-open to a generation skill fails read-only. Cleanup retains P-A
through A's terminal and close, then removes only unreferenced P-A. It never
changes a byte below C, P-B, P-X, the shared harness home, or a credential path.

**A-05 — Current-turn terminal publication (R-11).** Release an A turn after B
activation. Its terminal result commits once against the A binding and cannot
replace B's active stamps or resident generation. ACP close follows that commit.
Before the first B prompt, B's realized adapter session history cursor includes
that terminal row exactly once.

**A-06 — Authorization stability (R-16, I-06).** A fixture changes identity
prose and manifest bytes across A and B while holding user, device, role, and
compiled-law rows fixed. Apply grants and revokes no administrator or role
authority. A later tool operation from the held A turn records causal A and
active B, authenticates as the same session principal, and receives the same
decision as an equal principal outside apply.

**A-07 — Capability refusal and preparation failure (R-03, R-07 through R-09,
R-19).** Remove each required capability declaration from the first and last
sorted selected sessions. Each command returns
`generation_isolation_unsupported` with the exact remedy and creates no apply
material. Replace the running adapter package digest after acceptance, create a
reserved-name collision, and inject render, canonicalization, publication,
mode, and digest failures. Each preparation failure makes no adapter call,
changes no active generation, stamp, resident generation, running turn,
credential, or product file, returns `generation_prepare_failed` with the exact
remedy, and permits other accepted targets to continue.

**A-08 — Preparation crash recovery (R-08, I-10).** With database time starting
at 1,000,000 ms, owner P acquires epoch 1 with expiry 1,045,000 and immutable
effect-creation epoch 1. Stop the gateway at every boundary before and after
effect-ID persistence, invoke, and receipt persistence. At 1,044,999 another
owner cannot adopt. At 1,045,000 owner Q adopts epoch 2, preserves the exact
effect ID, and queries status before invoke. A return from P after adoption is
discarded; an already-started same-ID call may finish but creates at most one
logical prepared payload, and P cannot start another call or activate, roll
back, clean up, or commit a receipt.

For retryable observations committed at 2,000,000, 2,005,000, 2,015,000,
2,035,000, 2,075,000, and 2,135,000 ms, assert stored next-attempt times of
2,005,000, 2,015,000, 2,035,000, 2,075,000, 2,135,000, and 2,195,000 ms and
post-commit recovery ordinals 1 through 6. No process-clock change, restart, or
late wake changes those bytes. At one millisecond before each time no call is
eligible; at the stored time exactly one epoch winner may start status. Separate
fixtures prove the 30,000 ms call deadline and immediate status at lease-expiry
adoption when a crashed owner recorded no observation.

**A-09 — Atomic activation crash matrix (R-10, I-04).** Stop before and after
the activation transaction. Before commit, all active fields remain A and retry
may activate B. After commit, all active fields are B and recovery records
`active_verifying`, consumes the same prepared receipt, and records success
without another ordinal or adapter call. The resident generation and adapter
session ID remain A across both stops. No fixture observes a partial stamp,
state, or audit event.

**A-10 — Safe rollback with no readers (R-12, I-11).** Corrupt the target
payload immediately after activation and before any B admission. With prior
P-A proven valid, one rollback transaction advances the ordinal, restores all A
active fields, records failure and rollback evidence, and leaves the held A
turn and its resident adapter session untouched.

**A-11 — Rollback forbidden with a reader (R-12, I-11).** Admit one B operation
before injecting the same fault. Rollback does not run. B remains the advertised
revision, new turns are held while its payload is invalid, and automatic
recovery quarantines the invalid object and republishes only byte-equal P-B
whose metadata recomputes B. The B reader never refers to a generation the
session claims was not active and no published file is edited in place.

**A-12 — Concurrent applies (R-09, R-14, R-17, I-07).** Release same-revision B/B,
ancestor/descendant B/C, and unrelated B/X preparations in both activation
orders. Equal targets coalesce to `already_active`; C cannot be overwritten by
B; B followed by C reaches C; X never activates. With A held while B then C
activate, neither target creates an adapter session. A finishes on A and the
next turn realizes C without ever realizing B. A B-bound operation admitted
before C retains P-B through completion. Results and events use stable ordered
codes. If C commits before B consumes B's activation readback, B records
`activated_then_superseded` and no B recovery or rollback changes C.

**A-13 — Partial failure and durable query (R-01, R-02, R-15).** Three targets
succeed, fail before activation, and remain in preparation recovery. The first
two terminalize while the third remains pending. A lost response and repeated
key return the same operation. The query returns ordered applied, pending, and
failed arrays and performs no effect.

**A-14 — Retirement and mutation races.** Retirement before activation removes
the session and terminalizes the target as `session_retired`. Activation first
makes the target generation current before the existing retirement path runs.
Tune, repoint, and another session mutation serialize on the session row and
capture either the complete prior or target binding. None observes partial
activation or silently rewrites a captured generation.

**A-15 — Authorization and existence privacy (R-16, R-19).** A
nonadministrator receives `forbidden` for effect and query forms and creates no
operation, target, generation, payload, adapter session, or marker beyond the
denied-verb event.
Unknown and retired target keys share the authorized `not_found` shape.

**A-16 — Evidence and redaction (R-18, R-19, I-14).** Every operation,
transition, recovery observation, lease acquisition or adoption, activation,
rollback, cleanup, completion, and alarm carries cause, request principal, and
acting principal. Lease events also carry both epochs, database-clock lease
times, executor owner ID, recovery ordinal, and next-attempt time. Fixtures put
tokens in every raw adapter field and prove that output and durable rows contain
only fixed safe codes, messages, remedies, identifiers, hashes, ordinals, and
timestamps. Realization fixtures cover `closing`, `resuming`, `catching_up`,
stale owners, adapter-process replacement, uncertain resume return, and the
prompt gate. No fixture persists an additional-directory value, harness-home
path, environment value, adapter body, or identity byte.

**A-17 — Stale alarm lifecycle (R-20).** With a fake clock, one stale set opens
one normal episode and notice. Repeated boot and 60-second scans do not
duplicate it. At 29:59 no overdue marker exists. At 30:00 exactly one high
marker exists. Activating the last stale session closes the episode once. A
later live revision opens another episode. No scan calls a harness or applies.

**A-18 — Migration and downgrade refusal (R-21).** Copies of pre-feature
`0.1.9` and main databases migrate with existing row bytes and counts unchanged,
no generation rows, and empty apply stores. The readiness bridge refuses a
running session, then after its terminal creates one ordinal-zero payload,
closes the idle legacy adapter session, removes only byte-verified
Tightbeam-owned reserved skills, and sets `generationReady=true` without
changing product-owned bytes, cwd, credentials, revision, transcript, or
history. R-03 refuses a session before that marker. A package downgrade is
refused for every R-21 active condition and retains all evidence. The downgrade
bridge restores only verified legacy Tightbeam-owned reserved skills.

**A-19 — Cross-line conformance (R-04, R-21).** The same fixture corpus shall
run against exact `0.1.9` and main candidates. Canonical JSON for every state,
failure, visibility race, alarm, and final result is byte-equal after replacing
line-specific build and migration identifiers. Both lines shall serialize this
RFC 8785 generation fixture to exactly 418 UTF-8 bytes with no trailing newline:

```json
{"archetype":"coder","guidanceSha256":"0000000000000000000000000000000000000000000000000000000000000000","harness":"codex","renderContract":"served-identity-v1","revision":"1111111111111111111111111111111111111111","schema":"tightbeam.identity-generation.v1","sessionKey":"agent:coder:fixture","skills":[{"path":"tightbeam__alpha/SKILL.md","sha256":"2222222222222222222222222222222222222222222222222222222222222222"}]}
```

The lowercase SHA-256 of those exact bytes shall be
`1576938c11d748b9799516b2803ed9afaa7d2ddc95786cd9093cd26e16f8623b`.
Fixtures shall also reject non-NFC strings, backslash and dot-segment paths,
duplicate paths, wrong hash lengths, symlinks, multiply linked files, unlisted
leaves, missing leaves, and resolved-path escapes. Two input enumerations with
different skill order shall produce the same stored sorted bytes and generation
ID; a validator shall reject stored metadata whose `skills` array is not sorted.
CRLF and LF payload variants shall produce different covered digests and
generation IDs.

**A-20 — Prohibited mechanisms.** Source inspection shall find no identity
apply running-turn preflight, `turn_in_progress` result, apply-driven turn
cancellation, lazy next-boundary target activation, target adapter preparation,
in-place mutation of a generation used by a running turn, apply-time cwd write,
generation-specific harness home, credential copy, credential symlink,
credential broker, second rotating-credential writer, shared-runtime restart,
`session/load` target realization, or adapter fallback. Existing non-apply
cancellation and boundary mechanisms remain unchanged.

**A-21 — Real adapter contract capture (R-03, R-04, R-11, I-15).** On eezo or
racter, use a scratch `TIGHTBEAM_BASE_DIR`, fixture workdirs, and the exact
candidate packages. Run the A-04 sequence through real Codex ACP `1.1.4` and
Claude Agent ACP `0.66.0`; record each package-content digest and the exact
vendor CLI version. Use a deterministic local MCP gate to hold A. The sanitized
ACP capture shall prove the exact cwd, `additionalDirectories`, guidance meta,
`session/close`, `session/resume`, and prompt order. Native skill enumeration
and invocation shall prove A/B isolation and the concurrent P-X no-bleed case.

The process and filesystem ledger shall prove one unchanged shared `CODEX_HOME`
or `CLAUDE_CONFIG_DIR`, no generation-home environment value, no credential
object below any P, no second shared adapter process, no write to the rotating
credential store by an apply worker, and no product-cwd mutation. Capture the
credential writer identity before, during, and after activation and realization.
Sanitize tokens and identity bytes before publication. A package version or
content-digest mismatch, missing raw ordering evidence, skill bleed, unsupported
resume guidance, or second credential writer fails the gate and removes the
corresponding R-03 declaration. A mocked adapter cannot satisfy this acceptance.

**A-22 — Realization crash matrix (R-11, I-02, I-03, I-10).** Start with A's
terminal row committed, B active, and one B-bound turn in
`realization_pending`. Stop the coordinator immediately before and after each
persisted close intent, close request, close response, resume intent, resume
request, resume response, history catch-up, runnable transaction, and first
prompt. At each stop, advance the fake database clock to one millisecond before
lease expiry and then to expiry. Before expiry no adopter acts. At expiry one
owner epoch wins, stale returns change no row, and the R-08 retry times remain
byte-exact.

Every recovery order closes only A, realizes only the turn's captured P-B, and
sends exactly one first B prompt after the runnable transaction. An uncertain
resume response closes that unprompted adapter session before retry. Replacing
the adapter process makes the old resident session absent and still resumes B
with cwd C. Activating C during the matrix does not retarget the admitted B turn;
B runs once, then a later turn realizes C. No order sends a prompt on A after
its terminal row, sends P-C to the B turn, changes a credential or product byte,
or starts another shared adapter process.

**A-23 — Later-operation ordering (R-05, R-11, I-03).** Hold an A turn, activate
B, and admit one adapter-independent operation and one adapter-dependent
operation in that order. Both capture B. The independent operation reads B
immediately. The dependent operation remains `realization_pending` and sends no
request through A. Activate C and admit a C-bound adapter-dependent operation.
Release A. The realization lane runs the B-bound effect on P-B and the C-bound
effect on P-C in admission order, closing each different resident generation
before the next one. Each effect observes only its captured binding. Neither
apply waits for these effects, and no work row is retargeted.

**A-24 — Human-choice boundary (R-17, R-20, I-13).** Given a newer live
revision, a stale fleet, one terminal apply failure, and an available descendant
content revert, run every automatic scheduler and recovery worker. The substrate
computes relations, continues only previously elected nonterminal recovery,
emits the required facts and alarms, and starts no publish, new apply, content
revert, or host repair. Each such action begins only after a separately
authenticated administrator command. Served identity prose cannot supply that
election.

## Open Questions

None. The controlling ruling elects immediate multi-version activation inside
the existing single-writer harness-home topology. A running turn retains its
prior binding. The activation transaction makes the target binding current for
every later admission. Adapter realization follows only for admitted
adapter-dependent work and does not defer or repeat activation.
