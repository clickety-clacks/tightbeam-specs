# Drift MVP — editor, participation, and topology

## Goal

Complete the human/agent writing loop on the authoritative document service:
write and save plain text/Markdown; select and discuss exact passages; point,
edit, suggest, accept/decline, and resolve with independent participant attention;
recover work after disconnection or restart. The agent stays in its own harness.

Authority: [SPIRIT.md](SPIRIT.md), [MIKE_PRODUCT_BRIEF.md](MIKE_PRODUCT_BRIEF.md),
Mike's plain-text/Markdown ruling `dr_d9f53dfc`, and PO
[ACCEPTANCE.md](ACCEPTANCE.md) at `ea101a4`. Work item:
`wi_9069f091-53a7-41ff-8b7b-a7d07c188bde`; spec assignment:
`asg_13f64a20-ca20-4f9a-ac2d-fa38391b991c`. Code: `clickety-clacks/drift`.

[CORE_CONTRACT.md](CORE_CONTRACT.md) owns slice 1: documents, revisions, ranges,
anchors, authored messages, revision-checked commands, receipts, snapshots, and
durable event recovery. Its reviewed version is commit
`99aeeab827363cd30db959e7a6215596c6d233ac`, SHA-256
`7ffc5528918a55f08a0643b9f4d527a13fc20ac46a26969b0eb1097e5801a421`, reviewed-clean
in `att_611a41fe`. This file extends that core; it does not redefine it.
Core review/build proceeds independently of this file and its marked questions.

This draft replaces the earlier whole-loop draft's duplicated core definitions.
Remaining build slices are: **2**, symmetric participation and agent adapter;
**3**, toolkit-neutral writing/recovery GUI; **4**, configured split topology and
access integration after the PO's choice. Each can be reviewed against its
clauses below. Final product acceptance still requires the complete loop.
Draft status: cold digest and independent review are not yet recorded for these
remaining slices; the core's clean verdict does not cover them.

## Non-Goals

Rich-text representation/fidelity, rendered Markdown preview, DOCX, pagination,
an office suite, embedded models, bundled AI accounts, mandatory hosted services
or MCP, an agent harness inside Drift, automatic idle-harness wake or terminal
keystroke injection, public-cloud collaboration, or offline collaborative merging.

No release, installation, deployment, or live mutation. Deferred beyond MVP:
advanced undo across intervening edits, presence history, fuzzy relocation,
formatting, expanded import/export, and retention/compaction. These do not gate
the smallest complete writing loop.

## Terms

Core terms retain their meanings in CORE_CONTRACT.md, including Unicode-scalar
half-open ranges, LF text, immutable revisions, and document-bound event cursors.

- **Participant**: the core actor identity, whether human or agent. The same
  actions apply to both; the chosen access boundary supplies identity.
- **Presence**: a connection's transient selection and separate point-out,
  attributed to its participant and document. An empty selection is a caret;
  a point-out highlights a nonempty range. Presence is replaceable, not history.
- **Suggestion**: durable ID, author, original core passage anchor, proposed
  replacement text, and pending/accepted/declined state. Its target is nonempty;
  an empty replacement proposes deletion. Direct edits support insertion.
- **Draft**: client recovery material containing base revision/text and unsaved
  text or command payload. It is not authoritative service state.
- **Adapter session**: an explicitly started client process that holds an agent
  participant's WebSocket connection and accepts CLI commands locally. It runs
  no model. Its presence ends when that connection ends.

## Assumptions

1. The core contract is implemented and independently verified before claiming a
   complete writing loop. Core test fixtures do not prove product authentication.
2. The user runs an external harness capable of invoking a CLI and receiving a
   blocking tool result. Drift has no verified idle-harness wake mechanism.
3. Toolkit and access specifics remain PO-owned under Q1/Q2. Components can be
   developed against the boundaries below without selecting those choices.
4. Service storage survives process restart. Client recovery uses a separately
   configured client-side path. No shared filesystem between machines is assumed.

## Invariants

**P1 — Same actions, same service.** Human and agent use the core command boundary
for durable changes, with the same revision, receipt, author, and error rules.
Given a suggestion by either participant, when the other accepts it, then the
service commits its text replacement and decision together (W1, W2).

**P2 — Independent attention.** Remote selection and point-out events change
collaborator overlays, not the human's native selection or keyboard focus.
Given the human typing at a caret, when an agent points elsewhere, then the next
keyboard event still edits at that human caret (W1, W3).

**P3 — Preserve unacknowledged work.** Incoming events do not replace a dirty
editor buffer. Saved means service-acknowledged text. Given a stale GUI edit,
when the service refuses it, then the GUI retains its draft and offers the newer
revision for inspection (W3). Core refusal/retry rules also apply to the CLI.

