# Check tier v1 — verdict filings and completion gating (implementation spec, r4)

Status: DRAFT r4 (r3 round: the 'no router change' prohibition scoped to error_status/1 only — the additive @agent_verbs registration of the new `attests` verb is explicitly authorized). Prior:
CONFIRMED all four r1 fixes sound — FK-safe rebuild, verdict/revoke
ordering, raw-kind branch + narrowed compat, cached $assignment — and
returned six precision findings, no design rework: the public API is
pinned to NON-COLLIDING Tightbeam.Assignments functions
(verdict_kinds/2, list_attests/2) — no Tightbeam.Attests module
exists, attests are owned by Tightbeam.Assignments, and
Assignments.list/2 is already taken with different semantics; the
constitutional-refusal claim and invariant 4 are SCOPED to rules
demanding an assignment.* fact — an attest.kind-only rule may
legally pre-empt unknown_assignment (r6 invariant 1); the
supervision-impl cite is updated r11→r13; the verdictKind lexicon
parenthetical is corrected — statute rule names share the character
grammar but carry NO length cap, the 64 cap is new here; the router
status-mapping "extension" is deleted as a no-op — the landed
catch-all already maps both new codes to 400; and the "landed
precedence tests stand untouched" claim is retracted — the landed
fixtures use literal 'verdict' as the invalid-kind fixture
(assignments_test.exs ~147) and must move to a different garbage
kind, with the 'verdict' assertions updated separately to the
verdict path. The free-lexicon ruling held review unchanged again.)
r2 was: (r1 adversarial round, four findings: attests rebuild pinned
FK-safe — foreign_keys=OFF window with foreign_key_check, because
assignments.closingAttestId is an inbound FK to attests;
verdict/revoke race contract restated for a NON-CLOSING verdict —
both-succeed legal, only a post-closure verdict row forbidden;
zero-rules backward-compat narrowed to no-policy-change with the
authorized observable deltas enumerated and attest r5's LANDED
handler order restored; unknown-vs-empty for assignment.verdicts
pinned via the shared cached $assignment resolution mirroring the
landed $target pattern.) r1 was: initial draft.
This is the check tier promised by attest-v1.md r5
(§DELIBERATE NARROWING: "verdict-carrying attests arrive with the check
tier as a spec revision, extending the attests table rather than
redesigning it") and by supervision-v1.md §Prerequisites item 5
("report-done refused without required fact rows"). It is
SIMULTANEOUSLY an authorized revision of TWO closed sets: attest r5's
kind vocabulary (gains `verdict`) and statute-engine-v1.md r6's fact
vocabulary (gains four facts). Both parent specs declare those sets
closed-except-by-spec-revision; this spec is that revision, for exactly
these additions and nothing else. Attest r5 and statute-engine r6
remain sole authorities for everything they pin; where this spec is
silent, they govern unchanged.

The claims-vs-facts line (bible T1; ledger's verification walls —
generators can't judge themselves): a completion attest is the holder's
CLAIM of done. A VERDICT is a fact row filed by someone else — a
reviewing agent or a human — asserting a named check held
("tests-passed", "reviewed"). The check tier makes the claim REFUSABLE
until the facts exist. The substrate never judges whether work is good:
it counts rows of named kinds. Requiring them, and which ones, is
OPERATOR LAW — statutes, not code. This spec's entire enforcement
surface is: one new attest kind, four new statute facts, one read verb.
The gate itself is a TOML file the operator writes.

BUILD ORDERING: cut the worktree from main AT OR AFTER f739c07 (attest
merged). Verified present on main @ f739c07: the Dispatch chokepoint
with `Rules.evaluate(db, call)` before every handler and `:principal`
OPTIONAL in the call type (dispatch.ex ~36-70); the Rules fact table +
type-generic list-fact validation and the cached `$target` dependency
pattern (rules.ex ~27-40, ~170, ~355); session tokens (`cliToken`,
principal seam); sessions.archetype NOT NULL (org.ex ~64); the
`assignments`/`attests` schema, the attest/revoke handlers and their
landed error precedence (assignments.ex ~12-59, ~194-241); the
rename-rebuild migration precedent (idempotency.ex ~38) — which this
spec's migration deliberately does NOT copy verbatim (§Schema: attests
has an inbound FK; the bare rename-rebuild is FK-unsafe there). If the
attest schema or verbs are absent from main, STOP and report.
Supervision-impl is an independent sibling lane: it and this spec
extend attest's modules with DISJOINT function sets and share no
tables — either merge order works.

## Goals

1. "Report done" is refusable by data: an operator rule can deny
   attest(completion) until named verdict rows exist on the assignment.
2. Verdicts are first-class attested facts: attributed rows filed by a
   session OR a user, never inferred from prose, never content-read.
3. Zero new enforcement machinery: the gate is the existing statute
   chokepoint evaluating operator TOML over four new facts.
4. Filed proof is inspectable: a read verb lists an assignment's
   attests.

## Non-goals (do not build)

Verdict VALUES or payloads — no pass/fail enum, no findings body: a
verdict row asserts its named fact holds; adverse findings are notes or
a future structured-turn-results spec (decisions ledger, candidate b).
Verdict withdrawal/edit/delete (append-only like all attests; a wrong
verdict is remedied by revocation of the assignment or operator rule
change). Per-assignment required-proof declarations (an `--require`
flag, policy columns on assignment rows) — requiredness lives ONLY in
statutes. A verdict-kind registry (§Open question). Reaction rails
(verdict → auto-created fix assignment: ledger candidate d). Any change
to supervision's tables, predicate, templates, or ladder. Quality or
content evaluation of any kind. Pagination on the new query verb. UI.

## Ruled decisions (the design core)

- GATE = STATUTE. Required proof is declared as ordinary [[rule]] TOML
  on verb "attest" (deny-only, chokepoint-evaluated, refuse-by-name,
  fail-closed — all inherited from statute-engine r6 verbatim). No gate
  code path, no policy table, no new deny mechanism. Rationale: which
  work needs which proof is exactly "rules where sane operators could
  differ" — data, not code (bible §Law litmus).
- PROOF = PRESENCE. "Proof exists" means: ≥1 `attests` row with
  kind='verdict' and the named verdictKind against that assignmentId.
  Existence, not quality; the substrate never reads verdict content.
  Expressed in rules as `assignment.verdicts not_in [<kind>]` → deny
  (the intersection-empty reading of not_in on a list fact — the
  canonical POSITIVE use of statute r6's empty-list warning).
- WHO FILES: constitutionally, ANY session or user principal may file a
  verdict — including the holder. Forbidding self-verdicts is a policy
  sane operators could differ on → statute (worked example below), not
  code. Users file because humans verify (Flynn is a verdict source);
  this is the one attest kind not holder-gated and the one that may be
  user-filed.
- ONE VERB, NOT TWO: verdicts ride the existing `attest` verb (new
  kind), not a new verb — the closed verb set grows by only the read
  verb `attests`. Verdict filing needs attest's exact machinery
  (assignment lookup, open-check, atomic insert, audit) and nothing
  else.

## Schema (attests table extension; FK-safe rebuild migration)

attests gains (camelCase in DDL, per attest's ruling):

- kind CHECK widened: IN ('progress','completion','surrender',
  'verdict').
- verdictKind TEXT NULL — the named fact, e.g. "tests-passed".
  Lexicon: `^[a-z0-9][a-z0-9-]*$`, 1..64 chars (same character
  grammar as statute rule names — rules.ex @name_re — but rule names
  carry NO length cap in code and none is added here; the 64-char cap
  is NEW and applies to verdictKind only. Verdict kinds are compared
  as exact strings by rule values; lowercase-kebab keeps filings and
  TOML aligned by construction).
- byUser TEXT NULL — user filer, verdicts only.
- bySession widens to NULL-able (it was NOT NULL); consistency moves
  into CHECKs:
  - kind IN ('progress','completion','surrender') → bySession NOT NULL
    AND byUser IS NULL AND verdictKind IS NULL (v1 rows unchanged and
    valid as-is).
  - kind = 'verdict' → verdictKind NOT NULL AND exactly one of
    bySession/byUser non-null (the assignments opener-columns pattern).

Migration: fresh DDL carries the widened shape. Existing DBs need a
rebuild — SQLite cannot ALTER a CHECK (the idempotency/wake
precedent's own reason, idempotency.ex ~37), and no rebuild-free
widening exists — but NOT that precedent's bare rename-rebuild:
attests has an INBOUND FK (`assignments.closingAttestId TEXT NULL
REFERENCES attests(id)`, assignments.ex ~27) and every connection
opens with `PRAGMA foreign_keys=ON` (db.ex ~102). With foreign keys
enabled, `ALTER TABLE attests RENAME TO attests_old` rewrites the
REFERENCES clause stored in assignments' DDL to point at attests_old;
the later DROP then fails with a foreign-key error on any DB holding a
completed/surrendered assignment (non-null closingAttestId), or leaves
assignments referencing a nonexistent table. Pin SQLite's documented
table-rebuild procedure (lang_altertable, "Making Other Kinds Of Table
Schema Changes") instead, as statements on the (serialized) DB
connection — the two PRAGMAs MUST run outside any transaction (PRAGMA
foreign_keys is a no-op inside one):

1. `PRAGMA foreign_keys=OFF`
2. `BEGIN IMMEDIATE`
3. `CREATE TABLE attests_new (...)` — the widened DDL under the
   temporary name
4. `INSERT INTO attests_new (id, assignmentId, kind, note, bySession,
   ts) SELECT id, assignmentId, kind, note, bySession, ts FROM
   attests` (verdictKind/byUser stay NULL — v1 rows valid as-is)
5. `DROP TABLE attests` (no FK complaint: enforcement is off)
6. `ALTER TABLE attests_new RENAME TO attests` — with foreign keys
   OFF the REFERENCES clause in assignments is NOT rewritten; it still
   names `attests` and now resolves to the rebuilt table
7. `PRAGMA foreign_key_check` — MUST return zero rows; any row →
   raise and refuse to serve (fail closed, never a silent
   half-migration)
8. `COMMIT`
9. `PRAGMA foreign_keys=ON`

The transaction around steps 3-7 makes a mid-rebuild crash roll back
to the intact v1 table. Detection: the stored DDL via sqlite_master
contains `'verdict'` → skip (idempotent — the idempotency.ex ~41-50
detection pattern). Runs in ensure_schema before any verb is served.
No other table changes. `closingAttestId` semantics untouched — a
verdict is never a closing attest.

## Verbs

`attest` — AMENDED. Params gain `verdictKind` (wire name; required iff
kind='verdict', refused on other kinds). kind='verdict' appends a row;
the assignment STAYS OPEN (like progress). Same atomicity pattern as
progress: guarded EXISTS-open check + INSERT, one transaction. Because
a verdict does not close, the verdict/revoke race contract is NOT r5's
one-winner contract. Under the DB's serialized transactions, both
orders are legal outcomes: revoke-then-verdict → the verdict sees a
closed assignment and is refused "assignment_closed", no row;
verdict-then-revoke → BOTH succeed — the verdict landed on a then-open
assignment and the revoke closes normally afterward. A verdict row on
a later-revoked assignment is an ordinary append-only fact, not a
state, and is FINE. The sole race invariant: NO verdict row ever lands
AFTER closure — guaranteed by the guarded open-state check in the same
transaction as the INSERT. Returns {assignment, attest}, uniform.

Handler order — attest r5's LANDED order is preserved VERBATIM for
lifecycle kinds; this spec authorizes no reordering. The handler
branches on the RAW kind param (read for dispatch, not validated):

- kind = exactly 'verdict' → the verdict path below.
- ANY other value (lifecycle kinds, missing, non-string, garbage) →
  the landed lifecycle path UNCHANGED: principal checks
  (process_denied → principal_required) → row lookup
  (unknown_assignment) → holder authorization (not_holder) → state
  (assignment_closed) → param validation LAST (invalid_kind,
  invalid_note; assignments.ex ~197-215). Every lifecycle and
  invalid-kind call keeps r5's exact precedence SEMANTICS (non-holder
  beats invalid kind; closed beats invalid params) — but the landed
  precedence TESTS do change textually: their invalid-kind fixture is
  the literal 'verdict' (assignments_test.exs ~147), which this spec
  routes down the verdict path, so §Tests pins the rewrite (semantics
  preserved with a different garbage kind; the former 'verdict'
  assertions updated separately). The stray-verdictKind refusal
  (verdictKind present on a non-verdict kind → invalid_verdict_kind)
  joins this path's param step AFTER valid_kind and valid_note —
  precedence-last like all lifecycle param errors.
- The verdict path MIRRORS the landed shape, params last: principal
  checks (process_denied → principal_required, shared — the landed
  principal_allowed already admits both session and user principals,
  zero change) → row lookup (unknown_assignment) → authorization (any
  {:session, _} or {:user, _} principal — no holder check; this is
  the one non-holder-gated kind) → state (assignment_closed) → param
  validation (missing_verdict_kind, invalid_verdict_kind
  lexicon/length, invalid_note).

`attests` — NEW read verb. Params: {assignmentId}. Any non-nil
session/user principal (attest r5's query rule: no visibility
partitioning in v1); process denied. Unknown id → unknown_assignment.
Returns every attest row for the assignment, all kinds, ordered ts ASC,
id ASC (deterministic tie-break). No pagination. No typed target (the
reference is the params id, like attest itself — nothing for the router
to resolve).

New error codes (400-class unless noted): missing_verdict_kind
(kind='verdict' without the param), invalid_verdict_kind (lexicon or
length failure, OR verdictKind present on a lifecycle kind — message
says which). All other codes are attest r5's inventory unchanged. NO
error_status/1 change is required or authorized: its catch-all
(router.ex ~611) already maps every unlisted code — including these
two — to 400; adding clauses for them would be dead code. The ONE
authorized router change is the additive registration of the new
`attests` read verb in the `@agent_verbs` allowlist (router.ex ~316) —
without it the CLI request is rejected before dispatch; this is the
same one-line allowlist addition every new verb makes, not an
error-mapping change.

Public API additions, built in this lane, as new functions on
Tightbeam.Assignments — the module that owns all attest code. There
is NO Tightbeam.Attests module and this spec does NOT create one (the
supervision-impl precedent is exactly this: authorized extensions
land as new Assignments functions, like oldest_open/2 and
attest_count/2). Names are pinned NON-COLLIDING —
Assignments.list/2 already exists with filter semantics and is
untouched:
- Assignments.verdict_kinds(db, assignment_id) :: [String.t()] —
  DISTINCT verdictKind values (the fact source).
- Assignments.list_attests(db, assignment_id) — what the `attests`
  query verb uses.
No other public surface.

## Statute facts (vocabulary extension; rules.ex @facts + moduledoc)

Four entries join the closed fact table. All follow r6's regime
verbatim: computed demand-driven, cached per call, total-catch wrapped
(escape → rule_error deny, fail closed), nil-never-fires. The
assignment.* facts are DUMB PARAM-DRIVEN lookups — computed from the
call's assignmentId param on ANY verb that carries one (attest,
revoke-assignment), so operators may gate revocation on the same facts.

PINNED RESOLUTION — all three assignment.* facts resolve through ONE
internal cached dependency, mirroring the landed `$target` pseudo-fact
(rules.ex ~355, the with_dependency pattern): `$assignment` = the
assignment row for the call's assignmentId param, or nil when the
param is missing/non-string or no row exists. Computed once per call,
cached like every fact. Each assignment.* fact maps $assignment = nil
→ nil (nil-never-fires) and computes from the row otherwise. In
particular, assignment.verdicts consults Assignments.verdict_kinds/2 ONLY
when $assignment is non-nil: verdict_kinds/2 keeps its plain
[String.t()] return and is defined only over existing assignments —
the unknown-vs-empty distinction (nil for unknown assignment, present
[] for an existing assignment with zero verdicts) is carried entirely
by the $assignment resolution, NEVER by verdict_kinds/2's return
shape. `assignment.caller_is_holder` additionally reads the call's
PRINCIPAL with Map.get (`:principal` is OPTIONAL in the Dispatch call
type — dispatch.ex ~39; a missing key reads as nil → the fact is nil
and never fires, not a rule_error; principal-derived, unlike the
origin-derived caller.* facts — stated in the moduledoc).

| fact | type | definition & nil cases |
|---|---|---|
| attest.kind | string | the attest call's kind param when it is a string, RAW (no trim, no vocabulary check — garbage reaches the handler and refuses there); nil when missing/non-string or the verb is not "attest" |
| assignment.verdicts | list(string) | DISTINCT verdictKind set over kind='verdict' rows for the assignmentId param — a PRESENT [] when the assignment exists with zero verdicts (not_in FIRES on it: that IS the gate); nil when $assignment is nil (param missing/non-string or no assignment row) |
| assignment.holder_archetype | string | the holder session row's archetype for the named assignment (holder rows always exist and archetype is NOT NULL — org.ex; so non-nil whenever the assignment exists); nil when $assignment is nil |
| assignment.caller_is_holder | bool | true iff the call's principal is {:session, K} with K = the assignment's holder key; FALSE for every other non-nil principal (user, process, non-holder session); nil when the principal is nil/absent or $assignment is nil |

Typing per r6's operator matrix: assignment.verdicts is a list fact —
in/not_in only, intersection semantics; the load-time validator is
already type-generic (rules.ex validate_value! matches on
{:list, :string}, verified), so r6's "caller.roles only" prose is
amended to "list facts: caller.roles, assignment.verdicts" with zero
validator code change. attest.kind / holder_archetype: string ops.
caller_is_holder: bool (eq/ne). Moduledoc: fact table extended; the
empty-list warning gains the gate as its worked positive example.

PRECEDENCE FOR FREE (nil-never-fires doing its job), SCOPED to rules
demanding an assignment.* fact: such a rule against an UNKNOWN
assignment computes that fact = nil → the rule cannot fire → the
handler refuses unknown_assignment. The scope matters: a rule whose
conditions demand only attest.kind (e.g. deny all completions) fires
regardless of whether the assignment row exists — rule_denied then
legally pre-empts unknown_assignment. That pre-emption, like a rule
pre-empting assignment_closed or not_holder, is r6 invariant 1
behavior (deny pre-empting deny, outcome class identical, never a
grant).

BACKWARD COMPAT (deliberately narrower than "attest v1 exactly"):
zero rules → NO GATE-POLICY CHANGE. Every lifecycle attest call —
valid or invalid — takes r5's landed path with r5's exact error
precedence and outcomes (§Verbs: the landed order is preserved, not
reordered). But observable equivalence in r6 invariant 8's strict
sense does NOT hold, and this spec says so honestly: even at zero
rules there are exactly FOUR authorized observable deltas, all new
surface or additive —
1. kind='verdict' calls, refused in v1 (invalid_kind, at v1's
   precedence position), now run the verdict path. That IS the
   feature.
2. Attest response objects gain two always-present fields, verdictKind
   and byUser — null on every lifecycle attest (additive; existing
   consumers unaffected).
3. The new `attests` read verb and the two new error codes exist.
4. A lifecycle call carrying a stray verdictKind param — silently
   ignored in v1 (the router atomizes params without a whitelist,
   router.ex ~641; the v1 handler never read it) — is now refused
   invalid_verdict_kind, at the param step (precedence-last).
Nothing else changes at zero rules: no precedence shift, no gate — an
org that writes no gate rules gets zero POLICY change, forever.

Worked operator law (illustrative, not shipped):

    [[rule]]
    name = "coder-completion-needs-tests"
    verb = "attest"
    deny_when = [
      { fact = "attest.kind", op = "eq", value = "completion" },
      { fact = "assignment.holder_archetype", op = "eq", value = "coder" },
      { fact = "assignment.verdicts", op = "not_in", value = ["tests-passed"] },
    ]
    text = "completion requires a tests-passed verdict on the assignment"

    [[rule]]
    name = "no-self-verdicts"
    verb = "attest"
    deny_when = [
      { fact = "attest.kind", op = "eq", value = "verdict" },
      { fact = "assignment.caller_is_holder", op = "eq", value = true },
    ]
    text = "verdicts are filed by someone other than the holder"

N required kinds = N rules, one per kind (each missing kind denies by
its own name — implicit-AND-within, OR-as-multiple-rules composes
requirement conjunction correctly). Denials: code "rule_denied",
`<rule-name>: <text>`, one best-effort kind="denied" event — all r6,
nothing new.

DOCUMENTED HAZARD, not prevented: statutes can gate ANY attest kind —
an operator who gates completion AND surrender behind unsatisfiable
proof creates a prod-forever loop. Deny-only makes this loud and safe
(over-restriction, visible as denied events and live prods), and the
remedies are the operator's: fix the rule, file the verdict, or revoke.
This spec adds no gate to surrender or revoke and recommends none.

## Supervision interaction (confirmed no conflict; zero changes)

- A REFUSED completion inserts nothing: the assignment stays open,
  open_count ≥ 1 holds, the turn ended with no filing → the terminal is
  a stall edge → supervision prods. That is the DESIGN: the pressure
  stays on until the proof rows exist, the holder files progress, or it
  surrenders. The prod template's "file completion" remains honest —
  completion is available the moment the facts are.
- A VERDICT row increments the assignment's attest row count, so it
  RESETS the prod counter (supervision-impl r13 step 6 counts rows
  via Assignments.attest_count, "kind is irrelevant" — verbatim
  sibling-spec prose; supervision-impl has no landed code at
  f739c07). Correct:
  a fresh verdict is activity on the record.
- Nothing else touches: no supervision table, template, ladder, or
  predicate change; supervision needs no knowledge that a gate exists.

## Response shapes

attest object gains verdictKind and byUser (null for absent — additive;
existing consumers unaffected; this is authorized zero-rule delta 2,
§Backward compat): {id, assignmentId, kind, verdictKind,
note, bySession, byUser, ts}. attests verb: {attests: [attest...]}.
Events: verdict filings append kind="verb" via Dispatch's existing
semantics; gate denials kind="denied" — no new event kinds.

## CLI (Rust, cli/ — conventions from cli-rust-v1.md)

- `tightbeam attest <assignment-id> --kind verdict --verdict <kind>
  [--note "..."]` — `--verdict` required iff kind=verdict.
- `tightbeam attests <assignment-id>`.
Output/exit conventions identical to existing subcommands. Extend the
attest Operations-fragment bullet with verdict/attests mechanics (same
bullet, existing style).

## Invariants (acceptance lens)

1. The gate is operator data at the existing chokepoint: zero new
   enforcement code paths; zero rules ⇒ no gate-policy change — the
   only zero-rule observable deltas are the four enumerated authorized
   ones (§Backward compat), and lifecycle error precedence is r5's
   landed order unchanged.
2. Proof is presence: gate outcomes depend only on the EXISTENCE of
   verdict rows with named kinds; no code path reads verdict content or
   evaluates quality (T1 — the substrate counts, it never judges).
3. Verdicts are attributed, append-only rows filed by session or user
   principals — never process, never withdrawn, never inferred.
4. Deny-only composition holds end-to-end: no statute can make any
   attest succeed where attest v1 refuses; against rules demanding an
   assignment.* fact, the unknown_assignment refusal survives via
   nil-never-fires (an attest.kind-only rule may legally pre-empt it
   with rule_denied — same outcome class, r6 invariant 1).
5. A gated-incomplete assignment is an ordinary open assignment:
   supervision's conjunct, prods, and escalation see nothing new.
6. Zero behavior change to lifecycle attests' rows, authorization,
   atomicity, and error precedence (the landed order stands); existing
   DBs — including those holding completed/surrendered assignments
   with non-null closingAttestId — migrate through the FK-safe rebuild
   with all rows valid and foreign_key_check clean.

## Tests (condensed contract — cover every clause)

Schema: widened kind CHECK; verdict CHECKs (verdictKind ⇔ verdict,
exactly-one filer on verdict, lifecycle rows unchanged-and-valid);
the FK-safe rebuild proven against a pre-existing attest-v1 DB that
CONTAINS a completed assignment (non-null closingAttestId) plus its
attest rows — post-migration: PRAGMA foreign_key_check returns zero
rows, the closed assignment and its closing attest remain readable and
valid, and assignments writes still work; migration idempotent on
re-run; fresh DDL.
attest(verdict): filed by non-holder session / by holder session / by
user — all accepted with correct filer columns; process denied; nil
principal; unknown assignment; closed assignment; missing/malformed
(lexicon, oversize) verdictKind; verdictKind on a lifecycle kind
refused; duplicate same-kind verdict appends a second row; assignment
stays open; returns both objects; verdict vs revoke SERIALIZED
ORDERINGS (not a one-winner race): revoke-then-verdict → verdict
refused "assignment_closed" and NO verdict row exists;
verdict-then-revoke → BOTH succeed and the verdict row stands on the
revoked assignment (legal append-only fact); in neither order does a
verdict row land after closure. Order pins: lifecycle path — r5's
precedence SEMANTICS preserved, but the landed test file DOES change:
the fixtures using literal 'verdict' as the invalid kind
(assignments_test.exs ~147 — both the not_holder and the invalid_kind
assertions) are rewritten to a different garbage kind (e.g. 'bogus')
so the semantic tests still hold (non-holder + invalid kind →
not_holder; invalid kind from the holder → invalid_kind), and the
former 'verdict' assertions are updated SEPARATELY to their
verdict-path outcomes (both carry no verdictKind param, so on an open
assignment both become missing_verdict_kind — the non-holder one
because the verdict path has no holder check); lifecycle kind + stray
verdictKind → the constitutional
refusals still win (non-holder + stray verdictKind → not_holder), and
invalid_verdict_kind only after lookup/holder/state pass; verdict
path — unknown assignment + missing verdictKind → unknown_assignment;
closed assignment + malformed verdictKind → assignment_closed (params
last on both paths).
attests query: all kinds returned, ts/id ordering incl. tie-break;
unknown id; nil principal; process denied.
Facts: per-fact presence/nil matrix (missing param, non-string param,
unknown assignment — ALL THREE assignment.* facts nil via the shared
$assignment resolution; nil/user/process/other-session principals for
caller_is_holder, plus a call map with NO :principal key → nil fact,
not rule_error); verdicts unknown-vs-empty pinned: unknown assignment
→ nil (a not_in gate rule cannot fire), existing assignment with zero
verdicts → present [] (not_in FIRES); verdicts DISTINCT; load-time
typing (eq on assignment.verdicts → load error; in/not_in value
validation;
caller_is_holder bool); laziness (a would-raise fact after a false
condition causes nothing); a demanded fact that exits → rule_error
deny.
Gate end-to-end: completion denied by a require-rule (rule_denied, one
denied event, NO attest row, assignment open, handler not invoked);
verdict filed → same completion accepted and closes atomically; two
required kinds as two rules → each missing kind denies by its own
name; archetype-scoped rule inert for other archetypes;
no-self-verdicts blocks the holder's verdict while a user's passes;
gate rule present + unknown assignment → unknown_assignment (the
nil-never-fires precedence test — valid because the gate rule demands
assignment.verdicts; an attest.kind-only rule would legally pre-empt
with rule_denied, §PRECEDENCE); zero rules → no-policy-change
(completion with zero verdicts accepted; a lifecycle error-precedence
spot-check matches r5's landed tests; the only response delta is the
two null fields).
Supervision seam (one integration test each): a rule-denied completion
leaves open_count ≥ 1; a verdict row advances the assignment's attest
row count (the progress-reset input).
Events: verdict → one kind="verb" row; denial → one kind="denied" row.
CLI: both subcommands via the session-tokens CLI-integration harness.

## Handoff

Gates: mix compile --warnings-as-errors clean; full mix test green;
cargo test green in cli/. Commit on the branch; do not merge. STOP and
report on any conflict with existing code, attest's landed shape, or
this spec.

## Open question (Flynn)

Verdict-kind vocabulary: this spec rules FREE LEXICON strings (any
`^[a-z0-9][a-z0-9-]*$` name; the org's statutes close over the names
that matter). The hazard is silent typo drift — a "test-passed" filing
never satisfies a "tests-passed" gate; deny-only keeps it safe (the
completion stays refused, loudly) but an operator may prefer a
REGISTERED vocabulary (a kinds file beside the rules, fail-closed at
filing time) so typos refuse at the source. That is a real
operator-experience fork — registry-as-data is more law to maintain;
free lexicon is more rope. Ruled free-lexicon for v1; flagging because
retrofitting a registry later tightens legally (deny-only) but will
refuse previously-legal filings.
