# Operator ruling provenance v1

Status: ruled core-cut candidate for independent review. This file carries no product-code,
implementation, merge-to-main, release, deploy, configuration, identity, service, or live-state
authority.

Authority: Mike's rulings recorded in `tightbeam-decisions.md` at commits
`13b8203d6aa36f557f5a1dc4bbdfefb6a6b30619` and
`d84633447205dc024976cc18d8b24cc8fd2ec25f`.

Canonical path: `operator-ruling-provenance-v1.md` in the `tightbeam-specs` repository. This
revision replaces the broader candidate at
`1c922bd7be67b2e08963ff65dfa8c088e94869cf`. The removed delegation, source-carrier, transport,
recommendation, pagination, and persistent-alert designs remain available in repository history.

## Goal

Make the submitting session a required, immutable fact on each new operator ruling.

An authorized reader must be able to distinguish a new ruling with a recorded submitting session
from an historical ruling whose submitting session is unknown. The system must not present an
historical owner-attributed ruling as direct user action.

The change must retain the existing operator-request lifecycle and authorization policy. A delegate
may rule when the existing policy authorizes that delegate. The ruling row names both the authority
user and the submitting session.

The product-owner ruling identifies 315 current Mike-attributed historical rulings whose submitting
provenance is unproven. Migration labels that historical population `unknown`; it does not infer a
direct-user path.

Subtraction ruling: reuse the existing `operator-rule` mutation and `ruledViaSessionKey` carrier.
Adding grants, a submission lifecycle, source bytes, or alert machinery would violate the ruled
scope. Deleting provenance would leave the authority inversion intact. Accepting another new ruling
without a submitting session would preserve the demonstrated defect.

## Non-Goals

1. This spec does not defend against a dishonest, malicious, or rogue agent.
2. This spec does not add delegation grants, scoped authorization, delegate limits, or a grant
   lifecycle.
3. This spec does not decide which delegates may rule. Existing authorization remains the authority
   for that decision.
4. This spec does not add recommendation and binding-submission kinds or a second decision
   lifecycle.
5. This spec does not store source messages, source bytes, source digests, transport classes, or
   caller-supplied provenance.
6. This spec does not infer direct-user action from an asserted owner name, an absent session, a
   terminal row, chronology, or message content.
7. This spec does not rewrite decision text, rationale, authority, or outcome on an historical row.
8. This spec does not add persistent-alert timing, alert episodes, pagination, polling, notification,
   delivery, or human-contact machinery.
9. This spec does not change the existing operator-request question, options, context, original raise
   date, supersession, resolution, or consumption rules.
10. This spec does not expose decision text, rationale, message content, attachments, session tokens,
    or credentials through provenance reads, events, logs, or audit rows.

Operating pattern taught to agents: delegates rule through their own authenticated session. They do
not present a ruling through an owner identity without a submitting session.

## Terms

- **Operator request**: the existing user-owned decision request with kind `operator`.
- **Operator ruling**: the existing atomic transition that moves an open operator request to
  `ruled`.
- **Authority user**: the user whose authority the existing authorization policy applies to the
  ruling. The existing row stores this identity as `ruledBy` in `user:<id>` form.
- **Submitting session**: the authenticated session that invoked `operator-rule`. The existing row
  stores its canonical key as `ruledViaSessionKey`.
- **Real submitting session**: a submitting-session key derived from the authenticated ingress and
  resolving to a retained Tightbeam session row. A caller parameter, projected owner identity, role
  name, display name, or org credential does not satisfy this term.
- **Provenance epoch**: the maximum existing operator-ruling fact id captured by the activation
  transaction. Rows at or below the epoch are historical. Rows above it are new.
- **Recorded provenance**: the read label for a new ruling whose `ruledViaSessionKey` resolves to its
  retained session row.
- **Unknown provenance**: the exact read label `unknown` for an historical ruling. It makes no claim
  about who submitted the ruling.
- **Record-only operator request**: an operator request whose substrate duty ends at a queryable
  user-addressed row. The row preserves its question, options, context, and original raise date. The
  substrate does not contact the user.

## Assumptions

1. `operator-rule` is the sole existing mutation that terminalizes an open operator request.
2. Operator ruling rows already retain `ruledBy`, `ruledViaSessionKey`, terminal state, ruling fact,
   and terminal time.
3. Session rows remain retained after a session retires, so an historical session key can continue to
   resolve.
