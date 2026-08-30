# Agentd v0.3 — display identity without screen scraping

Status: READY FOR INDEPENDENT EXACT-HASH SPEC REVIEW

Date: 2026-08-29 PT

Work item: `wi_8fc3f7ce-13b3-4d16-b48d-f375a1f23f0a`

Producer assignment: `asg_9f929c6d-ec1c-4c76-9e3f-9150496d6317`

Canonical product repository: `https://github.com/clickety-clacks/agentd`

Authority and baseline:

- Mike's work-item ruling requires enough snapshot identity for a UI to distinguish
  agents without screen scraping.
- The specification base is `agentd-v1.md` at SHA-256
  `03445f45652b9e517a3fc1f158510ee053e66454124480fa0202ed879af68248` and
  `agentd-v1.1.md` at SHA-256
  `4a5804c2ed4401eb91b449630742a40e7b2206b56f675c3b83feabd2c0e3b0f8`.
- The reviewed release baseline is Agentd tag `v0.2.0` at product commit
  `17f1482e139e20554cee32cb5ae41993b71c2da5`. Its `README.md` has SHA-256
  `b00dbfbc6a9787dc5a8fcd3ba65cbb1da406013cba155e198977395f9aee7331`.
  Its `docs/verification.md` has SHA-256
  `207cb11ec645674b4852d0769627f6432b7723bf2dafa52cf2fb9faeed1aead4`.
- This file is the v0.3 amendment. A v0.3 implementation satisfies the two
  specification-base files as corrected by the reviewed v0.2.0 release contract. The
  reviewed v0.2.0 behavior takes precedence where the earlier v1.1 draft differs from
  the shipped release, including Codex feature/version handling, trust ownership,
  configuration concurrency, and restart-only activation. This file takes precedence
  only where it explicitly changes that corrected base.
- The product version for this delivery is exactly `0.3.0`. The delivery cuts one
  release, `v0.3.0`, after exact-commit code review and acceptance. This spec does not
  authorize that release.

## Goal

G1. Each agent record gives a local display enough stable, privacy-safe metadata to
distinguish agents that share a harness and working directory.

G2. A record reports its Linux controlling terminal, best-effort tmux location,
user-set display name, and process start time through additive fields in
`agentd.snapshot.v1`.

G3. A user can set or clear a display name for one present exact process identity. The
name survives an Agentd daemon restart during the same Linux boot while that process
identity remains live.

G4. Human-readable `agentd list` and `agentd watch` lead each agent line with display
name, tmux location, and working-directory basename.

G5. The v0.3 delivery preserves the reviewed v0.2.0 roster authority, ordering,
revision, hook, integration, restart-only activation, fail-open, transport, and privacy
contracts except for the explicit additions in this amendment.

G6. Real acceptance on Gibson and Osanwe proves the new fields for tmux and non-tmux
agents without collecting terminal, prompt, command, or transcript content.

## Non-Goals

- Reading terminal screen cells, scrollback, OSC terminal titles, shell titles, pane
  commands, command lines, prompts, transcripts, model responses, or tool input.
- Treating a tmux window name as a harness title. A tmux window name is the explicit
  structural tmux field requested by this amendment; Agentd reads no other title.
- Inferring a display name from a prompt, directory, transcript, tmux name, terminal
  title, process command, or environment value.
- Authenticating a person, harness, tmux server, session, or display name.
- Cross-user tmux discovery, a system tmux server, remote tmux, or multi-host
  aggregation.
- macOS, Windows, non-procfs Linux, containers that hide the required procfs data, or
  terminals that cannot be represented by Linux `tty_nr`.
- Name history, rename history, roster history, event replay, or persistence of
  activity claims.
- Retaining a name across a Linux boot, after its exact process identity is proved
  gone, or after the same PID acquires another start time.
- Automatically installing a Claude `SessionStart` name hook. The optional adapter is
  available for a user-authored hook and does not change the reviewed four-event Claude
  activity integration.
- Adding a generic metadata, tmux, terminal, hook, or naming plugin framework.
- Changing the v0.2.0 agent sort key, issue sort key, revision increment rule, reason
  precedence, complete-snapshot stream, socket, request byte limit, or systemd service
  lifecycle.
- Changing which procfs processes qualify as Agentd roster roots.
- Changing Agentd-owned hook recognition, install or uninstall ownership, Codex trust
  ownership, hooks-feature gating, unverified-version warning, restart-only activation,
  hook timeout, or hook fail-open behavior from the reviewed v0.2.0 release.
