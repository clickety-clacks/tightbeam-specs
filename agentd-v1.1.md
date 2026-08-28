# agentd v1.1 — harness-reported activity and reversible user integrations

Status: READY FOR INDEPENDENT RE-REVIEW

Date: 2026-08-26 PT

Work item: `wi_1ae31ec0-e490-4a00-8c41-971912753897`

Producer assignment: `asg_0e1e256e-a1d5-40e5-8bcb-95e327d5fead`

Canonical product repository: `https://github.com/clickety-clacks/agentd`

Authority and evidence:

- Owner Spirit gate: `att_e27a7ee6-63b6-4346-b293-15c204d58542`.
- Release-documentation and already-running-session addendum authority: work item
  `wi_70fd5c90-cd17-46e6-9e3f-b3600a4afef8`, producer assignment
  `asg_4828b4f0-70c9-45b7-b68d-78b53d8dce20`, and Spirit approval
  `att_4fb3ab62-1a8e-429b-b5f6-b188873b317d`.
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
- Exact-revision review `att_1c54c3b1-b403-497d-bae8-3aa16ad9e38f` and report
  `art_bbbb11d8` identified internal harness reload behavior. Owner ruling
  `att_103f5b40-c6d5-4e5d-a409-a467ad45ccf7` excludes internal watchers, RPC reload
  paths, and `/hooks` reload behavior from the supported Agentd v1.1 activation
  contract. The documented and accepted remedy is process restart. Lifecycle ruling
  `att_ef51d940-1a05-4b18-a34f-ddee24b48c1d` requires one fresh independent review of
  the corrected exact revision.
- Successor review `att_09e6937c-8a19-45fe-8415-d9edb9be7298` and report
  `art_9877a0d5` require pre-mutation refusal when Codex declaration removal would shift
  an unrelated positional trust key, plus secure temporary-file creation and explicit
  cleanup outcomes. Review assignment `asg_53cbf6cd-5f27-4fd8-8023-8c0e7423afbd`
  remains open for the corrected exact revision.
- An independent spec review must clear one exact v1.1 content hash before
  implementation starts.

## Goal

G1. Agentd accepts `needs_attention` as an explicit hook activity claim through the
wire protocol, snapshot, and CLI surfaces that already carry `active` and `idle`.

G2. A local Linux user can install Claude Code or Codex activity hooks that report
harness events to Agentd. Agentd uses no terminal text, screen scraping, model call, or
behavioral inference to produce those claims.

G3. Against each successfully validated configuration baseline, the integration
commands change only Agentd-owned hook declarations and their exact Codex trust state.
For an externally quiescent configuration set, they preserve unrelated user settings,
unrelated hooks, and unrelated Codex trust state. When preflight observes an unrelated
concurrent change before any replacement, they preserve it by refusing the operation
with `configuration_changed`.

G4. A hook invocation updates the one roster record whose process identity Agentd
already exposes, including when the hook's nearest harness ancestor is a nested helper
that the v1 scanner collapses under another same-harness agent root.

G5. The Codex integration conforms to the user hook schema and persisted-trust flow in
the installed Codex CLI `0.149.1`. Installation does not grant trust or bypass Codex's
trust check.

G6. The v1.1 acceptance run proves the installed hooks against real Claude Code and
Codex processes on Linux and retains the full v1 acceptance contract.

G7. At the v1.1 release cut, the product README gives a local Linux user one truthful,
end-to-end procedure for installing, activating, verifying, and uninstalling each
implemented Claude and Codex integration, including the already-running-session
boundary.

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
- Migrating, copying, or fabricating trust state for an unrelated Codex hook whose
  positional key would change when an Agentd-owned declaration is removed. Uninstall
  refuses that baseline before mutation instead.
- Pruning orphaned Codex `hooks.state` members whose positional key no longer identifies
  a current Agentd-owned handler after an external reorder or edit.
- Supporting a Codex hook schema other than the verified `0.149.1` user schema in this
  MVP.
- Adding a generic harness integration framework.
- Changing the v1 Linux-only, local-user, Unix-socket, systemd-user-service, privacy,
  or in-memory boundaries.
- Byte-for-byte preservation of JSON whitespace. Preservation means that unrelated JSON
  values and array order remain semantically equal.
