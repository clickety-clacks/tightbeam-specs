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

Independent review `att_b4b6bc73-e91e-4c04-b940-5da7f6009d3e` requested four
changes against revision `367274b3a203ba0e6c0f23d6740357337f26ded4`; report
`art_336143cb` is the durable analysis. This revision closes B1 with the exact
tool-call law/ABI below, B2 with ordinary authenticated dispatch, B3 with the
named inert-residue state, and B4 with deterministic `gh` hostname precedence.

## Goal

Make authenticated GitHub operations a host-local, account-scoped capability
on 0.2.0. Keep PR20's reviewed command classifier, probes, redaction, readiness,
and fixture behavior. Replace its three 0.1 seams:

1. An archetype provisioning election projects the selected GitHub credential
   home into an agent environment.
2. Org-authored dispatch-rule law guards GitHub operations before execution and
   names each refusal.
3. A first-class `github` credential kind points at one `gh`-owned credential
   home as 0.2.0's active authority. Tightbeam creates no secret copy and treats
   any pre-existing 0.1.9 residue as inert.

The maxim is: **the human chooses the GitHub identity, `gh` owns its active
secret home, the archetype elects its projection, and compiled law refuses an
unready network operation by name.**

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
- **Hostname** — the GitHub hostname supplied to onboarding, selected by a `gh`
  command, or parsed from a remote. `github.com` is the CLI default. An explicit
  `gh` selector is GitHub evidence even before onboarding. For Git commands, a
  non-default hostname is GitHub evidence only after onboarding recorded a
  binding for that machine; the substrate does not guess which arbitrary Git
  remotes run GitHub. Recognition never selects the profile used for
  authorization. Normalization lowercases the parsed host, removes one terminal
  DNS dot, and preserves an explicit numeric port. A hostname-only selector
  containing a scheme, userinfo, path, empty host, or malformed port returns
  `malformed_tool_call`.
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
  `{machine, profile, hostname}`. Onboarding is its only create seam and the
  only seam that changes hostname/account selection; local revocation may only
  transition an existing binding to `revoked`. It records the selected
  hostname, the last observed account, state, current mutation attempt when
  present, cause, principal, and time. It contains no credential path or
  provider output. The operation classifier uses the machine-wide hostname
  index across binding states to recognize configured enterprise GitHub hosts
  without opening `hosts.yml`; the elected profile still supplies the only
  binding and home used for authorization.
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
- **Inert legacy residue** — a secret-bearing file left at PR20's 0.1.9 path
  `<base_dir>/auth/github/gh`. It is neither active authority nor fallback while
  0.2.0 runs. Only the operator removes it or an older product reactivates it
  after product rollback.
- **Principal** — the user or session whose command caused onboarding,
  revocation, probing, projection, or refusal. The ordinary authenticated
  Tightbeam dispatch resolves it from a session credential or a validated
  global identity flag; an OS username or caller-supplied event field cannot.
  Each capability marker records it.

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

### I1. One active secret authority

For each `{machine, profile}`, `gh` writes and rotates one provider-native
credential home in place. Tightbeam stores only non-secret observations and
profile bindings. A projection, migration, health check, rotation, revocation,
home regeneration, assimilation, or rollback copies no secret and selects no
second active authority. During migration, an untouched inert legacy residue
may coexist until the operator removes it; 0.2.0 never projects, probes, opens,
or updates that residue.

**R1 / A1.** Given a sentinel secret in the profile fixture, when onboarding,
projection, probing, rotation, revocation, regeneration, remote provisioning,
doctor, and rollback fixtures run independently, then any remaining sentinel
exists only in the fixture provider's final `hosts.yml` or the fixture's
pre-existing inert legacy residue. No operation copies the sentinel between
those paths. Source scans and captured argv, env, events, stderr, stdout, JSON,
and artifacts contain no sentinel.

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

`ambiguous_hostname`, `projection_override`, `malformed_tool_call`, and
`rule_runtime_failure` are operation-check results, not credential health
states. Each refuses before the proposed command starts.

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
git-unready, unknown, unelected, ambiguous-hostname, projection-override,
malformed-tool-call, and rule-runtime failures refuse. Each refusal names the
rule, machine, profile, hostname, failed phase, state, cause, principal, and
exact repair. It omits secret paths and token bytes.

