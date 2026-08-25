# Visitor principal v3 — current-main contract

Status: SPEC-READY FOR ONE INDEPENDENT REVIEW; not implementation authority;
the work item remains untargeted and unbound until that review clears this exact
content.

Authority and identity:

- Work item: `wi_4ee303fa-12ed-4747-bce0-fc48024f4d53`.
- Spec continuation assignment:
  `asg_3ff49b50-3856-4388-8d4e-255a7d450d95`.
- Source baseline: Tightbeam main
  `8eeccbd6dfd221fe9d105783459637fb7a17ea83`, independently verified green.
- Canonical path: `visitor-principal-v3.md` in `tightbeam-specs`.
- Historical `art_d824eab5` and archived `art_765e7a53` are evidence only.
  This file supersedes their v1 and v2 designs after review clears this file.
- Reviewed `art_a86b44c7` is evidence only. Its closed `ActorContext` design is
  absent from the source baseline and this canonical repository.
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

The implementation shall serve transcript history through durable cursor replay.
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
`visitor-post`, and `visitor-self-revoke`. A later adapter to a landed general
actor context shall preserve every field and shall not replace `actorId` with
`brokerId` or `presenterId`.

### Invitation presentation

`InvitationPresentationV1` is the pre-principal context for a known invitation
credential. It contains schema, invitation id, broker user id, exact target
session, cause, operation id, and request fingerprint. Its closed cause set is
`invitation-read`, `invitation-accept`, and `invitation-decline`. It contains no
actor id or visitor access-session id. A successful acceptance terminal can
add the resulting visitor principal, grant, and access-session ids without
rewriting the attempted context.

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

The closed terminal reasons are `declined`, `revoked`, `expired`, and
`target-retired`. A terminal invitation, grant, or access session never becomes
active again.

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
9. Transcript ordering and cursor semantics reuse the existing durable session
   transcript sequence. The visitor surface neither invents a second sequence
   nor reads live frames.

## 5. Invariants

**I1 — Exact effective actor.** Every accepted or denied operation authenticated
by a known visitor access session records `actorKind=visitor` and the exact
visitor principal id. It never records the broker, access session, target
owner, or target agent as the effective actor. Invitation presentation records
no effective actor. Broker actions record their authenticated user actor.

**I2 — Separate provenance.** Every audit record for an operation authenticated
by a known visitor access session stores the exact visitor principal, visitor
access session, broker user, cause, target session, invitation, grant, and
operation ids from `VisitorActorEnvelopeV1`.

**I3 — Closed origin.** The origin parser, serializer, transcript projection,
message sender projection, and audit projection accept and preserve the closed
visitor origin. No string fallback can turn an unknown origin into a visitor.

**I4 — One exact target.** Authorization joins the active access session, active
grant, active visitor principal, nonterminal invitation, and exact target
session in one database read inside the operation transaction. It does not
accept a client-supplied replacement target.

**I5 — Independent least privilege.** Read requires `canRead=true`. Post
requires `canPost=true`. Either denial is indistinguishable from an unavailable
target and performs no target read or mutation.

**I6 — Broker is provenance, not delegation.** A broker can create or revoke a
grant only through existing owner/admin authorization. The visitor cannot use
the broker's user permissions. An outside agent presenting the visitor
credential remains the visitor principal.

**I7 — Consent proof.** Acceptance requires an affirmative decision over the
exact canonical consent bytes. The acceptance transaction stores the consent
version and SHA-256 digest before activating the principal, grant, and access
session.

**I8 — Secret handling.** Raw invitation and access credentials never enter a
durable row, log, error, trace, audit payload, artifact, or response other than
the credential-bearing creation response and deterministic acceptance success
responses. Stored credential values are
`HMAC-SHA-256(credentialDigestKey[keyId], credentialBytes)` with an explicit key
id and credential version.

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
operation id or acceptance key with a different fingerprint refuses. A
different acceptance key after terminal acceptance returns the generic
unavailable result.

**I10 — Transactional post.** One accepted visitor post atomically commits one
visitor-origin prompt echo, one turn enqueue, one consumed quota unit, and the
attempted-plus-accepted audit pair. Any failure commits none of those effects
except a terminal denied audit pair when the credential resolved to a known
visitor context.

**I11 — Read-before-return evidence.** A successful transcript read commits its
attempted-plus-accepted audit pair before returning content. If that audit
commit fails, it returns no content.

**I12 — Known operations are paired.** Every known invitation, visitor
access-session, and broker-authenticated operation records exactly one
attempted audit row and exactly one terminal `accepted` or `denied` row under a
unique operation id in the same transaction as its frozen outcome. Retrying the
same operation id and fingerprint returns the frozen result without duplicating
either row.

