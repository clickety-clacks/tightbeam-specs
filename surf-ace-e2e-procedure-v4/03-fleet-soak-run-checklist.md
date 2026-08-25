# Surf Ace Fleet Soak Run Checklist

Use this checklist with `00-v4-contract.md`, `01-gibson-cli-control-plane.md`, and `02-fleet-soak-phases.md` whenever Surf Ace protocol, topology, ownership, reconnect, or restart behavior changes.


---

## Required invariant gate — must be completed before marking Green

A Surf Ace E2E soak is **not Green** until every required invariant from `02-fleet-soak-phases.md` is checked below and marked `Pass`, `Fail`, `Unproven`, or `Out-of-scope`.

If any invariant is `Fail` or `Unproven`, the overall result must be **Yellow or Red**, not Green. Do not narrow an E2E soak after the fact to only the operations that passed.

- [ ] Discovery stability — surfaces appear consistently; identity/surfaceId does not unexpectedly change; busy/ownership state is plausible.
  - Status: `Pass / Fail / Unproven / Out-of-scope`
  - Evidence:
- [ ] Session stability — claimed surfaces stay usable during idle; reconnect does not require manual ritual unless expected.
  - Status: `Pass / Fail / Unproven / Out-of-scope`
  - Evidence:
- [ ] Topology truth — provider topology matches visible pane structure; split/close produce intended surviving panes; pane identity does not silently drift.
  - Status: `Pass / Fail / Unproven / Out-of-scope`
  - Evidence:
- [ ] CLI discovery readiness — the reviewed CLI hash and provenance are recorded, and harmless `surf-ace list` succeeds through the approved controller endpoint.
  - Status: `Pass / Fail / Unproven / Out-of-scope`
  - Evidence:
- [ ] Per-surface admission — before any operation targets a surface, durable evidence passes every field and rejection rule in the already-lockless predicate in `00-v4-contract.md`, or separately authorized explicit migration material with a supported CLI input location is bound to the exact surface and operation.
  - Status: `Pass / Fail / Unproven / Out-of-scope`
  - Evidence:
- [ ] Tool topology vs independent rendered/provider truth — recursive `surf-ace list.topology` shape, split orientation, leaf pane identities/order, pane labels, viewport/geometry, and `topologyRevision` are cross-checked against `surf-ace capture-pane` / `surf-ace read` and any product diagnostic provider truth available for the same pane tuple.
  - Status: `Pass / Fail / Unproven / Out-of-scope`
  - Evidence:
- [ ] Diagnostic-only boundary — logs, direct HTTP/WS probes, DNS-SD, local runtime/debug files, screenshots, remembered pane IDs, and successful admission of another surface are used only to explain failures; none substitutes for CLI discovery readiness plus independent per-surface admission.
  - Status: `Pass / Fail / Unproven / Out-of-scope`
  - Evidence:
- [ ] Window identity uniqueness — every admitted visible window/surface has a unique, stable user-facing window identity for the duration of the run; duplicate window labels/addresses, label churn, or ambiguous window identity are `Fail` unless explicitly justified by product spec and recorded.
  - Status: `Pass / Fail / Unproven / Out-of-scope`
  - Evidence:
- [ ] Pane identity uniqueness — every admitted visible pane has a unique, stable user-facing pane address for the duration of the run; duplicate pane addresses, bare duplicate labels presented as IDs, label churn, or ambiguous pane identity are `Fail` unless explicitly justified by product spec and recorded.
  - Status: `Pass / Fail / Unproven / Out-of-scope`
  - Evidence:
- [ ] Visible/user-facing pane identity — every user-visible pane address is unambiguous according to the current product spec; any duplicate-looking labels or ambiguous addresses are explicitly evaluated, not hand-waved as tool-internal identity.
  - Status: `Pass / Fail / Unproven / Out-of-scope`
  - Evidence:
- [ ] Content truth — pushed content lands in intended pane; surviving panes retain expected content after adjacent pane mutations; content replacement does not mutate structure unless requested.
  - Status: `Pass / Fail / Unproven / Out-of-scope`
  - Evidence:
- [ ] Multi-pane persistence truth — multi-pane layouts remain listed and visually/readback-correct through dwell on every included surface/window/pane.
  - Status: `Pass / Fail / Unproven / Out-of-scope`
  - Evidence:
- [ ] Recovery behavior — one bounded primary-surface restart/recovery cycle passes; optional separately authorized recovery scenarios pass or are `Out-of-scope`; changed bindings are re-admitted before target operations.
  - Status: `Pass / Fail / Unproven / Out-of-scope`
  - Evidence:
