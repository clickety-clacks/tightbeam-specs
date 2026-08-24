# agentd v1 — truthful local registry and event stream for coding agents

Status: READY FOR INDEPENDENT SPEC RE-REVIEW

Date: 2026-08-24

Work item: `wi_c09ad7a1-7e74-40d5-b15e-5f9f86eb0982`

Producer assignment: `asg_78c4a8b6-0665-4816-a4bd-39d3868d67d2`

Authority:

- Owner Spirit gate: `att_f86bed15-e1bd-490f-a45f-d1970d12059d`.
- Orchestrator digest: `att_a7fa9792-fec8-411f-9a5c-7e1c0e65fd66`.
- First changes-requested review: `att_aecc2141-763b-43df-a472-5454434bd484` with full
  report `art_2405714e` against commit
  `b14cc5f3165cbc4bb1161127397b21030911e870`.
- Successor changes-requested review: `att_32cf709c-7667-4ca8-a472-e857b63a8583`
  with full report `art_4ffef7c0` against commit
  `e4a3ae96b1a324c5951df7daaf3448a2b6ef9a21`.
- Round-three changes-requested review: `att_5f156780-dc9c-4a3f-bb09-0c4bb81e2137`
  with full report `art_232284fe` against commit
  `647b269face5e41652ca5dc850b6d2ab3a398faf`.
- The independent spec review must clear an exact content hash before implementation starts.

## Goal

G1. `agentd` gives a local Linux user one truthful roster of that user's running Codex
and Claude coding-agent processes.

G2. `agentd` derives process existence and process identity from the current Linux
`/proc` view. A lifecycle hook can add an activity claim to an existing roster entry.

G3. A consumer can read one complete roster snapshot or subscribe to complete roster
snapshots through one local Unix stream socket.

G4. A command-line user can inspect the current roster and watch roster changes without
reading daemon internals.

G5. A systemd user service starts, supervises, and stops the daemon within the user's
login lifecycle.

G6. The v1 acceptance run proves the contract with three real Codex processes and one
real Claude process that share one working directory on Linux.

## Non-Goals

- Remote or multi-host aggregation.
- A graphical or web user interface.
- Transcript capture, storage, transport, or display.
- An LLM call made by `agentd`.
- Steering, prompting, interrupting, or terminating a coding agent.
- A plugin or provider framework.
- macOS support.
- Windows support.
- Process authentication. A harness classification is an observation from procfs, not
  proof that a vendor produced the process.
- Cross-user process discovery or a system-wide daemon.
- Historical roster queries, event replay, event retention, or a durable registry.
- CPU, token, cost, model, task, conversation, or progress inference.
- Automatic conversion of elapsed time into an activity state.

## Terms

### Local user

The **local user** is the effective Unix user that runs `agentd`. The daemon reads only
the procfs view available to that user. The Unix socket admits clients under that same
user account through filesystem permissions.

### Procfs observation

A **procfs observation** is data read from `/proc` during one scan. The scanner reads
`/proc/<pid>/stat` for process ID, parent process ID, process state, command name, and
start time. It reads the effective UID from the `Uid:` row in `/proc/<pid>/status`. It
reads `/proc/<pid>/cwd` for the working directory.

Linux defines `starttime` as unsigned field 22 in `/proc/<pid>/stat`, measured in clock
ticks after system boot. The implementation retains the raw integer. It does not
convert the value to wall time.

### Process identity

A **process identity** is the pair `{pid, startTimeTicks}`. The process ID is a positive
integer. `startTimeTicks` is the positive field-22 value from procfs. A reused PID with
a different start time denotes a different process identity.

The identity has meaning within one Linux boot. `agentd` stores no identity across a
reboot.

### Harness candidate and agent root

A **harness candidate** is a live, non-zombie process whose procfs command name matches
one rule in this closed v1 table:

| Harness | Exact command names |
| --- | --- |
| `codex` | `codex` |
| `claude` | `claude`, `claude.exe` |

A **local harness candidate** is a harness candidate whose effective UID equals the
daemon's effective UID.

A **validated local harness candidate** is a local harness candidate whose two stat
reads in one scan report the same positive start time and the same parent process ID.
The second read must still match the harness rule and a non-zombie process state. A
parent process ID change leaves ancestry unresolved with cause `process_raced`.

An **agent root** is a validated local harness candidate whose resolved observed parent
chain contains no ancestor that is also a validated local harness candidate for the
same harness in the same completed procfs scan. The parent-chain walk passes through
processes that are not harness candidates. It resolves when it reaches parent process
ID 0. A missing referenced parent entry or a repeated process ID leaves the chain
unresolved with cause `process_raced`.
The walker visits each process ID at most once. This rule collapses same-user helper
descendants into one roster entry. A different-UID ancestor does not disqualify a local
harness candidate. Sibling validated local harness candidates remain separate entries.

