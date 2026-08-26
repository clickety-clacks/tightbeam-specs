# Clawline Incoming-Messages Fixture Addendum

Status: READY FOR INDEPENDENT SPEC REVIEW.

Authority:

- This addendum extends, and does not replace,
  `clickety-clacks/tightbeam-specs/clawline-full-green-repair.md` at commit
  `76d7fd8e1aaa11bbced68b4b018856e7ef2615f9`, SHA-256
  `5dc67f1614e371f8cdf35347d92bac377db929a7a9ce35399a449d1f2a8e373e`.
- Parent artifact: `art_b4b0da44`. Parent reviewed-clean verdict:
  `att_ba6d341f-ec73-4fc6-9533-d657fd5925aa`.
- Outcome work item: `wi_3ccc7dcd-f77d-45e2-96ba-f7e58170ecc1`.
- Spec assignment: `asg_916dce59-78aa-4836-bc47-6f5b7e90972c`.
- Product-spirit verdict: `att_99bf8980-a284-40d6-9896-69a80e6121ef`.
- S1 causal evidence: `att_ffa37cb6-25d4-4d28-a65c-a8e06760ed39`.
- Required R1 code base: reviewed-clean S1 commit
  `061d123009228e23672f84ac97124d3761718399`. S1 producer:
  `asg_46e300a8-ee6e-4ac8-8f6a-2b26f08427de`. S1 independent review:
  `asg_760aa557-1919-4389-9891-c953b53bf77d`. S1 reviewed-clean verdict:
  `att_b38420d3-44ec-46ef-8677-3a49a8620e65`.
- Exact R1 baseline evidence is retained in
  `eezo:/Users/mike/.tightbeam/work/16bdf7f7e5e7/clawline-s1-baseline-spec-061d/evidence/exact-s1-baseline/`.
  The focused files are `ChatViewModelTests.log` and
  `ChatViewModelTests.xcresult`. The combined files are
  `ChatViewModel-T320.log` and `ChatViewModel-T320.xcresult`.
- Reconciled Clawline `main` comparison target:
  `bbb6de019bed4ec511c0bd4b6463073831ea2107`.
- Provenance commits: repair `9c8043ed4139686bca03ccd643c45d978cba375d`
  and merge `b0b853d3f05b738ff959ecfa4f7564d073615cad`.
- Workflow: SPEC → independent SPEC REVIEW → CODE → independent CODE REVIEW.
  An author does not review their own work.

## Goal

Close the residual historically labeled the 44-failure
`ChatViewModelTests` fixture regression. The exact reviewed-clean S1 baseline
supersedes that historical count: it reproduces 46 focused failures and 48
combined failures. Restore the missing owner-gated path from
`ChatServicing.incomingMessages` to the existing
`ChatViewModel.handleIncoming` mutation seam.

The repair must keep S1's production single-connection-owner rule. It must
keep parent acceptance clauses A7 through A10. It must make all 164 focused
tests and all 166 combined tests pass with zero failures.

## Non-Goals

- Changing, weakening, replacing, or absorbing S1.
- Restoring the process-wide DEBUG ownership bypass from `9c8043ed`.
- Adding a fixture activation helper or changing any test fixture.
- Changing `ChatViewModel.activate`, `ChatViewModel.onAppear`,
  `ChatViewModel.handleIncoming`, lifecycle coordinator semantics, provider
  decoding, replay behavior, message presentation, haptics, stream rules,
  session controls, or test assertions.
- Changing `ChatServicing`, `ProviderChatService`, or a production wire format.
- Editing a file other than the one file named in Architecture section 3.
- Adding, removing, skipping, retrying, or marking an expected failure in a
  test.
- Changing the 1,042-unit-test full-gate count or a UI-test count in the parent
  spec.
- Starting S7, S8, or S9 before this addendum's ordered gates permit it.
- Reverting a reviewed tool-pill commit or changing a tool-pill seam.
- Merging, deploying, or releasing as part of this addendum's spec or code
  assignments.

## Terms

- **Parent spec**: the exact reviewed full-green spec named in Authority.
- **S1**: the parent spec's lifecycle-ownership repair slice at exact commit
  `061d123009228e23672f84ac97124d3761718399`.
