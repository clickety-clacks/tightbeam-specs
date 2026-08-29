# Feature-smoke Claude session-sidecar contract — recon and clause map

Status: supporting evidence for producer assignment
`asg_ee922fe3-3005-406b-af46-82cb4ffa2d10`.

This report records sources, observations, design choices, declined alternatives, and
two-way traceability for
`specs/tightbeam/feature-smoke-claude-session-sidecar-contract.md`. It is not
implementation authority.

## Durable trace readback

Read on 2026-08-14 UTC:

- Work item: `wi_15f960ac-3083-437a-9979-0f0313b7f474`, open.
- Work-item trace: 30 assignments, 1,425 timeline events, 677 attests.
- Sorted normalized work-item trace SHA-256:
  `d847c27ad0e5de9d6c9868f9ec814fedb286cdaa74a00e19d8828834fa8bda7c`.
- Sorted normalized work-item readback SHA-256:
  `1ad83ea32badbd4fe22f2cb661cc2c959a8748d27d4252a647023cdcc101ba63`.
- Producer assignment had no prior attests before recon. Recon receipt:
  `att_fe41e651-f77a-4df4-b1d4-efc3e6c05b44`.

Post-review readback on 2026-08-29 UTC, before the amended-artifact seal:

- Work item remains open with 47 assignments and 1,801 timeline events, including 833
  progress, completion, surrender, or verdict attests.
- Canonical sorted full work-item trace SHA-256:
  `0054b4937e636244480badba55f861596b9640156f684f61e3f0a88edea00a5e`.
- `specRefName` and `specRefSha256` remain null. Mike's ruling
  `dr_e649588d-317c-4c0a-aae3-ea95683495e3` authorizes a pushed Git commit plus
  hash-bearing attest as the binding substitute.
- The first linked review is closed at changes-requested verdict
  `att_db09d91a-e208-4806-acd2-700088124228` and completion
  `att_6aa0bffe-a742-4df5-9535-bb6b9cc9489b`.

## Authority and preserved state

| Source | Material ruling or fact |
| --- | --- |
| `att_d0b6affe-af19-44f5-9d6e-ca24292d9743` | Class 12: final fixture is consumed; future release needs a strict fixture-only `sessions/<positive-numeric>.json` contract independent of launcher `osPid`, then one fresh same smoke. |
| `att_a134b512-0dd2-4f24-b1d7-7d56e6dca9bf` | Fact 390 blocks the parent holder. Facts 373, 384, and 387, parent commit, surrendered history, and custody remain frozen. |
| `att_d694b965-8471-46df-842d-5ef915372aa8` | The initial assignment boundary allowed contract and recon artifacts plus a ready-or-blocked verdict. Later Mike rulings `dr_5fd346df`, `dr_fb80acd4`, and `dr_7262873b` add only their three bounded amendments, seals, and reviews. Fixture, smoke, implementation, integration, and live mutation remain forbidden. |
| `att_15121266-f5e8-4cbc-bd4b-22dae1ca2bbd` | Claude-only `.claude.json`, one bounded backup, and the `sessions` runtime namespace are fixture surfaces. Evidence excludes file contents. |
| `att_32e44600-c470-4b16-b9a9-54381992ce9a` | A sidecar is present after successful spawn and tuning, before the first wake. The earlier empty-pre-turn assumption is false. |
| `att_3db588ec-91b1-4af8-a3af-84eb98186fa7` | The last authorized replacement fixture was one-shot. A new mismatch had to stop without another live attempt. |
| `att_9e2e0562-f7ce-4d12-bce8-136f88ded9be` | Final fixture sidecar metadata: `sessions/1907971.json`, regular, mode 0644, 352 bytes, SHA-256 `f1fbd8a2629838cf2f244ff72b5859b1a5b1141d03c2d17e1990ed3e9fe68fff`. Launcher `osPid` was 1907930. |
| `att_f6acfc37-6ad2-4bfc-80c4-67cb5b6189e6` | The parent cannot proceed under the discarded launcher-PID predicate. |
| `att_3a08e484-b2b9-48c8-915f-904610eaa3d0` | Mike made `0.1.9` the sole base and integration branch for 0.1 work and preserved this card as post-merge contract, seal, and live-smoke custody. |
| `att_db09d91a-e208-4806-acd2-700088124228` | The first linked review requested four changes: per-leg phase topology, exact retained evidence serialization, the `0.1.9` branch name, and a same-path predicate tie-break. |
| `dr_5fd346df-75ab-4a1a-a78c-54de593fec12` | Mike authorized one bounded contract-and-recon amendment for those four findings, a new exact seal, and one fresh linked successor review. |
| `att_daa01a05-41c1-4e41-995b-7e5db6afc63c` | The successor review accepted F1, F3, and F4; it found F5's evidence-sink/cardinality contradiction and F6's undecidable absent-path output. |
| `dr_fb80acd4-8634-47be-a9ca-b576b43412b4` | Mike authorized one further bounded contract-and-recon amendment for F5-F6, a new seal, and one fresh linked review. |
| `att_af1b4ab8-55d6-4f74-b5b4-1c753668d05b` | The final review accepted F1-F6 and found F7: snapshot enumeration, metadata, open, read, disappearance, and type-change failures had no representable outcome. |
| `dr_7262873b-27b3-4d35-8a15-15bcd7e277e1` | Mike authorized one bounded contract-and-recon amendment for F7, a new seal, and one fresh linked review. |
| Parent commit `5f4341130419c4bae21bdd6c2278185dcd0f89a5` | Frozen execution-start observability implementation. Five files, 1,375 added lines. This contract does not modify it. |
| Product assignment `asg_17a50f66-c32d-42f2-aba5-dd39e072203e` | Frozen original base-synchronization product lane. This contract does not resume it. |