The check and action are intentionally two steps, not an atomic transaction. A
provider-side change after the check may make the action fail. The guard records
what it observed; it does not claim the later operation succeeded.

**R6 / A6.** Given a marker file written by fixture `git` before network work,
when direct, wrapped, connector-separated, and nested-shell GitHub operations
run under each non-live or operation-refusal state, then the marker remains
absent and exit is a named rule refusal. Under `live`, the marker appears. A
concurrent provider revocation after the check causes the operation fixture to
fail without changing the earlier observation to a false claim of success.

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
refusal, inert-residue detection, and rule-runtime failure write capability events
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
event. A session-local ceremony records the credential's session principal; a
satellite ceremony dispatched with authenticated `--as-user owner` records
`user:owner`. A missing or invalid dispatch principal stops before provider
mutation.

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
7. Query the non-secret machine hostname index or one elected-profile binding,
   and create or update bindings through the one binding API; only its
   create/update calls mutate binding state.

The machine hostname index returns only a set of normalized hostnames. It omits
profile names, accounts, states, and recency, so recognition cannot choose an
identity.

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
with reserved names. `TIGHTBEAM_MACHINE`, `TIGHTBEAM_PRINCIPAL`,
`TIGHTBEAM_GITHUB_PROFILE`, `GH_CONFIG_DIR`, `GH_TOKEN`, `GITHUB_TOKEN`,
`GH_ENTERPRISE_TOKEN`, and `GITHUB_ENTERPRISE_TOKEN` are reserved. Provisioning
removes inherited values for the four token variables and never projects them.
It always writes the registered local machine and authenticated session
principal to `TIGHTBEAM_MACHINE` and `TIGHTBEAM_PRINCIPAL`. An election writes
the profile to `TIGHTBEAM_GITHUB_PROFILE` and the exact host-local
credential-home path to `GH_CONFIG_DIR`. No election removes the latter two
variables. A colliding overlay is a named configuration refusal. An executable
tool command that assigns or unsets any reserved variable directly or through
`env` refuses as `projection_override` before its child starts.

Remote projection resolves the same logical `{machine, profile}` against the
remote host's base directory and quotes the path once in the SSH command. It
does not project the gateway path.

**R13 / A13.** Given workshop-with-election, workshop-without-election,
desk-without-election, desk-with-election, colliding-overlay, local, and remote
manifest fixtures plus inherited token variables and inline reserved-variable
assign/unset vectors, when manifests load, environments project, and tool calls
classify, then the first three valid shapes produce the specified env, the two
invalid shapes refuse by name, inherited token variables are absent, each inline
override refuses as `projection_override`, and remote output contains only the
remote path.

### 3. Compiled operation law

This feature extends the dispatch-rule files at `identity/rules/*.toml`; it does
not add predicate syntax to the existing `identity/rails/*.toml` regex gate.
`verb = "tool-call"` is a synthetic dispatch edge compiled into a
harness-native pre-tool-call hook rather than a gateway verb handler. The one
shipped law is `identity/rules/github.toml` with exactly the contents below:

```toml
[[rule]]
name = "github-network-auth-required"
verb = "tool-call"
edges = ["pre-execution"]
actors = { capability = "Bash" }
text = "GitHub network work requires the elected host profile to pass a current check."

[rule.check]
handler = "github-network-auth-v1"
abi = 1
timeout_ms = 60000
fallback_repair = "tightbeam doctor --json"
returns = [
  "not_applicable", "live", "profile_not_elected", "missing_cli",
  "needs_onboarding", "hollow", "expired", "insufficient_scope",
  "git_unready", "revoked", "present_but_unverified", "unknown",
  "ambiguous_hostname", "projection_override", "malformed_tool_call",
  "rule_runtime_failure"
]

[rule.check.effects]
not_applicable = "allow"
live = "allow"
profile_not_elected = "deny"
missing_cli = "deny"
needs_onboarding = "deny"
hollow = "deny"
expired = "deny"
insufficient_scope = "deny"
git_unready = "deny"
revoked = "deny"
present_but_unverified = "deny"
unknown = "deny"
ambiguous_hostname = "deny"
projection_override = "deny"
malformed_tool_call = "deny"
rule_runtime_failure = "deny"
```

