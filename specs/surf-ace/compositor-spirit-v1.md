# Surf Ace compositor spirit v1

Status: Product-owner spirit; T316 is ready for technical specification. T368 was amended after Mike's 2026-09-01 pane-visibility clarification.

Product owner: `product-owner:surf-ace-compositor`, under `product-owner:surf-ace-codex`.

Durable provenance:

- Takeover work item: `wi_e9e77bce-0b2c-4215-9f98-c209f6838726`.
- CLU learning pass: `att_1c4e42d3-8a15-4706-afa1-65c0c683e7d5`.
- Custody transfer: `att_eebb54ba-38f9-4024-9db0-b0006a8fc3be`.
- Product digest: `att_fa0c028d-1985-4ebb-a025-e0a6eca87b1b`.
- T316 focus ruling: `dr_595d4764-a089-4345-8167-6b3df807f5f2`, ruled `cancel-return-surf-ace`.
- T368 window-group ruling: `dr_eddcae41-3f78-4d3a-aa19-7be09abe6d47`, amended by Mike's 2026-09-01 clarification that focus-gated hiding is not surface disappearance.
- T285 diagnostic-logging ruling: `dr_ed029673-79ef-4564-838f-a3c1d33c8ae3`, ruled with the systemd user-unit and persistent-journal pattern relayed by Mike on 2026-09-03.

## Spirit

Surf Ace clients own the durable truth: pane identity, topology, resolved geometry, content mode, visible history, provenance, and operation ordering. The compositor must not reinterpret that truth or reconstruct missing controller intent.

The compositor makes that truth physically real on supported Linux appliances. It owns output and render-device selection, connector rebinding, presentation generations, rotation, native-process hosting, physical focus, input routing, and capture. It is a kiosk appliance component, not a desktop environment.

Native-child diagnostics are durable appliance evidence, not terminal output. On supported systemd appliances, the compositor's child-launch path spawns each child as a transient systemd user unit named `surfaceN-<child>` through `systemd-run --user`; no child relies on file-descriptor inheritance from a terminal. Child output goes to the host's persistent systemd journal and remains recoverable after compositor and child restart through `journalctl --user -u <unit>`. The child-launch wrapper strips token- and credential-shaped values before any line reaches the journal. Journald supplies rotation and retains at most 14 days or 200 MB, whichever limit is reached first; the compositor adds no rotation mechanism. This contract assumes that the target appliance supports systemd. A target outside that envelope requires a new explicit product ruling for a log-directory pattern, storage, and rotation.

One coherent presentation generation must govern pixels, damage, native surfaces, pane viewports, input transforms, capture, and published status. The compositor may reject unsafe or ambiguous realization. It must not show plausible mixed state or report health for a presentation that did not commit.

Physical focus is ephemeral device-local state. Surf Ace selection remains client-owned durable state. The compositor routes physical events only among surfaces that realize the currently presented generation. It rejects stale identity and generation requests; it never retargets them by label, selection, proximity, or current topology.

Pane focus and surface focus are separate. Pane focus selects the one pane whose native window group may receive keyboard input and show accessories. Surface focus selects the recipient inside that pane group or Surf Ace. Returning focus to Surf Ace changes the surface-level recipient without erasing the focused-pane invariant.

If focused or pointer-grabbed native content disappears, the compositor cancels the active interaction, records a durable diagnostic, and returns subsequent focus and input to Surf Ace. It never redirects that interaction to another pane or application.

Focus-gated hiding is a different state transition. When a pane loses focus, its accessory windows become hidden but continue to exist. Their group identity, position, size, z-order, application state, and restoration state remain intact. Refocusing the owning pane restores every still-existing hidden window. Blur-hiding must not cancel the interaction as if content disappeared, invoke the `cancel-return-surf-ace` fallback, close a window, or discard application state. If the app genuinely destroys a window while it is hidden, the compositor records the real lifecycle change and does not synthesize a restoration.

## Success outcomes

- The screen, native applications, capture, input, and status describe one actually presented generation.
- Ordinary unambiguous connector changes recover automatically.
- Ambiguous output, identity, generation, or input state fails closed with explicit and recoverable status.
- Supported Racter and Shrdlu devices, connectors, rotations, and normal connector moves work correctly.
- Operators can identify the selected backend, devices, connector, mode, rotation, generation, native-child lifecycle, capture generation, and recovery state from durable evidence.

## Quality stances

- High: correctness, performance, interaction quality, reliability, security, maintainability, safety, and observability.
- Medium: compatibility outside the declared supported-appliance envelope.
- Low: portability beyond Linux, Wayland, Smithay, and the declared appliance hardware.

