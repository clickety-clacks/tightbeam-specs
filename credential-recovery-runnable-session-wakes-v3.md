# Credential recovery wakes affected runnable sessions — v3

Status: PROPOSAL — INDEPENDENT REVIEW REQUIRED

Authority: Mike's product ruling
`att_c0d47267-eca0-49c9-9ac5-41c562b4dca7`, 2026-08-27.

Work item: `wi_82a81f78-5789-469e-863a-fb84d82781cd`.

Reconciled baselines: Tightbeam product `main` at
`8e269e89c04b6b8569813142a12742f3325b8503`; Tightbeam specs `main` at
`5f4b636d02aa8f1cd0670dd090d0af8c35894e88`.

Review history: round 1 requested changes in
`att_c16e2c1f-a419-4e68-b7c3-5ff4fa6acb63`, report `art_dfa9187a`.

Implementation target: UNSET. Review of this proposal does not select a release
line, branch, merge, release, or deployment target.

Supersession: after an independent `reviewed-clean` verdict accepts these exact
bytes, this specification supersedes `spec-oauth-recovery-main-prompt-v2.md` and
its Main-only recovery pattern. Until that verdict, the earlier specification
remains the current authority. This specification does not supersede
`harness-recovery-main-wake-v1.md` or the account-switch work in
`wi_008ad6d7-d976-4120-9e90-8557a24f7602`.

Operating pattern taught to agents: none. This specification adds a substrate
recovery event. It adds no standing guidance.

## Goal

After Tightbeam commits a provider credential on one host and completes the
replacement adapter cycle, Tightbeam creates one durable recovery obligation for
each affected active session. Tightbeam delivers a recovery turn to each target
that can run. Each target then inspects its own durable work and resumes or
dispositions work that it judges was stranded by the credential outage. The
operator takes no action after the credential ceremony succeeds.

The substrate determines the finite target set from session, host, harness, and
credential-lifecycle rows. It does not ask Main to infer the target set. It does
not decide which assignment or wake a target must resume.

## Non-Goals

- Select or switch a named provider account. That remains
  `wi_008ad6d7-d976-4120-9e90-8557a24f7602`.
- Detect generic spontaneous harness recovery. That remains separate from this
  explicit credential-activation event.
- Retry a prior failed inference turn or reproduce its external side effects.
- Change an existing assignment, work item, message, wake, or turn to make work
  appear resumed.
- Wake sessions on another host or sessions whose harness does not use the
  activated provider.
- Read, copy, log, or expose credential bytes or an external account identifier.
- Add identity, archetype, Kung Fu, skill, manual, or other standing-guidance
  text.
- Select an implementation target, merge, release, deployment, credential
  mutation, or service restart.

## Terms

- **Credential scope**: the pair `{host, provider}`. A successful activation on
  one scope says nothing about the same provider on another host.
- **Activation**: one credential ceremony whose credential install, onboarded
  metadata commit, provider adapter stop/start cycle, and session-resume callback
  each succeeded. Initial onboarding and re-onboarding use the same term.
- **Activation ID**: an opaque Tightbeam identifier minted before the credential
  mutation starts. It identifies lifecycle evidence. It does not identify a
  provider account.
- **Activation generation**: a monotonic integer within one credential scope.
  Replaying one Activation ID keeps its generation. A later Activation ID in the
  same scope receives a later generation.
- **Adapter generation**: the durable generation of the provider adapter that a
  run attempt uses. The successful replacement cycle publishes a later adapter
  generation before affected session lanes resume.
- **Account boundary**: the credential version installed by one Activation ID.
  Tightbeam does not select or expose a named external provider account. Host
  and provider form the routable scope.
- **Affected candidate**: a session that the target-snapshot transaction finds
  with `state = active`, the activation host, and a harness whose recorded
  credential provider equals the activation provider.
- **Affected runnable session**: an affected candidate that remains active and
  in the same credential scope when Tightbeam claims its recovery carrier, and
  whose attempt passes the typed pre-inference run-admission boundary. Delivery
  is the required result for this session, not part of the definition.
- **Recovery obligation**: the durable per-session statement that the session's
  handled generation is earlier than the scope's required generation.
- **Activation membership**: the durable decision row that binds one Activation
  ID and one snapshotted session. It records that activation's generation,
  target identity, snapshot facts, resolution, and any stranded-turn
  reconciliation. Later activations do not replace it.
- **Recovery carrier**: an ordinary immediate prompt wake for one recovery
  obligation. Its linked turn runs through the existing scheduler, ledger, and
  session lane.
- **Delivery cycle**: one carrier plus its finite retry attempts. A target starts
  a later delivery cycle only when its required generation remains later than
  the generation covered by its prior cycle.
