# Surf Ace Fleet Soak Procedure — Gibson CLI Control Plane

## Status and relationship to this bundle

This document defines the command path for `02-fleet-soak-phases.md` and
`03-fleet-soak-run-checklist.md`. Use it with the complete bundle named in `README.md`.

The frozen phase source had SHA-256
`d5e0b7b595ed2cac90c45c7d0646cf6466d259650f6af78a1a0fe913d78dc709`.
This bundle includes its phases, checkpoints, evidence rules, grading rules, and release gate.

The reviewed native `surf-ace` CLI is the only Surf Ace command path in this bundle.

## Purpose

Use this procedure when Gibson coordinates a Surf Ace fleet soak through the native `surf-ace` CLI and the approved Surf Ace controller endpoint.

This procedure does not authorize deployment, installation, build promotion, provider replacement, or fleet mutation outside the approved soak actions.

## Reviewed CLI provenance

Use reviewed CLI bytes. Record and verify their SHA-256 before discovery or per-surface admission.

The 2026-08-22 Green run proved this reviewed CLI path:

- source commit: `09e899c8137e27fde8b93a01b50c4974be18e62f`;
- source tree: `0ff00d8a0a2ee902eca97716821871127260b30e`;
- independent source review: `att_a1def3d6`;
- arm64 CLI artifact: `art_d739054f`;
- CLI SHA-256: `c3568c472b283a9b7cafc1e130879bc2ee4d143cb7653d1f342acf7f798fac0f`;
- Green install and rendered capture: `art_868dedf4`;
- Green preflight: `art_ca7a2e71`;
- Green six-iteration list soak: `art_63e3d91f`;
- reviewed first-Green digest report: `art_2a1fe78c`.

The Green runner called the CLI with a run-owned state root, the WebSocket controller endpoint, and a product label. It ran `list` with `{}`. It selected the returned surface and numeric pane instead of using a fixed pane. It then ran `capture-pane` for that discovered pair. The capture returned PNG bytes and produced SHA-256 `8c1143dcc1f3dcc147bca6dea4fcb5f2f4044b17d3346f67d0cb7a794bd97511`.

Do not infer that the short Green run proved repeated pushes, repeated captures, endurance, content persistence, or recovery. This procedure exists to test those claims.

## Gibson control plane

Gibson coordinates the run, retains evidence, and grades results. Run every Surf Ace discovery, topology, content, read, and capture operation through the reviewed `surf-ace` CLI.

The CLI connects to the approved Surf Ace controller endpoint. Do not call that endpoint with a raw WebSocket client, HTTP client, provider tool, app script, or manually edited state file.

The host that owns the CLI process also owns one run-specific controller state root. Use the same state root for the complete run. Do not share it with another run. Do not remove or edit its files while a command is active.

Record these values before the first command:

- CLI path and SHA-256;
- CLI source commit and review reference;
- CLI execution host;
- separately authorized preflight executor identity and assignment;
- designated gated E2E operator identity and assignment;
- preflight-ready fact kind and work-item scope;
- controller endpoint;
- controller fixture identity, expiry, and cleanup contract;
- run-specific state-root path;
- product label;
- run identifier;
- artifact root;
- operator identity and time window.

## Canonical invocation shapes

The following shapes come from the reviewed V3 source and the 2026-08-22 Green runner. Set every uppercase shell variable from the current run. Build dynamic JSON with `jq`; do not replace discovered numeric values with remembered examples.

### Network command prefix

Use this prefix for `list`, `push`, `capture-pane`, `topology-intent`, `topology-realize`, `clear`, `annotations-remove`, `surface-intent`, `target-register`, and `target-apply`:

```sh
"$SURF_ACE_BIN" \
  --state-root "$SURF_ACE_STATE_ROOT" \
  --endpoint "$SURF_ACE_CONTROLLER_ENDPOINT" \
  --product-label "$SURF_ACE_PRODUCT_LABEL" \
  COMMAND --input-json "$COMMAND_INPUT_JSON"
```

