# agentd v1.1 — harness-reported activity and reversible user integrations

Status: READY FOR FINAL INDEPENDENT REVIEW

Date: 2026-08-28 PT

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
  `0.149.1`. These versions are the verified smoke-test baseline, not an exact Codex
  version gate.
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
  `art_9877a0d5` remain the immutable verdict on commit `b773287`. Owner MVP ruling
  `att_e80a6d8f-0358-4f45-90d8-2b1b0161e394` supersedes its process-heavy remedies:
  Codex install detects the hooks feature and warns on unverified versions; mutation is
  read-merge-atomic-rename with one reread/retry; and acceptance is idempotence unit
  coverage plus one real Gibson tmux smoke. Review assignment
  `asg_53cbf6cd-5f27-4fd8-8023-8c0e7423afbd` remains the sole final review lane.
- That review must clear one exact v1.1 content hash before implementation starts.

## Goal

G1. Agentd accepts `needs_attention` as an explicit hook activity claim through the
wire protocol, snapshot, and CLI surfaces that already carry `active` and `idle`.

G2. A local Linux user can install Claude Code or Codex activity hooks that report
harness events to Agentd. Agentd uses no terminal text, screen scraping, model call, or
behavioral inference to produce those claims.

G3. The integration commands change only Agentd-owned hook declarations. They preserve
unrelated user settings, unrelated hooks, array order, and Codex-owned trust state.

G4. A hook invocation updates the one roster record whose process identity Agentd
already exposes, including when the hook's nearest harness ancestor is a nested helper
that the v1 scanner collapses under another same-harness agent root.

G5. The Codex integration requires an enabled installed `hooks` feature and conforms to
the verified user hook schema. An unverified Codex version produces a warning instead
of a version refusal. Agentd does not grant, migrate, remove, or bypass Codex trust.

G6. The v1.1 acceptance run includes merge and uninstall idempotence unit tests and one
real Gibson tmux smoke that proves `idle`, working (`active`), and `needs_attention`
for Claude and Codex. The full v1 acceptance contract remains governing.

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
  that the verified `0.149.1` baseline exposes those events; the MVP does not need them
  to express its three activity claims.
- Automatically accepting a permission prompt or changing a harness permission mode.
- Automatically trusting Codex hooks, writing, migrating, or removing a Codex trust
  hash, editing `hooks.state`, or passing `--dangerously-bypass-hook-trust`.
- Proving compatibility for a Codex version other than the verified `0.149.1` baseline.
  A hooks-enabled unverified version is allowed with the warning required by I6.
- Adding a generic harness integration framework.
- Changing the v1 Linux-only, local-user, Unix-socket, systemd-user-service, privacy,
  or in-memory boundaries.
- Byte-for-byte preservation of JSON whitespace. Preservation means that unrelated JSON
  values and array order remain semantically equal.
- Locking a harness configuration directory, journaling a mutation, or guaranteeing
  preservation of a concurrent edit that occurs after the final reread and before the
  atomic rename. I7 provides one reread/retry and then refuses a second observed change.
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

### Configuration read and retry

A **configuration read** records whether the one harness hook target exists and, when
it exists, its exact bytes, mode, owner, and no-follow directory-entry type. An absent
target is supported. An existing target is supported only when it is a regular file
owned by the invoking local user's effective UID. Any symlink, differently owned file,
or non-regular target is an **unsupported configuration target**.

A **concurrent change** exists when the target's existence, bytes, mode, owner, or
no-follow type differs at the reread immediately before atomic rename. The command
discards its candidate, rereads, remerges, and retries once. A second observed change
returns `configuration_changed` without renaming the second candidate.

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

**Unrelated configuration** is each value, object member, array element, and hook
handler that is not an Agentd-owned hook declaration. Every Codex hook-state entry is
unrelated configuration because Agentd does not own or edit Codex trust.

### Codex hook trust

Codex classifies an unmanaged command hook as:

- `untrusted` when the user configuration contains no trusted hash for the key;
- `trusted` when the persisted hash equals the current hash;
- `modified` when the persisted and current hashes differ.

Codex runs an unmanaged hook only when it is enabled and `trusted`, unless its caller
uses the dangerous per-invocation bypass. The interactive startup review offers review,
trust-and-continue, or continue-without-trusting. Codex owns its hashes, keys, review,
and persisted `hooks.state` values. Agentd never edits them.

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
- Codex CLI `0.149.1` verifies the JSON shape shown in Architecture C and exposes these
  11 command-hook event names:
  `PreToolUse`, `PermissionRequest`, `PostToolUse`, `PreCompact`, `PostCompact`,
  `SessionStart`, `SessionEnd`, `UserPromptSubmit`, `SubagentStart`, `SubagentStop`, and
  `Stop`.
