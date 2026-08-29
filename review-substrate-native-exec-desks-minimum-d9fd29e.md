# Independent successor review — substrate-native exec desks minimum rewrite

Reviewed assignment: `asg_747c1455-7110-4364-bdd2-55deb6d6ee1b`

Reviewed producer assignment: `asg_c37b6b1a-5258-45e0-b196-010911f5c1b1`

Reviewed commit: `d9fd29e22b197e3eaf511e70c7a045ec64f6f178`

Reviewed file: `substrate-native-exec-desks-v1.md`

Reviewed file SHA-256: `c2815d9be879efa3ab8748948493c6e521e1986b9f4ca7457284553d3692be7b`

Verdict: **changes-requested**

## Custody and scope

- A fresh reviewer-owned Gibson clone resolved
  `origin/spec/substrate-native-exec-desks-v1-minimum` to the reviewed commit.
- The sole parent is the previously reviewed commit
  `0767558eccfcdee974bee9d2b426c74e6f92fcc6`.
- The reviewed commit tree is `dedebda06d40131f6448d525ca10c398672526ca`.
- The parent-to-successor diff modifies only `substrate-native-exec-desks-v1.md`:
  25 insertions and 19 deletions. `git diff --check` passed.
- The worktree was clean at review start. The independently computed file hash matches
  producer artifact `art_cc16bd61` and readiness receipt `att_30422904`.
- Prior verdict `att_46758d8c` and report `art_0f207e26`, reviewer custody
  `att_59897e92`, and repair receipts `att_88ec6ce6` and `att_aa78fce6` were read
  with the full `wi_795a354d` trace.

## Prior-finding disposition

| Prior finding | Result | Evidence |
|---|---:|---|
| F1 — algedonic routing | Repaired | Lines 24 and 62 define Owner Main from recorded ownership, pass algedonic now and unchanged, prohibit intermediate handling and a second carrier, and prevent a Main-to-Main send loop. A3 repeats the complete rule. |
| F2 — initial NOTE single-flight and fan-out | Partly repaired | Lines 30, 53, and 72-74 add the durable pending NOTE claim, one execution wake, and deterministic terminal fan-out. The crash interval in R2-F1 below still defeats the promised one-call bound. |
| F3 — pilot baseline custody | Repaired | Lines 40 and 80 define retained source fields, an exact cutoff-bound command and projection, sorted output, version capture, and immutable artifact hash. `art_a4f39376` is seed provenance only. A22 makes the evidence reproducible. |

## Finding

### R2-F1 — blocking — restart replay can violate the one-call NOTE contract

The activity-summary paragraph says that one execution wake may start one bounded model
call, that restart replays an unsettled execution wake, and that the path has no second
model call in the same worker/window (`substrate-native-exec-desks-v1.md:72-74`). Those
clauses conflict when the provider accepts the call and the process stops before the
terminal transaction commits. The NOTE remains `pending` and the execution wake remains
unsettled. Restart therefore replays the wake. The described handler may start the call
again.

The durable NOTE/window key prevents concurrent trigger winners. It does not make an
external provider call atomic with the terminal database transaction. The spec defines
no durable started disposition, provider idempotency key, resumable call identity, or
deterministic `outcome_unknown` failure that would settle every linked check-in without
calling the provider again. Provider telemetry in Assumption 8 records attempts; it does
not enforce idempotency.

A15 proves only concurrent-arrival single-flight. A16 and A17 begin after a result or
terminal failure exists. No acceptance case covers a stop after provider admission and
before NOTE settlement (`substrate-native-exec-desks-v1.md:102-104`). Thus the successor
does not yet prove both required properties across restart: at most one semantic provider
execution per worker/window and deterministic settlement of all waiting check-ins.

Deletion test: removing replay strands the pending NOTE and its waiters. Removing the
one-call bound restores traffic-amplified semantic cost. Accepting duplicate provider
calls violates Invariant 8 and the paragraph's explicit no-second-call rule. The contract
must define the durable crash disposition and add an acceptance case for this interval.

## Clause table

