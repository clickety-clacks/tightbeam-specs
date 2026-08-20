# Event firehose v1 — the external event stream (product spec, r1)

Status: DRAFT r1, written 2026-08-20 by tb02 for Mike's review. Untargeted
(0.2.0 or later, undecided). When build work starts it branches from main
tip; ws is orthogonal enough that merge timing is unconstrained (Mike,
2026-08-20).

Authority and inputs:
- Mike's firehose ruling (tightbeam-decisions.md 2026-08-20): the stream is
  the observability layer; EVERY substrate event streams out of it; filters
  narrow what a subscriber receives and never gate what is streamable; any
  future UI or agent is a consumer.
- Mike's auth ruling (same day): no capability/API-key system; a consumer
  authenticates with the requesting user's existing gateway credential;
  deployment is localhost or tailscale; revocation is existing session and
  device revocation. Replay has no admission limit.
- Input, not authority: the archived focused design
  (archive/filtered-external-push-subscriptions-recon-v3.md) and draft spec
  (archive/focused-external-subscriptions-v1-draft.md). Their durable-row,
  cursor, epoch, and pump mechanics are reused here; their single-class
  vocabulary, capability system, and privacy-redacted frames are superseded.
- observability-v1.md r4: unchanged and complementary. Its doorbells are
  thin best-effort UI nudges on the existing chat wire, tolerating loss
  because reads recompute. The firehose is the complete durable feed on its
  own endpoint. Both exist; neither replaces the other.

## Goal

G1. Tightbeam SHALL provide one WebSocket endpoint from which every
substrate event streams to external consumers as it commits.

G2. A consumer that disconnects SHALL be able to resume from a cursor and
receive every event it missed, in order, without loss.

G3. A subscription MAY carry filters. Filters narrow delivery for that
subscriber only. Nothing is excluded from the stream itself.

G4. The endpoint SHALL serve any consumer the gateway can authenticate as a
user: a dashboard, ATC, a script, another agent.

## Non-goals

N1. No capability or API-key system, no key expiry, no key wire. Ruled out
2026-08-20. If a less-trusted consumer ever becomes real, scoped keys are a
later versioned addition.

N2. No chat traffic. The chat/prompt wire and its doorbells stay on the
existing socket. The firehose is read-only observability.

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

T2. **Class** — the event's namespaced kind string, e.g.
`work_item.created`, `attest.filed`, `verb.denied`, `lifecycle.boot`.
The set is OPEN: new substrate mechanisms mint new classes freely.

T3. **Seq** — the event's position in the single total order, a
monotonically increasing integer assigned at commit.

T4. **Epoch** — 128 CSPRNG bits, base64url. Identifies one continuous
history of the store. Rotates only on restore-from-backup.

T5. **Cursor** — a consumer checkpoint: `(epoch, seq)`. Server-issued,
opaque-ish (documented encoding, §Cursors), valid until the epoch rotates
or retention expires it.

T6. **Pump** — the serialized server process that drains durable rows to
connections. Reused from the archived design.

## The event vocabulary law

V1. Every substrate happening that commits SHALL publish exactly one
firehose event row, written in the same transaction as the fact it records.
A happening with no row does not exist to observers; a row written outside
the transaction can be lost or orphaned. Both are defects.

V2. Classes are namespaced `area.happening`, lowercase, dot-separated.
The initial vocabulary is derived mechanically from what main already
records (the events, lifecycle_events, and rail-denial tables, plus the
row-writing verbs). The build card enumerates it; this spec fixes only the
law: open set, one class per happening, a class name never changes meaning.

V3. The payload is the recorded truth: the same fields the substrate wrote,
unredacted. The reader is the authenticated user on their own gateway;
there is nothing to hide from them. (The draft's AR91 redaction died with
the capability threat model.)

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
  "cursor": "fhc_v1_..." ,
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
prefix. Multiple given fields are conjunctive. No filters means everything.

S3. `cursor` is optional. Omitted means "from now": the registration cut is
the durable head read during serialized registration (the archived design's
AR148 mechanism, kept verbatim). Supplied means "replay after this cursor,
then go live."

S4. `{"seq": 0}` at the current epoch is a lawful cursor: replay from the
beginning of retained history.

S5. The server answers `subscription_ready` carrying the cursor at which
live delivery begins (after any replay completes). One subscription per
connection; changing filters is a new connection. Connections are cheap on
a local network.

S6. There is NO admission or replay concurrency limit (Mike's OQ9 ruling:
no limit). Any number of consumers may replay any amount of history
concurrently.

