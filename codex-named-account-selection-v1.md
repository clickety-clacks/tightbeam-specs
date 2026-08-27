# Codex named-account selection — v1

Status: SPEC READY FOR INDEPENDENT RE-REVIEW. The work item remains targetless. This
revision authorizes no implementation, merge, release, deployment, live selection,
credential change, account change, or spec-ref binding.

Authority: `wi_008ad6d7-d976-4120-9e90-8557a24f7602`, recon verdict
`att_ae78b652-70ad-484e-b2ac-ed3062ab58ce`, and report `art_f245e870` at SHA-256
`09e57edcd8102141f269359004b1effd4e9c1bf3874ea2b6a533a93a48ebeba3`.
The successor also answers independent changes-requested verdict `att_de28818e` and
report `art_5d90dcdd` at SHA-256
`e8556161e30d3de18de219e69639fedfcc0c1c3c022fc028eb85512e768871f1`.

This spec introduces the **Named harness-account binding** pattern. It applies to one
Tightbeam harness on one registered host and names a non-secret account identity held
by the provider-account custodian on that host. V1 applies the pattern only to the
Codex harness and Lachesis. It does not apply to model selection, agent placement,
Claude, or account lifecycle.

Subtraction ruling: ADD wins because deleting account choice leaves the stated repair
verb absent, while accepting the failure preserves the measured org-wide outage. The
addition is one typed binding, one mutation seam, one agent-reachable verb, one
custodian activation lease, and reuse of the existing adapter and harness-health seams.
The review repairs extend those same seams with a typed candidate role and a park-release
transition. Deleting any repair loses proof-before-publish, account lifecycle exclusion,
the shared incident, or the required human fallback; accepting any race can publish an
unproved binding/adapter pair.

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
- V1 does not create a new fault table, fault queue, hold, adjudicator, account chooser,
  retry loop, or polling process.
- V1 does not create a second adapter key for a candidate or bypass the durable harness
  process ledger.
- V1 does not convert a consumer activation lease into account lifecycle state or a
  durable Tightbeam binding field.
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
  Lachesis holds the account operation lock.
- **Capacity-positive sample**: a synchronous Lachesis usage result whose `status` is
  `live` or `cache`, whose `sample.windows` contains at least one window, and for which
  each window has `used_percent < 100`. `stale`, `error`, a missing sample, an empty
  window set, a non-number, or `used_percent >= 100` does not establish capacity.
- **Healthy alternate**: a different Lachesis account on the target host whose provider
  is `codex`, whose account view is ready, and whose synchronous usage result is
  capacity-positive.
- **Consumer activation lease**: one connection-scoped Lachesis operation that acquires
  the account's existing exclusive operation lock, proves provider, readiness, mutation
  idleness, and capacity, and returns the provider home required by the provider CLI.
  Lachesis holds the lock until the connection closes. The lease contains no credential
  bytes, account mutation, durable account field, or caller-chosen timeout.
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
- **Incident-owned park**: a durable harness park fence whose `ownerKind` is
  `harness_health_incident` and whose `ownerId` is the exact open incident. V1 never
  releases a legacy, operator-owned, cleanup-owned, or differently owned fence.
- **Health proof**: the existing Codex adapter boot gate reaches its ready token while
  the candidate adapter uses the candidate's consumer binding. V1 adds no timer or
  synthetic health test; it uses the current adapter boot deadline and real gate.
- **Selection operation**: one call of the `account-select` verb, from authorization
  through validation, candidate proof, commit, and response.
- **Selected-account exhaustion observation**: an existing
  `HarnessHealth` `rate-limit-dead` authoritative-provider observation whose cause is
  the exact Codex `usageLimitExceeded` event plus a current named binding and at least
  one healthy alternate.

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
- Lachesis already serializes verify, usage, refresh, and re-onboard with one per-account
  operation lock. V1 exposes a connection-scoped use of that lock; it does not add a
  second lock or account mutation state.
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
consumer binding, expected revision, and candidate adapter health must pass before the
named binding becomes current. The Lachesis account operation lock stays held from the
final provider/readiness/capacity observations through candidate proof and publication.
Refresh, re-onboard, delete, or another lifecycle mutation cannot begin in that interval.