- A Codex version accepted by install reports its stable `hooks` feature as enabled.
- The user configuration directory for an integration exists and belongs to the local
  user before installation starts.
- A harness starts a command hook as a descendant of the harness process that emitted
  the event. The hook process can observe that ancestry through procfs.
- The hook payload can contain prompts, paths, tool inputs, and other private data.
  Agentd does not need any payload field to apply the fixed event mapping.
- A same-directory temporary file can be atomically renamed over each user configuration
  file on the target filesystem.
- The verified Claude Code `2.1.247` activation procedure starts a replacement process
  after install. It does not depend on a watcher, RPC, `/hooks` behavior, signal, flag,
  or other harness-internal reload path.
- The verified Codex CLI `0.149.1` activation procedure starts the next interactive
  process after install. That startup reviews new or changed unmanaged hooks. An
  unverified hooks-enabled version can differ, which is why install warns. The
  documented procedure does not depend on an in-session reload path.

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

I3.2. The Codex integration installs exactly these mappings:

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

I6.2. Before it writes, install resolves `codex`, runs `codex --version` and
`codex features list`, and requires the stable `hooks` feature to be present and
enabled. A missing or disabled feature returns `unsupported_codex_hooks`, exits 1, and
changes no file. Install does not use the version string as a refusal gate.

I6.3. Compatibility is verified against `codex-cli 0.149.1`. When the resolved version
differs, install continues after feature detection and prints
`warning=unverified_codex_version version=<reported-version>` in its result. The warning
does not claim compatibility and does not suppress the activation and trust guidance.

I6.4. Install targets only the Codex user `hooks.json`. It creates that file with a root
JSON object and a `hooks` object when the configuration directory exists and the file
does not.

I6.5. Each mapping in I3.2 adds one group under `hooks.<event>`. The group has no matcher
and contains one command handler with `type="command"`, the Agentd-owned command,
`timeout=1`, and `async=false`.

I6.6. Install replaces an Agentd-owned entry that names an old absolute Agentd path with
the canonical entry for the installer's current absolute path. Codex classifies the
changed definition as `modified` until the user trusts its new current hash.

I6.7. Install appends each missing Agentd group after existing groups. It preserves the
relative order and values of every existing group and handler.

I6.8. Install does not write `config.toml`, `hooks.state`, a `trusted_hash`, a hook
feature flag, or a trust-bypass option. Its success output says that Codex must review
new or changed hooks before Codex runs them.

I6.9. On the next interactive Codex startup without the bypass option, Codex presents
each new Agentd handler as `untrusted`. Choosing continue-without-trusting leaves it
non-runnable. Choosing trust persists Codex's current hash under that handler's
`hooks.state` key and makes that exact definition runnable.

I6.10. A changed Agentd handler becomes `modified` and does not run until Codex persists
the new current hash. Agentd does not compute, copy, or fabricate that hash.

I6.11. A second install against unchanged canonical Agentd entries changes no file
bytes. Because Agentd does not edit Codex trust, it preserves whatever trust state
Codex derives for the unchanged declarations.

I6.12. Uninstall removes only exact Agentd-owned handlers, regardless of the absolute
Agentd executable path they name. It removes an empty Agentd matcher group and event
member under I5.7. A command that is not an exact owned declaration remains in place
and is reported as not removed.

I6.13. Uninstall does not resolve Codex, apply a version or feature gate, or edit
`config.toml` or `hooks.state`. Codex owns any trust-state reconciliation caused by the
declaration removal.

I6.14. Uninstall preserves the root `hooks` object and Codex user `hooks.json`, including
when install created them and the resulting `hooks` object is empty. A second uninstall
changes no file bytes and exits 0.

### I7 — Configuration mutation is read-merge-retry-rename

I7.1. Before install or uninstall reads its one hook target, it uses a no-follow
metadata operation. An absent target is valid. An existing target must be a regular
file whose owner UID equals the invoking local user's effective UID. An existing
regular file with another owner, symlink, or other non-regular target returns
`unsupported_configuration_target`, names the path, exits 1, follows no referent, and
changes no path.

I7.2. The command reads the target, validates its JSON shape, and merges only the
Agentd-owned declaration change into that value. Malformed JSON, an invalid target
member type, an unresolved Agentd executable, or a set relative harness configuration
directory returns one named error and changes no path.

I7.3. When the merge produces no semantic change, the command does not rewrite the
target. This makes a repeated install or uninstall byte-idempotent.

