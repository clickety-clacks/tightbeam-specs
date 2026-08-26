# Model Catalog Probe Observability v1

Status: **PROPOSAL — review changes addressed; revised commit pending verdict**

Work item: `wi_54d54f16-8e8e-4895-8191-6bb64384bcb8`

Implementation target: **UNTARGETED**. The work item does not elect Tightbeam
0.1.8, active 0.1 maintenance, or main/0.2.0. Branch existence and the source-code
commit inspected for reconciliation do not supply a target.

This specification extends `per-host-catalogs-v1.md`, `model-identity-v1.md`,
`credential-kinds-v1.md`, and `cli-surface-v1.md`. It does not supersede them.

It reconciles the reviewed generic org-fault specification at commit
`153839b31704a6af28242d08a38ebfa35cc81540` with the catalog seams on Tightbeam
main at `7a70a2f616363074514237b5bee48ba67c52e2ea`. That main commit is evidence of
the current catalog shape, not an implementation target. Only host-scoped evidence,
independent signal axes, typed absence, privacy-safe projections, and one catalog
mutation seam remain applicable. The generic fault lifecycle, owner routing,
waivers, review obligations, recovery conjunctions, claims, outbox, and onboarding
remediation are declined. This defect needs catalog evidence and one repair verb,
not an organization-wide fault system.

Owner correction `att_28931ab5-93ef-4e5c-9cfd-d9f34f06537a` establishes that the
Anthropic credential is live. An expired-credential or onboarding premise is not
authority for this proposal.

Independent review verdict `att_5794e22f-bb10-457c-bd28-51ccca16d3c4` requested
six changes against commit `b3b1f40edc21e78895ec2735fb8c6526291788a0`.
This revision resolves them by separating the public and internal command names,
narrowing valid-empty semantics by harness, preserving existing credential renewal,
typing actor and origin independently, deleting an unused cause code, and deferring
agent guidance until the public command exists.

Exact-tip review verdict `att_a2393591-2d30-49b6-ba02-e04d8ec4ba4f` requested two
more changes against commit `1be78383879e45fa356f8627892b67152a9c7e8b`.
This revision makes `credential_present` origin null because its reserved fact does
not carry an initiating author, and it requires observed termination of an old
attempt and its descendant transport before replacement boot I/O starts.

## Goal

Make the difference between cached model inventory and an active provider probe
observable for every configured `{host, harness}` catalog.

An agent must be able to distinguish a catalog that has never completed a probe,
a successful empty provider response, a failed probe, and an explicit credential
rejection. The agent must also be able to force a fresh probe for one
`{host, provider}` without repeating credential setup.

The MVP adds typed probe state and wall-clock timestamps to `tightbeam list`, and
adds one agent-facing forced-refresh command. Existing model routing continues to use
the cached inventory and runtime harness validation defined by the source specs.

## Non-Goals

- This specification does not create an organization-wide fault, incident,
  ownership, waiver, review-obligation, claim, or outbox system.
- It does not infer that an empty catalog means a credential is absent or expired.
- It does not start onboarding, OAuth, credential capture, credential copying, or
  credential repair.
- It does not change credential storage, rotation harvest, or `credential-present`
  handling.
- It does not change the catalog refresh interval, routing readiness, picker
  eligibility, CAP, spawn admission, or runtime validation.
- It does not persist catalog inventory or probe state across a ModelCatalog process
  restart.
- It does not add automatic remediation or retry policy beyond the existing boot,
  read-expiry, and credential-present triggers.
- It does not add catalog state to `org-options`, `session-status`, REST resources,
  the firehose, or the ATC UI.
- It does not rename, remove, or expose the pre-parser internal helper
  `tightbeam catalog-probe <provider> <kind> <credential-path> <url>`.
- It does not classify a client-side `bwrap --unshare-net` connect `EPERM` or an SSH
  public-key failure as a provider credential rejection.
