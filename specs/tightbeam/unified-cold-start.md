# Unified first-user, first-device, and first-root cold start

Status: BLOCKED on five inherited decision requests. Target: Tightbeam 0.2.0.

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

G2. The winning first-device pairing shall return an allowlisted admin device
credential only after all three referents and their durable provenance commit.

G3. The resulting root shall make user-attributed CLI operations and the first
spawn legal before a client performs the later authenticated chat handshake.

G4. Tightbeam shall prevent the proven `add-user`-then-pair deadlock. The
documented install order shall be gateway boot, first-client pair, provider
onboarding, identity learning, and first turn.

G5. Tightbeam shall reject ordinary assertions of nonexistent users before
typed-target lookup, rails, audit events, or domain writes.

G6. Tightbeam shall provide a named, recoverable response for an incomplete
fresh database or a lost first-pair response before activation. It shall
document the proven database-reset ceremony without deleting provider
credentials.

G7. Existing claimed organizations and later-device pairing shall retain their
0.2 wire behavior except where this specification names a change.

The operating pattern taught by this specification is: **pair the first client
before `add-user`, onboarding, or spawning; reset only an unusable fresh
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

T3. **Claimed state** denotes a v6 database with exactly one structurally
valid cold-start receipt. Its user, device, and root foreign keys resolve; the
device and root belong to the receipt user; the root is built in, has kind
`main`, and is self-parented; and the receipt fields satisfy AR4 for their
cause. A claimed organization can contain additional identity rows. Ordinary
post-claim changes to the receipt user's admin bit, the receipt device's
status or token, or the root's active state do not erase this historical
classification.

T4. **Incomplete state** denotes a v6 identity graph that is neither cold nor
claimed, or an exact v5 graph for which AR8 finds no valid legacy witness.
Examples include a user without a device and root, a pending-only first
device, a receipt with a missing referent, and a Main whose operational parent
is not itself.

T5. **Claim request** denotes a valid protocol-version-1 WebSocket
`pair_request` received while the database owner observes cold state. Its
fields are `deviceId`, `claimedName`, and nullable `deviceInfo.platform` and
`deviceInfo.model`.

T6. **Request fingerprint** denotes SHA-256 over UTF-8 canonical JSON with
exactly these ordered keys: `deviceId` and normalized `userId`. It identifies
the committed logical device-to-principal claim in durable provenance. The
pair surface shall not use fingerprint equality to reopen a claim or vary the
refusal envelope. The fingerprint is not an authentication credential.

T7. **First principal** denotes the normalized `userId` derived by the existing
`Devices.slug_user_id/1` behavior from the winning request's `claimedName`.
The claimed name is input to normalization; it is not an authenticated user
assertion.

T8. **First device** denotes the winning request's device row. At claim commit,
it is `allowlisted`, owns a non-null `tbt_` token, and belongs to the first
principal.

T9. **Root session** denotes the first principal's canonical personal Main. Its
key comes only from `Org.personal_session_key/1`; new cold-start code shall not
reproduce or parse the key's string layout.

T10. **Activation** denotes the first successful token-authenticated socket
handshake by the first device. Activation sets the receipt's `activatedAt`
once. It does not create the root.

T11. **Claim retry** denotes any pair request for the receipt device received
after the claim transaction commits and before activation. A claim retry never
returns or rotates a device token. Its refusal does not vary with fingerprint
equality.

T12. **Ordinary identity assertion** denotes `asUser` or an equivalent user
principal constructed after cold start. It excludes `claimedName` on a pair
request.

T13. **Database set** denotes `state.db` and any sibling `state.db-wal` and
`state.db-shm` files that exist while the gateway is stopped.

T14. **Captured v5 fixture set** denotes a complete database set produced by
the pinned v5 gateway through the real boot, pair, auth, or local-user flow
named in its manifest. It is not a hand-authored approximation of the v5
schema.

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
exists; Rust format and 248 Rust tests passed; and the product worktree
remained clean. The requested final authoritative Mix gate passed at seed
`166732`: 9 doctests and 1,684 tests, 0 failures, 11 skips, exit 0. Earlier
authoritative runs remain flake evidence: one failed the timing-sensitive
`EffortCheckinTest`, whose exact isolated rerun passed; another failed a
different assertion in `CoordinationFabricTest`. This specification preserves
those unrelated intermittent specimens instead of classifying them as a
cold-start defect.

