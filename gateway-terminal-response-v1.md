# Gateway terminal response — v1

Status: DRAFT r3, TARGETLESS, independent spec review required.

Source baseline: `clickety-clacks/tightbeam` `origin/main`
`8b4a3df191ca4505bf7e65a2876da23c9e4f4a6c`.

Authority: `wi_f2281739-995d-4e1e-a263-b1b044986248`, assignment
`asg_3b66f469-d788-409a-b27a-791802eb6266`.

This spec teaches no new agent operating pattern. It defines a gateway substrate
contract and its CLI presentation.

## Goal

Give one non-streaming `POST /agent/dispatch` request a durable identity and one
named terminal outcome when gateway execution encounters a database,
Credentials, Router, or handler timeout, exit, exception, or restart.

The compatible Rust CLI must render that outcome by name and request id. It must
not reduce an HTTP connection that returned an empty or invalid body to the bare
JSON parser symptom `EOF while parsing a value`.

The smallest useful mechanism is one outer terminal-response guard and one
failure-independent terminal journal. The guard owns response emission. The
journal records safe metadata before a handler can execute. Per-handler rescue
clauses lose because an unlisted handler or dependency can still exit outside
the rescue. Reusing the domain database for the journal loses because a database
timeout would disable the recorder needed to name that timeout. Keeping the
current empty-body behavior loses because it violates Tightbeam's
conspicuous-failure rule. The narrow guard plus independent journal wins because
it closes the generic seam without changing a domain command's policy.

## Non-Goals

- This contract does not change a domain handler's explicit success result, named
  returned refusal, decision-pending result, authorization decision, or domain
  transaction.
- This contract does not change the timeout duration of `Tightbeam.DB`,
  `Tightbeam.Credentials`, a handler, or an external service.
- This contract does not add a deadline for a handler that remains alive without
  producing an exit, exception, or dependency timeout.
- This contract does not cover WebSocket delivery, static assets, `/api/*`
  facades, streaming HTTP responses, or a route other than
  `POST /agent/dispatch`.
- This contract does not reopen or reclassify the closed DNS incident or the
  closed spawn incident. Their remediation and disposition stay unchanged.
- This contract does not infer that the bounded `s_7269208c --limit 50` empty-body
  symptom came from `Tightbeam.DB`. That request has no producer log binding its
  cause.
- This contract does not persist a request body, authorization header, bearer
  token, credential, transcript content, handler success result, or full response
  body in the terminal journal.
- This contract does not add a journal query verb, a new authorization role, or a
  cross-caller-scope replay facility.
- This contract does not select an implementation branch, release line,
  deployment target, or release vehicle. The work item stays targetless until a
  product owner sets a target.

## Terms

- **Compatible CLI**: the built Rust CLI whose exact pre-1.0 version passes the
  gateway's existing CLI-version check.
- **Ingress-correlated request**: a `POST /agent/dispatch` request for which the
  outer guard has acquired a valid request id. This state precedes authentication
  and acceptance.
- **Accepted request**: an authenticated and authorized dispatch request whose
  JSON, verb, identity, and target checks passed and whose `accepted` terminal
  journal row committed. The domain handler has not started when this state is
  committed.
- **Request id**: `req_` followed by one lowercase UUID-shaped value, carried in
  the `x-tightbeam-request-id` request and response header. The Rust CLI generates
  a fresh UUIDv4 request id before its first connection attempt. The gateway
  generates one UUIDv4 value when a non-CLI caller omits the header.
- **Request fingerprint**: lowercase SHA-256 hex over the exact HTTP method,
  exact path, exact request-body bytes, and accepted CLI-version header value,
  separated by zero bytes in that order. It excludes the authorization header
  and request-id header.
- **Caller scope**: the stable journal key produced after existing authentication
  and authorization. A session uses `session:<sessionKey>`. `--as-user` uses
  `user:<userId>`. A process-attributed request uses `process:<processId>`. An
  org-token role call whose dispatch principal is nil uses
  `org_token:<HMAC-SHA256(token)>`. The journal creates its 256-bit HMAC key on
  first file creation and retains that key in the journal file. It stores no
  bearer token. The request id does not participate in caller-scope derivation.
- **Boot epoch**: a random UUID committed by the terminal journal for one
  HTTP-serving subtree generation. A replacement listener begins a new epoch even
  when the terminal journal process stays alive.
- **Terminal journal**: a durable metadata store with its own file, connection,
  process owner, and supervision position. Its availability does not depend on
  `Tightbeam.DB`, `Tightbeam.Credentials`, Dispatch, or a domain handler.
- **Normal terminal response**: an explicit success, domain refusal, or
  decision-pending response returned as data by dispatch execution.
- **Generic terminal response**: one JSON error envelope defined by this spec for
  an execution failure, unavailable journal, in-progress duplicate, unknown
  post-crash outcome, terminal duplicate, or request-id conflict.
- **Terminal descriptor**: journal metadata containing terminal kind `normal` or
  `generic`, HTTP status, body SHA-256, completion time, and generic code plus an
  optional safe cause descriptor for kind `generic`. It is not a response-body
  archive.
