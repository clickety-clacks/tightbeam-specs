# Bug A amendment: known-unrunnable wake recipients

Status: FROZEN FOR FRESH INDEPENDENT REVIEW

Date: 2026-08-18 UTC

Assignment: `asg_0c4356a4-29af-4c18-95c1-c2f1db2ba8d1`

Work items:

- this amendment serves `wi_c01e8f20-3f77-434f-a124-f006278c4ff6`;
- it extends Bug A on `wi_113d569f-7aff-412b-aec3-0c21f2e87f40`.

Reviewed base: `art_aac9cafc`, SHA-256
`a8fc963dd141721df2253a52644a60da7f9ef8792579518f7d65a3377829a990`,
reviewed-clean in `att_cb9a06bc-3ad3-4d6f-818e-8e78c51616b9`.

Independent review `asg_6089b268-2884-42a5-8dfd-93fc8447611a` returned
changes-requested verdict `att_3e944294-55a5-4704-9869-c5a4cf10c68d`. This
revision closes its two blocking findings: the null-carrier public terminal is
reconciled with the proposed parent ledger, and condition-match or fallback
settlement preserves its trigger evidence before terminalization.

Fresh stronger-model review `asg_48c2d18c-3870-4df8-b34b-de148f340979` returned
changes-requested verdict `att_05ec4a67-6384-446a-bd3c-6bfbfef88496` and report
`art_f1c994e5`, SHA-256
`bb1a10e4a62c7a9d6b09ef9097370fe1fd55be5cb9eb9f48154239e599994b9f`. It found
three blocking gaps: R4 omitted an accepted immediate wake at the act edge; R7's
authorized projections and forbidden request fields lacked acceptance proof; and the
trusted-routing migration conflict lacked a durable record and retry contract. This
revision closes those gaps in R4, R7-R8, the Architecture, and A4, A6-A7.

Fresh stronger-model review `asg_aac50476-4f35-42dc-9726-05f8ca153858`
returned changes-requested verdict
`att_043f1725-f43e-4019-b8f8-9a6e85812fed` and report `art_0bb1ed5f`,
SHA-256 `5930e096e58f2b5f1c9074f547bdcfcf22407ffc7858d6e2b4e10fcc8c854251`.
It found three blocking gaps: the fact match did not bind an exact execution identity;
the amendment did not define a stamped transition from the sibling v4 shape; and A7
required a push message for stream-only notices. This revision closes those gaps in
the Terms, R1-R2, R8, the Architecture, and A1, A2, and A7.

## Spec identity and authority

The canonical identity is
`tightbeam-specs/wake-known-unrunnable-recipient-amendment.md`. Assignment
`asg_0c4356a4-29af-4c18-95c1-c2f1db2ba8d1` owns its revisions. Each review and
handoff must bind this file by its SHA-256 digest and containing commit.

The reviewed base `art_aac9cafc` and the final F2 ruling control the public terminal
contract. The proposed sibling `wake-delivery-conservation.md` does not override that
contract while its producer assignment remains open. If both specifications reach
handoff, the integration table in R8 is binding: an implementation must not combine
the sibling's non-null `failed.turnSeq` constraint with this amendment's accepted
null-carrier failure.

Controlling sequencing: `att_a034fbd6-2542-4404-8fa5-f22a3ffa7be5`.
Historical partial implementation pointer `art_7409e650` remains integrity and custody
evidence only. Its missing bytes are not current source authority.

This amendment changes design only. It authorizes no implementation, source edit,
release-line work, provider probe, credential access, wake experiment, deployment,
runtime mutation, or work-item disposition.

## Goal

Tightbeam must reject a wake request when authoritative local facts already prove that
the exact resolved target cannot attempt a turn.

If Tightbeam accepts a wake and the target becomes unable to run before or after carrier
admission, the existing Bug A terminal lifecycle must settle the wake and create exactly
one sender notice. Retirement, carrier failure, and known pre-admission inability are
three causes in that one lifecycle.

The sender must receive one of two visible results:

1. a synchronous `target_known_unrunnable` refusal before Tightbeam accepts the wake; or
2. the reviewed `delivered | failed | canceled` terminal result and its existing sender
   notice after Tightbeam accepts the wake.

## Non-Goals

- Do not call a provider, adapter, ACP endpoint, harness process, or credential service
  to decide whether to accept a wake.
- Do not predict quota exhaustion or treat an unknown quota state as exhaustion.
- Do not parse provider prose, error prose, prompts, role labels, or prior failed turns
  to derive a precondition.
- Do not add a fourth public terminal value, a second notice table, or a third delivery
  workflow.
