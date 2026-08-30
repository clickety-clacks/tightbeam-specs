# Feature-smoke Claude sidecar and Codex runtime contract

Status: REVIEW CANDIDATE. This artifact is not implementation authority until one
fresh linked independent review records `reviewed-clean` for its exact SHA-256 and the
opener explicitly releases the Class 12 block.

Work item: `wi_15f960ac-3083-437a-9979-0f0313b7f474`

Producer assignment: `asg_ee922fe3-3005-406b-af46-82cb4ffa2d10`

Controlling ruling: `att_d0b6affe-af19-44f5-9d6e-ca24292d9743`

Creation-mode amendment ruling: `dr_16de6d11-492c-4ec4-aaa2-6cb1a03d4d7d`,
`contract-amendment`

Codex-runtime amendment ruling: `dr_1c06d9c9-df96-4fb7-b49e-0752a9d9fe54`,
`amend-after-recon`

Named Claude-waiver authority: correction wake
`s_1e05ddc2-e04f-47f3-8273-2964c38719c8`, the governing rationale on
`dr_7383a755-820d-4f1e-b882-4f16b08a103f`, and waiver receipt
`att_8548c286-d318-4293-9632-670af92b79fc`

Blocked parent: `asg_6f2a530d-19b4-417b-91f8-fafa4e5257cc`, frozen commit
`5f4341130419c4bae21bdd6c2278185dcd0f89a5`

Surrendered predecessor: `asg_0ec88f61-ba03-44d2-bb87-5b92ab04fc8f`, terminal
receipt `att_9e2e0562-f7ce-4d12-bce8-136f88ded9be`

Authorized implementation branch: `origin/0.1.9`

Historical source read: `be61cfc98df6b18c0cc280adeca42cba3fbf14b5`

## Goal

Define the fixture-only admission contract for the Claude runtime file
`sessions/<positive-numeric>.json` and the Codex runtime image so
`scripts/feature_smoke.exs` can preserve its exact-home proof without equating the
Claude file name to Tightbeam's launcher `osPid`.

The contract admits one mechanically verifiable Claude runtime set and one exact
normalized Codex runtime manifest during one newly released fresh smoke. It leaves
each path outside those two sets subject to deterministic unexpected-path refusal.

## Non-Goals

- This contract does not change source, tests, CI, product behavior, live homes, or
  harness behavior.
- This contract does not establish a relationship between a Claude sidecar PID and a
  Tightbeam `harness_processes.osPid` value.
- This contract does not admit a Codex path outside the exact C-07 normalized
  manifest.
- This contract does not assign content semantics to a Codex runtime file. It records
  content hashes and decides path, nesting, type, mode, cardinality, dynamic-name,
  freshness, size, and cross-phase identity predicates.
- This contract does not expand the ruled `.claude.json` or backup surfaces.
- This contract does not authorize fixture creation, smoke execution, review,
  integration, deployment, restart, parent completion, or product work.
- This contract does not authorize another live fixture after a released fixture is
  consumed.
- This contract does not make the surrendered uncommitted diff implementation
  authority.
- This contract establishes no agent operating pattern and requires no manual or
  guidance amendment.

## Terms

- **Fresh fixture**: a newly created isolated Tightbeam base that has exactly one user,
  that user is an admin, zero sessions, zero work items, zero turns, copied
  authentication stores, clean identity input, and one native home reconciliation for
  each selected harness. A released fixture stops being fresh when the invocation
  successfully creates its C-10 evidence file or spawns a harness process, whichever
  occurs first.
- **Projected home**: the harness-and-host directory returned by
  `Tightbeam.Homes.home_path/3` inside the fresh fixture.
- **Owned baseline**: the exact leaf-path set returned by
  `Tightbeam.Homes.owned_entries/1` after native reconciliation.
- **Runtime snapshot attempt**: one non-retrying filesystem walk for one projected-home
  phase. It returns either the complete observed paths, metadata, and required bytes or
  one acquisition failure under C-08.
- **Runtime delta**: the complete recursive path set produced by a successful runtime
  snapshot attempt after the validator subtracts the owned baseline and the baseline's
  ancestor directories.
- **Relative runtime path**: the raw filename-byte sequence from the projected home to
  one recursive entry, joined with byte `0x2f`. The set includes directories and does
  not follow symlinks. Admitted names are ASCII and contain no empty, `.` or `..`
  component.
- **Evidence token**: a single-line rendering of a relative runtime path or principal.
  Bytes in `A-Z`, `a-z`, `0-9`, `.`, `_`, `/`, and `-` render literally. Every other
  byte renders as `%HH` with uppercase hexadecimal digits.
- **Harness leg**: one sequential `check_local_deployment` execution for exactly one
  harness. The fixture completes that leg's cleanup before it starts the other leg.
  Without the active named Claude waiver, the full matrix runs exactly one Claude leg
  first and exactly one Codex leg second. With the active named Claude waiver, the
  matrix runs exactly one Codex leg and no Claude leg. A leg does not read the other
  harness's home.
- **Claude waiver observation**: the one scorecard row returned by
  `Tightbeam.ClientE2E.preflight("claude", fixture_base)` after C-10 establishes the
  evidence writer and immediately before run-start validation when the selected set is
  exactly Codex and `TIGHTBEAM_SMOKE_CLAUDE_WAIVER` has the exact named-waiver value.
  The row is a rejected-credential observation only when `step` is exact
  string `P-claude`, `status` is atom `:fail`, and `note` begins with exact ASCII bytes
  `credential rejected: `. A row with `status=:pass` is a live-credential observation.
  Another row is an unknown-credential observation. The fixture retains the row in
  memory through the next run-start action and does not record its `note`.
- **Active named Claude waiver**: exact value
  `dr_7383a755-820d-4f1e-b882-4f16b08a103f`, selected through
  `TIGHTBEAM_SMOKE_CLAUDE_WAIVER`, together with a rejected-credential Claude waiver
  observation from the same invocation. A live-credential or unknown-credential
  observation makes the waiver inactive. The observation is authoritative for that
  invocation because run-start consumes it in the next admission action. A later
  invocation repeats the observation. Another selected value or an absent value on a
  Codex-only run makes the fixture input invalid.
- **Spawn interval**: the inclusive wall-clock interval whose start is captured before
  the fixture sends the current leg's spawn request and whose end is captured after
  that leg's single runtime snapshot attempt returns success or failure.
- **Run-start phase**: after fixture gateway connection and C-10 evidence-writer setup.
  For a Codex-only candidate, it follows the same-invocation Claude waiver observation.
  It precedes the selected harness leg's credential preflight. This phase occurs once
  for the selected full or named-waiver matrix.
- **Pre-spawn phase**: the per-leg phase after native reconciliation of that harness's
  projected home and before the fixture sends that leg's spawn request.
- **Pre-wake phase**: the per-leg phase after that leg's spawn and deployment tuning
  return successfully and before the fixture sends that leg's first wake.
- **Post-turn phase**: the per-leg phase after the fixture observes that leg's wake turn
  boundary and before it writes that leg's durable-redelivery sentinel.
- **Cleanup phase**: the per-leg existing `after` block that retires that leg's spawned
  session and removes its fixture sentinel. Cleanup follows that leg's validation and
  is not an admission phase.
- **Canonical positive numeric stem**: a nonempty decimal string that matches
  `[1-9][0-9]*`. It contains no sign, prefix, leading zero, exponent, decimal point, or
  whitespace.
- **Permission mode**: the OTP file-information mode's permission and special-bit
  portion. An exact mode such as `0644` requires those nine permission bits and
  requires set-user-ID, set-group-ID, and sticky bits to be zero. File type is checked
  separately.
- **Regular-object identity**: the three-integer tuple `major_device`, `minor_device`,
  and `inode` returned in OTP file information. The validator compares this tuple only
  while one file handle remains open. It does not record the integers in evidence.
