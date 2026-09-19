# Explicit addressed-PO consultation — 0.1.9

Work item: `wi_32f1f25b-570d-4fc5-8115-0a31e4d07299`.
Product owner: `product-owner:tightbeam`, session `s_fde9b2be`.
PO assignment: `asg_0f1ead2b-aef7-488c-abd6-74f934a32e28`.
Authority: Mike's 2026-09-19 request to define, implement, review and land this small change on 0.1.9.
Integration target: `refs/heads/0.1.9` only. Source inspected at `5d07645e186583cd3565002bd3aea3a49f55e2f8`; execution must reconcile the actual target tip.

## Spirit

The PO recommends team shape. The addressed delivery orchestrator adopts or amends that recommendation, staffs the work, and retains delivery custody. Give that orchestrator one timely consultation notice when an explicit PO association is established. The substrate records the association and delivers the notice; it does not choose topology or wait for agreement.

Success means one durable, attributable association and one logical notice for each actual association change. A retry, restart, unchanged setting, or unrelated role binding must not create another prompt. Staffing remains available before, during and after consultation.

## Smallest record and public operation

Add one durable current-association row per exact orchestrator session incarnation. Suggested table `session_po_associations` contains `sessionKey` (primary key), `ownerUserId`, explicit `poRole`, monotonically increasing `revision`, `noticeWakeId`, the setting principal/cause, and timestamps. Reuse ordinary event and request-idempotency records for history and replay; do not introduce a second notification ledger.

One explicit setter, proposed CLI `session-po-set --session <exact-session-key> --po-role <exact-role-address> --key <request-key>`, travels through the normal authenticated dispatch path. It returns the current association and existing/new notice wake ID. Provide current association readback through an existing session read surface; no new management UI is needed.

The PO reference is an exact, registered role address, not a role-name convention. At setting time it must resolve to an active same-owner session. The caller explicitly designates that address as the PO; no product-name matching, prefix matching, ancestor inference, automatic role discovery, or archetype-name heuristic establishes the relationship. Persist the role address and include it literally in the notice. A later role rebind does not itself create a new association or prompt.

Allow the owner user, the target session itself, or its current responsible parent to set the association, under the existing authenticated identity and owner checks. Refuse cross-owner, nonexistent, retired or malformed targets and unresolved PO addresses without partial effects. Do not grant unrelated peers authority merely because they share an owner. Use current-parent authority where applicable, not immutable historical creation lineage. This operation grants no new staffing or code authority.

The association is explicit for existing sessions as well as newly spawned sessions. This first change needs no implicit inheritance or spawn-time parameter: the responsible actor can call the setter after spawn. Migration starts with no inferred associations and emits no backfill notices.

## Trigger and deduplication

The setter is the only new trigger. In one serialized database transaction:

1. Validate authority and request fingerprint. A repeated request key returns its original response; conflicting parameters under that key refuse.
2. If the current exact PO address is unchanged, return the current association and notice ID without changing its revision or creating a wake. Persist replay semantics even for this no-op.
3. For the first association or an explicit replacement, advance the revision and create exactly one ordinary prompt wake using `Wakes.schedule_in_txn/2`, atomically with the association and replay record. Record the principal and cause. The wake targets the exact orchestrator session and carries the PO role and association revision.

An explicit A-to-B-to-A replacement is three intentional association revisions, not a retry. Each receives one logical notice. Never deduplicate solely by prompt text or role suffix.

Use the existing durable wake delivery, queue deduplication and bounded recovery paths. A transaction failure leaves neither association nor orphan notice. A restart after commit preserves the same wake, including a crash after delivery but before acknowledgement. Do not add a polling loop, new delivery worker, acknowledgement handshake, blocking rule, approval request, recurring reminder, or automatic consultation response. Normal recovery of a failed delivery is not another logical association notice.

The notice is unique material, not an assignment-liveness prod. Existing stale-liveness suppression must not discard it. It contains the explicit PO address and revision and tells the orchestrator to read the current association before acting, so a delayed notice cannot make an obsolete PO association authoritative. Existing pending-wake supersession may be reused if needed; do not build a general queued-message cancellation feature.

Suggested notice: “Your addressed PO is `<role>` (association revision `<n>`). Read the current association and consult that PO about team shape. The PO recommends; you adopt or amend the recommendation, staff, and retain delivery custody. This notice does not block otherwise authorized staffing.”

## Acceptance and tests

Exercise the production setter/dispatch, database, scheduler and queue paths with isolated fixture sessions. No model inference or live host session is needed.

- A valid explicit association creates the row and one notice carrying the exact PO role and revision, with cause/principal attribution.
- A same-key replay, unchanged setting with a fresh key, concurrent identical settings and restart/retry create no extra prompt. Key reuse with different parameters refuses.
- The no-op replay remains a no-op even after a later association change; it must not restore an obsolete address.
- Reopen the same fixture database across commit-before-delivery and delivery-before-acknowledgement cuts. The existing queue produces one logical notice, and the record/wake identity survives.
- A genuine replacement produces one new revision/notice; an old delayed notice cannot authorize consultation with an obsolete association. Rebinding the same PO role or renaming unrelated roles does not trigger another notice.
- Matching role names without an explicit association produce zero notices. Sessions created before migration receive no inferred association.
- Invalid, retired, cross-owner and unauthorized-peer cases produce no partial association, wake or replay success; a permitted current parent can set while a stale historical parent cannot.
- Spawn/assign/dispatch remains available with no PO association, a pending notice, or an unavailable PO. The trigger never inserts a staffing gate or waits for a PO reply.
- The notice remains claimable through existing liveness suppression and retains visible delivery failures through existing recovery.
- Prove schema upgrade/fresh initialization and normal readback, plus CLI/wire spelling and response tests. Run focused tests, then applicable canonical Linux/macOS gates on the exact candidate and independent review before guarded integration.

## Custody and scope limits

PO retains this Spirit and product acceptance. Existing PDO `s_777369c7` owns source staffing, shared-file allocation, proof, independent review, integration and recovery. Recommend one implementation holder and one independent reviewer; the PDO may adopt or amend that team shape with a recorded reason. Reuse existing qualified sessions where practical.

The producer may choose smaller equivalent storage/dispatch details, but must return any scope change before expanding. In particular, do not turn this into a generic relationship registry, role-management overhaul, topology optimizer, automated staffing scheme, or new notification framework. Preserve ongoing schema/wake work through PDO allocation.

Do not change 0.1.8 runtime rules or migrate a live database. On 0.1.8, use only the already-directed guidance and explicit human/agent handoffs. This work authorizes 0.1.9 source implementation, review and landing; it does not authorize release, installation, gateway restart, live test execution, main integration or changes to unrelated holds.
