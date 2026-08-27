# Typed progress attests

Status: PROPOSAL amended after independent review, the owner query-recovery
ruling, and current-main schema reconciliation. The amended bytes require
fresh different-session review on one owner-opened review assignment. This
spec is targetless. It authorizes no product integration, release, deployment,
live mutation, identity edit, or configuration change.

Review evidence: exact-tip review `att_00078fa7` / `art_34d5ff29` requested
changes on commit `b226273db5707aa930cee26fd4f76a77800881fb` because `(ts,
id)` is deterministic query order but not append-monotonic recovery order.
This successor uses full assignment reconciliation plus durable seen-id
deduplication; it does not add a server cursor or firehose history.

The later exact-tip review `att_131946e0` / `art_03476a8d` found commit
`b981c43a885a73907c924c22036ae11ece277fec` reviewed-clean. Coder surrender
`att_e1099cee` / `art_1d4880f9` then found one source-composition conflict:
current main already assigns the unqualified phase-1 v7 stamp to
`messages.messageType`. This successor changes the schema composition clauses
only. It preserves the reviewed typed-progress and query-recovery behavior.

Authority: Mike ruling `art_e15670c9` (SHA-256
`26a9ce6832c1e442ce18dddf0b00768a2b23158442072fe256ad29b9046ff3e3`) and
spirit verdict `att_9c95b557-c4d2-4c73-be9f-6d24d3a22390` on work item
`wi_990f7b7e-837b-4aba-8f2e-ac6617327d78`, and owner query-recovery ruling
`att_b7a1c929-bab6-449c-b3a5-72d78874446a`. This spec amends `attest-v1.md`,
`effort-checkin-v2.md`, and the no-acknowledgment clauses in
`coordination-fabric-v1.md` only where this change names a replacement. Their
other clauses remain in force.

Source evidence: Tightbeam `origin/main` commit
`31c91a7a79bf411791d8422bb220495a72dd8d0c`, including landed
`messages.messageType` commit `258d122fded02f763ce7fe8e819479eea3f1b8ad`;
typed-progress candidate `a3268d1e3f8d69d82fc7a28c870844eee5024e7b`;
tightbeam-specs `origin/main` commit
`dd88e71cd9ee616e53b3df671a0194c7c5ecd1cc`. Code is evidence for the current
seams. The rulings above are the behavior authority.

## Goal

Give each newly filed progress attest the assignment's exact `effectKind`.
Make the progress filing mean forward motion on that assignment deliverable.
Let an effort check-in credit the attest channel only for matching typed
progress. Give a holder a distinct acknowledgment filing for ruling receipts
and coordination traffic that earns no effect credit.

The smallest useful outcome is one additive contract across the CLI, wire,
domain, database, public projections, effort evidence, and operating-manual
seed. The substrate compares recorded enum values. It does not interpret the
note, judge the work, or infer intent.

## Non-Goals

1. This spec does not change the assignment `effectKind` vocabulary or its
   current defaulting rules.
2. This spec does not decide whether a progress claim is honest, sufficient,
   correct, or valuable.
3. This spec does not change workspace-write, artifact, or work-item-update
   effect channels.
4. This spec does not change effort horizons, rungs, decisions, wake timing,
   or owner escalation.
5. This spec does not change completion, surrender, verdict, reopening,
   supervision, or review semantics beyond making acknowledgment a
   progress-ineligible attest kind.
6. This spec does not make acknowledgment a required reply. The fabric's
   no-acknowledgment law still forbids directives from requesting an
   acknowledgment turn. An optional acknowledgment row records non-effect
   traffic when the holder elects to preserve it. The row does not prove
   compliance with a directive or satisfy a requested reply.
7. This spec does not rewrite or backfill a historical attest.
8. This spec does not add an idempotency key to `attest`.
9. This spec does not select or request an integration, release, deployment,
   or live-state target.
10. This proposal does not edit product or served identity. It specifies the
    guidance text that a later implementation change must land with the
    capability.
11. This spec does not add durable history to `Firehose.Hub` or
    `ChangeSocket`, a firehose replay service, a server-side subscription
    cursor, or any other event-log architecture. Live change delivery remains
    best effort and historyless. Missed-notice recovery reads the existing
    durable attest rows.

## Terms

- **Assignment deliverable:** the obligation named by the assignment's
  `subject`, scoped by its work item when `workItemId` is present.
- **Assignment effect kind:** the assignment's resolved `effectKind`. The
  closed enum is `code`, `policy`, `release`, `live_mutation`, `evidence`,
  `review`, and `coordination`.
- **Typed progress attest:** an attest whose `kind` is `progress` and whose
  stored `effectKind` equals its assignment effect kind.
- **Explicit progress type:** an `effectKind` that the caller supplies on an
  `attest` request whose `kind` is `progress`.
- **Inherited progress type:** the assignment effect kind that the server
  copies into a progress attest when the caller omits `effectKind`.
- **Acknowledgment attest:** a nonterminal holder filing whose `kind` is
  `acknowledgment`, whose `effectKind` is null, and whose note records a ruling
  receipt or non-effect coordination traffic. Coordination traffic includes an
  exact blocker or refusal and the condition that would clear it.