The harness value reports which rule matched. It does not authenticate the executable,
the command line, or the vendor.

### Presence

**Presence** is the result of the latest procfs observation for one process identity:

- `present`: the scanner read the same positive start time twice during one scan, the
  process qualified as an agent root, and the second stat read still matched the
  harness rule and a non-zombie process state.
- `unknown`: the scanner previously proved the identity, but a non-absence read or
  ancestry-resolution failure prevented the next scan from proving or disproving it.
- `absent`: a complete scan proved that procfs no longer exposed the identity as a
  qualifying local-user agent. Disappearance, start-time change, harness mismatch,
  zombie state, effective-UID mismatch, or loss of agent-root qualification proves this
  result. An absent identity is not stored in the roster; its removal appears in the
  next snapshot.

### Activity claim

An **activity claim** is `active`, `idle`, or `unknown` for one exact process identity.
`active` and `idle` come only from an optional hook request. `unknown` means no hook
claim exists for the current daemon instance and identity.

An activity claim describes the latest accepted hook message. It does not prove what
the model or process is doing now. The server records the acceptance time so a consumer
can judge the claim's age without `agentd` inventing an expiry threshold.

### Roster and committed snapshot

The **roster** is the daemon's in-memory map from process identity to agent record. The
daemon keeps no persistent copy.

A **committed snapshot** is one immutable value of the complete roster and its scan
status at one revision. A timestamp-only scan can replace the current value at the same
revision. A client receives either one complete value or no value. A client does not
receive a partial scan.

### Daemon instance and revision

A **daemon instance** is one execution of the resident process. It creates a random
128-bit `instanceId` at startup and does not persist it.

A **revision** is a positive 64-bit integer within one daemon instance. Revision 1 is
the first committed snapshot. The daemon increments the revision once when a commit
changes any serialized snapshot field other than `observedAtUnixMs`.

A revision identifies roster, scan, and activity state. It does not identify byte-equal
snapshot frames because a later snapshot request can carry a newer
`observedAtUnixMs` at the same revision.

### Event stream

The **event stream** is a sequence of complete snapshot frames on one subscribed Unix
stream connection. It is a current-state feed, not a history. A reconnecting consumer
starts again with a new complete snapshot.

### Complete and degraded scan

A **complete scan** enumerates the numeric entries visible in `/proc` and resolves each
retained agent identity to `present` or `absent`. A cwd failure or a failure to classify
a previously unknown PID can add a scan issue without making the scan degraded.

A **degraded scan** cannot resolve at least one retained identity or cannot enumerate
`/proc`. The snapshot names the failure with a closed cause. The daemon does not convert
that uncertainty into absence.

## Assumptions

- The Linux host mounts procfs at `/proc`.
- Procfs exposes field 22 as documented by `proc_pid_stat(5)`.
- Current Linux Codex root processes use command name `codex`.
- Current Linux Claude root processes use command name `claude` or `claude.exe`.
- A systemd user manager supplies `XDG_RUNTIME_DIR` for the service.
- The local user's runtime directory is local, user-owned, and mode `0700`, as required
  by the XDG Base Directory Specification.
- A process can start or exit without an application hook. Therefore the daemon must
  observe procfs independently of hooks.
- Procfs provides no portable per-user start-and-exit subscription that this MVP can
  require. The acceptance deadline bounds observation delay; it does not decide whether
  a process exists.
- The test host has working, authenticated Codex and Claude installations. Those tools
  may contact their providers during the smoke. `agentd` itself makes no such call.
- The implementation can inject a procfs root and a clock in automated tests. The
  public runtime still uses `/proc` and the system clock.

## Invariants

### I1 — Procfs owns existence

I1.1. The scanner adds an agent record only after two reads of
`/proc/<pid>/stat` return the same positive field-22 start time during one scan.

I1.2. The scanner keeps `presence.state=present` only when the completed scan qualifies
the identity as an agent root and the second stat read still matches the same harness
rule and a non-zombie process state.

I1.3. The daemon removes an old process identity after a complete scan proves that the
identity no longer satisfies the `present` rule.

I1.4. The daemon treats the same PID with a different start time as one removal and one
addition in the same commit.

I1.5. An activity request cannot create an agent record.

I1.6. An activity request cannot keep an agent record after procfs proves absence.

I1.7. If procfs continuously exposes a qualifying new identity, or continuously stops
exposing a retained identity, the daemon publishes the corresponding addition or
removal no later than 2 seconds after that condition begins.

### I2 — Detection is closed and observational