- [ ] Ownership sanity — ownership locks are understandable; handoff does not leave surfaces wedged busy; stale ownership clears when it should.
  - Status: `Pass / Fail / Unproven / Out-of-scope`
  - Evidence:
- [ ] Time-based reliability — no silent decay over required dwell/checkpoint windows; no gradual drift between realized and expected topology/content.
  - Status: `Pass / Fail / Unproven / Out-of-scope`
  - Evidence:

Final invariant sign-off:
- [ ] All invariants above are `Pass` or explicitly justified `Out-of-scope`
- [ ] No `Fail` / `Unproven` invariant remains while overall result is Green
- [ ] Each invariant exercised by the primary required path is `Pass`, including discovery, session, topology, CLI-only discovery readiness, primary per-surface admission, diagnostic-only boundaries, content, primary multi-pane persistence, the required bounded recovery cycle, and time-based reliability; `Out-of-scope` applies only to a named optional surface, identity check, or recovery scenario that the procedure explicitly marks optional
- [ ] Any caveat is surfaced in the report summary, not buried in logs

---

## Run metadata

- **Date:**
- **Operator:**
- **Change under test:**
- **Reason for run:**
  - [ ] Protocol change
  - [ ] Topology realization change
  - [ ] Ownership / locking change
  - [ ] Reconnect / lifecycle change
  - [ ] Gateway / provider restart-path change
  - [ ] Reliability bug fix validation
  - [ ] Other:
- **Procedure bundle:** `surf-ace-e2e-procedure-v4`
- **Primary admitted surface:**
- **Primary admission basis:** `already-lockless / separately authorized explicit migration material`
- **Primary admission evidence:**
- **Overall result:**
  - [ ] Green
  - [ ] Yellow
  - [ ] Red

---

## Build identity by surface

Complete the primary-surface section and any independently admitted optional-surface section. Mark each other named section `Out-of-scope`.

### iPad Simulator
- **Repo path:**
- **Branch:**
- **HEAD SHA:**
- **Deployed SHA / package id:**
- **Fresh deploy this run?**
- **Proof ran against deployed code?** `Yes / No / Mixed`
- **If No/Mixed, exact local checkout or patch used:**
- **Observability:**
  - [ ] Full
  - [ ] Medium
  - [ ] Low
- **Notes:**

### Aleph
- **Repo path:**
- **Branch:**
- **HEAD SHA:**
- **Deployed SHA / package id:**
- **Fresh deploy this run?**
- **Proof ran against deployed code?** `Yes / No / Mixed`
- **If No/Mixed, exact local checkout or patch used:**
- **Observability:**
  - [ ] Full
  - [ ] Medium
  - [ ] Low
- **Notes:**

### Ansible when admitted
- **Repo path:**
- **Branch:**
- **HEAD SHA:**
- **Deployed SHA / package id:**
- **Fresh deploy this run?**
- **Proof ran against deployed code?** `Yes / No / Mixed`
- **If No/Mixed, exact local checkout or patch used:**
- **Observability:**
  - [ ] Full
  - [ ] Medium
  - [ ] Low
- **Notes:**


### All Cyberbrain Surf Ace windows/panes admitted to the run
- **Window/pane labels present at baseline:**
- **Repo path:**
- **Branch:**
- **HEAD SHA:**
- **Deployed SHA / package id:**
- **Fresh deploy this run?**
- **Proof ran against deployed code?** `Yes / No / Mixed`
- **If No/Mixed, exact local checkout or patch used:**
- **Observability:**
  - [ ] Full
  - [ ] Medium
  - [ ] Low
- **Per-window/pane notes and grades:**

### Racter Surf Ace
- **Repo path:**
- **Branch:**
- **HEAD SHA:**
- **Deployed SHA / package id:**
- **Fresh deploy this run?**
- **Proof ran against deployed code?** `Yes / No / Mixed`
- **If No/Mixed, exact local checkout or patch used:**
- **Observability:**
  - [ ] Full
  - [ ] Medium
  - [ ] Low
- **Notes:**

### All eezo Surf Ace windows/panes admitted to the run
- **Window/pane labels present at baseline:**
- **Repo path:**
- **Branch:**
- **HEAD SHA:**
- **Deployed SHA / package id:**
- **Fresh deploy this run?**
- **Proof ran against deployed code?** `Yes / No / Mixed`
- **If No/Mixed, exact local checkout or patch used:**
- **Observability:**
  - [ ] Full
  - [ ] Medium
  - [ ] Low
- **Per-window/pane notes and grades:**

---

## Electron cleanup precondition — first executable step for Electron targets

