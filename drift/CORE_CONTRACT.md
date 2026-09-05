# Drift — slice 1: persistent document and thread core

## Goal

Build a runnable private document service that creates and reads text documents,
accepts revision-matched edits, refuses stale edits without losing writing,
persists anchored threads and replies, and recovers state and durable events
after restart or client reconnect. This slice needs no GUI or agent harness.

Authority: [SPIRIT.md](SPIRIT.md), [MIKE_PRODUCT_BRIEF.md](MIKE_PRODUCT_BRIEF.md),
format ruling `dr_d9f53dfc`, PO receipt
`att_99414a35-50e6-4b4b-a97e-14eaa280ad6f`, and the slice-first direction on
`asg_13f64a20-ca20-4f9a-ac2d-fa38391b991c`. Work item:
`wi_9069f091-53a7-41ff-8b7b-a7d07c188bde`. Code: `clickety-clacks/drift`.

This is the normative home of the core contract, extracted from the earlier
whole-loop draft [TECH_SPEC.md](TECH_SPEC.md). It supersedes that draft's core
clauses; the draft remains context for later editor/adapter/topology slices.
Core review and implementation do not depend on those later slices' choices.

## Non-Goals

Editor toolkit, selections/presence, suggestions and decisions, thread resolution,
GUI autosave/undo, external-agent CLI/wait, and split-topology access-control
implementation belong to later slices on the same assignment. They remain MVP
obligations, not requirements for accepting this service-core milestone.

No rich text, rendered preview, embedded AI, mandatory MCP or hosted service,
fuzzy reattachment, offline merge, revision/event compaction, or multi-server
coordination. No release, installation, deployment, or live-state mutation.

## Terms

- **Document**: opaque service ID, title, format (`text` or `markdown`), and head
  text revision. Markdown is source text using the same representation as text.
- **Revision**: immutable document text, document-local increasing revision
  number, parent revision, producing command ID and actor, and replacement delta.
  Creation produces revision 1 without a parent; each accepted edit adds one.
- **Range**: half-open `[start,end)` in Unicode scalar values of a named revision.
  Equal endpoints mean insertion. Bytes, UTF-16 units, and grapheme clusters are
  not protocol positions. Text uses LF; clients convert CRLF before submitting
  and compute offsets after conversion. No Unicode normalization occurs.
  The service rejects CR characters in document/replacement text as
  `invalid_request` instead of silently changing text or offsets.
- **Actor**: stable participant ID and display name supplied by the service's
  trusted request context. The core stores authorship but does not choose the
  later authentication mechanism. Human and agent receive the same core actions.
- **Anchor**: original document/revision/range and exact quote, plus its current
  attached range or detached reason. The immutable original revision retains
  surrounding text as the context fingerprint; no separate hash or fuzzy index
  is required. The original passage is nonempty.
- **Thread**: stable ID, anchor, and ordered messages. Each message has a stable
  ID, actor, and body. The initial question is the first message; replies append.
- **Event cursor**: document-bound position in its durable event order, distinct
  from text revision. Discussion creates events without changing text revision.

## Assumptions

1. One service process owns a configured durable store whose files survive
   process restart. Disk loss and failover are outside this slice.
2. Core demonstrations use disposable private data and test identities on a
   development host. Tests run on racter or eezo, not Gibson.
3. An outer request boundary supplies a trusted actor ID. A private fixture can
   supply test actors there without selecting product credentials or trust policy.
   Such a fixture proves core behavior, not authenticated product access.
4. Toolkit, remote access specifics, and license remain open. None is necessary
   to build or review this core. The service interface can receive an eventual
   access-control wrapper without changing document semantics.

## Invariants

**C1 — One mutation boundary.** The service executes each durable command in one
transaction: validate base revision and target, mutate state, append its event,
and store its retry receipt. It acknowledges only after durable commit.
Given two edits based on revision 1, when they race, then one produces revision 2
and the other refuses without a partial write (T2).

**C2 — Refusal preserves writing.** A rejected command changes no document,
revision, thread, message, or event. Its error returns the submitted command and
the current revision so the caller can preserve and reconsider it. The caller
retains the original payload until it knows the result; network silence does not
mean refusal. Given an old edit, when newer text exists, then `stale_revision`
leaves that text intact and the submitted replacement remains recoverable (T2).

**C3 — Anchors follow edit history.** The service derives current attachment from
the ordered revision deltas and original passage, not from a search for similar
text. Given two identical sentences, when the first is deleted, then its thread
detaches and retains its messages instead of attaching to the second (T3).

**C4 — State and recovery share the commit.** Durable state, event order, and
retry results survive restart together. Given a lost reply acknowledgement,
when the caller retries its command after restart, then exactly one reply and
one event exist (T4). Replay plus a prior coherent snapshot reconstructs the
same core state as a fresh snapshot (T5).

## Architecture

### Persistence and commands

