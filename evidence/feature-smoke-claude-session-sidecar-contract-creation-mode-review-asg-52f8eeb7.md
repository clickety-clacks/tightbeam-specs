# Feature-smoke Claude session-sidecar contract creation-mode review

Review assignment: `asg_52f8eeb7-c65b-4985-9b9f-a66bb4127c61`  
Work item: `wi_15f960ac-3083-437a-9979-0f0313b7f474`  
Producer assignment: `asg_ee922fe3-efc4-45dd-b69a-1aa859b06788`  
Reviewed commit: `6e8b72a4abad1d272e5dbe21c10d73491b08e5be`  
Reviewed tree: `fc780496f45462bffdd1e52f8c5da9f022eb65fc`  
Reviewed parent: `7717ec827a7448b9b99518d2518383c43c8bd82a`  
Verdict: **changes-requested**

## Independent model and authority

The contract must define one release-gating Gibson feature smoke for the live Claude harness. It must use a fresh exact home, exercise the five named filesystem paths through Claude and Codex legs, retain same-path object identity across create and resume, and preserve evidence sufficient to decide every acceptance criterion. The amendment authorized by `dr_16de6d11-492c-4ec4-aaa2-6cb1a03d4d7d` is limited to a truthful one-file mechanism for the evidence file's effective creation mode. It does not authorize a helper, native dependency, reopen, chmod repair, product-file change, custody expansion, or a change to harness behavior.

I built this model from the work item, the complete producer-assignment history, the sealed `spec-ready` receipt `att_c0903c2d-6067-4539-aa4b-77ca4b5715a4`, Mike's `contract-amendment` ruling, the implementation verdict and report (`att_e167466a-8063-4d59-8d92-67750584cf7a`, `art_cdbca6e1-b96e-4229-9b50-53ccd4194c8e`), the implementation blocker and mechanism report (`att_619caef0-d33a-49ce-966e-242b919e985e`, `art_b1641827-46d6-45a0-983f-15db3a803407`), and the complete F1-F8 review/rework chain. I read the producer's recon only after forming the model.

## Sealed-byte verification

The pushed producer ref `refs/heads/spec/feature-smoke-sidecar-contract-asg-ee922fe3` resolves to the reviewed commit. The reviewed bytes reproduce the seal:

| Object | Expected | Observed | Result |
|---|---|---|---|
| Commit | `6e8b72a4abad1d272e5dbe21c10d73491b08e5be` | same | satisfied |
| Tree | `fc780496f45462bffdd1e52f8c5da9f022eb65fc` | same | satisfied |
| Parent | `7717ec827a7448b9b99518d2518383c43c8bd82a` | same | satisfied |
| Contract blob | `b447a8b6f4eca5078c71a0639f51b4dcc5501ee6` | same | satisfied |
| Contract SHA-256 | `6ed2cf92602920102a90deb705f24f12e1e1b7a8ea1d2bf8d20c2b3b50e6911e` | same | satisfied |
| Recon blob | `d671de3e9f77bbb59afcec44850c952ee15f11a8` | same | satisfied |
| Recon SHA-256 | `753ab24d5ba36d657a5c1e9372a1d3d2a4d46c501f5bce9c930723174db1e568` | same | satisfied |
| Parent-to-commit binary diff SHA-256 | `21303a800e812b40af7a308d5eb3ca957e6e91be7f6258587937a096ff87f3bb` | same | satisfied |

The diff contains only the contract and recon paths. `git diff --check` passes. The reviewed commit descends from the current remote `main` tip observed during review.

## Finding

### F9 — blocking — the process-wide launch umask escapes the evidence-file boundary

The amended contract requires the outer Gibson zsh process to execute `(umask 077 && exec mix run --no-start scripts/feature_smoke.exs)` and says the fixture neither reads nor changes the mask (`specs/tightbeam/feature-smoke-claude-session-sidecar-contract.md:105-110`). `umask` is process state. It survives `exec` and is inherited by descendants. Consequently, the full live matrix launches the Claude and Codex harness descendants under `0077`; the mechanism is not confined to the fixture's exclusive evidence-file open.

