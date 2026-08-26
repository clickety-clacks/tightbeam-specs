# First-user bootstrap and nonexistent-user backstop

Status: SPEC-READY for one independent exact-revision re-review. Work item
`wi_20df0b1f-322b-4781-bff9-c5daef1be0f8` remains open, untargeted, and
unbound.

Authority and evidence:

- Mike ruling `dr_38c8fdb2-f08c-4555-9132-e51ed5ea488b` controls the
  bootstrap design. Rulings `dr_1ac42a7a-e81f-4ff7-b4e6-0ffb06892f16`,
  `dr_4d95f4da-3b4f-4906-a05c-24a9efabd33a`,
  `dr_9457c6e3-756d-4148-be41-39720813e254`, and
  `dr_739be284-ccd6-4b7e-a01a-a0e70a077c7e` resolve its predicate, retry,
  actor-boundary, and refusal consequences.
- Product analysis uses `clickety-clacks/tightbeam` main commit
  `f6443b7e111b18a3523f0dcf172121fbbbfdb460`.
- This file branches from `clickety-clacks/tightbeam-specs` main commit
  `8133efdab14c5470937360a2e4be7fe595639a9d`.
- Frozen handback `art_c1eccb0a` has SHA-256
  `95df828ecf46054a94606a30ef7de6e7d81ceb72f1e716635d55da0d784b6482`.
- Owner handback `art_d1ccf807` has SHA-256
  `827724e770b7e8303d5d8055660862e55abc1f329fc4f8c051e3e7ddc8abc2c9`.
- Baseline `att_11d13c2b-6eef-4c2a-b744-41d00a0c7f6a` records 9 doctests,
  1,684 Elixir tests, and 248 Rust tests with zero failures at predecessor
  source commit `8eeccbd6dfd221fe9d105783459637fb7a17ea83`.
- The fresh current-main baseline passed with the declared Erlang, Elixir,
  Rust, Node, and fixture-harness PATH: Elixir format; 9 doctests and 1,751
  tests, zero failures and 11 skips; Rust format; 246 unit tests and 4
  integration tests, zero failures; and the release CLI build.
- Independent review `att_f3bb6094-0484-4fff-89c3-3280562a3fcc` requested
  changes against predecessor artifact `art_e7fd24d8`. Its full findings are
  `art_3a3ce31b`, SHA-256
  `a070c885203631ba4c9d043a0815c744af57c1f4ae3d2ddee76a0a858b4c081e`.

This file is the only canonical specification for this work item. It replaces
the handbacks' unruled recommendations with Mike's five final rulings. It does
not bind a release or change another work item's durable state.

## Goal

G1. A valid caller shall create the first user through `POST /agent/dispatch`
with verb `add-user` while the gateway transaction observes zero users.

G2. The gateway shall admit G1 without a bearer credential, user assertion,
session, role, local-host check, or network-location check.

G3. The CLI shall call the same `POST /agent/dispatch` route for the first
user and every later user. The CLI shall never open or write `state.db`.

G4. The first successful request shall create exactly one canonical user with
`isAdmin = 1` and the ordinary accepted user-creation records.

G5. The first-user authority shall close in the same transaction that creates
the first user. A later unauthenticated request shall require approval from an
existing admin.

G6. The server shall reject an asserted user that has no canonical `users`
row before it constructs an authoritative actor.

G7. The contract shall preserve the boundary between a one-call bootstrap
authority and visitor identity. Bootstrap shall issue no reusable identity or
credential.

G8. Concurrent requests shall have one deterministic winner and shall never
expose a uniqueness failure, partial user, or unrecorded accepted mutation.

## Non-Goals

NG1. This specification does not define visitor, guest, anonymous, or other
non-human external-participant identity. Work item
`wi_4ee303fa-12ed-4747-bce0-fc48024f4d53` owns that policy.

NG2. This specification does not change raw org-token impersonation policy.
It adds only the canonical-row existence backstop after current credential
and ownership checks admit a user assertion.

NG3. This specification does not define first-device approval, personal Main
construction, operational-parent topology, provider onboarding, or a first
root session. A separately bound cold-start contract owns those effects.

