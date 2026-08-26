# DB and gateway failure observability — v1

Status: **PROPOSAL — independent review required before work-item binding or
implementation.** This proposal is untargeted. It is based on Tightbeam product
`origin/main` commit `7a70a2f616363074514237b5bee48ba67c52e2ea`, Tightbeam
specs `origin/main` commit `bc916b29adf2566d6ee2a939d52774eaf6ad9445`, and recon
artifact `art_671a2c8d` at SHA-256
`4dff7f9b2a0a7dd63d47892ecd3d38e9cb21f0652b57740268facf563e585452`.
The recon completion receipt is
`att_b5ca2572-5d31-47a9-945a-3ac36963efa3`; its NO/high-confidence verdict is
`att_c38d0d33-2165-4767-bb3d-1a28c238ee6d`.

This spec extends `observability-v1.md` and
`job-trace-observability-v1.md`. It does not replace either contract.
`observability-v1.md` remains the authority for model-grain queries and thin
doorbells. `job-trace-observability-v1.md` remains the authority for work-item
trace. This spec owns only DB-call, HTTP-request, CLI-transport, and listener
failure evidence.

## Goal

Give an operator enough privacy-safe evidence to distinguish these outcomes
before anyone changes a timeout:

1. a call waited in the `Tightbeam.DB` mailbox;
2. SQLite returned `BUSY` or `LOCKED` while acquiring or retaining a lock;
3. SQLite execution or a transaction callback occupied the DB owner;
4. the DB caller reached its own `GenServer.call` deadline; and
5. the CLI failed before dispatch because DNS, connection refusal, transport
   loss, or a listener restart made the gateway unavailable.

The same correlation must reach the DB evidence, a structured gateway error,
and the CLI error when those surfaces exist. A stranger session must be able to
classify a reproduced failure from the records without reading SQL, parameters,
credentials, prompts, or application data.

## Non-Goals

- This spec does not change the current 5,000 ms DB-caller budget.
- This spec does not change the current 5,000 ms SQLite busy budget.
- This spec does not add retries, cancel a queued DB message, suppress a late
  write, or decide whether a timed-out mutation succeeded.
- This spec does not add a DB pool, a second application database connection,
  backpressure, admission control, circuit breaking, or a gateway-availability
  manager.
- This spec does not change authentication, authorization, identity
  resolution, verb permissions, or idempotency rules.
- This spec does not log successful SQLite busy-wait duration. The pinned
  Exqlite public API exposes `:busy` and terminal error reasons, but not the
  time spent in a successful busy-handler wait. V1 makes no proxy claim from
  elapsed time.
- This spec does not add a remote diagnostics query or a dashboard. The bounded
  host-local records and the CLI error are the MVP read surfaces.
- This spec does not instrument ACP, WebSocket message delivery, model calls,
  or application work that does not cross the DB or HTTP listener seams.
- This spec does not select a release line, host, deployment, or target.

The design chooses **ADD**. Deleting the DB or HTTP control plane would delete
core product behavior. Accepting the current failure would preserve conflated
causes and secret-bearing crash terms. The added mechanism only records events
that the caller, DB owner, SQLite, router, listener, and transport already
observe.

## Terms

- **Transport attempt**: one CLI attempt to send one HTTP request. A DNS-only
  retry is a second transport attempt with a new request ID.
- **Request ID**: a privacy-safe correlation value for one transport attempt.
  It is not an idempotency key and never authorizes an action.
- **DB call ID**: a privacy-safe correlation value for one message sent to
  `Tightbeam.DB`. Several DB call IDs can share one request ID.
- **DB operation**: a stable name from the closed DB-operation registry. It
  names the product action, such as `transcript.page`; it is never derived from
  SQL text.
- **Transport operation**: a stable name from the closed CLI-operation
  registry. It names the invoked command or dispatch verb without arguments or
  payload values.
- **HTTP operation**: a stable name from the closed route-operation registry.
  A DB timeout uses the matching DB operation. Another terminal response uses
  its route action without path parameters or request values.
- **Operation name**: any DB, transport, or HTTP operation above. Each is an
  ASCII registry value of at most 96 bytes and matches
  `[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)+`.
- **Effect kind**: `read`, `write`, or `schema`. It states whether a caller
  timeout can leave a mutation outcome unknown.
- **Caller budget**: the explicit duration that the caller waits for the DB
  reply. `timeout_source=otp_db_call` owns the current 5,000 ms budget.
