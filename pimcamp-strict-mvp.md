# Pimcamp strict MVP

Status: review candidate for work item
`wi_133b36ba-3078-4dc6-be9a-14b582facbfd`.

Authority: parent assignment
`asg_b16007ea-7f9d-4698-944d-f3173ad4f2d8`. This specification uses the
work item and parent assignment as its source. It does not use the temporary
discussion file.

## Goal

Deliver the smallest useful Pimcamp capability boundary for a local,
single-account Linux/Omarchy mail setup.

Pimcamp gives graphical clients, agents, and scripts one versioned structured
contract for these seven capabilities:

1. list inbox messages;
2. read one selected message;
3. create a new composition;
4. create a reply composition;
5. send either composition kind;
6. file one message as junk; and
7. subscribe to normalized new-mail notifications.

Pimcamp is the stable client contract. Himalaya supplies the first mail
operations adapter. Mirador supplies the first mail observation adapter. A
replacement for either adapter must preserve the Pimcamp contract.

The MVP succeeds when a client completes the seven capabilities through
Pimcamp, without receiving lower-adapter credentials, command syntax, raw
output, raw events, or backend-specific identifiers.

## Spirit

### Problem

A local graphical client, agent, or script should not have to understand
Himalaya commands, Mirador event shapes, or mail-backend credentials. Direct
coupling makes the presentation hard to replace, gives agents broader
authority than their task needs, and lets observation data drift into mail
truth.

### Outcomes

Pimcamp provides one runnable local cross-process seam for exactly seven
public capabilities: list, read, compose, reply, send, junk, and normalized
new-mail subscription. The seam carries structured requests, results, errors,
and a live event stream. A new UI, agent integration, or script targets that
seam and retrieves authoritative mail through Pimcamp after an event.

The exact capability grant and the private mutation receipt store are internal
safety mechanisms. They do not add an eighth public product capability.

### Quality stance

- Correctness and agent safety matter strongly. Pimcamp makes permission
  denial, ambiguous mutation outcome, and lower-adapter failure visible.
- Linux/Omarchy compatibility matters. The cross-process seam uses an ordinary
  local executable and standard input/output instead of new transport
  infrastructure.
- Local responsiveness matters, but the MVP invents no numeric latency target.
  A deployment-owned bound stops finite lower-adapter waiting, and the real
  smoke has an external-delivery bound. Neither bound infers a backend outcome.
- Failures and diagnostics remain content-safe. They expose normalized reason
  codes without mail content, credentials, or raw lower-adapter material.
- Himalaya and Mirador remain replaceable. Their formats do not define the
  client contract.
- Presentation remains replaceable. The MVP promises no full UI and no broader
  platform support.

The Non-Goals below complete this Spirit boundary. Independent spirit review
must reject a public surface beyond the seven named capabilities.

## Non-Goals

- A full graphical or terminal mail UI.
- Neverest integration.
- Local mail synchronization.
- A notmuch dependency.
- A Maildir dependency.
- A local search index.
- A generalized policy engine.
- An event broker.
- An event replay ledger.
- Elaborate permission profiles, role inheritance, policy expressions, or
  wildcard grants.
- A credential issuance, rotation, or grant-management API. Deployment uses
  its existing private secret and configuration path.
- Multiple-account selection, routing, or policy.
- D-Bus, a Unix-domain socket, or MCP.
- HTTP, WebSocket, gRPC, a message queue, a network listener, or another
  speculative transport.
- Search, archive, delete, arbitrary move, flag mutation, folder browsing,
  draft synchronization, attachment upload, attachment download, reply-all,
  forwarding, scheduled send, or bulk actions.
- A guarantee that a notification names a message or that a newly observed
  message is immediately queryable.
- Exactly-once delivery by an external mail server. Pimcamp guarantees the
  mutation-attempt behavior defined below.
- A client-visible cache that becomes a source of mail truth.
- A new operating or agent-guidance pattern. This specification teaches none.

## Terms

- **Pimcamp boundary**: the versioned structured interface exposed by the one
  local `pimcamp` executable over standard input and output. Clients call this
  boundary, not the lower adapters.
- **Client**: a graphical program, agent host, or script that invokes the
  `pimcamp` executable.