- **Replay horizon**: 2,592,000 seconds after `terminalAt`. The journal preserves
  duplicate suppression through this interval. After it deletes an expired row,
  the same caller scope and request id can create a new acceptance.
- **Cause descriptor**: the exact closed-key object `{phase, component, kind}`.
  `phase` is one of `authenticate`, `accept`, `dispatch`, `recover`.
  `component` is one of `database`, `credentials`, `router`, `handler`,
  `terminal_store`, `gateway`, `unknown`. `kind` is one of `timeout`, `exit`,
  `exception`, `restart`, `unknown`.
- **Sanitized structural envelope**: a diagnostic representation that retains
  tuple/list shape, classifier-recognized atom names, module/function/arity,
  exception class, and a numeric timeout while replacing unrecognized atom names,
  string values, binary values, map values, request data, credential data, and
  inspected process state with `[redacted]`.
- **Recovery request**: the compatible CLI's one repeat of the exact method,
  path, body bytes, authorization, CLI version, and request id after the first
  connected attempt returns an empty body, invalid JSON, or a transport close
  before a valid HTTP body is decoded.
- **Response-started boundary**: the single call at which the outer guard sends
  the already encoded status, headers, and body through the HTTP connection.

## Assumptions

1. The source baseline enforces exact CLI compatibility before 1.0 and sends one
   non-streaming response through `send_resp`.
2. The source baseline's `Dispatch.invoke` rescues exceptions but does not convert
   an exited `GenServer.call` into dispatch data.
3. The source baseline elides large handler results from its event log. A
   metadata-only terminal journal preserves that storage boundary.
4. Recon verdict `att_21312393-13eb-4bf8-a4bb-7aef3bdec7ac` and report
   `art_2a8132e7` at SHA-256
   `57137a814699bf1ef76d8b7b9183124f752f8e0bae9b723b1e559c7487f1f0f5`
   bind the `s_ac72dc3a --limit 500` CLI EOF to a journal-observed five-second
   `GenServer.call(Tightbeam.DB, ...)` timeout in the transcript producer path.
5. Closed work item `wi_890c351c-45c7-4224-a885-0202bf0788e2` contains
   producer-specific evidence that the spawn path encountered a distinct
   `Tightbeam.Credentials` timeout before its empty-body CLI EOF. This spec uses
   that evidence only to select a second failure component for acceptance.
6. Addendum `art_03b75465` at SHA-256
   `8379ebb16f3b078dd45d4a9ebbb15b84de149cb61a81073c9cc8cebb5832eb35`
   establishes that the bounded `s_7269208c --limit 50` fail/retry has an unknown
   upstream cause. Its timing near database timeouts and Router recovery does not
   classify that request.
7. A process exit or machine crash can occur after a domain mutation commits and
   before the terminal descriptor commits. The gateway cannot derive the domain
   outcome generically after that gap.
8. A disconnected client cannot acknowledge receipt. The terminal journal can
   prove server state, not client receipt.
9. The terminal journal's backing filesystem remains readable and writable while
   one accepted request executes. Process-owner exits are in scope; persistent
   media loss is outside the existence guarantee because no durable mechanism can
   commit through an unavailable medium.
10. A compatible CLI uses a fresh random request id for a new command, so its
    bounded recovery completes inside the replay horizon.

## Invariants

**INV-01 — One durable identity.** The compatible CLI generates one request id
before its first connection attempt and reuses it for its one recovery request.
The gateway echoes the request id in `x-tightbeam-request-id` on a response it
emits after ingress correlation.

**INV-02 — Acceptance precedes effects.** The gateway commits an `accepted` row
before it calls Rules, Dispatch, or a domain handler. A journal commit failure
returns `gateway_terminal_store_unavailable`; the handler does not start.

**INV-03 — Existing authorization stays first.** The gateway completes its
existing version, authentication, `--as-user`, identity, role, and target checks
before it looks up or creates a caller-scoped acceptance row. A request id grants
no access and reveals no other caller scope's row.

**INV-04 — One response owner.** The outer guard owns the response-started
boundary. Rules, Dispatch, classifiers, and handlers return data to that guard;
they do not receive the connection and do not send bytes.

**INV-05 — Failure isolation.** The guard runs the dispatch request pipeline in a
monitored execution process. The guard converts that process's
returned data, exception, exit, or observed dependency timeout into data before
it begins the HTTP response.

**INV-06 — Named generic envelope.** A generic terminal response has this exact
top-level shape:

```json
{
  "error": {
    "code": "gateway_outcome_unknown",
    "message": "gateway request outcome is unknown",
    "requestId": "req_018f3c42-15e7-4db8-a8f0-6aa09385b32f",
    "cause": {
      "phase": "dispatch",
      "component": "database",
      "kind": "timeout"
    }
  }
}
```