**I7 — old path stays authoritative until proof.** During candidate staging, the durable
binding remains unchanged. When the prior adapter is serving, lanes keep using it. When
an open rate-limit incident has already parked it, the park and prior binding remain the
authoritative failed state. A failed activation or health proof resolves only the
candidate process row; it neither releases the park nor changes the prior binding or
published generation.

**I8 — serialized source transition.** Every binding-changing operation for one harness
key, including `account-select` and interactive onboarding finish, shares one critical
section from transition reservation through publication. The coordinator reservation
does not block the coordinator process: ordinary checkouts and calls from the reservation
owner continue, while another source-transition request waits in the coordinator queue.
The implementation rechecks
authorization, lifecycle-lease liveness when applicable, and binding revision at the
commit boundary. `AdapterCoordinator`, the existing single owner of checkouts and
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

**I10 — idempotent result.** A caller supplies a non-empty idempotency key. The completed
result is keyed by `{principal, account-select, idempotency_key}` and bound to a digest
of `{host, harness, account_id, expected_revision, cause}`. Repeating the same digest
returns the recorded result without another activation lease, adapter stage, generation
change, or binding change. Reusing the key with a different digest returns
`idempotency_conflict`.

**I11 — cause and principal.** Each selection attempt records the authenticated
principal, the caller's non-empty cause, request digest, target harness key, candidate
identity, prior identity, observed Lachesis result, final outcome, binding revision,
and timestamp. The record contains no credential bytes or consumer-binding path.

**I12 — selection does not mutate an account.** The selection operation may list
accounts and acquire one consumer activation lease. Lease acquisition performs verify,
usage, and consumer-binding reads while holding Lachesis's existing account operation
lock. It does not call account create, adopt, delete, refresh, re-onboard, job, or
code-submission endpoints. Releasing or losing the lease changes only transient lock
ownership, not account or credential state.

**I13 — one shared exhaustion incident.** The exact `usageLimitExceeded` event on a
named selected account triggers a current-account and alternate check. When the check
finds a healthy alternate, it files one authoritative observation into the existing
`rate-limit-dead` incident for `{codex, host}`. The existing unique-open-incident rail
absorbs later observations. Assignment-specific failures remain evidence attached to
that incident; supervision does not emit per-assignment effort prods while the incident
stands.

**I14 — alternatives are information.** The exhaustion observation reports the selected
`{id, label, provider}`, binding revision, triggering turn sequence, and each healthy
alternate's `{id, label, provider, windows}`. It does not invoke `account-select`, change
a binding, or mark an assignment complete or failed.

**I15 — recovery remains evidence-based.** A successful ready-source transition does
not retract the rate-limit incident. Its publication transaction releases the adapter
park for `{codex, host}` after the replacement is ready only when that fence is owned by
the exact open incident. This permits the normal turn path to run. The first ordinary
delivered turn resolves the incident. If publication fails, the park remains. Park
release alone does not resolve or suppress evidence.

**I16 — onboarding remains the human exit.** `tightbeam onboard openai` keeps its
interactive ceremony. Begin captures the current safe binding revision in the onboarding
lease. Finish enters the same per-key ready-source transition as `account-select`, proves
a Tightbeam-managed candidate, and publishes only if that captured revision still
matches. A concurrent source transition produces `binding_conflict`; it does not silently
override the winner. A failed or conflicting ceremony leaves the current named binding,
published adapter generation, and repair park unchanged.

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

This takes the **unrepresentable** rung for duplicate current bindings, illegal source
shapes, and history deletion. Authorization, provider liveness, and account capacity
remain runtime checks because they depend on external observations.

### B. Lachesis consumer activation lease

Add one supported Lachesis operation:

```http
POST /api/v1/accounts/{id}/consumer-activation
Accept: application/x-ndjson
```

