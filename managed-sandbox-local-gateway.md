# Managed-sandbox local Tightbeam gateway

Status: PROPOSAL FOR INDEPENDENT REVIEW

Authority: work item `wi_7c53cfb2-1ad4-477c-b3df-bffc0d3714fa`;
recon verdict `att_5b82a9c3-dfcc-4da5-bafc-d011bf537ada`;
historical closure report `art_4a60cdf3` at SHA-256
`869f650ee514d52e3450e3809b26bf679d4ec0adade2de69925c947dca094227`;
live specimen `att_edd8f0e0-1568-4753-8079-e7bc9af3da61`.

Source basis: Tightbeam `7a70a2f616363074514237b5bee48ba67c52e2ea` and
tightbeam-specs `130c0dff508df38ef84780bda08ca4704434ad4e`, both current
`origin/main` when this proposal was drafted.

## Goal

Let a Codex agent in a Linux managed command sandbox call the Tightbeam gateway
on the same host without giving that sandbox IP-network access.

The supported path uses one exact filesystem Unix-domain socket. The gateway
serves the existing authenticated agent CLI routes on that socket. The Codex
permission profile permits that socket and leaves its domain allowlist empty.
An unrelated network action continues to require the existing explicit
approval and out-of-sandbox execution path.

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
- A new credential, capability token, identity rule, gateway verb, approval
  policy, or authorization rule.
- Automatic recovery by granting broad network access when the local transport
  fails.

## Terms

- **Managed command sandbox**: the Linux sandbox that Codex applies to a
  model-issued command. It uses an isolated network namespace and a named Codex
  permission profile. Its hosting execution surface owns explicit sandbox
  approvals. It does not include the Codex app-server or its provider
  connection, and it is not a Tightbeam ACP permission request that
  `Tightbeam.ACP.Conn` answers automatically.
- **Gateway-local session**: a Tightbeam session placed on the gateway's host,
  identified by a host-registry row with `ssh == nil`.
- **Local agent socket**: the gateway-owned Unix-domain stream socket at the
  absolute path in `config.local_agent_socket`. The path denotes transport, not
  authority.
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
- **Managed-profile compatibility stamp**: the exact Codex version and the
  SHA-256 of the canonical managed-profile template that the release gate
  proved. The template has typed `workspace_root` and `local_agent_socket`
  slots. The Tightbeam release embeds the stamp beside its Codex harness
  preset.
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
   system user. This MVP does not cross a user boundary.
7. The hosting Codex execution surface sends a blocked unrelated network action
   to its existing explicit approval path. A surface that automatically allows
   a Codex sandbox escalation does not satisfy this spec's support predicate.

If assumption 2, 3, or 4 fails on a supported release candidate, the release
is blocked. An implementer does not substitute a TCP exception, a wildcard
Unix-socket permission, or full network access.

## Invariants

### I-1 — One narrow network capability

For the managed profile, Tightbeam generates an empty domain allowlist and one
`allow` entry whose key is the absolute local agent socket path. Tightbeam sets
`dangerously_allow_all_unix_sockets = false` and
`allow_local_binding = false`. The filesystem profile grants `read` to the
private runtime directory, whose only entry is the local agent socket.

Acceptance example (AC-1): Given the generated profile, when a test reads its
effective Codex network policy, then it contains one allowed Unix socket, zero
allowed domains, `allow_local_binding = false`, and
`dangerously_allow_all_unix_sockets = false`; its added readable directory
contains only the socket.

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

When a session endpoint file contains `socket`, the CLI makes one local-socket
connection attempt. A failed attempt ends the command without using `url`.
Before the CLI writes request bytes, it reports a connect error. After it writes
one request byte, a missing complete HTTP response reports
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
of captured gateway logs and CLI stderr finds neither sentinel.

## Architecture

### R-1 — One gateway-owned socket lifecycle

`config.local_agent_socket` is the single mutation seam for the local
transport. Its default is `nil`, which starts no local listener and changes no
session endpoint or command posture. A Linux host that offers the managed
local-gateway mode sets it to an absolute path. The packaged host integration
uses `<base_dir>/run/local-agent/gateway.sock`. The gateway creates that
path's dedicated parent directory with mode `0700` and the bound socket with
mode `0600` before it starts a managed Codex adapter. If the directory contains
an entry other than the configured socket, boot stops with
`local_agent_runtime_conflict` and leaves every entry in place.

The path must be absolute and must fit the host's Unix-socket path limit. A
non-absolute or over-limit configured path stops gateway boot with
`invalid_local_agent_socket` and names the path constraint.

Acceptance example (AC-9): Given `local_agent_socket = nil`, when the gateway
boots, then it creates no listener or runtime directory. Given a configured
path in a fresh Linux base directory, when the gateway boots, then the runtime
directory and socket exist with the specified modes and the local listener
accepts an authenticated `GET /harnesses`. Given an unexpected directory
entry, boot returns `local_agent_runtime_conflict` without removing it.