- [ ] Separate run authority names each Electron host eligible for cleanup
- [ ] Killed stray/running Surf Ace Electron app instances on eezo only if eezo is an authorized included host
- [ ] Killed stray/running Surf Ace Electron app instances on Racter only if Racter is an authorized included host
- [ ] Killed stray/running Surf Ace Electron app instances on another host only if that host is authorized and included
- [ ] Host cleanup is recorded as pre-discovery cleanup, not surface admission or target-operation authority
- [ ] Confirmed no stale Surf Ace test instances still advertising / holding ports / reporting busy
- [ ] Relaunched only the intentional Electron instance(s) for this run
- **Notes:**

---

## Artifact capture started

- [ ] Timestamped run log created
- [ ] Reviewed CLI path, hash, source commit, and review reference recorded
- [ ] Harmless `surf-ace list` request/response artifact recorded
- [ ] Screenshots path recorded
- [ ] Readback/log capture path recorded
- [ ] Pane-capture artifact path recorded for `surf-ace capture-pane` outputs
- [ ] Any observability limitations recorded up front

Paths:
- **CLI provenance:**
- **Harmless `surf-ace list`:**
- **Run log:**
- **Screenshots / photos:**
- **Pane captures:**
- **Readbacks / exports:**
- **Gateway/provider logs:**
- **Endpoint fixture identity / expiry / cleanup:**

---

## CLI discovery and per-surface admission gate

- [ ] CLI path and SHA-256 recorded
- [ ] CLI source commit and independent review reference recorded
- [ ] Gibson execution host, endpoint fixture identity, fixture expiry and cleanup contract, product label, and run-owned state root recorded
- [ ] Harmless `surf-ace list` succeeds through the approved controller endpoint
- [ ] Input, standard output, standard error, exit status, and `surf-ace list` result saved as artifacts
- [ ] Each returned surface is recorded as a discovered candidate, not an admitted target
- [ ] One discovered candidate is selected as the primary surface
- [ ] Already-lockless evidence is immutable, issued by a separately authorized endpoint-fixture compatibility authority, and records `admissionBasis: already-lockless`, `lockless: true`, exact surface/fixture binding, covered operations, verification method/result, issuer/authority, issue time, expiry, cleanup, restart/recovery validity, and artifact identity/SHA-256; or separately authorized explicit migration material and its supported CLI input location are bound to the exact surface and operation
- [ ] Admission verifier rejected generic discovery/topology/readback/diagnostics, remembered success, operator assertion, another surface's result, and every record with a missing, expired, authority-mismatched, fixture-mismatched, surface-mismatched, or operation-out-of-scope field
- [ ] Branch, HEAD SHA, deployed SHA/package identity, deploy state, and admission basis recorded for the primary surface
- [ ] Each optional additional surface has its own admission evidence before any operation targets it
- [ ] Immediately before each target operation, the operator rechecks that the admission row is unexpired and covers the exact surface/controller fixture, current boundary, and operation; a failed check returns the surface to candidate state until a new row passes
- [ ] Required multi-pane work is scoped inside the primary admitted surface
- [ ] Multi-surface work is marked optional
- [ ] `pair.request` `capability_mismatch` has a terminal stop rule before mutation; no retry or bypass is permitted; a fresh fixture requires fresh discovery and a new admission row before any target operation
- [ ] Direct HTTP/WS, logs, DNS-SD, screenshots, and local runtime/debug files are labeled diagnostic-only
- **Result:** `Pass / Fail / Unproven`
- **Artifacts:**
- **Notes:**

Admission log — this table is the only seam that changes a candidate to admitted:

| Candidate `surfaceId` | Controller fixture / expiry / cleanup | Basis and explicit assertion | Issuer/authority + evidence or migration-material artifact/SHA-256 | Verification method/result + issue time | Covered target operations | Supported migration input location | Restart/recovery validity | Disposition |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  | `already-lockless + lockless:true / explicit migration` |  |  |  |  |  | `primary / optional / excluded` |

---

## Dynamic window discovery and admission log

- [ ] Operator-created windows/panes after deploy/launch are recorded as candidates when they appear
- [ ] Each candidate is added to the run only by an admission-table row with an admitted disposition
- [ ] Each admitted window/pane has its discovered surface/window/pane tuple and admission basis recorded
- [ ] Each admitted window/pane receives baseline content before being counted Green/Yellow/Red
- [ ] A discovered Cyberbrain/eezo window/pane without admission evidence remains excluded and untargeted

Derived admitted-target view — copy only admission-table rows with `primary` or `optional` disposition:
-

Discovered but excluded targets and reasons:
-

---

## Standard content labels prepared

- [ ] Pane A / red
- [ ] Pane B / blue
- [ ] Pane C / green
- [ ] Pane D / gold
- [ ] Explicit payload pushed into every pane used in the run
- [ ] Pane-to-content mapping recorded
- [ ] Content is visually unambiguous on observable surfaces