**P4 — Live delivery builds on durable recovery.** Live events and replay use the
core's event order. Presence is not replayed. Given a disconnected participant,
when it reconnects, then missed durable discussion returns but old presence is
not presented as a current connection (W4).

**P5 — Configured access spans transports.** The chosen access boundary protects
HTTP reads/commands, WebSocket actions/events, and replay consistently. Given an
unauthorized client, when it connects through any of those surfaces, then it
receives no protected document content and cannot claim another actor (W6).
The mechanism remains Q2; this is its acceptance floor, not a token-policy choice.

## Architecture

### Slice 2: symmetric participation and agent adapter

Extend the core's `POST /documents/{D}/commands` envelope with `suggest`, `accept`,
`decline`, and `resolve`. The existing `edit`, `comment`, and `reply` commands
retain their core semantics, including `baseRevision` on replies. Add the same
command envelope over WebSocket, backed by the same transaction boundary.
Do not create a second mutation implementation for socket clients (P1).

| Action | Payload and observable behavior |
| --- | --- |
| `suggest` | `{start,end,text}` at `baseRevision`. Persist a pending suggestion with a core anchor and author. Text remains unchanged. Show original and proposed text (W1). |
| `accept` | `{suggestionId}` at `baseRevision`. Require pending state and a currently attached target. Atomically replace that current range, create a revision, and mark accepted with deciding actor. The target may survive edits outside it; base revision must still be current (W2). |
| `decline` | `{suggestionId}` at `baseRevision`. Atomically mark a pending suggestion declined with deciding actor; text remains unchanged (W1, W2). |
| `resolve` | `{threadId}` at `baseRevision`. Mark the thread resolved, preserve messages/anchor, and record deciding actor. A resolved thread still accepts replies without reopening. An already resolved thread returns its existing state without another event (W1). |
| Select / point / clear | Connection-scoped presence update with document, revision, kind, and range, or clear. Caller can update only its own connection's presence. A point-out does not change its selection (W1). |

Core threads gain open/resolved state, initially open. Suggestions and thread
resolution join durable snapshots and replay. Each successful state change adds
one event with the affected object state; acceptance carries its text delta and
anchor changes in that same event. Resolve's no-change success receives an
idempotent receipt but no new event. The service checks suggestion status and
text revision in the same transaction as acceptance/decline. Two decision attempts
produce one terminal decision. Add errors `already_decided` and `anchor_detached`;
neither changes text or decision state. Declining a detached pending suggestion
is valid; accepting it fails visibly. Detached suggestions retain their text,
quote, author, and reason under the core anchor rules (W2, W4).

Expose current presence and suggestions through document reads, with presence
identified separately as transient. A passage read returns document, requested
revision/range, exact selected text, and surrounding text from that revision;
returning the whole revision is sufficient context. Reading a connection's
selection returns its revision/range/text or an explicit unavailable result.
Do not silently substitute today's text for an older selection (W1).

Presence belongs to the publishing connection, attributed to its participant.
Each connection has one selection and one point-out per document. The service
validates ranges against the named revision. It transforms an older nonempty
range along the core edit history; unmappable presence becomes unavailable until
its owner selects again. For an empty caret: edits strictly before it shift it;
an insertion at its position leaves it before the inserted text; a replacement
containing it maps to the replacement's end. Own typing uses local input intent,
not these remote-event rules. Presence is not stored durably. On observed socket
closure remove that connection's presence; after reconnect use new presence.
Until a broken connection is detected, displayed presence is last reported
attention, not proof that a participant is currently responding (W1, W4).

A WebSocket subscriber names document and last processed core cursor. Deliver
strictly later durable events in order, then continue live without a replay/live
gap. A coherent snapshot's cursor can start that subscription. Deduplicate by
cursor, including events received by their sender. Invalid cursors fail as in
the core; reconnect restores durable state and takes a fresh presence snapshot.
Presence updates are replaceable and carry their text revision, never a durable
event cursor. Exact socket route/frame spelling is a documented adapter detail
(W4); no separate broker or agent supervisor is required.

The external harness uses structured JSON CLI commands for document/passage reads,
thread reads, each durable command, presence, and wait. CLI failures use nonzero
exit status and preserve/return the submitted payload and base revision. Read
errors have no submitted command. After refusal, a participant explicitly reads
current text and resubmits with a new ID; the CLI does not silently change bases.
After an unknown outcome, retry the same command ID under the core contract.

For continuing presence, explicitly start an adapter session. CLI select/point
commands address its configured local endpoint; it owns the WebSocket and the
presence lifetime. Standalone HTTP commands remain available for durable actions.
The session needs no shared filesystem with the service. Continuing selection
needs a connection owner beyond one short CLI process; dropping it loses a
required action, and reporting an exited client as live misstates presence (W1).

