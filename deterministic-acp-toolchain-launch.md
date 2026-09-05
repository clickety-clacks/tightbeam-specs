# Deterministic ACP toolchain launch

Status: review candidate for implementation on the Tightbeam 0.2 main line.

Work item: `wi_abd25f93-ba45-4ba6-8933-5ca099307e5f`.

Authority:

- Mike's 2026-08-24 20:37 PT direction: prevent the missing-Node launch
  incident; do not inherit an interactive-shell `PATH`; record the resolved
  executable and lifecycle outcome.
- `0.2.0-cross-line-reconciliation-plan.md` F2: do not port commit `5ae9f10`
  or its `host_toolchain_dirs` registry; express the requirement as
  assimilation/provisioning host facts.
- The accepted durable turn-trace design remains unchanged. Its implementation
  commit is the repository object
  `c97c034d13ffdac99ce0df230bcf70edab4e80cf` (`c97c034`). Earlier receipts
  expanded the same short name to a nonexistent object; this spec uses the
  repository object.

## Goal

Make each local and remote ACP adapter launch independent of the gateway's
inherited `PATH`. Assimilation records the executable facts it observed on the
target host. A launch banks one deterministic plan from those facts before it
opens a process. The durable harness-process read then states which Node
executable and child `PATH` the launch used, plus the launch's existing
lifecycle outcome.

The governing maxim is: **assimilation observes the toolchain; launch executes
the banked observation; lifecycle rows report what happened.**

This spec is the smallest 0.2 answer to the incident captured in
`art_b6e6f04a`, SHA-256
`afd148ada1c50a6282e849b05fabc3752ea565ebd47c265354e9a13da5288e60`:
the installed Codex adapter is a `#!/usr/bin/env node` program;
`PATH=/usr/local/bin:/usr/bin:/bin` cannot launch it; adding
`/home/mike/.local/bin` resolves `/home/mike/.local/bin/node` and initializes
the same adapter.

## Non-Goals

- Do not change the accepted per-turn ACP lifecycle trace, its event vocabulary,
  its read surface, or commit `c97c034`.
- Do not port `5ae9f10`, create `host_toolchain_dirs`, or add an admin verb that
  writes arbitrary directories or `PATH` text.
- Do not make the gateway discover or infer a host toolchain at boot or launch.
- Do not install Node, npm, rsync, a vendor harness CLI, or credentials.
  Assimilation continues to install only Tightbeam-owned plumbing.
- Do not define a general command-shell, build-toolchain, workdir, or agent-tool
  environment. This contract governs ACP adapter launch and its child harness
  CLI only.
- Do not add routing, failover, host selection, remediation, retry, or
  credential policy.
- Do not store inherited environment variables, credentials, provider frames,
  prompt text, assistant text, or tool arguments in provisioning or launch
  evidence.
- Do not change adapter package versions, harness selection, model selection,
  turn ordering, or ACP result semantics after adapter connection.
- Do not port this mechanism to a 0.1 maintenance line.

## Terms

- **Provisioning fact manifest** — versioned JSON stored on the existing host
  registration by a successful assimilation. It records the target host's
  observed absolute Node path, Node version, and absolute CLI path for each
  harness selected by that assimilation.
- **Executable fact** — one absolute executable lookup path returned by the
  existing non-login preflight. The stored path is the exact pathname launch
  invokes; assimilation does not dereference a symbolic link. It is an
  observation, not operator-authored policy.
- **Runtime seed** — the optional target-host absolute Node path supplied to
  `tightbeam assimilate --node`. It lets the non-login preflight reach and
  verify a runtime outside its inherited `PATH`; it is not a stored `PATH` or a
  gateway launch override.
- **Fact digest** — lowercase SHA-256 of the manifest's canonical JSON bytes,
  encoded by A-1's exact rule.
- **Banked launch plan** — the fact digest, absolute Node executable, absolute
  adapter script, and exact child `PATH` copied into durable launch context in
  the same transaction that opens the harness-process launch row.
- **Deterministic child `PATH`** — the exact colon-separated path derived by
  this spec. It contains no bytes from the gateway process's inherited `PATH`.
- **Launch outcome** — the state and `lastError` already owned by the
  `harness_processes` row. This spec does not create a second lifecycle state
  machine.
