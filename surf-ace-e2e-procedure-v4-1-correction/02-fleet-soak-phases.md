# Surf Ace Fleet Soak Procedure

> Purpose: catch the failures that only show up over time — disconnect/reconnect churn, ownership weirdness, topology drift, and recovery after pieces of the system go down and come back.
>
> This is the procedure to run whenever we change the Surf Ace protocol, provider/networking behavior, topology realization logic, ownership/locking behavior, or reconnect lifecycle.

## What this procedure is for

This is **not** an "it connected once" checklist.

This procedure is meant to answer the real product questions:

- Does the Surf Ace fleet stay connected over time?
- When something disconnects, does it recover cleanly?
- Does the provider's realized topology stay aligned with what the user can actually see?
- Do pane identities stay stable through split/close/reconnect/restart churn?
- Does the network recover sanely when the gateway, provider, or a surface goes down and comes back?
- Do we preserve product truth under stress, not just in a happy-path demo?

## Fleet under test

### iOS / visionOS surfaces

- **iPad Simulator**
  - Best for full control, repeatability, and observability
  - Use for topology churn, reconnect loops, and automated readback assertions
- **Aleph**
  - Real-device iPad deploy target
  - Best for actual device/network behavior
  - Visual observability may be limited; compensate with stronger readback/log capture
- **Ansible when admitted**
  - Real-device iPhone target
  - Treat current `surf-ace list` output as discovery evidence only
  - Admit it only when durable evidence passes the complete already-lockless predicate in `00-v4-contract.md` or the run separately authorizes explicit migration material for it
  - Grade it independently from every other iOS surface
- **All Cyberbrain Surf Ace windows/panes admitted to the run**
  - visionOS multi-window deploy target
  - Window labels are dynamic; do not hard-code a label as the fleet definition
  - Treat every Cyberbrain Surf Ace window/pane as its own surfaced runtime
  - Each must be checked independently for topology truth, mutability, readback, websocket health, and churn
  - A pass on one Cyberbrain window/pane must never mask yellow, reconnect, lineage, or mutability failure on another

### Electron / desktop surfaces

- **Racter Surf Ace**
  - Best desktop visual observability
  - Use for visible truth checks and reconnect/restart behavior you can actually watch
- **All eezo Surf Ace windows/panes admitted to the run**
  - Window labels are dynamic; do not hard-code a label as the fleet definition
  - Treat every eezo Surf Ace window/pane as its own surfaced runtime, not just part of a generic eezo bucket
  - Each must be checked independently for topology truth, mutability, readback, websocket health, and churn
  - A pass on one eezo window/pane must never mask yellow, reconnect, lineage, or mutability failure on another
- **eezo (shared build/runtime host notes)**
  - Both eezo windows may share the same host build, but the smoke bar is per window, not per host
  - If visual capture is unavailable, rely on provider truth + readback + logs, but mark the run as partially observed

## Core test principle

For every significant step, compare at least two of the following:

1. **Expected topology** — what the test intended.
2. **CLI truth** — what the reviewed native CLI returns, especially from `surf-ace list`.
3. **Independent rendered or provider truth** — `surf-ace capture-pane` pixels and metadata, `surf-ace read` content, or an approved product diagnostic surface.
4. **Visible truth** — what is actually on-screen.

A test is strong only when the available truths agree.

Before topology soak starts, prove from reviewed CLI provenance or command inventory that the CLI supports each command required by the run. At minimum, verify `list`, `read`, `capture-pane`, `push`, `topology-intent`, and any `topology-realize` scenario without targeting a discovered candidate. If a required command is absent or the later CLI discovery call fails, stop `RED — BLOCKED: CLI_CONTROL_PLANE_UNAVAILABLE`.

Run every Surf Ace discovery, topology, content, read, and capture operation through the reviewed native CLI. Direct HTTP or WebSocket calls, provider logs, DNS-SD, local runtime files, debug JSON, screenshots, and remembered identities are diagnostic only. They can explain a failure. They cannot prove the CLI path.

Create, split, close, replace, or realize panes only through the reviewed CLI. Build each request from a fresh `list` result. If the CLI cannot perform a required topology mutation, stop the affected path and grade it Red.

Push content only through `surf-ace push`. Use the `surfaceId` and numeric `paneId` from the current `list` result. If the CLI cannot push to the intended pane, stop the affected path and grade it Red.

For topology proof, pane count is insufficient. The run must compare the complete recursive topology returned by `surf-ace list` — split tree shape, split direction/orientation, leaf pane identity/order, pane labels, viewport/geometry, and `topologyRevision` — against an independent rendered/provider truth source available in the product diagnostic path. A mismatch between tool topology and rendered/provider truth is a product failure. Operators must not downgrade it to a judgment call because logs, direct runtime probes, or screenshots appear plausible.

