# Spawned-session identity isolation

Status: F14 adapter-custody amendment draft after `att_592009bf`; implementation beyond the isolated adapter spike is blocked by OQ-1  
Work item: `wi_b8802849-0d10-475b-b5e6-2458842c9c11`  
Custody-recovery assignment: `asg_3e7d1e5e-6afe-4731-8908-8faf690e1fbc`  
Prior F8 amendment assignment: `asg_6cca1e12-2dd6-45c6-9235-45830a8f5af2`  
F8 authority: owner Option A `att_37069ca1-2639-4e62-978c-309e1b939711`, custody ruling
`att_dfa90221-6593-42b3-ad68-8de75377f1b7`, and changes-requested verdict
`att_534d5e79-c9e9-4053-9584-acba0128b0ff`  
F8 successor review: changes-requested `att_abccf4d6-a9fc-40d4-825c-359f687d9f09`;
report `art_37482b6d` SHA-256
`4fcd86c3032c4ebfe49201de052758276fa4e6e3bd056e9529e9c5fddad722a3`  
Custody-recovery authority: conditional verdict `att_3df70905-ca8c-4974-8a02-0b46415c9570`  
F13-F16 amendment authority: conditional verdict `att_7d4e06a1-90e6-4b31-8771-7fb4c5a0a25c`  
F13-F16 exact-artifact review: changes-requested `att_592009bf`; restored report `art_5ba40ba0`
SHA-256 `73830c05e2ec4434db44cd5688f3766ccfcc4cb19359808a70ef216cb7750b02`  
F14 seam decision: decision request `dr_bee56f9e-be60-482a-a3d3-63dabeb17789` is ruled
`adapter-custody`  
F9-F12 exact-artifact review: changes-requested
`att_5f51503c-e678-4c2f-a847-43e8cd41db08`; report `art_83c07b23` SHA-256
`2d829f2330a0ca5cf62ad66bf19f8091d014b4e2d2cfa8ad87e259320f963d75`  
F7 amendment assignment: `asg_f1e4efa5-928a-4a95-8577-db5eaed05a65`  
F7 authority: owner ruling `att_7c3805df-d256-4ddf-95e3-44046efc0050` and review finding
`att_62013980-633c-4d38-a96a-eb32dd0f673e`  
Successor spec assignment: `asg_5c27fc52-3004-47a9-a64d-51130c94687d`  
Superseded producer assignment: `asg_0298d1db-4a0e-47d8-b64e-68dc4deb480a`  
Direct owner assignment: `asg_4f7d2199-7281-48cb-a2b1-57d2ec64da94`  
Delivery target: Tightbeam `0.2.0`  
Source baseline: `origin/0.1.x` object
`be61cfc98df6b18c0cc280adeca42cba3fbf14b5`  
Canonical product home: `specs/tightbeam/spawned-session-identity-isolation.md`  
Canonical companion recon: `evidence/spawned-session-identity-isolation-recon.md`  
Installation seam: after independent review returns `reviewed-clean`, the opener installs the
review-cleared bytes at those two paths and gives implementation the canonical spec path plus its
exact SHA-256. No draft or custody copy is canonical.

Frozen predecessor artifacts `art_a2c67e69` and `art_75ad8a2d` remain sealed history. Prior F8
review subjects `art_77d4eb7e` and `art_40cfd70e`, and their spec-ready verdict
`att_31b24275-6a2c-48c0-9f6b-b1bd7daf4e34`, are quarantined as inaccessible historical hash
records by `att_3df70905-ca8c-4974-8a02-0b46415c9570`. Review
`att_abccf4d6-a9fc-40d4-825c-359f687d9f09` remains historical evidence about those exact hashes;
it does not supply readable-byte custody. This successor does not claim recovery or sealed custody
of those F8 bytes. Artifact `art_15800663` remains separately quarantined by
`att_54a89fcd-0d06-405d-8617-bc618258ffa6`; no requirement or acceptance claim relies on it.
Reviewed artifacts `art_f818e435` and `art_23ed387d` are immutable changes-requested history
under `att_5f51503c-e678-4c2f-a847-43e8cd41db08`; this successor does not edit or reuse their
recorded homes.

## 1. Goal

Bind each spawned Tightbeam session to one CLI credential independently of the process working
directory.

A CLI invocation that carries session A's complete anchor must either dispatch as session A or
refuse with a named error. A marker in session A's cwd, a parent directory, a nested checkout, or a
moved workdir must not make that invocation dispatch as session B.

The change protects attribution and authorization at the session-to-CLI boundary. It keeps the
existing gateway rules for role, user, and process selection.

The product adds a session-bound marker anchor because deletion and acceptance do not meet the
goal. Deleting session-implied identity breaks the normal agent CLI workflow. Accepting cwd-based
selection preserves silent authority corruption.

The product installs an additive database-shape fence when credential migration starts. A prior
binary refuses that database before agent-turn intake. Adding a compatibility mode for the prior
cwd-based resolver would violate the identity-isolation goal. Accepting that resolver after
migration would restore the unsafe state.

F7 retains host recovery because the owner requires unavailable sessions to recover. Deleting
recovery would make unavailability terminal, and accepting activation without acknowledged rearm
would permit turn intake before the active anchor reaches the harness.

F8 represents an operator-owned returned-rearm-failure fence in the existing `SessionLane` owner.
Deleting the returned `upgrade` or `host_recovery` `session_binding_rearm_failed` result would
violate F7. Accepting a released fence would permit a turn before rearm. A failed
`restart_repair` instead commits the binding unavailable before terminal release. A second
gateway-side admission check loses because `SessionLane` claims the turn first. The typed lane
state in R-48 is the smallest mechanism that preserves the operator-owned returned failure and
makes an intervening claim unrepresentable.

## 2. Non-Goals

1. This work does not isolate hostile processes that run as the same operating-system account. A
   process that can read another session's token can still attempt direct credential theft.
2. This work does not change which roles a session holds.
3. This work does not grant `--as-process` to a session token.
4. This work does not change the rule that a session can use `--as-user` only for its owner.
5. This work does not change organization-token selection of an explicit role, user, or process.
6. This work does not change TLS, gateway host authentication, or organization-token storage.
7. This work does not use cwd as a confinement boundary. A correctly anchored session can run the
   CLI from a handed-off worktree. Its identity remains the anchored session.
8. This work does not prove that the earlier Eezo no-filing incident used this seam. The controlling
   record attributes that incident to CLI protocol-version skew.
9. This work does not protect an obsolete binary that an operator points at a different or restored
   pre-migration database. The migrated database itself carries the rollback fence.
10. This work does not create physical-base identifiers, host-alias leases, root inventories,
    shared-root custody adjudication, or alias re-registration rules. A derived-root collision
    fails as marker custody or binding mismatch without selecting another session. Physical data
    custody is separate work.
11. This work does not add same-root credential rotation. A relocation whose normalized source and
    destination trusted roots are equal returns a named refusal and changes no session, binding, or
    marker state.

## 3. Terms

**Session credential** — the random `tbs_` bearer token stored for one Tightbeam session. The
gateway database is its authority. The token encodes 24 random bytes as 32 unpadded base64url
characters after the prefix.

**Credential binding** — one database row that associates a session credential with a session key,
credential identifier, generation, registered host, trusted root when available, lifecycle state,
and current status.

**Credential identifier** — a random, non-secret canonical lowercase UUIDv4 for one credential
generation. It detects a marker or anchor assembled from different generations.

**Credential generation** — a positive integer that orders credential tuples within one session.
Each distinct newly prepared tuple uses the next generation. A trusted-root or host change always
requires a new generation. Generation `n + 1` supersedes generation `n` only at the database commit
seam.

**Trusted root** — the normalized absolute workdir path that `Placement` derives for the binding's
session and registered host. Placement lexically normalizes the registered absolute base directory,
then appends `work/<session-digest>`, where `session-digest` is the first 12 lowercase hexadecimal
characters of SHA-256 over the session key. It does not follow a filesystem link. The binding and
registered host define this path. Marker content does not define it.

**Session marker** — the mode-`0600`, non-symlink JSON file at
`<trusted-root>/.tightbeam-session`. Schema version 2 contains `schemaVersion`, `url`, `token`,
`sessionKey`, `credentialId`, `generation`, `host`, and `trustedRoot`. It also contains `createdAt`,
`createdBy`, and `cause` from the credential binding.

**Session anchor** — four session-specific values supplied by the gateway to a harness session:
the absolute marker path, expected session key, expected credential identifier, and expected
gateway URL. The harness exposes them to that session's tool subprocesses as
`TIGHTBEAM_SESSION_FILE`, `TIGHTBEAM_SESSION_KEY`, `TIGHTBEAM_CREDENTIAL_ID`, and
`TIGHTBEAM_SESSION_URL`.

**Per-session turn fence** — the gateway-owned turn-admission exclusion for one Tightbeam
session. The gateway acquires it atomically with the check that the session has no running turn.
While it is held, the gateway records no new turn start and sends no new turn request for that
session. The fence does not reject an otherwise authorized CLI request. A process restart does not
count as fence release or as proof that an anchor reached a harness; R-38 reconstructs the exclusion
before turn intake can reopen for either accepted version-2 database shape.

**Harness rearm acknowledgment** — the gateway's recorded successful return from the request-local
ACP operation that makes the affected harness session ready: `session/load` for its persisted vendor
session, or `session/new` when no persisted vendor session exists. The gateway sends the current
active binding's four anchor values in that same request. `session/fork` does not acknowledge a
migration or host-recovery rearm. OQ-1 still blocks use of a vendor projection until AC-11 proves
the exact carrier.

**Bound session endpoint** — a CLI endpoint value that can be constructed only after a complete
session anchor and marker pass local checks.

**Operator endpoint** — an endpoint selected by the complete `TIGHTBEAM_URL` plus
`TIGHTBEAM_TOKEN` pair or by the provisioned `gateway.json`, when no session-anchor variable is
present.

**Nested marker** — a `.tightbeam-session` file in cwd or a cwd ancestor that is not the exact file
named by the session anchor. A nested marker is not an identity input.

**In-scope ACP lifecycle operations** — the three operations that source baseline `be61cfc9`
issues: `session/new`, `session/load`, and `session/fork`. `session/load` is this baseline's operation
for reopening a persisted vendor session. This specification does not claim or add the newer draft
`session/resume` operation.

**Stale marker** — a marker whose token or generation no longer names the active database binding.

**Fixture gateway** — a gateway backed by an isolated test database and fixture host. It contains
no production session row and no work assignment row.

**Canonical spec set** — the authoritative spec at
`specs/tightbeam/spawned-session-identity-isolation.md` and its read-only provenance companion at
`evidence/spawned-session-identity-isolation-recon.md`. Review and implementation identify the spec
by canonical path and SHA-256.

**Migration-start record** — the write-once `org_settings` row whose key is
`session-binding-migration-started`. Its JSON value has exactly `schemaVersion`, `startedAt`,
`createdBy`, and `cause`. Schema version is `1`, `startedAt` is a positive integer, `createdBy` is
the durable `process:tightbeam` principal, and `cause` is `upgrade`. Its presence means a
credential-binding migration transaction has begun and supported binary rollback is no longer
available.

**Credential provenance digest** — lowercase SHA-256 over the UTF-8 bytes of the credential's
canonical positive-decimal `createdAt`, one NUL byte, `createdBy`, one NUL byte, and `cause`, in that
order. A canonical durable principal label contains no NUL byte.

**Credential-binding schema fence** — the additive `session-binding-v2` row in `schema_stamp`.
An upgraded database contains both its original `model-identity-v1` row and this row. The prior
binary's existing exact shape check refuses a database with more than one row before schema
bootstrap or agent-turn intake. A fresh database created by this release contains only the
`session-binding-v2` row. On upgrade, its `stampedAt` equals the migration-start record's
`startedAt`. On fresh bootstrap, `stampedAt` is the bootstrap time.

**Adapter process incarnation** — the exact source-grounded tuple of adapter key
`{harness, "shared", host}`, `Tightbeam.Acp.Adapter` PID, and the monotonic generation returned by
`Tightbeam.AdapterCoordinator`. The PID owns one `Acp.Conn`. The coordinator monitors that PID,
increments the key's generation when it dies, and starts any successor as a distinct temporary
worker. A tuple with a predecessor PID or generation cannot identify the successor.

**Adapter rearm owner** — the `Tightbeam.Acp.Adapter` process in the current adapter process
incarnation. It owns the ACP connection and serial execution of `session/new` and `session/load`.
For rearm, it also retains the single in-flight or completed result for a retry-request identifier
until the caller records that result or the Adapter dies. `SessionLane` monitors the exact Adapter
PID for the dispatch. `AdapterCoordinator` owns monitoring, generation bump, backoff, and
replacement. `Tightbeam.Gateway` remains a plain composition module and is not assigned a PID or
lifecycle by this specification. Bearer-token authentication remains the principal evidence for
operator-owned `upgrade` and `host_recovery`; the boot path obtains the current Adapter checkout
from `AdapterCoordinator` for substrate-owned `restart_repair`.

