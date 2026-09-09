# Surf Ace full-soak platform contract — V4.2

Authority: Mike's direct all-supported-platform requirement and topology
clarification, 2026-09-09. Canonical home: this file in
`clickety-clacks/tightbeam-specs`, on `main`.

Follow-through authority, same date: Mike authorizes the full all-platform
soak and explicitly permits iPad simulators when physical iPad hardware is
unavailable. Routine reversible test setup is authorized; lack of a separate
older setup approval is not an execution blocker. Unrelated release,
installation, deployment, and host service/security changes remain outside
this request.

## Acceptance rule

A **FULL soak PASS** requires executed, independently reviewed evidence for
every supported client platform, every supported server platform, and their
interoperability through the shared network-wide controller. One primary
client with all other platforms optional is not a FULL soak.

This rule supersedes the platform-optional acceptance clauses in V4 and V4.1,
including frozen copies of those bundles. Their admission safeguards and
per-platform functional phases still apply. A primary surface is a phase
execution unit, not a substitute for the complete platform matrix.

Label useful narrower runs **PARTIAL — <exact tested scope>**. A partial run
may pass its own checks. It cannot pass full-soak acceptance. Missing,
unexecuted, blocked, failed, ungraded, or unreviewed required coverage leaves
the full soak **INCOMPLETE** (and records any product failures separately).
Do not mark a supported platform optional or out-of-scope because its host,
build, implementation, permission, package, or execution owner is missing.

## Product topology and ownership

Use one network-wide Surf Ace controller, with the CLI on its host, and a
Surf Ace client on each display machine. The controller owns fleet topology
and globally unique window labels. Pane addresses combine the window label
with the pane's window-local label; a pane ID is not its visible label.
Clients register stable client/surface identities with the controller and
retain content, history, and assigned identity across the tested recovery.

Clients try their configured controller first, then Bonjour server discovery
when absent or failed, and recover the configured route when it returns.
OpenClaw is an example consumer/integration, not a required runtime dependency.
Do not require a separate resident controller on each display machine.
For server-platform trials, move between explicitly recorded isolated
controller fixtures; never create competing authorities for one fleet.

Surf Ace Compositor can sit beneath a client where that integration is needed.
It remains compositor-owned. Generic client coverage does not acquire a
custom-compositor dependency. A supported compositor-backed configuration
needs its own declared coverage and owner; it does not replace client or
server platform evidence. This contract changes acceptance/documentation,
not source ownership, installation, deployment, release, or host policy.

## Support ledger: derive the matrix, do not infer it from hosts

Pin the product source revision and its support contract before grading.
Record role, OS, supported architecture/version/form factor, package hash,
support citation, execution owner, and evidence for every required row.
Split a row whenever the support contract distinguishes runtime variants.
An architecture, device, or server role cannot inherit a result merely
because another one uses the same source or host.

The baseline below pins `clickety-clacks/surf-ace` at
`cd4004c9376e465f27ffc2e6fe2954e2e5975280`. It does not declare new support
or silently remove an existing advertised platform.

| Role | Platform to account for | Product basis | Acceptance treatment |
| --- | --- | --- | --- |
| Client | Linux Electron | `README.md` package table; `DESIGN.md` Purpose | Required |
| Client | macOS Electron | Same declarations | Required |
| Client | Windows Electron | Same declarations | Required; Linux/macOS cannot substitute |
| Client | iOS (phone) | Same declarations; `packages/ios/README.md` | Required |
| Client | iPadOS (tablet) | Same declarations; `packages/ios/README.md` | Required separately from phone |
| Client | visionOS / SurfAceSpatial | `packages/ios/README.md` names the native target and shared runtime; V4.1 fleet includes Cyberbrain | Account as required while advertised; a simulator build alone is not native executed soak evidence |
| Server/controller + host CLI | Linux x86_64 | `surf-ace-release-split-r5.md`, Release files, names the Linux x86_64 resident controller/CLI; controller README names Linux integration infrastructure; Racter exact-source/runtime prerequisite `att_88bcb837` | Required server row; execute the actual packaged central server and matching host CLI, not allocator-only helper proof |
| Server/controller + host CLI | macOS arm64 | Accepted packaged central-server and combined-soak evidence on Eezo, including `art_2dc36698`, `art_7988dea4`; controller README names macOS infrastructure | Required server row; client-on-macOS does not prove this role |

