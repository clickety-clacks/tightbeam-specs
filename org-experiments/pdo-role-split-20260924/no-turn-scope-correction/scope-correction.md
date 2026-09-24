# Task scope was expanded into permanent org guidance

The September 11 engineering-kungfu consolidation was assigned to an external agent. The work was to gather feedback through Subetha, reconcile overlapping guidance work on a 0.1.9 branch, and later adapt the result to the live 0.1.8 org. It was not an instruction establishing a continuing organization-wide pause for unrelated work.

The conversation record is `/home/mike/.codex/sessions/2026/09/11/rollout-2026-09-11T15-17-32-01a0910b-9e5e-77e3-9bfb-3e0bc07ddb97.jsonl`. Relevant entries are human/assistant message records, not replayed Subetha traffic or agent-authored summaries.

- Line 2319, September 11 at 2:41 PM PT: the user's full assignment required the consolidation and reviews to happen outside Tightbeam, through Subetha, followed by a compatible live-org application.
- Line 2370, September 11 at 2:58 PM PT: "ok but make sure to mention that tightbeam can run turns. you can read agents and substrate but nothing that needs turns". This statement belongs to that external work assignment.
- Line 2375: the agent's immediate response said "this effort must not depend on or trigger any Tightbeam-managed turns". Its own wording initially retained the task scope.
- Lines 7749 and 7756, September 12 at 9:06 and 9:16 AM PT: the agent proposed allowing migration turns and resumed eligible work; the user replied "do it". That later authorization also contradicts treating the earlier task restriction as a current blanket prohibition.

Local identity commit `34afb8ebfdef367004221a82e1a158d768a406af`, September 12 at 1:21 AM PT, nevertheless added this to the shared operating manual under Gibson organization constraints:

> Tightbeam can run turns. While Mike's no-turn restriction is in effect, read agents and substrate but do not wake, dispatch, spawn, resume or perform another operation that needs or can trigger a Tightbeam turn. Mike controls resumption and gateway power.

The author identity `user:mike` is the CLI's attribution, not proof that the user personally wrote the passage. The passage was absent from the shipped v0.1.8 source checked during investigation. It remained in the live org's shared manual and reached both the PDO and PO during the September 24 evals.

The authoring failure was the scope expansion: a constraint on who would carry out a particular task became standing instructions for later agents. The current external evaluator compounded it by describing the passage as an org pause and discussing pause controls before establishing its original context. No current pause decision was established. A runtime feature proposal does not explain or justify this misplaced paragraph.

## Correction

Published identity `50ca792ad8a7fc20415d04ad9c1b0637ad838894` removes the task-specific execution restriction and retains the independently applicable gateway-power authority as "The user controls gateway power." No new permission gate or pause mechanism was added.

The exact diff and publication receipt are retained beside this note. Verified the published file against the candidate, a clean identity worktree, and no remaining "no-turn restriction" text in the live org guidance or skills. Source history, previous composed prompts, failed eval evidence and interviews remain intact. Existing conversations can retain older context; this publication is not a claim that all running sessions were refreshed.

The earlier eval outcomes remain historical facts. Luna medium produced directly; Luna max consulted the PO then stalled with the PO on this mis-scoped instruction. Those runs used modified org guidance containing this contamination, not clean shipped instructions. No post-correction behavior eval has run yet. This correction should not be ported as a new pause feature or a model-selection conclusion.
