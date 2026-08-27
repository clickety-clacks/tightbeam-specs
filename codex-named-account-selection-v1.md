# Codex named-account selection — v1

Status: SPEC READY FOR ONE PARENT-OPENED INDEPENDENT EXACT-SUCCESSOR RE-REVIEW. The work
item remains targetless. This revision authorizes no implementation, merge, release,
deployment, live selection, credential change, account change, or spec-ref binding.

Canonical spec home: repository `github.com/clickety-clacks/tightbeam-specs`,
repository-relative path `codex-named-account-selection-v1.md`. A review or handoff
identifies one exact revision by repository commit and file SHA-256. Artifacts and
workspace copies are evidence; they are not alternate canonical homes.

Authority: `wi_008ad6d7-d976-4120-9e90-8557a24f7602`, recon verdict
`att_ae78b652-70ad-484e-b2ac-ed3062ab58ce`, and report `art_f245e870` at SHA-256
`09e57edcd8102141f269359004b1effd4e9c1bf3874ea2b6a533a93a48ebeba3`.
The successor also answers independent changes-requested verdict `att_de28818e` and
report `art_5d90dcdd` at SHA-256
`e8556161e30d3de18de219e69639fedfcc0c1c3c022fc028eb85512e768871f1`.
This revision answers second independent changes-requested verdict `att_790131ff` and
report `art_415178b8` at SHA-256
`8c0d122dd540d404582a8b3f65847decb2d9637f13f7e7a211bca63c61923ec2`.
It also answers third independent changes-requested verdict `att_2cbb5bcd` and report
`art_e7a71cfa` at SHA-256
`86e50680ff6b54760c57c6621d7b1bbddd33fadfd23be0223ddd03a97f178e14`.
This revision answers fourth independent changes-requested verdict
`att_69f2b5c6-15e8-4b5d-8c3e-662a71f62d82` and report `art_2e4c22ac` at SHA-256
`7f83ebcb89183f9859611ab94c081adafd34a26028f17ecd3f714b00e5dcd769`.

This spec introduces the **Named harness-account binding** pattern. It applies to one
Tightbeam harness on one registered host and names a non-secret account identity held
by the provider-account custodian on that host. V1 applies the pattern only to the
Codex harness and Lachesis. It does not apply to model selection, agent placement,
or Claude. It adds no account lifecycle action.

Subtraction ruling: ADD wins because deleting account choice leaves the stated repair
verb absent, while accepting the failure preserves the measured org-wide outage. The
addition is one typed binding, one mutation seam, one agent-reachable verb, one
custodian activation operation with process handoff, and reuse of the existing adapter
and harness-health seams.
The review repairs extend those same seams with a typed candidate role, bounded activation
and transition ownership, generation-correlated failure evidence, and an explicit
park-release transition. Deleting any repair loses proof-before-publish, account lifecycle
exclusion, the shared incident, migration recovery, or the required human fallback;
accepting any race can publish an unproved binding/adapter pair or park the wrong source.

## Goal

Give an authorized Tightbeam agent a restart-safe command that binds the Codex harness
on one registered host to an explicitly named, ready Lachesis Codex account with
provider capacity. The command proves the candidate through the real adapter boot path
while Lachesis excludes account lifecycle mutation. It then publishes the new binding
and ready adapter as one source transition. It returns the selected non-secret account
identity.

When the selected account emits the exact Codex `usageLimitExceeded` event and Lachesis
shows a healthy alternate on the same host, record one host-scoped harness-health
incident. The incident reports the selected identity and the healthy alternate
identities. It suppresses per-assignment effort prods through the existing
`HarnessHealth` gate. A successful ready-source transition releases the incident's
adapter park without resolving the incident, so one ordinary proof turn can run. A mind
chooses whether to invoke the selection command.

Maxim: **Tightbeam records which host harness uses which custodian-owned account; only
the harness reads that account's credential.**

## Non-Goals

- V1 does not select an account automatically.
- V1 does not fail over after a provider failure.
- V1 does not rank accounts by plan, remaining capacity, cost, reset time, or label.
- V1 does not register, adopt, deregister, re-onboard, refresh, edit, copy, or delete a
  Lachesis account or credential.
- V1 does not add account selection for Claude or another harness.
- V1 does not move a credential or credential byte between hosts.
- V1 does not expose credential bytes through a Tightbeam request, response, row, log,
  lifecycle event, condition fact, artifact, or error.
- V1 does not replace `tightbeam onboard openai`. Interactive onboarding remains the
  human fallback and the owner of Tightbeam-managed OpenAI credentials.
- V1 does not change agent placement, model selection, model fallback policy, or
  session ownership.
- V1 does not create a new fault table, fault queue, adjudicator, account chooser, retry
  loop, or polling process.
- V1 does not create a second adapter key for a candidate or bypass the durable harness
  process ledger.
- V1 does not persist an activation or process-owned lock as account lifecycle state or
  as a durable Tightbeam binding field.
- V1 does not choose an implementation branch, release line, release version, host for
  deployment, or deployment time.
- V1 teaches no new operating pattern to agents beyond the command contract in this
  spec. No substrate-manual or identity-guidance amendment ships with it.

## Terms

- **Registered host**: a host row returned by Tightbeam's existing host registry. Its
  canonical identity is the row's `name`. The gateway's local host is the registered
  host whose `ssh` value is `nil`.
- **Harness key**: `{harness, host}`. V1 accepts only `{codex, <registered-host>}`.
  The adapter layer can include its existing shared-archetype component internally;
  that component does not create another account binding.
- **Lachesis account identity**: the non-secret tuple `{id, label, provider}` returned
  by Lachesis `GET /api/v1/accounts`. `id` is the stable identity. `label` is display
  text. `provider` must be `codex` in V1.
- **Tightbeam-managed source**: the OpenAI credential installed by
  `tightbeam onboard openai` in Tightbeam's existing host-local credential store. It is
  the implicit source when no named binding row exists.
- **Named binding**: the durable Tightbeam row that maps one harness key to one
  Lachesis account identity. The row stores no provider-home path and no credential
  material.
- **Binding revision**: a non-negative integer used for compare-and-swap. The implicit
  Tightbeam-managed source has revision `0`. Each successful ready-source transition
  increments the revision by one.
- **Candidate source**: either the Lachesis account identity named in one selection
  request or the staged Tightbeam-managed credential from one interactive onboarding
  finish. Its source digest covers only `{source_kind, account_id, expected_revision}`;
  it never hashes credential bytes or a provider-home path.
- **Ready account**: a Lachesis account for which the consumer activation's initial
  frame returns `status: "ready"`, `working: true`, and `mutationState: "idle"` while
  Lachesis holds the account operation lock and has established that no provider process
  already uses the account's provider home.
- **Capacity-positive sample**: a synchronous Lachesis usage result whose `status` is
  `live` or `cache`, whose `sample.windows` contains at least one window, and for which
  each window has `used_percent < 100`. `stale`, `error`, a missing sample, an empty
  window set, a non-number, or `used_percent >= 100` does not establish capacity.
- **Healthy alternate**: a different Lachesis account on the target host whose provider
  is `codex`, whose account view is ready, and whose synchronous usage result is
  capacity-positive.
- **Consumer activation lease**: one connection-scoped Lachesis operation that acquires
  the account's existing exclusive operation lock, proves provider, readiness, mutation
  idleness, capacity, and absence of a provider process already using the exact account
  home, and returns that home for the provider CLI. Lachesis assigns an activation ID and
  an absolute expiry 200,000 milliseconds after lock acquisition. Before process handoff,
  it releases the lock on response closure, expiry, or Tightbeam cancellation, whichever
  happens first. The lease contains no credential bytes, account mutation, durable
  account field, or caller-chosen timeout.
