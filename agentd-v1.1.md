# agentd v1.1 — harness-reported activity and reversible user integrations

Status: READY FOR INDEPENDENT RE-REVIEW

Date: 2026-08-26 PT

Work item: `wi_1ae31ec0-e490-4a00-8c41-971912753897`

Producer assignment: `asg_0e1e256e-a1d5-40e5-8bcb-95e327d5fead`

Canonical product repository: `https://github.com/clickety-clacks/agentd`

Authority and evidence:

- Owner Spirit gate: `att_e27a7ee6-63b6-4346-b293-15c204d58542`.
- The canonical spec home is `https://github.com/clickety-clacks/tightbeam-specs`.
  The complete Agentd v1.1 canonical set is the repository-root paths
  `/agentd-v1.md` and `/agentd-v1.1.md` at one pushed commit. A checkout or artifact
  pointer is evidence of that set, not a second spec home.
- This amendment supersedes `agentd-v1.md` for an Agentd v1.1 build. The pinned base
  file has SHA-256
  `03445f45652b9e517a3fc1f158510ee053e66454124480fa0202ed879af68248`.
- Each v1 clause remains governing unless this amendment changes it explicitly.
- Primary local evidence on Gibson identified Claude Code `2.1.247` and Codex CLI
  `0.149.1`.
- The installed Codex binary reports `hooks` as a stable, enabled feature. The matching
  official source tag is `rust-v0.149.1` at commit
  `ff29a44391deccde0aba0f8390337d7f3c319ea4`.
- Codex `0.149.1` loads user hook declarations from `$CODEX_HOME/hooks.json`. It stores
  per-hook `trusted_hash` values under `hooks.state` in `$CODEX_HOME/config.toml`.
- The matching source evidence is
  `codex-rs/config/src/hook_config.rs` for the JSON shape and event set,
  `codex-rs/hooks/src/engine/discovery.rs` for source paths, positional keys, hashes,
  and runnable trust states, and `codex-rs/tui/src/startup_hooks_review.rs` plus
  `codex-rs/tui/src/hooks_rpc.rs` for review and persisted trust writes.
- An independent spec review must clear one exact v1.1 content hash before
  implementation starts.

## Goal

G1. Agentd accepts `needs_attention` as an explicit hook activity claim through the
wire protocol, snapshot, and CLI surfaces that already carry `active` and `idle`.

G2. A local Linux user can install Claude Code or Codex activity hooks that report
harness events to Agentd. Agentd uses no terminal text, screen scraping, model call, or
behavioral inference to produce those claims.

G3. The integration commands add and remove only Agentd-owned hook declarations. They
preserve unrelated user settings, unrelated hooks, and unrelated Codex trust state.

G4. A hook invocation updates the one roster record whose process identity Agentd
already exposes, including when the hook's nearest harness ancestor is a nested helper
that the v1 scanner collapses under another same-harness agent root.

G5. The Codex integration conforms to the user hook schema and persisted-trust flow in
the installed Codex CLI `0.149.1`. Installation does not grant trust or bypass Codex's
trust check.

G6. The v1.1 acceptance run proves the installed hooks against real Claude Code and
Codex processes on Linux and retains the full v1 acceptance contract.

## Non-Goals

- Replacing procfs as the authority for process existence, process identity, harness
  classification, or roster membership.
- Claiming that `active`, `idle`, or `needs_attention` proves what a model or person is
  doing now. Each value remains the latest accepted hook claim with a server acceptance
  time.
- Inferring activity from terminal contents, process CPU, output rate, elapsed time,
  files, network traffic, or Linux process state.
- Adding activity expiry, freshness thresholds, retries, a delivery queue, history,
  replay, or persistence across daemon restarts.
- Installing project-scoped hooks, managed hooks, plugins, MCP hooks, prompt hooks, or
  agent hooks.
- Installing Codex `PostToolUse`, `PreCompact`, `PostCompact`, `SessionStart`,
  `SessionEnd`, `SubagentStart`, or `SubagentStop` handlers. Version evidence records
  those supported events; the MVP does not need them to express its three activity
  claims.
- Automatically accepting a permission prompt or changing a harness permission mode.
- Automatically trusting Codex hooks, writing a fabricated Codex trust hash, or passing
  `--dangerously-bypass-hook-trust`.
- Pruning orphaned Codex `hooks.state` members whose positional key no longer identifies
  a current Agentd-owned handler after an external reorder or edit.
