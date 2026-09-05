# Drift MVP — technical specification

## Goal

Deliver one complete writing loop: a human writes and saves plain text or Markdown;
their external agent reads a selected passage, discusses it, points elsewhere, and
proposes an edit; either participant can edit and decide suggestions. Discussion
stays attached to its passage or visibly loses its attachment. Writing survives
stale requests, disconnects, and service restart.

Authority: [SPIRIT.md](SPIRIT.md) and [MIKE_PRODUCT_BRIEF.md](MIKE_PRODUCT_BRIEF.md),
read in full at tightbeam-specs commit `6abd05b`. Mike's format ruling is
`dr_d9f53dfc-4e05-49fe-b353-17cdb2f6efb1`: plain text/Markdown first, without a
rendered-preview requirement. This specification implements that slice; it does
not replace the Spirit. Work: `wi_9069f091-53a7-41ff-8b7b-a7d07c188bde`.
Code home: private `clickety-clacks/drift`. Spec home: this file on
`clickety-clacks/tightbeam-specs` main.

Draft status: landed for custody; scheduled cold digest precedes review/build
handoff. [ACCEPTANCE.md](ACCEPTANCE.md) at `ea101a4` supplies the PO's acceptance
examples; the checks below implement those outcomes.

## Non-Goals

Rich-text representation or fidelity; Markdown preview; DOCX, pagination, or an
office suite; embedded models, bundled AI accounts, mandatory hosted services or
MCP; an agent harness inside Drift; automatic idle-harness wake or terminal input
injection; public-cloud collaboration; offline collaborative merging.

This spec authorizes no release, installation, deployment, or live mutation.
No product constant names Gibson or a user's machine or home directory.

Deferred: formatting, import/export workflows beyond plain-text save, advanced
merge/undo across other participants' edits, presence history, and retention or
compaction policies. These are not acceptance requirements for this slice.

## Terms

- **Document**: service-owned ID, title, format (`text` or `markdown`), and current
  text revision. Markdown is editable source text, not a second document model.
- **Revision**: immutable document text plus its parent revision and the committed
  replacement that produced it. Revisions belong to one document. Discussion
  actions do not change the text revision.
- **Range**: half-open `[start,end)` in Unicode scalar values in one named revision.
  UTF-8 bytes, UTF-16 units, and screen coordinates are not protocol offsets.
  A range with equal ends denotes an insertion point. Text uses LF line endings;
  adapters normalize CRLF on input and perform no Unicode normalization.
- **Participant**: stable service identity with display name. Human and agent are
  participants with the same action capabilities. Authenticated identity, not a
  submitted display name, supplies durable authorship.
- **Anchor**: document ID, original revision/range, original selected text, and
  derived current range or an explicit detached reason. Retained revision text
  supplies its context fingerprint: the exact original quote and surrounding
  text, recoverable by revision/range without a second stored copy. It records
  provenance, not a fuzzy-search key. A thread's anchor refers to a nonempty
  passage.
- **Thread**: durable anchor, ordered authored messages, and open/resolved state.
  A question is an ordinary message in a thread, not a separate delivery system.
- **Suggestion**: durable proposed replacement for a nonempty anchored passage,
  author, replacement text, and pending/accepted/declined state. Empty replacement
  means deletion. Direct edits also support insertion at an empty range.
- **Presence**: transient participant selection and point-out, each tagged with
  document and revision. Selection describes current attention; a point-out is
  a separate temporary highlight. Neither is a persisted comment.
- **Cursor**: opaque durable event position for one document. It is distinct from
  a text revision and from the human's typing caret.
- **Draft**: client-held unsaved text or command payload with its base revision.
  It is recovery material, not authoritative document state.

## Assumptions

1. One authoritative service instance owns a configured durable store. Its
   storage survives process restart; disk loss and multi-server failover are
   outside this slice.
