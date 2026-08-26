# Managed-sandbox local Tightbeam gateway

Status: F4-LIFECYCLE-CORRECTED PROPOSAL PENDING CLEAN INDEPENDENT REVIEW

Authority: work item `wi_7c53cfb2-1ad4-477c-b3df-bffc0d3714fa`;
recon verdict `att_5b82a9c3-dfcc-4da5-bafc-d011bf537ada`;
historical closure report `art_4a60cdf3` at SHA-256
`869f650ee514d52e3450e3809b26bf679d4ec0adade2de69925c947dca094227`;
live specimen `att_edd8f0e0-1568-4753-8079-e7bc9af3da61`.
First independent review `att_da816395-6895-4e9c-be2a-89c645066765`
requested five blocking changes against commit
`39200fe74bfb9bbd8be8c2fe9204f544302e7556`.
That sole review closed through completion `att_9facab30` and full report
artifact `art_405ed9cf`. This amendment addresses its five findings. Continuation
assignment `asg_7fa0cf19-956d-4c1b-807a-ae5c9391908e` requests clean review of
the amended bytes before policy completion.
Verification review `att_ca8e39a2-5175-4f52-a553-28cf0365c3da` and report
`art_a178df78` cleared F1, F2, F3, and F5 and requested one F4 correction
against commit `d33ce3dfd90d88f4e0c97c0565600756e9098671`.
F4-only review `att_5c37ae5c-1688-4a8b-adba-595653c798d0` and report
`art_89b5dd64` confirmed that commit
`682c7167b86e8550085c0108bd0491d4bfe0dd73` closes the original unlink race
and requested a complete activator failure and descriptor-lifecycle contract.

Source basis: Tightbeam `7a70a2f616363074514237b5bee48ba67c52e2ea` and
tightbeam-specs `2327bc66a45c7cedf6e726bf8e13b40153531e0b`, both current
`origin/main` when this amendment was frozen.

## Goal

Let a Codex agent in a Linux managed command sandbox call the Tightbeam gateway
on the same host without giving that sandbox IP-network access.

The supported path uses one exact filesystem Unix-domain socket. The gateway
serves the existing authenticated agent CLI routes on that socket. The Codex
permission profile permits that socket and leaves its domain allowlist empty.
The `tightbeam-managed-local` Codex mode sends an unrelated network escalation
through an explicit, allow-once operator decision before Codex can execute it
outside the sandbox.

## Non-Goals

- Remote or satellite gateway access. A session placed on a host whose registry
  row has `ssh != nil` keeps the existing advertised HTTP endpoint.
- macOS Seatbelt support in this MVP.
- Claude sandbox configuration in this MVP.
- Device, browser, WebSocket, asset, upload, download, or firehose access over
  the local agent socket.
- A model-provider proxy. The harness process keeps its existing provider
  connection outside the command sandbox.
- A general localhost proxy, a port allowlist, a domain allowlist, DNS access,
  or a joined host network namespace.
- A new credential, capability token, identity rule, gateway verb, or gateway
  authorization rule.
- A change to approval behavior outside `tightbeam-managed-local` mode.
- Automatic recovery by granting broad network access when the local transport
  fails.

## Terms

- **Managed command sandbox**: the Linux sandbox that Codex applies to a
  model-issued command. It uses an isolated network namespace and the
  `tightbeam-managed-local` Codex mode. It does not include the Codex app-server
  or its provider connection.
- **Managed local mode**: the `tightbeam-managed-local` ACP session mode. Its
  Codex approval policy is `on-request`; its sandbox policy is workspace-write
  with network enabled through the active Codex proxy; and its effective
  network policy permits only the local agent socket.
- **Explicit approval relay**: the mapping from one ACP
  `session/request_permission` to one existing Tightbeam operator decision
  request. Only an `allow-once` ruling selects the ACP allow-once option. A
  denial, cancellation, timeout, missing option, or automatic responder selects
  denial.
- **Gateway-local session**: a Tightbeam session placed on the gateway's host,
  identified by a host-registry row with `ssh == nil`.
- **Local agent socket**: the host-activator-owned Unix-domain stream socket at
  the absolute path in `config.local_agent_socket`. The path denotes transport,
  not authority.
- **Host socket activator**: the packaged Linux host component that owns the
  local socket directory under an operating-system identity distinct from the
  gateway user, stages the configured socket, and passes its bound descriptor
  and activation receipt to its direct gateway child. The gateway user cannot
  write the directory. The activator grants no gateway verb or session
  authority.
- **Activation record**: the durable activator-owned state for one socket
  generation. It binds the schema version, phase, configured path, staging
  path, prior and current filesystem identities, gateway user, activation
  generation, activator process id and start identity, child process id and
  start identity when launched, activator version, kernel release, runtime
  filesystem type, primitive-probe digest, cause, and host principal.
- **Activation receipt**: the immutable sealed snapshot of the staged activation
  record that the activator passes to its direct gateway child. It contains no
  credential.
- **Installation id**: the stable, non-secret identifier that the packaged host
  integration assigns to one Tightbeam installation. It selects one
  activator-owned runtime and record path; callers cannot override it per
  session.
