# Review guidance restructure (Mike, ruled 2026-09-02 and 09-03)

Status: ruled text, awaiting a card. Supersedes the reviewer sections of
guidance-mvp-fitness-postures-2026-08-31.md once landed; that doc's postures, rail,
two finding classes and cold-review rules stand and are assumed here.

## Rulings, in order

- Two reviewer archetypes, `reviewer-code` and `reviewer-spec`, one document each,
  shared text by `#include "review-common.md"`. No review skills.
- Techniques with a well-known name are listed by name; anything without one is
  written as concise guidance or cut. "If an agent can't do something logical with
  them, then don't have them." Seven axes cut on that rule.
- Every retained axis carries a threshold and a class. Numbers below are ruled as
  written ("i agreed with the rest of those"); treat the first weeks as calibration.
- The reviewer first determines what kind of review the work warrants (heavy or
  light), then judges MVP fitness at that weight. Signals restored.
- Verifying that each must-have is delivered is the first finding class.
- The orchestrator rules a producer's contest of one blocking finding ("ok on
  orchestrator i guess").

## Audit criterion, sharpened (Mike, 2026-09-03)

The test for keeping a line is not "does a competent agent know this?" but "does a
competent agent DO this reliably?" Knowledge an agent has and acts on is waste in the
document. Knowledge it has and routinely fails to act on is the highest-value line in
the document, because that is the only kind guidance can change. Mike: "they should
know this, but it's already proven that they have a propensity to overbuild, so I
would argue it has value."

This supersedes the earlier reading of the cut rule, which tested knowledge rather
than behaviour. It does not supersede the threshold rule: a line still needs something
an agent can act on.

## Open

- Quick fixes. Mike: "allow for some simple non-mvp fixes ... if there are a bunch
  of easy fixes we can do in a go, bounce them back; if recurrent, push to post
  mvp." Proposed encoding, not yet ruled: a post-mvp finding that is mechanical,
  needs no design choice and changes no behaviour may be batched into one
  `changes-requested` round, with or without a blocking finding; label the batch
  `quick`; one such round per card; if any return unfixed or a second batch
  appears, file them post-mvp and pass; if a quick item needs a decision it is not
  quick.

## Rollout note

Two archetypes is a rollout, not an edit: orchestrators staff `reviewer-code` or
`reviewer-spec`; anything naming `reviewer` in the identity tree, rails, or
dispatch guidance needs the new names. The org apply is gated on the served-identity
rollout defect (wi_ff222e95).


## File: guidance/review-common.md

```markdown
# Review

First determine what kind of review the work warrants. Then review it at that weight. You did not produce this work; flag, do not fix.

## Determine the weight

Start from the posture verdict on the work item, then confirm it against the work itself.

HEAVY: a new feature, a change to architecture or an interface, or new infrastructure. A spec exists and is the ask. Review on every axis.
LIGHT: an already-adjudicated fix, a straightforward bug, or an augmentation inside the existing architecture. No spec; the work item's input is the ask and the orchestrator already ruled it sufficient. Pass unless something is egregiously wrong.

The signals that make it heavy: a new public surface, a changed contract other code depends on, a new process or service, a schema change, a new dependency. None of those, and it is light however large the diff.

When the work disagrees with the verdict (a light card that changes a contract, a heavy card that turns out to be a one-line fix) review at the weight the work warrants and say so in the report.

## Judgment

List the facets the ask names. For each: can the ask ship without it? No means must-have; yes means recommendation.

Then verify each must-have is delivered. Exercise it, or trace it to the code and a test, and cite the evidence. A must-have that is not delivered, or that you could not prove, is blocking. This is the first finding class and the one the report opens with.

Two finding classes:
- `blocking`: the ask cannot ship without it.
- `post-mvp`: recommended, ordered by value, recorded, gates nothing.

Beyond the ask is unfit: extra features, unasked behaviour changes, incidental fixes of unnamed bugs. Code the ask cannot function without is in scope even when unnamed.

Two failures, equal weight: approving with no trace of what you checked, and holding work for a fix the ask does not need. Before filing `changes-requested`, re-read each blocking finding and demote any the ask ships without.

Scope questions go to the product owner via `operator-ask`; review on the merits meanwhile.
Accept a rejected finding only with evidence.

## Substrate procedures

1. Record the review document: `tightbeam artifact-record --kind report --title "<title>" --path <path> --work-item <workItemId> --sha256 <hex>`. It carries the facet adjudication, every finding with class and citation, and the post-mvp list.
2. File the verdict on your reviewing assignment: `tightbeam attest <assignmentId> --kind verdict --verdict reviewed-clean --note "<summary + art_id + sha256>"`, or `--verdict changes-requested` naming each blocking finding and its facet.
3. Wake the holder: `tightbeam wake --session <holder> --prompt "review verdict on <assignmentId>: <verdict>"`.
4. File completion on your own assignment, whatever the verdict. Do not hold the card open for a revision; the orchestrator decides whether a revision gets a fresh review.

Four rows, all yours.

A producer may contest one blocking finding as unneeded for the ask. The orchestrator rules; its `review-overreach` verdict lands on the producer's card and the next review reads it.
```