- **Legacy host row** — a host registration whose provisioning manifest is
  absent because it predates this schema. It remains readable and cannot launch
  an ACP adapter until assimilation replaces it.
- **Assimilation** — the existing `tightbeam assimilate` ceremony. Its
  read-only preflight observes the target through the same non-login boundary
  used for remote operation; its final `register-host` dispatch is the sole
  mutation seam for provisioning facts.

## Assumptions

1. `cli/src/preflight.rs` already observes `node`, `npm`, `rsync`, and each
   selected harness CLI with `command -v` without sourcing a login profile.
2. The installed Codex and Claude ACP adapters for this release are Node
   programs reached through absolute scripts beneath the registered
   `adapterBinDir`. The real Codex capture in `art_b6e6f04a` resolves
   `codex-acp` to
   `/home/mike/.tightbeam/adapters/node_modules/@agentclientprotocol/codex-acp/dist/index.js`
   with `#!/usr/bin/env node`.
3. A registered host already carries `baseDir`, `cliBin`, and
   `adapterBinDir`. Current Placement stores `adapterBinDir` but does not use it
   to construct the launch `PATH`. The gateway's real hostname remains the host
   key; the local host continues to use `ssh: nil` for transport.
4. `harness_processes` remains the single durable lifecycle truth for an OS
   harness process. Its existing `launching`, `running`, and terminal states
   remain authoritative.
5. The implementation base containing `c97c034` is stamped
   `coordination-fabric-v1-phase1-v5`. This spec introduces its exact successor.
6. The existing `tightbeam list` and `tightbeam harness-process list` commands
   are sufficient read surfaces; a new toolchain noun or read verb is not
   required.
7. The gateway host can be re-assimilated under its real hostname. Its
   persisted `ssh` and `baseDir` remain subordinate to boot-owned local values,
   while its persisted provisioning paths and fact manifest remain available
   to local launch.

## Invariants

Requirements use `R-` identifiers. Each points to its observable acceptance
case in the Acceptance section.

### R-1 — Launch does not inherit `PATH`

The launch planner constructs the ACP adapter's child `PATH` only from the
banked host-row fields and fixed system suffix in Architecture A-3. It reads no
`PATH` value from the gateway environment and emits no `$PATH` token.
`PATH` remains an existing reserved harness-overlay name, so an overlay cannot
replace the planner's bytes.

Acceptance: AC-2, AC-3, AC-7.

### R-2 — Assimilation is the fact mutation seam

A successful assimilation stores one complete provisioning fact manifest in
the same database transaction that creates or replaces the host registration.
A reassimilation replaces that manifest as a whole. No other verb writes or
patches executable facts.

Acceptance: AC-1, AC-4, AC-8.

### R-3 — Facts are observed and structurally valid

The CLI obtains each executable path from the existing non-login preflight,
optionally seeded with A-2's one absolute Node path.
The gateway accepts a manifest only when its version, cause, principal,
timestamp, platform, Node fact, selected-harness facts, registered `cliBin`,
and registered `adapterBinDir` match A-1. Each path is absolute, nonempty, and
contains no NUL, carriage return, line feed, or colon. The gateway recomputes
the fact digest from canonical JSON.

Acceptance: AC-1, AC-4.

### R-4 — The banked runtime is the executable

For a Node-backed adapter, the target command is the banked absolute Node path
followed by the absolute adapter script path. The command does not invoke the
adapter script through its `env node` shebang. The deterministic child `PATH`
still reaches the org CLI, the selected vendor CLI, and fixed system tools.

Acceptance: AC-2, AC-3, AC-7.

### R-5 — Planning is transactionally pinned; execution is observed

The host-row read of manifest, digest, `cliBin`, and `adapterBinDir`, plus the
harness-process launch-row and launch-context inserts, are one database
transaction. Reassimilation after that commit affects the next launch, not the
banked plan. OS process execution occurs after the transaction and is not
claimed atomic with it. Its observed result settles the existing launch row.

Acceptance: AC-5, AC-6.

### R-6 — Unknown or unusable facts refuse loudly