- **SQLite busy budget**: the duration that SQLite can wait on a lock.
  `timeout_source=sqlite_busy` owns the current 5,000 ms budget.
- **Timeout source**: the component whose configured budget elapsed. The
  closed values are `otp_db_call`, `sqlite_busy`, `cli_connect`,
  `cli_request`, and `none`. `none` requires a null budget and means the
  observed failure was not a configured deadline expiry.
- **Queue time**: monotonic time from immediately before the `GenServer.call`
  invocation that sends the DB message to the DB owner's entry into the
  matching call handler.
- **Execute time**: monotonic time spent inside SQLite prepare, bind, step,
  execute, begin, commit, rollback, and integrity-check calls for one DB call.
  It includes an unmeasured successful SQLite busy wait if one occurred.
- **Callback time**: monotonic time spent in a transaction callback, including
  its execute time. It is null for `query` and `execute` calls.
- **Callback SQL time**: the subset of execute time measured inside a
  transaction callback. It is null outside a transaction.
- **Total time**: monotonic time from immediately before the matching
  `GenServer.call` invocation to the DB owner's terminal result.
- **Caller-abandoned call**: a DB call for which the caller recorded that its
  budget elapsed before it received a reply. The message can still enter or
  finish in the DB owner under existing behavior. The DB owner does not infer
  this state.
- **DB result class**: one of `ok`, `sqlite_busy`, `sqlite_locked`,
  `sqlite_error`, or `callback_error`. `sqlite_busy` and
  `sqlite_locked` require an exact matching result from the pinned Exqlite
  adapter; arbitrary error-text matching is forbidden.
- **Gateway accepted**: a CLI fact with values `true`, `false`, or `unknown`.
  `false` means the transport proved that no connection reached the gateway.
  `true` means the CLI received a correlated HTTP response. `unknown` means the
  connection started but no correlated response completed. This term says
  nothing about mutation success.
- **Effect state**: `none`, `known`, or `unknown`. Reads use `none`. A response
  can use `known` only when the domain result is known. A timed-out write uses
  `unknown` until existing domain evidence proves an outcome.
- **Response state**: `not_started`, `started`, or `complete`, set by the router
  at the actual response-send seam.
- **Listener generation**: one fresh, opaque ID for one successfully bound
  Bandit listener instance. A later instance never reuses it.
- **Diagnostic record**: one structured JSON object written to a DB-independent
  bounded sink. It is evidence only. No product decision reads it.
- **Principal reference**: a bounded correlation value, never a credential.
  Its exact forms are `user:<existing-user-id>`,
  `session:<existing-session-key>`, `process:<registered-process-name>`, or
  `internal:<registered-component-name>`. The complete value is at most 256
  UTF-8 bytes and contains no control characters. It is null while unresolved.
- **Cause code**: a value from the closed failure vocabulary in R5. It names an
  observed event, not an inferred root cause.

## Assumptions

1. Product commit `7a70a2f` keeps one SQLite connection inside one
   `Tightbeam.DB` GenServer. `query`, `execute`, `transaction`, and
   `foreign_key_rebuild` serialize through that process.
2. The current DB calls inherit `GenServer.call/2`'s 5,000 ms deadline. SQLite
   separately receives `PRAGMA busy_timeout=5000`.
3. A transaction callback runs inside the DB owner. Non-SQL callback work can
   therefore block later DB messages.
4. The root supervisor uses `rest_for_one`. A crash in a child that starts
   before Bandit can stop and restart the listener.
5. BEAM monotonic time is comparable across processes in one VM incarnation.
   Durable records store durations and wall-clock occurrence time, not raw
   monotonic timestamps.
6. The pinned Exqlite step API returns `:busy` for `SQLITE_BUSY`. Other SQLite
   failures return an error reason rather than a numeric code. The adapter can
   normalize exact pinned outcomes without logging the raw reason, changing the
   busy timeout, or installing a new busy handler.
7. A disk-full, read-only-filesystem, or process-kill event can prevent any
   local diagnostic write. R6 makes that loss conspicuous without changing the
   original request result.
8. A bounded byte store cannot promise a time duration. Retention is expressed
   in bytes and record count, not days.

## Invariants

1. **Observe before tuning.** Implementation and review keep both 5,000 ms
   values unchanged. A later timeout change needs separate live authority and
   evidence from this contract.
