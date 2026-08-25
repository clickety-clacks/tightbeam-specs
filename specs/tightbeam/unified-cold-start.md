# Unified first-user, first-device, and first-root cold start

Status: SPEC-READY for independent exact-revision review. Target: Tightbeam
0.2.0.

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
- Reviewed predecessor: `art_2c3dbc77`, commit
  `13c5fb6ca2f2517cc76b46dabd3ca75d41e58f4e`, content SHA-256
  `fd10557526e4c456aeaf4f6e15197f69a9c40d30972d6e6b42b776b3b86b21e7`.
- Changes-requested review: `att_ec8118f8` and results `art_40f6fa93`.
- Controlling product disposition: `att_732021c2`.
- F1-F4 successor reviewed: `art_8f10f6d7`, commit
  `420208afed3491701730490bb7dd90a77af53ad8`, content SHA-256
  `5068013e58a70fcf06c7479f8b3082437d3cbbb41002258674d86c7d899a5f74`.
- Latest changes-requested review: `att_ab835da2` and report
  `art_7264611d`, report SHA-256
  `3182b592fd8445296222978be604c34de0dfefdfdba7a01dd368bf5da8e5fc6f`.

This file is the only normative cold-start artifact for work item
`wi_8edbc2c4`. Companion work item `wi_20df0b1f` remains untargeted and points
to this file; it does not own a second specification.

## Goal

G1. A fresh Tightbeam 0.2.0 organization shall acquire its first human
principal, first usable device credential, and first operational root session
through gateway-owned database transactions.

G2. The pair-first entry shall create the first principal, first device, first
root, receipt, and accepted event in one database transaction.

G3. The host-local entry shall create the first principal, first root, reserved
receipt, and accepted event in one database transaction. The first matching
pair shall attach the first device and complete that receipt in a second
database transaction.

G4. The root created by either entry shall make user-attributed CLI operations
and the first spawn legal before a client performs the authenticated chat
handshake.

G5. Tightbeam shall prevent the proven `add-user`-then-pair deadlock. The
README shall distinguish the pair-first entry from the host-local entry and
shall give a complete order for each.

G6. Tightbeam shall reject ordinary assertions of nonexistent users before
typed-target lookup, rails, audit events, or domain writes.

G7. Tightbeam shall provide a named, recoverable response for an incomplete
fresh database or a lost first-pair response before activation. It shall
document the proven database-reset ceremony without deleting provider
credentials.

G8. Existing claimed organizations and later-device pairing shall retain their
0.2 wire behavior except where this specification names a change.

The operating pattern taught by this specification is: **choose one entry:
pair the first client, or run the host-local bootstrap and then pair that
user's first client; use the stopped-gateway reset only for an unusable fresh
database.**

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

T2. **Bootstrap-open state** denotes one database-owner transaction snapshot
in which the canonical `users` table contains zero rows. No device, session,
or receipt count participates in this predicate. AR8 separately rejects a
structurally invalid database before it reaches a claim transaction.

T3. **Reserved state** denotes a v6 database with exactly one structurally
valid `reserved` cold-start receipt. The receipt has a user and root but no
device. **Claimed state** denotes a v6 database with exactly one structurally
valid `complete` cold-start receipt. The receipt has a user, device, and root.
In both states, each present foreign key resolves. The root belongs to the
receipt user, is built in, has kind `main`, and is self-parented. A present
device belongs to the receipt user. The receipt fields satisfy AR4 for their
cause and phase. A reserved or claimed organization can contain additional
identity rows. Ordinary post-completion changes to the receipt user's admin
bit, the receipt device's status or token, or the root's active state do not
erase the historical claimed classification.

T4. **Incomplete state** denotes a v6 identity graph that is neither
bootstrap-open, reserved, nor claimed, or an exact v5 graph for which AR8
finds no valid legacy witness. Examples include a user without a receipt and
root, a pending-only first device, a receipt with a missing referent, and a
Main whose operational parent is not itself.

T5. **Claim request** denotes a valid protocol-version-1 WebSocket
`pair_request` received while the database owner observes bootstrap-open or
reserved state. Its fields are `deviceId`, `claimedName`, nullable
`deviceInfo.platform`, nullable `deviceInfo.model`, and optional
`claimReplaySecret`.

T6. **Request fingerprint** denotes SHA-256 over UTF-8 canonical JSON with
exactly these ordered keys: `deviceId` and normalized `userId`. It identifies
the committed logical device-to-principal claim in durable provenance. It is
not an authentication credential.

T7. **First principal** denotes the normalized `userId` derived by the existing
`Devices.slug_user_id/1` behavior from the winning request's `claimedName`.
The claimed name is input to normalization; it is not an authenticated user
assertion.