## Historical source and current product-law evidence

- Authorized implementation branch: `origin/0.1.9`. Historical source read:
  `be61cfc98df6b18c0cc280adeca42cba3fbf14b5`.
- `scripts/feature_smoke.exs` blob:
  `b2a50cafd2fc69c9db7a766be72b25b7500874c2`.
- `lib/tightbeam/homes.ex` blob:
  `682331d702871b191382107fec40550f40f1b634`.
- `docs/SMOKE.md` blob:
  `729384db77bc506ccc7a3ae46a58eadea457cea3`.
- Reviewed base-synchronization successor:
  `base-synchronization-gate-v2.md`, SHA-256
  `16cb6348093d25bc46af05121b087eb8dd3663c98f510cca4895a40106dc4ceb`.
  AC-56 requires the live two-real-harness smoke when credentials work.
- Parent implementation report `art_12ff3fbc`, SHA-256
  `4a975661fd82f201998b8038169fb58fce9439cd4b35c3214c113b164361883f`.
  It records the Claude sidecar and Codex plugin-cache exact-home blockers.
- `AGENTS.md` requires the full fresh real Claude-plus-Codex feature-smoke matrix for an
  adapter-seam lane. It also requires a baseline and post-change repository gate.
- `Homes` owns a bounded projection and preserves harness-owned session state. A fixture
  validator may classify a proven runtime delta; it does not change `Homes` ownership.
- Current `feature_smoke` captures a spawned session key, derives its local workdir
  without DB access, validates the projected home, wakes once, observes the turn
  boundary, proves durable redelivery, and retires in an `after` block.

Before this post-review amendment, the owned specs branch fetched `origin/main` and
fast-forwarded cleanly. Its parent and the then-current remote `main` were both
`b20194fe464f5792788bb5b7033245e4d0696889`. The pre-amendment producer commit was
`0d422d33632eb13e63a5129f7f34890628cb06a6`; no source repository was edited or run.

Before the F5-F6 amendment, remote specs `main` had advanced to
`9ddcb07a779ee9f73285f5bfa54898651e781f13`. The owned branch fetched it. The
fast-forward-only gate refused because reviewed commit
`6881ff5af10ea32635ccc7c04499a1eb0429361a` and current `main` diverged from merge base
`b20194fe464f5792788bb5b7033245e4d0696889`. Merge commit
`a3b1e249250b14daafe40e217f59e0e047144411` then preserved both parents without a
conflict. Its second parent is exact current `main`; its first parent preserves the
reviewed artifact. No contract or recon edit preceded this sync.

Before the F7 amendment, the owned branch fetched `origin/main` again. Remote `main`
remained exact `9ddcb07a779ee9f73285f5bfa54898651e781f13`, which is already an ancestor of
reviewed commit `aad893964b0bbf08c99dfec54f64801611e85eca` through merge
`a3b1e249250b14daafe40e217f59e0e047144411`. No merge or contract edit was required
to synchronize the base.

## Preserved final-fixture evidence

Fixture:
`/home/mike/.tightbeam/work/8f6aa9af3615/feature-smoke-fixture-20260814-0256-mKPKsW`.

