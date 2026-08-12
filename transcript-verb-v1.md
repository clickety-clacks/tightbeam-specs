# Transcript verb — v1

Status: DRAFT r5 (2026-07-26). Flynn-directed: "tightbeam transcript
'session-id' from startmessageid to endmessageid … maybe [reading] from the chat
database instead of having to surface the claude or codex one", with two design
rulings: (1) SEPARATE flags for session key vs display name — a name resolves to a
CHOICE, never to content; (2) BEFORE/AFTER cursors with tail-by-default, never
absolute from/to — every cursor a caller passes is an id a previous response handed
it.

## Why the substrate's own rows, not the harness transcript file

The conversation is ALREADY substrate truth: an accepted prompt is one transaction
committing its `messages` echo AND its `turns` row together, and only an
`{:appended}` echo enqueues a turn (gateway.ex:833-847). Each assistant reply is a
`messages` row linked to its prompt by `replyToMessageId`
(gateway.ex:1245-1252) — the same rows the client renders. Reading them is a QUERY
over existing durable state (Law 0: no new recordkeeping). The harness transcript
file is rejected as the source for four reasons, any one sufficient:

- **Format churn** — harness CLIs auto-update under us; a verb built on their
  private layout inherits that churn.
- **Satellite locality** — a satellite session's harness file lives on the REMOTE
  host; a local path is useless exactly when placement did its job. The rows are
  already on the gateway.
- **Authorization granularity** — a file path grants whatever the whole file holds;
  rows are filtered per session against owner/admin.
- **T-PARITY cost** — reading harness files means a harness callback with manifest
  vectors. Not worth it for a need the substrate's own rows already serve.

SCOPE, stated honestly: this returns the CLIENT-VISIBLE CONVERSATION (prompts +
replies + their linkage), NOT the agent's internal tool calls or thinking — the
persisted message shape contains conversation fields, not either of those
(projection.ex:33-46). "What did the agent actually DO" is answered by
`work-item-trace` plus forensics. A future harness-file pointer (metadata only,
local sessions only) is NAMED and DEFERRED — build it only when something concrete
needs it.

## The history barrier and page flags

`sessions.clearedThroughSeq` (org.ex:64-89, default 0) is the per-session visibility
floor: rows at or below it are RETAINED but never served — replay already floors its
scan at `min_seq` (projection.ex:162-191), fed from the session row
(wire/socket.ex:310-320). The substrate advances it at two sites today: a harness
change sets it to the current MAX(seq) so the new engine gets a fresh visible slate
(gateway.ex:2700-2712), and turn-failure recovery sets the old session's barrier to
the failed prompt's seq (gateway.ex:3742-3758).

Let `V` be the target session's messages with `seq > clearedThroughSeq`, ordered by
`seq` ascending. Every mode selects only from `V`:

- tail selects the last `limit` rows of `V`;
- `--before C` selects the last `limit` rows of `V` whose seq is below C's resolved
  seq;
- `--after C` selects the first `limit` rows of `V` whose seq is above C's resolved
  seq.

Every non-empty page is returned oldest-first. Its `hasMoreBefore` is true exactly
when a row of `V` exists below the returned `oldestId`; its `hasMoreAfter` is true
exactly when a row of `V` exists above the returned `newestId`. Therefore:

- a tail page always has `hasMoreAfter: false`: it already contains the newest
  visible end;
- a `--before` page has `hasMoreAfter: true` whenever newer visible rows exist above
  that page, including the visible cursor row itself;
- an `--after` page has `hasMoreAfter: true` only while visible rows remain above
  its returned `newestId`;
- an empty tail has both flags false; an empty `--before` page has
  `hasMoreBefore: false` and `hasMoreAfter: (V is non-empty)`; an empty `--after`
  page has `hasMoreBefore: (V is non-empty)` and `hasMoreAfter: false`.

This makes both flags barrier-relative. Cleared rows never make either flag true.
In particular, when only cleared rows remain below a page, `hasMoreBefore` is false;
reporting otherwise would advertise history the caller can never page to.
`--name` candidates likewise compute `lastActivityAt` from visible rows only.

Returning cleared rows would expose durable history the client itself no longer
shows. An admin-only `--include-cleared` is NAMED AND DEFERRED — the forensic value
is real, but it is a second authorization question and v1 does not open it.

## The two entry points (Flynn ruling 1: never guess)

