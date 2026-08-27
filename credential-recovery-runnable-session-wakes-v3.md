# Credential recovery wakes affected runnable sessions — v3

Status: PROPOSAL — INDEPENDENT REVIEW REQUIRED

Authority: Mike's product ruling
`att_c0d47267-eca0-49c9-9ac5-41c562b4dca7`, 2026-08-27.

Work item: `wi_82a81f78-5789-469e-863a-fb84d82781cd`.

Reconciled baselines: Tightbeam product `main` at
`8e269e89c04b6b8569813142a12742f3325b8503`; Tightbeam specs `main` at
`86b7ac83953dfd07c4e156f25902bd2f2d1390e3`.

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

The transaction shall insert or advance one recovery obligation for each
affected candidate. The selection and obligation writes shall commit as one
step.

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

Recovery shall append its own run, target, wake, turn, and audit rows. It shall
not reopen, cancel, replace, reorder, or mutate an existing assignment, work
item, message, wake, or terminal turn. It shall not retry an earlier inference
turn.

The recovery carrier shall enter the target's FIFO after an existing queued or
running turn. A later normal turn boundary, not elapsed time, permits it to run.

After activation becomes ready, the ordinary run boundary shall reconcile a
target's running turn when that run is stamped with an earlier adapter
generation. It shall terminalize the run exactly once as `could_not_run` when
durable evidence proves inference was not admitted. It shall terminalize the run
as `outcome_unknown` when admission occurred or cannot be disproved. It shall
never mark that run delivered and shall never retry it.

A run claimed before this feature recorded adapter generations is a
prior-generation run only when its durable claim time precedes the replacement
adapter generation's publication time and its session satisfies the exact I2
scope. The run boundary shall classify it as `outcome_unknown`; it shall not
infer pre-admission safety. After the feature is enabled, the run-claim
transaction shall reject a missing adapter generation as typed
`generation_missing` before it admits inference.

That typed terminal transition releases the session lane so its recovery carrier
can run. A running turn stamped with the activated adapter generation is not a
stranded prior-generation run; recovery leaves it in place and remains behind it
in FIFO order.

### I6 — One mutation seam owns recovery state

One recovery component shall own activation and target transitions. Credential,
scheduler, session-lane, boot, and readback code shall call that component. They
shall not write recovery state directly.

The component shall enforce these run states:

`prepared -> credential_installed -> activation_ready -> recovering -> complete`

`activation_ready` means that credential install, onboarded metadata commit,
adapter stop/start, and resume each succeeded. This state name does not prescribe
an order among those credential-lifecycle edges. Their source authority owns that
order.

It shall also permit a transition from a nonterminal state to `failed` with a
typed cause. A later credential ceremony creates a new Activation ID; it does
not rewrite the failed activation.

The component shall enforce these target states:

`pending -> admitted -> claimed -> handled`

Typed `could_not_run` permits `claimed -> retry_wait -> pending`. A target in
`pending`, `admitted`, `claimed`, or `retry_wait` may instead reach `retired`,
`no_longer_affected`, or `undeliverable` through the rules below.

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
stamped covered generation.

If required generation is later than handled generation after a carrier becomes
terminal, the terminal transaction shall open one later delivery cycle. This
rule covers both a later activation that became ready while the carrier ran and
a later activation that became ready after the prior generation was handled.
It shall not credit the earlier carrier with a generation that became ready
after the carrier was claimed.

When a later activation snapshots an affected candidate whose prior target state
is `undeliverable` or `no_longer_affected`, the ready transaction shall open one
later delivery cycle at attempt `0`. It shall retain the earlier terminal state
in audit history. A retired session cannot satisfy the active snapshot predicate.

Activations in different credential scopes shall not coalesce.

### I8 — Replay is idempotent

Activation ID shall be unique. The target identity shall be unique by
`{host, provider, sessionKey}`. Delivery cycle shall increase monotonically for
one target. One carrier attempt shall be unique by
`{targetIdentity, deliveryCycle, attemptNumber}`.

Replaying lifecycle callbacks, the ready transaction, scheduler passes, turn
terminal callbacks, or boot reconciliation shall reuse those identities. A
replay shall create no second obligation, carrier attempt, or final
disposition.