- **Client credential**: a deployment-issued high-entropy bearer value sent
  inside the standard-input request. Pimcamp maps its hash to one client
  identity and one exact capability grant. Pimcamp does not accept identity or
  grant fields in a request.
- **Client session**: the authenticated context Pimcamp creates for one finite
  invocation or one live subscription after it resolves the client
  credential.
- **Capability grant**: a set drawn from `list`, `read`, `compose`, `reply`,
  `send`, `junk`, and `subscribe_new_mail`. The empty set is valid. No wildcard
  value exists. Deployment configuration owns the credential-to-grant map;
  Pimcamp exposes no grant-management operation.
- **Configured account**: the one mail account selected by deployment
  configuration. The public contract has no account selector in this MVP.
- **Adapter wait bound**: a positive deployment-owned duration that creates
  one absolute deadline for the lower-adapter phases of a finite invocation.
  Client `SIGTERM` creates a fresh teardown deadline of the same duration. The
  bound stops waiting and never infers a backend outcome.
- **Inbox**: the configured account's configured incoming mailbox.
- **Message reference**: an opaque Pimcamp string returned by `list`. A client
  may return it to Pimcamp in `read`, `reply`, or `junk`. The client must not
  parse it or treat it as durable across an account or adapter configuration
  change.
- **Composition**: a structured, immutable Pimcamp value with `kind` equal to
  `new` or `reply`. A reply composition also carries an opaque source message
  reference.
- **Mutation ID**: a caller-generated UUID used once for one `send` or `junk`
  request. Pimcamp binds it to the client identity, operation, and exact
  request digest.
- **Mutation receipt**: Pimcamp's durable local record of a mutation ID,
  request digest, attempt state, and result. It is safety state, not mail
  state, an event ledger, or a search index.
- **Authoritative mail data**: data returned by the configured mail operations
  adapter in response to a current Pimcamp query. Notification payloads and
  client state are not authoritative mail data.
- **Mail operations adapter**: a replaceable internal port for list, read,
  send, junk-capability discovery, spam reporting, and move-to-junk. Himalaya
  is the first implementation.
- **Mail observation adapter**: a replaceable internal port that reports
  possible new mail while a subscription is live. Mirador is the first
  implementation.
- **Normalized new-mail event**: the Pimcamp record
  `{contract_version, kind, mailbox, observed_at}` where
  `contract_version = "pimcamp.v1"`, `kind = "new_mail"`, and
  `mailbox = "inbox"`. `observed_at` is the UTC RFC 3339 time when Pimcamp
  accepted the observation. The event is a hint to query Pimcamp.
- **Strongest available junk mechanism**: `report_spam` when the operations
  adapter positively reports that capability; otherwise `move_to_junk` when
  the adapter positively reports a configured junk mailbox; otherwise no
  supported junk mechanism.

## Assumptions

1. Deployment configures one account, one inbox, any available junk mailbox,
   and one adapter wait bound before Pimcamp starts.
2. Deployment supplies a read-only map from client-credential hashes to stable
   client identities and exact capability grants. Clients receive their
   credential through an existing private secret-delivery path.
3. Himalaya can serve the six required mail-operation calls for the configured
   account, or return a failure that its adapter can normalize.
4. Mirador can expose a live observation source for possible new mail, or
   return a failure that its adapter can normalize.
5. Lower adapters may emit duplicate, delayed, malformed, or incomplete data.
6. A mail backend can accept a send and lose the response. Pimcamp therefore
   cannot infer external delivery success from silence.
7. A dedicated test account and a test recipient are available for the
   release-gating real-adapter smoke. The smoke may skip in ordinary local
   unit runs when credentials are absent; release evidence may not replace it
   with fabricated responses.
8. The product repository will choose its language and module layout. This
   specification defines observable boundaries, not source-file names.

## Invariants

**I-01 — Sole stable boundary.** Client code depends on `pimcamp.v1` records,
operation names, and normalized errors. Adapter commands, output fields, event
fields, and credentials remain internal.

**I-02 — Replaceable adapters.** The Himalaya and Mirador implementations
depend inward on Pimcamp-owned ports. The public contract contains no
Himalaya or Mirador type, version, command, exit code, or field name.

**I-03 — Query authority.** Each `list`, `read`, and reply-source lookup asks
the current mail operations adapter. Pimcamp does not answer those requests
from a notification or a client-owned copy.