### List

```sh
"$SURF_ACE_BIN" \
  --state-root "$SURF_ACE_STATE_ROOT" \
  --endpoint "$SURF_ACE_CONTROLLER_ENDPOINT" \
  --product-label "$SURF_ACE_PRODUCT_LABEL" \
  list --input-json '{}'
```

Store the complete JSON result. Require `ok: true`. Select `surfaceId`, numeric `paneId`, and the latest topology revision only from this result. Treat each returned surface as discovered, not admitted. Do not target it until the per-surface admission gate passes.

### Push

Build the input from the surface, pane, and content identities selected for the current step:

```sh
PUSH_INPUT_JSON="$(jq -nc \
  --arg surfaceId "$SURFACE_ID" \
  --argjson paneId "$PANE_ID" \
  --arg contentId "$CONTENT_ID" \
  --arg marker "$VISIBLE_MARKER" \
  --arg friendlyChatName "$SOAK_RUN_LABEL" \
  '{surfaceId:$surfaceId,paneId:$paneId,contentId:$contentId,contentType:"markdown",content:{markdown:("# "+$marker)},friendlyChatName:$friendlyChatName}')"

"$SURF_ACE_BIN" \
  --state-root "$SURF_ACE_STATE_ROOT" \
  --endpoint "$SURF_ACE_CONTROLLER_ENDPOINT" \
  --product-label "$SURF_ACE_PRODUCT_LABEL" \
  push --input-json "$PUSH_INPUT_JSON"
```

Do not concatenate unescaped content. Use the discriminated content value required by the reviewed CLI.

Require the exact correlated `operationReceipt`. Treat `outcome_unknown` as unknown, not failed. Do not retry an unknown mutation. Reconcile it through later list, read, capture, and receipt evidence.

### Capture pane

```sh
CAPTURE_INPUT_JSON="$(jq -nc \
  --arg surfaceId "$SURFACE_ID" \
  --argjson paneId "$PANE_ID" \
  '{surfaceId:$surfaceId,paneId:$paneId,includeImage:true,includeVisibleText:true}')"

"$SURF_ACE_BIN" \
  --state-root "$SURF_ACE_STATE_ROOT" \
  --endpoint "$SURF_ACE_CONTROLLER_ENDPOINT" \
  --product-label "$SURF_ACE_PRODUCT_LABEL" \
  capture-pane --input-json "$CAPTURE_INPUT_JSON"
```

If the approved run separately authorizes migration material for this exact surface and operation, add the exact authorized object as `migrationMaterial`. Do not invent, derive, broaden, or reuse migration material. Do not claim that an empty object proves there is no migration state.

Decode returned PNG bytes. Record the image SHA-256, dimensions, capture metadata, and source JSON. Preserve the raw response.

### Read

`read` uses the run-owned local projection. The invocation needs the state root and exact projected scope. Omit the network endpoint.

```sh
READ_SCOPE_ID="pane:${SURFACE_ID}:${PANE_ID}"
READ_INPUT_JSON="$(jq -nc --arg scopeId "$READ_SCOPE_ID" '{scopeId:$scopeId}')"

"$SURF_ACE_BIN" \
  --state-root "$SURF_ACE_STATE_ROOT" \
  read --input-json "$READ_INPUT_JSON"
```

Store the response in a file. Require CLI exit code 0, top-level `ok: true`, `command: read`, the expected `result.scopeId`, the matching acknowledgement scope, `result.cacheStatus: current`, and a content record with the expected `contentId`. Do not require `result.ok`; local `read` does not use the network-response envelope.

Source `05-read-response-validator.sh` from the canonical bundle. Call `surf_ace_read_response_ok` with the CLI exit code, response path, expected scope, and expected content id. The exact tick-0 response in `fixtures/tick-0-read-success.json` must pass the validator self-test.

### Topology changes

Replace a split operation with `topology-intent`. Supply the pane and revision from the latest `list` result:

```sh
SPLIT_INPUT_JSON="$(jq -nc \
  --arg surfaceId "$SURFACE_ID" \
  --argjson paneId "$PANE_ID" \
  --argjson expectedTopologyRevision "$CURRENT_TOPOLOGY_REVISION" \
  --arg direction "$SPLIT_DIRECTION" \
  '{action:"split",surfaceId:$surfaceId,paneId:$paneId,count:2,direction:$direction,expectedTopologyRevision:$expectedTopologyRevision}')"

"$SURF_ACE_BIN" \
  --state-root "$SURF_ACE_STATE_ROOT" \
  --endpoint "$SURF_ACE_CONTROLLER_ENDPOINT" \
  --product-label "$SURF_ACE_PRODUCT_LABEL" \
  topology-intent --input-json "$SPLIT_INPUT_JSON"
```

Replace a close operation with the same command and identities from a fresh `list` result:

```sh
CLOSE_INPUT_JSON="$(jq -nc \
  --arg surfaceId "$SURFACE_ID" \
  --argjson paneId "$PANE_ID" \
  --argjson expectedTopologyRevision "$CURRENT_TOPOLOGY_REVISION" \
  '{action:"close",surfaceId:$surfaceId,paneId:$paneId,expectedTopologyRevision:$expectedTopologyRevision}')"

"$SURF_ACE_BIN" \
  --state-root "$SURF_ACE_STATE_ROOT" \
  --endpoint "$SURF_ACE_CONTROLLER_ENDPOINT" \
  --product-label "$SURF_ACE_PRODUCT_LABEL" \
  topology-intent --input-json "$CLOSE_INPUT_JSON"
```

Use `topology-realize` only when the scenario requires a complete desired tree. Record the desired tree, destruction allowlist, expected revision, request, receipt, and realized result.

Use `surface-intent` for supported window open, close, or restore operations. Use `target-register` and `target-apply` only for scenarios that explicitly test target materialization.

## Command equivalence register

Apply this mapping everywhere in `02-fleet-soak-phases.md` and
`03-fleet-soak-run-checklist.md`.

| Procedure action | Gibson CLI action |
| --- | --- |
| Discover and refresh fleet topology | `list --input-json '{}'` |
| Read the projected pane or surface scope | local `read` with the exact `scopeId` |
| Push content | `push` with discovered `surfaceId`, numeric `paneId`, unique `contentId`, typed content, and run label |
| Capture pane pixels and visible text | `capture-pane` with discovered `surfaceId` and numeric `paneId` |
| Split, close, restore, or rename a pane | `topology-intent` with the current topology revision |
| Realize a complete desired topology | `topology-realize` with the expected revision and explicit destruction allowlist |
| Open, close, or restore a surface | `surface-intent` with the current surface-set revision |
| Clear pane content | `clear` with the expected content revision |
| Remove annotations | `annotations-remove` with exact content and stroke identities |
| Register or apply a native/process target | `target-register` or `target-apply` with exact target provenance |

## Surfaces driven by Gibson

CLI `list` discovers candidate surfaces and current topology. It does not admit a candidate and does not authorize mutation.

Admit a discovered candidate only when durable evidence binds the exact `surfaceId`, controller fixture identity, fixture expiry and cleanup contract, restart-validity boundary, exact run-owned state root, covered target-operation set, gated operator identity, issuer/authority, and immutable artifact identity to one of these bases:

1. evidence that the surface is already lockless; or
2. separately authorized explicit migration material and its supported CLI input location for that surface and operation.

Record the evidence reference and basis before the first operation that targets the surface. Discovery evidence, topology coherence, a remembered prior success, or admission of another surface cannot substitute for this evidence.

