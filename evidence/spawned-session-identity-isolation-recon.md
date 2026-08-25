# Spawned-session identity isolation: seam recon

Status: F14 adapter-custody amendment draft after `att_592009bf`  
Work item: `wi_b8802849-0d10-475b-b5e6-2458842c9c11`  
Custody-recovery assignment: `asg_3e7d1e5e-6afe-4731-8908-8faf690e1fbc`  
Prior F8 successor assignment: `asg_6cca1e12-2dd6-45c6-9235-45830a8f5af2`  
F8 authority: `att_37069ca1-2639-4e62-978c-309e1b939711`,
`att_dfa90221-6593-42b3-ad68-8de75377f1b7`, and
`att_534d5e79-c9e9-4053-9584-acba0128b0ff`  
F8 successor review: `att_abccf4d6-a9fc-40d4-825c-359f687d9f09`; report `art_37482b6d`
SHA-256 `4fcd86c3032c4ebfe49201de052758276fa4e6e3bd056e9529e9c5fddad722a3`  
Custody-recovery authority: conditional verdict `att_3df70905-ca8c-4974-8a02-0b46415c9570`  
F13-F16 amendment authority: conditional verdict
`att_7d4e06a1-90e6-4b31-8771-7fb4c5a0a25c`  
F13-F16 exact-artifact review: changes-requested `att_592009bf`; restored report `art_5ba40ba0`
SHA-256 `73830c05e2ec4434db44cd5688f3766ccfcc4cb19359808a70ef216cb7750b02`  
F14 seam decision: decision request `dr_bee56f9e-be60-482a-a3d3-63dabeb17789` is ruled
`adapter-custody`  
F9-F12 exact-artifact review: changes-requested
`att_5f51503c-e678-4c2f-a847-43e8cd41db08`; report `art_83c07b23` SHA-256
`2d829f2330a0ca5cf62ad66bf19f8091d014b4e2d2cfa8ad87e259320f963d75`  
Successor assignment: `asg_5c27fc52-3004-47a9-a64d-51130c94687d`  
Superseded producer assignment: `asg_0298d1db-4a0e-47d8-b64e-68dc4deb480a`  
Direct owner assignment: `asg_4f7d2199-7281-48cb-a2b1-57d2ec64da94`  
Recon dates: 2026-08-11–2026-08-14; F14 source-object recheck 2026-08-25  
Delivery target: Tightbeam `0.2.0`  
Sole source revision: `be61cfc98df6b18c0cc280adeca42cba3fbf14b5`
(`origin/0.1.x`)  
Remote: `git@github.com:clickety-clacks/tightbeam.git`  
Source-object repository: object `be61cfc98df6b18c0cc280adeca42cba3fbf14b5` in the producer's
owned clone `/home/mike/.tightbeam/work/877b1cfa8188/tightbeam`, read only with `git show`  
F8 source receipt: `att_3fe88a9e-4620-477e-b239-ae933a37365f`  
Canonical product spec home: `specs/tightbeam/spawned-session-identity-isolation.md`  
Canonical companion home: `evidence/spawned-session-identity-isolation-recon.md`  
Installation seam: after `reviewed-clean`, the opener installs the exact reviewed bytes at those
paths and gives implementation the canonical spec path plus its SHA-256. This branch copy is not
review-cleared or installable.

Frozen predecessor artifacts `art_a2c67e69` and `art_75ad8a2d` remain sealed history. Prior F8
review subjects `art_77d4eb7e` and `art_40cfd70e`, and their spec-ready verdict
`att_31b24275-6a2c-48c0-9f6b-b1bd7daf4e34`, are quarantined as inaccessible historical hash
records by `att_3df70905-ca8c-4974-8a02-0b46415c9570`. Review
`att_abccf4d6-a9fc-40d4-825c-359f687d9f09` remains historical evidence about those exact hashes;
it does not supply readable-byte custody. This successor does not claim recovery or sealed custody
of those F8 bytes. Artifact `art_15800663` remains separately quarantined by
`att_54a89fcd-0d06-405d-8617-bc618258ffa6`.
Reviewed artifacts `art_f818e435` and `art_23ed387d` are immutable changes-requested history
under `att_5f51503c-e678-4c2f-a847-43e8cd41db08`; this successor does not edit their recorded
homes.

## Scope and custody

This report traces the identity path from session creation to CLI dispatch. It covers local and
remote workdir materialization, marker discovery, harness session configuration, bearer-token
authentication, identity selection, host relocation, and present test coverage.

No checked-out worktree file or occupied worktree supplies a source fact in this successor. No product file,
session marker, identity row, Gateway runtime, deployment, or live session was changed or probed.
During F9-F12 recon, the producer read two occupied-worktree source paths in
breach of the Git-object-only release. `att_79aa0729-5fb4-4573-bd4d-09da0f297a9d` records the
read-only breach and absence of mutation. Those observations were discarded. The producer then
re-derived the F9-F12 source facts only through `git show` of the released object above. At that
object, `lib/tightbeam/session_lane.ex` has SHA-256
`55fb04e39243ab5b9d533eec25abbbd097a918e5b4259520cfa0f547f25e8f66`, and
`test/lane_test.exs` has SHA-256
`0cb00a86fef7e9a600bb7f886044fdc24611b46c452f1437711a73a21b5ce677`.