- Making tmux metadata authoritative. It is one best-effort observation and can be
  stale until the next scan.

## Terms

### Base contract and amendment

The **base contract** is the authority and baseline set named in the preamble. This
file is the **v0.3 amendment**. A clause not changed here retains its reviewed v0.2.0
meaning.

### Exact process identity

An **exact process identity** remains `{pid,startTimeTicks}`. `pid` is a positive
32-bit integer. `startTimeTicks` is positive Linux `/proc/<pid>/stat` field 22 as an
unsigned 64-bit integer. The identity has meaning only within one Linux boot.

### Controlling terminal and canonical tty

The **controlling terminal number** is signed `/proc/<pid>/stat` field 7, `tty_nr`,
from the same two stat observations that validate the agent root. Zero means that the
process has no controlling terminal.

Agentd reinterprets a nonzero signed `tty_nr` as the same 32 two's-complement bits in
an unsigned Linux `dev_t` value. It decodes the device with the Linux major/minor
encoding:

```text
major = (bits >> 8) & 0x00000fff
minor = (bits & 0x000000ff) | ((bits >> 12) & 0x000fff00)
```

A **canonical tty** is:

- `pts/<index>` for Unix98 PTY slave major 136 through 143, where
  `index = (major - 136) * 256 + minor`; or
- `dev/<major>:<minor>` for another nonzero decoded character-device number.

The JSON field is null when `tty_nr` is zero, either stat read is invalid, the two
validated reads disagree on `tty_nr`, or the decoded value cannot be represented by
the rules above. Agentd does not read a process file descriptor to guess a terminal.

### Tmux observation and location

A **tmux observation** is the output of at most one direct, no-shell invocation of
`tmux list-panes -a -F <format>` during one procfs scan. Agentd invokes tmux as the
daemon's effective user and sets `<format>` to these five fields separated by the
ASCII Unit Separator byte `0x1f`:

```text
#{pane_tty}\u001f#{session_name}\u001f#{window_index}\u001f#{window_name}\u001f#{pane_id}
```

LF separates pane rows. Agentd accepts a row only when it has five fields, valid UTF-8,
no embedded LF or Unit Separator, a nonempty session name, a decimal `window_index`
that fits an unsigned 32-bit integer, a nonempty window name, and a pane ID matching
`%[0-9]+`. A session or window name containing a Unicode control character is invalid.

Agentd normalizes `pane_tty` to a canonical tty. `/dev/pts/<decimal-index>` becomes
`pts/<index>`. Another absolute `/dev` character-device path becomes
`dev/<major>:<minor>` from its `stat(2)` device number. Another value is invalid.

A **tmux location** is an object from one accepted row:

```json
{"session":"agents","windowIndex":2,"windowName":"spec","paneId":"%7"}
```

An index entry exists only when one accepted row names a canonical tty. Two accepted
rows for the same canonical tty make that tty ambiguous and remove it from the index.
A record receives a location only when its canonical tty has one index entry.

### Display name and name registry

A **display name** is a user-provided UTF-8 string whose encoded length is 1 through
64 bytes and whose Unicode scalar values contain no control character. Agentd preserves
the accepted bytes. It does not trim, normalize, case-fold, or infer the value.

The **name registry** is Agentd-owned state at
`$XDG_STATE_HOME/agentd/names.json` when `XDG_STATE_HOME` is set to an absolute path,
and `$HOME/.local/state/agentd/names.json` when it is unset. A relative set value makes
name retention and mutation unavailable but does not stop roster service. The registry
maps an exact process identity to one display name and records the current Linux boot
ID read from `/proc/sys/kernel/random/boot_id`. The file contains no roster field other
than the identity and name. It contains no activity, cwd, tty, tmux, prompt, title,
command, or transcript value.

A registry entry is eligible for an agent record only when the stored boot ID equals
the current boot ID and the entry's exact identity equals that record's identity.

### Started-at time

`bootTimeUnixSeconds` is the one unsigned decimal value from the exact `btime` row in
`/proc/stat`. `ticksPerSecond` is the positive result of `sysconf(_SC_CLK_TCK)`.

For one valid identity, **started-at time** is this checked integer calculation:

```text
bootTimeUnixSeconds * 1000
  + floor(startTimeTicks * 1000 / ticksPerSecond)
```

The calculation uses an intermediate wide enough to detect overflow. The JSON result
is an unsigned 64-bit Unix-millisecond integer or null.

### Additive schema compatibility

