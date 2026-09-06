# Row-driven wakes: technical specification (0.1.9)

Revision 4 — review B1 corrected; cold digest pending before bounded rereview.

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
3. Orchestrator Gap-1/Gap-2 ruling, message `s_92a833e5-5a85-495b-b743-ca42318fa6ea`;
   Gap-2 amendments `s_33d4038f-c57a-441f-a075-70534eada151` and, controlling,
   `s_936bcb33-ffeb-4e53-a907-bda184a5c2c6` under parent fidelity ruling `att_ac0d162e`.
   Mechanical admission and semantic verification are distinct. Every dependency needs
   accountable verification/challenge; unresolved verification is explicitly provisional.
   Resolver disposition proves resolution, not necessity. No permanently unverified class.
4. This document makes that design buildable; it does not reopen the accepted architecture.

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
- Output/review provenance uses additive nullable columns and optional flags only: no
  backfill, new table, subsystem or native code. Existing completion-rail review
  qualification remains unchanged; the new revision binding serves wait predicates only.
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
| Future-output binding | A selector anchored to existing accountable work; its output row may be absent. Absence returns no match, not an invalid registration and not a success. `producedByAssignmentId` identifies the producer. |
| Recognition | The durable choice that success, reconsideration, or silence fallback warrants one notification. Reconsideration names resolver termination or the ruled verification cause. Recognition can precede eligibility to deliver. |
| Originating turn | The registrant's running ledger turn T, captured by the gateway, never asserted by the caller. Its terminal transition permits delivery and coverage evaluation. |
| Continuation | The registrant's prompt naming the action to take with the resulting state. It creates a fresh notification turn; it grants no authority to perform that action. |
| Prod coverage | Suppression of another prod for the exact obligation, while a qualifying pending wake or its queued/running continuation already supplies the next turn. |
| Effort relief | Exclusion of time spent in a policy-qualified unresolved dependency from the existing effort horizon. It preserves used budget and evidence watermarks. |
| Policy qualification | A TOML condition list evaluated by the same Rules evaluator against substrate facts. It is distinct from predicate truth and from semantic proof of progress. |
| Verification | A holder-filed judgment on an existing named verification assignment, bound to the exact wake. It confirms or challenges declared necessity; it is not inferred from the resolver's disposition. |
| Provisional | An admitted unresolved dependency whose named verifier has not confirmed necessity. Its rows name that verifier and the pass/challenge transition that ends provisional status. |
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
   it has no content-hash binding (`lib/tightbeam/assignments.ex:373`). A-R4 adds the
   ruled wait-specific provenance without changing that existing completion-rail query.
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
- **I4 — Two paths.** Success and implicit reconsideration remain armed independently.
  Reconsideration observes resolver termination; the later verification ruling also sends
  verification challenge through this path. Composition narrows only success. See B5–B8, V2.
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
- **I11 — Verification stays accountable.** Every admitted dependency has an existing
  verification obligation and a bounded verification transition. Pending verification
  is labeled provisional; passing confirms; challenge ends coverage and relief. Resolver
  success or rejection proves neither necessity nor advancement. See V1–V4.

## Architecture

### G-A: extend the common Rules engine

**A-R1.** Add `row-commit` to the existing edges. At each supported business-row mutation
chokepoint, pass changed domain, exact row identity, principal and field transition to
recognition after commit. The engine selects pending waits by intersecting fact domains,
then evaluates their full predicates and resolver path. Domain indexing is candidate
selection only. Post-commit recognition runs before the database owner admits the next
business mutation, with owner-local database access rather than a recursive GenServer
call. The existing scheduler tick sweeps pending waits after missed publication.
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
For loaded notice rules, extend the existing rule schema with `[rule.notice]`: exactly
one of `target_role` or `target_session`, plus nonblank `prompt`. Reuse existing target
resolution and whole-field/prompt binding tokens; reject unknown keys or unsupported
tokens at load. Require this table for `effect="notice"`; reject it for other effects.
For ad hoc waits the persisted target/prompt supply that same RHS, with no TOML lookup.

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
| `artifact.present` | boolean | True only when the complete bound identity/selector matches a hashed artifact; false for absent future output. A-R4 supplies provenance. |
| `artifact.content_sha256` | string or nil | Hash of the same bound artifact; no cross-row pairing. |
| `review.qualifying_verdict_kinds` | list of strings | Qualifying conclusion for the bound producer and exact artifact revision, using A-R4's recorded revision link. |
| `condition_fact.matches` | boolean | Legacy event selector: owner, kind, optional scope and `conditionAfterId`; event id must be strictly greater than its registration cursor. |

