# Independent F9 successor review — feature-smoke Claude session-sidecar contract

Reviewed at 2026-08-29 10:36 PT.

## Verdict

`reviewed-clean` for exact contract commit
`beb7c222c908486a774ded9656a5ababe596bd02`.

No blocking or important finding remains. The F9 amendment closes the process-boundary
gap without changing the admitted runtime set, required modes, product custody, live
authority, or one-shot fixture rule. This verdict does not release the Class 12 block;
the opener retains that authority under C-12.

## Exact subject and provenance

| Item | Independently verified value |
| --- | --- |
| Review assignment | `asg_69d68592-6846-4dde-916e-3a697a7fc1e7` |
| Producer assignment | `asg_ee922fe3-3005-406b-af46-82cb4ffa2d10` |
| Work item | `wi_15f960ac-3083-437a-9979-0f0313b7f474` |
| Contract commit | `beb7c222c908486a774ded9656a5ababe596bd02` |
| Contract tree | `571087f424c3d5b7b77954ec6805073f3934d4f3` |
| Contract SHA-256 | `e5746d178ba94d35c59ce9a3a9d21a1fe4bf4023faa2ecd1c9145fbe3848a338` |
| Recon SHA-256 | `5472f678b6d4d1b4bc4e6b34f1e241aedb7d5ffc6d18ae89e81562dfa7d19c04` |
| Parent-to-target binary diff SHA-256 | `0e442f96666d20946300c59d833df5a670dacea5fe9edd5cdaf836c6ab426f7e` |
| Preserved product commit | `08e55de896106aa7fcc2ea7f60f1357e5d6cf772` |
| Preserved feature-smoke blob | `6d9e236a34d99f710d330af0b0dc794063565709` |

I read the review assignment, all of its attests, the producer assignment's complete
attest history, and the full work-item trace before reading the producer's seal. I then
read the contract and reconstruction twice, read the previous F8 clean review, the
implementation changes-requested review, the creation-mode mechanism report, the F9
changes-requested review, and the controlling `contract-amendment` ruling.

The exact target changes only the contract and reconstruction: 117 insertions and five
deletions. `git diff --check` passes. No product byte is part of the amendment.

## Independent model

The feature smoke is a client of an already-running fixture gateway. The exact product
source documents and executes `mix run --no-start`, reads the existing
`<base>/gateway.json`, and sends each command through `curl` to the recorded loopback
gateway (`scripts/feature_smoke.exs:1-8,107-115,4246-4309`). A failed `curl` result enters
the fixture failure path (`scripts/feature_smoke.exs:4297-4309`).

The later launch envelope therefore changes only the zsh/Mix client process tree. It
cannot retroactively change the process state of the already-serving gateway. Gateway
dispatch handles spawn and wake (`lib/tightbeam/gateway.ex:631-665,3899-3975`), and the
gateway's adapter coordinator starts workers under its dynamic supervisor
(`lib/tightbeam/adapter_coordinator.ex:680-719`). Local or remote harness commands are
ultimately opened from that gateway-owned process tree
(`lib/tightbeam/harness_process.ex:690-708`). This supports the contract's narrow F9
claim: the client's exact `0077` umask governs its evidence-file creation but does not
govern gateway or harness descendants.

## Clause table

Status vocabulary: **satisfied** means the exact artifact is decisive; **unproven** means
the clause needs future implementation or live evidence and is correctly gated; no row
is unsatisfied.