- **Local CLI listener**: the Bandit listener bound to the local agent socket.
  It delegates the permitted requests to the existing
  `Tightbeam.Wire.Router` with the same dependency map as the TCP listener.
- **Local CLI routes**: exactly `POST /agent/dispatch`,
  `POST /agent/tool-call-observed`, and `GET /harnesses`.
- **Session endpoint file**: the nearest `.tightbeam-session` file discovered
  from the command's working directory. It already carries `url`, `token`, and
  `sessionKey`; this proposal adds `socket` for gateway-local sessions.
- **Transport phase**: one of `discovery`, `connect`, `http`, or `gateway`.
  The CLI uses the phase in its error code so an operator can identify the
  failing local-CLI layer without interpreting prose. SSH and ACP provider
  failures retain their existing `ssh` and `acp` reported layers.
- **Managed-profile compatibility stamp**: the exact Codex version,
  `codex-acp` version, and SHA-256 of the canonical host-profile template that
  the release gate proved. The template has one typed
  `local_agent_socket` slot. The Tightbeam release embeds the stamp beside its
  Codex harness preset.
- **Host policy receipt**: the configured socket path, materialized host-profile
  SHA-256, effective-policy SHA-256, and compatibility stamp recorded after the
  real host readiness probe passes.
- **Unrelated network action**: a command attempt to use an IP destination.
  The local agent socket is not an IP destination.

## Assumptions

1. A filesystem Unix-domain socket remains reachable from a bubblewrap network
   namespace when the sandbox can search the socket's directory.
2. Bandit 1.12.x and Thousand Island accept `ip: {:local, path}` with `port: 0`
   for a Unix-domain listener. The implementation must verify this against the
   dependency version in `mix.lock` before source work begins.
3. The supported Codex release accepts named permission profiles with an exact
   `network.unix_sockets` allowlist and an active network proxy. Codex 0.149.1
   documents and exposes this surface; the release gate must re-probe the
   pinned `CODEX_PATH` binary.
4. The Codex network proxy blocks IP destinations when the profile has
   `network.enabled = true`, the proxy is active, and the effective domain
   allowlist is empty.
5. The existing session bearer token authenticates both local-socket and TCP
   requests. `Tightbeam.Wire.Router` remains the authority for principal and
   verb authorization.
6. The gateway and each gateway-local managed command run as the same operating
   system user. The gateway-to-command data path does not cross a user boundary.
   This statement does not include the host socket activator. That component's
   distinct identity is an explicit lifecycle-only boundary under R-1 and R-2.
7. The existing operator decision subsystem can address the user who owns the
   managed session and can return one durable `allow-once` or `deny` ruling to
   the pending ACP permission request.
8. The packaged Linux host supervisor can run the socket activator under an
   identity distinct from the gateway user. It can pass a bound Unix socket
   descriptor, sealed receipt descriptor, and control descriptor only to its
   direct gateway child during process creation. The release gate must prove
   descriptor adoption against the pinned Bandit and Thousand Island versions.
9. The supported Linux kernel and runtime filesystem enforce `memfd` seals,
   `SO_PEERCRED`, `RENAME_NOREPLACE`, file and directory `fsync(2)`, and the
   activator-owned ancestor permissions used by R-1 through R-3. The release
   gate must exercise each primitive on the target host.

If assumption 2, 3, 4, 8, or 9 fails on a supported release candidate, the
release is blocked. An implementer does not substitute a TCP exception, a
wildcard Unix-socket permission, or full network access.

## Invariants

### I-1 — One narrow network capability

For the managed profile, Tightbeam generates an empty domain allowlist and one
`allow` entry whose key is the absolute local agent socket path. Tightbeam sets
`dangerously_allow_all_unix_sockets = false` and
`allow_local_binding = false`. The host socket activator makes the runtime
directory searchable but not writable by the gateway user. At listener
readiness its only entry is the local agent socket. Before readiness it may
contain one generation-named staging socket that the managed profile does not
allow.

Acceptance example (AC-1): Given the generated profile, when a test reads its
effective Codex network policy, then it contains one allowed Unix socket, zero
allowed domains, `allow_local_binding = false`, and
`dangerously_allow_all_unix_sockets = false`; its added filesystem permission
names only the socket path, the host directory contains only that
socket, and a process running as the gateway user cannot create, replace,
rename, or unlink a directory entry there.

### I-2 — Gateway authorization is transport-independent

The local CLI listener passes the existing bearer header, CLI-version header,
request method, path, and body to the existing router. The router derives the
principal and evaluates authorization through the existing code path.

Acceptance example (AC-2): Given one session token, when the same
`work-item-get` request reaches TCP and the local agent socket, then both
responses have the same status and JSON bytes and both event rows name the
same principal.

### I-3 — A socket path grants no authority

The local CLI listener requires the credential already required by the
selected route. Filesystem access to the socket does not select an identity or
authorize a verb.

Acceptance example (AC-3): Given a process that can connect to the socket but
has no bearer token, when it posts a valid dispatch body, then the router
returns its existing authentication error and writes no domain mutation.

### I-4 — Selected local transport does not degrade to IP

