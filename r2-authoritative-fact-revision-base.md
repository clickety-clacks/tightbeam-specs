# R2 authoritative fact and revision base

Status: REVIEW CANDIDATE — IMPLEMENTATION NOT AUTHORIZED

Date: 2026-08-27 PT

Assignment: `asg_8d329203-251e-4204-8ae6-54ca651e89e8`

Work item: `wi_c01e8f20-3f77-434f-a124-f006278c4ff6`

## Spec identity and authority

The canonical identity is
`tightbeam-specs/r2-authoritative-fact-revision-base.md`. Each review and handoff must
bind this file by its SHA-256 digest and containing commit.

Operator decision `dr_99628605-cb7a-44b4-a509-d46b8e7f4ffd` selected
`commission_r2_fact_base`. This specification supplies that separate base.

The consumer is exact reviewed composition specification `art_6d4c9985`, commit
`344ac913382d768af8bdeff0bdabf226009d7cb7`, SHA-256
`d24bd92d60203e17137870b275ef766c4e67c10e0368d747df5bd90dad9a9fa7`, reviewed-clean
in `att_66d3f0e9-df19-4aae-9a0b-44362ba6b2a4`. The reviewed F7 predecessor is
`art_9ee43d58`, commit `da969ebe2f44258338ec4e60792fa1171689cd3b`, SHA-256
`e98c898f9bda0cef462e4a4d0bd9a0e10eff6cb810f9299f4fe7b7955694f2ef`, reviewed-clean
in `att_43f3bd21-bd5c-48b0-802a-981c6998f0dc`.

This file does not amend either consumer. It preserves F7 R1-R8 and A1-A7 as reviewed.
It also preserves `art_6d4c9985`'s implementation gate: no product implementation,
exact-tip code review, migration, release, deployment, runtime mutation, credential
access, or live wake action is authorized until this base passes independent review and
the composition specification incorporates its exact objects, owners, and transitions.

## Goal

Tightbeam must hold durable, typed local state from which the R2 consumer can construct
each execution token and authoritative inability fact in one database transaction.

A committed source transition must make older evidence fail exact matching. This rule
applies when a source changes to a different value and when a new source event repeats
the same value.

The read seam must return either one internally consistent snapshot or a named failure.
It must not combine fields from different committed revisions.

## Non-Goals

- This base does not decide when product policy places or releases a session hold, opens
  or closes a circuit, changes an adapter or catalog state, selects a credential, or
  classifies a quota window.
- This base does not call a provider, adapter, ACP endpoint, harness process, credential
  service, or remote host to obtain a fact.
- This base does not predict quota exhaustion, infer state from elapsed failure counts,
  or parse provider prose, error prose, prompts, role labels, or prior failed turns.
- This base does not add a wake path, terminal path, sender-notice path, retry scheduler,
  alternate target, target alias, rerouting rule, or sibling-registry alias.
- This base does not change F7's precondition order, match keys, refusal response,
  accepted-wake lifecycle, authorization, migration conflict, or schema successor.
- This base does not define a public hold, circuit, catalog, credential, quota, or fact
  mutation verb.
- This base does not cover release-line `0.1.x` work.

## Terms

- **R2 consumer**: the exact R2 clauses in reviewed F7 and in `art_6d4c9985`. They define
  eight fact kinds and their complete match keys.
- **Execution selection**: the exact tuple
  `{sessionKey, sessionUpdatedAt, host, harness, provider, modelFamily, modelContext,
  effort}` read from the current session row. Null `modelContext` and null `effort` are
  values, not wildcards.
- **Adapter harness ID**: the adapter key's `harnessId`. It is the exact stored UTF-8
  value of the execution selection's `harness`; the two names do not introduce a
  mapping or alias.
- **Source event**: one typed local event accepted from a named source owner. It carries
  a `sourceEventId` of 1 through 512 UTF-8 bytes, a typed cause, an authenticated actor
  principal, and an observation time. A source event contains no fact ID, fact kind,
  match key, revision, or writer principal supplied by a caller.
- **Canonical source payload**: the deterministic CBOR map
  `{naturalKey, causeKind, actorPrincipal, observedAt, typedInputState}`. It excludes the
  source event ID and every R2-derived ID, revision, writer principal, fact field, and
  fact expiry. `typedInputState` includes the source hold or quota boundary from which
  `R2Facts` derives fact expiry. Each member uses the Fact ID encoding rules below. A
  catalog entry set is an array ordered by the canonical CBOR bytes of
  `{modelFamily,modelContext,effort}`; duplicate tuples are invalid.
- **Replay**: a second submission with the same
  `{sourceOwner, registryKind, sourceEventId}` and byte-equal canonical typed payload. A
  replay returns the first committed result and changes no row. The same identifier with
  a different payload returns `r2_source_event_conflict` and changes no row.
- **Same-value transition**: a source event with a new `sourceEventId` whose typed state
  equals the current typed state. It is a new observation and advances the registry
  revision.
- **Registry entity ID**: an opaque ID created once by the R2 mutation seam. Its format
  is the registry prefix in this specification followed by 32 lowercase hexadecimal
  characters. Tightbeam does not derive it from a host, harness, provider, credential,
  account, or quota value. It remains unchanged for that entity and is not reused.
- **Revision**: a positive 64-bit integer. Creation writes revision `1`. Each later
  committed source event for that entity writes the prior revision plus one. A replay,
  rejected mutation, validation pass, database restart, or rolled-back transaction does
  not advance it.
- **Transition ID**: `r2t_` followed by the lowercase SHA-256 digest of the canonical
  tuple
  `{registryKind, entityId, version, sourceOwner, sourceEventId, payloadDigest}`.
  `version` is `sessionUpdatedAt` for a session-execution event and the registry
  revision for another event. The source identity and payload digest prevent a restored
  database from reusing an old transition ID when a different new event later occupies
  the same revision. The tuple uses the Fact ID canonical CBOR rules below.
- **Adapter token**: the reviewed tuple
  `{{harnessId, "shared", host}, adapterGeneration, adapterRevision}`. Both revisions
  are positive 64-bit integers. Creation initializes both to `1`. A new registered
  adapter process advances both integers. A later event for that generation advances
  only `adapterRevision`.
