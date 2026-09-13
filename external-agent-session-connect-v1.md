# External-agent session connection v1

Status: FROZEN AMENDED PROTOCOL CANDIDATE for proportional independent
specification review. Spirit is approved, the public command spelling is
settled, and the integration line remains open under `dr_107b5cbc`.

Work item: `wi_684f7f8f-08eb-43f4-bdad-adfac6338426`.

This specification defines one persistent machine interface through which an
external agent sends prompts to one selected Tightbeam session and receives
that session's conversation and lifecycle changes without transcript polling.
It composes the ordinary wake write path, the canonical REST state reads, and
the native Event Firehose. It creates no parallel event, message, identity, or
authorization system.

This is the first live specification for this CLI connection. It supersedes no
live pattern. The archived `filtered-external-push-subscriptions-recon-v3.md`
and `focused-external-subscriptions-v1-draft.md` do not govern this feature;
canonical `event-firehose-v1.md` r6 already superseded their capability-token,
durable-event, replay, cursor, and retention designs.

## Spirit

The product intent is an ordinary Tightbeam conversation made available to a
machine peer through one long-running local CLI process. The peer chooses one
session it may already read and message, writes machine frames to stdin, and
receives live replies and relevant state changes on stdout. A satellite uses
its own installed CLI and the configured organization gateway; it does not
need or start a gateway on the satellite.

The product's state remains the durable model. Firehose notices provide
freshness, ordinary wake remains the write, and REST snapshots repair startup
and disconnect uncertainty. The stream is not history. Selected-session
authority comes only from the already discovered credential and its existing
authenticated principal. Existing identity flags choose attribution for the
ordinary outbound wake; they do not grant transcript, REST, or Firehose
visibility. The command does not silently turn an external participant into
Mike and does not revive the paused Visitor schema/security project.

Spirit and authority sources, frozen for this candidate on 2026-09-13 UTC:

- Mike-authored work item
  `wi_684f7f8f-08eb-43f4-bdad-adfac6338426`, as read 2026-09-13;
- product-owner assignment
  `asg_e3ec287b-14d6-41ad-91da-110573e91f95`, latest disposition
  `att_5b9f2770-42cf-4270-81a2-25555cb86d4a`, which approves this Spirit,
  settles the command spelling, and authorizes private non-integrating
  candidate development;
- external-agent orchestrator disposition
  `att_525d1d0b-0689-45b5-977e-479705ca1ab9`;
- external-agent orchestrator authority correction
  `s_1461da0a-6816-4a2a-9acd-8031377bf113`, which confirms that
  `--as-user` is attribution only and cannot authorize transcript or
  Firehose visibility;
- Visitor scope dispositions
  `att_86c98dbc-501e-44f1-a5a1-b7d7a01bd39a` and
  `att_a740faef-7d54-497a-ad2a-0ae299e878bd`;
- `tightbeam-specs` main
  `6b4ac660591c124369cfa8346c72494ff71cf5c1`, including canonical
  `event-firehose-v1.md` r6 at last-file revision
  `0c61770`, `rest-state-api-v1.md`, `rest-state-api-v1-wire-schema.md`,
  `transcript-verb-v1.md`, `session-tokens-v1.md`, and
  `cli-surface-v1.md`;
- Firehose Slice 2 source-line delivery
  `6c3392280ef7c2ae1fee780332ea00107f24d538` on `origin/0.1.9`,
  reviewed clean in `art_c892886e` and delivered in `art_18c62730`.
- authoritative served Gibson execution rule, Mike 2026-09-01, as projected
  to this spec writer on 2026-09-13: Gibson may compile and package only in
  an exact-tip throwaway worktree; product tests and gates run on Eezo or
  Racter, with the canonical Mix gate wrapper unmodified.

## Load-bearing terms

**Connection command** — the one long-running CLI process defined here. The
settled public spelling is
`tightbeam session-connect --session <sessionKey>`.

**Selected session** — the one exact full `sessionKey` passed by `--session`.
The command never changes this target and accepts no role, user, display-name,
or fallback target in its stdin protocol.

**Authorization principal** — the session or user principal authenticated
solely from the discovered existing gateway credential. It decides whether
the selected session and its rows are visible. An invocation identity flag is
never an input to this resolution.

**Attribution choice** — an allowed existing global `--as`, `--as-user`, or
`--as-process` invocation choice sent only through the ordinary wake write
path. It can change the recorded origin of an accepted send. It cannot change
the authorization principal or any REST, transcript, or Firehose result.

**Action origin** — the existing origin produced by the ordinary wake
principal/identity resolver from the fixed attribution choice and discovered
credential. It is recorded by the existing write path. It is not an
authorization grant and is not an stdin field.

**Connection generation** — a positive process-local integer. It starts at 1
and increments after every successful WebSocket re-authentication. It is not a
Firehose sequence, cursor, durable identifier, or resume token.

**Snapshot cycle** — a positive process-local integer carried as
`snapshotCycle`. It starts at 1 and increments whenever the command begins a
replacement snapshot, including a same-connection rebuild after a history
boundary change. At most one cycle is open at a time.

**Canonical event** — an unmodified Firehose `change` or `heartbeat` frame
nested in an `event` stdout frame. Its inner `seq`, `schemaVersion`, refs,
payload, and subscription identifier retain their Firehose meanings.

