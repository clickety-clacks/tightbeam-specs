# Feature-smoke Claude session-sidecar contract

Status: REVIEW CANDIDATE. This artifact is not implementation authority until one
fresh linked independent review records `reviewed-clean` for its exact SHA-256 and the
opener explicitly releases the Class 12 block.

Work item: `wi_15f960ac-3083-437a-9979-0f0313b7f474`

Producer assignment: `asg_ee922fe3-3005-406b-af46-82cb4ffa2d10`

Controlling ruling: `att_d0b6affe-af19-44f5-9d6e-ca24292d9743`

Blocked parent: `asg_6f2a530d-19b4-417b-91f8-fafa4e5257cc`, frozen commit
`5f4341130419c4bae21bdd6c2278185dcd0f89a5`

Surrendered predecessor: `asg_0ec88f61-ba03-44d2-bb87-5b92ab04fc8f`, terminal
receipt `att_9e2e0562-f7ce-4d12-bce8-136f88ded9be`

Source line: `origin/0.1.x` at
`be61cfc98df6b18c0cc280adeca42cba3fbf14b5`

## Goal

Define the fixture-only admission contract for the Claude runtime file
`sessions/<positive-numeric>.json` so `scripts/feature_smoke.exs` can preserve its
exact-home proof without equating the file name to Tightbeam's launcher `osPid`.

The contract admits one mechanically verifiable Claude runtime set during one fresh
full Claude-plus-Codex smoke. It leaves each unrelated path subject to the existing
unexpected-path refusal.

## Non-Goals

- This contract does not change source, tests, CI, product behavior, live homes, or
  harness behavior.
- This contract does not establish a relationship between a Claude sidecar PID and a
  Tightbeam `harness_processes.osPid` value.
- This contract does not admit a Codex runtime path.
- This contract does not expand the ruled `.claude.json` or backup surfaces.
- This contract does not authorize fixture creation, smoke execution, review,
  integration, deployment, restart, parent completion, or product work.
- This contract does not authorize a second live fixture after the one future fixture
  is consumed.
- This contract does not make the surrendered uncommitted diff implementation
  authority.
- This contract establishes no agent operating pattern and requires no manual or
  guidance amendment.

## Terms

- **Fresh fixture**: a newly created isolated Tightbeam base that has exactly one user,
  that user is an admin, zero sessions, zero work items, zero turns, copied
  authentication stores, clean identity input, and one native home reconciliation for
  each selected harness. A fixture stops being fresh when either harness process is
  spawned.
- **Projected home**: the harness-and-host directory returned by
  `Tightbeam.Homes.home_path/3` inside the fresh fixture.
- **Owned baseline**: the exact leaf-path set returned by
  `Tightbeam.Homes.owned_entries/1` after native reconciliation.
- **Runtime delta**: the complete recursive path set in a projected home after the
  validator subtracts the owned baseline and the baseline's ancestor directories.
- **Relative runtime path**: the raw filename-byte sequence from the projected home to
  one recursive entry, joined with byte `0x2f`. The set includes directories and does
  not follow symlinks. Admitted names are ASCII and contain no empty, `.` or `..`
  component.
- **Evidence token**: a single-line rendering of a relative runtime path or principal.
  Bytes in `A-Z`, `a-z`, `0-9`, `.`, `_`, `/`, and `-` render literally. Every other
  byte renders as `%HH` with uppercase hexadecimal digits.
- **Spawn interval**: the inclusive wall-clock interval whose start is captured before
  the fixture sends the Claude spawn request and whose end is captured after the
  validator reads the complete runtime-delta metadata and file bytes.
- **Run-start phase**: after fixture gateway connection and before the first credential
  preflight. This phase occurs once for the full Claude-plus-Codex run.
- **Pre-spawn phase**: after native reconciliation and before the fixture sends the
  harness spawn request.
- **Pre-wake phase**: after spawn and deployment tuning return successfully and before
  the fixture sends its first wake.
- **Post-turn phase**: after the fixture observes the wake turn boundary and before it
  writes the durable-redelivery sentinel.
- **Cleanup phase**: the existing `after` block that retires the spawned session and
  removes the fixture sentinel. Cleanup follows validation and is not an admission
  phase.