- **Covered generation**: the target's required generation when the session lane
  claims a carrier attempt. A carrier cannot handle a generation that becomes
  ready after that claim.
- **Handled**: the recovery carrier's linked turn reached the ledger's delivered
  terminal state. Handled proves delivery to inference. It does not claim that
  the model obeyed the prompt.
- **Stranded work**: an existing durable obligation or continuation that the
  target agent judges it could not advance because the old credential or its
  adapter could not run.
- **Dark target**: an affected candidate with neither a handled required
  generation nor a typed final disposition after the retry contract ends.
- **Typed final disposition**: `retired`, `no_longer_affected`, or
  `undeliverable`. Each disposition names its cause row and principal.

## Assumptions

1. Tightbeam owns one active credential per provider and host. Provider account
   inventory outside Tightbeam does not select that credential.
2. The credential lifecycle can observe credential commit, onboarded metadata,
   adapter stop/start results, and the resume callback separately.
3. Session rows record active or retired state, host, harness, owner, and current
   model selection.
4. The harness registry deterministically maps a harness to its credential
   provider.
5. The session lane preserves FIFO order and permits one running turn per
   session. A recovery carrier does not interrupt a running turn.
6. The run boundary can distinguish `could_not_run` from `run_failed`,
   `run_canceled`, and `outcome_unknown` without parsing prose. If the build
   baseline lacks this typed distinction, the recovery implementation must add
   it at the run boundary before it adds retry.
7. A run attempt can durably record the provider adapter generation it uses. If
   the build baseline lacks that field, the recovery implementation must add it
   at run claim before it reconciles a prior-generation run.
8. Retry delays of 5,000 ms, 30,000 ms, and 120,000 ms bound waiting. The delays
   do not detect credential recovery or decide an outcome.

## Invariants

### I1 — Only a completed activation opens recovery

Tightbeam shall mint an Activation ID before it starts credential mutation.
Tightbeam shall record each lifecycle edge under that ID.

Tightbeam shall open recovery only after the credential install, onboarded
metadata commit, provider adapter stop/start cycle, and resume callback each
report success for the same credential scope and Activation ID.

A begin, cancel, failed install, failed metadata commit, partial adapter start,
or failed resume shall create no recovery obligation. It shall record the
failed edge under the Activation ID.

The successful finish response shall not precede the transaction that records
the ready activation and its target set.

### I2 — Scope selection is finite and deterministic

The ready-activation transaction shall select affected candidates from session
rows and the harness-to-provider mapping. It shall use exact equality for host,
provider, harness mapping, and active state.

For each affected candidate, the transaction shall insert one activation
membership unique by `{ActivationID, sessionKey}` and insert or advance one
persistent recovery obligation unique by `{host, provider, sessionKey}`. The
membership records the activation generation and exact snapshot facts. Target
selection, membership writes, and obligation writes shall commit as one step.

Membership in an activation is immutable. Its resolution and reconciliation
fields may advance through I5-I7. A later activation writes its own membership
rows and cannot add to, remove from, or overwrite the earlier target set.

A session created after the snapshot is outside that activation. It starts
against the committed credential and needs no recovery carrier for prior work.

Main is a target only when its session row satisfies the same predicate. Main's
kind, role, or topology position grants no special recovery status.

### I3 — Each target receives its own carrier

Tightbeam shall route one outstanding recovery carrier directly to each open
recovery obligation. It shall use the target session key, `process:tightbeam`
as principal and origin, prompt consumer, immediate due time, and the ordinary
active-session gate.

Tightbeam shall not route the activation only to Main. Tightbeam shall not ask
one agent to enumerate or wake the target set. Tightbeam shall not select a
product owner, archetype, Kung Fu, work item, or assignment.

### I4 — The carrier leaves product judgment with the target

The stored prompt shall name the provider, host, originating Activation ID, and
originating activation generation. It shall state that a later activation can
coalesce into the obligation. It shall instruct the target to:

1. read the current target readback for the credential scope;
2. read its own open assignments and durable continuation facts;
3. inspect work that it judges was blocked by the credential outage;
4. resume that work or file its lawful disposition; and
5. preserve unrelated work.

The prompt shall not name an assignment to resume. The substrate shall not
parse assignment notes, wake prompts, transcript text, or model output to make
that choice.

### I5 — Recovery preserves existing work carriers

Recovery shall append its own run, activation-membership, target, wake, turn,
and audit rows. It shall not reopen, cancel, replace, reorder, or mutate an
existing assignment, work item, message, wake, or terminal turn. It shall not
retry an earlier inference turn.

The recovery carrier shall enter the target's FIFO after an existing queued or
running turn. A later normal turn boundary, not elapsed time, permits it to run.