- **R1**: this addendum's incoming-messages observation repair. R1 is not S1.
- **Historical 44-failure label**: the work-item label derived from the
  pre-S1, uncommitted `d77ac425`-based result. It does not define the immutable
  R1 baseline.
- **Exact focused baseline**: the retained 164-test result at exact S1. It
  reports 118 passes and 46 failures.
- **Exact combined baseline**: the retained 166-test result at exact S1. It
  reports 118 passes and 48 failures.
- **Exact Chat failure union**: the 48 distinct `ChatViewModelTests`
  identifiers in Architecture section 2. The focused result contains 46. The
  combined result contains 47 plus one T320 failure.
- **Incoming-messages observation seam**: one stored subscription to
  `chatService.incomingMessages`, one observer child that forwards each
  message to existing `handleIncoming`, and teardown that releases the stored
  subscription.
- **Owner-gated**: reachable only after the existing `isConnectionOwner`
  checks in `activate` and `startObservingIfNeeded` succeed.
- **Focused run**: the `ChatViewModelTests` command in Architecture section 5.
- **Combined run**: the `ChatViewModelTests` plus
  `T320ReplyIndicatorProofTests` command in Architecture section 5.

## Assumptions

1. The baseline checkout has detached `HEAD` at
   `061d123009228e23672f84ac97124d3761718399`. Only the retained `evidence/`
   directory is untracked. No product file differs from that commit.
2. The current parent-spec bytes match the reviewed parent SHA-256 even though
   the specs repository contains later unrelated commits.
3. Xcode 26.6 build 17F113 produced both baseline bundles on iPhone 17 Pro
   simulator `87C9E79C-76CB-45E0-B625-FBF021916789`, iOS 26.5 build 23F77.
4. The focused bundle is valid. It reports 164 total tests, 118 passes, 46
   failures, zero expected failures, and zero skipped tests.
5. The combined bundle is valid. It reports 166 total tests, 118 passes, 48
   failures, zero expected failures, and zero skipped tests. Its test tree
   contains 47 failed `ChatViewModelTests` cases and one failed T320 case.
6. The exact Chat failure union contains 48 identifiers. Forty-five fail in
   both runs. `cancelledReconnectDelayDoesNotTriggerExtraReconnect()` fails
   only in the focused run. `historyResetPreservesCursorBackedActiveStreamWithEmptyReplayWindow()`
   and `setHarnessUsesCapabilityWhenCurrentTightbeamServerFlagIsAbsent()` fail
   only in the combined run.
7. Both result summaries contain no failure text that names connection
   ownership, owner displacement, a non-owner guard, or an ownership
   assertion.
8. The S1 tests `testCreatedViewModelsHoldIsolatedConnectionOwnership()`,
   `productionAuthorityPermitsOneActiveConnectionOwner()`,
   `activateInitializesObservationOnce()`, and
   `transientDisappearPreservesLifecycleObservation()` pass in both runs.
9. Exact S1 gives test-created view models isolated ownership with activation
   policy `onFirstAppearance`. Exact S1 `onAppear` awaits `activate` before it
   marks the view visible when that policy has not activated the instance.
10. Every identifier in the exact Chat failure union already awaits either
    `activate` or `onAppear` before the observation-dependent action. A new
    activation helper would duplicate exact S1 behavior.
11. Current `ChatViewModel.startObservingIfNeeded` observes lifecycle
    transport, lifecycle output, lifecycle debug, provider connection state,
    and service event streams. It does not obtain or observe
    `chatService.incomingMessages`.
12. `TestChatService.emit(_:)` yields only through its `incomingMessages`
    continuation. The current view model never consumes that stream.
13. Commit `9c8043ed` contained `incomingMessagesSubscription`, an
    `observeIncomingMessages` child, and subscription teardown. Merge
    `b0b853d3`, whose parents are
    `d7bc6d84891c6b1975778883a61914070311ddcb` and
    `0c295c4cde4565a23b48894546130688bb95a7b4`, retained none of those three
    production lines of repair.

## Invariants

**I1 — S1 remains authoritative.** R1 does not change an ownership flag,
owner claim, owner release, replacement rule, activation policy, lifecycle
owner test, or test-only initializer. R1 does not add a global or per-suite
ownership bypass.

