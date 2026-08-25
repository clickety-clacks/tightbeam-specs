# Unified first-user, first-device, and first-root cold start

Status: DRAFT for independent spec review. Target: Tightbeam 0.2.0.

Authority baseline:

- Product source: `clickety-clacks/tightbeam` main at
  `d00e06aea578d711e608637d38a97872487df15e`.
- Shared specs: `clickety-clacks/tightbeam-specs` main at
  `09d4118dc6b651f0d1468a723a4d7a7afa8ca045`.
- The product delta from the proven operational-parent baseline
  `8eeccbd6` to `d00e06a` changes repository guidance only. It does not change
  the cold-start code paths described here.
- Live evidence: `att_7578dbc1` and `att_91c37e8f`.
- Preserved first-user handbacks: `art_d1ccf807` and `art_c1eccb0a`.

This file is the only normative cold-start artifact for work item
`wi_8edbc2c4`. Companion work item `wi_20df0b1f` remains untargeted and points
to this file; it does not own a second specification.

## Goal

G1. A fresh Tightbeam 0.2.0 organization shall acquire its first human
principal, first usable device credential, and first operational root session
in one gateway-owned database transaction.

G2. The winning first-device pairing shall return an authenticated admin
device only after all three referents and their durable provenance commit.

G3. The resulting root shall make user-attributed CLI operations and the first
spawn legal before a client performs the later authenticated chat handshake.

G4. Tightbeam shall prevent the proven `add-user`-then-pair deadlock. The
documented install order shall be gateway boot, first-client pair, provider
onboarding, identity learning, and first turn.

G5. Tightbeam shall reject ordinary assertions of nonexistent users before
typed-target lookup, rails, audit events, or domain writes.

G6. Tightbeam shall provide a named, recoverable response for an incomplete
fresh database and shall document the proven database-reset ceremony without
deleting provider credentials.

G7. Existing claimed organizations and later-device pairing shall retain their
0.2 wire behavior except where this specification names a change.

The operating pattern taught by this specification is: **pair the first client
before `add-user`, onboarding, or spawning; reset only an incomplete fresh
database through the documented stop-and-move ceremony.**

## Non-Goals

NG1. This specification does not define visitor, guest, anonymous, or raw-org-
token impersonation policy. It only requires a canonical user row after the
existing authority policy permits a user assertion.

NG2. This specification does not add a general device-approval CLI. Later
devices continue through the existing pending and admin-approval mechanism.

NG3. This specification does not change user deletion because Tightbeam 0.2.0
has no user-deletion operation.

NG4. This specification does not change ordinary session spawning, role
fallback, device revocation, device denial, user promotion, or token rotation
after cold-start activation.

NG5. This specification does not make a model provider credential a
prerequisite for claiming an organization. Credentials remain outside
`state.db`; the admin onboards them after the claim.

NG6. This specification does not repair an inconsistent database in place.
It preserves the database for inspection and directs the operator to the
supported reset or backup-restore ceremony.

NG7. This specification does not implement, merge, release, deploy, mutate a
live organization, or open its own review lane.

## Terms

T1. **Identity graph** denotes the rows in `users`, `devices`, `sessions`, and
the singleton `cold_start_receipts` table. Other schema, configuration,
credential, event, or file rows do not make an organization claimed.

T2. **Cold state** denotes one database-owner transaction snapshot in which
all four identity-graph tables contain zero rows.

T3. **Claimed state** denotes a database with exactly one cold-start receipt
whose user, device, and root foreign keys resolve and satisfy I2-I5. A claimed
organization can contain additional users, devices, or sessions created after
the receipt.

T4. **Incomplete state** denotes any identity graph that is neither cold nor
claimed. Examples include a user without a device and root, a pending-only
first device, a receipt with a missing referent, and a Main whose operational
parent is not itself.

T5. **Claim request** denotes a valid protocol-version-1 WebSocket
`pair_request` received while the database owner observes cold state. Its
fields are `deviceId`, `claimedName`, and nullable `deviceInfo.platform` and
`deviceInfo.model`.

