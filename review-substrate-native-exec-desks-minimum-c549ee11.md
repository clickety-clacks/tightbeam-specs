# Independent exact-successor review — substrate-native exec desks minimum

Reviewed assignment: `asg_a8e0ee31-ddd3-4805-abde-94514beece6d`

Reviewed producer: `asg_c37b6b1a-5258-45e0-b196-010911f5c1b1`

Reviewed commit: `c549ee110da9ba73bc710a81c9d3e722b098a873`

Reviewed file: `substrate-native-exec-desks-v1.md`

Reviewed file SHA-256: `31caa5b616cc331c7998f55ef01840ac8b10ab8d06ee05b236d4f0f56b1c12af`

Verdict: **reviewed-clean**

## Custody and independent evidence

- A fresh reviewer-owned Gibson clone resolved remote branch
  `origin/spec/substrate-native-exec-desks-v1-minimum` to the exact reviewed commit.
  Its sole parent is reviewed changes-requested commit
  `4af894567ff070c5ffee76b635dd2990a44f355d`.
- The parent-to-successor diff changes only `substrate-native-exec-desks-v1.md`;
  `git diff --check` passed.  `git show <commit>:<file> | sha256sum` produced the
  recorded hash.  The review clone was clean before this report was added.
- I read the complete reviewed specification, `wake-delivery-conservation.md`, the
  work-item trace and relevant producer/reviewer attests, Mike's minimum-rewrite
  order `att_7ccdd6bf-48f6-46c4-86f4-f96609594e8f`, his algedonic ruling
  `att_6b976672-6456-486a-808e-8ecbebcadb5f`, the previous changes-requested
  verdict `att_438b15ed-44ff-4335-9859-653448617a00`, and its immutable report
  `art_ac4d4db7`.
- This is a policy-specification review.  There is no implementation or
  code-test receipt to evaluate; producer readiness is `att_4dfc2e7f`.  As a
  proportional real-input check, the exact A22 baseline command ran successfully
  against the live decision-request rows under `tightbeam` 0.1.8 and emitted valid
  compact JSON.  This review did not artifact-record or otherwise mutate that
  baseline.

## Repair regression

The prior F1 was a source-terminal mirror that could not be represented: the child
turn's `wakeId` could not legally back a source wake's `handled` outcome under the
same-wake foreign key and terminal rules in `wake-delivery-conservation.md`.

The successor replaces that child with the source wake as the sole Owner-Main
carrier.  The carrier turn has the source wake id and records both represented worker
and performing exec (`substrate-native-exec-desks-v1.md:62,90,97`).  It therefore
uses the governing contract's normal same-wake `handled`, retry, and
`undeliverable` lifecycle.  No cross-wake terminal outcome remains.  Main is the
fixed point because a source already addressed to Owner Main creates no carrier wake.
The restart, attribution, and conservation rules are explicit and testable in A3.

## Clause table

`S` means the reviewed text satisfies the clause.  This table evaluates the policy
text, not an unbuilt implementation.

