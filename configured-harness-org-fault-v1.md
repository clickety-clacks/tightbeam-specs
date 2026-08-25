# Configured harness org fault — v1

Status: READY FOR INDEPENDENT SPEC RE-REVIEW.

Authority: `wi_8c466f03-0a44-4173-bc48-191a343a3b4e` and assignment
`asg_daf315f0-cbfc-4d94-9169-74ace5d67bda`.

Ground truth read for this draft: Tightbeam `origin/main` at `8b4a3df` and
the spec commons at `21b4b81` on 2026-08-25.

Blast-radius evidence: `art_6d46bd1c`, SHA-256
`99e317a5bde1ebb2c1a4b8894305dfd73195bcf89c3548e39eeb1651ba734212`.
Its 14 lexical card matches reduce to four current affected cards and three
distinct review obligations.

This spec extends `harness-adapter-seam-v1.md` CAP-018,
`per-host-catalogs-v1.md`, `tightbeam-credential-onboarding-v1.md`, and
`production-machine-v1.md`. It also amends the closed org projection in
`rest-state-api-v1.md`, `rest-state-api-v1-wire-schema.md`, and
`event-firehose-v1.md`. It also amends the living enumeration in
`cli-surface-v1.md`. It does not supersede them.

## Goal

When one credential provider used by a configured harness becomes unusable on
one or more registered grant scopes, Tightbeam records one loud, durable org
fault for that provider. The fault preserves each grant scope's evidence, routes one
opening notification to a fixed owner, links affected assignments, and
reports distinct review obligations without double-counting their producer and
reviewer cards. It closes only after direct recovery evidence or removal of the
affected scope.

The fault opens for any of these observed conditions on a configured
`{host, harness, provider}` grant scope:

1. the provider credential file is malformed;
2. the provider credential metadata says the credential is expired;
3. CAP-018 returns `{:dead, reason}` with a credential-scoped reason classified
   as `credential_rejected` or `credential_revoked`; or
4. an authenticated catalog refresh succeeds with an empty inventory.

The org receives one active fault even when several hosts or harnesses report
the condition. The read surfaces still show each host, harness, signal, cause,
first observation, and last observation.

## Non-Goals

- This spec does not repair, copy, rotate, delete, or re-onboard a credential.
- This spec does not change or approve the onboarding ceremony's native URL
  delivery. Tightbeam 0.1.8 can emit that URL outside the terminal/browser
  interaction; the fault renderer does not conceal or cure that separate
  privacy inconsistency.
- This spec does not move a credential between hosts. Assimilation keeps one
  independent grant per `{org, host, harness}`. Provider is the fault
  aggregation key, not permission to share a grant across harnesses or hosts.
- This spec does not treat a missing credential on a fresh host, an onboarding
  lease in progress, an unsupported subscription, a transient transport error,
  or a catalog refresh timeout as this fault.
- This spec does not infer credential death from file presence, file shape, a
  catalog projection, elapsed time since the last session, a request-level 401,
  or a failed spawn.
- This spec does not choose a substitute harness, model, reviewer, or waiver.
- This spec does not parse free-text decision requests to guess whether they ask
  for a fault waiver. The typed fault-waiver path is enforceable; unmarked prose
  stays inference's responsibility.
- This spec does not auto-spawn a recovery session. A mind initiates the real
  recovery smoke; the substrate records and verifies its result.
- This spec does not add a timer that decides whether the provider recovered.
- This spec does not police arbitrary user-authored conversations or artifacts
  that originate outside `Tightbeam.OrgFaults`.

## Terms

- **Configured harness:** A module in `Tightbeam.Harness.all/0`. On a registered
  host, its credential provider comes only from
  `Harness.credential_provider/0`. A missing credential alone does not open this
  fault.
- **Fault provider:** The credential provider shared by the fault, such as
  `anthropic`. Provider is the org-level deduplication axis because several
  harnesses can depend on the same provider. Their grants remain independent.
- **Grant scope:** One `{host, harness, provider}` tuple. It represents the
  independent grant required by assimilation doctrine. Each observation names
  one grant scope. Grant scopes remain separate inside the shared provider
  fault even when they share a host and provider.
- **Credential-file health:** A structural read of the provider's local
  credential and metadata. Its values are `valid_shape`, `malformed`,
  `expired`, `missing`, and `unknown`. `valid_shape` means only that the local
  bytes and required metadata fields have the expected form.
- **Authenticated liveness:** CAP-018's real provider check, with the unchanged
  result set `:live | {:dead, reason} | {:unknown, reason}`.
- **CAP-dead reason class:** A safe classification of a CAP-018 `dead` reason.
  `credential_rejected` and `credential_revoked` are credential-scoped and
  qualify for this fault. `entitlement_denied` and `subscription_unsupported`
  are provider-access conditions and do not qualify. `unclassified_dead`
  preserves a failed liveness result without authorizing credential repair.
- **Source ordinal:** A positive integer assigned by the durable typed-source
  transaction that first records a producer result. The org allocates ordinals
  monotonically. Replays retain the original ordinal. Lifecycle ordering uses
  this ordinal, not wall-clock time or an opaque row ID.
- **Fault source kind:** One of `credential_file_check`, `cap018_check`,
  `catalog_refresh`, `spawn_first_turn`, `scope_recovery`, or `scope_removal`.
  Its `sourceId` is a producer-generated opaque typed ID that matches
  `^src_[A-Za-z0-9]+$`; callers cannot supply it as prose.
- **Impact request ID:** A caller-generated opaque ID that identifies one
  impact mutation attempt. A retry retains the ID. A later intentional link,
  clear, classification, or reactivation uses a new ID. It matches
  `^req_[A-Za-z0-9]+$`.
- **Impact transition version:** A non-negative integer on one
  `{faultId, assignmentId}` impact. An absent impact has version 0. Each
  committed mutation increments the version by one.
- **Stored liveness outcome:** The fault row stores `live`, `dead`, or
  `unknown`. A `dead` row also stores one nullable typed CAP-dead reason class;
  the other outcomes store null. Raw CAP reasons do not enter OrgFaults.
- **Catalog state:** The result of a catalog refresh, not the rendered model
  array. Its values are `available_nonempty`, `available_empty`, `unavailable`,
  and `unknown`. Only `available_empty` opens this fault.
