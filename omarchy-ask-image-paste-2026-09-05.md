# Omarchy Ask image paste

## Authority

Work item: `wi_10cba12a-30a5-4b69-8d46-5a1f479cd9e6`.
Owner: `asg_65fcb778-db77-4cca-b847-c9de302fd700`, product-owner:ask.
Mike approved “Use proposed behavior” on decision
`dr_5f23b38b-5ff7-40e7-8933-f21739e8e59f`, superseding `dr_30264895`.
This records the durable owner brief and that ruling; it adds no scope.
Mike's subsequent September 5 directive changes the test target to nacelle.
That directive supersedes every earlier osanwe test-location instruction.
Repository baseline: `a6351b0e5fb0816dbaccc1180c318bd955196023` (v0.7.0).

## Spirit

Ask is “one box, two jobs”: a small launcher and a way to ask the user's
system agent a question. Image paste lets the user show that agent what they
mean without leaving the composer. Removable previews make the outgoing
content visible. Failures must not lose the user's submitted draft.

“Zero residue” applies to Ask's own conversation data: each window owns its
ephemeral conversation, attachments, and bridge. Pinning keeps that same
conversation. Closing it clears its app-owned data. Ask neither promises to
erase harness-owned logs nor alters source images or the system clipboard.

Success requires actual image understanding by both system Codex and Claude,
preserved ordinary text paste and text steering, safe retry, and independent
overlay/pinned conversations. Keep the existing permission and system-default
harness policy. No image service, archive, bundled-harness fallback, adjacent
regex/diagnostic repair, or broader composer redesign belongs in this slice.

## Approved behavior

Mike's September 6 clarification below supersedes any earlier wording that
could imply single-image prompts or disposal of submitted transcript images.

1. Accept pasted screenshot/browser image data and copied image files, with
   removable thumbnails. Repeated paste appends multiple images to the same
   draft. Preserve ordinary text paste. Send all images and text together over ACP.
2. Attachments suppress launcher results and activation. Image paste in file,
   repository, or window search mode (`@`, `^`, `%`) leaves that mode and keeps
   its query as ordinary prompt text. Removing the last draft image restores
   normal search. Return with attachments sends to the agent.
3. Submitted thumbnails stay visible and locked during the answer. Successful
   completion clears composer attachments only. Submitted images remain visible
   alongside their message for the lifetime of the chat. Composer clearing must
   not delete images or resources still needed by the transcript. Any failure, including one
   after partial output, preserves original text and images for explicit retry.
   Never automatically resend or overwrite later typed or steering text.
4. Reject new image paste during an active answer with a useful wait message.
   Existing ordinary text steering and text paste continue unchanged.
5. Accept PNG, JPEG, GIF, and WebP. Limit each image to 5 MiB and the aggregate
   to 20 MiB. These are app policy limits, not assertions of provider limits.
   Give useful unsupported-format, size, and capability errors. Do not silently
   resize or convert images.
6. Keep data and asynchronous clipboard results owned by their conversation.
   Pinning retains ownership; a result arriving after close cannot populate a
   new overlay. Clean resources only when no draft, in-flight send, or transcript
   needs them, or when the conversation closes. No durable transcript archive.

## Adapter launch and existing selector

Mike explicitly includes correction of the intrusive pre-existing recovery panel
and the missing ACP adapter launch. His screenshot reports `codex-acp ENOENT`
at the installed adapter path, alongside “Start new session” and “Choose harness”.
That error identifies a missing adapter executable; it does not establish that
the system Codex harness is missing. Diagnose the actual install/launch failure
on the authorized nacelle test target and fix it there. Do not bundle the system
harness again or conceal the failure with extra controls. Necessary errors must
be concise and user-facing, without raw internal paths.

Ask and its Super+comma harness selector were already delivered. Preserve that
existing selector and shortcut unchanged; image paste does not expand it.
Address the unwanted duplicate harness-selection/recovery panel controls without
removing the selector. These additions predate image work; do not attribute their
origin to image paste. This bounded correction is not a broader UI redesign.

## Bounded implementation

The existing composer/bridge/ACP architecture remains authoritative. A
short-lived clipboard reader is justified by the recorded finding that
Quickshell's clipboard interface exposes text while image paste needs MIME and
raw bytes. Use the recorded one-shot reader design, without a daemon, service,
archive, or temporary file. Existing lifecycle and permission invariants in
`docs/architecture.md` continue to govern.

## Evidence and acceptance

Nacelle is the test target for this project and image-paste work, including
live desktop and system-harness testing. Do not perform those tests or deploy
test builds on osanwe. Use a worker-owned checkout and a supported isolated
desktop on nacelle. Preserve shared source and installed plugins except for
Mike's explicitly authorized nacelle adapter install/launch correction above.

Discover nacelle's actual checkout paths and environment before testing. The
historical osanwe source path `/home/mike/Projects/omarchy-ask` and installed
plugin path `/home/mike/.config/omarchy/plugins/clickety-clacks.ask` are handoff
context only; they are not nacelle paths. Record the actual host, paths,
candidate identity, desktop and system-harness prerequisites in the evidence.

If nacelle access or prerequisites are missing, report the exact failed probe
or missing prerequisite. Do not substitute osanwe or another host, assimilate
a host, reconfigure it, or change credentials. The location directive does not
authorize general deployment or other live-state mutation. The subsequent
adapter install/launch correction is authorized only on the nacelle test target.

Require fresh real image-understanding responses from system Codex and Claude,
including actual understanding of multiple distinct images in one prompt,
not readiness, capability advertisements, or metadata echoes. Cover screenshot,
browser, and file-manager copies; removal and retry; overlay and pinned mode;
ordinary text paste and steering; failure retention without loss of newer text;
close/pin ownership and late clipboard results. Verify repeated-paste
append/removal, all images sent together, rendered
transcript images after composer clearing and later turns, failure/retry resource
retention, pin/unpin, and cleanup after conversation close. Include adapter-launch
success, concise failure behavior, and unchanged Super+comma selector behavior.
Earlier single-image evidence alone does not satisfy this clarified acceptance.
Keep screenshots free of private
content. Record dated commands/results, exact commit/diff hashes, limits, and
which checks are new versus historical. `docs/model-verification.md` and
`docs/reviews/2026-09-04-native-attention.md` are historical baselines only.
Earlier osanwe test results remain historical handoff evidence and do not
satisfy the required fresh nacelle desktop and system-harness acceptance.

Mike's theme feedback: preserve the existing theme-aware Ask appearance in
both popup and pinned windows; do not introduce a hardcoded black background.
Classify the reported black background against the actual nacelle candidate
and runtime as temporary test styling, theme-loading regression, or intentional
change, using evidence rather than appearance alone. Correct an image-work
regression within this slice. Include private-content-free themed popup and
pinned screenshots in acceptance. This is not a broader visual redesign.

Implementation assignment: `asg_9acc5352-3b86-4df6-8c29-a6957d32d06c`.
Orchestrator: `asg_a12431d5-bd1e-4443-9e39-35e3ce94670a`.
Exactly one fresh independent linked review follows the author's honest
passing-test receipt for the immutable candidate. The owner judges the spirit
summary before main integration. Partial slice tests are not final acceptance.

## Boundaries

No automatic release, version bump, tag, release workflow, disruptive deployment,
host assimilation/reconfiguration, credential changes, service/schema changes,
or live-state mutation. No code execution on gibson. This approval changes none
of those boundaries. The feature is not complete until its acceptance evidence
and independent review support the actual user outcome.
