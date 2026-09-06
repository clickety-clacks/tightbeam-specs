# Visitor principal v3 — current-main contract

Status: SPEC-READY FOR ONE INDEPENDENT EXACT-REVISION REVIEW after final-
recovery `changes-requested`; not implementation authority; the work item
remains untargeted and unbound until review clears this amended exact content.

Authority and identity:

- Work item: `wi_4ee303fa-12ed-4747-bce0-fc48024f4d53`.
- Spec continuation assignment:
  `asg_3ff49b50-3856-4388-8d4e-255a7d450d95`.
- Sanctioned green source baseline: Tightbeam main
  `8eeccbd6dfd221fe9d105783459637fb7a17ea83`.
- Current source census tip: Tightbeam main
  `7a70a2f616363074514237b5bee48ba67c52e2ea`; the sanctioned baseline is its
  ancestor.
- Canonical path: `visitor-principal-v3.md` in `tightbeam-specs`.
- Historical `art_d824eab5` and archived `art_765e7a53` are evidence only.
  This file supersedes their v1 and v2 designs after review clears this file.
- Reviewed `art_a86b44c7` is evidence only. Its closed `ActorContext` design is
  absent from the source baseline and this canonical repository.
- Review verdict `att_5efefdde-9ef9-4e57-bb42-792e73493923` and report
  `art_b591a285` govern this amendment. This revision closes findings F1-F7 by
  defining the external surface and key custody, scoping operation identity,
  naming the stamped migration, preserving immutable principal provenance,
  deleting decline and frozen-page replay, and adding negative acceptance
  cases.
- Successor verdict `att_f88643c7-e13e-4e53-a3fd-f98fcbe42583` and report
  `art_415294a6` govern this second amendment. It repairs the post-accept
  authorization join, closes nested wire projections, consumes the current
  lifecycle attribution seam, gives malformed known-bearer attempts a bounded
  server-owned audit namespace, defines no-replace keyring publication, and
  makes discovery order exact.
- Final-recovery verdict `att_9cefd0e7-1cd6-46e1-a9dc-a79ac50fba44` and report
  `art_f09335b6` govern this third amendment. They confirm the predecessor F1-F6
  closures and require a deterministic bound on durable evidence growth caused
  by a known external credential. I12A and A22 close that sole finding with
  fixed per-scope admission rows, minute and lifetime caps, and row-neutral
  over-limit refusal.
- Realized-cost specimen `att_1a77f64a-454a-4737-8e6c-7e3cb8346767` under
  closed `wi_aa14fcd4-f6e1-43d2-b87d-e95b4f84adb1` motivates the external-
  intermediary boundary. Closed actor-typing evidence is
  `art_a86b44c7` / SHA-256
  `15dc2ccf5b16c98c9353c6b8234733cdc7bd5c5ffc05de34b0a41ac1604c1cd1`
  with reviewed-clean verdict
  `att_c2e85ec7-c9ed-4f46-b842-c134662c7fe4`. This spec consumes those facts
  without reopening either work item or depending on the unlanded artifact.
- This spec teaches no new agent operating pattern. It requires no guidance
  amendment.

The six operator requests named in Mike's 2026-08-25 RULE YOUR OWN direction
were withdrawn because this session was not their operator owner. This spec
records the resulting writer rulings:

| Request | Ruling | Reason |
|---|---|---|
| `dr_8e4c3389-fd8e-4e60-8351-5906cf6e8e66` | `external-principal-human-broker` | The outside participant remains the effective principal. The sanctioning human is broker provenance, never substituted attribution. |
| `dr_344bc5cb-8917-4ed0-9e21-8a38ea3e8eec` | `visitor-local-envelope` | Current main cannot depend on an unlanded actor contract. A closed local envelope preserves a lossless later mapping. |
| `dr_104f953f-f2b4-40bd-8850-9ebab593c9d1` | `replay-only-mvp` | Durable cursor replay satisfies the visitor goal while deleting push-specific authority and recovery machinery. |
| `dr_730368f2-c6b8-4c07-a280-886c47fb107c` | `bounded-aggregate-only` | Unknown credentials must not create durable per-bearer identifiers or unbounded rows. |
| `dr_6bfbadce-8d45-41d2-a0f5-6a34e35d3549` | `preflight-and-refuse` | A migration must not invent actors or bless orphan attribution. |
| `dr_4bad9e98-43de-46c8-9c39-889510e2e9c5` | `one-session-read-post` | One exact existing session with independent read and post grants is the smallest useful external scope. |

## 1. Goal

Add a first-class external visitor principal that can receive a human-sanctioned
grant to read and/or post in one exact existing Tightbeam session. Every
post-accept visitor operation shall preserve four distinct facts: the effective
visitor principal, the presenting visitor access session, the sanctioning user
broker, and the operation cause. Pre-accept invitation presentation and
broker-authenticated actions shall use their own closed audit contexts and
shall not invent a visitor actor.

The implementation shall serve transcript history through ordinary durable
cursor replay. A repeated cursor with a new operation id may observe entries
that committed after an earlier page; this MVP makes no frozen-page promise.
A visitor post shall use the existing atomic message-append and turn-enqueue
seam. The implementation shall add the listed database backstops for existing
session, work-item, assignment, and assignment-reopening attribution before it
makes visitor identity available.

Subtraction ruling: DELETE live visitor push and credential rotation from this
MVP. Durable replay, short-lived access, and revocation satisfy the stated goal.
Adding push would also add subscription authority, revocation fences, delivery
claims, recovery, and hung-writer policy. Adding rotation would add overlapping
credential generations and a second recovery protocol. Neither is necessary to
prove visitor identity, attribution, read, post, or revocation.

Realized-cost evidence: at `2026-08-25 07:21:07`, two external intermediary
sessions both selected `--as-user mike` and attempted opposite rulings on
`dr_4edb91e6` and `dr_45999b0f` within seconds. Arrival order selected policy;
the losing writes returned `not_open`. The durable rows identify only
`user:mike`. They cannot distinguish Mike from either intermediary, identify
which external mind attempted each ruling, represent concurrent conflicting
authority, or preserve a delegation boundary. This contract prevents that
class for visitor access: the external mind is a visitor principal, the human
is broker provenance, and visitor credentials carry no user, operator, or
decision authority.

## 2. Non-Goals

1. This spec does not make a visitor a user, device, agent, process, remedy,
   role, archetype, assignment holder, work-item actor, or ordinary Tightbeam
   session owner.
2. This spec does not create a row in `sessions` for a visitor access session.
3. This spec does not grant dispatch, tune, wake, spawn, delegate, assign,
   attest, artifact, operator, administration, model, harness, tool, file,
   network, or host capabilities to a visitor.
4. This spec does not add live visitor events, socket subscription, server push,
   delivery claims, push acknowledgment, recovery replay, or a revocation fence.
5. This spec does not rotate a visitor credential. Revocation followed by a new
   invitation is the MVP replacement operation.
6. This spec does not implement the reviewed but unlanded closed
   `ActorContext` design. It defines the visitor-local envelope required for a
   lossless future adapter.
7. This spec does not assign `operationalParent`, provider, model, harness,
   effort, context, host, role, archetype, seed version, or delegation-card
   anatomy to a visitor access session.
8. This spec does not repair an orphaned historical identity reference, invent a
   placeholder actor, or split valid and invalid rows during migration.
9. This spec does not expose an organization inventory, a session key, user
   identifiers, access credentials, tool traffic, internal prompt metadata, or
   content from any session other than the exact grant target.
10. This spec does not target, implement, self-review, merge, or dispose the
    visitor work item.
11. This spec does not add invitation decline. Pending invitations leave the
    pending state only through acceptance, expiry, or target retirement.
12. This spec does not rewrite the collision's historical decision rows or the
    closed actor-context artifacts. It does not treat the prose-only split
    between targeting/release work and queue-triage/lane-unsticking work as
    policy, a grant, or a delegation record.
13. This spec does not grant a visitor operator-decision authority. A future
    product that does so requires a separate reviewed contract for explicit
    scope, conflict handling, concurrency visibility, revocation, and audit.

## 3. Terms

### Visitor principal

A **visitor principal** is the first-class effective actor
`{:visitor, visitorPrincipalId}`. Its canonical origin string is
`visitor:<visitorPrincipalId>`. It is not a user alias and never resolves to the
broker user.

### Broker

The **broker** is the existing user who creates the invitation and sanctions the
external participant's limited access. `brokerUserId` is durable provenance.
Broker status does not make the broker the effective actor of a visitor action.

### External intermediary

An **external intermediary** is the outside human or agent represented by the
visitor principal. It is never represented as the broker user, even when that
user sanctioned its access. One invitation sanctions one external principal.
The invitation and access credentials are bearer credentials for that one
principal and must not be shared. Tightbeam attributes a presentation to the
principal and access-session rows resolved by the bearer; it does not claim to
detect out-of-band credential sharing.

### Delegation boundary

The **delegation boundary** is the closed visitor authority projection:
`transcript-read`, `post` when granted, and `self-revoke`. It contains no user,
operator, decision, targeting, release, queue-triage, or lane-unsticking
authority. Prose, a display label, `brokerUserId`, and `--as-user` text cannot
add to it.

### Visitor grant

A **visitor grant** binds one visitor principal to one existing `sessions` row.
It contains independent `canRead` and `canPost` booleans. At least one boolean is
true. The target cannot change after invitation creation.