**`transcript --session <key>`** — retrieval. Exact key, goes straight to the rows.
Session STATE never gates retrieval: `Org.get/2` fetches by key without a state
predicate (org.ex:270-278), and this verb retains that property. An authorized
caller can read a retired session through `--session`.

**`transcript --name <display-name>`** — LOOKUP, never content. Returns the
candidate set `[{sessionKey, displayName, state, ownerUserId, lastActivityAt}]`
over `sessions.displayName` (org.ex:64-89), filtered by the SAME visibility rule as
retrieval, so lookup cannot enumerate sessions the caller may not read. Match is
CASE-INSENSITIVE SUBSTRING with `%` and `_` treated LITERALLY (escaped, never as
wildcards). RETIRED sessions participate and carry their `state`; retirement is a
soft state flip that retains history (org.ex:486-505). Candidates are ordered by
`lastActivityAt` DESC then `sessionKey` ASC, where `lastActivityAt` is the timestamp
of the session's highest visible message seq, or the session's own `createdAt` when
it has none (`createdAt` is durable session data at org.ex:64-89). Zero matches →
empty list, not an error. Multiple matches → all of them. EXACT SINGLE MATCH →
still the candidate list, one row: **a name always resolves to a CHOICE, never to
content**, so no caller transcripts the wrong session on a near-match. The caller
re-calls with the key it now holds. The flags are mutually exclusive; supplying
both, or neither, is a usage error.

Candidate ordering is BEST-EFFORT DISPLAY DATA, not conversation ordering:
`lastActivityAt` is a stored timestamp and therefore can tie or regress even though
the message chosen for it is the highest visible seq. The seq-only discipline below
governs transcript entries, not this candidate ranking.

## Cursors (Flynn ruling 2: BEFORE/AFTER, tail by default)

Absolute from/to leaves a caller guessing ids it has never seen — a caller cannot
ask for the end of a conversation whose last id it does not know. Therefore:

- **No cursor → the TAIL**: the newest `limit` visible messages, returned
  oldest-first for reading. This is the zero-cursor common case.
- **`--before <messageId>`** → the page immediately OLDER than that id.
- **`--after <messageId>`** → messages NEWER than that id.
- `--limit N`, default 50, hard cap 500: a request above the cap is CLAMPED, not
  refused, and the clamp is observable in the returned count.
- Cursors are mutually exclusive. Every cursor is an id a PREVIOUS response handed
  the caller — the verb never requires an id the caller must invent.
- ORDERING: the stable monotonic key is `messages.seq`, an `INTEGER PRIMARY KEY
  AUTOINCREMENT` (projection.ex:33-35). `id` is a random string
  (`"s_" <> uuid4`, projection.ex:103), and `timestamp` can tie or regress;
  neither may order results.

Cursor resolution is EXISTENCE-based, not visibility-based. The implementation
looks up the retained `messages` row by id without a barrier predicate — the
existing projection lookup has exactly that shape (projection.ex:141-159) — then
requires that row's `sessionKey` equal the requested session. A same-session id
resolves to its seq even when `seq <= clearedThroughSeq`; only after resolution does
the visibility floor constrain the RANGE:

- `--before <id-at-or-below-barrier>` returns an empty page with null cursors and
  `hasMoreBefore: false`; nothing older is visible. Its `hasMoreAfter` follows the
  empty-page rule above.
- `--after <id-at-or-below-barrier>` returns visible rows above the barrier. A
  caller whose history is cleared between pages catches up from the id it already
  holds instead of becoming stranded.

After an empty `--before <id-at-or-below-barrier>` page, the way forward is
`--after <that same id>`; existence-based resolution accepts the retained id and
applies the barrier only to the returned range.

Refusal remains correct only when the id does not exist at all or belongs to another
session. Those two cases return the same byte-identical `not_found` body, containing
neither the supplied id nor any indication of which case occurred. They are never
silently treated as the tail. `before` selects by `seq < cursor_seq`,
descending-with-limit and then reverses for display; `after` selects by
`seq > cursor_seq`, ascending-with-limit; both ranges are floored at the barrier.
The response closes the loop: tail → `--before oldestId` walks back,
`--after newestId` catches up.

## Response shape (pinned)

`{sessionKey, displayName, messages: [entry], oldestId|null, newestId|null,
hasMoreBefore, hasMoreAfter}`. `oldestId` and `newestId` are the first and last
returned ids; every empty page has `messages: []` and both cursors null. The flags
still follow the mode-specific empty-page rules above. In particular, an empty
`--after` response means the caller is caught up, so it MUST retain the prior
`newestId` it passed and use that same id for the next catch-up request; replacing
it with the response's null cursor would strand continuation.

