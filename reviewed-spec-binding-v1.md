# Reviewed spec binding for existing work items — v1

- Status: PROPOSAL; target unset; pending one owner-opened independent exact-revision review
- Work item: `wi_2cf1ce04-9fc9-4ffe-81a9-856ff5b00613`
- Spec assignment: `asg_32f1d662-7f64-4e41-a5f2-4855d1eab286`
- Current-main evidence pins: Tightbeam `7a70a2f616363074514237b5bee48ba67c52e2ea`;
  tightbeam-specs `20d854ee66d18e051b12f6572ea5b251298e6784`
- Pattern name: **reviewed spec binding**

## Goal

G1. An owner or administrator can bind one independently reviewed canonical spec revision
to an existing open Tightbeam work item through a supported CLI command.

- Acceptance: Given an open item with no spec reference, a same-item spec artifact, and a
  completed linked independent review whose latest holder verdict is `reviewed-clean`, when
  the item owner runs `work-item-bind-spec`, then one transaction stores the exact name,
  SHA-256, evidence ids, principal, and time.

G2. Tightbeam makes the binding and its evidence readable after process restart.

- Acceptance: Given a successful binding, when the gateway restarts on the same database
  and an authenticated caller runs `work-item-get`, then the response returns the same spec
  reference and binding evidence.

G3. Tightbeam preserves the first reviewed binding as immutable history.

- Acceptance: Given a reviewed binding, when a caller repeats the exact binding, then the
  command returns the stored binding without another state change. When a caller supplies a
  different name, digest, or evidence id, then the command refuses before a write.

This feature must add a mechanism. Deleting the spec-reference surface would remove the
authority pin used by builders. Accepting the gap would leave an existing reviewed spec with
no agent-reachable binding path.

## Non-Goals

- This spec does not bind `wi_c6589a66-33e2-43f3-ab84-1b21a5b8c6cf` or any other live item.
- This spec does not select an implementation, integration, release, or deployment target.
- This spec does not edit, fetch, clone, merge, or interpret spec content.
- This spec does not decide whether prose is canonical or whether a review is intellectually
  sound. The authorized principal makes that judgment by selecting the evidence rows.
- This spec does not add spec versions, replacement history, unbind, clear, delete, rollback,
  compare-and-swap, request idempotency keys, merge, or repair commands.
- This spec does not bind a closed, failed, or iceboxed item. An exact replay of a binding
  made while the item was open remains legal after later disposition.
- This spec does not require a spec reference on each work item.
- This spec does not change `work-item-create` or remove the existing raw metadata update
  behavior for an item that has no reviewed binding row.
- This spec does not copy artifact paths, artifact descriptions, review notes, assignment
  subjects, or spec bytes into a binding response or event.
- This spec does not add guidance before the command ships. It teaches no new operating
  pattern beyond the existing spec-handoff rule to bind a reviewed hash before build work.
- This proposal does not authorize product implementation. Implementation requires a clean
  independent spec verdict and separate owner authority.

Decisions considered and declined:

- Restoring the generic metadata-update CLI is declined because it cannot prove which
  artifact and independent review caused the pin.
- Treating a wake, attest note, artifact description, or review subject as the binding is
  declined because prose does not set `specRefName` or `specRefSha256`.
- Parsing review prose for a file name or digest is declined because the substrate must
  verify rows, not perform a cognitive act.
- Fetching GitHub during binding is declined because an agent coordination mutation must
  not depend on network availability or repository credentials.
- Replacing the two existing spec-reference columns is declined because current readers
  consume them. The sidecar records provenance while the columns remain the compatible
  projection.

## Terms

- **Reviewed spec binding**: One immutable row that associates a work-item id with an exact
  spec-reference name and SHA-256 plus the evidence rows and principal that caused the
  association. It lives in `work_item_spec_bindings`.
- **Spec-reference pair**: The existing `work_items.specRefName` and
  `work_items.specRefSha256` values. The pair is both null or both non-null.
- **Spec artifact**: An `artifacts` row whose `kind` is `spec`, whose `workItemId` is the
  item being bound, and whose `contentSha256` equals the requested digest. It must be the
  producer holder's newest same-item spec artifact at the time the review assignment
  opened, ordered by `createdAt DESC, artifactId DESC`.
- **Producer assignment**: The assignment named by a review assignment's
  `reviewsAssignmentId`. Its holder must equal the spec artifact's `createdBySession`, and
  its resolved work item must be the item being bound.
