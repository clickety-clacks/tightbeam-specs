# Surf Ace Gibson CLI E2E procedure bundle V4.1

This bundle is the complete operator procedure for a Gibson-coordinated Surf Ace fleet soak.
V4.1 introduced the mutation-admission seam for the current Linux Racter path.
This revision also repairs the operator faults that stopped the 2026-09-03 runs before the soak.
Use the bundle documents in this order:

1. Read `00-v4-contract.md` for the V4.1 scope and acceptance contract.
2. Read `01-gibson-cli-control-plane.md` and record the run-owned CLI inputs.
3. Execute `02-fleet-soak-phases.md` in order.
4. Complete `03-fleet-soak-run-checklist.md` while the run executes.
5. Use `04-v4-changed-clauses.md` to review each V4 clause changed by V4.1.
6. Source `05-read-response-validator.sh` from the run-specific harness.
7. Source `06-restoration-oracle.sh` from the run-specific preflight harness.

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

The gated operator must subscribe to one run-specific preflight-ready fact before the preflight starts. The preflight executor files that fact only after it records the immutable admission row and verifies the row against a fresh `list` result from the exact state root. After the fact arrives, the operator must run `list` again and compare the current controller, state root, operator, surface, pane, boundary, and operation set with the row. A completion, direct message, or admission artifact without the matching fact does not transfer custody.

For local `read`, a successful response has top-level `ok: true`. Its `result` contains the acknowledgement, `cacheStatus`, records, and scope. It does not contain `result.ok`. Local `read` returns the controller's unread consumable delta, not a snapshot of current rendered content. After a push, use `surf_ace_read_response_ok` to require that push's content record. For a baseline, restoration, or later check with no new push, use `surf_ace_current_read_response_ok`; `cacheStatus: current`, `consumableLoss: null`, `acknowledgement: null`, and an empty record list is valid because `capture-pane` supplies current rendered-content truth. The harness must use `05-read-response-validator.sh` and must not apply the network-response predicate to `read`.

After a reversible split/close probe, preserve the baseline and restored PNG files and their SHA-256 values as evidence. Do not require the two PNG byte hashes to match. The restoration oracle is the intended one-pane topology plus the semantic render/content metadata: exact pane, content id, content type, revision, visible text, selection, and viewport. The restored local `read` must pass `surf_ace_current_read_response_ok`, including `cacheStatus: current` and no consumable loss; it can be current-empty when the restored content predates controller admission. Use `06-restoration-oracle.sh` for the semantic comparison. A wrong or stale capture content value is a restoration failure.

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

This corrective revision also consumes checkpoint `art_ada61ba4` at SHA-256 `c6624e32c9fdb45589f07f56cb70b95b195c9a400c209a9fc635b0bb8f2d526b`. The checkpoint preserved the exact successful tick-0 `read` response and proved that the run-specific harness rejected it only because `result.ok` was absent. The revision also consumes preflight row `art_37ae29b4` at SHA-256 `33fab770a28fcfd72848261c2ba4db31954e0542fbe9413a6228555fd3ae0980`. That row bound another state root, controller, surface, and pane, and no required preflight-ready fact transferred custody to the stopped operator.

The visual restoration correction consumes refusal `art_663ac4d3` at SHA-256 `0f5ee1161a0c481069acdfed537d9a68b0469566d97ace97c46fe8d73b046ff1` and its evidence manifest at SHA-256 `531ff5147540bdaf4f1dd3da383c34f0758028fd5fe92ab56b66428b6f7507ac`. On `sf_49049d957bd4`, baseline PNG SHA-256 `7509fa0979e04e7f4542644f93e38eeaaee8499a035eb10babe201bcc9e9816e` and restored PNG SHA-256 `ecb9a7edd36ca9b562f6d66ee141033f06466ffb53378c3ec79e03180d7abccb` differed while the semantic render/content metadata matched. The first two surfaces restored. The last three were not probed after the stop.

The current-empty read correction consumes refusal `art_63b949fd` at SHA-256 `e1304d59a8f479e0be2698283a7101a1b4a78357602849838ae5ab7043e3500f`. Its exact response had top-level `ok: true`, the expected scope, `cacheStatus: current`, `consumableLoss: null`, `acknowledgement: null`, and no unread records while `capture-pane` returned the current rendered content. The product initializes a newly admitted controller's existing-scope cursor at the scope tail, so pre-existing content is not replayed as unread.
