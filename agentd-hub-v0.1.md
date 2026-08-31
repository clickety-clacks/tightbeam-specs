# Agentd-hub v0.1

Status: candidate for one independent exact-revision review.

Authority: work item `wi_c99729de-3737-42b1-b050-037f0011b0af`, Mike's
2026-08-31 ruling, and `agentd-hub-spirit-v1.md`.

Agentd source baseline: `clickety-clacks/agentd` commit
`73002f23d9f2ab6874298e1fdc37c80033166263` (v0.3.2).

## Invariants

I1. Agentd-hub is a separate product in `clickety-clacks/agentd-hub`. Agentd
remains a local Linux user service with no network listener, remote transport,
hub credential, or hub-specific protocol.

I2. The hub observes. It does not inject input, answer prompts, steer agents, or
offer a command endpoint.

I3. Each source uses the user's existing SSH authorization. The hub starts one
`ssh <machine> agentd watch --json` child for that source and does not install a
daemon or discovery service on the source.

I4. Each hub emission is a complete current snapshot. A consumer does not need
an earlier event to interpret a later event.

I5. The hub identifies an agent by `(machine, instanceId, pid,
startTimeTicks)`. It does not compare a PID from one machine with a PID from
another machine.

I6. A source failure changes visible source health. It does not erase the last
valid source snapshot or silently remove a configured source.

I7. The hub stores no durable roster, event, revision, or source-health history.
A restart discovers sources again, resubscribes, and starts a new hub revision
sequence.

I8. The HTTP server binds only an IP loopback address. The hub has no
authentication system. A deployment that exposes the loopback service owns its
access control.

I9. The hub does not collect or emit prompts, transcripts, terminal contents,
command lines, environment values, SSH stderr, or credentials. It carries only
the Agentd snapshot fields and hub source metadata defined here.

I10. Version 0.1 stays a small snapshot viewer. A future command plane is a
separate additive design and cannot reuse the observation endpoints as a
command channel.

## Goal

Ship `agentd-hub` v0.1.0 as a read-only, stateless multi-machine consumer of
Agentd. It discovers or accepts SSH sources, keeps one Agentd watch subscription
per source, serves a merged snapshot through JSON and server-sent events, and
serves a minimal browser page from the same loopback HTTP server.

## Non-Goals

- Changes to the Agentd wire schema, daemon, socket, integrations, or release
  other than one README pointer to Agentd-hub.
- A network listener, remote transport, or credential in Agentd.
- WebSocket, snapshot diffs, replay, cursors, or `Last-Event-ID` recovery.
- Input injection, tmux replies, harness control planes, or another command
  mechanism.
- An Agentd macOS observation backend.
- mDNS, port scanning, a per-machine discovery daemon, or continuous tailnet
  membership reconciliation.
- A database, on-disk cache, durable roster, or durable hub revision.
- Hub authentication, TLS termination, public binding, or Tailscale Serve
  configuration.
- A general dashboard framework, filtering language, plug-in system, or user
  preferences.

## Terms

- **Agentd frame**: one newline-delimited JSON snapshot emitted by the current
  documented `agentd list --json` or `agentd watch --json` command. Its schema
  marker is `agentd.snapshot.v1`.
- **candidate machine**: one SSH target obtained from tailnet discovery or the
  hosts file before an Agentd probe succeeds.
- **machine**: the stable hub source name. The hub trims the candidate token,
  converts ASCII letters to lowercase, and removes one trailing dot. Accepted
  tokens match `[A-Za-z0-9][A-Za-z0-9._-]*`; this excludes SSH options,
  usernames, whitespace, and shell syntax.
- **source**: one machine row retained for the process lifetime and supervised
  by one reconnect loop.