2. **The evidence path does not use the failing DB.** No diagnostic sink,
   formatter, rotation path, listener event, or CLI receipt calls
   `Tightbeam.DB`.
3. **Observed events decide classes.** The system names SQLite busy or locked
   only from the adapter's exact pinned outcomes. It names queue time only from
   both mailbox boundary timestamps. It never uses an elapsed threshold to
   invent either cause.
4. **A timeout does not cancel an effect.** A DB message keeps current mailbox
   and mutation semantics after caller abandonment. The DB owner records its
   terminal result when it eventually observes one.
5. **Correlation is not idempotency.** Request IDs and DB call IDs do not
   deduplicate, authorize, replay, or suppress work.
6. **One mutation seam per diagnostic store.** The gateway has one serialized
   append-and-wrap seam. The CLI has one locked append-and-wrap seam. Other
   code emits typed records through those seams and never writes the files
   directly.
7. **Protected content never enters diagnostics.** Diagnostic records, new
   HTTP and CLI errors, file names, and the sanitized DB-timeout crash term
   contain no SQL text, SQL parameters, tokens, prompts, message content,
   artifact paths, credential paths, HTTP bodies, or arbitrary exception text.
8. **Labels have bounded cardinality.** Operation, event, effect, principal
   kind, timeout source, cause, result class, response state, and action come
   from closed registries. Request IDs, DB call IDs, listener generations, and
   principal references are fields, never metric labels or file-name fragments.
9. **Diagnostics do not decide or block.** A sink failure does not change the
   domain result, restart a child, reject a request, delay a reply past its
   existing budget, or select a recovery action.
10. **Authorization remains unchanged.** The request-ID header and response
    fields add no authority. Host-local diagnostic files remain readable only
    by the account that owns the Tightbeam base directory.
11. **Response state has one writer.** The router's response-send seam owns the
    `not_started -> started -> complete` transition. No failure path can emit
    two terminal response states for one request ID.
12. **Existing history authorities remain separate.** Diagnostic files are not
    work-item state, conversation truth, dispatch audit, or lifecycle truth.
    Product behavior never reads them.

## Architecture

### R1 — Correlate transport attempts and DB calls

The CLI creates a fresh request ID before each network attempt. The value is
`req_` followed by the 22-character unpadded URL-safe base64 encoding of 128
random bits. The suffix matches `[A-Za-z0-9_-]{22}`.
The CLI sends it as `x-tightbeam-request-id`. The router validates this exact
shape, generates a value when an older client omits the header, and echoes it
in `x-tightbeam-request-id` on each HTTP response.

The router accepts exactly one valid request-ID header. A missing header gets a
generated ID. A malformed or repeated header returns the standard 400 error
envelope with `code=invalid_request_id` and a fresh gateway-generated request
ID; authentication and DB work do not run.

Each DB client wrapper creates a DB call ID with the same suffix encoding and
prefix `dbc_`. It carries the current request ID. An internal caller creates an
`int_` request ID with the same suffix encoding at its subsystem entry and
reuses it for the DB calls caused by that entry.

One request-context owner provides the only bind/restore seam. It binds the ID
and principal to the caller process for the duration of one request or internal
entry and restores the prior context in an unconditional cleanup step. A
spawned process receives no implicit context; its caller must pass a copy
explicitly. The DB envelope copies, rather than references, that context.

The router binds request context immediately after validating or generating the
header. It adds the resolved request principal when identity resolution
succeeds. Before that point, `principal_kind` is `unknown` and `principal_ref`
is null. Resolved references use only the exact principal-reference forms in
Terms. No diagnostic record copies an authentication token to fill this gap.

Acceptance A1: Given one CLI read and one internal wake scan, when each makes
two DB calls, then the read has one `req_` ID, the scan has one `int_` ID, each
DB call has a distinct `dbc_` ID, and no ID changes authorization or
idempotency behavior. Given a missing, malformed, and repeated request-ID
header, the router respectively generates an ID, returns `invalid_request_id`,
and returns `invalid_request_id` without running authentication.

### R2 — Make the DB call envelope typed

Each production DB call carries one envelope with these exact fields:

| Field | Type | Rule |
|---|---|---|
| `schema_version` | literal `db-call-v1` | fixed |
| `request_id` | request ID | required |
| `db_call_id` | DB call ID | fresh for each call |
| `operation` | registered string | required |
| `effect_kind` | `read` / `write` / `schema` | required |
| `principal_kind` | `user` / `session` / `process` / `internal` / `unknown` | required |
| `principal_ref` | safe string or null | null until resolved |
| `timeout_source` | `otp_db_call` | required in v1 |
| `budget_ms` | positive integer | 5,000 in v1 |
| `enqueued_monotonic_ms` | integer | set adjacent to `GenServer.call` invocation |

One closed registry owns every production DB operation name and its effect
kind. Names match `[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)+`. The affected call sites
use these exact entries:

- `transcript.page` (`read`);
- `assignment.files` (`read`);
- `auth.session_by_cli_token` (`read`);
- `wake.due_scan` (`read`);
- `wake.schedule` (`write`);
- `pointer.append` (`write`);
- `turn.reply_attention.read` (`read`);
- `turn.reply_attention.write` (`write`);
- `schema.ensure` (`schema`); and
- `db.query`, `db.execute`, `db.transaction`, and
  `db.foreign_key_rebuild` for remaining unchanged call sites at the baseline
  commit.

The implementation evidence includes a generated census that maps every
production DB call site to exactly one registry entry. A new call site must add
an action-specific registry entry; the four `db.*` migration entries do not
authorize new call sites.

Production code cannot call an untyped `query`, `execute`, `transaction`, or
`foreign_key_rebuild` entry. Test-local helpers can use a named
`test.fixture` operation. The build adds a source check that rejects the old
untyped arities under `lib/`.

Acceptance A2: Given the product source, when the source check scans `lib/`,
then each DB call uses a registered operation and effect kind, and changing one
call to an old untyped arity fails the check.

### R3 — Record both sides of the DB mailbox

The DB client and DB owner use the envelope's monotonic send time. The owner
records its handler-entry time, SQLite spans, callback span, terminal time, and
terminal result. Immediately before it replies, the owner submits one
`db_server_completed` record with:

- `observed_at_ms`, `request_id`, `db_call_id`, `operation`, `effect_kind`,
  `principal_kind`, and `principal_ref`;
- `queue_ms`, `execute_ms`, `callback_ms`, `callback_sql_ms`,
  `callback_outside_sql_ms`, and `total_ms`;
- `timeout_source=otp_db_call` and the resolved caller `budget_ms`;
- `sqlite_timeout_source=sqlite_busy` and the resolved
  `sqlite_busy_budget_ms`;
- `result_class` and nullable `cause`; and
- no claim about whether the caller still waits.

The owner returns the timing metadata with the internal reply. The public DB
functions remove that metadata and preserve their current success values. On
receipt, the caller submits one `db_caller_completed` record with its own
elapsed time, envelope fields, and `cause=null`.

If the caller reaches its deadline, it submits `db_call_abandoned` with its
elapsed time, envelope fields, `cause=db_caller_timeout`, and null owner-only
fields. The wrapper then raises one sanitized `Tightbeam.DB.Timeout` exception.
The owner still submits
`db_server_completed` if it later enters or finishes the message. The joined
presence of `db_call_abandoned` establishes caller abandonment; the server
record never guesses it from reply success or process liveness.

Each duration is a non-negative integer in milliseconds. Null means the named
boundary was not observed. Zero is a measured duration and never means
unknown.

For a transaction, `execute_ms` is the sum of every measured SQLite span,
including begin, callback SQL, commit, and rollback. `callback_ms` covers the
whole callback. `callback_sql_ms` sums only SQLite spans inside the callback.
`callback_outside_sql_ms` is `callback_ms - callback_sql_ms`. The implementation
subtracts native-unit spans before rounding each published duration once. A
negative difference is an instrumentation failure; it is not clamped or
published as a measurement. The record does not infer what the callback did.

Acceptance A3: Given a first DB call held after server entry and a second call
queued behind it, when the second caller expires, then its abandoned record has
null server fields, its later server-completed record has positive `queue_ms`,
and the first call reports its own execute and callback spans without borrowing
the second call's queue time. Releasing owner completion and caller deadline in
both orders never makes the server record claim caller abandonment.

### R4 — Preserve SQLite lock evidence

One adapter normalizes exact outcomes from the pinned Exqlite API. `:busy` maps
to `sqlite_busy`. A closed full-value table captured from real pinned fixtures
maps the observed `SQLITE_LOCKED` reasons to `sqlite_locked`. Every other error
maps to `sqlite_error`. Diagnostic records retain only the normalized class;
they never retain the raw reason or match an arbitrary substring. A successful
result uses `ok` even if execute time was long.

