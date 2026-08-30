# Independent R1-R3 successor contract review

## Outcome

- Review assignment: `asg_63a43b96-d782-41d1-81f3-3226a7826d55`
- Reviewed producer assignment: `asg_ee922fe3-3005-406b-af46-82cb4ffa2d10`
- Recovery producer assignment: `asg_f030c3e1-7ad0-4008-af6c-10db1ffde01e`
- Work item: `wi_15f960ac-3083-437a-9979-0f0313b7f474`
- Review time: 2026-08-29 19:25 PDT
- Reviewed commit: `7cf3748f7c329c5bad928e0f1d2a06613b6a7b7c`
- Verdict: **reviewed-clean**

The exact successor closes R1-R3. The review found no new finding. F1-F9 remain
closed. The change does not expand product custody, fixture authority, or live-state
authority.

## Identity and evidence checks

The remote producer ref
`refs/heads/spec/feature-smoke-sidecar-contract-asg-ee922fe3` resolved to the exact
reviewed commit. The commit has tree
`bf0c6d8e3683f067baa54623cfdea89004d349be` and sole parent
`16e3b37033e54fc7db493d6a57eb2c2b236f0bd0`.

I read both reviewed artifacts twice in this review clone. Their hashes matched the
assigned seals:

| Artifact | SHA-256 |
| --- | --- |
| Contract `art_f6083d3b` | `58c2d6cda3ddde9eb2abd68f804f26c71fe75affa0711d71f3831ca71762255e` |
| Reconciliation `art_380492e0` | `24d28d6a63c26fe0685ea50e2a970c725f2d1f15ed8332ba6470b398f1a9d013` |
| Binary two-file diff | `7eabb4d571eff35431885ea84fb2b1da30bb10ca9b88e1a0533a0e13568af0f8` |

The target changes only the canonical contract and its reconciliation report. The
diff passes `git diff --check`. The contract contains the eight required sections, 15
numbered assumptions, 14 numbered invariants, 12 numbered architecture clauses, and
60 contiguous acceptance rows.

I checked the product source through a read-only GitHub object lookup. Remote branch
`0.1.9` resolves to exact commit
`2e918768556ef16a4412f9e0844bb388b6fb1051`. Its
`lib/tightbeam/client_e2e.ex` blob is exact
`402c822cfdc71b10d04a85f8cf076a57c0894f5d`. The source gives `preflight/2` through
the default third argument. It maps `:live` to a passing row, `{:dead, reason}` to a
failing row whose note starts with `credential rejected: `, and
`{:unknown, reason}` to an incomplete row. This matches AS-15 and the R1 rail.

I performed the reconciliation's read-only reduction against retained evidence
`art_85f430fe`. The file remains a regular mode-0600 file of 65,431 bytes with
SHA-256 `d92dcbc0577b96a19a87de67db681a31bd94673f5e5944b03bec15c7146d7d2f`.
It contains three records. The reduction returned exact normalized-manifest SHA-256
`2040e2080e389b9a59650e77c7ba246a2c97396ea79b514b2d61c98f7c23f4d0`.
It retained both normalized shell-snapshot tuples. The observed 300 entries, type and
mode counts, 31,826,506-byte regular-file sum, and 7,330,920-byte maximum also match
AS-14. This check did not run or reuse the consumed fixture.

I read the full work-item history and the full producer-assignment history. I also
read the prior verdict `att_5ec4d759`, report `art_b4753931`, completion
`att_0443a25a`, decision `dr_1c06d9c9`, decision `dr_7383a755`, Mike's correction
wake `s_1e05ddc2`, waiver receipt `att_8548c286`, and producer seal
`att_9894535d`. The review used the governing rationale, not the erroneous `hold`
label on `dr_7383a755`.

## R1-R3 closure

### R1 — Satisfied — Run-start observes waiver expiry in the same invocation

The Claude waiver observation term, C-01, C-12, AS-15, and AC-47/57/58/59 now form
one closed sequence:

1. C-10 establishes the evidence writer.
2. An exact-waiver Codex-only candidate calls
   `Tightbeam.ClientE2E.preflight("claude", fixture_base)` once.
3. The next run-start action consumes that row before any selected-leg preflight or
   spawn.
4. Only exact step `P-claude`, status `:fail`, and note prefix
   `credential rejected: ` activate the waiver.
5. A passing, incomplete, or other failing row leaves the waiver inactive and refuses
   the candidate.