Bindings are a separate validated object, not arbitrary SQL or interpolated fact names.
The MVP supports one identity/selector per named domain in a predicate; the artifact and
review facts share one artifact-revision binding. Conditions retain `{fact,op,value}`
and the existing operators `eq ne gt gte lt lte in not_in`. `in` expresses alternatives
within a disposition set. It does not add an OR expression language.
On `row-commit`, a loaded rule's existing `verb` selects the originating mutation verb;
the changed-row context supplies its domain bindings. An ad hoc wait uses its own stored
bindings instead. A callback carrying several changed rows evaluates each relevant
candidate with one consistent committed snapshot; it does not splice fact values from
different snapshots into an AND.

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

**A-R4 — additive output and review binding.** Add nullable
`artifacts.producedByAssignmentId REFERENCES assignments(id)`. Populate it through
`artifact-record --produced-by-assignment <id>`; omission leaves null rather than
guessing among the filer's assignments. Validate that the referenced producer exists,
is held by the filer, belongs to the artifact's work item and shares its owner.
`Artifacts.record` remains the mutation seam. Existing artifact calls remain valid.

Add nullable `attests.artifactId REFERENCES artifacts(artifactId)` and
`attests.contentSha256`. `attest --kind verdict --artifact <id> --sha256 <hash>` supplies
the pair, or omits both for a legacy verdict. Validate the hash against the named artifact
and the artifact's typed producer against the review card's `reviewsAssignmentId`;
reject a partial pair, mismatch or cross-owner link. `Assignments.attest` remains the
mutation seam. Holder-filed and independent-review requirements still apply.
No legacy artifact/attest is backfilled, and no existing completion gate changes.

`bindings.artifact` is exactly one of:

- `{ "artifactId": "art_A", "contentSha256": "H1" }`: the row must exist at registration;
  the hash expectation can be false, but cannot silently select another artifact.
- `{ "producedByAssignmentId": "P", "contentSha256": "H1" }`: P must exist; the output
  can arrive later. The hash is optional only for a future output whose revision is
  not yet fixed. Each candidate is a hashed artifact with that exact producer link.

For future output, evaluate the artifact/review conjunction against one candidate artifact
at a time; it succeeds if one candidate satisfies the entire conjunction. A review for
H1 cannot combine with another artifact H2. If the hash is not known at registration,
the matching artifact row and its hash supply the exact revision, and the stamp names
both. The review verdict must still carry that exact id/hash; revision binding is never
optional on the satisfying verdict.

For a candidate revision, select the most recent holder-filed `reviewed-clean` or
`changes-requested` conclusion among linked review cards whose typed artifact/hash
binding matches that revision; order by verdict timestamp then rowid. Only a clean
winner held independently of P qualifies. Unbound legacy verdicts cannot satisfy this
fact. They continue to participate in the original completion-rail query exactly as
before. A newer verdict for another revision is not a verdict on this revision.
Acceptance: B4, B8, V5.

### G-B: durable waits, registration and delivery

**B-R1 — request.** Extend `wake` with a structured `--predicate` JSON object and
`--assignment <id>` for the covered obligation. The predicate object contains
`conditions`, `bindings`, `resolverRef`, `necessity`, and `verificationRef`.
`necessity` is nonblank declared dependency rationale, stored as audit evidence;
`verificationRef` names an existing verification assignment under B-R8.
Existing `--prompt` is the continuation;
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
| `necessity`, `verificationRef`, `verificationState` | Declared rationale, existing verifier assignment, and `provisional|confirmed|challenged`; dependency mode only. |
| `originatingTurnSeq` | Captured running T, or null for an eligible registration outside a turn. |
| `prompt` | Explicit continuation. |
| `dueAt` | Mandatory fallback for dependency mode; immediate eligibility time for ready-now mode. |
| recognition fields | Time, path (`success|reconsideration|fallback|after-turn`), reason (`resolver-terminal|verification-challenged|verification-terminal` for reconsideration), predicate evidence, disposition and triggering row transition. Null before recognition. |

Wakes is the sole mutation seam for registration, recognition, typed cancellation and
delivery. It inserts the wake and its coherent sidecar in one transaction. Existing
ledger enqueue is the sole mutation seam for the resulting turn. Row-domain owners
continue to own business-state transitions. No second wait registry is introduced.