**I2 — One owner observes.** The incoming-messages observer starts only inside
the existing owner-gated observation startup. A non-owner view model does not
subscribe to or consume incoming messages.

**I3 — One incoming subscription.** One active view model has at most one
stored incoming-messages subscription. Repeated or concurrent activation does
not create another subscription or another delivery.

**I4 — Existing message semantics.** The observer passes each message to the
existing `handleIncoming` method exactly once. R1 does not copy, fork, or
change message mutation logic.

**I5 — Complete teardown.** Logout, replacement, and observation teardown
cancel the observer through the existing observation task and clear the stored
incoming-messages subscription. A retired view model cannot consume a later
message.

**I6 — Exact S1 activation stays intact.** R1 does not add
`activateAndAppear`, replace `onAppear`, add an extra activation call, or edit
a test fixture.

**I7 — Assertion preservation.** R1 changes no test name, test annotation,
expected value, timeout, skip, expected-failure marker, or production outcome.

**I8 — Tool-pill preservation.** Parent clauses A7, A8, A9, and A10 remain
behavioral requirements. R1 does not change `handleAgentProgress`, provider
progress decoding, `LiveToolActivity`, or `TypingIndicatorCell`.

**I9 — Count preservation.** The focused run contains the same 164 tests as
the focused baseline. The combined run contains those 164 tests plus the same
two T320 tests. R1 adds or removes no test.

**I10 — Independent gates.** An independent reviewer approves the exact R1
spec revision before code starts. Another independent reviewer approves the
exact R1 code revision before S7, S8, or S9 can consume it.

## Architecture

### 1. Causal boundary

The exact S1 baseline closes the prior review's evidence hole:

1. S1's four ownership and lifecycle proof tests pass in both retained runs.
2. No retained failure text has a connection-owner signature.
3. Every failed Chat fixture already enters observation through exact S1
   `activate` or activation-aware `onAppear`.
4. `incomingMessagesRoutePerStream`, `streamingMessagesUpdateInPlace`, and the
   two assistant haptic tests emit through `TestChatService.emit(_:)`.
   Current `ChatViewModel` has no consumer for that stream.
5. The combined T320 failure calls activation-aware `onAppear` and then emits
   through the same missing incoming-messages path.

R1 therefore owns only the missing incoming-messages observer. R1 does not own
fixture activation. The code lane must stop and return to this spec if the
one-file observer repair does not make the focused and combined gates green.
The code lane must not widen the patch to chase a remaining failure.

### 2. Exact Chat failure union

The immutable focused and combined baselines produce this 48-identifier union:

1. `activatingStreamPublishesReadState()`
2. `activeStreamIncomingAssistantPublishesReadState()`
3. `adoptedGatewaySessionSendBypassesStreamOnlySessionInfo()`
4. `adoptedSessionRestoresAsLastSavedChat()`
5. `adoptedSessionsCanBeRenamedWithoutDelete()`
6. `assetBackedInteractiveHTMLHydratesForInlineRenderPath()`
7. `assistantIncomingAppendFiresHapticWhenVisibleAndForeground()`
8. `assistantIncomingHapticIsDebounced()`
9. `canSendRequiresActiveSessionProvisioning()`
10. `cancelledReconnectDelayDoesNotTriggerExtraReconnect()`
11. `createFailureLaterSocketReconcile()`
12. `currentPromptCancellationTargetsVisibleStreamDuringPagerSwitchDebounce()`
13. `deleteFailureLaterSocketReconcile()`
14. `deletingActiveStreamFallsBack()`
15. `disconnectedMapsToDisconnectedSendButtonState()`
16. `dismissedReplayedAssistantContentStaysDismissedUntilNewerAssistantContent()`
17. `dismissingNotificationClearsSourceUnreadDot()`
18. `historyResetDismissalKeepsOnlyLaterReplayNotifications()`
19. `historyResetPreservesCursorBackedActiveStreamWithEmptyReplayWindow()`
20. `incomingMessagesRoutePerStream()`
21. `incrementalStreamEvents()`
22. `initialTrackableSessionsLoadFailureIsSurfaced()`
23. `networkLostSendFailureLeavesSendButtonNonGreen()`
24. `notificationReplyActionTogglesReplyMode()`
25. `notificationReplyClosesOnlyAfterSuccessfulSend()`
26. `overflowingNotificationClosesReplyDraft()`
27. `pendingSendKeepsTargetSessionDuringSwitch()`
28. `persistDebounceCancellationDoesNotFlushEarly()`
29. `promptStageIndicatorIsScopedToSelectedStream()`
30. `promptTurnFailedStateMarksAcceptedSendFailedImmediately()`
31. `queuedCrossChatMentionClearsComposerToPreventCurrentChatLeak()`
32. `replayCommitAllowsSourceNoLongerCurrentAtTerminalBoundary()`
33. `replayNavigationDuringPendingDoesNotDropTerminalEligibleNotification()`
34. `selectedSessionOAuthUsageClearsWindowsOnAuthoritativeBindingFailure()`
35. `sendBlocksStaleSyntheticSessionKey()`
36. `serverEchoCanonicalSessionMovesPendingPlaceholderThroughSeam()`
37. `sessionStatusRefreshKeepsIncomingAuthModeWhenPreservingStickyFields()`
38. `sessionStatusStickyDisplayMetadataIsKeyedPerStream()`
39. `setHarnessUsesCapabilityWhenCurrentTightbeamServerFlagIsAbsent()`
40. `snapshotRemovesChildStreamOmittedByServer()`
41. `streamSnapshotReplacementFallback()`
42. `streamingMessagesUpdateInPlace()`
43. `trackAdoptsUntrackedSessionAcrossSnapshots()`
44. `trackCandidatesLoadFromProviderEndpoint()`
45. `typingIndicatorMorphTargetIsNewAssistantMessageAndOneShot()`
46. `untrackRemovesLocalLinkOnly()`
47. `untrackUndoRestoresAdoptedSession()`
48. `userEchoWithoutDeviceIdDoesNotDuplicate()`

Every identifier has target `ClawlineTests/ChatViewModelTests`. The combined
baseline also fails
`T320ReplyIndicatorProofTests/acceptedReplySendEchoesReplyTokenMetadataOntoOutgoingBubble()`.

### 3. Exact file and ownership boundary

R1 may edit only this file:

| File | R1 owns | R1 must not change |
| --- | --- | --- |
| `ios/Clawline/Clawline/ViewModels/ChatViewModel.swift` | Stored `incomingMessages` subscription, synchronous subscription initialization inside existing observation startup, one observer child, and subscription teardown | Owner authority, activation, lifecycle coordinator, `handleIncoming`, progress reducer, provider connection observer, service-event observer, message rules, or UI behavior |

The code assignment must stop and return to spec review if it needs a second
file, a test edit, another production mutation seam, or an assertion change.

### 4. Required implementation shape

The code author must implement all of these clauses:

1. Add one optional stored `AsyncStream<Message>` subscription for
   `chatService.incomingMessages`.
2. Initialize the stored subscription synchronously in the existing
   owner-gated startup task before assigning the observation task.
3. Reuse the stored subscription when activation joins or repeats. Do not
   obtain `chatService.incomingMessages` a second time while the stored
   subscription exists.
4. Add one child to the existing observation task group. The child iterates
   the stored stream and calls existing `handleIncoming` once for each value.
5. Clear the stored subscription in `stopObservingLifecycle` with the other
   stored subscriptions.
6. Keep every new line behind the existing owner checks. Do not add a
   test-only ownership exception.
7. Do not edit a test file. Do not add or use `activateAndAppear`.

The code reviewer compares the exact diff with `9c8043ed`. The reviewer may
accept only the incoming-messages subscription, observer child, and teardown
pattern. The reviewer must reject the historical global ownership bypass,
historical test-helper edits, and every unrelated historical change.

### 5. Verification commands

Run every command from an owned clean Clawline checkout based on exact S1
`061d123009228e23672f84ac97124d3761718399` on Eezo with Xcode 26.6, an iPhone
17 Pro simulator, and iOS 26.5. Replace only the angle-bracket paths and
simulator identifier. Each command uses a new derived-data directory and a new
result-bundle path.

Direct causal command:

```text
xcodebuild test \
  -project ios/Clawline/Clawline.xcodeproj \
  -scheme Clawline \
  -destination 'platform=iOS Simulator,id=<IOS_26_5_IPHONE_17_PRO_UDID>' \
  -derivedDataPath <FRESH_OWNED_DIRECT_DERIVED_DATA> \
  -resultBundlePath <FRESH_OWNED_DIRECT_RESULT_BUNDLE> \
  -parallel-testing-enabled YES \
  '-only-testing:ClawlineTests/ChatViewModelTests/incomingMessagesRoutePerStream()' \
  '-only-testing:ClawlineTests/ChatViewModelTests/streamingMessagesUpdateInPlace()' \
  '-only-testing:ClawlineTests/ChatViewModelTests/assistantIncomingAppendFiresHapticWhenVisibleAndForeground()' \
  '-only-testing:ClawlineTests/ChatViewModelTests/assistantIncomingHapticIsDebounced()'
```

Focused command:

```text
xcodebuild test \
  -project ios/Clawline/Clawline.xcodeproj \
  -scheme Clawline \
  -destination 'platform=iOS Simulator,id=<IOS_26_5_IPHONE_17_PRO_UDID>' \
  -derivedDataPath <OWNED_FOCUSED_DERIVED_DATA> \
  -resultBundlePath <OWNED_FOCUSED_RESULT_BUNDLE> \
  -parallel-testing-enabled YES \
  -only-testing:ClawlineTests/ChatViewModelTests
```

Combined S1 plus R1 command:

```text
xcodebuild test \
  -project ios/Clawline/Clawline.xcodeproj \
  -scheme Clawline \
  -destination 'platform=iOS Simulator,id=<IOS_26_5_IPHONE_17_PRO_UDID>' \
  -derivedDataPath <OWNED_COMBINED_DERIVED_DATA> \
  -resultBundlePath <OWNED_COMBINED_RESULT_BUNDLE> \
  -parallel-testing-enabled YES \
  -only-testing:ClawlineTests/ChatViewModelTests \
  -only-testing:ClawlineTests/T320ReplyIndicatorProofTests
```

Protected parent A7-A10 command:

```text
xcodebuild test \
  -project ios/Clawline/Clawline.xcodeproj \
  -scheme Clawline \
  -destination 'platform=iOS Simulator,id=<IOS_26_5_IPHONE_17_PRO_UDID>' \
  -derivedDataPath <OWNED_TOOL_PILL_DERIVED_DATA> \
  -resultBundlePath <OWNED_TOOL_PILL_RESULT_BUNDLE> \
  -parallel-testing-enabled YES \
  -only-testing:ClawlineTests/ChatViewModelTests/liveAgentProgressUpdatesAndClears \
  -only-testing:ClawlineTests/ProviderServiceTests/agentProgressDoesNotAdvanceReplayCursor \
  -only-testing:ClawlineTests/ProviderServiceTests/structuredToolProgressPreservesNameAndArgumentsSummary \
  -only-testing:ClawlineTests/ClawlineTests/toolActivityRendersDistinctVerbAndArgumentsPill
```

The coder retains the complete log and valid `.xcresult` from every command.
The evidence records the tested commit, command, Xcode version, runtime,
simulator identifier, counts, and exit status.

### 6. Ordering and integration

The product owner applies this order:

1. S1 reaches independently reviewed-clean at exact commit `061d1230`.
2. R1 code starts from exact commit `061d1230`.
3. R1 receives independently reviewed-clean at its exact code revision after
   the direct, focused, combined, and protected commands pass.
4. Only then, and only after the parent spec's other unit prerequisites are
   reviewed-clean, may the parent plan start or resume S7 and S8. R1 clears
   only the added R1 block.
5. S9 remains blocked until R1, S7, S8, and every other parent prerequisite
   are reviewed-clean and green.

R1 does not authorize integration. The parent spec remains authoritative for
the 1,042-test full gate, UI gates, frozen-target reconciliation, and remote
publication.

## Acceptance

**A1 — Focused baseline identity.** Given the retained focused result, when
the reviewer reads its summary and test tree, then they report exact code
commit `061d1230`, 164 tests, 118 passes, 46 failed test cases, zero skips, and
zero expected failures.