The fixture retains no note. The contract invents no duration, credential ceremony,
or cross-process state. The same-invocation observation now decides the waiver state
at run-start, so the former step-5-to-step-6 ambiguity is gone.

### R2 — Satisfied — Every non-admitted run-start record uses JSON null

C-01 and C-10 now require `waiver=null` for every run-start refusal that does not
admit the named-waiver matrix. C-10 also forbids serialization of an absent, wrong,
inactive, or otherwise rejected input. AC-48 and AC-56 decide the absent and wrong
input cases. AC-57 through AC-59 decide the live and unknown observation cases.

The evidence file is established before run-start. Its successful creation consumes
the released fixture even when run-start refuses before a harness spawn. I-08, C-06,
C-10, and C-12 agree on that boundary.

### R3 — Satisfied — Calendar bytes are canonical before normalization

C-07 requires exact 4/2/2/2/2/2 ASCII decimal widths for year, month, day, hour,
minute, and second. It checks repeated-date equality, Gregorian month and day ranges,
hour `00` through `23`, and minute and second `00` through `59`. It excludes offsets,
fractions, and leap-second spelling. It rejects alternate raw spellings before any
placeholder substitution.

AC-49 covers the exact-width passing image. AC-60 proves that a one-digit month
refuses before normalization. The manifest digest can no longer collapse an alternate
calendar spelling into the admitted path image.

## Clause conformance table

`Satisfied` means the clause is precise, supported, and mechanically decidable for
this spec review. `Out of scope` marks actions that this review does not authorize.

| Clause or audit group | Status | Evidence |
| --- | --- | --- |
| Repository identity and spec homing | Satisfied | The exact remote ref, commit, tree, parent, two artifact hashes, and binary diff match. The contract remains under `specs/tightbeam`; recon and this review remain under `evidence`. |
| Goal | Satisfied | Admission remains limited to the Claude five-path set and one exact normalized Codex runtime image in a fresh fixture. |
| Non-Goals | Satisfied | All nine exclusions remain intact, including no product, fixture, live, integration, or reusable-pattern authority. |
| Terms: fixture, home, snapshot, delta, paths, phases, identity, evidence, launch, and gateway | Satisfied | Each term keeps one observable meaning and a bounded lifecycle. |
| Terms: Claude waiver observation and active named waiver | Satisfied | R1 binds one exact source row from the same invocation to the next run-start decision. |
| AS-01 through AS-14 | Satisfied | The branch, prior observations, retained evidence, OTP boundary, launch envelope, gateway topology, ruling, and manifest bounds remain supported and unchanged in substance. |
| AS-15 | Satisfied | Direct source-object review matched the commit, blob, callback mapping, scorecard status, and note prefix. |
| I-01 through I-07 | Satisfied | Per-leg scope, baseline order, whole-set admission, PID independence, decision inputs, exact manifest, and no runtime-path mutation remain closed. |
| I-08 | Satisfied | Successful evidence-file creation consumes the fixture before a run-start refusal can otherwise leave it reusable. |
| I-09 through I-14 | Satisfied | Content exclusion, one-file custody, frozen parent state, refusal retention, exact envelope, and gateway boundary remain closed. |
| Architecture and pattern choice | Satisfied | The text names fixture harness-runtime admission and rejects a reusable agent pattern. It adds only the existing read-only preflight seam. |
| C-01 | Satisfied | Run-start ordering, exact matrix selection, all waiver branches, evidence value, and pre-spawn stop points are decidable. |
| C-02 through C-06 | Satisfied | Claude path set, internal PID binding, schema, freshness, cardinality, phase continuity, and no-reuse rules remain exact. |
| C-07 static manifest and counts | Satisfied | The read-only reduction reproduces the exact 300-line digest, counts, modes, size observations, and duplicate tuple. |
| C-07 dynamic families and calendar grammar | Satisfied | Cache, session, snapshot, and arg0 families have exact grammar, cardinality, equality, freshness, and pre/post binding. R3 closes raw calendar widths and ranges. |
| C-07 size and cross-phase rules | Satisfied | The 8 MiB and 32 MiB limits remain exact. Post-turn token identity and content-free size/hash flexibility remain bounded. |
| C-08 | Satisfied | Every supported acquisition failure has one ordered, content-free, non-retrying result with object-identity continuity. |
| C-09 | Satisfied | Error categories, set-level output, raw-path ordering, and fixed predicate ordering remain deterministic. |
| C-10 record schema and cardinality | Satisfied | The v2 schema keeps 32 ordered checks, seven full-matrix records, four admitted-waiver records, refusal truncation, and the sink-failure exception. |
| C-10 waiver and evidence-creation rules | Satisfied | R2 assigns the exact ID only after admission and JSON `null` elsewhere. Creation uses the same bounded evidence file and consumes the fixture. |
| C-11 | Satisfied | Future implementation custody remains only `scripts/feature_smoke.exs` on synchronized `origin/0.1.9`. |
| C-12 | Satisfied | The release sequence now distinguishes opener candidate selection from the same-invocation run-start observation. It grants no release itself. |
| AC-01 through AC-46 | Satisfied | The prior F1-F9 path, phase, evidence, acquisition, creation-mode, and gateway cases remain present and decidable. |
| AC-47 | Satisfied | The exact rejected-credential row admits only the exact-waiver Codex matrix. |
| AC-48 | Satisfied | An absent waiver refuses before preflight or spawn and writes `waiver=null`. |
| AC-49 | Satisfied | The passing retained image now requires exact-width calendar fields before normalization. |
| AC-50 through AC-55 | Satisfied | Path, type, mode, size, cross-phase, cardinality, and opener-selection outcomes remain exact. |
| AC-56 | Satisfied | A wrong supplied waiver refuses without copying that string into evidence. |
| AC-57 | Satisfied | A live same-invocation row expires the waiver and refuses with JSON `null`. |
| AC-58 | Satisfied | An incomplete row leaves the waiver inactive and refuses with JSON `null`. |
| AC-59 | Satisfied | A fail row without the exact rejection prefix leaves the waiver inactive and refuses with JSON `null`. |
| AC-60 | Satisfied | A one-digit month refuses before manifest normalization. |
| Open Questions | Satisfied | “None” is accurate for this exact contract. R1-R3 now have one interpretation each. |
| Product edits, implementation, fixture creation or execution, smoke, integration, release, deployment, restart, and parent or producer completion | Out of scope | The assignment and contract forbid these actions. This review performed none of them. |

