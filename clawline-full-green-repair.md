# Clawline Full-Green Repair

Status: READY FOR INDEPENDENT SPEC REVIEW.

Authority:

- Canonical spec: `clickety-clacks/tightbeam-specs/clawline-full-green-repair.md`.
- Outcome work item: `wi_81b3c5ac-de4b-4613-b146-c83d863a9b7d`.
- Canonical target: Clawline `bbb6de019bed4ec511c0bd4b6463073831ea2107`.
- Reviewed base: `8ea6331823d7214640ee21301f68ab5da02e00d1`.
- Integration blocker: `att_b40b02ef-b565-4246-9d0f-1012c5fbbe4b` and
  `art_7e55ac1a` at SHA-256
  `ecfb52207de241c9445f050d2089fa0dc73458383ae3709654520344b80b89bb`.
- Historical baseline: `wi_b314b4db-dbbb-44ff-95f7-e636aad36a54`,
  `asg_3642a044-ca5d-46ec-a873-336897783340`, and `art_95cc63a9` at
  SHA-256 `62a4689674483ef88e86a7b34c4c6d0641e0b3f69451c8ff55f2593787e17931`.
- Causal evidence: `wi_b39f7971-edea-4924-bbf2-c6d200cf1908` and
  completed replacement assignment
  `asg_055de05e-d64f-4002-b3f8-a497fe387ed6`, verdict
  `att_d5b72926-9b08-4e05-b20a-58008823dbd2`, and report
  `art_9ae54cbe` at SHA-256
  `bb0be87c50988451148415f61eca661459ec7448cb9987867fde47c3c841b4da`.
  Predecessor `asg_2aff86d8-427a-40d6-96b3-7b2382d54352` was revoked after a
  substrate failure. Its partial log, result bundle, and recovery reports are
  not a causal verdict and do not authorize a repair.
- Workflow: Mike's 2026-08-25 standing rule: SPEC → independent SPEC REVIEW
  → CODE → independent CODE REVIEW → iterate to reviewed-clean → integrate on
  a full green gate. An author does not review their own work.

## Goal

Restore the Clawline gate on canonical target `bbb6de019bed4ec511c0bd4b6463073831ea2107`.
The accepted result contains exactly 1,042 passing unit tests and exactly five
passing tests in the `ClawlineUITests` class. The complete UI target, including
all 15 `T1150NotificationDockUITests`, has zero failures.

The repair keeps the reviewed tool-call activity pill behavior. The repair
does not roll back either commit in the reviewed range from `8ea63318` to
`bbb6de01`.

## Non-Goals

- Reverting, dropping, or rewriting either reviewed tool-pill commit.
- Hiding failures by skipping tests, adding expected-failure markers, changing
  the scheme to omit tests, or reducing the observed test counts.
- Fixing Clawline behavior that the causal evidence does not connect to this
  full-green outcome.
- Reopening the historical forecast that seven T190 tests would change. The
  durable observed delta is four T190 tests.
- Duplicating the completed T190 URL-boundary repair.
- Changing Tightbeam wire or substrate behavior.
- Deploying, installing on a physical device, changing credentials, or
  releasing a build.
- Combining code authorship with code review or spec authorship with spec
  review.

## Terms

- **Canonical target**: Clawline commit
  `bbb6de019bed4ec511c0bd4b6463073831ea2107`, which canonical `main` held when
  the integration gate failed. In this spec, “target” always means this frozen
  commit, not a later moving `main` tip.
- **Reviewed base**: commit `8ea6331823d7214640ee21301f68ab5da02e00d1`,
  the parent baseline used to attribute a failure to the tool-pill range.
- **Full gate**: the `xcodebuild test` command in Architecture section 6,
  against an iPhone 17 Pro simulator on iOS 26.5.
- **Issue**: one test assertion or runtime issue that Xcode reports inside a
  test. One failed test can contain more than one issue.
- **Root cause**: the earliest observed condition whose correction removes a
  family of downstream failures.