---

## Phase 1 — Baseline attach and truth check

- [ ] The primary admitted surface is identified below
- [ ] Additional surface sections are completed only for independently admitted surfaces; other sections are marked `Out-of-scope`

### Simulator
- [ ] Discoverable
- [ ] Current controller association verified through CLI evidence
- [ ] Baseline content pushed
- [ ] Provider truth verified
- [ ] Visible truth verified
- [ ] 2-minute idle passed
- [ ] Post-idle truth still correct
- **Result:**
- **Notes:**

### Aleph
- [ ] Discoverable
- [ ] Current controller association verified through CLI evidence
- [ ] Baseline content pushed
- [ ] Provider truth verified
- [ ] Visible truth verified if available
- [ ] 2-minute idle passed
- [ ] Post-idle truth still correct
- **Result:**
- **Notes:**

### Ansible when admitted
- [ ] Discoverable
- [ ] Current controller association verified through CLI evidence
- [ ] Baseline content pushed
- [ ] Provider truth verified
- [ ] Visible truth verified if available
- [ ] 2-minute idle passed
- [ ] Post-idle truth still correct
- **Result:**
- **Notes:**

### All Cyberbrain Surf Ace windows/panes admitted to the run
- [ ] Discoverable
- [ ] Current controller association verified through CLI evidence
- [ ] Baseline content pushed
- [ ] Provider truth verified
- [ ] Visible truth verified if available
- [ ] `wsOpen=true`
- [ ] Harmless mutability/readback verified
- [ ] No reconnect/session churn observed
- [ ] 2-minute idle passed
- [ ] Post-idle truth still correct
- **Result:**
- **Notes:**

### Racter
- [ ] Discoverable
- [ ] Current controller association verified through CLI evidence
- [ ] Baseline content pushed
- [ ] Provider truth verified
- [ ] Visible truth verified
- [ ] 2-minute idle passed
- [ ] Post-idle truth still correct
- **Result:**
- **Notes:**

### All eezo Surf Ace windows/panes admitted to the run
- [ ] Discoverable
- [ ] Current controller association verified through CLI evidence
- [ ] Baseline content pushed
- [ ] Provider truth verified
- [ ] Visible truth verified if available
- [ ] `wsOpen=true`
- [ ] Harmless mutability/readback verified
- [ ] No reconnect/session churn observed
- [ ] 2-minute idle passed
- [ ] Post-idle truth still correct
- **Result:**
- **Notes:**

### Any other admitted surface
- [ ] Discoverable
- [ ] Current controller association verified through CLI evidence
- [ ] Baseline content pushed
- [ ] Provider truth verified
- [ ] Visible truth verified if available
- [ ] `wsOpen=true`
- [ ] Harmless mutability/readback verified
- [ ] No reconnect/session churn observed
- [ ] 2-minute idle passed
- [ ] Post-idle truth still correct
- **Result:**
- **Notes:**

---

## Phase 2 — Topology churn

### Sequence A — Two-pane lifecycle
- [ ] Start from one pane `A`
- [ ] Split to two panes
- [ ] Push `B` into second pane
- [ ] CLI `surf-ace list` recursive topology verified, including split direction/orientation and leaf order
- [ ] `surf-ace list` topology cross-checked against independent rendered/provider truth for the same pane tuple
- [ ] Visible truth verified where possible
- [ ] 2-minute two-pane dwell passed
- [ ] Both panes still listed after dwell
- [ ] Close second pane
- [ ] Surviving pane identity verified
- [ ] Surviving pane content verified
- [ ] Clean restoration to intended one-pane topology verified
- **Result:**
- **Notes:**

### Sequence B — Three-pane lifecycle
- [ ] Start from one pane `A`
- [ ] Grow to three panes
- [ ] Push `A/B/C`
- [ ] Expected recursive split tree recorded; pane count alone is not accepted
- [ ] CLI `surf-ace list` recursive topology verified, including split direction/orientation and leaf order
- [ ] Three-pane orientation cross-checked against independent rendered/provider truth for each leaf pane
- [ ] Visible truth verified where possible
- [ ] Close one non-root pane
- [ ] Surviving identities verified
- [ ] Close another pane
- [ ] Collapse back to one pane verified
- [ ] 2-minute idle passed
- [ ] Post-idle truth still correct
- **Result:**
- **Notes:**