### Visitor access session

A **visitor access session** is a credential-bearing presentation record for
one visitor grant. It is stored separately from `sessions`. It cannot carry or
inherit agent execution anatomy.

### Visitor actor envelope

`VisitorActorEnvelopeV1` is the closed current-main attribution value:

```json
{
  "schema": "visitor-actor-envelope-v1",
  "actorKind": "visitor",
  "actorId": "vis_exact",
  "presenterKind": "visitor-access-session",
  "presenterId": "vss_exact",
  "brokerKind": "user",
  "brokerId": "usr_exact",
  "cause": "visitor-post",
  "targetSessionKey": "session_exact",
  "invitationId": "vin_exact",
  "grantId": "vgr_exact",
  "operationId": "vop_exact"
}
```

The closed visitor-envelope `cause` set is `visitor-transcript-read`,
`visitor-post`, `visitor-self-revoke`, `visitor-authority-denied`, and
`visitor-invalid-request`. The last two causes are server-generated at an
authentication boundary and never reach a domain handler. A later adapter to a
landed general
actor context shall preserve every field and shall not replace `actorId` with
`brokerId` or `presenterId`.

### Invitation presentation

`InvitationPresentationV1` is the pre-principal context for a known invitation
credential. It contains schema, invitation id, broker user id, exact target
session, and cause. For `invitation-read` and `invitation-accept`, it contains
the required operation id and request fingerprint. For
`invitation-invalid-request`, it has no operation id or fingerprint and contains
the server-generated rejection id plus the required closed route and shape
classes. Those three values are its complete cause set. It contains no actor id
or visitor access-session id. A successful acceptance terminal can add the
resulting visitor principal, grant, and access-session ids without rewriting
the attempted context.

The **rejected-operation namespace** is separate from client operation
identity. For each admitted schema-invalid request whose bearer resolves to a
known invitation or visitor access session, the server creates one rejection id
`vrej_` plus 32 lowercase hexadecimal characters and stores that id unchanged
on the attempted and denied rows. The audit operation id is SQL `NULL`; the
server never copies, repairs, hashes, or guesses a missing or malformed client
operation id. A retry is a new rejected request with a new rejection id and no
idempotency relation to the earlier rejection. The cause is
`invitation-invalid-request` for an invitation bearer and
`visitor-invalid-request` for a visitor bearer. A visitor-bearer rejection uses
context kind `visitor-rejected-operation`, scopes to the authenticated visitor
principal, and retains the exact access-session and broker provenance. An
invitation-bearer rejection uses context kind
`invitation-rejected-operation`, scopes to the known invitation, and invents no
visitor principal. Neither context creates a `visitor_operations` row. The
audit stores one closed shape class:
`missing-operation-id`, `invalid-operation-id`, `invalid-json`, `missing-key`,
`unknown-key`, or `invalid-value`. It also stores the exact closed route class:
`invitation-read`, `invitation-accept`, `transcript-read`, `post`, or
`self-revoke`. It stores no raw body, field value, credential, or parser error
text.

A broker-authenticated `invitation-create` or `broker-revoke` is an ordinary
user action. Its audit context preserves that user actor and any resulting or
targeted visitor ids. It does not use `VisitorActorEnvelopeV1`.

### Canonical consent bytes

**Canonical consent bytes** are UTF-8 bytes generated by a versioned,
deterministic encoder over the invitation id, broker id, target display label,
visitor display label, `canRead`, `canPost`, issue time, expiry time, and consent
text version. The acceptance row stores the encoder version and SHA-256 digest.
It never relies on rendered HTML or client prose as the authoritative value.

### Acceptance key

An **acceptance key** is a client-generated opaque idempotency key. The database
stores its SHA-256 digest and a request fingerprint, never the raw key. The
unique key is `(invitationId, acceptanceKeyDigest)`.

### Request fingerprint

A **request fingerprint** is SHA-256 over the versioned canonical bytes of the
operation's semantic input. It excludes credentials, acceptance keys, and
operation ids. The same id with a different fingerprint is a conflict, not a
retry.

### Terminal visitor state

An invitation starts `pending` and can become `accepted`, `expired`, or
`target-retired`. Acceptance consumes the pending invitation by terminalizing it
as `accepted`; no invitation state is live after acceptance. The same acceptance
transaction creates the visitor principal, grant, and access session in state
`active`. A principal, grant, and access session can each become `revoked`,
`expired`, or `target-retired`. Every transition is one-way and uses
compare-and-set from its one live state. Principal identity and provenance
fields are immutable; only its lifecycle state, terminal time, and terminal
reason can change.

## 4. Assumptions

1. The target is an existing ordinary `sessions` row at invitation creation.
2. An existing owner/admin authorization seam determines whether a user may
   invite or broker-revoke for the target. This spec does not infer authority
   from possession of a session key.
3. Tightbeam has one authoritative database transaction boundary for visitor
   rows and the existing message/turn rows.
4. Server time is authoritative. A resource is expired when
   `now >= expiresAt`; no scheduler is required for correctness.
5. The invitation default lifetime is 24 hours and the maximum is 7 days. The
   access-session default lifetime is 7 days and the maximum is 30 days.
6. One broker may have at most 20 pending invitations. A transaction that would
   exceed that count refuses before inserting a row.
7. A visitor post body is valid UTF-8 and at most 65,536 bytes. Attachments are
   empty in this MVP.
8. The durable post quota is 10 accepted visitor posts per rolling 60 seconds
   per grant. A denied or duplicate post does not consume quota.
9. A known invitation bearer may pass admission at most 60 times per UTC minute
   and 1,000 times over that invitation's lifetime. A known visitor bearer may
   pass admission at most 60 times per UTC minute and 50,000 times over that
   visitor principal's lifetime. One full 200-entry transcript page per minute
   for the maximum 30-day access lifetime consumes 43,200 visitor admissions.
10. Transcript ordering and cursor semantics reuse the existing durable session
   transcript sequence. The visitor surface neither invents a second sequence
   nor reads live frames. A page reads the rows committed when that request's
   transaction takes its snapshot; the cursor is not a frozen result handle.
11. The operator provisions the visitor keyring before the stamped migration.
    The database and keyring are backed up and restored as one deployment unit.

## 5. Invariants

**I1 — Exact effective actor.** Every accepted or denied well-formed operation,
and every admitted malformed request, authenticated by a known visitor access
session records `actorKind=visitor` and the exact visitor principal id. It never
records the broker, access session, target owner, or target agent as the
effective actor. An I12A refusal creates no actor record. Invitation
presentation records no effective actor. Broker actions record their
authenticated user actor.

**I2 — Separate provenance.** Every audit record for an operation authenticated
by a known visitor access session stores the exact visitor principal, visitor
access session, broker user, cause, target session, invitation, grant, and
operation ids from `VisitorActorEnvelopeV1`.

**I3 — Closed origin.** The origin parser, serializer, transcript projection,
message sender projection, lifecycle principal projection, lifecycle
`origin`/`authenticatedCaller` detail, and audit projection accept and preserve
the closed visitor origin. No string fallback can turn an unknown origin into a
visitor.

**I4 — One exact target.** Authorization joins an access session whose state is
exactly `active`, a grant whose state is exactly `active`, the immutable
visitor-principal identity referenced by both whose lifecycle state is exactly
`active`, the terminal invitation whose state is exactly `accepted`, and the
exact existing target session in one database read inside the operation
transaction. It applies principal, access-session, and grant expiry in that
transaction before authorizing. It never requires a nonterminal invitation and
does not accept a client-supplied replacement target.

**I5 — Independent least privilege.** Read requires `canRead=true`. Post
requires `canPost=true`. Either denial is indistinguishable from an unavailable
target and performs no target read or mutation.

**I6 — Broker is provenance, not delegation.** A broker can create or revoke a
grant only through existing owner/admin authorization. The visitor cannot use
the broker's user permissions. An outside agent presenting the visitor
credential remains the visitor principal.

**I7 — Consent proof.** Acceptance requires an affirmative decision over the
exact canonical consent bytes. The acceptance transaction stores the consent
version and SHA-256 digest, compare-and-sets the invitation from `pending` to
terminal `accepted`, and inserts the principal, principal admission row, grant,
and access session as `active` atomically. No transaction can expose an active
principal with a pending invitation or an accepted invitation without its
active principal, fixed admission row, grant, and access session.

**I8 — Secret handling.** Raw invitation and access credentials never enter a
durable row, log, error, trace, audit payload, artifact, or response other than
the credential-bearing creation response and deterministic acceptance success
responses. Stored credential values are
`HMAC-SHA-256(credentialDigestKey[keyId], credentialBytes)` with an explicit key
id and credential version. A CLI reads a credential only from the safe input
seams in Architecture; it never accepts a credential or acceptance key in
argv. Derivation and digest keys are distinct, durable, and governed by the
keyring refusal and retention law in Architecture.

**I9 — Deterministic credential retries.** For the same invitation-create
operation id and request fingerprint, every retry returns the same invitation
credential bytes and invitation id. The server derives the invitation
credential as:

```text
"tbi_" || base64url(
  HMAC-SHA-256(
    key[keyId],
    "tightbeam/visitor-invitation-credential/v1\0" ||
    invitationId || "\0" || credentialVersion
  )
)
```