T8. **First device** denotes the winning request's device row. At pair-first or
reserved-completion commit, it is `allowlisted`, owns a non-null `tbt_` token,
and belongs to the first principal.

T9. **Root session** denotes the first principal's canonical personal Main. Its
key comes only from `Org.personal_session_key/1`; new cold-start code shall not
reproduce or parse the key's string layout.

T10. **Activation** denotes the first successful token-authenticated socket
handshake by the first device. Activation sets the receipt's `activatedAt`
once. It does not create the root.

T11. **Claim replay secret** denotes exactly 32 random bytes that a replay-
capable client generates before its first claim request and encodes as 43
unpadded base64url characters in `claimReplaySecret`. The client retains the
secret until activation. The gateway stores only the AR4 digest. The secret is
a credential; the request fingerprint is not.

T11a. **Exact claim replay** denotes a pre-activation request whose device id,
request fingerprint, and claim replay secret match the completed receipt. It
returns the committed device token without rotating it or writing a second
receipt or event. A claim without the secret can still win the initial claim,
but it cannot replay a lost response.

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
narrows each mutation to a gateway transaction. The optional replay secret
adds proof for credential replay; it does not add a wider endpoint.

A5. The deployment operator controls network exposure until a receipt reaches
`complete` and the first device receives its credential. An organization that
requires a separate invitation ceremony must specify it in later work.

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

A8. Five product-owner attempts to run `operator-rule` on the inherited rows
failed with `not_owner`. Those decision rows remain mechanically open.
Product disposition `att_732021c2` is the controlling durable product ruling
under the 2026-08-25 Mike lane authority. AR1 records its five exact choices
without claiming that the decision-request rows changed state.

A9. Tightbeam release `0.2.0` at product commit
`d00e06aea578d711e608637d38a97872487df15e` contains the exact
`coordination-fabric-v1-phase1-v5` predecessor used to capture the v5
acceptance fixtures. The fixture manifest shall bind the generating binary to
that release and source commit by SHA-256.

## Invariants

I1. A pair-first claim shall change bootstrap-open state to claimed state in
one gateway-owned transaction. A host-local claim shall change bootstrap-open
state to reserved state in one gateway-owned transaction. A later first-device
completion shall change that reserved state to claimed state in one gateway-
owned transaction.

I2. At the `first_device_pair` commit, the first user shall have `isAdmin = 1`
regardless of caller-supplied admin flags. Cold-start pairing shall accept no
admin flag. At the `gateway_local_bootstrap` commit, the requested first user
shall have `isAdmin = 1` regardless of the CLI `--admin` flag.

I3. At a pair-first or reserved-completion commit, the first device shall
belong to the first user, have status `allowlisted`, and have one non-null
token.

I4. At either first-user commit, the root shall be active, built in,
`kind = 'main'`, owned by the first user, and self-parented through
`operationalParent = sessionKey`. Its `spawnedBy` shall be null and its
creation origin shall be `process:tightbeam`, because no human or session
principal existed before the transaction.

I5. Every receipt shall be singleton id `1` and shall name the user, root,
cause, phase, principal `process:tightbeam`, `createdAt`, and nullable
`activatedAt`. A complete receipt shall name a device. A reserved receipt
shall not name a device. Each new claim shall name its accepted claim event. A
completed host-local claim shall also name its accepted device-completion
event. A `v5_observed` receipt shall be complete and activated and shall name
no event. A receipt shall store a replay-secret digest, not the replay secret
or device token. A complete new receipt shall store a digest of the original
claim token so replay can refuse a replaced token.

I6. A successful `pair_result` shall be emitted only after its pair-first,
reserved-completion, or exact-replay transaction commits. An exception before
a transaction commits shall roll back that transaction and shall return a
named failure without a token.

I7. The zero-users predicate and each I1 phase transition shall run in its
own database-owner transaction. The CLI shall send the dedicated host-local
request to the gateway. No CLI process, second SQLite connection, check-then-
dispatch sequence, or in-memory lock shall participate in the authority
decision.

I8. Before activation, an exact claim replay with a valid claim replay secret
shall return the committed device token without token rotation, identity
mutation, receipt replacement, or event. A request that omits the secret or
supplies a well-formed nonmatching secret shall return the same
`bootstrap_closed` envelope without a token. AR4 shall reject malformed
encoding or decoded length before a claim transaction. A denied receipt device
shall return `pair_denied`. After activation, the existing known-allowlisted-
device re-pair path shall rotate the token.

I9. A different device arriving after a complete claim shall follow the
ordinary claimed-org path. It shall receive `pair_pending`; it shall not
receive first-device authority. While a host-local receipt is reserved, only
a pair request whose normalized user id equals the reserved user may complete
the first device. Another request shall return `bootstrap_closed` without a
write.

