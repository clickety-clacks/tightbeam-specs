# Enforcement conformance smoke set — spec (r10)

_Revision: r10. Aligned to companion specs `p3-observables-producers-v1.md` (r7),
`rails-mechanism-v1.md` (r9), and `model-ringdown-pattern.md` (r11, model-adjudication); no cases
held. Fixture census: 72 (13 green, 59 pending). One
remaining forward dependency: the escalate trio is moot in v1, gating on `escalation-substrate-v1`'s
adversarial review landing clean (§10 Q4). Revision trail: r3 round-3 rulings; r4 residual
grammar/count; r5 concurrency/escalation breadth; r6 vocabulary/coherence; r7 mech-r7 lock; r8
park-wake text + park-race/prospective-revoke fixtures; r9 occurrence rule + `resolve/3` unified
union; r10 whole-lattice batch (iterate-rewake, unbound-reviewer, note-digest, orphaned-job,
sweep-never-consumes, adjudication-hold; ruled park scope + adjudication world vocab)._

> **AMENDED 2026-08-12:** Adjudication was deleted 2026-08-05 ("Adjudication is DELETED. Model policy is guidance, not substrate." — `tightbeam-decisions.md`).
> The deletion took the `adjudicate` / `adjudication_episode` world keys and
> the `adjudication-hold-order` fixture with it. The live census is **64**
> fixtures, not 72 (`conformance_test.exs` records the post-deletion deltas
> in place). Adjudication rows below are retained as history. See `adjudication-deletion-amendment.md`.

This is a **spec** for the enforcement conformance smoke set: the engine's executable
specification. It defines a graded conformance suite spanning every rail class the roadmap
names (C1–C7 + a capstone ensemble), the pure-data corpus that drives it, the runner that
executes it, and the wiring checks that prove the harness gates are live. Classes whose
machinery exists on `main` run green now; classes whose machinery lands in P3–P7 are authored
now and sit pending, and a phase is Done when its class goes green.

The load-bearing decisions this spec is written against (established r3, extended through r8):
- **One dry decision API: `Rules.decide/2` (pure).** `Rules.evaluate/2` keeps its current
  contract (`:ok | {:deny, …}`) as a wrapper. **Dispatch and Supervision are the only actors** —
  the dry decider never performs an effect; the acting layer (a `Dispatch`/`Supervision` entry)
  fires remedies and prods.
- **The sweep is decision-based**, not attest-heuristic. Reviewable-vs-abandoned is the dry
  decision itself (`{:remedy, …}` → run-remedy; a turn-end pure-deny → re-obligate; `:allow` →
  none). Suppression is **self-scheduled wakes only** (`Wakes.self_pending_count`); the rail step
  runs **before** supervision's pending-wake check, so a non-self wake does not suppress.
- **F1's producer registry is closed:** in-statute remedies (their `produces`) ∪
  `producers.toml` kinds ∪ statutes annotated `external_producer = true`. Nothing else counts;
  generic assign/attest capability is not a producer.
- **Provenance writers are split:** every verdict's `byHarness`/`byProvider` are stamped by the
  ordinary attest insert at filing; `producer`/`producerCommand` are written **only** by
  `insert_producer_verdict_in_txn`. Legacy NULL stamps read as **nil → never satisfies**.
- **Remedy episodes are CAS state machines:** `claimed → dispatched(producerKey) → live →
  closed`. Producer jobs live in a new `producer_jobs` table (`wire_idempotency` untouched).
- **Independence requires the verdict's author = the review assignment R's holder AND R's creator
  ≠ A's holder** — commissioned-reviewer-only, not merely review-link-only.
- Scripts and producers run **gateway-host-only** in v1; the workdir seam is
  `Placement.holder_workdir/2`. The overlap refusal code is `files_overlap` (P3 canonical). A
  missing required remedy target is a **load error**, never a runtime condition. Reviewer
  teardown is a separate org rail; the session-liveness observable it needs is a named gap.

Every green fixture was executed against the real compiled grep or the real `Rules.evaluate`
path before being written down. Definitive language throughout; content states rules and facts.

---

## Goal

One corpus of pure-data fixtures that:
1. proves every green rail class enforces correctly, in both directions, with named legibility;
2. carries every pending rail class as authored-but-skipped fixtures representative of the
   mechanism each phase delivers, so P3–P7 land against a written target;
3. makes last night's shipped-statute proofs a durable regression;
4. is consumed unchanged by two runners — the substrate's ExUnit conformance harness today, and
   the self-tuning system's generated-rail validator later.

## Non-goals

- **Not** a substrate-mechanism spec. The decider, remedy engine, sweep, producer jobs, and fact
  registry are specced in `rails-mechanism-v1.md` and `p3-observables-producers-v1.md`; this spec
  authors the fixtures those mechanisms must satisfy and marks them pending until they land.
  Where those specs and this one could disagree, they govern; a divergence is a bug here.
- **Not** a source of new rails for the shipped bundle. C2–C7 specimens exercise engine
  machinery; only C1 mirrors shipped law.
- **Not** an adversarial containment test. Containment-tier enforcement (own-worktree write wall,
  forbidden-substitution) is proven by the containment suite, referenced as a named cross-suite
  dependency (§6.3), never re-authored as rail-tier fixtures.

## Invariants

- **I1 — Pure data.** A fixture is TOML (artifact + metadata) and JSONL (cases), plus, for C5, an
  executable script file, plus, for load-rejection fixtures, a statute-set directory and a
  `.load.toml`. No fixture contains executable substrate code; the runner owns all
  materialization.
- **I2 — Both directions, with one exception.** Every **case-based** fixture carries ≥1 positive
  case (a violation the gate must deny/refuse/remedy) and ≥1 negative case (compliant work the
  gate passes silently); a case-based fixture with no negative case is malformed and fails the
  suite at load. **Load-rejection fixtures (§1.5) are duality-exempt**: each asserts exactly one
  load outcome (`load-raise` XOR `load-clean`); the pair of fixtures across a mechanism (a raise
  fixture and its clean twin) supplies the two directions, not two cases inside one fixture.
- **I3 — Legibility asserts the mechanism's own record.** Every positive case names the reason;
  every case-based fixture carries ≥1 legibility case asserting the extended `events` `denied`
  payload and/or the `rail_script`/`rail_remedy`/`rail_sweep` `lifecycle_events` row (§1.7). One
  legibility contract, the mechanism's.
- **I4 — Graded, never skipped-silently.** A pending fixture is registered and reported with its
  blocking phase (or `pending-unhomed`/`pending-runtime` with a named gap). Pending fixtures are
  authored to the same schema as green ones; flipping a class on is a runner change plus a
  manifest flag, never a rewrite.
- **I5 — Green means executed.** A green fixture runs real engine code. No green fixture is a
  mock.
- **I6 — Same corpus, two consumers.** The corpus format is repo-agnostic; the runner takes a
  corpus root.
- **I7 — Tier fidelity.** Each fixture asserts at its rule's tier: harness (compiled grep),
  dispatch decision (`Rules.decide`) or its wrapper (`Rules.evaluate`), the acting layer
  (`Dispatch`/`Supervision`), the verb handler (transactional refusal), or load (satisfiability).
  A fixture never asserts a containment-tier guarantee; those are named dependencies.

---

## 1. Corpus format

### 1.1 File layout

```
tightbeam_ex/test/
  conformance_test.exs                    # the ExUnit runner (§5)
  conformance/
    manifest.toml                         # class registry (§1.2)
    c1_harness_gates/  <fixture>.toml  <fixture>.cases.jsonl
    c2_dispatch_predicates/
    c3_fact_existence/
    c4_provenance_independence/
    c5_script_guards/
      <fixture>.toml  <fixture>.cases.jsonl
      scripts/<script>                     # bare kebab identifier, executable, NO extension
    c6_remedies/
      review-remedy-spawn.toml   review-remedy-spawn.cases.jsonl        # dispatch/acting fixtures
      # each load mechanism is a twin PAIR (a -raise fixture and its -clean twin, §1.5/I2):
      missing-producer-unsatisfiable.load.toml                          # outcome = load-raise
      missing-producer-unsatisfiable.loadset/
        gate.toml                                                       # the statute(s) under load
        producers.toml                                                  # the F1 registry input (§F1)
      producer-present-satisfiable.load.toml                            # the -clean twin
      producer-present-satisfiable.loadset/
        gate.toml   remedy.toml   producers.toml
    c7_turn_end_sweep/
    capstone/
```

The self-tuning validator (T-B) runs the identical runner against `identity/conformance/`. The
runner defaults to `test/conformance/` and accepts `--corpus <root>`. C5 script files are bare
kebab identifiers (`^[a-z0-9][a-z0-9-]*$`), executable, no extension — byte-identical to the
mechanism's `identity/rails/scripts/<name>` contract.

### 1.2 The manifest

`manifest.toml` is the class registry — the single place a phase flips a class on.