The stopped fixture retains `.claude.json`, the bounded backup, and an empty
mode-0700 `sessions` directory. Harness retirement removed the sidecar before this
recon. The terminal attest, smoke output, and note-cap specimen retain only its path,
type, mode, size, and SHA-256. The contract therefore does not claim that the deleted
bytes had the normative schema.

The final mismatch proves this negative fact:

`Tightbeam launcher osPid != Claude sidecar filename stem`

It does not prove a positive process relationship.

## Read-only sidecar schema observation

At 2026-08-14T03:23:27Z, the same host retained two current Claude Code 2.1.232
sidecars:

| File | Mode | Size | SHA-256 |
| --- | --- | --- | --- |
| `sessions/568804.json` | 0644 | 290 | `b7810df98c7b9245a1d387e6f80a1a616504ff92086f97eef4196b7d15f724d3` |
| `sessions/1553662.json` | 0644 | 291 | `3b03092b51e3656f48fcd0d9ee20a68f400b1a9f11d1933446f47885c969bb83` |

No file was changed. Recon decoded only schema and predicate results. Both files had
the exact member set `pid`, `sessionId`, `cwd`, `startedAt`, `procStart`, `version`,
`peerProtocol`, `kind`, `entrypoint`, `name`, and `nameSource`.

Both observations satisfied:

- internal positive integer `pid` equals the canonical numeric filename stem;
- lowercase canonical UUID `sessionId`;
- absolute Tightbeam workdir-shaped `cwd`;
- 13-digit integer `startedAt`;
- positive decimal-string `procStart`;
- SemVer `version`;
- integer `peerProtocol=1`;
- `kind=interactive`;
- `entrypoint=sdk-ts`;
- nonempty name;
- `nameSource=derived`.

Installed Claude Code package version: 2.1.232. Installed binary SHA-256:
`61d23f8749136907d586d5b11831ea8a5234d4c1dea40a5e55c33b52e204c6d1`.

One observed file had filesystem mtime 262 milliseconds before its JSON `startedAt`.
The contract therefore rejects mtime as freshness authority and uses an explicit
spawn-to-snapshot epoch bracket.

These live samples support a future normative schema. They do not retroactively
describe the deleted final-fixture bytes. The future smoke decides from its own bytes.

## Surrendered diff evidence

The predecessor worktree remains dirty only in `scripts/feature_smoke.exs`. Its diff
has 344 added and 14 removed lines; diff SHA-256
`575785cf034ce370187e7d1d21337dff2a75cf0ca85d3f2f519b3f2faf545c5c`.

Useful evidence in that diff:

- whole-set validation is necessary to enforce cardinality and nesting;
- pre-spawn, pre-wake, and post-turn seams exist in one file;
- `lstat`, mode, size, SHA-256, and JSON class are mechanically observable;
- deterministic table cases fit one-file custody;
- launcher `harnessProcesses/osPid` equality is the failed assumption and must leave.

The diff has no commit, verified verdict, or review. It is evidence, not authority.

## Design rulings

### D-01 — Sidecar self-binding replaces launcher binding

The accepted binding is the conjunction of:

1. canonical numeric filename;
2. internal JSON `pid` equality with that filename;
3. exact expected Tightbeam session workdir in `cwd`;
4. sidecar `startedAt` inside the spawn-to-snapshot interval;
5. exact schema and constant fields;
6. one sidecar and cross-phase sidecar identity continuity.

Each component is observable from fixture material. No component assigns a cognitive
meaning to a launcher process.

### D-02 — Whole-set validation, not a prefix allow list

A prefix allow list would admit nesting, duplicates, wrong types, and unrelated names.
The validator evaluates the complete delta and one exact five-path Claude set.

### D-03 — Lifecycle events, not time thresholds

The validator keys on native reconcile completion, spawn-and-tune return, first-wake
dispatch, observed turn boundary, and cleanup. Run-start occurs once. Pre-spawn,
pre-wake, post-turn, and cleanup occur separately for one Claude leg and one Codex
leg. The Claude leg runs first and finishes cleanup before the Codex leg starts. A leg
never reads the other harness's home. Epoch values only bracket freshness; they do not
decide whether a lifecycle event occurred.

### D-04 — Content-free, mechanically replayable evidence