- Coordinating with a non-Agentd configuration writer that does not participate in
  Agentd's advisory directory lock, or guaranteeing preservation when such a writer
  changes any target during the command's mutation interval. The supported contract
  requires the complete harness configuration set to remain externally quiescent from
  baseline read through the last replacement; the advisory lock serializes Agentd
  integration commands only. During Codex uninstall, an external `hooks.json` reorder
  after the trust replacement can make an unrelated hook lose trust before the later
  conflict refusal. The command names that partial result and never grants trust; the
  user must review and reapprove any affected hook.
- Restoring pre-install absence of a user hook file or deleting an empty root `hooks`
  object. Receipt-free uninstall preserves that residual structure so it cannot delete
  indistinguishable pre-existing empty configuration.
- Moving or renaming the canonical product repository again. The v1.1 product repository
  is `clickety-clacks/agentd`; `leftspin/agentd` is not a canonical reference.
- Publishing README instructions for an integration command before that command exists
  in the same accepted product release.
- Making hook installation change procfs roster membership or synthesize an activity
  claim for an already-running harness process.
- Treating installation alone as proof that an already-running harness process has
  loaded new or changed hook configuration. Only a later mapped hook event submits
  activity.
- Supporting or documenting a harness-internal watcher, RPC, `/hooks` behavior, signal,
  or flag as an Agentd in-session activation remedy. This amendment makes no claim that
  such internal behavior does not exist; the v1.1 operator contract relies only on a
  replacement harness process.

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

### Configuration baseline, conflict, and quiescence

A **configuration baseline** records whether each target path exists and, when it
exists, its directory-entry type, exact bytes, mode, and owner after validation. An
existing supported target is a regular file reached without following a symlink whose
owner UID equals the invoking local user's effective UID. An existing regular file with
another owner, symlink, directory, FIFO, socket, device, or other non-regular target is
an **unsupported configuration target**. A **configuration conflict** occurs when a
target's existence, directory-entry type, exact bytes, mode, or owner differ from that
baseline when the command compares them.

An **externally quiescent configuration set** is the complete set of target paths for
one integration command when no non-Agentd process changes any target from the first
baseline read through the command's last replacement. For Codex uninstall, the set is
`config.toml` and `hooks.json` together. This definition covers the interval between
their replacements as well as each target's final comparison-to-rename gap. Linux
atomic rename prevents a partial target value; it does not condition a rename on the
target still matching its baseline or make two target replacements one transaction.

Each harness configuration directory is also the lock identity for Agentd integration
commands. One command holds a non-blocking exclusive advisory lock on an open file
descriptor for that directory from baseline read through its last replacement. Another
Agentd integration command for that directory cannot enter the mutation interval at the
same time. A non-Agentd writer need not honor this advisory lock.

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

A **Codex positional trust conflict** exists when simulating removal of every exact
Agentd-owned handler would change the event, matcher-group index, or handler index in
the positional key of any surviving unrelated handler. Agentd does not inspect whether
that unrelated handler is currently trusted; it refuses every baseline with such a
shift rather than mutate or infer unrelated trust state.

### Installed-version evidence

**Installed-version evidence** is a retained report from the target host that names the
resolved executable, `codex --version`, `codex features list`, the exact user hook path,
the hook event names returned by the matching source or app-server schema, and the
persisted trust transition observed through `hooks/list` plus `config.toml`.

### Already-running harness session and activation

An **already-running harness session** is a Claude or Codex agent root whose process
identity exists before its integration install command commits. A tmux pane is only a
carrier for that process; procfs presence, not tmux state, decides whether the session
appears in the Agentd roster.

**Hook activation** is the supported replacement-process startup after installation
when that new process has loaded an Agentd-owned declaration and, for Codex, that exact
current declaration is trusted and runnable. `claude --continue`, `claude --resume`,
and `codex resume` preserve access to their conversations while starting replacement
processes. The next interactive Codex startup presents new or changed hooks for trust
review. The v1.1 procedure does not depend on or document a harness-internal in-session
reload path. Hook activation alone does not set activity; the first later accepted
mapped hook event does.

### v1.1 release cut

The **v1.1 release cut** is the accepted product commit from which the v1.1 release is
built. That commit contains the implemented integration commands and the matching
product README procedure. A pre-release spec or planned command is not an implemented
README surface.

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
- The supported Claude Code `2.1.247` activation procedure starts a replacement process
  after install. It does not depend on a watcher, RPC, `/hooks` behavior, signal, flag,
  or other harness-internal reload path.