Use `surf-ace capture-pane` as the primary visible-truth oracle for every admitted pane that supports it. The capture request must name the explicit `surfaceId` and numeric `paneId` from `surf-ace list`; do not infer a pane from labels alone. For marker checks, push a unique marker into one pane, capture that exact pane, and verify the returned image bytes/metadata show the marker in the same `surfaceId`, `windowLabel`, `paneId`, `paneLabel`, and `topologyRevision` reported by provider topology.

If pane capture is blocked, record the returned `failureReason` and fall back to screenshot/photo evidence where possible. If no visible-truth path is available on a given surface, mark the result as **partially observed**, not fully verified.

## Surface discovery, admission, and run scope

`surf-ace list` discovers surfaces and current topology. It does not admit a surface and does not authorize mutation.

Select one discovered candidate as the primary surface. Before the first operation targets it, validate the complete already-lockless predicate in `00-v4-contract.md`: the immutable record must come from the separately authorized preflight executor, bind the exact surface/controller fixture, exact run-owned state root, exact gated operator, covered operations, verification result, rollback proof, handoff evidence, issuer, issue time, expiry, cleanup, restart validity, and artifact identity, and reject every read-only or cross-root or cross-operator row. Alternatively, record separately authorized explicit migration material and its supported CLI input location for that exact surface and operation. Exclude the candidate when neither basis exists.

Run the required repeated pushes, capture proof, multi-pane topology, dwell checkpoints, and one bounded restart/recovery cycle inside the primary admitted surface. Multi-surface execution is optional. Apply the same admission gate independently to each additional targeted surface.

Immediately before each target operation, verify that the admission row is unexpired and covers the exact surface/controller fixture, exact run-owned state root, exact gated operator, current boundary, exact operation, and non-read-only status. If one check fails, return the surface to candidate state and record a new passing admission row before targeting it.

If `pair.request` returns `capability_mismatch`, stop before mutation. Preserve the request and response. Classify endpoint/procedure readiness. Clean the run-owned fixture and state at the terminal boundary. Route a fresh fixture. The fresh fixture starts a new admission boundary: run fresh `surf-ace list` discovery and record a new passing admission-table row for every target surface before any target operation. Do not retry, bypass the refusal, reuse the old admission row, invent migration material, or require a source change.

## Dynamic window admission

Some surfaces, especially Cyberbrain and other multi-window clients, may not expose every test window at run start because Flynn may need to create windows manually after the client is deployed/launched. That is expected.

The discovered set is not frozen at process start. A window or pane becomes a candidate when it is intentionally created or first observed in current CLI output and associated with the approved controller. It becomes part of the run only after the per-surface admission gate passes. From that point forward it has the same obligations as each other included target: baseline content, provider truth, visible truth where available, mutability/readback, idle/churn-soak stability, recovery checks, and independent final grading.

If the operator has separate authority to create additional windows after the run starts, record them as candidates after discovery. Add a candidate to the run only after its independent admission evidence passes. Do not hard-code labels; record the discovered surface/window/pane tuple and admission basis at admission time.

## Required invariants

The soak pass tests these invariants continuously. The run is not Green unless the checklist marks each invariant exercised by the primary required path `Pass`. The checklist may mark only a named optional surface, identity check, or recovery scenario `Out-of-scope` when this procedure explicitly marks that item optional. Any `Fail` or `Unproven` invariant makes the E2E result Yellow or Red.


1. **Discovery stability**
   - surfaces appear consistently
   - identity/surfaceId does not unexpectedly change
   - busy/ownership state is plausible

2. **Session stability**
   - a claimed surface stays usable during normal idle periods
   - reconnect does not require manual ritual unless explicitly expected

3. **Topology truth**
   - provider topology matches the visible pane structure
   - split/close operations produce the intended surviving panes
   - window identity is unique and stable for every admitted visible window/surface
   - pane identity is unique and stable for every admitted visible pane address
   - duplicate-looking user-facing window/pane labels are explicitly evaluated against product spec; they cannot be ignored as tool-internal details
   - pane identity does not silently drift

4. **Content truth**
   - pushed content lands in the intended pane
   - surviving panes keep the expected content after adjacent pane mutations
   - content replacement does not mutate structure unless requested

5. **Multi-pane persistence truth**
   - multi-pane layouts must stay listed over time, not just appear immediately after split
   - the provider-reported pane set must remain stable through the dwell window on every included surface
   - all eezo Surf Ace windows/panes admitted to the run must each independently stay in their expected 2-pane content state when included
   - collapse/close after the dwell must cleanly restore the intended surviving topology

