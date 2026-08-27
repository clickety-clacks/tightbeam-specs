# Decision-request expecter preference — v1

Status: SPEC-READY, TARGETLESS

Authority: Mike's assignment on `wi_c94444e6-3107-40c5-a577-2fe251a03661`:
"expecter is the preferred responder, not an authorization gate; any agent may
answer a decision request, with normal agent judgment determining whether it
should." This contract is derived from Tightbeam `main` commit
`8eeccbd6dfd221fe9d105783459637fb7a17ea83`.

## Goal

An authenticated agent session that knows one expecter-bearing decision
request's exact id can inspect and respond to that request. The request's
expecter stays the preferred notification or escalation target, as its kind
defines. The expecter does not grant or withhold an agent session's response
standing.

This change deletes three deterministic judgment gates: the asked-principal
gate on `answer`, the asked-principal gate on `return`, and the current-expecter
gate on `effort-rule`. A mind decides whether it should respond. The substrate
verifies the request kind and state, commits one terminal result, and records
the actual responder. This is wisdom 6: the substrate routes and verifies;
minds decide.

The smallest useful result is one response contract for the two request kinds
that carry an expecter: `agent` and `effort`. Deleting the gates wins over
adding delegation, proxy, or approval machinery because the requested standing
needs no intermediate state. Accepting the existing refusal loses because it
is the defect this work item changes.

## Non-Goals

- This contract does not change `statute` request visibility, `rule`, `waive`,
  authorization consumption, or owner/admin authority. Statute rows carry no
  expecter and can grant spendable authorization.
- This contract does not make decision-request lists visible to more
  principals.
- This contract does not give a human user, process, org-token role call, or
  anonymous caller new response standing.
- This contract does not grant `wake`, `revoke-assignment`, `dispatch`,
  `retire`, or another ordinary power to a responder.
- This contract does not decide whether an agent should respond. Guidance can
  tell an agent to inspect context and use judgment; the substrate does not
  infer competence, ownership, urgency, or correctness.
- This contract does not change request creation, expecter selection,
  notification targets, effort deadlines, rung rotation, answer consumption,
  returned-question replacement, or assignment liveness policy.
- This contract does not select an implementation branch, release line,
  deployment target, or release vehicle. `wi_c94444e6` stays untargeted until
  Mike sets a target.

## Terms

- **Decision request**: one durable `decision_requests` row.
- **Expecter-bearing request**: a request whose `kind` is `agent` or `effort`
  and whose row names an expected session or user in `expecterSessionKey` or
  `expecterUserId` under that kind's existing schema constraint.
- **Expecter**: the row's preferred notification or escalation target,
  according to request kind. The expecter fields describe routing preference
  and provenance.
- **Agent session principal**: the canonical session identity authenticated by
  the gateway, represented in audit data as `session:<sessionKey>`. A role
  alias or caller-supplied origin that preserves session authentication does
  not change that principal. `--as-user <id>` changes the authenticated
  principal to `user:<id>`; it does not preserve the session principal.
- **Existing human responder**: the user principal already authorized by the
  pinned source: the stamped `expecterUserId` for an `agent` request or the
  current `expecterUserId` for an `effort` request.
- **Response**: `answer` or `return` on an `agent` request, or `continue` or
  `dismiss` through `effort-rule` on an `effort` request.
- **Normalized response payload**: trimmed answer text, trimmed return reason,
  or the exact closed-vocabulary effort action `continue` or `dismiss`.
- **Actual responder**: the authenticated principal whose compare-and-set
  first changes the request from `open` to its terminal response state.
- **Exact-id access**: direct access using the complete canonical `dr_...` id.
  It is distinct from discovering rows through `decision-requests`.
- **List discovery**: selecting the caller-visible request roster through
  `decision-requests`, with or without a status filter.
- **Ordinary power**: an action outside the response verbs, including `wake`,
  `revoke-assignment`, `dispatch`, and `retire`. Its own handler decides its
  authorization.

## Assumptions

1. Commit `8eeccbd6dfd221fe9d105783459637fb7a17ea83` is the sole source pin for
   design and implementation planning.
2. The pinned schema already stores `answeredBy`, `answeredAt`, `returnedBy`,
   `returnedAt`, `ruledBy`, and `ruledAt`. This contract needs no new database
   column or schema-shape migration.