The ready-activation transaction shall inspect each affected candidate's lane.
When the lane has a running turn stamped with an earlier adapter generation, the
transaction shall record `reconciliation = pending` and that exact turn ID on
the activation membership. It shall commit the target membership, recovery
obligation, carrier, and reconciliation record before a later reconciliation can
release the lane.

After that commit, the recovery component shall invoke
`reconcile_ready_activation(ActivationID)`. This is the only actor that initiates
prior-generation reconciliation. Credential finish invokes it synchronously
after the ready transaction. Boot reconciliation invokes it for each ready or
recovering activation with a due pending membership. It does not wait for an old
adapter callback.

The component shall process pending memberships in ascending session-key order.
For each membership, one transaction shall re-read the recorded turn and lane.
When the exact turn remains running and prior-generation, the transaction shall
call the ordinary run-terminal mutation and mark the membership reconciliation
done. It shall terminalize the run exactly once as `could_not_run` when durable
evidence proves inference was not admitted. It shall terminalize the run as
`outcome_unknown` when admission occurred or cannot be disproved. It shall never
mark that run delivered and shall never retry it.

When the recorded turn is already terminal, the transaction shall mark
reconciliation done with that observed terminal row. When the lane no longer
contains that turn, or the turn uses the activated adapter generation, the
transaction shall record `reconciliation = not_required` without changing the
turn. The reconciliation identity
`{ActivationID, sessionKey, recordedTurnID}` is unique and replaying it has no
second effect.

A membership reconciliation is `not_required`, `pending`, `done`, or `failed`.
Only the ready transaction creates `pending`. A successful invocation changes
`pending` to `done` or `not_required`. When an invocation cannot complete the
terminal transaction, the recovery component records typed `could_not_run` on
the target's current pre-inference carrier attempt and leaves reconciliation
`pending`. I9 schedules the next carrier attempt and due time. Credential finish
invokes attempt `0`; the ordinary scheduler invokes each due retry before it
admits that carrier; boot invokes a due attempt that survived a crash.

When attempt `3` cannot reconcile, the terminal transaction changes
reconciliation to `failed`, resolves each still-open membership through the
then-current required generation as `undeliverable`, and applies I9's
generation-aware target transition. It admits no inference. A later activation
may create a new membership and delivery cycle; the failed membership never
reopens. One membership failure does not stop an invocation from processing
later memberships.

A run claimed before this feature recorded adapter generations is a
prior-generation run only when its durable claim time precedes the replacement
adapter generation's publication time and its session satisfies the exact I2
scope. The run boundary shall classify it as `outcome_unknown`; it shall not
infer pre-admission safety. After the feature is enabled, the run-claim
transaction shall reject a missing adapter generation as typed
`generation_missing` before it admits inference.

The typed terminal transaction releases the session lane through the existing
terminal publisher so its already-durable recovery carrier can run. A running
turn stamped with the activated adapter generation is not a stranded
prior-generation run; recovery leaves it in place and remains behind it in FIFO
order.

### I6 — One mutation seam owns recovery state

One recovery component shall own activation, membership, reconciliation, and
target transitions. Credential, scheduler, session-lane, boot, and readback code
shall call that component. They shall not write recovery state directly.

The component shall enforce these run states:

`prepared -> credential_installed -> activation_ready -> recovering -> complete`

`activation_ready` means that credential install, onboarded metadata commit,
adapter stop/start, and resume each succeeded. This state name does not prescribe
an order among those credential-lifecycle edges. Their source authority owns that
order.

It shall also permit a transition from a nonterminal state to `failed` with a
typed cause. A later credential ceremony creates a new Activation ID; it does
not rewrite the failed activation.

Each activation membership shall enforce this resolution machine:

`open -> handled | retired | no_longer_affected | undeliverable`

A membership resolution is terminal and never reopens. The transaction that
resolves a carrier cycle shall resolve each open membership for that target whose
activation generation is not later than the cycle's resolution generation.

The persistent target shall enforce these cycle states:

`pending -> admitted -> claimed -> handled`

Typed `could_not_run` permits `pending -> retry_wait -> pending` for a
pre-admission reconciliation attempt and `claimed -> retry_wait -> pending` for
a claimed carrier attempt. Eligibility revalidation may change `pending`,
`admitted`, or `retry_wait` to `retired` or `no_longer_affected`. A final
reconciliation failure may change `pending` to `undeliverable`. A terminal
carrier outcome may change `claimed` to `undeliverable` through the rules below.

At the recorded retry due time, one transaction shall change `retry_wait` to
`pending` and create exactly one carrier attempt unique by
`{targetIdentity, deliveryCycle, nextAttemptNumber}`. It shall not increment the
delivery cycle. Scheduler and boot replays shall reuse that identity.

