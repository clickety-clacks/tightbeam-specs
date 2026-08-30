# Independent Codex-runtime contract review

## Outcome

- Assignment: `asg_81abcdb3-43e9-40d7-b923-5febef82c511`
- Producer assignment: `asg_ee922fe3-3005-406b-af46-82cb4ffa2d10`
- Work item: `wi_15f960ac-3083-437a-9979-0f0313b7f474`
- Review time: 2026-08-29 18:50 PDT
- Reviewed commit: `16e3b37033e54fc7db493d6a57eb2c2b236f0bd0`
- Verdict: **changes-requested**

Three important findings remain. They affect waiver selection, refused evidence, and
the exact Codex path boundary. No product or live-fixture action is authorized by this
review.

## Identity and evidence checks

The remote producer branch resolved to the reviewed commit. The reviewed object had
tree `c0343a5721f0367fee0610df2ec04423d9faac73` and parent
`cfe3c1a7b6f00570de671fd0e06c451964fade8f`.

I read both reviewed artifacts twice in this review clone. Their hashes matched:

| Artifact | SHA-256 |
| --- | --- |
| Contract `art_7ea0d39b` | `6d54ac48302435574551e56d179607ee84579e4c329894ae6dfaa58df0fc389f` |
| Reconciliation `art_e2e3bb81` | `4117d96ca646e2409ce3b724fac41c288557870fd91debefc5718b7e5720411f` |
| Binary two-file diff | `3c03ba2181039db9211037af367d00637310bec666f7f2baf62c4b576c71c19b` |

I also read the retained evidence and its run report in full:

| Artifact | SHA-256 |
| --- | --- |
| Retained JSONL `art_85f430fe` | `d92dcbc0577b96a19a87de67db681a31bd94673f5e5944b03bec15c7146d7d2f` |
| One-shot report `art_424f3eff` | `0593f4c8230d6bafd7c7cbac5db974bdc2af57f831ec76d688b133e502a1961c` |

I independently reduced all 300 retained entries. The normalized manifest SHA-256
matched `2040e2080e389b9a59650e77c7ba246a2c97396ea79b514b2d61c98f7c23f4d0`.
The observed counts, modes, byte sum, maximum file size, and four dynamic families also
matched the contract.

I read the complete work-item and producer history that governs this amendment. This
included correction wake `s_1e05ddc2`, decision `dr_7383a755`, receipt
`att_8548c286`, and ruling `dr_1c06d9c9=amend-after-recon`. I also used the three
served manual sections named by the assignment.

## Findings

### R1 — Important — The fixture cannot decide immediate waiver expiry

The active-waiver term says that the waiver expires immediately when the Gibson org
Anthropic credential becomes valid. It also says that the step-5 release records the
credential condition. See contract lines 96-102.

C-12 samples that condition when the opener prepares step 5. See lines 822-825. The
fixture then validates run-start before credential preflight. See C-01 lines 281-285.
The contract does not carry the opener's observation into the fixture as a defined
input. It also does not define a freshness limit or a run-start recheck.

Two conforming implementations can now make different decisions when the credential
becomes valid between steps 5 and 6. One can freeze the step-5 selection. The other can
expire the waiver at run-start. This difference changes whether the Claude leg runs.

Deletion does not preserve the requirement. Deleting immediate expiry would conflict
with Mike's correction and `dr_7383a755`. The next revision must define which
observation is authoritative and how it binds to the released fixture. If the fixture
must recheck, the revision must define that check before implementation custody begins.

### R2 — Important — A refused Codex-only run has no defined `waiver` value

C-10 requires every record to contain `waiver`. It defines the exact decision ID for an
admitted Codex-only matrix. It defines JSON `null` for a full two-leg matrix. See lines
657-673.

AC-48 requires run-start refusal when Codex-only selection has an absent or wrong
waiver. C-01 and C-10 still require a synced refused record. That run is neither an
admitted Codex-only matrix nor a full matrix. The contract does not define its
`waiver` value.

An implementation can write `null`, the wrong supplied string, or the expected ID.
Each choice conflicts with a plausible reading of C-10. Recording an arbitrary supplied
value can also widen the evidence-content boundary.

Deleting the field would remove the required waiver audit from all v2 records. That
deletion does not preserve the goal. The smallest repair defines one bounded value for
every run-start refusal that did not enter an admitted named-waiver matrix. An
acceptance row must assert that value for the absent and wrong cases.

### R3 — Important — The calendar path grammar does not fix its byte spelling

C-07 names `<yyyy>`, `<mm>`, `<dd>`, `<hh>`, `<minute>`, and `<ss>`. It requires a
valid UTC second, but it does not define widths or a canonical byte encoding. See lines
424-431.

The normalization then replaces those components before it computes the manifest
digest. A parser can therefore accept `2026/8/29` as a valid date and produce the same
normalized digest as `2026/08/29`. This admits raw path bytes that the retained evidence
did not contain.

The reconciliation command uses exact widths of four, two, two, two, two, and two
digits. See reconciliation lines 282-285. C-11 directs the implementer to derive
behavior from the contract, so the reconciliation command cannot silently complete the
normative grammar.

Deleting the rollout family would reject the observed 300-entry runtime and defeat the
amendment. The smallest repair replaces the placeholder convention with an exact raw
path grammar and a canonical UTC conversion rule. The rule must reject every alternate
spelling before normalization.

## Clause conformance table

`Satisfied` means the clause is precise and supported for this spec review.
`Unsatisfied` means the text permits incompatible implementations or lacks a required
outcome. `Out of scope` marks work that this review did not authorize.