**I13 — Unknown bearers are bounded.** A credential that resolves to no
invitation or access session creates no visitor principal, audit, credential
digest, token fingerprint, IP address, header capture, or request row. It only
updates one fixed aggregate row for its closed operation class.

**I14 — Revocation and expiry are act-time facts.** Every read and post checks
terminal and expiry state in its transaction. Revocation terminalizes the
grant and all active access sessions atomically. A concurrent post either
commits completely before revocation or refuses completely after revocation.

**I15 — Replay only.** No visitor operation registers a socket, subscription,
push consumer, delivery cursor, claim, acknowledgment, or recovery job. The
only visitor content surface is explicit durable cursor replay.

**I16 — Identity backstops precede availability.** Visitor availability remains
disabled until the migration has added and validated the identity foreign keys
listed in Architecture. An orphan preflight refuses the complete migration;
it never performs a partial rebuild or creates a placeholder row.

**I17 — Checked `asUser`.** Every `agent_identity/3` path carrying `asUser`
looks up that exact user before a domain handler runs. A session-scoped
`asUser` also proves that the session owner user exists. Missing rows return a
typed authentication refusal and create no domain effect.

**I18 — Agent anatomy does not leak.** A visitor access session cannot satisfy
an ordinary session foreign key and cannot acquire `operationalParent`, typed
model/harness state, or r5 seed/delegation anatomy. A future visitor-agent
product requires a separate spec.

**I19 — Indistinguishable absence.** Unknown credential, wrong target,
unauthorized capability, revoked state, expired state, retired target, and a
missing target produce the same public status and response shape.

**I20 — No identity deletion cascade.** New foreign keys use restrictive
identity deletion. Deleting a user or ordinary session cannot erase or orphan
historical attribution, visitor provenance, consent, or audit.

## 6. Architecture

### 6.1 Current-main seams

The implementation shall be checked against these source facts at
`8eeccbd6dfd221fe9d105783459637fb7a17ea83`:

| Fact | Source citation |
|---|---|
| Agent dispatch authenticates first, then builds identity, and carries separate origin and principal | `lib/tightbeam/wire/router.ex:129-146`; `lib/tightbeam/dispatch.ex:37-53,73-81` |
| Organization and session `asUser` construction does not prove a user row | `lib/tightbeam/wire/router.ex:466-560` |
| Typed user target lookup already demonstrates the required existence check | `lib/tightbeam/wire/router.ex:648-651` |
| Origin is a closed user/agent/process/remedy type with no visitor | `lib/tightbeam/origin.ex:1-35` |
| Ordinary sessions require `operationalParent` but `ownerUserId` lacks its identity backstop | `lib/tightbeam/org.ex:63-91` |
| Work-item user/session actor columns lack identity foreign keys | `lib/tightbeam/work_items.ex:34-53` |
| Assignment opener/closer and reopening snapshot actor columns lack identity foreign keys | `lib/tightbeam/assignments.ex:45-76,139-155` |
| Attest actor columns already have identity foreign keys | `lib/tightbeam/assignments.ex:79-105` |
| User socket auth and transcript replay are currently user/session-shaped | `lib/tightbeam/wire/socket.ex:289-390`; `lib/tightbeam/transcript.ex:360-389` |
| User post stamps a user origin; gateway maps `call.origin` to sender | `lib/tightbeam/wire/socket.ex:411-450`; `lib/tightbeam/gateway.ex:628-643` |
| Append plus turn enqueue already has one transaction seam | `lib/tightbeam/gateway.ex:1028-1045,1124-1160` |
| Model and harness mutation use closed typed validation and expected versioning | `lib/tightbeam/gateway.ex:4311-4551`; `lib/tightbeam/org.ex:554-598` |
| r5 agent anatomy comes from typed archetype and guidance seed material | `priv/seed/archetypes/exec.toml:1-21`; `priv/seed/guidance/directive-vocabulary.md:15-41`; `priv/seed/guidance/delegation-card.md:1-45` |

### 6.2 Durable rows

The implementation shall add these tables with strict foreign keys and closed
state checks:

