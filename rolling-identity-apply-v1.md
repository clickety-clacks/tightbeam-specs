# Rolling identity apply — v1

**Status:** Candidate for independent exact-revision review.

**Work item:** `wi_ff222e95-ecd4-4ba0-83cc-ddd9e2301e07`

**Observed source bases:** Tightbeam `0.1.9` at
`c3299e3a75dab21ed2839822d8ad207514f92782` and Tightbeam `main` at
`3e1dc56e1bd27854487228c05f4b2e1c9dd4fb22` on 2026-09-02.

**Authority and scope:** This specification replaces only the apply behavior in
`served-identity-home-projection-v1.md` section 9 and the apply-operation design
in `relearn-and-identity-apply-workflow.md`. The identity Git publication model,
single-revision projection, explicit administrator election, per-session cwd,
same-workdir/history preservation, shared-runtime boundary, and relearn conflict
behavior remain authoritative. This replacement removes running-turn
interruption, runner-stop, and continuation-prompt machinery. It applies to the
`0.1.9` maintenance line and `main` with one behavior and wire contract.

## Goal

Make an explicit identity rollout converge without an organization-wide quiet
period. The gateway accepts one immutable target revision and one frozen session
set, then advances each session at that session's next safe turn boundary. A
running turn finishes normally. Later queued turns wait behind the accepted
apply gate. One busy or failed session does not block another session.

Make incomplete rollout visible through durable operation results, identity
status, doctor, and a deduplicated stale-version alarm. Preserve a runnable
prior identity whenever target replacement fails.

## Non-Goals

- Relearn and identity edit do not apply a revision automatically.
- Apply does not cancel, replay, resume, or manufacture a model turn.
- Apply does not roll back external effects from a model turn.
- Apply does not restart a shared Codex runtime or another session.
- Apply does not choose whether an administrator should publish or roll out an
  identity revision.
- This specification does not change identity composition, archetype election,
  credentials, adapters outside the named replace/status contract, or host
  placement.
- This specification does not make an ancestor revision current. An intentional
  content rollback is a new descendant identity commit that reverts content,
  followed by a new apply operation.

## Terms

- **Live revision:** The immutable Git object ID at `tightbeam/live`.
- **Recorded revision:** The `identityRevision` on one active session. `NULL` is
  a recorded missing revision.
- **Stale session:** An active session whose recorded revision, render contract,
  or guidance digest differs from the snapshot at the live revision.
- **Apply operation:** One durable administrator request with one frozen target
  revision and one frozen set of active session keys.
- **Apply target:** The durable per-session member of an apply operation.
- **Apply gate:** A durable row unique by active session key. A gate permits the
  turn that was already `running` when the gate committed to reach one terminal
  state. It prevents every later turn claim and conflicting session mutation
  until the target reaches a safe terminal state.
- **Session boundary:** Durable proof that no turn for that session has status
  `running`. It is not a sample of organization-wide activity and it is not an
  in-memory lane observation.
- **Target snapshot:** Guidance, elected Tightbeam-owned skills, revision,
  render contract, and guidance digest read from one target revision.
- **Prior snapshot:** The recorded revision and render stamps, the exact
  Tightbeam-owned materialized-skill projection, the session pointer and
  incarnation, the adapter generation, the workdir, and the runnable runtime
  context identity observed before replacement.
- **Replace effect:** One adapter operation that stages the target context,
  changes only the selected session's runtime context, and can authoritatively
  report either one runnable target context or one restored runnable prior
  context.
- **Request principal:** The authenticated administrator user or
  administrator-owned agent that accepted the operation.
- **Acting principal:** The authenticated principal or `process:tightbeam`
  actor that performed a recorded transition.
- **Cause:** A closed machine-readable value that explains why a transition or
  marker occurred. Free text is not a cause.
- **Rollout alarm episode:** The durable interval during which at least one
  active session is stale against one live revision.

## Assumptions