- **Review assignment**: An assignment whose `effectKind` is `review`, whose
  `reviewsAssignmentId` names the producer assignment, and whose holder differs from the
  producer holder. It must be closed with outcome `completed`. Its `openedAt` freezes the
  structured spec-artifact snapshot.
- **Review attest**: The exact holder-filed `verdict` attest selected by the caller. It must
  belong to the review assignment and be that assignment's latest holder-filed verdict by
  `ts DESC, rowid DESC`. Its `verdictKind` must be `reviewed-clean`.
- **Review report**: A same-item `artifacts` row whose `kind` is `report` and whose
  `createdBySession` equals the review assignment holder. It must be the holder's newest
  same-item report from the review interval, ordered by `createdAt DESC, artifactId DESC`,
  where the interval starts at the review assignment's `openedAt` and ends at the selected
  review attest's `ts`, inclusive.
- **Provenance bundle**: The spec artifact, producer assignment, review assignment, review
  attest, and review report joined by the rules above. The authorized principal selects the
  three public evidence ids. Tightbeam derives both assignment ids and verifies the joins.
- **Exact evidence id**: The complete stored `artifactId` or attest `id`. Evidence fields
  use exact primary-key lookup and do not expand prefixes. The work-item argument retains
  its existing exact-or-unambiguous-prefix behavior.
- **Row-verified**: Tightbeam checks the stored row values and relationships. It does not
  claim that the artifact digest was computed by Tightbeam or that review prose is correct.
- **Bind**: Insert a binding row and set a null spec-reference pair to the exact requested
  pair in the same transaction.
- **Adopt**: Insert a binding row for an already equal non-null spec-reference pair without
  changing the pair. Adoption is legal only on an open item and only with a verified
  provenance bundle.
- **Exact replay**: A request whose name, digest, spec artifact id, review attest id, and
  review report id equal the stored binding values.
- **Immutable conflict**: A request against a bound item that differs in any stored binding
  field, or a first request against an item whose existing spec-reference pair differs from
  the requested pair.
- **Target**: A top-level `sessionKey`, `role`, `userId`, or retired `target` routing field.
  This command acts on a work-item parameter and has no target.

## Assumptions

A1. Current Tightbeam main stores the spec-reference pair on `work_items`, returns it from
`work-item-get`, and enforces the both-null-or-both-non-null database check.

A2. Current main routes the raw `work-item-update` verb through the gateway and domain but
does not expose a Rust CLI update or binding command.

A3. Current main stores artifact kind, content SHA-256, creator session, work-item id, and
creation time. The artifact SHA-256 is a durable recorded claim. Binding verifies that
claim against the requested digest; it does not recompute artifact bytes.

A4. Current main stores review-of linkage, assignment effect kind, holder identity, attest
author, verdict kind, and deterministic attest ordering.

A5. SQLite serializes Tightbeam write transactions on one database.

A6. The existing router resolves the authenticated principal before a domain handler runs.
A session principal can be mapped to its owner user and that user's administrator bit.

A7. Existing work-item detail and trace readers already expose assignment and attest ids to
authenticated org participants. The new binding readback does not create a spec-content or
credential disclosure surface.

A8. The concrete blocker satisfies the intended evidence shape: spec artifact
`art_53d5c390` carries SHA-256
`cc856914d0c80eb4c8dc1f807692ad7b7c533f2f9ca666b9a629f76121b77bce`; review attest
`att_d50c9363-07b0-4af2-b14f-16e60c83e8ac` is `reviewed-clean`; review report
`art_150d769e` exists; and the work item's spec-reference pair is null. Read-only evidence
shows the selected spec artifact at `1787686549751`, review opening at `1787686598255`,
report at `1787686820059`, and verdict at `1787686840092`. This is evidence only. This
proposal performs no bind.

A9. The execution-time source SHAs in the header are evidence pins, not permanent build
baselines. A later implementation starts from the then-current green authorized line and
reconciles this contract before editing.

## Invariants

### Authority and target

R1. Only the work-item owner or an administrator may create a reviewed spec binding.

- Acceptance: Given an open item owned by `mike`, when `mike`, a session owned by `mike`,
  an administrator, and an administrator-owned session each bind valid evidence, then each
  succeeds in its own fixture. When another user or that user's session supplies the item
  id, then the command returns `not_found` and writes no row.

R2. A process principal cannot bind a spec, and a missing principal cannot bind a spec.

