# P3 — observables & producers v1 (implementation spec, r7)

Status: DRAFT r7 — hardened through eight adversarial ensemble rounds; companion-aligned with mechanism r10 / smoke r9 / escalation r6. Makes roadmap phase **P3** (`rails-and-guidance-roadmap.md`
§P3) implementable as parallel focused lanes. Authority: this spec is the sole
authority for the P3 observables and the review-of relation; its producer
subsystem (§5, and §4B's producer-backed deny-halves) is superseded — see
the banner at §5. It is
an authorized revision of two closed sets — `rules.ex`'s `@facts` registry
(gains the facts in §4) and the `attests` table (gains four provenance/author-
identity columns, §3.2) — exactly as `check-tier-v1.md` was for those same sets,
and for nothing
else. Parents govern where this spec is silent: `attest-v1.md` r5 (assignment/
attest behavior), `check-tier-v1.md` r4 (verdict filings, the `assignment.*`
fact regime, the FK-safe attests rebuild), `work-item-v1.md` r2 (the additive-
column migration precedent), the guidance spec `agentic-engineering-guidance-
spec.md` §6 (the enforcement mapping these rails satisfy), and the roadmap D1
ruling (**hybrid**: predicates are the always-on hot path; scripts are added
later).

Ground truth read on `main`: `lib/tightbeam/rules.ex` (the closed `@facts`
registry, the `$assignment`/`$target` cached-dependency pattern, the
literal-only `compare/3`), `lib/tightbeam/assignments.ex` (assignment/attest
storage, the FK-safe attests rebuild `ensure_attests_shape/1`, `verdict_kinds/2`),
`lib/tightbeam/org.ex` (session columns `harness`/`provider`/`model`/`archetype`/
`spawnedBy`), `lib/tightbeam/gateway.ex` (verb handler table, `session_workdir/2`,
model catalog), `lib/tightbeam/wire/router.ex` (`@agent_verbs` allowlist).

---

## 0. The load-bearing constraint (read first)

The statute engine compares a **fact against a rule literal** and nothing else.
`rules.ex` `compare(left, op, right)` binds `right` to `condition.value`, a
constant parsed from TOML. There is **no fact-to-fact operator**. Therefore a
rule cannot say "verdict author session ≠ this assignment's holder" or "author
harness ≠ producer harness" by naming two facts — one side of every comparison
is always an operator-written constant.

Every independence and provenance judgment in P3 is consequently **pre-joined by
the substrate into a fact whose value the operator matches against a literal**.
The chosen shape reuses the exact pattern check-tier already shipped:
`assignment.verdicts` is a `list(string)` of verdict kinds, and the operator
names the required kind as the literal (`not_in ["tests-passed"]`). P3 adds more
`list(string)` facts that are the **same set narrowed by an independence or
provenance predicate the substrate computes internally**. The operator still
supplies the kind; the substrate supplies "…filed by someone other than the
holder," "…by a cross-harness author," or "…by a substrate runner." This keeps
the *verdict vocabulary* (`reviewed-clean`, `tests-passed`, `real-run-passed`)
as bundle/org data — a rule literal — while the substrate exposes only
comparisons over its **own native columns** (session identity, `harness`,
`provider`, the producer stamp). The substrate never defines "model family,"
never names an engineering verdict, never decides which kind a given verb
requires.

This is why every P3 observable that a deny-half keys on is a **registered
fact**, not a script (§D1 posture, §7): the deny-halves must be *provable at
P3*, and roadmap P4 (script effect) lands after P3. A pure DB join that must
exist for the deny-half to be expressible cannot wait for the script runtime.
Scripts (P4+) subsume the elaborate cases; the P3 facts are the handful of hot,
terminating, auditable joins the flagship deny-gates cannot be written without.

---

## 1. Invariants (the acceptance lens)

1. **Facts vs literals.** No P3 fact requires a fact-to-fact comparison. Every
   independence/provenance predicate is computed inside the substrate and
   exposed as a `list(string)` or `bool` fact matched against an operator
   literal. The `compare/3` and validator code is unchanged; only `@facts`
   entries and their `compute_fact` clauses are added.
2. **nil never satisfies.** Every new fact obeys `rules.ex`'s regime verbatim:
   computed demand-driven, cached per call, total-catch-wrapped (escape →
   `rule_error` deny, fail closed), and **nil never fires any operator,
   including `ne` and `not_in`**. An empty list is *present* and `not_in` fires
   on it — that is the gate. A fact is nil exactly when its subject cannot be
   resolved (assignment/param missing), never as a disguised "false."
3. **Substrate exposes truth, not policy.** The substrate never hardcodes a
   verdict kind, a "model family" taxonomy, a required-proof declaration, or
   which archetype needs which proof. Required proof is operator statute (TOML)
   over these facts, exactly as check-tier ruled. The substrate's contribution
   is the join and the columns it owns.
4. **Provenance is a column, not a claim.** "A fact was produced by a mechanical
   runner, not self-attested" is carried by a typed `producer` stamp on the
   verdict row, and the exact command that ran is recorded alongside it
   (`producerCommand`). These **two** columns are writable **only** by the
   producer-verb insert path (`insert_producer_verdict_in_txn/2`); no agent-facing verb
   sets them. The producer runs a **committed-config** command, never a caller
   param — the party being measured does not choose the measure (§5A). The stamp
   is the difference between the weak self-attested ladder rung and the strong
   mechanical-producer rung (§6). (The author-identity stamps `byHarness`/
   `byProvider` are separate — see invariant 7 — and are written by **every**
   verdict insert, not only the producer path.)
5. **Review-of is a typed link, not a subject convention.** A review assignment
   names the producer assignment it covers in a typed column; the guidance
   subject convention `review of assignment <id>` becomes advisory prose, no
   longer load-bearing. The independence facts join through the link.
6. **Anti-laundering: independence is only ever established through the typed
   review link.** A verdict filed **directly on** the producer assignment `A`
   never counts toward any independence fact — not even when its author is a
   non-holder, cross-harness session. Independence facts read only verdicts on a
   separate assignment `R` whose `reviewsAssignmentId = A.id`. This closes the
   laundering path where a colluding non-holder (or the holder via a second
   session) files `reviewed-clean` straight onto `A` to manufacture apparent
   independence without any commissioned review. (The plain `assignment.verdicts`
   fact keeps its direct-on-`A` semantics for non-independence uses; the
   `produced_*` fact keys on the `producer` column, not on independence.)
6b. **Commissioned-reviewer-only.** A review-link verdict counts toward an
   independence fact only when its author is the **holder** of the review
   assignment `R` — the commissioned reviewer filing on its own review
   assignment — and that author is not `A`'s holder. A *third* session's verdict
   on `R`, any **user** verdict on `R`, and a verdict authored by `A`'s holder
   never count (users rule by escalation, not review). Who opened `R` does not
   affect this author-independence predicate; `A`'s holder may commission the
   review. Without the author conditions a producer colludes by planting a
   linked "shell" review assignment and filing on it from a second session.
7. **Temporal soundness: independence provenance is stamped, never live-read.**
   The author's model identity is stamped onto the verdict row at filing
   (`byHarness`/`byProvider`), and the reviewed party's identity is stamped onto
   the producer assignment at its creation (`holderHarness`/`holderProvider`).
   Every cross-family fact compares two immutable stamps; it never joins to a
   live session row. A session re-tuning its harness/provider after a filing can
   neither retroactively qualify a same-family review nor disqualify a valid one.
8. **Deny-half only.** P3 delivers the **deny** half of each gate: the verb is
   refused when the required independent/produced fact is absent. Remedies
   (spawn the reviewer, run the runner) are P5; the turn-end edge is P6. A P3
   rail that fires on the dispatch verb and denies is complete for P3; it is not
   yet the full loop.
9. **Additive and reversible.** Every schema change is additive (nullable
   columns, new tables, new verbs); an org that writes no P3 rules and calls no
   producer verb observes zero behavior change. Existing DBs migrate through the
   established precedents (additive `ALTER` for columns that permit it, the
   FK-safe rebuild for the `attests` CHECK/columns). Early-dev clean break is
   acceptable where noted (§3).

---

## 2. Non-goals (do not build in P3)

- **Remedies / active gates.** No spawn/wake/assign on an absent fact (P5). P3
  denies; it does not originate producers.
- **Turn-end sweep.** No omission edge (P6). P3 fires only at the dispatch verb.
- **Script effect.** No TOML statute names a script; no contained script runtime
  (P4). The producer verbs (§5) execute their command as an async local job on
  the gateway host, not through a P4 script-return-set evaluator. When P4 lands,
  producer execution MAY be re-hosted on the script runtime behind the same
  verb/job interface — a substrate-internal change, out of scope here.
- **Remote-host producer execution.** v1 runs producer commands on the **gateway
  host only** (§5B, F10). A holder placed on a remote host cannot have its remote
  build/smoke run in v1; that is a named deferred gap behind the unbuilt
  `Placement.run_on_host` seam, not a v1 feature.
- **Git-diff files-touched.** The **observed** file set (what a lane's branch
  actually changed) is a future, stronger producer requiring branch identity and
  the P4 runtime. P3 ships the **declared** file set only (§5E), and says so.
- **Model-family taxonomy.** The substrate exposes cross-harness and
  cross-provider (its own columns). Grouping distinct models into "families"
  (opus vs haiku) and the "reviewer thinks at a higher level when one family is
  available" fallback are org judgment / advisory guidance, never a substrate
  fact (§4C rationale).
- **Verdict values/payloads, withdrawal, required-proof columns, rail-set
  satisfiability, meta-rails, guidance-change review.** Governed by check-tier
  (unchanged) and later phases.
- **Rating/observability queries.** Denials already emit `kind="denied"` events
  (dispatch, unchanged); no new event kinds, no derived-rating store.

---

## 3. Schema & relations (Lane A)

Three additive changes. All follow the repo's camelCase DDL convention;
snake_case in prose.

### 3.1 Review-of relation — a typed column on `assignments`

**Decision: a single nullable self-referential column, not a relation table.**
A review assignment reviews **exactly one** producer assignment; a relation
table modelling many-to-many is unused surface (YAGNI, architectural-principles
§2/§7). If a future review-covers-many case appears it arrives additively.

- `assignments` gains `reviewsAssignmentId TEXT NULL REFERENCES assignments(id)`.
- Set at `assign` time from a new optional param `reviews` (wire `reviews`,
  atomized `:reviews_assignment_id`). On the create path the handler verifies,
  **inside the assignment INSERT transaction** (the work-item existence-check
  precedent, `work-item-v1` §Atomicity), that the referenced assignment exists —
  unknown → `unknown_review_target`, transaction aborts. Absent → NULL.
  Self-reference (`reviews` == the new id) is impossible (the id is minted in the
  same insert) and needs no guard.
- The reviewed assignment need not share a work-item with the review; linkage is
  the review-of column, not work-item co-membership (this is the whole point —
  the independent-review predicate keys on the link, not on co-membership).
- A verdict "inherits" the link structurally: to find reviews of `A` you query
  `assignments WHERE reviewsAssignmentId = A.id`; their verdicts are `A`'s
  review verdicts. Only these count for independence (invariant 6); a verdict on
  `A` itself never does. No verdict-row change is needed for inheritance.

**Holder model-identity stamp (temporal soundness, invariant 7).** `assignments`
also gains `holderHarness TEXT NULL` and `holderProvider TEXT NULL`, captured
**at `assign` time** from the holder session's then-current identity (the
producer's family "as commissioned"), immutable thereafter. The cross-family
facts (§4) compare a verdict's stamped `byHarness`/`byProvider` against the
reviewed assignment's `holderHarness`/`holderProvider` — two immutable stamps,
never a live `sessions` read. Null on an assignment whose holder had no family
recorded (pre-P3 rows); a null holder stamp makes the cross-family facts nil for
that assignment (ungated), consistent with invariant 2.

- **Migration:** additive `ALTER TABLE assignments ADD COLUMN` for each of
  `reviewsAssignmentId TEXT REFERENCES assignments(id)`, `holderHarness TEXT`,
  `holderProvider TEXT`, duplicate-column tolerated (the `work_item-v1` / org.ex
  host-column precedent). All legal under `foreign_keys=ON` (defaults NULL).
  **Clean break is acceptable** (early dev): no backfill of the old subject
  convention or of holder family onto pre-existing rows is attempted; such rows
  carry NULL and are not gated until re-created. Do not build a backfill.

### 3.2 Provenance & author-identity stamps — four columns on `attests`

- `attests` gains `producer TEXT NULL`. It is non-null **only** on verdict rows
  filed by a substrate producer verb (§5), holding the producer's identifier
  (`"build"` | `"smoke"` — the verb decides; a short lowercase-kebab token,
  `^[a-z0-9][a-z0-9-]*$`, ≤64). Null on every agent- or user-filed attest of
  every kind. No agent-facing verb path writes it.
- `attests` gains `producerCommand TEXT NULL` — the **exact command string the
  substrate ran** to produce this verdict (§5), stored verbatim. It records what
  reality actually touched, so a wrong committed command is visible in the
  attest row without forensics (invariant 4). Written only by a producer verb,
  in the same insert as `producer`.
- `attests` gains `byHarness TEXT NULL` and `byProvider TEXT NULL` — the **filing
  session's harness/provider, stamped at insert by EVERY verdict insert** (F5),
  whoever files it: the ordinary `attest --kind verdict` path stamps them from the
  live filing session, and the `insert_producer_verdict_in_txn/2` path stamps them
  from the values frozen on the `producer_jobs` row at accept (§5B) — same two
  columns, differing only in stamp source (live vs frozen). Non-null on any
  verdict filed by a session; NULL on user-filed verdicts (a user has no model
  family) and on non-verdict lifecycle attests.
  This is the immutable author side of every cross-family comparison; the facts
  never re-read the author's live `sessions` row. **These two columns are
  distinct from `producer`/`producerCommand`:** an ordinary reviewer verdict
  carries `byHarness`/`byProvider` (so it *can* satisfy `cross_harness`) but has
  `producer`/`producerCommand` NULL; a producer verdict carries all four.
- **CHECK:** `producer` non-null implies `kind = 'verdict'`; `producerCommand`
  non-null implies `producer` non-null; `byHarness`/`byProvider` non-null implies
  `kind = 'verdict'` (author-family stamps ride verdict rows only). No other
  CHECK change.
- **Migration — version-aware single rebuild to the full P3 shape.** Adding
  columns under an inbound FK with CHECKs forces the **FK-safe rebuild**
  check-tier already implements in `Assignments` `ensure_attests_shape/1`
  (assignments.ex): `PRAGMA foreign_keys=OFF` → `BEGIN IMMEDIATE` →
  `CREATE attests_new (…full P3 shape: verdictKind, byUser, producer,
  producerCommand, byHarness, byProvider + all CHECKs…)` → `INSERT … SELECT` of
  the **intersection of the current table's columns and the final shape**
  (columns absent in the current table default NULL) → `DROP attests` → rename →
  `PRAGMA foreign_key_check` (zero rows or fail closed) → `COMMIT` →
  `foreign_keys=ON`. **One rebuild reaches the final shape from ANY prior shape**
  — a bare attest-v1 table (no `verdictKind`/`byUser`), a check-tier table, or a
  partial-P3 table — by selecting whatever subset exists; no chained double
  rebuild. **Detection pins the full target shape:** skip only when the stored
  `sqlite_master` DDL contains **all four** new column names **and** the new
  CHECK clauses; any missing column or CHECK triggers the rebuild. (Detecting
  only `producer` would wrongly accept a partial shape missing `producerCommand`,
  `byHarness`, `byProvider`, or a CHECK — F15.) This lane **replaces** the
  existing `ensure_attests_shape/1` detection with the full-shape check and
  reuses its rebuild body; it does not add a second rebuild path.

### 3.3 Declared files-touched — a child table

#### Product ruling — file lists are bootstrap context, never custody (2026-08-11)

The `files` value exists so a parent or prior discovery pass can give a newly
staffed coder a useful starting set of likely-relevant paths. It saves repeated
repository discovery; it is not an authority boundary, a security feature, or a
claim that the list is complete. A coder may read or edit any path needed to
complete its assigned work, whether or not that path appeared in `files`.

Accordingly, `files` is always optional and non-blocking. Missing, incomplete,
or overlapping suggestions must never refuse an assignment, prevent a coder
from beginning work, or require a replacement assignment before editing. The
substrate may persist and return the supplied suggestions as neutral assignment
context. It must not derive access control, exclusive custody, scheduling
ownership, or a completion condition from them.

This ruling supersedes the `files_overlap` refusal, all-open overlap gate, and
"own-worktree/order-same-code" interpretation below and anywhere else in this
spec. Those mechanisms do not implement the product intent and must be removed
rather than repurposed as a softer permission wall. Concurrent-edit conflicts
remain ordinary engineering coordination and reconciliation work; they are not
a substrate authorization decision.

**Decision: a child table, populated at `assign`, not a JSON param column.** A
normalized `assignment_files` table makes the overlap join (§4E) a plain SQL
`INTERSECT`/self-join and keeps the file set queryable; a packed JSON column
would force in-Elixir set math on every candidate. Right-weight: one child
table, one index.

- `assignment_files (assignmentId TEXT NOT NULL REFERENCES assignments(id),
  path TEXT NOT NULL, PRIMARY KEY (assignmentId, path))`.
- Populated at `assign` from a new optional param `files` (wire `files`, a JSON
  array of strings; atomized `:files`). Each path is a non-blank string ≤2000
  chars after trim; a malformed entry refuses `invalid_files`. **Duplicate paths
  within one `files` array are deduped silently** (set semantics before insert),
  so the per-entry validation and the `(assignmentId, path)` primary key never
  disagree — a repeated path is not `invalid_files` (F13). Paths are stored
  **verbatim** — the substrate never resolves, normalizes, or checks them against
  a filesystem (T1: it records the declaration the caller computed).
- **Overlap enforcement is a transactional constitutional check in the `assign`
  handler, not a rules-tier fact (F13).** Inside the same serialized transaction
  that inserts the assignment and its file rows, the handler queries open
  assignments declaring any of the (deduped) declared paths; if any overlap
  exists it aborts and refuses `files_overlap` (403-class, message naming the
  colliding open assignment). Because the read and the insert share one
  serialized DB transaction (the attest-v1 §Atomicity pattern), two concurrent
  overlapping assigns cannot both observe "no overlap" and both commit — the
  loser sees the winner's row and refuses. The rules-tier fact
  `assign.declared_files_overlap_open` (§4) is **advisory/observational only** —
  available for an org that wants to *observe* or additionally gate at the
  statute tier, but never the authoritative race-free enforcement, which is the
  in-handler check.
- Absent `files` → no rows → the assignment declares nothing and the overlap
  check does not fire (opt-in by declaration). This is a forgeability limit
  (§6), stated, not closed here.
- **New table**, created by `Assignments.ensure_schema` after `assignments`
  exists. No migration of existing rows (they simply declare nothing).

### 3.4 Public read surface (owned by Lane A, consumed by Lanes B & C)

New functions on `Tightbeam.Assignments` (the module that owns all
assignment/attest code — no new module, the check-tier / supervision-impl
precedent). Signatures are **pinned here** so Lanes B and C code against them in
parallel before Lane A merges:

- `Assignments.commissioned_review_authors(db, assignment_id, a_holder_key) ::
  [%{verdict_kind: String.t(), by_harness: String.t() | nil,
  by_provider: String.t() | nil}]` — one row per **author-independent**
  review-link verdict, i.e. a verdict `V` filed on an assignment `R` where all of:
  `R.reviewsAssignmentId = assignment_id` (through the typed link, invariant 6);
  `V.bySession = R.holderKey` (the author IS `R`'s holder — invariant 6b(a); a
  third session's verdict on `R`, and any user verdict, are excluded here);
  and `V.bySession ≠ a_holder_key` (author independence). `R`'s opener is not a
  filter: `A`'s holder may commission `R`. `by_harness`/`by_provider` are the **stamped**
  `attests.byHarness`/`byProvider` (invariant 7). The whole 6/6b/independence
  predicate lives here in one tested query; the caller passes `a_holder_key` from
  `$assignment`. Defined only over an existing `assignment_id`; the
  unknown-vs-empty distinction is carried by `$assignment` resolution in rules.ex
  (§4), never by this function's return shape.
- `Assignments.produced_verdict_kinds(db, assignment_id) :: [String.t()]` —
  DISTINCT verdict kinds of `producer`-stamped verdicts **filed directly on**
  `assignment_id` (the producer verb files on the assignment whose work it ran).
  This is the sole reader path for the `produced_verdict_kinds` fact and is
  independent of the review link.
- `Assignments.declared_files(db, assignment_id) :: [String.t()]` — the declared
  path set (may be empty).
- `Assignments.open_assignments_touching(db, paths, exclude_id \\ nil) ::
  [String.t()]` — ids of **open** assignments declaring any path in `paths`,
  excluding `exclude_id`. Used both by the transactional overlap check in the
  `assign` handler (§3.3) and by the advisory overlap fact (§4).
- `Assignments.insert_producer_verdict_in_txn(txn, %{assignment_id:,
  verdict_kind:, producer:, producer_command:, by_session:, by_user:,
  by_harness:, by_provider:})` :: `{:ok, attest} | {:error, map}` — **the sole
  path that writes `producer`/`producerCommand` (F12).** It is an **in-transaction
  form** taking the caller's open `txn` (mirroring the `wake-on-fact`/`Ledger`
  `*_in_txn` precedent), so the producer worker's winning `running → done` CAS and
  this verdict insert commit as **one transaction** (NOT-6). It performs the
  open-state guarded verdict insert and sets `producer`/`producerCommand` plus the
  attribution/author-family stamps passed **explicitly** — the values **frozen on
  the `producer_jobs` row at accept** (§5B), never re-read from a live session at
  completion (F5/F6 — the accepting session may have re-tuned or retired). It
  writes exactly what it is given; it never reads `sessions`. No agent-facing verb
  reaches it; only `Tightbeam.Producers` (Lane C) calls it, inside the CAS
  transaction. It refuses `assignment_closed`/`unknown_assignment` as the ordinary
  verdict path. **There is no `db`-taking plain form** — the only caller needs the
  CAS+insert atomic, so the in-txn form is the only one. (The **ordinary**
  synchronous `attest --kind verdict` path instead derives `byHarness`/`byProvider`
  from the live filing session at insert — correct because it is synchronous; the
  two paths differ only in stamp *source*, live vs frozen.)
- The **ordinary** `attest --kind verdict` insert path (existing `Assignments`
  verdict transaction, Lane A) is amended to stamp `byHarness`/`byProvider` from
  the filing session on every verdict — the one behavioral change to the existing
  attest path (additive columns, previously always NULL).
- The reviewed assignment's `holderHarness`/`holderProvider` stamps (§3.1),
  carried on the `$assignment` row, supply the **producer side** of every
  cross-family comparison — immutable stamps, not a live `sessions` read.

---

## 4. Registry facts (Lane B)

**Five entries** join the closed `@facts` table in `rules.ex`, all
type-generic-validated already (the validator matches `{:list, :string}` and
`:bool`; no validator change — the moduledoc's list-fact enumeration is amended
to name the new list facts). All follow check-tier's regime: demand-driven,
cached per call, total-catch-wrapped, nil-never-fires. The `assignment.*` facts
resolve through the existing cached `$assignment` dependency (nil when the call's
`assignmentId` param is missing/non-string or no row exists → every
`assignment.*` fact nil → cannot fire → the handler's own `unknown_assignment`
survives; check-tier's PRECEDENCE-FOR-FREE, unchanged).

The **producer side** of a cross-family comparison is the reviewed assignment's
**stamped** `holderHarness`/`holderProvider` (§3.1), never a live `sessions`
read; `$assignment` is extended in this lane to carry `holder_harness` and
`holder_provider` alongside `holder_archetype`/`holder_key` (a wider SELECT in
the existing `$assignment` query in **rules.ex** `compute_fact("$assignment", …)`
— owned by Lane B, §7). The **author side** is the verdict row's stamped
`byHarness`/`byProvider`. Both sides are immutable stamps (invariant 7).

Canonical P3 fact-name set — these **exact, fully-prefixed** strings are the
authoritative names the mechanism spec's F1 list must use verbatim (the
`assignment.`/`assign.` prefix is part of the name, as in `rules.ex` `@facts`):
`assignment.independent_verdict_kinds`, `assignment.cross_harness_verdict_kinds`,
`assignment.cross_provider_verdict_kinds`, `assignment.produced_verdict_kinds`,
`assign.declared_files_overlap_open`. The pre-existing `assignment.verdicts`
(check-tier, direct-on-`A`, unchanged) is **not** a P3 addition. There is **no**
`verdict_kinds_any` fact (the earlier union fact is removed — the union of
direct-on-`A` and review-link verdicts is precisely the laundering path
invariant 6 forbids).

| fact | type | definition & nil cases |
|---|---|---|
| `assignment.independent_verdict_kinds` | list(string) | DISTINCT `verdict_kind` over `commissioned_review_authors/3` — author-independent review-link verdicts (invariants 6, 6b: author is `R`'s holder and author ≠ `A`'s holder; user and third-session verdicts excluded; `R`'s opener is irrelevant). Present `[]` when the assignment exists with no qualifying verdict (`not_in` fires — the gate); nil when `$assignment` nil. |
| `assignment.cross_harness_verdict_kinds` | list(string) | DISTINCT `verdict_kind` over `commissioned_review_authors/3` rows whose stamped `by_harness` ≠ the assignment's stamped `holderHarness` (both non-null). Present `[]` when the assignment exists (with `holderHarness` stamped) but no qualifying cross-harness verdict; **nil** when `$assignment` nil **or** the assignment's `holderHarness` stamp is NULL (a legacy/unstamped holder → the fact is nil → ungated, per invariant 7 / F5 — never present `[]`). |
| `assignment.cross_provider_verdict_kinds` | list(string) | as cross-harness, comparing stamped `by_provider` against stamped `holderProvider`; **nil** when `holderProvider` NULL. |
| `assignment.produced_verdict_kinds` | list(string) | DISTINCT kinds of `producer`-stamped verdicts filed **directly on** this assignment (`produced_verdict_kinds/2`, §3.4 — keys on the `producer` column, independent of the review link). The strong mechanical rung. Present `[]` when the assignment exists with no produced verdict; nil when `$assignment` nil. |
| `assign.declared_files_overlap_open` | bool | **advisory/observational only** (enforcement is the transactional in-handler check, §3.3). true iff the **`assign` call's** `files` param declares any path also declared by some **open** assignment (`open_assignments_touching/2`); false when it declares files but none overlap; **nil** when the call carries no `files` param, is not the `assign` verb, or the param is malformed. nil-never-fires. |

**Facts P3 does NOT define (re-homed by the smoke-set / mechanism F1).** The
enforcement smoke-set assigns two further facts to a P3-era class that this spec
**does not** define: **hand-off-field presence** (the "hand-off states what is
passed / expected back / whom to wake" arg-presence check) and
**`changes-requested` count** (the "two failed attempts → revert" derived
count). Neither is in the P3 fact set above. They are named here explicitly so
the smoke-set re-homes them (marked pending-elsewhere) rather than expecting P3
to carry them.

### 4A. Independent-review deny-half (the flagship)

The commissioned reviewer (the holder of `R`) files `reviewed-clean` on **its
own** review assignment `R`, where `R.reviewsAssignmentId = A.id`, and is not
`A`'s holder (invariants 6, 6b); the fact surfaces it on `A`. Who opened `R`
does not affect author independence. Cross-model is `cross_harness` (a `codex`
reviewer over a `claude` producer, or vice-versa).

```toml
[[rule]]
name = "coder-completion-needs-independent-review"
verb = "attest"
deny_when = [
  { fact = "attest.kind", op = "eq", value = "completion" },
  { fact = "assignment.holder_archetype", op = "eq", value = "coder" },
  { fact = "assignment.cross_harness_verdict_kinds", op = "not_in", value = ["reviewed-clean"] },
]
text = "completion needs a reviewed-clean verdict from a cross-model reviewer that is not the holder"
```

`not_in` on a present `[]` (no qualifying review) fires → deny.

**§4A gate policy — the completion gate's independence axis.** With 6b now
author-only, the self-commissioned-review path is closed not by the invariants
but at the COMPLETION GATE by the axis the ORG SELECTS IN RULE CONFIG (the value
is config, not law text — so a change is a config edit, never a canon
re-amendment). Two arms:

- **REQUIRE:** the gate reads `cross_harness_verdict_kinds` → the self-review,
  same-family-review, direct-on-`A`, and shell-assignment paths stay closed by
  invariants 6/6b, AND the self-commissioned-review path is closed by requiring
  the commissioned reviewer to be a harness the producer does not control.
- **RECORD:** the gate reads `independent_verdict_kinds` (author-only) and
  SURFACES `cross_harness_verdict_kinds` (surfaces = the fact is QUERYABLE on
  the assignment; no stamp is written on an allowed completion) — the
  self-commissioned-review path is an openly-recorded residual, not closed.
  Same rule shape, weaker axis, its choice.

### 4B. Tests-pass and real-run deny-halves (mechanical producer)

```toml
[[rule]]
name = "coder-completion-needs-produced-tests"
verb = "attest"
deny_when = [
  { fact = "attest.kind", op = "eq", value = "completion" },
  { fact = "assignment.holder_archetype", op = "eq", value = "coder" },
  { fact = "assignment.produced_verdict_kinds", op = "not_in", value = ["tests-passed"] },
]
text = "completion needs a tests-passed verdict produced by the build runner, not self-attested"
```

`produced_verdict_kinds` counts only `producer`-stamped rows, so an agent that
files its own `tests-passed` (author = holder or even a colluding non-holder)
does **not** satisfy it — only the §5 runner does. The real-run gate is the same
rule with `real-run-passed`. N required kinds = N rules (check-tier's
composition; each missing kind denies by its own name).

### 4C. Why cross-harness/cross-provider and not "model family"

The substrate's neutral truth is the session columns it stores: `harness`
(`claude`|`codex`) and `provider` (`anthropic`|`openai`). "Family" as a grouping
of distinct models under one provider (opus vs haiku both `anthropic`) is a
product/engineering taxonomy — it belongs to the org, and the org cannot express
it in the literal-only algebra anyway. The guidance's "different model family,
or a higher thinking level when only one family is available" is a **judgment
the orchestrator makes**, not a mechanical gate (guidance-spec §6: that fallback
is advisory, a judge/human call). The substrate therefore exposes the two
comparisons over its own columns; the org's rule picks the axis it will enforce
mechanically, and keeps the finer family/level logic in guidance. Exposing a
substrate `cross_model_verdict_kinds` over the free-string `model` column was
rejected: it would force the substrate to own a model-grouping policy it must not
own, and bare model-string inequality (`opus` ≠ `haiku`) is not what "family"
means.

### 4D. Files-touched overlap — enforced in the handler; the fact is advisory

The **authoritative** overlap gate is the transactional constitutional refusal
in the `assign` handler (§3.3, `files_overlap`) — race-free because the read and
insert share one serialized transaction (F13). The rules-tier fact below is
**advisory/observational only**: an org may write it to *observe* overlaps in the
event log or to layer an additional statute-tier signal, but it is not the
race-safe enforcement and must not be presented as such. Because a rules-tier
check runs *before* the handler transaction (dispatch chokepoint), it is subject
to TOCTOU and is deliberately demoted here.

```toml
# ADVISORY ONLY — the race-safe gate is the in-handler check (§3.3).
[[rule]]
name = "observe-overlapping-open-assignments"
verb = "assign"
deny_when = [
  { fact = "assign.declared_files_overlap_open", op = "eq", value = true },
]
text = "another open assignment already declares one of these files; order the work, do not parallelize it"
```

Undeclared assigns (no `files` param) → fact nil → never fires; and they are also
not subject to the in-handler check (opt-in by declaration). The observed-set
(git-diff) gate is future (§2).

### 4E. Fact resolution (implementation notes for Lane B)

- The three independence facts (`independent_/cross_harness_/cross_provider_
  verdict_kinds`) call `Assignments.commissioned_review_authors/3` **once**
  (passing `$assignment.holder_key`; it selects linked verdicts authored by
  `R`'s holder when that author is not `A`'s holder, without filtering on `R`'s
  opener; cache the qualifying author list under an
  internal `$verdict_authors` dependency keyed off `$assignment`, mirroring
  `$target`/`$assignment`) and derive the three DISTINCT-kind projections in
  Elixir. `independent_verdict_kinds` = all qualifying kinds. `cross_harness` /
  `cross_provider` compare each author's stamped `by_harness`/`by_provider`
  against `$assignment`'s stamped `holder_harness`/`holder_provider`, and are
  **nil when that holder stamp is NULL** (do not compute over an unstamped
  holder — return nil, never present `[]`; F5). One DB round trip, three facts.
- `produced_verdict_kinds` calls `Assignments.produced_verdict_kinds/2`
  (direct-on-`A`, `producer`-stamped) — a separate read, not the review-link one.
- `assign.declared_files_overlap_open` reads `call.params[:files]`; on a present
  well-formed non-empty list it dedupes paths then calls
  `open_assignments_touching/2` and returns the non-empty test as a bool;
  empty/absent/malformed → nil.
- Every fact is wrapped by the existing `compute_fact_safely` catch → a raising
  join denies `rule_error` (fail closed), never grants.

---

## 5. Producer verbs (Lane C) — SUPERSEDED

Superseded 2026-07-29 by `verification-papertrail-v1.md` (#90 re-ruling):
the substrate enforces by requiring papertrails and never by producing them,
so the producer verbs, the `producer_jobs` runner, and §4B's producer-backed
deny-halves are deleted — verification is an org statute requiring an attest
plus a recorded results artifact, with a remedy summoning inference. The
text below is retained as the record of the deleted subsystem; everything
else in this spec (observables, provenance stamps, review-of) stands.

Two substrate verbs emit **non-self-attested** verdicts. They are the mechanical
producers of the strength ladder: the substrate runs the check itself and files
the verdict stamped as its own producer, so the fact is anchored to a real
process outcome rather than an agent's word.

### 5A. The command is committed config, never a verb param

**Ruling (opine-pass): the command a producer runs is sourced from committed org
config in the identity repo — it is never a verb param and never falls back to
one.** A param-sourced command hands the caller the very lever the producer
exists to remove: the agent whose completion is gated could pass `true` (or any
no-op) as `command` and receive a substrate-stamped `tests-passed`. The stamp
would then certify a checkbox rather than a run — the exact measure-becomes-target
failure the tuning doc names as an institutional expectation (`self-tuning-rails-
core-FUTURE.md` §6f). Committing the command as law makes it git-tracked,
attributable, and **review-gateable** (a weak command is a diff a reviewer can
catch), and takes the choice of what "tests passed" means out of the hands of the
party being measured.

**Config home and key.** The command set lives in the org's identity repo as
`identity/producers.toml`, loaded at boot alongside the rails
(`Producers.load!(base_dir)` in `Gateway.children`, the `Rails.load!`/`Rules.load!`
precedent). **Keyed by producer kind, org-wide** — one `tests` command and one
`smoke` command per org:

```toml
# identity/producers.toml
tests = "mix test --warnings-as-errors"
smoke = "bin/smoke --against staging"
timeout_ms = 600000   # optional; per-run wall clock, default 600000
```

The optional `timeout_ms` key is the **org-tunable** source of the producer
run's wall-clock box (default 600000). It is config, not a verb param — the same
"party being measured does not set the measure" rule.

**`producers.toml` is the static registry the mechanism's F1 satisfiability
checker consumes (F4).** F1 decides whether a `produced_verdict_kinds` gate is
satisfiable by reading this file: a produced verdict kind is producible **iff**
its producer kind has a configured command. The shape F1 loads is exactly the one
above — a top-level table mapping the fixed producer keys `tests` → `tests-passed`
and `smoke` → `real-run-passed` to command strings, plus the optional
`timeout_ms` integer. No other keys. F1 does **not** treat generic agent
assign/attest capability as a producer (that would make almost every kind
theoretically producible and defeat the `missing-producer-unsatisfiable` check);
the only mechanical producers v1 registers are the two whose command keys are
present in `producers.toml`.

Justification for org-wide-by-kind (one sentence): in v1 an org runs one codebase
under one workdir convention (`gateway.ex` `session_workdir/2`, a single default
archetype), so "what a build/smoke run is" is a property of that codebase — org
law, one command per producer kind — not something that varies per work-item,
per archetype, or per caller. (Per-project keying via the work-item's spec-ref
project is the additive future if an org ever hosts multiple codebases — §9;
not built here.)

**Miss behavior — fail loudly, never fall back.** If the invoked producer kind
has no configured command, the verb refuses `producer_unconfigured` (403-class),
files nothing, and emits a `producer_failed` legibility event; it does **not**
accept a command from anywhere else. An unconfigured producer is a loud denial,
not a silent no-op.

### 5B. Shared shape — ASYNC, never an inline dispatch handler (F12)

A producer command can run for minutes; running it inline in a Dispatch handler
would block the dispatch path, violating dispatch's own invariant that long work
goes through the lane/ledger, never inline. **The producer verbs are therefore
accept-and-enqueue: the handler validates and queues a job, returns immediately,
and the job runs asynchronously on the gateway host, landing the fact on
completion.** Both verbs share one implementation in a new module
`Tightbeam.Producers` (`lib/tightbeam/producers.ex`), differing only in their
producer token, verdict kind, and config key.

**A durable jobs table, NOT `wire_idempotency` (F6).** Producers do not touch
`wire_idempotency` — its CHECK (`spawn|retire|wake|assign`) stays closed and Lane
C authorizes no `idempotency.ex` migration. Producers get their **own** durable
table, `producer_jobs`, owned by Lane C (created by `Producers.ensure_schema`).
It **persists the acting principal and the frozen author-family stamps** so the
verdict can be stamped correctly after async execution or a boot-recovered
re-run, when the accepting session is no longer available to read (F5/F6):

```
producer_jobs (
  id          TEXT PRIMARY KEY,    -- pj_ + uuid4; the job handle / idempotency seam
  assignmentId TEXT NOT NULL REFERENCES assignments(id),
  kind        TEXT NOT NULL,       -- "tests" | "smoke" (the producer key)
  command     TEXT NOT NULL,       -- the resolved committed command (recorded)
  state       TEXT NOT NULL CHECK(state IN ('queued','running','done','failed','cancelled')),
  bySession   TEXT,                -- acting principal (frozen at accept): session key, or
  byUser      TEXT,                --   user id — exactly one non-null (attribution source)
  byHarness   TEXT,                -- accepting session's harness, FROZEN at accept (NULL if user)
  byProvider  TEXT,                -- accepting session's provider, FROZEN at accept (NULL if user)
  timeoutMs   INTEGER NOT NULL,
  startedAt   INTEGER
)
```

**Accept (the Dispatch handler, synchronous, fast):**
- Wire params: `{ assignmentId }` only. No `command`, no `idempotencyKey`.
  Registered in `@agent_verbs`; runs through Dispatch, so statutes gate the
  producer verbs too if an org wants.
- Authorization: any session or user principal (the check-tier verdict-filer
  rule). Process denied. Unknown assignment → `unknown_assignment`. Closed →
  `assignment_closed`. Unconfigured kind → `producer_unconfigured` (§5A).
- On success, in **one serialized transaction**: if an **active**
  (`queued|running`) `producer_jobs` row already exists for this
  `(assignmentId, kind)`, return **its** `id` (idempotent — the job id is the
  seam, F6); else insert a new row `state='queued'` with the resolved command,
  `timeoutMs`, and **the frozen provenance** — `bySession`/`byUser` from the call
  principal and, when the principal is a session, its **then-current**
  `byHarness`/`byProvider` read once and stored. Return `{ queued: jobId }`. The
  handler does **not** run the command. Every stamp the eventual verdict carries
  is now on the row; nothing is re-read from `sessions` later.

**Run (the async worker, off the dispatch path — GATEWAY HOST ONLY, F10):**
- v1 executes producer commands **only on the gateway host** (the machine the
  gateway runs on), in the holder's gateway-host-local workdir. A holder placed
  on a **remote** host is a **named deferred gap**: running its remote build is
  future work behind `Placement.run_on_host` (below), out of v1 scope. v1 either
  serves gateway-host holders or the producer is not usable for that holder yet;
  it never silently runs the wrong checkout.
- A `Tightbeam.ProducerRunner` (a GenServer added to the gateway tree) drives the
  durable queue: it claims a `queued` row via CAS
  (`UPDATE producer_jobs SET state='running', startedAt=? WHERE id=? AND
  state='queued'`, `changes = 1` wins) and runs it as a task under a
  `Tightbeam.ProducerSupervisor` (`DynamicSupervisor`, next to
  `AdapterSupervisor`). The **`producer_jobs` table**, not the supervisor, is the
  durable record. This is P3's own machinery; it does not depend on the P4 script
  runtime.
- **Boot recovery (fail-closed on orphans):** at gateway start, `ProducerRunner`
  requeues rows left **`queued`** (never claimed) back to `queued` — those never
  ran. A row left **`running`** (its worker died with the gateway — orphaned) is
  **NOT requeued**: it transitions `running → failed` (the existing terminal guard
  `state='running'`) with a `producer_failed` (`orphaned`) event. Requeueing an
  orphaned `running` job would re-run an external command that **may already have
  executed** before the crash — and a "real run" (smoke) is not guaranteed
  idempotent, so a blind re-run could double a side-effecting execution. Instead
  the gate stays unsatisfied and the holder re-runs the producer verb
  **deliberately** (a fresh accept, a new job). No fencing tokens, no execution
  ledger — the state machine's fail-closed transition is the whole mechanism.
- **Guarantee scope (stated plainly):** `producer_jobs` guarantees **at-most-one
  terminal verdict** per job (the `running → done` CAS + in-txn insert, §terminal
  transitions), **not** at-most-one external command execution. The
  orphaned-`running` → `failed` rule above is exactly what keeps a crash from
  silently doubling the *command* — the substrate never re-runs a possibly-executed
  command on its own; re-execution is always a deliberate new verb call.
- **Pinned seams:**
  - workdir — `Placement.holder_workdir(config, holder_session) :: path`
    (promote the logic currently private in `gateway.ex` `session_workdir/2` to a
    public `Placement` function; Lane C owns this move). v1 resolves the
    gateway-host-local path.
  - execution — v1 runs the command **locally on the gateway host** as a
    supervised OS process (a `Port`/`System.cmd`-class local run): `argv =
    ["sh", "-lc", command]`, `cwd` the workdir, a **minimal env** (no operator
    secrets; only what the workdir bootstrap exposes), the `timeoutMs` wall-clock
    box, and a process-group kill for cancellation/timeout. **`Placement.run_on_host(host,
    argv, opts)` is the DEFERRED remote-execution seam — named, NOT built in v1;**
    when it lands, remote-holder producers ride it behind this same job/verb
    interface.
  - write — `Assignments.insert_producer_verdict_in_txn/2` (§3.4), the **only**
    path that writes `producer`/`producerCommand`, called **inside the CAS
    transaction** with the job row's frozen `bySession`/`byUser`/`byHarness`/
    `byProvider`.
- **Terminal transitions — each a single guarded `UPDATE producer_jobs SET
  state=? WHERE id=? AND state IN (<allowed>)` CAS (`changes = 1` wins, else the
  transition is a no-op), so success, failure, timeout, and cancellation never
  double-apply or race each other. The allowed prior states are per-transition,
  not universal:**
  - exit 0 → CAS `running → done` (guard `state='running'`), and **in the same
    transaction, only if that UPDATE changed a row**, the worker calls
    `insert_producer_verdict_in_txn/2` (verdict `kind = "verdict"`, `verdictKind =`
    the verb's kind, `producer =` the verb's token, `producerCommand =` the row's
    `command`, stamps from the frozen columns). If the CAS changed no row (a cancel
    already moved it to `cancelled`), the transaction commits nothing and **no
    verdict is filed.** Results land ONLY via `insert_producer_verdict_in_txn`, and
    only on a winning `running → done`.
  - non-zero exit, timeout (per `timeoutMs`), or host/spawn failure → CAS
    `running → failed` (guard `state='running'`); on a winning UPDATE **file no
    verdict** and emit a legible `producer_failed` lifecycle event (subject the
    assignment id; detail job id + kind + command + exit/timeout/fail). Gate stays
    denied — fail closed.
  - **cancellation** — reached through the pinned `cancel-producer-job` verb
    (below), it is CAS `queued|running → cancelled` (guard
    `state IN ('queued','running')` — its own two-state guard, since a job may be
    cancelled **before it is ever claimed**) plus, when the prior state was
    `running`, a best-effort process-group kill; the state transition is
    authoritative, the kill never blocks it. On a winning CAS it emits a
    `producer_failed` lifecycle event (detail `cancelled`). A cancel that wins the
    CAS before `running → done` guarantees no verdict is filed (previous bullet).
- The `command` on the job row, copied to `producerCommand` on the verdict, makes
  every run auditable from data.

**The `cancel-producer-job` verb (the pinned cancel seam).** Cancellation is not
an ambient capability — it is a dispatch verb owned by Lane C:
- Wire params: `{ jobId }`. Registered in `@agent_verbs`; runs through Dispatch.
- Authorization: the **holder of the job's assignment**, or the **admin axis**
  (the same owning-user admin check the admin-gated verbs use). Any other
  principal → `forbidden`; a `process` principal → denied; nil →
  `principal_required`. An unknown `jobId` → `unknown_producer_job`.
- Handler: executes the two-state CAS `UPDATE producer_jobs SET state='cancelled'
  WHERE id=? AND state IN ('queued','running')`. On a winning UPDATE
  (`changes = 1`): if the prior state was `running`, best-effort process-group
  kill the local run; emit the `producer_failed` (`cancelled`) event; return
  `{ cancelled: jobId }`. On no-op (`changes = 0` — the job is already terminal
  `done`/`failed`/`cancelled`): return `{ cancelled: jobId, noop: true }`, kill
  nothing, file nothing. Retiring the holder session drives the same CAS through
  this handler's internal path (not a separate mechanism).
- CLI: `tightbeam cancel-producer-job <jobId>`.

### 5C. `run-tests` / `run-smoke`

`run-tests`: producer token `"build"`, verdict kind `"tests-passed"`, config key
`tests`. Emits `tests-passed` only on exit 0.

`run-smoke`: producer token `"smoke"`, verdict kind `"real-run-passed"`, config
key `smoke`. The committed `smoke` command runs the artifact **against real
inputs** — the substrate supplies execution + attestation + the record of the
command; the org supplies, in reviewable law, what "a real run" is. Emits
`real-run-passed` only on exit 0.

### 5D. Honest strength assessment (§6 ladder)

- **What the producer stamp prevents:** an agent cannot make
  `produced_verdict_kinds` contain `tests-passed`/`real-run-passed` by filing an
  ordinary verdict — no agent-facing verb writes `producer`. The strong fact
  reads only substrate-run outcomes.
- **What it does NOT prevent:** the producer runs a **committed-config command**.
  If that command is weak (a `true`-equivalent, a build that does not actually
  run the tests, a smoke that does not touch real inputs), the stamp certifies
  "the substrate ran *this* command and it exited 0," not "the software works."
  The strength is `mechanical` — reality touched the command — but it is only as
  strong as the command the org committed and the containment it ran in. What
  config-sourcing **does** buy over a param: the caller being measured no longer
  chooses the command, so a weak check is a reviewable diff in `producers.toml`
  (attributable, revertable) and the actual run is recorded in `producerCommand`
  on the row — a weak or wrong command is visible without forensics, not a
  per-call forgery. This is the guidance-spec §6 ladder honestly:
  mechanical-producer beats self-attested and beats independent-judge for "it
  actually ran," but **exogenous verification** (the user, production) still sits
  above it, and a judge-passed/producer-passed item that fails reality is a
  finding about the command/judge that feeds the tuning system. P3 does not
  sample-and-reverify (that is T-B).
- **P4 note:** the contained, resource-capped execution the guidance-spec §6
  describes for rail scripts is the same runtime this producer wants. P3 runs the
  command as an async supervised **local** job on the gateway host (§5B, F10) so
  the deny-half is provable now; both remote execution (`Placement.run_on_host`)
  and P4's contained script runtime are deferred, and either MAY later re-host
  execution behind the same job/verb seams without
  changing the fact, the stamp, or the accept-and-enqueue shape.

### 5E. Files-touched — declared, and why not observed here

`run-tests`/`run-smoke` do not populate `assignment_files`. The **declared** set
(§3.3) is the P3 files-touched observable, set by the holder at `assign` and
authoritative for the commission-time overlap gate (§4D) and the own-worktree
intent. Its **staleness semantics**: it is a *declaration*, true at assign time
and never re-derived — if the holder touches a file it did not declare, the
declared set does not learn it. The **observed** set (git diff of the lane's
branch, the truth of what was touched) is the stronger, later producer: it needs
a branch identity per assignment and the P4 runtime to run `git diff` in
containment, and it is out of scope here (§2). P3 ships declaration; the roadmap
tracks observation as the strengthening follow-on.

---

## 6. Observable → mechanism table (decision-complete)

| # | Observable | Registered fact vs script | Producer / source of truth | Deny-half rail it unlocks | Strength (guidance §6) |
|---|---|---|---|---|---|
| A | Review-of relation | schema (typed column `reviewsAssignmentId`) + holder-family stamps, not a fact | declared at `assign` via `reviews`; holder family stamped at `assign` | (enables B) | — (structure) |
| B | Verdict-author independence | **registered** facts `independent_/cross_harness_/cross_provider_verdict_kinds` | **commissioned-reviewer-only through the link** (invariants 6, 6b: author is `R`'s holder and not `A`'s holder, no user/third-session verdicts, never direct-on-`A`; `R`'s opener is irrelevant); author family = verdict's stamped `byHarness/byProvider` vs assignment's stamped `holderHarness/holderProvider` (invariant 7), with the completion gate selecting `cross_harness` under REQUIRE | `cross_harness_verdict_kinds not_in ["reviewed-clean"]` on `attest completion` | strong (independent judge) |
| C | Build producer (tests-pass) | **registered** fact `produced_verdict_kinds` (direct-on-`A`, `producer`-stamped) + provenance/family columns | `run-tests` verb (accept-and-enqueue) runs the committed `tests` command async, `insert_producer_verdict_in_txn` stamps `producer="build"` + `producerCommand` | `produced_verdict_kinds not_in ["tests-passed"]` on `attest completion` | strong (mechanical) |
| D | Smoke producer (real-run) | **registered** fact `produced_verdict_kinds` (shared) + provenance/family columns | `run-smoke` verb runs the committed `smoke` command async, `producer="smoke"`, kind `real-run-passed` | `produced_verdict_kinds not_in ["real-run-passed"]` | strong (mechanical) |
| E | Files-touched (declared) | **transactional in-handler check** (authoritative); `assign.declared_files_overlap_open` fact is advisory only | declared at `assign` via `files` param → `assignment_files` | in-handler `files_overlap` refusal on `assign` (race-free); advisory fact for observation | mechanical (declared; forgeable by omission) |

**Every P3 observable is a registered fact (or the schema a registered fact
joins over), not a script.** Justification (D1 = hybrid): each is a hot,
terminating, auditable DB join, and each is the exact thing a P3 deny-half must
key on *before* the P4 script runtime exists — so the deny-halves are provable at
P3. The elaborate/expensive checks D1 routes to scripts (judge gates, git-diff
observation, remedies) are explicitly deferred (§2). The producer *verbs* are
real substrate mechanism either way; only their execution engine is a candidate
for P4 re-hosting (§5D).

---

## 7. Lane partition (honest ordering)

**Lane A is a hard prerequisite; Lanes B and C parallelize only after A merges.**
The round-1 "three fully-parallel lanes" claim was false (F16): B's facts need
A's columns and reads, C's producer job needs A's `insert_producer_verdict_in_txn` API,
and the `assign --reviews/--files` CLI needed for A's features lives in C's CLI
files. The `$assignment`-feeding SELECT lives in **rules.ex** (Lane B), not
`assignments.ex` — so A does *not* widen it; A only adds the columns B's widened
SELECT reads. The partition below is disjoint in files but **sequenced**:
A → then B ∥ C.

### Lane A — schema, storage, reads, producer-insert API (FIRST, blocking)
- **Files:** `lib/tightbeam/assignments.ex` (+ `test/tightbeam/assignments_test.exs`).
- **Builds:** the `reviewsAssignmentId` + `holderHarness` + `holderProvider`
  columns and `reviews`/holder-family capture in `assign` (§3.1); the `producer`
  + `producerCommand` + `byHarness` + `byProvider` columns via the full-shape
  version-aware FK-safe rebuild (§3.2, replacing `ensure_attests_shape/1`'s
  detection); the `assignment_files` table, `files` param handling with silent
  path-dedupe, **and the transactional `files_overlap` refusal in the assign
  handler** (§3.3); the public reads and the `insert_producer_verdict_in_txn/2`
  producer-stamping API (§3.4). All server-side in one module.
- **Touches no other module.** Does **not** touch `rules.ex` (the `$assignment`
  SELECT is Lane B's).

### Lane B — registry facts (after A)
- **Files:** `lib/tightbeam/rules.ex` (+ `test/tightbeam/rules_test.exs`), and the
  **statute examples** as authored rails in the org identity bundle
  (`identity/rails/*.toml` per guidance-spec §1 — not source-tree files).
- **Builds:** the five `@facts` entries + `compute_fact` clauses (§4), the
  `$verdict_authors` cached dependency, **the widening of the `$assignment`
  SELECT** to read `holder_harness`/`holder_provider` (this SELECT lives here in
  rules.ex, not in Lane A), the moduledoc list-fact amendment. **No
  validator/`compare` change.**
- **Depends on:** Lane A's columns + `commissioned_review_authors/3`,
  `produced_verdict_kinds/2`, `open_assignments_touching/2` (§3.4). Codes against
  those pinned signatures; integrates after A merges.

### Lane C — producer verbs + jobs + all CLI (after A; parallel with B)
- **Files:** new `lib/tightbeam/producers.ex` (+ test), owning the
  `producer_jobs` table (with frozen-provenance columns), `Producers.ensure_schema`,
  the `ProducerRunner` queue worker **and its local gateway-host execution**, and
  the config loader; `lib/tightbeam/placement.ex` (the new public
  `holder_workdir/2` seam, §5B — `run_on_host/3` is the deferred remote seam,
  **not built in v1**); `lib/tightbeam/gateway.ex` (`run-tests`/`run-smoke`
  handler registration **plus the `cancel-producer-job` handler**, `Producers.load!`
  + `Producers.ensure_schema` boot wiring, `ProducerSupervisor` + `ProducerRunner`
  added to `children/1`); `lib/tightbeam/wire/router.ex` (`@agent_verbs`, **three**
  additive entries: `run-tests`, `run-smoke`, `cancel-producer-job`); **all
  `cli/src/*.rs` changes** — the three producer subcommands (`run-tests`,
  `run-smoke`, `cancel-producer-job`) **and** the `assign --reviews`/`--files`
  flags that make Lane A's features reachable; and the `identity/producers.toml`
  config example.
- **Builds:** the committed-config loader + resolution + `timeout_ms` (§5A); the
  `producer_jobs` durable table (frozen provenance) + accept-and-enqueue verbs +
  `ProducerRunner` local-execution worker with boot recovery + CAS terminal
  transitions + the `cancel-producer-job` verb (holder/admin-gated two-state CAS,
  §5B); the `producer_unconfigured` refusal; the `producer_failed` event; the CLI.
- **Depends on:** Lane A's `insert_producer_verdict_in_txn/2` (§3.4) and the
  `assign` param handling. Codes against those signatures; integrates after A.

Lane A ∩ B ∩ C files: **empty** (B owns rules.ex; C owns producers/placement/
gateway/router/cli; A owns assignments.ex). But the **ordering is A first, then
B ∥ C** — this is not three-way parallel from a cold start.

**Cross-phase file contention (stated so later-phase lane claims stay honest):**
P4 and P5 both edit `rules.ex` and `dispatch.ex`; P6 folds the turn-end sweep
into `Supervision.evaluate` (no separate `RailSweep` GenServer) and edits
`rules.ex` again. Lane B's `rules.ex` work must land before those phases touch
the same file; P4/P5/P6 are sequential on `rules.ex`/`dispatch.ex`, not parallel
with each other or with a still-open Lane B.

---

## 8. Acceptance contract (per lane, keyed to conformance classes)

Keyed to the smoke-set taxonomy (`rails-and-guidance-roadmap.md` P2.5): **C3**
(count/producer fixtures) and **C4** (provenance). Each clause is decidable from
a test or a run.

### Lane A
- `reviews` links + holder stamp: assign `R --reviews A` sets
  `R.reviewsAssignmentId = A.id`; `reviews` naming an unknown assignment refuses
  `unknown_review_target` and no `R` row survives (transaction abort proven);
  absent `reviews` → NULL. Every assignment records `holderHarness`/
  `holderProvider` from the holder session at `assign`; the stamps never change
  when that session later re-tunes (temporal soundness, invariant 7).
- Full-shape FK-safe rebuild (F15): detection skips **only** when the stored DDL
  carries all four new columns (`producer`, `producerCommand`, `byHarness`,
  `byProvider`) **and** the new CHECKs; a partial shape (e.g. `producer` present
  but `byHarness` absent) triggers the rebuild. Proven from **three** starting
  DBs in one copy each — a bare attest-v1 table (no `verdictKind`/`byUser`), a
  check-tier table, and a partial-P3 table — each reaching the full shape with
  `foreign_key_check` zero rows, all prior rows readable and valid, new columns
  NULL; idempotent on re-run; fresh DDL carries the full shape. CHECKs:
  `producer`/`byHarness`/`byProvider`-non-null with `kind != 'verdict'` rejected;
  `producerCommand` without `producer` rejected.
- `assignment_files` + overlap: `assign … --files [a,b]` inserts two rows in the
  assignment's transaction; a repeated path is **deduped silently** (not
  `invalid_files`); a malformed entry → `invalid_files`, no assignment row
  survives; absent `files` → zero rows; verbatim storage (a `..` or absolute path
  stored unchanged). **Transactional overlap:** an `assign` declaring a path an
  open assignment already declares refuses `files_overlap`, no row survives; and
  **two concurrent overlapping assigns yield exactly one committed row** — the
  loser gets `files_overlap`, proving the read+insert share one transaction (the
  F13 race test).
- Provenance writers (F5): `insert_producer_verdict_in_txn/2` is the **only** writer of
  `producer`/`producerCommand` — a direct verdict via ordinary `attest` leaves
  those two NULL; but the **ordinary verdict insert stamps `byHarness`/
  `byProvider`** from the filing session, so an ordinary reviewer verdict carries
  `byHarness`/`byProvider` (and can satisfy `cross_harness`) while its
  `producer`/`producerCommand` stay NULL. A user-filed verdict leaves `byHarness`/
  `byProvider` NULL.
- Reads (F11): `commissioned_review_authors/3` returns **only** verdicts that are
  through-link (`R.reviewsAssignmentId = A`), authored by `R`'s holder, and whose
  author ≠ `A`'s holder — proven by a matrix
  that a direct-on-`A` verdict, a third-session verdict on `R`, a **user** verdict
  on `R` are each **absent** from the result, while a verdict by `R`'s holder on
  an `R` self-commissioned by `A`'s holder is **present**; stamped
  `by_harness`/`by_provider` correct per row.
  `produced_verdict_kinds/2` returns direct-on-`A` producer-stamped kinds;
  `declared_files/2` and `open_assignments_touching/2` correct incl. empty and
  no-overlap cases.

### Lane B (C3 + C4)
- Per-fact presence/nil matrix: each `assignment.*` fact is nil for a
  missing/non-string `assignmentId` and for an unknown assignment (shared
  `$assignment`); `independent_verdict_kinds` and `produced_verdict_kinds` are
  present `[]` for an existing assignment with no qualifying verdict (and `not_in`
  **fires** on the `[]`); `cross_harness`/`cross_provider` are present `[]` for an
  existing assignment **whose `holderHarness`/`holderProvider` is stamped** but
  with no qualifying cross-family verdict, and **nil** when that holder stamp is
  NULL (legacy/unstamped → ungated, F5 — asserted that it does **not** fire).
  `assign.declared_files_overlap_open` is nil for absent/malformed `files`, false
  for declared-but-disjoint, true for declared-overlap.
- **Anti-laundering + commissioned-reviewer (invariants 6, 6b):** none of a
  `reviewed-clean` filed directly on `A`, a third-session verdict on a linked
  `R`, or a **user** verdict on `R` appears in
  `independent_/cross_harness_verdict_kinds`; a verdict authored by `R`'s holder
  on an `R` linking to `A` does appear in `independent_` regardless of who opened
  `R`, and appears in `cross_harness_` exactly when its stamped harness differs
  from `A`'s holder harness. The full matrix (correct/wrong link ×
  holder/third/user author on `R` × producer-/non-producer-opened `R` ×
  same/cross harness) resolves as specified, with opener identity never changing
  the result.
- **Temporal soundness (invariant 7):** a `cross_harness` result computed from
  stamped `byHarness`/`holderHarness` does **not** change when either the author
  or the holder session re-tunes its harness/provider after filing.
- **C4 provenance:** `produced_verdict_kinds` contains a kind **iff** a
  `producer`-stamped verdict of that kind is filed directly on the assignment; an
  identically-named agent-filed verdict (`producer` NULL) does **not** appear. A
  same-harness commissioned review-link `reviewed-clean` is present in
  `independent_` but absent from `cross_harness_`.
- **C3 gate end-to-end:** the §4A rail denies `attest completion` (rule_denied,
  one `denied` event, no attest row, assignment open, handler not invoked) while
  no cross-harness review-link `reviewed-clean` exists, and **allows** it once
  such a verdict is filed on a reviewing assignment; the §4B rail denies until a
  `run-tests`-produced `tests-passed` exists. Load-time typing: `eq` on a list
  fact → load error; `in/not_in` value validation; the overlap fact is `bool`
  (eq/ne). Laziness and `rule_error`-on-raise preserved. **There is no
  `verdict_kinds_any` fact** (its absence is asserted).

### Lane C (C3 + C4)
- Accept-and-enqueue (F12): `run-tests` returns `{queued: jobId}` from the
  Dispatch handler **without** running the command inline, and inserts one
  `producer_jobs` row `state='queued'`; the verdict lands only after the async
  worker completes (proven by observing the queued return, then the later
  verdict). The verb takes **only** `assignmentId` (no `command`, no
  `idempotencyKey`); the command and `timeoutMs` come from `identity/producers.toml`.
  On exit 0 the worker CAS-transitions `running → done` and (only on the winning
  CAS, same transaction) calls `insert_producer_verdict_in_txn/2` → one verdict row `kind=verdict`,
  `verdictKind=tests-passed`, `producer=build`, `producerCommand=` the job's
  recorded command, `byHarness`/`byProvider` from the job's **frozen** columns;
  the row makes `produced_verdict_kinds` contain `tests-passed` and satisfies the
  §4B gate.
- **Frozen provenance (F5/F6):** the verdict's `bySession`/`byHarness`/`byProvider`
  equal the values captured on the `producer_jobs` row **at accept**, proven by
  re-tuning (or retiring) the accepting session between accept and completion and
  asserting the stamps are unchanged; a boot-recovered re-run stamps identically
  from the same frozen columns.
- Jobs table & idempotency (F6): does **not** touch `wire_idempotency` (asserted:
  no `run-tests`/`run-smoke` operation is written there). A second `run-tests`
  for the same `(assignmentId, kind)` while a job is `queued`/`running` returns
  the **existing** `jobId` and inserts no second row (the job id is the seam).
- Recovery (fail-closed, H15): at boot, `ProducerRunner` requeues jobs left
  `queued` back to `queued`, but an orphaned `running` job is **transitioned
  `running → failed`** with a `producer_failed` (`orphaned`) event and is **NOT
  requeued** — proven by a gateway-crash test asserting the orphaned job ends
  `failed`, no verdict is filed, and no command is re-run by the substrate; the
  holder re-runs the verb deliberately for a fresh job. (Asserts the stated scope:
  at-most-one terminal verdict, not at-most-one command execution.)
- Seams: the worker resolves the workdir via `Placement.holder_workdir/2` and runs
  the command **locally on the gateway host** (F10); `Placement.run_on_host/3` is
  **not** exercised (deferred). A holder placed on a remote host is
  refused/deferred, not silently run against the wrong checkout.
- **CAS race (F6):** terminal transitions are per-transition guarded UPDATEs —
  `running → done`/`failed` guard `state='running'`; `cancel` guards
  `state IN ('queued','running')`. The winning `running → done` UPDATE and the
  `insert_producer_verdict_in_txn/2` verdict insert are **one transaction**; a
  `cancel` that wins `running → cancelled` first means the `running → done` CAS
  changes no row and **no verdict is filed** (proven by forcing the interleaving),
  and success and cancellation never both apply.
- Cancellation verb (pinned seam): `cancel-producer-job <jobId>` CAS-transitions
  the job to `state='cancelled'` and, when it was `running`, best-effort
  process-group-kills the local run (the transition does not block on the kill),
  emitting a `producer_failed` (`cancelled`) event. **Cancel-before-claim:**
  cancelling a job still `queued` (never claimed by `ProducerRunner`) wins the
  `queued → cancelled` CAS through this verb, so the runner never starts it — the
  case that was previously unimplementable. Cancelling a job already terminal is a
  `{noop: true}` no-op (no kill, no event). Authorization: the job's assignment
  **holder** or an **admin** may cancel; any other principal → `forbidden`;
  process denied; nil → `principal_required`; unknown `jobId` →
  `unknown_producer_job`.
- Miss behavior: `tests` key absent → `producer_unconfigured`, **no job row
  enqueued**, one `producer_failed` event, no fallback command (a wire `command`
  param is ignored — no such param).
- Non-pass: command exiting non-zero, timing out (per `timeoutMs`), or spawn/host
  failure → CAS `running → failed`, files **no** verdict, emits one
  `producer_failed` event carrying jobId + command + reason, gate stays denied.
  `run-smoke` symmetric with `real-run-passed`/`smoke`/key `smoke`.
- Authorization: `run-tests`/`run-smoke` take any session/user principal (the
  verdict-filer rule); `cancel-producer-job` is holder-or-admin (above); process
  denied and nil → principal_required on all three; unknown/closed assignment (or
  unknown jobId) refused with the pinned codes. All three producer verbs are in
  `@agent_verbs`; their CLI subcommands **and** the `assign --reviews`/`--files`
  flags round-trip via the existing CLI-integration harness.
- **C4:** a `run-tests` verdict and an agent-filed `tests-passed` on the same
  assignment are distinguishable by `producer`/`producerCommand` and by
  `produced_verdict_kinds` (only the runner's appears; the agent's carries NULL
  in `producer`/`producerCommand` though it may carry `byHarness`/`byProvider`).

---

## 9. Open questions (spec-author decisions still required)

1. **Producer command source — RULED (opine-pass): committed config, not a
   param** (§5A). The command lives in `identity/producers.toml`, keyed org-wide
   by producer kind, loaded at boot; the verb takes only `assignmentId`; an
   unconfigured kind refuses `producer_unconfigured` with no param fallback; the
   command that ran is recorded in `attests.producerCommand`. Rationale: a
   param-sourced command lets the measured party pass a no-op and receive a
   substrate stamp certifying a checkbox — the Goodhart failure the tuning doc
   §6f names. Remaining flag (future, not built): if an org ever hosts multiple
   codebases under one identity, per-kind org-wide config is too coarse — add
   per-project keying via the work-item's spec-ref project. Additive when the
   need is real; org-wide-by-kind is correct for v1's single-codebase reality.
2. **Overlap scope.** Both the authoritative in-handler check (§3.3) and the
   advisory fact (§4D) overlap against **all** open assignments. An org may want
   work-item-scoped overlap (aspects of one feature) or cross-item overlap only;
   the in-handler check is constitutional (not operator-tunable) and the bool
   fact cannot carry a scope literal, so scoping would need a config knob or a
   second fact. Ruled all-open for P3 (the own-worktree/order-same-code intent is
   global to the repo, not per-feature); revisit if a real multi-feature-same-file
   case wants narrowing.
3. **Cross-provider redundancy today.** `harness` and `provider` are 1:1 in the
   current catalog (`claude↔anthropic`, `codex↔openai`), so
   `cross_harness_verdict_kinds` ≡ `cross_provider_verdict_kinds` now. Both are
   shipped because the mapping can diverge (a future harness on an existing
   provider) and the org picks its axis. Flag: if the catalog is guaranteed 1:1
   forever, one fact suffices — but that guarantee is not the substrate's to
   make.