I2.1. The scanner uses the command-name table in Terms to classify v1 harnesses.

I2.2. The scanner classifies a harness candidate as local only when the effective UID in
`/proc/<pid>/status` equals the daemon's effective UID.

I2.3. The scanner walks the observed parent chain for each validated local harness
candidate. It visits each process ID at most once.

I2.4. The scanner emits one record for each agent root.

I2.5. The scanner labels each record with `detectedBy="proc_comm"`.

I2.6. The scanner reads no command line or environment value for detection or output.

I2.7. A process outside the closed command-name table, or a process whose effective UID
differs from the daemon's effective UID, does not enter the roster.

I2.8. The parent-chain walker stops when it reaches parent process ID 0, cannot find a
referenced parent in the first-read table, or encounters a process ID that it has
already visited.

I2.9. A missing referenced parent, a repeated process ID, or a candidate parent process
ID that differs between its two stat reads produces a `parent_chain` scan issue with
cause `process_raced`.

I2.10. When ancestry is unresolved, the scanner keeps an affected retained identity
with `presence.state=unknown` and cause `process_raced`. It omits an affected new
identity because the scan did not prove agent-root qualification.

### I3 — Unknown remains explicit

I3.1. A non-absence stat, status, or ancestry failure for a retained identity changes
its presence to `unknown` with one cause from
`permission_denied | process_raced | io_error | proc_unavailable`.

I3.2. A failed cwd read produces `cwd.state=unknown`, `cwd.value=null`, and one cause
from `permission_denied | process_raced | io_error`.

I3.3. A successful cwd read produces `cwd.state=known`, the absolute path in
`cwd.value`, and `cwd.cause=null`.

I3.4. A new process identity starts with `activity.state=unknown`,
`activity.source=none`, and `activity.observedAtUnixMs=null`.

I3.5. The daemon derives no activity state from CPU use, elapsed time, output, files,
network traffic, or process state.

I3.6. A degraded scan keeps the last identity instead of reporting it as absent. The
record carries `presence.state=unknown` until a later scan proves presence or absence.

I3.7. A successful read that proves absence takes precedence over an unrelated failed
read. A failed read produces unknown presence only when that failure blocks both proof
of presence and proof of absence.

### I4 — One commit produces one atomic snapshot

I4.1. One mutation seam named **observe-then-commit** replaces roster state. The
scanner and activity handler submit proposed changes through that seam.

I4.2. A scan builds its next roster privately and performs one commit after the scan
finishes.

I4.3. At the mutation seam, a scan commit reads activity from the then-current committed
snapshot. It carries that claim forward only when the current and proposed process
identities match exactly. A scan proposal cannot overwrite an activity commit that
occurred while the scan was reading procfs.

I4.4. A commit discards an activity claim when the PID's start time changes.

I4.5. The serializer orders records by `(harness, pid, startTimeTicks)`.

I4.6. A snapshot request returns one complete snapshot from one revision and then
closes the connection.

I4.7. A subscribe request registers the subscriber and captures its first snapshot as
one indivisible operation. The first frame is that snapshot. Later frames have a greater
revision within the same daemon instance.

I4.8. Each subscriber has capacity for one complete changed snapshot whose socket write
has not started. A newer snapshot replaces that pending snapshot. A partially written
frame buffer completes before the pending snapshot starts. The application retains no
other frame buffer for that subscriber. The operating system's socket send buffer has a
fixed configured bound and is not an application event queue.

I4.9. The daemon runs at most one procfs scan at a time. Scan commits occur in scan-start
order.

I4.10. When an identity leaves the roster, the daemon discards its activity claim.

I4.11. If the same process identity later regains agent-root qualification, the daemon
adds it with activity `unknown`.

I4.12. Without releasing the observe-then-commit seam, the activity handler resolves
the exact identity, verifies present status, samples the activity time, constructs the
proposed claim, and compares its serialized activity data with the current claim.

I4.13. If the identity is absent or has unknown presence at that operation, the handler
returns `unknown_agent`. It leaves the roster, revision, and activity claims unchanged.

I4.14. If the proposed activity data differs from the current claim, the handler
increments the revision once, swaps the changed snapshot, and offers that snapshot to
each subscriber before it returns an acknowledgement with the new revision.

I4.15. If the proposed activity data equals the current claim, the handler retains the
current snapshot, revision, and reason. It offers no subscriber frame and returns a
successful acknowledgement with the retained revision.

### I5 — One local Unix socket carries the contract

I5.1. The daemon listens on one `AF_UNIX`, `SOCK_STREAM` socket at
`$XDG_RUNTIME_DIR/agentd.sock`.

