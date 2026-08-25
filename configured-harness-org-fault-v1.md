# Configured harness org fault — v1

Status: READY FOR INDEPENDENT SPEC RE-REVIEW.

Authority: `wi_8c466f03-0a44-4173-bc48-191a343a3b4e` and assignment
`asg_daf315f0-cbfc-4d94-9169-74ace5d67bda`.

Ground truth read for this draft: Tightbeam `origin/main` at `8b4a3df` and
the spec commons at `8a496f2` on 2026-08-25.

Blast-radius evidence: `art_6d46bd1c`, SHA-256
`99e317a5bde1ebb2c1a4b8894305dfd73195bcf89c3548e39eeb1651ba734212`.
Its 14 lexical card matches reduce to four current affected cards and three
distinct review obligations.

This spec extends `harness-adapter-seam-v1.md` CAP-018,
`per-host-catalogs-v1.md`, `tightbeam-credential-onboarding-v1.md`, and
`production-machine-v1.md`. It does not supersede them.

## Goal

When one credential provider used by a configured harness becomes unusable on
one or more registered hosts, Tightbeam records one loud, durable org fault for
that provider. The fault preserves each host's evidence separately, routes one
repair obligation to an authorized owner, links affected assignments, and
reports distinct review obligations without double-counting their producer and
reviewer cards. It closes only after direct recovery evidence or removal of the
affected scope.

The fault opens for any of these observed conditions on a configured
`{host, provider}` scope:

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

## Terms

- **Configured harness:** A module in `Tightbeam.Harness.all/0`. On a registered
  host, its credential provider comes only from
  `Harness.credential_provider/0`. A missing credential alone does not open this
  fault.
- **Fault provider:** The credential provider shared by the fault, such as
  `anthropic`. Provider is the org-level deduplication axis because several
  harnesses can depend on the same provider. Their grants remain independent.
- **Host scope:** One `{host, provider}` pair. A catalog or spawn observation
  also names the harness that produced it. Host scopes remain separate inside
  the shared provider fault.
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
- **Catalog state:** The result of a catalog refresh, not the rendered model
  array. Its values are `available_nonempty`, `available_empty`,
  `unavailable(reason)`, and `unknown`. Only `available_empty` opens this fault.
- **Spawn usability:** Evidence from a real session creation on the named host
  and harness, followed by one delivered first turn. Its values are `usable`,
  `unusable(reason)`, and `unknown`. Spawn usability does not classify a
  credential.
- **Signal conflict:** Current signals that point to incompatible repair paths,
  such as `malformed + CAP live`, or a catalog-empty diagnosis beside a request
  to replace the credential. Tightbeam preserves the signals and renders the
  conflict. It does not select one as truth. `valid_shape + CAP dead` is not a
  conflict: shape and authenticated liveness answer different questions.
- **Qualifying observation:** A durable observation of one of the four Goal
  conditions.
- **Fault occurrence:** One open-to-closed lifecycle for one provider. A later
  recurrence whose source cursor follows the affected scope's last recovery or
  removal cursor creates a new occurrence ID and retains the same logical
  deduplication key. A delayed observation at or before that cursor remains
  history on the closed occurrence.
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
- **Fault remediation channel:** The fault's stored summary and store-and-push
  owner message. It can name the affected host and a documented local command.
  It carries neither an authorization URL nor a carry-back code.
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
5. CAP-018 transport returns a source/run identity suitable for idempotency.
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

Each observation names its host and provider. Catalog and spawn observations
also name their harness. An observation from Gibson cannot update, clear, or
replace Eezo's current signal.

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

### I5 — Contradictions become data

Tightbeam records each contradictory signal with its source and time. It emits a
`signal_conflict` projection and keeps the fault open. It does not rewrite one
signal to agree with another.

### I6 — Remediation follows evidence

The fault renderer evaluates the following ordered table and selects the first
matching row. The conditions are mutually exclusive in this order:

| Current evidence on a host | Permitted remediation text |
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
waiver as typed input: `intent=fault_waiver`, `faultId`, `assignmentId`, and
`obligationKind=review`. When `faultId` names an active occurrence, the
transaction records or refreshes the fault impact and returns
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

Each fault, observation, impact, suppression result, owner delivery, and closure
records a cause code and the principal that produced it. Substrate-generated
records use `process:tightbeam`; agent-linked impacts retain the agent principal.

### I10 — Recovery is observed after the failure

A host scope recovers only when these observations occur after its most recent
qualifying observation. A provider-level file failure affects each configured
harness backed by that provider on the host. A catalog failure affects the
harness named by that observation.

1. credential-file health is `valid_shape`;
2. CAP-018 is `live` for each affected harness;
3. a fresh catalog refresh is `available_nonempty` for each affected harness;
   and