The envelope has the exact keys `code`, `message`, `requestId`, and `cause` for a
cause-bearing error. A state error that has no upstream execution cause replaces
`cause` with the exact `state` object defined in Architecture.

**INV-07 — Closed cause classification.** The classifier emits only cause values
listed in Terms. It classifies from the caught exit/exception term and the guard's
current phase. It emits `unknown` for a field it cannot bind from that evidence.
It does not classify from temporal proximity, another request's logs, or a later
successful retry.

**INV-08 — Secret-free durability.** The terminal journal stores the fields
listed in Architecture. It stores no request body, authorization header, bearer
token, credential, transcript content, handler success result, full response
body, raw exception text, raw exit term, or stack-local value.

**INV-09 — Accepted-request terminalization before send.** For an accepted
request, the guard commits a terminal descriptor before it crosses the
response-started boundary. A client disconnect during send leaves the descriptor
terminal and does not cancel handler execution. A pre-accept response follows
INV-19 and has no terminal descriptor.

**INV-10 — Request-id conflict blocks execution.** For one caller scope,
reuse of a request id with a different request fingerprint returns
`request_id_conflict` with HTTP 409. The gateway does not execute the second
request.

**INV-11 — Live duplicate blocks execution.** For one caller scope and
fingerprint, a duplicate whose accepted row belongs to the current boot epoch and
has no terminal descriptor returns `gateway_request_in_progress` with HTTP 409.
The gateway does not start a second execution.

**INV-12 — Prior-boot acceptance becomes unknown.** Before the gateway serves
dispatch traffic, recovery changes each nonterminal accepted row from an older
boot epoch to terminal code `gateway_outcome_unknown`, HTTP 500, and cause
`{phase: recover, component: gateway, kind: restart}`. A duplicate returns that
descriptor and does not execute the handler.

**INV-13 — Normal response bytes stay out of replay storage.** A duplicate of a
normal terminal request returns `request_already_terminal` with HTTP 409 and a
state object that contains the prior status and body SHA-256. The response
contains no prior success result or domain response body. The gateway does not
execute the handler.

**INV-14 — Compatible CLI performs one bounded recovery.** After a connected
attempt yields an empty body, invalid JSON, or a transport close before a valid
body is decoded, the CLI sends one recovery request. It sends no third attempt.
It does not automatically recover from a decoded server error or from a
pre-connection DNS failure.

**INV-15 — CLI names the final condition.** For a decoded generic response, the
CLI prints its stable code, message, request id, and cause or state fields. If the
one recovery request also lacks a decodable terminal response, the CLI prints
`gateway_terminal_response_missing`, the request id, and `outcome unknown`. It
does not print a bare JSON parser EOF as the command's error.

**INV-16 — Existing explicit responses retain their domain shape.** An explicit
success, returned domain refusal, or decision-pending response retains its
source-baseline status and JSON body. The guard adds only
`x-tightbeam-request-id`.

**INV-17 — Unknown stays unknown.** An unmatched execution failure commits cause
`{phase: <observed phase>, component: unknown, kind: unknown}` plus a sanitized
structural envelope. The public response contains the cause descriptor and omits
the structural envelope.

**INV-18 — Domain audit remains authoritative.** Existing EventLog and domain
rows retain their source-baseline writes. The terminal journal adds transport
and execution-lifecycle evidence; it does not replace or synthesize a domain
event.

**INV-19 — Pre-accept failure is named but not accepted.** A monitored Router
failure or returned terminal-store unavailability before acceptance produces a
generic cause-bearing response when the outer guard remains alive. The terminal
journal contains no acceptance or terminal row because no caller scope committed.

**INV-20 — Journal-owner exit closes before send.** If the terminal journal owner
exits after acceptance and before terminalization, the outer guard sends no
response bytes. Supervision restarts the journal and HTTP-serving subtree. Boot
recovery applies INV-12 before the listener accepts a recovery request.

**INV-21 — Dead execution owner becomes unknown.** At acceptance, the terminal
journal monitors the outer guard that owns the accepted execution. If that guard
dies before terminalization while the journal stays alive, the journal commits
`gateway_outcome_unknown`, HTTP 500, and cause
`{phase: recover, component: gateway, kind: exit}`. A duplicate does not execute
the handler.

**INV-22 — Cause does not assert domain outcome.** A caught timeout, exit, or
exception after handler selection returns code `gateway_outcome_unknown` and
message `gateway request outcome is unknown`. Its cause descriptor retains the
proven phase, component, and kind. The gateway uses
`gateway_execution_failed` only before handler selection proves that no domain
handler ran.

**INV-23 — Replay retention is bounded and reserved.** The journal deletes a
terminal row only after its replay horizon expires. Before acceptance, it removes
expired rows and reserves capacity for the accepted row's maximum terminal
descriptor. If it cannot reserve that capacity, it returns the pre-accept
`gateway_terminal_store_unavailable` response. An accepted row keeps its reserved
capacity through terminalization.

**INV-24 — Org-token rebinding is explicit.** An org token's HMAC defines its
caller scope independently of its current role. Existing authorization under the
current role runs before journal lookup. Rebinding the same token to another role
preserves duplicate suppression for that token. Replacing the token creates a new
caller scope.