1. The turn ledger changes a turn from queued to running in one transaction and
   gives each accepted turn exactly one terminal state.
2. Turn claim, session retirement, tune/repoint, and apply acceptance can lock
   the same session row and inspect the apply gate in that transaction.
3. Each line can add additive SQLite tables, constraints, and indexes without
   rewriting an existing session, turn, transcript, assignment, or work-item
   row.
4. The existing adapter coordinator limits session load work to three
   concurrent load slots per host.
5. Codex and Claude can reload a selected session on the same workdir and
   durable history without restarting a shared runtime.
6. The gateway can resolve the authenticated caller to an administrator user or
   administrator-owned session before it invokes the identity handler.
7. The exact-version CLI and gateway ship together on both pre-1.0 lines.

## Invariants

**I-01 — No global boundary.** An apply operation never waits for, tests, or
requires the absence of running turns outside the selected session. A running
selected session delays only its own target.

**I-02 — No turn interruption.** Apply never changes a running turn's state and
never signals its runner. The current turn finishes under the prior identity.

**I-03 — Gate before wait.** Acceptance commits the operation, each admitted
target, and its apply gate before it returns. A later turn claim checks the gate
in the same transaction that would claim the turn.

**I-04 — One immutable revision.** One operation and every target snapshot use
the target revision captured at acceptance. Guidance, skills, render contract,
digest, and stamp never straddle revisions.

**I-05 — Safe release.** A target gate is removed only with a terminal success,
a no-effect terminal refusal, or proof that the exact prior projection and
runtime context are again authoritative and runnable. An unknown or unsafe
external outcome keeps the gate and enters recovery.

**I-06 — No downgrade.** Apply does not replace a recorded revision with its Git
ancestor or with an unrelated revision. A stale worker cannot replace a revision
accepted by a later operation.

**I-07 — Per-session isolation.** Apply changes only the selected session's
Tightbeam-owned skill namespace, instruction snapshot, revision stamps, and
runtime context. It preserves the session key, workdir, durable transcript,
history pointer, assignments, work items, credentials, product-owned files, and
the shared runtime process.

**I-08 — Bounded execution.** Replace and projection work consumes the existing
host load semaphore. At most three targets per host perform preparation,
replacement, rollback, or recovery I/O concurrently. No database lock or lane
mailbox is held during adapter or filesystem I/O.

**I-09 — Durable recovery.** Each external effect has one deterministic effect
ID and a durable status contract. A timeout, disconnect, process crash, or lost
response causes status reconciliation, not a blind new effect.

**I-10 — Partial progress.** A waiting, failed, or recovering target does not
prevent another selected session from reaching a terminal result.

**I-11 — Explicit human choice.** The substrate computes revision relations,
stale sets, safe boundaries, effect status, and results. It never infers that an
identity should be published, applied, retried as a new operation, or rolled
back. Every such choice remains an administrator command.

**I-12 — Accountable evidence.** Every operation, target transition, refusal,
recovery observation, and alarm marker records a cause, request principal, and
acting principal. Public and durable evidence contains no identity content,
transcript content, raw adapter envelope, stack trace, credential, token, or
secret-bearing environment value.

## Architecture

### Current defect and elected mechanism

On both observed source bases, `identity apply --all` first gathers every
selected session with a durable running turn and returns one
`turn_in_progress` refusal for the whole cohort. The one-session path invokes
`SessionLane.at_turn_boundary/2` synchronously and returns the same refusal when
that target is running. An administrator agent that selects itself runs the
command inside the very turn whose boundary the command needs. Repeating the
command cannot change that fact.

The elected mechanism is durable acceptance followed by per-session rolling
execution. The apply gate is the serialization point. `--all` is a frozen set of
independent targets, not one atomic fleet effect. The request returns after the
acceptance transaction and never waits for completion.