Boot reconciliation shall inspect nonterminal activation and target rows. It
shall continue the next deterministic edge when the matching onboarded
metadata and adapter state prove that edge. It shall record `failed` when the
authoritative metadata proves that activation did not commit. It shall not
infer success from credential-file contents or transcript text.

### I9 — Retry is finite and run-admission safe

Attempt `0` is the initial carrier. A carrier that reaches typed
`could_not_run` before inference admission shall permit attempts `1`, `2`, and
`3` after 5,000 ms, 30,000 ms, and 120,000 ms respectively.

The terminal transaction shall authorize the next attempt and record its due
time. Attempt `3` reaching `could_not_run` shall record `undeliverable`.

`run_failed`, `run_canceled`, and `outcome_unknown` shall record
`undeliverable` without retry. These classes cannot prove that retrying is
side-effect safe.

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
- `credential_recovery_complete`: each target reached handled or a typed final
  disposition.
- `credential_recovery_incomplete`: at least one target reached
  `undeliverable`.

The partial-success result shall carry `credentialRecovered`, `adaptersReady`,
`recoveryStarted`, and Activation ID. The credential result and recovery result
shall be separate typed fields. A caller can therefore observe that the new
credential is installed even when recovery planning or delivery is incomplete.

The boot reconciler shall retry a ready activation whose target-plan
transaction did not commit. An agent can start a later credential ceremony to
exit a failed activation. No database edit is required.

### I12 — Completion does not claim semantic obedience

An activation reaches `complete` when each snapshotted target has `handled`,
`retired`, `no_longer_affected`, or `undeliverable` for the required
generation.

The aggregate shall report `credential_recovery_incomplete` when one or more
targets are `undeliverable`. It shall report `credential_recovery_complete`
otherwise.

Handled does not prove work resumed. Agent-owned assignment, continuation, and
completion rows remain the evidence that stranded work resumed.

### I13 — Readback, authorization, privacy, and audit are explicit

The credential finish result and a persistent readback shall expose Activation
ID, host, provider, credential kind, generation, aggregate state, target counts
by state, attempt counts, next retry time, and typed failures.

An admin can read the activation aggregate and its targets. A target session can
read its own target row. The owner of a target session can read that target row.
Other callers receive the existing non-disclosing authorization failure.

Each activation and target transition shall record timestamp, cause kind, cause
row ID, and principal. Substrate transitions use `process:tightbeam`.

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
an operator poke. ADD wins only for the per-scope run and per-session obligation
state needed to survive crashes, coalesce concurrent activations, and prove that
no target stayed dark. The Main-only prompt and transcript-only recovery
mechanisms are removed from this path rather than retained beside it.

## Architecture

### A. Recovery ledger

The implementation shall add one run store and one target store.

The run store records Activation ID, credential scope, credential kind,
generation, run state, lifecycle timestamps, cause, principal, and aggregate
result.

The target store records credential scope, session key, required generation,
handled generation, covered generation, target state, delivery cycle, current
carrier wake ID, attempt number, next retry time, latest linked turn, typed
failure, cause, and principal.

The target store has one mutation seam, as required by I6. Lifecycle events are
audit projections. They are not decision state.

### B. Credential-lifecycle bracket

Before credential mutation, the credential owner asks the recovery component to
prepare an Activation ID. The credential lifecycle persists that ID with its
non-secret Tightbeam-owned activation metadata. After each credential and
adapter edge, it records the edge through the component. After credential
install, onboarded metadata commit, adapter stop/start, and resume succeed, it
asks the component to atomically mark the activation ready, snapshot affected
candidates, advance target generations, and create missing attempt-0 carriers.

The finish response returns after this transaction commits. Carrier delivery is
asynchronous and visible through readback.

### C. Carrier lifecycle

The ordinary scheduler admits a recovery carrier through the active-session
gate. The admission and claim transactions revalidate the session scope. Before
the lane can remain blocked behind a prior-generation run, the existing run
boundary terminalizes that run under I5 and publishes its ordinary terminal
event. The session lane then runs the linked recovery turn in FIFO order. The
turn terminal transaction updates the target through the recovery component.

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
targets and one carrier for each target.