I10. Any incomplete v6 state shall fail closed with
`incompatible_cold_start_v1` at boot or `bootstrap_incomplete` if detected by
a live claim transaction. AR8 shall first classify an exact v5 predecessor;
only a v5 graph without a valid legacy witness shall fail. The failure shall
name the README reset section and shall not mutate identity rows.

I11. `tightbeam add-user` shall have one database mutation authority: the
gateway. A no-identity invocation against a locally discovered loopback
gateway shall call the dedicated host-local bootstrap verb. An identified
invocation shall call the ordinary gateway-admin verb. The Rust direct SQLite
writer shall not exist.

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

I17. The README shall teach two explicit first-order sequences. It shall name
the pair-first entry as the client path. It shall name gateway-local
`add-user` followed by same-user first pairing as the headless host path. It
shall not mix steps from those sequences.

I18. The reset ceremony shall apply only to an unusable fresh installation. It
shall move the database set as one stopped-gateway unit, preserve it as a
backup, leave `auth/` and other credential files in place, and restart on a
new database. The operator shall then choose one complete AR10 entry sequence.

I19. No accepted cold-start audit payload, doctor output, boot summary, error,
or log shall disclose a device token, claim replay secret, replay-secret
digest, claim-token digest, or provider credential.

I20. Boot classification shall validate the persistent relationships and
provenance in T3. It shall not reapply the commit-time admin, device-status,
token-presence, or root-state facts in I2-I4 after ordinary 0.2 lifecycle
operations change them.

## Architecture

### AR1. Controlling product disposition

The five inherited decision-request rows remain mechanically `open`. The
product owner attempted each `operator-rule`, and Tightbeam returned
`not_owner`. Product disposition `att_732021c2` records the controlling choices
under Mike's 2026-08-25 lane authority:

| Request | Controlling product choice | Contract consequence |
|---|---|---|
| `dr_38c8fdb2-f08c-4555-9132-e51ed5ea488b` | `gateway-local-bootstrap` | The bare host-local command sends a dedicated authenticated request to the local gateway. The CLI never writes SQLite. |
| `dr_1ac42a7a-e81f-4ff7-b4e6-0ffb06892f16` | `zero-users` | The user-bootstrap seam is open exactly when the transaction observes zero canonical users. Boot validation handles structural residue separately. |
| `dr_4d95f4da-3b4f-4906-a05c-24a9efabd33a` | `durable-receipt-replay` | The receipt preserves provenance and supports pre-activation replay only when the caller proves possession of the claim replay secret. |
| `dr_9457c6e3-756d-4148-be41-39720813e254` | `actor-boundary-only` | Canonical actor construction rejects nonexistent users. A broad user foreign-key migration remains outside this scope. |
| `dr_739be284-ccd6-4b7e-a01a-a0e70a077c7e` | `named-bootstrap-and-invalid-identity` | A closed bootstrap returns `bootstrap_closed`; an ordinary ghost user returns `invalid_identity`. |

This table does not claim that the decision-request rows are ruled, withdrawn,
consumed, or superseded. The controlling disposition resolves the product
choices for this revision. It does not decide visitor-principal semantics.

### AR2. Ownership and module boundary

Add one gateway module, `Tightbeam.ColdStart`, as the owner of identity-graph
classification and claim orchestration. It receives parsed pair requests from
`Wire.Socket` and dedicated host-local bootstrap requests from `Wire.Router`.
Each operation opens one `Tightbeam.DB.transaction/2` and uses only
`*_in_txn` helpers.

Refactor `Devices` to expose in-transaction pair and user insertion helpers.
Refactor the existing socket Main-seeding body into one shared
`Org.ensure_personal_main_in_txn/2` helper. `ColdStart` uses that helper inside
the claim transaction. Auth for later users shall call the same helper; the
helper shall remain convergent when Main already exists.

`Wire.Socket` shall call the cold-start coordinator for each pair request. The
coordinator shall classify and execute bootstrap-open, reserved, exact-replay,
incomplete, or ordinary behavior without an earlier database read.

For a running gateway, `Wire.Router` shall expose one read-only
`cold-start-state` verb after `cliToken` authentication and before actor
construction. The verb shall ask the existing database owner to classify the
graph. `tightbeam doctor` shall call this verb through the existing
`/agent/dispatch` transport. No process shall open `state.db` for doctor.

For bare `tightbeam add-user <userId>`, the CLI shall require an endpoint that
it discovered from the local base directory and shall connect through a
loopback address. It shall send a dedicated `bootstrap-user` request with the
existing `cliToken`. `Wire.Router` shall admit that request only after the
ordinary `cliToken` check and only when `conn.remote_ip` is IPv4 or IPv6
loopback. It shall not trust forwarding headers for this check. An explicit
remote endpoint shall fail in the CLI before dispatch with `bootstrap requires
a locally discovered loopback gateway`. A non-loopback request shall return
HTTP 403 `forbidden` with message `local bootstrap required` before a database
transaction.