3. The pinned `answer_open`, `return_open`, and `effort_rule_in_txn` paths use
   an `open`-scoped compare-and-set. The agent paths commit the terminal row,
   lifecycle event, and asker notification in one transaction. The effort path
   commits the ruling, generation effect, and deadline-wake disposition in one
   transaction. It emits no ruling lifecycle event. The stored `ruledBy` and
   `ruledAt` fields plus the existing trace form the audit floor.
4. The pinned `decision-request` gateway verb is an exact-id read. The Rust CLI
   does not expose it, although the operating manual and CLI help already tell
   agents to use it.
5. The pinned list predicate limits `agent` rows to the asker, asked principal,
   and asker's accountable owner; limits `effort` rows to the current expecter;
   and applies separate statute visibility. This contract preserves that list
   predicate.
6. Request ids are references, not secrets. Authentication, request kind, and
   access mode form the security boundary. Prefix scanning is not an access
   mode.

## Invariants

**INV-01 — Preference is not agent authorization.** For an `agent` or `effort`
request, the response handler derives an authenticated session caller's
standing from its session principal and the request kind. It does not compare
that session with either expecter field.

**INV-02 — Principal boundary.** An authenticated agent session may respond to
an open expecter-bearing request when it supplies the complete request id and
the response verb matches the request kind. Existing human responders retain
their pinned-source standing. A session invocation attributed with `--as-user
<id>` is a user principal for standing and audit and follows the existing human
responder boundary. Other user principals, process principals, org-token role
calls without a session principal, and anonymous calls gain no standing.

**INV-03 — Statute isolation.** The exact-id affordance and response-standing
change apply to `agent` and `effort` rows. A `statute` row continues to use its
owner/admin visibility and ruling path. An agent session that lacks existing
statute visibility receives the same `not_found` result for a statute id as for
an absent id.

**INV-04 — Exact-id access is not discovery.** An authenticated agent session
may fetch one `agent` or `effort` row by its complete canonical id. The shared
`decision-request --request` grammar in `cli-surface-v1.md` rejects a missing,
blank, or non-complete value locally before dispatch. An unknown complete id or
a non-visible statute id returns `not_found`. The direct read returns the
existing full request projection so the agent can judge the question, context,
current state, expecter, and prior terminal actor before it acts.

**INV-05 — List discovery stays byte-compatible.** `decision-requests` uses the
pinned list visibility predicates and projections. A bystander session does not
discover an agent question or effort request merely because that session could
respond after receiving the exact id through another channel.

**INV-06 — One terminal winner.** `answer`, `return`, `withdraw`, and another
terminal mutation of one agent request compete on `kind='agent' AND
status='open'`. `continue`, `dismiss`, and supersession compete for one terminal
effort outcome on the request's existing transaction predicates. A deadline
rotation may commit before a terminal effort outcome; a stale deadline fire
loses its wake-id compare-and-set. A losing response observes the committed row
and applies INV-07.

**INV-07 — Payload-and-principal idempotency.** A response retry by the actual
responder with the same verb and normalized response payload returns the
committed row, exits successfully, and writes no second event, notification,
wake disposition, or generation effect. A different principal, different
terminal verb, or different payload receives `not_open` after a terminal
winner. The stored actual responder does not change on a retry. Existing
withdrawal retry semantics stay outside this change.

**INV-08 — Actual responder is canonical and durable.** The winning transaction
writes the canonical authenticated principal and timestamp to the response
fields. An agent answer or return emits its existing lifecycle event with the
same canonical actor. An effort ruling writes `ruledBy` and `ruledAt`; those
stored fields plus the existing trace form the audit floor. The effort path
emits no ruling lifecycle event.
A role alias, caller-supplied origin, current expecter, or request owner cannot
substitute for the actual responder. The answer/return notice to the asker names
that actor.

**INV-09 — Expecter mechanics continue until disposition.** Request creation
and effort-rung rotation continue to set the expecter, arm notification and
deadline wakes, and escalate by the existing policy. A non-expecter response
uses the same terminal transaction as an expecter response, including current
wake cancellation or disposition. No retarget occurs solely because a
non-expecter inspected the row.

**INV-10 — Ordinary powers remain separate.** Response standing does not enter
the authorization predicate for `wake`, `revoke-assignment`, `dispatch`, or
`retire`. The effort prompt's ordinary-power menu remains a presentation for
the current expecter and reflects that expecter's handler-derived powers. A
direct reader treats that menu as expecter context, not as authority granted to
the reader.