V1 keeps the current `PRAGMA busy_timeout=5000`. It does not install or replace
an Exqlite busy handler. It does not name successful busy-wait time. A future
busy-handler measurement needs a reviewed amendment because the pinned
dependency states that `PRAGMA busy_timeout` replaces its custom handler.

Acceptance A4: Given a real second SQLite connection holding a write lock and
a test-only busy budget of 50 ms, when the product connection attempts a
conflicting write, then the terminal record carries `sqlite_busy`, measured
execute time, and no SQL, parameter value, or raw SQLite reason. Given a real
active-statement table lock that makes the pinned dependency return
`SQLITE_LOCKED`, the terminal record carries `sqlite_locked`. Given an
unrelated SQLite error whose text contains `locked`, the adapter returns
`sqlite_error`.

### R5 — Use closed event and cause vocabularies

The diagnostic event registry contains:

- `db_server_completed`, `db_caller_completed`, and `db_call_abandoned`;
- `http_response_terminal`;
- `listener_started`, `listener_stopped`, and
  `listener_predecessor_stop_unknown`;
- `cli_transport_failed`.

Every gateway record carries `schema_version=db-gateway-v1`, one event from
that registry, and `actor=process:tightbeam`. Every CLI record carries
`schema_version=cli-transport-v1`, `event=cli_transport_failed`, and the same
actor.

The v1 cause registry contains:

- `db_caller_timeout`, `sqlite_busy`,
  `sqlite_locked`, `sqlite_error`, and `transaction_callback_error`;
- `dns_failed`, `connect_refused`, `connect_timeout`, `request_timeout`,
  `connection_reset`, and `transport_failed`;
- `listener_child_exit`, `listener_gateway_exit`, and
  `listener_stop_unobserved`; and
- `diagnostic_sink_unavailable`.

The timeout-source registry is the closed vocabulary in Terms. Every deadline
failure stores the source and the resolved configured budget. A non-deadline
failure stores `timeout_source=none` and `budget_ms=null`.

The CLI error-code registry is `db_timeout`, `gateway_unavailable`, and
`gateway_transport_uncertain`. The first comes only from a correlated gateway
response. The other two come from the observed transport classes in R7.

The system can conclude `db_mailbox_queue_overrun` only when the owner's entry
time is after the caller deadline. It can conclude `db_execute_overrun` only
when the owner entered by the deadline and finished after it. These are derived
views over the two records, not stored root-cause claims. A record with
insufficient boundaries remains `db_caller_timeout`.

Every failure record carries `cause`, `actor=process:tightbeam`, and the
request principal fields. An unresolved principal stays visibly unknown. A
sink failure can produce only the safe stderr fallback in R6; it is not falsely
registered as a durable diagnostic event.

Acceptance A5: Given one queue overrun, one execute overrun, and one caller
timeout whose server record is absent, when a deterministic classifier reads
the records, then it returns the three distinct results above and never calls
the absent-record case a queue or execute overrun.

### R6 — Write to bounded DB-independent sinks

The gateway installs one structured wrap-log handler at
`<base_dir>/diagnostics/db-gateway-v1.log`. The handler owns four 16 MiB
segments, including the active segment, for a 64 MiB maximum. Each segment also
holds at most 4,096 records, so the sink retains at most 16,384 records. It
creates the directory with mode `0700` and files with mode `0600`. Each JSON
record is at most 4,096 bytes and one line. The formatter accepts only the
closed fields in this spec.

The CLI writes transport-failure receipts through one locked append-and-wrap
seam at `<base_dir>/diagnostics/cli-transport-v1.log`. It owns two 4 MiB
segments, including the active segment, for an 8 MiB maximum. Each segment also
holds at most 1,024 records, so the sink retains at most 2,048 records. It uses
the same directory and file modes. One transport attempt produces at most one
receipt.

Neither sink calls the application DB. Rotation occurs before an append would
cross either a byte or record-count bound. Concurrent CLI processes attempt
append and rotation through the same non-waiting host-local lock. Lock
contention uses the CLI fallback below instead of delaying the error. A crash
can leave one truncated last line; the reader skips only that line and
preserves earlier lines.

