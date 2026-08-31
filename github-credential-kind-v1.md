# GitHub credential kind and E3 host-auth seams — v1

Status: CANDIDATE for `main` / 0.2.0. This spec executes the E3 election in
`0.2.0-cross-line-reconciliation-plan.md` without applying the 0.1.8 patch
shape. Source behavior is the reviewed 16-commit PR20 first-parent range
`c57c1903f738c46b2519356f91c1c41d82136193^..60bda7eb1771a7d240a51d9277adff96f666ee5e`.
The exact reviewed source verdict is `att_399cfcd5`; the real-device row is
`att_4341d983`; the pre-device prompt defect is
`wi_f40b7527-72da-4855-ba12-c5c910fb7c08`. Credential custody follows
`credential-kinds-v1.md` plus the harness-home-only ruling on
`wi_b83e1fed-79fd-4fe4-9706-b004486af1a3`.

## Goal

Make authenticated GitHub operations a host-local, account-scoped capability
on 0.2.0. Keep PR20's reviewed command classifier, probes, redaction, readiness,
and fixture behavior. Replace its three 0.1 seams:

1. An archetype provisioning election projects the selected GitHub credential
   home into an agent environment.
2. Org-authored dispatch-rule law guards GitHub operations before execution and
   names each refusal.
3. A first-class `github` credential kind points at one `gh`-owned credential
   home. Tightbeam keeps no secret copy.

The maxim is: **the human chooses the GitHub identity, `gh` owns its only secret
home, the archetype elects its projection, and compiled law refuses an unready
network operation by name.**

ADD wins over DELETE because Mike elected the PR20 capability for 0.2.0. ACCEPT
wins for neither custody nor runtime-only failure: ambient credentials caused
the original daemon/keychain split, and a Git failure after an agent starts work
is later and less repairable than a pre-execution refusal.

## Non-Goals

- This spec does not add PAT input, `--with-token`, token environment variables,
  or token transit between hosts.
- This spec does not change the `api_key | subscription` model-provider kinds or
  the model-provider activation lifecycle.
- This spec does not choose a GitHub account for a user.
- This spec does not infer a GitHub account from a repository owner, remote URL,
  credential file, operating-system keychain, or prior shell environment.
- This spec does not support two GitHub credential profiles in one session.
- This spec does not make a preflight probe and the following provider operation
  atomic. External revocation can occur between them; the operation then fails
  through the provider path and the next probe observes the failure.
- This spec does not delete the 0.1.9 bank during upgrade.
- This spec does not turn a tool-call rule into a sandbox. The rule prevents
  accidental unauthenticated operations through supported harness tool-call
  seams; containment remains a separate mechanism.
- This spec does not add an agent operating pattern beyond
  `credential-home-projection`, defined below. The implementation adds its one
  operator directive to the existing onboarding guidance when the mechanism
  exists: choose a profile, run `tightbeam onboard github`, and do not give a PAT
  to an agent.

## Terms

- **GitHub credential kind** — the first-class kind named `github`. Its secret
  owner is the `gh` executable. Its consumer is a host process that runs `gh` or
  Git through `gh auth git-credential`. It is not a model-provider credential.
- **Credential profile** — a user-chosen, non-secret selector matching
  `^[a-z0-9][a-z0-9-]{0,62}$`, such as `default`, `work`, or `personal`. A profile
  gives concurrent GitHub identities separate `GH_CONFIG_DIR` values.
- **Credential home** — the sole provider-native storage authority for one
  `{machine, profile}`:
  `<base_dir>/credential-homes/<machine>/github/<profile>`. Tightbeam may create
  the directory, inspect file type and mode, change mode, and invoke `gh` against
  it. Tightbeam does not read, parse, serialize, copy, hash, link, or transmit a
  secret-bearing file in the home.
- **Account** — the non-secret login returned by
  `gh api --hostname <hostname> -i user --jq .login` for one hostname inside a
  credential profile. The provider response designates the account. The profile
  name does not.
- **Hostname** — the GitHub hostname supplied to onboarding or parsed from a
  remote. `github.com` is the CLI default. A non-default hostname enters the
  operation classifier only after onboarding recorded it for the elected
  profile; the substrate does not guess which hosts run GitHub.
- **Projection election** — an archetype manifest's explicit selection of one
  GitHub credential profile. The election projects only `GH_CONFIG_DIR` and
  non-secret selection facts. It projects no token bytes.