- The supported Codex CLI `0.149.1` activation procedure starts the next interactive
  process after install. That startup reviews new or changed unmanaged hooks. The
  procedure does not depend on an in-session reload path.

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

I6.11. Before it removes trust or a declaration, uninstall simulates exact removal of
all Agentd-owned handlers against the validated `hooks.json` baseline. A Codex
positional trust conflict returns `codex_positional_trust_conflict`, exits 1, names the
event plus each affected handler's current and resulting matcher-group and handler
indexes, and changes neither `hooks.json` nor `config.toml`. The error tells the user
that unrelated hooks must precede the Agentd-owned entries before retry and that the
user must reapprove any unrelated hook whose key or definition the user's rearrangement
changes. Agentd does not migrate an unrelated `hooks.state` member.

I6.12. Before it removes a handler, uninstall derives that handler's current Codex
`0.149.1` positional key from the absolute `hooks.json` path, snake-case event label,
matcher-group index, and handler index. With an externally quiescent configuration set,
it removes the `hooks.state` member for that exact key and preserves unrelated
hook-state members and each other `config.toml` value. I7.10 governs an external change
during the two-target mutation interval.

I6.13. If an Agentd command has changed so ownership is not exact, uninstall leaves the
handler and its trust state in place and reports them as not removed.

I6.14. Uninstall applies the verified Codex `0.149.1` positional-key rule to declared
Agentd handlers without requiring the currently resolved Codex executable to remain at
version `0.149.1`. A later Codex update does not block removal of the installed
declarations or their current exact trust members.

I6.15. When I6.11 permits mutation, uninstall removes an Agentd-owned handler regardless
of its absolute executable path. It removes an empty Agentd matcher group and event
member under I5.7.

I6.16. Uninstall preserves the root `hooks` object and Codex user `hooks.json`, including
when install created them and the resulting `hooks` object is empty.

I6.17. A second uninstall changes no file bytes and exits 0.

### I7 — Observed configuration conflicts refuse further mutation; replacement is atomic

I7.1. Before install or uninstall writes a path, it inspects each target with a
no-follow metadata operation. An absent target is valid. An existing target must be a
regular file whose owner UID equals the invoking local user's effective UID. An
existing regular file with another owner, symlink, or any other non-regular type returns
`unsupported_configuration_target`, names the path, observed type, and owner mismatch
when applicable, follows no referent, exits 1, and changes no path. After this type
check, a malformed JSON document, non-object root, non-object `hooks` member, non-array
target event, non-object `config.toml` hooks state, unsupported Codex version during
install, unresolved executable path, or set relative harness configuration directory
returns one named error and changes no path. A multi-target command completes all type,
ownership, and content validation before its first replacement.

I7.2. Before it reads a configuration baseline, the command acquires the exclusive lock
for that harness configuration directory. If another Agentd integration command holds
the lock, it returns `configuration_busy` and changes no target path. This advisory
lock does not exclude a non-Agentd writer.

I7.3. The command constructs each complete replacement privately. Before it commits its
first replacement, it verifies that each target still equals its configuration
baseline. A changed target returns `configuration_changed`, preserves the changed
target, and commits no replacement.

I7.4. After the preflight verification succeeds, the command creates each uniquely
named same-directory temporary path with exclusive no-follow creation, mode `0600`, and
owner UID equal to the invoking local user's effective UID. It never opens or truncates
an existing temporary path. It writes and flushes the complete replacement while that
temporary file remains mode `0600`. Immediately before each rename, the command performs
one final no-follow comparison of the target with its baseline. A type change, symlink
substitution, or other observed difference returns
`configuration_changed` when no earlier target was replaced, or
`configuration_changed_after_partial` when an earlier replacement committed. It
preserves the changed target and retains any earlier replacement per I7.10. After
equality is observed, the command atomically renames the mode-`0600` replacement. When
the baseline target existed, it then applies the baseline mode and ownership to the
renamed target; a successful command preserves them. The comparison and rename are not
indivisible against a non-Agentd writer. If such a writer changes the target between
them, the rename can replace that change without detecting it; that schedule is outside
G3's preservation guarantee.

I7.5. The command creates a new configuration file with mode `0600` and owner UID equal
to the invoking local user's effective UID.