```toml
[[class]]
id = "C1"; dir = "c1_harness_gates"; title = "Harness tool-gates"
kind = "harness-gate"; phase = "green"; blocking_phase = ""
runners = ["compiled_hook_grep"]

[[class]]
id = "C7"; dir = "c7_turn_end_sweep"; title = "Turn-end sweep"
kind = "sweep"; phase = "pending"; blocking_phase = "P6"
runners = ["rules_decide", "acting_layer"]
```

A class's `phase` gates its directory; a fixture may carry `phase = "pending"` /
`pending-unhomed` / `pending-runtime` individually. A class flips green when its `phase` is
`green` and every fixture in it is `green`.

### 1.3 The fixture artifact (`<name>.toml`)

```toml
[fixture]
class = "C4"
name = "review-link-independence-matrix"
phase = "pending"               # green | pending | pending-unhomed | pending-runtime
blocking_phase = "P3"           # phase, §6-mapping row, or "runtime" gap
kind = "dispatch-rule"          # harness-gate | dispatch-rule | script-guard | remedy
                                #  | handler-refusal | load-rejection
source = "p3 §4A; guidance §6:independent-review; orchestrator:independence"
legibility = "event:denied(rule=coder-completion-needs-independent-review)"

# harness-gate fixtures (C1) name the shipped statute and carry no rule:
#   shipped_ref = "engineering.toml:no-git-stash"

# dispatch-rule / script-guard / remedy fixtures carry the artifact inline as a real
# [[rule]], nested EXACTLY as rails-mechanism-v1 §A1/§C1 loads it. The runner strips the
# `fixture.` prefix and reserializes to a [[rule]] file for Rules.load! — the fixture root is
# `fixture`, NOT `rule`, so this is an honest extraction, not byte-identity.
[[fixture.rule]]
name = "coder-completion-needs-independent-review"
verb = "attest"
text = "completion needs a reviewed-clean verdict from a commissioned cross-harness reviewer"
edges = ["verb"]
deny_when = [
  { fact = "attest.kind", op = "eq", value = "completion" },
  { fact = "assignment.holder_archetype", op = "eq", value = "coder" },
  { fact = "assignment.cross_harness_verdict_kinds", op = "not_in", value = ["reviewed-clean"] },
]
```

A C5 fixture adds the nested script tables (`[fixture.rule.check]`,
`[fixture.rule.check.effects]`); a C6 remedy fixture adds `[fixture.rule.remedy]` /
`[fixture.rule.remedy.params]`. A **bare** root `[check]`/`[remedy]` is a mechanism load error,
asserted by the `grammar-root-table-rejected` load-rejection fixture.

### 1.4 The cases (`<name>.cases.jsonl`)

One JSON object per line. Fields:

| Field | Required | Meaning |
|---|---|---|
| `case` | yes | Unique case id within the fixture. |
| `kind` | yes | `positive` \| `negative` \| `legibility`. |
| `expect` | yes | `deny` \| `pass` \| `refuse` (handler abort) \| the four `rail_sweep` decisions `run-remedy` \| `re-obligate` \| `escalate-park` \| `none` \| `escalate-halt` (dispatch-actor escalate deny) \| `escalate-open` (dispatch-actor `{:needs_request, nil}` — the verb opens the DR and returns `{:decision_pending, id}`; the live raiser self-parks per the verb-edge rule) \| `escalate-continue` (the engine ruled `:allow` — the fold must proceed to the next statute, §C6 escalation). `escalate-park` is the **sweep** actor's `decision_pending` decision **only** (open DR + substrate-park the holder); the **dispatch** actor uses `escalate-open`, never `escalate-park`. |
| `reason` | positive+legibility | The rule/statute/handler-code the outcome must name. |
| `emits` | legibility | The mechanism record token (§1.7). |
| `input` | harness-gate | The raw tool-call JSON the grep reads on stdin. |
| `script_return` | script-guard | The token/band the runner drives the fixture script to (§4). |
| `world` | dispatch/handler/remedy/sweep | The declarative world the runner materializes (§1.6). |
| `call` | dispatch/handler/remedy | The dispatch call: `{verb, principal, params, session_key?}`. |
| `phase2` | remedy/producer | A second call + world mutation asserting the async release (§1.6). |
| `note` | no | Human note; ignored by the runner. |

### 1.5 The load-rejection schema (first-class, a sibling of the case schema)

Satisfiability, dead-remedy/dead-gate, missing-target, and malformed-law fixtures assert an
outcome of **`Rules.load!` itself**, before any call. A load-rejection fixture is a sibling pair
in the class directory: a `<name>.loadset/` directory holding the statute TOML files under load
(any basenames) plus, when the mechanism is producer-related, a literal `<name>.loadset/producers.toml`
(the F1 registry input, §F1) that the runner feeds to `Rules.load!` as the producer registry;
and a `<name>.load.toml` beside it:

```toml
[loadset]
name = "missing-producer-unsatisfiable"
class = "C6"; phase = "pending"; blocking_phase = "P5"
outcome = "load-raise"          # load-raise | load-clean
# for load-raise: the error must name the GATE and the MISSING KIND (mechanism §C1's single
# name form — the gate plus its unproducible kind, NOT two statute names). F2 blocked-remedy
# fixtures instead name BOTH the remedy statute and the blocking statute.
must_name = ["coder-completion-needs-independent-review", "reviewed-clean"]
error_match = "no producer"
source = "mechanism §F1 (closed registry: remedies ∪ producers.toml ∪ external_producer)"
```

- `outcome = "load-raise"` — `Rules.load!` (pointed at the loadset dir, given its `producers.toml`
  as the registry input) must raise, the message must contain `error_match`, and every token in
  `must_name` must appear.
- `outcome = "load-clean"` — `Rules.load!` must succeed (e.g. `runtime-conditional-blocker-loads`,
  or a gate annotated `external_producer = true` whose kind no in-statute remedy produces).

This schema is the reusable home for every future malformed-law regression.

### 1.6 The declarative world

`world` is a fixed vocabulary the runner materializes via public substrate APIs into a fresh
`:memory:` DB (the `check_tier_test` pattern). The runner rejects any key outside it.

| Key | Row shape | Materialized via |
|---|---|---|
| `users` | `{id, admin}` | `INSERT INTO users` |
| `sessions` | `{key, owner, archetype, harness?, provider?, host?, model?, adjudicationHold?}` | `Org.create`; `adjudicationHold` is the three-state column **NULL** (no hold) \| **`'*'`** (held, no recovery wake yet) \| **`<recoveryWakeId>`** (held, recovery wake scheduled) |
| `roles` | `{name, session}` | `Roles` bind |
| `work_items` | `{id, title}` | `WorkItems` |
| `assignments` | `{id, holder, creator?, reviews?, files?}` | `Assignments` assign; `creator` is R's opener (independence keys on it), `reviews` sets `reviewsAssignmentId`, `files` populates `assignment_files` |
| `attests` | `{assignment, kind, by, verdict_kind?}` | ordinary `Assignments.__handle__("attest", …)`; stamps the p3 columns `attests.byHarness`/`attests.byProvider` **at filing** from the author session — for **every** verdict, agent or reviewer. Leaves `attests.producer`/`attests.producerCommand` NULL |
| `producer_verdict` | `{assignment, verdict_kind, producer, producerCommand}` | `insert_producer_verdict_in_txn(txn, map)` (the plain form is dropped — no non-job caller exists) — the **only** writer of the p3 columns `attests.producer`/`attests.producerCommand`; the producer path stamps `byHarness`/`byProvider` from the **frozen job columns**, the ordinary path from the **live filing session** |
| `retune` | `{session, harness?, provider?}` | mutates a session's `harness`/`provider` **after** filing — the finding-14 regression: independence reads the frozen `attests.byHarness`/`byProvider` filing stamp, not the live session row |
| `producer_job` | `{verb, assignment, state}` where `state ∈ {queued, running, done, failed, cancelled}` (the canonical `producer_jobs` states) | dispatches `run-tests`/`run-smoke` (async accept → a `producer_jobs` row at `queued`, returning `{queued: jobId}`); the four provenance stamps are **frozen into the `producer_jobs` row at accept (`queued`)**, so a `retune` between accept and `done` does not change them; the runner advances it via the guarded transitions `running→done` and `running→failed` (incl. timeout/host-fail) `WHERE state='running'`, and the two-state cancellation `queued|running→cancelled` (a job may be cancelled **before it is ever claimed**); at `done` it lands the `insert_producer_verdict_in_txn` stamped verdict carrying the accept-time stamps; `failed`/`cancelled` land nothing (the gate stays denied). A **gateway crash mid-job** → boot recovery transitions `running→failed` with a `producer_failed(orphaned)` event, **no requeue**, no verdict (p3 fail-closed: the holder re-runs deliberately). `wire_idempotency` is untouched |
| `adjudicate` | `{session, hold}` | the pinned owner `adjudicate` verb (auth + per-action transaction) sets/clears `sessions.adjudicationHold`; used by `adjudication-hold-order` |
| `adjudication_episode` | `{session, status}` where `status ∈ {claimed, notified}` | seeds an **open `adjudication_episodes` row** — the row rails' total-order position 4 keys hold suppression on (`sessions.adjudicationHold` is the claim-filter column, not the suppression key); used by `adjudication-hold-order` |
| `ledger` | `{session, pending}` | seeds `Ledger.pending_count` (turn busy/queued) for sweep suppression |
| `wakes` | `[{target, creatorSessionKey, at}]` | seeds `Wakes`; suppression is **target-keyed on self-scheduled wakes** — a durable `creatorSessionKey` **equal to the target** marks a self-scheduled continuation (suppresses the sweep), while `creatorSessionKey` is **nil** for substrate/process-created wakes (a supervision prod or user reminder — does **not** suppress). Models both the durable creator and the target, never a mutable origin string |
| `turn` | `{session, seq, window_start}` | the terminal sequence / watermark and turn window the sweep evaluates against |