### AR3. Cold-start transactions

For a pair-first request, `ColdStart` shall perform this ordered transaction:

1. Read `SELECT COUNT(*) FROM users` and assert zero.
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
8. Insert complete receipt id `1` with cause `first_device_pair`, the event id,
   request fingerprint, nullable replay-secret digest, and claim-token digest.
9. Re-read the three referents and assert I2-I5 before returning from the
   transaction callback.

For a host-local bootstrap request, `ColdStart` shall perform this ordered
transaction:

1. Read `SELECT COUNT(*) FROM users` and assert zero.
2. Validate and normalize the requested `userId` with the ordinary add-user
   rules.
3. Resolve the same root defaults as the pair-first path.
4. Insert the admin user with creation kind `gateway_local_bootstrap`.
5. Create the canonical personal Main through the shared helper.
6. Append one accepted `cold-start` event with cause
   `gateway_local_bootstrap`.
7. Insert reserved receipt id `1` with that event id and no device, request
   fingerprint, replay-secret digest, activation time, or device-completion
   event id.
8. Re-read the user and root and assert I2, I4, and I5 before returning.

If a repeated authenticated loopback bootstrap request names the reserved
receipt user, the coordinator shall return the committed non-secret user,
root, phase, and receipt id without a write or second event. If it names
another user or the receipt is complete, it shall return `bootstrap_closed`.

For the first pair against a reserved receipt, `ColdStart` shall perform this
ordered transaction:

1. Re-read the reserved receipt and assert that its user and root are valid.
2. Normalize `claimedName` and compare it with the reserved user id.
3. Return `bootstrap_closed` without a write if the user ids differ.
4. Insert the first device as allowlisted and mint its token.
5. Append one accepted `cold-start-device` event.
6. Update the receipt to phase `complete` with the device id, request
   fingerprint, nullable replay-secret digest, claim-token digest, and device-
   completion event id.
7. Re-read the three referents and assert I2-I5 before returning.

The accepted event payload shall contain exactly `receiptId`, `cause`,
`phase`, `userId`, nullable `deviceId`, `rootSessionKey`, `isAdmin`, nullable
`deviceStatus`, `rootKind`, and `operationalParent`. It shall not contain the
claimed name, device-info fields, token, claim replay secret, replay-secret
digest, claim-token digest, org token, CLI token, or provider credential data.

`Wire.Socket` shall encode the existing successful `pair_result` from the
committed result. No new success frame or required client field is introduced.

### AR4. Receipt and user-origin schema

The current schema shape shall advance from
`coordination-fabric-v1-phase1-v5` to
`coordination-fabric-v1-phase1-v6`.

The `cold_start_receipts` columns shall be `id`, `userId`, `deviceId`,
`rootSessionKey`, `cause`, `phase`, `principal`, `requestFingerprint`,
`replaySecretHash`, `claimTokenHash`, `claimEventId`, `deviceEventId`,
`createdAt`, and `activatedAt`. The table shall enforce:

- `id INTEGER PRIMARY KEY CHECK (id = 1)`;
- non-null foreign keys to `users(userId)` and `sessions(sessionKey)`;
- a nullable foreign key to `devices(deviceId)`;
- `cause IN ('first_device_pair', 'gateway_local_bootstrap', 'v5_observed')`;
- `phase IN ('reserved', 'complete')`;
- `principal = 'process:tightbeam'`;
- a non-null claim event id for each new v6 claim;
- a non-null device, request fingerprint, and device-completion event id for a
  completed `gateway_local_bootstrap` receipt;
- a null device, request fingerprint, replay-secret digest, claim-token
  digest, device-completion event id, and activation time for a reserved
  receipt;
- a non-null device and request fingerprint for `first_device_pair`;
- phase `complete`, a null device-completion event id, and a non-null claim
  event id for `first_device_pair`;
- cause `gateway_local_bootstrap` for each reserved receipt;
- a nullable 32-byte replay-secret digest for each new complete receipt;
- a non-null 32-byte claim-token digest for each new complete receipt;
- phase `complete`, a non-null device and activation time, and null event ids,
  request fingerprint, replay-secret digest, and claim-token digest for
  `v5_observed`;
- nonnegative `createdAt`; and
- nullable nonnegative `activatedAt`.

The replay-secret digest shall be
`SHA-256(UTF-8("tightbeam-cold-start-replay-v1") || 0x00 || secretBytes)`.
The gateway shall decode exactly 32 bytes from the unpadded base64url field.
It shall reject another length or alphabet with `invalid_message` before a
claim transaction. It shall compare two digests with a constant-time byte
comparison.