4. a real spawn proof is `usable` for each affected harness.

`unknown` on any required axis leaves recovery incomplete. The substrate does
not initiate the spawn proof.

### I11 — Removal is not recovery

If a host leaves `Placement.hosts/1`, or the provider no longer backs a module in
`Harness.all/0`, the reconciler marks that scope `scope_removed`. It can close
the occurrence with `scope_removed`; it cannot emit `recovered` for that scope.

### I12 — Secrets stay outside fault storage and presentation

Fault rows, observations, events, logs, notifications, API responses, fault
chat, fault artifacts, and test snapshots exclude credential bytes, token
fragments, authorization headers, refresh tokens, browser URLs, carry-back
codes, provider response bodies, local credential paths, and SSH destinations.
The local ceremony channel can display its browser URL and accept its carry-back
code without copying either value into a fault surface. Native onboarding
emissions remain governed by their own contract and do not become permitted
fault surfaces. Fault surfaces can contain host name, provider, harness, HTTP
status class, safe cause code, missing field names, source row ID, and a
SHA-256 digest of a redacted envelope.

### I13 — One mutation seam owns fault state

`Tightbeam.OrgFaults` owns fault, observation, impact, suppression, and closure
transactions. Other modules submit typed observations; they do not write the
tables directly.

## Architecture

### 1. Durable records

The implementation adds these row families:

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
- `openedPrincipal`, `closedAt`, `closeReason`, and `closedPrincipal`.

A partial unique index on `(kind, provider) WHERE state='open'` enforces I1.

`org_fault_observations`

- `id`, `faultId`, `host`, `provider`, and nullable `harness`;
- `axis` — `credential_file | credential_liveness | catalog | spawn | scope`;
- `outcome` — one value from the Terms for that axis;
- `causeCode`, `observedAt`, `sourceKind`, `sourceId`, `principal`;
- `lateAfterClose` — true only when Architecture §6 attaches a delayed source
  at or before the closed scope's terminal cursor;
- `safeDetail` — an allowlisted JSON object that satisfies I12.

The unique source index is
`(sourceKind, sourceId, host, provider, COALESCE(harness, ''), axis)` so
provider-level observations deduplicate despite SQLite's nullable-value rules.
Replaying one source is a no-op.

`org_fault_impacts`

- `faultId`, `assignmentId`, nullable `obligationKind`, nullable
  `reviewObligationKey`, `causeCode`, and `principal`;
- `firstObservedAt`, `lastObservedAt`, nullable `clearedAt`, nullable
  `clearedCauseCode`, and nullable `clearedPrincipal`.

A unique index on `(faultId, assignmentId)` makes link and clear retries
idempotent.

The active affected-assignment count joins impacts to assignments and counts
distinct assignments whose assignment state is `open` and impact `clearedAt`
is null. Closed assignments remain in history and leave the active count.
The active affected-review-obligation count applies the same filter and counts
distinct non-null `reviewObligationKey` values. Assignment prose cannot
populate either count.

### 2. Observation and recognition

The existing producers submit typed results:

- `Credentials` submits structural and expiry results;
- each CAP-018 consumer submits its authenticated liveness result and safe
  CAP-dead reason class;
- `ModelCatalog` submits the pre-projection refresh result;
- the spawn/first-turn boundary submits usability evidence.

The recognizer opens the fault only for a Goal condition. Once an occurrence is
open, it records nonqualifying axis results on an already affected host scope so
the current detail and remediation preserve contradictions. A nonqualifying
result cannot add an affected host scope. A 401, catalog timeout, spawn failure,
or `unknown` liveness can trigger a bounded CAP-018 check, but it cannot itself
become `credential_dead`.

The catalog producer must preserve the distinction between:

- provider success with zero models (`available_empty`);
- refresh failure (`unavailable(reason)`);
- cache not derived (`unknown`); and
- a client projection that happens to render `models: []`.

Recognition and fault writes run in one database transaction after a producer
submits its typed result. Before it creates an occurrence, the seam checks the
global source key and returns the earlier result for a replay. The first new
qualifying observation creates the fault and selects the owner. A concurrent
creator that loses the partial-index race selects the winning open occurrence
and appends to it in the same retry transaction.

### 3. Current signal and conflict projection

For each `{faultId, host, provider, harness, axis}`, the current signal is the
accepted observation with the greatest `(observedAt, id)`. An older late-arrival
remains in history but does not replace the current projection. The fault's
current causes are the sorted set of qualifying current outcomes across host
scopes; no precedence rule collapses them.

### 4. Loud owner routing

After the opening transaction commits, a post-commit delivery worker stores and
pushes one substrate-authored owner message. It uses deterministic delivery
identity `org-fault:<faultId>:<ownerUserId>`. The message names the occurrence ID,
provider, affected hosts, safe cause codes, affected-assignment count, and the
affected-review-obligation count. It also includes the I6 remediation lines.