6. **Recovery behavior**
   - one bounded restart/recovery cycle on the primary admitted surface recovers
   - separately authorized gateway, provider, additional-surface, and network scenarios recover or are marked `Out-of-scope`
   - a surface staying listed is not enough if harmless mutation/readback no longer works
   - a changed surface/controller-fixture binding is re-admitted before the next target operation

7. **Ownership sanity**
   - ownership locks are real and understandable
   - handoff does not leave a surface wedged busy forever
   - stale ownership clears when it should

8. **Time-based reliability**
   - no silent decay over 5, 15, and 30 minute windows
   - no gradual drift between realized and expected topology
   - when a surface is intentionally left in a multi-pane state, those panes must still be present at the checkpoint rather than silently collapsing or disappearing
   - no reconnect/session churn loop during the dwell on a surface that otherwise still reports panes/content

## Pre-flight

Run this before every soak session.

### 0. Clear stale Electron app instances on every Electron target

This is the first executable step for Electron hosts named by separate run authority. Before starting any baseline, churn, or soak phase, kill stray or running Surf Ace Electron app instances only on those authorized hosts, so the run starts from a clean desktop or runtime state. This host cleanup does not admit a surface and does not authorize a target operation.

Why this is mandatory:

- test Electron instances tend to pile up
- stale instances can keep advertising, hold ports, confuse discovery, or leave fake busy/ownership state behind
- a soak run that starts from a dirty Electron process set is not trustworthy

Required outcome:

- no leftover Surf Ace test Electron processes remain on an authorized Electron host included in the run before the run begins
- if a single intentional baseline app instance is needed, launch exactly that instance after cleanup and record it in the run log

Record in the run log:

- what was found
- what was killed
- what intentional Electron instance(s) were relaunched for the test

### 1. Record build identity

For each surface under test, capture:

- repo path
- branch
- HEAD SHA
- deployed SHA or package/build identifier, if different from the repo HEAD
- whether the app was freshly deployed or already running
- whether the proof ran against deployed code, local checkout code, or an undeployed patch
- gateway/provider version if relevant

Do not run an ambiguous soak against unknown builds.

### 1.5 CLI discovery and per-surface mutation-admission gate

Before any topology soak can be Green, prove that the reviewed CLI path is available:

1. Record the CLI path, file SHA-256, source commit, and independent review reference.
2. Record the execution host, separately authorized preflight executor, designated gated E2E operator, controller endpoint fixture identity, fixture expiry and cleanup contract, product label, empty run-owned state root, preflight-ready fact kind, and work-item scope.
3. Invoke harmless `surf-ace list` with the canonical command shape in `01-gibson-cli-control-plane.md`.
4. Save the input, standard output, standard error, exit status, endpoint identity, state-root identity, and CLI hash.
5. Require `ok: true` and a coherent discovered fleet. Treat each result as a candidate only.
6. Stop `RED — BLOCKED: CLI_CONTROL_PLANE_UNAVAILABLE` if the command cannot execute, reach the approved endpoint, establish controller identity, or return coherent topology.
7. Select one primary candidate. Select additional candidates only for optional multi-surface coverage.
8. Before the preflight starts, the gated operator subscribes to the exact preflight-ready fact kind and scope.
9. For each selected candidate, either:
   - run the separately authorized reversible preflight probe inside the exact run-owned state root, cover the exact push, topology, capture, and read operations that the run will use before the next boundary, restore the preflight baseline under `06-restoration-oracle.sh`, and issue the immutable already-lockless row; or
   - record the separate authority, exact explicit migration material, and supported CLI input location for that surface and operation.
10. After it records the row, the preflight executor runs fresh `list` through the exact state root. It files the preflight-ready fact only if the current controller, selected surface, and pane match the row.
11. After the fact arrives, the gated operator runs fresh `list` through the exact state root. It compares the current controller, state root, operator, surface, pane, boundary, and operation set with the row.
12. Admit the candidate only after steps 9–11 pass. Record its branch, HEAD SHA, deployed SHA or package identity, deploy state, admission basis, exact state-root binding, exact gated operator, covered operations, rollback proof, fact delivery, and handoff evidence.
13. On `pair.request` `capability_mismatch`, stop before mutation, preserve exact evidence, classify endpoint/procedure readiness, clean the run-owned fixture and state, and route a fresh fixture without retry or bypass. Before resuming, repeat fixture verification, fresh `list` discovery, and steps 7–12 for every target surface. Do not reuse an admission row from the failed fixture.