That consequence conflicts with the contract's own non-goal that the fixture must not change Claude or Codex harness behavior (`...contract.md:36-39`) and with recon D11's assertion that the amendment changes no harness behavior and remains bounded to the evidence-file mechanism (`evidence/feature-smoke-claude-session-sidecar-contract-recon.md:365-395`). The mechanism report that motivated the amendment also expressly records that caller `umask` is process-wide.

It also leaves the release gate undecidable. C02 requires the Claude leg to produce `backups` at `0755` and the retained sidecar at `0644` (`...contract.md:243-262`). C10 forbids fixture chmod repair, reopen, replacement, helpers, and native dependencies (`...contract.md:459-486`). C12 requires both the case-only proof and the full live matrix to inherit the exact `0077` launch envelope (`...contract.md:644-687`). The contract contains no verified premise that the Claude harness explicitly requests or repairs those two less-restrictive modes independently of inherited `umask`. If the harness uses ordinary `0777`/`0666` creation requests, the exact launch environment makes those entries `0700`/`0600`, while C02 requires `0755`/`0644`. If it sets exact modes later, the contract must cite real evidence because the stated no-harness-behavior premise and the release decision depend on it. The present text specifies neither branch.

This is not a request for exhaustive robustness. It affects the core live run, exact five-path contract, and truthful release decision. The existing implementation review proved only the evidence-file race under hostile ambient `000`; it did not prove the downstream Claude/Codex path modes under the new inherited `0077` envelope.

**Deletion test:** deleting the process-wide launch envelope closes the descendant behavior leak, but then the authorized one-file contract has no mechanism that makes the evidence file's effective creation mode `0600` without a forbidden post-open repair. Accepting the failure as a named value also loses because exact modes, same-object evidence, and a decidable release gate are required. Therefore the product owner must choose a contract mechanism or a verified harness-mode premise that closes this contradiction; review must not invent one.

## Clause table

| Clause or section | Result | Evidence |
|---|---|---|
| Goal | unsatisfied | The exact-home live smoke remains the stated outcome, but F9 makes its launch environment conflict with required runtime modes and the no-harness-behavior boundary. Contract lines 19-34; F9. |
| Non-goals | unsatisfied | The launch envelope changes inherited process state for both harness descendants. Contract lines 36-51, especially 38-39; F9. |
| Terms | unsatisfied | The terms precisely define the launch envelope, truthful OTP request `0666`, inherited `0077`, effective `0600`, retained path/object identity, and outcome classes. The launch-envelope term is not bounded to the evidence-file open. Contract lines 53-125; F9. |
| AS01-AS10 | satisfied | The assumptions remain explicit and decide OS, repo, release-binary, harness, auth, home, entry-shape, and field-presence preconditions. Contract lines 127-163. |
| AS11 | unproven | The zsh envelope is available, but its asserted suitability for both case-only and live execution omits the inherited effect on harness-created path modes. Contract lines 164-168; F9. |
| I01-I12 | satisfied | The invariants keep exact home derivation, no reuse, provenance, per-leg isolation, retained same-handle/path/type/mode/identity, live binary use, canonicalization, and evidence ownership explicit. Contract lines 170-195. |
| I13 | unsatisfied | It mandates the process-wide envelope for every live-matrix leg while claiming the fixture does not repair or replace the file; it does not reconcile descendant inheritance with C02. Contract lines 196-198; F9. |
| Architecture and custody | satisfied | The contract remains one fixture file, one existing assignment, one specs artifact, and one live report/manifest custody lane. Contract lines 200-217. |
| C01 | satisfied | Exact environmental and binary preflight remains decidable. Contract lines 221-241. |
| C02 | unproven | The five exact paths, types, modes, and field contracts are precise, but `backups=0755` and sidecar `0644` are not reconciled with inherited `0077`. Contract lines 243-294; F9. |
| C03-C09 | satisfied | Fresh-home proof, provenance, Claude create/resume, Codex before/after observation, normalization, exact paths, and same-object snapshots remain explicit. Contract lines 296-457. |
| C10 | unsatisfied | The evidence-file primitive is precise and truthful locally: OTP requests `0666`; inherited `0077` yields `0600`; one exclusive handle is retained; no chmod, reopen, helper, or native dependency is allowed. But the selected process-wide carrier is not confined to that primitive. Contract lines 459-486; F9. |
| C11 | satisfied | Outcome precedence and evidence disposition remain deterministic. Contract lines 488-642. |
| C12 | unsatisfied | The exact case-only and full-live launch forms, content-bounded `strace`, ambient `000` proof, existing-assignment re-release, and no-duplicate rule are precise. The full-live launch also exports `0077` to the harness descendants without deciding its effect on C02. Contract lines 644-687; F9. |
| AC01-AC25 | satisfied | The prior F1-F8 review chain and this read found the exact-home, five-path, provenance, topology, normalization, evidence, and refusal clauses decidable. Contract lines 691-724. |
| AC26 | unproven | It requires the live evidence file at exact effective `0600` with no repair. The local mechanism is precise, but the full release gate cannot be accepted while the same envelope may invalidate C02. Contract line 725; F9. |
| AC27-AC28 | satisfied | Live release-binary execution and full-field retention remain explicit. Contract lines 726-727. |
| AC29 | unproven | Same-path/type/mode/identity is explicit for the evidence file, but the live run used to prove it inherits the unresolved descendant-mode effect. Contract line 728; F9. |
| AC30-AC42 | satisfied | Ordering, per-leg association, exact-home separation, evidence completeness, custody, refusal, same-object and no-replacement checks remain explicit. Contract lines 729-741. |
| AC43 | satisfied locally, incomplete globally | The content-bounded case-only trace can prove ambient `000`, `umask(0077)`, `exec`, requested `0666`, first metadata `0600`, and absence of chmod/reopen. It does not prove that the inherited mask preserves C02 in the full live harness. Contract line 742; F9. |
| AC44 | satisfied as a refusal rule | The fixture must refuse if the exact envelope or case-only trace is absent. That precision does not cure F9. Contract line 743. |
| Open questions | unsatisfied | The section says no open questions remain, but F9 is a load-bearing unresolved contract choice. Contract lines 745-761. |
| Spec homing and artifact custody | satisfied | Both amended source documents are committed in the durable specs repository; sealed hashes and artifact rows identify the bytes. |
| Existing assignment re-release | satisfied | C12 explicitly reuses `asg_0c3a1dcc-74d4-4ca9-94dd-cf2f480e68fd` and forbids a duplicate implementation assignment. Contract lines 671-676. |
| PID independence | satisfied | Identity is path/type/mode/object based; PID is not used as a retained-object identity condition. Contract lines 76-89, 176-184, 412-457. |