When a session endpoint file contains the `socket` key, the CLI never uses
`url`. A valid value causes one local-socket connection attempt. An invalid
value reports `invalid_local_gateway_endpoint` in phase `discovery`. Before the
CLI writes request bytes, a failed connection reports a connect error. After it
writes one request byte, a missing complete HTTP response reports
`local_gateway_outcome_unknown`.

Acceptance example (AC-4): Given a session file with a dead socket and a live
TCP URL, when the CLI sends a mutating verb, then it reports
`local_gateway_unavailable`, the TCP test server receives zero connections,
and the mutation count remains zero. Given a listener that drops the connection
after reading one request byte, when the same verb runs, then the CLI reports
`local_gateway_outcome_unknown` and makes no TCP attempt.

### I-5 — Remote placement keeps the existing transport

Placement writes `socket` only for a gateway-local session. Placement writes
the existing advertised `url` shape for a session whose host row has
`ssh != nil`.

Acceptance example (AC-5): Given one local host row and one satellite host row,
when Placement materializes both endpoint files, then the local file contains
an absolute `socket` and the satellite file contains no `socket`.

### I-6 — The local listener has a closed route set

The local listener delegates only the three local CLI routes. For another
method or path it returns `404` with the existing `not_found` envelope before
the main router handles the request.

Acceptance example (AC-6): Given valid device and session credentials, when a
client requests `/ws`, `/api/streams`, `/download/x`, `/version`, or an
unlisted method through the local socket, then each request receives
`404/not_found` and opens no WebSocket.

### I-7 — Existing evidence remains the observability authority

A successful local request produces the same attributed verb and event rows as
its TCP equivalent. A pre-HTTP connection failure writes no gateway row because
the gateway did not observe it; the CLI prints its phase, stable error code,
socket path, operating-system cause, and remedy to stderr.

Acceptance example (AC-7): Given a socket denied by filesystem policy, when the
CLI attempts `tightbeam toplines`, then stderr names phase `connect`, code
`local_gateway_connect_denied`, the socket path, the operating-system error,
and the remedy to expose the configured socket; the gateway event count does
not change.

### I-8 — Transport diagnostics carry no secret material

Transport logs and errors may carry the socket path, method, route, phase,
status, and stable error code. They omit bearer values, session-file bytes,
request bodies, response bodies, and credential paths.

Acceptance example (AC-8): Given sentinel values in the token and request
body, when connect, authentication, refusal, and outage cases run, then a scan
of captured gateway and activator logs, activation records and receipts, CLI
stderr, operator decision rows, and approval notifications finds neither
sentinel.

### I-9 — Approval is explicit and single-use

`Tightbeam.ACP.Conn` does not auto-select an allow option for a managed-local
session. It keeps the ACP request pending until the owning user rules the
linked operator decision. One `allow-once` ruling resolves one request and
creates no reusable rule.

Acceptance example (AC-21): Given an unrelated network command in managed-local
mode, when no ruling exists, then the command remains blocked and the fixture
receives zero connections. When the user rules `deny`, cancels the turn, or
does not rule within ten minutes, then the ACP request resolves denied and the
fixture receives zero connections. Given a new request that the user rules
`allow-once`, then that request runs once outside the sandbox. When the same
command runs again, then it creates a new pending decision and remains blocked
until a new ruling. Given the old automatic responder, then managed-mode
readiness refuses before a turn.

## Architecture

### R-1 — One host-owned socket lifecycle

`config.local_agent_socket` is the single mutation seam for the local
transport. Its default is `nil`, which starts no local listener and changes no
session endpoint or command posture. A Linux host that offers the managed
local-gateway mode sets it to an absolute path. The packaged host integration
uses `/run/tightbeam/<installation-id>/gateway.sock` and installs one host
socket activator. `/run/tightbeam` and the installation directory are owned by
the activator identity with mode `0711`; no ancestor below `/run` is writable by
the gateway user. The activator runs outside the gateway-user security boundary
and is the only supported writer of the installation directory. The gateway
user can search the path but cannot create, replace, rename, or unlink the
installation directory or an entry in it. The activator and gateway consume the
same `config.local_agent_socket` value; the activator accepts no independent
path override. Its durable record lives at activator-owned
`/var/lib/tightbeam/activations/<installation-id>.json`.
For the packaged mode, a configured path other than the derived runtime path
returns `invalid_local_agent_socket` before record or pathname mutation.
Before the first generation, the activator runs the Assumption 9 primitives in
an activator-owned disposable sibling directory. It records the successful
probe digest in each activation record. A failed primitive returns
`local_agent_activation_unsupported` and performs no configured-path mutation.

The activator serializes socket creation and gateway launch. It uses one
generation-named staging path in the same directory. It binds a Unix stream
socket at that path without calling `listen(2)`, changes the socket owner to the
gateway user and mode to `0600`, and passes the bound descriptor to its direct
gateway child. After bind it records and synchronizes the staging device and
inode before child launch. The configured pathname remains absent until R-3
publishes the ready listener.