- **Spawn usability:** Evidence from a real session creation on the named host
  and harness, followed by one delivered first turn. Its values are `usable`,
  `unusable`, and `unknown`. Spawn usability does not classify a
  credential.
- **Signal conflict:** Current signals that point to incompatible repair paths,
  such as `malformed + CAP live`, or a catalog-empty diagnosis beside a request
  to replace the credential. Tightbeam preserves the signals and renders the
  conflict. It does not select one as truth. `valid_shape + CAP dead` is not a
  conflict: shape and authenticated liveness answer different questions.
- **Qualifying observation:** A durable observation of one of the four Goal
  conditions.
- **Fault occurrence:** One open-to-closed lifecycle for one provider. A later
  qualifying source joins the active provider occurrence. If none is active, it
  creates a new occurrence ID with the same logical deduplication key. Evidence
  at or before its grant scope's latest terminal source ordinal becomes stale
  evidence and joins no occurrence.
- **Fault impact:** A durable link from an assignment to an active fault. The
  link says the assignment is affected; it does not change assignment state.
  It remains active while the assignment is open and `clearedAt` is null.
- **Review obligation marker:** Typed impact input `obligationKind=review`. A
  mind supplies this marker when the affected assignment participates in an
  independent-review obligation. The marker records its cause and principal.
- **Review obligation key:** The nullable producer assignment ID derived after
  a review obligation marker. A producer card uses its own ID. A review card
  uses its `reviewsAssignmentId`. Producer and reviewer cards can therefore
  count as two affected assignments and one review obligation. An impact
  without the marker has no review obligation key.
- **Lexical card match:** An assignment whose prose mentions a harness or
  cross-harness review. A lexical match is census evidence. It creates no fault
  impact and contributes to neither active count.
- **Fault owner:** The earliest-created admin user at the transaction that opens
  the occurrence, ordered by `(users.createdAt, users.userId)`. Admin authority
  already permits the local onboarding ceremony. The owner remains fixed for
  the occurrence.
- **Impact cause code:** A finite typed value. Link accepts
  `manual_dependency` or `fault_waiver`. Clear accepts
  `dependency_resolved`, `linked_in_error`, or `classification_reset`. The
  impact verbs accept no caller-authored text.
- **Org-fault cause code:** The finite union of `fault_opened`,
  `credential_file_malformed`, `credential_file_expired`, `credential_dead`,
  `catalog_empty`, `axis_observed`, `stale_before_terminal`,
  `manual_dependency`, `fault_waiver`, `dependency_resolved`,
  `linked_in_error`, `classification_reset`, `fault_waiver_suppressed`,
  `assignment_state_changed`, `scope_recovered`, `scope_removed`, and
  `recovered`. Each record
  type accepts only its applicable subset. No OrgFaults mutation accepts a
  caller-authored cause string.
- **Product-generated fault surface:** A fault row, observation, stale-evidence
  row, impact, transition event, delivery row, OrgFaults log, owner message,
  CLI/REST fault projection, or OrgFaults test snapshot. Each surface is built
  only from typed fields controlled by `Tightbeam.OrgFaults`.
- **Fault remediation channel:** The product-generated fault detail projection.
  It can name the affected host, harness, and a documented local command. It
  carries neither an authorization URL nor a carry-back code. The opening owner
  notification names the fault ID and provider and links to this live detail.
- **Local ceremony channel:** The interactive terminal and browser session on
  the affected host after an operator starts onboarding. This spec expects the
  authorization URL and carry-back code to stay in that channel. Tightbeam
  0.1.8 can also emit the URL through native wake, file, or structured-output
  delivery. That known contradiction remains an onboarding concern; this fault
  does not invoke the ceremony or declare its delivery conformant.

## Assumptions

1. A Tightbeam org contains at least one admin user. The cold-start user rule
   makes the first user an admin, and current product code has no user-removal or
   admin-demotion verb.
2. `Placement.hosts/1` is the authority for registered hosts.
3. `Harness.all/0` and `credential_provider/0` are the authorities for configured
   harnesses and their providers.
4. Credential-file validation can return safe structural codes without reading
   secret values into a fault row.
5. Each typed producer commits its result and one pending OrgFaults outbox row
   in the same transaction. That transaction assigns one org-monotonic source
   ordinal and stable source ID before `Tightbeam.OrgFaults` processes the
   result.
6. A catalog refresh can distinguish a successful empty response from an
   unavailable or not-yet-derived inventory before the client projection loses
   that distinction.
7. A successful recovery smoke can cite a session key and first-turn sequence.
8. The assignment relation and authorization checks can validate a fault impact
   without reading assignment prose.

If assumption 1 is falsified, fault creation records
`org_fault_owner_unavailable` as a substrate incident and refuses to fabricate
an owner. This is a product-constitution defect, not a recovered provider.

## Invariants

### I1 — One active org fault per provider

The database permits at most one open
`configured_harness_provider_unavailable` fault for a provider. Host and harness
observations attach to that occurrence; they do not create sibling faults.

### I2 — Host evidence does not collapse

Each observation names its host, harness, and provider. An observation from
Gibson cannot update, clear, or replace Eezo's current signal. An observation
from one harness cannot update, clear, or replace another harness's current
signal on the same host and provider.

### I3 — The four axes stay independent

Credential-file health, CAP-018 liveness, catalog state, and spawn usability
retain separate values and source evidence. No value on one axis implies a
value on another axis.

In particular:

- `valid_shape` does not imply CAP-018 `live`;
- CAP-018 `live` does not imply a non-empty catalog or a usable spawn;
- a non-empty catalog does not imply CAP-018 `live` because the inventory can be
  cached;
- `unusable` spawn evidence does not imply a dead credential; and
- an empty array in `tightbeam list` does not imply `available_empty`.

### I4 — CAP-018 keeps its three-state contract

Authenticated success maps to `live`. Explicit rejection or revocation maps to
`dead`. Timeout, DNS/TLS failure, 5xx, and an unrecognized response map to
`unknown`. `live` passes the liveness check, `dead` fails it, and `unknown`
leaves recovery incomplete.

The CAP-018 producer also emits one safe CAP-dead reason class from the Terms.
The liveness axis remains `dead` for each class. Only `credential_rejected` and
`credential_revoked` create the Goal's credential-dead qualifier. An
entitlement, unsupported-subscription, or unclassified dead result cannot
select onboarding remediation.

Each provider adapter normalizes a captured dead response to one safe reason
code, then applies this ordered mapping:

| Normalized reason code | CAP-dead reason class |
|---|---|
| `invalid_grant`, `invalid_token`, `expired_token` | `credential_rejected` |
| `revoked_token` | `credential_revoked` |
| `organization_disabled`, `organization_not_entitled`, `model_not_entitled` | `entitlement_denied` |
| `subscription_unsupported` | `subscription_unsupported` |
| each other dead reason code | `unclassified_dead` |

The adapter stores only the normalized code and class in the typed source row.
A new provider ships captured fixtures for each explicit mapping. Until that
mapping ships, each dead result for that provider maps to
`unclassified_dead`. The default cannot select onboarding remediation.

### I5 — Contradictions become data

Tightbeam records each contradictory signal with its source and time. It emits a
`signal_conflict` projection and keeps the fault open. It does not rewrite one
signal to agree with another.

### I6 — Remediation follows evidence

The fault renderer evaluates the following ordered table and selects the first
matching row. The conditions are mutually exclusive in this order:

| Current evidence on a grant scope | Permitted remediation text |
|---|---|
| CAP-018 `dead` with reason class `credential_rejected` or `credential_revoked` | Run the supported local `tightbeam onboard <provider> --as-user <ownerUserId>` ceremony on that host, then verify again. |
| CAP-018 `dead` with reason class `entitlement_denied` or `subscription_unsupported` | Diagnose provider entitlement or subscription support for that org, host, and harness. Do not recommend onboarding. |
| CAP-018 `dead` with reason class `unclassified_dead` | Classify the provider rejection before credential mutation. Do not recommend onboarding. |
| credential file `malformed` or `expired`, with CAP-018 `live` | Reconcile the file/source discrepancy before any credential mutation. Do not recommend onboarding. |
| catalog `available_empty`, with CAP-018 not `dead` | Diagnose the catalog refresh, harness version, and entitlement projection. If the file signal also says `malformed` or `expired`, reconcile the signal sources. Do not recommend onboarding. |
| credential file `malformed` or `expired`, with CAP-018 `unknown` | Repair that host with the supported local `tightbeam onboard <provider> --as-user <ownerUserId>` ceremony, then verify again. |
| spawn `unusable`, with CAP-018 `live` and catalog `available_nonempty` | Diagnose the adapter/spawn path. Do not recommend onboarding. |
| CAP-018 `unknown` without another permitted repair | Re-run the bounded authenticated check or diagnose its transport. Do not claim death. |

`--as-user` is a supported global flag in Tightbeam 0.1.8. The parser accepts
`tightbeam onboard anthropic --as-user mike --help`. Current command-specific
onboarding help omits the accepted flag. That omission is a help/remediation
inconsistency, not parser rejection.

The implementation makes top-level help, command-specific onboarding help, and
rendered remediation document the same global identity placement before it
ships the renderer. The renderer emits a command only when the current CLI
parser accepts that form and both help surfaces document it. A cross-half
contract test sends each rendered command through the current CLI parser and
checks both help surfaces. The fault does not describe `--as-user` as invalid or
unsupported.

The fault remediation channel tells the operator to run the ceremony in the
local ceremony channel on the named host. It does not embed the browser URL or
carry-back code. It does not invoke onboarding. It does not state that current
onboarding URL delivery satisfies the local-only expectation. It does not
suggest copying a grant from another host.

### I7 — The fault is information, not a hold

The fault does not gate a turn, assignment lifecycle, review verdict, or an
unrelated decision request. Agents decide whether to work elsewhere. The typed
fault-waiver path in I8 folds a duplicate intent into the existing fault; it is
not a gate over other decisions. The substrate records truth, routes the fault,
and verifies recovery.

### I8 — Typed fault-waiver requests deduplicate into the fault

The official decision-request create path represents a proposed per-card fault
waiver as typed input: `intent=fault_waiver`, `faultId`, `assignmentId`,
`obligationKind=review`, `requestId`, and `expectedTransitionVersion`. When
`faultId` names an active occurrence, the transaction records or refreshes the
fault impact and returns
`org_fault_active`. It creates no decision-request row and emits no
decision-request wake.

The impact seam accepts `obligationKind=review` as a typed judgment marker. For
that marker, it derives the review obligation key from durable assignment
relations. It counts current impacted assignment IDs separately. It counts
distinct non-null review obligation keys separately. An impact without that
marker changes only the assignment count. A lexical card match creates no
impact and changes neither count.

A generic free-text operator question remains available for a different user
decision. Tightbeam does not inspect that prose for hidden waiver intent. This
is the highest affordable enforcement rung: a typed affordance plus a rail over
the marker, not a classifier that guesses cognitive content (wisdom 2, 4, 6).

### I9 — Markers carry cause and principal

Each fault, observation, stale-evidence row, impact, suppression result, owner
delivery, and closure records an applicable Org-fault cause code and the
principal that produced it. `Tightbeam.OrgFaults` rejects a code outside the
finite Terms union or outside the record type's subset before it opens a write
transaction. Substrate-generated records use `process:tightbeam`; agent-linked
impacts retain the agent principal.

The applicable subsets are closed:

| Record or action | Accepted cause code |
|---|---|
| fault open; opening delivery | `fault_opened` |
| malformed file; expired metadata; qualifying CAP dead; empty catalog | `credential_file_malformed`; `credential_file_expired`; `credential_dead`; `catalog_empty`, respectively |
| accepted nonqualifying axis result | `axis_observed` |
| stale evidence | `stale_before_terminal` |
| impact link | `manual_dependency`, `fault_waiver` |
| impact clear | `dependency_resolved`, `linked_in_error`, `classification_reset` |
| typed waiver suppression event | `fault_waiver_suppressed` |
| impacted assignment closes or reopens | `assignment_state_changed` |
| grant recovery; grant removal | `scope_recovered`; `scope_removed`, respectively |
| occurrence close | `recovered`, `scope_removed` |

### I10 — Recovery is observed after the failure

A grant scope recovers only when these observations carry source ordinals
greater than its most recent qualifying observation. Credential-file, CAP-018,
catalog, and spawn evidence affect only the `{host, harness, provider}` grant
scope named by the source row.

1. credential-file health is `valid_shape`;
2. CAP-018 is `live`;
3. a fresh catalog refresh is `available_nonempty`; and
4. a real spawn proof is `usable`.

`unknown` on any required axis leaves recovery incomplete. The substrate does
not initiate the spawn proof.

