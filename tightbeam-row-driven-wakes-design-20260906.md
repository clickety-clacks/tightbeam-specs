# Row-driven wakes: unified production-engine design (0.1.9)

Revision 3 (canonical). Revises revision 2 (art_c7772427, specs@0c18c21) in place per
spirit-changes-required att_49ee3ba2 (R1-R3; architecture direction accepted, no restart).
Revision 2 superseded the rejected slice art_ff24cdb7 per att_7785b8e6 (F1-F4 + hole
rulings) and parent executive ruling att_1bd0c4d1. Work item
wi_fbcdf1a9-d3fc-4f17-ae1a-eb38ebc9facd, assignment asg_d5b51707,
orchestrator:row-driven-wakes-019. Posture-heavy (filed).
Spirit: tightbeam-wait-spirit-20260906-mike.md
sha256 ba377391d80433b735aca88ae5a104d9add82de86f8bc5e6c93f18fe62753964.
Evidence: four read-only static inspections of branch 0.1.9 tip f303dce plus parent report
row-wake-reuse-findings.md (sha256 56fd46a1…). Line cites are that tip. No code executed on
gibson. Implementation and spec-writer dispatch remain HELD until this design passes spirit;
protected-ref landing hold (main + 0.1.9) remains until the verified Toplines concern-tags
pair merge.

## 1. Architecture: one engine, no second matcher (F1)

A conditional wake IS an ad hoc production rule. This design makes that literal: **agent-
registered waits and data-defined rules evaluate through the same recognition/evaluation
path** — the existing `Tightbeam.Rules` engine — now, not as deferred convergence.

**The common engine grows three things (all in rules.ex core):**

1. **A `row-commit` edge** beside `verb` and `turn-end` (validate_edges!/3 rules.ex:421-431).
   Wired post-commit via DB.transaction_then/3 (db.ex:67-71) at the terminal write
   chokepoints of each row domain — assignments.ex:1227/:1321, work_items.ex:418/:429,
   artifacts.ex:95, escalation.ex:1131-1198 — following the precedented recognition-hook
   pattern (ConditionFacts.file/3 condition_facts.ex:76-85, CatalogRederive.recognize/3
   catalog_rederive.ex:45-61). The edge evaluates (a) loaded rules bearing it and (b) pending
   ad hoc waits whose fact domains intersect the committed rows. The existing tick remains
   the sweep fallback. No new processes.
2. **A non-blocking `notice` effect** in validate_effect!/4 (rules.ex:433-441): record +
   summon + allow. This is the primitive the staged-unarmed review-rounds-doorbell already
   names (engineering.toml:126-143). An ad hoc wait's RHS is a notice that fires its wake
   through the existing Wakes delivery. Arming the doorbell itself stays out of scope.
3. **New row facts in the whitelist** (@facts rules.ex:114-144, compute_fact/4 :1083-1526):
   work-item state/disposition, assignment state+outcome, decision-request disposition,
   artifact identity (id + contentSha256), qualifying-review binding. Facts remain
   substrate-implemented SQL over ownerUserId-scoped business rows; the vocabulary is the
   extension seam and is not closed (hole ruling: named predicates are examples, never a
   restriction on ad hoc predicates).

**An ad hoc wait is a durable row**: a condition list in the existing rule grammar
(@operators :145, validate_condition!/5 :654 — composition via the list AND-fold and
in/not_in) validated at registration against the fact whitelist, plus scope bindings, a
resolver reference (§2), a continuation prompt, and a mandatory fallback dueAt. Waits are
instances evaluated by the engine; rules are law loaded from TOML; one evaluator serves both.

**Wakes keeps what is proven**: durable rows, deliver-then-mark delivery (wakes.ex:2538),
restart durability (turns.wakeId UNIQUE ledger.ex:44), typed cancellation (:962-986), retry
ladder, fallback-dueAt enforcement (gateway.ex:666-673). **The independent (kind,scope)
matcher — candidate_sql/1 wakes.ex:2823-2885 and the parallel authoritative re-match in
fire_in_txn/2 :2926-3015 — is retired as a separate engine.** Legacy `--when-fact` syntax
remains supported as compatibility only: a (kind,scope) wake is internally represented as an
ad hoc wait whose single condition is condition-fact-match(kind, scope), evaluated by the
unified path (hole ruling: compatibility through the unified engine, not a second matcher).
condition_facts rows remain for genuinely event-shaped observations (escalation-ruled stays;
its atomic transaction escalation.ex:1162-1198 is the transition model all chokepoints copy).