Only these two transitions may open a later cycle:

1. The ready-activation transaction may change `handled`, `undeliverable`, or
   `no_longer_affected` to `pending` when it inserts a later open membership for
   the same active, in-scope session.
2. A carrier-terminal transaction may change `claimed` directly to `pending`
   when its resolution generation is earlier than the target's required
   generation.

Either transition shall increment delivery cycle, clear cycle-local carrier and
failure fields, set attempt to `0`, and create exactly one new carrier in the
same transaction. `retired` has no outgoing transition because a retired session
cannot satisfy the active snapshot predicate. Earlier membership resolutions
and wake or turn rows remain unchanged.

Each guard and its state change shall occur in one database transaction.

### I7 — Concurrent activations coalesce by required generation

Each credential scope shall have one current generation. Each session and scope
shall have at most one outstanding recovery carrier.

When a later activation in the same scope becomes ready, the transaction shall
advance each affected target's required generation. It shall preserve an
existing pending, admitted, claimed, retry-waiting, queued, or running carrier
for that target instead of adding a second carrier.

When the session lane claims a carrier attempt, the claim transaction shall
stamp its covered generation from the then-current required generation. A
delivered terminal transaction shall advance handled generation only to that
stamped covered generation. The stamped covered generation is the cycle's
resolution generation for delivered or run-terminal outcomes. An eligibility
disposition before claim uses the then-current required generation as its
resolution generation.

If required generation is later than handled generation after a carrier becomes
terminal, the terminal transaction shall resolve only memberships through the
cycle's resolution generation and atomically take I6 transition 2. This rule
covers a later activation that became ready while the carrier ran. It shall not
credit the earlier carrier with a generation that became ready after the carrier
was claimed.

When a later activation snapshots an affected candidate whose persistent target
is `handled`, `undeliverable`, or `no_longer_affected`, the ready transaction
shall atomically insert the new membership and take I6 transition 1. The earlier
terminal result remains decision state on its activation membership, not only an
audit event.

Activations in different credential scopes shall not coalesce.

### I8 — Replay is idempotent

Activation ID shall be unique. Activation membership shall be unique by
`{ActivationID, sessionKey}`. The persistent target identity shall be unique by
`{host, provider, sessionKey}`. Delivery cycle shall increase monotonically for
one target. One carrier attempt shall be unique by
`{targetIdentity, deliveryCycle, attemptNumber}`. Prior-generation
reconciliation shall be unique by
`{ActivationID, sessionKey, recordedTurnID}`.

Replaying lifecycle callbacks, the ready transaction, reconciliation invocation,
scheduler passes, turn terminal callbacks, or boot reconciliation shall reuse
those identities. A replay shall create no second membership, obligation,
carrier attempt, reconciliation terminal, or final disposition.

Boot reconciliation shall inspect nonterminal activation, membership, and target
rows. It shall invoke `reconcile_ready_activation` for a pending reconciliation
whose carrier attempt is due and continue the next deterministic carrier edge.
It shall not retry a final failed reconciliation. It shall continue a
credential-lifecycle edge only when matching onboarded metadata and adapter state
prove that edge. It shall record `failed` when authoritative metadata proves that
activation did not commit. It shall not infer success from credential-file
contents, transcript text, or audit projections.

### I9 — Retry is finite and run-admission safe

One delivery cycle uses one attempt sequence for both pre-admission stranded-turn
reconciliation and carrier run admission. Attempt `0` is the initial carrier. A
carrier attempt that reaches typed `could_not_run` before inference admission
shall permit attempts `1`, `2`, and `3` after 5,000 ms, 30,000 ms, and 120,000 ms
respectively. Reconciliation success does not consume or reset the current
attempt; the same carrier attempt proceeds to ordinary admission.

The terminal transaction shall authorize the next attempt and record its due
time. Attempt `3` reaching `could_not_run` shall resolve open memberships through
its resolution generation as `undeliverable`. If required generation is later
than that resolution generation, the transaction shall take I6 transition 2;
otherwise it shall change the persistent target to `undeliverable`.

`run_failed`, `run_canceled`, and `outcome_unknown` shall resolve open
memberships through their resolution generation as `undeliverable` without
retry. They shall use the same generation-aware target transition. These classes
cannot prove that retrying is side-effect safe.

A new activation generation shall not reset the attempt count of an outstanding
delivery cycle. A later cycle starts at attempt `0` only after the prior cycle
becomes terminal and required generation remains later than handled generation.

### I10 — Admission and claim revalidate session eligibility

The carrier-admission transaction and the session-lane claim transaction shall
re-read the target session.

