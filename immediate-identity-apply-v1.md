# Identity apply: file update and re-read nudge

**Status:** Candidate for proportionate independent exact-revision review. This
file is not implementation or rollout authority until that review returns
reviewed-clean for the exact commit and SHA-256.

**Work item:** `wi_ff222e95-ecd4-4ba0-83cc-ddd9e2301e07`

**Controlling authority:** Mike's ruled decision
`dr_07bdef13-45ae-435f-bc79-b2dc6b0a5ebf`, recovered and restated by Mike on
2026-09-04. The ruling says that identity apply does not merit contract
machinery. Tightbeam updates its identity files, tells a live session to re-read
them on a best-effort basis, and uses an explicit session reload when a workflow
needs strict confirmation.

This authority drops the former strict identity-apply terms. It supersedes every
immutable-generation candidate for this work item, including commits
`f4b49223caa4a24842675cde57c74daa01983043` and
`94496236016aafff8dcc485799084d8df98ef01e`. Their readiness receipts and
review evidence do not authorize implementation or rollout.

This file replaces only the `tightbeam identity apply` behavior in
`served-identity-home-projection-v1.md` and
`relearn-and-identity-apply-workflow.md`. Existing identity edit, relearn,
publication, file ownership, session reload, authorization, credential,
installation, release, and two-YES laws remain authoritative. Where those
older files require an atomic identity switch, an identity generation, adapter
revision readback, or quiescence for apply, this file supersedes them.

The implementation targets the authorized `0.1.9` line and `0.2.0/main`.

## Goal

For each selected existing session:

1. update Tightbeam-owned identity files from `tightbeam/live`;
2. stamp the session with that source revision; and
3. submit an ordinary prompt that tells the agent to re-read the files.

This path is best effort. It does not prove which identity text is in the
model's current context. A running turn is not a refusal. A workflow that needs
strict confirmation reloads the session after the file update.

## Deliberate limits

- No effect ID, effect status, operation query, durable coalescing, executor
  lease, or effect store.
- No atomic switch across files, database state, and model context.
- No immutable identity generation, generation ordinal, generation payload,
  reader graph, rollback protocol, or generation cleanup.
- No adapter extension, adapter receipt, adapter revision readback, sidecar, or
  process-global additional skill root.
- No projection root, generation-specific harness home, second runtime, or
  credential copy.
- No organization-wide, session-wide, or turn-boundary quiescence.
- No claim that the agent obeyed the prompt or that a running turn uses only old
  or only new identity text.
- No automatic identity edit, relearn, publish, reload, cancel, replay, install,
  release, deploy, or target move.
- No change to product files, credentials, authority, transcripts, assignments,
  work items, or vendor-owned state.

This specification does not authorize a live identity command, schema mutation,
Gibson execution, product implementation, installation, release, deployment,
or target move.

## Terms

- **Live revision:** The Git object ID at `tightbeam/live` when apply resolves
  it.
- **Identity files:** Files that the existing served-identity contract already
  assigns to Tightbeam. The controlling ruling treats guidance updates as files
  in the existing harness-home projection. Existing reserved `tightbeam__*`
  ownership governs skill files. This specification creates no file location,
  root, home, manifest, or discovery mechanism.
- **File update:** The existing served-identity renderer and projection writer
  reconcile those Tightbeam-owned files from one live revision.
- **Revision stamp:** The selected session's existing `identityRevision` field.
  It records the revision used for the successful file update. It is not adapter
  readback and is not proof of model context.
- **Re-read nudge:** An ordinary Tightbeam prompt submitted after the file
  update and revision stamp.
- **Reload:** The existing explicit session lifecycle that reconstructs the
  harness session from current files. This specification does not add or change
  it.
- **Strict confirmation:** A successful reload boundary before later work. An
  apply response, revision stamp, delivered prompt, or natural-language
  acknowledgment is not strict confirmation.

## Requirements

**R-01 — Existing command.** Both target lines shall accept:

```text
tightbeam identity apply (<session> | --all)
```