- **Historical untyped progress:** a progress row that predates this contract
  and therefore stores `effectKind = null` after migration.
- **Attest-channel effect credit:** the effort check-in's finding that at least
  one eligible attest row exists after its recorded attest watermark. This
  term does not include the other three effect channels.
- **Mismatch:** an explicit progress type that belongs to the enum but differs
  from the assignment effect kind.
- **Canonical attest event identity:** the immutable attest id stored in
  `attests.id`, carried by a live `attest.filed` notice as both
  `refs.attestId` and `payload.id`, and returned by the `attests` read as
  `attest.id`. A ChangeSocket `seq` is delivery order for one live connection;
  it is not this identity and is not a durable cursor.
- **Durable seen-id set:** the consumer-owned, durably stored set of every
  attest id already observed for one assignment. Recovery computes a set
  difference against a complete assignment read. This set, not query order or
  socket sequence, is the recovery watermark.
- **Recovery scope:** one exact assignment id under the existing `attests`
  read authorization. A work-item, session, origin, principal, or subscription
  filter is not a durable replay scope; a consumer resolves and retains the
  assignment ids it tracks, then reconciles each assignment separately.
- **Targetless:** the spec and later candidate remain unbound to a product
  integration branch, release, deployment, or live-state destination.

## Assumptions

1. At source commit `8e269e89`, `Tightbeam.Assignments` resolves assignment
   effect kinds from `assignment_effects`, with `code` as the non-review legacy
   fallback and `review` as the review-assignment legacy fallback.
2. At source commit `8e269e89`, no supported verb mutates an assignment effect
   kind after assignment creation.
3. At source commit `8e269e89`, the database server serializes each mutation
   transaction.
4. At source commit `8e269e89`, `attest` has no idempotency-key input and each
   accepted call appends a new attest row.
5. At source commit `8e269e89`, an effort generation records
   `attestWatermark` as an `attests.rowid` cursor.
6. At source commit `31c91a7a`, the current database shape stamp is
   `coordination-fabric-v1-phase1-v7`. Its named
   `coordination-fabric-v1-phase1-v6` predecessor migration adds nullable
   `messages.messageType` and preserves a null value for each historical
   message.
7. At source commit `8e269e89`, the CLI prints the gateway's JSON success
   object without a second semantic rendering layer.
8. A builder will stop and return to the spec-writer if the source facts above
   change before implementation.
9. Current main owns the unqualified `coordination-fabric-v1-phase1-v7` stamp
   for the landed `messages.messageType` shape. This proposal does not reuse,
   replace, or reinterpret that stamp.
10. At source commit `cba8d6c`, `attests` supports optional `after` and `limit`
    inputs. `after` is an attest id scoped to the named assignment; pages are
    ordered by immutable `(ts, id)` and return `nextAfter` and
    `hasMoreAfter`.
11. At source commit `cba8d6c`, `Firehose.Hub` and `ChangeSocket` are explicitly
    live-only and retain no event history. ChangeSocket sequence numbers begin
    and advance within one connection.
12. At source commit `cba8d6c`, there is no supported attest deletion or
    retention-compaction verb.
13. At source commit `cba8d6c`, attest ids are random UUIDv4 values and attest
    `ts` values come from a wall clock. The `(ts, id)` query key is
    deterministic and immutable for a stored row, but a later commit can sort
    before an earlier commit after a same-millisecond lower UUID or wall-clock
    regression.

## Invariants

1. A newly committed progress row stores one enum value that equals the
   assignment effect kind read in the same transaction.
2. A mismatch produces a typed refusal and commits no attest, marker,
   firehose notice, supervision transition, or effort effect.
3. An acknowledgment commits as a nonterminal attest. It does not satisfy an
   attest-channel effect check or a progress-only consumer.
4. The substrate validates kind, enum membership, equality, state, and
   principal. It does not read the note to decide whether progress occurred.
5. Migration preserves each historical attest's id, data, and SQLite `rowid`.
   Historical untyped progress remains null and receives no attest-channel
   effect credit after activation.
6. Each public projection that emits an attest row emits its stored
   `effectKind`, including null. A projection does not substitute the parent
   assignment effect kind for a historical null.
7. The parent assignment's existing read authorization controls the new field
   and acknowledgment row. This spec adds no reader and no visibility scope.
8. The holder-session authorization and precedence for lifecycle attests also
   govern progress and acknowledgment.
9. An effort check-in records counts and enum classifications needed for
   audit. It does not copy attest notes into effort evidence or prod text.
10. A directive does not request an acknowledgment turn. The acknowledgment
    kind makes optional non-effect traffic representable without recasting it
    as progress. Filing the row does not prove directive compliance.
11. This work stays targetless through reviewed-clean code and green gates.
    The later delivery state is `DONE-AWAITING-TARGET`.
12. Live notice loss does not lose the fact. While an attest row is retained,
    an authorized consumer can recover its exact stored kind, `effectKind`,
    and canonical identity by reconciling the complete existing
    assignment-scoped `attests` read against its durable seen-id set.
13. One attest id denotes one fact across live delivery and durable readback.
    A consumer suppresses a duplicate delivery of that id, but it never
    collapses two different ids merely because their kind, note, timestamp, or
    effect kind match.
