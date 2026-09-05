# REST vs CLI — the state-read adjudication (tb02)

Status: CANONICAL r2, 2026-08-21. r2 is the adopted three-plane authority
input for `rest-state-api-v1.md` canonical r4. Mike's 2026-08-25 ruling in
message `s_21b93fdd-5e62-4ed9-ac7e-923697463936` supersedes only r2's contrary
`asUser` query-parameter prohibition; canonical REST r4 owns that current
transport behavior. The read-plane, write-plane, and CLI-sugar rulings remain
unchanged.

r2 reconciled recon wi_9239a7f1's report
(NFS shared/specs/tightbeam/rest-state-api-recon.md; recon accepted the
three-plane ruling and its inventory corrections are adjudicated in).
Accepted from the recon: coordination-share and digest-members are pure
reads and move to the read plane (code-verified); REST homes for the
seven gateway read verbs the CLI does not surface (facts-read,
artifact-get, assignment-get, work-item-list, decision-request,
role-list, critical-state inspect); a paged /api/sessions split from the
small /api/org document; first-class bulk /api/attests, /api/wakes,
/api/turns (ATC's SQL is the demand evidence); doctor stays local (not a
state resource); canonical public projections with secrets structurally
excluded; notices carry resource+op with delete tombstones; keyset-only
pagination on immutable orders (the transcript precedent), whitelist
filters, no fields/sort/include/join params; and the then-current
bearer-credential rule with no `asUser` query parameter. The status paragraph
above marks that last clause's later, scoped supersession. Rejected: nothing
material. The recon's
"Formal REST contract" section (envelopes, pagination rules, filter
tables, resource routes, projection minima, migration order, acceptance
proofs) was adopted as the baseline for the REST spec, subject to the scoped
`asUser` supersession above. Spec-side folds landed as event-firehose-v1.md
r5. Adjudicated by tb02 per Mike's ruling
that recon output is input to my classification. Feeds
event-firehose-v1.md P5.

## Spec homing

The canonical CLI/query adjudication lives only in the `tightbeam-specs`
repository as `rest-vs-cli-adjudication.md` canonical r2. It is an authority
input, not a coupled custody companion for REST r4. Canonical
`rest-state-api-v1.md` owns current query routes, transport, authorization,
and wire behavior. A worktree, report, transcript, or artifact row is evidence,
not canonical custody.

## The decision rule

It is not a partition of functions into two buckets. It is THREE PLANES,
and the rule is one sentence per plane:

1. **REST is the read plane**: every state read a client could use to
   build or refresh a display model is a typed, paginated, filterable
   GET resource — and every read lives here EXACTLY ONCE.