| Table | Required identity and purpose |
|---|---|
| `visitor_invitations` | Invitation id; broker user FK; exact target session FK; display labels; independent grants; canonical consent version/digest; keyed invitation credential digest; issue/expiry/terminal fields; immutable target and broker. |
| `visitor_principals` | Visitor principal id; originating invitation FK; display label; created time; terminal reason/time. |
| `visitor_grants` | Grant id; principal, invitation, broker user, and exact target session FKs; `canRead`; `canPost`; active/terminal state and times. |
| `visitor_access_sessions` | Access-session id; grant/principal/invitation FKs; keyed access credential digest; credential version; issue/expiry/terminal fields. It has no FK to ordinary `sessions` as its own identity. |
| `visitor_acceptances` | Invitation FK; acceptance-key digest; request fingerprint; consent version/digest; resulting ids; accepted time; unique `(invitationId, acceptanceKeyDigest)`. |
| `visitor_audit` | Unique audit id and `(operationId, phase)`; phase `attempted` or `terminal`; closed context kind `invitation-presentation`, `visitor-action`, or `broker-action`; terminal outcome; the fields required by that context kind; request fingerprint; event time; no secret or content bytes. Database checks reject a visitor action without every envelope field, an invitation presentation with an actor id, or a broker action without its user actor. |
| `visitor_unknown_bearer_aggregates` | Exactly one updatable row for each closed class `invitation`, `read`, `post`, and `revoke`; current 60-second window start; saturating count; last-seen time; last closed cause. No bearer-derived key. |

All mutable state transitions use compare-and-set predicates in the same
transaction as their effects. Database check constraints enforce closed state,
phase, outcome, cause, and operation-class values. A grant check enforces
`canRead OR canPost`. The unknown-bearer count saturates at
`9_223_372_036_854_775_807`.

Accepted `visitor-post` terminal audit rows are the durable quota source. The
post transaction counts accepted rows for the exact grant in `(now - 60_000,
now]` under an index on `(grantId, cause, outcome, eventTime)`, applies the
limit, and inserts the accepted row before commit. It does not maintain a
separate eventually consistent quota counter.

The invitation summary is the canonical consent projection. It contains only
the broker display label, visitor display label, target display label,
capability booleans, consent text and version, consent SHA-256 digest, and
issue/expiry times. It contains no target content, session key, user id,
organization inventory, or access credential.

### 6.3 Migration and compatibility law

Before creating visitor rows or advertising visitor support, one transaction
shall preflight and then add these existing identity backstops:

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
table, changes no feature advertisement, and requires a separately authorized
repair.

On a clean preflight, the schema change is atomic and idempotent. Restrictive
foreign keys remain enabled after a code downgrade. Additive visitor tables are
preserved, not dropped, by downgrade. Old binaries ignore the tables and do not
accept visitor credentials. Existing user, agent, device, CLI, and socket
contracts retain their wire shape. New binaries advertise the closed feature
`visitor-principal-v3` only after the complete schema is validated.

### 6.4 Operations

The versioned visitor surface has these operations:

1. `invitation-create`: owner/admin user authorization, operation id, and
   request fingerprint; immutable one-session target and proposed grant;
   returns the raw invitation credential once.
2. `invitation-read`: invitation credential, operation id, and request
   fingerprint; returns only the bounded canonical summary.
3. `invitation-accept` or `invitation-decline`: invitation credential,
   operation id, acceptance key, request fingerprint, and affirmative consent
   digest for accept. Accept atomically creates/activates the principal, grant,
   access session, acceptance, and audit rows. Decline terminalizes the
   invitation.
4. `visitor-transcript-read`: access credential plus durable `afterSeq` and page
   limit; returns only target transcript entries allowed by the existing
   transcript projection and a next cursor.
5. `visitor-post`: access credential, operation id, request fingerprint, and
   body; invokes the existing append-plus-turn transaction with visitor origin.
6. `visitor-self-revoke`: access credential and operation id; terminalizes its
   grant and all access sessions.
7. `broker-revoke`: currently authorized broker/owner/admin user and operation
   id; terminalizes the selected grant and all access sessions.

No operation accepts a client-authored actor, broker, presenter, origin, model,
harness, or operational parent. `invitation-create` accepts one target session
identifier from its authenticated user caller, proves the caller's authority,
looks up the target, and freezes it. No invitation-credential or visitor-
credential operation accepts a replacement target. The server constructs every
audit context from authenticated joined rows.

## 7. Acceptance

Each case is deterministic and maps back to the named invariants.

**A1 — Checked current-main attribution (`I16`, `I17`, `I20`).**

Given one fixture with a missing referenced user in each listed legacy column,
when the migration runs, then it returns `identity_backstop_orphans`, reports
each offending primary key, and leaves the schema byte-for-byte unchanged.
Given the repaired fixture, when the migration runs twice, then both runs
succeed, all listed foreign keys are active and restrictive, and an
`agent_identity/3` request naming a nonexistent `asUser` refuses before its
domain handler records any effect.

**A2 — External intermediary attribution (`I1`, `I2`, `I6`).**

Given user U brokers an invitation for external agent V to session S, when V
posts through access session P, then the message origin and audit actor are
`visitor:V`, the presenter is P, the broker is U, and no user-U action or
permission is attributed to the post.