14. `(ts, id)` is presentation and page order, not append or causal order. A
    consumer never discards an unseen id because that row sorts at or before a
    previously seen row.
15. The typed-progress migration preserves the landed nullable
    `messages.messageType` column and each stored message value byte-for-byte.

## Architecture

### 1. One mutation seam

`Tightbeam.Assignments` remains the only mutation seam for assignment attests.
The handler performs the parent lookup, holder check, open-state check, kind
validation, note validation, effect resolution, attest insert, and related
state changes in one database transaction.

R1. The wire request accepts optional `params.effectKind` on `attest`.

R2. The CLI accepts optional `--effect-kind <kind>` on `attest` and sends it as
`params.effectKind`. The CLI does not invent a default.

R3. For `kind=progress`, the handler resolves the assignment effect kind in
the mutation transaction. If the request omits `effectKind`, the handler
stores the resolved assignment value. If the request supplies the matching
value, the handler stores that value. If the request supplies a mismatch, the
handler returns `effect_kind_mismatch`.

R4. For `kind=acknowledgment`, the handler requires a nonblank `note` from 1 to
2,000 characters inclusive. The handler stores `effectKind = null`, leaves the
assignment open, and runs no progress transition.

R5. The handler accepts `effectKind` only for `kind=progress`. A request that
supplies it for `acknowledgment`, `completion`, `surrender`, or `verdict`
returns `invalid_effect_kind_scope`.

R6. The handler returns `invalid_effect_kind` when a supplied value is not in
the assignment effect-kind enum. It returns the existing `invalid_note` error
when an acknowledgment omits a nonblank note or exceeds the note limit.

Validation order inside the current principal-authorized mutation seam is:
parent assignment, holder authorization, assignment state, attest kind, note,
effect enum, effect scope, effect equality. Existing router refusals retain
their earlier precedence.

### 2. Success shapes and exact text

R7. Each new progress attest object contains nonnull `effectKind`. Each
acknowledgment attest object contains `effectKind: null`. Completion,
surrender, verdict, and historical untyped progress objects also contain
`effectKind: null`.

R8. The `attest` mutation success object adds `message` with one of these exact
values:

- Progress: `progress asserts forward motion on this assignment's deliverable for effectKind=<resolved-kind>`
- Acknowledgment: `acknowledgment records a ruling receipt or coordination traffic and does not count as effect`

The mutation response for completion, surrender, and verdict keeps its current
shape except for `attest.effectKind: null`; it adds no `message`.

R9. The CLI help contains these exact semantic statements next to the
`attest` command:

```text
kind=progress asserts forward motion on this assignment's deliverable for its effectKind; omit --effect-kind to inherit it.
kind=acknowledgment requires --note, records a ruling receipt or coordination traffic, and does not count as effect.
```

The usage line lists `acknowledgment` in the kind vocabulary and lists
`[--effect-kind code|policy|release|live_mutation|evidence|review|coordination]`.

### 3. Storage and exact migration

R10. The `attests` table gains nullable camel-case column `effectKind TEXT`.
Its value constraint admits null or one assignment effect-kind enum value. The
`kind` constraint admits exactly `progress`, `acknowledgment`, `completion`,
`surrender`, and `verdict`.

R11. The rebuilt table uses these complete row-shape constraints:

- Progress requires `bySession` nonnull, `byUser` null, and `verdictKind` null.
  Its `effectKind` is nullable only so a historical row remains representable.
- Acknowledgment requires `bySession` nonnull, `byUser` null,
  `verdictKind` null, `effectKind` null, and `note` nonnull.
- Completion and surrender require `bySession` nonnull, `byUser` null,
  `verdictKind` null, and `effectKind` null.
- Verdict requires `verdictKind` nonnull, `effectKind` null, and exactly one of
  `bySession` and `byUser` nonnull.
- The existing note-length and verdict-only producer, producer-command,
  harness, and provider constraints remain in force.

R12. Four named database triggers protect the cross-table progress invariant.
`attests_typed_progress_nonnull_insert` and
`attests_typed_progress_match_insert` reject a new progress insert whose type
is null or differs from the parent assignment's resolved effect kind.
`attests_typed_progress_nonnull_update` and
`attests_typed_progress_match_update` apply the same checks before an update
changes `kind`, `assignmentId`, or `effectKind`. The handler maps its own
pre-insert checks to the typed errors in R3 and R6. A trigger failure is an
invariant breach, not a public mismatch path.

R13. The targetless final shape is
`coordination-fabric-v1-phase1-v8-typed-progress-attests`. Its fresh-database
bootstrap stamp is
`coordination-fabric-v1-phase1-v8-typed-progress-attests-bootstrapping`. The
typed-progress migration accepts the landed
`coordination-fabric-v1-phase1-v7` message-type shape as its sole direct
predecessor. It does not accept v6 directly and does not reuse or overwrite
the landed v7 stamp.

Boot dispatch follows this exact order:

1. A fresh unstamped database with no `sessions` table receives the bootstrap
   stamp. Schema creation uses the final `messages` and `attests` definitions,
   including the four R12 triggers. After schema creation, one transaction
   validates the final inventory and replaces the bootstrap stamp with the
   final stamp. A restart at the bootstrap stamp resumes missing final-shape
   objects. Each object already present must match its final definition.