4. The gateway can derive a session key from an authenticated session credential before it projects
   the authority user.
5. Existing operator-request authorization decides whether the authenticated caller may rule. This
   spec adds no authorization decision.
6. Existing decision-request REST resources and `decision_request.ruled` Firehose frames have
   exact-key consumers.
7. External-caller enforcement needs visitor identity from
   `wi_4ee303fa`. This dependency blocks activation on that ingress, not review or merge of this spec.
8. The product-owner card records 315 Mike-attributed historical rulings on 2026-08-31. That number
   is point-in-time context, not an activation count gate.
9. The frozen 2026-08-30 census at
   `operator-ruling-provenance-census-2026-08-30.md` records 294 Mike-attributed rulings: 291 without
   a retained session key, 3 with one, and 0 proven direct-user. Those counts are point-in-time
   evidence of the defect. They are not the current 315-row migration population.
10. The frozen diagnosis at `operator-ruling-provenance-diagnosis-2026-08-30.md` records the source
    path that dropped the submitting session before the terminal writer. Its former source-carrier,
    recommendation, and grant proposal is superseded by this ruled core cut.

## Invariants

P1. One successful post-epoch `operator-rule` transaction writes the authenticated submitting
session key to `ruledViaSessionKey` before it exposes the terminal state, ruling fact, or event.

P2. The gateway derives `ruledViaSessionKey` from authenticated ingress. It removes any caller field
that asserts or overrides that key.

P3. The handler resolves the derived key to a retained session row in the ruling transaction. A
missing or unresolved key returns `operator_ruling_submitting_session_required`. The refusal leaves
the request open and commits no ruling text, rationale, fact, notification, provenance event, or
terminal state.

P4. A request that asserts the authority user's name without a real submitting session receives the
P3 refusal. An org credential or external caller receives the same refusal unless ingress provides a
real session identity.

P5. The provenance check runs after existing authorization admits the caller and before terminal
mutation. It records who submitted. It does not grant authority or limit a delegate whom existing
authorization admits.

P6. The activation transaction records the maximum existing operator-ruling fact id as the
provenance epoch.

P7. The read projection labels each operator ruling at or below the epoch `unknown`, including a row
that retains an old session key. It omits a direct-user label from historical rows and preserves each
historical outcome and text.

P8. A database constraint rejects any operator ruling above the epoch when
`ruledViaSessionKey` is null or does not resolve to a retained session row. The application returns
P3's typed refusal before that constraint is reached.

P9. Existing decision-request REST bytes and existing `decision_request.ruled` Firehose bytes remain
unchanged.

P10. `GET /api/decision-requests/:id/operator-ruling-provenance` returns one read-only provenance
item with these fields:

| Field | Contract |
| --- | --- |
| `schemaVersion` | integer `1` |
| `requestId` | canonical operator-request id |
| `authorityPrincipal` | existing `ruledBy` value in `user:<id>` form |
| `state` | `recorded` for a post-epoch ruling or `unknown` for an historical ruling |
| `submittingSessionKey` | canonical retained key when `state=recorded`; null when `state=unknown` |
| `ruledAt` | existing terminal timestamp |

P11. The request owner and an existing Tightbeam admin may read the P10 route. This spec creates no new
permission or grant. Another caller receives the ordinary `404 not_found` body. A hidden id and an
absent id return that same body. Authorization runs before existence lookup.

P12. A successful new ruling emits one companion
`operator_ruling.provenance_recorded` Firehose event after commit. The event carries
`schemaVersion:1`, `op:"upsert"`, `requestId`, `authorityPrincipal`, `state:"recorded"`, and the
submitting session key. The serializer applies P11 authorization. Migration emits no provenance
event.

P13. Audit rows for an accepted ruling contain the request id, authority principal, authenticated
principal, submitting session key, and success cause. Refusal audit rows contain the request id,
asserted authority principal when present, authenticated principal, and refusal cause. Audit and logs
omit the private content named in Non-Goal 10.

P14. Restart exposes a committed ruling and its provenance once. It exposes no part of an
uncommitted ruling. Firehose replay may repeat the companion event; `requestId` identifies the one
immutable provenance projection over the terminal row.

P15. A record-only operator request remains queryable with its exact question, options, context, and
original raise date across supersession. Provenance recording schedules no user wake, external
transport, retry, delivery receipt, or other human-contact action.