I7.6. On every exit before a temporary path's successful rename, the command closes and
unlinks that path before returning. A successful cleanup leaves no temporary entry. If
the unlink itself fails, the command returns `temporary_cleanup_failed` when no target
was replaced or `temporary_cleanup_failed_after_partial` after an earlier replacement,
exits 1, and names the exact residual path. That residue remains an invoking-user-owned
regular file with mode `0600`; the command never leaves a permissively created or
unnamed temporary file.

I7.7. With an externally quiescent configuration set, install and uninstall preserve
each unrelated configuration value and the relative order of unrelated array elements.
A Codex trust edit preserves the bytes outside the removed `hooks.state` members,
including comments. A preflight conflict preserves every target. A later conflict
preserves its changed target but does not roll back an earlier replacement.

I7.8. Install and uninstall write no backup, receipt, cache, or integration registry.
The closed command marker makes ownership detectable without a second source of truth.

I7.9. Each command prints one result line that names the harness, action, changed or
unchanged result, and each target path. A Codex install result also names the pending
trust action. Usage or mutation failure exits 1 and writes one error line to stderr.
Success exits 0.

I7.10. Codex uninstall atomically removes the `hooks.state` members whose configuration-
baseline positional keys identify Agentd-owned declarations before it atomically
removes those declarations. These replacements are not one cross-file transaction. If
the hook-declaration replacement fails without an external `hooks.json` change, the
declarations remain at their baseline positions but non-runnable until the user trusts
them again. If the final `hooks.json` comparison observes an external change after the
trust replacement, the command returns `configuration_changed_after_partial` with
detail `codex_trust_review_required`, preserves the external `hooks.json`, and retains
the earlier trust replacement. An external reorder can therefore leave a now-unrelated
hook without trust as named in Non-Goals. Codex derives every retained declaration's
status from its current key and hash; Agentd grants no trust. A retry merges against
the new bytes and completes declaration removal; the user reapproves any unrelated hook
whose trust was lost.

I7.11. `agentd integrate --help` includes this warning: `Do not edit harness
configuration while an integration command runs; concurrent non-Agentd edits can be
overwritten, and Codex hook trust can be revoked.`

### I8 — Installation preserves roster truth and names the activation boundary

I8.1. An integration install changes only the configuration targets that I5-I7 name.
It does not rescan procfs, add or remove a roster record, or submit an activity request.

I8.2. An already-running Claude or Codex process remains eligible for roster membership
under I1.2. Therefore an existing session carried by tmux appears in the roster when
procfs proves its agent root, even when the process has not activated newly installed
hooks.

I8.3. An already-running Claude Code `2.1.247` process does not begin using a newly
installed or changed Agentd declaration merely because install committed it under the
supported v1.1 contract. The user exits and starts a replacement process with
`claude --continue` or `claude --resume` to preserve access to the conversation and
load the declaration. Agentd does not document or rely on harness-internal in-session
reload behavior.

I8.4. An already-running interactive Codex `0.149.1` process does not trust a newly
installed or changed Agentd declaration merely because install committed it under the
supported v1.1 contract. The user exits and runs `codex resume` to preserve access to
the conversation. That next interactive startup presents the new or changed hooks for
review under I6.8. Continue-without-trusting leaves them non-runnable; approval persists
each current hash and makes that definition runnable. Agentd does not document or rely
on a harness-internal in-session reload path.

I8.5. Install preserves the activity value of every already-running exact identity at
the instant the command returns. If that value is `unknown`, it remains `unknown` until
the daemon accepts a mapped hook event; install never converts the absence of an event
into `active`, `idle`, or `needs_attention`. A process that loaded the same unchanged
Agentd declarations before an Agentd daemon restart or idempotent reinstall can submit
its next mapped event without another harness reload or restart. A process that has not
loaded a new or changed declaration can submit from that declaration only after the
I8.3 or I8.4 replacement-process startup. A replacement identity enters the procfs
roster at `unknown` and does not inherit the old identity's claim.

I8.6. The one successful install result line required by I7.9 includes harness-specific
guidance for already-running sessions. Every line says procfs keeps the existing process
in the roster, install does not change its current activity, and the next accepted
mapped hook event changes activity. The Claude line names no in-session activation
action. It names `claude --continue` and
`claude --resume` as the conversation-preserving restart remedies. The Codex line names
`codex resume` as the conversation-preserving restart remedy and says the next
interactive startup presents trust review. The line does not claim that an unchanged
idempotent reinstall deactivates a declaration already loaded by the process.

### I9 — The release README is truthful and complete