## Delivery semantics

D1. Delivery is at-least-once, in seq order, per connection. An ambiguous
network break may repeat an event; it never loses one.

D2. The client dedupes by `(epoch, seq)` and persists its cursor only after
applying the event. (Archived AR160-AR162, kept.)

D3. The writer never touches a socket in the transaction: after commit it
sends a nonblocking nudge; the pump drains durable rows. A missing or
crashed pump never invalidates a row. A 30-second heartbeat compare of
drained-vs-durable head catches lost nudges. (Archived AR139-AR145,
AR163-AR164, kept.)

D4. Slow consumer: each connection has a bounded in-memory queue. On
overflow the server closes THAT connection with close code 4008 and the
last-delivered cursor in the close reason. The client reconnects and
replays; nothing is lost because the rows are durable. This is not an
admission limit; it is the only alternative to unbounded server memory.

D5. Decimation: kill the gateway mid-stream and every consumer resumes from
its cursor on restart with zero loss. Kill a consumer and the substrate
does not care.

## Subscribe-then-query (the consistency recipe)

Q1. A consumer that needs current state plus updates SHALL: (1) subscribe
with no cursor and receive `subscription_ready` with cursor K; (2) query
current state through the existing query surface; (3) apply events after K,
deduping against what the query already showed. Events between subscribe
and query are duplicates by construction, and D2 handles duplicates.

## Cursors

K1. Cursor encoding (this spec exercises the OQ10 delegation): the
documented prefix `fhc_v1_` plus unpadded base64url of canonical UTF-8 JSON
`{"epoch":"...","seq":N}`. The decoder rejects extra fields, non-canonical
encoding, negative or non-integer seq, and unknown prefixes, all as
`cursor_invalid`. Decoding stays backward compatible across versions: a
`fhc_v1_` cursor decodes forever.

K2. A well-formed cursor with a non-current epoch is `cursor_expired`. The
client re-enters via §Q1 (subscribe from now, re-query state).

K3. A cursor whose seq is below the retention floor is `cursor_expired`,
same recovery.

K4. A supported restore-from-backup rotates the epoch before the store
serves any read or write, so a stale-history cursor can never silently
resume against rewound truth. (Archived AR136-AR138, kept.)

## Storage

ST1. One append-only table, one AUTOINCREMENT seq, rows written in the
committing transaction (V1). The existing EventLog tables (events,
lifecycle_events, rail denials) either fold into it or dual-write during
transition; the build card decides, the wire contract above does not
change either way.

ST2. Retention: v1 retains everything. The `cursor_expired` machinery (K3)
exists so a retention horizon can be added later as a config change, not a
contract change. If the table's growth becomes a real problem before then,
that is a measured fact to bring back here, not a reason to pre-build
pruning.

## Errors and close codes

E1. Before upgrade completes: existing HTTP auth failures as today; `426`
for an unsupported protocolVersion.

E2. After upgrade, one closed error frame shape
`{"type":"error","code":"...","message":"..."}` with codes:
`invalid_request` (malformed subscribe), `cursor_invalid` (K1),
`cursor_expired` (K2, K3).

E3. Close codes: 4008 slow-consumer (D4, cursor in reason), 1012 restarting
(gateway shutdown; resume by cursor), plus the standard codes.

## Acceptance

A1. Every row-writing verb on main tip produces exactly one firehose event
in the same transaction, proven by a test that diffs the verb table against
the emitted classes.

A2. Kill -9 the gateway under sustained writes; on restart a consumer with
a pre-kill cursor replays to head with no gap and no duplicate it cannot
dedupe.

A3. A filtered subscriber (class prefix + workItemId) receives exactly the
matching events and its cursor still advances past non-matching seqs (a
filter must not strand a cursor).

A4. A consumer executing §Q1 arrives at state identical to a fresh query at
any quiescent moment.

A5. A slow consumer forced into 4008 resumes by cursor with zero loss.

A6. The feature-smoke drives one real external consumer (ATC or a script)
end to end.

## Open questions for Mike

MQ1. Payloads are full recorded truth (V3), which includes prompt text
inside verb payloads where the substrate recorded it. Confirm that is
wanted on this feed, or name classes whose payload should carry refs only.

MQ2. Retention-is-everything (ST2): confirm, or set a horizon now.

MQ3. Should the firehose fold the EventLog tables into itself (one table of
record) or sit beside them (ST1 leaves it to the build card)? Product-level
only if you care; otherwise it stays the builder's call.