- **Feature-smoke launch envelope**: a new Gibson zsh subshell that sets its process
  umask to exact octal `0077` and then replaces itself with the existing Mix
  invocation. The exact live form is
  `(umask 077 && exec mix run --no-start scripts/feature_smoke.exs)`. The parent shell
  exports every required live-run environment variable before it starts this envelope.
  The `--no-start` Mix client reads the existing fixture gateway's `gateway.json` and
  sends requests to that gateway over HTTP. No fixture code reads or changes the
  process umask.
- **Gateway process boundary**: the Tightbeam gateway process that is already serving
  the fixture before the feature-smoke launch envelope starts. The gateway is not a
  descendant of the envelope's zsh or Mix process. It receives spawn requests over
  HTTP and creates the Claude and Codex harness processes. Those harness processes
  inherit gateway process state, not the later feature-smoke client's umask.
- **Effective creation mode**: the permission bits assigned when the kernel creates an
  inode. For the evidence file, OTP 28.5 requests `0666` and the inherited exact umask
  `0077` removes group and other bits, so the effective creation mode is exact `0600`.
  This term does not mean that OTP requests mode `0600`.
- **Claude sidecar**: the sole regular file at
  `sessions/<canonical-positive-numeric-stem>.json` in the Claude runtime delta.
- **Normalized Codex manifest**: the C-07 canonical sequence of Codex runtime-delta
  path, type, and mode tuples after the validator validates and substitutes the four
  dynamic-name families. The sequence preserves one tuple per observed entry,
  including duplicate normalized shell-snapshot tuples.
- **Sidecar identity**: the tuple `pid`, `sessionId`, `cwd`, `startedAt`, and
  `procStart` decoded from a valid Claude sidecar.
- **Evidence file**: the non-symlink regular mode-0600 file
  `<fixture-base>/feature-smoke-home-evidence.jsonl`. The launch envelope and the
  fixture's exclusive OTP open create it with effective mode `0600` before run-start
  validation. The fixture retains the same open object with the consumed fixture base
  through cleanup. A preexisting path refuses the fixture before credential preflight.
- **Evidence record**: one UTF-8 JSON object and one trailing LF byte in the evidence
  file, serialized exactly as C-10 defines. It records captured file metadata, hashes,
  predicate outcomes, result, cause, and principal. A C-08 acquisition refusal records
  the bounded partial entry set that C-10 defines. It does not record a decoded JSON
  member value, observed file bytes, or operating-system error text.

## Assumptions

- AS-01. `origin/0.1.9` is the authorized implementation branch for 0.1 maintenance.
  Commit `be61cfc98df6b18c0cc280adeca42cba3fbf14b5` is the historical source read that
  informed this contract. A future implementer synchronizes the then-current
  `origin/0.1.9` before editing and confirms that each cited seam remains present.
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
- AS-09. One future fresh fixture remains subject to a separate explicit release after
  this exact contract passes review. The release names either the full two-leg matrix
  or the Codex-only matrix under the active named Claude waiver.
- AS-10. The authorized Gibson runtime uses Unix OTP 28.5. Its documented
  `:file.read_link_info/1` and `:file.read_file_info/1` results expose integer
  `major_device`, `minor_device`, and `inode` fields for a regular file, and the latter
  function accepts an open raw file handle. A future implementer confirms this seam on
  the synchronized implementation base before editing. A mismatch returns for ruling.
- AS-11. On the authorized Gibson runtime, Unix OTP 28.5 issues create mode `0666` for
  the documented exclusive raw file open in C-10, and the kernel applies the inherited
  process umask before the new inode becomes observable. The implementer confirms both
  facts on the synchronized base with the C-12 trace gate. A mismatch returns for
  ruling.
- AS-12. Exact product commit `08e55de896106aa7fcc2ea7f60f1357e5d6cf772`, blob
  `6d9e236a34d99f710d330af0b0dc794063565709`, documents the feature-smoke command as
  `mix run --no-start`, reads `<fixture-base>/gateway.json`, and sends the `spawn`
  request to `http://127.0.0.1:<gateway-port>/agent/dispatch` through `curl`. A
  nonzero `curl` result calls the fixture failure path. A future implementer confirms
  these seams on the synchronized implementation base before editing. A mismatch
  returns for ruling.
- AS-13. Mike's correction wake
  `s_1e05ddc2-e04f-47f3-8273-2964c38719c8` makes the rationale on
  `dr_7383a755-820d-4f1e-b882-4f16b08a103f` controlling. Receipt
  `att_8548c286-d318-4293-9632-670af92b79fc` records the named Claude waiver and its
  expiry. The consumed Codex-only run used exact product commit
  `c6b6632788f06ea8c7e64e6e08a1a635e07f01f4`. It retained three-record evidence
  `art_85f430fe`, SHA-256
  `d92dcbc0577b96a19a87de67db681a31bd94673f5e5944b03bec15c7146d7d2f`, and report
  `art_424f3eff`, SHA-256
  `0593f4c8230d6bafd7c7cbac5db974bdc2af57f831ec76d688b133e502a1961c`.
- AS-14. The retained Codex pre-wake record contains 300 entries: 113 directories, 183
  regular files, and four symlinks. Its mode counts are two `0600`, 181 `0644`, one
  `0700`, 112 `0755`, and four `0777`. Regular-file bytes total 31,826,506; the largest
  regular file is 7,330,920 bytes. C-07 rounds those two observed maxima upward to the
  next binary-megabyte bounds, 32 MiB total and 8 MiB per regular file. A later
  observation that does not satisfy the exact normalized manifest or either bound
  refuses and returns for a new ruling; it does not widen this contract.
- AS-15. Current `origin/0.1.9` commit
  `2e918768556ef16a4412f9e0844bb388b6fb1051`, `lib/tightbeam/client_e2e.ex` blob
  `402c822cfdc71b10d04a85f8cf076a57c0894f5d`, maps a harness credential callback's
  `:live` result to a passing preflight row, `{:dead, reason}` to a failing row whose
  note begins `credential rejected: `, and `{:unknown, reason}` to an incomplete row.
  A future implementer confirms that seam on the synchronized implementation base. A
  mismatch returns for ruling.

## Invariants

- I-01. The admission applies only to the current harness leg's projected home in a
  fresh fixture. C-02 decides Claude paths. C-07 decides Codex paths.
- I-02. The validator proves the owned baseline before it sends a spawn request.
- I-03. After a runtime snapshot succeeds, the validator evaluates the complete runtime
  delta as one set. C-08 decides the result when acquisition fails.
- I-04. The validator does not read, compare, or report a Tightbeam launcher `osPid`
  while deciding sidecar admission.
- I-05. After a runtime snapshot succeeds, the validator derives each admission
  decision from paths, initial and final `lstat` metadata, opened-object type and
  regular-object identity, captured file bytes, the spawned Tightbeam session key, and
  explicit phase timestamps. On acquisition failure, it derives the refusal from the
  phase, C-08 operation order, and first failing observed path.
- I-06. The validator admits a Codex runtime delta only when its normalized path, type,
  mode, cardinality, dynamic-name, freshness, size, and cross-phase predicates satisfy
  C-07. A normalized-manifest mismatch does not create a prefix, subtree, or
  best-effort exception.
- I-07. The fixture does not delete, preseed, rename, repair, or synthesize a harness
  runtime path.
- I-08. A released fixture invocation that successfully creates the C-10 evidence file
  is consumed after either pass or refusal, including a run-start refusal before spawn.
- I-09. Evidence excludes raw sidecar bytes and decoded JSON member values.
- I-10. Future implementation custody contains only `scripts/feature_smoke.exs`.
- I-11. Parent commit `5f4341130419c4bae21bdd6c2278185dcd0f89a5`, product
  assignment `asg_17a50f66-c32d-42f2-aba5-dd39e072203e`, and facts 373, 384, 387,
  and 390 remain unchanged until a later explicit release.
- I-12. The validator refuses a mismatch without mutating an observed runtime path.
  When evidence append and sync succeed, it records the refusal before lifecycle
  cleanup can remove that path. An evidence-sink failure follows the console-only
  boundary in C-10.
