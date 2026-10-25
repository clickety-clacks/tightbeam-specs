# Tool-call and session-transition records v1: REST and Firehose

Status: PROPOSED, 2026-10-25, revision r7. The size bound in §8 is ruled (64 KiB
per field). This file lands with its coupled amendments (§2) in one reviewed
revision.

r6 supersedes r5 (sha256
`d22b11f2f248878832cac2f61da18c0b672b7d079c0720c3ef0b7a7e46629991`) in one
respect: the session history boundary no longer hides tool records from REST or
Firehose [R-hist]. The clauses changed are AS6, TC13, the tool-call cells of
§7.1, FH1, FH5, NG11, §11.1, §11.2, A10, A11 and Q6. Every other clause is r5's
text.

r7 supersedes r6 (sha256
`86c9495f5998d59574c4221ac2b4ce8bf64b44fb6796e7731e7d0e280c4a8f27`) only in §2:
the coupled files are composed on the public specs main after the reset-safe
history amendment. No requirement changes.

Target: the release after 0.1.12. Base read for this contract: Tightbeam
`0.1.11` at `306f423d`, with adapters `@agentclientprotocol/claude-agent-acp`
0.81.0 and `codex-acp` 1.12.0 as pinned by that line.

## 1. Authority and spirit

Ask, 2026-10-24:

> "I want to be able to get to [tool] call information from the server... add this
> to Firehose as one of the things you can add to your Firehose subscription? Are
> you also getting fences like model switches... all the stuff should be coming in
> through the firehose and it should be giving you an API to turn it on and off as
> you need it"

Cited below as **[ASK]**. The Chat client is the first consumer. The ask is
settled into three outcomes and four limits, cited as follows:

- **[O1]** On Claude and Codex harnesses, each tool call and its result become
  durable records, ordered with the session's transcript messages and readable
  through REST the way messages are.
- **[O2]** Session transitions that mark a boundary (model or effort change,
  harness change, context reset or compaction, and similar transitions the system
  already observes) are readable as ordered points in the same history.
- **[O3]** Each category reaches Firehose as its own notice class. Subscribers
  turn categories on and off with the existing class filters and
  unsubscribe/subscribe; a separate on/off API only if the filters cannot serve.
- **[L-vis]** Existing session visibility applies. Add no new restriction,
  refusal or hardening.
- **[L-size]** Store what a client needs to show which tool ran, its input and
  its result. A bound on stored size states what a reader sees when it applies.
  Nothing is cut silently.
- **[L-turns]** Agent turns and notice batching stay as they are.
- **[L-schema]** State the schema need; the schema version slot is assigned at
  implementation.

A later ruling on the history boundary, 2026-10-25, cited as **[R-hist]**:

> "clearedThroughSeq marks an agent-context restart, never hides earlier
> human-visible REST history or Firehose rows. After harness changes,
> turn-failure recovery or any reset, the human still sees earlier words and
> replies, with a boundary marker. Agent context visibility is unchanged."

> "[The ruling] includes Chat-visible tool records and transition rows as earlier
> human-visible transcript history. clearedThroughSeq marks agent-context
> restart, not a REST-history/Firehose visibility cutoff for those rows; agent
> context exposure remains unchanged."

Spirit relied on: Firehose r6 P1 to P5 (`event-firehose-v1.md`, sha256
`ea7765bf151364f365975656d781ee99fda289326bdefcb07dd2ea63b855e266`). The state
database is truth, the stream only announces committed changes, missed notices are
rebuilt from REST, the socket carries no history, and REST owns reads. Cited as
**[P1]** to **[P5]**. Where a choice was open, it is resolved toward these:
anything a client sees live it can rebuild from REST, and every category can be
switched with the subscription filters that already exist.

## 2. Homing and coupled files

This file is a successor amendment to the Firehose r6 coupled set. It changes R8
mappings, a filter value and wire types, so by Firehose §Spec homing the
amendments in §11 land in `event-firehose-v1.md`, `rest-state-api-v1.md` and
`rest-state-api-v1-wire-schema.md`, together with this file, in one reviewed
revision. `cli-surface-v1.md` is the fourth file of the coupled set; this
contract changes nothing in it (§11.4).

Base revisions read:

| File | sha256 |
|---|---|
| `event-firehose-v1.md` (r6) | `ea7765bf151364f365975656d781ee99fda289326bdefcb07dd2ea63b855e266` |
| `rest-state-api-v1.md` (r4) | `4beab8ce659cf9e0f43e818086a9208b7e3b8edfccc6f245ec169956ed950c5a` |
| `rest-state-api-v1-wire-schema.md` | `4c52e940f3cf7f86139701f0b0066a15bcb9779d76ded92cf1da44f9f69ec68c` |
| `cli-surface-v1.md` | `c392c42369a8c4aeb9f4a265809d8359326cf09a861e01a62400d0311c539c86` |

The composed coupled files are built on the public specs main at
`5233467710bc1a8b49dc9c349659aa7e0c9598c6`, where these files read:

| File | sha256 |
|---|---|
| `event-firehose-v1.md` | `95d933208cac6a81c232a649aa59592e33bfc77716776b6cfe3c8fc4acf52c13` |
| `rest-state-api-v1.md` | `68eba1c42d368a4bcd5067f1e436a4ca5b9157a8282e701f960a49ea53ee2313` |
| `rest-state-api-v1-wire-schema.md` | `f5dfb8d0988ee8d44ea0441b1035ca753902e15281af62f6f94f3c903995222f` |
| `cli-surface-v1.md` | `c392c42369a8c4aeb9f4a265809d8359326cf09a861e01a62400d0311c539c86` |
| `chat-reset-safe-history-v1.md` | `dd21e0fa8e4c65a890ab6282e16c7294b93057fe1bd227eaae0e67a70bb6a512` |

That base already carries the reset-safe history amendment, which composes
with this contract by its §8a. Its `marker` key, `TransitionMarker` shape and
R7m presence rule are the TR4 edit, made once; §11's marker-field bullets are
met by that text. TR5 replaces its closed `marker.kind` domain. Marker messages
travel as `transition.recorded` (FH2), and its statements that markers travel
as `message.created` and that `transition.recorded` is absent describe the
public 0.1.9 and 0.1.12 lines only. Its version rule (REST R7s) covers a
marker item on either class. The M4 chat client subscribes as §11.1 states and
rebuilds as that amendment states, with no rebuild for a boundary change. Its
sender, version and history requirements are unchanged.

## 3. Goal and non-goals

Goal. For Claude and Codex sessions, every tool call the harness reports becomes a
durable record with its tool, input and result. Every boundary transition the
gateway already detects, plus context compaction, becomes an ordered point in the
transcript. Both are readable through REST and announced on Firehose under their
own classes. A subscriber turns each category on or off with the existing class
filter. [ASK] [O1] [O2] [O3]

Non-goals (the build does not drift into these):

- NG1. No new on/off API, subscription verb or preference store. §7.3 shows the
  existing filters serve. [O3]
- NG2. No change to when or how agent turns run, how assistant text is committed,
  or how the agent-notice batcher works. [L-turns]
- NG3. No new visibility rule, redaction, refusal, rate limit or other hardening.
  Tool records are user content like transcript content. [L-vis]
- NG4. No live streaming of partial tool output. A tool record is committed when
  first seen and when it ends (§5.3).
- NG5. No inference of a result the harness did not report. A call whose result
  never arrives stays non-terminal (§5.3).
- NG6. No change to the client capabilities the gateway advertises to adapters.
  Compaction is observed in the form the pinned adapters emit today (§6.2).
- NG7. No CLI verb or flag (§11.4).
- NG8. No retention or pruning policy. Tool records follow their session's
  transcript lifecycle.
- NG9. No transition kinds beyond those in §6. A model change the harness reports
  on its own, without a Tightbeam retune, is not recorded (Q3).