**Rearm attempt identity** — the exact tuple of session key, active credential generation, adapter
process incarnation, canonical lowercase UUIDv4 operation-attempt identifier, rearm cause, and
durable principal, plus authentication route `wire` or `boot`. The rearm cause is `upgrade`,
`host_recovery`, or `restart_repair`. The gateway
constructs this tuple after the applicable authentication route and before activation. Each initial
or retry adapter dispatch also carries a canonical lowercase UUIDv4 retry-request identifier.

**Rearm recovery record** — one durable `session_rearm_attempts` current-attempt row plus its
durable `session_rearm_dispatches` receipts. The
attempt row stores the rearm attempt identity, operation, phase, and whether one ledger eligibility
check remains due. Its phase is `guarded`, `pending`, `acknowledged`, or `released`. Each initial or
retry dispatch has one receipt keyed by operation-attempt plus retry-request identifier; its phase
is `prepared`, `dispatched`, `failed`, or `acknowledged`, and it stores its failure envelope or
acknowledgment plus failure-event identifier. The record has one mutation seam under R-48, one
current attempt per session, and one receipt per dispatch key. `SessionLane` projects the record
into its typed state; the durable record, not a lane mailbox, is the crash-recovery authority.

**Rearm-pending lane state** — the typed `SessionLane` state that retains one `upgrade` or
`host_recovery` rearm attempt
identity, its current rearm recovery record, and the retry results for the affected active
generation. A `pending` attempt projects as rearm-pending. The state excludes
`Ledger.claim_next/3`. It survives a returned operator-owned
`session_binding_rearm_failed` result. A harness acknowledgment or a terminal binding transition
releases it through R-48.

**Normalized rearm failure envelope** — the durable raw failure evidence at the Adapter boundary:
exactly one JSON-safe value from this closed tagged union, produced before the gateway classifies it
as `harness_rearm_failed`:

- `acp_error`: operation, protocol code, message, and data from an ACP error response;
- `timeout`: operation and the returned `:timeout` transport result;
- `transport_closed`: operation and the returned `:closed` transport result;
- `malformed_response`: operation and the returned success value that failed response validation;
- `preparation_failure`: operation, stage, returned reason, and cleanup result for a session,
  model, mode, or cleanup preparation failure;
- `outcome_unknown`: operation and the exact `gateway_stopped_after_dispatch` cut; or
- `unclassified_adapter_failure`: operation and one fixed term class from `json_value`,
  `non_utf8_binary`, `bitstring`, `improper_list`, `non_json_list`,
  `non_text_map_key`, `non_json_map`, `non_finite_float`, `atom`, `tuple`, `pid`,
  `port`, `reference`, or `function`.

Operation is `session/new` or `session/load`. Preparation stage is `session_prepare`,
`model_apply`, `mode_apply`, or `cleanup`; a returned session-creation cleanup result has status
`verified` or `unverified` plus its reason, and cleanup result is null when the returned failure
has none. Every persisted field is a JSON value: null, boolean, integer, finite decimal, valid
UTF-8 string, proper list, or map whose keys are valid UTF-8 strings. The Adapter boundary maps
each returned value to this union before the gateway, recovery row, or EventLog receives it. A
returned value or nested reason outside the JSON domain maps the whole result to
`unclassified_adapter_failure` with the first applicable fixed term class above; the original
term is not rendered, encoded, persisted, or logged. Normalization examines only the outer and
nested types required to select that fixed class. R-43's single redaction seam transforms the JSON-safe
envelope before either the recovery row or event stores it. The transformed value preserves union
tag, remaining keys, scalar values, list order, and nesting. It contains no token, credential
identifier, raw anchor value, absolute path, authorization value, or transport secret.

## 4. Assumptions

### Verified givens

A-01. Current CLI discovery visits cwd ancestors and selects the first marker before environment or
gateway-file discovery.

A-02. The current CLI uses marker `url` and `token`. It does not compare marker `sessionKey`.

A-03. The gateway derives the session principal from the bearer token, then applies role and owner
authorization.

A-04. Placement derives one work root from session key and host. It writes the current marker with
`url`, `token`, and `sessionKey`.

A-05. The gateway shares one adapter process across sessions for a harness and host. The ACP
`session/new`, `session/load`, and `session/fork` calls carry per-session cwd and metadata.

A-06. Source baseline `be61cfc9` declares `@agentclientprotocol/codex-acp` `1.1.4` and
`@agentclientprotocol/claude-agent-acp` `0.66.0`. Their registry tarball integrity values are,
respectively, `sha512-DzusIpGwlQwMWuHgJhU8FWMsyQvzjenB93IEzQATkdbNulo5Rd9GKOz8+B+/C9iWWxmyXgtgmjzaL+iRFyDryQ==`
and `sha512-BwalxKsxZzHZGEs+X9hV3biErLE7PHWoao2hmyP3QBWXxvMHbc1F1tzDE95ZA47Fle+KBYf2gKpgy1MJ+ZmVlw==`.
The harness resolves each executable from
`<registered-host-base>/adapters/node_modules/.bin/<adapter-name>`. Its patched package bundles are
`<registered-host-base>/adapters/node_modules/@agentclientprotocol/codex-acp/dist/index.js` and
`<registered-host-base>/adapters/node_modules/@agentclientprotocol/claude-agent-acp/dist/acp-agent.js`.
The isolated fixture in AC-11 must record each resolved entry point and named bundle SHA-256 before
it tests a carrier. The currently installed Eezo adapter directory is not a proof subject: on
2026-08-12, the package manifests under
`/Users/mike/.tightbeam/adapters/node_modules/@agentclientprotocol/` reported `codex-acp` `1.1.9`
and `claude-agent-acp` `0.59.0`, which do not match the source-declared versions. This recon did not
prove an anchor carrier for either package.

A-07. The current Eezo binaries observed on 2026-08-12 are Codex CLI `0.146.0` at
`/opt/homebrew/bin/codex`, SHA-256
`134063e133f0b4244fa3b251acf973d4fe4b4aeeacbdc135211bf480f59f1477`, and Claude Code `2.1.227`
at `/opt/homebrew/bin/claude`, SHA-256
`7432511ba3be818e01f23f6eef8630d214a8b618451e188c3c7d61a987eef6c7`. These observations pin the
OQ-1 proof subject; they do not prove a carrier.

A-08. Host relocation copies the marker before the gateway changes the session host. The current
token does not rotate.

A-09. The current host registry keys hosts by operator-chosen name and stores ssh destination, base
directory, CLI directory, and adapter directory. Placement already uses that registered base to
derive each session work root.

### Threat-model assumptions

A-10. The harness and gateway are trusted to construct the session anchor from the database
session and placement result.

A-11. The model can change cwd and can encounter markers in reachable directories.

A-12. The model can read its own environment and its own marker. The anchor is an identity selector,
not a secret.

A-13. Possession of another session's bearer token is outside this structural-isolation guarantee.
Deliberately removing the complete anchor does not produce another session credential. Selecting
an identity through an operator endpoint still requires possession of its operator token and an
explicit identity selector.

A-14. Registered host configuration is trusted routing input for this work. Physical-base alias
detection and shared data custody are outside this identity-isolation guarantee. Marker custody and
binding equality still prevent a colliding path from selecting another session.

### Historical classification

A-15. Attest `att_13437f28-85af-4409-a851-a0effe409735` records a parent-session observation but
does not contain a captured request or marker fixture.

A-16. Controlling attest `att_9f954a6e-b9c1-4b74-9256-325535f5c7c5` attributes the earlier Eezo
failures to CLI `0.1.3` versus gateway `0.1.4` protocol skew. This work item has zero confirmed
damage specimens.

## 5. Invariants

I-01. Cwd and cwd ancestors cannot construct a bound session endpoint.

I-02. A complete session anchor names exactly one marker path, session key, credential identifier,
and gateway URL. A partial anchor constructs no endpoint.

I-03. A bound session endpoint exists only when the anchor fields, marker fields, canonical marker
path, trusted root, and marker file type agree.

I-04. The gateway authorizes a bound-session request only when the bearer token selects one active
session and the request's session key, credential identifier, generation, host, trusted-root digest,
and credential-provenance digest equal that session's active credential binding.

I-05. The database credential binding and registered host define the trusted root. The anchor,
session marker, cwd, and request can claim the root but cannot establish it.

I-06. One gateway-owned mutation seam prepares, activates, rotates, marks unavailable, or revokes a
credential binding. No placement or router path writes part of a binding independently.

I-07. A prepared destination credential cannot authenticate before the database commit. A source
credential cannot authenticate after that commit.

I-08. A shared adapter process does not store a session anchor in process-wide environment or
mutable adapter-wide session defaults.

I-09. ACP `session/new`, `session/load`, and `session/fork` project the binding that is active for
the Tightbeam session at that operation's start. Concurrent operations cannot observe another
session's anchor. `session/load` is the baseline's persisted-session re-entry carrier.

I-10. A marker token or organization token does not appear in an event-log field, error body,
command argument, test name, or artifact title. A raw trusted root or anchor path does not appear in
an event-log field, error body, test name, or artifact title. Tests can use obvious fixture tokens
in isolated files.

I-11. Marker binding checks occur before the CLI sends a request. Gateway binding checks and
bearer authentication occur as one authorization step before identity selection.

I-12. A bound-session marker failure does not fall back to cwd discovery, operator environment,
or `gateway.json`.

I-13. Operator endpoints preserve the current explicit role, user, and process selection rules.
Session endpoints preserve the current held-role and owner-user rules and the process refusal.

I-14. Local and remote hosts enforce the same marker schema, file-mode, canonical-path, symlink,
binding, rotation, and refusal rules.

I-15. Existing running work reaches migration only at an observed turn boundary. A timer cannot
stand in for that event.

I-16. The implementation uses no production work row or live session to test refusal behavior.

I-17. Spawn, relocation, migration, and host recovery cannot start or commit a credential-binding
transition while a turn for the affected session is running. The gateway prevents a new turn from
starting until the harness acknowledges the active anchor and the gateway releases the session's
turn fence.

I-18. Placement changes no existing marker when its bytes do not match the same session's current,
pending, or legacy binding. A derived-root collision therefore fails without selecting or
overwriting another session.

I-19. After credential-binding migration begins, the migrated database is in a shape that a prior
binary refuses before schema bootstrap or agent-turn intake. It cannot run cwd-based session
identity against that database.

I-20. Credential activation and turn admission are separate linearization points during migration
and host recovery. Activation makes the new token authoritative for request authentication. Only a
harness rearm acknowledgment followed by turn-fence release makes the session turn-admissible.

I-21. A returned `upgrade` or `host_recovery` rearm failure leaves the affected lane in typed
rearm-pending state. While that state exists, the lane cannot invoke `Ledger.claim_next/3`. Only a
matching authenticated rearm attempt can retry or release the state. A returned `restart_repair`
failure takes R-38's unavailable and terminal-release transition and never creates that state.

I-22. The durable rearm recovery record precedes binding activation and each ACP dispatch. A lane
crash restores the recorded phase without repeating that dispatch. An Adapter-owner crash after
dispatch records `outcome_unknown` only after `AdapterCoordinator` observes `DOWN`, increments the
adapter generation, and thereby proves the prior Adapter and its owned ACP connection are gone.
It
creates a new `restart_repair` attempt only when it can load the current binding's persisted vendor
session, or when a stored response proves an earlier `session/new` created no session. Otherwise it
commits the current binding as unavailable and performs no second ACP dispatch.

## 6. Architecture

### 6.1 Credential-binding data

R-01. Add an additive `session_credentials` table. Each row has non-null `sessionKey`,
`credentialId`, `generation`, `token`, `host`, `schemaVersion`, `state`, `current`, `createdAt`,
`updatedAt`, `createdBy`, and `cause` fields, plus nullable `trustedRoot` and `reason` fields.
`createdBy` is the nonempty canonical durable principal label from the operation that prepared the
tuple. `cause` has the closed values `spawn`, `relocation`, `upgrade`, and `host_recovery`.
`sessionKey` references `sessions` with delete cascade. `host` references the registered host row
with delete restriction. `credentialId` and `token` are unique. `(sessionKey, generation)` is the
primary key. Generation is positive. `createdAt` is positive, `updatedAt` is not less than
`createdAt`, and `createdBy` contains no NUL byte. `current` is `0` or `1`. A row is current exactly
when its state is `active` or `unavailable`. Partial unique indexes permit at most one current row
and at most one pending row per session. The row's `createdAt`, `createdBy`, and `cause` form
immutable credential provenance after prepare.

Acceptance link: AC-01, AC-02, AC-12, AC-13, AC-15.

R-02. `generation` starts at `1`. Each distinct credential tuple after generation `n` uses
generation `n + 1`, including recovery after an unavailable tuple. A placement change always
prepares a new generation. A retry of the same uncommitted operation reuses its prepared generation,
token, credential identifier, created-at time, created-by principal, and cause under the existing
idempotency seam.