NG4. This specification does not add a bootstrap endpoint, bootstrap token,
claim secret, idempotency key, receipt table, or bootstrap-specific success
record.

NG5. This specification does not add user deletion. Tightbeam at the pinned
source commit has no supported user-deletion operation.

NG6. This specification does not repair a corrupt database or infer an
unknown schema. Existing schema boot and stopped-gateway recovery rules
remain authoritative.

NG7. This specification does not implement, review, merge, release, deploy,
target, bind, or mutate a live organization.

## Terms

T1. **Canonical user** means one row in the gateway-owned `users` table.

T2. **Bootstrap-open state** means the database-owner transaction reads
`SELECT COUNT(*) FROM users` as zero. No device, session, event, receipt,
configuration, or credential row participates in this predicate.

T3. **Bootstrap-closed state** means the same transaction reads one or more
canonical users.

T4. **Bootstrap candidate** means a structurally valid protocol request to
`POST /agent/dispatch` with verb `add-user`, no explicit identity selector,
and no typed target. Its `params.userId` passes the ordinary `add-user`
validation. Its optional `params.isAdmin` passes ordinary validation.

T5. **Explicit identity selector** means a nonempty top-level `as`, `asUser`,
or `asProcess` field. Supplying one selects the ordinary authenticated path;
the gateway shall not fall back to bootstrap authority.

T6. **Bootstrap authority context** means the gateway-created call context
with origin `bootstrap:first-user`, principal `bootstrap:first-user`, and no
session. It may enter only one `add-user` transaction. It authorizes accepted
user creation only when that transaction observes T2. When the transaction
observes T3, it supplies provenance for I17's denial and authorizes no domain
write.

T7. **Ordinary path** means the existing credential, identity, target,
dispatch, rule, and admin path for `add-user`, regardless of bootstrap state.

T8. **First-user commit** means one database transaction that rechecks T2,
inserts the forced-admin user, appends the accepted `add-user` event, and
stages the ordinary `user.added` notice for delivery after the SQLite commit.
The user and event are durable transaction records. The staged notice is a
best-effort process handoff, not a durable transaction record.

T9. **Failed attempt** means an attempt whose first-user transaction does not
commit. A lost response after a commit is not a failed attempt.

T10. **Authoritative user actor** means a `{:user, userId}` principal or an
implicit session-owner user that may enter typed-target resolution or
dispatch.

## Assumptions

A1. `Tightbeam.DB` remains the only production owner of `state.db`.

A2. `BEGIN IMMEDIATE` or an equivalent database-owner transaction serializes
all paths that can insert the first `users` row.

A3. The `users` table remains the sole source of truth for whether a user
exists. The server does not infer a user from a request, device claim,
session owner string, role, event, or credential.

A4. Publishing the gateway exposes first-user authority to every peer that
can reach `POST /agent/dispatch` until the first-user commit. This exposure is
the intentional product ruling, not an authentication guarantee.

A5. Existing protocol-version and JSON-shape checks run before request
classification. They do not require a bearer credential for a bootstrap
candidate.

A6. The accepted `add-user` event is the durable provenance record for this
contract. The ordinary `user.added` notice is a best-effort projection
notification. A gateway death after the SQLite commit and before handoff
delivery may lose the notice while preserving the user and accepted event.

A7. A future supported operation that can delete the last user must obtain a
separate product ruling before it lands. This contract does not add a
historical latch that changes the zero-users predicate.

A8. A separate first-device or first-root contract may attach additional
effects to the winning first-user transaction. Those effects shall not add a
second first-user authority, endpoint, or retry receipt.

A9. The actor-context contract requires origin, principal, and attribution to
come from one closed construction step. T6 is one internal authority context;
it is not a user, session, process, role, device, or visitor identity.

## Invariants

I1. The gateway shall construct T6 only for a T4 bootstrap candidate. No wire
field shall let a caller request, name, or replay T6.

I2. T6 shall be unusable for every verb other than `add-user`. After the
first-user transaction observes T3, T6 shall authorize no accepted domain
mutation. The handler may append I17's denied audit event.

