# Bug B F5 amendment: OS-verifiable process-birth identity

Status: READY FOR ONE INDEPENDENT CROSS-HARNESS SPEC REVIEW

Date: 2026-08-18 UTC

Work item: `wi_2342b1ae-3374-40a1-9034-f0b32bbcad38`

Producer assignment: `asg_485a757e-69bb-45d9-bbf4-97cda07d2d94`

Source line: MAIN only

Exact intermediate source: `origin/coder/wi-2342b1ae-bugb-main` at
`1ae81e619452963fe2ffcf96791d2085cdb311f9`

## Authority and amendment boundary

This file amends only Bug B finding F5 in `art_6817803a`, SHA-256
`a8fc963dd141721df2253a52644a60da7f9ef8792579518f7d65a3377829a990`.
It supersedes the four-field identity proof in revision 6 sections B2, B3, B4, B5,
B7, Architecture, Release-line fix plan, and review question 4 only where those
clauses authorize a process-group signal or classify a live process.

The review verdict is `att_c36308f5-7989-492e-86dd-58a3f3abd0ae`.
The controlling F5 ruling is `att_ed7f4892-b226-4dbe-a621-dcc20d617c40`.
The slice-order ruling is `att_ef5f0a1d-7e39-4285-b897-27d0036625fd`.
The intermediate-base gate is `att_0246dcb8-6e25-43ed-a0b5-f19c3e7f1353`.
The intermediate-base readiness record is `att_3a35adbe-4ef6-4eaa-a24f-1e866ef0c249`.

`art_1bdd00f8` remains historical provenance. Its registry SHA is
`31cd14a3fa47989c934bd2138c29ea812fc39c6e13d1be9f0d7f7ccf8f62e905`.
Its bytes and origin path are absent. Owner adjudication forbids consuming or
reconstructing that report. This amendment uses the gate, readiness record, exact Git
object, and controlling rulings instead.

This amendment preserves F1, F2, F3, F4, F6, and F7. It preserves the revision 6
non-goals, authority model, process states, stop causes, lease checks, launch barrier,
retirement fence, finalizer, credential boundary, and unresolved-state repair rules.
It authorizes no source edit, implementation assignment, merge, deployment, restart,
runtime mutation, credential access, or process signal.

## Goal

The managed-process boundary must distinguish the process that Tightbeam launched from
a later process that reused the same PID or process-group ID during the same boot.

The launch broker must capture an OS-verifiable birth identity before it releases the
workload. The broker must store the same typed birth identity in the managed-process row
and its durable evidence file. The physical worker must read the current OS birth
identity immediately before it classifies or signals the process group.

The worker must return `identity_unknown` without a signal when the proof is missing,
unreadable, malformed, mismatched, stale, or unsupported.

## Non-Goals

- This amendment does not change process ownership or authorization.
- It does not add a new public process verb.
- It does not remove `process-stop`, lease-expiry stop, or retirement stop.
- It does not authorize PID-only, PGID-only, command-line, executable-name, or artifact-only proof.
- It does not add Windows process custody.
- It does not extend custody to unmanaged ACP descendants.
- It does not change F2 spawn and exit reporting.
- It does not change F3 sweep ownership or boot scheduling.
- It does not infer a birth identity for a row created by the revision 6 intermediate source.
- It does not migrate a production database from the non-landable intermediate branch.
- It does not store a credential, device code, raw argument vector, or raw environment value.
- It does not parse an error message, command description, or other prose as identity evidence.
- It does not change the source-line election or authorize a cross-line cherry-pick.

## Terms

### Process-birth identity

A **process-birth identity** is the closed tuple
`{birthKind, birthPrimary, birthSecondary}` for the process-group leader.
The process-group leader has `osPid == processGroupId` at bind time.

The allowed kinds are:

- `linux_proc_stat_starttime_v1`: `birthPrimary` is unsigned field 22 from
  `/proc/<pid>/stat`. `birthSecondary` is `0`.
- `darwin_proc_bsd_starttime_v1`: `birthPrimary` is
  `proc_bsdinfo.pbi_start_tvsec`. `birthSecondary` is
  `proc_bsdinfo.pbi_start_tvusec`.

The kind is part of the identity. The worker does not convert one kind into another.

### Full process identity

The **full process identity** is:

```text
processId, osPid, processGroupId, bootIdentity, launchToken,
identityProofVersion, birthKind, birthPrimary, birthSecondary
```