- **Consumer process handoff**: the one-shot final frame on a consumer activation. After
  the real ready token, Tightbeam supplies the exact candidate OS process identity.
  Lachesis verifies that process against the leased provider home and atomically transfers
  the existing operation-lock owner from the activation connection to that process.
  Handoff and activation expiry linearize in the same Lachesis account state machine.
  Process exit releases the transferred lock. The handoff creates no second lock, durable
  account field, credential access, renewal, or caller-selected duration.
- **Process role**: `serving`, `candidate`, or `retiring` on one durable harness-process
  row. The role is subordinate to the unchanged adapter key; it is not another routing
  key. At most one unresolved row of each role exists for one adapter key.
- **Candidate adapter**: an unpublished process with role `candidate`, a unique launch
  ID, the selection operation ID, and the candidate source digest under the existing
  Codex adapter key on the target host. A lane cannot check it out before commit.
- **Ready-source transition**: the sole coordinator-owned critical section that stages
  one candidate and atomically publishes a binding revision, process-role promotion,
  adapter generation, and any repair-park release. Both `account-select` and successful
  interactive onboarding use it.
- **Source-transition reservation**: non-waiting coordinator ownership for one ready-source
  transition. It has a safe owner operation key and expires 240,000 milliseconds after acquisition.
  A competing transition receives `source_transition_busy`; it does not queue. Owner death,
  expiry, the owning ceremony's cancel path, or same-verb selection cancellation aborts the
  reservation and settles its candidate.
- **Incident-owned park**: a durable harness park fence whose `ownerKind` is
  `harness_health_incident` and whose `ownerId` is the exact open incident. V1 never
  releases an operator-owned, cleanup-owned, or differently owned fence. It releases a
  legacy fence only through an explicitly requested, exact-ID migration transition.
- **Health proof**: the existing Codex adapter boot gate reaches its ready token while
  the candidate adapter uses the candidate's consumer binding. V1 adds no timer or
  synthetic health test; it uses the current adapter boot deadline and real gate.
- **Selection operation**: one call of the `account-select` verb, whose safe operation key
  is the caller's idempotency key, from authorization through validation, candidate proof, commit,
  and response. The same verb's cancel mode can abort an active operation before commit.
- **Selected-account exhaustion observation**: an existing
  `HarnessHealth` `rate-limit-dead` authoritative-provider observation whose cause is
  the exact Codex `usageLimitExceeded` event plus an immutable match between the turn's
  checkout generation, the named binding revision that produced that generation, and the
  still-current serving source, with at least one healthy alternate.

## Assumptions

- Tightbeam source `main` identifies an adapter by harness, shared archetype, and host.
  `AdapterCoordinator` already owns adapter generation and readiness, while
  `HarnessProcess` owns durable launch identity and reconciliation. Current source
  permits one unresolved process per adapter key; V1 extends that ledger with typed
  roles without changing the adapter key.
- Tightbeam already records one open `HarnessHealth` incident per
  `{harness, host, failure_class}` and suppresses supervision prods while its condition
  fact stands. Current `rate-limit-dead` incidents also create a durable adapter park;
  V1 preserves the incident while releasing that park only after a ready source is
  published.
- Tightbeam's host registry and authorization machinery are durable DB-backed seams.
- Lachesis runs on `127.0.0.1:7843` on the host that owns its accounts. Remote access
  from the Tightbeam gateway uses the existing registered-host SSH transport and calls
  that loopback endpoint on the target host.
- Lachesis remains the registry and credential custodian for its accounts. Its provider
  homes are file-backed. The Codex CLI remains the writer and refresher inside a
  selected Codex provider home.
- Lachesis already serializes verify, refresh, delete, re-onboard, and job operations with
  one per-account operation lock. Ordinary usage reads do not acquire that lock. The V1
  activation operation acquires the existing lock first, establishes provider-process
  absence for the exact provider home, then performs its verify and synchronous capacity
  read without reacquiring the lock. V1 adds no second lock or account mutation state.
- Lachesis account IDs are stable across service restarts. Labels are non-secret display
  values and do not identify a binding without the ID.
- Lachesis `POST /api/v1/accounts/{id}/verify` observes credential and usage state. It
  does not mutate the account registry or credential.
- Lachesis `GET /api/v1/accounts/{id}/usage?refresh=wait` returns the normalized provider
  windows that decide whether the account can accept provider work at that observation.
- Tightbeam's existing interactive OpenAI onboarding can stage and prove a
  Tightbeam-managed credential without reading credential bytes into the gateway.
- The implementation revision will capture real Lachesis and Codex adapter responses
  for boundary fixtures before implementation acceptance runs.

## Invariants

**I1 — one typed binding per harness key.** A harness key resolves to either the
implicit Tightbeam-managed source or one named Lachesis account. A second current row
for the same harness key is unrepresentable through the primary key.

**I2 — one source-transition seam.** One Tightbeam binding module owns comparison,
commit, history, and projection. One `AdapterCoordinator` seam owns candidate
staging and publication for a harness key. `account-select` and interactive onboarding
finish call that same ready-source transition. No adapter, placement, CLI, migration,
credential callback, or health component writes binding state or publishes a replacement
generation directly.

**I3 — host confinement.** A selection for host A queries Lachesis on host A, stages
the Codex adapter on host A, and changes only `{codex, A}`. It does not query an account
home on host B or change a binding, adapter, session, credential, or account on host B.

**I4 — custodian ownership.** Tightbeam stores the Lachesis account ID, label, and
provider. It receives the consumer-binding path transiently and passes it to the target
adapter launch. Tightbeam does not read, parse, write, copy, archive, log, or return the
credential file. Lachesis owns account registry and provider-home lifecycle. Codex owns
credential refreshes inside the selected home.

**I5 — explicit choice.** The substrate executes the account ID supplied by the caller.
It does not choose from alternatives. Capacity and readiness checks can refuse the
supplied choice; they cannot replace it.

**I6 — check and exclude before publish.** Authorization, host existence, harness
support, account existence, provider match, readiness, mutation idleness, capacity,
consumer binding, absence of a process already using that provider home, expected
revision, and candidate adapter health must pass before the named binding becomes
current. The Lachesis account operation lock stays held by the activation from the final
provider/readiness/capacity observations through candidate proof. Before publication,
Lachesis atomically hands that same lock to the exact proven candidate process. Refresh,
re-onboard, delete, and credential-affecting jobs cannot begin while either owner holds
it. Activation expiry before handoff settles the candidate and leaves the prior source
authoritative. If handoff wins, activation expiry cannot release the process-owned lock;
candidate exit becomes the only lock-release event. The enclosing reservation still
expires after 240,000 milliseconds.

**I7 — old path stays authoritative until proof.** During candidate staging, the durable
binding remains unchanged. When the prior adapter is serving, lanes keep using it. When
an open rate-limit incident has already parked it, the park and prior binding remain the
authoritative failed state. A failed activation or health proof resolves only the
candidate process row; it neither releases the park nor changes the prior binding or
published generation.

**I8 — serialized source transition.** Every binding-changing operation for one harness
key, including `account-select` and interactive onboarding finish, shares one critical
section from transition reservation through publication. After authentication, the
binding module returns a completed exact replay or `idempotency_conflict` before the
caller consults transition ownership. A replay therefore cannot return
`source_transition_busy`. The coordinator reservation
does not block the coordinator process: ordinary checkouts and calls from the reservation
owner continue. Reservation acquisition is non-waiting; another source-transition request
receives `source_transition_busy` with the safe operation key and expiry and performs no
Lachesis, credential-install, or candidate action. The owner, an authorized same-verb
selection cancel, onboarding cancel, owner death, or the fixed reservation deadline can
abort ownership before commit. The implementation rechecks
authorization, activation or process-handoff ownership when applicable, and binding
revision at the commit boundary. A named candidate must also retain its acknowledged process handoff.
`AdapterCoordinator`, the existing single owner of checkouts and
generations, owns the final publication call. While that call is running, it executes
the binding and process-role transaction and swaps the ready candidate into the current
generation before it serves another checkout or source transition. A failed transaction
discards the candidate. Binding commit and candidate publication are therefore one
serialized operation from the perspective of every supported reader.

