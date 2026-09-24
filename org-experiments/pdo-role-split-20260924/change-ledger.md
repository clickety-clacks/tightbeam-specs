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