I5.2. The daemon creates the socket with mode `0600`.

I5.3. Each request and response is one UTF-8 JSON object followed by LF.

I5.4. The server accepts one request object of at most 65,536 UTF-8 bytes per
connection, excluding the terminating LF. If LF has not arrived after 65,536 object
bytes, the server returns `request_too_large` without parsing the object.

I5.5. The closed request set is:

```json
{"version":1,"op":"snapshot"}
{"version":1,"op":"subscribe"}
{"version":1,"op":"activity","agent":{"pid":930481,"startTimeTicks":1787554},"state":"active"}
```

Each request contains exactly the fields in its example. Duplicate, missing, or extra
fields, non-integer identity values, and non-positive identity values are malformed.

I5.6. The activity handler accepts `active` or `idle` only when the exact process
identity has `presence.state=present` at the activity commit operation in I4.12.

I5.7. The server samples `activity.observedAtUnixMs` when it accepts the request. It
sets `activity.source=hook`.

I5.8. A successful activity change commits before the server returns its acknowledgement.

I5.9. A request with an unknown version, unknown operation, malformed JSON, oversized
frame, invalid activity state, or absent identity returns one error frame and closes.
The error code comes from
`unsupported_version | unknown_operation | malformed_request | request_too_large |
invalid_activity | unknown_agent`.

I5.10. A subscriber receives complete snapshots only. The protocol exposes no diff,
cursor, replay, or history request.

I5.11. Each accepted activity request returns one acknowledgement. Its `revision` is
the new revision from I4.14 or the retained revision from I4.15.

### I6 — Snapshot schema is total

I6.1. A snapshot frame uses this exact field set. Each field is present.

```json
{
  "type": "snapshot",
  "reason": "initial",
  "schema": "agentd.snapshot.v1",
  "instanceId": "8d9ee30a6ae34fb0a2dc33ee088dd34a",
  "revision": 1,
  "observedAtUnixMs": 1787555200000,
  "scan": {
    "state": "complete",
    "issues": []
  },
  "agents": [
    {
      "id": {"pid": 930481, "startTimeTicks": 1787554},
      "harness": "codex",
      "detectedBy": "proc_comm",
      "presence": {"state": "present", "cause": null},
      "cwd": {"state": "known", "value": "/home/mike/work/agentd-smoke", "cause": null},
      "activity": {"state": "unknown", "source": "none", "observedAtUnixMs": null}
    }
  ]
}
```

I6.2. `reason` is `initial | roster_changed | activity_changed | scan_changed`. The
first committed snapshot uses `initial`. A later commit uses `roster_changed` when the
agent set or any non-activity agent field changes. Otherwise it uses `activity_changed`
when activity data changes. Otherwise it uses `scan_changed`. This order is the
precedence when one commit changes more than one category.

I6.3. `observedAtUnixMs` is the time sampled at the start of the most recently completed
procfs scan. A timestamp-only scan refreshes the current snapshot at the same revision,
retains its preceding reason, and emits no frame. An activity-only commit carries this
value forward unchanged.

I6.4. `scan.state` is `complete | degraded`. It is `degraded` exactly when procfs
enumeration failed or at least one retained identity has unknown presence.

I6.5. Each scan issue has the exact fields `pid`, `field`, and `cause`. `pid` is a
positive integer or null. `field` is
`proc | stat | status | parent_chain | cwd`. `cause` is
`permission_denied | process_raced | io_error | proc_unavailable`.

I6.6. The serializer orders scan issues by `(pid, field, cause)`, with a null PID before
positive PIDs. It emits no duplicate issue in one snapshot.

I6.7. A full `/proc` enumeration failure preserves the preceding records, changes their
presence to `unknown` with cause `proc_unavailable`, and emits a degraded snapshot.
If no preceding snapshot exists, the daemon emits a degraded empty snapshot whose scan
issue names `proc_unavailable`.

I6.8. The daemon increments the revision when roster data, scan state, scan issues, or
activity data changes. A timestamp-only change does not increment the revision and does
not emit a frame.

I6.9. `instanceId` contains exactly 32 lowercase hexadecimal digits. Every agent object
contains exactly `id`, `harness`, `detectedBy`, `presence`, `cwd`, and `activity`.
`presence.cause` is null exactly when presence is present. `cwd.cause` is null exactly
when cwd is known. `activity.source` is `none` exactly when activity is unknown.

### I7 — CLI inspection uses the socket contract

I7.1. `agentd list` sends a snapshot request and prints one human-readable snapshot.

I7.2. `agentd list --json` prints the snapshot frame unchanged, followed by LF.

I7.3. `agentd watch` sends a subscribe request and prints one human-readable snapshot
for the initial frame and each changed frame.