Acceptance link: AC-12, AC-13, AC-15.

R-03. Credential `state` has the closed values `pending`, `active`, `revoked`, and `unavailable`.
An unavailable row requires one `reason` from `host_unreachable`, `host_root_invalid`,
`cli_version_mismatch`, `migration_materialization_failed`, or `rearm_outcome_unknown`. Every other
state requires a null reason. Pending and active rows require a non-null trusted root. An
unavailable row with reason `cli_version_mismatch`, `migration_materialization_failed`, or
`rearm_outcome_unknown` requires a non-null trusted root. An unavailable row with reason
`host_unreachable` or `host_root_invalid`, and a revoked row, can retain the last trusted root or
store null when no trusted root was verified.
`Org.by_cli_token/2` returns a session only for a current `active` credential and active session.
An internal credential lookup can distinguish pending, revoked, unavailable, and unknown tokens
for redacted event reasons without changing the public refusal.

Acceptance link: AC-07, AC-12, AC-15.

R-04. `Tightbeam.Org` owns the closed credential transitions `prepare`, `activate`, `rotate`,
`unavailable`, and `revoke`. Each
credential transition accepts a complete `%Org.SessionCredential{}` value whose fields are
enforced at construction. `prepare` persists one complete pending tuple in one transaction.
`activate`, `rotate`, `unavailable`, and `revoke` commit token, identifier, generation, host,
trusted root, schema version,
credential state, reason, created-at time, created-by principal, cause, and prior-generation state
as one transition in one database transaction.
They preserve the persisted credential's created-at time, created-by principal, and cause. A caller
that supplies a different provenance value receives `credential_provenance_immutable` and causes no
mutation. Each transition separately accepts the event cause and durable event principal that R-43
requires; those event values do not change credential provenance.
The same transaction sets the existing `sessions.cliToken` field to `NULL`. `prepare` does not
write that field. New session rows start with it null. Migration can read a non-null legacy value
only to verify the R-08 legacy marker before that session reaches its R-40 terminal transition. No
credential-binding path writes a non-null value. Other modules cannot update one binding field or
the legacy token field directly. A source-ownership test rejects a production reference to
`session_credentials` outside `lib/tightbeam/org.ex`.

Session retirement calls `revoke` in the same database transaction that makes the session retired.
That transaction revokes the current credential, sets `sessions.cliToken` to null, and records one
`session_binding_revoked` event with cause `retirement` and the retiring durable principal. The last
marker remains unchanged and becomes stale. A retirement transaction that cannot complete the
credential transition changes neither the session nor credential state.

`Tightbeam.Org.begin_credential_migration/2` is the only mutation seam for the migration-start
record. It inserts the complete value from Terms if the key is absent and treats a valid existing
value as a successful no-op. It refuses any other stored value as
`session_binding_migration_record_invalid` without starting migration.
Its one database transaction calls `Tightbeam.Schema.install_session_binding_fence/1`, which is the
only production function that inserts the `session-binding-v2` stamp, and records the R-41 event.
No production file outside `lib/tightbeam/schema.ex` mutates `schema_stamp`.

Acceptance link: AC-08, AC-12, AC-13, AC-16, AC-17.

### 6.2 Marker materialization

R-05. Placement writes schema-version-2 marker JSON with these required fields:
`schemaVersion`, `url`, `token`, `sessionKey`, `credentialId`, `generation`, `host`,
`trustedRoot`, `createdAt`, `createdBy`, and `cause`. The last four values equal the credential
binding. `schemaVersion` equals `2`. `createdAt` is a positive integer, `createdBy` is nonempty, and
`cause` is one R-01 value. The version-2 parser rejects an unknown field or a duplicate member name.

Acceptance link: AC-01, AC-02.

R-06. Placement computes `trustedRoot` from the lexically normalized absolute base directory of the
binding's registered host and the session-derived `work/<session-digest>` path in Terms. A missing
registered host or non-absolute base returns `host_root_invalid` before a marker write. Marker
content and cwd do not override the result. A prepared marker root that differs from its binding
returns `session_binding_root_mismatch`. A prepared marker host that differs returns
`session_binding_host_mismatch`.
A prepared marker created-at time, created-by principal, or cause that differs returns
`session_binding_provenance_mismatch`.

Acceptance link: AC-02, AC-10.

R-07. After R-06 validates the registered base, Placement refuses materialization when a
trusted-root path component below that base or the marker path is a symbolic link. The error code is
`session_marker_symlink`. The same filesystem primitive opens or creates each component relative to
the held base descriptor without following links and retains the trusted-root handle through marker
materialization. The operation does not replace or follow the link, and a pathname swap cannot
redirect its read or write.

Acceptance link: AC-05, AC-10.

R-08. Placement creates the trusted root as a real directory and writes the marker through a
mode-`0600` file named `.tightbeam-session.tmp.<credentialId>` relative to the held trusted-root
handle, followed by an atomic rename relative to that same handle. The pending credential tuple
owns that exact temporary name. A retry reuses it only when its bytes equal the pending tuple;
otherwise it returns `session_marker_custody_mismatch` and preserves the file. Pre-commit cleanup
removes only that matching temporary file. It obtains existing-marker type and bytes without
reopening the pathname. An existing marker that
exactly matches the current active or pending binding is a successful no-op. Placement replaces an
existing final marker only when the database proves that marker is an inactive prior credential for
the same session, or when legacy migration finds the same session key and legacy
`sessions.cliToken` under the turn fence. Any other existing file returns
`session_marker_custody_mismatch` without replacement. A failed write leaves no active credential
for the prepared marker.

Acceptance link: AC-10, AC-12.

R-09. Remote marker materialization sends marker bytes through the existing protected transfer seam. It
does not put token bytes in ssh arguments, shell source, process listings, or event fields.
Relocation's generic workdir-transfer seam has no option that includes the reserved top-level
`.tightbeam-session` entry. Cross-root relocation copies every other workdir entry, then invokes the
marker-materialization seam for the prepared destination credential. Local and remote transfers use
the same exclusion.

Acceptance link: AC-10, AC-13, AC-16.

### 6.3 Session anchor delivery

R-10. The gateway constructs the session anchor from the active database binding, active marker
path, and configured gateway URL. It passes that structure to ACP `session/new`, `session/load`, and
`session/fork`. `session/load` is the baseline's persisted-session re-entry carrier; the product
adds no `session/resume` path in this work.

Acceptance link: AC-09, AC-11.

R-11. `TIGHTBEAM_SESSION_FILE` is the canonical absolute path to the active marker.
`TIGHTBEAM_SESSION_KEY` equals the binding session key. `TIGHTBEAM_CREDENTIAL_ID` equals the
binding credential identifier. `TIGHTBEAM_SESSION_URL` equals the gateway URL that Placement wrote
to the marker. The marker's host, generation, and trusted root come from the same binding. Its
created-at time, created-by principal, and cause also come from that binding.

Acceptance link: AC-01, AC-09.

R-12. This specification does not select a Codex or Claude vendor projection carrier. OQ-1 blocks
changes to either vendor harness until AC-11 proves one carrier against the exact adapter package
and vendor binary pins in A-06 and A-07. The reviewed proof must map each ACP operation in Terms to
the exact vendor request field and show the tool-subprocess values. A spec amendment records that
mapping before implementation uses it. The shared adapter process environment remains unchanged.

Acceptance link: AC-09, AC-11.

R-13. Adapter construction accepts host-level values only. The four anchor values enter through the
`session/new`, `session/load`, or `session/fork` request for one session. A source-shape test rejects anchor fields in a
global harness launch plan, shared home, host environment overlay, or process mutation. An attempt
to store any anchor name as a host or harness environment overlay returns existing code
`reserved_env_name` and changes no overlay row.

Acceptance link: AC-09.

### 6.4 CLI resolution

R-14. Replace `Origin::Session(PathBuf)` with a bound-session origin whose constructor requires a
validated anchor, marker, and binding claims. Remove upward session-marker discovery.

The bound resolver applies this refusal order: incomplete anchor; invalid anchor; absent marker;
symlink; non-regular marker; wrong mode; malformed JSON; absent or unsupported schema version;
invalid version-2 fields; anchor mismatch; root mismatch. Duplicate member names are malformed for
this order. It returns the first applicable R-16
through R-23 code and performs no later discovery step.

Acceptance link: AC-03, AC-04, AC-06.

R-15. If none of the four anchor variables exists, the CLI uses operator endpoint discovery. A
marker in cwd or a cwd ancestor has no effect.

Acceptance link: AC-03, AC-18.

R-16. If one, two, or three anchor variables exist, the CLI exits with code `1`, writes
`session_anchor_incomplete` to stderr, sends no network request, and performs no operator fallback.
If all four exist but one is non-UTF-8, the marker path is not absolute, the session key or gateway
URL is empty, the credential identifier is not a canonical lowercase UUIDv4, or the URL is not an
absolute `http`, `https`, `ws`, or `wss` URL, it writes `session_anchor_invalid` with the same exit,
network, and fallback behavior. Environment presence uses the operating-system value, so a
non-UTF-8 value cannot be treated as absent.

Acceptance link: AC-04.

R-17. If the marker path is absent, the CLI exits with code `1`, writes
`session_marker_missing` to stderr, and sends no network request.

Acceptance link: AC-04.

R-18. If the marker or any path component from the filesystem root through the marker path is a
symlink, the CLI exits with code `1`, writes
`session_marker_symlink` to stderr, and sends no network request. Starting from the filesystem root,
the resolver opens each directory component without following links and retains the parent handle
until it opens the marker without following links. It derives the canonical path from that held
descriptor chain and obtains marker type, mode, and bytes from the one marker handle. It does not
reopen a pathname between those checks. Replacing an intermediate or final pathname cannot redirect
the read.

Acceptance link: AC-05.

R-19. If the marker mode differs from `0600`, the CLI exits with code `1`, writes
`session_marker_permissions` to stderr, and sends no network request.

Acceptance link: AC-05.

R-20. If the marker is not a regular file, JSON parsing fails, a required field other than
`schemaVersion` is absent or has the wrong type, an unknown or duplicate field exists, or a
version-2 field fails semantic validation, the CLI exits with code `1`, writes
`session_marker_invalid` to stderr, and sends no network request. Semantic validation requires the exact token form in Terms, nonempty
session key, host, and created-by principal, canonical lowercase UUIDv4 identifiers,
positive generation and created-at values, a created-by principal without a NUL byte, one R-01 cause,
an absolute `http`, `https`, `ws`, or `wss` URL, and an absolute lexically normalized trusted root.

Acceptance link: AC-04.

R-21. If `schemaVersion` is absent or differs from `2`, the CLI exits with code `1`, writes
`session_marker_legacy` or `session_marker_version` respectively, and sends no network request.

Acceptance link: AC-04, AC-17.

R-22. If anchor session key, credential identifier, or gateway URL differs from the marker, the CLI
exits with code `1`, writes `session_marker_mismatch` to stderr, and sends no network request. URL
comparison occurs before websocket-to-HTTP scheme normalization.

Acceptance link: AC-06.

R-23. If the canonical marker path differs from `<marker.trustedRoot>/.tightbeam-session`, or if the
canonical containing root differs from `marker.trustedRoot`, the CLI exits with code `1`, writes
`session_marker_root_mismatch` to stderr, and sends no network request.

Acceptance link: AC-05, AC-08.

R-24. The CLI does not inspect cwd for markers in bound-session mode. Cwd can be inside another
session's workdir. The request still uses the bound session endpoint.

Acceptance link: AC-03.

R-25. Each bound request sends `x-tightbeam-session-key`, `x-tightbeam-credential-id`,
`x-tightbeam-credential-generation`, `x-tightbeam-marker-host`,
`x-tightbeam-marker-root-sha256`, and
`x-tightbeam-credential-provenance-sha256` beside the bearer token. It does not send trusted-root,
marker-path, created-by, or cause text. The root header is the lowercase SHA-256 digest of the
marker's validated normalized UTF-8 trusted root. The provenance header follows Terms.

Acceptance link: AC-01, AC-07.

### 6.5 Gateway attribution and authorization

R-26. The gateway applies these checks in one router authorization function after the exact protocol
version check: token lookup and session/credential state; presence of the six binding headers;
header parsing; equality with the active binding. An unknown, pending, unavailable, revoked, or
retired token returns R-28 regardless of its headers. An active token with a missing header returns
R-27's required response. An active token with an unparseable or unequal header returns R-27's
mismatch response. Identity resolution runs only after all checks return the bound session.

Header parsing requires nonempty session key and host, a canonical lowercase UUIDv4 credential identifier, a
positive base-10 generation with no sign or leading zero, and 64-character lowercase hexadecimal
root and provenance digests. Each required header has exactly one value. A duplicate required
header is unparseable for this gate.

Acceptance link: AC-07.

R-27. A missing binding header on an active session-token request returns HTTP `401` with code
`session_binding_required`. An unparseable claim or a claim that differs from the token-selected
binding returns HTTP `401` with code `session_binding_mismatch`. Neither response identifies the
expected value.

