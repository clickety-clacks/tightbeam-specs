# Attest v1 — assignments and filings (implementation spec, r5)

Status: DRAFT r5 after four adversarial review rounds (joint r4
round: stale stranding sentence in §Resolution aligned; precedence
split honestly across router/handler layers). The PRINCIPAL
SEAM and the normative six-row identity story live in
session-tokens-v1.md r3 — this spec conforms to that table and never
restates it. Parent design:
supervision-v1.md §Prerequisites item 1. This spec is sole authority
for its scope; supervision-v1.md is background.

The primitive that turns "done" from speech into rows. An ASSIGNMENT is
an open obligation held by a session; an ATTEST is a structured filing
against one. Content-neutral, judgment-free — the substrate records and
relates; it never evaluates whether work is good (check tier, out of
scope).

DELIBERATE NARROWING vs parent design (F11): the parent sketched a
generic `attest {subject, kind, verdict}`. v1 scopes attests to the
assignment lifecycle only (progress/completion/surrender), with no
verdict field — verdict-carrying attests arrive with the check tier as
a spec revision, extending the attests table rather than redesigning
it. "Assignment owner" (the ladder's Main terminus in supervision) is
DERIVED, not stored: the owner of the HOLDER session's row at
escalation time.

BUILD ORDERING (F1): cut the worktree from main AFTER session-tokens-v1
merges (in addition to the already-merged statute-engine and cli-rust).
Holder authorization below is defined in terms of the caller's
TOKEN-RESOLVED SESSION — without per-session tokens it is unbuildable
as specified. If session-tokens machinery is absent from main, STOP and
report. Attest verbs run through Dispatch.dispatch/3, so statutes gate
them with zero extra work; CLI lands in cli/ (Rust).

## Goals

1. An open obligation is a queryable fact: `open_count(db, key) >= 1`
   is the supervision conjunct.
2. Completion/surrender/progress are filings — rows created by the
   holder session, never inferred from prose.
3. Every act is attributed via typed columns and flows through the
   existing verb machinery.

## Non-goals (later specs; do not build)

Reaction executor, prods, counters, ladder (supervision-impl). Verdict
evaluation / completion gating (check tier). Reference pinning (F11:
cut from v1 — a future revision may add a refs column; nothing here
depends on it). Automatic assignment creation from turns. Re-staffing.
Multi-user visibility partitioning (see §Authorization). No UI.

## Schema (follow existing migration/rebuild conventions)

COLUMN NAMING (cross-review catch): the repo's actual convention is
camelCase (sessionKey, createdAt, dueAt) — the names below are
normative as camelCase in DDL (holderKey, holderRole, holderFallback,
openedByUser, openedBySession, openedAt, closedAt, closedByUser,
closedBySession, closingAttestId, assignmentId, bySession); this
spec's prose may write them snake_case for readability, but the DDL
follows the repo.

assignments:
- id TEXT PK — `asg_` + the existing id-generation convention (F10).
- subject TEXT NOT NULL — free text, 1..2000 chars, non-blank after
  trim (refused otherwise, code "invalid_subject").
- holder_key TEXT NOT NULL REFERENCES sessions(sessionKey) (F8 — session rows
  are never deleted, retire is a state change, so the FK is sound).
- holder_role TEXT NULL, holder_fallback INTEGER NOT NULL DEFAULT 0
  CHECK(holder_fallback IN (0,1)) — role-assignment provenance only.
  CHECK: holder_role IS NULL implies holder_fallback = 0 (F8).
- opened_by_user TEXT NULL, opened_by_session TEXT NULL — EXACTLY ONE
  non-null (table CHECK) (F2/F10: typed opener columns, no origin
  strings in domain tables).
- opened_at INTEGER NOT NULL (ms).
- state TEXT NOT NULL CHECK(state IN ('open','closed')) DEFAULT 'open'.
- outcome TEXT NULL CHECK(outcome IN ('completed','surrendered','revoked')).
- closed_at INTEGER NULL; closed_by_user TEXT NULL; closed_by_session
  TEXT NULL; closing_attest_id TEXT NULL REFERENCES attests(id) (F8:
  the terminal attest is navigable, not folklore).
- Table CHECKs: state='open' implies outcome/closed_at/closed_by_*/
  closing_attest_id all NULL; state='closed' implies outcome AND
  closed_at non-null AND exactly one closed_by_* non-null;
  outcome IN ('completed','surrendered') implies closing_attest_id
  NOT NULL; outcome='revoked' implies closing_attest_id NULL.

attests:
- id TEXT PK — `att_` + existing convention (F10).
- assignment_id TEXT NOT NULL REFERENCES assignments(id).
- kind TEXT NOT NULL CHECK(kind IN ('progress','completion','surrender')).
- note TEXT NULL — ≤2000 chars after trim; optional for all kinds.
- by_session TEXT NOT NULL REFERENCES sessions(sessionKey) — attests are filed
  by sessions, ALWAYS (F2: no role required, no origin strings).
- ts INTEGER NOT NULL (ms).

CLOSED KIND VOCABULARY — exactly three. Adding a kind (e.g. the check
tier's verdict) is a spec revision, not a config knob.

Cross-table terminal consistency (closed-with-attest ⇔ the attest row
exists and matches) cannot be a SQLite CHECK; it is enforced solely by
the transactional seam in §Atomicity and proven by its tests (F8).

## Authorization (F1, F2, F3, F4)

The authorization identity is the Dispatch call's PRINCIPAL field,
defined and threaded by session-tokens-v1 r3 (four-way seam:
{:session, key} | {:user, id} | {:process, name} | nil). Declared
`as`/`asUser` grant these verbs nothing; roles are not consulted.
PRECEDENCE (r5, honest about the transport seam): target/reference
errors resolve in the ROUTER pre-Dispatch (the existing typed_target
mechanics — such refusals produce NO event rows, exactly like every
existing verb's target errors today; stated, not changed). Everything
else is checked IN THE HANDLER, inside Dispatch with its audit
semantics, in this order: (1) {:process, _} → "process_denied" — the
process power vocabulary stays closed; (2) nil → "principal_required",
message teaching session tokens; (3) verb authorization; (4) state
checks. So a malformed target refuses before principal checks (router
truth), and among handler checks process beats nil beats
authorization beats state — the tests pin both layers. "Any non-nil
principal" below always means SESSION OR USER principals only.

- `assign` — callers: any session or user principal.
- `attest` — callers: ONLY principal {:session, K} where K equals the
  assignment's holder_key ("not_holder" otherwise, message names the
  holder; a {:user, _} principal gets "not_holder" too — filings come
  from workers, users revoke instead). HONEST LIMITS (r4, corrected):
  a roleless non-Main holder is refused at origin derivation ONLY when
  it omits identity flags — it can always file by passing verified
  `--as-user <owner>` (origin user:<owner>, principal still
  {:session, holderKey}, per the tokens r3 seam table). So a late
  role rebind does NOT strand a holder. The one true stranding is
  RETIREMENT (retired tokens are 401): remedy is revocation by an
  authorized caller. The assignment never re-resolves or transfers.
- `revoke-assignment` — callers: principal {:user, U} where U is an
  ADMIN or equals opened_by_user, or principal {:session, S} where S
  equals opened_by_session (F3). Everything else: "not_authorized".
- `assignments` (query) — any non-nil principal; read-only.
  RULED for v1's single-operator reality: no visibility partitioning —
  every authorized caller sees all rows (F3; revisit under multi-user,
  as a statute-shaped filter, not code).

These rules are CONSTITUTIONAL in the narrow sense that they define
what the verbs ARE (an attest by a non-holder is not a stricter policy
choice — it is meaningless). Operator policy narrower than this (e.g.
only certain archetypes may assign) is statute material, not code (F3).

## Verbs (registered exactly like existing verbs)

Wire shape PINNED (F7/r2-5): typed TARGETS (sessionKey | role) at the
body top level, exactly like existing verbs; ALL operational arguments
under `params` — assign: {subject, idempotencyKey}; attest:
{assignmentId, kind, note}; revoke-assignment: {assignmentId};
assignments: {state}. Reuse the existing router typed_target helper
EXTENDED, not forked: for `assign`, exactly one of sessionKey | role;
userId present → teaching error "assignments are held by sessions;
target a sessionKey or role"; NO target → NEW refusal, code
"missing_target" (typed_target's nil-success today is not a refusal —
this code and its teaching message are additions this spec authorizes).
Retired rows: typed_target accepts them; assign REFUSES a retired
holder ("session_retired") — AND (r2-3) re-validates holder
state='active' INSIDE the handler transaction (§Atomicity), since
typed_target resolution happens pre-Dispatch and can go stale; the
role→key pin is resolution-time by design, only liveness is
re-checked.

- `assign` — subject (required), exactly one of sessionKey | role,
  idempotencyKey (optional — the EXISTING field name, not "key"; F10).
  Returns the full assignment object (§Shapes).
- `attest` — assignmentId, kind, note (optional). kind=progress
  appends a row, assignment stays open. completion/surrender append
  the row AND close the assignment atomically (§Atomicity). Unknown
  id → "unknown_assignment"; closed → "assignment_closed"; bad kind →
  "invalid_kind" (F10). Returns {assignment, attest}.
- `revoke-assignment` — assignmentId. Closes with outcome 'revoked',
  closing_attest_id NULL, no attest row. Already closed →
  "assignment_closed". Returns the assignment object.
- `assignments` — optional: at most one of sessionKey | role (filter
  by resolved holder; role resolves per §Resolution), state filter
  open|closed|all (default open). Ordered opened_at DESC, id DESC
  (deterministic tie-break, F10). No pagination in v1.

## Atomicity (F5, F6 — load-bearing; do not simplify)

Every mutation verb executes its ENTIRE read-check-write as one atomic
unit inside a single serialized DB call (the DB GenServer serializes
calls; one call = one transaction — never read in one call and write
in another):

- attest(completion|surrender): one transaction that (a) SELECTs the
  assignment FOR the state/holder checks, (b) INSERTs the attest row,
  (c) UPDATEs the assignment guarded `WHERE id = ? AND state = 'open'`
  and VERIFIES changes = 1 — zero changed rows aborts the transaction
  and returns "assignment_closed" (the attest row from (b) rolls back
  with it). Authorization (holder check) happens on the row read in
  (a), inside the same transaction.
- attest(progress) and revoke: same pattern (guarded UPDATE for
  revoke; guarded EXISTS-open check for progress).
- assign with idempotencyKey: the idempotency lookup, the assignment
  INSERT, and the idempotency-key INSERT all inside the SAME
  transaction (F6 — do NOT mirror the wake path's separate calls; that
  precedent is a known race). Key scope PINNED (r4): the existing
  table's PK is (ownerUserId, operation, idempotencyKey); the
  ownerUserId slot holds the PREFIXED principal id — "user:" <> id for
  {:user, U}, "session:" <> key for {:session, S} (r3's bare-id
  disjointness claim was FALSE: approve-device stores arbitrary user
  ids, so a user id can equal a session key; the prefix restores
  disjointness by construction); operation = "assign" — the existing
  operation CHECK permits only spawn/retire/wake, so this REQUIRES the
  fresh-DDL CHECK widened, the rename-rebuild migration for existing
  DBs (the wake precedent), and a pre-existing-DB migration test, all
  three pinned here; the result column (historically named for session
  keys) stores the assignment id — document both historical names at
  the call site. Replay returns the original assignment object.

## Resolution & typing

`assign --role R`: resolve NOW via Roles.resolve (bound-active, else
owner's Main per no-void); pin resolved key as holder_key; record
holder_role=R, holder_fallback. Unknown role → the wake path's error.
The holder NEVER re-resolves after creation: obligations are work in a
session's hands, not offices. Stranding (r5, aligned with
§Authorization): a role rebind never strands a holder (verified
`--as-user <owner>` always works); only RETIREMENT strands, remedied
by revocation. Never silent re-resolution.
`assignments --role R`: resolves the same way, then filters — a dumb
filter input.

## Response shapes (F10)

assignment: {id, subject, holderKey, holderRole, holderFallback,
openedByUser, openedBySession, openedAt, state, outcome, closedAt,
closedByUser, closedBySession, closingAttestId} — null for absent.
attest: {id, assignmentId, kind, note, bySession, ts}.
assignments: {assignments: [assignment...]}.
attest verb: {assignment, attest}. Errors use the existing envelope.
COMPLETE code inventory with transport status (r2-6; the router's
status mapping is EXTENDED with these — that extension is authorized):
403-class: not_holder, not_authorized, process_denied,
principal_required. 404-class: unknown_assignment. 400-class:
missing_target, invalid_kind, invalid_subject, invalid_note (blank-only
or oversize), invalid_state_filter, invalid_idempotency_key (blank or
oversize >200), assignment_closed, session_retired, and
invalid_target_kind (the userId teaching error — same code on assign
AND on assignments queries). 404-class also includes the EXISTING
not_found for unknown sessionKey/role targets (router behavior today —
listed so the inventory is complete, not changed). Precedence follows
§Authorization's pinned order. Control-plane transports keep their
200-with-error convention; the classes above bind the /agent REST
statuses.

## Public API (for supervision)

- Assignments.open_count(db, session_key) :: non_neg_integer
- Assignments.list(db, filters) — what the query verb uses.
- Authorized extensions owned by supervision-impl-v1 (built in ITS
  lane, listed here so this inventory is complete):
  Assignments.oldest_open/2 and Assignments.attest_count/2.
No other public surface.

## Events & audit (F9)

All four verbs flow through Dispatch with the EXISTING audit
semantics, stated exactly (r2-7): for accepted calls, the kind="verb"
append happens AFTER the handler commits and its failure PROPAGATES
(Dispatch requires the append to succeed — the caller sees an error
though the domain rows are committed); only STATUTE denials use the
best-effort wrapper. This spec changes none of that and authorizes no
change. A crash or sink failure between commit and append leaves
domain rows without the event row: the assignments/attests tables ARE
the record of truth; the event log is the audit trail. No new event
kinds. No double-logging.

## Invariants (acceptance lens)

1. An open assignment is exactly one row with state='open'; the stall
   conjunct is open_count. No derived or inferred state.
2. Filings are rows or they did not happen; nothing reads content,
   evaluates quality, or concludes intent.
3. Terminal transitions are single-transaction atomic (§Atomicity);
   "assignment_closed" is the ONLY possible result of losing a race —
   never a double-close, never an orphan terminal attest.
4. Authorization binds to token-resolved principals; declared as/asUser
   grant nothing here; process origins denied everywhere in this spec.
5. Typed references: sessionKey | role via the EXISTING seam mechanics;
   userId-as-holder gets a teaching error; retired holders refused.
6. Zero behavior change to every existing verb and to sessions that
   never touch assignments.

## CLI (Rust, cli/ — conventions from cli-rust-v1.md)

- `tightbeam assign --subject "..." (--session K | --role R)
  [--idempotency-key IDEM]`   (--session, matching existing flags; F7)
- `tightbeam attest <assignment-id> --kind progress|completion|surrender
  [--note "..."]`
- `tightbeam revoke-assignment <assignment-id>`
- `tightbeam assignments [(--session K | --role R)] [--state S]`
Output/exit conventions identical to existing subcommands. Add ONE
compact Operations-fragment bullet teaching assign/attest/assignments
(mechanics only, existing bullet style).

## Tests (condensed contract — cover every clause)

Schema CHECKs: every consistency clause in §Schema (state/outcome/
closed-fields/closing_attest_id/holder_fallback/opener-exactly-one).
assign: by sessionKey; by role bound-active (pin + provenance); by role
unbound → Main fallback recorded; unknown role/session; retired holder
refused; userId teaching error; subject blank/oversize; idempotent
replay returns the original (and: two CONCURRENT same-key assigns
yield one row — the F6 race test); process origin denied; user opener
and session opener columns each recorded correctly.
attest: holder progress (stays open) / completion / surrender (closed,
outcome, closing_attest_id set — asserted as one atomic step);
non-holder session "not_holder"; user caller refused; process denied;
closed → "assignment_closed"; unknown id; invalid kind; CONCURRENT
completion vs revoke → exactly one wins, loser gets
"assignment_closed", no orphan attest row (the F5 race test).
revoke: admin user; opener-user; opener-session; non-opener non-admin
"not_authorized"; no attest row created.
Query: state filters; both reference types; role-resolution filter;
ordering incl. equal-timestamp tie-break.
API: open_count across open/closed mix. Events: each verb appends one
kind="verb" row (sink-available case). Statutes: one integration test
with a real [[rule]] denying assign. Principal/precedence: nil →
principal_required on every verb; {:process,_} → process_denied on
every verb INCLUDING revoke and query; BOTH precedence layers proven:
a malformed target refuses in the router (no event row, existing
semantics) even with a process principal; within the handler, process
beats nil beats authorization beats state. Idempotency migration: CHECK
widened in fresh DDL + rename-rebuild proven against a pre-existing
DB; collision test: a user id string equal to a session key string
scopes separately under the prefixes. Audit: accepted-call event
append failure PROPAGATES after domain commit (proven with a failing
sink). CLI: each subcommand via the CLI-integration harness DEFINED IN
session-tokens-v1 r3 (this spec does not define its own).

## Handoff

Gates: mix compile --warnings-as-errors clean; full mix test green;
cargo test green in cli/. Commit on the branch; do not merge. STOP and
report on any conflict with existing code or this spec.
