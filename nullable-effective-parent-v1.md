# Nullable effective parent v1

Status: SPEC READY. Implementation is forbidden until one independent review accepts
this exact revision and Mike reads the reviewed revision.

Authority: `wi_cd2bb06d-a736-451c-98c3-428129bbe246`, Mike brief
`s_c43e373c-a6e1-4878-9224-a053e3304e2c`, target election
`att_b90d64e1-f333-4aba-b594-79d426c56b72`, visibility clarification
`att_d9d5b31d-9467-4514-8088-973e50d81e7f`, and controlling simplification
`att_e759139e-0ae6-4c96-a0f8-6ffc16e589df`. Compatibility receipt:
`att_aa1111e0-ebbe-4452-a09d-92f5cf08c472`. Missing-Main advisory:
`att_15fd37b3-5b07-4dfa-bdce-14047bbafa93` from source
`att_114c9b72`. Completion compatibility receipt: `att_d6bbed39` against
`art_ae962883`.

Target baselines: main/0.2.0 at `8e269e89c04b6b8569813142a12742f3325b8503`;
0.1.9 at `6c0eacb337c1de086d8d7d76f1c1dc57cad9a3d5`.

## Goal

Keep `sessions.operationalParent` nullable. Define one effective-parent resolver that
returns the stored parent when present and the session owner's canonical Main key when the
stored parent is null. Every parent-dependent consumer uses that resolver.

Apply textually identical resolver semantics in two separately reviewed release arms:
main/0.2.0 relaxes its unelected hard invariant, while 0.1.9 introduces the nullable
concept directly. Display stored and effective parent truth on every session surface.

A proposal that strengthens intent into a harder invariant requires its own ruling.
“Null parents default to Main” did not elect `NOT NULL`, stored self-roots, or bootstrap
machinery that manufactures explicit parents.

## Non-Goals

1. This spec does not implement, merge, release, deploy, restart, or mutate a live org.
2. This spec does not target 0.1.8.
3. This spec does not change `spawnedBy`, ownership, reparent authorization, role routing,
   model choice, or consumer-specific target eligibility.
4. This spec does not require a command that clears an explicit parent. Reparenting may
   continue to set an explicit parent.
5. This spec does not create a second resolver or a separate terminal-assignment fallback
   mechanism for `wi_3d6d13a0-c4cf-4370-88a1-b407c41ff7c1`.
6. This spec does not port main's bootstrap, cold-start, replay, or activation subsystems
   to 0.1.9.
7. This spec does not make the governance rule a prose-parsing runtime rail.
8. This spec does not make 0.1.9 headless first-spawn legal and does not define or review
   the minimal add-user transaction on which that flow depends.

## Terms

- **Stored parent**: nullable `sessions.operationalParent`.
- **Owner Main**: the canonical Main session key derived from the source session's
  `ownerUserId`.
- **Effective parent**: the key returned by the resolver in `INV-02`.
- **Resolution source**: `explicit` for a non-null stored parent or `owner_main` for null.
- **Parent-dependent consumer**: any path that selects a parent for an escalation, prod,
  completion notice, ALWAYS-PARENT report, supervision climb, terminal-assignment report,
  or other parent-routed action.
- **Session surface**: any CLI, wire, query, topline, listing, detail, support projection,
  or ATC payload that presents a session.
- **main arm**: the main/0.2.0 constraint-relaxation release arm.
- **0.1.9 arm**: the 0.1.9 clean-introduction release arm.

## Assumptions

1. A session row has an immutable `ownerUserId`, and Tightbeam can derive that owner's
   canonical Main key without model output.
2. The elected main baseline has `operationalParent NOT NULL` and explicit stored values.
3. The elected 0.1.9 baseline has no `operationalParent` column.
4. Schema migration and parent-routed writes use the existing database transaction owner.
5. A parent consumer already owns its authorization, eligibility, idempotency, and named
   failure rules.
6. The reviewed completion contract requires raw `spawnedBy` target equality and treats a
   null parent as unavailable with no Main fallback. Those two rules conflict with Mike's
   later ruling and are replaced only as stated in ARC-04.
7. The reviewed exec-desk work has no semantic conflict. It consumes the resolver and owns
   no fallback or migration logic.
8. A 0.1.9 org can lack its canonical Main. Deriving a Main key does not prove that the row,
   first admin, credential, or admission receipt exists.

## Invariants

1. **INV-01 — Stored null is valid.** `sessions.operationalParent` accepts null on both
   target lines. Insert, boot, restart, migration, and projection do not replace null with
   a stored Main key.
2. **INV-02 — One resolution contract.** Both lines implement this exact resolver contract:

   > Read the source session in the caller's database transaction. If
   > `operationalParent` is non-null, return that exact key with source `explicit`.
   > Otherwise return the canonical Main key derived from the source session's
   > `ownerUserId` with source `owner_main`. Do not read `spawnedBy`. Do not write.

