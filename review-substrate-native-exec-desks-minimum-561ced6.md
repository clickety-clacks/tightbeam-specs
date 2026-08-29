# Independent exact-successor review — substrate-native exec desks minimum

Reviewed assignment: `asg_9a6b61c1-6e74-4013-b35a-d82ba244233d`

Reviewed producer assignment: `asg_c37b6b1a-5258-45e0-b196-010911f5c1b1`

Reviewed commit: `561ced6d0c7df35f5a3979b3d11185f752b32409`

Reviewed file: `substrate-native-exec-desks-v1.md`

Reviewed file SHA-256: `d7af572be867dafd67f9dba48d7b29aad6c4448999d62c0676734675abf26db3`

Verdict: **changes-requested**

## Custody and scope

- A fresh reviewer-owned Gibson clone resolved
  `origin/spec/substrate-native-exec-desks-v1-minimum` to the exact reviewed commit.
- Its sole parent is
  `7a13f97d6f418d2bf3104828619d6d6073aebf57`; the ancestry continues through
  `d9fd29e22b197e3eaf511e70c7a045ec64f6f178`.
- The reviewed tree is `8a805c74fa312c0acaaab8033a73e2c73e7c4b49`.
- The parent-to-successor diff modifies only `substrate-native-exec-desks-v1.md`:
  six insertions and six deletions. `git diff --check` passed.
- The initial review worktree was clean. The independently computed file hash matches
  producer artifact `art_39076e8a` and readiness receipt `att_5845454a`.
- The full `wi_795a354d` trace, Mike rewrite order `att_7ccdd6bf`, algedonic
  ruling `att_6b976672`, reviewed provenance `ac965ae3`, receiving evidence
  `art_a4f39376` as reproduced in the prior review record, prior verdict
  `att_b51166b7` and report `art_cc34685b`, and marker finding
  `att_a8128cf6` were read.
- No implementation, target/specRef, integration, Mike-reading, release, deployment,
  credential, identity, runtime, history, or live-state action is present in the exact
  commit or this review.

## Repair disposition

| Required repair | Result | Evidence |
|---|---:|---|
| Semantic-start marker attribution | Repaired | Lines 30, 53, 74, 102, and 104 require one nullable tuple containing time, cause `wake:<execution-wake-id>`, and principal `process:tightbeam`. |
| Provider-call single-flight across restart | Repaired | Line 74 admits the provider only for the null-to-tuple winner; a started nonterminal NOTE settles `outcome_unknown` after restart and never calls again. |
| Failure fan-out | Repaired | Lines 74 and 104 settle the execution wake and every linked check-in in one failure transaction, including the crash interval. |
| Failed NOTE/window branch | Repaired | Line 72 explicitly partitions absent, pending, published, and failed rows and makes terminal rows inert for worker-turn completion. |
| Baseline custody | Repaired | Lines 80 and 109 provide one exact compact, sorted, cutoff-bound executable pipeline and artifact custody; `art_a4f39376` is seed provenance only. |
| Algedonic source conservation | Unsatisfied | F1: the new source link exists, but the source is terminally marked `handled` at child admission rather than child delivery. |
| Algedonic two-name attribution | Unproven | F2: the newly specified forwarding action has no clause requiring its durable record to name both the represented worker and performing exec. |

## Findings

### F1 — blocking — algedonic admission is not a handled source outcome

The algedonic routing transaction creates and admits one Owner-Main wake, then records
`handled` as the source wake outcome
(`substrate-native-exec-desks-v1.md:62`; A3 at line 90). Admission only proves that the
new carrier wake and queued turn exist. It does not prove that the carrier turn delivered.

The spec names `wake-delivery-conservation.md` as the authority for admission, outcomes,
retry, and restart (Assumption 5 at line 39), and says direct delivery uses its terminal
outcome rules (line 64). That governing spec defines admission as a queued, not-yet-run
turn; defines `handled` only when the linked turn reaches
`turns.status='delivered'` and the same terminal transaction writes the outcome
(`wake-delivery-conservation.md:118-128`); repeats the atomic terminal rule at
lines 248-256; and makes `handled` mutually final with `undeliverable` at
lines 310-314.

If the Owner-Main child later becomes undeliverable, the source remains falsely
`handled`. The source-child link preserves traceability, but it does not change the
meaning or timing of the terminal outcome. This contradicts Invariant 3's visible-outcome
claim and makes A3 incompatible with the governing outcome vocabulary.

Deletion test: removing the source outcome restores the original silent-source hole.
Removing the child link loses custody. Accepting admission as handled destroys the
delivered-versus-admitted distinction that conservation exists to preserve. The contract
must define how the source follows the linked carrier's real terminal result, without
repurposing `handled`.