Low portability does not weaken support for Racter or Shrdlu. It rejects cross-platform and general-desktop ambitions.

## Product non-goals

- Multi-monitor desktop management.
- General window-manager semantics, global task switching, or independent workspace identity.
- Pane-rectangle clipping or drag clamping as the containment mechanism for native accessory windows.
- Treating focus-gated visibility changes as native surface destruction or application lifecycle events.
- Compositor ownership of pane topology, pane meaning, or operation ordering.
- Cross-platform compositor abstraction.
- General Xwayland or arbitrary-application compatibility.
- Resolving the deferred MS14 multi-screen policy choices through implementation accident.

## T316: one presentation transaction

Work item: `wi_b7b2e47d-e63a-4d7d-accf-d9c11871313b`.

### Outcome

After a scale, rotation, mode, or output-path change, the user must never see one geometry while clicking another, capture old pixels under new coordinates, or receive healthy status for a presentation that did not commit.

### Seven consumers

1. Root and output layout geometry.
2. Composited Surf Ace content geometry and clipping.
3. Native-surface materialization geometry.
4. Pane viewport projections.
5. Screen and pane capture geometry and frame state.
6. Physical input transforms and hit-testing.
7. Published status and control-plane geometry.

### Acceptance boundary

- Prepare every affected consumer for one candidate generation.
- Activate all consumers only at the actual presentation boundary.
- Bind activation to the exact KMS completion, including cross-device reclaim.
- On failure, preserve or restore the prior coherent generation and report the failure truthfully.
- Preserve FIFO response ordering across the commit boundary.
- Exercise production ownership and renderer/import paths in tests; helper-only lookalikes are not proof.
- Prove fractional native material, import, clip, damage, and rotation with real pixel evidence.
- Apply the ruled cancellation behavior only when a native surface genuinely disappears. A focus-gated hide is not disappearance and must preserve the surface for intact restoration.

### Mechanism stance

No current Rust mechanism is sacred. Existing staging helpers, geometry authorities, queues, and transaction wrappers may be replaced or deleted. Duplicate helper-only state should not exist. The single-generation guarantee is the product requirement.

The preserved candidate `e5a1f03adf01e9639acf94a9f2fae0b599bf9cea` is evidence, not an approved solution. Reviews 2 through 19 remain `CHANGES_REQUIRED`. Zero-byte review files are not approvals.

### Open product questions

None for this slice. Technical specification must preserve the deferred MS14 exclusions and the acceptance boundary above.

## Other active slices

- T1408: representative continuous pointer drawing on Racter requires Mike's human acceptance plus at least 50 presented frames per second in every one-second bucket of a recorded 60-second run. The retained approximately 39 fps result is adverse evidence, not a floor. Exact runtime revisions, native display mode, workload, capture, and measurement method must travel with the result.
- T285: child diagnostics must remain available outside terminal scrollback and across restart. The compositor's own child-launch path is authoritative. It uses transient systemd user units named `surfaceN-<child>`, persistent host journald storage under `/var/log/journal`, lookup through `journalctl --user -u <unit>`, journald retention capped at 14 days or 200 MB, and pre-journal stripping of token- and credential-shaped values. No bespoke rotation or terminal file-descriptor inheritance is allowed. This slice applies only to supported systemd appliances; another platform requires a new logging-pattern ruling.
- T359: deployment configuration owns appliance node identity, coordinates, timezone, and schedule input. No authoritative deployed values currently exist on Racter or Shrdlu; compiled examples are not deployment truth.
- T368: native child and dialog surfaces remain pane-owned physical families, but they may float outside their pane, over other panes, and over Surf Ace chrome. Focus-gated visibility is the containment mechanism: exactly one pane has keyboard focus; Surf Ace visibly and unambiguously identifies it even under accessory overlap; only that pane's accessory windows are visible. Primary pane content remains visible when its pane is unfocused. A visible overflow accessory wins hit-testing over the pane beneath it; an exposed pane region or explicit Surf Ace focus affordance changes pane focus. Blurring a pane hides its accessories without destroying them, and refocusing restores every still-existing accessory at its prior position, size, z-order, and application state. An accessory genuinely destroyed while hidden remains destroyed and is reported as such. Genuine disappearance during an active interaction remains the separate `cancel-return-surf-ace` case. Explicit pane target restore is not blur, and the first slice does not promise child-window persistence across it. Existing clipping, edge-clamping, and pane-containment proofs are invalid for this boundary. Shrdlu is a normal stopped deployment, not a recovery defect.