2. A v4 database runs the existing operational-parent migration to v5, the
   existing cold-start migration to v6, the existing message-type migration to
   v7, and then the typed-progress migration to the final shape.
3. A v5 database runs the existing cold-start migration to v6, the existing
   message-type migration to v7, and then the typed-progress migration.
4. A v6 database runs the existing message-type migration to v7 and then the
   typed-progress migration.
5. A v7 database runs only the typed-progress migration.
6. A final-shape database validates the final inventory and performs no schema
   or stamp write.

Each step re-reads its expected stamp inside its write transaction. Concurrent
boot calls serialize on the database. A call that acquires the write boundary
after another call advanced the stamp dispatches again from the observed named
shape. Concurrent calls from v4, v5, v6, v7, the bootstrap stamp, or the final
stamp converge on one final inventory without a duplicate-object error. A
second boot against the final inventory leaves the schema, rows, triggers,
stamp, and `stampedAt` unchanged.

The v7-to-final migration uses the repository's foreign-key rebuild transaction
to:

1. create the successor `attests` table;
2. copy each old row with its explicit SQLite `rowid` and
   `effectKind = null`;
3. replace the old table;
4. create the four named progress triggers;
5. run `PRAGMA foreign_key_check`; and
6. replace v7 with the final stamp in the same transaction.

A crash inside the existing message-type migration exposes v6 or complete v7.
A crash after that migration commits and before typed-progress migration begins
exposes complete v7. A crash inside typed-progress migration exposes complete
v7 or the complete final shape. A restart dispatches from the observed named
shape and runs only the remaining steps. Replaying a committed step does not
rewrite `messages.messageType`, an attest row, a trigger, or a stamp.

The exact v6 inventory contains `messages` without `messageType`, the legacy
`attests` table without `effectKind` or acknowledgment, and no R12 trigger. The
exact v7 predecessor inventory adds `messages.messageType` as nullable `TEXT`
and otherwise retains that legacy typed-progress inventory. The exact final
inventory contains the final stamp, nullable `messages.messageType TEXT`, one
rebuilt `attests` table with R10-R11's column and constraints, and the four R12
triggers. The typed-progress migration creates no new index. It preserves each
other schema object and each stored message value.

Shape recognition compares the stamp and the inventory for that named step. A
v6 stamp with a message-type or typed-progress successor object, a v7 stamp
with a missing or nonconforming message-type object or with a typed-progress
successor object, a final stamp with a missing or nonconforming final object, a
bootstrap stamp with a nonconforming present object, or another stamp refuses
startup. An existing message-type migration failure retains its
`incompatible_message_type_v1` prefix. A typed-progress stamp or inventory
failure uses `incompatible_typed_progress_attests_v1`. Its message is
`database shape <observed-stamp> is incompatible with typed-progress-attests-v1: <mismatches>`,
where `<observed-stamp>` is the stored value for one row, `<missing>` for zero
rows, or the lexically sorted values joined by `|` for two or more rows.
`<mismatches>` is a lexically sorted comma-separated list drawn from
`shape_stamp`, `messages.messageType`, `attests.effectKind`,
`attests.kind_constraint`, `attests.row_shape_constraints`, and the four exact
trigger names. A v6 or v7 inventory mismatch uses the typed-progress refusal;
`incompatible_message_type_v1` remains the prefix only for a failure inside the
existing migration after exact v6 preflight succeeds. A refusal changes no
schema object, stamp, or domain row.

### 4. Effort check-in consumption

R14. The effort check-in's attest channel counts a row after the generation's
`attestWatermark` only when the row has `kind=progress` and its stored
`effectKind` equals the parent assignment's resolved effect kind.

R15. The effort decision reads the eligible count in the same transaction that
records the existing effort outcome and action. Database serialization decides
the boundary: a progress transaction that commits first is visible; a progress
transaction that commits second belongs to the next evaluation.

R16. Effort evidence replaces the ambiguous attest count with this object:

```json
{
  "attestChannel": {
    "matchingTypedProgress": 0,
    "acknowledgments": 0,
    "historicalUntypedProgress": 0,
    "otherAttests": 0
  }
}
```

The counts cover rows after the generation watermark. `otherAttests` covers
verdict, completion, and surrender rows that remain observable at evaluation.
The effect predicate reads only `matchingTypedProgress`.

R17. Holder and owner messages replace `attests` in the four-channel list with
`matching typed progress attests`. When excluded rows exist, evidence reports
their counts. A message does not quote their notes.

This spec does not alter the other effect predicates. The complete effect
predicate remains: workspace writes, holder-recorded artifacts, matching typed
progress attests, or holder work-item metadata updates.

### 5. Projections and audit

R18. The mutation response, `attests` query, work-item trace, work-state detail,
and `attest.filed` firehose resource include the stored `effectKind`. An
abbreviated attest row in a public projection also includes the field. The
live resource carries the canonical identity as
`refs.attestId == payload.id == attests.id`; its ChangeSocket `seq` remains a
connection-local delivery number.