I3. An absent, malformed, or unrecognized bearer header shall not block a T4
request while T2 is true. The same request shall receive `approval_required`
while T3 is true.

I4. A request with T5 shall use T7 in both T2 and T3. Missing or invalid
credentials shall return the existing `auth_failed` response. The gateway
shall never drop the selector and retry as T6.

I5. The first-user handler shall re-read the zero-users predicate after it
owns the database write serialization boundary. A router precheck shall not
grant authority.

I6. The first-user commit shall force `isAdmin = 1`, regardless of an omitted,
true, or false `params.isAdmin` value.

I7. The user row and accepted `events` row shall commit in one SQLite
transaction. The transaction shall stage the `user.added` notice and shall
deliver it only after a successful SQLite commit. A failure before SQLite
commit shall roll back both rows and discard the staged notice. A gateway
death after SQLite commit and before handoff delivery may lose the notice; it
shall not roll back or duplicate the user or accepted event.

I8. Exactly one of two concurrent bootstrap candidates shall commit. The
loser shall return `approval_required` without a user write or accepted
event.

I9. A retry after T9 shall evaluate current state and may commit. A retry
after a lost success response shall return `approval_required`. It shall not
return the prior result or create a receipt.

I10. A WebSocket device-pair request shall not create the first canonical
user. While T2 is true, it shall return `first_user_required` without a user,
device, session, event, or credential mutation.

I11. After T3, device pairing retains its separately owned pending and
approval behavior. A staged device or user shall not receive first-user
authority.

I12. The CLI shall discover an endpoint and send an HTTP request before any
first-user decision. Local and explicit remote endpoints shall use identical
request and response semantics.

I13. The server shall validate an admitted `asUser` against `users` before
typed-target resolution, rules, accepted or denied dispatch events, and
domain writes.

I14. Session-token ownership checks shall run before I13. A selector for a
different owner shall keep `identity_not_yours`. A matching owner whose row
is absent shall return `invalid_identity`.

I15. An implicit built-in-session owner whose canonical row is absent shall
return `invalid_identity` before the gateway constructs T10.

I16. A bootstrap request shall create no visitor row, device token, session
token, org token, role binding, reusable bootstrap secret, or reusable
bootstrap principal.

I17. The gateway shall record a closed bootstrap attempt as a denied
`add-user` event with T6 attribution and `approval_required`. Actor-boundary
`invalid_identity` shall remain before dispatch and shall not create a verb
event. After the denied event commits, the gateway shall stage the ordinary
`verb.denied` notice for best-effort delivery.

I18. The response and all records shall exclude authorization headers,
gateway tokens, session tokens, device tokens, provider credentials, and
unvalidated identity claims.

I19. No CLI or helper process shall open `state.db` for first-user creation.
No second SQLite connection shall participate in I5.

## Architecture

### AR1. Product disposition and precedence

The five decision rows are ruled. They establish one design:

1. Bootstrap is permissive while `users` is empty.
2. Every caller uses the ordinary `add-user` REST route.
3. The CLI has no privileged or direct-database path.
4. The first committed user closes bootstrap.
5. Failed calls use ordinary retry semantics.
6. The server rejects nonexistent user assertions at actor construction.
7. Refusals name the true condition.

When an owner later targets and binds this work item, this contract controls
over any older overlapping clause that limits first-user creation to a local
gateway, adds a dedicated bootstrap verb, lets pairing create the first user,
or requires a bootstrap receipt for retry. Target reconciliation shall not
change separately owned first-device or first-root behavior after the first
user exists.

### AR2. Router classification

`Wire.Router` shall apply this order:

1. Validate the CLI protocol version.
2. Read and decode the JSON object.
3. Validate the required verb and the closed verb allowlist.
4. Detect explicit identity and typed-target fields.
5. Reject a typed target on `add-user` with `invalid_message`.
6. Validate the params of a selector-free, target-free `add-user` body, then
   construct T6.
7. Route every other body through existing bearer authentication and identity
   construction.

The chosen branch shall apply the ordinary per-verb param validation before a
handler mutates state.

For a T4 request, the router shall construct T6 without calling bearer-token
authentication. It shall ignore an absent or invalid bearer header for
authority. A valid bearer header does not change T6 when no explicit identity
selector exists.