- **Credential-home projection** — the pattern established by this spec: a
  provider CLI owns one secret home; identity law selects the home; provisioning
  projects its path; health code invokes the provider without reading its file.
  It applies to CLI-native host credentials. It does not replace harness-home
  custody for model-provider credentials.
- **GitHub operation** — a Bash tool call whose executable command contains a
  `gh repo`, `gh pr`, `gh issue`, or `gh api` operation, or a Git operation that
  can contact a configured GitHub remote: `clone`, `fetch`, `pull`, `push`,
  `ls-remote`, `remote update`, `submodule add`, or `submodule update`.
- **Operation classifier** — PR20's deterministic parser for executable command
  structure. It reads `tool_input.command`, preserves quoted arguments, follows
  shell connectors, unwraps environment assignments and wrappers, recurses into
  shell `-c` scripts, removes here-document bodies, resolves named Git remotes,
  and parses URLs. It does not read prose fields.
- **Operation rule** — org-authored dispatch-rule law named
  `github-network-auth-required`. The identity compiler projects it into the
  supported harness's pre-tool-call seam. The rule calls the classifier and
  readiness probe on the session's host. The rule, not a hardcoded reserved hook,
  decides allow or refusal.
- **Profile binding** — a non-secret durable row for one
  `{machine, profile, hostname}`. Onboarding is its only create/update seam;
  local revocation marks it revoked. It records the selected hostname, the last
  observed account, state, cause, principal, and time. It contains no credential
  path or provider output. The operation classifier uses every binding state to
  recognize configured enterprise GitHub hostnames without opening `hosts.yml`.
- **Capability observation** — a non-secret durable event describing one probe:
  kind, machine, profile, hostname, account when observed, state, cause,
  principal, operation class, observation time, and rule when operation-bound.
  It is evidence, not credential authority and not a cached authorization.
- **Hollow auth** — a present `hosts.yml` authority is zero-length,
  non-regular, symlinked, hard-linked, unreadable by `gh`, or more permissive
  than this spec allows. An absent home or absent `hosts.yml` is
  `needs_onboarding`, not hollow. Tightbeam establishes both states from file
  metadata and `gh`'s result, not from secret contents.
- **Expired auth** — the provider returned HTTP 401 while the elected profile was
  used. File age, metadata age, token shape, and `gh auth status` prose do not
  establish expiry.
- **Legacy bank** — PR20's 0.1.9 path `<base_dir>/auth/github/gh`. It is neither
  authority nor fallback on 0.2.0.
- **Principal** — the user or session whose command caused onboarding,
  revocation, probing, projection, or refusal. Each capability marker records it.

## Assumptions

1. GitHub CLI 2.97.0 accepts `--hostname`, `--web`, `--git-protocol https`, and
   `--insecure-storage`; `--with-token` remains a distinct path. The
   implementation rechecks the installed CLI's help in its real-response
   capture.
2. With `GH_CONFIG_DIR` set and `--insecure-storage`, `gh` writes its native
   secret authority under that directory and `gh auth git-credential` reads the
   same authority.
3. The installed `gh` may ask `Authenticate Git with your GitHub credentials?
   (Y/n)` before it emits a device code even when `--git-protocol https` is
   present. The successful TARS row `att_4341d983` observed this.
4. Main's identity projection can add one manifest table and compile a
   dispatch-rule into each supported harness home. Current main does not yet
   implement these E3 seams; this spec includes the minimum increments.
5. Supported harnesses expose a pre-tool-call Bash hook that can refuse before
   the Bash command runs. An implementation that loses this hook refuses the
   affected session's GitHub operations by name; it does not silently weaken the
   rule.
6. A remote host has its own base directory and installed `gh`. The gateway can
   provision identity material there, but it cannot make a local credential
   authoritative there.
7. Provider output and command grammar can change. A real-response fixture
   records the reading used by this version; an unknown response becomes
   `unknown`, not `live`.

## Invariants

### I1. One secret authority

For each `{machine, profile}`, `gh` writes and rotates one provider-native
credential home in place. Tightbeam stores only non-secret observations and
profile bindings. A projection, migration, health check, rotation, revocation,
home regeneration, assimilation, or rollback creates no second secret-bearing
file.