**INV-11 — Return keeps its meaning.** `return` remains a terminal statement
that the responder lacks enough information. It requires a non-blank reason,
keeps the original question immutable, leaves the row in `returned`, notifies
the asker, and requires the asker to file a new request if it still needs an
answer. The expanded agent standing does not turn return into delegation,
reassignment, withdrawal, or reopening.

**INV-12 — Guidance assigns judgment to minds.** Shipped human-readable agent
guidance says the expecter is preferred, another agent may respond when it has
the exact id and enough context, and response standing is not an instruction to
respond. Guidance does not define a deterministic competence or ownership
test.

## Architecture

### Access and mutation contract

The gateway classifies exact-read access before it reveals request state:

| Request kind | Agent-session exact read | Agent-session response | List discovery | Human response |
| --- | --- | --- | --- | --- |
| `agent` | allowed with complete id | `answer` or `return` | unchanged | existing stamped expecter user only |
| `effort` | allowed with complete id | `continue` or `dismiss` | unchanged | existing current expecter user only |
| `statute` | existing visibility only | no change | unchanged | existing owner/admin ruling only |

The response sequence is deterministic around one inference decision:

1. The agent decides whether to inspect or respond.
2. The gateway authenticates the canonical principal and resolves the complete
   id without prefix expansion.
3. An exact read checks direct visibility before it returns the row. A response
   handler applies the kind-specific principal and error contract below; it
   does not reuse the list predicate.
4. One existing mutation seam performs the open-state compare-and-set, audit
   write, and response side effects atomically.
5. A lost race is classified by the committed row under INV-07.

### CLI and wire contract

- Add `tightbeam decision-request --request <decisionRequestId>` to the Rust
  CLI's enumerated surface. It sends wire verb `decision-request` with
  `params.request`. It has no target flag. `agent` and `effort` are existing
  consumers of the shared grammar in `cli-surface-v1.md`: it accepts exactly
  one non-blank complete `dr_...` value and rejects a missing, blank, or
  non-complete value, positional id, target flag, or duplicate request flag
  locally before dispatch.
- A successful exact read, answer, return, or effort ruling returns HTTP 200
  with the existing `{ "result": ... }` envelope. The CLI prints the result
  and exits 0.
- For a complete id that resolves no visible row, `not_found` returns HTTP 404.
  The CLI prints `not_found: decision request not found` and exits nonzero.
- `not_authorized` returns HTTP 403 for a principal class that retains an
  authorization boundary, including a non-expecter human attempting an effort
  ruling. The CLI prints the typed code and message and exits nonzero.
- `answer` or `return` against a non-`agent` id returns HTTP 404 `not_found`.
  `effort-rule` against an agent-visible non-`effort` id returns HTTP 400
  `invalid`. A non-visible statute id returns HTTP 404 before either mismatch
  can reveal its kind.
- `invalid` or `invalid_action` returns HTTP 400 for invalid visible-kind input
  or an action outside the verb's closed vocabulary. The CLI prints the typed
  code and message and exits nonzero.
- `not_open` returns HTTP 400 for a terminal conflict that is not the exact
  retry defined by INV-07. The CLI prints the typed code and message and exits
  nonzero.
- Error envelopes use the existing
  `{ "error": { "code": <code>, "message": <message> } }` shape. No error
  includes a hidden statute's kind, status, owner, or existence.

### Compatibility and migration

- Database migration: none. Existing responder and timestamp columns are the
  storage seam.
- Wire migration: additive exact-id session visibility; response verbs keep
  their request and success shapes. Existing clients need no new field.
- CLI migration: additive `decision-request`; `decision-requests`, `answer`,
  `return`, and `effort-rule` keep their arguments. Amend `cli-surface-v1.md`
  before exposing the command.
- Behavioral compatibility: calls from the existing asked session, stamped
  expecter user, current effort expecter, and statute owner/admin retain their
  successful paths. The intentional delta is that another authenticated agent
  session can directly read and respond to a known `agent` or `effort` row.
- Historical rows: no rewrite. Existing open expecter-bearing rows acquire the
  new session response standing at runtime. Terminal rows preserve their stored
  actors and outcomes.

### Implementation seam map

