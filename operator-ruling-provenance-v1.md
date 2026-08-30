# Operator ruling provenance and persistent-alert escalation v1

Status: targetless candidate for independent review. This file carries no implementation,
binding, merge, release, deploy, credential, configuration, identity, service, or live-state
authority.

Authority: work item \`wi_a8de6fe5-5450-41c8-ac9b-f623d349d0cc\` and assignment
\`asg_4433bbf4-5f74-46b6-9c7e-f2c49a1c26cf\`. Evidence is frozen in
\`operator-ruling-provenance-census-2026-08-30.md\` and
\`operator-ruling-provenance-diagnosis-2026-08-30.md\`.

This proposal supersedes the parked design discussion in
\`user-alerted-decision-request-escalation.md\`. It extends the current operator-request
terminal contract. It does not change statute, effort, or agent-question rulings.

## Spirit

Mike's words remain distinguishable from an agent's representation of them. Direct Mike
evidence is stronger than an intermediary recommendation. Agents can still move work forward:
they file recommendations in their own identity, and Mike can confirm one without the agent
impersonating him.

The substrate records who, how, and from what exact evidence. It does not decide whether words
mean consent. Org policy decides which authenticated actors may bind Mike's authority.

## Goal

Deliver one buildable provenance seam for operator decision requests and use that seam for
persistent fault-alert decisions.

The result must let an authorized reader answer these questions without reading private text:

1. Which user authority owns the binding decision?
2. Which actor and session submitted each candidate answer?
3. Which authenticated transport admitted the submission?
4. Which exact stored bytes support a binding decision?
5. Was the submission a recommendation or a binding confirmation?
6. Is historical attribution known, session-mediated, or legacy-unknown?

The persistent-alert policy must file one decision request only when an observable alert
episode remains standing for 15 minutes.

Subtraction ruling: DELETE wins for session use of \`--as-user <owner>\` as a binding ruling
surface under the recommended policy. ADD wins for one immutable submission carrier because
deleting operator decisions would remove required human rulings, while accepting the current
collapsed row preserves the provenance defect. ADD wins for one policy rule over existing
alert facts because deleting terminal alerts removes required fault reporting and accepting
the gap leaves persistent alerts undiscoverable.

## Non-Goals

1. This spec does not infer a user's intent from prose, a model response, timing, a session
   name, or an absent field.
2. This spec does not rewrite or relabel historical ruling text.
3. This spec does not classify a legacy row with no submitting session as direct-user.
4. This spec does not expose decision, rationale, message, attachment, or source text in logs,
   census artifacts, Firehose refs, or list views.
5. This spec does not add a second decision lifecycle, alert latch, fault bubble, recovery
   sweep, queue, worker, or owner inbox.
6. This spec does not change fault bubbling, user-alerted retraction, harness quarantine, or
   turn delivery.
7. This spec does not change existing REST response bytes or existing Firehose event bytes.
8. This spec does not select a product branch, release, deployment, or backport target.
9. Operating pattern taught to agents: cite a recommendation row; do not speak as the user.

## Terms

- **Authority principal**: the user principal whose authority makes a decision binding.
- **Submitting actor**: the authenticated principal that invokes the submission mutation.
- **Submitting session**: the session credential observed at ingress. Its state is \`known\`,
  \`none\`, or \`legacy-unknown\`.
- **Transport class**: the closed ingress class \`user-device\`, \`session-cli\`, \`org-cli\`,
  or \`legacy-unknown\`. The ingress writes it. A caller cannot supply it.
- **Exact-source evidence**: an immutable carrier reference plus SHA-256 of the bytes that the
  authenticated actor submitted. An existing owner-visible message can be the carrier.
- **Ruling submission**: one immutable candidate answer for one operator request. Its kind is
  \`recommendation\` or \`binding-confirmation\`.
- **Recommendation**: a session-authenticated submission in that session's principal. It
  leaves the request open.
- **Binding confirmation**: an authorized submission that atomically moves an open operator
  request to ruled and becomes that request's binding submission.
- **Direct-user**: a binding confirmation admitted through authenticated user-device
  transport. An asserted \`asUser\` field or an absent session does not establish this class.
- **Session-mediated**: a submission with a substrate-observed submitting session.
- **Legacy-unknown**: a historical field whose value cannot be proved from retained rows.
- **Alert episode**: one assertion fact of kind \`user-alerted\`, \`harness-auth-dead\`, or
  \`harness-rate-limit-dead\`, ending at its matching retraction fact.
- **Persistent alert**: an alert episode that remains standing at assertion time plus 900,000
  milliseconds.

## Assumptions

1. Operator decision requests already have one owner, one open-to-ruled compare-and-swap, one
   ruling fact, one raiser notification, and owner-scoped read authorization.
2. Messages retain an id, session, sender, device id when present, exact content, and
   timestamp.
3. The gateway can distinguish a session credential, a user device credential, and the
   org-wide CLI credential at ingress.
4. Firehose authenticates with gateway credentials and filters by the caller's current read
   authorization.
5. The existing \`user-alerted\` fact clears on the first delivered turn owned by that user.
6. Harness authentication and rate-limit quarantine produce durable standing facts.
7. Existing public decision-request and Firehose payloads have exact-key consumers.
8. The source baseline is Tightbeam commit
   \`ea3e9c1879978b9362d30eea8973352d9dce8c1b\`. The live census came from release \`0.1.8\`,
   build \`1337\`, source stamp \`fdb3db5\`.

## Invariants

### Ruling provenance

P1. One immutable \`operator_ruling_submissions\` row stores these fields:

| Field | Contract |
| --- | --- |
| \`id\` | canonical submission id |
| \`requestId\` | existing operator request id |
| \`kind\` | \`recommendation\` or \`binding-confirmation\` |
| \`authorityPrincipal\` | request owner as \`user:<id>\` |
| \`actorPrincipal\` | authenticated submitter, or \`legacy-unknown\` only for migration |
| \`actorSessionState\` | \`known\`, \`none\`, or \`legacy-unknown\` |
| \`actorSessionKey\` | required only when session state is \`known\` |
| \`transportClass\` | \`user-device\`, \`session-cli\`, \`org-cli\`, or \`legacy-unknown\` |
| \`sourceKind\` | \`submission-bytes\`, \`message\`, or \`legacy-unknown\` |
| \`sourceRef\` | immutable carrier id, or null only for \`legacy-unknown\` |
| \`sourceSha256\` | lowercase 64-hex digest, or null only for \`legacy-unknown\` |
| \`decision\` | exact submitted option label or response text |
| \`rationale\` | exact submitted rationale, nullable |
| \`submittedAt\` | ingress time in epoch milliseconds |
| \`delegationId\` | nullable; used only if Open Question option A is selected |

The table permits no update or delete. The decision-request row gains nullable
\`bindingSubmissionId\`. A future terminal operator write requires a reference to one binding
confirmation for the same request.

P2. The gateway derives actor, session, and transport fields from authenticated ingress before
identity projection. It strips caller parameters with those names. The handler stores the
authenticated actor separately from the requested authority.

P3. The mutation stores exact submission bytes in the private message/content store or one new
private immutable byte carrier. It stores the carrier id and SHA-256 in the submission row. A
message source is admissible only when its stored sender is the authority user, its stored
device belongs to that user, and its digest matches. These checks and binding are one
transaction.

P4. Under the recommended policy, a session call creates only a recommendation and leaves the
request open. A user-device call can create a binding confirmation. An org CLI call creates no
ruling submission because that credential proves no human or session actor.

P5. A binding transaction inserts the submission, sets \`bindingSubmissionId\`, changes the
request to ruled, files the ruling fact, schedules the raiser notification, and emits the
existing lifecycle event. A rollback exposes none of those effects.

P6. Idempotency is scoped to actor principal, request id, and client submission key. An equal
retry returns the first submission. An unequal retry returns
\`ruling_submission_conflict\`. Two binding confirmations racing for one open request produce
one winner. The loser returns \`decision_request_not_open\` and commits no source bytes.

P7. Recommendations remain attached to their request. Supersession does not copy them. A
successor can cite an old recommendation as context but cannot bind it.

P8. Migration records the maximum pre-activation ruling fact id as the provenance epoch. It
classifies old operator terminal rows as follows:

| Retained evidence | Migrated classification |
| --- | --- |
| non-null \`ruledViaSessionKey\` | session known; transport \`session-cli\`; actor and source \`legacy-unknown\` |
| null \`ruledViaSessionKey\` | actor, session, transport, and source \`legacy-unknown\` |
| valid post-baseline performer fields | preserve those known values; source stays \`legacy-unknown\` without a carrier |

Migration emits no direct-user classification and creates no source text. A terminal row above
the epoch without a valid binding submission refuses as
\`decision_request_provenance_invalid\`.

P9. Owner-authorized detail returns authority, actor, session state, transport, submission
kind, source kind, reference, digest, and timestamps. It returns source text only when the
caller can already read that private carrier. List views use exactly these labels: \`Mike
confirmed\`, \`session recommendation\`, \`session-mediated legacy ruling\`, and \`legacy
attribution unknown\`.

P10. Existing REST decision-request routes and Firehose
\`decision_request.opened|ruled|consumed|withdrawn|superseded\` frames remain byte-compatible.
The versioned \`operator ruling submissions\` resource exposes owner-visible submissions. Its
Firehose classes are \`operator_ruling_submission.recommended\` and
\`operator_ruling_submission.bound\`, with \`schemaVersion:1\`, \`op:\"upsert\"\`, request id,
and submission id. REST and Firehose use one authorized serializer.

P11. Audit and refusal output contains ids, enums, digests, and cause codes. It contains no
decision, rationale, message, attachment, or source text. Authorization runs before existence
disclosure. A hidden id and an absent id return the same detail body.

P12. After restart, a committed submission appears once and an uncommitted submission is
absent. Recovery does not derive actor, source, or delegation from chronology. The provenance
epoch is the only migration cutoff.

### Persistent alerts

A1. Org policy schedules one persistence check for the exact assertion fact id when a
\`user-alerted\`, \`harness-auth-dead\`, or \`harness-rate-limit-dead\` episode begins. The due
time is assertion time plus 900,000 milliseconds.

A2. At the due boundary, one transaction rechecks the exact episode and files one operator
request only if it still stands. The idempotency key is
\`persistent-alert:<fact-kind>:<assertion-fact-id>\`. A committed retraction produces no
request.

A3. The request has the closed action menu \`re-staff\`, \`park\`, and \`acknowledge\`. These
are instructions for the accountable agent. The substrate does not perform those actions.

A4. The owner delivery line is:

> Tightbeam has been unable to reach an agent for 15 minutes. Choose re-staff, park, or acknowledge. Status: {standing|recovered}.

The message carries the request id and alert kind as typed metadata. It carries no private
failure text.

A5. Recovery after request filing appends the matching retraction fact to the request's
observable basis and changes its derived display status to \`recovered\`. It does not withdraw,
rule, consume, supersede, or close the request. The same episode cannot file a second request.
A later assertion is a new episode.

A6. \`user-alerted\` uses its owner scope. Harness auth and rate-limit episodes resolve the
owner through the existing affected-session and host relation. Zero or several owners produce
\`persistent_alert_owner_unresolved\` and no decision request.

A7. The alert rule is org policy over substrate facts. Removing the policy removes only
persistence escalation. It does not remove facts, terminal alerts, quarantine, or recovery.

## Architecture

### One mutation seam

\`submit_operator_ruling\` is the only new mutation seam. It receives a request id, candidate
answer, optional rationale, client submission key, and optional exact-message reference. The
gateway adds the authenticated actor, transport, and byte carrier. The handler selects
recommendation or binding confirmation from authenticated authority and the selected policy.
Callers cannot select the kind.

\`operator-rule\` becomes a direct-user binding surface. A session receives
\`direct_user_confirmation_required\` and a pointer to \`operator-recommend\`. The recommendation
command does not accept \`--as-user\`; it uses the session principal from its credential. The
current decision-request row remains the canonical outcome. The submission table explains how
that outcome arrived and stores recommendations; it is not a second lifecycle.

### Exact source and confirmation

A user action sends the request id and exact confirmation bytes through user-device
authentication. Ingress stores the bytes once and binds their digest to the submission. A user
action can cite an earlier owner-authored message only when the transaction verifies sender,
device ownership, and digest. An agent can quote or summarize Mike only inside a recommendation.

### Delegation seam

Option B, recommended, authorizes only user-device binding confirmations. Option A also
requires an immutable delegation row whose owner, session, request scope, allowed option set,
activation time, and expiry match in the binding transaction. An absent, expired, revoked,
differently scoped, or legacy delegation refuses. The system does not parse free-text
delegation. The schema keeps nullable \`delegationId\` so the Mike decision does not force a
schema rewrite.

### Rollout and rollback

Rollout performs a read-only preflight, creates the submission table and epoch, adds
\`bindingSubmissionId\`, migrates legacy classifications, installs future-write integrity
triggers, and activates the writer at one schema boundary. Activation refuses an unknown
terminal shape, duplicate binding reference, invalid digest, or post-epoch terminal row
without provenance.

The activation gate includes a real HTTP fixture proving that the router retains authenticated
transport separately from projected identity. A unit call that injects
\`transport_session_key\` does not satisfy this gate.

Rollback before activation leaves no new state. Rollback after activation preserves the
table, epoch, column, and triggers. An older binary can serve unaffected reads and work, but
its operator writer returns \`ruling_provenance_writer_unavailable\`. Rollback does not delete
evidence or re-enable an unproven writer.

### Persistent-alert policy

One org-authored policy production observes the existing fact stream. It schedules the exact
episode boundary, rechecks standing state, and files the existing operator-request kind with
the closed action menu. It uses the provenance seam for recommendations and confirmation. It
adds no alert state beyond the assertion fact id, ordinary scheduled check, and ordinary
decision request.

## Acceptance

T1 — Given the frozen August 20 through August 30 fixture, when migration classifies the 294
Mike-attributed rulings, then 3 are session-mediated legacy, 291 are legacy attribution
unknown, and 0 are direct-user. Any input order produces identical classification and epoch
bytes.

T2 — Given a session credential and \`--as-user mike\`, when the real CLI and HTTP router reach
the seam, then actor remains that session, session state is known, transport is session-cli,
and option B cannot bind. Given an org credential with \`asUser:\"mike\"\`, then the call returns
\`authenticated_actor_required\` and creates no submission.

T3 — Given Mike's active device credential, an open request, and exact confirmation bytes,
when he confirms, then one transaction creates one binding submission, rules the request,
files one ruling fact, schedules one raiser notification, and hands off compatible events
after commit. A mismatched digest returns \`ruling_source_mismatch\` and leaves those effects
absent.

T4 — Given an agent recommendation, when Mike reads list and detail, then the request stays
open, the list says \`session recommendation\`, and detail names actor, session state,
transport, source kind, and digest. Given a migrated null-session row, then the list says
\`legacy attribution unknown\`.

T5 — Given an equal retry, when it reaches the seam, then it returns the first submission id
without another row or event. An unequal retry returns \`ruling_submission_conflict\`. Given
two confirmations race, then one wins and the loser commits no bytes. Given supersession,
then old recommendations stay only on the old request.

T6 — Given the owner, an admin without message-read authority, and an unrelated user, when
each reads lists, details, logs, and Firehose, then only the owner receives source text; the
admin receives authorized metadata; the unrelated user receives no row-identifying response
or event. Logs and events contain no candidate, rationale, message, attachment, or source text.

T7 — Given pre-change exact-key fixtures, when an open request receives a recommendation and
later binds, then existing REST decision-request responses and existing Firehose frames remain
byte-equal. A new client reconstructs the new submission resource after missed, duplicate, or
reordered version-1 events.

T8 — Given process loss before commit, when service restarts, then no submission, terminal
change, fact, wake, or event exists. Given loss after commit, then one submission and terminal
exist and an equal retry returns them. Given rollback after activation, then the old writer
refuses while unrelated reads and mutations remain available.

T9 — Given each supported alert retracts at 899,999 milliseconds, when its check runs, then no
request exists. Given it remains standing at 900,000 milliseconds, then one request with the
exact menu and delivery line exists. A boundary race produces one request only if the filing
transaction observes the episode standing.

T10 — Given a persistent-alert request is open, when its episode retracts, then the request
stays open, display status becomes \`recovered\`, and Mike receives no second alert. A later
standing assertion can file one new request. An unresolved harness-alert owner produces the
typed refusal and no guessed owner.

Trace: P1-P4 and P8 map to T1, T2, and T4. P3-P7 map to T3 and T5. P9-P11 map
to T4, T6, and T7. P12 maps to T5 and T8. A1-A2 map to T9. A3-A7 map to T9
and T10.

## Open Questions

Q1 — **BLOCKING only for activation of the binding writer. Recommendations, reads, migration
fixtures, and persistent-alert filing can proceed.** May an explicitly scoped session
delegation issue a binding ruling in Mike's authority, or may sessions only submit
recommendations for Mike's direct confirmation?

- **Option A — scoped delegation can bind.** The transaction requires the immutable delegation
  row described in Architecture.
- **Option B — sessions recommend; Mike confirms directly. RECOMMENDED.** This preserves the
  evidence hierarchy, removes routine impersonation, and keeps agents useful without turning
  their paraphrase into Mike's words.

No other open question remains.
