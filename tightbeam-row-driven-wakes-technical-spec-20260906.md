# Row-driven wakes: technical specification (0.1.9)

Revision 1 — draft; Open Questions Q1–Q2 block affected clauses and review handoff.

Work item: `wi_fbcdf1a9-d3fc-4f17-ae1a-eb38ebc9facd`.
Spec assignment: `asg_26e06eec-4d09-4ecc-bb43-251acb9d82ac`.
Spec expert: session `agent:main:clawline:mike:main s_c86af874`.
Delivery owner: `orchestrator:row-driven-wakes-019`.

## Goal

Deliver G-A through G-D of the accepted row-driven-wake design: evaluate conditional
wakes and TOML rules through `Tightbeam.Rules`, recognize business-row changes directly,
and resume the accountable agent through the existing durable wake delivery path.
An assignment's valid continuation suppresses duplicate prods for that assignment.
Only a justified unresolved dependency qualifies for wait-aware effort treatment.

Controlling authority, in order:

1. Mike's Spirit, `tightbeam-specs@9eae6ad668b10707739a3eff4e57ac9c12fadd81:`
   `tightbeam-wait-spirit-20260906-mike.md`, SHA-256
   `ba377391d80433b735aca88ae5a104d9add82de86f8bc5e6c93f18fe62753964`, artifact `art_5f4f4acb`.
   Its Commission and Agreed turn-end rule control the earlier proposals.
2. Accepted design Revision 4, `tightbeam-specs@017380772ed0da242c5aacf3b135d3e80056fa3b:`
   `tightbeam-row-driven-wakes-design-20260906.md`, SHA-256
   `fae821d5e9a4f89ff273b20902f8c810f11c125d3dc771e0296f59b8940e691a`, artifact `art_388a1997`.
   PO verdict `att_3eb744f2` on `asg_5ac4d197` and binding acceptance `att_6a34a1ed`.
3. This document makes that design buildable; it does not reopen the accepted architecture.

Holds, verbatim from the assignment:

> 0.1.9-only scope; implementation held until this spec passes independent review; final Spirit acceptance before integration; no protected-ref landings on the code repo; no runtime/live-org action; gibson compile-only, no code execution there.

The specs-repository main landing is authorized. It is not a code-repository landing.

## Non-Goals

- NO assessor subsystem, NO duplicate matcher, NO cadence default.
- No new GenServer, blocker taxonomy, agent SQL, executable predicate code, arbitrary
  expression language, automatic recurring worker check, or automatic resolution of work.
- No new quota, credential, or capability observation producers. The fact vocabulary
  remains extensible when those producers acquire truthful durable rows.
- No arming of the staged review-rounds doorbell. `notice` enables it but does not elect it.
- No new progress/effect channel, effort-budget renewal from scheduling, or rewrite of
  closed work history. No removal of the existing typed recovery/accountability path.
- No 0.2.0 work, release, installation, deployment, gateway restart, or production-data repair.
- No fold/closure of another owner's cadence or prod-wording card. Design §7 controls
  reconciliation of `wi_2ef3d514`, `wi_fca19e0c`, `wi_c60c0189`, and `wi_c737aee7`.

## Terms

| Term | Exact meaning and source |
|---|---|
| Obligation | The open assignment whose next turn this wake supplies. `obligationRef` is `{kind:"assignment",id:<assignment id>}` in this MVP. `assignmentId` is the same id, not another scope. |
| Resolver | The existing assignment or decision request that owes the awaited action. `resolverRef` is `{kind:"assignment"|"decision_request",id:<id>}`. Its holder/addressee comes from its row. |
| Predicate | A nonempty list of the existing `{fact,op,value}` conditions, combined by AND, with explicit row bindings. It describes expected output, not the resolver's identity. |
| Existing-row binding | An exact row id whose existence and tenant are checked at registration. An unknown or inaccessible id refuses registration. |
| Future-output binding | A selector anchored to existing accountable work; its output row may be absent. Absence returns no match, not an invalid registration and not a success. Q1 controls the exact producer/review provenance. |
| Recognition | The durable choice that success, resolver-terminal reconsideration, or silence fallback warrants one notification. Recognition can precede eligibility to deliver. |
| Originating turn | The registrant's running ledger turn T, captured by the gateway, never asserted by the caller. Its terminal transition permits delivery and coverage evaluation. |
| Continuation | The registrant's prompt naming the action to take with the resulting state. It creates a fresh notification turn; it grants no authority to perform that action. |
| Prod coverage | Suppression of another prod for the exact obligation, while a qualifying pending wake or its queued/running continuation already supplies the next turn. |
| Effort relief | Exclusion of time spent in a policy-qualified unresolved dependency from the existing effort horizon. It preserves used budget and evidence watermarks. |
| Policy qualification | A TOML condition list evaluated by the same Rules evaluator against substrate facts. It is distinct from predicate truth and from semantic proof of progress. |
| Terminal | Assignment: `state=closed`, actual outcome `completed|surrendered|revoked`. Decision: status other than `open`, with integrity checks preserved. Work item: `closed|failed|iceboxed`. Turn: `delivered|canceled|failed|failed_unknown`. |