Apply shall expose no idempotency key, operation ID, or operation-status form.
The help text shall call it a best-effort file update and re-read nudge. The
help text shall direct a caller to reload the session when strict confirmation
matters.

The existing administrator check remains in force. An unauthorized caller
receives the existing privacy-preserving refusal before Tightbeam reads or
writes selected-session state.

**R-02 — Selection and source.** A single-session selector addresses one
existing active session. `--all` takes one initial snapshot of active session
keys. A session created later is not selected. A session that retires before its
update is skipped through the existing safe refusal path.

Apply shall resolve `tightbeam/live` once before file I/O. Every selected
session uses that object ID. Apply does not accept a revision argument or move
the live ref. A later publication does not retarget the current command.

**R-03 — Update only existing Tightbeam-owned files.** For each selected
session, apply shall call the target line's existing served-identity renderer
and file-projection writer. That writer shall update only paths that the
existing projection contract assigns to Tightbeam. It shall preserve all
product, user, vendor, credential, transcript, and non-reserved skill bytes.

Apply adds no path rule, file format, root, symlink, home, adapter input, or
write privilege. The existing projection contract continues to control exact
locations, reserved `tightbeam__*` skill ownership, path validation, modes,
git exclusion, and local or remote placement.

The update has no multi-file atomicity promise. A running process can read an
old file before the writer changes it and a new file afterward. A failed write
can leave a partial file update. The command reports the existing safe apply
failure and the caller retries; it does not roll back or reconstruct an effect.

**R-04 — Stamp after file success.** After the file-projection writer returns
successfully, and only then, apply shall set the selected session's existing
`identityRevision` field to the resolved live revision.

The stamp means only “Tightbeam's file writer returned successfully for this
revision.” Tightbeam shall not read a revision from the adapter or model. If the
file writer or stamp fails, apply sends no re-read nudge for that attempt.

**R-05 — Submit one explicit nudge.** After the revision stamp commits, apply
shall submit this exact ordinary prompt to the selected session:

```text
Your Tightbeam identity files changed to revision <revision>. Re-read the
Tightbeam guidance and skills before you continue work. This update does not
reload your current model context.
```

`<revision>` is the full live Git object ID. Apply shall not convert this prompt
to adapter metadata or wait for an answer.

Ordinary Tightbeam prompt delivery controls when the agent receives the nudge.
If a turn is running, the prompt follows the ordinary per-session order. A
prompt-submission failure uses the existing safe apply failure path. The file
update and revision stamp remain in place.

**R-06 — Running turns and retries.** Apply shall not inspect a session lane,
turn ledger, adapter, or vendor child to decide whether it may update files. It
shall not return `turn_in_progress`.

Apply does not cancel, rebind, replay, close, load, resume, or restart a running
turn. Text already in model context remains there. A later file read can observe
new bytes. No snapshot-isolation promise applies inside the turn.

A disconnect, process crash, or lost response makes the result unknown to the
caller. The caller retries the ordinary command. File reconciliation and an
equal revision stamp are content-idempotent. A retry can submit a duplicate
re-read nudge. At-least-once nudges are acceptable; exactly-once delivery is not
promised.

**R-07 — Honest result and status.** The existing success response remains:

```json
{
  "applied": ["agent:coder:one"],
  "identityRevision": "<live-oid>"
}
```

A session enters `applied` only after R-03 through R-05 return successfully.
The response contains no operation, effect, generation, adapter-session, or
strict-confirmation field. On `--all`, an earlier completed target remains
updated if a later target fails. The caller retries to reconcile the selection.

Existing identity status shall describe `identityRevision` as the revision of
the last successful Tightbeam file update. It shall not describe the adapter,
running turn, or model context as verified current.

**R-08 — Reload when strict confirmation matters.** A workflow that needs
strict confirmation shall explicitly reload the selected session after apply
and wait for the existing reload lifecycle's normal success result before it
relies on the new identity for later work.

Apply success, the revision stamp, prompt acceptance, prompt delivery, and an
agent's acknowledgment are not substitutes for reload. If reload fails or is
unavailable, strict confirmation is unavailable. Apply adds no reload flag,
protocol, receipt, or revision readback.