I9.1. Before the product commit that implements and accepts the v1.1 integration
commands, the product README contains no instruction or example that tells a user to
run `agentd integrate install` or `agentd integrate uninstall`. The v1.1 release cut
adds the procedure in I9.2-I9.6 in the same release change set as the implemented
commands. A spec, placeholder, or forecast does not satisfy this clause.

I9.2. The v1.1 release README gives separate end-to-end Claude and Codex procedures.
Each procedure names the supported harness version, user configuration target, exact
install command, restart-only activation action, conversation-preserving restart
command, observable verification, exact uninstall command, and successful teardown
check. The Claude procedure names `claude --continue` and `claude --resume`. The Codex
procedure names `codex resume`.

I9.3. The release README reproduces both complete I3 event-to-state tables and defines
`needs_attention` as the latest accepted hook claim that the harness emitted an event
mapped to user attention. It states that the claim does not prove the need still
exists.

I9.4. The Codex procedure states that install supports exactly `codex-cli 0.149.1`,
that another version makes install exit 1 with one stderr line containing
`unsupported_codex_hooks`, and that this refusal changes no target file. It states
that the next interactive Codex startup reviews each new or changed Agentd hook, that
continue-without-trusting leaves it non-runnable, and that trust approval makes only
the approved current definition runnable.

I9.5. The uninstall procedure states the guarantees from I5.7-I5.10, I6.11-I6.17, and
I7.6-I7.10 in operator terms: a successful uninstall removes each exact Agentd-owned
declaration even after the Agentd executable moves; Codex uninstall removes the current
exact owned trust members; each harness preserves unrelated configuration; user hook
files and their root `hooks` objects remain; a repeated uninstall is
byte-idempotent; and a configuration conflict refuses or names a partial Codex trust
removal instead of claiming complete teardown. It states that
`codex_positional_trust_conflict` refuses
before mutation when declaration removal would shift an unrelated hook's key, names the
required user reorder and reapproval boundary, and changes no file. It also states that
pre-rename failure removes secure temporary files and that a cleanup failure names the
exact mode-`0600` residue instead of silently leaving it.

I9.6. Each README command and recovery action names a command or harness surface that
exists in the v1.1 release cut. The README does not advertise a future Agentd command,
an in-session activation remedy, automatic Codex trust, automatic activity on install,
or inferred activity. This restriction does not assert that harness-internal reload
behavior is absent; it keeps unsupported internals out of the Agentd operator contract.

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
replace unrelated hooks present in the validated baseline.

Before Codex uninstall mutates either file, it simulates removal against the baseline.
If any surviving unrelated handler would move to another positional key, the command
returns `codex_positional_trust_conflict` without removing trust or declarations.
Agentd refuses because copying or recomputing an unrelated handler's trust would cross
the native trust boundary. The user can place unrelated handlers before Agentd-owned
entries, reapprove any hook affected by that user edit, and retry.

Codex uninstall has two files because Codex owns trust separately from hook
declarations. Deleting trust cleanup would leave integration-owned state behind.
Accepting that residue would violate reversible removal. The implementation therefore
uses I7.10's trust-first order; it adds no transaction journal or recovery service.
Orphaned trust members from an earlier external reorder are accepted as the named
Non-Goal because no current declaration identifies them, while pruning positional keys
without that evidence could delete unrelated trust.

Atomic replacement uses an exclusive no-follow same-directory temporary file created
as invoking-user-owned mode `0600`. Replacement bytes remain protected by that mode
until rename. Every pre-rename exit unlinks the temporary path; an unlink failure names
the exact secure residue and whether earlier targets committed. This bounds the extra
filesystem effect without a backup, journal, or cleanup service.

The configuration mutation pattern is **observed-conflict merge**. The directory lock
makes two Agentd integration mutations mutually exclusive. A preflight comparison
prevents mutation when a baseline is already stale. The comparison immediately before
each rename catches a target change visible at that point during a multi-file operation.
Conflict exits are named outcomes; the user can retry against the new bytes. External
quiescence applies to the complete target set for the full mutation interval. The lock
does not coordinate an editor, harness, or other non-Agentd writer; comparison plus
rename is not a compare-and-swap; and two renames are not a cross-file transaction.
Users must not edit the target files concurrently with an integration command.