3. **INV-03 — Every consumer uses the resolver.** The resolver is the only production
   parent-selection rule. Every parent-dependent consumer calls it. A consumer applies its
   existing target eligibility and action rules after resolution. When an existing contract
   climbs past an ineligible target, it calls the same resolver again with that target as
   the next source. The resolver itself does not climb, skip, or judge eligibility.
4. **INV-04 — Provenance stays provenance.** `spawnedBy` remains immutable creation
   provenance. Reparenting changes only `operationalParent` and need not support clearing it.
5. **INV-05 — Explicit values survive.** Migration preserves each explicit stored parent
   byte-for-byte. A null resolves at use time and is never backfilled for convenience.
6. **INV-06 — One committed ordering.** Resolution and a parent-routed write share one
   transaction when the consumer requires an atomic check and action. Restart adds no cache
   or alternate rule.
7. **INV-07 — Authorization does not widen.** The resolver grants no authority. The source
   row supplies `ownerUserId`; callers cannot nominate the fallback owner. A missing or
   ineligible Main produces the consumer's named failure and no misrouted action.
8. **INV-08 — Surfaces show stored and computed truth.** Every session surface exposes
   `operationalParent`, `effectiveParent`, and `effectiveParentSource`. Stored null remains
   visible as null while the computed fields show Owner Main and `owner_main` unambiguously.
9. **INV-09 — Owner Main is a fixed point.** An Owner Main with stored null resolves to its
   own canonical key. A consumer detects that fixed point before another hop.
10. **INV-10 — Terminal fallback is a corollary.** The terminal-assignment owner-Main
    behavior bound to `wi_3d6d13a0` is a corollary of INV-02. It has no separate fallback
    path, candidate ladder, marker, or lifecycle store.

## Architecture

1. **ARC-01 — Shared helper.** Both arms expose one transaction-aware
   `Tightbeam.Org.effective_parent_in_txn/2` with the exact INV-02 behavior. It accepts the
   transaction and source session key. It returns the effective key, resolution source, and
   source owner. An unknown source returns the line's named missing-session result.
2. **ARC-02 — Main migration.** The main arm rebuilds the current complete `sessions` table
   with nullable `operationalParent`. It copies every row and explicit parent unchanged,
   recreates the line's indexes and foreign keys, advances one shape stamp, and commits only
   after the existing integrity checks pass.
3. **ARC-03 — 0.1.9 migration.** The 0.1.9 arm introduces nullable `operationalParent`.
   Every pre-feature row receives stored null because that line has no elected
   operational-parent history. It does not infer a value from `spawnedBy` and does not pass
   through a `NOT NULL` design. The migration does not create a missing canonical Main.
4. **ARC-04 — Consumer substitution.** Escalation, prod, completion notice, ALWAYS-PARENT
   reporting, exec-desk escalation, and terminal-assignment reporting call the shared
   resolver. In `completion-escalation-rail-v2.md` Goal, Terms, R5, A8, and A21, effective
   parent replaces raw `spawnedBy` as the completion target and equality source. A non-null
   stored parent therefore keeps the existing explicit-parent route. Null selects Owner
   Main before R5 applies its existing target checks; null alone is not unavailable. A
   missing or ineligible selected Main still takes R5's named unavailable outcome. The
   report-to target continues to come only from explicit `reportTo`; its existing
   shared-parent deduplication remains. Disposition authority, owner checks, deadlines,
   idempotency, and all other completion rules remain unchanged. These two parent-source
   rules are the only reviewed-contract contradictions.
5. **ARC-05 — Session surfaces.** Session serializers compute effective parent through the
   shared resolver. They add the additive fields `effectiveParent` and
   `effectiveParentSource` beside nullable `operationalParent`. The same meaning applies to
   session detail, list, topline, support,
   transcript-facing, and ATC projections. An implementation inventory names every
   session surface before its arm can pass review.
6. **ARC-06 — Deletion inventory.** The main arm deletes machinery whose only purpose is
   to satisfy the unelected non-null invariant: the `NOT NULL` clause; migration inference
   from kind or provenance; required stored self-roots; creation-time parent manufacture;
   `resolve_personal_main_defaults/1`; `ensure_personal_main_in_txn/3`; the internal
   `bootstrap-user` route; self-root receipt proof; and consumer-local parent selection.
   This spec binds, but does not absorb, a separately reviewed minimal add-user transaction.
   Before headless spawn, that transaction creates the first admin, credential, canonical
   Main, receipt, and provenance. Existing main cold-start admission, authorization, replay,
   and activation outcomes remain unchanged. The 0.1.9 arm adds neither the obsolete
   machinery nor a constraint-relaxation migration. Resolver evidence alone cannot close
   0.1.9 headless cold-start.
7. **ARC-07 — Compatibility and rollback.** Each arm rejects an unknown predecessor without
   writes. Migration is atomic and restart-safe. Rollback before successor writes restores
   the captured predecessor database and binary. Rollback after successor writes requires
   restoring that capture with acknowledged later-write loss or a separately reviewed
   forward repair. An old binary never writes the successor shape.
