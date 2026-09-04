# Surf Ace E2E Admission Procedure V4.1 Contract

## Goal

Provide a self-contained CLI-only E2E procedure that separates surface discovery from per-surface mutation admission, requires operation-covering proof inside the exact run-owned state root before the first mutation, and preserves the V4 endurance and evidence contract.

## Non-Goals

- This bundle does not authorize a live E2E run.
- This bundle does not authorize a product, source, package, installation, endpoint, deployment, or Tightbeam change.
- This bundle does not require multi-surface execution.
- This bundle does not turn `pair.request` `capability_mismatch` into a source defect.
- This bundle does not supply or derive migration material.

## Terms

- **Discovered candidate:** A surface returned by the current `surf-ace list` result. Discovery proves identity and current topology only.
- **Admitted surface:** A discovered candidate whose exact `surfaceId`, controller fixture, run-owned state root, and gated operator have admission evidence that remains valid for the next target operation.
- **Primary admitted surface:** The one admitted surface that carries the required multi-pane, repeated-push, capture, endurance, and bounded restart/recovery proof.
- **Additional admitted surface:** An optional surface that passed the same admission gate independently.
- **Already lockless:** The pre-existing compatibility state in which the exact surface/controller-fixture binding accepts every covered target operation without migration material. Discovery or successful operation on a different binding does not establish this state.
- **Preflight executor:** The separately authorized session that runs the bounded preflight probe, proves operation coverage, restores the preflight baseline, and issues the immutable admission row for the exact run.
- **Gated E2E operator:** The one designated session that may consume one admission row for one run after the preflight executor hands off custody.
- **Already-lockless evidence:** An immutable record from a preflight executor that is separately authorized to attest endpoint-fixture compatibility for the exact run. The record must contain `admissionBasis: already-lockless`, an explicit `lockless: true` assertion, the exact `surfaceId`, controller-fixture identity, covered target-operation set, verification method and result, issuer/authority reference, exact gated-operator identity, exact run-owned state-root identity, issue time, expiry, cleanup contract, restart/recovery validity, reversible probe and rollback proof, custody handoff, and artifact identity or SHA-256. A `list`, topology, readback, diagnostic, remembered success, operator assertion, another surface's result, a read-only row, or a row from another state root is not already-lockless evidence.
- **Admission evidence:** A durable reference that names the exact surface, controller fixture identity, run-owned state-root identity, gated-operator identity, fixture expiry and cleanup contract, validity across restart/recovery boundaries, covered target-operation set, issuer/authority, immutable identity, and one permitted admission basis.
- **Explicit migration material:** The exact object supplied under separate authority for one named surface and operation, together with its supported CLI input location.
- **Target operation:** A Surf Ace CLI operation that names a surface or pane. Separately authorized host cleanup before discovery is not a target operation and does not admit a surface.
- **Fresh fixture:** A newly verified endpoint fixture with its own identity, expiry, and cleanup contract.
- **Reversible probe:** The bounded preflight sequence that covers the exact planned mutation and proof operations, captures receipts and visual/readback proof, and restores the preflight baseline before handoff.
- **Restored preflight baseline:** The intended one-pane topology and matching semantic render/content metadata after the temporary pane closes. The operator preserves both PNG byte hashes as evidence but does not require them to match.
- **Preflight-ready fact:** The run-specific Tightbeam condition that transfers custody after the preflight executor records and verifies the immutable admission row. The fact kind and scope are inputs to the run.

## Assumptions

- Reviewed V4 artifact `art_a19b6b3a` has SHA-256 `fb832918337290546c321b7b166c6147703e2049c7ab8abf27f02010f990f0d3`.
- Read-only admission artifact `art_545e1cf3` has SHA-256 `3e928b4224d19db47e0ebd6a09fe3b9e088c52829b9711a2ec104015a7c6e0cc`.
- Red report `art_876f6fce` correctly identified that the read-only row did not cover mutation and expired across the new state root.
- The V4 CLI invocation shapes remain authoritative outside the admission changes listed in `04-v4-changed-clauses.md`.
- Artifact `art_88d4ac74` had no available bytes during preparation. V4 does not claim to inspect or reconstruct it.

## Invariants

1. `surf-ace list` changes only the discovered-candidate record. It does not change the admitted-target record.
2. The preflight executor issues one already-lockless row only after the reversible probe proves the exact covered operations inside the exact run-owned state root and restores the preflight baseline before handoff.
3. Immediately before each target operation, the gated operator verifies that every required admission-evidence field is present, unexpired, fixture-matching, state-root-matching, operator-matching, authority-valid, boundary-valid, and operation-covering. A failed check returns the surface to candidate state until a new admission row passes.
4. The checklist admission log is the single seam that adds a surface to the admitted-target record.
5. One admission row binds one gated operator and one run-owned state root. An operator change or state-root change invalidates the row until a new row passes.
6. Required multi-pane work stays inside the primary admitted surface.
7. Each additional targeted surface carries independent admission evidence.
8. The operator applies explicit migration material only to its authorized surface and operation.
9. A `pair.request` `capability_mismatch` ends the current fixture before mutation. A fresh fixture starts a new admission boundary: the operator performs fresh discovery and records a new passing admission row for each target surface before any target operation.
10. After a restart or recovery boundary, the operator re-runs discovery. If the surface/controller-fixture binding changed or the admission evidence does not explicitly cover the boundary, the operator re-admits the candidate before the next target operation.
11. The operator preserves the V4 phase order, CLI-only path, repeated pushes, per-push capture proof, multi-pane topology, 2/5/15/30-minute checkpoints, 60-minute churn dwell, and one bounded restart/recovery cycle.
12. A successful local `read` has CLI exit code 0, top-level `ok: true`, the expected scope, `cacheStatus: current`, and no consumable loss. Local `read` is an unread-delta projection, not a current-content snapshot. Immediately after a push it must include that push's content record and matching acknowledgement. For a baseline, restoration, or later check with no new push, `acknowledgement: null` and an empty record list is valid; current rendered-content truth comes from `capture-pane`. The operator never requires `result.ok` from `read`.
13. The preflight executor files the preflight-ready fact only after a fresh `list` result matches the admission row. The gated operator consumes the row only after that fact arrives and its own fresh `list` result still matches every binding.
14. Preflight restoration requires the intended one-pane topology, a current lossless local `read`, and exact agreement between baseline and restored capture pane, content id, content type, revision, visible text, selection, and viewport. The read can be current-empty when that content predates controller admission. PNG files and SHA-256 values remain evidence, but PNG byte equality is not a restoration predicate.