It shall record `retired` and admit no turn when the row is retired. It shall
record `no_longer_affected` and admit no turn when the session's host or harness
no longer maps to the credential scope.

It shall admit the turn when the row remains active and in scope. The
revalidation and admission action shall be indivisible.

If the session becomes retired or leaves scope after admission but before claim,
the claim transaction shall suppress inference for that recovery turn and record
the matching typed final disposition. This rule affects only the recovery
carrier; it does not cancel an ordinary queued turn.

A session that tunes into the scope after the ready snapshot is not added to the
past activation. Its later work already starts against the activated
credential.

### I11 — Partial failures remain visible and recoverable

The credential finish surface shall distinguish these outcomes:

- `credential_activation_failed`: the credential or adapter cycle did not
  complete; recovery did not start.
- `credential_recovered_recovery_plan_failed`: the credential and adapter cycle
  completed, but the target-plan transaction did not commit.
- `credential_recovery_in_progress`: the activation and target plan committed;
  one or more target obligations remain open.
- `credential_recovery_reconciliation_retrying`: the activation and target plan
  committed, but the synchronous reconciliation attempt reached typed
  `could_not_run` and a finite retry is due.
- `credential_recovery_complete`: each activation membership reached handled or
  a typed final disposition.
- `credential_recovery_incomplete`: at least one activation membership reached
  `undeliverable`.

The partial-success result shall carry `credentialRecovered`, `adaptersReady`,
`recoveryStarted`, reconciliation counts by state, and Activation ID. The
credential result and recovery result shall be separate typed fields. A caller
can therefore observe that the new credential is installed even when recovery
planning, reconciliation, or delivery is incomplete.

The boot reconciler shall retry a ready activation whose target-plan transaction
did not commit and shall replay a due pending membership reconciliation under
I5 and I9. It shall not replay final `failed`. The persistent readback shall
expose the last reconciliation failure, current attempt, and next due time while
it is retryable. An agent can start a later credential ceremony to exit a failed
activation. No database edit is required.

### I12 — Completion does not claim semantic obedience

An activation reaches `complete` when each of its immutable membership rows has
`handled`, `retired`, `no_longer_affected`, or `undeliverable`, and each recorded
reconciliation is `done`, `not_required`, or final `failed`.

Each membership-resolution or reconciliation transaction shall recompute the run
state of every affected Activation ID from its membership rows and change an
eligible run to `complete` in that same transaction. No stored aggregate outside
those rows decides completion.

The aggregate shall report `credential_recovery_incomplete` when one or more of
that activation's memberships are `undeliverable`. It shall report
`credential_recovery_complete` otherwise.

Handled does not prove work resumed. Agent-owned assignment, continuation, and
completion rows remain the evidence that stranded work resumed.

### I13 — Readback, authorization, privacy, and audit are explicit

The credential finish result and a persistent readback shall expose Activation
ID, host, provider, credential kind, generation, aggregate state, the exact
activation membership set, membership counts by resolution, reconciliation
state, persistent-target cycle and state, attempt counts, next retry time, and
typed failures. Activation aggregates and counts shall derive from membership
rows for that Activation ID, not from the persistent target's latest state.

An admin can read the activation aggregate and its targets. A target session can
read its own target row. The owner of a target session can read that target row.
Other callers receive the existing non-disclosing authorization failure.

Each activation, membership, reconciliation, and target transition shall record
timestamp, cause kind, cause row ID, and principal. Substrate transitions use
`process:tightbeam`.

Rows, prompts, logs, finish results, and readback shall contain no credential
bytes, access token, refresh token, authorization code, provider account ID,
email address, or external account label.

### I14 — The mechanism does not assume an org topology

Target selection shall produce the same result for one owner or several owners,
with or without an active Main, and with any mix of archetypes and Kung Fu.

A missing, retired, wedged, or wrong-provider Main shall not prevent another
affected runnable session from receiving its carrier.

### Subtraction ruling

DELETE loses because removing recovery wakes preserves the reported silent
outage. ACCEPT loses because a successful credential ceremony would still need
an operator poke. ADD wins only for the per-scope run, immutable activation
membership, and persistent per-session obligation needed to survive crashes,
coalesce concurrent activations, and prove that no target stayed dark. The
membership row also carries the stranded-turn reconciliation marker; no fourth
recovery store is added. The Main-only prompt and transcript-only recovery
mechanisms are removed from this path rather than retained beside it.

## Architecture

### A. Recovery ledger

The implementation shall add one run store, one activation-membership store, and
one persistent-target store.

The run store records Activation ID, credential scope, credential kind,
generation, run state, lifecycle timestamps, cause, and principal. Aggregate
readback derives from activation memberships under I12 and I13.