**R1 / A1.** Given a sentinel secret in the profile fixture, when onboarding,
projection, probing, rotation, revocation, regeneration, remote provisioning,
doctor, and rollback fixtures run independently, then any remaining sentinel
exists only in the fixture provider's final `hosts.yml`; source scans and
captured argv, env, events, stderr, stdout, JSON, and artifacts contain no
sentinel.

### I2. Explicit projection and ambient isolation

Provisioning reads the session's pinned archetype manifest. An elected profile
sets `GH_CONFIG_DIR` to that host's credential home. A manifest with no GitHub
election removes inherited `GH_CONFIG_DIR`; the operation rule refuses GitHub
operations as `github-profile-not-elected`. The local host, gateway host, another
profile, an OS keychain, and `~/.config/gh` are not fallbacks.

**R2 / A2.** Given a live `default` profile on the gateway and no elected profile
on a satellite session, when that session attempts a GitHub operation, then the
rule refuses before `gh` or network Git runs and names the satellite plus the
manifest remedy. Given a satellite `work` election, only the satellite `work`
path appears in its environment.

### I3. Law owns the guard

The identity tree carries `github-network-auth-required` as dispatch-rule law.
The rule compiler projects it by archetype into the pre-tool-call seam. Product
code supplies the classifier, credential-kind operations, and probe facts; it
does not unconditionally append a reserved GitHub hook. Amending or removing
the rule uses the ordinary identity law path and changes the projected identity
hash.

**R3 / A3.** Given the rule present, absent, and text-amended in three identity
fixtures, when the same archetype home compiles, then its hook set and identity
hash change exactly with the rule. A repository search finds no
`github_auth_entry`-style unconditional hook append. A refusal begins with the
rule name.

### I4. Observed health only

The kind reports `missing_cli`, `profile_not_elected`, `needs_onboarding`,
`hollow`, `live`, `expired`, `insufficient_scope`, `git_unready`, `revoked`,
`present_but_unverified`, or `unknown`. `account_mismatch` and
`device_flow_expired` are mutation outcomes that leave
`present_but_unverified` when the provider touched the home, or the prior
observed state when it did not; they are not additional health states. Only a
successful current probe returns `live`. Only a provider
HTTP 401 returns `expired`; a 403 returns `insufficient_scope`; transport
failure, timeout, unrecognized output, unavailable host, or disagreement
between provider checks returns `unknown`. None of those last states authorizes
work.

**R4 / A4.** Given fixture responses for each health state and mutation outcome,
when both Rust and Elixir classifiers read them, then they return the same
state. Changing file mtime or
recorded observation time does not change state. Replacing the response with an
HTTP 401 changes it to `expired` and records the observation cause and principal.

### I5. Account and host isolation

A profile selects one credential home per machine. Two profiles use disjoint
homes and locks. A profile may contain one provider-selected account per
onboarded hostname because `gh` natively supports multiple hostnames in one
config directory. Sessions with different profiles can operate concurrently;
the product does not call `gh auth switch` on a shared store.

**R5 / A5.** Given `work` and `personal` profiles on one host plus `work` on a
second host, when three session fixtures run concurrent status and Git probes,
then each fixture observes only its elected account and home. No invocation
changes another fixture's active account, bytes, mode, or capability event.

### I6. Fail closed at the operation boundary

The compiled rule completes its check before the guarded command starts. It
allows only `not_applicable` or a current `live` result for each GitHub hostname
and remote the command can contact. Missing, hollow, expired, insufficient,
git-unready, unknown, unelected, malformed-tool-call, and rule-runtime failures
refuse. Each refusal names the rule, machine, profile, hostname, failed phase,
state, cause, principal, and exact repair. It omits secret paths and token bytes.

The check and action are intentionally two steps, not an atomic transaction. A
provider-side change after the check may make the action fail. The guard records
what it observed; it does not claim the later operation succeeded.

**R6 / A6.** Given a marker file written by fixture `git` before network work,
when direct, wrapped, connector-separated, and nested-shell GitHub operations
run under each non-live state, then the marker remains absent and exit is a
named rule refusal. Under `live`, the marker appears. A concurrent provider
revocation after the check causes the operation fixture to fail without changing
the earlier observation to a false claim of success.

### I7. Prose is not an operation

