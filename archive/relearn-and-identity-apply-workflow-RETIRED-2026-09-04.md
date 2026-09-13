# RETIRED — Relearn and identity-apply workflow

**Retired 2026-09-04 under Mike's operator ruling
`dr_07bdef13-45ae-435f-bc79-b2dc6b0a5ebf` (ruled `1787708624624`, fact `1459`).**

The ruling reads, in Mike's words: "this does not merit contract machinery.
Guidance updates are files in the harness home; a live session gets told to
reread them, best effort; when it actually matters that a session is on the new
guidance, reload the session. No effect IDs, no atomic switch, no revision
readback, no adapter extension spec. The reviewed strict identity-apply Terms
are dropped and the heavyweight candidate is not to be rolled out or maintained;
keep only whatever trivially serves the file-update-plus-nudge path."

This file IS that heavyweight candidate. Its contract is structurally the killed
machinery — effect IDs and creation epochs, an `invoke`/`status` effect-recovery
contract, atomic reload replacement with rollback, prior-context snapshot and
readback, an admission fence, `runner-stop`/`reload` effect phases, adapter
generation tokens, and reset/reload of sessions with running turns. None of it
was ever implemented: `0.1.9` at `81c91e2a` and `main` at `1c1110ca` contain no
effect ID, admission fence, prior-context, runner-stop, reload adapter, identity
generation, or revision readback. Retiring it removes a spec-only surface, not a
shipped behavior.

It is kept here as a record. It is not authority, and it is not maintained. Do
not build from it, cite it as a requirement, or refine it.

**Live home for `tightbeam identity apply`:** `immediate-identity-apply-v1.md`
(candidate pending independent exact-revision review at the time of this
retirement). Ownership, publication, `identity edit`, `relearn`, and the
credential and installation laws of `served-identity-home-projection-v1.md`
remain authoritative and are untouched by this retirement.

---

# Relearn and identity-apply workflow

**Status:** spec-approved after cold digest under owner ruling
`att_0e64684f-daed-4934-a052-f9cf80c1d06f`, which applies superseding ruling
`att_b579460b-3887-41d2-8418-450c966e2843` and its adopted proposal
`att_df001f03-b6e1-4308-9726-701095538f85` to changes-requested verdict
`att_d63e3816-bdf6-4027-b598-8d904d54dbbe` on `art_f96d3c92`; that review found
F2 satisfied and requested only four missing positive ASCII-fold fixtures. All
prior owner rulings remain normative except the superseded F2 fence-release
instruction in `att_a62fb81a-4bf9-442f-b640-e4d0083464bd`. Pending one fresh
independent exact-artifact review for
`wi_1f4ff80a-46b3-41a9-bb68-009665015bed`.

**Authority:** This spec extends
`served-identity-home-projection-v1.md`. It supersedes that spec's requirement
that `identity apply` wait for a turn boundary or refuse a running session. It
does not change the identity Git model, the single-revision provisioning rule,
or the explicit-publication rule.

## Goal

Make a shipped Kung Fu relearn and its rollout to existing sessions a complete,
safe operator workflow.

The workflow gives an administrator enough information to resolve a relearn
conflict without discovering hidden paths. A successful relearn names the
sessions that still use an older identity revision and explains the explicit
apply step. An apply operation resets or reloads each selected active session,
including a session with a running turn. It queues one new continuation turn
from durable state after success. If self-apply interrupts the caller and then
safely fails, it queues the caller's staged recovery continuation on the
restored prior context. It reports a durable outcome for every selected session.

## Non-Goals

- A successful relearn does not apply the new identity to a session.
- The system does not choose a conflict resolution for the administrator.
- The system does not overwrite an organization customization to resolve a
  conflict.
- The continuation turn does not replay the interrupted model request.
- The workflow does not roll back external effects produced before a running
  turn was interrupted.
- The workflow does not restart the shared Codex runtime process. It resets or
  reloads the selected Codex thread.
- This spec does not change `identity edit`, `identity status`, `learn`,
  `unlearn`, session retirement, or identity content composition.
- This spec does not add a second identity mutation path outside the existing
  identity seam.

## Terms

- **Identity resolution root:** The absolute path to the Tight Beam-owned
  `identity/` Git working tree in which an administrator resolves a relearn
  conflict.
- **Live revision:** The immutable Git object ID referenced by
  `tightbeam/live`. Sessions read identity content only from this revision.
- **Published relearn:** A clean `identity relearn` or a completed
  `identity relearn --resolve` that advances `tightbeam/live`.
- **Stale session:** An active session whose recorded `identityRevision` differs
  from the live revision. A `NULL` recorded revision differs from a non-`NULL`
  live revision.
- **Selector:** Either one exact session key or `--all`.
- **Selected session:** For one-session apply, the active session named by the
  selector. For `--all`, each active session present when the server accepts the
  operation. The server freezes this set for the life of the operation.
- **Target revision:** The live revision captured when the server accepts a new
  apply operation. One operation never changes target revision.
- **Running turn:** A turn that has entered the durable `running` state and has
  not entered a terminal state.
- **Reset/reload:** Stop the selected session's current harness context when one
  is resident, provision guidance and skills from the target revision, and
  establish a harness context on the same workdir and durable history. A Codex
  reset/reload changes the thread, not the shared runtime process.
- **Durable transcript:** The session's retained message rows and history
  pointer. Reset/reload does not delete, clear, or replace these rows.
- **Continuation prompt:** The exact normal-turn prompt in Architecture R-13.
  The server writes it after reset/reload success or, only for an interrupted
  caller, after safe restoration of the prior context. It is not an exact retry
  of the interrupted turn.
- **Apply operation:** One durable request to apply one target revision to one
  frozen set of selected sessions.
- **Per-session outcome:** One durable executable-attempt record for a selected
  session. It records progress, terminal success or failure, and the IDs of any
  interrupted turn and continuation turn. A terminal record and its attempt
  number are immutable. Retry admission appends a new outcome only for a session
  it reacquires. The R-18 session projection selects the latest executable
  attempt. A retry-admission classification never overlays or replaces a
  terminal outcome's state, error, retryability, epoch, or attempt number.
- **Request principal:** The authenticated administrator user or
  administrator-owned agent identity that requested the operation.
- **Normalized effect request:** The canonical JSON value produced after CLI
  parsing and before idempotency lookup. It has exactly
  `{"selector":{"kind":"all","sessionKey":null}}` or
  `{"selector":{"kind":"session","sessionKey":"<exact-session-key>"}}`.
  The caller key and transport fields are not part of this value.
- **Admission fence:** A durable per-session database row owned by one apply
  operation. A turn claim, another apply effect, and session retirement cannot
  pass this fence. An in-memory lane or mutex is not an admission fence.
- **Recovery owner:** The durable executor epoch recorded on an admission fence.
  It identifies the automatic recovery worker responsible for its nonterminal
  per-session outcome.
- **Execution-owner epoch:** A monotonically increasing fencing token on an
  operation and per-session outcome. Only the executor whose epoch equals both
  the operation's current durable value and its nonterminal outcome's durable
  value can advance a phase, invoke its next harness effect, or commit an
  outcome.
- **Prior runtime context:** The adapter's read-only snapshot of the exact
  logical context active for the session before apply, or its exact restorable
  identity when that context is nonresident. It binds the prior revision,
  workdir, durable history pointer, session incarnation, and adapter
  configuration/generation token. A supported adapter can activate this snapshot
  as one runnable context without changing those durable values.
- **Effect phase:** Exactly `runner-stop` or `reload`. It is the effect
  discriminator stored in the existing executable-attempt phase record and is
  distinct from the R-14 outcome phase. There is no `close` effect phase.
- **Effect ID:** The lowercase hexadecimal SHA-256 of the UTF-8 operation ID,
  one NUL byte, the UTF-8 session key, one NUL byte, the ASCII decimal
  execution-owner epoch at effect creation, one NUL byte, and exactly one ASCII
  effect phase. The executable-attempt phase record
  stores `effectId` and its immutable creation epoch before invocation. A new
  effect under a different epoch produces a different ID and cannot use the
  prior ID's receipt. The derivation does not include an executable-outcome ID
  or attempt number.
- **Effect recovery contract:** The runner-stop adapter and runtime-context
  reload adapter expose `invoke(effectId)` and `status(effectId)`. Both durably
  coalesce calls by effect ID. For `runner-stop`, `status` returns exactly
  `not_started`, `in_progress`, `succeeded(result)`, or `failed(class)`. A
  retryable runner-stop failed class certifies that no runner-stop effect remains
  active and permits another `invoke` with the same ID. A terminal runner-stop
  failed class supplies the applicable R-29 classification; it authorizes safe
  terminal cleanup only with the separate exact-prior-context readback in R-15.
  The `reload` status returns exactly `not_started`, `in_progress`,
  `succeeded(targetContextId,targetRevision,runnable=true)`, or
  `failed(class,priorContextId,priorRevision,runnable=true)`. Before disruption,
  reload invoke stages and validates the target context. It then atomically
  switches the runtime context and internally owns close, target activation,
  rollback, and prior-context restart. A succeeded reload receipt proves the
  named target context is the session's one active runnable context at the
  target revision. A failed reload status proves target activation did not
  commit and the named prior runtime context is again the session's one active
  runnable context at the prior revision, including after runner-stop
  succeeded. A reload class carries `effectDisposition: "retryable"` or
  `effectDisposition: "terminal"`. Retryable disposition makes failed a
  nonterminal adapter status. It permits another `invoke` with the same ID only
  when `priorContextId`, `priorRevision`, and `runnable=true` match the stored
  prior-context snapshot. A missing, mismatched, or nonrunnable prior-context
  claim is invalid recovery evidence and enters the R-15 status-only recovery
  substate instead of authorizing an invoke.
  Terminal disposition makes it the terminal failed receipt and supplies the
  applicable R-29 classification; that public classification retains its own
  R-29 retryability. The reload adapter returns no other terminal receipt and
  never terminalizes with neither context runnable. Calls with one ID produce
  at most one logical phase effect and one terminal receipt. Only the current
  executor lease that owns the durable obligation for that exact ID and
  creation epoch may consume the receipt. Recovery adoption can transfer that
  obligation to a new owner epoch; it does not turn the receipt into the result
  of an effect created under the new epoch.
- **Effect recovery policy:** The operation snapshots the positive integer
  field `effectTimeoutMs: 30000` and
  `effectRecoveryBackoffMs: [5000, 10000, 20000, 40000, 60000]` at acceptance.
  Invoke and status deadline is `callStartedAt + 30000`. The gateway persists
  `callStartedAt` and the deadline before each call. It records those values,
  observations, and `nextAttemptAt` as integer Unix-epoch milliseconds from the
  database transaction clock. Recovery ordinal zero through four uses the
  corresponding delay in the array; each later ordinal uses `60000`. The
  durable `nextAttemptAt` is the timeout or unavailable observation timestamp
  plus that delay. The schedule has no jitter.
- **Effect recovery obligation:** The recovery state in the existing durable
  executable-attempt phase record: effect ID, phase, immutable creation epoch,
  current owner epoch, recovery-attempt ordinal, last call kind and result,
  adapter status, terminal receipt when present, next-attempt timestamp,
  supervising recovery owner, and, while invalid recovery evidence is active,
  the status-only recovery marker, invalid receipt observation, and typed
  recovery cause. It is not a separate store. The admission fence
  protects the session while this state waits; no executor lease or database
  lock remains held between attempts.
- **Prior-context snapshot obligation:** The pre-effect recovery state in the
  existing executable-attempt row. Acceptance records the expected session
  incarnation and adapter configuration/generation token, snapshot-attempt
  ordinal zero, no recovery-attempt ordinal, generation-retry count zero, current owner
  epoch, and supervising worker.
  Before each snapshot call it records `callStartedAt`, a 30,000 ms deadline,
  and, after a failed call, `nextAttemptAt`. It carries no effect ID because the
  snapshot is read-only. The admission fence protects the session while this
  obligation waits; no executor lease or database lock spans snapshot I/O.
- **Execution cohort:** The per-session outcomes admitted to execute under one
  operation execution-owner epoch. Initial acceptance admits fence-owning
  outcomes to the initial cohort. Retry admission appends and admits only new
  outcome records for reacquired sessions; all prior terminal records remain
  immutable history of their earlier epochs.
- **Retry admission:** The one transaction that can retry terminal failed
  sessions whose latest errors are retryable by appending new executable-attempt
  records. It is admissible only after every outcome in the operation's current
  execution cohort is terminal. An idempotent replay that only returns an
  existing result is not retry admission.
- **Retry attempt:** A monotonically increasing operation-scoped admission
  ordinal allocated only when R-16 commits a new retry-admission decision. It is
  distinct from a per-session executable attempt number. A classified-only
  decision records the ordinal on its event and never on a terminal outcome.
- **Retry-admission result:** An append-only fact for a terminal retry candidate
  that a retry-admission transaction does not reacquire. Its unique key is
  `(operationId, retryAttempt, executionOwnerEpoch, sessionKey)`. It records the
  source executable-outcome ID, prior cohort and epoch, requested and current
  revisions, deterministic R-29 classification, retryability and
  failure-material ID, request principal, and controlled cause. It is an
  `identity_apply_retry_admission_result` event in the existing event history
  with linked existing failure material, not a new store. Its event ID is
  deterministically derived from the unique key, so the existing event-ID
  uniqueness rail rejects a duplicate. It is queryable through that history and
  never changes the candidate's terminal outcome or attempt number.
- **Continuation intent:** A durable, non-claimable record containing the exact
  R-13 prompt, client message ID, and execution-owner epoch. At most one intent
  exists for an operation/session/epoch. Materializing it writes the transcript
  row and queued turn through the normal delivery transaction.
- **Failure material:** One durable, sanitized structural envelope for one
  failed executable attempt or retry-admission classification. Its `ifm_`
  identifier connects the safe public error to incident evidence without
  exposing raw adapter data.
