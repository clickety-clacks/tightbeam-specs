# Bug A amendment: known-unrunnable wake recipients

Status: V7 COMPOSITION REVIEW CANDIDATE — IMPLEMENTATION BLOCKED ON COMMISSIONED R2 FACT BASE

Date: 2026-08-27 PT

Successor assignment: `asg_c59889f4-dbe4-4ac9-bb96-e605bcb525d1`

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

F7 producer `asg_c0c17c42-6298-47a0-8480-dfddf1675b10` added the five
one-member opaque-key mismatch fixtures authorized by
`dr_d5be052b-e0fb-471e-af14-3337dba2eadf`. Independent review
`asg_f798c849-32f2-4484-8e3e-4d7e9bf49a60` returned reviewed-clean verdict
`att_43f3bd21-bd5c-48b0-802a-981c6998f0dc` for artifact `art_9ee43d58`,
SHA-256 `e98c898f9bda0cef462e4a4d0bd9a0e10eff6cb810f9299f4fe7b7955694f2ef`,
at commit `da969ebe2f44258338ec4e60792fa1171689cd3b`.

Two implementation assignments then proved that the reviewed schema composition could
not apply to current main. `att_82f7e763-69dd-4a89-ac3b-2ec7d888ae45` and blocker
report `art_637121bf`, verified SHA-256
`c3da796a89b3a88f08b79e6e7a783ab4dc4e81b63c6e7d551ef844f24bdbc13e`, show that
main is already v7 and lacks the assumed Bug A terminal, `wake_sender_notices`, and
sibling-registry bases. Operator ruling
`dr_f99d1bc5-626c-44f9-b5c4-bd19e5060a6f=amend_and_review_spec` authorizes this
successor. This revision is limited to base and schema composition; it does not alter
reviewed R1-R7 or A1-A6.

Independent composition review `asg_c381f52a-423c-4607-b929-58aa828cf516`
returned changes-requested verdict
`att_66e4d5c8-0d05-4a03-b397-cf1b357a38b6` and report `art_4b9bb6f3`, SHA-256
`a3c9b98a534d1ce4b843fa216551c3ffac3ed3f35357513f8dca64a25fbc84c9`.
It proved that current v7 also lacks the R2 fact-and-revision base, that direct
`process:tightbeam` prompt wakes can have linked carriers without an accepted wake
event, and that the proposed migration conflict created a boot-wide hold with no
agent-reachable exit. This revision names the missing base as blocking, composes the
actual stored delivery-principal rule, and replaces the global hold with a per-wake
quarantine.

## Spec identity and authority

The canonical identity remains
`tightbeam-specs/wake-known-unrunnable-recipient-amendment.md`. Assignment
`asg_c59889f4-dbe4-4ac9-bb96-e605bcb525d1` owns this v7 composition successor.
Each review and handoff must bind this file by its SHA-256 digest and containing commit.

The reviewed base `art_aac9cafc` and the final F2 ruling control the public terminal
contract. Current main does not implement that base. R8 makes its Bug A terminal and
sender-notice slice an explicit part of this successor instead of assuming it exists.
Current main and the reviewed bases also do not define the R2 authoritative fact store,
registry revisions, or their writer transitions. This successor names that missing base
and blocks implementation; it does not invent it inside schema-composition text.
In preserved F7 clauses, “existing” or “pre-amendment” terminal and notice behavior
denotes that reviewed contract. It does not assert that current main already implements
the contract.
The proposed sibling `wake-delivery-conservation.md`, frozen as `art_b770c2f7`, does
not override that contract. The integration table in R8 remains binding: an
implementation must not combine the sibling's non-null `failed.turnSeq` constraint
with this amendment's accepted null-carrier failure.

Controlling sequencing: `att_a034fbd6-2542-4404-8fa5-f22a3ffa7be5`.
Historical partial implementation pointer `art_7409e650` remains integrity and custody
evidence only. Its missing bytes are not current source authority.

Operator request `dr_99628605-cb7a-44b4-a509-d46b8e7f4ffd` is ruled
`commission_r2_fact_base`. The ruling selects the missing-base path; it does not define
the base. This successor remains non-buildable until that commissioned authority exists,
passes independent review, and is incorporated here.