## Architecture

### A. Outer guard and execution boundary

`POST /agent/dispatch` enters a route-specific outer guard before the current
Router logic. The guard acquires or validates a request id, then runs the current
version/authentication/body/verb/identity/target pipeline in a monitored worker.
The outer process retains the connection. The worker returns a tagged value. Its
monitor exit is data to the outer process.

Dispatch changes its raised-handler exception rescue to return an internal
`handler_exception` tag to the guard. It does not place `Exception.message/1` in
the public domain-error tuple. An explicit error tuple returned by a handler stays
a normal terminal response under INV-16.

A Router or handler boundary tag is evidence only when the named boundary emits
the tag before its own timeout or exit, or when a supervisor action record names
that boundary as its direct target. A wrapper does not retag a caught nested exit
as its enclosing Router or handler. The raw nested term proceeds to the closed
classifier.

The guard does not start a general wall-clock timer. A five-second
`GenServer.call` timeout remains the dependency's timeout and arrives as an exit
term. An alive handler without such an event remains outside this version.

After authorization, the worker asks the terminal journal to accept the request.
The journal keys a row by `(caller scope, request id)`. The worker may call
Rules and Dispatch only after the journal confirms the committed acceptance.

For an accepted request, the outer guard encodes one complete body, asks the
journal to commit its terminal descriptor, and then calls the single
response-started boundary. A normal terminal body is not stored; its SHA-256 and
classification are stored. A generic terminal body is deterministic from its
descriptor and can be reconstructed.

A Router failure before acceptance has no caller-scope journal key. The
outer guard returns its generic response without creating a journal row. If an
accept call returns `unavailable` while the journal owner remains alive, the
guard returns the pre-accept 503 response in section C. If the journal owner exits
after acceptance, its supervision position restarts the HTTP-serving subtree;
the interrupted guard crosses no response-started boundary. Reconciliation in
the next boot epoch converts the durable accepted row to
`gateway_outcome_unknown` before the listener starts.

At acceptance, the journal also installs a runtime monitor on the outer guard.
A monitor `DOWN` before terminalization changes that row to
`gateway_outcome_unknown` with the INV-21 cause. The guard owns and links its
monitored execution worker, so guard death terminates that worker. The unknown
classification does not claim whether a racing domain transaction committed.

### B. Request-id wire rules

The accepted request-id syntax is the regular language
`req_[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}`. The gateway
returns `invalid_request_id` with HTTP 400 for a present value outside this
language. The guard generates a valid value when the header is absent. The CLI
supplies the header on its first attempt.

An emitted response after ingress correlation carries:

```text
x-tightbeam-request-id: req_018f3c42-15e7-4db8-a8f0-6aa09385b32f
content-type: application/json
```

The request id in a generic JSON body equals the response header byte for byte.
The generic body uses compact UTF-8 JSON with keys in the order shown in INV-06
and section C. Descriptor reconstruction uses the same encoder, so its body hash
is stable.

### C. Generic codes and HTTP mapping

The guard uses these exact mappings:

| Condition | Code | HTTP | Message |
|---|---|---:|---|
| Caught timeout before handler selection | `gateway_execution_failed` | 504 | `gateway request failed` |
| Caught exit, exception, or unknown failure before handler selection | `gateway_execution_failed` | 500 | `gateway request failed` |
| Caught timeout after handler selection | `gateway_outcome_unknown` | 504 | `gateway request outcome is unknown` |
| Caught exit, exception, or unknown failure after handler selection | `gateway_outcome_unknown` | 500 | `gateway request outcome is unknown` |
| Terminal journal unavailable before acceptance | `gateway_terminal_store_unavailable` | 503 | `gateway terminal store unavailable` |
| Same current-boot request still executing | `gateway_request_in_progress` | 409 | `gateway request is in progress` |
| Older-boot accepted request or dead execution owner lacks a terminal descriptor | `gateway_outcome_unknown` | 500 | `gateway request outcome is unknown` |
| Same request has a normal terminal descriptor and body is not replayed | `request_already_terminal` | 409 | `gateway request is already terminal` |
| Same caller scope and request id have a different fingerprint | `request_id_conflict` | 409 | `request id conflicts with accepted request` |

`gateway_execution_failed` and `gateway_outcome_unknown` carry a cause object. A
terminal-store failure uses cause
`{phase: accept, component: terminal_store, kind: exit}` or kind `timeout` when
the caught term proves a timeout. Another returned unavailability uses kind
`unknown`. Boot recovery uses the restart cause in INV-12.

The three state responses carry this exact object in place of `cause`:

```json
{
  "state": {
    "status": 200,
    "bodySha256": "6f1ed002ab5595859014ebf0951522d9a699b6af5078c2d496eb29a620630f13"
  }
}
```