The durable incident record is work item
`wi_ff222e95-ecd4-4ba0-83cc-ddd9e2301e07`: 258 of 327 active sessions were
stale, including 250 on revision `3a8f3bc9a4dea76d1e7d0ea73df42af0dbdd95f3`
and eight with no revision, while live was
`2e12888fecaf6e34b2a1fbdb259bb8afa60c08f8`. Attest
`att_864fed42-a14e-43b0-94f4-5df4f0038ecf` records both all-session and
single-session `turn_in_progress` refusals. Attest
`att_c65de4bc-1925-4804-a657-da41c3c64726` records the associated zero-effect
effort request refusing both actions because the stale assignment had no
liveness trigger.

The source seam is the same on both lines: `identity_apply_sessions` performs a
whole-selection running check, `identity_apply_at_boundary` rejects the set,
and `identity_apply_at_lane` synchronously calls
`SessionLane.at_turn_boundary/2`. The relevant observed locations are
`lib/tightbeam/gateway.ex:4198-4306` on main and
`lib/tightbeam/gateway.ex:3094-3202` on `0.1.9`.

### Requirements

**R-01 — Command and response.** Both lines shall accept these forms:

```text
tightbeam identity apply (<session> | --all) [--key <idempotency-key>]
tightbeam identity apply --operation <operation-id>
```

The effect form returns immediately after R-03 commits. It shall not poll. Its
result has this shape, with arrays in ascending session-key order:

```json
{
  "state": "running",
  "outcome": null,
  "operationId": "iap_<id>",
  "identityRevision": "<target-oid>",
  "selector": {"kind": "all", "sessionKey": null},
  "requestedBy": "session:agent:product-owner:example",
  "applied": [],
  "waiting": ["agent:coder:one"],
  "failed": []
}
```

`applied` and `identityRevision` retain their existing names and types.
`--operation` is read-only and returns the same operation's current durable
projection. It is mutually exclusive with a selector and `--key`.

**R-02 — Idempotency.** `--key` shall bind the request principal, verb, key, and
canonical selector in one unique transaction. The canonical selector is exactly
`{"kind":"all","sessionKey":null}` or
`{"kind":"session","sessionKey":"<exact-key>"}`. The target revision is
captured only by the winning transaction. Repeating the same binding returns the
same operation. Reusing the key with another selector returns
`idempotency_conflict` and the remedy `Use a new --key for the different
selector.` An unkeyed request creates a unique operation and generated key.

**R-03 — Atomic acceptance.** The acceptance transaction shall authenticate
R-15, capture the live revision, freeze active selected sessions, lock their
session rows in ascending key order, create the operation and one target per
frozen session, and acquire one apply gate per admitted target. It shall then
commit before execution starts. A one-session selector that is absent or
retired returns `not_found` with the remedy `Run tightbeam identity status and
select an active session.` It creates no operation.

For `--all`, a session that retires before its row lock is excluded. A session
created after the transaction is not selected. A target whose gate is already
owned by another operation records terminal `apply_in_progress`; it does not
abort other targets.

**R-04 — Turn-claim order.** Turn claim and apply acceptance shall lock the same
session row. If claim commits first, that turn may finish and the accepted gate
blocks the following claim. If the gate commits first, claim leaves the turn
queued. The terminal-turn path shall notify the apply reconciler before it asks
the lane to claim more work. The lane and the periodic reconciler shall process
an eligible apply gate before another queued turn for that session.

**R-05 — Per-target state machine.** Each target shall have exactly these
states and transitions:

```text
waiting_boundary -> preparing -> switching -> commit_pending -> succeeded
                                 |       |
                                 |       +-> rolling_back -> failed
                                 +----------> recovery_required
recovery_required -> switching | commit_pending | rolling_back
waiting_boundary | preparing -> superseded | failed
```

`succeeded`, `failed`, and `superseded` are terminal. `recovery_required` is
nonterminal. Each transition uses a compare-and-set on the target owner epoch.
The operation has `state: "running"` and `outcome: null` while any target is
nonterminal. It has `state: "completed"` and `outcome: "succeeded"` when every
target succeeded, `outcome: "partial"` when successes coexist with terminal
failures or supersessions, and `outcome: "failed"` when no target succeeded.
An empty `--all` selection completes with `outcome: "succeeded"`.