A8. The 2026-08-25 standing Mike rule delegates technical analysis and
decision handling to this lane. It does not transition a durable operator
decision request. The five inherited rows in AR1 remain open. This file cannot
be spec-ready, handed to implementation, or treated as selecting an AR1 branch
until Mike records exact rulings on those rows.

A9. Product commit `d00e06aea578d711e608637d38a97872487df15e`
contains the exact `coordination-fabric-v1-phase1-v5` predecessor used to
capture the v5 acceptance fixtures. The fixture manifest shall bind the binary
used for capture to that source commit by SHA-256.

## Invariants

I1. Exactly one gateway-owned transaction shall change cold state to claimed
state. That transaction shall insert the first user, first device, root
session, cold-start receipt, and one accepted audit event.

I2. At the `first_device_pair` commit, the first user shall have `isAdmin = 1`
regardless of caller-supplied admin flags. Cold-start pairing shall accept no
admin flag.

I3. At the `first_device_pair` commit, the first device shall belong to the
first user, have status `allowlisted`, and have one non-null token.

I4. At the `first_device_pair` commit, the root shall be active, built in,
`kind = 'main'`, owned by the first user, and self-parented through
`operationalParent = sessionKey`. Its `spawnedBy` shall be null and its
creation origin shall be `process:tightbeam`, because no human or session
principal existed before the transaction.

I5. Every receipt shall be singleton id `1` and shall name the user, device,
root, cause, principal `process:tightbeam`, `createdAt`, and nullable
`activatedAt`. A `first_device_pair` receipt shall name a non-null request
fingerprint and accepted event id. A `v5_observed` receipt shall be activated
and shall have a null fingerprint and event id. No receipt shall store a
device token or provider credential.

I6. A successful `pair_result` shall be emitted only after I1 commits. Any
exception before commit shall leave all I1 rows absent and shall return a
named failure without a token.

I7. The cold predicate and every I1 write shall run in the same database-owner
transaction. No CLI process, second SQLite connection, check-then-dispatch
sequence, or in-memory lock shall participate in the authority decision.

I8. Before activation, every claim retry for the receipt device shall return
`bootstrap_closed` without a token, token rotation, identity mutation,
receipt insertion or replacement, or event. A denied receipt device shall
return `pair_denied`. After activation, the existing known-allowlisted-device
re-pair path shall rotate the token.

I9. A different device arriving after the winning commit shall follow the
ordinary claimed-org path. It shall receive `pair_pending`; it shall not
receive first-device authority.

I10. Any incomplete v6 state shall fail closed with
`incompatible_cold_start_v1` at boot or `bootstrap_incomplete` if detected by
a live claim transaction. AR8 shall first classify an exact v5 predecessor;
only a v5 graph without a valid legacy witness shall fail. The failure shall
name the README reset section and shall not mutate identity rows.

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

I18. The reset ceremony shall apply only to an unusable fresh installation. It
shall move the database set as one stopped-gateway unit, preserve it as a
backup, leave `auth/` and other credential files in place, restart on a new
database, and pair the first client before any `add-user` call.

I19. No accepted cold-start audit payload, doctor output, boot summary, or
error shall disclose a device token or provider credential.

I20. Boot classification shall validate the persistent relationships and
provenance in T3. It shall not reapply the commit-time admin, device-status,
token-presence, or root-state facts in I2-I4 after ordinary 0.2 lifecycle
operations change them.

## Architecture

### AR1. Open inherited decision branches

