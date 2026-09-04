# Pragmatic late-ruling handoff v1

Status: cold digest completed 2026-09-04; candidate for fresh independent review.
Work item: `wi_60f879d9-f1cd-4461-82c7-7f1e922d75db`
Incident decision: `dr_07bdef13-45ae-435f-bc79-b2dc6b0a5ebf`

This file carries no implementation, target, merge, deploy, install, release, or
live-state authority.

## Goal

Keep an operator ruling actionable when it arrives after the assignment named by
the request became terminal. The substrate must deliver that late ruling to the
nearest active session in the existing opener-or-owner lineage. The accountable
owner must be able to record one durable receipt for the commit or operational
action that incorporated the ruling. A caller that explicitly opens a successor
assignment must carry each applicable ruled-but-unconsumed decision id into the
new assignment subject.

This contract applies the same observable behavior and proof to product line
`0.1.9` and to `main`, the `0.2.0` line. It adds one regression that reproduces the
loss of `dr_07bdef13-45ae-435f-bc79-b2dc6b0a5ebf` from revocation through late
ruling, active-owner delivery, successor carry, and recorded consumption.

## Non-Goals

- This contract does not create an authority, adjudication, arbitration, or
  decision engine.
- This contract does not backfill a marker, notification, successor subject, or
  consumption receipt for a ruling that predates activation of this contract.
- This contract does not scan specifications, guidance, commits, assignments, or
  decision text for contradictions.
- This contract does not add or alter a database migration.
- This contract does not add a readiness, merge, release, install, deploy, or
  identity-apply gate.
- This contract does not redesign a REST projection, Firehose projection, work
  projection, job trace, lifecycle or Firehose event vocabulary, or decision-request
  status vocabulary.
- This contract does not change statute, effort, or agent-question workflows. It
  changes only an operator decision request whose attached assignment is terminal
  when the request owner rules it.
- This contract does not infer that two assignments have the same intent. A caller
  declares a successor with the input defined below.
- This contract does not change `decision_requests.status`,
  `decision_requests.consumedAt`, or the existing authorization-consumption
  meaning of those fields.
- This contract does not edit or supersede `immediate-identity-apply-v1.md`, its
  exact candidate commit
  `703cbb8c04640cf082de9171a7eddf66333addcd`, or a canonical file owned by
  `wi_7dfe752d-b8a8-414b-be30-1fa7106a0913`.
- This contract does not change product line `0.1.8`.
- Operating pattern taught to agents: when an assignment replaces or continues a
  terminal assignment, open it with `assign --succeeds <assignmentId>` or
  `dispatch --succeeds <assignmentId>`. The persisted subject then carries the
  applicable decision ids without prose copying.

## Terms

- **Operator decision request**: a `decision_requests` row whose `kind` is
  `operator`. This document calls it a **request**.
- **Request owner**: the user named by the request's existing `ownerUserId`.
- **Source assignment**: the assignment row named when the request's existing
  `assignmentId` field is non-null.
- **Terminal source**: a source assignment whose existing `state` is `closed`.
  Completion, surrender, and revocation are the three existing outcomes that close
  an assignment.
- **Accountable owner**: the source work item's existing `ownerUserId` when the
  source has a work item; otherwise the request owner.
- **Late ruling**: the successful `open` to `ruled` transition of a request while
  its source is terminal in the same state transaction. Elapsed time does not make
  a ruling late.
- **Opener-or-owner lineage**: the finite ordered recipient list constructed from
  the source assignment's existing `openedBySession`, that session's existing
  effective operational-parent chain, the source assignment's existing
  `openedByUser`, and the accountable owner. A user contributes
  `Org.personal_session_key(userId)`.
- **Active candidate**: a session row in the opener-or-owner lineage whose existing
  state is `active` at recipient selection time.
- **Late-route marker**: one reserved substrate occurrence fact with exact kind
  `operator-ruling-late-routed`, scope equal to the full decision-request id, and
  origin `process:tightbeam`. The marker says that the post-activation late-ruling
  path completed. It does not express a judgment or standing state.
- **Consumption receipt**: one `attests` row attached to the terminal source. Its
  `kind` is `verdict` and its `verdictKind` is
  `ruling-consumed:<fullDecisionRequestId>`. Absence of this exact row means
  **ruled-but-unconsumed** only for this contract. It does not mean that an
  authorization remains spendable.