This successor changes design only. It authorizes no implementation, source edit,
release-line work, provider probe, credential access, wake experiment, deployment,
runtime mutation, or work-item disposition. R1-R7 and A1-A6 from reviewed F7 remain
unchanged. R8, the schema paragraph in Architecture, and A7 supersede only F7's stale
v3/v4-to-v5 schema composition, legacy-routing migration, and boot-conflict behavior.
The Terms and Assumptions ground those replacement clauses against current v7.

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

This sender-visible goal applies to wakes accepted by v8 and to v7 wakes whose trusted
routing and terminal shape are reconstructible. R8 preserves a v7 pre-carrier
cancellation without inventing a notice, and represents untrusted legacy routing as one
durable conflict instead of inventing a sender.

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
- **Missing R2 fact base**: the absent authority that must define the durable
  authoritative-fact object, each hold, circuit, adapter, catalog, credential, and quota
  registry token used by R2, the sole writer for each object, and the exact transition
  that advances each revision. Current main v7, reviewed Bug A, and reviewed F7 define
  none of those objects or writer transitions. This is a BLOCKING base, not an
  implementation detail or a sibling-registry alias.
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
- **Prompt wake**: a `wakes` row whose `consumer='prompt'`. Unqualified accepted-wake
  requirements in this amendment refer to prompt wakes. Internal consumer wakes are
  outside this amendment's terminal, notice, and migration-conflict scope. R8 separately
  names the legacy exceptions: it preserves a v7 pre-carrier cancellation without a new
  terminal, and represents a v7 prompt wake whose stored sender cannot be reconstructed
  by one migration-conflict row and no invented public terminal or notice.
- **Public wake terminal**: one `wake_terminal_outcomes` wake-level row whose closed
  terminal values are `delivered | failed | canceled`. It is separate from the current
  turn row and from the proposed sibling carrier ledger. Current main v7 has no such
  table or record.
- **Sender notice**: the required `wake_sender_notices` row whose recipient is the stored
  authenticated sender principal. This amendment adds no notice recipient. Current main
  v7 has no such table or `wake-notices` projection.
- **Current schema base**: Tightbeam main commit
  `d38cd7823511a4b6ee5bb3d8180a1628fcb2ac3b`, stamped
  `coordination-fabric-v1-phase1-v7`. `Schema.@schema_modules` orders the module-owned
  DDL. The shape gate carries exact v4-to-v5, v5-to-v6, and v6-to-v7 transitions.
- **Sibling carrier ledger**: the proposed `wake_delivery_outcomes` table in
  `art_b770c2f7`. Current main v7 does not contain this table, its migration-conflict
  table, or its normalized object registry. This successor does not make them a base.
- **V7 stored delivery principal**: the current delivery rule in
  `Gateway.wake_delivery_principal/1`: a non-empty `wakes.creatorSessionKey` denotes that
  exact session; otherwise the exact stored `wakes.origin` is the delivery principal.
  For migration, a fallback origin is trusted only when it is the reserved exact value
  `process:tightbeam`. User and session routing still require an accepted wake event or
  a validated creator session.
- **Routing migration conflict**: one durable
  `wake_known_unrunnable_migration_conflicts` row that quarantines one legacy prompt wake
  for which migration cannot derive trusted sender routing. It is a named final value,
  not a boot hold and not a public wake terminal.

## Assumptions

1. Current main commit `d38cd7823511a4b6ee5bb3d8180a1628fcb2ac3b` is the exact
   implementation base. Its `wakes.state='fired'` means admission. Its turn terminal is
   not a wake-level terminal. It has no `terminalOutcomeId`, `wake_sender_notices`,
   `wake-notices`, wake-notice publisher, sibling carrier ledger, or normalized sibling
   registry.
2. The reviewed Bug A base remains authoritative for public terminal values,
   identical-principal notice routing, authorization, outbox recovery, and exactly-once
   notice identity. This successor must add that missing slice in the same v7-to-v8
   successor that adds known-unrunnable behavior.