- Supporting a Codex hook schema other than the verified `0.149.1` user schema in this
  MVP.
- Adding a generic harness integration framework.
- Changing the v1 Linux-only, local-user, Unix-socket, systemd-user-service, privacy,
  or in-memory boundaries.
- Byte-for-byte preservation of JSON whitespace. Preservation means that unrelated JSON
  values and array order remain semantically equal.
- Restoring pre-install absence of a user hook file or deleting an empty root `hooks`
  object. Receipt-free uninstall preserves that residual structure so it cannot delete
  indistinguishable pre-existing empty configuration.
- Moving or renaming the canonical product repository again. The v1.1 product repository
  is `clickety-clacks/agentd`; `leftspin/agentd` is not a canonical reference.

## Terms

### Base contract and amendment

The **base contract** is the pinned `agentd-v1.md` named in the preamble. This file is
the **v1.1 amendment**. A v1.1 implementation satisfies both documents, with this file
taking precedence only where it explicitly changes the base contract.

### Activity claim

The base term **activity claim** now has the closed value set `active | idle |
needs_attention | unknown`.

`needs_attention` means that an installed hook reported an event whose fixed mapping in
this amendment says the harness is waiting for user attention. Like `active` and
`idle`, it is a claim about the latest accepted event. It is not proof that the need
still exists.

### User hook configuration

The **Claude user configuration directory** is `$CLAUDE_CONFIG_DIR` when that variable
contains an absolute path. It is `$HOME/.claude` when the variable is unset. A set
relative value is invalid. Its user settings file is `settings.json` under that
directory.

The **Codex user configuration directory** is `$CODEX_HOME` when that variable contains
an absolute path. It is `$HOME/.codex` when the variable is unset. A set relative value
is invalid. Its user hook file is `hooks.json` and its user configuration and hook-trust
file is `config.toml` under that directory.

The integration commands modify no project `.claude` or `.codex` directory.

### Configuration baseline and conflict

A **configuration baseline** records whether each target path exists and, when it
exists, its exact bytes, mode, and owner after validation. A **configuration conflict**
occurs when a target's existence, exact bytes, mode, or owner differ from that baseline
before its conditional replacement commits.

Each harness configuration directory is also the lock identity for Agentd integration
commands. One command holds a non-blocking exclusive advisory lock on an open file
descriptor for that directory from baseline read through its last replacement. Another
Agentd integration command for that directory cannot enter the mutation interval at the
same time.

### Agentd-owned hook declaration

An **Agentd-owned hook declaration** is one command handler whose parsed command line
has this closed form:

```text
<absolute-agentd-path> hook --integration agentd-v1.1 --harness <claude|codex> --event <event>
```

The installer resolves `<absolute-agentd-path>` from its own executable. The
`--integration agentd-v1.1` marker names Agentd as the principal. The closed event names
the cause. The installer encodes the absolute path as one POSIX shell word. Ownership
inspection tokenizes POSIX shell words without executing them and accepts exactly the
eight words shown above; a command with a control operator, redirection, assignment, or
expansion is unrelated. The marker is reserved for this integration. An entry that only
contains the word `agentd`, has an event outside I3, has extra arguments, or omits this
marker is unrelated. The absolute executable path is not ownership evidence; this lets
uninstall remove an entry after the Agentd binary moves.

### Hook process, harness anchor, and mapped agent root

The **hook process** is the `agentd hook` process started by a harness command hook.

The **harness anchor** is the nearest validated local harness candidate for the declared
harness in the hook process's observed ancestor chain. The walk can pass through shell,
Node, or other non-harness processes.

The **mapped agent root** is the highest validated local candidate for the same harness
in the anchor's resolved ancestor chain. This is the same same-harness collapsing rule
that the base contract uses for roster agent roots. A candidate for a different harness
is not a target and does not stop the ancestor walk.

### Unrelated configuration

**Unrelated configuration** is each value, object member, array element, hook handler,
and Codex hook-state entry that is not an Agentd-owned hook declaration or the persisted
trust state for one such declaration.

### Codex hook trust

For Codex `0.149.1`, an unmanaged command hook has one positional key derived from its
absolute source path, event name, matcher-group index, and handler index. Codex hashes
the normalized hook definition. It classifies the hook as:

- `untrusted` when the user configuration contains no trusted hash for the key;
- `trusted` when the persisted hash equals the current hash;
- `modified` when the persisted and current hashes differ.