Acceptance link: AC-07.

R-28. A token for a retired session, unavailable credential, revoked prior generation, or pending
destination returns HTTP `401` with existing code `auth_failed`. The public response does not
distinguish those cases.

Acceptance link: AC-07, AC-13, AC-15.

R-29. After binding authentication, the router retains the current decisions:

- a held `--as <role>` succeeds;
- an unheld role returns `role_not_held`;
- matching owner `--as-user` succeeds;
- another user returns `identity_not_yours`;
- session `--as-process` returns `identity_not_yours`;
- organization-token role, user, and non-reserved process selection remain available.

Acceptance link: AC-14.

### 6.6 Spawn and relocation

R-30. Spawn persists a credential in `pending` state and persists the new session row with a null
`sessions.cliToken`. It prepares the marker before it returns the
session or starts its first harness turn. One prepare transaction persists the pending credential.
The binding mutation seam activates the credential after the marker rename
succeeds. Before activation commits, the pending token cannot authenticate and a harness turn cannot
start.

Acceptance link: AC-12.

R-31. A marker materialization failure before final rename returns its named placement error. The
pending token cannot authenticate or start a turn. Cleanup removes a final marker only when its
credential identifier matches the pending row. After the marker is absent, one spawn-failure
cleanup transaction removes the failed session, role, idempotency projection, and pending
credential. A marker-removal failure or different credential identifier returns
`session_binding_cleanup_failed`, retains the rejected pending row, and emits the matching R-43
reason. Cleanup removes only the matching R-08 temporary name. A retry with the same idempotency key
resumes cleanup before it can prepare another credential.

If final marker rename succeeds but credential activation does not commit, spawn returns
`session_binding_activation_failed` and retains the pending row and matching marker.
A retry with the same idempotency key rereads the exact marker. A complete match resumes activation
without changing any prepared tuple field. An absent marker resumes materialization with
the persisted pending tuple. A different credential identifier returns
`session_binding_cleanup_failed`, preserves the file, and leaves the pending token rejected.

Acceptance link: AC-12.

R-32. For a relocation whose normalized destination trusted root differs from the source trusted
root, the gateway atomically acquires a per-session turn fence only when no turn is running. It
returns `session_turn_running` without preparing a credential or marker when that check fails. It
holds the fence through destination preparation, binding commit, source-marker cleanup attempt,
and harness rearm. Relocation prepares generation `n + 1` at the destination with a new token and credential
identifier. Before the database commit, generation `n` authenticates and generation `n + 1` does
not. The commit changes the host and complete binding in one transaction. After the commit,
generation `n + 1` authenticates and generation `n` does not. The gateway releases the turn fence
only after the harness carries the currently active binding's anchor: generation `n + 1` after a
successful commit or generation `n` after a pre-commit failure.

Acceptance link: AC-13.

R-33. When source and destination normalized trusted roots differ, relocation transfers the
workdir without the source `.tightbeam-session`, then materializes generation `n + 1` at the
destination before commit. The generation-`n` marker remains unchanged at the source until
source-marker removal occurs after the relocation commit. A removal failure records the
cleanup failure but does not reactivate generation `n`. Retry removes the named stale source
marker only when its credential identifier still equals generation `n`.

Acceptance link: AC-13.

R-34. A failure before relocation commit removes the uncommitted destination marker when its
credential identifier matches the prepared value. A missing or successfully removed matching
marker permits the mutation seam to remove the pending row. Cleanup also removes only the matching
R-08 temporary name. A removal failure or different credential identifier retains the pending row,
emits `session_binding_cleanup_failed` with the matching R-43 reason, and makes the same relocation
request resume cleanup before another preparation. Generation `n` remains active. Before
it releases the turn fence, the gateway confirms that the harness carries generation `n`'s anchor.
A failure after commit uses forward repair; it does not restore generation `n`, and the fence
remains held until the harness carries generation `n + 1`'s anchor.

Acceptance link: AC-13.

R-35. Local-to-local, local-to-remote, remote-to-local, and remote-to-remote moves whose normalized
source and destination trusted roots differ use the same prepare, commit, and cleanup states. When
the normalized roots are equal, relocation returns `session_relocation_same_root` before turn-fence
acquisition and changes no session host, credential row, marker, workdir entry, or event. This
specification adds no same-root staging object or credential rotation path.

Acceptance link: AC-10, AC-13.

### 6.7 Compatibility, migration, and rollback

R-36. The release changes the pre-1.0 CLI protocol version. Exact CLI/gateway version checking
remains the first request check.

Before spawn or relocation prepares a binding, and before migration or recovery activates one, the
gateway asks that host's registered CLI binary for its version through the existing bounded local or
ssh execution seam. A missing, malformed, or non-equal pre-1.0 version returns
`host_cli_version_mismatch`. Spawn and relocation make no credential, marker, session, or
host mutation. Migration and recovery follow R-39's named unavailable transition. The packaged
local CLI and gateway still pass the existing assembly version-smoke gate.

Acceptance link: AC-15, AC-17.

R-37. Database migration is additive. It retains nullable `sessions.cliToken` only as a legacy
migration input; adds `session_credentials` and its constraints and indexes; and uses the existing
`org_settings` table for the migration-start record.
It adds the credential-binding schema-fence row without altering the existing `schema_stamp`,
`hosts`, or `sessions` table definitions. Each active session's R-40 terminal transition and each
retired session's R-39 terminal transition clears its legacy token field. No new session
or credential transition repopulates that field.
Schema-version-2 marker JSON remains parseable by the prior CLI because its added fields do not
replace `url` or `token`. A manual shell that relied on cwd marker discovery no longer receives
session identity. It must receive a complete session anchor or use an operator endpoint with an
identity flag.

Acceptance link: AC-17.

R-38. After the read-only host preflight below succeeds, upgrade enters an explicit migration mode
that does not start a new agent turn. If a session has no running turn, entry to migration is its
observed boundary. If a turn is running, its terminal event is the boundary. At that boundary,
migration atomically checks that no turn is running and acquires the session turn fence. Migration
mode rejects spawn, relocation, retirement, and host registration with `migration_in_progress`
until each active session has an R-40 terminal result and each retired legacy token is null. For an
active legacy session whose registered host is reachable, whose base yields a valid trusted root,
and whose CLI passes R-36, migration prepares generation `1` with a fresh token and credential
identifier and materializes a version-2 marker. The lane and durable R-48 attempt then enter
`guarded` for that generation and initial retry-request identifier. Migration activates the binding
and rearms or loads the harness session with its anchor while it holds the fence. It releases the
fence only after the harness rearm acknowledgment.

Before the first R-41 transaction, a read-only preflight verifies that every active or retired
session's host is registered. A missing alias returns `session_host_unregistered`. It creates no
migration-start record, schema fence, binding, marker, or event, and it does not infer transport or
root values. The
legacy database remains available to the prior release so the operator can register the missing
host before retrying the upgrade.

On every application start that accepts either R-41 version-2 shape—the upgraded shape pair with
its migration-start record or the fresh single version-2 shape—the boot path keeps global agent-turn
intake closed. For each active session with a current active binding, it acquires a replacement
per-session turn fence after the ledger reports no running turn, then rearms the harness with that
binding's exact anchor. An active binding is not an R-40 terminal result for that application start
until the harness rearm acknowledgment occurs and the fence releases. A current unavailable binding
requires no harness rearm. An active session with no current active or unavailable binding resumes
migration. A retired session that retains a legacy token resumes its R-39 terminal clearing.
Recovery reuses a persisted pending tuple and matching marker under R-31's activation-retry rules;
it does not mint another generation. Restart rearm of an already active binding uses that binding
without preparing, activating, rotating, or emitting a second binding-lifecycle event. A process
restart is not a turn boundary, a fence release, a rearm acknowledgment, or a successful migration
result. Before it starts a replacement lane, the boot path resolves each current R-48 record. A
`dispatched` receipt without a result transitions once to `failed` and its attempt transitions to
`pending` with an `outcome_unknown` envelope only after `AdapterCoordinator` observes `DOWN` for
the receipt's Adapter PID and advances that adapter key past the receipt's generation. That proves
the prior Adapter and its owned ACP connection stopped. If the guarded generation did not become
the current active binding, the gateway changes that guard to `released` with result
`activation_not_committed` and resumes the existing migration or recovery path. It does not create
rearm-pending state or a `restart_repair` attempt for that guard.

For a prior `guarded`, `pending`, or `acknowledged` attempt whose generation is the current active binding, the
boot path changes an attempt bound to a dead Adapter incarnation to `released` with result
`superseded_restart` and no
ledger eligibility check due; a prior `released` attempt retains its result. Each
dead-incarnation attempt is stale and cannot open intake. A `guarded` attempt with no dispatched
receipt can repeat its original operation because it records zero prior ACP calls. A prior
`session/new` failure is safe to repeat only when its stored envelope is `acp_error`, or is
`preparation_failure` with cleanup status `verified`; those returned results prove no external
session remains. An acknowledged `session/new`, or any `session/load`, can continue only through
`session/load` of the exact persisted vendor session identifier. Every other prior `session/new`,
and any load without that identifier, causes one transaction to change the binding to unavailable with reason
`rearm_outcome_unknown`, emit the unavailable event, and clear the replacement fence through
R-48's terminal-release path. That branch creates no new attempt and makes no other ACP call.
Otherwise the boot path checks out the current Adapter PID and generation from
`AdapterCoordinator`, then mints a new attempt identifier and retry-request identifier for the
applicable `restart_repair` new or load operation. It does not
reuse or redispatch the prior request. The transaction that makes the new attempt current also
makes the released prior attempt non-current. If restart rearm does not acknowledge, one
transaction normalizes and redacts the returned failure, changes the receipt to `failed`, records
`session_binding_rearm_failed` with cause `restart_repair` and principal
`process:tightbeam`, changes the active binding to unavailable with reason
`rearm_outcome_unknown`, and changes the attempt to `released` with a terminal result. The
boot path then clears the replacement fence through R-48's terminal-release path and continues
global readiness evaluation. It does not enter rearm-pending state, accept a same-Adapter-incarnation retry,
wait for another start, or make another ACP call.

On a cold upgrade, the prior release's terminal turn event or the existing boot-recovery terminal
event is the observed boundary for a turn that had been running. Migration starts only after the
ledger reports no running turn for the affected session. Process disappearance without that event
is not a boundary.

If marker materialization or binding activation fails, migration removes a final marker only when
its credential identifier matches the prepared row. A missing marker or successful matching
removal completes cleanup. A removal failure or a different credential identifier leaves the file
in place and records `session_binding_cleanup_failed`; it does not use or
overwrite that file. In either cleanup outcome, one transaction marks the prepared binding current
and unavailable with reason `migration_materialization_failed`, sets `sessions.cliToken` to `NULL`,
and records `session_binding_unavailable`. Migration releases the fence only after that transaction
commits. The unavailable token returns `auth_failed`, and no turn starts for that session.

If migration activation commits but harness rearm does not acknowledge, the gateway returns
`session_binding_rearm_failed`, records `session_binding_rearm_failed` with cause `upgrade`, leaves
the committed active binding and marker unchanged, and, before replying, projects the durable R-48
`pending` attempt and its failed receipt into rearm-pending lane state. A retry whose Adapter
process incarnation, operation-attempt identifier, session key, generation, cause, and principal match that
state rearms the exact active
generation. It does not prepare or activate a new generation. If the Adapter or application stops
before rearm acknowledgment and fence release, recovery applies the preceding boot rule: intake
stays closed, the lane restores R-48 state before it accepts a nudge, and the boot path either performs the
preceding safe `restart_repair` branch for the exact active generation or commits
`rearm_outcome_unknown` without another ACP call.

Acceptance link: AC-15, AC-17.

R-39. At the R-38 boundary, migration handles each legacy session through one credential mutation
seam. A retired session receives no credential row; one transaction sets its legacy
`sessions.cliToken` to null and records no binding lifecycle event. An active session on an
unreachable host receives generation `1` as current and unavailable with reason `host_unreachable`,
a fresh token and credential identifier, and a null trusted root. An active session whose
registered base cannot produce the Terms trusted root receives the same shape with reason
`host_root_invalid`. Neither token authenticates and neither case writes a marker.

An active session whose host is reachable and trusted root is valid but whose CLI fails R-36
receives generation `1` as current and unavailable with reason `cli_version_mismatch`, the derived
trusted root, and no marker. Placement on that host returns `host_cli_version_mismatch`.

For a reachable compatible host, migration prepares and materializes generation `1`. A pre-existing
marker that R-08 cannot prove to the same legacy session returns
`session_marker_custody_mismatch`, remains byte-for-byte unchanged, and drives the prepared binding
to current `unavailable` with reason `migration_materialization_failed`. Migration does not assign
file custody or overwrite a colliding marker. This named failure closes identity migration for that
session without adding a root inventory or adjudication mechanism.