For `gateway_request_in_progress`, both state values are JSON `null`. For
`request_id_conflict`, both state values are JSON `null`. For
`request_already_terminal`, both values come from the committed terminal
descriptor. The outer error object still contains exact keys `code`, `message`,
`requestId`, and `state`.

### D. Cause classification

The classifier applies these rules in order:

1. An exit term for `GenServer.call` whose registered destination is
   `Tightbeam.DB` and whose reason proves timeout maps to
   `{<phase>, database, timeout}`.
2. Another exit term for `GenServer.call` whose registered destination is
   `Tightbeam.DB` maps to `{<phase>, database, exit}`.
3. An exit term for `GenServer.call` whose registered destination is
   `Tightbeam.Credentials` and whose reason proves timeout maps to
   `{<phase>, credentials, timeout}`.
4. Another exit term for `GenServer.call` whose registered destination is
   `Tightbeam.Credentials` maps to `{<phase>, credentials, exit}`.
5. A Router-boundary monitor term that names the Router boundary and proves a
   timeout maps to `{<phase>, router, timeout}`.
6. A Router-boundary monitor term that names the Router boundary and proves a
   non-timeout exit maps to `{<phase>, router, exit}`.
7. An internal `handler_exception` tag that names the selected handler module and
   whose first non-guard stack frame belongs to that module maps to
   `{dispatch, handler, exception}`.
8. A handler-boundary monitor term that names the selected handler module and
   proves a direct boundary timeout maps to `{dispatch, handler, timeout}`.
9. A handler-boundary monitor term that names the selected handler module and
   proves a direct non-timeout boundary exit maps to
   `{dispatch, handler, exit}`.
10. Boot recovery maps to `{recover, gateway, restart}`.
11. For a remaining term, the classifier sets component to `unknown`. It sets
    kind to `timeout`, `exception`, or `exit` only when the term itself proves
    that kind; otherwise it sets kind to `unknown`.

The phase is the guard's stage at the instant it observes the term. Execution
position alone does not identify a component. An unmatched dependency exit from
inside a Router or handler maps through rule 11 to `unknown`. The classifier
writes the sanitized structural envelope only to the journal's restricted
diagnostic field. It does not copy that field into the HTTP body or CLI output.

### E. Terminal journal record

One journal row stores:

- caller-scope kind and canonical id or HMAC;
- authenticated role at acceptance for an org-token caller;
- request id and request fingerprint;
- boot epoch;
- route, verb, target kind, and canonical target id;
- accepted timestamp;
- state `accepted` or `terminal`;
- terminal timestamp, terminal kind, HTTP status, and body SHA-256 when terminal;
- stable code when terminal kind is `generic`;
- cause phase, component, and kind when a cause exists;
- one generated failure correlation id and sanitized structural envelope when an
  execution failure exists.

The journal stores the target id already authorized for the caller scope.
It stores no caller-supplied display label or free-form origin. The process owner
serializes acceptance and terminalization. A unique constraint on caller scope
plus request id makes duplicate resolution deterministic.

The journal stores `retentionSeconds = 2592000` and
`maxRows = 250000` as schema-versioned constants. Before one acceptance, it
deletes terminal rows whose `terminalAt + retentionSeconds` is not greater than
the transaction time. It then refuses acceptance with
`gateway_terminal_store_unavailable` when the remaining row count equals
`maxRows`. One accepted row reserves the fixed descriptor columns that its
terminal update uses. A schema version change may change either constant only
through a later spec amendment.

The journal metadata table stores the randomly generated HMAC key used for
org-token caller scopes. It uses file permissions equal to the domain database's
existing private-file permissions. Logs, events, responses, and diagnostic
envelopes omit that key and each bearer token.

The terminal journal uses a SQLite file distinct from the files owned by
`Tightbeam.DB` and EventLog. Its supervision child starts before
`Tightbeam.DB`, `Tightbeam.Credentials`, Router, and the HTTP listener. A restart
of one of those later children leaves the journal owner and file available. The
HTTP-serving subtree asks the journal to commit a fresh boot epoch on each start.
The HTTP listener starts after rows from earlier epochs are reconciled. This rule
also covers a listener restart caused by a `rest_for_one` restart below the
surviving journal owner.

### F. Duplicate and recovery state machine

For the same caller scope and request id:

```text
no row + same request       -> commit accepted -> execute once
accepted + current epoch    -> gateway_request_in_progress
accepted + older epoch      -> gateway_outcome_unknown
terminal + generic failure  -> reconstruct the committed generic response
terminal + normal response  -> request_already_terminal
row + different fingerprint -> request_id_conflict
```

Authentication and authorization run before this lookup. A caller using another
scope follows that scope's independent key space and cannot inspect the first
scope's state. The existing authorization path may reject it before the journal
lookup. Rebinding one org token preserves its HMAC caller scope and stored
accepted-role metadata. Replacing that token produces another HMAC caller scope.

The CLI recovery request is byte-identical at the fingerprint inputs. It may
cause first execution only when the first attempt failed before acceptance and
left no row. A current execution continues after client disconnect. A prior-boot
row becomes unknown because the generic gateway cannot prove whether the domain
effect committed. Neither case starts a duplicate execution.