| Clause or audit group | Status | Evidence |
| --- | --- | --- |
| Repository, commit, tree, parent, artifact, diff, and manifest identity | Satisfied | Independent remote and local object checks matched every assigned value. |
| Goal | Satisfied | The contract limits admission to one fresh feature-smoke fixture and exact harness runtime deltas. |
| Non-Goals | Satisfied | The text excludes production reconciliation, launcher PID inference, content semantics, symlink targets, other groups, and a reusable agent pattern. |
| Terms except active waiver and calendar placeholders | Satisfied | The terms define homes, deltas, phases, evidence tokens, snapshots, and sidecar identity. |
| Active named Claude waiver term | Unsatisfied | R1 leaves immediate expiry undecidable at run-start. |
| AS-01 through AS-12 | Satisfied | Branch, source, runtime, evidence, OTP, launch, and gateway assumptions remain bounded. |
| AS-13 | Unsatisfied | It cites the exact authority, but R1 does not represent the authority's expiry state. |
| AS-14 | Satisfied | Independent reduction matched all 300-entry counts and both size observations. |
| I-01 through I-05 | Satisfied | The fixture, set-level snapshot, PID independence, and decision inputs remain exact. |
| I-06 | Unsatisfied | R3 permits an alternate raw calendar spelling before normalization. |
| I-07 through I-14 | Satisfied | Mutation, consumption, evidence, custody, parent, refusal, umask, and gateway boundaries remain closed. |
| Architecture and agent-pattern answer | Satisfied | The pattern is fixture harness-runtime admission, not a reusable agent pattern. |
| C-01 | Unsatisfied | R1 leaves active-waiver selection undecidable across release and run-start. |
| C-02 through C-06 | Satisfied | Claude path, PID independence, schema, clock, and identity rules remain exact. |
| C-07 counts and static manifest | Satisfied | The 300/113/183/4 counts, modes, normalized digest, and duplicate tuple are exact. |
| C-07 four dynamic families | Unsatisfied | Cache, snapshot, and arg0 grammars are exact; R3 leaves the calendar bytes open. |
| C-07 size bounds | Satisfied | The 8 MiB per-file and 32 MiB total limits are exact and derive from retained maxima. |
| C-07 cross-phase binding | Satisfied | Raw dynamic tokens must match pre-wake values; AC-53 gives one deterministic refusal. This rule narrows admission. |
| C-08 | Satisfied | One ordered snapshot binds initial, open-handle, and final regular-object identity without retry or content disclosure. |
| C-09 | Satisfied | The category order, raw-path order, predicate order, and set-level `path=-` refusal are exact. |
| C-10 record sequence and cardinality | Satisfied | The full matrix has seven records and the waived matrix has four records. Sink failure has an explicit exception. |
| C-10 v2 checks | Satisfied | The list has exactly 32 checks, fixed mappings, fixed applicability, and first-failure evaluation. |
| C-10 `waiver` field | Unsatisfied | R2 leaves a required run-start refusal value undefined. |
| C-11 | Satisfied | Custody remains one product file on synchronized `origin/0.1.9`. |
| C-12 | Unsatisfied | R1 leaves the boundary between step-5 observation and step-6 execution undefined. |
| AC-01 through AC-46 | Satisfied | Prior F1-F9 closure cases remain present and decidable. |
| AC-47 | Unsatisfied | Its external credential premise has no defined binding into run-start. |
| AC-48 | Satisfied for refusal; unsatisfied for evidence | Control flow refuses, but R2 leaves the required record incomplete. |
| AC-49 | Unsatisfied | “Fresh valid dynamic tokens” inherits R3's calendar ambiguity. |
| AC-50 | Unsatisfied | An alternate calendar spelling can normalize to the accepted digest instead of refusing. |
| AC-51 through AC-54 | Satisfied | Type, mode, size, cross-phase, and four-record cases are exact. |
| AC-55 | Satisfied in isolation | It decides selection when the opener prepares step 5, but it does not close R1's later interval. |
| Open Questions | Unsatisfied | R1 requires an owner choice, so “None” is not accurate. |
| Implementation, fixture, smoke, integration, release, deployment, and restart | Out of scope | The assignment forbids these actions. |

## Required audit results

- F1-F9: the original closure mechanisms remain present. R1-R3 concern new waiver and
  Codex-runtime text.
- PID independence: satisfied. No admission rule reads or compares launcher `osPid`.
- Waiver expiry: unsatisfied by R1.
- C-07 exact manifest: the retained digest and counts match. R3 leaves one raw-name
  family wider than the evidence.
- C-07 cross-phase binding: satisfied as a deterministic fail-closed rule.
- Set-level refusal: satisfied with `FX_PATH_SET` or `FX_CODEX_RUNTIME_PATH` and
  `path=-`, as applicable.
- C-08 acquisition: satisfied. The rule makes each supported failure representable.
- v2 evidence: the 32-check order and applicability table are exact. R2 leaves one
  field value undefined.
- Cardinality: satisfied at seven records for the full matrix and four for the active
  waiver matrix.
- Prefix and subtree widening: none, except the alternate calendar spelling in R3.
- Content and symlink-target widening: none.
- Product custody and one-file implementation custody: unchanged.
- Live authority: unchanged. The contract does not authorize a fixture or product run.

## Verdict basis

Each finding changes a result that the future one-file implementation must produce.
The contract therefore cannot receive `reviewed-clean` at the reviewed commit. A narrow
contract-and-reconciliation amendment can close all three findings without product or
live-fixture work.