- **valid frame**: a JSON object accepted by the compatible subset of the
  current Agentd snapshot contract. It requires `type == "snapshot"`,
  `schema == "agentd.snapshot.v1"`, a non-empty string `instanceId`, unsigned
  integer `revision` and `observedAtUnixMs`, string `reason`, an object `scan`,
  and an `agents` array. Each agent requires unsigned integer `id.pid` and
  `id.startTimeTicks`, string `harness`, object `presence`, object `cwd`, and an
  `activity` object with string `state` and null or unsigned integer
  `observedAtUnixMs`. When present, `name` and `tty` are string or null,
  `startedAtUnixMs` is an unsigned integer or null, and `tmux` is an object or
  null. The hub retains the baseline frame fields `type`, `reason`, `schema`,
  `instanceId`, `revision`, `observedAtUnixMs`, `scan`, and `agents`. Within
  them it retains the baseline nested fields for scan issues, agent identity,
  harness, detection, presence, cwd, activity, tty, tmux, name, and start time.
  It preserves those values without semantic translation and omits additive
  fields that this spec does not name.
- **hub snapshot**: the complete JSON value served by `/snapshot` and carried
  in each `/events` event.
- **hub revision**: a process-local unsigned 64-bit integer. It starts at 1 and
  increases by one when the externally visible hub snapshot changes.
- **health transition time**: Unix time in milliseconds captured when a source
  enters its current health state. A reconnect attempt that leaves the state
  unchanged does not change this value.
- **claim age**: browser current time minus `activity.observedAtUnixMs`. The
  page shows `unknown` when that Agentd value is null and `clock ahead` when the
  value is later than browser current time.

## Assumptions

- Each source that can report has a current Agentd executable on the remote
  command path and an Agentd user service available to that command.
- Existing non-interactive SSH authorization is already configured outside the
  hub. The hub does not ask for, store, or repair SSH credentials.
- The installed `ssh` supports `BatchMode=yes` and `ConnectTimeout=5`.
- Tailnet discovery runs against the installed `tailscale status --json`
  object. Candidate peers expose `DNSName` or, when it is empty, `HostName`.
- Agentd v0.3 frames contain additive `name`, `tmux`, `tty`, and
  `startedAtUnixMs` fields. Their absence remains equivalent to `null` for an
  older compatible frame.
- Machine clocks can differ. The hub displays source timestamps and claim ages
  without using them to infer activity or liveness.
- Rust is the implementation language. The new repository can reuse Agentd's
  locked Cargo, CI, deterministic packaging, and tag-release pattern.

## Architecture

### Process and inputs

The binary is `agentd-hub`. It listens on `127.0.0.1:7317` by default. An
optional `--port <u16>` changes only the port; the binary still binds
`127.0.0.1`. It rejects port 0 outside tests.

The process selects one discovery mode at startup:

1. By default, it runs `tailscale status --json` once. It reads `Peer` entries,
   uses non-empty `DNSName` and otherwise non-empty `HostName`, normalizes and
   deduplicates the tokens, and probes them concurrently once with
   `ssh -o BatchMode=yes -o ConnectTimeout=5 <machine> agentd list --json`.
   A peer becomes a source when SSH reaches the remote command, including when
   that command returns a nonzero status. A valid frame creates a `reporting`
   source, status 127 creates a `no_agentd` source, and another remote failure
   creates a `not_reached` source. Transport failure before a remote exit
   status does not create an auto-discovered source.
2. `--hosts-file <path>` selects the fallback mode instead of running
   Tailscale. The file contains exactly one non-empty UTF-8 line of
   whitespace-separated machine tokens. Each valid, deduplicated token becomes
   a source even when its probe fails, so curated membership remains visible.

An invalid hosts file, failed Tailscale command, invalid Tailscale JSON, or a
mode that produces zero sources ends startup with a typed diagnostic that names
the failed mode and recommends `--hosts-file`. Diagnostics do not include SSH
stderr or frame bodies.

### Source supervision and health

The probe establishes each source's initial health and last valid frame using
the same classifications as the watch loop. After the probe, each source owns
one reconnect loop. The loop starts
`ssh -o BatchMode=yes -o ConnectTimeout=5 <machine> agentd watch --json` as an
argument vector, reads newline-delimited frames, and accepts only valid frames.
It never invokes a shell. It drains and discards child stderr. Hub shutdown
terminates and reaps each SSH child before the hub process exits.