### G. CLI rendering

The CLI renders the example database timeout after handler selection as one line:

```text
gateway_outcome_unknown: gateway request outcome is unknown (request req_018f3c42-15e7-4db8-a8f0-6aa09385b32f; phase dispatch; component database; kind timeout)
```

A state error uses the same prefix and request-id placement, followed by the
state fields in the order `status`, `bodySha256`.
Null-valued state fields are omitted from the parenthetical display. The CLI
keeps its existing rendering for a decoded normal success or domain refusal.

If both attempts fail before a valid body is decoded, the CLI renders:

```text
gateway_terminal_response_missing: gateway returned no decodable terminal response (request req_018f3c42-15e7-4db8-a8f0-6aa09385b32f; outcome unknown)
```

The process exits nonzero for each generic error. A normal success keeps its
existing exit status.

### H. Observability

One structured log event named `gateway_terminal` accompanies each journal
terminalization. It contains request id, caller-scope kind and id or HMAC, route,
verb, target kind and id, boot epoch, accepted and terminal timestamps, terminal
kind, HTTP status, body SHA-256, failure correlation id, generic code, and cause
descriptor. It omits fields that the terminal descriptor does not have.

One structured log event named `gateway_terminal_send_failed` records a send
failure after terminalization. It carries request id, one generated send-failure
correlation id, and the committed generic code when present. It does not change
the committed terminal state.

One structured log event named `gateway_preaccept_failure` records a Router or
terminal-store failure before acceptance. It carries request id, phase,
component, kind, HTTP status, and stable code. It carries no caller scope or
target because acceptance did not commit.

The existing EventLog continues to record domain dispatch outcomes under its
source-baseline rules. Operators correlate the terminal journal, structured log,
and domain event by request id or failure correlation id. The public wire reveals
the request id and safe cause descriptor, not the sanitized structural envelope.

## Acceptance

AC-01 and AC-02 run against a fresh file-backed gateway, the built release CLI,
and the named real producer paths. AC-03 through AC-09 and AC-11 through AC-26
run against a fresh file-backed candidate gateway and use the real boundary named
in the clause. AC-10 is the CLI-only protocol-endpoint exception. A deterministic
test coordination seam may pause a named process after acceptance; a handwritten
replacement handler may not stand in for the transcript or spawn producer path.

**AC-01 — Journal-bound transcript database timeout (INV-01, INV-02, INV-05,
INV-06, INV-07, INV-09, INV-15, INV-22).**

Given an authenticated transcript request for a seeded session and limit 500,
and given the test seam pauses `Tightbeam.DB` after the terminal journal commits
acceptance but before the real transcript handler calls it,
when the built CLI sends the request and the real `GenServer.call` reaches its
five-second timeout,
then the gateway returns HTTP 504 with header `x-tightbeam-request-id`, code
`gateway_outcome_unknown`, message `gateway request outcome is unknown`, and cause
`{phase: dispatch, component: database, kind: timeout}`,
and the CLI output contains that code and request id and contains no bare `EOF
while parsing a value`.

The fixture captures the real exit shape and asserts that the classifier matched
it. This case is the deterministic descendant of the independently journal-bound
`s_ac72dc3a --limit 500` evidence. It does not use `s_7269208c --limit 50` as a
database fixture.

**AC-02 — Distinct Credentials timeout (INV-02, INV-05, INV-06, INV-07,
INV-09, INV-22).**

Given a seeded spawn request whose real handler calls `Tightbeam.Credentials`,
and given the test seam pauses `Tightbeam.Credentials` after acceptance,
when the built CLI sends the spawn request and the real `GenServer.call` reaches
its five-second timeout,
then the gateway returns HTTP 504 with code `gateway_outcome_unknown` and cause
`{phase: dispatch, component: credentials, kind: timeout}`,
and the terminal journal contains one accepted row and one terminal descriptor
for that request id.

This case uses the producer-specific Credentials evidence from closed
`wi_890c351c-45c7-4224-a885-0202bf0788e2` to select the component. It does not
change that closed work item.

**AC-03 — Unmatched failure remains unknown (INV-07, INV-17, INV-22).**

Given the monitored execution process receives a deterministic term that proves
neither a component nor a kind after handler selection,
when the guard classifies the caught term,
then the HTTP response is 500 `gateway_outcome_unknown` with cause
`{phase: dispatch, component: unknown, kind: unknown}`,
and the journal stores one sanitized structural envelope whose string, binary,
map-value, request, credential, and process-state positions equal `[redacted]`.

This case proves the treatment required by `art_03b75465`; it does not assert a
database cause for the bounded fail/retry symptom.

**AC-04 — Authentication remains authoritative (INV-03).**

Given principal A has an accepted or terminal row for request id R,
when principal B sends the same request id and body without authorization for the
requested identity or target,
then the gateway returns the source-baseline authorization response,
and the terminal journal performs no lookup result disclosure and starts no
handler for principal B.