The activation-membership store records Activation ID, session key, persistent
target identity, activation generation, immutable snapshot host and harness,
resolution state, resolved cycle and turn, reconciliation state, recorded
stranded turn, typed reconciliation failure, cause, and principal. It is the
decision source for one activation's target list and aggregate.

The persistent-target store records credential scope, session key, required
generation, handled generation, covered generation, cycle state, delivery cycle,
current carrier wake ID, attempt number, next retry time, latest linked turn,
typed failure, cause, and principal. Existing wake and turn rows retain each
cycle's attempts and terminal evidence.

All three stores have the one recovery-component mutation seam required by I6.
Lifecycle events are audit projections. They are not decision state.

### B. Credential-lifecycle bracket

Before credential mutation, the credential owner asks the recovery component to
prepare an Activation ID. The credential lifecycle persists that ID with its
non-secret Tightbeam-owned activation metadata. After each credential and
adapter edge, it records the edge through the component. After credential
install, onboarded metadata commit, adapter stop/start, and resume succeed, it
asks the component to atomically mark the activation ready, snapshot affected
candidates, insert immutable activation memberships, advance target generations,
record pending stranded-turn reconciliations, and create missing attempt-0
carriers.

After this transaction commits, credential finish invokes
`reconcile_ready_activation`. The finish response returns the typed result of
that synchronous pass. Carrier delivery remains asynchronous and visible through
readback.

### C. Carrier lifecycle

The recovery component, invoked by credential finish and boot under I5, consumes
pending membership reconciliations before it nudges carrier delivery. Its
transaction calls the existing run-terminal mutation and records reconciliation
completion under one replay identity. The existing terminal publisher releases
the lane. No old-adapter callback is required.

If reconciliation reaches `could_not_run`, the component leaves the carrier
pre-inference and uses its I9 attempt and due-time contract. At each due time the
ordinary scheduler calls the recovery component before carrier admission. It
admits the carrier only after reconciliation is `done` or `not_required`.

The ordinary scheduler then admits a recovery carrier through the active-session
gate. The admission and claim transactions revalidate the session scope. The
session lane runs the linked recovery turn in FIFO order. The turn terminal
transaction updates membership resolution and persistent-target cycle state
through the recovery component.

Only a typed pre-inference `could_not_run` result schedules a retry. Final
failures enter the existing capable-parent fault-bubble path with the target
identity and Activation ID. The recovery ledger remains the source for status.

### D. Main-only ruling

One Main wake plus inferred fanout does not satisfy this specification.

The predecessor Main-only implementation at commit
`133ebadc640e974d3d0578d9a8399c80ba6feb42` passed independent review
`att_fdc015f4-8355-4797-83f1-2246befee3b0` and a disposable-org proof. That
evidence proves that Main can perform fanout when its turn runs.

The same contract deliberately suppresses recovery when Main retires before
delivery. The predecessor successor assignment
`asg_dd67f584-b39e-43f1-b32a-b86cd6424ad6` also records a real seven-hour
wedged turn for which a Main wake queued but did not run after capacity returned.
These cases leave target coverage dependent on one session and one inference
result.

The accepted product outcome requires deterministic coverage of a finite set.
Per-session recovery obligations provide that coverage without moving the
target agent's work judgment into the substrate.

### E. Compatibility

Existing credential, adapter, session, assignment, wake, turn, and transcript
rows retain their meaning. The migration creates empty recovery stores. It does
not backfill an activation from transcript notices or historical credential
metadata.

The migration does not invent adapter generations for historical run attempts.
I5 defines the deterministic treatment of a still-running historical attempt at
the first later activation. New run claims cannot represent a missing adapter
generation.

The implementation replaces the successful-finish Main-only scheduling call and
the recovery value of transcript-only notices. It can retain credential
transition messages as informational transcript facts, but those messages do
not satisfy or advance a recovery obligation.

The implementation shall reuse the ordinary wake scheduler, turn ledger,
session lane, terminal publisher, boot reconciliation, and fault-bubble path. It
shall not add a second scheduler or supervision tree.

## Acceptance

### A1 — Trigger and ordering

Given a staged provider credential, when credential install and metadata commit
succeed but one provider adapter fails to start, then Tightbeam records
`credential_activation_failed`, creates zero recovery targets, and returns no
ordinary onboarded response.

Given the same ceremony, when credential install, metadata commit, each provider
adapter start, and resume succeed, then the ready transaction commits before the
success response and returns one Activation ID.

### A2 — Exact target set

Given a disposable org with two active matching sessions under different
owners, one matching active Main, one retired matching session, one active
session on another host, and one active session on another provider, when the
activation becomes ready, then the recovery ledger contains exactly three open
activation memberships, exactly three open persistent targets, and one carrier
for each target.