- It does not publish agent operating guidance before the public refresh command
  ships.
- It does not retain the reviewed generic org-fault specification as implementation
  authority for this defect.

Deleting the model catalog would remove required routing data. Accepting an
indistinguishable empty catalog already blocked diagnosis. Therefore, this proposal
adds the smallest observable state and repair verb that close the defect.

## Terms

**Catalog key** — the existing `{host, harness}` key owned by `ModelCatalog`. A
catalog key has exactly one provider, as derived from the harness definition.

**Cached inventory** — the model set from the most recent successful provider
response for a catalog key, including a valid empty set. It is the same inventory
that `tightbeam list` already projects under `models[host][harness]`. A failed probe
does not erase an earlier successful inventory. A successful empty response replaces
an earlier non-empty inventory with an empty inventory.

**Probe attempt** — one capability derivation for one catalog key: obtain the current
credential, and, when a credential is available, perform one provider read. A probe
attempt has a start time, a trigger, an actor, an optional origin, and one terminal
result.

**Active probe** — the probe attempt currently performing credential lookup or
provider I/O for a catalog key. An attempt remains active until its capability task
and every descendant provider transport have exited. At most one probe is active for
a catalog key.

**Probe trigger** — the event that requested an attempt. Its closed values are
`boot`, `ttl_read`, `credential_present`, and `forced`.

**Probe actor** — the typed, durable Tightbeam identity accountable for the trigger.
Its shape is `{kind, id}`, where `kind` is `session`, `user`, or `process`. Forced
probes use the authenticated Gateway call principal. Boot, expiry, and
credential-present probes use `{kind: process, id: tightbeam}` because the substrate
starts those attempts.

**Probe origin** — the optional public attribution string carried separately from
the actor, such as `agent:<role>`, `user:<id>`, or `process:<name>`. Forced probes
copy the Gateway call origin. A trigger without a distinct public attribution uses
null. A credential-present probe uses null because its reserved durable fact carries
only `process:tightbeam`, not an initiating agent or user. Origin never replaces the
actor used for authorization and accountability.

**Last probe result** — the latest completed result for a catalog key, or
`never_probed` when no attempt has completed since the current ModelCatalog process
started. Its closed values are:

- `never_probed` — no attempt has completed in the current process lifetime;
- `available_nonempty` — the provider returned a valid, non-empty model set;
- `available_empty` — the harness contract accepted the provider response as a valid,
  empty model set;
- `probe_failed` — transport, remote-host access, timeout, protocol, or response
  parsing prevented a valid provider result;
- `credential_rejected` — the provider explicitly rejected the supplied provider
  credential; and
- `credential_unavailable` — Tightbeam could not obtain a credential with which to
  attempt the provider request.

**Cause code** — a privacy-safe refinement of a non-success result. The closed cause
codes are:

| Result | Cause codes |
| --- | --- |
| `probe_failed` | `provider_forbidden`, `transport_timeout`, `attempt_timeout`, `remote_host_auth_failed`, `probe_network_forbidden`, `client_version_filtered_empty`, `malformed_response`, `unclassified_failure` |
| `credential_rejected` | `provider_unauthorized` |
| `credential_unavailable` | `credential_missing`, `credential_in_progress`, `credential_store_unreadable`, `credential_kind_unknown` |

Successful results and `never_probed` have no cause code. HTTP 401, or an equivalent
structured provider-authentication rejection, maps to `provider_unauthorized`. HTTP
403 alone maps to `provider_forbidden`; it does not prove that the credential is
invalid.

`available_empty` is harness-specific. The Anthropic catalog contract can accept a
valid empty model array. The Codex catalog contract cannot: when client-version
filtering removes every returned entry, the result is `probe_failed` with
`causeCode=client_version_filtered_empty`, as required by `per-host-catalogs-v1.md`.

**Inventory timestamp** — `derivedAt`, the epoch-millisecond wall-clock time of the
successful probe that produced the cached inventory. It is null when no successful
probe has produced an inventory.