The dispatch-rule loader accepts `actors` only on `verb = "tool-call"`. V1
accepts exactly `{ capability = "Bash" }`. It accepts `check.handler` only on
that edge, resolves the handler through a product-owned closed registry, and
requires ABI `1`. `returns` must equal the handler's registered token set;
`effects` must map each token once to `allow` or `deny`; `timeout_ms` must be an
integer from 1 through 60000; `fallback_repair` must be the non-empty safe
display command used only when the handler renders no valid envelope. The
compiler stores it as redacted display data and never executes it. Each
tool-call rule must map `rule_runtime_failure` and `malformed_tool_call` to
`deny`; malformed input and a missing checker cannot become policy-controlled
authorization facts. A tool-call rule
rejects `deny_when`, a script check, a gateway remedy, an unknown key, handler,
ABI, token, effect, edge, or actor selector at identity load as
`tool-call-rule-invalid`. The existing gateway dispatch-rule shapes and the
existing rails loader remain unchanged.

The compiler evaluates `actors` against each pinned archetype manifest. A
capability selector reads the selected harness adapter's declared tool set; it
does not infer capability from guidance text. A matching rule contributes its
normalized bytes, handler registration, and the archetype manifest revision to
the identity hash and harness artifact. A non-matching archetype receives no
entry. The generated entry invokes this exact internal command on the session
host:

```text
tightbeam dispatch-rule-check
  --rule github-network-auth-required
  --handler github-network-auth-v1
  --abi 1
  --identity-sha <pinned-identity-sha>
```

The command reads exactly one supported harness PreToolUse JSON document from
stdin. The document must identify tool `Bash` and carry a string
`tool_input.command`; any other shape returns `malformed_tool_call`. The command
resolves the session key, session principal, gateway URL, and gateway recording
credential through the ordinary `.tightbeam-session` credential. It reads the
registered machine and projected principal from `TIGHTBEAM_MACHINE` and
`TIGHTBEAM_PRINCIPAL`, the optional elected profile from
`TIGHTBEAM_GITHUB_PROFILE`, and the provider home from `GH_CONFIG_DIR`. It
verifies that the projected principal equals the session credential's principal
and that the supplied identity SHA equals the session's pinned revision, then
performs structural classification locally. A Git candidate on a non-default
hostname reads the current machine-wide hostname index through the binding API;
after recognition, health reads only the elected profile's binding and home.
The gateway authorizes each read with the same session credential. An
unavailable or unauthorized required read returns `rule_runtime_failure`; it
does not fall back to a cached host list. A `not_applicable` call performs no
gateway or provider I/O. No actor, machine, profile, or identity field from
tool-call JSON is authoritative.

The registered handler returns this typed fact envelope for one classified
target:

```text
ToolCheckMaterialV1 {
  state: <one declared return token>,
  operation_class: not_applicable | gh | git,
  machine: <registered machine>,
  profile: <elected profile | none>,
  hostname: <normalized target | none>,
  phase: <classifier | projection | storage | provider | git | recording>,
  cause: <safe cause>,
  principal: <authenticated session principal>,
  repair: <exact safe command | none>,
  observation_ids: [<durable observation id>]
}
```

The handler does not return allow or deny. The generic rule executor maps
`state` through the compiled `effects` table. Material whose mapped effect is
`allow` uses `repair: none`; material whose mapped effect is `deny` carries one
non-empty redacted repair command. The wrapper uses `TIGHTBEAM_MACHINE`,
`TIGHTBEAM_PRINCIPAL`, the optional profile, the rule name, and
`fallback_repair` to render a safe refusal when the internal command returns no
valid envelope; it does not trust values inside tool-call JSON.

The generic executor processes executable commands and target hostnames in
source order. It requests one material envelope, maps its state through law,
and stops at the first `deny`; it requests the next target only after `allow`.
Each contacted hostname requires one current recorded observation. The internal
command exits 0 with empty stdout and stderr only after each material envelope
maps to `allow`. It exits 2 and writes the safe named refusal to stderr on
`deny`. The compiled wrapper turns command-not-found, timeout, signal, an
undeclared token, invalid envelope, identity mismatch, or any other exit into
synthetic `rule_runtime_failure` material, maps it through the required effect,
emits the rule's safe fallback remedy, and exits 2. Thus product code reports
facts, org law chooses the effect, and no nonzero path can become allow.

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
identity, exact argv, ABI, reserved environment, stdin shape, and effect table,
then later enforce the vector. Given each invalid schema case named above, the
identity load refuses as `tool-call-rule-invalid`. Given an unarmed hook,
session readiness refuses as `github-rule-unarmed` before an agent tool call;
given the rule removed from identity, the compiler emits no GitHub entry.