T6. **Request fingerprint** denotes SHA-256 over UTF-8 canonical JSON with
exactly these ordered keys: `deviceId` and normalized `userId`. It identifies
the logical device-to-principal claim. Cosmetic claimed-name changes and
device-info changes do not strand recovery when they normalize to the same
user. The fingerprint is an idempotency key, not an authentication credential.

T7. **First principal** denotes the normalized `userId` derived by the existing
`Devices.slug_user_id/1` behavior from the winning request's `claimedName`.
The claimed name is input to normalization; it is not an authenticated user
assertion.

T8. **First device** denotes the winning request's device row. It is
`allowlisted`, owns a non-null `tbt_` token, and belongs to the first principal.

T9. **Root session** denotes the first principal's canonical personal Main. Its
key comes only from `Org.personal_session_key/1`; new cold-start code shall not
reproduce or parse the key's string layout.

T10. **Activation** denotes the first successful token-authenticated socket
handshake by the first device. Activation sets the receipt's `activatedAt`
once. It does not create the root.

T11. **Exact bootstrap replay** denotes a pre-activation claim retry whose
fingerprint and device id match the receipt. It returns the already-committed
device token and receipt result without rotating the token or writing a second
event.

T12. **Ordinary identity assertion** denotes `asUser` or an equivalent user
principal constructed after cold start. It excludes `claimedName` on a pair
request.

T13. **Database set** denotes `state.db` and any sibling `state.db-wal` and
`state.db-shm` files that exist while the gateway is stopped.

## Assumptions

A1. `Tightbeam.DB` remains the only production database owner. Its
`BEGIN IMMEDIATE` transaction is the serialization boundary for concurrent
claim, pair, auth, and admin writes.

A2. `sessions.operationalParent` remains `NOT NULL REFERENCES
sessions(sessionKey)`. `Org.create_in_txn/2` represents a Main as a
self-parent and represents another session's default parent through
`Org.personal_session_key/1`.

A3. Gateway startup supplies the same resolved harness, provider, model,
local host, and default archetype inputs that current authenticated-chat Main
seeding uses. A missing provider credential does not make those identity
values unavailable.

A4. The first-pair wire already exposes unauthenticated claim authority to the
network location where the operator publishes the gateway. This specification
narrows its mutation to one atomic transaction; it does not introduce an
invite code or a wider endpoint.

A5. The deployment operator controls network exposure until the first claim.
An organization that requires a separate invitation ceremony must specify it
in later work.

A6. Provider credentials live under the base directory outside `state.db`.
Moving only the database set aside preserves those credentials, as proven by
`att_91c37e8f`.

A7. Current-main baseline evidence is bounded as follows: the release CLI
exists; Rust format and 248 Rust tests passed; the authoritative Mix run
exposed one timing-sensitive `EffortCheckinTest` failure which passed its exact
isolated rerun; and the product worktree remained clean. This specification
does not classify that unrelated timing flake as a cold-start failure.

A8. The 2026-08-25 standing Mike rule delegates technical ambiguity and
decision handling to this lane. The five inherited request seams are resolved
in AR1; none requires money or materially unagreed scope.

## Invariants

I1. Exactly one gateway-owned transaction shall change cold state to claimed
state. That transaction shall insert the first user, first device, root
session, cold-start receipt, and one accepted audit event.

I2. The first user shall have `isAdmin = 1` regardless of caller-supplied admin
flags. Cold-start pairing shall accept no admin flag.

I3. The first device shall belong to the first user, have status
`allowlisted`, and have one non-null token when the transaction commits.

I4. The root shall be active, built in, `kind = 'main'`, owned by the first
user, and self-parented through `operationalParent = sessionKey`. Its
`spawnedBy` shall be null and its creation origin shall be
`process:tightbeam`, because no human or session principal existed before the
transaction.

I5. The receipt shall be singleton id `1`. It shall name the user, device,
root, request fingerprint, cause `first_device_pair`, principal
`process:tightbeam`, accepted event id, `createdAt`, and nullable
`activatedAt`. It shall not store a device token or provider credential.

I6. A successful `pair_result` shall be emitted only after I1 commits. Any
exception before commit shall leave all I1 rows absent and shall return a
named failure without a token.

I7. The cold predicate and every I1 write shall run in the same database-owner
transaction. No CLI process, second SQLite connection, check-then-dispatch
sequence, or in-memory lock shall participate in the authority decision.