- **Canonical positive numeric stem**: a nonempty decimal string that matches
  `[1-9][0-9]*`. It contains no sign, prefix, leading zero, exponent, decimal point, or
  whitespace.
- **Permission mode**: the `lstat` mode's permission and special-bit portion. An exact
  mode such as `0644` requires those nine permission bits and requires set-user-ID,
  set-group-ID, and sticky bits to be zero. File type is checked separately.
- **Claude sidecar**: the sole regular file at
  `sessions/<canonical-positive-numeric-stem>.json` in the Claude runtime delta.
- **Sidecar identity**: the tuple `pid`, `sessionId`, `cwd`, `startedAt`, and
  `procStart` decoded from a valid Claude sidecar.
- **Evidence record**: the content-free observation defined by C-10. It records file
  metadata, hashes, predicate outcomes, cause, and principal. It does not record JSON
  member values or file bytes.

## Assumptions

- AS-01. `origin/0.1.x` commit
  `be61cfc98df6b18c0cc280adeca42cba3fbf14b5` is the current maintenance-line source
  read for this contract.
- AS-02. `Tightbeam.Homes.owned_entries/1` designates Tightbeam-owned home leaves. The
  harness owns runtime additions outside that projection, but `feature_smoke` decides
  which additions satisfy this fixture acceptance gate.
- AS-03. The final consumed fixture recorded a Claude sidecar at
  `sessions/1907971.json` as a non-symlink regular mode-0644 file, size 352, SHA-256
  `f1fbd8a2629838cf2f244ff72b5859b1a5b1141d03c2d17e1990ed3e9fe68fff`.
- AS-04. The same final fixture recorded launcher `osPid=1907930`. The unequal values
  prove only that launcher PID equality is false; they do not identify the process
  represented by `1907971`.
- AS-05. Harness cleanup removed the final sidecar after the terminal observation. Its
  instance values are unavailable and this contract makes no retrospective schema
  claim about those deleted bytes.
- AS-06. Read-only samples produced by installed Claude Code 2.1.232 on the same host
  exposed the same eleven JSON member names and types. Each sample bound its internal
  positive integer `pid` to its canonical numeric filename.
- AS-07. `local_workdir_path/2` deterministically derives the spawned Tightbeam
  session's expected local work directory from the fixture base and Tightbeam session
  key.
- AS-08. The Claude sidecar `startedAt` member and backup filename timestamp use Unix
  epoch milliseconds compatible with `System.system_time(:millisecond)`. A future
  observation that falsifies this assumption fails the smoke and returns for ruling.
- AS-09. One future full-parity fixture remains subject to a separate explicit release
  after this exact contract passes review.

## Invariants

- I-01. The admission applies only to the Claude projected home in a fresh fixture.
- I-02. The validator proves the owned baseline before it sends a spawn request.
- I-03. The validator evaluates the complete runtime delta as one set.
- I-04. The validator does not read, compare, or report a Tightbeam launcher `osPid`
  while deciding sidecar admission.
- I-05. The validator derives each decision from paths, `lstat` metadata, captured file
  bytes, the spawned Tightbeam session key, and explicit phase timestamps.
- I-06. The validator admits no runtime delta for Codex.
- I-07. The fixture does not delete, preseed, rename, repair, or synthesize a harness
  runtime path.
- I-08. A fixture that reaches harness spawn is consumed after either pass or refusal.
- I-09. Evidence excludes raw sidecar bytes and decoded JSON member values.
- I-10. Future implementation custody contains only `scripts/feature_smoke.exs`.
- I-11. Parent commit `5f4341130419c4bae21bdd6c2278185dcd0f89a5`, product
  assignment `asg_17a50f66-c32d-42f2-aba5-dd39e072203e`, and facts 373, 384, 387,
  and 390 remain unchanged until a later explicit release.
- I-12. The validator refuses a mismatch without mutating an observed runtime path.
  It records evidence before the existing lifecycle cleanup can remove that path.

## Architecture

The pattern is **fixture runtime sidecar admission**. It applies only to the
`check_local_deployment` group in `scripts/feature_smoke.exs`. It does not apply to
live home reconciliation, credential handling, harness process supervision, product
sessions, or another smoke group.