The host-owned activation record is inaccessible to the gateway user. Its
phase is exactly `staged`, `published`, `adopted`, `stopping`, or `stopped`.
Its generation is an unsigned 64-bit integer. A fresh record starts at one;
each successor is exactly the prior value plus one; a phase transition keeps
the value unchanged; and exhaustion returns
`local_agent_activation_generation_exhausted` before mutation.
For each phase change, the activator writes a complete next record to a new
mode-`0600` file, calls `fsync(2)` on that file, atomically renames it over the
record, and calls `fsync(2)` on the record directory before the next pathname
mutation. A create,
write, sync, rename, or directory-sync failure returns
`local_agent_activation_record_unavailable`. Before a durable `staged` record,
the activator closes unpublished descriptors and removes nothing. After a
durable record, a transition failure permits no further pathname mutation; the
next activator recovers from the last durable phase.

Recovery applies this closed table:

- No record plus no configured or staging entry is a fresh start.
- `staged` plus absent configured and staging paths resumes staging bind.
  `staged` plus an absent configured path and a staging socket with the required
  owner, mode, and recorded name records its current identity when missing and
  resumes child launch.
- `staged` plus the recorded current inode at the configured path, or
  `published` or `adopted` after an activator restart, first relies on control
  channel closure to stop the child, verifies the recorded process id and start
  identity before any signal or wait, then durably advances to `stopping`.
- `stopping` waits for child exit. It then removes the configured or staging
  entry only when its identity equals the recorded current identity,
  synchronizes the socket directory, and records `stopped`. If both paths are
  already absent, it records `stopped` without pathname mutation.
- `stopped` plus absent configured and staging paths permits the next increasing
  generation. Another `stopped` state is a conflict.

An absent record with any socket entry, a truncated or corrupt record, an
unsupported schema, a non-increasing generation, an unlisted phase, or another
path/record combination returns `local_agent_activation_record_invalid`. The
activator removes nothing in these states. The error names the record phase,
generation when readable, path, and the remedy to stop the gateway and repair
the host-owned activation record; it contains no credential.

Direct gateway launch with a configured path but without the three inherited
activation descriptors returns `local_agent_socket_activation_required` before
adapter start.

The path must be absolute and must fit the host's Unix-socket path limit. A
non-absolute or over-limit configured path stops gateway boot with
`invalid_local_agent_socket` and names the path constraint.

Acceptance example (AC-9): Given `local_agent_socket = nil`, when the gateway
boots, then it creates no listener or runtime directory. Given a configured
path for a fresh disposable installation id, when the gateway boots, then the
runtime directory and socket exist with the specified modes and the local listener
accepts an authenticated `GET /harnesses`. Given an unexpected directory
entry, activation returns `local_agent_runtime_conflict` without removing it.
Given a configured direct gateway launch without an inherited listener, then
the gateway refuses before adapter start. Given record create, write, file-sync,
rename, and directory-sync failures, then each returns
`local_agent_activation_record_unavailable` at the named phase and performs no
later pathname mutation. Given absent-with-entry, truncated, corrupt,
unsupported-schema, non-increasing-generation, and unlisted-phase records, then
each returns `local_agent_activation_record_invalid` and removes nothing. Given
each missing Assumption 9 primitive, then activation returns
`local_agent_activation_unsupported` before configured-path mutation. Given a
maximum generation, then activation returns
`local_agent_activation_generation_exhausted` and removes nothing.

### R-2 — The gateway never removes a socket pathname

The activator passes exactly three descriptors during direct child creation:
the bound socket, a read-only sealed `memfd` containing the complete staged
receipt, and one end of a Unix `SOCK_SEQPACKET` control socketpair. The gateway
uses `SO_PEERCRED` on the control endpoint to require the activator operating-
system identity and process id named by the receipt. It accepts the descriptors
only in that direct child launch. The forked child waits behind an exec barrier
while the activator records and synchronizes its process id and start identity.
The activator then releases exec. It closes its socket duplicate after
successful child exec. The gateway becomes the sole socket-descriptor owner.
The activator retains the process handle and control endpoint, not a socket
duplicate.

The gateway validates the socket with `fstat(2)`, `getsockname(2)`, `SO_TYPE`,
and `SO_ACCEPTCONN`. It requires a bound, non-listening Unix stream socket at
the receipt's staging path. It validates every receipt field, the `memfd` write,
grow, shrink, and seal seals, and the direct-child activation generation. A
mismatch returns `invalid_local_agent_activation` before adapter start. The
gateway neither binds nor mutates a pathname during startup, shutdown, or crash
recovery.

The activator is the sole pathname owner. Its activation record carries the
socket device and inode, gateway user, path, and activation generation. Before
removal it requires an exact record match. The runtime directory permissions
prevent every gateway-user process, including each managed agent command, from
changing the pathname before, during, or after that check. Only the activator
can remove the recorded socket and bind its successor. Thus the supported
lifecycle contains no check-then-unlink interval that a same-user process can
race.