For the same invitation, acceptance key digest, and request fingerprint, every
acceptance retry returns the same access credential bytes and ids. The server
derives the access credential as:

```text
"tbv_" || base64url(
  HMAC-SHA-256(
    key[keyId],
    "tightbeam/visitor-credential/v1\0" ||
    visitorAccessSessionId || "\0" || credentialVersion
  )
)
```

Each stored credential digest is computed over its exact returned bytes. An
operation id with a different fingerprint refuses. Reuse of one acceptance key
with the same fingerprint and a new operation id returns the same deterministic
accepted result, creates one audit pair for the new operation id, and creates no
new principal, grant, access session, or acceptance. Reuse of that key with a
different fingerprint is an operation conflict. A different acceptance key
after terminal acceptance returns the generic unavailable result.

**I10 — Transactional post.** One accepted visitor post atomically commits one
visitor-origin prompt echo, one turn enqueue, the enqueue's accepted
`turn_lifecycle_events` row, one consumed quota unit, and the
attempted-plus-accepted audit pair. The lifecycle row's `principal`, detail
`origin`, and detail `authenticatedCaller` are all exactly
`visitor:<visitorPrincipalId>`; none can be the broker, presenter, target, or
substrate. Any failure commits none of those effects except a terminal denied
audit pair when the credential resolved to a known visitor context.

**I11 — Read-before-return evidence.** A successful transcript read commits its
attempted-plus-accepted audit pair before returning content. If that audit
commit fails, it returns no content. A transcript-read operation id is
single-use: repeating it returns `visitor_read_retry_requires_new_operation`
without reading target content or adding audit rows. Repeating `afterSeq` with a
new operation id performs an ordinary new cursor read and can observe later
commits.

**I12 — Admitted known operations are paired.** Every request that passes I12A
and is a well-formed known invitation or visitor access-session operation, and
every broker-authenticated operation, records exactly one attempted audit row
and exactly one terminal `accepted` or `denied` row under a
principal-and-cause-scoped operation key in the same transaction as its
outcome. Retrying a mutation with the same scoped operation id and fingerprint
returns its stored result without duplicating either row. Transcript reads use
the single-use rule in I11. A scoped id with a different fingerprint is a
conflict. The same operation-id bytes under a different principal or cause are
independent operations. A schema-invalid known invitation or visitor request
that passes I12A instead records exactly one attempted/denied audit pair under
a fresh rejection id in the stable rejected-operation namespace and the closed
invalid-request cause in one transaction. It keeps `operationId=NULL`, creates
no operation row, and invokes no domain handler. A visitor bearer scopes the
pair to its authenticated visitor principal; an invitation bearer scopes it to
the known invitation and invents no principal. A request refused by I12A is not
an operation and creates no per-request evidence. An unknown bearer follows
I13 and creates no such pair.

**I12A — Known external admission is finite.** After resolving a known
invitation or visitor bearer and before validating request shape, assigning an
operation or rejection id, reading target content, or invoking a domain
handler, the server atomically admits or refuses the request against one fixed
durable scope row. All invitation routes share the invitation row. All visitor
routes and access sessions share the visitor-principal row, including a known
visitor bearer presented to a privileged route. Each scope admits at most 60
requests in the UTC minute whose start is
`floor(serverEpochMilliseconds / 60_000) * 60_000`. An invitation scope admits
at most 1,000 requests over its lifetime. A visitor-principal scope admits at
most 50,000 requests over its lifetime. Malformed requests and replay attempts
consume admission exactly like other requests. A request that would exceed
either bound creates no operation, rejection, audit, target, domain, or other
durable mutation. Its refusal does not update the fixed scope row. Concurrent
admission cannot exceed a bound. Minute rollover updates the existing row; it
never inserts a window row. On a visitor route the refusal is the exact visitor
rate-limit result in 6.5. On a pre-existing privileged route it retains that
route's existing `auth_failed` response. Therefore one invitation can cause at
most 1,000 operation rows and 2,000 audit rows, and one visitor principal can
cause at most 50,000 operation rows and 100,000 audit rows through
bearer-authenticated requests.

**I13 — Unknown bearers are bounded.** A credential that resolves to no
invitation or access session creates no visitor principal, audit, credential
digest, token fingerprint, IP address, header capture, or request row. It only
updates one fixed aggregate row for its closed operation class.

**I14 — Revocation and expiry are act-time facts.** Every read and post checks
terminal and expiry state in its transaction. Revocation terminalizes the
active principal, grant, and all active access sessions atomically. A concurrent
post either commits completely before revocation or refuses completely after
revocation. Revocation does not mutate the accepted invitation or any immutable
principal identity/provenance field. Expiry terminalizes the active principal,
grant, and access sessions. Target retirement terminalizes a pending invitation
before acceptance or the active principal, grant, and access sessions after
acceptance. Every post-accept terminal path changes only lifecycle state, time,
and reason on the principal.

**I15 — Replay only.** No visitor operation registers a socket, subscription,
push consumer, delivery cursor, claim, acknowledgment, or recovery job. The
only visitor content surface is explicit durable cursor replay.

**I16 — Identity backstops precede availability.** Visitor availability remains
disabled until the migration has added and validated the identity foreign keys
listed in Architecture. An orphan preflight refuses the complete migration;
it never performs a partial rebuild or creates a placeholder row.

**I17 — Transport identity and checked broker identity.** Ordinary AU2 reads
and dispatch retain self-declared transport identity: `agent_identity/3` does
not assert that an `asUser` row exists. Commit
`c09cf0693507226b3d5c8806c43666ef491b71cb` deliberately superseded the general
existence check introduced by `a0299e8c`; this Visitor contract does not
restore that check or change ordinary AU2 behavior.

Transport identity is not authorization for a Visitor broker operation.
The existing CLI-token, checked-`asUser`, and owner/admin requirements for
`visitor-invitation-create` and `visitor-broker-revoke` in section 6.5 remain
unchanged. Their checked-user boundary is before Visitor broker dispatch,
not a universal check on ordinary AU2 dispatch. A15's typed authentication
refusal for a nonexistent broker `asUser`, before Visitor dispatch and with
no Visitor audit, remains required; ordinary AU2 acceptance cannot bypass it.
This distinction adds no check architecture or refusal type. Visitor
authentication has no `asUser` selector and cannot construct an authoritative
user actor.

**I18 — Agent anatomy does not leak.** A visitor access session cannot satisfy
an ordinary session foreign key and cannot acquire `operationalParent`, typed
model/harness state, or r5 seed/delegation anatomy. A future visitor-agent
product requires a separate spec.

**I19 — Indistinguishable absence.** Unknown credential, wrong target,
unauthorized capability, revoked state, expired state, retired target, and a
missing target produce HTTP `404` and exactly
`{"error":{"code":"visitor_unavailable"}}`, with no `message` field. Those
conditions produce the same CLI exit code `4` and the same stderr line
`visitor unavailable`. No response distinguishes which join failed.

**I20 — No identity deletion cascade.** New foreign keys use restrictive
identity deletion. Deleting a user or ordinary session cannot erase or orphan
historical attribution, visitor provenance, consent, or audit.

**I21 — One checked visitor actor source.** After bearer resolution, one closed
visitor actor value derives origin `visitor:<principalId>`, visitor-only
authority, principal/access-session/broker attribution, target, and cause.
For posts it also derives the turn lifecycle `principal`, detail `origin`, and
detail `authenticatedCaller`. Callers cannot supply any of those projections
beside it. The broker id and target never derive authority. This imports the
coherence rule proven by
closed `art_a86b44c7` without importing its unlanded type. A known visitor
credential presented to a user, operator, agent, device, session, or websocket
authority seam records a `visitor-authority-denied` pair identifying the
visitor principal and presenter, then refuses before policy or domain effects.
This pair is required only when I12A admits the request; an admission refusal
keeps the pre-existing seam's response and creates no pair.

## 6. Architecture

### 6.1 Current-main seams

The implementation shall preserve the source facts first inspected at green
baseline `8eeccbd6dfd221fe9d105783459637fb7a17ea83` and shall rebase against current
main `7a70a2f616363074514237b5bee48ba67c52e2ea`. Citations without a second commit
suffix are to the green baseline; rows that name `7a70a2f` are additive landed
current-main facts:

| Fact | Source citation |
|---|---|
| Agent dispatch authenticates first, then builds identity, and carries separate origin and principal | `lib/tightbeam/wire/router.ex:129-146`; `lib/tightbeam/dispatch.ex:37-53,73-81` |
| The router has one closed agent-verb set and separate CLI/session/device bearer classifiers; no visitor class exists | `lib/tightbeam/wire/router.ex:55-57,421-458` |
| Organization and session `asUser` construction does not prove a user row | `lib/tightbeam/wire/router.ex:466-560` |
| Typed user target lookup already demonstrates the required existence check | `lib/tightbeam/wire/router.ex:648-651` |
| Current rate limiting is in-memory and device/WebSocket-specific; no generic HTTP admission bound exists for visitor routes to inherit | `lib/tightbeam/conn_registry.ex:118-121,209-216`; `lib/tightbeam/wire/socket.ex:219-240` at `7a70a2f` |
| Origin is a closed user/agent/process/remedy type with no visitor | `lib/tightbeam/origin.ex:1-35` |
| Ordinary sessions require `operationalParent` but `ownerUserId` lacks its identity backstop | `lib/tightbeam/org.ex:63-91` |
| Work-item user/session actor columns lack identity foreign keys | `lib/tightbeam/work_items.ex:34-53` |
| Assignment opener/closer and reopening snapshot actor columns lack identity foreign keys | `lib/tightbeam/assignments.ex:45-76,139-155` |
| Attest actor columns already have identity foreign keys | `lib/tightbeam/assignments.ex:79-105` |
| User socket auth and transcript replay are currently user/session-shaped | `lib/tightbeam/wire/socket.ex:289-390`; `lib/tightbeam/transcript.ex:360-389` |
| User post stamps a user origin; gateway maps `call.origin` to sender | `lib/tightbeam/wire/socket.ex:411-450`; `lib/tightbeam/gateway.ex:628-643` |
| Append plus turn enqueue already has one transaction seam | `lib/tightbeam/gateway.ex:1028-1045,1124-1160` |
| Current enqueue accepts `principal` separately from `origin` and persists an accepted lifecycle event in the append transaction | `lib/tightbeam/gateway.ex:1315-1331`; `lib/tightbeam/ledger.ex:134-160` at `7a70a2f` |
| Current durable lifecycle rows store a required `principal`; accepted-event detail admits `origin` and `authenticatedCaller` | `lib/tightbeam/turn_lifecycle.ex:19-30,33-59`; `lib/tightbeam/ledger.ex:134-159` at `7a70a2f` |
| Current ordinary transcript entries contain internal identity and execution fields that the visitor projection must not copy wholesale | `lib/tightbeam/transcript.ex:190-248` at `7a70a2f` |
| Current schema is stamped `coordination-fabric-v1-phase1-v5`, admits one predecessor, rebuilds and stamps atomically, and refuses unknown shapes | `lib/tightbeam/schema.ex:35-73,800-823,987-1011` |
| The Rust CLI has one shared base-directory resolver and hand-parsed closed commands/identity flags | `cli/src/base_dir.rs:1-35`; `cli/src/args.rs:1-24` |
| Model and harness mutation use closed typed validation and expected versioning | `lib/tightbeam/gateway.ex:4311-4551`; `lib/tightbeam/org.ex:554-598` |
| r5 agent anatomy comes from typed archetype and guidance seed material | `priv/seed/archetypes/exec.toml:1-21`; `priv/seed/guidance/directive-vocabulary.md:15-41`; `priv/seed/guidance/delegation-card.md:1-45` |

### 6.2 Durable rows

`VisitorActorEnvelopeV1` is the sole checked identity input to visitor policy,
authorization, audit, transcript projection, and post construction. Its
constructor accepts resolved database rows, not request identity fields. It
derives the closed visitor authority projection from the grant booleans and
cause. Compatibility origin, authorization facts, audit attribution, enqueue
principal, and accepted lifecycle detail are outputs of that value. A visitor
post passes `visitor:<principalId>` as both enqueue `origin` and `principal`;
the accepted lifecycle writer therefore stores that same value in
`turn_lifecycle_events.principal`, detail `origin`, and detail
`authenticatedCaller`. This is the visitor-local analogue of the one-source
actor rule reviewed in `art_a86b44c7`; no current-main code imports that
unlanded artifact.

The implementation shall add these tables with strict foreign keys and closed
state checks:

| Table | Required identity and purpose |
|---|---|
| `visitor_invitations` | Invitation id; broker user FK; exact target session FK; display labels; independent grants; canonical consent version/digest; derivation and digest key ids; keyed invitation credential digest; issue/expiry/state fields; immutable target and broker. State is `pending`, `accepted`, `expired`, or `target-retired`. |
| `visitor_principals` | Visitor principal id; originating invitation FK; display label; created time; lifecycle state `active`, `revoked`, `expired`, or `target-retired`; optional terminal time/reason. Identity and provenance fields are immutable. Acceptance inserts the row as `active`; only the closed lifecycle fields can later change. |
| `visitor_grants` | Grant id; principal, invitation, broker user, and exact target session FKs; `canRead`; `canPost`; active/terminal state and times. |
| `visitor_access_sessions` | Access-session id; grant/principal/invitation FKs; derivation and digest key ids; keyed access credential digest; credential version; issue/expiry/terminal fields. It has no FK to ordinary `sessions` as its own identity. |
| `visitor_acceptances` | Invitation FK; acceptance-key digest; request fingerprint; first operation id; consent version/digest; resulting ids; accepted time; unique `(invitationId, acceptanceKeyDigest)`. |
| `visitor_invitation_admission` | Exactly one row per invitation, created in the invitation-create transaction with its creation UTC minute and both counts zero; invitation FK and primary key; current UTC-minute start; admitted count in that minute from 0 through 60; lifetime admitted count from 0 through 1,000. No request, credential, address, or header field. |
| `visitor_principal_admission` | Exactly one row per visitor principal, created in the acceptance transaction with its creation UTC minute and both counts zero; principal FK and primary key; current UTC-minute start; admitted count in that minute from 0 through 60; lifetime admitted count from 0 through 50,000. All access sessions for the principal share this row. No request, credential, address, or header field. |
| `visitor_operations` | Context kind, scope id, cause, operation id, request fingerprint, replay policy `stored` or `single-use`, terminal outcome, public status, and canonical result projection without raw credentials or transcript content. Unique `(contextKind, scopeId, cause, operationId)`. Mutation results regenerate deterministic credentials from stored ids and key ids. |
| `visitor_audit` | Unique audit id; phase `attempted` or `terminal`; closed context kind `invitation-presentation`, `visitor-action`, `broker-action`, `invitation-rejected-operation`, or `visitor-rejected-operation`; terminal outcome; the fields required by that context kind; nullable operation id; nullable rejection id; optional request fingerprint; optional closed malformed route and shape classes; event time; optional closed denied capability and resource classes plus a non-secret resource id; no secret or content bytes. Well-formed contexts are unique on `(contextKind, scopeId, cause, operationId, phase)` and require operation id/fingerprint while forbidding rejection and malformed fields. Rejected-operation contexts are unique on `(contextKind, scopeId, cause, rejectionId, phase)`, require `operationId=NULL`, no fingerprint, and both malformed classes. Database checks reject a visitor action or visitor rejection without every resolved envelope provenance field, an invitation context with an actor id, or a broker action without its user actor. |
| `visitor_unknown_bearer_aggregates` | Exactly one updatable row for each closed class `invitation`, `read`, `post`, and `revoke`; current 60-second window start; saturating count; last-seen time; last closed cause. No bearer-derived key. |

Operation scope is closed. Broker operations use
`(broker-action, authenticatedUserId, cause, operationId)`. Invitation
operations use `(invitation-presentation, invitationId, cause, operationId)`.
Visitor operations use
`(visitor-action, visitorPrincipalId, cause, operationId)`. The access-session
id remains required provenance but does not widen the idempotency namespace.
`visitor-transcript-read` has replay policy `single-use`; every other listed
operation has replay policy `stored`. An invitation-read result can be stored
because its bounded summary is immutable and contains no credential. Stored
credential-bearing results contain ids and key ids only and regenerate the raw
credential at return time.

`visitor_audit` has one partial unique index on
`(contextKind, scopeId, cause, operationId, phase)` where `operationId IS NOT
NULL AND rejectionId IS NULL`, and a second partial unique index on
`(contextKind, scopeId, cause, rejectionId, phase)` where `rejectionId IS NOT
NULL AND operationId IS NULL`. Rejection-id generation retries a uniqueness
collision inside the request transaction before inserting either audit phase;
it never turns that collision into a client operation identity.

A privileged-route presentation of a known `tbv_` credential creates a
server-generated operation id `vbd_` plus 32 lowercase hexadecimal characters.
Its fingerprint covers the versioned canonical semantic request, including the
route class, requested verb class, and any syntactically valid non-secret
resource kind/id, but excluding credentials and raw prose. In one transaction
it inserts attempted and denied `visitor-authority-denied` audit rows with the
resolved principal, access session, broker, closed denied capability class
`user`, `operator`, `agent`, `device`, `session`, or `websocket`, and bounded
resource kind/id when valid. It stores no proposed decision, prompt, arbitrary
request parameters, or credential bytes and invokes no policy or domain
handler.

Request processing on an invitation or visitor route resolves the bearer class
and known row before it validates the JSON shape. It next locks that scope's
admission row. When the stored minute differs from the current UTC-minute
start, admission replaces the minute, sets the minute count to one, and
increments the lifetime count. In the same minute it increments both counts
only when the minute count is below 60 and the lifetime count is below the
scope's closed cap. A missing admission row, invalid counter, or failed
admission commit is invariant corruption and returns HTTP `503` and exactly
`{"error":{"code":"visitor_admission_unavailable"}}`. At either cap it rolls
back without mutation and returns the route-class-specific I12A refusal. Only
an admitted request continues to shape validation. If its body is
invalid JSON, lacks `operationId`, has an invalid operation id, or otherwise
fails the closed request schema, the server generates one `vrej_` rejection id
and commits one attempted/denied pair in the corresponding stable
rejected-operation context under `invitation-invalid-request` or
`visitor-invalid-request`. Both rows keep `operationId=NULL`. The pair contains
only the resolved provenance, rejection id, route class, closed shape class,
and event times. The server does not infer an operation id from request bytes or
reuse a syntactically invalid value. It stores no request fingerprint, creates
no `visitor_operations` row, and invokes no policy or domain handler. Unknown
and wrong-class bearers still follow I13/I19 and never create identity audit or
touch an admission row.

