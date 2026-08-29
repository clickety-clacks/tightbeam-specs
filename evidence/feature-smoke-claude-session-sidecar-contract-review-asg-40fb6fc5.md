# F7 review — feature-smoke Claude session-sidecar contract

Review assignment: `asg_40fb6fc5-db5a-4ba2-ad8c-0669ecd42f2b`

Producer assignment: `asg_ee922fe3-3005-406b-af46-82cb4ffa2d10`

Reviewed at: 2026-08-29 00:11 PT

Verdict: **changes-requested**

## Exact target and custody

- Reviewed commit: `cf6653ede091b5ef20d0474c312e0bf611020814`
- Tree: `12f514db44f4fa7ce004b629234faa6feaa251b3`
- Parent: `aad893964b0bbf08c99dfec54f64801611e85eca`
- Remote branch: `refs/heads/spec/feature-smoke-sidecar-contract-asg-ee922fe3`
- Changed paths: the contract and its recon report only.
- Contract blob: `2b86f3bcb4513882d68903e3c8fd25b1dc986dea`
- Contract SHA-256: `708742058e18df78b5e1a6794c411032a4de32fbcfac73c18d480c8c1732b2c8`
- Recon blob: `3b48c329170d273d93e219eac70d0652beee058e`
- Recon SHA-256: `67c256a63641ae56220cd59900414bdc241bd1d7485fd23a2981b522e294ff07`
- Binary diff SHA-256: `d8eac50486ef07bbe26756249a9f924106d1b8e58b7327e87977722434f547c0`
- `git diff --check` passed.

I read the full current work-item trace and the producer history. I also read all three prior review verdicts and reports. The three operator rulings select the bounded F1-F4, F5-F6, and F7 amendments.

## Prior-finding closure

| Finding | Result | Evidence |
| --- | --- | --- |
| F1 — per-leg topology | satisfied | Terms and C-01 require one Claude leg, cleanup, and one Codex leg. They forbid cross-home reads. Contract lines 74-91 and 182-211. |
| F2 — retained evidence | satisfied subject to F8 | C-10 fixes creation, mode, record order, fields, 29 checks, sync, retention, and refusal truncation. Contract lines 397-545. |
| F3 — implementation base | satisfied | AS-01 and C-11 name `origin/0.1.9`. The remote branch resolves to `bdf0ad2c9ae4078f897a00e8c57767968676477c`. Contract lines 115-118 and 547-558. |
| F4 — predicate tie | satisfied | C-09 orders category, raw path, then C-10 predicate. Contract lines 352-395. |
| F5 — evidence-sink failure | satisfied | C-10 makes the console refusal the sole guarantee. It forbids retry, fallback, and a second append. Contract lines 411-428. |
| F6 — absent path | satisfied | `FX_PATH_SET` uses `path=-`. It creates no missing-path candidate and performs no path sort. Contract lines 374-383 and 622. |
| F7 — snapshot acquisition result | unsatisfied by F8 | Enumeration, `lstat`, open, read, disappearance, and type-change map to `FX_SNAPSHOT`. The required open operation has no supported implementation under C-11. Contract lines 321-350 and 623-627. |

## Finding

### F8 — important — the required no-follow open has no authorized implementation seam

C-08 requires the validator to open each required regular file once “without following a symlink.” It also requires opened-object type verification. C-11 limits the implementation to `scripts/feature_smoke.exs`.

The authorized product branch uses Elixir 1.19 on OTP 28. OTP 28.5 documents all `:file.open/2` modes in `kernel-10.6.3/src/file.erl` lines 279-289 and 1260-1424. That list has no no-follow mode. The current product has no syscall or filesystem helper that supplies this capability.

A read-only Gibson probe reproduced the gap:

```text
mise exec -- elixir -e 'IO.inspect(File.lstat!("/etc/mtab").type); IO.inspect(:file.open(~c"/etc/mtab", [:read, :binary, :raw, :no_follow]))'
:symlink
{:ok, {:file_descriptor, :prim_file, ...}}
```

OTP accepts the unknown atom but still follows the symlink. A normal `lstat`, path open, and handle `fstat` cannot prove no-follow behavior during a path replacement. A symlink to a regular file can therefore pass the opened-object type check.

The contract leaves two different implementations possible. One can use the documented OTP API and follow the replacement symlink. Another can add an unstated external helper or native dependency for `O_NOFOLLOW`. These implementations differ in core refusal behavior and dependency surface.

