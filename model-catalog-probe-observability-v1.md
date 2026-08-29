# Model Catalog Probe Observability v1

Status: **PROPOSAL — exact-tip review changes addressed; pending owner-routed re-review**

Work item: `wi_54d54f16-8e8e-4895-8191-6bb64384bcb8`

Implementation target: **UNTARGETED**. The work item does not elect Tightbeam
0.1.8, active 0.1 maintenance, or main/0.2.0. Branch existence and the source-code
commit inspected for reconciliation do not supply a target.

This specification extends `per-host-catalogs-v1.md`, `model-identity-v1.md`,
`credential-kinds-v1.md`, `cli-surface-v1.md`, and the named Claude divergence in
`harness-support.md`. It also supersedes only the `harness-adapter-seam-v1.md`
`fetch_catalog(state)` sentence that says catalog refresh is gateway-only and has no
placement target. The surviving seam remains one `fetch_catalog(state)` callback;
`state` names the owning host and its local or SSH runner context. No parallel catalog
transport or second callback is created.

It reconciles the reviewed generic org-fault specification at commit
`153839b31704a6af28242d08a38ebfa35cc81540` with the catalog seams on Tightbeam
main at `6f1cfc787b6a589e3e725e74e3a370bf71b130b1`, with the canonical specs on
main at `b20194fe464f5792788bb5b7033245e4d0696889`. Those commits are evidence of
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

Exact-tip review verdict `att_e0717449-a3d5-4c6b-929d-10b5b9bc81f9` found that the
first restart closure could wait forever for descendant exit. This revision replaces
that unbounded drain with one bounded owning-host attempt-runner lease, a typed
cleanup-unconfirmed result, and production lifecycle evidence for local and SSH
process trees.

Exact-tip review verdict `att_bc1fbe38-cf5e-4b8d-bcaf-34f7a233aaf4` found that a
runner restart could erase the only lease authority and that retained lifecycle
evidence had no closed privacy contract. This revision makes one durable owning-host
authority record precede all attempt I/O, requires replacement runners to recover it
fail closed, and defines bounded lifecycle evidence fields, retention, and redaction.

Exact-tip review verdict `att_93dca3da-7d9e-4a14-afe5-0cc3627ab509` found that the
proposal could pass while Claude still had zero usable models, that malformed
authority state could hold a key forever, and that lifecycle identity non-reuse was
only asserted. This revision requires repair of the established Claude adapter-filter
starvation, bounded namespace recovery from corrupt authority, and a boot-scoped
monotonic identity allocator with deliberate reuse tests.

Exact-tip review verdict `att_6c18dc92-b0c4-46ab-a2e1-1baa945e20b6` found four
remaining gaps against commit `3c7b1b45344bafbc912f671950fbcd40bf2af340`:
Claude placement capability depends on session cwd and settings, the active adapter
seam still claimed gateway-only catalog fetching, capability-I/O failures lacked a
closed mapping, and corrupt high-water state had no typed recovery. This revision
makes the exact session context authoritative for placement, supersedes the stale
catalog sentence, closes the capability outcome mapping, and makes allocator faults
fail closed until a new host boot safely resets the generation domain.

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

The MVP also repairs the reported Claude catalog. Current main actively reads the
provider, then can filter a non-empty provider response to zero against one
cwd/settings-dependent adapter snapshot. The repaired catalog retains the owning
host's provider inventory. The exact target session's adapter capability response,
not a context-free catalog snapshot, is the final authority for Claude placement.

## Non-Goals

- This specification does not create an organization-wide fault, incident,
  ownership, waiver, review-obligation, claim, or outbox system.
- It does not infer that an empty catalog means a credential is absent or expired.
- It does not start onboarding, OAuth, credential capture, credential copying, or
  credential repair.
- It does not change credential storage, rotation harvest, or `credential-present`
  handling.
- It does not change the catalog refresh interval, routing policy, picker ranking,
  CAP, harness switching, or runtime model application. It does require placement to
  treat the exact target session's existing capability check as authoritative instead
  of treating a context-free Claude catalog entry as final admission.
- It does not persist catalog inventory, result history, timestamps, or active-probe
  state across a ModelCatalog process restart. The owning-host authority and
  generation high-water records are lifecycle safety state, not catalog state or
  probe history.
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
that `tightbeam list` already projects under `models[host][harness]`. For a harness
with a named context-dependent model divergence, this is provider discovery evidence,
not final placement approval. A failed probe does not erase an earlier successful
inventory. A successful empty response replaces an earlier non-empty inventory with
an empty inventory.

**Probe attempt** — one catalog derivation for one catalog key: obtain the current
credential and perform one provider read when a credential is available. A probe
attempt has a start time, a trigger, an actor, an optional origin, and one terminal
result. It does not create an adapter session or read session-scoped configuration
options.

**Active probe** — the probe attempt currently performing credential lookup,
provider I/O, or bounded cleanup for a catalog key. At most one probe is active in
`ModelCatalog` for a catalog key.