- **Cascade**: a failed assertion that follows from a root cause and does not
  justify a separate product change.
- **Commit-related failure**: a root cause that passes at the reviewed base and
  fails at the canonical target under the same test environment.
- **Historical-baseline failure**: a root cause that also fails at the reviewed
  base or traces to the accepted historical debt record.
- **Environment failure**: a root cause produced by the simulator, test runner,
  fixture, or test isolation rather than by Clawline product behavior.
- **Classification precedence**: classify a proven runner, fixture, or
  isolation cause as environment. Otherwise, classify a root that reproduces
  at the reviewed base as historical baseline. Classify it as commit-related
  only when it passes at the reviewed base and fails at the target.
- **Repair slice**: one code assignment with one root-cause family, one
  mutation seam, focused verification, and a separate review assignment.
- **Tool-pill contract**: the reviewed behaviors listed in Invariant I4.

## Assumptions

1. Canonical `main`, local `HEAD`, and `origin/main` resolved to the canonical
   target during the integration check.
2. The integration blocker observed 1,042 unit tests in 62 suites with 230
   issues. Its five-test `ClawlineUITests` class had one failure. The completed
   recovery gate later proved nine UI failures: that one failure plus eight of
   15 `T1150NotificationDockUITests`.
3. The integration blocker observed the focused tool-pill test pass during the
   red unit run.
4. Replacement causal assignment
   `asg_055de05e-d64f-4002-b3f8-a497fe387ed6` compared the canonical target
   with the reviewed base in one owned workspace. The reviewed base reproduced
   all six unit groups and the same 1+8 UI shape. The verdict has high
   confidence that the tool-pill commits caused none of these failures.
   Partial artifacts from its revoked predecessor remain non-authoritative.
5. The historical baseline accepted T1484 plus four timing or layout flakes as
   tracked debt. It later recorded an observed four-test T190 red-to-green
   delta after `d4af47ff6b2ca76f2cfaad49e0aa8ae5c327238a` landed. The earlier
   seven-test forecast is not evidence.
6. Eezo provides Xcode 26.6, an iOS 26.5 runtime, and an iPhone 17 Pro
   simulator. The final gate uses that operating environment.
7. A fetch immediately before this spec's publication resolved `origin/main`
   to `bbb6de019bed4ec511c0bd4b6463073831ea2107`. The frozen target and current
   main have zero commits of divergence.

## Invariants

**I1 — Target preservation.** Each repair commit descends from the canonical
target. A repair does not remove either commit in the reviewed tool-pill range.
The accepted integration candidate contains only the target, the reviewed
repair commits, and commits that their independent reviews explicitly covered.

**I2 — Evidence-bound scope.** Each changed production or test seam traces to
one of the six unit groups or two UI groups in the causal verdict. All 230 unit
issues and all nine UI failures map to exactly one repair slice.

**I3 — One owner per failure.** The repair ledger assigns each failing test to
one root-cause family and one repair slice. Cascades stay with their root cause.
Historical failures retain their historical work-item reference even when this
outcome depends on their repair.

**I4 — Tool-pill contract.** The repaired build preserves these reviewed
behaviors:

1. A flat `agent_progress.progressText` payload produces live tool-activity
   progress without a structured pill.
2. A structured tool progress item preserves its tool `name` and argument
   `summary` as separate values.
3. The typing indicator renders a distinct pill for structured tool activity.
4. The pill renders the tool verb in bold terracotta text.
5. The pill renders the argument summary in regular ink text.
6. The pill exposes `"<verb>, <arguments>"` as its accessibility label when
   arguments exist.
7. A terminal progress event or the matching final assistant message clears
   the live progress.

**I5 — Gate integrity.** The accepted unit phase reports exactly 1,042 tests
with zero issues. The accepted `ClawlineUITests` class reports exactly five
tests with zero failures. All 15 `T1150NotificationDockUITests` pass, and the
complete UI target has zero failures. The implementation does not reduce any
of these counts or add test cases that change them.