**Probe timestamps** — `startedAt` and `completedAt`, expressed as epoch
milliseconds. `completedAt` is present only for a completed attempt.

**Stale inventory** — cached inventory whose age exceeds the existing ModelCatalog
refresh interval. `stale` is null when no cached inventory exists. The implementation
uses a monotonic clock for age calculations and exposes wall-clock time only for
observation.

**Forced probe** — an authenticated request for fresh provider reads on one host.
The request expands from `{host, provider}` to every configured catalog key on that
host whose harness uses that provider.

**Observe-then-refresh workflow** — after the public command ships, an agent reads
`modelCatalogs` before it infers why `models` is empty. For a never-probed, failed,
rejected, unavailable, or stale catalog, it runs the scoped public refresh command
and reads the resulting typed evidence. This workflow does not apply to credential
setup, runtime harness authentication, model execution, or generic connectivity
diagnosis.

## Assumptions

- `ModelCatalog` remains the single in-process owner of cached inventory and probe
  state.
- The harness registry determines the provider for each harness and which harnesses
  are configured on each registered host.
- Provider catalog reads already execute on the owning host and already have a
  bounded transport timeout.
- The current `models[host][harness]` projection is consumed by existing agents and
  remains backward compatible.
- A harness contract can accept an empty provider model array. The Anthropic contract
  accepts it; the Codex client-version filter does not.
- The Anthropic credential implicated by the reported defect is currently live:
  `ready=true`, `working=true`, and no credential error. This specification does not
  rely on an expired-credential premise.
- Gateway authentication already identifies an agent or user principal before an
  agent-facing command is admitted.

## Invariants

1. **Scope remains explicit.** Every inventory, active probe, and last result belongs
   to exactly one catalog key. Evidence from one host or harness never changes the
   state of another catalog key.

2. **Cached and active state remain independent.** A catalog may expose cached
   inventory while a probe is active or while its last probe result is empty or
   failed. The projection never represents cached inventory as proof that the latest
   probe succeeded.

3. **Empty has a typed cause.** When `models[host][harness]` is empty, the sibling
   catalog-state projection states whether the current process has never completed a
   probe, completed a valid empty response, failed its last probe, observed an
   explicit credential rejection, or could not obtain a credential.

4. **A successful empty response is not a credential judgment.**
   `available_empty` does not trigger or recommend onboarding, credential repair, or
   a new credential mutation seam.

5. **Only explicit provider authentication rejection proves rejection.** A local
   connection error, timeout, malformed body, HTTP 403, SSH public-key failure, or
   sandbox network denial cannot produce `credential_rejected`.

6. **One mutation seam owns state.** Capability-task completions send typed results
   to `ModelCatalog`. Only `ModelCatalog` changes inventory, active-probe state, last
   result, timestamps, trigger, actor, origin, or staleness.

7. **One attempt runs per catalog key.** A catalog key never has overlapping
   capability derivations or provider reads, including across a ModelCatalog restart.
   A completion can mutate state only when its generation matches the active
   generation for that key; a late completion from an older generation is discarded.

8. **Forced means post-admission evidence.** A successful
   `model-catalog-refresh` response is based on an attempt that started after the
   request was admitted. An already-active attempt cannot satisfy that request.

9. **Concurrent forced requests coalesce safely.** Requests admitted before the
   required follow-up attempt starts may share that attempt. A request admitted after
   it starts requires a later attempt. Coalescing never changes the result or scope.

10. **Restart is explicit.** A ModelCatalog process restart discards inventory and
    probe history. Before the replacement process starts any boot attempt, the
    lifecycle owner terminates and observes the exit of every capability task and
    descendant provider transport owned by the prior process. Sending a cancellation
    signal or discarding a late completion is not sufficient. Before any post-restart
    attempt completes, each catalog reports `lastProbe.result=never_probed`; boot
    probes may be active at the same time.