- **Routed session**: the `sessionKey` on the one condition wake created by the
  successful late-ruling transaction for the full decision-request id.
- **Canonical commit target**: exactly one existing verified `commitRefs` member
  with the current commit-reference shape `{repo,commit}`. The repo includes the
  existing host-qualified absolute Git path. The commit resolves in that repo.
- **Operational-action target**: no `commitRefs` member and a nonblank attest note
  whose exact prefix is `operational-action: `.
- **Predecessor**: a terminal assignment explicitly named by the new
  `succeedsAssignmentId` input.
- **Successor**: the one assignment created by a successful `assign` or `dispatch`
  call that includes `succeedsAssignmentId`.
- **Successor marker**: one reserved substrate occurrence fact with exact kind
  `assignment-successor-created`, scope equal to the full successor assignment id,
  and origin `process:tightbeam`. It proves that the assignment handler wrote the
  successor's final paragraph.
- **Carry suffix**: this exact final paragraph in a successor's persisted subject,
  written after the handler appends exactly two line-feed bytes to the caller's
  subject. The `<predecessor>` and decision ids are full canonical ids:

  ```text
  Ruled-but-unconsumed decisions carried from <predecessor>: none
  Ruled-but-unconsumed decisions carried from <predecessor>: <decisionId>[, <decisionId>...]
  ```

  The handler writes the first form when the finite carry set is empty. It writes
  the second form when the set is nonempty.
- **Predecessor chain**: the finite ordered list that starts with the explicitly
  named predecessor. While the current assignment has a successor marker and a
  valid carry suffix, the assignment id after `carried from` is the next member.
  An unmarked assignment ends the chain.
- **Applicable decision**: an operator request that has a late-route marker, is
  still `ruled`, has no consumption receipt, and meets at least one of these finite
  conditions: its source is a predecessor-chain member; its source belongs to a
  work item named by a predecessor-chain member; or its full id appears in a valid
  carry suffix on a predecessor-chain member.
- **Activation**: the first process start on a product line whose product bytes
  implement this complete contract. Activation does not mutate an existing row.

## Assumptions

1. Assignment rows already store `holderKey`, `workItemId`, `openedBySession`,
   `openedByUser`, and terminal state. Work-item rows already store `ownerUserId`.
2. Session rows already store `state`, `ownerUserId`, and the edges used by the
   effective operational-parent lineage. `Org.personal_session_key/1` already
   derives an owner's personal Main session key.
3. Operator decision requests already store `assignmentId`, `ownerUserId`,
   `raiserSessionKey`, `status`, `ruledAt`, and `rulingFactId`.
4. The existing operator-ruling transaction already files
   `escalation-ruled`, schedules one ruling notification, and changes the request
   from `open` to `ruled` atomically.
5. Condition facts are append-only occurrence rows. Adding a reserved kind does not
   require a schema change.
6. Attests already provide the durable work trace and verified Git commit-reference
   shape. This contract reserves one verdict-kind prefix and one narrow terminal-
   assignment admission path; it does not add an attest field or table.
7. Assignment subjects already hold at most 2,000 Unicode code points. The CLI
   already sends `assign` and `dispatch` inputs to the same assignment creation
   seam used by their handlers. No supported mutation changes an assignment subject
   after creation.
8. `main` already publishes accepted assignment and attest mutations through its
   existing Firehose behavior. Product line `0.1.9` need not add a new publisher
   to satisfy this contract.
9. The common product-path inventory below exists at inspected `0.1.9` tip
   `81c91e2aad3790d631e298dc50a8cf9acb05a5e2` and inspected `main` tip
   `1c1110cabf93cb013cac772277493f5923389aa7`. These hashes prove the inventory
   inspection; they are not implementation targets.

Closure choice: ADD wins because deleting late owner rulings or successor
assignments would remove required coordination, while accepting the loss would
repeat the demonstrated `dr_07bdef13` failure. The addition reuses existing
assignment, session, condition-fact, wake, subject, and attest seams.

## Invariants

LR1. The operator-ruling transaction reads the request's assignment reference before
it chooses the notification recipient. A request with no source and a request with
an open source keep the existing recipient and do not file a late-route marker. A
terminal source uses LR2 through LR4. The source-state check, recipient selection,
notification scheduling, late-route marker, existing `escalation-ruled` fact, and
request transition commit together or have no effect. [AC1, AC2]

LR2. For a terminal source, the transaction builds this finite recipient sequence:

1. the source assignment's `openedBySession`, when present;
2. each next session in that opener session's effective operational-parent chain,
   nearest first;
3. `Org.personal_session_key` for the source assignment's `openedByUser`, when
   present;
4. `Org.personal_session_key` for the accountable owner.

The transaction removes a duplicate session key after its first occurrence. It
removes the source's `holderKey` and the request's `raiserSessionKey` before
selection. It visits a session key at most once and stops a cyclic parent chain
before the repeated key. It selects the first remaining candidate whose session row
is `active`. It does not inspect roles, assignment text, decision text, sibling
sessions, unrelated work items, or elapsed time. A user id contributes only its
matching personal Main candidate and does not start a global user-session search.
[AC1, AC6]

LR3. A terminal source with no active LR2 candidate makes `operator-rule` return the
exact refusal code `late_ruling_recipient_unavailable`. The transaction leaves the
request open and writes no wake, condition fact, lifecycle event, attest, assignment,
or Firehose handoff. [AC2]

LR4. A successful late ruling schedules exactly one ruling notification to the LR2
recipient and no ruling notification to the terminal request raiser. The existing
`escalation-ruled` fact releases that notification after commit. The same transaction
files exactly one late-route marker. The marker and notification contain the full
request id. An identical `operator-rule` replay returns the existing ruled request
and adds no wake, condition fact, lifecycle event, or projection handoff. [AC1, AC3]

LR5. Only a post-activation late ruling can file a late-route marker. Read, startup,
successor creation, receipt creation, and replay paths cannot synthesize the marker.
Existing ruled requests without the marker stay outside this contract. [AC3, AC6]

LR6. The routed session, the accountable owner's personal Main session, or the
accountable owner as an authenticated user may file the consumption receipt. A
caller with none of those relationships receives `not_found` for an unknown request,
an ineligible request, and a request outside its boundary. The receipt call must
name the full request id in the reserved verdict kind and the full terminal source
assignment id. The handler admits it only when the request is an operator request,
is `ruled`, names that source, has a late-route marker, and has no different existing
receipt. [AC4]

LR7. A consumption receipt names exactly one target form:

- A canonical commit target has exactly one verified `commitRefs` member and no
  attest note.
- An operational-action target has no `commitRefs` member and a note that starts
  with `operational-action: ` and contains at least one non-whitespace code point
  after the prefix.

A call with both forms, neither form, more than one commit reference, an unresolved
commit reference, a different note prefix, or a blank operational action returns
`invalid_ruling_consumption_target` and writes no row. [AC4]

LR8. The receipt handler reserves the exact verdict-kind grammar
`ruling-consumed:dr_<lowercase UUID>`. This form is the only exception to the
existing generic verdict-kind character grammar. It permits that form on the
matching terminal source without reopening or changing the source. Other verdicts
keep their existing verdict-kind, open-assignment, and review-link rules. One state
transaction rechecks LR6, the target form, and receipt absence, then inserts the
receipt. The existing commit-reference verifier resolves a new canonical-commit
target before that transaction; an exact replay may return the stored receipt
without resolving its commit again. The receipt changes no request status,
`consumedAt`, assignment state, condition fact, wake, or readiness state. [AC4, AC5]

LR9. A replay by an LR6-authorized principal with the same target form and byte-equal
target returns the existing receipt and writes nothing. A later call for the same
request with a different target returns `ruling_consumption_conflict` and preserves
the first receipt. The serialized state transaction inserts only when no attest has
that exact verdict kind. A concurrent pair can commit at most one receipt without a
new index, trigger, table, or migration. [AC5]

LR10. `assign` and `dispatch` accept one optional CLI input
`--succeeds <assignmentId>`. The wire body names it `succeedsAssignmentId`. The
handler, not the CLI, resolves the id, checks the caller's existing assignment-create
authorization, and requires the predecessor to be terminal. The predecessor is
visible only to its holder, its opener, the owner of its work item, or a session that
is the personal Main of that owner. An unknown, ambiguous, invisible, or unauthorized
predecessor returns `unknown_assignment`; an open predecessor returns
`predecessor_not_terminal`. Each refusal creates no assignment. A call without
`succeedsAssignmentId` keeps the existing assignment behavior and performs no carry
query. [AC6, AC8]