R19. Existing aggregate attest counts include acknowledgment under its stored
kind. An aggregate that reports progress counts only `kind=progress`; it does
not recast acknowledgment as progress.

R20. The existing attest id, event, marker, author columns, timestamp, note,
and parent relationship remain the audit record. The acknowledgment transcript
marker reads `[acknowledgment filed on <assignmentId>]`. The progress marker
keeps its current text because the response and row carry the type. Recovery
uses the attest id and stored row; it does not synthesize a replacement event.

R21. This change adds no note to a projection that currently omits notes. It
adds no cross-principal lookup. The effort evidence in R16 exposes counts, not
note content.

### 6. Authorization, recovery, and races

R22. Only the holder session can file progress or acknowledgment. User,
process, and non-holder session principals receive the current typed principal
refusals under the current precedence.

R23. The three new request failures use the existing control-plane error
envelope and map to HTTP 400 on the agent REST transport:

| Code | Exact message |
| --- | --- |
| `invalid_effect_kind` | `effectKind must be one of code, policy, release, live_mutation, evidence, review, coordination` |
| `invalid_effect_kind_scope` | `effectKind is only valid when kind is progress` |
| `effect_kind_mismatch` | `progress effectKind <supplied> does not match assignment effectKind <expected>` |

The existing `invalid_note` code uses exact message
`note must be 1..2000 non-blank characters` for an absent, blank, or
over-limit acknowledgment note. Each refusal commits no domain row, marker,
event, or firehose notice.

The existing unpaged recovery read keeps its current typed failures and
transport classes: `principal_required` and `process_denied` are HTTP 403, and
`unknown_assignment` is HTTP 404. The CLI exits nonzero and prints the returned
error. REST returns the ordinary `{"error":{"code","message"}}` envelope. A
refusal or transport failure does not change the durable seen-id set; retrying
the same unpaged read is safe because the set difference suppresses ids already
consumed.

R24. `attest` remains non-idempotent. Two accepted requests append two attest
rows. A client that receives an unknown mutation outcome must read the
assignment's attest trail before it elects another filing. This spec does not
authorize an automatic retry. Those two accepted requests have different
attest ids and are different facts. Delivery of one accepted row through both
the live socket and query recovery has one attest id and is one fact.

R25. Concurrent progress or acknowledgment versus a terminal assignment
transition uses the current serialized transaction rule. The first committed
transaction wins. If the terminal transition commits first, the nonterminal
filing returns `assignment_closed` and writes no row. If the nonterminal filing
commits first, its row remains and the later terminal transition may close the
assignment.

R26. Schema restart, gateway restart, and effort-generation replay read the
stored `effectKind`. They do not derive a type for a historical null.
Preserved rowids keep each existing effort watermark ordered across the
migration.

`Firehose.Hub` and `ChangeSocket` remain live-only and historyless. A connected,
authorized, subscribed consumer may receive the post-commit `attest.filed`
notice, but delivery is best effort. The hub stores no recovery history, a
ChangeSocket `seq` is not durable across reconnect, and this contract creates
no firehose replay operation.

The durable recovery source is the existing assignment-scoped `attests` read.
For each tracked assignment, the consumer durably stores the complete set of
attest ids it has observed. Every reconciliation begins at the start of the
assignment trail and reads the whole trail in one call:

```text
tightbeam attests <assignmentId>
```

The equivalent agent REST call is authenticated `POST /agent/dispatch` with
body:

```json
{"verb":"attests","params":{"assignmentId":"<assignmentId>"}}
```

The read returns every exact stored row in deterministic `(ts, id)` order, but
that order is not append-monotonic: UUIDv4 ids and wall-clock timestamps allow
a later commit to sort before an earlier one. Therefore recovery does not pass
`after` or `limit`, and the consumer never uses `nextAfter`, the last returned
id, the greatest timestamp, or the greatest socket sequence as durable
recovery state. The existing paged read remains available for interactive
audit traversal, outside this recovery contract.

At the end of a successful full read, the consumer unions every returned id
with live-buffer ids, computes `unseen = union - durableSeenIds`, processes
each unseen progress or acknowledgment fact once by canonical id, then
durably adds every returned or buffered attest id to `durableSeenIds`. It does
not use note equality, `effectKind`, `occurredAt`, `(ts, id)` position, or
socket `seq` as identity. If processing stops partway through the difference,
the fact's consumer-side effect and insertion of its id into the seen set must
commit atomically; when the effect target cannot share that transaction, the
consumer makes the effect idempotent under the canonical attest id. Merely
recording the id before its effect could commit would lose the fact, while
performing a non-idempotent effect before recording the id could duplicate it.
Retrying the full read is safe under either supported shape.

A consumer reconciles after its first subscription, every reconnect, its own
restart, a gateway restart, a slow-consumer close, any observed in-connection
sequence gap, and any other interval in which it cannot prove continuous live
delivery. To close the subscribe/query race without server history, it first
reaches `subscription_ready`, buffers subsequent matching live notices, walks
the complete unpaged durable query, then unions buffered notices and query rows
by attest id before resuming ordinary live processing. An attest committed
before subscription readiness is found by the full query, even when it sorts
before every previously seen row. One committed after
readiness is found by the live buffer, the query, or both. A later full read
also finds it independently of `(ts, id)` position.