The request body is empty. Lachesis resolves the exact account, acquires that account's
existing operation lock, refuses a non-idle lifecycle state, and performs verify and
`usage?refresh=wait` while it owns the lock. The first response frame is either one typed
refusal or:

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
  "lease": {"kind": "connection"}
}
```

After that frame Lachesis keeps the response open and retains the operation lock. Closing
or losing the response releases the lock. The endpoint has no lease ID, renewal verb,
heartbeat poller, caller-selected duration, or durable lease row. Lachesis uses transport
closure only to release ownership. Refresh, re-onboard, delete, and other account
lifecycle operations use the same existing lock and therefore cannot start while the
response remains open.

Lock acquisition is non-waiting; an owned lock returns `account_busy`. The operation
reads the registry row and normalized file store binding. It returns no
credential path below the provider home and no credential bytes. A keychain or
unsupported store returns a typed refusal before it grants the lease. Verify or usage
failure closes the response. The operation returns direct observations without updating
account status, mutation state, registry state, usage cache, provider-home contents, or
credential state.

Tightbeam keeps the response open through candidate proof and ready-source publication.
It monitors transport closure as a selection failure. At the commit boundary the
candidate is already a running Codex process in the leased home, so Lachesis's existing
provider-process check continues to exclude refresh or re-onboard after Tightbeam closes
the lease. Tightbeam keeps `home` only in memory and omits it from DB rows, CLI output,
firehose, lifecycle events, artifacts, and selection-attempt records.

### C. Agent-reachable wire and CLI

Add one dispatch verb and one CLI command:

```text
tightbeam account-select \
  --host <registered-host> \
  --harness codex \
  --account <lachesis-account-id> \
  --if-revision <non-negative-integer> \
  --cause <non-empty-text> \
  --key <idempotency-key>
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
    "idempotencyKey": "asg-example-select-acct-2"
  }
}
```

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
| `lachesis_unavailable` | target-host activation connection cannot complete | none |
| `account_not_found` | Lachesis list has no exact account ID | none; return safe known IDs |
| `account_provider_mismatch` | account provider differs from `codex` | none |
| `account_busy` | mutation state differs from `idle` or another lifecycle operation owns the account lock | none |
| `account_not_ready` | verify does not return ready and working | none |
| `account_capacity_exhausted` | usage result is not capacity-positive | none; return normalized windows |
| `consumer_binding_unavailable` | Lachesis cannot return a file-backed provider home | none |
| `park_owner_conflict` | a park stands but is not owned by the exact open rate-limit incident | resolve candidate; prior binding, generation, and park remain |
| `activation_lease_lost` | Lachesis activation connection closes before publication | resolve candidate; prior binding, generation, and park remain |
| `candidate_activation_failed` | candidate adapter fails to start or reach ready | resolve candidate; prior binding, generation, and park remain |
| `process_cleanup_required` | an exact candidate or retiring process cannot be terminated and settled | fence key; return safe current binding and whether publication committed |
| `idempotency_conflict` | key exists with a different request digest | none |

Each refusal names the failed check, the safe non-secret account identity when known,
the current binding revision, and one concrete remedy. A refusal does not suggest
another account as the selected outcome.

### D. Durable candidate lifecycle and atomic boundary

Extend `harness_processes` with logical fields `role`, `transitionId`, and
`sourceDigest`. `role` is `serving`, `candidate`, or `retiring`. The schema permits at
most one unresolved row per `{adapterKey, role}`. A candidate child has a unique process
identity derived from its launch ID, not a second adapter key. Ordinary adapter checkout
reads only the coordinator's `serving` entry.

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

`AdapterCoordinator.reserve_source_transition` allocates the transition ID and records
the reservation owner in coordinator state. It returns control to the caller; it does not
hold a synchronous coordinator callback open. Ordinary checkouts continue against the
serving entry. Only the reservation owner can prepare, resolve, or publish that
transition's candidate. Other source transitions for the key queue until the owner
publishes or aborts, and until any prior `retiring` row resolves. Caller death aborts the
reservation and invokes candidate settlement.
This lets the OpenAI credential lifecycle call back into the coordinator without a
GenServer self-deadlock.

The ready-source publication transaction performs these process-ledger changes with the
binding change:

1. Change the prior unresolved `serving` row, when present, to `retiring`.
2. Change the exact ready `candidate` row to `serving`.
3. Write the new binding revision, binding history, completed attempt, and lifecycle
   event.
4. Delete the adapter's rate-limit park fence only when its typed owner is the exact open
   incident. Record that release on the incident. Do not retract the incident fact.

If any write fails, the transaction changes none of them. After commit the coordinator
publishes the already-ready process as the next generation before serving another
checkout. It then closes the `retiring` process through the existing process-ledger
settlement path.

On gateway startup, reconciliation handles role before adapter checkout:

- An unresolved `candidate` whose transition has no committed binding-change record is
  terminated and resolved. The prior binding remains current.
- A committed transition already records its promoted process as `serving`; startup may
  reconcile that process and lazily relaunch it from the new binding, but it cannot
  revert the binding.
- An unresolved `retiring` process is terminated and resolved without touching the
  current binding or serving row.
- Every open `rate-limit-dead` incident re-establishes its park fence unless its incident
  release fields prove that a ready-source transition released that incident's park. Thus a
  pre-commit crash cannot accidentally unpark the failed source.

Failure to identify or terminate a candidate or retiring process leaves the adapter key
fenced and startup reports the existing process-ledger cleanup refusal. It never starts
another candidate or serves an ambiguous process.

If candidate cleanup fails before publication, `process_cleanup_required` returns
`changed: false` with the prior safe binding. If retiring cleanup fails after the atomic
publication, the same code returns `changed: true` with the new safe binding and serving
generation. It does not claim rollback: activation and publication already succeeded.
The durable retiring row and fence make the cleanup obligation visible and restart-safe;
existing reconciliation retries it from exact process identity.

The existing harness-process projection adds safe `role`, `transitionId`, and
`sourceDigest` fields. Lifecycle events record candidate prepared, candidate resolved,
source transition published, prior process retiring, and incident park released or
re-established. They carry adapter key, launch ID, binding revision, cause, and principal;
they omit provider home and credential material.

For one harness key, the gateway performs this sequence:

1. Parse the request and authenticate the principal.
2. Acquire the per-harness-key ready-source transition reservation and allocate its
   transition ID.
3. Read the registered host, current safe binding, and any park fence with its typed
   owner.
4. Check for an exact idempotent replay.
5. Compare `expectedRevision` to the current revision and refuse a known incompatible
   park owner.
6. Open target-host Lachesis consumer activation for the exact account ID. Refuse unless
   its first frame establishes provider, ready state, mutation idleness, capacity, and a
   file-backed consumer binding while holding the account operation lock.
7. Start the unpublished candidate through `prepare_candidate_launch` for the resolved
   Codex adapter key and transition ID.
8. Wait for the candidate's existing real boot gate to issue its ready token while the
   activation connection remains open.
9. Recheck principal authorization, activation-connection liveness, exact candidate
   identity, current binding revision, and any park owner.
10. Call `AdapterCoordinator`'s prepared-generation publication operation. While the
    coordinator is not serving another checkout or publication for this adapter key,
    that operation executes the binding, process-role, history, attempt, lifecycle, and
    repair-park transaction described above.
11. After that transaction commits and before the publication call returns, swap the
    ready candidate into the adapter key's next generation. New checkouts see the new
    generation. If the transaction fails, discard the candidate and keep the prior
    generation and park. Retire the prior process through existing process-ledger
    reconciliation.
12. Close the Lachesis activation connection only after publication returns, then return
    the safe selected identity, revision, adapter key, generation, and readiness.

Candidate staging does not change the durable binding and does not make the candidate
routable. Activation failure, lease loss, or a failed publication resolves the candidate
row and records a safe failed attempt. The prior binding, published generation, and park
remain authoritative. A crash before the publication transaction restarts from the prior
binding and reconciles the candidate. A crash after it restarts from the new binding and
reconciles the promoted serving process. The implementation must not persist a `pending`,
`activating`, or `waiting` binding state.

The authorization, lease-liveness, candidate-identity, and revision checks in step 9 and
the coordinator-owned commit/publication in steps 10–11 form the selection commit
boundary. The coordinator
queues supported adapter checkouts across this boundary. The binding module exposes no
independent current-binding read to lanes, so another selector or adapter checkout cannot
observe a new binding paired with the prior published adapter generation.

### E. Adapter launch and catalog authority

When a named Lachesis binding exists, placement derives `CODEX_HOME` from the transient
consumer binding on that host. The adapter launch reads the credential from that home.
Tightbeam's credential store is not copied into it and is not rewritten.

When the binding is the implicit Tightbeam-managed source, placement uses the existing
Tightbeam credential store and home projection without behavior change.

The per-host Codex catalog probe uses the current binding's source. A named Lachesis
binding probes the selected account home on that host. The catalog remains keyed by
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
AND current binding for {codex,H} is named Lachesis account A at revision R
AND target-host Lachesis currently reports at least one healthy alternate B != A
```