The schema marker remains exactly `agentd.snapshot.v1`. Each v0.3 agent object adds
four fields while retaining the v0.2 fields and meanings. A consumer that ignores
unknown agent-object fields remains compatible with v0.3. A strict v0.2 consumer that
rejects unknown fields must upgrade. A v0.3 consumer must treat the absence of any new
field in a v0.2 frame as null. Request `version=1`, acknowledgement, error, snapshot,
and subscribe framing remain unchanged; v0.2 servers can return `unknown_operation`
for the new name request.

## Assumptions

- Each base-contract assumption remains true.
- The runtime is Linux with procfs mounted at `/proc`.
- Linux exposes `tty_nr` as stat field 7 and `starttime` as stat field 22.
- Linux exposes one `btime` row in `/proc/stat` and a positive `_SC_CLK_TCK` value on
  hosts where `startedAtUnixMs` can be known.
- The daemon user can execute its own tmux client when tmux metadata is available.
- The tmux server, when present, belongs to the daemon user. `tmux list-panes -a` reports
  panes visible to that user's default tmux client environment.
- A tmux pane terminal can move or disappear between `list-panes` and snapshot commit.
  Linux and tmux expose no indivisible cross-process snapshot for this MVP.
- `XDG_STATE_HOME`, or its `$HOME/.local/state` fallback, is on a filesystem that can
  atomically rename a same-directory regular file.
- `/proc/sys/kernel/random/boot_id` stays constant during one Linux boot and changes
  across boots.
- A user-authored Claude `SessionStart` hook can pass a constant display name as an
  argv value. Its stdin can contain private JSON that Agentd must discard.

## Invariants

### I1 — The reviewed v0.2.0 contract remains the base

I1.1. Procfs remains the only authority for process existence, exact identity, harness
classification, presence, absence, and roster-root selection.

I1.2. The serializer retains the v0.2.0 agent order
`(harness,pid,startTimeTicks)` and the v0.2.0 scan-issue order.

I1.3. A scan increments the revision once when any serialized field other than the
top-level `observedAtUnixMs` changes. A name change increments the revision once. A
no-op name request retains the revision. The reason precedence remains
`roster_changed`, then `activity_changed`, then `scan_changed`. A tty, tmux,
started-at, or name change is a non-activity agent change and uses `roster_changed`.

I1.4. A daemon restart creates a new instance ID, resets revision to 1, rebuilds the
roster from procfs, and resets each activity claim to `unknown`. It can restore only an
eligible display name. It does not restore activity, tty, tmux, cwd, presence, scan, or
revision state from disk.

I1.5. The reviewed v0.2.0 activity requests, hooks, exact activity mapping, hook
ancestry mapping, payload discard, integration file ownership, Codex trust ownership,
restart-only hook activation, and fail-open behavior do not change.

### I2 — Each v0.3 agent object is total and additive

I2.1. Each serialized v0.3 agent object contains exactly these fields:

```json
{
  "id": {"pid": 930481, "startTimeTicks": 1787554},
  "harness": "codex",
  "detectedBy": "proc_comm",
  "presence": {"state": "present", "cause": null},
  "cwd": {"state": "known", "value": "/home/mike/work/agentd-smoke", "cause": null},
  "activity": {"state": "unknown", "source": "none", "observedAtUnixMs": null},
  "tty": "pts/13",
  "tmux": {"session": "agents", "windowIndex": 2, "windowName": "spec", "paneId": "%7"},
  "name": "Agentd spec",
  "startedAtUnixMs": 1787555200120
}
```

I2.2. `tty` is a canonical-tty string or null. `tmux` is the exact object in Terms or
null. `name` is a display-name string or null. `startedAtUnixMs` is an unsigned 64-bit
integer or null. Each key is present, including when its value is null.

I2.3. The top-level schema value remains `agentd.snapshot.v1`. The top-level snapshot,
scan, issue, identity, presence, cwd, and activity field sets do not otherwise change.

I2.4. JSON `agentd list --json` and `agentd watch --json` continue to emit daemon frames
unchanged followed by LF.

### I3 — Stat parsing produces identity and tty without guessing

I3.1. The scanner finds the first `(` and final `)` in `/proc/<pid>/stat`. It parses
the PID before the first `(` and fields 3 onward after the final `)`. Spaces or right
parentheses in `comm` cannot shift `tty_nr` or `starttime`.

I3.2. The scanner parses field 7 as a signed 32-bit integer and field 22 as a positive
unsigned 64-bit integer. A missing field, invalid integer, mismatched PID, zero start
time, or out-of-range value makes that stat read invalid under the base failure rules.