**I-04 — Observation is not truth.** A normalized new-mail event contains
only the four fields in the term above. It contains no message reference,
sender, recipient, subject, body, count, backend cursor, or lower-adapter
payload. A client retrieves mail through `list` and `read` after it receives
the hint.

**I-05 — Narrow permission.** A session can invoke only the named operations
in its immutable grant. Pimcamp returns `permission_denied` before calling an
adapter or reserving a mutation receipt for a denied request. A grant for one
operation covers that operation's internal adapter calls without granting the
client another public operation or returning that operation's data. For
example, a `reply` grant permits the source lookup but does not permit `read`.

**I-06 — One mutation seam per effect.** `send` is the sole client operation
that submits mail. `junk` is the sole client operation that reports spam or
moves a message to junk. The mutation receipt store is the sole writer of
Pimcamp's mutation safety state.

**I-07 — Check and act stay bound.** The session grant is immutable. For an
allowed `send` or `junk` request, Pimcamp validates the request and durably
reserves its mutation ID before one adapter attempt. Pimcamp does not call the
adapter when reservation fails.

**I-08 — Ambiguity fails loudly.** If Pimcamp cannot prove whether an adapter
accepted a mutation, it records and returns `outcome_unknown`. A repeat with
the same mutation ID does not call the adapter again.

**I-09 — No implicit mutation.** `list`, `read`, `compose`, `reply`, and
`subscribe_new_mail` do not send mail, report spam, move mail, or change
message flags.

**I-10 — Content-free diagnostics.** Ordinary logs and errors may include a
client identity, operation, mutation ID, duration, result code, and adapter
class. They omit addresses, subjects, body content, client credentials,
backend credentials, raw adapter output, and raw observation payloads.

## Architecture

### Public contract

Pimcamp exposes one cross-process interface named `pimcamp.v1` through one
local executable named `pimcamp`. It uses UTF-8 JSON on standard input and
standard output. This process/stdio seam is ordinary operating-system
plumbing, not a listener, broker, or transport service.

For `list`, `read`, `compose`, `reply`, `send`, and `junk`, the client runs
`pimcamp <operation>`. The process reads exactly one RequestEnvelope from
standard input. It writes exactly one SuccessEnvelope or Error as one JSON
line to standard output, then exits. A success exits with code 0. A normalized
Error exits with code 1. Standard error carries only the content-free
diagnostics allowed by I-10.

For `subscribe_new_mail`, the client runs `pimcamp subscribe_new_mail`. The
process reads one RequestEnvelope and opens the observation adapter. After the
adapter confirms that the live subscription is open, Pimcamp writes one
SuccessEnvelope whose `result` is `{status: "subscribed"}`. It then writes one
normalized event per JSON line while the subscription is live. On a normalized
subscription failure it writes one Error line and exits with code 1. On client
`SIGTERM`, it closes the observation adapter, writes no synthetic event, and
exits with code 0.

The executable accepts no other product operation. Command-line arguments do
not carry a client credential, mail content, account selector, grant, or
lower-adapter option. An unknown subcommand emits one `invalid_request` Error
line and exits with code 1.

The common structured values are:

```text
RequestEnvelope = {
  contract_version: "pimcamp.v1",
  client_credential: string,
  input: object
}

SuccessEnvelope = {
  contract_version: "pimcamp.v1",
  result: object
}

Address = {
  name: string | null,
  address: string
}

MessageSummary = {
  message_ref: string,
  from: [Address],
  subject: string,
  received_at: RFC3339 UTC string | null,
  unread: boolean
}

Message = {
  message_ref: string,
  from: [Address],
  to: [Address],
  cc: [Address],
  subject: string,
  sent_at: RFC3339 UTC string | null,
  body_parts: [{media_type: "text/plain" | "text/html", content_utf8: string}]
}

Composition = {
  kind: "new" | "reply",
  to: [Address],
  cc: [Address],
  bcc: [Address],
  subject: string,
  body_text: string,
  reply_to_message_ref: string | null
}

Error = {
  contract_version: "pimcamp.v1",
  code: "invalid_request" | "permission_denied" | "not_found" |
        "unsupported" | "backend_unavailable" | "conflict" |
        "outcome_unknown",
  retryable: boolean,
  message: string
}
```

The seven operation inputs are closed JSON objects:

```text
list.input = {
  limit: integer,
  cursor?: string
}

read.input = {
  message_ref: string
}

compose.input = {
  to: [Address],
  cc: [Address],
  bcc: [Address],
  subject: string,
  body_text: string
}

reply.input = {
  message_ref: string,
  body_text: string
}

send.input = {
  composition: Composition,
  mutation_id: UUID string
}

junk.input = {
  message_ref: string,
  mutation_id: UUID string
}

subscribe_new_mail.input = {}
```

The RequestEnvelope and each nested input value accept only the fields shown
in their schemas. Pimcamp returns `invalid_request` for an unknown field, a
duplicate object-member name at any nesting level, a value of the wrong JSON
type, a missing required input or envelope field other than
`client_credential`, or a second JSON value after the envelope. R-00 defines
the non-revealing result for a missing `client_credential`. JSON whitespace
may follow the one envelope before end-of-file. The question mark above
designates the only optional input field.

The error `message` describes the normalized failure without raw lower-adapter
data. `retryable = true` only for `backend_unavailable`. It is false for the
other six codes. A client needs a human decision before it attempts a mutation
again after `outcome_unknown`. For a mutation, `retryable = true` means the
adapter proved that it made no external attempt; the client uses a fresh
mutation ID for a later attempt. Reusing the failed mutation ID returns its
recorded result.

**R-00 — Envelope and authorization.** Pimcamp returns `invalid_request` for
an unsupported `contract_version`, malformed JSON, or an envelope or input
that does not match the closed schema for the selected operation. Pimcamp
returns `permission_denied` for a missing credential, an unknown credential,
or a credential without the selected operation so the response does not
reveal whether a credential exists. Pimcamp hashes the credential, resolves
client identity and grant from deployment configuration, and performs the
I-05 check before an operation calls an adapter. A request cannot carry client
identity, grant, adapter selection, or account selection.

### Operations

**R-01 — `list`.** The request requires `limit` from 1 through 100 and accepts
one optional opaque `cursor`. Pimcamp queries the configured inbox and returns
`{messages: [MessageSummary], next_cursor: string | null}`. The adapter defines
the snapshot boundary behind the cursor. Pimcamp treats the cursor as opaque
and returns `invalid_request` when the configured adapter rejects it. Pimcamp
preserves the adapter's authoritative mailbox order; the MVP defines no sort
parameter or chronology beyond the explicit `received_at` value.

**R-02 — `read`.** The request requires one message reference. Pimcamp queries
the operations adapter and returns one `Message`. Pimcamp returns `not_found`
when that reference no longer resolves.

**R-03 — `compose`.** The request requires `to`, `cc`, `bcc`, `subject`, and
`body_text`. At least one recipient must appear across `to`, `cc`, and `bcc`.
For a sendable Address, `address` contains exactly one `@` between non-empty
local and domain strings and contains no ASCII whitespace or control
character. Address names and subjects contain no carriage return or line feed.
Pimcamp validates these rules and returns a `new` Composition. This operation
has no mail-backend side effect.

**R-04 — `reply`.** The request requires one message reference and
`body_text`. Pimcamp reads the source through the operations adapter. It uses
the source `Reply-To` address when present; otherwise it uses the source
`From` address. It returns a `reply` Composition addressed to that one
recipient. It preserves a subject that begins with `Re:` after a
case-insensitive comparison; otherwise it prefixes `Re: `. It sets
`reply_to_message_ref` to the source reference. The send adapter uses the
source message's current threading headers when it submits the reply.

**R-05 — `send`.** The request requires one complete Composition and one
mutation ID. Pimcamp validates the composition, reserves the mutation receipt,
and makes one adapter submission attempt. A proved success returns
`{status: "sent", mutation_id}`. A proved rejection returns a normalized
error and a terminal receipt. An ambiguous attempt returns
`outcome_unknown` and an unknown receipt.

For a `reply` Composition, Pimcamp resolves `reply_to_message_ref` through the
operations adapter at send time. It passes the source's current threading
context to the send adapter and does not accept client-supplied threading
headers.

For the same client identity, operation, mutation ID, and request digest,
Pimcamp returns the recorded result without a second adapter attempt. Reuse of
that tuple with a different request digest returns `conflict` without an
adapter attempt.

