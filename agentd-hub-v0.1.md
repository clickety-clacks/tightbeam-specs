# agentd-hub v0.1 — multi-machine roster aggregator

Status: READY FOR INDEPENDENT REVIEW

Date: 2026-08-31

Work item: `wi_c99729de-3737-42b1-b050-037f0011b0af`

Canonical product repository: `https://github.com/clickety-clacks/agentd-hub`

Authority:

- Mike's ruled work-item text is the product authority for this MVP.
- `agentd-hub-spirit-v1.md` at tightbeam-specs commit
  `e9b6b29dc8df20af1376c5296c4d5ec53317a47d`, SHA-256
  `e3d126c4a6cddc35fdb9e025b3acef51ca055275cee150554c6e1eae60d3268a`,
  supplies the product invariants.
- Current Agentd contract and release evidence comes from `clickety-clacks/agentd`
  commit `73002f23d9f2ab6874298e1fdc37c80033166263` (release `v0.3.2`).
- Implementation starts only after one independent review clears one exact revision of
  this file.

## Invariants

I1. The hub observes Agentd snapshots. It does not send commands to agents, inject
terminal input, answer permission prompts, or control a harness.

I2. Agentd remains a local Linux user service with no network listener, network
credential, or hub-specific protocol. The hub reaches each source only by running the
documented Agentd CLI through the user's existing SSH access.

I3. Each hub emission is complete current state. A consumer replaces its prior state
with the new snapshot. The hub does not emit diffs, cursors, or replay data.

I4. The hub identifies an agent by the tuple `(machine, instanceId, pid,
startTimeTicks)`. It does not compare or merge process IDs across machines.

I5. The hub represents each discovered machine as a source row. A failed source stays
visible with explicit health. The hub does not turn stale source data into a different
agent activity or presence state.

I6. The hub exposes no prompt, transcript, command line, environment value, SSH stderr,
or terminal content. It passes through only the Agentd snapshot fields named in this
specification, plus hub-owned machine and health fields.

I7. The HTTP server listens on an IPv4 or IPv6 loopback address. The hub contains no
authentication mechanism. A deployment that exposes the listener owns that decision.

I8. The hub keeps no database, roster file, event journal, or replay log. A restart
rebuilds the roster by discovering, probing, and subscribing to sources again.

I9. The product has one mutation seam for in-memory current state: a valid source
snapshot or a source-health transition atomically creates the next complete hub
snapshot and increments the hub revision once.

## Goal

G1. A user can run one `agentd-hub` process and see one truthful current roster from
the user's reachable Agentd machines.

G2. A local HTTP consumer can fetch that roster once or subscribe to complete snapshot
updates.

G3. A user can inspect the same roster in a minimal browser page without installing a
separate front end.

G4. The first public release, `v0.1.0`, uses the same gated, tag-triggered,
reproducible-release pattern as Agentd.

## Non-Goals

- Changing the Agentd wire schema, CLI, daemon, socket, privacy contract, or Linux-only
  backend.
- Adding a network listener or discovery service to Agentd.
- Sending commands, terminal input, harness requests, or permission responses through
  the hub.
- Adding WebSocket, diffs, cursors, event replay, durable history, a database, or a
  cache that survives restart.
- Adding mDNS, broadcast discovery, port scanning, or a per-machine discovery daemon.
- Adding hub authentication or authorizing non-loopback binding.
- Adding a macOS Agentd backend.
- Replacing a PTY-owning host or implementing a tmux reply adapter.
- Hiding a source, an unknown Agentd value, or the age of an activity claim to make the
  roster appear healthier.
- Supporting browsers without native `EventSource`.

## Terms

**Machine** is the stable SSH target string for one source. For Tailscale discovery it
is the peer's `DNSName` with one trailing dot removed. For the hosts-file fallback it is
the trimmed line exactly as written. The hub does not resolve aliases or merge two
machine strings.

**Source** is one machine plus one supervision lane. The lane owns at most one child
process that runs `ssh <machine> agentd watch --json` and owns that source's reconnect
timer while no child runs.

**Discovery probe** is one startup execution of
`ssh <machine> agentd list --json`. It decides whether a candidate becomes a source; it
does not supply continuing state.

**Valid Agentd snapshot** is one newline-delimited JSON object with `type="snapshot"`,
`schema="agentd.snapshot.v1"`, a non-empty string `instanceId`, unsigned-integer
`revision` and `observedAtUnixMs`, an Agentd `scan` object, and an `agents` array. Each
agent satisfies Architecture A4. The hub ignores additive fields that it does not
project.