For a request with T5, the router shall run the existing bearer and selector
checks. It shall never construct T6 for that request. A top-level typed target
on `add-user` shall return `invalid_message` before dispatch because user
creation has no target principal.

The transaction, not the router, decides T2 or T3. The router may classify a
selector-free request as a bootstrap candidate after closure so the handler
can return the stable closed response and denial record.

### AR3. First-user transaction

The `add-user` handler shall accept T6 and the ordinary admin context. When it
receives T6, it shall perform this ordered transaction:

1. Acquire the database write serialization boundary.
2. Read `SELECT COUNT(*) FROM users`.
3. If the result is not zero, append I17's denied event, stage the ordinary
   `verb.denied` notice for post-commit delivery, commit the denial record,
   and return `approval_required`.
4. Validate `params.userId` with the ordinary `add-user` rules.
5. Insert the user with `isAdmin = 1` and the ordinary creation timestamp.
6. Append the accepted `events` row with kind `verb`, verb `add-user`, origin
   `bootstrap:first-user`, principal `bootstrap:first-user`, and no session.
7. Stage the ordinary `user.added` notice from the committed user projection
   for best-effort handoff after SQLite commit.
8. Re-read the user and return the ordinary `add-user` result.

The SQLite commit shall make the user and accepted event durable together.
The existing `Tightbeam.DB.Txn.handoff/3` mechanism may deliver the staged
notice after that commit. The contract adds no durable outbox. If the gateway
dies after SQLite commit and before notice delivery, restart shall retain the
user and accepted event. The missing notice is an allowed result. The next
selector-free attempt shall observe T3 and return `approval_required`.

The response shall use HTTP 200 and the existing envelope:

```json
{"result":{"user":{"userId":"mike","isAdmin":true,"createdAt":0}}}
```

`createdAt` is the committed nonnegative timestamp. The example value `0`
states the field shape; it is not a required clock value.

The ordinary authenticated-admin path shall keep its current user-creation
semantics. Its transaction may share the same insertion helper, but it shall
not receive T6 attribution.

### AR4. Refusal envelopes

The selector-free `add-user` request in T3 shall return HTTP 403:

```json
{"error":{"code":"approval_required","message":"an existing admin must approve user creation"}}
```

An admitted assertion for a missing canonical user shall return HTTP 403:

```json
{"error":{"code":"invalid_identity","message":"asserted user does not exist"}}
```

The zero-user device-pair refusal shall use the existing failed
`pair_result` shape with reason `first_user_required`. Its human recovery text
shall say `create the first user through add-user`.

Malformed JSON, malformed params, invalid protocol versions, invalid
credentials, selector ownership failures, and ordinary non-admin calls shall
keep their existing error codes. A transaction exception shall return the
existing `server_error` response. A failure before SQLite commit shall satisfy
I7's rollback rule. A gateway death after commit shall satisfy I7's durable
row and best-effort notice rule.

### AR5. Actor construction

The authoritative actor constructor shall query `users` after existing
credential and session-ownership checks admit a user assertion. It shall run
before `typed_target`, `Rules.decide`, and `Dispatch.dispatch`.

The check shall cover:

1. Org-token `asUser`.
2. Session-token `asUser` after the owner-equality check.
3. The implicit owner of a built-in session.

The check shall not change authority for an existing user. It shall not add a
foreign key to every historical user-like field. A pairing `claimedName` is
not an authoritative user assertion.

### AR6. CLI and client behavior

`tightbeam add-user <userId> [--admin]` shall always discover its endpoint,
build the ordinary `add-user` body, and send it through the gateway. A bare
command shall omit all identity selectors. The first-user transaction shall
ignore `--admin` for authority and force the result to admin.

An identified CLI command shall use T7. Local endpoint discovery shall not
trigger database inspection. An explicit remote endpoint shall not disable
bootstrap.

A client that starts from T2 shall call `POST /agent/dispatch` `add-user`
before it sends a pair request. A pair request in T2 shall receive AR4's
`first_user_required` refusal. After the first user exists, device approval
continues through its separately owned policy.