Link the discovery artifact and each per-surface admission artifact in the run report. A list result without per-surface admission evidence is not mutation authority or product proof.

For each split/close rollback, preserve the baseline and restored PNG files and their SHA-256 values. Do not require byte-identical PNGs. Require the intended one-pane topology and exact agreement between baseline and restored pane id, content id, content type, revision, visible text, selection, and viewport. Require the restored local `read` to pass `surf_ace_current_read_response_ok`, including `cacheStatus: current` and no consumable loss. Accept an exact current-empty delta when the restored content predates controller admission; `capture-pane` carries the content comparison. A wrong or stale capture content value fails restoration.

### 2. Record observability level per surface

For each surface, explicitly mark one of:

- **Full** — visible screen + provider truth + logs
- **Medium** — provider truth + logs only
- **Low** — only liveness/discovery, no direct truth check

Confidence in results should track this.

### 3. Start artifact capture

Open a timestamped run log for the session and record:

- test operator
- date/time
- change being validated
- surfaces included
- observability limits
- failures seen
- screenshots/readbacks/log snippets
- `surf-ace capture-pane` artifacts for every marker/topology oracle check, including metadata and failure reasons

## Standard test content

Use stable, human-legible content so pane truth is obvious.

Recommended labels:

- `A / red`
- `B / blue`
- `C / green`
- `D / gold`

Each pane should show unmistakably different content so drift is visible immediately.

For any multi-pane phase, do not leave panes empty. Push explicit payloads into every pane that matters to the check, and record which label/content belongs in which pane so content drift is testable instead of implied.

## Test phases

## Phase 1 — Baseline attach and truth check

Run on the primary admitted surface. Run on any additional surface only after it passes the same independent admission gate.

For each included surface or window:

1. Confirm it is discoverable.
2. Verify its current controller association through the CLI result.
3. Push a single full-screen baseline payload.
4. Verify provider truth.
5. Verify visible truth where possible.
6. Leave it idle for 2 minutes.
7. Re-check discovery, connection health, provider truth, and visible truth.

### Pass criteria

- the primary surface is discovered and independently admitted
- each optional additional surface is discovered and independently admitted
- association succeeds without unexplained busy-state residue
- baseline content remains correct after 2 minutes idle
- no unexplained disconnect or topology change

## Phase 2 — Topology churn

Run fully inside the primary admitted surface. Run on additional surfaces only when they are independently admitted. Multi-pane proof inside the primary surface satisfies the required topology scope; multi-surface proof is optional.

### Sequence A: two-pane lifecycle

1. Start from one pane showing `A`
2. Split into two panes using the CLI `surf-ace topology-intent` with `action:"split"` tool
3. Push `B` into second pane using the CLI `surf-ace push` tool and the numeric `paneId` returned by `surf-ace list`
4. Verify recursive topology, split direction/orientation, pane count, labels/ids, and visible content
5. Leave the two-pane layout idle for 2 minutes
6. Verify that both panes are still listed and still match visible truth where possible
7. Close second pane using the CLI `surf-ace topology-intent` with `action:"close"` tool
8. Verify surviving pane identity and content
9. Verify clean restoration back to the intended one-pane topology

### Sequence B: three-pane lifecycle

1. Start from one pane showing `A`
2. Split to create second pane using the CLI `surf-ace topology-intent` with `action:"split"` tool
3. Split again to create third pane using the CLI `surf-ace topology-intent` with `action:"split"` or `surf-ace topology-realize` tool required by the scenario
4. Push `A/B/C` into distinct panes using CLI `surf-ace push` calls and numeric `paneId` values returned by `surf-ace list`
5. Record the expected recursive split tree and orientation, not just the resulting pane count. For a three-vertical-pane case, the expected tree must explicitly encode the vertical split structure and leaf order.
6. Cross-check `surf-ace list.topology` against independent rendered/provider truth: pane capture metadata/pixels and readback for each leaf pane must agree with the tool-returned topology tuple and orientation.
7. Close one non-root pane using the CLI `surf-ace topology-intent` with `action:"close"` tool
8. Verify surviving pane identities, contents, and split-tree shape/orientation
9. Close another pane using the CLI `surf-ace topology-intent` with `action:"close"` tool
10. Verify collapse back to one pane
11. Leave idle 2 minutes
12. Verify again

### Sequence C: repeated topology churn soak

Repeat split/push/close cycles 10 times inside the primary admitted surface. When an independently admitted multi-window client such as Cyberbrain is also in scope, optionally repeat create/push/close cycles across its panes/windows: create several panes/windows under separate authority, push distinct content into each one, close a subset, then push again to each survivor.