A crash between the fault commit and delivery cannot lose or duplicate the
message: restart recognition sees the open fault without a delivery receipt and
retries the same identity. Repeated equal observations stay silent. Later
observations update the live summary and detail projections without sending
another owner message. Closure also updates the detail projection without
another owner message.

The owner message uses store-and-push without an inference turn. Owner delivery
does not block the fault row or any work row.

### 5. Assignment impacts and waiver suppression

The only impact-creation paths are the single explicit impact-link verb and the
typed `fault_waiver` path. A dispatch or spawn failure creates no impact by
itself. The explicit verb accepts `faultId`, `assignmentId`, a cause, and
optional `obligationKind=review`. It authorizes the assignment holder, the
assignment opener, or an admin. It returns the existing link on an idempotent
retry.

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

The explicit impact-clear verb accepts `faultId`, `assignmentId`, and a cause.
It uses the link verb's authorization rule. It sets `clearedAt`,
`clearedCauseCode`, and `clearedPrincipal` in one transaction. A retry returns
the cleared row. A later authorized link reactivates the row and derives its
classification from that link's typed input.

Each link, classification, clear, and reactivation also writes an append-only
ordinary verb event with cause and principal. Reactivation changes the current
impact projection without erasing prior transition evidence.

The typed `fault_waiver` create path calls the same impact-link transaction,
then returns the active fault. It does not mint a second intent for the owner.
The owner sees one org fault with an increasing affected-assignment count rather
than one waiver decision per card.

### 6. Recovery and stale-fault closure

After each accepted observation, the recognizer checks I10 against the most
recent qualifying observation for that host scope. When the later provider
proof and each affected harness's three later proofs exist, it appends one
idempotent `scope_recovered` observation whose source ID is the hash of the
evidence IDs.

On host-registry or harness-registry change, the reconciler appends
`scope_removed` for an affected scope that no longer exists. Boot runs the same
reconciliation for open faults, which closes stale pre-restart scopes without
inventing recovery.

The occurrence closes atomically when each host scope with a qualifying
observation has a later `scope_recovered` or `scope_removed` observation. A
recovery close uses `recovered` only when each scope recovered. A mixed or
removal-only close uses `scope_removed`.

A qualifying observation racing closure either lands before the closure check
and keeps the occurrence open, or lands after closure and compares its
`(observedAt, id)` cursor with that host scope's terminal `scope_recovered` or
`scope_removed` cursor. A later cursor creates the next fault occurrence. An
equal or earlier cursor appends to the closed occurrence as
`lateAfterClose=true`; it changes no current projection and opens no fault.

### 7. Read surfaces

`tightbeam list` and the org REST projection add `orgFaults`, containing open
summary rows with:

- fault ID, kind, provider, state, owner user ID;
- first and last observation times;
- sorted affected hosts and safe cause codes;
- signal-conflict indicator; and
- active affected-assignment count;
- active affected-review-obligation count.

A dedicated fault detail read returns the four current axes per host, source
references, safe history, linked assignments visible to the caller, deliveries,
and closure evidence. Admins and the fault owner can read the full detail.
Other authenticated users can read the org summary and assignment impacts they
already have authority to read. The response applies I12 before serialization.

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
`malformed` with the missing field names `accessToken`, `refreshToken`, and
`expiresAt`, when the observations commit concurrently, then one open Anthropic
fault exists.
Its detail shows two host scopes and preserves each signal without overwrite.

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

Given an `available_empty` fault and CAP-018 returns `unknown:timeout`, when the
fault renders and evaluates recovery, then it keeps catalog-empty as the cause,
reports liveness incomplete, and keeps the fault open. It does not recommend
browser onboarding.

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
real spawn proof returns `unusable:adapter_start_failed`, then the liveness and
catalog axes remain passing while spawn stays unusable. The renderer names the
spawn path and does not recommend onboarding. Given that failed spawn carries
an assignment ID, it creates no impact until an authorized principal calls the
explicit impact-link verb or uses the typed `fault_waiver` path.

### A9 — Observation replay and creation races deduplicate (I1, I9, I13)

Given two processes observe the first qualifying failures for one provider,
when both transactions run, then one open fault row exists and both unique
observations attach to it. When either source event replays after restart, no
second observation, owner delivery, or fault row appears.

Given an instrumented CAP-018 or catalog producer, when it submits a typed
result, then its provider I/O finishes before the `Tightbeam.OrgFaults`
transaction opens.

### A10 — First and last observation times are stable (I13)

Given accepted observations carry `observedAt` values 200, 300, then a late
100, when the detail is read, then `firstObservedAt` remains 200 for the
occurrence, `lastObservedAt` is 300, and the late observation at 100 remains in
history without becoming current.