`identityProofVersion` is `2` for the identity defined by this amendment.
The row, broker evidence, and current OS observation must agree on each applicable
field before the worker returns `present` or sends a group signal.

### Broker evidence version 2

The **broker evidence version 2** record is one exact tab-separated record:

```text
2<TAB>processId<TAB>osPid<TAB>processGroupId<TAB>bootIdentity<TAB>launchToken<TAB>birthKind<TAB>birthPrimary<TAB>birthSecondary<LF>
```

The parser accepts nine fields after trimming one final line ending. It accepts no
extra field and no missing field. It parses the version, PID, PGID, and birth values as
typed integers. It compares strings as exact bytes. A version 1 five-field record is
legacy evidence, not process proof.

### Current OS observation

A **current OS observation** is one of four typed results:

- `matched`: the OS returned the stored leader PID, stored PGID, and stored birth identity.
- `absent`: the leader PID and process group are both absent on the stored boot.
- `mismatch`: the numeric PID or PGID exists, but the OS birth identity or group relation differs.
- `unavailable`: the platform query, permission check, parser, or required evidence could not answer.

The worker maps `mismatch` and `unavailable` to `identity_unknown`. It sends no signal
for either result. The worker may map `absent` to the existing proven-exit path.

### Signal attempt

A **signal attempt** is one invocation of the physical custody worker for one row
revision and one signal. The worker reads the evidence, reads the OS birth identity,
compares the full tuple, and calls `killpg` in that order. The worker performs no wait,
database call, filesystem read, child spawn, or caller callback between the final OS
read and `killpg`.

### Legacy row

A **legacy row** is a managed-process row without `identityProofVersion=2` and the three
birth fields. The worker may prove that the old process is absent. The worker cannot use
the row to authorize a signal or a `present` result.

## Assumptions

- The launch barrier holds the child before `exec` until the gateway grants release.
- The launch broker can query the group leader after both sides complete `setpgid`.
- Linux exposes process start time in `/proc/<pid>/stat` field 22 as clock ticks after boot.
- Darwin exposes process start time through `proc_pidinfo` with `PROC_PIDTBSDINFO` and
  `proc_bsdinfo.pbi_start_tvsec` plus `pbi_start_tvusec`.
- The existing boot identity remains available on Linux and Darwin.
- SQLite remains the transaction owner for the managed-process row.
- The broker can create a new mode-0600 evidence file and synchronize its bytes before bind.
- The gateway invokes the custody worker on the host named by the managed-process row.
- The exact intermediate branch is non-landable and has not entered MAIN.

The Linux authority is the Linux man-pages definition of `/proc/<pid>/stat` field 22:
https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html

The Darwin authority is Apple's XNU `proc_bsdinfo` definition:
https://github.com/apple-oss-distributions/xnu/blob/main/bsd/sys/proc_info.h

## Invariants

### F5-I1 — Release proof

The broker opens the launch barrier only after the gateway commits
`identityProofVersion=2` and the birth tuple on the row.

The broker opens the barrier only after the bind reply returns the same row revision,
`identityProofVersion=2`, and the same birth tuple.

### F5-I2 — Dual durable evidence

The broker evidence and managed-process row contain the same full process identity
before release.

### F5-I3 — Live OS proof

The custody worker returns `present` only after the current OS observation is `matched`.

The custody worker calls `killpg` only after the current OS observation is `matched` in
that signal attempt.

### F5-I4 — Fail-closed result

The custody worker returns `identity_unknown` for `mismatch`.

The custody worker returns `identity_unknown` for `unavailable`.

The gateway records `identity_unknown` with a typed uncertainty cause and preserves the
existing stop cause.

### F5-I5 — Legacy compatibility

The custody worker treats a revision 6 evidence record as `unavailable`.

The gateway refuses release when `process-bind` omits the version 2 birth fields.

### F5-I6 — Restart behavior

Boot recovery reads the same full identity and uses the same OS observer as
`process-reconcile` and `process-stop`.

### F5-I7 — Existing stop capability

A matched version 2 identity remains eligible for the existing TERM-then-KILL group stop.

The existing stop causes and stop-attempt count remain unchanged.

### F5-I8 — Evidence is data

The bind request, managed row, broker evidence, helper input, and helper output use typed
fields or closed enum values. No component derives identity from prose.

## Architecture

### A. Capture and release order

The launch broker performs this sequence for each new managed process:

1. The gateway inserts `preparing` with a unique launch token.
2. The broker creates the closed pre-exec barrier.
3. The broker spawns the child.
4. The child and broker set `pgid=pid` before the child waits on the barrier.
5. The broker verifies `getpgid(pid) == pid`.
6. The broker reads the process-birth identity from the OS.
7. The broker writes broker evidence version 2 with mode `0600` and `create_new`.
8. The broker synchronizes the evidence bytes before it sends `process-bind`.
9. The bind transaction stores the full identity and applies the existing generation,
   lease, deadline, revision, and stop-cause checks.
10. The gateway returns `release=true`, the exact row revision, proof version, and birth tuple
    only for the existing lawful `running` result.
11. The broker compares the reply to the captured tuple.
12. The broker opens the barrier only when the reply matches.

An OS read failure at step 6 leaves the barrier closed. An evidence write or sync failure
at steps 7 or 8 leaves the barrier closed. A bind refusal or reply mismatch at steps 9
through 11 leaves the barrier closed.

### B. Platform birth authorities

#### Linux

The observer reads `/proc/<pid>/stat`. It parses the record as procfs data and reads
field 5 (`pgrp`) plus field 22 (`starttime`). It verifies that field 1 equals the
requested PID and field 5 equals the requested PGID. It records field 22 without
converting clock ticks to wall time.

The parser must handle a `comm` field that contains spaces or right parentheses. A
short record, numeric overflow, zero start time, permission refusal, read error, or
parse ambiguity returns `unavailable`.

#### Darwin

The observer calls `proc_pidinfo(pid, PROC_PIDTBSDINFO, 0, ...)`. It requires a return
size equal to `sizeof(struct proc_bsdinfo)`. It verifies `pbi_pid == pid` and
`pbi_pgid == pgid`. It records `pbi_start_tvsec` and `pbi_start_tvusec` separately.

A short result, invalid microsecond value, permission refusal, syscall error, PID
mismatch, or PGID mismatch returns `unavailable` or `mismatch` according to the current
OS observation definitions.

### C. Managed-process schema

The pending MAIN table adds these nullable bind-time columns:

```text
identityProofVersion INTEGER
birthKind            TEXT
birthPrimary         INTEGER
birthSecondary       INTEGER
```

The table accepts `identityProofVersion` only as `2`. It accepts `birthKind` only as
`linux_proc_stat_starttime_v1` or `darwin_proc_bsd_starttime_v1`. Linux rows require
`birthSecondary=0`. Darwin rows require `0 <= birthSecondary < 1000000`.

The table requires the original identity fields, `brokerIdentity`, proof version, and
three birth fields for `running` and `stop_requested`. A row binds the original and new
identity fields in one revision compare-and-set.

The managed-process projection returns `identityProofVersion` and `birthKind`. It does
not return `birthPrimary`, `birthSecondary`, `launchToken`, or broker evidence bytes to
an ordinary caller.

The uncertainty-cause set adds:

- `process_birth_identity_missing`;
- `process_birth_identity_mismatch`;
- `process_birth_identity_unavailable`.

### D. Schema and compatibility migration

The intermediate branch is non-landable. MAIN does not contain `managed_processes`.
The implementation therefore changes the pending table definition before the combined
source enters MAIN. It does not add an in-place production schema migration.

A database created by the intermediate branch has an unauthorized candidate table
shape. Schema activation refuses that shape with
`incompatible_managed_process_birth_identity_v1`. It does not inspect live PIDs, rewrite
rows, add columns opportunistically, or backfill a birth identity.

The version 2 reader recognizes the version 1 evidence shape only to return
`identity_unknown` with `process_birth_identity_missing`. It does not copy current OS
values into the row as historical launch evidence.

Mixed-version behavior is closed:

- A new gateway rejects an old broker bind that omits version 2 fields and returns
  `release=false` with `process_birth_identity_required`.
- A new broker rejects a bind reply that omits `identityProofVersion=2` or returns a
  different birth tuple. It keeps the barrier closed.
- A new custody worker returns `identity_unknown` for a version 1 evidence file.
- An old custody worker rejects the nine-field version 2 evidence file by arity and
  therefore sends no signal.
- A rollback to the pre-F5 intermediate helper cannot use version 2 evidence to signal.

### E. Stop and reconcile decision order

The physical worker uses this order for `probe` and for each TERM or KILL signal:

1. Parse the expected full identity from typed helper arguments.
2. Read broker evidence version 2.
3. Compare the evidence with the row tuple.
4. Compare the stored boot identity with the current boot.
5. Read the current OS birth identity and current PGID.
6. Return the typed observation.
7. For `matched`, perform the requested probe or signal.
8. For `absent`, return the existing proven-absence result.
9. For `mismatch` or `unavailable`, return `identity_unknown` without a signal.

The worker repeats steps 4 through 6 immediately before SIGKILL after the TERM grace
period. A TERM match does not authorize a later KILL without a second OS read.

The gateway attaches the row revision to each worker result. The existing revision
compare-and-set rejects a result gathered for an older row revision.

### F. PID and PGID reuse

A row and broker file that agree on PID, PGID, boot identity, and launch token do not
prove the current OS process. The final OS birth read supplies that proof.

When the OS returns the same PID or PGID with another birth identity, the worker returns
`identity_unknown`. The foreign group receives no signal. Retirement remains blocked
and names `process-reconcile`.

### G. Leader and broker exit

When the leader PID and process group are both absent on the stored boot, reconciliation
may record the existing proven-exit result.

When the leader PID is absent but the process group still exists, reconciliation records
`identity_unknown` with `process_birth_identity_unavailable`. The worker sends no group
signal because no current leader birth identity exists to authorize the numeric PGID.

When the leader PID now names another birth identity, reconciliation records
`identity_unknown` with `process_birth_identity_mismatch`.

A broker exit after the evidence and row commit does not erase proof. The durable file,
row, and current OS read remain required. A missing broker file returns
`identity_unknown`.

A broker exit before evidence sync or bind leaves the barrier closed. Recovery proves
absence or records `identity_unknown`; it does not infer that the workload ran.

### H. Crash and restart ordering

| Crash point | Required restart result |
|---|---|
| Before birth capture | The barrier remains closed. The row remains unresolved until broker proof or deadline reconciliation. |
| After capture, before evidence sync | The barrier remains closed. Recovery treats missing durable evidence as unavailable. |
| After evidence sync, before bind commit | Recovery compares the version 2 file, row token, OS birth identity, lease, session generation, and deadline before any bind decision. |
| After bind commit, before barrier release | Recovery may observe the child or prove its exit. It does not infer that the workload executed. |
| After barrier release, before broker reply handling | The committed `running` row and full identity remain authoritative. |
| After TERM, before stop outcome commit | Retry rereads the OS birth identity before another signal and uses the existing stop attempt semantics. |
| During TERM grace | The KILL phase performs a new birth read. A mismatch yields `identity_unknown` and no KILL. |
| During reconcile, before row compare-and-set | The evidence revision loses when another transition changed the row. |
| Gateway restart | Boot recovery uses the same version 2 observer and decision table as the public repair verb. |

### I. Source and path census

The census compares MAIN base `a18d8b307ef10788d5113cbf0bd148f6613c2534` with
the exact intermediate tip `1ae81e619452963fe2ffcf96791d2085cdb311f9`.
The branch changes 26 paths. F5 implementation is bounded to the following expected
seams. The implementation producer must recensus the combined tip before editing.

| Path | F5 responsibility |
|---|---|
| `cli/src/process_birth.rs` | New single Linux and Darwin birth observer with typed results. |
| `cli/src/main.rs` | Register the internal birth module if Rust module layout requires it. |
| `cli/src/ceremonies.rs` | Capture birth before release, write version 2 evidence, send version 2 bind, and verify the bind reply. |
| `cli/src/process_custody.rs` | Compare row, evidence, boot, and current OS birth identity before probe, TERM, and KILL. |
| `cli/src/dispatch.rs` | Add typed version and birth fields to `process-bind`. |
| `lib/tightbeam/managed_processes.ex` | Add columns, checks, tuple binding, uncertainty causes, row mapping, and revision rules. |
| `lib/tightbeam/gateway.ex` | Validate bind fields, pass full helper arguments, map typed outcomes, and preserve revision checks. |
| `lib/tightbeam/wire/router.ex` | Normalize the new internal bind fields. |
| `lib/tightbeam/wire/payloads.ex` | Return safe proof metadata without secret identity values. |
| `lib/tightbeam/schema.ex` | Refuse the unauthorized intermediate table shape with the named compatibility error. |
| `lib/tightbeam/boot.ex` | Keep boot recovery on the shared version 2 reconciliation path. |
| `test/managed_processes_test.exs` | Verify schema checks, bind atomicity, uncertainty causes, and legacy refusal. |
| `test/custody_ceremony_f6_test.exs` | Verify capture-before-release and row/evidence/OS equality with real children. |
| `test/boot_test.exs` | Verify restart cases and legacy rows. |
| `test/router_test.exs` | Verify internal bind validation and safe projections. |
| `test/schema_shape_test.exs` | Verify the version 2 table and named version 1 refusal. |
| `test/cli_integration_test.exs` | Verify mixed helper and bind versions fail closed. |