The classifier examines executable command structure. Assignment briefs,
prompts, descriptions, comments, quoted data, and here-document bodies do not
trigger a probe. Named Git remotes resolve from local Git configuration before a
network check. A configured non-GitHub remote passes without a GitHub probe.

**R7 / A7.** Given the reviewed PR20 command vector plus userinfo, mixed-case,
leading-redirection, push-option, submodule, and relative-submodule cases, when
the classifier runs, then the operation cases classify and the prose/data cases
return `not_applicable`. Breaking any one parser branch turns its named vector
red.

### I8. Secret-shaped values cannot reach output

Remote URLs and provider diagnostics enter reportable code only through a
redacted value type. The type removes URL userinfo and GitHub token families
`ghp_`, `gho_`, `ghu_`, `ghs_`, `ghr_`, and `github_pat_` before formatting or
serialization. Raw provider output cannot satisfy a report, event, error, doctor,
readiness, or refusal field type.

**R8 / A8.** Given one distinct sentinel in each token family, URL userinfo,
provider stdout, provider stderr, a remote name, and a repair hint, when each
error and success surface renders, then no sentinel appears and the useful
hostname/owner/repository context remains. A Rust compile-fail fixture proves a
raw string cannot populate a safe-detail field. An Elixir boundary fixture
proves serializers and event constructors reject an untagged raw detail at
runtime.

### I9. Minds choose; the substrate verifies and acts

The user chooses profile names, hostnames, accounts, device-flow completion,
rotation, local revocation, remote grant revocation, and manifest elections.
The substrate validates structure, serializes mutations, projects the elected
path, runs deterministic probes, compiles law, refuses, and records facts. It
does not choose or switch an account from remote ownership, last use, or health.

**R9 / A9.** Given two live profiles and a manifest with no election, when a
session reaches GitHub work, then the substrate refuses with the election remedy
instead of selecting either profile. After a human-authored manifest election,
a fresh session uses only that profile.

### I10. Each marker carries cause and principal

Onboarding, rotation, revocation, projection refusal, probe result, operation
refusal, legacy-bank detection, and rule-runtime failure write capability events
with non-null `cause` and `principal`. The event payload carries no credential
path or provider raw output.

One append-only capability-event API is the mutation seam for observations and
refusals. One profile-binding API is the mutation seam for configured hostnames,
last observed accounts, and revocation tombstones. Product code does not write
either record shape by another path.

**R10 / A10.** Given each terminal branch in the fixture matrix, when the branch
returns, then exactly one event of each applicable kind exists with the actor,
cause, machine, profile, and hostname. Repeating an idempotent success creates
no duplicate mutation event; a fresh probe may create a fresh observation
event.

## Architecture

### 1. First-class kind contract

The credential-kind registry gains `github`. The kind exposes only these
operations to the rest of Tightbeam:

1. Resolve a credential home from `{base_dir, machine, profile}`.
2. Validate profile syntax and storage metadata without reading secret bytes.
3. Return the environment projection for an elected profile.
4. Run onboarding, current health, optional remote readiness, rotation, and
   local revocation by invoking `gh` with the resolved `GH_CONFIG_DIR`.
5. Return typed non-secret observations and typed redacted diagnostics.
6. Enumerate secret *paths* for redaction and permission checks without opening
   their contents.
7. Create or update a non-secret profile binding through the one binding API.

No kind method returns credential bytes. No generic credential store accepts
GitHub bytes. The closed function set makes a Tightbeam-owned secret copy
unsayable through the credential-kind interface. Elixir cannot enforce return
types at compile time, so the implementation also tests the exported function
set and keeps secret-file opening out of this module.

**R11 / A11.** Given the registry module and its fake kind, when the public API
inventory runs, then the closed operation set above is exact and no function
accepts or returns credential bytes. A source-boundary test fails when the kind
module opens `hosts.yml` or calls a generic secret-bank write. The fake kind can
return only a home reference and non-secret observation. This takes the
strongest affordable rung on the dynamic Elixir seam: one closed interface plus
a test, with the Rust safe-detail boundary enforced by the compiler under R8.

Storage rules:

- The credential home and each directory Tightbeam creates below
  `credential-homes/` use mode `0700`.
- Each regular file under the home uses mode `0600` and link count one.
- A symlink, hard link, device, directory in place of `hosts.yml`, zero-length
  `hosts.yml`, or mode with group/other bits produces `hollow` and the repair.
