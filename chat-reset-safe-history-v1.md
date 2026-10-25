# Chat reset-safe history and message attribution amendment — v1

Status: PROPOSED, 2026-10-25. Pending independent review.

This amendment changes four adopted contracts, read at public specs commit
`1cd0b0ee8f681b10153fd10cda5bfe38ec2c5db8`:

| Contract | SHA-256 at that commit |
|---|---|
| `rest-state-api-v1.md` | `ade39c16159d518d92dd14f3f003dcf02b417764808a03fd2e1d2bd046ac12e2` |
| `rest-state-api-v1-wire-schema.md` | `4c52e940f3cf7f86139701f0b0066a15bcb9779d76ded92cf1da44f9f69ec68c` |
| `event-firehose-v1.md` | `6b4cafb0016b48e49708fa18cd9726ca2741c419d567ac537fc3b18caf7e7a86` |
| `transcript-verb-v1.md` | `21b80ccae00b5500f15e76e5333cb397f7d30340323988e19499d2ed5b3b547e` |

The companion files in this revision already carry the clause changes listed
in section 8. Where this amendment and those texts disagree, this amendment
governs once adopted.

## 1. Spirit

The intent this amendment serves, from the governing product rulings:

- "messages must not disappear. Firehose plus REST is the one authority."
- "clearedThroughSeq marks an agent-context restart, never hides earlier
  human-visible REST history or Firehose rows. After harness changes,
  turn-failure recovery or any reset, the human still sees earlier words and
  replies, with a boundary marker. Agent context visibility is unchanged."
- "WIRE requires nonempty sender for human rows; document actual served
  fields/classes used by Chat and state unserved ones absent; any re-emitted
  update gets a new rowVersion."
- "[The ruling] includes Chat-visible tool records and transition rows as
  earlier human-visible transcript history. clearedThroughSeq marks
  agent-context restart, not a REST-history/Firehose visibility cutoff for
  those rows; agent context exposure remains unchanged."
- "nonempty sender for human rows includes empty strings. Spec and code treat
  empty human sender the same as NULL so no human row is served without
  attribution. No new repair or reconstruction of historical original-poster
  ambiguity is wanted."

## 2. Terms

- **History boundary** (`clearedThroughSeq`, written F): the per-session `seq`
  at which the agent's working context last restarted. After this amendment it
  is a position, not a filter.
- **Visible set**: every R7 transcript-message row of the target session,
  ordered by R5a `(seq,id)`. It no longer depends on F.
- **Boundary marker**: a transcript row with `messageType:"marker"` and a
  `marker` object, appended when F advances.
- **Agent context**: what the harness gives the model when a turn starts: the
  native harness session state and, after a harness change, the handoff
  messages selected through the handoff `seq`. A CLI or REST read the agent
  performs during a turn is a lookup, not agent context.
- **Human row**: a transcript-message row with `role:"user"` whose stored
  `messageType` is null, so the item omits `messageType`.
- **Attribution path**: the shared read projection that fills a human row's
  sender as `user:<principal>` from the row's direct turn or source-wake
  principal, else from the session owner.
- **Served projection** of a message: the R7 item bytes REST returns and
  `message.created` carries for that message.

## 3. Assumptions

Each can be falsified by a source read or a served response.

- AS-A. No agent-context path reads F. In public 0.1.12 the only readers of F
  are the REST/CLI transcript query, the session serializer, and the legacy
  socket's authentication replay; the harness handoff uses its own
  `handoff_through_seq`.
- AS-B. In public 0.1.12 the harness-change path advances F and appends its
  `harness-switch` marker in one transaction.
- AS-C. The attribution path exists in a pending attribution change, and this
  amendment reuses it rather than duplicating it. Without further change it
  passes a nonnull stored sender through, including `""`.
- AS-D. A gateway restart or upgrade makes every Firehose client rebuild under
  M2. A served-projection change that an upgrade causes is covered by that
  rebuild, not by a version bump.
- AS-E. Historical role-user rows with a null `messageType` are treated as
  human rows even when an old non-human origin wrote them. They get owner
  fallback attribution like any unlinked human row.

## 4. Non-goals

