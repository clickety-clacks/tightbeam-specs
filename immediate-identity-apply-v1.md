# Identity apply: selected-session skill-file update and re-read nudge

**Status:** Candidate for proportionate independent exact-revision review. This
file is not implementation or rollout authority until that review returns
reviewed-clean for the exact commit and SHA-256.

**Work item:** `wi_ff222e95-ecd4-4ba0-83cc-ddd9e2301e07`

**Controlling authority:** Mike's decision
`dr_07bdef13-45ae-435f-bc79-b2dc6b0a5ebf`, recovered in direct message
`s_4867db6b-8fa8-4f81-b46a-b1806531463b` and final owner ruling
`att_6349ad2d-6d7e-4352-a333-6ff0218cfd79`. Owner ruling
`att_1e928176-63b6-4a39-b76b-fd7694c2311b` and producer verdict
`att_fb2292c8-1732-48fe-9582-d5b3b50dd81c` apply the same correction.
Target ruling `att_a3883546-7a75-4208-8823-5eeac314052a` fixes the two product
lines and indivisible landing rule.

Review adjudication `att_fdfbb9e5-a015-4645-94f4-bca5c43554a7` supplies two
source-reality corrections: apply covers materialized Tightbeam skill files
only, and neither target CLI currently exposes a per-session reload result. The
same adjudication accepts the existing `identityRevision` bookkeeping and a
revision-bearing ordinary prompt. This contract preserves both without treating
either as revision readback or strict confirmation.

The controlling decision says that identity apply does not merit transition
machinery. Tightbeam updates its owned skill files in a selected session's
existing harness home. Tightbeam then tells that session to re-read the files
on a best-effort basis. Apply supplies no strict confirmation that later work
uses the new guidance.

This authority supersedes owner ruling
`att_8aaff8d4-aba0-44c4-be19-7099eba49fce` where that ruling required atomic
replacement or revision readback. It preserves only the existing bookkeeping
that `att_fdfbb9e5` accepts. It drops all earlier strict identity-apply and
immutable-generation designs for this work item. Earlier commits, including
`f4b49223caa4a24842675cde57c74daa01983043`,
`94496236016aafff8dcc485799084d8df98ef01e`, and
`dd6ce9af9b6b3736014bd47d8d99b2f1bc1acd8c`, are not implementation or rollout
authority.

This file replaces only the `tightbeam identity apply` behavior in
`served-identity-home-projection-v1.md` and
`relearn-and-identity-apply-workflow.md`. Existing identity edit, relearn,
publication, skill-file ownership, authorization, credential, installation,
release, and two-YES laws remain authoritative. Where an older
file requires an atomic apply switch, adapter or model revision readback, an
identity generation, an adapter extension, or quiescence, this file supersedes
that requirement.

The authorized product lines are exactly `0.1.9` and `main`, where `main` is
the `0.2.0` integration line. Live `0.1.8` is locked and excluded.

## Goal

Update the Tightbeam-owned skill files of each selected existing session from
the current published identity. After a successful file update, record that
source in the session's existing `identityRevision` field. Then submit an
ordinary prompt that tells the session to re-read its Tightbeam skills.

This path is best effort. It does not prove which skill text is in the model's
current context. A running turn is not a refusal. Identity apply does not define
how a workflow obtains strict confirmation.

## Non-Goals

- Apply does not make an atomic switch across one file, multiple files,
  database state, prompt delivery, or model context.
- Apply does not add an effect ID, operation status, durable executor, recovery
  worker, adapter revision readback, or loaded-revision status.
- Apply does not create an immutable identity generation, generation ordinal,
  generation payload, reader graph, rollback protocol, or cleanup protocol.
- Apply does not create a projection root, additional skill root,
  process-global skill root, or generation-specific harness home.
- Apply does not add an adapter extension, adapter receipt, adapter-specific
  transition, sidecar, second runtime, or credential copy.
- Apply does not wait for organization, session, or turn quiescence.
- Apply does not cancel, replay, close, load, resume, restart, or rebind a
  running turn.
- Apply does not change non-file archetype guidance in a resident harness
  session.
- Apply does not claim that the agent received or obeyed the prompt.
- Apply does not claim that a running turn reads only old files or only new
  files.