I7.4. `agentd watch --json` prints each received snapshot frame unchanged as NDJSON.

I7.5. `agentd activity --pid <positive-integer> --state active|idle` reads the current
start time from procfs and sends an activity request for the exact identity.

I7.6. Each human-readable snapshot starts with this exact header field order:
`instance=<instanceId> revision=<revision> scan=<state> agents=<count>`.

I7.7. The human-readable snapshot prints one line for each scan issue in serialized
order as `issue pid=<pid|none> field=<field> cause=<cause>`.

I7.8. The human-readable snapshot prints one line for each agent in serialized order
with the process ID, start-time ticks, harness, presence, cwd, and activity. It prints
the word `unknown` for each unknown value.

I7.9. A zero-agent human-readable snapshot prints its header and each scan issue.

I7.10. `agentd list` exits 0 after printing a valid complete or degraded snapshot. A
degraded scan is not a command error.

I7.11. `agentd watch` prints a valid degraded snapshot and keeps the subscription open.

I7.12. `agentd activity` exits 0 after it receives an acknowledgement for its request.
It writes nothing to stdout or stderr.

I7.13. A usage, socket, protocol, or daemon error exits 1 and writes one error line to
stderr that names the failed operation and cause.

### I8 — The systemd user service owns runtime lifecycle

I8.1. The repository ships `packaging/systemd/agentd.service` for the systemd user
manager.

I8.2. The unit sets `ExecStart=%h/.local/bin/agentd daemon`.

I8.3. Daemon mode resolves its sole socket as `$XDG_RUNTIME_DIR/agentd.sock`, using the
runtime environment from the systemd user manager.

I8.4. The unit uses `Restart=on-failure` and joins `default.target` through its
`[Install]` section.

I8.5. The installation instructions place the binary under `$HOME/.local/bin`, place
the unit under `${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user`, run
`systemctl --user daemon-reload`, and run `systemctl --user enable --now agentd.service`.

I8.6. On SIGTERM, the daemon stops accepting clients, closes subscriber connections,
removes its socket, and exits 0 within 5 seconds.

I8.7. At startup, the daemon refuses to remove a path that is not a socket or is not
owned by the local user. For an owned socket, the daemon attempts to connect. A
successful connection makes startup fail without changing the path. `ECONNREFUSED`
permits removal only after a second `lstat` confirms the same device and inode.
`ENOENT` restarts the bind attempt without removal. Any other connection result makes
startup fail without changing the path.

I8.8. After a daemon restart, the daemon creates a new `instanceId`, rebuilds the roster
from procfs, and initializes each activity claim to `unknown`.

### I9 — Data and privacy stay bounded

I9.1. The daemon keeps the roster, revisions, hook claims, and subscriber slots in
memory only.

I9.2. The daemon opens no IPv4 or IPv6 listening socket and makes no outbound network
connection.

I9.3. The daemon sends and logs no command line, environment value, transcript, prompt,
or model response.

I9.4. The socket emits only the fields in I6, acknowledgement fields, or error fields.

I9.5. An acknowledgement has the exact fields `type="ack"`, `instanceId`, and
`revision`.

I9.6. An error has the exact fields `type="error"`, `code`, and `message`. The message
does not echo the rejected request bytes.

## Architecture

### A. Resident daemon

The resident daemon is the one added long-lived mechanism. Deleting it would remove the
required push stream. Accepting snapshot-only polling would fail G3. The daemon therefore
earns its place; a database, replay log, HTTP server, and network listener do not.

The daemon owns four components in one process:

1. A procfs scanner produces observations.
2. The observe-then-commit seam owns the current immutable roster snapshot.
3. A Unix socket server handles snapshot, subscribe, and activity requests.
4. A broadcaster offers the latest changed snapshot to each subscriber's one-slot queue.

The operating pattern taught to Tightbeam agents is **none**. This product contract does
not require a Tightbeam manual or guidance amendment.

### B. Scan and commit sequence

The scanner performs this sequence:

1. Sample `observedAtUnixMs`.
2. Read the numeric directory names visible under `/proc` once.
3. Read each numeric PID's stat record. Parse fields after the final right parenthesis so a
   command name that contains spaces or parentheses does not shift the numeric fields.
4. Build the PID, parent, command-name, state, and start-time table.
5. Apply the closed harness table.
6. Read each harness candidate's status record and extract the effective UID from the
   second value in its `Uid:` row. Retain only candidates whose effective UID equals the
   daemon's effective UID.
7. Re-read each local harness candidate's stat record. Drop the candidate when the
   second read disappeared, changed start time, changed harness, or became a zombie.
   Mark its ancestry `process_raced` when the parent process ID changed.