- Tightbeam may correct an overly broad mode only during an explicit onboarding
  or rotation command. Readiness and operation checks report `hollow`; they do
  not silently mutate storage.
- Identity home regeneration, `identity apply`, assimilation, upgrade, and
  session retirement exclude `credential-homes/` from copy, link, removal, and
  staging sets.

**R12 / A12.** Given regular-private, absent, empty, permissive, symlink,
hard-link, directory, and device fixtures, when readiness runs, then only the
regular-private fixture can reach the provider probe. Given explicit onboarding
over the permissive fixture, then modes become private before success is
reported. Regeneration and assimilation leave sentinel inode identities and
bytes unchanged.

### 2. Archetype provisioning election

An archetype manifest accepts this optional table:

```toml
[provisioning]
class = "workshop"

[provisioning.credentials.github]
profile = "default"
```

`provisioning.class` is `workshop` or `desk`. A missing `provisioning` table
preserves the current workshop capability shape but elects no GitHub profile.
The seed `exec` archetype declares `class = "desk"`. A desk manifest that
declares a credential election is a load error. The shipped
agentic-engineering `coder`, `reviewer`, `recon`, `spec-writer`, `orchestrator`,
and `product-owner` manifests explicitly elect `default`; no wildcard or
implicit election exists. The neutral `default`, `avasarala`, `miller`, and
`exec` manifests elect no GitHub profile.

Provisioning composes environment in this order: substrate-reserved variables,
archetype credential elections, then host/harness overlays that do not collide
with reserved names. `GH_CONFIG_DIR` is reserved. An election writes the exact
host-local credential-home path. No election removes inherited
`GH_CONFIG_DIR`. A colliding overlay is a named configuration refusal.

Remote projection resolves the same logical `{machine, profile}` against the
remote host's base directory and quotes the path once in the SSH command. It
does not project the gateway path.

**R13 / A13.** Given workshop-with-election, workshop-without-election,
desk-without-election, desk-with-election, colliding-overlay, local, and remote
manifest fixtures, when manifests load and environments project, then the first
three valid shapes produce the specified env, the two invalid shapes refuse by
name, and remote output contains only the remote path.

### 3. Compiled operation law

The dispatch-rule compiler accepts the existing rule name, text, actor scope,
and check/effect shape for a `tool-call` edge. It compiles a rule for an
archetype into a harness-native pre-tool-call hook. The hook runs on the
session's host, not on the gateway, because that process owns the filesystem,
Git configuration, `gh`, and network failure.

The E3 law declares one check with these results:

```text
not_applicable -> allow
live           -> allow
profile_not_elected | missing_cli | needs_onboarding | hollow | expired |
insufficient_scope | git_unready | revoked | present_but_unverified | unknown |
malformed_tool_call | rule_runtime_failure -> deny
```

The law's actor scope is each archetype with Bash capability. A manifest
election changes which profile the check reads; it does not turn the law on or
off. This closes the ambient-credential bypass for unelected archetypes.

The compiled entry carries the rule name and identity revision. At session
start, the existing hook wiring proof includes this rule. A failed wiring proof
refuses session readiness as `github-rule-unarmed` before agent work can start;
the product does not claim that a missing hook can intercept a later command. A
law-free org can remove the rule through the identity path; the product does not
recreate it as a reserved entry.

**R14 / A14.** Given Claude and Codex home fixtures, when the law compiles and
the wiring proof runs, then both harnesses refuse the probe with the same rule
identity and later enforce the vector. Given an unarmed hook, session readiness
refuses as `github-rule-unarmed` before an agent tool call; given the rule
removed from identity, the compiler emits no GitHub entry.

The classifier preserves the reviewed 60bda7e behavior and tests. It adds
configured GitHub hostnames from the elected profile's profile bindings instead
of hardcoding only `github.com`. A binding is recognition evidence, not health;
the current probe still decides authorization. The classifier removes URL
userinfo before using a remote in a probe or remedy. It resolves named remotes
and submodule URLs from local configuration without contacting a server.

**R15 / A15.** Given `github.com`, a configured enterprise hostname,
look-alike hosts, mixed case, trailing dot, scp syntax, ssh/http/https syntax,
userinfo, relative submodules, and named non-GitHub remotes, when the classifier
runs, then only the default or recorded GitHub hostnames classify. Safe output
contains no userinfo.