- Apply does not change product files, user files, vendor state, credentials,
  transcripts, assignments, work items, authority, identity publication, or
  host placement.
- Apply does not edit, relearn, publish, reload, install, release, deploy, move a
  target, or execute a live identity change automatically.
- This specification does not authorize product implementation before review.
- This specification does not authorize a live identity command, schema
  mutation, Gibson product execution, installation, release, deployment, or
  target move.

## Terms

- **Live revision:** The Git object at `tightbeam/live` when the command resolves
  its input.
- **Selected session:** One active Tightbeam session named by the command. For
  `--all`, each session in the command's initial active-session set is a
  separate selected session.
- **Existing harness home:** The workdir and native harness-home structure that
  the selected session already uses. Apply does not create or replace it.
- **Tightbeam-owned skill file:** A skill file that the existing served-identity
  projection contract assigns to Tightbeam. Existing reserved `tightbeam__*`
  ownership and native Codex or Claude skill discovery rules continue to apply.
  This specification creates no path, root, manifest, or discovery mechanism.
- **Skill-file update:** The existing renderer and projection writer reconcile
  the selected session's Tightbeam-owned skill files from one live revision.
- **Revision stamp:** The selected session's existing `identityRevision` field.
  It records the source of the last skill-file update whose writer returned
  success. It is not adapter readback and does not prove model context.
- **Re-read nudge:** An ordinary Tightbeam prompt that tells the selected
  session that its Tightbeam skills changed and asks it to re-read them. Apply
  submits it after the revision stamp commits. Prompt acceptance, delivery,
  acknowledgment, and compliance are best effort.
- **Strict confirmation:** Proof that current model context uses the new
  guidance. An apply response, file observation, prompt result, agent
  acknowledgment, or revision stamp does not provide this proof.
- **Non-file archetype guidance:** Guidance supplied through a harness
  instruction channel, such as Codex developer instructions or a Claude system
  prompt. It is not a skill file.

## Assumptions

1. The existing identity renderer can render the elected Tightbeam-owned skill
   files from an exact Git object without reading mutable identity working-tree
   bytes.
2. The existing selected-session record identifies its active state, workdir,
   harness, archetype, and `identityRevision` field.
3. The existing served-identity projection contract identifies native skill
   locations and the reserved files that Tightbeam may write or remove.
4. The existing projection writer preserves every path that Tightbeam does not
   own. Its existing path-validation and error-redaction rules remain in force.
5. The ordinary prompt surface can accept a prompt for a selected session that
   has a running turn. Existing per-session ordering controls when the prompt is
   delivered.
6. Neither target CLI currently exposes a per-session reload command or a reload
   success result.
7. The existing identity-administrator check runs before the command reveals a
   selected session.

## Invariants

**I-01 — Selected-session scope.** Apply changes only Tightbeam-owned skill
files in each selected session's existing harness home.

**I-02 — Ownership stays unchanged.** Apply preserves product, user, vendor,
credential, transcript, harness-owned, and non-reserved skill bytes.

**I-03 — Running turns continue.** Turn state is not a precondition. Apply does
not signal, cancel, rebind, reload, or restart a running turn.

**I-04 — File observations are best effort.** A running process can read old
skill text before an update and new skill text afterward. It can observe a mix
of old and new files while the writer runs. A failed write can leave a partial
skill-file update.

**I-05 — File, stamp, then nudge.** Apply updates `identityRevision` only after
the projection writer reports a successful skill-file update. Apply submits the
re-read nudge only after that stamp commits.

**I-06 — Apply supplies no strict boundary.** No apply response, status value,
revision stamp, prompt event, or natural-language acknowledgment proves that
current model context uses the new guidance. This specification defines no way
to obtain strict confirmation.

**I-07 — Non-file guidance stays separate.** Apply leaves the resident harness
session's non-file archetype guidance unchanged.

**I-08 — Durable authority stays separate.** Skill text does not grant user,
device, role, assignment, or administrator authority. Apply changes none of
those rows.

**I-09 — Credentials keep one writer.** Apply does not read, write, link, copy,
rotate, harvest, or relocate a credential. It does not stop or replace the
shared runtime.