`cli/src/child_process.rs` remains the authority for the existing TERM-then-KILL timing
and non-reaping in-process child rules. `cli/src/harness_process.rs` remains the boot
identity authority. This amendment requires no behavior change in either file unless the
implementation review proves that extracting shared code is necessary. Such an
extraction must preserve byte-equivalent behavior outside managed-process F5.

The remaining changed paths at the exact intermediate tip carry F1, F2, F3, F4, F6,
F7, retirement, routing, or test support. F5 does not authorize changes to them.

### J. Requirement trace

| Requirement | Primary implementation seam | Acceptance cases |
|---|---|---|
| F5-I1 | `ceremonies.rs`, `gateway.ex`, `managed_processes.ex` | A1, A2, A8 |
| F5-I2 | `ceremonies.rs`, `managed_processes.ex` | A1, A2, A3 |
| F5-I3 | `process_birth.rs`, `process_custody.rs` | A4, A5, A6, A7 |
| F5-I4 | `process_custody.rs`, `gateway.ex`, `managed_processes.ex` | A5, A6, A7, A9 |
| F5-I5 | schema, bind, and helper compatibility seams | A10, A11 |
| F5-I6 | `boot.ex`, `gateway.ex` | A12, A13 |
| F5-I7 | existing stop worker plus version 2 proof | A4, A14 |
| F5-I8 | wire, row, evidence, and helper parsers | A3, A10, A15 |

## Acceptance

Each acceptance case uses an exact Given/When/Then result. Linux cases run on Linux.
Darwin cases run on Darwin. The final review requires evidence from both platforms.

### A1 — Linux capture before release

Given a real child held behind the launch barrier on Linux, when the broker binds it,
then the row and version 2 evidence contain the same field 22 start time. The workload
marker remains absent until the version 2 bind reply grants release.

### A2 — Darwin capture before release

Given a real child held behind the launch barrier on Darwin, when the broker binds it,
then the row and version 2 evidence contain the same `pbi_start_tvsec` and
`pbi_start_tvusec`. The workload marker remains absent until the version 2 bind reply
grants release.

### A3 — Evidence durability and shape

Given a bind-ready child, when the fixture pauses after evidence sync and before the bind
request, then a second process reads one complete nine-field mode-0600 record. A truncated,
extra-field, symlink, pre-existing, or unsynchronized record causes a bind refusal and no
workload release.

### A4 — Matched stop remains functional

Given a real process-group leader whose row, evidence, boot, and OS birth identity match,
when the owner runs `process-stop`, then the worker sends TERM to that group. If the group
survives the grace period with the same birth identity, the worker sends KILL. The final
row records the existing `killed`, `exited`, or `stop_failed` result.

### A5 — Deterministic same-boot reuse fixture

Given real foreign process group B, a row and evidence that name B's numeric PID and PGID,
and the stored birth identity from earlier process A on the same boot, when the fixture
releases the worker at its final OS-read seam, then the worker reads B's different birth
identity. It returns `identity_unknown`, records
`process_birth_identity_mismatch`, calls no signal syscall, and leaves B alive.

The fixture does not wait for the kernel to reuse a PID. It constructs the exact stale-row
state with a real foreign group and asserts both the typed result and the surviving process.

### A6 — Overlap before the final read

Given a worker paused after it validates matching row and broker evidence, when the fixture
changes the OS observer from A's birth identity to B's birth identity at the same numeric
identity, then the resumed worker performs the required final OS read. It returns
`identity_unknown`, calls no signal syscall, and leaves the real sentinel process alive.

### A7 — Leader exit with a surviving group

Given a real leader that creates a descendant in its group and then exits, when the leader
PID is unavailable but the group remains present, then `process-reconcile` records
`identity_unknown` with `process_birth_identity_unavailable`. It sends no signal and leaves
the descendant alive.

### A8 — Capture and release crash matrix