A fresh 2026-08-14 read-only re-derivation used only `git cat-file`, `git show`, `git grep`,
and `git diff` over object `be61cfc98df6b18c0cc280adeca42cba3fbf14b5`. Its `AGENTS.md`
identifies `0.1.x` as the maintenance line and forbids targeting `main`. The re-derivation
re-read the repository law, source-declared adapter package pins, ACP request seams, cwd resolver,
binding-adjacent EventLog and Schema seams, and the complete source citations below. No
occupied-worktree observation supplies a source fact in this successor.

The installed CLI reports version `0.1.7`. The repository manifest also reports `0.1.7`.
`/opt/homebrew/bin/tightbeam` resolves into the installed npm package. The installed package does
not identify its source commit, so version equality is the strongest installed-to-source
provenance claim available from package material.

Installed executable SHA-256 values captured during recon:

- CLI: `2619300168090e7425a817fdbff3adb5dd10e8e296d281d0c84939eb8ea549d4`
- gateway launcher: `ce7dd7836a840f21b893c156ea22c1b3127d0c4ea804aed06e5577e1deac1351`

## Evidence classification

### Verified facts

1. The Rust CLI represents a session endpoint as `Origin::Session(PathBuf)` and describes that
   path as a marker found by walking upward from the working directory
   (`cli/src/dispatch.rs:33`).
2. Endpoint discovery obtains the process cwd, visits `cwd.ancestors()`, and selects the first
   existing `.tightbeam-session` before it considers the explicit URL/token pair or the
   provisioned gateway file (`cli/src/dispatch.rs:883`, `cli/src/dispatch.rs:887`,
   `cli/src/dispatch.rs:897`, `cli/src/dispatch.rs:901`).
3. The selected marker contributes `url` and `token`. The CLI does not parse or compare the
   marker's `sessionKey` (`cli/src/dispatch.rs:908`).
4. The current unit test requires nearest-ancestor selection and gives marker discovery priority
   over explicit endpoint environment (`cli/src/dispatch.rs:2410`). A malformed nearer marker
   refuses instead of falling through (`cli/src/dispatch.rs:2455`).
5. CLI help and its implicit-identity refusal describe upward discovery as supported behavior
   (`cli/src/args.rs:374`, `cli/src/args.rs:599`, `cli/src/dispatch.rs:1344`).
6. Placement writes one marker at the computed session work root. Its JSON fields are `url`,
   `token`, and `sessionKey` (`lib/tightbeam/placement.ex:295`). Local markers converge to mode
   `0600`; remote materialization checks or establishes the same mode
   (`lib/tightbeam/placement.ex:797`).
7. A work root is `<host.base_dir>/work/<first 12 lowercase hex characters of
   sha256(sessionKey)>` (`lib/tightbeam/placement.ex:347`). The path is derived from the key; it is
   not stored as an authorization binding.
8. Session creation mints one random `tbs_` CLI token. `Org.by_cli_token/2` returns the active
   session whose `cliToken` equals the bearer token (`lib/tightbeam/org.ex:188`,
   `lib/tightbeam/org.ex:237`, `lib/tightbeam/org.ex:1147`).
9. `/agent/dispatch` checks exact CLI protocol compatibility before bearer authentication.
   Authentication derives the session principal only from the token lookup
   (`lib/tightbeam/wire/router.ex:119`, `lib/tightbeam/wire/router.ex:392`). It does not receive or
   verify the marker path, marker `sessionKey`, work root, host, or marker generation.
10. After bearer authentication, a session can select only a role held by that session. It can
    select only its owner with `--as-user`. It cannot select a process identity. An organization
    token retains the distinct explicit role, user, and process paths
    (`lib/tightbeam/wire/router.ex:452`).
11. Spawn persists the session before `finish_spawn/4` returns it
    (`lib/tightbeam/gateway.ex:3975`, `lib/tightbeam/gateway.ex:4018`). Marker materialization is
    first forced by `Placement.holder_workdir/2` when the gateway provisions a harness session,
    not by the spawn commit (`lib/tightbeam/gateway.ex:2294`).
12. One adapter process is shared by harness and host. The ACP boundary sends a per-session cwd
    and `_meta` on new, load, and fork, but it calls `session_config/2` with an empty session map
    (`lib/tightbeam/acp/adapter.ex:702`, `lib/tightbeam/acp/adapter.ex:751`,
    `lib/tightbeam/acp/adapter.ex:801`). Adapter process environment is therefore not a safe place
    for session-specific identity.