- **Harness-catalog token**: the reviewed tuple
  `{host, harness, provider, catalogRevision}`.
- **Credential token**: the reviewed tuple
  `{host, harness, provider, credentialSlotId, credentialRevision}`.
  `credentialSlotId` is opaque and never exposes credential material or an account ID.
- **Hold token**: `{holdId, holdRevision}` for the one active hold on an exact session.
- **Circuit token**: `{circuitId, circuitRevision}` for the one circuit associated with
  an adapter registry entity.
- **Quota token**: `{quotaWindowId, quotaWindowRevision}` for one exact bounded quota
  window observed for one exact credential token.
- **Ordinary execution observation**: a typed local quota signal linked by positive
  `sourceTurnSeq` to a carrier turn that Gateway admitted and the existing turn
  lifecycle recorded. A standalone health check, catalog request, credential check, or
  synthetic turn is not an ordinary execution observation.
- **Authoritative fact**: one immutable `r2_authoritative_facts` row with `factId`, one
  R2 `factKind`, the complete typed R2 match key, `sourceTransitionId`,
  `selectionTransitionId`, `materializedByTransitionId`, `causeKind`, `principal`,
  `observedAt`, and optional `expiresAt`. The source transition proves inability. The
  selection transition supplies the exact execution selection. The materializing
  transition is the source, selection, or token transition whose commit required this
  fact to be inserted. Two or all three IDs are equal when one transition performs
  those roles.
- **Fact ID**: `r2f_` followed by the lowercase SHA-256 digest of the canonical CBOR
  encoding of
  `{factKind, completeMatchKey, sourceTransitionId, selectionTransitionId,
  materializedByTransitionId}`. The causal transition IDs prevent a restored database
  from reusing an old evidence reference for a different observation at the same
  revision. Canonical CBOR uses definite lengths, lexicographically ordered text keys,
  UTF-8 text without normalization, signed integer values, and explicit null. Tightbeam
  compares typed members after candidate-row lookup; a digest is not evidence of
  equality.
- **Current fact**: an authoritative fact whose typed key equals the read snapshot
  member-for-member, whose referenced registry revisions remain current, whose source
  registry state still denotes that fact kind, and whose `expiresAt` is null or greater
  than the transaction clock.
- **Expiry transition**: the deterministic local transition that changes an entity with
  a reached `expiresAt` to `expired`, advances its revision, and writes no inability
  fact. The clock crossing also makes the old fact non-current before that transition
  commits.
- **R2 snapshot**: the result of `R2Facts.snapshot_for_selection/2`, called inside the
  consumer's existing database transaction. It contains one execution selection,
  available current tokens, and exact matching current facts ordered by F7 R2 priority.
- **Writer principal**: exact value `process:tightbeam`, stored on each registry event
  and authoritative fact. The registry event separately stores the authenticated actor
  principal that caused the transition.

## Assumptions

1. The session row remains the source of `sessionKey`, `sessionUpdatedAt`, `host`,
   `harness`, `provider`, `modelFamily`, `modelContext`, and `effort`.
2. The current database supplies transactions with a single transaction clock and
   snapshot isolation across the rows read by `R2Facts.snapshot_for_selection/2`.
3. Each source owner can produce typed local transitions without an external call at
   the R2 send or act edge. A source that cannot do so leaves its token absent, which
   means unknown ability under F7.
4. The composition successor owns the final schema stamp and migration order. This base
   owns only its module DDL, state transitions, and validation contract.
5. No reviewed Tightbeam specification already defines these R2 registry objects,
   transition writers, or fact writer. The sibling proposal is not an alias or source.
6. F7 remains the sole authority for how Gateway and Wakes use a returned fact. This
   base exposes facts and tokens; it does not refuse, accept, settle, notify, reroute, or
   retry a wake.

## Invariants

### B1. One schema owner and one mutation seam

`R2Facts` is the only module that supplies DDL for the objects in B2. `Schema` remains
the central stamp and migration coordinator and consumes that DDL through the existing
ordered module seam.

`R2Facts` is the only module that inserts, updates, or deletes an R2 registry current
row; appends an R2 registry event; or inserts an authoritative fact. A source owner must
call a typed `R2Facts` transition function inside the source owner's existing database
transaction. A source owner must not write an R2 table directly.

`R2Facts` derives each transition ID, revision, fact kind, complete match key, fact ID,
writer principal, and fact expiry. A caller supplies none of those derived fields.

`R2Facts` exposes one typed function for each B3 row and no generic `record_fact`,
`record_transition`, or map-shaped mutation function. Each function fixes its
`sourceOwner` literal, accepts the source domain's typed state plus existing
authorization context, and derives the actor from that context. Database checks backstop
the typed seam.

### B2. Exact durable objects

The base owns these objects:

| Object | Stable identity and current fields | Event history | Required constraints |
|---|---|---|---|
| `r2_transitions` | `transitionId`, `registryKind`, entity ID, version, source owner and event ID, canonical source payload, 32-byte SHA-256 `payloadDigest`, typed cause, actor, writer principal, observed time | the table is the immutable common event header | unique `{registryKind,entityId,version}` and `{sourceOwner,registryKind,sourceEventId}`; append-only |
| `r2_session_execution_events` | transition ID, existing `sessionKey`, exact execution-selection fields, `sessionState=active|retired`, and `sessionUpdatedAt` as version | the table is the immutable session-execution detail history; the session row remains current truth | one event per `{sessionKey,sessionUpdatedAt}`; greatest event equals the current session selection and state; append-only |
| `r2_session_holds` | `holdId` (`r2h_`), `sessionKey`, `holdRevision`, `state=active|released|expired`, typed cause, actor, `releasePrincipal`, observed time, optional expiry, optional `terminalAt` | `r2_session_hold_events` | one active hold per session; positive revision; active has null `terminalAt`; released or expired has non-null `terminalAt`; activation has exactly one of expiry and release principal |
| `r2_adapter_instances` | `adapterId` (`r2a_`), `harnessId`, exact scope `shared`, `host`, `adapterGeneration`, `adapterRevision`, `adapterState=unknown|available|unavailable`, `acpState=unknown|available|unavailable`, typed cause, actor, observed time | `r2_adapter_events` | one current row per `{harnessId,shared,host}`; positive generation and revision |
| `r2_adapter_circuits` | `circuitId` (`r2c_`), `adapterId`, `circuitRevision`, `state=open|closed`, typed cause, actor, observed time | `r2_adapter_circuit_events` | one circuit per adapter entity; positive revision |
| `r2_harness_catalogs` | `catalogId` (`r2g_`), `host`, `harness`, `provider`, `catalogRevision`, typed cause, actor, observed time | `r2_harness_catalog_events` | one registry per `{host,harness,provider}`; positive revision |
| `r2_harness_catalog_entries` | catalog ID and current revision plus exact `modelFamily`, explicit-null-or-text `modelContext`, explicit-null-or-text `effort`, and `state=available|unavailable` | current projection of `r2_harness_catalog_event_entries` | one entry per exact selection tuple at the current revision; absence is unknown, not unavailable |
| `r2_harness_catalog_event_entries` | catalog transition ID and revision plus the same typed entry fields | immutable child rows of `r2_harness_catalog_events` | one entry per exact selection tuple at that transition; append-only |
| `r2_credential_slots` | `credentialSlotId` (`r2k_`), `host`, `harness`, `provider`, `credentialRevision`, `state=present|missing`, typed cause, actor, observed time | `r2_credential_events` | one slot per `{host,harness,provider}`; no secret, account ID, token fingerprint, quota amount, or provider response |
| `r2_quota_windows` | `quotaWindowId` (`r2q_`), credential slot ID and credential revision, `quotaWindowRevision`, opaque typed `windowKind`, `startsAt`, `expiresAt`, `state=available|exhausted|expired`, typed cause, actor, observed time, optional source turn | `r2_quota_window_events` | positive credential revision; `startsAt < expiresAt`; exhaustion proves inability only before `expiresAt`; an observed exhaustion references an admitted ordinary turn; no quota amount or predictive field |
| `r2_authoritative_facts` | fact fields and flat typed key columns from B5 | none; facts are themselves the immutable history | append-only; exact fact-kind nullability checks; unique fact ID; no secret-bearing field |

Each ID, enum, natural-key member, source event ID, cause, and principal uses `TEXT`.
Each ID and required text has a non-empty check. Revisions, generations, and times use
`INTEGER`; revisions and generations are positive, and times are non-negative. Canonical
typed payloads use `BLOB`. Explicit-null fields use SQL null. Each named relationship
uses a foreign key. No registry or fact column stores JSON.

`r2_transitions` stores the common source fields and canonical payload. Replay compares
the stored payload bytes, not only its digest. The payload must decode canonically and
equal the transition header and typed event detail member-for-member. Each non-session
registry event table stores its `transitionId` foreign key, entity ID, `priorRevision`
or null for creation, `revision`, and complete typed state. The session-execution event
instead uses `sessionKey` as entity ID, the prior `sessionUpdatedAt` or null, and the new
`sessionUpdatedAt` as version. The event tables, catalog event-entry table, transition
table, and fact table reject update and delete.

The current registry tables are projections of their event histories. The session row
is current session truth and its greatest R2 session-execution event must equal its
selection and state. Validation must prove these equalities and that no revision gap,
duplicate revision, or orphan event exists.

Each current registry row stores `currentTransitionId` as a foreign key to
`r2_transitions` and its matching typed event. Each current catalog entry stores the
catalog's current transition ID. Each fact stores source, selection, and materializer
foreign keys to `r2_transitions`; its selection foreign key must name a
`session_execution` transition for the fact's exact session key and selection fields.
Thus each current state and fact resolves to its exact selection, typed cause, actor
principal, writer principal, and observation time without inference.

### B3. Exact source owners and principals

Only these typed source calls may create transitions:

| Source owner | R2 call | State it may supply | Fact result when the committed state proves inability |
|---|---|---|---|
| `Sessions` | `record_session_transition` | session-row `updatedAt` advance or retirement from the same session mutation | `session_retired` for a retired exact selection; refresh current selection-dependent facts after another `updatedAt` advance |
| `R2Facts.Holds` | `record_hold_transition` | activate, renew, release, or expire one session hold after its separate policy authorization | `session_held` while active |
| `AdapterCoordinator` | `record_adapter_transition` | adapter generation, adapter state, or ACP state | `adapter_unavailable` and `acp_unavailable` for the corresponding unavailable state |
| `AdapterCircuit` | `record_circuit_transition` | open or close one adapter circuit | `circuit_open` while open |
| `HarnessCatalog` | `record_catalog_transition` | one complete typed catalog entry set for host, harness, and provider | `harness_unavailable` only for an explicit unavailable entry matching the selection |
| `Credentials` | `record_credential_transition` | create a slot, record present, record missing, or record replacement | `credential_missing` while missing |
| `QuotaClassifier` | `record_quota_transition` | one bounded typed window state derived from an ordinary execution observation | `quota_exhausted` while exhausted and unexpired |
| `R2Facts` expiry worker | `expire_due_entities` | due hold or quota expiry selected by the transaction clock | no inability fact for the expired revision |

The authenticated transport supplies `actorPrincipal`; request data cannot override it.
`R2Facts` stores `process:tightbeam` as writer principal on the derived event and fact.
The typed local quota classifier may consume a structured provider or harness signal
that an ordinary execution already produced. `QuotaClassifier` is callable only from
that turn's existing terminal transaction. It derives `sourceTurnSeq` from the carrier
and the credential token from the adapter's structured execution envelope, not request
data or a later current-token read. The quota event stores that token in its canonical
payload. It cannot initiate traffic or translate an untyped string into exhaustion.

The hold row is a hold under T-RECOGNITION. This base records it by that name. It does
not hide it behind adjudication or decision vocabulary. Each activation records its
cause, actor principal, and either an explicit expiry or the separately authorized
`releasePrincipal`. A release requires that exact principal or existing administrator
authority. This base adds no policy that decides activation or release.