I3.3. A present agent gets a non-null tty only when its two identity-validating stat
reads report the same `tty_nr` and Terms can canonicalize it. Zero produces null. A
changed or unrepresentable `tty_nr` produces null tty and null tmux for that scan; it
does not change the process's proven presence.

I3.4. Agentd does not inspect `/proc/<pid>/fd`, `/proc/<pid>/cmdline`, or
`/proc/<pid>/environ` to fill a display field.

### I4 — Tmux is one bounded, fail-open observation per scan

I4.1. The scanner starts at most one tmux command per scan. It constructs one complete
tty-to-location index from that command and reuses the index for each agent in the
scan.

I4.2. Agentd executes tmux directly without a shell. It applies one 250 ms total
deadline and a 1,048,576-byte stdout limit. The deadline bounds waiting; it does not
decide whether an agent belongs to tmux.

I4.3. A missing executable, spawn failure, timeout, nonzero exit, signal, stdout-limit
breach, or non-UTF-8 output produces an empty index. The procfs scan still commits.
Each agent has `tmux=null`. The scan state and scan issues do not report a tmux failure.

I4.4. One malformed row invalidates only that row when row boundaries remain known.
An invalid whole output encoding or size invalidates the complete index.

I4.5. Zero matching rows produces null. More than one accepted row for a canonical tty
is ambiguous and produces null. Agentd does not choose a first or last row.

I4.6. The location is the observation made in that scan. Agentd does not claim the pane
still exists at commit time. A later scan replaces or clears stale metadata when its
one new observation differs. Agentd does not run a second tmux command to close this
race.

I4.7. Tmux output supplies only pane tty, session name, window index, window name, and
pane ID. Agentd requests, parses, stores, emits, and logs no pane command, pane title,
terminal title, screen content, history, environment, or current command.

### I5 — Started-at conversion is exact or null

I5.1. The scanner reads `/proc/stat` at most once per scan and samples
`sysconf(_SC_CLK_TCK)` at most once per scan. It reuses those values for each agent.

I5.2. A read failure, missing or duplicate `btime` row, non-decimal or overflowing
`btime`, nonpositive or unrepresentable tick rate, multiplication overflow, addition
overflow, or result outside unsigned 64-bit range produces `startedAtUnixMs=null` for
the affected scan or agent. Agentd does not substitute the current wall clock.

I5.3. A timestamp-conversion failure does not change presence, degrade the scan, add a
scan issue, or stop publication. A later valid scan can replace null with an integer.

I5.4. For one exact identity and unchanged boot inputs, the calculation in Terms
produces the same integer on each scan.

### I6 — Name requests bind to a present exact identity

I6.1. The version-1 request set adds exactly these shapes:

```json
{"version":1,"op":"name","agent":{"pid":930481,"startTimeTicks":1787554},"name":"Agentd spec"}
{"version":1,"op":"name","agent":{"pid":930481,"startTimeTicks":1787554},"name":null}
```

Each request contains exactly the fields shown. Duplicate, missing, or extra fields are
`malformed_request`. A string outside the display-name definition is `invalid_name`.

I6.2. Without releasing the base observe-then-commit seam, the name handler resolves
the exact identity and verifies `presence.state=present`. An absent, unknown, removed,
or reused identity returns `unknown_agent`. It changes no registry, snapshot, revision,
or other identity.

I6.3. A string sets the name. Null clears it. Setting the current value or clearing an
already-null value returns the ordinary acknowledgement with the retained revision,
writes no registry replacement, and offers no subscriber frame.

I6.4. A changed request commits its registry replacement before it swaps the changed
snapshot. A registry validation, directory, temporary-file, write, flush, mode,
ownership, or rename failure returns `name_store_unavailable`, leaves the current
snapshot and revision unchanged, and offers no frame.

I6.5. After a successful changed request, the snapshot contains the new name or null,
the revision increments once with `reason=roster_changed`, the daemon offers the
complete snapshot to each subscriber, and the handler returns the ordinary v0.2.0
acknowledgement.

I6.6. The error-code set adds `invalid_name` and `name_store_unavailable`. The error
frame retains the v0.2.0 exact fields. Its message does not echo the rejected name or
request bytes.

I6.7. A scan proposal does not own display names. At scan commit, the mutation seam
reads the then-current eligible registry value for each exact proposed identity. A scan
that started before a name set or clear cannot overwrite or resurrect that mutation.

### I7 — Name CLI and optional Claude adapter are privacy-safe

I7.1. The CLI adds these exact manual forms:

```text
agentd name --pid <positive-u32> <NAME>
agentd name --pid <positive-u32> --clear
```

The set form accepts one argv value as `NAME`. The CLI validates the name, reads the
PID's current stat record with the base parser, sends an exact name request, and accepts
only the ordinary acknowledgement. The clear form sends null.

I7.2. If the process exits or its start time changes between the CLI stat read and the
daemon commit, the daemon returns `unknown_agent`. The CLI exits 1, names that code,
and does not retry against the new identity.

I7.3. A successful manual set or clear exits 0 and writes nothing to stdout or stderr.
A usage, procfs, socket, protocol, validation, unknown-agent, or store error exits 1 and
writes one error line without echoing the name.

I7.4. The CLI also exposes this optional user-authored Claude hook form:

```text
agentd name --from-claude-session-start <NAME>
```

It accepts the name only from the argv value. It drains stdin without parsing, storing,
logging, or sending it. It maps its process ancestry to the existing Claude roster root
with the reviewed v0.2.0 hook resolver and sends the same exact name request.

I7.5. The optional adapter applies the reviewed hook 500 ms total deadline and typed
fail-open behavior. A valid-name operational failure writes
`agentd name: <code>` to stderr and exits 0. `<code>` is one of
`runtime_directory_unavailable`, `socket_unavailable`, `protocol_error`,
`ancestry_unresolved`, `process_identity_changed`, `unknown_agent`,
`name_store_unavailable`, or `deadline_exceeded`. Success writes nothing and exits 0.
An invalid CLI shape or invalid name exits 1 before opening the daemon socket.

I7.6. `agentd integrate install claude` and uninstall retain the reviewed v0.2.0 exact
four activity mappings. They do not install, remove, or claim ownership of a
`SessionStart` name hook.

### I8 — Name retention is bounded by boot and process identity

I8.1. The daemon creates the Agentd state directory with mode `0700` and the name file
with mode `0600`. It accepts an existing directory only when `lstat` reports a
non-symlink directory owned by the daemon user with mode `0700`. It accepts an existing
file only when `lstat` reports a regular, non-symlink file owned by that user with mode
`0600`. A safety failure makes name mutation unavailable but does not stop procfs
roster service.

I8.2. The file uses this exact versioned JSON shape and orders entries by
`(pid,startTimeTicks)`:

```json
{
  "version": 1,
  "bootId": "8ddf97c5-8f38-4db7-ae9d-3cc8ac70df44",
  "names": [
    {"agent":{"pid":930481,"startTimeTicks":1787554},"name":"Agentd spec"}
  ]
}
```

The boot ID is the lowercase 36-byte hexadecimal-and-hyphen value read from procfs and
must match `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`. Duplicate identities, duplicate
object keys, unknown fields, invalid identities, invalid names, an invalid version, or
an invalid boot-ID shape make the registry unavailable for mutation. The daemon starts
and publishes null names rather than inventing values.

I8.3. Agentd writes a changed registry through one exclusively created same-directory
temporary regular file, sets mode `0600`, flushes the file, atomically renames it, and
then performs the non-fallible in-memory snapshot swap before acknowledging the change.
It leaves no successful temporary file. It creates no journal, backup, history, or
second registry. Crash durability of the directory entry is outside this same-boot
daemon-restart retention contract.

I8.4. At startup, a matching boot ID allows exact live identities to recover their
names. A missing registry yields no names. A different boot ID yields no names and is
replaced by the current boot ID on the next successful registry mutation or cleanup.

I8.5. A scan carries a name only across an exact identity match. A PID start-time
change clears the displayed name for the new identity in the same commit.

I8.6. After a complete scan proves that `/proc/<pid>/stat` is absent or has another
start time, Agentd removes that exact registry entry. Loss and later recovery of
agent-root qualification does not remove the name while procfs still proves the exact
process identity exists.

I8.7. Registry cleanup is best-effort and cannot keep an absent roster record. A cleanup
write failure leaves a stale disk entry but does not attach it to another identity,
degrade the scan, or stop publication. The next successful cleanup or name mutation
removes stale entries before writing.

### I9 — Human display leads with deterministic identity fields

I9.1. The snapshot header and scan-issue lines retain their v0.2.0 formats and order.

I9.2. Each human agent line uses this exact field order:

```text
agent name=<json-string|null> tmux=<json-string|null> cwdBase=<json-string|null> pid=<pid> startTimeTicks=<ticks> startedAtUnixMs=<integer|null> tty=<json-string|null> harness=<harness> presence=<presence> cwd=<json-string|null> activity=<activity>
```

