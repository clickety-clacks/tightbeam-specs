# Independent review — substrate-native exec desks minimum rewrite

Reviewed producer assignment: `asg_c37b6b1a-5258-45e0-b196-010911f5c1b1`

Reviewed commit: `0767558eccfcdee974bee9d2b426c74e6f92fcc6`

Reviewed file: `substrate-native-exec-desks-v1.md`

Reviewed file SHA-256: `57f34d39130d65f24cf4a1d6622bb08c8f84b70888940583369fe37e90f20869`

Verdict: **changes-requested**

## Custody and scope

- A fresh owned Gibson clone resolved remote branch
  `origin/spec/substrate-native-exec-desks-v1-minimum` to the reviewed commit.
- The sole parent is canonical base
  `b20194fe464f5792788bb5b7033245e4d0696889`.
- The commit tree is `251639fb22bb344b9aa18df7f53d68b5ebbe7161`.
- `git diff --check HEAD^ HEAD` passed.
- The commit adds only `substrate-native-exec-desks-v1.md`: 110 inserted lines and
  no other changed path.
- The reviewed predecessor `ac965ae33852d6890b6ae2624d9a899fed1722cb`
  is provenance, not an ancestor. The new commit starts from canonical main and
  names that predecessor explicitly.
- Producer artifact `art_28c8d9a5` and receipt `att_719cf7ec` match the reviewed
  branch, commit, parent, path, and file hash. The producer remains open pending
  this different-session review.

## Findings

### F1 — blocking — algedonic routing retains superseded behavior

The class sentence says an algedonic wake goes `now`, replaces the governing
spec's desk bypass for an exec-bound worker, and preserves configured human-channel
delivery (`substrate-native-exec-desks-v1.md:61`; A3 at line 87). The governing
revision at this exact commit still says algedonic bypasses every desk and delivers
to both the principal and an org-configured human channel
(`coordination-fabric-v1.md:560-566,596-602`). Mike's later durable ruling
`att_6b976672-6456-486a-808e-8ecbebcadb5f` instead says algedonic reaches Main,
no intermediate agent may answer, absorb, triage, or reclassify it, Main is the
user boundary, and the fabric owns no second human carrier.

The reviewed text neither requires the Main route nor removes the second carrier.
It therefore permits the obsolete addressed-worker-plus-human-channel behavior on
the exact governing set it cites. This is a core pain-signal routing defect.

Deletion test: deleting only the obsolete human-channel phrase does not establish
the required Main route. Deleting class handling loses the rewrite order. Accepting
the mismatch can misroute a pain signal. The contract must consume the landed
retain-five ruling and make algedonic handling deterministic pass-through routing,
not intermediate exec judgment.

### F2 — blocking — NOTE debounce serializes publication, not semantic work

The activity path says one trigger may stage a bounded transcript window, and a
unique worker/window key permits one initial NOTE
(`substrate-native-exec-desks-v1.md:71-73,99`). It does not define a durable
single-flight claim before the provider call. With no current NOTE, concurrent
check-ins or a check-in racing worker-turn completion can each stage semantic work;
the unique NOTE key can reject duplicate publication only after multiple model
calls already ran. The failure branch is also singular (`its check-in wake`) and
does not settle the other concurrent check-ins.

This contradicts the governing execution-model evidence `art_c03cbbd5`, which
requires recomputation at most once per debounce window and model cost that scales
with semantic work rather than traffic volume. A15 proves one NOTE, not one
recomputation or one bounded model execution.

Deletion test: deleting initial NOTE generation loses the required check-in
capability. Accepting duplicate calls rebuilds the check-in-volume cost this design
exists to remove. The existing NOTE/window seam must deterministically serialize
semantic execution and define success or failure fan-out for every concurrent
check-in, without adding an unrequested record type.

### F3 — important — the claimed frozen Main baseline is not reproducible