I8. An exact bootstrap replay before activation shall return the committed
result without a second identity mutation, token rotation, receipt, or event.
A same-device request with a different fingerprint before activation shall
return `bootstrap_closed`. After activation, the existing known-allowlisted-
device re-pair path shall rotate the token.

I9. A different device arriving after the winning commit shall follow the
ordinary claimed-org path. It shall receive `pair_pending`; it shall not
receive first-device authority.

I10. Any incomplete state shall fail closed with
`incompatible_cold_start_v1` at boot or `bootstrap_incomplete` if detected by
a live claim transaction. The failure shall name the README reset section and
shall not mutate identity rows.

I11. `tightbeam add-user` shall have one implementation: the ordinary
gateway-admin path. The Rust direct SQLite first-user writer and its dispatch
exception shall not exist. A no-identity invocation shall not create a user.

I12. After the existing credential policy admits an ordinary user assertion,
the authoritative actor-construction boundary shall require a canonical
`users` row. A missing row shall return `invalid_identity` before target
resolution, rail execution, accepted or denied event creation, and domain
writes.

I13. The actor-boundary existence check shall cover org-token `asUser`,
session-token `asUser`, and an implicit built-in-session owner. It shall not
change the existing authorization decision for a user that exists.

I14. New cold-start code shall call `Org.personal_session_key/1` and shared
in-transaction Main construction. It shall not contain the literal
`agent:main:clawline:` topology prefix.

I15. A database written by this contract shall prevent an older Rust direct
writer from inserting a user outside the gateway. The refusal shall leave the
database unchanged and name `bootstrap_owned_by_gateway`.

I16. Boot validation shall classify the complete identity graph on every boot;
it shall not infer a claim from user count alone.

I17. The README shall teach one first-order sequence. It shall not present
local `add-user` and client pairing as interchangeable cold-start paths.

I18. The reset ceremony shall move the database set as one stopped-gateway
unit, preserve it as a backup, leave `auth/` and other credential files in
place, restart on a new database, and pair the first client before any
`add-user` call.

I19. No accepted cold-start audit payload, doctor output, boot summary, or
error shall disclose a device token or provider credential.

## Architecture

### AR1. Resolved inherited seams

The standing lane-authority rule resolves the five preserved request seams as
follows. The new first-device deadlock evidence supersedes the earlier
recommendations for the first two rows; the request records remain provenance
for why the choices were explicit.

| Request | Resolution | Contract consequence |
|---|---|---|
| `dr_38c8fdb2` | `remove-cli-bootstrap` | Delete the Rust direct database writer. First-device pairing is the only cold claim surface. Ordinary `add-user` remains. |
| `dr_1ac42a7a` | `zero-identity-graph` | Cold means zero users, devices, sessions, and receipts. User count alone cannot classify the proven partial state. |
| `dr_4d95f4da` | `durable-receipt-replay` | The claim transaction writes the singleton receipt; exact pre-activation retry replays it. |
| `dr_9457c6e3` | `actor-boundary-only` | Canonical actor construction rejects nonexistent users. A broad user foreign-key migration remains outside this scope. |
| `dr_739be284` | `named-bootstrap-and-invalid-identity` | Bootstrap mismatch returns `bootstrap_closed`; ordinary ghost users return `invalid_identity`. |

These choices do not decide visitor-principal semantics. They require only
that any authority policy which elects a user principal must bind it to a
canonical user row.

### AR2. Ownership and module boundary

Add one gateway module, `Tightbeam.ColdStart`, as the owner of identity-graph
classification and claim orchestration. It receives the already-parsed pair
request and resolved gateway defaults from `Wire.Socket`. It opens exactly one
`Tightbeam.DB.transaction/2` and uses only `*_in_txn` helpers.

Refactor `Devices` to expose in-transaction pair and user insertion helpers.
Refactor the existing socket Main-seeding body into one shared
`Org.ensure_personal_main_in_txn/2` helper. `ColdStart` uses that helper inside
the claim transaction. Auth for later users shall call the same helper; the
helper shall remain convergent when Main already exists.