**Boundedness (F1's contingency):** the unification is bounded and is therefore built, not
deferred and not raised as a scope request (parent ruling forbids deferral requests). Surface:
rules.ex (+1 edge, +1 effect, +~6 facts, evaluator entry for wait instances), wakes.ex
(registration/storage/compat routing; matcher retirement), 4-5 chokepoint hook calls,
supervision gate rework (§4), schema (wait columns + sidecar origin). No blocker taxonomy, no
assessor-budget subsystem, no data-defined query language beyond the existing grammar, no new
GenServers, no rewrite of closed history.

## 2. Accountable resolver: obligation, not output (F2, R1)

A satisfying-state stamp is reporting, not accountability. The awaited **output** commonly
does not exist yet at registration — an artifact id cannot be named before the artifact is
produced. So a wait separates two things it previously conflated:

- `resolverRef` — the **existing obligation that owes the action**: a decision_request id
  or an assignment id with an accountable holder/addressee. This row must exist and be
  non-terminal at registration (else immediate evaluation §3 fires now). A work item id or
  an artifact pointer is NOT a valid resolverRef on its own: a work-item owner or a pointer
  to bytes proves no one currently owes an action. A wait over work-item disposition still
  names, as resolver, the open assignment (or decision request) through which that
  disposition is owed.
- **Expected output identity** lives in the predicate, not the resolverRef: the success
  conditions (§3) describe the awaited output — the artifact this assignment produces, a
  known contentSha256 when the revision is already fixed, a work-item disposition, a review
  verdict. The predicate may reference rows that do not exist yet; the resolver obligation
  must exist now.
- The responsible party is derived from the resolver row, not asserted: a decision
  request's addressee, an assignment's holder. The wait links the request/work that must
  move — wisdom 14, no intent in limbo: absence is detectable because the wait points at
  the exact obligation whose silence is the problem.
- **Revision binding for reviews**: a review-verdict condition binds to the exact output
  revision under review (the linked review card's verdict over the artifact revision's
  contentSha256), never merely "the producer assignment has a clean review" — a producer
  assignment is reused across revisions and a stale round must not satisfy a wait on the
  current one (qualifying_review_verdict_kinds assignments.ex:373-405 is already
  latest-round-authoritative; the wait predicate carries the revision identity alongside).
- `continuation` — the explicit actionable next step, authored at registration, delivered as
  the wake prompt. "Re-read rows" alone is not a continuation; the prompt states what the
  agent will do with the resolved state.
- Firing stamps which path fired (§3) + predicate + resolverRef + the satisfying transition
  (row, field, old→new) into the delivered prompt, extending the existing "[woke: …]"
  stamping.
- Truthful observation remains the producer's duty: the resolver's own row transition is the
  observation. Nothing manufactures facts on the waiter's behalf.

Reconsideration, not permission (carried from wi_fca19e0c): the fired wake is a notification
turn. The agent re-reads the rows and decides; a firing never authorizes an action, and the
continuation prompt is an instruction to reconsider with named context, not a grant.

## 3. Terminal-complete predicates and exact binding (F3, R2)

Every wait has **two independent firing paths**, and both are always armed:

1. **Success predicate** — the registrant's composed conditions (AND-fold over the fact
   grammar) describing the awaited outcome.
2. **Resolver-terminal reconsideration** — implicit, engine-supplied, never composed away:
   the wait ALSO fires when the resolverRef obligation reaches any terminal state without
   the success predicate holding — assignment surrendered/revoked/failed, decision request
   withdrawn/superseded, review verdict revoked out from under a partially-satisfied
   conjunction. An AND like "artifact hash present AND clean review" can otherwise stay
   false forever once the reviewer revokes or the producer fails; the waiter must be woken
   for reconsideration at that known terminal moment, not stranded. The stamp names which
   path fired and the terminal disposition.

`dueAt` is the fallback for **silence only** — a resolver that neither succeeds nor
terminates. It is never the sole detection of a known terminal failure: a terminal
resolver transition fires path 2 at its own commit (row-commit edge, §1), not at dueAt.

Success predicates over the named domains resolve on **terminal disposition, never
success-only**:

- Decision predicate: satisfied when decision_requests.status leaves `open` —
  ruled | withdrawn | superseded (the DDL already carries the enum, escalation.ex:53-135;
  ruled additionally guarantees decision+ruledBy+ruledAt :112-115). The delivered stamp names
  which disposition; withdrawal and supersession are reconsideration triggers, not silent
  non-events.