The validator may decode bytes to decide. It exclusive-creates one retained mode-0600
JSONL file under the fixture base. A passing matrix writes exactly seven synced,
LF-terminated records: one run-start record and pre-spawn, pre-wake, and post-turn
records for each harness leg. Each record uses the contract's exact key order, entry
shape, 29-check order, result, cause, and phase-specific applicability. Durable
evidence contains metadata, hashes, and predicate outcomes, not decoded JSON values or
observed bytes. This preserves the earlier content boundary while making a pass or
validator refusal mechanically replayable. If evidence append or sync itself fails,
the deterministic console `FX_EVIDENCE` line is the sole guaranteed evidence. The
fixture neither retries nor claims that the current JSONL record is complete or durable.
If runtime snapshot acquisition fails, one `FX_SNAPSHOT` record carries the captured
partial entry set, null unavailable fields, and failed `snapshot_acquired` check. It
records no operating-system error text and starts no retry or second snapshot.

### D-05 — Codex remains outside the exception

The known Codex plugin-cache path is not part of the Class 12 sidecar ruling. A future
repeat is a new exact blocker, not a reason to widen this contract.

### D-06 — Backup identity is phase-local

The backup ruling requires exactly one bounded backup at each admitted phase. It does
not require the same filename across phases. A backup may rotate between pre-wake and
post-turn when each observed name, type, mode, JSON syntax, and freshness predicate
passes independently.

### D-07 — First-review closure is bounded to F1-F4

The amendment closes only the four findings in
`att_db09d91a-e208-4806-acd2-700088124228`:

1. F1: C-01 now gives each harness its own baseline, pre-wake, post-turn, and cleanup
   observations. It forbids cross-harness home validation.
2. F2: C-10 now fixes the evidence path, creation mode, record cardinality, byte
   framing, field order and semantics, check order, pass cause, refusal truncation, and
   retention boundary.
3. F3: AS-01 and C-11 name `origin/0.1.9`; the old commit remains historical evidence.
4. F4: For path-specific categories, C-09 selects a failure by error category, raw
   relative-path bytes, then the fixed C-10 predicate order. The refusal includes the
   mapped clause.

No other admission surface or implementation custody changed.

### D-08 — Successor-review closure is bounded to F5-F6

The amendment closes only the two findings in
`att_daa01a05-41c1-4e41-995b-7e5db6afc63c`:

1. F5: C-10 exempts append and sync failures from the complete-record cardinality
   promise. The console `FX_EVIDENCE` line is the only guaranteed evidence. The
   fixture makes no completeness or durability claim for that current record and adds
   no retry or fallback sink.
2. F6: C-09 makes `FX_PATH_SET` a set-level result with `path=-`. The validator does
   not construct a missing-path candidate or sort observed paths for that category.

I-12 and AC-34 now carry the F5 exception. C-02 examples and AC-06, AC-16, AC-19, and
AC-35 carry the F6 output. No other admission surface or implementation custody changed.

### D-09 — Final-review closure is bounded to F7

The amendment closes only finding F7 in
`att_af1b4ab8-55d6-4f74-b5b4-1c753668d05b`:

1. Terms and I-03 distinguish a successful complete runtime delta from one failed
   snapshot attempt.
2. C-08 defines one non-retrying raw-byte-ordered walk and maps projected-home
   enumeration or path-specific metadata, open, type-stability, and read failure to
   `FX_SNAPSHOT`.
3. C-09 orders `FX_SNAPSHOT` before baseline and path-set validation and fixes
   `path=-` only for projected-home enumeration failure.
4. C-10 adds `snapshot_acquired` to the fixed check order and permits null metadata or
   hash fields only where the single attempt did not capture them.
5. AC-36 through AC-40 cover enumeration, `lstat`, open, read, and type-change cases.

The amendment adds no retry, fallback reader, second snapshot, new evidence file,
admitted runtime path, implementation file, fixture attempt, or live authority.

## Declined alternatives

