# Typed progress attests

Status: PROPOSAL for one different-session independent review. This spec is
targetless. It authorizes no product integration, release, deployment, live
mutation, identity edit, or configuration change.

Authority: Mike ruling `art_e15670c9` (SHA-256
`26a9ce6832c1e442ce18dddf0b00768a2b23158442072fe256ad29b9046ff3e3`) and
spirit verdict `att_9c95b557-c4d2-4c73-be9f-6d24d3a22390` on work item
`wi_990f7b7e-837b-4aba-8f2e-ac6617327d78`. This spec amends `attest-v1.md`
and `effort-checkin-v2.md` only where this text names a change. Their other
clauses remain in force.

Source evidence: Tightbeam `origin/main` commit
`8e269e89c04b6b8569813142a12742f3325b8503`; tightbeam-specs `origin/main`
commit `1bb5881b9813f24e61cc3760e34a7a36cbddb805`. Code is evidence for the
current seams. The ruling above is the behavior authority.

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
   acknowledgment turn. An acknowledgment row records traffic when the holder
   elects to preserve it; it does not prove compliance with a directive.
7. This spec does not rewrite or backfill a historical attest.
8. This spec does not add an idempotency key to `attest`.
9. This spec does not select or request an integration, release, deployment,
   or live-state target.
10. This spec does not edit the operating manual. It supplies the seed text
    that a later implementation change must land with the capability.

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
  `acknowledgment`, whose `effectKind` is null, and whose note names the ruling
  receipt or coordination traffic that the holder records.
- **Historical untyped progress:** a progress row that predates this contract
  and therefore stores `effectKind = null` after migration.
- **Attest-channel effect credit:** the effort check-in's finding that at least
  one eligible attest row exists after its recorded attest watermark. This
  term does not include the other three effect channels.
- **Mismatch:** an explicit progress type that belongs to the enum but differs
  from the assignment effect kind.
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
6. At source commit `8e269e89`, the current database shape stamp is
   `coordination-fabric-v1-phase1-v6`, and the schema layer accepts only named
   predecessor migrations.
7. At source commit `8e269e89`, the CLI prints the gateway's JSON success
   object without a second semantic rendering layer.
8. A builder will stop and return to the spec-writer if the source facts above
   change before implementation.
9. `completion-escalation-rail-v2.md` reserves the unqualified successor stamp
   `coordination-fabric-v1-phase1-v7` for a separate targetless candidate.

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
    kind makes non-effect traffic representable without recasting it as
    progress.
11. This work stays targetless through reviewed-clean code and green gates.
    The later delivery state is `DONE-AWAITING-TARGET`.

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

R4. For `kind=acknowledgment`, the handler requires a nonblank `note` under the
existing 2,000-character limit. The handler stores `effectKind = null`, leaves
the assignment open, and runs no progress transition.

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
`kind` constraint gains `acknowledgment`.

R11. The table attribution constraint admits acknowledgment only with
`bySession` nonnull, `byUser` null, `verdictKind` null, `effectKind` null, and
`note` nonnull. The constraint admits progress with a holder session and a
nullable effect kind so historical rows remain representable. Completion,
surrender, and verdict require `effectKind` null.

R12. A database trigger rejects a new progress insert whose `effectKind` is
null. A second database trigger rejects a new progress insert whose
`effectKind` differs from the parent assignment's resolved effect kind. The
handler maps its own pre-insert checks to the typed errors in R3 and R6; a
trigger failure is an invariant breach, not a public mismatch path.

R13. The targetless candidate shape is
`coordination-fabric-v1-phase1-v7-typed-progress-attests`. It accepts
`coordination-fabric-v1-phase1-v6` as the sole predecessor for this migration.
This feature-qualified name does not claim the unqualified v7 stamp reserved by
`completion-escalation-rail-v2.md`. A later integration-target ruling that
composes schema candidates must amend this spec before source work continues.
The migration uses the repository's foreign-key rebuild transaction to:

1. create the successor `attests` table;
2. copy each old row with its explicit SQLite `rowid` and
   `effectKind = null`;
3. replace the old table;
4. create the two progress triggers;
5. run `PRAGMA foreign_key_check`; and
6. replace the shape stamp in the same transaction.

A crash exposes the predecessor shape and table or the complete successor. It
does not expose a mixed shape. A restart retries the named predecessor
migration. An unknown or partially assembled shape refuses with
`incompatible_typed_progress_attests_v1` and names the observed stamp or
object mismatch.

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
abbreviated attest row in a public projection also includes the field.

R19. Existing aggregate attest counts include acknowledgment under its stored
kind. An aggregate that reports progress counts only `kind=progress`; it does
not recast acknowledgment as progress.

R20. The existing attest event, marker, author columns, timestamp, note, and
parent relationship remain the audit record. The acknowledgment transcript
marker reads `[acknowledgment filed on <assignmentId>]`. The progress marker
keeps its current text because the response and row carry the type.