Each entry has this EXACT key set; missing or extra keys fail the schema test:

`{id, at, role, sender|null, content, attachments, replyToMessageId|null,
turnSeq|null, model|null, harness|null, assignmentId|null, jobRef|null}`

- `role` is the row's mandatory column, values exactly `user` | `assistant`;
  `content` is the row's content column (projection.ex:33-46) and the same key the
  client wire emits (wire/payloads.ex:95-107); `attachments` is the stored list
  (projection.ex:45-46, 270-283). A transcript omitting any of these would not be
  the conversation.
- `sender` is NULLABLE and VERBATIM from the row: device prompts store none,
  substrate deliveries store their origin, assistant replies store `"tightbeam"`
  (gateway.ex:1245-1251). No canonical agent handle is derivable for every session,
  so the verb reports what the row holds rather than inventing an encoding.
- `at` is the row's `timestamp`; it is display data, never an ordering key
  (projection.ex:33-46).
- Turn attribution join, pinned: a `user` entry joins on
  `turns.messageId = entry.id`; an `assistant` entry joins on
  `turns.messageId = entry.replyToMessageId`, and has no turn when that link is
  null. `turns.messageId` has no UNIQUE constraint (ledger.ex:37-50); the 0-or-1
  relationship is grounded instead in the production write invariant:
  `Gateway.deliver_prompt_in_txn/5` is the sole turn-bearing enqueue path and
  enqueues exactly once only after `Projection.append_in_txn/2` returns
  `{:appended}` (gateway.ex:776-810, 833-847). The production source has
  exactly one qualified `Ledger.enqueue_in_txn/2` call site, that Gateway call, and
  no `Ledger.enqueue/2` call site under `lib/` (gateway.ex:837; ledger.ex:136-139).
  No other production path may enqueue a turn for a message id. A source-structure
  test MUST assert those call-site counts so a second enqueue path cannot silently
  invalidate the 0-or-1 join.
- From the joined turn: `turnSeq`; `assignmentId` and `jobRef`, stamped at enqueue
  (ledger.ex:110-129); and `model` and `harness`, stamped at claim
  (ledger.ex:209-221). All attribution fields are null where no turn exists.
  Assistant/context/failure/recovery markers are message-only writes
  (gateway.ex:3760-3767, 4212-4263), and credential-transition messages are also
  message-only writes (gateway.ex:2985-3000), so they yield null attribution.
  Turns created before the attribution columns were added have null
  `assignmentId`/`jobRef`; the migration adds nullable columns without a backfill
  (ledger.ex:75-81). This mapping makes a transcript join straight into
  `work-item-trace` using the same stored turn attribution.
- Deliberately EXCLUDED: `deviceId`, `clientMessageId`, `replyToClientMessageId`,
  `llmVisibleMessageId` — client/harness correlation internals present in the
  message store (projection.ex:40-45), not conversation.

## Audit without duplication

Dispatch appends every successfully returned verb result into `events.payload`
(dispatch.ex:152-160; event_log.ex:101-119). That column holds `inspect/1` TEXT,
not JSON (`event_log.ex` `encode/1`), so a proof over it reads the inspected
string rather than decoding it. Today `events.payload` is write-only
observability at the application seam, while agents on the gateway host can read the
SQLite database directly (event_log.ex:19-28, 124-147; application.ex:43-49;
client_e2e/substrate.ex:1-12, 30-34). Elision therefore does not protect a secret
from an agent. It prevents UNBOUNDED STORAGE GROWTH — a second copy of every
transcript on every read, plus content in crash rows — and keeps the audit trail to
WHAT was read rather than WHAT was returned. Contract:

- `transcript` is registered in a RESULT-ELIDED verb set at the Dispatch seam — a
  closed set, like the handler table; any future read verb whose result must not be
  duplicated into observability joins it.
- For an elided verb, the successfully returned `"verb"` event's payload is
  `%{elided: true, params: <the call's params>, count: N}` — N is the returned
  entry/candidate count. The params ARE the access trail (which session or name,
  which cursor, which limit); no message content and no candidate rows appear in
  the payload.
- A denial event is NOT elided: its error map is useful audit and contains no
  transcript (dispatch.ex:147-156).