**Replacement snapshot** — a complete visible current set for the selected
session across the four resources in R8, reconciled with the finite Firehose
prefix captured for that cycle. A consumer stages snapshot items and pre-ready
events for one cycle and atomically replaces its prior set only at `ready`.
`snapshot.end` ends item transfer; it is not a publication point.

**Accepted history boundary** — the `clearedThroughSeq` shared by the two
equal session reads that bracket one transcript snapshot. Their shared
`rowVersion` starts the covered session version; higher same-boundary session
items in the validated prefix may advance it before emission. The emitted
session snapshot item's `rowVersion` is the cycle's final covered session
version. No accepted snapshot contains a transcript message whose `seq` is at
or below this boundary.

**Accepted send** — a `send` whose ordinary wake call returned a `wakeId`.
Acceptance means the gateway accepted the wake request. It does not promise a
turn, model response, or successful completion.

**Ambiguous send** — a send for which the command cannot determine whether the
gateway committed the wake. It is safe to retry only with the same supplied
idempotency key.

**Current-state gap** — inability to construct or maintain a complete
replacement snapshot for the selected session. It is different from omitted
intermediate transitions: reconnect recovery promises current durable state,
not replay of every Firehose notice.

## Assumptions

AS1. The selected delivery line provides the canonical Firehose change socket,
`message.created`, `wake.*`, `turn.*`, and `session.*` notices. A source and
acceptance check falsifies this assumption if any class cannot be subscribed
with an equal `sessionKey` filter.

AS2. The selected delivery line provides canonical REST detail for the session
and paginated collections for its transcript messages, wakes, and turns. A
real snapshot that cannot enumerate one complete authorized set falsifies this
assumption.

AS3. One existing CLI discovery operation returns one base URL and bearer by
the ordered chain: walk-up `.tightbeam-session`, then paired
`TIGHTBEAM_URL`/`TIGHTBEAM_TOKEN`, then the configured `gateway.json`.
Capturing different endpoint or bearer values across this command's WebSocket,
REST, and wake requests falsifies this assumption.

AS4. Ordinary wake accepts an idempotency key and returns its durable
`wakeId`. A same-key retry that creates a second wake, or a successful response
without a `wakeId`, falsifies this assumption.

AS5. The canonical message, wake, and turn projections retain the identifiers
listed in `rest-state-api-v1-wire-schema.md`: wake `wakeId`; turn `wakeId`,
`messageId`, and `seq`; transcript message `id`, `turnSeq`,
`replyToMessageId`, and `replyToClientMessageId`. A selected target line that
omits one required correlation field falsifies this assumption and blocks that
line's integration.

AS6. The selected delivery line can compose at least one CLI-discoverable
credential into the same authorization principal for ChangeSocket and REST.
Current source does not yet satisfy this for session CLI tokens: ChangeSocket
proves device-token authentication only. An organization CLI token has no
credential-bound user or session principal in v1. A real session-token
connection that cannot authenticate, or one whose Firehose and REST
principals differ, falsifies this assumption and blocks integration.

## Invariants

I1. There is one selected session, one credential-derived authorization
principal, one independent action-origin resolution, one gateway base URL,
and one bearer for a command process.

I2. Stdin and stdout are a versioned NDJSON protocol. Prompt content enters
only through stdin `send` frames. Every stdout byte belongs to exactly one
complete protocol frame followed by LF.

I3. Every send uses ordinary wake. Every live event uses native Firehose. Every
bootstrap or repair read uses canonical REST. No fourth state, message, or
delivery path exists.

I4. Authorization runs before selection or row disclosure. Firehose and REST
visibility use the authorization principal derived from the bearer alone;
wake attribution uses the independent action-origin resolver. A subscription
filter can only narrow an authorized view; an attribution choice cannot change
that view.

I5. The command emits no credential, raw auth frame, request header, storage
secret, or secret-bearing environment value on stdout or stderr.

I6. A reconnect creates a new subscription and replacement snapshot. It never
submits a Firehose sequence as a cursor and never asks the socket for replay.

I7. `requestId` is local correlation; `wakeId`, turn `messageId`, turn `seq`,
and message `replyToMessageId` remain Tightbeam correlation. The command does
not synthesize a durable conversation or reply identifier.

I8. The command never silently substitutes `user:mike` or another user for an
external caller. Any named origin is produced through the existing CLI
identity flags and ordinary resolver.

I9. A snapshot describes current durable visible state. It does not claim that
every intermediate state transition or observational event was delivered.

I10. Holding the bearer fixed while adding, removing, or changing `--as`,
`--as-user`, or `--as-process` cannot change whether a selected session is
visible or which rows and Firehose notices the command can receive.

I11. A snapshot candidate is never authoritative before `ready`. A history
boundary advance removes every transcript message at or below the new boundary
before the next presentation and starts a cursorless replacement snapshot.

## Normative protocol

### R1 — invocation and fixed selection

The `tightbeam session-connect` command SHALL require exactly one full
`--session <sessionKey>` selector and SHALL reject an omitted, empty,
display-name, prefix, role, user, or multiple selector before gateway I/O.