| Requirement | Source seam at `8eeccbd6` | Required change | Acceptance |
| --- | --- | --- | --- |
| INV-01, INV-02, INV-03 | `lib/tightbeam/escalation.ex` `decision_reader?/2`; `lib/tightbeam/effort_checkin.ex` `authorized?/2` | Separate direct response standing from expecter/user standing; share canonical principal rendering | A-01, A-03, A-04, A-07, A-08, A-15 |
| INV-04, INV-05 | `Escalation.get/4`, `visibility/2`, `agent_visibility/3`; `Gateway` handlers for `decision-request` and `decision-requests` | Add direct-read visibility for complete ids without changing list visibility | A-06, A-14, A-15 |
| INV-06, INV-07, INV-08, INV-11 | `answer_open/4`, `return_open/4`, `EffortCheckin.rule_in_txn/7`, `Escalation.effort_rule_in_txn/5` | Classify CAS loss against actor, verb, and normalized payload; stamp the authenticated principal, not `call.origin` | A-01, A-03, A-04, A-09, A-10, A-11, A-12 |
| INV-09, INV-10 | `EffortCheckin.deadline_in_txn`, `rule_in_txn`, `menu_in_txn/3`; `Escalation.effort_update_generation_in_txn/4` | Preserve deadline race and ordinary-power handlers; add negative authorization proofs | A-02, A-04, A-05, A-10, A-13 |
| CLI/wire | `cli/src/args.rs`, `cli/src/dispatch.rs`, `lib/tightbeam/gateway.ex`, `lib/tightbeam/wire/router.ex` | Expose exact-id read; preserve response envelopes and typed status mapping | A-06, A-07, A-08, A-14, A-15 |
| INV-12 | `priv/guidance/operating-manual.md`, CLI help, source moduledocs; specs `coordination-fabric-v1.md` §7 and `cli-surface-v1.md` | Replace exclusive-expecter wording with preference, direct-reference, and agent-judgment wording | A-16 |
| Proofs | `test/conformance_test.exs`, `test/cli_integration_test.exs`, `test/effort_checkin_test.exs`, `test/router_test.exs` | Add deterministic standing, privacy, race, idempotency, audit, and real-CLI cases | A-17 |

## Acceptance

Each acceptance case runs against a fresh database and names the authenticated
principal explicitly.

**A-01 — Non-expecter answer.** Given Alice asks session Bob question `dr_A`
and session Carol receives the complete id and question through a separate
agent channel, when Carol runs `answer` with non-blank text, then `dr_A` becomes
`answered`, `answeredBy` is Carol's canonical session principal, one answered
event and one asker notification commit, and Bob remains the stored expecter.

**A-02 — Normal judgment is outside the substrate.** Given Carol knows `dr_A`,
when Carol performs no response, then Tightbeam writes no response, delegation,
or competence row on Carol's behalf and the agent question's existing
expecter-notification delivery continues.

**A-03 — Non-expecter return.** Given an open agent question and a non-expecter
session with its complete id, when that session returns it with a non-blank
reason, then the row becomes `returned`, stores that session in `returnedBy`,
notifies the asker once with the immutable question and reason, and the default
open list excludes the row.

**A-04 — Non-expecter effort ruling.** Given an open effort request expected by
session Parent, when session Observer uses the complete id to choose `continue`,
then the request becomes `ruled`, `decision` is `continue`, `ruledBy` is
Observer's canonical session principal, and the existing continue effects and
deadline-wake disposition occur once.

**A-05 — Dismiss keeps snapshot safety.** Given an open effort request and a
non-expecter session preparing `dismiss`, when the holder's effort state changes
before the transaction, then the call returns `stale_effort_snapshot` and writes
no ruling. When the caller retries from the fresh state, the normal dismiss path
applies.

**A-06 — Exact read, narrow list.** Given a bystander session and one open agent
question plus one open effort request, when the session lists open decision
requests, then neither row appears through the bystander branch. When the
session fetches either complete id through `decision-request`, then the matching
row appears. A shortened id fails locally with no wire request. An unknown
complete id and a non-visible statute id each return the same 404 `not_found`
envelope.

**A-07 — Human compatibility.** Given the stamped user expecter for an agent or
effort request, when that user performs its existing response, then the call
succeeds and records `user:<id>`. A session invocation using `--as-user <id>`
uses that same user principal for standing, idempotency, and audit. Given a
different user with the same complete id, when it attempts `answer` or `return`
on an agent request, then it receives `not_found`; when it attempts
`effort-rule`, then it receives `not_authorized`. No row changes.