**I-10 — Cross-line parity.** `0.1.9` and `main/0.2.0` implement and test the
same observable contract. Live `0.1.8` implements none of this change.

## Architecture

### Command, selection, and file update

**R-01 — Existing command and authorization.** Both target lines shall accept:

```text
tightbeam identity apply (<session> | --all)
```

Apply shall expose no idempotency key, effect ID, operation ID, operation-status
form, revision selector, or reload flag. Help text shall call apply a
best-effort Tightbeam skill-file update and re-read nudge. It shall state that
apply cannot provide strict confirmation.

The existing identity-administrator check shall run before Tightbeam resolves
or reveals a selected session and before it writes a file. An unauthorized
caller receives the existing privacy-preserving refusal.

**R-02 — Selection and source.** A single-session selector shall address one
existing active session. `--all` shall capture one initial set of active session
keys. A session created after that capture is not selected. A session that
retires before its update shall receive no file update and no nudge. A selector
that names no session shall receive no file update and no nudge. Each target
line shall preserve its pre-change missing-session and retired-session result.

Apply shall resolve `tightbeam/live` once before target file I/O. Every selected
session shall use that Git object as its render source. Apply shall not accept a
revision argument, move `tightbeam/live`, or retarget itself after a later
publication.

**R-03 — Use the existing skill projection.** For each selected session, apply
shall call the target line's existing served-identity renderer and projection
writer for the Tightbeam-owned skill-file subset. It shall use that session's
existing workdir, harness, archetype, and native harness-home skill location.

The existing projection contract shall continue to control exact paths,
reserved `tightbeam__*` ownership, skill names, path validation, file modes, Git
exclusion, local or remote placement, and addition or removal of elected skills.
Apply shall add no path rule, root, home, manifest, discovery rule, adapter
input, write privilege, or projection format.

The writer shall preserve all non-owned paths. Apply shall not invoke a whole
home regeneration or a general product-file projection.

**R-04 — Preserve ordinary file semantics.** Apply shall not add an atomic
rename protocol, staging tree, transaction, snapshot, rollback, or recovery
mechanism around the existing projection writer.

An update can expose an old file before the writer changes it and a new file
afterward. Different skill files can expose different source revisions while
the writer runs. A failed update can leave some Tightbeam-owned skill files
changed and others unchanged. If the projection writer fails, apply shall
return a failure for that selected session and shall submit no nudge for that
attempt. The caller retries the ordinary command to reconcile the session.

### Nudge, running turns, and confirmation

**R-05 — Record the source after file success.** After the projection writer
returns success for a selected session, apply shall set that session's existing
`identityRevision` field to the R-02 live revision. If the writer or stamp
fails, apply shall submit no nudge for that attempt.

The stamp means only that the projection writer returned success for that
revision. The gateway shall not obtain the value from an adapter, vendor
process, model, prompt, or file watcher.

**R-06 — Submit one explicit nudge after the stamp.**
After the stamp commits, apply shall submit this exact ordinary prompt to that
session:

```text
Your Tightbeam-owned skill files changed to identity revision <revision>.
Re-read your Tightbeam skills before you continue work. This update does not
reload your current model context.
```

`<revision>` is the full R-02 Git object ID.

Apply shall not convert this prompt into adapter metadata. It shall not wait for
an answer or interpret an answer as confirmation. Ordinary Tightbeam prompt
ordering controls when the session receives the nudge.

If prompt submission fails, the skill-file update remains in place. The command
shall return a failure for that selected session. The revision stamp also
remains in place. The caller can retry apply or send the same ordinary prompt.
A retry can submit a duplicate nudge.

**R-07 — Running turns are allowed.** Apply shall not inspect a session lane,
turn ledger, adapter, or vendor child to decide whether it may update files. It
shall not return `turn_in_progress` because a selected session has a running
turn.

Apply shall not cancel, replay, close, load, resume, restart, or rebind that
turn. Text already in model context remains there. A later skill-file read can
observe new bytes. Apply promises no snapshot isolation inside the turn.

**R-08 — Keep retry behavior simple.** Apply shall create no durable apply
operation, effect row, effect query, executor lease, or recovery worker.