### 4. Onboarding, rotation, and revocation

The compatible command is:

```text
tightbeam onboard github [--hostname github.com] [--profile default]
                         [--account <login>] [--remote <URL>] [--replace]
```

Omitting the new flags preserves PR20's operator shape: hostname and profile
default to `github.com` and `default`. The command remains host-local. An
operator runs it on a satellite for that satellite; the gateway does not relay
secret material.

The command acquires a process-bound exclusive lock for `{machine, profile}`.
The operating system releases the lock when the process exits. A second writer
refuses as `github-credential-busy`, names the first principal when known, and
asks the operator to retry after that process exits. A readiness probe takes a
non-blocking shared lock. If a writer holds the lock, the probe returns `unknown`
without inspecting the home and denies the operation.

Without `--replace`, the command first runs current health. A live matching
account and passing optional remote probe returns an idempotent success without
starting login. A supplied `--account` must equal the account observed after
login; mismatch returns `account_mismatch` and `present_but_unverified`. The
substrate does not switch accounts to satisfy the argument.

For device login, the command:

1. Validates the profile and final home without opening secret contents.
2. Creates or updates the profile binding to `onboarding`. A binding-write
   failure stops before `gh` runs. This makes an enterprise hostname recognizable
   even if a later provider step fails.
3. Creates the final home private. It does not create a secret staging home.
4. Runs `gh auth login --hostname <hostname> --web --git-protocol https
   --insecure-storage` with the final home as `GH_CONFIG_DIR`.
5. Writes exactly `Y\n` to the child's stdin to accept Git credential-helper
   configuration, then closes stdin. This explicit answer is part of the
   operator's onboarding command. No hidden terminal input remains before the
   device URL and code.
6. Emits the sign-in URL and one-time code through the existing first-class tee
   delivery seam. It does not log or persist the code after the ceremony.
7. Waits for provider completion, operator cancellation, or the provider/device
   deadline. A deadline bounds waiting and records `device_flow_expired`; it
   does not classify the credential.
8. Rechecks file type and private modes, then runs
   `gh auth status --active --hostname <hostname>`,
   `gh api --hostname <hostname> -i user --jq .login`, and
   `gh config get git_protocol --host <hostname>` in the same home.
9. If `--remote` is present, runs `git ls-remote <sanitized-URL> HEAD` with the
   same `GH_CONFIG_DIR`, closed stdin, and `GIT_TERMINAL_PROMPT=0`.
10. Updates the profile binding and records success only after the checks pass.
    A binding- or event-write failure after provider mutation leaves
    `present_but_unverified`; it does not roll secret bytes back.

The command does not run `--with-token` or `gh auth status --show-token`. The
argument parser refuses `--api-key`, `--token`, token environment input, and
identity flags on this host-local ceremony.

**R16 / A16.** Given the recorded real pre-device transcript fixture, when the
real installed `gh` runs under a non-TTY fixture with one supplied `Y\n`, then a
device URL and code become observable without another stdin read. The captured
argv contains the required flags and omits `--with-token`. Cancellation and
deadline branches bank no Tightbeam copy and record their exact causes.

`--replace` is rotation. It runs the same provider-owned flow in the same final
home; it creates no backup. If provider login fails before `gh` changes its
authority, the prior authority remains. If `gh` changes authority and a later
check fails, the state is `present_but_unverified`; Tightbeam does not restore
secret bytes. The repair is rerun `--replace`, choose another profile, or revoke.

Local revocation is:

```text
tightbeam revoke github [--hostname github.com] [--profile default]
                        [--account <login>]
```

It acquires the same writer lock and invokes `gh auth logout --hostname <host>
--user <account>` against the final home. The account comes from the current
non-secret provider observation or an exact `--account` argument. If neither
designates one account, the command refuses as `github-account-required`; it
does not open an interactive account chooser. It records the observed account
and result without reading the file. After success it marks the profile binding
revoked and retains the non-secret last account. A repeat for that exact
hostname, profile, and account returns idempotent `revoked` from the tombstone
without invoking `gh` again. GitHub-side OAuth grant revocation remains a human
action in GitHub settings; the command says so.

