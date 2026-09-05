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