Deleting all byte capture would lose C-02 through C-06. Deleting only the no-follow requirement would weaken the existing non-symlink safety boundary. Accepting the missing primitive as `FX_SNAPSHOT` would make every required regular file refuse. The closure needs an explicit, available primitive or a supported object-identity algorithm and matching acceptance case. A new helper or dependency needs separate authority.

Citations: contract C-08 lines 327-350; C-11 lines 547-558; AC-20 and AC-40 lines 607 and 627; recon D-09 lines 265-282; product `mix.exs` at `origin/0.1.9` commit `bdf0ad2c9ae4078f897a00e8c57767968676477c`; OTP 28.5 `kernel-10.6.3/src/file.erl` lines 279-289 and 1260-1424.

## Clause table

| Clause | Classification | Evidence |
| --- | --- | --- |
| Goal | satisfied | The contract stays fixture-only and independent of launcher `osPid`. |
| Non-Goals | satisfied | It excludes source, live, Codex admission, retry, and second-fixture authority. |
| Terms: fixture, home, baseline, snapshot, delta, path, token | unproven | The snapshot result is exact, but its no-follow open has no supported primitive. F8. |
| Terms: harness leg and phases | satisfied | The sequential Claude and Codex legs are exact. |
| Terms: stem, mode, sidecar, identity | satisfied | Each predicate and identity field is exact. |
| Terms: evidence file and record | satisfied subject to F8 | The record schema and partial-entry rules are exact if the snapshot primitive exists. |
| AS-01-AS-09 | satisfied | The branch, observations, epoch assumption, CWD seam, and one-shot release are explicit. |
| I-01-I-04 | satisfied | Scope, baseline proof, snapshot result, and launcher independence are exact. |
| I-05 | unproven | A followed replacement symlink can supply regular opened-object metadata and bytes. F8. |
| I-06-I-12 | satisfied | Codex refusal, mutation limits, consumption, evidence limits, custody, frozen state, and sink failure are exact. |
| Architecture pattern and seam | satisfied | The validator remains fixture-only and per-leg. |
| C-01 | satisfied | Phase order and cleanup are decidable. |
| C-02 | unproven | Exact type and byte evidence depend on the unsupported no-follow open. F8. |
| C-03-C-07 | satisfied subject to F8 | The captured-value predicates are exact. |
| C-08 | unsatisfied | It requires a no-follow open that the authorized one-file toolchain cannot perform. F8. |
| C-09 | satisfied subject to F8 | `FX_SNAPSHOT` ordering is exact after a supported acquisition operation exists. |
| C-10 | satisfied subject to F8 | The 29 checks, partial entries, null fields, and no-retry evidence are exact. |
| C-11 | unproven | One-file custody supplies no syscall helper or dependency for no-follow open. F8. |
| C-12 | satisfied subject to F8 | The release order is exact, but implementation cannot start from a decidable mechanism. |
| AC-01-AC-19 | satisfied subject to F8 | The cases are exact after safe capture exists. |
| AC-20-AC-39 | satisfied subject to F8 | Static symlink and acquisition failures are exact, but a replacement symlink can bypass the intended open boundary. |
| AC-40 | unproven | Opened-object type verification does not detect a symlink that resolves to a regular file. F8. |
| Open Questions | unsatisfied | `None` omits the required primitive or dependency choice. F8. |
| Spec homing | satisfied | The remote commit, tree, two blobs, SHA-256 values, artifact rows, producer, and linked review bind the canonical set. |
| Agent operating pattern | satisfied | Non-Goals states that this fixture contract adds no agent pattern. |

## Completeness, YAGNI, law, and subtraction

The F7 text adds no retry, fallback reader, second snapshot, path admission, or live authority. F1-F6 remain closed. The new `FX_SNAPSHOT` result is deterministic once acquisition uses a supported primitive.

The contract cannot leave the primitive implicit. An external helper, native dependency, or subprocess protocol would add unreviewed capability and failure paths. Wisdom 6 requires deterministic mechanism at this boundary. Wisdom 25 requires the failure to remain durable. The contract meets both rules only after it selects an available mechanism.

The narrow validator should still exist. Deleting it loses the required exact-home smoke. Accepting permanent failure leaves the gate closed. The next ruling must select a supported acquisition seam or relax the no-follow claim explicitly.