**Attempt lease** — the internal per-catalog-key execution lease enforced by the host
that performs credential lookup and provider I/O. The owning host atomically creates
the lease's authority record before it starts credential lookup, renewal, a
credential-file write, or provider I/O. It releases the lease only after it locally
observes the attempt task and every process in its lifecycle unit exit. A lease can
remain held after `ModelCatalog`
records `attempt_cleanup_unconfirmed`. While held, a later request may retry bounded
cleanup but cannot start credential or provider I/O. The lease is
owning-host process-lifecycle state, not catalog inventory or probe history.

**Lease authority record** — the durable active-lease authority for one catalog key
on its owning host. Its closed fields are `schemaVersion`, `host`, `harness`,
`leaseGeneration`, `hostBootId`, `lifecycleUnitId`, and `phase`, where `phase` is
`reserved`, `running`, or `cleaning`. `hostBootId` and `lifecycleUnitId` identify one
operating-system lifecycle unit without storing a command, path, environment value,
or provider material. The owning host retains exactly one authority record per key
while a lease is reserved or held and deletes it atomically only after it proves the
unit absent. The record survives an attempt-runner exit or restart. A host reboot
changes `hostBootId`; that mismatch proves that processes from the prior boot cannot
remain and permits deletion of the old record.

**Lifecycle identity** — the tuple `{hostBootId, host, harness, leaseGeneration}`.
The owning host allocates `leaseGeneration` with one atomic, monotonically increasing
arbitrary-precision high-water counter per catalog key. That counter is outside runner
memory, survives runner replacement, and is retained until `hostBootId` changes. The
allocator never accepts a caller-supplied value, decrements the counter, or issues a
prior value during the same boot. Deleting an authority record does not delete or
lower the counter. Therefore a lifecycle identity cannot be reused while a process
from its boot could remain.

**Generation high-water record** — the allocator's closed per-catalog-key state:
`{schemaVersion, host, harness, hostBootId, issuedThrough}`. The authenticated
owning-host lifecycle namespace updates it with atomic compare-and-swap before it
returns a generation. A supported write exposes either the prior complete record or
the next complete record; it cannot expose torn or partial bytes. The namespace
retains the record after authority deletion and runner restart and replaces it only
when the host boot changes. Host/harness configuration creates the current-boot
record with `issuedThrough=0` before the key becomes visible to `ModelCatalog`; no
attempt lazily recreates a missing record. The namespace exposes no same-boot delete,
reset, decrement, or schema-downgrade operation. An unreadable, missing, malformed,
unsupported, or host-boot-mismatched record for a visible key is allocator state
unavailable, never a pristine counter.

**Capability context** — the exact placement inputs that can change a harness's
offered model set: owning host, harness, adapter version, projected home, credential
grant, session cwd, and resolved project settings. Raw cwd, paths, settings, and grant
material are not catalog fields and are not persisted or logged by this proposal.

**Placement authority** — the existing adapter session boundary evaluated with the
exact capability context. For Claude, the `model` option in that session's
`session/new` response is the authoritative offered set. A selected value succeeds
only after the existing `session/set_config_option` verification for that same
session. The context-free cached inventory can reject a provider-absent identity, but
it cannot by itself approve a Claude placement.

**Capability-I/O outcome** — a typed placement result, separate from catalog probe
state. A failed `session/new` transport or protocol exchange is
`adapter_unavailable`; a successful session response with no usable `model` option or
with malformed model `configOptions` is `model_capability_unavailable`; and a
well-formed offered set that omits the selected identity, or an explicit
`session/set_config_option` model refusal, is `model_unavailable`. These outcomes do
not change `lastProbe`, erase cached inventory, or imply credential rejection.

**Lifecycle evidence record** — the privacy-closed terminal summary retained for
verification. Its only fields are `schemaVersion`, `host`, `harness`,
`leaseGeneration`, `transportKind`, `recoveryKind`, `cleanupStartedAt`,
`termSentAt`, `killSentAt`, `observedEmptyAt`, `unitState`, and `outcome`.
`transportKind` is `local` or `ssh`; `recoveryKind` is `none`,
`runner_replacement`, `authority_corrupt`, or `prior_boot`;
`unitState` is `absent`, `present`, or `unknown`; `outcome` is `reaped` or
`cleanup_unconfirmed`; the four timestamps are epoch milliseconds or null. `reaped`
requires `unitState=absent` and a non-null `observedEmptyAt`.
`cleanup_unconfirmed` requires `unitState=present` or `unitState=unknown` and a null
`observedEmptyAt`. The owning host retains at most the newest terminal summary per
catalog key. A later terminal summary replaces it atomically, and a host restart
clears it. No other runner event or process-table material is retained.

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
- `probe_failed` — lifecycle allocation, transport, remote-host access, timeout,
  protocol, or response parsing prevented a valid provider result;
- `credential_rejected` — the provider explicitly rejected the supplied provider
  credential; and
- `credential_unavailable` — Tightbeam could not obtain a credential with which to
  attempt the provider request.

**Cause code** — a privacy-safe refinement of a non-success result. The closed cause
codes are:

| Result | Cause codes |
| --- | --- |
| `probe_failed` | `provider_forbidden`, `transport_timeout`, `attempt_timeout`, `attempt_cleanup_unconfirmed`, `lifecycle_allocator_unavailable`, `remote_host_auth_failed`, `probe_network_forbidden`, `client_version_filtered_empty`, `malformed_response`, `unclassified_failure` |
| `credential_rejected` | `provider_unauthorized` |
| `credential_unavailable` | `credential_missing`, `credential_in_progress`, `credential_store_unreadable`, `credential_kind_unknown` |

Successful results and `never_probed` have no cause code. HTTP 401, or an equivalent
structured provider-authentication rejection, maps to `provider_unauthorized`. HTTP
403 alone maps to `provider_forbidden`; it does not prove that the credential is
invalid. `attempt_cleanup_unconfirmed` means the caller did not receive an owning-host
`reaped` acknowledgement within the five-second cleanup deadline. It is a terminal
probe result. When the runner itself cannot confirm exit, the owning-host authority
record retains the attempt lease until that runner or a replacement runner observes
the lifecycle unit absent. After an SSH acknowledgement loss, the remote authority
record and locally observed lifecycle-unit state remain authoritative.

`lifecycle_allocator_unavailable` means the owning host cannot prove a monotonic
current-boot generation and therefore starts no attempt I/O. A later forced request
retries the read but cannot recreate or lower that boot's record. A new host boot is
the lawful recovery boundary: the changed `hostBootId` proves that no process from
the prior generation domain survives, configuration creates a new zero record before
exposing the key, and a forced request may then allocate generation one.

`available_empty` is harness-specific. The Anthropic catalog contract can accept a
valid provider envelope whose model array is empty. A non-empty valid Anthropic
provider response produces `available_nonempty`; no context-specific adapter filter
may reduce the host catalog to empty. The Codex catalog contract cannot accept
client-version-filtered empty: when that provider-side filter removes every returned
entry, the result is `probe_failed` with
`causeCode=client_version_filtered_empty`, as required by
`per-host-catalogs-v1.md`.

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
  remains structurally backward compatible.
- `harness-support.md` names Claude model selection as cwd/settings-dependent. A
  context-free host inventory cannot prove what a later Claude session will offer.
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
   state of another catalog key. Placement capability evidence belongs only to the
   exact session and capability context that produced it; it never becomes a global
   `{host,harness}` allow-list.

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

6. **One mutation seam owns catalog state.** Attempt-task completions send typed
   results to `ModelCatalog`. Only `ModelCatalog` changes catalog inventory,
   active-probe state, last result, probe timestamps, trigger, actor, origin, or
   staleness. Owning-host lifecycle records do not mutate or duplicate catalog state.

7. **One attempt runs per catalog key.** A catalog key never has overlapping
   credential lookups, provider reads, renewal operations, or
   credential-file writes, including across a ModelCatalog restart. The owning-host
   authority record is created before any such I/O. A runner never grants a new
   attempt lease until it reconciles and releases the prior authority record. Runner
   death, replacement, or lost volatile state cannot authorize replacement I/O. The
   boot-scoped allocator never reissues a lifecycle identity after authority-record
   deletion or runner restart. Unavailable allocator state completes the attempt as
   `probe_failed` / `lifecycle_allocator_unavailable` before credential or provider
   I/O. A completion can mutate state only when its generation
   matches the active generation for that key; a late completion from an older
   generation is discarded.

8. **Forced means post-admission evidence.** A successful
   `model-catalog-refresh` response is based on an attempt that started after the
   request was admitted. An already-active attempt cannot satisfy that request.

9. **Concurrent forced requests coalesce safely.** Requests admitted before the
   required follow-up attempt starts may share that attempt. A request admitted after
   it starts requires a later attempt. Coalescing never changes the result or scope.

10. **Restart, corrupt authority, and allocator failure are explicit.** A ModelCatalog
    or attempt-runner restart discards its volatile state, but it does not discard an
    owning-host authority record. A replacement may request a boot attempt immediately. The
    replacement runner first reads and reconciles any prior record, then applies the
    five-second termination-and-reaping protocol to the named lifecycle unit. It
    starts new credential or provider I/O only after it observes the unit
    absent and atomically deletes the old record. If recovery or cleanup is
    unconfirmed at five seconds,
    the attempt completes as `probe_failed` / `attempt_cleanup_unconfirmed`; the old
    record remains and no new I/O starts. A later automatic or forced request repeats
    this bounded recovery, which supplies an agent-reachable exit once the owning
    host observes the unit absent. If the authority record is unreadable, malformed,
    or unsupported, the replacement runner uses the authenticated lifecycle namespace
    to enumerate every current-boot unit for the catalog key without trusting that
    record. It applies the same bounded cleanup to all matching units, deletes the bad
    record only after it observes none, and may then start a new attempt. Failed
    enumeration returns the typed unconfirmed result and a later forced request
    retries the same bounded recovery. An unreadable, missing, malformed,
    unsupported, or mismatched current-boot generation record returns
    `probe_failed` / `lifecycle_allocator_unavailable`, authorizes no attempt I/O, and
    is not recreated during that boot. After a host reboot changes `hostBootId`, key
    configuration creates a new zero record before the key becomes visible, and a
    forced request can safely proceed in the new generation domain. Before any
    post-ModelCatalog-restart attempt
    completes, each catalog reports `lastProbe.result=never_probed`; boot probes may
    be active at the same time.