`principal` is `["session", key]`, `["user", id]`, `["process", name]`, or `null`.
**Independence facts** (`independent_/cross_harness_/cross_provider_verdict_kinds`) qualify a
verdict only when it is filed on a review assignment `R` with `reviewsAssignmentId = A`, **its
author is R's holder**, **and R's creator ≠ A's holder** — a third-party author on R, a user on
R, or an R commissioned by A's own holder all fail. `produced_verdict_kinds` reads
`producer`-stamped verdicts filed **directly** on `A`. A **legacy NULL provenance stamp reads as
nil and never satisfies** any fact.

### 1.7 The legibility contract (single, the mechanism's)

`emits` names the mechanism's own record:
- **harness-gate (C1):** stderr contains `[gate: <name>]`, hook exits 2. `emits = "gate:<name>"`.
- **dispatch / script / remedy / sweep (C2–C7):** the extended `events` `denied` payload
  `{code, rule, edge, reason, script_exit_class, ref, producer, message}` (mechanism §E1), queried
  via `EventLog.rail_denials/3`; plus one `rail_script`/`rail_remedy`/`rail_sweep`
  `lifecycle_events` row for script/remedy/sweep invocations (§E2). `emits =
  "event:denied(reason=…,rule=…)"` and/or `"lifecycle:rail_remedy(outcome=…)"`. Predicate-only
  gates emit only the `denied` event.
- **handler-refusal (C4 overlap):** the handler aborts its insert transaction and returns
  `files_overlap`; `emits = "handler:files_overlap"` and the runner asserts no assignment row
  survives.

---

## 2. Class taxonomy

| Class | Title | Kind | Runner(s) | Phase | Green when | Strength |
|---|---|---|---|---|---|---|
| **C1** | Harness tool-gates | harness-gate | compiled-hook grep | **green now** | — | accident-grade |
| **C2** | Dispatch deny-predicates | dispatch-rule | `Rules.evaluate` | **green now** (2 pending-unhomed) | — | mechanical |
| **C3** | Fact-existence gates | dispatch-rule | `Rules.evaluate` | **green now** (1 pending-unhomed) | — | mechanical |
| **C4** | Provenance / independence | dispatch-rule + handler-refusal | `Rules.evaluate`, handler | pending | **P3** | strong (judge / mechanical) |
| **C5** | Script guards | script-guard | `rail-exec` exit-band | pending | **P4** | mechanical |
| **C6** | Remedies / active gates | remedy + load-rejection | `Rules.decide` + acting layer, `Rules.load!` | pending | **P5** | — |
| **C7** | Turn-end sweep | sweep | `Rules.decide` inside `Supervision.evaluate` | pending | **P6** | scaled by decision |
| **Cap** | Reviewer-loop ensemble (C3–C7) | capstone | full stack | pending | **P7** | strong, end-to-end |

**The green/pending seam is the fact registry and the mechanism.** Fixture counts: C1=6, C2=6,
C3=4, C4=10, C5=3, C6=25 (4 dispatch/acting + 9 concurrency/escalation + 12 load-rejection [6 twin
pairs]), C7=13, Cap=5 — **72 fixtures**, of which **13 green** (C1×6, C2×4, C3×3) and **59 pending**.
The census counts every physical fixture: a load mechanism's `-raise` and `-clean` twin are two
fixtures (I2). The round-5 concurrency/escalation additions (9 fixtures) prove the new
episode-fencing, per-statute closure, producer CAS/verdict-transaction, four-shape escalation,
and watermark requirements; **all are locked** against p3 r7 and mech r7 (occurrence-keyed
external-dispatch fencing, `{decision, to_close, to_consume}` per-statute closure/consume,
`insert_producer_verdict_in_txn`, `rail_step/4`, the `run-remedy|re-obligate|escalate-park|none`
`rail_sweep` enum, the §D2.4 sweep-opens-DR-and-parks-holder rule, and the pre-rail-step
`holder_state` check). The escalate trio is **moot in v1** and goes
green when the `escalation-substrate-v1` spec's adversarial review lands clean (the model is
ratified; the review gates loading) — the one remaining forward dependency (§10 Q4).

---

## 3. Per-class fixtures

### C1 — Harness tool-gates (green)

Runner: compile each statute as `rails.ex` does, pipe each case's `input` into the `sh -c`
command; assert exit 2 (deny) / 0 (pass) and `[gate:<name>]` on stderr. Every case executed
against the real grep.

| Fixture | Positive (deny) | Negative (pass) |
|---|---|---|
| `no-git-stash` (simple) | `git stash`, `git stash -u`, `git stash push -m wip`, `git stash pop`, `git stash drop`, `git stash clear`, `git stash apply`, `git stash save wip` | `git stash list`, `git stash show -p`, `echo git stashing is fun` |
| `no-git-reset-hard` (simple) | `git reset --hard`, `git reset --hard HEAD~1` | `git reset HEAD file`, `git reset --soft HEAD~1` |
| `no-git-clean-force` (simple) | `git clean -fd`, `git clean --force`, `git clean -xdf` | `git clean -n`, `git clean --dry-run` |
| `no-git-checkout-discard` (simple) | `git checkout -- .`, `git checkout -- src/a.ex` | `git checkout --detach abc`, `git checkout --track origin/x`, `git checkout -b x`, `git checkout main` |
| `no-git-restore` (simple) | `git restore src/a.ex`, `git restore --staged f` *(documented over-match)* | `git status`, `git stash show -p` |
| `compound-and-quote` (complex) | `cd src && git reset --hard`, `git commit -m "wip" && git stash` (JSON-escaped quotes) | `git commit -m "do not git stash by hand"` |

**`c1-shipped-parity`** (runner assertion): every statute in the shipped `engineering.toml` has a
C1 fixture whose `shipped_ref` names it and whose asserted pattern is byte-identical. The shipped
law's canonical source is IN THE CODE REPO at `priv/kungfu/agentic-engineering/` (rails now;
scripts and `producers.toml` as P7b lands) — the conformance suite reads `priv/`, never a live
identity repo (org instances are deployment copies seeded/updated from `priv/`, per the
`init_identity!` precedent). P7b authors into `priv/` and deploys to the playground.

### C2 — Dispatch deny-predicates (green; 2 pending-unhomed)

Runner: materialize `world`, run `Rules.evaluate`; assert `{:deny,…}` vs `:ok`; legibility via
`Dispatch.dispatch` + `EventLog.rail_denials/3`.

| Fixture | Feature | Positive (deny) | Negative (pass) | Facts |
|---|---|---|---|---|
| `admin-only-verb` (simple) | caller identity | non-admin runs `spawn` | admin runs `spawn` | `caller.is_admin` |
| `no-self-verdict` (simple) | verb-holder relation | holder files own verdict | reviewer/user files it | `assignment.caller_is_holder` |
| `gauge-quota` (simple) | gauge read | over the live-session gauge | under it | `org.live_sessions_owned_by_caller` |
| `non-admin-self-verdict` (complex) | two fact families | non-admin **and** holder | admin user; reviewer | `caller.is_admin` + `assignment.caller_is_holder` |
| `handoff-wake` (**pending-unhomed**) | hand-off fields, `wake` | `wake` missing what-passed / expected-back / whom-to-wake | all three present | needs a param-presence fact — no planned home |
| `handoff-assign` (**pending-unhomed**) | hand-off fields, `assign` | `assign` missing any field | all three present | as above |

### C3 — Fact-existence gates (green; 1 pending-unhomed)

| Fixture | Feature | Positive (deny) | Negative (pass) | Facts |
|---|---|---|---|---|
| `verdict-present-tests` (simple) | presence, empty-list-fires | completion, no `tests-passed` | completion, `tests-passed` present | `assignment.verdicts`, `attest.kind` |
| `verdict-present-review` (simple) | presence, review kind | completion, no `reviewed-clean` | completion, `reviewed-clean` present | `assignment.verdicts`, `attest.kind` |
| `verdict-and-archetype` (complex) | 3 conditions ANDed | (completion, coder, none)→deny | (completion, coder, `tests-passed`); (completion, reviewer, none); (progress, coder, none) | `attest.kind` + `holder_archetype` + `verdicts` |
| `two-changes-requested-revert` (**pending-unhomed**) | verdict **count** | 3rd completion after 2 `changes-requested` | fewer than 2 | needs a derived count — no planned home |