### I11 — Removal is not recovery

If a host leaves `Placement.hosts/1`, a harness leaves `Harness.all/0`, or that
harness no longer names the provider, the reconciler marks the exact grant scope
`scope_removed`. Another harness on the same host and provider retains its own
scope. The reconciler can close the occurrence with `scope_removed`; it cannot
emit `recovered` for the removed scope.

### I12 — Secrets stay outside fault storage and presentation

Product-generated fault surfaces exclude credential bytes, token fragments,
authorization headers, refresh tokens, browser URLs, carry-back codes, provider
response bodies, local credential paths, and SSH destinations.
The local ceremony channel can display its browser URL and accept its carry-back
code without copying either value into a fault surface. Native onboarding
emissions remain governed by their own contract and do not become permitted
fault surfaces. The ingestion API accepts only the closed scalar columns named
in Architecture §1. It rejects an extra field, object, array, or free-text
detail before any source or fault transaction begins. Product-generated fault
surfaces can contain host, provider, harness, axis outcome, safe cause code,
source row ID, source ordinal, principal ID, assignment ID, and message ID.

### I13 — One mutation seam owns fault state

`Tightbeam.OrgFaults` owns fault, observation, impact, suppression, and closure
transactions. Other modules submit typed observations; they do not write the
tables directly.

## Architecture

### 1. Durable records

The implementation adds these row families:

`org_fault_source_outbox`

- the globally unique source key
  `(sourceKind, sourceId, host, harness, provider, axis)`;
- the org-unique positive `sourceOrdinal`;
- one closed typed outcome, nullable typed `capDeadReasonClass`, and applicable
  Org-fault cause code;
- `observedAt`, `principal`, and `state=pending | processed`; and
- nullable `processedClaimId`, present only in `processed` state.

The producer inserts this row in the transaction that durably records its
result. The row contains no free-text detail or raw provider response. A unique
index on `sourceOrdinal` enforces one ordered source result per org.

`org_fault_source_claims`

- the globally unique source key
  `(sourceKind, sourceId, host, harness, provider, axis)`;
- the org-unique positive `sourceOrdinal` assigned by the durable typed-source
  transaction; and
- `disposition=observation | stale_evidence` plus exactly one corresponding row
  ID.

The recognition transaction inserts an uncommitted claim before it inserts
either result. It then inserts exactly one result, fills the claim's disposition
and corresponding row ID, and commits both together. One source can therefore
become an accepted observation or stale evidence, but never both. A replay
returns the disposition and corresponding row ID already stored in the claim.

`org_faults`

- `id` — opaque occurrence ID;
- `dedupeKey` — `configured-harness-provider-unavailable:<provider>`;
- `kind` — `configured_harness_provider_unavailable`;
- `provider`;
- `state` — `open | closed`;
- `ownerUserId`;
- `firstObservedAt` — the `observedAt` value from the first accepted qualifying
  observation, immutable after opening;
- `lastObservedAt` — the monotonic maximum `observedAt` value among accepted
  observations;
- `openedCauseCode=fault_opened`, `openedPrincipal`, `closedAt`, nullable
  `closedCauseCode=recovered | scope_removed`, and nullable
  `closedPrincipal`.

A partial unique index on `(kind, provider) WHERE state='open'` enforces I1.

`org_fault_observations`

- `id`, `faultId`, `host`, `harness`, and `provider`;
- `axis` — `credential_file | credential_liveness | catalog | spawn | scope`;
- `outcome` — one value from the Terms for that axis;
- nullable typed `capDeadReasonClass`, present only for liveness `dead`;
- typed `causeCode`, `observedAt`, `sourceOrdinal`, `sourceKind`, `sourceId`, and
  `principal`;
- nullable `terminalSourceOrdinal`, present only for a `scope_recovered` or
  `scope_removed` outcome.

The observation references its source claim. Replaying one source is a no-op.

`org_fault_stale_evidence`

- `id`, `terminalFaultId`, `host`, `harness`, `provider`, and `axis`;
- typed `outcome`, nullable typed `capDeadReasonClass`,
  `causeCode=stale_before_terminal`, `observedAt`,
  `sourceOrdinal`, `sourceKind`, `sourceId`, and `principal`;
- `terminalSourceOrdinal`.

The stale-evidence row references its source claim. Its rows cannot join fault
current projections, affected scopes, recovery proofs, impact counts, or owner
deliveries.

`org_fault_deliveries`

- `id` — `org-fault:<faultId>:<ownerUserId>`;
- `faultId`, `ownerUserId`, `kind=opening`, `state=pending | delivered`;
- immutable `payloadVersion=1` and canonical UTF-8 `payloadBytes` encoding only
  `{faultId, provider, detailLocator="org-fault:<faultId>"}` with keys in that
  order and no optional fields;
- `causeCode=fault_opened`, `principal=process:tightbeam`, nullable
  `deliveredAt`, and nullable `deliveredMessageId`.

The fault-opening transaction inserts the immutable pending delivery row. A
unique index on `id` permits one opening delivery per owner and occurrence.
The `delivered` state, `deliveredAt`, and `deliveredMessageId` form the durable
delivery receipt; no second receipt store exists.

`org_fault_impacts`

- `faultId`, `assignmentId`, nullable `obligationKind`, nullable
  `reviewObligationKey`, typed `linkCauseCode`, and `linkPrincipal`;
- positive `transitionVersion`, `lastRequestId`;
- `firstObservedAt`, `lastObservedAt`, nullable `clearedAt`, nullable
  `clearedCauseCode`, and nullable `clearedPrincipal`.

A unique index on `(faultId, assignmentId)` permits one current impact
projection. It does not identify a mutation retry.

The active affected-assignment count joins impacts to assignments and counts
distinct assignments whose assignment state is `open` and impact `clearedAt`
is null. Closed assignments remain in history and leave the active count.
The active affected-review-obligation count applies the same filter and counts
distinct non-null `reviewObligationKey` values. Assignment prose cannot
populate either count.

`org_fault_events`

- positive org-monotonic integer `id`, `faultId`, `eventKind`, applicable
  Org-fault `causeCode`, `principal`, and `createdAt`;
- closed typed references for the source claim, impact, assignment, or
  delivery involved; and
- `requestId`, nullable `priorTransitionVersion`, nullable
  `nextTransitionVersion`, and
  nullable closed `resultCode`, `resultTransitionVersion`, `resultCleared`,
  `resultObligationKind`, and `resultReviewObligationKey` for impact events.