**I6 — Independent gates.** A reviewer who did not author a change reviews the
exact code revision. Integration starts only after each repair slice receives
a reviewed-clean verdict.

**I7 — Evidence integrity.** Each focused run and the final full gate retain a
complete log and valid `.xcresult`. The evidence records the commit, Xcode
version, simulator runtime, simulator identifier, command, test counts, and
exit status.

**I8 — No product workaround for environment debt.** An environment repair
changes the fixture, test isolation, or test synchronization seam that causes
the failure. It does not change unrelated product behavior to satisfy a test.

## Architecture

### 1. Evidence ledger

The causal verdict owns the root-cause classification. Its final mapping is:

| Family | Classification | Earliest cause | Target failures | Reviewed-base result | Closure choice | Repair slice |
| --- | --- | --- | --- | --- | --- | --- |
| U1 lifecycle ownership | Environment | Concurrent test suites replace the process-wide `ChatViewModel` connection owner before the owning test finishes | 197 unit issues | Same root reproduced | ADD an isolated ownership authority for tests while keeping one production owner | S1 |
| U2 escaped T105 write | Historical baseline | The debug notification seed writes `sessionMessages` directly outside the message-stream mutation seam | 1 unit issue | Same root reproduced | ADD the seed write to the existing mutation seam | S2 |
| U3 HTTP body stub | Environment | `HTTPStubURLProtocol` exposes request bodies inconsistently to handlers | 24 unit issues | Same root reproduced | ADD one normalized request-body capture seam for the stub | S3 |
| U4 timing | Environment | Three stream-toast checks and one submit-readiness check depend on wall-clock scheduling | 4 unit issues | Same root reproduced | ADD observable deterministic timing control | S4 |
| U5 proof directory | Environment | The T1185 render proof writes to a relative directory whose ownership depends on the test runner's current directory | 1 unit issue | Same root reproduced | ADD a writable test-owned default directory with an optional explicit override | S5 |
| U6 stale palette | Historical baseline | Three expected RGB values predate the current canonical palette | 3 unit issues | Same root reproduced | ADD current canonical palette values to the expectations; do not change the palette | S6 |
| UI1 scroll-button proof | Historical baseline | The forced scroll-button launch proof does not expose `scroll_to_bottom_button` before its six-second existence check | 1 of 5 `ClawlineUITests` | Same 1-of-5 shape reproduced | ADD deterministic proof startup while preserving drag and detent behavior | S7 |
| UI2 notification-dock proof | Historical baseline | The T1150 seeded landscape proof does not establish each test's required dock or peek state before interaction | 8 of 15 `T1150NotificationDockUITests` | Same 8-of-15 shape reproduced | ADD deterministic per-test proof state while preserving notification behavior | S8 |

The predecessor's partial artifacts do not modify this mapping. Every row uses
ADD. DELETE loses because A5 and A6 preserve the exact test surfaces and
counts. ACCEPT loses because A5 and A6 require zero issues and failures. A
cascade stays in its owning row instead of becoming a separate closure.
No family is commit-related.

The ledger reconciles the historical 16-red card by identity, not by the old
forecasted count. It records four facts:

1. The T190 repair belongs to `wi_c4000894`; this plan does not duplicate it.
2. The supported landed T190 delta is four tests, from 110 failures to 106 in
   the same-simulator comparison.
3. The four current timing issues are U4. They retain a link to the historical
   debt record, but their current classification is environment because the
   causal verdict identifies test timing as the cause. They must close in S4
   because this outcome permits no gate debt.
4. The current causal partition does not identify T1484 as a root. This plan
   does not absorb it. U2, U6, UI1, and UI2 retain distinct historical repair
   slices and do not become evidence against the tool-pill commits.

### 2. Ordered repair slices

The product owner opens and staffs the slices after the exact spec revision
receives independent reviewed-clean approval. The ordering is:

1. **Wave 1 — bounded unit seams.** Run S2 escaped T105 write before S1
   lifecycle ownership because both touch `ChatViewModel`. S3 HTTP body
   capture, S4 deterministic timing, S5 proof-directory ownership, and S6
   palette can run independently. Each slice gets a separate review.
2. **Wave 2 — lifecycle family closure.** Run S1 after S2. Verify that all 197
   lifecycle issues disappear without changing the production rule that only
   one view model owns the connection.
3. **Wave 3 — UI proof seams.** Run S7 scroll-button proof and S8 T1150 dock
   proof after the unit roots are green. These slices may change only debug or
   UI-test proof setup unless a focused failing test proves a production seam
   is the earliest cause. Any newly proved production behavior change returns
   to spec review before code continues.
4. **S9 — Full-gate integration.** Form the candidate from the frozen target
   plus only reviewed-clean repair slices, run the full gate, and publish that
   exact candidate plus gate evidence. If `origin/main` moves away from the
   expected target before publication, do not merge, rebase, or push under
   this spec. The product owner opens a separately reviewed reconciliation
   lane, and the reconciled candidate must pass a new full gate.

S1 through S8 each own only their ledger row. A slice that uncovers another
root stops and returns the evidence to the product owner; it does not absorb
the new root.

### 3. Ownership boundaries

| Work | Owner | Expected durable result |
| --- | --- | --- |
| Causal classification | Completed `asg_055de05e-d64f-4002-b3f8-a497fe387ed6` | Verdict `att_d5b72926`, report `art_9ae54cbe`, complete log `art_6cc09f4e`, valid result `art_0c285ce3` |
| Repair spec | `asg_31a51bba-dbfa-44d7-8bce-d9be75a35de1` | Canonical spec commit, content hash, artifact row |
| Spec review | New reviewer assignment | Exact-revision reviewed-clean or changes-requested verdict |
| Each code slice | One named coder assignment | Focused green evidence and commit |
| Each code review | One separate reviewer assignment | Exact-revision reviewed-clean or changes-requested verdict |
| Integration | One integrator assignment | Full-green gate and remote-main proof |

### 4. Mutation seams

Each slice has one mutation seam:

- S1: the `ChatViewModel` connection-ownership authority used by test-created
  view models. Production still permits one active connection owner.
- S2: the existing `ChatViewModel` message-stream mutation seam. The debug
  notification seed enters through that seam.
- S3: `ProviderServiceTests.HTTPStubURLProtocol` request-body capture.
- S4: the controllable completion signal used by `StreamToastManagerTests` and
  `SubmitFailureVerificationTests`. Wall-clock sleeps do not decide pass/fail.
- S5: `t1185ProofDirectory`. Without an override it derives a writable
  test-owned temporary directory; an explicit environment value overrides
  that default.
- S6: `MessageBubbleShadowTests` expected RGB fixtures. Production palette
  values do not change.
- S7: the `--debug-force-scroll-button` launch proof and its persisted detent
  fixture.
- S8: `launchDockedNotificationProofApp` and the debug notification-dock seed
  state used by `T1150NotificationDockUITests`.

A slice that needs a second independent seam becomes a second assignment and
returns to spec review before code starts.

The tool-pill seams remain:

- `ChatViewModel.handleAgentProgress` and its progress reducer helpers own live
  progress state.
- `TypingIndicatorCell` owns the structured pill presentation.
- `ProviderChatService` decoding owns preservation of structured tool fields.

No S1 through S8 change can touch these tool-pill seams. The causal verdict
found no commit-related family, and the focused tool-pill tests already pass.
The reviewer verifies Invariant I4 from the exact diff and focused tests.

### 5. Focused verification

Each code slice runs its causal test first with this command shape:

```text
xcodebuild test \
  -project ios/Clawline/Clawline.xcodeproj \
  -scheme Clawline \
  -destination id=<IOS_26_5_IPHONE_17_PRO_UDID> \
  -derivedDataPath <OWNED_DERIVED_DATA> \
  -resultBundlePath <OWNED_RESULT_BUNDLE> \
  -only-testing:<TARGET>/<SUITE>/<TEST>
```