If child exec fails, the activator durably records `stopping` before it closes
its socket descriptor. If the child exits before publication, the kernel closes
the child's descriptor and the activator durably records `stopping` before
pathname cleanup. A final stop, disable, uninstall, gateway crash, or activator
control-channel loss follows the same order: record `stopping`, stop or observe
the child, wait for descriptor closure, remove only the exact recorded inode,
synchronize the directory, then record `stopped`. Uninstall removes the record
and runtime directory only after both socket paths are absent and the directory
is empty. An identity or record mismatch invokes R-1's remove-nothing refusal.

Acceptance example (AC-10): Given two concurrent gateway starts, when both ask
the activator for the configured socket, then the activator starts one gateway
generation and refuses the other without changing the live pathname. Given a
process running as the gateway user, when it attempts replacement immediately
before the activator's identity check, between that check and removal, and
immediately after removal, then each operation fails with `EACCES` or `EPERM`.
Given an unexpected pathname inode or another directory entry, when activation
runs, then it returns `local_agent_runtime_conflict` and removes nothing. Given
a gateway shutdown, failed exec, pre-publication child exit, final stop,
disable, and uninstall, then the gateway issues no pathname-mutation syscall
and the activator follows the exact teardown above. Given a crash after each
durable record transition and each unlink, bind, publish, child-exec, and
child-exit boundary, then restart selects exactly one recovery-table row or a
remove-nothing refusal.

### R-3 — Listener order exposes only a complete gateway

After its router dependencies, `AdapterCoordinator`, and `LaneManager` are live,
the gateway calls `listen(2)` on the staging descriptor and starts Bandit's
accept loop. It then sends `listener_ready_to_publish` with the activation
generation over the inherited control channel. Before this message the
configured pathname is absent, so a CLI connect writes zero request bytes and
reports `local_gateway_unavailable`.

For the matching generation, the activator atomically renames the recorded
staging entry to `config.local_agent_socket` with `RENAME_NOREPLACE`,
synchronizes the socket directory, records `published`, and acknowledges the
gateway. The gateway uses `lstat(2)` to match the published device, inode,
owner, and mode to its sealed receipt. It sends `listener_adopted`; the
activator records `adopted` and acknowledges. The gateway starts the existing
TCP Bandit listener next. Readiness reports both listeners only after that
final acknowledgment and both accept loops are live. It prints the configured
local listener path without a token.

A control-channel close, wrong generation, publication collision, rename or
sync failure, receipt mismatch, or 30-second readiness deadline closes the gateway's
socket descriptor and stops the child. Before any pathname cleanup, the
activator must durably enter `stopping`; a record-transition failure permits no
further pathname mutation and leaves recovery to the next activator. The
activator then applies R-1 recovery and R-2 teardown. It never retains a
listening socket duplicate.
After atomic publication, a CLI request follows the normal byte-boundary rules:
a completed response succeeds; a child failure after request bytes reports
`local_gateway_outcome_unknown`.

Acceptance example (AC-11): Given a boot probe at each child boundary, when the
gateway starts, then the gateway processes no local request before
`AdapterCoordinator` and `LaneManager` are live. Given probes before staging
listen and after staging listen but before atomic publication, then the
configured path accepts zero connections and the CLI reports
`local_gateway_unavailable`. Given publication, record sync, and acknowledgment,
then an authenticated `GET /harnesses` succeeds through both listeners. Given
each publication and control-channel failure above, then the child stops, no
listening descriptor remains, and teardown selects one named recovery state.

### R-4 — A route filter reuses the existing router

A small Plug filter owns the local route set and delegates permitted requests
to `Tightbeam.Wire.Router`. It contains no handler, authentication,
authorization, or response-shaping copy.

Acceptance example (AC-12): Given a test that replaces one shared router
handler, when the permitted request reaches TCP and the local socket, then both
listeners call that replacement and no local-only handler exists.

### R-5 — Session discovery selects the socket by recorded origin

For a gateway-local session, `Placement.holder_workdir/2` writes the absolute
`socket` beside the existing `url`, `token`, and `sessionKey`. The Rust CLI
extends `Endpoint` with an HTTP or Unix transport while keeping
`Origin::Session(path)` unchanged.

Discovery keeps the existing precedence: nearest session file, then explicit
environment endpoint, then provisioned `gateway.json`. Within a selected
session file, the presence of the `socket` key suppresses HTTP selection. Its
value is valid only when it is a non-empty JSON string, absolute, lexically
normalized, contains no NUL byte, and fits the host Unix-socket path limit. If
the path exists, `lstat(2)` must identify a socket owned by the current user.
A valid value selects Unix transport and `url` remains diagnostic compatibility
material. An invalid present value returns `invalid_local_gateway_endpoint` in
phase `discovery`, names the failed constraint, and makes no connection. A
session file without the key selects the existing HTTP transport.

Acceptance example (AC-13): Given nested working directories and a nearest
session file with `socket`, when discovery runs, then it selects that socket,
retains the nearest file as origin, and ignores an environment HTTP endpoint.
Given empty, non-string, relative, non-normalized, NUL-containing, over-limit,
and existing non-socket values beside a live `url`, when discovery runs, then
each returns `invalid_local_gateway_endpoint` and the HTTP fixture receives
zero connections.

### R-6 — The CLI speaks the existing HTTP contract over Unix transport