For an admitted request, the admission increment and the I12 audit pair and
outcome share one database transaction. Any shape, audit, authorization,
projection, target, domain, or commit failure that prevents the required
terminal pair rolls back the admission increment with the other request
effects. A schema-invalid admitted request commits its denial pair and
admission together. No process crash can consume an admission without its
terminal pair or leave a pair without its admission.

All mutable state transitions use compare-and-set predicates in the same
transaction as their effects. Database check constraints enforce closed state,
phase, outcome, cause, and operation-class values. A grant check enforces
`canRead OR canPost`. The unknown-bearer count saturates at
`9_223_372_036_854_775_807`.

The terminal transition matrix is closed:

| Event | Invitation | Principal | Grant | Active access sessions |
|---|---|---|---|---|
| Accept | `pending -> accepted` | insert `active` | insert `active` | insert one `active` |
| Broker or self revoke | unchanged `accepted` | `active -> revoked` | `active -> revoked` | `active -> revoked` |
| Invitation expiry | `pending -> expired` | absent | absent | absent |
| Access expiry | unchanged `accepted` | `active -> expired` | `active -> expired` | `active -> expired` |
| Target retirement before accept | `pending -> target-retired` | absent | absent | absent |
| Target retirement after accept | unchanged `accepted` | `active -> target-retired` | `active -> target-retired` | `active -> target-retired` |

The first compare-and-set observer records the terminal time and reason. Later
observers return the stored terminal outcome without changing any row.

Accepted `visitor-post` terminal audit rows are the durable quota source. The
post transaction counts accepted rows for the exact grant in `(now - 60_000,
now]` under an index on `(grantId, cause, outcome, eventTime)`, applies the
limit, and inserts the accepted row before commit. It does not maintain a
separate eventually consistent quota counter.

The invitation summary is the canonical consent projection. Its exact JSON
shape is:

```json
{
  "brokerDisplayLabel": "Broker",
  "visitorDisplayLabel": "Visitor",
  "targetDisplayLabel": "Target",
  "canRead": true,
  "canPost": false,
  "consentText": "I accept visitor-only access to this Tightbeam session with the read and post capabilities shown. This does not grant user, agent, operator, or administrative authority.",
  "consentVersion": "visitor-consent-v1",
  "consentSha256": "64_lowercase_hex_characters",
  "issuedAt": 0,
  "invitationExpiresAt": 0
}
```

The three labels are JSON strings. For `visitor-consent-v1`, `consentText` is
exactly the UTF-8 string shown above, including punctuation. The capability
fields are booleans; `consentVersion` is exactly `visitor-consent-v1`;
`consentSha256` is 64 lowercase hexadecimal characters; and both times are
integer milliseconds. No key is optional or nullable. The summary contains no
target content, session key, user id, organization inventory, or access
credential.

The visitor transcript entry projection is exact and intentionally narrower
than the ordinary internal transcript projection:

```json
{
  "seq": 1,
  "at": 0,
  "role": "user",
  "content": "exact durable message content",
  "author": {"kind": "visitor", "visitorPrincipalId": "vis_exact"}
}
```

`seq` is the positive durable message sequence; `at` is an integer millisecond
timestamp; `role` is exactly `user` or `assistant`; and `content` is a JSON
string. `author` is exactly either
`{"kind":"visitor","visitorPrincipalId":"<exact id from the closed visitor origin>"}`
or `{"kind":"tightbeam"}`. The visitor form is used only for a parsed closed
visitor origin and preserves its exact principal id. Every user, agent,
process, remedy, session, or internal origin maps to the identifier-free
`tightbeam` form. An unknown origin refuses the complete read before content or
an accepted audit row is returned. Attachments, sender, reply ids, turn ids,
model, effort, context, harness, assignment id, job ref, wake class, delivery
rule, user id, session key, and internal prompt metadata are absent.

### 6.3 Credential-key custody

The sole MVP key store is
`<TIGHTBEAM_BASE_DIR>/secrets/visitor-keyring-v1.json`. It is a regular file,
not a symlink, owned by the gateway OS account with mode `0600`; its `secrets`
directory has mode `0700`. Its closed JSON shape is:

```json
{
  "schema": "visitor-keyring-v1",
  "activeDerivationKeyId": "vdk_exact",
  "activeDigestKeyId": "vgk_exact",
  "keys": {
    "vdk_exact": {"purpose": "credential-derivation", "bytesBase64": "..."},
    "vgk_exact": {"purpose": "credential-digest", "bytesBase64": "..."}
  }
}
```

Each key id is globally unique in the file. Each decoded key is exactly 32
bytes. The active ids and key bytes must be distinct and have the named
purposes. Provisioning uses the following no-replace publication protocol in
the `secrets` directory before the visitor migration:

1. Open or create regular mode-`0600`
   `.visitor-keyring-v1.init.lock` without following a symlink and take an
   exclusive OS advisory lock. The lock is released automatically on process
   death. A concurrent initializer that cannot take it immediately returns
   `visitor_keyring_init_busy` and changes no file.
2. While holding the lock, remove only stale regular mode-`0600` files owned by
   the gateway account whose names begin `.visitor-keyring-v1.json.tmp.`. A
   matching symlink, wrong owner, wrong mode, or nonregular entry causes
   `visitor_keyring_init_unsafe_temp` and no removal. If the final keyring
   exists after cleanup, return `visitor_keyring_exists` without replacing or
   rewriting it.
3. Create one random-suffix same-directory temporary file with
   create-new/no-follow semantics and mode `0600`. Write the complete JSON,
   flush it, `fsync` it, close it, reopen it without following symlinks, and
   validate its exact bytes and mode.
4. Publish by a same-filesystem hard-link operation from the temporary inode to
   `visitor-keyring-v1.json`. Link creation is atomic and fails when the final
   name exists; no precheck can authorize replacement. On link success, open
   the final name without following symlinks and verify that its device/inode,
   length, SHA-256, owner, mode, schema, and key ids equal the validated
   temporary file. Then `fsync` the directory, unlink the temporary name, and
   `fsync` the directory again before reporting success. A verification failure
   returns `visitor_keyring_publish_verification_failed`, reports no ids, never
   overwrites or unlinks the final name, and removes only the caller's safe
   temporary name.
5. If link creation loses with final-name-exists, open the race winner without
   following symlinks and validate its regular-file type, owner, mode, complete
   JSON schema, distinct key purposes, lengths, and ids. Remove the caller's
   safe temporary name and `fsync` the directory in both the valid and invalid
   winner cases. A valid winner returns `visitor_keyring_exists`; an invalid
   winner returns `visitor_keyring_race_winner_invalid`. The loser never prints
   either its own ids or the winner's ids and never modifies the winner.

If the platform or filesystem cannot provide the exclusive lock,
same-filesystem no-replace link, file `fsync`, and directory `fsync`, the
command returns `visitor_keyring_init_unsupported`, deletes its safe temporary
file, and publishes no target. A crash before link creation leaves no target;
the next initializer removes the safe stale temporary file and starts with new
keys. A crash after link creation can leave both names, but both name the same
fully written and synced inode; the next initializer removes the safe temporary
name, validates the final target as the race winner, and refuses to replace it.
Cleanup identifies an orphan only by the fixed temporary prefix plus
regular-file/no-follow, gateway owner, and mode `0600`, and only while the
initializer holds the exclusive lock; it never removes a final keyring or an
unsafe matching entry. The command prints the final path and key ids only after
successful winner verification and the second directory `fsync`. This spec adds no remote
key-management or rotation verb. Every invitation and access-session row stores
both key ids used for it.

The gateway loads and locks the keyring before it attempts migration or admits
a visitor route. Missing file, wrong ownership or mode, symlink, malformed
JSON, duplicate id, wrong purpose, wrong key length, equal active keys, or a
database row referencing an absent key causes boot refusal
`visitor_keyring_unavailable`. The refusal includes only the missing key id or
validation class, never key bytes or credential material. Once the stamped
visitor schema contains any credential row, all referenced keys remain in the
file for the lifetime of that database. Backup and restore must treat the
database plus this file as one unit; a restore missing either half refuses at
boot. Process restart reloads the same bytes and therefore preserves credential
verification and deterministic lost-response recovery.

### 6.4 Migration and compatibility law

The new schema stamp remains exactly `visitor-principal-v3-v1`. Its one direct
predecessor is exactly `coordination-fabric-v1-phase1-v21`, the schema at
allocated Tightbeam main `f4b68f078d3767cede71572aa88c4516372867cf`.
This predecessor preserves the intervening schema rather than reconstructing
the historical v5 shape. The target stays unchanged because the visitor
principal contract does not change; no v22 rung or visitor fields/tables are
added by this refresh. Authority for this bounded amendment is `dr_44be05e3`;
the amendment requires independent review before implementation resumes.

Existing boot compatibility for `coordination-fabric-v1-phase1-v19` and
`coordination-fabric-v1-phase1-v20` remains: the existing migrations first
advance those shapes through v20 to v21, with their existing validation and
transaction boundaries. Only then may the visitor migration begin. Neither
v19 nor v20 is a direct visitor predecessor. Failure in that existing chain
prevents entry to the visitor migration. No unstamped or other stamped shape,
including v5, can enter the visitor migration. This amendment does not add a
boot path for a shape the allocated source already refuses.

