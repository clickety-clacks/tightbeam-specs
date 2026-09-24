# Partial independent code review: engineering ownership enforcement at 504825b3

- Review assignment: asg_fca130e2-7f1d-486b-b7b2-183208f39fd8
- Producer assignment: asg_d0478bad-22c0-46e9-94f8-9838a5176dbf (coder:engineering-ownership-enforcement, s_4574cda7)
- Work item: wi_c13b63c8-b21f-47ce-bfac-61d51de854a4
- Subject:
  - Racter lane commit 504825b365a72e82b3357490819dbc535e5f97a5, tree 45367761258a0494b5349e5e54eb31b80079ca34, over e28880d6. The diff has 14 files, +2682/-16.
  - Local composition 36b0798e48dc0b59fb9b0b2cab83c3f0db898f5c (tree 40d68627), atop guidance 19eb9895.
- Verdict: changes-requested (PARTIAL). The producer is still amending. This verdict covers 504825b3 only. A successor commit needs a changed-hunk re-review against the findings below.

## Governing sources (hashes verified)

- Topology v2 art_790ca424 (SHA 0a1f65…) and v1 art_250b81dd (SHA 032905f…):
  - "Lane 2 authors executable rules."
  - Acceptance requires deterministic positive and negative coverage for these cases:
    - same-product accountable ownership
    - actual delegated scope
    - spawn and assignment/default-archetype/missing-item bypasses
    - bootstrap and consultation exceptions
    - reuse and succession
    - stale and cross-product authority
    - idempotent recovery
    - completion/failure routing
  - Refusals name the responsible delivery owner and a usable remedy.
- PO ruling art_469c22d7 (SHA cc40ac…):
  - A delegation identifies the active governing assignment/work and its existing authorized grantor.
  - Tests cover default-archetype and missing-item production calls, direct Main/PO production and stale delegation.
  - Succession is exercised with two items, open workers, normal completion, failure and an unavailable owner, and demonstrates "actual recipient/recovery behavior, not only database uniqueness or a sent notification".
- PDO packet art_5b91c742 (pending-review-points.md, SHA cf4fccb0…).
- Producer report art_8215447b (SHA c3c4f178…) and holder tests-passed att_5dde7841.

## Evidence used and its limits

- Source: `git show` of 504825b3 and 36b0798e, read-only on Racter.
- Files read in full: lib/tightbeam/delivery_responsibilities.ex and test/delivery_responsibilities_test.exs.
- Files read for the relevant hunks: assignments.ex, rules.ex, gateway.ex, router.ex, cli/src/dispatch.rs, session_po_associations.ex, pdo.toml, archetypes_test.exs, scripts/engineering_identity_evidence.exs.
- Also read: priv/kungfu/agentic-engineering/rules/engineering.toml.
- Nothing was run. I did not reproduce the test counts in the holder report (Mix 2662/0, Rust 383/0, focused 58/0). I accept them as the holder's record of what those suites exercise. They do not exercise the behavior named in B1 to B3.

## Findings

### B1, blocking: no production-admission rule ships, so the topology rail is not enforced

- engineering.toml is byte-identical in 504825b3 and 36b0798e. It contains only `completion-requires-review`.
- `validate_assignment_delegation_in_txn` returns `:ok` whenever `delegates_delivery` is absent or false. So an ordinary `assign`, `dispatch` or `spawn` is admitted whatever the caller's delivery responsibility. That covers:
  - direct Main or PO production,
  - a missing or unknown work item,
  - a default-archetype spawn.
- The neutral facts are adequate inputs:
  - `caller.delivery_responsibility`
  - `target.delivery_responsibility`
  - `work_item.reference_state`
  - `work_item.delivery_owner_ref` and `work_item.delivery_owner_state`
  - `assign.delegates_delivery`
  - For spawn, the facts read `workItemId` through the router's generic underscore mapping.
- The only rule coverage (the test at line 381) writes a temporary `delivery.toml` in a tmp identity dir and calls `Rules.decide` directly. It proves the facts evaluate. It does not prove that the shipped engineering policy refuses anything, or that a real `assign`/`dispatch`/`spawn` call through the gateway is refused or admitted.
- Consequence: the acceptance items "direct Main/PO production", "default-archetype and missing-item production calls" and "refusals name the responsible delivery owner and usable remedy" are unmet.
- Mike's audit (c883506c) is correct on the actual bytes.
- The remedy home is right. Executable rules belong in the engineering kungfu rules (or the topology rules file this lane owns), not in new runtime special cases. The runtime should stay neutral.
- Acceptance needs end-to-end gateway calls, not only `Rules.decide`, with the shipped rules loaded. They should show:
  - Refused: Main, the PO and an unrelated same-user session commissioning production on a bound item; production with an omitted work item; production with an unknown work item; spawn with no work item through the default archetype.
  - Admitted: the accountable owner and an active delegate; intake to the accountable owner (including a user-opened `--as-user` dispatch to the PDO); review or consultation assignments; Main/bootstrap scope and owner setup; backlog creation without execution.
  - Refusal text names `work_item.delivery_owner_ref` and a usable remedy (route to the owner, or ask the owner for a delegated grant).
- The false-positive side needs equal weight. Several of the admitted cases above go through the same verbs.