**I9 — crash boundary.** A candidate exists durably only as a typed harness-process row,
never as binding state. Before the publication transaction commits, gateway startup
terminates and resolves the candidate row, restores any park required by an open
rate-limit incident, and resolves the prior binding. After the transaction commits, the
candidate row is already `serving`, the prior row is `retiring`, and startup resolves the
new binding. Reconciliation terminates unresolved `candidate` and `retiring` processes
before serving a checkout. No durable pending-selection binding exists.
Every launch or relaunch from a committed named binding, including restart recovery after
the serving process is absent, reacquires a bounded consumer activation for that exact
account, derives the transient home, and holds the account operation lock until the real
adapter ready token. Lachesis then hands the same lock to that exact process before it can
become serving. A launch that loses activation, exceeds activation, or fails process
handoff does not become serving.

**I10 — idempotent result.** A caller supplies a non-empty idempotency key. The completed
result is keyed by `{principal, account-select, idempotency_key}` and bound to a digest
of `{host, harness, account_id, expected_revision, cause, repair_legacy_park}`. Repeating
the same digest returns the recorded result without another activation lease, adapter
stage, generation change, or binding change. Reusing the key with a different digest
returns `idempotency_conflict`.
Cancel mode is keyed by `{principal, account-select-cancel, harness_key,
idempotency_key}` and bound to a digest of `{host, harness, operation_key, cause}`.
Repeating the same digest returns its recorded safe outcome. Reusing the key with a
different digest returns `idempotency_conflict`. Cancel after publication returns
`selection_not_active` and cannot undo the committed transition.

**I11 — cause and principal.** Each selection attempt records the authenticated
principal, the caller's non-empty cause, request digest, target harness key, candidate
identity, prior identity, observed Lachesis result, final outcome, binding revision,
and timestamp. The record contains no credential bytes or consumer-binding path.

**I12 — selection does not mutate an account.** The selection operation may list
accounts and acquire one consumer activation lease. Lease acquisition performs verify,
usage, and consumer-binding reads while holding Lachesis's existing account operation
lock. Its process handoff transfers only the transient owner of that lock. Selection does
not call account create, adopt, delete, refresh, re-onboard, job, or code-submission
endpoints. Releasing or losing the activation, handing the lock to the exact candidate,
or releasing it on candidate exit changes only transient lock ownership, not account or
credential state.

**I13 — one shared exhaustion incident.** Each checkout records its adapter key and
generation on the turn. Each published generation has an immutable safe mapping to its
binding revision and source identity. The exact `usageLimitExceeded` event triggers an
alternate check only after the production joins the turn to that mapping and proves at
its transaction boundary that the same generation, revision, and named identity are still
serving. When the check finds a healthy alternate, it files one authoritative observation into the existing
`rate-limit-dead` incident for `{codex, host}`. The existing unique-open-incident rail
absorbs later observations. Assignment-specific failures remain evidence attached to
that incident; supervision does not emit per-assignment effort prods while the incident
stands.

**I14 — alternatives are information.** The exhaustion observation reports the selected
`{id, label, provider}`, binding revision, serving generation, triggering turn sequence,
and each healthy alternate's `{id, label, provider, windows}`. A late event whose serving
mapping is no longer current remains turn evidence but cannot open, update, park, or
re-park an incident. The production does not invoke `account-select`, change a binding,
or mark an assignment complete or failed.

**I15 — recovery remains evidence-based.** A successful ready-source transition does
not retract the rate-limit incident. Its publication transaction releases the adapter
park for `{codex, host}` after the replacement is ready only when that fence is owned by
the exact open incident. This permits the normal turn path to run. The first ordinary
delivered turn from the released generation and binding revision resolves the incident.
If publication fails, the park remains. Park
release alone does not resolve or suppress evidence.
Only a delivered turn checked out from the generation and binding revision recorded in
the incident's release fields can resolve that incident or re-establish its park. A late
turn from a retired generation changes neither field nor fence.

**I16 — onboarding remains the human exit.** `tightbeam onboard openai` keeps its
interactive ceremony. Begin captures the current safe binding revision in the onboarding
lease. Finish enters the same per-key ready-source transition as `account-select`, proves
a Tightbeam-managed candidate, and publishes only if that captured revision still
matches. A concurrent source transition produces `source_transition_busy`; after the
winner commits, retry with the captured revision produces `binding_conflict`. Neither
outcome silently overrides the winner. A failed or conflicting ceremony leaves the current named binding,
published adapter generation, and repair park unchanged.
Onboarding finish uses the same fixed 240,000-millisecond reservation deadline. Existing
onboarding cancel, owner death, or expiry aborts the reservation and runs the existing
staged-credential cleanup path.

**I17 — no topology constant.** The selector resolves the registered host and current
Codex adapter key from live registry and harness data. It does not hardcode Gibson,
Eezo, an org ID, an account ID, a session, an archetype roster, or a release line.

## Architecture

### A. Binding state and mutation seam

Add a DB-backed current projection keyed by `(harness, host)`. Its logical fields are:

```text
harness            "codex"
host               registered host name
source_kind        "tightbeam_managed" | "lachesis"
account_id         null | Lachesis account ID
account_label      null | Lachesis display label
provider           "openai" for tightbeam_managed | "codex" for lachesis
revision           non-negative integer
selected_at_ms     epoch milliseconds
selected_by        authenticated principal
cause              non-empty caller cause
```

An absent row projects as `tightbeam_managed`, revision `0`. The database enforces the
source/account nullability combination and the `(harness, host)` primary key.

The binding module is the sole writer. It writes one append-only attempt record for a
completed `account-select` result and one append-only binding-change record for a
successful change. Both records carry principal and cause. Update and delete triggers
protect their identity fields and history. The attempt record stores the request digest
and safe response so an exact replay is restart-safe.

Each binding-change record stores the promoted launch ID. Every serving harness-process
row stores its adapter generation and binding revision; ordinary relaunch writes the same
current revision on its new row. Binding history maps that revision to the safe source
identity. The turn ledger's existing checkout generation joins through the process row to
that immutable history; exhaustion processing never substitutes the current binding for
a turn's recorded generation.

This takes the **unrepresentable** rung for duplicate current bindings, illegal source
shapes, and history deletion. Authorization, provider liveness, and account capacity
remain runtime checks because they depend on external observations.

### B. Lachesis consumer activation lease

Add one supported Lachesis operation:

```http
POST /api/v1/accounts/{id}/consumer-activation
Content-Type: application/x-ndjson
Accept: application/x-ndjson
```

The first request frame is `{"action":"open"}`. Lachesis resolves the exact account, acquires that account's
existing operation lock, refuses a non-idle lifecycle state, and runs the provider-process
check for the account's exact provider home while it owns the lock. A matching process or
an inspection result that cannot establish process absence returns `account_busy` and
releases the lock. This backstops both orphaned provider processes and transient lock loss
after a Lachesis restart. Only after that check establishes absence does Lachesis perform
verify and one synchronous provider-capacity read without re-entering the lock-taking
service path. The first response frame is either one typed refusal or:

```json
{
  "account": {
    "id": "<id>", "label": "<label>", "provider": "codex",
    "status": "ready", "working": true, "mutationState": "idle"
  },
  "usage": {
    "status": "live",
    "sample": {"windows": [{"name": "primary", "used_percent": 42}]}
  },
  "consumerBinding": {"kind": "provider_home", "home": "/absolute/provider/home"},
  "lease": {
    "kind": "connection", "activationId": "act-7",
    "expiresAtMs": 1787850000000
  }
}
```

