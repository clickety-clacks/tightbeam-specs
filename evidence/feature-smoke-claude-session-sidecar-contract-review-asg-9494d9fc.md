# F8 successor review — feature-smoke Claude session-sidecar contract

Review assignment: `asg_9494d9fc-ad92-4cf0-8eba-4c995cc54bb9`

Producer assignment: `asg_ee922fe3-3005-406b-af46-82cb4ffa2d10`

Reviewed at: 2026-08-29 00:37 PT

Verdict: **reviewed-clean**

## Outcome

I found no blocking or important defect in the exact amended contract or its recon.
The F8 amendment replaces the unsupported no-follow open with a documented OTP 28
path-handle-path identity check. It preserves the F1-F7 closures, the exact evidence
boundary, one-file implementation custody, PID independence, and every live-action hold.

This verdict approves only the reviewed specification bytes. It does not release an
implementation, fixture, smoke, integration, deployment, restart, parent lane, or live
state change.

## Exact target and custody

| Item | Verified value |
| --- | --- |
| Repository | `https://github.com/clickety-clacks/tightbeam-specs.git` |
| Reviewed commit | `7717ec827a7448b9b99518d2518383c43c8bd82a` |
| Tree | `3e5c96a2bb0c823e73a66a9015b8ec69ed43dda0` |
| Parent | `cf6653ede091b5ef20d0474c312e0bf611020814` |
| Remote ref | `refs/heads/spec/feature-smoke-sidecar-contract-asg-ee922fe3` |
| Contract blob | `c144f2193a3b7cea64392dcce754cbef5a526622` |
| Contract SHA-256 | `74bb0c3069d41948095eb998b28a4788587b6149bb77b6ccaa68fa3b7efafcc0` |
| Recon blob | `28036780aa03c172a5058d3e981425e8f84790a0` |
| Recon SHA-256 | `d55b343775e55b0fec614ab641d5dfe4b6251ee2bf87d0ccc62ea8e61141ab91` |
| Binary two-file diff SHA-256 | `357b9171bb2a4183992b4c4dfcc19ef46627b0b4d5c04e6aecf0108a66a9681a` |
| Changed paths | The contract and its recon report only |
| Whitespace gate | `git diff --check` passed |

I used the owned Gibson clone at
`/home/mike/.tightbeam/work/917749529dbe/tightbeam-specs`. The remote ref, commit,
tree, parent, blobs, file hashes, and two-file diff matched producer seal
`att_216776a6-e9aa-4d3a-95d6-98d96b114024`.

## Authority and independent model

- Work item `wi_15f960ac-3083-437a-9979-0f0313b7f474` remains open.
- Mike ruling `dr_9a179914-0d23-440b-9a3b-4577e0d0c707` authorizes only the bounded
  F8 object-identity amendment, its exact seal, and one fresh linked review.
- Class 12 requires a strict fixture-only Claude sidecar contract that does not compare
  the sidecar filename with Tightbeam launcher `osPid`.
- The preserved live evidence proves only that launcher `osPid=1907930` differed from
  sidecar stem `1907971`. The contract does not infer a process relationship from it.
- The permitted implementation surface remains only `scripts/feature_smoke.exs` on a
  synchronized `origin/0.1.9` base after a separate release.

I built this model from the work item, controlling rows, exact contract, and exact recon
before I read the producer seal. I then checked the producer claim against the parent
diff and the prior F8 verdict `att_101f8af2-6694-4389-8dc0-b39883077f48` with report
`art_5233e4ba`.

## Independent OTP 28 verification

Gibson reported Elixir 1.19.5 on Erlang/OTP 28.5.

The installed OTP source supports every operation that C-08 names:

- `kernel-10.6.3/src/file.erl:653-664` specifies that `read_file_info/1` accepts an
  I/O device.
- `kernel-10.6.3/src/file.erl:689-696` documents the raw-handle path.
- `kernel-10.6.3/src/file.erl:702-761` documents `type`, `major_device`,
  `minor_device`, and `inode`.
- `kernel-10.6.3/src/file.erl:786-790` dispatches a raw descriptor to
  `read_handle_info`.
- `kernel-10.6.3/src/file.erl:813-855` documents link metadata and the `symlink` type.
- `kernel-10.6.3/src/file.erl:279-289` lists the supported open modes and contains no
  no-follow mode.

A read-only `/etc/hosts` specimen used initial `:file.read_link_info/1`, one raw
read-only open, `:file.read_file_info/1` on that handle, one read to EOF, and final
`:file.read_link_info/1` before close. All three types were `regular`. All three
`{major_device, minor_device, inode}` tuples matched. The specimen read 221 bytes and
produced a 32-byte SHA-256 digest. It changed no file.

The contract claims only object-identity continuity. It explicitly does not claim
`O_NOFOLLOW`, and it does not claim to observe a transient same-object path state.
Initial-path identity A versus opened-handle identity B refuses before read. A final
path type or identity mismatch after read refuses with the captured hash. These two
boundaries are mechanically decidable in one file.

## Prior-finding closure