An actor principal has exact form `user:<non-empty-id>`, `session:<non-empty-id>`, or
`process:<non-empty-id>`. The writer principal is exactly `process:tightbeam`. The closed
`registryKind` values are `session_execution`, `session_hold`, `adapter`, `circuit`,
`catalog`, `credential`, and `quota_window`. The closed source cause set is:

| Registry kind | Allowed `causeKind` |
|---|---|
| session execution | `session_updated`, `session_retired` |
| session hold | `hold_activated`, `hold_renewed`, `hold_released`, `hold_expired` |
| adapter | `adapter_registered`, `adapter_state_reported`, `acp_state_reported` |
| circuit | `circuit_opened`, `circuit_closed` |
| catalog | `catalog_registered` |
| credential | `credential_registered`, `credential_replaced`, `credential_removed`, `credential_absent` |
| quota window | `quota_observed`, `quota_cleared`, `quota_expired` |

`R2Facts` copies the source event cause into each derived fact. A new cause requires a
reviewed amendment to this table.

Each cause permits exactly this transition. “Same” below means a new source event with
a byte-equal typed state; it advances revision under B4.

| `causeKind` | Permitted state transition |
|---|---|
| `session_updated` | create `active` or `active` to `active`, including same selection values before the required `sessionUpdatedAt` advance |
| `session_retired` | create `retired` during structured migration or `active` to `retired`; `retired` is terminal |
| `hold_activated` | create `active` |
| `hold_renewed` | `active` to `active`, including same |
| `hold_released` | `active` to terminal `released` |
| `hold_expired` | expiry worker changes `active` to terminal `expired` |
| `adapter_registered` | create an adapter entity or advance both generation and revision for its newly registered process; it supplies both typed states |
| `adapter_state_reported` | within one generation, keep ACP state and set adapter state, including same |
| `acp_state_reported` | within one generation, keep adapter state and set ACP state, including same |
| `circuit_opened` | create `open`, change `closed` to `open`, or repeat `open` |
| `circuit_closed` | create `closed`, change `open` to `closed`, or repeat `closed` |
| `catalog_registered` | create or replace one complete entry set, including a byte-equal set |
| `credential_registered` | create `present` |
| `credential_absent` | create `missing` |
| `credential_replaced` | change `present` or `missing` to `present`, including same |
| `credential_removed` | change `present` or `missing` to `missing`, including same |
| `quota_observed` | create or change an unexpired exact window to `exhausted`, including same, from its admitted ordinary turn |
| `quota_cleared` | create or change an unexpired exact window to `available`, including same, from its admitted ordinary turn |
| `quota_expired` | expiry worker changes `available` or `exhausted` to terminal `expired` |

Any other state or cause pairing returns `r2_transition_invalid` and changes no row.

### B4. Revision initialization and advancement

Creation initializes each registry entity at revision `1`. Adapter creation initializes
`adapterGeneration=1` and `adapterRevision=1`. A new hold after a released or expired
hold creates a new hold ID at revision `1`; a terminal hold ID cannot become active
again. A later quota event identifies the same window only by the exact tuple
`{credentialSlotId, credentialRevision, windowKind, startsAt, expiresAt}`; another tuple
creates a new quota window ID at revision `1`. A credential replacement therefore
cannot reuse a prior credential revision's quota window.

A committed source event with a new `sourceEventId` advances its entity revision by one
even when its new typed state equals the prior state. `Sessions` must advance
`sessionUpdatedAt` for each new session source event, including a same-value event. If
the transaction clock does not exceed the prior value, `Sessions` uses the prior value
plus one. It appends the matching R2 session-execution event and refreshes facts against
that exact selection in the same transaction. A newly
registered adapter process advances `adapterGeneration` and `adapterRevision` by one;
this transition does not reuse the prior token. An adapter-state or ACP-state event
within the generation advances only `adapterRevision` by one.

A source event that changes a complete catalog replaces its entry set and advances
`catalogRevision` once. A credential replacement that remains `present` advances
`credentialRevision`. A quota observation or clearing event for the same window advances
`quotaWindowRevision`; a new bounded window receives a new quota window ID at revision
`1`. Hold renewal advances `holdRevision`. Circuit open-to-open and closed-to-closed
source events advance `circuitRevision`.

When a same-value event preserves an inability state, the transaction inserts or reads
the fact for the new exact revision and the older fact stops matching. When it preserves
a runnable or unknown state, it inserts no inability fact.

A replay returns the original transition and derived facts. A compare-and-set conflict,
authorization failure, malformed input, database validation failure, or transaction
rollback changes no revision and creates no event or fact.

A compare-and-set conflict returns `r2_revision_conflict`. A typed event with an empty,
oversized, or invalid-UTF-8 source event ID; negative time; invalid enum; missing
required field; extra field; or state transition forbidden by B2 returns
`r2_transition_invalid`.

An entity at the greatest positive 64-bit revision rejects a new event with
`r2_revision_exhausted`. The same error applies when `adapterGeneration` or
`sessionUpdatedAt` cannot advance within a positive 64-bit integer. An entity-ID
collision rejects creation with `r2_id_collision`. A transition-ID digest collision
whose full identity tuple differs rejects the event with `r2_transition_id_collision`.
A fact-ID digest collision whose full identity tuple differs rejects the transition with
`r2_fact_id_collision`. Each error rolls back the source transaction and changes no row.

Database restart alone changes no revision. At startup, `R2Facts` runs the expiry worker
before Gateway or Wakes can consume an R2 snapshot. Each due entity advances once to
`expired`. Repeating startup reads the committed expired revision and writes nothing.

### B5. Exact fact shapes

`r2_authoritative_facts` stores the execution-selection fields as typed columns. It
stores the optional token columns shown below. Its checks make every column outside the
selected shape null and every column inside the selected shape non-null, except the
explicitly nullable execution `modelContext` and `effort` values.