| Clause | Status | Evidence |
| --- | --- | --- |
| Goal | Satisfied | The fixture-only sidecar admission and launcher-PID non-equivalence remain exact (`contract:26-34`). |
| Non-Goals | Satisfied | No product/live authority, second fixture, or agent operating pattern is introduced (`contract:36-51`). |
| Terms | Satisfied | All operational nouns are grounded; F9 adds only the launch envelope, gateway boundary, and effective creation mode (`contract:53-135`). |
| AS-01 | Satisfied | Authorized branch and sync duty remain explicit (`contract:139-142`). |
| AS-02 | Satisfied | Owned baseline and fixture admission authority remain separated (`contract:143-145`). |
| AS-03 | Satisfied | Preserved final-fixture path metadata and hash are bounded (`contract:146-148`). |
| AS-04 | Satisfied | Unequal launcher and sidecar PIDs support only the negative claim (`contract:149-151`). |
| AS-05 | Satisfied | Deleted bytes are not promoted into schema authority (`contract:152-154`). |
| AS-06 | Satisfied | Read-only current samples support the eleven-member schema (`contract:155-157`; `recon:207-220`). |
| AS-07 | Satisfied | Expected workdir derivation remains pinned (`contract:158-160`). |
| AS-08 | Satisfied | Epoch-millisecond compatibility is explicit and falsifiable (`contract:161-163`). |
| AS-09 | Satisfied | One future fixture still needs separate release (`contract:164-165`). |
| AS-10 | Satisfied | OTP file-information seams are stated as assumptions with a recheck gate (`contract:166-170`). |
| AS-11 | Satisfied | OTP `0666` request and kernel umask application are stated truthfully and gated by trace (`contract:171-175`). |
| AS-12 | Satisfied | Exact product commit/blob prove `--no-start`, `gateway.json`, loopback HTTP, and curl failure (`contract:176-182`; product source cited above). |
| I-01 | Satisfied | Admission remains Claude-only and fresh-fixture-only (`contract:186`). |
| I-02 | Satisfied | Baseline precedes spawn (`contract:187`). |
| I-03 | Satisfied | One complete runtime delta or one C-08 refusal (`contract:188-189`). |
| I-04 | Satisfied | Launcher PID is excluded from admission (`contract:190-191`). |
| I-05 | Satisfied | Decision inputs and acquisition-failure inputs are closed (`contract:192-196`). |
| I-06 | Satisfied | Codex runtime delta remains empty (`contract:197`). |
| I-07 | Satisfied | Fixture cannot repair harness runtime paths (`contract:198-199`). |
| I-08 | Satisfied | Spawn consumes the fixture (`contract:200`). |
| I-09 | Satisfied | Evidence excludes raw bytes and decoded values (`contract:201`). |
| I-10 | Satisfied | Product custody remains one file (`contract:202`). |
| I-11 | Satisfied | Frozen parent identifiers remain pinned (`contract:203-205`). |
| I-12 | Satisfied | Runtime mismatch cannot mutate observed paths; sink failure is bounded (`contract:206-209`). |
| I-13 | Satisfied | Exact launch envelope and no post-create repair remain mandatory (`contract:210-212`). |
| I-14 | Satisfied | Client-only umask and pre-existing gateway process tree close F9 (`contract:213-215`). |
| Architecture | Satisfied | One fixture validation seam; no product-runtime or supervision expansion (`contract:217-227`). |
| C-01 | Satisfied | Run-start and per-leg phase order are decidable (`contract:229-258`). |
| C-02 | Satisfied | Exact five Claude paths and exact modes remain unchanged, including `0755` backups, `0700` sessions, and `0644` sidecar (`contract:260-275`). |
| C-03 | Satisfied | Canonical filename binds only to internal JSON PID (`contract:281-291`). |
| C-04 | Satisfied | Exact JSON member set, types, and semantic checks remain closed (`contract:293-317`). |
| C-05 | Satisfied | Freshness uses the inclusive spawn interval, not unsupported mtime inference (`contract:319-334`). |
| C-06 | Satisfied | Cardinality, continuity, cleanup, and no-reuse rules remain exact (`contract:336-356`). |
| C-07 | Satisfied | Any Codex runtime delta remains a refusal (`contract:358-366`). |
| C-08 | Satisfied | One non-retrying snapshot has a result for every acquisition failure (`contract:368-429`). |
| C-09 | Satisfied | Error category, raw path, and predicate order decide the first failure (`contract:431-474`). |
| C-10 | Satisfied | OTP `0666` create under client `0077`, effective `0600`, same-handle proof, evidence shape, sink boundary, and no chmod are exact; gateway descendants are excluded from client umask (`contract:476-648`). |
| C-11 | Satisfied | Future implementation custody remains only `scripts/feature_smoke.exs` (`contract:650-665`). |
| C-12 | Satisfied | Review, release, sync, trace, source-topology, deterministic, live, and successor-review gates are ordered (`contract:667-731`). |
| AC-01 | Satisfied | Fresh run-start state passes once (`contract:736`). |
| AC-02 | Satisfied | Reused fixture refuses before credential preflight (`contract:737`). |
| AC-03 | Satisfied | Each leg proves its own baseline without cross-home inspection (`contract:738`). |
| AC-04 | Satisfied | Exact Claude set passes without launcher PID (`contract:739`). |
| AC-05 | Satisfied | Canonical filename/internal PID equality passes (`contract:740`). |
| AC-06 | Satisfied | Leading-zero path refuses at the whole-set boundary (`contract:741`). |
| AC-07 | Satisfied | Unequal internal PID refuses semantically (`contract:742`). |
| AC-08 | Satisfied | Invalid UTF-8 maps to `FX_JSON` (`contract:743`). |
| AC-09 | Satisfied | Malformed JSON maps to `FX_JSON` (`contract:744`). |
| AC-10 | Satisfied | Duplicate JSON member maps to `FX_JSON` (`contract:745`). |
| AC-11 | Satisfied | Missing sidecar member maps to schema refusal (`contract:746`). |
| AC-12 | Satisfied | Extra sidecar member maps to schema refusal (`contract:747`). |
| AC-13 | Satisfied | Wrong member type maps to schema refusal (`contract:748`). |
| AC-14 | Satisfied | Wrong cwd refuses without exposing values (`contract:749`). |
| AC-15 | Satisfied | Out-of-interval timestamp refuses (`contract:750`). |
| AC-16 | Satisfied | Duplicate sidecar or backup refuses the whole set (`contract:751`). |
| AC-17 | Satisfied | Phase-local backup identity is allowed when freshness passes (`contract:752`). |
| AC-18 | Satisfied | Sidecar identity drift refuses (`contract:753`). |
| AC-19 | Satisfied | Unexpected nested path refuses with `path=-` (`contract:754`). |
| AC-20 | Satisfied | Symlink refuses without following (`contract:755`). |
| AC-21 | Satisfied | Wrong `.claude.json` mode refuses (`contract:756`). |
| AC-22 | Satisfied | Oversize sidecar refuses before decode (`contract:757`). |
| AC-23 | Satisfied | Wrong top-level JSON shape refuses (`contract:758`). |
| AC-24 | Satisfied | Codex runtime path refuses without Claude inspection (`contract:759`). |
| AC-25 | Satisfied | Repeated multi-failure cases have one deterministic winner (`contract:760`). |
| AC-26 | Unproven by design | The seven-record passing live matrix remains gated after implementation and release (`contract:761`). |
| AC-27 | Satisfied | A refused spawned fixture remains consumed and retained (`contract:762`). |
| AC-28 | Satisfied | Implementation cannot begin before review/release and remains one-file (`contract:763`). |
| AC-29 | Unproven by design | Full sequential Claude-plus-Codex matrix remains a later real-input gate (`contract:764`). |
| AC-30 | Satisfied | New runtime shape refuses with no retry (`contract:765`). |
| AC-31 | Satisfied | Frozen parent readback remains required (`contract:766`). |
| AC-32 | Satisfied | Wrong cwd produces a bounded terminal evidence record (`contract:767`). |
| AC-33 | Satisfied | Preexisting evidence path refuses without mutation (`contract:768`). |
| AC-34 | Satisfied | Sink failure has console-only evidence, no retry, and cleanup (`contract:769`). |
| AC-35 | Satisfied | Missing-plus-extra set refusal is `path=-` without invented ordering (`contract:770`). |
| AC-36 | Satisfied | Enumeration failure has one empty-entry snapshot refusal (`contract:771`). |
| AC-37 | Satisfied | Observed-path `lstat` failure preserves null metadata (`contract:772`). |
| AC-38 | Satisfied | Open failure retains metadata but no content hash (`contract:773`). |
| AC-39 | Satisfied | Read failure has no second read or snapshot (`contract:774`). |
| AC-40 | Satisfied | Opened non-regular object refuses without fallback (`contract:775`). |
| AC-41 | Satisfied | Initial/opened identity mismatch refuses before read (`contract:776`). |
| AC-42 | Satisfied | Final identity/type mismatch refuses while retaining captured hash (`contract:777`). |
| AC-43 | Unproven by design | Exact umask, exec, create-mode, metadata, and no-chmod syscall trace remains a future gate (`contract:778`). |
| AC-44 | Satisfied | Ambiently-correct mode without exact envelope/trace is nonconforming (`contract:779`). |
| AC-45 | Satisfied | Existing gateway + loopback HTTP place gateway/harness creation outside the client tree; product source supports the topology (`contract:780`; product source cited above). |
| AC-46 | Satisfied | An unserved recorded loopback port produces nonzero curl and the fixture failure path before any spawn result (`contract:781`; `scripts/feature_smoke.exs:4271-4309`). |
| Open Questions | Satisfied | No open contract question remains (`contract:783-801`). |
| Spec homing | Satisfied | Both artifacts are durable in `tightbeam-specs` at the exact reviewed commit and hashes. |
| Agent operating pattern | Satisfied | The contract explicitly establishes none (`contract:50-51`). |