This is not only a burst stress test. After the churn completes, hold the surviving multi-pane/multi-window layout for at least 60 minutes with 10-minute checkpoints. A window/pane that was green at baseline and then goes yellow/unreachable/connecting without user action or an explicit precursor event is a failure, even if no mutation was targeting that window/pane. Because Cyberbrain and eezo labels are dynamic, identify the failing target by the run-admitted surface/window/pane record instead of hard-coding a label.

Watch for:

- pane id drift
- surviving-pane content corruption
- mismatched visible vs realized tree
- stale phantom panes
- closed panes/windows lingering as stale `connecting` surfaces
- untouched green windows spontaneously turning yellow/unreachable/connecting
- ownership/session/epoch mismatch on valid surviving panes
- session id, ownership epoch, pane lineage, content, or history drift during the 60-minute dwell
- lockups after repeated mutations

### Pass criteria

- realized topology always matches expected topology
- `surf-ace list` topology, independent rendered/provider truth, and visible pane structure agree where visible checks exist
- split tree shape and orientation are preserved; pane count preservation alone is not a pass
- no pane identity drift unless a destructive structural change explicitly requires it
- no mutation causes a wedge or permanent loss of control
- after churn, surviving panes/windows remain stable through the sustained dwell
- closed panes/windows are removed or tombstoned and are not resurrected as stale surfaces
- untouched green windows remain green through the dwell unless a captured precursor explains the transition

## Phase 2.5 — Chat push history replacement/fronting

Run this after Phase 2 has proven basic targeting stability on the chosen pane/window set. Use a small, controlled topology first; do not start this test during active reconnect/yellow churn or it will be impossible to interpret.

When a pushed item from a chat/session is present in pane history and the same chat/session pushes something new to that pane, the soak must verify one of the two allowed outcomes:

1. the existing history item from that chat/session is moved to the front/current position and displayed, or
2. the new content is displayed and the old content from that chat/session is removed from history.

Forbidden outcome: old content from the same chat/session remains buried in history while new content from that same chat/session is also added/displayed, creating duplicate or stale provenance entries.

Operational sequence:

1. Pick one stable pane/window that passed Phase 2.
2. From chat/session A, push `A1` with a unique `contentId` and `friendlyChatName`. Record the operation receipt and history position.
3. Push unrelated content from chat/session B so `A1` is no longer only the current visible item.
4. From chat/session A, push `A2` with a new `contentId` and the same `friendlyChatName`.
5. Verify either `A1` was fronted/current or `A2` is current and `A1` is removed from history.
6. Repeat with chat/session B to prove the rule is scoped by chat/session, not global.
7. Restart/reconnect the surface and repeat the same sequence to prove persisted history obeys the same rule.


## Phase 2.6 — Capture-backed push/topology truth oracle

Run this after Phase 2 has proven basic split/push targeting, and before long idle soak. This phase does **not** exist to prove capture works as a feature. It exists because pane capture is the visual oracle for the real product question: when the provider says it pushed content to a specific pane in the topology, did that exact visible pane actually show that content?

Run on the primary admitted surface where pane capture is expected to work. Run on each additional surface only after independent admission. Multi-surface coverage is optional.

### Required two-pane push oracle

1. Start from one known pane.
2. Split into two panes using the CLI `surf-ace topology-intent` with `action:"split"` tool.
3. Record the post-split provider topology for both panes: `surfaceId`, `windowLabel`, numeric `paneId`, `paneLabel`, `topologyRevision`, remote/provider pane identity when available, and viewport/dimensions.
4. Push typed markdown into the first/left pane by exact `surfaceId` and numeric `paneId`. The document must include the marker `SOAK-PUSH-MARKDOWN-{runId}-{surfaceId}-{paneId}` and must look like a document.
5. Push a second typed-markdown visual oracle into the second/right pane by exact `surfaceId` and numeric `paneId`. It must include the marker `SOAK-PUSH-CONTROL-{runId}-{surfaceId}-{paneId}`.
6. For each push, record the returned `contentId`, `operationReceipt`, `paneId`, `paneLabel`, correlation id, revision, and any apply evidence.
7. Immediately call `surf-ace list` / read state again and verify provider truth says each content item is associated with the intended pane identity.
8. Capture each pane with `surf-ace capture-pane` by the same exact `surfaceId` + numeric `paneId` used for the push.
9. Verify for each pushed pane:
   - image bytes are present, or a failure reason is recorded;
   - capture metadata matches the intended pushed pane tuple (`surfaceId`, `windowLabel`, `paneId`, `paneLabel`, `topologyRevision`);
   - decoded pixels contain the marker pushed to that exact pane;
   - decoded pixels do not contain the sibling pane's marker;
   - captured pixels agree with the `contentId`/visible-content state that provider/readback reports.