### Sequence C — Repeated topology churn soak
- [ ] 10 repeated split/push/close cycles completed inside the primary admitted surface
- [ ] Optional repeated split/push/close cycles on another independently admitted surface recorded when included
- [ ] Optional repeated create/push/close cycles completed on an independently admitted multi-window client when included
- [ ] Each cycle creates several panes/windows, pushes distinct content into every pane/window, closes a subset, then pushes again to all surviving panes/windows
- [ ] Closed panes/windows are removed or tombstoned and are not replayed, retargeted, or resurrected as stale `connecting` surfaces
- [ ] All surviving panes/windows remain reachable, targetable, and content-stable after each cycle
- [ ] After churn completes, hold the surviving multi-pane/multi-window layout for a sustained soak: minimum 60 minutes, with checkpoints every 10 minutes
- [ ] During the sustained churn soak, no untouched green window may drift to yellow/unreachable/connecting without an explicit precursor event
- [ ] During the sustained churn soak, every untouched Cyberbrain and eezo window/pane admitted to the run must remain green if it was green at its admission/baseline check; spontaneous yellow is a soak failure, not a harmless warning. Use the run-admitted target record because labels are dynamic and must not be hard-coded.
- [ ] Every 10-minute checkpoint verifies provider truth, visible truth where available, `wsOpen`, session id stability, ownership epoch/session stability, pane lineage stability, and content/history stability
- [ ] Every 10-minute checkpoint verifies `surf-ace list.topology` recursive shape/orientation against independent rendered/provider truth; any mismatch is marked `Fail`
- [ ] No pane-id drift observed
- [ ] No phantom panes observed
- [ ] No surviving-pane content corruption observed
- [ ] No ownership/session/epoch mismatch on valid surviving panes
- [ ] No spontaneous reconnect storm or surface disappearance observed
- [ ] No wedge observed
- **Result:**
- **Notes:**

### Sequence D — Chat push history replacement semantics
- [ ] Establish a pane with pushed content from chat/session A
- [ ] Navigate/push additional content so chat/session A's item is present in pane history rather than only current view
- [ ] From the same chat/session A, push a new item into the same pane
- [ ] Verify one of the two allowed outcomes occurs:
  - [ ] Existing history item from chat/session A is moved to the front/current position and displayed, with history still coherent
  - [ ] New content from chat/session A is displayed and chat/session A's old content is removed from history
- [ ] Verify forbidden outcome does not occur: old content from chat/session A remains buried in history while new content from the same chat/session is also added/displayed, creating duplicate/stale provenance entries
- [ ] Repeat with a different chat/session B to prove provenance scoping is per chat/session, not global
- [ ] Repeat after reconnect/restart so persisted history obeys the same replacement/fronting rule
- **Result:**
- **Notes:**

---


## Phase 2.6 — Capture-backed push/topology truth oracle

- [ ] Started from one known pane on the primary admitted capture-capable surface
- [ ] Additional surfaces included only after independent admission
- [ ] Split to two panes
- [ ] Recorded post-split provider topology for both panes: `surfaceId`, `windowLabel`, `paneId`, `paneLabel`, `topologyRevision`, provider/remote pane identity if available, viewport/dimensions
- [ ] Pushed typed markdown into first/left pane by exact `surfaceId` and numeric `paneId`, with unique marker
- [ ] Pushed a second typed-markdown visual oracle into second/right pane by exact `surfaceId` and numeric `paneId`, with unique marker
- [ ] Recorded each push result: `contentId`, `operationReceipt`, `paneId`, `paneLabel`, correlation id, revision, apply evidence
- [ ] Re-read provider/list state and confirmed each pushed content item is associated with the intended pane identity
- [ ] Captured first/left pane by the same exact `surfaceId` + `paneId` used for its push
- [ ] Captured second/right pane by the same exact `surfaceId` + `paneId` used for its push
- [ ] First pane capture pixels contain first pane marker
- [ ] Second pane capture pixels contain second pane marker
- [ ] First pane capture contains no occurrence of the second pane marker
- [ ] Second pane capture contains no occurrence of the first pane marker
- [ ] Capture metadata matches intended pushed pane tuple and topology revision
- [ ] `surf-ace capture-pane` visible text, `contentSnapshot`, provider `visibleContentId`, push `contentId`, and captured pixels agree for both panes
- [ ] 2-minute idle repeat list/read/capture proves each pushed marker in its intended pane and zero occurrences of the sibling marker
- [ ] Restart/relaunch repeat list/read/capture proves each pushed marker in its intended pane and zero occurrences of the sibling marker when restart is in scope
- [ ] Any capture failure records metadata and `failureReason`; visible-truth confidence marked Yellow at best if capture cannot prove push placement
- **Result:**
- **Artifacts:**
- **Notes:**


## Phase 3 — Idle soak