The five preserved request rows remain durably open. The table records every
available branch and the current draft candidate. A candidate is not a ruling.
All downstream requirements describe those candidates so that the contract is
reviewable. They become normative only if Mike rules the matching rows. A
different ruling requires an amendment to this file before spec readiness.
The durable rows recommend `gateway-local-bootstrap`, `zero-users`,
`durable-receipt-replay`, `actor-boundary-only`, and
`named-bootstrap-and-invalid-identity`, in row order. The draft differs on the
first two because `att_7578dbc1` and `att_91c37e8f` prove the first-device
order deadlock and partial-state residue. That evidence does not override the
open rows.

| Request | Durable options | Current draft candidate and consequence |
|---|---|---|
| `dr_38c8fdb2` | `gateway-local-bootstrap`; `keep-direct-db-writer`; `remove-cli-bootstrap` | `remove-cli-bootstrap`: delete the Rust direct writer; first-device pairing is the only cold claim surface; ordinary authenticated `add-user` remains. |
| `dr_1ac42a7a` | `zero-users`; `zero-identity-graph`; `explicit-unclaimed-marker` | `zero-identity-graph`: cold means zero users, devices, sessions, and receipts; user count alone cannot classify the proven partial state. |
| `dr_4d95f4da` | `durable-receipt-replay`; `one-shot-named-refusal`; `event-only-best-effort` | `durable-receipt-replay`: retain the singleton as durable provenance, but apply the I8 security floor; a retry returns the named `bootstrap_closed` refusal and no receipt data or credential. |
| `dr_9457c6e3` | `actor-boundary-only`; `boundary-plus-fk-migration`; `router-only-check` | `actor-boundary-only`: canonical actor construction rejects nonexistent users; a broad user foreign-key migration remains outside this scope. |
| `dr_739be284` | `named-bootstrap-and-invalid-identity`; `uniform-forbidden`; `reuse-current-errors` | `named-bootstrap-and-invalid-identity`: every pre-activation retry returns `bootstrap_closed`, and an ordinary ghost user returns `invalid_identity`. |

The non-candidate consequences also remain explicit:

- For `dr_38c8fdb2`, `gateway-local-bootstrap` retains the host-local command
  but sends a dedicated request to a locally provisioned gateway that verifies
  local origin and the organization credential. `keep-direct-db-writer`
  retains the Rust SQLite mutation authority and requires revision of I7, I11,
  AR2, and AR11.
- For `dr_1ac42a7a`, `zero-users` makes user count the claim predicate and
  requires a separate rule for device/session residue. `explicit-unclaimed-
  marker` adds a second durable source of truth and requires migration and
  reconciliation rules.
- For `dr_4d95f4da`, `one-shot-named-refusal` removes replay behavior and
  requires the provenance schema to be narrowed or justified separately.
  `event-only-best-effort` removes the singleton receipt and requires T1-T4,
  I1, I5, AR3-AR5, and migration acceptance to be rewritten.
- For `dr_9457c6e3`, `boundary-plus-fk-migration` adds a broad historical
  foreign-key migration. `router-only-check` leaves other actor constructors
  unchanged and requires I12-I13 and AC10 to be narrowed.
- For `dr_739be284`, `uniform-forbidden` returns one nondisclosing forbidden
  envelope for both cases. `reuse-current-errors` retains the current
  ownership/not-found errors and requires AR7, AR9, and AC9-AC10 to be
  rewritten.

No branch decides visitor-principal semantics. Every branch remains subject to
NG1 and to I19. The request fingerprint is not a proof of possession, so no
possible ruling may use it to disclose a bearer token.

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
The coordinator shall classify and execute cold, claim-retry, incomplete, or
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
apply these rules without treating the request fingerprint as proof:

- Any request for the receipt device returns a failed `pair_result` with
  reason `bootstrap_closed`, except for the existing denied-device case below.
  The response returns no receipt data or token and performs no write. Its
  fixed recovery text says that the organization accepted an earlier claim
  and directs an operator who lost that response to the README stopped-
  gateway reset ceremony for an unusable fresh installation. The envelope
  does not vary with the request fingerprint.
- A request for the receipt device still returns `bootstrap_closed` after an
  admitted admin operation revokes the unactivated token. It does not mint a
  replacement token.
