# V4 Changed-Clause Register

V4 starts from reviewed V3 artifact `art_de142a5e` at SHA-256 `f5623e298abcc92d74a558378b5c6929dae946fef668a75847965b3c61c344c6`. This register lists each V3 clause changed by V4. Text not listed here remains inherited.

## `README.md`

1. **Bundle identity and read order:** Renames the bundle V4 and adds the V4 contract and changed-clause register to the read order.
2. **Authority boundary:** Adds the distinction between discovery and admission, the two permitted admission bases, controller-fixture validity, single-surface required proof, optional independently admitted surfaces, and terminal `capability_mismatch` handling.
3. **Frozen source custody:** Adds the reviewed V3 bundle hash.
4. **Version and scope rules:** Makes the 2/5/15/30-minute checkpoints, 60-minute churn dwell, and one bounded restart/recovery cycle explicit preservation requirements.
5. **V4 source ruling:** Records the sanctioned assignment/ruling inputs, unavailable and uninspected `art_88d4ac74`, and excluded invalid `art_ff2cad0e`.

## `01-gibson-cli-control-plane.md`

1. **Reviewed CLI provenance:** Requires CLI verification before discovery or per-surface admission instead of before one generic admission call.
2. **Canonical invocation preamble:** Removes the assumption that the run is already admitted.
3. **List result handling:** Classifies returned surfaces as discovered candidates and bars targeting before per-surface admission.
4. **Capture migration material:** Requires separate authority and exact surface/operation scope; bars derivation, broadening, and reuse.
5. **Surfaces driven by Gibson:** Replaces list-based admission with two permitted durable per-surface evidence bases. Binds evidence to the controller fixture, expiry, cleanup, and restart-validity boundary. Reclassifies named surfaces as candidates. Applies the same rule to controller-hosted clients.
6. **CLI gate:** Splits controller/list discovery readiness from per-surface admission. Selects one primary candidate. Makes additional candidates optional. Defines independent admission, exclusion, migration input location, terminal `capability_mismatch` handling, and post-boundary re-admission.
7. **Phase integration:** Scopes required Phase 1, Phase 2, Phase 3, and bounded Phase 4 proof to the primary admitted surface. Keeps additional fault experiments optional and separately authorized. Requires re-admission after a changed binding.
8. **Failure and retry rules:** Makes `pair.request` `capability_mismatch` terminal for the current fixture before mutation.
9. **Intentional divergence register:** Corrects `GIB-CLI-03` and adds `GIB-CLI-09` and `GIB-CLI-10` for independent admission and single-surface required proof.
10. **Final report:** Adds discovered, admitted, excluded, and admission-basis evidence.
11. **Revision history:** Adds the V4 repair record and marks the V3 list-as-admission history superseded.

## `02-fleet-soak-phases.md`

