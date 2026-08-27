# Transcript CLI wrapper — v1

Status: G5 reconciliation candidate, 2026-08-27. Mike's firehose gap
remediation ruling makes REST/transcript authority reconciliation a read-side
firehose prerequisite. When this exact candidate passes independent review and
lands, it supersedes the prior `transcript-verb-v1.md` lookup, projection,
history-floor, response-envelope, and message-id cursor clauses. Git history
retains those clauses as implementation history; they do not remain a second
public contract.

Authority: `rest-state-api-v1.md` owns the conversation query, item,
authorization, visibility-floor, page, and cursor semantics.
`event-firehose-v1.md` owns freshness and gap detection. This file owns only
the `tightbeam transcript` CLI mapping and its presentation.

The exact G5 candidate is the five-file set `transcript-verb-v1.md`,
`rest-state-api-v1.md`, `event-firehose-v1.md`,
`rest-vs-cli-adjudication.md`, and `cli-surface-v1.md` at one git commit.

## Goal

Provide one CLI command that reads the canonical REST conversation resources
without defining another lookup, message projection, history boundary, cursor,
or recovery rule. A client can use the same REST pages for cold start, backward
history, and recovery after a firehose gap.

## Non-Goals

- This wrapper adds no route, row, message field, query, serializer, mutation,
  notice class, event storage, replay, or stream cursor.
- This wrapper does not expose messages at or below the session's
  `clearedThroughSeq`.
- This wrapper does not specify physical deletion of durable message rows.
- This wrapper does not preserve the superseded case-insensitive substring
  lookup, five-field candidate projection, message-id cursor, or 12-field
  message projection.
- This wrapper does not use firehose notices as history. Firehose r6 stores no
  notice history and defines no retention horizon.

## Terms

T1. **REST history authority** — `GET /api/sessions/:sessionKey/messages`
under REST R4, R5, R5a, R5d, R7, AU4, and AU7.

T2. **Visible history** — the target session's R7 transcript-message rows whose
`seq` is greater than the session's current `clearedThroughSeq`, ordered by
`(seq,id)`.

T3. **History boundary** — `clearedThroughSeq`, the logical visibility floor
for one session. The boundary hides retained rows. It is not firehose
retention and is not a request filter.

T4. **Page cursor** — an opaque signed REST cursor returned as
`page.oldestCursor` or `page.newestCursor`. The cursor encodes the immutable
`(seq,id)` boundary plus REST request binding. It is not a message id.

T5. **Cold build** — subscribe first, then construct the displayed
conversation slice from REST while buffering post-subscription notices.

T6. **Gap recovery** — rebuild the displayed conversation slice from REST
after reconnect, a skipped firehose sequence, a session history-boundary
change, or a gateway restart reported by the connection.

## Assumptions

AS1. REST R7 exposes `seq` on each transcript-message item and
`clearedThroughSeq` on each session item.

AS2. REST R5 compares a decoded cursor tuple directly. Cursor validity does
not require the boundary row to remain present.

AS3. The separate session-freshness prerequisite from recon finding G2
supplies `session.spawned`, `session.updated`, and `session.retired` under the
`session.` subscription prefix. That prerequisite owns their mutation mapping;
this spec does not duplicate it.

AS4. Firehose M1 and M2 supply subscribe-first buffering, last-version-wins
application, gap detection, and full displayed-slice rebuild.

## Invariants

I1. REST is the sole public data authority for transcript lookup and
retrieval. The CLI does not query SQLite or call a second public query seam.

I2. `transcript --name <displayName>` performs the REST sessions collection's
exact Unicode-code-point `displayName` filter. It returns visible full R7
session items in `(createdAt,sessionKey)` order. It returns no message content.

I3. `transcript --session <sessionKey>` performs the REST transcript-message
collection read. Each returned item has the R7 transcript-message shape.

I4. The wrapper passes `before`, `after`, and `limit` to REST without decoding,
rewriting, or translating a cursor. It returns the REST R4 page object without
rewriting either cursor. A prior message id passed as a cursor receives REST's
`400 invalid_cursor`; the wrapper does not provide a compatibility alias.

I5. REST evaluates the history boundary on each message-page request. A page
contains only items whose `seq` is greater than the boundary used for that
request. The service reads the boundary, selects the items, and computes the
page flags as one indivisible read. A returned page reflects one boundary
value.

I6. `clearedThroughSeq` does not enter a cursor fingerprint because it is
server-owned state, not caller selection. A boundary advance does not make an
otherwise valid cursor malformed.

I6a. The observable `clearedThroughSeq` for one `sessionKey` is
non-decreasing. A session mutation cannot make a cleared message visible
again.

I7. A client uses `page.oldestCursor` as the next `before` value to walk
backward. It uses `page.newestCursor` as an `after` value only while the same
subscription connection remains established and its received sequence is
contiguous. Gap recovery starts from a fresh tail read.

I8. A successful machine-readable CLI response preserves the REST R4 envelope
and R7 items. A human renderer may select fields, add labels, or summarize
counts. It does not add a data field or cursor meaning.

I9. The wrapper preserves REST authorization, unknown-versus-forbidden
indistinguishability, error precedence, bearer credential, and `asUser`
principal selection. It does not implement a second visibility decision.

## Architecture

The final M4 wrapper has two modes:

| CLI request | Canonical read | Result |
|---|---|---|
| `transcript --name <displayName> [--before C | --after C] [--limit N]` | `GET /api/sessions?displayName=<exact>&before=C&after=C&limit=N` with absent options omitted | REST R4 sessions page containing full R7 session items and no messages |
| `transcript --session <sessionKey> [--before C | --after C] [--limit N]` | `GET /api/sessions/:sessionKey/messages?before=C&after=C&limit=N` with absent options omitted | REST R4 transcript-messages page |