| `factKind` | Complete typed match key | Source state that permits insertion | Fact expiry |
|---|---|---|---|
| `session_retired` | `{executionSelection}` | exact session transition is retired | null |
| `session_held` | `{executionSelection, holdId, holdRevision}` | hold state is active | hold expiry or null |
| `circuit_open` | `{executionSelection, adapterToken, circuitId, circuitRevision}` | circuit state is open for the current adapter token | null |
| `adapter_unavailable` | `{executionSelection, adapterToken}` | adapter state is unavailable | null |
| `acp_unavailable` | `{executionSelection, adapterToken}` | ACP state is unavailable | null |
| `harness_unavailable` | `{executionSelection, harnessCatalogToken}` | exact catalog entry state is unavailable | null |
| `credential_missing` | `{executionSelection, credentialToken}` | credential slot state is missing | null |
| `quota_exhausted` | `{executionSelection, credentialToken, quotaWindowId, quotaWindowRevision}` | quota window state is exhausted and transaction clock is before its expiry | quota-window expiry |

The typed writer and B7 validation also require each duplicated association to agree.
A hold's session key equals the execution session key. An adapter or circuit fact's
adapter host and harness ID equal the execution host and harness, and its scope is
`shared`. A catalog or credential token's host, harness, and provider equal the
execution fields. A credential slot belongs to that exact natural key. A quota window's
credential slot and credential revision equal the complete credential token. A row that
violates one association returns `r2_fact_shape_invalid` and cannot become current.

One source transition may insert several fact kinds when its exact state proves several
conditions. For example, one adapter event may prove both adapter and ACP unavailability.
Each fact receives its own deterministic ID and the same source transition ID.

In the source transaction, `R2Facts` materializes those facts for this exact affected
selection set:

| Transition | Current session rows in the affected set |
|---|---|
| session execution or hold | the one row with the transition's exact `sessionKey` |
| adapter or circuit | every row whose `host` equals the adapter host and whose `harness` equals the adapter `harnessId` |
| catalog | every row whose `{host,harness,provider}` equals the catalog key and whose `{modelFamily,modelContext,effort}` has an explicit unavailable entry |
| credential | every row whose `{host,harness,provider}` equals the credential slot key |
| quota window | every row whose `{host,harness,provider}` equals the quota window's credential-slot key and whose current credential revision equals the window's credential revision |

Each selected row must have a matching current `r2_session_execution_events` detail.
The fact stores that event as `selectionTransitionId` and stores the source transition as
`materializedByTransitionId`. A transition with no affected current session inserts no
fact. An affected row without its matching detail returns `r2_state_invalid` and rolls
back the source transaction. A later session transition materializes the
still-applicable fact for its new selection and stores that session transition as both
selection and materializer.

If a fact ID already exists, `R2Facts` compares its fact kind, each typed match-key
member, and all three causal transition IDs. Exact equality returns the existing fact.
Any difference returns `r2_fact_id_collision`; the digest alone never authorizes reuse.

An execution-selection transition refreshes facts only for current source states that
still prove inability for that new exact selection. Those facts retain the inability
event as `sourceTransitionId` and name the session event as
`selectionTransitionId` and `materializedByTransitionId`. An adapter-token transition
refreshes an open-circuit fact against the new adapter token, retains the circuit event
as source, retains the current session event as selection, and names the adapter event
as materializer. A credential revision change does not refresh an exhausted quota fact
or return the old quota token; a new typed quota observation must bind exhaustion to the
new credential token.

An available, closed, present, unknown, released, or expired state creates no runnable
fact. Its revision advance makes the prior inability fact stale. This base represents
failure as a named value and represents lack of proof as unknown; it does not mint a
positive runnable assertion.

### B6. Transactional read seam

`R2Facts.snapshot_for_selection/2` accepts only an exact session key and the caller's
database transaction. It reads the transaction clock, session row, current registry
rows, current catalog entries, and fact rows from that transaction.

The function returns `selection_missing` when the session row is absent. It returns
`r2_state_invalid` with the first affected entity ID in byte order when validation finds
a current row that does not equal its greatest event revision. A catalog-entry mismatch
uses the canonical CBOR bytes of its complete natural key in place of an entity ID. It
returns no partial snapshot on either error.

For a valid state, it returns:

```text
{
  executionSelection,
  holdToken | null,
  adapterToken | null,
  circuitToken | null,
  harnessCatalogToken | null,
  credentialToken | null,
  quotaTokens: [...],
  currentFacts: [...]
}
```

`holdToken` names only the active hold. The adapter, circuit, catalog, and credential
tokens name an existing current registry row regardless of whether that row proves
inability. The quota-token list contains only unexpired windows whose credential slot
and credential revision equal the current credential token. It orders them by
`expiresAt`, then by exact `quotaWindowId` bytes. `currentFacts` uses F7 R2 precondition
priority; facts of the same kind use exact `factId` byte order. The first fact for a
selected precondition is its deterministic evidence reference.

The seam compares text as exact stored UTF-8 bytes, integers by value, and null only
with null. It performs no case folding, Unicode normalization, alias expansion, default
substitution, fuzzy match, or prose parse. It compares each typed member after
candidate-row lookup and does not accept a hash match as member equality.

The function performs no network, provider, adapter, ACP, harness, credential, process,
or filesystem call. An absent row, absent token, unknown state, expired fact, stale
revision, invalid fact shape, or member mismatch contributes no current fact.

The send check and act-edge check call this seam inside their own existing transactions.
The check and the consumer action that depends on it use the same database snapshot; no
gap may separate the check from the R3 refusal decision or the R4 act-edge branch.

### B7. Expiry, restart, migration, rollback, and validation

The transaction clock makes a fact non-current at `expiresAt`. The expiry worker selects
due active holds and quota windows in `{expiresAt, entityId}` order. It commits one typed
expiry transition per entity through the same mutation seam. Its source event ID is
`r2-expire:<entityId>:<currentRevision>:<expiresAt>` and its observation time is the
transaction clock. A worker failure leaves the current revision unchanged for the
uncommitted entity. Restart repeats selection and writes only missing expiry transitions.
At startup, `R2Facts` validates once, runs this worker, validates again, and only then
permits Gateway or Wakes to start. A validation error returns its B7 code. An expiry
transaction failure returns `{r2_expiry_failed, entityId}` and starts no consumer.

This base supplies one normalized DDL string for each B2 table, index, and append-only
trigger. The composition successor must add these strings to the existing ordered
`Schema` module registry before it may implement its v7-to-v8 transaction. This file
does not change the schema stamp.

