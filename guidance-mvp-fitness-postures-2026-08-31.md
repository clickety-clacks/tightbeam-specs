# Review evidence: MVP fitness review, work postures, posture rail (2026-08-31)

Mike's guidance review of 2026-08-31 produced five corrections to the
agentic-engineering kungfu. This note is the review evidence main's
integration process requires; the working file with the rulings, the
recon evidence, and the application notes is `~/guidance-changes-todo.md`
on gibson.

## What changed

1. `guidance/model-policy.md` deleted (0.1.9); on main it was already gone
   and the ownership sentence went on the kungfu activity table.
2. Two work postures, heavy and light, ruled by the orchestrator on
   receiving a slice and filed as `posture-heavy` or `posture-light` on the
   slice card it holds open. Light: the input is the spec, one coder, one
   review at the light bar.
3. Rails `implementation-requires-posture` (assign) and
   `implementation-dispatch-requires-posture` (dispatch): no coder card on a
   work item without a posture verdict. Deny, `external_producer`,
   `target.archetype`.
4. The reviewer adjudicates MVP fitness against the ask: facets first;
   beyond the ask is unfit; two classes, `blocking` and `post-mvp`; the
   orchestrator files `review-overreach` when a blocking finding did not
   earn the block; contests are adjudicated by the orchestrator.
5. Guidance-authoring criterion (seed skill, rule 15): constrain the work,
   not the boxes; cut what a competent agent does unprompted.

## Superseded clauses (org follow-up, not done here)

- `tightbeam-decisions.md:2093`, Flynn 2026-07-22: the eight-section spec
  skeleton as a review gate. Under item 4 the skeleton stays the writer's
  and the reviewer blocks only on a load-bearing hole.
- `agentic-engineering-guidance-spec.md:234` (and 166, 227, 247, 435): the
  blocking/important/nit severity vocabulary. Under item 4 the classes are
  `blocking` and `post-mvp`.

## Where it landed

- 0.1.9: https://github.com/clickety-clacks/tightbeam/pull/39, commit
  a1b43ff8. Gate: 1765 tests, 1 failure, the same `escalation_test`
  transaction-observability test that fails on a clean 0.1.9 worktree.
- main: branch `guidance/mvp-fitness-postures-main`, commit f55ad946,
  adapted to main's text and mechanisms (main's rails, `ask --user`, armed
  doorbell, revocation reasons). Gate: 2023 tests, 0 failures. Main's CI
  was red at the OTP preflight; PR #37's two gate commits were cherry-picked
  to main (c5ba4488, 6e852693) under Mike's election to make it green before
  the merge.

## Learned while applying

- A verdict-fact gate without a declared producer fails `Rules.load!` for
  the whole rules file, and the loader runs at boot. Both posture rules
  carry `external_producer = true`.
- A completed non-review card on a bug work item counts as a prior fix for
  `refix-requires-diagnosis`. Posture goes on the slice card the
  orchestrator holds open for the life of the slice.
- Basing the reviewer rewrite on the live org's text dropped 0.1.9's
  receipt-first paragraph, which the `code-review-requires-passing-tests`
  rail depends on; the identity test caught it. Both lines now carry it.
- Main's identity test pins the kungfu activity table by SHA-256; any edit
  to that table re-pins.