- Do not spawn, reassign, rebind, reroute, retry, or choose another agent after the
  normal target-resolution path returns an exact target.
- Do not change role fallback, condition wakes, delayed wakes, cancellation authority,
  sender-notice authorization, or Bubble routing.
- Do not reopen the reviewed Bug B process-custody contract.
- Do not absorb implementation or 0.1.8 release scope.

## Terms

- **Send check**: the deterministic check after normal target resolution and before the
  scheduling transaction inserts a wake row.
- **Act-edge check**: the same check after normal delivery-time target resolution and
  before an accepted wake admits a carrier turn.
- **Execution selection**: the exact tuple
  `{sessionKey, sessionUpdatedAt, host, harness, provider, modelFamily, modelContext,
  effort}` read inside the checking transaction. A null model context or effort is an
  exact tuple value; it is not a wildcard.
- **Adapter token**: the exact tuple
  `{{harnessId, "shared", host}, adapterGeneration, adapterRevision}` read from the
  adapter coordinator for the execution selection. It is valid only when both numeric
  revisions identify the currently registered adapter instance.
- **Harness-catalog token**: the exact tuple
  `{host, harness, provider, catalogRevision}` read from the local catalog registry.
- **Credential token**: the exact tuple
  `{host, harness, provider, credentialSlotId, credentialRevision}` read from the local
  credential registry. `credentialSlotId` is an opaque local identifier. A refusal or
  projection must not expose it.
- **Authoritative local fact**: a typed local record with `factId`, `factKind`,
  `matchKey`, `principal`, `observedAt`, and optional `expiresAt`. The fact writer must
  advance each registry revision named in `matchKey` whenever that registry state
  changes. A fact is current only when each named revision equals the revision read by
  the checking transaction and `expiresAt` is null or later than the transaction clock.
- **Exact fact match**: member-for-member equality between a fact's complete typed
  `matchKey` and the cause-specific key that R2 constructs from the current execution
  selection and local registry tokens inside the same transaction. Text compares by
  exact stored bytes, integers compare by value, and null compares only with null. The
  check performs no case folding, alias expansion, or default substitution. A missing
  key member, stale revision, or different tuple member is not a match.
- **Known-unrunnable target**: the exact resolved session has one current authoritative
  local fact with an exact fact match in the closed precondition set in R2.
- **Unknown ability**: no current authoritative local fact proves inability. Unknown
  ability is not a refusal condition.
- **Pre-admission failure**: Tightbeam accepted a wake earlier, but the act-edge check
  proves inability before a carrier exists.
- **Late carrier failure**: an admitted carrier reaches the reviewed `failed` or
  `canceled` terminal path.
- **Sender notice**: the reviewed `wake_sender_notices` row whose recipient is the stored
  authenticated sender principal. This amendment adds no notice recipient.
- **Routing migration conflict**: one durable
  `wake_known_unrunnable_migration_conflicts` row that preserves the identity of a
  legacy null-carrier terminal for which migration cannot derive trusted sender routing.

## Assumptions

1. The reviewed base remains authoritative for public terminal values, identical-principal
   notice routing, authorization, outbox recovery, and exactly-once notice identity.
2. The final F2 ruling keeps the public terminal set exactly
   `delivered | failed | canceled`. A legacy null-carrier result maps to `failed` with
   `failureClass=legacy_outcome_unknown`, trusted migrated sender and routing identity,
   and one notice. The design creates no fabricated carrier and no absent
   attempt/admitted/handled/undeliverable ledger.
   Direct source: product-owner ruling wake `w_da8051d5`, issued by owner session
   `s_fde9b2be`. Its exact ruling is also carried without alteration in sole Bug A
   implementation assignment `asg_e7556f25-d909-42f1-ba89-68e1714e6cef`.
3. Normal resolution returns one exact session after it applies the existing direct,
   role-fallback, and owner-Main rules.
4. The gateway can read current session, hold, circuit, harness, ACP, adapter,
   credential-presence, and typed quota facts without an external call.
5. The 2026-08-18 specimen records session `s_f63d31e5`, twelve failed turns, and lost
   wakes `w_45faa8a8` and `w_a2a13028`. The specimen motivates this amendment. It does
   not authorize a live replay or provider probe.
6. Existing request idempotency, terminal compare-and-set behavior, deterministic notice
   identity, and publisher recovery remain available.

## Invariants

### R1. Resolve before checking

The gateway must run the existing target-resolution path before the send check. The
check must construct the execution selection for the exact resolved session. The
act-edge check must construct a new selection instead of reusing the send-check
selection.

For a role target, the gateway must preserve the existing fallback result. The check
must not search for another holder after that result.

### R2. Use a closed, typed precondition set

