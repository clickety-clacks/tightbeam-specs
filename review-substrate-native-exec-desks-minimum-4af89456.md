# Independent exact-successor review — substrate-native exec desks minimum

Reviewed assignment: `asg_45b2b6e0-77c7-4df6-9702-30c3df6d767a`

Reviewed producer assignment: `asg_c37b6b1a-5258-45e0-b196-010911f5c1b1`

Reviewed commit: `4af894567ff070c5ffee76b635dd2990a44f355d`

Reviewed file: `substrate-native-exec-desks-v1.md`

Reviewed file SHA-256: `8c61e7af876bac0c35c3e811244495a5b59aeef0dc4cdf93798f60b7052b9be4`

Verdict: **changes-requested**

## Custody and review boundary

- A fresh reviewer-owned Eezo clone resolved
  `origin/spec/substrate-native-exec-desks-v1-minimum` to the exact reviewed commit.
- Its sole parent is `561ced6d0c7df35f5a3979b3d11185f752b32409`.
  The parent-to-successor diff changes only `substrate-native-exec-desks-v1.md`
  (five insertions and five deletions); `git diff --check` passed.
- The independently calculated file SHA-256 equals the producer receipt
  `att_5cdecc1f-0932-472d-8b9a-3b34165bea4f` and spec artifact
  `art_00fa3eaa`.
- I read the full producer attests, the full work-item assignment history, Mike's
  minimum-rewrite order `att_7ccdd6bf-48f6-46c4-86f4-f96609594e8f`, Mike's
  algedonic ruling `att_6b976672-6456-486a-808e-8ecbebcadb5f`, prior
  changes-requested verdict `att_6f42c78a-6a5d-4750-b918-55053f209828`, and
  its immutable report `art_438dfbdf`.
- I read the `art_a4f39376` artifact record. Its payload is not locally available
  on Eezo (`/home/mike/.tightbeam/work/4b8707f483fe/adjudication-ledger.md` is
  absent), and authenticated Gibson access was unavailable to this reviewer. This
  does not block the draft because lines 80 and A22 make that artifact seed
  provenance only and bind the pilot to a new cutoff-bound query artifact.
- This is a policy/specification review, not code. No test receipt or executable
  implementation exists to review. Mike reading, implementation, integration, and
  live-state actions remain outside this review.

## Finding

### F1 — blocking — the source-terminal mirror is not representable under the named wake-conservation authority

The successor correctly repairs the old premature-outcome defect in prose: its
algedonic route leaves the source nonterminal when it creates the Owner-Main child,
then says the child's terminal transaction records the source as `handled` or
`undeliverable` (`substrate-native-exec-desks-v1.md:62`; A3 at line 90). It also
correctly requires the child to retain source, represented-worker, and performing-exec
attribution (lines 50, 62, 90, and 97).

But the same draft names `wake-delivery-conservation.md` as the continuing authority
for wake admission, terminal outcomes, retry, and restart (Assumption 5, line 39),
and says direct delivery uses its terminal-outcome rules (line 64). That authority
defines `handled` as the terminal state of the linked turn for *that wake*
(`wake-delivery-conservation.md:123-128`), requires any `handled` outcome to name a
turn (`:228-236`), and enforces the linkage with
`FOREIGN KEY (turnSeq, wakeId, attemptNo) REFERENCES turns(seq, wakeId, wakeAttempt)`
(`:472-498`). The child terminal turn therefore cannot be used as the source wake's
`handled` outcome: its `wakeId` is the child, not the source. The closed mutation
seam also permits `handled` only with cause `turn_terminal` and `turn:<turnSeq>`
(`:535-544`), while the source's proposed terminal event is the child's outcome.

The draft supplies neither a source-linked carrier turn nor an explicit, reviewed
change to the authority that makes a child terminal result a legal source outcome.
Two incompatible implementations follow from the current words: one attempts an
invalid cross-wake outcome link; the other invents a new source-outcome representation
or treats the child as the source carrier. The latter two options change the governing
contract but are not specified.

Deletion test: deleting the mirror restores the admitted-but-unsettled source hole;
deleting the child loses Owner-Main routing; accepting an invalid cross-wake terminal
outcome violates the authority that this draft adopts. The required closure is a lawful,
explicit representation and transaction rule for source settlement, or a separately
reviewed amendment that changes the named wake-conservation authority. Adding another
record type without that authority would not close the contradiction.

## Clause table

`S` = satisfied. `U` = unsatisfied. `OOS` = out of scope for this policy-only review.