After that frame Lachesis keeps the duplex stream open and retains the operation lock.
Before the real ready token, response closure or the server-assigned expiry exactly
200,000 milliseconds after lock acquisition releases the lock. Tightbeam cancellation
closes the stream. The endpoint has no renewal verb, heartbeat poller, caller-selected
duration, or durable lease row. `activationId` exists only in Lachesis memory for the
activation and in Tightbeam's in-memory operation state; neither side persists or logs it.
Refresh, re-onboard, delete, and credential-affecting jobs use the same existing lock and
therefore cannot start while the activation owns it.

Lock acquisition is non-waiting; an owned lock returns `account_busy`. The operation
reads the registry row and normalized file store binding. It returns no
credential path below the provider home and no credential bytes. A keychain or
unsupported store returns a typed refusal before it grants the lease. Verify or usage
failure closes the response. The operation returns direct observations without updating
account status, mutation state, registry state, usage cache, provider-home contents, or
credential state.

After the candidate reaches the real ready token, Tightbeam sends one final request frame:

```json
{"action":"process_handoff","activationId":"act-7","process":{"pid":321,"startToken":"os-start-9"}}
```

Lachesis verifies that the exact live process belongs to the activation's provider home.
Under the same per-account state machine, it linearizes this frame against activation
expiry. If expiry wins, Lachesis releases the connection-owned lock and returns
`operation_deadline_exceeded`; Tightbeam settles the candidate. If handoff wins, Lachesis
changes the transient owner of the existing operation lock from the connection to that
exact process and returns `{"status":"process_bound"}`. The original expiry can then close
the stream but cannot release the process-owned lock. Tightbeam publishes only after it
receives `process_bound` and while the coordinator still observes that exact process as
live and ready. Process exit releases the lock and invalidates an uncommitted publication.

Each Lachesis operation that can mutate an account row, credential, or provider home,
including delete, refresh, re-onboard, and credential-affecting jobs, acquires the existing
operation lock. It also performs the provider-process check for that exact provider home
while it owns the lock. This extends the existing refresh and re-onboard guard to every
named lifecycle mutation, including delete. The check preserves exclusion after a Lachesis
restart reconstructs no transient process owner. Tightbeam keeps `home`, `activationId`,
PID, and start token only in memory.
It omits them from DB rows, CLI output, firehose, lifecycle events, artifacts, and
selection-attempt records.

### C. Agent-reachable wire and CLI

Add one dispatch verb with select and cancel modes:

```text
tightbeam account-select \
  --host <registered-host> \
  --harness codex \
  --account <lachesis-account-id> \
  --if-revision <non-negative-integer> \
  [--repair-legacy-park] \
  --cause <non-empty-text> \
  --key <idempotency-key>

tightbeam account-select \
  --cancel \
  --host <registered-host> \
  --harness codex \
  --operation-key <active-selection-idempotency-key> \
  --cause <non-empty-text> \
  --key <cancel-idempotency-key>
```

Wire parameters use camel case:

```json
{
  "verb": "account-select",
  "params": {
    "host": "gibson",
    "harness": "codex",
    "accountId": "acct-2",
    "expectedRevision": 0,
    "cause": "recover provider capacity for asg_example",
    "idempotencyKey": "asg-example-select-acct-2",
    "repairLegacyPark": false
  }
}
```

Cancel mode uses the same `account-select` verb with `action: "cancel"`, `host`,
`harness`, `operationKey`, `cause`, and its own `idempotencyKey`. It authenticates under
the same admin mutation rule. Before commit it closes the matching activation connection,
settles the exact candidate, aborts the reservation, and records cancel principal and
cause. It cannot cancel onboarding, another harness key, an operation whose key does not
match, or a committed transition. Onboarding continues to use its existing cancel path.
The cancel idempotency digest covers `host`, `harness`, `operationKey`, and `cause`.
Reusing a cancel key with a changed target or cause returns `idempotency_conflict` and
does not affect either selection.

Select mode may set `repairLegacyPark: true`. This is an explicit compare-and-replace
request for the one legacy fence on the target key; omission never infers permission to
remove it. The operation records the flag in its request digest and audit history.

Authorization matches existing host and credential mutations: an admin user or an active
session owned by an admin user can call it. Process principals and sessions owned by a
non-admin user receive `not_authorized`. The gateway derives the principal from the
credential; the request cannot supply or override it.

On success, stdout and the wire return only:

```json
{
  "changed": true,
  "binding": {
    "host": "gibson",
    "harness": "codex",
    "source": "lachesis",
    "revision": 1,
    "account": {"id": "acct-2", "label": "work", "provider": "codex"}
  },
  "adapter": {"key": "codex:shared@gibson", "generation": 7, "ready": true}
}
```

An exact idempotent replay returns the recorded safe response with
`"idempotentReplay": true` and no effect.

`tightbeam list` adds an `accountBindings` projection with the same safe binding fields.
The implicit Tightbeam-managed source appears with revision `0` and `account: null`.
The projection contains no consumer home or credential field.

Typed refusals are:

| Code | Decidable condition | Effect |
| --- | --- | --- |
| `not_authorized` | principal fails the existing admin mutation rule | none |
| `unknown_host` | host registry has no target row | none |
| `unsupported_harness` | harness is not `codex` in V1 | none |
| `binding_conflict` | current revision differs from `expectedRevision` | none; return current safe binding |
| `source_transition_busy` | another bounded reservation owns the key | none; return safe operation key and expiry |
| `lachesis_unavailable` | target-host activation connection cannot complete | none |
| `account_not_found` | Lachesis list has no exact account ID | none; return safe known IDs |
| `account_provider_mismatch` | account provider differs from `codex` | none |
| `account_busy` | mutation state differs from `idle`, an activation or lifecycle operation owns the account lock, or Lachesis cannot establish that no provider process uses the exact home | none |
| `account_not_ready` | verify does not return ready and working | none |
| `account_capacity_exhausted` | usage result is not capacity-positive | none; return normalized windows |
| `consumer_binding_unavailable` | Lachesis cannot return a file-backed provider home | none |
| `park_owner_conflict` | a park stands but is not owned by the exact open rate-limit incident | resolve candidate; prior binding, generation, and park remain |
| `legacy_park_repair_required` | a legacy park stands and select mode omitted `repairLegacyPark` | none; return the safe fence kind and remedy |
| `legacy_park_not_found` | select mode requested legacy repair but the observed fence is absent or not legacy | none |
| `activation_lease_lost` | Lachesis activation connection closes before process handoff | resolve candidate; prior binding, generation, and park remain |
| `operation_deadline_exceeded` | activation expires before process handoff or transition reservation expires before commit | close activation, resolve candidate, abort reservation; prior state remains |
| `selection_not_active` | cancel mode finds no matching uncommitted selection | none |
| `candidate_activation_failed` | candidate adapter fails to start, reach ready, or match process handoff | resolve candidate; prior binding, generation, and park remain |
| `process_cleanup_required` | an exact candidate or retiring process cannot be terminated and settled | fence key; return safe current binding and whether publication committed |
| `idempotency_conflict` | key exists with a different request digest | none |

Each refusal names the failed check, the safe non-secret account identity when known,
the current binding revision, and one concrete remedy. A refusal does not suggest
another account as the selected outcome.

### D. Durable candidate lifecycle and atomic boundary