**B-R2 — registration transaction.** Resolve/authenticate the owner, validate types and
references, evaluate admission, capture T and legacy cursor if applicable, persist wake
and sidecar, and evaluate both firing paths in the same transaction. Return wake id,
recognition path or null, and eligibility. Refusal leaves neither wake nor sidecar.
If success holds, recognize success; otherwise if the resolver is terminal, recognize
path reconsideration with reason resolver-terminal. A terminal resolver is the
immediate-evaluation exception to the open-resolver rule, not an accepted unresolved dependency. Mechanically admitted unresolved
dependencies start provisional with their named verifier; relief may start at registration
under policy, independently of after-turn prod coverage. Acceptance: B1–B4, A3, V1.

**B-R3 — subsequent recognition.** A relevant committed transition evaluates the full
success predicate and the independent resolver-terminal path. When both hold in the
same snapshot, stamp success and include the resolver's actual terminal disposition.
An AND's unsatisfied member cannot suppress the terminal path. Recognition is durable
before delivery eligibility and remains latched if later state changes; delivery is a
notification to reread current state, not a claim that the older snapshot still holds.
The first recognition is immutable. Later verification evidence remains on its attest,
but does not overwrite an earlier firing or produce a second notification. A verification
challenge that wins recognition ends coverage under B-R8. A later cancellation can still
cancel undelivered notification under B-R4.
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
ids and refuses their owner attribution rather than assigning them to the current caller.
That refusal leaves those historical rows unscoped; it does not block conversion of
unrelated rows. Unscoped facts cannot satisfy an owner-bound wake. A pending legacy wake
retains its fallback when no safely scoped fact matches.
Migration preserves closed rows and the registration cursor; it does not manufacture
business facts for assignments, artifacts, reviews or work items. Acceptance: L2–L3.

**B-R8 — accountable verification, without an assessor subsystem.** A dependency request
names `verificationRef={kind:"assignment",id:"V"}`. V must already exist, be open and
owner-scoped, with a recorded holder admitted by the verification TOML. Record the holder,
`selectedPolicyName` from G-D's deterministic selection, and `verificationState=provisional`
on the wake in the registration transaction. That policy name records the admission
cause and remains unchanged by later policy reloads. The registrant
supplies the obligation; the engine does not staff or create a verifier. Registration's
notice summons that holder once if the dependency remains unresolved after immediate
evaluation, with wake id, exact predicate, necessity and requested judgment, through
ordinary Wakes. Already-recognized truth does not summon a verifier for an ended wait.
The existing assignment lifecycle supervises V.

The same fallback dueAt bounds provisional waiting; no second verification timer or
cadence default is added. Policy must name an actual verification transition and cannot
select `never`. Extend verdict attests with nullable `waitId REFERENCES wakes(wakeId)`
and optional `--wait <wakeId>` at the existing attest seam. For this contract,
`wait-verified` and `wait-challenged` require that binding and a holder-filed verdict on
V. The exact wake id pins the immutable predicate, resolver, version expectations,
necessity and continuation; a verdict on another wait cannot qualify it.

A `wait-verified` verdict changes provisional→confirmed and records its attest id.
A `wait-challenged` verdict changes provisional/confirmed→challenged and recognizes
reconsideration with reason `verification-challenged`. Ending V without a bound confirming
verdict likewise recognizes reconsideration with reason `verification-terminal`; the
engine does not invent a failed-necessity judgment. Those paths end coverage and effort
relief immediately, retain the actual evidence, and deliver after T through the shared
notification path. The challenged wake's resulting notification does not regain coverage
merely by being queued/running. The agent can reconsider and register a new justified
next transition. No resolver assignment is closed by this operation.

Resolver-terminal reconsideration stays armed even while verification is pending or
confirmed. At any success/fallback/resolver-terminal firing, relief ends and provisional
coverage ends or transfers to ordinary ready-now continuation coverage. Resolution does
not change the recorded verification state to confirmed. No class bypasses verification
indefinitely; silence reaches dueAt and existing verifier-assignment supervision remains
active. These facts establish accountability, not semantic proof that inference is right.
Acceptance: V1–V4. The added state uses existing wake/attest rows and mutation seams.

### G-C: coverage and effort

