# Event firehose v1 — the external event stream (product spec, r2.1)

Status: DRAFT r2.1, 2026-08-20. r2.1 adds §Client workflows (rationale) per
Mike's changelog comment: the cursor as a stable scroll-back point, and the
workflows the protocol exists to support, written into the doc as the why. r2 folds Mike's nine review comments from the
r1 reading copy (artifact comments pulled 2026-08-20): observability
framing corrected, class vocabulary enumerated in-doc, tail and
scroll-back history reads added, per-view cursors clarified, the read-only
boundary restated with the chat-client pattern, MQ1 ruled (full payloads),
MQ2 and MQ3 rewritten as plain discussions. Untargeted (0.2.0 or later,
undecided). When build work starts it branches from main tip; ws is
orthogonal enough that merge timing is unconstrained (Mike, 2026-08-20).

Authority and inputs:
- Mike's firehose ruling (tightbeam-decisions.md 2026-08-20): the live
  event stream is PART of the observability layer — the pushed part. The
  other parts already exist: the CLI's reads (toplines, traces, attests)
  and direct read-only state-db queries. EVERY substrate event streams out
  of this endpoint; filters narrow what a subscriber receives and never
  gate what is streamable; any future UI or agent is a consumer.
- Mike's auth ruling (same day): no capability/API-key system; a consumer
  authenticates with the requesting user's existing gateway credential;
  deployment is localhost or tailscale; revocation is existing session and
  device revocation. Replay has no admission limit.
- Mike's payload ruling (r1 comment, 2026-08-20): frames carry everything —
  a client must be able to display content straight off the stream without
  an independent query per event. See V3.
- Input, not authority: the archived focused design
  (archive/filtered-external-push-subscriptions-recon-v3.md) and draft spec
  (archive/focused-external-subscriptions-v1-draft.md). Their durable-row,
  cursor, epoch, and pump mechanics are reused; their single-class
  vocabulary, capability system, and redacted frames are superseded.
- observability-v1.md r4: unchanged and complementary. Its doorbells are
  thin best-effort UI nudges on the existing chat wire, tolerating loss
  because reads recompute. The firehose is the complete durable feed on its
  own endpoint. Both exist; neither replaces the other.

## Goal

G1. Tightbeam SHALL provide one WebSocket endpoint from which every
substrate event streams to external consumers as it commits.

G2. A consumer SHALL be able to read history three ways: resume from a
cursor and receive everything missed in order without loss; fetch the
newest N events to boot cold; and page backward from any point for
scroll-back. The cursor's job for a UI is marking NEWNESS — an event after
the client's saved cursor is "new to the user" — not gatekeeping how
history is fetched.

G3. A subscription MAY carry filters. Filters narrow delivery for that
subscriber only. Nothing is excluded from the stream itself.

G4. The endpoint SHALL serve any consumer the gateway can authenticate as a
user: a dashboard, ATC, a script, another agent.

## Non-goals

N1. No capability or API-key system, no key expiry, no key wire. Ruled out
2026-08-20. If a less-trusted consumer ever becomes real, scoped keys are a
later versioned addition.

N2. Nothing is sent INTO Tightbeam on this socket. The firehose is
one-directional: server to client, plus the client's subscribe/history
requests. A chat-shaped client is a legitimate consumer and the pattern is
explicit (Mike, r1 comment): it SENDS by calling the normal gateway verbs
(wake to message a session), and it SEES the effect come down this stream
as the resulting events (`wake.scheduled`, the turn and message classes).
The existing Clawline chat wire is untouched by this spec.

N3. No state snapshots on this endpoint. Current state comes from the
existing query surface (CLI verbs, observability-v1 queries). The firehose
carries events only; the consistency recipe is §Subscribe-then-query.

N4. No delivery judgment. The substrate never decides an event is
uninteresting. Interruption shaping is the consumer's business (philosophy
gate 5: shape WHEN attention is spent, never WHAT is recorded).

N5. No webhooks, SSE, or polling interface in v1. Later versioned additions
if needed.

N6. This spec does not authorize implementation. It exists so Mike can
interrogate the design before any build card is cut.

## Terms

T1. **Event** — one committed substrate happening, recorded as one durable
row: a verb accepted or denied, a lifecycle transition, a rail denial, a
row-changing fact (work item created, assignment opened, attest filed, wake
scheduled or fired, turn started or ended), a marker, a boot or shutdown.