2. Participants receive access through the configured trust boundary. A single
   shared workspace is a pending proposal under Q2, not an approved given.
   The document protocol does not require a per-document role hierarchy.
3. A user runs the agent in an existing external harness that can invoke the CLI.
   An active tool call can wait for events. Drift has no verified means to wake
   an idle harness.
4. GUI toolkit and remote access mechanism remain undecided. The neutral boundary
   below supports either choice. Private development does not require a license
   declaration.

## Invariants

**I1 — One durable mutation boundary.** The service validates a participant command
and commits its state changes, event, and retry receipt atomically. GUI and agent
use this same boundary. Only text-edit commits create revisions. Acceptance: two
editors submit against revision 4; exactly one edit can create revision 5 (A3).

**I2 — Compare and write are one step.** Each durable command on an existing
document carries `baseRevision`. The service compares it with the current revision
inside the same transaction as its mutation. It also checks object state there.
A rejected command changes no document, thread, suggestion, or event. Acceptance:
an edit against revision 4 after revision 5 exists returns `stale_revision` (A3).

**I3 — Attachment follows provenance.** The service maps an anchor through recorded
replacements, not a fresh search for matching prose. If that mapping cannot
preserve the selected passage, it retains original text and reports detachment.
Acceptance: deleting one of two identical sentences detaches its thread rather
than attaching it to the other sentence (A2).

**I4 — Independent attention and authorship.** Each participant controls only its
own presence. The GUI renders other participants' presence separately from its
native selection and typing caret. Remote events preserve typing focus and local
work. Acceptance: an agent point-out while the human types neither redirects the
next character nor replaces the human selection (A1, A4).

**I5 — Acknowledgement means durable commit.** The service acknowledges a command
only after its transaction persists. A saved indicator identifies acknowledged
text; unsaved work remains visibly distinct. Acceptance: restart after an
acknowledged save returns that revision and its discussion (A4, A5).

**I6 — Transport does not grant authority.** HTTP reads/writes, WebSocket actions,
subscriptions, and replay enforce the same configured access boundary. Clients
cannot impersonate another participant by changing an action field. Acceptance:
an unauthorized split client receives neither document content nor events (A7).

## Architecture

### Components and ownership

`GUI <-> document service <-> external-agent CLI/adapter` is the component boundary.
The GUI edits a local draft and renders service state. The service owns documents,
immutable revisions, threads/messages, suggestions, and the durable event log.
The CLI is a client of that service; it contains no model runtime. The builder
chooses implementation language, persistence library, and editor toolkit within
these contracts. No separate broker, CRDT, or background agent supervisor is needed.

Persist each successful durable command as one ordered event for its document.
An event contains its cursor, command ID, actor ID, type, resulting text revision,
and affected object IDs with their changes. Document snapshots include text,
threads, suggestions, authors, anchor states, and an event cursor from one
consistent read. Retain revisions, events, and retry receipts for this MVP;
compaction is deferred. Acceptance: snapshot plus later events reconstructs the
same state as a fresh snapshot (A5).

This specification teaches no Tightbeam operating pattern. Its named product
pattern is **revision-checked command**, used for durable document actions only:
`edit(document=D, baseRevision=4, range=[0,3), text="New", commandId=X)` either
commits once against revision 4 or returns recoverable failure. Presence uses
replaceable updates instead. This pattern refines the proposed service boundary
in Mike's brief; it supersedes no other Drift technical specification.

### Commands and the writing surface

The following semantic operations are shared by HTTP/CLI and WebSocket clients.
Exact route and flag spelling is an implementation detail; ship documented
request/response examples with the adapter. Each durable command has a
client-generated command ID and a payload retained until its outcome is known.