13. Source baseline `be61cfc9` declares `@agentclientprotocol/codex-acp` `1.1.4` and
    `@agentclientprotocol/claude-agent-acp` `0.66.0`
    (`lib/tightbeam/harness/codex.ex:10`, `lib/tightbeam/harness/codex.ex:122`,
    `lib/tightbeam/harness/claude.ex:10`, `lib/tightbeam/harness/claude.ex:152`). Registry metadata
    read on 2026-08-12
    reports the exact tarball integrity values
    `sha512-DzusIpGwlQwMWuHgJhU8FWMsyQvzjenB93IEzQATkdbNulo5Rd9GKOz8+B+/C9iWWxmyXgtgmjzaL+iRFyDryQ==`
    and `sha512-BwalxKsxZzHZGEs+X9hV3biErLE7PHWoao2hmyP3QBWXxvMHbc1F1tzDE95ZA47Fle+KBYf2gKpgy1MJ+ZmVlw==`,
    respectively. The source resolves their executable entries under
    `<registered-host-base>/adapters/node_modules/.bin/` (`lib/tightbeam/harness/support.ex:948`).
    The exact patched bundles are
    `node_modules/@agentclientprotocol/codex-acp/dist/index.js` and
    `node_modules/@agentclientprotocol/claude-agent-acp/dist/acp-agent.js`
    (`lib/tightbeam/harness/codex.ex:66`, `lib/tightbeam/harness/claude.ex:12`).
    The current Eezo manifests under
    `/Users/mike/.tightbeam/adapters/node_modules/@agentclientprotocol/` instead reported
    `codex-acp` `1.1.9` and `claude-agent-acp` `0.59.0`; those installed packages are not the
    source-declared proof subject.
    Fresh Eezo reads
    observed Codex CLI `0.146.0` at `/opt/homebrew/bin/codex`, SHA-256
    `134063e133f0b4244fa3b251acf973d4fe4b4aeeacbdc135211bf480f59f1477`, and Claude Code `2.1.227`
    at `/opt/homebrew/bin/claude`, SHA-256
    `7432511ba3be818e01f23f6eef8630d214a8b618451e188c3c7d61a987eef6c7`. No carrier was executed or
    proven.
14. Source baseline `be61cfc9` issues ACP `session/new`, `session/load`, and `session/fork`. Its
    `session/load` is the persisted-session re-entry operation in scope. The official ACP changelog
    (`https://github.com/agentclientprotocol/agent-client-protocol/blob/main/CHANGELOG.md`) now
    records a newer draft `session/resume`, but this source baseline does not issue that method.
    This recon therefore makes no `session/resume` carrier claim.
15. Host relocation copies the complete workdir between local or remote hosts and removes the
    source marker. The gateway updates the session host after placement returns
    (`lib/tightbeam/placement.ex:881`, `lib/tightbeam/gateway.ex:4203`,
    `lib/tightbeam/gateway.ex:5958`). The marker token does not rotate, and the gateway has no
    location epoch to reject a stale copy.
16. Remote placement carries the advertised gateway URL in the marker. Shared adapter launch
    environment carries host-level values, not a session token. Session identity therefore still
    depends on cwd marker discovery on remote hosts (`lib/tightbeam/placement.ex:299`,
    `lib/tightbeam/placement.ex:1115`).
17. The current host registry uses operator-chosen `name` as its only key. It stores ssh
    destination, base directory, CLI directory, and adapter directory, with no stable identifier for
    the physical base directory (`lib/tightbeam/placement.ex:100`,
    `lib/tightbeam/placement.ex:147`). Assimilation resolves the remote base with `cd ... && pwd` but
    registers only the chosen name and those path/transport values (`cli/src/ceremonies.rs:1488`,
    `cli/src/ceremonies.rs:1567`, `cli/src/dispatch.rs:836`). Two registered names can therefore
    structurally address one physical work root without the registry recognizing that equivalence.
    Physical alias detection and shared data custody are outside this identity work. The successor
    spec accepts a collision only as a named marker-custody refusal.
18. Repository law and operational material still teach cwd-derived identity. The operating manual
    says a session's workdir supplies the credential (`priv/guidance/operating-manual.md:24`), the
    inter-node runbook says the CLI walks upward from a session workdir
    (`docs/INTER-NODE-COMMS.md:46`), and the rail observation description says its hook resolves
    identity from the workdir marker (`lib/tightbeam/rails.ex:182`). These are implementation seams,
    not authority for retaining the unsafe behavior; they must change with the CLI contract.
19. The current database boot path treats incompatible pre-release table shapes as a named refusal.
    It does not alter or infer an existing table shape (`lib/tightbeam/schema.ex:729`). The existing
    `org_settings` table already supplies a key/value mutation seam (`lib/tightbeam/org.ex:102`,
    `lib/tightbeam/org.ex:147`, `lib/tightbeam/org.ex:167`). One additive `session_credentials`
    table and a write-once migration-start setting fit this repository law; adding columns to the
    existing `hosts` table does not.
20. The packaged `tightbeam-gateway` launcher resolves the installed release and dispatches every
    release command through one shell seam (`packaging/tightbeam-gateway:11`,
    `packaging/tightbeam-gateway:45`, `packaging/tightbeam-gateway:70`). It has no install, downgrade,
    or rollback operation. A wrapper shipped inside a package cannot remain the security fence when
    an operator replaces that package with an earlier one.
21. The existing remote-client ceremony asks each registered CLI for its version and refuses a
    staged binary whose answer does not exactly equal the current package version
    (`cli/src/ceremonies.rs:1249`, `cli/src/ceremonies.rs:1266`,
    `cli/src/ceremonies.rs:1683`). Migration can reuse that bounded, exact-version seam instead of
    inferring remote compatibility from host registration.