The classifier preserves the reviewed 60bda7e behavior and tests. It adds
configured GitHub hostnames from the machine-wide hostname index instead of
hardcoding only `github.com`. That index is recognition evidence, not health or
profile selection; the elected profile's current probe still decides
authorization. The classifier removes URL userinfo before using a remote in a
probe or remedy. It resolves named remotes and submodule URLs from local
configuration without contacting a server.

For each executable `gh repo`, `gh pr`, `gh issue`, or `gh api` segment, the
classifier resolves exactly one target hostname in this order:

1. Reject an assignment or unset of a reserved projection/token variable as
   `projection_override`.
2. Use an explicit host-qualified command selector: `gh api --hostname`,
   `-R`/`--repo [HOST/]OWNER/REPO`, or a host-qualified repository or GitHub URL
   in the command's repository position. An unqualified explicit repository
   skips local-repository inference and uses the effective `GH_HOST`, then
   `github.com`.
3. Otherwise use the effective `GH_REPO`. A host-qualified value supplies the
   hostname. An unqualified value uses the effective `GH_HOST`, then
   `github.com`. The closest executable-segment assignment, including `env`,
   wins over the inherited process value; the last assignment to the same name
   in that prefix wins.
4. Otherwise, when the command operates on the current repository, inspect Git
   configuration without network access. Exactly one
   `remote.<name>.gh-resolved=base` marker selects that remote and makes its
   syntactically valid hostname explicit GitHub evidence. With no marker, the
   candidate set is each `remote.<name>.url` whose normalized hostname is
   `github.com` or appears in the machine-wide binding hostname index. Use the
   hostname when that non-empty set normalizes to one hostname. Conflicting
   markers or different candidate hostnames return `ambiguous_hostname`. An
   empty set continues to step 5.
5. Otherwise use the effective `GH_HOST`, then `github.com`.

A stronger selector ignores a different lower-precedence value. Two different
normalized hostnames at the same winning rank return `ambiguous_hostname`
instead of probing either. `github.com` and any hostname selected by an explicit
`gh` selector are GitHub targets even without a profile binding. A hostname
inferred only from a Git remote is a GitHub target when it is `github.com` or
appears in the machine-wide hostname index. A selected but unbound enterprise
hostname reaches the current probe for the elected profile and returns
`needs_onboarding`; it never becomes `not_applicable` and never selects the
profile whose binding supplied recognition evidence.

**R15 / A15.** Given `github.com`, a configured or explicit unbound enterprise
hostname, look-alike Git remotes, mixed case, trailing dot, scp syntax,
ssh/http/https syntax, userinfo, relative submodules, named non-GitHub remotes,
each selector rank above, stronger/lower conflicts, same-rank conflicts, and a
reserved-variable override plus each malformed hostname-only shape, when the
classifier runs, then it selects the specified exact hostname or named refusal.
An explicit unbound enterprise host returns `needs_onboarding`; a same-rank
conflict returns `ambiguous_hostname`; a reserved override returns
`projection_override`; a malformed selector returns `malformed_tool_call`. Safe
output contains no userinfo.

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

The command keeps Tightbeam's ordinary global identity path. Inside a session
workdir, the session credential supplies the session principal. Outside one, a
human uses the existing authenticated `--as-user <id>` path; `--as <role>` is
valid only when ordinary dispatch resolves that role to a session principal.
The gateway validates either identity before the command takes the writer lock.
The command does not infer an OS user and does not accept a principal inside a
profile-binding or event payload.

On a satellite, `gh` and filesystem work stay local. The command sends only the
non-secret machine, profile, hostname, account observation, cause, and outcome
through ordinary authenticated dispatch to the gateway's profile-binding and
capability-event APIs. The gateway verifies that the dispatch principal may act
for the registered machine. A dispatch or binding failure before provider
mutation stops the ceremony. A durable-write failure after provider mutation
returns `present_but_unverified`; the provider home remains the only active
authority and no secret crosses the wire.