`drift wait --document D --after C [--timeout SECONDS]` can run independently of
an adapter session. It opens an active subscription and returns a nonempty ordered
batch after C plus its next cursor, then exits. Backlog returns immediately. With
none, it blocks until a durable event, caller timeout, cancellation, or connection
failure. Timeout returns an explicit empty `timeout` result; cancellation and
transport/auth failure return distinct failing results and do not advance the
caller cursor. Omitted timeout waits until an event or interruption. Registration
uses the same no-gap replay/subscription contract; optional event filtering is
outside this MVP (W5).

The harness processes the returned batch, acts, and invokes wait again after its
last processed cursor. No active tool call means durable questions wait for later
retrieval. A connected socket alone does not wake an idle model. MCP and verified
harness wake integration may be future adapters; neither is required or simulated.

### Slice 3: toolkit-neutral editor, save, and recovery

The GUI integration exposes text/base revision, local replacement deltas, native
selection, and separate participant/thread/suggestion overlays. Convert toolkit
positions to core scalar offsets in both directions. Wrap/scroll affect geometry,
not passage identity. Reserve native selection and focus for the local human.
The Qt spike observed `QTextDocument.contentsChange(position, removed, added)` as
a local delta source; if Qt is selected under Q1, adapt it at this boundary.
Widget cursors do not own durable attachment decisions (W1, W3).

The GUI creates, lists, reopens, and edits service documents. It submits local
text commands in order, at most one outstanding per document, and retains the
base text plus resulting draft until acknowledgement. Coalesce adjacent local
typing if useful, but do not widen an edit across an untouched passage. Autosave
submits pending typing when no command is outstanding; Save flushes pending work
and reports saved only after acknowledgement. A client-side UTF-8 save/export
writes acknowledged source text to the user's chosen file. That file is not a
second authoritative document store (W3).

With no pending local text, apply an incoming replacement and map the local caret
without changing focus. With pending text, preserve the draft and show that newer
service text exists. Resolve any unknown submitted outcome before resubmission.
The user can inspect/copy draft and current text, then explicitly resubmit. An
incoming service update cannot clear unsaved text. Discussion actions return
focus to the editor when they finish; remote activity does not request focus.
Show authors, suggestion decisions, thread resolution, and detached discussion
with its original quote/reason even when it has no inline location (W1–W3).

Before network submission, write local recovery material to a configured client
path: document ID, base revision/text, draft, and outstanding command ID/payload.
On GUI restart offer that recovery material and resolve unknown outcomes through
same-ID receipts. Keep recovery material until the command outcome and remaining
draft are recorded. A failed recovery write is visible; retain the draft for
copying. A crash before a local recovery write can lose the input not yet
recorded there; do not report that input as saved. Service acknowledgement proves
service durability, not durability of later unrecorded keystrokes (W3).

Undo reverses the latest unsent local text operation. For a saved local edit,
submit its inverse with a new command ID against the revision it produced.
If an intervening edit superseded that revision, report a recoverable conflict
and preserve the proposed inverse. This MVP does not silently undo across newer
work or reverse discussion and suggestion decisions. Show this limit when undo
cannot proceed; advanced collaborative undo remains deferred (W3).

### Slice 4: topology and access integration

Configure service bind address/port and durable store; GUI/CLI service URL;
client recovery/config paths; adapter's local endpoint; and connection/auth
settings. Paths belong to the machine running that component. No product constant
names Gibson, a user, or a home directory. Loopback defaults do not prevent a
configured split deployment after access integration (W6).

Q2 selects the trust/access mechanism. Integrate it at the core's request boundary
and at HTTP/WebSocket reads and subscriptions. It supplies actor identities,
permits authorized actions, protects remote content/credentials, and rejects
impersonation. An unconfigured network-facing service fails startup visibly
instead of adopting the core fixture's trust. Product clients use configured
participant identities; a submitted actor field cannot override authentication.
Core fixtures with test actors remain valid core evidence, not product-access
proof. Nothing here selects workspace scope, token issuance, or credential policy.

## Acceptance

Run the core T1–T5 checks plus the applicable slice checks below. These map to
[ACCEPTANCE.md](ACCEPTANCE.md) examples 1–7. Record exact candidate, actual machines,
commands/harness, inputs, and observed output/captures. Real GUI and external-harness
interaction are required for full-loop acceptance; a spec read, synthetic test,
or Qt spike alone does not prove it. No live installation follows from these tests.

- **W1 — Symmetric loop (slice 2/3; P1/P2; PO 1–3).** Given H and A and
  `The draft is clear. The ending is weak.`, H saves, selects sentence two and
  asks a question. A reads that exact passage/context, replies, points at sentence
  one, and suggests a replacement. H accepts it. Reverse roles for the discussion
  actions, decline a fresh suggestion, and resolve a thread. Observe distinct
  authors and selections, accepted text, unchanged text on decline, and retained
  resolved messages. During point-out, a real key event edits at H's original
  caret with focus intact. Emoji, combining marks, wrap and scroll preserve
  agreement between GUI selection and service/CLI text.