**A2 — Combined baseline identity.** Given the retained combined result, when
the reviewer reads its summary and test tree, then they report exact code
commit `061d1230`, 166 tests, 118 passes, 48 failed test cases, zero skips, and
zero expected failures. Forty-seven failed cases belong to
`ChatViewModelTests`. One failed case belongs to
`T320ReplyIndicatorProofTests`.

**A3 — No ownership signature.** Given both retained summaries and logs, when
the reviewer searches failure text for connection ownership, owner
displacement, non-owner guards, and ownership assertions, then the search
returns no match. The four S1 proof tests named in Assumption 8 pass.

**A4 — Provenance.** Given `9c8043ed` and merge `b0b853d3`, when the reviewer
compares `ChatViewModel.swift`, then `9c8043ed` contains the incoming
subscription, observer child, and teardown, and the merge result contains none
of them. The R1 diff restores only that bounded production pattern. It does
not restore the ownership bypass or a test-helper edit.

**A5 — Direct cause.** Given the exact R1 code revision, when the coder runs
the direct command, then the result reports total=4, passed=4, failed=0,
skipped=0, and zero expected failures.

**A6 — Focused family.** Given the same revision and a clean derived-data
path, when the coder runs the focused command, then all 164 tests pass. Every
section 2 identifier is present. The result reports zero failures, skips, and
expected failures.

**A7 — Combined S1 boundary.** Given reviewed-clean S1 plus R1, when the coder
runs the combined command under normal parallel testing, then all 166 tests
pass. Both T320 tests pass. The result reports zero failures, skips, and
expected failures.

**A8 — Flat progress compatibility.** Given an `agent_progress` payload whose
only progress body is `progressText = "Read config/runtime.exs"`, when
`ChatViewModel` consumes it, then the selected session exposes tool-activity
stage and the same summary without a structured tool pill.

**A9 — Structured tool preservation.** Given a structured tool progress item
with `name = "exec"` and `summary = "git status"`, when the provider decoder
and progress reducer consume it, then live progress retains
`LiveToolActivity(verb: "exec", argumentsSummary: "git status")`.

**A10 — Pill presentation.** Given the live tool activity from A9, when
`TypingIndicatorCell` renders it, then the cell shows a distinct pill, bold
verb text, regular argument text, accessibility label `"exec, git status"`,
and a height greater than the summary-only indicator height.

**A11 — Progress cleanup.** Given live progress linked to a client message,
when Clawline receives a matching final assistant message or terminal progress
state, then `liveProgress` for that session becomes absent.

**A12 — Protected tool-pill run.** Given the exact R1 revision, when the coder
runs the protected parent A7-A10 command, then all four named tests pass with
zero failures. The R1 diff does not touch a tool-pill seam.

**A13 — Exact file boundary.** Given the R1 code diff, when the reviewer lists
changed paths, then it lists only
`ios/Clawline/Clawline/ViewModels/ChatViewModel.swift`. The diff contains no
activation, ownership, lifecycle-coordinator, test, assertion, timeout,
test-count, or unrelated behavior change.

**A14 — Single delivery.** Given `streamingMessagesUpdateInPlace`, when its
fixture emits the partial and final values for one message identifier, then
the view model contains one message with final content. Static review confirms
that one observer consumes the stored subscription and teardown clears it.

**A15 — No fixture rewrite.** Given the R1 code diff, when the reviewer
searches changed files for `ChatViewModelTests`, `T320ReplyIndicatorProofTests`,
`activateAndAppear`, or an added activation call, then the search returns no
change.

**A16 — Stop on residual.** Given the one-file R1 patch, when the direct,
focused, combined, or protected command reports one failure, then the code
author files the exact evidence and returns to spec review. The author does
not edit another file or widen R1.

**A17 — Ordered review.** Given the full-green repair graph, when R1 code
starts, then S1 is already reviewed-clean at `061d1230`. When S7 or S8 starts
or resumes, then R1 is independently reviewed-clean with A5 through A16 green.

**A18 — S9 remains blocked.** Given reviewed-clean R1, when the product owner
evaluates integration, then R1 alone does not authorize S9. S9 still waits for
all parent-spec repair slices, independent reviews, focused evidence, and the
parent full-gate conditions.

## Open Questions

None. Exact S1 evidence fixes the baseline identity, removes the rejected
visibility-only assumption, and excludes fixture rewrites from R1.