8. Walk each validated local harness candidate's observed parent chain with a visited
   process-ID set. Apply I2.8-I2.10 when the walk stops. Retain the candidate as an agent
   root only when the resolved chain contains no validated local candidate for the same
   harness.
9. Read each root's cwd link.
10. Reconcile old identities under I1 and I3. Remove a retained identity when it loses
    agent-root qualification. Add an existing process identity when it gains agent-root
    qualification and passes the two stat reads.
11. Carry hook activity only across an exact identity match.
12. Submit the complete proposed snapshot to observe-then-commit once.

The parser rejects a zero start time, an integer overflow, a stat record without all
fields through field 22, a status record without a valid four-value `Uid:` row, or a
record without a parseable stat delimiter. A failure for a new PID creates a scan issue
but no identity. A non-absence failure for a retained identity follows I3.

The daemon performs the scan independently of subscriber count and hook traffic. Hook
traffic cannot delay or cancel a scheduled scan.

### C. Snapshot commit and broadcast

Observe-then-commit compares the proposed serialized state to the current state without
the top-level scan observation timestamp. When a scan proposal's state matches, it
refreshes only the current snapshot's scan observation timestamp, retains the revision
and reason, and sends no frame. Previously captured values remain unchanged. When the
state differs, it increments the revision once, swaps the full immutable snapshot, and
offers that snapshot to each subscriber.

The activity handler parses the request before entering the mutation seam. At the seam,
it performs I4.12-I4.15 against the then-current immutable snapshot. An identical
activity proposal retains the complete current snapshot and revision, returns an
acknowledgement for that revision, and causes no broadcast. A scan removal that commits
first makes the handler return `unknown_agent`; the handler cannot restore the removed
record. An activity change that lands first is carried or discarded by the later scan
under I4.3-I4.4.

The broadcaster stores at most the newest not-yet-started snapshot for a subscriber. It
can also finish the one application frame buffer whose socket write has started. The
kernel socket send buffer remains bounded separately. This rule lets a slow consumer
skip intermediate revisions without losing access to a complete current roster. A
consumer that requires current state reconnects and receives the current committed
snapshot as its first frame.

### D. Unix protocol

The daemon commits its first procfs snapshot before it binds the one socket. After
stale-socket checks complete, the server binds and listens. It reads one request line,
enforces the byte limit before JSON parsing, and dispatches by `version` and `op`.

For `snapshot`, the server captures the current immutable snapshot, writes one frame,
and closes. For `subscribe`, the server registers the subscriber and captures the first
snapshot under the same commit lock, then writes that frame before changed snapshots.
For `activity`, the server applies I4.12-I4.15. It broadcasts the changed snapshot only
after I4.14 changes the activity data. It writes one acknowledgement containing the
revision identified by I5.11 and closes.

The protocol carries complete snapshots because they make loss and coalescing harmless.
A diff protocol, replay store, or cursor would add a second reconstruction mechanism
without serving a v1 goal.

### E. CLI and service packaging

The `agentd` binary contains the daemon and CLI commands. Daemon and inspection commands
resolve the sole socket as `$XDG_RUNTIME_DIR/agentd.sock`. The CLI exposes no socket-path
configuration. When `XDG_RUNTIME_DIR` is unset, the error names that variable. When the
socket is unavailable, the error names the resolved path and
`systemctl --user status agentd.service` as the diagnostic command.

The systemd user unit starts the same binary in daemon mode. The unit expresses login
lifecycle, restart policy, and the runtime socket path. The README states the install,
inspect, log, stop, restart, and uninstall commands separately. Uninstall removes the
unit and binary after stopping the service. There is no durable roster to remove.

## Acceptance

Each acceptance case names the invariants that it verifies.

### A1 — Real four-agent shared-cwd smoke (G1, G6; I1, I2, I7)

**Given** a real Linux host, a dedicated working directory, a running systemd user
service, and no agentd lifecycle hooks, **when** the test starts as the daemon user
three real Codex coding-agent processes and one real Claude coding-agent process in that
directory,
**then** `agentd list --json` contains four `presence.state=present` agent roots whose
known cwd equals that directory, with three `codex` records and one `claude` record.

The test filters by the dedicated cwd so unrelated host agents do not affect the count.
Each record has a distinct process identity. Helper descendants do not add records.
Each activity state is `unknown`.

**Given** a local-UID `bash` parent and its local-UID `codex` child, **when** one complete
scan qualifies only the child as a Codex root and the next scan observes the same parent
identity with command name `codex`, **then** one commit adds the parent root and removes
the child root. The child keeps running but no longer appears in the roster.