- A request for a denied receipt device returns the existing `pair_denied`
  result without a token or write.
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
   migration back to v5, and name the README unusable-fresh-database recovery
   section.

Every v6 boot shall validate T2-T4 and all receipt referents. A receipt-less
nonempty graph and a malformed claimed graph both refuse before the gateway
serves operational requests.

An older gateway shall refuse the v6 stamp. A supported rollback shall stop
both binaries and restore a pre-v6 database set; no process shall downgrade
v6 rows in place. The user insert guard supplies defense in depth against an
older direct-writer CLI placed beside a v6 database.

The migration test corpus shall contain captured v5 fixture sets for at least
the empty and healthy-witness paths. The capture harness shall:

1. Check out the exact A9 source commit and record the resulting v5 binary
   SHA-256, build command, SQLite library version, journal mode, and schema
   stamp.
2. Produce the empty fixture through a real v5 gateway boot and clean stop.
3. Produce the healthy fixture through the real v5 first-device pair and
   authenticated handshake that creates Main, followed by a clean stop.
4. Copy every member of the stopped database set and record each file name,
   byte length, and SHA-256 in a checked-in manifest. The manifest shall also
   record the exact capture commands and a deterministic table/row census.
5. Produce user-only, admin-plus-pending-device, and allowlisted-device-
   without-Main specimens through the real v5 `add-user`, pair, and pre-auth
   stopping points where those flows can create the state.
6. Produce states that no real flow can create, including a missing or
   non-self Main parent and a corrupted v6 receipt, only through a versioned
   derivation script. Record the base fixture digest, script digest, exact
   invocation, foreign-key setting, and resulting database-set manifest.

No migration test may substitute a hand-authored ideal schema for a captured
v5 fixture. An interrupted-migration test shall start from a fresh copy of a
captured database set. After each injected failure, it shall compare the
schema stamp, schema-object inventory, canonical logical row census, and full
database-set membership with the pre-migration manifest, then prove that the
pinned v5 gateway can reopen the restored set.

### AR9. Failures and observability

The pair surface shall use these stable reasons:

| Reason | Condition | Identity mutation |
|---|---|---|
| `bootstrap_closed` | Any pre-activation request for the winning device id. | None |
| `bootstrap_incomplete` | A live transaction observes an identity graph that is neither cold nor claimed. | None |
| `bootstrap_failed` | The cold transaction raises or cannot commit. | Rolled back in full |
| `pair_pending` | A different device pairs after the winning commit. | Existing pending-device mutation only |
| `pair_denied` | A known denied device pairs, including the unactivated receipt device. | None |

Boot-time structural failure uses `incompatible_cold_start_v1`, not a pair
reason. Ordinary nonexistent user assertions use `invalid_identity`.

On `incompatible_cold_start_v1`, the database-owner startup operation shall
return the stable reason, violated invariant, and README reset-section name to
the gateway supervisor. The supervisor shall log that envelope and fail
startup. It shall not start the advertised pair/auth listener, ordinary
router, or a diagnostic-only gateway. This contract adds no second database
reader or doctor transport for a gateway that did not start.

For a running compatible gateway, the boot summary and
`tightbeam doctor --json` shall report `open` or `claimed`. `open` shall say
`pair the first client before add-user or onboarding`. `claimed` shall report
receipt cause, user id, device id, root key, and activation state. The startup
error is the only required live diagnostic for `incompatible`. None shall
report tokens.

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

Add a section named **Recover an unusable fresh database**. It shall:

1. Restrict the ceremony to an incomplete identity graph or a lost first-pair
   response before activation in a fresh installation that the operator
   intends to discard.
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
field/guard, actor-boundary check, compatible-gateway doctor state, captured-
fixture manifests, derivation harness, and tests. A coordinator is necessary
because no existing module owns user, device, session, receipt, and event
writes in one transaction. Putting session defaults into `Devices` would
couple credential storage to topology; leaving orchestration in `Wire.Socket`
would preserve a second transaction boundary.