10. Run `surf-ace read` on both panes. Immediately after each push, use `surf_ace_read_response_ok` to require top-level success, current synchronized content, the matching acknowledgement, and the pushed content id. Do not require `result.ok`. Verify that the pushed delta agrees with the captured pixels and content id.
11. Leave the two-pane state idle for 2 minutes and repeat the complete list/read/capture verification in steps 7–10, including zero sibling-marker occurrences, without pushing new content. Use `surf_ace_current_read_response_ok` for the repeated read because the pushed record was already consumed; use `capture-pane` to prove unchanged current content.
12. Restart/relaunch the surface when in scope, reconnect, and repeat the complete list/read/capture verification in steps 7–10, including zero sibling-marker occurrences, without changing content. Use `surf_ace_current_read_response_ok` for the repeated read and `capture-pane` for current content truth.

### Pass criteria

- a push to pane A is visually proven in capture of pane A;
- a push to pane B is visually proven in capture of pane B;
- neither pane capture contains any occurrence of the sibling pane's marker;
- no push reports applied while the intended pane capture remains unchanged or stale;
- provider/list/read metadata agrees with captured pixels for the exact pushed pane;
- after idle/restart, the same pane identity still maps to the same visible pushed content or fails explicitly with a diagnostic;
- if capture is unavailable on a surface, the run must be marked Yellow at best for push/topology visible-truth confidence and must include the exact `failureReason` plus screenshot/photo fallback if possible.

### Failure signatures this phase must catch

- push reports `applied` but capture of the intended pane does not show the pushed marker;
- pushed marker appears in a different pane than the one targeted;
- provider/list says content is on one pane while capture shows it elsewhere;
- `surf-ace capture-pane` visible text says one thing while captured pixels show another;
- capture returns stale/previous content after a new push;
- capture returns no bytes, blocking visible proof of push/topology truth.

## Phase 3 — Idle soak

This is the heart of the procedure.

Run at minimum on the primary admitted surface. Include optional Cyberbrain, eezo, simulator, Aleph, Racter, or other surfaces only after each passes independent admission, and grade each included surface separately.

### Setup

Start Phase 3 from a clean, known state produced after Phase 2/2.5 cleanup, not from a half-mutated stress layout. If Phase 2 churn left extra panes/windows that are not part of the idle-soak baseline, close them first and verify the closed topology is gone.

Put each surface into a known state:

- stable topology (prefer 2-pane)
- distinct pushed content in each pane
- pane-to-content mapping recorded for the run
- active session/ownership recorded

This phase is not just a liveness dwell. It must explicitly prove multi-pane persistence.

Before starting the timers:

- leave each included surface in a known multi-pane layout
- push explicit, human-legible content into every pane in that layout
- record the expected pane count, pane identities, and pane-to-content mapping for that layout
- record which pane(s) must survive after collapse at the end of the dwell
- if eezo is included, record each eezo window/pane separately with their own expected 2-pane pane ids/content map

### Timers

Check at:

- 5 minutes
- 15 minutes
- 30 minutes

For each checkpoint verify:

- surface still discoverable
- claim/session still sane
- provider topology unchanged
- any `snapshot.get` timeout degrades only to stale snapshot/topology state, then retries later
- the expected multi-pane layout is still fully listed
- each pane still shows the expected pushed content
- visible truth still matches where screen observation exists
- harmless mutability/readback still works on every included surface, even if no structural change is intended
- `wsOpen=true` still holds on every included surface/window that is supposed to be healthy
- no bogus busy lock
- no reconnect storm in logs
- no session-id churn or repeated reconnect loop on a surface that otherwise still reports panes/content

### Pass criteria

- no unexplained disconnects
- no topology drift
- no silent content corruption
- no intentionally-created panes silently disappear during the dwell
- no pane loses or swaps its expected pushed content without an intentional mutation
- collapse/close after the dwell restores the intended surviving topology on every included surface
- no surfaces stuck busy after being otherwise healthy
- no `snapshot.get` timeout by itself closes the socket, rotates ownership/session state, collapses topology, clears content, or triggers a reconnect storm

Before entering Phase 4, restore a known-good baseline and record it. Phase 4 failures are only interpretable if they start from a clean baseline, not from unresolved Phase 2 or Phase 3 drift.

## Phase 4 — Failure injection and recovery

Do these one at a time. Re-establish a known baseline before each experiment.

### Required restoration proof after deploy/restart/bounce boundary

Any deploy, reinstall, restart, relaunch, or provider/client bounce in scope for the release must include a restoration proof before the soak can pass. This proof is required; it is not optional commentary.