The two selection flags remain mutually exclusive. The wrapper rejects a call
that supplies both or neither. `before` and `after` remain mutually exclusive.
REST supplies the default limit, cap, page order, cursor binding, and error.

REST emits `page.oldestCursor` for use only as `before` and
`page.newestCursor` for use only as `after`. A nonempty page sets
`hasMoreBefore` exactly when a visible row exists below its first item and
sets `hasMoreAfter` exactly when a visible row exists above its last item. A
cursorless tail sets `hasMoreAfter:false`. An empty cursorless tail sets both
flags false. An empty caught-up `after` page sets
`hasMoreBefore:(visible history is nonempty)` and `hasMoreAfter:false`.

For a valid message cursor whose tuple is at or below a newly advanced history
boundary:

- `before=<cursor>` returns an empty item list with
  `hasMoreBefore:false`; `hasMoreAfter` is true exactly when visible history
  exists above the boundary;
- `after=<cursor>` returns the first visible page above the boundary; and
- neither request resolves the cursor through a live message row.

Cold build uses this sequence:

1. Resolve or choose one `sessionKey`. Name lookup selects a key but builds no
   conversation state.
2. Establish a firehose subscription filtered to that `sessionKey`. The
   subscription includes `message.created` and the `session.` prefix supplied
   by recon finding G2. Receive `subscription_ready`.
3. Fetch the selected R7 session item and record its `clearedThroughSeq`.
4. Fetch the transcript tail. Page backward with `oldestCursor` only until the
   displayed slice is complete.
5. Fetch the session item again. If `clearedThroughSeq` changed, discard the
   candidate slice and repeat from step 3.
6. Inspect buffered session notices before accepting the slice. If one carries
   a different `clearedThroughSeq`, discard the candidate slice and repeat from
   step 3.
7. Apply buffered notices by the firehose M1 last-version-wins rule. Remove a
   cached message when its `seq` is at or below the accepted history boundary.

Operating-guidance impact: none. This product contract creates no agent
procedure outside the existing spec handoff.

Gap recovery repeats the cold-build sequence for the displayed slice. It does
not request firehose replay and does not treat an `after` page as proof that no
notice was lost.

Subtraction ruling: this revision deletes the duplicate transcript data
contract. Accepting both authorities keeps slice 2 blocked. Adding a cursor or
projection translation layer would create a third authority.

## Acceptance

A1 (I2). Given two readable sessions with one exact display name, a readable
case-only variant, a readable substring variant, and an unreadable exact
collision, when the caller runs `transcript --name` with the exact name, then
the CLI returns only the two readable exact-match full R7 items in
`(createdAt,sessionKey)` order. It returns no message item.

A2 (I3, I4, I5, I7). Given 1,205 visible messages with tied and regressed timestamps, when the
caller reads the tail and repeatedly passes each `page.oldestCursor` as
`before`, then the pages visit each visible `(seq,id)` once in ascending order
within each page and stop with `hasMoreBefore:false`. No request or response
uses a message id as a cursor.

A3 (I4, I6). Given a cursor returned before its boundary message is deleted, when the
caller requests the next page, then the server compares the decoded
`(seq,id)` tuple and returns the same page it would have returned while the
boundary row existed.

A4 (I5, I6, I7). Given a client that holds a tail page and its cursors, when
`clearedThroughSeq` advances through the held page and newer messages commit,
then `before=<held-oldest-cursor>` returns an empty item list with
`hasMoreBefore:false`, and `after=<held-newest-cursor>` returns only rows above
the new boundary. The before page sets `hasMoreAfter:true`. A cold rebuild
removes the held rows whose `seq` is at or below the new boundary.

A4a (I5, I7). Given nonempty visible history and a caught-up `after` cursor,
when the caller requests the next page, then the page is empty and sets
`hasMoreBefore:true` and `hasMoreAfter:false`. Given an `oldestCursor` used as
`after` or a `newestCursor` used as `before`, REST returns
`400 invalid_cursor`.

A4b (I6a). Given each production seam that can change the boundary, when that
seam would produce a candidate below the stored value, then the next session
read returns the stored value and no cleared message becomes visible.

A5 (I5, I6, I6a). Given a boundary advance between cold-build steps 4 and 5, when the client
re-reads the session item, then it observes the changed boundary, discards the
candidate slice, and repeats the REST build. The accepted slice contains no
row at or below the accepted boundary. Given a boundary advance after step 5,
then the buffered session notice produces the same discard and repeat.

A6 (I7). Given a firehose sequence skip after the client has paged three history
pages, when gap recovery runs, then the client subscribes first, refetches the
session and displayed message slice from a fresh tail, and converges after
buffered notices. The proof supplies no replay endpoint and no stream cursor.

A7 (I1, I3, I8, I9). Given the same principal and selection, when direct REST
and the CLI wrapper run successfully, then their R4 envelopes, R7 items, and
page cursors are equal. Given a REST refusal, the wrapper returns the same REST
error code without choosing a second authorization or cursor outcome. A source
check rejects SQL, a second serializer, a second visibility predicate,
message-id cursor conversion, and fallback to the legacy dispatch read after
M4 parity passes.

A8 (I4). Given a prior transcript message id in `--before`, when the M4 wrapper
runs, then REST returns `400 invalid_cursor`. The wrapper does not retry with a
legacy handler and does not convert the id.

## Open Questions

None. Mike's 2026-08-27 G5 ruling fixes the authority boundary and scope.