- A raised handler is distinct from both success and denial. Dispatch builds its
  kind-`"verb"` crash payload with
  `%{code: "server_error", message: Exception.message(exception)}`
  (dispatch.ex:162-165). For an elided verb, the crash event is ALSO elided: its
  payload is exactly
  `%{elided: true, params: <the call's params>, crash: true, code: "server_error"}`.
  That PAYLOAD never carries `Exception.message/1`. An exception message is an
  uncontrolled channel for whatever the handler was holding, so an elided verb
  cannot let one into durable storage. Implementers must classify the handler
  outcome, not key elision on event kind alone.
- SCOPE OF ELISION, stated exactly so the guarantee is not read wider than it is:
  it governs the AUDIT ROW only. Dispatch still builds the CALLER's returned error
  with `Exception.message/1`, so that error can carry the term the handler held.
  That is deliberate and unchanged — the caller has just passed authorization for
  exactly those rows, so it is content they were entitled to read, and narrowing
  the caller's error is a behavior change this spec does not authorize. A proof
  must therefore assert the payload's exact elided shape and the absence of
  content from it, and must not imply the returned error is content-free.

Rails still evaluate normally before the handler (dispatch.ex:95-124). The verb is
read-only in ITS OWN effects, and that is what "pure read" means here.

## Authorization and the non-target wire declaration

Session OWNER, via `sessions.ownerUserId`, or admin. Session and user principals
resolve by the same ownership/admin rules as `work-item-trace`
(work_items.ex:593-618). Every other principal and an unknown session key return
`not_found` with BYTE-IDENTICAL bodies; the handler owns both answers. `--name`
candidates are filtered by the identical visibility rule before returning.

`transcript` is a NON-TARGET agent verb. This is a LOCAL declaration about this verb:
it has no legitimate top-level typed-target use. It does not depend on, preempt, or
prejudge `router-existence-oracle-v1`'s general question of whether point-addressed
existence is org-visible.

The declaration belongs in the ROUTER, not the handler. `/agent/dispatch` is the
sole generic agent-verb entry point, and it runs `typed_target` for every agent verb
before it constructs the handler call (wire/router.ex:110-127). `typed_target`
resolves a volunteered `sessionKey` through `Org.get/2`, returning an identifying
404 for an unknown key; it also has earlier generic refusals for the retired
`target` field and for multiple typed target fields (wire/router.ex:513-548). A
handler-side rejection is too late: the router can answer first. For a known key,
that resolution becomes `call.session_key` (dispatch.ex:61-69), which Dispatch
writes to `events.sessionKey` (dispatch.ex:152-165; event_log.ex:101-119).

The router therefore recognizes `transcript` as non-target BEFORE any typed-target
lookup or generic target-shape refusal. Supplying any top-level targeting field
(`sessionKey`, `role`, `userId`, or the retired `target`), alone or in combination,
to `transcript` returns HTTP 400 with error code `invalid_message` and message
`transcript takes no typed target`. The router map-encodes that error pair
(wire/router.ex:832-843); JSON object key order is not part of the contract. The
transcript-specific non-target refusal wins over both the generic retired-field
refusal and the generic multiple-target-fields refusal. Response bytes are identical
for an unknown key, an existing session the caller may read, an existing session the
caller may not read, retired `target` syntax, and multiple targeting fields; the
router never queries the volunteered target's existence. The legitimate retrieval
key travels only as the ordinary body param `params.session_key`, exactly as
`work-item-trace` carries `work_item_id`; the CLI maps `--session` to params.
Consequently `call.session_key` and the events row's `sessionKey` column are nil for
this verb; the audited session lives in the elided params.

## Non-goals

No harness transcript files. No tool-call or thinking capture. No new tables,
columns, or emission — a pure read over `messages`/`turns`/`sessions`. No full-text
search. No mutation of any kind.

## Required proofs

All automated; each must fail when the behavior it names is broken.

1. Tail default: no cursor returns the newest `limit` visible rows, oldest-first,
   with correct `oldestId`/`newestId`, `hasMoreBefore: true` on a longer session,
   and `hasMoreAfter: false`.
2. Paging: `--before` walks strictly older and `--after` strictly newer. Paging the
   whole session with `--before oldestId` visits every visible message exactly once
   and terminates with `hasMoreBefore: false`; every before page with newer visible
   rows has `hasMoreAfter: true`. After pages assert `hasMoreAfter: true` while rows
   remain and false when caught up. An empty caught-up `--after` response has
   `messages: []`, null `oldestId`/`newestId`, and `hasMoreAfter: false`; the test
   retains the previously passed `newestId`, appends a row, and proves that reusing
   that retained id returns the new row.