The three **unproven by design** rows are future execution evidence, not specification
holes. C-12 correctly prevents them from being treated as already passed.

## F1-F9 regression and correction check

| Finding | Result | Evidence |
| --- | --- | --- |
| F1 | Closed | Per-leg phases and separate home reads remain explicit in C-01 and AC-03/AC-29. |
| F2 | Closed | Evidence bytes, canonical JSONL, synchronization, and seven-record cardinality remain exact in C-10. |
| F3 | Closed | `origin/0.1.9` and one-file product custody remain exact in AS-01/C-11. |
| F4 | Closed | C-09 plus the fixed C-10 check order decide every same-path predicate conflict. |
| F5 | Closed | Evidence append/sync failure is console-only, non-retrying, and cleanup-preserving. |
| F6 | Closed | `FX_PATH_SET` uses `path=-`; no missing path is fabricated or mixed into raw-path order. |
| F7 | Closed | C-08 defines one acquisition attempt and one ordered, content-free refusal for each failure seam. |
| F8 | Closed | Initial path, open-handle, and final path identity continuity uses supported OTP 28 operations and one open handle. |
| F9 | Closed | `--no-start`, `gateway.json`, loopback HTTP, and curl failure prove a pre-existing gateway boundary; I-14 limits `0077` to the client tree, C-02 modes remain unchanged, and AC-45/AC-46 make both positive and absent-gateway cases decidable. |