**R-06 — `junk`.** The request requires one message reference and one mutation
ID. Pimcamp reserves the mutation receipt, asks the operations adapter which
junk mechanisms are positively available, and selects the strongest mechanism
by the fixed order in Terms. A success returns
`{status: "filed", mutation_id, mechanism: "report_spam" | "move_to_junk"}`.
No supported mechanism returns `unsupported`. Pimcamp does not substitute
delete or an arbitrary folder move.

The operations port reports `report_spam` as positively available only when a
successful call reports the message as spam and files it out of the configured
inbox. A successful `move_to_junk` call also files the message out of the
configured inbox. Pimcamp returns `status = "filed"` only after the selected
port call reports that postcondition. Pimcamp makes at most one junk mutation
call for a request and does not try a second mechanism after that call begins.

The same mutation-ID replay and conflict rules as `send` apply to `junk`.

**R-07 — `subscribe_new_mail`.** Pimcamp opens one live subscription through
the observation adapter. Pimcamp emits the subscribed SuccessEnvelope only
after the adapter confirms that the live subscription is open. For each
accepted Mirador new-mail observation it emits one normalized new-mail event.
An observation that predates the live subscription produces no replay.
Duplicate accepted observations may produce duplicate normalized events.
When the observation adapter stops or violates its contract, Pimcamp closes
the subscription with a normalized Error. When the client terminates the
subscription process with `SIGTERM`, Pimcamp closes the lower observation
subscription before it exits.

### Internal ports

**R-08 — Mail operations port.** The Pimcamp-owned port defines list-inbox,
read-message, send-composition, junk-capability discovery, report-spam, and
move-to-junk. The Himalaya adapter maps current real responses into this port.
Contract tests run against the port, not Himalaya's public syntax.

**R-09 — Mail observation port.** The Pimcamp-owned port reports only an
accepted possible-new-mail signal or a normalized adapter failure. The
Mirador adapter parses the real event source and discards lower-event payload
fields before it crosses the port.

**R-10 — Error normalization.** Each adapter maps its failures to the closed
Error code set. Unsupported backend behavior maps to `unsupported`; a missing
message maps to `not_found`; unavailable lower I/O maps to
`backend_unavailable`; an unprovable mutation result maps to
`outcome_unknown`.

Before the first lower-adapter phase of a finite invocation, Pimcamp applies
the configured adapter wait bound as one absolute deadline across adapter
open, call, and close. At the deadline, Pimcamp stops waiting and
force-terminates the lower adapter. If the adapter already proved a normalized
result before its cleanup hung, Pimcamp returns that proved result. Otherwise,
a query, capability probe, or subscription-open timeout returns
`backend_unavailable`. A mutation invocation that reaches the deadline before
its mutation adapter call begins records `failed` and returns
`backend_unavailable`. A mutation invocation that reaches the deadline after
its mutation adapter call begins records `unknown` and returns
`outcome_unknown`; termination does not prove that the backend rejected the
mutation. Silence on an already-open live subscription does not reach the
deadline because the event stream is not a finite invocation.

On client `SIGTERM`, Pimcamp starts a fresh teardown deadline from the adapter
wait bound and asks the observation adapter to close. If close does not finish
by that deadline, Pimcamp force-terminates the lower adapter. Pimcamp then
exits with code 0 and writes no event or Error for that client-requested
termination.

### Mutation receipt state

**R-11 — Durable receipts.** One private local receipt store records mutation
reservations before external I/O. A receipt key is
`(client_identity, operation, mutation_id)`. A receipt stores the request
digest, a `mutation_call_began` boolean, one state from `reserved`,
`succeeded`, `failed`, or `unknown`, and the normalized result when known. The
store survives a Pimcamp process restart.

Pimcamp computes the request digest as SHA-256 over the RFC 8785 canonical JSON
form of the validated operation input after removing `mutation_id`. The
receipt key already binds the client identity, operation, and mutation ID.
JSON member order and insignificant JSON whitespace therefore do not change
request equality.

