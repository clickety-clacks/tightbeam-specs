# Feature-smoke creation-mode implementation review

Reviewed at 2026-08-29 11:29 PT.

## Verdict

`reviewed-clean` for the exact product commit `ec2b28b8eaf47e3ef85318524752a827c23bd0af`.

No blocking or important finding remains. The change implements the reviewed creation-mode amendment without adding another evidence-file opening, a descriptor mode mutation, a helper, or custody outside `scripts/feature_smoke.exs`.

## Reviewed object and provenance

- Product repository: `clickety-clacks/tightbeam`.
- Exact commit: `ec2b28b8eaf47e3ef85318524752a827c23bd0af`.
- Tree: `8851a4e087d8e444f5d5a3e0b35c657d42ed1710`.
- Parent: `08e55de896106aa7fcc2ea7f60f1357e5d6cf772`.
- Implementation base: `bdf0ad2c9ae4078f897a00e8c57767968676477c`.
- Exact-commit delta: 87 insertions and 66 deletions in `scripts/feature_smoke.exs` only.
- Cumulative custody from the implementation base: `scripts/feature_smoke.exs` only.
- Product source SHA-256: `0fa7543014f2f8407213f71c68350d2e9064a66d2f1f2280e3101cf4be8655eb`.
- Source-of-truth contract commit: `beb7c222c908486a774ded9656a5ababe596bd02` in `clickety-clacks/tightbeam-specs`.
- Producer `tests-passed` receipt: `att_36c342d8-4491-405a-ba21-c5d72223102a`, pinned to the reviewed commit.
- Producer trace artifact: `art_21af1a8f`, SHA-256 `122e58ac01cbaf3092cbe98da5f275a68ed1d22964f77f6305cabdac386e93e4`.
- Producer gate report: `art_7096d323`, SHA-256 `6149b11c4e8ac3c2cf806e30f3564b4531504db601dd05f04c5fa0b7f3372228`.

## Independent verification

- Built `cli/target/release/tightbeam` from the reviewed commit on Gibson.
- `mix format --check-formatted`: pass.
- Exact deterministic envelope, with inherited Tightbeam and release overrides removed: pass, `42/42`.
- `scripts/verify_mix.sh`: pass, 9 doctests, 1704 tests, 0 failures, 11 skipped.
- `git diff --check`: pass.
- Exact and cumulative custody checks: pass.
- Trace inspection: the shell sets `0077` before the Mix exec (trace lines 76-80); the evidence path has one `O_RDWR|O_CREAT|O_EXCL` request with `0666`, handle mode `0600`, and no-follow path mode `0600` (trace lines 3843-3849). The successful created-evidence path has no chmod-family call or second open.
- Integrated lifecycle inspection: the retained evidence handle is created and verified before run-start at source lines 468-503; creation uses the required OTP open at lines 1882-1884; the same handle is retained through the phase loop at lines 117-152 and is written and synced at lines 2043-2077.

## Clause table

Status values are `satisfied` and `out-of-scope`. The latter marks later live-matrix execution that this implementation-review assignment expressly forbids; it is not an implementation defect.

