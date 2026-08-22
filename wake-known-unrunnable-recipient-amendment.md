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
- **Authoritative local fact**: a typed local record that names the affected execution
  identity, its cause, its principal, and its validity. A fact is current when it has no
  expiry or when its expiry is later than the transaction clock.
- **Known-unrunnable target**: the exact resolved session has one current authoritative
  local fact in the closed precondition set in R2.
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
check must examine the exact resolved session and its execution tuple.

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

The gateway must derive each precondition from its matching current authoritative local
fact. `quota_exhausted` requires a typed, unexpired local exhaustion fact. A rate or
quota error string is not that fact.

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

The successor shape must contain this amendment-owned conflict table:

```sql
CREATE TABLE wake_known_unrunnable_migration_conflicts (
  conflictId        TEXT PRIMARY KEY CHECK (length(conflictId) > 0),
  predecessorShape  TEXT NOT NULL CHECK (length(predecessorShape) > 0),
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

The schema registry must own the table and both triggers. If the sibling v4 registry is
present, the combined registry must add these three records without changing the
sibling `wake_migration_conflicts` table or assigning this amendment's reason to that
table. The pre-boot schema gate must verify the registered table and both append-only
triggers before it evaluates conflict rows.

If trusted routing cannot be derived, the migration transaction must copy the legacy
wake and public terminal without changing their stored values. It must insert one
conflict row with deterministic
`conflictId='wake-routing:<wakeId>:terminal:<sourceTerminalId>'`,
`causeId='terminal:<sourceTerminalId>'`, and the migration clock as `recordedAt`. It must
create no notice, message, notice cursor, carrier, route, or sibling-ledger row for that
wake.

`sourceTerminalId` must equal the exact stored `terminalOutcomeId` rendered in its
canonical text form. `predecessorShape` must equal the exact predecessor registry stamp
observed by that migration transaction. The transaction must use those stored values in
the conflict ID and cause ID without parsing or normalizing prose.

The migration transaction must commit the successor schema and stamp, copied source
rows, and conflict row together. After that commit, the pre-boot schema gate must return
`wake_migration_conflict` with `conflictId`, `wakeId`, `sourceTerminalId`, and `reason`.
The gate must start no Gateway, Wakes, publisher, Bubble, or session-lane consumer. The
error must omit any untrusted sender or recipient value.

A restart against the committed conflict must return the same error and change no row.
The unique conflict identity must prevent a second record. This amendment authorizes no
automatic repair. An operator can restore the predecessor backup with corrected trusted
identity and rerun the migration; the migration must then use the normal trusted-routing
path. A failure before the conflict transaction commits must roll back the successor
schema, copied rows, conflict row, and stamp together.

An accepted wake that has no carrier at upgrade remains eligible for the R4 act-edge
check. An admitted carrier remains eligible only for R5. Migration and boot recovery
must use the same deterministic terminal and notice identities, so a second run reads
the first result and creates no duplicate.

## Architecture

The gateway composes the new guard with the existing lifecycle:

1. Resolve the target through the current direct or role-fallback path.
2. Read the closed local fact sources inside the scheduling transaction.
3. Return R3 when a current fact proves inability.
4. Otherwise, run the existing wake insertion path.
5. At the act edge, first claim and preserve the ordinary, condition-match, or fallback
   trigger under R4, then repeat steps 1 and 2 against current facts.
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
R8's append-only migration-conflict table and pre-boot conflict gate.

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

### A2. Unknown or expired evidence does not refuse

Given no current authoritative inability fact, when the sender sends a wake, then the
gateway performs no provider or process probe and continues through the existing wake
path.

Given an expired quota fact or untyped provider error prose, when the sender sends a
wake, then the gateway does not return `quota_exhausted` from that evidence.

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

Given trusted migrated routing for a legacy null-carrier result, when migration and boot
recovery each run twice, then the public result is `failed` with
`legacy_outcome_unknown`; the carrier remains null; one notice, one message identity,
and one notice cursor exist.

Given routing is not derivable, when migration runs, then it preserves the legacy wake
and public terminal values, commits one
`wake_known_unrunnable_migration_conflicts` row with the deterministic conflict ID,
reason `trusted_sender_routing_unknown`, cause `legacy_import`, exact terminal cause ID,
exact predecessor stamp, null prior carrier, migration time, and `process:tightbeam`
principal, and creates no notice, message, cursor, carrier, route, or sibling-ledger row.
The successor stamp and conflict commit together. The pre-boot gate verifies the
registered table and triggers, returns `wake_migration_conflict` with the four R8
identifiers, and starts no database consumer.

Given that committed conflict, when startup runs twice, then both runs return the same
error and the database still contains one conflict row and unchanged copied source rows.
Given an injected failure before the conflict transaction commits, when migration exits,
then it retains the predecessor stamp and rows and contains no successor conflict table
or row. Given the operator restores a predecessor backup whose structured identity now
proves trusted routing, when migration runs, then it creates the normal legacy terminal
notice and no conflict row.

## Open Questions

None. A new precondition, external health probe, alternate recipient, automatic retry,
or rerouting rule requires a separate reviewed amendment.