Reservation atomically creates one `reserved` receipt, one exclusive live
claim for that receipt across Pimcamp processes, and one absolute claim
deadline equal to the finite invocation's adapter deadline. Only the claimant
may call the mutation adapter. The claimant atomically changes
`mutation_call_began` from false to true immediately before that call. Before
the deadline and while the live claim exists, only the claimant may change
`reserved` to `succeeded`, `failed`, or `unknown`. A second invocation with the
same key and a different digest returns `conflict`. A second invocation with
the same key and digest makes no adapter call. It waits for the claimant to
record a terminal state or for the claim deadline, then returns the recorded
result.

At the claim deadline, the receipt store atomically changes a still-`reserved`
receipt with `mutation_call_began = false` to `failed` with recorded
`backend_unavailable`. It changes a still-`reserved` receipt with
`mutation_call_began = true` to `unknown` with recorded `outcome_unknown`.
The claimant discards a lower result that arrives after either transition and
returns the recorded result. The live claim ends automatically when its
process exits. When the store finds a `reserved` receipt without its live claim
before the deadline, it applies the same boolean-based terminal transition
before returning the recorded result. No process may acquire a second mutation
claim for that receipt. `succeeded`, `failed`, and `unknown` are immutable
terminal states.

This mechanism is part of the MVP because accepting duplicate send attempts
would violate the agent-safety goal, while deleting `send` would remove a core
outcome. A named `outcome_unknown` value handles the failure that Pimcamp
cannot safely resolve.

### Fixtures and observability

**R-12 — Real response captures.** Parser fixtures for Himalaya responses and
Mirador events come from real, credentialed test-account captures. The
repository redacts addresses, subjects, bodies, message identifiers, paths,
and credentials while preserving syntax. A fabricated ideal response cannot
serve as the only parser fixture.

**R-13 — Evidence.** The test harness records boundary requests, normalized
result codes, adapter-call counts, selected junk mechanism, and event/query
order. It does not record mail content or raw lower-adapter data.

## Acceptance

Each acceptance case is a required pass/fail check. The parenthetical IDs map
the case back to the requirement or invariant it verifies.

**AC-00 — Runnable cross-process seam (R-00, I-01).** Given the built
`pimcamp` executable, fixture adapters, and a valid credential with the seven
grants, when a separate test process invokes each of the six finite
subcommands, sends its RequestEnvelope through standard input, and reads
standard output, then each invocation emits one parseable SuccessEnvelope or
normalized Error line and the specified exit code. When that test process
invokes `subscribe_new_mail`, the process emits a subscribed SuccessEnvelope
with `result = {status: "subscribed"}` after the fixture adapter records a live
open, then a fixture observation produces one parseable event line; `SIGTERM`
closes the lower subscription and exits with code 0. The test process imports
no Pimcamp module and communicates only through process arguments, pipes, exit
status, and the termination signal. The executable's dispatch table exposes
the seven named operations and no eighth product operation.

For each subcommand, the separate process sends the exact input object defined
in Public contract and receives the expected fixture result. Repeating one
case with an unknown input field, one with a duplicate `mutation_id` member,
and one with a second JSON value makes each process emit `invalid_request`,
exit with code 1, and retain zero adapter calls.

**AC-01 — Permission denial is pre-I/O (R-00, I-05, I-07).** Given a
deployment credential whose grant contains only `list` and spy adapters with
zero calls, when separate `pimcamp` invocations request `read`, `compose`,
`reply`, `send`, `junk`, and `subscribe_new_mail` once each, then each process
emits `permission_denied` and exits with code 1, both spies retain zero calls,
and the receipt store has no new row. An unknown credential produces the same
observable result. An envelope with no `client_credential` field also produces
that same result.

**AC-02 — Structured list with paging (R-01, I-01, I-03).** Given an
operations-port fixture with 101 inbox messages whose record shape is covered
by a real captured parser fixture and a session granted `list`,
when the client requests `limit = 100`, then Pimcamp returns 100 valid
MessageSummary records and a non-null opaque cursor. When the client submits
that cursor with `limit = 100`, then Pimcamp returns the remaining record and
`next_cursor = null`. Neither response contains a lower-adapter field or
identifier type.

**AC-03 — Read queries current truth (R-02, I-03).** Given a list result for
message reference `M` and an operations adapter whose body for `M` changes
before the next call, when the client reads `M`, then Pimcamp makes a new
adapter read and returns the changed body in a valid Message record. When the
adapter subsequently reports that `M` is absent, a second read returns
`not_found` rather than the prior body.