An absent manifest, invalid digest or shape, unsupported manifest version, or
missing selected-harness fact prevents the adapter process from opening. The
caller receives one of the named codes in A-4, the refusal names the host and
repair command, and the launch row reaches existing terminal state `exited`
with nonnull `resolvedAt` and the same code in `lastError`. A banked executable
or adapter script that has disappeared is an attempted OS launch with a normal
loud lifecycle failure; it does not cause launch-time tool discovery.

Acceptance: AC-4, AC-6.

### R-7 — Launch evidence has cause and principal

Each new launch-context row carries the banked fact digest, runtime executable,
adapter script, deterministic child `PATH`, typed cause, and principal.
Missing-fact refusals carry null plan fields plus cause and principal. Joining
that context to the existing harness-process row yields the resolved executable
and current or terminal lifecycle outcome without inference.

Acceptance: AC-5, AC-6, AC-9.

### R-8 — Local and remote launches use one plan

The same manifest validation, path construction, launch-context write, and
command tail apply to local and SSH-wrapped adapters. Transport adds its
existing SSH prefix and POSIX argument encoding only. Remote launch does not
append the remote shell's `$PATH`; local launch does not append the gateway's
`PATH`.

Acceptance: AC-2, AC-7.

### R-9 — Failure does not trigger inference or repair

The gateway executes only the banked paths. After a fact refusal, it leaves the
host row unchanged and tells the operator to re-run assimilation for that
host. After an OS or remote launch failure, it leaves the host row unchanged
and preserves the existing lifecycle failure policy.

Acceptance: AC-4, AC-6.

### R-10 — Turn behavior and trace remain unchanged

This feature changes adapter process construction and evidence only. It does
not add, remove, reorder, or reinterpret any turn-lifecycle event or change the
accepted `turn-trace` contract. The implementation remains a descendant of the
immutable repository object `c97c034d13ffdac99ce0df230bcf70edab4e80cf`.
It may edit a file that object also touched only for this independent launch
feature; no such hunk may alter the accepted event vocabulary, ordering,
privacy, or read behavior.

Acceptance: AC-10, AC-11.

### R-11 — Schema shape is explicit

Fresh databases receive A-5's complete schema and stamp. Only the exact v5
predecessor migrates. An absent or other stamp refuses before feature DDL. No
legacy fact is inferred from a service environment or filesystem.

Acceptance: AC-8.

### R-12 — Evidence is allowlisted

Fields introduced by this spec contain only A-1 and A-4 material. They exclude
raw environment maps, credentials, prompt or response content, tool arguments,
provider frames, and stderr. Existing `harness_processes.lastError` keeps its
existing purpose; this feature writes a named fact code or OS/remote-exit
reason rather than captured raw stderr.

Acceptance: AC-9.

## Architecture

Architecture elements use `A-` identifiers. Acceptance cases trace back to
both requirements and elements.

### A-1 — Host provisioning fact manifest

Extend the existing `hosts` row with one nullable canonical JSON manifest and
its digest. The manifest is not a second host registry. It is the
assimilation-produced capability observation attached to the existing
addressing row.

Version 1 has this exact logical shape:

```json
{
  "v": 1,
  "cause": "assimilate",
  "principal": "user:mike",
  "observedAt": 1787629180000,
  "platform": "Linux x86_64",
  "adapterRuntime": {
    "name": "node",
    "path": "/home/mike/.local/bin/node",
    "version": "v24.18.0"
  },
  "harnessCliPaths": {
    "claude": "/home/mike/.local/bin/claude",
    "codex": "/home/mike/.local/bin/codex"
  }
}
```

Rules:

1. `v` is the integer `1`.
2. `cause` is the literal `assimilate`.
3. `principal` is the authenticated principal that dispatches
   `register-host`; the gateway refuses a caller-supplied different value.
4. `observedAt` is the CLI's epoch-ms preflight observation time.
5. `platform` is the preflight's nonempty `uname -sm` value.
6. `adapterRuntime.name` is `node`.
7. `adapterRuntime.path` is the exact absolute path observed by
   `command -v node`. The CLI does not replace that path with a dereferenced
   symbolic-link target.
8. `adapterRuntime.version` is the trimmed first nonempty stdout line from
   executing that absolute path with `--version`; a nonzero or empty result
   fails assimilation before registration.
9. `harnessCliPaths` contains exactly the harnesses selected by this
   assimilation. Each value is the absolute path observed for that harness's
   catalog-declared CLI binary.