The service is the only owner of documents, revisions, anchors, threads/messages,
events, and retry receipts. Storage engine and language are engineering choices.
Retain these records for this MVP; no retention service or background broker is
needed. Thread creation and replies retain the current text revision.

The named pattern **revision-checked command** applies to durable document
actions. For example, `edit(D, baseRevision=1, [0,3), "New", commandId=X)` either
commits once against revision 1 or returns a recoverable error. It establishes
no Tightbeam operating pattern and does not govern later transient presence.

A command envelope contains `commandId`, `type`, and its payload. Commands on an
existing document also carry `baseRevision`. Document IDs are explicit in the
route/context. The trusted request context supplies `actorId`; a body field
cannot override it. Validate malformed inputs and range bounds without mutation.
Document/thread/message IDs are service-generated and remain stable on retry.

For each command, first check the receipt keyed by actor and command ID. An
identical command (same document, type, base revision, and payload) returns its
original success, even if that base revision is now old. Different content with
the same key returns `command_id_conflict`. Concurrent retries also commit only
once. Otherwise check `baseRevision == headRevision` atomically with the write.
On mismatch return `stale_revision`; do not automatically rebase or merge.
After a refusal the caller can refetch and explicitly submit a new command ID.

A successful command returns `commandId`, `documentId`, resulting `revision`,
event `cursor`, and its affected object/result. An error returns `code`, `reason`,
`submittedCommand`, and, for an existing accessible document, `currentRevision`.
Codes needed here: `stale_revision`, `invalid_range`, `invalid_request`,
`not_found`, `command_id_conflict`, and `invalid_cursor`. Storage failure returns
an explicit failure; an interrupted connection leaves an unknown outcome for
same-ID retry. A refusal never reports saved. This is an API preservation
contract; GUI crash recovery is a later client contract (T2, T4).

### Minimal runnable service surface

Use JSON HTTP commands/reads for the slice. Endpoint spelling below is a concrete
integration contract; an engineering transport change may preserve these
semantics without a product DR. This slice does not require a WebSocket: durable
cursor retrieval supplies reconnect recovery. Later live subscriptions build on
the same event order, without changing durable command behavior.

| Request | Input and result |
| --- | --- |
| `POST /documents` | Envelope type `create`; payload `title`, `format`, `text`. Returns new document ID, revision 1, creation event cursor. Empty text is valid. |
| `GET /documents` | Returns document IDs, titles, formats, and head revisions. |
| `GET /documents/{D}` | Returns one coherent snapshot: document metadata, head text/revision, threads with anchors/messages/authors, and a cursor captured from the same read. |
| `GET /documents/{D}/revisions/{R}` | Returns exact retained revision text and metadata. A reader obtains passage and context with its range; current text is not substituted for R. |
| `POST /documents/{D}/commands` | Envelope type `edit`, `comment`, or `reply`; requires `baseRevision`. Returns durable acknowledgement or structured error. |
| `GET /documents/{D}/events?after={C}` | Returns ordered durable events strictly after C, `nextCursor`, and `hasMore`. No events means an empty list and unchanged cursor. A documented start cursor means before creation. |

`edit` payload is `{start,end,text}`: replace one validated range in the base
revision. Empty replacement deletes; empty range inserts. Keep unaffected text
unchanged. `comment` payload is `{start,end,body}`: create a thread on a nonempty
base-revision passage; the service derives its quote and stores the first message.
`reply` payload is `{threadId,body}`: append to that document's named thread,
including when its anchor is detached. Discussion bodies are plain text.
Empty message bodies and out-of-document targets fail validation (T1, T3).

Use HTTP success statuses for completed reads/writes, 409 for stale revision or
command-ID conflict, 400 for malformed inputs/ranges/cursors, and 404 for missing
objects. Service storage errors are 5xx, never a successful acknowledgement.
The actor comes from the request boundary, not from route spelling (C1, C2).

The builder documents startup, configured bind/port and store path, and HTTP
examples for create/read/edit/comment/reply/replay. The private core fixture
binds only to loopback with disposable data. Configurable storage and port must
work without source edits. It is not a split deployment or a product security
demonstration; no network exposure or live credentials are authorized (T1, T4).

### Anchor transform

For a current attached range `[s,e)` and next revision's replacement `[a,b)`
with replacement length `n`, apply these ordered rules in the edit transaction:

1. If `b <= s`, shift both endpoints by `n - (b-a)`.
2. Otherwise, if `a >= e`, retain both endpoints.
3. Otherwise, detach. Use `passage_deleted` when an empty replacement covers
   the entire passage; use `passage_changed` for other overlap, including an
   insertion strictly inside the passage.

Insertion at the start shifts the original passage past the inserted text;
insertion at the end leaves the passage unchanged. An attached range must still
select the original quote in the resulting revision. Missing history or a quote
mismatch produces `unverifiable`; a mapping with more than one possible target
produces `ambiguous` and selects none. The ordered-delta path needs no fuzzy
candidate search. Duplicate prose alone does not create ambiguity (T3).