The send check and act-edge check may return only these preconditions, in this priority
order:

1. `session_retired`;
2. `session_held`;
3. `circuit_open`;
4. `adapter_unavailable`;
5. `acp_unavailable`;
6. `harness_unavailable`;
7. `credential_missing`;
8. `quota_exhausted`.

The check must build and compare these complete match keys:

| Precondition | Required current local state | Exact `matchKey` |
|---|---|---|
| `session_retired` | retired session-state fact | `{executionSelection}` |
| `session_held` | active session-hold fact | `{executionSelection, holdId, holdRevision}` |
| `circuit_open` | open adapter-circuit fact | `{executionSelection, adapterToken, circuitId, circuitRevision}` |
| `adapter_unavailable` | unavailable adapter-instance fact | `{executionSelection, adapterToken}` |
| `acp_unavailable` | unavailable ACP-instance fact | `{executionSelection, adapterToken}` |
| `harness_unavailable` | unavailable selected-harness fact | `{executionSelection, harnessCatalogToken}` |
| `credential_missing` | missing selected-credential fact | `{executionSelection, credentialToken}` |
| `quota_exhausted` | typed, unexpired quota-window fact | `{executionSelection, credentialToken, quotaWindowId, quotaWindowRevision}` |

Each ID and revision in this table is an opaque typed field from its named local
registry. The registry must change the revision when its state changes, even when the
new state later returns to the same value. The check must treat an unavailable token or
revision as unknown ability and continue through the existing wake path.

The gateway must derive a precondition only from a current authoritative local fact
whose `factKind` equals that precondition and whose full key equals the constructed key.
A fact for the same session but an earlier session update, adapter generation, catalog
revision, credential revision, quota window, harness, provider, model, context, effort,
or host is not a match.
`quota_exhausted` requires the typed, unexpired local exhaustion fact in the table. A
rate or quota error string is not that fact.

If several preconditions are current, the gateway must return the first value in the
priority order. This makes replay and audit comparison deterministic.

### R3. Reject before accepting

When the send check finds a precondition, the gateway must return:

```text
{
  error: "target_known_unrunnable",
  targetSessionKey,
  precondition,
  evidenceRef
}
```

`evidenceRef` must name the authoritative local fact. It must not expose a credential,
account identifier, provider response, quota amount, or secret.

The scheduling transaction must insert no wake, prompt message, carrier turn, terminal
outcome, or sender notice for this refusal. The authenticated caller receives the
refusal directly. Existing request audit may retain the stable error, target,
precondition, and evidence reference.

### R4. Settle each accepted wake at its act edge

Each accepted ordinary prompt wake, including an immediate or delayed wake, and each
accepted condition wake must pass through the same Wakes act-edge transaction before it
admits a carrier. The transaction may follow the scheduling transaction immediately or
run later. The wake retains its existing due-time, condition, fallback, cancellation,
and role-resolution semantics.

At its act edge, one Wakes transaction must use this order:

1. Load the accepted wake and select its eligible trigger. An immediate ordinary wake is
   eligible at its accepted timestamp. A delayed ordinary wake is eligible at its due
   time. A condition wake is eligible through a matching fact or elapsed fallback.
2. Win the existing admission or trigger-claim compare-and-set. For a condition match or
   fallback, write
   its existing `firedBy` value and lifecycle provenance. A matched condition must retain
   the condition kind, scope, fact identity, and fact timestamp already used by that
   lifecycle. A fallback must retain its fallback deadline. A losing trigger writes
   nothing. An ordinary wake retains its existing ordinary trigger kind and accepted or
   due timestamp; it gains no condition or fallback provenance.
3. Resolve the target through the existing path and run the act-edge check.
4. If the check finds no precondition, continue through normal carrier admission.
5. If the check finds a precondition before a carrier exists, commit the ordinary
   admission or trigger claim, its applicable provenance, one public `failed` terminal
   result, and one sender notice together.

The step 5 public terminal must use a null carrier sequence,
`causeKind=target_known_unrunnable`, the R2 precondition as its typed failure class, the
exact resolved target session, the authoritative evidence reference, and
`principal=process:tightbeam`. The transaction must not fabricate a carrier.
This result is final and retry-ineligible. A later runnable fact does not reopen it; the
sender may submit a new wake.

The public terminal result is the reviewed `delivered | failed | canceled` record. It
is not a `wake_delivery_outcomes(kind='failed')` row from the proposed sibling ledger.
That proposed row requires a carrier sequence and therefore cannot represent this
cause. No `attempt`, `admitted`, `handled`, or `undeliverable` row is created.

### R5. Settle admitted carrier failures through the reviewed path