The implementation uses one validation seam for the runtime delta. That seam validates
both harnesses at pre-spawn, pre-wake, and post-turn. Parallel allow lists are out of
contract.

### C-01 — Phase boundaries

The fixture captures and validates these states in order:

1. In the run-start phase, the selected harness set is exactly Claude and Codex; the
   fixture has exactly one user, that user is an admin, and it has zero sessions, work
   items, and turns.
2. In the pre-spawn phase, each projected home's leaf set equals its owned baseline.
3. In the pre-wake phase, the Claude runtime delta satisfies C-02 through C-06 and the
   Codex runtime delta satisfies C-07.
4. In the post-turn phase, the Claude runtime delta satisfies C-02 through C-06 and
   the Codex runtime delta satisfies C-07.
5. In cleanup, the existing retirement path runs after the final evidence record. The
   validator performs no post-retirement admission check.

Acceptance example: Given a native-reconciled fixture with exact owned baselines, when
Claude spawn and tuning return and no wake has been sent, then the validator labels the
observation `pre-wake` and evaluates it before the wake call.

### C-02 — Complete admitted Claude path set

At pre-wake and post-turn, the Claude runtime delta contains exactly these five paths:

| Path | Type | Permission mode | Additional condition |
| --- | --- | --- | --- |
| `.claude.json` | non-symlink regular file | `0600` | UTF-8 JSON object with no duplicate member name at any object depth |
| `backups` | non-symlink directory | `0755` | direct child of the projected home |
| `backups/.claude.json.backup.<epoch-ms>` | non-symlink regular file | `0600` | sole direct child of `backups`; valid UTF-8 JSON value with no duplicate member name at any object depth; C-05 timestamp |
| `sessions` | non-symlink directory | `0700` | direct child of the projected home |
| `sessions/<positive-numeric>.json` | non-symlink regular file | `0644` | sole direct child of `sessions`; size 1 through 4096 bytes; C-03 through C-06 |

The backup filename suffix contains exactly 13 decimal digits. The validator rejects a
sixth runtime path, a missing listed path, a nested child, a symlink, and a special
filesystem type.

Acceptance example: Given the five listed entries plus `sessions/nested/2.json`, when
the validator evaluates the whole delta, then it refuses with `FX_PATH_SET` and names
the nested relative path without reading it as an admitted sidecar.

### C-03 — Canonical sidecar filename and internal PID binding

The sidecar filename matches
`\Asessions/([1-9][0-9]*)\.json\z`. The JSON `pid` member is an integer greater than
zero. Its base-10 rendering equals the captured filename stem byte for byte.

The validator does not compare either value with Tightbeam launcher state.

Acceptance example: Given `sessions/1907971.json` whose JSON `pid` is integer
`1907971`, when the remaining clauses pass, then C-03 passes without reading
`harness_processes.osPid`.

### C-04 — Exact sidecar JSON schema

The sidecar bytes are valid UTF-8 JSON with one top-level object, no duplicate member
names, and exactly these members:

| Member | Required value contract |
| --- | --- |
| `pid` | positive integer; C-03 equality |
| `sessionId` | lowercase canonical UUID text matching `\A[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\z` |
| `cwd` | string byte-equal to `local_workdir_path(fixture_base, spawned_session_key)` |
| `startedAt` | integer Unix epoch milliseconds; C-05 interval |
| `procStart` | string matching `\A[1-9][0-9]*\z` |
| `version` | string matching `\A(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?\z` |
| `peerProtocol` | integer `1` |
| `kind` | string `interactive` |
| `entrypoint` | string `sdk-ts` |
| `name` | nonempty UTF-8 string |
| `nameSource` | string `derived` |

The validator rejects a missing member, an additional member, a duplicate member, a
wrong JSON type, and a value outside its stated predicate.

Acceptance example: Given a sidecar with the exact eleven members except an additional
`launcherPid`, when the validator evaluates its schema, then it refuses with
`FX_SIDECAR_SCHEMA`.

### C-05 — Bounded freshness provenance