Acceptance example: given `s_abc` and another readable session, when the
caller invokes the command with `--session s_abc`, then every REST filter,
Firehose subscription, and wake target names only `s_abc`; `--session s_`
fails locally and sends no request.

The connection command SHALL accept the existing global `--as <role>`,
`--as-user <userId>`, and `--as-process <name>` forms as fixed attribution
choices for ordinary wake sends, subject to the existing CLI and wake
resolver's validation and refusals. It SHALL NOT send any attribution choice
to Firehose or REST or use one to resolve selected-session authority. An
omitted choice SHALL retain the ordinary wake path's existing default-origin
behavior.

The authorization principal SHALL follow this closed credential-only matrix:

| Discovered bearer | Credential-derived authorization principal | Attribution effect on visibility |
|---|---|---|
| active session token | that exact session | none |
| active device token | that device's user, including its existing admin bit | none |
| organization CLI token | none | none; no attribution choice may create one |
| unknown, revoked, or retired token | none | none |

Acceptance example: given one active session token and two otherwise identical
invocations, one with `--as-user` equal to the session owner and one without,
when both select that session, then their snapshot and Firehose visibility are
identical; an accepted wake may record different origins under the ordinary
wake resolver.

Acceptance example: given an organization CLI token plus `--as-user mike`,
when the command attempts to connect, then `--as-user` is not sent to
Firehose or REST, the token does not become Mike's authorization principal,
and the command emits no selected-session state.

### R2 — one discovery result

WHEN the command starts, it SHALL run the existing CLI discovery chain once
and SHALL use the resulting exact base URL and bearer for WebSocket auth, REST
snapshots, and wake dispatch for the life of the process.

Acceptance example: given a satellite workdir whose `.tightbeam-session`
names `https://gateway.example`, plus conflicting environment and local
fallback files, when the command connects, then all captured requests go to
`gateway.example` with the workdir credential and none go to localhost or the
fallback endpoints.

IF discovery fails or its selected file is malformed, the command SHALL emit
one fatal frame when stdout remains writable, write a credential-free human
diagnostic to stderr, make no gateway request, and exit 1.

Acceptance example: given malformed JSON in the winning
`.tightbeam-session`, when the command starts, then stdout contains one
`fatal` frame with code `discovery_failed`, stderr names the file without its
contents, and no network capture exists.

### R3 — existing credential and principal resolution

WHEN the Firehose authenticates this command, the gateway SHALL accept the
same existing credential selected by CLI discovery and SHALL resolve the
authorization principal from that credential alone under R1's closed matrix;
it SHALL NOT mint a ticket, capability, API key, visitor token, or
connection-only principal. The in-band auth request SHALL contain the
existing `type:"auth"` and `token` keys and SHALL NOT contain `as`, `asUser`,
`asProcess`, an origin, or another caller-declared principal.

WHEN the command requests a REST snapshot, it SHALL authenticate with that
same credential and SHALL NOT add `asUser` or another attribution field as an
authorization input. The Firehose and REST paths SHALL resolve the same
credential-derived principal before the command can emit `snapshot.begin` or
`ready`.

Acceptance example: given an active device bearer for user Alice, when Alice
selects one of her visible sessions, then ChangeSocket and REST independently
resolve Alice from the bearer and snapshot start follows; changing the
invocation from omitted attribution to `--as-user Bob` cannot expose Bob's
session or rows.

Acceptance example: given an active session CLI token, when ChangeSocket has
not yet composed existing session-token authentication, then the command does
not reach `snapshot.begin` or `ready`; completing S2 resolves the token to
that exact session without minting a Visitor credential.

IF the discovered credential has no credential-derived authorization
principal for both Firehose and REST, the command SHALL emit a fatal
`auth_failed`, expose no selected-session state, and exit 1. It SHALL NOT
fall back to a caller-declared user or a different credential.

Acceptance example: given an organization CLI token and any valid ordinary
wake attribution, when the token has no credential-bound read principal, then
the command fails authentication and emits no session key, display name,
message, wake, turn, or Firehose notice.

WHEN authentication resolves a session principal, the command SHALL expose
only sessions and rows granted to that session; WHEN it resolves a user
principal, it SHALL expose only sessions and rows granted to that user under
REST AU4.

Acceptance example: given two users' sessions and a non-admin user credential,
when the caller selects the other user's session, then the command returns the
same not-found/forbidden posture as canonical REST and emits no session key,
display name, message, wake, turn, or Firehose notice from that session.

### R4 — stdin framing

WHILE the command is running, it SHALL parse stdin as UTF-8 NDJSON, with one
JSON object per LF-terminated nonblank line; it SHALL ignore blank or
whitespace-only lines and SHALL reject a non-object, invalid UTF-8, invalid
JSON, unknown `type`, unsupported `protocolVersion`, unknown key, or invalid
field without dispatching a wake.

Acceptance example: given a valid send, a blank line, and then an object with
an extra `target` key, when the lines arrive, then the valid line is processed,
the blank line emits nothing, and the extra-key line emits one `input.error`
with no second wake.

The sole v1 input object SHALL be:

```json
{"type":"send","protocolVersion":1,"requestId":"req-17","content":"continue with the review","idempotencyKey":"external-run-9-message-17"}
```