If retirement cancels an admitted queued carrier, the terminal outcome remains
`canceled` with cause `session_retired`.

If an admitted carrier cannot run or terminates failed, the terminal outcome remains
`failed` with its typed cause and failure class.

The carrier terminal transaction must insert or read the existing deterministic sender
notice. A later precondition recognizer, Bubble pass, publisher pass, restart pass, or
supervision pass must not create another logical notice.

### R6. Preserve exactly-once settlement

One accepted wake must have one public terminal result. One terminal result must have
one logical sender notice for the stored authenticated sender principal.

The ordinary admission or trigger claim, terminal result, and notice must commit together
when R4 applies.
The notice must keep the reviewed deterministic identity for the tuple of accepted wake,
public terminal result, and stored authenticated sender principal. Its durable row must
link that terminal result and wake. Transaction replay must return the same terminal and
notice identities. Publisher replay may redeliver transport, but it must not create a
second durable message or notice.

The synchronous R3 refusal is not an accepted wake and therefore has no terminal outcome
or sender notice.

### R7. Preserve authority and neutral output

The gateway must return `wake_derived_field_forbidden` when a request supplies a
precondition, evidence reference, sender, recipient, push session, target substitution,
or terminal value. It must return that error before target resolution and insert no wake,
message, carrier, terminal, notice, route, or evidence row.

The refusal response and terminal projections must reveal only the exact target, the
neutral precondition code, and an authorized evidence reference. Existing `wake-get`,
`wake-notices`, work-item trace, sender-owner, process, and administrator authorization
rules remain controlling.

For an R4 result, `wake-get` and the work-item trace must project public terminal
`failed`, a null carrier, `target_known_unrunnable`, the R2 failure class, the exact
target, the authorized evidence reference, and the winning trigger provenance. They
must not project a sibling-ledger `attempt`, `failed`, or `undeliverable` event.
`wake-notices` must return the one linked sender notice.

Bubble and boot recovery must consume the committed public terminal and linked notice.
They must not require or synthesize a `wake_delivery_outcomes` cursor entry. Bubble may
publish the committed notice through the reviewed outbox path; it must not create a
second notice or start a second logical failure climb.

### R8. Integrate and migrate without inventing a ledger

The public terminal enum and existing terminal rows remain unchanged. The durable cause
vocabulary gains `target_known_unrunnable`; the typed failure-class vocabulary gains the
R2 values for runtime rows.

This table is normative:

| Case | Public terminal record | Carrier link | Proposed sibling ledger | Notice |
|---|---|---|---|---|
| synchronous R3 refusal | none | none | none | none |
| accepted wake, R4 known-unrunnable before carrier | `failed`, class from R2 | null | no row | one deterministic sender notice |
| admitted carrier failure | `failed`, reviewed carrier class | exact carrier | any separately approved carrier ledger may link the carrier | same reviewed notice identity |
| retirement cancels admitted queued carrier | `canceled`, `session_retired` | exact carrier | any separately approved carrier ledger may link the carrier | same reviewed notice identity |
| legacy null-carrier terminal | `failed`, `legacy_outcome_unknown` | null | no row | one notice from trusted migrated routing |

The sibling proposal's `CHECK (kind NOT IN ('admitted','handled','failed') OR turnSeq IS
NOT NULL)` remains valid for its carrier ledger because this amendment writes no row to
that ledger. A build must not project the R4 public failure into that ledger, relax its
carrier-integrity constraint, or create an `undeliverable` substitute. If a branch
already added the proposed table, migration must leave it unchanged and empty for every
R4 or legacy null-carrier result.

Migration must preserve every existing wake, public terminal result, notice, sender and
recipient principal, notice cursor, message identity, cause, and carrier link. It must
not reinterpret an old failure from prose. It may map a legacy null-carrier terminal
only through the F2 rule: `failed`, `legacy_outcome_unknown`, trusted migrated sender and
routing identity, and one deterministic notice.

The trusted-routing path must apply the reviewed sender-notice rules without adding a
new cursor or publication rule. The notice row's `noticeSeq` is its one stream cursor.
A user, process, or session without a validated same-session `pushSessionKey` must use
`deliveryMode='stream'`, `state='stream_ready'`, and null `messageId`. Only a failed
notice whose stored session sender, recipient, and `pushSessionKey` are the same session
may use `deliveryMode='push'` and `state='pending_push'`. The normal publisher is the
only writer that may create its deterministic push message and change it to `pushed`.

The successor shape must contain this amendment-owned conflict table:

```sql
CREATE TABLE wake_known_unrunnable_migration_conflicts (
  conflictId        TEXT PRIMARY KEY CHECK (length(conflictId) > 0),
  predecessorShape  TEXT NOT NULL
                      CHECK (predecessorShape IN
                        ('coordination-fabric-v1-phase1-v3',
                         'coordination-fabric-v1-phase1-v4')),
  wakeId            TEXT NOT NULL CHECK (length(wakeId) > 0),
  sourceTerminalId  TEXT NOT NULL CHECK (length(sourceTerminalId) > 0),
  reason            TEXT NOT NULL
                      CHECK (reason = 'trusted_sender_routing_unknown'),
  causeKind         TEXT NOT NULL CHECK (causeKind = 'legacy_import'),
  causeId           TEXT NOT NULL CHECK (length(causeId) > 0),
  priorTerminalKind TEXT NOT NULL CHECK (priorTerminalKind = 'failed'),
  priorCarrierSeq   INTEGER NULL CHECK (priorCarrierSeq IS NULL),
  recordedAt        INTEGER NOT NULL CHECK (recordedAt >= 0),
  principal         TEXT NOT NULL CHECK (principal = 'process:tightbeam'),
  UNIQUE (wakeId, sourceTerminalId, reason)
);