- I-13. Every accepted deterministic case-only run and live matrix uses the exact
  feature-smoke launch envelope. The fixture does not chmod, replace, or reopen the
  evidence path to obtain mode `0600` after creation.
- I-14. The exact `0077` umask belongs to the feature-smoke zsh and Mix client process
  tree. The already-serving gateway remains outside that process tree. The gateway
  creates each harness process under the gateway's process state.

## Architecture

The pattern is **fixture harness-runtime admission**. It applies only to the
`check_local_deployment` group in `scripts/feature_smoke.exs`. It does not apply to
live home reconciliation, credential-store mutation, onboarding, harness process
supervision, product sessions, or another smoke group. It uses the existing read-only
Claude credential-liveness preflight only to decide the named-waiver input at run-start.

The implementation uses one validation seam for a harness leg's runtime delta. The
fixture invokes that seam separately for the Claude leg and the Codex leg at each
per-leg phase. One leg never validates the other harness's projected home. Parallel
allow lists and concurrent harness sessions are out of contract.

### C-01 — Phase boundaries

The fixture captures and validates these states in order:

1. C-10 establishes the evidence writer. When the selected harness set is exactly
   Codex and the selected waiver value is exact, the fixture captures one Claude waiver
   observation and performs no other credential operation before run-start validation.
2. In the sole run-start phase, the selected harness set is exactly Claude and Codex,
   or it is exactly Codex while the active named Claude waiver passes. The fixture has
   exactly one user, that user is an admin, and it has zero sessions, work items, and
   turns. A missing or wrong selected waiver returns `FX_FIXTURE_STATE` before any
   credential preflight or spawn. An inactive exact waiver returns
   `FX_FIXTURE_STATE` after the Claude waiver observation and before the selected leg's
   credential preflight or spawn. C-10 records `waiver=null` for either refusal.
3. When Claude is selected, pre-spawn validation requires the Claude projected home's
   leaf set to equal its owned baseline. Pre-wake and post-turn validation require that
   leg's Claude runtime delta to satisfy C-02 through C-06. Claude cleanup runs after
   the Claude post-turn evidence record and before the next harness leg starts.
4. For the Codex leg, pre-spawn validation requires the Codex projected home's leaf set
   to equal its owned baseline. Pre-wake and post-turn validation require that leg's
   Codex runtime delta to satisfy C-07's exact normalized manifest. Codex cleanup runs
   after the Codex post-turn evidence record.
5. A refusal writes the current phase's evidence record and stops the selected matrix. If
   the current leg reached spawn, its existing cleanup runs before the matrix stops.
   The fixture does not start a later harness leg.
6. The validator performs no post-retirement admission check and does not observe the
   other harness's home during one leg.

Acceptance example: Given a native-reconciled fixture with exact owned baselines, when
Claude spawn and tuning return and no Claude wake has been sent, then the validator
labels the Claude observation `pre-wake`, evaluates C-02 through C-06 before the wake
call, and does not inspect the Codex home.

Acceptance example: Given completed Claude cleanup, or an active named Claude waiver,
and a native-reconciled Codex home, when Codex spawn and tuning return and no Codex wake
has been sent, then the validator labels the Codex observation `pre-wake`, evaluates
C-07 before the wake call, and does not inspect the Claude projected home.

Acceptance example: Given a Codex-only candidate with the exact selected waiver value,
when its same-invocation Claude waiver observation has `status=:pass`, then run-start
returns `FX_FIXTURE_STATE`, records `waiver=null`, and sends no selected-leg credential
preflight or spawn.

### C-02 — Complete admitted Claude path set

After the C-08 snapshot attempt succeeds, the Claude runtime delta at pre-wake and
post-turn contains exactly these five paths:

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
the validator evaluates the whole delta, then it refuses with `FX_PATH_SET`, emits
`path=-`, and does not read the nested entry as an admitted sidecar.

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

The opener may authorize one fresh fixture after reviewed-clean contract and
implementation evidence. The release names the full or named-waiver matrix. C-01
run-start state makes prior harness use observable. A refusal after harness spawn
consumes that fixture. Successful C-10 evidence-file creation also consumes the
released fixture when run-start later refuses before spawn. A later attempt needs a
new ruling.

Acceptance example: Given a passing pre-wake sidecar and a post-turn sidecar with a
different `sessionId`, when the validator compares sidecar identity, then it refuses
with `FX_IDENTITY_DRIFT`.

### C-07 — Exact Codex runtime manifest

After the C-08 snapshot attempt succeeds, the Codex pre-wake runtime delta contains
exactly 300 entries. The entry counts are 113 directories, 183 regular files, and four
symlinks. The mode counts are two `0600`, 181 `0644`, one `0700`, 112 `0755`, and four
`0777`. No entry has another type or mode.

Each raw Codex relative path contains only ASCII bytes from `A-Z`, `a-z`, `0-9`, `.`,
`_`, `/`, and `-`. No component is empty, `.` or `..`. The raw path does not contain
the reserved normalization bytes `<` or `>`.

Exactly four dynamic-name families exist:

1. `cache/codex_apps_server_info/<cache-key>.json` and
   `cache/codex_apps_tools/<cache-key>.json` are the only dynamic cache paths.
   `<cache-key>` matches `[0-9a-f]{40}` and is byte-equal in both paths.
2. `sessions` has exactly one direct year directory, one direct month directory below
   that year, one direct day directory below that month, and one rollout file below
   that day. Their path is
   `sessions/<yyyy>/<mm>/<dd>/rollout-<yyyy>-<mm>-<dd>T<hh>-<minute>-<ss>-<run-uuid>.jsonl`.
   `<yyyy>` is exactly four ASCII decimal digits. Each of `<mm>`, `<dd>`, `<hh>`,
   `<minute>`, and `<ss>` is exactly two ASCII decimal digits. The repeated date fields
   are byte-equal. Month is `01` through `12`; day is `01` through the Gregorian number
   of days in that year and month; hour is `00` through `23`; minute and second are
   `00` through `59`. The fields encode one UTC second with no offset, fractional
   second, or leap-second spelling. Its Unix epoch second is `rollout_s`. Integer
   division requires
   `div(spawn_started_at, 1000) <= rollout_s <= div(snapshot_finished_at, 1000)`.
   `<run-uuid>` is lowercase canonical UUID text. The validator rejects a shorter,
   longer, signed, space-padded, or otherwise alternate field spelling before
   normalization.
3. `shell_snapshots` has exactly two direct regular-file children. Each name matches
   `<snapshot-uuid>.<epoch-ns>.sh`, where the UUID is lowercase canonical UUID text and
   `<epoch-ns>` is exactly 19 decimal digits with a nonzero first digit. The two names
   differ. Exactly one snapshot UUID equals `<run-uuid>`. The other snapshot UUID
   differs from `<run-uuid>`. Integer division of each `<epoch-ns>` by `1_000_000`
   yields a Unix epoch millisecond inside the current Codex spawn interval.
4. `tmp/arg0` has exactly one direct directory named `codex-arg0<token>`, where
   `<token>` matches `[0-9A-Za-z]{6}`. That directory has exactly five direct children:
   regular file `.lock` and symlinks `apply_patch`, `applypatch`,
   `codex-execve-wrapper`, and `codex-linux-sandbox`. No nested child exists below
   those five entries.

The validator produces the normalized Codex manifest with these substitutions:

- It substitutes `<cache-key>` for the validated cache key in both cache paths.
- It substitutes `<yyyy>`, `<mm>`, and `<dd>` in the three session ancestor paths. It
  emits the normalized rollout path
  `sessions/<yyyy>/<mm>/<dd>/rollout-<date>T<time>-<run-uuid>.jsonl`.
- It emits `shell_snapshots/<snapshot-uuid>.<epoch-ns>.sh` for each validated shell
  snapshot. The two observed files therefore produce two equal normalized path
  strings, and both tuples remain in the manifest.