The CLI sends HTTP/1.1 over `UnixStream`. It sends the same authorization,
`x-tightbeam-cli-version`, content type, method, route, body, timeout, and
response parser used by HTTP transport. It sets a fixed `Host: localhost`
header because the router does not derive authority from Host.

The Unix sender records whether it wrote zero bytes or at least one byte. This
mechanical fact selects `local_gateway_unavailable` or
`local_gateway_outcome_unknown`; it does not infer whether the gateway
committed a mutation.

Acceptance example (AC-14): Given a recording Unix listener, when each local
CLI route runs, then the captured request has the existing headers and body,
and the existing response parser returns the same CLI result as its TCP
fixture.

### R-7 — One host profile and one per-session mode compose the boundary

Tightbeam generates one host-scoped Codex permission profile for the shared
Codex adapter process. It has no workspace path or session input. It:

- extends the existing managed workspace filesystem posture;
- preserves the existing `bypass_hook_trust` setting and configured hooks;
- grants the exact filesystem access needed to search the host-owned runtime
  directory and connect to its socket, without directory write access;
- sets `network.enabled = true`;
- activates `features.network_proxy`;
- defines no allowed domain;
- allows the exact `config.local_agent_socket` under
  `network.unix_sockets`;
- keeps `allow_local_binding = false`;
- keeps `dangerously_allow_all_unix_sockets = false`.

The matching `codex-acp` exposes a `tightbeam-managed-local` session mode. That
mode sets `approvalPolicy = on-request` and selects workspace-write with
network enabled. The selected session `cwd` supplies the workspace root; the
host profile supplies only the shared socket capability. Two sessions with
different worktrees therefore share one process-wide network profile without
sharing filesystem roots.

Tightbeam writes the complete merged profile into its existing owned
`CODEX_HOME` launch material before it starts the shared adapter. It does not
modify the identity repository, the user's Codex configuration, or the user's
permission profiles. It selects `tightbeam-managed-local` per session through
`session/set_mode`; other sessions retain their existing mode. After the
effective readback succeeds, the adapter registers that ACP session id as
managed-local in `Tightbeam.ACP.Conn` and removes the registration when the
session closes. A permission request follows the relay only when its session id
has that live registration.

Codex applies proxy readiness, the effective destination policy, and command
start as one boundary. If the proxy cannot start or the profile cannot apply,
Codex returns `managed_network_proxy_unavailable` and does not start the
command. Tightbeam supports managed mode only for a stamped Codex release whose
gate executes this failure case.

The profile generator accepts no caller-supplied domain, wildcard socket,
proxy URL, or local-binding override. An operator who wants another network
destination uses the explicit approval relay. For a managed-local session,
`Tightbeam.ACP.Conn` records one existing operator decision request and waits.
It returns Codex's allow-once option only after the owning user rules
`allow-once`; otherwise it returns denial. It never selects allow-always and
never treats an automatic response as an explicit ruling. Turn cancellation,
user denial, and a ten-minute decision deadline resolve the ACP request as
denied and close the pending decision.

The operator decision carries the ACP request id, session display name,
working directory, executable basename, zero or more requested network
destinations reduced to scheme, host, and port, and requested permission
options. It replaces other argument values with
`<redacted>` and omits environment values, bearer values, session endpoint
bytes, and unrelated conversation content. A sentinel scan of the durable
decision and its user notification is part of AC-8.

Acceptance example (AC-15): Given the generated profile in a real Codex
managed sandbox, when a command connects to the Tightbeam socket, an unlisted
Unix socket, the gateway's TCP loopback port, and a host-side TCP fixture, then
only the Tightbeam socket connects without approval. The effective launch
keeps the pre-existing hooks and `bypass_hook_trust` value, and the files that
supplied them remain unchanged. When the proxy-start fixture fails, then the
command does not start. Given two managed-local sessions with different `cwd`
values on one shared adapter, then each can read only its own workspace and
both can reach the same local agent socket. Given an unrelated network request,
then AC-21 proves deny, allow-once, and re-prompt behavior.

### R-8 — Capability mismatch refuses the managed profile

Before enabling the managed profile for a release, the release gate runs the
pinned `CODEX_PATH` and `codex-acp` binaries with an isolated Tightbeam-owned
`CODEX_HOME` and the complete generated profile. It proves local-socket
success, IP denial, proxy-start failure, per-session workspace isolation, and
the explicit approval relay. The release embeds the resulting compatibility
stamp.

The matching `codex-acp` returns typed `effectivePermissions` after
`session/set_mode`. The value comes from Codex's resolved session state, not
from the template. It includes mode id, approval policy, sandbox kind,
workspace roots, proxy-active state, effective domains, effective Unix
sockets, local-binding flag, and wildcard-socket flag.

At adapter start, Tightbeam compares the selected binary versions and canonical
template SHA-256 with the release stamp, materializes the socket slot, and runs
a real probe session. It records a host policy receipt only when the typed
readback and behavioral probe agree. After selecting mode for each managed
session, Tightbeam requires another typed readback whose mode, approval policy,
workspace root, and network fields equal the receipt and that session's `cwd`.
Any extra config layer, legacy `sandbox_mode`, added domain or socket, changed
binding flag, wildcard permission, wrong workspace, wrong approval policy, or
missing readback returns `managed_local_gateway_unsupported` before a turn.
The receipt is generation-scoped state in `AdapterCoordinator`; an adapter
restart discards it and repeats the probe before a managed session can run.