### R-2 — Stale paths resolve without deleting unknown material

At bind time the gateway handles the socket path as follows:

- An absent path is available for bind.
- A live socket owned by the gateway user returns
  `local_agent_socket_in_use`; the gateway leaves it in place.
- A socket owned by the gateway user for which `connect(2)` returns
  `ECONNREFUSED` is stale; the gateway unlinks that socket inode and binds the
  replacement.
- Another file type or another owner returns
  `local_agent_socket_path_conflict`; the gateway leaves it in place.

On clean listener termination, the gateway unlinks the path only when its
device and inode still equal the socket that this listener bound. It leaves a
replacement or conflicting path in place.

Acceptance example (AC-10): Given each path state above, when the listener
starts, then it binds only the absent and stale-owned cases, preserves the live
and conflicting inodes, and reports the named result. Given a path replacement
after bind, when the listener terminates, then it preserves that replacement.

### R-3 — Listener order exposes only a complete gateway

The gateway starts the local CLI listener after its router dependencies and
after `AdapterCoordinator` and `LaneManager`. It starts the existing TCP Bandit
listener next. Readiness reports both listeners only after both accept
connections, and it prints the local listener path without a token.

Acceptance example (AC-11): Given a boot probe at each child boundary, when the
gateway starts, then the local socket accepts no request before
`AdapterCoordinator` and `LaneManager` are live; after readiness, an
authenticated `GET /harnesses` succeeds through both listeners.

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
session file, a valid `socket` selects Unix transport and `url` remains
diagnostic compatibility material. A session file without `socket` selects the
existing HTTP transport.

Acceptance example (AC-13): Given nested working directories and a nearest
session file with `socket`, when discovery runs, then it selects that socket,
retains the nearest file as origin, and ignores an environment HTTP endpoint.

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

### R-7 — The managed profile permits the socket, not localhost

Tightbeam generates a Codex permission profile that:

- extends the existing managed workspace filesystem posture;
- preserves the existing `bypass_hook_trust` setting and configured hooks;
- grants read access to the private local-agent runtime directory;
- sets `network.enabled = true`;
- activates `features.network_proxy`;
- defines no allowed domain;
- allows the exact `config.local_agent_socket` under
  `network.unix_sockets`;
- keeps `allow_local_binding = false`;
- keeps `dangerously_allow_all_unix_sockets = false`; and
- keeps the existing interactive approval policy for sandbox escalation.

Tightbeam writes the generated profile into session-owned launch material. It
does not modify the identity repository, the user's Codex configuration, or
the user's permission profiles. The adapter passes the merged configuration
only to the selected managed command launch.

Codex applies proxy readiness, the effective destination policy, and command
start as one boundary. If the proxy cannot start or the profile cannot apply,
Codex returns `managed_network_proxy_unavailable` and does not start the
command. Tightbeam supports managed mode only for a stamped Codex release whose
gate executes this failure case.

The profile generator accepts no caller-supplied domain, wildcard socket,
proxy URL, or local-binding override. An operator who wants another network
destination uses Codex's existing approval path; this feature does not add an
allow surface.

Acceptance example (AC-15): Given the generated profile in a real Codex
managed sandbox, when a command connects to the Tightbeam socket, an unlisted
Unix socket, the gateway's TCP loopback port, and a host-side TCP fixture, then
only the Tightbeam socket connects without approval. The effective launch
keeps the pre-existing hooks and `bypass_hook_trust` value, and the files that
supplied them remain unchanged. When the proxy-start fixture fails, then the
command does not start.

### R-8 — Capability mismatch refuses the managed profile

Before enabling the managed profile for a Codex release, the release gate runs
the pinned `CODEX_PATH` binary with strict configuration and the generated
profile. It proves local-socket success, IP denial, and proxy-start failure.
The release embeds the resulting managed-profile compatibility stamp. At
adapter start, Tightbeam compares the selected `CODEX_PATH` version and
canonical template SHA-256 with that stamp. It also verifies that the
materialized `workspace_root` equals the selected worktree and that the
materialized `local_agent_socket` equals `config.local_agent_socket`. A
mismatch or a release that cannot parse or enforce the profile receives
`managed_local_gateway_unsupported`.

Open-network and full-access Codex modes keep their existing behavior. The
gateway does not silently select one of those modes after this refusal.

Acceptance example (AC-16): Given a Codex fixture that rejects
`network.unix_sockets`, when managed-mode readiness runs, then the adapter
refuses before a turn with `managed_local_gateway_unsupported` and starts no
fallback adapter.

### R-9 — Errors identify the layer and next action

The CLI maps outcomes to the following stable classes:

| Observed boundary | CLI result | Remedy |
| --- | --- | --- |
| `connect(2)` returns `EACCES` or `EPERM` before HTTP bytes | `local_gateway_connect_denied` | expose the configured socket in the managed profile; do not change token or provider |
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