The procedural act files one `authoritative-provider` observation into failure class
`rate-limit-dead` with correlation
`selected-account-exhausted:<turn-seq>:<binding-revision>`. Its `cause` is canonical
JSON with kind, triggering turn sequence, binding revision, selected safe identity and
windows, and healthy alternate safe identities and windows. Its `principal` is the
failed turn's recorded origin. The existing unique open incident for
`{codex, host, rate-limit-dead}` deduplicates the org fault and attaches later session
and assignment evidence.

The production runs after the failed turn transaction. If Lachesis cannot establish a
healthy alternate, it does not file this authoritative observation. The original failed
turn, lifecycle event, marker, and existing generic harness-health classification remain
truth. The production does not poll and does not retry on a timer.

The incident retains the existing durable park. Extend the existing park fence with
`ownerKind`, `ownerId`, `cause`, and `principal`; every newly created selected-account
park names the exact incident as owner. Pre-V1 fences migrate as `ownerKind: legacy` and
cannot be released by a source transition. Add two fields to the existing incident
projection: nullable `parkReleasedByBindingRevision` and `parkReleasedAt`. These fields
do not create another incident or fault state.

Opening the incident or attaching another exact `usageLimitExceeded` authoritative
observation clears the release fields and idempotently establishes an incident-owned
park fence. A successful ready-source publication writes its new binding revision into
those fields and deletes that exact incident-owned fence in the same transaction. A
different or legacy fence causes `park_owner_conflict`; a failed source transition
changes neither release field nor fence.