- **W2 — Suggestion safety (slice 2; P1; PO 3–5).** Given a pending suggestion,
  edit outside its passage, refetch, and accept against the current revision.
  Observe one text revision and accepted state in one event. Accepting against
  the old revision fails with original payload preserved; accepting a detached
  target fails, and decline still works. Concurrent accept/decline produces one
  terminal decision. Retry a lost acknowledgement: no duplicate decision or edit.
- **W3 — Writing and recovery (slice 3; P2/P3; PO 2–5).** Type into a blank
  document, autosave, explicitly save, reopen, and compare text. Save a UTF-8
  file on the GUI machine. Keep typing during agent activity. Race an agent edit
  against a dirty GUI draft; inspect both preserved versions after refusal.
  Undo an unsent and a just-saved local edit; an intervening edit makes saved
  undo refuse without overwriting newer text. Restart the GUI after recovery
  write but before acknowledgement; recover the draft and resolve the command
  without duplication. Verify saved/error status matches the actual boundary.
- **W4 — Reconnect (slice 2/3; P4; PO 5–6).** Persist text, thread, reply, and
  suggestion, then restart the service. Verify content, authors, decisions, and
  detached states. Disconnect a participant, change discussion/text, and recover
  after its prior cursor. A commit at snapshot/subscription transition is not
  lost. Replayed events do not duplicate replies. Close the presence connection:
  its old selection disappears; after service restart it is not resurrected.
- **W5 — Actual harness wait (slice 2; P4; PO 6).** Invoke wait from a real
  external harness with no backlog. A human question releases the active tool
  call; the agent reads and replies. Check immediate backlog, an event during
  registration, explicit timeout, cancellation, and transport failure. Without
  an active harness call, the question persists; make no idle-wake claim.
- **W6 — Configured topology (slice 4; P5; PO 7).** After the Q2 decision,
  demonstrate the same writing loop with colocated components and with client
  and service on separate machines, using disposable data and credentials.
  Name the actual host of GUI, service, and adapter. Change endpoint, bind, and
  storage through configuration. Verify allowed access and denial on HTTP,
  WebSocket, and replay; reject actor impersonation. Unconfigured non-loopback
  startup fails. Separate processes on one machine are not split-host evidence.

## Open Questions

- **Q1 — NON-BLOCKING: toolkit.** PO-owned decision path:
  `dr_fb76ce2a-bca9-46da-8115-3472275e2394`. Standalone Qt Quick is a recommendation,
  not a selection. Spike `art_114d275d`, SHA-256
  `be59ae69a4d6346def0d0a809c372126285c6a9d958646358f852871c0482f86`, reports 12
  offscreen assertions on racter using Qt/PySide6 6.11.2: independent overlays,
  focus preservation, wrap/scroll and local deltas. Quickshell was unavailable,
  not disproven. Report: `racter:/home/clu/.tightbeam/work/d9274efe5684/drift-editor-spike/REPORT.md`.
  The neutral boundary and service work proceed; final toolkit integration uses
  the eventual ruling. No toolkit recommendation becomes format authority.
- **Q2 — NON-BLOCKING: trust/access.** Same request, not a second decision path:
  `dr_fb76ce2a-bca9-46da-8115-3472275e2394`. Its recommendation is one trusted
  workspace, separately revocable participant tokens, and encrypted remote
  access. It is not an approved trust boundary. Possible connection mechanisms
  include a protected private tunnel with participant credentials, TLS with
  application credentials, or mutual TLS with participant mapping. The PO chooses
  the trust/access specifics; W6 needs that choice, while other slices proceed.
- **Q3 — NON-BLOCKING: license.** PO/user choice. Private development proceeds;
  a license declaration or release under one awaits the choice.
- **Q4 — NON-BLOCKING: core review maintenance.** Review `art_3f66108f`
  (SHA-256 `87f4839046f4629fa4f62784f965d804224f1f12a1ec14cfab39bdc9b1c144e0`)
  cleared core 99aeeab and recommended later clarification of defensive-only
  ambiguity, document-checkable cursors, command-only error payloads, and refusal
  receipts. Ruling: defer edits to that reviewed core while implementation uses
  its exact bytes; no new fuzzy matcher or change to reply freshness. Its fifth
  recommendation records possible later relaxation of reply freshness, not a
  change in this MVP. Report: `gibson:/home/mike/.tightbeam/work/af9645055239/review-CORE_CONTRACT-99aeeab.md`.

No blocking question is left unmarked. Details that change these contracts return
to the spec writer. Rulings amend the canonical spec before affected work proceeds.