- It substitutes `<token>` for the validated `codex-arg0` suffix in that directory and
  its five children.
- It leaves each other validated raw path byte unchanged.

For each observed entry, the validator emits one ASCII manifest line containing the
normalized path, one tab byte, the lowercase type token, one tab byte, the four-digit
mode, and one LF byte. It sorts the 300 lines by normalized-path bytes, then type bytes,
then mode bytes. The SHA-256 of the concatenated lines equals
`2040e2080e389b9a59650e77c7ba246a2c97396ea79b514b2d61c98f7c23f4d0`.
The two equal normalized shell-snapshot lines are present twice. Each other normalized
path occurs once.

Each regular-file size is an integer from zero through 8,388,608 bytes. The sum of the
183 regular-file sizes is at most 33,554,432 bytes. C-08 captures a SHA-256 for each
regular file but C-07 does not assign semantics to its bytes.

At post-turn, the Codex runtime delta independently satisfies the same entry counts,
type counts, mode counts, dynamic-name predicates, normalized manifest SHA-256, and
size bounds. Its cache key, session date, rollout time, rollout UUID, two shell-snapshot
names, and `codex-arg0` token are byte-equal to the pre-wake values. Regular-file sizes
and SHA-256 values may change within the stated bounds. The Codex leg does not inspect
the Claude projected home.

A failed C-07 predicate returns `FX_CODEX_RUNTIME_PATH`, `path=-`, and `clause=C-07`.
It does not convert the observed path into a Claude exception.

Acceptance example: Given the exact retained 300-entry path, type, and mode image with
fresh dynamic names, when the Codex pre-wake validator normalizes it, then the manifest
SHA-256 and size predicates pass.

Acceptance example: Given the passing image plus `plugins/cache/extra`, when the Codex
validator runs, then it refuses with `FX_CODEX_RUNTIME_PATH`, `path=-`, and
`clause=C-07`.

Acceptance example: Given a passing pre-wake image and a post-turn image whose
`codex-arg0` token differs, when cross-phase validation runs, then it refuses with
`FX_CODEX_RUNTIME_PATH`, `path=-`, and `clause=C-07`.

### C-08 — Refusal behavior

The validator refuses the smoke on the first failing ordered check. It does not remove,
rename, rewrite, chmod, preseed, or ignore the observed entry. Cleanup may retire the
spawned session through the existing fixture lifecycle after evidence capture.

At pre-spawn, pre-wake, and post-turn, the validator makes exactly one runtime snapshot
attempt. It enumerates the projected home once without following symlinks. For each
successfully enumerated directory, it sorts direct-child names by raw filename bytes
and processes them depth-first. For each observed relative path, it obtains initial
`lstat` metadata once with `:file.read_link_info/1`. It does not descend through an
entry whose initial type is not `directory`.

For each entry whose initial type is `regular` and whose bytes the phase requires, the
validator performs these operations in order:

1. It captures the initial regular-object identity from the `lstat` metadata.
2. It opens the path once with documented OTP modes `[:read, :binary, :raw]`.
3. Before a read, it calls `:file.read_file_info/1` on that open handle. It requires
   the opened type to be `regular`. It requires the opened regular-object identity to
   equal the initial identity.
4. It reads that one handle to EOF once and computes the required byte size and
   SHA-256 from those bytes.
5. While the handle remains open, it obtains final `lstat` metadata once with
   `:file.read_link_info/1`. It requires the final type to be `regular`. It requires
   the final regular-object identity to equal both earlier identities.

Each identity acquisition requires three integer fields. A missing, noninteger, or
unequal field is an identity acquisition failure.

A replacement symlink or rename that resolves to a different regular-object identity
returns `FX_SNAPSHOT` instead of supplying admitted bytes. The validator does not
claim to observe an intermediate path state that resolves to the same still-open
object. Such an unobserved state cannot change the captured object's identity or
bytes.

The validator does not pass an undocumented open mode. It does not retry an operation,
restart the walk, use a fallback reader, invoke a helper or native dependency, or take
a second snapshot.

If projected-home enumeration fails, the validator refuses with `FX_SNAPSHOT`,
`path=-`, and `clause=C-08`. If directory enumeration, initial `lstat`, open,
opened-handle information, opened type, opened identity, read, final `lstat`, final
type, or final identity fails for an observed relative path, it refuses with
`FX_SNAPSHOT`, that path's evidence token, and `clause=C-08`. A disappearance is the
corresponding initial or final `lstat` or open failure. The validator emits no
operating-system error text. C-10 records exactly the metadata and bytes captured
before this refusal.

Acceptance example: Given a sidecar symlink whose target is a schema-valid JSON file,
when the validator reads `lstat` metadata, then it refuses with `FX_TYPE` before it
opens the target.

Acceptance example: Given `.claude.json` has captured regular-file metadata but its
single open fails, when snapshot acquisition runs, then the validator refuses with
`FX_SNAPSHOT`, `path=.claude.json`, and `clause=C-08`; its evidence entry has
`sha256=null`, and the validator does not retry or evaluate `FX_MODE`.

Acceptance example: Given initial `lstat` reports regular-object identity A for a
sidecar and the opened handle reports regular-object identity B, when snapshot
acquisition compares the identities, then it refuses with `FX_SNAPSHOT`, does not read
the handle, and does not retry with another reader.

### C-09 — Deterministic error mapping

The validator evaluates categories in this order:

1. `FX_PHASE` for a missing or out-of-order phase input.
2. `FX_FIXTURE_STATE` for a run-start harness-selection, named-waiver input,
   named-waiver observation, or fixture-count mismatch.
3. `FX_CLOCK` for an inverted spawn interval.
4. `FX_SNAPSHOT` for the C-08 runtime-snapshot acquisition failure.
5. `FX_BASELINE` for a pre-spawn baseline mismatch.
6. `FX_PATH_SET` for Claude path or cardinality mismatch.
7. `FX_CODEX_RUNTIME_PATH` for a C-07 dynamic-name, normalized-manifest,
   cardinality, type, mode, size, freshness, or cross-phase mismatch.
8. `FX_TYPE` for symlink, wrong type, or special type.
9. `FX_MODE` for a permission-mode mismatch.
10. `FX_SIZE` for a sidecar outside the byte bound.
11. `FX_JSON` for invalid UTF-8, invalid JSON, or duplicate member names.
12. `FX_JSON_SHAPE` when `.claude.json` has a valid JSON top level other than an
    object.
13. `FX_SIDECAR_SCHEMA` for a sidecar member-set or member-type mismatch.
14. `FX_SIDECAR_SEMANTIC` for C-03 or C-04 value mismatch.
15. `FX_FRESHNESS` for C-05 mismatch.
16. `FX_IDENTITY_DRIFT` for C-06 cross-phase mismatch.

`FX_PHASE`, `FX_FIXTURE_STATE`, `FX_CLOCK`, `FX_BASELINE`, `FX_PATH_SET`, and
`FX_CODEX_RUNTIME_PATH` are set-level categories. Their refusal lines emit `path=-`,
and the validator performs no path sort for them. For `FX_PATH_SET`, the validator does
not construct a candidate for a missing expected path. `FX_SNAPSHOT` uses the
single-attempt operation and path order
in C-08. It does not collect or sort failure candidates after the first acquisition
failure. Within each other category, the validator sorts observed
relative paths by raw byte order. If one observed path fails more than one predicate in
that category, the validator selects the first failed predicate in the C-10 `checks`
order. The refusal line's `clause` field names that predicate's mapped C-clause. This
category, observed path, then predicate order is the complete first-failure tie-break
for path-specific categories. One refusal line has this shape:

`feature-smoke fixture HOME REFUSED code=<code> harness=<harness-or-all> phase=<phase> principal=<evidence-token> path=<evidence-token-or-dash> clause=<clause-id>`

Acceptance example: Given both a missing `sessions` directory and a wrong-mode
`.claude.json`, when the validator evaluates the delta, then it returns `FX_PATH_SET`
with `path=-` before `FX_MODE` on repeated runs.