**When** the next complete scan observes the parent identity with command name `bash`
again, **then** one commit removes the parent root and adds the child root. The child
returns with activity `unknown` because its preceding claim was discarded on removal.

**Given** a local-UID Codex candidate with a different-UID Codex ancestor, **when** the
scanner computes roots, **then** it retains the local candidate because the ancestor is
outside the local-candidate domain.

### A2 — Hook independence and enrichment (G2; I1, I3, I4, I5, I6)

**Given** the four hookless records from A1, **when** the test sends `active` and then
`idle` for one exact identity, **then** two changed snapshots report those claims with
server times, while the other three records remain `unknown`.

**Given** an absent PID or the right PID with the wrong start time, **when** the test
sends an activity request, **then** the server returns `unknown_agent`, creates no
record, and changes no retained activity claim.

**Given** a present identity whose current claim is `active` from an acceptance time T
and a clock fixed at T, **when** the test sends `active` again, **then** the server
returns an acknowledgement with the current instance ID and retained revision. The
current snapshot and revision remain unchanged, and a subscriber receives no frame.

### A3 — Start and exit deadline (I1.3, I1.7)

**Given** a live subscription and a completed baseline scan, **when** one real agent
process starts or exits, **then** the subscriber receives a complete snapshot that
reflects the addition or removal within 2 seconds of the procfs change.

### A4 — PID reuse (I1.4, I4.3, I4.4)

**Given** a captured real procfs fixture for PID 4242 at start time 100 with an `active`
claim, **when** the next injected scan exposes PID 4242 at start time 200, **then** one
commit removes `{4242,100}`, adds `{4242,200}`, and gives the new identity activity
`unknown`.

### A5 — Explicit uncertainty (I3, I6)

**Given** a retained identity and an injected non-absence stat or status read failure
that blocks proof of presence and absence, **when** the scanner commits, **then** the
record remains with `presence.state=unknown` and the typed cause.

**Given** a present identity and an injected cwd permission refusal, **when** the scanner
commits, **then** cwd has state `unknown`, value null, and cause `permission_denied`,
while the scan state remains `complete`.

**Given** a full procfs enumeration failure, **when** the scanner commits, **then** the
snapshot is degraded, preceding records remain with unknown presence, and no record is
reported absent.

### A6 — Atomic first snapshot and ordered changes (I4, I6)

**Given** one subscriber and a concurrent scan commit, **when** the subscriber registers,
**then** it receives either the complete pre-commit snapshot or the complete post-commit
snapshot first. It does not receive a mixed roster.

**Given** later roster and activity commits, **when** the subscriber reads frames,
**then** each frame is complete, records are sorted, and revisions increase within the
same instance.

**Given** a scan in progress for an unchanged identity, **when** an activity commit lands
before that scan commits, **then** the later scan snapshot retains the new activity
claim.

**Given** an activity request that has been parsed for identity X, **when** a complete
scan removes X before the activity handler enters observe-then-commit, **then** the
handler returns `unknown_agent`, commits no snapshot, and does not restore X or change
another identity's activity claim.

**Given** one scan commit that changes both roster and scan fields, **when** the daemon
serializes it, **then** its reason is `roster_changed`. **Given** an activity-only
commit, **then** its reason is `activity_changed` and its `observedAtUnixMs` equals the
preceding scan snapshot's value.

**Given** a scan that changes only `observedAtUnixMs`, **when** it completes, **then** a
new snapshot request returns the same revision and reason with the new timestamp, and a
subscriber receives no new frame.

### A7 — Slow subscriber bound (I4.8, I5.10)

**Given** a subscriber that stops reading, **when** the daemon commits 1,000 changed
snapshots, **then** that subscriber owns at most one frame whose write has started and
one complete pending frame in application memory. Its queue allocation and configured
kernel send-buffer bound do not grow with the number of skipped revisions.

**When** the subscriber reads again or reconnects, **then** it can obtain a complete
current roster without replaying skipped revisions.

### A8 — Protocol and byte limit (I5, I9)

**Given** the live socket, **when** a client sends each valid request example, **then**
the server returns the specified snapshot or acknowledgement behavior.

**When** a client sends malformed JSON, an unknown version, an unknown operation, an
invalid activity, an unknown identity, or 65,537 object bytes without LF, **then** the
server returns the matching closed error code, echoes no request bytes, and closes the
connection. A valid 65,536-byte object followed by LF does not fail as oversized.

### A9 — CLI inspection (G4; I7)

**Given** a roster with one known cwd and one injected unknown cwd, **when** a user runs
`agentd list`, **then** the first line reports the instance, revision, scan state, and
agent count. Each agent line includes the required fields. The unknown cwd prints as
`unknown`.