### C4 — Provenance / independence (pending P3)

Runner: `Rules.evaluate` for deny gates; `handler-refusal` for overlap. Fixtures authored to the
final P3 registry with the **commissioned-reviewer** independence rule.

| Fixture | Feature | Positive (deny/refuse) | Negative (pass) |
|---|---|---|---|
| `review-link-independence-matrix` (complex) | **commissioned-reviewer independence**: author = R's holder AND R's creator ≠ A's holder | **direct-on-A cross-harness non-holder `reviewed-clean` → denies** (anti-laundering); **wrong-author-on-R** (author ≠ R's holder) → denies; **user-on-R** → denies; **producer-commissioned-shell** (R's creator = A's holder) → denies; on-R same-harness → denies | on-R, R's holder authored, R's creator ≠ A's holder, cross-harness → passes |
| `independence-author-only` (simple) | author ≠ holder, harness-agnostic | on-R same-harness R's-holder verdict, gated on cross-harness → denies | same gated on `independent_verdict_kinds` → passes |
| `cross-provider` (simple) | provider axis | on-R same-provider verdict → denies | cross-provider on-R verdict → passes |
| `produced-tests-only` (simple) | mechanical stamp; **async two-phase** | phase 1: `run-tests` → `{queued: jobId}`, produced fact absent → completion denies; an agent-filed `tests-passed` (`producer` NULL, legacy nil) never satisfies | phase 2 (`producer_job.state=done`): stamped verdict lands → re-dispatch passes; a `failed`/`cancelled` job lands nothing → stays denied |
| `produced-real-run-only` (simple) | real-run stamp | as above with `run-smoke`/`real-run-passed` | phase-2 release |
| `re-tuned-after-filing` (complex) | provenance frozen at filing (finding-14) | **positive:** verdict filed **same**-harness, author `retune`d cross-harness afterward → gate **still DENIES** (frozen non-qualifying stamp) | **negative:** verdict filed cross-harness, author `retune`d same-harness afterward → gate **still passes** (frozen qualifying stamp) |
| `declared-files-overlap` (complex, handler-refusal) | transactional refusal at `assign`; fact observational; **concurrency proof** | `assign` declaring a path an **open** assignment declares → handler aborts insert (`files_overlap`), no row survives; two concurrent overlapping assigns → the serialized handler transaction lets exactly one win, the other refuses | disjoint files; overlap only with a **closed** assignment; absent `files` → succeeds; `assign.declared_files_overlap_open` asserted **observational only** |
| `frozen-job-provenance` (complex) | provenance frozen at accept **through the job world** | sequence: `run-tests` accept (`producer_job.state=queued`, four stamps frozen) → `retune` the running producer's session to a same-harness/same-provider identity → `producer_job.state=done` → the landed verdict's `byHarness`/`byProvider`/`producer`/`producerCommand` equal the **accept-time** values, so a `cross_harness` gate that qualified at accept **still passes** despite the mid-job retune | the negative direction: a job whose accept-time stamps did **not** qualify stays non-qualifying at `done` even if the session is retuned to qualify afterward |
| `producer-cas-verdict-txn` (complex) | producer `running→done` CAS **and** verdict in ONE transaction (p3 r7 final) | the winning worker flips `running→done` and inserts its verdict atomically via `insert_producer_verdict_in_txn(txn, map)` (the plain form is dropped); losing interleavings — a second worker on the same job, and a `running→failed` (timeout/host-fail) racing the flip, each guarded `WHERE state='running'` — land no duplicate verdict; a **cancel-before-claim** (`queued→cancelled` before any worker claims) is its own asserted case | a `cancelled` or `failed` job commits no verdict; the gate stays denied |
| `orphaned-running-failed` (complex) | gateway-crash recovery is fail-closed (p3 r7) | a gateway crash **mid-job** (`producer_job.state=running`) → boot recovery transitions `running→failed` and emits `producer_failed(orphaned)`, with **NO requeue** and **no verdict**; the gate stays denied and the holder re-runs deliberately | a job that reached `done` before the crash keeps its verdict; recovery leaves it untouched |

### C5 — Script guards (pending P4)

A `[[rule]]` with `[rule.check]` names a script whose return maps via `[rule.check.effects]`.
Executed (once P4) via the Rust `tightbeam rail-exec` wrapper with class-encoded exit bands. The
invocation carries `holder_workdir`/`host`/`harness` (the workdir seam is
`Placement.holder_workdir/2`; there is **no `repo` key — the holder workdir is the context**);
CWD = the holder workdir, writes scratch-only. Scripts run **gateway-host-only** in v1.

| Fixture | Script check | Returns / effects | Phase |
|---|---|---|---|
| `reconcile-with-main` (complex) | `git merge-base --is-ancestor main <branch>` in the holder workdir | `{reconciled→allow, behind→deny}`; carries the fail-closed matrix (§4) | pending P4 |
| `files-touched-observed` (simple) | `git diff` branch vs base compared to the declared set | `{within-declared→allow, outside-declared→deny}` | pending P4 |
| `predicate-prefilter-script-laziness` (simple) | a would-crash (band 10) script **behind a non-matching predicate** | asserts the script **never runs** on predicate-miss → `allow` (D1 hybrid / r6-laziness) | pending P4 |

**Materialization note (§4):** the `pass`/`in-set`/`out-of-set`/`error`/`timeout` bands are
driven by fixture-script behavior in a real gateway-host checkout the runner seeds. The band-30
`contained-refused` (sandbox profile fails to *apply*) cannot be forced from script content; that
single case is tagged **`pending-runtime`** with a note that it is exercised by a fault-injected
`sandbox-exec` harness, not by fixture data.

### C6 — Remedies / active gates (pending P5)

**Dispatch/acting fixtures (4)** act through the **acting layer** (a `Dispatch`/`Supervision`
entry) that consumes the dry `Rules.decide/2` decision and performs the effect — the runner never
expects the dry decider to mutate.

| Fixture | Feature | Positive / assertion | Negative |
|---|---|---|---|
| `review-remedy-spawn` (simple) | remedy originates producer through the acting layer | absent `reviewed-clean` → `Rules.decide` returns `{:remedy,…}`; the acting layer **claims the episode row (CAS `claimed`) before any side effect**, dispatches the reviewer as the `remedy:<statute>` principal (`dispatched(producerKey)` → `live`), denies now, self-releases when the verdict lands (`phase2`) | verdict present → decide `:allow`, no episode, no dispatch |
| `remedy-episode-idempotent` (complex) | episode CAS `claimed→dispatched(producerKey)→live→closed` | concurrent **initial publication**: two fires race the `claimed` CAS; the loser observes the claim and does **not** dispatch a second producer; a live episode re-fire → **rewake, not respawn**; `changes-requested` keeps the episode `live` (next fire rewakes); `reviewed-clean` → `closed`; a **dead producer** → guarded `replacement`; a **closed** episode with the fact re-absent → guarded `reopen`. **Occurrence rule (mech r9): any transition out of a TERMINAL state bumps `occurrence`; only the TTL-stale-claim (non-terminal, pre-live) reclaim preserves it** — three reclaim branches asserted: **reclaim-closed** (bump → observed-occurrence CAS → fresh wire key → genuinely NEW producer), **reclaim-stale-claim** (preserve → the still-running original dedupes), **reclaim-dead-live** (bump). `fresh-occurrence-on-reopen` asserts close→re-fire→a distinct new producer | first fire → exactly one producer |
| `remedy-action-breadth` (complex) | per-action target schemas | `assign`→`target_role`; `wake`→`target_role`\|`target_session`; `spawn`→`name`/`harness`/`model` each resolve through the acting layer and dispatch | the gate's required fact already present → `Rules.decide` returns `:allow`, so **no** remedy fires for any action (compliant work passes silently, no dispatch) |
| `script-result-remedy` (complex) | C5 token → C6 effect | a `[rule.check.effects]` value of `remedy` on a return token fires the remedy | an `allow` token fires nothing |

**Load-rejection twin pairs (6 mechanisms → 12 fixtures).** Each mechanism is two physical
fixtures under the I2 duality exemption: a `load-raise` fixture and its `load-clean` twin (§1.5),
each asserting its single outcome via `Rules.load!`.