- **Failure-normalization boundary:** A supervised isolated worker or process
  that owns an arbitrary ECMAScript thrown value and returns only its canonical
  redacted envelope. The gateway persists `normalizationTimeoutMs: 30000` and
  `normalizationMaxVisitedNodes: 65536` before starting it. The supervisor can
  terminate the worker at the deadline or node budget without holding a gateway
  or database lock.
- **Well-formed failure string:** The string produced from an ECMAScript string
  value by `String.prototype.toWellFormed` semantics. Reading UTF-16 code units
  left to right, each valid high-surrogate/low-surrogate pair becomes its one
  Unicode scalar, each unpaired high or low surrogate becomes one U+FFFD, and
  each other code unit becomes its scalar. This operation performs no other
  Unicode normalization.
- **Source-key order:** Ascending lexicographic order of the original ECMAScript
  property-name UTF-16 code units treated as unsigned 16-bit integers. A key
  that is an exact prefix sorts first. This order is fixed before secret-name
  comparison, preserved-name allowlisting, or `$field<N>` remapping.
- **ASCII secret-name fold:** A transform defined only for a well-formed source
  key. It adds hexadecimal `0x20` to each UTF-16 code unit from U+0041 through
  U+005A and leaves each other code unit unchanged. It performs no Unicode
  normalization, Unicode case folding, or locale mapping. The worker compares
  the transformed code-unit sequence exactly with the lowercase ASCII secret
  names in R-29. An ill-formed source key is ineligible for this transform and
  for a secret-name match.

## Assumptions

1. The identity tree uses `main` as the organization customization branch,
   `tightbeam/upstream` as the imported shipped-content branch, and
   `tightbeam/live` as the only published session source.
2. Relearn already leaves a conflicted merge in the identity working tree and
   leaves `tightbeam/live` on the last good revision.
3. Each session row records the identity revision from which its current
   harness context was provisioned.
4. The session turn ledger already provides exactly one durable terminal state
   for an accepted prompt.
5. The turn ledger's claim transaction and the session-retirement transaction
   can lock the session row and consult a durable admission fence before either
   transaction changes session state.
6. Normal prompt delivery already writes a transcript row and a queued turn in
   one database transaction. It can reject a second delivery that uses the same
   session-scoped client message ID.
7. The gateway already resolves the authenticated caller to a durable origin
   string and checks administrator authority for identity verbs.
8. The pre-1.0 CLI and gateway use exact version matching. A release that
   changes the wire result ships the matching CLI and gateway together.
9. `identity apply --all` selects active sessions. Retired sessions remain
   durable history and do not resume work.
10. Local durable host-adapter registry metadata identifies the runner-stop,
    read-only prior-context snapshot, and runtime-context reload capabilities
    before apply acceptance. Reading that metadata performs no adapter I/O. It
    reports whether effect adapters implement durable recovery and whether
    reload implements atomic replacement plus prior-context snapshot/readback.

## Invariants

**I-01 — Conflict safety.** A conflicted relearn leaves `tightbeam/live`
unchanged. It leaves both conflicting sides in the identity resolution root.

**I-02 — One revision per operation.** Reset/reload reads guidance, elected
skills, and the revision stamp from the operation's one target revision.

**I-03 — Explicit rollout.** Relearn publication does not create an apply
operation, reset a session, change a session revision stamp, or queue a
continuation prompt.

**I-04 — Running work does not block apply.** A running turn causes apply to
interrupt that turn. It does not cause `turn_in_progress`, an idle wait, or a
fleet-wide refusal.

**I-05 — Crash-durable admission fence.** Apply acceptance or retry admission
writes an admission fence before any harness effect. On boot, recovery assigns
every existing fence to a recovery owner before the gateway enables turn
admission. Every later turn claim also checks the fence in the same transaction
that claims the turn. From fence commit through a terminal apply commit, the
selected session cannot claim another turn. The interruption check and its
action run while the fence remains committed.

**I-06 — Exactly one continuation.** One apply operation produces one
continuation prompt for each selected session that reaches reset/reload
success. It also produces one recovery continuation if it interrupted its caller
and then safely restored the prior context after failure. A retry, caller
disconnect, gateway crash, or duplicate request does not produce a second prompt
for that operation and session. Delivery of the caller recovery continuation
makes the entire operation and key ineligible for retry admission.

**I-07 — Durable history.** Reset/reload retains the session key, workdir,
harness history pointer, transcript rows, assignment rows, work-item rows, and
their provenance. It does not move the visible-history barrier.

**I-08 — Durable outcomes.** Initial acceptance or retry admission records the
operation, affected outcomes, and each acquired admission fence before it begins
harness effects. The acceptance transaction records a prior-context snapshot
obligation without performing adapter I/O. Before a runner-stop or reload effect
can run, a short locked transaction stores the verified snapshot and records
that phase's effect ID and recovery policy.
A gateway restart resolves a lost
response through the adapter's durable status instead of inferring or blindly
replaying the effect. A timed-out call leaves a durable recovery obligation and
admission fence while releasing its executor lease and database locks. An
invalid reload receipt leaves that same nonterminal obligation, effect ID, and
fence in a status-only recovery substate while releasing its executor lease and
database locks. No turn or invoke passes that substate until R-15 receives a
matching authoritative receipt. An in-memory lane never substitutes for
recovery adoption plus the transactional
fence check.

**I-09 — Failure isolation.** A failure for one selected session does not stop
another selected session from attempting reset/reload. The operation result
names each success and each failure. The retry barrier does not cancel, replace,
or delay the current execution cohort; its supervised execution or recovery
continues independently of a rejected retry request.

**I-10 — Provenance.** The operation records the request principal and the
target revision. The continuation turn records `process:tightbeam` as sender,
the apply operation as cause, and the request principal as initiating
principal.

**I-11 — Authorization.** The gateway accepts relearn and apply only from the
existing administrator authority boundary. The gateway performs this check
before it writes an operation or changes identity state.

**I-12 — Harness scope.** Reset/reload affects only the selected session's
harness context. It does not restart an unrelated session or the shared Codex
runtime.

**I-13 — Deterministic projection.** Result arrays use ascending session-key
order. Conflict-path arrays use ascending absolute-path order. A retry of one
operation returns the same frozen selector, target revision, and session order.

**I-14 — No revision downgrade.** At most one nonterminal apply operation owns
the admission fence for a session. Apply never replaces a session revision with
an ancestor of that session's recorded revision. An executor with a stale epoch
cannot invoke another effect or commit progress or completion. The operation's
execution-owner epoch cannot advance through retry admission while any outcome
in its current execution cohort is nonterminal. Crash-recovery adoption remains
governed by I-05 and R-15 and updates every nonterminal row in that cohort. Two
execution cohorts of one operation cannot contain nonterminal outcomes at the
same time. A terminal per-session outcome and its attempt number never change;
retry appends a new executable outcome or a retry-admission result.

**I-15 — Caller-independent execution.** Once acceptance commits, the apply
operation survives request disconnect and cancellation of the caller's turn.
If that caller's agent session is selected, acceptance also persists its
operation ID and exact retrieval command in a continuation intent before any
interruption. Retry admission provides the same guarantee for a retrying agent
caller. An administrator can retrieve the current or terminal result by
operation ID.

## Architecture

### Relearn results

**R-01 — Conflict result.** When relearn produces a Git conflict, the gateway
returns this result shape:

```json
{
  "state": "relearn-conflicted",
  "liveRevision": "<unchanged-live-oid>",
  "resolutionRoot": "/absolute/path/to/identity",
  "conflictingPaths": [
    "/absolute/path/to/identity/guidance/coder.md"
  ],
  "resolveCommand": "tightbeam identity relearn --resolve"
}
```

`resolutionRoot` is the absolute identity resolution root.
`conflictingPaths` contains each unresolved Git conflict below that root as an
absolute path. The gateway sorts the array. `resolveCommand` has the exact value
shown above. The result does not stage files, write file contents, create a
resolution commit, or move `tightbeam/live`. Acceptance: AC-01 and AC-02.

**R-02 — Successful-relearn result.** A published relearn returns the existing
`state: "published"` and `liveRevision` fields. It adds `staleSessions`,
`applyCommand`, and `applyWarning`:

```json
{
  "state": "published",
  "liveRevision": "<new-live-oid>",
  "staleSessions": [
    {
      "sessionKey": "agent:coder:example",
      "identityRevision": "<prior-or-null>"
    }
  ],
  "applyCommand": "tightbeam identity apply --all",
  "applyWarning": "Applying identity resets/reloads each selected session. If a turn is running, Tight Beam cancels that turn before reload. After a successful reload, Tight Beam queues exactly one new continuation turn from the durable transcript and assignment state. It does not retry the interrupted turn. If the caller is a selected agent session, that turn can end before the command receives its final response; before interruption, Tight Beam durably stages a continuation containing the operation ID and exact result command, then releases it after reload succeeds or the prior context is restored."
}
```

The gateway lists active stale sessions after publication and sorts them by
session key. If this list is empty, `applyCommand` is `null`. If this list is
nonempty, `applyCommand` has the exact value shown above. Both a clean initial
relearn and `identity relearn --resolve` use this result. Acceptance: AC-03 and
AC-04.

**R-03 — No implicit apply.** The successful-relearn path computes the stale
projection without invoking the apply executor. Acceptance: AC-04.

### Help and command input

**R-04 — Apply warning.** The `identity apply` entry in global help and the
output of `tightbeam identity apply --help` contain the exact `applyWarning`
string from R-02. The help states the effect form and the mutually exclusive
read-only result form:

```text
tightbeam identity apply (<session> | --all) [--key <idempotencyKey>]
tightbeam identity apply --operation <operationId>
```

Acceptance: AC-05 and AC-24.

**R-05 — Idempotency input.** `identity apply` accepts an optional nonempty
`--key <idempotencyKey>`. The database has one unique binding on
`(requestPrincipal, "identity-apply", idempotencyKey)`. One acceptance
transaction performs the unique insert-or-replay decision. The binding stores
the complete normalized effect request. The transaction that wins a new binding
then captures the live revision, locks selected active session rows in ascending
session-key order, freezes the cohort, and writes the operation, per-session
outcomes, acquired admission fences, initial execution-owner epoch, and any R-30
caller continuation intent before it commits. For each fence-owning outcome, it
also writes the prior-context snapshot obligation and its expected session
incarnation and adapter configuration/generation token. The operation, each
acquired fence, each fence-owning outcome, and each caller intent record that
same initial epoch. A concurrent transaction that loses the unique-binding race
reads the committed operation in that transaction. It cannot create another
operation, cohort, fence, epoch, or continuation intent.

The same principal, key, and byte-equal normalized effect request resumes or
returns the bound operation. The same principal and key with any different
normalized effect request returns `idempotency_conflict` and changes no
operation. Because the loser resolves insert-or-replay before it reads the live
revision, a later publication cannot retarget a retry. Acceptance: AC-10 and
AC-21.

**R-06 — Unkeyed compatibility.** The existing one-session and `--all` forms
remain valid without `--key`. The gateway creates a unique operation ID for
such an invocation and generates its idempotency key inside the R-05 acceptance
transaction. The help states that a caller needs `--key` to coalesce a repeated
effect-form request after it loses the first response. An unkeyed caller can
recover the generated operation ID through R-13 when self-apply cancels its
turn. Acceptance: AC-05, AC-18, and AC-24.

### Apply-operation state

**R-07 — Frozen operation.** The gateway resolves the target revision and the
selected active sessions once inside the R-05 acceptance transaction. For each
selected session, that transaction writes the outcome row and applies the R-17
revision-availability and supersession validation while it holds the session
row lock. It performs that validation before it attempts the session's unique
admission-fence insert. A rejected validation records the applicable terminal
outcome and failure material without a fence, executor, caller intent, or
effect. For a valid revision, the transaction attempts the fence insert. If
another operation owns the fence, this outcome becomes `failed` with
`apply_in_progress`; the other selected sessions remain eligible. If the
authenticated caller is an agent session in the frozen cohort and this
operation acquires that session's fence, the same transaction also writes its
R-30 continuation intent. It writes no caller intent for a revision rejection
or when another operation owns the fence. A session created after `--all`
acceptance is not part of that operation. Acceptance: AC-08, AC-14, AC-20,
AC-21, AC-22, and AC-24.

**R-08 — One mutation seam.** Apply executes each selected session through the
same database-backed session-mutation seam used by turn admission and session
retirement. Each transaction locks the session row before it examines or writes
the admission fence. If retirement commits first, one-session apply returns
`not_found`, and `--all` excludes that session. If apply acceptance and its fence
commit first, retirement cannot commit until apply deletes the fence in a safe
terminal transaction; retirement then runs after apply. New turn claims refuse
the session while the fence exists. Acceptance: AC-07, AC-08, AC-13, and AC-20.

**R-09 — Running-turn interruption.** If the session has a running turn, the
session seam uses one transaction to change that turn to the existing durable
`canceled` terminal state through the ledger compare-and-set and commit the
`interrupting` phase, runner-stop effect ID, and effect recovery obligation.
The transaction exposes neither the canceled state without that obligation nor
the obligation without the canceled state. The executor persists the call start
and 30,000 ms deadline, releases the transaction's database locks, then calls
`invoke(effectId)`. If the turn reaches another terminal state first, the
ledger result is the truth and apply continues without a runner-stop effect.
Apply records the observed terminal outcome and turn sequence in the
per-session row. It records the runner as stopped and advances after
either `invoke(effectId)` returns a `succeeded(result)` receipt or
`status(effectId)` reads back that receipt under the current obligation and
lease. A terminal failed status follows R-29. It does not wait for the model to
finish naturally. A retryable failed, lost, timed-out, unavailable,
`not_started`, `in_progress`, or late response follows R-15. Acceptance: AC-07,
AC-11, and AC-13.