LR11. In the assignment-create transaction, a successful successor call builds the
predecessor chain under LR12 and computes the applicable decisions from that chain.
It rechecks each candidate against canonical request, late-route-marker, and
consumption-receipt rows. It removes duplicate ids and sorts the remaining full ids
by `ruledAt` ascending, then by id ascending. It appends one carry suffix, using
`none` for an empty set, and files one successor marker. The assignment row, suffix,
and marker commit together or have no effect. The persisted subject, returned
assignment, and existing assignment-created projection use the same final subject.
An existing assignment-idempotency hit returns its original assignment and adds no
suffix or successor marker. [AC6, AC7]

LR12. The handler visits a predecessor-chain assignment at most once. It reads that
assignment's final paragraph only when a successor marker names the assignment. The
paragraph must match the Terms grammar exactly, name an existing terminal
predecessor at the time the marked successor was created, and contain `none` or full
canonical decision ids. An unmarked assignment ends the chain, and text that only
resembles the suffix contributes no candidate. A linked predecessor may have
reopened after its successor was created. A missing linked assignment, marked
malformed suffix, or repeated assignment id returns `invalid_successor_chain` and
creates no assignment or side effect. A carried id does not qualify by text alone;
LR11 rechecks its rows. This bounded parse supports a linear successor chain across
work items without adding a successor column or inferring intent. [AC6]

LR13. If the caller-supplied subject, the paragraph separator, and the computed
suffix exceed the existing 2,000-code-point subject limit, the handler returns
`successor_brief_too_long` and creates no assignment, wake, fact, attest, lifecycle
event, or projection handoff. The caller can shorten the original subject and retry.
[AC7]

LR14. Product lines `0.1.9` and `main` implement LR1 through LR13 with the same
command names, wire key, marker kind, receipt kind and target forms, carry grammar,
selection order, refusal codes, ordering rule, limits, and forensic regression. A
line-specific transport or publisher difference cannot change those observable
results. [AC8]

## Architecture

The operator-ruling transaction remains the sole mutation seam for a request's
`open` to `ruled` transition. It asks one bounded recipient selector for the terminal
source's first active opener-or-owner candidate. The selector reads existing
assignment, work-item, and session rows. It does not decide who should own the work;
it follows explicit ownership edges. The transaction files the late-route marker
only after the selector succeeds, and the existing condition-wake path performs the
post-commit nudge.

The attest creation seam remains the sole mutation seam for a consumption receipt.
The reserved verdict-kind prefix makes the wrong row shape rejectable at one point.
The special admission permits one exact receipt on its terminal source. It does not
weaken ordinary terminal-assignment refusals. Receipt absence, not the request's
authorization-consumption status, supplies the finite carry query.

The assignment creation seam remains the sole mutation seam for a successor subject.
The explicit predecessor input declares the relationship that the substrate cannot
infer. The handler computes and appends the suffix before it validates the final
subject length and inserts the assignment. A later successor walks only the explicit
linear predecessor chain proven by successor markers and canonical final paragraphs.
It reads the assignments, their named work items, and their revalidated carried ids.
A visited-id set bounds corrupt cycles. The handler performs no sibling, global,
role, text-similarity, or semantic search.

The implementation changes this exact common product path inventory on both lines:

| Path | Required consequence |
|---|---|
| `lib/tightbeam/escalation.ex` | Detect a terminal source inside `operator-rule`, select LR2's recipient, schedule that recipient, and file the late marker atomically with the existing ruling effects. |
| `lib/tightbeam/condition_facts.ex` | Reserve `operator-ruling-late-routed` and `assignment-successor-created` for `process:tightbeam`. |
| `lib/tightbeam/assignments.ex` | Admit and validate the receipt; compute, validate, order, and append the successor carry suffix and file its marker inside assignment creation. |
| `cli/src/args.rs` | Parse `--succeeds <assignmentId>` for `assign` and `dispatch`, with local missing-value coverage. |
| `cli/src/dispatch.rs` | Send `succeedsAssignmentId` for both commands and cover exact body omission and inclusion. |
| `test/late_ruling_handoff_test.exs` | Hold the one cross-seam forensic regression in AC9 and focused refusal assertions required by AC1 through AC8. |

No schema, migration, router, gateway, lifecycle-event schema, Firehose registry,
REST serializer, work projection, job trace, or `0.1.8` path belongs in this inventory.
If implementation evidence shows that one listed behavior cannot be achieved through
these paths, the implementer must stop and request a scope ruling before adding a
path.