| Mechanism | Raise fixture (→ load-raise) | Clean twin (→ load-clean) |
|---|---|---|
| Missing remedy target (§C1) | `remedy-target-missing`: a `[rule.remedy]` omitting a target field its `action` requires → raise (replaces r2's runtime `unbound`) | `remedy-target-present`: every required target supplied |
| F1 closed registry | `missing-producer-unsatisfiable`: a gate requiring a kind no source in `{remedies ∪ producers.toml ∪ external_producer=true}` produces → raise naming **gate + missing kind**; an independence gate's direct-on-A remedy does **not** count | `producer-present-satisfiable`: a matching-path in-statute remedy exists, **or** the gate is `external_producer=true`, **or** a `produced_verdict_kinds` gate has a `producers.toml` producer |
| F2 conditional blocker | `static-blocker-unsatisfiable`: a remedy whose producer verb a **pure static** blocker forbids → raise naming **both** statutes | `runtime-conditional-blocker-loads`: a remedy forbidden only on runtime state (`verb_count_24h gte 3`) → loads clean |
| Dead remedy (§C1) | `dead-remedy`: `[rule.remedy].produces` matches no gate → raise | `live-remedy`: `produces` matches a required kind |
| Dead gate (§F1) | `dead-gate`: a gate requiring a verdict nothing produces → raise | `producer-backed-gate`: a producer for the kind is present |
| Grammar nesting (§A1) | `grammar-root-table-rejected`: a bare root `[check]` (not `[rule.check]`) → raise | `grammar-nested-accepted`: correct `[rule.check]` nesting |

**Concurrency & escalation fixtures (9, round-5/8/lattice additions; r9/r11-aligned).** All are **locked** to
mech r7 / p3 r7 (the `pending-mech-r6`/`pending-p3-r6` holds are cleared — both diffs landed); the
escalate fixtures carry only the forward `escalation-substrate-v1` review-clean dependency (§10 Q4).

| Fixture | Feature | Positive / assertion | Negative |
|---|---|---|---|
| `escalation-return-dispatch` (complex) | the escalate effect at the **dispatch** actor over `resolve/3`'s unified union (mech r9) | an `escalate`-effect statute (`decide`'s escalate decision is `{:escalate, statute, ctx, dr_id}`); `resolve/3` returns `:allow \| {:allow, ruling_id} \| {:deny, e} \| {:needs_request, dr_id\|nil}`: `{:deny, e}` → `escalate-halt` (verb denied); `{:needs_request, nil}` → **`escalate-open`** — the dispatch actor **opens the DR and returns `{:decision_pending, id}` to the caller**, and the live raiser self-parks per the verb-edge rule (**not** `escalate-park`, which is the sweep actor's decision only); `{:needs_request, dr_id}` with **non-nil `dr_id`** → the existing `{:decision_pending, dr_id}` is **re-returned without opening** a second DR; `:allow` (waiver-sourced) or `{:allow, ruling_id}` (ruling-sourced, consumed by the actor on whole-fold allow) → `escalate-continue` | `:allow` with no later gate → verb proceeds silently |
| `escalation-continue-the-fold` (complex) | **bypass regression** + `{decision, to_close, to_consume}` shape, per-ruling-row consume (mech r8) | two statutes on one verb: statute 1 escalates and the engine rules `:allow`; statute 2 (a later gate) is **still evaluated** and denies → net `deny` by statute 2; asserts `Rules.decide` returns the `{decision, to_close, to_consume}` triple | statute 2 also allows → **whole-fold `:allow`**, so the actor **consumes** the `to_consume` set via a **per-ruling-row CAS** — **any CAS loss denies** the whole fold; asserts statute 2 was evaluated either way |
| `waiver-revoked-mid-fold` (complex) | prospective-revoke: revocation is not retroactive (mech r8) | a waiver revoked **after** a call has already passed the fold check → that call **PROCEEDS**, asserted **correct** (not a leak): the revoke catches only **subsequent** calls | a call that reaches the fold **after** the revoke → the waiver no longer applies and the gate fires |
| `stale-claimant-fencing` (complex) | **one external effect per occurrence** (mech r7) | the external dispatch wire key is `rail-dispatch:<statute>:<subject>:<occurrence>`; a **TTL reclaim's** re-dispatch collapses to **one** producer via the forever ledger (occurrence unchanged), while a **dead-live replacement** bumps `occurrence` — which advances **only on provable termination** (producer confirmed dead **AND** wire entry inspected, never on TTL) → a genuinely new producer. `claimToken` is **row-fencing only** (not the wire nonce); episode rows carry `occurrence` + `rewakeCount`, and re-wakes land under distinct `occurrence`+`rewakeCount` keys | the live claimant dispatches exactly once per occurrence |
| `denied-dispatch-release-retry` (complex) | a denied remedy dispatch releases the lease for an **edge-driven** retry (mech r6) | a `remedy` whose producer dispatch is denied → the lease is **DELETEd**, `blocked` is recorded, the gate stays denied, and the episode does **not** wedge `live`; the re-fire is **edge-driven** (the next verb dispatch or next sweep re-claims a fresh lease). Asserts **no wedge and no timer** | a successful dispatch holds the lease and the episode `live` |
| `multi-statute-episode-closure` (complex) | per-statute closure ownership via `{decision, to_close, to_consume}` (mech r7) | `Rules.decide` returns `{decision, to_close, to_consume}`; the **actor** closes each individually-passed statute's episode scoped `WHERE statute AND subject`, regardless of the final decision. The proof: S1 passes, S2 denies on one subject → **E1 closes, E2 stays `live`, net `deny`** | both statutes `:allow` → both episodes close |
| `iterate-rewake-target` (complex) | re-fire wakes the right role by latest reachable verdict (mech §C3 step 3) | on an episode re-fire, the latest reachable verdict = `changes-requested` → wake **A's holder** (iterate the producer); **no verdict yet** → wake the **reviewer** (chase the pending review) | the required fact is present → episode closes, no wake |
| `unbound-reviewer-remedy` (complex) | a remedy target with no real bound session fails LOUD (mech §C2) | a `[rule.remedy]` target role that `Roles.resolve` resolves via the **owner-Main fallback** (`{:ok, _, true}`) or `unknown_role` → the remedy fails **loud `unbound`**, records it, and **never silently assigns owner-Main** | a target role with a real bound session → dispatches |
| `note-digest-exclusion` (complex) | actionKey ignores `--note` (escalation case 21's twin) | a re-issued `attest` **with a `--note`** still matches the prior ruling's `actionKey` (the note is excluded from the digest), so the ruling still applies | a genuinely different action (different verb/params) → new `actionKey`, no match |

### C7 — Turn-end sweep (pending P6)

The sweep is a **step inside `Supervision.evaluate`** whose decision comes from the dry
`Rules.decide/2` on the synthesized completion, acted on **at most once**. The `rail_sweep`
decision enum is **`run-remedy | re-obligate | escalate-park | none`** (mech r7). There are **no
progress/attest heuristics**: the decision itself is the outcome. `holder_state` is checked
**before** the rail step — a retired holder yields `:stranded` and no rail step runs. Suppression
is **self-scheduled wakes only** (`Wakes.self_pending_count`, keyed on `creatorSessionKey ==
target`); the rail step runs **before** supervision's pending-wake check, so a non-self wake does
**not** suppress.

| Fixture | Feature | Positive / assertion | Negative |
|---|---|---|---|
| `idle-open-obligation` (simple) | omission catch, decision = remedy | idle, open obligation; `Rules.decide` on the synthesized completion returns `{:remedy,…}` → sweep **runs the remedy** through the acting layer (idempotent under the episode key); `rail_sweep` records `run-remedy` | obligation whose decision is `:allow` (verdict present) → `none` |
| `reobligate-pure-deny` (simple) | decision = deny, no remedy | a `turn-end`-edged **pure-deny** statute (no `[remedy]`) denies the synthesized completion → sweep decision `re-obligate`; the wake is supervision's prod, **not** a remedy (remedy XOR prod) | decision `:allow` → `none` |
| `scheduled-wake-suppression` (complex) | self-wake suppresses; others do not | **negative:** a **self**-scheduled continuation wake (`creatorSessionKey == target`, `Wakes.self_pending_count > 0`) → sweep does **not** fire (`none`). **positive:** a supervision prod or user-reminder wake (`creatorSessionKey` nil / ≠ target, `self_pending_count == 0`) → the rail step precedes the pending-wake check, so the sweep **still fires** its decision | — |
| `busy-or-queued-no-sweep` (simple) | ledger suppression | a running/queued turn (`Ledger.pending_count > 0`) → `none` | idle → the decision fires |
| `satisfied-obligation-no-sweep` (simple) | gate-satisfied suppression | the completion gate is satisfied (verdict present) → decide `:allow` → `none` | gate-unsatisfied → the decision fires |
| `turn-end-script-gate` (complex, C5×C7) | script gate at the omission edge | a `turn-end`-edged **script** statute evaluated at the sweep returns a `remedy`-mapped token → `run-remedy` | script `allow` token → `none` |
| `escalation-return-sweep` (complex) | the escalate effect at the **sweep** actor over `resolve/3`'s unified union (mech §D2.4 / r9) | `resolve/3` returns `:allow \| {:allow, ruling_id} \| {:deny, e} \| {:needs_request, dr_id\|nil}`: `{:deny, e}` routes through **ordinary re-obligation** (`re-obligate`), **not** `escalate-halt` (mech rails:790 — the sweep has no verb to halt); `:allow` (waiver-sourced) or `{:allow, ruling_id}` (ruling-sourced — obligation-met at the sweep, NO consume; the verb edge consumes, see `sweep-never-consumes`) → the fold continues to the next `turn-end` statute (`escalate-continue`); `{:needs_request, nil}` → the declared `rail_sweep` **`escalate-park`** decision — the sweep **opens the DR with raiser = the holder principal AND parks the holder** via a substrate-created, holder-targeted **park wake matching `{escalation-ruled, <decisionRequestId>}` whose fallback `dueAt` = the DR's `deadlineAt` (org-configurable), idempotent via a stored `parkWakeId`**; `{:needs_request, dr_id}` with **non-nil `dr_id`** → the existing DR is **re-returned without opening** and the same `parkWakeId` is reused (raiser-self-park is verb-edge-only — the sweep cannot self-park a terminated turn). Owned by `escalation-substrate-v1`; **moot in v1** pending that spec's adversarial review landing clean (the model is ratified; the review gates loading) | no `turn-end` escalate statute applies → `none` |
| `watermark-nil-duplicate` (complex) | terminal-seq watermark input & nil behavior via `rail_step/4` (mech r6) | `rail_step/4` takes `terminal_seq`; a **`nil`** seq → `:fallthrough` (no acted branch, **no NULL write** to the NOT-NULL watermark); a **duplicate** same-seq terminal → the sweep does **not** re-act | a fresh, larger terminal seq → the sweep acts and advances `lastEvaluatedTerminal` |
| `retired-holder-no-remedy` (simple) | `holder_state` pre-checked **before** the rail step (mech r7) | a **retired** holder with a pending wake yields **`:stranded`** — not `:continuation`, and **no** remedy/re-obligation fires; the rail step never runs because `holder_state` is checked ahead of it | a **live** holder → the rail step runs and the sweep decides normally |
| `parkwakeid-reuse` (simple) | park is idempotent across sweep passes (mech r8/r9) | a second sweep pass over the same open DR → `resolve/3` returns `{:needs_request, dr_id}` (non-nil) → the existing DR is **re-returned without opening** and the **same `parkWakeId`** is reused, **no double-park** | the first pass on a fresh DR (`{:needs_request, nil}`) opens the DR and schedules exactly one park wake |
| `schedule-then-check` (complex) | schedule-then-check ordering, no-replay cursor (mech r11) | the ordering is **wake first, then the recovered-check**: after scheduling the park wake, the post-schedule recovered-check reads status; if the ruling **already landed** → **cancel the park wake and proceed** (the no-replay cursor prevents a stale replay), so the holder is not stranded on a wake for an already-decided DR | the ruling lands after the check → the ordinary wake path resolves it |
| `sweep-never-consumes` (complex) | the sweep never CAS-consumes a ruling (escalation case 22's twin) | a `{:allow, ruling_id}` at the **sweep** leaves the ruling **`ruled`** (obligation-met, **no CAS consume**); the **verb edge** later consumes it **exactly once** | at the verb edge the `{:allow, ruling_id}` consumes the ruling row (one CAS) |
| `adjudication-hold-order` (complex) | model-adjudication hold precedes the rail step (mech total-order position 4) | a **live** holder with an **open `adjudication_episodes` row** (status `claimed|notified`, seeded via the `adjudication_episode` world key; `sessions.adjudicationHold` set to match) → `{:held, :adjudication_hold}`: the rail step **and** supervision's prod are **both suppressed**, and the **watermark is written** (total-order position 4); the DR-park re-return path stays distinct (`parkWakeId` idempotency) | no adjudication hold → the rail step runs normally |

### Capstone — reviewer-loop ensemble (pending P7; composes C3–C7)

Five end-to-end fixtures, the §6 flagship loops, firing at both the dispatch verb and the
turn-end edge; the ensemble spans **C3–C7 including C5**.

| Fixture | Loop | Composes |
|---|---|---|
| `capstone-reviewer-loop` | commissioned cross-harness review: deny → episode remedy assigns to the bound reviewer role (loud `unbound` if unprovisioned) → `changes-requested` iterates → `reviewed-clean` (author = R's holder, R's creator ≠ A's holder) releases; sweep catches a pre-review idle. **Teardown is out of scope** (see below). | C3 gate + C4 independence + C6 episode remedy + C7 sweep |
| `capstone-tests-before-success` | tests-pass at both edges; a `reconcile-before-build` script gate chains ahead | C4 produced-fact + C5 script + C7 sweep re-obligation (no C6 — produced-fact gates deny + re-obligate, no remedy; the holder runs the producer deliberately) |
| `capstone-real-run-before-ship` | real-run at both edges | C4 produced-fact + C7 sweep re-obligation (no C6 — produced-fact gates deny + re-obligate, no remedy) |
| `capstone-yagni-judge` | YAGNI judge gate until a `yagni`-clean commissioned verdict | C4 independence + C6 remedy |
| `capstone-spec-review` | spec-review judge gate until a `spec-reviewed` commissioned verdict | C4 independence + C6 remedy |

**Reviewer teardown descoped (finding 12).** The mechanism makes reviewer teardown a separate
**org rail**, and no reviewer-retired / session-liveness observable exists to gate completion on.
`capstone-reviewer-loop` therefore does **not** assert a teardown gate; the missing observable is
recorded as a named gap (§10 Q2), and the leak-prevention clause returns when that observable and
its org rail land.

---

## 4. The fail-closed matrix (C5)

Cases cover the mechanism's exit-band classification (`tightbeam rail-exec`: 0 pass / 10
child-nonzero / 20 timeout / 30 profile-apply-refusal):

| Case | Script behavior | Band | Gate decision | Reason / `script_exit_class` | Materialization |
|---|---|---|---|---|---|
| `pass` | trimmed stdout ∈ `returns`, `allow` | 0 | **allow** (silent) | `returned` | fixture script in seeded checkout |
| `in-set-deny` | trimmed stdout ∈ `returns`, `deny` | 0 | **deny** | `rule_denied` / `returned` | fixture script |
| `out-of-set` | stdout ∉ `returns` (incl. empty) | 0 | **deny** | `script_out_of_set` / `out-of-set` | fixture script |
| `error` | child nonzero, crash, **or in-sandbox EPERM** (write outside scratch) | 10 | **deny** | `script_error` / `error:<N>` | fixture script attempting an out-of-scratch write |
| `timeout` | exceeds `timeout_ms`; process group `SIGKILL`ed | 20 | **deny** | `script_timeout` / `timeout` | fixture script that sleeps |
| `contained-refused` | `sandbox-exec` cannot **apply** the profile | 30 | **deny** | `script_contained_refused` / `contained` | **`pending-runtime`** — fault-injected `sandbox-exec`, not fixture data |

Correction retained from r2: an in-sandbox EPERM (the script's own out-of-scratch write) is band
10 `script_error`; band 30 is the sandbox failing to *apply* the profile — a runtime fault the
corpus cannot fabricate from data, hence its `pending-runtime` tag. Async judgment is not in this
matrix (it is a C3/C4 fact-existence shape).

---

## 5. The runner

`conformance_test.exs` reads `manifest.toml`, then dispatches on each class's `runners`:

**`compiled_hook_grep` (C1).** Compile via `pre_tool_use_entry`, pipe `input`, assert exit 2/0
and the marker. Run `c1-shipped-parity`.

**`rules_evaluate` (C2/C3, C4 deny gates, C5 script effects).** Extract `fixture.rule` (strip the
`fixture.` prefix), reserialize to a `[[rule]]` file, `Rules.load!` (a malformed specimen fails
here). Materialize `world` (incl. `retune`/`producer_job` phases), run `Rules.evaluate`; assert
`{:deny, %{rule: reason}}` ⇔ `deny`, `:ok` ⇔ `pass`. `phase2` applies the mutation and re-runs.
Legibility via `Dispatch.dispatch` + `EventLog.rail_denials/3` + any `rail_script` row. C5 script
execution (P4) goes through `rail-exec` with the exit-band classification (§4).

**`rules_decide` + `acting_layer` (C6 remedies, C7 sweep).** The dry `Rules.decide/2` returns the
decision (`:allow | {:deny,…} | {:remedy,…} | {:escalate,…}`) with **no effect**; the runner
asserts the decision, then drives the effect through the acting-layer entry (`Dispatch` for the
verb edge, `Supervision.evaluate` for the sweep edge) and asserts the episode CAS transition, the
`remedy:<statute>` dispatch, and the `rail_remedy`/`rail_sweep` row. Producer async is the
`producer_jobs` table; `phase2` lands the producer verdict via `insert_producer_verdict_in_txn`,
which the runner asserts performs the job CAS UPDATE and the verdict insert in **one** transaction.

**`handler_refusal` (C4 overlap; future transactional refusals).** Dispatch the `assign` verb;
assert the handler aborts its insert transaction with `files_overlap` (or `invalid_files`,
`unknown_review_target`) and that **no assignment row survives**. The concurrency case drives two
overlapping assigns and asserts exactly one wins.

**`load_assert` (C6 load-rejection).** Point `Rules.load!` at the loadset dir (feeding its
`producers.toml` as the F1 registry input); for `load-raise` assert it raises with `error_match`
and every `must_name` token present; for `load-clean` assert it succeeds.

**Pending / pending-unhomed / pending-runtime / pending-escalation-review.** Registered with the
matching tag and its gap (blocking phase, §6-mapping row, runtime, or the escalation spec's
review-clean gate); ExUnit reports them skipped with the reason. The `pending-mech-r6` and
`pending-p3-r6` tags are **retired** — both peer diffs landed and their fixtures are locked.
Pending fixtures are parsed and schema-validated now. The suite prints a pending census. The
`escalate` outcomes drive through the same `rules_decide` + `acting_layer` path, delegating the
ruling to the escalation engine and asserting the fold **continues** past an engine `:allow`.

**Phase flip.** (1) implement the runner branch for that `kind`; (2) set `phase = "green"`; (3)
drop the pending tag. No fixture is rewritten.

**Corpus root.** `--corpus <root>` (default `test/conformance/`); the self-tuning validator points
it at the identity repo's generated-rail corpus (I6).

---

## 6. Wiring checks and cross-suite dependencies

### 6.1 Codex — live boot probe (exists)
The adapter boot-proves the reserved probe (`tightbeam-probe`, pattern `tightbeam-gate-probe`).
The suite asserts `Rails.probe_entry()` compiles to the byte-pinned reserved gate (covered by
`rails_test.exs`) and that piping the probe token refuses.

### 6.2 Claude — compiled-presence wiring check (`c1-wiring-claude`)
Claude has no hook-trust layer, so the silent-skip failure the codex boot probe guards against
does not exist. The suite asserts the probe statute is present in the compiled `settings.json`
hook map (`Rails.hook_settings()` + `probe_entry`) and that piping `tightbeam-gate-probe` refuses
with exit 2 and `[gate: tightbeam-probe]`. Codex needs a runtime boot probe; claude's gates
cannot be silently dropped once compiled in, so compiled-and-refuses is the complete guarantee.

### 6.3 Containment-tier — named cross-suite dependency (not rail-tier fixtures)
- **Own-worktree write wall** — a **named dependency on `test/containment_test.exs`** (the
  Seatbelt write-boundary suite); the smoke set asserts the dependency exists and is green, not
  the wall itself.
- **Forbidden substitution** — documented **partial-coverage-by-containment**: containment
  catches the destructive *action*, not the *intent*; the intent half is advisory guidance,
  unenforceable, named as such. Not a fixture.

---

## 7. Fixture provenance

| Fixture(s) | Source |
|---|---|
| C1 `no-git-*` (×5) | Shipped `engineering.toml`; last night's proven cases. |
| C1 `compound-and-quote` | `rails.ex` moduledoc — raw-JSON matching, escaped quotes, compound commands. |
| C2 `admin-only-verb`/`gauge-quota` | Substrate manual §identity; §6 admin-only / gauge exemption. |
| C2 `no-self-verdict`/`non-admin-self-verdict` | Orchestrator independence; `check_tier_test`. |
| C2 `handoff-*` | Tenet hand-off; §6 arg-presence row (pending-unhomed). |
| C3 `verdict-present-*`/`verdict-and-archetype` | §6 tests-pass / independent-review presence half; `check_tier_test`. |
| C3 `two-changes-requested-revert` | Tenet/orchestrator revert; §6 count row (pending-unhomed). |
| C4 `review-link-independence-matrix` | P3 §4A commissioned-reviewer invariant; orchestrator independence; §6. |
| C4 `independence-author-only`/`cross-provider` | P3 `independent_/cross_provider_verdict_kinds`. |
| C4 `produced-*` | P3 §5 producer verbs + `producer_jobs`; §6 tests-pass/real-run. |
| C4 `re-tuned-after-filing` | P3 stamp-at-filing; review finding-14. |
| C4 `declared-files-overlap` | P3 §3.3/§4D handler transaction + concurrency; tenet order-same-code. |
| C5 `reconcile-with-main`/`files-touched-observed` | Mechanism §A; coder/worktree-session; P3 §5E observed-set follow-on. |
| C5 `predicate-prefilter-script-laziness` | Mechanism I1/§B (D1 hybrid). |
| C6 `review-remedy-spawn`/`remedy-episode-idempotent` | Mechanism §C2 + `rail_remedy_episodes` CAS; §6 worked example. |
| C6 `remedy-action-breadth`/`remedy-target-missing` | Mechanism §C1 target schemas + missing-target-is-load. |
| C6 `script-result-remedy` | Mechanism §A3/§C. |
| C6 `missing-producer-unsatisfiable`/`dead-*`/`grammar-root-table-rejected` | Mechanism §F1 closed registry, §C1, §A1. |
| C6 `runtime-conditional-blocker-loads` | Mechanism §F2 bound. |
| C7 all | Mechanism §D (sweep in `Supervision.evaluate`, `Rules.decide`, `Wakes.self_pending_count`, remedy XOR prod). |
| Capstone ×5 | §6 flagship loops; feature-cycle skill. |

---

## 8. Refinements the code and companion specs forced

1. **C2/C3 "green" ≠ "shipped."** Only C1 mirrors shipped law; C2/C3 green fixtures are engine
   specimens over the existing registry.
2. **Grading within green classes.** C3 presence green, count `pending-unhomed`; C2 identity green,
   hand-off `pending-unhomed`.
3. **Independence is commissioned-reviewer-only** (r3, finding 11): author = R's holder AND R's
   creator ≠ A's holder — closes wrong-author-on-R, user-on-R, and producer-commissioned-shell,
   beyond r2's direct-on-A anti-laundering.
4. **Provenance writers split** (finding 5): ordinary attest stamps `byHarness`/`byProvider` for
   every verdict; `insert_producer_verdict_in_txn` is the sole `producer`/`producerCommand` writer;
   legacy NULL → nil → never satisfies. `re-tuned-after-filing` now carries both directions.
5. **Producers are async via `producer_jobs`** (finding 6/10): `{queued: jobId}` → verdict-lands;
   `wire_idempotency` untouched.
6. **Overlap is a handler transaction** using `files_overlap` (finding 8/11), with a concurrency
   proof; the fact is observational.
7. **Fail-closed matrix on exit bands** (finding 10): in-sandbox EPERM = band 10; band 30
   (profile-apply-refusal) is `pending-runtime` (fault-injected, not fixture data). The C5
   context has no `repo` key — the holder workdir (via `Placement.holder_workdir/2`) is the
   context; scripts run gateway-host-only.
8. **Remedy episodes are CAS** `claimed→dispatched(producerKey)→live→closed` (finding 3):
   `remedy-episode-idempotent` covers concurrent initial publication, replacement, and reopen.
   Remedies dispatch as `remedy:<statute>` through the **acting layer**, not the dry decider.
9. **One dry API `Rules.decide/2`** (finding 1); `Rules.evaluate/2` is its wrapper; Dispatch and
   Supervision are the only actors. C6/C7 runners assert the decision, then drive the effect
   through the acting layer.
10. **The sweep is decision-based** (finding 7): no attest heuristics; run-remedy vs re-obligate
    is the decision; self-scheduled wakes only suppress; the rail step precedes the pending-wake
    check.
11. **Missing remedy target is a load error** (finding 8): `remedy-target-missing` is a
    load-rejection fixture, replacing r2's runtime `unbound`.
12. **F1 registry is closed** (finding 4): remedies ∪ `producers.toml` (a loadset input) ∪
    `external_producer=true`; the error names the gate + missing kind (single form); F2 names both
    statutes.
13. **Load-rejection fixtures are duality-exempt, counted physically** (finding 9): I2 amended;
    each asserts one outcome, and a mechanism's `-raise`/`-clean` twin are **two** physical
    fixtures. The six load mechanisms are therefore 12 fixtures. `remedy-action-breadth` gained
    its negative case (gate satisfied → `:allow`, no remedy).
14. **Capstone teardown descoped** (finding 12): reviewer teardown is an org rail; the
    session-liveness observable is a named gap (§10 Q2).
15. **`no-git-restore` over-match is pinned** as an expected deny fixture.
16. **Round-5 concurrency & escalation representativeness** (r5 verdict): nine fixtures added for
    the requirements that landed after the census — episode fencing (`stale-claimant-fencing`),
    denied-dispatch retry (`denied-dispatch-release-retry`), per-statute closure
    (`multi-statute-episode-closure`), producer CAS+verdict atomicity (`producer-cas-verdict-txn`,
    aligning to p3's `insert_producer_verdict_in_txn`), the four-shape escalate effect at both
    actors with the **continue-the-fold bypass regression** (`escalation-return-dispatch`,
    `escalation-continue-the-fold`, `escalation-return-sweep`), frozen job provenance through the
    job world (`frozen-job-provenance`), and watermark nil/duplicate behavior
    (`watermark-nil-duplicate`). The `expect` enum gained `escalate-halt`/`escalate-open`/
    `escalate-park`/`escalate-continue`. Total is **72** everywhere (taxonomy, A2, census). The
    whole-lattice round added six more, all mechanics final: `iterate-rewake-target`,
    `unbound-reviewer-remedy`, `note-digest-exclusion` (C6), `orphaned-running-failed` (C4), and
    `sweep-never-consumes`, `adjudication-hold-order` (C7); the park fixtures adopted the ruled
    scope form `"<harness>:<identity_name>"` and the wake-first/recovered-check ordering, and the
    world vocabulary gained `sessions.adjudicationHold` (three-state), the `adjudicate` verb, and
    `producer_jobs` orphan (crash → `running→failed`, no requeue) semantics. With p3 r7, mech r9,
    and model-adjudication r11 final, **all fixtures are locked** to their confirmed constructs. The
    escalate trio is moot in v1 and goes green when the `escalation-substrate-v1` spec's adversarial
    review lands clean (§10 Q4).

---

## 9. Acceptance contract

- **A1.** `manifest.toml` registers all 8 classes; C1/C2/C3 green, C4–C7 + capstone pending with
  their `blocking_phase`.
- **A2.** **72 fixtures** exist to the §1.3/§1.4/§1.5 schemas (C6's 12 load-rejection fixtures are
  6 `-raise`/`-clean` twin pairs, counted physically); every **case-based** fixture has ≥1
  positive, ≥1 negative, ≥1 legibility case (I2, I3); load-rejection fixtures are duality-exempt
  and assert one load outcome each (I2). The runner fails the suite if a case-based fixture lacks a
  negative case, or if a load mechanism is missing either twin.
- **A2.1.** The round-5/6/7 concurrency/escalation additions are present and finalized to the p3
  r7 and mech r7 constructs — `frozen-job-provenance`, the escalation trio
  (`escalation-return-dispatch`, `escalation-continue-the-fold`, `escalation-return-sweep`),
  `producer-cas-verdict-txn` (`insert_producer_verdict_in_txn`), `denied-dispatch-release-retry`,
  `multi-statute-episode-closure` (`{decision, to_close, to_consume}`, `WHERE statute AND subject`),
  `stale-claimant-fencing` (occurrence-keyed `rail-dispatch:<statute>:<subject>:<occurrence>`;
  `claimToken` row-fencing only), `watermark-nil-duplicate` (`rail_step/4`, `nil`→`:fallthrough`),
  and `retired-holder-no-remedy` (pre-rail-step `holder_state` → `:stranded`). All are locked to
  their confirmed constructs, including the §D2.4 sweep-opens-DR-and-parks-holder rule; the escalate trio
  is moot in v1 pending `escalation-substrate-v1` (§10 Q4).
- **A3.** Every C1/C2/C3 green fixture executes real engine code (I5) both directions; every C1
  deny emits `[gate:<name>]`; every C2/C3 legibility case emits the `denied` payload via
  `EventLog.rail_denials/3`.
- **A4.** `c1-shipped-parity` passes against the live `engineering.toml`.
- **A5.** C5 fixtures carry the exit-band matrix (§4); the band-30 case is `pending-runtime`.
- **A6.** Every pending fixture is parsed, schema-validated, and reported against its blocking
  phase / §6-mapping row / runtime gap; the suite prints the census.
- **A7.** The codex probe, `c1-wiring-claude`, and the containment named dependency resolve.
- **A8.** The runner carries `compiled_hook_grep`, `rules_evaluate`, `rules_decide` + `acting_layer`,
  `handler_refusal`, and `load_assert`, and accepts `--corpus <root>` (I6).
- **A9.** Each roadmap P3–P7 Done criterion referencing "C<n> fixtures green" is satisfied by
  flipping that class here after its runner branch lands (§5).
- **A10.** Every fixture keyed to a P3 fact or a mechanism construct names it exactly as the
  companion specs define it (`Rules.decide/2`, `producer_jobs`, `files_overlap`,
  `Placement.holder_workdir/2`, the episode CAS states, the closed F1 registry); a rename in those
  specs is a diff this suite must track.

## 10. Open questions

- **Q1 — the two `pending-unhomed` fixtures.** `handoff-wake`/`handoff-assign` (a param-presence
  fact) and `two-changes-requested-revert` (a derived `changes-requested` count) are confirmed
  **not P3** and have **no planned home**. Authored to schema, census-reported against their
  §6-mapping rows; homing them is a roadmap decision.
- **Q2 — reviewer teardown / session-liveness observable.** `capstone-reviewer-loop`'s
  leak-prevention clause needs a reviewer-retired / session-liveness observable and the org
  teardown rail that gates on it; neither exists in the mechanism or P3. The clause is descoped
  and the gap named; it returns when that observable and rail land. Guidance §6's reviewer-loop
  worked example now matches this descope (team-lead edit this round), so no companion spec still
  gates completion on teardown — the set is coherent.
- **Q3 — the band-30 `pending-runtime` case.** `contained-refused` (sandbox profile-apply failure)
  is exercised by a fault-injected `sandbox-exec` harness, not fixture data. If the P4 runtime
  exposes a deterministic profile-apply-failure hook, this case flips from `pending-runtime` to a
  materializable fixture.
- **Q4 — all concurrency/escalation fixtures locked; escalation fixtures carry the
  escalation-substrate-v1 dependency.** With p3 r7 and mech r7 both final, all are locked to their
  confirmed constructs: `producer-cas-verdict-txn` (`insert_producer_verdict_in_txn(txn, map)`, CAS
  + verdict in one transaction, cancel-before-claim), `stale-claimant-fencing`
  (occurrence-keyed wire key `rail-dispatch:<statute>:<subject>:<occurrence>`, occurrence bumping
  only on provable termination; `claimToken` row-fencing only; `occurrence`+`rewakeCount` on the
  episode row), `denied-dispatch-release-retry` (lease DELETE, `blocked` recorded, edge-driven
  re-claim, no timer), `multi-statute-episode-closure` (`{decision, to_close, to_consume}`, actor
  closes `WHERE statute AND subject`), `watermark-nil-duplicate` (`rail_step/4`,
  `nil`→`:fallthrough`, no NULL write), and `retired-holder-no-remedy` (`holder_state` pre-checked
  → `:stranded`). The
  `escalation-return-sweep` `decision_pending` sub-case is locked to mech §D2.4: the sweep opens
  the decision-request (raiser = holder principal) and parks the holder via a substrate-created,
  holder-targeted park wake whose fallback `dueAt` = the DR's `deadlineAt` (org-configurable),
  idempotent via a stored `parkWakeId`; raiser-self-park is
  verb-edge-only; `escalation-substrate-v1` owns it. The escalate effect is a **load error until
  the `escalation-substrate-v1` spec's adversarial review lands clean** — the model is ratified;
  the clean review is what gates loading (mech §A1). So the escalation trio is **moot in v1** and
  goes green when that review passes — the one remaining forward dependency, named not invented.
- **Q5 — RESOLVED: mech r7 landed and its alignments are applied.** `stale-claimant-fencing` now
  asserts **one external effect per occurrence** — the wire key `rail-dispatch:<statute>:<subject>:<occurrence>`,
  `occurrence` bumping only on provable termination (dead + wire-inspected, never TTL), so a TTL
  reclaim collapses to one producer and a dead-live replacement makes a genuinely new one;
  `claimToken` is row-fencing only; episode rows carry `occurrence` + `rewakeCount`. The `rail_sweep`
  decision enum is `run-remedy | re-obligate | escalate-park | none`, and the escalation fixtures
  use the declared `escalate-park` token. `Rules.decide` returns `{decision, to_close, to_consume}`;
  `escalation-continue-the-fold` and `multi-statute-episode-closure` assert the triple and the actor
  consuming `to_consume` on a whole-fold `:allow`. The new `retired-holder-no-remedy` negative
  asserts `holder_state` is checked **before** the rail step (a retired holder → `:stranded`, no
  remedy). The **only** remaining forward dependency is Q4's escalation-substrate-v1 review-clean
  gate.
- **Q6 — RESOLVED: mech r9 landed.** The occurrence rule is locked: **any transition out of a
  TERMINAL episode state bumps `occurrence`; only the TTL-stale-claim (non-terminal, pre-live)
  reclaim preserves it.** `remedy-episode-idempotent` asserts the three reclaim branches —
  **reclaim-closed** (bump → observed-occurrence CAS → fresh wire key → genuinely new producer),
  **reclaim-stale-claim** (preserve → still-running original dedupes), **reclaim-dead-live**
  (bump); `fresh-occurrence-on-reopen` asserts close→re-fire→a distinct new producer. All fixtures
  touching `resolve/3` use the unified four-shape union `:allow | {:allow, ruling_id} | {:deny, e} | {:needs_request, dr_id|nil}`
  (non-nil `dr_id` = re-returned `{:decision_pending, dr_id}` without opening; `decide`'s escalate
  decision is `{:escalate, statute, ctx, dr_id}`). The **only** remaining forward dependency is
  Q4's escalation-substrate-v1 review-clean gate.