CREATE TRIGGER wake_known_unrunnable_conflicts_no_update
BEFORE UPDATE ON wake_known_unrunnable_migration_conflicts
BEGIN
  SELECT RAISE(ABORT, 'wake migration conflicts are append-only');
END;

CREATE TRIGGER wake_known_unrunnable_conflicts_no_delete
BEFORE DELETE ON wake_known_unrunnable_migration_conflicts
BEGIN
  SELECT RAISE(ABORT, 'wake migration conflicts are append-only');
END;
```

The combined successor stamp is
`coordination-fabric-v1-phase1-v5-known-unrunnable`. The implementation must expose one
complete ordered `Schema.known_unrunnable_successor_registry/0`. That registry is the
only DDL authority for a clean v5 bootstrap, each supported transition, v5
validation, and the source census. It must contain one v5 record for each object name
owned by the sibling v4 registry, plus the amendment-owned table and both triggers. A
record unaffected by this amendment must keep the sibling v4 normalized SQL and
dependencies byte-for-byte. A record that owns a cause or failure-class check must
replace that SQL with the v5 check from this amendment. Each record must retain the
sibling registry shape `{owner, type, name, sql, dependsOn}`.

The v5 registry must preserve the sibling `wake_migration_conflicts` table and its
records without assigning this amendment's conflict reason to that table. It must own
`wake_known_unrunnable_migration_conflicts` and both append-only triggers as three
separate records. The product must contain no second DDL string for a v5-owned object.

The pre-boot shape gate must select exactly one of these paths from the durable stamp:

1. An empty new database creates the complete v5 registry and writes the v5 stamp in
   one transaction.
2. An exact `coordination-fabric-v1-phase1-v3` database acquires exclusive custody,
   rechecks that one v3 stamp remains, and runs the sibling R18 mapping and this
   amendment's mapping in that transaction. It must not commit an intermediate v4 stamp
   or v4 row shape.
3. An exact `coordination-fabric-v1-phase1-v4` database acquires exclusive custody,
   rechecks that one v4 stamp remains, and validates the complete normalized sibling v4
   registry without mutation. It then runs this amendment's v4-to-v5 mapping in that
   transaction.
4. An exact v5 database validates the complete normalized v5 registry without DDL or
   row mutation.

A non-empty database with no stamp, multiple stamps, or another stamp must return
`ShapeError`. It must run no successor DDL and start no database consumer.

Both transition paths must load the v5 registry, reject a missing, duplicate,
mismatched, or dependency-unreachable record, and compute the complete dependency
closure before they alter a row. The v3 path must apply the sibling's closed v3 mapping
before it applies this amendment's legacy terminal and trusted-routing rules to the
copied successors. The v4 path must preserve the already normalized sibling rows and
apply only this amendment's added columns, checks, vocabulary, conflict records, and
trusted-routing mapping. Both paths must use structured columns and deterministic IDs;
they must not parse stored prose.

Before either path changes the stamp, it must compare each normalized `sqlite_master`
object with the v5 registry, require an empty `PRAGMA foreign_key_check`, and require an
`ok` `PRAGMA integrity_check`. The stamp change to v5 is the transaction's final
mutation. A failure during DDL, copy, normalization, conflict creation, object
validation, either integrity check, or the stamp update must roll back to the exact v3
or v4 predecessor stamp, rows, and objects. After commit, immediate validation and a
clean restart must perform read-only v5 validation.

The pre-boot schema gate must verify the registered amendment table and both append-only
triggers before it evaluates conflict rows.

If trusted routing cannot be derived, the selected migration transaction must copy the
legacy wake and public terminal without changing their stored values. It must insert
one conflict row with deterministic
`conflictId='wake-routing:<wakeId>:terminal:<sourceTerminalId>'`,
`causeId='terminal:<sourceTerminalId>'`, and the migration clock as `recordedAt`. It
must create no notice, message, carrier, route, or sibling-ledger row for that wake.

`sourceTerminalId` must equal the exact stored `terminalOutcomeId` rendered in its
canonical text form. `predecessorShape` must equal the exact predecessor registry stamp
observed by that migration transaction. The transaction must use those stored values in
the conflict ID and cause ID without parsing or normalizing prose.

The migration transaction must commit the v5 schema and stamp, copied source rows, and
conflict row together. After that commit, the pre-boot schema gate must return
`wake_migration_conflict` with `conflictId`, `wakeId`, `sourceTerminalId`, and `reason`.
The gate must start no Gateway, Wakes, publisher, Bubble, or session-lane consumer. The
error must omit any untrusted sender or recipient value.

A restart against the committed conflict must return the same error and change no row.
The unique conflict identity must prevent a second record. This amendment authorizes no
automatic repair. An operator can restore the exact v3 or v4 predecessor backup with
corrected trusted identity and rerun the selected migration; the migration must then use
the normal trusted-routing path. A failure before the conflict transaction commits must
preserve that predecessor's stamp, schema, rows, and objects and leave no v5 conflict
table or row.

An accepted wake that has no carrier at upgrade remains eligible for the R4 act-edge
check. An admitted carrier remains eligible only for R5. Migration and boot recovery
must use the same deterministic terminal and notice identities, so a second run reads
the first result and creates no duplicate.

## Architecture

The gateway composes the new guard with the existing lifecycle:

1. Resolve the target through the current direct or role-fallback path.
2. Construct the R1 execution selection and the R2 cause-specific key from current
   local rows inside the scheduling transaction.
3. Return R3 only when one current fact's complete key equals that constructed key.
4. Otherwise, run the existing wake insertion path.
5. At the act edge, first claim and preserve the ordinary, condition-match, or fallback
   trigger under R4, then repeat steps 1 and 2 from new current reads.
6. Commit the R4 trigger evidence, null-carrier public `failed` result, and notice, or
   admit the carrier through the reviewed admission path.
7. After carrier admission, use only the reviewed `delivered | failed | canceled`
   terminal and notice path.

Traceability is explicit in both directions:

| Requirement | Architecture source | Acceptance evidence |
|---|---|---|
| R1 | Steps 1 and 5 | A1 and A3 |
| R2 | Steps 2 and 5; response schema | A1, A2, and A4 |
| R3 | Step 3; response schema | A1 and A2 |
| R4 | Steps 4 through 6; Wakes transaction owner | A4 |
| R5 | Step 7; terminal and notice path | A5 |
| R6 | Steps 6 and 7; Wakes transaction owner and publisher | A4 and A5 |
| R7 | Response schema and existing authorization projections | A6 |
| R8 | Durable integration and migration contract | A6 and A7 |

The Wakes transaction owner remains the only writer for accepted-wake terminal outcomes
and sender notices. The normal publisher remains the only failed-or-canceled push
writer. Bubble may reference the committed notice and must not publish a second sender
message.

The response schema adds only `target_known_unrunnable` and its closed precondition.
The durable schema extends existing cause and failure-class checks. It adds no wake
attempt ledger, retry scheduler, alternate recipient, or provider-health probe. It adds
R8's append-only migration-conflict table, v5 registry and stamp, two exact predecessor
transitions, and pre-boot conflict gate. `Schema.known_unrunnable_successor_registry/0`
is the shared source for clean bootstrap, both migrations, validation, and the source
census.

After implementation passes acceptance, CLI help and the operating manual must state:

- a send may return `target_known_unrunnable` from current local facts;
- an accepted wake reports later failure through `wake-get` and `wake-notices`;
- the sender decides whether to send a new wake.

No guidance may promise predictive quota knowledge or automatic rerouting.

## Acceptance

### A1. Immediate known inability rejects at send

Given one fixture for each R2 precondition on exact session `S`, when an authorized
sender sends an immediate wake to `S`, then the response is
`target_known_unrunnable`, names `S`, names the expected precondition and evidence
reference, and creates no wake, message, carrier, terminal outcome, or sender notice.

Given two current facts, when the same request runs, then the response uses R2 priority.
An idempotent replay returns the same refusal while the same fact remains authoritative.

Given one current matching fact for each R2 row, when the fixture changes only one key
member before the check, then the old fact does not refuse the request. The fixture must
exercise a changed session update, host, harness, provider, model family, model context,
effort, adapter generation, adapter revision, catalog revision, credential revision,
quota-window revision, hold revision, and circuit revision. It must also exercise a
fact whose session key differs from the resolved session and a fact whose `factKind`
differs from the precondition under test. Each case continues through the existing wake
path unless another exact fact matches.

### A2. Unknown or expired evidence does not refuse

Given no current authoritative inability fact, when the sender sends a wake, then the
gateway performs no provider or process probe and continues through the existing wake
path.

Given an expired quota fact or untyped provider error prose, when the sender sends a
wake, then the gateway does not return `quota_exhausted` from that evidence.

Given a current fact whose required adapter, catalog, credential, hold, circuit, or
quota token cannot be read, when the sender sends a wake, then the gateway treats the
ability as unknown and continues through the existing wake path. It does not probe an
adapter, harness, provider, or credential service to fill the missing token.

### A3. Role fallback stays authoritative

Given a role whose existing fallback resolves to session `S`, when `S` has a current R2
fact, then the refusal names `S`. The gateway does not spawn, reassign, choose a second
session, or mutate the role.

Given a role whose existing fallback resolves to runnable or unknown session `T`, when
the sender sends a wake, then the existing path targets `T` unchanged.

### A4. Accepted wake fails before carrier admission

Given an immediate ordinary wake passes the send check, when a transaction barrier holds
its Wakes act edge until after the exact target gains a current R2 fact, then the resumed
act-edge transaction commits one public `failed` result with a null carrier and one
sender notice. It creates no carrier or sibling-ledger row. Releasing the same barrier
without a new R2 fact admits the ordinary carrier through the existing path.

Given an accepted delayed ordinary wake with no carrier, when its resolved target gains
a current `quota_exhausted`, `session_retired`, or unavailable-execution fact before the
act edge, then the act-edge transaction commits one public `failed` result with a null
carrier, one typed cause, and one sender notice. It creates no carrier or sibling-ledger
row.

Given one matching condition fact and one condition wake whose target is known
unrunnable, when the act edge runs, then the same transaction commits
`firedBy='condition'`, the matched condition kind, scope, fact identity and timestamp,
the null-carrier `failed` result, and one notice. A replay returns the same identities.

Given an elapsed fallback and no matching condition fact, when the same target is known
unrunnable, then the transaction commits `firedBy='fallback'`, the fallback deadline,
the null-carrier `failed` result, and one notice. A later condition fact does not replace
the winning trigger.

Given a condition match and fallback become eligible concurrently, when both workers
race, then one existing trigger-claim compare-and-set wins. The loser commits no trigger
provenance, terminal result, or notice.

When the terminal transaction, publisher, Bubble recognizer, and boot recovery each run
twice, then the wake still has one terminal outcome, one notice, and at most one durable
push message.

### A5. Carrier failure and retirement use the same notice lifecycle

Given an admitted carrier that fails before it can run, when its terminal transaction
commits, then the wake reaches public `failed` and creates one existing sender notice.

Given retirement cancels an admitted queued carrier, when the retirement transaction
commits, then the wake reaches public `canceled` with `session_retired` and creates one
existing sender notice.

Given either terminal already exists, when a local inability fact is later recognized,
then no second terminal outcome or sender notice is created.

### A6. Specimen, authorization, and compatibility

Given a fixture modeled on session `s_f63d31e5` with a current typed weekly
`quota_exhausted` fact, when the two historical prompt shapes are submitted as new test
requests, then each request receives the R3 refusal and no accepted wake disappears.
The test does not contact a provider and does not replay `w_45faa8a8` or `w_a2a13028`.

Given an unauthorized reader, when it requests another principal's refusal evidence,
terminal outcome, or notice, then existing authorization returns `denied` without
revealing credential or quota details.

Given one R4 fixture for each stored sender kind `user`, `session`, and `process`, when
the exact stored sender reads `wake-get`, the linked work-item trace, and `wake-notices`,
then `wake-get` and the trace each return the same wake ID, public terminal `failed`, null
carrier, cause `target_known_unrunnable`, R2 failure class, exact target, authorized
evidence reference, and winning ordinary, condition, or fallback provenance. Neither
projection returns an `attempt`, sibling-ledger `failed`, or `undeliverable` event.
`wake-notices` returns one row whose wake and terminal IDs match those projections and
whose sender and recipient equal the stored authenticated sender. The row's target,
cause, failure class, evidence reference, and trigger provenance match the terminal.

Given the same session-sender fixture, when its stored owner user and an administrator
read the three surfaces, then the existing authorization returns that same projection.
Given an unrelated user, session, or process principal, each surface returns `denied`
and reveals no terminal, evidence, trigger, sender, or recipient field.

Given one request for each caller-supplied precondition, evidence reference, sender,
recipient, push session, target substitution, and terminal value, when the gateway
validates the request, then it returns `wake_derived_field_forbidden` before target
resolution. Each fixture leaves the wake, message, carrier, terminal, notice, route, and
evidence-row counts unchanged.

Given pre-amendment terminal and notice fixtures, when migration runs twice, then their
public values, IDs, sender routing, notice cursors, messages, causes, and carrier links
remain byte-for-byte equal. No new notice, terminal, or carrier appears.

### A7. Null-carrier integration and recovery

Given a schema fixture that includes the proposed sibling `wake_delivery_outcomes`
table, when an R4 failure and a legacy null-carrier migration run, then each creates one
public `failed` result and one sender notice and creates no sibling-ledger row. The
table's non-null carrier constraint remains unchanged.

Given an empty database, when bootstrap runs, then it creates the complete normalized v5
registry and the one `coordination-fabric-v1-phase1-v5-known-unrunnable` stamp. Immediate
validation and a clean restart execute no DDL and leave every normalized object and row
equal. The registry enumeration equals the complete owned-object census and includes
the amendment table and its two triggers.

Given an exact v3-stamped fixture with one row for each sibling R18 mapping and each
amendment mapping, when startup runs, then it selects the direct v3-to-v5 plan and
commits one v5 stamp. The committed database contains the sibling normalizations, the
amendment vocabulary, and each lawful trusted-routing or conflict result. It never
contains a committed v4 stamp or intermediate v4 row shape.

Given an exact valid v4-stamped fixture with each amendment mapping, when startup runs,
then it first validates the complete v4 registry without mutation and commits one
v4-to-v5 transaction. The v5 database preserves each sibling v4 row and normalized
object except for the amendment-owned check, vocabulary, routing, and conflict changes.

Given either supported predecessor, when a fixture injects a failure during DDL, copy,
normalization, trusted-routing settlement, conflict creation, dependency creation,
normalized-object comparison, either integrity check, or the stamp change, then the
transaction preserves that exact predecessor stamp, rows, and objects and leaves no v5
object or row. Given a non-empty fixture with no stamp, multiple stamps, or another
stamp, startup returns `ShapeError`, runs no DDL, and starts no database consumer.

Given trusted user routing for a legacy null-carrier result, when migration and boot
recovery each run twice, then the public result is `failed` with
`legacy_outcome_unknown`; the carrier remains null; and one notice row has one stable
`noticeSeq`, `deliveryMode='stream'`, `state='stream_ready'`, and null
`pushSessionKey` and `messageId`. No durable push message exists.

Given trusted process routing for the same result, when migration and boot recovery each
run twice, then the notice has the same stream-only shape and remains readable through
exact process authority. No durable push message exists.

Given trusted session routing without a validated same-session push relation, when the
migration and boot recovery each run twice, then the notice has the same stream-only
shape and remains readable by the session and its stored owner. No durable push message
exists.

Given trusted session routing with a validated `pushSessionKey` equal to the stored
sender and recipient session, when migration commits, then the failed notice has
`deliveryMode='push'` and `state='pending_push'`. When the publisher and boot recovery
each run twice, then the notice reaches `state='pushed'`, stores the deterministic
`wake-notice:<noticeId>` message identity, and one durable message exists. Migration,
Bubble, and boot recovery do not create another message.

Given routing is not derivable, when migration runs, then it preserves the legacy wake
and public terminal values, commits one
`wake_known_unrunnable_migration_conflicts` row with the deterministic conflict ID,
reason `trusted_sender_routing_unknown`, cause `legacy_import`, exact terminal cause ID,
exact predecessor stamp, null prior carrier, migration time, and `process:tightbeam`
principal, and creates no notice, message, carrier, route, or sibling-ledger row. The v5
stamp and conflict commit together. The pre-boot gate verifies the registered table and
triggers, returns `wake_migration_conflict` with the four R8
identifiers, and starts no database consumer.

Given that committed conflict, when startup runs twice, then both runs return the same
error and the database still contains one conflict row and unchanged copied source rows.
Run this fixture once from v3 and once from v4; each conflict row names that exact
predecessor stamp. Given the operator restores the same predecessor backup whose
structured identity now proves trusted routing, when migration runs, then it creates the
normal legacy terminal notice and no conflict row.

## Open Questions

None. A new precondition, external health probe, alternate recipient, automatic retry,
or rerouting rule requires a separate reviewed amendment.
