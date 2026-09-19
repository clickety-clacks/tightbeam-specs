# Terminal-child parent wake — reduced contract and implementation brief

Status: **ready for independent specification review; not implementation authority**  
Work item: `wi_236e5efa-b5a2-49b4-b6d5-9dcbe5e9fdad`  
Coordinator: `asg_e32bb9d9-9b55-4787-8e97-c3542f5f4f0b`  
Frozen historical producer: `asg_f627fbdf-3624-4823-90d5-35fefc39a2cf`

## 1. Authority and supersession

This specification is the exact reduced subject required by:

- Mike's scope correction `att_fd1c03c9-0aa8-4f4d-96eb-e297ee39d0b5`;
- PDO verdict `att_e1a670c5-b776-469c-b3ef-05eb21f3b7fc` and its bound reconciliation `art_11569cec`, SHA-256 `c8ab78d67563a8c9cd7c3a21cab1270dc57249ba184d85a1f0dfada94f0d265b`;
- PDO coverage/order verdict `att_e2db043f-4802-4865-aeaf-dd7b9923b48b` and `art_d72331cb`, SHA-256 `0e8cb22df8986414c605ea68b3a42e379c46e6290427e991b40ce06c1f917471`.

The historical reviewed contracts remain evidence for unchanged guarantees:

- `art_ead2e407`, SHA-256 `b1623a57fc2d17683e60e24c6a11921f64a1fb0ae17d2cb1f20e27ff0f879c92`;
- amended `art_90c8962c`, SHA-256 `d6e36b86354f93fdb48a5eeaedd796bb50bc7c62ccc74130f1d09274514d7f18`;
- reviewed revocation amendment `att_66bcd4fe-0cbb-4506-882d-2eac75064d6d` / `art_4b001733`.

They are not blanket approval of this changed subject. This reduced specification needs one independent specification review. It supersedes historical requirements only where this document says so.

## 2. Outcome

When a child assignment acquires a committed terminal result, Tightbeam durably admits one semantic owner-facing notification for that exact terminal event and eventually gives the current accountable parent or owner a truthful opportunity to act on it.

The notification carries enough durable identity, outcome, causality, and evidence to support a human disposition. It survives restart and a busy or changed owner, distinguishes admission from actual delivery, exposes failed or unknown delivery, and can be recovered without manufacturing another terminal outcome.

The mechanism does not choose the disposition. The accountable mind still decides whether the remaining work, session, or child should be retained, parked, reassigned, retried, or retired.

## 3. Terms

**Child** — the assignment whose durable state acquires a terminal result.

**Accountable parent or owner** — the current durable recipient derived from assignment/work ownership and lineage rows. Prompt text, shared work-item membership, role labels, and historical session ancestry alone are not authority.

**Terminal event** — one durable transition identified by its terminal source row, token, and timestamp. A failed turn is not a terminal assignment event.

**Notification admission** — durable creation or durable queue admission of the owner-facing notification. Calling a wake function is not admission unless its durable row commits.

**Delivery** — a scheduler/turn-ledger fact that the admitted notification reached an eligible recipient turn. Invocation or queue presence is not delivery.

**Semantic duplicate** — another attempt to represent the same terminal event and recipient purpose. It is not merely a similar message or another terminal event on the same assignment.

**Proved obsolete report** — an older machine/agent report for which a newer durable disposition on the same scope makes execution unnecessary. Ambiguous, unscoped, human, ruling, decision, or unique material-result messages are not proved obsolete.

## 4. Contract

### R1 — Durable identity

The terminal notification derives the exact child assignment, work item, accountable parent/owner relation, terminal outcome, causal source, terminal source token, terminal timestamp, and closing evidence from durable rows.

It must not infer the parent or owner from prompt text, a common work item, display name, role label, or session ancestry alone.

### R2 — Atomic admission where the terminal transaction owns both effects

Where the transaction committing the terminal result can also schedule or admit the owner notification, the two effects are atomic. Notification admission failure rolls back that terminal commit.

Where an existing seam cannot make both effects atomic, the terminal path must record an explicit, queryable, recoverable undelivered state in the existing wake/delivery machinery. It may not silently commit a terminal result while losing the owner's notice.

### R3 — Existing delivery machinery only

Delivery uses the existing wake queue, scheduler, turn ledger, lineage re-resolution, and bounded recovery. This work must not add a second scheduler, outbox, polling loop, generic close hook, notification framework, or supervision framework.