The test inventory is the new Elixir regression above, Rust unit tests beside the
changed CLI parsing and body mapping, and the pre-existing full Elixir and Rust suites
on each product line. Implementation verification must run outside Gibson with
`TIGHTBEAM_BASE_DIR` set to an isolated path. The implementation handoff must name the
host, commands, and baseline-versus-after counts for each line. This spec task does
not execute product code.

## Acceptance

AC1 — Terminal detection and nearest active recipient (LR1, LR2)

- Given a terminal source whose opener is active, an active ancestor also exists,
  and the accountable owner's personal Main is active, when the request owner rules
  its open operator request, then the ruling transaction schedules one ruling
  notification only to the opener and files one late-route marker.
- Given the same rows with a retired opener and active nearest ancestor, when the
  request owner rules the request, then the transaction schedules the notification
  only to that ancestor.
- Given a retired opener, a cyclic parent chain with no active member, and an active
  accountable-owner Main, when the request owner rules the request, then selection
  terminates and schedules the notification only to the accountable-owner Main.
- Given an open source, when the request owner rules its request, then the existing
  raiser notification remains and no late-route marker exists.
- Given a request with no source, when the request owner rules it, then the existing
  raiser notification remains and no late-route marker exists.
- Given no session opener, an `openedByUser` personal Main that is active, and an
  active accountable-owner Main, when the request owner rules the request, then the
  notification goes only to the opener user's Main.
- Given the active source holder or raiser appears in the opener's parent chain,
  when another active opener-or-owner candidate follows it, then selection skips the
  holder or raiser and notifies the next candidate.

AC2 — Atomic refusal (LR1, LR3)

- Given a terminal source with no active opener, parent, or owner-Main candidate,
  when the request owner rules its request, then the response code is
  `late_ruling_recipient_unavailable`; the request remains open; and counts for new
  wakes, facts, lifecycle events, attests, assignments, and Firehose handoffs are
  zero.

AC3 — Marker activation and replay (LR4, LR5)

- Given a successful late ruling, when the transaction commits and the scheduler
  consumes its `escalation-ruled` fact, then the selected recipient receives one
  notification that names the full request id and the source raiser receives none.
- Given the same answer is replayed, when `operator-rule` returns the ruled request,
  then wake, fact, lifecycle-event, and projection-handoff counts do not change.
- Given an existing ruled request without `operator-ruling-late-routed`, when the
  process starts, reads the request, creates an ordinary assignment, and creates a
  declared successor, then no path creates a marker or carries that request id.

AC4 — Receipt admission and target forms (LR6 through LR8)

- Given a marked ruled request and its terminal source, when the routed session files
  `ruling-consumed:<fullDecisionRequestId>` with one resolvable canonical commit
  reference and no note, then one terminal-source verdict exists with that exact
  commit reference and the source and request rows do not change.
- Given the same setup, when the accountable owner files the verdict with no commit
  references and note `operational-action: reloaded the affected session`, then one
  receipt exists with that exact note.
- Given each invalid target form in LR7, when an authorized principal files it, then
  the response is `invalid_ruling_consumption_target` and no attest exists.
- Given an unrelated session, when it files a receipt for the known request and when
  it files one for an unknown request, then both calls return the same opaque
  not-found response and disclose no request or assignment field.

AC5 — Receipt singularity (LR8, LR9)

- Given one committed receipt, when the same authorized principal repeats the
  byte-equal target, then it receives the original receipt id and the attest count
  stays one.
- Given one committed receipt, when an authorized principal submits the other target
  form or a different target, then the response is `ruling_consumption_conflict`,
  the original row remains byte-equal, and the attest count stays one.
- Given two authorized transactions race with different targets, when both finish,
  then one returns the committed receipt, the other returns
  `ruling_consumption_conflict`, and the database contains one matching verdict.

AC6 — Explicit successor and bounded carry (LR2, LR5, LR10 through LR12)

- Given a terminal predecessor with two marked, ruled, unconsumed requests in its
  work item; one duplicate id in its canonical carry suffix; one consumed request;
  one unmarked legacy ruling; and one unrelated-work-item request, when an authorized
  caller creates a successor with `--succeeds <predecessor>`, then its persisted
  subject has one carry suffix. The suffix contains the two qualifying full ids once,
  ordered by `ruledAt` and then id. It omits the consumed, unmarked, and unrelated
  ids.
- Given a terminal predecessor in a different work item whose canonical suffix
  carries one still-eligible request, when the caller creates its successor, then
  the new subject carries that id after row revalidation.