Open-network and full-access Codex modes keep their existing behavior. The
gateway does not silently select one of those modes after this refusal.

Acceptance example (AC-16): Given a Codex fixture that rejects
`network.unix_sockets`, when managed-mode readiness runs, then the adapter
refuses before a turn with `managed_local_gateway_unsupported` and starts no
fallback adapter. Given fixtures that inject a legacy `sandbox_mode`, extra
domain, extra socket, local binding, wildcard sockets, wrong approval policy,
wrong mode, or wrong workspace root, then each effective readback refuses the
managed session before its first command.

### R-9 — Errors identify the layer and next action

The CLI maps outcomes to the following stable classes:

| Observed boundary | CLI result | Remedy |
| --- | --- | --- |
| `connect(2)` returns `EACCES` or `EPERM` before HTTP bytes | `local_gateway_connect_denied` | expose the configured socket in the managed profile; do not change token or provider |
| A present `socket` fails endpoint validation | `invalid_local_gateway_endpoint` in phase `discovery` | repair or re-project the session endpoint; do not use `url` as fallback |
| Socket is absent, refuses, or times out before the CLI writes a request byte | `local_gateway_unavailable` | start or restart the local Tightbeam gateway; do not re-onboard |
| Connection resets, returns EOF, or times out after the CLI writes a request byte but before a complete HTTP response | `local_gateway_outcome_unknown` | inspect the referenced work before repeating a mutation |
| Gateway returns `401` | preserve the gateway authentication code and prefix phase `gateway` | repair the session endpoint/token projection |
| Gateway returns another error envelope | preserve its exact code and message and prefix phase `gateway` | follow the gateway's named remedy |
| A remote host operation reports `Permission denied (publickey)` | preserve the existing SSH-authentication classification and `ssh` layer | repair that host's SSH key; do not change local transport |
| An ACP turn records `usageLimitExceeded`, `rate_limit`, or another provider code | preserve the existing provider-failure classification and `acp` layer | follow provider recovery; do not change local transport |

The CLI classifies from the observed boundary or typed response. It does not
classify by searching arbitrary provider or SSH prose in a local socket error.

Acceptance example (AC-17): Given one fixture for each table row, when the
failure is surfaced, then each output has the specified class and reported
layer and no fixture is classified as another row.

### R-10 — Restart retains the address and principal

The host activator preserves the configured address across gateway-process
restarts. It serializes generation replacement, removes only its recorded old
socket, stages the successor at its generation path, and atomically publishes
the configured path only after the new accept loop is ready. The session
endpoint file and token remain valid. While the configured path is absent, a
CLI command reports `local_gateway_unavailable` before request bytes. The first
command after publication uses the same configured path and principal. A crash
after publication follows R-6's byte-boundary classification.

Acceptance example (AC-18): Given one active local session, when the gateway is
stopped between two read requests and restarted, then the first request
succeeds, the gap request reports `local_gateway_unavailable`, the final
request succeeds, and both successful rows carry the same session principal.
The recorded socket inode changes by one activator generation, and the gateway
process issues no pathname-mutation syscall. Given a failure after atomic
publication and after the CLI writes one request byte, then the CLI reports
`local_gateway_outcome_unknown`. Given final stop, disable, and uninstall, then
the descriptors close, the configured and staging paths are absent, and the
activator records `stopped` before optional empty-directory removal.

### R-11 — Upgrade order preserves old sessions

The release installs the host socket activator, gateway, and matching CLI as one
versioned package, as the current release contract requires. The new activator
publishes the ready local listener before the gateway projects `socket` into a
gateway-local session file. Before it enables the managed profile, the gateway
reconciles each active gateway-local session endpoint so `socket` equals
`config.local_agent_socket`. A new CLI against an old session file uses HTTP.
An old CLI ignores the added JSON field and retains its existing HTTP behavior
outside the managed profile.

The managed profile becomes selectable only after the matching CLI and local
listener pass AC-15 and the adapter records the host policy receipt. This order
prevents an old CLI from entering an IP-disabled sandbox with no Unix transport
implementation. For the new CLI, a present invalid `socket` never invokes the
old HTTP path.

Acceptance example (AC-19): Given the four old/new CLI and old/new endpoint
file combinations, when they run outside managed mode, then each uses its
supported transport; when managed mode is requested with the old CLI, then
readiness refuses before a turn. Given a new endpoint file with an invalid
present `socket`, then both managed and non-managed invocation refuse discovery
without contacting `url`.

### R-12 — Host and harness scope is explicit

The MVP support predicate is:

`os == linux AND activator identity != gateway user AND config.local_agent_socket == derived activator-owned runtime path AND activated socket path == config.local_agent_socket AND activator phase == adopted AND sealed receipt and control peer match AND session.socket == config.local_agent_socket AND host.ssh == nil AND harness == codex AND mode == tightbeam-managed-local AND compatibility stamp matches AND host policy receipt matches AND per-session effective readback matches AND approval relay is available`.