The command acquires a process-bound exclusive lock for `{machine, profile}`.
The operating system releases the lock when the process exits. A second writer
refuses as `github-credential-busy`, names the first principal when known, and
asks the operator to retry after that process exits. A readiness probe takes a
non-blocking shared lock. If a writer holds the lock, the probe returns `unknown`
without inspecting the home and denies the operation.

Without `--replace`, the command first runs current health. A live matching
account and passing optional remote probe returns an idempotent success without
starting login. A binding with an `onboarding` attempt and a present authority
runs the post-login checks in steps 8–10 once; success clears the attempt without
another login, while failure refuses with the `--replace` repair. A supplied
`--account` must equal the account observed after login; mismatch returns
`account_mismatch` and `present_but_unverified`. The substrate does not switch
accounts to satisfy the argument.

For device login, the command:

1. Validates the profile and final home without opening secret contents.
2. Creates an absent profile binding with state `needs_onboarding`, then sets
   its mutation attempt to `onboarding` without replacing a prior state or
   account. A binding-write failure stops before `gh` runs. This makes an
   enterprise hostname recognizable even if a later provider step fails.
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
10. In one gateway transaction, clears the mutation attempt, updates the
    binding with the observed live state/account, and appends the success event.
    It reports success only after that transaction commits. A transaction
    failure after provider mutation leaves the prior binding/attempt, which
    health reports as `present_but_unverified`; it does not roll secret bytes
    back.

The command does not run `--with-token` or `gh auth status --show-token`. The
argument parser refuses `--api-key`, `--token`, and token environment input.
The global authenticated identity flags remain available as specified above.

**R16 / A16.** Given the recorded real pre-device transcript fixture, when the
real installed `gh` runs under a non-TTY fixture with one supplied `Y\n`, then a
device URL and code become observable without another stdin read. The captured
argv contains the required flags and omits `--with-token`. Cancellation and
deadline branches bank no Tightbeam copy and record their exact causes. Given a
session principal, an authenticated satellite `--as-user` principal, a missing
principal, and an invalid principal, only the first two reach the writer lock
and each durable row names the dispatch-resolved principal.

`--replace` is rotation. It runs the same provider-owned flow in the same final
home; it creates no backup. If provider login fails before `gh` changes its
authority, the command clears the mutation attempt and the prior authority and
binding state remain. If `gh` changes authority, file metadata indicates a
possible change, or a later check fails, the state is
`present_but_unverified`; Tightbeam does not restore secret bytes. The repair is
rerun `--replace`, choose another profile, or revoke.

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
same absence without that tombstone is `needs_onboarding`. A present authority
with an `onboarding` attempt or `present_but_unverified` binding returns
`present_but_unverified` without provider/network I/O; only an explicit
onboarding or rotation command may clear it. After valid storage and no pending
mutation, the adapter captures both provider checks before classification
unless the process cannot start or times out. The API status line is the sole
401/403 authority; raw headers and body remain inside the redaction boundary. A
200 response plus active-status disagreement is `unknown`, not `live`.
Otherwise the first non-live phase after the API classification determines
state and cause. Each provider or Git probe has PR20's 15-second wait bound,
uses closed stdin, and returns `unknown` on timeout; the bound never decides
credential validity. The optional remote probe also sets
`GIT_TERMINAL_PROMPT=0` and proves repository Git readiness; API liveness alone
does not.

Session/project readiness and `tightbeam doctor --json` expose:

- kind `github`;
- machine, profile, hostname, and account when observed;
- `gh` executable path;
- protocol;
- state, failed phase, cause, principal, observation id, and observation time;
- sanitized remote when one was checked;
- exact repair command.

They omit the credential-home path, token location, raw provider output, and
secret-shaped bytes. V1 doctor checks GitHub when a project remote classifies as
a configured GitHub hostname. No GitHub remote produces no GitHub failure.

**R18 / A18.** Given no project remote, a non-GitHub remote, and each GitHub
health state, when human and JSON doctor modes run, then the first two do not
fail GitHub readiness, each GitHub case shows the required non-secret fields and
repair, and only current `live` passes. Rust and Elixir output agree.

### 6. Migration, compatibility, and rollback

