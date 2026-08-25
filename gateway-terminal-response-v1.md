# Gateway terminal response — v1

Status: DRAFT r1, TARGETLESS, independent spec review required.

Source baseline: `clickety-clacks/tightbeam` `origin/main`
`6796338b9a207edf75f4e245361d76c1c14f33d9`.

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

- This contract does not change a domain handler's success result, named refusal,
  decision-pending result, authorization decision, or domain transaction.
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
  cross-principal replay facility.
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
- **Request id**: `req_` followed by one lowercase canonical UUID, carried in the
  `x-tightbeam-request-id` request and response header. The Rust CLI generates a
  fresh request id before its first connection attempt. The gateway generates
  one when a non-CLI caller omits the header.
- **Request fingerprint**: lowercase SHA-256 hex over the exact HTTP method,
  exact path, exact request-body bytes, and accepted CLI-version header value,
  separated by zero bytes in that order. It excludes the authorization header
  and request-id header.
- **Effective principal**: the canonical session or user principal produced by
  the existing version, bearer-authentication, `--as-user`, identity, role, and
  target checks. The request id does not participate in this derivation.
- **Boot epoch**: a random UUID written by the terminal journal owner before the
  gateway begins serving dispatch requests. One running gateway instance uses
  one boot epoch.
- **Terminal journal**: a durable metadata store with its own file, connection,
  process owner, and supervision position. Its availability does not depend on
  `Tightbeam.DB`, `Tightbeam.Credentials`, Dispatch, or a domain handler.
- **Normal terminal response**: an existing success, domain refusal, or
  decision-pending response returned as data by dispatch execution.
- **Generic terminal response**: one JSON error envelope defined by this spec for
  an execution failure, unavailable journal, in-progress duplicate, unknown
  post-crash outcome, terminal duplicate, or request-id conflict.
- **Terminal descriptor**: journal metadata containing terminal class, HTTP
  status, stable code, body SHA-256, completion time, and a safe cause descriptor.
  It is not a response-body archive.
- **Cause descriptor**: the exact closed-key object `{phase, component, kind}`.
  `phase` is one of `authenticate`, `accept`, `dispatch`, `respond`, `recover`.
  `component` is one of `database`, `credentials`, `router`, `handler`,
  `terminal_store`, `gateway`, `unknown`. `kind` is one of `timeout`, `exit`,
  `exception`, `restart`, `unknown`.
- **Sanitized structural envelope**: a diagnostic representation that retains
  tuple/list shape, atom names, module/function/arity, exception class, and a
  numeric timeout while replacing string values, binary values, map values,
  request data, credential data, and inspected process state with `[redacted]`.
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
before it looks up or creates a principal-scoped acceptance row. A request id
grants no access and reveals no other principal's row.

**INV-04 — One response owner.** The outer guard owns the response-started
boundary. Rules, Dispatch, classifiers, and handlers return data to that guard;
they do not receive the connection and do not send bytes.

**INV-05 — Failure isolation.** The guard runs the authenticated dispatch
pipeline in a monitored execution process. The guard converts that process's
returned data, exception, exit, or observed dependency timeout into data before
it begins the HTTP response.

**INV-06 — Named generic envelope.** A generic terminal response has this exact
top-level shape:

```json
{
  "error": {
    "code": "gateway_execution_failed",
    "message": "gateway request failed",
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

**INV-09 — Durable terminalization before send.** The guard commits a terminal
descriptor before it crosses the response-started boundary. A client disconnect
during send leaves the descriptor terminal and does not cancel handler execution.

**INV-10 — Request-id conflict blocks execution.** For one effective principal,
reuse of a request id with a different request fingerprint returns
`request_id_conflict` with HTTP 409. The gateway does not execute the second
request.

**INV-11 — Live duplicate blocks execution.** For one effective principal and
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
state object that contains the prior terminal class, status, stable code, and
body SHA-256. The response contains no prior success result or domain response
body. The gateway does not execute the handler.

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

**INV-16 — Existing responses retain their domain shape.** A success, domain
refusal, or decision-pending response retains its source-baseline status and JSON
body. The guard adds only `x-tightbeam-request-id`.

**INV-17 — Unknown stays unknown.** An unmatched execution failure commits cause
`{phase: <observed phase>, component: unknown, kind: unknown}` plus a sanitized
structural envelope. The public response contains the cause descriptor and omits
the structural envelope.

**INV-18 — Domain audit remains authoritative.** Existing EventLog and domain
rows retain their source-baseline writes. The terminal journal adds transport
and execution-lifecycle evidence; it does not replace or synthesize a domain
event.

## Architecture

### A. Outer guard and execution boundary

`POST /agent/dispatch` enters a route-specific outer guard before the current
Router logic. The guard acquires or validates a request id, then runs the current
version/authentication/body/verb/identity/target pipeline in a monitored worker.
The outer process retains the connection. The worker returns a tagged value. Its
monitor exit is data to the outer process.

The guard does not start a general wall-clock timer. A five-second
`GenServer.call` timeout remains the dependency's timeout and arrives as an exit
term. An alive handler without such an event remains outside this version.

After authorization, the worker asks the terminal journal to accept the request.
The journal keys a row by `(effective principal, request id)`. The worker may call
Rules and Dispatch only after the journal confirms the committed acceptance.

The outer guard encodes one complete body, asks the journal to commit its terminal
descriptor, and then calls the single response-started boundary. A normal
terminal body is not stored; its SHA-256 and classification are stored. A generic
terminal body is deterministic from its descriptor and can be reconstructed.

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
| Caught dependency or execution timeout | `gateway_execution_failed` | 504 | `gateway request failed` |
| Caught execution exit, exception, or unknown failure | `gateway_execution_failed` | 500 | `gateway request failed` |
| Terminal journal unavailable before acceptance | `gateway_terminal_store_unavailable` | 503 | `gateway terminal store unavailable` |
| Same current-boot request still executing | `gateway_request_in_progress` | 409 | `gateway request is in progress` |
| Older-boot accepted request lacks a terminal descriptor | `gateway_outcome_unknown` | 500 | `gateway request outcome is unknown` |
| Same request has a normal terminal descriptor and body is not replayed | `request_already_terminal` | 409 | `gateway request is already terminal` |
| Same principal and request id have a different fingerprint | `request_id_conflict` | 409 | `request id conflicts with accepted request` |

`gateway_execution_failed` carries a cause object. A terminal-store failure uses
cause `{phase: accept, component: terminal_store, kind: exit}` or kind `timeout`
when the caught term proves a timeout. `gateway_outcome_unknown` carries the
restart cause in INV-12.

The three state responses carry this exact object in place of `cause`:

```json
{
  "state": {
    "terminalClass": "normal_success",
    "status": 200,
    "code": "ok",
    "bodySha256": "6f1ed002ab5595859014ebf0951522d9a699b6af5078c2d496eb29a620630f13"
  }
}
```

For `gateway_request_in_progress`, each state value is JSON `null`. For
`request_id_conflict`, each state value is JSON `null`. For
`request_already_terminal`, the values come from the committed terminal
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
5. A timeout exit from the monitored Router execution process before a handler
   starts maps to `{<phase>, router, timeout}` unless a dependency rule matched.
6. A non-timeout exit from that Router process before a handler starts maps to
   `{<phase>, router, exit}`.
7. An exception raised after Dispatch selects a handler maps to
   `{dispatch, handler, exception}`.
8. A timeout exit after Dispatch selects a handler maps to
   `{dispatch, handler, timeout}` unless a dependency rule matched.
9. A non-timeout exit after Dispatch selects a handler maps to
   `{dispatch, handler, exit}`.
10. Boot recovery maps to `{recover, gateway, restart}`.
11. A remaining term maps to `{<phase>, unknown, unknown}`.

The phase is the guard's stage at the instant it observes the term. The
classifier writes the sanitized structural envelope only to the journal's
restricted diagnostic field. It does not copy that field into the HTTP body or
CLI output.

### E. Terminal journal record

One journal row stores:

- effective-principal kind and canonical id;
- request id and request fingerprint;
- boot epoch;
- route, verb, target kind, and canonical target id;
- accepted timestamp;
- state `accepted` or `terminal`;
- terminal timestamp, class, HTTP status, stable code, and body SHA-256 when
  terminal;
- cause phase, component, and kind when a cause exists;
- one generated failure correlation id and sanitized structural envelope when an
  execution failure exists.

The journal stores the target id already authorized for the effective principal.
It stores no caller-supplied display label or free-form origin. The process owner
serializes acceptance and terminalization. A unique constraint on effective
principal plus request id makes duplicate resolution deterministic.

The terminal journal uses a SQLite file distinct from the files owned by
`Tightbeam.DB` and EventLog. Its supervision child starts before
`Tightbeam.DB`, `Tightbeam.Credentials`, Router, and the HTTP listener. A restart
of one of those later children leaves the journal owner and file available. The
HTTP listener starts after older-epoch reconciliation completes.

### F. Duplicate and recovery state machine

For the same effective principal and request id:

```text
no row + same request       -> commit accepted -> execute once
accepted + current epoch    -> gateway_request_in_progress
accepted + older epoch      -> gateway_outcome_unknown
terminal + generic failure  -> reconstruct the committed generic response
terminal + normal response  -> request_already_terminal
row + different fingerprint -> request_id_conflict
```

Authentication and authorization run before this lookup. A caller using another
principal follows that principal's independent key space and cannot inspect the
first principal's state. The existing authorization path may reject it before
the journal lookup.

The CLI recovery request is byte-identical at the fingerprint inputs. It may
cause first execution only when the first attempt failed before acceptance and
left no row. A current execution continues after client disconnect. A prior-boot
row becomes unknown because the generic gateway cannot prove whether the domain
effect committed. Neither case starts a duplicate execution.

### G. CLI rendering

The CLI renders the example database timeout as one line:

```text
gateway_execution_failed: gateway request failed (request req_018f3c42-15e7-4db8-a8f0-6aa09385b32f; phase dispatch; component database; kind timeout)
```

A state error uses the same prefix and request-id placement, followed by the
state fields in the order `terminalClass`, `status`, `code`, `bodySha256`.
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
terminalization. It contains request id, effective-principal kind and id, route,
verb, target kind and id, boot epoch, accepted and terminal timestamps, terminal
class, HTTP status, stable code, body SHA-256, failure correlation id, and cause
descriptor. It omits fields that the terminal descriptor does not have.

One structured log event named `gateway_terminal_send_failed` records a send
failure after terminalization. It carries request id, failure correlation id, and
the committed terminal code. It does not change the committed terminal state.

The existing EventLog continues to record domain dispatch outcomes under its
source-baseline rules. Operators correlate the terminal journal, structured log,
and domain event by request id or failure correlation id. The public wire reveals
the request id and safe cause descriptor, not the sanitized structural envelope.

## Acceptance

Each acceptance case runs against a fresh file-backed gateway and the built
release CLI from the candidate implementation. Tests invoke real Router,
Dispatch, and domain handler paths. A deterministic test coordination seam may
pause a named process after acceptance; a handwritten replacement handler may
not stand in for the named producer path.

**AC-01 — Journal-bound transcript database timeout (INV-01, INV-02, INV-05,
INV-06, INV-07, INV-09, INV-15).**

Given an authenticated transcript request for a seeded session and limit 500,
and given the test seam pauses `Tightbeam.DB` after the terminal journal commits
acceptance but before the real transcript handler calls it,
when the built CLI sends the request and the real `GenServer.call` reaches its
five-second timeout,
then the gateway returns HTTP 504 with header `x-tightbeam-request-id`, code
`gateway_execution_failed`, and cause
`{phase: dispatch, component: database, kind: timeout}`,
and the CLI output contains that code and request id and contains no bare `EOF
while parsing a value`.

The fixture captures the real exit shape and asserts that the classifier matched
it. This case is the deterministic descendant of the independently journal-bound
`s_ac72dc3a --limit 500` evidence. It does not use `s_7269208c --limit 50` as a
database fixture.

**AC-02 — Distinct Credentials timeout (INV-02, INV-05, INV-06, INV-07,
INV-09).**

Given a seeded spawn request whose real handler calls `Tightbeam.Credentials`,
and given the test seam pauses `Tightbeam.Credentials` after acceptance,
when the built CLI sends the spawn request and the real `GenServer.call` reaches
its five-second timeout,
then the gateway returns HTTP 504 with code `gateway_execution_failed` and cause
`{phase: dispatch, component: credentials, kind: timeout}`,
and the terminal journal contains one accepted row and one terminal descriptor
for that request id.

This case uses the producer-specific Credentials evidence from closed
`wi_890c351c-45c7-4224-a885-0202bf0788e2` to select the component. It does not
change that closed work item.

**AC-03 — Unmatched failure remains unknown (INV-07, INV-17).**

Given the monitored execution process receives a deterministic unmatched exit
after acceptance,
when the guard classifies the caught term,
then the HTTP response is 500 with cause
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

**AC-05 — Acceptance-store failure prevents effects (INV-02).**

Given the terminal journal is unavailable before acceptance,
when an otherwise valid authenticated dispatch request reaches the acceptance
step,
then the gateway returns HTTP 503 with code
`gateway_terminal_store_unavailable`,
and the domain handler invocation count remains zero.

**AC-06 — Same-id fingerprint conflict (INV-10).**

Given principal A has an accepted row for request id R and body fingerprint F1,
when principal A sends request id R with body fingerprint F2,
then the gateway returns HTTP 409 with code `request_id_conflict`,
and the domain handler invocation count for R remains one.

**AC-07 — Disconnect before send (INV-09, INV-11, INV-13).**

Given the journal accepted a request and the client closes its socket while the
real handler executes,
when the handler returns a normal success,
then the journal commits one `normal_success` descriptor before the send attempt,
and a later request from the same principal with the same request id and
fingerprint returns HTTP 409 `request_already_terminal` with the committed status,
code, and body SHA-256 and does not invoke the handler again.

**AC-08 — Live duplicate (INV-11).**

Given a current-epoch accepted request is paused inside its real handler,
when the same principal sends the same request id and fingerprint,
then the duplicate returns HTTP 409 `gateway_request_in_progress`,
and the handler invocation count remains one.

**AC-09 — Crash gap and restart (INV-12).**

Given a real handler's domain transaction commits and the test process kills the
gateway after that commit but before terminal journal terminalization,
when the gateway restarts and reconciles old boot epochs,
then the row becomes HTTP 500 `gateway_outcome_unknown` with cause
`{phase: recover, component: gateway, kind: restart}`,
and a same-principal retry with the same request id and fingerprint returns that
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

Given pinned fixtures for one success, one domain refusal, and one
decision-pending result from the source baseline,
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

**AC-16 — Router exit (INV-05, INV-07).**

Given the monitored Router worker exits deterministically after ingress
correlation during the authentication phase and before handler selection,
when the outer guard observes the monitor event,
then it returns HTTP 500 `gateway_execution_failed` with cause
`{phase: authenticate, component: router, kind: exit}`,
and it emits one response-started call.

**AC-17 — Handler timeout and exit (INV-05, INV-07).**

Given Dispatch selected a test-registered production-shape handler and the handler
exits with a reason that proves timeout,
when the outer guard observes the monitored execution exit,
then it returns HTTP 504 `gateway_execution_failed` with cause
`{phase: dispatch, component: handler, kind: timeout}`.

Given the same handler exits with a deterministic non-timeout reason,
when the outer guard observes the monitored execution exit,
then it returns HTTP 500 `gateway_execution_failed` with cause
`{phase: dispatch, component: handler, kind: exit}`.

**AC-18 — Router timeout (INV-05, INV-07).**

Given the monitored Router worker exits with a reason that proves timeout during
the authentication phase and before handler selection,
when the outer guard observes the monitor event,
then it returns HTTP 504 `gateway_execution_failed` with cause
`{phase: authenticate, component: router, kind: timeout}`.

**AC-19 — Handler exception (INV-05, INV-07, INV-08).**

Given Dispatch selected a test-registered production-shape handler and the
handler raises an exception whose message contains a canary string,
when the outer guard receives the classified result,
then it returns HTTP 500 `gateway_execution_failed` with cause
`{phase: dispatch, component: handler, kind: exception}`,
and the public body and structured log omit the canary string.

## Open Questions

None. The document remains DRAFT until one independent spec reviewer clears its
requirements, architecture, evidence boundaries, and acceptance traceability.
The producer must amend this canonical file before resolving a defect found by
that review. The work item receives a path and content-hash binding only after the
review clears the amended text.