**AC-05 — Acceptance-store failure prevents effects (INV-02, INV-19).**

Given the live terminal journal owner returns `unavailable` before acceptance,
when an otherwise valid authenticated dispatch request reaches the acceptance
step,
then the gateway returns HTTP 503 with code
`gateway_terminal_store_unavailable` and cause
`{phase: accept, component: terminal_store, kind: unknown}`,
and the domain handler invocation count remains zero,
and `gateway_preaccept_failure` contains the request id and contains no caller
scope or target.

**AC-06 — Same-id fingerprint conflict (INV-10).**

Given caller scope A has an accepted row for request id R and body fingerprint F1
after one handler invocation,
when caller scope A sends request id R with body fingerprint F2,
then the gateway returns HTTP 409 with code `request_id_conflict`,
and the domain handler invocation count for R remains one.

**AC-07 — Disconnect before send (INV-09, INV-11, INV-13).**

Given the journal accepted a request and the client closes its socket while the
real handler executes,
when the handler returns a normal success,
then the journal commits one `normal` descriptor before the send attempt,
and a later request from the same caller scope with the same request id and
fingerprint returns HTTP 409 `request_already_terminal` with the committed status,
code, and body SHA-256 and does not invoke the handler again.

**AC-08 — Live duplicate (INV-11).**

Given a current-epoch accepted request is paused inside its real handler,
when the same caller scope sends the same request id and fingerprint,
then the duplicate returns HTTP 409 `gateway_request_in_progress`,
and the handler invocation count remains one.

**AC-09 — Crash gap and restart (INV-12).**

Given a real handler's domain transaction commits and the test process kills the
gateway after that commit but before terminal journal terminalization,
when the gateway restarts and reconciles old boot epochs,
then the row becomes HTTP 500 `gateway_outcome_unknown` with cause
`{phase: recover, component: gateway, kind: restart}`,
and a same-caller-scope retry with the same request id and fingerprint returns that
descriptor without another domain mutation.

**AC-10 — Empty-body bounded recovery (INV-01, INV-14, INV-15).**

Given a protocol test endpoint accepts a compatible CLI request and closes the
first connected response with an empty body before acceptance,
when the endpoint returns a decodable success response to the CLI's recovery
request,
then both attempts carry the same request id and exact fingerprint inputs,
and the handler invocation count is one.

Given the endpoint also closes the recovery response without decodable JSON,
when the CLI finishes,
then it sends two total attempts, exits nonzero, and prints
`gateway_terminal_response_missing`, the request id, and `outcome unknown` with no
bare parser EOF.

**AC-11 — Generic failure replay (INV-09, INV-14).**

Given an accepted request committed a deterministic generic terminal response and
the client lost its first response,
when the compatible CLI sends its recovery request with the same request id and
fingerprint,
then the gateway reconstructs the same code, message, request id, cause, HTTP
status, and body SHA-256 from the descriptor,
and the handler invocation count remains one.

**AC-12 — Response-started structure (INV-04, INV-09).**

Given the candidate production source,
when a source-structure test counts response emission call sites for
`POST /agent/dispatch`,
then exactly one guard-owned response-started call site can send the route's
status, headers, and body,
and Rules, Dispatch, classifiers, and domain handler modules contain zero route
response emission call sites.

**AC-13 — Normal-response compatibility (INV-16).**

Given fixtures captured from real gateway responses at source commit
`8b4a3df191ca4505bf7e65a2876da23c9e4f4a6c` for one explicit success, one
explicitly returned domain refusal, and one decision-pending result, and given
the test records that commit plus each fixture file's SHA-256,
when the candidate gateway handles those requests,
then each status and JSON body is byte-identical to its pinned fixture,
and each response adds one `x-tightbeam-request-id` header.

**AC-14 — Version boundary (INV-03, INV-14).**

Given a CLI version that fails the source-baseline exact-version check,
when it sends `POST /agent/dispatch`,
then the gateway returns the source-baseline HTTP 426 response,
and the client performs no terminal recovery request and no accepted journal row
is created.

**AC-15 — Secret exclusion and correlation (INV-08, INV-18).**

Given a request whose body, authorization header, credential result, transcript
result, and raised exception contain five distinct canary strings,
when the guard commits an unknown generic failure and emits its structured logs,
then none of the five canaries occurs in the terminal journal file or structured
log output,
and the response header, response body, terminal row, and `gateway_terminal` log
contain the same request id.

**AC-16 — Router exit (INV-05, INV-07, INV-19).**

Given the Router boundary emits a tag that names itself and proves its direct
non-timeout exit after ingress correlation during the authentication phase and
before handler selection,
when the outer guard observes the monitor event,
then it returns HTTP 500 `gateway_execution_failed` with cause
`{phase: authenticate, component: router, kind: exit}`,
and it emits one response-started call and creates no journal row,
and `gateway_preaccept_failure` contains the same request id and cause.

**AC-17 — Handler timeout and exit (INV-05, INV-07, INV-22).**

