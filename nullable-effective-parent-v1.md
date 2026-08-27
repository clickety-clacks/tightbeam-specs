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
`art_ae962883`. Lifecycle-correlation repair authority:
`wi_708db495-1fe6-486a-933e-91f1216c4219`, changes-requested verdict
`att_dd1ca4f0-8b58-4e00-a858-b122a4619982`, and report `art_eb59029e` at
SHA-256 `2bcb2950762321c19a3ce4805deaf1196b48e85fad3adda15dc5911e97193ec6`.

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

Close the existing terminal corollary's supervision-coverage ambiguity with one durable
controller root link. Only the failed assigned turn and assignment named by that link can
receive coverage or duplicate suppression from the controller.

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
9. This spec does not revive the lifecycle source store, candidate ladder, or Main marker
   from `assignment-lifecycle-fallback-escalation-v1.md`. That file and closed
   `wi_3d6d13a0-c4cf-4370-88a1-b407c41ff7c1` supply no separate implementation authority.

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
- **Supervision controller**: a `supervision_liveness_sidecar` row whose `controllerOrigin`
  is `scheduled` or `retirement_elevation`, together with the wake identified by its
  `wakeId`. Its recorded recipient is that wake's `sessionKey`.
- **Controller root link**: the immutable tuple `(wakeId, assignmentId, rootTurnSeq)` on a
  supervision controller. `rootTurnSeq` identifies the terminal turn that caused the root
  scheduled controller, and that turn's `assignmentId` equals the tuple's `assignmentId`.
- **Exact supervision coverage**: a supervision controller whose controller root link
  equals the evaluated source's `(assignmentId, turnSeq)`. A pending controller is pending
  coverage. A delivered controller turn is `resolved_existing` coverage. A terminal
  non-delivered controller is a prior attempt only for that exact source and its recorded
  recipient. These are derived query results, not stored controller states or markers.
- **Historical unknown correlation**: a migrated supervision controller, or a later
  retirement elevation descended from it, whose `rootTurnSeq` is null. This is a named
  stored value, not evidence for any source.
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
9. On the main baseline, the supervision wake transaction already receives the causal
   terminal sequence as `supervision_terminal_seq`. On the 0.1.9 baseline,
   `Supervision.deliver_wake/5` has `pending.lastEvaluatedTerminal` but does not carry it into
   the wake transaction.
10. On both target baselines, the scheduled controller sidecar already stores the controller
    `wakeId` and exact `assignmentId` in the wake transaction.

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
11. **INV-11 — A controller names one root.** Each new scheduled supervision controller
    carries one non-null controller root link. A retirement elevation copies the source
    controller's link; only a retirement elevation descended from historical unknown
    correlation may retain null. The wake, sidecar, and link commit in one transaction.
    Settlement can change `controllerState`; no update or delete can change or remove the
    link, its wake identity, its recorded recipient, its root turn, or a delivered controller
    turn's attribution.
12. **INV-12 — Suppression uses exact identity.** `resolved_existing`, pending-coverage
    suppression, and prior-recipient suppression match both `rootTurnSeq` and
    `assignmentId`. They do not match `chargedGeneration`,
    `supervision_watermarks.lastEvaluatedTerminal`, pending watermark fields, or
    `assignmentId` alone.
13. **INV-13 — Missing identity fails safe.** Historical unknown correlation, a mismatched
    link, or an absent link supplies no coverage and suppresses no parent action. The
    consumer continues through its existing effective-parent path. This can produce a
    duplicate for historical data; it cannot silently discard the evaluated source.

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
10. **ARC-10 — Embedded controller link.** Both arms add nullable
    `supervision_liveness_sidecar.rootTurnSeq INTEGER REFERENCES turns(seq)` to the existing
    sidecar; they add no link table or lifecycle store. The sidecar's existing
    `assignmentId` and `wakeId` complete the controller root link. The scheduled-controller
    insert validates that `rootTurnSeq` is non-null, that the named turn exists, and that the
    turn's `assignmentId` equals the sidecar's `assignmentId`. On main, the Gateway wake seam
    passes its existing `supervision_terminal_seq` into `Supervision.transition_in_txn/2`.
    On 0.1.9, `Supervision.deliver_wake/5` adds
    `supervision_terminal_seq: pending.lastEvaluatedTerminal` to its reserved-process wake
    parameters, and the Gateway wake seam passes that value into the same transition. The
    transition inserts the wake, sidecar, and link under the existing wake transaction. The
    mutable watermark supplies the scheduling input once; no coverage or suppression query
    reads it after the link commits. A retirement elevation inserts `rootTurnSeq` by selecting
    it from the source-controller row identified by the existing accepted transfer's
    `wakeId` and the same assignment; no caller supplies the copied value. An exact source
    link therefore stays exact; a historical null stays null. A check or trigger refuses a
    new scheduled controller without a link, and an elevation insert that does not select
    exactly one same-assignment source controller refuses its transaction. Immutability
    rails refuse an update to `wakeId`, `assignmentId`, `controllerOrigin`, `wakeKind`,
    `rootTurnSeq`, or the linked wake's `sessionKey`; refuse deletion of the controller
    sidecar, wake, or root turn; and preserve the root turn's `seq` and `assignmentId`. They
    let only the existing controller-state transition settle the sidecar. Once a controller
    turn exists, rails also preserve its `seq`, `sessionKey`, `wakeId`, and `assignmentId`.
    The foreign keys preserve the linked wake and root turn.