## Prior finding closure

| Finding | Result | Evidence |
|---|---|---|
| F1 per-leg topology | closed | Per-leg before/after association and report/manifest topology are explicit in C03-C09 and AC12-AC14/AC31-AC33. |
| F2 evidence completeness | closed | Full field retention, command/output capture, hashes, deterministic paths, and refusal on absent evidence are explicit in C09-C12. |
| F3 release origin / 0.1.x | closed | C01 and AC18-AC20 bind origin, clean checkout, tag, version, and release binary. |
| F4 tie-break | closed | C11 defines outcome precedence and no-result escalation. |
| F5 sink contradiction | closed | C11 separates release verdict, no-result, and escalation dispositions. |
| F6 absent-path output | closed | C11 and its evidence requirements represent absence explicitly. |
| F7 snapshot acquisition failures | closed | C11 makes snapshot/tool acquisition failure a represented refusal or no-result path. |
| F8 object identity | closed | C07-C10 and AC37-AC42 require same retained path/type/mode/object identity and forbid replacement/reopen. |

## Completeness, necessity, and subtraction

The amendment is authorized only by Mike's `contract-amendment` ruling and stays textually within the one fixture file, its evidence contract, and recon. No product source, test, live state, helper, native dependency, or new assignment is introduced. The new content-bounded trace and AC43/AC44 are necessary evidence for the creation-mode claim, not optional polish. I found no separate YAGNI addition.

F9 is a principle-level contradiction rather than a request for another review ratchet. The contract says the amendment does not change harness behavior, yet selects a process-wide inherited mechanism. Deletion cannot preserve the authorized effective-mode proof; acceptance cannot preserve the core release criteria. The next step is an owner-ratified contract choice, followed by re-review of exact bytes.

## Verdict

**changes-requested** for exact commit `6e8b72a4abad1d272e5dbe21c10d73491b08e5be` because F9 remains blocking. F1-F8 are closed. No other important or blocking finding remains.