| Alternative | Decision |
| --- | --- |
| Compare filename with `harness_processes.osPid` | Declined. Real fixture disproved equality. |
| Infer the represented process from PID proximity or process-tree position | Declined. This assigns meaning without an authoritative row and hardcodes topology. |
| Require live `/proc/<pid>` ownership | Declined. It hardcodes Linux topology and creates a liveness race. |
| Use file mtime or a grace duration | Declined. Mtime disagreed with `startedAt` in one real sample; a duration would detect a proxy. |
| Admit `sessions/**` by prefix | Declined. It admits nesting, wrong names, multiple files, and wrong types. |
| Delete or preseed `sessions` | Declined. It destroys or manufactures harness state and violates the one-shot evidence boundary. |
| Persist decoded JSON values | Declined. Predicate booleans and hashes prove the contract without carrying runtime contents. |
| Use console output or an unspecified report as evidence | Declined. It does not fix destination, cardinality, framing, pass cause, or cleanup retention. |
| Retry a failed evidence append or use a fallback sink | Declined. It adds a second mechanism and cannot prove that the original sink is durable. The deterministic console refusal is sufficient. |
| Retry a failed snapshot operation or use a fallback reader | Declined. It changes the observation after failure and makes the one-shot result depend on another filesystem race. |
| Take a second runtime snapshot after acquisition failure | Declined. It can observe a different path set and hides the first acquisition failure. |
| Validate both harness homes in one shared phase | Declined. It makes the sequential lifecycle and failure boundary undecidable. |
| Use a wildcard 0.1 implementation-branch placeholder | Declined. Mike designated `origin/0.1.9` as the sole 0.1 branch. |
| Leave same-path predicate order implicit | Declined. Error category and raw-path order alone do not decide which clause wins on one multiply-invalid entry. |
| Sort missing and extra path candidates for `FX_PATH_SET` | Declined. A missing expected path is not an observed relative path. The set-level result emits `path=-`. |
| Admit the Codex plugin cache | Declined. No ruling authorizes that separate surface. |
| Delete the exact-home smoke assertion | Declined. Reviewed product law and repository policy require the live two-harness proof. |
| Accept permanent smoke failure | Declined. It leaves frozen parent work unable to reach its required live gate. |
| Require one backup filename across both phases | Declined. No ruling or observation establishes cross-phase backup identity; exact phase-local cardinality and freshness provide the required rail. |

Subtraction result: ADD the one narrow fixture validator. DELETE loses because it
removes required exact-home and two-harness evidence. ACCEPT loses because it leaves
the required smoke permanently blocked. The enforcement rung is a one-file code rail
with deterministic cases and one real fresh matrix.

## Clause map

| Contract clause | Upstream source | Future implementation and verification |
| --- | --- | --- |
| Goal, I-04, C-03 | `att_d0b6affe`, `att_9e2e0562`, `att_f6acfc37` | Remove launcher-PID input from admission; case proves filename/internal-PID equality without launcher read. |
| C-01 | `att_32e44600`; current `feature_smoke` call order; first-review F1 | Validate run-start once; validate separate Claude and Codex pre-spawn, pre-wake, post-turn, and cleanup phases without cross-home reads. |
| C-02 | `att_15121266`; final fixture metadata; preserved stopped fixture tree | Exact five-path whole-set predicate plus negative nesting/type/mode cases. |
| C-04 | Two read-only Claude 2.1.232 sidecars; installed binary | Exact eleven-member schema and semantic cases. |
| C-05 | Backup ruling; sidecar samples; mtime contradiction | Spawn-to-snapshot interval tests; no mtime or duration decision. |
| C-06 | `att_3db588ec`; `att_d0b6affe`; one-shot fixture history | Exact phase-local backup cardinality, cross-phase sidecar identity, and no-reuse cases. |
| C-07 | Parent `att_cbdc7419`; assignment scope | Empty Codex delta and a plugin-cache negative case. |
| C-08-C-09 | Engineering tenet to report dirt; law wisdom 4-5; first-review F4; successor F6; final-review F7 | Emit set-level `FX_PATH_SET` with `path=-`; emit ordered `FX_SNAPSHOT` for the single acquisition attempt; otherwise select first failure by category, observed raw path, then fixed predicate order. |
| C-10 | `att_15121266`; assignment evidence boundary; first-review F2; successor F5; final-review F7 | Exact retained mode-0600 JSONL path, seven-record passing cardinality, validator-refusal truncation, 29 fixed checks, hashes and booleans, null uncaptured snapshot fields, and no decoded values, bytes, or OS error text. |
| C-11 | Assignment custody; Mike branch correction; first-review F3 | One-file diff from synchronized `origin/0.1.9` and custody check. |
| C-12 | `att_d694b965`; `spec-handoff`; `AGENTS.md` live-smoke law | Reviewed hash, explicit release, deterministic gates, one fresh matrix, linked exact-commit review. |
| AC-29 | Reviewed base-sync AC-56; `AGENTS.md`; first-review F1-F2 | One sequential Claude-plus-Codex matrix after repository gates, with separate leg observations and seven retained records. |
| AC-34-AC-35 | Successor-review F5-F6; `dr_fb80acd4` | Console-only sink-failure evidence and deterministic `path=-` for missing-plus-extra set refusal. |
| AC-36-AC-40 | Final-review F7; `dr_7262873b` | Deterministic single-attempt snapshot refusal for enumeration, metadata, open, read, and type-change failure. |
| I-11, AC-31 | Facts 373/384/387/390; parent and product cards | Readback proves frozen identifiers unchanged before handoff. |