8. **ARC-08 — Observability and closure.** Each arm records resolution source in existing
   parent-action observability where that record already accepts structured detail. Source
   closure permits direct stored-parent reads only in the resolver, migration,
   serialization, diagnostics, and tests.
9. **ARC-09 — Separate gates.** The canonical spec receives one parent-opened independent
   exact-hash review. Mike reads that reviewed revision before either implementation
   assignment opens. The main and 0.1.9 arms then receive separate producer cards,
   migrations, tests, reviews, landing decisions, and release gates. Evidence from one arm
   cannot satisfy the other.

**Headline release note — Parent routing for existing 0.1.9 sessions changes on upgrade.**
Every pre-feature session receives a null stored operational parent, so the shared resolver
selects its owner's Main for parent escalation. Delivery still requires that Main row to
exist and be eligible; otherwise the consumer records its named missing-target result.
Release evidence must name the observed live owner and relief sessions, 32 null-parent
roots, 423 superseded effort decision requests, and the ATC product-owner surrender. These
counts describe the elected snapshot; the release gate must recapture them because
knowledge rows can become stale.

## Acceptance Criteria

1. **AC-01 — Resolver parity.** Given explicit parent `P`, resolver tests on both lines
   return `P` with `explicit`. Given null, both return the source owner's canonical Main key
   with `owner_main`. Given an unknown source, both return the named missing-session result.
   The line fixtures produce textually identical successful results.
2. **AC-02 — Main migration.** Given the main predecessor fixture, migration produces a
   nullable column, preserves every stored parent and `spawnedBy` value, advances one shape
   stamp, and passes foreign key and integrity checks. Fault injection at each migration
   stage leaves the complete predecessor or complete successor, never an intermediate shape.
3. **AC-03 — 0.1.9 migration.** Given the 0.1.9 predecessor fixture, migration adds the
   nullable column with null for every copied row, advances one shape stamp, and adds no
   inferred parent or bootstrap subsystem. Fault injection has the same atomic result as
   AC-02.
4. **AC-04 — Surface truth.** Given explicit and null sessions, every enumerated session
   surface returns the stored value, computed effective key, and source. A null row renders
   as null plus Owner Main plus `owner_main`; it never masquerades as a stored explicit link.
5. **AC-05 — Consumer closure.** Given each named parent-dependent consumer, explicit and
   null fixtures prove that it calls the shared resolver and preserves its existing
   authorization, eligibility, idempotency, and named failure behavior. Static source
   closure finds no consumer-local read of `operationalParent` or parent fallback to
   `spawnedBy`.
6. **AC-06 — Cross-lane composition.** Given R5 fixtures where `spawnedBy` differs from a
   non-null stored parent, completion targets that explicit stored parent through the
   resolver. Given null and eligible Owner Main, completion targets Main instead of taking
   null-unavailable. Given null and missing Main, it records R5's named unavailable result.
   Report-to routing and disposition-authority fixtures pass unchanged. Exec-desk escalation
   uses the same resolver and owns no fallback mechanism.
7. **AC-07 — Terminal fallback.** Given terminal completion, surrender, revocation, or
   failed assigned-turn fixtures with null stored parent, the existing parent action targets
   eligible Owner Main once through the resolver. Source closure finds no separate
   implementation for `wi_3d6d13a0`.
8. **AC-08 — Failure, concurrency, and restart.** Given a missing, inactive, or foreign-owner
   Main target, the consumer records its named failure and writes no parent action. Given
   concurrent reparent and parent action, the recorded target and action match one committed
   ordering. Restart resolves from committed rows and no effective-parent cache.
9. **AC-09 — Deletion proof.** Given the main successor diff, review confirms every `ARC-06`
   deletion or a surviving non-parent requirement that justifies retention. Main's existing
   cold-start outcome fixtures pass unchanged. Given a 0.1.9 org without canonical Main,
   resolver tests return the derived key, the consumer records its named missing-target
   result, and headless spawn remains refused. Only evidence from the separately reviewed
   minimal add-user transaction can satisfy creation of the first admin, credential, Main,
   receipt, and provenance before headless spawn. Given the 0.1.9 successor diff, review
   confirms the obsolete bootstrap machinery was not introduced.
10. **AC-10 — Rollback.** Given a predecessor capture and successor shape, rollback tests
    prove the `ARC-07` paths and prove that the predecessor binary refuses the successor
    stamp before writes.
11. **AC-11 — Retroactivity evidence.** Given the release evidence for 0.1.9, it contains
    the headline paragraph, a fresh session-surface inventory, and a fresh
    count-and-identity capture for each named live-org consequence. A stale knowledge row
    cannot satisfy this gate.
12. **AC-12 — Review gates.** Given this exact spec hash, one independent reviewer accepts
    it and Mike records that he read the reviewed revision before either implementation arm
    opens. Each arm then supplies its own baseline proof, migration fixture, tests, review,
    and landing evidence.

## Open Questions

None.