The claim-token digest shall be
`SHA-256(UTF-8("tightbeam-cold-start-token-v1") || 0x00 || UTF-8(token))`.
Replay shall compare the current token digest with this stored digest in
constant time before returning the token.

The `users` table shall gain required `creationKind` with the closed values
`cold_start`, `gateway_local_bootstrap`, `device_pair`, `admin_add`, and
`legacy`. New gateway writes shall always name the value. Ordinary pairing
uses `device_pair`; authenticated `add-user` uses `admin_add`; the v5 migration
marks existing rows `legacy`.

A schema-owned insert guard shall reject a user insert that omits
`creationKind` with `bootstrap_owned_by_gateway`. This guard is the old-local-
CLI fence required by I15; a shape stamp alone cannot stop that CLI because
the deleted Rust path opens SQLite without asking the gateway.

### AR5. Pairing, retry, and activation

When a complete receipt exists and `activatedAt` is null, the coordinator
shall apply these rules:

- A request with the receipt device id and request fingerprint shall return
  the committed token and user tuple only when the receipt has a non-null
  replay-secret digest, the request supplies a well-formed secret, the digest
  matches in constant time, the receipt device remains allowlisted with a
  non-null token, and that token matches the stored claim-token digest in
  constant time.
- A replay success shall not rotate the token or write a receipt or event.
- A request with a missing or wrong secret, a different fingerprint, or a
  revoked or replaced token shall return the same failed `pair_result` with
  reason `bootstrap_closed`. It shall return no token or receipt data.
- A request for a denied receipt device shall return `pair_denied` without a
  token or write.
- A different device shall proceed through ordinary pairing and shall receive
  `pair_pending` when newly inserted.

A replay-capable client shall generate its claim replay secret before the
first request. It shall retain the secret in device-private storage until the
first authenticated handshake succeeds. It shall delete the secret after
activation. A legacy client can omit the optional field and can complete an
initial claim. If that response is lost, its retry receives
`bootstrap_closed`; the fixed response names the README stopped-gateway reset
section for an unusable fresh installation.

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
3. If the predecessor passes its structural checks and users is empty, leave
   the receipt table empty and stamp v6. Device and session counts do not
   participate in the bootstrap-open predicate.
4. Otherwise, find a deterministic legacy witness ordered by
   `(devices.createdAt, devices.deviceId)`: an allowlisted device with a
   non-null token, an admin owner, and that owner's active built-in personal
   Main whose `kind` is `main` and whose operational parent is itself.
5. If a witness exists, insert one complete, activated `v5_observed` receipt
   for that tuple. Set both receipt times to migration time. Do not synthesize
   a historical event, request fingerprint, or replay-secret digest.
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
4. Copy the stopped database set. Record `state.db`, `state.db-wal`, and
   `state.db-shm` as present or absent. For each present file, record its byte
   length and SHA-256 in a checked-in manifest. The manifest shall also record
   the exact capture commands and a deterministic table/row census.
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
| `bootstrap_closed` | The user-bootstrap seam has closed; a reserved claim names another user; or a replay proof fails. | None |
| `bootstrap_incomplete` | A live transaction observes an identity graph that is neither bootstrap-open, reserved, nor claimed. | None |
| `bootstrap_failed` | A cold-start phase raises or cannot commit. | Current phase rolled back in full |
| `pair_pending` | A different device pairs after a complete claim. | Existing pending-device mutation only |
| `pair_denied` | A known denied device pairs, including the unactivated receipt device. | None |

The WebSocket `bootstrap_closed` envelope shall contain exactly the keys
`type`, `success`, `reason`, and `recovery`. Their values shall be
`pair_result`, `false`, `bootstrap_closed`, and
`Recover an unusable fresh database`. The host-local bootstrap verb shall
return HTTP 409 with error code `bootstrap_closed` and message
`bootstrap is already claimed`. Neither envelope shall identify the winning
user, device, fingerprint, or proof state.

Boot-time structural failure uses `incompatible_cold_start_v1`, not a pair
reason. Ordinary nonexistent user assertions use `invalid_identity`.

On `incompatible_cold_start_v1`, `Schema.ensure_all/1` shall raise
`Tightbeam.Schema.ShapeError` with this exact message shape:
`incompatible_cold_start_v1: <invariant>; recovery: Recover an unusable fresh
database`. `<invariant>` shall be one closed identifier from the boot
validator. `Tightbeam.Boot` shall log one structured error with fields
`code`, `invariant`, and `recoverySection`, then let its supervised start fail.
The application start result shall contain
`{:failed_to_start_child, Tightbeam.Boot, %Tightbeam.Schema.ShapeError{}}`.
The release shall print the ShapeError message to stderr and exit nonzero. It
shall not start the advertised pair/auth listener, ordinary router, or another
gateway. This contract adds no second database reader or transport.