Recovery scope is the exact assignment id. Existing live filters continue to
govern best-effort notices, and the existing `attests` principal gate governs
readback. This clause does not turn a subscription filter into a query, add a
cross-assignment scan, or widen visibility. A missing or foreign cursor returns
`cursor_not_found` only on the separate paged audit surface; recovery supplies
no cursor. Current attest rows have no supported deletion or compaction path.
Any future retention change must preserve unseen durable rows until
reconciliation or amend this contract with a replacement recovery seam before
it ships.

### 7. Operating-manual seed and pattern

R27. The implementation candidate lands the operating-manual replacement and
the two role-refraction amendments in this section with the shipped command.

The capability teaches one operating pattern: progress is a typed effect
claim; acknowledgment is an optional non-effect record. The implementation
change must replace the current blocked-as-progress instruction and the
ambiguous reporting-attest instruction. It must land this seed with the
shipped command:

> An assignment's `effectKind` classifies its deliverable as `code`, `policy`,
> `release`, `live_mutation`, `evidence`, `review`, or `coordination`. File
> `kind=progress` only for forward motion on that deliverable. Omit
> `--effect-kind` to inherit the assignment value. File
> `kind=acknowledgment` when you elect to preserve a ruling receipt or
> non-effect coordination traffic. If progress has stopped, use
> `kind=acknowledgment` to record the exact blocker or refusal, its evidence,
> and the condition that would clear it. Keep the card and schedule a concrete
> continuation wake. An acknowledgment does not count as assignment effect.

The replacement must map each reporting exception to one lawful path. If the
holder elects an attest for a material result that moved the deliverable
forward, the holder uses matching typed progress. Existing artifact and
work-item-update paths remain separate effect channels. An exact blocker or
refusal uses acknowledgment and a continuation wake. A bounded decision
request uses the decision-request command and its continuation wake; it may
also have an acknowledgment row when the holder needs a durable
assignment-local receipt, but that row earns no effect. A checkpoint with no
forward motion uses a continuation wake, not progress.

The manual must retain the no-acknowledgment directive: do not request an
acknowledgment turn for an ordinary directive or `fyi` delivery. An elected
acknowledgment row does not prove directive compliance.

The same implementation change must amend two role refractions in the
agentic-engineering kungfu:

- The unblocking skill must direct the reader to the latest blocker-bearing
  acknowledgment or terminal surrender. For rows filed before this capability,
  it must also accept the last historical progress attest as blocker evidence.
- The recon-lifecycle skill must direct the holder to record a finding beyond
  the assigned question as a non-effect acknowledgment and not pursue it. It
  must not call that out-of-scope finding progress.

The coder ready-for-review attest, orchestrator first-progress check, and
recon-first root-cause attest remain progress instructions because each names
forward motion on its assignment deliverable.

### 8. Subtraction ruling

ADD wins: deleting progress credit would discard Mike's ruled typed signal;
accepting the ambiguity would preserve regression `asg_3d219794` on
`wi_ecd8cd9d`. The addition uses one existing mutation seam, one stored field,
one new kind, and one equality predicate. It adds no content classifier or
decision mechanism. Composition also adds one v7-to-feature-qualified-v8
migration because deleting the typed storage change cannot satisfy R1-R3 and
accepting the v7 collision leaves the reviewed contract unbuildable.

## Acceptance

Each acceptance case runs deterministically against a fresh successor database
unless the case names a predecessor database. Tests must identify the
requirement ids they verify.

1. **A1 — inherited type for each enum value (R1-R3, R7).** Given one open
   assignment for each assignment effect kind, when its holder files progress
   without `effectKind`, then each success row stores the assignment value and
   returns the exact progress message with that value.
2. **A2 — explicit match for each enum value (R1-R3, R7).** Given the same
   seven assignments, when each holder files progress with the matching value,
   then each call appends one typed progress row and leaves its assignment open.
3. **A3 — mismatch matrix (R3, R12).** Given each assignment effect kind, when
   the holder supplies each of the other six enum values, then the handler
   returns `effect_kind_mismatch`, names supplied and expected values, and
   commits no row, marker, firehose notice, supervision transition, or effort
   effect.
4. **A4 — database rails (R10-R12).** Given a successor database, direct
   inserts independently attempt: an unknown kind; an unknown nonnull effect
   value; acknowledgment with null `bySession`, nonnull `byUser`, nonnull
   `verdictKind`, nonnull `effectKind`, null `note`, blank `note`, a
   2,001-character `note`, or any nonnull verdict-only producer, command,
   harness, or provider field; progress with invalid attribution; completion
   or surrender with nonnull `effectKind`; verdict with nonnull `effectKind`
   or invalid principal cardinality; progress with null `effectKind`; and
   progress with a mismatching enum value. SQLite rejects every attempt and
   leaves the table unchanged. Direct updates that change a valid progress
   row's kind, parent, or type to a null or mismatching progress shape also
   fail and leave the row unchanged.
5. **A5 — invalid value and scope (R5-R6, R23).** Given an open assignment,
   when the holder supplies an unknown value on each attest kind, then the
   handler returns `invalid_effect_kind` under the stated validation order.
   When the holder supplies an enum value on acknowledgment, completion,
   surrender, or verdict, then the handler returns
   `invalid_effect_kind_scope` with the exact messages and transport class in
   R23. Each case commits no mutation.