10. Each string is valid UTF-8 and contains no NUL, carriage return, or line
    feed. Each executable path and the registered `cliBin` and `adapterBinDir`
    is absolute, nonempty, and contains no colon. Harness keys are current
    catalog wire names.
11. Canonical JSON is the RFC 8785 JSON Canonicalization Scheme. The manifest
    contains no floating-point value, and `observedAt` is within JSON's exact
    integer range.
12. The gateway validates the fields and computes the SHA-256 over those exact
    canonical bytes; it does not trust a caller-supplied digest.

The CLI may continue to probe npm and rsync because assimilation uses them.
They are not adapter-launch facts and do not enter this manifest.

### A-2 — One mutation seam

`tightbeam assimilate` keeps its existing order: read-only preflight, directory
and adapter provisioning, CLI delivery when compatible, then `register-host`.
It adds one optional input, `--node <target-absolute-path>`.

When `--node` is absent, the preflight keeps its current non-login lookup. When
it is present, the CLI requires an absolute path whose basename is `node`,
applies A-1's string and path constraints before remote use, quotes it as one
remote argument, verifies that exact target-host file is executable, and
executes it with `--version`. The CLI prepends only the path's parent directory
to the unchanged non-login `PATH` for the preflight and the remaining
assimilation commands. It then requires `command -v node` to return the
supplied path and records that observation. It does not source a profile,
accept raw `PATH` text, or retain the inherited preflight `PATH`.

This seed lets the Gibson ceremony name
`/home/mike/.local/bin/node`; its parent also makes the colocated npm and vendor
CLIs visible to existing preflight checks. If another prerequisite remains
absent, assimilation keeps its existing named refusal. A missing unseeded Node
refusal also names `--node <target-absolute-path>` as the alternative to host
provisioning. This contract does not add a general executable map.

The final dispatch adds the A-1 manifest. The gateway upserts addressing and
the manifest atomically. `--dry-run` runs the read-only verification and
displays the observation fields, but labels authenticated principal and digest
as pending registration; it writes no row. A local-host registration retains
the fact manifest even though local transport remains the boot-owned `ssh: nil`
entry.

Reassimilation is replacement, not patching. It is the repair for a missing,
stale, or changed fact. There is no `host-toolchain-set` successor.

When Placement projects the gateway host, boot-owned `baseDir` and `ssh: nil`
remain authoritative. The database row with the same real hostname supplies
only its persisted `cliBin`, `adapterBinDir`, `provisioningFacts`, and
`provisioningFactDigest`. The boot projection cannot hide those provisioning
fields, and the database row cannot replace local transport or `baseDir`.

### A-3 — Deterministic launch plan

The planner derives these bytes from one banked host-row version:

1. `runtimeExecutable` = `adapterRuntime.path`.
2. `adapterScript` = the absolute adapter script for the selected harness under
   the existing registered `adapterBinDir`. No second adapter-location field is
   added to the provisioning manifest.
3. `toolchainPath` = the colon join of this ordered list after dropping empty
   entries and later duplicates:
   1. directory of `runtimeExecutable`;
   2. registered `cliBin`;
   3. directory of the selected harness's `harnessCliPaths` value;
   4. `/usr/local/bin`;
   5. `/usr/bin`;
   6. `/bin`.
4. Local command tail = `[runtimeExecutable, adapterScript]`.
5. Remote command tail = the same two entries after the existing SSH and
   `exec env` prefix.
6. The adapter environment carries `PATH=toolchainPath` plus the existing
   allowlisted launch environment. No inherited `PATH` bytes or `$PATH` token
   survive. The existing reserved-name validation continues to refuse `PATH`
   through `host-env-set`; the planner is the only writer of this environment
   key.

For a remote launch, the existing POSIX shell-argument encoder quotes each
planner-produced environment assignment, `runtimeExecutable`, and
`adapterScript` exactly once before SSH hands the command to the remote shell.
The context row stores the unquoted plan bytes. No executable-fact or derived
path byte is concatenated unquoted into remote command text.

The runtime directory comes first, so an executable with the same name in a
later directory cannot replace the banked Node. Calling the absolute Node path
makes the same guarantee at the process boundary rather than relying on PATH
search.

### A-4 — Durable launch context and named refusals

Add one one-to-one context table keyed by the existing `harness_processes`
launch id:

```sql
CREATE TABLE harness_process_launch_contexts (
  launchId              TEXT PRIMARY KEY REFERENCES harness_processes(launchId),
  provisioningFactDigest TEXT,
  runtimeExecutable     TEXT,
  adapterScript         TEXT,
  toolchainPath         TEXT,
  cause                 TEXT NOT NULL,
  principal             TEXT NOT NULL,
  CHECK (
    (provisioningFactDigest IS NULL AND runtimeExecutable IS NULL AND
     adapterScript IS NULL AND toolchainPath IS NULL)
    OR
    (provisioningFactDigest IS NOT NULL AND runtimeExecutable IS NOT NULL AND
     adapterScript IS NOT NULL AND toolchainPath IS NOT NULL)
  )
);
```

The context table records inputs. `harness_processes` remains the only owner of
lifecycle state and `lastError`. The planner inserts the launch row and context
row in one transaction before it opens a process.

For a valid plan, the context row carries the four plan fields. The launch then
uses those banked bytes. For a fact refusal, the context row carries null plan
fields, the launch row settles as `exited` with nonnull `resolvedAt`, and
`lastError` starts with exactly one code:

- `host_toolchain_facts_missing`
- `host_toolchain_facts_invalid`
- `host_toolchain_facts_unsupported`
- `host_toolchain_harness_missing`

The returned refusal has the same code and names the host. Fact-related
refusals end with:

`run tightbeam assimilate <ssh-dest> --name <host> and retry; if Node is outside the non-login PATH, add --node <target-absolute-path>`

The repair text uses the registered SSH destination when present. For the
gateway host it uses the real hostname as both target and `--name`.

Each context's `cause` is exactly one of:

- `adapter-checkout:<adapterKey>` for a first ordinary demand;
- `credential-activation:<adapterKey>:<credentialKind>` for a credential
  lifecycle start; or
- `adapter-restart:<adapterKey>:<generation>` for an automatic restart.

The launch principal is the literal `process:tightbeam` for each cause:
the shared adapter is an OS process opened by the coordinator, not a one-to-one
projection of the user or agent whose operation first demanded it. That
caller's own durable operation or turn row keeps its authenticated principal.
The implementation passes cause and launch principal through the single
launch-planning seam. It does not reconstruct either value from an error
string, timestamp, or later lifecycle state.

After a valid plan is banked, the launcher executes its absolute command
without a preliminary directory search, `command -v`, version probe, or
alternate-path check. An unavailable runtime or adapter script therefore keeps
the four plan fields and settles through the existing launch-failure lifecycle
with the OS or remote-exit error in `lastError`. Reassimilation is the only
fact repair.

### A-5 — Schema, stamp, and migration

The new shape is `coordination-fabric-v1-phase1-v6`.

Fresh schema:

- `hosts` gains nullable `provisioningFacts TEXT` and
  `provisioningFactDigest TEXT` columns.
- `harness_process_launch_contexts` has A-4's exact shape.
- The schema stamp is v6.

Upgrade posture:

1. Read and verify the current stamp before feature DDL.
2. In one database transaction, upgrade only exact
   `coordination-fabric-v1-phase1-v5` by adding the two nullable host columns,
   creating the launch-context table, and updating the stamp to v6.
3. Existing host rows retain null facts. Existing harness-process rows retain
   no context row. Reads expose those cases only through A-6's legacy
   representations: host provisioning status `missing` and null launch-context
   fields. No backfill inspects the gateway environment, host filesystem,
   stored DDL, or prior stderr.
4. An interrupted transaction leaves v5 and no partial feature schema. A retry
   performs the same exact upgrade.
5. An absent stamp or any stamp other than v5/v6 refuses before mutation and
   names the found and required shapes.
6. The accepted `turn_lifecycle_events` and `turn_lifecycle_epoch` tables from
   `c97c034` are not changed, rebuilt, or inferred.

Feature modules must not run `CREATE TABLE IF NOT EXISTS` against a stamped v5
database before the central shape check. Fresh creation and the one exact
migration pass through the central schema seam.

### A-6 — Existing CLI reads

`tightbeam list` adds this bounded object to each host:

```json
{
  "provisioning": {
    "status": "ready",
    "factDigest": "<sha256>",
    "observedAt": 1787629180000,
    "principal": "user:mike",
    "runtimeExecutable": "/home/mike/.local/bin/node",
    "runtimeVersion": "v24.18.0",
    "harnesses": ["claude", "codex"]
  }
}
```

A legacy row returns `{"provisioning":{"status":"missing"}}`.
An unreadable shape or digest mismatch returns `status: "invalid"`; an unknown
manifest version returns `status: "unsupported"`. Those two forms include the
matching A-4 code and no derived executable fields.

Exact examples are
`{"provisioning":{"status":"invalid","code":"host_toolchain_facts_invalid"}}`
and
`{"provisioning":{"status":"unsupported","code":"host_toolchain_facts_unsupported"}}`.
The ready form sorts `harnesses` by wire name.

`tightbeam harness-process list` left-joins A-4 and adds
`provisioningFactDigest`, `runtimeExecutable`, `adapterScript`,
`toolchainPath`, `launchCause`, and `launchPrincipal` to each row. A historical
row with no context returns these fields as null. The existing `state`,
timestamps, and `lastError` are the lifecycle outcome; no synthesized summary
field competes with them. Existing admin authorization stays unchanged.

The JSON rows retain the existing newest-first ordering.

### A-7 — Authority reconciliation and operating pattern

This spec narrows one older placement clause. `tightbeam.md` says the host
registry records addressing only and does not persist capability. F2 is the
newer, feature-specific authority: adapter executable observations now live in
the host's assimilation-produced provisioning manifest. The broader placement
rules remain: the manifest does not choose hosts, grant harness access, move
credentials, install vendor tools, or become policy.

This is not `5ae9f10` under another name:

- a fact is captured by assimilation, not authored through a setter;
- the manifest records absolute observed executables, not arbitrary
  directories;
- the planner reuses the existing registered `adapterBinDir` and reserved
  `PATH` overlay boundary;
- the launch banks one exact fact digest and uses the absolute runtime;
- the read surface shows fact provenance and launch outcome.

The operating pattern is therefore complete in existing commands: re-run
`assimilate` to replace facts; use `list` to inspect host readiness; use
`harness-process list` to inspect the actual launch plan and outcome. The CLI
refusal names that repair. No substrate-manual amendment is required for the
spec handoff; implementation updates the existing assimilation and
harness-process help text in the same change.

### A-8 — Subtraction ruling

ADD wins for one reason: deleting inherited `PATH` without a deterministic
replacement makes each Node-backed adapter unlaunchable, while accepting the
failure preserves the exact incident Mike directed the product to prevent.
The added mechanism is limited to one host-row manifest, one one-to-one launch
context, one planner, and two existing reads.

## Acceptance

Each acceptance case names the requirements and architecture it verifies.

### AC-1 — Real capture becomes the fixture floor

Traces: R-2, R-3; A-1, A-2.

Given the real Gibson capture `art_b6e6f04a` with source SHA-256
`afd148ada1c50a6282e849b05fabc3752ea565ebd47c265354e9a13da5288e60`,
when the implementer adds the launch fixture, then the fixture preserves these
captured observations rather than a hand-written ideal response:

- adapter path
  `/home/mike/.tightbeam/adapters/node_modules/.bin/codex-acp`;
- resolved script ending
  `@agentclientprotocol/codex-acp/dist/index.js`;
- shebang `#!/usr/bin/env node`;
- failing `PATH=/usr/local/bin:/usr/bin:/bin`;
- stderr containing `node` and `No such file or directory`;
- successful path containing `/home/mike/.local/bin`;
- resolved Node `/home/mike/.local/bin/node`.

The fixture records the source artifact id and SHA. Mechanical removal of
compiler warnings, ANSI bytes, and provider capability payload is documented;
the seven observations above remain byte-exact excerpts. A parser or command
builder test consumes the fixture. Merely checking the fixture into the tree
does not pass this case.

Given the fixture's failing system-only `PATH`, when assimilation preflight is
run with `--node /home/mike/.local/bin/node`, then it verifies that exact
executable, observes the same absolute Node path, and does not source a login
profile. The test fails if the CLI stores or forwards the inherited preflight
`PATH` as a host fact.

### AC-2 — Local plan is exact

Traces: R-1, R-4, R-8; A-3.