Before creating visitor rows or advertising visitor support, one
`foreign_key_rebuild` transaction shall verify the predecessor stamp, preflight
the keyring and attribution rows, rebuild the affected existing tables, create
the visitor tables and indexes, validate every foreign key/check, and replace
the predecessor stamp with the new stamp. Validation requires exactly one
invitation-admission row per invitation, exactly one principal-admission row
per visitor principal, and counters inside the closed I12A bounds. It adds
these identity backstops:

- `sessions.ownerUserId -> users(userId)`;
- `work_items.ownerUserId -> users(userId)`;
- `work_items.createdByUser -> users(userId)`;
- `work_items.createdBySession -> sessions(sessionKey)`;
- `assignments.openedByUser -> users(userId)`;
- `assignments.openedBySession -> sessions(sessionKey)`;
- `assignments.closedByUser -> users(userId)`;
- `assignments.closedBySession -> sessions(sessionKey)`;
- `assignment_reopenings.priorClosedByUser -> users(userId)`; and
- `assignment_reopenings.priorClosedBySession -> sessions(sessionKey)`.

The preflight produces a typed operator report with a count for every listed
column and the exact primary keys of offending rows. The report must not include
credentials or message content. If any count is nonzero, the migration returns
`identity_backstop_orphans`, creates no visitor table, rebuilds no existing
table, changes the stamp, advertises no feature, and requires a separately
authorized repair. A keyring failure returns `visitor_keyring_unavailable`
before the database transaction. Any DDL, validation, or stamp failure rolls
back the complete transaction to the predecessor stamp and schema.

Here rollback means rollback of the visitor transaction to v21, preserving
the v21 rows, columns, indexes, triggers, foreign keys, checks, principal-duty
provenance, and artifact-digest invariants, except for the ten expressly listed
identity backstops when the visitor transaction succeeds. It does not undo
already committed v19-to-v20 or v20-to-v21 migrations, restore a v5 database,
restore keyring files, or undo changes outside that transaction. A refusal
before entry to the visitor transaction likewise leaves any already committed
pre-visitor migration intact. There is no reverse migration after a successful
visitor commit; downgrade remains a refusal, not a data-restoration operation.

A database already stamped `visitor-principal-v3-v1` is validated and never
rebuilt again. A new binary accepts that stamp, its direct v21 predecessor,
and v19/v20 only through the existing boot chain described above. An
old binary at the allocated v21 source baseline sees `visitor-principal-v3-v1` as unknown and
refuses at boot; downgrade never rewrites or drops visitor bytes. Existing user,
agent, device, CLI, and socket requests retain their pre-visitor request and
response bytes when served by the new binary. Visitor discovery appears only
after the new stamp, all constraints, and the keyring validate.

### 6.5 Versioned wire, authentication, and CLI

The external HTTP surface is rooted at `/visitor/v1`. `GET /visitor/v1`
requires no credential. It returns HTTP `200` and exactly
`{"authority":"visitor-only-no-user-delegation","feature":"visitor-principal-v3","operations":["invitation-accept","invitation-read","post","self-revoke","transcript-read"],"wireVersion":1}`
only while the complete feature gate is live; otherwise it returns the I19
unavailable response. The operation list is ascending bytewise lexical order
over the exact lowercase ASCII operation names and advertises product capability,
not a particular grant; the invitation summary carries that grant's read/post
booleans. No field is added to the existing `/version` response.

Invitation and visitor routes require exactly one
`Authorization: Bearer <credential>` header. Prefix `tbi_` is admitted only to
invitation routes; prefix `tbv_` is admitted only to visitor routes. Org, CLI,
device, session, invitation, and visitor credential classes are mutually
exclusive. On `/visitor/v1`, a credential in the wrong class or route receives
the I19 response before a domain lookup. On every pre-existing HTTP or websocket
authority seam, any `tbi_` or `tbv_` value receives that seam's existing
`auth_failed` response and never reaches policy or a handler. A known `tbv_`
value first passes I12A and, when admitted, records the I21 boundary-denial pair
before refusal. At its admission cap it returns the same `auth_failed` bytes
without an audit pair or other mutation. An unknown value and every `tbi_`
value disclose and record no visitor identity.

The JSON request and success projection are closed:

| Method and path | Authentication | Exact request keys | HTTP 200 `result` keys |
|---|---|---|---|
| `POST /agent/dispatch`, verb `visitor-invitation-create` | Existing CLI token plus checked `asUser`; owner/admin target authorization | `targetSessionKey`, `visitorDisplayLabel`, `canRead`, `canPost`, `expiresAt`, `operationId` | `invitationId`, `invitationCredential`, `summary` |
| `POST /visitor/v1/invitation/read` | `tbi_` | `operationId` | `invitationId`, `summary` |
| `POST /visitor/v1/invitation/accept` | `tbi_` | `operationId`, `acceptanceKey`, `consentVersion`, `consentSha256` | `visitorPrincipalId`, `grantId`, `visitorAccessSessionId`, `visitorCredential`, `expiresAt`, `authorityBoundary`, `canRead`, `canPost` |
| `POST /visitor/v1/transcript/read` | `tbv_` | `operationId`, `afterSeq`, `limit` | `entries`, `nextAfterSeq` |
| `POST /visitor/v1/post` | `tbv_` | `operationId`, `body` | `messageId`, `turnId` |
| `POST /visitor/v1/revoke` | `tbv_` | `operationId` | `status` equal to `revoked` |
| `POST /agent/dispatch`, verb `visitor-broker-revoke` | Existing CLI token plus checked `asUser`; owner/admin target authorization | `grantId`, `operationId` | `status` equal to `revoked` |

Every `summary` value is the exact 10-key object in 6.2. Acceptance `expiresAt`
is the integer millisecond expiry of the created visitor access session; it is
not `summary.invitationExpiresAt`. `authorityBoundary` is a string, grant flags
are booleans, and every returned id is a string.

For transcript read, `entries` is a JSON array of the exact entry objects in
6.2. The server selects durable target messages with `seq > afterSeq`, orders
them by `seq` ascending, and returns at most `limit`. `nextAfterSeq` is the
highest returned `seq` when the array is nonempty. For an empty page it is
exactly the request's `afterSeq`. It is always a nonnegative integer, never
`null`, and never advances past an entry omitted from the response. `messageId`
and `turnId` are strings. Revoke `status` is the string `revoked`. No success
object admits an unlisted key or a `null` value.

Every non-discovery operation success uses `{"result":{...}}`; discovery uses
the exact direct object above. The server rejects an unknown key or missing key
with HTTP `400` and exactly
`{"error":{"code":"visitor_invalid_request"}}`. A scoped operation-id or
acceptance-key fingerprint conflict uses HTTP `409` and exactly
`{"error":{"code":"visitor_operation_conflict"}}`. A duplicate transcript
read operation id uses HTTP `409` and exactly
`{"error":{"code":"visitor_read_retry_requires_new_operation"}}`. An
oversized body uses HTTP `413` and exactly
`{"error":{"code":"visitor_body_too_large"}}`. Post-quota refusal uses HTTP
`429` and exactly `{"error":{"code":"visitor_quota_exceeded"}}`. I12A
admission refusal uses HTTP `429` and exactly
`{"error":{"code":"visitor_rate_limited"}}`. No error includes a credential,
internal id, target fact, or `message` field.

Admission-row corruption or a failed admission commit uses HTTP `503` and
exactly `{"error":{"code":"visitor_admission_unavailable"}}`. It returns no
domain result and creates no partial admission, operation, rejection, audit,
target, or domain mutation.

Bearer classification and known-row resolution precede request-shape
validation on invitation and visitor routes. Therefore a known bearer with
invalid JSON, a missing or invalid `operationId`, or any other schema error
returns the same `visitor_invalid_request` body only after the malformed-request
audit pair in I12 commits. If that audit commit fails, the route returns HTTP
`503` and exactly `{"error":{"code":"visitor_audit_unavailable"}}`; it returns
no domain result and stores no partial audit pair. An unknown or wrong-class
bearer follows I13/I19 and creates no malformed-request audit.

If an internal transcript row has an unknown origin or cannot satisfy the exact
entry projection, transcript read returns HTTP `500` and exactly
`{"error":{"code":"visitor_projection_invalid"}}` after committing one
attempted/denied audit pair and before returning any entry. The error contains
no row, origin, content, or parser detail.

Every acceptance success sets `authorityBoundary` exactly to
`visitor-only-no-user-delegation` and returns the immutable grant booleans. No
visitor response advertises a user, operator, decision, targeting, release,
queue-triage, or lane-unsticking capability.

The server computes the request fingerprint from the closed semantic request
keys; clients do not send it. Every external request includes `operationId`.
An operation id is exactly `vop_` followed by 32 lowercase hexadecimal
characters. An acceptance key is 16 through 128 opaque bytes; file/stdin input
removes one optional trailing LF before hashing. Labels are valid UTF-8 from 1
through 200 bytes. `expiresAt` is an integer millisecond timestamp inside the
invitation lifetime bounds. `consentVersion` is the exact version in the
summary and `consentSha256` is 64 lowercase hexadecimal characters. `afterSeq`
is a nonnegative integer and `limit` is an integer from 1 through 200. No
external route accepts a target, actor, broker, presenter, origin, model,
harness, or operational parent.

