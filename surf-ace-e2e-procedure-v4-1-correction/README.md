# Surf Ace Gibson CLI E2E procedure bundle V4.1

This bundle is the complete operator procedure for a Gibson-coordinated Surf Ace fleet soak.
V4.1 repairs only the mutation-admission seam for the current Linux Racter path.
Use the bundle documents in this order:

1. Read `00-v4-contract.md` for the V4.1 scope and acceptance contract.
2. Read `01-gibson-cli-control-plane.md` and record the run-owned CLI inputs.
3. Execute `02-fleet-soak-phases.md` in order.
4. Complete `03-fleet-soak-run-checklist.md` while the run executes.
5. Use `04-v4-changed-clauses.md` to review each V4 clause changed by V4.1.

The bundle does not authorize product, package, install, endpoint, live, deployment, or state action by itself.
The operator must obtain separate authority for every approved soak action and every fault injection.
The operator must stop when that authority is absent.

## V4.1 mutation-admission boundary

`surf-ace list` discovers candidates. A successful list result does not admit a surface and does not authorize mutation.

The operator may admit a discovered surface only when durable evidence identifies that exact surface, controller fixture, fixture expiry and cleanup contract, restart-validity boundary, exact run-owned state root, covered target operations, issuer/authority, designated gated E2E operator, and immutable artifact identity, and proves one of these cases:

1. the surface is already lockless for the exact operations that this run will perform before the next admission boundary; or
2. the run has separately authorized explicit migration material and a supported CLI input location for that surface and operation.

For case 1, the evidence must be an immutable record from a separately authorized preflight executor that is allowed to attest endpoint-fixture compatibility for the exact run. It must state `admissionBasis: already-lockless` and `lockless: true`, name the exact covered operations, and record the verification method and result, issue time, expiry, reversible probe and rollback proof, cleanup contract, custody handoff, and every binding field above. The preflight executor must issue that row inside the exact run-owned state root that the gated operator will later use. A read-only row, a row from another state root, or a row issued for another operator does not satisfy this predicate. Discovery, topology, readback, diagnostics, remembered success, an operator assertion, and another surface's result do not satisfy this predicate.

Immediately before each target operation, the operator must verify that the admission row is unexpired and covers the current fixture, state root, operator, boundary, and operation. A failed check returns the surface to candidate state until a new admission row passes.

The operator must use topology changes inside one admitted surface for the required multi-pane proof. Additional surfaces are optional. Each additional surface needs its own admission evidence before any operation targets it.

If `pair.request` returns `capability_mismatch`, the operator stops before mutation, preserves the response, classifies endpoint/procedure readiness, cleans the run-owned fixture and state, and routes a fresh fixture. The operator does not retry, bypass the refusal, invent migration material, or require a source change. A fresh fixture begins a new admission boundary. The operator must run fresh discovery and create a new passing admission row for every surface before the fresh fixture targets it.

Only one gated E2E operator may consume one admission row. A new operator, a new state root, cleanup that releases the fixture, a changed controller/surface/pane binding, or a restart boundary that the row does not explicitly cover invalidates the row until a new one passes.

## Frozen source custody

The producer rehashed these inputs before preparing this bundle:

| Input | SHA-256 |
| --- | --- |
| Reviewed Gibson CLI procedure V2 | `5ac96a41fea1a70792b33b480678a47cd1fac7655cfc248f547d3a667f1adb1a` |
| Canonical fleet soak procedure | `d5e0b7b595ed2cac90c45c7d0646cf6466d259650f6af78a1a0fe913d78dc709` |
| Fleet soak run checklist | `b1c18b02a7235cb7311cba59958b4cda24b4b9ec5579487baacc0f1fcb3bd74a` |
| Reviewed V3 bundle | `f5623e298abcc92d74a558378b5c6929dae946fef668a75847965b3c61c344c6` |

The source paths are evidence provenance only. The operator does not need them to use this bundle.

## Version and scope rules

- The reviewed native `surf-ace` CLI is the only Surf Ace command path in this procedure.
- Discover every surface, pane, topology revision, content identity, and target identity from current CLI output.
- Do not type a remembered or example runtime identity into a command.
- Use one run-owned state root for the complete run.
- Preserve every phase, checkpoint, oracle, grading rule, and checklist duty in this bundle.
- Preserve the required 2-, 5-, 15-, and 30-minute checkpoints, the 60-minute churn dwell with 10-minute checkpoints, and one bounded restart/recovery cycle.
- Tightbeam 0.1.9 can exist beside a frozen 0.1.8 installation.
- Target Tightbeam 0.2.0 only when the governing work explicitly specifies 0.2.0.
- Leave work without a specified Tightbeam target untargeted.

## Bundle result

The completed checklist and evidence determine the run grade. This procedure never grants release authority.

## V4.1 source ruling

V4.1 consumes reviewed V4 artifact `art_a19b6b3a` at SHA-256 `fb832918337290546c321b7b166c6147703e2049c7ab8abf27f02010f990f0d3`, read-only admission artifact `art_545e1cf3` at SHA-256 `3e928b4224d19db47e0ebd6a09fe3b9e088c52829b9711a2ec104015a7c6e0cc`, and Red report `art_876f6fce`. The referenced report `art_88d4ac74` still had no surviving bytes and was not inspected or reconstructed. The invalid artifact `art_ff2cad0e` is not an input.