Gateway producers submit records to one bounded, non-blocking ingress owned by
the wrap-log writer. The ingress holds at most 8,192 formatted records. A full
ingress drops the new diagnostic record, increments
`diagnostics.droppedRecords`, and sets `diagnostics.lastDropAt`; it does not
block the observed operation. Submission returns only `accepted` or `dropped`.
The writer drains accepted records through the single append-and-wrap seam. A
process or VM death can lose accepted but unflushed records. The health fields
make capacity loss observable without claiming that an absent record proves no
event occurred.

The gateway sink stores the caller-side and server-side records that its
ingress accepted for each DB call. The CLI sink stores at most one record per
transport attempt. Neither uses request IDs, call IDs, listener generations,
or principal references as metric labels. V1 adds no metrics exporter.

If the gateway sink write fails, the gateway recorder emits one privacy-safe
`diagnostic_sink_unavailable` line to the gateway's existing stderr and
increments a gateway-owned in-memory failure count. `/version` adds
`diagnostics.writeFailures`, `diagnostics.lastFailureAt`,
`diagnostics.droppedRecords`, and `diagnostics.lastDropAt` from gateway-owned
state. If the CLI sink write fails or its lock is held, that CLI process appends
`diagnosticReceipt=unavailable` to its safe error line; it does not change the
gateway count. Neither fallback contains the rejected record or raw error. The
original domain or transport result does not change.

Acceptance A6: Given enough fixed-size safe records to cross each bound, when
rotation completes, then the gateway files total no more than 64 MiB, the CLI
files total no more than 8 MiB, record counts stay within 16,384 and 2,048,
permissions are exact, retained lines parse, and no diagnostic write invoked
`Tightbeam.DB`. Given an ingress held full, submission returns without waiting
for the writer and the drop fields increase. Given independent injected
failures in the gateway and CLI sinks, only the gateway failure changes its
write-failure fields, and only the CLI failure adds
`diagnosticReceipt=unavailable`.

### R7 — Return sanitized, actionable errors

`Tightbeam.DB` catches the raw `GenServer.call` timeout at its client wrapper.
It submits `db_call_abandoned` and raises `Tightbeam.DB.Timeout` with only the
typed envelope, elapsed time, and effect state. It never carries the original
GenServer message, SQL, parameters, callback, or exception inspection.

One router error boundary covers the whole HTTP request, including CLI-token
authentication before Dispatch. If `Tightbeam.DB.Timeout` reaches that boundary
while the response is still `not_started`, it returns HTTP 503 with this
additive error shape:

```json
{
  "error": {
    "code": "db_timeout",
    "message": "database operation timed out",
    "requestId": "req_...",
    "operation": "transcript.page",
    "elapsedMs": 5001,
    "budgetMs": 5000,
    "timeoutSource": "otp_db_call",
    "gatewayAccepted": true,
    "effectState": "none",
    "action": "retry_safe"
  }
}
```

The `action` registry is `retry_safe`, `retry_same_idempotency_key`, and
`do_not_retry_report`. A timed-out read uses `retry_safe`. A timed-out write
with an existing idempotency contract uses `retry_same_idempotency_key`. A
timed-out write without that contract uses `do_not_retry_report`.

The CLI prints one line with the same code and fields. It keeps its current
nonzero exit behavior. DNS failure, connection refusal, and a connect deadline
print `code=gateway_unavailable`,
`timeoutSource=none`, `budgetMs=null`, `gatewayAccepted=false`,
`effectState=none`, and `action=retry_safe`, except that a connect deadline
reports `timeoutSource=cli_connect` and its resolved client budget. A
post-connect request deadline reports `code=gateway_transport_uncertain` and
`timeoutSource=cli_request`. Each reports its resolved current client budget.
A reset or EOF after connection reports `code=gateway_transport_uncertain`,
`timeoutSource=none`, and a null budget. A post-connect failure before a
correlated response completes prints `gatewayAccepted=unknown`,
`effectState=none` for reads, and `effectState=unknown` for writes. Its action
uses the same effect/idempotency mapping as a DB timeout. The CLI performs no
automatic retry for these uncertain failures. The message tells the operator
to report the request ID when the action is `do_not_retry_report`; it does not
name an unbuilt command.

Each `cli_transport_failed` record contains exactly `schema_version`,
`observed_at_ms`, `request_id`, `code`, `operation`, `effect_kind`, nullable
`listener_generation`, `cause`, `timeout_source`, `budget_ms`, `elapsed_ms`,
`gateway_accepted`, `effect_state`, `action`, `principal_kind=unknown`, and
`principal_ref=null`. `operation` comes from the closed transport-operation
registry; it never includes command arguments. The CLI never derives a
resolved principal from a credential.