**R-10 — Queued turns.** Apply retains queued turns. The session seam prevents
them from starting during reset/reload. `Ledger.claim_next` locks the session
row and returns no claim when an admission fence exists. After a successful
terminal commit deletes the fence, queued turns read the target revision.
After a safe failed terminal commit deletes the fence, queued turns read the
unchanged prior revision. Acceptance: AC-08, AC-11, and AC-13.

**R-11 — Resident and nonresident sessions.** Apply establishes a harness
context from the target revision for a selected active session even when the
session has never started or its last harness pointer is no longer resident.
It does not treat a missing resident pointer as successful reset/reload by
stamp alone. Acceptance: AC-06 and AC-08.

**R-12 — Post-reload commit.** After the runtime-context reload adapter returns
or reads back a succeeded replacement receipt,
the executor commits `continuation-pending` on the same executable-attempt
record and retains that exact terminal target receipt, its effect ID, and its
immutable creation epoch. The gateway then uses one database transaction to record the target revision on the
session, record reload success, materialize R-13 into the transcript and turn
ledger, record its message and turn IDs, mark the per-session row `succeeded`,
and delete that operation's admission fence. A rejected transaction writes none
of those changes. It leaves the outcome `continuation-pending`, retains the
fence and stored target receipt. After a defined rejection, a separate recovery
transaction appends the deduped R-29 `post_reload_commit_unavailable` event,
records its recovery ordinal and exact `nextAttemptAt`, and releases database
locks and the executor lease. Recovery remains in the same executable-attempt
generation; when that timestamp arrives, it may retry only this identical
atomic database transaction under the current owner epoch.
It does not invoke or query an adapter, create another effect ID, terminalize a
failure, create failure material, or enter R-16. A later successful retry
commits the stamp, reload-success fact, continuation, succeeded outcome, and
fence deletion together. A failure
transaction can mark the outcome `failed` and delete the fence only after one
of four closed proofs: a defined ledger CAS failure before interruption or any
adapter invocation; the second R-15 incarnation or snapshot-generation mismatch
before interruption or any adapter invocation; a terminal runner-stop failure
before reload invocation plus adapter readback that matches the snapshotted
prior context and revision with `runnable=true`; or a failed reload receipt whose class has
`effectDisposition: "terminal"` and that authoritatively names the snapshotted
prior context and revision with `runnable=true`. The first proof leaves the
original turn and prior runtime context unchanged; the second proof does too.
For a selected caller, the
same failure transaction materializes its pre-interruption continuation intent
before deleting the fence only if this operation interrupted that caller's turn.
That transaction records `self_apply_retry_requires_new_operation` with
`retryable: false`, regardless of the underlying failed stage. The failure
material retains that stage and its redacted structural envelope. The same
transaction records that caller's session key as the operation's
`retryAdmissionBlockedBySession`. If the operation did not interrupt the
caller's turn, the failure transaction deletes the unused intent and keeps the
applicable R-29 code. When none of the four closed proofs exists, the outcome
remains nonterminal and the automatic recovery worker retains the fence. A
reload failure does not enter the success transaction.

After any required R-09 runner-stop succeeds and before reload invocation, the
executor commits the `reload` effect ID, the verified prior runtime-context
snapshot, and the recovery obligation in the executable-attempt phase record.
The reload adapter internally owns close, target activation, rollback, and
prior-context restart; the gateway invokes no standalone close effect. It
persists the exact 30,000 ms deadline, releases the transaction's database
locks, then calls `invoke(effectId)`. It
enters the success transaction only after invoke returns or status reads back a
`succeeded(targetContextId,targetRevision,runnable=true)` receipt that matches
the operation target. It enters the safe failure transaction only after invoke
returns or status reads back a
`failed(class,priorContextId,priorRevision,runnable=true)` receipt whose class
has `effectDisposition: "terminal"` and that matches the stored prior snapshot.
For either transition, the current executor lease
must own the obligation's exact effect ID, creation epoch, and current owner
epoch. A terminal failed class follows the existing target-apply failure
cleanup. Retryable failed, lost, timed-out, unavailable, `not_started`,
`in_progress`, or late responses follow R-15; they cannot directly commit the
outcome. Acceptance: AC-06, AC-09, AC-11, AC-12, and AC-24.

**R-13 — Continuation prompt.** Inside the R-12 success transaction or an
interrupted selected caller's safe failure transaction, the gateway delivers
this exact normal-turn prompt:

```text
Identity apply operation <operationId> finished processing this session. Continue from the durable transcript and current assignment state. If the apply interrupted a turn, do not assume its external side effects were rolled back.
Inspect durable results with: tightbeam identity apply --operation <operationId>
```

The delivery uses the session's existing transcript and normal turn ledger. The
gateway assigns a stable client message ID derived from the apply operation ID
and session key. The transcript/turn transaction rejects a second delivery with
that ID. For a selected caller, R-05 stores the exact instantiated prompt and
client message ID as a non-claimable continuation intent before R-09 can
interrupt its turn. For another selected session, R-12 constructs and
materializes the same prompt after reload success. The gateway deletes the
admission fence in a terminal transaction. When that outcome requires a
continuation, the same transaction materializes it before deleting the fence.
The two `<operationId>` placeholders receive the same accepted operation ID.
Once materialized, that operation/session client message ID is final and no
retry admission can request its delivery again. The result query can report
`state: "running"` while other cohort members continue. Acceptance: AC-06,
AC-07, AC-09, AC-10, AC-11, and AC-24.

**R-14 — Durable phase machine.** Each per-session row records these phases:
`pending`, `interrupting`, `reloading`, `continuation-pending`, `succeeded`, or
`failed`. It also records attempt count, prior revision, target revision,
interrupted turn sequence, observed turn outcome, reload outcome, continuation
message ID, continuation turn sequence, exact continuation-intent prompt and
identity when present, admission-fence ownership, execution-owner epoch, and the
R-29 error code, retryability, and failure-material ID when present. The
same row stores the Terms prior-context snapshot obligation and
failure-normalization boundary fields while either obligation is active. The
operation records `retryAdmissionBlockedBySession` as `null` or the one selected
caller session that caused R-12 recovery delivery. The executor supplies its
epoch to every phase transition, next-effect claim, and terminal transaction. A
mismatched epoch changes no row and authorizes no harness call. The executor
writes a phase before the external effect that phase brackets. Each terminal
transition and each transaction that changes the operation epoch locks the
operation row first, then affected outcome rows in ascending session-key order.
R-15 recovery adoption and R-16 retry admission therefore serialize with every
terminal transition on the same operation lock. A nonterminal outcome must
carry the current operation epoch. A terminal outcome not reacquired by retry
retains its last-attempt epoch and has no executor. Acceptance: AC-11, AC-12,
AC-22, and AC-23.

**R-15 — Crash recovery.** Before the gateway enables any turn-admission
endpoint, `Ledger.claim_next` worker, or apply executor, one recovery-adoption
transaction assigns every existing fence to the current durable recovery-owner
epoch. That transaction increments each affected operation's execution-owner
epoch and records the new value on its nonterminal outcomes, fences, and
nonmaterialized continuation intents. For an outstanding effect obligation, it
also retains the effect ID and immutable creation epoch while changing the
obligation's current owner epoch to the adopted value. That transfer authorizes
the new owner to reconcile only the stored logical effect; it does not authorize
the old receipt for a new-epoch effect. For an outstanding prior-context
snapshot obligation, adoption retains its call deadline, attempt ordinals,
generation-retry count, and expected incarnation/generation while changing its
current owner epoch to the adopted value. If adoption cannot commit, those three
surfaces remain disabled. The executor then resumes the nonterminal per-session
row for every adopted fence. Each later claim transaction still refuses a
session whose fence exists. A worker holding the pre-adoption owner epoch cannot
invoke, query, accept a callback, or commit.

Inside the R-05 acceptance transaction, after it locks and freezes the selected
session set but before it commits any durable write, the gateway reads only the
local durable adapter-registry metadata for each selected session. It verifies
the runner-stop and reload effect recovery contracts, read-only snapshot
capability, reload's atomic replacement capability, and exact prior-context
readback capability without invoking an adapter. If any metadata check fails,
the transaction returns the exact R-29
`adapter_effect_recovery_unsupported` command error and rolls back before it
creates an operation or key binding, acquires a fence, or invokes an effect.

After acceptance, a supervised executor claims the durable prior-context
snapshot obligation. Before it calls the read-only snapshot adapter, one
transaction retains snapshot-attempt ordinal zero for the first call or
increments it for a later call, records `callStartedAt`, the exact 30,000 ms
deadline, and the supervising worker, then releases the database locks. The executor invokes the
adapter outside database locks. A successful snapshot returns the prior context
fields in Terms plus the session incarnation and adapter
configuration/generation token observed by the adapter.

A short pre-effect transaction follows the R-14 lock order and reacquires the
session row lock. It revalidates the R-17 revision relation, this operation's
fence ownership, the session incarnation, and the snapshot's
configuration/generation token. If each value still matches, the transaction
stores the snapshot and atomically records the first `runner-stop` or `reload`
effect phase, effect ID, and recovery obligation; the R-09 running-turn case
also commits its ledger cancellation. Only that commit authorizes the effect.
If revision validation rejects, the transaction follows the R-17 terminal
no-effect path.

On the first incarnation or generation mismatch, the transaction discards the
snapshot, changes no turn, refreshes the obligation's expected incarnation and
generation from the locked session row, sets generation-retry count to one,
and returns the obligation to snapshot-pending without an effect. The executor
performs exactly one more snapshot call under the same deadline rules. A second
incarnation or generation mismatch commits terminal `internal_apply_failure`
and its failure material, deletes the fence and unused caller intent, and
records no effect phase, effect ID, interruption, or continuation. A stale
snapshot never authorizes an effect.

When the snapshot call times out, the adapter is unreachable, the supervised
worker crashes, or the supervisor observes its deadline, one transaction appends the deduped R-29
`prior_context_snapshot_unavailable` event. It sets recovery ordinal zero for
the first schedule or increments the prior ordinal, stores `nextAttemptAt` as
the observation timestamp plus 5,000, 10,000, 20,000, 40,000, or 60,000 ms for
ordinals zero through four, and uses 60,000 ms for each later ordinal. It
retains the visible nonterminal outcome and fence and releases the executor
lease and database locks. Recovery repeats only the read-only snapshot call;
no lock spans adapter I/O. A callback after lease release changes no durable
state. Recovery adoption retains the obligation and its current ordinal and
timestamp; when it finds an abandoned in-flight call, it waits until the
persisted deadline, records the unavailable event once, and follows the same
schedule.

For a nonterminal effect obligation after a retryable failed response, lost
response, crash, or timeout, the recovery owner claims a durable executor lease and calls
`status(effectId)` after persisting that call's exact 30,000 ms deadline and
without holding a database lock. It handles the returned status as follows:

1. A runner-stop `succeeded(result)` enters the R-09 phase commit once. A reload
   `succeeded(targetContextId,targetRevision,runnable=true)` enters the R-12
   success transaction once. The applicable result, effect ID, immutable
   creation epoch, current owner epoch, and executor lease must match the
   obligation.
2. `not_started`, a retryable runner-stop `failed(class)`, or a retryable reload
   `failed(class,priorContextId,priorRevision,runnable=true)` that matches the
   stored prior snapshot persists a new 30,000 ms call deadline, then calls
   `invoke(effectId)` again with the same ID.
3. `in_progress` for either phase records the observation and schedules another
   status recovery by setting recovery-attempt ordinal zero for the first schedule or
   incrementing the prior ordinal, stores the corresponding exact
   `nextAttemptAt`, then releases the executor lease and transaction locks.
4. A terminal runner-stop `failed(class)` enters the R-12 safe failure
   transaction with `turn_interruption_failed` only after readback verifies that
   reload was not invoked and the stored prior context and revision remain
   active with `runnable=true`. A terminal reload
   `failed(class,priorContextId,priorRevision,runnable=true)` enters that
   transaction with the applicable R-29 code only when the class has
   `effectDisposition: "terminal"` and the receipt matches the stored prior
   snapshot. A retryable reload failed receipt with a missing or different
   `priorContextId` or `priorRevision` has recovery cause `context_mismatch`.
   One whose identifiers match but whose `runnable` value is not exactly `true`
   has recovery cause `nonrunnable`. Either is invalid recovery evidence. Any
   other terminal shape or failed runner-stop readback also violates the adapter
   contract. The worker records one deduped nonterminal `adapter_unavailable`
   recovery event, retains the outcome, fence, effect ID, immutable creation
   epoch, and invalid receipt observation, sets recovery-attempt ordinal zero
   for the first schedule or increments the prior ordinal, stores the
   corresponding exact `nextAttemptAt`, releases its executor lease and
   database locks, and makes the host fail subsequent capability checks. It
   performs no invoke, outcome commit, continuation delivery, fence deletion,
   or turn admission.

An invalid retryable reload receipt returned directly by `invoke(effectId)`
enters the same status-only recovery transaction with `callKind: "invoke"`.
An invalid receipt read by `status(effectId)` enters it with
`callKind: "status"`. Neither source authorizes another invoke.

After invalid recovery evidence, the obligation remains in status-only recovery
for the same effect ID. At each `nextAttemptAt`, a current-epoch owner may call
only `status(effectId)`. `not_started`, `in_progress`, adapter unavailability,
or another invalid receipt appends the applicable deduped recovery observation,
advances the exact 5,000, 10,000, 20,000, 40,000, then 60,000 ms capped schedule,
and again releases the executor lease and database locks without invoking. A
later retryable failed receipt that matches the stored snapshot with
`runnable=true` clears status-only recovery and may enter rule 2. A matching
authoritative succeeded or terminal failed receipt clears it and enters rule 1
or rule 4. Recovery adoption retains this substate, observation, ordinal, and
timestamp. While the marker is active, these status-only rules take precedence
over rules 2 and 3. The worker does not infer success or safe failure from
invalid evidence.