**Delete:** delete `cli/src/users.rs`, the `create_first_if_local` dispatch
branch, local-target classification helpers used only by that branch, and the
README claim that local `add-user` is a cold-start alternative. Accepting
those pieces preserves the split SQLite authority and recreates the proven
order deadlock. Deleting the whole `add-user` command would remove a valid
post-bootstrap admin operation, so only its cold exception is deleted.

**Delete from the candidate contract:** delete unauthenticated bearer-token
replay and the unsupported diagnostic-only runtime. Retain the receipt only
for durable provenance and non-secret classification. Fail an incompatible
boot before the gateway opens a listener. Also delete any statement that the
five inherited decisions are resolved until their durable rows are ruled.

**Refactor and accept:** retain the pair/auth frames, `tbt_` token class,
ordinary pending/approval behavior, canonical personal-Main representation,
and DB-owner transaction mechanism. Extract their in-transaction helpers so
the new coordinator composes existing rules instead of duplicating them.

### AR12. Traceability

| Contract | Acceptance proof |
|---|---|
| G1-G4, I1-I11, I14, AR2-AR6 | AC1-AC8 |
| G5, I12-I13, AR7 | AC9-AC10 |
| G6, I10, I15-I19, AR8-AR10 | AC11-AC15 and AC19 |
| G7, I8-I9, I20, AR5 | AC3-AC5 and AC16 |
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

AC4. **Concurrent identical claim.** Given cold state and two identical claim
requests for the same device, when both complete before activation, then
exactly one response succeeds with the committed token and tuple. The other
returns `bootstrap_closed` without a token. The database contains one device,
receipt, root, user, and event. No token rotation occurs.

AC5. **Lost response and activation boundary.** Given a committed claim whose
successful response is lost, when the exact request repeats before auth, then
it returns `bootstrap_closed` without a token, write, or event and names the
README fresh-reset recovery. Moving the complete database set aside while the
gateway is stopped and restarting returns the organization to cold state.
Given a separate committed claim whose response token was received, when that
token authenticates, then the receipt gains `activatedAt` once. When the
device pairs again after activation, it receives a new token and the old token
fails authentication. Given separate unactivated fixtures whose claim token
is revoked or whose receipt device is denied, an exact request returns
`bootstrap_closed` or `pair_denied`, respectively, without a token or
mutation.

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
devices, and sessions from the captured empty fixture set, when v6 boots, then
migration stamps v6, adds the guarded schema, leaves the receipt table empty,
and doctor reports `open`. A first pair then satisfies AC1.

AC12. **Healthy v5 migration.** Given the captured healthy v5 fixture set with
a usable admin device and its active self-parented personal Main plus later
identity rows, when v6 boots, then it selects the deterministic witness, marks
all prior users `legacy`, writes one activated `v5_observed` receipt,
synthesizes no event, and preserves every prior row and token. Known-device
and later-device behavior then satisfy AC16.

AC13. **Incomplete refusal and reset recovery.** For each exact v5
fixture—user only, admin user plus pending device, allowlisted device without
Main, and Main with a missing or non-self parent—given no valid legacy
witness, when v6 boots, then the migration rolls back and gateway startup
fails with `incompatible_cold_start_v1`, the violated invariant, and the
README reset-section name. The gateway opens no listener. The v5 stamp,
schema-object inventory, canonical row census, and complete database-set
membership still match the fixture manifest, and the pinned v5 gateway can
reopen the set. Given a stamped-v6 fixture whose receipt has a deliberately
corrupted referent, v6 startup fails with the same named refusal, opens no
listener, and leaves the preexisting `integrity_check` and
`foreign_key_check` outcomes unchanged. When the stopped-gateway database set
is moved aside, the gateway restarts, doctor reports `open`, provider
credentials remain available, and pair-first produces the AC1 tuple.