An empty database creates the B2 objects with no registry or fact rows. The first typed
source event for an entity creates revision `1`.

The v7-to-v8 transaction defined by the future incorporated composition creates the B2
objects and no facts from prompt text, error text, prior failed turns, unstructured
origin, in-memory state, or guessed identity. It may call the named local source owners
against structured current rows before consumers start. It initializes `Sessions`
events first in exact session-key byte order. It then calls the remaining B3 source
owners in B3 table order and orders each owner's entities by the canonical CBOR bytes of
its B2 natural key. A source owner that cannot produce a complete typed event leaves its
registry absent and its ability unknown.
Each migration event uses source event ID
`r2-migrate-v7:<sourceOwner>:<sha256(canonicalStructuredSourceIdentityAndVersion)>`,
using the Fact ID canonical CBOR rules. The ID exposes no source identity member.

Before the composition transaction changes its stamp, `R2Facts.validate/1` must compare
each normalized database object with the one owning DDL string, validate event-to-current
projection equality, validate revision continuity, validate fact-kind nullability,
recompute each canonical payload digest, transition ID, and fact ID, and prove that each
canonical payload equals its header and typed event detail. It must prove that each
fact's source event permits its kind and that its selection event equals its complete
execution selection. It must also prove that its materializer is the source, selection,
or token transition that required that fact, require an empty foreign-key check, and
require an `ok` integrity check. The stamp change remains the composition transaction's
final mutation.

Validation uses this closed error set in priority order:

1. `r2_schema_object_mismatch`;
2. `r2_revision_gap`;
3. `r2_revision_duplicate`;
4. `r2_event_orphan`;
5. `r2_payload_digest_invalid`;
6. `r2_transition_id_invalid`;
7. `r2_event_payload_mismatch`;
8. `r2_current_projection_mismatch`;
9. `r2_fact_shape_invalid`;
10. `r2_fact_id_invalid`;
11. `r2_foreign_key_invalid`;
12. `r2_integrity_invalid`.

Within one code, validation names the first identifier by exact stored bytes: a schema
object name for a DDL mismatch and an entity, transition, or fact ID for a row mismatch.
It returns one error and starts no Gateway or Wakes consumer.

A failure during DDL, structured source initialization, registry event insertion,
current projection, fact insertion, ID recomputation, object comparison, foreign-key
check, integrity check, or stamp change preserves the exact predecessor stamp, rows, and
objects and leaves no B2 object or row. Immediate post-commit validation and a clean
restart perform read-only validation except for reached expiries.

Restoring a database backup restores its registry revisions, events, and facts as one
snapshot. Startup neither invents a missing later revision nor replays an external
source event. A genuinely new later source event must carry a new source event ID and
advances from the restored current revision. An exact external replay of the discarded
event may carry its original ID and payload and reconstructs that event at the restored
next revision.

### B8. Authorization and projections

Only the internal source-owner calls in B3 can request mutation. Each call must pass the
existing authorization for its source domain before `R2Facts` writes. A remote request
or public command that supplies a registry state, entity ID, revision, fact kind, match
key, fact ID, writer principal, observed time, or expiry is rejected before mutation.

Gateway and Wakes may read a snapshot inside their authorized transaction. The existing
F7 R7 authorization controls public refusal, terminal, trace, and notice projections.
This base adds no public registry dump.

An authorized `evidenceRef` resolves to `factId`, `factKind`, typed cause, writer
principal, observation time, and expiry. It does not expose the stored match key,
`credentialSlotId`, another registry entity ID, account data, quota amount, or provider
response. An unrelated principal receives `denied` and no existence signal.

### B9. Subtraction and pattern ruling

ADD wins for the typed registries and immutable facts because reviewed F7 requires each
exact token and evidence reference; deleting them or accepting an untyped failure would
make reviewed R2 unbuildable and would permit stale evidence to refuse a wake. This is
the minimum mechanism that closes that reviewed dependency.

No positive runnable registry, probe scheduler, inferred health score, alias registry,
repair workflow, or retry workflow is added. Unknown remains the named absence of proof.
The substrate records and verifies local truth; Gateway applies the already-reviewed R2
policy. This preserves wisdom 6, 9, and 10.

This capability establishes one pattern: a consumer that gates on local failure evidence
uses immutable facts bound to monotonically revised source tokens and reads them in the
same transaction as its action. Guidance must not teach that pattern until this base is
reviewed, incorporated, implemented, and verified against real inputs (wisdom 20).

## Architecture

The base has one write path:

1. A named source owner receives or creates one typed local source event through its
   existing authorized path.
2. In the source transaction, the owner calls its B3 `R2Facts` transition function.
3. `R2Facts` checks authorization and source-event replay identity.
4. `R2Facts` validates the typed event against the source registry shape.
5. `R2Facts` appends one registry event and updates its current projection.
6. `R2Facts` derives and inserts the exact immutable inability facts permitted by B5.
7. The transaction commits the source mutation, registry event, current projection, and
   facts together.

The base has one read path:

1. Gateway or Wakes resolves the exact target under F7 R1.
2. Inside the caller's existing transaction, it calls
   `R2Facts.snapshot_for_selection/2`.
3. `R2Facts` returns one snapshot or one named error under B6.
4. The caller applies F7 R2-R4 without another state read between the check and action.

Traceability is explicit in both directions:

| Base requirement | Architecture step | Acceptance evidence |
|---|---|---|
| B1-B3 | write steps 1-4 | A1 and A5 |
| B4 | write steps 3-5 | A2 |
| B5 | write step 6 | A3 |
| B6 | read steps 1-4 | A4 |
| B7 | schema and write steps 5-7 | A2 and A6 |
| B8 | write step 3 and read step 3 | A5 |
| B9 | object census and exclusions | A1 and A7 |

The current projection is an affordance; the append-only event and fact histories are
the audit rows; exact revisions and table checks are the rail (wisdom 1-5). No inference
runs in either path.

## Acceptance

### A1. Object census, ownership, and stable IDs