22. Database boot checks `schema_stamp` before it ensures product schemas. The current binary
    accepts exactly its one known shape row, rejects one different row, and rejects more than one
    row with `ShapeError` (`lib/tightbeam/schema.ex:729`, `lib/tightbeam/schema.ex:902`). An additive
    second stamp therefore makes the migrated database deterministically unreadable to the prior
    binary before agent-turn intake, while the new binary can explicitly recognize the exact pair.
23. Repository release law rolls an installed test host back by selecting an earlier proved package
    and rolls source forward through a reviewed revert commit and new candidate
    (`docs/RELEASE_TRAIN.md:133`). It does not provide a runtime rollback command. Credential
    migration must therefore fence the database itself and direct post-migration recovery to a
    current forward-repair release.
24. Read-only source receipt `att_3fe88a9e-4620-477e-b239-ae933a37365f` inspected Git object
    `be61cfc98df6b18c0cc280adeca42cba3fbf14b5`. It records
    `lib/tightbeam/session_lane.ex` SHA-256
    `55fb04e39243ab5b9d533eec25abbbd097a918e5b4259520cfa0f547f25e8f66` and
    `test/lane_test.exs` SHA-256
    `0cb00a86fef7e9a600bb7f886044fdc24611b46c452f1437711a73a21b5ce677`.
    `SessionLane.at_turn_boundary/2` excludes claims only while it services the callback. Its
    handler replies with `fun.()` and returns to the mailbox; a later nudge can then reach
    `Ledger.claim_next/3`. `test/lane_test.exs` is the direct test seam. This is the F8 source fact;
    it does not change the pinned behavioral baseline for F1-F7.
25. Exact-artifact review `att_abccf4d6-a9fc-40d4-825c-359f687d9f09` found four F8 defects:
    recovery began after unsafe effects; the ACP-error-only envelope omitted transport and adapter
    failures; `restart_repair` had no legal authenticated caller; and the pre-activation pending
    release was unreachable. Its full report independently hashes to the value in this header.
26. A corrected read-only Git-object recheck of
    `be61cfc98df6b18c0cc280adeca42cba3fbf14b5` confirms `Acp.Conn` returns
    `{:error, :timeout}` and `{:error, :closed}`, Adapter returns malformed-success and
    cleanup-bearing preparation failures, and EventLog has no existing raw-envelope redactor.
    Process receipt `att_79aa0729-5fb4-4573-bd4d-09da0f297a9d` records that the producer first read
    those two source files through the prohibited occupied-worktree path. That read changed no
    bytes; its observations were discarded before this Git-object recheck and amendment.
27. `Tightbeam.Gateway` is a composition module whose `children/1` and handler functions wire named
    processes. The source does not define a Gateway GenServer, Gateway PID, boot reference, or
    process incarnation (`lib/tightbeam/gateway.ex:1`, `lib/tightbeam/gateway.ex:9`,
    `lib/tightbeam/gateway.ex:17`, `lib/tightbeam/gateway.ex:129`). The exact source-object file
    SHA-256 is `6d0ae49e89e01b795c9a201946da3ceaf24efa479ebd7b5bc704e028fa3d1f98`.
28. `Tightbeam.Acp.Adapter` is a GenServer. Its state owns `:conn`; its public `new_session/5` and
    `load_session/6` calls send the corresponding work to that process
    (`lib/tightbeam/acp/adapter.ex:22`, `lib/tightbeam/acp/adapter.ex:49`,
    `lib/tightbeam/acp/adapter.ex:99`, `lib/tightbeam/acp/adapter.ex:118`). The exact source-object
    file SHA-256 is `a3052838f8c9efc218258e91d004b15474d1be318a03d614720f445d41975b4a`.
29. `Tightbeam.AdapterCoordinator` owns one temporary Adapter per
    `{harness, archetype, host}`. It returns the Adapter PID and monotonic generation, monitors the
    PID, records `DOWN`, increments the generation, and schedules the replacement
    (`lib/tightbeam/adapter_coordinator.ex:1`, `lib/tightbeam/adapter_coordinator.ex:6`,
    `lib/tightbeam/adapter_coordinator.ex:31`, `lib/tightbeam/adapter_coordinator.ex:47`,
    `lib/tightbeam/adapter_coordinator.ex:517`, `lib/tightbeam/adapter_coordinator.ex:573`,
    `lib/tightbeam/adapter_coordinator.ex:690`, `lib/tightbeam/adapter_coordinator.ex:697`). The
    exact source-object file SHA-256 is
    `3e93bd0a652d4c8359ace3f4970407a16368990504979d5a7dd6766b228aa40b`.

### Provenance

Commit `91fa15697b39d873543e8c1a97140ee69c4a3018` introduced the current
`cwd.ancestors()` behavior on 2026-07-25 with the subject “Restore session-implied CLI identity.”
The Rust CLI itself entered the repository in commit
`7f6144d75bee5b7058d0115d60264f0674e82329` on 2026-07-19. This history establishes that upward
discovery is an intentional compatibility behavior, not an incidental filesystem call.

### Unconfirmed history