Upgrade performs metadata-only detection of inert legacy residue. It may
`lstat` the legacy path; it does not open `hosts.yml`. Presence records state
`inert_legacy_residue` with cause and principal. Runtime projection and probes
ignore the residue and do not fall back to it.

The migration procedure is:

1. Select a profile and run the compatible onboarding command.
2. Verify current health and any required remote from the new home.
3. Update the relevant archetype manifests to elect the profile.
4. Apply identity through the existing identity-apply path. Pinned existing
   sessions keep their prior identity until the existing
   apply/session-replacement law moves them.
5. Revoke and remove the legacy credential through the old version's provider
   command or an explicit operator action. 0.2.0 reports residue until it is
   absent; it does not sweep it.

No migration step copies a credential. A host can remain usable for non-GitHub
work while migration is incomplete. New onboarding asks the provider for a new
credential in its final home; it does not derive that credential from the
residue. While both files exist, 0.2.0 selects only the new home as active
authority and reports the residue as `inert_legacy_residue`. The operation rule
refuses GitHub work with the next exact step until the new home is live.

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

**R19 / A19.** Given a sentinel in inert legacy residue and an empty new
profile, when 0.2 starts, projects, doctors, and attempts GitHub work, then no
process opens or copies the residue; doctor reports `inert_legacy_residue` and
the operation refuses with onboarding. After the provider issues a distinct new
credential and the profile is elected, operations use only the new home while
the residue remains inert. Identity and product rollback leave both inode sets
unchanged.

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
text. The fixture sends the exact ABI-1 stdin through the compiled Claude and
Codex entries and proves the authenticated session credential, not tool JSON,
owns each row.

## Acceptance

The implementation is ready for code review only when these fixture groups pass
against the real built CLI. Hand-written ideal provider output does not satisfy
the boundary-capture rows.

| Fixture group | Required cases | Clauses |
|---|---|---|
| `github-kind-storage` | private, permissive, absent, empty, symlink, hard link, directory, device; regeneration and assimilation preservation | R1, R11, R12 |
| `github-projection` | local and satellite hosts; elected, unelected, desk, overlay collision; inherited token removal; inline reserved-variable assign/unset; gateway credential cannot satisfy satellite | R2, R5, R13 |
| `github-rule-compile` | exact specimen; each invalid schema case; registered handler/ABI/token/effect validation; rule present/absent/amended; exact argv/stdin/env; Claude/Codex hook wiring; unarmed and runtime failures; named refusal | R3, R14, R20 |
| `github-command-vector` | direct Git verbs; `gh repo/pr/issue/api`; each hostname selector rank and malformed hostname-only shape; stronger/lower and same-rank conflicts; explicit unbound enterprise host; env/wrapper prefixes; connectors; nested shells; named remotes; submodules; userinfo; mixed case; leading redirects; push value options; prose and here-doc negatives | R6, R7, R15 |
| `github-health` | missing CLI, unelected, missing, hollow, live, stale/rejected credential observed through provider 401, provider 403, git failure, timeout, transport error, provider-check disagreement, unrecognized response, revoked, present-but-unverified; pending onboarding with an absent or present home | R4, R18 |
| `github-device-real-response` | sanitized capture from the installed `gh`: pre-device Git-auth prompt, one explicit `Y\n`, URL/code emission, completion and cancellation shapes; session and authenticated satellite user principals; missing/invalid principal pre-mutation refusal | R10, R16 |
| `github-multiple-identities` | two profiles on one host and one on a satellite; enterprise host recognized only through a non-elected profile while the elected profile returns `needs_onboarding`; the same host with no election returns `profile_not_elected`; concurrent probes and writer collision | R5, R9, R15, R17 |
| `github-redaction` | each token family, URL userinfo, stdout, stderr, remote, repair, JSON, events, doctor; compile-fail raw detail | R8, R10, R20 |
| `github-migration` | inert legacy residue untouched and reported, no fallback or copy, distinct provider-issued new credential, one active authority, new election, identity rollback, product rollback | R1, R19 |

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
5. **NON-BLOCKING — explicit doctor selector.** V1 checks project remotes. A
   later CLI may add an operator-selected machine/profile/hostname doctor check
   after its exact syntax and authorization are specified.
6. **BLOCKING: none.** The MVP boundary, authorities, failure states, fixtures,
   migration, and rollback are specified.