Given one fixture for each crash point in Architecture H, when the broker or gateway
restarts, then the row reaches the exact stated result. A fixture whose barrier was not
released has no workload marker.

### A9 — TERM-to-KILL identity change

Given a matched group that receives TERM, when the final OS read before KILL returns a
different birth identity, then the worker returns `identity_unknown` and sends no KILL.

### A10 — Legacy evidence and row

Given the exact five-field evidence and row shape from commit `1ae81e6`, when the version
2 worker probes or stops it, then it returns `identity_unknown` with
`process_birth_identity_missing` and sends no signal. When schema activation sees the
candidate table shape, it returns `incompatible_managed_process_birth_identity_v1` and
does not alter the table.

### A11 — Mixed-version release fence

Given each old/new broker and gateway pairing, when `process-bind` runs, then only a reply
that echoes version `2` and the exact birth tuple opens the barrier. Each other pairing
keeps the barrier closed and records the typed refusal.

### A12 — Boot recovery parity

Given equivalent rows presented to `process-reconcile` and boot recovery, when each path
uses the same OS observation, then both paths produce the same state, uncertainty cause,
stop cause, and repair verb.

### A13 — Reboot and restart

Given a stored row from another boot, when boot recovery runs, then the existing reboot
rule proves the old process ended. Given the same-boot numeric identity with a mismatched
birth tuple, boot recovery records `identity_unknown` and sends no signal.

### A14 — Lease and retirement stops

Given one matched version 2 row for each stop cause `owner_stop`, `lease_expired`, and
`session_retired`, when the corresponding stop path runs, then it uses the same final
birth read and retains the original stop cause. The retirement finalizer remains blocked
until the row reaches an existing terminal state.

### A15 — Typed-data boundary

Given canary values in command text, error text, arguments, environment, and credentials,
when capture, bind, stop, and reconcile run, then no identity decision changes because of
those strings. The managed row and evidence contain only the fields defined in this
amendment, and the existing credential canary scan remains clean.

### Acceptance matrix

| Risk | Linux | Darwin | Required observable |
|---|---:|---:|---|
| Capture before release | A1 | A2 | Workload marker appears only after version 2 grant. |
| Durable row/evidence equality | A1, A3 | A2, A3 | Exact typed tuples match. |
| Positive stop capability | A4 | A4 | Matched real group receives the existing bounded stop. |
| Same-boot PID/PGID reuse | A5, A6 | A5, A6 | `identity_unknown`, zero signal calls, foreign sentinel alive. |
| Leader exit | A7 | A7 | Surviving group receives no unproved signal. |
| Crash and restart | A8, A12, A13 | A8, A12, A13 | Shared decision table and closed barrier. |
| TERM/KILL overlap | A9 | A9 | Second birth read gates KILL. |
| Legacy and mixed versions | A10, A11 | A10, A11 | Refusal, no table rewrite, no release, no signal. |
| Stop-cause preservation | A14 | A14 | Cause unchanged through stop and reconciliation. |
| Prose and credential exclusion | A15 | A15 | Typed decisions and clean canary scan. |

## Open Questions

No blocking question remains.

No non-blocking question remains.

The implementation may choose Rust data types and module-private function names. It may
not change the field meanings, decision order, refusal codes, evidence version, schema
rules, or acceptance outcomes without amending this canonical file first.

## Review and handoff

The owner must open exactly one independent cross-harness spec review for this immutable
artifact. The reviewer must bind its verdict to the artifact SHA-256 and answer:

1. Does the amendment remain F5-only?
2. Does each lawful signal require row, evidence, boot, and current OS birth agreement?
3. Do Linux and Darwin use the named OS authorities?
4. Do mismatch and unavailable proof produce `identity_unknown` with no signal?
5. Does a matched version 2 row retain the required stop capability?
6. Does the design handle PID/PGID reuse, leader exit, broker exit, and each crash point?
7. Do legacy and mixed-version paths fail closed without inventing a birth identity?
8. Does the deterministic reuse fixture assert that the foreign real process survives?
9. Does the source census cover each required implementation and verification seam?
10. Does the amendment preserve F1-F4, F6-F7, revision 6 retirement, security, and credential boundaries?

Implementation remains blocked until this exact artifact receives a reviewed-clean
verdict. A changes-requested verdict amends this canonical file first and produces a new
artifact SHA before another handoff.

Operating-pattern amendment: none. The public process verbs and agent repair pattern
remain unchanged.