Extend `harness_processes` with logical fields `role`, `transitionId`, `sourceDigest`,
`bindingRevision`, and `adapterGeneration`. `role` is `serving`, `candidate`, or `retiring`. The schema permits at
most one unresolved row per `{adapterKey, role}`. A candidate child has a unique process
identity derived from its launch ID, not a second adapter key. Ordinary adapter checkout
reads only the coordinator's `serving` entry.
Once non-null, `bindingRevision` and `adapterGeneration` are immutable on that launch row.
Settlement can change process status and role but cannot rewrite which source generation
the row served.

The coordinator's per-key state has separate serving, candidate, and retiring slots.
Every monitor, ready signal, close request, and settlement names `{adapterKey, role,
launchId}`. A delayed ready or `DOWN` from one launch can update only that launch's row
and slot. Candidate promotion and retiring cleanup never call a "latest process for key"
mutation that could settle the newly serving launch by mistake.

`HarnessProcess.prepare_candidate_launch` is the sole candidate-launch seam. It can
create a `candidate` row while a `serving` row and a rate-limit park fence exist, because
the candidate is not routable to a lane. It refuses while any unresolved `candidate` or
`retiring` row exists. Ordinary `prepare_launch` retains its current fence refusal. The
candidate row binds the selection operation ID, safe source digest, OS identity, and
process group through the existing launch-identity wrapper.
The candidate fields for binding revision and adapter generation remain null until the
publication transaction promotes it. A serving row always has both fields. A relaunch of
an unchanged binding writes that binding's current revision and the coordinator's new
generation before checkout can use it.

`AdapterCoordinator.reserve_source_transition` allocates the transition ID, records the
reservation owner and absolute expiry 240,000 milliseconds later in coordinator state,
and returns control to the caller; it does not hold a synchronous coordinator callback
open. Ordinary checkouts continue against the serving entry. Only the reservation owner
can prepare, resolve, or publish that transition's candidate. Another source transition,
or any transition while a prior `retiring` row remains unresolved, receives
`source_transition_busy` immediately and does not queue. Owner abort, authorized
same-verb selection cancellation, onboarding cancellation, caller death, or expiry closes
the activation when present and invokes exact candidate settlement.
This lets the OpenAI credential lifecycle call back into the coordinator without a
GenServer self-deadlock.

The ready-source publication transaction performs these process-ledger changes with the
binding change:

1. Change the prior unresolved `serving` row, when present, to `retiring`.
2. Change the exact ready `candidate` row to `serving`.
3. Write the new binding revision, binding history, completed attempt, and lifecycle
   event; write that revision and the next adapter generation on the promoted process row.
4. Delete the adapter's rate-limit park fence only when its typed owner is the exact open
   incident, or when select mode explicitly requested legacy repair and the fence is still
   the same legacy fence observed before candidate launch. Record an incident release when
   an exact open incident exists. Do not retract the incident fact.

If any write fails, the transaction changes none of them. After commit the coordinator
publishes the already-ready process as the next generation before serving another
checkout. It then closes the `retiring` process through the existing process-ledger
settlement path.

On gateway startup, reconciliation handles role before adapter checkout:

- An unresolved `candidate` whose transition has no committed binding-change record is
  terminated and resolved. The prior binding remains current.
- A committed transition already records its promoted process as `serving`; startup may
  reconcile that process. If the exact process is absent, startup must reacquire bounded
  consumer activation for the committed named account before it derives the transient
  home or relaunches. After the real ready token, it must complete process handoff before
  checkout can use the relaunch. It cannot revert the binding or launch from an unleased
  home.
- An unresolved `retiring` process is terminated and resolved without touching the
  current binding or serving row.
- Startup first reads the one existing park fence for the key. When any fence exists, it
  preserves that exact fence and owner without retagging or replacement. When no fence
  exists, an open `rate-limit-dead` incident re-establishes its incident-owned park only
  if its release fields are null. Thus a migrated legacy fence remains legacy until the
  explicit exact-ID repair, and a pre-commit crash cannot accidentally unpark a failed
  source.

Failure to identify or terminate a candidate or retiring process leaves the adapter key
fenced and startup reports the existing process-ledger cleanup refusal. It never starts
another candidate or serves an ambiguous process.

If candidate cleanup fails before publication, `process_cleanup_required` returns
`changed: false` with the prior safe binding. If retiring cleanup fails after the atomic
publication, the same code returns `changed: true` with the new safe binding and serving
generation. It does not claim rollback: activation and publication already succeeded.
The durable retiring row and fence make the cleanup obligation visible and restart-safe;
existing reconciliation retries it from exact process identity.

The existing harness-process projection adds safe `role`, `transitionId`, `sourceDigest`,
`bindingRevision`, and `adapterGeneration` fields. Lifecycle events record candidate prepared, candidate resolved,
source transition published, prior process retiring, and incident park released or
re-established. They carry adapter key, launch ID, binding revision, cause, and principal;
they omit provider home and credential material.

For one harness key, the gateway performs this sequence:

1. Parse the request and authenticate the principal.
2. Compute the request digest and check the completed idempotency record. Return an exact
   replay or `idempotency_conflict` before consulting transition ownership.
3. Acquire the per-harness-key ready-source transition reservation and allocate its
   transition ID and fixed expiry. Refuse immediately if another transition owns the key.
4. Read the registered host, current safe binding, and any park fence with its typed
   owner.
5. Compare `expectedRevision` to the current revision. Accept an incident-owned park, or
   accept a legacy park only when `repairLegacyPark` is true; refuse every other owner.
6. Open target-host Lachesis consumer activation for the exact account ID. Refuse unless
   its first frame establishes provider, ready state, mutation idleness, capacity,
   provider-process absence for the exact home, and a file-backed consumer binding while
   holding the account operation lock.
7. Start the unpublished candidate through `prepare_candidate_launch` for the resolved
   Codex adapter key and transition ID.
8. Wait for the candidate's existing real boot gate to issue its ready token while the
   activation connection remains open.
9. Send the process-handoff frame for the exact candidate and require `process_bound`.
10. Recheck principal authorization, process-handoff ownership and candidate liveness,
   reservation liveness and expiry, exact candidate identity, current binding revision,
   and the exact park fence observed in step 5.
11. Call `AdapterCoordinator`'s prepared-generation publication operation. While the
    coordinator is not serving another checkout or publication for this adapter key,
    that operation executes the binding, process-role, history, attempt, lifecycle, and
    repair-park transaction described above.
12. After that transaction commits and before the publication call returns, swap the
    ready candidate into the adapter key's next generation. New checkouts see the new
    generation. If the transaction fails, discard the candidate and keep the prior
    generation and park. Retire the prior process through existing process-ledger
    reconciliation.
13. Close the Lachesis activation stream after handoff; the process-owned lock remains.
    After publication returns, return
    the safe selected identity, revision, adapter key, generation, and readiness.

Candidate staging does not change the durable binding and does not make the candidate
routable. Activation failure, lease loss, or a failed publication resolves the candidate
row and records a safe failed attempt. The prior binding, published generation, and park
remain authoritative. A crash before the publication transaction restarts from the prior
binding and reconciles the candidate. A crash after it restarts from the new binding and
reconciles the promoted serving process. The implementation must not persist a `pending`,
`activating`, or `waiting` binding state.
Cancel, reservation-deadline handling, candidate exit, and publication linearize through
the coordinator-owned commit boundary. Activation expiry linearizes against process
handoff inside Lachesis before this boundary. If expiry wins there, publication cannot
begin. If handoff wins, activation expiry cannot release the process-owned lock. Before
publication, cancel, reservation expiry, or candidate exit settles the candidate,
releases transition ownership, and leaves source state unchanged. If publication wins,
cancel returns `selection_not_active`; later handlers observe the immutable completed
result. None can reverse the publication transaction.

The authorization, process-handoff, candidate-identity, and revision checks in step 10 and
the coordinator-owned commit/publication in steps 11–12 form the selection commit
boundary. The coordinator
queues supported adapter checkouts across this boundary. The binding module exposes no
independent current-binding read to lanes, so another selector or adapter checkout cannot
observe a new binding paired with the prior published adapter generation.