Deleting configuration mutation would fail G2 and the non-concurrent part of G3.
Deleting Codex trust cleanup would fail reversible removal. A new lock protocol cannot
compel existing external writers to participate, and a journal cannot create an atomic
compare-and-replace primitive or cross-file transaction for these files. Those
mechanisms therefore lose to the explicit configuration-set quiescence boundary and
named trust-revocation outcome above.

The operating pattern taught to Tightbeam agents is **none**. This product amendment
does not require a Tightbeam manual or guidance change.

### F. Presence, activation, and claim are separate events

Procfs observation determines whether an already-running harness process appears in
the roster. Integration install changes declarations on disk but submits no activity.
For a process that predates first integration or has not loaded a changed declaration,
the supported activation action is replacement-process startup: `claude --continue`,
`claude --resume`, and `codex resume` preserve access to their conversations. The next
interactive Codex startup performs trust review. A later mapped hook event submits the
next claim.

A process that already loaded unchanged Agentd hooks can report without another harness
restart, including after the Agentd daemon restarts or an idempotent reinstall. The v1.1
operator contract does not rely on or document harness-internal in-session reload
behavior. Keeping presence, disk mutation, supported activation, trust, and claim as
separate events preserves I1.2 and prevents installation from inventing activity.

### G. Release documentation lands with the surface

The product README is the operator procedure under test, but it becomes truthful only
when its commands exist. The v1.1 release change set therefore lands the procedure with
the implemented and accepted command surface. Deleting the procedure would leave the
activation and safe-uninstall boundary undiscoverable; accepting undocumented behavior
would make a successful install look broken for already-running sessions. Publishing
the procedure earlier loses because it directs users to commands that cannot run.

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

**Given** Claude Code `2.1.247`, a running Agentd daemon, and a successful
`agentd integrate install claude`, **when** the test starts a dedicated real Claude
process and real harness actions emit `UserPromptSubmit`, `PreToolUse`, `Notification`,
and `Stop`, **then** retained hook captures prove those exact event names and the Agentd
subscription reports, in event order, `active`, `active`, `needs_attention`, and `idle`
for the one Claude root.

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
the test starts the next interactive Codex process and its `hooks/list` surface
evaluates them, **then** it returns their source as the user `hooks.json`, their status
as `untrusted`, and no Agentd hook executes.

**When** an interactive user chooses continue-without-trusting, **then** the handlers
remain non-runnable. **When** the user later approves the Agentd hooks, **then** Codex
writes each current hash under its exact `hooks.state` key, `hooks/list` reports
`trusted`, and real `UserPromptSubmit`, `PermissionRequest`, and `Stop` events produce
`active`, `needs_attention`, and `idle` claims for the Codex root.

**Given** one trusted Agentd entry whose command changes, **when** the next interactive
Codex process starts, **then** `hooks/list` reports `modified` and that handler does not
execute until the user approves its new hash.

**Given** unchanged trusted Agentd entries, **when** Codex install runs again, **then**
it changes no file bytes and `hooks/list` continues to report those entries as
`trusted`.

The evidence report retains the installed executable path, package version, official
source tag and commit, source hook path, event list, hook keys, hashes, trust statuses,
and the field-scoped `config.toml` changes. It does not retain credentials or hook
payload contents.

### A4 — Idempotent merge and reversible removal (G3; I5, I6, I7)

**Given** an externally quiescent configuration set with captured valid Claude
`settings.json`, Codex `hooks.json`, and Codex `config.toml` fixtures with unrelated
root values, multiple third-party matcher groups, multiple handlers in one group, and
unrelated hook trust, **when** each install runs twice, **then** the second run changes
no bytes and the parsed files contain one copy of each Agentd-owned handler.

**Given** the configuration set remains externally quiescent and Codex has approved its
installed Agentd handlers, **when** each harness uninstall runs once, **then** no exact
Agentd-owned handler remains, the Codex trust members for those handlers are absent,
and each unrelated parsed value and array order equals the pre-install fixture. The
comments and bytes outside the removed owned `hooks.state` members equal the
pre-uninstall Codex file. **When** uninstall runs again, **then** it changes no bytes
and exits 0.

**Given** Codex has unrelated group U before an installed and trusted Agentd group A,
the user later adds and trusts unrelated group B after A, and the complete configuration
set is quiescent for uninstall, **when** Codex uninstall simulates removing A, **then**
it returns `codex_positional_trust_conflict`, exits 1, names B's current and resulting
indexes, and leaves `hooks.json`, `config.toml`, A, and B byte-unchanged. `hooks/list`
continues to report B as `trusted`. **When** the user moves B before A, reviews and
reapproves B if that edit changed its key or definition, and retries uninstall, **then**
uninstall removes A and A's exact trust member while B remains at its user-approved key
and `trusted` status.

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