Attest `att_13437f28-85af-4409-a851-a0effe409735` records an earlier observation that session
`s_3a51b15e` appeared as parent session `s_7269208c` and identifies upward discovery as the
structural route by which that result can occur. The available record does not contain a captured
request, marker fixture, or gateway event that confirms damage from that occurrence.

The later controlling ruling, attest `att_9f954a6e-b9c1-4b74-9256-325535f5c7c5`, states that the
Eezo no-filing failures were protocol-version skew: the CLI offered `0.1.3` while the gateway
required `0.1.4`. The self-check for the affected session passed. That incident is not evidence of
this marker-selection seam. This work item has zero confirmed damage specimens as of this report.

The structural fact remains independently verified: a process whose cwd sits under another
session's marker selects that marker and sends its bearer token. The resulting gateway principal
is the session named by that token.

## Threat model

### In scope

- A cooperative agent or tool runs the CLI from an unexpected cwd.
- A checkout, nested worktree, or parent directory contains another session marker.
- A marker is malformed, copied, stale after retire or move, or located through a symlink.
- A shared adapter provisions concurrent sessions and leaks session-specific configuration from
  one request to another.
- Local-to-local, local-to-remote, remote-to-local, or remote-to-remote relocation stops between
  filesystem preparation and database commit.
- A caller supplies marker claims that disagree with the bearer token's database session.

### Outside this item's guarantee

- A malicious process running as the same operating-system account reads another session's
  `0600` token and deliberately constructs a request. Filesystem permissions do not isolate
  processes that share an account.
- Theft of the organization token, gateway host compromise, transport security, or model prompt
  injection.
- A new user-facing role or process-impersonation policy. Present gateway authorization remains
  authoritative.
- Physical-base alias detection, host-alias ownership, shared-root data custody, and alias
  re-registration. If two session derivations collide, identity material must remain unchanged and
  the operation must fail by marker custody or binding mismatch.

The target is structural selection safety. Changing cwd must not change which session credential
the CLI reads. This does not turn same-account workdirs into a security sandbox.

## Existing coverage and missing proofs

### Existing coverage

- `cli/src/dispatch.rs:2410` proves nearest ancestor wins and environment loses to a marker;
  `cli/src/dispatch.rs:2455` proves a malformed nearest marker refuses.
- `test/cli_integration_test.exs:288` proves implicit session dispatch from a nested cwd, explicit
  owner selection, no-marker behavior outside the tree, and token rejection after retire.
- `test/placement_test.exs:278` and later move cases cover the four local/remote copy directions,
  source-marker removal, marker mode, convergence, and remote command redaction.
- `test/gateway_test.exs:6134` checks the current three-field marker shape.
- Router and CLI integration tests cover held-role, owner-user, process, retired-token, and exact
  CLI-version behavior.

### Missing proofs

- No test binds marker `sessionKey` to its token.
- No test proves a child-session process cannot select a parent or sibling marker.
- No test makes cwd irrelevant to credential selection.
- No test rejects a symlinked marker or a symlinked registered work root.
- No test gives a marker a schema, credential identifier, or location generation.
- No gateway test compares marker claims with the token's session binding.
- No relocation test proves which credential works on each side of the database commit.
- No adapter test proves two concurrent sessions receive distinct marker anchors on source-baseline
  `session/new`, `session/load`, and `session/fork`.
- No isolated real-adapter fixture proves that Codex and Claude tool subprocesses receive their
  per-session anchor without cross-session leakage.
- No retirement test proves that credential revocation and session retirement commit as one durable
  transaction with one event.
- No same-root relocation test proves the new security path refuses before mutation and creates no
  staging object.
- No lane test proves that a returned `upgrade` or `host_recovery` failure retains turn exclusion,
  restores it after a lane or gateway crash, or admits only a matching process, attempt, and
  generation retry. No test proves that a failed `restart_repair` terminates unavailable and
  releases without another ACP call.

## Design ruling

The specification adds one session-bound anchor that the gateway supplies to each harness session
through its per-session configuration request. The CLI must read only the marker named by that
anchor. It must not search cwd or its ancestors for identity material. The marker must carry an
independent session key, credential identifier, generation, host, and registered work root. The
anchor also carries the expected gateway URL, so marker corruption cannot redirect the bearer
token before a gateway check. The CLI validates anchor claims before dispatch. The gateway
validates binding claims against the session selected by the bearer token. The binding and marker
also persist the preparing operation's cause and durable principal, so retry and recovery reproduce
accountable bytes.

The successor deletes physical-base identifiers, root leases, host inventories, custody
adjudication, and alias re-registration. They solve a separate data-ownership problem and are not
required to prevent wrong-parent identity. If two session derivations reach one trusted root, the
existing marker remains unchanged and Placement returns `session_marker_custody_mismatch`.
Deletion wins because a named refusal meets this work item's safety goal without assigning file
ownership. A separate work item can specify physical data custody if the product needs it.

The successor also deletes same-root credential staging. A same-root relocation returns
`session_relocation_same_root` before mutation. Different-root relocation retains the existing
prepare, commit, cleanup, and forward-repair design.