The coder then runs the mapped family. The reviewer repeats the direct causal
test from a clean derived-data path at the exact review revision.

The slice-to-test map is:

| Slice | Direct verification | Family verification |
| --- | --- | --- |
| S1 | Run `ChatViewModelTests` and `T320ReplyIndicatorProofTests` together under the repository's normal parallel suite schedule | Both suites have zero lifecycle-owner issues; production still resolves competing view models to one active owner |
| S2 | `ChatViewModelTests/messageStreamDirectWritesStayInsideSeam` | The debug notification seed still produces its three seeded transcripts through the mutation seam |
| S3 | `ProviderServiceTests/sessionControlPostsTypedProviderActions` receives the exact non-empty POST body for each action | `ProviderServiceTests`; zero missing, empty, or cross-test request-body issues |
| S4 | `StreamToastManagerTests/dismissesAfterConfiguredIdleDelay`, `busyTimeCountsAgainstTotalWindow`, `scrubPreviewToastRemainsPinnedUntilReleaseUpdate`, and `SubmitFailureVerificationTests/sendRequiresActualTransportReadiness` | Both suites pass without wall-clock sleep deciding an assertion |
| S5 | `MessageInputBarBoundaryTests/simulatorRenderProofArtifacts` | The test creates its directory and non-empty proof PNGs beneath the supplied owned path |
| S6 | `MessageBubbleShadowTests` | Light RGB `(213, 237, 201)` and dark RGB `(41, 55, 38)` then `(32, 46, 30)` pass; production palette bytes are unchanged |
| S7 | `ClawlineUITests/testScrollButtonDragMovesAndPersistsDetent` | The one test passes from a clean app install twice in succession |
| S8 | `T1150NotificationDockUITests` is the focused family; all 15 tests start from their declared dock or peek state before interaction | All 15 tests pass from clean per-test proof state; the prior eight failures are absent |

Each row runs with its own derived-data path and result bundle. Before every S7
or S8 run, erase the app under test so persisted proof state cannot mask
startup behavior.

```text
xcrun simctl uninstall <IOS_26_5_IPHONE_17_PRO_UDID> co.clicketyclacks.Clawline
```

S5 first runs without a proof-directory environment variable and proves that
its default is writable and outside the source checkout. It then supplies
`T1185_RENDER_PROOF_DIR=<OWNED_PROOF_DIRECTORY>` and proves that the explicit
override wins. Both runs create non-empty PNGs beneath the selected directory.

### 6. Full-gate verification

The integrator runs this repository command from an owned clean checkout:

```text
xcodebuild test \
  -project ios/Clawline/Clawline.xcodeproj \
  -scheme Clawline \
  -destination id=<IOS_26_5_IPHONE_17_PRO_UDID> \
  -derivedDataPath <OWNED_DERIVED_DATA> \
  -resultBundlePath <OWNED_RESULT_BUNDLE>
```

Before the gate, the integrator records the expected `origin/main` object ID.
After the gate, the integrator verifies the counts, the zero-failure result,
and that the tested revision is unchanged. Publication and the remote-ref
precondition form one operation: the push succeeds only when `origin/main`
still has the recorded object ID and the candidate is its fast-forward
descendant. A changed local revision or remote object ID stops publication and
requires reconciliation plus a new gate.

### 7. No-rollback rule

This plan has no rollback slice. A failed repair returns to its code assignment
for another independently reviewed iteration. A tool-pill regression blocks
integration; the offending repair changes until the existing tool-pill tests
pass without modifying the tool-pill seams. The integrator does not revert
`87b347bf132d31b1f2a6d0983dbd629070cb30e7` or
`bbb6de019bed4ec511c0bd4b6463073831ea2107`.

### 8. Operating pattern

This spec teaches no recurring agent operating pattern. It is a one-time
repair plan and does not amend Clawline or Tightbeam guidance.

## Acceptance