I7.4. When the merge changes the value, the command writes and flushes the complete
serialized result to a uniquely named same-directory temporary regular file created
exclusively with mode `0600`. It removes that temporary path after any pre-rename exit.

I7.5. Immediately before rename, the command rereads the target with the I7.1 checks.
If the target differs from the read used for the merge, the command discards its first
candidate, performs one fresh read and merge, and creates one fresh candidate. If the
target differs again at the second reread, the command returns
`configuration_changed`, removes the candidate, and changes no target. The command
does not attempt a second retry.

I7.6. When the reread matches, the command atomically renames the complete candidate
over the target. It preserves the mode and owner of an existing target. It creates a
new target with mode `0600` and owner UID equal to the invoking local user's effective
UID. The reread and rename are not an indivisible compare-and-swap; the Non-Goals name
the remaining concurrent-write race.

I7.7. Each merge preserves every unrelated root value, hook event, matcher group,
handler, and the relative order of unrelated array elements. Codex commands do not
read or write `config.toml`.

I7.8. Install and uninstall write no backup, receipt, cache, integration registry, or
advisory lock. The closed command marker makes ownership detectable without a second
source of truth.

I7.9. Each command prints one result line that names the harness, action, changed or
unchanged result, and target path. A Codex install result also names the pending trust
action and any I6.3 unverified-version warning. Usage or mutation failure exits 1 and
writes one error line to stderr. Success exits 0.

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

I8.4. An already-running interactive Codex process does not trust a newly
installed or changed Agentd declaration merely because install committed it under the
supported v1.1 contract. The user exits and runs `codex resume` to preserve access to
the conversation. That next interactive startup presents the new or changed hooks for
review under I6.9. Continue-without-trusting leaves them non-runnable; approval persists
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

I8.6. The successful install result required by I7.9 includes harness-specific
guidance for already-running sessions. Every line says procfs keeps the existing process
in the roster, install does not change its current activity, and the next accepted
mapped hook event changes activity. The Claude line names no in-session activation
action. It names `claude --continue` and
`claude --resume` as the conversation-preserving restart remedies. The Codex line names
`codex resume` as the conversation-preserving restart remedy and says the next
interactive startup presents trust review. The line does not claim that an unchanged
idempotent reinstall deactivates a declaration already loaded by the process. When
I6.3 applies, the Codex result also warns that the installed version is unverified.

### I9 — The release README is truthful and complete

I9.1. Before the product commit that implements and accepts the v1.1 integration
commands, the product README contains no instruction or example that tells a user to
run `agentd integrate install` or `agentd integrate uninstall`. The v1.1 release cut
adds the procedure in I9.2-I9.6 in the same release change set as the implemented
commands. A spec, placeholder, or forecast does not satisfy this clause.

I9.2. The v1.1 release README gives separate end-to-end Claude and Codex procedures.
Each procedure names the verified harness version, user configuration target, exact
install command, restart-only activation action, conversation-preserving restart
command, observable verification, exact uninstall command, and successful teardown
check. The Claude procedure names `claude --continue` and `claude --resume`. The Codex
procedure names `codex resume` and states that an enabled `hooks` feature is required.

I9.3. The release README reproduces both complete I3 event-to-state tables and defines
`needs_attention` as the latest accepted hook claim that the harness emitted an event
mapped to user attention. It states that the claim does not prove the need still
exists.

I9.4. The Codex procedure states that compatibility is verified with
`codex-cli 0.149.1`, but install gates on the enabled `hooks` feature instead of an
exact version. A missing or disabled feature returns `unsupported_codex_hooks` and
changes no target file. Another hooks-enabled version proceeds with an
`unverified_codex_version` warning. The procedure states that the next interactive
Codex startup reviews each new or changed Agentd hook, continue-without-trusting leaves
it non-runnable, and trust approval makes only the approved current definition
runnable. It states that Agentd never edits Codex trust state.

I9.5. The uninstall procedure states the guarantees from I5.7-I5.10, I6.12-I6.14, and
I7 in operator terms: a successful uninstall removes only exact Agentd-owned
declarations even after the Agentd executable moves; each harness preserves unrelated
configuration and ordering; Codex trust state remains Codex-owned and unchanged by
Agentd; user hook files and their root `hooks` objects remain; and a repeated uninstall
is byte-idempotent. It states that a concurrently changed file is reread and merged once
before `configuration_changed` refuses a second observed change.

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

The Codex integration merges this `0.149.1`-verified user shape for each I3.2 event:

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
does not read or write Codex trust state during install or uninstall. Removing a
declaration can cause Codex to reconcile its own positional trust metadata. Agentd does
not decide that executable code is safe on the user's behalf.

### E. Configuration merge and removal