- Given successor B was created from terminal assignment A with an empty carry set,
  a late ruling for A commits afterward, and B then closes, when the caller creates
  successor C from B, then C's predecessor-chain query carries A's new ruled-but-
  unconsumed decision id.
- Given suffix-like caller prose on an assignment with no successor marker, when the
  handler creates a successor from it, then that prose contributes no carried id.
- Given a marked predecessor has a malformed final suffix, names a missing linked
  predecessor, or repeats an assignment id in its chain, when the caller creates a
  successor, then the response is `invalid_successor_chain` and all creation-side-
  effect counts stay zero.
- Given a historical linked predecessor reopened after its marked successor was
  created, when the immediate predecessor is terminal and the caller creates the
  next successor, then the chain remains valid and its applicable decisions are
  rechecked.
- Given an unknown, ambiguous, invisible, or unauthorized predecessor, when a caller
  supplies it, then no assignment is created and the response is
  `unknown_assignment`.
- Given an open visible predecessor, when an authorized caller supplies it, then no
  assignment is created and the response is `predecessor_not_terminal`.

AC7 — Subject identity and limit (LR11, LR13)

- Given a nonempty carry set within the subject limit, when successor creation
  commits, then the database row, command response, and existing assignment-created
  projection contain the same final subject bytes.
- Given the computed final subject has 2,001 Unicode code points, when successor
  creation runs, then the response is `successor_brief_too_long` and the counts for
  new assignments, wakes, facts, attests, lifecycle events, and projection handoffs
  are zero.
- Given an empty carry set, when successor creation commits, then the handler appends
  the exact `none` suffix and files one successor marker.
- Given a keyed successor call already created an assignment, when the caller
  repeats that key, then the handler returns the original assignment and adds no
  suffix or successor marker.

AC8 — CLI and dual-line equivalence (LR10, LR14)

- Given `assign` and `dispatch` without `--succeeds`, when each CLI builds its wire
  request, then `succeedsAssignmentId` is absent.
- Given either command with `--succeeds asg_full`, when the CLI builds its wire
  request, then `succeedsAssignmentId` equals `asg_full`. A missing option value
  fails locally and sends no request.
- Given the same LR1 through LR13 fixture corpus at the reviewed `0.1.9` and `main`
  implementation commits, when the external gate runs each corpus, then response
  codes, selected session keys, marker rows, receipt rows, carried subject bytes, and
  refusal side-effect counts are equal.

AC9 — The `dr_07bdef13` forensic regression (Goal, LR1 through LR14)

One test named `dr_07bdef13_survives_revocation_late_ruling_successor_and_consumption`
uses an isolated database and the literal id
`dr_07bdef13-45ae-435f-bc79-b2dc6b0a5ebf`. The test performs this sequence in one
case:

1. Create a source work item, a source assignment, its opener lineage, and an open
   operator request attached to the source assignment.
2. Revoke the source assignment before the request owner rules the request.
3. Retire the original raiser while leaving the nearest opener-or-owner candidate
   active.
4. Rule the request and assert one late-route marker, one notification to the nearest
   active candidate, and no notification to the retired raiser.
5. Create a replacement assignment in a different work item with
   `succeedsAssignmentId` equal to the revoked source. Assert that its persisted and
   returned subjects carry the full decision id and one successor marker names the
   replacement.
6. File a canonical-commit consumption receipt on the revoked source. Assert the
   verified commit reference, unchanged request status, unchanged source state, and
   one receipt.
7. Replay that receipt and assert the same receipt id and a count of one.
8. Close the replacement, then create a second successor from it. Assert that the
   second successor's subject does not carry the consumed decision id.

The same test file and assertions run on product line `0.1.9` and `main`. A
handwritten ideal fixture does not replace this state sequence.

## Open Questions

- BLOCKING: none.
- NON-BLOCKING: A later contract may replace the explicit carry suffix with a typed
  successor relation. This MVP keeps the relationship in a handler-written subject
  because the card forbids migration and the substrate must not infer intent.
- NON-BLOCKING: A later contract may add a dedicated receipt read projection if a
  product needs one. This MVP uses the existing assignment attests and work trace.
- DECLINED: automatic successor inference, historical marker backfill, decision-
  status consumption, a contradiction scanner, a global readiness gate, and any
  identity-guidance edit. These mechanisms are outside this work item.