**R-06 — Boundary acquisition.** The reconciler may change
`waiting_boundary` to `preparing` only while the apply gate belongs to this
target and the durable ledger has no running turn for that session. It performs
this check and the owner-epoch claim in one transaction. It shall not count
queued turns as running. It shall not inspect any other session's turns.

**R-07 — Preparation.** Under the per-host load slot, the executor shall read
the target snapshot from the operation revision and record its hashes. It shall
read the prior snapshot and stage the complete target Tightbeam-owned skill
projection below the Tightbeam base staging directory. It shall validate the
staged projection, the session incarnation, the adapter generation, and the Git
revision relationship before changing the session cwd or runtime.

The executor shall revalidate those values and its gate in a short transaction
before it records the R-08 effect. A first incarnation or adapter-generation
change returns the target to `waiting_boundary` with cause
`session_generation_changed`. A second consecutive change terminates as
`failed` with `session_unstable`; no projection or adapter effect occurs.

**R-08 — Recoverable replacement seam.** A resident target shall use one
adapter contract:

```text
replace_identity(effectId, priorSnapshot, targetSnapshot)
replace_identity_status(effectId)
```

The effect ID is lowercase SHA-256 of UTF-8 operation ID, one NUL byte, UTF-8
session key, one NUL byte, ASCII target owner epoch, one NUL byte, and ASCII
`identity-replace`. Calls with the same ID coalesce to one logical effect.
Status returns only `not_started`, `in_progress`,
`target_active(contextId,targetRevision,runnable=true)`, or
`prior_restored(contextId,priorRevision,runnable=true,errorCode)`.

The implementation shall stage and validate the target before it disrupts the
prior context. It shall atomically elect one context as authoritative. It shall
not return a terminal status until exactly one named context is runnable. Target
failure shall restore the exact prior context and prior Tightbeam-owned skill
projection before it returns `prior_restored`. A failure to prove either safe
terminal status returns `in_progress`; the gateway records
`recovery_required`, retains the gate, and admits no turn.

The gateway shall persist the effect ID and call deadline before invocation. A
call deadline is 30,000 ms. Recovery calls status after exact delays of 5,000,
10,000, 20,000, 40,000, and 60,000 ms, then every 60,000 ms. `not_started`
authorizes the same-ID invoke. `in_progress`, timeout, unavailable adapter, or
an invalid receipt authorizes another status call only. A response after its
owner lease expires changes no durable state.

**R-09 — Nonresident targets.** A target with no session pointer has never
started. A target whose pointer is unknown to the current adapter generation is
nonresident. For either case, apply shall not start a harness context. It shall
install the target Tightbeam-owned projection and stamp the target snapshot in
the R-10 transaction. If projection installation or the database commit fails,
the gate remains and recovery reconciles the staged target or restores the
prior projection. The next ordinary start shall use the recorded target
revision. No pointer event claims that a harness load occurred.

**R-10 — Success commit.** After R-08 reports `target_active` or R-09 has an
installed target projection, one transaction shall verify the effect receipt or
nonresident fact, target revision, owner epoch, gate ownership, and current
session revision. It shall update all three identity stamps, record
`succeeded`, delete the gate, and record the success audit event together. If
the transaction rejects, the target enters or remains `commit_pending`; it
retries only this transaction and invokes no adapter effect. A queued turn can
be claimed only after this commit.

**R-11 — Failure and automatic rollback.** A preparation failure before any
projection or runtime change may record terminal `failed` and delete the gate.
After any external change, terminal `failed` is lawful only after an R-08
`prior_restored` receipt or an R-09 prior-projection readback proves that the
recorded prior revision is again authoritative. The terminal transaction stores
the safe error, records the rollback event, and deletes the gate together.