### AR7. Observability and concurrency

The first-user event and notice shall use the same schemas as authenticated
`add-user`. Only their authority attribution differs. This contract shall not
add `cold-start`, `bootstrap-user`, or receipt events.

A closed selector-free attempt shall append one denied event with verb
`add-user`, origin and principal `bootstrap:first-user`, and payload code
`approval_required`. It shall stage the ordinary `verb.denied` notice for
best-effort handoff after commit of the denial record. The denied event is the
durable refusal record; a post-commit gateway death may lose only the notice.

The database-owner transaction shall serialize REST candidates with every
other user insertion path. No code shall translate a lost race into a UNIQUE
constraint or `server_error` response. The losing path shall re-evaluate the
state and return its state-specific refusal.

### AR8. Compatibility, migration, documentation, and deletion

This contract requires no new table or column. Existing databases remain
read-compatible. A database with one or more users starts in T3. An empty
database starts in T2 after normal schema validation.

An older binary is data-compatible but policy-incompatible because it can
restore the local SQLite writer or pair-first user insertion. A rollback
operator shall stop the gateway before changing binaries. No migration shall
rewrite user or event history for rollback.

The README shall replace the local-direct and pair-first bootstrap claims. It
shall teach this order:

1. Start the gateway.
2. Send `add-user` to the advertised gateway, directly or with the CLI.
3. Verify the returned user is admin.
4. Use that admin through the ordinary gateway path for later users.
5. Pair and approve devices through the separately documented device flow.

The README shall warn that any reachable peer can win step 2 while the org is
empty. It shall state that the CLI never opens `state.db`. It shall state that
an older binary remains data-compatible but can restore the superseded local
SQLite writer or pair-first policy.

The implementation deletion assessment shall name these removals:

- Delete `cli/src/users.rs` and its direct SQLite first-user tests.
- Delete `create_first_if_local`, `first_user_for_target`,
  `add_user_target_is_local`, and their local-target branching tests.
- Delete CLI help text that says the first user is created directly.
- Replace the router test that forbids empty-org wire `add-user`.
- Replace the device test that lets pairing create the first user.
- Delete or amend any dedicated `bootstrap-user`, local-only, or receipt-
  replay code that a selected target carries for this same decision.

The implementation shall retain the ordinary `add-user` verb, user
serialization, `user.added` projection, authenticated-admin path, and
post-bootstrap device approval behavior.

## Acceptance

AC1. Given a valid empty database and a selector-free remote `add-user`
request without `Authorization`, when the gateway handles it, then it returns
HTTP 200, creates one admin user, and records one accepted `add-user` event
and one `user.added` notice.

AC2. Given the same state and request through local CLI discovery, when the
CLI runs, then the gateway observes the same HTTP body and no process other
than the gateway opens `state.db`.

AC3. Given the same state and an explicit remote endpoint, when the bare CLI
command runs, then it can create the first user. A local-host predicate shall
not affect the result.

AC4. Given T2 and `isAdmin` omitted, false, or true in three fresh databases,
when each request commits, then every created user has `isAdmin = 1`.

AC5. Given two concurrent valid bootstrap candidates for different user ids,
when both complete, then exactly one returns HTTP 200. The other returns the
exact `approval_required` envelope. The `users` table contains only the
winner. The events table contains one accepted winner event and one denied
loser event.

AC6. Given a failure injected after the user insert but before the accepted
event commit, or after notice staging but before SQLite commit, when the
transaction exits, then no user or accepted event remains and no notice is
delivered. A retry can win.

AC7. Given a committed first user whose HTTP response was lost, when the same
request retries without identity, then it returns `approval_required`. It
does not return the prior result, add another user, append another accepted
event, or create a receipt. It appends I17's ordinary denied event.

AC8. Given T2 and an `asUser` selector naming the requested new user, when the
request has no valid bearer credential, then it returns `auth_failed` and
creates no row or event.

AC9. Given T2, a valid org credential, and `asUser` naming a nonexistent
user, when the request arrives, then it returns the exact `invalid_identity`
envelope before target lookup, rules, events, or writes. It does not fall back
to T6.