## F1-F9 preservation audit

| Prior finding | Status | Preserved mechanism |
| --- | --- | --- |
| F1 | Satisfied | C-01 keeps per-leg baselines, pre-wake, post-turn, cleanup, and no cross-home read. |
| F2 | Satisfied | C-10 keeps the exact evidence path, framing, field order, checks, cardinality, and retention boundary. |
| F3 | Satisfied | AS-01 and C-11 keep exact branch `origin/0.1.9`. |
| F4 | Satisfied | C-09 keeps category, raw-path, and fixed-predicate tie-breaking. |
| F5 | Satisfied | C-10 keeps console-only `FX_EVIDENCE` handling without retry or false durability claims. |
| F6 | Satisfied | C-09 keeps `FX_PATH_SET` as set-level `path=-`. |
| F7 | Satisfied | C-08 keeps one representable result for enumeration, metadata, open, read, disappearance, and type change. |
| F8 | Satisfied | C-08 keeps supported OTP operations and initial, handle, and final object-identity continuity. |
| F9 | Satisfied | AS-12, I-14, C-10, and C-12 keep the pre-existing HTTP gateway outside the later client process tree. |

## Completeness, scope, and deletion audit

The contract includes Goal, Non-Goals, Terms, Assumptions, Invariants, Architecture,
Acceptance, and Open Questions. Each R1-R3 success path has corresponding refusal
paths. Error order, evidence values, fixture consumption, and teardown boundaries are
explicit. No newly added behavior lacks an acceptance row or a reconciliation trace.

The amendment adds no helper, dependency, product file, credential ceremony, retry,
fixture attempt, fixture reuse, content semantic, prefix allowlist, custody transfer,
or live authority. The exact `ClientE2E` call is an existing read-only seam.

Deletion is not a valid closure for any reviewed delta. Deleting the same-invocation
observation reopens R1. Deleting the bounded null rule reopens R2. Deleting the raw
calendar grammar reopens R3. The added evidence-creation consumption rule prevents a
refused pre-spawn invocation from becoming reusable. No added clause is an optional
embellishment.

## Verdict basis

The exact successor has one mechanically decidable result for each prior ambiguity.
It preserves the full earlier contract, evidence boundary, one-file future custody,
and no-live-authority rail. Exact commit
`7cf3748f7c329c5bad928e0f1d2a06613b6a7b7c` is therefore **reviewed-clean**.