**R17 / A17.** Given a live profile, when rotation succeeds, fails before write,
and fails after provider write in three fixtures, then respectively the new
account is live, the old account remains live, and the profile reports
`present_but_unverified`; no backup exists. Given two concurrent writers, one
owns the lock and the other refuses before invoking `gh`. Repeated local
revocation emits one mutation event and returns `revoked` both times.

### 5. Health, readiness, and doctor

Each authorization check runs against the current elected home. Cached
observations support display and audit only. Authorization does not use an age
threshold or a cached `live` value.

Probe order is: projection election, host reachability, `gh` path, storage
metadata, `gh auth status --active --hostname <hostname>`,
`gh api --hostname <hostname> -i user --jq .login`,
`gh config get git_protocol --host <hostname>`, then optional `git ls-remote`.
An absent `hosts.yml` with a matching revocation tombstone is `revoked`; the
same absence without that tombstone is `needs_onboarding`. After valid storage,
the adapter captures both provider checks before classification unless the
process cannot start or times out. The API status line is the sole 401/403
authority; raw headers and body remain inside the redaction boundary. A 200
response plus active-status disagreement is `unknown`, not `live`. Otherwise
the first non-live phase after the API classification determines state and
cause. Each provider or Git probe has PR20's 15-second wait bound, uses closed
stdin, and returns `unknown` on timeout; the bound never decides credential
validity. The optional remote probe also sets `GIT_TERMINAL_PROMPT=0` and proves
repository Git readiness; API liveness alone does not.

Session/project readiness and `tightbeam doctor --json` expose:

- kind `github`;
- machine, profile, hostname, and account when observed;
- `gh` executable path;
- protocol;
- state, failed phase, cause, principal, observation id, and observation time;
- sanitized remote when one was checked;
- exact repair command.

They omit the credential-home path, token location, raw provider output, and
secret-shaped bytes. Doctor checks GitHub when a project remote classifies as a
configured GitHub hostname or when the operator names a profile/hostname check.
No GitHub remote and no explicit check produces no GitHub failure.

**R18 / A18.** Given no project remote, a non-GitHub remote, and each GitHub
health state, when human and JSON doctor modes run, then the first two do not
fail GitHub readiness, each GitHub case shows the required non-secret fields and
repair, and only current `live` passes. Rust and Elixir output agree.

### 6. Migration, compatibility, and rollback

Upgrade performs metadata-only detection of the legacy bank. It may `lstat` the
legacy path; it does not open `hosts.yml`. Presence records
`legacy_github_bank_present` with cause and principal. Runtime projection and
probes ignore the bank and do not fall back to it.

The migration procedure is:

1. Select a profile and run the compatible onboarding command.
2. Verify current health and any required remote from the new home.
3. Update the relevant archetype manifests to elect the profile.
4. Apply identity through the existing identity-apply path; pinned existing sessions keep their prior identity
   until the existing apply/session-replacement law moves them.
5. Revoke and remove the legacy credential through the old version's provider
   command or an explicit operator action. 0.2.0 reports residue until it is
   absent; it does not sweep it.

No migration step copies a credential. A host can remain usable for non-GitHub
work while migration is incomplete; the operation rule refuses GitHub work with
the next exact step.

CLI compatibility keeps `tightbeam onboard github --hostname ... --remote ...`
and the internal `github-auth-check` entry point. The internal command becomes
the typed check used by compiled law; calling it directly returns the same safe
state and remedy but grants no bypass. PR20's tests move to the new homes and law
fixtures; they are not deleted.

Rollback has three independent meanings:

- **Identity rollback:** elect the prior profile in the manifest and apply the
  prior identity revision. No credential bytes move.
- **Product rollback:** the older product ignores the 0.2 credential homes;
  0.2 leaves them untouched, and a later return to 0.2 reuses them after a live
  probe. No automatic downgrade migration exists.
- **Credential rollback:** unsupported by design. Secret backups would violate
  I1. The operator reselects an existing profile, rotates in place, or revokes.

**R19 / A19.** Given a legacy sentinel bank and an empty new profile, when 0.2
starts, projects, doctors, and attempts GitHub work, then no process opens or
copies the legacy file; doctor reports residue and the operation refuses with
onboarding. After new onboarding and election, operations use only the new home.
Identity and product rollback leave both inode sets unchanged.

### 7. Audit and failure ownership