`Wire.Socket` shall call the cold-start coordinator for every pair request.
The coordinator shall classify and execute cold, exact-replay, incomplete, or
ordinary behavior without an earlier database read.

### AR3. Claim transaction

For a cold snapshot, `ColdStart` shall perform this ordered transaction:

1. Re-read the exact identity-graph counts and assert cold state.
2. Normalize `claimedName` with the existing slug behavior.
3. Resolve the default archetype from `org_settings`, falling back to
   `default`, and validate the supplied gateway defaults.
4. Insert the admin user with creation kind `cold_start`.
5. Insert the allowlisted device and mint its token.
6. Create the canonical personal Main through
   `Org.personal_session_key/1` and shared Main construction.
7. Append one `events` row with `kind = 'verb'`, `verb = 'cold-start'`,
   origin and principal `process:tightbeam`, and `sessionKey` equal to the
   root key.
8. Insert receipt id `1` with the event id and request fingerprint.
9. Re-read the three referents and assert I2-I5 before returning from the
   transaction callback.

The accepted event payload shall contain exactly `receiptId`, `cause`,
`userId`, `deviceId`, `rootSessionKey`, `isAdmin`, `deviceStatus`, `rootKind`,
and `operationalParent`. It shall not contain the claimed name, device-info
fields, token, org token, CLI token, or credential data.

`Wire.Socket` shall encode the existing successful `pair_result` from the
committed result. No new success frame or required client field is introduced.

### AR4. Receipt and user-origin schema

The current schema shape shall advance from
`coordination-fabric-v1-phase1-v5` to
`coordination-fabric-v1-phase1-v6`.

The `cold_start_receipts` table shall enforce:

- `id INTEGER PRIMARY KEY CHECK (id = 1)`;
- non-null foreign keys to `users(userId)`, `devices(deviceId)`, and
  `sessions(sessionKey)`;
- `cause IN ('first_device_pair', 'v5_observed')`;
- `principal = 'process:tightbeam'`;
- a non-null request fingerprint and event id for `first_device_pair`;
- null request fingerprint and event id for `v5_observed`;
- nonnegative `createdAt`; and
- nullable nonnegative `activatedAt`.

The `users` table shall gain required `creationKind` with the closed values
`cold_start`, `device_pair`, `admin_add`, and `legacy`. New gateway writes shall
always name the value. Ordinary pairing uses `device_pair`; authenticated
`add-user` uses `admin_add`; the v5 migration marks existing rows `legacy`.

A schema-owned insert guard shall reject a user insert that omits
`creationKind` with `bootstrap_owned_by_gateway`. This guard is the old-local-
CLI fence required by I15; a shape stamp alone cannot stop that CLI because
the deleted Rust path opens SQLite without asking the gateway.

### AR5. Pairing, retry, and activation

When receipt id `1` exists and `activatedAt` is null, the coordinator shall
compare the request to the stored claim:

- Matching device id and fingerprint returns the existing token and tuple.
- Matching device id with a different fingerprint returns a failed
  `pair_result` with reason `bootstrap_closed`.
- A different device proceeds through ordinary pairing and receives
  `pair_pending` when newly inserted.

The first successful auth transaction for the receipt device shall set
`activatedAt = COALESCE(activatedAt, now)` after validating the current token.
It shall not insert a second event. A later auth is a no-op for the receipt.

After activation, known allowlisted re-pair keeps the existing 0.2 contract:
it rotates the token and invalidates the previous token. Known pending,
denied, and revoked-device behavior remains unchanged.

### AR6. Root representation and first spawn

The root row shall use the existing `kind = 'main'` representation. Its own
session key is its operational parent. The transaction shall not invent a
placeholder parent, nullable parent, synthetic ancestor, or hardcoded role
name.

Because the root commits with the user, an org-token CLI call that asserts the
new canonical user can perform an otherwise-authorized first spawn before
client auth. The spawned session shall receive the canonical Main as its
operational parent through existing `Org.create_in_txn/2` behavior.

### AR7. Actor construction

Move canonical user existence into the authoritative identity-construction
step in `Wire.Router` or its extracted actor constructor. Perform it after the
current credential/ownership checks admit the assertion and before
`typed_target/3` or `Dispatch.call/2`.