I9.3. A non-null tmux display string is
`<session>:<windowIndex>.<windowName>:<paneId>`. Agentd JSON-encodes each complete
`name`, tmux display string, cwd basename, tty, and full cwd value, including the
surrounding double quotes and escapes. Null prints as the literal `null`.

I9.4. `cwdBase` is the final lexical component of a known absolute cwd. Root `/`
prints as the JSON string `"/"`. An unknown cwd prints null. The later `cwd` field
retains the full known path or null, so the v0.2.0 information remains available.

I9.5. `agentd watch` uses the same human header, issue, and agent-line formats for each
received snapshot.

### I10 — Privacy remains structural

I10.1. Agentd reads display material only from procfs stat, procfs cwd, procfs boot
files, the bounded tmux five-field command, the Agentd name registry, and an explicit
name argv value.

I10.2. Agentd sends and logs no prompt, transcript, model response, tool input,
command line, environment value, pane command, pane title, terminal title, screen text,
or scrollback.

I10.3. A display name and tmux session or window name can be user-sensitive. Agentd
exposes them only through the existing mode-`0600` local socket and human CLI. It makes
no outbound connection and opens no network listener.

I10.4. Error output never echoes a display name, tmux output row, hook stdin, or name
registry bytes.

## Architecture

### A. Scan enrichment

The procfs scanner extends its existing stat record with field 7. After procfs
enumeration succeeds, one bounded tmux runner builds a private tty index. One private
boot-time input supplies started-at conversion. The scanner enriches only validated
agent roots, then submits one complete proposal through the existing observe-then-commit
seam.

The pattern is **one observation index per scan**. It applies to tmux only. It does not
apply to procfs identity validation or hook ancestry. Canonical example: tmux returns
`/dev/pts/13`, session `agents`, window 2, name `spec`, and pane `%7`; a validated root
with canonical tty `pts/13` receives that one location.

The tmux query is added because deleting it would fail G2 and accepting null for each
tmux agent would fail the requested location. A persistent tmux watcher and a second
event stream lose because one bounded per-scan observation meets the MVP and contains
failure.

### B. Exact-identity name mutation

The version-1 socket adds one `name` operation. The CLI resolves PID to exact identity
before sending. The daemon validates present identity again at the existing atomic
state seam. The registry replacement completes before the visible snapshot swap, so a
successful acknowledgement means the name can survive a daemon restart.

The name registry is added because deleting it would fail G3 restart retention and
accepting restart loss would contradict that goal. A general metadata database and
history lose because the required state is one bounded map keyed by existing process
identity.

The registry is the one mutation seam for durable names. Scans can request stale-entry
cleanup; only the registry writer replaces the file. The observe-then-commit seam
remains the one mutation seam for published snapshots.

### C. Optional Claude SessionStart adapter

The optional adapter reuses the reviewed hook ancestry resolver and the same wire name
operation. It takes the name from one explicit argv value and discards stdin. Agentd's
owned integration does not install it. This keeps private hook payload fields outside
the product while allowing a user who already owns a SessionStart hook to supply a
constant display name.

A new automatic integration entry loses because the MVP does not define who chooses
the per-session name. Parsing Claude's private payload loses because no payload field
is required to set the explicit argv value.

### D. Compatibility and release boundary

The response schema remains `agentd.snapshot.v1` because the four fields are additive
and nullable. The protocol version remains 1 because old operations and frame meanings
do not change. The `name` operation is capability-additive: an old daemon rejects it as
unknown; a v0.3 daemon accepts it.

The implementation updates the product version once from `0.2.0` to `0.3.0`. It cuts
one `v0.3.0` release only after the exact implementation commit passes review and the
acceptance below. No v0.3.0 release candidate, second release number, or compatibility
alias is in scope.

The operating pattern taught to Tightbeam agents is **none**. This product amendment
does not require Tightbeam guidance.

## Acceptance

Each case is a concrete pass/fail contract. Tests use captured real responses when a
real external response is part of the contract; they do not fabricate an ideal tmux or
procfs capture and label it real.

### A1 — Additive snapshot and unchanged base behavior (G2, G5; I1, I2)

**Given** the reviewed v0.2.0 fixture with one agent, **when** the v0.3 serializer emits
it with unavailable enrichment, **then** the frame retains each v0.2 field and value,
adds `tty:null`, `tmux:null`, `name:null`, and `startedAtUnixMs:null`, and retains schema
`agentd.snapshot.v1`.