An assignment has no `failed` outcome at the pinned source. A failed continuation is a
terminal turn failure; an unsuccessful resolver assignment closes by surrender or revocation.
A legacy decision can already be `consumed`; current-state evaluation treats that as
terminal and reports it literally. Neither clarification adds a state to the source enums.

## Assumptions

1. The source baseline is code commit `f303dce752119a493030fcddbb1053ecbc314384` on 0.1.9.
   Paths and lines below were inspected statically at that exact commit.
2. `DB.transaction/2` uses `BEGIN IMMEDIATE`; `transaction_then/3` publishes after COMMIT
   before releasing the database owner (`lib/tightbeam/db.ex:55`, `:147`). Its callback
   must not synchronously call that same DB owner. The tick is the crash-recovery sweep.
3. `Rules` already owns the fact whitelist, operator types, nil semantics and AND-fold
   (`lib/tightbeam/rules.ex:114`, `:654`, `:1048`). It currently accepts only `verb` and
   `turn-end`, and `deny|remedy|escalate` (`:421`, `:433`). These are extension points.
4. `turns.wakeId` is UNIQUE; terminal ledger states are durable and one-way
   (`lib/tightbeam/ledger.ex:1`, `:44`). Repeated delivery attempts reuse that identity.
5. Artifact rows have a hash but no producing-assignment id
   (`lib/tightbeam/artifacts.ex:30`). Review qualification currently selects the newest
   holder-filed review conclusion across linked review cards, then tests independence;
   it has no content-hash binding (`lib/tightbeam/assignments.ex:373`). Q1 is not assumed solved.
6. `condition_facts` has no tenant column at this baseline
   (`lib/tightbeam/condition_facts.ex:61`). Legacy migration must establish tenant
   provenance or refuse ambiguous data; kind/scope equality cannot establish authority.
7. Existing effort accounting has a horizon and effect-channel watermarks
   (`lib/tightbeam/effort_checkin.ex:868`, `:1216`). Waiting is not a fourth effect channel.

## Invariants

Each invariant names its acceptance cases; those cases are the implementation contract.

- **I1 — One evaluator.** `Rules` validates and evaluates the same predicate representation
  for TOML productions, policy qualification, and ad hoc waits. Wakes owns selection and
  delivery, not a second truth evaluator. See A1, A2, L1.
- **I2 — Owner-scoped truth.** Each row read resolves under the wake's authenticated
  `ownerUserId`, including nested joins and legacy condition facts. Cross-owner matches
  do not create registrations, observations, or delivery. See A3, L2.
- **I3 — Accountable waiting.** A dependency names an existing resolver obligation.
  An output pointer, work-item owner, prompt, or asserted responsible party cannot
  substitute for that row. A resolver already terminal causes immediate recognition
  instead of becoming an unresolved wait. See B1–B4.
- **I4 — Two paths.** The success predicate and implicit resolver-terminal reconsideration
  remain armed independently. Composition narrows only success. See B5–B8.
- **I5 — Recognition is not delivery.** Registration evaluates both paths atomically with
  persistence. Delivery and coverage become eligible at T's terminal state. No elapsed-time
  proxy for T is allowed. See B2, B9, C1.
- **I6 — One notification.** Success, terminal reconsideration and fallback compete for one
  durable recognition and the existing wakeId delivery identity. Canceling a pending wake
  invalidates any undelivered recognition. See B10–B12.
- **I7 — Silence is not an outcome.** `dueAt` fires a one-shot fallback only when neither
  earlier path recognized a result. Known terminal failure does not wait for dueAt.
  See B6, B11.
- **I8 — Separate coverage and effort.** Coverage protects the obligation's pending or
  queued/running continuation. Only policy-qualified unresolved dependencies receive
  effort relief; ready-now work uses the normal budget. See C2–C7.
- **I9 — No synthetic advancement.** Creating, verifying, recognizing, delivering or
  replacing a wait does not reset the progress ladder, evidence cursors, or consumed
  effort. Capacity failure creates no completion, refusal, or effect credit. See C6–C8.