`resultCode` is `impact_linked`, `impact_classified`, `impact_cleared`, or
`impact_reactivated`. The remaining result columns reproduce the committed
impact result without reading the later current row. Non-impact events store
null in each result column.

A unique index on `(faultId, requestId)` identifies one impact mutation across
later transitions. Source, delivery, fault lifecycle, and waiver-suppression
events use deterministic substrate request IDs in the same index.

The seam records fault open/close, accepted observations, stale evidence,
scope recovery or removal, impact link/classify/clear/reactivate,
`fault_waiver_suppressed`, assignment-state invalidations, and delivery-state
transitions here. It accepts no free-text payload.

### 2. Observation and recognition

The existing producers submit typed results:

- `Credentials` submits structural and expiry results for one grant scope;
- each CAP-018 consumer submits its authenticated liveness result and safe
  normalized reason code for one grant scope;
- `ModelCatalog` submits the pre-projection refresh result for one grant scope;
- the spawn/first-turn boundary submits usability evidence for one grant scope.

Each producer result carries its durable source ordinal. The CAP-018 adapter
maps its normalized reason code through I4 before the producer transaction
creates the outbox row. The producer validates the closed scalar payload before
that transaction begins.

The recognizer opens the fault only for a Goal condition. Once an occurrence is
open, it records nonqualifying axis results on an already affected grant scope
so the current detail and remediation preserve contradictions. A nonqualifying
result cannot add an affected grant scope. A 401, catalog timeout, spawn
failure, or `unknown` liveness can trigger a bounded CAP-018 check, but it cannot
itself become `credential_dead`.

The catalog producer must preserve the distinction between:

- provider success with zero models (`available_empty`);
- refresh failure (`unavailable`);
- cache not derived (`unknown`); and
- a client projection that happens to render `models: []`.

One post-commit consumer scans pending outbox rows in source-ordinal order.
Gateway boot starts the same scan before it reports OrgFaults readiness. The
consumer performs recognition, inserts or reuses the global source claim, and
marks the outbox row `processed` with `processedClaimId` in one database
transaction. A crash before that commit leaves the row pending. A crash after
that commit leaves the row processed. Two consumers racing one row converge on
the unique source claim and the processed row.

Inside that transaction, the seam first claims the global source key or returns
its earlier disposition for a replay. Before it selects an open
occurrence, it reads the greatest terminal source ordinal for the exact grant
scope across closed occurrences. A qualifying source ordinal at or below that
watermark creates one `org_fault_stale_evidence` row and returns without
selecting an occurrence. A greater qualifying source selects the active provider
occurrence or creates one and selects the owner when none is active. A
concurrent creator that loses the partial-index race selects the winning open
occurrence and appends to it in the same retry transaction.

### 3. Current signal and conflict projection

For each `{faultId, host, harness, provider, axis}`, the current signal is the
accepted observation with the greatest source ordinal. `observedAt` is a display
timestamp and does not order lifecycle state. A source with a lower ordinal
remains in history but does not replace the current projection. The fault's
current causes are the sorted set of qualifying current outcomes across grant
scopes; no precedence rule collapses them.

### 4. Loud owner routing

The opening transaction inserts the frozen pending delivery row from
Architecture §1. Its canonical `payloadBytes` contain only the occurrence ID,
provider, and stable detail locator. They contain no host set, cause set, impact
count, or remediation snapshot.

After commit, a delivery worker calls idempotent store-and-push with the row ID
and frozen payload. On success or an already-delivered response for that ID, a
second transaction marks the row `delivered` and stores the returned message
ID. A crash before push leaves `pending`. A crash after push but before the
receipt transaction retries the same store-and-push ID and receives the same
message before marking the receipt. Repeated observations and later changes
create no owner delivery. Live detail supplies current grant scopes, causes,
counts, and I6 remediation.

The owner notification uses no inference turn and blocks neither the fault row
nor a work row.

### 5. Assignment impacts and waiver suppression

The only impact-creation paths are the single explicit impact-link verb and the
typed `fault_waiver` path. A dispatch or spawn failure creates no impact by
itself. The explicit verb accepts `faultId`, `assignmentId`,
`linkCauseCode=manual_dependency | fault_waiver`, and optional
`obligationKind=review`, plus required `requestId` and
`expectedTransitionVersion`. It authorizes the assignment holder, the
assignment opener, or an admin. It rejects another cause code before its
transaction.

The CLI form is `tightbeam org-fault impact-link <faultId> <assignmentId>
--request-id <req> --expected-version <n> --cause
<manual_dependency|fault_waiver> [--obligation review]`. The rendered shell
command is one line; this wrapping is prose layout only.

When `obligationKind=review`, the impact-link transaction derives
`reviewObligationKey` from durable assignment relations. It uses
`reviewsAssignmentId` for a review card and the assignment's own ID for a
producer card. When the marker is absent, it stores a null key. The transaction
rejects another obligation kind. It does not read assignment prose.

An active relink with an omitted marker preserves the current classification.
An active relink can add `obligationKind=review` to a null classification. It
cannot remove that marker. The seam returns `impact_classification_conflict`
with the remedy `clear the impact, then relink it with the intended marker` when
an active relink requests removal or another classification.

The explicit impact-clear verb accepts `faultId`, `assignmentId`, and
`clearCauseCode=dependency_resolved | linked_in_error |
classification_reset`, plus required `requestId` and
`expectedTransitionVersion`. It uses the link verb's authorization rule. It
rejects another cause code before its transaction. It sets `clearedAt`,
`clearedCauseCode`, and `clearedPrincipal` in one transaction. A retry returns
the cleared row. A later authorized link reactivates the row and derives its
classification from that link's typed input.

The CLI form is `tightbeam org-fault impact-clear <faultId> <assignmentId>
--request-id <req> --expected-version <n> --cause
<dependency_resolved|linked_in_error|classification_reset>`. The rendered
shell command is one line; this wrapping is prose layout only.

Each impact mutation first looks up `(faultId, requestId)`. An existing event
returns its stored typed result without reading or changing the current impact.
A new request compares `expectedTransitionVersion` with the current version;
an absent row has version 0. A mismatch returns
`impact_transition_conflict` with the current version and writes nothing. A
match commits the impact change, increments the version by one, and records the
event and result under the request ID in the same transaction.