Acceptance example: Given one sidecar whose internal `pid` differs from its filename
and whose `cwd` differs from the expected workdir, when semantic validation runs, then
the validator returns `FX_SIDECAR_SEMANTIC` with `clause=C-03` because
`filename_pid_equal` precedes `expected_cwd_equal`.

### C-10 — Evidence and cleanup boundary

Before run-start validation, the C-12 launch envelope has set exact umask `0077` and
replaced its subshell with the Mix process. The fixture opens the evidence path once
with documented OTP modes `[:read, :write, :exclusive, :binary, :raw]`. On Unix OTP
28.5 this exclusive create requests mode `0666`; the inherited `0077` umask makes the
new inode's effective creation mode exact `0600`. The fixture does not request mode
`0600` from OTP. It does not call `chmod`, `fchmod`, `:file.change_mode/2`, a helper,
or a native dependency before or after the open.

While the new handle remains open, the fixture obtains file information from that
handle and obtains `lstat` information for the path. It requires both observations to
be regular files with exact permission mode `0600`, and it requires their
regular-object identities to be equal. The fixture retains that same handle as the
sole evidence writer. If the path exists, creation fails, either information operation
fails, either type or mode differs, or the identities differ, the fixture emits this
one line and stops before run-start validation without deleting, replacing, chmodding,
or reopening the path:

`feature-smoke fixture HOME REFUSED code=FX_EVIDENCE harness=all phase=run-start principal=run-start path=feature-smoke-home-evidence.jsonl clause=C-10`

This pre-record refusal creates no evidence record. It precedes the C-09 category
order because no valid evidence file exists in which to record a check.

An invocation outside the exact launch envelope is not release evidence, even when an
ambient umask happens to produce mode `0600`. C-12 binds launch provenance to a
system-call trace. The trace is release evidence outside product code; it is not a
fixture helper, runtime dependency, or additional implementation file.

The launch envelope does not start the Tightbeam gateway or either harness process.
The Mix client reads the gateway process boundary's existing connection record and
sends each spawn request over HTTP. Therefore the client `0077` umask applies to the
evidence-file open but does not alter the gateway umask that governs its later Claude
and Codex descendants. C-02 validates the modes that those descendants produce.

For each phase, the fixture makes one evidence-record append attempt. If that append
succeeds, the fixture requires `:file.sync(evidence_io_device)` to return `:ok` before
that phase returns, sends a wake, writes a sentinel, or enters cleanup. If append or
sync fails, the fixture emits the C-09 refusal-line shape with `code=FX_EVIDENCE`, the
current harness, phase, and principal, `path=feature-smoke-home-evidence.jsonl`, and
`clause=C-10`; it starts no later admission, spawn, wake, or sentinel action and does
not attempt a second evidence append. The console refusal is the only guaranteed
evidence for this sink failure. The evidence file may omit the current phase's complete
JSON object and LF, or the current record may remain unsynced. The fixture does not
retry the append, use a fallback sink, or claim a durable current-phase record. If the
current leg reached spawn, its existing cleanup still runs. A passing full matrix
contains exactly seven records in this sequence: run-start; Claude pre-spawn, pre-wake,
and post-turn; Codex pre-spawn, pre-wake, and post-turn. A passing Codex-only matrix
under the active named Claude waiver contains exactly four records: run-start; Codex
pre-spawn, pre-wake, and post-turn. For a validator refusal other than an
evidence-sink failure,
the evidence file contains one record for each completed phase plus one synced
`refused` record for the failing phase. It contains no record for a later phase or
harness leg. This refusal-cardinality rule does not apply when append or sync itself
fails.

Each record is one JSON object with keys in this exact order and no insignificant
whitespace:

`schema`, `sequence`, `harness`, `phase`, `principal`, `waiver`, `result`, `cause`,
`entries`, `checks`

The fields have these contracts:

- `schema` is string `tightbeam.feature_smoke.home_evidence.v2`.
- `sequence` is an integer that starts at `1` and increments by one per appended line.
- `harness` is string `all` for run-start or the current leg's lowercase harness name.
- `phase` is one of `run-start`, `pre-spawn`, `pre-wake`, or `post-turn`.
- `principal` is string `run-start`, string `pre-spawn`, or the spawned Tightbeam
  session key rendered as an evidence token.
- `waiver` is string `dr_7383a755-820d-4f1e-b882-4f16b08a103f` in each record of a
  Codex-only matrix admitted under the active named Claude waiver. It is JSON `null` in
  each record of a full two-leg matrix and in a run-start refusal that did not admit a
  named-waiver matrix. The fixture does not serialize an absent, wrong, inactive, or
  otherwise non-admitted supplied waiver value.
- `result` is string `pass` or `refused`.
- `cause` is string `validated` for a passing record. For a refused record, it is the
  mapped C-clause of the first failed predicate selected by C-09.
- `entries` is an array sorted by each entry's raw relative-path bytes. Each entry has
  keys `path`, `type`, `mode`, `size`, and `sha256` in that order. `path` is an evidence
  token string. `type` is string `directory`, `regular`, `symlink`, or `other`, or JSON
  `null` only for the failing path when `lstat` did not return metadata. `mode` is a
  string of exactly four digits matching `[0-7]{4}` for the permission and special bits,
  or JSON `null` when `lstat` did not return metadata. `size` is the regular file's
  nonnegative integer byte size or JSON `null`. In a pre-wake or post-turn record,
  `sha256` is the regular file's lowercase SHA-256 string matching `[0-9a-f]{64}` when
  the one read completed. It is JSON `null` for run-start, pre-spawn, a non-regular
  entry, a path without `lstat` metadata, or a regular entry whose bytes were not fully
  captured because C-08 refused acquisition.
- `checks` is an array that contains exactly the following objects in the listed order.
  Each object has keys `id`, `applicable`, `evaluated`, and `passed` in that order. The
  two state fields are booleans. `passed` is a boolean when `evaluated=true` and is JSON
  `null` when `evaluated=false`. `applicable=false` requires `evaluated=false`.

The fixed check order is:

1. `phase_order`
2. `fixture_state`
3. `clock_order`
4. `snapshot_acquired`
5. `baseline_equal`
6. `path_set_equal`
7. `codex_dynamic_names_valid`
8. `codex_manifest_equal`
9. `codex_size_bounded`
10. `codex_identity_matches_pre_wake`
11. `entry_type_equal`
12. `entry_mode_equal`
13. `sidecar_size_bounded`
14. `json_utf8_valid`
15. `json_syntax_valid`
16. `json_unique_members`
17. `claude_json_object`
18. `sidecar_member_set_equal`
19. `sidecar_member_types_equal`
20. `filename_pid_equal`
21. `session_id_shape`
22. `expected_cwd_equal`
23. `proc_start_shape`
24. `version_shape`
25. `peer_protocol_equal`
26. `kind_equal`
27. `entrypoint_equal`
28. `name_nonempty`
29. `name_source_equal`
30. `backup_epoch_in_interval`
31. `started_at_in_interval`
32. `identity_matches_pre_wake`

The validator maps checks 1, 2, and 5 to C-01; check 3 to C-05; check 4 to C-08;
checks 6, 11-13, and 17 to C-02; checks 7-10 to C-07; checks 14-16 to C-02 for
`.claude.json` or the backup and to C-04 for the sidecar; checks 18 and 19 to C-04;
check 20 to C-03; checks 21-29 to C-04; checks 30 and 31 to C-05; and check 32 to C-06.
For a Codex record, check 3 maps to C-07 instead of C-05.

When `snapshot_acquired` passes, each record uses the exact entry rules in this table.
On `FX_SNAPSHOT`, the partial-entry paragraph below replaces only the table's `entries`
content; check applicability remains unchanged. A listed range includes both endpoints.
Every unlisted check is `applicable=false`, `evaluated=false`, and `passed=null`.