T2. **Class** — the event's namespaced kind string from the registry in
§The class registry. The set is OPEN: new substrate mechanisms mint new
classes freely, and the registry section is amended with them.

T3. **Seq** — the event's position in the single total order, a
monotonically increasing integer assigned at commit.

T4. **Epoch** — 128 CSPRNG bits, base64url. Identifies one continuous
history of the store. Rotates only on restore-from-backup.

T5. **Cursor** — a checkpoint: `(epoch, seq)`, a position in the one global
order. Cursors are PER VIEW, not global: a client keeps one cursor for each
filtered subscription it cares about — one for its all-events view, one for
"events from this agent," one for "events on this work item" — and may hold
any number. Every cursor is encoded the same way and is valid with any
filter set, because the seq underneath is the same global order; a filtered
view simply skips the rows its filter excludes while the cursor advances
past them.

T6. **Pump** — the serialized server process that drains durable rows to
connections. Reused from the archived design.

## The event vocabulary law

V1. Every substrate happening that commits SHALL publish exactly one
firehose event row, written in the same transaction as the fact it records.
A happening with no row does not exist to observers; a row written outside
the transaction can be lost or orphaned. Both are defects.

V2. Classes are namespaced `area.happening`, lowercase, dot-separated. The
registry below is part of this spec (Mike, r1 comment: classes are called
out in-doc, not deferred). A class name never changes meaning. The
acceptance test A1 proves the registry matches what the substrate actually
emits, so registry drift is a red build, not a doc rot.

V3. **RULED (Mike, r1 comment):** the payload is everything — the full
recorded truth, the same fields the substrate wrote, unredacted, sufficient
for a client to display the event without an independent query. The reader
is the authenticated user on their own gateway; there is nothing to hide
from them.

V4. Frame shape:

```json
{
  "type": "firehose_event",
  "schemaVersion": 1,
  "eventId": {"epoch": "fhe_...", "seq": 40213},
  "class": "attest.filed",
  "occurredAt": 1786900000000,
  "refs": {"sessionKey": "...", "workItemId": "wi_...",
           "assignmentId": "asg_...", "origin": "...", "principal": "..."},
  "payload": { }
}
```

Every field above the payload is stamped by the substrate. `refs` carries
whichever reference ids the event has; absent refs are omitted. One
schemaVersion keeps one meaning; widening the frame bumps it.

## The class registry (initial enumeration, derived from main tip)

R1. Work:
`work_item.created`, `work_item.updated`, `work_item.iceboxed`,
`work_item.reopened`, `work_item.closed`, `work_item.failed`,
`assignment.opened`, `assignment.reopened`, `assignment.closed` (outcome
completed | revoked | surrendered-while-it-exists in payload),
`attest.filed` (kind and verdictKind in payload).

R2. Attention and escalation:
`wake.scheduled`, `wake.fired`, `wake.canceled`, `prod.fired`,
`turn.started`, `turn.ended`, `decision_request.opened`,
`decision_request.ruled`, `decision_request.withdrawn`.

R3. Org shape:
`session.spawned`, `session.retired`, `role.created`, `role.bound`,
`role.removed`, `user.added`, `device.approved`, `device.denied`,
`device.revoked`.

R4. Records: `artifact.recorded`.

R5. Dispatch: `verb.accepted`, `verb.denied` — one per gateway verb call,
every verb in the router's vocabulary, with the verb name, origin, and
principal in payload/refs. These are the catch-all: a happening whose fact
class is missing still surfaces here, which is how A1 catches registry
gaps.

R6. Rails and lifecycle: `rail.denied`, `lifecycle.boot`,
`lifecycle.clean_shutdown`, `lifecycle.dirty_exit` (recorded by inference
at the next boot — no component claims to log its own death),
`lifecycle.takeover`.

R7. This enumeration is derived from main tip's row vocabulary as of
2026-08-20. The build card verifies it mechanically (A1) and amends this
section where reality disagrees; new mechanisms amend it as they mint
classes.

## Connection and auth

C1. The endpoint is a WebSocket upgrade on the gateway's existing HTTP
listener, at its own path, separate from the chat socket.

C2. Auth is the existing gateway credential flow, authenticating the
requesting user, identical in mechanism to the current socket auth. No new
credential type. A failed auth closes with the existing auth failure
behavior.

C3. Transport posture matches the deployment ruling: localhost or tailscale.
TLS termination, if any, is the operator's reverse proxy, exactly as today.

## Subscribing

S1. After auth, the client sends one subscribe message:

```json
{
  "type": "subscribe",
  "protocolVersion": 1,
  "cursor": "fhc_v1_...",
  "tail": 50,
  "filters": {
    "classes": ["attest.", "work_item."],
    "sessionKey": null,
    "workItemId": null,
    "origin": null,
    "principal": null
  }
}
```

S2. `filters` and every field in it are optional. `classes` entries match by
prefix against the registry. Multiple given fields are conjunctive. No
filters means everything.

S3. `cursor` is optional. Omitted means "from now": the registration cut is
the durable head read during serialized registration (the archived design's
AR148 mechanism, kept verbatim). Supplied means "replay after this cursor,
then go live."

S4. `tail` is optional and composes with an omitted cursor: the server
first delivers the newest `tail` matching events in chronological order,
then `subscription_ready`, then live delivery. This is the cold-boot read
(Mike, r1 comment): a booting client shows the last N items immediately,
uses its SAVED cursor only to mark which of them are new to the user, and
scroll-back is §History below. `tail` with a supplied cursor is
`invalid_request` — they answer the same question two ways.

S5. `{"seq": 0}` at the current epoch is a lawful cursor: replay from the
beginning of retained history.

S6. The server answers `subscription_ready` carrying the cursor at which
live delivery begins (after any tail or replay completes). One subscription
per connection; changing filters is a new connection. Connections are cheap
on a local network, and a client holding several filtered views (T5) holds
one connection per view.

S7. There is NO admission or replay concurrency limit (Mike's OQ9 ruling:
no limit). Any number of consumers may replay any amount of history
concurrently.

## History (scroll-back)

H1. On an open subscription the client may request older events at any
time:

```json
{"type": "history", "before": "fhc_v1_...", "limit": 100}
```

H2. The server returns the `limit` matching events (this subscription's
filters) immediately older than `before`, in chronological order:

```json
{"type": "history_page", "events": [ ... ],
 "olderCursor": "fhc_v1_...", "atFloor": false}
```

`olderCursor` points at the oldest event returned and is a lawful `before`
for the next page; `atFloor: true` means retained history is exhausted.
History pages never move the subscription's live position.

H3. The intended UI shape (Mike, r1 comment): boot with `tail`, mark
newness against the saved per-view cursor, page backward with `history` as
the user scrolls. The cursor is never required just to fetch content.

## Client workflows (rationale, non-normative)

These are client concerns, outside the ws layer's purview — but the
protocol exists to make them buildable, and they are why the shapes above
are what they are (Mike, r2 comment).

W1. **Cold boot.** Subscribe with `tail: 50`. The last 50 events render
immediately; the saved per-view cursor marks which of them are unseen; live
events append. No query, no replay ceremony.

W2. **Jump to first unread.** The saved cursor is a stable position in the
global order, not an offset — so "scroll up to where unseen starts" is:
page backward with `history` from the live head until the page spans the
saved cursor, land the viewport there. Offsets would rot as events arrive;
a position does not. This workflow is why the cursor is `(epoch, seq)`.

W3. **Resume after disconnect or sleep.** Subscribe with the saved cursor;
everything missed arrives in order, then live delivery continues. The
client cannot tell a laptop-lid nap from a gateway restart, and does not
need to.

W4. **A chat client.** Send by calling the normal gateway verbs (wake);
watch the effect arrive on the stream (`wake.scheduled`, turn and message
classes). Filter the subscription to the session in view; keep one cursor
per conversation view for unread marking (T5, W2).

## Delivery semantics

D1. Delivery is at-least-once, in seq order, per connection. An ambiguous
network break may repeat an event; it never loses one.

D2. The client dedupes by `(epoch, seq)` and persists its cursor only after
applying the event. (Archived AR160–AR162, kept.)

D3. The writer never touches a socket in the transaction: after commit it
sends a nonblocking nudge; the pump drains durable rows. A missing or
crashed pump never invalidates a row. A 30-second heartbeat compare of
drained-vs-durable head catches lost nudges. (Archived AR139–AR145,
AR163–AR164, kept.)

D4. Slow consumer: each connection has a bounded in-memory queue. On
overflow the server closes THAT connection with close code 4008 and the
last-delivered cursor in the close reason. The client reconnects and
replays; nothing is lost because the rows are durable. This is not an
admission limit; it is the only alternative to unbounded server memory.

D5. Decimation: kill the gateway mid-stream and every consumer resumes from
its cursor on restart with zero loss. Kill a consumer and the substrate
does not care.

## Subscribe-then-query (the consistency recipe)