When the predicate is false, Tightbeam keeps the existing transport and
permission behavior. The predicate is a mechanical conjunction over recorded
facts and a release-gate result; it makes no model or operator judgment.

Acceptance example (AC-20): Given the cross-product of Linux/macOS,
derived/other socket path, distinct/same activator identity, ready/unready
activator, local/satellite, Codex/Claude, proven/unproven effective policy, and
available/unavailable approval relay, when Tightbeam selects a command posture,
then only the tuple with an adopted generation and matching receipt/control
peer selects the managed local-socket profile.

### Pattern and subtraction ruling

This spec establishes the **gateway-only local transport** pattern. It applies
only to an agent CLI that targets a gateway on the same Linux host from a
network-restricted Codex command sandbox. It does not apply to provider calls,
satellite placement, device traffic, or general localhost access.

Canonical example: a gateway-local Codex agent runs `tightbeam attest ...` in
its managed sandbox; the CLI discovers `.tightbeam-session.socket`, connects
over the allowlisted Unix socket, and the existing router records the session
principal. A subsequent `curl https://example.com` remains denied until the
operator rules its decision `allow-once`. That ruling executes one request
outside the sandbox and does not authorize the next invocation.

ADD wins because managed agents need the existing durable coordination verbs
inside ordinary turns. DELETE loses because removing those verbs from managed
turns removes the product's accountability path. ACCEPT loses because broad
host escalation for each Tightbeam command makes the routine control plane
indistinguishable from unrelated network access.

The enforcement rung is **unrepresentable in the generated profile**: its
generator has one socket input and no domain, wildcard, or local-binding input.
Codex's proxy and the kernel enforce the resulting allowlist. Prose only names
the contract.

Operating pattern taught to agents: none. A Tightbeam CLI command uses the
local transport through discovery; agents receive no new instruction or
approval heuristic.

## Acceptance

The implementation passes when AC-1 through AC-21 pass and the following
reality smoke passes on Gibson against the release CLI, the release gateway,
and the pinned Codex binary:

1. Start a real host socket activator and gateway with a disposable installation
   id under the activator-owned runtime root. Use the inherited Unix listener.
2. Create a real gateway-local session endpoint through Placement; do not
   hand-author the endpoint fixture.
3. Start two real sessions with different worktrees on one shared Codex adapter.
   Select `tightbeam-managed-local` for both and verify their typed effective
   permission readbacks before running a command.
4. Execute one authenticated read and one idempotent mutation through the Unix
   socket. Verify the returned JSON and the attributed durable row.
5. In the same sandbox, attempt the gateway TCP loopback port, another host TCP
   listener, and one unlisted Unix socket. Verify three denials and zero
   connections at the fixtures. These local fixtures prove the sandbox's IP
   namespace and socket allowlist without depending on DNS or an Internet host.
6. Attempt one unrelated network action. Verify zero connections while its
   operator decision is pending and after `deny`. Create a new attempt, rule
   `allow-once`, verify one out-of-sandbox connection, and verify its next
   invocation is pending again without changing the host profile.
7. In the disposable activator, inject each record I/O failure and crash
   boundary from AC-9 through AC-11. Verify the named recovery row or
   remove-nothing refusal and verify that no listening descriptor survives a
   failed launch.
8. Restart the gateway between two CLI reads and verify AC-18 against the real
   socket inode. Stop it finally and verify both socket paths are absent and the
   durable phase is `stopped`.
9. Scan the captured CLI stderr, gateway and activator logs, activation record
   and receipt, and Codex sandbox log for the sentinel token and body values.
   Verify AC-8.

The test matrix records the Tightbeam commit, host-activator version and
generation, CLI version, Codex version, `codex-acp` version, kernel version,
canonical-template SHA-256, materialized-profile SHA-256, effective-policy
SHA-256, host policy receipt,
baseline result, and after result. A hand-written idealized gateway response
does not satisfy this acceptance.

Traceability:

| Requirement | Acceptance |
| --- | --- |
| I-1 | AC-1, AC-15 |
| I-2 | AC-2, AC-14 |
| I-3 | AC-3 |
| I-4 | AC-4, AC-13, AC-19 |
| I-5 | AC-5, AC-20 |
| I-6 | AC-6, AC-12 |
| I-7 | AC-7, AC-17 |
| I-8 | AC-8 |
| I-9 | AC-15, AC-21 |
| R-1 | AC-9 |
| R-2 | AC-10, AC-18 |
| R-3 | AC-11 |
| R-4 | AC-6, AC-12 |
| R-5 | AC-5, AC-13, AC-19 |
| R-6 | AC-2, AC-14 |
| R-7 | AC-1, AC-15, AC-21 |
| R-8 | AC-15, AC-16, AC-20 |
| R-9 | AC-7, AC-17 |
| R-10 | AC-18 |
| R-11 | AC-19 |
| R-12 | AC-20 |

## Open Questions

None. A failed release-gate assumption is a named unsupported value under R-1,
R-8, or R-12, not an invitation to widen network access.
