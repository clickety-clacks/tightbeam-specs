# PDO role split experiment, September 24, 2026

Mike authorized applying the proposed split and annotating changes for a later 0.1.9 port. This is an org identity experiment on released 0.1.8, not a .9 merge or release. Baseline is 30b55757d466f189bb4cc701d243fde2bd181146. Exact candidate patch and all before/after files are retained alongside this ledger. Published at identity revision 2f38dba4a5b3f793c76f1505324edc9923204f9f after independent review corrections. Fresh-session behavior trial failed; see report.md.

## Changes and reasons

| Org identity path | Change | Reason and .9 treatment |
| --- | --- | --- |
| archetypes/pdo.toml, guidance/pdo.md | New always-loaded PDO role, Luna medium default matching existing test seat | PO determines plan; PDO staffs/executes and never produces. Port role semantics to engineering bundle; host placement is org-only. |
| guidance/delivery-coordination.md | Extract shared delivery duties, current-record reconciliation and within-plan recovery | One home shared by PDO/lane owner. Osanwe routing retained from old orchestrator is org-only, omit from portable bundle. |
| archetypes/orchestrator.toml, guidance/orchestrator.md | Preserve executive scope; lane scope under existing PO plan; remove product-delivery skill election | No repeated PO consult for covered child assignments; no authority to amend PO plan. Preserve current Sol high default. |
| guidance/product-owner.md, skills/team-design/SKILL.md | PO determines and alone revises plan | Remove adoption/amendment authority granted to delivery. |
| guidance/team-planner.md | Planner returns advice for PO decision | Remove another route granting delivery owners topology redesign. No mandatory planner introduced. |
| guidance/archetype-roster.md, kungfu/agentic-engineering/capabilities.md | Discover real PDO role; distinguish lane owner | Bundle root stays product-owner; no migration implied. |
| skills/product-delivery/SKILL.md | Retirement notice for unelected legacy skill | No defining role duties in a skill. Retained historical file only; it supplies no compatibility or refresh mechanism. |
| guidance/engineering-model-activities.md | Capability floor requires reconciling delivery records and recognizing plan revisions | Keep existing model order. Remove direction to forward every evidence conflict to PO. Model sufficiency remains experimental. |
| rules/topology.toml | Include PDO in intake exception and completion check | Mechanical same-item decision rail applies to new role. No authorship gate, no fixed topology. |

## Publication and port discipline

Use identity edit for guidance, archetype manifests and skills. Rules and capability metadata have no installed edit verb; commit only those reviewed configuration paths, then publish through identity edit and reload the released rule engine with the supported already-learned bundle command. No service restart or replacement binary. Record all returned revisions and verify served configuration with fresh sessions.

Source locations for a later port are the engineering bundle's archetypes/guidance/skills/rules under priv/kungfu/agentic-engineering, plus any shared canonical home already used on .9. Reconcile against the .9 tree rather than copying a whole live identity. Retain host-independent behavior; exclude Gibson/Racter placement, Osanwe GUI routing and local deployment rules. PR #110 remains separate and unmerged. Neither this ledger nor a passing fixture authorizes its merge.

Existing PDOs remain legacy orchestrator sessions with current custody; no retirement/repoint, all-session apply or notification reparenting. Fresh tests prove only newly received composition. The .8 resumed-session refresh issue is fixed in .9; identity revision stamps alone are not receipt evidence.

The rail checks same-item topology record existence. It cannot prove PO consultation, block product file writes, inherit topology across separate items or prevent missing-item assignments. These are declared limits, not passing behavior results. Preserve failing trials even if a rail forces recovery.

## Evidence

Baseline and candidate trees, candidate.patch, changed-files.json, compose.exs and composed prompts; native-check.exs and its results; independent review; publication receipts; live traces, actual received provider prompts and final report. Stage and outcome updates will be appended here.

## Independent review corrections before publication

The first review found four issues. Tightened the revision test to require a returned decision before substitution and fail every PDO product write. Preserved executive-scope orchestration for fresh executive sessions. Removed cross-role file references that are not materialized into homes and labeled the unelected old skill as retired, not a working compatibility mechanism. Clarified planner commissioning requires a genuine bounded planning decision under the existing rail. The PO can plan directly; no mandatory planner stage was added.

## Publication evidence

Published all 13 candidate files through exact-path config commit and identity edit. Final live revision: `2f38dba4a5b3f793c76f1505324edc9923204f9f`. Byte comparison against candidate passed; already-learned reload returned successfully. Independent final review is clean. Native released-rule checks passed 23 assertions, including explicit known-limit assertions. Fresh PDO `s_4690118d` uses archetype `pdo`, Luna medium; fresh PO `s_048b0964` uses Astra high. First fixture is `wi_318b25ce-1c84-4812-9153-21edb411368c`. Behavior failed consultation ordering; recovery does not erase that result.

## Final experimental outcome

The first fresh PDO trial attempted worker staffing before PO consultation despite receiving the new core. The existing rail refused it, then the PDO recovered through the correct PO. PDO kept product authorship delegated in the observed run. Incorrect code-effect classifications caused additional refusals. The temporary coder read session credentials while finding the PDO directory, so the fixture was ended and all six temporary sessions retired. No open fixture cards, pending wakes or queued/running turns remain. No credentials are included in the exported evidence.