| Record | `entries` content | Applicable checks |
| --- | --- | --- |
| Run-start | Empty array | 1-2 |
| Claude pre-spawn | Complete recursive projected-home path set after subtracting only baseline ancestor directories | 1, 4-5 |
| Codex pre-spawn | Complete recursive projected-home path set after subtracting only baseline ancestor directories | 1, 4-5 |
| Claude pre-wake | Complete Claude runtime delta | 1, 3-4, 6, 11-31 |
| Claude post-turn | Complete Claude runtime delta | 1, 3-4, 6, 11-32 |
| Codex pre-wake | Complete Codex runtime delta | 1, 3-4, 7-9 |
| Codex post-turn | Complete Codex runtime delta | 1, 3-4, 7-10 |

A validator evaluates applicable checks in fixed numeric order. If one fails, each
later applicable check is `applicable=true`, `evaluated=false`, and `passed=null`.
`identity_matches_pre_wake` is therefore inapplicable at Claude pre-wake and applicable
at Claude post-turn. For an entry whose type is not `regular`, `size` and `sha256` are
`null`; the validator never follows a symlink to populate them.

On `FX_SNAPSHOT`, the record's `entries` array contains each entry whose initial
`lstat` metadata and required bytes were captured before the failure, plus the failing
observed path. It omits unprocessed paths and does not claim to be a complete runtime
delta. If projected-home enumeration fails, `entries` is empty. If initial `lstat`
fails, the failing entry has `type=null`, `mode=null`, `size=null`, and
`sha256=null`. If open, opened-handle information, opened type, opened identity, or
read fails, the failing entry retains its initial `lstat` fields and has
`sha256=null`. If final `lstat`, final type, or final identity fails after the read
completed, the entry retains its initial `lstat` fields and the captured SHA-256.
Check `snapshot_acquired` is `evaluated=true` and `passed=false`; each later applicable
check is unevaluated. The record has `result="refused"` and `cause="C-08"`. No record
field contains a regular-object identity or raw operating-system error.

The fixture writes JSON strings using their stated ASCII tokens, appends one LF byte,
and emits no other byte to the evidence file. It does not record JSON bytes, decoded
member values, credential material, stdout, or stderr. It records and syncs evidence
before retirement because harness cleanup may remove the sidecar. The fixture does not
delete the used fixture base or evidence file; the existing harness lifecycle may
remove its own transient sidecar during retirement.

Acceptance example: Given a sidecar whose `cwd` is wrong, when the validator refuses,
then the current phase record has `result="refused"`, `cause="C-04"`, and
`expected_cwd_equal` with `evaluated=true` and `passed=false`; the record omits both the
observed and expected path values.

Acceptance example: Given a passing full matrix, when both per-leg cleanup blocks
complete, then the retained evidence file has seven LF-terminated records with
contiguous `sequence` values and each passing record has `cause="validated"`.

Acceptance example: Given a passing Codex-only matrix under the active named Claude
waiver, when Codex cleanup completes, then the retained evidence file has four
LF-terminated records and contains no Claude phase record.

### C-11 — One-file implementation custody

A future implementation assignment owns only `scripts/feature_smoke.exs`. It starts
from the then-current `origin/0.1.9`, names this reviewed artifact and SHA, and keeps
the existing exact-home proof.

The builder may read the surrendered one-file diff as evidence. The builder derives
behavior from this contract and does not treat the diff as authority.

The C-12 zsh subshell and system-call trace do not add a product file, linked
library, fixture subprocess, or runtime helper. The product implementation remains one
file and uses only the documented OTP operations in C-08 and C-10.

Acceptance example: Given an implementation proposal that also changes
`lib/tightbeam/homes.ex`, when custody is checked, then implementation stops before an
edit and reports the additional-file requirement to the opener.

### C-12 — Release sequence

The release sequence is:

1. One fresh linked independent reviewer reads the exact contract and recon hashes.
2. The reviewer records `reviewed-clean` or `changes-requested` on a review assignment
   linked to this producer assignment.
3. After `reviewed-clean`, the opener explicitly releases one one-file implementation
   correction. The correction preserves the named-waiver behavior from exact commit
   `c6b6632788f06ea8c7e64e6e08a1a635e07f01f4` and replaces its empty Codex-delta
   predicate with C-07 and the C-10 v2 evidence checks.
4. Before coding or a post-review correction, the implementer synchronizes and
   verifies a green `origin/0.1.9` in the owned product workspace. The implementer then
   proves deterministic allow and reject cases, format, syntax, `git diff --check`, and
   the repository gate before a live fixture. The case-only command runs in this exact
   envelope:
   `(export TIGHTBEAM_SMOKE_HOME_CASES_ONLY=1 && umask 077 && exec mix run --no-start scripts/feature_smoke.exs)`.
5. The opener authorizes one new never-reused fixture and names the selected harness
   set. If Gibson's org Anthropic credential is valid, it selects Claude then Codex and
   the named waiver is inactive. If that credential remains invalid, it may select
   Codex only with the exact named-waiver input. This opener observation selects the
   candidate matrix; it does not replace the fixture's run-start observation.
6. The implementer runs the selected matrix once with
   `(umask 077 && exec mix run --no-start scripts/feature_smoke.exs)` and records pass
   evidence or the exact first blocker. For a Codex-only candidate, the fixture captures
   the Claude waiver observation after evidence setup and immediately before run-start.
   Only a rejected-credential observation activates the waiver. A live-credential or
   unknown-credential observation returns `FX_FIXTURE_STATE` with `waiver=null` before
   the selected-leg credential preflight or spawn. A refusal consumes that fixture. The
   implementer does not retry or reuse it.
7. A passing implementation returns for one fresh linked independent exact-commit
   review before the parent lane resumes.

Closed implementation assignment `asg_0c3a45b1-d0ac-499d-b55e-2b7743a11c21` and its
reviewed-clean commit `ec2b28b8eaf47e3ef85318524752a827c23bd0af` remain historical
evidence. The named-waiver correction commit remains evidence until step 3 creates the
new bounded implementation obligation. Neither commit is live-fixture authority.

Before step 5, the implementer records one Gibson system-call trace of the exact
case-only envelope. The trace starts at the subshell, follows descendants, and proves
this order: the traced subshell's umask call sets `0077` and returns prior mask `000`;
it execs Mix; OTP exclusively creates the evidence path with request mode `0666`; the
fixture's first handle and path metadata observations both report exact mode `0600`.
The trace contains no `chmod`, `fchmod`,
`fchmodat`, or second open of that evidence path. The implementer records the trace
command, tool version, result, and SHA-256. The trace artifact is evidence only and is
not copied into either repository.

The system-call trace is one Gibson `strace -f -yy -s 4096` capture. Its selected
system calls are exactly `umask`, `execve`, `open`, `openat`, `openat2`, `fstat`,
`newfstatat`, `statx`, `chmod`, `fchmod`, `fchmodat`, and `fchmodat2`. It decodes
file-status mode results. It does not request environment strings or file-buffer
contents. Before recording the artifact, the implementer verifies that it contains no
credential value. If the installed tracer cannot select or decode those supported host
events, the implementer stops before step 5 and returns the exact blocker for ruling.

Before step 5, the implementer also records a source-topology gate for the exact
product commit. The gate proves these predicates in source order:

1. The documented command is `mix run --no-start scripts/feature_smoke.exs`.
2. `FeatureSmoke.run/0` binds `gw` by reading and decoding
   `<fixture-base>/gateway.json` before it begins a leg.
3. `post/3` builds `http://127.0.0.1:<gateway-port>/agent/dispatch` from `gw`, then
   invokes `curl` for `spawn` and the other verbs.
4. A nonzero `curl` result calls `fail/2` instead of returning a spawn result.

If a predicate fails, the implementer stops before step 5 and returns the exact blocker
for ruling.

Acceptance example: Given a reviewed-clean contract but no opener release, when a
worker proposes a fixture run, then the worker remains blocked and does not create the
fixture.