Vendor carrier claims remain blocked. The proof subject is now exact: source-declared
`@agentclientprotocol/codex-acp` `1.1.4` with its registry integrity and Codex CLI `0.146.0`
SHA-256 `134063e1...`, and `@agentclientprotocol/claude-agent-acp` `0.66.0` with its registry
integrity and Claude Code `2.1.227` SHA-256 `7432511b...`. The current Eezo adapter-directory
packages do not match those declared versions and are ineligible for the proof. Source-baseline ACP
operations are `session/new`, `session/load`, and `session/fork`; this work does not claim the newer
draft `session/resume`. The canonical spec must record the exact ACP-to-vendor mapping after the
isolated proof and before vendor-harness implementation.

This makes the dangerous state unconstructable in the normal CLI resolver: a session endpoint can
exist only after a complete anchor and marker agree. Cwd cannot construct a session origin.

Adding this anchor wins the subtraction test. Deleting implicit session identity would break the
normal agent CLI workflow. Accepting the failure would preserve silent attribution and authority
corruption.

Post-migration binary rollback loses the same test. A compatibility layer that lets the prior
binary run cannot prevent its cwd ancestor walk or make it understand the new binding tables.
Accepting that behavior violates the headline invariant. A packaged-wrapper preflight also loses:
selecting an earlier package replaces the wrapper itself. The specification instead inserts an
additive `session-binding-v2` schema-stamp row atomically with the migration-start record. The prior
binary's existing multiple-shape refusal then stops it before intake. The current release recognizes
the exact pair, leaves `sessions.cliToken` null for every new or terminally migrated session, and
provides forward repair. Before the transaction exists, no new binding state exists and the legacy
database remains readable by the prior release.

Migration refuses a missing legacy host alias before that fence transaction instead of inventing
transport. It clears the legacy token for each retired session in one terminal transaction and
creates no credential row for that session.

The controlling protocol-skew ruling also sets the migration gate. A session cannot activate a v2
binding until its registered local or remote CLI reports the exact pre-1.0 release version. Missing,
malformed, prior, and future versions become the named unavailable reason `cli_version_mismatch`;
they are not evidence of an identity-selection damage specimen.

An anchor identifies the credential; it does not confine cwd. A correctly anchored session keeps
its own identity when it works in a handed-off checkout or another permitted directory. Markers
found there are not candidates. This preserves remote operation and worktree handoff without
reintroducing cwd-based selection.

Retirement uses one durable transition: the same Org transaction retires the session, revokes its
current credential, clears the legacy token, and records one `session_binding_revoked` event with
cause `retirement`. The last marker remains unchanged and becomes stale. This removes the prior
active-versus-revoked ambiguity.

Cross-root relocation cannot reuse the current whole-workdir copy unchanged: that copy includes the
still-active source marker, while destination preparation must install the pending next generation
before the binding commit. The design therefore removes `.tightbeam-session` from the generic
workdir-transfer input and materializes the prepared destination marker through the credential seam.
Same-root relocation uses the named no-mutation refusal above.

F8 uses Option A from `att_37069ca1-2639-4e62-978c-309e1b939711`. The existing lane is the
deterministic turn-admission owner, so the implementation surface now includes
`lib/tightbeam/session_lane.ex` and `test/lane_test.exs`. The typed rearm-pending state persists
after an `upgrade` or `host_recovery` `session_binding_rearm_failed` result, excludes ledger claims,
admits only the matching authenticated Adapter-incarnation/attempt/generation retry, and releases on
acknowledgment or a verified terminal binding result. A failed `restart_repair` never enters that
state and instead commits the unavailable terminal result. Durable attempt rows and per-dispatch receipts bracket activation and ACP
I/O before either effect. A lane restart restores those rows before a nudge. An Adapter death
classifies an unresolved dispatch as `outcome_unknown` only after `AdapterCoordinator` observes
`DOWN`, advances the adapter generation, and thereby proves the prior Adapter and its owned ACP
connection are down. The boot path constructs a new `restart_repair` load only for an exact persisted vendor session; an
uncertain `session/new` or load without that identifier makes the binding unavailable with
`rearm_outcome_unknown` and performs no second ACP call. The current `Tightbeam.Acp.Adapter` owns
the rearm ACP request and retained result. Its source-grounded adapter key, PID, and coordinator
generation identify the incarnation. `AdapterCoordinator` monitors and replaces it; Gateway remains
a plain composition module. The boot path obtains that checkout directly, and wire callers cannot assert
`process:tightbeam`. Adding this state wins because deleting returned
failure violates F7 and accepting release permits an unarmed turn. A parallel gateway admission
check loses because the lane claims first.

The F9 recovery mechanism is the smallest state that can prove an external call was or was not
issued: one current attempt row and one receipt per retry identifier. A same-Adapter-incarnation retry dispatches
only after a completed response proves the operation retryable; a transport-uncertain result becomes
the named unavailable result `rearm_outcome_unknown`. An uncertain `session/new` after restart also
becomes unavailable because neither deletion of crash restoration nor a duplicate external session
satisfies Option A. F10 retains the required raw evidence only after the Adapter maps it into a
closed JSON-safe failure union, then uses one named EventLog redaction function. An out-of-domain
Erlang term becomes a fixed class and is never rendered, persisted, logged, or encoded. The
normalizer examines only enough structure to select that class. This
preserves the accountable artifact without claiming an arbitrary-term redactor. F11 uses the
current Adapter checkout from `AdapterCoordinator` instead of exposing a new wire principal.
F12 does not invent a post-failure branch: a pre-activation failure resolves the
`guarded` attempt through the existing migration or recovery result and never constructs
rearm-pending state. A returned `restart_repair` failure also does not create a pending hold: its
single transaction records the normalized failure, makes the binding unavailable with
`rearm_outcome_unknown`, releases the attempt terminally, and permits no retry or later ACP call.