When an invoke or status deadline expires, the worker aborts that transport
best-effort. One transaction records call result `timed_out`, sets
recovery-attempt ordinal zero for the first schedule or increments the prior
ordinal, computes and stores the corresponding exact `nextAttemptAt`, preserves
the fence and effect ID, and releases the executor lease. The transaction
releases its database locks when it commits. A transport callback that arrives
after lease release changes no durable state. A later current-epoch
recovery owner can consume the stored logical effect only through status for the
obligation's exact effect ID and creation epoch.
Timeout does not prove that the external effect stopped or cannot complete
later. Durable same-ID coalescing plus readback provides that safety; each
recovery invoke and status call uses the stored effect ID.
If the obligation was in status-only recovery when the call began, timeout
retains that marker, invalid observation, and typed recovery cause; the next
attempt remains status-only.

When the adapter cannot be reached, the same transaction records the R-29
nonterminal `adapter_unavailable` recovery event, its `nextAttemptAt`, and the
recovery owner's supervision evidence. The transaction sets recovery-attempt
ordinal zero for the first schedule or increments the prior ordinal, then uses
the corresponding exact delay. It releases the executor lease and database
locks. Each later unavailable observation repeats this durable step at the
60,000 ms capped delay. It does not mark success, terminalize the outcome,
delete the fence, or admit a turn. The operation query therefore exposes a
running outcome backed by a visible durable obligation instead of a hung worker.
An unavailable observation in status-only recovery retains that marker,
invalid observation, and typed recovery cause and cannot authorize `invoke`.

For a `continuation-pending` outcome with a stored succeeded reload receipt,
the recovery owner waits until its durable `nextAttemptAt`, then claims an
executor lease for that same executable attempt,
verifies the receipt's effect ID, immutable creation epoch, target revision, and
current owner epoch, and retries only the R-12 atomic database transaction. A
defined storage rejection changes no stamp, continuation, outcome, or fence.
A separate transaction appends one deduped
`post_reload_commit_unavailable` event, sets recovery ordinal zero after the
first rejection or increments the prior ordinal, and stores `nextAttemptAt` as
the rejection-observation timestamp plus 5,000, 10,000, 20,000, 40,000, or
60,000 ms for ordinals zero through four; each later ordinal uses 60,000 ms.
That transaction releases the lease and database locks. If recovery observes a
`continuation-pending` row with no `nextAttemptAt`, whether the process stopped
before its initial post-reload transaction or after a rejection but before
scheduling, it records ordinal zero once and waits for that timestamp before
another commit attempt. Recovery adoption may change the current owner epoch, but it retains
the executable attempt, stored receipt, effect creation epoch, recovery
ordinal, and next-attempt timestamp. Neither normal recovery nor adoption
invokes `status`, invokes an adapter, creates a new effect, or classifies a
terminal failure for this state.

Recovery consults the stable continuation message ID before it delivers R-13.
It deletes a fence only in the R-12 success transaction or the safe failure
transaction described there. Once the adapter returns a valid terminal receipt,
phase-boundary recovery converges to one terminal outcome and at most one
continuation prompt per operation/session. Acceptance: AC-11.

**R-16 — Retry after failure.** Repeating the command with the same principal,
key, and byte-equal normalized effect request enters one retry-admission
transaction. That transaction locks the operation row, then reads and locks
every current-execution-cohort outcome in ascending session-key order. It tests
the locked phases before it reads `retryAdmissionBlockedBySession`. If any
locked cohort row is nonterminal, it returns this exact retryable command error
and rolls back the transaction without a durable write:

```json
{
  "code": "apply_cohort_in_progress",
  "message": "Identity apply operation <operationId> still has a nonterminal session; retry after the current cohort completes.",
  "retryable": true
}
```

It does not advance the operation epoch, append an outcome, acquire a fence,
bind an executor, create a continuation intent, or create a continuation fact.
The existing automatic execution or recovery owner remains responsible for
every nonterminal row. This command error is not a failed per-session outcome
and creates no R-29 failure material or event. An empty current execution cohort
satisfies this terminal-cohort check.

Only after the same transaction observes every current-execution-cohort row
terminal does it read `retryAdmissionBlockedBySession`. When the field is
non-`null`, it returns the completed operation unchanged, including the
`self_apply_retry_requires_new_operation` result, and creates no retry attempt.
Otherwise it excludes succeeded outcomes and outcomes whose latest durable
error is nonretryable. It never retries a session whose continuation client
message ID was materialized.

Before it creates another retry attempt, the transaction checks the latest
retry-admission result for each candidate's source executable-outcome ID. A
nonretryable result for that source outcome is final and always replays. A
retryable `apply_in_progress` result replays while its recorded blocking
fence-owner cause still equals current durable state; it permits a new decision
only after that equality becomes false. A response-loss replay therefore
returns the unchanged terminal application projection, and the event-history
query returns the already committed fact with its stored principal, normalized
request binding from the operation, source outcome, prior cohort and epoch,
requested and current revisions, and controlled cause. Replay does not allocate
another retry attempt or operation epoch.

For the remaining terminal retryable candidates, the transaction locks each
immutable outcome record and its session row in ascending session-key order
through the same session lock used by retirement. It allocates one new
`retryAttempt` and one new operation execution-owner epoch. It then applies
these rules in order for each candidate:

1. If retirement already committed, it appends a `session_retired`
   retry-admission result and creates no outcome, fence, executor, continuation
   intent, or interruption.
2. It applies the R-17 revision-order check. `apply_superseded` or
   `identity_revision_unavailable` appends that retry-admission result and
   creates no outcome, fence, executor, or continuation intent.
3. It attempts the unique fence insert. A lost insert appends a retryable
   `apply_in_progress` retry-admission result whose cause names the blocking
   fence owner, and creates no outcome, executor, or continuation intent.
4. A won insert appends a new `pending` per-session outcome with the next
   executable attempt number, records the new epoch on that outcome and fence,
   and includes that new outcome in the execution cohort. When the authenticated
   retry caller is that selected agent session, it also creates exactly one
   caller continuation intent for the new operation/session/epoch.

Each retry-admission result is one
`identity_apply_retry_admission_result` event using the unique key and fields
defined in Terms and linked to its applicable existing R-29 failure material.
The transaction advances the operation epoch and commits all classification
events, linked failure material, new outcomes, acquired fences, and applicable
caller intents together. Only reacquired sessions bind the new epoch and fence.
If none is reacquired, the new execution cohort is empty and no executor exists.
If at least one is reacquired, the same transaction binds the supervised
executor claim to the new epoch before it can enter `interrupting`. R-18 and
R-30 continue to project only executable application outcomes. A classified-only
fact is queried separately through the R-23 event history and never changes a
terminal session projection or counter.

If retry admission wins a retirement race, retirement waits for or follows the
fenced new attempt. If retirement wins, rule 1 appends the only new result. A
worker with an earlier epoch cannot invoke a next effect, advance a phase, or
commit a terminal result. Recovery adoption and retry admission serialize on
the operation row; adoption does not perform retry admission or bypass the
cohort-terminal check. A new effect after
`self_apply_retry_requires_new_operation` requires a new key and therefore a
new operation. Acceptance: AC-10, AC-12, AC-20, AC-22, AC-23, and AC-24.

**R-17 — Concurrent operations.** The per-session mutation seam orders two
apply operations that select the same session without holding one fleet-wide
lock during harness I/O. A unique nonterminal-fence constraint permits only one
operation to perform effects for that session. A later operation that encounters
the fence records `apply_in_progress`, performs no harness effect, and queues no
continuation for that session. R-16 is the only seam that can reacquire a fence
for that failed row.

Initial acceptance and retry admission compare the operation target revision
with the session's recorded revision while holding the session row lock and
before attempting the unique fence insert. A `NULL` recorded revision, an equal
revision, or a recorded revision that is a Git ancestor of the target can
proceed. If the target is an ancestor of the recorded revision, the transaction
records nonretryable `apply_superseded`. If both revisions exist but neither is
an ancestor of the other, or either required object cannot be read, it records
nonretryable `identity_revision_unavailable`. These terminal rejections commit
without a fence, executor, caller intent, harness effect, or continuation.

Immediately before the first runner-stop or reload effect, one transaction
follows the R-14 lock order, holds the same session row lock, and repeats that
revision validation. It also verifies this operation's fence ownership and the
R-15 snapshot's session incarnation and adapter configuration/generation token.
If revision validation rejects, the transaction records the applicable terminal
outcome and failure material, deletes this operation's pre-effect fence and
unused caller intent, and commits no snapshot, effect phase, effect ID, or
recovery obligation. An incarnation or generation mismatch follows the bounded
R-15 discard/resnapshot-or-terminal-no-effect rule. If every check accepts, that
same transaction stores the verified snapshot and commits the first effect
phase, effect ID, and recovery obligation before it releases the session row
lock. R-09 additionally commits its ledger cancellation in that transaction.
No pre-effect invalidation can leave a terminal outcome with a fence. Each
operation retains its own target revision and continuation dedupe ID.
Acceptance: AC-13, AC-14, and AC-22.

### Apply result and failure policy

**R-18 — Apply result.** An effect-form response and the R-30 result query return
this additive durable snapshot. `applied` and `identityRevision` preserve the
existing fields.

```json
{
  "state": "completed",
  "outcome": "succeeded",
  "operationId": "iap_<id>",
  "idempotencyKey": "<caller-key-or-generated-key>",
  "identityRevision": "<target-live-oid>",
  "selector": {
    "kind": "all",
    "sessionKey": null
  },
  "requestedBy": "agent:product-owner:example",
  "applied": ["agent:coder:example"],
  "failed": [],
  "sessions": [
    {
      "sessionKey": "agent:coder:example",
      "state": "succeeded",
      "attempts": 1,
      "priorIdentityRevision": "<prior-or-null>",
      "identityRevision": "<target-live-oid>",
      "interruptedTurnSeq": null,
      "turnOutcome": "not-running",
      "reloadOutcome": "reloaded",
      "continuationMessageId": "<message-id>",
      "continuationTurnSeq": 42,
      "error": null
    }
  ]
}
```

`outcome` is `succeeded` when each selected session succeeded, `partial` when
at least one succeeded and at least one failed, and `failed` when each selected
session failed. While any row is nonterminal, `state` is `running`, `outcome` is
`null`, and the arrays reflect the durable rows at query time. When every row is
terminal, `state` is `completed`. An empty frozen selection produces
`state: "completed"`, `outcome: "succeeded"`, and three empty arrays.
`turnOutcome` is `not-running`, `canceled`, `delivered`, `failed`, or
`failed-unknown`. `reloadOutcome` is `reloaded` or `not-completed`. `applied`,
`failed`, and `sessions` use ascending session-key order. A failed session uses
`state: "failed"` and includes this exact error shape. Its continuation IDs are
`null` unless R-12 materialized the selected caller's recovery continuation.

```json
{
  "code": "harness_reload_failed",
  "message": "Tight Beam could not reload identity for session <sessionKey>; retry this operation.",
  "retryable": true,
  "failureMaterialId": "ifm_<id>"
}
```

The code, message template, and retryability come from R-29. Acceptance: AC-06,
AC-08, AC-12, AC-23, and AC-24.

`retryable` describes whether R-16 can initially consider that executable
outcome for another attempt when `retryAdmissionBlockedBySession` is `null`. A
later nonretryable retry-admission result can close that candidacy without
changing this terminal projection. A `self_apply_retry_requires_new_operation`
outcome blocks retry admission for the whole operation; its fixed message gives
the required new-key action.

**R-19 — Caller-independent partial completion.** Acceptance commits a durable
executable operation. A supervised executor that is not a child of the HTTP
request, CLI connection, or caller's `TurnTask` claims ownership of the initial
R-05 epoch by compare-and-set. No per-session row can enter `interrupting`
before that claim commits. `--all` attempts each eligible frozen selected
session even after another session fails. While connected, a newly accepted
ordinary effect-form caller waits for the completed attempt result. A replay
while that operation's current cohort is nonterminal follows R-16 instead. The
CLI exits zero for `outcome: "succeeded"` and exits nonzero for `partial` or
`failed`. If the caller disconnects or its selected turn is canceled, the
executor continues and R-30 retrieves the result. On retry, only after every
current-cohort outcome is terminal, the R-16 transaction advances the
execution-owner epoch. When it reacquires at least one session, that transaction
also claims the epoch and binds the claim atomically with the new outcomes,
fences, and applicable caller intents; no separate claim can intervene. A
classified-only retry has an empty cohort and no executor claim. Acceptance:
AC-12, AC-22, and AC-24.

**R-20 — Invalid single target.** A one-session selector that names no active
session returns `not_found` before operation creation. It does not reveal
whether the key names a retired session. Acceptance: AC-15.

### Authorization, provenance, and observability

**R-21 — Principal check.** The gateway performs the existing administrator
check for conflict output, relearn publication, effect-form apply, and the R-30
result query. A denied request returns `forbidden` and writes no identity or
apply-operation state. An authorized query for an unknown operation returns
`not_found`. Acceptance: AC-15 and AC-24.

**R-22 — Apply provenance.** The durable operation stores `operationId`,
`requestedBy`, `requestedAt`, `idempotencyKey`, normalized effect request,
selector, target revision, execution-owner epoch, and the frozen
selected-session keys. For each epoch it also stores the execution-cohort
session keys. Every terminal outcome and its executable attempt number are
append-only. For each classified-only candidate, the existing append-only R-23
event history stores one R-16 `identity_apply_retry_admission_result` event keyed
by operation, retry attempt, epoch, and session, plus its linked failure
material. The event contains every field in the Terms definition. The terminal
R-18/R-30 application projection remains byte-for-byte unchanged by that event.
The continuation transcript row stores
`sender: "process:tightbeam"` plus machine-readable cause metadata containing
the operation ID, target revision, and request principal. Acceptance: AC-15 and
AC-17.