| Clause | Status | Evidence |
| --- | --- | --- |
| C-01 | satisfied | Integrated run-start and per-leg phase order at lines 107-152; deterministic phase cases pass. |
| C-02 | satisfied | Complete admitted Claude path-set implementation and deterministic path-set cases pass. |
| C-03 | satisfied | Canonical filename and internal PID binding cases pass. |
| C-04 | satisfied | Exact sidecar schema, type, and cwd cases pass. |
| C-05 | satisfied | Spawn-interval freshness and backup provenance cases pass. |
| C-06 | satisfied | Cardinality, phase continuity, identity, and no-reuse cases pass. |
| C-07 | satisfied | Codex empty-runtime separation cases pass; the integrated leg loop preserves separate homes. |
| C-08 | satisfied | One-snapshot, no-follow, no-mutation, no-retry refusal cases pass. |
| C-09 | satisfied | Deterministic category, path-token, and predicate-order cases pass. |
| C-10 | satisfied | Lines 468-503 and 1882-1884 implement exclusive retained-handle creation and handle/path verification; trace lines 76-80 and 3843-3849 prove the exact real syscall envelope. |
| C-11 | satisfied | Only `scripts/feature_smoke.exs` differs from the implementation base. |
| C-12 | satisfied | Reviewed contract, pinned implementation, deterministic envelope, source topology, format, and full repository gate all pass. The later live matrix remains outside this review assignment. |
| AC-01 | satisfied | Deterministic run-start fixture case passes. |
| AC-02 | satisfied | Reused-fixture refusal case passes. |
| AC-03 | satisfied | Per-leg baseline and home-isolation cases pass. |
| AC-04 | satisfied | Exact five-path Claude pre-wake case passes. |
| AC-05 | satisfied | Canonical filename/PID case passes. |
| AC-06 | satisfied | Leading-zero path-set refusal case passes. |
| AC-07 | satisfied | Unequal filename/internal PID refusal case passes. |
| AC-08 | satisfied | Invalid UTF-8 refusal case passes. |
| AC-09 | satisfied | Malformed JSON refusal case passes. |
| AC-10 | satisfied | Duplicate-member refusal case passes. |
| AC-11 | satisfied | Missing-member schema refusal case passes. |
| AC-12 | satisfied | Extra-member schema refusal case passes. |
| AC-13 | satisfied | Wrong-type schema refusal case passes. |
| AC-14 | satisfied | Wrong-cwd refusal case passes without value disclosure. |
| AC-15 | satisfied | Out-of-interval freshness refusal case passes. |
| AC-16 | satisfied | Duplicate sidecar/backup cardinality refusal cases pass. |
| AC-17 | satisfied | Canonical post-turn backup replacement case passes. |
| AC-18 | satisfied | Sidecar identity-drift refusal case passes. |
| AC-19 | satisfied | Unexpected nested path refusal case passes. |
| AC-20 | satisfied | Symlink-at-admitted-name no-follow refusal case passes. |
| AC-21 | satisfied | Mode `0644` refusal case passes. |
| AC-22 | satisfied | Oversize-before-decode refusal case passes. |
| AC-23 | satisfied | Non-object JSON-shape refusal case passes. |
| AC-24 | satisfied | Codex runtime-path refusal and Claude-home isolation case passes. |
| AC-25 | satisfied | Repeated multi-failure selection remains deterministic. |
| AC-26 | out-of-scope | The exact retained-file content is covered by the deterministic full-evidence case; execution of the fresh live matrix belongs to the later C-12 release step. |
| AC-27 | satisfied | Spawn-time refusal, retained fixture, no mutation, and cleanup case passes. |
| AC-28 | satisfied | Reviewed contract exists and the implementation changes one authorized file. |
| AC-29 | out-of-scope | Deterministic cases and repository gates pass; the fresh live matrix is the later C-12 release step and was prohibited here. |
| AC-30 | out-of-scope | This governs operator conduct if the later live matrix discovers drift; no live matrix ran in this review. |
| AC-31 | satisfied | Work-item trace records the pinned parent, product assignment, and facts after the contract. |
| AC-32 | satisfied | Wrong-cwd retained-evidence case passes and stops later phase/leg evidence. |
| AC-33 | satisfied | Existing regular-file and FIFO occupants refuse before run-start without replacement, deletion, or mode change. |
| AC-34 | satisfied | Append and sync failure cases pass with one console refusal, no retry/fallback/later admission, and cleanup. |
| AC-35 | satisfied | Missing-plus-unexpected path-set selection is stable at `path=-`. |
| AC-36 | satisfied | Enumeration-error snapshot refusal case passes with empty entries and no retry. |
| AC-37 | satisfied | Observed-path `lstat` failure case passes with null metadata. |
| AC-38 | satisfied | Single-open failure case preserves metadata and suppresses later predicates. |
| AC-39 | satisfied | Read-before-EOF failure case refuses without another read or snapshot. |
| AC-40 | satisfied | Opened-object type mismatch case refuses without fallback. |
| AC-41 | satisfied | Initial/open-handle identity mismatch refuses before reading. |
| AC-42 | satisfied | Final type/identity drift refuses while retaining the captured hash and without resnapshot. |
| AC-43 | satisfied | Trace lines 1, 76-80, and 3843-3849 prove the required shell, exec, create request, `0600` observations, and retained-descriptor topology. |
| AC-44 | satisfied | The required exact envelope and descendant-following trace are present, so ambient-mask-only evidence is not being used. |
| AC-45 | satisfied | `gateway.json` is read before the evidence scope at lines 107-117; requests use recorded loopback port via HTTP at lines 4267-4318, so harness creation remains in the serving gateway. |
| AC-46 | satisfied | The HTTP client treats nonzero curl exit as fixture failure at lines 4318-4330; it cannot produce a harness spawn result. |

## Completeness and subtraction lenses

The integrated result contains the required creation, retained descriptor, metadata checks, refusal boundary, deterministic coverage, source-topology evidence, and full repository gate. No required current-stage behavior is missing.

The exact amendment removes the prior chmod and descriptor-path helper machinery. It adds no new helper, fallback sink, retry, reopening path, or custody surface. There is therefore no YAGNI finding. No finding needs a closure proposal, so deletion analysis is not applicable beyond confirming that the obsolete mechanism was deleted.