1. **Ansible scope:** Makes list output discovery-only and requires independent admission evidence.
2. **Core test principle:** Changes required-command “admission” to command-availability verification.
3. **Surface discovery, admission, and run scope:** Adds the primary-surface rule, controller-fixture validity, optional independently admitted surfaces, the single-surface proof boundary, and terminal `capability_mismatch` handling.
4. **Dynamic window admission:** Separates candidate discovery from admission and requires separate authority before creating optional windows.
5. **Required invariants:** Makes one bounded primary-surface restart required, marks other recovery scenarios optional, and requires re-admission after a changed binding.
6. **Pre-flight cleanup:** Limits pre-discovery Electron cleanup to separately authorized hosts and states that cleanup does not admit or authorize a target operation.
7. **Pre-flight 1.5:** Splits CLI discovery readiness from per-surface admission and defines fixture validity, migration input location, exclusion, cleanup, and fresh-fixture outcomes.
8. **Phase 1 scope and pass criteria:** Requires the primary admitted surface and makes additional surfaces conditional on independent admission.
9. **Phase 2 scope:** Runs required multi-pane churn inside the primary admitted surface and makes multi-surface proof optional.
10. **Phase 2 Sequence C:** Moves the ten required churn cycles to the primary admitted surface; makes additional multi-window cycles optional.
11. **Phase 2.6 scope:** Runs the required capture-backed oracle on the primary admitted surface; makes additional surfaces optional.
12. **Phase 3 scope:** Runs idle soak on the primary admitted surface and includes another named surface only after independent admission.
13. **Phase 4 restoration proof:** Records the exact admitted target list, revalidates admission across the boundary, and uses discovery plus read/capture/receipt evidence for post-boundary actionability.
14. **Phase 4 gateway/provider restart:** Makes these separate experiments optional and separately authorized; they do not replace the required primary-surface cycle.
15. **Phase 4 individual surface restart:** Requires one bounded restart/recovery cycle on the primary admitted surface; makes other cycles optional and re-admits changed bindings.
16. **Phase 4 network and ownership scenarios:** Makes each scenario optional, separately authorized, and limited to admitted surfaces.
17. **Phase 5 scope:** Moves the required longitudinal audit to the primary admitted surface; makes additional surfaces optional.
18. **Minimum release bar:** Replaces fixed multi-surface requirements with complete proof on one independently admitted primary surface, independent grades for optional surfaces, and explicit `capability_mismatch` handling.

## `03-fleet-soak-run-checklist.md`

1. **Required invariant gate:** Separates CLI discovery readiness from fixture-bound per-surface admission, requires the bounded primary recovery cycle, and bars another surface's success from substituting for admission evidence.
2. **Run metadata:** Binds the run to V4 and records the primary surface, admission basis, and evidence.
3. **Build identity:** Marks non-admitted named surface sections out of scope.
4. **Electron cleanup:** Limits pre-discovery cleanup to separately authorized included hosts and denies admission effect.
5. **CLI gate:** Adds the sole admission table. Records candidates, controller-fixture validity, migration input location, the primary selection, independent admission evidence, optional additional surfaces, single-surface multi-pane scope, and terminal `capability_mismatch` handling.
6. **Dynamic window log:** Separates discovered candidates, admitted targets, and excluded untargeted candidates.
7. **Phase 1:** Identifies the primary surface and marks non-admitted surface sections out of scope.
8. **Phase 2 Sequence C:** Moves the ten required cycles to the primary admitted surface and makes other surface/window cycles optional.
9. **Phase 2.6:** Starts the capture-backed oracle on the primary admitted surface and independently gates additional surfaces.
10. **Phase 3:** Makes the primary admitted surface the required multi-pane precondition, marks fixed named checkpoints conditional, and makes each named surface optional.
11. **Phase 4:** Adds one bounded primary-surface restart/recovery record with pre-state, post-state, capture/read proof, five-minute dwell, and post-boundary re-admission protection.
12. **Phase 4 optional scenarios:** Adds explicit authority/admission preconditions and a global re-admission rule to gateway, simulator, Aleph, Cyberbrain, Racter, eezo, Ansible, network, and ownership checks.
13. **Phase 5:** Binds the longitudinal audit to the primary admitted surface and rechecks admission after restart.
14. **Final judgment:** Adds primary-surface grading, out-of-scope choices for optional named surfaces, and an admission/scope judgment that checks discovery-only use, fixture validity, independent admission, migration-material scope, post-boundary re-admission, and terminal `capability_mismatch` handling.

## Added contract file

`00-v4-contract.md` adds the canonical Goal, Non-Goals, Terms, Assumptions, Invariants, Architecture, Acceptance, and Open Questions sections. It does not change a V3 procedure clause.

## Unchanged endurance structure

V4 retains Pre-flight 0–3; Phases 1, 2, 2.5, 2.6, 3, 4, and 5; repeated pushes with per-push capture; two-pane and three-pane topology; ten churn cycles; the 60-minute churn dwell with 10-minute checkpoints; 2-minute checks; 5-, 15-, and 30-minute idle checkpoints; longitudinal 10-minute checks; the required bounded restart/recovery cycle; invariant grading; failure capture; and final release judgment.
