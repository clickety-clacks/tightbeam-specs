# Surf Ace E2E Admission Procedure V4 Contract

## Goal

Provide a self-contained CLI-only E2E procedure that separates surface discovery from per-surface admission while preserving the V3 endurance and evidence contract.

## Non-Goals

- This bundle does not authorize a live E2E run.
- This bundle does not authorize a product, source, package, installation, endpoint, deployment, or Tightbeam change.
- This bundle does not require multi-surface execution.
- This bundle does not turn `pair.request` `capability_mismatch` into a source defect.
- This bundle does not supply or derive migration material.

## Terms

- **Discovered candidate:** A surface returned by the current `surf-ace list` result. Discovery proves identity and current topology only.
- **Admitted surface:** A discovered candidate whose exact `surfaceId` and controller fixture have admission evidence that remains valid for the next target operation.
- **Primary admitted surface:** The one admitted surface that carries the required multi-pane, repeated-push, capture, endurance, and bounded restart/recovery proof.
- **Additional admitted surface:** An optional surface that passed the same admission gate independently.
- **Already lockless:** The pre-existing compatibility state in which the exact surface/controller-fixture binding accepts every covered target operation without migration material. Discovery or successful operation on a different binding does not establish this state.
- **Already-lockless evidence:** An immutable record from an authority that is separately authorized to attest endpoint-fixture compatibility. The record must contain `admissionBasis: already-lockless`, an explicit `lockless: true` assertion, the exact `surfaceId`, controller-fixture identity, covered target-operation set, verification method and result, issuer/authority reference, issue time, expiry, cleanup contract, restart/recovery validity, and artifact identity or SHA-256. A `list`, topology, readback, diagnostic, remembered success, operator assertion, or another surface's result is not already-lockless evidence.
- **Admission evidence:** A durable reference that names the exact surface, controller fixture identity, fixture expiry and cleanup contract, validity across restart/recovery boundaries, covered target-operation set, issuer/authority, immutable identity, and one permitted admission basis.
- **Explicit migration material:** The exact object supplied under separate authority for one named surface and operation, together with its supported CLI input location.
- **Target operation:** A Surf Ace CLI operation that names a surface or pane. Separately authorized host cleanup before discovery is not a target operation and does not admit a surface.
- **Fresh fixture:** A newly verified endpoint fixture with its own identity, expiry, and cleanup contract.

## Assumptions

- Reviewed V3 artifact `art_de142a5e` has SHA-256 `f5623e298abcc92d74a558378b5c6929dae946fef668a75847965b3c61c344c6`.
- The V3 CLI invocation shapes remain authoritative outside the admission changes listed in `04-v4-changed-clauses.md`.
- Assignment `asg_d13a60f6-dfd4-45a2-967c-d40c24ba85a9` and ruling `att_c2148d28-cfcd-4b28-9072-5de5cdd167d6` authorize this repair.
- Artifact `art_88d4ac74` had no available bytes during preparation. V4 does not claim to inspect or reconstruct it.

## Invariants

1. `surf-ace list` changes only the discovered-candidate record. It does not change the admitted-target record.
2. Immediately before each target operation, the operator verifies that every required admission-evidence field is present, unexpired, fixture-matching, authority-valid, boundary-valid, and operation-covering. A failed check returns the surface to candidate state until a new admission row passes.
3. The checklist admission log is the single seam that adds a surface to the admitted-target record.
4. Required multi-pane work stays inside the primary admitted surface.
5. Each additional targeted surface carries independent admission evidence.
6. The operator applies explicit migration material only to its authorized surface and operation.
7. A `pair.request` `capability_mismatch` ends the current fixture before mutation. A fresh fixture starts a new admission boundary: the operator performs fresh discovery and records a new passing admission row for each target surface before any target operation.
8. After a restart or recovery boundary, the operator re-runs discovery. If the surface/controller-fixture binding changed or the admission evidence does not explicitly cover the boundary, the operator re-admits the candidate before the next target operation.
9. The operator preserves the V3 phase order, CLI-only path, repeated pushes, per-push capture proof, multi-pane topology, 2/5/15/30-minute checkpoints, 60-minute churn dwell, and one bounded restart/recovery cycle.

## Architecture

- `README.md` defines bundle custody, use order, and the V4 boundary.
- `01-gibson-cli-control-plane.md` defines CLI commands, discovery, admission, and failure handling.
- `02-fleet-soak-phases.md` defines the preserved phase sequence and execution scope.
- `03-fleet-soak-run-checklist.md` is the sole run record and admission-log mutation seam.
- `04-v4-changed-clauses.md` traces each V3 clause changed by V4.
- `MANIFEST.sha256` binds the bundle contents.

This design adds no runtime mechanism. Deleting the admission gate would repeat the V3 failure, and accepting discovery as admission would authorize an unsafe mutation. A procedure gate is therefore the smallest closure.

## Acceptance

1. Given a successful `surf-ace list` result and no per-surface admission evidence, when the operator evaluates a candidate, then the checklist records it as excluded and no command targets it.
2. Given an immutable, separately authorized record with `admissionBasis: already-lockless`, `lockless: true`, exact surface/controller-fixture binding, covered operation set, verification method and result, issuer, issue time, expiry, cleanup contract, restart validity, and artifact identity or SHA-256, when the admission verifier confirms every field is present, current, authority-valid, fixture-matching, and operation-covering, then the checklist can admit that surface as the primary surface. Generic discovery, topology, readback, diagnostics, memory, operator assertion, and another surface's result fail this predicate.
3. Given separately authorized explicit migration material for one discovered surface, when the operator records its authority, exact scope, and supported CLI input location, then the checklist can admit that surface without applying the material to another surface or operation.
4. Given one admitted surface, when the operator runs the required topology phase, then the operator creates the required multi-pane topology inside that surface without selecting a second surface.
5. Given a second discovered surface without independent admission evidence, when the primary surface has already passed, then the second surface remains excluded and untargeted.
6. Given a `pair.request` response with `capability_mismatch`, when the operator reaches the first mutation boundary, then the run records no mutation, performs terminal fixture/state cleanup, classifies endpoint/procedure readiness, and routes a fresh fixture without retry. Before resuming, the operator runs fresh `surf-ace list` discovery and creates a new passing admission row for every surface that the fresh fixture will target.
7. Given a restart or recovery boundary, when fresh discovery returns a changed surface/controller-fixture binding or the prior admission evidence does not cover the boundary, then the candidate is re-admitted before read, capture, push, or topology work targets it.
8. Given the sealed V4 bundle, when a reviewer compares its phase and checklist headings with V3, then each V3 endurance phase remains present and the required 2/5/15/30-minute, 60-minute, and restart/recovery checkpoints remain stated.
9. Given preparation evidence, when a reviewer inspects commands and artifacts, then the evidence contains document, archive, hash, and repository operations only and contains no live Surf Ace action.
10. Given an admitted surface whose evidence expired, does not cover the current boundary, or does not cover the next target operation, when the operator performs the pre-operation admission check, then the operator records the surface as a candidate and creates a new passing admission row before any target operation names it.

## Open Questions

None.