Source links for audit:

- [Product README](https://github.com/clickety-clacks/surf-ace/blob/cd4004c9376e465f27ffc2e6fe2954e2e5975280/README.md)
- [Product design](https://github.com/clickety-clacks/surf-ace/blob/cd4004c9376e465f27ffc2e6fe2954e2e5975280/DESIGN.md)
- [Apple client contract](https://github.com/clickety-clacks/surf-ace/blob/cd4004c9376e465f27ffc2e6fe2954e2e5975280/packages/ios/README.md)
- [Controller README](https://github.com/clickety-clacks/surf-ace/blob/cd4004c9376e465f27ffc2e6fe2954e2e5975280/packages/controller/README.md)
- [Proposed release artifact list](surf-ace-release-split-r5.md)

Do not use that narrower proposed release artifact list to drop Windows,
Apple mobile clients, visionOS, or a currently supported server variant.
Do not infer runtime support from Node/Electron portability or a directory.
For this pinned build, the required server matrix is Linux x86_64 and macOS
arm64, as declared/built above. The cited contract and supported-build record
do not establish a Windows server or another required server OS/architecture.
Do not create an unknown-platform row or require open-ended support discovery
before execution or acceptance. This is not a claim that other systems cannot
run the code, and it does not waive a platform actually declared supported.
Add a server row only when a concrete support declaration or supported-build
record establishes it; cite that evidence and route the uncovered execution.
Record exact OS/runtime versions actually tested without inventing requirements
for every hypothetical version. Never pause already-known rows for that search.
A support withdrawal requires explicit product authority, not a test waiver.

## Required execution and interoperability

1. Freeze the client/server/CLI build matrix and enumerate all required
   client-platform by server-platform combinations. Record compatibility
   for the exact packages. Mixed unreviewed revisions do not form a pass.
2. Execute the existing full functional sequence on each supported client:
   registration, configured route and Bonjour fallback, recovery, multi-pane
   distinct content, supported Back/Forward actions, current/no-loss reads,
   decoded pane pixels, topology churn, dwell, and restart/recovery.
   Preserve V4.1 timed phases (2/5/15/30-minute checkpoints, 60-minute churn
   dwell, longitudinal checks) rather than replace them with build tests.
3. Execute packaged controller and host CLI startup, registration/control,
   persistent allocation/topology, dwell, reconnect, and controller restart
   recovery on each supported server platform. Keep custody storage and
   client processes separately identified. A database or client host is not
   server execution evidence; a server host is not client execution evidence.
4. For each supported server platform, connect the supported client platforms
   through that one shared controller. Execute every matrix pairing. Prove
   cross-client addressing, distinct fleet window labels, unambiguous pane
   addresses, targeted content isolation, combined topology/readback, and
   reconnect identity continuity with multiple clients active together.
   Independent single-client runs alone cannot establish interoperability.
5. Record native device versus simulator/emulator. For iPadOS, when physical
   iPad hardware is unavailable, Mike explicitly authorizes an iPad simulator
   to satisfy this soak's iPad platform row: execute the full required sequence
   and interoperability, recording model, OS runtime, build/hash, commands,
   hardware-unavailability basis, and simulator limitations. A build alone
   never satisfies the row. This exception does not assert physical-device
   coverage or automatically waive native iPhone or visionOS requirements.
   Keep other simulator results partial for a native-device requirement unless
   the applicable support contract or explicit authority allows substitution.
   Use product pane capture/read
   and decoded pixels as authorized by Mike's 2026-09-08 ruling. Unrelated
   desktop overlays and Screen Recording permission are not prerequisites
   for direct capture. Never relabel direct capture as visible-screen proof.
6. Seal logs, timestamps, manifests, actual commands, expected/observed
   outcomes, platform/runtime identities, controller/client identities,
   labels, cleanup, and all failures. Independent review checks the complete
   coverage ledger, not merely a selected successful report.

## Checklist and reporting criteria

Use this ledger in addition to the phase checklist; expand every required
platform/architecture row and every client-by-server pairing before execution.

| Role or pairing | Support contract/ref | OS/arch/device/runtime | Source/package/CLI hashes | Host + existing owner/card | Executed phases + evidence | Result / missing work |
| --- | --- | --- | --- | --- | --- | --- |
| One row per required client | | | | | | |
| One row per required server + host CLI | | | | | | |
| One row per required client x server pairing | | | | | | |

Required final checks:

- [ ] The role-specific support set is complete, pinned, and owner-confirmed.
- [ ] Every supported client and server row has executed phase evidence.
- [ ] Every supported client/server pairing has shared-controller evidence.
- [ ] All required checks pass and the complete evidence has independent review.
- [ ] Missing/unexecuted coverage is listed with exact blocker and existing owner.
- [ ] Historical evidence retains its source, platform, timing, and limitations.
- [ ] No partial run, build, package check, or available-host subset is called FULL.

Report two separate fields: **Executed-scope result** (pass/fail/ungraded)
and **Full-soak acceptance** (PASS/INCOMPLETE). State exact tested client
platforms, server platforms, pairings, revisions, and missing rows in the
summary. Use FULL PASS only when every required check above is satisfied.
This is not release/install approval.

## Pending acceptance and preserved historical evidence — 2026-09-09

Existing coordination remains `asg_4ea30f60` on work item
`wi_ef5e9b29-d440-4c39-b01b-58600569109b`, held by the Surf Ace CLIENT owner.
Execution coordination remains with `operator:surf-ace-endurance`; do not
reopen closed runs or create duplicate servers. The last read of the
endurance and Plumbus holders showed no open execution assignments. Thus
missing-platform execution is **unassigned**, not silently in progress.
Route those gaps through this existing ownership after reconciling current
cards and venue authority. This documentation correction launches nothing.

Follow-through checkpoint: Mike subsequently authorized execution on the
same work item. Sole coordinator `operator:surf-ace-endurance` now holds
`asg_f8fea8f2-6cfa-48b1-a3c9-632c25285958`. Reconcile and select existing
capable operators, preserve useful accepted evidence, and execute uncovered
rows without duplicate controllers or runs. The earlier unassigned statement
records the preceding checkpoint, not a continuing hold. File the actual
selected hardware/simulators, candidate hashes, failed operations and
alternatives, first execution, and material results in Tightbeam.

| Existing evidence | Actual scope preserved | Full-matrix gap |
| --- | --- | --- |
| Linux17 + native macOS18, `art_7988dea4`, clean `att_c4fece8c`, completed `asg_1db43c16` | cd4004c Linux/macOS client direct soak, 662 hashes and 77 capture/read checks; stated screen/chronology/recovery limits retained | Not Windows/iOS/iPadOS/visionOS client proof; not complete server-platform/interoperability matrix |
| Plumbus run03, `art_96430efc`, clean `att_63cfe9d3`, completed `asg_9a5cb445` | Additional Linux client, 21 capture/read checks, stated timing/input/recovery limits retained | Another Linux host is not another OS platform |
| Eezo central fixture `asg_0ed9349e`, cleanup `art_3dc545ba` | Packaged macOS central fixture used by the recorded client runs; now stopped and cleaned | No current endpoint; not Linux server or all supported server variants; exact host-CLI/recovery/pairing coverage still requires ledger review |

Missing evidence at this checkpoint: Windows, iOS, iPadOS, and visionOS
client full sequences; Linux controller/host-CLI full sequence; remaining
macOS controller recovery/host-CLI obligations; and all required client/server
interoperability pairings. The finite server matrix above replaces the earlier
open-ended server-support-enumeration prerequisite under Mike's clarification.
Linux/macOS historical client passes remain valid for their recorded scope,
but are not retroactively widened or sufficient for the pending FULL pass.
Fresh or reused evidence must identify the exact supported build and prove
each required row; reuse is an evidence review, never an invented execution.

Do not rewrite old receipts, re-label old failures as passes, or claim this
new acceptance rule governed their original execution. Preserve old results
and append this scope qualification in every current summary that cites them.
