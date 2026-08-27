# Codex named-account selection — v1

Status: SPEC READY FOR INDEPENDENT REVIEW. The work item remains targetless. This
revision authorizes no implementation, merge, release, deployment, live selection,
credential change, account change, or spec-ref binding.

Authority: `wi_008ad6d7-d976-4120-9e90-8557a24f7602`, recon verdict
`att_ae78b652-70ad-484e-b2ac-ed3062ab58ce`, and report `art_f245e870` at SHA-256
`09e57edcd8102141f269359004b1effd4e9c1bf3874ea2b6a533a93a48ebeba3`.

This spec introduces the **Named harness-account binding** pattern. It applies to one
Tightbeam harness on one registered host and names a non-secret account identity held
by the provider-account custodian on that host. V1 applies the pattern only to the
Codex harness and Lachesis. It does not apply to model selection, agent placement,
Claude, or account lifecycle.

Subtraction ruling: ADD wins because deleting account choice leaves the stated repair
verb absent, while accepting the failure preserves the measured org-wide outage. The
addition is one typed binding, one mutation seam, one agent-reachable verb, one
read-only custodian query, and reuse of the existing adapter and harness-health seams.

## Goal

Give an authorized Tightbeam agent a restart-safe command that binds the Codex harness
on one registered host to an explicitly named, ready Lachesis Codex account with
provider capacity. The command proves the candidate through the real adapter boot path
before it publishes the new binding. It returns the selected non-secret account
identity.

When the selected account emits the exact Codex `usageLimitExceeded` event and Lachesis
shows a healthy alternate on the same host, record one host-scoped harness-health
incident. The incident reports the selected identity and the healthy alternate
identities. It suppresses per-assignment effort prods through the existing
`HarnessHealth` gate. A mind chooses whether to invoke the selection command.

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
  Tightbeam-managed source has revision `0`. Each successful named selection increments
  the revision by one.
- **Candidate**: the Lachesis account identity named in one selection request.
- **Ready account**: a Lachesis account for which a synchronous verify returns
  `status: "ready"`, `working: true`, and `mutation_state: "idle"`.
- **Capacity-positive sample**: a synchronous Lachesis usage result whose `status` is
  `live` or `cache`, whose `sample.windows` contains at least one window, and for which
  each window has `used_percent < 100`. `stale`, `error`, a missing sample, an empty
  window set, a non-number, or `used_percent >= 100` does not establish capacity.
- **Healthy alternate**: a different Lachesis account on the target host whose provider
  is `codex`, whose account view is ready, and whose synchronous usage result is
  capacity-positive.
- **Consumer binding**: a read-only Lachesis response that maps one account ID to the
  provider home required by the provider CLI. It contains no credential bytes.
- **Candidate adapter**: an unpublished replacement process for the existing Codex
  adapter key on the target host. A lane cannot check it out before commit.
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

- Tightbeam source `main` identifies an adapter by harness, shared archetype, and host,
  and `AdapterCoordinator` already owns adapter generation, readiness, replacement,
  and process-ledger reconciliation.
- Tightbeam already records one open `HarnessHealth` incident per
  `{harness, host, failure_class}` and suppresses supervision prods while its condition
  fact stands.
- Tightbeam's host registry and authorization machinery are durable DB-backed seams.
- Lachesis runs on `127.0.0.1:7843` on the host that owns its accounts. Remote access
  from the Tightbeam gateway uses the existing registered-host SSH transport and calls
  that loopback endpoint on the target host.
- Lachesis remains the registry and credential custodian for its accounts. Its provider
  homes are file-backed. The Codex CLI remains the writer and refresher inside a
  selected Codex provider home.
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

**I2 — one mutation seam.** One Tightbeam module owns binding comparison, commit,
history, and projection. `account-select` and successful interactive onboarding call
that module. No adapter, placement, CLI, migration, or health component writes binding
state directly.

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

**I6 — check before publish.** Authorization, host existence, harness support, account
existence, provider match, readiness, mutation idleness, capacity, consumer binding,
expected revision, and candidate adapter health must pass before the named binding
becomes current.

**I7 — old path stays authoritative until proof.** During candidate staging, lanes keep
using the prior adapter and the durable binding remains unchanged. A failed activation
or failed health proof discards the candidate. The prior binding and adapter remain the
published pair.

**I8 — serialized commit.** Selection operations for one harness key share one critical
section. The implementation rechecks authorization and binding revision at the commit
boundary. `AdapterCoordinator`, the existing single owner of checkouts and generations,
owns the final publication call. While that call is running, it executes the binding
transaction and swaps the ready candidate into the current generation before it serves
another checkout or selection call. A failed transaction discards the candidate. Binding
commit and candidate publication are therefore one serialized operation from the
perspective of every supported reader.