**AC-04 — New composition is pure (R-03, I-09).** Given a `compose` grant and
valid addresses for `to`, `cc`, and `bcc`, when the client composes subject
`Roadmap` with body `Ready`, then Pimcamp returns a `new` Composition with the
same semantic values and a null reply reference. The operations adapter and
receipt store retain zero calls and writes. Given no recipients, the operation
returns `invalid_request`.

**AC-05 — Reply composition uses authoritative source data (R-04, I-03).**
Given a session granted `reply` but not `read` and source message `M` with
`Reply-To: reply@example.test`,
`From: author@example.test`, and subject `Status`, when the client creates a
reply with body `Acknowledged`, then Pimcamp reads `M` through the operations
adapter and returns a `reply` Composition addressed only to
`reply@example.test`, with subject `Re: Status` and reply reference `M`.
Creating a reply to a source whose subject is `re: Status` does not add a
second prefix.

**AC-06 — New composition send is retry-safe (I-06, R-05, R-11).** Given a valid
`new` Composition, mutation ID `550e8400-e29b-41d4-a716-446655440000`, and a
send adapter that proves success, when the client sends it twice with the same
identity and mutation ID, then both calls return the same sent result and the
adapter records one submission. When the client reuses that mutation ID with
a changed body, Pimcamp returns `conflict` and the adapter still records one
submission.

Given two executable processes, the same identity, mutation ID, and
Composition, and an adapter that pauses its first submission, when both
processes send concurrently and the adapter then completes successfully
before the adapter deadline, both processes return the same sent
result and the adapter records one submission. Reordering JSON members in the
second process does not change the digest or the result.

**AC-07 — Reply send preserves threading and ambiguity (R-04, R-05, I-08).**
Given the reply Composition from AC-05 and a send adapter that accepts the
submission but loses its response, when the client sends it with a new
mutation ID, then the adapter receives one reply submission with the source's
threading context and Pimcamp returns `outcome_unknown`. Repeating the same
request after a Pimcamp restart returns `outcome_unknown` without another
adapter submission.

Given a send process whose adapter has observed one submission and paused
before Pimcamp records a terminal receipt, when that process is forcibly
terminated and another process repeats the same request, then Pimcamp changes
the abandoned `reserved` receipt with `mutation_call_began = true` to
`unknown`, returns `outcome_unknown`, and the adapter records exactly one
submission.

**AC-08 — Junk selects spam reporting first (I-06, R-06).** Given an adapter that
positively reports both `report_spam` and `move_to_junk`, when a granted client
files message `M` as junk, then Pimcamp calls `report_spam` once, does not call
`move_to_junk`, returns `mechanism = "report_spam"`, and the adapter's inbox
state no longer contains `M`.

**AC-09 — Junk fallback is bounded (R-06).** Given an adapter that reports
only `move_to_junk`, when a granted client files `M` as junk, then Pimcamp
calls that mechanism once and returns `mechanism = "move_to_junk"`. Given an
adapter that reports neither mechanism, the same operation returns
`unsupported` without a delete or move call. A same-ID retry after success
does not make a second adapter call. Given a move-to-junk adapter that accepts
the move but loses its response, the operation returns `outcome_unknown` and
a same-ID retry after restart does not make a second adapter call.

**AC-10 — Notification precedes authoritative query (R-07, I-04).** Given a
granted subscription process that has emitted its subscribed SuccessEnvelope,
a redacted real Mirador fixture event containing lower-specific message ID,
sender, and subject fields, and an operations-adapter spy, when Mirador emits
that event, then Pimcamp first emits exactly
`{contract_version: "pimcamp.v1", kind: "new_mail", mailbox: "inbox",
observed_at: <valid UTC RFC3339>}` and the operations spy retains zero calls.
When the client then calls `list`, Pimcamp calls the operations adapter and
returns its current summaries. No Mirador message field appears in the event
or list response. When the client sends `SIGTERM` to the subscription process,
the observation adapter records one close and the process exits with code 0.

**AC-11 — Adapters remain replaceable (I-01, I-02, R-08, R-09, R-10).** Given
one reference operations adapter, one replacement operations adapter, one
reference observation adapter, and one replacement observation adapter, when
the same boundary contract suite runs against each pair, then the client sees
the same record shapes, permission behavior, error codes, mutation replay
behavior, and normalized event shape. Adapter-specific spy evidence may
differ; client-visible values may differ only where the backing mailbox data
differs.