Each link, classification, clear, and reactivation also writes an append-only
ordinary verb event with cause and principal. Reactivation changes the current
impact projection without erasing prior transition evidence.

An assignment close or reopen transaction calls the OrgFaults mutation seam
for each linked fault before commit. The seam writes one invalidation event with
cause `assignment_state_changed` and deterministic request ID
`assignment-state:<assignmentId>:<assignmentRowVersion>:<faultId>`. It does not
change the impact transition version. A replay of the same assignment version
returns the event. The post-commit `org_fault.changed` notice makes both active
counts refreshable.

The typed `fault_waiver` create path calls the same versioned impact-link
transaction. In that transaction it records the impact event under the caller's
request ID and the suppression event under deterministic request ID
`waiver-suppressed:<requestId>`, then returns the active fault. It does not mint
a second intent for the owner.
The owner sees one org fault with an increasing affected-assignment count rather
than one waiver decision per card.

### 6. Recovery and stale-fault closure

After each accepted observation, the recognizer checks I10 against the most
recent qualifying source ordinal for that grant scope. When the four later
proofs exist, it appends one idempotent `scope_recovered` observation whose
source ID is `src_` followed by the hash of the evidence IDs and whose
`terminalSourceOrdinal` is their least source ordinal. The least ordinal is the
recovery coverage boundary: all four cited proofs follow any qualifying source
at or below that boundary.

On host-registry, harness-registry, or harness-provider mapping change, the
reconciler appends `scope_removed` for each exact affected grant scope that no
longer exists. For each removed grant, the durable source seam creates one
derived result with a deterministic source ID and a newly allocated source
ordinal; that ordinal is also its terminal source ordinal. Boot runs the same
reconciliation for open faults, which closes stale pre-restart scopes without
inventing recovery.

The occurrence closes atomically when each grant scope with a qualifying
observation has a `scope_recovered` or `scope_removed` whose
`terminalSourceOrdinal` is greater than the scope's greatest qualifying source
ordinal. The lifecycle does not use the derived scope observation's own source
ordinal as proof freshness. A recovery close uses `recovered` only
when each scope recovered. A mixed or removal-only close uses `scope_removed`.

A qualifying source racing closure either lands before the closure check and
keeps the occurrence open, or lands after closure and enters the recognition
ordering above. Recognition compares its source ordinal with the exact grant
scope's greatest terminal source ordinal before it selects any active provider
occurrence. A greater ordinal joins the active occurrence or creates the next
one. An equal or lower ordinal creates stale evidence and joins no occurrence.
When a greater ordinal joins an open occurrence after a prior recovery row, the
recognizer re-evaluates the four axes against that failure and writes a new
recovery row only from four proofs whose ordinals each exceed it.

### 7. Read surfaces

The canonical field order, types, nullability, enum domains, and array ordering
for `/api/org` summaries and `GET /api/org-faults/:faultId` live only in
`rest-state-api-v1.md` R2/R7/R9/AU4 and its wire-schema companion. This spec
does not define a second wire shape. `tightbeam list` exposes the canonical
`orgFaults` array inside its org value; it does not recompute one.

The detail route returns the four current axes per grant scope, typed source
history, stale evidence, impacts, deliveries, and closure evidence in that
canonical shape. The fault owner and an admin can read it. Another principal
receives the REST contract's same 404 for unknown and forbidden detail. That
principal can still read assignment impacts through the existing assignment
resource when its assignment grant permits the read.

Each new `org_fault_events` commit emits the canonical
`org_fault.changed` source-invalidation notice. REST R9 lists that class for
both org and org-fault detail. An authorized cached client refetches the view;
an idempotency replay that creates no event emits no notice.

The CLI detail verb is exactly `tightbeam org-fault show <faultId>`. The list
summary remains inside `tightbeam list`. No additional summary verb ships.

The boot readiness prose may link to the active fault ID, but readiness remains
a projection. It does not open, update, or close fault rows.

### 8. Operating pattern taught to agents

The implementation amends the operating manual in the same product change:

> One active org fault is the shared blockage identity. Link affected work to
> it. Do not ask for the same provider failure one assignment at a time.

This is the only new agent pattern. The manual points to the fault read and the
typed impact-link path. It does not teach agents to diagnose credentials from
`list` or `doctor` prose.

### 9. Subtraction ruling

ADD wins because deleting the configured provider would remove required review
capacity, while accepting per-card waivers is the observed six-day erosion of
that requirement; the added mechanism stores one neutral fault and deletes the
repeated decision surface. A separate adjudicator, hold, retry ladder, or
credential repair engine loses because the substrate must not decide or repair
(wisdom 6–10).

## Acceptance

### A1 — One fault aggregates divergent hosts (I1, I2, I3)

Given Anthropic backs a configured harness on Gibson and Eezo, Gibson reports
`valid_shape` while CAP-018 reports `dead:credential_rejected`, and Eezo reports
`malformed`, when the observations commit concurrently, then one open Anthropic
fault exists.
Its detail shows two grant scopes and preserves each signal without overwrite.

### A2 — Healthy file does not pass authenticated liveness (I3, I4)

Given credential-file validation returns `valid_shape`, when CAP-018 returns
`{:dead, :revoked}`, then the host shows file `valid_shape` and liveness `dead`.
The fault opens with `credential_dead`; no read reports the credential live.

### A3 — CAP-018 mapping remains exact (I4)

Given recorded real CAP-018 transport fixtures, when the harness maps an
authenticated success, explicit rejection, timeout, DNS failure, 5xx, and an
unknown response, then the outcomes are respectively `live`, `dead`, `unknown`,
`unknown`, `unknown`, and `unknown`. Only `dead` fails liveness. Each `unknown`
leaves recovery incomplete. The explicit credential rejection carries reason
class `credential_rejected`; an entitlement-denial fixture remains `dead` but
carries reason class `entitlement_denied` and does not qualify by itself.

Given each explicit normalized reason code in I4 and one unmatched dead reason
code, when every supported provider adapter maps the fixtures, then each
explicit code maps to its table class and the unmatched code maps to
`unclassified_dead`. Given a provider has no captured mapping, when it returns
any dead result, then the result maps to `unclassified_dead` and the renderer
prints no onboarding command.

### A4 — Empty projection is not an empty refresh (I3)

