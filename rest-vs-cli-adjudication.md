# REST vs CLI — the state-read adjudication (tb02, draft r1)

Status: DRAFT r1, 2026-08-21, adjudicated by tb02 per Mike's ruling that
the classification is the orchestrator's call and recon output is input
("you are smarter at looking at a pool of functions and classifying
them"). Pending reconciliation with recon wi_9239a7f1's report
(recon:rest-state-api, running); its inventory may add rows to the tables
below but the decision rule stands unless Mike overrules. Feeds
event-firehose-v1.md P5.

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
| transcript | GET /api/sessions/:key/messages?before&after&limit | pagination precedent from transcript.ex |
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
deny-device/revoke-device, promote-user, add-user, config, register-host,
host-env-set/-unset, update-clients, identity-edit/-relearn/-repoint/
-apply, learn, unlearn, kungfu-scaffold, onboard, artifact-record,
attend, coordination-share, digest-members. All mutate or carry org
semantics; none becomes a REST endpoint.

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
  model build is the canonical consumer (spec M4). CLI wrapper stays for
  agents reading a colleague's conversation.
- **work-item-trace**: REST composed resource; the CLI wrapper stays.
- **attend / coordination-share / digest-members**: verbs — they change
  attention/membership state, they are not reads.
- **read markers**: split by plane exactly like everything else — GET on
  REST, set via verb (spec RM2), change notice on the ws (RM3).

## What this means for the CLI's future

The CLI stops being where new read features land. A new flexible read
(filter, join-shaped view, bulk fetch) is designed REST-first; the CLI
gains a wrapper only when a common agent task wants it in one line. The
CLI's identity: make common things easy, carry the org's write verbs,
never re-create SQL.

## Reconciliation state

- Recon wi_9239a7f1 (running): its full inventory reconciles against
  these tables; disagreements surface here as amendments, and Mike
  adjudicates anything I change my mind on.
- Kin: wi_9fdc0c07 (client buildability) supplies the demand side;
  event-firehose-v1.md r4.2 (P5, M-recipe, RM) is the consumer of this
  ruling.