6. **A6 — acknowledgment contract (R4, R7-R9, R18-R23).** Given an open
   assignment of each effect kind, when its holder files acknowledgment with a
   nonblank note, then each response contains the exact acknowledgment message,
   each row has null `effectKind`, each assignment remains open, each public
   attest projection reports kind and null type, a connected subscriber's live
   notice reports the same id and null type, durable query recovery reports the
   same id and null type, the transcript carries the exact R20 marker, the
   acknowledgment aggregate increments without incrementing the progress
   aggregate, and no progress-only transition runs.
7. **A7 — acknowledgment note (R4, R6, R23).** Given an open assignment, when
   its holder files acknowledgment with an absent, blank, or over-limit note, then
   the handler returns `invalid_note` with the exact message in R23 and commits
   no row.
8. **A8 — effort match for each enum value (R14-R17).** Given an armed effort
   generation for each assignment effect kind with no other effect channel,
   when one matching typed progress row commits after each watermark, then the
   attest channel reports `matchingTypedProgress: 1` and the effort check-in
   takes the current effect-present path.
9. **A9 — acknowledgments earn no effect (R14-R17).** Given the same seven
   armed generations with no other effect channel, when each holder files one
   acknowledgment after the watermark, then the channel reports
   `acknowledgments: 1`, `matchingTypedProgress: 0`, and the effort check-in
   takes the existing zero-effect holder-prod path.
10. **A10 — historical rows and composed predecessor chain (R10-R17, R26).**
    Given a stamped v7 database with classified and null historical
    `messages.messageType` values plus progress, completion, surrender, and
    verdict rows, when the schema migrates, then message values, attest ids,
    attest field values, foreign keys, and attest rowids match their predecessor
    values. Each historical attest projects `effectKind: null`; a historical
    progress row after an armed watermark increments
    `historicalUntypedProgress` and earns no effect. An unpaged `attests`
    reconciliation after migration and gateway restart returns each preserved
    id for comparison with the consumer's durable seen-id set. A separate v6
    fixture runs v6-to-v7 before v7-to-final and proves the same results plus
    nullable `messages.messageType` on each historical message.
11. **A11 — bootstrap, migration restart, concurrency, and shape refusal (R13,
    R26).** Deterministic fixtures prove these boundaries:

    - A fresh database receives the exact bootstrap stamp. One forced
      interruption after `sessions` exists and before the last schema module
      runs leaves that stamp and a partial set of conforming final objects.
      Another forced interruption after final-inventory validation and before
      stamp replacement rolls its transaction back to the bootstrap stamp.
      Restart from either boundary completes the final inventory once and
      changes the stamp once. A malformed present object under the bootstrap
      stamp returns the typed-progress refusal without changing another object.
    - Forced interruption after typed-attest copy and, in a separate v7 run,
      after table replacement rolls back to exact v7. Restart migrates once,
      `PRAGMA foreign_key_check` returns empty, and the final inventory exists
      once.
    - Forced interruption inside v6-to-v7 rolls back to exact v6. Interruption
      after v7 commits but before typed migration leaves exact v7. Restart from
      either state reaches the same final schema and rows.
    - Two boot calls released on a barrier from each of v4, v5, v6, v7, the
      bootstrap stamp, and the final stamp converge to one final inventory.
      Neither call returns a raw SQLite error. Repeating boot after convergence
      leaves the full schema dump, data dump, stamp, and `stampedAt`
      byte-identical.
    - Separate startup fixtures cover zero stamps with a preexisting `sessions`
      table; two stamp rows; an unknown stamp with a conforming final inventory;
      v6 with `messages.messageType` or one typed-progress object; v7 with
      missing or malformed `messages.messageType`; v7 with each typed-progress
      successor object; final shape with the predecessor table; final shape
      with each missing trigger; a wrong kind constraint; and a wrong row-shape
      constraint. Each in-transaction message-type failure has the named
      `incompatible_message_type_v1` prefix. Each stamp or inventory failure
      returns `incompatible_typed_progress_attests_v1` with the exact message
      and sorted mismatch inventory in R13. Each refusal leaves its before and
      after schema and data dumps byte-identical.
12. **A12 — effort boundary race (R15).** Given one armed generation and one
    matching progress filing released on a barrier with the effort evaluation,
    when progress commits first, then the evaluation observes it. When the
    evaluation commits first, then that evaluation reports zero matching
    progress and the later row remains eligible only for a later generation.
13. **A13 — terminal race (R25).** Given one open assignment, when progress
    versus completion and acknowledgment versus revocation run on a barrier,
    then each race produces one of the two serialized outcomes in R25, with no
    orphan or partially written attest.
14. **A14 — non-idempotent mutation replay and delivery duplicate (R24,
    R26).** Given an open assignment, when the holder sends the same accepted
    progress request twice or the same accepted acknowledgment request twice,
    then the server stores two ids and the response does not claim idempotency.
    Given one accepted row observed once live and once through query recovery,
    the consumer union contains that id once. The test proves that
    deduplication keys on id and does not collapse the two accepted mutation
    ids.