Given `tightbeam list` renders `models: []` because the catalog is unavailable
or not derived, when the detector evaluates the event, then it does not record
`catalog_empty`. Given an authenticated refresh succeeds with zero models, it
records `available_empty` and opens or updates the provider fault.

### A5 — Empty catalog does not prescribe re-onboarding (I5, I6)

Given credential-file health is `valid_shape`, CAP-018 is `live`, and the
catalog refresh is `available_empty`, when the fault renders, then it preserves
live liveness beside the empty catalog and reports the catalog diagnosis. Given
the file instead reports `malformed`, it also reports a signal conflict and
requires source reconciliation. Neither case prints an onboarding command,
browser URL, or credential-copy instruction.

### A6 — Unknown does not become dead (I4, I6)

Given an `available_empty` fault and CAP-018 returns `{:unknown, :timeout}`, when
the adapter stores liveness `unknown` and the fault renders and evaluates
recovery, then it keeps catalog-empty as the cause, reports liveness incomplete,
and keeps the fault open. It does not recommend browser onboarding.

### A7 — Malformed and expired remain distinct (I3, I6)

Given one host reports `malformed` and another reports `expired`, with neither
host holding CAP-018 `live`, when the fault renders, then the host rows keep the
two cause codes. Each local remediation uses a command accepted by the current
CLI parser and documented by top-level and command-specific help. Given the
0.1.8 parser accepts global `--as-user` while command-specific onboarding help
omits it, the help/remediation contract test fails until that help documents the
accepted placement. After the help correction, the renderer emits
`tightbeam onboard <provider> --as-user <ownerUserId>`. The parser accepts the
command, both help surfaces document it, the fault does not call `--as-user`
invalid or unsupported, and the text contains no cross-host copy instruction.

Given CAP-018 returns `dead:entitlement_denied` beside an expired file, when the
fault renders, then liveness remains failed and the renderer diagnoses
entitlement without printing an onboarding command. Given CAP-018 returns only
`dead:subscription_unsupported` and no other Goal condition exists, recognition
opens no configured-harness provider fault. Given CAP-018 returns
`dead:unclassified_dead` beside an open catalog-empty fault, the renderer asks
for cause classification and prints no onboarding command.

### A8 — Spawn usability remains independent (I3)

Given CAP-018 is `live` and a fresh catalog is `available_nonempty`, when the
real spawn proof maps an adapter-start failure to `unusable`, then the liveness
and catalog axes remain passing while spawn stays unusable. The raw adapter
reason does not enter OrgFaults. The renderer names the spawn path and does not
recommend onboarding. Given that failed spawn carries an assignment ID, it
creates no impact until an authorized principal calls the explicit impact-link
verb or uses the typed `fault_waiver` path.

### A9 — Observation replay and creation races deduplicate (I1, I9, I13)

Given two processes observe the first qualifying failures for one provider,
when both transactions run, then one open fault row exists and both unique
observations attach to it. When either source event replays after restart, no
second source claim, observation, stale-evidence row, owner delivery, or fault
row appears.

Given an instrumented CAP-018 or catalog producer, when it submits a typed
result, then its provider I/O finishes before the `Tightbeam.OrgFaults`
transaction opens. Its durable source transaction has already assigned one
org-unique source ordinal and source ID and inserted one pending outbox row. A
replay retains both values.

Given a qualifying catalog-empty source and pending outbox row commit, when the
process exits before recognition begins and the gateway restarts, then the boot
consumer recognizes that row, opens or updates one fault, and marks the outbox
row processed in the same transaction as its source claim. Crashes before that
transaction commits leave the row pending; crashes after it commits create no
second claim or observation.

### A10 — First and last observation times are stable (I13)

Given accepted observations carry `(sourceOrdinal, observedAt)` values
`(1, 200)`, `(3, 300)`, then `(2, 100)`, when the detail is read, then
`firstObservedAt` remains 200, `lastObservedAt` is 300, and the ordinal-2
observation remains in history without becoming current. The ordinal-3
observation is current even though lifecycle processing received ordinal 2
last.

### A11 — Current impacts exclude lexical matches and deduplicate obligations (I8)

Given the `art_6d46bd1c` census finds 14 lexical card matches, when typed impact
evidence links four current affected cards with
`linkCauseCode=manual_dependency, obligationKind=review` and two of those cards
are the producer and reviewer for one durable
`reviewsAssignmentId`, then the summary reports `affectedAssignmentCount = 4` and
`affectedReviewObligationCount = 3`. The other ten lexical matches create no
impact rows. When the review card in the shared pair closes while its producer
remains open, the assignment count becomes 3 and the review-obligation count
remains 3. Each closed impact remains in detail history.

Given the four-card state above and one ordinary affected producer links
with `requestId=req_link1`, `expectedTransitionVersion=0`,
`linkCauseCode=manual_dependency`, and no `obligationKind`, when the summary
recomputes, then the assignment count becomes 5 and the
review-obligation count remains 3. The impact stores a null
`reviewObligationKey`. When an authorized principal clears that ordinary impact
with `requestId=req_clear1`, `expectedTransitionVersion=1`, and
`clearCauseCode=dependency_resolved`, the counts return to 4 and 3, and detail
history retains its typed link and clear causes and principals. Repeating
`req_clear1` returns its stored result and changes neither count nor version.

Given `req_link1` succeeded but its response was lost, and `req_clear1` then
cleared the impact at version 2, when delayed `req_link1` retries with expected
version 0, then it returns the original link result and does not reactivate the
impact.
Given a new `req_link2` request still expects version 1, when it runs against
version 2, then it returns `impact_transition_conflict` with current version 2
and writes nothing. A new `req_link3` with expected version 2 reactivates the
impact at version 3. A delayed retry of `req_clear1` returns its stored result
and does not clear version 3.

Given an active review-marked impact at version 1, when a new request with
expected version 1 omits `obligationKind`, then the existing marker and key
remain and the transition reaches version 2. When another new request at
expected version 2 sends `obligationKind=none`, then the seam returns
`impact_classification_conflict`, names the clear-then-relink remedy, and changes
neither count nor marker.

Given an impact link or clear supplies a caller-authored sentence, URL, token,
path, provider body, or an unrecognized cause code in place of its typed cause,
when ingestion validates the request, then it rejects the request before a
transaction and writes no source claim, impact, event, log, or delivery.

### A12 — Typed per-card waiver asks are suppressed (I8, I9)