Precondition for this phase:
- [ ] Primary admitted surface left in an intentional multi-pane layout
- [ ] Simulator left in an intentional multi-pane layout if admitted and included
- [ ] Aleph left in an intentional multi-pane layout if admitted and included
- [ ] Racter left in an intentional multi-pane layout if admitted and included
- [ ] all Cyberbrain Surf Ace windows/panes admitted to the run left in an intentional multi-pane/window layout if included
- [ ] all eezo Surf Ace windows/panes admitted to the run left in an intentional 2-pane layout if included
- [ ] Explicit content pushed into every pane on each included surface/window
- [ ] Expected pane identities/count recorded for each included surface/window
- [ ] Pane-to-content mapping recorded for each included surface/window
- [ ] Intended surviving pane(s) after post-soak collapse recorded

### 5-minute checkpoint
- [ ] Simulator healthy if admitted and included; otherwise `Out-of-scope`
- [ ] Aleph healthy if admitted and included; otherwise `Out-of-scope`
- [ ] Racter healthy if admitted and included; otherwise `Out-of-scope`
- [ ] all Cyberbrain Surf Ace windows/panes admitted to the run healthy / noted if not included
- [ ] all eezo Surf Ace windows/panes admitted to the run healthy / noted if not included
- [ ] Expected multi-pane layout still listed on every included surface/window
- [ ] Expected pushed content still present in every pane on every included surface/window
- [ ] Unique marker pushed to each admitted pane and verified with `surf-ace capture-pane` against the explicit `surfaceId` + `paneId`
- [ ] Pane-capture metadata matches provider topology: `windowLabel`, `paneLabel`, `topologyRevision`, visible content id, dimensions, scale, timestamp
- [ ] Each admitted and included Cyberbrain window/pane still shows known content/topology state; otherwise `Out-of-scope`
- [ ] Each admitted and included eezo window/pane still shows known 2-pane content state; otherwise `Out-of-scope`
- [ ] `wsOpen=true` on every included surface/window
- [ ] Harmless mutability/readback still succeeds on every included surface/window
- [ ] No topology drift
- [ ] No content drift
- [ ] Any `snapshot.get` timeout marked stale/retried without socket teardown, session churn, ownership churn, content loss, topology collapse, or reconnect storm
- [ ] No bogus busy lock
- [ ] No reconnect storm or session-id churn noted
- **Notes:**

### 15-minute checkpoint
- [ ] Simulator healthy if admitted and included; otherwise `Out-of-scope`
- [ ] Aleph healthy if admitted and included; otherwise `Out-of-scope`
- [ ] Racter healthy if admitted and included; otherwise `Out-of-scope`
- [ ] all Cyberbrain Surf Ace windows/panes admitted to the run healthy / noted if not included
- [ ] all eezo Surf Ace windows/panes admitted to the run healthy / noted if not included
- [ ] Expected multi-pane layout still listed on every included surface/window
- [ ] Expected pushed content still present in every pane on every included surface/window
- [ ] Each admitted and included Cyberbrain window/pane still shows known content/topology state; otherwise `Out-of-scope`
- [ ] Each admitted and included eezo window/pane still shows known 2-pane content state; otherwise `Out-of-scope`
- [ ] `wsOpen=true` on every included surface/window
- [ ] Harmless mutability/readback still succeeds on every included surface/window
- [ ] No topology drift
- [ ] No content drift
- [ ] Any `snapshot.get` timeout marked stale/retried without socket teardown, session churn, ownership churn, content loss, topology collapse, or reconnect storm
- [ ] No bogus busy lock
- [ ] No reconnect storm or session-id churn noted
- **Notes:**

### 30-minute checkpoint
- [ ] Simulator healthy if admitted and included; otherwise `Out-of-scope`
- [ ] Aleph healthy if admitted and included; otherwise `Out-of-scope`
- [ ] Racter healthy if admitted and included; otherwise `Out-of-scope`
- [ ] all Cyberbrain Surf Ace windows/panes admitted to the run healthy / noted if not included
- [ ] all eezo Surf Ace windows/panes admitted to the run healthy / noted if not included
- [ ] Expected multi-pane layout still listed on every included surface/window
- [ ] Expected pushed content still present in every pane on every included surface/window
- [ ] Each admitted and included Cyberbrain window/pane still shows known content/topology state; otherwise `Out-of-scope`
- [ ] Each admitted and included eezo window/pane still shows known 2-pane content state; otherwise `Out-of-scope`
- [ ] `wsOpen=true` on every included surface/window
- [ ] Harmless mutability/readback still succeeds on every included surface/window
- [ ] No topology drift
- [ ] No content drift
- [ ] Any `snapshot.get` timeout marked stale/retried without socket teardown, session churn, ownership churn, content loss, topology collapse, or reconnect storm
- [ ] No bogus busy lock
- [ ] No reconnect storm or session-id churn noted
- **Notes:**