**R-23 — Events.** The durable event stream records operation acceptance, each
per-session phase change, each named failure, each retry, and operation
completion. Each event carries the operation ID, session key when applicable,
target revision, request principal, and cause. An executable-attempt failure
event carries the same public error object as its R-18 outcome: code, sanitized
message, retryability, and failure-material ID. An R-16 retry-admission result
event carries those four fields for its classification while leaving the R-18
outcome unchanged. Neither event carries stage, source, or the unclassified
structural envelope. The event contains no identity file contents, transcript
contents, credentials, raw adapter messages, stack traces, response bodies, or
harness tokens. Acceptance: AC-12, AC-15, AC-17, and AC-23.

**R-24 — Status truth after partial apply.** `identity status` continues to
derive staleness from each session's recorded revision compared with
`tightbeam/live`. A failed session therefore remains stale. A succeeded session
reports current when the operation target is still live. Acceptance: AC-12 and
AC-14.

### Migration and compatibility

**R-25 — Additive storage migration.** The release adds durable operation,
per-session outcome, admission-fence, and failure-material stores. Migration
creates them without rewriting existing session, transcript, turn, assignment,
or work-item rows. The operation and outcome stores include the execution-owner
epoch, retry-admission block, continuation-intent, prior-context snapshot
obligation, and failure-normalization obligation fields required by R-14,
R-15, R-19, R-29, and R-30. Migration creates unique constraints for the R-05
principal/verb/key binding, one nonterminal admission fence per session, and one
continuation delivery per operation/session dedupe ID. It also creates one
continuation intent per operation/session/execution-owner epoch. An existing
organization with no apply operations yields empty stores. Acceptance: AC-16
and AC-21.

**R-26 — Command compatibility.** Existing invocations
`identity apply <session>` and `identity apply --all` remain valid. `--key` is
additive. The R-30 `--operation` query is additive and mutually exclusive with
the effect selectors and `--key`. Existing result keys retain their names and
types. Conflict paths retain the `conflictingPaths` array key but become
absolute. Acceptance: AC-16, AC-18, and AC-24.

**R-27 — Source-spec compatibility.** This spec replaces only the
turn-boundary refusal and stamp-only nonresident apply clauses in
`served-identity-home-projection-v1.md`. Its publication isolation, one-OID
provisioning, same-workdir/history, identity seam, and shared-runtime rules
remain normative. Acceptance: AC-09, AC-14, and AC-18.

**R-28 — Operating pattern.** This spec teaches one operator pattern: publish
identity, inspect the stale-session list, apply explicitly, and inspect the
durable per-session results. CLI help and successful-relearn output teach that
pattern. This change requires no seed-guidance or substrate-manual amendment.
Acceptance: AC-19.

**R-29 — Error taxonomy and failure material.** Every failed executable attempt
and every R-16 retry-admission classification uses the first matching condition
in this table. `<sessionKey>`, `<targetRevision>`, and `<failureMaterialId>` are
replaced with their recorded values.

| Code | Deterministic condition | Retryable | Exact safe message template |
| --- | --- | --- | --- |
| `self_apply_retry_requires_new_operation` | The operation interrupted its selected caller, safely restored the prior context after failure, and durably materialized that caller's recovery continuation. | `false` | `Self-apply for session <sessionKey> restored the prior context and delivered its recovery continuation; start a new identity apply operation with a new key.` |
| `session_retired` | R-16 retry admission observes that retirement committed before the session-row lock was acquired. | `false` | `Session <sessionKey> retired before retry admission; this operation will not retry it.` |
| `apply_in_progress` | The fence insert or reacquire loses the session's unique-fence constraint. | `true` | `Another identity apply operation controls session <sessionKey>; retry this operation.` |
| `apply_superseded` | R-17 proves that the target is an ancestor of the recorded session revision. | `false` | `Session <sessionKey> already uses a newer identity revision; this operation will not replace it with <targetRevision>.` |
| `identity_revision_unavailable` | R-17 cannot read a required Git object or proves that target and recorded revisions are unrelated. | `false` | `Identity revision <targetRevision> is unavailable or is not a valid successor for session <sessionKey>.` |
| `turn_interruption_failed` | The ledger CAS returns its defined no-write failure before interruption or any adapter invocation, or runner-stop status returns terminal failed and R-15 readback proves the exact prior context remains active and runnable before reload invocation. | `true` | `Tight Beam could not durably interrupt the running turn for session <sessionKey>; retry this operation.` |
| `harness_reload_failed` | `reload` returns a terminal failed receipt that proves the stored prior context is active and runnable and target activation did not commit. | `true` | `Tight Beam could not reload identity for session <sessionKey>; retry this operation.` |
| `internal_apply_failure` | No earlier condition matches, including an unrecognized thrown value after R-15 has reconciled any adapter effect status. | `true` | `Identity apply failed for session <sessionKey> with an internal error; failure material is <failureMaterialId>.` |

The pre-acceptance unsupported-adapter error has this exact command shape:

```json
{
  "code": "adapter_effect_recovery_unsupported",
  "message": "Identity apply requires recoverable prior-context snapshot, runner-stop, and atomic recoverable runtime-context reload; session <sessionKey> on host <host> does not support that contract.",
  "retryable": false
}
```

The gateway reports the first unsupported selected session in ascending
session-key order. This command error creates no operation, idempotency binding,
outcome, failure material, event, fence, intent, or effect.

`adapter_unavailable` is a nonterminal recovery event, not a failed outcome. It
uses the exact safe message `Identity apply adapter for session <sessionKey> is
unavailable; recovery will retry at <nextAttemptAt>.`, `retryable: true`, and
records the effect ID, phase, epoch, call kind, recovery-attempt ordinal,
`nextAttemptAt`, recovery owner, and supervising worker ID. A `timed_out`
recovery event records the same fields plus the deterministic call deadline.
For invalid reload recovery evidence, the event additionally records
`recoveryCause: "context_mismatch"` when `priorContextId` or `priorRevision` is
missing or differs from the stored snapshot, or
`recoveryCause: "nonrunnable"` when those identifiers match and `runnable` is
not exactly `true`. The executable-attempt phase record retains the structured
receipt, stored snapshot identifiers, request principal, effect ID, immutable
creation epoch, and current owner epoch as correlation evidence; it stores no
raw adapter message or credential. While that observation is current, the event
records the actual observing call kind, `invoke` or `status`. Each later call in
status-only recovery records `callKind: "status"`, and no invoke is authorized.
The message renders `<nextAttemptAt>` as its decimal Unix-epoch-millisecond
value. Each event ID is the lowercase hexadecimal SHA-256 of its effect ID,
one NUL byte, ASCII decimal recovery-attempt ordinal, one NUL byte, and ASCII
call kind; event-ID uniqueness dedupes a replay of that recovery call. Neither
event creates failure material or changes the R-18 error projection.

`post_reload_commit_unavailable` is a nonterminal recovery event, not a failed
outcome. It uses the exact safe message `Identity apply post-reload commit for
session <sessionKey> is unavailable; recovery will retry at <nextAttemptAt>.`,
`retryable: true`, and records the stored reload effect ID and creation epoch,
current owner epoch, recovery-attempt ordinal, `nextAttemptAt`, recovery owner,
and supervising worker ID. The message renders `<nextAttemptAt>` as its decimal
Unix-epoch-millisecond value. Its event ID is the lowercase hexadecimal SHA-256
of the executable-outcome ID, one NUL byte, ASCII decimal recovery-attempt
ordinal, one NUL byte, and ASCII `post_reload_commit_unavailable`. Event-ID
uniqueness dedupes a replay of that schedule. The event creates no failure
material and changes no R-18 error projection, session revision stamp,
continuation, outcome, or fence.

`prior_context_snapshot_unavailable` is a nonterminal recovery event, not a
failed outcome. It uses the exact safe message `Identity apply prior-context
snapshot for session <sessionKey> is unavailable; recovery will retry at
<nextAttemptAt>.`, `retryable: true`, and records the snapshot-attempt ordinal,
recovery-attempt ordinal, generation-retry count, expected session incarnation
and adapter generation,
30,000 ms call deadline, `nextAttemptAt`, current owner epoch, recovery owner,
and supervising worker ID. Its event ID is the lowercase hexadecimal SHA-256 of
the executable-outcome ID, one NUL byte, ASCII decimal recovery-attempt ordinal,
one NUL byte, and ASCII `prior_context_snapshot_unavailable`. Event-ID
uniqueness dedupes a replay of that schedule. The event creates no failure
material and changes no R-18 error projection, session stamp, snapshot,
continuation, outcome, or fence.

Before an executable attempt can terminalize an unrecognized thrown value as
`internal_apply_failure`, one transaction records the Failure-normalization
boundary's deadline, node budget, and supervising worker on the nonterminal
attempt. It then releases its locks while the isolated worker normalizes the
value. A current-epoch recovery owner that finds an abandoned normalization
obligation closes it with the supervisor-generated `inspection-failure`
sentinel. The terminal transaction accepts only the canonical worker envelope
or fixed supervisor sentinel. An R-16 classified-only result uses a fixed
controlled-cause envelope and never reflects over a thrown value.

For an executable-attempt failure, the executor writes one immutable
failure-material row in the transaction that commits the failed outcome. For an
R-16 classified-only result, the retry-admission transaction writes one
immutable failure-material row and its event atomically without writing or
changing an outcome. A failure-material row contains `failureMaterialId`,
operation ID, session key, `attemptKind` (`executable` or `retry-admission`), the
corresponding executable attempt number or retry-attempt ordinal, code, stage,
controlled source (`gateway`, `ledger`, `database`, `codex`, or `claude`),
capture timestamp, SHA-256 of the transient raw source bytes or `null`, raw byte
count, and a restricted durable `unclassifiedEnvelope` produced after secret
redaction.

When no transient raw source bytes exist for an ECMAScript value, the row stores
the raw-source SHA-256 as `null` and raw byte count as `0`.

The gateway performs no reflection or coercion on an unrecognized thrown value.
It starts the Failure-normalization boundary after persisting its exact deadline
and node budget, then releases gateway and database locks. The isolated worker
owns the value and inspects it without invoking a getter, setter, `toJSON`,
iterator, callback, string coercion, or numeric coercion. The supervisor accepts
only the worker's canonical envelope or a supervisor-generated sentinel.

Each generated unsupported sentinel is exactly this object in this member order:

```json
{"kind":"unsupported","type":"<type>"}
```

`<type>` is exactly one member of this closed set: `undefined`, `bigint`,
`symbol`, `function`, `accessor`, `sparse-hole`, `cycle`, `exotic-object`,
`symbol-keyed-object`, `number-nan`, `number-positive-infinity`,
`number-negative-infinity`, `inspection-failure`, or `inspection-timeout`.
Sentinels are normalizer-owned and bypass source-string redaction. A source
object cannot impersonate one because each source string scalar is replaced by
its string-summary object.

The worker increments one visited-node counter for the root and for each array
position or object-property value before classification. If the next increment
would exceed 65,536, the supervisor terminates the worker, discards partial
output, and returns the root `inspection-timeout` sentinel. The supervisor does
the same at the persisted 30,000 ms deadline, including when a Proxy trap hangs.
A worker crash, a thrown Proxy trap, or a failed own-descriptor inspection
returns the root `inspection-failure` sentinel. The gateway does not retry or
inspect the original value after either supervisor-generated result.

The worker accepts `null`, Booleans, ECMAScript Number values, and strings as
supported scalars. It encodes each finite Number's actual IEEE-754 binary64
value with the RFC 8785 JSON Canonicalization Scheme number serialization;
negative zero encodes as `0`. A Number written above 2^53 therefore reflects
its binary64 value. A BigInt uses the `bigint` sentinel. `NaN`, positive
infinity, and negative infinity use their three closed number sentinels. The
worker applies the Terms well-formed-failure-string operation to every supported
string value before value redaction, UTF-8 byte counting, JSON emission,
truncation accounting, or a hash derived from the normalized value. This
operation does not rewrite separately supplied transient raw-source bytes or
their raw-source hash. The worker then replaces the well-formed value with
`{"redactedString":true,"utf8Bytes":<count>}`. That generated object uses
exactly the displayed member order and counts the well-formed value's UTF-8
bytes. No original string code unit reaches the envelope.

The worker treats only native arrays and objects whose prototype is exactly
`Object.prototype` or `null` as supported containers. It obtains own property
descriptors inside the killable boundary. An object with an own symbol key uses
the `symbol-keyed-object` sentinel. Another exotic container uses
`exotic-object`. For an ordinary object, the worker considers its enumerable
own string-keyed descriptors in Terms source-key order and never reads an
accessor. It does not apply the well-formed-failure-string operation to a source
key before ordering. A source key containing an unpaired surrogate cannot match
the preserved-name allowlist; the worker remaps it to its traversal-order
`$field<N>` name. Therefore replacement with U+FFFD cannot merge or reorder
emitted keys. For an ordinary array, the worker considers positions zero through
`length - 1` in order; a missing position uses `sparse-hole`, an accessor
position uses `accessor`, and any extra own string key other than `length` or a
canonical array index makes the whole array `exotic-object`.

Before it examines a descriptor's value, the worker applies the Terms ASCII
secret-name fold to a well-formed source key and compares the resulting
code-unit sequence exactly with `token`, `secret`, `password`, `authorization`,
`cookie`, `set-cookie`, `api-key`, `api_key`, `credential`, `private-key`, and
`private_key`. It applies no other case or normalization transform. An
ill-formed source key does not match. A match produces `[REDACTED]` without
traversing a data value or invoking an accessor. The same allowlist/remapping
rule still applies to that source key.
For another accessor it produces `accessor` without invoking the getter or
setter. For a data descriptor, it preserves only the source key names
`name`, `code`, `status`, `statusCode`, `exitCode`, `signal`, `timedOut`,
`cause`, `errors`, `details`, `kind`, and `type`; it replaces every other key
with `$field<N>` in traversal order and recursively normalizes the value.