`type`, `protocolVersion`, `requestId`, and `content` are required.
`idempotencyKey` is optional. `requestId`, `content`, and a present
`idempotencyKey` SHALL be nonempty strings. No other key is permitted.
`requestId` SHALL be unique among all previously parsed valid send frames in
the process.

Acceptance example: given two valid lines with `requestId:"req-17"`, when
the second is read, then it emits `input.error` code
`duplicate_request_id`, makes no gateway call for the second line, and leaves
the connection running.

### R5 — ordinary wake send

WHEN a valid send frame is read, the command SHALL issue exactly one ordinary
immediate wake to the selected session, carrying `content` byte-for-byte as
the prompt, the invocation's existing identity selection, and the optional
idempotency key; it SHALL NOT add a delayed wake, condition, assignment, work
item, reply record, or alternative message write.

Acceptance example: given content containing newlines, Unicode, and JSON
punctuation, when the gateway capture decodes the wake request, then the prompt
string equals the input string, the target equals the selected session, and
no other mutation request occurs.

WHEN the wake response returns a `wakeId`, the command SHALL emit
`send.accepted` before emitting any buffered event whose canonical refs or
payload carry that `wakeId`:

```json
{"type":"send.accepted","protocolVersion":1,"requestId":"req-17","wakeId":"w_123"}
```

Acceptance example: given Firehose fan-out that races ahead of the wake HTTP
response, when both reach the command, then stdout places the
`send.accepted` line before the first `event` line containing `w_123`.

IF the gateway refuses a send before commit, the command SHALL emit one
`send.rejected` frame with the input `requestId` and the gateway's safe public
error code and message, SHALL make no retry, and SHALL remain connected:

```json
{"type":"send.rejected","protocolVersion":1,"requestId":"req-17","code":"not_found","message":"target unavailable"}
```

Acceptance example: given a session retired after startup, when a send is
refused, then one correlated rejection appears, no automatic second request
occurs, and the subsequent retirement handling follows R11.

IF transport fails after the wake request may have reached the gateway but
before a response identifies the outcome, the command SHALL emit
`send.rejected` with code `outcome_unknown`, SHALL make no automatic retry,
and SHALL state in the public message that only the same `idempotencyKey` can
be retried safely.

Acceptance example: given a server that commits the wake and drops the HTTP
response, when the command loses the response, then it emits
`outcome_unknown`; resubmitting with the same key yields the original wake and
does not create a second one.

### R6 — selected-session subscription

WHEN authentication succeeds, the command SHALL open one Firehose
subscription whose filters are exactly the selected `sessionKey` and the class
prefixes `message.created`, `wake.`, `turn.`, and `session.`; it SHALL wait for
`subscription_ready` before any snapshot query.

Acceptance example: given changes to the selected session, another visible
session, and an unrelated work item after registration, when Firehose fans out,
then the command receives only the selected session's matching four class
families and receives no work-item event.

The subscribe request SHALL use canonical Firehose S1: protocol negotiation
appears only in the WebSocket upgrade query, and the `subscribe` frame SHALL
NOT contain `protocolVersion`. A delivery line that requires a version in the
subscribe frame is not composition-ready and SHALL be reconciled before this
command integrates there.

Acceptance example: given a protocol-1 connection, when the command subscribes,
then the captured frame contains only `type`, `subscriptionId`, and `filters`;
a server build that refuses it for missing `protocolVersion` fails the
dependency check rather than causing the CLI to send a noncanonical field.

The command SHALL preserve the accepted Firehose protocol negotiation,
in-band auth, heartbeat, sequence, close-code, slow-consumer, revocation, and
schema rules from `event-firehose-v1.md`; it SHALL NOT add replay or a stream
cursor.

Acceptance example: given a protocol-2 command and a protocol-1 server, when
the first offer receives 426, then the command follows Firehose E1's one-offer
fallback, subscribes under protocol 1, and does not submit a prior sequence.

### R7 — stdout envelope and purity

The command SHALL emit only LF-terminated, compact UTF-8 JSON objects on
stdout. It SHALL write banners, retry diagnostics, stack traces, and human
explanations only to stderr, with credentials and prompt/message content
redacted.

Acceptance example: given startup, two sends, a reconnect, and shutdown, when
stdout is split on LF and each nonempty segment is decoded, then every segment
is one complete JSON object and no non-JSON byte occurs.

The command SHALL wrap each canonical Firehose frame without modifying it:

```json
{"type":"event","protocolVersion":1,"generation":2,"event":{"type":"change","schemaVersion":2,"subscriptionId":"external-agent-2","seq":41,"class":"message.created","resource":"transcript messages","op":"upsert","occurredAt":1786900000000,"refs":{"messageId":"m_2","sessionKey":"s_1"},"payload":{}}}
```

Acceptance example: given a captured Firehose frame, when the corresponding
stdout event is decoded, then its `event` value is structurally and
byte-semantically equal to the captured frame and `generation` identifies the
connection that received it.

### R8 — replacement snapshot

AFTER `subscription_ready`, and after every same-connection history-boundary
invalidation under R9, the command SHALL begin a new snapshot cycle. It SHALL
construct a candidate containing exactly the authorized current
selected-session item and the complete visible paginated sets of transcript
messages, target wakes, and turns, using the canonical REST routes and
serializers.