A disconnect, process crash, or lost response makes the outcome unknown to the
caller. The caller shall retry the ordinary command. Reconciliation through the
existing projection writer is the only file recovery. At-least-once nudges are
acceptable. Exactly-once nudge delivery is not promised.

**R-09 — Apply supplies no strict confirmation.** Identity apply and the current
target CLIs supply no strict confirmation. An independently available external
session-replacement or reload procedure, if any, is outside this contract.

This specification shall not define such a procedure's availability,
invocation, behavior, result, proof, or dependent-work sequencing. Apply shall
add no reload command, flag, protocol, receipt, model query, status field, or
revision readback.

### Guidance, status, and preserved boundaries

**R-10 — Treat non-file guidance separately.** Apply shall not change Codex
developer instructions, Claude system-prompt additions, or another non-file
archetype guidance carrier in a resident harness session.

The behavior of a reload, session replacement, or new-session construction is
outside this specification. Apply shall not promise that the current CLI exposes
such a lifecycle. Apply help, response, and status text shall not claim that a
skill-file update changed resident non-file guidance or current model context.

**R-11 — Keep bookkeeping distinct from readback.** The existing success
response shall remain:

```json
{
  "applied": ["agent:coder:one"],
  "identityRevision": "<live-oid>"
}
```

A session shall enter `applied` only after its skill-file update, revision
stamp, and prompt submission return success. `identityRevision` shall identify
the R-02 source revision. It shall not claim that an adapter, running turn, or
model context uses that revision.

Identity status shall describe `identityRevision` as the source of the last
successful Tightbeam skill-file update. The gateway shall not read a loaded
identity or skill revision from an adapter, vendor process, model, session
acknowledgment, or file watcher. The response and status shall expose no
loaded-revision or strict-confirmation field.

**R-12 — Preserve runtime, credentials, and authority.** Apply shall not invoke
credential code, home regeneration, onboarding, adapter installation, adapter
restart, adapter close/load/resume, harness switching, runtime replacement, or
authority mutation. The existing sole rotating-credential writer and shared
runtime topology shall remain unchanged.

### Release and handoff

**R-13 — Equivalent target-line implementation.** Exactly `0.1.9` and
`main/0.2.0` shall implement the same command, selection rule, source capture,
skill-file scope, file semantics, stamp meaning, response, status wording,
nudge text and ordering, running-turn behavior, retry behavior,
no-strict-confirmation disclosure, non-file-guidance disclosure, and prohibited
machinery.

Line-specific module names are not behavioral differences. Live `0.1.8` shall
receive no backport, feature test execution, target move, identity action, or
state mutation.

**R-14 — Review and indivisible landing gates.** Implementation shall not begin
until a fresh independent reviewer files reviewed-clean for this exact canonical
commit and file SHA-256.

The later implementation shall produce equivalent candidates and tests on both
target lines. The same independent review round shall cover both candidates.
The landing shall include both reviewed candidates in one authorized sequence
or neither candidate.

The existing release-cut gate, installation gate, and later live two-YES gate
remain in force. This specification authorizes no live identity edit or apply.

### Traceability

| Controlling ruling | Requirements | Acceptance |
| --- | --- | --- |
| Update selected-session Tightbeam-owned skill files | R-02 through R-04 | A-01, A-03, A-04 |
| Send an explicit best-effort re-read nudge | R-06 through R-08 | A-02, A-04 |
| Running turn is allowed | R-04, R-07 | A-02, A-03 |
| Apply supplies no strict confirmation; external procedures are out of scope | R-09 | A-05 |
| Existing revision bookkeeping is not readback or confirmation | R-05, R-09, R-11 | A-01, A-04, A-05 |
| No atomic, effect, generation, adapter, root, or quiescence machinery | Non-Goals, R-04, R-08, R-12 | A-04, A-07 |
| Treat non-file guidance separately | R-09, R-10 | A-05, A-06 |
| Exactly `0.1.9` and `main/0.2.0`; indivisible landing | R-13, R-14 | A-08 |

## Acceptance

**A-01 — Selected-session skill-file update (R-02 through R-05, I-01,
I-02).** Give two active sessions different workdirs and Tightbeam skill
sentinels. Publish revision B that adds, changes, and removes elected Tightbeam
skills. Apply only session A. Assert that session A's Tightbeam-owned skill
files reconcile to B through the existing projection writer. Assert that
session B and every non-owned path remain byte-for-byte unchanged. Assert that
apply creates no new root, home, manifest, or discovery rule. Assert that
session A records B only after the writer succeeds.