### E. Adapter launch and catalog authority

When a named Lachesis binding exists and its exact serving process is absent, every launch
path opens the same bounded consumer activation for the bound account. Placement derives
`CODEX_HOME` from that transient response, starts the exact process, and holds activation
until the real ready token. It then requires process handoff before the process can become
serving. Response closure or expiry before handoff, provider mismatch, loss of readiness,
handoff refusal, or capacity refusal leaves the binding durable but the adapter unavailable;
checkout refuses and placement does not start from a cached home. The fixed activation
expiry bounds restart and lazy relaunch just as it bounds selection. Once handed off, the
same account operation lock remains owned by the running process until exit. The adapter
launch reads the credential from that home.
Tightbeam's credential store is not copied into it and is not rewritten.

When the binding is the implicit Tightbeam-managed source, placement uses the existing
Tightbeam credential store and home projection without behavior change.

The per-host Codex catalog probe uses the current binding's serving source. A named
Lachesis binding probes through a live serving adapter; it does not open or retain a
provider home independently of bounded activation. The catalog remains keyed by
`{host, harness}`. Changing the binding invalidates only that entry and re-derives it
after candidate health succeeds.

This spec supersedes the one-credential-per-provider-per-host statement in
`tightbeam-credential-onboarding-v1.md` only for Codex runtime selection: Tightbeam
still owns one Tightbeam-managed credential per host, while the binding can instead
point the Codex runtime at one Lachesis-owned account on that host. It supersedes the
fixed-host-credential assumption in `per-host-catalogs-v1.md`; the host remains the
catalog scope, and the current binding now chooses the account within that host.

### F. Selected-account exhaustion production

Reuse `HarnessHealth`; do not add a fault subsystem.

The production's left-hand side is:

```text
terminal turn has exact codexErrorInfo=usageLimitExceeded
AND turn session has harness=codex and host=H
AND turn ledger checkout used adapter generation G
AND immutable generation mapping for {codex,H,G} is named Lachesis account A at revision R
AND current serving source at the production transaction boundary is exactly {G,R,A}
AND target-host Lachesis currently reports at least one healthy alternate B != A
```

The procedural act files one `authoritative-provider` observation into failure class
`rate-limit-dead` with correlation
`selected-account-exhausted:<turn-seq>:<adapter-generation>:<binding-revision>`. Its
`cause` is canonical JSON with kind, triggering turn sequence, adapter generation,
binding revision, selected safe identity and windows, and healthy alternate safe
identities and windows. Its `principal` is the
failed turn's recorded origin. The existing unique open incident for
`{codex, host, rate-limit-dead}` deduplicates the org fault and attaches later session
and assignment evidence.

The production runs after the failed turn transaction. If Lachesis cannot establish a
healthy alternate, it does not file this authoritative observation. The original failed
turn, lifecycle event, marker, and existing generic harness-health classification remain
truth. The production does not poll and does not retry on a timer.
If the generation mapping is absent or the current serving source no longer equals
`{G,R,A}`, the event remains ordinary turn evidence only. It cannot open or update the
incident, clear release fields, or establish a park.

The incident retains the existing durable park. Extend the existing park fence with
`ownerKind`, `ownerId`, `cause`, and `principal`; every newly created selected-account
park names the exact incident as owner. Pre-V1 fences migrate as `ownerKind: legacy` and
can be released only by an explicitly requested, exact-ID legacy repair transition. Add fields to the existing incident
projection: nullable `parkReleasedByBindingRevision`, nullable
`parkReleasedByAdapterGeneration`, and `parkReleasedAt`. These fields do not create
another incident or fault state.

Opening the incident or attaching another generation-correlated exact
`usageLimitExceeded` authoritative observation clears the release fields and idempotently
establishes an incident-owned park fence only when no fence exists. When any fence exists,
the observation preserves its exact owner and ID. A successful ready-source publication
writes its new binding revision and adapter generation into the release record and deletes
that exact incident-owned fence in the same transaction. A differently owned fence causes
`park_owner_conflict`. A legacy fence requires the explicit migration transition below;
a failed source transition changes neither release field nor fence.

Startup preserves any existing fence and its owner. Only when no fence exists does it
re-derive an incident-owned fence for an open incident whose
`parkReleasedByBindingRevision` is null. This makes migrated legacy ownership stable,
pre-commit crash recovery preserve the park, and post-commit recovery preserve the
deliberate proof-turn opening. If the
released serving generation immediately emits another exact `usageLimitExceeded`, the
generation-correlated observation clears the release fields and re-parks the key. An
event from a retired generation cannot do so.

Ready-source publication alone does not resolve the incident or retract its condition
fact. With the park absent, the first ordinary delivered Codex turn whose checkout
generation and binding revision equal the release record reaches the existing
normal-turn-success path, resolves the incident, and idempotently completes the
already-released park. A late delivery from an older generation does not resolve it. This
is the proof event; no timer, synthetic probe, or selection-success inference substitutes
for it.

### G. Interactive onboarding, migration, and rollback

Migration adds the binding and immutable history schema, harness-process roles and
transition identity, typed park ownership, and incident park-release fields. For each
harness key, migration pauses checkout at the coordinator publication boundary. It makes
an existing unresolved current launch `serving` at binding revision `0` and copies the
exact current published adapter generation for that launch. Migration creates the
corresponding revision-`0` Tightbeam-managed history entry. If it cannot establish that
exact launch-to-generation mapping, it marks the row `retiring`, places the existing
process-cleanup fence, and leaves the key unavailable until exact-identity reconciliation
terminates the row and performs an ordinary revision-`0` relaunch. It never invents a
mapping or permits checkout from an unmapped process. Existing park fences become
`legacy` and V1 does not release them automatically. Migration assigns each legacy fence
a stable safe owner ID derived from its existing fence row identity. Migration initializes
incident release fields to null. It does not inspect credential files, infer a Lachesis
account, or create a candidate. An org with no binding row behaves as the current
Tightbeam-managed source at revision `0`.

An authorized select request with `repairLegacyPark: true` is the sole V1 legacy repair.
It captures the exact legacy owner ID before activation. Candidate proof proceeds while
that fence continues blocking ordinary checkout. At publication, the transaction compares
the same fence ID, publishes the proven source, deletes that legacy fence, and records a
`legacy_park_replaced` lifecycle event with cause and principal. If an open
`rate-limit-dead` incident exists for the key, the same transaction records the new
binding revision and generation as that incident's release proof so startup does not
recreate the fence. A changed, absent, non-legacy, or unrequested fence refuses without
publication. This transition never clears a legacy fence and reruns the old source.

Interactive `tightbeam onboard openai` remains available. For OpenAI, begin reads the
current Codex binding revision for the target host and stores it in the existing
onboarding lease; its safe response also returns that revision. Begin and cancel do not
change a binding. Finish enters the per-key ready-source transition before it installs
or activates the staged credential and compares the captured revision to current state.
A mismatch returns `binding_conflict` and leaves the staged credential subject to the
existing cancel/lease cleanup path.

After the Tightbeam-managed credential is locally installed, Codex onboarding uses the
same durable candidate role and real boot proof as named selection. It does not call the
ordinary stop-then-start callback for the target Codex key. The common publication
transaction selects `tightbeam_managed`, increments the binding revision, promotes the
candidate generation, records cause and authenticated human principal, and releases an
owned rate-limit park. If activation or publication fails while the prior source is a
named Lachesis binding, that named binding and published adapter remain authoritative;
the Tightbeam-managed credential retains the existing present-but-unverified failure
marker. If the prior source is already Tightbeam-managed, its credential store retains
the existing fail-closed onboarding semantics, but no crossed binding/generation pair is
published.