Startup re-derives the fence for an open incident only when
`parkReleasedByBindingRevision` is null. This makes pre-commit crash recovery preserve
the park and post-commit recovery preserve the deliberate proof-turn opening. If the
released adapter immediately emits another exact `usageLimitExceeded`, the new
observation clears the release fields and re-parks the key.

Ready-source publication alone does not resolve the incident or retract its condition
fact. With the park absent, the first ordinary delivered Codex turn on the host reaches
the existing normal-turn-success path, resolves the incident, and idempotently completes
the already-released park. This is the proof event; no timer, synthetic probe, or
selection-success inference substitutes for it.

### G. Interactive onboarding, migration, and rollback

Migration adds the binding and immutable history schema, harness-process roles and
transition identity, typed park ownership, and incident park-release fields. Existing
unresolved process rows become `serving`. Existing park fences become `legacy` and V1
cannot release them. Migration does not inspect credential files, infer a Lachesis
account, or create a candidate. An org with no binding row behaves as the current
Tightbeam-managed source at revision `0`.

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
binding must refuse startup with the host and harness named; it must not silently use the
Tightbeam-managed credential.

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
for missing account, Claude provider, busy mutation, degraded account, empty windows,
stale usage, 100-percent primary window, and ready Codex account with each window below
100 percent, when selection evaluates each fixture, then only the last fixture reaches
candidate adapter staging and its activation connection stays open through publication.
Each other case returns its typed refusal, closes any granted connection, and leaves
state unchanged.

**A5 — real candidate proof.** Given a ready Codex account fixture and a real captured
candidate adapter boot exchange, when the candidate reaches the existing gate ready
token, then its durable process row has role `candidate` under the same adapter key and
selection can commit. Given captured adapter startup refusal and gate failure responses,
when selection stages each candidate, then it returns `candidate_activation_failed`,
resolves the unpublished candidate row, and the prior adapter PID, generation, binding,
park, and catalog entry remain authoritative.

**A6 — check and publish boundary.** Given two concurrent selectors with expected
revision `4`, when both request the same source-transition reservation, then one selector
can acquire an activation lease, stage a candidate, and commit revision `5`. The queued
selector then returns `binding_conflict` with revision `5` before it calls Lachesis or
creates a candidate. Adapter checkouts observe either the prior binding with its prior
generation or the new binding with its new generation. No checkout observes a crossed
pair, two candidate roles, or a candidate process.

**A7 — host confinement.** Given registered hosts Gibson and Eezo with separate
Lachesis fixtures and running Codex adapters, when selection targets Eezo, then only the
Eezo loopback endpoint, Eezo binding row, Eezo catalog entry, and Eezo adapter generation
change. Gibson rows, requests, process identity, and generation remain byte-identical.

**A8 — restart-safe idempotency.** Given a completed selection with key `k`, when the
same principal repeats the same request after a gateway restart, then the safe result is
byte-equivalent except for `idempotentReplay: true`; Lachesis request counts, adapter
generation, and binding revision do not change. Given the principal reuses `k` with a
different account ID or cause, then it receives `idempotency_conflict` and no effect.

