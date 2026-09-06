# V9 identity transition design

Status: bounded reuse design under the owner's `rule-reuse-boundaries` ruling.
No implementation or live action is authorized by this document. No product tests
ran during its preparation. One independent design review follows the writer's
cold digest; this document does not claim that review has passed.

Decision `dr_c41118fc-3871-4024-8064-2f6d2d1e6036`, relayed by the orchestrator
on 2026-09-05, resolves Q1–Q3: reuse relearn after separately authorized installed
input preparation; retain retired old-reviewer rows for historical access and
create explicit successors; accept merge-abort recovery plus limited
post-publication repair. **A new seam is forbidden.** The ruling selects this
design's boundary; it authorizes neither installation nor live rollout.

Authority: decision `dr_bfa7429e-9e59-49a2-8871-dadfdc0370f8`; work item
`wi_fc47cb46-cfc4-45c6-9b74-def1522e5ebf`; design assignment
`asg_8e8a82b0-ea3d-408a-9090-f935ee8ff9c7`. The canonical brief is
[`v9-identity-transition-design-brief.md` at 3add567](https://github.com/clickety-clacks/tightbeam-specs/blob/3add567f2847b38505747799995b8f09a00e5dad/v9-identity-transition-design-brief.md),
SHA-256 `6e0dbc15fccecb7216df87ab4afc1c9ed467892ff65c98dbf940d5877127693f`,
artifact `art_0741d994`. That object lives on the brief's branch, not in this
design's allocated main tree. It remains the read-only input; this document does
not land or revise the brief.

## Goal

### Spirit — carried verbatim from the brief

Finish the existing outcome: land the reviewer restructure on both product branches, then make it available to the org. The source half is complete. The remaining outcome is a supported, reviewable way to publish that exact catalog change, select its recipients, and recover if the publication fails. Preserve unrelated identity customizations and existing work.

Success means an operator can inspect a complete command-and-input packet and understand what will change, which sessions are affected, what remains unchanged, and how recovery works. A packet that omits unsupported steps is not complete. No new identity architecture is implied.

### Bounded result

Reuse the existing bundle import, Git merge, publication, and explicit session
refresh seams within the prerequisites and limitations the owner accepted.
The intended catalog has `reviewer-code` and `reviewer-spec`, with one
`review-common.md` include, and no spawnable `reviewer` archetype.

Catalog deletion is already expressible through a bundle relearn. The deliverable
of later preparation is the finite input/command/fixture packet specified here.
The installed old bundle cannot supply V9, and exact catalog reversal is outside
the ruled recovery promise. Actual session choices and installation authority are
later packet inputs; this design selects no live recipients.

## Non-Goals

No V9 source edits; new reviewer behavior; new publication, generation, activation,
atomicity, runtime-readback, migration, audit, or identity architecture; automatic
reviewer classification; fleet-wide apply; historical backfill; session override
erasure; retirement of unfinished work; or live execution during design.

No edit to closed identity recovery or `asg_1295062f`. No installation, release,
deployment, service, adapter, or credential work. No second-YES request. This design
does not revive the reset/reload machinery described in older identity workflow
specs: the brief expressly preserves the accepted simple file-refresh behavior.

Operating pattern introduced: none. This design composes existing commands for
this transition and adds no command or interface.

## Terms

- **Accepted V9 source:** Tightbeam main commit
  `dbe46a8fbabc0d81460c8239dbf54ac8989d6b0b` and maintenance commit
  `7ccf653185fa9b9e26610dec8909eae49b594862`; source completion is `att_7488ce2d`.
- **Installed input:** the gateway application's seed and shipped bundle files.
  A checkout, a specs artifact, and a CLI help listing are not this input.
- **Identity tree:** the org's Git repository at `<base>/identity`; `main` holds
  customizations, `tightbeam/upstream` holds imported material, and
  `tightbeam/live` identifies published content. These three names are existing
  implementation names, not new transition records.
- **Receipt:** `kungfu/agentic-engineering/installed.toml` in that tree. Its `paths`
  array records bundle custody. It contains no source-version or content-hash pin.
- **Publication:** advancing the existing live reference and reloading catalog,
  rails, and rules. This is separate from refreshing session files.
- **Refresh:** existing `identity apply <exact-session-key>` file projection,
  followed by its stamp and, for a resident session, a submitted reread prompt.
  It does not prove that a model read the files or changed its current context.
- **Recovery:** an owner-approved supported operation from a named observed failure
  state. “Abort an uncommitted merge,” “restore usable content,” and “restore the
  exact prior catalog” are distinct claims.
- **Roster:** a later owner-reviewed document listing exact session keys and
  disposition, with evidence and authorization. It is an input document, not a
  new database table or automatic classifier.

## Assumptions

1. The accepted source pair remains authoritative. Neither current main drift nor
   an installed package version elects a replacement source revision.
2. The inspected source is evidence of available implementation to reuse, not proof
   that the installed BEAM files were built from that exact commit. The future
   fixture run must use the exact runtime candidate whose behavior is claimed.
3. Separately authorized installed-input preparation supplies the reviewed bundle
   to the real gateway import path. That preparation and its authority remain
   outside this assignment; a local checkout does not satisfy the prerequisite.
4. The future packet is prepared from fresh identity Git objects and an exact
   installed-input inventory. Snapshot counts cannot authorize session changes.
5. Files outside the V9 delta can contain org changes and later shipped changes.
   A clean Git merge is not evidence that either category was preserved as intended.

## Invariants

**I1 — Bounded content.** The preparer accounts for each changed path in A2 below
and preserves bytes outside the approved set. Given an unrelated local guidance
fragment, when the candidate is compared with the captured before tree, then its
path, mode, and bytes match. A broader imported delta makes the packet unready;
the preparer does not silently accept it.

**I2 — Preserve customization deliberately.** The preparer transplants the old
reviewer's unrelated manifest settings into the two proposed manifests and records
any ambiguous guidance clause for owner disposition. Given the inspected old
manifest, then `where`, model preferences, `no-testing-on-gibson.md`,
`specs-home.md`, `integration-targets`, and `tightbeam-atc` survive unless the owner
explicitly changes them. Copying the shipped manifests wholesale fails this check.

**I3 — Preserve work and history.** Publication changes no session archetype,
override, role, assignment, transcript, or harness-history row. Given an existing
reviewer with custom overrides, then publication leaves those values unchanged.
Any later retirement or successor assignment is explicit in the roster and uses
the existing lifecycle. Historical-only access for retired reviewers satisfies
the ruled requirement; there is no implicit repoint or runnable compatibility alias.

**I4 — Select recipients explicitly.** Given two stale sessions and a roster that
selects one, then the packet contains only that session's apply command. Age,
staleness, name resemblance, and counts do not select the other session.

**I5 — Separate publication and refresh truth.** Given a published revision and a
failed refresh, then the report says publication succeeded and identifies the
failed session. It does not describe the publication as rolled back or the session
as having adopted new model instructions.

**I6 — Honest evidence.** The packet binds expected file bytes by SHA-256 before
execution and records the observed Git OID afterwards. Given identical fixture
content committed at different times, differing commit OIDs do not fail the content
check. A file stamp proves only the writer's reported success for those files.

## Architecture

### A1. Inspected implementation and installed custody

Source citations below use immutable Tightbeam main
`f4b68f078d3767cede71572aa88c4516372867cf` (the read-only clone tip). Its
`lib/tightbeam/identity.ex` is byte-identical to accepted V9 main's file:
SHA-256 `e36cf451a9255f1921b51b843884bff2602085d84eaaa9c0295431ea57341c0e`.
The maintenance file differs; its SHA-256 is
`b32ed2f168fb45d509827a3aca02f7834279addb7caa499924d590b27090d7d0`.
Do not infer cross-line runtime equivalence from the guidance pair's acceptance.

| Fact | Inspectable evidence | Consequence |
|---|---|---|
| Guidance edit accepts a fragment name; it need not already be an archetype. Manifest edits create or replace a TOML file. Removal is limited to skills. | [identity.ex:373–395, 1316–1352](https://github.com/clickety-clacks/tightbeam/blob/f4b68f078d3767cede71572aa88c4516372867cf/lib/tightbeam/identity.ex#L373) | `identity edit review-common --file ...` can supply the shared include. There is no existing CLI manifest/guidance deletion inverse. |
| Learning an already-receipted bundle is a no-op. Unlearn deletes its entire receipted set. | [identity.ex:447–520](https://github.com/clickety-clacks/tightbeam/blob/f4b68f078d3767cede71572aa88c4516372867cf/lib/tightbeam/identity.ex#L447) | Unlearn/relearn of the engineering bundle is not a bounded reviewer replacement. It removes coder and owner material too. |
| Relearn imports seed plus each learned bundle, then performs a three-way Git merge and refreshes receipts. | [identity.ex:658–709, 725–867, 1113–1147](https://github.com/clickety-clacks/tightbeam/blob/f4b68f078d3767cede71572aa88c4516372867cf/lib/tightbeam/identity.ex#L658) | Shipped deletions can remove old reviewer files; modified deletions become conflicts. There is no CLI argument to select an arbitrary captured bundle or restrict import to V9. |
| Abort requires a pending merge. Resolve validates, stages, and commits its resolution. | [identity.ex:682–709](https://github.com/clickety-clacks/tightbeam/blob/f4b68f078d3767cede71572aa88c4516372867cf/lib/tightbeam/identity.ex#L682) | Conflict resolution is the existing exception for file edits inside identity. It is not authority to make raw Git edits outside a real conflict. |
| Publication creates a candidate before advancing live; the ref move precedes law reload and the final accepted marker. | [gateway.ex:3637–3698, 3793–3873](https://github.com/clickety-clacks/tightbeam/blob/f4b68f078d3767cede71572aa88c4516372867cf/lib/tightbeam/gateway.ex#L3637), [identity.ex:1525–1549](https://github.com/clickety-clacks/tightbeam/blob/f4b68f078d3767cede71572aa88c4516372867cf/lib/tightbeam/identity.ex#L1525) | A failed response is not proof that live stayed old. No new atomicity promise follows from existing marker code. |
| Spawn selects from the currently loaded archetypes and rechecks that the archetype exists when creating the row. | [gateway.ex:5630–5657, 5832–5841](https://github.com/clickety-clacks/tightbeam/blob/f4b68f078d3767cede71572aa88c4516372867cf/lib/tightbeam/gateway.ex#L5630) | Another authorized actor can spawn during the separately published prefix. The operator's roster check does not prevent that race; A4 requires a later recensus and stop outcome. |
| Repoint accepts retired sessions (and special permanent sessions) but clears overrides and identity stamps. | [gateway.ex:3901–4008](https://github.com/clickety-clacks/tightbeam/blob/f4b68f078d3767cede71572aa88c4516372867cf/lib/tightbeam/gateway.ex#L3901), [org.ex:1396–1430](https://github.com/clickety-clacks/tightbeam/blob/f4b68f078d3767cede71572aa88c4516372867cf/lib/tightbeam/org.ex#L1396) | Repoint is not a preservation-safe automatic classification operation. |
| Unlearn checks even retired session references; ordinary relearn has no corresponding reference-release call. | [org.ex:1434–1536](https://github.com/clickety-clacks/tightbeam/blob/f4b68f078d3767cede71572aa88c4516372867cf/lib/tightbeam/org.ex#L1434), [gateway.ex:3670–3788](https://github.com/clickety-clacks/tightbeam/blob/f4b68f078d3767cede71572aa88c4516372867cf/lib/tightbeam/gateway.ex#L3670) | Relearn's ability to delete a manifest does not prove existing sessions remain operable. |
| Retirement keeps history; apply selects active rows and writes files before stamps and reread submission. Status renders the current archetype for active sessions. | [org.ex:971–1040](https://github.com/clickety-clacks/tightbeam/blob/f4b68f078d3767cede71572aa88c4516372867cf/lib/tightbeam/org.ex#L971), [gateway.ex:4018–4050, 4194–4330](https://github.com/clickety-clacks/tightbeam/blob/f4b68f078d3767cede71572aa88c4516372867cf/lib/tightbeam/gateway.ex#L4194) | Do not delete the manifest while active reviewer sessions depend on it. Retired transcript access and runnable-session access must be distinguished. |

Read-only installed observations on Gibson, 2026-09-05:

- CLI resolves to `/home/mike/.local/lib/node_modules/tightbeam/bin/tightbeam`;
  its version and package metadata say `0.1.8`. This version string is not a build
  commit pin. The inspected installed Identity BEAM SHA-256 is
  `f878927f5bb6668f4738a2d7fd43684a05eff9cc7352c6487e2d5344c433a0c0`.
- Installed bundle root is
  `/home/mike/.local/lib/node_modules/tightbeam/release/lib/tightbeam-0.1.8/priv/kungfu/agentic-engineering`.
  Its `archetypes/reviewer.toml` exists, SHA-256
  `6b1db43faa72f9c525d6a997e15780ef31cf5187aee46842a3882bedadf9af53`.
  `tightbeam kungfu list` advertises that bundle; it does not attest that it is V9.
- Identity `main` and `tightbeam/live` both name
  `5110d5d0ca9da61aa32d37bc93c846ba51c0cfff`; upstream names
  `9b65f1403b407908f464330ce860a4f7c7763fe7`. The tree is clean.
  No command changed those refs during design.
- The live receipt SHA-256 is
  `573ad71ed94ee53be4ddd0913b171d5b0d694e40afd515566dc3bb9f3fb626f9`.
  It owns `archetypes/reviewer.toml`, `guidance/reviewer.md`, both obsolete skill
  files, and the other engineering paths. The live old reviewer manifest SHA-256
  is `02bfc8b64e6b6c9368dc8f160f845b634c9c7c0fe702bce541a3112e391fb7d1`.
- `git diff tightbeam/upstream tightbeam/live` shows org edits to the old reviewer
  manifest, guidance, both obsolete skills, shared skills, and rules. The old
  manifest and guidance therefore require explicit preservation decisions when
  an updated bundle deletes them. Git rename detection is not that decision.

These observations correct the earlier help-only inference that no catalog deletion
path exists. They also explain why running relearn now would not be a proved V9
transition. They do not identify the exact source of the running gateway from a
package version alone.

### A2. Exact intended identity delta

Map the accepted main commit's changes beneath
`priv/kungfu/agentic-engineering/` into identity paths. The bundle mapper relocates
bundle-level documents beneath `kungfu/agentic-engineering/`; other paths retain
their relative names. This is the closed initial allowlist, not permission to
replace whole files without preserving org edits.

| Operation | Identity paths |
|---|---|
| Add | `archetypes/reviewer-code.toml`, `archetypes/reviewer-spec.toml`; `guidance/review-common.md`, `guidance/reviewer-code.md`, `guidance/reviewer-spec.md` |
| Remove | `archetypes/reviewer.toml`, `guidance/reviewer.md`; `skills/reviewing-code/SKILL.md`, `skills/reviewing-specs/SKILL.md` |
| Amend V9 references only | `guidance/coder.md`, `guidance/orchestrator.md`, `guidance/product-owner.md`, `guidance/spec-writer.md`, `guidance/subtraction.md`, `guidance/wisdom-core.md`; `kungfu/agentic-engineering/capabilities.md`, `kungfu/agentic-engineering/preferred-models.md`; `rules/engineering.toml`, `rules/verification.toml`; `skills/committing-and-pushing/SKILL.md`, `skills/feature-cycle/SKILL.md`, `skills/spec-conformance/SKILL.md`, `skills/spec-handoff/SKILL.md`, `skills/spec-homing/SKILL.md` |
| Update custody through existing receipt code | `kungfu/agentic-engineering/installed.toml` |

The receipt removes deleted paths and adds installed paths under the existing
`current_bundle_receipt` rule. A newly added path customized during a conflict may
not match upstream and therefore may not become bundle-owned; the packet records
that actual result rather than forging receipt membership. Its recovery assessment
must include that ownership difference.

The new manifests preserve the old reviewer's unrelated settings and remove these
five elections: `reviewing-code`, `reviewing-specs`, `spec-conformance`,
`review-for-completeness`, `review-for-yagni`. Only the first two skill directories
are deleted. The other three remain present and unelected by the reviewers. Other
archetypes' elections are preserved; an unexpected remaining elector of a removed
skill is a blocking input finding, not permission to edit another manifest.

The three guidance bodies remain the accepted exact V9 bytes:

| File | SHA-256 |
|---|---|
| `review-common.md` | `72b595ecd7480d1b1f22a5b985552e80ce20b6fa954261a78c71fc83b06ca5ea` |
| `reviewer-code.md` | `93162275f788d11041310b11afd161197715e32cad8b87223f10b018ff80b73f` |
| `reviewer-spec.md` | `8479006d38fc699eae9324d66dce4a10eebf8d13c771dd2e04cd4a36799d7b19` |

Unrelated old guidance belongs in existing retained fragments or manifest guidance,
not inside those fenced bodies. A clause whose placement or applicability changes
the reviewer's behavior needs an owner ruling before deletion or transplantation.
Preserve the pooled completion-review semantics; apply only the accepted V9
reference changes in the rules. Preserve any org-local rule's unrelated clauses.
No quick-fix rule is introduced.

Git import/merge commits and their existing publication markers are the only new
publication records. No transition table is proposed. Existing law reload updates
its existing in-memory catalog. Session stamp changes arise only from separately
selected apply commands; lifecycle changes arise only from roster actions.

### A3. Supported sequence for the later approved packet

1. The preparer captures the exact installed runtime, seed, learned bundle inputs,
   before refs, receipt, permitted output bytes, and roster. The fixture exercise
   proves the complete resulting delta; it does not authorize live execution.
   Separately authorized installed-input preparation must finish before this
   sequence uses the gateway's relearn command.
2. Under later live authority, the operator publishes the five reviewed additions
   through existing edits in this order. Each command's file is an exact hashed
   packet input; the two manifests contain the preserved settings from I2:

   ```text
   tightbeam identity edit review-common --file <packet>/review-common.md
   tightbeam identity edit reviewer-code --file <packet>/reviewer-code.md
   tightbeam identity edit reviewer-spec --file <packet>/reviewer-spec.md
   tightbeam identity edit reviewer-code --manifest --file <packet>/reviewer-code.toml
   tightbeam identity edit reviewer-spec --manifest --file <packet>/reviewer-spec.toml
   ```

   Observe each result before the next edit. A prefix can leave old and new
   archetypes present together; it is recorded partial preparation, not the final
   catalog. This ordering ensures that customization does not depend on Git
   producing a conflict: a clean relearn otherwise publishes automatically.
   Existing target files at packet-capture time require their exact before hashes
   and content reconciliation; do not blindly recreate or overwrite them.
3. The owner resolves each old-reviewer customization and selects session
   dispositions. The operator stops the rollout if an active reviewer still needs
   the retiring catalog name or a default setting still selects it. An active
   session's retirement requires completed or lawfully transferred obligations.
   The operator creates, assigns, and wakes no successor during this partial
   five-edit prefix. A successor's first turn must follow step 7 below; the prefix
   does not yet contain the final V9 rules and cross-role references. An old
   obligation may transfer to an existing owner only when that recorded handoff
   can safely wait for the final publication and later successor. Otherwise the
   old holder finishes the obligation before retirement. The old row's overrides
   remain intact; they are not erased by repoint or silently copied into another
   role.
   Retire the explicitly selected old reviewers before removing their manifest;
   retain their original archetype fields, overrides, and history. If the default
   setting names `reviewer`, the packet names an owner-selected installed replacement
   and the existing `config set default-archetype <name>` command before publication.
   Record that exact setting change as a conditional roster effect, not a new
   catalog mechanism. No default-setting change is implied by this design alone.
4. The operator invokes `tightbeam identity relearn`.
   A clean merge publishes immediately; this command is not a dry run. If there is
   a real conflict, the operator applies only the reviewed resolution files and
   stages those resolutions in the identity tree, then invokes
   `tightbeam identity relearn --resolve`. `--abort` is the supported way to
   abandon that pending merge. Do not manufacture a conflict to obtain an editor.
5. The operator records the resulting live OID, catalog, file-content comparison,
   and receipt. Any difference from the approved content packet ends this sequence
   at the corresponding recovery state below. After these checks pass and before
   any refresh or successor action, the operator performs A4's post-publication
   recensus. A raced or unproven roster stops this sequence at A5; successful
   publication alone does not permit steps 6–7.
6. The operator invokes `tightbeam identity apply '<exact key>'` for each roster
   entry selected for refresh. Publication remains recorded independently from
   each file-refresh result. If a selected refresh fails, the sequence stops at
   A5's corresponding outcome before creating any successor. An explicitly empty
   refresh selection needs no apply command. Apply cannot change an old session's
   archetype into a new one.
7. Only after final relearn succeeds, step 5 verifies exact content, receipt, and
   the post-publication roster,
   and step 6 completes the selected refreshes, the operator creates each
   authorized successor using ordinary spawn, then assign, then wake. The new
   session provisions from the verified final catalog. The roster records its
   predecessor and successor keys, explicit role/work handoffs, and any prior
   per-session customizations the owner elects through supported spawn inputs.
   This ordering governs the successor's first turn; a later apply is not a
   substitute for it and cannot repair an already composed partial-prefix context.

The preparation prefix's revisions and final relearn revision are separately
recorded. The operator uses the prefix only to create identity files; concurrent
session creation is checked under A4 rather than presumed absent. Receipt
membership follows the actual merge rule in A2, including for customized manifests
created in the prefix.
This sequence does not make publication of the five additions and subsequent
deletions atomic.

This sequence has no supported CLI selector for an arbitrary saved bundle or
selective V9 import. If the actual shipped inputs import unrelated changes, the
packet fails I1. The author does not prescribe an unbuilt `--from`, catalog-remove,
batch-edit, or named-revision rollback command to fill that gap.

### A4. Session selection and preservation

The later roster has one row per affected session and an explicit excluded set:

`sessionKey | owner | state | archetype | roles | open assignment IDs | override
content hash | disposition | successor archetype/key (if any) | reason/evidence |
owner ruling | exact command(s)`.

Allowed dispositions are `keep-unrefreshed`, `refresh-same-archetype`,
and `finish-or-transfer-then-retire; create successor`. A retired row is
`retain-history`, with no repoint or apply command. A code/spec ambiguity is
`unresolved` and blocks that row's transition. Shared-subject work does not imply
one permanent reviewer type; the owner can name separate successor obligations.

The operator re-reads the named row and its obligations before its command. A
changed state or new obligation returns that row to its owner for reconciliation.
This is an operator procedure, not an atomic admission fence. Final catalog-removal
publication is not ready while an old reviewer remains active. `keep-unrefreshed` therefore applies
to unaffected archetypes, not an active row whose manifest will be deleted.
Retirement side effects and historical-only access are the accepted boundary.
Before final catalog-removal publication, the roster accounts for each observed active `reviewer` row;
the operator reconciles any new old-reviewer row instead of proceeding from a
stale census. No fleet freeze or automatic classification is introduced.

After final relearn and exact content/receipt verification, and before any refresh
or successor action, recensus the existing session rows and their assignment,
wake, and turn records against the approved roster. Account for active `reviewer`
rows and `reviewer-code`/`reviewer-spec` rows created or active since the initial
capture, including any subsequently retired row. Record exact keys, owners,
archetypes, obligations, and creation/wake/turn state and its ordering against
the observed publication records. A late active old reviewer or a new reviewer
created, assigned, or woken under the partial prefix is a raced partial-publication
outcome, even if that new reviewer is now idle or retired. Stop before steps 6–7.
Missing records or indeterminate ordering also stop the sequence as unproven;
absence from the original roster is not permission to refresh or adopt the row.

Return the affected rows and obligations to their existing owners for explicit
finish/transfer/retire disposition under I3. No automatic retirement or apply
repairs an already composed partial-prefix context. The stopped packet does not
resume itself; a later owner-approved continuation must account for those rows
and repeat the content and roster checks before selecting refreshes or clean
successors. If existing lifecycle operations cannot complete that disposition,
record it as unrecovered. This recensus reports observed rows; it adds no admission
fence, freeze, or guarantee against subsequent concurrent action.

### A5. Forward, failure, and recovery truth

| Observed boundary | Truth to record | Supported next step / explicit limit |
|---|---|---|
| Dirty tree, wrong branch, missing input, invalid preflight | Publication not attempted by this sequence | Correct preparation through its owning workflow; do not clean another actor's work. |
| One of the five preparation edits fails | Earlier additions may already be published; the old reviewer has not yet been removed by relearn | Stop at the failed command and record each observed revision. Use only a covered forward repair; do not claim removal of already created manifests. Preserve existing staffing until the roster's separate lifecycle steps. |
| Relearn reports conflicted paths | Merge pending; live remains prior; upstream may have advanced | Resolve the actual conflicts then `relearn --resolve`, or `relearn --abort`. Abort does not promise to rewind upstream. |
| Merge validation or pre-merge hook fails in the inspected rollback branch | That branch aborts merge and restores upstream; live remains prior | Record exact error and refs; revise the input through its owner. Other Git/I/O failures need their own observed state, not this branch's guarantee. |
| Candidate commit exists, but publication returns conflict or marker failure | Main may contain candidate while live differs or remains prior | Record refs, response, and owning assignment; stop this rollout and return the observed failure to that owner. There is no standalone publish-candidate retry. This is an accepted unrecovered outcome, not a claim that old state was restored. |
| Live advances, then law reload or final response fails | Publication may be partial; an error is not proof of reversal | Stop subsequent rollout commands and record the observed failure for the owning assignment. Use a limited per-file repair only if the packet's exact supported command and preconditions cover it. No `--abort` can undo committed publication. |
| Post-publication recensus finds a late active old reviewer or partial-prefix new-reviewer creation/assignment/wake | Raced partial-publication outcome: catalog publication may have succeeded, but the roster condition failed | Record exact affected rows and evidence; STOP before refresh or successor actions. Existing owners disposition obligations and rows under A4. Neither apply nor merge abort repairs this state. |
| Recensus cannot establish the relevant rows or their ordering | Publication is recorded separately; roster condition is unproven | STOP before refresh or successors; return missing evidence to the owner. Do not infer a clean census or claim rollout completion. |
| Publication succeeds; no sessions selected | New catalog published; existing contexts unchanged | This is publication success, not org rollout completion. |
| File writer fails during apply | Publication unchanged; files may be partially written; no new successful stamp from that failed writer | Record `apply_failed` and the exact key. A later explicit retry uses then-current live; verify that it still matches the packet. |
| Files and stamp succeed; reread submission fails | Files/stamp updated; reread not submitted | Report that partial outcome. Retry is a later explicit decision, not automatic model-context recovery. |
| Apply succeeds | Writer succeeded; reread submitted if resident | No claim that the model consumed the update. Retired/missing selectors report no match. |

Existing per-file edits can restore retained guidance and valid retained manifests
whose elected skills and include dependencies are present. They cannot delete the
new manifests through the current edit CLI, restore arbitrary rules, or restore an
exact prior receipt. Whole-bundle
unlearn is destructive outside this slice. Relearn has no saved-input selector;
reinstalling an old bundle is a separate live/runtime action. Exact catalog
reversal is **not promised**, under the owner's explicit limitation acceptance.
No raw ref reset, database edit, service restart, or new seam supplies an inverse.

The limited repair packet can contain `identity edit <fragment> --file <saved-file>`
and `identity edit <archetype> --manifest --file <saved-manifest>` for a concrete
valid retained-file repair, with the before/after hashes of each input and proof
that its dependencies are present. Validate the entire candidate tree in the
fixture first. Each edit publishes independently and may itself fail; it is
not an atomic rollback. Leave new manifests and receipt membership present when
the existing commands cannot remove them. If the observed failure has no covered
repair, report it as unrecovered and return it to the existing owner; accepting
that limitation does not authorize another live action. Old retired sessions stay
retired. Existing transcripts, assignments, and overrides remain the preserved
historical evidence.

Restoration of the saved old-reviewer manifest after final skill removal is
**unrecovered**, outside this covered repair set. That manifest elects
`reviewing-code` and `reviewing-specs`; the final relearn removes both skills, and
existing validation rejects those absent elections. This design declines adding
skill restoration or inventing a changed old-reviewer manifest to broaden recovery.
Its packet therefore contains no saved-old-reviewer-manifest restore command.

### A6. Future command and content evidence

The preparer supplies one immutable report containing:

1. Source commit pair, runtime/build provenance, actual gateway input locations,
   and SHA-256 for each seed/bundle file that relearn reads. Capture modes and
   presence/absence too. Package version alone fails this requirement.
2. Before main/live/upstream OIDs, clean-state evidence, receipt bytes/hash, and
   the complete proposed after-path inventory. Removed files carry their before
   hashes; additions carry expected after hashes. Record preserved customizations
   separately from V9 changes within each amended file.
3. The exact ordered command list, execution host, principal, resolved arguments,
   input files/hashes, expected observable result, and either the applicable
   supported repair or the accepted unrecovered outcome for each failure state.
   Commands contain explicit session keys, never `--all`. No command placeholder,
   undefined recipient, or unruled content choice is allowed in an execution-ready
   packet. An explicitly accepted absence of rollback is not a missing command.
4. Real fixture capture provenance and each verification result below. Bind exact
   expected content before execution; record actual command output, exit status,
   observed OIDs, and Git-object content checks afterwards.
5. Separate publication and per-session results, including the post-publication
   recensus, its comparison with the approved roster, and any raced or unproven
   stop outcome with exact row/turn references. Identify any missing evidence
   plainly. Do not infer a future Git OID or model uptake from file hashes/stamps.

### A7. Reuse, deletion, and limitation acceptance

**Reuse, selected:** five existing edits, relearn/resolve/abort, explicit lifecycle, and
file refresh. Catalog import and shared includes already exist. No production
code change is required by this design; allow roughly 1–2 engineer
days for captured fixtures and a bounded command packet, plus one design review.
Installation, waiting for work to finish, and disputed customization rulings are
outside that estimate.

**Delete the rollout surface:** keep accepted source and stop at source-only.
This costs no transition implementation, but does not make V9 available to the org.
The owner declined that reduced outcome by selecting reuse.

**Accept named limitations, selected alongside reuse:** installed-input preparation
needs separate authority; retired old rows provide historical access; recovery
covers pending-merge abort and only the bounded per-file repairs A5 describes.
Some post-publication failures remain unrecovered. The owner accepted those limits;
they cannot be called exact rollback or preservation of runnable old reviewers.

No mechanism is added. A new source selector, catalog-removal verb, compatibility
alias, general migration, and exact rollback machinery were considered and
declined under `dr_c41118fc`. Deleting rollout loses the requested org outcome;
reusing the existing seams with named limits delivers the chosen boundary without
new architecture.

## Acceptance

### Design acceptance

The independent reviewer checks the whole Spirit, A1's source/custody evidence,
A2's bounded delta, I1–I6, and the resolved decisions in Open Questions. The review
must preserve the owner's accepted limits rather than restore an exact-rollback
requirement. A passing design review means the later preparer can build the
specified packet and fixtures. It does not authorize that work, installation, or
live execution, and does not claim the future fixture cases already passed.

### Finite future fixture verification

Run only on **eezo or racter**, in a holder-owned fixture checkout and scratch base.
Use an authorized sanitized capture of the relevant identity Git history and
installed input files. Do not copy credentials, gateway tokens, or live state.db.
Use fixture session rows for lifecycle behavior; do not fabricate external harness
success. These are proposed cases, not passed tests or live compatibility evidence.

| Case | Given / When / Then | Covers |
|---|---|---|
| F1 | Given the captured old bundle and receipt, when relearn uses those same installed inputs, then it does not establish V9 from checkout files alone. | A1, Q1 |
| F2 | Given exact proposed new input and unrelated custom files/settings, when the five preparation edits and real relearn path run, then each prefix is valid, the final diff is A2, both new manifests preserve I2, and shared include rendering uses the three accepted bodies in their intended roles. Exercise a clean merge as well as F3's conflict path. | I1–I2, A2–A3 |
| F3 | Given the captured modified old reviewer and obsolete skills, when import encounters deletion/rename conflicts, then the observed conflict list is recorded; abort preserves prior live, while reviewed resolution preserves named customizations and records actual receipt ownership. | I2, A5 |
| F4 | Given invalid resolved include/election bytes, when resolve validates, then no successful publication is reported. Record actual refs, worktree, and error; compare with the branch of A5 that ran. | I1, I6 |
| F5 | Given active and retired old reviewers with overrides/history, when the lifecycle disposition and publication run without interference, then history remains at the old keys, retired rows retain overrides, and no active row depends on a deleted archetype. Verify transcript access using the real supported path. Command/turn records show no successor creation, assignment, or first turn before final publication, exact content verification, post-publication recensus, and completion of selected refreshes. In separate fixture runs, use a second authorized actor to (a) create/assign/wake a new reviewer during the published prefix and (b) create an old reviewer after the final pre-publication census but before relearn removes its manifest. In each run the post-publication recensus detects the exact raced rows/turn state, records the raced partial-publication outcome, preserves history/overrides and obligations, and stops before any refresh or designated successor action. Missing or ambiguous ordering evidence produces the unproven stop outcome. | I3–I4, Q2, A3–A5 |
| F6 | Given two eligible sessions and one selected key, when apply runs, then only that key receives file/stamp/nudge effects. A writer failure and a reread-submission failure produce the distinct A5 outcomes. | I4–I5 |
| F7 | Given publication failures before and after live advancement, when a covered limited repair runs, then compare the actual catalog, receipt, customization hashes, and session rows with its promised state. Given final removal of both reviewing skills, the repair packet names saved-old-reviewer-manifest restoration as unrecovered and contains no command attempting it. For a failure outside the covered repair set, record the unrecovered state and verify that the sequence stops before refresh; do not invent a rollback command. | Q3, A5 |
| F8 | Given the complete packet and successful fixture, when another reader checks it from Git objects, then each command/input/result is bound, actual revision is observed rather than predicted, and there is no model-consumption claim. | I6, A6 |

The later builder adds these finite cases to the existing identity/gateway tests
and runs the repository's **unmodified** `scripts/verify_mix.sh` with the selected
test paths. The wrapper supplies its canonical environment isolation. Build the
required release CLI first on that test host using
`cargo build --release --manifest-path cli/Cargo.toml`. Record the host, exact
checkout, actual command, capture hashes, and result. Follow that candidate's
required checks if implementation is later authorized. A remote host/toolchain
failure stops verification; Gibson is not a fallback. No gate or product code
execution belongs to this design assignment.

## Open Questions

No unresolved load-bearing design choice remains after
`dr_c41118fc-3871-4024-8064-2f6d2d1e6036` (`rule-reuse-boundaries`). Preserve these
resolved questions so a later reader does not re-decide them:

- **Q1 — RESOLVED:** reuse relearn after separately authorized installed-input
  preparation. No new saved-bundle or selective-import seam. The future input must
  pass I1; broader imports are not silently authorized by this ruling.
- **Q2 — RESOLVED:** retain retired old-reviewer rows for historical access, with
  overrides and history preserved; create explicitly classified successors.
  Declined: runnable compatibility alias and implicit repoint.
- **Q3 — RESOLVED:** merge-abort plus limited post-publication repair is sufficient.
  Declined: a new seam or exact prior-catalog recovery requirement. This is the
  **same identity-delivery boundary previously repaired for file refresh**; the
  existing closed recovery/source work remains closed.

**BLOCKING for live packet execution, not for this design's review:** actual
installed-input provenance/preparation authority; exact content resolutions and
any unanticipated extra import delta; the roster's specific session, successor,
role, work-transfer, and conditional default-setting selections; fixture evidence;
and live execution authority. The later preparer returns an unexpected load-bearing
content choice to the owner before executing its affected step. No actual recipient
or live command is elected in this design.

**NON-BLOCKING:** presentation format for the later packet and roster. Markdown
tables and a hash inventory are sufficient; no product UI, schema, or dashboard is
required. Future optional convenience commands are declined from this slice.