11. **Forced probing does not perform a credential ceremony.** It uses the same
    credential lookup and provider-read path as automatic catalog derivation. The
    command does not invoke onboarding or credential capture and does not file a
    `credential-present` fact. Existing Anthropic renewal, atomic credential-file
    write, and rotation-harvest behavior remains in force; this specification adds no
    second renewal or credential-write seam.

12. **The projection is privacy-closed.** Catalog state and
    `model-catalog-refresh` output never include credential values, authorization
    headers, response bodies, request URLs, prompts, local credential paths, SSH
    destinations, or raw stdout/stderr. They include only the fields and closed
    result and cause values defined here.

13. **Existing model consumers remain compatible.** The shape and meaning of
    `models[host][harness]` do not change. New state appears in a sibling
    `modelCatalogs` field.

14. **Pre-gateway failures cannot mutate catalog state.** If a caller cannot connect
    to Tightbeam, including a client-side `bwrap --unshare-net` connect `EPERM`, no
    forced request is admitted and no catalog attempt or result is recorded.

## Architecture

### Catalog state

For every configured catalog key, `ModelCatalog` owns this logical state:

```text
inventory: {entries, derivedAtWall, derivedAtMonotonic} | null

activeProbe: {generation, startedAt, trigger, actor, origin} | null

lastProbe: {
  result, startedAt, completedAt, trigger, actor, origin, causeCode
}
```

Before the first completion in a process lifetime, `lastProbe.result` is
`never_probed` and its other fields are null. Starting a probe changes
`activeProbe`; it does not erase `lastProbe`. Completing the matching generation
atomically clears `activeProbe` and replaces `lastProbe`.

`available_nonempty` replaces the cached inventory with the returned models. When the
harness contract accepts an empty result, `available_empty` replaces the inventory
with an empty set. Both successful results set `derivedAt` to their completion time.
A Codex client-version-filtered empty result is a failure, so it retains any earlier
successful inventory. All other `probe_failed`, `credential_rejected`, and
`credential_unavailable` results also retain an earlier successful inventory. This
preserves the existing degraded-cache behavior while exposing the newest evidence
separately.

The existing boot, read-expiry, and credential-present triggers use the same state
transition seam as forced probes. A list read that starts an expiry probe returns a
snapshot that already shows that probe under `activeProbe`.

The ModelCatalog lifecycle owner owns each capability task and every provider
transport that task starts as one attempt unit. Normal completion, timeout, and
restart cleanup do not release the catalog key until the owner observes all processes
in that unit exit. On restart, the lifecycle owner drains every prior-process attempt
unit before it permits the replacement ModelCatalog to start boot probes. This
ordering prevents old and new provider I/O, Anthropic renewal, and credential-file
writes from overlapping. Generation matching still rejects any stale completion
message that arrives after cleanup.

### List projection

`tightbeam list` retains the existing `models` field and adds:

```json
{
  "modelCatalogs": {
    "gibson": {
      "claude": {
        "provider": "anthropic",
        "inventory": {
          "modelCount": 4,
          "derivedAt": 1787701200000,
          "stale": false
        },
        "activeProbe": {
          "startedAt": 1787702100000,
          "trigger": "forced",
          "actor": {
            "kind": "session",
            "id": "agent:main:clawline:mike:main s_example"
          },
          "origin": "agent:spec-writer:catalog"
        },
        "lastProbe": {
          "result": "available_nonempty",
          "startedAt": 1787701198000,
          "completedAt": 1787701200000,
          "trigger": "ttl_read",
          "actor": {"kind": "process", "id": "tightbeam"},
          "origin": null,
          "causeCode": null
        }
      }
    }
  }
}
```

When no cached inventory exists, `inventory` is:

```json
{"modelCount": 0, "derivedAt": null, "stale": null}
```

When no probe is running, `activeProbe` is null. Every configured catalog key appears
in `modelCatalogs`, including before its first probe completes.