Codex runs an unmanaged hook only when it is enabled and `trusted`, unless its caller
uses the dangerous per-invocation bypass. The interactive startup review offers review,
trust-and-continue, or continue-without-trusting. Trusting writes the current hash to
`hooks.state` in the user `config.toml`.

### Installed-version evidence

**Installed-version evidence** is a retained report from the target host that names the
resolved executable, `codex --version`, `codex features list`, the exact user hook path,
the hook event names returned by the matching source or app-server schema, and the
persisted trust transition observed through `hooks/list` plus `config.toml`.

## Assumptions

- The base contract's assumptions remain true.
- Claude Code `2.1.247` reads user command hooks from the `hooks` object in the Claude
  user `settings.json`.
- Claude Code `2.1.247` emits `UserPromptSubmit`, `PreToolUse`, `Stop`, and
  `Notification` events to configured command hooks.
- Codex CLI `0.149.1` reads the JSON shape shown in Architecture C from the Codex user
  `hooks.json`.
- Codex CLI `0.149.1` exposes these 11 command-hook event names:
  `PreToolUse`, `PermissionRequest`, `PostToolUse`, `PreCompact`, `PostCompact`,
  `SessionStart`, `SessionEnd`, `UserPromptSubmit`, `SubagentStart`, `SubagentStop`, and
  `Stop`.
- Codex CLI `0.149.1` enables its stable `hooks` feature without a user
  `features.hooks` override.
- The user configuration directory for an integration exists and belongs to the local
  user before installation starts.
- A harness starts a command hook as a descendant of the harness process that emitted
  the event. The hook process can observe that ancestry through procfs.
- The hook payload can contain prompts, paths, tool inputs, and other private data.
  Agentd does not need any payload field to apply the fixed event mapping.
- A same-directory temporary file can be atomically renamed over each user configuration
  file on the target filesystem.

## Invariants

### I1 — The v1 authority remains intact

I1.1. The v1.1 implementation satisfies each base invariant except the closed activity
value lists that I2 extends.

I1.2. Procfs remains the only authority that creates an agent record, proves presence,
proves absence, assigns a process identity, classifies a harness, and selects roster
agent roots.

I1.3. A hook request enriches one present exact identity. It cannot create a record,
retain an absent record, change presence, change cwd, or change harness.

I1.4. The base observe-then-commit seam remains the sole mutation seam for roster and
activity state.

I1.5. A daemon restart rebuilds the procfs roster and initializes each activity claim to
`unknown`, including when integrations remain installed.

### I2 — `needs_attention` extends each activity surface

I2.1. The wire activity request in base I5.5 accepts `state="needs_attention"` in
addition to `active` and `idle`. Its request fields and identity validation do not
change.

I2.2. The activity handler in base I5.6 accepts exactly `active | idle |
needs_attention` for a present exact process identity.