**Hub snapshot** is the complete JSON object defined in Architecture A5. The current
hub snapshot is the only roster state served by `/snapshot`, `/events`, and `/`.

**Hub revision** is a process-local unsigned 64-bit integer. The first published hub
snapshot has revision `1`. Each atomic state change increments it by one. A restart can
start again at `1`; it is not a durable cursor.

**Source health** is exactly one of:

- `reporting`: the hub has accepted a snapshot from the current watch child;
- `not_reached`: the hub has not obtained a valid snapshot since `sinceUnixMs`;
- `no_agentd`: an SSH connection ran the remote shell and reported that `agentd` does
  not exist or cannot execute.

**Claim age** is the browser's current Unix time minus `activity.observedAtUnixMs` when
Agentd supplies an observation time that is not in the browser's future. It is unknown
otherwise. The JSON API preserves the source timestamp.

## Assumptions

- Each intended machine accepts non-interactive SSH from the hub host through the
  user's existing SSH configuration.
- Each reporting machine runs Agentd v0.3-compatible CLI output with schema marker
  `agentd.snapshot.v1`.
- `tailscale status --json` returns peer objects with `DNSName` values when Tailscale
  discovery is available.
- A supplied hosts file is UTF-8 text with one SSH target per non-empty line. A line
  whose first non-space character is `#` is a comment.
- The hub host supplies a monotonic timer for reconnect scheduling and a Unix wall
  clock for JSON timestamps.
- The static page and API share one process and one listener.

## Architecture

### A1 — Process and listener

The product is one Rust binary named `agentd-hub`. It starts one HTTP server that
defaults to `127.0.0.1:8787`. A listen option may select another port or a loopback IPv4
or IPv6 address. The binary rejects a non-loopback address before discovery or SSH.
The server begins accepting requests after discovery produces the complete initial hub
snapshot at revision `1` and before watch children can publish a later revision.

The server exposes exactly three successful routes in v0.1:

- `GET /snapshot` returns the current hub snapshot as `application/json`.
- `GET /events` returns an SSE stream.
- `GET /` returns one self-contained HTML document with inline CSS and JavaScript.

Another method or path returns a non-success status and does not mutate hub state.

### A2 — Discovery

At startup the hub runs `tailscale status --json` once. It takes the non-empty
`DNSName` from the top-level `Self` object and each non-empty `DNSName` from the values
of the top-level `Peer` map. It removes one trailing dot, sorts the resulting strings,
and removes exact duplicates. It probes each resulting machine once.

The CLI accepts `--hosts-file <path>`. The hub reads this file only when the Tailscale
command fails, its JSON is invalid, or it yields no machine. The hub trims each line,
ignores blank and comment lines, sorts the targets, removes exact duplicates, and
probes each target once. Startup fails with a typed diagnostic when no discovery path
produces a target.

Each probe uses SSH batch mode, a 10-second SSH connection timeout, and a 10-second
whole-probe deadline. At the whole-probe deadline, the hub terminates the probe and
records `not_reached`. A candidate becomes a source when the probe returns a valid
Agentd snapshot, proves `no_agentd`, or fails to yield a valid snapshot. Thus a known
candidate remains visible even when it cannot report.

The hub assembles the sorted probe results into one initial snapshot. It sets that
snapshot's revision to `1`; individual probe completions do not publish intermediate
snapshots.

### A3 — Watch supervision and health

The hub starts exactly one watch child per source. A source has no overlapping watch
children. The child runs non-interactively as
`ssh <machine> agentd watch --json` with SSH batch mode and a 10-second connection
timeout, and reads newline-delimited complete snapshots.

The first reconnect delay is 1 second. Consecutive unsuccessful attempts wait 2, 4, 8,
16, then 30 seconds; later attempts remain at 30 seconds. Acceptance of one valid
snapshot resets the next delay to 1 second. The hub schedules from child exit or
invalid-frame detection, so checking and scheduling form one state transition. On an
invalid frame, the hub terminates that watch child before it schedules a replacement.

When a source first fails to yield a valid snapshot, health becomes `not_reached` and
`sinceUnixMs` records that transition time. Further failures keep the same time. If the
hub has an earlier valid snapshot for that source, it retains those agents unchanged
while the source is `not_reached`.

When SSH establishes the remote session and the remote command exits `126` or `127`
before a valid frame, health becomes `no_agentd`, the source's agent list becomes
empty, and the hub continues the same reconnect schedule. The API exposes a stable
health code, not remote stderr.

Acceptance of a valid snapshot atomically replaces that source's prior Agentd state,
sets health to `reporting`, records the hub acceptance time as
`health.observedAtUnixMs`, and publishes one new hub snapshot. Each accepted frame
publishes one revision, including when its JSON equals the prior frame.