**A1 — Exact causal mapping.** Given the completed evidence in
`att_d5b72926` and `art_9ae54cbe`, when the reviewer sums the ledger, then the
six disjoint unit groups equal 230 issues: 197 lifecycle ownership, one escaped
T105 write, 24 HTTP body stub, four timing, one proof directory, and three
palette. The UI groups equal nine failures in the exact 1+8 shape. Every group
has one classification and one repair slice.

**A2 — Historical reconciliation.** Given `art_95cc63a9` and the later
four-T190 landed delta, when the reviewer checks the repair ledger, then the
ledger preserves the four-test observed delta, assigns no duplicate T190
repair, and keeps each observed historical failure under a historical work
reference.

**A3 — Focused slice result.** Given a repair slice at its exact code revision,
when its coder runs the direct causal test and mapped family, then each named
test passes with zero issues and the result bundle is valid.

**A4 — Independent code review.** Given a repair commit and focused evidence,
when a reviewer who did not author the commit reviews and repeats its direct
causal test, then the reviewer files reviewed-clean before integration starts.

**A5 — Unit gate.** Given the integrated reviewed-clean revision on an iPhone
17 Pro simulator with iOS 26.5, when the integrator runs the full gate, then
Xcode reports exactly 1,042 unit tests with zero issues.

**A6 — UI gate.** Given the same integrated revision and simulator, when the
full gate reaches the UI target, then the `ClawlineUITests` class reports
exactly five tests with zero failures, all 15
`T1150NotificationDockUITests` pass, and every other UI suite has zero
failures. `testScrollButtonDragMovesAndPersistsDetent` passes.

**A7 — Flat progress compatibility.** Given an `agent_progress` payload whose
only progress body is `progressText = "Read config/runtime.exs"`, when
`ChatViewModel` consumes it, then the selected session exposes tool-activity
stage and the same summary without a structured tool pill.

**A8 — Structured tool preservation.** Given a structured tool progress item
with `name = "exec"` and `summary = "git status"`, when the provider decoder
and progress reducer consume it, then live progress retains
`LiveToolActivity(verb: "exec", argumentsSummary: "git status")`.

**A9 — Pill presentation.** Given the live tool activity from A8, when
`TypingIndicatorCell` renders it, then the cell shows a distinct pill, bold
verb text, regular argument text, accessibility label `"exec, git status"`,
and a height greater than the summary-only indicator height.

**A10 — Progress cleanup.** Given live progress linked to a client message,
when Clawline receives a matching final assistant message or terminal progress
state, then `liveProgress` for that session becomes absent.

**A11 — No rollback.** Given the integration revision, when the reviewer checks
its ancestry, then both tool-pill commits are ancestors and the reviewed
tool-pill tests A7 through A10 pass.

**A12 — Gate integrity.** Given the accepted full-gate log and `.xcresult`,
when the reviewer compares the scheme and test counts with the blocker run,
then the scheme contains the unit and UI targets, the unit count is 1,042, the
`ClawlineUITests` count is five, the T1150 count is 15, every UI test passes,
and the command exits zero.

**A13 — Frozen-target publication.** Given a candidate whose reviewed ancestry
starts at the canonical target and an `origin/main` object ID recorded before
its gate, when integration publishes the gated candidate, then the tested
revision is unchanged, the remote compare succeeds against that recorded
object ID, and the update is fast-forward. A remote mismatch produces no
publication under this spec.

**A14 — Unit-family closure.** Given S1 through S6 at their reviewed revisions,
when the reviewer runs the slice-to-test map, then each direct test and mapped
family passes, the six issue deltas sum to 230, and the production palette,
single-owner rule, and unrelated product behavior are unchanged.

**A15 — UI-proof closure.** Given S7 and S8 on a clean simulator app install,
when the reviewer runs each focused proof twice, then the scroll-button proof
passes twice, all 15 T1150 tests pass twice, and no run depends on state left
by its predecessor.

## Open Questions

None. The causal verdict closes the former blocking family-map question. The
current-main check found no drift from the frozen target.
