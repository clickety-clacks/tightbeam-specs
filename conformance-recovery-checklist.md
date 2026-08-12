# Conformance recovery — working checklist

Tracking only (the specs it audits against remain the decision homes). Live recovery
state for the 2026-07-23 spec-completeness reckoning: the audit found ~400+ unsatisfied
clauses across 20 system/spec pairs; fix passes are converging under adversarial
verification. Session scratchpad evidence (verify/redo/pass3 reports) lives under the
recovery session's scratchpad; final ledgers get persisted here (item 8).

## Acceptance bar (the stopping rule — do not loop past this)

A lane is DONE when: zero STUBBED clauses, every HANDOFF entry has a nameable blocker
(spec decision or cross-lane file), compile + touched tests green. The RECOVERY is done
when: all lanes merged, full suite green, and the live e2e smoke (shrdlu) passes —
including the fresh-install → kungfu-install → spawn → flagship-gate → escalation path.
Everything not covered by that bar goes to the honest-gap ledger as roadmap debt, not
another fix loop. Clause counts are a proxy; the live smoke is ground truth.

## Checklist

1. [x] Spec-completeness audit — 20 Sol-high reviewers, clause tables (~400+ unsatisfied).
2. [x] Fix pass 1 (Sol-medium, 13 file-disjoint lanes) + adversarial verify pass 1.
       Result: 122 CLOSED-REAL / 122 STUBBED / 140 STILL-OPEN; 3 lanes verified
       (roles, wake-on-fact, core-org), 10 deficient.
3. [x] Kungfu packaging: full cultivated bundle copied to priv/kungfu on the
       kungfu-packaging branch, verified 44/44 vs backup (last fragment closed).
       Backup deletion BLOCKED until that branch merges to main (it is the only
       second copy until then).
4. [x] Fix pass 2 (anti-stub contract, Sol-high, 10 lanes) + verify pass 2.
       Result: +2 lanes verified (spinup, core-containment); 7 deficient on NAMED
       residuals only (dominant sin shifted from stubbing to HANDOFF-abuse);
       core-supervision verifier died on infra (retried).
5. [~] Fix pass 3: 6/7 lanes done + delta-verify (verify3) IN FLIGHT on them;
       conformance-smoke pass 3 still running (large corpus rebuild).
       core-supervision verify retry: LANE-VERIFIED (0 stubbed, 0 abuse) → merged.
       This is the LAST fix loop unless something structural surfaces (see stopping
       rule).
6. [~] Integration (STARTED early per jump-in-when-delicate):
       MERGED to main, build-gated green (526 tests, 0 failures): roles, core-org,
       spinup, core-containment, core-supervision + wake-on-fact (pair-merged;
       fire_matching/2 seam hand-fixed: per-fact eager nudges threaded through
       escalation rule/waive, one lane test corrected from the old MAX(id)
       latest-fact approximation to per-fact fan-out per wake-on-fact-v1; seam
       commit 334b15f under Sol symmetric review). Darwin /var-symlink harness
       canonicalization hand-fixed (b55ad22). HANDOFFs relocated to
       conformance-handoff-ledger.md at each merge.
       Spec adjudication queue → conformance-spec-adjudications.md. STATE:
       rulings #1–2 RULED + EXECUTED (r21 amendment landed in spec, code
       pipeline + lease comments + order-pinning test, commit 2cd4a25);
       #3 dead-strand notification AWAITING FLYNN (next up); #4 F2(b)
       narrowing, #5–6 artifacts, #7 cli verb-freeze AWAITING FLYNN.
       Seam-review findings all fixed (F13 filer-owned nudges, ordered
       multi-fact eager drain + fails-on-revert test, commit 2cddbfb).
       verify3: catalog/artifacts/guidance/core-rules/core-assignments
       LANE-VERIFIED → READY TO MERGE (guidance↔kungfu-packaging priv/
       reconciliation is the delicate one); cli LANE HELD on ruling #7;
       conformance-smoke final verify IN FLIGHT. Remaining:
       a. Merge order: verified implementation lanes first (roles, core-org, spinup,
          core-containment, catalog, artifacts, guidance, cli, core-rules,
          core-assignments, core-supervision as they verify), with wake-on-fact
          merged TOGETHER with the fire_matching callsite fix in escalation.ex;
          kungfu-packaging with the implementation lanes; conformance-smoke LAST so
          its corpus judges the integrated behavior.
       b. Resolve the HANDOFF ledger at merge time — cross-lane entries should
          mostly dissolve once files coexist; whatever survives goes to the ledger.
       c. Full suite green + live e2e smoke green on shrdlu (acceptance bar).