Given a local host fact with Node `/opt/node/bin/node`, `cliBin=/srv/tb/bin`,
`adapterBinDir=/srv/tb/adapters/node_modules/.bin`, Codex
`/opt/codex/bin/codex`, and Claude `/opt/claude/bin/claude`, when the planner
prepares Codex, then the command tail is exactly
`["/opt/node/bin/node", "/srv/tb/adapters/node_modules/.bin/codex-acp"]` and
`PATH` is exactly
`/opt/node/bin:/srv/tb/bin:/opt/codex/bin:/usr/local/bin:/usr/bin:/bin`.
The output contains neither the test process's sentinel `PATH` directory nor
`$PATH`.

### AC-3 — Gateway environment cannot change the plan

Traces: R-1, R-4; A-3.

Given the same stored host row in two fresh processes whose inherited `PATH`
values differ, when each plans the same adapter, then command tail,
`runtimeExecutable`, `toolchainPath`, and fact digest are byte-identical.

### AC-4 — Manifest validation and reassimilation

Traces: R-2, R-3, R-6, R-9; A-1, A-2, A-4.

Given manifests with a relative Node path, a colon in any executable,
`cliBin`, or `adapterBinDir`, an unsupported version, an omitted selected
harness, a digest mismatch, or a principal different from the authenticated
dispatcher, when registration is attempted, then the gateway refuses before
changing the prior host row and names the invalid field. Given a nonzero or
empty Node-version probe, when assimilation runs, then the CLI refuses before
registration. Given a later valid reassimilation, when registration commits,
then one host row contains only the new manifest and recomputed digest.

Given `--node` with a relative path, a basename other than `node`, a missing
target file, a non-executable target, a nonzero version result, or a
`command -v node` result different from the supplied path, when assimilation
runs, then it refuses before provisioning or registration and names the failed
check. Given executable Node, npm, Codex, and Claude files under
`/home/mike/.local/bin`, executable rsync at `/usr/bin/rsync`,
`--node /home/mike/.local/bin/node`, and a non-login `PATH` that omits the local
directory, when assimilation completes, then only the Node parent was
prepended during provisioning and the stored manifest contains the observed
absolute Node and harness paths rather than the inherited `PATH`.

Given that the supplied absolute Node path is a symbolic link whose executable
target returns a valid version, when `command -v node` returns the supplied
path, then assimilation and launch retain and invoke that supplied pathname.
Neither the manifest nor the launch context substitutes the dereferenced
target.

Given an admin attempts `host-env-set` with the name `PATH`, when existing
reserved-name validation runs, then it refuses and the stored manifest and
banked launch plan remain unchanged.

Given a valid registration for the gateway's real hostname, when Placement
projects that host, then `ssh` is null, `baseDir` equals the boot configuration
even if the row differs, and `list` plus local launch use the persisted
`cliBin`, `adapterBinDir`, fact digest, and manifest.

Given an invalid digest or unsupported stored version, when `list` reads the
host, then its provisioning status and code match A-6 and it exposes no
derived executable fields.

### AC-5 — Fact read and launch context are one transaction

Traces: R-5, R-7; A-3, A-4.

Given host-row version `A`, when a launch-planning transaction begins and a
concurrent reassimilation commits host-row version `B`, then the launch row and
context contain either one complete A plan or one complete B plan. No row
combines a digest, runtime, `cliBin`, `adapterBinDir`, script, or `PATH` from
different host-row versions. The process uses the plan stored on its own
context row.

### AC-6 — Missing facts refuse; unavailable bytes fail loudly

Traces: R-5, R-6, R-7, R-9; A-4.

Given each fact refusal condition in A-4, when a launch is requested, then no
adapter target process opens, the caller receives the matching code, and
`harness-process list` shows one launch row with state `exited`, nonnull
`resolvedAt`, the same code in `lastError`, null plan fields, cause, and
principal.

Given a valid banked manifest whose absolute Node or adapter-script path no
longer exists, when launch executes, then no alternate-path or version probe
runs, the context retains the four plan fields, and the existing launch row
settles with the observed OS or remote-exit failure. The read names the exact
runtime that failed. A test fails if launch consults inherited `PATH`, invokes
`command -v`, searches a directory, or silently selects another executable.

### AC-7 — Remote launch uses the same tail and no remote `$PATH`