**I9 — crash boundary.** Before the binding transaction commits, a gateway restart
resolves the prior binding. After it commits, a gateway restart resolves the new
binding. No durable pending-selection state exists.

**I10 — idempotent result.** A caller supplies a non-empty idempotency key. The completed
result is keyed by `{principal, account-select, idempotency_key}` and bound to a digest
of `{host, harness, account_id, expected_revision, cause}`. Repeating the same digest
returns the recorded result without another verify, adapter stage, generation change,
or binding change. Reusing the key with a different digest returns
`idempotency_conflict`.

**I11 — cause and principal.** Each selection attempt records the authenticated
principal, the caller's non-empty cause, request digest, target harness key, candidate
identity, prior identity, observed Lachesis result, final outcome, binding revision,
and timestamp. The record contains no credential bytes or consumer-binding path.

**I12 — selection does not mutate an account.** The selection operation may call
Lachesis account list, verify, usage, and consumer-binding queries. It does not call
account create, adopt, delete, refresh, re-onboard, job, or code-submission endpoints.

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

**I15 — recovery remains evidence-based.** A successful selection does not retract the
rate-limit incident. The first ordinary delivered turn on `{codex, host}` resolves it
through the existing `HarnessHealth` normal-turn path.

**I16 — onboarding remains the human exit.** `tightbeam onboard openai` keeps its
interactive ceremony. On successful credential activation, it uses the binding mutation
seam to publish the Tightbeam-managed source for that host and rotate that host's Codex
adapter. A failed ceremony leaves the current named binding and adapter unchanged.

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

### B. Lachesis read-only consumer binding

Add one supported Lachesis query:

```http
GET /api/v1/accounts/{id}/consumer-binding
```

Success returns:

```json
{
  "account": {"id": "<id>", "label": "<label>", "provider": "codex"},
  "consumer_binding": {"kind": "provider_home", "home": "/absolute/provider/home"}
}
```

The endpoint accepts no request body. It reads the registry row and its normalized file
store binding. It returns no credential path below the provider home and no credential
bytes. A keychain or unsupported store returns a typed refusal. The endpoint does not
change account status, mutation state, registry state, cache state, or credential state.

Tightbeam invokes the endpoint on the target host after account verification. It keeps
`home` in memory for candidate launch and omits it from DB rows, CLI output, firehose,
lifecycle events, artifacts, and selection-attempt records.

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
| `lachesis_unavailable` | target-host loopback query cannot complete | none |
| `account_not_found` | Lachesis list has no exact account ID | none; return safe known IDs |
| `account_provider_mismatch` | account provider differs from `codex` | none |
| `account_busy` | mutation state differs from `idle` | none |
| `account_not_ready` | verify does not return ready and working | none |
| `account_capacity_exhausted` | usage result is not capacity-positive | none; return normalized windows |
| `consumer_binding_unavailable` | Lachesis cannot return a file-backed provider home | none |
| `candidate_activation_failed` | candidate adapter fails to start or reach ready | discard candidate; prior binding and adapter remain published |
| `idempotency_conflict` | key exists with a different request digest | none |

Each refusal names the failed check, the safe non-secret account identity when known,
the current binding revision, and one concrete remedy. A refusal does not suggest
another account as the selected outcome.

### D. Selection sequence and atomic boundary

For one harness key, the gateway performs this sequence:

1. Parse the request and authenticate the principal.
2. Enter the per-harness-key selection critical section.
3. Read the registered host and current safe binding.
4. Check for an exact idempotent replay.
5. Compare `expectedRevision` to the current revision.
6. Query target-host Lachesis for the exact account ID.
7. Run synchronous verify and synchronous usage for that ID.
8. Check provider, ready state, mutation state, and capacity.
9. Read the consumer binding.
10. Start an unpublished candidate replacement for the resolved Codex adapter key.
11. Wait for the candidate's existing real boot gate to issue its ready token.
12. Recheck principal authorization and current binding revision.
13. Call `AdapterCoordinator`'s prepared-generation publication operation. While the
    coordinator is not serving another checkout or publication for this adapter key,
    that operation executes one DB transaction that writes the new binding,
    binding-change history, safe completed attempt, and normal lifecycle event.
14. After that transaction commits and before the publication call returns, swap the
    ready candidate into the adapter key's next generation. New checkouts see the new
    generation. If the transaction fails, discard the candidate and keep the prior
    generation. Retire the prior process through existing process-ledger reconciliation.
15. Return the safe selected identity, revision, adapter key, generation, and readiness.

Steps 10–11 do not change the durable binding and do not make the candidate routable.
Failure in either step discards the candidate and records a safe failed attempt. The
prior binding and adapter remain active. A crash before step 13 restarts from the prior
binding. A crash after step 13 restarts from the new binding. The implementation must
not persist a `pending`, `activating`, or `waiting` binding state.