- Acceptance: Given valid evidence, when a process principal calls the verb, then it
  returns `process_denied`. When no principal reaches the handler, then it returns
  `principal_required`. Neither call reads evidence rows or changes the item.

R3. `work-item-bind-spec` accepts no target.

- Acceptance: Given any top-level target field, including null or an unknown id, when the
  request reaches the router, then it returns `invalid_message` with
  `work-item-bind-spec takes no typed target` before target lookup or domain dispatch.

### Input and provenance

R4. The command requires one work-item id, one non-blank spec-reference name of at most
2,000 characters, one 64-character lowercase hexadecimal SHA-256, one exact spec artifact
id, one exact review attest id, and one exact review report artifact id.

- Acceptance: Given a missing value, a blank name, an uppercase, short, or non-hex digest,
  a repeated flag, or an extra positional value, when the CLI parses the command, then it
  returns the exact usage text and sends no request. Given an equivalent malformed raw
  request, the domain returns `invalid_spec_binding` before a database write. Given a
  non-blank evidence-id prefix on a first request with no binding row, the domain performs
  exact primary-key lookup and returns `spec_provenance_unverified`; it does not expand the
  prefix or list candidates. On an already-bound item, the same different string follows
  R16 and returns `spec_binding_conflict` before evidence lookup.

R5. The requested name must identify the spec artifact's path.

- Acceptance: Given a spec artifact whose `originPath` or non-null `home` equals the name,
  ends with `/` plus the name, or ends with `:` plus the name, when the other evidence is
  valid, then name verification passes. Given no such exact boundary match, then binding
  returns `spec_provenance_unverified` and changes no row.

R6. The spec artifact must carry the requested digest and the same work-item id.

- Acceptance: Given a missing artifact, a non-`spec` artifact, a null or different
  `contentSha256`, or an artifact attached to another item, when the owner requests a bind,
  then binding returns `spec_provenance_unverified` and changes no row. Given an artifact
  recorded after the review opened, or an older producer spec superseded before review
  opening by another same-item producer spec, then the same refusal occurs.

R7. The review attest must prove the latest holder judgment on an independent linked
review assignment.

- Acceptance: Given a holder-filed latest `reviewed-clean` attest on a review-effect
  assignment linked to the producer, with different producer and reviewer holders and
  assignment outcome `completed`, when the owner binds, then review verification passes.
  Given a missing attest, a non-verdict, a verdict filed by someone other than the review
  holder, a latest holder verdict other than `reviewed-clean`, no review-of link, a
  non-review effect, an open, surrendered, or revoked review assignment, or equal producer
  and reviewer holders, then binding returns `spec_provenance_unverified` and changes no
  row.

R8. The spec artifact creator and review report creator must match the verified producer
and reviewer holders.

- Acceptance: Given a spec artifact created by the producer holder and the review holder's
  newest same-item report in the inclusive review interval, when the owner binds, then
  provenance verification passes. Given either creator differs, either artifact belongs
  to another item, the report is not kind `report`, the report falls outside the interval,
  or a newer eligible report exists, then binding returns
  `spec_provenance_unverified` and changes no row.

R9. A provenance refusal reveals no stored row from another work item.

- Acceptance: Given an evidence id that is missing or belongs to another item, when an
  authorized owner calls the verb, then the response contains only code
  `spec_provenance_unverified`, the caller-supplied field name, and a remedy to supply
  same-item evidence. It contains no foreign item id, principal, path, title, description,
  note, subject, digest, or candidate list.

### State, atomicity, and immutability

R10. A first bind or adoption is legal only while the item state is `open`.

- Acceptance: Given an unbound item in each state `iceboxed`, `closed`, and `failed`, when
  its owner supplies valid evidence, then each call returns `work_item_not_open` and writes
  no binding or spec-reference value.

R11. Missing and caller-invisible work items have the same result.

- Acceptance: Given a nonexistent id and an id owned by another non-admin user, when the
  caller invokes the command, then both calls return HTTP 404 `not_found` with
  `work item not found`, before evidence lookup. An exact-id lookup must perform the same
  owner-or-admin check as a prefix lookup.

R12. Binding or adoption commits the spec-reference pair, provenance, principal, time, and
audit handoff in one transaction.

- Acceptance: Given an injected failure after any write or before the audit handoff, when
  the transaction exits, then neither the sidecar row nor a new spec-reference value is
  visible and no binding state event is published.