### F2 — blocking — algedonic forwarding omits two-name attribution

The non-Main algedonic path is an exec-performed durable forwarding action. It creates an
Owner-Main wake, a source link, and a source outcome, but the architecture and A3 require
none of those rows to record the original worker represented by the exec and the exec that
performed the action (`substrate-native-exec-desks-v1.md:62,90`).

Invariant 5 requires an exec-authored escalation to record both names, and A10 makes the
fields independently inspectable (lines 50 and 97). Mike's minimum rewrite order requires
two-name attribution without exempting deterministic algedonic routing. The destination
wake names Owner Main, not the represented source worker; the source link does not by
itself freeze the performing exec, whose active binding can later change.

Deletion test: deleting algedonic forwarding violates Mike's routing ruling. Accepting
derivable current bindings loses historical actor identity. The algedonic forwarding
record must carry the same represented-worker and performing-exec attribution required
for other exec-authored escalations.

## Clause table

`S` = satisfied. `U` = unsatisfied. `P` = unproven. `OOS` = out of scope.

| Clause | Result | Evidence |
|---|---:|---|
| Authority, canonical home, and successor lineage (lines 1-3) | S | Work item, Mike rulings, prior verdicts, canonical path, immediate parent, and provenance revisions are explicit. |
| Goal: worker-addressed exec; now or next bundle only (lines 5-9) | S | The worker remains the public target; the exec has two timing choices and no work authority. |
| Goal: one Main pilot before expansion (line 9) | S | The before cohort is reproducible and the expansion gate is explicit. |
| Non-Goals 1-2: inbound only; no exec address, recursion, ACP, workdir, shell, repository, filesystem, or assignment (lines 13-14) | S | The architecture uses one worker-row binding and bounded direct provider calls. |
| Non-Goals 3-4: no work/decision authority and no observation request/cancel rows (lines 15-16) | S | I6, A11, and A18 enforce both exclusions. |
| Non-Goals 5-7: independent batcher; no org/target/0.1.x decision; no premature guidance (lines 17-19) | S | The exact commit changes one draft policy file and authorizes none of those actions. |
| Terms: Worker, Owner Main, and Exec (lines 23-25) | S | Addressability, recorded ownership, non-recursion, and representation are decidable. |
| Terms: BUNDLE and SUMMARIZE (lines 26-27) | S | Ordered membership and strict `N > 1` creation are explicit. |
| Terms: ANNOTATE and ESCALATE (lines 28-29) | S | Citations and source-linked authority sends are explicit. |
| Term: Activity-summary NOTE (line 30) | S | States, fields, semantic-start tuple, terminal outcomes, provenance, and literal-idle behavior are defined. |
| Term: Org policy (line 31) | S | Timing and model choices remain versioned org input, not substrate inference. |
| Assumptions 1-4 (lines 35-38) | S | Persisted wakes, landed class, resolver, and concrete model catalog each name a governing seam. |
| Assumption 5: wake conservation authority (line 39) | U | F1: the algedonic source outcome contradicts the authority's definition of `handled`. |
| Assumption 6: baseline fields (line 40) | S | The exact projection uses the listed retained fields. |
| Assumptions 7-8: NOTE privacy and provider telemetry (lines 41-42) | S | Both are explicit, falsifiable prerequisites. |
| I1 — worker address and exec delivery (line 46) | S | Exec addressing is unrepresentable and the bound exec precedes any worker turn. |
| I2 — only now or next bundle (line 47) | S | No later/private priority exists. |
| I3 — visible outcome and conservation (line 48) | U | F1: the source can say handled before its linked delivery has a terminal result. |
| I4 — three verbs (line 49) | S | `SUMMARIZE`, cited `ANNOTATE`, and resolver-backed parent `ESCALATE` remain the complete exposed set. |
| I5 — two-name attribution (line 50) | P | F2: algedonic forwarding is not required to retain both names. |
| I6 — no work authority (line 51) | S | The closed write surface excludes work and decision state. |
| I7 — event-driven shell/model split (line 52) | S | Durable triggers, deterministic routing, semantic-only model use, deadlines, and zero-idle behavior are explicit. |
| I8 — NOTE single-flight and fan-out (line 53) | S | The attributed tuple, one checked winner, terminal fan-out, and no-turn check-in path are complete. |
| I9 — policy remains policy (line 54) | S | Results retain their elected revision and the substrate derives no replacement policy. |
| Inbound binding and atomic acceptance (line 60) | S | The worker row holds the binding; invalid configuration refuses before listed writes; no extra binding or envelope row exists. |
| Class precedence and algedonic route (line 62) | U | Destination, fixed point, and carrier count are correct, but F1 and F2 make the durable forwarding result incomplete. |
| Bundle boundary and deadline wake (line 64) | S | Earlier-of closure, one durable wake, no polling, direct `N=1`, and BUNDLE `N>1` are explicit. |
| Annotation, escalation, resolver, and authorization (line 66) | S | Citation, ordinary send, transaction-aware resolution, and caller authorization are preserved. |
| Delivery atomicity, replay, expiry, and sole writers (line 68) | S | The first blocking question correctly holds the destination transaction; failures cannot silently settle. |
| Activity trigger state partition (line 72) | S | Absent, pending, published, and failed NOTE/window cases are deterministic and transcript privacy is preserved. |
| Semantic start, terminal fan-out, and restart (line 74) | S | The marker precedes admission, has time/cause/principal, has one CAS winner, and outcome-unknown restart settles all wakes without a second call. |
| Runtime: light elected model, direct call, no ACP/workdir (line 78) | S | Concrete model/effort and bounded telemetry are explicit; credentials remain a blocking question. |
| Exact cutoff-bound baseline pipeline (line 80) | S | One executable compact pipeline fixes cutoff, filter, projection, ordering, and artifact custody. |
| Main pilot report and expansion gate (line 82) | S | Both artifacts and the product-owner continue decision precede a second worker or layer. |
| Record minimum and subtraction rationale (line 84) | S | BUNDLE is the only new record type; wake and NOTE rows are reused. |
| A1 — Worker target | S | Valid binding yields exec receipt before a worker turn. |
| A2 — Invalid target/configuration | S | Typed refusal precedes wake, assignment, and turn writes. |
| A3 — Timing and algedonic | U | F1 and F2; routing destination is decidable, but its source terminal and attribution are not conformant. |
| A4 — Bundle bound | S | Turn boundary versus deadline and no private delay are testable. |
| A5 — Direct conservation | S | A direct delivery has one restart-visible terminal outcome and no BUNDLE. |
| A6 — Failure conservation | S | Deadline expiry preserves the source and reason. |
| A7 — Summary cardinality | S | One and three member cases prove direct versus one ordered BUNDLE. |
| A8 — Cited annotation | S | Citation plus represented-worker and performing-exec fields are concrete. |
| A9 — Parent escalation | S | Resolver use and source-linked ordinary send are concrete. |
| A10 — Attribution | P | F2: the enumerated rows are decidable, but the new algedonic forwarding action is omitted. |
| A11 — Capability floor | S | Attest, transition, ruling, and other work mutations refuse before effect. |
| A12 — Idle cost | S | A trigger-free hour produces zero exec queries, calls, and wakes. |
| A13 — Semantic boundary | S | Pass-through and stored replies use no model; semantic work cites inputs and policy. |
| A14 — Debounce | S | Published NOTE reuse starts no pending row, execution wake, or call. |
| A15 — Initial single-flight | S | Concurrent triggers yield one NOTE, one wake, one attributed tuple winner, and no second call. |
| A16 — Success fan-out | S | One transaction publishes, settles the execution wake, and gives all waiters one pointer. |
| A17 — Failure fan-out and restart | S | Terminal failure and post-start restart settle every linked wake with one cause and no replayed provider call. |
| A18 — Minimal summary records | S | Observation request and cancellation records remain absent. |
| A19 — Honest idle NOTE | S | Literal inactivity and prohibited health/progress/cause inferences are testable. |
| A20 — Summary privacy | S | NOTE authorization does not disclose transcript evidence bodies. |
| A21 — Policy record | S | Historical policy attribution survives later policy changes. |
| A22 — Baseline custody | S | Exact pipeline, fixed cutoff, version, compact sorted bytes, and SHA-256 are required. |
| A23 — Pilot gate | S | Frozen baseline, before/after report, and continue decision are mandatory. |
| Open Question 1 — delivery-destination transaction | S | It is blocking, singular, and explains the atomicity risk. |
| Open Question 2 — exec-model credential lane | S | It is blocking, singular, and requires a revocable non-worker credential. |
| Eight canonical sections and exactly two blocking questions | S | All canonical sections exist; only the final two paragraphs are open questions and both are marked blocking. |
| Plain language, citations, deletions, and no-action gates | S | The draft is readable, cites governing specs, retains the minimum record set, and contains no implementation, target/specRef, integration, Mike-read, release, deployment, credential, identity, runtime, history, live-state, or 0.1.x action. |

## Review lenses

- Completeness: F1 is the missing terminal propagation rule; F2 is missing historical
  actor attribution on the newly durable forwarding path.
- YAGNI: no unrequested capability, record type, or implementation surface was found.
- Law split: semantic-start is now a correctly attributed deterministic marker, and
  model use is confined to semantic work. F1 and F2 concern deterministic outcome law.

Mike's reading gate remains separate and closed.