11. **Forced probing does not perform a credential ceremony.** It uses the same
    credential lookup and provider-read path as automatic catalog derivation. The
    command does not invoke onboarding or credential capture and does not file a
    `credential-present` fact. Existing Anthropic renewal, atomic credential-file
    write, and rotation-harvest behavior remains in force; this specification adds no
    second renewal or credential-write seam.

12. **Observation is privacy-closed.** Catalog state, placement capability outcomes,
    `model-catalog-refresh` output, generation high-water records, authority records,
    lifecycle evidence
    records, runner logs, and verification artifacts never retain or log credential
    values, authorization headers, provider frames or response bodies, request URLs,
    prompts, cwd values, settings names or values, projected-home or grant
    identifiers, local or remote paths, SSH destinations, command lines or argument
    vectors, environment names or values, process-table rows, or raw stdout/stderr.
    Catalog surfaces use only their defined fields and closed result and cause values.
    Internal lifecycle records use only their closed schemas defined here.

13. **Existing model consumers remain structurally compatible.** The shape of
    `models[host][harness]` does not change. Claude contents become the owning-host
    provider inventory required by `per-host-catalogs-v1.md`, rather than one
    session-context filter. New state appears in a sibling `modelCatalogs` field. For
    a named context-dependent harness, the inventory is not final placement approval;
    the source contract already leaves runtime final.

14. **Pre-gateway failures cannot mutate catalog state.** If a caller cannot connect
    to Tightbeam, including a client-side `bwrap --unshare-net` connect `EPERM`, no
    forced request is admitted and no catalog attempt or result is recorded.

15. **Claude catalog and placement have one authority chain.** A non-empty valid
    Claude provider response cannot become a successful empty host catalog. The
    owning-host provider inventory is discovery evidence. Placement first requires
    the selected identity to be present in that inventory, then treats the exact
    target session's cwd/settings-aware adapter response and model application as
    final. No static, projected-home, or arbitrary scratch-session offered set can
    globally approve or remove Claude identities. Capability-I/O failures use only
    the closed placement outcomes defined here and never mutate catalog probe state.

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

### Claude catalog repair

At reconciled product commit `6f1cfc787b6a589e3e725e74e3a370bf71b130b1`,
Claude catalog derivation actively reads `/v1/models`; the reported zero inventory is
not evidence of a cache-only path. The defect occurs afterward: `keep_selectable`
intersects provider entries with a static plus projected-home adapter set, the static
set can rot, the SSH path does not read a remote home, and any one adapter offered set
depends on session cwd and resolved settings. That intersection reduced the live
account's non-empty provider response to zero and still could not prove a different
session's placement.

The repaired Claude catalog attempt reads the provider on the owning host through the
existing credential path and publishes that structured provider inventory without a
global adapter-offering filter. On an SSH catalog key, the provider read executes on
the remote owning host. This proposal makes the existing host-aware
`fetch_catalog(state)` callback the one catalog seam and supersedes the gateway-only
sentence in `harness-adapter-seam-v1.md`; a builder does not add a second capability
transport beside it.

Placement supplies the exact target cwd and resolved settings to the existing adapter
session boundary. The `session/new` response for that session supplies its offered
`model` values. Placement may proceed only when the structured selection is in the
owning-host provider inventory and the exact session offers it; the existing verified
`session/set_config_option` then applies it. Missing or malformed model options return
`model_capability_unavailable`. A well-formed omission or explicit model refusal
returns `model_unavailable`. Session transport or protocol failure returns
`adapter_unavailable`. None becomes a catalog success, catalog failure, credential
judgment, silent alias substitution, or global filter update.

For `placementAuthority=session_context`, a successful `ModelCatalog.route` answer is
provider eligibility only. Placement does not report a spawn, tune, or harness-change
success and does not publish a context-specific offer until the exact session boundary
passes. An existing session uses the offered set retained from its own
`session/new` or `session/load` response and the same verified model application. If
that session has no trustworthy retained set, it returns
`model_capability_unavailable`; it does not fall back to the host catalog.

The adapter may equate one offered alias with one structured provider identity only
when its private parse/render mapping and a same-session
`session/set_config_option` plus next-turn `modelUsage` readback prove that exact
identity. Otherwise the alias does not authorize the selection. Placement does not
rewrite a requested identity to a different model.

The incident regression fixture contains the redacted non-empty provider envelope and
two session capability contexts for the same owning host and grant: one cwd/settings
context that offers an exact identity and one that refuses it. Catalog derivation must
remain `available_nonempty` in both cases. Placement must accept the identity only in
the offering context and return the closed typed refusal in the other. A genuinely
empty provider array may remain `available_empty`.

### Owning-host attempt runner