15. **A15 — principal and privacy matrix (R21-R23).** Given an open assignment,
    when its holder, another session, a user, and a process each attempt both
    new forms, then only the holder succeeds. Existing authorized readers see
    `effectKind`; principals without parent-read access gain no row, count,
    note, or event access. Effort evidence contains no note text.
16. **A16 — CLI contract (R2, R8-R9).** Given the candidate CLI built from the
    candidate, when a user runs `tightbeam help`, then the usage and two exact
    semantic statements appear. When the CLI files inherited progress and an
    acknowledgment against a real gateway fixture, then stdout contains the
    exact mutation messages and stored effect fields.
17. **A17 — named regression (R4, R14-R17).** Given a fixture that models
    spec-writer assignment `asg_3d219794` on work item `wi_ecd8cd9d`, with an
    armed horizon, holder turns, ruling-receipt acknowledgments, and no writes,
    artifacts, matching typed progress, or holder work-item update, when the
    horizon evaluates, then the holder receives the zero-effect prod. When the
    holder later files matching typed progress, then the next evaluation sees
    assignment effect.
18. **A18 — targetless delivery (R26 and Invariant 11).** Given reviewed-clean
    candidate code and green required gates in the later build lane, when the
    producer reports delivery state, then it reports `DONE-AWAITING-TARGET`
    without an integration, release, deployment, or live-state mutation.
19. **A19 — live notice plus durable same-event recovery (R18, R20, R23-R26).**
    The deterministic matrix uses one typed progress row with nonnull
    `effectKind` and one acknowledgment row with null `effectKind` on the same
    assignment. It proves all of these boundaries:

    - **Connected live delivery.** With an authorized ChangeSocket consumer
      authenticated and `subscription_ready` for `attest.filed`, filing both
      rows emits post-commit live notices whose `refs.attestId`, `payload.id`,
      kind, and stored `effectKind` equal the mutation response and durable
      row. The socket `seq` is asserted only as connection-local delivery
      order.
    - **Disconnected recovery across nonmonotonic order.** After the consumer
      durably records a prior id in its seen-id set and disconnects, a later
      row is inserted with the same timestamp and a lexically lower UUID. A
      separate fixture appends a later row after forcing its wall-clock
      timestamp below the prior row. No live backlog is expected. In each
      fixture an unpaged `attests <assignmentId>` read includes both exact ids,
      and the set difference returns the later appended id exactly once even
      though it sorts before the prior id. A control assertion proves
      `--after <prior>` would return neither regression row and is not used for
      recovery.
    - **Reconnect race and duplicate suppression.** The consumer reconnects,
      reaches `subscription_ready`, buffers live notices, and walks the query
      while a barrier releases one filing. Both legal commit positions —
      before and after the unpaged query statement — converge to the same id
      set through the query, live buffer, or both. A row delivered by both
      paths is processed once by id; two distinct ids with byte-identical kind,
      note, timestamp, and effect kind remain two facts. Forced consumer
      crashes at the effect/seen-id boundary prove the shared-transaction form
      commits both or neither and the external-effect form safely retries by
      canonical attest-id idempotency.
    - **Gateway and consumer restart.** With the database preserved and the
      live hub replaced, a fresh gateway plus a fresh consumer holding only
      the durable seen-id set recover the same rows, ids, kinds, and stored
      types through a new unpaged read. This is run for both the same-timestamp
      lower-UUID and wall-clock-regression fixtures. The test asserts the new
      hub emits no historical notice.
    - **Gap and read failures.** An in-connection `seq` gap triggers the same
      unpaged reconciliation. A transport failure, missing principal, process
      principal, and unknown assignment leave the durable seen-id set
      byte-identical. The supported retry begins another unpaged read; it does
      not invent or resume a cursor.
    - **Authorization, filter scope, and privacy.** The existing permitted
      session and user principals recover the same rows; a process and missing
      principal receive the R23 403 failures; an unknown assignment receives
      the R23 404 failure. Recovery is run per exact assignment id, never by
      treating a work-item, session, origin, principal, or subscription filter
      as a replay cursor. No read or notice gains a field, note, or assignment
      outside its existing projection and authorization.
    - **Projection identity.** Mutation response, paged and unpaged `attests`,
      work-item trace, work-state detail, every abbreviated public attest row,
      and connected live notice emit the same stored `effectKind`. No
      projection derives a different value from the parent, and no recovery
      path synthesizes a new event id.
20. **A20 — guidance refractions (R9, R27).** Given the
    candidate product and served-identity tree, when a deterministic guidance
    scan runs, then the operating manual contains the exact seed and path
    mapping in Architecture 7; the unblocking skill names acknowledgment,
    surrender, and the historical-progress fallback; and the recon-lifecycle
    skill names acknowledgment for findings beyond the assigned question. The
    scan finds no instruction that files a current blocker or an out-of-scope
    finding as progress. The coder ready-for-review, orchestrator
    first-progress, and recon-first root-cause progress instructions remain.

## Open Questions

None. This proposal has no blocking or non-blocking holes. A source change that
falsifies an assumption returns to the spec-writer as an amendment request; it
does not authorize the builder to guess.