For each candidate, the command SHALL fetch the selected session as `S0`,
record `S0.rowVersion` and `S0.clearedThroughSeq`, fetch the complete
cursorless transcript snapshot, and fetch the selected session again as `S1`.
It SHALL accept the REST candidate only when the two values match in `S0` and
`S1`; otherwise it SHALL discard the candidate and repeat from `S0`. It SHALL
omit every transcript message whose `seq` is at or below the accepted
`clearedThroughSeq`.

Acceptance example: given 1,205 visible messages plus paginated wakes and
turns under equal session reads, when snapshot cycle 1 bootstraps, then the
candidate visits every visible row once in each canonical resource order,
contains no row for another session, and contains no message at or below its
accepted history boundary.

Acceptance example: given a history boundary advance between transcript page
three and `S1`, when `S1` differs from `S0` in `rowVersion` or
`clearedThroughSeq`, then the command emits no `snapshot.item`,
`snapshot.end`, or `ready` from that candidate and restarts the cycle's REST
reads from a fresh `S0`.

WHILE those REST reads run, the command SHALL buffer canonical Firehose frames.
After an acceptable `S1`, it SHALL atomically detach a finite prefix through a
cut `Q` and validate that prefix in connection-sequence order before emitting
the candidate. A connection doubt through `Q` SHALL reject the candidate and
restart with a healthy subscription. A session item at or below
`S1.rowVersion` is covered. A higher session item with the accepted
`clearedThroughSeq` updates the candidate. A higher session item with a
different `clearedThroughSeq` SHALL reject the candidate before publication
and restart from `S0`. Other rebuildable items SHALL apply to the candidate by
canonical last-version-wins rules; a message at or below the accepted boundary
SHALL remain omitted.

Acceptance example: given buffered session versions with boundaries 5 then 10
while `S0` and `S1` are the later version at boundary 10, when the prefix is
validated, then both covered notices are no-ops and the candidate does not
livelock. Given instead a newer different-boundary notice through `Q`, the
candidate is rejected before any `snapshot.begin` for it.

The snapshot wire SHALL be:

```json
{"type":"snapshot.begin","protocolVersion":1,"generation":2,"snapshotCycle":3,"sessionKey":"s_1","resources":["sessions","transcript messages","wakes","turns"]}
{"type":"snapshot.item","protocolVersion":1,"generation":2,"snapshotCycle":3,"resource":"sessions","item":{}}
{"type":"snapshot.item","protocolVersion":1,"generation":2,"snapshotCycle":3,"resource":"transcript messages","item":{}}
{"type":"snapshot.end","protocolVersion":1,"generation":2,"snapshotCycle":3,"sessionKey":"s_1"}
```

The command SHALL emit the selected session item first, transcript messages in
ascending `(seq,id)` order, wakes in ascending `(createdAt,wakeId)` order, and
turns in ascending `(createdAt,seq)` order. It SHALL emit `snapshot.end` only
after all four resource sets are complete. It SHALL then emit the detached
prefix as canonical `event` frames in connection-sequence order and emit:

```json
{"type":"ready","protocolVersion":1,"generation":2,"snapshotCycle":3,"sessionKey":"s_1"}
```

The command SHALL emit no snapshot frame until the candidate and prefix pass
the preceding validation. A consumer SHALL stage all snapshot items and
pre-ready events for that cycle; `ready` SHALL atomically publish the staged
replacement. Frames after `Q` SHALL remain buffered until `ready` and then
follow it in connection-sequence order.

Acceptance example: given a disconnect after three `snapshot.item` frames,
when the command reconnects, then it emits `snapshot.aborted` for that
generation and snapshot cycle, never emits its `ready`, and starts a new
generation whose complete cycle can replace the consumer's staged state.

Acceptance example: given a message committed between the transcript page and
snapshot completion, when the validated prefix drains, then the staged model
contains the message through the snapshot, the buffered event, or both; it is
never absent from both when `ready` publishes the replacement.

### R9 — duplicate and gap semantics

WHEN the same `(resource, primary key, rowVersion)` appears in both a snapshot
and an event, the command MAY emit both; a conforming consumer SHALL apply
last-version-wins and treat an equal version as a no-op. For a session item,
the consumer SHALL treat an event at or below the cycle's covered session
version as a no-op even if it carries an older boundary.

Acceptance example: given message `m_2` version 8 in the snapshot and the same
version in a buffered `message.created` event, when a consumer applies both,
then its model contains one version-8 `m_2`.

WHEN a ready consumer receives a higher-version selected-session event whose
`clearedThroughSeq` differs from its accepted history boundary, it SHALL
atomically accept the higher boundary and remove every transcript message with
`seq` at or below that boundary before its next presentation, and SHALL mark
the prior transcript replacement noncurrent. The command SHALL emit that
canonical event in order, buffer subsequent events, and begin a cursorless
replacement snapshot cycle on the same healthy subscription. A higher session
version with the same boundary is an ordinary last-version-wins update and
does not rebuild.

Acceptance example: given a ready model holding messages 1 through 120 at
boundary 0, when a higher session event advances `clearedThroughSeq` to 100,
then the consumer removes messages 1 through 100 before its next presentation,
the command begins a new snapshot cycle, and that cycle can publish only after
its accepted boundary and buffered prefix satisfy R8.