Q1. A consumer that needs current STATE plus updates SHALL: (1) subscribe
with no cursor and receive `subscription_ready` with cursor K; (2) query
current state through the existing query surface; (3) apply events after K,
deduping against what the query already showed. Events between subscribe
and query are duplicates by construction, and D2 handles duplicates. A
consumer that only displays the event feed itself needs none of this —
`tail` plus live delivery is complete (S4).

## Cursors

K1. Cursor encoding (this spec exercises the OQ10 delegation): the
documented prefix `fhc_v1_` plus unpadded base64url of canonical UTF-8 JSON
`{"epoch":"...","seq":N}`. The decoder rejects extra fields, non-canonical
encoding, negative or non-integer seq, and unknown prefixes, all as
`cursor_invalid`. Decoding stays backward compatible across versions: a
`fhc_v1_` cursor decodes forever.

K2. A well-formed cursor with a non-current epoch is `cursor_expired`. The
client re-enters via Q1 or a fresh `tail` subscribe.

K3. A cursor whose seq is below the retention floor is `cursor_expired`,
same recovery.

K4. A supported restore-from-backup rotates the epoch before the store
serves any read or write, so a stale-history cursor can never silently
resume against rewound truth. (Archived AR136–AR138, kept.)

## Storage

ST1. One append-only table, one AUTOINCREMENT seq, rows written in the
committing transaction (V1). Whether the existing internal EventLog tables
fold into it is MQ2 below.

ST2. Retention: v1 retains everything. The `cursor_expired` machinery (K3)
exists so a retention horizon can be added later as a config change, not a
contract change. Plain version in MQ1 below.

## Errors and close codes

E1. Before the HTTP-to-WebSocket upgrade handshake completes (the "upgrade"
is the HTTP request that switches the connection into a WebSocket): existing
HTTP auth failures as today; `426` for an unsupported protocolVersion.

E2. After upgrade, one closed error frame shape
`{"type":"error","code":"...","message":"..."}` with codes:
`invalid_request` (malformed subscribe/history, or tail+cursor),
`cursor_invalid` (K1), `cursor_expired` (K2, K3).

E3. Close codes: 4008 slow-consumer (D4, cursor in reason), 1012 restarting
(gateway shutdown; resume by cursor), plus the standard codes.

## Acceptance

A1. Every row-writing verb on main tip produces exactly one firehose event
in the same transaction, and every emitted class appears in this spec's
registry — proven by a test that diffs the verb table and emitted classes
against §The class registry both ways.

A2. Kill -9 the gateway under sustained writes; on restart a consumer with
a pre-kill cursor replays to head with no gap and no duplicate it cannot
dedupe.

A3. A filtered subscriber (class prefix + workItemId) receives exactly the
matching events and its cursor still advances past non-matching seqs (a
filter must not strand a cursor).

A4. A consumer executing Q1 arrives at state identical to a fresh query at
any quiescent moment.

A5. A slow consumer forced into 4008 resumes by cursor with zero loss.

A6. A cold-boot client using `tail` then `history` renders the same event
sequence a cursor-zero replay would, in the same order.

A7. The feature-smoke drives one real external consumer (ATC or a script)
end to end.

## Open questions for Mike

MQ1 (was MQ2). **Retention, plainly.** Every event is a database row and
they accrue forever — every wake, every turn, every attest, from now on.
The question is only: do we ever delete old ones? I propose NO — keep
everything until table growth is a measured problem someone brings back
here with numbers. Saying yes costs nothing today, and the expired-cursor
machinery (K3) already handles a future "we only keep 90 days" as a config
change. Confirm keep-everything, or set a horizon now.

MQ2 (was MQ3). **One event table or two systems, the discussion.** Main
already has internal append-only tables recording some of this (verb calls
and denials, lifecycle transitions, rail denials — the EventLog, written
for observability, currently with no consumer). The firehose needs its own
single-seq table (ST1). Two ways to relate them: (a) FOLD — the firehose
table becomes THE event log; the old tables' writers write firehose rows
instead, old tables retire. One source of truth, one seq, matches the
"state is computed from rows" philosophy; costs a migration of the writer
call sites. (b) BESIDE — the old tables stay, their writers dual-write a
firehose row too. No migration, but the same happening then has two rows in
two places that can drift, and drift between two records of truth is a
standing bug factory. My recommendation: FOLD, with dual-write only as a
short transition state inside the build. Rule (a), (b), or leave it to the
build card.