Broker dispatch refusals use the existing dispatch error envelope. Failed
owner/admin authorization uses code `visitor_forbidden`; the pending limit uses
`visitor_pending_invitation_limit`; a missing `asUser` uses the existing typed
authentication refusal before visitor dispatch. These broker errors contain no
invitation or visitor credential.

The CLI adds these exact commands: `tightbeam visitor invite`,
`invitation-read`, `accept`, `transcript-read`, `post`, `revoke`, and
`broker-revoke`, plus local operator command `tightbeam visitor keyring-init`.
`keyring-init [--base-dir <path>]` writes two independently random 32-byte keys
and distinct ids through the exact locked, same-directory, atomic no-replace
publication protocol in 6.3. It never uses a replacing rename. It prints only
the path and key ids after durable publication and never sends key material to
the gateway.

Broker commands use the existing gateway discovery, CLI token, and `--as-user`
identity seam. `invite` requires `--as-user`, `--target-session`,
`--visitor-label`, at least one of `--can-read` or `--can-post`,
`--expires-at-ms`, and `--operation-id`. `broker-revoke` requires `--as-user`,
`--grant-id`, and `--operation-id`. External commands use
`--gateway <absolute-http-or-https-url>`; non-loopback HTTP is refused. They
require exactly one of `--credential-file <path>` or
`--credential-stdin`. A credential file must be a nonsymlink regular file owned
by the invoking user with mode `0600`. Credential stdin contains only the
credential plus one optional trailing newline. `accept` reads its acceptance
key from exactly one of `--acceptance-key-file <path>` or
`--acceptance-key-stdin`; credential and acceptance key cannot both claim
stdin. `invitation-read` and `revoke` also require `--operation-id`; `accept`
also requires `--operation-id`, `--consent-version`, and `--consent-sha256`;
`transcript-read` also requires `--operation-id`, `--after-seq`, and `--limit`.
`post` also requires `--operation-id` and reads the body from
`--body-file <path>` or `--body-stdin`; the credential cannot claim stdin when
the body does. External visitor commands reject `--as`, `--as-user`,
`--as-process`, `--session`, and every agent target/identity flag locally as an
invalid request. No command accepts raw secret bytes in argv or prints them to
stderr. Success JSON is the HTTP result object; the credential-bearing invite
and accept successes may print their credential to stdout. I19 maps to exit
`4`; invalid request to `2`; conflict to `5`; quota or admission limit to `6`;
transport failure or HTTP `500`/`503` visitor service failure to `7`; success
to `0`. Exit `7`
writes exactly `visitor service unavailable` for an HTTP `500`/`503` visitor
error and never writes the server's internal validation class.

## 7. Acceptance

Each case is deterministic and maps back to the named invariants.

**A1 — Checked current-main attribution (`I16`, `I17`, `I20`).**

Given one fixture with a missing referenced user in each listed legacy column,
when the migration runs, then it returns `identity_backstop_orphans`, reports
each offending primary key, leaves stamp
`coordination-fabric-v1-phase1-v21`, and leaves the schema byte-for-byte
unchanged. At every injected rebuild and validation failure, the same
predecessor schema and stamp remain. Given the repaired fixture and valid
keyring, when the migration runs twice, then both runs succeed, the stamp is
exactly `visitor-principal-v3-v1`, all listed foreign keys are active and
restrictive. Ordinary AU2 unknown-user reads and dispatch retain the existing
behavior established by `c09cf0693507226b3d5c8806c43666ef491b71cb`; this case
does not require a universal user-existence check. Visitor broker operations
still satisfy the checked-user and authorization requirements of section 6.5
and A15 at the boundary defined in I17. Their guarantees are not relaxed by
ordinary AU2 transport acceptance.

Run the same visitor-failure cases after existing v19 and v20 boot fixtures
reach v21. A failed visitor transaction retains their completed v21 state;
it does not restore their original v19/v20 stamp. A failure in an existing
boot migration obeys that migration's original rollback contract and never
starts the visitor transaction. Successful migration preserves every
intervening invariant described in section 6.4 and adds only the previously
specified visitor schema and ten identity backstops.

**A2 — External intermediary attribution (`I1`, `I2`, `I6`).**

Given user U brokers an invitation for external agent V to session S, when V
posts through access session P, then the message origin and audit actor are
`visitor:V`, the presenter is P, the broker is U, and the accepted lifecycle
row stores `principal=visitor:V`, `detail.origin=visitor:V`, and
`detail.authenticatedCaller=visitor:V`. No user-U, presenter-P, target, or
substrate action or permission is attributed to the post.

**A3 — One-target capability matrix (`I4`, `I5`, `I19`).**

Given three grants for the same fixture session with read/post values `10`,
`01`, and `11`, each with an active principal, a terminal `accepted` invitation,
and an active grant and access session, when each read and post is attempted,
then only the true capability succeeds. Authorization requires the active
principal and accepted terminal invitation; it never requires a nonterminal
invitation. Every false capability returns the same public unavailable shape
and reads or mutates no target content. An attempted target replacement at
invitation mutation or at the internal authorization seam refuses and leaves
the immutable target unchanged.

**A4 — Consent and lost-response retry (`I7`, `I8`, `I9`, `I12`).**

Given broker operation O creates an invitation but its response is lost, when
the gateway restarts and O retries with the identical fingerprint, then it
loads the same keyring and returns the byte-identical
`tbi_` credential and invitation id with one invitation and one audit pair. A
changed fingerprint refuses. Given that pending invitation and acceptance key
K, when acceptance commits but its response is lost and the gateway restarts,
then a retry with K, the original operation id, and the identical fingerprint
returns byte-identical `tbv_` credential and ids with one acceptance and one
audit pair. The same K and fingerprint under a new operation id returns the
same ids and credential, creates one pair for that operation, and creates no
identity row. A retry with K and a changed fingerprint conflicts. A new key
after acceptance returns unavailable. A database/log/argv scan finds no raw
invitation credential, raw access credential, or raw K. At every injected
acceptance-transaction failure, the invitation remains pending and no
principal, principal admission, grant, access session, or acceptance row
exists. On success, the invitation is terminal accepted, the fixed principal
admission row exists, and all three post-accept lifecycle rows are active in
the same commit.

**A5 — Atomic visitor post (`I2`, `I10`, `I12`).**

Given an active post grant, when the post transaction succeeds, then exactly one
visitor-origin prompt echo, queued turn, accepted lifecycle event, quota unit,
attempted audit, and accepted audit exist under the operation id. The lifecycle
principal and its `origin` and `authenticatedCaller` detail fields are the exact
visitor origin. At each injected transaction failure point, none of the echo,
turn, lifecycle, or quota effects exist and no partial accepted result exists.

**A6 — Audit-before-read (`I11`, `I12`).**

Given an active read grant, operation R, and transcript entries after cursor 40,
when read audit commits, then the response contains only the allowed target
entries using the exact 6.2 projection, ascending sequence order, and a
`nextAfterSeq` equal to the last returned sequence. In a separate fixture with
no durable row after cursor 40, the response is exactly `entries=[]` and
`nextAfterSeq=40`.
When audit commit is injected to fail, the response contains no transcript
content. Repeating R returns
`visitor_read_retry_requires_new_operation`, reads no target rows, and creates
no new audit. A fresh operation id with cursor 40 performs a new read.

**A7 — Replay-only proof (`I15`).**

Given an active visitor and newly appended target messages, when no explicit
transcript-read occurs, then the visitor receives no frame or notification.
When it reads from its last durable cursor, then it receives the messages in
sequence order through the exact safe entry projection and receives the
specified integer next cursor. After later messages append, repeating the same
cursor under a new operation id may include those later rows; the cursor is not
a frozen-page handle. A code and schema assertion
finds no visitor subscription, push claim, delivery acknowledgment, recovery
job, or live cursor row.

**A8 — Revocation/post race (`I12`, `I14`).**

Given one active grant, when revocation and post are committed in both possible
transaction orders, then the database contains either the complete post before
one terminal revocation or no post after the terminal revocation. No ordering
produces a partial post. Repeated revocation with the same operation id returns
the stored result and one audit pair. Self-revoke and authorized broker-revoke
change the active principal, grant, and every active access session to
`revoked`, leave the accepted invitation unchanged, and do not change immutable
principal identity or provenance.

**A9 — Expiry and target retirement (`I14`, `I19`).**

Given access expiry T, when authorization runs at T-1 ms it can succeed and at T
it refuses and terminalizes the active principal, grant, and access sessions as
`expired`.
Given a retired target, the first observer atomically records
`target-retired` on a pending invitation before acceptance or on the active
principal, grant, and access sessions after acceptance. Access expiry also
uses that same principal terminal transition. All later operations return the
same public unavailable shape without target content.

**A10 — Unknown-bearer bound (`I13`, `I19`).**

Given one million distinct random credentials distributed across the four
operation classes, when every credential fails resolution, then the database
contains exactly four aggregate rows, no visitor or audit rows for those
attempts, and no stored value derived from any bearer. Counts saturate without
overflow and a new 60-second window resets only its fixed class row.

**A11 — Quota and duplicate operation (`I10`, `I12`).**