For the already-lockless basis, accept only an immutable record from a preflight executor that is separately authorized to attest endpoint-fixture compatibility for the exact run. The record must contain `admissionBasis: already-lockless`, `lockless: true`, exact `surfaceId`, exact controller-fixture identity, exact run-owned state-root identity, exact gated-operator identity, covered target-operation set, verification method and result, reversible probe and rollback proof, issuer/authority reference, issue time, expiry, cleanup contract, restart/recovery validity, custody handoff, and artifact identity or SHA-256. The verifier must reject a missing field, expired evidence, an authority mismatch, a fixture, state-root, surface, or operator mismatch, a read-only row, a row from another state root, or an operation outside the recorded set. A `list`, topology, readback, diagnostic, remembered success, operator assertion, or another surface's result never satisfies this predicate.

| Surface | Gibson-driven role | Required evidence |
| --- | --- | --- |
| Racter production Electron/compositor surface | Production desktop candidate | CLI discovery, per-surface admission evidence, exact window/pane topology, read, mutation receipt, and capture |
| eezo Surf Ace windows and panes | macOS development and orchestration candidates | CLI discovery plus independent admission evidence for each targeted surface |
| Aleph iPad | Real-device tablet candidate | CLI discovery, per-surface admission evidence, device identity, push/read/capture evidence |
| Ansible iPhone | Real-device phone candidate | CLI discovery, per-surface admission evidence, device identity, push/read/capture evidence |
| Cyberbrain visionOS windows and panes | Spatial multi-window candidates | CLI discovery plus independent admission evidence for each targeted surface |
| Surf Ace simulator | Controlled baseline and fault-injection candidate | CLI discovery, per-surface admission evidence, stable identity, push/read/capture evidence |

Treat a controller-hosted client as a candidate only if `list` proves a distinct client surface runs there. Admit it only through the same per-surface gate. Preserve the dynamic window admission rule in `02-fleet-soak-phases.md`.

## CLI discovery and per-surface mutation-admission gate

Run this gate after the Electron cleanup and build-identity steps, but before Phase 1.

1. Verify the CLI file SHA-256 and bind it to its source and review.
2. Verify the controller endpoint fixture, its identity, expiry, cleanup contract, and host reachability. Create or select the empty run-specific state root that the gated operator will later use. Record one run-specific preflight-ready fact kind and the work-item scope.
3. Run the harmless CLI `list` invocation.
4. Store the full request, response, exit status, endpoint identity, state-root identity, and CLI hash.
5. Require `ok: true` and a coherent discovered fleet.
6. Stop `RED — BLOCKED: CLI_CONTROL_PLANE_UNAVAILABLE` if the CLI cannot execute, reach the approved controller endpoint, establish controller identity, or return coherent topology.
7. Record each returned surface as a discovered candidate with its pane identities, stable identity, topology revision, product build, and observability level.
8. Select one candidate as the required primary surface. Select additional candidates only when the run needs optional multi-surface coverage.
9. Before the preflight starts, the gated operator subscribes to the exact preflight-ready fact kind and scope. A fallback wake can report a missing fact, but it never transfers custody.
10. For each selected candidate, require one of these evidence paths:
   - a separately authorized preflight executor runs the bounded reversible probe inside the exact run-owned state root, covers each planned first-boundary operation, restores the preflight baseline under the semantic restoration oracle below, and issues the immutable already-lockless row; or
   - the run records separate authority, exact explicit migration material, and supported CLI input location for that surface and operation.
11. The preflight executor runs fresh `list` through the exact state root after it records the row. It compares the returned `controllerInstanceId`, selected surface, and pane with the row. It files the preflight-ready fact only when every binding matches.
12. After the fact arrives, the gated operator runs fresh `list` through the exact state root. It compares the current controller, state root, operator, surface, pane, boundary, and operation set with the row. A completion, direct message, or artifact without the matching fact is not a handoff.
13. Admit the candidate only after steps 10–12 pass. Exclude candidates without one of those two evidence bases. For the already-lockless path, the row must name the exact controller fixture, exact surface and pane, exact run-owned state root, exact gated operator, exact covered operations, issue time, expiry, restart validity, cleanup contract, rollback proof, preflight-ready fact kind and scope, and custody handoff.
14. Perform all required multi-pane topology work inside the primary admitted surface. Treat multi-surface execution as optional. Apply this gate independently to each additional surface.
15. If any selected operation returns `pair.request` with `capability_mismatch`, stop before mutation. Preserve the request and response. Classify endpoint/procedure readiness. Clean the run-owned fixture and state at the terminal boundary. Route a fresh fixture. Treat it as a new admission boundary: repeat fixture verification, fresh `list` discovery, candidate selection, and steps 9–13 for every surface before any target operation. Do not retry, bypass the refusal, reuse an old fixture's admission row, invent migration material, or require a source change.