**AC-12 — Real single-account journey (R-00 through R-13).** Given a dedicated
test account configured for real Himalaya and Mirador adapters, a unique test
subject and body, a test recipient that automatically replies with the same
unique token, a deployment credential granted the seven capabilities, and an
explicit 120-second external-delivery wait bound, when a client uses only the
`pimcamp` executable and its standard-input/output contract to perform this
sequence:

1. start `subscribe_new_mail` and read its subscribed SuccessEnvelope;
2. compose and send the unique message;
3. receive a normalized new-mail event for the resulting incoming test mail;
4. page through `list` until it locates the message by its returned structured
   summary;
5. call `read` and verify the unique body from authoritative query data;
6. create and send a reply composition;
7. file the selected incoming message as junk; and
8. page through `list` again until `next_cursor = null`;

then each boundary result conforms to `pimcamp.v1`, the event arrives before
the post-event list request, the send and reply each have one adapter attempt,
the junk result names the strongest mechanism that the real backend reported,
and the final inbox list does not contain the filed message. The 120-second
bound only stops the external smoke; reaching it fails the smoke and does not
infer delivery outcome.

Release evidence includes the redacted real response captures, the exact test
command, adapter versions, the selected junk mechanism, and a content-free
event/query ordering trace.

**AC-13 — Diagnostics omit mail content (I-10, R-13).** Given unique sentinel
values in an address, subject, body, client credential, backend credential,
raw Himalaya output, and raw Mirador event, when the boundary completes one
successful query, one failed query, one successful mutation, one ambiguous
mutation, and one subscription failure, then a scan of ordinary logs and
returned Error records finds none of the sentinel values. The evidence still
names the operation, normalized result code, adapter class, mutation ID when
present, and event/query order.

**AC-14 — Finite lower I/O fails visibly (R-10, I-08).** Given the configured
adapter wait bound and a controllable adapter, when a `list` call never
returns, then Pimcamp force-terminates that adapter at the bound, emits
`backend_unavailable`, and exits with code 1. When a `send` adapter call begins
but never returns, Pimcamp force-terminates that adapter at the bound, records
`unknown`, emits `outcome_unknown`, and a same-ID retry makes no second adapter
call. When subscription open never returns, Pimcamp force-terminates that
adapter at the bound, emits `backend_unavailable`, and exits with code 1. When
a `list` adapter proves a result and then blocks during cleanup, Pimcamp
force-terminates that adapter at the bound, returns the proved result, and
exits with code 0.

**AC-15 — Subscription teardown is bounded (R-07, R-10).** Given a live
subscription whose observation adapter blocks during close, when the client
sends `SIGTERM`, then Pimcamp requests close, force-terminates the adapter when
the teardown deadline is reached, writes no additional standard-output
line, and exits with code 0. A content-safe diagnostic records that forced
termination occurred.

## Open Questions

1. **NON-BLOCKING — Credential/grant configuration format.** The repository's
   existing private configuration pattern is not named here. The builder uses
   that pattern when it exists. Otherwise it uses one owner-readable local
   file that maps a client-credential hash to one client identity and an array
   of the seven exact capability names. R-00 defines behavior; serialization
   syntax and path do not change the public seam.
2. **NON-BLOCKING — Receipt-store technology and location.** The repository's
   existing durable local-state pattern is not named here. The builder uses
   that pattern if one exists; otherwise it chooses one private local store
   with atomic reservation and restart durability. The schema in R-11 is
   normative. The storage engine and path are not.
3. **NON-BLOCKING — Exact Himalaya capability probe.** The available Himalaya
   version and account backend determine how the adapter proves
   `report_spam` or `move_to_junk`. The adapter may use only positively
   observed capability evidence. Absence maps to `unsupported`; it does not
   justify a guessed fallback.
4. **NON-BLOCKING — Mirador malformed-event recovery.** The first adapter
   closes the affected subscription with `backend_unavailable` after one
   malformed event. Reconnect policy belongs to the client. A later product
   decision can permit bounded skip-and-continue behavior after real captures
   show that it is needed.
5. **BLOCKING questions: none.** The four questions above have explicit MVP
   rulings and do not require a product decision before implementation or
   independent spec review.