R13. A null pair becomes the requested pair. An equal legacy pair is adopted. A different
legacy pair is an immutable conflict.

- Acceptance: Given three open unbound fixtures with a null pair, the requested pair, and a
  different pair, when the owner binds valid evidence, then the first sets the pair and
  inserts provenance, the second preserves the pair and inserts provenance, and the third
  returns `spec_binding_conflict` without a write.

R14. A reviewed binding has no update or delete seam.

- Acceptance: Given a binding row, when a raw metadata update supplies a different or null
  spec-reference field, then it returns `spec_binding_conflict` and preserves both tables.
  When it supplies values that produce the stored pair, then the metadata update is a
  spec-reference no-op. Title, `isBug`, and a separately authorized body field retain their
  existing behavior.

R15. Exact replay returns the original binding in any later work-item state and creates no
second binding state effect.

- Acceptance: Given a binding made while open and later item state `closed`, when the owner
  repeats the five binding identity fields, then the command returns `changed: false`, the
  original principal and timestamp, and no new metadata doorbell or
  `work_item.spec_bound` event. The ordinary accepted-verb audit still records the call.
  A later artifact-state change or verdict on a separate review assignment does not rewrite
  or invalidate the recorded bind-time decision.

R16. A different request against a reviewed binding is an immutable conflict.

- Acceptance: Given one stored binding, when a caller changes the name, digest, spec
  artifact id, review attest id, or review report id one at a time, then each call returns
  `spec_binding_conflict` and preserves the original row and spec-reference pair.

R17. Concurrent binding has one deterministic durable winner.

- Acceptance: Given two calls released concurrently against one unbound open item, when
  their five binding identity fields are equal, then one creates the binding and the other
  returns its exact replay; one state event exists. When any identity field differs, then
  one creates the binding and the other returns `spec_binding_conflict`; the stored pair
  and evidence each come from the winner. Given a concurrent raw metadata update, SQLite
  serialization produces one of two complete orders: a different pair committed first
  makes the bind conflict, while a bind committed first makes the different update
  conflict. An equal metadata result preserves the binding in either order. Given review
  completion concurrent with a first bind, a bind serialized before completion refuses the
  open review and a bind serialized after completion evaluates the closed review. A spec
  artifact created after review opening or a report created after the selected verdict is
  outside the frozen snapshot regardless of commit order. Later evidence cannot alter a
  successful bind.

### Readback, audit, durability, and compatibility

R18. `work-item-get` returns a nullable top-level `specBinding` sibling of `workItem` and
`assignments`.

- Acceptance: Given a legacy item with no sidecar row, when a caller gets it, then
  `specBinding` is null and no backfill occurs. Given a reviewed binding, then readback
  returns the exact stored name, digest, three evidence ids, two derived assignment ids,
  bound principal, and bind time.

R19. A successful first bind or adoption emits one metadata doorbell, one committed
`work_item.spec_bound` state event, and the existing accepted-verb audit.

- Acceptance: Given one successful first bind, when event rows and the live firehose are
  inspected, then the doorbell names only the item and `metadata`; the state event uses the
  work-item projection and `workItemId` primary reference; and the accepted audit result
  carries the binding descriptor. The binding row and accepted audit name the selected
  evidence cause. The binding row, state event refs, and accepted audit name the
  authenticated principal. The existing metadata doorbell retains its
  item-plus-`metadata` shape.

R20. Binding responses and events contain no spec or report content.

- Acceptance: Given unique sentinels in the artifact path, artifact description, review
  note, assignment subject, spec bytes, and report bytes, when bind succeeds, replays, and
  refuses, then no sentinel outside the caller-supplied name, digest, or public ids appears
  in the binding response, error, event, or audit payload. The response may contain the
  requested name, digest, public ids, principal, time, and `changed` flag.

R21. The binding survives gateway restart and replay without reconstruction.

- Acceptance: Given a file-backed database with one binding, when the gateway restarts,
  then `work-item-get` returns the same sidecar values. An exact replay after restart
  returns `changed: false` and does not change the stored timestamp.

R22. Existing work-item behavior stays compatible outside the reviewed binding boundary.

- Acceptance: Given baseline fixtures for create, get, trace, list, disposition,
  assignment, and raw metadata update on an item without a binding row, when the feature is
  present, then their pre-feature fields, errors, state transitions, and request bytes are
  unchanged except that `work-item-get` adds nullable `specBinding`. Existing items require
  no backfill. Existing non-null spec-reference pairs remain readable and can be adopted
  only through this command while open.