P16. Writer activation is atomic across each enabled `operator-rule` ingress. Activation refuses as
`operator_ruling_external_identity_unavailable` while an enabled external-caller ingress cannot
produce a real submitting session. The spec and its read/migration design may merge before
`wi_4ee303fa` supplies visitor identity; the post-epoch writer may not activate partially.

## Architecture

The design keeps one mutation seam: existing `operator-rule`. Ingress supplies the authenticated
session key to that seam. The transaction uses the existing `ruledViaSessionKey` field and existing
terminal row; it creates no submission table.

Activation performs one read-only shape check, records the provenance epoch, installs the P8
constraint, verifies each enabled ingress, and enables the writer as one boundary. The versioned
REST detail route and companion Firehose event project the terminal row. They do not create another
state owner or paged collection.

This spec adds read surfaces because a required field that no authorized reader can inspect would
not meet the goal. Deleting the read surfaces would make provenance unverifiable. Accepting opaque
storage would move the same ambiguity from the write path to review.

Rollback after activation preserves the epoch and recorded session keys. An older or incompatible
writer returns `operator_ruling_provenance_writer_unavailable`; it does not write a terminal ruling
without a session. Unrelated request reads and mutations remain available.

## Acceptance

T1. Given an authorized delegate's authenticated session and an open Mike-owned operator request,
when the delegate calls `operator-rule`, then the same transaction stores `user:mike` as
`authorityPrincipal`, stores the delegate's retained session key, rules the request, and exposes
`state:"recorded"`.

T2. Given a call that asserts `user:mike` and has no real submitting session, when it calls
`operator-rule`, then it receives `operator_ruling_submitting_session_required`; the request remains
open and no terminal effect listed in P3 exists.

T3. Given the frozen 294-row fixture under
`fixtures/operator-ruling-provenance-migration-2026-08-30/rows.jsonl`, when migration classifies the
rows below the epoch, then each row projects `state:"unknown"`, no row projects direct-user, and the
fixture's recorded 291/3/0 evidence remains unchanged. The test does not treat 294 as the current
315-row population.

T4. Given the product-owner's 315-row inventory at the 2026-08-31 ruling boundary, when preflight
projects that inventory, then the result contains 315 `state:"unknown"` items, zero direct-user
items, and the original decision, rationale, authority, outcome, and timestamp on each source row.
The count does not gate activation.

T5. Given a non-negative integer N operator rulings commit after that inventory and before activation
records the epoch, when migration projects the pre-epoch population, then the result contains 315 + N
`state:"unknown"` items and zero direct-user items.

T6. Given the request owner, an existing admin, and an unrelated user, when each calls P10's exact
detail route, then the first two receive exactly P10's fields and the unrelated user receives the
ordinary `404 not_found` body. Given an absent request id, the unrelated user receives the same body.
Existing decision-request response fixtures remain byte-equal.

T7. Given a committed new ruling, when Firehose publishes and replays its events, then the authorized
consumer receives the unchanged `decision_request.ruled` frame plus P12's idempotent companion
event. An unauthorized consumer receives no companion event. Each event omits decision text,
rationale, message content, attachments, and credentials.

T8. Given one accepted ruling and one P3 refusal, when an admin reads their audit rows and service
logs, then the accepted row contains the request id, authority principal, authenticated principal,
submitting session key, and success cause; the refusal row contains the request id, asserted
authority principal, authenticated principal, and refusal cause. Neither record contains content
named in Non-Goal 10.

T9. Given process loss before the ruling transaction commits, when the service restarts, then the
request is open and no provenance or companion event exists. Given loss after commit, then one
terminal ruling with one recorded session is readable, and replay does not create another ruling.

T10. Given an enabled external-caller ingress without visitor identity, when activation runs before
`wi_4ee303fa` lands, then activation returns
`operator_ruling_external_identity_unavailable` and no post-epoch writer is enabled. The spec merge
itself remains valid.

T11. Given a record-only operator request that is superseded, when the owner reads the chain, then the
original question, options, context, and original raise date remain exact. Provenance work creates no
human-contact effect.

Trace: P1, P2, P5, and P8 map to T1. P3 and P4 map to T2. P6 and P7 map to T3, T4, and
T5. P9, P10, and P11 map to T6. P12 maps to T7. P13 maps to T8. P14 maps to T9. P15 maps
to T11. P16 maps to T10.

## Open Questions

None. The external visitor-identity dependency is owned by `wi_4ee303fa`; it does not reopen this
spec's ruled scope and does not block independent review or merge of the spec.