Rollback of the shipped feature is schema-compatible and data-preserving: disable the
`account-select` command and ignore named rows only after an authorized migration has
rebound each affected host to a proven Tightbeam-managed credential. Do not delete
binding history or Lachesis accounts. A binary that does not understand a present named
binding must not silently use the Tightbeam-managed credential. Before downgrade, the new
binary's authorized preflight names every host and harness that still has a named binding
or role-aware unresolved process. An older binary that encounters the unknown schema
stamp must refuse startup with the found and expected schema stamps. It is not required
to read future rows or name affected keys.

## Acceptance

**A1 — canonical shape.** Given a fresh database, when the schema initializes, then a
query for `{codex, gibson}` returns the implicit Tightbeam-managed source at revision
`0`. Given an attempted second current row for the same key or a Lachesis row without an
account ID, when SQLite applies the write, then the write fails at the schema boundary.

**A2 — authorization.** Given an admin-owned agent session, when it calls
`account-select`, then authorization proceeds. Given a non-admin-owned session or a
process principal, when it sends the same payload, then the gateway returns
`not_authorized`; Lachesis receives no request and the adapter generation and binding
revision stay unchanged.

**A3 — exact candidate.** Given Lachesis lists `acct-a` and `acct-b`, when the caller
names `acct-b`, then Tightbeam verifies and stages only `acct-b`. The response names
`acct-b`. No request selects `acct-a`.

**A4 — provider, readiness, and capacity.** Given table-driven real-response fixtures
for missing account, Claude provider, busy mutation, matching provider process,
unavailable process inspection, degraded account, empty windows, stale usage, 100-percent
primary window, and ready Codex account with each window below 100 percent, when selection
evaluates each fixture, then only the last fixture reaches candidate adapter staging and
process handoff.
Each other case returns its typed refusal, closes any granted connection, and leaves
state unchanged. The activation frame carries an expiry exactly 200,000 milliseconds
after lock acquisition. Before process handoff, advancing the server clock to that
instant closes the response, releases the account lock, resolves any candidate, and
returns `operation_deadline_exceeded` without publication.

**A5 — real candidate proof.** Given a ready Codex account fixture and a real captured
candidate adapter boot exchange, when the candidate reaches the existing gate ready
token and Lachesis acknowledges process handoff for its exact PID and start token, then
its durable process row has role `candidate` under the same adapter key and selection can
commit. Given captured adapter startup refusal, gate failure, and handoff process-mismatch
responses,
when selection stages each candidate, then it returns `candidate_activation_failed`,
resolves the unpublished candidate row, and the prior adapter PID, generation, binding,
park, and catalog entry remain authoritative.

**A6 — check and publish boundary.** Given two concurrent selectors with expected
revision `4`, when both request the same source-transition reservation, then one selector
acquires the reservation and the other immediately returns `source_transition_busy`
before it calls Lachesis or creates a candidate. The owner can acquire activation, stage a
candidate, and commit revision `5`. A retry with expected revision `4` then returns
`binding_conflict`. Given the owner stalls, when its 240,000-millisecond reservation
deadline arrives, then the coordinator closes activation, settles the candidate, releases
the reservation, and a new transition can acquire it. Adapter checkouts observe either the prior binding with its prior
generation or the new binding with its new generation. No checkout observes a crossed
pair, two candidate roles, or a candidate process.
Given a completed selection replay while a different transition owns the reservation,
when the same principal repeats the exact completed request, then the binding module
returns the recorded replay before it consults the reservation. The result is not
`source_transition_busy`, and neither owner receives an additional effect.

**A7 — host confinement.** Given registered hosts Gibson and Eezo with separate
Lachesis fixtures and running Codex adapters, when selection targets Eezo, then only the
Eezo loopback endpoint, Eezo binding row, Eezo catalog entry, and Eezo adapter generation
change. Gibson rows, requests, process identity, and generation remain byte-identical.

**A8 — restart-safe idempotency.** Given a completed selection with key `k`, when the
same principal repeats the same request after a gateway restart, then the safe result is
byte-equivalent except for `idempotentReplay: true`; Lachesis request counts, adapter
generation, and binding revision do not change. Given the principal reuses `k` with a
different account ID or cause, then it receives `idempotency_conflict` and no effect.
Given an active pre-commit selection with key `k`, when an authorized agent invokes cancel
mode for `k`, then activation closes, the exact candidate settles, the reservation releases,
and the cancel result is restart-safe. Repeating cancel returns its recorded result. Cancel
after commit returns `selection_not_active` and does not change the published result.
Given a completed cancel with cancel key `c`, when the principal reuses `c` with a
different `operationKey` or cause, then the gateway returns `idempotency_conflict` and
does not cancel either operation.

**A9 — crash boundaries.** Given an injected gateway crash before the binding
transaction while serving and candidate process groups exist, when the gateway restarts,
then it terminates and resolves the candidate, resolves the prior binding and adapter
source, and preserves any incident-owned park. Given an injected crash after the binding
and process-role transaction, when the gateway restarts, then it resolves the new named
binding, cleans the retiring process, and starts or adopts the adapter from that account.
If the promoted process is absent, restart opens bounded activation for the committed
account, holds its operation lock through the real ready token, completes process handoff,
and only then serves a checkout. Concurrent refresh, re-onboard, delete, and
credential-affecting jobs cannot mutate the home during that relaunch. Activation expiry
before handoff leaves the named binding durable, the adapter unavailable
with checkout refusing, and no serving process. In every successful reconciliation the database has no
pending-selection binding and no unresolved candidate or retiring process.

**A10 — privacy and custody.** Given real Lachesis account and consumer-activation
fixtures containing sentinel credential bytes in the backing file,
when selection succeeds and the adapter runs, then the sentinel bytes appear only in
the Lachesis-owned provider home and in the Codex process's own credential access.
Searches of Tightbeam DB text columns, stdout, stderr, lifecycle events, firehose,
condition facts, logs, artifacts, request captures, and selection history find zero
sentinel occurrences.

**A11 — no account mutation.** Given a request recorder around Lachesis, when selection
succeeds and when each validation case fails, then observed methods and paths are limited
to account list and `POST /api/v1/accounts/{id}/consumer-activation`. Registry bytes,
credential bytes, account count, labels, account mutation state, and provider-home file
hashes remain unchanged except for credential activity produced by the real Codex
candidate itself. Before process handoff, the account operation lock is released after
each refusal, transport loss, fixed expiry, and authorized cancellation. After handoff,
the exact process retains the lock through success and releases it on process exit; cancel
terminates the candidate before it returns. A spy on ordinary usage proves that it does
not take the operation lock. A spy on consumer activation proves that activation acquires
the existing lock before its provider-process check and direct capacity read, fails closed
when process absence cannot be established, does not reacquire the lock, and transfers
that same lock only to the exact proven process.

**A12 — safe projection.** Given a named binding, when `tightbeam list` and
`account-select` render success or refusal, then they include host, harness, revision,
account ID, label, and provider. They omit consumer home, credential path, access token,
refresh token, device code, activation ID, PID, process start token, and raw Lachesis
response.

**A13 — one exhaustion fault.** Given three assignments on `{codex, gibson}` fail with
the exact `usageLimitExceeded` event while the selected account is at 100 percent and
two healthy Codex alternates exist, and each turn's recorded checkout generation maps to
the same still-serving named binding revision, when the exhaustion production runs, then one open
`rate-limit-dead` incident exists for `{codex, gibson}`. Its observations name the three
turns. Its authoritative cause reports the selected identity and both alternate
identities and windows plus the serving generation and binding revision. The supervision prod count for those assignments does not
advance while the incident stands, and one durable park fence blocks ordinary adapter
checkout until a ready-source transition releases it. An attempted rewrite of a serving
row's binding revision or adapter generation fails at the schema boundary.