| Operation | Minimum contract and observable result |
| --- | --- |
| Create/list/read documents | Create title, format, and initial text; list IDs/titles/revisions; read a coherent snapshot. A new blank document can be written, reopened, and saved (A1, A4). |
| Read passage/selection | Return exact revision, range, selected text, and surrounding text. A passage request can name a retained revision; current selection reads identify unavailable/detached presence rather than guessing (A1, A2). |
| Select / point | Publish caller's own revision/range; allow clear. New presence replaces that caller's prior value of that kind. Point-out does not change selection. Subscribers see actor and range (A1). |
| Comment / reply | Create a thread on a passage or append an authored message to a named thread. Service derives the original quote from the supplied revision/range. Reply remains possible on detached or resolved threads and does not reopen them (A1, A2). |
| Edit | Replace one range with supplied text in the named base revision. Service validates bounds and stores parent, replacement, actor, and resulting text. A user may insert, delete, or replace text (A3, A4). |
| Suggest | Persist a replacement and its passage anchor without changing text. Display original and proposed text with author and pending state (A1). |
| Accept / decline | Either participant may decide a pending suggestion. Accept replaces its currently attached passage and marks accepted in one commit. Decline changes only suggestion state. A second decision fails with `already_decided`; a detached target cannot be accepted (A3). |
| Resolve | Either participant may mark a thread resolved. Preserve its messages and anchor; show its resolved state. Resolve on an already resolved thread returns that state without a duplicate event (A1). |

Retrying the same actor/command-ID/payload returns its original committed result,
including after restart. The service checks this receipt before rejecting a now
stale base revision. Reusing that ID with another payload returns
`command_id_conflict`. Unknown outcome after a network break calls for retry with
the same ID, not an invented new edit. Acceptance: lose a reply acknowledgement,
retry it, and observe exactly one reply and event (A5).

Errors expose a machine-readable code and a readable reason. `stale_revision`
includes the current revision and a means to read it; `invalid_range`,
`anchor_detached`, and `already_decided` identify the affected object. The GUI
retains rejected text visibly; the CLI retains/returns the submitted payload and
base revision with a failing exit status. A participant reads current state and
explicitly resubmits with a new command ID. Drift does not silently merge or
retry a rejected edit against a newer base. Acceptance: A3 preserves both the
newer document and the rejected replacement.

### Revision-aware passage anchors

For an attached range `[s,e)` and committed replacement `[a,b)` with replacement
length `n`, transform through the ordered revision chain:

1. If `b <= s`, shift both endpoints by `n - (b-a)`.
2. Otherwise, if `a >= e`, retain both endpoints.
3. Otherwise, detach with `passage_changed` (or `passage_deleted` if the whole
   selected passage was removed). Insertion strictly inside a passage also
   detaches: its original selected text no longer survives unchanged.

These rules exclude boundary insertions from the original passage: insertion at
its start shifts it forward; insertion at its end leaves it unchanged. Verify
the mapped text equals the original quote. A missing revision chain or mismatch
detaches with `unverifiable`; a non-unique mapping reports `ambiguous` and chooses
no candidate. Duplicate text elsewhere is irrelevant; exact edit
history identifies the occurrence. A detached anchor stays detached even if
matching text later returns. The MVP offers a new thread or suggestion on a
new explicit selection, not automatic reattachment.

Threads and suggestions retain their content, original quote/revision, author,
and detached reason. The GUI shows them in discussion even when it cannot draw
an inline highlight. The API exposes the same state. This conservative behavior
accepts visible detachment after editing the passage itself; nearby edits remain
attached. Adding fuzzy relocation lost because it can silently change meaning;
deleting detached discussion lost because it discards the user's work (A2).

Selection and point-out ranges use the same mapping during a connection.
An unmappable presence range becomes visibly unavailable until its participant
selects again. A zero-length caret maps through earlier edits, stays before an
insertion at its own position, and moves to the end of a replacement containing
it. The human caret uses local edit intent for the human's own typing; remote
presence never drives it. Presence is connection-scoped, not replayed history.
On a lost socket, mark it disconnected; a new connection republishes presence.

### Toolkit-neutral editor boundary, save, and recovery