The boot validator shall report the first failure in this order:
`orphan_identity_row`, `receiptless_nonempty_users`, `receipt_cause_invalid`,
`receipt_phase_invalid`, `receipt_missing_user`, `receipt_missing_root`,
`receipt_missing_device`, `receipt_owner_mismatch`,
`root_not_personal_main`, `receipt_event_shape_invalid`, and
`receipt_replay_shape_invalid`. A v5 migration without a witness shall use
`legacy_witness_missing`.

For a running compatible gateway, the boot summary and the authenticated
`cold-start-state` result shall report `open`, `reserved`, or `claimed`.
`open` shall return exactly `state` and `action`, with action
`choose pair-first or host-local bootstrap`. `reserved` shall return exactly
`state`, `cause`, `userId`, `rootSessionKey`, and `action`, with action
`pair the first client with the reserved user`. `claimed` shall return exactly
`state`, `cause`, `userId`, `deviceId`, `rootSessionKey`, and `activated`.

`tightbeam doctor --json` shall place that result at top-level key
`cold_start`. Human doctor output shall print one `cold start:` line with the
state and action. After an incompatible boot, doctor shall retain its current
installation and process checks, set `cold_start` to null, and include the
existing note `gateway is not running; local registered harness checks still
ran`. Doctor shall not read or classify `state.db`. The startup stderr and
structured Boot log are the only cold-start diagnostics for that state. These
surfaces shall report no token or replay-secret material.

The gateway shall emit one structured error log for each
`bootstrap_incomplete` or `bootstrap_failed` response with the request device
id, identity-graph counts, reason, and rollback outcome. It shall not log
claimed name, tokens, claim replay secrets, replay-secret digests,
claim-token digests, authorization headers, or provider credentials.

### AR10. README order and database-reset recovery

Replace the current ambiguous cold-start text with two complete entry
sequences.

The **Pair first** sequence shall be:

1. Start the gateway.
2. Point the first client at `TIGHTBEAM_ADVERTISED_URL` and pair it with the
   intended name.
3. Verify that pairing succeeded and the catalog contains Main.
4. Onboard each provider credential as the new admin.
5. Learn the selected identity bundle.
6. Run a real turn in Main.
7. Use authenticated `tightbeam add-user ... --as-user <adminUserId>` only
   for later users.

The **Bootstrap on the host** sequence shall be:

1. Start the gateway and run bare `tightbeam add-user <userId>` on that host.
2. Verify that the command reports the forced-admin user and Main and that
   doctor reports `reserved`.
3. Perform any otherwise-authorized headless onboarding or first spawn as that
   canonical user.
4. Pair the first client with a claimed name that normalizes to the reserved
   user id.
5. Verify that pairing succeeds and doctor reports `claimed`.
6. Continue with provider onboarding, identity learning, and a real Main turn.
7. Use authenticated `tightbeam add-user ... --as-user <adminUserId>` only for
   later users.

The README shall state that bare host-local `add-user` sends a dedicated
request to the running loopback gateway. It shall state that the CLI does not
open or write `state.db`. An explicit remote target shall use the ordinary
identified admin path and cannot invoke bootstrap.

The README shall state that a replay-capable client retains its claim replay
secret until authentication. If the first response is lost, the client shall
repeat the exact pair request with that secret. A legacy client or a client
that lost the secret receives `bootstrap_closed` and must use the fresh-reset
ceremony if the installation is safe to discard.

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
7. Choose and complete one of the two entry sequences above.
8. Verify exactly one admin user, one allowlisted device, one complete receipt,
   and one active self-parented Main before continuing.

### AR11. Deletion assessment

**Add:** add the narrow `ColdStart` coordinator, dedicated loopback bootstrap
verb, singleton phased receipt, user-origin field/guard, replay-secret digest,
actor-boundary check, compatible-gateway doctor state, captured-fixture
manifests, derivation harness, and tests. A coordinator is necessary because
no existing module owns the cross-table phase transitions. Putting session
defaults into `Devices` would couple credential storage to topology; leaving
orchestration in `Wire.Socket` would preserve split transaction ownership.

**Delete:** delete `cli/src/users.rs` and the `create_first_if_local` direct-
writer branch. Retain and narrow local-target classification so it dispatches
the dedicated loopback request. Keeping the writer preserves split SQLite
authority and recreates the proven order deadlock. Deleting the whole
`add-user` command would remove the ruled bootstrap entry and a valid later-
user operation.

**Delete from the predecessor contract:** delete bearer-token replay based
only on public request fingerprint and delete the unsupported diagnostic-only
runtime. Retain replay only behind the claim replay secret. Fail an
incompatible boot before the gateway opens a listener. Delete each statement
that claims the five decision-request rows changed from mechanically open.