### A4 — Agent projection and identity

For each Agentd record, the hub emits one agent object with `machine` and `instanceId`
from the source, followed by these Agentd v0.3 fields without reinterpretation:

`id`, `harness`, `detectedBy`, `presence`, `cwd`, `activity`, `tty`, `tmux`, `name`, and
`startedAtUnixMs`.

The hub requires `id.pid`, `id.startTimeTicks`, `harness`, `detectedBy`, `presence`,
`cwd`, and `activity` with the Agentd v0.3 JSON types. It treats absent v0.3 fields
`tty`, `tmux`, `name`, and `startedAtUnixMs` as `null`. It preserves Agentd's explicit
unknown objects and values. It sorts agents by machine, instance ID, PID, then
start-time ticks.

### A5 — Hub snapshot JSON

The JSON object has this closed hub-owned shape. `scan` and each projected Agentd field
retain their Agentd JSON shape. The hub sorts `sources` by machine.

```json
{
  "type": "snapshot",
  "schema": "agentd-hub.snapshot.v1",
  "revision": 7,
  "observedAtUnixMs": 1788200000000,
  "sources": [
    {
      "machine": "gibson.example.ts.net",
      "health": {"state": "reporting", "observedAtUnixMs": 1788200000000},
      "instanceId": "0123456789abcdef0123456789abcdef",
      "sourceRevision": 42,
      "sourceObservedAtUnixMs": 1788199999000,
      "scan": {"state": "complete", "issues": []}
    }
  ],
  "agents": [
    {
      "machine": "gibson.example.ts.net",
      "instanceId": "0123456789abcdef0123456789abcdef",
      "id": {"pid": 930481, "startTimeTicks": 987654},
      "harness": "codex",
      "detectedBy": "proc_comm",
      "presence": {"state": "present", "cause": null},
      "cwd": {"state": "known", "value": "/work/agentd", "cause": null},
      "activity": {"state": "needs_attention", "source": "hook", "observedAtUnixMs": 1788199990000},
      "tty": "pts/13",
      "tmux": {"session": "agents", "windowIndex": 2, "windowName": "spec", "paneId": "%7"},
      "name": "Agentd spec",
      "startedAtUnixMs": 1788190000000
    }
  ]
}
```

For `not_reached`, `health` is
`{"state":"not_reached","sinceUnixMs":<u64>}`. For `no_agentd`, it is
`{"state":"no_agentd","observedAtUnixMs":<u64>}`. A source without an accepted
snapshot uses `null` for `instanceId`, `sourceRevision`, `sourceObservedAtUnixMs`, and
`scan`.

### A6 — SSE

Each SSE message uses event name `snapshot`, decimal hub revision as `id`, and the
complete hub snapshot JSON as one `data` value. The first message on each connection is
the current snapshot. Each later message is the next complete snapshot. Reconnection
ignores `Last-Event-ID`; it sends current state and performs no replay.

The server gives each client one replaceable pending-snapshot slot. A new revision
replaces an unsent older revision in that slot. The server removes a disconnected
client without changing the hub revision. A slow client may skip intermediate
revisions, but its next delivered message is one complete current snapshot.

### A7 — Static page

The root document opens `/events` with native `EventSource` and replaces its rendered
state from each message. It renders one section per source. It sorts sources by machine
and sorts each source's agents with `needs_attention` first, then by display name,
harness, PID, and start-time ticks.

Each source section shows machine and source health. Each agent row shows activity,
claim age or `unknown`, name or `unknown`, harness, PID, cwd or `unknown`, tty or
`unknown`, tmux session/window/pane or `unknown`, and presence. The page does not infer
that an old claim has changed state. It shows claim age as `unknown` when the activity
timestamp is `null` or later than the browser's current wall-clock time. It recomputes
visible claim ages at least once per second without changing hub state.

### A8 — Release and cross-repository pointer

The new repository copies Agentd's CI gates: format, clippy with warnings denied, and
locked tests. Its tag-triggered release verifies equality among Git tag, Cargo package
version, and package-script version; runs the gates; builds with `--release --locked`;
packages twice; compares archive bytes; and publishes the archive plus `SHA256SUMS`.

The package script creates a deterministic `agentd-hub-0.1.0-<rust-host>.tar.gz` from
the built binary and README. The release is created only by pushing the version-bump
commit and matching `v0.1.0` tag. A person or agent does not upload release assets by
hand.

Agentd's README gains one sentence that points users to
`https://github.com/clickety-clacks/agentd-hub` for multi-machine aggregation. No other
Agentd file changes for this MVP.

