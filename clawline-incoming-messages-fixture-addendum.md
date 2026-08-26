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
- Causal evidence: `att_ffa37cb6-25d4-4d28-a65c-a8e06760ed39`, result
  `eezo:/Users/mike/.tightbeam/work/ae53f768d95c/clawline-s1/evidence/s1-focused-pass/ChatViewModel-T320.xcresult`,
  and complete log beside it at `ChatViewModel-T320.log`.
- Canonical Clawline target: `bbb6de019bed4ec511c0bd4b6463073831ea2107`.
- Provenance commits: repair `9c8043ed4139686bca03ccd643c45d978cba375d`
  and merge `b0b853d3f05b738ff959ecfa4f7564d073615cad`.
- Workflow: SPEC → independent SPEC REVIEW → CODE → independent CODE REVIEW.
  An author does not review their own work.

## Goal

Close the 44-test `ChatViewModelTests` residual that remained after the S1
connection-ownership repair proved its causal checks. Restore the deterministic
test-fixture path from `TestChatService.incomingMessages` into the existing
`ChatViewModel.handleIncoming` mutation seam. Start every affected fixture's
observers before the fixture declares the view visible.

The repair must keep the production single-connection-owner rule. It must keep
the reviewed tool-pill behaviors in parent acceptance clauses A7 through A10.
It must make the focused `ChatViewModelTests` suite and the combined S1 suite
pass with zero failures.

## Non-Goals

- Changing, weakening, replacing, or absorbing the S1 connection-ownership
  repair.
- Restoring the process-wide DEBUG ownership bypass from `9c8043ed`.
- Changing `ChatViewModel.handleIncoming`, lifecycle coordinator semantics,
  provider decoding, replay behavior, message presentation, haptics, stream
  rules, session controls, or test assertions.
- Changing `ChatServicing`, `ProviderChatService`, or any production wire
  format.
- Editing a file outside the two files named in Architecture section 3.
- Changing the 1,042-unit-test full-gate count or any UI-test count in the
  parent spec.
- Starting S7, S8, or S9 before this addendum's ordered gates permit it.
- Reverting either reviewed tool-pill commit or changing the tool-pill seams.
- Merging, deploying, or releasing as part of this addendum's spec or code
  assignments.

## Terms

- **Parent spec**: the exact reviewed full-green spec named in Authority.
- **S1**: the parent spec's lifecycle-ownership repair slice. It owns test
  connection authority and the production single-owner rule.
- **R1**: this addendum's incoming-messages fixture residual. R1 is not S1 and
  does not change S1's authority.
- **Affected fixture**: a `ChatViewModelTests` test that constructs
  `TestChatService`, depends on one of its asynchronous streams, and belongs to
  the 44-test ledger in Architecture section 2.
- **Fixture activation**: awaiting `ChatViewModel.activate(origin:)` before
  awaiting `ChatViewModel.onAppear(origin:)`.
- **Incoming-messages observation seam**: one stored subscription to
  `chatService.incomingMessages`, one observer task that forwards each message
  to the existing `handleIncoming` method, and teardown that releases the
  subscription.
- **Owner-gated**: reachable only after the existing `isConnectionOwner` checks
  in `activate` and `startObservingIfNeeded` succeed.
- **Focused run**: the `ChatViewModelTests` command in Architecture section 5.
- **Combined run**: the `ChatViewModelTests` plus
  `T320ReplyIndicatorProofTests` command in Architecture section 5.
- **44-test family**: the exact identifiers in Architecture section 2, as
  reported by the cited valid result bundle.

## Assumptions

1. A fresh reconciliation resolved local Clawline `HEAD` and `origin/main` to
   `bbb6de019bed4ec511c0bd4b6463073831ea2107`. The target has zero commits of
   drift in either direction.
2. The current `clawline-full-green-repair.md` bytes still match the reviewed
   parent SHA-256 even though the specs repository has later unrelated commits.
3. The cited result bundle is valid. It reports 164 total tests, 120 passes,
   44 failures, zero expected failures, and zero skipped tests on an iPhone 17
   Pro simulator with iOS 26.5.
4. Both T320 proof tests pass in that result. S1 activation, idempotence,
   transient lifecycle, and production shared-owner checks also pass.