AC10. Given a session credential owned by `alice`, when `asUser` names `bob`,
then the gateway returns `identity_not_yours`. When it names `alice` but no
`alice` row exists, the gateway returns `invalid_identity`.

AC11. Given a built-in session whose owner row is absent, when an ordinary
verb request omits a selector and implicit identity would select that owner,
then the gateway returns `invalid_identity` before dispatch.

AC12. Given T3 and no credential or selector, when any caller sends
`add-user`, then the gateway returns the exact `approval_required` envelope,
records one denied event, and writes no user.

AC13. Given T3 and an authenticated existing admin, when the admin sends
ordinary `add-user`, then the existing path can add the requested user and
uses the admin's origin and principal.

AC14. Given T3 and an authenticated existing non-admin, when that user sends
ordinary `add-user`, then the existing `forbidden` `admin required` response
and zero-write behavior remain unchanged.

AC15. Given T2, when a device sends the former pair-first request, then the
gateway returns `first_user_required` and creates no user, device, session,
event, or credential. A concurrent REST `add-user` request can still commit.

AC16. Given a pair request and a REST request start concurrently in T2, when
both complete, then only the REST request can create the first user. The pair
request either returns `first_user_required` before the commit or follows
ordinary post-bootstrap device behavior after it.

AC17. Given an accepted or denied bootstrap call, when an auditor reads its
event, then origin and principal both equal `bootstrap:first-user`. No
request field can construct that context for another verb.

AC18. Given malformed JSON, malformed `userId`, a typed target, or an
incompatible protocol version in four tests, when each request arrives, then
the gateway returns the existing structural error before a transaction and
writes no user or accepted event.

AC19. Given the final implementation tree, when reviewers search Rust and
Elixir source, then no CLI SQLite first-user writer, local-only bootstrap
branch, dedicated bootstrap endpoint, bootstrap receipt, or pair-first user
insert remains.

AC20. Given an existing nonempty database from the pinned source, when the new
gateway boots, then it performs no schema or user migration and classifies
the org as T3.

AC21. Given the repository's full verification commands, when the coder runs
them on the implementation revision after a recorded green baseline, then
all applicable Elixir and Rust format, test, and release gates pass.

AC22. Given four fresh T2 databases and otherwise identical T4 requests with
an absent bearer header, malformed bearer header, unrecognized bearer token,
or valid bearer token, when each request runs, then each returns HTTP 200 and
creates one admin user. The four authority contexts and durable records
contain no bearer value.

AC23. Given three fresh T2 databases and otherwise valid `add-user` requests
that each contain one nonempty `as`, `asUser`, or `asProcess` selector without
a valid bearer credential, when each request runs, then each follows T7 and
returns the ordinary `auth_failed` response. No request constructs T6 or
creates a user or event.

AC24. Given two concurrent valid bootstrap candidates for the same user id,
when both complete, then exactly one returns HTTP 200. The other returns the
exact `approval_required` envelope. The database contains one user and one
accepted `add-user` event plus one denied loser event. Neither response
exposes a uniqueness error.

AC25. Given accepted bootstrap, closed bootstrap, and rejected nonexistent-
identity requests whose inputs contain distinct sentinel authorization
headers, tokens, and unvalidated identity claims, when a test reads each HTTP
response, event payload, and delivered notice, then none contains a sentinel
value. The actor-boundary rejection creates no event or notice.

AC26. Given fault injection that terminates the gateway after SQLite commits
the first user and accepted event but before `user.added` handoff delivery,
when the gateway restarts, then the user and one accepted event remain. A
`user.added` notice is not required, and a selector-free retry returns the
exact `approval_required` envelope without a second user, accepted event, or
receipt.

AC27. Given a database with a first-user commit from the new binary, when an
operator stops the gateway and selects the pinned older binary, then no
rollback migration runs and the existing user and event rows remain
unchanged. On boot the older binary observes a nonempty `users` table. The
README states that the older binary can restore the superseded local SQLite
writer or pair-first policy.

## Open Questions

None. Mike ruled the five inherited product questions. A future operation
that can delete the last user must open its own evidence-backed product
question; it does not block this contract.