R21. This change adds no note to a projection that currently omits notes. It
adds no cross-principal lookup. The effort evidence in R16 exposes counts, not
note content.

### 6. Authorization, replay, and races

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

R24. `attest` remains non-idempotent. Two accepted requests append two attest
rows. A client that receives an unknown mutation outcome must read the
assignment's attest trail before it elects another filing. This spec does not
authorize an automatic retry.

R25. Concurrent progress or acknowledgment versus a terminal assignment
transition uses the current serialized transaction rule. The first committed
transaction wins. If the terminal transition commits first, the nonterminal
filing returns `assignment_closed` and writes no row. If the nonterminal filing
commits first, its row remains and the later terminal transition may close the
assignment.

R26. Schema restart, gateway restart, effort-generation replay, and firehose
replay read the stored `effectKind`. They do not derive a type for a historical
null. Preserved rowids keep each existing effort watermark ordered across the
migration.

### 7. Operating-manual seed and pattern

The capability teaches one operating pattern: progress is a typed effect
claim; acknowledgment is a non-effect record. The implementation change must
land this operating-manual seed with the shipped command:

> File `kind=progress` only for forward motion on the assignment deliverable in
> its `effectKind`. File `kind=acknowledgment` for a ruling receipt or
> coordination traffic. An acknowledgment does not count as assignment effect.

The manual must retain the no-acknowledgment directive: do not request an
acknowledgment turn for an ordinary directive or `fyi` delivery.

### 8. Subtraction ruling

ADD wins: deleting progress credit would discard Mike's ruled typed signal;
accepting the ambiguity would preserve regression `asg_3d219794` on
`wi_ecd8cd9d`. The addition uses one existing mutation seam, one stored field,
one new kind, and one equality predicate. It adds no content classifier or
decision mechanism.

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
4. **A4 — database rails (R10-R12).** Given a successor database, when a direct
   insert attempts new progress with null `effectKind`, then SQLite rejects the
   insert. When a direct insert supplies an enum value that differs from the
   parent assignment effect kind, then SQLite rejects the insert. Each attempt
   leaves the attest table unchanged.
5. **A5 — invalid value and scope (R5-R6, R23).** Given an open assignment,
   when the holder supplies an unknown value on progress, then the handler returns
   `invalid_effect_kind`. When the holder supplies an enum value on
   acknowledgment, completion, surrender, or verdict, then the handler returns
   `invalid_effect_kind_scope` with the exact messages and transport class in
   R23, and commits no mutation.
6. **A6 — acknowledgment contract (R4, R7-R9, R18-R23).** Given an open
   assignment of each effect kind, when its holder files acknowledgment with a
   nonblank note, then each response contains the exact acknowledgment message,
   each row has null `effectKind`, each assignment remains open, each public
   attest projection reports kind and null type, the firehose live notice and
   replay report the same null type, the transcript carries the exact R20
   marker, the acknowledgment aggregate increments without incrementing the
   progress aggregate, and no progress-only transition runs.
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
10. **A10 — historical rows (R10-R17, R26).** Given a stamped
   `coordination-fabric-v1-phase1-v6` database with progress, completion,
   surrender, and verdict rows, when the schema migrates, then ids, field
   values, foreign keys, and rowids match their predecessor values; each row
   projects `effectKind: null`; a historical progress row after an armed
   watermark increments `historicalUntypedProgress` and earns no effect.
11. **A11 — migration restart (R13, R26).** Given the predecessor fixture,
    when a forced exception interrupts migration after copy and in a separate
    run after table replacement, then each transaction rolls back to the exact
    predecessor stamp and rows. When the gateway starts again, one migration
    completes, foreign-key check returns empty, and the successor objects and
    stamp exist once.
12. **A12 — effort boundary race (R15).** Given one armed generation and one
    matching progress filing released on a barrier with the effort evaluation,
    when progress commits first, then the evaluation observes it. When the
    evaluation commits first, then that evaluation reports zero matching
    progress and the later row remains eligible only for a later generation.
13. **A13 — terminal race (R25).** Given one open assignment, when progress
    versus completion and acknowledgment versus revocation run on a barrier,
    then each race produces one of the two serialized outcomes in R25, with no
    orphan or partially written attest.
14. **A14 — non-idempotent replay (R24).** Given an open assignment, when the
    holder sends the same accepted progress request twice or the same accepted
    acknowledgment request twice, then the server stores two ids and the
    response does not claim idempotency.
15. **A15 — principal and privacy matrix (R21-R23).** Given an open assignment,
    when its holder, another session, a user, and a process each attempt both
    new forms, then only the holder succeeds. Existing authorized readers see
    `effectKind`; principals without parent-read access gain no row, count,
    note, or event access. Effort evidence contains no note text.
16. **A16 — CLI contract (R2, R8-R9).** Given the release CLI built from the
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

## Open Questions

None. This proposal has no blocking or non-blocking holes. A source change that
falsifies an assumption returns to the spec-writer as an amendment request; it
does not authorize the builder to guess.