After a restart, relaunch, gateway/provider bounce, network recovery, ownership handoff, or state-root change, run discovery again. Reuse admission only when the exact surface/controller-fixture binding is unchanged, the same gated operator still owns the run, the same state root remains in force, the row is not read-only, and the recorded admission evidence explicitly covers that boundary. Otherwise, treat the result as a candidate and repeat steps 7–13 before the next target operation. Never reuse admission across a fresh-fixture route; fresh discovery and a new admission-table row are mandatory even if a `surfaceId` repeats.

Immediately before each target operation, recheck the admission row's expiry, exact surface/controller-fixture binding, exact state-root binding, exact gated-operator binding, boundary validity, operation coverage, and non-read-only status. If one check fails, return the surface to candidate state and repeat steps 7–13. Do not target the surface until a new row passes.

Do not require a separate tool declaration. Do not call a provider plugin as a substitute.

### Preflight restoration oracle

After each reversible split/close probe, run fresh `list`, `read`, and `capture-pane` for the surviving baseline pane. Require the intended one-pane topology. Validate `read` with `05-read-response-validator.sh`, including the expected content id and `cacheStatus: current`. Build the restoration summary from the baseline and restored capture payloads without image bytes. Source `06-restoration-oracle.sh` and require `surf_ace_restoration_ok` to pass.

The semantic restoration fields are the exact pane id, content id, content type, revision, visible text, selection, and viewport. Preserve both PNG files and their SHA-256 values in the evidence manifest. Do not use PNG byte equality as the restoration predicate. A changed PNG SHA-256 with matching semantic fields is evidence, not a failure. A wrong pane, content id, content type, revision, visible text, selection, or viewport is a failure. A missing or stale restored read is a failure.

## Mandatory capture-and-compare after every push

Run these steps immediately after every successful or outcome-unknown `push`. Apply them to baseline, topology, history, retry, recovery, and fault-recovery pushes.

1. Record the expected surface, pane, topology, content, visible marker, metadata, revision, and retry status.
2. Run CLI `push`. Store the full response and correlation identifiers.
3. Run CLI `list`. Verify the exact surface, pane, topology revision, and content association.
4. Run local CLI `read` for the exact projected scope. Verify synchronized content and acknowledgement state.
5. Run CLI `capture-pane` for the same surface and pane.
6. Decode and inspect the returned pixels. Verify that they contain the expected marker and zero occurrences of each sibling pane's marker. Compare layout, colors, clipping, and images.
7. Compare the capture metadata, list topology, read projection, content identity, and operation receipt.
8. Record one classification and one per-push evidence row.

Use these classifications:

| Classification | Meaning | Run effect |
| --- | --- | --- |
| `MATCH` | Primary capture exists; pixels, metadata, list, read, receipt, and pane agree | Continue |
| `MISMATCH` | Pixels, metadata, topology, content, or correlation disagree | Stop the affected path and grade it Red |
| `PRIMARY_CAPTURE_FAILED_FALLBACK_MATCH` | CLI capture failed, but approved screenshot or photo evidence matches | Preserve the primary failure and grade Yellow at best |
| `PRIMARY_CAPTURE_FAILED_FALLBACK_MISMATCH` | CLI capture failed and fallback evidence does not match | Stop the affected path and grade it Red |
| `NO_CAPTURE_ROUTE` | Neither CLI capture nor approved fallback evidence exists | Mark visual proof unproved; grade Yellow at best or Red when visual proof gates release |

Record one row for every push:

| Time | Surface/pane | CLI request and receipt | Expected pixels | Expected metadata | List result | Read result | Observed pixels | Capture reference | Classification | Failure reference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

A batch capture cannot replace per-push evidence.

## Phase and checkpoint integration

Preserve the phase order and checkpoint durations in `02-fleet-soak-phases.md`.

1. **Pre-flight 0:** clean stale Electron instances only on each host that owns an Electron target. Do not clean Gibson merely because it coordinates the run.
2. **Pre-flight 1:** record build and deployed identities.
3. **Pre-flight 1.5:** run the CLI discovery and per-surface admission gate above.
4. **Pre-flight 2 and 3:** record observability and start immutable evidence capture.
5. **Phase 1:** use CLI list, push, read, and capture on the primary admitted surface for baseline attach, then repeat list/read/capture after the two-minute idle.
6. **Phase 2, Sequence A:** use CLI topology-intent split and close calls inside the primary admitted surface. Run list/read/capture after each mutation and after the two-minute dwell.
7. **Phase 2, Sequence B:** use CLI topology-intent or topology-realize inside the primary admitted surface for the three-pane lifecycle. Preserve the recursive-tree and orientation checks.
8. **Phase 2, Sequence C:** run ten CLI churn cycles. Preserve the 60-minute dwell and ten-minute checkpoints.
9. **Phase 2.5:** use unique `contentId` and `friendlyChatName` values to test history replacement or fronting for two chat identities, including the restart repetition.
10. **Phase 2.6:** run the two-pane push oracle entirely through CLI list, push, read, and capture-pane calls. Preserve the two-minute idle and restart checks.
11. **Phase 3:** preserve the 5-, 15-, and 30-minute idle checkpoints. At each checkpoint run list, read, capture, and every stated health check for each admitted pane in scope.
12. **Phase 4:** require one bounded restart/recovery cycle on the primary admitted surface. Preserve the other one-at-a-time gateway/controller, provider, surface, network, and ownership experiments as optional scenarios that require separate authority. Use only the approved host-control action for the fault itself. Use the CLI for all Surf Ace restoration and proof.
13. **Phase 5:** preserve each ten-minute dwell and use CLI evidence at every truth check.

The checklist in `03-fleet-soak-run-checklist.md` remains mandatory.

## Failure and retry rules

- Stop a mutation path on an unknown outcome. Do not retry it until later evidence resolves the exact request.
- Refresh topology before every mutation. Never use a stale revision or remembered pane identity.
- Treat a revision conflict as evidence of concurrent change. Re-list and re-plan; do not force the old request.
- Treat `pair.request` `capability_mismatch` as a terminal admission/readiness refusal for that fixture. Stop before mutation and do not retry it.
- Treat the routed fresh fixture as a new admission boundary. Run fresh discovery and per-surface admission before any target operation; do not carry an old fixture's admission row forward.
- Preserve raw CLI standard output, standard error, exit status, input JSON, and decoded artifacts.
- Do not treat provider logs, state files, or direct protocol probes as successful CLI-path proof.
- Diagnose failures without changing product, packaging, installation, or procedure scope. Route a separate repair card when the failure belongs elsewhere.

## Intentional divergence register

These adaptations apply throughout this bundle.