3. Seq ordering under hostile timestamps: rows written directly with EQUAL
   timestamps and a REGRESSED timestamp order by `seq` in every mode, and paging
   across them neither skips nor duplicates. An implementation ordering by
   `timestamp` or `id` fails this proof.
4. Cursor refusal: an id from another session and a nonexistent id receive
   byte-identical `not_found` bodies containing neither id; neither is silently
   treated as the tail.
5. Barrier: after advancing `clearedThroughSeq` mid-history, tail/`--before`/
   `--after` never return a row at or below it; both flags ignore cleared rows;
   `hasMoreBefore` is false when only cleared rows remain below the page; a row
   committed above the barrier is served; `--name`'s `lastActivityAt` reflects only
   visible rows. The proof first receives a page and holds its `oldestId` and
   `newestId`, advances the barrier through those rows, commits newer rows, then
   re-pages with the held cursors: `--before heldOldestId` returns an empty page
   with null cursors and `hasMoreBefore: false` (and `hasMoreAfter: true` while the
   newer visible rows exist), while `--after heldNewestId` returns the rows above
   the barrier and computes `hasMoreAfter` from any rows still above that page.
6. `--name`: exact single match returns a ONE-ROW candidate list, never content;
   partial and zero matches; a stored name containing `%` is found by literal
   match while `%` in the query does not wildcard; retired sessions appear with
   `state`; ordering is `lastActivityAt` DESC and then `sessionKey` ASC when
   timestamps tie; a regressed highest-visible-seq timestamp demonstrates that this
   is best-effort display ordering, not seq ordering; both flags together, and
   neither, are usage errors.
7. Authorization and wire non-targeting: owner and admin read, including a retired
   session through `--session`; a non-owner principal and an unknown params key
   receive byte-identical `not_found`; `--name` candidates exclude sessions the
   caller cannot read. The legitimate wire call carries the key in body params,
   has no typed target, and its `events.sessionKey` is nil. Three volunteered
   top-level `sessionKey` calls — unknown, existing-and-visible, and
   existing-but-forbidden — plus retired `target` syntax and a multiple-target-field
   call all receive the `invalid_message` / `transcript takes no typed target` pair
   before dispatch. Their raw response bodies are byte-identical, and none emits a
   verb event.
8. Schema and attribution: entries match the pinned key set exactly; missing or
   extra fails. A `user` entry carries its turn's
   `turnSeq`/`model`/`harness`/`assignmentId`/`jobRef`; an `assistant` entry carries
   its prompt's turn attribution via `replyToMessageId`; a message with no turn
   carries nulls throughout. Marker and credential-transition messages have null
   attribution, and a pre-attribution-column turn has null `assignmentId`/`jobRef`.
   A source-structure assertion proves the only qualified
   `Ledger.enqueue_in_txn/2` call under `lib/` is gateway.ex:837 and that no
   `Ledger.enqueue/2` call exists under `lib/`; adding either second production
   enqueue path fails the proof.
9. Limit: default 50; a request above 500 is clamped, observable in the returned
   count.
10. Elision: after a successful read, the `events` row for the call carries
    `elided: true`, the call params, and the count, while its `sessionKey` is nil. A
    distinctive message body present in the response appears NOWHERE in the
    payload; this is fail-before/pass-after against un-elided Dispatch. A denied
    call's event remains un-elided. Force the transcript handler to raise while it
    holds a row containing a different distinctive body string: the kind-`"verb"`
    crash event has exactly `elided: true`, the call params, `crash: true`, and
    `code: "server_error"`, with no `message` key, and the distinctive body appears
    NOWHERE in its payload. The crash assertion is fail-before/pass-after against
    the un-elided `%{code: "server_error", message: Exception.message(exception)}`
    row.

## Component touches

`Tightbeam.Transcript` (new read module over `messages`/`turns`/`sessions`),
gateway verb registration, the verb added to the router's agent-verb set and local
non-target declaration (wire/router.ex:46-48, 110-127, 515-548), the result-elided
verb set at the Dispatch seam (dispatch.ex:145-168), CLI command +
`cli-surface-v1` row, tests. NO schema, NO migration, NO emission, NO harness
surface. Depends on job-trace v1 (merged) for the turn attribution columns the
entries carry.