## Architecture

- `README.md` defines bundle custody, use order, and the V4.1 mutation-admission boundary.
- `01-gibson-cli-control-plane.md` defines CLI commands, discovery, mutation admission, and failure handling.
- `02-fleet-soak-phases.md` defines the preserved phase sequence and execution scope.
- `03-fleet-soak-run-checklist.md` is the sole run record and admission-log mutation seam.
- `04-v4-changed-clauses.md` traces each V4 clause changed by V4.1.
- `05-read-response-validator.sh` validates strict post-push content deltas and current lossless baseline/restoration deltas.
- `06-restoration-oracle.sh` validates semantic restoration while preserving PNG hashes as evidence.
- `MANIFEST.sha256` binds the bundle contents.

This design adds no new product mechanism. Deleting the mutation-capable preflight row would repeat the V4 failure, and accepting discovery or a read-only row as mutation authority would authorize an unsafe mutation. A separate preflight issuer plus one admission seam is therefore the smallest closure.

## Acceptance

1. Given a successful `surf-ace list` result and no per-surface admission evidence, when the operator evaluates a candidate, then the checklist records it as excluded and no command targets it.
2. Given a read-only row that covers only `read` and `capture-pane`, when the next target operation is `push` or topology mutation, then the verifier rejects that row and the checklist records the candidate as excluded until a new passing row exists.
3. Given an immutable, separately authorized record with `admissionBasis: already-lockless`, `lockless: true`, exact surface/controller-fixture binding, exact run-owned state root, exact gated operator, covered operation set, verification method and result, reversible probe and rollback proof, issuer, issue time, expiry, cleanup contract, restart validity, and artifact identity or SHA-256, when the admission verifier confirms every field is present, current, authority-valid, fixture-matching, state-root-matching, operator-matching, and operation-covering, then the checklist can admit that surface as the primary surface.
4. Given separately authorized explicit migration material for one discovered surface, when the operator records its authority, exact scope, and supported CLI input location, then the checklist can admit that surface without applying the material to another surface or operation.
5. Given one admitted surface, when the operator runs the required topology phase, then the operator creates the required multi-pane topology inside that surface without selecting a second surface.
6. Given a second discovered surface without independent admission evidence, when the primary surface has already passed, then the second surface remains excluded and untargeted.
7. Given a `pair.request` response with `capability_mismatch`, when the operator reaches the first mutation boundary, then the run records no mutation, performs terminal fixture/state cleanup, classifies endpoint/procedure readiness, and routes a fresh fixture without retry. Before resuming, the operator runs fresh `surf-ace list` discovery and creates a new passing admission row for every surface that the fresh fixture will target.
8. Given a restart, recovery, ownership handoff, or state-root change, when fresh discovery returns a changed surface/controller-fixture binding or the prior admission evidence does not explicitly cover that boundary, then the candidate is re-admitted before read, capture, push, or topology work targets it.
9. Given a newly admitted controller and pre-existing pane content, when local `read` returns top-level `ok: true`, the exact scope, `cacheStatus: current`, `consumableLoss: null`, `acknowledgement: null`, and no records while `capture-pane` proves the expected rendered content, then the baseline or restoration read passes. The same empty response does not satisfy a post-push content check.
10. Given the sealed V4.1 bundle, when a reviewer compares its phase and checklist headings with V4, then each V4 endurance phase remains present and the required 2/5/15/30-minute, 60-minute, and restart/recovery checkpoints remain stated.
11. Given preparation evidence, when a reviewer inspects commands and artifacts, then the evidence contains document, archive, hash, and repository operations only and contains no live Surf Ace action.
12. Given an admitted surface whose evidence expired, does not cover the current boundary, does not cover the next target operation, names another operator, or names another state root, when the operator performs the pre-operation admission check, then the operator records the surface as a candidate and creates a new passing admission row before any target operation names it.
13. Given the exact successful tick-0 local `read` fixture, when the harness validates it, then the response passes without a `result.ok` field and the harness proceeds to capture.
14. Given a preflight row that names another controller, state root, operator, surface, pane, boundary, or operation set, or given no matching preflight-ready fact, when the operator evaluates the handoff, then the operator rejects the row and performs no target operation.
15. Given the exact `art_663ac4d3` restoration fixture whose baseline and restored PNG hashes differ while semantic render/content metadata matches, when the harness validates restoration, then the semantic oracle passes and both hashes remain recorded.
16. Given a restored capture with a wrong content id, wrong visible text, or stale revision, when the harness validates restoration, then the semantic oracle rejects it.

## Open Questions

None.