Return HTTP 403 with stable error code `invalid_identity` and message
`asserted user does not exist` for a missing user. Use the same status, code,
and message for org-token `asUser`, session-token `asUser` whose admitted
owner row is missing, and an implicit built-in-session owner whose row is
missing. Do not echo the nonexistent id in the response.

The check shall not add an ownership restriction to existing org-token
`asUser`; that separate authority policy remains as it is. It shall not add
foreign keys to every historical user-like column.

### AR8. Boot validation and v5 migration

Schema migration and its stamp update shall be one atomic database-owner
operation. The exact v5 predecessor shall migrate as follows:

1. Rebuild `users` with `creationKind = 'legacy'` for every existing row and
   install the old-writer guard.
2. Create and validate `cold_start_receipts`.
3. If users, devices, and sessions are all empty, leave the receipt table
   empty and stamp v6.
4. Otherwise, find a deterministic legacy witness ordered by
   `(devices.createdAt, devices.deviceId)`: an allowlisted device with a
   non-null token, an admin owner, and that owner's active built-in personal
   Main whose `kind` is `main` and whose operational parent is itself.
5. If a witness exists, insert one activated `v5_observed` receipt for that
   tuple. Set both receipt times to migration time. Do not synthesize a
   historical event or request fingerprint.
6. If no witness exists, raise `incompatible_cold_start_v1`, roll the whole
   migration back to v5, and name the README incomplete-fresh-database reset
   section.

Every v6 boot shall validate T2-T4 and all receipt referents. A receipt-less
nonempty graph and a malformed claimed graph both refuse before the gateway
serves requests.

An older gateway shall refuse the v6 stamp. A supported rollback shall stop
both binaries and restore a pre-v6 database set; no process shall downgrade
v6 rows in place. The user insert guard supplies defense in depth against an
older direct-writer CLI placed beside a v6 database.

### AR9. Failures and observability

The pair surface shall use these stable reasons:

| Reason | Condition | Identity mutation |
|---|---|---|
| `bootstrap_closed` | Pre-activation same-device request does not match the winning fingerprint. | None |
| `bootstrap_incomplete` | A live transaction observes an identity graph that is neither cold nor claimed. | None |
| `bootstrap_failed` | The cold transaction raises or cannot commit. | Rolled back in full |
| `pair_pending` | A different device pairs after the winning commit. | Existing pending-device mutation only |

Boot-time structural failure uses `incompatible_cold_start_v1`, not a pair
reason. Ordinary nonexistent user assertions use `invalid_identity`.

The boot summary and `tightbeam doctor --json` shall report one of `open`,
`claimed`, or `incompatible`. `open` shall say `pair the first client before
add-user or onboarding`. `claimed` shall report receipt cause, user id, device
id, root key, and activation state. `incompatible` shall report the violated
invariant and the README reset-section name. None shall report tokens.

The gateway shall emit one structured error log for each
`bootstrap_incomplete` or `bootstrap_failed` response with the request device
id, identity-graph counts, reason, and rollback outcome. It shall not log
claimed name, tokens, authorization headers, or credentials.

### AR10. README order and database-reset recovery

Replace the current two-path cold-start text with one order:

1. Start the gateway.
2. Point the first client at `TIGHTBEAM_ADVERTISED_URL` and pair it with the
   intended name.
3. Verify that pairing succeeded and the catalog contains Main.
4. Onboard each provider credential as the new admin.
5. Learn the selected identity bundle.
6. Run a real turn in Main.
7. Use authenticated `tightbeam add-user ... --as-user <adminUserId>` only
   for later users.

The README shall state that 0.2 has no CLI-only first-user path. Running bare
`tightbeam add-user <userId>` cannot prepare a fresh org and must not be used
before pairing.

Add a section named **Recover an incomplete fresh database**. It shall:

1. Restrict the ceremony to a fresh database the operator intends to discard.
2. State that the database contains organization identity, sessions, work,
   and audit history, so a non-fresh database must be restored or investigated
   instead of reset.
3. Stop the gateway and verify it exited.
4. Move the complete database set to one timestamped backup location without
   deleting it.
5. Leave `auth/`, gateway configuration, installed binaries, and provider
   credential files in place.