- **I10 — Reconsideration, not permission.** A delivered prompt names the actual disposition
  and instructs the recipient to reconsider its named next action. It never turns
  withdrawn, failed, iceboxed, or merely terminal into approval. See B7, B8, D3.

## Architecture

### G-A: extend the common Rules engine

**A-R1.** Add `row-commit` to the existing edges. At each supported business-row mutation
chokepoint, pass changed domain, exact row identity, principal and field transition to
recognition after commit. The engine selects pending waits by intersecting fact domains,
then evaluates their full predicates and resolver path. Domain indexing is candidate
selection only. The existing scheduler tick sweeps pending waits after missed publication.
Acceptance: A1–A2, B12.

The required producers are assignment opening/attests/closure/revocation; work-item
disposition; decision ruling/consumption/withdrawal/supersession; artifact recording and
relevant revision-binding writes; and genuine condition-fact recording. Existing terminal
mutation sites include `assignments.ex:1227`, `work_items.ex:429`, and
`escalation.ex:1131`; artifact insertion is `artifacts.ex:95`. Hook the owning write seam,
not just its CLI caller, so internal producers receive the same recognition behavior.
Turn-terminal observation supplies after-turn eligibility and continuation coverage.

**A-R2.** Add nonblocking `notice`: record the matching cause/principal and summon through
Wakes while allowing the operation. Matching notice rules do not short-circuit subsequent
deny rules or change the operation's authority. An ad hoc wait's RHS is this notice with
its target and continuation already bound. Do not activate the commented doorbell in
`priv/kungfu/agentic-engineering/rules/engineering.toml:126`. Acceptance: A1, D3.

**A-R3.** Expose a transaction-aware evaluation entry so registration and authoritative
recognition read one committed snapshot; do not call the DB GenServer recursively from
its own transaction. Share condition validation, fact computation and comparison with
the ordinary rule entry. Existing ordinary dispatch semantics need not change outside
this feature. Unknown facts/operators or invalid value types refuse registration/load;
nil fails every operator, including `ne` and `not_in`. Acceptance: A2–A4.

Required fact contracts (names below are the new public predicate vocabulary):

| Fact | Type | Binding and result |
|---|---|---|
| `work_item.state` | string | Exact `bindings.workItemId`; literal row state. |
| `assignment.state` | string | Exact `bindings.assignmentId`; `open|closed`. |
| `assignment.outcome` | string or nil | Same row; actual outcome, nil while open. |
| `decision_request.status` | string | Exact `bindings.decisionRequestId`; literal disposition. |
| `artifact.present` | boolean | True only when the complete bound identity/selector matches a hashed artifact; false for absent future output. Q1 supplies provenance. |
| `artifact.content_sha256` | string or nil | Hash of the same bound artifact; no cross-row pairing. |
| `review.qualifying_verdict_kinds` | list of strings | Qualifying conclusion for the bound producer and exact artifact revision; Q1 supplies the recorded revision link. |
| `condition_fact.matches` | boolean | Legacy event selector: owner, kind, optional scope and `conditionAfterId`; event id must be strictly greater than its registration cursor. |

Bindings are a separate validated object, not arbitrary SQL or interpolated fact names.
The MVP supports one identity/selector per named domain in a predicate; the artifact and
review facts share one artifact-revision binding. Conditions retain `{fact,op,value}`
and the existing operators `eq ne gt gte lt lte in not_in`. `in` expresses alternatives
within a disposition set. It does not add an OR expression language.

Default terminal builders expand to ordinary conditions:

```json
[{"fact":"assignment.state","op":"eq","value":"closed"}]
[{"fact":"decision_request.status","op":"in","value":["ruled","consumed","withdrawn","superseded"]}]
[{"fact":"work_item.state","op":"in","value":["closed","failed","iceboxed"]}]
```

These are convenience expansions, not a closed catalog of allowed predicates.
A caller can narrow work-item success to `closed`; resolver terminal reconsideration
still fires when success becomes impossible through resolver termination. A4, B5–B8
verify the fact semantics without requiring new domain producers.

### G-B: durable waits, registration and delivery

**B-R1 — request.** Extend `wake` with a structured `--predicate` JSON object and
`--assignment <id>` for the covered obligation. The predicate object contains
`conditions`, `bindings`, and `resolverRef`. Existing `--prompt` is the continuation;
existing `--fallback-after` or `--at` supplies required `dueAt`. An actionable ready-now
continuation uses `--after-turn` with `--assignment` and `--prompt`; it has no fabricated
resolver or dependency. Its due time is registration time, held behind originating-turn
eligibility. `--after-turn` and `--predicate` are mutually exclusive. An agent-created
predicate wake automatically captures T; the caller cannot choose an earlier turn.
The gateway refuses `--after-turn` when no running originating turn exists. A predicate
registration outside a running turn is immediately eligible. Acceptance: B1–B4, C1.