**Given** a first scan whose `/proc` enumeration fails, **when** a user runs
`agentd list`, **then** it exits 0 and prints a header with `scan=degraded agents=0`.
It also prints `issue pid=none field=proc cause=proc_unavailable`. It prints no agent
line.

**Given** a daemon whose current snapshot is degraded with zero agents after a full
`/proc` enumeration failure, **when** a user runs `agentd watch`, **then** its first
frame has `scan=degraded agents=0` and the `proc_unavailable` issue. The command keeps
the subscription open.

**When** the user runs `agentd list --json`, **then** stdout equals the daemon's snapshot
frame plus LF.

**When** the user runs `agentd watch --json` and one agent exits, **then** stdout contains
the initial complete frame and a later complete frame without that identity.

**Given** a present agent identity, **when** a user runs `agentd activity --pid <pid>
--state active`, **then** the command exits 0, writes nothing to stdout or stderr, and a
subsequent `agentd list --json` reports `activity.state=active` with source `hook` for
that exact identity.

### A10 — User-service lifecycle (G5; I8)

**Given** a clean Linux user account with a systemd user manager, **when** the operator
follows the documented install commands, **then** `systemctl --user is-enabled
agentd.service` and `systemctl --user is-active agentd.service` both succeed, and the
socket exists at `$XDG_RUNTIME_DIR/agentd.sock` with mode `0600`.

**When** the test reads the installed unit's expanded `ExecStart`, **then** it contains
the absolute installed binary followed by `daemon` and no socket-path argument.

**When** a client connects immediately after the socket starts accepting connections,
**then** a snapshot request returns revision 1 or later; no pre-snapshot state is visible.

**Given** the active service, **when** the daemon exits unsuccessfully, **then** systemd
starts a new instance, the instance ID changes, and the daemon rebuilds the hookless
roster from procfs.

**When** the operator stops the service, **then** the process exits and the socket
disappears within 5 seconds.

### A11 — Safe stale-socket recovery (I8.7)

**Given** an owned stale socket with no listener, **when** the service starts, **then**
the daemon replaces it and begins listening.

**Given** a regular file, a socket owned by another user, or a live listener at the fixed
socket path, **when** a second daemon starts, **then** it exits 1, names the conflict,
and leaves the path unchanged.

### A12 — Privacy and local-only transport (Non-Goals; I2.6, I9)

**Given** real agent processes whose command lines and environments contain distinct
sentinel secrets, **when** the test captures daemon stdout, stderr, logs, list output,
and socket frames, **then** no sentinel appears in the capture.

**Given** a running daemon, **when** the test inspects its open sockets and traces one
scan plus one activity request, **then** it observes the one Unix listener and no IPv4,
IPv6, or outbound connection from `agentd`.

### A13 — Real procfs fixtures and parser stability (I1, I2, Architecture B)

**Given** procfs stat, status, and cwd fixtures captured from the four real A1 processes,
**when** the automated scanner tests replay them, **then** the parser reproduces the real
process identities, parent relations, effective UIDs, harnesses, and cwd results.

**Given** two harness candidates whose status fixtures report the daemon's effective UID
and a different effective UID, **when** the scanner classifies them, **then** it retains
only the candidate with the daemon's effective UID.

**Given** a captured real-shaped stat record whose command name contains spaces and a
right parenthesis, **when** the parser reads it, **then** it still reads the correct
parent PID, process state, and field-22 start time.

### A14 — Repository gate

**Given** the implementation commit that is proposed for review, **when** a clean Linux
checkout runs the repository's documented format, static-analysis, unit, integration,
and real-smoke commands, **then** each command exits 0 and the report records the exact
commit, commands, exit results, socket path, daemon instance IDs, process identities,
and teardown result.

### A15 — Raced parent-chain termination (I2, I3, I6)

**Given** a retained root candidate whose two stat reads keep the same identity and
harness but report different parent process IDs, **when** the scanner commits, **then**
the record remains with `presence.state=unknown` and cause `process_raced`. The snapshot
contains `field=parent_chain cause=process_raced` for that PID.

**Given** a first-read table in which candidate PID 100 names parent PID 200 and PID 200
names parent PID 100, **when** the scanner resolves PID 100's ancestry, **then** it visits
each PID at most once, commits without inventing a present agent root, and emits a
`parent_chain` issue with cause `process_raced`. It keeps PID 100 with unknown presence
when that identity was retained before the scan. It omits PID 100 when the identity was
new in that scan.

## Open Questions

Blocking questions: none.

Non-blocking questions: none.

The independent spec review can return defects against this draft. A reviewer finding
does not authorize implementation. The producer must amend this canonical file first,
land the revision, and present its new content hash for review.