The editor integration exposes text with its base revision, local replacement
deltas, local selection, and separately rendered participant/thread ranges. It
converts toolkit positions to protocol scalar offsets in both directions.
Wrapping and scrolling change geometry only. They do not change passage identity.
Acceptance: an emoji before the selected sentence, line wrapping, and scrolling
leave GUI and CLI selecting the same sentence (A2).

Reserve the native editor selection for the local human; collaborator ranges
are separate overlay records. The spike observed Qt's
`QTextDocument.contentsChange(position, removed, added)` as a local delta source.
If Qt is selected under Q1, adapt those deltas to the protocol convention;
another toolkit must expose equivalent deltas. Widget cursor movement is not
the service's durable anchor decision (spike report section 5; A2).

The GUI submits local edits in order with at most one outstanding text command
per document. It may coalesce adjacent local typing into a replacement, but must
not widen the replacement across an untouched passage. It retains
the base text and resulting draft until acknowledgement. Save flushes pending
typing and reports saved only after acknowledgement; ordinary typing also
autosaves when no command is outstanding. A plain-text save/export writes the
visible acknowledged document as UTF-8 to a user-chosen client-side file; it does
not require shared filesystems or make that file the service's source of truth.

When remote text arrives with no local pending edit, update the editor through
the replacement and map its caret/selection without changing focus. With local
pending text, keep that draft, show that newer service text exists, and resolve
any unknown submitted outcome first. The user can inspect/copy the draft and
current text and explicitly resubmit. Incoming events must not replace a dirty
editor buffer. This is recoverable conflict handling, not offline merging (A3).

The GUI keeps local recovery material for unacknowledged text in a configured
client storage location: document ID, base revision/text, draft text, and any
outstanding command ID/payload. It writes recovery material before network
submission. On restart it offers that draft and resolves unknown outcomes by
retry receipt before resubmitting. A failed local recovery write appears as a
visible error, and the draft stays available for copying. Service-acknowledged
work survives restart; a GUI crash before a local recovery write can lose only
the input not yet recorded there. Do not describe that input as saved (A4).

Undo reverses the latest local text operation in an unsent draft. For a saved
local edit, undo submits its inverse against the revision produced by that edit,
with a new command ID. If another edit superseded that revision, undo reports a
conflict and preserves the proposed inverse instead of overwriting newer work.
Undo does not reverse another participant's change, a discussion message, or a
suggestion decision. The editor shows this MVP limitation when undo cannot
proceed; advanced collaborative undo is deferred (A4).

### Live events, replay, and external harness adapter

The service exposes a WebSocket for actions and live events, plus small HTTP
operations for the semantic commands, reads, and durable event retrieval. The CLI
supports those operations as structured JSON output with nonzero error exits.
It can read a document or passage, inspect current presence and threads, perform
each participant action, and wait. GUI and adapter use configured service URLs.

For selection and point-out, the CLI offers an explicit connected adapter session
that holds a WebSocket and accepts subsequent CLI commands through a configured
local endpoint. Those commands address that connection's presence. Starting it
does not start a model. Closing it clears its presence; a standalone HTTP command
does not claim a lasting live selection. Durable commands and wait can also run
without this session. No shared filesystem between adapter and service is needed.
This connection exists because independent continuing agent selection needs an
owner beyond one short CLI process; discarding that surface loses a required
action, and pretending a finished process remains connected misstates presence.

A subscriber supplies document ID and last processed cursor. The service sends
durable events strictly after that cursor, in order, then continues live on the
same stream without a replay/live gap. Clients deduplicate by cursor. An initial
snapshot's cursor is the starting point for subsequent events. Validate cursors
against their document; report an invalid cursor explicitly rather than silently
starting at the present. Reconnection restores durable state; transient presence
is a fresh snapshot. Acceptance: a comment committed between snapshot and live
subscription appears exactly once in reconstructed state (A5).