I2.3. An agent object's `activity.state` in base I6 is exactly `active | idle |
needs_attention | unknown`.

I2.4. `agentd activity --pid <positive-integer> --state` accepts exactly `active`,
`idle`, or `needs_attention`.

I2.5. Human-readable `agentd list` and `agentd watch` print `needs_attention` without
abbreviation when the snapshot contains that value.

I2.6. An accepted `needs_attention` change uses `activity.source=hook`, samples the
server acceptance time, follows the base idempotent commit rule, and produces
`reason=activity_changed` when it changes the snapshot.

I2.7. Agentd derives no `needs_attention` claim from elapsed time or another activity
value. Only an explicit activity request can set it.

### I3 — Hook commands report fixed event mappings

I3.1. The Claude integration installs exactly these mappings:

| Claude event | Activity claim |
| --- | --- |
| `UserPromptSubmit` | `active` |
| `PreToolUse` | `active` |
| `Stop` | `idle` |
| `Notification` | `needs_attention` |

I3.2. The Codex `0.149.1` integration installs exactly these mappings:

| Codex event | Activity claim |
| --- | --- |
| `UserPromptSubmit` | `active` |
| `PreToolUse` | `active` |
| `PermissionRequest` | `needs_attention` |
| `Stop` | `idle` |

I3.3. Each installed handler is synchronous. The harness waits for one handler to
finish before it advances past that event. The handler configuration does not set
Codex `async=true`.

I3.4. `agentd hook` accepts only the harness-and-event pairs in I3.1 and I3.2. It derives
the activity claim from that table. Its CLI exposes no state argument, so a configured
event cannot name a conflicting state. Another pair is a usage failure: it writes
`agentd hook: invalid_hook_event` to stderr, opens no daemon socket, and exits 1.

I3.5. `agentd hook` drains its standard input without logging, storing, parsing, or
sending the payload. It sends no prompt, transcript, tool input, cwd, environment value,
session identifier, or model response to the daemon.

I3.6. `agentd hook` enforces one 500 ms total deadline across input draining, procfs
resolution, socket connect, request write, and acknowledgement read. An operational
failure writes exactly `agentd hook: <code>` to stderr and exits 0. `<code>` is one of
`runtime_directory_unavailable`, `socket_unavailable`, `protocol_error`,
`ancestry_unresolved`, `process_identity_changed`, `unknown_agent`, or
`deadline_exceeded`. The command completes before the one-second harness timeout, so it
cannot block or fail the harness operation that emitted the event.

I3.7. A successful hook update exits 0 and writes nothing to stdout or stderr.

### I4 — Hook ancestry maps to the existing collapsed root

I4.1. `agentd hook` reads its own parent process ID and walks the observed ancestor
chain with the base v1 procfs parsing, local-UID, harness-name, two-stat-read, and visited
PID rules.

I4.2. The resolver selects the nearest validated candidate for the declared harness as
the harness anchor. A chain with no such candidate is unresolved.

I4.3. From the anchor, the resolver selects the highest validated local candidate for
the same harness in the resolved chain as the mapped agent root. It continues through
non-harness processes and candidates for a different harness. A different-harness
candidate cannot become the mapped root.

I4.4. The resolver re-reads the mapped root's stat record. It sends the ordinary v1
activity request only when both reads return the same positive start time and the same
harness classification.

I4.5. The activity request contains the mapped root's exact `{pid,startTimeTicks}`
identity. The wire protocol gains no PID-only activity selector and no separate
hook-activity operation.

I4.6. The daemon applies the request only when that exact identity is present at the
base I4.12 commit operation. A mapping race or roster mismatch returns `unknown_agent`
and changes no snapshot.

I4.7. A nested same-harness hook maps to the one root record that the base scanner
already exposes. It does not add a record for the nested process.

I4.8. A Codex hook inside a Claude process tree maps to the highest validated Codex
candidate in the full resolved chain, including a Codex ancestor above the Claude
candidate. A Claude hook inside a Codex process tree follows the corresponding Claude
rule. A different-harness candidate is not changed by the hook.

### I5 — Claude integration owns only its declarations

I5.1. The CLI exposes `agentd integrate install claude` and
`agentd integrate uninstall claude`.

I5.2. Install targets only the Claude user `settings.json`. It creates that file as a
JSON object when the configuration directory exists and the file does not.

I5.3. Each mapping in I3.1 adds one matcher group under `hooks.<event>`. The group has
no matcher and contains one command handler with the Agentd-owned command from Terms
and a one-second harness timeout.

I5.4. Install replaces an Agentd-owned entry that names an old absolute Agentd path with
the canonical entry for the installer's current absolute path. It changes no unrelated
entry.

I5.5. Install appends each missing Agentd group after existing groups for that event.
It preserves the relative order and values of existing groups and handlers.

I5.6. A second install against the installed result changes no file bytes and adds no
handler.

I5.7. Uninstall removes each exact Agentd-owned Claude handler regardless of the
absolute executable path it names. If its matcher group then
contains no handler, uninstall removes that group. If its event array then contains no
group, uninstall removes that event member.

I5.8. Uninstall preserves the root `hooks` object and Claude user `settings.json`,
including when install created them and the resulting `hooks` object is empty.

I5.9. Uninstall leaves a command with an unrecognized argument set in place and reports
its path and event as not removed. It does not treat a substring or executable basename
as ownership proof.

I5.10. A second uninstall changes no file bytes and exits 0.

### I6 — Codex integration preserves the native trust boundary

I6.1. The CLI exposes `agentd integrate install codex` and
`agentd integrate uninstall codex`.

I6.2. Before it writes, install resolves `codex`, runs `codex --version`, and accepts
exactly `codex-cli 0.149.1` for this MVP. Another version returns
`unsupported_codex_hooks` and changes no file.

I6.3. Install targets only the Codex user `hooks.json`. It creates that file with a root
JSON object and a `hooks` object when the configuration directory exists and the file
does not.

I6.4. Each mapping in I3.2 adds one group under `hooks.<event>`. The group has no matcher
and contains one command handler with `type="command"`, the Agentd-owned command,
`timeout=1`, and `async=false`.

I6.5. Install replaces an Agentd-owned entry that names an old absolute Agentd path with
the canonical entry for the installer's current absolute path. Codex classifies the
changed definition as `modified` until the user trusts its new current hash.

I6.6. Install appends each missing Agentd group after existing groups. It preserves the
relative order and values of existing hook groups and handlers. Therefore installing
or reinstalling Agentd does not change the positional keys of preceding user hooks.

I6.7. Install does not write `hooks.state`, a `trusted_hash`, a hook feature flag, or a
trust-bypass option. Its success output says that Codex must review new or changed hooks
before Codex runs them.

I6.8. On the next interactive Codex startup without the bypass option, Codex presents
each new Agentd handler as `untrusted`. Choosing continue-without-trusting leaves it
non-runnable. Choosing trust persists Codex's current hash under that handler's
`hooks.state` key and makes that exact definition runnable.

I6.9. A changed Agentd handler becomes `modified` and does not run until Codex persists
the new current hash. Agentd does not compute, copy, or fabricate that hash.

I6.10. A second install against unchanged canonical Agentd entries changes no file bytes,
keeps their positional keys stable, and preserves their Codex trust status.

I6.11. Before it removes a handler, uninstall derives that handler's current Codex
`0.149.1` positional key from the absolute `hooks.json` path, snake-case event label,
matcher-group index, and handler index. It removes the `hooks.state` member for that
exact key. It preserves unrelated hook-state members and each other `config.toml` value.

I6.12. If an Agentd command has changed so ownership is not exact, uninstall leaves the
handler and its trust state in place and reports them as not removed.

I6.13. Uninstall applies the verified Codex `0.149.1` positional-key rule to declared
Agentd handlers without requiring the currently resolved Codex executable to remain at
version `0.149.1`. A later Codex update does not block removal of the installed
declarations or their current exact trust members.

I6.14. Uninstall removes an Agentd-owned handler regardless of its absolute executable
path. It removes an empty Agentd matcher group and event member under I5.7.

I6.15. Uninstall preserves the root `hooks` object and Codex user `hooks.json`, including
when install created them and the resulting `hooks` object is empty.

I6.16. A second uninstall changes no file bytes and exits 0.

### I7 — Configuration changes fail closed and replace atomically

I7.1. Before install or uninstall writes a path, it reads and validates each target
file it must change. A malformed JSON document, non-object root, non-object `hooks`
member, non-array target event, non-object `config.toml` hooks state, unsupported Codex
version during install, unresolved executable path, or set relative harness
configuration directory returns one named error and changes no path.

I7.2. Before it reads a configuration baseline, the command acquires the exclusive lock
for that harness configuration directory. If another Agentd integration command holds
the lock, it returns `configuration_busy` and changes no target path.

I7.3. The command constructs each complete replacement privately. Before it commits its
first replacement, it verifies that each target still equals its configuration
baseline. A changed target returns `configuration_changed`, preserves the changed
target, and commits no replacement.

I7.4. After the preflight verification succeeds, the command writes each same-directory
temporary file, applies the target's baseline mode and ownership when the target
exists, and flushes the file. Immediately before each rename, the command conditionally
verifies that target against its baseline and atomically renames only on equality. That
verification and rename form one guarded mutation step. A later conflict returns
`configuration_changed`, preserves that target, and retains any earlier replacement
per I7.9.

I7.5. The command creates a new configuration file with mode `0600`.

I7.6. Install and uninstall preserve each unrelated configuration value and the relative
order of unrelated array elements. A Codex trust edit preserves the bytes outside the
removed `hooks.state` members, including comments.

I7.7. Install and uninstall write no backup, receipt, cache, or integration registry.
The closed command marker makes ownership detectable without a second source of truth.

I7.8. Each command prints one result line that names the harness, action, changed or
unchanged result, and each target path. A Codex install result also names the pending
trust action. Usage or mutation failure exits 1 and writes one error line to stderr.
Success exits 0.

I7.9. Codex uninstall atomically removes owned trust members before it atomically removes
the corresponding hook declarations. If the second replacement fails, the declarations
remain installed but non-runnable until the user trusts them again. A retry completes
the removal.

## Architecture

### A. One event-to-activity adapter

The `agentd hook` CLI mode is the only new runtime adapter. It accepts one closed
harness-and-event pair and derives the fixed state from I3. The adapter discards the
hook payload, resolves the existing root identity through procfs, and sends the base
wire activity request. The daemon retains one activity mutation seam and one activity
source. Omitting a state argument makes a contradictory event-to-state pair
unrepresentable at this seam.

This adds a small adapter because deleting hook instrumentation would fail G2, and
accepting hookless `unknown` would fail the requested status pane. A second daemon API,
PID-only selector, durable queue, or state inference loses because the base exact-
identity request already serves the need.

### B. One shared root resolver

The implementation uses the base parent-chain parser and validation rules for both the
scanner and hook mapping. The hook resolver starts from the hook process instead of the
global PID table, then produces the same `{pid,startTimeTicks}` root identity. There is
no second definition of an agent root.

The pattern is **same-harness ancestor collapse**. It applies to roster scanning and
hook-origin mapping. A different-harness candidate does not qualify as the target and
does not stop the walk.

Canonical example:

```text
claude root {pid=410,start=100}
  -> shell pid 420
    -> nested claude {pid=430,start=110}
      -> shell pid 440
        -> agentd hook pid 450