Four planned behavior cases were not run after the stop; they remain explicitly unproven. Native same-item checks passed but do not establish lane behavior. The change remains an installed org experiment, not a proven .9 fix. Keep this negative result with the exact patch when considering later porting. Complete results are in report.md.

## Fresh rerun 2, same identity and models

Mike requested another eval. No guidance or rail changed. A new PDO on Luna medium and PO on Astra high received the same supplied-facts correction task, with an explicit credential-file prohibition and retention for interview added. The PDO directly wrote a 148-word note without consulting the PO, then attempted completion. The rail refused; the PDO surrendered citing an unsupported current no-turn restriction. Both live interview answers are preserved. The second answer admitted no instruction allowed the producer exception and no visible current ruling activated the conditional no-turn text.

Role compliance and proactive consultation failed. Completion enforcement passed; it did not prevent the already-completed file write. The PO had no turns, so its model was not evaluated. Two temporary sessions are retired with no open assignments, pending fixture or work-item wakes, or queued/running fixture turns. This rerun strengthens the negative evidence for the current configuration; it does not authorize or establish a successful .9 port. See [rerun-2/report.md](rerun-2/report.md) for chronology, comparison limits and evidence.

## Luna max comparison

Mike requested the same eval with Luna at max. Only PDO effort changed from medium to max; fresh identities and marker were substituted, and task text otherwise matches rerun 2 exactly. Provider context confirms gpt-5.6-luna max and unchanged PO gpt-6-astra high. No guidance or rail changed.

The PDO consulted the PO before staffing without external correction, obtained a same-item topology decision, and did not author the note. Delivery still failed. The PO and PDO treated conditional no-turn guidance as an active restriction without a current ruling; both acknowledged the evidentiary gap in same-session interviews. No worker ran and no note exists. The PDO also opened consultation with the default code effect, leading to an avoidable review refusal.

The consultation-order result improved in this sample; delegation and completed delivery remain unproven. This is not a general model comparison or a successful .9 fix. Both fixture sessions are retired with no remaining open obligations, pending wakes or active turns. See [luna-max/report.md](luna-max/report.md) and both preserved interview answers.

## Generic user references in authored guidance

The user requested: unless the authoring prompt names the user, guidance must use "the user" and never the user's personal name. Added two lines under the concise-writing rule in the current shared authoring home, `guidance/guidance-policy-craft.md`:

> Unless the authoring prompt explicitly names the user, never use their name in guidance. Write "the user".

Published through `identity edit` at revision `3457325895f22be680db3a1aa3c3487b091b2296`. Both guidance-writer and guidance-reviewer include this home. The older `tightbeam-guidance-authoring` skill is release-owned; its installed bytes were not edited. This is an active org authoring-rule update and a portable rule to retain in a later .9 port, not a release or blanket refresh of existing sessions. Verified the exact two-line diff, clean identity worktree and both role includes. No behavior eval was warranted for this narrow text addition. The separate no-turn paragraph was not changed by this request.

## Remove the mis-scoped external-task restriction

The user clarified that the original task was to have external agents perform the engineering-kungfu consolidation. Read the original conversation: that task's restriction was expanded into a permanent shared manual paragraph in local identity 34afb8e. It does not establish a continuing org-wide pause. The evaluator's earlier org-pause framing was wrong.

Published identity 50ca792ad8a7fc20415d04ad9c1b0637ad838894 removes that restriction while retaining the user's control of gateway power. No runtime pause feature, new permission gate or blanket session refresh was added. The failure evidence remains unchanged and no post-correction eval is claimed. See [the scope correction](no-turn-scope-correction/scope-correction.md), original conversation locations and exact patch.

## Opus 5.5 high PO rerun

The user requested a fresh run with Opus5.5 high as PO and Luna max retained as PDO. Corrected guidance69bdb209 reached the PDO. It consulted before staffing, used coordination, and did not produce. The requested PO could not execute: the managed Claude2.1.274 was rejected, requiring2.1.280+. Running gateway1342 predates the installed1343 adapter correction. No topology, worker or note was produced; this is an environment-blocked attempt, not a PO behavior result. The PDO was interviewed and admitted avoidable command discovery and an inconsistent fallback proposal. Both fixture owners were retired after evidence capture with no open fixture work, wakes or turns. No guidance or runtime was changed. See [opus55-high/report.md](opus55-high/report.md). The full requested eval still needs activation of the installed release and a fresh rerun.

## Sol low PDOs for new work

The user broadened the trial model choice to all new work items. Published PDO default and preference are now gpt-5.6-sol low at identity ea24101. Both live PDOs, Engram and Tightbeam, were tuned to that configuration with engine context preserved. No role migration or prose-guidance change occurred. Updating three contradictory model-selection references awaits explicit guidance permission. The fresh Opus PO eval still awaits authorization to activate installed build1343; no eval success is claimed. See [sol-low/report.md](sol-low/report.md) and the before/after settings.

## Align PDO model-selection guidance with Sol low

After explicit user approval, identity 312a6e17 changes only the three shared PDO model references: remove PDO from the Luna capsule and replace the first candidate with sol[low] in both PDO activity rows. Defaults and live PDO runtime settings already match. No role duties, topology rail or unrelated model selection changed. Publication is verified; existing contexts were not blanket-refreshed. See [sol-low/guidance-alignment/report.md](sol-low/guidance-alignment/report.md) and exact patch. The gateway restart is now authorized and waiting for the sudo password handoff; the eval has not started.