### B2, blocking: delegation rows omit the governing grantor assignment, and parent-closure semantics are undeclared

- `assignment_delivery_delegations` records the delegating session (`delegatedByRef`). It records no governing assignment of the grantor.
- `authorize_delegation` admits any caller for which `active_delegation_in_txn?` holds. It does not check which grant that is.
- `current_delegation?` checks the scope, owner and holder-association revisions. It does not check that the grantor's own grant is still active.
- The PO ruling requires that a delegation "identify the active governing assignment/work and its existing authorized grantor."
- The test at line 182 closes the child before the parent, so the other ordering is never exercised.
- As written, when a parent lane grant closes or is revoked while the child worker assignment is open, the child keeps full commissioning power. It can nest further grants until owner succession or revision drift. Nothing records or tests whether that is intended.
- Required:
  - Record the grantor's governing assignment (or the owner's authority when the grantor is the accountable owner).
  - Declare one semantics:
    - (a) Durable handoff: the child grant stands on its own once issued. State that it survives parent closure, and why.
    - (b) Dependent grant: commissioning power is evaluated against the grantor's still-active grant at use time.
  - Add a parent-closed-while-child-open test for the chosen semantics.
- My view: (b) matches "active governing assignment" best, and an evaluation-time check is not recursive revocation. The child's existing assignment and custody stay intact, and only new commissioning is refused. Either choice is acceptable with a stated reason and a test. Do not add cascading revocation of the open child assignment.

### B3, blocking (missing evidence, and routing that as read bypasses the successor): recipient after the former owner is unavailable

- The succession test at line 214 closes the worker and lane assignments through the original lane and the original owner `pdo-a`. `pdo-a` is still active in that test.
- The test at line 273 makes an owner unavailable, but it has no open assignments.
- No test shows who receives completion, failure or recovery for an open lane or worker whose opener was the former owner, once that owner has been transferred away or retired.
- In 504825b3, `review_notice_recipient_in_txn` (gateway.ex, about line 5415) resolves the recipient as follows:
  - the opener if that session is active,
  - otherwise the owner user's Main.
- It never consults `DeliveryResponsibilities.current_owner`. So:
  - After a transfer with the old owner still active, results route to the former owner, which is no longer accountable.
  - After the old owner retires, results route to Main, which the ruling says is not a production owner. They do not route to the current accountable successor.
  - The same opener-based resolution appears to govern ordinary assignment-change notices. I did not trace every notify path; the producer should confirm.
- The ruling asks for "a current accountable recovery recipient" and "actual recipient/recovery behavior, not only … a sent notification."
- Required:
  - Either route terminal outcomes on delivery-scoped items to the current accountable owner (with the former opener as a secondary audience, if kept),
  - or make succession carry open obligations to the successor as a declared handoff.
- Then show it end to end:
  - two items, open lane and worker,
  - transfer, then retirement of the former owner,
  - the worker completes and a sibling fails,
  - assert the actual wake or remedy row lands on the successor, and the successor can act on it.

### Resolved or acceptable at this revision

- Neutral notice: the final bytes in `session_po_associations.ex` `notice_prompt/2` are neutral. They name the addressed PO and association revision, point to the current association and applicable role guidance, preserve custody, route product questions to the PO, and say "grants no delivery authority and requires no acknowledgement". No PDO or engineering policy is embedded. This is acceptable.
- PDO default: `pdo.toml` defaults to codex `gpt-6-sol`, effort `low`. `gpt-6-sol` is present in the live model catalog. `preferred-models.md` line 30 explicitly lets the gpt-6-sol/low default carry incoming consultation. The evidence runner asserts this default, but it is labeled "offline source/default-resolution evidence only; no provider request ran". So fresh-default selection is shown at the source/snapshot level only. An actual spawned PDO taking that default has not been observed. Post-mvp unless the orchestrator treats observed selection as required.
- Human-communication election: PDO elects `["repository-retirement", "human-communication"]`, and the updated test asserts that no other engineering role elects it. The PDO is the engineering role that most often explains consequential delivery choices to a human. Routine reporting stays with the operating manual, and the test still guards against spreading the election. This is consistent. No finding.
- External legacy intake: the candidate `alignment-evidence/legacy-candidate/SKILL.md` (s_ea541c9d workdir, SHA 9d61c12b…) already qualifies the old absolute. It says user-opened intake to the accountable PDO is valid, that the absence of `openedBySession` does not mean delivery stops, and that the reader should inspect the actual holder, opener, notification and recovery routes. This matches the runtime: for a user-opened assignment, `review_notice_recipient_in_txn` routes to the owner's Main. It adds no confirmation gate. This is acceptable. It is outside 504825b3; custody sits with its author.

### Post-mvp

- P1: `authorize_delegation` lets any active delegate re-delegate without limit. This is acceptable as "nested" if B2 settles the chain semantics. No depth limit is requested.
- P2: spawn accepts `workItemId` only as a rule-fact input and does not record it. That is fine for admission. If later tracing needs the spawn-to-item link, record it then.

## Coordination

- Please send the producer's successor commit for a changed-hunk re-review scoped to B1 to B3 and any interactions they touch.
- Earlier evidence for the neutral notice, the PDO defaults and the elections carries forward unless those hunks change.