Acceptance example: given a higher same-boundary session update followed by a
covered older session notice, when both arrive in order, then the first updates
the session item, the second is a no-op, and neither starts a replacement
snapshot.

WHEN a reconnect succeeds, the command SHALL create a new generation,
resubscribe first, and emit a full replacement snapshot before `ready`. It
SHALL NOT claim or reconstruct the Firehose notices that occurred while
disconnected.

Acceptance example: given a wake that advances from scheduled to fired while
the socket is down, when generation 2 becomes ready, then its snapshot contains
the current fired wake row; stdout need not contain the missed scheduled-to-
fired notice sequence and makes no claim that it does.

IF a sequence skip, heartbeat mismatch, slow-consumer close, restart close, or
other doubt occurs, the command SHALL invalidate the current live generation
and follow the same resubscribe-and-replacement-snapshot path.

Acceptance example: given events at Firehose sequence 9 then 11, when 11
arrives, then generation 1 emits no further applied event, enters reconnect,
and generation 2 reaches `ready` only after a complete snapshot.

IF canonical REST cannot complete a replacement snapshot, the command SHALL
emit `snapshot.aborted`, SHALL NOT emit `ready` for that snapshot cycle, and
SHALL either retry connection recovery for a transient failure or terminate
with a fatal frame for an authorization, protocol, or permanent projection
failure.

Acceptance example: given page two returning `projection_invalid`, when the
snapshot is staged, then the generation is aborted and no partial snapshot is
presented as ready state.

### R10 — identifier correlation

For every accepted send, the command SHALL preserve this correlation chain
without inventing a replacement identifier:

```text
stdin requestId
  -> send.accepted.wakeId
  -> wake payload/refs wakeId
  -> turn payload wakeId + turn seq + turn messageId
  -> transcript message payload turnSeq + id + replyToMessageId
```

Acceptance example: given accepted `req-17 -> w_123`, turn row `seq:44,
wakeId:w_123,messageId:m_prompt`, and assistant message
`id:m_reply,turnSeq:44,replyToMessageId:m_prompt`, when the consumer traverses
the fields, then it identifies `m_reply` as a response on the accepted send's
turn without a synthesized conversation id.

The command SHALL preserve nulls and missing relationships from canonical
rows and SHALL NOT infer that every wake starts a turn, every turn yields one
assistant message, or every message is a reply.

Acceptance example: given a canceled wake with no turn, when its current row
arrives, then the output preserves the wake state and contains no fabricated
turn or reply reference.

### R11 — lifecycle, EOF, signals, and revocation

WHEN the live socket disconnects for a recoverable network or server reason,
the command SHALL emit a `connection` frame with state `reconnecting`, the
ended generation, and the safe close code/reason; it SHALL keep reading stdin
and retry until it reconnects, stdin closes, a termination signal arrives, or
a fatal auth/protocol condition occurs. Retry pacing is an implementation
choice but SHALL NOT busy-loop.

Acceptance example: given a gateway restart close 1012 while stdin stays open,
when the gateway returns, then the same process increments its generation,
re-authenticates, snapshots, emits `ready`, and accepts later sends.

WHEN stdin reaches EOF, the command SHALL stop accepting input, complete a
terminal `send.accepted` or `send.rejected` for every send already read, close
the WebSocket normally, flush complete stdout frames, and exit 0.

Acceptance example: given two sends whose lines precede EOF, when EOF arrives
during the second wake request, then each request receives exactly one terminal
send frame before process exit and no partial JSON line remains.

WHEN the process receives SIGINT or SIGTERM, it SHALL stop accepting input,
finish at most the currently encoding stdout frame, close the WebSocket when
possible, and exit 130 for SIGINT or 143 for SIGTERM. A second termination
signal MAY force immediate exit.

Acceptance example: given SIGTERM during live delivery, when the process
stops, then previously completed stdout lines remain valid JSON, no new send is
accepted, and the exit status is 143.

WHEN the credential is revoked, retired, rotated, or no longer authorized,
the existing Firehose policy close or the next re-authentication SHALL end the
connection; the command SHALL emit a fatal safe error and exit 1 rather than
switch credentials or principals within the process.

Acceptance example: given an active session bearer whose session retires,
when the socket closes with policy code 1008, then the process does not fall
through to environment or `gateway.json`, emits no further selected-session
row, and exits 1.

IF stdout closes or returns a write error, the command SHALL stop gateway I/O,
close the socket, write at most a credential-free diagnostic to stderr, and
exit 1.

Acceptance example: given a downstream pipe that closes after `ready`, when
the next event hits EPIPE, then the command closes rather than continuing to
send prompts or accumulate undisclosed output.

### R12 — structured errors

Recoverable stdin errors SHALL use:

```json
{"type":"input.error","protocolVersion":1,"requestId":null,"code":"invalid_json","message":"stdin line is not valid JSON"}
```

`requestId` SHALL be the valid parsed request id when available and `null`
otherwise. Fatal errors SHALL use:

```json
{"type":"fatal","protocolVersion":1,"code":"auth_failed","message":"gateway authentication failed"}
```

Snapshot interruption SHALL use:

```json
{"type":"snapshot.aborted","protocolVersion":1,"generation":2,"snapshotCycle":3,"code":"connection_lost","message":"snapshot did not complete"}
```

Connection transition SHALL use:

```json
{"type":"connection","protocolVersion":1,"state":"reconnecting","generation":2,"code":"server_restart","message":"gateway connection closed"}
```

The error `code` domains SHALL reuse an existing gateway/Firehose public code
when one exists. CLI-only codes are limited to `discovery_failed`,
`invalid_utf8`, `invalid_json`, `invalid_frame`,
`unsupported_protocol_version`, `duplicate_request_id`,
`outcome_unknown`, `connection_lost`, and `stdout_failed`.

Acceptance example: given one gateway `identity_not_yours` refusal and one
malformed stdin line, when both are emitted, then the first preserves
`identity_not_yours`, the second uses `invalid_json`, and neither frame
contains a credential, stack trace, or unrelated row identifier.

## Satellite acceptance

R13. GIVEN an assimilated satellite with the supported local CLI and a
configured remote organization gateway, WHEN the command starts on that
satellite, it SHALL use the existing discovery result and establish its
WebSocket, REST, and wake requests through that remote gateway without
starting, probing, or requiring a satellite-local gateway.

Acceptance example: given the gateway on host A and the CLI process on host B,
when host B has no listening Tightbeam gateway, then the command on B still
reaches `ready`, sends a wake, and receives the selected session's reply from A.

R14. GIVEN one isolated non-production gateway, one real selected agent
session, and one assimilated satellite on a different host, WHEN the satellite
CLI sends two uniquely identified prompts through stdin, it SHALL emit each
`send.accepted`, the corresponding wake and turn identifiers, and each real
assistant `message.created` response through stdout without an external
transcript poll.

Acceptance example: the evidence captures the satellite hostname, gateway
hostname and endpoint, absence of a satellite-local gateway, CLI and gateway
source revisions, selected session key, redacted discovered credential kind,
two requestId-to-wakeId-to-turn-to-message chains, and parsed stdout frames.
The replies are observed responses from the real harness, not synthetic
fixtures.

R15. GIVEN the R14 conversation and a forced Firehose-only disconnect, WHEN a
new durable selected-session change commits during the gap and the CLI
reconnects, it SHALL emit `snapshot.aborted` or `connection` for the old
generation, a complete replacement snapshot for the new generation, the gap's
current durable state, and `ready`; it SHALL emit no replay claim or stream
cursor.

Acceptance example: the proof drops only the WebSocket path while leaving the
gateway's REST and wake paths available, commits a uniquely identifiable
message or wake row, restores the socket, and shows the row in the new
snapshot. Duplicate same-version rows are accepted under R9 and no current
visible row is missing at quiescence.

The R13-R15 proof and every product test or gate SHALL run on Eezo or Racter.
The Mix gate SHALL use the repository's unmodified canonical
`scripts/verify_mix.sh`; the repository-prescribed Rust gate SHALL run on one
of those same authorized test hosts. The proof SHALL place the satellite CLI
and its isolated non-production gateway on different hosts and SHALL name
both hosts and the gate host in its receipt.

Acceptance example: a receipt shows the unmodified `scripts/verify_mix.sh`
and the Rust gate ran on Eezo or Racter, identifies an Eezo-or-Racter
satellite client and a different host for the isolated gateway, and reports
R13-R15 from that topology. A receipt using Gibson for a product test, gate,
gateway, or satellite process fails regardless of result.

Gibson MAY compile and package the exact candidate only in an exact-tip
throwaway worktree. That build/package permission does not permit a product
test, gate, proof process, development gateway, or ad-hoc product execution
on Gibson.

Acceptance example: a Gibson receipt identifies the exact candidate commit,
the disposable worktree, and only compile/package commands; any Gibson test,
gate, gateway boot, CLI proof run, or other product execution fails this
requirement.

## Non-goals

- No Firehose replay, event persistence, retention, resume cursor, SSE,
  webhook, or polling loop.
- No replacement for ordinary wake and no new message table, send endpoint,
  conversation id, or reply id.
- No arbitrary subscription filters, multi-session connection, dynamic target
  change, display-name selection, role fallback, delayed wake, condition wake,
  attachments, binary stdin frame, or interactive text mode in v1.
- No credential, ticket, capability, API key, Visitor schema, Visitor
  security subsystem, identity registry, caller-declared read principal, or
  authorization grant.
- No claim that current-state repair replays every intermediate transition or
  observational event.
- No change to Clawline's chat WebSocket, Firehose wire, canonical REST item
  projections, or existing command semantics.
- No release, install, deploy, gateway power, production configuration,
  service, credential, identity, database, or live-state operation.

## Implementation slices and dependency map

