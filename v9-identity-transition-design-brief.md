# V9 identity transition: bounded design brief

Status: design authorized by dr_bfa7429e-9e59-49a2-8871-dadfdc0370f8. Not an implementation specification or live-action authorization.

## Spirit

Finish the existing outcome: land the reviewer restructure on both product branches, then make it available to the org. The source half is complete. The remaining outcome is a supported, reviewable way to publish that exact catalog change, select its recipients, and recover if the publication fails. Preserve unrelated identity customizations and existing work.

Success means an operator can inspect a complete command-and-input packet and understand what will change, which sessions are affected, what remains unchanged, and how recovery works. A packet that omits unsupported steps is not complete. No new identity architecture is implied.

## Authority and preserved evidence

- V9 source is closed by att_7488ce2d; main dbe46a8fbabc0d81460c8239dbf54ac8989d6b0b and 0.1.9 7ccf653185fa9b9e26610dec8909eae49b594862 remain the accepted source pair.
- Owner source-complete/live-publication-blocked verdict: att_d724fa4a.
- Dry packet art_c7455040, SHA-256 a019e803f0a0c02f8dab53bfb2de03d2133d5e1ba81eb406cfed1a9fa4fa163d.
- Read-only installed-surface report art_27c048da, SHA-256 7ef877097956f83086ab2762cba7512835613e264b4fcb34845084d2511031e9; inspected from Racter. Its CLI-help omissions are evidence of an unproved path, not proof that a new subsystem is necessary.
- Accepted simple identity-refresh work remains closed. Do not restore generation, activation, atomicity, or runtime-readback promises removed from that scope.

## Questions the design must settle

1. Catalog and content: identify the smallest supported transition from reviewer to reviewer-code/reviewer-spec, including review-common.md, manifest elections, obsolete review skills, and affected references. Inspect implementation and installed bundle custody before proposing any new command. Distinguish source changes from installed runtime capabilities.
2. Preservation: enumerate exactly which identity paths and records change. Explain how unrelated customizations survive. State how existing sessions bound to reviewer remain addressable; do not silently reassign their role or discard history.
3. Recipients: propose an explicit session-selection rule and a reviewable roster format. Explain ambiguous code/spec reviewer assignments and how an owner resolves them. Counts and staleness alone are not selection authority. Actual live selection and application remain later decisions.
4. Recovery: describe supported forward and recovery operations, their inputs, and the observable state after each failure point. Prefer restoration through existing supported operations if sufficient. Do not demand a named-revision rollback verb merely because the old packet asked for one.
5. Evidence: specify a complete future command/input-hash packet and content checks. If a future Git revision cannot be predicted, say so and bind expected content plus subsequent observed revision instead; do not invent a revision or add a prediction mechanism solely for paperwork.

## Required output and acceptance

Produce one bounded technical design in tightbeam-specs with source citations, exact supported command semantics, proposed minimal changes only where necessary, and proportional independent review. Compare reuse, deletion of the requested surface, and explicit acceptance of the limitation. Adding a mechanism must explain in one line why deletion and accepting the limitation fail the chosen outcome.

The design must separate publication from session refresh and name every unresolved question. Any load-bearing product choice returns to this owner before implementation. Include estimated implementation cost and a finite fixture-based verification plan on Eezo or Racter; design work itself runs no product code. No test fixture may claim live compatibility or recovery behavior it did not observe.

Done for this slice means the owner receives a buildable, independently reviewed design or an exact evidenced impossibility with a bounded choice. It does not mean the org rollout is complete. Implementation requires a later authorization; live execution still requires its separate explicit approval.

## Non-goals

No V9 source rework, new reviewer behavior, identity-generation framework, global quiescence barrier, general migration engine, new audit/readiness subsystem, automatic session classification, fleet-wide apply, historical backfill, runtime deployment, credential/service changes, or closure-defect repair. No live identity edit/relearn/apply, install, release, deploy, or second-YES request.

## Ownership and handoff

Keep this design on existing V9 work item wi_fc47cb46-cfc4-45c6-9b74-def1522e5ebf and owner asg_f70bf2e7. Prior identity recovery wi_ff222e95 is completed; its residual owner row is done-but-open solely for a routed lifecycle defect, not implementation capacity.

Reuse existing orchestrator session s_4071c218, whose recorded spawner is this owner s_daf5ef80. Open a separate design-only assignment; never reopen closed source assignment asg_1295062f. The orchestrator must verify no duplicate identity-transition design custody before staffing a spec writer and independent reviewer. Return the design/review or exact scope question to s_daf5ef80. Preserve the entire Spirit section in the technical handoff.