**A14 — no proxy trigger.** Given selected-account usage reaches 100 percent without a
failed turn, when no `usageLimitExceeded` event exists, then the production files no
selected-account exhaustion observation. Given a generic 429 without the exact Codex
event, then existing generic rate-limit handling remains unchanged.

**A15 — no auto-failover.** Given an open selected-account exhaustion incident and a
healthy alternate, when the production completes, then the binding revision, adapter
generation, selected account, and account registry remain unchanged. Only an authorized
`account-select` or successful interactive onboarding can change the binding.

**A16 — evidence-based recovery.** Given a successful account selection while the
rate-limit incident stands, when publication commits, then the incident stays open, its
condition fact stays asserted, its release fields name the new binding revision and
adapter generation, and its park fence is absent. When the first ordinary Codex turn
checked out from that exact generation and revision delivers, then the
existing normal-turn path resolves the incident once and supervision becomes eligible
again. If that turn instead emits exact `usageLimitExceeded`, then the incident stays
open, the release fields clear, and one park fence stands again. A delayed failure or
delivery from the retiring generation changes neither release fields, park, nor incident
resolution.

**A17 — interactive fallback.** Given a named binding and a failed interactive OpenAI
ceremony, when onboarding exits, then the named binding, published adapter, and park
remain authoritative. Given a successful ceremony whose Tightbeam-managed candidate
reaches ready, when finish commits through the ready-source transition, then the binding
source becomes `tightbeam_managed`, the revision increments once, any incident-owned park
is released, and only the target host's Codex adapter rotates.

**A18 — migration refusal and rollback.** Given a pre-V1 legacy fence, when ordinary
selection omits `repairLegacyPark`, then it returns `legacy_park_repair_required` without
activation. Given an authorized agent invokes `tightbeam account-select` with
`--repair-legacy-park`, then the wire sets `repairLegacyPark: true`. Given an authorized
selection includes the flag and the captured legacy owner
ID remains current, then candidate proof runs behind the fence and one publication
transaction publishes the new source, removes that exact fence, records the release on an
open incident when present, and never reruns the old source. A changed fence refuses with
no effect. Given the new binary's downgrade preflight, then it names each affected host and
harness. When an older binary that lacks this schema starts, then it refuses on the unknown
schema stamp and reports only found and expected stamps. Given an authorized rollback that first proves and binds the
Tightbeam-managed source, when the new command is disabled, then turns use that source,
Lachesis accounts remain unchanged, and binding history remains queryable.
Given one pre-V1 unresolved process with an exact durable coordinator generation, when
migration runs, then its row becomes `serving` at binding revision `0`, its generation is
unchanged, and revision-`0` history maps it to the Tightbeam-managed source. Given no exact
launch-to-generation mapping, then migration marks the row `retiring`, fences the key,
and permits no checkout until exact-identity cleanup and an ordinary revision-`0`
relaunch complete.

**A19 — gate verification.** Given an implementation candidate, when its baseline and
after-change gates run in fresh owned worktrees at the exact commits under review, then
the Rust CLI gate, Elixir gate, real Lachesis response-fixture tests, and real Codex
adapter smoke are green with recorded baseline and after counts. A hand-written ideal
Lachesis or Codex boundary fixture does not satisfy this clause.

**A20 — lifecycle exclusion race.** Given a selector has received an idle activation
frame, when concurrent refresh and re-onboard calls start before candidate readiness,
then neither lifecycle call enters credential or provider-home mutation while the
activation connection is open. If the connection closes before process handoff, selection
returns `activation_lease_lost`, resolves its candidate, and neither binding nor adapter
generation changes. Given handoff and activation expiry become runnable in the same
Lachesis account-state step, when expiry linearizes first, then handoff refuses,
publication does not begin, and the prior source remains authoritative. When handoff
linearizes first, then expiry closes only the activation stream; the exact process retains
the account operation lock and publication can commit. Concurrent refresh, re-onboard,
delete, and credential-affecting jobs remain blocked until that process exits. A Lachesis
restart during the process-owned phase makes each lifecycle mutation acquire the lock,
detect the live provider process, and refuse before changing an account row, credential,
or provider-home byte. Given that restart and a new consumer activation for the same
account, when activation holds the reconstructed operation lock and checks the provider
home, then it detects the serving process and returns `account_busy` before verify,
capacity read, or candidate launch. A process-inspection error returns the same fail-closed
refusal. Authorized same-verb cancellation before publication terminates the candidate
and releases the transition reservation. The resulting process exit releases the account
lock in the same test tick.

**A21 — lawful candidate coexistence.** Given one serving adapter and one selector, when
candidate boot begins, then the process ledger contains one `serving` and one `candidate`
row with the same adapter key and different launch identities; checkout returns only the
serving generation. Given a second selector or onboarding finish, then it cannot acquire
a second candidate role. Given pre-commit gateway death, startup terminates the candidate
process group and leaves the prior source authoritative. A process it cannot terminate
fences the key and returns `process_cleanup_required` with `changed: false`. Given the
prior process emits a delayed ready or `DOWN` after candidate promotion, then only the
prior launch's `retiring` row settles; the new serving row, generation, and readiness
remain unchanged. Given retiring cleanup fails after publication, then the operation
returns `process_cleanup_required` with `changed: true`, the new safe binding and serving
generation, and one durable fenced retiring row for exact-identity reconciliation.

**A22 — incident park transition.** Given an open selected-account exhaustion incident
and its durable park, when candidate activation or publication fails, then the park
remains and no ordinary turn starts. When ready-source publication succeeds, then the
same transaction records the releasing binding revision and adapter generation and removes the park without
resolving the incident. An injected restart on either side of that transaction restores
the corresponding parked or proof-turn-eligible state. Given a differently owned park
fence on the key, when publication reaches its boundary, then it returns
`park_owner_conflict`, resolves the candidate, and preserves the fence, binding, and
published generation. Given a late `usageLimitExceeded` event from the retired generation,
then the event remains turn evidence but cannot clear the release fields or re-park the
new generation. Legacy behavior is covered by A18.
Given a migrated legacy fence and an open incident with null release fields, when the
gateway restarts, then it preserves the exact legacy fence ID and owner. It neither
retags the fence nor creates a second incident-owned fence. Given the same open incident
with no fence, startup creates one incident-owned fence.

**A23 — selector and onboarding race.** Given OpenAI onboarding begin captured revision
`4` and `account-select` also expects revision `4`, when both finish concurrently, then
one request acquires the non-waiting reservation and the other returns
`source_transition_busy` before installing a staged credential, opening Lachesis, or
creating a candidate. The owner can publish exactly one revision `5` binding and one
serving generation. Retrying the loser with expected revision `4` returns
`binding_conflict`. Cancel, owner death, or fixed expiry frees the reservation and settles
the owner's candidate or staged-credential path. No checkout observes a crossed
binding/generation pair and no second candidate exists.

**A24 — refusal completeness.** Given an unregistered host, when an authorized selection
names it, then the gateway returns `unknown_host` before any Lachesis or candidate action.
Given harness `claude`, when the same principal invokes selection, then the gateway
returns `unsupported_harness` before any host transport or state change. Given a registered
remote host whose Lachesis connection refuses or times out, when selection opens
activation, then it returns `lachesis_unavailable` and preserves the binding, generation,
park, and account registry. Given an exact ready account backed by an unsupported keychain
store, when activation evaluates its consumer binding, then it returns
`consumer_binding_unavailable`, closes the activation, creates no candidate, and preserves
the binding, generation, park, and provider-home bytes.

## Open Questions

None. Independent exact-revision review can reject or amend this contract. Implementation
and target selection remain a separate Mike decision after that review.