**A-02 — Running turn and nudge (R-05 through R-07, I-03, I-05).** Hold the
selected session's turn in running state. Apply B. Assert no turn-status
refusal, lane-boundary wait, adapter lifecycle call, cancel, close, load,
resume, restart, or rebind. Assert that the file writer runs and that its
successful return precedes the B stamp. Assert that the stamp precedes
submission of the exact R-06 prompt through ordinary prompt ordering.

**A-03 — Intended read boundary (R-04, R-07, I-04).** During a running turn,
read skill alpha before the writer changes it and skill beta afterward. Accept
complete old alpha and complete new beta. Inject a writer failure between two
skill changes and accept a partial Tightbeam-owned file update. Assert that
apply makes no atomic-snapshot or single-revision claim.

**A-04 — Failure and retry stay simple (R-04 through R-06, R-08).** Inject a
failure during the file update, after file success but before prompt
submission, and after prompt acceptance but before the command response. Assert
no nudge after a reported file-update failure. Assert no rollback of partial
skill files or the prior stamp, no adapter revision readback, no effect row, no
adapter receipt, and no automatic recovery protocol. Assert that a failed
writer leaves the prior stamp and submits no nudge. Inject a stamp failure after
file success and assert no nudge. Retry the ordinary command and assert file and
stamp convergence. Permit a duplicate nudge when the prior submission result
was lost.

**A-05 — Apply supplies no strict confirmation (R-09, I-06).**
Complete apply while the running turn retains old skill text. Assert that the
apply response, status, prompt result, and agent acknowledgment make no
strict-current claim. Assert that the B stamp describes only the last successful
skill-file update. Assert that apply exposes no reload form, result, receipt,
proof, or dependent-work sequencing.

**A-06 — Non-file guidance is separate (R-10, I-07).** Give a resident Codex
or Claude session A-only non-file guidance. Publish B-only non-file guidance and
changed Tightbeam skill files. Apply B. Assert that the skill files can change
while the resident non-file instruction carrier remains A. Assert that help,
response, and status text do not call the resident non-file guidance B. Assert
that apply exposes no non-file-guidance update or confirmation result.

**A-07 — Ownership and prohibited machinery (R-03, R-08, R-11, R-12, I-02,
I-08, I-09).** Invoke apply as an unauthorized principal and assert the existing
privacy-preserving refusal and no file, prompt, credential, adapter, or authority
effect. Plant product files, non-reserved skills, vendor state, transcripts,
credentials, and harness-owned state beside the existing skill projection.
After authorized apply, assert that only Tightbeam-owned skill files changed.
Source inspection on both target lines shall find no apply-specific atomic
switch, staging tree, adapter revision readback, loaded-revision status, effect
ID, operation query, durable effect store, immutable generation, projection
root, additional skill root, process-global skill root, generation-specific
home, adapter extension, adapter split, sidecar, quiescence wait, rollback
graph, credential write, or runtime replacement. Assert that the only revision
state changed by apply is the existing `identityRevision` field described by
R-05 and R-11.

**A-08 — Cross-line conformance and gates (R-01, R-13, R-14, I-10).** Run the
same focused fixture corpus against exact `0.1.9` and `main/0.2.0` candidates.
Assert byte-equal R-06 prompt text and logically equivalent selection, source
capture, skill-file scope, file semantics, running-turn behavior, retries,
non-file-guidance disclosure, no-strict-confirmation disclosure, and failure
behavior.
Review evidence shall name both implementation commits. Landing evidence shall
show one authorized both-line sequence. Negative evidence shall show no feature
commit or execution on live `0.1.8` and no implementation before exact-spec
reviewed-clean, installation, release, target move, or live identity action
before the existing gates and later two YES decisions.

## Open Questions

None. `dr_07bdef13-45ae-435f-bc79-b2dc6b0a5ebf` selects the simple,
best-effort skill-file-update-plus-nudge path. A stricter transition protocol
would require a new product decision and a separate specification. It is not a
refinement of this contract.