### Forced-refresh command

The agent-facing command is:

```text
tightbeam model-catalog-refresh --host <host> --provider <provider>
```

This public Gateway verb is distinct from the existing pre-parser internal helper
`tightbeam catalog-probe <provider> <kind> <credential-path> <url>`. The internal
helper remains non-agent-facing and unchanged.

The gateway admits the command only for an authenticated active Tightbeam agent or
user. The pair must resolve to a registered host and at least one configured harness
on that host that uses the provider. Otherwise, the command returns the typed refusal
`catalog_scope_not_found` and starts no attempt.

On admission, `ModelCatalog` resolves the matching catalog-key set and enrolls the
request against that set as one serialized operation. Later configuration changes do
not add or remove keys from the admitted request. `ModelCatalog` schedules one fresh
generation for every admitted key. Matching keys execute independently. The command
waits until the post-admission generation required for every admitted key completes,
then returns the keys in ascending harness-name order. Each item contains `host`,
`harness`, `provider`, `result`, `startedAt`, `completedAt`, `actor`, `origin`, and
`causeCode`. It contains no model identifiers or raw provider output; callers obtain
inventory from `tightbeam list`.

Each HTTP provider read retains its existing 30-second bound. `ModelCatalog` owns a
40-second execution deadline for each attempt, including credential lookup and remote
host transport. When that deadline expires, the lifecycle owner terminates the
capability task and every descendant provider transport. After it observes their
exits, `ModelCatalog` atomically completes its active generation as `probe_failed`
with `causeCode=attempt_timeout`.

The gateway waits at most 85 seconds for the admitted key set. This covers the
remainder of one already-active 40-second attempt plus the forced request's required
40-second follow-up attempt and five seconds of termination and dispatch overhead. If
the gateway wait expires before `ModelCatalog` returns every required result, the
gateway returns the top-level error `model_catalog_refresh_wait_timeout`. The gateway
does not fabricate a probe result or mutate catalog state. The caller may retry.

The command is safe to retry. It does not promise exactly-once provider I/O.
Concurrent requests can coalesce as invariant 9 defines. A process restart can end an
in-flight caller without a response; the caller may retry after reconnecting.

### Failure classification

Classification occurs where structured transport and provider status are available,
before a typed result enters `ModelCatalog`.

- An explicit provider authentication rejection becomes `credential_rejected` /
  `provider_unauthorized`.
- Provider HTTP 403 becomes `probe_failed` / `provider_forbidden`.
- A probe subprocess sandbox denial that contains the structured connect-`EPERM`
  condition becomes `probe_failed` / `probe_network_forbidden`.
- SSH host authentication failure becomes `probe_failed` /
  `remote_host_auth_failed`.
- A transport deadline becomes `probe_failed` / `transport_timeout`.
- A Codex response whose entries are all removed by the client-version filter becomes
  `probe_failed` / `client_version_filtered_empty`.
- A successful transport with an invalid catalog envelope becomes `probe_failed` /
  `malformed_response`.
- Any unmatched failure becomes `probe_failed` / `unclassified_failure`.

Classifier tests use captured, redacted provider and transport envelopes from real
probe responses. Hand-written ideal envelopes do not establish classifier fidelity.
The catalog path stores and logs only the typed result, cause code, scope, actor,
origin, and timestamps. It does not store or log raw response bodies or raw process
output.

## Acceptance

1. **Never-probed and active are both visible.**

   Given a newly started ModelCatalog with a blocked probe transport,
   when an agent runs `tightbeam list` before the boot probe completes,
   then the configured key has `lastProbe.result=never_probed`, a non-null
   `activeProbe` with `trigger=boot`, and null inventory timestamps.

2. **A list-triggered refresh is visible in the same snapshot.**

   Given stale cached inventory and no active probe,
   when `tightbeam list` starts the existing expiry refresh,
   then the same response retains the cached models and reports a non-null
   `activeProbe` with `trigger=ttl_read` and `inventory.stale=true`.