The retired, other-host, and other-provider sessions receive no carrier. The
test fails if routing depends on archetype, Kung Fu, product owner, or Main
fanout.

### A3 — Each runnable target receives a real turn

Given the A2 org and real Scheduler, Gateway, Ledger, and SessionLane processes,
when the three target sessions can each complete an ordinary turn, then each
recovery carrier reaches one delivered linked turn and each target reaches
handled for the required generation.

The test fails if one target remains pending, admitted, claimed, retry-waiting,
unlinked, or absent after the lane becomes idle. A transcript insertion or
direct terminal-row fixture does not satisfy this check.

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
evidence, when activation becomes ready, then the run boundary terminalizes that
turn once as `could_not_run`, does not retry it, releases the lane, and the
recovery carrier can reach a real turn.

Given a target has a running prior-generation turn whose inference admission
occurred or is unknown, when activation becomes ready, then the run boundary
terminalizes that turn once as `outcome_unknown`, does not retry it, releases the
lane, and the recovery carrier can reach a real turn.

Given a matching historical running turn has no adapter-generation stamp and its
claim predates publication of the activated generation, when activation becomes
ready, then the run boundary terminalizes it once as `outcome_unknown`. Given a
new claim lacks an adapter generation, the claim fails as `generation_missing`
before inference admission.

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
5 becomes ready, then the system creates one new carrier.

Given a carrier was claimed with covered generation 4 before generation 5 became
ready, when that carrier reaches delivered, then it handles only generation 4
and the terminal transaction opens one later delivery cycle for generation 5.

Given generation 4 ended `undeliverable` and generation 5 later snapshots the
same active in-scope session, when generation 5 becomes ready, then the target
opens one later delivery cycle at attempt 0 and retains the generation-4 failure
in audit history.

### A7 — Retry and final failure

Given a target whose attempts 0, 1, and 2 each end in typed
`could_not_run`, when the retry clock reaches each recorded due time, then the
system admits attempts 1, 2, and 3 once each at the specified delays.

Given attempt 3 also ends in `could_not_run`, when its terminal transaction
commits, then the target reaches `undeliverable` and no later scheduler or boot
pass creates attempt 4.

Given any attempt ends in `run_failed`, `run_canceled`, or `outcome_unknown`,
when its terminal transaction commits, then the target reaches
`undeliverable` without another attempt.

### A8 — Crash and replay

Given a crash after credential metadata commits but before adapter readiness,
when boot reconciliation runs, then it continues the matching Activation ID or
records its typed failed edge from authoritative metadata.

Given a crash after the ready transaction commits but before scheduler nudge,
when boot reconciliation runs, then each missing carrier is delivered from the
existing target row and no duplicate target or carrier appears.

Given repeated ready, scheduler, terminal, and boot callbacks, when the database
settles, then unique identities leave one run, one target per session and scope,
and one row per delivery-cycle and attempt-number pair.

### A9 — Partial success and readback

Given credential and adapter success plus a forced target-plan transaction
failure, when finish returns, then it returns
`credential_recovered_recovery_plan_failed` with
`credentialRecovered = true`, `adaptersReady = true`,
`recoveryStarted = false`, and Activation ID.

Given a recovery with one handled target and one undeliverable target, when an
authorized caller reads it, then the aggregate reports
`credential_recovery_incomplete`, both target states, attempt counts, linked
turns, and the final typed cause.

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
credential, two active sessions on that provider and host, and one unrelated
active session, when the supported onboarding command completes against the
real provider adapter, then both matching sessions receive and handle recovery
turns without an operator poke and the unrelated session receives none.

The smoke records redacted credential-commit, adapter-generation, recovery-run,
target, wake, turn, and agent-owned resumption evidence. It records no secret.
The feature does not ship from a fixture-only proof.

### A12 — Regression and removal

Given the final implementation diff, when review inspects the successful
credential-finish path, then it finds no Main-only recovery scheduler and no
direct product-agent selection outside the exact I2 predicate.

Given the repository verification gates, focused deterministic lifecycle tests,
and A11 smoke, when each runs from a clean target baseline, then each reports a
passing result with baseline and final counts. A test suite that leaves one
affected runnable target dark fails acceptance.

## Open Questions

None. The implementation target remains unset by explicit owner ruling; it is
not a design hole.