| Clause | Result | Evidence |
|---|:---:|---|
| Authority, canonical home, exact custody | S | Header and remote/parent/hash proof above; spec lines 1-3. |
| Goal and one-Main pilot | S | Worker-addressed delivery, now-or-bundle boundary, and cohort comparison; lines 5-9. |
| All non-goals and operating-guidance disposition | S | Explicit exclusions, including no work authority and no premature guidance; lines 11-19. |
| Worker, Owner Main, Exec terms | S | Addressability, owner resolution, non-recursion, and no public exec address are defined; lines 21-25. |
| BUNDLE and three verb terms | S | Cardinality, citations, and source linkage are defined; lines 26-29. |
| NOTE and policy terms | S | State, attribution, privacy boundary, honest-idle text, and policy/non-truth split are defined; lines 30-31. |
| Assumptions 1-4 and 6-8 | S | Existing wake, class, resolver, model, history, authorization, and telemetry seams are named; lines 35-42. |
| Assumption 5, conservation authority | S | The source carrier now uses its own wake id, so its linked turn satisfies the authority's same-wake outcome linkage; lines 39, 62. |
| I1-I2, worker-only address and timing bound | S | Exec delivery precedes a worker turn; the only timing choice is now or bounded next bundle; lines 46-47. |
| I3, visible outcome | S | Direct source wake has its own governed terminal outcome; BUNDLE outcomes are explicit; line 48 and A3/A5/A6. |
| I4-I6, verbs, attribution, no work authority | S | Closed verb set; all exec writes retain worker/exec names; work and decision writes are excluded; lines 49-51. |
| I7-I9, event/model split, NOTE single-flight, policy | S | Durable triggers only, deterministic shell, semantic-call boundary, fan-out, and recorded policy revision are explicit; lines 52-54. |
| Inbound acceptance and refusal | S | One transaction reads worker binding or refuses before named writes; line 60 and A1-A2. |
| Algedonic routing, fixed point, restart, conservation | S | Same source wake carries the Owner-Main turn; no child/cross-wake outcome; preserved content/class, retry, and terminal behavior are explicit; line 62 and A3. |
| Bundle delivery, annotations, escalation | S | Earlier boundary/deadline, N>1 BUNDLE, cited rows, resolver, and normal authorization are specified; lines 64-66 and A4/A7-A9. |
| Delivery atomicity and failures | S | Delivery/outcome commit is one transaction; replay, expiry, and model failure have durable outcomes; line 68. |
| NOTE transition, restart, privacy | S | Insert-or-read state partition, semantic-start winner, one call, terminal fan-out, and `outcome_unknown` restart settlement are explicit; lines 72-74 and A14-A20. |
| Runtime and credential boundary | S | Policy-elected bounded direct call has no ACP or workdir; credential lane is marked blocking; line 78. |
| A22 baseline custody | S | One executable cutoff-bound pipeline, version, compact output, and SHA custody are specified; line 80 and A22. |
| Pilot expansion gate | S | Required before/after measures and recorded PO decision precede expansion; line 82 and A23. |
| Subtraction / record scope | S | BUNDLE is the sole added record; deletion and acceptance alternatives are decided; line 84. |
| A1-A2 | S | Worker target, exec target/configuration refusal, and no-write result are decidable; lines 88-89. |
| A3 | S | Timing inputs plus source-wake Owner-Main carrier, same-wake handled/undeliverable, and Owner-Main fixed point are decidable; line 90. |
| A4-A10 | S | Bundle deadline, conservation, cardinality, cited annotation, resolver escalation, and two-name attribution are concrete; lines 91-97. |
| A11-A13 | S | Capability refusals, zero idle cost, and model/no-model boundary are concrete; lines 98-100. |
| A14-A19 | S | Debounce, initial single-flight, success/failure fan-out, restart, minimal records, and honest-idle wording are concrete; lines 101-106. |
| A20-A21 | S | NOTE-only access and policy-revision retention are concrete; lines 107-108. |
| A22-A23 | S | Baseline bytes and expansion evidence are concrete; lines 109-110. |
| Open questions | S | Exactly two, each explicitly BLOCKING and implementation-gating; lines 112-116. |
| Canonical spec structure | S | Goal, Non-Goals, Terms, Assumptions, Invariants, Architecture, Acceptance, and Open Questions are all present; eight headings. |

## Review lenses

- Completeness: no previously missing lifecycle remains.  The source wake, not an
  unrepresentable child mirror, owns the terminal outcome; NOTE restart/fan-out and
  pilot custody remain covered.
- YAGNI: the five-line repair removes an invalid cross-wake design without adding a
  record type, capability, policy, target, or implementation surface.
- Subtraction: deletion of F1's source carrier restores either source loss or
  unrepresentable cross-wake settlement; accepting a cross-wake outcome violates
  `wake-delivery-conservation.md`.  The source-carrier replacement is the smallest
  lawful closure.

No blocking or important finding remains.  Mike reading, implementation, target
selection, integration, release, and live-state changes remain outside this review.