3. The final F2 ruling keeps the public terminal set exactly
   `delivered | failed | canceled`. A legacy null-carrier result maps to `failed` with
   `failureClass=legacy_outcome_unknown`, trusted migrated sender and routing identity,
   and one notice. The design creates no fabricated carrier and no absent
   attempt/admitted/handled/undeliverable ledger.
   Direct source: product-owner ruling wake `w_da8051d5`, issued by owner session
   `s_fde9b2be`. Its exact ruling is also carried without alteration in sole Bug A
   implementation assignment `asg_e7556f25-d909-42f1-ba89-68e1714e6cef`.
4. Normal resolution returns one exact session after it applies the existing direct,
   role-fallback, and owner-Main rules.
5. Current main v7 has no durable R2 fact-and-revision base. The Gateway can read
   session state, but no reviewed authority defines the hold, circuit, adapter, catalog,
   credential, or quota objects and writer transitions required to construct every R2
   key. Operator ruling `dr_99628605-cb7a-44b4-a509-d46b8e7f4ffd` commissions that
   base. R1-R7 remain controlling intent, but implementation is blocked until the
   commissioned authority is reviewed and incorporated here.
6. The 2026-08-18 specimen records session `s_f63d31e5`, twelve failed turns, and lost
   wakes `w_45faa8a8` and `w_a2a13028`. The specimen motivates this amendment. It does
   not authorize a live replay or provider probe.
7. Existing request idempotency remains available. The same implementation slice must
   add the reviewed wake-terminal compare-and-set, deterministic notice identity, and
   publisher recovery because current main v7 does not contain them.

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

### R8. Compose current v7 with the missing Bug A base

Current main v7 has turn terminals but no public wake terminal. It also has no
`wake_sender_notices` table, notice publisher, `wake-notices` projection, sibling
carrier ledger, or normalized sibling registry. These absences are source facts, not
implementation choices. The successor must add the reviewed Bug A public-terminal and
sender-notice slice before it can satisfy R4-R7. It must add the known-unrunnable cause,
typed failure classes, evidence reference, and trigger provenance to that same slice.

Current main v7 also has no Missing R2 fact base. This amendment does not authorize an
implementer to choose its tables, in-memory state, token encodings, revision sources, or
writers. Operator ruling `dr_99628605-cb7a-44b4-a509-d46b8e7f4ffd` commissions a
separate R2 fact-base authority. No v8 implementation assignment may open until that
authority passes independent review and this canonical file incorporates its exact
objects, owners, and transitions. It must make each R2 source and revision constructible
in one checking transaction; an unspecified phrase such as “R2 fact material” is not a
base.

This table remains normative:

| Case | Public wake terminal | Carrier link | Sibling carrier ledger | Notice |
|---|---|---|---|---|
| synchronous R3 refusal | none | none | none | none |
| accepted wake, R4 known-unrunnable before carrier | `failed`, class from R2 | null | no row | one deterministic sender notice |
| admitted carrier failure | `failed`, reviewed carrier class | exact carrier | a separately approved ledger may link the carrier | same reviewed notice identity |
| retirement cancels admitted queued carrier | `canceled`, `session_retired` | exact carrier | a separately approved ledger may link the carrier | same reviewed notice identity |
| legacy null-carrier terminal | `failed`, `legacy_outcome_unknown` | null | no row | one notice from trusted migrated routing |
| legacy prompt wake with untrusted sender routing | none; one migration conflict | preserve existing link or null | no new row | none |