11. **ARC-11 — Exact coverage query.** The terminal corollary joins a controller sidecar to
    its wake and, when present, the controller turn. It accepts coverage only when the
    sidecar's `(assignmentId, rootTurnSeq)` equals the evaluated source's
    `(assignmentId, turnSeq)`. A controller turn supplies delivery or prior-attempt evidence
    only when its `(wakeId, assignmentId, sessionKey)` equals the linked wake's recorded
    values. Queued or running exact coverage delays the existing parent action. Delivered
    exact coverage yields `resolved_existing`. A terminal non-delivered exact controller
    suppresses a duplicate only for its immutable recorded recipient and lets the consumer
    continue through the resolver. A historical null or mismatched pair derives
    `historical_unknown` or `different_root` and supplies no coverage. The query does not
    read controller generation, terminal watermarks, pending watermark fields, or
    assignment-only correlation.
12. **ARC-12 — Correlation migration and compatibility.** Each arm includes the sidecar
    change in its one successor shape migration. The migration preserves every existing
    sidecar column value byte-for-byte and sets the new `rootTurnSeq` column to null. It does
    not infer a root from `chargedGeneration`, terminal watermarks, pending watermark fields,
    wake times, or the latest turn on the assignment. New scheduled controllers require the
    link after the successor stamp commits. Fault injection leaves the complete predecessor
    or complete successor shape. ARC-07's rollback rules apply to the link: an old binary
    refuses the successor stamp before writes, and rollback never strips a link while
    preserving later successor writes.
13. **ARC-13 — Corollary boundary, races, and restart.** The link changes only how the
    existing terminal corollary recognizes supervision coverage. Parent selection remains
    INV-02's resolver, and the corollary gains no source store, candidate ladder, marker, or
    mutation seam. The controller transaction and the parent-action transaction use the
    existing database serializer. If the exact controller link commits first, the
    parent-action check observes it and suppresses that action. If the parent action commits
    first, a later controller does not erase the action or rewrite its result. That is the
    valid pre-coverage ordering: a later evaluation sees the exact link and writes no
    additional parent action. Restart reads the committed link; it does not reconstruct one
    from mutable supervision state.

Subtraction decision for the correlation repair: ADD one field to the row that already owns
the controller. DELETE loses because exact supervision coverage remains an elected
duplicate-suppression input. ACCEPT loses for new controllers because assignment-only
matching can silently discard a later root; historical null rows remain the bounded named
failure value.

Agent operating pattern taught: none. This repair changes substrate correlation only.

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
13. **AC-13 — Exact controller match.** Given failed assigned turns `T1` and `T2` on
    assignment `A`, and delivered controller `W1` linked to `(A,T1)`, when the terminal
    corollary evaluates `T1`, then it returns `resolved_existing` and writes no duplicate
    parent action. When it evaluates `T2`, then `W1` returns `different_root`, suppresses
    nothing, and the consumer follows the effective-parent path. Replacing the exact-link
    predicate with assignment-only, generation, watermark, or pending-field correlation
    makes this test fail. Given retirement elevation `W2` from `W1`, then `W2` retains
    `(A,T1)` and its delivered turn resolves `T1`, not `T2`.
14. **AC-14 — Atomic and immutable link.** Given a new scheduled controller, when fault
    injection stops each write point in the wake transaction, then the database contains
    the wake, sidecar, and valid controller root link together or contains none of them.
    Given main's existing `supervision_terminal_seq` carrier and 0.1.9's new carrier from
    `pending.lastEvaluatedTerminal`, when each arm schedules a controller for `(A,T1)`, then
    each committed sidecar stores `(A,T1)`. Overwriting the watermark with `T2` after commit
    changes neither link.
    Given the committed row and its controller turn, when a writer changes `wakeId`,
    `assignmentId`, `controllerOrigin`, `wakeKind`, `rootTurnSeq`, the wake's `sessionKey`,
    the root turn's `seq` or `assignmentId`, or the controller turn's `seq`, `sessionKey`,
    `wakeId`, or `assignmentId`, or deletes the controller sidecar, wake, root turn, or
    controller turn, then the database refuses the write. Changing `controllerState` from
    `pending` to `settled` preserves the link and attribution. Given a retirement elevation
    from that controller, fault injection commits its wake, copied link, sidecar, and turn
    together or commits none.
15. **AC-15 — Historical compatibility.** Given a predecessor database containing a
    scheduled controller for assignment `A`, when either arm migrates it, then the copied
    row has `rootTurnSeq = null` and reports `historical_unknown`. When the corollary
    evaluates a source on `A`, then that row does not produce `resolved_existing` and does
    not suppress the parent action. Migration derives no root from generation, watermark,
    pending fields, timestamps, or another turn. Ten restarts preserve the null and add no
    inferred link. Given a later retirement elevation descended from that historical row,
    then it copies null, remains `historical_unknown`, and suppresses nothing. The
    predecessor binary refuses the successor stamp before writes.
16. **AC-16 — Controller race and restart.** Given one source and its controller schedule
    racing the parent-action transaction, when the controller link commits first, then the
    parent action observes exact pending coverage and writes nothing. When the parent action
    commits first, then a later controller does not delete or rewrite that action, and ten
    later evaluations add no parent action. Given a crash before the controller transaction
    commits, restart sees neither wake nor link and follows the effective-parent path. Given
    a crash after commit but before controller delivery, restart sees the exact pending link
    and does not create a duplicate parent action.
17. **AC-17 — Corollary source closure.** Given both successor diffs, review finds one
    controller-root field and its coherence and immutability rails on each line. It finds no
    new lifecycle source store, candidate ladder, Main marker, parent selector, or mutation
    verb. Each terminal parent action still obtains its target only from INV-02's resolver.

## Open Questions

None.