- Assignment predicate: state='closed' with outcome delivered —
  completed | surrendered | revoked. A surrender wakes the waiter exactly as a completion
  does; what differs is the continuation the agent chooses.
- Work-item predicate: state IN (closed, failed, iceboxed) with disposition delivered.
  **Iceboxed never silently reads as completed**: the stamp carries the actual state, and the
  registrant may compose a narrower wait (e.g. state in [closed]) — but the default terminal
  wait covers all three so no disposition strands a waiter.
- Exact revision binding: artifact conditions bind artifact identity and contentSha256, not
  kind-level existence; review conditions bind the qualifying holder-filed verdict to the
  exact output revision per §2 (never a producer assignment reused across revisions, never
  "some clean review exists").
- Composition uses the rule grammar as-is: multiple conditions AND-fold; in/not_in bounds
  disposition sets. Registration-time validation refuses conditions over unknown facts.
  Composition narrows the success predicate only; it never disarms path 2.
- Immediate registration evaluation: both paths are evaluated inside the scheduling
  transaction; an already-satisfied predicate or already-terminal resolver is **recognized**
  now rather than parking a wait on a past event. Delivery of that recognition follows §4's
  after-turn eligibility (recognition at registration, delivery at the originating turn's
  end — no mid-turn interruption, no lost firing).

Quota/credential/capability predicates require net-new observation rows (no quota table;
credentials.ex is filesystem-only) — observations remain producer responsibilities per the
spirit; the fact seam admits them later without engine change.

## 4. Obligation-specific coverage and after-turn eligibility (F4, R3)

The suppression gate (gate_reason_in_txn supervision.ex:3132) is rebuilt per-obligation:

- **Unrelated coverage is removed.** A queued/running turn suppresses prodding ONLY when that
  turn is linked to the same obligation (turns.wakeId → wake.assignmentId + obligationRef).
  The present session-wide pending_turn read (:3137-3142) stops covering unrelated
  obligations. Likewise pending_wake (:3145-3153) credits only a wait whose obligationRef
  matches. prod_production_matches?/3 (:1313) and oldest_supervised_assignment/2 (:1339)
  move from per-holder-oldest to per-obligation; watermarks (:1930-1945) follow.
- **Agent-armed coverage becomes representable.** Sidecar controllerOrigin gains
  `holder_continuation` (CHECK schema.ex:288-330; insert-coherence trigger :684-712 relaxed
  for exactly that origin); wake rows gain obligationRef; agent-created waits may carry
  assignmentId (admission-checked, §5). This closes the null-assignment gap in executive
  specimen att_3f02d597: w_9639742e and w_181be052 named obligations in prose while their
  rows said assignmentId NULL, and prods 118974/118975/118976 fired anyway. That specimen is
  a named acceptance scenario: a holder with a pending wait whose obligationRef matches the
  obligation is not prodded for it.
- **After-turn eligibility, specified**: a wake armed during turn T becomes eligible for
  delivery and for coverage evaluation when T reaches a terminal turn state. Recognition
  and delivery are distinct moments (§3): satisfaction may be recognized at registration or
  at any row commit, while delivery waits for the originating turn's end. A covering wake
  delivered into a queued/running continuation turn for the same obligation continues to
  cover until that turn completes (no duplicate prod — spirit turn-end rule l.127-131). If
  the turn completes without discharging the obligation and no new coverage exists,
  eligibility to prod resumes at the next evaluation.
- **Dependency covers; a ready-now continuation does not.** A pending wait is covered state
  ONLY while it is a justified unresolved dependency: the resolverRef obligation (§2) is
  open, non-terminal, and owed by another accountable party. A wait whose success predicate
  or resolver-terminal path is already recognized, or whose continuation is actionable now
  without the dependency, is an actionable continuation — it burns effort normally and
  suppresses nothing. Naming a resolver does not by itself buy coverage; scheduling never
  renews the evidence budget. Which waits qualify as covered state is admission/effort RAIL
  POLICY (rule TOML at the existing edges, §5), not engine behavior: the engine supplies
  the facts (resolver open? owed by whom? recognized?), the rails decide the suppression.