### A11 — Current impacts exclude lexical matches and deduplicate obligations (I8)

Given the `art_6d46bd1c` census finds 14 lexical card matches, when typed impact
evidence marks four current affected cards with `obligationKind=review` and two
of those cards are the producer and reviewer for one durable
`reviewsAssignmentId`, then the summary reports `affectedAssignmentCount = 4` and
`affectedReviewObligationCount = 3`. The other ten lexical matches create no
impact rows. When the review card in the shared pair closes while its producer
remains open, the assignment count becomes 3 and the review-obligation count
remains 3. Each closed impact remains in detail history.

Given the four-card state above and one ordinary affected producer links
without `obligationKind`, when the summary recomputes, then the assignment
count becomes 5 and the review-obligation count remains 3. The impact stores a
null `reviewObligationKey`. When an authorized principal clears that ordinary
impact, the counts return to 4 and 3, and detail history retains its link and
clear causes and principals. Repeating that clear returns the same cleared row
and changes neither count.

Given an active review-marked impact, when an idempotent relink omits
`obligationKind`, then the existing marker and key remain. When a relink sends
`obligationKind=none`, then the seam returns
`impact_classification_conflict`, names the clear-then-relink remedy, and changes
neither count nor marker.

### A12 — Typed per-card waiver asks are suppressed (I8, I9)

Given an active fault and an agent submits
`intent=fault_waiver, faultId=<id>, assignmentId=<asg>,
obligationKind=review`, when the create path runs, then it returns
`org_fault_active`, records one impact with cause, principal, and the derived
review obligation key, and creates zero decision-request rows and zero
decision-request wakes. Repeating the request returns the same impact.

### A13 — Opening owner delivery is durable and later changes stay quiet (I9)

Given the earliest-created admin owns a new fault, when the opening transaction
commits, then the owner's main stream receives one store-and-push message with
the safe summary. When the same current classification repeats, no second
message appears. Given the gateway crashes after the fault commit and before
the opening delivery receipt commits, when restart reconciliation runs, then it
retries the same delivery identity and exactly one opening message exists. When
Eezo later adds `credential_file_malformed` or the occurrence closes, the live
detail changes and no additional owner message appears.

### A14 — Recovery needs the provider proof and three proofs per affected harness (I10)

Given a host's latest failure occurred at time 500 and two harnesses backed by
the provider are affected, when file-valid plus each harness's CAP-live,
fresh-nonempty-catalog, and usable-spawn observations exist at times after 500,
then the recognizer appends one `scope_recovered`. If any proof is absent,
unknown, or older than 500, it appends none.

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

### A17 — Restart reconciliation closes a stale occurrence (I11, I13)

Given the process exits after all recovery observations commit but before
closure, when the gateway restarts, then reconciliation emits the same
idempotent scope recovery and closes the existing occurrence. It creates no new
occurrence or additional owner message.

### A18 — Closure and new failure race safely (I1, I13)

Given closure at recovery cursor `(300, recovery-id)` and a qualifying
observation at cursor `(400, failure-id)` run concurrently, when both
transactions finish, then either the original occurrence remains open with the
new observation or it closes and one new occurrence opens. Given the occurrence
has closed and a delayed qualifying observation at cursor `(100, late-id)`
arrives, when recognition runs, then it appends the observation to the closed
occurrence as `lateAfterClose=true`, changes no current projection, and opens
no new occurrence.

### A19 — Read surfaces redact credential material (I12)

Given fixtures containing token-like strings, authorization headers, browser
URLs, local paths, and provider bodies, when each fault read, event, log, owner
message, chat payload, artifact, and API response serializes, then none of those
fixture strings or their substrings appears. Given the local ceremony presents
an authorization URL and accepts a carry-back code, the ceremony can use both
values while the fault surfaces still contain neither value. Given Tightbeam
0.1.8 also emits the URL through a native onboarding wake, file, or structured
output, the fault does not copy that emission, invoke onboarding, or report the
native delivery as privacy-conformant. Host, provider, harness, safe cause
codes, missing field names, and source IDs remain readable.

### A20 — CAP live plus non-empty catalog does not fake spawn proof (I3, I10)

Given file health, CAP-018, and catalog checks pass but no real spawn proof
exists, when recovery evaluates, then spawn usability stays `unknown` and the
fault remains open.

### A21 — Pattern and read surface ship together

Given the implementation build, when packaging assembles shipped guidance and
CLI help, then the operating manual contains the Architecture §8 pattern, the
CLI lists the fault summary/detail reads plus impact-link and impact-clear
verbs, and the help text uses only parser-accepted remediation commands.

## Open Questions

None. Independent review can reject a ruling; implementation does not need a
product decision to begin after review clears this draft.