New request fields are proposed implementation syntax, not available commands before
G-B ships. The generic JSON object avoids introducing one CLI flag per row domain.

Persist these logical fields on the existing wake row (physical JSON/text columns may
follow the repository's schema conventions):

| Field | Required meaning |
|---|---|
| `ownerUserId` | Gateway-derived principal owner; immutable. |
| `assignmentId`, `obligationRef` | Same exact assignment; required for new covering wakes. Existing unrelated wakes retain no coverage. |
| `predicate` | Canonical validated conditions and row bindings; dependency mode only. |
| `resolverRef` | Existing accountable assignment or decision request; dependency mode only. |
| `originatingTurnSeq` | Captured running T, or null for an eligible registration outside a turn. |
| `prompt` | Explicit continuation. |
| `dueAt` | Mandatory fallback for dependency mode; immediate eligibility time for ready-now mode. |
| recognition fields | Time, path (`success|resolver-terminal|fallback|after-turn`), predicate evidence, resolver disposition and triggering row transition. Null before recognition. |

Wakes is the sole mutation seam for registration, recognition, typed cancellation and
delivery. It inserts the wake and its coherent sidecar in one transaction. Existing
ledger enqueue is the sole mutation seam for the resulting turn. Row-domain owners
continue to own business-state transitions. No second wait registry is introduced.

**B-R2 — registration transaction.** Resolve/authenticate the owner, validate types and
references, evaluate admission, capture T and legacy cursor if applicable, persist wake
and sidecar, and evaluate both firing paths in the same transaction. Return wake id,
recognition path or null, and eligibility. Refusal leaves neither wake nor sidecar.
If success holds, recognize success; otherwise if the resolver is terminal, recognize
resolver-terminal. A terminal resolver is the immediate-evaluation exception to the
open-resolver rule, not an accepted unresolved dependency. Acceptance: B1–B4, A3.

**B-R3 — subsequent recognition.** A relevant committed transition evaluates the full
success predicate and the independent resolver-terminal path. When both hold in the
same snapshot, stamp success and include the resolver's actual terminal disposition.
An AND's unsatisfied member cannot suppress the terminal path. Recognition is durable
before delivery eligibility and remains latched if later state changes; delivery is a
notification to reread current state, not a claim that the older snapshot still holds.
Acceptance: B5–B9.

**B-R4 — eligibility and once-only delivery.** An originating turn is eligible when its
ledger status is terminal, including failure/cancellation. Recheck wake state and
eligibility and claim the single delivery atomically; enqueue with the same wakeId.
Keep the existing target gate, role resolution, retry ladder and terminal recovery.
Do not create a queued continuation before T ends merely because the ledger would
serialize its execution later. Cancellation wins if it commits before enqueue;
after enqueue the existing typed cancellation/turn rules govern. Acceptance: B9–B12.

**B-R5 — stamp.** Extend `[woke: …]` with wake id, covered assignment, recognition path,
predicate/binding evidence, resolver identity and derived holder/addressee, and actual
row/field old→new. Registration against existing truth is labeled `registration-snapshot`
with the observed value; it must not invent an earlier transition. Fallback says the
resolver was silent through dueAt; it does not say the dependency cleared. Append the
registrant's prompt without rewriting it. Acceptance: B2, B7, B8, B11.

**B-R6 — compatibility.** Preserve `--when-fact <kind> [--when-scope <scope>]` with a
mandatory fallback. Normalize it to `condition_fact.matches` through Rules. Preserve
future-event cursor semantics, including wildcard scope when omitted. Legacy event
wakes do not acquire a fake resolver or effort relief; the two resolver paths apply to
new row-dependency wakes. Preserve existing scheduled wake and retry behavior.
Retire `candidate_sql/1`'s independent condition matcher and the authoritative re-match
inside `fire_in_txn/2` (`wakes.ex:2823`, `:2926`). Shared delivery remains. Acceptance: L1–L3.

**B-R7 — tenant migration.** Store authenticated owner provenance with newly produced
condition facts, including internal producers. An internal business transition derives
owner from the owning business row. Resolve legacy provenance through its recorded
session/user origin and owning references, not scope spelling. Historical system facts
without a unique owner do not qualify for cross-tenant matching: migration reports their
ids and refuses an ambiguous conversion rather than assigning them to the current caller.
Migration preserves closed rows and the registration cursor; it does not manufacture
business facts for assignments, artifacts, reviews or work items. Acceptance: L2–L3.

### G-C: coverage and effort

**C-R1 — scoped coverage.** Replace session-wide queued/running coverage at
`supervision.ex:3132` and holder-oldest selection at `:1313` with per-obligation
evaluation. A queued/running continuation joins through `turns.wakeId` to the admitted
wake's matching `assignmentId` and `obligationRef`. A prose assignment mention does not
join. Pending coverage requires T terminal and a coherent admitted sidecar. Evaluate
coverage and prod claim in one transaction so a competing continuation cannot be ignored
between the check and action. Watermarks follow the same obligation scope. C1–C4 verify it.

**C-R2 — sidecar.** Extend `controllerOrigin` with `holder_continuation`, and add exactly
that coherent branch to `schema.ex:288` and its insert trigger at `:684`. This branch
requires a prompt wake, matching open assignment, authenticated authorized registrant,
captured turn and matching obligationRef. It carries neither a charged prod generation
nor a fabricated `wakeKind=prod`. Existing scheduled and retirement branches retain
their checks. The sidecar's pending→settled transition follows delivery/cancellation;
the ledger join supplies coverage after enqueue. Acceptance: C1–C4, C8.

**C-R3 — separate effort policy.** A dependency qualifies only while its resolver is open,
another accountable party owes it, no success/terminal/fallback recognition has occurred,
and justification passes the TOML evidence rule (Q2). Ready-now pending/queued/running
continuations remain covered but use normal effort. Scheduling does not reset an effort
generation, extend the unused budget repeatedly, or count as progress. Acceptance: C5–C7.

Pause the existing effort horizon for the actual qualifying interval and preserve the
remaining budget. When qualification ends, resume from that remainder, not a fresh
horizon. Qualification transitions and accounting updates must be atomic and durable;
restart cannot lose a pause or grant it twice. Overlapping qualifying waits for one
assignment exclude the union of their intervals, not their sum. The policy determines
qualification; the engine measures the interval. Do not change configured horizon,
multiplier, progress receipts, or effect-channel cursors. Acceptance: C6–C7.

**C-R4 — failure.** Coverage from a queued/running continuation ends on any terminal
turn state. If the obligation remains open and has no other covering wake, the next
evaluation can prod under existing recovery. A pending dependency elsewhere still
covers only on its own valid rows. Capacity death, `failed`, and `failed_unknown` do
not answer a prod, consume the assignment, or grant evidence. Acceptance: C8.

### G-D: TOML admission and qualification; operating pattern

Use the existing Rules TOML loader and evaluator. Admission remains an ordinary
`[[rule]]` at the wake verb. Add named predicate-only policy declarations to the same
loader for read-only qualification. They use the existing condition grammar and fact
registry; they do not create another rule engine, worker, or effect dispatcher.

Policy schema:

```toml
[[policy]]
name = "holder-continuation-coverage"
purpose = "wait-prod-coverage"
when = [
  { fact = "wait.obligation_matches", op = "eq", value = true },
  { fact = "wait.admitted", op = "eq", value = true },
  { fact = "wait.after_turn_eligible", op = "eq", value = true },
  { fact = "wait.continuation_state", op = "in", value = ["pending", "queued", "running"] },
]

[[policy]]
name = "justified-unresolved-dependency"
purpose = "wait-effort-relief"
when = [
  { fact = "wait.obligation_matches", op = "eq", value = true },
  { fact = "wait.admitted", op = "eq", value = true },
  { fact = "wait.after_turn_eligible", op = "eq", value = true },
  { fact = "wait.continuation_state", op = "eq", value = "pending" },
  { fact = "wait.recognized", op = "eq", value = false },
  { fact = "resolver.open", op = "eq", value = true },
  { fact = "resolver.owed_by_other", op = "eq", value = true },
  { fact = "wait.justification_qualified", op = "eq", value = true },
]
```

`policy` is an additional array-of-tables root in the existing rule files. Each table
requires exactly `name`, `purpose`, and nonempty `when`. Names use the existing rule-name
syntax and are unique across the loaded rule/policy set. Purpose is exactly
`wait-prod-coverage` or `wait-effort-relief`. No `effect`, remedy or check script is valid
inside a policy. Unknown keys/facts, unsupported purpose, empty conditions, duplicate
names and type errors fail loading with file/policy/condition location. Conditions AND-fold;
multiple declarations for one purpose qualify if any one matches. No matching declaration
means no qualification. Candidate selection never substitutes for condition evaluation.

Each policy query binds one candidate wake, one obligation and one owner, with a fresh
fact cache. `wait.continuation_state` is pending for an uncanceled, undelivered wake;
queued/running for its ledger continuation; terminal otherwise. `wait.admitted` refers
to successful admission and coherent durable provenance, not to prompt wording.
`resolver.open` is false for terminal or absent resolvers. `resolver.owed_by_other`
compares the derived resolver principal to the covered assignment holder. An owner user
is a distinct accountable party from that user's agent. Q2 defines justification evidence.

Admission example, an ordinary loaded rule rather than a compiled self-block ban:

```toml
[[rule]]
name = "wake-obligation-registration-authority"
verb = "wake"
edges = ["verb"]
effect = "deny"
text = "Register this obligation wake as its holder or through an authorized ancestor."
deny_when = [
  { fact = "wake.has_obligation", op = "eq", value = true },
  { fact = "wake.registrant_is_holder", op = "eq", value = false },
  { fact = "wake.registrant_is_ancestor", op = "eq", value = false },
]
```

The gateway computes holder/lineage facts from recorded sessions and assignment ownership.
It rechecks admission inside registration to prevent a stale preliminary dispatch read
from granting coverage. Who qualifies is TOML policy; tenant isolation, valid references,
mandatory fallback, coherent sidecar and typed transitions remain substrate constraints.
The shipped policy must implement the accepted matrix, not merely provide a configuration
example. Tests replace policy in an isolated org to prove qualification follows TOML.
See D1–D2 and Q2.

Operating pattern established: **obligation-scoped after-turn continuation**. It applies
when an agent ends a turn with an unfinished assignment. It does not replace timed
rechecks of external systems with no observable rows, or invent a resolver for ready work.

The following is the proposed replacement text for the existing manual's relevant
instrument, held for activation with G-D's shipped CLI; it is not current command guidance:

> Before ending a turn with unfinished actionable work, schedule its next wake with
> `wake --assignment <id> --after-turn --prompt "<concrete next action>"`.
> For a row dependency, open or link the assignment or decision request that owes the
> action. Register its predicate, resolver, covered assignment, continuation and fallback
> with `wake --assignment <id> --predicate '<object>' --fallback-after <duration>
> --prompt "<action to reconsider with the result>"`.
> A wake covers only the named obligation. Its queued or running continuation keeps that
> coverage. Scheduling is a plan, not advancement. Read the actual disposition before
> acting; delivery supplies no permission.

Land this amendment in the canonical guidance source through the identity seam when
the commands exist. G-D also carries a migration note: legacy syntax remains compatible
through the common evaluator; no deadline forces callers to convert. Verify actual CLI
help, parser and output before activating the amendment (wisdom 20–22). Acceptance: D3.

## Acceptance

Tests use isolated fixtures on **eezo or racter**, over SSH, through unmodified
`scripts/verify_mix.sh`. Name the actual host and candidate commit in every gate attest.
Use source fixtures for SQL/state properties; no invented live observation capture.
No tests, probes, gates or checkout code execute on gibson. If the remote host fails
for host/toolchain reasons, record the blocker and stop that run; do not fall back.
CLI changes also receive the applicable Rust gate on the remote host.

The following matrix is carried **verbatim from accepted design §4**:

  | Wait state | Prod coverage | Effort accounting |
  |---|---|---|
  | Unresolved justified dependency | Covered | Wait-aware effort policy |
  | Ready-now pending / queued / running continuation | Covered | Normal effort burn |
  | Unrelated wake (no obligationRef match) | No coverage | Normal |
  | Terminally failed continuation | Coverage ends | Existing recovery/accountability |

### Executable cases

Each case must exercise the real registration/evaluation/delivery or supervision seam
and assert durable rows, not a helper that repeats its own implementation. Fixture ids
below stand for rows created by those seams. `H1` and `H2` are distinct SHA-256 values.

| Case | Given / When / Then |
|---|---|
| A1 (I1) | Given identical supported conditions in a TOML notice and an ad hoc wait, when the business row commits a satisfying change, then both use Rules recognition, the notice records/summons without denying the write, and the wait reaches the shared wake delivery path. A later deny rule still denies its own governed operation. |
| A2 (I1,I5) | Given a row update that rolls back, when recognition would match its uncommitted value, then no recognition or notification commits. Given a committed change whose publication is interrupted, when the existing tick runs, then the pending wait is recognized once. |
| A3 (I2) | Given an owner-A registration naming an owner-B obligation, resolver, output or review, when registering, then reject without wake/sidecar and without exposing the other owner's value. A future-output selector anchored to A cannot match B's later output. |
| A4 (I1) | Given unknown fact/operator, malformed value, or an existing-row id that is absent, when registering, then refuse without a wake. Given absent future output, when evaluating `ne` or `not_in` against a nil fact, then no success is recognized. |
| B1 (I3) | Given open assignment A held by S and open resolver R held by another accountable party, when S registers valid conditions, fallback and continuation for A, then one admitted wake and coherent sidecar persist. Given a work-item id or artifact pointer as resolverRef, then registration refuses. |
| B2 (I3,I5) | Given output H1 and its qualifying review already exist while T runs, when an otherwise valid wait registers, then success recognition commits immediately with registration-snapshot evidence, no continuation turn exists yet, and T terminal permits exactly one enqueue. |
| B3 (I3,I5) | Given R already surrendered, withdrawn or superseded and success false, when registration occurs during T, then resolver-terminal recognition commits immediately with the actual disposition, and delivery waits for T terminal. It never receives unresolved-dependency effort relief. |
| B4 (I3) | Given R exists but its future output does not, when a producer-bound output predicate registers, then it remains pending. When a different assignment by the same holder on the same work item records an artifact, then no match occurs. R's exact bound output can satisfy it. Q1 governs executable binding. |
| B5 (I4) | Given output H1 exists and the clean-review conjunct is false, when R terminates without the clean review, then the resolver-terminal path recognizes at that commit, before dueAt, regardless of the false conjunct. |
| B6 (I4,I7) | Given success false and R closes as surrendered/revoked or its decision is withdrawn/superseded, when that transition commits, then one resolver-terminal notification becomes eligible after T, without advancing the clock to fallback. |
| B7 (I4,I10) | Given default terminal predicates, when a work item becomes iceboxed or failed, an assignment surrendered, or a decision withdrawn, then success includes the actual disposition. A narrow work-item `closed` predicate does not call iceboxed success; if R then terminates it uses path 2. |
| B8 (I4,I10) | Given producer P has an older clean review of H1 and the wait expects H2, when evaluating, then H1 cannot satisfy H2. Given an applicable later changes-requested conclusion, then the earlier clean conclusion cannot win. Terminal revocation/closure of R still triggers reconsideration. Q1 governs exact binding. |
| B9 (I5) | Given recognition occurs during T and the observed row changes again before T ends, when the gateway restarts and T becomes terminal, then one notification carries the recorded recognition and prompts a reread. No notification is enqueued while T is running. |
| B10 (I6) | Given success, resolver termination and fallback race, when their transactions serialize, then one recognition wins and `turns.wakeId` yields one continuation. Given cancellation commits first, then no later recognition or enqueue occurs. |
| B11 (I7) | Given R stays open, no success occurs and dueAt passes, when the tick evaluates, then one fallback is recognized, stamped silence rather than success, and delivery still respects T. The fallback does not automatically rearm the wait. |
| B12 (I6) | Given a crash after recognition or enqueue but before marking delivery, when the gateway restarts, then pending delivery reuses wakeId and does not duplicate the continuation. Existing target refusal/retry behavior and typed cancellation remain observable. |
| C1 (I5,I8) | Given A's wait registers during T, when supervision evaluates before T terminal, then the new wait grants no after-turn coverage yet. In the transaction observing T terminal, a valid pending or enqueued continuation suppresses a duplicate prod for A. |
| C2 (I8) | Given S holds A and B and has a valid pending dependency wake for A, when supervision evaluates both, then A is covered and B remains independently eligible. Repeat with a ready-now pending wake, and with A's queued/running continuation; the result is unchanged. |
| C3 (I8) | Given the executive specimen shape (`w_9639742e`, `w_181be052`: prose named work but assignmentId was null), when fixtures register the equivalent new wakes with typed A/B scope, then prods corresponding to 118974/118975/118976 are suppressed only for the covered obligations. Legacy null/prose-only wakes earn no new coverage. |
| C4 (I8) | Given A's continuation is queued, then running, when successive supervision evaluations occur, then no duplicate prod is issued. When it completes with A open and no next wake, then prod eligibility resumes at the next evaluation. |
| C5 (I8) | Given two otherwise equivalent covering wakes, one justified unresolved dependency and one ready-now continuation, when effort is accounted, then only the first receives relief. Self-owed R does not qualify as another-party dependency. |
| C6 (I9) | Given an effort generation with used budget U and unchanged effect cursors, when a wait registers, is replaced, or is recognized, then U and cursors do not reset and no effect is credited. A qualifying interval pauses only the remaining horizon; ending it resumes the same remainder. |
| C7 (I8,I9) | Given overlapping qualifying intervals and a gateway restart, when relief is reconciled, then their union is excluded once and used effort survives. When success, terminal reconsideration, cancellation or fallback occurs, then relief ends even while the continuation stays covered. |
| C8 (I9) | Given a covered continuation dies on model capacity, failed or failed_unknown, when its terminal row commits, then its coverage ends, A remains open, no effect/refusal/progress credit is created, and existing recovery handles the failure. An independently valid open dependency covers only on its own merits. |
| D1 (I1,I8) | Given valid qualification TOML, when its condition changes in an isolated fixture and policy reloads, then coverage/effort qualification follows that policy without a binary change. Neither policy change can permit a cross-tenant read or waive a missing fallback. |
| D2 (I3,I8) | Given holder, ancestor and unrelated same-owner registrants, when each registers an obligation wake, then the shipped admission rule admits the first two and refuses the third. A well-formed but unjustified claimed dependency fails effort qualification; it cannot renew evidence budget. Q2 supplies the verification record. |
| D3 (I10) | Given compiled CLI help/parser and the amended manual example, when the example runs in an isolated remote org, then it registers the documented rows and delivers a notification with the prompt intact. Staged doorbell remains unarmed; no cadence configuration changes. |
| L1 (I1) | Given a legacy kind/scope wake with cursor N, when fact N already exists, then it does not fire. When same-owner matching fact N+1 is recorded, then Rules recognizes it. Omitted scope retains wildcard semantics. A code inspection finds no independent authoritative matcher in Wakes. |
| L2 (I2) | Given identical kind/scope in two tenants, when a fact arrives for B, then A's wake remains pending. Given an old system fact with ambiguous owner provenance, migration reports/refuses that ambiguity and never silently grants A visibility. |
| L3 (I1,I6) | Given an upgrade fixture with pending legacy condition wakes, ordinary timed wakes, canceled/fired wakes and delivery retries, when migrated and restarted, then pending work retains cursor/fallback/identity, closed history is unchanged, and deliveries use the retained shared path. |

Traceability: G-A implements A-R1–A-R3 (A1–A4); G-B implements B-R1–B-R7
(B1–B12, L1–L3); G-C implements C-R1–C-R4 (C1–C8); G-D implements policy and
the operating amendment (D1–D3). Cross-cutting invariants are cited by each case.
Build order is G-A → G-B → G-C → G-D through the same implementation seam.

Spec handoff requires this canonical file in tightbeam-specs main, exact SHA-256 artifact
row, a completed cold digest, and an independent spec review. The orchestrator returns
the review verdict to the spec expert. After a clean review, bind the work item's
implementation specRef/hash to those reviewed bytes. Implementation then returns remote
gate evidence and fresh independent code review to the orchestrator; final Spirit
acceptance precedes integration and does not itself lift the protected-ref landing hold.

## Open Questions

- **Q1 — BLOCKING: exact output/review provenance.** The accepted design requires future
  output of an exact assignment and a verdict over an exact `contentSha256`. The pinned
  schema has neither an artifact→producer-assignment link nor a review-verdict→revision
  link. `createdBySession + workItemId` and `reviewsAssignmentId` alone are insufficient
  when a holder has several assignments or a producer has multiple revisions. Raised
  in progress `att_e4e85a8f-31e3-4d22-baf6-1d5cc4e746ea`, wake `w_8d5c3712` to the
  orchestrator. Proposed minimum: typed provenance at existing artifact-record/attest
  seams. Await the owning ruling before specifying that mutation contract. Blocks exact
  artifact/review facts and B4/B8, not engine or coverage drafting.
- **Q2 — BLOCKING: semantic justification evidence.** Resolver existence/open state and
  another accountable party prove an action is owed, not that this work depends on it.
  The accepted design assigns qualification to rails without naming the evidence those
  rails read. The same attest/wake asks the orchestrator to identify the durable evidence
  contract. No assessor subsystem or self-asserted necessity flag is assumed. Blocks
  `wait.justification_qualified`, final effort policy and D2/C5 qualification cases.
- **Q3 — NON-BLOCKING: legacy deprecation horizon.** Follow design §8: indefinite syntax
  compatibility until separately ruled. No forced migration deadline.
- **Q4 — NON-BLOCKING: additional row domains.** The required domains above implement the
  accepted examples. New observable domain facts can extend the existing fact seam;
  observation producers and their semantics require their own authority.