The fixture captures `spawn_started_at` immediately before it sends the Claude spawn
request. The validator captures `snapshot_finished_at` immediately after it reads the
complete runtime-delta metadata and regular-file bytes.

The validator requires `snapshot_finished_at >= spawn_started_at`. It requires both the
backup filename epoch and the sidecar `startedAt` value to lie inside the inclusive
`[spawn_started_at, snapshot_finished_at]` interval.

Filesystem modification time, file birth time, elapsed-duration thresholds, and
launcher start time do not decide freshness.

Acceptance example: Given a schema-valid sidecar whose `startedAt` is one millisecond
before `spawn_started_at`, when the validator evaluates freshness, then it refuses with
`FX_FRESHNESS`.

### C-06 — Cardinality, phase continuity, and no reuse

The pre-wake Claude delta contains one sidecar and one backup. The post-turn Claude
delta contains one sidecar and one backup.

The post-turn sidecar identity equals the pre-wake sidecar identity. The validator
evaluates C-04 again at post-turn; it does not substitute the earlier result.
Members outside the sidecar-identity tuple need not be byte-equal across phases; each
must independently satisfy C-04.

The validator evaluates the post-turn backup name, type, mode, JSON syntax, and C-05
freshness independently. The backup may have a different valid name at post-turn.

The opener may authorize one fresh full-parity fixture after reviewed-clean contract
and implementation evidence. C-01 run-start state makes prior harness use observable.
A refusal after harness spawn consumes that fixture. A later attempt needs a new
ruling.

Acceptance example: Given a passing pre-wake sidecar and a post-turn sidecar with a
different `sessionId`, when the validator compares sidecar identity, then it refuses
with `FX_IDENTITY_DRIFT`.

### C-07 — Codex separation

The Codex runtime delta is empty at pre-wake and post-turn. The Claude exception does
not classify a Codex path.

Acceptance example: Given a Codex runtime delta containing one plugin-cache file, when
the Codex validator runs, then it refuses with `FX_CODEX_RUNTIME_PATH` and does not
classify the file under the Claude contract.

### C-08 — Refusal behavior

The validator refuses the smoke on the first failing ordered check. It does not remove,
rename, rewrite, chmod, preseed, or ignore the observed entry. Cleanup may retire the
spawned session through the existing fixture lifecycle after evidence capture.

Acceptance example: Given a sidecar symlink whose target is a schema-valid JSON file,
when the validator reads `lstat` metadata, then it refuses with `FX_TYPE` before it
opens the target.

### C-09 — Deterministic error mapping

The validator evaluates categories in this order:

1. `FX_PHASE` for a missing or out-of-order phase input.
2. `FX_FIXTURE_STATE` for a run-start harness-selection or fixture-count mismatch.
3. `FX_CLOCK` for an inverted spawn interval.
4. `FX_BASELINE` for a pre-spawn baseline mismatch.
5. `FX_PATH_SET` for Claude path or cardinality mismatch.
6. `FX_CODEX_RUNTIME_PATH` for a nonempty Codex runtime delta.
7. `FX_TYPE` for symlink, wrong type, or special type.
8. `FX_MODE` for a permission-mode mismatch.
9. `FX_SIZE` for a sidecar outside the byte bound.
10. `FX_JSON` for invalid UTF-8, invalid JSON, or duplicate member names.
11. `FX_JSON_SHAPE` when `.claude.json` has a valid JSON top level other than an
    object.
12. `FX_SIDECAR_SCHEMA` for a sidecar member-set or member-type mismatch.
13. `FX_SIDECAR_SEMANTIC` for C-03 or C-04 value mismatch.
14. `FX_FRESHNESS` for C-05 mismatch.
15. `FX_IDENTITY_DRIFT` for C-06 cross-phase mismatch.

Within one category, the validator sorts relative paths by raw byte order. One
refusal line has this shape:

`feature-smoke fixture HOME REFUSED code=<code> harness=<harness-or-all> phase=<phase> principal=<evidence-token> path=<evidence-token-or-dash> clause=<clause-id>`

Acceptance example: Given both a missing `sessions` directory and a wrong-mode
`.claude.json`, when the validator evaluates the delta, then it returns `FX_PATH_SET`
before `FX_MODE` on repeated runs.