`S` = satisfied. `U` = unsatisfied. `P` = unproven. `OOS` = out of scope.

| Clause | Result | Evidence |
|---|---:|---|
| Authority, canonical home, and successor lineage (lines 1-3) | S | Work item, Mike rulings, prior verdict, canonical path, parent revision, and provenance revision are explicit. |
| Goal: worker-addressed exec; only now or next bundle (lines 5-9) | S | The worker stays public target; the exec has only the two timing choices and no work authority. |
| Goal: one Main pilot before expansion (line 9) | S | The frozen-query repair makes the before cohort reproducible. |
| Non-Goals 1-2: inbound only; no exec address, recursion, ACP, workdir, shell, repository, filesystem, or assignment (lines 13-14) | S | The architecture uses a worker-row binding and bounded direct provider call only. |
| Non-Goals 3-4: no work/decision authority and no observation request/cancel rows (lines 15-16) | S | I6, A11, A18, and the closed write surface preserve both exclusions. |
| Non-Goals 5-7: independent batcher; no org/target/0.1.x decision; no premature guidance (lines 17-19) | S | The successor changes one policy file and authorizes none of those actions. |
| Terms: Worker, Owner Main, and Exec (lines 23-25) | S | Addressability, ownership resolution, non-recursion, and representation are decidable. |
| Terms: BUNDLE and SUMMARIZE (lines 26-27) | S | Ordered membership and the strict `N > 1` creation rule are explicit. |
| Terms: ANNOTATE and ESCALATE (lines 28-29) | S | Citations and source-linked authority sends are required. |
| Term: Activity-summary NOTE (line 30) | P | Durable states and fields are explicit, but R2-F1 leaves the cross-restart single-call promise unproven. |
| Term: Org policy (line 31) | S | Versioned timing/model inputs remain product policy, not substrate inference. |
| Assumptions 1-5 (lines 35-39) | S | Persisted wakes, landed class, resolver, catalog, and conservation each name a governing seam. |
| Assumption 6: baseline source fields (line 40) | S | The exact retained fields support the cutoff projection. |
| Assumptions 7-8: NOTE privacy and provider telemetry (lines 41-42) | S | Both are explicit, falsifiable prerequisites; telemetry does not cure R2-F1. |
| I1 — worker address and exec delivery (line 46) | S | Public exec addressing is unrepresentable and accepted worker wakes pass through the bound exec. |
| I2 — only now or next bundle (line 47) | S | No later/private priority is allowed. |
| I3 — visible outcome and conservation (line 48) | S | Every accepted input has a direct or BUNDLE outcome. |
| I4 — three verbs (line 49) | S | `SUMMARIZE`, cited `ANNOTATE`, and resolver-backed `ESCALATE` are the only verbs. |
| I5 — two-name attribution (line 50) | S | Each exec-authored row names represented worker and performing exec. |
| I6 — no work authority (line 51) | S | The write surface excludes work and decision state. |
| I7 — event-driven shell/model split (line 52) | S | Durable triggers, deterministic routing, semantic-only model use, deadlines, and zero-idle behavior are stated. |
| I8 — NOTE single-flight and fan-out (line 53) | U | R2-F1; the one-semantic-execution invariant is not preserved by the stated restart replay. |
| I9 — policy remains policy (line 54) | S | Results retain the elected revision; the substrate derives no replacement policy. |
| Inbound binding and atomic acceptance (line 60) | S | The worker row holds the binding; refusal precedes all listed writes; no extra binding/envelope row is added. |
| Class precedence and algedonic route (line 62) | S | Landed classes drive the shell; algedonic deterministically reaches Owner Main without judgment, loop, absorption, or second carrier. |
| Bundle boundary and deadline wake (line 64) | S | Earlier-of boundary, one durable wake, no polling, direct `N=1`, and BUNDLE `N>1` are explicit. |
| Annotation, escalation, resolver, and authorization (line 66) | S | Citations, ordinary sends, transaction-aware parent resolution, and caller authorization are preserved. |
| Delivery atomicity, replay, expiry, and sole writers (line 68) | S | The first blocking question correctly holds the still-unknown destination transaction; inputs cannot silently settle. |
| Activity trigger and durable pending claim (line 72) | S | Concurrent triggers insert/read one keyed NOTE and only the winner creates the execution wake. |
| Activity terminal fan-out and restart (line 74) | U | Success/failure fan-out is deterministic after a terminal result, but R2-F1 leaves the admitted-call crash interval contradictory. |
| Runtime, light model, no ACP/workdir, and telemetry (line 78) | S | The concrete elected model/effort is used through a bounded direct call. |
| Cutoff-bound baseline query and custody (line 80) | S | Exact command, projection, cutoff, sort, version, output, and SHA-256 are required; the old artifact is provenance only. |
| Main-only pilot report and gate (line 82) | S | Both artifacts and the product-owner decision precede any second worker or layer. |
| Record-minimum and deletion rationale (line 84) | S | BUNDLE is the only new record type; wake and NOTE rows are reused. |
| A1 — Worker target | S | Valid binding yields exec receipt before a worker turn. |
| A2 — Invalid target/configuration | S | Typed refusal precedes wake, assignment, and turn writes. |
| A3 — Timing and algedonic | S | Class cases, Owner Main pass-through, and the no-loop/no-second-carrier cases are testable. |
| A4 — Bundle bound | S | Turn boundary versus deadline wake is decidable and private delay is forbidden. |
| A5 — Direct conservation | S | Restart-visible terminal outcome and no BUNDLE are required. |
| A6 — Failure conservation | S | Deadline expiry retains a queryable source and reason. |
| A7 — Summary cardinality | S | One and three member cases prove `N=1` direct and `N>1` BUNDLE. |
| A8 — Cited annotation | S | The cited durable row and both names are concrete. |
| A9 — Parent escalation | S | Resolver use and source-linked ordinary send are concrete. |
| A10 — Attribution | S | All four exec-authored row kinds expose separate worker and exec fields. |
| A11 — Capability floor | S | Work and decision mutations refuse before effect. |
| A12 — Idle cost | S | An hour with no trigger produces zero queries, calls, and wakes. |
| A13 — Semantic boundary | S | Deterministic paths have no model execution; semantic work cites inputs and policy. |
| A14 — Published-NOTE debounce | S | All check-ins reuse one pointer without a pending row, wake, or call. |
| A15 — Initial single-flight | P | It proves concurrent arrivals, but not the crash interval in R2-F1. |
| A16 — Success fan-out | S | One transaction publishes and settles all linked wakes with one pointer. |
| A17 — Failure fan-out | P | It covers deadline/terminal failure, but not an accepted provider call whose terminal result is lost before commit. |
| A18 — Minimal summary records | S | No observation request or cancellation record may exist. |
| A19 — Honest idle NOTE | S | Literal inactivity and prohibited inference are testable. |
| A20 — Summary privacy | S | NOTE read permission does not grant transcript-body access. |
| A21 — Policy record | S | Historical policy attribution survives later policy changes. |
| A22 — Baseline custody | S | Exact cutoff artifact content and same-row byte reproducibility are testable. |
| A23 — Pilot gate | S | Frozen baseline, before/after report, and continue decision are mandatory. |
| Open Question 1 — delivery-destination transaction | S | It is blocking, singular, and explains the atomicity risk. |
| Open Question 2 — exec-model credential lane | S | It is blocking, singular, and requires a revocable non-worker credential. |
| Eight canonical sections and exactly two blocking open questions | S | All sections exist and only the two final paragraphs are open questions. |
| Plain language, citations, and no-action boundary | S | The policy is readable, cites its authorities, deletes superseded claims, and contains no edit authorization, target/specRef, merge, release, deploy, live mutation, or 0.1.x action. |

## Review lenses

- Completeness: R2-F1 is a missing crash and restart contract, not optional polish.
- YAGNI: no unrequested capability, record type, or implementation surface was found.
- Law split: routing and enforcement remain deterministic; only semantic prose and
  judgments use the model. R2-F1 is the remaining deterministic bracket around that
  inference.

Mike's reading gate remains separate and closed.