**Given** each installed harness configuration, a harness process started after that
installation, and an absent Agentd socket, **when** a real Claude or Codex event invokes
its handler, **then** the handler exits 0 within 750 ms, the harness operation
continues, and one diagnostic names the socket failure.

**Given** a running daemon and present mapped identity, **when** the same event fires,
**then** the hook exits 0, writes no output, and the changed claim is observable through
the socket.

**Given** a harness-and-event pair outside I3, **when** `agentd hook` receives it,
**then** it opens no daemon socket, writes `agentd hook: invalid_hook_event`, and exits
1.

### A7 — Observed-conflict refusal and atomic replacement (G3; I7)

**Given** an externally quiescent configuration set whose existing user files have mode
`0600`, **when** install or uninstall succeeds, **then** each replaced file retains its
mode and owner, parses in its native format, and contains the complete pre-change
unrelated configuration plus the required change.

**Given** a new user hook file, **when** install creates it, **then** its mode is `0600`
and its owner UID equals the invoking local user's effective UID.

**Given** a controlled integration test pauses after same-directory temporary creation
and before writing replacement bytes, **when** it inspects that path without following
links, **then** the path is a new invoking-user-owned regular file with mode `0600`.
No pre-existing path was opened or truncated.

**Given** install or uninstall succeeds, **when** the test enumerates the harness
configuration directory, **then** no integration temporary path remains.

**Given** any target path is an existing regular file not owned by the invoking local
user, symlink, directory, FIFO, socket, device, or other non-regular type, **when**
install or uninstall runs, **then** it exits 1 with
`unsupported_configuration_target`, names the path, observed type, and owner mismatch
when applicable, follows no symlink, changes no directory entry or referent, and commits
no replacement to any target in that command.

**Given** an injected write, flush, chmod, chown, or rename failure, **when** the command
returns, **then** the original target path contains either the complete old value or the
complete new value. It contains no partial serialization.

**Given** an injected write, flush, final-comparison, or rename failure before one
temporary path is renamed, **when** cleanup succeeds, **then** that temporary path is
absent before the command returns. **Given** injected unlink failure during that
cleanup, **when** the command returns, **then** it exits 1 with
`temporary_cleanup_failed` or `temporary_cleanup_failed_after_partial`, names the exact
residual path and whether an earlier target committed, and the residue remains an
invoking-user-owned regular file with mode `0600`.

**Given** an integration command has read its baselines and an external writer changes
a target's type, bytes, mode, or owner before preflight completes, **when** the command
attempts to commit, **then** it returns `configuration_changed`, preserves every
external target, and adds or removes no hook declaration or trust member.

**Given** one Agentd integration command holds the harness configuration-directory
lock, **when** another Agentd integration command targets that directory, **then** the
second command returns `configuration_busy` and changes no target. A retry after lock
release merges against the first command's committed bytes.

**Given** Codex uninstall has removed its owned trust members and an external writer
then reorders `hooks.json` so an unrelated hook occupies one removed positional key,
**when** the final declaration comparison runs, **then** it returns
`configuration_changed_after_partial` with `codex_trust_review_required`, preserves
the external `hooks.json` bytes, and leaves the Agentd declarations installed without
granting them trust. Codex derives their current statuses from their new positional
keys and hashes. `hooks/list` reports the unrelated hook at the removed key as
`untrusted`, and the command reports that it requires trust review. A retry merges
against those bytes and completes declaration removal. After the user reapproves that
unrelated hook, Codex persists its current hash and reports it as `trusted` again.

**Given** a controlled integration test pauses a command after its last successful
baseline comparison and a non-Agentd writer that ignores the advisory lock writes a
new complete value before the command's rename, **when** the command resumes, **then**
the atomic rename replaces that external value with the command's complete
baseline-derived replacement, and the command does not return `configuration_changed`
for that write. **When** the user reads `agentd integrate --help`, **then** it includes
the exact I7.11 warning.

### A8 — Base regression and repository gate (G6; I1)

**Given** the v1.1 implementation commit in a clean checkout of
`clickety-clacks/agentd`, **when** the repository runs each base v1 acceptance case and
the documented format, static-analysis, unit, integration, and real-smoke commands,
**then** each command exits 0.