Assumption 6 calls `art_a4f39376` a frozen receiving-end baseline, and the pilot
must use it (`substrate-native-exec-desks-v1.md:39,79,104`). The artifact row records
SHA-256 `7dd588ce58896842132aedf33c9fecafb4b3e05510b92fdc1aa7fb06055ca937`
for `/home/mike/.tightbeam/work/4b8707f483fe/adjudication-ledger.md`. Independent
rehash produced
`1f0f3c2cbd745391793d1ed7af00d178baaae8a5e1cf037ded265ea271defb04`.
No second `adjudication-ledger.md` exists under the durable work roots, and the
origin directory is not a Git repository. The exact recorded bytes and rerunnable
query are therefore unavailable from the cited artifact.

Deletion test: deleting the baseline removes the required before/after pilot.
Accepting an unavailable baseline makes A20 untestable. Capture a real immutable
baseline or a complete rerunnable query with a frozen cutoff before this citation
can support the pilot gate.

## Clause table

`S` = satisfied, `U` = unsatisfied, `P` = unproven, `OOS` = out of scope.

| Clause | Result | Evidence |
|---|---:|---|
| Canonical home, authority, predecessor, review status (lines 1-3) | S | Exact repository, path, work item, authority row, and predecessor are named. |
| Goal: worker-addressed inbound exec and now/next-bundle choice (line 7) | S | Stated directly and carried through I1-I2/A1-A4. |
| Goal: one Main pilot before expansion (line 9) | U | F3; the required before baseline is not retrievable. |
| Non-Goals 1-2: inbound only; no exec address/exec/ACP/workdir/shell/filesystem/assignment (lines 13-14) | S | Architecture uses worker targeting, a session-row binding, and direct provider calls only. |
| Non-Goals 3-4: no work authority; no observation request/cancel records (lines 15-16) | S | I6/A11 and A16 cover both exclusions. |
| Non-Goals 5-7: notice batcher independent; no org/target/0.1.x choice; no premature guidance (lines 17-19) | S | No extra file, target, specRef, implementation, or guidance change exists. |
| Terms: Worker and Exec (lines 23-24) | S | Addressability and no-recursion meanings are decidable. |
| Terms: BUNDLE and SUMMARIZE (lines 25-26) | S | Ordered members and N greater than one are explicit; A7 is decidable. |
| Terms: ANNOTATE and ESCALATE (lines 27-28) | S | Citations and source-linked worker send are stated; parent resolution is separately tested. |
| Terms: Activity-summary NOTE (line 29) | U | F2; the durable NOTE is defined, but the pre-NOTE semantic single-flight is not. |
| Term: Org policy (line 30) | S | Policy inputs and substrate boundary are explicit. |
| Assumptions 1-5: persisted wake, landed class, resolver, catalog, conservation (lines 34-38) | S | Each names a governing existing seam/spec. |
| Assumption 6: frozen receiving baseline (line 39) | U | F3; row hash and current bytes differ, with no immutable copy/query. |
| Assumptions 7-8: NOTE-read separation and provider telemetry (lines 40-41) | S | Both are explicit, falsifiable prerequisites. |
| I1 Worker address, exec delivery (line 45) | U | F1 for algedonic: exact governing text and later ruling conflict with the stated override. |
| I2 One timing choice (line 46) | S | Only now/next bundle and no private reordering are stated. |
| I3 Visible outcome (line 47) | S | Direct wake or BUNDLE outcome and no silent loss are explicit; OQ1 blocks the transaction seam. |
| I4 Three verbs (line 48) | S | Cardinality, citation, and resolver requirements are explicit. |
| I5 Two names (line 49) | S | Worker and performing exec are separate fields; A10 proves it. |
| I6 No work authority (line 50) | S | Closed write surface and authorization refusal are explicit. |
| I7 Event-driven split (line 51) | S | Durable triggers, deterministic shell, semantic model boundary, and zero-idle rule are explicit. |
| I8 Observation without authority (line 52) | U | F2; NOTE publication is bounded, but concurrent semantic recomputation is not. |
| I9 Policy stays policy (line 53) | S | Validation and immutable result attribution are explicit. |
| Architecture: inbound binding/acceptance transaction (lines 57-59) | S | Worker row owns exec id/policy revision; no extra binding record is added. |
| Architecture: class/timing rule (line 61) | U | F1; algedonic destination/carrier semantics are stale and contradictory. |
| Architecture: bundle boundary/deadline wake (line 63) | S | Earlier-of boundary, one durable wake, no polling, and inherited ordering are explicit. |
| Architecture: annotate/escalate/resolver (line 65) | S | Citation, ordinary send, transaction-aware resolver, and authorization boundary are explicit. |
| Architecture: atomic delivery, replay, expiry/model failure (line 67) | S | OQ1 is correctly marked blocking; failure cannot silently settle input. |
| Architecture: activity summary (lines 69-73) | U | F2; concurrency and shared failure fan-out remain undecidable. |
| Architecture: runtime/policy (lines 75-77) | S | Direct provider call, elected model/effort, no ACP/workdir, and telemetry are explicit. |
| Architecture: pilot (line 79) | U | F3; metrics and gate are stated, but cited before evidence is not reproducible. |
| Subtraction rationale (line 81) | S | BUNDLE is the only added record; deletion and acceptance alternatives are addressed. |
| A1 Worker target (line 85) | S | Valid binding and pre-turn exec receipt are decidable. |
| A2 Invalid target/configuration (line 86) | S | Typed pre-write refusal is decidable. |
| A3 Timing inputs (line 87) | U | F1; immediate algedonic timing is shown, but required Main/no-second-carrier routing is absent. |
| A4 Bundle bound (line 88) | S | Boundary/deadline race and no private delay are decidable. |
| A5 Direct conservation (line 89) | S | One terminal direct outcome and no BUNDLE are required. |
| A6 Failure conservation (line 90) | S | Deadline expiry and queryable source are required. |
| A7 Summary cardinality (line 91) | S | One versus three member cases are concrete. |
| A8 Cited annotation (line 92) | S | Fact citation and two-name attribution are concrete. |
| A9 Parent escalation (line 93) | S | Resolver call and source-linked ordinary send are concrete. |
| A10 Attribution (line 94) | S | Every exec-authored row names worker and exec. |
| A11 Capability floor (line 95) | S | Work/decision mutation refuses before effect. |
| A12 Idle cost (line 96) | S | Zero query/model/wake outcome over a fixed interval is measurable. |
| A13 Semantic boundary (line 97) | S | Deterministic paths prohibit model rows; semantic work requires one bounded execution. |
| A14 Debounce with current NOTE (line 98) | S | Reuse/no-model behavior inside a live window is concrete. |
| A15 Initial summary/concurrency (line 99) | U | F2; one NOTE is proven, not one recomputation, and failed shared-attempt settlement is ambiguous. |
| A16 No request/cancel records (line 100) | S | Exact forbidden records are testable. |
| A17 Honest idle NOTE (line 101) | S | Exact literal and prohibited inferences are testable. |
| A18 Summary privacy (line 102) | S | NOTE read versus transcript denial is decidable. |
| A19 Policy record (line 103) | S | Historical revision stability and no substrate-derived policy are concrete. |
| A20 Pilot gate (line 104) | U | F3; the gate is concrete, but its mandatory baseline evidence is unavailable. |
| Open Question 1: delivery-destination transaction (line 108) | S | Exactly one paragraph, blocking, and states why implementation waits. |
| Open Question 2: credential lane (line 110) | S | Exactly one paragraph, blocking, and states the revocable/non-reuse requirement. |
| Eight canonical sections and exactly two open questions | S | Goal, Non-Goals, Terms, Assumptions, Invariants, Architecture, Acceptance, Open Questions all exist; both questions are blocking. |
| YAGNI/no-action boundary | S | One record type is added; reviewed commit contains one spec file and no implementation, target, specRef, merge, release, deploy, live mutation, or 0.1.x action. |

## Review lenses

- Completeness: F1-F3 are the material missing/contradictory contracts. No optional
  polish or exhaustive edge was used to block.
- YAGNI: no unrequired capability or extra durable record was found in the reviewed
  bytes.
- Law split: routing and verification remain deterministic; semantic summary and
  annotation/escalation judgment remain inference. F1 violates the live routing
  authority; F2 fails to deterministically bracket inference under concurrency.