| Slice | Buildable outcome | Depends on | Current disposition |
|---|---|---|---|
| S1: CLI NDJSON shell | command parsing; R4/R5/R7/R11/R12 framing; one pinned discovery result; ordinary wake adapter | settled `tightbeam session-connect --session <sessionKey>` spelling; existing Rust CLI discovery and dispatch | Command spelling settled by PO `att_5b9f2770`; private non-integrating candidate work is authorized from recorded base `6c339228`. |
| S2: credential-derived Firehose authentication | ChangeSocket composes existing active session-token authentication into that exact session principal; device tokens retain their existing user principal; organization CLI tokens have no selected-session read authority; exact selected-session filter | Firehose owner `asg_34c16cdf`; `session-tokens-v1`; REST AU1-AU4; current ChangeSocket source; no Visitor expansion | Required gap: current ChangeSocket evidence authenticates only `Devices.by_token`, while CLI discovery can yield session or organization credentials. No current source proves a CLI session/org token can authenticate ChangeSocket. `--as-user` is attribution only and cannot close the gap. The technical owner must compose existing session-token resolution; an organization token fails R3 rather than becoming a user; no credential or Visitor security lane is minted. |
| S3: snapshot and live bridge | subscription-first four-resource snapshot; canonical S0/message/S1 boundary cut; `snapshotCycle` framing; buffered-prefix validation; canonical event wrapping; correlation; same-connection boundary rebuild; reconnect replacement | canonical Firehose r6; `transcript-verb-v1` steps 3–8; canonical REST/session/transcript/wake/turn routes on the selected line | Specs exist. Candidate source availability, canonical subscribe wire, and shared serializers must be proved from recorded base `6c339228`; the elected integration line must satisfy the same proof before merge. |
| S4: isolated integration and satellite proof | R13-R15 real bidirectional conversation and reconnect repair | reviewed S1-S3 candidate; Eezo/Racter gates; assimilated satellite; isolated gateway on a different host; real harness credential on its owning host | Required before delivery acceptance. Mix uses unmodified `scripts/verify_mix.sh`, the Rust gate runs on Eezo or Racter, and Gibson is compile/package-only in an exact-tip throwaway worktree. This grants no release or install authority. |

Dependency availability on 2026-09-13:

- Firehose Slice 2 is reviewed and present on source line `origin/0.1.9` at
  `6c3392280ef7c2ae1fee780332ea00107f24d538`; this is source availability,
  not integration or release authority. PO `att_5b9f2770` authorizes private
  non-integrating candidate development from that exact recorded base. The
  base identifies bytes only; it implies no candidate branch or destination
  branch.
- Firehose portfolio owner `asg_34c16cdf-8195-4a73-a7e7-88b2dfbc7674`
  retains broader main/0.1.9 custody. This spec neither transfers it nor
  declares main equivalent.
- Canonical REST and Firehose contracts are coupled in `tightbeam-specs`.
  The implementation owner must prove the elected line provides the named
  routes, serializers, filters, and notice classes before composition.
- At inspected Firehose source `6c339228`, ChangeSocket authentication calls
  `Devices.by_token` and retains that device's `user_id`, `device_id`, and
  `is_admin`; it has no session-token or organization-token branch. Existing
  CLI discovery can return a session or organization token. This is the S2
  composition gap, not evidence for caller-declared read authority.
- At that same source revision, ChangeSocket requires
  `protocolVersion:1` inside each subscribe frame. Canonical Firehose S1/E1
  places protocol negotiation only on the WebSocket upgrade and forbids that
  subscribe field. The elected source line must resolve this mismatch before
  S3 integration; the CLI does not fork the canonical wire to accommodate it.
- Visitor `att_86c98dbc` proves current caller-declared event attribution is
  preserved at the inspected source seam. It does not make that attribution
  an authorization principal. `att_a740faef` keeps expanded Visitor
  schema/security work paused. This command supplies the concrete
  outside-agent use without authorizing that expansion.
- The integration line is not chosen by this spec. Operator request
  `dr_107b5cbc` remains open between `0.1.9` and `main`. Private candidate
  branching, implementation, and remote gates may proceed from recorded base
  `6c339228`; no dependency ref, base commit, private candidate branch, or
  Firehose delivery line is target authority.

## Resolved product question

### BQ1 — public command spelling (product owner)

PO `att_5b9f2770` settles the public spelling as
`tightbeam session-connect --session <sessionKey>`. The alternatives
considered were `session-stdio` (precise but implementation-flavored),
`session-stream` (suggests stdout-only), and `connect` (too broad for a growing
CLI). No command-spelling question remains.

## Open questions — BLOCKING

### BQ2 — integration line (delivery owner)

Which authorized product line receives implementation? Current evidence proves
Firehose Slice 2 source availability on `origin/0.1.9` and retains a broader
main obligation, but this assignment grants no target selection. PO
`att_5b9f2770` authorizes private non-integrating candidate development and
gates from exact recorded base `6c339228`; that base implies no branch.
Operator request `dr_107b5cbc` asks whether `0.1.9` or `main` receives the
feature. This question blocks integration only. It does not block private
candidate branching, implementation, proportional review, or remote gates.

## Open questions — NON-BLOCKING

### NQ1 — future first-class Visitor presentation

If Visitor later supplies a first-class external presentation, should a future
protocol version expose its public participant label in a connection-ready
frame? V1 deliberately uses existing credential-derived authorization and
ordinary action-origin behavior and does not need that display field to send,
correlate, or receive.

### NQ2 — retry pacing

The exact reconnect delay and jitter policy is left to implementation. It must
avoid a busy loop and preserve R11's observable retry-until-terminal behavior;
changing the pacing without changing those observations does not amend this
spec.

### NQ3 — optional bounded bootstrap presentation

A later version may offer a caller-selected initial history bound. V1 emits a
complete current visible replacement snapshot so reconnect correctness has one
meaning. Adding a bound would require an explicit gap indicator and is not
part of this build.