**Given** records with distinct enrichment values, **when** a scan commits, **then**
the serializer still orders them by `(harness,pid,startTimeTicks)`. A change to one new
field increments the revision once with `reason=roster_changed`. A timestamp-only scan
retains the revision and emits no subscriber frame.

**Given** a v0.3 consumer and a captured v0.2.0 frame without the four fields, **when**
it decodes the frame, **then** it exposes each new value as null. **Given** a JSON
consumer that ignores unknown agent fields, **when** it decodes a v0.3 frame, **then**
the v0.2 values retain their meanings.

### A2 — Parenthesized comm, tty, and timestamps (G2; I3, I5)

**Given** a captured real-shaped stat record whose `comm` contains spaces and a right
parenthesis, tty number encodes `/dev/pts/13`, and field 22 is 250 ticks, **when** the
parser uses boot time 1,700,000,000 seconds and 100 ticks per second, **then** it returns
tty `pts/13` and `startedAtUnixMs=1700000002500` without shifting either field.

**Given** `tty_nr=0`, two different tty numbers across the validating stat reads, or an
unrepresentable number, **when** the scan commits a present root, **then** tty and tmux
are null.

**Given** each of a missing `btime`, duplicate `btime`, invalid tick rate, overflowing
boot multiplication, overflowing tick conversion, and overflowing sum, **when** the
scan commits, **then** `startedAtUnixMs` is null, presence remains proven, and the scan
does not become degraded because of the conversion.

### A3 — One bounded tmux index and ambiguity (G2; I4)

**Given** a captured real `tmux list-panes` response with two panes and one agent tty
matching exactly one row, **when** one scan processes three agents, **then** the runner
was invoked once and the matching record contains the exact session, window index,
window name, and pane ID. Nonmatching records contain null.

**Given** two accepted rows with the same canonical tty, **when** the index builds,
**then** that tty is absent from the index and the record's tmux value is null.

**Given** one malformed row among valid bounded UTF-8 rows, **when** the index builds,
**then** only that row is discarded. **Given** invalid UTF-8, output above 1,048,576
bytes, timeout, nonzero exit, signal, spawn failure, or an absent tmux executable,
**when** the scan completes, **then** each tmux value is null, the snapshot still
commits, and no tmux scan issue appears.

**Given** the pane changes after the one tmux observation, **when** that scan commits,
**then** the snapshot can contain the observed prior location. **When** the next scan
observes the change, **then** it replaces or clears the value and increments the
revision once if serialized state changed.

### A4 — Name validation, set, clear, and stale refusal (G3; I6, I7)

**Given** a present agent and a 64-byte valid UTF-8 name, **when** the user runs the set
form, **then** the CLI exits 0 silently, the daemon acknowledges a new revision, the
next snapshot contains the exact name, and a subscriber receives one complete
`roster_changed` frame.

**Given** that value, **when** the user sets the same bytes again, **then** the daemon
retains the revision, writes no registry replacement, and emits no frame. **When** the
user runs the clear form, **then** the next snapshot contains null and the command exits
0 silently. A second clear is a no-op.

**Given** an empty string, 65-byte UTF-8 string, invalid UTF-8 argv, or a string with a
Unicode control character, **when** the CLI or wire handler validates it, **then** it
rejects the value before mutation and does not echo it.

**Given** a PID whose CLI stat read reports start time 100, **when** the daemon has no
present `{pid,100}` or now has `{pid,200}`, **then** it returns `unknown_agent`, changes
no name, registry, snapshot, or revision, and does not retry against `{pid,200}`.

**Given** a scan proposal captured a record before a name set or clear, **when** the
name mutation commits first and that scan commits later for the same exact identity,
**then** the later snapshot retains the then-current registry name. It does not restore
the proposal's older name value.

### A5 — Name lifetime, restart retention, and cleanup (G3; I8)

**Given** a successfully named live identity and its mode-`0600` registry under a
mode-`0700` state directory, **when** the daemon restarts during the same boot while
that identity remains live, **then** the new instance starts at revision 1 with the
same name and activity `unknown`.

**Given** that process remains live but temporarily loses and regains roster-root
qualification, **when** scans commit both transitions, **then** the recovered exact
identity retains its name and resets activity under the base rule.

**Given** procfs proves the identity exited or the PID has another start time, **when**
cleanup succeeds, **then** the old name is absent from the roster and registry. A new
identity at the PID has name null.

**Given** a different boot ID, malformed registry, unsafe symlink, wrong owner, or
cleanup write failure, **when** the daemon starts or scans, **then** roster service
continues with no invented name. A name mutation returns `name_store_unavailable`
until a safe registry write can complete. No stale entry attaches to another identity.