The loop uses delays of 1, 2, 4, 8, 16, and then 30 seconds between failed
attempts. Later consecutive failures remain at 30 seconds. The first valid
watch frame resets the next failure delay to 1 second. The process does not
sleep before the first watch attempt.

Each source exposes exactly one health object:

- `reporting`: the loop has accepted a valid current frame.
- `not_reached`: SSH did not reach a remote command, the stream ended, the
  remote command returned a nonzero status other than 127, or the stream
  supplied an invalid frame before another valid frame.
- `no_agentd`: the remote command returned status 127.

Each health object contains `state` and `sinceUnixMs`. A valid frame changes
health to `reporting` and replaces the source's last valid frame. A failure
changes health as above and retains the last valid frame. Repeated failures in
the same health state retain the existing `sinceUnixMs`. A degraded Agentd
scan is still `reporting`; its `scan` value remains visible in the preserved
frame.

### Merged snapshot and identity

The hub snapshot has this exact top-level shape:

```json
{
  "type": "snapshot",
  "schema": "agentd-hub.snapshot.v1",
  "revision": 12,
  "machines": [
    {
      "machine": "gibson.example.ts.net",
      "health": {"state": "reporting", "sinceUnixMs": 1788200000000},
      "snapshot": {"type": "snapshot", "schema": "agentd.snapshot.v1"}
    }
  ]
}
```

The example abbreviates the nested Agentd projection; the real `snapshot` value
is the complete accepted baseline-field projection of the last valid frame or
`null` before a source has produced one. Machine rows sort by the UTF-8 bytes of
`machine`. The hub preserves the projected agent ordering.

The identity of a nested agent is the machine row's `machine`, the nested
frame's `instanceId`, and the agent's `id.pid` and `id.startTimeTicks`. The hub
does not synthesize an identity from name, cwd, tty, tmux, array position, or
source-local revision.

The hub serializes state changes through one mutation seam. After discovery and
probing finish, it materializes the complete initial source set as revision 1.
It then increments the hub revision once when health changes or a last valid
frame changes. It does not increment for an identical frame, a repeated
failure in the same health state, a reconnect attempt, or time passing.

### HTTP, SSE, and page

The server exposes three GET routes:

- `GET /snapshot` returns the current hub snapshot as JSON with
  `Content-Type: application/json` and `Cache-Control: no-store`.
- `GET /events` returns `Content-Type: text/event-stream` and
  `Cache-Control: no-store`. Its first event is sent immediately and contains
  the current complete hub snapshot. Each later hub revision produces another
  complete snapshot event. Each event uses `event: snapshot`, `id: <revision>`,
  and one `data:` line containing the compact JSON. The server ignores
  `Last-Event-ID`; a reconnect receives the current snapshot and no replay.
- `GET /` returns one self-contained HTML document with inline CSS and
  JavaScript. It opens `/events` and replaces its rendered state from each
  complete event.

Other paths return 404. Non-GET requests return 405. The server exposes no
mutation route. The JSON body from `/snapshot` and the decoded `data:` value
from `/events` are byte-identical when they refer to the same hub revision.

The page renders one section per machine in machine order. Each section shows
the machine, source health state, health transition time, and Agentd scan state.
Within a section, agents with `activity.state == "needs_attention"` appear
first; remaining agents retain Agentd order. Each agent row shows harness,
name or `unnamed`, tmux `session:windowIndex.windowName:paneId` or `not
reported`, claim age or `unknown`, cwd or `unknown`, PID, and start-time ticks.
An activity timestamp later than browser current time renders as `clock ahead`
instead of a negative claim age.
The page uses DOM text nodes for source values and loads no remote script,
style, font, image, or telemetry endpoint.

### Privacy and logging