The existing one-time DNS retry remains because DNS failure proves that no
request reached the gateway. Each DNS attempt gets a distinct request ID and
receipt. No other automatic retry is added.

Acceptance A7: Given a token, prompt, SQL value, and path containing four
distinct sentinels, when each DB and transport failure runs, then the
diagnostic logs, crash reports, HTTP bodies, headers, and CLI stderr contain
none of the sentinels and do contain the safe request ID, operation, elapsed
time, budget, source, gateway-accepted value, effect state, and action.

For the pre-Dispatch case: Given CLI-token authentication whose
`auth.session_by_cli_token` DB call reaches its caller budget before Dispatch,
when the response has not started, then the router returns the same sanitized
503 contract, the CLI prints its actionable form, and neither surface contains
the token or raw GenServer message.

### R8 — Correlate listener lifecycle without claiming an unseen stop

The gateway diagnostic recorder and one listener-lifecycle owner start before
Wakes and Bandit in the production `rest_for_one` child order. The lifecycle
owner holds the current listener generation and monitor; it submits lifecycle
records to the recorder. Both therefore survive ordinary failures of Wakes,
later children, and Bandit. Neither makes a domain decision or reads the
application DB.

Each successfully bound Bandit instance receives a fresh `lgen_` prefix plus
the same 22-character suffix encoding as request IDs. The lifecycle owner
submits `listener_started` only after the socket binds. It submits
`listener_stopped` when its monitor observes that instance stop, with the exact
generation and an observed cause code. Listener records use
`operation=gateway.listener`, `timeout_source=none`, `budget_ms=null`,
`principal_kind=internal`, and
`principal_ref=internal:listener_lifecycle`. They carry `schema_version`,
`observed_at_ms`, event, current generation, nullable prior generation, and
nullable cause.

If the listener disappears before observation or the recorder rejects its stop
record, the next successful listener submits
`listener_predecessor_stop_unknown` before submitting its own start record. It
names the prior generation only when the same lifecycle owner retained it. A whole-VM
restart or a crash of that owner loses predecessor memory; the next
start does not emit a predecessor record or invent a prior generation. It never
invents a crash cause.

Every HTTP response carries `x-tightbeam-listener-generation`. The router
includes the same generation in its request terminal record. A CLI
pre-connect refusal has a null listener generation and cannot claim that one
listener handled it.

Acceptance A8: Given Bandit on port `0` under the production `rest_for_one`
order, when Wakes crashes, then the same lifecycle owner survives,
one listener generation stops or gets an unknown-stop record, a different
generation starts, a request accepted by each instance names the matching
generation, and a refusal during the gap names none. Given a whole-VM restart,
the new owner emits no predecessor claim for the old generation.

### R9 — Make response, timeout, and restart races single-winner

The router records response state at the response-send seam. A failure before
send produces one structured error when the connection remains writable. A
failure after send starts records `started` and lets the transport outcome
stand; it does not attempt a second response. Successful send records
`complete`.

For each terminal transition that the router observes, it submits exactly one
`http_response_terminal` record with `request_id`, `listener_generation`,
`operation`, principal fields, `response_state`, nullable HTTP status, and
nullable cause. An error response that finishes is `complete` with its status
and cause. A post-start transport loss is `started` with a null status and its
observed cause. A process or VM death can prevent this record; a later listener
record does not fabricate it.

A DB caller timeout and a DB owner completion are independent observations.
They can both exist for one DB call ID. The records never convert that pair
into a retry, rollback, or success claim.

Request ID reuse has no effect on domain idempotency. The CLI reuses only an
existing verb idempotency key when `action=retry_same_idempotency_key`. A
connection error never causes the CLI to replay a mutation automatically.

Listener and diagnostic records survive a listener restart because their
owners start before the restartable child set and write outside the
application DB. A whole-VM restart keeps flushed records and starts a new
generation without an in-memory predecessor claim.

Acceptance A9: Given an injected barrier immediately before response send and
a mutation whose DB caller reaches its deadline, when response failure,
late DB completion, and listener restart are released in each permutation,
then the domain mutation occurs no more than current idempotency permits, the
router records one terminal response state, the CLI performs no forbidden
retry, and all observed records join by request and DB call IDs.

### R10 — Preserve compatibility and authority