The retired, other-host, and other-provider sessions receive no carrier. The
test fails if routing depends on archetype, Kung Fu, product owner, or Main
fanout.

Given activation 4 snapshots sessions A and B and activation 5 later snapshots B
and C, when an authorized caller reads both activations, then activation 4 still
lists exactly A and B and activation 5 lists exactly B and C. Advancing B's
persistent target to generation 5 does not alter either membership set.

### A3 — Each runnable target receives a real turn

Given the A2 org and real Scheduler, Gateway, Ledger, and SessionLane processes,
when the three target sessions can each complete an ordinary turn, then each
recovery carrier reaches one delivered linked turn and each target reaches
handled for the required generation.

The test fails if one target remains pending, admitted, claimed, retry-waiting,
unlinked, or absent, or if one activation membership remains open after the lane
becomes idle. A transcript insertion or direct terminal-row fixture does not
satisfy this check.

Given the same matching non-Main targets with no Main session, a retired Main,
or a wrong-provider Main, when their lanes can complete ordinary turns, then
each matching non-Main target still reaches handled. No Main row or Main turn is
test setup for this proof.

### A4 — Stranded work resumes through agent judgment

Given two target sessions with open assignments and durable pre-activation
failure evidence, when a real recovery turn reaches each target, then each
target independently reads its assignment rows and files a lawful post-recovery
progress, completion, surrender, or bounded-continuation receipt.

The proof records the recovery turn and resulting agent-owned receipt for each
assignment. It does not accept a substrate-authored receipt as evidence of
resumption.

### A5 — Running, queued, tuned, and retired boundaries

Given one target with a running turn stamped with the activated adapter
generation and one target with a queued ordinary wake, when activation becomes
ready, then recovery creates one carrier for each without canceling or
reordering either existing carrier. The recovery turns run at later turn
boundaries.

Given a target has a running prior-generation turn with durable pre-inference
evidence, when the ready transaction commits, then it first records the carrier
and one pending reconciliation keyed by the Activation ID, session, and running
turn. When credential finish invokes `reconcile_ready_activation`, then that
transaction terminalizes the turn once as `could_not_run`, marks reconciliation
done, does not retry the old turn, releases the lane, and permits the recovery
carrier to reach a real turn.

Given a target has a running prior-generation turn whose inference admission
occurred or is unknown, when the reconciliation invocation runs after the ready
commit, then it terminalizes that turn once as `outcome_unknown`, marks
reconciliation done, does not retry the old turn, releases the lane, and permits
the recovery carrier to reach a real turn.

Given a matching historical running turn has no adapter-generation stamp and its
claim predates publication of the activated generation, when activation becomes
ready and the reconciliation invocation runs, then the recovery component uses
the ordinary run-terminal mutation to terminalize it once as `outcome_unknown`.
Given a new claim lacks an adapter generation, the claim fails as
`generation_missing` before inference admission.

Given a target that retires before carrier admission, when admission runs, then
the target reaches `retired` and no turn is admitted.

Given a target that changes host or harness before carrier admission, when
admission runs, then the target reaches `no_longer_affected` and no turn is
admitted.

Given a target retires after carrier admission but before lane claim, when claim
runs, then inference is suppressed for that recovery turn and the target reaches
`retired`.

### A6 — Concurrent activation and dedupe

Given one open target carrier for generation 4, when generation 5 in the same
credential scope becomes ready before the session lane claims that carrier, then
the target's required generation becomes 5 and the system retains one
outstanding carrier.

Given the lane then claims that carrier at required generation 5, when its
delivered terminal transaction commits, then the target's handled generation
becomes 5.

Given generation 4 was handled before generation 5 became ready, when generation
5 becomes ready, then the ready transaction preserves generation 4's handled
membership, increments the persistent target's delivery cycle, changes target
state from `handled` to `pending`, and creates one new attempt-0 carrier.

Given a carrier was claimed with covered generation 4 before generation 5 became
ready, when that carrier reaches delivered, then it handles only generation 4
membership, increments the persistent target's delivery cycle, changes its state
directly from `claimed` to `pending`, and creates one attempt-0 carrier for
generation 5 in the same transaction.

Given generation 4 ended `undeliverable` and generation 5 later snapshots the
same active in-scope session, when generation 5 becomes ready, then the target
increments its delivery cycle, changes from `undeliverable` to `pending`, opens
attempt 0, and retains the generation-4 `undeliverable` membership as decision
state.

### A7 — Retry and final failure

Given a target whose attempts 0, 1, and 2 each end in typed
`could_not_run`, when the retry clock reaches each recorded due time, then the
system admits attempts 1, 2, and 3 once each at the specified delays.