### R4 — Delivery-state truth

The durable state distinguishes at least:

1. terminal result committed;
2. notification admitted or queued;
3. delivered to an eligible turn;
4. delivery failed; and
5. delivery outcome unknown.

Only the scheduler/turn ledger can establish delivery. The sender or current owner can inspect failure or unknown delivery and invoke bounded recovery through the existing recovery seam.

### R5 — Event identity and retry

Retry or restart for the same terminal event returns or advances the same semantic notification. It does not create a second terminal result or a second independent owner obligation.

New revocation events use immutable `assignment_revocations.id` as the terminal source token and that row's `revokedAt` as the terminal timestamp. Revoke, reopen, revoke produces two distinct events. Historical `C.id`-keyed revoked notifications remain immutable read-only compatibility evidence; no new event emits that legacy identity.

A conflicting durable identity yields a named refusal without mutation.

### R6 — Current recipient and obsolete-result recheck

Immediately before delivery or claim, the substrate re-resolves the current accountable parent/owner and rechecks whether a later durable disposition has proved the queued machine/agent report obsolete.

Changing the recipient does not change terminal-event identity. Suppression is permitted only for a proved semantic duplicate or proved-obsolete eligible report. Human requests, rulings, decisions, unique material results, ambiguous or unscoped rows, and required audit history remain claimable.

### R7 — Restart, busy owner, and incomplete delivery

Restart before or after admission preserves one semantic notification. A busy owner does not lose it. An unavailable former owner re-resolves to the current accountable owner.

Failed or unknown delivery remains visibly incomplete and enters bounded recovery. Recovery must reconcile any prior invocation, turn-repair lineage, and durable delivery fact before retry; absence of a linked review or result alone does not prove absence of effects.

### R8 — Nonterminal children remain nonterminal

A child without a committed terminal result stays under its existing dependency wait, deadline, and bounded recovery. Silence, repeated notification, a failed turn, lack of owner response, or notification volume does not fabricate completion, death, irrelevance, or permission to retire.

### R9 — Disposition remains accountable

Delivery wakes a responsible mind; it does not complete, reassign, retry, retire, or select product disposition. The accountable agent decides retain, park, reassign, retry, or retire under its existing authority. No auto-retirement is introduced.

### R10 — Physical liveness remains separate

Physical liveness remains the computed diagnostic governed by `wi_4ef0bb82-7d16-4ddd-acff-54fbb516e80f`. Agent-authored progress, artifacts, attest prose, notification count, and owner response are not stored as physical-liveness truth and do not gate terminal-notification admission.

### R11 — Privacy, authority, and audit

Unauthorized, corrupt, or conflicting identity refuses without mutation. Notification content is limited to durable identifiers, outcome, causal source, timestamp, and evidence necessary for the accountable recipient to act. Original terminal, wake, message, delivery, repair, and disposition history remains auditable.

### R12 — Evidence applicability

Historical review and test evidence may be reused only for unchanged clauses or unchanged bytes and must remain attributed to its original subject. Changed specification text and the future combined implementation each require their own independent review.

## 5. Explicitly superseded mandatory machinery

The following are not requirements of this parent-wake contract and cannot gate it unless a later recorded finding proves one is necessary for a retained guarantee:

- F1-F4 and old supervision-file custody as universal gates;
- artifact cursors, progress-absorption rows, or liveness generations as proof of terminal delivery;
- a cooperative child pre-completion wake receipt ceremony;
- special immediate-session CLI `--key` behavior or a special Router target-kind protocol for that receipt;
- `receiptChildTurnSeq`, `receiptAcceptedGeneration`, `receiptCause`, or `receiptPrincipal` sidecar fields;
- completion refusal based on cooperative receipt generation;
- the v1-to-v2 `supervision_liveness_sidecar` rebuild and `terminal_child_receipt_v1` migration receipt;
- field-by-field cooperative replay fixtures and their dedicated CLI refusal surface;
- the historical sixteen-file implementation shape;
- acceptance cases whose sole purpose is to prove the superseded apparatus; and
- old instructions that every historical mechanism must survive or that this work may never be folded or narrowed.

This supersession does not delete historical evidence or authorize source removal. Redundant machinery may be removed only after the reviewed combined implementation proves replacement coverage.

## 6. Acceptance cases