Host recovery atomically checks that no turn is running and acquires the per-session turn fence
before it applies R-36, derives the trusted root through R-06, or mutates a credential or marker. A
running turn returns `session_turn_running`, creates no pending generation or marker, and changes no
binding. Recovery holds the fence through the host checks, marker materialization, activation or
unavailable commit, harness rearm, and fence release.

After the host checks succeed, recovery prepares and materializes the next generation for an
unavailable active session. Before activation, the lane and durable R-48 attempt enter `guarded` for
that generation and initial retry-request identifier; recovery then activates it. A marker custody mismatch makes that next generation
current and unavailable with reason `migration_materialization_failed`; the existing marker remains
unchanged, and the gateway releases the fence only after the unavailable transition and event
commit. An active binding that becomes unreachable after verified migration keeps its last trusted
root when it becomes unavailable.

After recovery activation commits, the new generation authenticates but remains
non-turn-admissible behind the held fence. The gateway rearms the harness with that exact active
anchor and releases the fence only after the harness rearm acknowledgment. If rearm does not
acknowledge, the gateway returns `session_binding_rearm_failed`, records
`session_binding_rearm_failed` with cause `host_recovery`, leaves the active binding and marker
unchanged, and, before replying, projects the durable R-48 `pending` attempt and its failed receipt
into rearm-pending lane state. A matching same-Adapter-incarnation retry with an R-48 retryable envelope
performs only rearm of that active generation and does not prepare generation `n + 2`. A
non-retryable envelope instead commits `rearm_outcome_unknown` and takes the terminal-release path
without another ACP call. If the gateway stops after activation and before rearm acknowledgment
and fence release, R-38's boot ordering restores the replacement fence before the lane accepts a
nudge. It either performs the safe `restart_repair` branch for the same active generation or
commits `rearm_outcome_unknown` without another ACP call, then follows the corresponding
acknowledged or terminal release.

If the current unavailable binding already has the same host, trusted root, and reason, another
failed version, root, or reachability check is a successful no-op. It does not mint a generation or
emit a second unavailable event. Recovery releases the fence only after it re-reads that current
binding as unavailable. A failed check that commits a different unavailable reason releases the
fence only after the unavailable transition and event commit.

Acceptance link: AC-15.

R-40. During initial migration and each application start that accepts either R-41 version-2 shape,
global agent-turn intake reports ready only after each active session has one terminal result for
that start: an active binding whose exact anchor received a harness rearm
acknowledgment and whose per-session turn fence then released, or a current unavailable binding with
one R-03 reason. An active database binding alone is not a terminal turn-readiness result. After
global intake opens, host recovery preserves turn admission for other sessions while the recovering
session's fence blocks that session through rearm. An unavailable session cannot start a turn and
its token returns
`auth_failed`. Placement on a host with a failed current CLI version check returns
`host_cli_version_mismatch`. Placement for an invalid registered base returns `host_root_invalid`.
Every retired session has a null legacy token before readiness. Migration does not accept a legacy
marker as a temporary identity source.

Acceptance link: AC-15, AC-17.

R-41. The first R-38 migration-mode transaction inserts the migration-start record before it can
prepare a binding or write a version-2 marker. In that same transaction it inserts
the credential-binding schema-fence row and records `session_binding_migration_started`. The setting
and fence row are never deleted or changed. The event has cause `upgrade` and principal
`process:tightbeam`.

The current release accepts exactly these shape states: legacy `model-identity-v1` alone before an
upgrade begins; `model-identity-v1` plus `session-binding-v2` with the valid migration-start record
after an upgrade begins; or `session-binding-v2` alone with no migration-start record for a fresh
database. Any other combination, a fence pair without the record, or a record without the exact
fence pair returns `session_binding_migration_fence_invalid` before intake opens.

When this release boots with the legacy shape alone and R-38's preflight succeeds, it enters
migration mode and commits the R-41 transaction before intake can open. A fresh database needs no credential migration and emits
no migration-start event; its single new shape row still makes the prior binary refuse it.

Before the migration transaction, an earlier proved package can use the unchanged legacy database
because no new binding state exists. After it, the prior binary's existing exact shape check sees
two rows and raises its existing `ShapeError` before it creates a schema object or opens intake.
Forward repair with the current release is the only supported recovery. The product does not add a
second rollback command or a compatibility path for the cwd resolver.

Acceptance link: AC-17.

### 6.8 Observability

R-42. The event log records these session-binding lifecycle events:
`session_binding_prepared`, `session_binding_activated`, `session_binding_unavailable`,
`session_binding_rotated`, `session_binding_revoked`, and `session_binding_cleanup_failed`. It also
records `session_binding_rearm_failed` and the global event
`session_binding_migration_started`. `prepare`, initial `activate`,
`unavailable`, and explicit `revoke` each emit their named event in the transition transaction. A
successful rotation emits
`session_binding_rotated` for the new generation and does not emit a second revoked event for the
superseded generation. Each cleanup failure emits `session_binding_cleanup_failed`. Rollback emits
no event because the prior binary refuses before the current event subsystem can run. Each failed
harness rearm attempt emits `session_binding_rearm_failed` with the R-48 normalized failure
envelope. For `upgrade` and `host_recovery`, the event does not change the active binding; the
transaction changes the R-48 receipt from `dispatched` to `failed` and its attempt to `pending`.
For `restart_repair`, that transaction instead changes the active binding to unavailable with
`rearm_outcome_unknown` and the attempt to terminal `released` under R-38. The transaction inserts
or reads that attempt-and-retry identifier's single failure event. A unique
operation-attempt and retry-request key makes a duplicate return the recorded result and event
identifier without a second event. The migration transaction emits one start event under
R-41. The retirement transition in R-04 emits
exactly one revoked event in its transaction.

Acceptance link: AC-16.

R-43. Each session-binding lifecycle event contains event name, session key, registered host name,
credential generation, marker schema version, outcome, cause, durable principal, and a SHA-256
digest of the trusted root. The digest is null only when the binding has a null trusted root under R-03.
Each event also has a nullable reason.
`session_binding_unavailable` uses one R-03 reason. `session_binding_cleanup_failed` uses
`marker_remove_failed` or `marker_credential_mismatch`. `session_binding_rearm_failed` uses
`harness_rearm_failed`, outcome `failed`, and cause `upgrade`, `host_recovery`, or
`restart_repair`. An `upgrade` or `host_recovery` rearm failure uses the durable principal of that
operation. A `restart_repair` failure uses principal `process:tightbeam`. Other lifecycle events use
a null reason. Binding-event cause is one of `spawn`, `relocation`, `upgrade`, `host_loss`,
`host_recovery`, `restart_repair`, `retirement`, `manual_revoke`, or `cleanup`.

A `session_binding_rearm_failed` event also contains the operation-attempt identifier,
retry-request identifier, Adapter process incarnation, and normalized rearm failure envelope from
Terms. The process incarnation and identifiers are non-secret. The event's session, generation, cause,
and principal equal the R-48 state.

`Tightbeam.Acp.Adapter.normalize_rearm_failure/2` is the only boundary from an arbitrary returned
adapter term into the Terms union. Its arguments are the operation and returned value. It passes
through only listed response shapes whose fields are JSON values. It maps any other JSON value to
`unclassified_adapter_failure` with class `json_value`. It maps a non-UTF-8 binary, non-byte
bitstring, improper list, proper list with a non-JSON descendant, map with a non-text key, map with
a non-JSON descendant, non-finite float, other atom, tuple, PID, port, reference, or function to
the corresponding fixed Terms class. It examines only enough structure to select the class and
does not render, encode, persist, or log the rejected term. These cases cover the Erlang external
term classes; the function returns one JSON-safe union
value for each input.

`Tightbeam.EventLog.redact_session_binding_rearm_failure/2` is the one failure-envelope redaction
seam. Its arguments are that normalized union value and the set of nonempty sensitive byte strings
from the binding and request: token, credential identifier, four raw anchor values, Authorization
value, trusted root, marker path, registered base, ssh destination, and transport secret. It
accepts only the Terms JSON domain. For each source map key it ASCII-lowercases the UTF-8 key and
removes `_` and `-`; if the result is one of `authorization`, `token`, `credentialid`,
`anchor`, `sessionanchor`, `marker`, `markerpath`, `path`, `cwd`, `trustedroot`, `base`,
`sshdestination`, or `transportsecret`, it preserves the source key and replaces the value with
`[REDACTED]`. Otherwise it recursively redacts the value while preserving scalar values, list
order, map keys, and nesting. For each string value it replaces each exact sensitive byte string,
longest first, with `[REDACTED]`; if the whole value begins with `/`, a drive-letter plus `:\\`
or `:/`, or `\\\\`, it replaces the whole value. It returns one JSON-safe transformed union
value. AC-16 verifies both the total boundary classifier and this exact redaction algorithm before
event insertion.

`session_binding_migration_started` has event name, outcome `started`, cause `upgrade`, reason null,
durable principal `process:tightbeam`, and null session, host, generation, schema-version, and
root-digest fields. It contains no path, transport, credential, or token value.

Acceptance link: AC-16.

R-44. Gateway binding refusals record `session_binding_refused` with session key when the token
selects one, request generation when parseable, and one internal reason from `unknown_token`,
`missing_claim`, `claim_mismatch`, `pending`, `revoked_prior_generation`, `retired_session`,
`host_unreachable`, `host_root_invalid`, `cli_version_mismatch`,
`migration_materialization_failed`, or `rearm_outcome_unknown`. The public
response follows R-27 and R-28.

Acceptance link: AC-07, AC-16.

R-45. CLI local refusals use the stable stderr codes in R-16 through R-23. The message can include
the anchor variable name. It must not include marker JSON, token, credential identifier, or an
absolute marker path.

Acceptance link: AC-04, AC-05, AC-06, AC-16.

### 6.9 Named implementation surface

R-46. Implementation changes are limited to these production files unless the spec writer first
amends `specs/tightbeam/spawned-session-identity-isolation.md`, clears independent review, and
installs the amended bytes plus exact SHA-256 through the header's installation seam:

- `cli/src/dispatch.rs`
- `cli/src/args.rs`
- `cli/Cargo.toml`
- `cli/Cargo.lock`
- `lib/tightbeam/org.ex`
- `lib/tightbeam/schema.ex`
- `lib/tightbeam/placement.ex`
- `lib/tightbeam/gateway.ex`
- `lib/tightbeam/acp/adapter.ex`
- `lib/tightbeam/adapter_coordinator.ex`
- `lib/tightbeam/harness.ex`
- `lib/tightbeam/harness/support.ex`
- `lib/tightbeam/harness/codex.ex`
- `lib/tightbeam/harness/claude.ex`
- `lib/tightbeam/wire/router.ex`
- `lib/tightbeam/event_log.ex`
- `lib/tightbeam/readiness.ex`
- `lib/tightbeam/rails.ex`
- `lib/tightbeam/session_lane.ex`
- `priv/guidance/operating-manual.md`
- `docs/INTER-NODE-COMMS.md`
- `docs/RELEASE_TRAIN.md`
- `README.md`

Test changes belong in `cli/src/dispatch.rs`,
`test/cli_integration_test.exs`,
`test/placement_test.exs`, `test/org_test.exs`, `test/schema_shape_test.exs`,
`test/gateway_test.exs`, `test/router_test.exs`, `test/acp_adapter_test.exs`,
`test/adapter_coordinator_test.exs`,
`test/harness_seam_test.exs`, and
`test/adapter_patch_mode_test.exs`, `test/readiness_test.exs`,
`test/support/test_case.ex`, `test/lane_test.exs`, and `packaging/assemble.sh`.

Acceptance link: AC-19.

R-47. The repository operating pattern states that a spawned session receives identity through its
harness-supplied session anchor. Its identity remains the anchored session when cwd is outside its
trusted root or inside another session's nested workdir. An operator shell has no session anchor and
uses an operator endpoint plus an explicit identity selector. CLI help, the operating manual, the
inter-node runbook, Placement's operator-endpoint documentation, the rail observation description,
and README contain no claim that cwd or an ancestor marker selects session identity. The release
train states that a database with credential-binding migration started can recover only with a
current release; an earlier proved package is not a rollback target for that database.

Acceptance link: AC-19.

R-48. `Tightbeam.SessionLane` owns turn exclusion and the typed projection of the rearm recovery
record. `Tightbeam.Org` owns the record's single mutation seam. The schema permits only the Terms
phases and their forward transitions, one current attempt per session, and one receipt per
operation-attempt and retry-request pair.

At the held turn boundary, the lane authenticates the rearm request under the cause-specific route
below. Before binding activation, it installs `guarded` in its state and commits the identical
durable row. Neither activation nor ACP I/O starts before that commit returns. An activation
failure changes `guarded` to `released` with result
`activation_not_committed` in the transaction that preserves or makes unavailable the binding; it
does not enter rearm-pending and emits no `session_binding_rearm_failed` event. The existing R-38
or R-39 path then releases or retains the turn fence from that durable binding result.