An unknown effect, unreachable adapter, failed rollback, or storage uncertainty
shall remain `recovery_required`. Automatic recovery continues with the same
effect ID and owner-epoch fencing. It never deletes the gate to restore
availability at the cost of identity uncertainty.

**R-12 — Concurrency and conflicting mutations.** One unique active apply gate
shall exist per session. Another apply records `apply_in_progress` for that
target, names the controlling operation, and performs no effect. Tune, repoint,
and a second identity mutation shall return `identity_apply_pending` with the
remedy `Inspect tightbeam identity apply --operation <operationId> and retry
after it is terminal.`

Retirement may cancel a target only while it is `waiting_boundary` or
`preparing` and no external effect has been recorded. It shall record terminal
`session_retired`, delete the gate, and then retire in the same session-row
transaction. During `switching`, `commit_pending`, `rolling_back`, or
`recovery_required`, retirement returns `identity_recovery_required` with the
remedy `Restore the matching Tightbeam build, let operation <operationId>
recover, then retry retirement.`

**R-13 — Revision races and operator rollback.** Acceptance and the R-07
pre-effect transaction shall use Git ancestry. A `NULL` recorded revision, an
equal revision, or an ancestor of the target may proceed. A target that is an
ancestor of the recorded revision becomes `superseded` with no gate or effect.
Unreadable or unrelated objects become terminal `failed` with
`identity_revision_unavailable` and no effect.

A later publication does not retarget an accepted operation. A success at B may
therefore remain stale against later live C. The stale alarm shall report it and
a new administrator operation may apply C. To undo identity content, an
administrator shall publish a descendant commit that reverts the content and
start a new operation. Apply shall never move a session stamp directly to an
ancestor.

**R-14 — Result projection and partial failure.** The operation query shall
return every frozen target in ascending key order with `state`, prior revision,
target revision, effect ID when created, attempt count, safe error, accepted
time, last transition time, and terminal time. `applied` lists succeeded keys;
`waiting` lists nonterminal keys; `failed` lists `failed` and `superseded` keys.
One target failure does not stop another executor.

The same idempotency key never retries a terminal target. After repairing a
terminal failure, the remedy is `Start a new identity apply operation with a
new --key.` Nonterminal recovery is automatic and a duplicate command only
returns its durable state.

**R-15 — Authorization.** Effect and query forms require the existing identity
administrator boundary. The gateway shall check authority before reading a
target operation or writing an idempotency binding. A denial returns
`forbidden` with the remedy `Ask an identity administrator to run this
command.` It writes only the ordinary denied-verb audit row and exposes no
operation or session existence.

**R-16 — Audit and redaction.** Additive audit events shall record
`identity_apply_accepted`, each target state transition,
`identity_apply_completed`, `identity_rollout_stale`,
`identity_rollout_overdue`, and `identity_rollout_current`. Each event shall
store the operation ID when applicable, session key when applicable, target
revision, closed cause, request principal, acting principal, and database
timestamp. Recovery events also store effect ID, owner epoch, call kind, safe
status class, ordinal, and next-attempt time.

The only durable error text is a fixed template from R-17. Unknown errors map
to `internal_apply_failure`; raw thrown values, adapter messages, response
bodies, stdout, stderr, and stack traces are neither interpolated nor persisted.
The event stream and command result contain no identity bytes, transcript bytes,
credentials, tokens, cookies, authorization headers, or environment values.

**R-17 — Named failures and remedies.** The first matching row controls a
command or target result. `<operationId>`, `<sessionKey>`, and
`<targetRevision>` receive recorded safe values.