The operation's host owns its `gh`, Git, filesystem, and network failures. The
gateway records the safe result but does not rerun the probe from another host.
If observation recording fails, the local rule changes the result to
`rule_runtime_failure`, denies before execution, and adds
`observation_record_failed` to safe stderr. A network operation never runs
without its current observation row.

Each refusal uses this shape:

```text
[rule: github-network-auth-required] GitHub operation refused:
machine=<machine> profile=<profile|none> hostname=<hostname> phase=<phase>
state=<state> cause=<safe cause> principal=<principal>.
Repair: <exact command>. Do not paste a PAT into an agent.
```

The rule emits no refusal when satisfied. Its allow-path event is the capability
observation already produced by the probe; it adds no acknowledgment row.

**R20 / A20.** Given event-log success and failure fixtures, when a non-live or
live operation runs, then an event-write failure denies before execution. The
successful non-live fixture records one safe observation and one named refusal;
the failed fixture says the observation could not be recorded. Neither output
contains raw detail. A live operation with a recorded observation prints no rule
text.

## Acceptance

The implementation is ready for code review only when these fixture groups pass
against the real built CLI. Hand-written ideal provider output does not satisfy
the boundary-capture rows.

| Fixture group | Required cases | Clauses |
|---|---|---|
| `github-kind-storage` | private, permissive, absent, empty, symlink, hard link, directory, device; regeneration and assimilation preservation | R1, R11, R12 |
| `github-projection` | local and satellite hosts; elected, unelected, desk, overlay collision; gateway credential cannot satisfy satellite | R2, R5, R13 |
| `github-rule-compile` | rule present/absent/amended; Claude/Codex hook wiring; unarmed failure; named refusal | R3, R14 |
| `github-command-vector` | direct Git verbs; `gh repo/pr/issue/api`; env/wrapper prefixes; connectors; nested shells; named remotes; submodules; userinfo; mixed case; leading redirects; push value options; prose and here-doc negatives | R6, R7, R15 |
| `github-health` | missing CLI, unelected, missing, hollow, live, stale/rejected credential observed through provider 401, provider 403, git failure, timeout, transport error, provider-check disagreement, unrecognized response, revoked, present-but-unverified | R4, R18 |
| `github-device-real-response` | sanitized capture from the installed `gh`: pre-device Git-auth prompt, one explicit `Y\n`, URL/code emission, completion and cancellation shapes | R16 |
| `github-multiple-identities` | two profiles on one host and one on a satellite, concurrent probes and writer collision | R5, R9, R17 |
| `github-redaction` | each token family, URL userinfo, stdout, stderr, remote, repair, JSON, events, doctor; compile-fail raw detail | R8, R10, R20 |
| `github-migration` | legacy bank untouched, no fallback, new onboarding/election, identity rollback, product rollback | R19 |

The real-response fixture records: `gh` version and binary hash; host OS; exact
sanitized argv; stdout/stderr channel and order; exit status; capture time; and
the SHA-256 of the sanitized fixture. If capture requires a human or live
credential, the automated test skips with that requirement named. The release
gate still requires one authorized real ceremony before 0.2.0 claims installed
GitHub onboarding works. Tests must not fabricate that receipt.

PR20 preservation check: the implementation maps each reviewed 60bda7e behavior
to one fixture above. The code reviewer compares the old and new vector by name.
Deletion or weakening requires a clause in this spec; refactor fidelity alone
does not authorize it.

## Open Questions

1. **NON-BLOCKING — two profiles in one session.** `GH_CONFIG_DIR` is
   single-valued. V1 chooses one profile per session. A future design may add an
   explicit per-operation profile, but it cannot call `gh auth switch` on a
   shared store.
2. **NON-BLOCKING — remote OAuth grant revocation API.** V1 removes local
   authority through `gh auth logout` and tells the human to revoke the GitHub
   grant in provider settings. A provider API for remote revocation needs its
   own evidence and scope review.
3. **NON-BLOCKING — additional tool frontends.** V1 covers supported Bash
   pre-tool-call seams. A future non-Bash Git tool must expose an equivalent
   pre-execution dispatch edge before it can claim this guard.
4. **NON-BLOCKING — account rename.** V1 treats a renamed login observed from
   the same profile as changed non-secret metadata. If provider behavior makes
   that ambiguous, the operator creates a new profile and re-onboards.
5. **BLOCKING: none.** The MVP boundary, authorities, failure states, fixtures,
   migration, and rollback are specified.