6. Restart the gateway and verify doctor reports `open`.
7. Pair the first client before `add-user`.
8. Verify exactly one admin user, one allowlisted device, one receipt, and one
   active self-parented Main before continuing.

### AR11. Deletion assessment

**Add:** add the narrow `ColdStart` coordinator, singleton receipt, user-origin
field/guard, actor-boundary check, doctor state, and tests. A coordinator is
necessary because no existing module owns user, device, session, receipt, and
event writes in one transaction. Putting session defaults into `Devices`
would couple credential storage to topology; leaving orchestration in
`Wire.Socket` would preserve a second transaction boundary.

**Delete:** delete `cli/src/users.rs`, the `create_first_if_local` dispatch
branch, local-target classification helpers used only by that branch, and the
README claim that local `add-user` is a cold-start alternative. Accepting
those pieces preserves the split SQLite authority and recreates the proven
order deadlock. Deleting the whole `add-user` command would remove a valid
post-bootstrap admin operation, so only its cold exception is deleted.

**Refactor and accept:** retain the pair/auth frames, `tbt_` token class,
ordinary pending/approval behavior, canonical personal-Main representation,
and DB-owner transaction mechanism. Extract their in-transaction helpers so
the new coordinator composes existing rules instead of duplicating them.

### AR12. Traceability

| Contract | Acceptance proof |
|---|---|
| G1-G4, I1-I11, I14, AR2-AR6 | AC1-AC8 |
| G5, I12-I13, AR7 | AC9-AC10 |
| G6, I10, I15-I19, AR8-AR10 | AC11-AC15 |
| G7, I8-I9, AR5 | AC3-AC5 and AC16 |
| AR1 and preserved decision provenance | AC17 |
| AR11 deletion boundary | AC18 |

## Acceptance

AC1. **Atomic fresh claim.** Given a v6 database in cold state and valid
gateway defaults, when device `d1` sends a valid pair request claiming
`Alice`, then the response succeeds only after one transaction commits one
admin user, one allowlisted device with a token, one active built-in Main, one
receipt, and one accepted event. The user, device, root, receipt, and event
fields satisfy I2-I5. No token appears in the event.

AC2. **Statement-by-statement rollback.** Given the AC1 fixture and a fault
injected after each ordered write in AR3, when the claim runs once per fault,
then every run returns `bootstrap_failed`; users, devices, sessions, receipts,
and accepted cold-start events each remain at zero. A subsequent fault-free
claim succeeds.

AC3. **Concurrent different devices.** Given cold state and two barriers that
enter pair concurrently with different device ids, when the DB owner releases
both calls, then one call returns successful first pairing and the other
returns `pair_pending`. Exactly one admin, root, receipt, and cold-start event
exist. The pending device has no token and cannot authenticate.

AC4. **Concurrent identical retry.** Given cold state and two identical claim
requests for the same device, when both complete before activation, then both
responses contain the same committed token and tuple. The database contains
one device, receipt, root, user, and event. No token rotation occurs.

AC5. **Replay and activation boundary.** Given a committed claim whose first
response is lost, when the exact request repeats before auth, then it returns
the stored token without a write or event. When that token authenticates, the
receipt gains `activatedAt` once. When the device pairs again after activation,
then it receives a new token and the old token fails authentication.

AC6. **The proven bad order cannot mutate.** Given cold state, when a local
shell runs bare `tightbeam add-user alice`, then the command returns its
ordinary identity-required guidance and the four identity-graph tables remain
empty. When Alice's device pairs next, then AC1 succeeds rather than
`pair_pending`.

AC7. **The documented good order works.** Given cold state, when Alice pairs
first and then runs `tightbeam add-user bob --as-user alice`, then Bob is
created through the ordinary gateway path and is not admin unless `--admin`
was supplied. Alice's receipt and root do not change.

AC8. **First root and first spawn.** Given AC1 has committed but the client has
not sent auth, when the org-token CLI performs an otherwise-valid spawn as
Alice, then the spawn commits. Its `operationalParent` equals the session key
returned by `Org.personal_session_key("alice")`; the first root remains
self-parented. A source scan of the new cold-start code finds no literal
`agent:main:clawline:`.