| Code | Deterministic condition | Terminal | Exact remedy |
| --- | --- | --- | --- |
| `forbidden` | R-15 denies the caller. | command | `Ask an identity administrator to run this command.` |
| `not_found` | A one-session target or authorized operation query has no visible active object. | command | `Run tightbeam identity status and select an active session or operation.` |
| `idempotency_conflict` | A principal reuses one key with another canonical selector. | command | `Use a new --key for the different selector.` |
| `apply_in_progress` | Another operation owns the session gate. | target | `Inspect tightbeam identity apply --operation <operationId> and start a new operation after it is terminal.` |
| `identity_apply_pending` | A tune, repoint, or mutation encounters a safe active gate. | command | `Inspect tightbeam identity apply --operation <operationId> and retry after it is terminal.` |
| `identity_recovery_required` | Retirement encounters a target with an external or uncertain effect. | command | `Restore the matching Tightbeam build, let operation <operationId> recover, then retry retirement.` |
| `session_retired` | Retirement wins before any external apply effect. | target | `Run tightbeam identity status; no apply is required for the retired session.` |
| `target_superseded` | The target is an ancestor of the recorded session revision. | target | `Run tightbeam identity status and start a new operation against the current live revision.` |
| `identity_revision_unavailable` | A required object is unreadable or the revisions are unrelated. | target | `Repair the identity repository, run tightbeam identity status, then start a new operation.` |
| `session_unstable` | Incarnation or adapter generation changes twice during preparation. | target | `Stabilize the session adapter, then start a new operation with a new --key.` |
| `adapter_replace_unsupported` | The selected resident adapter lacks same-ID replace and status readback. | target | `Upgrade this release line's matching adapter build, then start a new operation.` |
| `projection_prepare_failed` | Target projection cannot be read, staged, or validated before mutation. | target | `Repair the named identity revision or session workdir, then start a new operation.` |
| `harness_replace_failed` | R-08 proves the prior context and projection were restored. | target | `Repair the session adapter, then start a new operation with a new --key.` |
| `internal_apply_failure` | No earlier safe condition matches before any external effect, or after prior restoration is proven. | target | `Inspect operation <operationId>, repair the substrate fault, then start a new operation.` |

`recovery_required`, adapter unavailability, timeout, invalid receipt, and
`commit_pending` are nonterminal states, not failure codes. Their remedy is
`Inspect tightbeam identity apply --operation <operationId>; recovery retries
automatically. Restore the matching build or adapter if progress stops.`

**R-18 — Stale-version alarm.** At boot, after every live-revision publication,
after every apply terminal transition, and every 60,000 ms, the substrate shall
compute the active stale-session set from durable session stamps and the one
live snapshot. It shall not call a harness or mutate identity.

When a nonempty set has no open alarm episode for that live revision, one
transaction shall open an episode and record one normal-attention
`identity_rollout_stale` notice to each distinct administrator Main session.
The notice states live revision, stale count, missing-revision count, active
apply-operation count, and these remedies:
`Run tightbeam identity status. Elect rollout with tightbeam identity apply
--all.` It shall not enumerate identity content or choose the election.

If the set remains nonempty 30 minutes after `firstObservedAt`, one transaction
shall record exactly one high-attention `identity_rollout_overdue` notice for
that episode. It adds oldest waiting-target age and counts of waiting,
recovering, and terminally failed targets. Its remedy is
`Inspect tightbeam identity status and each reported tightbeam identity apply
--operation <operationId>; repair named failures or elect a new rollout.`

When the stale set becomes empty, one transaction shall close the episode and
record `identity_rollout_current`. A later live revision creates a different
episode. Restart and repeated scans shall not duplicate any of the three
markers. If no administrator session is addressable, the durable event still
commits and doctor reports the active episode.

**R-19 — Status and doctor.** `identity status` shall retain its per-session
stale reasons and add one `rollout` object with live revision, stale count,
missing-revision count, open operation IDs, waiting count, recovery-required
count, failed count, alarm episode ID, and first-observed time. It shall perform
no apply effect.

Doctor shall add `identity-session-rollout`: `PASS` when no active session is
stale, `WARN` when an alarm episode is open, and `INFO` when the identity
repository or session store is unavailable for a non-mutating check. `WARN`
shall print the exact R-18 status and apply remedies. This check composes with,
but does not replace, the separate shipped-Kung-Fu staleness check from
`wi_61c28d6e-9a2b-4743-916b-a31fd47748e2`.