| ID | Gibson adaptation | Reason and effect |
| --- | --- | --- |
| `GIB-CLI-01` | The reviewed native CLI is the only Surf Ace command path | Establishes one supported control path |
| `GIB-CLI-02` | Gibson supplies an approved controller endpoint, run-specific state root, and product label to each network command | Uses the proven standalone V3 invocation contract |
| `GIB-CLI-03` | CLI `list` is the discovery and topology source for test actions; it does not admit a surface | Separates discovery from mutation authority |
| `GIB-CLI-04` | CLI `push`, `read`, and `capture-pane` form the per-push correlation oracle | Preserves receipt, projection, and visual proof without a provider tool |
| `GIB-CLI-05` | CLI topology-intent, topology-realize, and surface-intent perform structural operations | Preserves inherited topology phases through the supported command set |
| `GIB-CLI-06` | Capture-and-compare remains mandatory after every push | Preserves the stronger Gibson visual-proof rule |
| `GIB-CLI-07` | Electron cleanup and fault injection occur only on the host that owns the affected process | Keeps host mutation scoped to runtime ownership |
| `GIB-CLI-08` | Gibson retains CLI inputs, outputs, receipts, reads, captures, and grading in the canonical artifact location | Keeps review evidence complete and accessible |
| `GIB-CLI-09` | Each targeted surface needs durable lockless evidence or separately authorized explicit migration material | Prevents discovery or another surface's success from authorizing mutation |
| `GIB-CLI-10` | Required topology and endurance proof runs inside one primary admitted surface; additional surfaces are optional and independently admitted | Preserves full multi-pane proof without manufacturing multi-surface readiness |

## Final report additions

In addition to the checklist final matrix, report:

- Gibson session and operator identity;
- CLI execution host, path, SHA-256, source commit, and review;
- controller endpoint identity and run-specific state-root identity;
- discovered candidates, admitted surfaces, excluded surfaces, and the controller-fixture binding, validity boundary, and admission evidence basis for each targeted surface;
- every exercised divergence ID;
- counts of `MATCH`, `MISMATCH`, fallback, and `NO_CAPTURE_ROUTE` rows;
- all pushes without a complete per-push evidence row;
- every unknown mutation outcome and its final resolution;
- first concrete failure for each Red or Blocked result;
- durable references to raw CLI inputs, outputs, receipts, reads, captures, decoded images, and the completed checklist.

Do not promote, deploy, or change fleet ownership from this report. Route release and remediation decisions through the owning work item.

## V4 admission and oracle repair

V4 changes the admission and execution-scope clauses plus the sibling-pane capture-isolation assertion identified by independent review:

1. It makes `list` discovery-only.
2. It requires the complete already-lockless evidence predicate or separately authorized explicit migration material before targeting a surface, and it rechecks expiry, binding, boundary validity, and operation coverage immediately before each target operation.
3. It makes one admitted surface sufficient for required multi-pane, endurance, and bounded restart/recovery proof.
4. It makes additional surfaces optional and independently admitted.
5. It makes `pair.request` `capability_mismatch` a terminal pre-mutation endpoint/procedure-readiness result for the current fixture and requires fresh discovery plus new per-surface admission on the routed fresh fixture.
6. It requires each pane capture to contain its own marker and zero occurrences of its sibling pane's marker.
7. It preserves the CLI-only path, phase order, 2/5/15/30-minute checkpoints, 60-minute churn dwell, repeated push/capture oracle, grading, and release judgment.

`04-v4-changed-clauses.md` lists each edited V3 clause.

## V3 procedure revision record

This section records V3 history only. V4 supersedes its items 1 and 5: `list` now proves discovery readiness, while per-surface admission requires separate durable evidence.

This revision changes only the Gibson control path:

1. It makes CLI provenance and a harmless CLI list call the admission requirement.
2. It makes the reviewed native CLI the official control path.
3. It adds dynamic, JSON-encoded list, push, capture-pane, read, and topology invocation shapes.
4. It maps every discovery, content, capture, topology, surface, and target action to a CLI command.
5. It replaces the pre-flight tool gate with a CLI and controller-endpoint gate.
6. It keeps the phase order, durations, checkpoints, invariants, grading, and release bar.
7. It keeps the mandatory per-push capture-and-compare oracle.
8. It adds CLI input, output, receipt, state-root, and endpoint evidence to the final report.

## V2 review corrections

This V2 preserves V1 as `art_32f3e080` and changes only the two independent-review findings:

1. Every pane ID and expected topology revision in an invocation is now a dynamic uppercase shell variable encoded as a JSON number.
2. The `read` section no longer claims that the reviewed CLI rejects the product-label option. The canonical invocation omits the network endpoint and uses the run-owned local projection.