2. **Verbs are the write plane**: every state change goes through
   dispatch verbs (today's `/agent/dispatch` + CLI), because writes carry
   org semantics — identity, attribution, rails, law. REST never mutates.
3. **The CLI is sugar, not surface**: it wraps common reads and writes
   for agents and humans at a terminal. It carries NO data of its own —
   every CLI read is a thin wrapper over a REST GET underneath, and a
   read too niche for sugar is REST-only. The CLI never grows
   SQL-shaped flag languages; flexible querying is REST's job.

Corollaries that make it unambiguous for any future function: if it
returns rows and changes nothing → REST, with a CLI wrapper only if
agents use it routinely. If it changes anything → verb, with a CLI
wrapper if common. Nothing is ever CLI-only data; nothing on REST ever
mutates.

## Disposition — CLI read verbs → REST resources

Every row: the CLI verb KEEPS its wrapper (it is common agent
convenience) and the data moves to/lands on a REST resource.

| CLI verb | REST resource | Note |
|---|---|---|
| list | GET /api/org (sessions, archetypes, hosts, catalog) | consolidates /api/streams, /api/trackable-sessions, /api/org-options |
| toplines, topline | GET /api/toplines, /api/toplines/:id | computed projection is still a read answered from rows |
| work-item-list / -get | GET /api/work-items, /api/work-items/:id | routes exist on main; regularize shape |
| work-item-trace | GET /api/work-items/:id/trace | composed resource |
| assignments / assignment-get | GET /api/assignments, /api/assignments/:id | today's /api/work reconciles into this naming |
| attests | GET /api/assignments/:id/attests | |
| transcript | GET /api/sessions/:key/messages?before&after&limit | REST R5/R5d owns opaque cursor and history-boundary semantics; the CLI wrapper owns no data contract |
| inspect | GET /api/sessions/:key | |
| artifacts / artifact-get | GET /api/artifacts, /api/artifacts/:id (+ existing /download/:asset_id) | |
| decision-requests / decision-request | GET /api/decision-requests, /:id | |
| facts-read | GET /api/facts | scoped as today |
| identity-status | GET /api/identity | |
| role-list | GET /api/roles | |
| kungfu-list | GET /api/kungfu | |
| host-env-list | GET /api/host-env | |
| harness-processes | GET /api/harness-processes | |
| (new, spec §10) read markers | GET /api/read-markers/:scopeKey | write stays a verb per RM2 |

## Disposition — writes stay verbs (CLI + /agent/dispatch)

wake, condition, cancel, critical, tune, attest, assign, dispatch,
revoke-assignment, reopen-assignment, work-item-create/-update/-icebox/
-reopen/-close/-fail, rule, effort-rule, waive, revoke-waiver, withdraw,
ask, answer, spawn, retire, role-create/-bind/-rm, approve-device/
deny-device/revoke-device, promote-user, add-user, config (writes),
register-host, host-env-set/-unset, update-clients,
identity-edit/-relearn/-repoint/-apply, learn, unlearn, kungfu-scaffold,
onboard, artifact-record, attend. All mutate or carry org semantics; none
becomes a REST endpoint. (r2 correction: coordination-share and
digest-members were listed here in r1 and are in fact pure reads — moved
to the read plane: GET /api/sessions/:key/coordination-share and
GET /api/wakes/:wakeId/digest-members.)

## Disposition — existing HTTP routes

| Route | Ruling |
|---|---|
| GET /version, /harnesses | keep — meta/health reads of the read plane |
| GET /api/streams, /api/trackable-sessions, /api/org-options | fold into GET /api/org (and /api/sessions/:key) |
| GET /api/session-status | fold into GET /api/sessions/:key |
| GET /api/work, /api/work/:id | rename into /api/assignments naming |
| GET /api/work-items, /:id | keep — already the right shape's seed |
| GET /download/:asset_id | keep — artifact bytes read |
| POST /agent/dispatch | keep — THE write plane's door |
| POST /agent/tool-call-observed | keep — adapter-internal, not client surface |
| POST /api/streams, /api/session-control, /upload | write-shaped: route their semantics through the verb plane over time; interim they stand as named exceptions serving the chat client |
| GET /ws | the chat socket (unchanged); the firehose notice socket arrives per event-firehose-v1 |

## Boundary cases, ruled

- **toplines**: REST. Computed is still read; philosophy gate 9 (a status
  question answerable from rows is answered by rows) does not care which
  plane computes the projection. CLI wrapper stays because agents live in
  it.
- **transcript**: REST with before/after pagination; the chat client's
  model build is the canonical consumer (spec M4). The CLI wrapper stays for
  agents reading a colleague's conversation and passes REST's opaque cursors
  through unchanged. It does not retain the superseded message-id cursor or
  candidate/message projection.
- **work-item-trace**: REST composed resource; the CLI wrapper stays.
- **attend**: verb — it changes attention state. **coordination-share
  and digest-members**: r2 correction — pure reads (gateway.ex confirms
  "files nothing, rules nothing"), so read plane with CLI wrappers.
- **read markers**: split by plane exactly like everything else — GET on
  REST, set via verb (spec RM2), change notice on the ws (RM3).

## What this means for the CLI's future

The CLI stops being where new read features land. A new flexible read
(filter, join-shaped view, bulk fetch) is designed REST-first; the CLI
gains a wrapper only when a common agent task wants it in one line. The
CLI's identity: make common things easy, carry the org's write verbs,
never re-create SQL.

## Reconciliation state

- Recon wi_9239a7f1: DONE and reconciled (this r2). Report:
  NFS shared/specs/tightbeam/rest-state-api-recon.md. Verdict filed on
  asg_9a1b4764.
- Kin: wi_9fdc0c07 (client buildability) supplies the demand side;
  event-firehose-v1.md r5 (P5, V3-V5, registry, A6) carries the
  spec-side folds of this ruling.