Each acceptance case must be demonstrated on every later authorized target line for which implementation is commissioned. Fixtures should use existing public APIs and durable rows rather than test-only testimony.

### AC1 — Exact relation, not prompt inference

A terminal child with durable parent relation `P` produces a notification for `P` or its current accountable owner even when prompt text, shared work item, or session ancestry suggests another recipient. Missing or corrupt durable relation refuses without mutation.

### AC2 — Completion payload

A committed completion notification contains the exact child assignment, work item, parent/owner relation, outcome, causal source, terminal token/timestamp, and closing evidence. A failed child turn produces no terminal notification.

### AC3 — Revocation payload and repeated revocation

A revocation uses `assignment_revocations.id` and `revokedAt`. Revoke/reopen/revoke produces two distinct terminal notifications. Retry of either event remains idempotent. No new legacy `C.id` identity is emitted.

### AC4 — Retirement-interruption outcome

An interruption or retirement-related terminal path that leaves an accountable obligation admits a truthful owner notification and retains the evidence needed to decide the remaining disposition. It does not auto-retire or declare the work irrelevant.

### AC5 — Atomic terminal admission

Injected notification-admission failure in a transaction that owns both effects rolls back the terminal result. A seam that cannot be atomic records an explicit recoverable undelivered state; it never silently loses intent.

### AC6 — Invocation is not delivery

A scheduled or invoked wake without a delivered eligible turn remains admitted/queued or delivery-unknown. Only the matching scheduler/turn-ledger fact changes it to delivered.

### AC7 — Restart boundaries

Restart before notification admission leaves no committed terminal result where AC5 requires atomicity. Restart after admission but before delivery preserves exactly one semantic notification. Restart after delivery does not redeliver the same event absent an authorized recovery of an actually incomplete delivery.

### AC8 — Busy, unavailable, and changed owner

A busy owner retains the admitted notification. If the historical owner becomes unavailable or responsibility changes before delivery, the same event routes to the current accountable owner. The old recipient is not treated as proof of delivery.

### AC9 — Failed and unknown delivery recovery

Failed and unknown delivery are queryable. Bounded recovery first reconciles wake, turn, and repair lineage, then advances the same semantic notification without minting a second terminal result or duplicate review/staffing obligation.

### AC10 — Duplicate suppression

Two attempts for the same terminal event and recipient purpose yield one claimable semantic notification. A conflicting identity yields a named refusal and no mutation.

### AC11 — Obsolete-report suppression boundaries

An older machine/agent report is suppressible only after a newer durable same-scope disposition proves it obsolete. Human requests/rulings, decisions, unique material results, ambiguous/unscoped rows, and continuation-originated turns remain claimable.

### AC12 — Nonterminal child

A child with no committed terminal result retains its dependency wait, deadline, and bounded recovery. Silence, failed turns, repeated notices, or absent owner response never fabricate terminal state.

### AC13 — Accountable disposition

Successful delivery changes no assignment outcome, session lifecycle, work-item state, product decision, or staffing by itself. A separate accountable action is required to retain, park, reassign, retry, or retire.

### AC14 — Liveness separation

Progress attestations, artifact filings, owner responses, and message count cannot set or replace computed physical-liveness truth. The separate diagnostic remains query-only input and is not a terminal-event gate.

### AC15 — Cancellation and retirement races

The combined seam exposes enough exact identity and recovery state for the existing cancellation-provenance lane to prove typed reason, requester, causal source, replacement/disposition linkage, rollback, restart safety, and no silent orphan. Cancellation implementation follows the reviewed combined seam; it is not parallel first-touch work.

### AC16 — No replacement framework

Source and schema census shows the outcome is implemented through existing wake, ledger, scheduler, turn, assignment, and recovery mechanisms. No second scheduler/outbox, polling loop, generic close hook, notification registry, cooperative receipt protocol, or supervision sidecar is introduced.

## 7. Dependency and ownership map