R23. The Rust CLI adds only the dedicated binding operation for changing spec references
on an existing work item.

- Acceptance: Given the command help and unknown-command roster, when a caller reads them,
  then they list `work-item-bind-spec` and do not expose the legacy title, `isBug`, clear,
  or generic spec-reference patch flags.

## Architecture

### 1. Command and wire shape

Add this command:

```text
tightbeam work-item-bind-spec <workItemId> \
  --spec-ref <name> \
  --spec-sha256 <64-lowercase-hex> \
  --spec-artifact <artifactId> \
  --review-attest <attestId> \
  --review-report <artifactId>
```

The command accepts the existing optional, at-most-one identity selectors. It accepts no
target selector or generic metadata flag. Its exact one-line usage text is:

```text
usage: tightbeam work-item-bind-spec <workItemId> --spec-ref <name> --spec-sha256 <64-lowercase-hex> --spec-artifact <artifactId> --review-attest <attestId> --review-report <artifactId>
```

The CLI sends this parameter map through the existing `/agent/dispatch` route:

```json
{
  "verb": "work-item-bind-spec",
  "params": {
    "workItemId": "wi_…",
    "specRefName": "feature-v1.md",
    "specRefSha256": "<64 lowercase hex>",
    "specArtifactId": "art_…",
    "reviewAttestId": "att_…",
    "reviewReportArtifactId": "art_…"
  }
}
```

Add `work-item-bind-spec` to the closed router and gateway verb sets and to the router's
non-target set. The router atomizes the six parameter names through its existing spelling
rule. No new HTTP route exists.

### 2. Durable representation

Add one sidecar after the work-item, assignment, attest, and artifact schemas exist:

```sql
CREATE TABLE work_item_spec_bindings (
  workItemId             TEXT PRIMARY KEY REFERENCES work_items(id),
  specRefName            TEXT NOT NULL
                         CHECK(length(trim(specRefName)) BETWEEN 1 AND 2000),
  specRefSha256          TEXT NOT NULL
                         CHECK(length(specRefSha256) = 64 AND
                               specRefSha256 NOT GLOB '*[^0-9a-f]*'),
  specArtifactId         TEXT NOT NULL REFERENCES artifacts(artifactId),
  producerAssignmentId   TEXT NOT NULL REFERENCES assignments(id),
  reviewAssignmentId     TEXT NOT NULL REFERENCES assignments(id),
  reviewAttestId         TEXT NOT NULL REFERENCES attests(id),
  reviewReportArtifactId TEXT NOT NULL REFERENCES artifacts(artifactId),
  boundByUser            TEXT NULL REFERENCES users(userId),
  boundBySession         TEXT NULL REFERENCES sessions(sessionKey),
  boundAt                 INTEGER NOT NULL CHECK(boundAt >= 0),
  CHECK((boundByUser IS NOT NULL) != (boundBySession IS NOT NULL))
);
```

The table has one writer: `work-item-bind-spec`. No update or delete statement targets it.
The binding transaction keeps its name and digest equal to the work-item projection.
Schema activation creates and validates the exact sidecar shape without changing the
existing schema stamp or backfilling a row. A partial or incompatible object causes the
named boot refusal `incompatible_work_item_spec_binding_v1`; bootstrap does not infer or
repair its shape.

### 3. Domain transaction

The handler applies this order inside one serialized transaction:

1. Validate the resolved principal class. Refuse a process or missing principal before
   validating parameters or reading the item or evidence.
2. Validate the input shape. Treat the three evidence ids as exact strings without prefix
   expansion.
3. Resolve the work item through an owner-or-admin visibility predicate, then explicitly
   recheck owner-or-admin authority on the resolved row. Apply the recheck to exact ids and
   prefixes. Return the same `not_found` for missing and invisible items.
4. Read a binding row. If one exists, return an exact replay or
   `spec_binding_conflict`; do not evaluate current item state or replacement evidence.
5. Require `state = 'open'`.
6. Require the existing spec-reference pair to be null or equal to the requested pair.
7. Resolve and verify the provenance bundle with exact evidence-id and same-item predicates
   in each query. Use the review opening time to select the newest eligible producer spec
   artifact, require the review assignment to be closed with outcome `completed`, and use
   the selected verdict time to select the newest eligible reviewer report. Reject a
   caller-selected artifact or report that is not that deterministic snapshot row.