**Refactor and accept:** retain the pair/auth frames, `tbt_` token class,
ordinary pending/approval behavior, canonical personal-Main representation,
and DB-owner transaction mechanism. Extract their in-transaction helpers so
the new coordinator composes existing rules instead of duplicating them.

### AR12. Traceability

| Contract | Acceptance proof |
|---|---|
| G1-G5, I1-I11, I14, AR2-AR6 | AC1-AC8 and AC20-AC21 |
| G6, I12-I13, AR7 | AC9-AC10 |
| G7, I10, I15-I19, AR8-AR10 | AC11-AC15 and AC19 |
| G8, I8-I9, I20, AR5 | AC3-AC5, AC16, and AC21 |
| AR1 and preserved decision provenance | AC17 |
| AR11 deletion boundary | AC18 |

## Acceptance

AC1. **Atomic pair-first claim.** Given a v6 database in bootstrap-open state
and valid gateway defaults, when device `d1` sends a valid pair request claiming
`Alice`, then the response succeeds only after one transaction commits one
admin user, one allowlisted device with a token, one active built-in Main, one
complete receipt, and one accepted event. The user, device, root, receipt, and
event fields satisfy I2-I5. No credential appears in the event.

AC2. **Statement-by-statement rollback.** Given the AC1 fixture and a fault
injected after each ordered write in AR3, when the claim runs once per fault,
then every run returns `bootstrap_failed`; users, devices, sessions, receipts,
and accepted cold-start events each remain at zero. A subsequent fault-free
claim succeeds.

AC3. **Concurrent different devices.** Given bootstrap-open state and two barriers that
enter pair concurrently with different device ids, when the DB owner releases
both calls, then one call returns successful first pairing and the other
returns `pair_pending`. Exactly one admin, root, receipt, and cold-start event
exist. The pending device has no token and cannot authenticate.

AC4. **Concurrent identical replay-safe claim.** Given bootstrap-open state
and two otherwise-identical requests that contain the same valid claim replay
secret, when both complete before activation, then both responses contain the
same committed token and tuple. One response comes from the winning claim and
one comes from exact replay. The database contains one device, receipt, root,
user, and event. No token rotation occurs.

AC5. **Lost response and activation boundary.** Given a committed claim whose
successful response is lost, when the exact request repeats with the retained
claim replay secret before auth, then it returns the same token and tuple
without a write, event, or rotation. When the request omits the secret or
changes one secret bit, it returns the identical `bootstrap_closed` envelope
without a token. When the committed token authenticates, the receipt gains
`activatedAt` once and the client deletes its replay secret. When the device
pairs again after activation, it receives a new token and the old token fails
authentication. Given separate unactivated fixtures whose claim token is
revoked or whose receipt device is denied, an otherwise exact request returns
`bootstrap_closed` or `pair_denied`, respectively, without a token or
mutation.

AC6. **Gateway-local bootstrap authority.** Given bootstrap-open state and a
CLI endpoint discovered from the local base directory, when a local shell runs
bare `tightbeam add-user alice`, then the CLI connects over loopback with the
`cliToken` and the gateway commits one forced-admin Alice, one active
self-parented Main, one reserved receipt, and one accepted event. No device
exists. A same-user retry returns the same non-secret receipt result without a
write or event. A different-user retry returns `bootstrap_closed`. Given an
explicit remote endpoint, the CLI returns the exact AR2 local-gateway refusal
before dispatch. Given a non-loopback request with a valid `cliToken`, the
router returns the exact HTTP 403 AR2 envelope without a database transaction.

AC7. **Reserved first-device completion.** Given AC6, when a device claims a
name that normalizes to `alice`, then one transaction inserts the allowlisted
first device, appends one completion event, and changes the receipt to
complete. The response contains the token only after commit. When a device
first claims another normalized user, it receives `bootstrap_closed` and no
device row. After completion, Alice can add Bob through the ordinary identified
gateway path; Bob is not admin unless `--admin` was supplied.

AC8. **First root and first spawn.** Given either AC1 or the reserved AC6 state
and no client auth, when the org-token CLI performs an otherwise-valid spawn as
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

AC11. **Empty v5 migration.** Given the captured exact-v5 fixture set with zero
users and a structurally valid predecessor, when v6 boots, then migration
stamps v6, adds the guarded schema, leaves the receipt table empty, and doctor
reports `open`. A first pair then satisfies AC1. This test asserts the zero-
users predicate separately from predecessor structural validation.

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
fails with exit status nonzero. Stderr contains exactly the AR9 message shape
with the expected closed invariant and README section. The structured Boot log
contains the three AR9 fields. The application result names the failed Boot
child, and the gateway opens no listener. The v5 stamp, schema-object
inventory, canonical row census, and complete database-set membership still
match the fixture manifest, and the pinned v5 gateway can reopen the set.
Given a stamped-v6 fixture whose receipt has a deliberately corrupted
referent, v6 startup fails through the same UX and leaves the preexisting
`integrity_check` and `foreign_key_check` outcomes unchanged. When the stopped-
gateway database set is moved aside, the gateway restarts, doctor reports
`open`, provider credentials remain available, and pair-first produces the
AC1 tuple.