The minimum CLI wait contract is
`drift wait --document D --after C --timeout SECONDS`. The invocation owns an
active subscription, returns a nonempty ordered batch of durable events after C
and a next cursor, then exits. It immediately returns already available events.
With none, it blocks until an event, the caller's timeout, cancellation, or a
connection/auth error. Timeout returns an explicit empty `timeout` result;
cancellation and transport/auth failure return distinct failing results. An
error never advances the caller's cursor. Omitting timeout waits until an event
or interruption. Registration and backlog retrieval obey the same no-gap
contract as replay; wait does not poll a terminal or simulate harness input (A6).

The harness reads the returned batch, acts, and invokes wait again with its last
processed cursor. It may filter question messages itself; the MVP does not need
server-side question routing. Without an active wait/tool call or verified
external harness integration, Drift promises persisted questions only. A socket
left open does not constitute waking an idle model. Acceptance must demonstrate
one real external harness invocation, not only a WebSocket client (A6).

### Configuration and access boundary

Configure service bind address/port, service storage path, GUI/CLI service URL,
client recovery/config paths, and connection/auth settings. Service and client
paths refer to their respective machines. A loopback default must not prevent a
configured split deployment. Document the values needed to run GUI, service,
and CLI together or on separate machines (A7).

The access-control implementation remains Q2. Its fixed minimum outcome is that
only configured participants can read, subscribe, or write, credentials bind
actions to participant identities, and the split connection protects content
and credentials against unauthorized network peers. Local mode must also prevent
untrusted clients from claiming another actor. An unconfigured split service
refuses network exposure rather than silently adopting local trust. Implement
against an authentication/authorization boundary now; do not select a remote
mechanism by inference. Q2 does not block document service or editor development;
split access acceptance needs the PO's choice (A7).

## Acceptance

The examples below are the MVP contract, not evidence that a build exists.
Each maps to the requirements beside it. Record actual candidate commit, commands,
machines, real input, and observed outcomes. Do not claim runtime proof from a
spec read or a passing synthetic fixture. No demonstration authorizes a live
Gibson installation.

- **A1 — Complete symmetric loop (I1, I4; actions).** Given human H, external
  agent A, and `The draft is clear. The ending is weak.`, when H saves it, selects
  the second sentence, and asks a question, A reads that exact sentence and its
  context, replies, points at the first sentence, and suggests a replacement.
  Then H can accept that suggestion while retaining typing focus. Repeat with
  the roles reversed, decline a fresh suggestion, and resolve the discussion.
  Observe distinct identities, independent selections/points, durable messages,
  accepted text, unchanged text on decline, and visible resolved state.
- **A2 — Passage identity (I3; anchors/editor boundary).** Given an anchor on
  `beta` in `alpha beta gamma`, when an edit inserts text before it or after it,
  then the thread still selects exactly `beta`. Insertion at either boundary
  excludes the inserted text. When an edit replaces/deletes inside the passage,
  then the thread visibly detaches and retains the original quote/messages.
  Given `same. same.` with a thread on the first occurrence, deleting that
  occurrence never attaches it to the second. A missing mapping reports
  `unverifiable`. Repeat a nearby-edit case with an emoji before the passage
  and combining-mark text before it, and with GUI wrap/scroll; GUI and CLI agree
  on text and scalar range. Coalesced typing before/after a passage must not
  replace the untouched passage between the edits.
- **A3 — Conflict and suggestion safety (I1, I2; actions/recovery).** Given two
  edits based on revision R, when the human's edit commits first, then the
  agent's edit fails `stale_revision`, the human's text remains, and the agent's
  payload remains recoverable. Repeat with a dirty GUI draft during an agent
  edit; the GUI preserves the draft. Given a pending suggestion whose passage
  survives a nearby edit, accept against the current revision and observe one
  text revision plus accepted state. Acceptance against the old revision fails;
  acceptance of a detached passage fails. Two concurrent decisions produce
  exactly one terminal decision, with no partial text/status commit.
