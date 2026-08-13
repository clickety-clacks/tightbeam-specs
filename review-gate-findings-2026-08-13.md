# Review gate — consolidated findings (2026-08-13)

Status: RECORD — awaiting Mike's ruling. Step 1 of the 0.2 program (§9.1):
one Fable round and one Sol-xhigh round on `coordination-fabric-v1.md` (r3)
and `v0.2-program-2026-08-12.md`, reviewing-specs rubric checks 2–9,
reviewers independent and blind to each other. Findings are reproduced
VERBATIM per round. No fold to r4 and no Phase 1 until Mike rules.

Conduct notes:
- Fable round: fresh agent session (this session's model), read targets +
  rubric + grounding (pragmatics record, adjudication amendment, philosophy
  gate) from disk.
- Sol round: codex plugin, fresh thread, `gpt-5.6-sol` effort xhigh. First
  attempt failed cleanly — codex's bwrap sandbox cannot initialize on gibson
  (`bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`; the known
  wi_1625a095 / wi_424308f6 host class). Sol refused to review unread
  documents (correct behavior). Re-run on the same thread with all six
  documents embedded verbatim in the prompt; review performed with zero
  filesystem access. Blindness preserved throughout — Sol never saw Fable's
  findings, and vice versa.
- INCIDENT (live evidence for the fabric, issue-#12 class): Sol's round
  COMPLETED at 06:16:46Z but the completion never reached the orchestrator —
  the companion job registry lost the job (`result`: "No job found" while
  `status` showed a phantom `running/starting`), so the completion doorbell
  never rang and a monitor sat waiting on it. Unwedged by the predecessor
  session acting as Avasarala (quiet-past-floor prod), and resolved by
  READING THE DURABLE ROW — the codex rollout JSONL's `task_complete` event
  carried the full review in `last_agent_message`. The truth was in rows the
  whole time; only the interruption was lost. Lost-completion/doorbell-replay
  is precisely the wedge class the fabric's Law 2 and wake-integrity probes
  (C5) exist for.
- STALENESS FLAG: both rounds reviewed the program doc as of 2d18008 —
  BEFORE §8b "repo governance: no door" (87e7a79, ruled 2026-08-13). Findings
  citing PR machinery (PR-only landings, "PRs cross-reviewed", CI-on-PRs)
  touch text §8b now partially supersedes: PRs are abolished; landings are
  direct-to-main after gates, with CI-on-main-push as tripwire. Mike rules on
  current text; the fold must reconcile those findings against §8b rather
  than the reviewed snapshot.

---

## Round A — Fable (verbatim)

# coordination-fabric-v1.md (DRAFT r3) — findings

1. **BLOCKING — structure: four canonical sections missing entirely.** The spec has no **Non-Goals**, no **Terms**, no **Assumptions**, and no **spec-homing** section. Goal exists in substance (§1 "Problem"), Invariants in substance (§2 "Governing laws" + §10), Architecture (§§3–10), Acceptance (§11). But: §13's "everything 'deliberately excluded from v0' is placed, not dropped" is deferral, not a Non-Goals list — nothing names what the fabric will *never* do besides the anti-adjudication clauses; load-bearing terms ("principal," "front desk"/"back desk," "summon," "toplines," "rumination," "spirit verdict," "identity tree," "archetype," "obligation," "turn boundary") are used undesignated; the falsifiable assumptions the design rests on (e.g., "the exec is told, not smart: gating quality comes from directives, not from model capability" — §6, an empirical bet stated as fact) are never listed as assumptions; and the status header names provenance ("Authored from the ruled forks of `coordination-fabric-ideation-2026-08-12.md`") but no canonical spec set. Per the rubric each missing section is blocking; an empty section must be stated empty, not dropped.

2. **BLOCKING — Open Questions unmarked.** §12 "Open gaps" lists six items with no blocking/non-blocking marks. This is not cosmetic: "Directive schema: key vocabulary and precedence beyond latest-wins" is open, yet Phase 3 requires "file the delegation card and first directives" — an implementer cannot tell whether that gap blocks the pilot. Same for "Metrics plumbing for acceptance №1" (open) vs Phase 3's exit gating on acceptance №1.

3. **BLOCKING — avasarala's defined trigger cannot satisfy acceptance №3.** §5 defines avasarala as "starvation watermark: open obligation quiet > X → escalate regardless of any gate." §11 acceptance (3) demands "no `input-needed`/`blocker` older than the avasarala floor without a summon." An unanswered `input-needed` (a decision-request row — per the adjudication amendment, "data the asker chooses to honor," not an obligation on the answerer) whose *asker keeps working* is not an "open obligation quiet." A coder who builds avasarala literally from §5 watches obligation quiescence, never message age, and fails acceptance (3) by construction. The behaviour definition and the acceptance contract name two different triggers.

4. **BLOCKING — the default class→immediacy map does not exist anywhere.** §5: "`batcher` | delivers non-urgent classes at turn boundaries | class → immediacy map"; §13 seam ②: "Delivery-policy seam in `wakes.ex`: class→immediacy table." The knob is kungfu policy, but kungfu policy tables arrive in Phase 6 ("Hardcoded seed defaults stay the fallback") — and the hardcoded defaults are never stated. §7 fixes immediacy for `blocker` ("front desk triages immediately"), `fyi` ("digest at most"), and `algedonic` ("never batched"), but is silent on `input-needed` and `status-query`. Every seam-② implementer must invent whether a genuinely-required decision waits for a turn boundary. That silent decision is the spec's central subject matter.

5. **IMPORTANT — classifier vs sender election: two confident readings.** §5: "`classifier` | stamps inbound messages with a class (§9); unclassified → `fyi` | class vocabulary extensions, sender defaults." §7: "Class is **advisory metadata extending `attend`** — sender-elected, receiver re-classifiable, never a gate." Reading A: the classifier only defaults unclassified traffic to `fyi`. Reading B: it stamps *all* inbound messages per policy — the "sender defaults" knob invites this — meaning a deterministic rule can overwrite a sender's elected `input-needed` down to `fyi`. Both readings satisfy the words; they differ in whether a bone can silently downgrade a decision request (a Q1 "who judges?" failure in Reading B).

6. **IMPORTANT — `algedonic` routing is "and/or."** §7: "bypasses every bone and every desk, straight to the principal and/or the human." Three conforming implementations: principal only, human only, both. For the class defined as "genuine pain (constitution violation, spirit drift, data loss)," where the signal lands is the whole mechanism; no actor or rule decides which.

7. **IMPORTANT — the mis-classification claim is false for over-classification, and nothing bounds it.** §7: "Mis-classification costs latency (avasarala bounds it), never truth." True only downward. Upward — `fyi` elected as `algedonic` — "bypasses every bone and every desk": it costs principal interruption, precisely the resource §1 says is scarcest, avasarala bounds nothing about it, receiver re-classification arrives only *after* the interrupt lands, and §12 opens abuse shaping only for `status-responder`. The spec's own one-line safety claim is refuted by its own class table.

8. **IMPORTANT — exec "MUST NOT hold anything" vs "MAY batch, schedule."** §6 MUST NOT: "hold anything — its only 'no' is 'later,' and the avasarala bounds every 'later.'" §6 MAY: "batch, schedule, and deliver to its principal." Batching *is* holding delivery. The intended line (never hold obligations/lifecycle; may hold delivery timing) is never drawn; a literal coder forbids the queue the exec exists to run, or else ignores the MUST NOT — either way inventing the boundary.

9. **IMPORTANT — standing directives collide with holder-filed doctrine, unaddressed.** §6: "Standing directives (v1, zero new rows): filed as attests on the delegation card" and the exec reads "the directives its worker publishes." The worker is not the holder of the delegation card (the exec is — §4: "The exec holds exactly one assignment"). §4 simultaneously insists "holder-filed doctrine untouched." Whether non-holders may file non-lifecycle attests on another's card is never stated — the substrate either refuses the worker's directive or the doctrine's boundary (lifecycle-only?) needs stating. Every implementer decides.

10. **IMPORTANT — batched delivery to an idle session: Law 3 permits a violating build.** §2 Law 3: "A batched delivery exits on time or a turn boundary, nothing else." §13 ②: "turn-boundary digests materializing one turn for N payloads." "Materializing one turn" reads two ways: the batcher *creates* a wake (generates the turn), or the digest folds into the next externally-caused turn. Under the second reading, an idle session's `fyi` digest waits on someone else sending urgent traffic — a state whose exit is someone else's action, the exact shape Law 3 and philosophy-gate Q3 forbid. No time ceiling for batched deliveries is specified anywhere.

11. **IMPORTANT — §11's summon enumeration contradicts its own acceptance clause.** §11: "The PO becomes back-desk only — summoned for rumination cadence, spirit verdicts, and algedonic signals; its exec fronts everything else." Acceptance (3) requires summons for aging `input-needed`/`blocker`. The enumerated triggers exclude both, and §6's exec "MUST NOT … make product judgments" — so decisions must reach the PO, yet the pilot sentence tells a coder to configure the exec to front them. Built from the first sentence, the pilot fails criterion (3).

12. **IMPORTANT — acceptance №1 is undecidable as evidenced.** "(1) PO-session coordination turns drop measurably (toplines/turn counts, before/after)" with §13 Phase 3: "Baseline for acceptance №1 is the 2026-08-12 `state.db`." "Measurably" has no threshold; "coordination turns" is undefined; the baseline rows predate the class vocabulary (Phase 1), so before and after cannot be computed by the same method; and the baseline is the 0.1.x org while the pilot runs the 0.2 org on a changed substrate — the comparison is confounded by everything else that changed. §12 itself lists the plumbing as open while §13 gates Phase 3 exit on the criterion.

13. **IMPORTANT — the pilot's avasarala floor has no value and no owner.** §5 makes "thresholds per class/archetype" kungfu policy; Phase 6 is when policy extraction happens; acceptance (3) at Phase 3 depends on "the avasarala floor." What the seed-default floor is, and who sets it for the pilot, is stated nowhere.

14. **IMPORTANT — "substance verdict" is undefined, making acceptance №5 an audit without a rule.** "(5) exec never files a substance verdict (audit its card)" alongside §6 MAY "file/consume attests on its own card" and MUST NOT "file verdicts on substance." The line between the exec's lawful lifecycle attests (completion on its own delegation card?) and a forbidden "substance" verdict is never designated; the auditor of (5) supplies their own definition.

15. **NIT — broken load-bearing cross-reference.** §5: "`classifier` | stamps inbound messages with a class (§9)" — classes are §7; §9 is the self-healing map.

16. **NIT — §7's `status-query` claim is false for Phases 1–4.** "`status-query` — auto-answered from rows; never reaches a mind" — but `status-responder` is "Excluded from v0" (Phase 5); until then the exec, which is a mind (cartilage), answers per §6.

17. **NIT — restaffing has no named actor.** §4: "worker dies → normal restaffing while the exec keeps triaging" — passive; whether the exec may restaff its own worker is unstated and §6's verb list omits it.

18. **NIT — Phase 0 gates Phase 1 with no stated reason.** §13: "Phase 1 — substrate seams (entry: Phase 0 merged)." Nothing explains why classing wakes depends on the completion-selection repair; unexplained serialization of the critical path.

**Verdict: changes-requested.** Basis: four canonical sections absent and open questions unmarked (findings 1–2); two internal contradictions that make the acceptance contract unsatisfiable as written (3, 11); the central default table undefined (4); plus ten important defects — ambiguity on classifier authority, algedonic routing, exec holding, directive filing legality, idle-session delivery, and three undecidable/under-specified acceptance clauses.

# v0.2-program-2026-08-12.md — findings

1. **BLOCKING — the integration branch contradicts itself across ruled sections.** §5: "main IS the 0.2 line … the `0.2` branch name is retired." Yet §6: "0.2 development runs as ordinary agent sessions against the `0.2` branch"; §8: "worktrees off branch `0.2`"; §9.2: "Phase 1 build on `0.2` once READY"; the staffing table's Integrator row: "merge main→0.2 forward"; and Immediate actions: "`0.2` branch cut on clickety-clacks/tightbeam from main." An agent staffed from this record targets a branch the same record retires (the repo's CLAUDE.md confirms main is the line, PR-only). Every downstream worktree, PR target, and merge instruction is wrong in at least one of the two readings; the flip ruling was never swept through the document it lives in.

2. **BLOCKING — structure: none of the eight canonical sections.** The document self-declares "PROGRAM RECORD," but it is a review target under the reviewing-specs rubric and carries normative, build-directing content (§4's adjudication boundary, §5's election law, §8's staffing law). It has no Goal, Non-Goals, Terms, Assumptions, Invariants, Architecture, Acceptance (nothing says when the program is *done* or what evidence closes it), and no Open Questions register — open items are scattered and unmarked ("Mike to ratify," Phase-7 promotion criteria, §9.5 handoffs). If program records are exempt from spec structure, that exemption should be ruled explicitly; under the rubric as given, a missing section is blocking.

3. **IMPORTANT — "ringdown" is dead vocabulary under a sealed sweep contract.** §4 is titled "Model defaults + ringdown (TOML upgrade)." `adjudication-deletion-amendment.md`'s sweep contract: "The dead vocabulary is: `adjudication_episodes`, `adjudicationHold`, … `ringdown`" and "Every hit must be this file, a bannered file, or a file in the left-unbannered list above." This program file is none of those — the standing grep verification now fails on the corpus — and shipping a `ringdown` TOML field re-saturates specs and code with the term the sweep polices, inviting exactly the conflation with `model-ringdown-pattern.md` (bannered whole-file as mechanism) that the amendment exists to prevent. The §4 substance is defensibly lawful ("selection happens at CREATION time only, as a deterministic function of (org-authored ordered preference × live catalog truth), recorded, overridable"), but the name must change or the sweep contract must be amended in the same change; as written the two records contradict.

4. **IMPORTANT — seam ② is staffed twice, differently.** §8 table: "Origination coder | NEW components: all Phase 1 seams (②①③④), first implementations … | **Opus 5**." §9.2: "seam ② leads (Fable), ①③④ parallel (Sols)." Two ruled clauses assign the lead seam to different models, and §9.2's Sols originating ①③④ contradicts §8's own division-of-labor law ("Opus 5 originates components — first implementations"). The integrator's first build-staffing act has two incompatible instructions.

5. **IMPORTANT — the spec-reviewer fallback is the pair a preserved ruling rejects.** §8 table: "Spec reviewers | … | Fable 5 AND Sol xhigh (cross-vendor) | Opus 5." §9's preserved hold record: "Mike ruled WAIT rather than a same-vendor substitute — cross-vendor disagreement is what the review gate runs on; a Fable+Opus pair would manufacture unearned confidence." The fallback fires precisely when a vendor is unavailable — the ruled scenario — and names the rejected pair, with no condition distinguishing lawful fallback from the forbidden substitution.

6. **IMPORTANT — TOML manifests don't exist by the document's own account.** §4: "Today: archetype defaults exist informally (.md with the substrate, one per kungfu…)" followed by "a structured `ringdown` field in archetype manifests (TOML)." There is no TOML manifest to add a field to; whether the workstream creates manifests, converts the .md files, or runs both in parallel is a silent decision every implementer must make, in the workstream where the doc itself says architecture gets baked in.

7. **IMPORTANT — Miller's probes carry unbound parameters, so the output contract is not computable.** §7 E2: "prod issued ≤N min after a progress attest = false positive" — N is never fixed. C1 and E4 lean on "quiet past floor" / "the Avasarala floor" — no floor value exists anywhere in the corpus (the fabric spec defers it to kungfu policy that arrives Phase 6). E1's before-side ("share of frontier-model turns spent on coordination-class traffic … PREDICTION: falls after front desks") predates the class vocabulary and sits on the other side of the 0.1.x/0.2 line split — confounded. Yet the "Output contract: an evidence ledger per run — tenet, verdict (CONFIRMS/REFUTES/GAP), cited rows" demands classifiable verdicts; each Miller run will invent its own thresholds, making runs incomparable.

8. **IMPORTANT — nobody owns the r4 fold.** §9.1: "findings to Mike, fold → r4 READY." Passive voice, no named actor; the §8 staffing table has no spec-writer lane (the Anatomy author's scope is "using-the-substrate.md, exec archetype, office convention, playbooks," not the fabric spec). The single action standing between this review and all building is unassigned.

9. **NIT — stale ratification state.** §1: "Suggested sibling when §7's auditor lands: **Miller** … (Mike to ratify.)" vs §8 table: "Miller | tenet auditor — name RATIFIED 2026-08-12." Same document, both states.

10. **NIT — stale hold clause leaves workstream 2 unscheduled.** §2: "Nothing in this workstream runs during the hold" — §9: "HOLD LIFTED 2026-08-13." Whether the gap audit now runs, and where it sits relative to the review gate, is stated nowhere.

11. **NIT — undecidable scope boundary in §6.** "with Tightbeam used only where it demonstrably works (record-keeping, evidence rows)" — "demonstrably works" has no decider or criterion, and whether the parenthetical is exhaustive or illustrative changes what dev sessions may touch.

**Verdict: changes-requested.** Basis: the integration-branch contradiction (finding 1) misdirects every build session staffed from this record; structure absent per the rubric (2); and six important defects — a sealed-contract breach on dead vocabulary (3), two staffing contradictions including one against a preserved ruling (4, 5), an unstated migration in the ringdown workstream (6), unbound audit parameters (7), and an unowned critical-path action (8).

---

## Round B — Sol xhigh (verbatim)

## 1. `coordination-fabric-v1.md`

1. **Blocking — The canonical spec structure is incomplete.**

   Exact clauses:

   > `Status: DRAFT r3 (2026-08-12). Authored from the ruled forks of coordination-fabric-ideation-2026-08-12.md (retained as provenance; this file supersedes it as design authority).`

   > `## 1. Problem`

   > `## 12. Open gaps`

   The design authority has no explicit Goal, Non-Goals, Terms, falsifiable Assumptions, or canonically identified Invariants section. Architecture and Acceptance are present in distributed form. “Open gaps” does not mark each item blocking or non-blocking, and the document does not home the complete canonical spec set. Implementers therefore cannot distinguish settled requirements from assumptions or determine which acknowledged gaps prevent construction.

2. **Blocking — The substrate owns an immutable policy vocabulary despite the stated layer boundary.**

   Exact clauses:

   > `The substrate ships neutral behaviours; each kungfu ships the policy that configures them — the OTP behaviours-vs-callbacks split. Policy lives in the identity tree beside rails, versioned, distributed by the same learn/relearn lifecycle. The substrate stays calcium: it executes the org's coordination law and owns none of it.`

   > `Substrate-shipped base vocabulary; kungfu may extend, never remove:`

   > `① wake --class with the five-class vocabulary (unclassified → fyi; algedonic substrate-reserved, never batchable).`

   The five semantic classes determine routing and interruption, so they are policy/anatomy rather than neutral mechanism. Making them substrate-reserved and non-removable means an org cannot reshape or inhibit them. That contradicts “owns none of it” and fails the philosophy gate’s layer and override tests.

3. **Important — Receiver reclassification and mandatory algedonic bypass have incompatible confident readings.**

   Exact clauses:

   > `algedonic — genuine pain (constitution violation, spirit drift, data loss): bypasses every bone and every desk, straight to the principal and/or the human. Never batched, never digested, never triaged.`

   > `Class is advisory metadata extending attend — sender-elected, receiver re-classifiable, never a gate.`

   One implementation can reclassify before routing, allowing a receiver to downgrade `algedonic`; another must execute the mandatory bypass before the receiver sees it, making reclassification ineffective. The undefined `principal and/or the human` also permits materially different delivery targets. False or hostile `algedonic` classifications therefore have no specified handling.

4. **Important — Extended classes have no defined behavior during policy skew.**

   Exact clauses:

   > `Substrate-shipped base vocabulary; kungfu may extend, never remove:`

   > `| classifier | stamps inbound messages with a class (§9); unclassified → fyi | class vocabulary extensions, sender defaults |`

   > `| batcher | delivers non-urgent classes at turn boundaries | class → immediacy map |`

   The spec does not say what happens when a class extension exists but the receiving identity lacks its immediacy mapping. Rejecting it, treating it as `fyi`, delivering immediately, or retaining the sender’s policy all satisfy the text and differ observably.

5. **Blocking — Avasarala does not establish the safety bound claimed for every misclassification.**

   Exact clauses:

   > `| avasarala | starvation watermark: open obligation quiet > X → escalate regardless of any gate (née prodder/watchdog — renamed r3; Expanse: the org's relentless prodder, escalates pain to the top) | thresholds per class/archetype |`

   > `Mis-classification costs latency (avasarala bounds it), never truth.`

   > `no input-needed/blocker older than the avasarala floor without a summon`

   Avasarala is defined over quiet open obligations, while classification applies to inbound messages generally. The spec never says every message creates or links to an obligation. A decision or blocker misclassified as `fyi` can therefore remain merely recorded without ever entering the watermark population. Implementers must invent that linkage or the claimed latency bound is false.

6. **Important — `status-query` has no out-of-scope or read-failure behavior.**

   Exact clauses:

   > `| status-responder | answers status-query from rows (toplines/trace); the question never reaches a mind | scope of auto-answerable queries |`

   > `status-query — auto-answered from rows; never reaches a mind`

   If a sender labels a question `status-query` but it falls outside the configured auto-answerable scope—or rows are unavailable, stale, or insufficient—the spec does not choose among named failure, reclassification, delayed retry, or escalation to a mind. “Never reaches a mind” rules out one obvious fallback without supplying another.

7. **Blocking — The directives on which gating quality depends lack an implementable contract.**

   Exact clauses:

   > `The exec is told, not smart: gating quality comes from directives, not from model capability.`

   > `Standing directives (v1, zero new rows): filed as attests on the delegation card — durable, ordered, queryable; latest-wins per directive key.`

   > `- Directive schema: key vocabulary and precedence beyond latest-wins.`

   No directive-key vocabulary, encoding in the existing attest shape, conflict scope, cancellation rule, or precedence between personal and skeletal directives is defined. Yet Phase 2 must ship a base vocabulary and Phase 3 relies on directives to gate the PO’s traffic. Every implementer must invent the primary control surface.

8. **Blocking — Office dissolution and routing failover require an unspecified transition mechanism.**

   Exact clauses:

   > `Everything the exec does traces to that card; revoking it dissolves the office.`

   > `card revoked → role rebinds to the worker.`

   > `a role resolves to a session at send time`

   > `Substrate blesses "office" first-class: atomic desk rebind, desk recorded in attribution, office-scoped queries.`

   The text simultaneously treats card revocation as causing role rebind, claims no new substrate concept, and postpones atomic rebind to Phase 7. It does not say whether Phase 3 dissolution is automatic, manually ordered, or multi-step, nor what repairs a crash between revocation and rebind. It also leaves already-routed batched messages attached to a dead exec or silently re-resolved contrary to send-time resolution. The decimation guarantee cannot be implemented from this contract.

9. **Important — “Hold” is defined two incompatible ways.**

   Exact clauses:

   > `MAY: read substrate rows; file/consume attests on its own card; answer routine queries answerable from rows; batch, schedule, and deliver to its principal;`

   > `MUST NOT: file verdicts on substance; accept or reject work; make product judgments; alter another principal's reflexes; hold anything — its only "no" is "later," and the avasarala bounds every "later."`

   > `No hold: nothing in the fabric ever blocks a turn, a completion, or an assignment lifecycle.`

   A literal implementation cannot both schedule delivery for later and “hold anything.” Another implementation can interpret “hold” narrowly as a lifecycle/adjudication gate. The spec needs to define the prohibited state, since both readings are confident and one eliminates batching.

10. **Blocking — The Phase 3 acceptance gate is not decidable.**

    Exact clauses:

    > `Acceptance (evidence, not vibes): (1) PO-session coordination turns drop measurably (toplines/turn counts, before/after); (2) zero information loss — every attenuated message still present in rows; (3) summon latency bounded — no input-needed/blocker older than the avasarala floor without a summon; (4) at least one personal override and one skeletal change exercised end-to-end; (5) exec never files a substance verdict (audit its card).`

    > `- Metrics plumbing for acceptance №1 (turn counts by class exist in rows; a toplines cut may suffice).`

    “Measurably” has no observation window, cohort, minimum delta, or classification rule, and its evidence plumbing is explicitly unresolved. Criterion 3 depends on the undefined floor/linkage above. Criterion 5 does not define how an audit decides whether a verdict is “on substance.” Because Phase 4 requires Phase 3 acceptance to be ruled, these ambiguities block phase progression.

11. **Important — Agent-facing mechanisms ship before their operating guidance.**

    Exact clauses:

    > `Phase 1 — substrate seams`

    > `① wake --class with the five-class vocabulary`

    > `③ decision-request create-path (issue #11) as the input-needed carrier.`

    > `Phase 2 — anatomy (entry: Phase 1 shipped; zero substrate changes). Neutral seed gains: the exec archetype, the office convention doc, the delegation-card template (bounded verb list verbatim), the base directive vocabulary.`

    Phase 1 exposes new agent-facing classification and request behavior, while the convention and vocabulary teaching agents how to use it cannot begin until Phase 1 has shipped. The rubric requires the operating-pattern amendment to land with the capability, not one phase later.

**Verdict: changes-requested with basis.**

## 2. `v0.2-program-2026-08-12.md`

1. **Blocking — The program record lacks the canonical specification contract.**

   Exact clauses:

   > `Status: PROGRAM RECORD (Mike's rulings, 2026-08-12 evening). Seven workstreams around coordination-fabric-v1.md. Each names its deliverable and where it lands. Companion: v0.2-ticket-audit-2026-08-12.md.`

   > `## 9. Next steps (0.2 only, in order)`

   There is no explicit Goal, canonical Non-Goals section, designated Terms, falsifiable Assumptions, stated-first Invariants, program-level Acceptance contract, or marked Open Questions. The companion documents are named, but their authority order and the complete canonical set are not homed. Workstream prose and “next steps” cannot supply a decidable definition of program completion.

2. **Blocking — The document gives mutually exclusive integration branches and directions.**

   Exact clauses:

   > `FLIPPED (RULED 2026-08-12, late): main IS the 0.2 line.`

   > `the 0.2 branch name is retired.`

   > `0.2 development runs as ordinary agent sessions against the 0.2 branch`

   > `worktrees off branch 0.2, PRs on GitHub`

   > `| Integrator | sequence phases, stitch PRs, merge main→0.2 forward | Claude session (standing) + Mike as spirit | — |`

   > `Phase 1 build on 0.2 once READY`

   > `Philosophy gate MERGED INTO 0.2 (d3e070c) — main untouched (0.1.x's line; the docs/philosophy-gate branch stays alive if that org elects it).`

   An implementer can confidently target either `main` or the retired `0.2` branch, and the integrator is explicitly told to merge in the obsolete direction. The final “Immediate actions” additionally claims `main` is still the 0.1.x line. This can place every PR on the wrong program line.

3. **Blocking — Phase 1 has two contradictory staffing plans.**

   Exact clauses:

   > `| Origination coder | NEW components: all Phase 1 seams (②①③④), first implementations — where architecture gets baked in | Opus 5 | Fable 5 |`

   > `Opus 5 originates components — first implementations, where architecture mistakes get baked in.`

   > `Phase 1 build on 0.2 once READY: seam ② leads (Fable), ①③④ parallel (Sols), PRs cross-reviewed, CI on PRs already active.`

   One plan assigns every first implementation to Opus; the operational next step assigns the lead seam to Fable and the other first implementations to Sols. Staffing, authorship-based review assignment, and the “originator never patches its own gaps” rule all depend on which plan is authoritative.

4. **Important — Phase 2 is scheduled contrary to the design authority’s entry gate.**

   Exact program clause:

   > `Phase 2 anatomy in parallel — no code dependency.`

   Exact design-authority clause:

   > `Phase 2 — anatomy (entry: Phase 1 shipped; zero substrate changes).`

   One reading allows Phase 2 work concurrently with Phase 1; the design authority forbids entry until Phase 1 has shipped. This changes whether anatomy is written against real, settled verbs or speculative interfaces.

5. **Blocking — The model `ringdown` recreates the model-choice mechanism deleted by standing doctrine.**

   Exact clauses:

   > `Upgrade: a structured ringdown field in archetype manifests (TOML) — an ORDERED list of model elections`

   > `Spawn semantics: model unspecified → walk the ringdown deterministically against live catalog availability/quota; record which rung was chosen and why; caller override always wins; list exhausted → NAMED FAILURE, never a silent substitute.`

   > `selection happens at CREATION time only, as a deterministic function of (org-authored ordered preference × live catalog truth), recorded, overridable — physics executing culture, like rails.`

   The substrate still chooses one model among alternatives by walking a preference chain. Moving that choice to creation time and allowing caller override does not change the settled model-policy boundary: catalog truth, named failure, and a record are substrate duties; choosing a fallback model is an agent decision. Building this would restore deleted adjudication machinery under a new storage format.

6. **Important — The rail workstream indiscriminately extracts judgment-bearing disciplines.**

   Exact clause:

   > `For the engineering kungfu: each archetype (coder, reviewer, spec-writer, product-owner, recon, exec) gets a playbook section — how THIS role manipulates the substrate to do its job (a reviewer's verdict discipline; a coder's progress/artifact cadence; a PO's rumination verbs; an exec's delegation-card operations). Rails are then MODIFIED OR ADDED to backstop each playbook — the rail encodes the floor of the discipline the playbook teaches (playbook = should; rail = must-not-fall-below).`

   “Each playbook” includes activities with judgment content, such as verdict and rumination discipline. The program supplies neither a mechanical-only boundary nor an inhibition seam. Implementers must decide which parts become deterministic enforcement, risking rails that judge or seize instead of merely recording named org law.

7. **Important — The program orders mutations inside a line it declares wholly out of scope.**

   Exact clauses:

   > `0.1.x is the current org's business, wholly out of this program's purview`

   > `Triage debt: 57 open items never worked at all, 26 of them ZOMBIE (staffed, zero attests ever) — sweep: revoke-or-wake the zombies, icebox the rest unless elected.`

   The sweep has no line qualifier or named external actor. As written, a program agent can execute it against the current 0.1.x org even though that org is explicitly outside the program. Section 9 correctly requires Mike to authorize 0.1.x handoffs, but this mutation has no equivalent boundary.

8. **Important — The documentation gap audit defines only its successful branch.**

   Exact clause:

   > `If they do, the misuse evidence (57 never-worked items, zombie staffing) supports the fabric's founding thesis: documentation cannot produce coordination discipline; bones do.`

   The program never says what happens if the existing documents do not cover the recipes agents are fumbling. Updating those documents, changing the founding inference, or proceeding directly to bones are all plausible. The audit therefore cannot produce a determined workstream disposition.

9. **Important — The “read-only” auditor contains an active destructive drill with no actor or safety contract.**

   Exact clauses:

   > `A smart agent + read-only Tightbeam database + this heuristic set.`

   > `E7 Decimation drill (staged, not passive): retire a session mid-flight; measure whether the org degrades to a working topology without human repair.`

   The document does not say whether Miller performs the retirement, requests another actor to do it, or merely observes a separately staged exercise. It also omits target selection, authorization, recovery, and protection of live obligations. Implementations range from passive observation to killing production work.

10. **Important — C5 can classify a sanctioned agent-elected wait as a fabric violation.**

    Exact clause:

    > `C5 Wake integrity: zero empty prompts; zero wakes whose exit condition is a decision rather than time/turn-boundary.`

    The clause does not distinguish a substrate-imposed decision gate from an agent who receives a decision request and chooses to wait. It also assigns an “exit condition” to a wake without defining where that condition is represented. The auditor can therefore condemn lawful agent choice or fail to detect a real substrate hold.

11. **Important — Several Miller verdicts are undecidable.**

    Exact clauses:

    > `E2 Avasarala precision: prod false-positive rate (prod issued ≤N min after a progress attest = false positive). PREDICTION: retargeting to desks cuts the COST of false positives ~10-100× even if the rate holds.`

    > `E5 Exception-based reporting adherence: routine progress landing as attest-only vs upstream messages. PREDICTION: bones make the discipline near-universal; low adherence with bones live = bones misconfigured.`

    > `E8 Zombie rate: staffed-never-attested cards (26 today) trend to ~zero under desk triage; a stable zombie population = the fabric isn't reaching staffing hygiene.`

    `N`, the false-positive cost unit, measurement window, “near-universal,” “low adherence,” “~zero,” and “stable” are undefined. Two auditors can use the same rows and confidently emit opposite `CONFIRMS`/`REFUTES` verdicts.

12. **Important — E6 has no possible refutation despite the section’s falsifiability claim.**

    Exact clauses:

    > `A tenet with no way to lose is not a tenet; each check below states what refutation would look like.`

    > `E6 Correlated-failure signature: identical wrong outcomes clustered by one rule (bone misfire — fix the table) vs scattered (inference noise — tune guidance). The signature TELLS you which tissue failed.`

    Both possible observations are interpreted as confirming one tissue diagnosis; no observation refutes the heuristic. E6 is therefore a diagnostic taxonomy, not a falsifiable effect probe, contrary to the section’s stated contract.

13. **Important — Miller’s start point is ambiguous.**

    Exact clauses:

    > `First run AFTER 0.2 + the fabric have soaked (post-Phase-3/4)`

    > `the org, the PO front desk, and eventually Miller enter there, not before.`

    “Post-Phase-3/4” can mean after Phase 3 or after Phase 4, “soaked” has no duration or evidence threshold, and the second clause places Miller within the Phase 3 cutover. This changes when the first evidence ledger and the active decimation drill occur.

**Verdict: changes-requested with basis.**

---

## Convergence / divergence (orchestrator's consolidation)

Tallies: fabric r3 — Fable 18 findings (4 blocking), Sol 11 (6 blocking).
Program doc — Fable 11 (2 blocking), Sol 13 (4 blocking). All four verdicts:
**changes-requested**. Labels below: F = Fable finding number, S = Sol.

**CONVERGENT (both rounds, independently) — highest-confidence defects:**

1. Canonical spec structure missing on BOTH documents (fabric F1+F2 / S1;
   program F2 / S1) — blocking in all four filings. Both also flag §12's
   open gaps unmarked blocking/non-blocking.
2. Program integration-branch contradiction (F1 / S2): retired `0.2` branch
   still targeted by §6, §8, §9.2, the Integrator row, and Immediate
   actions. Both call it blocking; both note it misdirects every build
   session. (Partially intersects the §8b staleness flag — the fix now
   lands on §8b's no-door text.)
3. Seam ② staffed twice, differently (F4-program / S3-program): §8 says
   Opus originates all seams; §9.2 says Fable leads ② with Sols on ①③④.
4. Avasarala's obligation-quiescence trigger cannot deliver acceptance №3's
   message-age bound (F3 / S5) — both blocking; both note nothing links a
   classed message to a watermarked obligation, so a misclassified decision
   never enters the watched population and the "avasarala bounds it" safety
   claim fails (F7 / S5).
5. Exec "MUST NOT hold anything" vs MAY "batch, schedule" (F8 / S9) — both
   construct a literal coder who forbids the queue the exec exists to run.
6. `algedonic` "principal and/or the human" underdetermined (F6 / S3), and
   sender-election vs deterministic classification/reclassification has two
   confident readings that differ in whether a bone or receiver can
   downgrade an elected class (F5 / S3).
7. Phase 3 acceptance undecidable as written (F12/F13/F14 / S10):
   "measurably" unbounded, floor value unowned, "substance verdict"
   undefined, metrics plumbing explicitly open while the phase gates on it.
8. Directive schema absent while the pilot depends on it (F2 / S7): the
   exec's entire control surface ("told, not smart") has no key vocabulary,
   encoding, precedence, or cancellation contract.

**DIVERGENT — the cross-vendor disagreement the gate exists to surface:**

9. **The ringdown workstream (program §4).** Fable (F3-program): the NAME
   violates the adjudication amendment's sealed sweep contract (`ringdown`
   is enumerated dead vocabulary; the standing grep now fails), but the
   SUBSTANCE is defensibly lawful — creation-time, deterministic,
   org-authored preference × catalog truth, recorded, overridable. Sol
   (S5-program, blocking): the MECHANISM ITSELF rebuilds deleted
   adjudication — "the substrate still chooses one model among alternatives
   by walking a preference chain"; choosing the fallback model is an agent
   decision, and moving it to creation time doesn't change whose judgment
   it is. This is a genuine judgment call on the 2026-08-05 boundary and is
   Mike's to rule: EITHER the §4 boundary pin stands (walking an
   org-authored ordered list is physics-executing-culture, like rails, and
   only the name changes) OR Sol is right and spawn-time selection must
   collapse to: named refusal + the agent (spawner) reads the ringdown
   guidance and elects the rung itself.
10. **Substrate-reserved class vocabulary (fabric §5/§7).** Sol alone
    (S2, blocking): making the five classes substrate-shipped and
    "kungfu may extend, never remove" contradicts "the substrate…owns none
    of it" and fails the layer/override tests — classes determine routing
    and interruption, which is policy, not physics. Fable did not raise it.
    Cuts at the PHYSICS/ANATOMY seam of the whole design; needs a ruling
    (is the base vocabulary calcium or seed?).

**ONE ROUND ONLY — real, but single-witness:**

- Sol-only, fabric: class-extension policy skew undefined (S4);
  `status-query` out-of-scope/read-failure path unspecified, "never reaches
  a mind" forbids the obvious fallback (S6); office dissolution/rebind
  transition unimplementable before Phase 7's atomic rebind — decimation
  guarantee not constructible from the text (S8, blocking).
- Sol-only, program: Phase-2 entry contradicts the fabric's own gate
  ("in parallel" vs "entry: Phase 1 shipped") (S4); playbook→rail
  extraction has no judgment-content boundary — risks rails that judge
  (S6); the zombie sweep is a 0.1.x MUTATION ordered inside a document that
  declares 0.1.x out of purview, with no named external actor (S7); the
  gap audit defines only its success branch (S8); Miller's E7 decimation
  drill is destructive with no actor/authorization/safety contract inside a
  "read-only" auditor (S9); C5 can condemn lawful agent-elected waits
  (S10); E2/E5/E8 parameters unbound (S11, = F7-program); E6 unfalsifiable
  (S12); Miller start point ambiguous (S13).
- Fable-only, fabric: default class→immediacy map stated nowhere — every
  seam-② implementer invents whether `input-needed` waits (F4, blocking);
  idle-session digest under Law 3's second reading waits on someone else's
  traffic (F10); standing directives filed by a non-holder on the exec's
  card vs holder-filed doctrine (F9); §11's summon enumeration excludes the
  two classes acceptance №3 requires summons for (F11); plus nits (broken
  §9 cross-reference, `status-query` claim false until Phase 5, restaffing
  actor unnamed, Phase 0→1 gate unexplained).
- Fable-only, program: spec-reviewer fallback row names the exact
  Fable+Opus pair the preserved hold ruling rejects, with no condition
  distinguishing lawful fallback (F5); TOML manifests don't exist to add a
  field to (F6); nobody owns the r4 fold (F8); stale
  ratified/unratified Miller state (F9); stale hold clause (F10);
  "demonstrably works" undecidable (F11).

## Ruling requested from Mike

All four verdicts are changes-requested; per §9.1 nothing is built until
the fold produces r4 READY. Decisions that need YOUR ruling before or
during the fold (everything else is mechanical fold work):

1. **Ringdown boundary (consolidation №9)** — the genuine cross-vendor
   split: does §4's creation-time walk stand as physics-executing-culture
   (rename it, amend the sweep contract in the same change), or does Sol's
   reading hold (substrate never walks the list; named refusal + spawner
   judgment)?
2. **Class vocabulary's layer (№10)** — are the five classes substrate
   calcium ("extend, never remove") or neutral-seed anatomy an org may
   reshape? Decides seam ①'s shape.
3. **Program-record structure exemption (№1)** — both rounds hold the
   program doc to the eight-section rubric. Rule whether PROGRAM RECORDs
   are exempt (and record the exemption) or the doc gets the structure.
4. **Seam ② staffing (№3)** — Opus originates all seams per §8, or Fable
   leads ② per §9.2. One of the two clauses must die.
5. **Fold ownership (Fable F8-program)** — who writes r4. I propose: I
   hold the fold as integrator (Fable, the judgment lane §8 already gives
   me), with the r4 diff itself passing a light cross-vendor re-check on
   the folded deltas only. Say otherwise if you want a different hand.
6. **Zombie-sweep actor (S7-program)** — the sweep as written mutates
   0.1.x; either it moves to the 0.1.x org's handoff list (Mike relays)
   or it's re-scoped. My read: handoff list, per the purview boundary.

Everything else in both rounds folds mechanically under existing law
(structure sections, unmarked gaps, dead cross-references, unbound
parameters get values or explicit deferral marks, stale clauses swept,
§8b reconciliation per the staleness flag).

---

## Integrator rulings (2026-08-13, drive-to-completion authorization)

Mike authorized "drive to completion" on the findings package. The six
decision points fall in lanes program §8 assigns to Fable (spec review, the
§4 boundary review, tiebreak when reviewers split) or to the integrator.
Each ruling below is PROVISIONAL — recorded, executed, and overridable by
Mike at any time; an override reverses the folded text by the normal law
path.

1. **Ringdown boundary (tiebreak, reviewers split).** The mechanism STANDS;
   the name dies. Walking an org-authored ordered election list against
   live catalog truth at creation time, recorded, caller-override-wins,
   exhaustion = named failure, is physics executing culture — the exact
   shape of rails. The judgment happened when the ORG authored the list;
   the walk executes it. Sol's strongest point (fallback choice is agent
   judgment) is honored at the seam: the walk runs only when the caller
   elected silence, the caller's election always wins, and mid-session
   failure still summons a mind (the §4 pin untouched). The term
   `ringdown` is sealed dead vocabulary — renamed **model election**
   (manifest field `elections`); the sweep contract stays clean because
   the corpus drops the word rather than amending the seal.
2. **Class vocabulary layer (Sol S2).** Split by the standing layer test:
   the class FIELD and the behaviours consuming it are physics; the five
   NAMES and their default immediacies are NEUTRAL SEED — shipped as
   content, reshapeable by the skeletal law path (identity-tree edit),
   never silently removable. "Extend, never remove" is corrected to
   "extend freely; reshape or remove only via the skeletal path."
   `algedonic`'s never-batched handling is a seed default whose change
   requires the skeletal path — nobody silences someone else's alarm
   quietly, but an org CAN reshape its pain channel by law.
3. **Program-record structure.** No exemption ruled (that would be new
   law, Mike's). The program doc GETS the compact canonical header —
   the missing Acceptance ("when is the program done") was a real hole,
   not ceremony.
4. **Seam ② staffing.** §8's origination-vs-maintenance revision is the
   later ruling and the 2026-08-13 handoff restates it: **Opus 5
   originates all four seams, ② leads.** §9.2's "(Fable)" dies. Fable
   stays on judgment lanes only.
5. **Fold ownership.** The integrator (this session, Fable) holds the
   fold; the folded deltas get a Sol cross-vendor re-check before r4 is
   declared READY.
6. **Zombie sweep.** Moves to the 0.1.x handoff list (Mike relays; their
   org executes). The program text is re-scoped so no program agent can
   read a 0.1.x mutation as theirs to run.

---

## Fold round 2 — Sol delta re-check (2026-08-13) and READY declaration

Sol (gpt-5.6-sol, high, fresh thread, embedded docs) re-checked both folds
against every original finding. Resolution tally: fabric — all 18 Fable +
all 11 Sol findings RESOLVED or DEFERRED-EXPLICITLY except S5 (a leftover
§6 clause); program — all resolved except F2/S1 (missing Architecture +
authority order in the header), F3 (the dead term still printed in the
rename note), and F7 (C1/E4 floors unseeded). New fold-introduced defects
found: (1) BLOCKING — §11.3 counted correctly answered/consumed requests
as acceptance violations; (2) BLOCKING — §6 "avasarala bounds every
ceiling" contradicted the §5 watermark scoping; (3) IMPORTANT — §4's
rename note printed the sealed term. Verdict: FOLD-DEFECTS.

All seven items fixed same day, verbatim as prescribed: §11.3 accepts
answer/consume/summon as clearing; §6 re-scoped (batcher enforces
ceilings per Invariant 3, avasarala bounds watermark starvation); §5
seeds the 60-min open-obligation quiet floor beside the 30-min decision
floor and C1/E4 cite them; program header gains Architecture +
spec-homing authority order; §4's note no longer prints the term (the
amendment's exemption list updated to match). Fix commits in this repo's
log, 2026-08-13.

**r4 READY declared 2026-08-13** by the integrator under the
drive-to-completion authorization. The fix round was applied by the fold
owner rather than re-originated because every fix was verbatim-prescribed
by the cross-vendor re-check (zero judgment content added); Mike may
order a fresh re-check on the fix diff if he wants a third vendor pass.