The hub may hold current Agentd frames in memory and serve their documented
fields. It writes no frame or roster to disk. Logs can name a machine, health
state, reconnect delay, HTTP status, and typed failure class. Logs do not print
frame bodies, cwd, agent names, tmux values, SSH stderr, command lines,
environment values, prompts, transcripts, terminal contents, or credentials.

### Repository and release

Implementation starts in the new `clickety-clacks/agentd-hub` repository.
Agentd receives only this one README sentence:

> For a read-only multi-machine view, see
> [agentd-hub](https://github.com/clickety-clacks/agentd-hub).

Agentd-hub clones Agentd's current release controls with product names changed:

- Pull requests and pushes to `main` run `cargo fmt --all -- --check`,
  `cargo clippy --all-targets --all-features -- -D warnings`, and
  `cargo test --locked --all-targets`.
- Development uses crate and packaging version `0.0.0`. The release-preparation
  commit changes both versions and the README product version to `0.1.0`.
  Release tag `v0.1.0` points exactly to that version-bump commit.
- A `v*` tag starts the release workflow. The workflow requires tag, crate,
  and packaging versions to match; reruns the locked gates; builds the locked
  release binary; packages twice; and compares the two archives byte for byte.
- The deterministic archive is
  `agentd-hub-0.1.0-<rust-host>.tar.gz`. It contains the executable and README
  under one same-named directory, uses fixed modes, sorted entries, root numeric
  ownership, the source commit time, and gzip without a timestamp. The workflow
  publishes the archive and `SHA256SUMS` with `gh release create`.
- A human or agent does not hand-upload a release asset. A failed parity,
  locked gate, build, reproduction check, or checksum step publishes no GitHub
  release.
- Before the tag push, A15 passes against the exact version-bump commit and its
  evidence is recorded. The tag workflow alone publishes the release.

This spec teaches no Tightbeam operating pattern and requires no substrate or
guidance amendment.

## Acceptance

A1 (I1-I3). **Given** a source fixture and process/socket inventory, **when**
the hub observes it and then shuts down, **then** the only source-side child is
the specified SSH Agentd CLI process, the hub reaps that child, Agentd still
opens only its Unix socket, and neither repository contains an Agentd network
listener or hub-specific Agentd wire field.

A2 (discovery). **Given** a captured real `tailscale status --json` shape with
peers whose probes return a valid frame, status 127, status 23, and a transport
failure, plus one duplicate normalized name and one malformed entry, **when**
default discovery runs, **then** it probes each distinct valid machine once,
skips the malformed entry, omits only the transport-failed peer, and starts one
source loop with initial health `reporting`, `no_agentd`, and `not_reached` for
the three remote responders.

A3 (fallback). **Given** a one-line hosts file containing
`GIBSON gibson. osanwe`, **when** fallback discovery runs, **then** the snapshot contains the
two machine rows `gibson` and `osanwe` even if one probe is unreachable; a
second non-empty line or a leading-dash token refuses startup before SSH runs.

A4 (health). **Given** a reporting source with a last valid frame, **when** its
watch exits, a reconnect fails twice, and a later reconnect yields a valid
frame, **then** the source retains the old frame while `not_reached`, keeps one
failure transition time across both failures, enters `reporting` on the valid
frame, and never disappears.

A5 (no Agentd). **Given** an SSH child that reaches the remote host and exits
127, **when** the hub classifies the result, **then** the source health is
`no_agentd`, the API and page print no captured stderr, and the reconnect loop
continues.

A6 (backoff). **Given** a fixed clock and six consecutive failed watch
attempts, **when** the reconnect loop schedules them, **then** the delays are
1, 2, 4, 8, 16, and 30 seconds; a later valid frame makes the next failed
attempt wait 1 second.

A7 (identity). **Given** equal PIDs and start-time ticks from two machines and
two Agentd instance IDs on one machine, **when** the hub merges the frames,
**then** it exposes four distinct tuple identities and does not collapse them
by PID, name, tmux value, or cwd.

A8a (initial revision). **Given** discovery and probes produce three source
rows, **when** the hub exposes its first merged snapshot, **then** that complete
snapshot contains the three rows at hub revision 1.

A8b (revision changes). **Given** hub revision 7, **when** the hub receives an
identical frame, a repeated same-state failure, and then one changed valid
frame, **then** the first two inputs leave revision 7 and the changed frame
produces revision 8 exactly once.

A9 (snapshot-first SSE). **Given** current revision 8 and a fresh or
`Last-Event-ID: 3` connection, **when** the client opens `/events`, **then** its
first event has `event: snapshot`, `id: 8`, and the complete current snapshot;
the server sends no revision 4 through 7 replay.

A10 (API parity). **Given** no state mutation between reads, **when** a client
reads `/snapshot` and decodes the first `/events` data line, **then** both JSON
values and compact JSON bytes match, and each contains every machine row,
health object, and complete accepted projection of each last valid Agentd
frame.

A11 (closed HTTP surface). **Given** the running server, **when** a test probes
the loopback listener, a non-loopback interface, `/`, `/snapshot`, `/events`,
an unknown path, and a POST, **then** only loopback accepts a connection, the
three GET routes have the defined responses, the unknown path returns 404, and
the POST returns 405 without a state change.

A12 (page). **Given** a snapshot with two machines, mixed activity states,
name/tmux values, null name/tmux values, and a name containing HTML markup,
**when** the page renders it, **then** machine sections are ordered, attention
rows lead, health and scan state are visible, claim ages use only
`observedAtUnixMs`, nulls use the defined labels, a future activity timestamp
renders as `clock ahead`, and the markup name appears as text rather than
executable HTML.

A13 (stateless restart). **Given** a hosts-file hub at revision 12 with cached
source frames, **when** the process stops and restarts while those sources are
unavailable, **then** revision starts at 1, no earlier frame is present, source
health comes only from new probes, and no roster file exists.

A14 (privacy). **Given** accepted Agentd fields containing one allowed sentinel
and SSH stderr, environment values, command lines, prompts, transcripts,
terminal contents, and unnamed additive frame fields containing distinct
prohibited sentinels, **when** discovery, reconnect, API, page, diagnostics,
and logs run, **then** API/page output contains the allowed Agentd-field
sentinel, each prohibited sentinel is absent from HTTP output, and each frame
or input sentinel is absent from logs, files, and archives.

A15 (real external-I/O smoke). **Given** two authorized non-production SSH
machines with Agentd and a disposable observed agent process, **when** the
exact release-mode hub version-bump commit starts from a hosts file, **then** one
`/events` subscription receives both reporting machine rows in its first full
snapshot, a real Agentd activity change produces a later full snapshot with a
higher hub revision, stopping one test Agentd service makes its source visibly
`not_reached`, and restarting that service returns the source to `reporting`
without restarting the hub. Evidence records the exact hub and Agentd commits
and command results without retaining credentials, SSH stderr, prompts,
transcripts, or terminal contents.

A16 (repository boundary). **Given** the implementation diffs for both
repositories, **when** review compares them with this spec, **then**
`agentd-hub` contains the new product and Agentd contains only the exact README
pointer sentence.

A17 (CI). **Given** a clean `agentd-hub` candidate, **when** pull-request and
main CI run, **then** the locked format, clippy, and all-target test gates pass
using the checked-in lockfile.

A18 (release). **Given** the reviewed version-bump commit with crate, packaging,
and README product version `0.1.0` and passing A15 evidence for that exact
commit, **when** tag `v0.1.0` is pushed, **then** the tag workflow builds and
byte-compares two deterministic archives, publishes one archive plus its
matching `SHA256SUMS`, and identifies the tagged commit; a parity or
reproduction failure creates no release.

## Open Questions

- NON-BLOCKING: The v0.1 page has no user-selected sort or filter. Usage after
  v0.1.0 can determine whether either belongs in a later version.
- NON-BLOCKING: Continuous tailnet membership refresh is outside v0.1. Restart
  is the defined way to rerun discovery.
- BLOCKING: none.
