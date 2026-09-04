# V4.1 Changed-Clause Register

V4.1 starts from reviewed V4 artifact `art_a19b6b3a` at SHA-256 `fb832918337290546c321b7b166c6147703e2049c7ab8abf27f02010f990f0d3`. This register lists each V4 clause changed by V4.1. Text not listed here remains inherited.

## Repair target

Red report `art_876f6fce` proved that V4 over-admitted a read-only same-epoch row. The row in `art_545e1cf3` covered only `read` and `capture-pane`, expired on a new state root, and could not authorize the first `push` in the fresh Linux Racter run. V4.1 repairs only that mutation-admission seam.

## `README.md`

1. **Bundle identity and read order:** Renames the bundle V4.1 and points the changed-clause register at V4.1-over-V4 changes.
2. **Mutation-admission boundary:** Replaces generic already-lockless admission with an exact run-bound row that names the state root, gated operator, covered operations, rollback proof, and custody handoff.
3. **Source ruling:** Binds V4.1 to reviewed V4, the read-only admission row, and the Red report that justified the repair.

## `00-v4-contract.md`

1. **Goal:** Requires operation-covering proof inside the exact run-owned state root before the first mutation.
2. **Terms:** Adds `Preflight executor`, `Gated E2E operator`, and `Reversible probe`. Extends already-lockless evidence and admission evidence with exact state-root binding, exact operator binding, rollback proof, and custody handoff.
3. **Assumptions:** Replaces V3-source assumptions with reviewed V4, the read-only row, and the Red finding.
4. **Invariants:** Adds the separate preflight issuer, exact operator/state-root binding, and the immediately-prior mutation check over those bindings.
5. **Acceptance:** Adds explicit rejection of read-only rows for mutation and explicit rejection of rows bound to another operator or state root.

## `01-gibson-cli-control-plane.md`

1. **Recorded identities:** Adds the separately authorized preflight executor and the designated gated E2E operator to the first recorded values.
2. **Surfaces driven by Gibson:** Extends the already-lockless predicate from fixture-bound to fixture-plus-state-root-plus-operator-bound, and requires rollback proof and custody handoff.
3. **CLI gate:** Renames the gate to mutation admission, requires the exact run-owned state root that the gated operator will use, and replaces passive validation of a pre-existing row with either:
   - a separately authorized reversible preflight probe that covers the planned first-boundary operations and restores baseline; or
   - separately authorized explicit migration material.
4. **Boundary reuse rules:** Rejects reuse across operator changes and state-root changes, in addition to the existing fresh-fixture and changed-binding boundaries.
5. **Immediately-prior check:** Extends the pre-operation check to exact state-root and exact operator binding.

## `02-fleet-soak-phases.md`

1. **Surface discovery and run scope:** Replaces the stale V4 predicate with the exact V4.1 preflight-executor, state-root, gated-operator, rollback, handoff, and read-only-row rejection requirements at the first active operator checkpoint.
2. **Immediately-prior check:** Extends the active run-scope recheck from fixture plus boundary coverage to fixture plus exact state root plus exact gated operator plus non-read-only status plus operation coverage.
3. **Pre-flight 1.5 recorded inputs:** Adds the execution host, preflight executor, gated operator, and exact run-owned state root.
4. **Pre-flight 1.5 evidence path:** Requires the bounded reversible probe to cover the exact push, topology, capture, and read operations planned before the next boundary, restore the preflight baseline, and issue the immutable row.
5. **Pre-flight 1.5 admission record:** Requires the recorded row to include the state-root binding, gated operator, rollback proof, and handoff evidence.

## `03-fleet-soak-run-checklist.md`

1. **Run metadata:** Adds explicit fields for the preflight executor and the gated E2E operator.
2. **CLI gate section:** Renames the gate to mutation admission and extends each readiness check to exact state-root binding, exact operator binding, rollback proof, and handoff evidence.
3. **Admission verifier:** Adds explicit rejection of read-only rows and rows bound to another state root or operator.
4. **Admission log table:** Adds columns for run-owned state root plus gated operator, and for rollback proof plus handoff.
5. **Phase 4 reuse rule:** Replaces restart, interruption, and handoff reuse based only on unchanged surface/controller binding with the complete V4.1 reuse rule: unchanged fixture, unchanged state root, unchanged gated operator, non-read-only row, and explicit boundary coverage.
6. **Final judgment:** Requires every target operation to prove the exact state root and exact gated operator, and requires each already-lockless row to come from the separate preflight executor after the baseline-restoring reversible probe.