### A6 — Optional Claude input discards private payload (G3, G5; I7, I10)

**Given** a user-authored Claude `SessionStart` hook that invokes the optional adapter
with name `Review lane` and sends stdin containing prompt, cwd, session, transcript,
and sentinel fields, **when** the adapter maps a present Claude root, **then** only the
explicit argv name and exact identity reach the daemon. The snapshot reports
`Review lane`. The sentinel does not appear in socket frames, registry, stdout, stderr,
or daemon logs.

**Given** an absent socket or unresolved ancestry, **when** that hook runs, **then** it
exits 0 within 750 ms with one typed diagnostic and Claude continues. **Given** the
reviewed automatic Claude integration, **when** install and uninstall run, **then** its
exact four activity mappings and ownership behavior remain unchanged and no
`SessionStart` name hook is added or removed.

### A7 — Human output (G4; I9)

**Given** a named tmux agent with cwd `/home/mike/work/agentd`, **when** the user runs
`agentd list`, **then** its line begins
`agent name="Agentd spec" tmux="agents:2.spec:%7" cwdBase="agentd"` and later includes
the exact PID, ticks, started-at value, tty, harness, presence, full cwd, and activity
in I9.2 order.

**Given** null name, tmux, tty, started-at, and unknown cwd, **when** the user runs
`agentd list`, **then** the line begins `agent name=null tmux=null cwdBase=null` and
prints each other null fallback exactly. Header, issue lines, degraded-snapshot exit
behavior, and zero-agent behavior remain unchanged.

### A8 — Real Gibson and Osanwe matrix (G6; I1-I10)

**Given** the same reviewed v0.3.0 candidate bytes on Gibson and Osanwe, **when** an
operator runs the matrix below as the daemon user on each host, **then** the evidence
records the host, kernel, exact product commit, binary SHA-256, tmux version, boot ID,
tick rate, daemon instance IDs, exact process identities, commands, exit codes, and
teardown without recording private hook input or terminal content.

On each host the matrix proves:

1. One real harness root inside tmux reports canonical tty and the exact pane's session,
   window index, window name, and pane ID.
2. One real harness root outside tmux reports its procfs-derived tty or null and
   `tmux=null`.
3. Manual set, identical-set no-op, daemon restart retention, clear, identical-clear
   no-op, and a wrong-start-time raw request produce the A4 and A5 outcomes.
4. Independent arithmetic from captured `/proc/stat`, the real root's stat field 22,
   and `getconf CLK_TCK` equals `startedAtUnixMs` exactly.
5. An isolated foreground daemon with a fresh mode-`0700` runtime directory, fresh
   state directory, and a PATH containing no tmux executable publishes each agent with
   `tmux=null`; snapshot, list, watch, activity, and name operations continue.
6. A daemon restart changes instance ID, resets activity, retains an eligible name,
   re-observes tty, tmux, cwd, and started-at, and preserves the v0.2 service/socket
   contract.
7. Non-secret random sentinels placed in a harness command line, environment, OSC
   title, pane screen text, prompt, and transcript do not appear in Agentd JSON,
   human output, registry, diagnostics, service journal, or accepted evidence. The
   tmux window name uses a separate structural value because it is intentionally
   emitted.

The isolated absent-tmux check does not replace or stop the installed service. It uses
another `XDG_RUNTIME_DIR` and `XDG_STATE_HOME`, invokes the candidate by absolute path,
and removes its temporary state after recording teardown.

### A9 — Base regression, repository gate, and release boundary (G5; I1)

**Given** the exact implementation commit proposed for code review, **when** a clean
Linux checkout runs the reviewed v0.2.0 format, clippy, library, integration, base real
smoke, and real harness-integration commands plus the v0.3 tests above, **then** each
command exits 0 and the report records baseline and after counts.

**Given** the unchanged reviewed code commit and successful Gibson and Osanwe matrix,
**when** the release owner builds v0.3.0 assets, **then** one `v0.3.0` release identifies
that commit and publishes deterministic assets plus `SHA256SUMS`. Independent release
review verifies the published bytes before either host installs them.

This acceptance case does not authorize this spec writer to review, implement, release,
install, restart a live service, or mutate Gibson or Osanwe runtime state.

## Open Questions

Blocking questions: none.

Non-blocking questions: none.

The independent exact-hash spec review can return a defect against this amendment. A
finding does not authorize implementation. The producer must amend this canonical file
first, push the revision, and present its new content hash before review continues.