3. **A non-empty success updates both axes atomically.**

   Given a catalog key with no cached inventory and an active probe,
   when a captured valid provider response contains two models,
   then one state snapshot has no active probe, has
   `lastProbe.result=available_nonempty`, has `inventory.modelCount=2`, and has
   matching non-null completion and derivation timestamps.

4. **A successful empty response remains distinct.**

   Given an Anthropic catalog key with earlier cached inventory,
   when a captured valid Anthropic response contains an empty model array,
   then `models` and the cached inventory become empty,
   `lastProbe.result=available_empty`, `inventory.derivedAt` equals
   `lastProbe.completedAt`, `causeCode` is null, and no onboarding or credential
   repair entry point runs; and given a captured Codex response whose entries are all
   removed by client-version filtering,
   when the same classifier processes it,
   then prior inventory remains and the last result is `probe_failed` /
   `client_version_filtered_empty`.

5. **A probe failure retains cache and exposes safe evidence.**

   Given a catalog key with earlier cached inventory,
   when its next probe reaches the transport deadline,
   then the inventory remains, staleness continues to derive from its earlier
   monotonic timestamp, and the last result is `probe_failed` /
   `transport_timeout` with completed wall-clock timestamps.

6. **Credential rejection requires explicit evidence.**

   Given captured provider responses for HTTP 401 and HTTP 403,
   when the classifier processes them,
   then 401 produces `credential_rejected` / `provider_unauthorized`, while 403
   produces `probe_failed` / `provider_forbidden`.

7. **Forced scope is exact and does not redo credentials.**

   Given two Anthropic harnesses and one Codex harness on `gibson`, plus an Anthropic
   harness on another host,
   when an authenticated agent runs
   `tightbeam model-catalog-refresh --host gibson --provider anthropic`,
   then post-admission probes run for the two matching Gibson keys only, the response
   is ordered by harness name, no onboarding, credential capture, or
   `credential-present` fact occurs, and any Anthropic token renewal and atomic
   credential-file write uses the existing internal probe and rotation-harvest seams;
   and when `tightbeam list` projects the forced attempt,
   then `actor` is the authenticated call principal and `origin` is the Gateway call
   origin, while automatic boot and `credential_present` attempts have actor
   `{kind: process, id: tightbeam}` and null origin.

8. **A concurrent active probe cannot satisfy a forced request.**

   Given a TTL probe is active for a matching key,
   when two forced requests arrive before that attempt completes,
   then exactly one follow-up generation starts after the TTL generation completes,
   both requests wait for the follow-up, and the TTL completion cannot satisfy either
   request.

9. **Credential absence and lookup failure are typed.**

   Given captured credential-subsystem results for missing, in-progress,
   unreadable-store, and unknown-kind states,
   when each state prevents the provider request,
   then the result is `credential_unavailable` with cause code
   `credential_missing`, `credential_in_progress`, `credential_store_unreadable`,
   and `credential_kind_unknown`, respectively; no provider I/O starts and any prior
   successful inventory remains.

10. **Late task results cannot overwrite newer state.**

   Given test control of task completion messages,
   when a completion for a non-active generation arrives after a newer generation
   has completed,
   then the late completion changes no catalog field and no waiting forced response.

11. **Restart semantics are visible and retry-safe.**

    Given cached inventory, completed history, a forced caller, and an active
    Anthropic attempt whose injected provider transport is blocked,
    when the lifecycle owner restarts ModelCatalog,
    then the scheduler's ordered event log shows the old capability task and every
    descendant provider transport exit before the replacement process starts its boot
    attempt, shows no overlap between old and new provider I/O, renewal, or
    credential-file writes, shows that the new process exposes no pre-restart
    inventory and reports `lastProbe.result=never_probed` until its boot attempt
    completes, and shows that the new process accepts a retried forced command without
    credential setup.