AC9. **Ordinary ghost user refusal.** Given a claimed org with no user
`ghost`, when org-token `asUser=ghost` calls one read verb and one write verb,
then both return HTTP 403 `invalid_identity` with the fixed message before
typed-target lookup. No accepted or denied event and no domain row is added.

AC10. **Every actor constructor checks existence.** Given fixtures for an
org-token assertion, a session-token owner assertion, and an implicit built-in
owner whose user row is removed, when each constructs an actor, then each
returns the identical `invalid_identity` envelope. Given an existing user,
the same calls reach their pre-change authorization result. This test does not
assert new raw-org-token ownership policy.

AC11. **Empty v5 migration.** Given an exact v5 database with zero users,
devices, and sessions, when v6 boots, then migration stamps v6, adds the guarded
schema, leaves the receipt table empty, and doctor reports `open`. A first pair
then satisfies AC1.

AC12. **Healthy v5 migration.** Given an exact v5 database with a usable admin
device and its active self-parented personal Main plus later identity rows,
when v6 boots, then it selects the deterministic witness, marks all prior users
`legacy`, writes one activated `v5_observed` receipt, synthesizes no event, and
preserves every prior row and token. Known-device and later-device behavior
then satisfy AC16.

AC13. **Incomplete v5 refusal and reset recovery.** For each fixture—user only,
admin user plus pending device, allowlisted device without Main, Main with a
missing or non-self parent, and receipt with a missing referent—given no valid
legacy witness, when v6 boots, then it returns
`incompatible_cold_start_v1`, names the README reset section, and leaves the
schema stamp, schema objects, and queryable rows unchanged with
`PRAGMA integrity_check` passing. When the stopped-gateway database set is
moved aside, the gateway restarts, doctor reports `open`, provider credentials
remain available, and pair-first produces the AC1 tuple.

AC14. **Interrupted migration and rollback fence.** Given a healthy v5
database, when migration is interrupted after each rebuild/create/copy/stamp
step, then the whole step rolls back and a retry converges on AC12. Given the
resulting v6 database, when a v5 gateway opens it, then it refuses the v6 shape;
when an older direct-writer CLI attempts its old INSERT, then it receives
`bootstrap_owned_by_gateway` and adds no row. Restoring the stopped pre-v6
database set permits the v5 gateway to boot.

AC15. **Observable and secret-free.** Given open, claimed, and incomplete
fixtures, when boot summary and `doctor --json` inspect each one, then they
report the exact AR9 state and action. Given accepted, replayed, incomplete,
and failed claim attempts, when logs, events, and doctor output are searched,
then user/device/root provenance and rollback status appear where AR3 and AR9
require them; no `tbt_` token, org token, CLI token, authorization header,
claimed name, or provider credential appears.

AC16. **Warm compatibility matrix.** Given a claimed and activated org, when
an allowlisted device re-pairs, a new device pairs, a pending device re-pairs,
a denied device re-pairs, a token is revoked, and an admin approves a pending
device, then each frame, reason, token-rotation result, and derived admin value
matches the pre-change 0.2 behavior. Existing client J0 still receives
successful first pair, auth success, Main in `stream_snapshot`, and
`sync_complete` without a new required client field.

AC17. **Decision and scope audit.** Given the five inherited decision-request
records and the 2026-08-25 standing rule, when an independent reviewer checks
this file, then each request has exactly one AR1 disposition, the changed
recommendations cite the first-device evidence, visitor semantics remain in
NG1, and `wi_20df0b1f` remains untargeted with no second spec.

AC18. **Deletion boundary.** Given the implementation diff, when a reviewer
searches it, then the Rust direct user writer and its special dispatch helpers
are absent; one ordinary `add-user` gateway path remains; `ColdStart` owns one
transaction; Devices and Org expose shared in-transaction helpers; and no
second SQLite mutation authority, placeholder root, nullable operational
parent, or duplicate personal-Main constructor was added.

## Open Questions

There are no blocking or non-blocking open questions. AR1 resolves the five
inherited technical seams under standing lane authority. Money, materially new
scope, visitor-principal policy, and a separate invitation ceremony remain
outside this specification rather than hidden as unanswered holes.