An older CLI can omit the request header. The new gateway generates and echoes
an ID; the older CLI can ignore the additive header and error fields. A new CLI
talking to an older gateway keeps its local request ID, accepts a missing echo,
leaves listener generation null, and preserves the older gateway's generic
failure presentation. Existing 2xx bodies and DB public success returns remain
byte-compatible.

The new header does not affect bearer authentication or session-token
authentication. Authorization still runs at its current point. Diagnostics add
no HTTP, WebSocket, or agent-dispatch read verb. The filesystem owner is the
only reader.

The spec adds no application DB table and no schema migration. It adds no
operating pattern for agents; the substrate manual needs no amendment.

Acceptance A10: Given old/new CLI and gateway pairs, when each pair performs
one successful read, one authorization refusal, and one DB timeout, then
success and authorization outcomes match the old contract, a new gateway
returns the safe 503 timeout contract, an older component degrades to its
existing generic failure without an automatic retry, additive fields are
ignored safely, and no principal gains a new read or mutation capability.

### R11 — Provide deterministic and reality-based test seams

Production timing reads a monotonic clock. Tests can inject the clock, ID
generators, test-only caller and SQLite budgets, mailbox barriers, SQLite
execution barriers, response-send barriers, sink writer, and listener port.
Production exposes no delay or failure-control API, and production budget
resolution still returns 5,000 ms for both DB deadlines.

Mailbox tests use process barriers, not sleeps. Lock tests use a real second
SQLite connection and the real pinned Exqlite version. Listener tests use the
production supervisor order and an ephemeral port. HTTP and CLI error fixtures
come from captured real responses. A hand-written ideal fixture does not
satisfy acceptance.

Acceptance A11: Given the captured fixtures and deterministic barriers, when a
test changes one cause code, timing boundary, protected-content filter, request
ID, response state, or listener generation, then the corresponding test fails.

### Component and proof map

| Requirements | Expected implementation seam | Required proof home |
|---|---|---|
| R1–R5 | `lib/tightbeam/db.ex` plus one operation registry and one diagnostic record module | focused DB observability tests |
| R6 | one gateway bounded-ingress wrap-log writer and one Rust CLI wrap-log writer | rotation, concurrency, permission, drop, and sink-failure tests |
| R7, R9–R10 | `lib/tightbeam/dispatch.ex`, `lib/tightbeam/wire/router.ex`, `cli/src/dispatch.rs` | router tests, CLI tests, captured envelopes |
| R8 | gateway recorder and listener-lifecycle children before Wakes/Bandit in `lib/tightbeam/gateway.ex` | listener-generation restart test |
| R11 | test support only | real SQLite and ephemeral-listener fixtures |

## Acceptance

The implementation passes only when A1–A11 pass and the evidence bundle
contains:

1. the exact product commit and spec SHA-256 under test;
2. baseline and after counts from both CI halves that the implementation
   touches;
3. the real SQLite lock fixture and its captured diagnostic lines;
4. the real HTTP 503 and CLI stderr fixtures;
5. the listener restart trace with both generation IDs;
6. a sentinel scan over every retained diagnostic, new HTTP and CLI error, and
   sanitized DB-timeout crash output;
7. proof that both production timeout values remain 5,000 ms;
8. proof that no new application DB table, authorization path, automatic
   retry, or late-effect cancellation exists; and
9. an independent code review against the exact implementation commit.

Traceability is two-way: R1–R11 each name their acceptance example and proof
seam above. A changed implementation file or test with no R1–R11 reference is
out of scope. A requirement without its named proof blocks completion.

The implementation may begin only after one independent spec review returns
`reviewed-clean` on the exact proposal hash, the canonical spec absorbs any
ruling, and the work item binds that cleared file hash.

## Open Questions

1. **BLOCKING for implementation — target selection.** The release line, host,
   and integration target remain unset by directive. Mike owns that choice
   after independent spec review. Review and spec amendment can proceed while
   the target stays unset; implementation cannot.
2. **NON-BLOCKING — successful SQLite busy-wait duration.** V1 reports the
   normalized terminal busy or locked class and total execute time. A later
   revision can propose a busy-handler duration seam only after it proves that
   the change preserves current SQLite behavior.
3. **NON-BLOCKING — remote diagnostics query.** V1 keeps evidence host-local.
   Live use can show whether a read-only, authorization-preserving query is
   worth adding. No implementation work waits on that product decision.