- NG10. No ordering change inside a turn's committed assistant text (Q1).
- NG11. No change to what a harness is given as agent context when a turn
  starts, including after a history-boundary advance. [R-hist "Agent context
  visibility is unchanged"]

## 4. Terms and assumptions

Terms:

- **Tool call**: one ACP `tool_call` notification and the `tool_call_update`
  notifications that share its `toolCallId`, received by the gateway's ACP adapter
  for a session during a turn.
- **Tool record**: the durable row and its public projection for one tool call
  (resource `tool calls`).
- **Terminal status**: ACP tool status `completed` or `failed`. `pending` and
  `in_progress` are non-terminal.
- **Transition**: a transcript marker message, `messageType:"marker"`, written
  through the existing marker write seam (`Projection.append_marker*`). Its
  `marker` object names the kind and the before and after values.
- **Anchor** (`afterMessageSeq`): the greatest transcript-message `seq` of the
  session, or `0` when it has none, read in the transaction that first inserts a
  tool record.
- **Field bound**: the per-field size limit of §8.

Assumptions, each falsifiable by the named acceptance item:

- AS1. Both pinned adapters send a stable `toolCallId` on `tool_call` and on every
  `tool_call_update` for the same call: the Claude `tool_use` id or the Codex item
  id. Falsified by A1 or A2 if updates cannot be matched to their call.
- AS2. Both pinned adapters report a tool's input in `rawInput` and its result in
  `rawOutput` and/or `content`. Claude also sends `_meta.claudeCode.toolName`;
  Codex sends none. Falsified by A1 or A2 if a completed call shows neither input
  nor result.
- AS3. With the client capabilities the gateway advertises on 0.1.11, both pinned
  adapters report a context compaction as a `tool_call` whose `_meta` contains a
  `contextCompaction` object, followed by a `tool_call_update` to a terminal
  status. (Claude 0.81.0 `dist/context-compaction.js`; Codex 1.12.0
  `createContextCompactionStartUpdate`/`CompleteUpdate`.) Falsified by A3.
- AS4. An operator can force a compaction on each harness with the harness's
  `/compact` command sent as a prompt. Falsified by A3; if false, A3 uses any
  operator action that makes that harness compact.
- AS5. Every turn's prompt is committed as a transcript message before the turn's
  first tool call is observed. Falsified by A1 or A2 if a tool record's anchor is
  lower than its turn's prompt message `seq`.
- AS6. Withdrawn in r6. The history boundary does not filter tool records
  (TC13), so no requirement depends on where a post-boundary call anchors.

## 5. Tool records

### 5.1 What exists and what is new

Exists on 0.1.11: the adapter receives every `tool_call` and `tool_call_update`.
It uses them only for the progress label ("Using a tool" or the title), for
subagent markers (Agent/Task calls, in `subagent_markers.sourceEventRef`) and for
the rail gate probe. It drops the call id, input, output and content. No table
holds tool calls.

New: the `tool calls` table, writer, serializer, REST routes and Firehose classes
below.

### 5.2 Recording requirements

TC1. When the adapter receives a `tool_call` for a session, the gateway SHALL
commit one tool record carrying the session, the turn, the harness `toolCallId`,
the title, the kind, the tool name when the harness reports one, the status and
the input, output and content values the notification carries. [O1] [ASK "get to
[tool] call information from the server"]
Example: a Claude session runs `Bash` with `{"command":"ls"}`. A REST read of the
session's tool calls shows one record with `toolName:"Bash"`,
`rawInput:{"command":"ls"}` and status `pending` or `in_progress` before the
result arrives.

TC2. When the adapter receives a `tool_call_update` that brings a known call to a
terminal status, the gateway SHALL update that call's record in one commit with
the terminal status and every field value received for the call since the last
commit, applying the notifications in arrival order. [O1]
Example: the same `Bash` call finishes. The record now shows `status:"completed"`,
the listing in `rawOutput` or `content`, an `endedAt` time and `rowVersion:2`.

TC3. While a call is non-terminal, the gateway SHALL NOT commit intermediate
`tool_call_update` notifications on their own. It SHALL fold them into the
terminal commit. [L-turns, NG4; keeps writes to two per call]
Example: a Codex `execute` call reports `in_progress` with partial output three
times, then `completed`. The record has `rowVersion:1` until completion and
`rowVersion:2` after, with the final output.

TC4. If the first notification for a call already carries a terminal status, the
gateway SHALL commit one record in that terminal state. [O1]
Example: a call reported `completed` in its first `tool_call` produces one record
with `rowVersion:1` and status `completed`.

TC5. If a call's turn ends, or its adapter process stops, before a terminal status
arrives, the record SHALL keep its last committed non-terminal status and no
`endedAt`. The gateway SHALL NOT invent a result or a terminal status. [NG5,
L-size "nothing is cut silently"] If a terminal update for that call arrives later
in the same session, TC2 applies.
Example: the gateway is restarted mid-call. The record stays `in_progress`; the
turns resource shows the turn ended. A reader can see both.

TC6. A `tool_call_update` whose `toolCallId` matches no record committed for the
session SHALL be recorded as if it were the call's first notification (TC1 or
TC4). [O1; nothing seen is dropped]
Example: an update arrives for an id the gateway never saw start. One record
appears with whatever fields the update carried; absent fields are null.

TC7. Records SHALL be kept for every tool call the adapter receives, including a
compaction call (§6.2) and calls made inside a subagent. [O1 "each tool call"]
Example: a Claude `Task` call whose subagent runs `Read` twice produces three
records.

TC8. The insert that creates a record SHALL read the anchor in the same
transaction, so within one session record `seq` order never contradicts anchor
order. [O1 "ordered with the session's transcript messages"]
Example: records with `seq` 900 and 905 in one session have anchors 410 and 410,
or 410 and 412; never 412 and 410.

### 5.3 Public projection (REST and Firehose payload)

Field list, in R7 order:

| Field | Type | Meaning | Cites |
|---|---|---|---|
| `id` | S | Gateway id, `tc_` + UUIDv4. Primary key; equals Firehose `refs.toolCallId`. | [P5], Firehose V5 |
| `seq` | I | Global insert order. Immutable. | REST R5 |
| `sessionKey` | S | The session. | [O1] |
| `turnSeq` | I | The turn during which the call was first seen. | [O1] |
| `afterMessageSeq` | I | Anchor (§4). The record sorts after transcript message `afterMessageSeq` and before the next one. | [O1] |
| `harnessToolCallId` | S | ACP `toolCallId`. | [O1] |
| `title` | S | ACP title; `""` if absent. | [ASK "which tool"] |
| `kind` | S | ACP kind (open string: `read`, `edit`, `execute`, `think`, ...); `"other"` if absent. | [ASK] |
| `toolName` | S | Harness-reported tool name (`_meta.claudeCode.toolName`), else null. | [ASK] |
| `status` | S | `pending`, `in_progress`, `completed` or `failed`. | [O1] |
| `rawInput` | J | ACP `rawInput`, or null. | [L-size "input"] |
| `rawOutput` | J | ACP `rawOutput`, or null. | [L-size "result"] |
| `content` | J | ACP `content` array, or null. | [L-size "result"] |
| `truncated` | A<O<ToolCallTruncation>> | One entry per bounded field (§8); `[]` when none. | [L-size "nothing is cut silently"] |
| `startedAt` | I | Commit time of the first insert. | [O1] |
| `endedAt` | I | Commit time of the terminal commit, else null. | [O1] |
| `rowVersion` | I | 1 at insert; +1 per later commit. | Firehose V4a |

Nullable: `toolName`, `rawInput`, `rawOutput`, `content`, `endedAt`.
`ToolCallTruncation` is the closed object `{field, originalBytes}`.

TC9. REST detail, REST collection items and Firehose payloads for tool records
SHALL come from one serializer and be byte-equivalent. [P5, Firehose V3/A6]
Example: the `tool_call.ended` payload for `tc_…` equals the `item` of
`GET /api/sessions/:sessionKey/tool-calls/tc_…` read after that commit.

### 5.4 REST resource

Routes:

- `GET /api/sessions/:sessionKey/tool-calls`: paged collection, resource
  `tool calls`.
- `GET /api/sessions/:sessionKey/tool-calls/:toolCallId`: detail by `id`.

TC10. The collection SHALL follow REST R4 envelopes and R5 paging, oldest to
newest, default limit 50, cap 500, with cursor tuple `(seq, id)`. [O1 "readable
through REST the way messages are"]
Example: a session with 120 tool records returns its newest 50 on a cursorless
read; `before=page.oldestCursor` returns the previous 50.

TC11. The collection SHALL accept the filters `afterMessageSeqFromInclusive` and
`afterMessageSeqToExclusive` (integers, `>=` and `<`; either may be omitted).
[O1 "ordered with the session's transcript messages"; P3]
A record anchored at message m sorts after m and before the next message. So for
a displayed slice whose messages run from `seq` a through b, the records that
belong to it are those with anchors from a through b inclusive:

- for a slice that is not the newest, the client requests
  `afterMessageSeqFromInclusive=a&afterMessageSeqToExclusive=b+1`;
- for the newest slice (a cursorless message tail, `hasMoreAfter:false`), the
  client requests `afterMessageSeqFromInclusive=a` with no upper end, so calls
  after the newest message, including those of a running turn or of a turn that
  ended without a reply, are included.

Either request is a REST R5 page chain with fixed filters. A cursorless request
returns the newest matching page; the client follows `before` with
`oldestCursor` until `hasMoreBefore` is false, and then holds every matching
record. A reader orders a merged history by `(anchor, kind, seq)`, where a
message's anchor is its own `seq`, the message comes before every tool record of
equal anchor, and records of equal anchor keep `seq` order.
Example: messages 410 to 415 are the newest slice and a turn is running after
prompt 415. A request with `afterMessageSeqFromInclusive=410` returns the records
between 410 and 415 and the running turn's records anchored at 415. For the
older slice 400 to 409, `afterMessageSeqFromInclusive=400&afterMessageSeqToExclusive=410`
returns the records anchored at 400 through 409.

TC12. Visibility SHALL be exactly the REST AU4 transcript-messages rule: the
target session, its owner, or an admin. An unknown or forbidden session or record
id returns the same 404 as for messages. [L-vis]
Example: a session principal reading another session's tool calls gets the same
404 it gets for that session's messages.

TC13. The session's history boundary (`clearedThroughSeq`, REST R5d) SHALL NOT
filter tool records. The collection, its page flags and its `before` and `after`
chains SHALL return every record TC12 permits, whatever its anchor relative to
`clearedThroughSeq`, and an advance of `clearedThroughSeq` SHALL NOT remove a
record from them. The detail route applies TC12, as the message detail route
does. The boundary marks where the agent's context restarted; tool records are
not agent context (I6, NG11). [R-hist "never hides earlier human-visible REST
history or Firehose rows"; R-hist "not a REST-history/Firehose visibility cutoff
for those rows"; L-vis; P3]
Example: message 500 is a prompt whose turn was interrupted mid-call, leaving a
record anchored at 500. A harness change sets `clearedThroughSeq` to 500 and
appends its marker at 501. A cursorless read of the collection still returns the
record anchored at 500, followed by the next turn's calls anchored at 502, and no
page flag treats it as absent.

Transition markers are transcript messages, so the messages rule of REST R5d
governs how the boundary treats them. This contract adds no boundary rule for
them (Q6).

## 6. Transitions

### 6.1 What exists and what is new

Exists on 0.1.11 (transcript marker rows, `messageType:"marker"`, sent on Firehose
as `message.created`):

| Transition [O2] | Marker kind | Writer | from / to |
|---|---|---|---|
| Model change | `model-retune` | `gateway.ex` tune paths (≈8965, ≈9036) | `Model.describe/1` before and after |
| Effort or context-size change | `model-retune` | same; `Model.describe/1` includes the effort and context qualifiers | same |
| Harness change | `harness-switch` | `gateway.ex` swap transaction (≈8284), with `session.harness_changed` on the session row | `describe_engine(harness, model)` before and after |
| Context reset (fallback to a fresh harness session) | `session-restart` | `append_session_restart_marker` (≈4353) | old and new harness session ids |
| Context reset (identity override removed) | `session-restart` | `append_session_restart_marker` (≈9604) | old and new identity names |

Exists but undocumented: the 0.1.11 serializer emits a `marker` object
`{kind, from, to}` on marker messages (`state_resources.ex`, validator
`:transition_marker`, from commit `be61cfc9`). Canonical REST R7 and the wire
schema do not list it. §11 folds it in.

New: the `context-compacted` kind (6.2), the open reader domain for marker kinds
(6.3) and a separate Firehose class (7.2).

### 6.2 Context compaction

TR1. When the adapter receives a `tool_call` or `tool_call_update` whose `_meta`
contains a `contextCompaction` object and whose status becomes `completed`, the
gateway SHALL append one marker of kind `context-compacted` through the existing
marker write seam, once per compaction call. [O2 "context reset or compaction"]
Example: an operator sends `/compact` to a Codex session. Its transcript gains
one marker message with `marker.kind:"context-compacted"`, and its tool calls
gain one record titled "Compact conversation" with kind `think`.

TR2. The marker's `from` SHALL be the session's last context usage observed
before the compaction call began, written `"<used>/<size> tokens"`, or
`"unknown"` if none was observed. Its `to` SHALL be `"compacted"`. Its content
SHALL begin `[context compacted]` and state that the session's working context
was summarized. [O2; NG5: say only what was observed]
Example: last usage before compaction was 151,200 of 200,000. The marker shows
`from:"151200/200000 tokens"`, `to:"compacted"`.

TR3. A compaction call that ends `failed`, or never ends, SHALL produce no marker.
Its tool record still exists under §5. [NG5]
Example: a failed `/compact` leaves a `failed` tool record and no marker.

### 6.3 Marker field

TR4. A transcript-message item SHALL carry `marker` immediately after
`messageType` exactly when the stored marker kind is non-null, which the
existing table constraint ties to `messageType:"marker"`. Its value is the closed
object `{kind, from, to}` of non-null strings. Other items omit the key. [O2;
documents existing 0.1.11 bytes]
Example: a model retune message has `"messageType":"marker","marker":{"kind":"model-retune","from":"…","to":"…"}`; an assistant reply has neither key.

TR5. Producers SHALL emit only `harness-switch`, `model-retune`,
`session-restart` or `context-compacted` as `marker.kind`. Readers SHALL accept
an unrecognized kind string and show the message `content`. [O2 "and similar
transitions"; same additive rule as `messageType`, so an older Chat build is not
broken by the new kind]
Example: a reader built before this change receives `context-compacted`, does not
reject the item, and shows its text.

`marker.kind` names a transition, not a message kind. `messageType` stays the sole
message-kind discriminator (Firehose P6).

## 7. Firehose

### 7.1 Classes

| Class | Resource | Op | Primary notice ref | Serializer | Version and emission | Visibility and convergence | A1/A6 coverage |
|---|---|---|---|---|---|---|---|
| `tool_call.started` | `tool calls` | `upsert` | `toolCallId`, `sessionKey` | the one tool-call serializer (TC9) | A commit that inserts a non-terminal record (TC1, TC6) emits one notice after commit, whatever the record's anchor (FH5). | REST AU4 transcript visibility (TC12). Last-version-wins on `(payload.id, payload.rowVersion)`. | A1 covers the insert seam and class; A6 byte-equivalence with the detail route. |
| `tool_call.ended` | `tool calls` | `upsert` | `toolCallId`, `sessionKey` | same | A commit that sets a terminal status, by update (TC2) or by first insert (TC4, TC6), emits one notice after commit, whatever the record's anchor (FH5). | same | same |
| `transition.recorded` | `transcript messages` | `upsert` | `messageId`, `sessionKey` | exact shared R7 transcript-message serializer | Each new marker message emits one notice after commit, in place of `message.created`. An idempotent replay emits none. | `GET /api/sessions/:sessionKey/messages` visibility. Last-version-wins on `(payload.id, payload.rowVersion)`. | A1 covers the marker seam; A6 byte-equivalence with the message detail route. |

Refs also carry `turnSeq` for tool classes, and `assignmentId` when the turn has
one.

FH1. Each tool-record commit SHALL select exactly one of `tool_call.started`
and `tool_call.ended`, and SHALL emit through the existing post-commit
publisher. [O3 "each category ... its own notice class"; Firehose V1, D2]
Example: a call seen at start and at completion produces exactly one
`tool_call.started` and one `tool_call.ended`.

FH2. A marker-message commit SHALL select `transition.recorded` and SHALL NOT also
emit `message.created`. Every other new transcript message keeps
`message.created`. [O3; precedent: Firehose R8 sessions row, where
`session.harness_changed` replaces `session.updated` for its commit, "One commit
selects one class"]
Example: a harness switch commit emits `session.harness_changed` for the session
row and `transition.recorded` for its marker message, and no `message.created`.

FH3. The tool and transition notices SHALL use the existing D1 delivery, seq,
heartbeat and close behavior and the existing S2 filter matching. They add no
socket frame type. [P2, L-turns]
Example: a subscription with `classes:["tool_call."]` and a `sessionKey` filter
receives only that session's tool notices.

### 7.2 Compatibility with current subscribers

A subscriber that names exactly `message.created`, as the M4 recipe does today,
stops receiving marker messages live. It still sees them on every REST read and
rebuild, because markers stay transcript messages. Making transitions their own
class requires this: a class filter cannot keep messages while dropping
transitions if both share `message.created`. Dual emission would also break the
one-commit-one-class rule and deliver every marker twice to a `message.`
subscriber. The amended M4 (§11.1) adds `transition.`. This is the main point
for the Chat client (Q2).

### 7.3 The existing filters are the on/off control

The ask is for "an API to turn it on and off as you need it" [ASK]. Firehose S1
and S2 already give one: `classes` matches by prefix, so `tool_call.` and
`transition.` each switch one category. S4 changes the set with unsubscribe and a
fresh subscribe on the same connection. S5 allows 100 subscriptions, so a client
can also hold one subscription per category and drop it alone. Turning a
category on follows M1: subscribe, then read REST. No case was found that these
filters cannot serve, so no new API is proposed. [O3]

FH4. A subscriber that omits `tool_call.` and `transition.` from `classes` SHALL
receive no notice of either category. A subscriber with no `classes` filter
receives all, as S2 already states. [O3]
Example: Chat subscribes `["message.created","session."]` and receives no
`tool_call.*` or `transition.recorded` notices; it adds `"tool_call."` with
unsubscribe and subscribe and receives them from that cut.

FH5. The history boundary SHALL NOT suppress a tool-record notice: each
tool-record commit emits its FH1 notice whatever the record's anchor relative to
`clearedThroughSeq`. [R-hist "never hides earlier human-visible ... Firehose
rows"; P3, P5: the stream announces what REST serves]
Example: after `clearedThroughSeq` advances to 500, a late terminal update for
the record anchored at 500 is committed and emits one `tool_call.ended`, whose
payload equals the record's collection item.

## 8. Size bound (ruled: 64 KiB per field)

Store the tool, its input and its result [L-size]. Each of `rawInput`,
`rawOutput` and `content` is bounded separately.

Ruling, 2026-10-25: the field bound is 64 KiB (65,536 bytes) for `rawInput`,
`rawOutput` and `content`. It replaces the 16 KiB bound ruled on 2026-10-24.
TC14 stands as written; nothing is cut silently. NG8 stands, with no retention
or pruning. A2 records the exact received Codex field sizes and the share of
Codex results the server cuts at 64 KiB. If that share is around 5% or more, the
bound is reconsidered as a product question; it is not changed during
implementation. The Codex proxy figures below are not that cut rate.

Storage note. The expected growth is about 0.6 to 1.0 GB/day, about 39% above
the earlier 0.4 to 0.7 GB/day estimate for 16 KiB. The 39% comes from a Codex
proxy: one output array per call at 160,000 calls a day stores about 0.954
GB/day at 16 KiB and about 1.331 GB/day at 64 KiB. The proxy omits inputs,
duplication across `rawOutput` and `content`, JSON string escaping, `truncated`
entries, row, index and SQLite overhead, and the share of calls that are Codex.
Exact growth awaits A2. No retention change follows (NG8).

TC14. When a field's canonical JSON encoding (wire-schema J rules) exceeds the
field bound, the stored and served value SHALL be a JSON string holding the
longest prefix of that encoding that fits the bound without splitting a UTF-8
character, and `truncated` SHALL list `{field, originalBytes}` for that field.
A field within the bound is stored whole and is not listed. The bound counts the
UTF-8 bytes of the prefix itself; serving the prefix as a JSON string adds
escaping, so its encoded form on the wire can be longer than the bound.
`originalBytes` is the byte length of the full canonical encoding. [L-size
"nothing is cut silently"; "state what a reader sees"; ruling 2026-10-25]
Example: with a 64 KiB bound, a 643,384-byte result (the largest in the sample
below) is served as
`"rawOutput":"{\"file\":…"` (65,536 bytes or fewer) with
`"truncated":[{"field":"rawOutput","originalBytes":643384}]`. The full value is
not kept anywhere Tightbeam serves.

What a reader sees: a string where it would expect an object or array, plus the
`truncated` entry naming the field and its full size. A client can show "output
truncated: 628 KiB" and the prefix text.

Sizing basis. A sample of 150 recent Claude agent sessions, 42,546 tool calls,
sizes as canonical JSON:

| | mean | p50 | p90 | p99 | max |
|---|---|---|---|---|---|
| input | 667 B | 394 B | 1.4 KB | 4.6 KB | 69.6 KB |
| result | 3,384 B | 473 B | 4.9 KB | 25 KB | 643.4 KB |

Volume for the sampled deployment: about 6,000 turns a day at about 27 tool
calls a turn, so roughly 160,000 tool calls a day.

| Bound per field | results cut | inputs cut | stored per call, input + one result field | growth per day | if `rawOutput` and `content` both carry the result |
|---|---|---|---|---|---|
| 4 KiB | 12.5% | 1.2% | 1.8 KB | ~0.3 GB | ~0.5 GB |
| 16 KiB | 1.7% | 0.05% | 2.4 KB | ~0.4 GB | ~0.7 GB |
| **64 KiB (ruled)** | **0.5%** | **0%** | **2.8 KB** | **~0.45 GB** | **~0.8 GB** |
| none | 0% | 0% | 4.1 KB | ~0.65 GB | ~1.2 GB |

Codex proxy sample: 11 Codex sessions, 1,605 output arrays, sized as compact
JSON of the adapter's output array rather than the server's stored field bytes.
The share above the bound was 16.6% at 16 KiB, 6.4% at 32 KiB and 0.56% at
64 KiB, and stayed about flat to 256 KiB.

Basis for the ruled 64 KiB: it keeps 99.5% of Claude results whole, and in the
Codex proxy it is the first bound past which larger bounds cut almost no more.
In the worst case it holds a 50-record REST page under about 9.8 MB and a single
notice under about 192 KiB. The Claude sample alone shows a smaller storage rise
than the Codex proxy (table above); the storage note uses the larger rise. A2
reports observed Codex sizes under the re-check rule above. There is no
retention policy (NG8).

## 9. Invariants

- I1. Substrate and product stay separate. The gateway records what the adapter
  reports and announces committed rows. How a client groups, collapses, hides or
  presents tool records and transitions is the client's. Nothing in this contract
  names a presentation, threshold or default view. [Firehose P1, P2]
- I2. Everything a notice announces is rebuildable from REST: tool records from
  the tool-calls collection, transitions from the messages collection. [P3, P4]
- I3. Visibility is unchanged and shared with transcript messages (TC12). [L-vis]
- I4. Nothing is cut without a `truncated` entry (TC14). [L-size]
- I5. Turns, assistant-text commit timing and agent-notice batching are unchanged.
  Tool-record writes happen beside the turn, not inside its control flow.
  [L-turns]
- I6. Tool records are never transcript messages. They do not enter message
  pages, unread counts, attention tiers or the `transcript` verb. [O1 "readable
  ... the way messages are", not "as messages"; keeps old clients that treat an
  unknown `messageType` as an assistant bubble from rendering tool calls as
  replies]

## 10. Schema needs

The schema version slot is assigned at implementation [L-schema]. This contract
claims no REST or Mementos version number.

- SC1. A new table for tool records, holding the §5.3 fields (J values as JSON
  text, `truncated` as JSON text), with `seq` as an autoincrement key, `id`
  unique, and an index on `(sessionKey, seq)` and on `(sessionKey, afterMessageSeq)`.
  A lookup key for matching updates to a session's call by `harnessToolCallId`.
- SC2. The `messages.markerKind` check must accept `context-compacted`. SQLite
  cannot alter a CHECK in place, and a deployed `messages` table can hold more
  than a million rows, so the migration technique and its run time are chosen at
  implementation.

## 11. Coupled-file amendments

### 11.1 `event-firehose-v1.md`

- R4b gains `transition.recorded`; new R4d "Tool calls: `tool_call.started`,
  `tool_call.ended`."
- R8 table gains the three rows of §7.1. The `message.created` row's emission cell
  becomes "Each newly committed non-marker transcript message".
- M4 recipe: the chat client subscribes to `message.created`, `transition.`, the
  `session.` prefix and, when it shows tool calls, `tool_call.`, then reads REST.
  Rebuild reads the tool-calls collection alongside the messages tail when
  `tool_call.` is subscribed.
- A1 table covers the tool-record insert and terminal seams and the marker seam;
  A6 covers the tool-call serializer.
- V1 is unchanged; the history boundary adds no exception to it (FH5).
- §Spec homing names this successor's set.

### 11.2 `rest-state-api-v1.md`

- R2 and the route-to-resource table add the two tool-call routes; R3c adds the
  detail route keyed by `id` = `refs.toolCallId`.
- R5a adds `tool calls | (seq, id)`. R5d states that the history boundary does
  not filter the tool-calls collection or its page flags (TC13). This contract
  does not change R5d's rule for transcript messages.
- R6 whitelist adds `tool calls | afterMessageSeqFromInclusive,
  afterMessageSeqToExclusive`, and its bounded-filter sentence admits this
  integer pair for tool calls.
- R7 adds the `tool calls` field list (§5.3) and inserts `marker` after
  `messageType` in the transcript-messages list; R7m states the TR4 condition and
  TR5 reader rule.
- R8 seed adds `tool_call.started`, `tool_call.ended` (tool calls, upsert,
  `toolCallId` + `sessionKey`) and `transition.recorded` (transcript messages,
  upsert, `messageId` + `sessionKey`).
- AU4 table row "transcript messages, coordination share" becomes "transcript
  messages, tool calls, coordination share".

### 11.3 `rest-state-api-v1-wire-schema.md`

- Core stored resources gains the `tool calls` row: strings `id, sessionKey,
  harnessToolCallId, title, kind, toolName, status`; integers `seq, turnSeq,
  afterMessageSeq, startedAt, endedAt, rowVersion`; arrays and objects
  `truncated A<O<ToolCallTruncation>>`, `rawInput J`, `rawOutput J`, `content J`;
  nullable `toolName, rawInput, rawOutput, content, endedAt`.
- Transcript messages gain `marker O<TransitionMarker>`; the conditional-omission
  rule names `marker` beside `messageType` (TR4).
- Shared closed shapes add `ToolCallTruncation {field S, originalBytes I}` and
  `TransitionMarker {kind S, from S, to S}`.
- Enum domains add tool-call status `pending|in_progress|completed|failed`;
  `ToolCallTruncation.field` `rawInput|rawOutput|content`; marker kind current
  producer values `harness-switch|model-retune|session-restart|context-compacted`
  as a second open reader domain under TR5. Tool-call `kind` is an open string.
- Canonical order: `truncated` sorts by field in the order `rawInput`,
  `rawOutput`, `content`.

### 11.4 `cli-surface-v1.md`

No change. Under its demand rule no consumer has asked for a CLI read of tool
records; REST serves Chat. A later demand adds a wrapper by its own amendment.

## 12. Acceptance

Each item runs against a real gateway build of the integrated change, with real
Claude and Codex sessions on the pinned adapters, under the repository's
canonical test route. A synthetic adapter feed does not satisfy A1 to A5.

A1. Claude tool calls. Given a Claude session subscribed on Firehose with
`classes:["tool_call."]` and its `sessionKey`, when the operator sends a prompt
that makes it run a shell command and read a file, then: each call produces one
`tool_call.started` and one `tool_call.ended`; each ended payload shows the tool
name, the input and the result; `GET …/tool-calls` returns the same records
byte-equal to the payloads; and every record's anchor is at least that turn's
prompt `seq` and below the turn's reply `seq`. Covers TC1, TC2, TC8, TC9, TC10,
FH1, AS1, AS2, AS5.

A2. Codex tool calls. A1 repeated on a Codex session, with `toolName` null and
the shell call's `kind` and `title` as the adapter reports them. Covers the same
items for Codex. It reports the observed Codex result sizes and the share of
results the server cuts at 64 KiB; at around 5% or more, the bound is
reconsidered as a product question (§8).

A3. Compaction on both harnesses. Given a subscription with
`classes:["transition.","tool_call."]`, when the operator sends `/compact` to a
Claude session and then to a Codex session, then each session's transcript gains
one `context-compacted` marker, announced as `transition.recorded` and not as
`message.created`, and each gains one completed "Compact conversation" tool
record. Covers TR1, TR2, FH2, AS3, AS4.

A4. Other transitions. On real sessions, a model retune, an effort change, a
harness switch and a context reset each produce their existing marker kind,
announced as `transition.recorded`, with `marker` present in the REST item and
the notice payload. A subscriber of exactly `["message.created"]` receives none
of these live and sees all of them on a REST read. Covers TR4, FH2, §7.2.

A5. Rebuild after missed notices. Given a Chat-recipe client subscribed to all
four categories, when its connection is dropped and, while it is down, a Claude
and a Codex session each run tool calls and one compacts, then after reconnect it
subscribes first, reads the messages tail and the tool-calls collection, and its
model equals a fresh client's model built from REST alone, with records and
markers in TC11 order. Two further cases each rebuild the same way: (a) the
client reconnects while a Claude tool call is still running and before any reply
message exists, and the running call's record appears in the newest-slice
request; (b) a Codex turn is stopped after a tool call with no reply message, and
that record appears after the turn's prompt. Covers I2, P3, M2, TC11.

A6. On and off. A subscriber with `["message.created","session."]` receives no
tool or transition notice during A1 to A4. After unsubscribe and subscribe with
`"tool_call."` added it receives tool notices from that cut only. Covers FH4, §7.3.

A7. Size bound. A tool call whose result exceeds the bound is served as a prefix
string with a `truncated` entry naming the field and its original size; a call
within the bound has `truncated:[]` and its whole value. Covers TC14.

A8. Visibility. A principal denied a session's messages gets 404 on its tool-call
collection and detail and receives none of its tool or transition notices.
Covers TC12, I3.

A9. Unfinished call. A call interrupted by stopping the turn stays non-terminal
with null `endedAt`, and no `tool_call.ended` is emitted for it. Covers TC5.

A10. History boundary. On a real session, a turn is interrupted mid-call so its
record is anchored at the newest message, and the session then changes harness.
After the change, that record and every record anchored at or below the new
`clearedThroughSeq` are still returned by the collection, on a cursorless read
and along its `before` chain, and no page flag treats them as absent; the
`harness-switch` marker is visible; and the first post-change turn's tool calls
are present. Covers TC13.

A11. Late update to a record at or below the boundary. On a real session, a call
is interrupted so its record is anchored at the newest message, and the session
changes harness so `clearedThroughSeq` reaches that anchor. A terminal update
for that call is then committed (driven through the adapter seam if the harness
does not send one after the change). A subscriber whose classes include
`tool_call.` and that is otherwise eligible for the session receives one
`tool_call.ended` for it. Its payload is byte-equal to the detail route item and
to the record's item in the collection, found on a cursorless read or along its
`before` chain, both showing the terminal status. Covers FH1, FH5, the §7.1
emission cells, TC13.

## 13. Open questions

- Q1 (NON-BLOCKING, Chat client). Assistant text commits at turn end, so a
  turn's tool records sort before all of that turn's reply messages, even where
  the agent wrote text between tool calls. Changing this would change how turns
  commit text, which [L-turns] rules out. Is turn-level order enough for Chat?
- Q2 (NON-BLOCKING, Chat client, to settle before this contract is adopted).
  §7.2: markers move from `message.created` to `transition.recorded`. Does Chat
  agree to add `transition.` to its subscription in the release that ships this,
  or ask for a different shape?
- Q3 (NON-BLOCKING, product). A model change the harness reports on its own,
  without a Tightbeam retune, is seen by the adapter but not recorded (NG9).
  Should it become a transition later?
- Q4 (NON-BLOCKING, Chat client). Subagent tool calls are recorded flat, without
  a parent link (TC7). Does Chat need nesting?
- Q5 (CLOSED). Field bound: ruled 64 KiB per field on 2026-10-25 (§8).
- Q6 (NON-BLOCKING, sequencing). Under R-hist the reset-safe history amendment
  removes the history-boundary filter from transcript messages, including
  transition markers, in REST R5d and Firehose. This contract composes onto
  it and adds no rule of its own for messages (TC13). Integrated without that
  amendment, a tool record at or below the boundary would be served while the
  message it follows stays hidden. The settled order lands that amendment
  first.