The current `Tightbeam.Acp.Adapter`, not the lane, owns rearm ACP execution. The Gateway
composition function resolves the session's adapter key and obtains `{adapter_pid,
adapter_generation}` from `AdapterCoordinator`; it does not supply a gateway PID. The lane records
that exact Adapter incarnation and monitors its PID. Immediately before one `session/new` or
`session/load` call, the lane inserts that retry-request identifier's `prepared` receipt and changes
the receipt to `dispatched`. It submits the request to that Adapter only after the `dispatched`
commit. The Adapter serializes the ACP call through its owned `Acp.Conn` and retains the in-flight
or completed result by the attempt-and-retry key independently of the lane. A lane that stops
before `guarded` commits causes no binding or ACP effect. A replacement lane restores a `guarded`
attempt before a nudge. For a `dispatched` receipt whose Adapter incarnation is still current, it
joins or reads that Adapter's one retained result. The Adapter accepts duplicate joins only for the
same attempt-and-retry key and retains the result even when the initiating lane has stopped.

For an `upgrade` or `host_recovery` failed result, one transaction calls R-43's normalization
and redaction seams, changes the receipt from `dispatched` to `failed`, changes the attempt to
`pending`, stores the transformed envelope, and inserts or reads the R-42 event. A failed
`restart_repair` instead performs R-38's unavailable transition and terminal release in the same
transaction that stores its failed receipt and event; it never becomes `pending`. For a harness
acknowledgment, one transaction changes the receipt to `acknowledged`, changes the attempt to
`acknowledged`, and stores that result. A replacement lane restores either result before accepting
a nudge. If the Adapter process stops at or after a `dispatched` receipt and before a stored
result, R-38 records that receipt's single `outcome_unknown` failure only after
`AdapterCoordinator` proves the prior Adapter PID is down and the key has advanced to a later
generation. It never redispatches
the prior retry-request identifier. R-38 either makes the active binding unavailable without
another ACP call or creates a distinct `restart_repair` for a proved-absent new session or an exact
persisted vendor session; it never issues a second `session/new` for an uncertain result.

After a `pending` attempt and failed receipt exist, the lane installs rearm-pending state before it
replies `session_binding_rearm_failed`. A nudge while the current attempt is `guarded`, `pending`,
or `acknowledged`, including while a receipt is `prepared`, `dispatched`, `failed`, or
`acknowledged`, performs one state check and no `Ledger.claim_next/3` call. Cause, principal,
credential generation, Adapter process incarnation, operation-attempt identifier, retry-request
identifier, normalized envelope, and event
identifier come from the same recovery row.

An attempt whose durable principal is not `process:tightbeam` uses the `wire` route. Router
bearer-token authentication derives that principal; the Gateway composition function obtains the
current Adapter checkout before the lane call. An attempt whose principal is `process:tightbeam`
uses the `boot` route. The boot path has no wire caller: it obtains the current Adapter checkout
directly from `AdapterCoordinator`, and the lane accepts it only when the adapter key, PID, and
generation equal the checkout and its own monitor names that PID. A
`restart_repair` initial attempt uses this internal route, has no wire route, and has no
same-Adapter-incarnation retry after a returned failure. A
Adapter-key, Adapter-PID, Adapter-generation, authentication-route, or principal mismatch returns
`session_binding_rearm_wrong_process`. A missing current row or a session-key,
operation-attempt-identifier, generation, or cause mismatch returns
`session_binding_rearm_stale`. A refusal performs no ACP operation, binding change, recovery-row
change, or lifecycle event.

For `upgrade` and `host_recovery`, the unique attempt-and-retry key is the duplicate receipt.
The first matching request can add a
`prepared` receipt to a `pending` attempt and advance that receipt to `dispatched`. A concurrent
duplicate joins the Adapter's in-flight request. A later duplicate returns the stored
`failed` or `acknowledged` receipt, or its attempt's `released` result, without another ACP request
or event. While one receipt is `dispatched`, a different retry-request identifier returns
`session_binding_rearm_retry_in_progress`. After a stored failure, a different identifier can add
the next serial receipt for the same attempt only under this retry-safety gate. `acp_error` is
retryable for either operation. `preparation_failure` is retryable for `session/load`, and for
`session/new` only with cleanup status `verified`. `malformed_response` is retryable only for
`session/load` of the exact persisted vendor session because the prior response completed.
`timeout`, `transport_closed`, `outcome_unknown`, and `unclassified_adapter_failure` are terminal
for a same-Adapter-incarnation retry. Any non-retryable failure, or any load without its persisted identifier,
makes the matching authenticated retry change the binding to unavailable with reason
`rearm_outcome_unknown` and take the terminal-release path without another ACP call.

For a harness acknowledgment, the lane changes `acknowledged` to `released` with one
`Ledger.claim_next/3` eligibility check due. Before it invokes that check, it atomically marks the
due action consumed, clears rearm-pending state, and releases turn admission. A lane crash before
the consumed mark restores the due action; a crash after the mark cannot repeat it, and the normal
lane-manager nudge remains the liveness path for queued work. Without a crash, the releasing
mailbox turn invokes the eligibility check once. A duplicate acknowledgment returns the released
receipt and performs no release or eligibility check.

A terminal release from rearm-pending requires the credential mutation seam to have committed the
same generation as `unavailable` or `revoked`. The lane re-reads that row, changes the recovery row
to `released` with no eligibility check due, clears pending state, and performs no
`Ledger.claim_next/3` call. A post-activation repair does not reactivate the prior generation. A
terminal-release request without that durable result returns
`session_binding_rearm_terminal_uncommitted` and leaves the lane pending.

Nudges cannot starve a retry by starting work: a pending-state nudge performs no database claim.
The lane processes a matching retry after the finite set of mailbox messages already accepted
before that call, and each intervening nudge performs one state check. The lane uses no elapsed-time
threshold to release, retry, or classify the state.

Acceptance link: AC-15, AC-16, AC-20.

## 7. Acceptance

All tests use fixture markers, fixture tokens, an isolated database, or a fixture gateway. No test
uses a production session, production marker, active assignment row, or production gateway.

### AC-01 — valid bound dispatch

Given a schema-version-2 marker for session A and an anchor whose four values match it,  
When the CLI builds a dispatch request,  
Then the request uses marker A's URL and token, includes A's key, credential identifier,
generation, host, root-digest, and provenance-digest headers, and the gateway
resolves the bearer principal to session A.

Traces: I-02, I-03, I-04; R-01, R-05, R-11, R-25.

### AC-02 — trusted-root authority

Given a marker whose `trustedRoot` or `host` differs from the prepared database binding,  
When placement verifies the marker or the gateway activates it,  
Then a root difference returns `session_binding_root_mismatch`, a host difference returns
`session_binding_host_mismatch`, and the token remains inactive.

Given a marker whose created-at time, created-by principal, or cause differs from its prepared
binding, when Placement verifies it, then it returns `session_binding_provenance_mismatch` and the
token remains inactive.

Given fixture derivation makes sessions A and B resolve to one trusted root and A's valid marker
already exists,  
When Placement materializes B's pending marker,  
Then it returns `session_marker_custody_mismatch`, leaves A's marker byte-for-byte unchanged, and
B's token remains inactive.

Traces: I-05, I-18; R-01, R-05, R-06, R-08.

### AC-03 — parent and nested markers cannot select identity

Given session A's complete anchor, cwd inside session B's trusted root, and markers for A and B,  
When session A runs a CLI command,  
Then the filesystem fixture records a read of A's exact marker only, the request uses A's token,
and the gateway attributes the request to A.

Given no session anchor, cwd below a marker, a valid provisioned operator endpoint, and no explicit
identity flag,  
When the caller runs a command that requires identity,  
Then the CLI returns `identity_required` and does not read the cwd marker.

Traces: I-01, I-12; R-14, R-15, R-24.

### AC-04 — missing, partial, malformed, and legacy input

Table-driven CLI fixtures assert these exact results with exit code `1` and zero network calls:

| Fixture | Error code |
| --- | --- |
| one, two, or three anchor variables | `session_anchor_incomplete` |
| complete anchor with a non-UTF-8 value, relative marker path, empty key/URL, invalid identifier, or non-absolute/unsupported URL | `session_anchor_invalid` |
| anchored marker absent | `session_marker_missing` |
| invalid JSON | `session_marker_invalid` |
| required field other than `schemaVersion` absent or wrong type | `session_marker_invalid` |
| unknown version-2 field | `session_marker_invalid` |
| duplicate version-2 member name | `session_marker_invalid` |
| token, key, identifier, generation, host, URL, trusted root, created-at, created-by, or cause fails R-20 semantic validation | `session_marker_invalid` |
| schema version absent | `session_marker_legacy` |
| schema version not equal to `2` | `session_marker_version` |

Multi-fault fixtures assert R-14's order. In particular, a missing marker plus operator endpoint
returns `session_marker_missing`; an invalid complete anchor plus missing marker returns
`session_anchor_invalid`; a symlink with wrong mode returns `session_marker_symlink`; and an
unsupported schema with unknown fields returns `session_marker_version`. Each case performs zero
fallback reads after the deciding fault.

Traces: I-02, I-12; R-16, R-17, R-20, R-21, R-45.

### AC-05 — symlink and moved-root input

Table-driven CLI filesystem fixtures cover a symlinked registered base, trusted-root component,
marker file, and marker whose containing trusted root is a symlink. Each case returns
`session_marker_symlink`.

Deterministic path-swap fixtures replace an intermediate directory pathname and the final marker
pathname after their no-follow opens. The resolver validates and reads the held descriptor chain or
returns a local refusal; it does not read either replacement.

A regular marker whose mode differs from `0600` returns `session_marker_permissions`.

A marker copied to a path other than `<trustedRoot>/.tightbeam-session` returns
`session_marker_root_mismatch`. Each case exits before network dispatch.

Traces: I-03, I-05, I-14; R-07, R-18, R-19, R-23, R-45.

### AC-06 — anchor and marker mismatch

Given a valid marker and an anchor with a different session key, credential identifier, or gateway
URL,  
When the CLI resolves the endpoint,  
Then it returns `session_marker_mismatch`, reads no fallback source, and sends no request.

Traces: I-02, I-03, I-12; R-14, R-22, R-45.

### AC-07 — gateway binding gate

Table-driven router fixtures assert:

| Token and claims | HTTP status | Public code |
| --- | ---: | --- |
| active token plus matching claims | downstream identity result | downstream result |
| active token plus missing claim | 401 | `session_binding_required` |
| active token plus malformed or mismatched key, identifier, generation, host, root digest, or provenance digest | 401 | `session_binding_mismatch` |
| active token plus a duplicated binding header | 401 | `session_binding_mismatch` |
| retired, unavailable, revoked prior-generation, or pending token | 401 | `auth_failed` |
| unknown token | 401 | `auth_failed` |

Pending and unknown tokens with missing headers still return `auth_failed`. An active token with two
missing headers returns `session_binding_required`. Each refusal occurs before role, user, or process
resolution.

Traces: I-04, I-11; R-03, R-25, R-26, R-27, R-28, R-44.

### AC-08 — stale and moved markers

Given an unchanged generation-`n` marker at its original root after generation `n + 1` commits,  
When its original anchor invokes the CLI,  
Then local checks pass and the gateway returns `auth_failed` for the revoked token.

Given that marker copied to the generation-`n + 1` root without a rewrite,  
When the generation-`n + 1` anchor reads it,  
Then the CLI returns `session_marker_mismatch` and sends no request.

Given a fixture anchor that retains generation `n`'s key and credential identifier but names the
copied path,  
When the CLI reads the copy,  
Then it returns `session_marker_root_mismatch` and sends no request.

Given a retired fixture session whose last marker remains byte-for-byte unchanged,  
When retirement commits and its last anchor invokes the CLI,  
Then the retirement transaction has one revoked current credential, a null legacy token, and one
`session_binding_revoked` event with cause `retirement`; local checks pass, and the gateway returns
`auth_failed` without selecting an identity.

Given the credential transition is forced to fail inside a fixture retirement transaction,  
When retirement is attempted,  
Then the session remains active, its current credential remains active, its null legacy token and
last marker remain unchanged, and no retirement event exists.

Traces: I-04, I-07; R-04, R-23, R-28, R-42.

### AC-09 — concurrent adapter isolation

Given fixture sessions A and B on one shared adapter process,  
When `session/new`, `session/load`, and `session/fork` requests overlap under a deterministic barrier,  
Then each recorded harness request contains its own four anchor values and process environment
remains unchanged.

Table-driven overlay fixtures attempt each anchor name for each harness and host. Every attempt
returns `reserved_env_name` and leaves the overlay table unchanged.

Traces: I-08, I-09; R-10, R-11, R-12, R-13.

### AC-10 — local and remote materialization

Given fixture local and remote hosts,  
When Placement materializes a marker,  
Then the resulting regular file has mode `0600`, the normalized trusted root, the exact version-2
fields including created-at time, created-by principal, and cause, and no token byte
in recorded command arguments or event fields.

Table-driven fixtures cover a missing registered host, a non-absolute registered base, a symlinked
trusted-root component, wrong marker mode, malformed JSON, unknown field, duplicate member name,
binding root mismatch, binding host mismatch, and provenance mismatch. The first two cases return
`host_root_invalid`. Each other refusal returns the exact R-05 through R-08 code without replacing
the registry row or existing marker.

Deterministic local and fixture-remote path-swap cases replace a base component, trusted-root
component, temporary-marker pathname, and final-marker pathname after
their no-follow opens. Placement completes against the held descriptor chain or returns the named
refusal; it never reads or writes the replacement.

Marker replacement fixtures prove that an exact active or pending marker is an unchanged no-op and
that an inactive prior marker for the same session or a matching legacy marker can be replaced. A
malformed marker, non-marker file, or marker not proven to the same session returns
`session_marker_custody_mismatch` and remains byte-for-byte unchanged.

Crash and retry fixtures stop after writing `.tightbeam-session.tmp.<credentialId>`, before rename,
and after rename. A retry reuses only a matching temporary file. Cleanup removes only that matching
name. A different temporary or final marker remains unchanged and returns
`session_marker_custody_mismatch`.

The test covers local, remote, and each relocation direction.

Traces: I-05, I-10, I-14; R-06, R-07, R-08, R-09, R-35.

### AC-11 — real adapter carrier fixture

Given `@agentclientprotocol/codex-acp` `1.1.4` with the A-06 registry integrity runs with Codex CLI `0.146.0` at
`/opt/homebrew/bin/codex` SHA-256
`134063e133f0b4244fa3b251acf973d4fe4b4aeeacbdc135211bf480f59f1477`, and
`@agentclientprotocol/claude-agent-acp` `0.66.0` with the A-06 registry integrity runs with Claude Code `2.1.227` at
`/opt/homebrew/bin/claude` SHA-256
`7432511ba3be818e01f23f6eef8630d214a8b618451e188c3c7d61a987eef6c7`, against a fixture gateway and
isolated test home, and the fixture has recorded each resolved adapter entry point and package
bundle SHA-256,  
When each harness receives `session/new`, `session/load`, and `session/fork` for sessions A and B,  
Then a tool subprocess in each session prints only that session's four non-secret anchor values.
The fixture records the exact ACP-to-vendor field mapping. It proves that `session/load` reaches the
vendor's persisted-session re-entry path; it exercises no `session/resume` operation. The harness
captures adapter request and response envelopes with secret fields redacted and commits them as
deterministic fixtures. No production work row or session participates.

Traces: I-08, I-09, I-16; R-10, R-12.

### AC-12 — spawn activation seam

Given a fixture spawn,  
When marker preparation has not committed,  
Then the token returns `auth_failed` and no harness turn starts.

A deterministic database barrier proves that the complete pending row becomes visible in one
transaction or no credential field becomes visible.

When atomic marker rename succeeds and the gateway binding transaction commits,  
Then the token plus matching claims authenticates and `sessions.cliToken` remains null. A forced marker-write failure returns a named
spawn error and leaves no active credential. When matching-marker cleanup succeeds, it also leaves
no session, role, idempotency projection, or pending credential. When cleanup finds a marker with a
different credential identifier, the pending token stays rejected, the marker stays unchanged, and
the same idempotency retry resumes cleanup.

Given marker rename succeeds and activation fails before commit,  
When the same idempotency key retries with the matching marker present,  
Then the first attempt returns `session_binding_activation_failed`; the retry reuses the pending
generation, token, identifier, created-at time, created-by principal, and cause and commits
activation. With the marker absent, it rematerializes
the persisted tuple. With a different identifier, it returns `session_binding_cleanup_failed`,
preserves the marker, and keeps the pending token rejected.

A transition fixture that changes the pending tuple's created-at time, created-by principal, or
cause returns `credential_provenance_immutable`, changes no row, and emits no activation event.

Direct database fixtures that omit a non-null binding field, use a non-positive generation or
created-at time, use an updated-at time before created-at, put a NUL byte in created-by, create
a second current row, create a second pending row, use a null root outside unavailable
reasons that R-03 permits or a revoked row, name an unregistered host, use an empty created-by
principal, use an invalid cause, or use an invalid
state/reason combination fail a schema constraint. A
source-ownership fixture fails when a production file other than `lib/tightbeam/org.ex` names
`session_credentials`.

Traces: I-06, I-07, I-11, I-18; R-01, R-02, R-03, R-04, R-08, R-30, R-31.

### AC-13 — relocation linearization and failure recovery

A deterministic barrier test pauses before turn-fence acquisition, before database commit, after
database commit, and before turn-fence release for each relocation direction.

If a fixture turn is running before acquisition, relocation returns `session_turn_running` and
creates no pending row or destination marker.

Before commit, only generation `n` authenticates. After commit, only generation `n + 1`
authenticates. A pre-commit failure removes only the matching prepared destination, rearms the
harness with generation `n`, and releases the fence only after that rearm. A post-commit
source-removal failure leaves generation `n` rejected and records cleanup failure. A retry cannot
remove a marker whose credential identifier differs from the stale generation. A new turn cannot
start after fence acquisition and before rearm completes.

A pre-commit destination cleanup with a different credential identifier preserves the file and
pending row, emits reason `marker_credential_mismatch`, and makes the next relocation
request resume cleanup before it prepares another generation.

Given different normalized source and destination trusted roots, the transfer fixture records
every non-marker source entry and no `.tightbeam-session` entry or source-marker byte. Before commit,
the source final marker still names generation `n` and the destination final marker names the
prepared generation `n + 1`.

Given source and destination normalized trusted roots are equal, relocation returns
`session_relocation_same_root` before turn-fence acquisition. The fixture records no session-host
change, credential row, marker write, workdir copy, source removal, or event.

Traces: I-06, I-07, I-14, I-17, I-18; R-01, R-02, R-04, R-32, R-33, R-34, R-35.

### AC-14 — identity-selection compatibility

Against a valid active session binding, existing integration cases prove held-role success,
unheld-role `role_not_held`, matching-owner success, other-user `identity_not_yours`, session
process refusal, zero-role behavior, and ambiguous-role behavior.

Against an operator endpoint, existing cases prove explicit role, owner-user, non-reserved process,
and reserved-process behavior.

Traces: I-13; R-29.

### AC-15 — migration availability

Given an isolated database with reachable and unreachable active session fixtures,  
When migration reaches the explicit no-running-turn boundary or observes a running turn's
terminal event,  
Then reachable sessions receive active version-2 bindings and rearmed anchors. Unreachable sessions
become unavailable with `host_unreachable`, a null trusted root, and tokens that return
`auth_failed`. Global agent-turn readiness remains false until each active row is in one of those
two states and each retired legacy token is null. It can then become true while unavailable
sessions remain individually unable to start a turn.

Given a reachable session whose fixture marker writer fails after generation `1` is prepared,  
When migration handles that failure while it holds the session turn fence,  
Then the binding is current and unavailable with `migration_materialization_failed`,
`sessions.cliToken` is null, the token returns `auth_failed`, and the fence is released only after
the unavailable transaction and event commit. A missing or matching marker is absent after cleanup.
A marker with a different credential identifier remains unchanged and a redacted
`session_binding_cleanup_failed` event exists.

Given migration activation commits and fixture harness rearm fails, the gateway returns
`session_binding_rearm_failed`, records one redacted `session_binding_rearm_failed` event with
reason `harness_rearm_failed` and cause `upgrade`, keeps generation `1` active and its marker
unchanged, enters R-48 rearm-pending state before the call returns, and records no turn start. A
matching same-Adapter-incarnation retry with a retryable R-48 envelope and an Adapter replacement with a safe R-38
operation both rearm generation `1`, create no generation `2`, and release the session fence only
after the rearm acknowledgment. A non-retryable same-Adapter-incarnation envelope instead commits
`rearm_outcome_unknown`, performs no later ACP call, and takes the terminal-release path. The
restart uses a new `restart_repair` attempt and keeps global intake closed until acknowledgment and
successful release or until the R-38 failed-restart transaction commits its terminal release.

Given two legacy sessions whose fixture derivation produces one trusted root and session A's marker
already occupies it, when migration reaches session B, then B becomes unavailable with
`migration_materialization_failed`; A's marker remains byte-for-byte unchanged and neither B's new
nor legacy token authenticates. The product creates no ownership, lease, inventory, or custody
adjudication row.

Given a registered host with a non-absolute base, migration makes each affected active session
unavailable with `host_root_invalid`, writes no marker, and clears its legacy token. A retired
session receives no credential row and has a null legacy token after its terminal transaction.

Given a reachable host whose registered CLI reports the prior version, migration makes each active
session current and unavailable with `cli_version_mismatch`, writes no marker, and returns
`host_cli_version_mismatch` for placement. After the fixture CLI reports the exact release version,
recovery creates the next generation, activates its marker, and rearms the session before a turn
starts.

A deterministic recovery barrier pauses before turn-fence acquisition, after acquisition and
before activation, after activation and before harness rearm acknowledgment, and after
acknowledgment and before fence release. If a fixture turn is running before acquisition, recovery
returns `session_turn_running` and creates no pending generation or marker. After acquisition, a
concurrent turn attempt produces no turn-start event and reaches no harness until the fence
releases. Before activation, only the current unavailable state is visible. After activation, only
generation `n + 1` authenticates, but the concurrent turn remains unstarted. After rearm
acknowledgment and fence release, that turn starts with generation `n + 1`'s exact anchor.

Given recovery activation commits and fixture harness rearm fails, the gateway returns
`session_binding_rearm_failed`, records one redacted `session_binding_rearm_failed` event with
reason `harness_rearm_failed` and cause `host_recovery`, keeps generation `n + 1` active and its
marker unchanged, enters R-48 rearm-pending state before the call returns, and records no turn
start. A matching same-Adapter-incarnation retry with a retryable R-48 envelope rearms generation `n + 1`,
emits no second activation event, creates no generation `n + 2`, and releases the fence only after
the acknowledgment. A non-retryable envelope instead commits `rearm_outcome_unknown`, performs no
later ACP call, and takes the terminal-release path.

Table-driven crash fixtures use both R-41 version-2 shapes. They stop the fixture lane before the
durable guard commit, after that commit and before activation, after activation and before dispatch,
after dispatch and before adapter outcome, after adapter outcome and before result commit, and after
result commit and before release. AC-20 defines the exact result at each cut. They also stop the
fixture Adapter after a dispatched receipt and after an acknowledged receipt. After
`AdapterCoordinator` observes its `DOWN` and advances the adapter generation, global intake remains
closed, the prior Adapter and its owned ACP connection are down, an unresolved dispatched
`session/load` receipt has one `outcome_unknown` event, and the boot path rearms the same generation
`n + 1` through a new `restart_repair` load of its exact persisted vendor session. It creates no
generation `n + 2` and opens turn intake only after the new rearm acknowledgment and fence release.
For an unresolved `session/new` receipt, or a load whose binding has no persisted vendor session
identifier, the fixture instead records one unavailable transition with reason
`rearm_outcome_unknown`, zero later ACP calls, terminal fence release, and no turn start.

Given restart rearm does not acknowledge, one transaction records one redacted
`session_binding_rearm_failed` event with reason `harness_rearm_failed`, cause `restart_repair`,
and principal `process:tightbeam`; makes generation `n + 1` unavailable with
`rearm_outcome_unknown`; and releases the attempt terminally. The marker remains unchanged, no
turn starts, the gateway performs no later ACP call for that attempt, and global readiness can
advance after the terminal fence release. The fixture submits no same-Adapter-incarnation retry and creates no
generation `n + 2`.

A repeated failed check against the unchanged mismatch leaves the unavailable generation and event
count unchanged.

Crash fixtures stop the fixture gateway after the migration-start record, after a pending binding,
and after marker rename. On restart, the gateway enters migration mode before intake opens, reuses
the persisted tuple, and reaches exactly one R-40 terminal result without minting another token,
identifier, or generation or changing its created-at time, created-by principal, or cause.

Traces: I-15, I-17, I-18, I-20, I-21, I-22; R-01, R-03, R-36, R-38, R-39, R-40, R-48.

### AC-16 — observability and redaction

Given spawn, move, retirement, cleanup failure, unavailable host, migration start, binding-refusal,
and rearm-failure fixtures,  
When their event rows are serialized,  
Then each row has the required event fields and reason. A recursive value scan finds no fixture
token, credential identifier, ssh destination, base directory, raw trusted root, or marker path.

Every session-binding lifecycle event has a null root digest exactly when its binding has a null
trusted root under R-03. Otherwise it has a 64-character lowercase hexadecimal root digest. Each
event fixture asserts cause and durable principal. Rotation produces one rotated event for the new
generation. Retirement produces one revoked event in the same transaction that retires the session.
Unavailable and cleanup-failure fixtures assert the exact reason lists in R-43. Table-driven binding
refusals assert the exact internal reason list in R-44 while their public responses remain those in
R-27 and R-28. Rearm-failure fixtures assert reason `harness_rearm_failed`, cause `upgrade`,
`host_recovery`, or `restart_repair`, the matching durable principal, the active generation, and no
token, credential identifier, or raw anchor value.

The rearm-failure fixture corpus is captured from actual isolated `Tightbeam.Acp.Conn` and
`Tightbeam.Acp.Adapter` calls, not authored result terms. A fixture ACP child emits one JSON-RPC
error, withholds one response until `Conn` returns `:timeout`, closes its port until `Conn` returns
`:closed`, emits a success missing its required session field, and acknowledges `session/new`
before refusing model preparation so Adapter returns its cleanup-bearing preparation failure. The
test stores the captured returned values and feeds those same values through Adapter normalization
and R-43 redaction. A gateway-crash barrier supplies `outcome_unknown`.

For each Terms union tag, the stored envelope equals the captured value after the exact Adapter
normalization and R-43 redaction algorithm. A table injects an unknown JSON value, non-UTF-8 binary,
non-byte bitstring, improper list, proper list with a non-JSON descendant, map with a non-text key,
map with a non-JSON descendant, non-finite float, other atom, tuple, PID, port, reference, and
function. Each maps to its one fixed `unclassified_adapter_failure` class; no rendered, encoded,
persisted, or logged source payload appears in the recovery row, event, or log capture. The redaction assertion covers
operation, protocol code, message, remaining data keys, scalar values, list order, nesting, source
key preservation, longest-first secret replacement, named sensitive keys, POSIX paths,
drive-letter paths, and UNC paths. A recursive value scan finds none of the I-10 secret or path
values in the envelope.

The migration-start fixture has the global event shape in R-43, a null reason, cause `upgrade`, and
principal `process:tightbeam`. Every session, host, generation, schema, root, credential, transport,
and path field is null or absent as R-43 requires.

Traces: I-10, I-21, I-22; R-04, R-09, R-42, R-43, R-44, R-45, R-48.

### AC-17 — version, upgrade, and rollback

Given the prior CLI, new CLI, prior gateway, and new gateway fixture matrix,  
When each pair dispatches,  
Then mismatched protocol versions return existing `426 incompatible_cli`; the new pair rejects a
legacy marker; and the prior pair parses a version-2 marker's `url` and `token`. A new CLI in a
manual shell does not read a cwd marker unless that shell has a complete session anchor.

Given any active or unavailable R-40 terminal binding, or any retired session after its R-39
terminal result, a direct database fixture proves that its legacy `sessions.cliToken` field is
null.

Given a legacy database with only the `model-identity-v1` stamp and no migration-start record, when
the prior gateway fixture boots, then its existing shape check succeeds. No binding, marker, event,
setting, or second stamp is written.

Given an active or retired legacy session whose host alias has no registered row, when
the new gateway preflights migration, then it returns `session_host_unregistered` without writing a
migration-start record, fence, binding, marker, or event. The prior gateway fixture still
accepts the unchanged legacy shape.

Given the first migration-mode transaction, when it commits, then the fixture observes the exact
migration-start record from Terms, the additive `session-binding-v2` fence row, and one migration
start event before any binding or marker mutation. A repeated begin call preserves all
three. A malformed existing record returns `session_binding_migration_record_invalid`. An
inconsistent record/fence combination returns `session_binding_migration_fence_invalid`. Either
refusal starts no migration operation.

A source-ownership fixture fails when a production file other than `lib/tightbeam/schema.ex`
mutates `schema_stamp`.

Given the migrated database has both shape rows and the migration-start record, when the prior
gateway fixture boots, then it raises its existing multiple-shape `ShapeError` before schema
bootstrap or intake. It writes no row or file. Restarting the current release accepts the exact
pair and resumes migration or forward repair.

Fresh-bootstrap fixtures prove that `session-binding-v2` alone with no migration-start record is the
stable fresh shape, opens intake after normal bootstrap, and makes the prior gateway refuse its
different single shape. A record/fence mismatch returns
`session_binding_migration_fence_invalid`. Repository release guidance states that post-migration
recovery uses a forward current release, not an earlier package.

While the fixture gateway is in migration mode, spawn, relocation, retirement, and host registration each
return `migration_in_progress` and create no session, credential, marker, or host-row change.

A registered-host version fixture proves that a missing, malformed, prior, or future pre-1.0 CLI
version returns `host_cli_version_mismatch` before marker write or binding activation. Only the
exact release version proceeds. Spawn and relocation fixtures also prove that the refusal creates no
session, credential, marker, or host mutation. The packaged local pair passes the assembly
version-smoke gate.

Traces: I-15, I-19; R-21, R-36, R-37, R-38, R-40, R-41.

### AC-18 — operator endpoint preservation

Given no session-anchor variable,  
When a complete `TIGHTBEAM_URL` plus `TIGHTBEAM_TOKEN` pair exists,  
Then the CLI selects that named operator endpoint.

Given no pair,  
When a valid provisioned `gateway.json` exists,  
Then the CLI selects that provisioned operator endpoint.

Traces: I-13; R-15.

### AC-19 — gates and reality check

The implementation passes:

- Rust unit and CLI integration tests for the named CLI files;
- `mix test` for the named Elixir suites;
- `sh packaging/assemble.sh`;
- the isolated real-adapter fixture in AC-11;
- an isolated end-to-end fixture where a session-A process runs from session B's nested workdir and
  the gateway records session A.

The final diff changes only R-46 files or cites a canonical spec amendment.

A repository text fixture fails if the named R-47 files describe cwd traversal, ancestor-marker
selection, or workdir presence as a session identity source. It passes the canonical anchor-bound
and operator-shell statements in R-47.

Traces: I-01, I-13, I-16; R-46, R-47.

### AC-20 — returned-failure lane fence

Given a fixture lane, its current Adapter checkout, and an inactive next credential generation at
a held turn boundary,  
When deterministic barriers stop the lane before the durable `guarded` commit, after that commit
and before activation, after activation and before a `prepared` receipt, after `prepared` and before
`dispatched`, after `dispatched` and before adapter outcome, after adapter outcome and before result
commit, and after result commit and before release,  
Then the before-guard cut records no binding or ACP effect. At each later cut, a replacement lane
restores the exact durable phase before accepting a nudge and records no turn start. The
after-guard and after-activation cuts continue the same attempt. The prepared cut records zero ACP
calls. The dispatched and after-outcome cuts record exactly one ACP call, and the replacement lane
joins or consumes the current Adapter's retained result. The after-result cut returns that stored result without
another ACP call or event.

Given activation fails after `guarded` commits but before an ACP dispatch,  
When the existing migration or recovery transaction preserves the prior binding or commits the
named unavailable result,  
Then the attempt becomes `released` with `activation_not_committed`, no dispatch receipt or
`session_binding_rearm_failed` event exists, and no fabricated rearm-pending state is required.

Given each captured AC-16 failure value, an `upgrade` or `host_recovery` cause, and an active
generation `n`,  
When the current Adapter returns it for the initial dispatch,  
Then one transaction stores the matching closed-union envelope, moves the receipt to `failed` and
the attempt to `pending`, records one failure event, and the lane enters the complete R-48
rearm-pending state before returning `session_binding_rearm_failed`. A queued nudge produces zero
`Ledger.claim_next/3` calls and zero turn-start events.

Given the pending state and table-driven retry claims that alter adapter key, Adapter PID, Adapter
generation, authentication route, principal, operation-attempt identifier, session key, credential
generation, or cause,  
When each claim invokes the retry seam,  
Then an adapter-key, Adapter-PID, Adapter-generation, authentication-route, or principal mismatch
returns `session_binding_rearm_wrong_process`; a session-key, operation-attempt-identifier,
generation, or cause mismatch returns `session_binding_rearm_stale`. Each fixture records zero ACP
calls, binding changes, recovery-row changes, and rearm lifecycle events.

Given the boot path must `restart_repair` generation `n` through the safe R-38 branch,  
When it obtains the current `{adapter_key, Adapter PID, Adapter generation}` checkout from
`AdapterCoordinator` and submits the initial attempt with principal `process:tightbeam` and matching
attempt fields,  
Then the lane accepts the internal call without a bearer token and dispatches one rearm of
generation `n`. A wire request that asserts `process:tightbeam` remains refused by the existing
reserved-principal rule. If that dispatch returns any failure envelope, the same transaction stores
the failed receipt and event, makes generation `n` unavailable with `rearm_outcome_unknown`,
changes the attempt to `released`, and enables terminal fence release. It accepts no retry and
performs no later ACP call.

Given a pending `session/new` attempt whose stored envelope is `timeout`, `transport_closed`,
`malformed_response`, `outcome_unknown`, `unclassified_adapter_failure`, or
`preparation_failure` with cleanup status `unverified`,  
When the retry seam receives a new retry-request identifier with the matching authenticated
Adapter incarnation,  
Then the gateway makes the active binding unavailable with reason `rearm_outcome_unknown`, takes
the terminal-release path, and records zero later ACP calls. An `acp_error` or preparation failure
with cleanup status `verified` instead admits one serial `session/new` retry. For `session/load`,
`acp_error`, `malformed_response`, or `preparation_failure` admits one serial load of the same
persisted vendor session identifier; `timeout`, `transport_closed`, `outcome_unknown`, or
`unclassified_adapter_failure` takes the same terminal path without another ACP call.

Given two matching retry calls with one retry-request identifier overlap at a deterministic ACP
barrier,  
When the adapter returns one failure or one acknowledgment,  
Then the fixture records one receipt, one ACP call, one result shared by both callers, and no more
than one failure event. Repeating the identifier returns that result without another ACP call or
event. A different identifier while the receipt is `dispatched` returns
`session_binding_rearm_retry_in_progress`.

Given a matching retry receives a harness acknowledgment,  
When the lane consumes the acknowledged attempt without crashing,  
Then it marks the eligibility action consumed, clears rearm-pending state, releases admission, and
invokes the `Ledger.claim_next/3` eligibility check once. A crash before the consumed mark restores
one due action. A crash after the mark records no duplicate check; a subsequent lane-manager nudge
can claim queued work. A duplicate success returns the released result and produces no second
release or eligibility check.

Given a terminal-release request,  
When the fixture binding lacks the matching unavailable or revoked result,  
Then the lane returns `session_binding_rearm_terminal_uncommitted` and remains pending. After the
fixture commits an unavailable or revoked result for generation `n`, the same request clears
pending state and records zero `Ledger.claim_next/3` calls. A post-activation fixture does not make
the prior generation active.

Given the Adapter process stops with a `dispatched` receipt and no result,  
When `AdapterCoordinator` observes `DOWN` for that PID and advances the key to a later generation,  
Then one transaction records `outcome_unknown` and one failure event for the old receipt, and the
replacement Adapter never redispatches its retry-request identifier. For `session/load` with the exact
persisted vendor session identifier, the boot path keeps global intake closed, creates one
`restart_repair` load attempt for generation `n`, rejects the prior Adapter incarnation as
wrong-process, and opens intake only after its acknowledgment and release. For `session/new`, or a
load without that identifier, it makes generation `n` unavailable with reason
`rearm_outcome_unknown`, performs zero later ACP calls, releases through the terminal path, and
records no turn start.

Given 100 fixture nudges are accepted before and after one matching retry call,  
When the lane drains its mailbox,  
Then each unreleased-state nudge performs no ledger claim, the retry receives one adapter result or
one terminal result, and no turn starts before a successful or terminal release. No timer
participates in the result.

Traces: I-17, I-20, I-21, I-22; R-38, R-39, R-42, R-43, R-48.

## 8. Open Questions

### OQ-1 — BLOCKING: per-session carrier proof in vendor harnesses

The source-declared adapter package names, versions, registry integrity values, and install seam and
the observed Eezo vendor binaries are pinned in assumptions A-06 and A-07. The mismatched packages
currently present in Eezo's adapter directory are ineligible. No vendor carrier is selected until
the isolated fixture installs the pinned packages, records the resolved entry points and package
bundle hashes, and proves the carrier.

Before implementation proceeds beyond the isolated adapter carrier spike, AC-11 must prove:

1. `@agentclientprotocol/codex-acp` `1.1.4` maps ACP `session/new`, `session/load`, and `session/fork` to exact Codex
   `0.146.0` request fields and applies the four values.
2. `@agentclientprotocol/claude-agent-acp` `0.66.0` maps the same three ACP operations to exact Claude Code `2.1.227`
   request fields and applies the four values.
3. Each `session/load` proof reaches the vendor persisted-session re-entry path; no
   `session/resume` operation is claimed or tested for source baseline `be61cfc9`.
4. Internal tool subprocesses receive the values.
5. Two overlapping sessions do not exchange values.
6. Shared adapter process environment remains unchanged.

If either pinned adapter cannot satisfy these checks, the affected harness release is blocked. The
builder can change only the isolated adapter fixture or patch used to obtain the proof. The builder
must amend the canonical spec with the exact verified carrier mapping before changing another
product seam.

No other user-owned open question remains. The ruling for cwd outside the trusted root is explicit:
cwd does not select identity and does not confine a correctly anchored session.