| Finding | Result | Current evidence |
| --- | --- | --- |
| F1 — per-leg topology | satisfied | Terms and C-01 define Claude, cleanup, then Codex and forbid cross-home reads; lines 74-91 and 185-219. |
| F2 — retained evidence | satisfied | C-10 fixes creation, sync, sequence, keys, entries, 29 checks, truncation, and retention; lines 437-589. |
| F3 — implementation base | satisfied | AS-01 and C-11 name `origin/0.1.9`; lines 118-121 and 590-601. |
| F4 — same-path predicate tie | satisfied | C-09 orders category, raw path, then C-10 predicate and mapped clause; lines 414-435 and 503-538. |
| F5 — evidence-sink failure | satisfied | C-10 makes the console refusal the sole guarantee and forbids retry, fallback, and a second append; lines 451-468 and AC-34. |
| F6 — absent path | satisfied | `FX_PATH_SET` is set-level `path=-`, with no missing candidate or path sort; lines 414-430 and AC-35. |
| F7 — snapshot acquisition | satisfied | C-08 maps each enumeration, metadata, open, handle-info, type, identity, read, and final-path failure to one `FX_SNAPSHOT`; C-10 fixes partial evidence; AC-36 through AC-42 cover the failure positions. |
| F8 — supported safe capture | satisfied | Terms, AS-10, I-05, C-08, C-10, and AC-41 through AC-42 specify the documented three-point regular-object identity check and its before-read and after-read evidence. |

## Clause table

| Clause group | Classification | Evidence |
| --- | --- | --- |
| Goal | satisfied | Lines 23-31 define one fixture-only admission rule without launcher-PID equality. |
| Non-Goals | satisfied | Lines 33-48 exclude product behavior, Codex admission, live actions, a second fixture, and an agent operating pattern. |
| Terms | satisfied | Lines 50-114 define every phase, path, identity, evidence token, file, and record used later. |
| AS-01 through AS-10 | satisfied | Lines 116-149 state the branch, observed facts, time model, release hold, and OTP 28 seam as falsifiable assumptions. |
| I-01 through I-12 | satisfied | Lines 151-176 preserve fixture scope, complete-set evaluation, PID independence, no mutation, one-shot use, evidence limits, custody, and cleanup. |
| Architecture and validation seam | satisfied | Lines 178-188 keep the mechanism inside the fixture smoke and separate the two harness legs. |
| C-01 | satisfied | Lines 190-219 decide all phase, refusal, cleanup, and cross-home boundaries. |
| C-02 | satisfied | Lines 221-240 define the exact five-path Claude set, types, modes, cardinality, and nesting refusal. |
| C-03 | satisfied | Lines 242-252 bind the canonical filename only to the internal positive integer `pid`. |
| C-04 | satisfied | Lines 254-278 define the exact eleven-member JSON schema and predicates. |
| C-05 | satisfied | Lines 280-295 define the inclusive spawn-to-snapshot freshness bracket and exclude proxy clocks. |
| C-06 | satisfied | Lines 297-317 define phase cardinality, sidecar continuity, independent backup rotation, and no reuse. |
| C-07 | satisfied | Lines 319-327 require an empty Codex delta and forbid Claude classification there. |
| C-08 | satisfied | Lines 329-390 define one ordered attempt, documented OTP calls, three identity checks, every acquisition refusal, and no retry or second snapshot. |
| C-09 | satisfied | Lines 392-435 define category, path, predicate, and clause tie-breaking, including set-level `path=-`. |
| C-10 | satisfied | Lines 437-589 define exact evidence bytes, sink failure, partial snapshot entries, identity-failure hash boundaries, and cleanup retention. |
| C-11 | satisfied | Lines 590-601 preserve one-file implementation custody. |
| C-12 | satisfied | Lines 603-622 preserve the review, release, deterministic proof, one-fixture, and implementation-review sequence. |
| AC-01 through AC-35 | satisfied | Lines 629-665 decide the retained lifecycle, path, schema, evidence, ordering, no-reuse, and custody cases. |
| AC-36 through AC-42 | satisfied | Lines 666-672 decide enumeration, metadata, open, read, type, and both object-identity failure positions. |
| Open Questions | satisfied | Lines 674-688 close F8 under the exact ruling and retain the explicit implementation and fixture holds. |
| Spec homing | satisfied | The pushed commit, tree, blobs, file hashes, producer artifacts, and this linked review bind the canonical set in `tightbeam-specs`. |
| Agent operating pattern | satisfied | Non-Goals explicitly states that this fixture contract adds no agent-facing pattern. |

No clause is unsatisfied or unproven.

## Completeness, YAGNI, law, and subtraction

The amended result covers both identity-mismatch positions and both evidence outcomes.
It adds no helper, subprocess, NIF, dependency, retry, fallback reader, second snapshot,
admitted path, implementation file, fixture attempt, or live authority.

Every behavioral addition in the diff traces to F8 and ruling `dr_9a179914`. The
mechanism uses deterministic filesystem facts. It does not ask the substrate to infer a
process relationship. Each refusal keeps a cause and principal, and a satisfied check
adds no operator step.

Deletion does not close F8 because deleting byte capture or the non-symlink boundary
loses the required exact-home proof. Accepting permanent acquisition failure leaves the
required smoke blocked. The bounded identity check is therefore the smallest authorized
closure.