Reverse trace check:

- No design element lacks a cited authority or observation.
- No contract clause lacks a Given/When/Then example or an acceptance row.
- No acceptance row authorizes source mutation, fixture execution, review, parent work,
  or live mutation on this producer assignment.

## Cold digest

The scheduled 2026-08-14 UTC digest re-read both artifacts from the beginning and
tested each load-bearing clause for a second interpretation.

It removed one unsupported condition: cross-phase backup filename equality. It also
anchored the UUID, `procStart`, and SemVer predicates; removed an unsupported `name`
length/content restriction; defined special-bit mode refusal; separated JSON syntax,
JSON shape, and sidecar-schema errors; made run-start no-reuse and cleanup ownership
explicit; and converted resolved gates out of the open-question category. No blocking
contract question remains.

The digest did not change the five-path set, sidecar self-binding, exact eleven-member
schema, spawn-bracket freshness, sidecar identity continuity, Codex refusal, one-file
custody, one-shot fixture rule, or release sequence.

The 2026-08-29 post-review digest read the complete changes-requested report at
`art_2fb7d6fb`, SHA-256
`c986d5cd8a03eb59104de9b2974a4fdc0a53de7a278c54afa8ede21ed1c72880`, and its remote
report commit `8b99a0f882ce094168fedbcf83c17b3edf765d08`. Mike's
`authorize-bounded-rework-and-successor-review` ruling limited the amendment to F1-F4.
The amendment made phases per-leg, made evidence byte- and record-decidable, replaced
the branch placeholder with `origin/0.1.9`, and completed the first-failure order. It
did not widen the path set, custody, live authority, or one-shot release. A successor
review must decide the new exact hashes.

The successor review read that amended seal at exact commit
`6881ff5af10ea32635ccc7c04499a1eb0429361a`. Its verdict `att_daa01a05` and full report
`art_63218896`, SHA-256
`204fe01ec7c01e2c98d10fea2ef25dbfac221ed374a8f917fb10ff267d9fd458`, accepted F1,
F3, and F4. It found F5 and F6. Mike ruling `dr_fb80acd4` authorized the narrow second
amendment. The digest removed the impossible sink-failure record guarantee and removed
missing-path candidate ordering. It added no retry, fallback sink, admitted path,
implementation file, live authority, or fixture attempt. A fresh review must decide
the new exact hashes.

The final review read exact commit `aad893964b0bbf08c99dfec54f64801611e85eca`.
Verdict `att_af1b4ab8` and report `art_2bb013c0`, SHA-256
`1fe2b651f0857d915dc9f08a56049c8db4147c8c87819047de0f0981c7785eef`, accepted
F1-F6 and found F7. Mike ruling `dr_7262873b` authorized the narrow amendment. The
digest added one representable acquisition refusal and partial content-free evidence.
It added no retry, fallback reader, second observation, path admission, implementation
file, fixture attempt, or live authority. A fresh review must decide the new hashes.

During digest scheduling, the liveness monitor issued three false no-continuation
prods although wake `w_31ff3a98-8ed9-4ae0-844c-994145a6deb6` was scheduled. The exact
specimen receipts are `att_175f30de-6940-423c-bc35-cbd47a00712e`,
`att_d2fb406f-f0bb-4272-b4a2-f84b84b997e0`, and
`att_02748200-3c4d-48ab-b226-f5df031b704f`. This is a substrate incident record, not
contract authority.

## Review target

One fresh linked reviewer should hash both amended artifacts, read the full work item,
all prior reviews and rework rulings, and the cited attests, and decide:

1. whether the normative schema is supported without claiming deleted final bytes;
2. whether each admitted path, type, mode, cardinality, and phase is exact;
3. whether any clause reintroduces launcher inference or topology;
4. whether error ordering and evidence are deterministic and content-free;
5. whether one-file custody and no-reuse remain intact;
6. whether the Codex boundary remains a refusal;
7. whether each implementation element traces back to the contract;
8. whether F1-F4 remain closed;
9. whether F5-F6 remain closed;
10. whether F7 now gives each acquisition failure one ordered, content-free,
    non-retrying result without introducing another interpretation.

The reviewer records `reviewed-clean` or precise `changes-requested`. The reviewer does
not edit, implement, run a fixture, resume the parent, or mutate facts.
