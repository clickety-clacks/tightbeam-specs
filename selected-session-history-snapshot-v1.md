# Selected-session snapshot in the history response amendment: v1

Status: PROPOSED, 2026-10-25.

This amendment changes three adopted contracts, read at public specs commit
`3c7af7fb933bef170da5a88cf47e8f6146b1e400`:

| Contract | SHA-256 at that commit |
|---|---|
| `rest-state-api-v1.md` | `eec1342919e206e2a9bc1e9297b8dd001fa6b4a7dd49e1d0a779fe61cd4dd9ed` |
| `rest-state-api-v1-wire-schema.md` | `0ce30766ff1d73e7d2aa8a2f233e86b603d5a3e6be2560a0dff07514f129d88b` |
| `transcript-verb-v1.md` | `80664c09e9d1fa94b3f156d6feb8dd49dd5460f23fc7513dfbae0b0aaca4c7d9` |

## 1. Spirit

The intent this amendment serves, from the governing product rulings:

- A chat client "needs one parameterized live subscription plus one paged
  history read, and an API gap is a server failure."
- "The server supplies an authoritative, current snapshot of the selected
  session in the history envelope ... After this, Chat can render the
  selected session from the history read and subscription alone and drops the
  extra GET. Chat adds no client workaround meanwhile."
- Not in scope: "new session fields beyond what the GET already returns,
  changes to other endpoints, removing GET /api/sessions/<key>, caching or
  push redesign."
- The history response is the carrier; the subscription readiness frame is
  unchanged.

## 2. Why the current contracts need this amendment

1. REST R4 fixes the list envelope as
   `{"schemaVersion":1,"resource":...,"items":[],"page":{...}}`. No clause
   allows a further top-level key on a collection.
2. REST R7c makes the wire schema normative for JSON types, nullability and
   nested keys. The wire schema defines no `session` key for the
   transcript-messages collection.
3. The `transcript-verb-v1.md` cold build fetches the session separately
   before the first history page (step 3) and after the last (step 5).

## 3. Terms

- **History response**: a successful response from
  `GET /api/sessions/:sessionKey/messages` (tail, `before` or `after` page).
- **Canonical session item**: the R7 `sessions` item for a session key, as
  returned in `item` by `GET /api/sessions/:sessionKey` for the same principal.

## 4. Requirements

### 4.1 REST R4f (new clause, after R4e)

> R4f. Each history response SHALL encode exactly `schemaVersion`,
> `resource`, `session`, `items`, and `page`, in that order, with
> `resource:"transcript messages"`. `session` SHALL be the canonical session
> item for the path's `sessionKey`, encoded by the same sessions serializer as
> `GET /api/sessions/:sessionKey`. It is never null, never a subset of the R7
> sessions fields, and contains no field that the session detail route does
> not return. The server SHALL read `session`, `items`, and `page` from the
> same committed state. Error responses are unchanged (R4c). The message
> detail route, `GET /api/sessions/:sessionKey`, and every other route are
> unchanged. `schemaVersion` remains `1`.

Serves: "an authoritative, current snapshot of the selected session in the
history envelope" and "render the selected session from the history read and
subscription alone". The full item, rather than a field subset, serves the
requirement that the history result match `GET /api/sessions/:sessionKey`,
and R7, which permits one sessions shape. It already contains `sessionKey`,
`rowVersion`, `displayName`, `ownerUserId`, `model`, `harness`, `state` and
`mechanicalStatus`, with their existing nullability (`ownerUserId` and
`model` nullable; the rest not).

The same-state rule serves "authoritative, current": the session and the page
describe one moment, so the client needs no second read. One ordinary read
transaction covering the session row and the page satisfies it.

### 4.2 Wire schema (addition, beside the ExecutionMap envelope definitions)

> Transcript-messages collection success responses are closed top-level
> objects in this key order: `{schemaVersion:I, resource:S,
> session:O<sessions item>, items:A<O<transcript message>>, page:O<Page>}`.
> `resource` is exactly `transcript messages`. `session` is not nullable.

Serves R7c: the route stays frozen only with a wire row.

### 4.3 transcript-verb cold build (steps 3 to 5 replaced)

Replace steps 3, 4 and 5 of the ordered cold-build handoff with:

> 3. Fetch the transcript tail. Record the response's `session` as `S0` and
>    its `rowVersion` as `V0`.
> 4. Page backward with `oldestCursor` only until the displayed slice is
>    complete.
> 5. Record the `session` of the last history response fetched in steps 3
>    and 4 as `S1`, and its `rowVersion` as `V1`. When step 4 fetched no page,
>    that response is the step 3 tail and `S1 = S0`. Accept the session
>    snapshot only if `V1 = V0`. Otherwise discard the candidate slice and
>    repeat from step 3.
>
> The comparison requires `S0` to describe a state no later than the first
> page and `S1` a state no earlier than the last page. A history response's
> `session` satisfies both, because R4f reads it from that page's committed
> state. A client that instead fetches `GET /api/sessions/:sessionKey`
> immediately before step 3 and immediately after step 4 also satisfies it.

Serves: "drops the extra GET". Steps 1, 2 and 6 to 8 are unchanged, so the
subscribe-first buffer cut and the `rowVersion` discard and advance rules
still hold, now keyed on the page-carried `S1`. The closing paragraph keeps
one comparison rule and states the condition both read routes meet, so
`external-agent-session-connect-v1.md`, which fetches the session around its
reads, stays conformant without edits. The CLI wrapper's existing envelope
parity (I3, I8, A7) carries `session` with no new rule.

## 5. Acceptance

A57 (REST, R4f). Given a visible session, one principal, and one running
gateway build, when the client reads `GET /api/sessions/:sessionKey/messages`
and `GET /api/sessions/:sessionKey` with no session commit between them, then
the history response's top-level keys are exactly `schemaVersion`,
`resource`, `session`, `items`, `page` in that order, and its `session` bytes
equal the detail response's `item` bytes. Within that same build, any two
such reads whose session `rowVersion` values are equal return equal bytes.
Across a gateway release, the wire schema's build-owned harness-catalog rule
still applies: `capabilities` may change without a `rowVersion` change, and
the fresh rebuild's value is authoritative. Given a session with no messages,
the history response still carries `session`. Given an unknown or forbidden
session key, the response is the existing R4c `not_found` body, with no
`session` key.

Example: session `rowVersion` 41, `ownerUserId` "alice", `model` null. The
tail page returns `session.rowVersion:41`, `session.ownerUserId:"alice"`,
`session.model:null`, byte-equal to the detail `item`.

A58 (REST, R4f same state). Given a committed advance of the history boundary
to `F'` whose boundary marker appears on a page, then that response's
`session.clearedThroughSeq >= F'`. A server that reads the session row,
`items`, and `page` in one ordinary read transaction satisfies R4f's
same-state rule; this check runs on committed state and needs no concurrent
writer or timing harness.

A11 (transcript-verb, steps 3 to 5). Given a firehose subscription that is
ready, when a client cold-builds a three-page slice, then it records `S0`
from the tail response, pages back twice, records `S1` from the third
response, accepts when `V1 = V0`, and sends no
`GET /api/sessions/:sessionKey`. Given a session commit between the tail and
the third page, then `V1 != V0`, the client discards the slice and repeats
from step 3 with a new tail. Given a slice complete in the tail alone, then
step 4 fetches nothing, `S1 = S0`, and the client accepts from one response.
Given the buffered notices of A5, then step 7 discards and advances against
the page-carried `S1` exactly as A5 states. The `transcript` CLI output
carries the same `session` bytes as REST.

## 6. Assumptions

- AS1. Existing readers of the history response ignore an unrecognized
  top-level key. If a current consumer rejects one, the change is not
  additive and needs a new namespace per R1.
- AS2. Any principal who can read the messages collection can read the
  session detail (AU4, AU5 nested-route visibility). If not, R4f would expose
  a session item the principal cannot otherwise see.

## 7. Non-goals

- The subscription readiness frame (`subscription_ready`) does not carry a
  session.
- No new session fields; no change to the R7 sessions row or its wire row.
- No change to `GET /api/sessions/:sessionKey`, the message detail route, or
  any other endpoint. The session GET is not removed.
- No caching, push, or firehose change.

## 8. Design choices

- The response carries the full canonical session item, not only the fields
  a chat client reads, because R7 permits one sessions shape and the result
  must match the session GET.
- The same-state rule is met by one read transaction; the mechanism is an
  implementation choice.

## 9. Implementation notes

- In the success path of `GET /api/sessions/:sessionKey/messages`, encode
  `session` between `resource` and `items` with the existing sessions
  serializer, using the session row already resolved for the visibility
  check, read in the same transaction as the page.
- Error paths, the message detail route, `subscription_ready`, the session
  GET, caching and push stay as they are.
- The `transcript` CLI wrapper passes the REST envelope through. If it
  rebuilds the envelope from known keys, it passes `session` through
  unchanged.
- Tests that assert the four-key messages envelope move to the five-key form.