The worker keeps an ancestor identity stack. A value that refers to an ancestor
uses `cycle`. A repeated reference that is not an ancestor is acyclic and is
encoded again by value. `undefined`, BigInt, Symbol, and Function values use
their respective sentinels. After this total normalization, the structural
encoder applies the existing depth, object-entry, array-member, and byte limits.

After secret redaction, the structural encoder walks the redacted value from a
root depth of zero. It retains the first 64 entries of each redacted object in the
worker's traversal order. When an object has more entries, the encoder appends
this reserved final property after those 64 entries:

```json
"$truncation":{"kind":"object-keys","omittedCount":N}
```

`N` is the redacted object's entry count minus 64. The encoder retains the first
32 members of each array. When an array has more members, it appends this
reserved final member after those 32 members:

```json
{"$truncation":{"kind":"array-members","omittedCount":N}}
```

`N` is the normalized array's member count minus 32. Descending through an object or
array member increments depth by one. Instead of descending into a container at
depth six, the encoder emits this object:

```json
{"$truncation":{"kind":"depth","omittedCount":N}}
```

For a cut object, `N` is its direct redacted-entry count. For a cut array, `N` is
its direct redacted-member count. The encoder applies the object and array caps
recursively to retained children. It owns each `$truncation` marker and does not
redact, rename, count, or cap the marker as source material. A source key named
`$truncation` cannot collide with a marker: that key is outside the allowlist,
so the worker maps it to the next `$field<N>` name before structural encoding.
The presence of at least one encoder-owned `$truncation` marker is the envelope's
truncation flag; the envelope contains no separate truncation Boolean.

The encoder serializes the structurally bounded redacted value as UTF-8 JSON
with no insignificant whitespace. It emits object members in the established
order. It emits `true`, `false`, and `null` as those lowercase literals, emits
each finite Number with the R-29 RFC 8785/JCS representation, escapes only
JSON control characters, quotation mark, and reverse solidus, and emits each
other Unicode scalar directly without normalization. This serialization is the
full canonical redacted envelope.

If the full canonical redacted envelope is at most 65,536 UTF-8 bytes, the
normalizer stores it unchanged as `unclassifiedEnvelope`. If it is larger, the
normalizer stores exactly this canonical object and no other member:

```json
{"$truncation":{"kind":"bytes","originalBytes":N,"sha256":"<lowercase-64-hex>"}}
```

`N` is the UTF-8 byte length of the full canonical redacted envelope before the
replacement. `sha256` is the lowercase hexadecimal SHA-256 of those complete
bytes. The encoded replacement, including braces and member syntax, must be at
most 65,536 UTF-8 bytes. The byte marker is encoder-owned, and its presence is
the truncation flag. The separate failure-material fields for the transient raw
source hash and raw byte count remain unchanged.

The normalizer never persists transient raw bytes, an original key name outside
the allowlist, or an original string scalar. It maps an unrecognized failure to
`internal_apply_failure` and stores its canonical bounded envelope without
assigning a more specific cause. The same input bytes and stage produce the
same code, safe message, retryability, raw hash, raw byte count, and envelope;
identifiers and capture time are the only varying fields. Public result, outcome, and event
projections expose only code, sanitized message, retryability, and
failure-material ID. Acceptance: AC-12, AC-17, and AC-23.

**R-30 — Result retrieval and self-apply.**
`tightbeam identity apply --operation <operationId>` performs no apply effect.
After the R-21 check, it returns the R-18 snapshot from durable rows. Acceptance
of an effect-form operation and transfer to the R-19 supervised executor commit
before the executor can cancel a selected caller's running turn. Specifically,
the R-05 acceptance transaction persists the generated operation ID and exact
`tightbeam identity apply --operation <operationId>` command inside the caller's
R-13 continuation intent, and the R-19 execution-owner claim commits, before its
per-session row can enter `interrupting`. This applies to keyed and unkeyed
effect requests. The caller's command response can end with that turn, but the
operation continues. R-12 materializes the intent after success or after it
restores a safe prior context for an interrupted failed caller row. Repeating the
query does not change the operation, create a prompt, or acquire a fence.
Once the recovery continuation is delivered, the same operation and key always
return the terminal `self_apply_retry_requires_new_operation` result; they never
enter R-16. A new effect uses a new key and operation ID. Acceptance: AC-24.

### Mechanism choice

This spec **adds** durable operation, per-session outcome, admission-fence, and
failure-material records because the explicit apply surface must survive
crashes, prevent turn admission, and leave named incident evidence. Deleting
apply loses the user-required rollout surface. Accepting unknown or duplicate
outcomes loses the user-required durable result and exactly-one continuation
guarantee. For overlapping effects, this spec instead **deletes** concurrency at
the per-session seam: a second operation records `apply_in_progress` and does no
effect. After delivery of an interrupted caller's recovery continuation, it also
**deletes** same-operation retry: another interruption would need a second
continuation with the same dedupe identity, so any further effect uses a new
operation and key.

The durable row is the source of operational truth. The executor performs the
effects. It does not ask an inference system to decide whether a prior apply
probably succeeded.

## Acceptance

Each check uses a disposable organization and disposable sessions. A test does
not manufacture malformed values on a live work row. Unit tests use controlled
adapters. The final smoke uses real CLI output, a real gateway, and real Codex
and Claude harness sessions.

**AC-01 — Self-locating conflict (R-01, I-01, I-13).** Given a disposable
identity tree with two conflicts, when an administrator runs
`tightbeam identity relearn`, then the JSON result equals the R-01 schema,
`resolutionRoot` is absolute, `conflictingPaths` contains the two absolute
paths in ascending order, `resolveCommand` equals
`tightbeam identity relearn --resolve`, and `tightbeam/live` remains on its
prior object ID.

**AC-02 — No automatic resolution (R-01, I-01).** Given the AC-01 conflicted
tree, when the command returns, then both files still contain Git conflict
stages, no merge-resolution commit exists, and neither organization content
nor shipped content was selected automatically. Given an administrator edits
both files and runs the exact returned command, when Git reports no unresolved
path, then the result publishes the resolved merge.

**AC-03 — Successful resolve projection (R-02, I-03).** Given a conflict that an
administrator resolves, when `identity relearn --resolve` publishes, then its
result contains the same stale-session, apply-command, and warning fields as a
clean successful relearn.

**AC-04 — Relearn lists but does not apply (R-02, R-03, I-03).** Given two
active sessions on the prior revision and one active session already on the
new revision, when relearn publishes, then `staleSessions` names only the two
prior-revision sessions in ascending order, `applyCommand` equals
`tightbeam identity apply --all`, and `applyWarning` equals R-02 byte for byte.
The three session stamps, harness contexts, turn rows, and transcript row counts
remain unchanged. Given no stale active session, the same result contains an
empty `staleSessions` array and `applyCommand: null`.

**AC-05 — Help contract (R-04, R-06).** Given the released CLI, when a caller
runs global help and `tightbeam identity apply --help`, then each output names
the one-session selector, `--all`, optional `--key`, read-only `--operation`
query, the exact R-02 warning, and the response-loss reason to use `--key`.

**AC-06 — One idle session (R-11, R-12, R-13, R-18, I-02, I-06, I-12).** Given
one idle active session on revision A and live revision B, when an administrator
runs keyed one-session apply, then the harness context reads guidance and skills
only from B, the session stamp becomes B, the workdir and history pointer stay
the same, one continuation prompt with both R-13 placeholders replaced by the
accepted operation ID is queued, and the R-18 result reports one success. For
Codex, the shared runtime PID stays the same.

**AC-07 — Running single session (R-08, R-09, R-13, I-04, I-05).** Given one
selected session with a held running turn, when keyed one-session apply reaches
that session, then the ledger records exactly one terminal state for the old
turn, apply does not return `turn_in_progress`, the harness reload begins
without waiting for natural model completion, no queued turn starts inside the
durable admission fence, and one R-13 continuation prompt exists after reload.
The result names the interrupted turn sequence and observed terminal outcome.

**AC-08 — Mixed fleet progress (R-07, R-10, R-11, R-18, I-04, I-09).** Given an
`--all` cohort containing an idle resident session, a running resident session,
a session with queued turns, a never-started session, and a session whose last
pointer is nonresident, when apply runs, then it freezes those five keys,
attempts each key, interrupts only the running turn, retains the queued turns,
establishes each successful harness context from the target revision, and
returns one ordered outcome per key. A session created after acceptance does not
appear in the operation.

**AC-09 — Durable-state preservation (R-12, R-13, R-27, I-07).** Given an idle
selected session with transcript, assignment, work-item, artifact, and wake
history, when apply succeeds, then each pre-apply row remains byte-for-byte
unchanged, the visible-history barrier is unchanged, and the only new
conversation rows are the one continuation prompt and its later model output.

**AC-10 — Duplicate and lost response (R-05, R-13, R-16, I-06).** Given a keyed
apply that succeeds but whose client loses the response, when the same principal
repeats the same byte-equal normalized effect request and key, then the gateway
returns the original operation ID and terminal result, performs no second
reset/reload, and finds one continuation prompt for that operation and session.
When that principal reuses the key with any unequal normalized effect request,
the gateway returns `idempotency_conflict` and changes neither operation.

**AC-11 — Crash matrix (R-05, R-14, R-15, I-06, I-08).** For a separate test at
each durable phase boundary, given the gateway stops after recording the phase
but before or after the bracketed external effect, when the gateway restarts,
then the gateway exposes no turn-admission or apply-executor path until one
adoption transaction has assigned every existing fence to the current
recovery-owner epoch. Every adopted outcome, fence, and nonmaterialized caller
intent contains that same epoch before the recovery executor resumes it. A
pre-adoption worker can neither invoke an adapter nor commit. A queued turn claim
released immediately after admission opens returns no claim while its durable
fence exists. Once the adapter returns a valid terminal receipt, recovery reaches
`succeeded` or a safe named `failed` outcome. Each terminal case leaves no
nonterminal old turn. A recovered success leaves one target revision stamp, one
continuation prompt, and no fence. A safe failed outcome leaves a runnable
context at the prior stamp, no continuation prompt for a non-caller, and no
fence. An interrupted selected caller receives its one staged recovery
continuation in that failure transaction; a caller that was not interrupted
does not. If prior-context safety is not yet established, the row and fence
remain nonterminal for automatic recovery. A crash after the R-12 transaction
commit returns the recorded success without redelivery.

Given reload has stored one succeeded target receipt and the first two R-12
atomic database transactions return defined storage rejections, then with a
fake database clock the first rejection appends one ordinal-zero
`post_reload_commit_unavailable` event whose `nextAttemptAt` is exactly 5,000
ms after observation, and the second appends one ordinal-one event whose
`nextAttemptAt` is exactly 10,000 ms after observation. Each rejection leaves
the same executable attempt `continuation-pending`, the prior revision stamp
unchanged, the target context active, the admission fence present, and no
continuation, terminal error, failure material, or admitted turn. Replaying
either scheduling transaction creates no duplicate event. A restart between
rejections adopts that same attempt, receipt, ordinal, and timestamp without an
adapter `invoke` or `status` call. When the third identical transaction commits,
it writes the target stamp, reload-success fact, one continuation, succeeded
outcome, and fence deletion together. Separate rejection fixtures verify the
remaining exact 20,000, 40,000, and 60,000 ms delays and the 60,000 ms cap. In
a crash fixture that exposes `continuation-pending` with no `nextAttemptAt`,
adoption appends ordinal zero once before another commit attempt.

For `runner-stop` and `reload` separately, a phase-boundary fixture records the
expected Terms effect ID before releasing the adapter. The fenced pre-effect
fixture records the prior runtime-context snapshot before it releases
runner-stop. If the process crashes before either invoke, recovery reads
`not_started` and invokes that same phase ID once. If runner-stop commits but its
response is lost, recovery reads `succeeded(result)`, advances to reload once,
and creates no second logical runner-stop. If reload commits but its response is
lost, recovery reads the closed reload receipt, commits the outcome once, and
makes no second logical replacement. The ID fixture changes an otherwise
ignored outcome ID and attempt number while holding operation, session,
creation epoch, and effect phase constant; the expected effect ID remains equal.
Changing only the effect phase from `runner-stop` to `reload` produces a
different expected ID. Changing only the creation epoch also produces a
different expected ID.

A crash immediately before the R-09 session-seam transaction leaves neither
`canceled` nor a runner-stop obligation. A crash immediately after its commit
leaves both. No fixture observes exactly one of those durable values. A crash
after runner-stop succeeds but before the reload effect record causes recovery
to consume that runner-stop receipt once and create one reload obligation from
the persisted prior snapshot; it neither reuses the runner-stop ID nor invents
a close phase.

After a runner-stop fixture returns `succeeded(result)`, atomic reload fixtures
inject failure while target staging validates, immediately before the switch,
and immediately after switch initiation. The first two return
`failed(class,priorContextId,priorRevision,runnable=true)` with
`class.effectDisposition: "terminal"` only after the exact prior context is
restarted and runnable. The third rolls back or restarts that exact prior
context before it returns the same closed failed shape. A rollback-failure
fixture returns `in_progress`, retains the fence, admits no turn, and keeps
recovering the same reload effect ID until the exact prior context is runnable;
only then may it return the closed failed shape. A nonresident-prior fixture uses
the stored restorable identity and returns the failed shape only after that
exact prior context is active and runnable. A success fixture returns
`succeeded(targetContextId,targetRevision,runnable=true)` with the target
context runnable. At each terminal receipt, a readback query finds exactly one
runnable context: the named target after success or the named prior context
after failure. No fixture returns a terminal receipt with neither or both
contexts runnable.