The gate report records the exact product commit, base and amendment hashes, commands,
exit results, installed harness versions, real process identities, hook event captures,
socket path, daemon instance IDs, configuration before-and-after hashes, trust
transitions, and teardown result.

### A9 — Already-running Claude activation (G2, G7; I1, I3, I5, I8)

**Given** a real Claude Code `2.1.247` session already running inside tmux, a running
Agentd daemon, no installed Agentd Claude hooks, and that root's activity
`unknown`, **when** the user runs `agentd integrate install claude`, **then** the
existing process remains in `agentd list --json` with the same exact process identity
and `activity.state=unknown` at command return. The install result says that procfs keeps
the process present, install submits no activity, and `claude --continue` or
`claude --resume` is the supported conversation-preserving restart remedy. It names no
in-session activation action, and the existing first-integration process remains
`unknown` under the supported procedure.

**When** the user exits that process and runs `claude --continue` or selects the
conversation with `claude --resume`, **then** the replacement process loads the
installed declarations and appears in the roster only when procfs proves its new exact
identity. Its record starts at `unknown`; later real I3.1 events produce the exact I3.1
state sequence, and the new identity does not carry the old identity's claim.

**Given** the Claude process loaded the unchanged Agentd declarations before the Agentd
daemon restarted, **when** idempotent install changes no bytes and that process emits a
mapped event, **then** Agentd accepts the claim for the same present identity without a
Claude reload or restart.

### A10 — Already-running Codex activation and refusal (G2, G5, G7; I1, I3, I6, I8)

**Given** a real Codex `0.149.1` session already running inside tmux, a running Agentd
daemon, no installed Agentd Codex hooks, and that root's activity `unknown`, **when**
the user runs `agentd integrate install codex`, **then** the existing process remains
in `agentd list --json` with the same exact process identity and
`activity.state=unknown` at command return. The install result says that procfs keeps
the process present, install submits no activity or trust, and `codex resume` is the
supported conversation-preserving restart remedy whose next interactive startup
presents trust review. It names no in-session activation action, and the existing
first-integration process remains `unknown` under the supported procedure.

**When** the user exits, runs `codex resume` without the bypass option, and chooses
continue-without-trusting, **then** each Agentd hook remains non-runnable and the
replacement roster identity remains `unknown`. **When** the user instead trusts the
Agentd hooks and the replacement process later emits each real I3.2 event, **then**
Agentd reports the exact I3.2 state sequence for the new identity.

**Given** the Codex process loaded and trusted the unchanged Agentd declarations before
the Agentd daemon restarted, **when** idempotent install changes no bytes and that
process emits a mapped event, **then** Agentd accepts the claim for the same present
identity without another Codex review, reload, or restart.

**Given** the same setup with a resolved Codex version other than `codex-cli 0.149.1`,
**when** the user runs `agentd integrate install codex`, **then** the command exits 1,
writes one stderr line containing `unsupported_codex_hooks`, changes no target file,
and leaves the already-running process present with `activity.state=unknown`.

### A11 — Release README is the end-to-end integration procedure (G7; I3, I5-I9)

**Given** the product commit immediately before the accepted integration commands
exist, **when** a reviewer reads its product README, **then** it contains no instruction
or example for `agentd integrate install` or `agentd integrate uninstall`.

**Given** the v1.1 release candidate, **when** a reviewer checks the product README,
**then** it contains separate Claude and Codex procedures with each field required by
I9.2, both exact I3 mapping tables, the I9.3 `needs_attention` meaning, the Codex
version/refusal/trust behavior in I9.4, and the uninstall guarantees in I9.5. Each
documented command and harness action resolves to a surface present in that candidate.

**Given** clean isolated user configuration and real supported Claude and Codex
processes, **when** a new user follows each README procedure verbatim from install
through activation, mapped-event verification, uninstall, and teardown check, **then**
each documented command produces its stated result, each real event produces its exact
I3 claim after the documented replacement-process startup, install itself changes no
activity, and teardown satisfies I9.5. The retained run records the README commit and
line references, command outputs, before-and-after configuration hashes, process
identities, hook captures, restart evidence, and Codex trust statuses.

## Open Questions

Blocking questions: none.

Non-blocking questions: none.

The independent spec review can return defects against this amendment. A finding does
not authorize implementation. The producer must amend this canonical file, land the
revision, and present its new content hash for review before a builder reads it.