Every catalog attempt runs through one internal attempt runner on the host that owns
the catalog key. The runner first obtains the owning host's exclusive kernel lock for
that key. The lock serializes reserve, recovery, cleanup, and release, and the kernel
releases it if the runner dies. Before any attempt I/O, the lock holder asks the
boot-scoped high-water allocator for the next lease generation. If the configured
key's record is unreadable, missing, malformed, unsupported, or names another boot,
the runner returns `lifecycle_allocator_unavailable`, performs no attempt I/O, and
does not create or repair a same-boot record. Otherwise it atomically reserves a
per-catalog-key authority record with that generation and its lifecycle identity. It
creates the lifecycle unit in the authenticated namespace with labels for
the exact catalog key and lifecycle identity. Those labels are queryable without
reading the authority record. The catalog-key label is version-invariant across
authority-record schema versions. It then starts the attempt task and all
descendants inside that unit and changes the record from `reserved` to `running`.
The lifecycle unit is the process-ownership boundary; a bare process identifier or
local transport process is not sufficient authority. The runner holds the kernel
lock until it deletes the authority record or exits.

For an SSH host, the remote authority record and lifecycle unit own the lease;
observing the local SSH client exit is not proof of remote cleanup. The remote runner
may outlive the SSH channel that requested the attempt. Only the authenticated
internal ModelCatalog host-transport path can reserve, recover, stop, or query a
lease. The public Gateway cannot address this seam directly.

A runner starts no credential lookup, renewal, credential-file write, or provider I/O
until it holds the kernel lock and has read back the `running` authority record for
the lifecycle unit. If the runner exits at any point, a replacement must obtain that
lock and read the authority record before
it handles a new lease request. If the lock cannot be obtained inside the five-second
caller deadline, the request returns `cleanup_unconfirmed` and starts no I/O. A
`reserved`, `running`, or `cleaning`
record on the current host boot is fail-closed: the replacement queries the named
lifecycle unit, performs bounded cleanup when it exists, and grants no new lease
while absence is unconfirmed. An absent named unit permits atomic record deletion
while the lock is held. The dead runner cannot resume after the kernel has released
its lock. A prior-boot record also permits deletion because no process from that boot
can survive the reboot; the replacement emits `reaped` evidence with
`recoveryKind=prior_boot` and `unitState=absent`.

If the authority record is unreadable, malformed, or uses an unsupported schema, the
lock holder does not trust any field from it. It asks the authenticated owning-host
lifecycle namespace for every live current-boot unit labeled with the catalog key.
At cleanup start it records `recoveryKind=authority_corrupt`, sends termination to all
matching units in parallel, sends forced termination at two seconds to every survivor,
and at five seconds reports `reaped` only if the namespace reports no matching unit.
It may then delete the bad record and reserve a new generation. If enumeration or
absence is unconfirmed, it retains the record, returns `cleanup_unconfirmed`, ends the
runner to release the kernel lock, and authorizes no I/O. A later automatic or forced
request retries this same bounded path, so a readable lifecycle namespace supplies an
agent-reachable terminal recovery without trusting or manually editing the record.

ModelCatalog assigns the attempt's 40-second execution budget, and the runner enforces
that budget independently of ModelCatalog and the initiating SSH channel. Channel
loss cannot leave the lock held indefinitely: the runner starts cleanup when its
local monotonic budget expires and ends with `reaped` or `cleanup_unconfirmed` within
the following five seconds. At cleanup start, the lock holder atomically changes the
authority record to `cleaning` before it sends a termination signal.

Normal completion releases the lease only after the runner reaps the task and its
entire lifecycle unit. Timeout, ModelCatalog restart, runner restart, and later
requests against a retained lease use this single cleanup protocol:

1. At cleanup start, send termination to the whole lifecycle unit.
2. At two seconds, if any member remains, send forced termination to the whole unit.
3. At five seconds, return `reaped` only if the owning host has observed the lifecycle
   unit absent. Atomically delete the authority record and release the lease on
   `reaped`.
4. Otherwise persist the closed `cleanup_unconfirmed` evidence record, retain the
   authority record and lease, and end the runner so the kernel releases its lock.

The caller enforces the same five-second deadline end to end, including local runner
dispatch or SSH connection and command delivery. If it lacks a structured
acknowledgement at that deadline, it stops the control transport and returns
`cleanup_unconfirmed`; it does not extend cleanup to the provider transport's
30-second bound.

The caller maps `cleanup_unconfirmed` to `probe_failed` /
`attempt_cleanup_unconfirmed`, clears `activeProbe`, and retains prior inventory. A
later automatic or forced attempt asks the current runner to acquire the lease. If a
prior authority record remains, that runner repeats bounded recovery and cleanup. It
grants the new lease only after it locally observes the old unit absent and deletes
the record. If cleanup remains unconfirmed, the new request returns the same typed
failure within five seconds and starts no credential or provider I/O.

For SSH execution, the remote runner returns a structured reaping acknowledgement.
A missing acknowledgement, including an SSH disconnect, is
`cleanup_unconfirmed` for that caller. A remote runner may release the lease only
from its own observed lifecycle-unit state; a later caller must recover the remote
authority record before it starts I/O. Generation matching still rejects any stale
completion message that arrives after cleanup.

A terminal record for an attempt that needed no recovery uses `recoveryKind=none`.
A replacement runner that recovers a valid authority record uses
`recoveryKind=runner_replacement`. Corrupt-record and prior-boot paths use their
corresponding closed values.