**R-09 — Preserve runtime and credential ownership.** Apply shall not invoke
credential code, home regeneration, onboarding, adapter installation, adapter
restart, adapter close/load/resume, harness switching, or runtime replacement.
The existing single rotating-credential writer and shared-runtime topology stay
unchanged.

**R-10 — Cross-line parity and gates.** `0.1.9` and `0.2.0/main` shall implement
the same command, selection, file-first order, stamp meaning, prompt text,
running-turn behavior, retry semantics, response, status wording, and reload
rule.

Implementation shall not begin until an independent reviewer files a
reviewed-clean verdict for this exact canonical commit and file SHA-256. Later
implementation candidates on both lines require their normal tests and
independent review. Existing installation, release, deployment, target, and
two-YES gates remain in force. A one-line-only implementation, landing,
installation, or rollout is not authorized.

## Acceptance

**A-01 — File update, stamp, nudge.** With live revision B and a selected
session stamped A, change a Tightbeam-owned guidance file and reserved
Tightbeam skill file in B. Apply the session. Assert that the existing
projection contains B's bytes, the session records B, and the ordinary prompt
queue receives the exact R-05 prompt after the stamp.

**A-02 — Running turn is not a refusal.** Hold a turn in running state and apply
B. Assert no running-state check, lane-boundary call, adapter call, cancel,
close, load, resume, or runtime restart. Assert the file update and stamp
complete and the nudge follows ordinary prompt ordering.

**A-03 — Failure and retry stay simple.** Inject failures during file update,
after file success but before stamp, and after stamp but before prompt
submission. Assert no effect row, rollback, adapter receipt, or automatic
recovery. Retry the command and assert file/stamp convergence. Permit duplicate
nudges when the first submission result was lost.

**A-04 — Ownership is unchanged.** Plant product files, non-reserved product
skills, vendor state, transcripts, credentials, and harness-owned state beside
the existing projection. Apply a revision that adds, changes, and removes
Tightbeam-owned files. Assert every planted non-owned byte is unchanged and no
credential or runtime function runs.

**A-05 — Status is not confirmation.** Complete apply while a turn retains old
identity text. Assert the response and identity status describe B only as the
last successful file update and expose no loaded-revision or
strict-confirmation claim.

**A-06 — Reload supplies the strict boundary.** After A-05, run the existing
explicit reload lifecycle and wait for its ordinary success. Assert that a
workflow requiring strict confirmation relies on that reload boundary, not on
the apply stamp, prompt, or agent acknowledgment.

**A-07 — Prohibited machinery.** Source inspection on both target lines shall
find no identity-apply effect ID, operation query, durable effect store,
generation ordinal, generation payload, projection root, additional skill
root, adapter revision readback, adapter extension, sidecar, per-generation
home, quiescence wait, rollback reader graph, or credential write.

**A-08 — Cross-line conformance and gates.** Run the same focused fixture corpus
against `0.1.9` and `0.2.0/main`. Assert byte-equal R-05 prompt text and
logically equal selection, ordering, response, retry, status, and reload
behavior. Assert that no implementation starts before exact-spec
reviewed-clean, and no later install, release, deployment, target move, live
identity command, or one-line landing bypasses existing review and two-YES
gates.

## Traceability

| Mike's ruling | Contract | Acceptance |
| --- | --- | --- |
| Update the files | R-02 through R-04 | A-01, A-03, A-04 |
| Tell the live session to re-read, best effort | R-05 through R-07 | A-01 through A-03, A-05 |
| Reload when strict confirmation matters | R-08 | A-06 |
| No strict contract machinery | Deliberate limits, R-01, R-06, R-09 | A-03, A-07 |
| Preserve both lines and release law | R-10 | A-08 |

## Open questions

None. `dr_07bdef13-45ae-435f-bc79-b2dc6b0a5ebf` chose the simple,
best-effort file-update-plus-nudge behavior. A future strict identity-transition
protocol would require a separate product decision. It is not a refinement of
this contract.