Given attempt 3 also ends in `could_not_run` with no later required generation,
when its terminal transaction commits, then the target reaches `undeliverable`
and no later scheduler or boot pass creates attempt 4.

Given any attempt ends in `run_failed`, `run_canceled`, or `outcome_unknown` with
no later required generation, when its terminal transaction commits, then the
target reaches `undeliverable` without another attempt.

Given reconciliation attempts 0, 1, and 2 each reach typed `could_not_run`, when
the recorded due times arrive, then the ordinary scheduler invokes attempts 1,
2, and 3 before carrier admission at 5,000 ms, 30,000 ms, and 120,000 ms. Given
attempt 3 also cannot reconcile, then the membership reconciliation reaches
final `failed`, its open memberships reach `undeliverable`, the target follows
the generation-aware I9 transition, and inference is never admitted for that
carrier cycle.

### A8 — Crash and replay

Given a crash after credential metadata commits but before adapter readiness,
when boot reconciliation runs, then it continues the matching Activation ID or
records its typed failed edge from authoritative metadata.

Given a crash after the ready transaction commits but before scheduler nudge,
when boot reconciliation runs, then each missing carrier is delivered from the
existing target row and no duplicate target or carrier appears.

Given a crash after the ready transaction records a pending stranded-turn
reconciliation but before credential finish invokes it, when boot reconciliation
runs, then it invokes the same reconciliation identity, terminalizes the exact
old turn at most once, marks the membership reconciliation done, and releases the
lane without an old-adapter callback.

Given repeated ready, scheduler, terminal, and boot callbacks, when the database
settles, then unique identities leave one run, one target per session and scope,
one membership per activation and session, one reconciliation per recorded old
turn, and one row per delivery-cycle and attempt-number pair.

### A9 — Partial success and readback

Given credential and adapter success plus a forced target-plan transaction
failure, when finish returns, then it returns
`credential_recovered_recovery_plan_failed` with
`credentialRecovered = true`, `adaptersReady = true`,
`recoveryStarted = false`, and Activation ID.

Given the target plan commits but synchronous stranded-turn reconciliation
reaches typed `could_not_run`, when finish returns, then it reports
`credential_recovery_reconciliation_retrying`, the current attempt, the next due
time, and `recoveryStarted = true`.

Given a recovery with one handled target and one undeliverable target, when an
authorized caller reads it, then the aggregate reports
`credential_recovery_incomplete`, both membership resolutions, attempt counts,
linked turns, and the final typed cause.

Given overlapping activations 4 and 5 have different membership sets, when an
authorized caller reads activation 4 after generation 5 completes, then the
activation-4 aggregate derives only from activation-4 membership resolutions and
retains its original counts.

### A10 — Authorization and privacy

Given an admin, a target session, that target's owner, and an unrelated caller,
when each reads the same recovery, then the first three receive only their
authorized projection and the unrelated caller receives the existing
non-disclosing denial.

The test scans database rows, logs, prompts, finish results, and readback. It
fails on credential bytes, authorization codes, provider account identifiers,
email addresses, or external account labels.

### A11 — Real credential lifecycle smoke

Given an operator-approved disposable base directory, a throwaway provider
credential, two active sessions on that provider and host, one unrelated active
session, and an actual prior-generation turn running through the real Scheduler,
Gateway, Ledger, and SessionLane, the smoke shall use its controlled fault seam
to stop the old adapter without publishing that turn's terminal callback. The
ledger shall show that the child is gone while the turn and lane remain running.

When the supported onboarding command completes against the real replacement
provider adapter, then the ready transaction records the exact stranded turn and
its already-durable carrier. The recovery component, not an adapter callback,
terminalizes the stranded turn once as `outcome_unknown`, releases the lane, and
both matching sessions receive and handle real recovery turns without an
operator poke. The unrelated session receives none.

The smoke records redacted credential-commit, old and replacement adapter
generations, absent callback, pre-reconciliation running row, activation
membership, reconciliation identity, old-turn terminal, recovery-run, carrier,
recovery turn, and agent-owned resumption evidence. It records no secret. A
handwritten row, direct terminal callback, or fixture-only proof does not satisfy
this smoke.

### A12 — Regression and removal

Given the final implementation diff, when review inspects the successful
credential-finish path, then it finds no Main-only recovery scheduler and no
direct product-agent selection outside the exact I2 predicate.

Given the repository verification gates, focused deterministic lifecycle tests,
and A11 smoke, when each runs from a clean target baseline, then each reports a
passing result with baseline and final counts. A test suite that leaves one
affected runnable target dark or one stranded-turn reconciliation pending after
the lane can run fails acceptance.

## Open Questions

None. The implementation target remains unset by explicit owner ruling; it is
not a design hole.