- No new route, query parameter, filter, notice class, or retention rule.
- No security hardening, identity check, or device predicate.
- No overflow (4008) fixture, driver, probe, or test; the existing
  unattributed-4008 limitation stands.
- No reconstruction of the original poster of an unlinked legacy row. Owner
  fallback stands even when the original poster was someone else.
- No physical deletion of transcript rows, and no change to F's writers,
  causes, or monotonicity.
- No change to agent context: what a restarted model remembers stays as it is.
- No contract for the unpublished fields in section 7.2; their own amendment
  specifies them.
- No client workaround.

## 5. History requirements

H1. The REST transcript-messages collection SHALL return the visible set
without reference to F. Tail, `before`, `after`, `hasMoreBefore`, and
`hasMoreAfter` SHALL operate on the visible set. *(Serves: "never hides
earlier human-visible REST history".)*

> Example: a session has rows `seq` 1–120 and F = 100. The cursorless tail
> with `limit=50` returns 71–120 with `hasMoreBefore:true`; paging `before`
> reaches row 1 and stops with `hasMoreBefore:false`. Before this amendment
> paging stopped at 101.

H2. When F advances, no row SHALL leave the visible set. Every page SHALL
equal the page the same request returns over the same committed rows with F
ignored. The only row an advance adds is its H3 marker, so a page can differ
from the same request made before the advance only by that marker and by
other rows committed since. *(Serves: "never hides earlier … REST history or
Firehose rows".)*

> Example: a client holds `oldestCursor` at `seq` 90 and `newestCursor` at
> `seq` 120. F advances from 0 to 120 and the H3 marker is appended at 121.
> `before=<oldestCursor>` returns rows below 90, exactly as before the advance.
> `after=<newestCursor>` returns the marker at 121. Before this amendment the
> `before` request returned an empty page.

H3. When `advanceClearedThroughSeq` changes the stored F to F′, the same
commit SHALL append one boundary marker with `seq > F′`. Its kind SHALL be
`harness-switch` for the harness-change cause and `session-restart` for the
turn-failure-recovery cause. The `session-restart` marker's `from` and `to`
SHALL be the old and new native harness session ids, as for the existing
pointer-fallback marker. A no-change call SHALL append no marker. *(Serves:
"the boundary is visible in transcript"; "with a boundary marker".)*

> Example: a harness change at maximum `seq` 120 sets F = 120. A REST read
> that returns the session with F = 120 also finds a marker row at `seq` 121
> with `marker.kind:"harness-switch"`. A second identical call leaves F at 120
> and adds no row.

H4. A boundary marker's `content` SHALL NOT state that earlier messages are
hidden, removed, or no longer shown. It MAY state that the agent no longer
remembers them. *(Serves: "the human still sees earlier words and replies";
the public 0.1.12 `harness-switch` text says they are "no longer shown here".)*

> Example: after a harness change, the marker's content contains no claim that
> earlier messages are not shown, and the rows before it are still returned
> by REST. The existing `session-restart` text ("Earlier messages stay visible
> here, but the agent no longer remembers them.") already passes.

H5. A boundary advance SHALL leave agent context exactly as it is without this
amendment. *(Serves: "Agent context visibility is unchanged".)*

> Example: for the same session state and harness change, the new harness
> receives the same handoff message set, and a turn-failure recovery starts
> the same fresh native session, whether or not this amendment is built.

H6. A client building or recovering conversation state SHALL treat a session
notice that changes F as an ordinary last-version-wins session update. A
change in F SHALL NOT cause a client to drop rows, reject a snapshot, or
rebuild. Reconnect, a Firehose sequence skip, and other M2 doubt still
rebuild. *(Serves: "never hides … Firehose rows"; F no longer changes the
visible set, so the boundary-specific recovery has nothing left to protect.)*

> Example: during a cold build the buffered prefix holds a session notice
> with a higher `rowVersion` and F = 120, and message notices for rows 118–122.
> The client advances the session item, applies all five messages, and
> publishes. No row at or below 120 is omitted, and no rebuild starts.

H7. The CLI `transcript` wrapper SHALL keep returning the same envelope,
items, and cursors as direct REST (REST A53). It therefore returns the full
visible set to every caller, including an agent reading its own session.
*(Serves: "Firehose plus REST is the one authority"; one projection, no second
pattern. See open question Q3.)*

> Example: an agent runs `transcript --session <its own key>` after a harness
> change and receives rows below the boundary, equal to the REST response.

## 6. Attribution and version requirements

S1. When REST or `message.created` serves a human row, its `sender` SHALL be
a nonempty string. *(Serves: "WIRE requires nonempty sender for human rows";
"no human row is served without attribution".)*

> Example: no REST page or `message.created` payload contains a human row
> with `sender:null` or `sender:""`.

S2. A human row whose stored sender is null and one whose stored sender is
`""` SHALL go through the same attribution path and be served with the same
value. A nonempty stored sender SHALL pass through unchanged. *(Serves: "treat
empty human sender the same as NULL"; the ruling to reuse the existing sender
work rather than duplicate it.)*

> Example: two unlinked legacy human rows in a session owned by user `u1`,
> one stored null and one stored `""`, are both served with `sender:"user:u1"`.
> A row stored with `sender:"user:u2"` is served with `"user:u2"`.

S3. When the attribution path cannot find a direct turn or source-wake
principal, it SHALL use the session owner and SHALL NOT infer a poster from
content, device, or other fields. *(Serves: "No new repair or reconstruction
of historical original-poster ambiguity is wanted".)*

> Example: an unlinked legacy post that another user made into `u1`'s session
> is served as `user:u1`. That is the accepted limit, not a defect.

V1. When a message's served projection changes, its `rowVersion` SHALL be
strictly greater than every version previously served for that message id.
Two `message.created` notices, or a notice and a REST item, that carry the
same `(id,rowVersion)` SHALL carry identical items. *(Serves: "any re-emitted
update gets a new rowVersion"; REST I6.)*

> Example: a queued human message is published at acceptance with
> `turnSeq:null` and `rowVersion` v. On delivery it is published again with
> `turnSeq:42`. The second notice carries a version greater than v, and a
> REST read after delivery returns that greater version with the same item. A
> pure duplicate of the first notice with the same version and the same bytes
> is still allowed and converges under M1.

V1 does not require `rowVersion` to equal `seq`. Per AS-D, it covers changes
inside one running build, not projection changes an upgrade causes.

## 7. Served fields and classes

Claims here are labeled by evidence subject. "Public" means the published
0.1.9 and 0.1.12 source lines. Every claim is a source reading; none is proof
of a specific installed build.

### 7.1 Public 0.1.9 and 0.1.12 (normative for this contract)

E1. The transcript-message item SHALL include `marker` only when the row has a
stored marker. `marker` is the closed object `{kind, from, to}` of three
strings. Its position is immediately after `messageType`. `kind` is one of
`harness-switch`, `model-retune`, `session-restart`; this enum is closed.
Markers travel as `message.created`; no `transition.recorded` class exists.
*(Serves: "document actual served fields/classes used by Chat"; served in both
public lines but missing from the R7 table and the wire schema.)*

E1's closed enum and its class sentence describe the public lines. Section
8a states what replaces them if the tool-call and transition amendment lands.

> Example: a harness-change marker item reads
> `…"messageType":"marker","marker":{"kind":"harness-switch","from":"…","to":"…"},"content":…`;
> an ordinary assistant item has no `marker` key.

E2. `message.created` notices SHALL carry `resource:"messages"`. *(Serves:
"document actual served … classes".)*

E3. The public transcript-message item does not include `turnIncludesHuman`
or `isBatchCarrier`. The public turn item does not include `triggerSource` or
`batchMemberCount`. The public Firehose registry does not include
`turn.queued`. No public line includes `transition.recorded`. A client SHALL
treat each of these as absent. *(Serves: "state unserved ones absent".)*

> Example: a client decoding public 0.1.12 output finds none of these keys or
> classes, and degrades to the behavior it has without them.

### 7.2 Unpublished (not part of this contract)

A pending change, not yet published, adds `turnIncludesHuman` (omitted when
unknown) and `isBatchCarrier` (emitted only when true) to transcript-message
items, `triggerSource` and `batchMemberCount` to turn items, and the
`turn.queued` class. It also holds the re-publication path that V1 corrects.
The reviewed amendment that publishes it specifies these and amends E3. This
amendment says nothing more about them.

## 8. Clause changes in the companion specs

### `rest-state-api-v1.md`

- Status: adds this amendment's PROPOSED note.
- R5d paragraph 1: defines the history boundary as a position, states H1 and
  H2, and keeps "the observable value of `F` is non-decreasing". It deletes
  the sentences on reading F as part of one indivisible read, "Cleared rows do
  not make either page flag true", and "A production mutation cannot expose a
  row that an earlier value of `F` hid".
- R5d writer paragraph: keeps the initializer, the sole seam, and the
  two-cause inventory, and adds H3, H4, and H5.
- R5d cursor paragraphs: keeps "does not contain `clearedThroughSeq`" and
  deletes the paragraph on cursors at or below the boundary, keeping its
  caught-up `after` sentence. The rebuild sentence drops "or a
  history-boundary change" and adds that a boundary change invokes no rebuild.
- R7 conditional-key sentence: `messageType` and `marker` are the only
  conditionally omitted transcript-message keys.
- R7 transcript-messages field list: inserts `marker` after `messageType`.
- R7m: adds E1's presence, shape, closed kind enum, and class sentence.
- New R7s: S1–S3 and V1, with their examples.
- A51a: H1's and H2's examples. A51c: "An advance removes no row from the
  transcript route and appends its R5d boundary marker in the same commit",
  with H3's and H4's examples. A52: each page equals the page the same request
  returns over the same committed rows with `clearedThroughSeq` ignored, and
  the advance adds only its R5d boundary marker. A53: adds H7's example.

### `rest-state-api-v1-wire-schema.md`

- Status: adds this amendment's PROPOSED note.
- Conditional-key sentence: `messageType` and `marker` are the only
  conditionally omitted transcript-message keys.
- Adds the `marker` presence rule, the human-row `sender` rule, the
  `TransitionMarker` shape `{kind:S, from:S, to:S}`, the optional-key
  sentence, the table entry `marker O<TransitionMarker>`, the nullable
  `sender` exception for human rows, and the closed
  `TransitionMarker.kind` domain `harness-switch|model-retune|session-restart`.

### `event-firehose-v1.md`

- Status: adds this amendment's PROPOSED note.
- R4b: adds E2 and the class half of E3, and states that boundary markers
  travel as `message.created`.
- `message.created` R8 row: adds V1.
- M4 snapshot cut: "must match in both `rowVersion` and `clearedThroughSeq`"
  becomes "must match in `rowVersion`". The sentence on a higher session
  version invalidating the candidate becomes H6: such a version is an
  ordinary upsert.
- M4 chat client: deletes "or a session history-boundary change" from the
  rebuild triggers and "the mandatory rebuild for every newer
  different-boundary session notice", and adds H6 with its example.

### `transcript-verb-v1.md`

- Status: adds this amendment's PROPOSED note. Authority: "visibility-floor"
  becomes "history-boundary".
- Non-goals: deletes "does not expose messages at or below the session's
  `clearedThroughSeq`".
- T2: the visible set. T3: the history boundary. T6: deletes "a session
  history-boundary change". AS4: deletes the boundary-change rebuild clause.
- I3: adds H7. I5: "A message page does not depend on `clearedThroughSeq`."
  I6a: "cannot make a cleared message visible again" becomes "never removes a
  row from the visible history".
- Deletes the boundary-cursor list after the page-flag paragraph.
- Cold build: step 3 records only `V0`; step 5 accepts when `V1 = V0`. Step 7
  deletes the different-boundary rejection and "omit the message when its
  `seq <= F1`". Step 8 deletes the different-boundary invalidation. All
  higher session versions are ordinary updates (H6).
- A4: given a held tail page and a boundary advance through it, the held rows
  stay, the `before` cursor returns the same page as before, the `after` cursor
  returns the boundary marker and any later rows, and a cold rebuild returns
  the held rows and the marker.
- A4b: "no cleared message becomes visible" becomes "no visible message is
  removed".
- A5: keeps the covered-version and session-mutation rejections, replaces the
  boundary rejection and invalidation sentences with H6's example, and ends
  "Every accepted slice includes rows at or below its session's boundary."
- A7: adds H7's example.

## 8a. Composition with the tool-call and transition amendment

The tool-call and session-transition records amendment
(`tool-call-and-session-transition-records-v1.md`, SHA-256
`86c9495f5998d59574c4221ac2b4ce8bf64b44fb6796e7731e7d0e280c4a8f27`) edits
`rest-state-api-v1.md`, `rest-state-api-v1-wire-schema.md`, and
`event-firehose-v1.md`. It does not edit `transcript-verb-v1.md`. This
amendment lands first; the tool-call amendment composes onto it. When both
apply, these rules compose them.

C1. History boundary. F SHALL NOT filter the tool-calls collection, its page
flags, or tool-call notices. A tool record anchored at or below F stays in the
collection and emits its notices as any other record does. *(Serves: "never
hides earlier human-visible REST history or Firehose rows"; "includes
Chat-visible tool records and transition rows as earlier human-visible
transcript history".)* The tool-call amendment's TC13 and FH5 state the same
rule for its collection and notices, so the two texts agree.

> Example: the tool-call amendment's TC13 example. Message 500's turn was
> interrupted mid-call, leaving a tool record anchored at 500. A harness
> change sets F = 500 and appends its marker at 501. The record anchored at 500 stays in the collection, as message 500
> stays in the messages collection under H1, and a later terminal update for
> it emits `tool_call.ended`.

C2. Marker field. E1's field placement and the tool-call amendment's TR4 are
the same edit. The R7 and wire-schema `marker` insertions SHALL be made once.
Where the tool-call amendment has landed, section 8 drops its R7 and
wire-schema `marker` bullets.

C3. Marker kinds. Where the tool-call amendment has landed, its TR5 replaces
E1's closed kind enum: producers emit `harness-switch`,
`model-retune`, `session-restart` or `context-compacted`, and readers accept
an unknown kind. H3 still names the kind a boundary advance writes. H4
applies only to markers H3 writes, so a `context-compacted` marker is outside
it.

C4. Marker class. Where the tool-call amendment has landed, a marker message,
including one H3 writes, emits `transition.recorded` in place of
`message.created` (tool-call amendment FH2). E1's "markers travel as
`message.created`" sentence and E3's "No public line includes `transition.recorded`" become claims about the
public 0.1.9 and 0.1.12 lines only. V1 covers a transcript-message item
whichever of the two classes carries it.

C5. Chat recipe. The tool-call amendment and section 8 both edit the M4 chat
client paragraph. Composed, the client subscribes as the tool-call amendment
states and rebuilds as section 8 states, with no rebuild for a boundary
change in either collection.

## 9. Open questions

Q1 (NON-BLOCKING). The legacy socket still uses F as its replay floor, and the
harness-change path still sends a legacy `stream_history_cleared` broadcast.
The ruling names REST, Firehose, the wire schema and the transcript verb, not
the legacy socket, so this amendment leaves both alone. Should the legacy
socket also stop hiding history, or wait for its retirement?

Q2 (NON-BLOCKING). REST R5d's inventory names a turn-failure-recovery caller.
No such boundary writer exists in public 0.1.12; there the harness change is
the only writer. H3's `session-restart` clause applies wherever that caller
exists on the target line and is vacuous where it does not.

Q3 (NON-BLOCKING). H7 resolves by spirit that the `transcript` CLI shows the
full history to agents too, because it is defined as REST. The alternative, a
CLI that hides pre-boundary rows from agents, would make two projections of
one collection.

Q4 (SETTLED). Sequencing. This amendment leads the 0.1.12 slice on the public
specs main line. The tool-call and transition amendment stays after 0.1.12 and
composes onto this one through section 8a. The pending attribution change's
0.1.12 port is unchanged by either.

Q5 (NON-BLOCKING; sequencing dependency for joint publication only). The
scope is settled: tool and transition rows are human-visible history, and F
hides none of them (section 8a C1). The reviewed tool-call amendment conforms
to C1 in TC13 and FH5. Publishing or accepting the two together still requires
composing them on one exact subject and reviewing that subject. This
amendment proceeds without it.