```

The hook anchor is PID 430. The mapped agent root is `{410,100}`. The daemon updates the
existing PID 410 roster record and emits no PID 430 record.

### C. Native user hook shapes

The Claude integration merges this native shape for each I3.1 event:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/absolute/path/agentd hook --integration agentd-v1.1 --harness claude --event UserPromptSubmit",
            "timeout": 1
          }
        ]
      }
    ]
  }
}
```

The Codex integration merges this `0.149.1` user shape for each I3.2 event:

```json
{
  "hooks": {
    "PermissionRequest": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/absolute/path/agentd hook --integration agentd-v1.1 --harness codex --event PermissionRequest",
            "timeout": 1,
            "async": false
          }
        ]
      }
    ]
  }
}
```

The examples show the Agentd-owned group only. A real file can contain unrelated root
members, events, matcher groups, and handlers before or after it.

### D. Codex owns trust decisions

Install writes hook declarations, then stops. Codex discovers the declarations,
calculates their normalized hashes, asks the user, and persists the decision. Agentd
reads enough hook metadata during uninstall to remove trust state only for the exact
entries it owns. Agentd does not decide that executable code is safe on the user's
behalf.

### E. Configuration merge and removal

Each harness has one schema-aware JSON merge path. It validates first, identifies owned
handlers by parsed exact command, appends missing entries, removes exact owned entries,
and writes a complete value by atomic replacement. Codex uninstall also performs a
field-scoped TOML edit for the owned trust keys. The commands do not normalize or
replace unrelated hooks.