The runtime directory persists across gateway-process restarts. A gateway
restart replaces a stale owned socket at the same path. The session endpoint
file and token remain valid. A CLI command during the gap reports
`local_gateway_unavailable`; the first command after listener readiness uses
the same path and principal.

Acceptance example (AC-18): Given one active local session, when the gateway is
stopped between two read requests and restarted, then the first request
succeeds, the gap request reports `local_gateway_unavailable`, the final
request succeeds, and both successful rows carry the same session principal.

### R-11 — Upgrade order preserves old sessions

The release installs the gateway and matching CLI as one versioned package, as
the current release contract requires. The new gateway starts its local
listener before it projects `socket` into a gateway-local session file. Before
it enables the managed profile, it reconciles each active gateway-local session
endpoint so `socket` equals `config.local_agent_socket`. A new CLI against an
old session file uses HTTP. An old CLI ignores the added JSON field and retains
its existing HTTP behavior outside the managed profile.

The managed profile becomes selectable only after the matching CLI and local
listener pass AC-15. This order prevents an old CLI from entering an
IP-disabled sandbox with no Unix transport implementation.

Acceptance example (AC-19): Given the four old/new CLI and old/new endpoint
file combinations, when they run outside managed mode, then each uses its
supported transport; when managed mode is requested with the old CLI, then
readiness refuses before a turn.

### R-12 — Host and harness scope is explicit

The MVP support predicate is:

`os == linux AND config.local_agent_socket != nil AND session.socket == config.local_agent_socket AND host.ssh == nil AND harness == codex AND compatibility stamp matches AND approval surface == explicit`.

When the predicate is false, Tightbeam keeps the existing transport and
permission behavior. The predicate is a mechanical conjunction over recorded
facts and a release-gate result; it makes no model or operator judgment.

Acceptance example (AC-20): Given the cross-product of Linux/macOS,
configured/unconfigured socket, local/satellite, Codex/Claude,
proven/unproven capability, and explicit/automatic approval surface, when
Tightbeam selects a command posture, then only the tuple that satisfies the
predicate selects the managed local-socket profile.

### Pattern and subtraction ruling

This spec establishes the **gateway-only local transport** pattern. It applies
only to an agent CLI that targets a gateway on the same Linux host from a
network-restricted Codex command sandbox. It does not apply to provider calls,
satellite placement, device traffic, or general localhost access.

Canonical example: a gateway-local Codex agent runs `tightbeam attest ...` in
its managed sandbox; the CLI discovers `.tightbeam-session.socket`, connects
over the allowlisted Unix socket, and the existing router records the session
principal. A subsequent `curl https://example.com` remains denied until the
operator approves an out-of-sandbox retry.

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

The implementation passes when AC-1 through AC-20 pass and the following
reality smoke passes on Gibson against the release CLI, the release gateway,
and the pinned Codex binary:

1. Start a real gateway on a disposable base directory and its real Unix
   listener.
2. Create a real gateway-local session endpoint through Placement; do not
   hand-author the endpoint fixture.
3. Run the released `tightbeam` CLI inside Codex's real managed Linux sandbox
   with the generated profile.
4. Execute one authenticated read and one idempotent mutation through the Unix
   socket. Verify the returned JSON and the attributed durable row.
5. In the same sandbox, attempt the gateway TCP loopback port, another host TCP
   listener, and one unlisted Unix socket. Verify three denials and zero
   connections at the fixtures. These local fixtures prove the sandbox's IP
   namespace and socket allowlist without depending on DNS or an Internet host.
6. Run one approved out-of-sandbox network fixture. Verify it succeeds without
   changing the generated managed profile.
7. Restart the gateway between two CLI reads and verify AC-18 against the real
   socket inode.
8. Scan the captured CLI stderr, gateway log, and Codex sandbox log for the
   sentinel token and body values. Verify AC-8.

The test matrix records the Tightbeam commit, CLI version, Codex version,
kernel version, canonical-template SHA-256, materialized-profile SHA-256,
baseline result, and after result. A hand-written idealized gateway response
does not satisfy this acceptance.

Traceability:

| Requirement | Acceptance |
| --- | --- |
| I-1 | AC-1, AC-15 |
| I-2 | AC-2, AC-14 |
| I-3 | AC-3 |
| I-4 | AC-4 |
| I-5 | AC-5, AC-20 |
| I-6 | AC-6, AC-12 |
| I-7 | AC-7, AC-17 |
| I-8 | AC-8 |
| R-1 | AC-9 |
| R-2 | AC-10, AC-18 |
| R-3 | AC-11 |
| R-4 | AC-6, AC-12 |
| R-5 | AC-5, AC-13 |
| R-6 | AC-2, AC-14 |
| R-7 | AC-1, AC-15 |
| R-8 | AC-16, AC-19 |
| R-9 | AC-7, AC-17 |
| R-10 | AC-18 |
| R-11 | AC-19 |
| R-12 | AC-20 |

## Open Questions

None. A failed release-gate assumption is a named unsupported value under R-8,
not an invitation to widen network access.