The authorization and revision checks in step 12 and the coordinator-owned
commit/publication in steps 13–14 form the selection commit boundary. The coordinator
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

The first ordinary delivered Codex turn on the host resolves the incident through the
existing normal-turn-success path. Selection success alone does not resolve it.

### G. Interactive onboarding, migration, and rollback

Migration adds the binding and immutable history schema. It does not inspect credential
files and does not infer a Lachesis account. An org with no binding row behaves as the
current Tightbeam-managed source at revision `0`.

Interactive `tightbeam onboard openai` remains available. Its begin and cancel phases do
not change a binding. After the new Tightbeam-managed credential passes the existing
activation proof, finish calls the binding mutation seam to select
`tightbeam_managed`, increments the revision, and rotates only the target host's Codex
adapter. If activation fails, the named binding and current adapter remain published.

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
candidate adapter staging. Each other case returns its typed refusal and leaves state
unchanged.

**A5 — real candidate proof.** Given a ready Codex account fixture and a real captured
candidate adapter boot exchange, when the candidate reaches the existing gate ready
token, then selection can commit. Given captured adapter startup refusal and gate
failure responses, when selection stages each candidate, then it returns
`candidate_activation_failed`, closes the unpublished candidate, and the prior adapter
PID, generation, binding, and catalog entry remain authoritative.

**A6 — check and publish boundary.** Given two concurrent selectors with expected
revision `4`, when each candidate passes its external checks, then one selector commits
revision `5`; the other returns `binding_conflict` with revision `5`. Adapter checkouts
observe either the prior binding with its prior generation or the new binding with its
new generation. No checkout observes a crossed pair.

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
transaction, when the gateway restarts, then it resolves the prior binding and prior
adapter source. Given an injected crash after the binding transaction, when the gateway
restarts, then it resolves the new named binding and starts the adapter from that
account. In both cases the database has no pending-selection row.

**A10 — privacy and custody.** Given real Lachesis account, verify, usage, and
consumer-binding fixtures containing sentinel credential bytes in the backing file,
when selection succeeds and the adapter runs, then the sentinel bytes appear only in
the Lachesis-owned provider home and in the Codex process's own credential access.
Searches of Tightbeam DB text columns, stdout, stderr, lifecycle events, firehose,
condition facts, logs, artifacts, request captures, and selection history find zero
sentinel occurrences.

**A11 — no account mutation.** Given a request recorder around Lachesis, when selection
succeeds and when each validation case fails, then observed methods and paths are limited
to account list, verify, usage, and consumer-binding. Registry bytes, credential bytes,
account count, labels, account mutation state, and provider-home file hashes remain
unchanged except for credential activity produced by the real Codex candidate itself.

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
advance while the incident stands.

**A14 — no proxy trigger.** Given selected-account usage reaches 100 percent without a
failed turn, when no `usageLimitExceeded` event exists, then the production files no
selected-account exhaustion observation. Given a generic 429 without the exact Codex
event, then existing generic rate-limit handling remains unchanged.

**A15 — no auto-failover.** Given an open selected-account exhaustion incident and a
healthy alternate, when the production completes, then the binding revision, adapter
generation, selected account, and account registry remain unchanged. Only an authorized
`account-select` or successful interactive onboarding can change the binding.

**A16 — evidence-based recovery.** Given a successful account selection while the
rate-limit incident stands, when no ordinary turn has delivered, then the incident stays
open. When the first ordinary Codex turn on that host delivers, then the existing
normal-turn path resolves the incident once and supervision becomes eligible again.

**A17 — interactive fallback.** Given a named binding and a failed interactive OpenAI
ceremony, when onboarding exits, then the named binding and adapter remain authoritative.
Given a successful ceremony whose Tightbeam-managed candidate reaches ready, when finish
commits, then the binding source becomes `tightbeam_managed`, the revision increments
once, and only the target host's Codex adapter rotates.

**A18 — migration refusal and rollback.** Given a database with a named binding, when an
older binary that lacks this schema starts, then startup refuses and names the host and
harness. Given an authorized rollback that first proves and binds the
Tightbeam-managed source, when the new command is disabled, then turns use that source,
Lachesis accounts remain unchanged, and binding history remains queryable.

**A19 — gate verification.** Given an implementation candidate, when its baseline and
after-change gates run in fresh owned worktrees at the exact commits under review, then
the Rust CLI gate, Elixir gate, real Lachesis response-fixture tests, and real Codex
adapter smoke are green with recorded baseline and after counts. A hand-written ideal
Lachesis or Codex boundary fixture does not satisfy this clause.

## Open Questions

None. Independent exact-revision review can reject or amend this contract. Implementation
and target selection remain a separate Mike decision after that review.