Codex uninstall has two files because Codex owns trust separately from hook
declarations. Deleting trust cleanup would leave integration-owned state behind.
Accepting that residue would violate reversible removal. The implementation therefore
uses I7.9's trust-first order; it adds no transaction journal or recovery service.
Orphaned trust members from an earlier external reorder are accepted as the named
Non-Goal because no current declaration identifies them, while pruning positional keys
without that evidence could delete unrelated trust.

The configuration mutation pattern is **conflict-detecting merge**. The directory lock
makes two Agentd integration mutations mutually exclusive. A preflight comparison
prevents mutation when a baseline is already stale. The conditional comparison at each
rename protects a later target change during a multi-file operation. Conflict exits are
named outcomes; the user can retry against the new bytes.

The operating pattern taught to Tightbeam agents is **none**. This product amendment
does not require a Tightbeam manual or guidance change.

## Acceptance

Each case names the goals and invariants it verifies. Captured hook fixtures come from
real installed harness responses, not hand-written ideal payloads.

### A1 — `needs_attention` wire, snapshot, and CLI (G1; I1, I2)

**Given** a present exact identity with activity `unknown`, **when** a client sends the
base activity request with `state="needs_attention"`, **then** the daemon acknowledges
the new revision and the next snapshot reports `activity.state=needs_attention`,
`activity.source=hook`, and a non-null server acceptance time.

**Given** a subscriber and that accepted change, **when** it reads the next frame,
**then** it receives a complete snapshot with `reason=activity_changed`.

**Given** the same identity and a fixed clock, **when** the same request arrives again,
**then** the daemon retains its revision and emits no subscriber frame under the base
idempotence rule.

**Given** that snapshot, **when** the user runs human-readable `agentd list` and
`agentd watch`, **then** each prints `needs_attention`. **When** the user runs
`agentd list --json` or `agentd watch --json`, **then** the JSON frame carries the same
value unchanged.