## Phase 3 result
- [ ] Idle soak passed
- [ ] No unexplained disconnects during dwell
- [ ] No topology drift during dwell
- [ ] No intentionally-created panes disappeared during dwell
- [ ] Expected pushed content remained correct in every tracked pane during dwell
- [ ] Each admitted and included Cyberbrain window/pane stayed listed, `wsOpen=true`, mutable/readable, and free of reconnect/session churn; otherwise `Out-of-scope`
- [ ] Each admitted and included eezo window/pane stayed listed, `wsOpen=true`, mutable/readable, and free of reconnect/session churn; otherwise `Out-of-scope`
- [ ] Post-soak collapse/close restored the intended surviving topology on every included surface
- [ ] No silent content corruption during dwell
- [ ] Snapshot-timeout mitigation passed: stale/retry only, no destabilizing reconnect/session/topology/content side effects
- **Result:**
- **Notes:**

---

## Phase 4 — Failure injection and recovery

After each restart, relaunch, bounce, interruption, or handoff, re-run discovery. Reuse admission only when the exact surface/controller-fixture binding is unchanged and the admission row explicitly covers that boundary. Otherwise, re-admit the candidate before read, capture, push, topology, or another target operation.

A fresh fixture is always a new admission boundary. Run fresh discovery and create a new passing admission-table row for every target surface before read, capture, push, topology, or another target operation. Do not reuse the failed fixture's row even if the `surfaceId` repeats.

### Required bounded restart/recovery cycle

- [ ] One primary admitted surface selected
- [ ] Known-good multi-pane/content baseline recorded before restart
- [ ] One separately authorized restart or relaunch performed on that surface
- [ ] Disappearance and reappearance recorded
- [ ] Fresh discovery confirms the same expected surface identity or records an explicit identity transition
- [ ] Exact surface/controller-fixture binding and admission validity rechecked after restart
- [ ] Changed binding or evidence that does not cover restart caused re-admission before read/capture
- [ ] Read and capture prove restored topology/content without manual repopulation
- [ ] 5-minute post-recovery idle passed
- [ ] No additional surface was targeted without independent admission
- **Result:**
- **Artifacts:**
- **Notes:**

### Gateway restart
- [ ] Scenario is separately authorized and relevant; otherwise marked `Out-of-scope`
- [ ] Known-good baseline established first
- [ ] Gateway/provider restarted
- [ ] Surfaces rediscovered afterward
- [ ] Session sanity restored
- [ ] Topology truth restored
- [ ] Visible truth restored where observable
- [ ] 5-minute post-recovery idle passed
- **Result:**
- **Notes:**

### Surface restart — Simulator
- [ ] Simulator is the primary admitted surface or has independent optional-surface admission; otherwise marked `Out-of-scope`
- [ ] Known-good baseline established
- [ ] Surface stopped
- [ ] Disappearance observed
- [ ] Relaunch observed
- [ ] Restored controller association verified through fresh CLI evidence
- [ ] Truth restored after recovery
- [ ] 5-minute post-recovery idle passed
- **Result:**
- **Notes:**

### Surface restart — Aleph
- [ ] Aleph is the primary admitted surface or has independent optional-surface admission; otherwise marked `Out-of-scope`
- [ ] Known-good baseline established
- [ ] Surface stopped
- [ ] Disappearance observed
- [ ] Relaunch observed
- [ ] Restored controller association verified through fresh CLI evidence
- [ ] Truth restored after recovery
- [ ] 5-minute post-recovery idle passed
- **Result:**
- **Notes:**

### Surface restart — each Cyberbrain Surf Ace window/pane admitted to the run
- [ ] Each targeted Cyberbrain surface has independent admission evidence; otherwise marked `Out-of-scope`
- [ ] Known-good baseline established
- [ ] Surface/window stopped or closed
- [ ] Disappearance/removal observed
- [ ] Relaunch/recreate observed
- [ ] Restored controller association verified through fresh CLI evidence
- [ ] Truth restored or stale state tombstoned after recovery
- [ ] 5-minute post-recovery idle passed
- **Result:**
- **Notes:**

### Surface restart — Racter
- [ ] Racter is the primary admitted surface or has independent optional-surface admission; otherwise marked `Out-of-scope`
- [ ] Known-good baseline established
- [ ] Surface stopped
- [ ] Disappearance observed
- [ ] Relaunch observed
- [ ] Restored controller association verified through fresh CLI evidence
- [ ] Truth restored after recovery
- [ ] 5-minute post-recovery idle passed
- **Result:**
- **Notes:**