5. The result summary and log contain no failure text that names connection
   ownership, owner displacement, a non-owner guard, or an ownership
   assertion. The remaining failures are therefore not evidence that S1 is
   incomplete.
6. Current `ChatViewModel.startObservingIfNeeded` observes lifecycle transport,
   lifecycle output, lifecycle debug, provider connection state, and service
   event streams. It does not observe `chatService.incomingMessages`.
7. Current `TestChatService.emit(_:)` yields only through its
   `incomingMessages` continuation. Tests that only call `onAppear` do not
   start the observation task because `onAppear` is visibility-only.
8. Commit `9c8043ed` contained an `incomingMessagesSubscription`, an
   `observeIncomingMessages` task, subscription teardown, and an
   `activateAndAppear` test helper. Merge `b0b853d3`, whose parents are
   `d7bc6d84891c6b1975778883a61914070311ddcb` and
   `0c295c4cde4565a23b48894546130688bb95a7b4`, retained neither repair in its
   result.

## Invariants

**I1 — S1 remains authoritative.** R1 does not change an ownership flag,
owner claim, owner release, replacement rule, or lifecycle owner test. R1 does
not introduce a global or per-suite ownership bypass.

**I2 — One owner observes.** The incoming-messages observer starts only inside
the existing owner-gated observation startup. A non-owner view model does not
subscribe or consume incoming messages.

**I3 — One incoming subscription.** One active view model has at most one
stored incoming-messages subscription and one incoming observer task.
Repeated activation does not create another subscription or another delivery.

**I4 — Existing message semantics.** The observer passes each message to the
existing `handleIncoming` method exactly once. R1 does not copy, fork, or
change message mutation logic.

**I5 — Complete teardown.** Logout, replacement, and observation teardown
cancel the observer task through the existing observation task and clear its
stored incoming-messages subscription. A retired view model cannot consume a
later fixture message.

**I6 — Fixture order.** Each affected fixture awaits `activate` before it
awaits `onAppear`. The helper does not claim ownership, disable ownership, or
perform assertions.

**I7 — Assertion preservation.** R1 changes no test name, test annotation,
expected value, timeout, skip, expected-failure marker, or production outcome.

**I8 — Tool-pill preservation.** Parent clauses A7, A8, A9, and A10 remain
byte-for-byte behavioral requirements. R1 does not change
`handleAgentProgress`, provider progress decoding, `LiveToolActivity`, or
`TypingIndicatorCell`.

**I9 — Count preservation.** The focused run contains the same 162
`ChatViewModelTests` tests observed in the cited evidence. The combined run
contains those 162 tests plus the same two T320 tests. R1 adds or removes no
test.

**I10 — Independent gates.** An independent reviewer approves the exact R1
spec revision before code starts. Another independent reviewer approves the
exact R1 code revision before S7, S8, or S9 can consume it.

## Architecture

### 1. Causal boundary

The 44 failures are one fixture-startup cascade, not 44 product defects.
Three direct observations establish the boundary:

1. `incomingMessagesRoutePerStream`, `streamingMessagesUpdateInPlace`, and the
   assistant incoming-haptic tests emit through `TestChatService.emit(_:)`.
   Current `ChatViewModel` has no consumer for that stream.
2. Stream, status, prompt, notification, and control tests emit through other
   asynchronous `TestChatService` streams. Many affected fixtures call only
   visibility-only `onAppear`, so their observer task never starts.
3. The S1 ownership proofs pass, and none of the 44 failure texts carries an
   owner signature. Ownership is a prerequisite supplied by S1, not the root
   that R1 changes.

R1 therefore restores the two coupled halves of one fixture contract:

- the owner-gated `incomingMessages` consumer; and
- the fixture helper that activates observers before marking the view visible.

### 2. Exact 44-test ledger

The focused family contains these identifiers and no inferred additions:

1. `activatingStreamPublishesReadState()`
2. `activeStreamIncomingAssistantPublishesReadState()`
3. `adoptedGatewaySessionSendBypassesStreamOnlySessionInfo()`
4. `adoptedSessionRestoresAsLastSavedChat()`
5. `adoptedSessionsCanBeRenamedWithoutDelete()`
6. `assetBackedInteractiveHTMLHydratesForInlineRenderPath()`
7. `assistantIncomingAppendFiresHapticWhenVisibleAndForeground()`
8. `assistantIncomingHapticIsDebounced()`
9. `canSendRequiresActiveSessionProvisioning()`
10. `createFailureLaterSocketReconcile()`
11. `currentPromptCancellationTargetsVisibleStreamDuringPagerSwitchDebounce()`
12. `deleteFailureLaterSocketReconcile()`
13. `deletingActiveStreamFallsBack()`
14. `disconnectedMapsToDisconnectedSendButtonState()`
15. `dismissedReplayedAssistantContentStaysDismissedUntilNewerAssistantContent()`
16. `dismissingNotificationClearsSourceUnreadDot()`
17. `historyResetDismissalKeepsOnlyLaterReplayNotifications()`
18. `incomingMessagesRoutePerStream()`
19. `incrementalStreamEvents()`
20. `initialTrackableSessionsLoadFailureIsSurfaced()`
21. `networkLostSendFailureLeavesSendButtonNonGreen()`
22. `notificationReplyActionTogglesReplyMode()`
23. `notificationReplyClosesOnlyAfterSuccessfulSend()`
24. `overflowingNotificationClosesReplyDraft()`
25. `pendingSendKeepsTargetSessionDuringSwitch()`
26. `persistDebounceCancellationDoesNotFlushEarly()`
27. `promptStageIndicatorIsScopedToSelectedStream()`
28. `promptTurnFailedStateMarksAcceptedSendFailedImmediately()`
29. `replayCommitAllowsSourceNoLongerCurrentAtTerminalBoundary()`
30. `replayNavigationDuringPendingDoesNotDropTerminalEligibleNotification()`
31. `selectedSessionOAuthUsageClearsWindowsOnAuthoritativeBindingFailure()`
32. `sendBlocksStaleSyntheticSessionKey()`
33. `serverEchoCanonicalSessionMovesPendingPlaceholderThroughSeam()`
34. `sessionStatusRefreshKeepsIncomingAuthModeWhenPreservingStickyFields()`
35. `sessionStatusStickyDisplayMetadataIsKeyedPerStream()`
36. `snapshotRemovesChildStreamOmittedByServer()`
37. `streamingMessagesUpdateInPlace()`
38. `streamSnapshotReplacementFallback()`
39. `trackAdoptsUntrackedSessionAcrossSnapshots()`
40. `trackCandidatesLoadFromProviderEndpoint()`
41. `typingIndicatorMorphTargetIsNewAssistantMessageAndOneShot()`
42. `untrackRemovesLocalLinkOnly()`
43. `untrackUndoRestoresAdoptedSession()`
44. `userEchoWithoutDeviceIdDoesNotDuplicate()`

Every identifier has target `ClawlineTests/ChatViewModelTests`.

### 3. Exact files and ownership boundaries

R1 may edit only these files:

| File | R1 owns | R1 must not change |
| --- | --- | --- |
| `ios/Clawline/Clawline/ViewModels/ChatViewModel.swift` | Stored `incomingMessages` subscription, subscription initialization inside existing observation startup, one observer child task, and subscription teardown | Owner authority, lifecycle coordinator, `handleIncoming`, progress reducer, provider connection observer, service-event observer, message rules, or UI behavior |
| `ios/Clawline/ClawlineTests/ChatViewModelTests.swift` | One `activateAndAppear` helper and the affected fixtures' startup calls | Test declarations, assertions, expected values, timeouts, `TestChatService.emit`, or unrelated fixtures |

The code assignment stops and returns to spec review if it needs another file,
another production mutation seam, or an assertion change.

### 4. Required implementation shape

The code author must implement all of these clauses:

1. Store the stream returned by `chatService.incomingMessages` before the
   observation task begins.
2. Reuse the stored stream when activation joins or repeats. Do not create a
   second stream subscription.
3. Add one child to the existing observation task group. The child iterates
   the stored stream and calls existing `handleIncoming` for each value.
4. Clear the stored stream in `stopObservingLifecycle` with the other stored
   subscriptions.
5. Keep every new production-side line behind the existing owner checks. Do
   not add a test-only ownership exception.
6. Add one `@MainActor` test helper that awaits `activate(origin:)` and then
   awaits `onAppear(origin:)`.
7. Route the 44 affected fixtures through that helper where they currently
   depend on observation without activation. Do not change their assertions.