## Completeness, necessity, and subtraction

Completeness: every normative clause has an acceptance example or acceptance row, every
failure branch has a named result, and future empirical claims remain behind explicit
gates. The amendment does not rely on the producer's summary for the topology claim; the
preserved product source independently supports it.

Necessity: every observable delta from parent contract commit
`6e8b72a4abad1d272e5dbe21c10d73491b08e5be` traces to F9 and ruling
`dr_16de6d11-492c-4ec4-aaa2-6cb1a03d4d7d`. The amendment adds AS-12, I-14, the C-10
process-boundary statement, the C-12 source-topology gate, and AC-45/AC-46. It does not
change product behavior or any required runtime mode.

YAGNI: no helper, dependency, retry, secondary fixture, new admitted path, product file,
or live mutation appears. The reconstruction records the rejected alternatives and
keeps implementation custody at one file.

Subtraction: deleting the new F9 clauses would reopen the false assumption that a later
client umask flows into an already-serving gateway. Accepting the ambiguity would leave
the required path modes undecidable. The narrow declarative correction is therefore the
smallest closure; no new runtime mechanism is added.

## Independent checks performed

- Read both amended artifacts twice and verified their exact SHA-256 values.
- Verified exact commit, tree, parent, changed-file set, binary diff hash, and clean
  `git diff --check` in an owned Gibson clone.
- Read the integrated preserved product source at exact commit `08e55de8`, including
  the feature-smoke launch header, gateway-record read, local-deployment lifecycle,
  HTTP post/curl failure path, gateway dispatch, adapter supervision, and harness command
  launch.
- Read the complete prior review and ruling chain through F9.
- Did not implement, run a fixture or smoke, mutate live state, release the Class 12
  block, or modify producer/product bytes.