### F8 clause map

| F8 requirement | Successor clauses | Direct proof |
| --- | --- | --- |
| Returned operator-owned failure retains exclusion; failed restart repair terminates unavailable | Terms: rearm-pending state; I-21; R-38; R-39; R-48 | AC-15; AC-20 returned-failure and failed-restart cases |
| Same Adapter incarnation, attempt, and generation retry | Terms: Adapter process incarnation and attempt identity; R-48 retry seam | AC-20 mismatch table |
| Cause, principal, and raw envelope | Terms: closed failure union; R-42; R-43 | AC-16 captured response corpus and exact redaction |
| Lane and Adapter crash restoration | I-22; R-38 boot order; R-48 durable attempt and dispatch receipts | AC-15 crash matrix; AC-20 seven cut points |
| Duplicate retry idempotency | R-42; R-48 unique dispatch receipt | AC-20 overlap and duplicate cases |
| Stale and wrong-process refusal | R-48 named refusals | AC-20 mismatch table |
| Successful and terminal release | R-48 release transitions | AC-20 acknowledgment and terminal cases |
| Nudge starvation bound | R-48 claim exclusion and mailbox bound | AC-20 100-nudge fixture |
| Internal restart authentication | Terms: Adapter rearm owner; R-48 cause-specific route | AC-20 current-checkout fixture |
| Pre-activation failure | R-48 guarded resolution | AC-20 activation-not-committed fixture |
| Authorized implementation surface | R-46 | `lib/tightbeam/session_lane.ex`; `lib/tightbeam/acp/adapter.ex`; `lib/tightbeam/adapter_coordinator.ex`; corresponding tests |

| Review finding | Successor ruling | Pass/fail evidence |
| --- | --- | --- |
| F9 — effect precedes recovery | Durable guard precedes activation; a unique prepared/dispatched receipt precedes ACP; Adapter owner retains result independently of lane | AC-20 stops at seven cuts, proves one call per receipt, and makes transport-uncertain retry or uncertain `session/new` terminal without a second call |
| F10 — envelope is partial | Closed JSON-safe union at the Adapter boundary plus one EventLog redactor over that domain | AC-16 captures real Conn/Adapter values, checks every union tag and rejected Erlang class, and proves rejected payload is not rendered, encoded, persisted, or logged |
| F11 — restart caller is impossible | `process:tightbeam` uses the current source-grounded Adapter key, PID, and coordinator generation; wire route remains reserved | AC-20 positive internal checkout plus wire refusal |
| F12 — rollback branch is fabricated | Guarded activation failure resolves as `activation_not_committed` and never enters pending | AC-20 pre-dispatch activation-failure case |
| F13 — source baselines are mixed | Every source-derived fact and citation is re-derived from `origin/0.1.x@be61cfc98df6b18c0cc280adeca42cba3fbf14b5` by Git-object reads only | This report names one source revision; verified facts, existing coverage, and implementation seams cite that object only |
| F14 — separate rearm-owner lifecycle is ambiguous | Follow decision `adapter-custody`: the current `Tightbeam.Acp.Adapter` owns ACP execution and result retention; `AdapterCoordinator` owns its existing lifecycle | Terms and R-48 identify one adapter key/PID/generation; AC-20 exercises that Adapter and its coordinator-proved replacement |
| F15 — arbitrary Erlang-term persistence exceeds the redactor domain | Delete arbitrary-term persistence: Adapter maps each result into the closed JSON-safe union before EventLog or recovery storage | R-43 is total over Erlang input classes at the Adapter boundary and redacts only normalized JSON-safe values; AC-16 covers every rejected class |
| F16 — failed restart repair can become an unowned hold | Delete failed-restart retry: the failure transaction makes the binding unavailable, releases the attempt terminally, and permits no retry, future-start wait, or later ACP call | R-38 and R-48 define the terminal transaction; AC-15 and AC-20 prove release and zero later calls |

For terminal release, an unavailable or revoked binding clears the fence without a ledger claim;
an acknowledged active generation resumes the `Ledger.claim_next/3` eligibility check. An
activation failure does not enter rearm-pending and follows the existing pre-activation binding
result. This preserves the existing unavailable and retired turn-intake prohibitions without a
fabricated rollback state.

The amendment preserves the F1-F8 security scope and quarantined history while correcting the
reviewed F9-F12 recovery clauses through the F13-F16 owner ruling and the direct-owner F14
`adapter-custody` decision. It changes only provenance, the rearm-owner model, the
failure-normalization boundary, and failed-`restart_repair` terminal handling. Non-Goals 1-11,
OQ-1, the migration and rollback fence, scope, and identity security retain their predecessor
contract. The frozen predecessor artifacts remain sealed. The drifted F8
artifact rows and their spec-ready verdict remain quarantined historical hash records under
`att_3df70905-ca8c-4974-8a02-0b46415c9570` and are not claimed as readable-byte custody.