**A3 — One-target capability matrix (`I4`, `I5`, `I19`).**

Given three grants for the same fixture session with read/post values `10`,
`01`, and `11`, when each read and post is attempted, then only the true
capability succeeds. Every false capability returns the same public unavailable
shape and reads or mutates no target content. An attempted target replacement
at invitation mutation or at the internal authorization seam refuses and leaves
the immutable target unchanged.

**A4 — Consent and lost-response retry (`I7`, `I8`, `I9`, `I12`).**

Given broker operation O creates an invitation but its response is lost, when O
retries with the identical fingerprint, then it receives the byte-identical
`tbi_` credential and invitation id with one invitation and one audit pair. A
changed fingerprint refuses. Given that pending invitation and acceptance key
K, when acceptance commits but its response is lost, then a retry with K and
the identical fingerprint returns byte-identical `tbv_` credential and ids with
one acceptance and one audit pair. A retry with K and a changed fingerprint
refuses. A new key after acceptance returns unavailable. A database/log scan
finds no raw invitation credential, raw access credential, or raw K.

**A5 — Atomic visitor post (`I2`, `I10`, `I12`).**

Given an active post grant, when the post transaction succeeds, then exactly one
visitor-origin prompt echo, queued turn, quota unit, attempted audit, and
accepted audit exist under the operation id. At each injected transaction
failure point, then none of the echo, turn, or quota effects exist and no
partial accepted result exists.

**A6 — Audit-before-read (`I11`, `I12`).**

Given an active read grant and transcript entries after cursor 40, when read
audit commits, then the response contains only the allowed target entries and a
monotone next cursor. When audit commit is injected to fail, then the response
contains no transcript content.

**A7 — Replay-only proof (`I15`).**

Given an active visitor and newly appended target messages, when no explicit
transcript-read occurs, then the visitor receives no frame or notification.
When it reads from its last durable cursor, then it receives the messages in
sequence order and receives a monotone next cursor. Repeating the same read
from the same cursor returns the same frozen page. A code and schema assertion
finds no visitor subscription, push claim, delivery acknowledgment, recovery
job, or live cursor row.

**A8 — Revocation/post race (`I12`, `I14`).**

Given one active grant, when revocation and post are committed in both possible
transaction orders, then the database contains either the complete post before
one terminal revocation or no post after the terminal revocation. No ordering
produces a partial post. Repeated revocation with the same operation id returns
the frozen result and one audit pair.

**A9 — Expiry and target retirement (`I14`, `I19`).**

Given access expiry T, when authorization runs at T-1 ms it can succeed and at T
it refuses. Given a retired target, the first observer atomically records the
single terminal reason `target-retired`; all later operations return the same
public unavailable shape without target content.

**A10 — Unknown-bearer bound (`I13`, `I19`).**

Given one million distinct random credentials distributed across the four
operation classes, when every credential fails resolution, then the database
contains exactly four aggregate rows, no visitor or audit rows for those
attempts, and no stored value derived from any bearer. Counts saturate without
overflow and a new 60-second window resets only its fixed class row.

**A11 — Quota and duplicate operation (`I10`, `I12`).**

Given an active grant with nine accepted posts in the preceding 60 seconds,
when one new operation id posts twice concurrently, then one post commits, both
callers receive its frozen result, and the quota count becomes ten. A different
operation id in the same window refuses without a message, turn, or quota unit.

**A12 — No agent anatomy (`I18`).**

Given a visitor access session, when every ordinary agent/session lookup,
dispatch, tune, wake, assignment, and harness/model mutation surface receives
its id or credential, then each refuses with no effect. The visitor row has no
`operationalParent`, provider, model, harness, effort, context, host, role,
archetype, seed, or delegation-card field.

**A13 — Origin round trip (`I1`, `I3`).**

Given visitor principal V, when `{:visitor, V}` serializes to an origin, passes
through append, transcript projection, and audit projection, and parses again,
then every projection preserves `visitor:V` and the parser returns the same
closed value. Every unknown origin prefix refuses.

**A14 — Compatibility and feature gate (`I15`, `I16`, `I20`).**

Given an old client and a new server after a clean migration, when ordinary user
and agent fixtures run, then their wire bytes and effects are unchanged. Given
an old server or incomplete migration, visitor feature discovery is absent and
visitor credentials are rejected. A downgrade preserves all attribution and
visitor rows and leaves the restrictive identity foreign keys active.

## 8. Open Questions

None. This exact text is ready for one independent adversarial review. Any
review or build-time clarification shall amend this canonical file first,
produce a new cold digest, and rebind the work item only after the cleared bytes
are committed and pushed.