- **Effort-check treatment**: effort_checkin (separate 4h-horizon budget, effect channels
  counted at effort_checkin.ex:1229) treats a qualifying dependency wait (previous bullet)
  as covered state — no effort burn and no prod for the covered obligation while the
  dependency is live. Scheduling a wait remains coverage, never evidence of advancement:
  receipt absorption (:2708-2716) and ladder resets (supervision.ex:1303 — progress prose
  never resets) are NOT widened, and verification of advancement stays with the existing
  rail policy.
- **A failed continuation ends its coverage.** When a continuation turn fails — including
  death on model capacity (specimen 118975) — its queued/running coverage ends at that
  failure and the existing retry/failure accountability applies to the turn. Capacity
  failure is neither refusal nor progress nor permanent coverage: it discharges nothing,
  credits no effect channel, and answers no prod; the obligation returns to evaluation
  exactly as it was. The pending dependency wait itself continues to cover only if its
  resolver obligation genuinely remains open.

## 5. Admission policy in rails; tenant safety in substrate

Who may register a wait over which rows is POLICY at the existing wake-verb chokepoint
(Rules.decide, dispatch.ex:107-168), expressed as rule TOML — registrant holds or sits in
lineage above the scoped obligation (promoting the hardcoded work_block_authority? test,
gateway.ex:3863-3877, to a fact per the commission). The engine enforces only physics:
predicate SQL is written against ownerUserId-scoped rows (closing the hazard that
condition_facts carries no tenant column and the legacy matcher joined kind/scope alone);
the scoped row must exist; the fallback dueAt is mandatory; cancellation/supersession reuse
the typed state machine.

## 6. Implementation goals (dispatch HELD until spirit pass)

- **G-A — engine unification** (rules.ex): row-commit edge, notice effect, new row facts,
  evaluator entry for wait instances. The load-bearing goal; everything else consumes it.
- **G-B — waits in Wakes** (wakes.ex, schema, chokepoints): registration + immediate eval +
  storage (resolverRef, obligationRef, continuation), the implicit resolver-terminal
  reconsideration path (§3 path 2), legacy (kind,scope) compatibility routed through the
  unified evaluator, matcher retirement, two-path firing stamps.
- **G-C — supervision coverage** (supervision.ex, effort_checkin.ex, sidecar schema):
  per-obligation gate, holder_continuation origin, after-turn eligibility,
  dependency-vs-actionable covered-state facts, effort-check coupling, failed-continuation
  and capacity accountability, specimen regression tests.
- **G-D — admission + coverage TOML, guidance**: wake-verb admission rules and the
  covered-state suppression policy (§4) as rule TOML; operating-manual "Match the wake to
  what you wait on" gains the predicate instrument; migration note (compatibility, no
  forced migration).

Sequential G-A → G-B → G-C (one seam, one coder path); G-D follows. Remote regressions per
goal on eezo/racter via scripts/verify_mix.sh unmodified, host named in each attest; fresh
independent review per preferred-models; spirit summary before any integration; integration
additionally held under the standing landing hold.

**Removed from the plan (hole rulings):** the former G1 interval-default fix. The
supervision-interval default (today wake_tick_ms=1000ms via config/runtime.exs:32 →
application.ex:258 → gateway.ex:1004/:1014/:4227, ladder clobber :1858) belongs to
wi_c737aee7's owner s_0cd749fc; no default is invented here and no duplicate producer is
staffed. Likewise prod-prompt wording (wi_c60c0189, supervision.ex:4415) is s_0cd749fc's;
G-C makes the advertised remedy real and this orchestrator coordinates the wording and both
cards' dispositions with that owner before any fold or close.

## 7. Card reconciliation

- wi_2ef3d514 (iceboxed): superseded by this design; dueAt-fallback requirement survives.
  Stays iceboxed, annotated.
- wi_fca19e0c (closed): reconsideration-not-permission carried as §2 requirement. No reopen.
- wi_c60c0189 (open, wording, owner s_0cd749fc): G-C supplies the mechanism that makes the
  prompt true; wording and disposition coordinated with the owner, not folded unilaterally.
- wi_c737aee7 (open, cadence, owner s_0cd749fc): interval default remains that card's;
  this design only documents the dependency.

## 8. Remaining marked holes

1. Coexistence horizon for legacy (kind,scope) syntax: compatibility indefinitely, or a
   deprecation milestone once ad hoc waits prove out. Non-blocking; default is indefinite
   compatibility.
2. Initial row-fact list for G-A beyond the F3 set (decision/assignment/work-item/artifact/
   review): extension is open by design; the named five domains are examples, not a bound.