## Unchanged endurance structure

V4.1 retains V4 Pre-flight 0–3; Phases 1, 2, 2.5, 2.6, 3, 4, and 5; repeated pushes with per-push capture; two-pane and three-pane topology; ten churn cycles; the 60-minute churn dwell with 10-minute checkpoints; 2-minute checks; 5-, 15-, and 30-minute idle checkpoints; longitudinal 10-minute checks; the required bounded restart/recovery cycle; Aleph visual proof; invariant grading; failure capture; and final release judgment.

## 2026-09-03 operator-harness correction

Checkpoint `art_ada61ba4` proved that the run-specific harness rejected a successful tick-0 local `read` before capture. The CLI exited 0 and returned top-level `ok: true`, `result.cacheStatus: current`, the matching scope and acknowledgement, and the expected content record. Local `read` does not return `result.ok`. This revision adds the real response fixture and a validator that uses the correct local-read contract.

Preflight row `art_37ae29b4` bound another state root, controller, surface, and pane. The stopped operator also did not receive the required preflight-ready fact. This revision makes the handoff observable and adds fresh controller-binding checks on both sides of the fact.

These are the only new behavior changes:

1. `README.md`, `00-v4-contract.md`, `01-gibson-cli-control-plane.md`, and `02-fleet-soak-phases.md` separate the local `read` response contract from the network-response contract.
2. `05-read-response-validator.sh` enforces the local `read` contract against the exact tick-0 fixture.
3. `README.md`, `00-v4-contract.md`, `01-gibson-cli-control-plane.md`, `02-fleet-soak-phases.md`, and `03-fleet-soak-run-checklist.md` require one preflight-ready fact and fresh controller-binding checks before the operator admits a surface.


## 2026-09-04 visual restoration-oracle correction

Refusal `art_663ac4d3` at SHA-256 `0f5ee1161a0c481069acdfed537d9a68b0469566d97ace97c46fe8d73b046ff1` stopped preflight when restored PNG SHA-256 `ecb9a7edd36ca9b562f6d66ee141033f06466ffb53378c3ec79e03180d7abccb` differed from baseline SHA-256 `7509fa0979e04e7f4542644f93e38eeaaee8499a035eb10babe201bcc9e9816e`. The intended one-pane topology and the pane, content, revision, visible-text, selection, and viewport metadata matched. Evidence manifest SHA-256 `531ff5147540bdaf4f1dd3da383c34f0758028fd5fe92ab56b66428b6f7507ac` preserves the stopped run.

This correction changes only the preflight restoration oracle. The harness preserves baseline and restored PNG files and hashes but grades restoration against one-pane topology, current read content, and matching semantic capture metadata. `06-restoration-oracle.sh` covers the exact passing drift fixture plus wrong-content, wrong-visible-text, and stale-revision failures.

## 2026-09-04 current-empty local-read correction

Refusal `art_63b949fd` at SHA-256 `e1304d59a8f479e0be2698283a7101a1b4a78357602849838ae5ab7043e3500f` proved that a fresh controller can capture pre-existing rendered content while its first local `read` is current and empty. The exact Red state had `clientCursor` and `projectedCursor` at 21 with retained content records ending at sequence 20. Surf Ace intentionally initializes a newly admitted controller's existing-scope cursor at the scope tail, so local `read` does not replay that content as unread.

This correction changes only the read validator and the preflight clauses that mistook unread records for current rendered-content state. `surf_ace_read_response_ok` remains strict after each push. New `surf_ace_current_read_capture_ok` jointly checks the local read and same-controller capture for baseline and restoration checks. It accepts the exact current-empty, no-loss shape only when the capture supplies the expected current pane/content; every nonempty content delta must match the capture's content id and revision. The self-test consumes the exact Red response in `fixtures/preflight-read-current-empty.json` and the image-free semantic projection of its exact paired capture in `fixtures/preflight-capture-current-semantic.json`; it rejects failed exits, stale cache, loss, wrong content, wrong revision, and controller mismatch.