**C-R1 — scoped coverage.** Replace session-wide queued/running coverage at
`supervision.ex:3132` and holder-oldest selection at `:1313` with per-obligation
evaluation. A queued/running continuation joins through `turns.wakeId` to the admitted
wake's matching `assignmentId` and `obligationRef`. A prose assignment mention does not
join. Pending coverage requires T terminal (or no originating turn) and a coherent
admitted sidecar. Evaluate
coverage and prod claim in one transaction so a competing continuation cannot be ignored
between the check and action. Watermarks follow the same obligation scope. C1–C4 verify it.

**C-R2 — sidecar.** Extend `controllerOrigin` with `holder_continuation`, and add exactly
that coherent branch to `schema.ex:288` and its insert trigger at `:684`. This branch
requires a prompt wake, matching open assignment, authenticated authorized registrant,
captured turn (or explicit null for registration outside a turn) and matching obligationRef.
It carries neither a charged prod generation
nor a fabricated `wakeKind=prod`. Existing scheduled and retirement branches retain
their checks. The sidecar's pending→settled transition follows delivery/cancellation;
the ledger join supplies coverage after enqueue. Acceptance: C1–C4, C8.

**C-R3 — separate effort policy.** Mechanical qualification requires an open accountable
resolver, durable predicate/row identities/version expectations/necessity/resume action,
successful immediate evaluation, and an accountable verifier under B-R8. The shipped
policy admits other-party dependencies; self-block relief requires an explicit rail
election over `resolver.owed_by_other=false`, not a compiled prohibition. Provisional
and confirmed waits can receive relief, labeled distinctly. Relief starts at registration
and ends at any firing or cancellation, including verification challenge. This timing
does not advance after-turn prod-coverage eligibility. Ready-now pending/queued/running
continuations use normal effort. Scheduling does not reset a generation, extend the
unused budget repeatedly, or count as progress. Acceptance: C5–C7, V1–V4.

Pause the existing effort horizon for the actual qualifying interval and preserve the
remaining budget. When qualification ends, resume from that remainder, not a fresh
horizon. Qualification transitions and accounting updates must be atomic and durable;
restart cannot lose a pause or grant it twice. Overlapping qualifying waits for one
assignment exclude the union of their intervals, not their sum. The policy determines
qualification; the engine measures the interval. Do not change configured horizon,
multiplier, progress receipts, or effect-channel cursors. Acceptance: C6–C7.
`EffortCheckin` owns those accounting mutations in its existing generation rows; use
additive interval fields there, not a new accounting table or service.

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
  { fact = "wait.coverage_valid", op = "eq", value = true },
  { fact = "wait.continuation_state", op = "in", value = ["pending", "queued", "running"] },
]

[[policy]]
name = "justified-unresolved-dependency"
purpose = "wait-effort-relief"
when = [
  { fact = "wait.obligation_matches", op = "eq", value = true },
  { fact = "wait.admitted", op = "eq", value = true },
  { fact = "wait.continuation_state", op = "eq", value = "pending" },
  { fact = "wait.recognized", op = "eq", value = false },
  { fact = "resolver.open", op = "eq", value = true },
  { fact = "resolver.owed_by_other", op = "eq", value = true },
  { fact = "wait.declaration_complete", op = "eq", value = true },
  { fact = "wait.verification_accountable", op = "eq", value = true },
  { fact = "wait.verification_state", op = "in", value = ["provisional", "confirmed"] },
]