12. **Network and authentication failures stay separate.**

    Given redacted real envelopes for client-side `bwrap` connect `EPERM`, probe-side
    connect `EPERM`, SSH public-key rejection, provider HTTP 401, and provider HTTP
    403,
    when each path is exercised,
    then the client-side failure admits no request and mutates no catalog state; the
    other four classify as `probe_network_forbidden`, `remote_host_auth_failed`,
    `provider_unauthorized`, and `provider_forbidden`, respectively.

13. **Failure handling cannot leak raw material.**

    Given probe failures whose raw bodies and stderr contain a sentinel token, URL,
    local path, and SSH destination,
    when an agent reads `tightbeam list` and `model-catalog-refresh` output and the
    test captures catalog logs,
    then none of those sentinel values appear in the projections or logs and only the
    closed result and cause fields identify the failure.

14. **Authentication and scope refusals are side-effect free.**

    Given an unauthenticated caller, an inactive principal, an unknown host, and a
    host/provider pair with no configured harness,
    when each requests a forced probe,
    then the authentication cases receive the existing gateway authentication
    refusal, the scope cases receive `catalog_scope_not_found`, and no provider read
    starts.

15. **Existing list consumers remain compatible.**

    Given a recorded `tightbeam list` response from before this change,
    when the same catalog inventory is projected after this change,
    then `models` is structurally identical and the only catalog addition is the
    sibling `modelCatalogs` field defined here.

16. **Deterministic tests cover time and races.**

    Given an injected wall clock, monotonic clock, transport, and task-completion
    scheduler,
    when catalog tests exercise boot, expiry, forced coalescing, late completion,
    ModelCatalog timeout, gateway wait timeout, and restart,
    then no test depends on wall-clock sleep or a live provider and repeated runs
    produce the same state and response order.

17. **Attempt and gateway timeouts preserve ownership.**

    Given an admitted forced request and injected clocks,
    when its capability task remains active for 40 seconds,
    then the scheduler's ordered event log shows the lifecycle owner terminate the
    task and every descendant provider transport, observe all exits, and only then
    let `ModelCatalog` atomically record `probe_failed` / `attempt_timeout`; and given
    a ModelCatalog test double that does not answer,
    when the gateway wait reaches 85 seconds,
    then the gateway returns `model_catalog_refresh_wait_timeout` without fabricating
    a result or mutating catalog state.

18. **A real provider smoke proves the external path.**

    Given a configured test host and a credential that the credential subsystem
    reports as ready and working,
    when an operator records `tightbeam list`, runs
    `tightbeam model-catalog-refresh --host <host> --provider <provider>`, and
    records `tightbeam list` again,
    then the command returns `available_nonempty` or `available_empty`, the affected
    keys' completed timestamps advance, the second list agrees with the command, and
    no credential onboarding occurs. The verification record includes the redacted
    real response fixture used by the deterministic catalog-parser tests.

19. **Agent guidance activates with the shipped command.**

    Given an implementation candidate in an elected product line where
    `model-catalog-refresh` exists and passes its command acceptance,
    when that candidate enables the public command,
    then the same candidate amends the always-on operating manual with one grounded
    directive: read `modelCatalogs` before inferring why `models` is empty; for a
    never-probed, failed, rejected, unavailable, or stale catalog, run
    `model-catalog-refresh` for that host and provider, then read the new typed
    evidence. No operating-manual amendment lands before the command exists.

## Open Questions

1. **BLOCKING for implementation, not for independent spec review:** Which product
   line does Mike elect for implementation? The work item is untargeted. No builder
   may infer 0.1.8, active 0.1 maintenance, or main/0.2.0 from branch existence,
   source-code provenance, or this proposal.

This revised proposal is ready for reviewer verification. It is not implementation
authority until that review records a passing verdict, the approved content hash is
bound to the work item, and Mike has elected an implementation target.