Before crossing the boundary:

1. Record the exact admitted target list and the independent admission basis for each included surface/window/pane.
2. Use reviewed native CLI commands to create or confirm a nontrivial topology with multiple windows where supported and multiple panes per included surface/window where supported.
3. Push distinct content into every pane with CLI `surf-ace push`.
4. Record the expected recursive topology, pane identities, content ids, targets, history entries, visible paint/capture metadata, and any native/process target materialization evidence for each pane.
5. Save `surf-ace list`, `surf-ace read`, and `surf-ace capture-pane` artifacts for the baseline. If capture is unavailable for a pane, record the exact `failureReason` and the approved fallback evidence.

After crossing the boundary:

1. Use CLI `surf-ace list` to prove each expected admitted surface/window/pane is still discovered. If the exact surface/controller-fixture binding changed or prior admission evidence does not cover this boundary, re-admit the candidate before read, capture, or another target operation. A fresh fixture always requires fresh discovery and a new passing admission row, even if the `surfaceId` repeats. Then use read/capture and receipt evidence to prove it is actionable.
2. If windows do not reopen naturally and the scenario permits restoration, use `surf-ace surface-intent` and record its request, receipt, and response. This is a restoration path, not manual repopulation.
3. Use `surf-ace read` and `surf-ace capture-pane` on every expected pane to compare post-boundary state against the pre-boundary baseline.
4. Verify pane topology, content, targets, history, and visible paint are restored without manual repopulation.
5. For native/process panes, verify relaunch or reattach happened through the Surf Ace provider path. `restore_requires_confirmation`, `matching native pane window group was not observed`, empty `activeContent` for a native target, or manual confirmation required is a pane restore failure.

**Pass:** every expected window and pane is present or officially reopened, every pane's topology/content/target/history/paint matches the baseline, and every native/process pane relaunches or reattaches through the provider path without manual confirmation.

**Fail:** any expected pane is missing, non-actionable, manually repopulated, has empty or wrong active content, loses target/history/paint evidence, or requires manual confirmation for native/process restore.

### A. Gateway/provider restart

Run gateway and provider restarts as separate optional fault-boundary checks only when separately authorized and relevant to the change under test. They do not replace the required bounded primary-surface restart/recovery cycle.

1. Bring each admitted surface included in this optional scenario to a known good state
2. Restart only the approved Surf Ace gateway or controller process and record the exact command and process transition.
3. Observe each included admitted surface for reconnection behavior
4. Verify discovery, session sanity, topology truth, and content truth after recovery
5. Re-check again after 5 minutes idle
6. Restore a known good state
7. Restart only the Surf Ace provider/extension path and record the exact command/process transition
8. Observe each included admitted surface for reconnection behavior
9. Verify discovery, session sanity, topology truth, and content truth after recovery
10. Re-check again after 5 minutes idle

**Pass:** surfaces recover without manual cleanup beyond the expected reconnect path; no long-lived drift or false ownership residue.

### B. Individual surface restart

Run one bounded restart/recovery cycle on the primary admitted surface. Optional additional restart cycles may run on independently admitted surfaces under separate authority.

1. Put the surface in a known topology/content state
2. Kill/quit/relaunch that surface
3. Observe disappearance from discovery
4. Observe reappearance
5. Verify the restored controller association through fresh discovery. Re-admit before the next target operation when the binding changed or prior evidence does not cover restart.
6. Verify topology/content/identity behavior after recovery
7. Re-check after 5 minutes idle

**Pass:** restart produces understandable state transitions and a sane recovery path.

### C. Network interruption

When separately authorized and relevant, simulate a temporary network interruption for one admitted surface.

1. Record pre-interruption state
2. Interrupt connectivity briefly
3. Restore connectivity
4. Observe discovery and session recovery
5. Verify no permanent lock/busy wedge remains

**Pass:** temporary network loss either recovers cleanly or fails in a way that is explicit and recoverable.

A phase is not green if any included Cyberbrain or eezo Surf Ace window/pane churns/reconnects while another passes. Every included Cyberbrain and eezo window/pane must independently satisfy the same listing, `wsOpen=true`, harmless mutability/readback, and no-churn bar.

### D. Ownership handoff

Run this optional experiment only when separately authorized and relevant to the change under test.

1. Establish the approved controller association from session A.
2. Relinquish or replace that association through the approved run orchestration path.
3. Establish the approved controller association from session B.
4. Verify that ownership semantics are intelligible and surface truth remains sane

**Pass:** no orphaned lock, no invisible owner, no long-lived busy state with no active controller.