### C-10 — Evidence and cleanup boundary

For each observed runtime entry, the fixture records harness, phase, path as an evidence token,
`lstat` type, permission mode, byte size, and SHA-256 for a regular file. It records
these predicate results for the sidecar: exact member set, member types, filename-PID
equality, expected-CWD equality, UUID shape, start-interval membership, `procStart`
shape, SemVer shape, constant-field equality, and cross-phase identity equality.

Each record names the Tightbeam session key as principal after spawn and names
`pre-spawn` before a session exists. Each refusal names its C-clause as cause.

The fixture does not record JSON bytes, decoded member values, credential material,
stdout, or stderr. It records evidence before retirement because harness cleanup may
remove the sidecar. The fixture does not delete the used fixture base; the existing
harness lifecycle may remove its own transient sidecar during retirement.

Acceptance example: Given a sidecar whose `cwd` is wrong, when the validator refuses,
then the evidence says `expected_cwd_equal=false` and omits both the observed and
expected path values.

### C-11 — One-file implementation custody

A future implementation assignment owns only `scripts/feature_smoke.exs`. It starts
from the then-current `origin/0.1.x`, names this reviewed artifact and SHA, and keeps
the existing exact-home proof.

The builder may read the surrendered one-file diff as evidence. The builder derives
behavior from this contract and does not treat the diff as authority.

Acceptance example: Given an implementation proposal that also changes
`lib/tightbeam/homes.ex`, when custody is checked, then implementation stops before an
edit and reports the additional-file requirement to the opener.

### C-12 — Release sequence

The release sequence is:

1. One fresh linked independent reviewer reads the exact contract and recon hashes.
2. The reviewer records `reviewed-clean` or `changes-requested` on a review assignment
   linked to this producer assignment.
3. After `reviewed-clean`, the opener explicitly releases the Class 12 block and opens
   one one-file implementation assignment.
4. The implementer proves deterministic allow and reject cases, format, syntax,
   `git diff --check`, and the repository gate before a live fixture.
5. The opener authorizes one new never-reused full Claude-plus-Codex fixture.
6. The implementer runs the full matrix once and records pass evidence or the exact
   first blocker.
7. A passing implementation returns for one fresh linked independent exact-commit
   review before the parent lane resumes.

Acceptance example: Given a reviewed-clean contract but no opener release, when a
worker proposes a fixture run, then the worker remains blocked and does not create the
fixture.

## Acceptance

The future implementer attaches one deterministic case to each row before live smoke.
The Given/When/Then examples in C-01 through C-12 are part of this acceptance contract.