### Surface restart — each eezo Surf Ace window/pane admitted to the run
- [ ] Each targeted eezo surface has independent admission evidence; otherwise marked `Out-of-scope`
- [ ] Known-good baseline established
- [ ] Surface stopped
- [ ] Disappearance observed
- [ ] Relaunch observed
- [ ] Restored controller association verified through fresh CLI evidence
- [ ] Truth restored after recovery
- [ ] 5-minute post-recovery idle passed
- **Result:**
- **Notes:**

### Surface restart — Ansible when admitted
- [ ] Ansible is the primary admitted surface or has independent optional-surface admission; otherwise marked `Out-of-scope`
- [ ] Known-good baseline established
- [ ] Surface stopped
- [ ] Disappearance observed
- [ ] Relaunch observed
- [ ] Restored controller association verified through fresh CLI evidence
- [ ] Truth restored after recovery
- [ ] 5-minute post-recovery idle passed
- **Result:**
- **Notes:**

### Network interruption
- [ ] Scenario is separately authorized and relevant; otherwise marked `Out-of-scope`
- [ ] Pre-interruption state recorded
- [ ] Temporary interruption induced
- [ ] Connectivity restored
- [ ] Discovery recovered
- [ ] Session behavior sane
- [ ] No permanent busy/ownership wedge
- **Result:**
- **Notes:**

### Ownership handoff
- [ ] Scenario is separately authorized and relevant; otherwise marked `Out-of-scope`
- [ ] Approved controller association established from session A
- [ ] Association relinquished or replaced through the approved run orchestration path
- [ ] Approved controller association established from session B
- [ ] No orphaned busy state
- [ ] Truth remained sane during handoff
- **Result:**
- **Notes:**

---

## Phase 5 — Longitudinal drift audit

- [ ] Run on the primary admitted surface
- [ ] Established 2-pane `A/B` baseline
- [ ] 10-minute idle passed
- [ ] Truth verified
- [ ] Performed one structural mutation
- [ ] Another 10-minute idle passed
- [ ] Truth verified again
- [ ] Restarted gateway or surface
- [ ] Post-restart discovery and admission validity rechecked before restored-state target operations
- [ ] Restored known state
- [ ] Final 10-minute idle passed
- [ ] Final truth verification passed
- [ ] No realized-vs-visible mismatch observed
- **Result:**
- **Notes:**

---

## Failures captured

For each failure, record:

- **Timestamp:**
- **Surface:**
- **Expected state:**
- **Provider truth:**
- **Visible truth:**
- **Discovery state:**
- **Busy / ownership state:**
- **Immediate precursor event:**
- **Manual intervention required?:**
- **Artifact links:**

### Failure 1
-

### Failure 2
-

### Failure 3
-

---

## Final judgment

### Surface/window grading
- **Primary admitted surface:**
  - [ ] Green
  - [ ] Yellow
  - [ ] Red
- **Primary admission evidence:**
- **Simulator:**
  - [ ] Green
  - [ ] Yellow
  - [ ] Red
  - [ ] Out-of-scope
- **Aleph:**
  - [ ] Green
  - [ ] Yellow
  - [ ] Red
  - [ ] Out-of-scope
- **Racter:**
  - [ ] Green
  - [ ] Yellow
  - [ ] Red
  - [ ] Out-of-scope
- **Each Cyberbrain Surf Ace window/pane admitted to the run:**
  - [ ] Independently listed in notes
  - [ ] Green / Yellow / Red per window/pane
- **Each eezo Surf Ace window/pane admitted to the run:**
  - [ ] Independently listed in notes
  - [ ] Green / Yellow / Red per window/pane

### Admission and scope judgment

- [ ] `surf-ace list` was used only for discovery and current topology
- [ ] Each targeted surface had independent admission evidence before targeting
- [ ] Each admission row records and passes every already-lockless schema/verifier field or every explicit-migration authority/material/scope/input field, including exact controller-fixture identity, expiry, cleanup, covered operations, and restart/recovery validity
- [ ] Each target operation has a recorded immediately-prior check that its admission row was unexpired and covered the exact surface/controller fixture, current boundary, and operation
- [ ] Required multi-pane proof ran inside one admitted surface
- [ ] Each additional surface was optional and independently admitted
- [ ] No migration material was invented, derived, broadened, or reused
- [ ] No `pair.request` `capability_mismatch` was retried or bypassed
- [ ] Any `capability_mismatch` stopped before mutation, produced endpoint/procedure-readiness classification, cleanup, and a fresh-fixture route
- [ ] Any resumed fresh-fixture run performed fresh discovery and created a new passing admission row for every target surface before any target operation
- [ ] Any changed post-restart binding was re-admitted before the next target operation

### Release judgment
- [ ] Ready
- [ ] Changed but unverified
- [ ] Not ready

### Why

### Next required action

### Open questions