## Acceptance

The future implementer attaches one deterministic case to each row before live smoke.
The Given/When/Then examples in C-01 through C-12 are part of this acceptance contract.

| ID | Given | When | Then | Trace |
| --- | --- | --- | --- | --- |
| AC-01 | Exactly Claude and Codex are selected without the named waiver; the fixture has one user who is an admin and zero sessions, work items, and turns | Run-start validation runs | The fixture passes once before the first credential preflight | C-01, C-06 |
| AC-02 | A prior spawn left one session row in the base | Run-start validation runs | `FX_FIXTURE_STATE` refuses the reused fixture before credential preflight | C-01, C-06, C-09 |
| AC-03 | One harness leg has its exact owned baseline | That leg's pre-spawn validation runs | Its baseline passes, no runtime exception is used, and the validator does not inspect the other harness's home | C-01, I-02 |
| AC-04 | The exact five-path Claude runtime set exists in the Claude leg | That leg's pre-wake validation runs | The set passes without a launcher PID read | C-02-C-05, I-04 |
| AC-05 | Canonical filename and equal internal `pid` | Sidecar semantics run | Filename-PID binding passes | C-03 |
| AC-06 | `sessions/0123.json` with internal `pid=123` | Whole-set path validation runs | `FX_PATH_SET` refuses with `path=-` before sidecar semantics | C-02, C-03, C-09 |
| AC-07 | `sessions/123.json` has internal `pid=124` | Sidecar semantics run | `FX_SIDECAR_SEMANTIC` refuses the unequal binding | C-03, C-09 |
| AC-08 | One runtime JSON file contains invalid UTF-8 | JSON validation runs | `FX_JSON` refuses it | C-02, C-04, C-09 |
| AC-09 | One runtime JSON file contains malformed JSON | JSON validation runs | `FX_JSON` refuses it | C-02, C-04, C-09 |
| AC-10 | One runtime JSON object has a duplicate member name | JSON validation runs | `FX_JSON` refuses it | C-02, C-04, C-09 |
| AC-11 | Sidecar has one missing member | Schema validation runs | `FX_SIDECAR_SCHEMA` refuses it | C-04, C-09 |
| AC-12 | Sidecar has one extra member | Schema validation runs | `FX_SIDECAR_SCHEMA` refuses it | C-04, C-09 |
| AC-13 | Sidecar has one member with the wrong JSON type | Schema validation runs | `FX_SIDECAR_SCHEMA` refuses it | C-04, C-09 |
| AC-14 | Sidecar `cwd` differs from the spawned Tightbeam workdir | Semantic validation runs | `FX_SIDECAR_SEMANTIC` refuses it without logging either value | C-04, C-10 |
| AC-15 | Backup timestamp or `startedAt` lies outside the spawn interval | Freshness validation runs | `FX_FRESHNESS` refuses it | C-05 |
| AC-16 | Two sidecars or two backups exist | Whole-set validation runs | `FX_PATH_SET` refuses the set with `path=-` | C-02, C-06 |
| AC-17 | The post-turn backup has a new canonical name and satisfies C-02 and C-05 | Post-turn validation runs | The backup passes without requiring pre-wake filename equality | C-05, C-06 |
| AC-18 | Post-turn sidecar identity differs from pre-wake identity | Continuity validation runs | `FX_IDENTITY_DRIFT` refuses it | C-06 |
| AC-19 | One unexpected Claude nested path exists | Whole-set validation runs | `FX_PATH_SET` refuses with `path=-` | C-02, C-08-C-09 |
| AC-20 | One symlink occupies an admitted name | Metadata validation runs | `FX_TYPE` refuses it without following the link | C-02, C-08 |
| AC-21 | `.claude.json` has mode `0644` | Mode validation runs | `FX_MODE` refuses it | C-02, C-09 |
| AC-22 | Sidecar has 4097 bytes | Size validation runs | `FX_SIZE` refuses it before JSON decoding | C-02, C-09 |
| AC-23 | `.claude.json` contains the valid JSON value `[]` | JSON-shape validation runs | `FX_JSON_SHAPE` refuses it | C-02, C-09 |
| AC-24 | The Codex leg has the passing normalized manifest plus one runtime path | That leg's validation runs | `FX_CODEX_RUNTIME_PATH` refuses with `path=-` without inspecting the Claude home | C-07 |
| AC-25 | Snapshot acquisition succeeds, one path fails multiple predicates, and another path fails in the same or a later error category | The case runs repeatedly | Each run returns the same first code, phase, path evidence token, and clause selected by category, raw path, then C-10 predicate order | C-09-C-10 |
| AC-26 | One full matrix uses the exact live launch envelope and passes | Both per-leg cleanup blocks complete | The v2 evidence file was created with effective mode `0600` and the retained file contains exactly seven synced LF-terminated canonical JSON records with contiguous sequence values, `cause="validated"`, exact `entries` and `checks`, and no decoded JSON values or observed file bytes | C-10, C-12 |
| AC-27 | One fixture reaches harness spawn and refuses | Cleanup completes | The fixture base remains, no observed runtime path is fixture-mutated before lifecycle cleanup, and no second fixture starts | C-06, C-08, C-10 |
| AC-28 | Reviewed-clean contract and explicit release exist | One-file implementation begins | Only `scripts/feature_smoke.exs` changes from current `origin/0.1.9` | C-11-C-12 |
| AC-29 | Deterministic cases and repository gates pass | One fresh full matrix runs | One Claude leg completes first and one Codex leg completes second; Claude passes its own pre-wake and post-turn sidecar records; Codex passes its exact normalized-manifest pre-wake and post-turn records; neither leg inspects the other home; the evidence file contains seven records | C-01-C-12 |
| AC-30 | The selected matrix encounters a new runtime path or schema | The validator refuses | The implementer files the exact blocker and does not retry | C-06-C-10, C-12 |
| AC-31 | Parent commit, product assignment, and facts are read after this contract | Contract production ends | Their identifiers and state match I-11 | I-11 |
| AC-32 | The Claude pre-wake sidecar has a wrong `cwd` | Claude pre-wake validation runs | The current evidence record is `refused` with `cause="C-04"`, `expected_cwd_equal` is evaluated and false, no later-phase or Codex-leg record exists, and the evidence file remains through cleanup | C-04, C-09-C-10 |
| AC-33 | The evidence path already exists | Exclusive creation runs | `FX_EVIDENCE` refuses before run-start validation, writes no evidence record, and does not delete, replace, or change the existing path | C-10 |
| AC-34 | An evidence append or `:file.sync/1` fails after spawn | The current phase writes evidence | The console `FX_EVIDENCE` line is the only guaranteed evidence; the fixture makes no completeness or durability claim for the current-phase record, performs no retry, fallback sink, or secondary append, starts no later admission, wake, or sentinel action, and still runs existing cleanup | I-12, C-10 |
| AC-35 | One required Claude path is missing and one unexpected path exists | Whole-set validation runs repeatedly | Each run returns `FX_PATH_SET` with `path=-`; the validator neither constructs a missing-path candidate nor sorts the unexpected path for this category | C-02, C-09 |
| AC-36 | Projected-home enumeration returns an error | The single snapshot attempt runs | `FX_SNAPSHOT` refuses with `path=-`, an empty `entries` array, `snapshot_acquired` evaluated and false, and no retry | C-08-C-10 |
| AC-37 | `lstat` returns an error for observed path `sessions/2.json` | The single snapshot attempt reaches that path | `FX_SNAPSHOT` refuses with `path=sessions/2.json`; the failing entry has null type, mode, size, and hash | C-08-C-10 |
| AC-38 | `.claude.json` has captured regular-file metadata and its single open returns an error | The snapshot attempts byte capture | `FX_SNAPSHOT` refuses with `path=.claude.json`; its captured metadata remains, `sha256=null`, and `FX_MODE` is not evaluated | C-08-C-10 |
| AC-39 | A regular sidecar read returns an error before EOF | The snapshot attempts byte capture | `FX_SNAPSHOT` refuses with the sidecar path, `sha256=null`, and no second read or snapshot | C-08-C-10 |
| AC-40 | The opened object is not regular after initial `lstat` reported a regular path | The snapshot verifies the opened type | `FX_SNAPSHOT` refuses with that path, `sha256=null`, and no fallback reader | C-08-C-10 |
| AC-41 | Initial `lstat` reports regular-object identity A and the opened handle reports regular-object identity B | The snapshot compares identities before reading | `FX_SNAPSHOT` refuses with that path, `sha256=null`, and no read, fallback, or retry | C-08-C-10 |
| AC-42 | Initial `lstat` and the opened handle report regular-object identity A, the read completes, and final `lstat` reports a symlink or identity B | The snapshot performs its final identity check while the handle remains open | `FX_SNAPSHOT` refuses with that path, retains the captured SHA-256, and does not take another snapshot | C-08-C-10 |
| AC-43 | The caller has ambient umask `000` and the case-only launch envelope starts under a descendant-following system-call trace | The deterministic case creates the evidence path | The traced umask call sets `0077` and returns prior mask `000`; the trace then orders Mix/BEAM exec and one exclusive create request with mode `0666`; the first handle and path metadata observations report exact mode `0600`; the trace contains no chmod-family call or second evidence-path open | AS-11, I-13, C-10-C-12 |
| AC-44 | Ambient umask would independently yield mode `0600`, but the exact launch envelope or its trace is absent | Release evidence is evaluated | The run is nonconforming and cannot authorize the live matrix or parent lane | I-13, C-10-C-12 |
| AC-45 | A Tightbeam gateway is already serving the fixture before the exact feature-smoke envelope starts | The Mix client sends the Claude and Codex spawn requests | The client uses the recorded gateway port over HTTP; the gateway creates both harness processes outside the client process tree; the client `0077` umask cannot change the gateway or harness umask | AS-12, I-14, C-10-C-12 |
| AC-46 | `gateway.json` names a loopback port with no serving Tightbeam gateway | The exact `mix run --no-start` client reaches its first HTTP request | `curl` returns nonzero, the client calls its failure path, and no harness spawn result exists | AS-12, I-14, C-10-C-12 |
| AC-47 | `TIGHTBEAM_SMOKE_CLAUDE_WAIVER` equals the exact waiver ID, only Codex is selected, and the same-invocation Claude waiver observation has exact step `P-claude`, status `:fail`, and note prefix `credential rejected: ` | Run-start validation runs | The fixture records the named waiver, admits the Codex-only selection, and starts no Claude phase | AS-13, AS-15, C-01, C-10 |
| AC-48 | Only Codex is selected and the exact named waiver is absent | Run-start validation runs | `FX_FIXTURE_STATE` refuses before any credential preflight or spawn; the synced run-start record has `waiver=null` | C-01, C-09-C-10 |
| AC-49 | The retained 300-entry Codex image is supplied with exact-width valid calendar fields, fresh valid dynamic tokens, and bounded sizes | Codex pre-wake validation runs | Dynamic-name checks pass and the normalized manifest SHA-256 equals the C-07 value | AS-14, C-07 |
| AC-50 | One Codex path is added, removed, renamed, or nested differently | Codex manifest validation runs | `FX_CODEX_RUNTIME_PATH` refuses with `path=-` and `clause=C-07` | C-07, C-09 |
| AC-51 | One Codex entry has a different type or mode | Codex manifest validation runs | `FX_CODEX_RUNTIME_PATH` refuses with `path=-` and `clause=C-07` | C-07, C-09 |
| AC-52 | One Codex regular file exceeds 8,388,608 bytes or the regular-file sum exceeds 33,554,432 bytes | Codex size validation runs | `FX_CODEX_RUNTIME_PATH` refuses with `path=-` and `clause=C-07` | C-07, C-09 |
| AC-53 | Codex pre-wake passes and one post-turn dynamic token differs | Codex post-turn validation runs | `FX_CODEX_RUNTIME_PATH` refuses the cross-phase mismatch with `path=-` | C-07, C-09-C-10 |
| AC-54 | The active named Claude waiver admits a passing Codex-only matrix | Codex cleanup completes | The v2 evidence file contains exactly four records in run-start, Codex pre-spawn, Codex pre-wake, Codex post-turn order | C-01, C-10-C-12 |
| AC-55 | A valid Gibson org Anthropic credential exists | The opener prepares step 5 | The named waiver is expired, the opener selects the full Claude-then-Codex matrix, and no Codex-only fixture is released | AS-13, C-12 |
| AC-56 | Only Codex is selected and `TIGHTBEAM_SMOKE_CLAUDE_WAIVER` contains a wrong string | Run-start validation runs | `FX_FIXTURE_STATE` refuses before any credential preflight or spawn; the synced run-start record has `waiver=null` and does not contain the supplied string | C-01, C-09-C-10 |
| AC-57 | Step 5 selected a Codex-only candidate, the exact waiver input remains set, and its same-invocation Claude waiver observation has `status=:pass` | Run-start validation runs | The waiver is inactive; `FX_FIXTURE_STATE` refuses with `waiver=null` before selected-leg preflight or spawn | AS-15, C-01, C-10, C-12 |
| AC-58 | A Codex-only candidate has the exact waiver input and its Claude waiver observation has `status=:incomplete` | Run-start validation runs | The waiver is inactive; `FX_FIXTURE_STATE` refuses with `waiver=null` before selected-leg preflight or spawn | AS-15, C-01, C-10, C-12 |
| AC-59 | A Codex-only candidate has the exact waiver input and its Claude waiver observation has `status=:fail` without the exact `credential rejected: ` prefix | Run-start validation runs | The waiver is inactive; `FX_FIXTURE_STATE` refuses with `waiver=null` before selected-leg preflight or spawn | AS-15, C-01, C-10, C-12 |
| AC-60 | The Codex runtime uses month directory `sessions/2026/8` with an otherwise matching rollout family | C-07 dynamic-name validation runs | `FX_CODEX_RUNTIME_PATH` refuses with `path=-` before manifest normalization | C-07, C-09 |