8. Set a null pair to the requested pair; leave an equal pair byte-identical.
9. Insert the sidecar row with the derived assignment ids and authenticated principal.
10. Append the accepted-verb audit row and queue its `verb.accepted` plus
   `work_item.spec_bound` firehose handoffs on the transaction. A replay appends its
   accepted audit row but suppresses the state handoff because `changed` is false.
11. After commit, invoke the existing work-item metadata-doorbell callback once. Callback
    failure does not roll back or retry the committed binding.

The exact-replay comparison includes the name, digest, and three caller-selected evidence
ids. The derived assignment ids, principal, and time come from the stored first bind and
are derived by Tightbeam. Replay does not re-verify evidence rows: it reports the immutable
bind-time decision and cannot turn a later artifact-state change or a separate review into
history rewrite.

The existing metadata update handler consults the sidecar only when a request supplies a
spec-reference field. No row means baseline behavior. A row means an equal resulting pair
is a no-op and any different resulting pair returns `spec_binding_conflict`.

### 4. Read and event shapes

`work-item-bind-spec` returns:

```json
{
  "changed": true,
  "workItem": { "id": "wi_…", "specRefName": "feature-v1.md",
                "specRefSha256": "<sha>", "…": "existing fields" },
  "specBinding": {
    "specRefName": "feature-v1.md",
    "specRefSha256": "<sha>",
    "specArtifactId": "art_…",
    "producerAssignmentId": "asg_…",
    "reviewAssignmentId": "asg_…",
    "reviewAttestId": "att_…",
    "reviewReportArtifactId": "art_…",
    "boundByUser": "mike",
    "boundBySession": null,
    "boundAt": 0
  }
}
```

An exact replay returns the same shape with `changed: false`. `work-item-get` adds the same
nullable `specBinding` object at the top level. Other work-item projections retain their
current shapes.

Register `work_item.spec_bound` as a work-item upsert class with primary reference
`workItemId`. Add `work-item-bind-spec` to the transactional verb set and its canonical
work-item lookup set. The state event carries the existing sanitized work-item resource;
its refs carry the call origin and principal. The durable accepted-verb audit row carries
the binding descriptor above. Its `verb.accepted` firehose observation retains the standard
sanitized verb metadata shape. Denials use the existing denied-event path with a sanitized
error descriptor.

### 5. Error contract

| Condition | Result | HTTP |
| --- | --- | --- |
| CLI grammar failure | exact usage; no request | — |
| Invalid raw name, digest, id type, or missing field | `invalid_spec_binding` | 400 |
| Process principal | `process_denied` | 403 |
| Missing principal | `principal_required` | 403 |
| Missing or caller-invisible work item | `not_found` | 404 |
| First bind or adoption on non-open item | `work_item_not_open` | 400 |
| Existing different pair or binding | `spec_binding_conflict` | 409 |
| Missing, foreign, mismatched, stale, non-clean, or non-independent provenance | `spec_provenance_unverified` | 400 |
| Unexpected exception | existing `server_error` envelope | 500 |

`spec_binding_conflict` names the remedy: read the existing binding and open a separate
owner decision if a new governing spec is required. This MVP supplies no rewrite verb.
`spec_provenance_unverified` names only the caller-supplied field that failed and tells the
caller to supply same-item structured evidence.

### 6. Traceability and deterministic verification

| Contract | Implementation surface | Verification surface |
| --- | --- | --- |
| R1-R2, R4-R17, R21-R22 | new binding domain module plus bounded work-item metadata guard | domain and schema tests |
| R3-R4, R23 | router and Rust CLI parser/request builder/help | router, Rust unit, and CLI integration tests |
| R18 | work-item detail query | domain, route, and CLI integration tests |
| R19-R20 | gateway callback and firehose registry/publisher | event-log, firehose, and redaction tests |
| R12, R15-R17 | one transaction and replay branch | injected-failure and barrier-controlled concurrency tests |
| R21 | file-backed gateway and built release CLI | executable restart/replay smoke |

The executable smoke uses a fresh file-backed gateway and the built release CLI. Through
supported verbs it creates an owner, producer, reviewer, one open work item, one producer
assignment, one spec artifact, and one linked review assignment. The reviewer records one
report artifact, files one holder `reviewed-clean` verdict, and closes the review assignment
with outcome `completed`, in that order. The owner binds, reads the result, restarts the
gateway on the same database, reads again, repeats the exact command, and attempts one
conflicting command. The smoke asserts one binding row, one state event, stable principal
and timestamp, no sentinel leakage, and cleanup of the fresh run directory.