AC14. **Interrupted migration and rollback fence.** Given a healthy v5
database, when migration is interrupted after each rebuild/create/copy/stamp
step, then the whole operation rolls back; the schema stamp, schema-object
inventory, canonical row census, and database-set membership match the
pre-migration manifest; the pinned v5 gateway reopens the set; and a v6 retry
converges on AC12. Given the resulting v6 database, when a v5 gateway opens
it, then it refuses the v6 shape; when an older direct-writer CLI attempts its
old INSERT, then it receives `bootstrap_owned_by_gateway` and adds no row.
Restoring the stopped pre-v6 database set permits the v5 gateway to boot.

AC15. **Observable and secret-free.** Given open and claimed fixtures, when
boot summary and `doctor --json` inspect each running gateway, then they report
the exact AR9 state and action. Given an incomplete fixture, gateway startup
fails with the exact AR9 envelope and no doctor endpoint is available. Given
accepted, claim-retry, incomplete, and failed claim attempts, when logs,
events, responses, startup errors, and available doctor output are searched,
then user/device/root provenance and rollback status appear where AR3 and AR9
require them; no `tbt_` token, org token, CLI token, authorization header,
claimed name, or provider credential appears.

AC16. **Warm compatibility matrix.** Given a claimed and activated org, when
an allowlisted device re-pairs, a new device pairs, a pending device re-pairs,
a denied device re-pairs, a token is revoked, and an admin approves a pending
device, then each frame, reason, token-rotation result, and derived admin value
matches the pre-change 0.2 behavior. Existing client J0 still receives
successful first pair, auth success, Main in `stream_snapshot`, and
`sync_complete` without a new required client field. Given separate fixtures
where an existing 0.2 operation changes the receipt user's admin bit, the
receipt device's status or token, or the root's active state, when each fixture
reboots, then doctor still reports `claimed` if the persistent T3
relationships remain valid.

AC17. **Decision and scope audit.** Given the five inherited decision-request
records, when an independent reviewer checks this file before Mike rules them,
then every row is still marked open, AR1 contains every durable option, no
candidate is called a ruling, and the status blocks implementation. After Mike
rules them, this file shall be amended to cite each durable ruling and to
remove every losing branch before it can become spec-ready. In both states,
visitor semantics remain in NG1 and `wi_20df0b1f` remains untargeted with no
second spec.

AC18. **Deletion boundary.** Given the implementation diff, when a reviewer
searches it, then the Rust direct user writer and its special dispatch helpers
are absent; one ordinary `add-user` gateway path remains; `ColdStart` owns one
transaction; Devices and Org expose shared in-transaction helpers; and no
second SQLite mutation authority, placeholder root, nullable operational
parent, or duplicate personal-Main constructor was added.

AC19. **Captured fixture provenance.** Given a clean checkout of the A9 commit
and the checked-in capture harness, when the fixture maintainer follows the
manifest commands, then the empty and healthy fixtures come from the named v5
gateway flows and every stopped database-set member has a recorded byte length
and SHA-256. Each partial or corrupt fixture names its captured base and either
the real v5 stopping point or the exact versioned derivation script. An
independent verifier can check every manifest hash, reproduce each derivation,
match its canonical table/row census, and open each intended v5 fixture with
the pinned v5 gateway. A test that creates an idealized v5 schema directly
fails this acceptance criterion.

## Open Questions

The following existing decision requests are **BLOCKING**. This specification
does not duplicate, supersede, withdraw, or answer them:

- `dr_38c8fdb2`: Which authority seam should implement the documented
  host-local first-user command?
- `dr_1ac42a7a`: What exact state keeps the first-user bootstrap seam open?
- `dr_4d95f4da`: What durable retry and provenance contract should first-user
  bootstrap use?
- `dr_9457c6e3`: Where should ordinary nonexistent-user assertions be
  rejected?
- `dr_739be284`: Which observable refusals should distinguish a closed
  bootstrap seam from a nonexistent asserted user?

AR1 preserves every durable option and the reviewable draft consequence. Mike
must record exact rulings on the five existing rows. The writer shall amend
this file first and remove every losing branch before requesting another
spec-ready review. Money, materially new scope, visitor-principal policy, and
a separate invitation ceremony remain outside this specification.