Given an active fault and an agent submits
`intent=fault_waiver, faultId=<id>, assignmentId=<asg>,
obligationKind=review, requestId=req_waiver1,
expectedTransitionVersion=0`, when the create path runs, then it returns
`org_fault_active`, records one impact with
`linkCauseCode=fault_waiver`, the agent principal, and the derived review
obligation key, and creates zero decision-request rows and zero decision-request
wakes. Repeating `req_waiver1` after an authorized clear returns its original
stored result and does not reactivate the impact.

### A13 — Opening owner delivery is durable and later changes stay quiet (I9)

Given the earliest-created admin owns a new fault, when the opening transaction
commits, then it also commits one pending delivery row whose immutable v1
canonical UTF-8 payload bytes encode only the fault ID, provider, and
`detailLocator="org-fault:<faultId>"` in the Architecture §1 key order. The
payload contains no host set, cause set, counts, remediation, browser URL, or
credential data.

Given a second grant scope and an impact commit before the delivery worker runs,
when the worker sends the opening message, then its bytes equal the frozen
payload and the live detail shows the later scope and impact. Given a crash
before store-and-push, when the worker retries, then one message and one
delivered receipt exist. Given a crash after store-and-push succeeds but before
the receipt transaction, when the worker retries the same delivery ID, then
store-and-push returns the original message ID and one message and one delivered
receipt exist. Repeated observations, later impacts, and closure create no
additional owner message.

### A14 — Recovery needs four later proofs per affected grant scope (I10)

Given one grant scope's latest qualifying failure has source ordinal 500 and a
second harness on the same host and provider has its own affected grant scope,
when file-valid, CAP-live, fresh-nonempty-catalog, and usable-spawn observations
for the first grant all have source ordinals greater than 500, then the
recognizer appends one `scope_recovered` for the first grant only and stores the
least of the four proof ordinals as its terminal source ordinal. If one proof
is absent, unknown, belongs to the second grant, or has an ordinal at or below
500, it appends no recovery for the first grant.

Given failure 100 and recovery proofs at 110, 120, 130, and 200, when recovery
evaluates, then its terminal source ordinal is 110. When a delayed qualifying
failure at 150 arrives, then the old recovery does not cover that failure and
the occurrence stays open until four proofs with ordinals greater than 150
exist.

### A15 — Multi-host recovery closes only after the last scope (I10)

Given Gibson and Eezo share one fault, when Gibson satisfies A14, then the fault
remains open with Eezo affected. When Eezo later satisfies A14, then the fault
closes as `recovered`; the detail shows the closure and the opening owner
delivery remains the only owner message for that occurrence.

### A16 — Removed scope closes honestly (I11)

Given a fault affects only Eezo, when Eezo is removed from the registered-host
authority and reconciliation runs, then the scope receives `scope_removed` and
the fault closes with `scope_removed`. No recovery or successful spawn is
claimed.

Given two harness grants on Eezo share the provider and both affect one open
fault, when only one harness leaves `Harness.all/0` or stops naming the provider,
then only that exact grant receives `scope_removed`. The other grant remains
affected, and the occurrence remains open until that grant recovers or is
removed.

### A17 — Restart reconciliation closes a stale occurrence (I11, I13)

Given the process exits after all recovery observations commit but before
closure, when the gateway restarts, then reconciliation emits the same
idempotent scope recovery and closes the existing occurrence. It creates no new
occurrence or additional owner message.

### A18 — Closure and new failure race safely (I1, I13)

Given occurrence 1 contains grant A and closes with terminal source ordinal 300,
while occurrence 2 for the provider is open because grant B has source ordinal
500, when a delayed qualifying source for grant A with ordinal 100 arrives,
then recognition writes one stale-evidence row linked to occurrence 1 and does
not attach it to occurrence 2. When a qualifying source for grant A with
ordinal 600 arrives, then it joins occurrence 2.

Given recovery for a grant at source ordinal 300 and its qualifying failure at
source ordinal 400 run concurrently, when both transactions finish, then either
the original occurrence remains open with the failure or it closes and the
failure joins or creates the next active provider occurrence. The result does
not depend on `observedAt` or opaque row-ID ordering. Replaying any source in
these cases returns its original accepted-or-stale disposition.

Given a closed occurrence whose four recovery proofs have ordinals 110, 120,
130, and 200, when a delayed failure at ordinal 150 arrives, then recognition
compares it with terminal boundary 110 and creates or joins the next occurrence.
It does not record stale evidence for that failure.

### A19 — Read surfaces redact credential material (I12)

Given fixtures containing token-like strings, authorization headers, browser
URLs, local paths, provider bodies, an extra field, an object, and an array,
when a producer or impact caller submits each fixture outside the closed
Architecture §1 scalar columns, then ingestion rejects it before the producer
source or fault transaction and writes no outbox, claim, fault, observation, impact,
event, log, or delivery. Given valid typed rows, when each product-generated
fault read, event, log, owner message, delivery, projection, and OrgFaults test
snapshot serializes, then it contains only the closed row and wire fields.

Given the local ceremony presents an authorization URL and accepts a carry-back
code, when that separate ceremony runs, then it can use both values while the
fault surfaces contain neither. Given Tightbeam 0.1.8 also emits the URL through
a native onboarding wake, file, or structured output, the fault does not copy
that emission, invoke onboarding, or report the native delivery as
privacy-conformant. This acceptance does not claim control of arbitrary
user-authored conversations or artifacts outside `Tightbeam.OrgFaults`. Host,
provider, harness, safe cause codes, and source IDs remain readable.

### A20 — CAP live plus non-empty catalog does not fake spawn proof (I3, I10)

Given file health, CAP-018, and catalog checks pass but no real spawn proof
exists, when recovery evaluates, then spawn usability stays `unknown` and the
fault remains open.

### A21 — Pattern and read surface ship together

Given the implementation build, when packaging assembles shipped guidance and
CLI help, then the operating manual contains the Architecture §8 pattern, the
CLI lists `tightbeam org-fault show`, `tightbeam org-fault impact-link`, and
`tightbeam org-fault impact-clear` with the Architecture §5 required flags,
and the help text uses only parser-accepted remediation
commands. The same build's canonical REST R2/R7/R9, wire schema, and firehose
R4c/R8b rows contain the org summary, detail resource,
`org_fault.changed` invalidation, visibility, and dependency-vector contracts.

## Open Questions

None. Independent review can reject a ruling; implementation does not need a
product decision to begin after review clears this draft.