[[policy]]
name = "accountable-dependency-verifier"
purpose = "wait-verification-admission"
when = [
  { fact = "verifier.open", op = "eq", value = true },
  { fact = "verifier.holder_is_other", op = "eq", value = true },
]
verification = { trigger = "registration", terminal = "bound-verdict-or-obligation-terminal", fallback = "wake-due-at" }
```

`policy` is an additional array-of-tables root in the existing rule files. Each table
requires `name`, `purpose`, and nonempty `when`. Names use the existing rule-name
syntax and are unique across the loaded rule/policy set. Purpose is exactly
`wait-prod-coverage`, `wait-effort-relief` or `wait-verification-admission`.
Verification-admission declarations additionally require the `verification` inline table
shown above with exactly those three keys and literal values. Other purposes reject that
table. This MVP summons the named verifier at registration and uses the existing fallback;
`never` or an omitted verification transition fails policy loading. No `effect`, remedy
or check script is valid
inside a policy. Unknown keys/facts, unsupported purpose, empty conditions, duplicate
names and type errors fail loading with file/policy/condition location. Conditions AND-fold;
multiple declarations for one purpose qualify if any one matches. No matching declaration
means no qualification. Candidate selection never substitutes for condition evaluation.

For each purpose and one evaluation snapshot, select the matching declaration whose
unique validated name is smallest in ascending bytewise order. Loader order, file order,
and declaration order do not break ties or affect selection. An empty matching set has
no selected policy and does not qualify. B-R8 persists the selected
`wait-verification-admission` name as `selectedPolicyName`; other purposes use the same
selection when reporting a policy cause. Overlap still grants qualification once and
does not multiply notices, coverage or effort relief. This uses existing unique names;
it introduces no priority field, extra registry, or overlap refusal. Acceptance: V1.

Each policy query binds one candidate wake, one obligation and one owner, with a fresh
fact cache. `wait.continuation_state` is pending for an uncanceled, undelivered wake;
queued/running for its ledger continuation; terminal otherwise. `wait.admitted` refers
to successful admission and coherent durable provenance, not to prompt wording.
`resolver.open` is false for terminal or absent resolvers. `resolver.owed_by_other`
compares the derived resolver principal to the covered assignment holder. An owner user
is a distinct accountable party from that user's agent. `wait.declaration_complete` means
the required stored fields passed registration validation; it never judges their prose.
`wait.verification_accountable` reads B-R8's admitted verifier and its recorded transitions.
`verifier.open` reads V's assignment state; `verifier.holder_is_other` compares V's
recorded holder to the covered assignment's holder, not to a caller-supplied name.
`wait.coverage_valid` is false after challenge or unverifiable terminal verification;
otherwise it is true for a coherent pending wake or its queued/running continuation.
Policy qualifiers expose truth, not a new effect channel or confirmation of advancement.

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
It rechecks admission conditions inside registration to prevent a stale preliminary
dispatch read from granting coverage, without executing notice/remedy effects twice.
Who qualifies is TOML policy; tenant isolation, valid references,
mandatory fallback, coherent sidecar and typed transitions remain substrate constraints.
The shipped policy must implement the accepted matrix, not merely provide a configuration
example. Tests replace policy in an isolated org to prove qualification follows TOML.
See D1–D2 and V1–V4. No new default verifier selection exists: the registrant names the
existing obligation, and the shipped TOML checks its holder is another party. Verification
admission is mandatory for dependency registrations regardless of coverage/effort elections.

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
> Include declared necessity and the existing verification assignment in the predicate
> object. Coverage is provisional until its holder verifies necessity. A challenge ends
> that coverage and summons reconsideration.
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

The later Gap-2 fidelity ruling makes admitted but unverified dependency coverage
explicitly provisional. Its policy-qualified effort relief starts at registration;
usable prod coverage still waits for T terminal. A verification challenge ends both.
Neither the matrix's word "justified" nor resolver disposition is a machine proof of
necessity. V1–V4 check this distinction.

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
| B4 (I3) | Given R exists but its future output does not, when a producer-bound output predicate registers, then it remains pending. When a different assignment by the same holder on the same work item records an artifact, then no match occurs. R's exact output linked by producedByAssignmentId can satisfy it. Repeat without a known hash: artifact and review must still match the same recorded id/hash. |
| B5 (I4) | Given output H1 exists and the clean-review conjunct is false, when R terminates without the clean review, then the resolver-terminal path recognizes at that commit, before dueAt, regardless of the false conjunct. |
| B6 (I4,I7) | Given success false and R closes as surrendered/revoked or its decision is withdrawn/superseded, when that transition commits, then one resolver-terminal notification becomes eligible after T, without advancing the clock to fallback. |
| B7 (I4,I10) | Given default terminal predicates, when a work item becomes iceboxed or failed, an assignment surrendered, or a decision withdrawn, then success includes the actual disposition. A narrow work-item `closed` predicate does not call iceboxed success; if R then terminates it uses path 2. |
| B8 (I4,I10) | Given producer P has an older clean review of H1 and the wait expects H2, when evaluating, then H1 cannot satisfy H2. Given an applicable later changes-requested conclusion for H2, then the earlier clean H2 conclusion cannot win. Terminal revocation/closure of R still triggers reconsideration. A verdict lacking artifactId/contentSha256 cannot satisfy the exact-revision wait. |
| B9 (I5) | Given recognition occurs during T and the observed row changes again before T ends, when the gateway restarts and T becomes terminal, then one notification carries the recorded recognition and prompts a reread. No notification is enqueued while T is running. |
| B10 (I6) | Given success, resolver termination and fallback race, when their transactions serialize, then one recognition wins and `turns.wakeId` yields one continuation. Given cancellation commits first, then no later recognition or enqueue occurs. |
| B11 (I7) | Given R stays open, no success occurs and dueAt passes, when the tick evaluates, then one fallback is recognized, stamped silence rather than success, and delivery still respects T. The fallback does not automatically rearm the wait. |
| B12 (I6) | Given a crash after recognition or enqueue but before marking delivery, when the gateway restarts, then pending delivery reuses wakeId and does not duplicate the continuation. Existing target refusal/retry behavior and typed cancellation remain observable. |
| C1 (I5,I8) | Given A's wait registers during T, when supervision evaluates before T terminal, then the new wait grants no after-turn coverage yet. In the transaction observing T terminal, a valid pending or enqueued continuation suppresses a duplicate prod for A. |
| C2 (I8) | Given S holds A and B and has a valid pending dependency wake for A, when supervision evaluates both, then A is covered and B remains independently eligible. Repeat with a ready-now pending wake, and with A's queued/running continuation; the result is unchanged. |
| C3 (I8) | Given the executive specimen shape (`w_9639742e`, `w_181be052`: prose named work but assignmentId was null), when fixtures register the equivalent new wakes with typed A/B scope, then prods corresponding to 118974/118975/118976 are suppressed only for the covered obligations. Legacy null/prose-only wakes earn no new coverage. |
| C4 (I8) | Given A's continuation is queued, then running, when successive supervision evaluations occur, then no duplicate prod is issued. When it completes with A open and no next wake, then prod eligibility resumes at the next evaluation. |
| C5 (I8) | Given two otherwise equivalent covering wakes, one policy-qualified unresolved dependency and one ready-now continuation, when effort is accounted, then only the first receives relief. Self-owed R does not qualify under the shipped other-party policy; an isolated explicit self-block rail election can qualify it, with accountable verification still required. |
| C6 (I9) | Given an effort generation with used budget U and unchanged effect cursors, when a wait registers, is replaced, or is recognized, then U and cursors do not reset and no effect is credited. A qualifying interval pauses only the remaining horizon; ending it resumes the same remainder. |
| C7 (I8,I9) | Given overlapping qualifying intervals and a gateway restart, when relief is reconciled, then their union is excluded once and used effort survives. When success, terminal reconsideration, cancellation or fallback occurs, then relief ends even while the continuation stays covered. |
| C8 (I9) | Given a covered continuation dies on model capacity, failed or failed_unknown, when its terminal row commits, then its coverage ends, A remains open, no effect/refusal/progress credit is created, and existing recovery handles the failure. An independently valid open dependency covers only on its own merits. |
| D1 (I1,I8) | Given valid qualification TOML, when its condition changes in an isolated fixture and policy reloads, then coverage/effort qualification follows that policy without a binary change. Neither policy change can permit a cross-tenant read or waive a missing fallback. |
| D2 (I3,I8) | Given holder, ancestor and unrelated same-owner registrants, when each registers an obligation wake, then the shipped admission rule admits the first two and refuses the third. A complete declaration is mechanically eligible but remains provisional; it does not establish necessity or renew evidence budget. A bound verifier challenge ends its relief and coverage. |
| D3 (I10) | Given compiled CLI help/parser and the amended manual example, when the example runs in an isolated remote org, then it registers the documented rows and delivers a notification with the prompt intact. Staged doorbell remains unarmed; no cadence configuration changes. |
| L1 (I1) | Given a legacy kind/scope wake with cursor N, when fact N already exists, then it does not fire. When same-owner matching fact N+1 is recorded, then Rules recognizes it. Omitted scope retains wildcard semantics. A code inspection finds no independent authoritative matcher in Wakes. |
| L2 (I2) | Given identical kind/scope in two tenants, when a fact arrives for B, then A's wake remains pending. Given an old system fact with ambiguous owner provenance, migration reports/refuses that ambiguity and never silently grants A visibility. |
| L3 (I1,I6) | Given an upgrade fixture with pending legacy condition wakes, ordinary timed wakes, canceled/fired wakes and delivery retries, when migrated and restarted, then pending work retains cursor/fallback/identity, closed history is unchanged, and deliveries use the retained shared path. |
| V1 (I11) | Given valid unresolved R and open named verifier V, when registration succeeds, then the wake durably records necessity, exact predicate/bindings, V/holder, selectedPolicyName, provisional status and bounded verification transitions. Given both `a-verifier` and `z-verifier` match verification admission, register with their file/declaration orders reversed in a second fixture: each wake records `a-verifier` and summons V's holder once. A later reload does not rewrite either stored admission name. With neither policy matching, registration refuses without a wake. Relief starts at registration under policy; coverage waits for T terminal. Missing V refuses dependency registration. |
| V2 (I4,I11) | Given provisional W, when V's holder files wait-verified bound to W, then W becomes confirmed without resetting effort. When that holder files wait-challenged, then coverage/relief end and W recognizes reconsideration with the challenge attest id, even if the success conjunction is false. The queued challenge notification does not restore coverage. |
| V3 (I11) | Given W and another wait X, when a verdict is bound to X or filed by someone other than V's holder, then it does not confirm W. Given V closes without confirmation or remains silent through W's dueAt, then W leaves provisional waiting through reconsideration or fallback, never an invented confirmation. Existing supervision still owns V's unfinished obligation. |
| V4 (I11) | Given a TOML class omits verification or selects never, when loading/registering, then it cannot admit a permanently unverified dependency. Given R resolves while W is provisional, then W fires and relief ends, but the record does not claim verified necessity. |
| V5 (I3) | Given legacy unbound artifact/verdict rows, when the additive schema ships, then their new fields remain null and original completion-rail results stay unchanged. New wait predicates reject unbound review evidence. Partial artifact/hash pairs and mismatched/cross-owner producer links refuse at their existing write seams. |

Traceability: G-A implements A-R1–A-R4 (A1–A4, V5); G-B implements B-R1–B-R8
(B1–B12, L1–L3, V1–V3); G-C implements C-R1–C-R4 (C1–C8, V1–V2); G-D implements
policy and the operating amendment (D1–D3, V4). Cross-cutting invariants are cited by each case.
Build order is G-A → G-B → G-C → G-D through the same implementation seam.

Review handoff requires this canonical file in tightbeam-specs main, exact SHA-256 artifact
row, and a completed cold digest. Build handoff additionally requires independent spec
review to pass. The orchestrator returns
the review verdict to the spec expert. After a clean review, bind the work item's
implementation specRef/hash to those reviewed bytes. Implementation then returns remote
gate evidence and fresh independent code review to the orchestrator; final Spirit
acceptance precedes integration and does not itself lift the protected-ref landing hold.

## Open Questions

No blocking questions remain. Resolved rulings are retained so later readers do not
re-decide them:

- **Q1 — RESOLVED:** opener message `s_92a833e5-5a85-495b-b743-ca42318fa6ea`
  authorizes A-R4's additive nullable producer and revision links, with no backfill or
  completion-rail changes. The source gap was recorded in `att_e4e85a8f`.
  Deleting exact revision binding loses a required acceptance case; accepting approximate
  holder/work-item provenance permits stale or unrelated output. Those alternatives lost.
- **Q2 — RESOLVED:** the same initial ruling, superseded on necessity by messages
  `s_33d4038f-c57a-441f-a075-70534eada151` and `s_936bcb33-ffeb-4e53-a907-bda184a5c2c6`
  under `att_ac0d162e`, supplies B-R8 and C-R3. Mechanical admission precedes semantic
  confirmation; accountable verification is mandatory and provisional status explicit.
  The existing obligation/attest/wake seams suffice. A new assessor subsystem was declined;
  permanently unverified classes and treating resolver disposition as proof were rejected.
- **Review B1 — RESOLVED:** verdict `att_621e21e8` / report `art_2c42d897` exposed
  unspecified selected-policy provenance under overlapping matches. G-D now selects the
  bytewise-smallest matching name per purpose/snapshot; B-R8 persists that admission cause
  and V1 proves order independence. Deleting provenance loses required accountability;
  accepting unspecified iteration order loses reproducibility. Existing unique names
  supply the ordering without adding a priority mechanism or rejecting valid overlap.
- **Q3 — NON-BLOCKING: legacy deprecation horizon.** Follow design §8: indefinite syntax
  compatibility until separately ruled. No forced migration deadline.
- **Q4 — NON-BLOCKING: additional row domains.** The required domains above implement the
  accepted examples. New observable domain facts can extend the existing fact seam;
  observation producers and their semantics require their own authority.