7. [ ] SPIRIT AUDIT (Fable, post-integration — added 2026-07-23 per Flynn's
       backfilling-drift concern). Letter-faithful/spirit-wrong drift is invisible
       to every Sol verifier because they all check the same spec distillation; this
       is the only check against the design-conversation record.
       a. Scope: ONLY the concept-heavy surfaces — artifacts/provenance ("promise
          the record, not search"; archive-if-artifacts; custody-exit notice),
          rumination redirect (redirect-not-deny, teach-the-re-entry,
          once-per-work-item), guidance/default-archetype (cultivated onboarding
          intent — the one place spirit already escaped the spec twice), and the
          conformance corpus. Mechanical systems (session-tokens, cli, containment,
          statute-engine) are letter=concept; skip them.
       b. The conformance corpus gets special scrutiny: post-merge it becomes the
          de facto executable spec — a misreading encoded in a fixture ratchets
          forever. Review its cases against decided intent, not just the clause
          table.
       c. Spec-blocked HANDOFF entries are the spec-weakness map: entries reading
          "spec forbids X" = spec working (fine); entries reading "spec doesn't say"
          = a concept that never left conversation → ADJUDICATE WITH FLYNN, never
          with another Sol pass. Fold each ruling back into the owning spec.
8. [ ] Persist the ledgers before session end: final satisfied / handoff-blocked /
       roadmap-debt split lands in this tree (checklist updated + gap items filed
       to the roadmap); missing-feature bucket (e.g. spinup org-CLI
       detect/ensure/deploy) filed as roadmap work items, not conformance fixes.
9. [ ] Post-merge cleanup (all guarded, only after their gating condition):
       a. Delete the identity backup (~/tightbeam-beam-backup-20260723-081431) —
          ONLY after kungfu-packaging is merged to main.
       b. Prune the 13 fix worktrees + kungfu-pkg worktree after their branches
          merge.
       c. Stray base_dirs on eezo (~/.tightbeam, ~/.tightbeam-serve,
          ~/.tightbeam-smoke1, ~/.tightbeam-soak) and /tmp/tb-*; shrdlu strays
          (/home/clu/.tightbeam, /home/mike checkout, /home/mike/.tightbeam-rails-test).
10. [ ] Roadmap follow-through (not recovery, but exposed by it):
       a. Build the kungfu install/projection mechanism (kungfu-template-v1) —
          the shipped bundle is inert until an org can adopt it.
       b. Add kungfu-install to the e2e smoke as an acceptance gate on (a): fresh
          base_dir → install agentic-engineering → spawned agent resolves the real
          coder kernel + skills + the engineering rail fires. This is the check
          that would have caught the blank default archetype.
       c. Candidate kungfu material: the anti-stub contract + CLOSED-REAL/
          HANDOFF-ABUSE verification rubric (the recovery manually enacted the
          flagship completion-requires-review rail — productize what worked).
       d. bug-provenance (Flynn-ratified shape 2026-07-24, folded into
          agentic-engineering-guidance-spec.md — the kungfu's single content
          spec): the `bug-provenance` skill for recon (§5) + coder/orchestrator
          kernel lines (§4) + the `refix-requires-diagnosis` statute in the
          enforcement mapping (§6, flagship rail's re-entry twin; promotes
          root-cause-before-refix out of advisory). Kungfu content only; no
          substrate change.

## Standing constraints (recovery-scoped)

- Nothing merges on self-report; every claimed close survives an independent
  adversarial verify grounded in `git diff main`.
- HANDOFF.md is the ONLY legal non-close; its claims get adversarially re-checked
  (HANDOFF-ABUSE = closeable-in-lane but punted = deficiency).
- "Done" is Flynn's word. The recovery ends at the acceptance bar + Flynn
  verification, not before.