## Open Questions

None. Finding F8 in `att_101f8af2-6694-4389-8dc0-b39883077f48` is closed under
`dr_9a179914-0d23-440b-9a3b-4577e0d0c707`. The implementation-review create-mode
finding in `att_e167466a-8063-4d59-8d92-67750584cf7a` is resolved normatively by Mike's
`contract-amendment` ruling in `dr_16de6d11-492c-4ec4-aaa2-6cb1a03d4d7d`. F9 in
`att_5456488a-1187-44e4-983a-02d920586d8d` is resolved by the explicit pre-existing
gateway process boundary and its source-topology gate. One fresh linked review decides
whether the exact successor artifact is reviewed-clean. The C-07 empty-delta defect is
resolved normatively by `amend-after-recon` in
`dr_1c06d9c9-df96-4fb7-b49e-0752a9d9fe54`; that decision does not authorize a live
fixture.

The bounded successor amendment resolves R1-R3 in
`att_5ec4d759-138f-4775-9332-1ea11b9e38fa`: the same-invocation Claude waiver
observation decides expiry at run-start, a non-admitted run-start record uses
`waiver=null`, and C-07 fixes the calendar byte widths and UTC ranges before
normalization. These details implement the existing named-waiver and fail-closed
Codex-runtime intent; they add no product or fixture authority.

The following resolved boundaries remain gates, not open questions:

- The contract does not infer the schema of the deleted final-fixture bytes. A future
  fixture validates its own captured bytes and refuses a mismatch.
- A future Codex path, dynamic name, type, mode, size, or cross-phase state that differs
  from C-07 blocks parent verification. The validator does not infer a broader prefix
  or subtree exception from the retained observation.
- Implementation and fixture execution remain blocked until one linked independent
  review records `reviewed-clean` for the exact artifact hashes and the opener issues
  an explicit release.