The code reviewer compares the exact diff with `9c8043ed`. The reviewer may
accept only the incoming-messages subscription and fixture-activation pattern.
The reviewer must reject the historical global ownership bypass and every
unrelated historical change.

### 5. Verification commands

Run every command from an owned clean Clawline checkout on Eezo with Xcode
26.6, an iPhone 17 Pro simulator, and iOS 26.5. Replace only the angle-bracket
paths and simulator identifier. Each command uses a new derived-data directory
and a new result-bundle path.

Direct causal command:

```text
xcodebuild test \
  -project ios/Clawline/Clawline.xcodeproj \
  -scheme Clawline \
  -destination 'platform=iOS Simulator,id=<IOS_26_5_IPHONE_17_PRO_UDID>' \
  -derivedDataPath <OWNED_DIRECT_DERIVED_DATA> \
  -resultBundlePath <OWNED_DIRECT_RESULT_BUNDLE> \
  -parallel-testing-enabled YES \
  -only-testing:ClawlineTests/ChatViewModelTests/incomingMessagesRoutePerStream \
  -only-testing:ClawlineTests/ChatViewModelTests/streamingMessagesUpdateInPlace \
  -only-testing:ClawlineTests/ChatViewModelTests/assistantIncomingAppendFiresHapticWhenVisibleAndForeground
```

Focused 44-family command:

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

Protected A7–A10 command:

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

1. S1 reaches independently reviewed-clean at its exact code revision.
2. R1 code starts from that reviewed-clean S1 revision.
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

**A1 — Evidence identity.** Given the cited S1 result bundle, when the reviewer
reads its summary, then it reports 164 tests, 120 passes, 44 failures, zero
skips, and zero expected failures. Every failed identifier belongs to the
section 2 ledger.

**A2 — No ownership signature.** Given the same result summary and complete
log, when the reviewer searches failure text for connection ownership, owner
displacement, non-owner guards, and ownership assertions, then no one of the
44 failures matches. The passing S1 and T320 ownership proofs remain passing.

**A3 — Provenance.** Given `9c8043ed` and merge `b0b853d3`, when the reviewer
compares `ChatViewModel.swift` and `ChatViewModelTests.swift`, then commit
`9c8043ed` contains the incoming subscription plus fixture-activation pattern
and the merge result contains neither. The R1 diff restores only that bounded
pattern and does not restore the ownership bypass.

**A4 — Direct cause.** Given the exact R1 code revision, when the coder runs
the direct causal command, then all three named tests pass with zero failures.

**A5 — Focused family.** Given the same revision and a clean derived-data
path, when the coder runs the focused command, then all 162
`ChatViewModelTests` pass. Each of the 44 section 2 identifiers is present and
passes. The result has zero failures, skips, and expected failures.

**A6 — Combined S1 boundary.** Given reviewed-clean S1 plus R1, when the coder
runs the combined command under normal parallel testing, then all 164 tests
pass with zero failures. Both T320 proofs pass. The result contains no owner
displacement and no duplicate incoming-message delivery.

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

**A11 — Protected tool-pill run.** Given the exact R1 revision, when the coder
runs the protected A7–A10 command, then all four named tests pass with zero
failures. The R1 diff does not touch a tool-pill seam.

**A12 — Exact file boundary.** Given the R1 code diff, when the reviewer lists
changed paths, then it lists only the two section 3 files. Within those files,
the diff contains no assertion, expectation, timeout, test-count, owner-rule,
or unrelated behavior change.

**A13 — Single delivery.** Given
`streamingMessagesUpdateInPlace`, when its fixture emits the partial and final
values for one message identifier, then the view model contains one message,
that message contains the final content, and the observer produces no
duplicate. Static review confirms that teardown clears the stored subscription
with the other observation subscriptions.

**A14 — Ordered review.** Given the full-green repair graph, when R1 code
starts, then S1 is already reviewed-clean. When S7 or S8 starts or resumes,
then R1 is already independently reviewed-clean with A4 through A13 green.

**A15 — S9 remains blocked.** Given a reviewed-clean R1, when the product owner
evaluates integration, then R1 alone does not authorize S9. S9 still waits for
all parent-spec repair slices, independent reviews, focused evidence, and the
parent full-gate conditions.

## Open Questions

None. The cited evidence, current-main reconciliation, and historical
provenance close the scope, causal, and ordering questions for this addendum.