Traces: R-1, R-4, R-8; A-3.

Given the AC-2 facts on an SSH host, when the planner prepares Codex, then the
existing SSH prefix is followed by `exec env`, the exact deterministic `PATH`,
the same absolute Node path, and the same absolute adapter script. No command
argument contains `$PATH`. A captured command test breaks if the remote branch
returns to `cliBin:$PATH`.

Given valid runtime, CLI, and adapter paths containing a space and a single
quote, when the remote command passes through a real POSIX-shell parsing
fixture, then the parsed `PATH`, Node argv entry, and adapter-script argv entry
are byte-identical to the banked plan. The test fails if a plan value splits
into multiple arguments or any of its bytes execute as shell syntax.

### AC-8 — Fresh shape and exact v5 migration

Traces: R-2, R-11; A-5.

Given an empty database, when schema creation completes, then the host fact
columns, launch-context table, and v6 stamp exist. Given an exact v5 database
with host rows, harness-process history, and the `c97c034` turn-trace tables,
when migration completes, then preexisting row values remain, host facts are
null, historical launch contexts are absent, turn-trace schema and rows are
unchanged, and the stamp is v6. Given interruption after each DDL step, when
the transaction aborts, then the database remains exact v5 and a retry passes.
Given an absent or other stamp, boot refuses before feature DDL and names that
there is no migration.

### AC-9 — Reads expose only allowlisted evidence

Traces: R-7, R-12; A-4, A-6.

Given one successful launch, one fact refusal, and one historical launch, when
an admin runs `list` and `harness-process list`, then their JSON shapes match
A-6, order is deterministic, and the historical fields are null rather than
invented. Searches over stored manifests, contexts, and CLI output find no
credential, prompt, assistant text, tool argument, provider frame, or unrelated
environment variable.

### AC-10 — Existing turn trace is unchanged

Traces: R-10; A-5, A-7.

Given the complete `c97c034` focused lifecycle, connection, adapter, ledger,
lane, gateway, privacy, restart, and race tests, when this feature is applied,
then those tests pass without weakening an assertion or changing an expected
event sequence. A diff from
`c97c034d13ffdac99ce0df230bcf70edab4e80cf` classifies each overlapping hunk;
each has a launch-only purpose and preserves the accepted turn-trace event
vocabulary, ordering, privacy, and read behavior.

### AC-11 — Real fresh-org smoke proves the prevention

Traces: R-10; A-1 through A-7.

Given a fresh v6 org on Gibson whose gateway process `PATH` excludes
`/home/mike/.local/bin`, valid Codex and Claude credentials, and executable
Node, npm, Codex, and Claude files in that omitted directory plus rsync at
`/usr/bin/rsync`, when
`assimilate --node /home/mike/.local/bin/node` installs the adapters and records
that absolute executable, then one real Codex turn and one real Claude turn
complete through the real ACP adapters. `harness-process list` shows the same
resolved Node path and fact digest for each launch plus its lifecycle state.
`turn-trace` shows the accepted unchanged event contract for each turn. The
smoke then restarts the fresh gateway and proves the facts and launch evidence
remain readable.

A missing credential or unavailable real harness is a named incomplete smoke,
not a pass. A mock, fixture-only run, inherited login `PATH`, temporary symlink,
manual environment override, or edit to a service unit does not satisfy this
case. Here, `temporary symlink` means a shim introduced for the smoke; the
persisted package-manager Node symlink allowed by A-1 and AC-4 is valid.

### AC-12 — Repository gates and review handoff

Traces: R-1 through R-12; A-1 through A-8.

Given a clean worktree from a proven-green current main, when implementation is
complete, then the implementer records baseline and after counts for the
CI-defined Mix and Rust gates, runs the real AC-11 smoke, freezes one clean
commit, and obtains one independent exact-commit review before merge. The
review checks this complete acceptance matrix and the no-`host_toolchain_dirs`
constraint.

## Open Questions

None. There are no blocking or non-blocking open questions for the MVP.

The load-bearing choices are ruled by current authority: assimilation facts
replace a setter registry; absolute Node execution plus a deterministic child
`PATH` replaces inheritance; the existing harness-process row remains the
lifecycle truth; exact v5 is the only migration source; and `c97c034` remains
unchanged.