**R-20 — Additive storage and migration.** Each line shall add logically
equivalent operation, target, active-gate, and alarm-episode storage. Operation
storage includes ID, principal, idempotency binding, canonical selector, target
revision, frozen keys, state, and timestamps. Target storage includes session
key, prior stamps, target stamps, state, effect ID, owner epoch, generation
observations, recovery ordinal, next-attempt time, safe error code, and
timestamps. The active gate has a unique session key and names its operation,
target, epoch, and cause.

Migration shall not rewrite an existing row. Existing stale and missing stamps
remain truthful. Migration creates no operation, gate, alarm, turn, or
notification. The first R-18 scan may open the one warranted alarm episode; it
shall never auto-apply.

**R-21 — Release-line parity and rollback.** `0.1.9` and `main` shall implement
the same states, wire fields, refusal codes, audit fields, timers, per-host
bound, and fixtures. A line-specific module name or migration number is not a
behavioral divergence.

Disabling new acceptance shall not disable recovery of an existing nonterminal
target. Package rollback to a build that does not understand apply gates shall
be refused while any target is nonterminal. The refusal is
`identity_apply_downgrade_blocked` with remedy `Restore the matching Tightbeam
build and wait for every identity apply operation to become terminal before
retrying package rollback.` Additive tables remain inert after every operation
is terminal. A schema rollback shall not drop operation, target, gate, alarm, or
audit evidence.

### Deterministic action and human choice boundary

The substrate may authenticate, capture a revision, freeze keys, order locks,
insert a gate, observe a session boundary, render and hash snapshots, invoke or
query an already elected effect, classify a closed result, restore the prior
snapshot, update status, and emit an alarm. These are facts and actions.

Only an administrator may publish identity, elect apply, select one session or
all sessions, choose a new retry key after a terminal result, publish a
content-revert commit, or repair a host. The substrate shall expose the relevant
facts and exact remedies. It shall not make these choices.

## Acceptance

**A-01 — Self-apply terminates the command (R-01, R-03, R-04, I-01, I-02).**
Given an administrator-owned agent invokes `identity apply --all` inside its own
held running turn, the command returns a `running` accepted operation with an ID before
that turn terminals. The caller target is `waiting_boundary`, every later caller
turn remains queued, and no turn is canceled. When the invoking turn terminals,
that target applies before the next queued turn.

**A-02 — Busy bystander does not block fleet progress (R-04, R-06, R-14).**
Given `--all` selects one held running session, one idle resident session, one
queued-only session, one nonresident session, and one never-started session,
the idle and nonresident targets succeed while the held target waits. The
operation does not return `turn_in_progress`. Releasing the held turn lets its
target apply before its next queued turn.

**A-03 — Claim race (R-03, R-04, I-03).** A deterministic barrier shall release
turn claim and acceptance in both commit orders. Claim-first produces one
normally completed prior-identity turn followed by apply. Gate-first leaves the
turn queued until apply terminalizes. No turn starts inside an active gate.

**A-04 — Single revision and revision race (R-07, R-10, R-13).** Given target B
and a live advance to C during execution, every B success uses B for guidance,
skills, render contract, digest, and stamp. Status reports B stale against C.
An operation for ancestor A cannot replace B or C. A new operation can apply C.

**A-05 — Resident success on both harnesses (R-07 through R-10, I-07, I-08).**
Controlled Codex and Claude adapters shall prove same-ID replacement, same
workdir and history, one target context runnable, target projection and all
three stamps committed, gate removed, queued work admitted afterward, and no
shared runtime restart or other-session effect. The host load-slot count never
exceeds three.

**A-06 — Nonresident shapes (R-09).** Never-started and pointer-but-not-resident
fixtures perform no adapter load, append no pointer event, install and stamp the
target snapshot, and start later from that recorded revision.