Host/harness configuration creates the generation high-water record before exposing
the key to ModelCatalog. The lifecycle namespace persists that non-deletable record
for the current boot. The runner persists only the authority record while a lease
exists and the newest terminal lifecycle evidence record after an outcome. It may log only the
lifecycle evidence record's closed fields. A lifecycle-unit query reduces process
state in memory to `present`, `absent`, or `unknown`; the runner does not retain or
log process-table rows, process identifiers, commands, paths, arguments, environment
material, stdout, or stderr. Test and verification artifacts apply the same reduction
and redaction. The authority record is deleted on observed absence without changing
the high-water record. The terminal evidence record is replaced by the next terminal
outcome for that key or cleared by host restart. When a new boot changes
`hostBootId`, configuration creates a new zero high-water record before re-exposing
the key; no old lifecycle identity can collide because `hostBootId` is part of it.

### List projection

`tightbeam list` retains the existing `models` field and adds:

```json
{
  "modelCatalogs": {
    "gibson": {
      "claude": {
        "provider": "anthropic",
        "placementAuthority": "session_context",
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
`placementAuthority` is `session_context` for a harness with a named
cwd/settings-dependent model divergence and `catalog_then_runtime` otherwise. This
static field makes the catalog-to-placement contract visible without exposing cwd or
settings.

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

Each HTTP provider read retains its existing 30-second bound. `ModelCatalog` assigns a
40-second execution deadline for each attempt, including credential lookup, provider
I/O, and remote-host transport. The owning-host runner enforces the remaining budget
locally. When that deadline expires, the runner applies the five-second cleanup
protocol. A `reaped` acknowledgement completes the generation as `probe_failed` /
`attempt_timeout`. `cleanup_unconfirmed` completes it as
`probe_failed` / `attempt_cleanup_unconfirmed`; the caller treats the lease as
unreleased until the same runner or a replacement runner recovers the authority
record and proves the lifecycle unit absent.

The gateway waits at most 95 seconds for the admitted key set. This covers the
remainder of one already-active 40-second execution window and its five-second
cleanup, the forced request's required 40-second execution window and five-second
cleanup, and five seconds of dispatch overhead. If the gateway wait expires before
`ModelCatalog` returns every required result, the gateway returns the top-level error
`model_catalog_refresh_wait_timeout`. The gateway does not fabricate a probe result
or mutate catalog state. The caller may retry.

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
- SSH host authentication failure while starting an attempt with no retained lease
  becomes `probe_failed` / `remote_host_auth_failed`.
- During cleanup of a known lease, any missing `reaped` acknowledgement at the
  five-second deadline, including SSH authentication or transport loss, becomes
  `probe_failed` / `attempt_cleanup_unconfirmed`.
- A transport deadline becomes `probe_failed` / `transport_timeout`.
- An unavailable generation high-water record becomes `probe_failed` /
  `lifecycle_allocator_unavailable` before attempt I/O.
- A Codex response whose entries are all removed by the client-version filter becomes
  `probe_failed` / `client_version_filtered_empty`.
- A successful transport with an invalid catalog envelope becomes `probe_failed` /
  `malformed_response`.
- Any unmatched failure becomes `probe_failed` / `unclassified_failure`.

Classifier tests use captured, redacted provider and transport envelopes from real
probe responses. Hand-written ideal envelopes do not establish classifier fidelity.
The catalog path stores and logs only the typed result, cause code, scope, actor,
origin, and timestamps. The runner stores and logs only the closed authority and
lifecycle evidence fields. Neither path stores or logs raw response bodies, process
tables, command material, environment material, or raw process output.

Placement capability classification occurs at the adapter session boundary. It uses
the closed `adapter_unavailable`, `model_capability_unavailable`, and
`model_unavailable` mapping in the Terms section. Placement outcomes do not enter
`ModelCatalog` as probe results.

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
    Anthropic attempt whose injected owning-host runner retains its lease and whose
    task ignores normal termination,
    when ModelCatalog restarts and its boot attempt requests that lease,
    then the injected clock and runner log termination at zero seconds, forced
    termination at two seconds, and one of these outcomes at five seconds: `reaped`
    before any new credential lookup or provider I/O starts, or
    `probe_failed` / `attempt_cleanup_unconfirmed` with the lease retained and no new
    I/O. Given the unconfirmed outcome, when a forced request retries while cleanup
    remains unconfirmed, then it returns the same typed failure within five seconds
    and starts no credential or provider I/O; and when a later
    forced request observes the old unit absent, then the runner releases the lease,
    starts the new attempt,
    and does not repeat credential setup. Given the runner is killed after its
    authority record becomes `reserved`, `running`, or `cleaning`, when an injected
    replacement runner handles the next automatic or forced request, then it obtains
    the released kernel lock, recovers that exact record, and either proves the named
    unit absent before new I/O or returns `attempt_cleanup_unconfirmed` by five
    seconds. The scheduler proves no old and replacement credential lookup, renewal,
    credential-file write, or provider I/O overlap in each kill phase. Given a
    truncated or unsupported authority record and one matching old lifecycle unit,
    when a forced request obtains the key lock, then it ignores the bad fields,
    enumerates by authenticated catalog-key label, applies termination at zero seconds
    and forced termination at two seconds, and by five seconds either records
    `recoveryKind=authority_corrupt` / `reaped`, deletes the bad record, and continues
    the admitted attempt with a new generation, or returns
    `attempt_cleanup_unconfirmed` without I/O. Given that unconfirmed outcome, when a
    later forced request observes the namespace empty, then it completes the recovery
    without credential setup or manual record editing.

12. **Network and authentication failures stay separate.**

    Given redacted real envelopes for client-side `bwrap` connect `EPERM`, probe-side
    connect `EPERM`, ordinary attempt-start SSH public-key rejection with no retained
    lease, provider HTTP 401, and provider HTTP 403,
    when each path is exercised,
    then the client-side failure admits no request and mutates no catalog state; the
    other four classify as `probe_network_forbidden`, `remote_host_auth_failed`,
    `provider_unauthorized`, and `provider_forbidden`, respectively.

13. **Failure handling and lifecycle evidence cannot leak raw material.**

    Given probe and placement-capability failures whose credential, authorization
    header, request URL, prompt, cwd, settings, local and remote paths, SSH
    destination, command arguments, environment, raw provider frame, stdout, and
    stderr each contain a distinct sentinel,
    when an agent reads `tightbeam list` and `model-catalog-refresh` output and the
    test captures catalog logs, runner logs, generation high-water records, authority
    records, lifecycle evidence records, and retained verification artifacts,
    then no sentinel appears in any captured or retained surface. The authority and
    lifecycle evidence records contain exactly their closed fields. A process-state
    query retains only `unitState`, never a process-table row. Each key retains one
    generation high-water record for the current boot, at most one authority record
    while its lease exists, and one newest terminal evidence record until replacement
    or host restart.

14. **Authentication and scope refusals are side-effect free.**

    Given an unauthenticated caller, an inactive principal, an unknown host, and a
    host/provider pair with no configured harness,
    when each requests a forced probe,
    then the authentication cases receive the existing gateway authentication
    refusal, the scope cases receive `catalog_scope_not_found`, and no provider read
    starts.

15. **Existing list consumers remain compatible.**

    Given a recorded `tightbeam list` response shape from before this change,
    when an owning-host provider inventory is projected after this change,
    then `models` retains that structure and the only catalog-state addition is the
    sibling `modelCatalogs` field defined here; the Claude entry reports
    `placementAuthority=session_context`, so no consumer can treat its context-free
    provider inventory as final placement approval.

16. **Deterministic tests cover time and races.**

    Given an injected wall clock, monotonic clock, owning-host runner, transport, and
    task-completion scheduler,
    when catalog tests exercise boot, expiry, forced coalescing, late completion,
    ModelCatalog timeout, reaped and cleanup-unconfirmed outcomes, retained-lease
    retry, runner death in `reserved`, `running`, and `cleaning` phases, replacement
    recovery, corrupt-authority recovery, host-boot mismatch, gateway wait timeout,
    and restart; and when a test deletes an authority record, restarts the runner, and
    tries to reuse its issued lifecycle identity or lower the boot high-water counter,
    then both reuse attempts are refused and the next allocation has a greater
    generation. Given unreadable, missing-after-configuration, malformed,
    unsupported-schema, and host-boot-mismatched high-water records, each same-boot
    forced attempt returns `probe_failed` / `lifecycle_allocator_unavailable` and
    starts no credential or provider I/O. When an injected host reboot changes
    `hostBootId`, configuration creates a new zero record before exposing the key and
    the next forced attempt safely allocates generation one in the new domain. No test
    depends on wall-clock sleep or a live provider, and repeated runs produce the same
    state and response order.

17. **Attempt and gateway timeouts preserve ownership.**

    Given an admitted forced request and injected clocks,
    when its attempt task remains active for 40 seconds,
    then the owning-host runner starts its five-second cleanup protocol; a `reaped`
    acknowledgement records `probe_failed` / `attempt_timeout`, while an unconfirmed
    cleanup records `probe_failed` / `attempt_cleanup_unconfirmed`, and the runner
    grants no new lease until its lifecycle-unit query reports the old unit absent;
    both outcomes set `completedAt` no later than 45 seconds after `startedAt`; and
    given a ModelCatalog test double that does not answer,
    when the gateway wait reaches 95 seconds,
    then the gateway returns `model_catalog_refresh_wait_timeout` without fabricating
    a result or mutating catalog state.

18. **A real provider smoke proves repair of the affected Claude path.**

    Given the affected live Anthropic account on a local test host and a registered SSH
    test host, with the credential subsystem reporting ready and working,
    when an operator records `tightbeam list`, runs
    `tightbeam model-catalog-refresh --host <host> --provider anthropic` on each host,
    and records `tightbeam list` again,
    then each command returns `available_nonempty`, each Claude inventory has a
    positive model count, the completed timestamps advance, and each second list
    agrees with the command. On each host, two controlled session cwds with different
    resolved settings produce different real `session/new` model offerings. For each
    cwd, the user-facing placement offer is the intersection of provider inventory and
    that exact session offering; every identity it advertises passes real
    `session/set_config_option` and next-turn `modelUsage` in that session. An identity
    omitted by the second context is not offered there and returns `model_unavailable`
    if explicitly requested. `available_empty` does not pass this case. No credential
    onboarding occurs. The verification record includes the redacted real provider
    response and capability fixtures used by deterministic tests.

19. **Agent guidance activates with the shipped command.**

    Given an implementation candidate in an elected product line where
    `model-catalog-refresh` exists and passes its command acceptance,
    when that candidate enables the public command,
    then the same candidate amends the always-on operating manual with one grounded
    directive: read `modelCatalogs` before inferring why `models` is empty; for a
    never-probed, failed, rejected, unavailable, or stale catalog, run
    `model-catalog-refresh` for that host and provider, then read the new typed
    evidence. No operating-manual amendment lands before the command exists.

20. **Production process and runner-recovery ownership are proved locally and over
    SSH.**

    Given the production owning-host runner on a local test host and a registered SSH
    test host, plus a fixture helper that forks a descendant, ignores normal
    termination, and places distinct sentinels in its arguments, environment, stdout,
    and stderr,
    when each runner applies cleanup,
    then the privacy-closed owning-host lifecycle evidence shows termination at
    cleanup start, forced termination at two seconds, the lifecycle unit absent from
    the owning host by five seconds, and a structured `reaped` acknowledgement before
    any replacement helper starts. Given the local runner and then the remote runner
    are each killed while the fixture descendant remains active,
    when a production replacement runner handles the next request,
    then it obtains the released kernel lock, recovers the retained authority record,
    reaps the old lifecycle unit before granting a new lease, and emits a terminal
    evidence record with `recoveryKind=runner_replacement`. Given an SSH connection that
    drops before the acknowledgement,
    when the caller reaches its cleanup deadline,
    then its result is `probe_failed` / `attempt_cleanup_unconfirmed`; and when a
    replacement attempt later reaches the remote runner, then the runner grants its
    lease only after its lifecycle-unit query reports the old unit absent. Verification
    proves that no replacement credential lookup, renewal, credential-file write, or
    provider process overlaps the old unit, that runner
    death and the initiating SSH-channel exit do not erase authority, and that the
    five-second caller deadline includes SSH setup and delivery. Verification
    exercises the production kernel lock, authority record, and lifecycle-unit query
    but retains only the closed
    evidence record with `unitState=absent`. No fixture sentinel appears in runner
    logs, authority records, lifecycle evidence records, or verification artifacts. A
    local SSH-client exit, raw process-table capture, or an injected scheduler log
    alone does not pass this case. On both hosts, verification also writes a truncated
    authority record while a labeled fixture unit survives, proves namespace recovery
    reaps that unit before replacement I/O, deletes the bad record only after absence,
    and reaches a new attempt through a forced request. It then deletes a completed
    authority record and asks the production allocator to reissue its lifecycle
    identity; the allocator refuses and issues a greater generation. The production
    allocator fixture on both transports also presents unreadable, missing,
    malformed, unsupported, and mismatched current-boot high-water state; every case
    returns `lifecycle_allocator_unavailable` before attempt I/O. A controlled new-boot
    fixture proves that a changed `hostBootId` permits a new zero record and a distinct
    generation-one lifecycle identity.

21. **The captured zero-model incident is repaired deterministically.**

    Given the redacted provider envelope and two cwd/settings capability fixtures that
    reproduced a non-empty Claude provider response followed by an empty
    `keep_selectable` result at product commit
    `6f1cfc787b6a589e3e725e74e3a370bf71b130b1`,
    when the repaired derivation runs through injected local and registered-SSH owning
    host transports,
    then both results are `available_nonempty` and both inventories equal the exact
    structured provider identities without reading the other host's projected home.
    For the selected identity, placement accepts the offering cwd/settings fixture and
    returns `model_unavailable` for the omitting fixture without changing catalog
    state. Repeated runs produce the same ordered inventory and placement outcomes,
    and no onboarding, credential capture, or `credential-present` fact occurs.

22. **Capability-I/O failures are closed and context-scoped.**

    Given exact-session fixtures for a failed `session/new` transport, a failed
    `session/new` protocol exchange, a response with no `model` option, malformed
    model `configOptions`, a well-formed offered set that omits the selection, and an
    explicit model-option refusal,
    when placement evaluates each fixture for its target cwd and resolved settings,
    then the first two return `adapter_unavailable`, the next two return
    `model_capability_unavailable`, and the last two return `model_unavailable`.
    Given an existing session with no trustworthy retained offered set, when a
    resident model-change validation consults it, then the result is
    `model_capability_unavailable` and the host catalog cannot approve the selection.
    None changes inventory, `activeProbe`, `lastProbe`, timestamps, credential state,
    or any other capability context's offer.

## Open Questions

1. **BLOCKING for implementation, not for independent spec review:** Which product
   line does Mike elect for implementation? The work item is untargeted. No builder
   may infer 0.1.8, active 0.1 maintenance, or main/0.2.0 from branch existence,
   source-code provenance, or this proposal.

This revised proposal is ready for owner-linked reviewer verification. It is not
implementation authority until an owner-linked review records a passing verdict, the
approved content hash is bound to the work item, and Mike has elected an
implementation target.