In separate readback fixtures, a retryable runner-stop `failed(class)` causes
one re-invoke with the same runner-stop effect ID, and a later
`succeeded(result)` advances to reload once. A retryable reload failed receipt
that names the active runnable prior context causes one re-invoke with the same
reload effect ID, and a later succeeded target receipt advances once. An
`in_progress` status for either phase schedules the ordinal-zero 5,000 ms status
recovery, releases the executor lease and database locks, and performs no
invoke; the next matching phase-specific succeeded status advances once.

In invalid retryable reload-receipt fixtures, a missing or different prior
context ID or revision records `recoveryCause: "context_mismatch"`; matching
identifiers with `runnable` missing or false record
`recoveryCause: "nonrunnable"`. The ordinal-zero transaction appends one
deduped `adapter_unavailable` event, retains the same nonterminal outcome,
fence, effect ID, and invalid receipt, sets `nextAttemptAt` exactly 5,000 ms
after observation, and releases the executor lease and database locks. It
performs no invoke, outcome commit, continuation delivery, fence deletion, or
turn admission. Held status-only polls verify exact later delays of 10,000,
20,000, 40,000, and 60,000 ms plus the 60,000 ms cap. A `not_started`,
`in_progress`, unavailable, repeated mismatch, or repeated nonrunnable result
in that substate schedules another status poll and never invokes. A matching
retryable receipt later authorizes exactly one same-ID invoke; a matching
succeeded or terminal failed receipt follows its normal one-time transition.
A status-call timeout and an unavailable observation each retain the durable
status-only marker, original invalid receipt, and typed recovery cause before
scheduling the next status poll; neither can fall through to the ordinary
`not_started` or retryable-failure invoke rule. A crash before the scheduling
transaction leaves no partial event or ordinal;
a crash after commit adopts the same substate, receipt, effect ID, ordinal, and
timestamp. Separate first-observation fixtures return invalid evidence once
from `invoke` and once from `status`; their event records the actual call kind,
and both enter the same status-only state. Replaying either observation creates
no duplicate event or call.

A terminal runner-stop failed fixture enters the safe
`turn_interruption_failed` transaction only when adapter readback matches the
stored prior context and revision with `runnable=true` and proves reload was not
invoked. A mismatched or nonrunnable readback records `adapter_unavailable`,
keeps the outcome and fence nonterminal, releases its executor lease and
database locks, and admits no turn.

A defined ledger CAS no-write failure before `interrupting` invokes no adapter,
leaves the original turn and prior context unchanged, deletes the unused caller
intent, commits `turn_interruption_failed`, and deletes the fence. A CAS result
that does not prove the no-write condition leaves the outcome and fence
nonterminal for recovery.

Two recovery workers released together observe one current executor lease; the
loser cannot invoke, consume status, or commit. A worker from the prior epoch
cannot consume a matching old-ID receipt after recovery adoption transfers the
stored obligation to the new owner epoch. The new owner can reconcile that
stored old-ID effect, but cannot use its receipt as proof of a new-epoch effect.

With a fake database clock and snapshotted `effectTimeoutMs: 30000`, separate
never-returning invoke and never-returning status fixtures for each effect phase
advance exactly 30,000 ms from the persisted call start. Each fixture records one `timed_out`
event and durable recovery obligation, releases the executor lease and database
locks, retains the fence, and sets the first `nextAttemptAt` exactly 5,000 ms
after the timeout observation. A transaction on an unrelated session commits
while that obligation waits. A direct response released after timeout can
represent a real late completion but changes no row directly; a later status
call under the same effect ID, immutable creation epoch, current owner epoch,
and current lease reads the durable receipt and is the only path that consumes
its result.

In an unavailable-adapter fixture, recovery ordinals zero through four schedule
exact delays of 5,000, 10,000, 20,000, 40,000, and 60,000 ms; each later ordinal
schedules 60,000 ms. Each attempt appends one deduped
`adapter_unavailable` event with the exact next-attempt timestamp and supervision
fields, releases its executor lease and database locks, and leaves one visible
nonterminal obligation plus fence. When the adapter becomes reachable and
returns a valid terminal receipt, that same effect ID reaches the applicable
terminal outcome without a duplicate effect or continuation.

In prior-context snapshot fixtures, acceptance reads only local registry
metadata and commits an outcome, fence, expected incarnation/generation, and
snapshot obligation without calling an adapter. A held snapshot call retains no
database lock: an unrelated-session transaction commits while it waits. With a
fake database clock, a never-returning call reaches its persisted 30,000 ms
deadline, the supervisor terminates it, and one ordinal-zero
`prior_context_snapshot_unavailable` event records `nextAttemptAt` exactly 5,000
ms later. Unreachable-adapter and worker-crash fixtures retain the nonterminal
outcome and fence, release the lease and locks, dedupe the event by ordinal, and
verify the remaining exact 10,000, 20,000, 40,000, and 60,000 ms delays plus the
60,000 ms cap. Recovery invokes only the read-only snapshot until one succeeds.

A successful snapshot fixture returns the exact prior context, session
incarnation, and adapter configuration/generation. The locked pre-effect
transaction revalidates those values, revision order, and fence ownership, then
stores the snapshot and first effect obligation together. A barrier exposes no
effect call before that commit. In one mismatch fixture, the first locked check
observes a changed generation, discards the snapshot, records generation-retry
count one, and creates no effect; a second snapshot with the refreshed token
commits one first effect obligation. In another fixture, both snapshots mismatch;
the second locked check commits `internal_apply_failure` and material, deletes
the fence and unused caller intent, and leaves the turn, session stamp, harness
context, transcript, and continuation unchanged. No stale snapshot produces an
adapter effect.

Given a selected session whose runner-stop adapter lacks coalescing or readback,
whose registry metadata lacks read-only snapshot capability, or whose
runtime-context reload adapter lacks coalescing, readback, target staging,
atomic switching, or exact prior-context rollback/restart, apply
returns the exact R-29
`adapter_effect_recovery_unsupported` error for the first unsupported session
and creates none of the rows or effects enumerated there.

**AC-12 — Partial failure and retry (R-12, R-16, R-18, R-19, R-23, R-24,
I-09).** Given three selected sessions whose adapters return success, a
`harness_reload_failed` response, and a held nonterminal result, when the second
session fails and the third is still nonterminal, then the administrator's same
keyed request returns the exact R-16 `apply_cohort_in_progress` error, exits
nonzero, and writes no retry fact. When the third session is released and the
first attempt completes successfully for it, then the result outcome is
`partial`, `applied` names two sessions, `failed` names one session, the failure
equals the R-29 code, message, retryability, and material-ID shape, the CLI exits
nonzero, and the third session was attempted after the second failed.
`identity status` reports the failed session stale. After correcting the failed
adapter, the same keyed request retries only the failed row, the final result is
`succeeded`, and each session has one continuation prompt for the operation.

**AC-13 — Turn and operation races (R-08, R-09, R-10, R-17, I-05).** Given a
turn becomes claimable while apply acquires the session seam, when the race is
released in both possible mailbox orders, then either the turn terminalizes
before apply starts or apply cancels it through the ledger CAS. No turn runs
during reset/reload. Given operation X owns the session fence when operation Y
selects the same session, Y records retryable `apply_in_progress`, performs no
harness effect, queues no continuation, and retains its own target and dedupe
identity. No fleet-wide lock prevents an unrelated selected session from
progressing.

**AC-14 — Publication during apply (R-07, R-17, R-24, I-02).** Given operation
X captures live revision B and a later relearn publishes C while X is in
progress, when X completes, then each X success uses only B and records B. The
result still names B. `identity status` reports those sessions stale against C.
A new operation can then apply C.

**AC-15 — Authorization and provenance (R-20, R-21, R-22, R-23, I-10, I-11).**
Given a non-administrator principal, when it requests relearn or apply, then the
gateway returns `forbidden` and creates no operation, event, prompt, Git change,
or session change. The same principal receives `forbidden` for an operation
query. Given an administrator-owned agent requests apply, the operation, events,
and continuation cause metadata name that agent as request principal and
`process:tightbeam` as continuation sender. Given an unknown or retired
single-session key, apply returns `not_found` before operation creation.

**AC-16 — Migration and command compatibility (R-25, R-26).** Given a copy of a
pre-release organization database with sessions, turns, transcript, assignment,
and work-item history, when the new release migrates it, then those rows and
counts remain unchanged; the new operation, outcome, fence, and failure-material
stores are empty; and the four R-25 unique constraints exist. The old
one-session and `--all` command forms parse. Their success results retain
`applied` as an array and `identityRevision` as a string. The new read-only
operation-query form parses only without a selector or `--key`.

**AC-17 — Observability and data boundary (R-22, R-23, I-10, I-13).** Given a
successful apply and a partial apply, when an operator reads the durable event
stream, then it can reconstruct operation acceptance, per-session phases,
retries, error codes, failure-material IDs, and completion from operation IDs and
session keys. No event contains an R-29 source envelope, identity file contents,
transcript contents, credentials, raw adapter messages, stack traces, response
bodies, or harness tokens. Repeated reads return the same event order and result
order.

**AC-18 — Real workflow smoke (R-04, R-06, R-26, R-27).** Given a disposable
organization using the released CLI and gateway, one real Codex session, and one
real Claude session, when a real shipped Kung Fu change is relearned and applied
with `--all`, then captured command output matches R-02 and R-18, both harness
sessions resume through the exact R-13 prompt, each transcript retains its
pre-apply messages, and each session runs its next turn with the target identity
revision. The test fixture is captured from these real responses. It is not a
handwritten ideal response.

**AC-19 — Operating guidance boundary (R-28).** Given the released identity
content and manual plus the released CLI, when a reviewer searches for this
workflow, then the exact warning and publish-inspect-apply-inspect sequence
exist in CLI help and successful-relearn output. No identity seed or manual file
changes solely to repeat that sequence.

**AC-20 — Retirement after selection and retry (R-07, R-08, R-16, R-29, I-05,
I-14).** Given an active session and synchronized apply-acceptance and retirement transactions, when the
test releases retirement first, then retirement commits, one-session apply
returns `not_found`, and `--all` excludes the retired key. When the test releases
apply acceptance first, then its operation, outcome, and fence commit together;
retirement cannot commit while the fence exists; apply reaches a safe terminal
commit; and retirement commits afterward. Neither ordering reloads or resumes a
retired session.

Given a retryable failed row and synchronized R-16 retry-admission and retirement
transactions, when retirement wins the shared session-row lock, then the row
and its attempt number remain byte-for-byte unchanged, one append-only
`session_retired` retry-admission result commits, and no new outcome, fence,
execution owner, caller intent, interruption, or harness effect exists. A lost
response replay returns the same unchanged terminal projection, and the event
history query returns that same fact with no duplicate. When retry
admission wins, it appends a new pending outcome and atomically commits that
outcome, its fence, new execution-owner epoch, and applicable caller intent; the
prior terminal outcome remains unchanged, and retirement commits only after the
new fenced attempt reaches a safe terminal outcome.

**AC-21 — Atomic keyed acceptance (R-05, R-07, R-25).** Given no prior fence and
two connections from one principal that use the same new key and byte-equal
normalized effect request, when a barrier releases both acceptance transactions
together, then both receive the same operation ID and the database contains one
key binding with that full normalized request, one operation, one frozen cohort,
one fence per selected session, and at most one eventual continuation per
operation/session. No intermediate binding is visible without its operation and
cohort. Given the same race with any unequal normalized effect request, one full
request binds the key and the other returns `idempotency_conflict` without a
second operation.

**AC-22 — Cross-revision apply order and retry-epoch barrier (R-16, R-17,
I-14).** Given operation X targets B and owns a session fence while a later
operation Y targets descendant C, then Y first records retryable
`apply_in_progress`. After X reaches a safe terminal commit, and after every row
in Y's current execution cohort is terminal, Y retry admission atomically
acquires its fence, assigns a new execution-owner epoch, and appends a pending
executable-attempt row with any required caller intent; Y then applies C and
queues one Y continuation. Y's prior terminal row remains unchanged.

In initial-admission fixtures, a session already on descendant C and a session
whose required revision object is unavailable produce respectively terminal
`apply_superseded` and `identity_revision_unavailable` outcomes in the R-05
transaction. Each outcome has its failure material and has no fence, executor,
caller intent, phase, effect ID, effect, or continuation. In pre-effect
invalidation fixtures, admission first acquires a fence for a valid target, then
the locked R-17 recheck observes those same two invalid conditions. The recheck
transaction records the applicable terminal outcome and material, deletes the
fence and unused intent, and commits no effect phase or obligation. A turn claim
released after that commit observes no fence and no apply effect occurred.

In a mixed-cohort barrier test, given Y epoch E1 has nonterminal running row A
and terminal retryable failed row B, when the administrator repeats Y's keyed
request, then the gateway returns the exact R-16 `apply_cohort_in_progress`
error. The operation remains at E1; B remains terminal; and no epoch increment,
new outcome, B fence, executor claim, caller intent, continuation fact, retry
event, or failure material exists. After A terminalizes, the same request can
commit retry admission at E2 and atomically bind B's new attempt row, fence,
executor claim, and any applicable caller intent to E2. The operation records
that new row as the E2 execution cohort and
preserves the terminal A and B E1 rows byte-for-byte. At that commit no cohort
row has an active E1 executor.

In a terminalization race, the E1 terminal transaction and retry admission both
lock the operation row. If retry observes A nonterminal first, it returns the
fixed error with no write and A then terminalizes at E1. If A terminalizes
first, retry observes the wholly terminal E1 cohort and can atomically admit E2.
No other ordering or partial E2 state is observable. In a crash-recovery test,
recovery adoption assigns every nonterminal E1 row the same new recovery epoch
before admission opens; a concurrent retry still returns the fixed error until
those adopted rows terminalize and cannot create an additional epoch or
executor. At every observation point, at most one execution cohort contains a
nonterminal outcome.