| ID | Given | When | Then | Trace |
| --- | --- | --- | --- | --- |
| AC-01 | Exactly Claude and Codex are selected; the fixture has one user who is an admin and zero sessions, work items, and turns | Run-start validation runs | The fixture passes once before the first credential preflight | C-01, C-06 |
| AC-02 | A prior spawn left one session row in the base | Run-start validation runs | `FX_FIXTURE_STATE` refuses the reused fixture before credential preflight | C-01, C-06, C-09 |
| AC-03 | Exact Claude and Codex owned baselines | Pre-spawn validation runs | Both baselines pass and no runtime exception is used | C-01, I-02 |
| AC-04 | The exact five-path Claude runtime set | Pre-wake validation runs | The set passes without a launcher PID read | C-02-C-05, I-04 |
| AC-05 | Canonical filename and equal internal `pid` | Sidecar semantics run | Filename-PID binding passes | C-03 |
| AC-06 | `sessions/0123.json` with internal `pid=123` | Whole-set path validation runs | `FX_PATH_SET` refuses the noncanonical name before sidecar semantics | C-02, C-03, C-09 |
| AC-07 | `sessions/123.json` has internal `pid=124` | Sidecar semantics run | `FX_SIDECAR_SEMANTIC` refuses the unequal binding | C-03, C-09 |
| AC-08 | One runtime JSON file contains invalid UTF-8 | JSON validation runs | `FX_JSON` refuses it | C-02, C-04, C-09 |
| AC-09 | One runtime JSON file contains malformed JSON | JSON validation runs | `FX_JSON` refuses it | C-02, C-04, C-09 |
| AC-10 | One runtime JSON object has a duplicate member name | JSON validation runs | `FX_JSON` refuses it | C-02, C-04, C-09 |
| AC-11 | Sidecar has one missing member | Schema validation runs | `FX_SIDECAR_SCHEMA` refuses it | C-04, C-09 |
| AC-12 | Sidecar has one extra member | Schema validation runs | `FX_SIDECAR_SCHEMA` refuses it | C-04, C-09 |
| AC-13 | Sidecar has one member with the wrong JSON type | Schema validation runs | `FX_SIDECAR_SCHEMA` refuses it | C-04, C-09 |
| AC-14 | Sidecar `cwd` differs from the spawned Tightbeam workdir | Semantic validation runs | `FX_SIDECAR_SEMANTIC` refuses it without logging either value | C-04, C-10 |
| AC-15 | Backup timestamp or `startedAt` lies outside the spawn interval | Freshness validation runs | `FX_FRESHNESS` refuses it | C-05 |
| AC-16 | Two sidecars or two backups exist | Whole-set validation runs | `FX_PATH_SET` refuses the set | C-02, C-06 |
| AC-17 | The post-turn backup has a new canonical name and satisfies C-02 and C-05 | Post-turn validation runs | The backup passes without requiring pre-wake filename equality | C-05, C-06 |
| AC-18 | Post-turn sidecar identity differs from pre-wake identity | Continuity validation runs | `FX_IDENTITY_DRIFT` refuses it | C-06 |
| AC-19 | One unexpected Claude nested path exists | Whole-set validation runs | `FX_PATH_SET` refuses it | C-02, C-08 |
| AC-20 | One symlink occupies an admitted name | Metadata validation runs | `FX_TYPE` refuses it without following the link | C-02, C-08 |
| AC-21 | `.claude.json` has mode `0644` | Mode validation runs | `FX_MODE` refuses it | C-02, C-09 |
| AC-22 | Sidecar has 4097 bytes | Size validation runs | `FX_SIZE` refuses it before JSON decoding | C-02, C-09 |
| AC-23 | `.claude.json` contains the valid JSON value `[]` | JSON-shape validation runs | `FX_JSON_SHAPE` refuses it | C-02, C-09 |
| AC-24 | Codex writes one runtime path | Codex validation runs | `FX_CODEX_RUNTIME_PATH` refuses it | C-07 |
| AC-25 | One mismatch satisfies more than one error category | The case runs repeatedly | Each run returns the same first code, phase, and path evidence token | C-09 |
| AC-26 | One valid sidecar observation | Evidence is written | Metadata, hashes, booleans, cause, and principal are present; JSON values and bytes are absent | C-10 |
| AC-27 | One fixture reaches harness spawn and refuses | Cleanup completes | The fixture base remains, no observed runtime path is fixture-mutated before lifecycle cleanup, and no second fixture starts | C-06, C-08, C-10 |
| AC-28 | Reviewed-clean contract and explicit release exist | One-file implementation begins | Only `scripts/feature_smoke.exs` changes from current `origin/0.1.x` | C-11-C-12 |
| AC-29 | Deterministic cases and repository gates pass | One fresh full matrix runs | Claude and Codex credential preflights pass; both full legs complete; Claude passes both sidecar phases; Codex has empty deltas | C-01-C-12 |
| AC-30 | The full matrix encounters a new runtime path or schema | The validator refuses | The implementer files the exact blocker and does not retry | C-06-C-10, C-12 |
| AC-31 | Parent commit, product assignment, and facts are read after this contract | Contract production ends | Their identifiers and state match I-11 | I-11 |

## Open Questions

None. The contract is ready for independent review.

The following resolved boundaries remain gates, not open questions:

- The contract does not infer the schema of the deleted final-fixture bytes. A future
  fixture validates its own captured bytes and refuses a mismatch.
- A future Codex runtime path, including the previously observed plugin-cache path,
  blocks parent verification under C-07. This contract does not admit or repair it.
- Implementation and fixture execution remain blocked until one linked independent
  review records `reviewed-clean` for the exact artifact hashes and the opener issues
  an explicit release.