This spec establishes no new operating pattern for agents.

## Acceptance

A1. **Loopback floor.** Given default startup, when the HTTP server listens, then an
OS socket inspection shows only `127.0.0.1:8787`. Given a requested non-loopback
address, when startup validates it, then the process exits nonzero before SSH starts.

A2. **Discovery choice.** Given valid Tailscale JSON whose self and peer entries produce
three DNS names with one duplicate, when the hub starts, then it probes the two sorted
unique names once and does not read the hosts file. Given a failed Tailscale command
and a hosts file with two targets, blanks, comments, and one duplicate, when the hub
starts, then it probes the two sorted unique targets once.

A3. **Source health.** Given one reporting source, one unreachable target, and one host
without an executable `agentd`, when discovery finishes, then one `/snapshot` response
contains three source rows with health `reporting`, `not_reached`, and `no_agentd` and
does not expose SSH stderr.

A4. **Backoff and single child.** Given a watch child that exits before a valid frame,
when six retry timers fire under a controlled clock, then starts occur after 1, 2, 4,
8, 16, and 30 seconds and no two watch children overlap. Given a later valid frame,
when the next watch attempt fails, then its replacement waits 1 second.

A5. **Identity isolation.** Given two machines whose snapshots contain the same PID and
start-time ticks, when the hub merges them, then `/snapshot` contains two agents with
different `(machine, instanceId, pid, startTimeTicks)` keys.

A6. **Stale truth.** Given a reporting source with one `needs_attention` agent, when its
watch becomes unreachable, then the next snapshot retains that agent unchanged, marks
the source `not_reached` with the first-failure time, and the page shows the source
health and increasing claim age without changing activity.

A7. **Snapshot mutation seam.** Given revision 7, when one valid source frame
arrives, then the source replacement, health transition, merged agents, timestamp, and
revision 8 become visible together. Given a byte-for-byte duplicate frame next, when
the hub accepts it, then the complete current state becomes revision 9 through the same
seam.

A8. **Snapshot-first SSE.** Given current revision 8, when a client connects to
`/events` with or without `Last-Event-ID`, then its first event is named `snapshot`, has
ID `8`, and contains the same JSON value as `/snapshot`. Given a later source change,
when the hub publishes revision 9, then the client's next event contains the complete
revision 9 snapshot.

A9. **Slow subscriber.** Given a subscriber that cannot consume revisions 10 through
12, when it next receives an event, then the event is one complete current snapshot;
the hub does not replay the three missed revisions or disconnect another subscriber.

A10. **Static page.** Given two sources and agents in mixed activity states, when a
browser opens `/`, then it shows machine sections, source health, Agentd v0.3 name and
tmux fields, cwd, tty, presence, and claim ages; within each source it places
`needs_attention` agents first.

A11. **Privacy.** Given fixtures whose SSH stderr and local process environment contain
unique sentinels, when tests fetch `/snapshot`, consume `/events`, and render `/`, then
none of those response bytes contains a sentinel, prompt, transcript, command line, or
environment value.

A12. **Restart.** Given a populated hub, when the process stops and restarts with the
same discovery inputs, then it reads no prior roster or revision from disk, discovers
and subscribes again, and publishes a new revision 1 snapshot.

A13. **Routes.** Given a running hub, when a client requests `/snapshot`, `/events`, and
`/`, then each returns its specified media type. Given the same running hub, when a
client requests another path or uses a mutating method, then the server returns
non-success and the hub revision does not change.

A14. **Real SSH smoke.** Given two reachable Linux hosts running current Agentd and one
authorized SSH identity, when `agentd-hub` runs against them, then a real browser and
`curl` observe both machine sections. Given that running hub, when one real Agentd claim
changes, then the next SSE event is a complete snapshot. Given that running hub, when
one SSH path stops, then the affected source remains visible as `not_reached`.

A15. **Release.** Given the `0.1.0` version-bump commit, when CI runs on tag `v0.1.0`,
then version parity passes, all Rust gates pass, two package runs produce identical
archives, `SHA256SUMS` verifies the published archive, and the GitHub release contains
only CI-built assets.

A16. **Agentd separation.** Given the completed MVP changes, when reviewers compare the
Agentd repository with its prior revision, then only one README sentence points to the
hub; Agentd has no listener, hub protocol, discovery logic, or other source change.

## Open Questions

- **NON-BLOCKING — browser styling:** The MVP has no visual-design requirement beyond
  A10. The builder chooses accessible native HTML and CSS without adding a front-end
  framework or another route.
- **BLOCKING:** none.