AC14. **Interrupted migration and rollback fence.** Given a healthy v5
database, when migration is interrupted after each rebuild/create/copy/stamp
step, then the whole operation rolls back; the schema stamp, schema-object
inventory, canonical row census, and database-set membership match the
pre-migration manifest; the pinned v5 gateway reopens the set; and a v6 retry
converges on AC12. Given the resulting v6 database, when a v5 gateway opens
it, then it refuses the v6 shape; when an older direct-writer CLI attempts its
old INSERT, then it receives `bootstrap_owned_by_gateway` and adds no row.
Restoring the stopped pre-v6 database set permits the v5 gateway to boot.

AC15. **Observable and secret-free.** Given open, reserved, and complete
fixtures, when boot summary and `doctor --json` inspect each running gateway,
then they report the exact AR9 state and action. Given an incomplete fixture,
gateway startup fails with the exact AR9 UX; doctor reports only that the
gateway is not running and does not open the database. Given accepted, replay,
incomplete, and failed claim attempts, when logs, events, responses, startup
errors, and available doctor output are searched, then provenance and rollback
status appear where AR3 and AR9 require them; no `tbt_` token, claim replay
secret, replay-secret digest, claim-token digest, org token, CLI token,
authorization header, claimed name, or provider credential appears.

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
records and disposition `att_732021c2`, when an independent reviewer reads the
control plane, then each request row remains mechanically open because each
product-owner `operator-rule` attempt was refused `not_owner`. AR1 cites the
disposition and contains exactly these choices: `gateway-local-bootstrap`,
`zero-users`, secret-proven `durable-receipt-replay`, `actor-boundary-only`,
and `named-bootstrap-and-invalid-identity`. The spec never calls a decision-
request row ruled. Visitor semantics remain in NG1, and `wi_20df0b1f` remains
untargeted with no second spec.

AC18. **Deletion boundary.** Given the implementation diff, when a reviewer
searches it, then the Rust direct user writer and its special dispatch helpers
are absent; bare local and identified `add-user` both dispatch to the gateway;
`ColdStart` owns each phase transaction; Devices and Org expose shared in-
transaction helpers; and no second SQLite mutation authority, placeholder
root, nullable operational parent, or duplicate personal-Main constructor was
added.

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

AC20. **Cross-entry races converge.** Given bootstrap-open state and barriers
on one host-local bootstrap plus one pair-first request, when the database
owner releases both, then transaction order decides the result. If pair-first
wins, the local request returns `bootstrap_closed` and AC1 is the only claim.
If host-local wins, the pair completes that reserved claim only when its
normalized user matches; otherwise it returns `bootstrap_closed` without a
device row and leaves the receipt reserved. After a matching pair completes,
each terminal outcome has one admin, one Main, one singleton receipt, and one
first device. The pair-first outcome has one accepted cold-start event. The
completed host-local outcome has one claim event and one device-completion
event. A retry converges without another user, root, receipt, or event.

AC21. **Replay proof security and falsification.** Given an unactivated
complete receipt with a known public device id, user id, request fingerprint,
and token sentinel, when requests supply no secret, malformed base64url,
31 bytes, 33 bytes, or each one-bit mutation of the valid 32-byte secret, then
none returns the sentinel or another token. Malformed base64url and each value
that decodes to 31 or 33 bytes return one WebSocket frame with exactly
`type = 'error'` and `code = 'invalid_message'`, then close the socket without
starting a claim transaction. An omitted secret and each well-formed wrong
proof return the exact AR9 `bootstrap_closed` frame. Given the exact valid
secret, the response returns the sentinel without rotation or a write. A test
spy proves the constant-time digest comparator is called only after device-id
and fingerprint equality. A scan of database rows, events, logs, doctor
output, boot output, and error responses finds neither the secret nor either
claim digest.

## Open Questions

**NON-BLOCKING control-plane reconciliation:** the five decision-request rows
listed in AR1 remain mechanically open because the product owner's five
`operator-rule` attempts returned `not_owner`. Product disposition
`att_732021c2` controls this revision's exact choices. A future owner may
reconcile the row mechanics without changing this specification. A different
product choice requires an amendment to this canonical file before handoff.

There are no other blocking or non-blocking product questions. Money,
materially new scope, visitor-principal policy, and a separate invitation
ceremony remain outside this specification.