- **A4 — Daily writing (I4, I5; editor/save/undo).** Given a blank document, when
  H types, autosaves, explicitly saves, closes, and reopens, then the text
  matches and saved status corresponds to acknowledged revision. Save a UTF-8
  file on the GUI machine and compare its content. Undo an unsent edit and a
  just-saved local edit; observe the intended inverse. Insert an intervening
  agent edit before saved undo; observe conflict with newer work intact. Kill
  and restart the GUI after its recovery write but before acknowledgement;
  recover its draft and resolve the command without duplication. An agent
  point-out during typing leaves the next typed character at the human caret.
- **A5 — Durable recovery (I1, I5; persistence/retry/replay).** Given an
  acknowledged document, thread, reply, and suggestion, when the service
  restarts using the same configured store, then a snapshot returns their
  content, authors, decisions, anchor states, and revision. Disconnect a client,
  commit discussion and text changes, reconnect after its prior cursor, and
  reconstruct the same snapshot. Commit at the replay/live boundary and lose a
  reply acknowledgement; replay and same-ID retry produce no lost event or
  duplicate reply. A wrong-document cursor returns an explicit error.
- **A6 — Truthful agent wait (events/adapter).** Given a real external harness
  running the CLI wait after cursor C with no backlog, when H comments, then
  the active tool call returns the event and next cursor and A can reply.
  A second wait with backlog returns immediately. An event committed during
  wait registration is returned. Timeout, cancellation, and connection failure
  each report their actual outcome. With no active harness call, a question
  persists for later retrieval; the demonstration makes no idle-wake claim.
- **A7 — Configurable topology (I6; configuration).** Given configured identities
  and connection protection selected under Q2, demonstrate the loop with the
  components on one machine and with service, GUI, and adapter locations split.
  Record the actual machine for each component; do not substitute different
  processes on one machine for a split demonstration. Change host/port/storage
  through configuration alone. An unauthorized client cannot read snapshots,
  mutate documents, or receive replay/live content. A client cannot submit
  another participant's actor ID. With no configured split protection, a
  non-loopback service start fails visibly. Q2 remains an explicit dependency
  for this acceptance example, not a claim that insecure split mode is enough.

## Open Questions

- **Q1 — NON-BLOCKING: final editor toolkit.** Qt Quick/Quickshell feasibility
  assignment `asg_c022859a-1ab5-46b1-941d-c4ba236d423e` supplies evidence, not a
  toolkit ruling. Report `art_114d275d` (SHA-256
  `be59ae69a4d6346def0d0a809c372126285c6a9d958646358f852871c0482f86`) records
  12 passing offscreen assertions on racter with Qt/PySide6 6.11.2: independent
  overlays, preserved typing focus, wrap/scroll geometry, and local edit deltas.
  Quickshell was unavailable; this is not full writing-loop evidence. The report
  lives at `racter:/home/clu/.tightbeam/work/d9274efe5684/drift-editor-spike/REPORT.md`.
  Existing request `dr_fb76ce2a-bca9-46da-8115-3472275e2394` covers toolkit/trust
  choices. The PO owns the toolkit decision; the orchestrator applies that
  ruling. Build the neutral editor/service boundary above.
- **Q2 — NON-BLOCKING: remote access-control mechanism.** Options for the PO
  include a protected private tunnel with participant credentials, TLS with
  application credentials, or mutual TLS with participant mapping. These are
  options, not selections or permission to deploy. The PO chooses connection
  trust/access specifics through existing `dr_fb76ce2a` before split access is
  accepted. Work independent of that mechanism proceeds against I6.
  No unauthenticated network fallback.
- **Q3 — NON-BLOCKING: license.** PO/user chooses. Private development proceeds;
  declaring a license or releasing under one awaits that choice.

No other load-bearing question is intentionally left open. Implementation
questions that change these contracts return to the spec writer; rulings amend
this canonical file before the affected build proceeds.