**A9 — crash boundaries.** Given an injected gateway crash before the binding
transaction while serving and candidate process groups exist, when the gateway restarts,
then it terminates and resolves the candidate, resolves the prior binding and adapter
source, and preserves any incident-owned park. Given an injected crash after the binding
and process-role transaction, when the gateway restarts, then it resolves the new named
binding, cleans the retiring process, and starts or adopts the adapter from that account.
In both cases the database has no pending-selection binding and no unresolved candidate
or retiring process after reconciliation.

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
candidate itself. The account operation lock is released after success, every refusal,
and transport loss.

**A12 — safe projection.** Given a named binding, when `tightbeam list` and
`account-select` render success or refusal, then they include host, harness, revision,
account ID, label, and provider. They omit consumer home, credential path, access token,
refresh token, device code, and raw Lachesis response.

**A13 — one exhaustion fault.** Given three assignments on `{codex, gibson}` fail with
the exact `usageLimitExceeded` event while the selected account is at 100 percent and
two healthy Codex alternates exist, when the exhaustion production runs, then one open
`rate-limit-dead` incident exists for `{codex, gibson}`. Its observations name the three
turns. Its authoritative cause reports the selected identity and both alternate
identities and windows. The supervision prod count for those assignments does not
advance while the incident stands, and one durable park fence blocks ordinary adapter
checkout until a ready-source transition releases it.

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
condition fact stays asserted, its release fields name the new binding revision, and its
park fence is absent. When the first ordinary Codex turn on that host delivers, then the
existing normal-turn path resolves the incident once and supervision becomes eligible
again. If that turn instead emits exact `usageLimitExceeded`, then the incident stays
open, the release fields clear, and one park fence stands again.

**A17 — interactive fallback.** Given a named binding and a failed interactive OpenAI
ceremony, when onboarding exits, then the named binding, published adapter, and park
remain authoritative. Given a successful ceremony whose Tightbeam-managed candidate
reaches ready, when finish commits through the ready-source transition, then the binding
source becomes `tightbeam_managed`, the revision increments once, any incident-owned park
is released, and only the target host's Codex adapter rotates.

**A18 — migration refusal and rollback.** Given a database with a named binding or
role-aware unresolved harness-process row, when an older binary that lacks this schema
starts, then startup refuses and names the host and harness. Given an authorized rollback
that first proves and binds the
Tightbeam-managed source, when the new command is disabled, then turns use that source,
Lachesis accounts remain unchanged, and binding history remains queryable.

**A19 — gate verification.** Given an implementation candidate, when its baseline and
after-change gates run in fresh owned worktrees at the exact commits under review, then
the Rust CLI gate, Elixir gate, real Lachesis response-fixture tests, and real Codex
adapter smoke are green with recorded baseline and after counts. A hand-written ideal
Lachesis or Codex boundary fixture does not satisfy this clause.

**A20 — lifecycle exclusion race.** Given a selector has received an idle activation
frame, when concurrent refresh and re-onboard calls start before candidate readiness,
then neither lifecycle call enters credential or provider-home mutation while the
activation connection is open. If the connection closes before publication, selection
returns `activation_lease_lost`, resolves its candidate, and neither binding nor adapter
generation changes. After successful publication closes the connection, the running
Codex candidate makes both lifecycle calls return the existing provider-process-busy
refusal.

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
same transaction records the releasing binding revision and removes the park without
resolving the incident. An injected restart on either side of that transaction restores
the corresponding parked or proof-turn-eligible state. Given a legacy or differently
owned park fence on the key, when publication reaches its boundary, then it returns
`park_owner_conflict`, resolves the candidate, and preserves the fence, binding, and
published generation.

**A23 — selector and onboarding race.** Given OpenAI onboarding begin captured revision
`4` and `account-select` also expects revision `4`, when both finish concurrently, then
the shared ready-source transition publishes exactly one revision `5` binding and one
serving generation. If selection wins, onboarding returns `binding_conflict` before
installing its staged credential. If onboarding wins, selection returns
`binding_conflict` before opening a Lachesis activation connection or creating a
candidate. No checkout observes a crossed binding/generation pair and no second candidate
exists.

## Open Questions

None. Independent exact-revision review can reject or amend this contract. Implementation
and target selection remain a separate Mike decision after that review.