Given Dispatch selected a test-registered production-shape handler and the handler
emits a boundary tag that names itself and proves its direct timeout,
when the outer guard observes the monitored execution exit,
then it returns HTTP 504 `gateway_outcome_unknown` with cause
`{phase: dispatch, component: handler, kind: timeout}`.

Given the same handler emits a boundary tag that names itself and proves its
direct non-timeout exit,
when the outer guard observes the monitored execution exit,
then it returns HTTP 500 `gateway_outcome_unknown` with cause
`{phase: dispatch, component: handler, kind: exit}`.

**AC-18 — Router timeout (INV-05, INV-07, INV-19).**

Given the Router boundary emits a tag that names itself and proves its direct
timeout during the authentication phase and before handler selection,
when the outer guard observes the monitor event,
then it returns HTTP 504 `gateway_execution_failed` with cause
`{phase: authenticate, component: router, kind: timeout}`,
and it creates no journal row,
and `gateway_preaccept_failure` contains the same request id and cause.

**AC-19 — Handler exception (INV-05, INV-07, INV-08, INV-22).**

Given Dispatch selected a test-registered production-shape handler and the
handler raises an exception whose message contains a canary string,
when the outer guard receives the classified result,
then it returns HTTP 500 `gateway_outcome_unknown` with cause
`{phase: dispatch, component: handler, kind: exception}`,
and the public body and structured log omit the canary string.

**AC-20 — Journal-owner exit after acceptance (INV-12, INV-20).**

Given one accepted row committed in boot epoch E1 and the test process terminates
the terminal journal owner before terminalization,
when supervision starts boot epoch E2,
then the interrupted connection receives zero response bytes before closing,
and reconciliation commits `gateway_outcome_unknown` before the HTTP listener
starts,
and the compatible CLI's same-id recovery request returns that named response
without a second handler invocation.

**AC-21 — Outer-guard exit while journal survives (INV-21).**

Given one accepted request whose real handler is paused and whose terminal
journal stays alive,
when the test process terminates the outer guard,
then the guard's linked execution worker terminates,
and the journal commits HTTP 500 `gateway_outcome_unknown` with cause
`{phase: recover, component: gateway, kind: exit}`,
and a same-caller-scope same-fingerprint request returns that response without a
second handler invocation.

**AC-22 — Post-effect exit preserves unknown outcome (INV-22).**

Given a test-registered production-shape handler commits one seeded domain effect
and then emits a boundary tag that names itself and proves its direct exit,
when the outer guard classifies that exit,
then the response is HTTP 500 `gateway_outcome_unknown` with cause
`{phase: dispatch, component: handler, kind: exit}`,
and the domain effect count is one,
and the public message contains no claim that the domain effect failed.

**AC-23 — Complete caller scopes and role rebinding (INV-03, INV-24).**

Given one session call, one `--as-user` call, one process-attributed call, and one
nil-principal org-token role call pass their source-baseline authorization,
when each request commits acceptance,
then the four journal keys begin with `session:`, `user:`, `process:`, and
`org_token:` respectively,
and the journal file and logs contain no bearer-token canary.

Given the same org token is rebound from role R1 to role R2 and the R2
authorization check passes for the repeated request,
when the caller repeats the request id and fingerprint,
then the journal resolves the R1 acceptance through the same HMAC caller scope
and starts no second handler.

Given a replacement org token authenticates as R2,
when it sends that request id and fingerprint,
then its different HMAC defines a different caller scope.

**AC-24 — Replay retention and capacity (INV-23).**

Given transaction time T and a terminal row whose `terminalAt + 2592000` equals
T,
when the journal begins an acceptance transaction,
then it deletes that expired row before duplicate lookup,
and the same caller scope and request id may commit a new acceptance.

Given 250000 unexpired or accepted rows remain after expiry deletion,
when another valid request reaches acceptance,
then the gateway returns HTTP 503 `gateway_terminal_store_unavailable`,
and the journal creates no row and the domain handler invocation count remains
zero.

**AC-25 — Normal duplicate state is closed (INV-13).**

Given a normal terminal response committed status 200 and body SHA-256 H,
when the same caller scope repeats its request id and fingerprint inside the
replay horizon,
then the HTTP 409 `request_already_terminal` state object has exact keys `status`
and `bodySha256` with values 200 and H,
and the state object has no `terminalClass` or `code` key.

**AC-26 — Nested dependency is not relabeled (INV-07, INV-17, INV-22).**

Given a selected handler calls an unlisted nested dependency and the caught term
proves a timeout without naming that dependency,
when the classifier receives the term,
then the response is HTTP 504 `gateway_outcome_unknown` with cause
`{phase: dispatch, component: unknown, kind: timeout}`,
and the cause contains neither `handler` nor `router`.

## Open Questions

None. The document remains DRAFT until one independent spec reviewer clears its
requirements, architecture, evidence boundaries, and acceptance traceability.
The producer must amend this canonical file before resolving a defect found by
that review. The work item receives a path and content-hash binding only after the
review clears the amended text.