**A-07 — Target failure rollback (R-08, R-11, I-05).** Inject failure before
replacement, during target activation, and after target activation begins. A
terminal failure is visible only after the exact prior projection and one prior
context are authoritative and runnable. Its stamp stays prior and its gate is
removed in the failure transaction. No queued turn observes a mixed projection.

**A-08 — Unknown effect recovery (R-08, R-10, R-11, I-09).** At every phase
boundary, stop the gateway before and after the external call and before and
after the terminal database commit. Recovery adopts a higher owner epoch,
queries the same effect ID, and reaches one success or proven rollback. A stale
worker cannot invoke or commit. Timeout fixtures prove the exact deadline and
backoff sequence. Invalid or unavailable status keeps the gate and admits no
turn.

**A-09 — Commit-pending recovery (R-10).** Given target activation succeeded and
two database commits reject, the target remains `commit_pending`, the gate
remains, and no adapter call or turn occurs. A later successful retry commits
the stamps, outcome, event, and gate deletion once.

**A-10 — Partial failure (R-05, R-14).** Given three targets that succeed,
restore prior after failure, and remain in recovery, the first two reach their
terminal states while the third stays nonterminal. The operation query reports
ordered applied, waiting, and failed sets. Repairing the third adapter lets
automatic same-effect recovery complete without repeating the first two.

**A-11 — Duplicate and overlapping operations (R-02, R-12, R-13).** Concurrent
byte-equal keyed requests create one operation and one gate per target. A
different selector with that key gets `idempotency_conflict`. A different
operation that overlaps an active gate records `apply_in_progress` only for
that target and continues its other targets. No effect runs twice.

**A-12 — Retirement and tune races (R-12).** Retirement that wins before an
effect records `session_retired`, clears the gate, and retires once. Retirement
after an effect record receives `identity_recovery_required` and changes
nothing. Tune and repoint receive `identity_apply_pending` while the gate is
active. Every response contains the exact R-17 remedy.

**A-13 — Authorization and existence privacy (R-15).** A nonadministrator gets
`forbidden` for effect and query forms and creates no operation, gate, marker,
or session change beyond the denied-verb audit. Unknown and retired target keys
produce the same authorized `not_found` shape.

**A-14 — Evidence and redaction (R-16, R-17, I-12).** Every accepted operation,
state transition, safe failure, recovery observation, completion, and alarm has
cause, request principal, and acting principal. Fixtures inject tokens in every
raw adapter field and prove that command output and durable rows contain only a
fixed safe code, message, remedy, and structural correlation fields.

**A-15 — Stale alarm lifecycle (R-18, R-19).** With a fake database clock, a
nonempty stale set opens one normal episode and notice. Repeated boot and
60-second scans do not duplicate it. At 29:59 no overdue marker exists. At
30:00 exactly one high marker exists with correct counts and remedies. When the
last stale session becomes current, one current marker closes the episode. A
later live revision opens a new episode. No scan calls a harness or applies.

**A-16 — Migration and rollback (R-20, R-21).** Copies of pre-feature `0.1.9`
and main databases migrate with all existing row bytes and counts unchanged and
empty apply stores. Their first scan reports existing staleness without
applying. A package rollback with a nonterminal target receives
`identity_apply_downgrade_blocked`; after all targets terminalize, old code can
ignore the retained additive history.

**A-17 — Cross-line conformance (R-21).** The same fixture corpus shall run
against exact implementation candidates on `0.1.9` and main. Canonical JSON for
acceptance, every state, every refusal, alarm fields, and final results shall be
byte-equal after replacing line-specific build and migration identifiers.

**A-18 — No prior interruption machinery (scope).** A source and migration
inspection shall find no runner-stop effect, apply-driven turn cancellation,
apply continuation intent, apply continuation prompt, or global running-turn
preflight. Existing ordinary cancel and continuation mechanisms remain
unchanged outside identity apply.

## Open Questions

None. The current assignment elects asynchronous per-session rolling apply for
both lines. It replaces synchronous global refusal and the unshipped
running-turn interruption design.
