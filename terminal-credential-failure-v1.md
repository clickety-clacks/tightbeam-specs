# Terminal credential failure backoff, redirect, and standing notice v1

Status: FROZEN FOR ONE PARENT-OPENED INDEPENDENT EXACT-REVISION REVIEW

Date: 2026-09-03 UTC

Assignment: `asg_5c8903dd-6195-4c2a-b4f7-98d79d6ffd55`

Work item: `wi_7e25614b-a42d-4125-a48d-2991121039a6`

Posture authority: `att_86e7b312-c950-4e1f-a6d8-84033ab6d91e`

Source baseline: Tightbeam main
`3e1dc56e1bd27854487228c05f4b2e1c9dd4fb22`.

Specs baseline: tightbeam-specs main
`7cac32b8675730e6cda5cdbc2fb3c29bb8e810cf`.

This targetless acceptance contract governs the main implementation first. A later 0.1.9
effective-delta port needs its own reviewed revision after the main change lands. This
revision authorizes no product-code edit, target move, landing, release, installation,
credential action, service action, adapter workaround, or live-state mutation.

## Goal

After a catalog probe reaches a final credential 401, Tightbeam must treat that exact
`{host, harness}` pair as a terminal credential incident. Tightbeam must stop every
automatic catalog probe for the pair. It must keep the existing lawful routing path free
to select another capable host. It must maintain one deduplicated standing statement that
names the affected host, harness, observed redirect destination, and required human
sign-in.

The statement must reach the org's human administrators, including `user:mike` in the
current org. Runtime readiness and doctor must render the same current statement on every
read until a post-incident credential transition and a successful catalog derivation
prove recovery.

The 2026-09-03 specimen is the controlling example. The Anthropic credential used by
Claude on `gibson` was revoked. Rotation harvest did not recover it. Claude catalog
selection on that host refused with `catalog_unavailable`. Existing placement continued
work on `racter`, but no standing notice told Mike about the lost capacity or the redirect
for days. A later human re-onboarding restored service. The contract keeps the redirect,
stops the failed probe loop, and makes both facts visible while the incident is open.

This requirement joins the mechanisms proved in:

- George issue [#9](https://github.com/clickety-clacks/tightbeam/issues/9): a subscription
  rotation can leave Tightbeam's banked copy stale; the existing recovery path harvests
  once and retries once; and
- George issue [#16](https://github.com/clickety-clacks/tightbeam/issues/16): a terminal
  credential failure can drive force re-derivation far above the catalog TTL. Mike's
  2026-09-03 comment requires backoff, continued redirect, and one standing operator
  statement.

## Non-Goals

- Do not add a proactive credential refresh, expiry, polling, retry, or backoff timer.
- Do not slow a terminal loop and call that stopped. An open incident permits no automatic
  provider probe for its catalog key.
- Do not add a Tightbeam read, reference, fingerprint, hash, comparison, repair, replace,
  or copy of the harness credential store. The pre-existing rotation-harvest attempt
  remains the only harvest in the catalog failure path. Incident and recovery state must
  not treat the harness store as authority.
- Do not add a second rotation-harvest retry or broaden current retry eligibility.
- Do not sign in, onboard, refresh, install, or mutate a credential. A human performs the
  sign-in through the existing credential lifecycle.
- Do not change any behavior before a final 401. Successful derivation, credential
  absence, credential onboarding, transient failure, stale populated catalog service,
  model selection, host ordering, and retry ownership retain their current rules.
- Do not make a timeout, connection failure, malformed response, 429, 5xx, empty
  inventory, local credential-server outage, or a rotation retry that ends in one of
  those results a terminal credential incident.
- Do not invent a host, widen an archetype's `where`, substitute for an explicit host,
  change `where=["*"]`, or otherwise expand current placement authority.
- Do not merge this incident with a turn-derived `auth-dead` incident whose current
  normal-turn-success rule can resolve it. A normal turn does not prove this catalog
  credential recovered.
- Do not add a second notice for the same open incident. Event history and per-admin
  delivery projections may be plural; their logical standing statement is one.
- Do not expose provider response bodies, bearer tokens, API keys, account identifiers,
  credential paths, credential bytes, file metadata, or credential-derived hashes.
- Do not infer an incident from old logs, old warnings, a stale cached reason, or a
  pre-upgrade failure.
- Do not change Gibson, another host, an adapter, a service, or a live database while
  implementing or verifying this contract.
- Do not start the 0.1.9 port with the main implementation. It is a later, separate,
  reviewed effective delta.

## Terms

- **Catalog key**: one exact `{host, harness}` pair. Incident, suppression, recovery, and
  redirect evidence use this key. A provider name alone is not a catalog key.
- **Probe attempt**: one provider catalog request owned by the existing ModelCatalog
  derivation path.
- **Current retry policy**: the policy that exists at the source baseline. An eligible
  local subscription 401 runs one rotation harvest and one retry. A remote probe or a
  credential kind that is not eligible receives no invented harvest retry.
- **Final 401**: the 401 returned after the current retry policy has finished. For an
  eligible local subscription, both the initial attempt and its one retry returned 401.
  For an ineligible probe, the initial 401 is final because the current policy permits no
  retry. A retry that returns a non-401 failure is not a final 401.
- **Terminal credential incident**: one durable open incident with class
  `terminal_credential_failure` for one catalog key. Its opening evidence is a final 401.
- **Opening watermark**: the greatest durable `credential-present` fact id for the
  affected host and provider that exists when the opening transition commits.
- **Credential transition**: a later durable `credential-present` fact filed by the
  existing credential lifecycle after its authorized commit. Its fact id must be greater
  than the incident's opening watermark and every recovery fact already consumed by that
  incident. It is an edge, not credential evidence and not permission to read a
  credential file.
- **Suppression**: the terminal rule that refuses to start provider I/O for an open
  catalog key. A suppressed trigger may increment one aggregate counter. It must not
  enqueue a recheck or produce one warning per call.
- **Recovery attempt**: the one catalog derivation that an eligible credential transition
  arms for an open incident. It uses the current retry policy. No clock, read, spawn, boot,
  doctor run, or ordinary force re-derivation can arm it.
- **Lawful redirect**: the existing ordered placement path selects a different capable
  host after it encounters the affected catalog key. The destination must already be in
  the request's authorized candidate set. An explicit affected host has no lawful
  redirect under this contract.
- **Redirect observation**: durable evidence that one accepted routing request encountered
  the open key and then selected another host for the same harness. It records no prompt,
  model entitlement body, or credential material.
- **Standing statement**: one logical, durable, current human-readable projection for one
  incident. It has a stable identity across administrator delivery, readiness, doctor,
  redirect updates, restarts, and publisher retries.
- **Proven recovery**: one eligible recovery attempt returned a non-empty catalog for the
  affected host and harness, and the durable resolution transition committed.

## Assumptions

1. At the source baseline, `Tightbeam.ModelCatalog` owns provider catalog I/O. Its ordinary
   reads and TTL path call `refresh_due`; its `credential_present` path can bypass TTL;
   its `refreshing` field bounds only concurrent work; and `recheck` can schedule a
   successor derive after either completion result.
2. At the source baseline, an eligible local subscription 401 calls
   `Tightbeam.Homes.sweep_auth/2` and invokes `fetch_catalog/1` once more. The combined
   `rotation_retry_failed` value preserves both results. This contract classifies that
   value as terminal only when the retry result is also 401.
3. At the source baseline, populated catalog entries can remain routable while stale.
   Once a final 401 proves the credential cannot spend, the terminal incident is stronger
   than those cached entries. This is the first behavior change in the incident path.
4. At the source baseline, multi-candidate spawn placement examines the archetype's
   authorized hosts in order and continues after a candidate refusal. An explicit host,
   a single host, and `where=["*"]` retain their existing resolution rules.
5. Host and harness identity already exist in the host registry and harness registry.
   The implementation must derive provider and sign-in command from the registered
   harness. It must not hardcode the specimen topology.
6. The durable database, condition facts, event log, and HarnessHealth incident substrate
   are available on main. The implementation may extend that substrate. It must give this
   incident its catalog-specific evidence and resolution rule.
7. Current `HarnessHealth.resolve_normal_turn_in_txn/3` resolves open health classes after
   a normal turn. It must not resolve `terminal_credential_failure`.
8. Runtime readiness already evaluates registered host-harness rows. Doctor already opens
   an existing org database read-only and distinguishes a failed check from an
   unverifiable check. Both can project durable incidents without probing an affected
   key.
9. The standing statement is an operational capacity statement. It is not a credential
   oracle. A final 401 justifies `credential rejected`; it does not always justify a
   provider-specific word such as `revoked`.
10. The spec remains targetless. The parent opens one different-session exact-revision
    review. No implementation starts until that review is reviewed-clean and the exact
    spec hash is bound by the implementation assignment.

## Invariants

### I1. The final-401 predicate is closed

The catalog derivation owner must classify exactly these results as a final 401:

1. the current retry policy does not permit a harvest retry, and the completed attempt
   returned an HTTP 401; or
2. the current retry policy ran its one harvest retry, and both the initial result and the
   retry result were HTTP 401.

The classifier must use typed status fields. It must not search provider prose for
`revoked`, `expired`, `invalid`, or another word.

A non-401 retry result keeps the complete existing degraded result and current transient
behavior. A successful retry keeps current success behavior. A result that does not match
I1 must not open this incident.

### I2. Opening is durable, atomic, and unique

The completed final-401 result must cause one serialized transition for its catalog key.
The transition must atomically:

1. insert or find the one open `terminal_credential_failure` incident for the key;
2. attach sanitized opening evidence and the opening watermark;
3. establish durable suppression;
4. establish the stable standing-statement identity;
5. file the incident assertion and lifecycle event; and
6. make the key unavailable for routing, even if its memory cache contains older entries.

The uniqueness rule is one open incident for `{host, harness,
terminal_credential_failure}`. Concurrent final results must return the same incident.
They may attach deduplicated evidence. They must not create a second open incident or
standing statement.

The ModelCatalog completion handler must discard an earlier pending `recheck` when I2
opens or finds the incident. No ordinary refresh may start between terminal
classification and suppression.

If the durable transition cannot commit, the catalog owner must not continue as healthy.
It must stop serving that key and surface an internal persistence failure. It must not
turn a failed database write into a fresh provider loop.

### I3. Suppression covers every automatic probe source

While an incident is open, suppression must win over:

- ModelCatalog startup and host enumeration;
- ordinary `get` and route reads;
- TTL expiry and refresh passes;
- credential-presence force re-derivation unless the fact passes I7;
- queued or in-flight `recheck` flags that predate the incident;
- readiness rendering;
- doctor execution;
- spawn and tune model validation; and
- process restart reconciliation.

Each source must read or receive the same durable incident state before it can start
provider I/O. Repeated suppressed sources return the same neutral incident reference.
Elapsed time alone never changes suppression.

The affected catalog must expose no routable entries while the incident is open. An
unaffected catalog key keeps its current cache, TTL, read, and force-rederive behavior.

### I4. Routing continuity preserves existing authority

An open terminal incident is one typed candidate refusal. If the existing placement path
has another authorized candidate, it must continue in the current order and may select
the first capable candidate.

The terminal incident must not:

- stop evaluation of later authorized candidates;
- remove or reorder an archetype's candidates;
- make an unauthorized host eligible;
- change the harness or model request;
- redirect an explicit host request; or
- convert an all-candidate refusal into success.

When no lawful candidate succeeds, the caller receives the current aggregate
`host_unready` or `catalog_unavailable` refusal shape, augmented only by a sanitized
incident reference where that surface already permits detail.

The same accepted routing transaction that selects an alternate must insert or find its
redirect observation. Request-idempotency replay must return the original destination
and observation. It must not count as another redirect.

### I5. One current statement tells the whole operational truth

Each open incident must have one logical standing statement with this stable content
shape:

```text
<lost-host> lost <harness>: its <provider> credential was rejected after the allowed
retry policy completed. Redirect destination: <redirect-state>. <lost-host> needs a human
sign-in for <harness>; run on <lost-host>: tightbeam onboard <provider> --as-user
<admin-user>.
```

`<redirect-state>` must be one of:

- `not yet observed; lawful alternate routing remains enabled`, when no routing request
  has yet selected an alternate; or
- the lexically sorted, comma-separated set of actual destination hosts recorded by
  redirect observations for this incident.

The statement must never claim that a globally capable destination exists. It names only
an actual lawful redirect. A failed or explicit-host request does not fabricate one.

The canonical statement has one stable identity derived from the incident id. Opening,
repeated failures, suppressed calls, destination updates, restart, and publisher replay
must update or redeliver that identity. They must not create another logical statement.
Append-only lifecycle events remain separate audit evidence.

The opening transaction must make the statement high-attention and deliverable to every
current human administrator. In the current org, that audience includes `user:mike`.
An unavailable personal session may delay transport, but it must not erase the durable
statement. Delivery is deduplicated per `{statement, administrator}`.

Readiness must render the current statement for every open incident, including when some
other harness remains runnable and the first line is `READY`. Doctor must render the same
statement before any affected-key probe. Doctor must treat an affected local harness as
failed, or as a warning when its existing overall-ready rule has another usable harness.
It must not label the final 401 `UNKNOWN` or `unverifiable`.

### I6. Records are minimal, immutable evidence

The durable incident projection may record only:

- incident id, class, state, host, harness, and derived provider name;
- opened and resolved transaction times;
- sanitized observation ids, source kinds, and principals;
- opening and consumed credential-transition fact ids;
- recovery state and sanitized outcome class;
- redirect request identity and destination host; and
- standing-statement and lifecycle-event identities.

It must not store a credential value, provider body, prompt, catalog body, model list,
account id, credential path, file timestamp, file size, inode, hash, or other value derived
from credential contents.

Incident identity, observations, transition watermarks, redirect observations, and
resolution evidence are append-only. Resolution changes the one state from open to
resolved exactly once. No path may delete or rewrite history.

Public route errors expose only the stable error code and an incident reference permitted
by existing caller authorization. Full standing and diagnostic projections require the
existing administrator or local-operator authority. Callers cannot supply the incident,
failure class, source host, destination, recovery fact, resolution, audience, or notice
identity.

### I7. Recovery requires a newer credential transition and a successful catalog

At incident open, the system stores the opening watermark without reading a credential.
Only a credential-transition fact for the affected host and derived provider whose id is
strictly greater than that watermark and every consumed recovery fact may arm a recovery
attempt.

One fact may arm at most one recovery attempt for each affected catalog key. Concurrent
consumers must claim it once. If a second newer fact arrives during an attempt, the
incident may retain only the greatest pending fact id. It may run one successor attempt
only if the first attempt does not resolve the incident.

The recovery attempt uses the same catalog derivation and current retry policy as a
healthy key. It must not read credential contents to decide whether to start.

- A non-empty successful catalog result must publish the entries and commit one durable
  resolution edge before routing can use the recovered key.
- A final 401, transient failure, or empty catalog must keep the same incident open. It
  must record one sanitized recovery outcome, consume that fact, preserve suppression,
  and wait for another newer credential transition.
- A normal turn, an administrator `resume`, a provider callback, a doctor run, a boot, a
  clock advance, or a successful catalog on another key must not resolve the incident.

Resolution must retract the incident assertion, remove the standing projection from
current readiness and doctor output, re-enable ordinary catalog refresh for the exact
key, and preserve the incident, statement, redirect, and resolution history.

### I8. Crash, restart, and migration preserve the terminal edge

On startup, the catalog owner must load open incidents before it schedules initial
refresh. It must install suppression for every open key and must not perform a recovery
probe without an eligible credential-transition fact.

A crash after I2 commits but before memory state changes must restart suppressed. A crash
before I2 commits may repeat the completed provider read once; the next final 401 must
open the incident. A crash after a recovery fact is durably claimed but before its outcome
commits leaves an outcome-unknown recovery. Startup may resume that same idempotent,
read-only recovery attempt once. It must not consume another fact or run concurrently.

Migration on main must be additive and idempotent. It must preserve every current catalog,
condition fact, event, HarnessHealth incident, readiness rule, host, session, assignment,
and notice. It must not synthesize incidents from old rows or logs. The first qualifying
post-migration final 401 opens the new incident.

The new durable rows must remain readable after a failed startup and a retry of the same
migration. A code rollback may leave the additive rows in place. Because old code cannot
honor the new suppression, operators must not run the old gateway while an open terminal
credential incident exists. Rollback instructions must require either proven recovery
under the new code or an explicit acknowledgement that the old probe-loop behavior
returns. Re-upgrade must recognize the preserved open incident before probing.

## Architecture

### A1. Classification stays with the catalog retry owner

The component that owns the current probe and rotation-harvest retry must emit one typed
final result. It applies I1 after the current policy is complete. No router, readiness
renderer, doctor formatter, or log parser may reclassify provider prose.

### A2. A catalog-specific durable incident owns suppression

Use the existing database, condition-fact, lifecycle-event, and HarnessHealth foundations
for transaction ownership and publication. Add a catalog-specific incident class or an
equivalent typed subtype whose resolution policy is I7. Do not make it eligible for the
current normal-turn-success resolver.

The durable owner exposes a side-effect-free lookup by catalog key. ModelCatalog uses the
lookup at initialization and at every refresh edge. Its in-memory terminal cache is only
an optimization; the durable row remains authority after a crash.

### A3. ModelCatalog turns the terminal result into unavailable capacity

The final-401 completion handler commits I2, clears `refreshing` and `recheck`, and replaces
the affected key's route health with a sanitized terminal-unavailable value. Existing
entries may remain in historical memory for diagnostics, but no route may consume them.

Every later ordinary trigger short-circuits before task creation. The short circuit may
update an aggregate `suppressedProbeCount` and `lastSuppressedAt` projection at a bounded
rate or transaction edge. It must not append one log or event per read.

### A4. Placement records only real redirects

The existing candidate loop remains the routing owner. When it encounters an open key, it
retains the source incident reference and continues. If it later accepts another host for
the same request and harness, the accepted routing transaction records the redirect
observation. A request that never encountered the key is ordinary placement and does not
appear in the incident.

Multiple destinations remain possible because different authorized candidate sets may
produce different results. The standing projection lists actual distinct destinations;
it does not turn them into a new routing policy.

### A5. One projection serves notice, readiness, and doctor

The incident owner derives one standing-statement view from incident and redirect rows.
The high-attention administrator delivery, runtime readiness, doctor human output, and
doctor JSON output must use that view. They must not maintain independent message text.

Doctor must open the existing org database read-only before live catalog collection. It
must exclude each open key from provider collection and render its durable terminal row.
It may continue current checks for unaffected keys. Running doctor must never claim,
retry, or resolve recovery.

Lifecycle observability must include typed events for incident opening, suppression
activation, redirect observation, recovery claim, recovery outcome, and resolution.
Every event must name the incident and catalog key and must satisfy I6.

### A6. The credential-transition production is the only re-arm edge

The existing successful credential commit continues to file `credential-present` for
`{host, provider}`. A production compares its durable fact id with each matching open
incident's watermarks. It claims an eligible fact and asks ModelCatalog for one recovery
attempt. It does not inspect the credential or call an onboarding function.

If several harnesses on one host use the provider, the fact independently arms at most
one attempt for each open catalog key. A failure on one harness does not suppress another
harness that has no open incident.

### A7. Main and 0.1.9 are serialized deliverables

The first implementation binds this exact reviewed spec to current main. It uses isolated
`/tmp` bases and recorded provider fixtures. It performs no live credential or host action.

After main lands, the owner may open one separate effective-delta spec for 0.1.9. That
revision must name the main landed commit, the 0.1.9 target tip, every necessary semantic
difference, and its own independent review. This document does not target that port.

### A8. Deletion assessment

Delete no feature, table, history, route, retry, stale-catalog rule, or diagnostic. The
new incident conditionally prevents future probe task creation for one open key. Recovery
restores the existing path. The old uncontrolled post-terminal loop has no independent
contract or caller and needs no compatibility shim.

## Acceptance

All product tests must use a holder-owned checkout, an isolated temporary base, a real
temporary database, and recorded or deterministic provider responses. They must not read
or modify a real credential, contact a provider, change Gibson, install software, start a
service, or mutate live state.

### AC1. Eligible harvest failure opens once and stops

Given an eligible local subscription catalog key with no cached entries, and an initial
probe 401, when the existing harvest runs and its one retry also returns 401, then exactly
two provider attempts occur. One open incident and one standing-statement identity exist.
Ten thousand concurrent and sequential catalog reads, TTL advances, refresh passes, and
force-rederive calls cause zero additional provider attempts.

This test must fail if a third provider attempt starts or if `recheck` remains armed.

### AC2. Retry success and non-401 outcomes do not terminalize

Given the same initial 401, when the one retry returns a non-empty catalog, then no
incident opens and current success behavior remains.

Given the same initial 401, when the retry returns a timeout, 429, 5xx, malformed result,
or empty inventory, then no terminal credential incident opens. The exact existing
degraded result remains available to its current transient handling.

### AC3. Ineligible final 401 terminalizes without a new retry

Given a catalog key for which the current retry policy permits no harvest retry, when its
probe returns 401, then one provider attempt occurs and I2 opens the incident. No harvest
or invented second attempt occurs.

Given the same key with a non-401 failure, then no terminal credential incident opens.

### AC4. Terminal state dominates stale entries

Given a populated stale catalog and a final 401, when the incident opens, then the
affected key becomes terminal-unavailable. A route cannot use its old entries. The
historical entries are not deleted or attributed to another host.

### AC5. Lawful alternate routing continues

Given an authorized ordered candidate set `[lost, alternate]`, an open incident on
`{lost, harness}`, and a capable catalog on `{alternate, harness}`, when a spawn uses that
candidate set, then placement selects `alternate` through the existing loop and records
one redirect observation.

Given an explicit `lost` request, a single-host set, or no capable later candidate, then
the current refusal returns and no unauthorized redirect or observation appears.

### AC6. The statement starts truthful and gains real destinations

Given a newly opened incident with no accepted redirect, then the canonical statement
contains the exact lost host, harness, derived provider, human sign-in remedy, and
`Redirect destination: not yet observed; lawful alternate routing remains enabled`.

When AC5 commits, then the same statement identity names `alternate`. When independent
authorized requests later select two destinations, then the same identity lists the two
distinct host names in lexical order. An idempotent replay does not add a destination or
statement.

### AC7. Mike, readiness, and doctor see the same open statement

Given `user:mike` is an administrator and the incident opens, then one high-attention
delivery projection for that statement and user exists. Publisher retry does not create
a second logical projection.

Given another harness can run, then readiness may remain `READY` and doctor may retain
its current successful exit, but both outputs contain the terminal statement as a blocked
capacity warning. Given no harness can run, readiness is `NOT READY` and doctor fails.

Doctor starts zero provider attempts for every open key and includes the incident in both
human and JSON output. Its JSON uses stable structured fields, not parsed statement text.

### AC8. Concurrency creates one incident

Given many final-401 completions for the same key race, then the real database contains
one open incident, one assertion, one standing-statement identity, and deduplicated
opening evidence. No uniqueness exception escapes and no follow-on probe starts.

Given final 401s for different hosts or harnesses, then each exact key has its own incident
and suppression state. No incident blocks an unaffected key.

### AC9. Only a newer credential transition re-arms

Given an open incident and credential-present facts at or below its opening watermark,
then replaying those facts starts no recovery attempt.

When one newer fact for the affected host and provider commits, then exactly one recovery
attempt starts for each matching open catalog key. Duplicate consumption of the same fact
starts none. A fact for another host or provider starts none.

### AC10. Recovery success clears at one observable edge

Given AC9 and a non-empty successful catalog result, when the completion handler commits,
then the entries become routable, the incident is resolved once, its assertion is
retracted, ordinary refresh is re-enabled for the key, and the standing statement no
longer appears in current readiness or doctor output.

The resolved incident, statement history, opening evidence, transition fact, catalog
outcome class, and redirect observations remain queryable by authorized diagnostics.

### AC11. Failed recovery stays suppressed

Given AC9, when recovery returns a final 401, transient failure, or empty catalog, then
the same incident remains open, the fact is consumed once, one sanitized outcome is
recorded, and suppression continues. Reads, time advances, boot, readiness, and doctor
start no next attempt. A strictly newer credential transition is required.

### AC12. A newer fact racing recovery is bounded

Given one recovery is in flight and two newer credential-transition facts race, then only
one provider task is in flight. The durable pending watermark becomes the greatest fact
id. If the first attempt succeeds, no successor runs. If it fails, at most one successor
runs for the greatest pending fact.

### AC13. Restart preserves suppression

Given an incident commit followed by a forced process or gateway crash before in-memory
publication, when the system restarts, then it loads the incident before refresh and
starts zero provider attempts for the key.

Given a forced crash before the opening commit, when the final result is observed again,
then it opens one incident. Given a crash after recovery claim but before outcome commit,
then restart resumes that one outcome-unknown recovery without a concurrent duplicate or
a new fact claim.

### AC14. Normal harness recovery cannot clear this incident

Given an open terminal catalog incident and a successful ordinary turn on the same host
and harness, when the normal-turn-success HarnessHealth path runs, then the terminal
catalog incident remains open and suppressed.

Given another health class resolves, then its resolution does not alter the terminal
catalog incident.

### AC15. Privacy and authorization remain closed

Given opening, notice, redirect, failure, recovery, and resolution records, then a scan of
the database, event details, logs, public refusals, readiness, and doctor finds none of the
fixture token, raw 401 body, catalog body, credential path, account id, file metadata, or
credential hash.

Given an ordinary unauthorized caller, then the caller cannot list or mutate full
incident state. Supplying a forged incident id, destination, fact id, resolution, notice
audience, or failure class does not change any row.

### AC16. No timer or hidden probe remains

Given an open incident and a virtual clock advanced by one year, then provider-attempt
count stays unchanged. Boot, health reads, 10,000 routes, 10,000 force-rederive calls, and
10,000 doctor/readiness evaluations also leave it unchanged.

A static call-site inventory must account for every function that can start a catalog
task. Each site must prove the durable suppression check or prove that it is the I7
recovery owner. The test must fail when a new unaccounted call site appears.

### AC17. Migration is additive and replay-safe

Given a real pre-change database fixture, when the main migration runs twice, then all old
rows and behavior remain, no terminal incident is inferred, and the second run is a no-op.
The first new qualifying final 401 opens one incident.

Given a database with an open incident, when the new code restarts after an interrupted
migration, then the migration completes idempotently and suppression precedes provider
I/O. The documented old-code rollback warning is present and exact.

### AC18. Pre-failure compatibility stays byte-for-byte where public

Given the current success, missing-credential, transient-failure, stale-populated,
explicit-host, wildcard, multi-candidate, model-selection, onboarding, readiness, and
doctor fixtures without a final 401, then existing public responses, exit decisions, host
order, retries, and provider-attempt counts remain unchanged.

### AC19. Observability is bounded and correlated

Given one full open-redirect-failed-recovery-successful-recovery lifecycle, then typed
events exist for open, suppression activation, redirect, each recovery claim/outcome, and
resolution. Each names the same incident and exact catalog key.

Repeated suppressed reads produce no per-read warning storm. Any aggregate suppression
counter is monotonic and its update rate is bounded independently of read rate.

### AC20. Repository and release gates

The main implementation must bind the reviewed SHA-256 of this exact file. It must pass
focused ModelCatalog, HarnessHealth, placement/gateway, readiness, doctor, schema, restart,
and privacy tests, followed by the repository's required Elixir and Rust gates. It must
use only isolated temporary bases.

The independent code reviewer must verify AC1-AC20 against the exact implementation
commit. A later 0.1.9 work item must present a separately reviewed effective delta. No
test or artifact from main silently satisfies that later review.

## Open Questions

None. Mike's 2026-09-03 ruling fixes the product behavior. The parent must return any
proposed change to the canonical file and repeat exact-revision review before
implementation.