**A-08 — Statute authority.** Given an open statute request and a bystander
agent session with its complete id, when the agent reads or responds through an
expecter-bearing path, then it receives the hidden-id `not_found` result and the
statute row remains open. Given the authorized owner/admin rules it, then the
existing ruling and consumption path remains byte-compatible.

**A-09 — Agent terminal race.** Given one open agent request, when distinct
sessions concurrently submit answer and return while the asker submits
withdraw, then one open-state compare-and-set wins. The row contains the
winner's terminal state and canonical actor, and the database contains one
matching lifecycle event plus at most one response notification. Each loser
receives `not_open`.

**A-10 — Effort race.** Given one open effort request whose deadline fire races
with `continue` and `dismiss` from distinct sessions, when the transactions are
released in each deterministic ordering, then either one ruling wins and the
deadline path no-ops against the terminal row, or rotation wins first and one
later ruling can still win without an expecter comparison. One ruling actor,
one terminal ruling, and one set of generation effects remain. The effort
ruling emits no lifecycle event.

**A-11 — Idempotent retries.** Given a committed answer, return, continue, or
dismiss, when the stored actual responder repeats the same verb and normalized
payload, then the call exits 0 with the committed row and row/event/wake counts
do not change. When another principal repeats the same payload or the winner
changes the payload, then the call returns `not_open` and counts do not change.

**A-12 — Session-preserving aliases do not replace the responder.** Given a
session calls through a role alias or caller-supplied origin while authentication
remains session-scoped, when it wins a response, then the row and each applicable
lifecycle event, trace, and asker notification name
`session:<authenticatedSessionKey>`, not the alias, role, expecter, owner, or
supplied origin. A call attributed with `--as-user <id>` follows A-07 instead.

**A-13 — Ordinary powers do not hitchhike.** Given a non-expecter session can
read and rule an effort request but its principal cannot revoke, dispatch, or
retire under those handlers, when it attempts each ordinary power, then each
handler keeps its existing refusal and the response-standing predicate is not
consulted. The session can still answer or rule the known request.

**A-14 — Real CLI and wire.** Given the built Rust CLI and a real gateway, when
an authenticated agent runs `decision-request`, `answer`, `return`, and
`effort-rule` in their success and refusal cases, then captured HTTP status,
whole JSON envelope, CLI exit status, and rendered typed error match the CLI
and wire contract above. Parser tests prove the exact-id command accepts one
non-blank complete `--request` and rejects missing, blank, or non-complete
values, target flags, positional ids, and duplicate request flags locally with
no wire request. Gateway tests prove an unknown complete id returns `not_found`
without prefix resolution. On a `terminal-operator-decision-parity-v1.md`
A-27a REST-absent proof arm, these are gateway-wire captures only. They do not
claim REST-route or R4c envelope coverage.

**A-15 — Security falsification matrix.** Given complete ids for one `agent`,
one `effort`, and one `statute` request, when an authenticated bystander session,
an unrelated user, a process principal, an org-token role call without a
session principal, and an unauthenticated caller each try exact read and each
response verb, then only the bystander session gains direct read and response
standing for the `agent` and `effort` rows. Existing expecter users keep only
their existing standing. The statute row follows existing visibility and
owner/admin ruling. Hidden and absent rows produce the same envelope within
each caller and verb class. No refused call changes a request, event, wake, or
effort generation.

**A-16 — Guidance projection.** Given the candidate source and specs revisions,
when a verifier reads `tightbeam help`, the served operating manual,
`coordination-fabric-v1.md` §7, and `cli-surface-v1.md`, then each relevant
surface says the expecter is preferred, a session with the complete id may
respond, and response standing is not an instruction to respond. None of those
surfaces says an agent response requires the asked principal or current
expecter. The guidance names no competence, ownership, or urgency algorithm.

**A-17 — Compatibility gate.** Given the unmodified source pin and the candidate
implementation, when the implementation lane runs the applicable baseline and
candidate gates from `.github/workflows/ci.yml`, then both runs are green. The
candidate additionally runs deterministic focused checks for A-01 through A-16
and the real CLI smoke for A-14.

## Open Questions

None. The implementation target is intentionally unset and does not block spec
review or implementation planning. Mike must name the target before a producer
changes source.