Given an active grant with nine accepted posts in the preceding 60 seconds,
when one new operation id posts twice concurrently, then one post commits, both
callers receive its stored result, and the quota count becomes ten. A different
operation id in the same window refuses without a message, turn, or quota unit.

**A12 — No agent anatomy (`I18`).**

Given a visitor access session, when every ordinary agent/session lookup,
dispatch, tune, wake, assignment, and harness/model mutation surface receives
its id or credential, then each refuses with no effect. The visitor row has no
`operationalParent`, provider, model, harness, effort, context, host, role,
archetype, seed, or delegation-card field. Conversely, org, CLI, device,
session, invitation, and visitor credentials are each submitted to every wrong
authentication class; every pair refuses before a domain handler runs. Each
I12A-admitted known visitor-to-privileged-seam case records one
`visitor-authority-denied` pair with its exact principal and presenter. No
other wrong-class case creates visitor identity or audit rows.

**A13 — Origin round trip (`I1`, `I3`).**

Given visitor principal V, when `{:visitor, V}` serializes to an origin, passes
through append, transcript projection, lifecycle accepted-event projection, and
audit projection, and parses again, then every identity-bearing projection
preserves `visitor:V`; lifecycle `principal`, `origin`, and
`authenticatedCaller` all equal `visitor:V`; and the parser returns the same
closed value. The external transcript author is the exact visitor form for V,
while nonvisitor origins expose only `{"kind":"tightbeam"}`. Every unknown
origin prefix returns the exact `visitor_projection_invalid` result with no
entry content and one attempted/denied visitor audit pair.

**A14 — Compatibility and feature gate (`I15`, `I16`, `I20`).**

Given an old client and a new server after a clean migration, when ordinary user
and agent fixtures run, then their wire bytes and effects are unchanged. Given
an old server or incomplete migration, visitor feature discovery is absent and
visitor credentials are rejected. A downgrade preserves all attribution and
visitor rows byte-for-byte because the old binary refuses the unknown
`visitor-principal-v3-v1` stamp at boot and performs no DDL.

**A15 — Broker authority and pending limit (`I6`, `I12`, `I16`).**

Given a target owner, an authorized admin, an unrelated user, and a nonexistent
`asUser`, only the owner and authorized admin can create or broker-revoke for
the target. An authenticated unrelated user receives `visitor_forbidden`, one
broker-action attempted/denied audit pair, and no invitation/grant mutation. A
nonexistent `asUser` receives the typed authentication refusal before visitor
dispatch and creates no visitor audit. Given 19 pending invitations, two
concurrent creates by one broker produce exactly one new pending row and one
`visitor_pending_invitation_limit` refusal; expiry at the boundary removes an
invitation from the counted pending set in transaction order.

**A16 — Known-denial audit and public absence (`I5`, `I11`, `I12`, `I19`).**

For each known invitation or visitor credential, exercise wrong capability,
expiry, revocation, target retirement, missing target, and wrong target at the
internal authorization seam. Each call records exactly one attempted and one
denied audit row under its scoped operation key, reads or mutates no target
content, and returns exactly the I19 HTTP body and CLI result. An injected
denial-audit failure rolls back the denial and returns no target fact. For both
a known invitation bearer and a known visitor bearer with available I12A
admission, submit invalid JSON, missing `operationId`, invalid `operationId`,
missing required key, unknown key, and invalid value. Each request returns the
same invalid-request body, keeps
`operationId=NULL`, and creates one attempted/denied pair under a distinct
`vrej_` rejection id with the exact closed shape and route classes. The visitor
bearer pair scopes to its authenticated visitor principal; the invitation pair
scopes to its invitation and invents no principal. Each creates no operation
row, invokes no domain handler, and stores no raw body, malformed operation-id
value, or field value. Repeating the same malformed bytes creates a new
rejection id and no guessed idempotency relation. The same malformed requests
with unknown bearers create no visitor audit.

**A17 — Wire, discovery, and secret input (`I8`, `I16`, `I19`).**

Before complete schema/keyring validation, `GET /visitor/v1` returns the I19
response and every visitor route is absent. After validation it returns the
exact feature object with its five operation names in ascending bytewise lexical
order. Every listed route rejects an extra or missing JSON key. Golden JSON
fixtures prove the exact summary, acceptance expiry meaning, transcript entry
union, empty and nonempty cursor result, post result, and revoke result; a
fixture copied from the ordinary internal transcript fails because it contains
forbidden internal keys. CLI tests prove that credential and acceptance-key
bytes never occur in argv, stderr, logs, traces, or error JSON; a symlink,
wrong-owner, or non-`0600` credential file refuses locally before network I/O.

**A18 — Keyring restart, backup, and missing-key refusal (`I8`, `I9`, `I16`).**

Create invitation and access credentials, restart the gateway, and restore a
database/keyring pair; both credentials still authenticate and lost-response
retries remain byte-identical. Remove either referenced key, swap its purpose,
make the active keys equal, corrupt the file, or restore only one half; boot
refuses `visitor_keyring_unavailable`, admits no visitor route, and emits no key
or credential bytes. Run two initializers concurrently: one publishes one
fully valid inode and reports its ids; the other returns
`visitor_keyring_init_busy` or, after retry, `visitor_keyring_exists`; neither
replaces the target. The winner verifies final and temporary inode, length,
digest, owner, mode, schema, and ids before reporting success. A link loser
validates the winner, removes and syncs only its own temporary name, and prints
no ids. An invalid winner yields `visitor_keyring_race_winner_invalid` without
modifying it. Inject a crash before publication: no target exists, and the next
initializer removes only the safe stale temporary file and succeeds with new
keys. Inject a crash after link publication and before temporary-name cleanup:
the final target is complete and synced, the next initializer verifies it,
removes the safe alias, syncs the directory, and refuses to replace the final
target. An unsafe orphan-shaped symlink or wrong-owner/mode file is never
removed. On a filesystem without the required lock/link/fsync guarantees,
initialization returns `visitor_keyring_init_unsupported` with no target and no
key bytes in output.

**A19 — Scoped operation collisions (`I9`, `I11`, `I12`).**

Use identical operation-id bytes for two visitor principals and for two causes;
all four scoped operations commit independently with one audit pair each. Reuse
one scoped id with a changed fingerprint and receive one conflict with no
domain effect. Reuse one acceptance key under a new operation id with the same
fingerprint and receive the same deterministic result with one new audit pair
but no new identity row. Duplicate one transcript-read operation id and receive
the exact single-use conflict without content or new audit.

**A20 — Terminal transition closure (`I7`, `I14`, `I20`).**

Exercise acceptance, invitation expiry, access expiry, self-revoke,
broker-revoke, and target retirement before and after acceptance. Every row
matches the closed transition matrix, every compare-and-set winner records one
terminal time/reason, no terminal row reactivates, and no path changes or
deletes a principal identity/provenance field. Acceptance exposes no state in
which the invitation is accepted but the principal is absent/inactive, or the
principal is active while the invitation remains pending.

**A21 — Realized intermediary collision cannot recur (`I1`, `I6`, `I17`,
`I21`).**

Reproduce specimen `att_1a77f64a` with human broker Mike and two separately
invited external intermediaries V1/P1 and V2/P2. Submit opposite
`operator-rule` attempts for `dr_4edb91e6` and `dr_45999b0f` through their
visitor credentials within the same millisecond. Both attempts refuse before
decision lookup or mutation; neither arrival can win. The two denial audit
pairs identify V1/P1 and V2/P2 separately, retain Mike only as broker
provenance, carry distinct request fingerprints and event times, and contain no
`byUser=mike` attribution. Decision rows remain unchanged. The external CLI
rejects `--as-user mike`, discovery and acceptance advertise exactly
`visitor-only-no-user-delegation`, and a database/projection scan finds no
stored targeting/release or queue-triage/lane-unsticking grant derived from the
historical prose split.

**A22 — Known-scope admission and audit-growth bound (`I12`, `I12A`).**

Given one invitation scope and one visitor-principal scope at minute count 59,
run two concurrent requests for each scope in the same UTC minute, one
well-formed and one malformed. Exactly one request per scope advances both
counters to 60 and reaches I12; the other receives the route's exact admission
refusal and creates no operation, rejection, audit, target, or domain row.
Send 10,000 more requests in that minute. The admission rows remain unchanged,
no per-request row count grows, and no handler runs. At the next exact UTC
minute, one request resets the minute count to one and increments the lifetime
count once without inserting a window row. Repeat the concurrency fixture at
lifetime count 999 for the invitation and 49,999 for the visitor principal.
Exactly one request reaches I12 in each fixture; all later requests remain
row-neutral across minute rollover. Two access sessions for the visitor share
the same 50,000 counter. A known visitor credential on a privileged route also
shares it and retains that route's `auth_failed` response when refused. A
database assertion proves the invitation caused no more than 1,000 operation
rows and 2,000 audit rows and the visitor principal caused no more than 50,000
operation rows and 100,000 audit rows. An injected admission-commit failure
returns the exact `visitor_admission_unavailable` response and creates no
partial effect.

## 8. Open Questions

None. This amended text closes review `att_5efefdde` findings F1-F7 and is ready
to return to the independent review rail after also closing successor verdict
`att_f88643c7` findings F1-F6 and final-recovery verdict `att_9cefd0e7` finding
F7. Any review or build-time clarification shall amend this canonical file
first, produce a new cold digest, and bind the work item only after the cleared
bytes are committed and pushed.