**Given** a present PID, **when** the user runs `agentd activity --pid <pid> --state
needs_attention`, **then** the command exits 0 and the next snapshot contains that
claim. An activity value outside the amended closed set returns `invalid_activity`.

### A2 — Real Claude event mapping (G2, G6; I3, I4, I5)

**Given** Claude Code `2.1.247`, a dedicated real Claude process, a running Agentd
daemon, and `agentd integrate install claude`, **when** real harness actions emit
`UserPromptSubmit`, `PreToolUse`, `Notification`, and `Stop`, **then** retained hook
captures prove those exact event names and the Agentd subscription reports, in event
order, `active`, `active`, `needs_attention`, and `idle` for the one Claude root.

**Given** those captures, **when** automated tests replay each payload through the
installed command entry, **then** the hook drains the payload and sends only the fixed
state and mapped process identity. No sentinel prompt, tool input, transcript path, or
environment value appears in the socket capture, daemon output, or hook diagnostics.

### A3 — Installed Codex schema and trust flow (G2, G5, G6; I3, I6)

**Given** the resolved installed Codex executable, **when** the evidence capture runs
`codex --version` and `codex features list`, **then** it records `codex-cli 0.149.1` and
an enabled stable `hooks` feature.

**Given** an isolated Codex user directory and unrelated valid user hooks, **when** the
user runs `agentd integrate install codex`, **then** `$CODEX_HOME/hooks.json` contains
the four exact I3.2 Agentd groups in the native Architecture C shape after the unrelated
groups. The install changes no feature or trust value in `config.toml`.

**Given** the new hooks and raw Codex `0.149.1` without the trust-bypass option, **when**
the Codex `hooks/list` surface evaluates them, **then** it returns their source as the
user `hooks.json`, their status as `untrusted`, and no Agentd hook executes.

**When** an interactive user chooses continue-without-trusting, **then** the handlers
remain non-runnable. **When** the user later approves the Agentd hooks, **then** Codex
writes each current hash under its exact `hooks.state` key, `hooks/list` reports
`trusted`, and real `UserPromptSubmit`, `PermissionRequest`, and `Stop` events produce
`active`, `needs_attention`, and `idle` claims for the Codex root.

**Given** one trusted Agentd entry whose command changes, **when** Codex reloads hooks,
**then** `hooks/list` reports `modified` and that handler does not execute until the
user approves its new hash.

**Given** unchanged trusted Agentd entries, **when** Codex install runs again, **then**
it changes no file bytes and `hooks/list` continues to report those entries as
`trusted`.

The evidence report retains the installed executable path, package version, official
source tag and commit, source hook path, event list, hook keys, hashes, trust statuses,
and the field-scoped `config.toml` changes. It does not retain credentials or hook
payload contents.

### A4 — Idempotent merge and reversible removal (G3; I5, I6, I7)

**Given** captured valid Claude `settings.json`, Codex `hooks.json`, and Codex
`config.toml` fixtures with unrelated root values, multiple third-party matcher groups,
multiple handlers in one group, and unrelated hook trust, **when** each install runs
twice, **then** the second run changes no bytes and the parsed files contain one copy of
each Agentd-owned handler.

**Given** Codex has approved its installed Agentd handlers, **when** each harness
uninstall runs once, **then** no exact Agentd-owned handler remains, the Codex trust
members for those handlers are absent, and each unrelated parsed value and array order
equals the pre-install fixture. The comments and bytes outside the removed owned
`hooks.state` members equal the pre-uninstall Codex file. **When** uninstall runs again,
**then** it changes no bytes and exits 0.

**Given** an unrelated command that contains the word `agentd`, an Agentd executable
basename with different arguments, and a command with the Agentd marker plus an event
outside I3, **when** uninstall runs, **then** it removes none of them and names the
owned-looking entries as not removed.

**Given** an exact Agentd-owned entry whose absolute executable path differs from the
current binary, **when** install runs, **then** it replaces that entry with the current
canonical path. **When** uninstall runs instead, **then** it removes the entry despite
the old path.

**Given** an Agentd executable path that needs POSIX shell quoting, **when** install
runs, **then** the stored command parses to that path as its first word and the seven
fixed argument words in Terms. **When** uninstall reads that command, **then** it
recognizes and removes the exact owned handler without executing the command text.