## Exact implementation surface identified after recon

Production seams:

- `cli/src/dispatch.rs` — replace upward discovery with a typed bound-session resolver; attach
  binding claims to dispatch requests.
- `cli/src/args.rs` — replace upward-discovery help and refusal text.
- `cli/Cargo.toml` and `cli/Cargo.lock` — advance the pre-1.0 package/protocol version that the CLI
  sends and the gateway derives from the same manifest.
- `lib/tightbeam/org.ex` — persist and mutate the active credential binding with the session row;
  bind token lookup to credential state; own the durable rearm-attempt and dispatch-receipt
  transition seam.
- `lib/tightbeam/schema.ex` — recognize the legacy, fresh-v2, and exact fenced-upgrade shape states;
  install and validate the additive rollback fence before intake; constrain the rearm attempt and
  dispatch phases, current-attempt key, and receipt idempotency key.
- `lib/tightbeam/placement.ex` — materialize versioned markers, enforce non-symlink roots, and
  prepare/commit credential rotation during relocation.
- `lib/tightbeam/gateway.ex` — activate spawn credentials only after marker materialization;
  rotate different-root relocation credentials at one commit seam; pass the anchor into
  `session/new`, `session/load`, and `session/fork`; route rearm to the current Adapter checkout
  without inventing a Gateway process identity.
- `lib/tightbeam/acp/adapter.ex` — carry the session map and anchor through source-baseline
  `session/new`, `session/load`, and `session/fork` metadata; map every returned value into the
  closed JSON-safe failure union before any recovery or event-log seam receives it; retain one
  in-flight or completed rearm result per attempt-and-retry key independently of a lane.
- `lib/tightbeam/adapter_coordinator.ex` — expose the current source-grounded adapter key, PID, and
  generation to the rearm seam; preserve its existing monitor, `DOWN`, generation-bump, backoff,
  and temporary-worker replacement lifecycle.
- `lib/tightbeam/harness.ex` — define the session-config contract that accepts the anchor.
- `lib/tightbeam/harness/support.ex` — reserve the four session-anchor names from host and harness
  environment overlays.
- `lib/tightbeam/harness/codex.ex` — gated by OQ-1; use only the exact reviewed carrier mapping.
- `lib/tightbeam/harness/claude.ex` — gated by OQ-1; use only the exact reviewed carrier mapping.
- `lib/tightbeam/wire/router.ex` — compare request binding claims with the token-selected active
  binding before identity resolution.
- `lib/tightbeam/event_log.ex` — carry the existing event-log projection for binding lifecycle and
  refusal events; provide the exact recursive redaction seam over the normalized JSON-safe union;
  do not log token bytes or raw absolute roots.
- `lib/tightbeam/readiness.ex` — include migration terminal state in global intake readiness and
  its operator-facing summary.
- `lib/tightbeam/rails.ex` — describe the observation hook's inherited session anchor instead of a
  cwd-derived marker.
- `lib/tightbeam/session_lane.ex` — represent guarded, pending, acknowledged, and released turn
  exclusion; restore, retry, and release it at the lane-owned claim seam.

Test seams:

- `cli/src/dispatch.rs`
- `test/cli_integration_test.exs`
- `test/placement_test.exs`
- `test/org_test.exs`
- `test/schema_shape_test.exs`
- `test/gateway_test.exs`
- `test/router_test.exs`
- `test/acp_adapter_test.exs`
- `test/adapter_coordinator_test.exs`
- `test/harness_seam_test.exs`
- `test/adapter_patch_mode_test.exs`
- `test/readiness_test.exs`
- `test/support/test_case.ex`
- `test/lane_test.exs`

Documentation and packaging seams:

- CLI help generated from `cli/src/args.rs`
- `README.md`, `priv/guidance/operating-manual.md`, and `docs/INTER-NODE-COMMS.md` sections that
  describe session-implied identity
- `docs/RELEASE_TRAIN.md` rollback section, which must direct a migrated installation to forward
  repair with a current release
- `packaging/assemble.sh` for the repository's documentation/package consistency gate

An implementation can change a file outside this list only after the spec writer amends
`specs/tightbeam/spawned-session-identity-isolation.md`, clears independent review, and installs the
amended bytes plus exact SHA-256 through the canonical installation seam.

## Load-bearing verification still required

This recon did not execute either vendor adapter because the assignment forbids live-session
reproduction. Before vendor-harness implementation can be accepted, the isolated fixture must
install and verify the exact package integrity and vendor binary pins recorded above, then record
the resolved adapter entry points and package bundle SHA-256 values. It must map source-baseline `session/new`,
`session/load`, and `session/fork` to exact vendor request fields, prove that `session/load` reaches
the persisted-session re-entry path, prove that tool subprocesses receive the four anchor values,
and prove that concurrent sessions do not observe each other's values. It must not claim or test a
source-baseline `session/resume` operation. The canonical spec marks this as blocking question
`OQ-1`.