The concurrency test releases two calls at one barrier and exercises both equal and
different five-field identities, then releases a binder and raw metadata update at one
barrier. It asserts one serialized outcome and complete winner provenance with no mixed
row. Each relevant test uses concrete rows; no test infers review identity from prose.
Provenance tests insert a later producer spec before review opening, a producer spec after
review opening, reports before and after the review interval, and two eligible reports with
the same millisecond. They prove the stated ordering and boundary inclusivity. Barrier
tests place review completion on each side of the binding transaction and prove that rows
created outside the frozen artifact or report interval remain ineligible.

### 7. Principle and compatibility boundary

The owner decides which canonical artifact and independent review justify the binding.
The substrate verifies the selected rows and makes their association durable (wisdom 6).
The binding row carries cause and principal (wisdom 5). The transaction makes a partial or
rewritten reviewed binding unrepresentable (wisdom 26). It adds no hold: each refusal ends
the command and names an agent-reachable next action.

This spec supersedes only `work-item-v1.md`'s unrestricted spec-reference mutation for an
item that has a `work_item_spec_bindings` row. It preserves that spec's current-governing
pair, existing create behavior, and raw unbound metadata behavior. It preserves
`specs/tightbeam/editable-work-item-body.md`'s body separation: body-only updates do not
read or change this sidecar.

## Acceptance

AC1 — Concrete evidence fixture:

- Given a fixture with the exact relational shape of `art_53d5c390`,
  `att_d50c9363-07b0-4af2-b14f-16e60c83e8ac`, and `art_150d769e`, plus null spec-reference
  fields on an open owned item and a completed linked review assignment,
- When the owner invokes `work-item-bind-spec` with
  `codex-session-usage-capture-v1.md` and
  `cc856914d0c80eb4c8dc1f807692ad7b7c533f2f9ca666b9a629f76121b77bce`,
- Then the fixture binds once with complete provenance and no content parsing.
- This is a test fixture only. The implementation and this proposal do not invoke the
  command against the live concrete item.

AC2 — Authorization and privacy:

- Given owner, administrator, foreign-user, process, missing-principal, missing-item, and
  foreign-item cases,
- When each caller invokes the verb,
- Then only owner and administrator cases can bind; foreign and missing items are
  indistinguishable; process and missing principal retain typed refusals; and no refusal
  leaks another item's rows.

AC3 — Validation and provenance:

- Given each malformed input and each broken provenance edge from R4-R9,
- When the CLI or domain receives it,
- Then the specified typed refusal occurs before any binding or spec-reference write.

AC4 — Lifecycle and adoption:

- Given null, equal, and different pairs across open, iceboxed, closed, and failed items,
- When valid binding requests run,
- Then only open null and open equal cases create provenance; a null pair is set, an equal
  pair is adopted, a different pair conflicts, and non-open first requests refuse.

AC5 — Replay, conflict, and concurrency:

- Given one completed bind,
- When exact replay runs before and after item disposition and gateway restart,
- Then it returns the original binding with `changed: false` and no second state effect.
- When a different identity competes serially or concurrently, then it returns
  `spec_binding_conflict`; equal concurrent input converges on one row.

AC6 — Atomicity and no history rewrite:

- Given injected failures at each transaction seam and raw attempts to clear or replace a
  reviewed pair,
- When the calls finish,
- Then no partial binding exists and no committed reviewed binding changes.

AC7 — Readback, audit, and redaction:

- Given a successful bind with unique content and prose sentinels,
- When get, event, audit, replay, and denial paths run,
- Then get returns the exact descriptor after restart; the event counts and causes match
  R19; and no non-request sentinel appears outside the original artifact and report bytes.

AC8 — Compatibility:

- Given the pre-feature CLI and domain fixtures plus legacy items with null and non-null
  spec-reference pairs,
- When the full Mix and Rust gates run before and after the change,
- Then baseline behavior remains green under R22, the new command is the only added CLI
  spec-reference mutation surface for an existing item, and a clean file-backed built-CLI
  smoke passes.

## Open Questions

- None. A review finding that changes authority, provenance structure, mutability, privacy,
  or lifecycle policy requires an amendment to this canonical file before implementation.