**Given** malformed JSON, an invalid target member type, malformed target Codex trust
state, or an unresolved Agentd executable, **when** install or uninstall runs, **then**
it exits 1, names the cause and path, and the hash of each target file remains
unchanged.

**Given** an unsupported Codex version, **when** Codex install runs, **then** it returns
`unsupported_codex_hooks` and changes no target file. **When** Codex uninstall instead
finds an exact declaration created for `0.149.1`, **then** it removes that declaration
and its current exact trust member without version-gating the removal.

**Given** the Claude user `settings.json` or Codex user `hooks.json` was absent, or an
existing root object had no `hooks` member, **when** install succeeds and uninstall
later removes its owned handlers, **then** the user file remains, its root object
remains valid, and its root `hooks` object is empty. A file created by install retains
mode `0600`. A second uninstall changes no bytes.

### A5 — Nested hook-parent mapping (G4; I1, I4)

**Given** a captured real-shaped procfs fixture with a local Claude root, a non-harness
wrapper, a nested local Claude candidate, a command shell, and an `agentd hook` child,
**when** the hook reports `needs_attention`, **then** the resolver sends the root's exact
identity and the daemon changes only the existing root record.

**Given** a live equivalent process tree, **when** the nested hook fires, **then**
`agentd list --json` contains one Claude root with the new claim and no nested Claude
record.

**Given** an outer Codex candidate, a nested Claude candidate, and a nested inner Codex
anchor, **when** the inner Codex hook fires, **then** it maps to the outer Codex root and
changes no Claude record.

**Given** a repeated PID, missing parent, UID mismatch, parent change between stat reads,
root start-time change, or exact root missing from the committed roster, **when** the
hook resolves or commits, **then** it changes no snapshot, exits 0 within 750 ms, and
writes one typed diagnostic.

### A6 — Hook failure cannot block the harness (G2; I3.6, I3.7)

**Given** each installed harness configuration and an absent Agentd socket, **when** a
real Claude or Codex event invokes its handler, **then** the handler exits 0 within 750
ms, the harness operation continues, and one diagnostic names the socket failure.

**Given** a running daemon and present mapped identity, **when** the same event fires,
**then** the hook exits 0, writes no output, and the changed claim is observable through
the socket.

**Given** a harness-and-event pair outside I3, **when** `agentd hook` receives it,
**then** it opens no daemon socket, writes `agentd hook: invalid_hook_event`, and exits
1.

### A7 — Conflict-detecting atomic replacement (G3; I7)

**Given** existing user files with mode `0600`, **when** install or uninstall succeeds,
**then** each replaced file retains its mode and owner, parses in its native format, and
contains the complete pre-change unrelated configuration plus the required change.

**Given** a new user hook file, **when** install creates it, **then** its mode is `0600`.

**Given** an injected write, flush, chmod, chown, or rename failure, **when** the command
returns, **then** the original target path contains either the complete old value or the
complete new value. It contains no partial serialization.

**Given** an integration command has read its baseline and an external writer changes a
target's bytes, mode, or owner before the first guarded replacement step, **when** the
command attempts to commit, **then** it returns `configuration_changed`, preserves the
external target, and adds or removes no hook declaration or trust member.

**Given** one Agentd integration command holds the harness configuration-directory
lock, **when** another Agentd integration command targets that directory, **then** the
second command returns `configuration_busy` and changes no target. A retry after lock
release merges against the first command's committed bytes.

**Given** Codex uninstall has removed its owned trust members and an external writer
then changes `hooks.json` before the declaration replacement, **when** the conditional
replacement runs, **then** it returns `configuration_changed`, preserves the external
`hooks.json` bytes, and leaves the Agentd declarations installed but untrusted. A retry
merges against those bytes and completes removal.

### A8 — Base regression and repository gate (G6; I1)

**Given** the v1.1 implementation commit in a clean checkout of
`clickety-clacks/agentd`, **when** the repository runs each base v1 acceptance case and
the documented format, static-analysis, unit, integration, and real-smoke commands,
**then** each command exits 0.

The gate report records the exact product commit, base and amendment hashes, commands,
exit results, installed harness versions, real process identities, hook event captures,
socket path, daemon instance IDs, configuration before-and-after hashes, trust
transitions, and teardown result.

## Open Questions

Blocking questions: none.

Non-blocking questions: none.

The independent spec review can return defects against this amendment. A finding does
not authorize implementation. The producer must amend this canonical file, land the
revision, and present its new content hash for review before a builder reads it.