The sibling proposal's `CHECK (kind NOT IN ('admitted','handled','failed') OR turnSeq IS
NOT NULL)` remains valid because this successor writes no null-carrier row to that
ledger. A build must not project the R4 public failure into that ledger, relax its
carrier-integrity constraint, or create an `undeliverable` substitute. If another branch
later adds the proposed table, its migration must leave it unchanged and empty for each
R4 or legacy null-carrier result.

The v7-to-v8 wake backfill applies only to rows whose `consumer='prompt'`. It must
preserve every other consumer row and create no public terminal, sender notice, or
migration-conflict row for it.

The required `wake_terminal_outcomes` table must keep the final F2 enum exactly
`delivered | failed | canceled`. It must carry `terminalOutcomeId`, `wakeId`, nullable
carrier turn sequence, terminal kind, typed cause, typed failure class when applicable,
principal, event time, stored sender principal, identical notice recipient, target,
authorized evidence reference, and trigger provenance. The exact terminal
compare-and-set and the linked `wake_sender_notices` insert must share one Wakes-owned
transaction. The notice shape, authorization, deterministic identity, stream cursor,
same-session push constraint, publisher recovery, and Bubble boundary remain those in
reviewed `art_aac9cafc` as narrowed by final F2 and R4-R7 here.

The trusted-routing migration must use structured v7 rows only. It may accept an exact
`events` row with `kind='verb'`, `verb='wake'`,
`json_extract(payload, '$.wake_id')=wakes.wakeId`, and a stored principal whose exact
prefix is `user:`, `session:`, or `process:` with a non-empty ID. It may also use a
non-null `wakes.creatorSessionKey` only when the current `sessions` row proves that exact
session identity. When neither source exists, it may use the actual v7 stored delivery
principal only when `wakes.creatorSessionKey IS NULL` and
`wakes.origin='process:tightbeam'`; this is the reserved internal process identity used
by direct current-main scheduling call sites. It must not accept another `origin` value
as user, session, role, or process routing. If two present structured sources disagree,
or either disagrees with that reserved process fallback, routing is untrusted. Migration
must not parse another `wakes.origin`, event prose, lifecycle detail, prompt text, or
error text.

For a trusted v7 wake with one linked terminal turn, migration maps `delivered` to the
public `delivered` terminal, `canceled` to `canceled`, and `failed | failed_unknown` to
`failed`. When that turn has one typed `turn_lifecycle_events` `terminal_committed` row,
migration copies its exact `cause` and `principal`. A pre-epoch turn without that row
uses cause `legacy_import` and principal `process:tightbeam`; migration must not parse
`turns.error` to invent either value. Current v7 has no wake-delivery failure class.
Migration therefore maps every `failed | failed_unknown` carrier to
`legacy_outcome_unknown`. It must not substitute a harness-health class or classify
stored error or cause prose.

For trusted routing, migration leaves a queued or running carrier without a wake
terminal; R5 settles it later. It leaves an accepted wake without a carrier eligible for
R4. It creates no terminal for a v7 wake that was canceled before carrier admission. A
v7 `fired` wake without a carrier maps only through final F2 to `failed`,
`legacy_outcome_unknown`, a null carrier, and one notice. Migration creates
deterministic terminal and notice IDs, so replay reads the first rows.

For untrusted routing, migration must create one conflict for every prompt wake that
either remains eligible to admit a carrier or already links a queued, running, or
terminal carrier. A v7 wake canceled before carrier admission needs no conflict because
it can perform no later settlement. A conflicted pending or fired null-carrier wake must
be excluded from post-migration Wakes eligibility. A conflicted linked carrier remains
in its current turn lifecycle, but no public wake terminal or sender notice may be
invented for it. This is the explicit legacy exception to R6: the durable conflict is
the final named record that exact sender routing was not reconstructible.

The successor shape must contain this amendment-owned conflict table:

```sql
CREATE TABLE wake_known_unrunnable_migration_conflicts (
  conflictId        TEXT PRIMARY KEY CHECK (length(conflictId) > 0),
  predecessorShape  TEXT NOT NULL
                      CHECK (predecessorShape =
                        'coordination-fabric-v1-phase1-v7'),
  wakeId            TEXT NOT NULL CHECK (length(wakeId) > 0),
  sourceKind        TEXT NOT NULL CHECK (sourceKind IN ('wake','turn')),
  sourceId          TEXT NOT NULL CHECK (length(sourceId) > 0),
  reason            TEXT NOT NULL
                      CHECK (reason = 'trusted_sender_routing_unknown'),
  priorWakeState    TEXT NOT NULL CHECK (priorWakeState IN ('pending','fired')),
  priorTurnStatus   TEXT NULL
                      CHECK (priorTurnStatus IS NULL OR priorTurnStatus IN
                        ('queued','running','delivered','canceled','failed',
                         'failed_unknown')),
  priorCarrierSeq   INTEGER NULL,
  recordedAt        INTEGER NOT NULL CHECK (recordedAt >= 0),
  principal         TEXT NOT NULL CHECK (principal = 'process:tightbeam'),
  CHECK (
    (sourceKind = 'wake' AND sourceId = wakeId AND priorTurnStatus IS NULL
      AND priorCarrierSeq IS NULL)
    OR
    (sourceKind = 'turn' AND priorTurnStatus IS NOT NULL
      AND priorCarrierSeq IS NOT NULL AND priorCarrierSeq >= 0
      AND sourceId = CAST(priorCarrierSeq AS TEXT))
  ),
  UNIQUE (wakeId, sourceKind, sourceId, reason)
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

The successor stamp is `coordination-fabric-v1-phase1-v8`. The central `Schema` shape
gate remains the one stamp owner. `Schema.@schema_modules` remains the actual ordered
schema-owner list. Wakes remains the one DDL and mutation owner for wakes, public wake
terminals, sender notices, the migration-conflict table, and its two triggers. The
product must contain one DDL string for each new Wakes object. The missing R2 base must
name its own schema module and mutation owners before this v8 shape can be implemented.
This successor does not invent `Schema.known_unrunnable_successor_registry/0` or reuse
the sibling normalized registry as that owner.

The pre-boot shape gate must select one path from the durable stamp:

1. An empty database writes the v8 stamp through the existing stamp-first bootstrap,
   then each current schema module creates its owned v8 objects in dependency order.
   Restart after any interruption resumes that same v8 bootstrap without inferring a
   shape from object existence.
2. An exact v4, v5, or v6 database runs the current main transition chain to v7. It then
   runs the v7-to-v8 transition.
3. An exact v7 database runs only the v7-to-v8 transition.
4. An exact v8 database validates every module-owned v8 object and starts no migration.

A non-empty database with no stamp, multiple stamps, or another stamp must return
`ShapeError`. It must run no successor DDL and start no database consumer.

The v7-to-v8 transition must acquire exclusive custody and recheck that one v7 stamp
remains. In one transaction it must add the missing typed sender snapshot, public wake
terminal, sender notice, publisher state, migration-conflict objects, vocabulary,
checks, trusted legacy rows, and the exact objects later incorporated from the reviewed
R2 base. Before it changes the stamp, it must compare each new normalized
`sqlite_master` object with its owning module's one DDL string, require an empty
`PRAGMA foreign_key_check`, and require an `ok` `PRAGMA integrity_check`. The stamp
change to v8 is the transaction's final mutation. Failure before commit preserves the
exact v7 stamp, schema, rows, and objects. Immediate validation and a clean restart must
perform read-only v8 validation. Until the R2 base is incorporated, this paragraph is a
composition constraint and authorizes no partial v8 transition.

The earlier v4-to-v5, v5-to-v6, and v6-to-v7 transitions remain the current main
transactions. A failure in one preserves that transition's exact predecessor. A restart
from a committed intermediate v5, v6, or v7 stamp resumes the next named transition.
This successor does not replace those reviewed current-main contracts with a direct
v3/v4-to-feature registry.

If trusted routing cannot be derived for a legacy prompt wake in a shape named above,
the v7-to-v8 transaction must preserve the wake and every linked turn. For a wake with
no carrier it must insert
`conflictId='wake-routing:<wakeId>:wake:<wakeId>'`, `sourceKind='wake'`, and
`sourceId=<wakeId>`. For a linked carrier it must insert
`conflictId='wake-routing:<wakeId>:turn:<turnSeq>'`, `sourceKind='turn'`,
`sourceId=CAST(<turnSeq> AS TEXT)`, the same integer `priorCarrierSeq`, and the exact
stored `priorTurnStatus`. Each row uses the exact stored `priorWakeState`, the migration
clock, predecessor v7 stamp, and reserved recording principal. The transaction must not
parse or normalize prose to construct any field.

The migration must commit the v8 schema, stamp, and conflict rows together. It must not
commit a prospective terminal, notice, message, route, carrier, or sibling-ledger row
for a conflicted wake. The v8 shape gate must verify the conflict table and both
triggers, then start Gateway, Wakes, the notice publisher, Bubble, and session-lane
consumers normally. Wakes must exclude only conflicted pending or fired null-carrier
wakes from trigger selection and delivery. Existing linked carriers remain governed by
their current turn lifecycle; the conflict prevents public wake-terminal or notice
materialization for them. A restart must retain the same conflict rows, create no
duplicates, and leave unrelated wakes and carriers runnable.

This successor authorizes no automatic conflict repair. The conflict is an accepted,
named historical failure, not a hold whose exit waits for another principal. A future
authority may define a repair only if it can prove the original authenticated sender
without caller-supplied identity. A failure before the migration transaction commits
must preserve v7 and leave no v8 conflict object or row.

Subtraction ruling: ADD the reviewed Bug A terminal and notice base because deleting it
would leave new accepted wake failures invisible. ACCEPT untrusted legacy routing as one
durable per-wake conflict because inventing a sender is forbidden. DELETE the earlier
boot-wide conflict hold because one historical ambiguity must not stop unrelated work.
Do not ADD an R2 registry in this amendment: its state owners and revision transitions
are missing authority, and `dr_99628605-cb7a-44b4-a509-d46b8e7f4ffd` commissions that
authority separately. The sibling registry loses because current main has no such
mechanism and its non-null carrier boundary cannot represent R4 or legacy null-carrier
results.

## Architecture

The following gateway path becomes implementable only after the Missing R2 fact base
has named its objects, writers, and revision transitions and this file incorporates that
authority:

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

The Wakes transaction owner is the only writer for accepted-wake terminal outcomes and
sender notices. The Bug A notice publisher added by R8 is the only failed-or-canceled
push writer. Bubble may reference the committed notice and must not publish a second
sender message.

The Missing R2 fact base has no architecture owner in current authority. A builder must
not assign it to Wakes, `ConditionFacts`, `HarnessHealth`, an in-memory adapter, or the
sibling registry by analogy. The owner named by the future ruling must be added here and
to R8 before implementation handoff.

The response schema adds only `target_known_unrunnable` and its closed precondition.
The durable schema adds the missing Bug A `wake_terminal_outcomes` and
`wake_sender_notices` base, extends its cause and failure-class checks, and adds R8's
append-only migration-conflict table, v8 stamp, v7 transition, and per-wake exclusion
for conflicted null-carrier rows. It adds no wake attempt ledger, retry scheduler,
alternate recipient, provider-health probe, sibling carrier ledger, or normalized schema
registry.

Wakes owns the public-terminal and sender-notice mutation seam. `Schema` owns the one
shape transition. The R8 notice publisher owns the only post-commit push. Bubble consumes
the committed terminal and notice. This amendment authorizes no second schema system and
does not pre-assign the missing R2 mutation seam.

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

The same fixture must include one otherwise-identical mismatch case for each opaque
member that R2 carries inside a token or cause-specific key: `adapterToken.harnessId`,
`credentialToken.credentialSlotId`, `quotaWindowId`, `holdId`, and `circuitId`. Each case
changes only that member in the stored fact and then verifies that the old fact does not
refuse the request.

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

Every A7 v8 fixture includes the exact R2 base objects and writers from the future
commissioned authority incorporated into this file. Until that authority passes review
and is incorporated, A7 is a composition contract and no implementation gate may claim
it passed.

Given a v7 fixture that does not include the proposed sibling `wake_delivery_outcomes`
table, when migration and the next clean boot run, then the v8 product still satisfies
R1-R8 and does not create that sibling table or registry.

Given a branch-composition fixture that separately includes the proposed sibling
`wake_delivery_outcomes` table, when an R4 failure and a legacy null-carrier migration
run, then each creates one `wake_terminal_outcomes` `failed` row and one sender notice.
It creates no sibling-ledger row. The sibling table's non-null carrier constraint remains
unchanged.

Given an empty database, when bootstrap runs, then it writes the one
`coordination-fabric-v1-phase1-v8` stamp and creates each module-owned v8 object. Given
an interruption after the stamp and before each module boundary, when bootstrap restarts,
then it resumes v8 object creation without changing the stamp or inferring a predecessor
from object existence. Immediate validation and the next clean restart change no row.

Given one exact fixture for each current supported v4, v5, and v6 stamp, when startup
runs, then it commits the current main transitions in order until it reaches v7 and then
commits the v7-to-v8 transition. Given a forced failure before any named transition
commits, when startup returns, then the database retains that transition's exact
predecessor stamp, rows, and objects. Given restart from each committed v5, v6, or v7
intermediate, when startup runs again, then it resumes at the next named transition and
finishes at v8 without repeating an earlier committed transition.

Given an exact v7 fixture, when startup runs, then one v7-to-v8 transaction creates the
missing typed sender snapshot, `wake_terminal_outcomes`, `wake_sender_notices`, notice
publisher state, migration-conflict objects, vocabulary, checks, trusted legacy rows,
and every exact object required by the incorporated R2 base. It changes the stamp last.
Immediate validation and a clean restart change no schema object or row.

Given one v7 row for each non-prompt consumer present in current main, when migration
runs, then it preserves that wake byte-for-byte and creates no public terminal, sender
notice, or migration-conflict row for it.

Given one v7 wake for each typed `user`, `session`, and `process` principal whose exact
accepted `events` row names that wake, when migration runs, then the migrated sender and
recipient equal the event's structured principal. Given a validated
`creatorSessionKey` without a conflicting event, when migration runs, then it uses that
session identity. Given one direct current-main prompt wake with null
`creatorSessionKey`, no accepted wake event, and exact `origin='process:tightbeam'`, when
migration runs, then sender and recipient equal that reserved process principal. Given
two present sources that disagree, when migration runs, then it takes the conflict path
and exposes neither candidate as trusted. Given another origin without an event or
validated creator session, then it takes the conflict path and does not parse that
origin as a principal.

Given one trusted v7 wake linked to each terminal turn state `delivered`, `canceled`,
`failed`, and `failed_unknown`, when migration runs, then it creates one deterministic
public wake terminal with the R8 mapping and one deterministic notice. Given a terminal
turn with a typed `terminal_committed` row, then the migrated terminal copies its cause
and principal. Given a pre-epoch terminal turn without that row, then it uses
`legacy_import` and `process:tightbeam`. Every migrated `failed | failed_unknown`
carrier uses `legacy_outcome_unknown`; changing only `turns.error` or a harness-health
classification changes no migrated public value. Given a queued or running linked turn,
when migration runs, then it creates no wake terminal and leaves R5 eligible. Given an
accepted prompt wake without a carrier, when migration runs, then it creates no wake
terminal unless the exact v7 row is the final F2 legacy null-carrier case.

Given an exact v7 fixture, when a failure is injected during DDL, copy, trusted-routing
settlement, terminal creation, notice creation, conflict creation, object comparison,
either integrity check, or the stamp change, then the transaction preserves the exact v7
stamp, rows, and objects and leaves no v8 object or row. Given a non-empty fixture with
no stamp, multiple stamps, or another stamp, startup returns `ShapeError`, runs no DDL,
and starts no database consumer.

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

Given routing is not derivable for each of these prompt-wake shapes—pending without a
carrier, fired without a carrier, or linked to a queued, running, delivered, canceled,
failed, or failed-unknown turn—when migration runs, then it preserves the wake and linked
turn and commits one `wake_known_unrunnable_migration_conflicts` row with the exact R8
`sourceKind`, `sourceId`, prior wake state, optional carrier and turn status,
`trusted_sender_routing_unknown`, predecessor v7 stamp, migration time, and
`process:tightbeam` recording principal. It creates no public terminal, notice, message,
route, carrier, or sibling-ledger row for that wake. A v7 wake canceled before carrier
admission creates no conflict and remains canceled.

Given one conflict for a pending or fired null-carrier wake and one unrelated due prompt
wake, when startup and Wakes delivery run twice, then all consumers start normally, the
conflicted wake admits no carrier, the unrelated wake follows its ordinary delivery
path, and the database still contains exactly one unchanged conflict row. Given a
conflicted linked carrier, when its current turn later terminates, then its turn lifecycle
remains authoritative and no public wake terminal or sender notice is fabricated. A
restart creates no duplicate conflict and does not block another wake or carrier.

## Open Questions

None. The owner answered the only blocking choice through
`dr_99628605-cb7a-44b4-a509-d46b8e7f4ffd=commission_r2_fact_base`. Production remains
blocked on that commissioned, reviewed, and incorporated dependency; the dependency is
not an unanswered spec choice.

A new precondition, external health probe, alternate recipient, automatic retry,
conflict repair, or rerouting rule requires a separate reviewed amendment.