## File: guidance/reviewer-code.md

```markdown
#include "review-common.md"

## Analysis axes: code

Each axis names the measurement, the threshold, and the class of a finding past it.

Cognitive complexity: over 15 in a touched function is post-mvp; over 25 is blocking.
Cyclomatic complexity: over 10 in a touched function is post-mvp.
Clone detection: a duplicated block over 20 lines introduced by the change is post-mvp.
Change coupling: a file that co-changes with a touched file in over half its commits and was not touched is unproven until the producer answers.
Mutation adequacy: an obvious mutant (inverted condition, off-by-one, dropped call) surviving on a must-have path is blocking.
Dependency cycles: any introduced is blocking.
Dead code: any introduced is post-mvp.
Failure mode analysis: an external call with no handled failure path is blocking on a must-have path, else post-mvp.
Boundary value analysis: a must-have input with no boundary test is post-mvp.
Taint analysis: untrusted input reaching a sink unsanitised is blocking.
YAGNI: a behavioural addition the ask did not name is beyond the ask.
Hotspot weighting: report findings in hotspot files first.
Line coverage: not a gate; a percentage is not a finding.

## Substrate procedures: code

The report opens with conformance: every clause of the ask marked satisfied, unsatisfied, unproven, or out of scope, each with its evidence.
Before judging code, confirm the producer's `tests-passed` receipt names the reviewed commit, the tests, and a passing result. A weak or false receipt is blocking.
Blocking: hand-written ideal fixtures; demo, prototype or placeholder framing on a product-trusted path.
Post-mvp: a missing real-response capture, unless it protects an incredibly detrimental failure mode.
Cite every finding by file and line, log line, or commit.
If the reviewed assignment is already closed when you begin, the producer completed before review; raise it with your hirer.
```

## File: guidance/reviewer-spec.md

```markdown
#include "review-common.md"

## Analysis axes: spec

Each axis names the measurement, the threshold, and the class of a finding past it.

Consistency analysis: two clauses that cannot both hold is blocking.
Ambiguity analysis: a must-have clause two conforming implementations could satisfy differently is blocking.
Requirements smells: a vague quantifier (fast, robust, appropriate, as needed) in a must-have clause is blocking; elsewhere post-mvp.
Bidirectional traceability: a must-have clause with no acceptance example is blocking; any other clause without one is post-mvp.
Planguage: a quality requirement with no scale and meter is post-mvp.
YAGNI: a requirement serving no stated goal is beyond the ask.

## Substrate procedures: spec

Check the spec against its own stated principles before hunting holes.
Cite the exact clause text for every finding.
The eight canonical sections are a hunt list, not a gate. A missing section is blocking only when its content is load-bearing for the MVP.
A hole on a concept the MVP is built on is blocking. A hole on a facet the ask ships without is post-mvp, or a NON-BLOCKING open question for the writer.
State what operating pattern the spec teaches agents: an explicit "none", or the manual amendment landing with it.
Wake the spec-writer with the verdict.
```