In a separate stale-worker barrier test, given a retryable Y failure is terminal
at epoch E1 and retry admission commits E2, when the delayed E1 worker is
released immediately before and immediately after the E2 commit, then terminal
phase state blocks it before the commit and the epoch mismatch blocks it after
the commit; only E2 can produce an adapter call or result.

In classified-only fixtures, retirement, a blocking fence, a newer descendant
session revision, and an unrelated or unreadable revision append respectively
`session_retired`, `apply_in_progress`, `apply_superseded`, and
`identity_revision_unavailable` retry-admission results. Each fixture leaves the
terminal outcome, error/retryability projection, epoch, and attempt number
byte-for-byte unchanged and creates no new outcome, fence, executor, intent,
effect, or continuation. The event fact stores the prior cohort/epoch, requested
and current revisions, source executable-outcome ID, principal, controlled
cause, classification, retryability, and material ID. A crash before the atomic
fact transaction commits leaves no event, material, retry-attempt ordinal, or
new operation epoch; the replay commits exactly one of each. After a crash
immediately after fact commit but before response, the same request returns the
unchanged terminal application projection; the event-history query returns the
fact with the same retry attempt, epoch, classification, and material ID and
creates no duplicate. Concurrent identical requests serialize on the operation
lock. The event ID is the deterministic function of the Terms unique key, and
the existing event-ID constraint permits one event fact for that key.
When an `apply_in_progress` fence later disappears, one new retry attempt may
pass the prior classified-only epoch's empty-cohort terminal check and append
the executable outcome; nonretryable classifications never do. The final
session stamp and harness context remain at the newest accepted revision.

**AC-23 — Error taxonomy and durable material (R-14, R-16, R-18, R-23, R-29).**
For every executable-attempt condition in R-29 and for fixtures that make later
conditions coexist with an earlier one, given a controlled adapter or policy
condition, when the attempt fails, then its R-18 result and event use the first
matching table row's exact code, message, and retryability and name one
immutable failure-material row. For each R-16 classified-only condition
(`session_retired`, `apply_in_progress`, `apply_superseded`, and
`identity_revision_unavailable`), the retry-admission event and linked material
use that exact classification; the terminal R-18 outcome, public error,
retryability, epoch, and attempt counter remain byte-for-byte unchanged. Given
an unknown adapter failure containing credentials in headers, body, message,
stack, stdout, and stderr, then the result uses `internal_apply_failure`; the
durable material contains the raw-byte hash and count plus only the R-29
canonical bounded envelope; all secret-key values are `[REDACTED]` in the full
redacted envelope; original string scalars and unrecognized key names are
absent. Public outcome and event rows contain only the exact code, sanitized
message, retryability, and material ID as error fields.

The following fixtures verify the canonical envelope exactly:

- For byte boundaries, let `E0` be the canonical JSON number `0`; let `E1` be
  an array of 32 copies of `E0`; let `E2` be an array of 32 copies of `E1`; and
  let `B` be an array of 31 copies of `E2`. `B` is 65,535 UTF-8 bytes and is
  stored unchanged. Replacing its first `0` with `10` produces 65,536 bytes and
  is stored unchanged. Replacing that first `0` with `100` produces 65,537
  bytes and stores exactly
  `{"$truncation":{"kind":"bytes","originalBytes":65537,"sha256":"4c21079ce5167abd0116f92cce75038dbcfc13840b30378921b6444cf3930f3a"}}`.
  The stored replacement is 130 UTF-8 bytes. Recomputing SHA-256 over the full
  65,537-byte envelope yields the marker value; hashing the replacement does
  not.
- A constructed ECMAScript source object whose `details` data value is the lone
  high surrogate `"\uD800"`, the lone low surrogate `"\uDC00"`, or the literal
  replacement scalar `"\uFFFD"` produces the same 49-byte envelope
  `{"details":{"redactedString":true,"utf8Bytes":3}}`. Its lowercase
  SHA-256 is
  `21c7a82b953de3df9b2d8fcfdc11d443cba256222556c9afd044e1dc510aaf98`.
  A valid `"\uD83D\uDE00"` pair produces the 49-byte envelope with
  `utf8Bytes:4` and SHA-256
  `774ec72add7e54cf96c6ad1a7df6c16ad8b7c94313787e53ed474e438c033b82`.
  The mixed value `"\uD800A\uDC00"` produces the 49-byte envelope with
  `utf8Bytes:7` and SHA-256
  `5d0c66ce2fdfbbed348c0714a4018bb47123e937533f150624a34170897d18a7`.
- The well-formed source value `{"details":"é😀"}` produces
  `{"details":{"redactedString":true,"utf8Bytes":6}}`. The canonically
  distinct source value `{"details":"e\u0301😀"}` produces
  `{"details":{"redactedString":true,"utf8Bytes":7}}`. The encoder persists
  neither source string and performs no normalization beyond replacement of
  unpaired surrogates.
- Let `L` be `"\uD800".repeat(21845)`. The `details` values `L`, `L + "A"`,
  and `L + "AB"` produce respective `utf8Bytes` counts 65,535, 65,536, and
  65,537. Their three canonical 53-byte envelopes have respective SHA-256
  values `461c131d949f78a88015494ea4ed27aaf63a026602317176e5cb7ccf8c3164be`,
  `02ee512db330168d0e8bc00232fbb551f150143f1bee763d075633cfd79417e3`,
  and `bc54de0cd68f63c564d03a25b94d70ff8524ec3820d9affdcbf7c371a52e2886`.
  Source-value size does not trigger the envelope fallback; the canonical
  redacted envelope size does.
- Replacing the first `E0` in the preceding `B` fixture with the normalized
  summary for `"\uD800A\uDC00"` produces a 65,571-byte full envelope and stores
  exactly
  `{"$truncation":{"kind":"bytes","originalBytes":65571,"sha256":"0d9a0d570d0bc6a9f78a16761cb751d6a2b2cc241a61262976f2d584d9a4af9d"}}`.
  The hash is over that full envelope after `toWellFormed` semantics and before
  byte fallback.
- A constructed object with own data properties `"code"` to `0`,
  `"code\uD800"` to `1`, `"\uD800"` to `2`, `"\uD83D\uDE00"` to `3`,
  `"\uDC00"` to `4`, and `"\uFFFD"` to `5` sorts in that displayed unsigned
  UTF-16 order and produces exactly
  `{"code":0,"$field0":1,"$field1":2,"$field2":3,"$field3":4,"$field4":5}`.
  That 70-byte envelope has SHA-256
  `023a9316f1cfb06509e07763ff284aecb8f9024349d1320161624d0264017142`.
  Each permutation of property insertion order produces the same bytes; each
  of the three ill-formed keys is remapped rather than allowlisted.
- V8 and JavaScriptCore conformance runners execute each surrogate, key,
  boundary, and hash fixture twice. Each run produces the exact bytes, counts,
  ordering, and lowercase SHA-256 values above.
- The source object `{"$truncation":0,"code":1}` produces
  `{"$field0":0,"code":1}` and has no truncation flag. The source key cannot
  overwrite or impersonate an encoder-owned marker.
- A source object with keys `k00` through `k64`, in that byte-sort order and
  with respective numeric values `0` through `64`, retains `$field0` through
  `$field63` with values `0` through `63`, then appends the final property
  `"$truncation":{"kind":"object-keys","omittedCount":1}`.
- A source array containing the numbers `0` through `32` retains `0` through
  `31`, then appends
  `{"$truncation":{"kind":"array-members","omittedCount":1}}`.
- With root depth zero, `[[[[[[[0,1]]]]]]]` produces
  `[[[[[[{"$truncation":{"kind":"depth","omittedCount":2}}]]]]]]`.

The following fixtures verify the total normalization boundary exactly:

- A worker fixture supplies, in order, `undefined`, a BigInt, a Symbol, a
  Function, a nonsecret accessor descriptor, and a sparse array hole. Each
  position produces the fixed two-member sentinel with respective `type`
  `undefined`, `bigint`, `symbol`, `function`, `accessor`, and `sparse-hole`;
  no callback or accessor runs.
- A Number fixture containing `-0`, `9007199254740992`, the Number literal
  `9007199254740993`, BigInt `9007199254740993n`, `NaN`, positive infinity,
  and negative infinity produces exactly
  `[0,9007199254740992,9007199254740992,{"kind":"unsupported","type":"bigint"},{"kind":"unsupported","type":"number-nan"},{"kind":"unsupported","type":"number-positive-infinity"},{"kind":"unsupported","type":"number-negative-infinity"}]`.
  Separate RFC 8785 fixtures encode `1e30`, `1e-7`, and `0.000001` as
  `1e+30`, `1e-7`, and `0.000001`.
- Separate source objects with throwing getters under `token`, `TOKEN`, and
  `ToKeN` each produce `{"$field0":"[REDACTED]"}` and leave the getter-call
  counter at zero. Their ASCII secret-name fold is exactly `token`. Separate
  source objects with throwing getters under `Authorization`, `Set-Cookie`,
  `API_KEY`, and `Private-Key` each produce
  `{"$field0":"[REDACTED]"}` and leave the getter-call counter at zero. Their
  ASCII secret-name folds are exactly `authorization`, `set-cookie`, `api_key`,
  and `private-key`, respectively. V8 and JavaScriptCore produce those same
  four redacted envelopes without invoking an accessor. Throwing getters under
  `"\u017Fecret"`,
  `"\uFF34\uFF2F\uFF2B\uFF25\uFF2E"`, `"\u0130oken"`, and `"\u0131oken"`
  each produce
  `{"$field0":{"kind":"unsupported","type":"accessor"}}` and leave the
  getter-call counter at zero. The fold leaves every non-ASCII code unit in
  those four keys unchanged, so none matches an ASCII secret name in V8 or
  JavaScriptCore. The same getter under source key `details` produces
  `{"details":{"kind":"unsupported","type":"accessor"}}` and also leaves
  the counter at zero. The same getter under ill-formed key `"token\uD800"`
  produces
  `{"$field0":{"kind":"unsupported","type":"accessor"}}`: the key is
  remapped, the secret-name comparison does not accept the ill-formed suffix,
  and the getter-call counter remains zero. `toJSON`, iterator, and setter
  counters likewise remain zero in their fixtures.
- A hostile Proxy whose own-key trap does not return is terminated exactly at
  the persisted 30,000 ms fake-clock deadline and produces the root
  `inspection-timeout` sentinel. A 65,537th visited-node attempt produces that
  same root sentinel. A throwing trap and a killed worker each produce the root
  `inspection-failure` sentinel. The supervisor returns no partial envelope,
  and an unrelated database transaction commits while each worker is held.
- A Date or another unsupported prototype produces `exotic-object`; an object
  with an own Symbol key produces `symbol-keyed-object`. Neither fixture invokes
  a coercion method.
- For `a = {}; a.self = a`, normalization produces
  `{"$field0":{"kind":"unsupported","type":"cycle"}}`. For
  `x = {code:7}; {cause:x,details:x}`, normalization produces
  `{"cause":{"code":7},"details":{"code":7}}`, proving that a shared
  acyclic reference encodes twice by value.

Each structural fixture treats marker presence as the truncation flag. Two runs
over each ordinary, sentinel, timeout, failure, cyclic, and shared-reference
source with the same stage produce equal projected material except for ID and
capture time.

**AC-24 — Administrator-agent self-apply (R-04, R-06, R-12, R-13, R-16, R-18,
R-19, R-21, R-29, R-30, I-06, I-15).** Given an administrator-owned agent with a running turn invokes
keyed and unkeyed `identity apply --all` in separate tests and its own session is
selected, when acceptance commits but the interruption barrier remains held,
then the operation, generated or caller key, cohort, outcome rows, acquired
fences, and caller continuation intent already exist. That non-claimable intent
contains the accepted operation ID twice and the exact R-30 query command. The
supervised executor's durable execution-owner epoch also exists before the
barrier can release the row into `interrupting`. The effect command may lose its
response, but every selected session continues to a durable outcome. On success,
or on failure after a safe prior-context restore, exactly one interrupted-caller
continuation materializes and retrieves the current or final R-18 snapshot. A
failed caller row that never entered `interrupting` deletes its unused intent
and queues no recovery continuation. A repeated query and continuation delivery
create no second operation, reload, or prompt.

Given a retryable failed caller row whose prior attempt did not materialize a
continuation, when the same agent repeats the same key, then one R-16 transaction
commits the active-session check, fence, new execution-owner epoch, new pending
outcome, and exactly one operation/session/epoch intent before interruption;
the prior terminal outcome and attempt number remain unchanged. Given a
selected caller is interrupted and the attempt safely fails, then its recovery
continuation materializes once and the row reports nonretryable
`self_apply_retry_requires_new_operation`. After that operation completes,
repeating the same key returns the entire frozen operation unchanged: no cohort
row receives a fence, executor, interruption, reload, or prompt. When the agent
submits the same selector with a new key, a new operation can succeed and deliver
its own one continuation.

Given that self-apply failure has already set
`retryAdmissionBlockedBySession` while another current-cohort row remains
nonterminal, a same-key replay returns exact `apply_cohort_in_progress` and
writes no retry fact. Only after that row terminalizes does replay honor the
block, return the completed unchanged operation with
`self_apply_retry_requires_new_operation`, and require a new key.

## Open Questions

None. Current owner assignment
`asg_bc9984d7-d4e4-424d-806b-4e33626105d5` resolves the formerly open
behavior through ruling `att_20acd607-7d1c-4a96-9d10-571772476df1`: apply
interrupts running turns, reset/reloads selected sessions, queues one post-reload
continuation after success, stages caller recovery before self-interruption, and
reports durable per-session outcomes. Ruling
`att_d85f9a36-4b79-4dd6-bff7-2a12a403c061` resolves retry admission,
retirement linearization, execution epochs, and new-operation-only retry after a
delivered self-apply recovery continuation.