Each harness has one schema-aware JSON merge path. It validates first, identifies owned
handlers by parsed exact command, appends missing entries, removes exact owned entries,
and writes one complete value by atomic replacement. Codex integration edits only
`hooks.json`; Codex remains the sole writer of its trust state.

The configuration mutation pattern is **read-merge-reread-retry-rename**. The command
reads and validates the current file, merges its own entries, writes a complete private
candidate, and rereads immediately before atomic rename. One observed concurrent
change restarts that sequence from the new bytes. A second observed change refuses the
operation. The command uses no directory lock, baseline protocol, quiescence contract,
journal, backup, or cross-file transaction.

This pattern preserves unrelated values in every merge and avoids partial target
serialization. The small race between the final reread and rename remains an explicit
MVP boundary. A lock cannot coordinate arbitrary editors, and a journal does not make
rename a compare-and-swap. Codex-owned trust also avoids the positional-trust mutation
that caused F4, while mode-`0600` private candidates and pre-rename cleanup close F5 at
MVP scope.

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

The v1.1 amendment adds exactly two acceptance gates. The base contract's existing
acceptance remains governing.

### A1 — Merge and uninstall idempotence unit tests (G3, G5; I5-I7)

**Given** valid Claude `settings.json` and Codex `hooks.json` fixtures that contain
unrelated root values, events, matcher groups, multiple handlers, and array ordering,
**when** each install runs twice, **then** the first run appends or canonicalizes only
the exact Agentd-owned declarations, the second run changes no bytes, and the parsed
files contain exactly one copy of each required handler.

**Given** those installed fixtures, including an Agentd-owned declaration whose
absolute executable path is old and unrelated commands that contain the word `agentd`,
**when** each uninstall runs twice, **then** the first run removes only exact
Agentd-owned declarations, the second run changes no bytes, and all unrelated values
and relative array order equal the pre-uninstall fixture. Claude and Codex hook files
and their root `hooks` objects remain. Codex `config.toml` is byte-identical before and
after both commands.

### A2 — One real Gibson tmux integration smoke (G1, G2, G4-G7; I1-I9)

**Given** the v1.1 release candidate on Gibson, its matching README, a running Agentd
daemon, clean isolated user configuration, and real Claude and Codex processes already
running in separate tmux sessions with `activity.state=unknown`, **when** the operator
follows the README and runs both install commands, **then** both commands exit 0 and
create their exact I3 declarations without changing unrelated hooks or Codex trust.
Codex install records an enabled `hooks` feature and prints the I6.3 warning only when
its version is not `codex-cli 0.149.1`.

At each install return, procfs keeps the existing process in the roster under the same
exact identity and its activity remains `unknown`. Claude output names
`claude --continue` and `claude --resume`. Codex output names `codex resume` and the
next-interactive-startup trust review. Neither output names an in-session reload.

**When** the operator starts replacement processes with the documented
conversation-preserving commands and approves the current Agentd Codex hooks at the
interactive trust review, **then** procfs alone admits each replacement identity and
each new record starts at `unknown`.

**When** real Claude `UserPromptSubmit`, `Notification`, and `Stop` events occur,
**then** the Claude record shows working (`active`), `needs_attention`, and `idle` in
that order. **When** real Codex `UserPromptSubmit`, `PermissionRequest`, and `Stop`
events occur, **then** the Codex record shows working (`active`),
`needs_attention`, and `idle` in that order. The captures prove the fixed I3 mapping
and contain no retained prompt, tool input, transcript path, or other hook payload.

**Given** the Agentd socket is unavailable during one real event for each harness,
**when** each installed handler runs, **then** it exits 0 within 750 ms, prints only
the typed Agentd diagnostic, and does not block or fail the harness action.

**When** the operator follows the README uninstall and teardown steps for both
harnesses, **then** only exact Agentd-owned declarations are removed, unrelated
configuration remains, Codex trust state is unchanged by Agentd, and a repeated
uninstall changes no bytes and exits 0.

The retained smoke evidence names the exact product and spec commits, README lines,
harness versions and Codex feature output, tmux sessions, exact process identities,
command results, before-and-after hook-file hashes, activity frames, hook diagnostics,
and teardown result. It retains no hook payload contents or credentials.

## Open Questions

Blocking questions: none.

Non-blocking questions: none.

Known MVP safety boundaries are the unverified Codex-version warning, the concurrent
write gap between the final reread and atomic rename, and Codex-owned trust
reconciliation after declaration removal. The delivery owner records these concerns at
completion.

The independent spec review can return defects against this amendment. A finding does
not authorize implementation. The producer must amend this canonical file, land the
revision, and present its new content hash for review before a builder reads it.