| Order | Existing work/custody | Required result | Boundary |
| --- | --- | --- | --- |
| 0 | Historical producer `asg_f627fbdf` / `s_cb647d0b` | Preserve old candidates, drafts, patches, gates, and reviews as provenance. | Frozen and read-only; no wake, edit, gate, push, or adoption. |
| 1 | Stale-message owner `asg_b95aa412-e17f-4a71-9185-ff8ff18ee6e5`; producer `asg_b54dec3d-8462-417a-83b2-448a4db64600`; candidate `140ab59d28b9bbaebd4f2f9cc2e469ee81d322de` / tree `2d0b5400` | Existing changed-subject independent review, then its already-authorized macOS/line disposition if clean. | Sole first-touch custody for `gateway.ex`, `ledger.ex`, `schema.ex`, `queued_message_suppression.ex`, and its tests. No duplicate review/gate. |
| 2 | This coordinator `asg_e32bb9d9` | This exact reduced specification and one independent reviewed-clean verdict. | No code authority; review is of this changed subject, not an empty confirmation of historical review. |
| 3 | Wake-delivery item `wi_113d569f-7aff-412b-aec3-0c21f2e87f40`; coordinator `asg_abbd8e46-bd4b-4e8e-b6ac-0925a2bc3129`; source owner `asg_19d32a78-e2e0-47af-98ea-50327ee7ae35` / `s_fd3a9283` | Reuse reviewed/current wake admission, delivery-state, failure/unknown, restart, and bounded-recovery semantics. | Historical `26ce6e9e` and 0.1.9 WIP are comparison evidence, not edit-base or cherry-pick authority. |
| 4 | Future combined seam; selected eligible executor remains `asg_19d32a78` only after a later PDO execution-control row | One fresh candidate combining accepted stale-message boundary, wake lifecycle, and terminal owner notification on exact authorized bases. | No execution until step 1 disposition, reviewed-clean step 2, exact target/base authority, shared-hunk release, and a later PDO control record. |
| 5 | Cancellation source `asg_6b3247e4-8858-4b21-8e30-e8bb33e6dcbb` / `s_0184755c`; wire fixture `asg_933e6f72` / `s_fcdd77af` | Consume the exact reviewed combined seam and close AC15 follow-on behavior. | Follows, never edits in parallel; `asg_933e6f72` retains `test/wire_seam_test.exs`. |
| 6 | `wi_809821f8`, `wi_d884d359`, `wi_86165cfa`, and other named overlap owners | Close already-covered behavior as no-op dependency dispositions; retain only specifically uncovered behavior on its existing item. | No imported framework or duplicate producer. Delivered `wi_21c95808` stays delivered; held `wi_fcbc79fe` is not contacted; `wi_4ef0bb82` stays diagnostic. |

## 8. Future implementation brief

This section constrains a later PDO-controlled source assignment. It does not start it.

The smallest implementation should touch only seams proved necessary by reviewed source census. PDO has preallocated the likely shared sequence as follows:

1. existing wake outcome/admission/delivery/failure projection in `lib/tightbeam/wakes.ex`, `lib/tightbeam/ledger.ex`, `lib/tightbeam/gateway.ex`, `lib/tightbeam/productions/bubble.ex`, and the existing CLI projection only if a retained acceptance case cannot be observed without it;
2. terminal-event emission from existing completion, revocation, and retirement owner transactions, deriving durable child/parent/current-owner identity and the reviewed revocation token; and
3. focused tests for restart, owner change, failed/unknown delivery, event dedupe, nonterminal waits, cancellation/retirement races, privacy, and refusal.

The later executor must begin from exact authorized current bases after shared-hunk release. It must stop on semantic drift or custody conflict. It must not reconstruct the historical sixteen-file design, import cooperative receipt/sidecar/progress-generation machinery, or add a general framework without a new recorded necessity and product ruling.

The future candidate needs one independent code review of its exact changed subject and exact-candidate hosted gates required by then-current delivery law. Historical tests and reviews do not substitute for those gates.

## 9. Holds and next transition

This document authorizes only its own independent specification review.

It does not authorize source edits, target/base movement, local or remote product tests, CI/workflow execution, pushes, branches, pull requests, merges, publication, release, package work, installation, service or adapter action, schema/database mutation, credentials, live state, Firehose action, or contact with frozen/held sessions.

The frozen producer remains frozen. The only current transition is:

1. record this exact artifact and SHA;
2. obtain one independent specification verdict on this changed subject; and
3. if reviewed-clean, emit `po-wake-scope-reconciled` for `wi_236e5efa-b5a2-49b4-b6d5-9dcbe5e9fdad` with this artifact, its review report/verdict, and the still-controlling downstream dependencies.

No source lane resumes merely because the specification is reviewed-clean. PDO must later issue the exact execution-control row after every condition in the dependency map is satisfied.