Return `anchor.status` as `attached` with `currentRevision/start/end`, or
`detached` with `reason` and no current range. In both cases retain original
revision/range/quote and messages. These API fields make lost attachment visible
to a core client; the later GUI supplies its presentation. A detached anchor
stays detached even if identical text returns. A participant may create a new
explicitly selected thread. Accepting visible detachment avoids guessing;
deleting the thread instead would discard writing (T3).

### Events and recovery

Append one event for each successful create/edit/comment/reply. Each event
contains its document-bound cursor, document ID, command ID, actor ID, event
type, and resulting text revision. Its payload contains the new document,
replacement and affected anchor states, new thread, or new reply, respectively,
so a client can update a prior snapshot without guessing. Event ordering is
strict within a document; no cross-document order is required.

Replay returns an ordered prefix of the events after the supplied cursor.
`nextCursor` names the final returned event (or retains the input when empty).
`hasMore` states whether further committed events existed at the read boundary.
The caller keeps reading from its last processed cursor, even after reconnect;
an event committed after an empty response appears on a subsequent read. Invalid,
future, or wrong-document cursors fail explicitly rather than starting at the
present. Clients deduplicate repeated delivery by cursor (T5).

Snapshot data and its cursor come from the same consistent read. Events after
that cursor cover later changes. Restart with the same store returns the same
committed state, cursors, and receipts; it does not reset event numbering.
An interrupted transaction yields either the prior state or the whole commit,
including event and receipt, not a partial document/thread update (T4, T5).

## Acceptance

These are service-core checks, derived from PO [ACCEPTANCE.md](ACCEPTANCE.md)
examples 3–6 and the slice-first receipt. They do not claim full GUI/harness or
split-topology acceptance. Record candidate commit, actual test host, startup
and request commands, input/output, restart evidence, and any limitations.

- **T1 — Runnable core (C1; API).** Given a fresh configured store and two fixture
  actors, when one creates `alpha beta gamma` as text, then list/read return its
  ID and revision 1. Create a comment on `[6,10)` and have the other actor reply.
  Then the snapshot returns quote `beta`, ordered messages and both authors,
  still at text revision 1. Repeat document creation with Markdown source and
  empty text. No toolkit, model, or vendor account participates.
- **T2 — Revision safety (C1, C2).** Given revision 1, submit two edits with that
  base. When one commits, then the other returns 409 `stale_revision`, its exact
  submitted text, and current revision 2. Read both retained revisions; neither
  original nor accepted bytes are lost. Read revision 2 and submit a fresh
  command; it succeeds. Invalid ranges and stale comments/replies cause no
  partial state or event. Concurrent requests exercise the atomic comparison.
- **T3 — Honest anchors (C3).** Given T1's thread, insert before/after `beta` and
  at each boundary; then its current range still selects exactly `beta`.
  Replace inside it; then it detaches with `passage_changed`, quote and messages
  intact, and still accepts replies at the current revision. Delete the first
  occurrence in `same. same.` under its thread; then `passage_deleted` has no
  range on the second occurrence. Check scalar offsets using emoji and
  combining-mark text before the passage. Fault fixtures for missing history,
  quote mismatch, and a non-unique mapping must return visible detached reasons,
  not a guessed passage; no fuzzy-matching mechanism is required by the fixture.
- **T4 — Restart and retry (C1, C4).** Given acknowledged text, question and reply,
  restart the process with its original store. Then snapshots and old revision
  reads preserve their content and authors. Interrupt a reply around commit
  acknowledgement; retry its identical command after restart. Then exactly one
  reply/event exists and its receipt returns the original result. Reuse its ID
  with changed content; then conflict leaves state unchanged. An incomplete
  transaction does not corrupt the prior state. Repeat using a different
  configured store path/port without editing source.
- **T5 — Reconnect (C4; replay).** Given snapshot cursor C, disconnect the reader,
  edit text and append a reply, and restart the service. When the reader replays
  after C, then applying those events reconstructs the fresh snapshot. Repeat
  a read around a concurrent commit and an empty result; no durable event is
  skipped. Repeating a cursor may repeat delivery, not durable effects. Reject a
  wrong-document or future cursor visibly. Pagination, if used, preserves order.

## Open Questions

**No blocking core question.** Language, storage library, and transport internals
are engineering choices within this contract. The private fixture's trusted
  actor context is not approval of a product trust model.

**NON-BLOCKING, later slices:** final editor toolkit and remote trust/access
mechanism remain PO-owned under existing
`dr_fb76ce2a-bca9-46da-8115-3472275e2394`; license also remains undecided. These
questions live with the later editor/adapter/topology draft in
[TECH_SPEC.md](TECH_SPEC.md). Neither their answer nor that draft's completion
gates independent review and implementation of this core.