Given an empty fixture, when the R2 module bootstrap runs, then the database contains
exactly the B2 tables, required uniqueness indexes, foreign keys, fact-shape checks, and
append-only triggers from the module DDL. The object census contains no wake, terminal,
notice, sibling-ledger, retry, alias, probe, or positive-runnable object.

Given one creation event for each hold, adapter, circuit, catalog, credential slot, and
quota window registry, when the transaction commits, then each entity ID has its exact
B2 prefix plus 32 lowercase hexadecimal characters, each revision is `1`, and each
event names `process:tightbeam` plus the authenticated actor and typed cause. No ID
contains host, harness, provider, credential, account, or quota text.

Given an update or delete against an event or fact row outside `R2Facts`, when the
database executes it, then an append-only trigger aborts the statement and each row
remains byte-for-byte equal.

### A2. Revision lifecycle, expiry, restart, and rollback

For each registry kind, given revision `1`, when a new source event changes its typed
state, then one transaction writes revision `2`, one exact transition ID, and the new
current projection. Given another event with a new source event ID and the same typed
state, then it writes revision `3`. Given a replay of either event, then it returns the
first transition and leaves row counts and revisions unchanged.

Given the same source event ID with one changed typed payload member, when the source
submits it, then the mutation returns `r2_source_event_conflict` and leaves the first
event, current projection, revisions, and facts unchanged.

For each B3 cause, given each creation, change, and same-state transition permitted by
the B3 matrix, when its new source event commits, then it produces the exact state and
revision required by B4. Given a different cause-state pairing, a retired session
reactivation, a terminal hold mutation, or an expired quota-window mutation, then the
call returns `r2_transition_invalid` and changes no row.

Given that the repeated state proves inability, when revision `3` commits, then the new
exact fact is current and the revision-`2` fact is stale. Given that the repeated state
is available, closed, present, unknown, released, or expired, then revision `3` creates
no inability fact.

Given adapter generation `1` at adapter revision `N`, when a new adapter process
registers, then the token has generation `2` and adapter revision `N+1`; the prior token
does not match. Given an adapter-state event in generation `2`, then only adapter
revision advances to `N+2`.

Given one active hold with an expiry and one exhausted quota window, when the transaction
clock reaches each expiry, then neither old fact is current. When the expiry worker
runs, it advances each due entity exactly once to `expired` in B7 order and inserts no
inability fact. When Tightbeam restarts before or after that worker commit, then startup
finishes the missing expiry transition once and preserves a committed transition.

Given a due entity and a forced expiry-transaction failure during startup, when startup
runs, then it returns `{r2_expiry_failed, entityId}`, starts neither Gateway nor Wakes,
and leaves that entity unchanged. When the failure is removed and startup runs again,
then it commits the one missing expiry transition and starts consumers only after the
second validation succeeds.

Given a forced failure after event insertion, current-row update, or fact insertion,
when the transaction rolls back, then the prior event count, current revision, and fact
count remain exact. Given database restart without a due expiry, then no revision,
transition ID, fact ID, or row changes.

Given the greatest positive 64-bit revision, an entity-ID collision, a transition-ID
digest collision with a different full identity tuple, or a fact-ID digest collision
with a different full identity tuple, when the mutation runs, then it returns the named
B4 error and changes no source row, event, current projection, or fact.

### A3. Each R2 fact key and each one-member mismatch

Given one exact current source state for each F7 R2 fact kind, when the named source
transition commits, then `r2_authoritative_facts` contains one fact with the exact B5
key, correct fact kind, deterministic fact ID, source transition, selection transition,
materializing transition, typed source cause, `process:tightbeam` principal, source
observation time, and required expiry.

Given a current inability state before a session is created or its selection changes,
when `Sessions` commits the new exact selection and its session-execution event, then the
same transaction inserts each B5 fact whose source state applies to that selection.
Each refreshed fact retains the inability event as source and names the session event as
selection and materializer.
Given an open circuit and a new adapter token, when the adapter transition commits, then
the same transaction inserts the open-circuit fact against the new token and the prior
fact becomes stale; the new fact names the circuit event as source and adapter event as
materializer and names the current session event as selection. Given an exhausted quota
fact and a credential revision change, then the transaction does not copy exhaustion or
the old quota token to the new credential token.

Given two current sessions in one affected B5 set and one current session outside it,
when the source transition commits, then it inserts the applicable facts for exactly the
two affected selections. Given no current session in the affected set, it inserts no
fact; when a later session transition enters that set, that transaction inserts the
still-applicable fact.

Each mismatch fixture below exercises the snapshot's candidate-row matcher. It changes
exactly one typed member on one side of the comparison: the current snapshot when a
typed lifecycle transition can produce the change, or a candidate row with a recomputed
fact ID otherwise. When B2 or B5 makes the resulting candidate combination impossible
in durable state, the fixture also asserts `r2_fact_shape_invalid`; it is matcher
evidence, not evidence that the source writer accepts that row.

For each fact kind, start with one matching fact. In separate fixtures, change only one
of these members in the snapshot: `sessionKey`, `sessionUpdatedAt`, `host`, `harness`,
`provider`, `modelFamily`, `modelContext`, or `effort`. The old fact must not appear in
`currentFacts`. Run both null and non-null mismatch directions for `modelContext` and
`effort`.

For the fact kinds that carry the member, repeat the fixture by changing only
`adapterToken.harnessId`, `adapterGeneration`, `adapterRevision`, `catalogRevision`,
`credentialRevision`, `quotaWindowRevision`, `holdRevision`, or `circuitRevision`. The
old fact must not appear.

Repeat the one-member fixture for each duplicated token member:
`adapterToken.scope`, `adapterToken.host`, `harnessCatalogToken.host`,
`harnessCatalogToken.harness`, `harnessCatalogToken.provider`,
`credentialToken.host`, `credentialToken.harness`, and `credentialToken.provider`.
Each otherwise-valid changed key uses its recomputed deterministic fact ID and does not
match. `adapterToken.scope` has only the valid value `shared`; a different stored value
also fails fact-shape validation.