| Clause | Result | Evidence |
|---|:---:|---|
| Authority, canonical home, exact successor lineage (lines 1-3) | S | Exact remote custody, parent, scope, and hash proved above. |
| Goal: worker-addressed delivery and only now/next-bundle timing (lines 5-8) | S | Worker remains public target; exec has no work authority. |
| Goal: one-Main pilot before expansion (line 9) | S | Baseline and expansion gate are explicit. |
| Non-goals: no outbound mediation, exec address/recursion, ACP/workdir/shell/filesystem/assignment (lines 13-14) | S | Explicit exclusions and direct provider call boundary. |
| Non-goals: no work/decision mutation; no observation request/cancel records (lines 15-16) | S | I6, A11, and A18 make both decidable. |
| Non-goals: independent batcher; no target/org/0.1.x decision; no premature guidance (lines 17-19) | S | Explicit exclusions; no corresponding action is in the commit. |
| Terms: Worker, Owner Main, Exec (lines 23-25) | S | Addressability, ownership resolution, representation, and non-recursion are defined. |
| Terms: BUNDLE, SUMMARIZE, ANNOTATE, ESCALATE (lines 26-29) | S | Cardinality, citations, and source linkage are concrete. |
| Term: activity-summary NOTE and semantic-start tuple (line 30) | S | States, attributed start marker, terminal forms, evidence, and honest-idle content are specified. |
| Term: org policy (line 31) | S | Policy selects inputs; substrate does not derive it. |
| Assumptions 1-4, 6-8 (lines 35-38, 40-42) | S | Each names an existing persisted/class/resolver/model/baseline/privacy/telemetry seam. |
| Assumption 5: wake-conservation authority (line 39) | U | F1: the proposed source mirror lacks a representation legal under that authority. |
| I1 worker address and exec delivery (line 46) | S | Exec targets are unrepresentable and delivery precedes worker turn. |
| I2 timing bound (line 47) | S | No private priority or delay beyond next boundary. |
| I3 visible outcome/conservation (line 48) | U | F1: source terminal propagation is undefined in the authoritative outcome store. |
| I4 three verbs (line 49) | S | `SUMMARIZE`, `ANNOTATE`, and `ESCALATE` are the named exec capabilities; deterministic routing is separately stated. |
| I5 two-name attribution (line 50) | S | The child wake is expressly included; A3/A10 make it inspectable. |
| I6 no work authority (line 51) | S | Closed permitted writes exclude work and decision state. |
| I7 deterministic/event-driven semantic split (line 52) | S | Durable triggers, deterministic shell, model-only semantic use, and zero idle activity are explicit. |
| I8 NOTE single-flight, terminal fan-out, and no worker turn for check-ins (line 53) | S | A14-A19 and architecture provide matching cases. |
| I9 policy stays policy (line 54) | S | Historical policy revision is retained without inference. |
| Inbound binding and atomic refusal (line 60) | S | Worker fields are read in one acceptance transaction; refusal precedes named writes. |
| Class use and algedonic routing (line 62) | U | Destination, content preservation, fixed point, restart reuse, and attribution are clear; F1 leaves the terminal source write impossible under the adopted authority. |
| Bundle deadline and cardinality (line 64) | S | Earlier-of boundary/deadline, one deadline wake, direct one-member delivery, and `N > 1` BUNDLE are explicit. |
| Annotation/escalation and effective-parent authorization (line 66) | S | Citation, ordinary source-linked send, resolver, and existing authorization are explicit. |
| Delivery atomicity, replay, expiry, model failure, sole writers (line 68) | S | The unresolved destination is correctly held as a blocking question; the rest is determinate. |
| NOTE state partition and privacy (line 72) | S | Absent/pending/published/failed rows and check-in results are complete. |
| Semantic-start admission, terminal fan-out, and restart (line 74) | S | Nullable tuple winner, one call, `outcome_unknown`, and no replay are explicit. |
| Direct light-model runtime and credential boundary (line 78) | S | Policy-elected direct call, no ACP/workdir, telemetry, and blocking credential question. |
| Exact baseline pipeline/custody (line 80) | S | One cutoff-bound, compact, sorted pipeline and new artifact requirements; `art_a4f39376` is provenance only. |
| Pilot report and expansion gate (line 82) | S | Required measures and recorded product-owner decision precede expansion. |
| Minimal-record/subtraction rationale (line 84) | S | BUNDLE is the only added record; delete/accept alternatives are stated. |
| A1-A2 worker target and invalid configuration | S | Concrete acceptance cases and typed no-write refusal. |
| A3 timing and algedonic path | U | F1: it requires a source terminal kind without a legal source-outcome linkage. |
| A4-A10 bundle bound, direct/failure conservation, cardinality, annotation, parent escalation, attribution | S | Each has a concrete input/outcome; A10 now includes algedonic child wake. |
| A11-A13 capability floor, idle cost, semantic boundary | S | Deterministic refusal/zero-work/model-use expectations are decidable. |
| A14-A19 debounce, single flight, success/failure fan-out, minimal rows, honest note | S | Concurrent and restart cases cover the NOTE lifecycle. |
| A20-A21 privacy and historical policy | S | Principal-visible NOTE only and retained revision are explicit. |
| A22-A23 baseline custody and pilot gate | S | Exact rerunnable bytes and required expansion evidence are specified. |
| Open question: delivery-destination transaction (line 114) | S | It is singular, blocking, and names the atomicity risk. |
| Open question: exec-model credential lane (line 116) | S | It is singular, blocking, and names the revocable non-worker credential constraint. |
| Eight canonical sections; exactly two blocking questions; operating guidance disposition | S | All required sections exist; line 19 explicitly states guidance remains unchanged. |

## Review lenses

- Completeness: F1 is the missing lawful source-settlement representation.
- YAGNI: the successor introduces no new unrequested capability, record type, or
  implementation surface. The sole disputed mechanism is required but not yet legally
  specified.
- Subtraction: deletion cannot close F1 without restoring either silent source loss or
  lost escalation routing; a new law must be explicit before a mechanism is added.

Mike's later reading gate remains separate.