## Phase 5 — Longitudinal drift audit

This phase exists specifically because Surf Ace can appear healthy while slowly diverging from truth.

Run this after Phase 4 recovery is green or after explicitly resetting to a known-good baseline. Do not begin the longitudinal audit from a surface that is already yellow, reconnecting, or carrying unresolved failure-injection residue.

Run this on the primary admitted surface. Additional independently admitted surfaces are optional.

1. Establish a 2-pane state with obvious `A/B` content
2. Leave it alone for 10 minutes
3. Verify truth
4. Perform one structural mutation
5. Leave it alone for 10 minutes
6. Verify truth
7. Restart gateway or surface
8. Restore known state
9. Leave it alone again for 10 minutes
10. Verify truth

This phase is looking for:

- realized vs visible mismatch after time passes
- layout drift after reconnect
- pane identity confusion after multiple lifecycle transitions
- stale provider state surviving longer than reality

## Confidence grading

Every surface result should be graded:

- **Green** — provider truth and visible truth agree across soak + recovery steps
- **Yellow** — liveness and provider truth look good, but visible truth was partially unobserved
- **Red** — disconnect, drift, ownership wedge, or recovery failure observed

Overall protocol-change confidence should be based on the weakest important surface, not the happiest path.

## Minimum release bar after protocol/runtime changes

Do not call a protocol/runtime change ready unless all of the following are true:

1. **The primary surface has independent admission evidence** that passes the complete already-lockless predicate in `00-v4-contract.md` or binds separately authorized explicit migration material to that exact surface.
2. **The primary surface passes** baseline, repeated pushes with per-push capture proof, topology churn, chat history semantics when in scope, the 2/5/15/30-minute checkpoints, the 60-minute churn dwell, and one bounded restart/recovery cycle.
3. **Required multi-pane proof stays inside the primary admitted surface.** A second surface is not required.
4. **Each optional additional surface has independent admission evidence and an independent grade.** A result from the primary surface cannot admit or grade another surface.
5. **Each included multi-window client passes** create/push/close churn plus the sustained churn soak; spontaneous yellow on an untouched green window is a release blocker unless a captured external precursor explains it.
6. **Chat push history semantics pass** for at least two chat/session identities and after reconnect/restart when the change touches push provenance, history, target replay, or chat-originated content.
7. No unresolved realized-vs-visible topology mismatch remains on an included fully observed surface.
8. Snapshot timeout mitigation holds: `snapshot.get` timeout may mark stale and retry later, but must not cause socket teardown, session churn, ownership churn, content loss, topology collapse, or reconnect storm.
9. Capture-backed push/topology truth oracle passes on each included surface where pane capture is expected to work: each pushed marker is captured in the exact pane targeted by the push, each capture contains zero occurrences of its sibling pane's marker, and provider/list/read metadata matches the captured pixels.
10. No `pair.request` `capability_mismatch` was retried or bypassed. Any such refusal stopped the fixture before mutation and produced endpoint/procedure-readiness evidence plus cleanup. Any resumed run used a fresh fixture, fresh discovery, and a new passing admission row for every target surface.


## What to log when something fails

When a failure appears, capture immediately:

- timestamp
- surface name
- expected topology/content
- provider-reported topology/content
- visible truth (`surf-ace capture-pane` artifact first; screenshot/photo fallback if pane capture is blocked)
- pane-capture metadata: surfaceId, windowLabel, paneId, paneLabel, topologyRevision, visible content id, dimensions, scale, capture timestamp, and failure reason if blocked
- discovery status
- ownership/busy status
- what happened immediately before failure
- whether recovery required manual intervention

Do not summarize a drift bug as "reconnect issue" or "flaky networking" unless the evidence really supports that.

## Recommended run cadence

Run this procedure:

- after protocol changes
- after topology realization changes
- after ownership/locking changes
- after reconnect/lifecycle changes
- after gateway/provider restart-path changes
- before calling a networking/reliability bug fixed

## Known limitations

- **Aleph** may have incomplete visual observability
- **eezo** may require additional screen-observation setup for full confidence
- Visible truth is stronger than logs alone; if we cannot see a surface, we should be explicit that confidence is lower

## Required companion artifact

Use `03-fleet-soak-run-checklist.md` as the per-run checklist and log. It contains:

- build SHAs by surface
- test start/end time
- phase-by-phase results
- drift incidents
- screenshots/readbacks
- final confidence grading

---

## Bottom line

The job is not proving that Surf Ace can connect.

The job is proving that **the fleet stays sane over time** — across idling, topology churn, disconnects, restarts, and recovery — without the realized system slowly drifting away from the truth the user sees.