Repeat the fixture by changing only each opaque member required by reviewed F7:
`credentialToken.credentialSlotId`, `quotaWindowId`, `holdId`, and `circuitId`. Also
change only `factKind`. Each otherwise-valid changed key uses its own recomputed
deterministic fact ID. Each old fact must not appear.

Given an absent registry token, stale revision, expired fact, malformed fact shape,
catalog entry absence, or unknown source state, when the snapshot runs, then the result
contains no fact for that source. It performs no external call.

### A4. Transactional snapshot and deterministic result

Given a consumer transaction that starts before a concurrent registry transition
commits, when it calls the snapshot, then it returns only the prior complete token and
fact set. Given a consumer transaction that starts after the commit, then it returns
only the new complete token and fact set. No fixture returns a new revision with an old
state or an old revision with a new fact.

Given current facts for several F7 preconditions, when the snapshot runs, then
`currentFacts` follows the exact F7 R2 priority. Given several exhausted quota windows,
then their tokens follow `expiresAt` and exact quota-window ID byte order. A repeated
snapshot in the same transaction returns byte-for-byte equal IDs and ordering.

Given a current-row/event mismatch, when the snapshot runs, then it returns
`r2_state_invalid` with the first B6 identifier in byte order and no partial selection,
token, or fact result. Given an absent session, it returns `selection_missing` and no
partial result.

Given an unexpired quota window observed for credential revision `N`, when the current
credential revision is `N+1`, then the snapshot returns neither that quota token nor its
fact. Given a later typed quota observation at revision `N+1`, then it returns only the
new credential-bound window and exact matching fact.

Given a transaction barrier between the snapshot call and the consumer action, when a
concurrent source transition commits outside that transaction, then the consumer still
acts only on its original snapshot. A new send or act-edge transaction sees the later
revision. This fixture proves the check and action share one transactional step.

### A5. Writers, authorization, privacy, and validation

Given the compiled `R2Facts` API, when the source-owner function census runs, then it
contains the exact B3 functions and contains no generic fact, transition, or map-shaped
mutation entry point.

Given one request from each unauthorized user, session, and process principal, when it
attempts an R2 transition, then existing source-domain authorization returns `denied`
before an event, current row, or fact changes.

Given a public or remote request that supplies a registry entity ID, revision,
transition ID, fact kind, match key, fact ID, writer principal, observation time, or
expiry, when request validation runs, then it returns `r2_derived_field_forbidden` and
changes no row. Internal source calls identify current entities through their exact B2
natural keys; only `R2Facts` resolves the opaque entity ID.

Given an adapter source event whose scope is not exact `shared`, when validation runs,
then it returns `r2_adapter_scope_invalid` and changes no row.

Given a typed quota event from an ordinary execution, when it carries an exact bounded
window and typed exhaustion state, then the quota source may commit it. Given error prose,
an unbounded exhaustion claim, a predicted threshold, a missing or non-admitted source
turn, a structured execution envelope that does not name the credential token, or an
event produced by a probe, then validation returns `r2_quota_evidence_invalid` and
changes no row.

Given an authorized R2 consumer, when it resolves a fact evidence reference, then it
receives the B8 non-secret projection. Given an unrelated principal, then the resolver
returns `denied` without revealing fact existence, credential slot ID, registry entity
ID, account data, quota amount, or provider response.

### A6. Migration, validation, restart, and backup restore

Given an exact predecessor fixture used by the future incorporated v7-to-v8 composition,
when migration runs, then it creates each B2 object from its one module DDL string and
creates no fact from prompt text, error text, prior failed turns, unstructured origin, or
in-memory state. It creates session events first and then source events in the exact B7
order. A named source owner either supplies one complete typed local event or leaves the
source absent and ability unknown.

Given a failure during each B7 migration stage, when the migration transaction exits,
then the predecessor stamp, rows, and objects remain byte-for-byte equal and no B2 object
or row remains. Given a successful commit, when validation and a clean restart run, then
they change no object, registry row, event, revision, or fact except one reached expiry.

Given one fixture for a missing DDL object, changed normalized SQL, revision gap,
duplicate revision, orphan event, current/event mismatch, invalid fact nullability,
fact source that does not permit its kind, selection event that differs from its
execution selection, invalid materializer, wrong payload digest, wrong transition ID,
canonical payload/detail mismatch, wrong fact ID, foreign-key failure, or integrity
failure, when validation runs, then it returns the corresponding B7 error before Gateway
or Wakes starts. Given several faults, it returns the first B7 code and identifier in the
specified orders.

Given a backup at revision `N` and later live revision `N+1`, when the backup is restored,
then startup retains revision `N` and its matching event and fact set. It does not invent
or replay `N+1`. The next new source event commits revision `N+1` from the restored row.
Given that its source event or payload differs from the discarded live event, its
transition ID and every derived fact ID also differ from the discarded IDs. Given an
exact replay of the discarded event ID and payload instead, it reconstructs the same
transition and fact IDs.

### A7. Consumer conformance and preserved gate

Given the reviewed F7 key table, when its eight fact-kind fixtures run against this base,
then each exact matching fact is constructible through B3-B6 and each A1 opaque mismatch
fixture from F7 is represented by A3 here.

Given exact `art_6d4c9985`, when this separate base is reviewed, then the composition
file remains byte-for-byte equal to SHA-256
`d24bd92d60203e17137870b275ef766c4e67c10e0368d747df5bd90dad9a9fa7`. No test may
claim F7 A7 or a v8 implementation gate passed until a later reviewed composition commit
incorporates this base's exact object names, DDL owners, mutation owners, source owners,
revision transitions, snapshot seam, named snapshot-error disposition, and acceptance
fixtures.

Given an absent token, unknown state, expired fact, or mismatched member, when the R2
consumer runs, then it follows F7's existing unknown-ability wake path. The base creates
no probe, prediction, sibling alias, reroute, retry, or second lifecycle to fill the gap.

## Open Questions

None. The owner commissioned this separate base through
`dr_99628605-cb7a-44b4-a509-d46b8e7f4ffd=commission_r2_fact_base`.

Independent review of this exact file is required before any incorporation ruling. The
composition successor remains the authority for whether and how these reviewed objects
enter its v8 transaction. That dependency is a gate, not an unanswered design choice in
this base.
